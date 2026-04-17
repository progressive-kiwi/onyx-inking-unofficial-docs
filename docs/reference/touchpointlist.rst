TouchPointList
==============

``com.onyx.android.sdk.pen.data.TouchPointList``

An ordered, mutable list of :doc:`touchpoint` objects representing one stroke.
Implements ``Serializable`` and ``Cloneable``.

.. contents::
   :local:
   :depth: 1
   :class: this-will-duplicate-information-and-it-is-still-useful-here

----

Constructors
------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``TouchPointList()``
     - [AI Generated] Empty list.
   * - ``TouchPointList(int capacity)``
     - [AI Generated] Empty list with pre-allocated capacity.
   * - ``TouchPointList(TouchPointList source)``
     - [AI Generated] Copy constructor.
   * - ``TouchPointList(List<TouchPoint> points)``
     - [AI Generated] Wraps an existing point list.

----

Access
------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``List<TouchPoint> getPoints()``
     - Returns the underlying point list.
   * - ``List<TouchPoint> getRenderPoints()``
     - [AI Generated] Returns a potentially smoothed or thinned version suitable for
       rendering. May differ from ``getPoints()`` depending on SDK filter settings.
   * - ``int size()``
     - Number of points in the list.
   * - ``TouchPoint get(int index)``
     - Returns the point at ``index``.
   * - ``boolean isEmpty()``
     - Returns ``true`` if the list has no points.
   * - ``Iterator<TouchPoint> iterator()``
     - Standard iterator.

----

Mutation
--------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``void add(TouchPoint)``
     - Appends a point.
   * - ``void add(int index, TouchPoint)``
     - Inserts a point at ``index``.
   * - ``void addAll(TouchPointList)``
     - Appends all points from another list.
   * - ``TouchPointList setPoints(List<TouchPoint>)``
     - Replaces the entire point list.
   * - ``void clear()``
     - Removes all points.

----

Geometric transforms
--------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``TouchPointList applyMatrix(Matrix)``
     - [AI Generated] Applies an affine transform to all points in-place. Returns ``this``.
   * - ``void scaleAllPoints(float)``
     - [AI Generated] Scales all x and y values uniformly.
   * - ``void scaleAllPoints(float sx, float sy)``
     - [AI Generated] Scales x by ``sx`` and y by ``sy``.
   * - ``void translateAllPoints(float dx, float dy)``
     - [AI Generated] Translates all points by ``(dx, dy)``.
   * - ``void rotateAllPoints(float angle, PointF pivot)``
     - [AI Generated] Rotates all points by ``angle`` degrees around ``pivot``.
   * - ``void mirrorAllPoints(MirrorType, float axis)``
     - [AI Generated] Mirrors all points across the given axis.

----

Static helpers
--------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``static TouchPointList detachPointList(TouchPointList)``
     - [AI Generated] Returns a deep copy with the internal list detached, safe to hold
       after the callback returns.
