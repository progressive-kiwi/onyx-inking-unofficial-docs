Troubleshooting
===============

This page documents every failure mode encountered during development, with
root causes and fixes. Each section names the logcat tag and exact log message
where applicable.

.. contents:: On this page
   :local:
   :depth: 2

MotionEvent fallback instead of TouchHelper
--------------------------------------------

**Symptom**

.. code-block:: text

   I InkView: Ink backend: MotionEvent fallback (Onyx SDK unavailable — expect high latency)

**Cause**

``OnyxPen.createTouchHelper`` returned ``null``. This happens when:

* The SDK classes are not bundled in the APK (see :ref:`classes-not-bundled`).
* ``TouchHelper.create()`` threw an exception (check for ``OnyxPen: Onyx SDK
  init failed:`` in logcat).
* The view had zero dimensions when ``createTouchHelper`` was called (see
  :ref:`zero-dimensions`).

**Fix**

Check logcat for ``E OnyxPen:`` lines and address the specific exception.

.. _classes-not-bundled:

SDK classes not bundled (compileOnly mistake)
----------------------------------------------

**Symptom**

.. code-block:: text

   java.lang.ClassNotFoundException: com.onyx.android.sdk.pen.TouchHelper
       at dalvik.system.BaseDexClassLoader.findClass

**Cause**

The SDK dependency was declared as ``compileOnly``. This is incorrect — the
Onyx SDK classes are **not** provided by the device OS classpath. Unlike
framework libraries, they are not injected at runtime. Every APK that uses
the SDK must bundle it.

Confirm the APK contents:

.. code-block:: bash

   adb shell cp /data/app/com.your.app-*/base.apk /data/local/tmp/app.apk
   adb pull /data/local/tmp/app.apk
   unzip -p app.apk classes.dex | strings | grep "TouchHelper"
   # Must show: Lcom/onyx/android/sdk/pen/TouchHelper;
   # If empty: SDK is not bundled.

**Fix**

Change ``compileOnly`` to ``implementation`` with ``transitive = false``:

.. code-block:: groovy

   implementation('com.onyx.android.sdk:onyxsdk-pen:1.4.12')    { transitive = false }
   implementation('com.onyx.android.sdk:onyxsdk-base:1.7.7')    { transitive = false }
   implementation('com.onyx.android.sdk:onyxsdk-device:1.2.31') { transitive = false }

Transitive dependency resolution failure
-----------------------------------------

**Symptom**

.. code-block:: text

   > Could not resolve com.tencent:mmkv:1.0.15.
   > Could not resolve org.apache.commons.io:commonsIO:2.5.0.

**Cause**

``onyxsdk-base`` declares broken transitive dependencies. These artifact
coordinates do not exist on any public Maven repository.

**Fix**

Add ``{ transitive = false }`` to all three SDK modules and declare RxJava 2
explicitly:

.. code-block:: groovy

   implementation('com.onyx.android.sdk:onyxsdk-pen:1.4.12')    { transitive = false }
   implementation('com.onyx.android.sdk:onyxsdk-base:1.7.7')    { transitive = false }
   implementation('com.onyx.android.sdk:onyxsdk-device:1.2.31') { transitive = false }
   implementation 'io.reactivex.rxjava2:rxjava:2.2.21'
   implementation 'io.reactivex.rxjava2:rxandroid:2.1.1'

DeviceFeatureUtil not found
----------------------------

**Symptom**

.. code-block:: text

   java.lang.ClassNotFoundException: com.onyx.android.sdk.utils.DeviceFeatureUtil
       DexPathList: [base.apk]
   I InkView: Ink backend: MotionEvent fallback

**Cause**

``onyxsdk-base`` was omitted from the dependency list. Early setups added
``onyxsdk-pen`` and ``onyxsdk-device`` but skipped ``onyxsdk-base`` to avoid
its broken transitive deps. ``DeviceFeatureUtil`` lives in ``onyxsdk-base``
and is called during ``TouchHelper`` initialisation.

**Fix**

Add ``onyxsdk-base`` explicitly:

.. code-block:: groovy

   implementation('com.onyx.android.sdk:onyxsdk-base:1.7.7') { transitive = false }

Empty region / no pen events
------------------------------

**Symptom**

