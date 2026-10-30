# Device release checks

Record actual device, app version, Android version, media codec, library size,
duration, observations, and measured memory values privately. Use synthetic media.
Do not convert this plan into a claim that tests have already passed.

| Scenario | Expected result |
| --- | --- |
| First launch in airplane mode | Local introduction, no download requirement |
| Permission denied | Explanation and local document selection remain available |
| Android 14+ selected access | Only permitted videos appear; reselection works |
| Permission revoked in settings | Foreground refresh drops inaccessible media |
| Empty / one video | Useful empty state / stable looping video |
| 10,000+ local videos | Cancelable indexing; responsive scrolling and bounded thumbnails |
| Rapid swipes for 30 minutes | One active player; settled video only; no overlapping audio |
| Backwards and cycle boundaries | Same prior order, complete permutations, no boundary repeat |
| Delete file / remove SD card | Clear error or disappearance after refresh; no retry loop |
| Corrupt or unsupported video | Error with explicit skip; no automatic transcoding |
| Background / lock / phone call | No background audio; player releases on pause/stop |
| Headphone removal / audio focus loss | Audio stops or pauses according to system focus |
| Process kill and restart | Explicit resume restores saved order/position, subject to checkpoint delay |
| Large text and TalkBack | No clipped actions; labeled controls; accessible next/previous |
| Bright/dark and rotated media | Readable controls; original colors; correct aspect and orientation |
| Clear local app data | Flags/session/sources gone; original media hashes unchanged |
| Low RAM and thermal pressure | Optional thumbnail work disabled; no unbounded background work |
| GitHub with and without URL handler | Exact external URL, copy fallback; core app works offline |

Measure PSS and codec instances at a steady set of checkpoints, not just once at
startup. Garbage collection and decoder pools can cause temporary variation.
Investigate persistent growth across repeated comparable cycles. No real phone
was attached to the development environment; emulation cannot establish physical
codec, SD-card, call, thermal, battery, or low-RAM behavior.

Version 0.2.0 regression checks: repeat rapid swipes and reshuffles while checking
that each new video has a visible first frame before any audio; test viewport
resize, lock/unlock, and background return. Confirm horizontal 16:9 clips fit fully
in the 9:16 stage, separate Like/Save behavior, transparent overlay controls, no
bottom transport panel, and no repeated loading text. Check actual display refresh
rate and frame timing on 60/90/120/144 Hz devices; a 144 Hz request is not an FPS
measurement or a promise. Verify old 0.1.0 favorites, sources and settings remain.
