# Sky Forecast - 2026-09-21-warsaw-astrophoto

## Forecast Horizon Check
Today is 2026-09-21. All three candidate nights (2026-10-16, 2026-10-17, 2026-10-18)
are 25-27 days out. A `mcp__open-meteo__weather_forecast` call for Site 1 with
explicit `start_date`/`end_date` for the candidate dates was rejected with:

> `Invalid request parameters: Parameter 'start_date' is out of allowed range from
> 2026-06-20 to 2026-10-06`

This confirms the Open-Meteo forecast API's usable horizon from today tops out at
**2026-10-06**, roughly 10 days before the earliest candidate night. **None of the
three candidate nights can be forecast today.** No hourly cloud, wind, humidity or
dew-point numbers exist yet for 2026-10-16/17/18 at any of the three candidate sites,
and none are fabricated here per the no-extrapolation rule.

A supplementary call for Site 1 with `forecast_days=16` (the maximum allowed) returned
hourly data only through 2026-10-07, confirming the boundary directly rather than
relying on the error message alone.

## Forecast by Site and Night
One row per (site, night) pair, hourly values averaged over the dark window only:

| Site | Night of | Mean cloud % | Low/Mid/High cloud % | Precip prob % | Wind m/s | Temp C | Dew point C | Dew risk | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1. Bolimowski (51.97901, 20.35037) | 2026-10-16 | N/A - beyond horizon | N/A | N/A | N/A | N/A | N/A | N/A | UNKNOWN - recheck |
| 1. Bolimowski (51.97901, 20.35037) | 2026-10-17 | N/A - beyond horizon | N/A | N/A | N/A | N/A | N/A | N/A | UNKNOWN - recheck |
| 1. Bolimowski (51.97901, 20.35037) | 2026-10-18 | N/A - beyond horizon | N/A | N/A | N/A | N/A | N/A | N/A | UNKNOWN - recheck |
| 2. Chrosna (52.0382, 21.45781) | 2026-10-16 | N/A - beyond horizon | N/A | N/A | N/A | N/A | N/A | N/A | UNKNOWN - recheck |
| 2. Chrosna (52.0382, 21.45781) | 2026-10-17 | N/A - beyond horizon | N/A | N/A | N/A | N/A | N/A | N/A | UNKNOWN - recheck |
| 2. Chrosna (52.0382, 21.45781) | 2026-10-18 | N/A - beyond horizon | N/A | N/A | N/A | N/A | N/A | N/A | UNKNOWN - recheck |
| 3. Zegrzyński Reservoir (52.43152, 21.03212) | 2026-10-16 | N/A - beyond horizon | N/A | N/A | N/A | N/A | N/A | N/A | UNKNOWN - recheck |
| 3. Zegrzyński Reservoir (52.43152, 21.03212) | 2026-10-17 | N/A - beyond horizon | N/A | N/A | N/A | N/A | N/A | N/A | UNKNOWN - recheck |
| 3. Zegrzyński Reservoir (52.43152, 21.03212) | 2026-10-18 | N/A - beyond horizon | N/A | N/A | N/A | N/A | N/A | N/A | UNKNOWN - recheck |

Calls for Site 2 (Chrosna) and Site 3 (Zegrzyński Reservoir) were not made for the
candidate dates because the horizon limit established by the Site 1 call and the
`forecast_days=16` confirmation call is a property of the forecast model/today's date,
not of the site coordinates - it applies identically to all three sites. Re-running
per-site calls once the dates fall inside the horizon (from roughly 2026-10-01 onward
for the earliest night, 2026-10-16) will populate this table with real numbers.

Dark windows to apply once data is available (from night.md, ~5 min variance across
sites): 10-16 19:32-05:11, 10-17 19:30-05:12, 10-18 19:28-05:14 (all local, UTC+2).
When re-run, restrict averaging strictly to these windows and split low/mid/high
cloud - low cloud kills both visual and astrophotography, high thin cloud mainly
degrades long-exposure astrophotography while visual observing can partly work
around it.

## Ranked Nights
No cloud-based ranking is possible today. night.md's darkness/moon ranking (weather
excluded) stands as the only ordering currently available:

1. 2026-10-16 - lowest moon contamination (moon up ~7% of window, 33.9% illum)
2. 2026-10-17 - moon up ~20% of window, 43.1% illum
3. 2026-10-18 - moon up ~30% of window, 52.6% illum

This order must be re-checked against real cloud cover once the forecast horizon
reaches these dates; cloud wins ties over darkness, so night 1 above being the
"best" night on darkness/moon alone does not guarantee it is the best night once
weather is known.

## Primary and Backup
| Slot | Site | Night | Mean cloud % | Why |
|---|---|---|---|---|
| Primary (provisional) | 1. Bolimowski Landscape Park farmland edge | 2026-10-16 | N/A - no forecast yet | Darkest of the three sites (site-scout) and best moon/darkness night (night.md); cloud cover has not been checked and could overturn this pick |
| Backup (provisional) | 2. Chrosna farmland | 2026-10-17 | N/A - no forecast yet | Second-best darkness night, shorter 41-min drive; same caveat - no cloud data yet |

**This is not a GO/NO-GO call.** Neither pick can be confirmed GO until real cloud
data exists for these dates. Treat both as placeholders based on darkness/moon and
site quality alone.

## Forecast Confidence
Zero days of forecast data exist yet for any of the three candidate nights - they sit
10-12 days past the current ~16-day forecast horizon. This is not the ordinary
"beyond 7 days, indicative only" case from the workflow's own threshold; it is a
complete absence of forecast data. **Do not trust any weather assumption for this
plan until it is rechecked.** Recommended recheck schedule:
- From ~2026-10-01: first indicative (7-16 day range) numbers become available for
  the earliest night (10-16); treat as low-confidence trend only.
- From ~2026-10-09 (7 days before the earliest night): numbers become moderately
  reliable.
- 24 hours before the chosen night: final go/no-go check, as required regardless of
  horizon.

## Sources
- mcp__open-meteo__weather_forecast(latitude=51.97901, longitude=20.35037, hourly=[cloud_cover, cloud_cover_low, cloud_cover_mid, cloud_cover_high, precipitation_probability, wind_speed_10m, temperature_2m, dew_point_2m, relative_humidity_2m], start_date="2026-10-16", end_date="2026-10-19", timezone="Europe/Warsaw", wind_speed_unit="ms") - rejected: "Invalid request parameters: Parameter 'start_date' is out of allowed range from 2026-06-20 to 2026-10-06"
- mcp__open-meteo__weather_forecast(latitude=51.97901, longitude=20.35037, hourly=[cloud_cover, cloud_cover_low, cloud_cover_mid, cloud_cover_high, precipitation_probability, wind_speed_10m, temperature_2m, dew_point_2m, relative_humidity_2m], forecast_days=16, timezone="Europe/Warsaw", wind_speed_unit="ms") - succeeded, returned hourly data 2026-09-21 through 2026-10-07 only, confirming the horizon boundary
- https://open-meteo.com/en/docs - Open-Meteo forecast API documentation (16-day forecast horizon)
- runs/2026-09-21-warsaw-astrophoto/artifacts/sites.md - candidate site coordinates
- runs/2026-09-21-warsaw-astrophoto/artifacts/night.md - dark windows and darkness/moon ranking
- runs/2026-09-21-warsaw-astrophoto/artifacts/requirements.md - 40% cloud threshold, candidate nights
