UpdateMode
==========

``com.onyx.android.sdk.api.device.epd.UpdateMode``

Enum specifying the EPD waveform for a screen update. Pass to
:doc:`epdcontroller` methods.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Value
     - Description
   * - ``None``
     - [AI Generated] No waveform / skip the EPD update.
   * - ``DU``
     - Direct Update. Fast black/white binary transition (~120 ms). No greyscale.
   * - ``DU4``
     - [AI Generated] 4-level DU variant. Faster than ``GC`` with some greyscale support.
   * - ``GU``
     - [AI Generated] Greyscale Update. Supports full greyscale at moderate speed.
   * - ``GU_FAST``
     - [AI Generated] Faster greyscale update at the cost of some quality.
   * - ``GC``
     - Grayscale Clear. Full black-flash then redraw. Eliminates all ghosting (~700 ms).
       Use on page turns or explicit clean-up.
   * - ``GCC``
     - [AI Generated] GC with additional colour correction.
   * - ``DEEP_GC``
     - [AI Generated] Extended black-flash cycle for heavily ghosted screens.
   * - ``ANIMATION``
     - [AI Generated] Fast binary animation waveform for smooth scrolling or video.
   * - ``ANIMATION_QUALITY``
     - [AI Generated] Higher quality animation waveform with some greyscale.
   * - ``ANIMATION_MONO``
     - [AI Generated] Monochrome animation waveform.
   * - ``ANIMATION_X``
     - [AI Generated] Extended animation waveform. Can be used with
       ``applyTransientUpdate`` to suppress artefacts during mode transitions.
   * - ``GC4``
     - [AI Generated] 4-level GC variant.
   * - ``REGAL``
     - HD waveform. Full greyscale. Default display mode (~300 ms).
   * - ``REGAL_D``
     - [AI Generated] REGAL with dithering.
   * - ``DU_QUALITY``
     - [AI Generated] DU with post-processing for improved quality.
   * - ``HAND_WRITING_REPAINT_MODE``
     - Optimised for incremental handwriting. Repaints only the changed region with a
       partial A2-like pass (~30–50 ms). Use with ``enablePost(view, 1)``.
