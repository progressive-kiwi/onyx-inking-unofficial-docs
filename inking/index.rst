Onyx SDK Inking
===============

Low-latency stylus input for Onyx BOOX e-ink Android devices, using the
``onyxsdk-pen`` TouchHelper API to bypass the standard MotionEvent stack and
draw directly through the device's Wacom I2C digitizer at sub-20 ms latency.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   getting-started
   architecture
   sdk-setup
   touchhelper-api
   epd-rendering
   troubleshooting
   samples

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
