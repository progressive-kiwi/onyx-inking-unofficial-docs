Getting Started
===============

This guide walks through the minimum steps to get hardware-accelerated stylus
input working in a third-party app on an Onyx BOOX device.

Prerequisites
-------------

* Android Studio (any recent version)
* A physical Onyx BOOX device with USB debugging enabled
* ``compileSdk 33`` or higher

Step 1 — Add the Boox Maven repository
---------------------------------------

The Onyx SDK is hosted on Boox's own Maven server. Add it to your project's
``settings.gradle`` (or top-level ``build.gradle`` for older setups):

.. code-block:: groovy

   // settings.gradle
   dependencyResolutionManagement {
       repositories {
           google()
           mavenCentral()
           maven { url 'https://repo.boox.com/repository/maven-public/' }
           maven { url 'https://jitpack.io' }
       }
   }

Step 2 — Add SDK dependencies
-------------------------------

Add the following to ``app/build.gradle``. All three modules are required.
Use ``transitive = false`` on each — the default transitive graph pulls in
broken dependencies that are not resolvable from any public repository.

.. code-block:: groovy

   dependencies {
       // Hidden-API bypass — must be initialised before any Onyx SDK class loads
       implementation 'org.lsposed.hiddenapibypass:hiddenapibypass:4.3'

       // Onyx pen SDK — transitive = false avoids unresolvable deps in onyxsdk-base
       implementation('com.onyx.android.sdk:onyxsdk-pen:1.4.12')    { transitive = false }
       implementation('com.onyx.android.sdk:onyxsdk-base:1.7.7')    { transitive = false }
       implementation('com.onyx.android.sdk:onyxsdk-device:1.2.31') { transitive = false }

       // RxJava 2 — used internally by onyxsdk; must be explicit when transitive = false
       implementation 'io.reactivex.rxjava2:rxjava:2.2.21'
       implementation 'io.reactivex.rxjava2:rxandroid:2.1.1'
   }

See :doc:`sdk-setup` for a full explanation of why each module is needed.

Step 3 — Initialise the hidden-API bypass
------------------------------------------

Android's hidden API list is a set of internal framework methods and fields
that Google and device OEMs reserve for platform and system apps. Apps
targeting Android 10+ are blocked from calling them by default — they either
get ``null`` from reflection, or throw ``NoSuchMethodException``.

The Onyx SDK uses two categories of hidden API at startup:

* **``VMRuntime.setHiddenApiExemptions``** — ``ReflectUtil`` (inside
  ``onyxsdk-base``) calls this in its static initialiser to whitelist further
  hidden methods it needs. This method is itself on the hidden list, creating
  a bootstrapping problem: the SDK tries to use a hidden API in order to
  access other hidden APIs.
* **EPD controller fields** — ``EpdController`` (inside ``onyxsdk-device``)
  reads device-specific fields on the ``Device`` class via reflection to map
  pen digitizer coordinates to screen space. These fields are hidden.

On Onyx's own system apps (e.g. the built-in note app) this is not a problem
— the ``SYSTEM`` package flag disables all hidden API enforcement for the
process. Third-party apps carry no such flag, so the restriction applies.

If the bypass is not in place when the first SDK class loads, ``ReflectUtil``
fails to initialise, which poisons ``EpdController``, which returns an empty
coordinate rect, which causes the hardware event filter to cover zero area —
no pen events are ever delivered. See :ref:`hidden-api-bypass` for the full
failure chain and library options.

Create an ``Application`` subclass and call ``HiddenApiBypass.addHiddenApiExemptions``
in ``attachBaseContext``:

.. code-block:: kotlin

   class App : Application() {
       override fun attachBaseContext(base: Context) {
           super.attachBaseContext(base)
           // Must run before any Onyx SDK class is touched.
           HiddenApiBypass.addHiddenApiExemptions("")
       }
   }

Register it in ``AndroidManifest.xml``:

.. code-block:: xml

   <application
       android:name=".App"
       ... >

.. important::

   ``attachBaseContext`` fires before ``Application.onCreate`` and before
   any Activity or Service is created. This is the only safe place to call
   the bypass. If any Onyx SDK class is loaded first (e.g. by a diagnostic
   ``Class.forName`` call) the static initialiser may fail permanently and
   subsequent SDK usage will silently produce empty regions or no callbacks.
   See :ref:`class-poisoning`.

Step 4 — Create an ink overlay view
-------------------------------------

Subclass ``View`` and set up ``TouchHelper`` after the view has been laid out.
The SDK requires screen-absolute coordinates, so creation must be deferred
until after the first layout pass:

.. code-block:: kotlin

   class InkView @JvmOverloads constructor(
       context: Context, attrs: AttributeSet? = null
   ) : View(context, attrs) {

       private var touchHelper: TouchHelper? = null

       override fun onAttachedToWindow() {
           super.onAttachedToWindow()
           viewTreeObserver.addOnGlobalLayoutListener(object :
               ViewTreeObserver.OnGlobalLayoutListener {
               override fun onGlobalLayout() {
                   viewTreeObserver.removeOnGlobalLayoutListener(this)
                   initTouchHelper()
               }
           })
       }

       private fun initTouchHelper() {
           val screenRect = Rect()
           if (!getGlobalVisibleRect(screenRect) || screenRect.isEmpty) return

           touchHelper = TouchHelper.create(this, object : RawInputCallback() {
               override fun onBeginRawDrawing(b: Boolean, p: TouchPoint) {}
               override fun onEndRawDrawing(b: Boolean, p: TouchPoint) {}
               override fun onRawDrawingTouchPointMoveReceived(p: TouchPoint) {
                   // live point during stroke — SDK renders A2 simultaneously
               }
               override fun onRawDrawingTouchPointListReceived(list: TouchPointList) {
                   // complete stroke on pen-up
               }
               override fun onBeginRawErasing(b: Boolean, p: TouchPoint) {}
               override fun onEndRawErasing(b: Boolean, p: TouchPoint) {}
               override fun onRawErasingTouchPointMoveReceived(p: TouchPoint) {}
               override fun onRawErasingTouchPointListReceived(list: TouchPointList) {}
           }).apply {
               setLimitRect(mutableListOf(screenRect), mutableListOf())
               openRawDrawing()
               setRawDrawingRenderEnabled(true)
               setPenUpRefreshEnabled(false)
               setRawDrawingEnabled(true)
           }
       }

       override fun onDetachedFromWindow() {
           touchHelper?.closeRawDrawing()
           touchHelper = null
           super.onDetachedFromWindow()
       }
   }

Step 5 — Connect activity lifecycle
-------------------------------------

Pause and resume raw drawing when the activity moves in and out of the
foreground:

.. code-block:: kotlin

   // In your Activity or Fragment:
   override fun onResume()  { inkView.onResume() }
   override fun onPause()   { inkView.onPause()  }

   // In InkView:
   fun onResume() = touchHelper?.setRawDrawingEnabled(true)
   fun onPause()  = touchHelper?.setRawDrawingEnabled(false)

Step 6 — Verify with logcat
-----------------------------

After installing on device, filter logcat:

.. code-block:: text

   adb logcat -s InkView RawInputReader ReflectUtil

A successful init produces lines like:

.. code-block:: text

   I InkView: Ink backend: Onyx TouchHelper (low-latency e-ink path)
   I RawInputReader$a: submitJob nativeRawReader pool-3-thread-1-65
   I lib_touch_reader: find path /dev/input/event3 result name onyx_emp_Wacom I2C Digitizer

If you see ``MotionEvent fallback`` instead, consult :doc:`troubleshooting`.
