StrokeStyle
===========

``com.onyx.android.sdk.pen.style.StrokeStyle``

[AI Generated] Integer constants for the SDK's built-in stroke styles.
Mirrors the ``STROKE_STYLE_*`` constants on :doc:`touchhelper` — pass to
``TouchHelper.setStrokeStyle()``.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Constant
     - Description
   * - ``PENCIL``
     - Pencil texture. Pressure-sensitive width with a slightly rough edge.
   * - ``FOUNTAIN``
     - Fountain pen. Width varies strongly with pressure and speed.
   * - ``MARKER``
     - Marker. Flat opaque strokes, fixed width.
   * - ``NEO_BRUSH``
     - Brush pen rendered via the NeoPen native renderer. Requires
       ``NeoPenConfig`` init.
   * - ``CHARCOAL``
     - Charcoal texture. Soft edges, tilt-sensitive on supported digitizers.
   * - ``DASH``
     - Dashed line.
   * - ``CHARCOAL_V2``
     - Charcoal V2. Improved charcoal rendering. May be unstable on some devices.
