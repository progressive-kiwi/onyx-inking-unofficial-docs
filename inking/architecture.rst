Architecture
============

This page describes how the Onyx pen stack works, from the physical digitizer
through to Java callbacks in your app.

Overview
--------

On Onyx BOOX devices the stylus and e-ink display share a tightly integrated
hardware pipeline. The SDK short-circuits the normal Android input stack to
deliver raw digitizer events directly to the app while simultaneously rendering
fast A2 waveform strokes in hardware — achieving end-to-end latency of
< 20 ms (vs. 50–100 ms via standard ``MotionEvent``).

.. code-block:: text

   ┌─────────────────────────────────────────────────────────────┐
   │ Physical layer                                              │
   │   Wacom I2C Digitizer  →  /dev/input/eventX (Linux evdev)  │
   └──────────────────────────────┬──────────────────────────────┘
                                  │
   ┌──────────────────────────────▼──────────────────────────────┐
   │ Onyx native layer (libtouch_reader.so, inside SDK .aar)     │
   │   RawInputReader opens /dev/input/eventX via O_RDONLY       │
   │   Reads ABS_X, ABS_Y, ABS_PRESSURE evdev events            │
   │   Maps coordinates through EpdController.mapToRawTouchPoint │
   └──────────────────────────────┬──────────────────────────────┘
                                  │
   ┌──────────────────────────────▼──────────────────────────────┐
   │ Onyx Java SDK layer                                         │
   │   TouchHelper — public API, manages lifecycle               │
   │   TouchRender  — drives A2 waveform during stroke           │
   │   RawInputCallback — your app's event callbacks             │
   └──────────────────────────────┬──────────────────────────────┘
                                  │
   ┌──────────────────────────────▼──────────────────────────────┐
   │ Your application                                            │
   │   onRawDrawingTouchPointMoveReceived — per-point            │
   │   onRawDrawingTouchPointListReceived — per-stroke           │
   │   App canvas (postInvalidate after stroke commit)           │
   └─────────────────────────────────────────────────────────────┘

Key components
--------------

TouchHelper
~~~~~~~~~~~

The central public class. You create one instance per view. It owns the
connection to the native reader thread, the A2 render state, and the
coordinate mapping.

Important methods:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Method
     - Purpose
   * - ``create(view, callback)``
     - Factory. Binds helper to a view and registers callback.
   * - ``setLimitRect(limit, exclude)``
     - Defines the active drawing region (screen-absolute coords) and
       exclusion zones (system gesture strips).
   * - ``openRawDrawing()``
     - Starts the native reader thread. Must be called after ``setLimitRect``.
   * - ``closeRawDrawing()``
     - Stops the native reader thread. Call on view detach / destroy.
   * - ``setRawDrawingEnabled(bool)``
     - Combined toggle: render + input reader + reset pen state.
       Use on Activity pause/resume.
   * - ``setRawDrawingRenderEnabled(bool)``
     - Toggle only the A2 render pass. Cycling ``false→true`` releases
       the EPD A2 mode claim and unlocks system gesture routing.
   * - ``setRawInputReaderEnable(bool)``
     - Toggle only the digitizer reader thread. Does **not** release
       the EPD A2 mode claim.
   * - ``setPenUpRefreshEnabled(bool)``
     - When ``false``, suppresses the SDK's automatic full-waveform
       screen refresh on pen-up. Eliminates the "blink" artefact.

RawInputCallback
~~~~~~~~~~~~~~~~

Abstract base class you implement to receive pen events:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Callback
     - When fired
   * - ``onBeginRawDrawing(b, p)``
     - Pen tip touches surface (pen-down).
   * - ``onRawDrawingTouchPointMoveReceived(p)``
     - Each intermediate point during a stroke. High frequency.
   * - ``onEndRawDrawing(b, p)``
     - Pen lifts (pen-up).
   * - ``onRawDrawingTouchPointListReceived(list)``
     - Complete stroke delivered as a list on pen-up.
   * - ``onBeginRawErasing / onEnd... / onRawErasing...``
     - Eraser-end equivalents of the above.

``onRawDrawingTouchPointMoveReceived`` and
``onRawDrawingTouchPointListReceived`` are both called for the same stroke.
The list callback is more convenient for persisting strokes; the move callback
is needed if you render your own per-point preview.

