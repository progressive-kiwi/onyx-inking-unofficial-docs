RawInputCallback
================

``com.onyx.android.sdk.pen.RawInputCallback``

Abstract base class for receiving pen events from ``TouchHelper``. All eight
abstract methods must be implemented — the SDK uses an abstract class, not an
interface.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``void onBeginRawDrawing(boolean, TouchPoint)``
     - [AI Generated] Pen tip touches the surface. The ``boolean`` indicates whether
       raw drawing is currently enabled. ``TouchPoint`` is the initial contact point.
   * - ``void onRawDrawingTouchPointMoveReceived(TouchPoint)``
     - [AI Generated] Called for each sampled point during a stroke at digitizer rate
       (often 100–200 Hz). The SDK's A2 renderer fires simultaneously — no
       ``postInvalidate()`` needed here unless running with
       ``setRawDrawingRenderEnabled(false)``.
   * - ``void onEndRawDrawing(boolean, TouchPoint)``
     - [AI Generated] Pen tip lifts. Fired before
       ``onRawDrawingTouchPointListReceived``.
   * - ``void onRawDrawingTouchPointListReceived(TouchPointList)``
     - [AI Generated] Complete stroke delivered on pen-up. Primary callback for
       persisting stroke data. Call ``postInvalidate()`` here after committing to
       your canvas model.
   * - ``void onBeginRawErasing(boolean, TouchPoint)``
     - [AI Generated] Eraser end touches the surface.
   * - ``void onRawErasingTouchPointMoveReceived(TouchPoint)``
     - [AI Generated] Per-point callback during an erasing gesture.
   * - ``void onEndRawErasing(boolean, TouchPoint)``
     - [AI Generated] Eraser end lifts.
   * - ``void onRawErasingTouchPointListReceived(TouchPointList)``
     - [AI Generated] Complete erasing stroke on eraser-up.
   * - ``void onPenActive(TouchPoint)``
     - [AI Generated] Non-abstract (no-op default). Fired when the pen hovers above
       the surface without touching. Useful for showing a cursor.
   * - ``void onPenUpRefresh(RectF)``
     - [AI Generated] Non-abstract (no-op default). Fired after the SDK's pen-up
       screen refresh with the bounding rect of the refreshed area. Only fires when
       ``setPenUpRefreshEnabled(true)``.
