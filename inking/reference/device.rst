onyxsdk-device
==============

:Artifact: ``com.onyx.android.sdk:onyxsdk-device:1.2.31``
:Root package: ``com.onyx.android.sdk.api.device``
:Last release: February 2026

Low-level EPD hardware control. Waveform selection, partial and full screen
refreshes, display-hold freezing, front-light brightness, and coordinate
mapping between screen space and the digitizer's native space.

Most classes in this module are **hidden APIs** and require the
``hiddenapibypass`` library to be initialised in ``Application.attachBaseContext``
before any class is loaded — see :ref:`hidden-api-bypass`.

.. toctree::
   :caption: Classes

   epdcontroller
   updatemode
   updateoption
   refreshtype

.. list-table::
   :header-rows: 1
   :widths: 36 38 26

   * - Class
     - Responsibility
     - Package
   * - :doc:`epdcontroller`
     - Static EPD display controller: waveform selection, partial/full
       refreshes, display-hold, coordinate mapping, CTP region management.
     - ``…api.device.epd``
   * - :doc:`updatemode`
     - Enum of EPD waveforms: ``GC``, ``A2``, ``DU``, ``REGAL``,
       ``HAND_WRITING_REPAINT_MODE``, and more.
     - ``…api.device.epd``
   * - :doc:`updateoption`
     - Enum for app-scope refresh mode overrides
       (``NORMAL``, ``FAST``, ``REGAL``, …).
     - ``…api.device.epd``
   * - :doc:`refreshtype`
     - Enum distinguishing GC refresh variants
       (``NORMAL_GC``, ``DEEP_GC``).
     - ``…api.device.epd``
