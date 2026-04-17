Overview
========

Classes and methods extracted from ``onyxsdk-pen:1.4.12``,
``onyxsdk-base:1.7.7``, and ``onyxsdk-device:1.2.31`` via ``javap``.
Entries for other SDK modules are sourced from the official
`OnyxAndroidDemo <https://github.com/onyx-intl/OnyxAndroidDemo>`_ documentation.
All descriptions without official Javadoc are **[AI Generated]**.


.. rubric:: SDK Modules

All modules share the Maven group ``com.onyx.android.sdk`` and are hosted at
``https://repo.boox.com/repository/maven-public/``. Add the repository once
in your project-level ``build.gradle``; individual module deps go in the app
module. All three actively maintained modules should use ``transitive = false``
— see :doc:`sdk-setup` for the full Gradle block.

.. list-table::
   :header-rows: 1
   :widths: 26 24 12 38

   * - Artifact
     - Package prefix
     - Latest
     - Purpose
   * - :doc:`reference/pen`
     - ``com.onyx.android.sdk.pen``
     - 1.4.12
     - Stylus input via the Wacom I²C digitizer. ``TouchHelper``,
       callbacks, stroke data, multi-view support.
   * - :doc:`reference/base`
     - ``com.onyx.android.sdk``
     - 1.7.7
     - Shared data types (``TouchPoint``, note model) used across all
       other SDK modules.
   * - :doc:`reference/device`
     - ``com.onyx.android.sdk.api.device``
     - 1.2.31
     - EPD waveform control, screen refresh, front-light, device
       environment queries.
   * - ``onyxsdk-scribble``
     - ``com.onyx.android.sdk``
     - 1.0.8
     - **Deprecated.** Legacy all-in-one inking module (pre-2019).
       Superseded by ``onyxsdk-pen``.
   * - ``onyxsdk-data``
     - ``com.onyx.android.sdk``
     - 1.1.2.17
     - Cloud storage (Aliyun OSS), file download, OTA updates, and
       WeChat SDK integration.
   * - ``onyxsdk-notedata``
     - ``com.onyx.android.sdk``
     - 1.0
     - Note document model and SQLite persistence used by the
       BOOX built-in Notes app.
   * - ``onyxsdk-note``
     - ``com.onyx.android.sdk``
     - 1.0.5
     - High-level note-taking pipeline composing ``notedata`` and
       ``pen``. Rarely needed by third-party apps.

----

.. rubric:: onyxsdk-pen

:Artifact: ``com.onyx.android.sdk:onyxsdk-pen:1.4.12``
:Root package: ``com.onyx.android.sdk.pen``
:Actively maintained: yes (last release February 2026)

The core SDK for all stylus work on Boox devices. Rather than routing pen
events through the Android ``MotionEvent`` stack — which adds 50–200 ms of
system latency — ``onyxsdk-pen`` registers directly with the Wacom I²C
digitizer driver. The driver streams raw coordinate, pressure, and tilt data
at the panel's native polling rate (≥200 Hz) and renders each point using the
A2 e-ink waveform, which updates individual pixels in ~10 ms without a full
panel flash.

**When to use:** Any app that needs responsive stylus input on a Boox device.
This is the only actively maintained SDK module for pen input.

**Key concepts:**

- One :doc:`reference/touchhelper` instance per host ``View``. The helper
  owns the digitizer region claim and the A2 render session.
- Pen events arrive on a background thread in :doc:`reference/rawinputcallback`.
  Move events fire per digitizer sample; the stroke list fires once on pen-up.
- The helper renders A2 strokes to the panel hardware buffer during the stroke.
  After pen-up the app must call ``postInvalidate()`` to commit the stroke to
  its own ``Canvas`` before the SDK clears the hardware buffer.
- ``setPenUpRefreshEnabled(false)`` suppresses the SDK's automatic screen
  refresh on pen-up, preventing a visible blink between A2 and normal waveform.
  See :doc:`troubleshooting` for the full blink/gesture-lock interaction.

**Gradle:**

.. code-block:: groovy

   implementation('com.onyx.android.sdk:onyxsdk-pen:1.4.12') { transitive = false }

**Key classes:** :doc:`reference/touchhelper` · :doc:`reference/rawinputcallback`
· :doc:`reference/touchpointlist` · :doc:`reference/strokestyle`
· :doc:`reference/neopenconfig` · :doc:`reference/multiviewtouchhelper`
· :doc:`reference/limitviewinfo`

----

.. rubric:: onyxsdk-base

