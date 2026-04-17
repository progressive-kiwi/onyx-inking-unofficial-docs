TouchPoint
==========

``com.onyx.android.sdk.data.note.TouchPoint``

A single digitizer sample. Fields are public and mutable.

.. contents::
   :local:
   :depth: 1
   :class: this-will-duplicate-information-and-it-is-still-useful-here

----

Fields
------

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Field
     - Type
     - Description
   * - ``x``
     - ``float``
     - Screen-absolute X coordinate in pixels.
   * - ``y``
     - ``float``
     - Screen-absolute Y coordinate in pixels.
   * - ``pressure``
     - ``float``
     - Normalised pen pressure, 0.0–1.0.
   * - ``size``
     - ``float``
     - Contact area / tip size.
   * - ``tiltX``
     - ``int``
     - [AI Generated] Pen tilt angle along the X axis in degrees. Populated on
       devices with tilt-capable digitizers.
   * - ``tiltY``
     - ``int``
     - [AI Generated] Pen tilt angle along the Y axis in degrees.
   * - ``timestamp``
     - ``long``
     - Milliseconds since device boot.

----

Constructors
------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``TouchPoint()``
     - [AI Generated] Zero-initialised point.
   * - ``TouchPoint(float x, float y)``
     - [AI Generated] Point with position only.
   * - ``TouchPoint(float x, float y, float pressure, float size, long timestamp)``
     - [AI Generated] Full constructor without tilt.
   * - ``TouchPoint(float x, float y, float pressure, float size, int tiltX, int tiltY, long timestamp)``
     - [AI Generated] Full constructor with tilt.
   * - ``TouchPoint(MotionEvent)``
     - [AI Generated] Constructs from the current pointer of a ``MotionEvent``.
   * - ``TouchPoint(TouchPoint)``
     - [AI Generated] Copy constructor.

----

Static helpers
--------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``static TouchPoint create(MotionEvent)``
     - [AI Generated] Constructs a point from the current event position.
   * - ``static TouchPoint fromHistorical(MotionEvent, int index)``
     - [AI Generated] Constructs a point from a historical sample in a batched
       ``MotionEvent``.
   * - ``static float getPointDistance(float x1, float y1, float x2, float y2)``
     - [AI Generated] Euclidean distance between two points.
   * - ``static float getPointAngle(TouchPoint, TouchPoint)``
     - [AI Generated] Angle between two points in degrees.
   * - ``static List<TouchPoint> renderPointArray(Matrix, List<TouchPoint>)``
     - [AI Generated] Applies a matrix transform to a point list, returning a new list.

----

Instance methods
----------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``void set(TouchPoint)``
     - [AI Generated] Copies all fields from another point into this one.
   * - ``void offset(int dx, int dy)``
     - [AI Generated] Translates the point by ``(dx, dy)``.
   * - ``void applyMatrix(Matrix)``
     - [AI Generated] Transforms x/y by the given matrix in-place.
   * - ``void translate(float dx, float dy)``
     - [AI Generated] Float-precision translate.
   * - ``TouchPoint scale(float)``
     - [AI Generated] Scales x and y by the given factor. Returns ``this``.
   * - ``TouchPoint clone()``
     - [AI Generated] Deep copy.
