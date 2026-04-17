TouchHelper API
===============

Complete reference for ``TouchHelper`` lifecycle, methods, and callbacks,
with working Kotlin examples.

Lifecycle state machine
-----------------------

``TouchHelper`` must progress through states in order. Skipping or reversing
steps produces silent failures (no pen events, empty regions, or crashes).

.. code-block:: text

   ┌──────────┐
   │  Created  │  TouchHelper.create(view, callback)
   └─────┬────┘
         │
   ┌─────▼──────┐
   │ Configured  │  setLimitRect(limitRects, excludeRects)
   └─────┬──────┘
         │
   ┌─────▼──────┐
   │   Opened   │  openRawDrawing()
   └─────┬──────┘
         │
   ┌─────▼──────┐
   │  Active    │  setRawDrawingEnabled(true)   ← pen events flow
   └─────┬──────┘
         │ pause/resume
   ┌─────▼──────┐
   │  Paused    │  setRawDrawingEnabled(false)  ← pen events suspended
   └─────┬──────┘
         │
   ┌─────▼──────┐
   │  Closed    │  closeRawDrawing()            ← native thread stopped
   └────────────┘

Creating the helper
-------------------

.. code-block:: kotlin

   val helper: TouchHelper = TouchHelper.create(view, callback)

``view`` must be attached to a window and have non-zero dimensions. Create
the helper inside a ``ViewTreeObserver.OnGlobalLayoutListener`` to guarantee
these conditions.

Setting the active region
--------------------------

.. code-block:: kotlin

   fun setLimitRect(view: View, helper: TouchHelper) {
       val screenRect = Rect()
       val excludeRects = mutableListOf<Rect>()

       if (!view.getGlobalVisibleRect(screenRect) || screenRect.isEmpty) return

       // Exclude system gesture strips so swipe-up/down still work.
       // Use insets from WindowInsetsCompat; fall back to safe minimums in
       // fullscreen mode where insets report zero.
       val density = view.resources.displayMetrics.density
       val w = view.rootView.width
       val h = view.rootView.height
       val insets = ViewCompat.getRootWindowInsets(view)
           ?.getInsets(WindowInsetsCompat.Type.systemGestures())
       val bottom = maxOf(insets?.bottom ?: 0, (40 * density).toInt())
       val top    = maxOf(insets?.top    ?: 0, (24 * density).toInt())
       excludeRects.add(Rect(0, h - bottom, w, h))   // home gesture strip
       excludeRects.add(Rect(0, 0, w, top))           // notification pull-down

       helper.setLimitRect(mutableListOf(screenRect), excludeRects)
   }

.. important::

   ``setLimitRect`` takes **screen-absolute** coordinates. The SDK maps these
   to the digitizer's native coordinate space internally via
   ``EpdController.mapToRawTouchPoint``. Passing view-local coordinates
   (``Rect(0, 0, view.width, view.height)``) produces an incorrect
   (possibly empty) hardware event filter.

Opening and enabling
---------------------

After ``setLimitRect``, open and enable in sequence:

.. code-block:: kotlin

   helper.setLimitRect(limitRects, excludeRects)
   helper.openRawDrawing()
   helper.setRawDrawingRenderEnabled(true)   // SDK renders A2 live
   helper.setPenUpRefreshEnabled(false)      // suppress pen-up blink
   helper.setRawDrawingEnabled(true)         // start accepting pen events

Handling view size changes
---------------------------

If the view is resized (e.g. keyboard shown, split-screen), update the region:

.. code-block:: kotlin

   override fun onSizeChanged(w: Int, h: Int, oldW: Int, oldH: Int) {
       super.onSizeChanged(w, h, oldW, oldH)
       if (w <= 0 || h <= 0 || touchHelper == null) return
       touchHelper?.apply {
           setRawDrawingEnabled(false)
           closeRawDrawing()
           setLimitRect(view, this)
           openRawDrawing()
           setRawDrawingEnabled(true)
       }
   }

The ``close → setLimitRect → open`` sequence is required by the SDK; updating
``setLimitRect`` without closing first has no effect.

Activity lifecycle integration
--------------------------------

.. code-block:: kotlin

   // Activity or Fragment:
   override fun onResume() {
       super.onResume()
       inkView.onResume()
   }

   override fun onPause() {
       inkView.onPause()
       super.onPause()
   }

   // InkView:
   fun onResume() = touchHelper?.setRawDrawingEnabled(true)
   fun onPause()  = touchHelper?.setRawDrawingEnabled(false)

Cleanup
-------

