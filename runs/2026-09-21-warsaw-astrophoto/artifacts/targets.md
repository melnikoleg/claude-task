# Target List - 2026-09-21-warsaw-astrophoto

Gear owned: Canon EOS R6 (full-frame, 20.1 MP, ~5.98 micron pixel pitch), Samyang/generic
24mm f/1.8 lens, sturdy tripod, **no star tracker**. All exposures below are therefore
untracked and are capped by the NPF rule, not the simpler 500-rule, because the R6's
pixel pitch is small enough that the 500-rule's ~20.8s (500/24mm) would already show
star trailing on a 20MP sensor. NPF rule used: t = (35 x f-number + 30 x pixel pitch
microns) / focal length mm = (35 x 1.8 + 30 x 5.98) / 24 = **10.1 s, rounded to 10 s**.

Planning is anchored on the two best-ranked nights from night.md (sky-forecast.md does
not exist yet in this parallel run): primary **2026-10-16** (moon up only ~7% of the
9.65 h dark window, 19:34-05:14 local) and secondary **2026-10-17** (moon up ~20% of
the 9.72 h dark window, 19:32-05:15 local). Altitudes are given for both. Site used for
the MCP calls is the recommended site from sites.md, Bolimowski Landscape Park farmland
edge (lat 51.97901, lon 20.35037, elevation 137 m); night.md notes altitude differences
across the 90-minute travel radius are under 5 minutes of local time, so these numbers
hold for the runner-up site (Chrosna) too.

24mm on a full-frame R6 gives a field of view of about 74 deg (horizontal) x 53 deg
(vertical). M31's apparent size is roughly 3 x 1 degrees, so at 24mm it fills well under
5% of the frame width - a small, unresolved smudge in a wide starfield, not a close-up
of the galaxy's spiral structure. This plan is honest about that: M31 here is a
wide-field "constellation portrait" target, not a detail shot.

## Targets

### Andromeda Galaxy (M31)

| Field | Value |
|---|---|
| Type | galaxy |
| Magnitude | 3.4 |
| Max altitude | 79.4 deg at 23:34 local (2026-10-16, transit); 79.4 deg at 23:32 local (2026-10-17, transit) |
| Hours above 20 deg in dark window | 9.67 h on 2026-10-16 (essentially the whole dark window - already 47.7 deg at dark-window start 19:34); 10.0 h on 2026-10-17 |
| Best observing slot | 19:34-05:14 local on 2026-10-16 (whole window usable); tightest framing and lowest atmospheric extinction near transit, 22:30-00:30 |
| Mode notes | 24mm f/1.8 on tripod, no tracking. NPF-rule exposure 10 s, ISO 3200, f/1.8 (wide open for light gathering; some coma/vignetting at the corners is expected and acceptable for a wide-field frame). Shoot 80-120 subs of 10 s (about 15-20 minutes of stacked integration) plus calibration frames. Because the frame is 74 x 53 deg and Earth's rotation is only ~15 deg/hour, no re-aiming is needed for at least an hour of shooting - the galaxy will not drift out of frame. |
| What you will actually see | A small, soft, elongated grey smudge with a brighter core near the frame's position, set against a wide starfield with Cassiopeia nearby - not a close-up of the galaxy's disc or dust lanes; that requires a telephoto lens and, ideally, tracking. |

## Observing Order

1. **Setup (19:00-19:30 local, before the dark window opens at 19:32-19:34)**: arrive at
   the site while there is still residual twilight, level the tripod, mount the R6,
   set focus to infinity using a bright star or distant light with live-view
   magnification, take test frames, and dial in framing for M31 against Cassiopeia.
   Budget the full 20-30 minutes - this is the party's first night at this site and
   with this exact framing.
2. **M31 sequence, 19:40-04:30 local**: begin light frames as soon as the dark window
   opens and M31 clears the site's tree-line horizon comfortably (already 47.7 deg
   at 19:34). Shoot the 80-120 x 10 s subs in two or three sittings spread either side
   of the 23:32-23:34 local transit (when the galaxy is highest, at 79.4 deg, giving
   the least atmospheric extinction and the darkest sky background), rather than one
   continuous burst, so a few frames can be reviewed and refocus/leveling rechecked
   partway through the night.