.. code-block:: text

   E RawInputReader: Empty region detected!!!!!
   E RawInputReader: Empty region detected when mapping!!!!!

Inking initialises without error but no pen events are ever delivered.

**Root cause chain**

.. code-block:: text

   ReflectUtil.<clinit>
     → calls VMRuntime.setHiddenApiExemptions (hidden API)
     → NoSuchMethodException (method absent from this Boox ROM)
     → class permanently poisoned

   Device.<clinit>
     → calls ReflectUtil.getDeclaredMethodSafely → null

   EpdController.mapToRawTouchPoint
     → Device.currentDevice() broken
     → returns empty Rect (0, 0, 0, 0)

   RawInputReader.setLimitRect
     → receives empty mapped rect
     → hardware event filter covers 0 area
     → digitizer forwards no events

This chain affects SDK 1.2.1 (where ``ReflectUtil`` failure is fatal) but
also SDK 1.4.12 if the hidden-API bypass has not been initialised in time.

**Fix**

Initialise the hidden-API bypass in ``Application.attachBaseContext`` before
any SDK class is loaded:

.. code-block:: kotlin

   class App : Application() {
       override fun attachBaseContext(base: Context) {
           super.attachBaseContext(base)
           HiddenApiBypass.addHiddenApiExemptions("")
       }
   }

After fixing, the "Empty region" lines disappear and logcat shows:

.. code-block:: text

   I RawInputReader$a: submitJob nativeRawReader pool-3-thread-1-65
   I lib_touch_reader: find path /dev/input/event3 result name onyx_emp_Wacom I2C Digitizer

.. _class-poisoning:

EpdController class poisoning by diagnostic code
-------------------------------------------------

**Symptom**

``TouchHelper.create()`` throws ``ExceptionInInitializerError`` or
``NoClassDefFoundError`` referencing ``EpdController``, even though the SDK
classes are bundled.

**Cause**

Diagnostic code earlier in startup called ``Class.forName`` on an SDK class:

.. code-block:: kotlin

   // DO NOT DO THIS — triggers EpdController.<clinit> before bypass is ready
   Class.forName("com.onyx.android.sdk.api.device.epd.EpdController")

In the JVM, if a class's static initialiser throws (e.g. ``ReflectUtil``
fails), the class is permanently marked as "failed to initialise". Every
subsequent reference to that class — including by the SDK itself — throws
``NoClassDefFoundError``. There is no recovery short of restarting the process.

**Fix**

Remove all SDK ``Class.forName`` probes. If you want to detect SDK presence,
check for the class in a safe way only after the bypass is initialised, or
rely on ``try/catch`` around ``TouchHelper.create()``.

.. _zero-dimensions:

TouchHelper created before view is laid out
--------------------------------------------

**Symptom**

.. code-block:: text

   E RawInputReader: Empty region detected!!!!!

…even though the bypass is installed. Or:

.. code-block:: text

   W OnyxPen: createTouchHelper: view has no screen rect yet, aborting

**Cause**

``TouchHelper.create()`` (or the ``setLimitRect`` that follows it) was called
in ``onAttachedToWindow`` directly, before the first layout pass. The view
dimensions are 0×0 at that point. Even with a guard ``if (view.width > 0)``
fallback of 1, this produces ``Rect(0, 0, 1, 1)`` — effectively empty after
the digitizer coordinate mapping.

**Fix**

Defer helper creation to a ``ViewTreeObserver.OnGlobalLayoutListener``:

.. code-block:: kotlin

   override fun onAttachedToWindow() {
       super.onAttachedToWindow()
       viewTreeObserver.addOnGlobalLayoutListener(object :
           ViewTreeObserver.OnGlobalLayoutListener {
           override fun onGlobalLayout() {
               viewTreeObserver.removeOnGlobalLayoutListener(this)
               if (touchHelper == null) initTouchHelper()
           }
       })
   }

setLimitRect with view-local instead of screen-absolute coordinates
-------------------------------------------------------------------

**Symptom**

SDK initialises (``submitJob nativeRawReader`` appears), digitizer is found,
but pen events produce strokes at the wrong position or are not delivered at
all on devices where the ink view does not start at (0, 0).

**Cause**

``setLimitRect`` was called with view-local coordinates:

