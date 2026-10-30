# Native UI renders — 0.2.0

The separate OfflineScroll_Native_UI_Renders.zip contains actual MainActivity /
Compose Canvas renders under Robolectric API 35: Welcome, Source selection,
Settings, empty Library, Welcome and Source selection at 150% system text, and
Feed controls with an unavailable synthetic test source.

These are native UI test renders, not HTML mockups, generated artwork or
physical-phone screenshots. Robolectric has no GPU TextureLayer: the inactive
video surface is omitted while drawing the Feed test image. The actual
TextureView object, its identity across paging/reshuffle and FIT mode are tested
separately. No screenshot is presented as proof of successful hardware decoding
or 144 fps performance. No Instagram screenshot is distributed.

Run :app:testDebugUnitTest to reproduce the images. Testing dependencies are
build/test only; the installed app has no networking requirement. See
VERIFICATION.md for actual results and remaining device checks.
