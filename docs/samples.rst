Sample Implementations
======================

Three open-source applications demonstrate real-world Onyx SDK inking
integration at varying levels of complexity. Each is a useful reference for
specific aspects of the API.

.. list-table::
   :header-rows: 1
   :widths: 22 13 13 52

   * - Project
     - Language
     - SDK version
     - Best reference for
   * - `OnyxAndroidDemo <https://github.com/onyx-intl/OnyxAndroidDemo>`_
     - Java
     - pen 1.2.1
     - Official minimal examples of every SDK feature
   * - `PngNote <https://github.com/karino2/PngNote>`_
     - Kotlin + Compose
     - pen 1.2.1
     - SurfaceView canvas, eraser throttling, Compose + SDK integration
   * - `notable <https://github.com/Ethran/notable>`_
     - Kotlin
     - pen 1.5.2
     - Full production app, latest SDK, NeoTools pen styles

----

OnyxAndroidDemo
---------------

https://github.com/onyx-intl/OnyxAndroidDemo

The **official sample repository** from Onyx International. Demonstrates
every major SDK feature in isolated, minimal Java activities.

.. list-table::
   :widths: 30 70

   * - Maintainer
     - Onyx International (official)
   * - Language
     - Java
   * - SDK versions
     - ``onyxsdk-pen:1.2.1``, ``onyxsdk-device:1.1.11``
   * - Stars / forks
     - 211 / 45
   * - Status
     - Infrequently updated; SDK versions are old but patterns are stable

.. rubric:: Key demo activities

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Activity
     - What it shows
   * - ``ScribbleTouchHelperDemoActivity``
     - ``TouchHelper`` on a ``SurfaceView``. Minimal end-to-end setup:
       ``create`` → ``setLimitRect`` → ``openRawDrawing`` → callbacks.
       The canonical "hello world" for the pen SDK.
   * - ``ScribbleWebViewDemoActivity``
     - Overlaying ink capture on a ``WebView`` — useful for PDF annotation
       or web-content inking.
   * - ``ScribbleMoveEraserDemoActivity``
     - Eraser tool implementation using the eraser callbacks in
       ``RawInputCallback``.
   * - ``ScribbleMultipleScribbleViewActivity``
     - Multiple independent drawing regions in a single Activity, showing
       ``setMultiRegionMode()`` or separate ``TouchHelper`` instances per
       view.

.. rubric:: Notes for SDK 1.4+ users

The demo uses SDK 1.2.1, which differs from the current recommended version
in two important ways:

* ``TouchPoint`` is at ``com.onyx.android.sdk.pen.data.TouchPoint`` (moved
  to ``com.onyx.android.sdk.data.note.TouchPoint`` in 1.4.x).
* ``ReflectUtil`` crashes fatally if ``VMRuntime.setHiddenApiExemptions`` is
  absent from the ROM. The hidden-API bypass (see :ref:`hidden-api-bypass`)
  is not shown in the demo — add it before adopting these patterns on
  Android 13+.

----

PngNote
-------

https://github.com/karino2/PngNote

A minimal Kotlin note-taking app that stores pages as plain PNG files. The
drawing engine in ``CanvasBoox.kt`` is one of the clearest available examples
of ``TouchHelper`` used with a ``SurfaceView`` and a real bitmap canvas.

.. list-table::
   :widths: 30 70

   * - Maintainer
     - karino2 (independent)
   * - Language
     - Kotlin, Jetpack Compose UI
   * - SDK versions
     - ``onyxsdk-pen:1.2.1`` (referenced; may be vendored)
   * - Stars / forks
     - 70 / 11
   * - Supported devices
     - BOOX Note3, Note2, Note Air, Nova2. Not compatible with Poke series.
   * - Status
     - Last release September 2021 (v0.4). Stable but unmaintained.
   * - License
     - MIT

.. rubric:: What to study in this repo

``ui/CanvasBoox.kt`` — the entire inking implementation in one file:

* **Lazy ``TouchHelper`` init** — ``private val touchHelper by lazy { TouchHelper.create(this, inputCallback) }``
* **Stroke style setup** — ``setStrokeWidth``, ``setStrokeColor``,
  ``setStrokeStyle(TouchHelper.STROKE_STYLE_PENCIL)`` called before
  ``openRawDrawing()``.
* **Eraser with throttle** — ``onRawErasingTouchPointMoveReceived``
  accumulates points and refreshes every 300 ms or 100 points, avoiding
  excessive EPD updates during erasing.
* **Jump-point filter** — skips points where ``abs(prev.y - point.y) >= 30``
  to suppress digitizer noise during fast strokes.
* **``EpdController.enablePost(view, 1)``** called during eraser init to
  enable partial-update post-processing.
* **SurfaceView lifecycle** — ``surfaceDestroyed`` calls ``closeRawDrawing()``;
  ``onRestart`` reattaches the surface callback and resumes drawing.
* **Quadratic curve rendering** — touch points drawn as ``quadTo`` paths on
  a bitmap, giving smooth curves between sampled points.

----

notable
-------

https://github.com/Ethran/notable

A maintained, production-quality note-taking app for Onyx BOOX devices.
Active fork of the archived ``olup/notable``. Uses the latest SDK version
of the three samples listed here and demonstrates NeoTools pen styles.

.. list-table::
   :widths: 30 70

   * - Maintainer
     - Ethran (community-maintained fork)
   * - Language
     - Kotlin
   * - SDK versions
     - ``onyxsdk-pen:1.5.2``, ``onyxsdk-base:1.8.4``,
       ``onyxsdk-device:1.3.3``
   * - Stars / forks
     - 194 / 31
   * - Requires
     - Android 10+ (API 29)
   * - Community
     - Discord: discord.gg/rvNHgaDmN2
   * - Status
     - Actively maintained (1 000+ commits)
   * - License
     - Open source (see repo)

.. rubric:: What to study in this repo

* **Latest SDK version** — uses pen 1.5.2 / base 1.8.4 / device 1.3.3,
  the most recent versions available at time of writing. Useful to see
  what changed from 1.4.x.
* **NeoTools pen styles** — integrates ``NeoBallpointPen``, ``NeoFountainPen``,
  etc. Note that ``NeoCharcoalPenV2``, ``NeoMarkerPen``, and ``NeoBrushPen``
  are disabled by default due to instability on some devices.
* **PDF annotation** — full PDF reading with ink overlay, making it the
  closest open-source analogue to this project's own use case.
* **Performance patterns** — fast page turns with bitmap caching, infinite
  vertical scroll, gesture controls. The codebase shows how to manage
  ``TouchHelper`` lifecycle across page/scroll events.
* **Database stroke encoding** — strokes persisted to SQLite
  (``Documents/notabledb``); the schema is documented in
  ``docs/database-structure.md`` in the repo.

.. rubric:: Stability note on NeoTools

The following pen types are present in the SDK but disabled in notable due
to crash risk on certain devices. Treat them as experimental:

* ``NeoCharcoalPenV2``
* ``NeoMarkerPen``
* ``NeoBrushPen``