:Artifact: ``com.onyx.android.sdk:onyxsdk-base:1.7.7``
:Root package: ``com.onyx.android.sdk``
:Actively maintained: no (last release October 2020)

Foundation library depended on by both ``onyxsdk-pen`` and ``onyxsdk-device``.
Ships the shared data types that flow between the two: ``TouchPoint`` (a single
digitizer sample), the note document model (``NoteModel``, ``ShapeModel``), and
a collection of device utility classes.

Because both pen and device modules declare ``onyxsdk-base`` as a transitive
dependency, you must add ``transitive = false`` to each and then declare
``onyxsdk-base`` explicitly — otherwise Gradle resolves it transitively and may
pull in a different version than expected.

**Utility classes [AI Generated]:**

.. list-table::
   :header-rows: 1
   :widths: 32 68

   * - Class
     - Responsibility
   * - ``DeviceEnvironment``
     - Storage path resolution for internal and SD card; device
       locale and country code.
   * - ``DeviceInfoUtil``
     - Runtime device model, serial number, firmware version, and
       screen resolution queries.
   * - ``DeviceUtils``
     - Miscellaneous helpers: full-screen mode, keyboard state,
       vibration, screen wake lock.
   * - ``FrontLightController``
     - Cold and warm front-light brightness control (0–255) for
       devices with adjustable front illumination.

**Gradle:**

.. code-block:: groovy

   implementation('com.onyx.android.sdk:onyxsdk-base:1.7.7') { transitive = false }

**Key classes:** :doc:`reference/touchpoint`

----

.. rubric:: onyxsdk-device

:Artifact: ``com.onyx.android.sdk:onyxsdk-device:1.2.31``
:Root package: ``com.onyx.android.sdk.api.device``
:Actively maintained: yes (last release February 2026)

Low-level EPD hardware control. Every refresh on an e-ink panel is driven by a
*waveform* — a lookup table that tells each pixel which voltage sequence to
apply. Different waveforms trade speed for quality:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Waveform
     - Speed
     - Best for
   * - ``GC``
     - ~600 ms
     - Full page turns; eliminates ghosting
   * - ``DU``
     - ~260 ms
     - Fast text updates; moderate ghosting
   * - ``A2``
     - ~10 ms
     - Live pen strokes; strong ghosting, binary pixel
   * - ``REGAL``
     - ~300 ms
     - Mixed text/image with anti-ghosting heuristics
   * - ``HAND_WRITING_REPAINT_MODE``
     - ~120 ms
     - Ink view repaint after stroke commit

``onyxsdk-device`` exposes these waveforms via ``EpdController``, a static
abstract class accessed through reflection. All its methods are **hidden APIs**
(``@hide`` in AOSP) — the ``hiddenapibypass`` library must be initialised in
``Application.attachBaseContext`` before any class in this SDK is loaded. See
:ref:`hidden-api-bypass`.

**When to use:** Call ``EpdController`` directly when you need precise waveform
control — e.g., forcing GC after a page turn, holding the display frozen
during a data update, or setting ``HAND_WRITING_REPAINT_MODE`` on an ink view.
Most drawing apps need both this module and ``onyxsdk-pen``.

**Gradle:**

.. code-block:: groovy

   implementation('com.onyx.android.sdk:onyxsdk-device:1.2.31') { transitive = false }

**Key classes:** :doc:`reference/epdcontroller` · :doc:`reference/updatemode`
· :doc:`reference/updateoption` · :doc:`reference/refreshtype`

----

.. rubric:: onyxsdk-scribble (deprecated)

:Artifact: ``com.onyx.android.sdk:onyxsdk-scribble:1.0.8``
:Last release: November 2018
:Status: **Deprecated — do not use for new projects**

The predecessor to ``onyxsdk-pen``. Bundled pen input, a built-in rendering
canvas (``ScribbleView``), and EPD waveform control in a single dependency.
The design tied rendering to the SDK's own view, leaving apps with little
control over the canvas, waveform timing, or gesture interaction.

``onyxsdk-pen`` was introduced to decouple these concerns: the app owns its
``View`` and ``Canvas``, and the SDK handles only digitizer input and A2
hardware rendering. This separation is what makes blink suppression, gesture
pass-through, and custom stroke rendering possible.

**Migration:** Replace ``ScribbleView`` with your own ``View`` subclass.
Instantiate ``TouchHelper`` in ``onAttachedToWindow`` and implement
``RawInputCallback`` for stroke events. See :doc:`getting-started` for the
minimal setup.

The ``OnyxAndroidDemo`` repository contains ``scribble_*`` activities showing
the old API; they are preserved for migration reference only.

----

