TouchHelper
===========

``com.onyx.android.sdk.pen.TouchHelper``

The primary entry point for hardware-accelerated pen input. One instance
per host view. All mutating methods return ``this`` for chaining.

.. contents::
   :local:
   :depth: 1
   :class: this-will-duplicate-information-and-it-is-still-useful-here

----

Constants
---------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Constant
     - Description
   * - ``STROKE_STYLE_PENCIL``
     - [AI Generated] Style ID for pencil rendering. Pass to ``setStrokeStyle()``.
   * - ``STROKE_STYLE_FOUNTAIN``
     - [AI Generated] Style ID for fountain pen rendering.
   * - ``STROKE_STYLE_MARKER``
     - [AI Generated] Style ID for marker rendering (opaque, flat edges).
   * - ``STROKE_STYLE_NEO_BRUSH``
     - [AI Generated] Style ID for brush pen rendering via the NeoPen native renderer.
   * - ``STROKE_STYLE_CHARCOAL``
     - [AI Generated] Style ID for charcoal rendering.
   * - ``STROKE_STYLE_DASH``
     - [AI Generated] Style ID for dashed line rendering.
   * - ``STROKE_STYLE_CHARCOAL_V2``
     - [AI Generated] Style ID for charcoal V2 rendering. May be unstable on some devices.
   * - ``FEATURE_APP_TOUCH_RENDER``
     - [AI Generated] Feature flag: use app-side touch rendering (no SDK A2 pass).
   * - ``FEATURE_SF_TOUCH_RENDER``
     - [AI Generated] Feature flag: use SurfaceFlinger-based touch rendering.
   * - ``FEATURE_ALL_TOUCH_RENDER``
     - [AI Generated] Feature flag: enable both render paths simultaneously.

----

Factory methods
---------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``static TouchHelper create(View, RawInputCallback)``
     - [AI Generated] Creates a helper bound to ``view`` with the default render feature set.
       Call from a ``ViewTreeObserver.OnGlobalLayoutListener`` — the view must have real
       dimensions and a valid screen position.
   * - ``static TouchHelper create(View, boolean, RawInputCallback)``
     - [AI Generated] Creates a helper; the ``boolean`` parameter enables finger-touch input
       in addition to stylus.
   * - ``static TouchHelper create(View, int, RawInputCallback)``
     - [AI Generated] Creates a helper with an explicit render feature flag
       (``FEATURE_APP_TOUCH_RENDER``, ``FEATURE_SF_TOUCH_RENDER``, or
       ``FEATURE_ALL_TOUCH_RENDER``).

----

Region configuration
--------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``TouchHelper setLimitRect(List<Rect> limit, List<Rect> exclude)``
     - [AI Generated] Defines the active pen region and gesture exclusion zones in
       **screen-absolute** coordinates. Must be called before ``openRawDrawing()``.
   * - ``TouchHelper setLimitRect(Rect limit, List<Rect> exclude)``
     - [AI Generated] Single-rect convenience overload.
   * - ``TouchHelper setLimitRect(List<Rect> limit)``
     - [AI Generated] Sets limit rects with no exclusion zones.
   * - ``TouchHelper setExcludeRect(List<Rect> exclude)``
     - [AI Generated] Updates exclusion zones without changing the limit rects.

----

Lifecycle
---------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``TouchHelper openRawDrawing()``
     - [AI Generated] Starts the native digitizer reader thread and sets up the EPD
       event filter. Must be called after ``setLimitRect()``.
   * - ``void closeRawDrawing()``
     - [AI Generated] Stops the native reader thread and releases the EPD A2 mode claim.
       Call in ``onDetachedFromWindow()``.
   * - ``void restartRawDrawing()``
     - [AI Generated] Convenience for ``closeRawDrawing()`` + ``openRawDrawing()``.
       Useful after region changes.

----

