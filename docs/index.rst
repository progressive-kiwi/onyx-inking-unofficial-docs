Unofficial Onyx SDK Docs
========================

GitHub: https://github.com/progressive-kiwi/onyx-inking-unofficial-docs

.. warning:: AI-Generated Documentation

   This documentation was produced by an AI assistant (Claude). Knowledge was
   acquired from four sources: (1) decompiling the SDK AARs with ``javap`` to
   extract public method signatures; (2) five debug session logs recording
   every attempted fix for the blink/gesture-lock problem on a real Boox
   NoteMax; (3) the official
   `OnyxAndroidDemo <https://github.com/onyx-intl/OnyxAndroidDemo>`_ repository
   and its bundled Markdown docs; and (4) open-source apps that ship Onyx SDK
   integrations (`notable <https://github.com/Ethran/notable>`_,
   `PngNote <https://github.com/karino2/PngNote>`_).

   Method descriptions that could not be verified against source or Javadoc are
   individually marked **[AI Generated]**. Treat all unmarked content as
   best-effort reverse-engineering, not official Onyx documentation.

Unofficial Onyx SDK Docs
------------------------

Low-latency stylus input for Onyx BOOX e-ink Android devices, using the
``onyxsdk-pen`` TouchHelper API to bypass the standard MotionEvent stack and
draw directly through the device's Wacom I2C digitizer at sub-20 ms latency.

.. toctree::
   :maxdepth: 2
   :caption: Inking

   getting-started
   architecture
   sdk-setup
   touchhelper-api
   epd-rendering
   troubleshooting
   samples

.. toctree::
   :maxdepth: 1
   :caption: API Reference

   reference
   reference/pen
   reference/base
   reference/device

.. rubric:: At a glance

.. list-table::
   :widths: 35 65

   * - Target device
     - Onyx BOOX (NoteMax, Max 3, …)
   * - Android API
     - 33+ (Android 13)
   * - SDK version (current)
     - ``onyxsdk-pen:1.4.12``
   * - Maven repository
     - ``https://repo.boox.com/repository/maven-public/``
   * - Digitizer
     - Wacom I2C (``/dev/input/eventX``)
   * - Drawing waveform
     - A2 (fast, hardware-accelerated)

.. note::

   The Onyx SDK classes are **not** provided by the OS classpath. They must be
   bundled inside your APK. See :doc:`sdk-setup` for the correct Gradle
   configuration.
