MultiViewTouchHelper
====================

``com.onyx.android.sdk.pen.multiview.MultiViewTouchHelper``

[AI Generated] Manages pen input across multiple view regions simultaneously.
Internally owns a single :doc:`touchhelper` and routes callbacks to the correct
:doc:`limitviewinfo` based on where the pen tip lands. Used by the built-in note
app when multiple canvas panes are on screen.

For single-view apps, use plain :doc:`touchhelper` instead.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Signature
     - Description
   * - ``MultiViewTouchHelper(View container, int renderFeature)``
     - [AI Generated] Creates a helper bound to a container view. ``renderFeature``
       is one of the ``FEATURE_*`` constants from ``TouchHelper``.
   * - ``MultiViewTouchHelper bindContainerView(View)``
     - [AI Generated] Rebinds to a different container view after creation.
   * - ``void add(LimitViewInfo)``
     - [AI Generated] Registers a view region. The helper begins routing pen events
       to it immediately.
   * - ``void remove(LimitViewInfo)``
     - [AI Generated] Unregisters a view region.
   * - ``void clear()``
     - [AI Generated] Removes all registered view regions.
   * - ``void refreshLimitRect()``
     - [AI Generated] Recomputes the screen-absolute rects for all registered views.
       Call after layout changes.
   * - ``void clearActiveLimitViewInfo(boolean)``
     - [AI Generated] Clears the currently active (pen-down) region. The ``boolean``
       controls whether in-flight raw drawing is also closed.
   * - ``TouchHelper getTouchHelper()``
     - [AI Generated] Returns the underlying ``TouchHelper`` for direct configuration
       (stroke style, pen-up refresh, etc.).
   * - ``void addExcludeView(View)`` / ``addExcludeView(List<View>)``
     - [AI Generated] Adds views whose screen rects should be excluded from pen input
       (e.g. overlay buttons).
   * - ``void removeExcludeView(View)`` / ``removeExcludeView(List<View>)``
     - [AI Generated] Removes previously excluded views.
