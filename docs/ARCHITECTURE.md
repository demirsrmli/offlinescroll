# Architecture

`LocalMedia` is the read-only storage boundary. It accepts narrow content URI
shapes from recognized system providers and checks regular-file descriptors.
Its MediaStore cursor reads basic projected columns in batches of 256 on IO;
there is no native metadata decoder per library item. Explicit documents need
individual validation and duration lookup, serially on IO. Cancellation checks
occur between rows/documents. An active scan is replaced on controlled refresh.
There is no background observer, worker, service, periodic scan, or media copy.

`AppViewModel` owns source consent, flags, filters, and the queue. Private local
records use SharedPreferences and an atomic session file in no-backup storage.
An IO mutex serializes writes. Session checkpoints are made every five seconds
and on player release; abrupt termination may lose the most recent five seconds.
Users choose whether to remember and explicitly resume a previous session.

`ShuffleQueue` is a tested pure Kotlin state machine. Randomness is consumed only
for explicit reset or the next cycle. Each cycle is a permutation. New cycles
avoid repeating the previous last video when at least two videos exist. At most
three cycles are held; paging further drops the oldest cycle. Earlier dropped
history is intentionally unavailable. Explicit library/filter changes begin a
new cycle and preserve the focused item when it remains permitted.

`PlayerController` is the only ExoPlayer construction site. Feed owns exactly one
persistent PlayerView with a TextureView, outside every pager page and outside
queue-anchor keys. Reshuffling, history trimming and paging therefore cannot
release an old page surface and detach the current video output. TextureView
supports the stage's translation and clipping within Compose. This reliability
choice adds GPU composition compared with a direct SurfaceView; it remains one
surface and one hardware video decoder, with no preloading or secondary renderer.

Each source gets an opaque generation ID. Preparing remains paused until the
AnalyticsListener reports the first rendered frame for that exact ID. Old frame
callbacks cannot authorize new audio. Detach, background and lock invalidate
readiness; reattachment prepares the current position again. User pause, paging,
headphone removal and audio-focus loss are respected separately. A 12-second
first-frame/buffering timeout exposes an actionable local-file error. No automatic
error-skipping loop, transcoding, network source, or platform MediaMetrics exists.

The stage is 9:16; Media3 FIT preserves a horizontal clip's full aspect ratio,
adding black space rather than cropping or stretching. Fill remains an explicit
optional preference; the upgrade resets the old Fill default to Fit once. Paging
uses Compose's display-synchronized animation clock and a 240 ms snap/transition.
The window requests 144 Hz once on entering normal Feed and clears the preference
on leaving/low-resource mode. Media3's per-clip frame-rate switching is disabled.
The display, OS, battery saver and thermal policy choose the actual refresh rate.
Video is decoded at its original frame rate, without artificial interpolation.

The video-size guard uses an orientation-neutral long edge and pixel budget:
1920 / 2,073,600 pixels in low-resource mode, 3840 / 8,294,400 pixels otherwise.
Portrait 1080×1920 is therefore treated the same as landscape 1920×1080. Selected
track and reported decoder dimensions are checked before audio is allowed;
audio-only track selection stops with an unsupported-format message. Normal
TRIM_MEMORY_UI_HIDDEN clears thumbnails without permanently enabling low-resource
mode. Actual running-low/critical or background memory pressure still does so.

Thumbnails run only in Library/Hidden screens, where Feed is disposed. One
request at a time is allowed, sized at 240×144 and cached in a 4 MiB memory LRU.
No permanent frames are written. Android 8–9 uses placeholders. Low-resource
mode or memory/thermal pressure disables optional thumbnail work. Pressure is
conservatively retained until process restart. The video buffer is capped at
12 MiB, or 4 MiB when the player is created in low-resource mode.

Backup is disabled and both old and Android 12+ extraction rules exclude all app
records. Clear-data releases persisted URI grants, clears metadata/cache, and
disables library consent; it never writes the originals. Android 13+ supports
self-revocation of runtime media grants on a later process termination. On older
Android versions the user revokes the OS runtime permission in system settings;
the app still discards its internal consent immediately.

Known tradeoffs: only basic MediaStore metadata is indexed, no prefetch is used,
history is bounded, OEM providers can be rejected, initial explicit-document
indexing is serial, and system decoder behavior still requires real-device tests.

An unavailable or incomplete thermal service cannot block startup: optional thermal listener registration/removal is guarded. Playback checkpoints also update the in-memory restore position for recreation or navigation back to Feed.

The metadata index stores no frames or video bytes and is bounded to 16 MiB in
no-backup private storage. Its gallery/source-consent header must match. Cached
gallery records are exposed only while current full access exists; partial access
must be queried anew. A reduced permission clears the old broader list immediately.
Selected-document metadata can be reused only after a fresh local descriptor,
MIME, name and size check. The initial welcome, likes and saved favorites are
separate persistent fields; old favorites/hidden records and source grants remain.
