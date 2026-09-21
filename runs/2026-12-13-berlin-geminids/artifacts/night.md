# Darkness and Moon - 2026-12-13-berlin-geminids

Coordinates used: Berlin start point, lat 52.52437, lon 13.41053, elevation 46 m
(observer did not fix a specific site; requirements.md leaves site selection to
site-scout within 80 minutes of Berlin — darkness and moon shift by under 5 minutes
across that radius, so these verdicts hold regardless of the exact site chosen).

All local times below are UTC+1 (Europe/Berlin standard time, December).

## Night Assessment
One row per candidate night, all values from the astro MCP:

| Night of | Dark window (local) | Darkness h | Moon phase | Illum % | Moon up in window | Verdict |
|---|---|---|---|---|---|---|
| 2026-12-13 | 17:59 - 06:02 | 12.05 | Waxing crescent (age 4.9 d) | 20.2% | 16% of window (moonset 20:01; max alt 12.2°) | good |
| 2026-12-14 | 17:59 - 06:03 | 12.06 | Waxing crescent (age 5.9 d) | 28.4% | 27% of window (moon up 17:59-21:15, moonset 21:15; max alt 19.8°) | good |

Both nights have illumination well under the 40% threshold from requirements.md, and
the moon is up for well under half of each dark window. Both qualify as `good` for
deep-sky/meteor viewing. The Moon itself is unaffected by moonlight and is visible low
in the west shortly after dark on both nights for the observer's opportunistic
secondary target, before it sets.

## Recommended Nights
Ranking rule: lower moon illumination and lower fraction of the dark window with the
moon above the horizon rank better (darkness hours are effectively identical at ~12.05h
both nights, so illumination and moon-up fraction decide the order). Weather is
excluded from this ranking; that is the sky-forecaster's job.

1. **2026-12-13** - illumination 20.2%, moon up only 16% of the window (sets 20:01,
   well before midnight), lower max altitude (12.2°). Best moon conditions of the two.
2. **2026-12-14** - illumination 28.4%, moon up 27% of the window (sets 21:15), still
   well within the good threshold but slightly worse than the 13th.

Both nights are usable; 2026-12-13 is the marginally better of the two on
darkness/moon alone.

## Notes
- Neither night lacks astronomical darkness; both have a full ~12-hour dark window
  well inside the December long night, so no nautical-twilight fallback is needed.
- On both nights the moon rises the following morning (after 10:00 local), so once it
  sets in the evening it does not return before the dark window ends — no mid-session
  moonrise to plan around.
- For the observer's secondary goal of viewing the Moon itself: it is a thin waxing
  crescent low in the west right after dark on both nights (max altitude only 12-20°),
  visible for a short window before it sets — best viewed 2026-12-14 for a slightly
  higher, longer-visible crescent (up until 21:15 vs 20:01), even though 12-13 wins on
  overall darkness for meteors.
- Geminids peak activity timing (radiant altitude through the night) is not computed
  here; this artifact covers darkness and moon only.

## Sources
- mcp__astro__dark_window(lat=52.52437, lon=13.41053, date="2026-12-13", tz_offset_hours=1, elevation_m=46)
- mcp__astro__moon_info(lat=52.52437, lon=13.41053, date="2026-12-13", tz_offset_hours=1, elevation_m=46)
- mcp__astro__dark_window(lat=52.52437, lon=13.41053, date="2026-12-14", tz_offset_hours=1, elevation_m=46)
- mcp__astro__moon_info(lat=52.52437, lon=13.41053, date="2026-12-14", tz_offset_hours=1, elevation_m=46)
- Europe/Berlin UTC+1 standard time in December, confirmed per requirements.md: https://www.timeanddate.com/time/zone/germany/berlin