3. **Wide starfield / nightscape frames, whenever composition suits (per requirements.md
   step 3 guidance and rule 4 below)**: the galactic core requested as "Milky Way" is
   not usable this night (see Rejected Targets); if the party wants extra frames beyond
   M31, use spare time before moonrise/after M31 sequences for simple wide constellation
   or foreground-inclusive shots (10 s, ISO 3200, f/1.8) of whatever is highest and
   darkest at the time - untracked wide fields tolerate opportunistic timing since there
   is no single meridian-critical object.
4. **Calibration frames**:
   - **Darks**: 20-30 dark frames at the same 10 s / ISO 3200 / same ambient temperature,
     shot with the lens cap on either immediately after the light frames at the site
     (battery and time permitting) or at home before/after the trip if temperature is
     close to the shoot night.
   - **Flats**: 20-30 flat frames at dawn twilight or against a uniformly lit white
     screen/t-shirt over the lens, same aperture (f/1.8) and focus as the lights, ISO
     and exposure auto-adjusted for a mid-grey histogram; shoot these before breaking
     down the tripod so the lens/sensor orientation matches the lights (any sensor dust
     shadows must line up).
   - **Bias**: 20-30 frames at the fastest shutter speed with the lens cap on, any time;
     not scene-dependent.
5. **Pack down after 04:30-05:00 local**, ahead of the 05:14 dark-window end, to be off
   site with margin before the drive home.

## Rejected Targets

- **Milky Way (galactic core / Sagittarius region), as literally requested**: rejected
  by rule 4 (20 deg / 1-hour threshold). `mcp__astro__object_visibility` for
  `MILKY WAY CORE` returns a max altitude of only **0.9 deg at 19:34 local on
  2026-10-16** and **0.7 deg at 19:32 local on 2026-10-17** - the core rises barely
  above the horizon at dusk and is below the horizon (negative altitude) for the rest
  of both dark windows. `hours_above_min_altitude` is 0 on both nights. This is an
  October seasonal effect at Warsaw's latitude (52 deg N), not a site or weather
  problem: the bright Sagittarius/core region of the Milky Way sets with the Sun in
  mid-autumn from this latitude and will not return to a useful evening altitude until
  spring. No amount of site selection or clear sky fixes this on 16-18 October 2026.
  Note for the observer: the fainter northern arm of the Milky Way (through Cassiopeia,
  Perseus and Cygnus) is above the horizon and naked-eye visible at a dark site, but the
  astro MCP catalog only tracks the galactic-core object, not that diffuse band, so no
  altitude/transit figure can be cited for it here - it is not listed as a planned
  target for that reason, only mentioned as an honest aside.

## Sources
- mcp__astro__list_catalog()
- mcp__astro__object_visibility(lat=51.97901, lon=20.35037, date="2026-10-16", object_name="M31", tz_offset_hours=2, elevation_m=137)
- mcp__astro__object_visibility(lat=51.97901, lon=20.35037, date="2026-10-16", object_name="MILKY WAY CORE", tz_offset_hours=2, elevation_m=137)
- mcp__astro__object_visibility(lat=51.97901, lon=20.35037, date="2026-10-17", object_name="M31", tz_offset_hours=2, elevation_m=137)
- mcp__astro__object_visibility(lat=51.97901, lon=20.35037, date="2026-10-17", object_name="MILKY WAY CORE", tz_offset_hours=2, elevation_m=137)
- https://photographylife.com/500-rule-vs-npf-rule - NPF rule formula and rationale for high-resolution sensors
- https://www.photopills.com/articles/milky-way-photography-settings - untracked wide-field exposure/ISO practice used to sanity-check the NPF result
- https://astrobackyard.com/photographing-the-andromeda-galaxy/ - realistic expectations and frame-count guidance for wide-field/untracked M31 imaging