TouchPoint
~~~~~~~~~~

Carries ``x``, ``y``, ``pressure``, ``size``, and a timestamp for each
sampled digitizer point.

.. note::

   **Package location changed in SDK 1.4.x:**

   +-----------------+--------------------------------------------------+
   | SDK version     | Import                                           |
   +=================+==================================================+
   | ≤ 1.2.x         | ``com.onyx.android.sdk.pen.data.TouchPoint``     |
   +-----------------+--------------------------------------------------+
   | 1.4.x (current) | ``com.onyx.android.sdk.data.note.TouchPoint``    |
   +-----------------+--------------------------------------------------+

EpdController
~~~~~~~~~~~~~

Low-level EPD (Electronic Paper Display) control. Used directly only for
waveform management; the pen SDK uses it internally for coordinate mapping.
See :doc:`epd-rendering`.

Coordinate system
-----------------

The SDK digitizer coordinate system is **screen-absolute**. The origin is the
top-left corner of the physical display, not the top-left of your view.

When calling ``setLimitRect``, always use ``View.getGlobalVisibleRect(Rect)``
rather than view-local dimensions. If you pass ``Rect(0, 0, view.width,
view.height)`` the SDK maps the region to screen space and may compute an
incorrect (or empty) digitizer filter area.

.. code-block:: kotlin

   val screenRect = Rect()
   view.getGlobalVisibleRect(screenRect)  // screen-absolute ✓
   // NOT: Rect(0, 0, view.width, view.height)  // view-local ✗

Dual-rendering model
--------------------

When ``setRawDrawingRenderEnabled(true)`` the SDK renders a fast **A2**
waveform stroke directly to the EPD panel during the stroke. This is what
gives the < 20 ms visual feedback. The A2 buffer is separate from the app's
``Canvas``.

On pen-up the A2 buffer is cleared and the display reverts to the normal
waveform. Your app must then paint the finished stroke onto its own ``Canvas``
(via ``postInvalidate()``) before the A2 clear is visible. The timing is:

.. code-block:: text

   onRawDrawingTouchPointListReceived  ← commit stroke to app canvas
       postInvalidate()                ← schedule Canvas redraw
   (SDK clears A2 buffer)              ← display shows app canvas instead
   (next onDraw fires)                 ← canvas redrawn with committed stroke

The ``setPenUpRefreshEnabled(false)`` flag prevents the SDK from issuing an
explicit EPD refresh on pen-up, which would cause a visible waveform-change
flash ("blink") if your canvas is not yet repainted.

Gesture interaction
-------------------

Onyx's gesture navigation (swipe-up for home, swipe-down for notifications)
shares the same digitizer hardware as the stylus. When the SDK holds the
EPD panel in A2 mode, the system gesture recogniser cannot claim its input
path — gestures stop working until the A2 claim is released.

The A2 claim is released by cycling ``setRawDrawingRenderEnabled(false →
true)``. This is the only known mechanism as of SDK 1.4.12. See
:doc:`troubleshooting` for the current workaround status.

Module dependency graph
-----------------------

.. code-block:: text

   onyxsdk-pen:1.4.12
     └─ (internal) onyxsdk-base:1.7.7      ← DeviceFeatureUtil, ReflectUtil
         └─ (internal) onyxsdk-device:1.2.31  ← EpdController, Device

All three modules must be on your classpath. The SDK does not declare these
as resolvable transitive Maven deps (its ``pom.xml`` references internal
artifact IDs that do not exist on public repos), so all three must be listed
explicitly with ``transitive = false``.

System app vs user app
----------------------

Onyx's own note application (``com.onyx.android.note``) ships in
``/system/app/`` signed with the platform key. System apps:

* Bypass all Android hidden-API enforcement
* Have the ``SYSTEM`` package manager flag
* May hold additional Binder permissions for the pen subsystem

Third-party apps have none of these. The hidden-API bypass library
(``hiddenapibypass``) bridges most of the gap, but certain platform-internal
APIs (``android.onyx.hardware.DeviceController``,
``android.onyx.optimization.Constant``) remain inaccessible. The pen SDK's
``TouchHelper`` surface works fine for user apps as long as the hidden-API
bypass runs first.
