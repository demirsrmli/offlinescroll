# UI and playback references

Checked October 29, 2026. The implementation uses original OfflineScroll branding
and project-authored icons. No Instagram image, screenshot, font or proprietary
asset is packaged into the app or source delivery.

- Meta, Instagram repost introduction (August 6, 2025):
  https://about.fb.com/news/2025/08/new-instagram-features-help-you-connect/
- Visual reference showing the Reels reaction rail and transparent overlays:
  https://socialbiz.nhndata.com/post/blog_250811
- Meta, simplified Reels-first navigation (September 28, 2025):
  https://about.fb.com/news/2025/09/in-india-instagram-debuts-a-reels-first-experience-for-its-mobile-app/
- Android, Media3 surface lifecycle and Compose interop considerations:
  https://developer.android.com/media/media3/ui/surface
- Android, preferred refresh rate and platform constraints:
  https://developer.android.com/media/optimize/performance/frame-rate

The resulting design uses a dominant portrait video stage, a compact right-side
Like/Save rail, transparent header icons, tap playback, and secondary controls in
a sheet. OfflineScroll's repost-style button means **save to local Favorites**;
it never posts publicly, contacts followers, sends messages, or uploads content.
There are no invented social counts. This is an original offline app inspired by
common short-video interaction patterns, not an Instagram client or affiliation.