.. code-block:: kotlin

   override fun onDetachedFromWindow() {
       touchHelper?.closeRawDrawing()
       touchHelper = null
       super.onDetachedFromWindow()
   }

Implementing RawInputCallback
------------------------------

All eight abstract methods must be overridden (the SDK uses an abstract class,
not an interface):

.. code-block:: kotlin

   val callback = object : RawInputCallback() {

       // Pen touches surface
       override fun onBeginRawDrawing(b: Boolean, p: TouchPoint) {}

       // Called for each sampled point during the stroke
       override fun onRawDrawingTouchPointMoveReceived(p: TouchPoint) {
           // Track points for your own preview rendering if needed.
           // The SDK's A2 waveform already renders the stroke visually;
           // you only need to record points here if you draw on your own Canvas.
       }

       // Pen lifts
       override fun onEndRawDrawing(b: Boolean, p: TouchPoint) {}

       // Full stroke delivered on pen-up
       override fun onRawDrawingTouchPointListReceived(list: TouchPointList) {
           val points = list.points.map { Point(it.x, it.y, it.pressure) }
           // Commit to your model, then call postInvalidate() so the Canvas
           // is repainted before the SDK's A2 buffer clears.
           commitStroke(points)
           postInvalidate()
       }

       // Eraser-end equivalents (implement as no-ops if erasing not supported)
       override fun onBeginRawErasing(b: Boolean, p: TouchPoint) {}
       override fun onEndRawErasing(b: Boolean, p: TouchPoint) {}
       override fun onRawErasingTouchPointMoveReceived(p: TouchPoint) {}
       override fun onRawErasingTouchPointListReceived(list: TouchPointList) {}
   }

TouchPointList
--------------

``TouchPointList.points`` returns a ``List<TouchPoint>``. Each ``TouchPoint``
has:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Field
     - Type
     - Notes
   * - ``x``
     - ``Float``
     - Screen-absolute X, matches ``getGlobalVisibleRect`` space
   * - ``y``
     - ``Float``
     - Screen-absolute Y
   * - ``pressure``
     - ``Float``
     - 0.0 – 1.0 (normalised from digitizer range)
   * - ``size``
     - ``Float``
     - Contact area (pen tip size)
   * - ``timestamp``
     - ``Long``
     - Milliseconds since boot

Handling the ``Any?`` type wrapper
------------------------------------

If your module compiles without the Onyx SDK (e.g. a shared module used by
both Boox and non-Boox product variants), store ``TouchHelper`` as ``Any?``
and cast at the call site. This avoids ``NoClassDefFoundError`` on devices
where the SDK is absent:

.. code-block:: kotlin

   // Stored as Any? so InkView.class has no direct TouchHelper type reference
   private var touchHelper: Any? = null

   // At call site, inside a try/catch:
   @Suppress("UNCHECKED_CAST")
   (touchHelper as? TouchHelper)?.setRawDrawingEnabled(true)

Encapsulate all SDK calls in a separate object (e.g. ``OnyxPen``) that
is only referenced from Boox-specific code paths:

.. code-block:: kotlin

   object OnyxPen {
       fun setRawDrawingEnabled(helper: Any?, enabled: Boolean) {
           try {
               @Suppress("UNCHECKED_CAST")
               (helper as TouchHelper?)?.setRawDrawingEnabled(enabled)
           } catch (_: Throwable) {}
       }
       // … other thin wrappers
   }

Pen shape classes
-----------------

``onyxsdk-pen`` ships several ``Neo*Pen`` classes that apply different stroke
rendering styles using the SDK's own A2 renderer:

* ``NeoBallpointPen``
* ``NeoBrushPen`` (may be unstable on some devices)
* ``NeoCharcoalPen`` / ``NeoCharcoalPenV2`` (may crash, disabled by default
  in some third-party apps)
* ``NeoFountainPen``
* ``NeoMarkerPen`` (may be unstable)
* ``NeoPencilPen``
* ``NeoSquarePen``

These are used with ``MultiViewTouchHelper`` or passed to ``TouchHelper`` as
brush configuration. If you render strokes on your own ``Canvas`` (setting
``setRawDrawingRenderEnabled(false)``), these classes are not relevant.

MultiViewTouchHelper
---------------------

``com.onyx.android.sdk.pen.multiview.MultiViewTouchHelper`` manages multiple
view regions simultaneously and handles view lifecycle events automatically.
It is used by Onyx's own note application when multiple canvas views are on
screen. For single-view use cases, plain ``TouchHelper`` is sufficient.
