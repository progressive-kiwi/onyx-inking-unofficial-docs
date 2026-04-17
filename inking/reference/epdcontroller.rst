EpdController
=============

``com.onyx.android.sdk.api.device.epd.EpdController``

Abstract class (all methods static) providing low-level EPD display control.
Hidden API — requires the ``hiddenapibypass`` library to be initialised before
use. See :ref:`hidden-api-bypass`.

.. contents::
   :local:
   :depth: 1
   :class: this-will-duplicate-information-and-it-is-still-useful-here

----

Waveform control
----------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``static void invalidate(View, UpdateMode)``
     - [AI Generated] Triggers an immediate EPD refresh of the entire view using the
       specified waveform.
   * - ``static void invalidate(View, int x, int y, int w, int h, UpdateMode)``
     - [AI Generated] Triggers a partial EPD refresh of the given screen-absolute rect.
   * - ``static void postInvalidate(View, UpdateMode)``
     - [AI Generated] Schedules an EPD refresh from a background thread.
   * - ``static void refreshScreen(View, UpdateMode)``
     - [AI Generated] Full-screen refresh. Equivalent to ``invalidate`` on the root view.
   * - ``static void refreshScreenRegion(View, int x, int y, int w, int h, UpdateMode)``
     - [AI Generated] Partial refresh of a screen region.
   * - ``static void applyGCOnce()``
     - [AI Generated] Queues a single GC refresh on the next frame. Clears ghosting
       without requiring a specific view.

----

View update mode
----------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``static boolean setViewDefaultUpdateMode(View, UpdateMode)``
     - [AI Generated] Sets the persistent waveform mode for a view. All subsequent
       normal redraws use this mode until changed or reset.
   * - ``static UpdateMode getViewDefaultUpdateMode(View)``
     - [AI Generated] Returns the current default waveform for a view.
   * - ``static boolean resetViewUpdateMode(View)``
     - [AI Generated] Removes any per-view waveform override, reverting to system default.
   * - ``static void enablePost(View, int)``
     - [AI Generated] Enables EPD post-processing for the view. Pass ``1`` to activate.
       Required for ``HAND_WRITING_REPAINT_MODE`` to function correctly.
   * - ``static void enablePost(int)``
     - [AI Generated] System-wide post-processing toggle. Prefer the per-view overload.

----

Transient and scoped updates
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``static boolean applyTransientUpdate(UpdateMode)``
     - [AI Generated] Applies a temporary waveform for the next redraw only. Reverts
       automatically after one frame. Useful for suppressing artefacts during mode
       transitions.
   * - ``static boolean clearTransientUpdate(View, boolean)``
     - [AI Generated] Clears a previously set transient waveform.
   * - ``static boolean applyAppScopeUpdate(String pkg, boolean, boolean, UpdateMode, int)``
     - [AI Generated] Sets a waveform override scoped to a specific package. Persists
       until ``clearAppScopeUpdate()`` is called.
   * - ``static boolean clearAppScopeUpdate()``
     - [AI Generated] Removes the current app-scope waveform override.

----

Display hold / bypass
----------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``static void holdDisplay(boolean hold, UpdateMode, int durationMs)``
     - [AI Generated] When ``hold=true``, freezes display output for up to
       ``durationMs`` ms, suppressing EPD updates. Can hide render-cycle flicker.
   * - ``static void byPass(int)``
     - [AI Generated] Low-level display bypass control. Undocumented.

----

Handwriting repaint
-------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``static void handwritingRepaint(View, int x, int y, int w, int h)``
     - [AI Generated] Issues a partial repaint using the handwriting waveform.
   * - ``static void handwritingRepaint(View, Rect)``
     - [AI Generated] Rect-based overload.
   * - ``static void enterScribbleMode(View)``
     - [AI Generated] Puts the EPD driver into scribble (handwriting) mode for the view.
       The SDK calls this internally around raw drawing sessions.
   * - ``static void leaveScribbleMode(View)``
     - [AI Generated] Exits scribble mode for the view.

----

Coordinate mapping
------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``static RectF mapToRawTouchPoint(View, RectF)``
     - [AI Generated] Converts a screen-space rect to the pen digitizer's native
       coordinate space. Returns empty if ``Device.currentDevice()`` failed (hidden API
       not unblocked).
   * - ``static void mapToRawTouchPoint(View, float[] in, float[] out)``
     - [AI Generated] Point-array overload.
   * - ``static void mapFromRawTouchPoint(View, float[] in, float[] out)``
     - [AI Generated] Inverse: digitizer native → screen space.
   * - ``static float getTouchWidth()`` / ``getTouchHeight()``
     - [AI Generated] Pen digitizer native resolution (may differ from display).

----

CTP (Capacitive Touch Panel) control
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``static void setAppCTPDisableRegion(Context, Rect[])``
     - [AI Generated] Disables capacitive finger touch in the specified screen regions
       while leaving stylus input active. Useful to prevent accidental palm touches.
   * - ``static void appResetCTPDisableRegion(Context)``
     - [AI Generated] Removes all app-level CTP disable regions.
   * - ``static void powerCTP(boolean)``
     - [AI Generated] Powers the capacitive touch panel on or off.
