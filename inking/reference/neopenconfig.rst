NeoPenConfig
============

``com.onyx.android.sdk.pen.NeoPenConfig``

[AI Generated] Configuration object for the native NeoPen renderer. Passed to
``NeoPen.initPen()`` when using brush, fountain, or charcoal pen types via the
native render path. Only required if calling ``NeoPen`` directly rather than
relying on ``TouchHelper``'s built-in stroke rendering.

.. contents::
   :local:
   :depth: 1
   :class: this-will-duplicate-information-and-it-is-still-useful-here

----

Constants
---------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Constant
     - Description
   * - ``NEOPEN_PEN_TYPE_BRUSH``
     - [AI Generated] Native brush pen type.
   * - ``NEOPEN_PEN_TYPE_FOUNTAIN``
     - [AI Generated] Native fountain pen type.
   * - ``NEOPEN_PEN_TYPE_MARKER``
     - [AI Generated] Native marker pen type.
   * - ``NEOPEN_PEN_TYPE_CHARCOAL``
     - [AI Generated] Native charcoal pen type.
   * - ``NEOPEN_PEN_TYPE_CHARCOAL_V2``
     - [AI Generated] Native charcoal V2 type. May be unstable on some devices.
   * - ``TILT_SCALE_VALUE``
     - [AI Generated] Default tilt scaling factor.

----

Properties
----------

All fields have corresponding getters and setters with fluent (``this``) returns.

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Field
     - Type
     - Description
   * - ``type``
     - ``int``
     - Pen type; one of the ``NEOPEN_PEN_TYPE_*`` constants.
   * - ``color``
     - ``int``
     - ARGB stroke colour.
   * - ``width``
     - ``float``
     - Base stroke width in pixels.
   * - ``rotateAngle``
     - ``int``
     - [AI Generated] Rotation applied to the pen tip texture (degrees).
   * - ``tiltEnabled``
     - ``boolean``
     - Whether tilt data varies stroke width.
   * - ``tiltScale``
     - ``float``
     - [AI Generated] Scaling factor for tilt influence on stroke width.
   * - ``maxTouchPressure``
     - ``float``
     - Maximum pressure value for normalisation.
