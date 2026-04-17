onyxsdk-base
============

:Artifact: ``com.onyx.android.sdk:onyxsdk-base:1.7.7``
:Root package: ``com.onyx.android.sdk``
:Last release: October 2020

Foundational data types and utility helpers shared by all other SDK modules.
Contains the ``TouchPoint`` struct, note document model types, device info
helpers, storage path resolution, and screen-orientation utilities.

Because ``onyxsdk-pen`` and ``onyxsdk-device`` depend on ``onyxsdk-base``
transitively, you must add ``transitive = false`` to each Gradle dependency
block and declare ``onyxsdk-base`` explicitly — see :doc:`../sdk-setup`.

.. toctree::
   :caption: Classes

   touchpoint

.. list-table::
   :header-rows: 1
   :widths: 36 38 26

   * - Class
     - Responsibility
     - Package
   * - :doc:`touchpoint`
     - A single digitizer sample: screen-absolute x/y, pressure, size,
       tilt, and timestamp.
     - ``…sdk.data.note``
