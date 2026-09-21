# Gear Plan - 2026-09-21-warsaw-astrophoto

Checklist-only mode: the 150 EUR budget is earmarked for fuel only (requirements.md,
Budget/Covers), and the observer's gear list is stated as fixed. No purchases are
proposed against that budget; this artifact checks owned gear against the plan's
demands and turns any genuine, zero-cost-workaround-only need into a checklist note.

## Owned Gear Check
| Item | Covers | Good enough? |
|---|---|---|
| Canon EOS R6 | Image capture, high-ISO (ISO 3200) wide-field subs for M31 | Yes - targets.md's NPF-rule plan (10 s, ISO 3200, f/1.8, 80-120 subs) is built around this body's 5.98 micron pixel pitch |
| 24mm f/1.8 lens | Wide-field framing of M31 against Cassiopeia (74 x 53 deg FOV) | Yes - matches targets.md framing and exposure math exactly |
| Sturdy tripod | Vibration-free support for 10 s untracked subs | Yes - untracked NPF-rule exposures only need a stable platform, not a tracker |
| No star tracker (owned gear explicitly excludes one) | N/A | Not a gap - targets.md deliberately plans untracked 10 s subs via the NPF rule because no tracker is owned; buying one is out of scope (astrophoto detail beyond a "constellation portrait" was already ruled out in targets.md) |

## Gaps to Fill
| Item | Why the night needs it | Buy or rent | Price | Where |
|---|---|---|---|---|

No gaps. The 150 EUR budget is earmarked for fuel only (requirements.md, Budget/Covers:
"no gear purchases (observer gear list is fixed)"), so this table stays empty per the
workflow's zero-gear-budget rule. Two items that would normally appear as purchases in
an astrophoto gear plan are handled instead as zero-cost workarounds below, not bought:

- **Remote shutter release / intervalometer**: not needed. Exposures are 10 s (well
  under bulb threshold, per targets.md's NPF-rule calc), so the R6's built-in 2-second
  self-timer plus continuous drive mode fires the 80-120 subs hands-off without touching
  the body during exposure, avoiding shutter-shake without buying an accessory.
- **Spare battery**: not budgeted. Workaround below (Power section) - keep the single
  owned battery warm and minimize LCD/live-view use between sequences to stretch its
  charge across the ~9.5 h session instead of buying a second LP-E6NH.

## Night Checklist

### Optics
- Canon R6 + 24mm f/1.8 lens, mounted on the owned tripod, leveled at setup (owned)
- Lens hood if owned, to cut stray light/dew ingress at the front element (owned, if held)
- Microfiber lens cloth, checked every 20-30 min for dew film on the front element -
  October farmland-edge nights commonly dew up under clear sky even though
  sky-forecast.md has no dew-point number yet for 2026-10-16/17 (forecast horizon
  does not reach these dates - see sky-forecast.md Forecast Horizon Check); treat this
  as a standing precaution, not a confirmed trigger, and recheck once real dew-point
  data lands (sky-forecast.md's recheck schedule: first indicative numbers from
  ~2026-10-01, moderately reliable from ~2026-10-09)
- Memory card(s) with enough free space for 150-200+ RAW frames (lights + darks +
  flats + bias) and a spare card as backup (assumed owned - already implied by having
  a working camera kit; not listed as a gap since nothing in requirements.md or
  targets.md flags it missing)

### Power
- Fully charged camera battery, installed
- Keep the battery in an inner jacket pocket (body heat) between shooting blocks
  rather than left on the camera in the cold - cold significantly cuts lithium-ion
  battery life (roughly halved per ~10 C drop), and no spare battery is budgeted (see
  Gaps to Fill), so conserving the one battery matters more here than usual
- Minimize chimping/live-view review time to stretch the single battery across the
  full ~9.5 h dark window (19:3x-05:1x local, per targets.md observing order)
- Phone, charged, for navigation, red-light-mode/backup light, and a go/no-go weather
  recheck the night before (per sky-forecast.md's 24-hours-before final check)

### Warmth
- Layered warm clothing (base layer, insulating mid layer, windproof/waterproof
  outer shell), warm hat, gloves (ideally touchscreen-compatible for camera controls),
  insulated boots - an October overnight session in Poland (setup from 19:00, pack-down
  by 05:00) runs well past midnight in open farmland; sky-forecast.md has no confirmed
  temperature for 2026-10-16/17 yet (forecast horizon does not reach these dates), so
  this is precautionary for a typical Polish October night, not tied to a specific
  forecast number - reconfirm actual overnight low against sky-forecast.md once it is
  updated (from ~2026-10-09) and adjust layering before departure
- Hot drink in a thermos, for both adults across the long standing/waiting session

### Safety
- Red-light headlamp (preserves night vision during setup, refocusing checks, and
  calibration-frame work)
- Phone charged and carried (see Power) - signal check at the farmland site is worth
  doing on arrival since it is the primary means of calling for help or checking a
  last-minute weather update
- Basic first-aid items if normally carried in the car

### Comfort
- Something to sit on (camp chair or folding stool) for the long stationary M31
  sequence and calibration-frame waiting periods
- Snacks for the two adults across the ~9.5 h session
- A simple compass/star app orientation reference for setup, if not already using the
  phone for that

## Sources
- runs/2026-09-21-warsaw-astrophoto/artifacts/requirements.md - Owned Gear list;
  Budget/Covers ("no gear purchases"); party size (2 adults, no children)
- runs/2026-09-21-warsaw-astrophoto/artifacts/targets.md - NPF-rule 10 s exposure calc
  confirming no tracker/remote-release is required; ~9.5 h observing-order timeline
  (19:00 setup to 04:30-05:00 pack-down) used to size battery/warmth/comfort needs
- runs/2026-09-21-warsaw-astrophoto/artifacts/sky-forecast.md - Forecast Horizon Check
  (no cloud/wind/temperature/dew-point numbers exist yet for 2026-10-16/17/18) and its
  recheck schedule, cited for every weather-driven checklist item above
- https://www.slrlounge.com/cold-weather-photography-tips-how-to-protect-your-batteries-from-the-cold/ - cold-weather lithium-ion battery drain (roughly halved per ~10 C drop), backing the single-battery conservation workaround above
