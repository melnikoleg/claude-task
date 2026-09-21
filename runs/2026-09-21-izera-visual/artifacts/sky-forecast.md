# Sky Forecast - 2026-09-21-izera-visual

## Forecast by Site and Night
One row per (site, night) pair, hourly values would be averaged over the curfew-bounded window only (dark-window start through 22:30 hard end, per the revised requirements.md - not the full ~10.8h dark window):

| Site | Night of | Mean cloud % | Low/Mid/High cloud % | Precip prob % | Wind m/s | Temp C | Dew point C | Dew risk | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| Izera Dark-Sky Park (proxy: Świeradów-Zdrój, 50.9092, 15.34309) | 2026-11-05, window 18:19-22:30 | N/A - beyond forecast horizon | N/A | N/A | N/A | N/A | N/A | unknown | NOT-FORECASTABLE |
| Izera Dark-Sky Park (proxy: Świeradów-Zdrój, 50.9092, 15.34309) | 2026-11-06, window 18:17-22:30 | N/A - beyond forecast horizon | N/A | N/A | N/A | N/A | N/A | unknown | NOT-FORECASTABLE |
| Izera Dark-Sky Park (proxy: Świeradów-Zdrój, 50.9092, 15.34309) | 2026-11-07, window 18:16-22:30 | N/A - beyond forecast horizon | N/A | N/A | N/A | N/A | N/A | unknown | NOT-FORECASTABLE |

No hourly cloud/wind/temperature/dew-point data could be retrieved for any of the three candidate nights. A live call to `mcp__open-meteo__weather_forecast` for this site and date range, re-run today, returned the API error `"Parameter 'start_date' is out of allowed range from 2026-06-20 to 2026-10-06"`. Today is 2026-09-21; the requested nights (2026-11-05 to 2026-11-07) are roughly 45-47 days out, well beyond the Open-Meteo forecast model's horizon (the API's own allowed range tops out at 2026-10-06, about 15 days ahead). No hourly forecast numbers are available to report, and none have been estimated or extrapolated from climatology, model memory, or any other source, per the workflow's no-guessing rule. This also means low-vs-high cloud (which matters most: low cloud blocks visual observing outright, high thin cloud degrades it but less severely) cannot yet be distinguished for any night.

The curfew from the revised requirements.md (hard session end 22:30, driven by the last bus back to Szklarska Poręba) does not change which nights need forecasting - all three still need it - but it does shrink the window that matters once data exists: only 18:16/17/19-22:30 (roughly 4h11m-4h14m per night.md) needs to verify clear, not the full overnight dark window. A night could show poor cloud cover after midnight and still be a GO if the pre-22:30 stretch is clear, or vice versa - the family will already be on the bus home when the after-curfew sky happens.

## Ranked Nights
Cloud cover cannot be ranked because no forecast data exists yet for any of the three nights - all three are equally "unknown" on the weather axis. Falling back to the darkness/moon ranking from `night.md` (weather excluded there by design, already restricted to the pre-22:30 curfew stretch), the order by illumination and moon-up fraction within that stretch is:

1. **2026-11-07** - 2.0% moon illumination, moon up 0% of the 18:16-22:30 curfew window - best darkness/moon conditions of the three.
2. **2026-11-06** - 5.7% illumination, moon up 0% of the 18:17-22:30 curfew window - very close second.
3. **2026-11-05** - 11.3% illumination overall; moon does not rise until 03:44, hours after the 22:30 curfew, so the pre-curfew stretch (18:19-22:30) is fully moon-free too - still weakest of the three on the illumination number, though the gap has no practical effect within curfew.

This ranking reflects darkness and moon only, already scoped to the curfew-bounded session. It must not be read as a weather recommendation: without cloud data, none of the three nights can be called "clear" or "usable" yet.

## Primary and Backup
| Slot | Site | Night | Mean cloud % | Why |
|---|---|---|---|---|
| Primary | Izera Dark-Sky Park (Świeradów-Zdrój proxy) | 2026-11-07, session 18:16-22:30 | N/A - no forecast yet | Best darkness/moon ranking from night.md within the curfew-bounded window (2.0% illumination, 0% moon-up before 22:30); cloud cover is unknown and must be checked before committing. |
| Backup | Izera Dark-Sky Park (Świeradów-Zdrój proxy) | 2026-11-06, session 18:17-22:30 | N/A - no forecast yet | Second-best darkness/moon ranking (5.7% illumination, 0% moon-up before 22:30); same caveat - cloud cover unknown. |

**Plan status: NO-GO (provisional, weather unresolved).** None of the three nights can be confirmed usable because no cloud-cover forecast exists this far out. This is not a "least cloudy pick" - no cloudiness numbers exist to pick from. 2026-11-07 is named primary and 2026-11-06 backup purely on darkness/moon grounds within the curfew window (the least-bad candidates on the data available today); both require a full weather recheck before the trip is finalized, and the plan cannot be called GO until that recheck clears the 40% max-cloud-cover threshold from requirements.md for the specific 18:16/17-22:30 stretch that the child's curfew actually allows the party to use - clearing later in the night after curfew does not help this plan.

## Forecast Confidence
Today is 2026-09-21. The candidate nights are 45-47 days out. A fresh live call to Open-Meteo's forecast API today confirmed it only serves forecasts out to roughly 15-16 days ahead (allowed range ended 2026-10-06 at call time) - the target nights fall entirely outside that window, so zero forecast numbers were obtainable, not merely low-confidence ones. This is beyond even the workflow's own "beyond 7 days, treat as indicative" guidance: at 45+ days out there is no forecast to be indicative of. Cloud cover, precipitation probability, wind, temperature and dew point for all three nights, specifically for the curfew-bounded 18:16/17/19-22:30 windows, must be re-pulled from this same MCP once the dates fall inside the forecast horizon - practically, no earlier than mid-to-late October 2026, and the numbers should be re-verified again 24 hours before the trip, per requirements.md's own risk tolerance. Until then, gear and session planning downstream should treat sky conditions as unknown and build in a same-week reschedule option among 2026-11-05/06/07, keeping in mind that whichever night is finally chosen must also still work against the last-bus schedule.

## Sources
- mcp__open-meteo__weather_forecast(latitude=50.9092, longitude=15.34309, hourly=["cloud_cover","cloud_cover_low","cloud_cover_mid","cloud_cover_high","precipitation_probability","wind_speed_10m","temperature_2m","dew_point_2m","relative_humidity_2m"], start_date="2026-11-05", end_date="2026-11-07", timezone="Europe/Warsaw") - re-run today (2026-09-21) against the revised requirements/night artifacts; returned error: "Invalid request parameters: Parameter 'start_date' is out of allowed range from 2026-06-20 to 2026-10-06". Confirms the candidate nights are still beyond the Open-Meteo forecast horizon as of 2026-09-21; no hourly data obtained.
- runs/2026-09-21-izera-visual/artifacts/requirements.md - site coordinates, 40% max-cloud-cover threshold, revised hard 22:30 session-end constraint.
- runs/2026-09-21-izera-visual/artifacts/night.md - dark windows, curfew-bounded (18:16/17/19-22:30) usable windows, and darkness/moon ranking used as the fallback ranking axis.
- https://www.izerskipark.pl/ - Izera Dark-Sky Park site reference (carried from requirements.md/night.md for site context).
