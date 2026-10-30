# OfflineScroll 0.2.0 verification report

Date: October 29, 2026. Version: 0.2.0; versionCode: 2 (previously 1).
minSdk: 26; compileSdk/targetSdk: 36. Release ID: `dev.offlinescroll.app`.
Test ID: `dev.offlinescroll.app.test`. Both IDs and the signing setup are unchanged.

## Implemented result

The Feed now uses one persistent PlayerView/TextureView outside pager pages and
queue-anchor replacement. Preparing a new clip stays paused until its own first
rendered frame is reported; stale frame callbacks cannot start the next clip's
audio. Surface detach, background and screen-off invalidate readiness. Selected
tracks and decoded dimensions are checked; audio-only or over-budget selections
stop with a useful error. The orientation-neutral budget accepts portrait
1080×1920 as well as landscape 1920×1080. Normal UI_HIDDEN is no longer mistaken
for low-memory pressure. These fix concrete source paths that could cause missing
video or audio-only selection; hardware reproduction remains untested below.

The large bottom transport panel is removed. Tap video to pause/resume; double
tap to like. Transparent top actions and a compact right rail provide Like,
repost-style Save, and mute. Likes and saved favorites are independent private
records; Save does not publish or send anything. Seeking, speed, Fit/Fill and
accessible previous/next actions remain in Video options. The stage is 9:16 with
FIT by default, preserving the complete horizontal frame with black space.

A first-run Let's start screen explains the local-only privacy boundary. Existing
favorites, hidden flags and sources are retained. A consent-scoped private metadata
index avoids repeated blocking Feed-loading text. It stores no media bytes or
frames, is capped at 16 MiB, and is disabled in low-resource mode. Reduced gallery
permission discards the old broader list immediately. Core app text remains English.

Paging uses a 240 ms display-synchronized transition. Normal Feed requests 144 Hz
and restores that preference after foregrounding; low-resource mode clears it.
Actual refresh rate is selected by Android/display/power policy. Video keeps its
original frame rate and color; no grayscale filter or frame interpolation exists.
No 144 fps measurement or guarantee is claimed.

## Executed checks

| Check | Result | Evidence and practical limit |
| --- | --- | --- |
| Debug APK | PASS | `:app:assembleDebug`; a real development-signed APK, separate `.test` ID |
| Release compilation | PASS | `:app:bundleRelease :app:assembleRelease`, explicit unsigned opt-in |
| Logic tests | PASS | 22 tests: nine shuffle, five URI/filter, eight first-frame/video-budget tests |
| Private records/provider tests | PASS | Nine Robolectric tests: six migration/cache/clear/memory cases, three cached-source consent cases |
| Native UI regression tests | PASS | Five Robolectric API 35 tests: welcome, Settings, empty Library, 150% text, stable Feed surface/actions/lifecycle preference |
| All tests together | PASS | 36 tests; zero failures, errors, or skipped tests |
| Debug/release lint | PASS with warnings | Zero errors, 43 warnings in each variant; no lint baseline suppresses errors |
| Missing-key release guard | PASS | Normal `bundleRelease` fails explicitly; no automatic debug signing of release |
| Debug signature/update continuity | PASS | SDK apksigner accepts the APK; certificate matches the delivered 0.1.0 test APK |
| Compiled AAB | PASS, UNSIGNED | Official bundletool validation exits 0; jarsigner reports `jar is unsigned` |
| API/version/manifest | PASS | Compiled release manifest: target 36, code 2, no INTERNET/ACCESS_NETWORK_STATE/WAKE_LOCK/write/service permission; no services; backup false |
| Native alignment | PASS | arm64-v8a and x86_64 ELF LOAD segments aligned to 16 KiB; release APK zipalign check and AAB 16 KiB config pass |
| Dependency audit | PASS within scope | Same 71 resolved runtime coordinates; no added network/cloud/analytics/ads library; strict content-only playback factory |
| Runtime diagnostics/assets | PASS, source/manifest audit | Platform MediaMetrics disabled; downloadable-emoji initializer absent; system fonts and bundled vectors/logos/text |
| Clean sharing-copy build | PASS | Separate source tree without build outputs: all 58 tasks executed, debug APK, all 36 tests and debug lint; cached dependencies with Gradle --offline |
| Source privacy audit | PASS within scope | 100 source files; zero pattern findings; clean image metadata; unchanged signing setup and logo bytes |

