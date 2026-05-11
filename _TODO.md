# TODO list
* [x] : fix : the remaining time is not adjusted on pause
* [x] : fix UI misplacing
* [x] : fix progress bar text
* [x] : calibrate page : drawing adding A4 A3 and A2 and adjusting with a precision slider
* [x] : auto pause (for recharging pen)
* [x] : resuming with options changes - pen height ok

## Known limitations
* [ ] : pause/resume does not work for points-only plots (stippling, dots) — `axidrawinternal` tracks resume position via `down_travel_inch` which stays at 0 for vertical pen-down moves with no horizontal displacement. `crop(0)` is a no-op so the plotter always restarts from the beginning.

## TODO
* [ ] : manual move ??
* [ ] : keyboard actions inputs : use the bind key : https://tkinterexamples.com/events/keyboard/