Enable / disable
----------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``TouchHelper setRawDrawingEnabled(boolean)``
     - [AI Generated] Combined toggle: render pass + input reader +
       ``resetPenDefaultRawDrawing()``. Use on Activity ``onPause`` / ``onResume``.
   * - ``TouchHelper forceSetRawDrawingEnabled(boolean)``
     - [AI Generated] Like ``setRawDrawingEnabled`` but bypasses internal state guards.
   * - ``TouchHelper setRawDrawingRenderEnabled(boolean)``
     - [AI Generated] Toggles only the A2 render pass. Cycling ``false→true`` releases
       the EPD A2 mode claim and restores system gesture routing.
   * - ``TouchHelper setRawInputReaderEnable(boolean)``
     - [AI Generated] Toggles only the digitizer reader thread. Does **not** release the
       EPD A2 mode claim.
   * - ``boolean isRawDrawingInputEnabled()``
     - [AI Generated] Returns ``true`` if the input reader is active.
   * - ``boolean isRawDrawingRenderEnabled()``
     - [AI Generated] Returns ``true`` if the A2 render pass is active.
   * - ``boolean isRawDrawingCreated()``
     - [AI Generated] Returns ``true`` if ``openRawDrawing()`` succeeded.

----

Stroke appearance
-----------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``TouchHelper setStrokeStyle(int)``
     - [AI Generated] Sets the SDK's built-in stroke style using one of the
       ``STROKE_STYLE_*`` constants. Only affects the SDK's own A2 renderer.
   * - ``TouchHelper setStrokeColor(int)``
     - [AI Generated] Sets the ARGB colour for the SDK's A2 stroke renderer.
   * - ``TouchHelper setStrokeWidth(float)``
     - [AI Generated] Sets the base stroke width in pixels for the SDK's A2 renderer.

----

Pen / eraser configuration
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``TouchHelper setBrushRawDrawingEnabled(boolean)``
     - [AI Generated] Enables or disables raw drawing for the pen tip. Normally ``true``.
   * - ``TouchHelper setEraserRawDrawingEnabled(boolean)``
     - [AI Generated] Enables raw drawing for the eraser end. Default ``false``.
   * - ``void enableSideBtnErase(boolean)``
     - [AI Generated] When ``true``, the pen side button acts as an eraser toggle.
   * - ``void resetPenDefaultRawDrawing()``
     - [AI Generated] Resets to defaults: brush enabled, eraser disabled.
       Called internally by ``setRawDrawingEnabled``.

----

Touch / finger input
--------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``void enableFingerTouch(boolean)``
     - [AI Generated] Allows finger touch events to be processed alongside stylus events.
   * - ``void onlyEnableFingerTouch(boolean)``
     - [AI Generated] Restricts input to finger touch only, disabling stylus processing.
   * - ``boolean onTouchEvent(MotionEvent)``
     - [AI Generated] Passes a ``MotionEvent`` to the SDK pipeline. Returns ``true`` if
       consumed.

----

Refresh and timing
------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``void setPenUpRefreshEnabled(boolean)``
     - [AI Generated] When ``false``, suppresses the SDK's automatic waveform refresh on
       pen-up, eliminating the "blink" artefact. **Set to ``false`` for flicker-free inking.**
   * - ``void setPenUpRefreshTimeMs(int)``
     - [AI Generated] Delay in ms between pen-up and the automatic refresh. Only relevant
       when ``setPenUpRefreshEnabled(true)``.
   * - ``void setFilterRepeatMovePoint(boolean)``
     - [AI Generated] When ``true``, duplicate consecutive move points are filtered before
       delivery to the callback.
   * - ``void setPostInputEvent(boolean)``
     - [AI Generated] When ``true``, input events are posted to the main thread queue
       rather than delivered synchronously.

----

Region mode
-----------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``TouchHelper setSingleRegionMode()``
     - [AI Generated] Treats all limit rects as a single logical drawing region. Default.
   * - ``TouchHelper setMultiRegionMode()``
     - [AI Generated] Treats each limit rect as an independent region. Used with
       ``MultiViewTouchHelper``.

----

Scroll / host-view interaction
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``TouchHelper setHostViewScrollListenerEnabled(boolean)``
     - [AI Generated] When ``true``, registers a scroll listener on the host view to pass
       scroll events through while the SDK captures stylus input.

----

Misc
----

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``TouchHelper bindHostView(View, RawInputCallback)``
     - [AI Generated] Rebinds the helper to a different view after creation.
   * - ``TouchHelper debugLog(boolean)``
     - [AI Generated] Enables verbose internal SDK logging.
   * - ``static void register(Object)`` / ``unregister(Object)``
     - [AI Generated] Registers / unregisters on the SDK's internal EventBus for
       ``PenActiveEvent`` / ``PenDeactivateEvent`` notifications.
