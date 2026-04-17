LimitViewInfo
=============

``com.onyx.android.sdk.pen.multiview.LimitViewInfo``

[AI Generated] Associates a ``View`` with a :doc:`rawinputcallback` and the
screen-absolute limit rects used by :doc:`multiviewtouchhelper`. One instance
per drawing surface.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``LimitViewInfo(View, RawInputCallback)``
     - [AI Generated] Constructor. The view must be attached and laid out before
       ``initLimitRect()`` is called.
   * - ``LimitViewInfo initLimitRect()``
     - [AI Generated] Computes and caches the view's current screen-absolute rect.
       Call after the view has been laid out.
   * - ``LimitViewInfo setContainerViewScreenXY(int x, int y)``
     - [AI Generated] Provides the container view's screen-absolute origin when it is
       not derivable from the view itself.
   * - ``List<Rect> getLimitRectList()``
     - [AI Generated] Returns the screen-absolute rects for this view.
   * - ``LimitViewInfo setLimitRectList(List<Rect>)``
     - [AI Generated] Manually overrides the limit rects.
   * - ``TouchPoint offSetXY(TouchPoint)``
     - [AI Generated] Translates a touch point from screen-absolute to view-local
       coordinates.
   * - ``TouchPointList offSetXY(TouchPointList)``
     - [AI Generated] Translates an entire stroke to view-local coordinates.
   * - ``boolean contains(TouchPoint)``
     - [AI Generated] Returns ``true`` if the point falls within this view's limit rect.
   * - ``boolean intersect(Rect)``
     - [AI Generated] Returns ``true`` if the given rect overlaps this view's limit rect.
