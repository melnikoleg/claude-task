# Darkness and Moon - 2026-09-21-izera-visual

Coordinates used: Świeradów-Zdrój, Poland (proxy for Izera Dark-Sky Park), lat 50.9092, lon 15.34309, elevation 465 m, per requirements.md (site fixed by observer; exact park point not resolvable via geocoding). All local times below are UTC+1 (CET, Poland is off DST from 2026-10-25).

Hard constraint carried from requirements.md: session must end by 22:30 (child curfew, driven by last bus back to Szklarska Poręba), overriding darkest-window optimization. This overrides the usual "rank by darkest/lowest-moon window" approach: the figure that matters downstream is how much dark, moon-clean sky falls between dark-window start and 22:30, not the full night.

## Night Assessment
One row per candidate night, all values from the astro MCP:

| Night of | Dark window (local) | Darkness h | Moon phase | Illum % | Moon up in window | Usable dark window before 22:30 curfew | Verdict |
|---|---|---|---|---|---|---|---|
| 2026-11-05 | 18:19 - 05:05 | 10.78 | Waning crescent | 11.3% | 12% (moonrise 03:44, max alt 9.9°, in final ~80 min of window, i.e. well after curfew) | 18:19 - 22:30 = 4h11m, entirely moon-free (moon rises 03:44, long after curfew) | good |
| 2026-11-06 | 18:17 - 05:07 | 10.83 | Waning crescent | 5.7% | 0% (moon sets 14:53, before dark window starts; moonrise 05:00 next day, after window ends) | 18:17 - 22:30 = 4h13m, entirely moon-free | good |
| 2026-11-07 | 18:16 - 05:08 | 10.88 | Waning crescent | 2.0% | 0% (moon sets 15:08, before dark window starts; moonrise 06:16 next day, after window ends) | 18:16 - 22:30 = 4h14m, entirely moon-free | good |

## Recommended Nights
Ranking rule: within the curfew-bounded session (dark-window start through 22:30, since the child must be home by 22:30 regardless of how dark the rest of the night gets), rank by lower moon illumination and lower moon-up fraction of that pre-22:30 stretch; darkness-hours differences are negligible (all ~4h11m-4h14m of usable dark sky before curfew) so illumination is decisive. Weather is excluded from this ranking (sky-forecaster's remit).

All three nights deliver a full, moon-free dark stretch before the 22:30 curfew - the moon is either already set or has not yet risen in every case, so the curfew constraint does not cost any of the three nights their darkest, moon-cleanest hours. The only differentiator left is background illumination phase, which is marginal on all three.

1. **2026-11-07** - best: 2.0% illumination, moon up 0% of the full window and 0% of the pre-22:30 stretch (18:16-22:30 available, fully moon-free).
2. **2026-11-06** - very close second: 5.7% illumination, moon up 0% of the full window and 0% of the pre-22:30 stretch (18:17-22:30 available, fully moon-free).
3. **2026-11-05** - still good but weakest of the three: 11.3% illumination overall, though irrelevant to the pre-22:30 stretch since the moon does not rise until 03:44, hours after curfew (18:19-22:30 available, fully moon-free).

All three nights clear the 40% illumination threshold from requirements.md comfortably and qualify as `good` under the stated rule (illumination at or under threshold), both for the full night and for the curfew-bounded session.

## Notes
- Dark window start times (18:16-18:19 local) leave roughly 4h11m-4h14m of full astronomical darkness before the 22:30 curfew on all three nights - session-plan-builder should treat this pre-22:30 stretch, not the full ~10.8h dark window, as the usable observing session.
- Moon phase is waning crescent all three nights, heading toward new moon (~2026-11-09/10 based on the increasing moon age: 26.3 -> 27.3 -> 28.3 days), so conditions only improve night to night.
- On 2026-11-05 the moon rises at 03:44 local, well inside the full dark window (which runs to 05:05) but far outside the curfew-bounded session (ends 22:30); its maximum altitude of 9.9° is low, so contamination is confined to the pre-dawn end of the full window and has zero effect on the actual 18:19-22:30 session.
- Jupiter is a planet, so moonlight (present or not) does not affect its visibility on any of the three nights, in the full window or the curfew-bounded session.
- No astronomical-darkness failure on any night; full dark windows of ~10.8-10.9 hours are available all three nights, of which ~4h11m-4h14m fall before the 22:30 curfew.
- Downstream agents (sky-forecaster, target planner) should check target altitude/timing for Jupiter, M42 and M45 specifically within the curfew-bounded 18:16/17/19-22:30 stretch, not the full dark window, given the hard 22:30 end time.

## Sources
- mcp__astro__dark_window(lat=50.9092, lon=15.34309, date="2026-11-05", tz_offset_hours=1, elevation_m=465)
- mcp__astro__moon_info(lat=50.9092, lon=15.34309, date="2026-11-05", tz_offset_hours=1, elevation_m=465)
- mcp__astro__dark_window(lat=50.9092, lon=15.34309, date="2026-11-06", tz_offset_hours=1, elevation_m=465)
- mcp__astro__moon_info(lat=50.9092, lon=15.34309, date="2026-11-06", tz_offset_hours=1, elevation_m=465)
- mcp__astro__dark_window(lat=50.9092, lon=15.34309, date="2026-11-07", tz_offset_hours=1, elevation_m=465)
- mcp__astro__moon_info(lat=50.9092, lon=15.34309, date="2026-11-07", tz_offset_hours=1, elevation_m=465)
- https://www.izerskipark.pl/ - Izera Dark-Sky Park site reference (carried from requirements.md for site context).
