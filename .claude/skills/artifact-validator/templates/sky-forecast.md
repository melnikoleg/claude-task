# Sky Forecast - <run-id>

## Forecast by Site and Night
One row per site and night, hourly values averaged over the dark window only:

| Site | Night of | Mean cloud % | Low/Mid/High cloud % | Precip prob % | Wind m/s | Temp C | Dew point C | Dew risk | Verdict |
|---|---|---|---|---|---|---|---|---|---|

## Ranked Nights
Best to worst, combining cloud cover with night.md's darkness ranking.

## Primary and Backup
| Slot | Site | Night | Mean cloud % | Why |
|---|---|---|---|---|
| Primary | | | | |
| Backup | | | | |

## Forecast Confidence
Days out, model used, and how much the plan should trust it.

## Sources
- open-meteo MCP calls with coordinates, dates and the hourly variables requested.
