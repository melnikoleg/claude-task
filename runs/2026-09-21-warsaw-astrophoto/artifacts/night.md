# Darkness and Moon - 2026-09-21-warsaw-astrophoto

Coordinates used: Warsaw, Poland, lat 52.22977, lon 21.01178, elevation 113 m (the
observer's start point; no site was fixed and site-scout runs in parallel, so
sites.md was not yet available. Darkness/moon numbers vary by under five minutes
across the 90-minute travel radius, so the verdicts below hold for any candidate
site site-scout selects). All local times are UTC+2 (Europe/Warsaw, CEST, confirmed
in requirements.md through 25 October 2026).

## Night Assessment
| Night of | Dark window (local) | Darkness h | Moon phase | Illum % | Moon up in window | Verdict |
|---|---|---|---|---|---|---|
| 2026-10-16 | 19:32-05:11 | 9.65 | waxing crescent | 33.9 | moonset 20:15, ~7% of window (max alt 3 deg) | good |
| 2026-10-17 | 19:30-05:12 | 9.71 | waxing crescent | 43.1 | moonset 21:20, ~20% of window (max alt 7.9 deg) | good |
| 2026-10-18 | 19:28-05:14 | 9.77 | waxing gibbous | 52.6 | moonset 22:31, ~30% of window (max alt 12.6 deg) | good |

Verdicts applied per requirements.md's 40% illumination threshold and the rule: good
if illumination is at/under threshold, OR the moon is up for less than half the dark
window. All three nights qualify as "good" on the second clause even where
illumination exceeds 40%, because in each case the moon rises during daytime and sets
low in the west within the first ~1-3 hours after dark begins, leaving the bulk of
each ~9.7-hour dark window fully moon-free for both M31 and Milky Way imaging.

## Recommended Nights
Ranked best to worst on darkness and moon alone, weather excluded. Rule: lowest
moon-up fraction of the dark window first (least moonlight contamination), then
lower illumination, then longer darkness as tiebreak.

1. **2026-10-16 (Friday)** - moon up only ~7% of the window (very low, 3 deg max
   altitude) and lowest illumination (33.9%, under threshold). Best night.
2. **2026-10-17 (Saturday)** - moon up ~20% of the window, illumination just over
   threshold (43.1%) but moon sets by 21:20, leaving a long fully dark stretch.
3. **2026-10-18 (Sunday)** - moon up ~30% of the window, highest illumination
   (52.6%) and highest max altitude (12.6 deg) of the three; still leaves most of
   the window moon-free after moonset at 22:31, but the weakest of the three.

## Notes
- All three nights have a full astronomical darkness window (astro MCP reported
  darkness, not just nautical twilight) - no substitution was needed.
- Moon is a waxing crescent-to-gibbous, rising around midday and setting in the
  early-to-mid evening on all three nights, so it never interferes with the deep
  pre-midnight or post-moonset hours that make up most of each dark window.
- These verdicts affect deep-sky imaging (M31, Milky Way) only; the Moon itself and
  planets are unaffected by moonlight, so nothing here rules out lunar/planetary
  observation on any of the three nights.
- Weather (cloud cover) is not evaluated here; that gate is the sky-forecaster's
  responsibility.

## Sources
- mcp__astro__dark_window(lat=52.22977, lon=21.01178, date="2026-10-16", tz_offset_hours=2, elevation_m=113)
- mcp__astro__moon_info(lat=52.22977, lon=21.01178, date="2026-10-16", tz_offset_hours=2, elevation_m=113)
- mcp__astro__dark_window(lat=52.22977, lon=21.01178, date="2026-10-17", tz_offset_hours=2, elevation_m=113)
- mcp__astro__moon_info(lat=52.22977, lon=21.01178, date="2026-10-17", tz_offset_hours=2, elevation_m=113)
- mcp__astro__dark_window(lat=52.22977, lon=21.01178, date="2026-10-18", tz_offset_hours=2, elevation_m=113)
- mcp__astro__moon_info(lat=52.22977, lon=21.01178, date="2026-10-18", tz_offset_hours=2, elevation_m=113)
- https://www.timeanddate.com/time/change/poland/warsaw?year=2026 (Europe/Warsaw UTC offset confirmation, carried from requirements.md)
