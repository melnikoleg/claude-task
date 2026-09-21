# Sky Forecast - 2026-12-13-berlin-geminids

## Forecast by Site and Night
One row per (site, night) pair, hourly values averaged over the dark window only:

Both candidate nights (2026-12-13 and 2026-12-14) fall far outside the Open-Meteo
forecast horizon as of today, 2026-09-21. A live query for the dark-window hours was
attempted and the API rejected it outright:

`mcp__open-meteo__weather_forecast(latitude=52.786901, longitude=12.60948, hourly=[cloud_cover, cloud_cover_low, cloud_cover_mid, cloud_cover_high, precipitation_probability, wind_speed_10m, temperature_2m, dew_point_2m, relative_humidity_2m], start_date="2026-12-13", end_date="2026-12-14", timezone="Europe/Berlin")` returned:
`Invalid request parameters: Parameter 'start_date' is out of allowed range from 2026-06-20 to 2026-10-06`.

That is an 83-day-out request against an API whose allowed window currently reaches
only 15 days ahead (2026-10-06). No hourly cloud, wind, temperature, dew point or
humidity numbers exist yet for either candidate site or night. The table below
records that explicitly rather than leaving it blank or inventing numbers:

| Site | Night of | Mean cloud % | Low/Mid/High cloud % | Precip prob % | Wind m/s | Temp C | Dew point C | Dew risk | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| Zootzen observation site | 2026-12-13 | not available (beyond forecast horizon) | not available | not available | not available | not available | not available | unknown | recheck required |
| Zootzen observation site | 2026-12-14 | not available (beyond forecast horizon) | not available | not available | not available | not available | not available | unknown | recheck required |
| Klessener See observation site | 2026-12-13 | not available (beyond forecast horizon) | not available | not available | not available | not available | not available | unknown | recheck required |
| Klessener See observation site | 2026-12-14 | not available (beyond forecast horizon) | not available | not available | not available | not available | not available | unknown | recheck required |

No dew-risk or cold-warning flags can be computed without temperature and dew-point
data. Given mid-December in Brandenburg and a summer-jackets-only party (per
requirements.md), a cold warning (below 5 C) should be assumed likely on physical
grounds alone, and rechecked with real numbers before departure.

## Ranked Nights
Ranking by darkness/moon alone (from night.md, weather unknown):

1. **2026-12-13** - illumination 20.2%, moon up only 16% of the dark window (sets
   20:01), better of the two on darkness/moon. Cloud cover for this night is
   currently unknown and cannot break or confirm this ranking.
2. **2026-12-14** - illumination 28.4%, moon up 27% of the window (sets 21:15),
   still within the "good" threshold but marginally worse on moon than the 13th.
   Cloud cover for this night is also unknown.

Site ranking (Zootzen vs Klessener See) cannot be weather-differentiated either,
since no forecast exists for either location on either date. Zootzen is preferred
per sites.md on travel time (69 vs 75 minutes) and identical estimated sky darkness,
independent of weather.

## Primary and Backup
| Slot | Site | Night | Mean cloud % | Why |
|---|---|---|---|---|
| Primary | Zootzen observation site | 2026-12-13 | not available | Best darkness/moon ranking of the two nights (night.md) and shorter drive of the two sites (sites.md); cloud cover cannot yet be assessed, so this pick is provisional, not a go decision. |
| Backup | Klessener See observation site | 2026-12-14 | not available | Second-best darkness/moon ranking, backup site with a slightly larger parking area (sites.md); also weather-unverified. |

**This plan is NO-GO pending a weather recheck.** No cloud-cover threshold from
requirements.md (max 40% in the dark window) can be evaluated today because no
forecast data exists for either candidate night. Do not treat the primary/backup
naming above as a green light to drive out — it only encodes the darkness/moon and
travel-time ranking, which is the only data currently available. The least-bad
fallback, if a forecast recheck later shows both nights over the cloud threshold, is
2026-12-13 at Zootzen, since it has the better darkness/moon profile of the two and
the more legally certain, closer access point of the two sites.

## Forecast Confidence
Today is 2026-09-21. The candidate nights are 83 and 84 days out. Open-Meteo's
`weather_forecast` endpoint currently only accepts start dates through 2026-10-06
(confirmed by the rejected call above), i.e. roughly a 15-16 day forecast horizon
from today. This is far beyond that horizon: there is no meaningful weather signal
to report, seasonal climatology is not a substitute, and none of the "not available"
cells above should be treated as indicative. This entire artifact must be
regenerated with a live Open-Meteo query once the candidate nights fall inside the
forecast window - i.e., from approximately 2026-11-29 (16 days before 2026-12-13)
onward, and again as a final check within 24 hours of departure, per the standing
rule for any forecast beyond 7 days out.

## Sources
- mcp__open-meteo__weather_forecast(latitude=52.786901, longitude=12.60948, hourly=["cloud_cover","cloud_cover_low","cloud_cover_mid","cloud_cover_high","precipitation_probability","wind_speed_10m","temperature_2m","dew_point_2m","relative_humidity_2m"], start_date="2026-12-13", end_date="2026-12-14", timezone="Europe/Berlin") -> error: "Invalid request parameters: Parameter 'start_date' is out of allowed range from 2026-06-20 to 2026-10-06"
- Open-Meteo forecast API documentation on model horizon limits: https://open-meteo.com/en/docs
- Candidate site coordinates and travel times: runs/2026-12-13-berlin-geminids/artifacts/sites.md
- Dark window and moon data for both candidate nights: runs/2026-12-13-berlin-geminids/artifacts/night.md
