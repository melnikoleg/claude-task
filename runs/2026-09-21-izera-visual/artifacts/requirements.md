# Requirements - 2026-09-21-izera-visual

The observer, staying in Szklarska Poręba, wants a visual, binoculars-only stargazing night at the fixed Izera Dark-Sky Park on one of 5, 6 or 7 November 2026, for two adults and a 9-year-old traveling on foot or by local bus, to view Jupiter, the Orion Nebula and the Pleiades with their owned 10x50 binoculars, within a 40 EUR total budget and a maximum 60-minute one-way travel time, with the hard constraint that the session must start early and end by 22:30 so the child is home on time, governed by the last bus back to Szklarska Poręba rather than by darkest-sky timing.

## Observer Profile
| Field | Value |
|---|---|
| Party | 2 adults, 1 child (age 9); no stated experience level |
| Mobility / constraints | No car; travel on foot or by local bus; hard bedtime constraint - child must be home by 22:30, so the session must start early and end by 22:30; last bus back to Szklarska Poręba is the binding scheduling factor, taking priority over maximizing dark-window/darkest-hour coverage; child's cold tolerance not stated |
| Transport | Public transport (local bus) or on foot; no car |

## Observing Mode
`visual` - the observer did not name a camera or ask for photos; they asked to view targets by eye/binoculars only (telescope idea withdrawn by the observer).

## Site
| Field | Value |
|---|---|
| Home / start point | Szklarska Poręba, Poland, lat 50.82567, lon 15.52274 |
| Site fixed by user? | yes |
| Named site (if fixed) | Izera Dark-Sky Park, Poland - not present in the geocoding database as a distinct point; nearest resolvable named settlement within the park area used as coordinate proxy: Świeradów-Zdrój, lat 50.9092, lon 15.34309, elevation 465 m |
| Max travel | 60 minutes |
| Timezone offset | UTC+1 on 5-7 November 2026 (Poland is on CET; DST ends 2026-10-25) |

## Candidate Nights
- 2026-11-05
- 2026-11-06
- 2026-11-07

## Targets Requested
- Jupiter
- Orion Nebula (M42)
- Pleiades (M45)

## Owned Gear
- One pair of 10x50 binoculars
- Warm clothes

## Budget
| Field | Value |
|---|---|
| Limit | 40 EUR |
| Covers | Travel/gear-related spend if any; no telescope rental or purchase (observer withdrew the telescope idea - observing is binoculars-only); no other spend categories stated by the observer |

## Thresholds
| Gate | Value |
|---|---|
| Max cloud cover in dark window | 40% (default; observer did not specify) |
| Max moon illumination tolerated | 40% (default; observer did not specify) |
| Max travel time one way | 60 minutes (observer-specified) |
| Session end time | 22:30 local, hard constraint (observer-specified); session must start early enough to end by this time, scheduled around the last bus back to Szklarska Poręba rather than around darkest-sky timing |

## Assumptions
- No party experience level or child's cold tolerance was stated; downstream agents should treat comfort as unconstrained beyond "warm clothes" owned and the hard 22:30 end time.
- The exact geographic point for "Izera Dark-Sky Park" is not resolvable via the geocoding tool; Świeradów-Zdrój, the nearest named settlement associated with the park, is used as a coordinate proxy for elevation/timezone purposes only. Downstream agents (e.g. night-calculator, sky-forecaster) should refine to the park's actual observation point if a more precise source is found.
- Max cloud cover (40%) and max moon illumination (40%) use workflow defaults since the observer gave no numbers.
- Budget "covers" scope is assumed to include only travel/gear costs implied by the plan (no telescope, per observer correction); the observer did not itemize food, fees, etc.
- No maximum party fatigue/duration for the child was stated beyond the hard 22:30 end time.
- The exact local bus schedule for the return trip to Szklarska Poręba is not stated by the observer; downstream agents (e.g. site-scout, session-plan-builder) must source the actual last-bus time to fix the session end.

## Sources
- mcp__open-meteo__geocoding(name="Szklarska Poręba", countryCode="PL") - resolved start point lat 50.82567, lon 15.52274, elevation 647 m.
- mcp__open-meteo__geocoding(name="Izera Dark-Sky Park") - no results.
- mcp__open-meteo__geocoding(name="Izerski Park Ciemnego Nieba") - no results.
- mcp__open-meteo__geocoding(name="Izera", countryCode="PL") - no results.
- mcp__open-meteo__geocoding(name="Świeradów-Zdrój") - resolved lat 50.9092, lon 15.34309, elevation 469 m, used as nearest named-place proxy for the Izera Dark-Sky Park site.
- mcp__open-meteo__elevation(latitude=50.9092, longitude=15.34309) - elevation 465 m.
- https://www.izerskipark.pl/ - Izera Dark-Sky Park official information, used to confirm the park's location context near Świeradów-Zdrój.
