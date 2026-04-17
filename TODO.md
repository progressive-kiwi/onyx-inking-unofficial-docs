# TODO

## Unclear / missing documentation

- **TouchRender**: mentioned in `epd-rendering.rst` and `architecture.rst` but never defined. Unclear whether it is a public class, internal SDK component, or an alias for something else. Needs research and a proper description (what it is, its relation to `TouchHelper`, and any relevant API surface).

## Terms needing clarification or links

### Hardware / display

- **Wacom I2C digitizer** (`index.rst`, `architecture.rst`, `reference.rst`): "Wacom" is used as if self-evident. Needs a brief note — Wacom supplies the pen digitizer hardware inside BOOX devices; I2C is the bus protocol it uses.
- **evdev** (`architecture.rst`): Linux input subsystem interface. Not defined; readers unfamiliar with Linux kernel input may not understand how the SDK hooks into it.
- **A2 / GC / DU / REGAL waveforms** (`epd-rendering.rst`, `reference.rst`): abbreviations used across multiple files. GC and DU are expanded in the table, but REGAL is never expanded (Reactive Grayscale ALgorithm or similar — needs verification).
- **HAND_WRITING_REPAINT_MODE** (`epd-rendering.rst`, `reference.rst`): constant name but no explanation of when to use it vs A2, or what "repaint mode" means at the hardware level.
- **framebuffer / A2 buffer** (`epd-rendering.rst`, `architecture.rst`): hardware rendering buffer concept; not explained for developers without embedded/display background.
- **libtouch_reader.so** (`architecture.rst`): native library name mentioned in the architecture diagram but never explained — what it does and who owns it (Onyx SDK or OS).

### SDK classes / utilities (unlinked)

- **ReflectUtil** (`getting-started.rst`, `troubleshooting.rst`): appears multiple times as if it is a known SDK class, but has no reference page and is never explained.
- **DeviceFeatureUtil** (`sdk-setup.rst`): mentioned without definition or link.
- **EinkRefresh** (`epd-rendering.rst`): unclear whether this is an SDK class, a custom wrapper, or pseudocode.
- **ApplicationFreezeHelper** (`troubleshooting.rst`): Onyx system service referenced in troubleshooting; no explanation of what it does or how to interact with it.
- **VMRuntime / VMRuntime.setHiddenApiExemptions** (`getting-started.rst`, `troubleshooting.rst`): the hidden-API bypass mechanism is described at a high level, but VMRuntime itself is not explained (it is an internal Android class, not in the public SDK).

### Android / system concepts (non-obvious in this context)

- **Hidden API enforcement** (`sdk-setup.rst`, `troubleshooting.rst`): the concept of `@hide` APIs and greylist/blocklist is referenced but not explained for developers who have not encountered it before.
- **JNI libraries / libc++_shared.so** (`sdk-setup.rst`): JNI is mentioned but it is not explained why the SDK ships native `.so` files or what the developer needs to do (or not do) with them.
- **dex / dex archive** (`troubleshooting.rst`): used in the context of `ClassNotFoundException` troubleshooting; "dex archive" is jargon that may confuse developers not familiar with Android build internals.
- **Binder permissions / SYSTEM package flag** (`architecture.rst`): referenced in the context of why certain APIs require system-level access; not explained.
- **TOOL_TYPE_STYLUS / TOOL_TYPE_FINGER** (`troubleshooting.rst`): `MotionEvent` constants used without explaining why distinguishing them matters for the SDK.

### Third-party libraries (unlinked, unexplained)

- **mmkv** (`sdk-setup.rst`): Tencent key-value store bundled in the SDK; no explanation of why it is there or whether the developer needs to initialise it.
- **RxJava 2** (`sdk-setup.rst`): listed as a transitive dependency; no context for why the SDK depends on a reactive-streams library.
- **commonsIO** (`sdk-setup.rst`): Apache Commons IO; mentioned without context.

### Pen styles (reference.rst / samples.rst)

- **NeoCharcoalPenV2, NeoMarkerPen, NeoBrushPen** (`samples.rst`): pen style class names referenced in sample descriptions but never defined or linked to a reference page.
- **NeoTools** (`samples.rst`): mentioned as an SDK feature set without definition.