.. code-block:: kotlin

   // WRONG — view-local
   setLimitRect(mutableListOf(Rect(0, 0, view.width, view.height)), ...)

The SDK maps this rect through ``EpdController.mapToRawTouchPoint`` which
expects screen-absolute coordinates to translate to the digitizer's native
space. View-local coordinates (which may be offset by toolbars, status bars,
etc.) produce a shifted or incorrect mapping.

**Fix**

.. code-block:: kotlin

   // CORRECT — screen-absolute
   val screenRect = Rect()
   view.getGlobalVisibleRect(screenRect)
   setLimitRect(mutableListOf(screenRect), ...)

Pen events not firing after SDK init (missing enable call)
----------------------------------------------------------

**Symptom**

``submitJob nativeRawReader`` appears in logcat. The digitizer is found.
No "Empty region" errors. But ``onBeginRawDrawing`` / ``onRawDrawingTouchPointListReceived``
are never called.

**Cause**

``openRawDrawing()`` starts the native reader thread but leaves the SDK in a
"open but not enabled" state. ``setRawDrawingEnabled(true)`` must be called
afterwards to activate event routing.

**Fix**

Ensure the full init sequence is followed in order:

.. code-block:: kotlin

   helper.setLimitRect(limitRects, excludeRects)
   helper.openRawDrawing()
   helper.setRawDrawingRenderEnabled(true)
   helper.setPenUpRefreshEnabled(false)
   helper.setRawDrawingEnabled(true)   // ← must not be omitted

System gestures broken after inking
-------------------------------------

**Symptom**

After drawing one or more strokes, Android system navigation gestures
(swipe-up for home, swipe-down for notification shade) stop responding.
Navigating away and back restores them.

**Cause**

The Onyx SDK holds the EPD panel in A2 render mode after a stroke. While A2
mode is claimed, the Boox gesture subsystem cannot use the digitizer. The A2
claim is released by cycling ``setRawDrawingRenderEnabled(false → true)``,
which also triggers an EPD refresh (and hence a visible blink).

The exact coupling between the EPD A2 claim and the gesture lock is not
documented by Onyx. It appears to be a side effect of how the Boox gesture
recogniser shares the Wacom digitizer with the pen SDK.

**Current state (SDK 1.4.12)**

There is no clean solution. The tradeoff is:

* Without render cycle: no blink, but gestures lock after each stroke.
* With render cycle: gestures restored, but each cycle causes a visible EPD
  flash.

**Workaround options**

1. **Conditional cycle on finger touch** — trigger ``setRawDrawingRenderEnabled``
   only when a finger touch is detected (``TOOL_TYPE_FINGER``). The blink
   occurs only when the user transitions from drawing to swiping, at the
   moment they lift the pen and place a finger — when it is least noticeable.

2. **``holdDisplay`` freeze** (untested) — call
   ``EpdController.holdDisplay(true, mode, ms)`` to freeze the display during
   the render cycle, then release it. If this prevents the EPD hardware from
   issuing a visible update, the cycle could proceed invisibly.

3. **SurfaceView canvas** (untested) — ``SurfaceView`` compositing is
   independent of the regular view hierarchy. The A2 layer interaction may
   differ, potentially eliminating the gesture lock entirely.

Pen panning the page instead of drawing
-----------------------------------------

**Symptom**

Pen strokes pan the underlying content (e.g. a PDF viewer) instead of drawing
ink.

**Cause**

``InkView.onTouchEvent`` returned ``false`` (or was not overriding), so pen
``MotionEvent`` events fell through to the view underneath.

When the Onyx SDK is active, the SDK handles raw pen events via its own
input channel. However, Android also delivers ``MotionEvent`` events with
``TOOL_TYPE_STYLUS`` to the normal view hierarchy. If ``InkView`` does not
consume them, the underlying view (e.g. ``AndroidPdfViewer``) receives and
acts on them.

**Fix**

In ``onTouchEvent``, consume stylus events when the SDK is active:

.. code-block:: kotlin

   override fun onTouchEvent(event: MotionEvent): Boolean {
       if (touchHelper != null) {
           // Stylus: consume here so underlying views never receive pen events.
           // Finger: pass through so page swipes and system gestures work.
           return event.getToolType(0) == MotionEvent.TOOL_TYPE_STYLUS
       }
       // … fallback MotionEvent handling
       return true
   }

