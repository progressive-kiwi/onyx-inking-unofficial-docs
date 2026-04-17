EPD Rendering
=============

.. note::

   **EPD** stands for *Electrophoretic Display* — the technology behind e-ink
   screens. Charged pigment particles migrate through a fluid in response to an
   electric field, producing the high-contrast, paper-like image characteristic
   of BOOX devices.

How the e-ink display waveforms work, how the SDK interacts with them, and
how to control them from your app via ``EpdController``.

EPD waveform basics
-------------------

E-ink displays do not have a fixed refresh cycle. Each screen update specifies
a **waveform** (update mode) that trades visual quality for speed:

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Waveform
     - Speed
     - Description
   * - ``GC`` (Grayscale Clear)
     - ~700 ms
     - Full black-flash clear then redraw. Eliminates all ghosting.
       "SNOW Field" in the Boox UI. Use on page turns.
   * - ``A2``
     - ~20–30 ms
     - Two-level (black/white) fast update. No grey. Used by the SDK
       for live stroke rendering.
   * - ``DU`` (Direct Update)
     - ~120 ms
     - Transition from any grey to black/white only. Fast, no flash.
   * - ``REGAL``
     - ~300 ms
     - HD waveform, preserves greyscale. Default display mode.
   * - ``HAND_WRITING_REPAINT_MODE``
     - ~30–50 ms
     - Optimised for incremental handwriting. Repaints only the
       changed region using a partial A2-like pass.

How the SDK uses waveforms
---------------------------

During a stroke (pen down → pen up):

* The SDK drives the EPD in **A2** mode via ``TouchRender``. Each new segment
  is pushed as a partial update covering only the bounding box of the new
  points. This is why drawing feels instantaneous.

On pen-up, without ``setPenUpRefreshEnabled(false)``:

* The SDK issues a full waveform refresh to transition back from A2 to the
  view's normal mode (REGAL or HAND_WRITING_REPAINT_MODE). This transition
  is visible as a brief darkening or flash ("blink").

With ``setPenUpRefreshEnabled(false)``:

* The SDK does **not** issue the pen-up refresh. The A2 buffer content
  stays visible. Your app must then paint the committed stroke to its own
  ``Canvas`` via ``postInvalidate()``, which triggers the next normal-mode
  redraw and seamlessly replaces the A2 content.

EpdController API
-----------------

``EpdController`` is accessed via reflection from ``EinkRefresh`` (or
directly once the class is on the classpath). The primary methods used for
inking are:

.. code-block:: kotlin

   // Set the default waveform mode for a view
   EpdController.setViewDefaultUpdateMode(view, UpdateMode.HAND_WRITING_REPAINT_MODE)

   // Trigger an explicit EPD refresh with a specific waveform
   EpdController.invalidate(view, UpdateMode.GC)

   // Enable post-processing for partial updates (required for
   // HAND_WRITING_REPAINT_MODE to work correctly)
   EpdController.enablePost(view, 1)

   // Reset view to device default mode
   EpdController.resetViewUpdateMode(view)

Because these are hidden APIs, they are accessed via reflection in production
code:

.. code-block:: kotlin

   object EinkRefresh {

       private val controllerClass by lazy {
           runCatching {
               Class.forName("com.onyx.android.sdk.api.device.epd.EpdController")
           }.getOrNull()
       }

       private val updateModeClass by lazy {
           runCatching {
               Class.forName("com.onyx.android.sdk.api.device.epd.UpdateMode")
           }.getOrNull()
       }

       private fun mode(name: String): Any? {
           @Suppress("UNCHECKED_CAST")
           return (updateModeClass as? Class<Enum<*>>)
               ?.enumConstants?.firstOrNull { it.name == name }
       }

       /** Full GC refresh — eliminates ghosting. Use on page turns. */
       fun fullRefresh(view: View) {
           controllerClass
               ?.getMethod("invalidate", View::class.java, updateModeClass)
               ?.runCatching { invoke(null, view, mode("GC")) }
       }

       /**
        * Initialise the view for handwriting.
        * Sets HAND_WRITING_REPAINT_MODE (falls back to REGAL) and enables post.
        */
       fun initInkView(view: View) {
           if (!setViewMode(view, "HAND_WRITING_REPAINT_MODE"))
               setViewMode(view, "REGAL")
           controllerClass
               ?.getMethod("enablePost", View::class.java, Int::class.java)
               ?.runCatching { invoke(null, view, 1) }
       }

       /** Reset to device default when ink view is torn down. */
       fun resetMode(view: View) {
           controllerClass
               ?.getMethod("resetViewUpdateMode", View::class.java)
               ?.runCatching { invoke(null, view) }
       }

       private fun setViewMode(view: View, modeName: String): Boolean {
           val m = mode(modeName) ?: return false
           return controllerClass
               ?.getMethod("setViewDefaultUpdateMode",
                   View::class.java, updateModeClass)
               ?.runCatching { invoke(null, view, m) }
               ?.isSuccess == true
       }
   }