Frame-readiness tests reject 100 obsolete generation callbacks, preserve user
pause and scroll intent, and prevent detached audio. Pixel-budget tests cover
portrait/landscape symmetry, excessive square frames and integer-overflow inputs.
The Feed UI test verifies the same actual TextureView identity across eight
swipes and reshuffle, 9:16 geometry, FIT, separate Like/Save states, no permanent
bottom transport, and 144→0→144 window preference across pause/resume. It uses
synthetic unavailable media, not a hardware decoder. Queue tests also cover
empty/single lists, repeated cycles, saved sessions, source changes and bounded
history with 20,000 synthetic IDs; this is not a real 20,000-file indexing benchmark.

The seven provided PNGs are actual native MainActivity/Compose Canvas test
renders, not design mockups or physical-device screenshots. Robolectric cannot
draw a GPU TextureLayer; the inactive synthetic Feed video surface is omitted
only during screenshot capture. The image is explicitly labeled unavailable.
These renders do not demonstrate successful video decoding. No personal media or
external Instagram image is included.

Lint warnings concern KTX conveniences, serialized IO SharedPreferences commits,
unused legacy resources, text plurals, a permission compatibility branch, a
redundant SDK condition, parentless Compose host inflation, overdraw and launcher
shape. Android deprecated-memory callback constants are retained for older phones.
No broad lint suppression was added.

## Device limitations — UNTESTED

No physical Android phone is attached. Earlier attempts with API 35 software
emulation installed the APK but encountered System UI ANR; API 28 did not finish
booting in the attempt. Those attempts are not app-functionality passes. They
were not repeated as evidence for 0.2.0. The following still require a reliable
phone/emulator:

- Actual video decoding and the reported swipe bug with real files, rotations,
  bright/dark content, seeking, speed, Fit/Fill and full original-color playback.
- Real 144 Hz frame timing, dropped-frame counts, low-RAM long sessions,
  decoder/PSS/heap growth, battery use, and thermal behavior.
- Airplane-mode interaction with real sources; permission dialogs/denial/partial
  access/revocation; real document grants; cloud-provider and removable-SD cases.
- Deleted/corrupt video, screen lock, phone calls, audio-focus loss, headphone
  removal and measured background silence.
- Process death with real media, original-file hash checks after data clearing,
  huge-archive indexing, storage failures, TalkBack traversal and external GitHub
  handoff/copy fallback on a phone.

The source has one player construction site, one persistent video host, no
secondary renderer prewarming, software-video fallback, preloading, background
service, media copies or network fallback. Buffers/thumbnails/index are bounded.
These are safeguards and automated assertions, not measured device guarantees.
TextureView supports reliable Compose translation/clipping but requires GPU
composition, which can cost more than direct SurfaceView output.

## Provenance and release work

This is an update to the actual 0.1.0 project delivered in this session. Its earlier
source snapshot and supplied attachments were preserved. The initial project was
implemented from requirements/logos because no older Android source or signing
history was supplied; it was not decompiled from an APK. Compatibility with an
unknown external Play release cannot be asserted.

No production/upload key was supplied or generated. Configure the owner's private
upload key, sign the AAB, use Play App Signing, confirm final ID/history and raise
versionCode for every upload. Complete the device checks above, logo-rights
confirmation, public store privacy page, store metadata and account-specific Play
requirements. No GitHub push or store publication was performed.

## Source packaging

The complete source comprises 100 files, split into two ZIPs of 50 files each.
Directory entries are not counted. Hidden files are included; paths retain the
project root layout with no extra enclosing folder, duplicates, traversal or
nested ZIP. The final delivery SHA-256 list records every archive count/hash
and the fresh combined-extraction comparison. UI renders are a separate ZIP
of seven PNGs plus one explanation file. Source archives contain no APK/AAB,
keys, logs, private configuration, caches or Git history.
