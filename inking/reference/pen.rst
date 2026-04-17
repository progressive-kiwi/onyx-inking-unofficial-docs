onyxsdk-pen
===========

:Artifact: ``com.onyx.android.sdk:onyxsdk-pen:1.4.12``
:Root package: ``com.onyx.android.sdk.pen``
:Last release: February 2026

Provides hardware-accelerated stylus input for Boox devices. Routes pen events
directly from the Wacom digitizer driver, bypassing the Android ``MotionEvent``
stack for sub-20 ms latency and native A2 e-ink waveform rendering during
stroke.

.. toctree::
   :caption: Classes

   touchhelper
   rawinputcallback
   touchpointlist
   strokestyle
   neopenconfig
   multiviewtouchhelper
   limitviewinfo

.. list-table::
   :header-rows: 1
   :widths: 36 38 26

   * - Class
     - Responsibility
     - Package
   * - :doc:`touchhelper`
     - Primary entry point. Creates and manages the hardware pen input
       session for a single view: region setup, lifecycle, stroke
       appearance, render/input toggles.
     - ``…sdk.pen``
   * - :doc:`rawinputcallback`
     - Abstract callback. Implement to receive per-point move events,
       completed stroke lists, eraser events, and pen hover.
     - ``…sdk.pen``
   * - :doc:`touchpointlist`
     - Ordered list of ``TouchPoint`` objects representing one complete
       stroke. Supports geometric transforms and serialisation.
     - ``…sdk.pen.data``
   * - :doc:`strokestyle`
     - Integer constants for the SDK's built-in stroke styles
       (pencil, fountain, marker, brush, charcoal, dash).
     - ``…sdk.pen.style``
   * - :doc:`neopenconfig`
     - Configuration object for the native NeoPen renderer: pen type,
       colour, width, tilt, and pressure curve.
     - ``…sdk.pen``
   * - :doc:`multiviewtouchhelper`
     - Manages pen input across multiple view regions simultaneously.
       Routes callbacks to the correct ``LimitViewInfo`` by pen position.
     - ``…sdk.pen.multiview``
   * - :doc:`limitviewinfo`
     - Associates a ``View`` with a ``RawInputCallback`` and its
       screen-absolute limit rects. One per drawing surface under
       ``MultiViewTouchHelper``.
     - ``…sdk.pen.multiview``