Call ``EinkRefresh.initInkView(view)`` after a successful ``TouchHelper``
init and ``EinkRefresh.resetMode(view)`` when the ink view is torn down.

Rendering strategy choices
---------------------------

Two rendering strategies are available. Choose based on whether you want the
SDK to own stroke rendering or your app to own it.

Strategy A — SDK renders A2 (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``setRawDrawingRenderEnabled(true)`` — SDK renders A2 live during stroke.
* ``setPenUpRefreshEnabled(false)`` — suppress SDK's pen-up refresh.
* In ``onRawDrawingTouchPointListReceived``: commit to app canvas, call
  ``postInvalidate()``.
* ``onRawDrawingTouchPointMoveReceived``: track points only, no
  ``postInvalidate()``.

.. code-block:: text

   Pen down  → SDK starts A2 render (visual feedback < 20 ms)
   Pen moves → SDK appends A2 segments; app tracks points
   Pen up    → onRawDrawingTouchPointListReceived fires
               → app commits stroke, postInvalidate()
               → next onDraw paints committed strokes
               → A2 buffer fades, canvas shows committed strokes

**Advantage:** Lowest-latency visual feedback. No per-move ``postInvalidate``
calls on the app side.

**Disadvantage:** The app canvas must be painted before the A2 buffer clears
or a brief blank flash may be visible (mitigated by ``setPenUpRefreshEnabled(false)``).

Strategy B — App owns all rendering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``setRawDrawingRenderEnabled(false)`` — SDK does not touch the display.
* In ``onRawDrawingTouchPointMoveReceived``: add point to current path,
  call ``postInvalidate()``.
* In ``onRawDrawingTouchPointListReceived``: commit stroke, call
  ``postInvalidate()``.

**Advantage:** Full control over stroke appearance (anti-aliasing,
pressure-width mapping, custom pen shapes).

**Disadvantage:** Every ``postInvalidate()`` per move triggers a normal-mode
EPD refresh. Normal mode is 100–300 ms, making the stroke visually lag far
behind the pen. This strategy is impractical for real-time drawing on e-ink.

Ghosting and the GC refresh
-----------------------------

A2 mode is a binary (black/white) waveform. After many A2 updates, grey
"ghost" images accumulate on the panel. Trigger a ``GC`` refresh to clear
them:

.. code-block:: kotlin

   // On page turn, clear all, or explicit user-triggered clean-up:
   EinkRefresh.fullRefresh(view)

The ``GC`` refresh flashes the screen black and then redraws from the
framebuffer. It is slow (~700 ms) and visually disruptive, so trigger it
only when the content changes significantly (page navigation, clear-all).

Syncthing / build cache interference
--------------------------------------

Syncthing or other file-sync tools that watch the project directory can
sync ``build/`` outputs, causing duplicate class files in dex archives:

.. code-block:: text

   > Duplicate class com.example.ActivityMainBinding found in:
       module classes.dex (…)
       module ActivityMainBinding.sync-conflict-*.class (…)

Fix: run ``./gradlew clean`` to purge cached intermediates, then add
``build/`` to the sync tool's ignore list.
