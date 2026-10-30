# Release and signing — 0.2.0 (code 2)

1. Recover the existing source/Play identity and key history if this replaces an
   earlier app. None was supplied here. The ID is provisional, not a claim about
   an existing installation. Never change a published application ID or overwrite
   an existing key. Increase `offlineScroll.versionCode` for every Play upload.
2. Confirm `compileSdk` and `targetSdk` are at least 36. This source uses both 36.
3. Install JDK 17, Platform 36, Build Tools 35.0.0. Android Studio can create the
   ignored `local.properties`; never commit your machine's SDK path.
4. Copy `keystore.properties.example` to the ignored `keystore.properties` and
   enter the existing private upload-key path and credentials locally. Do not
   place the key inside this project. Use forward slashes for Windows paths.
5. Alternatively use private environment variables `OFFLINESCROLL_STOREFILE`,
   `OFFLINESCROLL_STOREPASSWORD`, `OFFLINESCROLL_KEYALIAS`, and
   `OFFLINESCROLL_KEYPASSWORD`. Do not paste real values into shared scripts,
   issue comments, terminal transcripts, or source files.
6. Build with `./gradlew :app:bundleRelease :app:assembleRelease :app:lintRelease`
   (Windows: `.\gradlew.bat` with the same tasks). Missing signing information
   fails explicitly. The build never creates a production key or falls back to
   the debug certificate.
7. Validate the AAB with the official bundletool `validate --bundle=...` command.
   Check its signature with JDK `jarsigner -verify`. Verify the APK with SDK
   `apksigner verify --verbose`. Keep fingerprints private if they identify an
   unrelated application; only publish the intended app's public certificate.
8. Enroll the new app in Play App Signing and upload the **signed AAB**. Your upload
   key authenticates the bundle; Play's app-signing key signs delivered APKs.
   An upload-key APK may not install over a Play-installed app if their
   certificates differ. A debug APK is a separate `.test` application here.
9. Complete device tests, store metadata, Data safety, content rating, target
   audience, accessibility checks, and any testing requirements shown in your
   actual Play Console account. Do not claim this app is already published.
10. Host the packaged privacy policy publicly for the store listing. Hosting that
    page does not give OfflineScroll a networking requirement or permission.

For review without a key, the explicit command
`./gradlew :app:bundleRelease :app:assembleRelease -PallowUnsignedRelease=true`
produces **unsigned** artifacts. They are not signed Play uploads. No upload key
was provided during this implementation; any delivered AAB is labeled UNSIGNED.

The store's current policies should be rechecked immediately before publication.
Primary references: https://developer.android.com/studio/publish/app-signing,
https://developer.android.com/google/play/requirements/target-sdk,
https://developer.android.com/build/releases/agp-8-13-0-release-notes.

Version 0.2.0 retains the 0.1.0 application IDs and signing setup. The previous test APK can be updated with the new test APK when their development certificates match. Existing favorites and sources are migrated; no original media is changed. The new welcome appears once, and default video display resets to Fit.