Application disabled by Boox power management
-----------------------------------------------

**Symptom**

App appears to be installed but does not launch, or launches then immediately
disappears. Logcat shows:

.. code-block:: text

   ApplicationFreezeHelper: setApplicationEnabledSettingAsUser,
       packageName:com.your.app, enable: false

``pm list packages`` shows the package with ``enabled=3``
(``COMPONENT_ENABLED_STATE_DISABLED``).

**Cause**

Onyx's ``ApplicationFreezeHelper`` is a power-management service that
disables backgrounded apps. It can trigger on first install or after the app
is suspended.

**Fix (development)**

.. code-block:: bash

   adb shell pm enable com.your.app

**Fix (production)**

There is no official whitelist API for third-party apps. Users can manually
add the app to the Boox "keep-alive" list in the Boox settings. For
development, re-enable via adb after each install if affected.

TouchPoint import changes across SDK versions
----------------------------------------------

**Symptom**

Build error:

.. code-block:: text

   error: unresolved reference: TouchPoint
   import com.onyx.android.sdk.pen.data.TouchPoint   // SDK ≤ 1.2.x only

**Cause**

The ``TouchPoint`` class moved packages in SDK 1.4.x:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - SDK version
     - Import
   * - ≤ 1.2.x
     - ``com.onyx.android.sdk.pen.data.TouchPoint``
   * - 1.4.x (current)
     - ``com.onyx.android.sdk.data.note.TouchPoint``
   * - 1.5+ / notecore
     - ``com.onyx.android.sdk.geometry.data.TouchPoint``

**Fix**

Update the import to match your SDK version:

.. code-block:: kotlin

   import com.onyx.android.sdk.data.note.TouchPoint      // SDK 1.4.12
   import com.onyx.android.sdk.pen.data.TouchPointList   // unchanged

FreeReflection / hiddenapibypass bootstrap failure log
-------------------------------------------------------

**Symptom**

Even after adding the bypass library you see:

.. code-block:: text

   W BootstrapClass: reflect bootstrap failed:
   W BootstrapClass: java.lang.NoSuchMethodException: VMRuntime.setHiddenApiExemptions

**Explanation**

This is expected and non-fatal when using ``FreeReflection`` on Boox Android 13.
``FreeReflection`` tries ``VMRuntime.setHiddenApiExemptions`` first (which
is absent from this ROM), then falls back to loading a small dex file into
the boot classpath. The fallback succeeds. You can confirm it worked by the
absence of ``ReflectUtil: reflect bootstrap failed`` from the Onyx SDK itself,
and by the presence of ``submitJob nativeRawReader`` in logcat.

With ``hiddenapibypass`` (LSPosed), neither log line appears — the library
calls the ART runtime directly via JNI without using ``VMRuntime`` at all.

Duplicate class from Syncthing / file sync
-------------------------------------------

**Symptom**

.. code-block:: text

   > Duplicate class com.example.Foo found in:
       module classes.dex
       module Foo.sync-conflict-2024-01-01_*.class

**Cause**

A file-sync tool (Syncthing, Dropbox, etc.) is syncing the ``build/``
directory. Conflict files are copied into the build intermediates and included
in the dex step.

**Fix**

.. code-block:: bash

   ./gradlew clean

Then add ``build/`` to the sync tool's ignore list:

* Syncthing: ``.stignore`` file with ``build/``
* Dropbox: selective sync → uncheck ``build/``

Logcat diagnostic reference
-----------------------------

Useful logcat filter for inking debugging:

.. code-block:: bash

   adb logcat -s InkView:* OnyxPen:* RawInputReader:* ReflectUtil:* \
       BootstrapClass:* lib_touch_reader:* ApplicationFreezeHelper:*

Expected healthy output after successful init:

.. code-block:: text

   I InkView: Ink backend: Onyx TouchHelper (low-latency e-ink path)
   I RawInputReader$a: submitJob nativeRawReader pool-3-thread-1-65
   I lib_touch_reader: find path /dev/input/event3 result name onyx_emp_Wacom I2C Digitizer
   D OnyxPen: onBeginRawDrawing x=1200.0 y=1600.0
   D OnyxPen: onStrokeList size=143
