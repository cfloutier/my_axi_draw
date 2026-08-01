# TODO list

* [x] : fix : the remaining time is not adjusted on pause
* [x] : fix UI misplacing
* [x] : fix progress bar text
* [x] : calibrate page : drawing adding A4 A3 and A2 and adjusting with a precision slider
* [x] : auto pause (for recharging pen)
* [x] : resuming with options changes - pen height ok

## Known limitations

* [x] : pause/resume does not work for points-only plots (stippling, dots) — fixed in fork
  `cfloutier/axidrawinternal` branch `fix/pause-resume-dots-path-count` via `pause_count`
  (path ordinal index as fallback resume metric when `down_travel_inch == 0`).
  **To test on real hardware before merging to main.**

## TODO

* [ ] : manual move ??
* [ ] : keyboard actions inputs : use the bind key : https://tkinterexamples.com/events/keyboard/
