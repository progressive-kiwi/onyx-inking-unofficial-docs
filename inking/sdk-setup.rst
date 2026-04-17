SDK Setup
=========

Gradle configuration, dependency rationale, and the hidden-API bypass required
for third-party apps on Android 10+.

Maven repositories
------------------

Add both the Boox Maven server and JitPack to your repository list:

.. code-block:: groovy

   // settings.gradle
   dependencyResolutionManagement {
       repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
       repositories {
           google()
           mavenCentral()
           maven { url 'https://repo.boox.com/repository/maven-public/' }
           maven { url 'https://jitpack.io' }
       }
   }

Dependencies
------------

.. code-block:: groovy

   // app/build.gradle
   dependencies {
       // Hidden-API bypass (required on Android 10+, non-system apps)
       implementation 'org.lsposed.hiddenapibypass:hiddenapibypass:4.3'

       // Core pen SDK
       implementation('com.onyx.android.sdk:onyxsdk-pen:1.4.12')    { transitive = false }
       implementation('com.onyx.android.sdk:onyxsdk-base:1.7.7')    { transitive = false }
       implementation('com.onyx.android.sdk:onyxsdk-device:1.2.31') { transitive = false }

       // RxJava 2 — onyxsdk internal, must be explicit when transitive = false
       implementation 'io.reactivex.rxjava2:rxjava:2.2.21'
       implementation 'io.reactivex.rxjava2:rxandroid:2.1.1'
   }

Why ``transitive = false``
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``onyxsdk-base`` POM declares two transitive dependencies that do not
exist on any reachable public Maven repository:

* ``org.apache.commons.io:commonsIO:2.5.0`` — incorrect groupId (should be
  ``commons-io:commons-io``). Gradle cannot resolve it.
* ``com.tencent:mmkv:1.0.15`` — not on Google Maven, Maven Central, or
  JitPack.

Attempting a default (transitive) build fails at dependency resolution with
``Could not resolve com.tencent:mmkv``. Adding ``transitive = false`` on all
three SDK modules skips their POM graphs entirely. RxJava 2 is the only
internal dependency you need to add back manually.

Why three modules
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - What it provides
   * - ``onyxsdk-pen``
     - ``TouchHelper``, ``RawInputCallback``, ``TouchPointList``,
       pen shape classes (``NeoBallpointPen``, etc.)
   * - ``onyxsdk-base``
     - ``DeviceFeatureUtil`` (device model detection used by ``TouchHelper``
       during init), ``ReflectUtil``, ``TouchPoint`` (1.4.x location)
   * - ``onyxsdk-device``
     - ``EpdController``, ``Device``, ``UpdateMode`` — display waveform
       control and digitizer coordinate mapping

Leaving out ``onyxsdk-base`` causes a ``ClassNotFoundException`` for
``com.onyx.android.sdk.utils.DeviceFeatureUtil`` at runtime.
Leaving out ``onyxsdk-device`` causes ``EpdController`` to fail, which
makes ``mapToRawTouchPoint`` return an empty rect and the SDK registers
a zero-area hardware event filter — no pen events are ever delivered.

Available SDK versions
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - onyxsdk-pen
     - onyxsdk-base
     - onyxsdk-device
     - Notes
   * - 1.2.1
     - (bundled)
     - 1.1.11
     - Original OnyxAndroidDemo version. ``TouchPoint`` at
       ``com.onyx.android.sdk.pen.data``. ``ReflectUtil`` crashes fatally
       on ROMs where ``VMRuntime.setHiddenApiExemptions`` is absent.
   * - 1.4.12
     - 1.7.7
     - 1.2.31
     - Current recommended version. ``TouchPoint`` moved to
       ``com.onyx.android.sdk.data.note``. ``ReflectUtil`` catches its
       own bootstrap failure gracefully. Native reader thread confirmed
       working on Android 13.
   * - 1.5.3
     - (check repo)
     - (check repo)
     - Available on repo.boox.com. Not yet widely tested with
       third-party apps.

.. _hidden-api-bypass:

Hidden-API bypass
-----------------

Background
~~~~~~~~~~

``ReflectUtil`` (inside ``onyxsdk-base``) runs a static initialiser that
attempts to call ``VMRuntime.setHiddenApiExemptions`` via reflection. This
method is on Android's hidden API list. On Android 10–12 it was accessible to
reflection-based bypass. On some Boox Android 13 ROMs the method was removed
entirely from the device's boot classpath.

Without a working bypass:

1. ``ReflectUtil.<clinit>`` throws, the class is permanently marked as
   failed-to-initialise by the JVM.
2. ``Device.currentDevice()`` cannot proceed.
3. ``EpdController.mapToRawTouchPoint()`` returns an empty ``Rect``.
4. The hardware event filter covers zero area — the digitizer never
   forwards events to the SDK.

Using ``hiddenapibypass``
~~~~~~~~~~~~~~~~~~~~~~~~~

`LSPosed/hiddenapibypass <https://github.com/LSPosed/HiddenApiBypass>`_
calls ``art::Runtime::SetHiddenApiEnforcementPolicy(kDisabled)`` directly via
JNI, bypassing the missing ``VMRuntime`` method entirely. It works on Android
9–14.

.. code-block:: kotlin

   // App.kt
   class App : Application() {
       override fun attachBaseContext(base: Context) {
           super.attachBaseContext(base)
           HiddenApiBypass.addHiddenApiExemptions("")
       }
   }

.. code-block:: xml

   <!-- AndroidManifest.xml -->
   <application android:name=".App" ...>

The call must happen in ``attachBaseContext``, not ``onCreate``. The JVM
loads class statics lazily — any code path that touches an Onyx SDK class
before ``attachBaseContext`` completes may trigger ``ReflectUtil.<clinit>``
prematurely. Common pitfalls:

* ``Class.forName("com.onyx.android.sdk.api.device.epd.EpdController")``
  in diagnostic code fires ``EpdController.<clinit>`` → permanently poisons
  the class. Remove all SDK ``Class.forName`` probes from production code.
* Static singleton initialisers in ``Application.onCreate`` that reference
  SDK types.

Alternative: ``FreeReflection``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`tiann/FreeReflection <https://github.com/tiann/FreeReflection>`_ (JitPack:
``com.github.tiann:FreeReflection:3.2.2``) uses a two-stage approach:

1. Try ``VMRuntime.setHiddenApiExemptions`` — fails on affected ROMs.
2. Load a small dex file into the boot classpath — succeeds.

Call via ``Reflection.unseal(base)`` in ``attachBaseContext``. Either library
works; ``hiddenapibypass`` is generally preferred as it is more actively
maintained and does not require JitPack.

JNI libraries
-------------

``onyxsdk-pen`` embeds ARM64 native libraries. If your app also bundles other
native code that ships ``libc++_shared.so``, add a ``pickFirst`` rule to
avoid duplicate-library build errors:

.. code-block:: groovy

   android {
       packaging {
           jniLibs {
               pickFirsts += ['**/libc++_shared.so']
           }
       }
   }

Checking what is in the APK
-----------------------------

To confirm the SDK classes are bundled after build:

.. code-block:: bash

   # Pull the installed APK
   adb shell cp /data/app/com.your.app-*/base.apk /data/local/tmp/app.apk
   adb pull /data/local/tmp/app.apk

   # Verify SDK classes are present in dex
   unzip -p app.apk classes.dex | strings | grep "TouchHelper"
   # Expected: Lcom/onyx/android/sdk/pen/TouchHelper;

If the output is empty the SDK was not bundled — re-check your Gradle
dependencies.