.. rubric:: onyxsdk-data

:Artifact: ``com.onyx.android.sdk:onyxsdk-data:1.1.2.17``
:Last release: January 2021
:Status: Maintained for existing integrations

Cloud-connected utility SDK targeting Onyx's own cloud services and Chinese
ecosystem integrations. Bundles several large third-party libraries:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Dependency
     - Purpose
   * - Aliyun OSS SDK
     - Object storage: user document sync, image upload/download.
   * - DBFlow (via jitpack)
     - SQLite ORM used for local caching of cloud metadata.
   * - Retrofit2 + OkHttp
     - REST API calls to Onyx cloud services.
   * - Alibaba FastJSON
     - JSON serialisation for API request/response models.
   * - WeChat SDK
     - OAuth login, content sharing, and in-app payment flow.

.. warning::

   Adding this module without ``transitive = false`` pulls all of the above
   into your APK. It also requires a ``jitpack.io`` Maven repository entry for
   DBFlow. Only depend on this module if your app explicitly needs Onyx cloud
   sync or WeChat integration.

**[AI Generated]** Key classes:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Class
     - Responsibility
   * - ``OssManager``
     - Aliyun OSS session lifecycle: credential refresh, upload/download
       with progress, signed URL generation, and bucket enumeration.
   * - ``FileDownloader``
     - Resumable async file download with per-chunk progress callbacks
       and error-retry logic.
   * - ``OTAManager``
     - Over-the-air firmware and app update: version check, incremental
       download, and install trigger via system broadcast.
   * - ``WechatManager``
     - WeChat SDK bridge: initialise, OAuth authorisation, share sheet,
       and payment session.
   * - ``Request``
     - Base class for Retrofit2-backed HTTP requests to Onyx cloud APIs.

**Gradle:**

.. code-block:: groovy

   implementation('com.onyx.android.sdk:onyxsdk-data:1.1.2.17') { transitive = false }
   // Also requires:
   maven { url 'https://jitpack.io' }

----

.. rubric:: onyxsdk-notedata

:Artifact: ``com.onyx.android.sdk:onyxsdk-notedata:1.0``
:Last release: October 2020
:Status: Used by Onyx system apps; not recommended for third-party use

Persistence layer for the BOOX built-in Notes application. Defines the
document/page/stroke data model and stores it in a local SQLite database via
DBFlow. The schema mirrors the note format used by the system Notes app,
allowing third-party apps to read notes created by the system app if they
share the same database path.

**[AI Generated]** Key types:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Type
     - Responsibility
   * - ``NoteModel``
     - Top-level note document: title, creation date, page list,
       cover thumbnail.
   * - ``NotePageModel``
     - A single page within a note: background template, layer list,
       page dimensions.
   * - ``ShapeModel``
     - A single stroke or shape on a page: point list, colour, width,
       stroke style, timestamp.
   * - ``NoteDrawingArgs``
     - Rendering parameters passed from the persistence layer to the
       drawing engine: zoom, pan, visible layers.

**When to use:** Only if your app must read or write notes in the same format
as the system Notes app. For custom document formats, store strokes from
``TouchPointList`` directly in your own data layer.

----

.. rubric:: onyxsdk-note

:Artifact: ``com.onyx.android.sdk:onyxsdk-note:1.0.5``
:Last release: October 2020
:Status: Used by Onyx system apps; not recommended for third-party use

High-level note-taking pipeline that composes ``onyxsdk-notedata`` (storage),
``onyxsdk-pen`` (input), and ``onyxsdk-device`` (EPD waveform) into a unified
API. Manages the full document lifecycle — create, open, save, export — plus
page rendering, stroke commit, undo/redo, and bitmap thumbnail generation.

**[AI Generated]** Key classes:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Class
     - Responsibility
   * - ``NoteManager``
     - Entry point: open/create/delete note documents, enumerate pages,
       trigger save and export (PDF, PNG).
   * - ``NoteViewHelper``
     - Connects a host ``View`` to the pen input and rendering pipeline.
       Manages ``TouchHelper`` lifecycle on behalf of the view.
   * - ``RenderContext``
     - Holds the active ``Canvas``, viewport transform, and waveform
       mode for the current render pass.
   * - ``UndoRedoManager``
     - Stroke-level undo/redo stack with configurable depth.

**When to use:** If you are building a note-taking app that must interoperate
with the system Notes app file format. Otherwise, implement your own document
model on top of ``onyxsdk-pen`` — it gives you full control over storage,
rendering, and export without taking on the system app's schema as a
dependency. See :doc:`samples` for examples of both approaches.
