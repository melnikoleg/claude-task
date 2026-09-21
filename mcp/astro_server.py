# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=2,<3", "ephem>=4.2"]
# ///
"""Astronomy MCP server: darkness windows, moon conditions, object visibility.

Everything the stargazing workflow must not guess. All times are returned in UTC
and in the caller's local offset; a "night" always means the evening of `date`
through the following morning.
"""

import datetime as dt
from typing import Any

import ephem
from mcp.server.mcpserver import MCPServer

server = MCPServer(
    "astro",
    version="1.0.0",
    instructions=(
        "Astronomical darkness, moon conditions and object visibility for a "
        "given site and night. Call list_catalog to see supported object names."
    ),
)

STEP_MINUTES = 20  # altitude sampling resolution; 3 samples make an hour

# ephem readdb lines: name,type,RA,Dec,magnitude,epoch
CATALOG_DB = {
    "M31": "M31,f|G,0:42:44,41:16:8,3.4,2000",
    "M42": "M42,f|U,5:35:17,-5:23:28,4.0,2000",
    "M45": "M45,f|U,3:47:0,24:7:0,1.6,2000",
    "M13": "M13,f|C,16:41:41,36:27:36,5.8,2000",
    "M57": "M57,f|P,18:53:35,33:1:45,8.8,2000",
    "M27": "M27,f|P,19:59:36,22:43:16,7.5,2000",
    "M51": "M51,f|G,13:29:53,47:11:43,8.4,2000",
    "M81": "M81,f|G,9:55:33,69:3:55,6.9,2000",
    "M82": "M82,f|G,9:55:52,69:40:47,8.4,2000",
    "M8": "M8,f|U,18:3:37,-24:23:12,6.0,2000",
    "M33": "M33,f|G,1:33:50,30:39:37,5.7,2000",
    "NGC7000": "NGC7000,f|U,20:59:17,44:31:44,4.0,2000",
    "ALBIREO": "Albireo,f|D,19:30:43,27:57:35,3.1,2000",
    "VEGA": "Vega,f|S,18:36:56,38:47:1,0.03,2000",
    "POLARIS": "Polaris,f|S,2:31:49,89:15:51,1.98,2000",
    "SIRIUS": "Sirius,f|S,6:45:9,-16:42:58,-1.46,2000",
    "MILKY WAY CORE": "Milky Way core,f|U,17:45:40,-29:0:28,0.0,2000",
    "DOUBLE CLUSTER": "Double Cluster,f|U,2:19:0,57:9:0,5.3,2000",
}

PLANETS = {
    "MOON": ephem.Moon,
    "MERCURY": ephem.Mercury,
    "VENUS": ephem.Venus,
    "MARS": ephem.Mars,
    "JUPITER": ephem.Jupiter,
    "SATURN": ephem.Saturn,
    "URANUS": ephem.Uranus,
    "NEPTUNE": ephem.Neptune,
}

ALIASES = {
    "ANDROMEDA": "M31",
    "ANDROMEDA GALAXY": "M31",
    "ORION NEBULA": "M42",
    "PLEIADES": "M45",
    "HERCULES CLUSTER": "M13",
    "GREAT GLOBULAR CLUSTER": "M13",
    "RING NEBULA": "M57",
    "DUMBBELL NEBULA": "M27",
    "WHIRLPOOL GALAXY": "M51",
    "BODES GALAXY": "M81",
    "CIGAR GALAXY": "M82",
    "LAGOON NEBULA": "M8",
    "TRIANGULUM GALAXY": "M33",
    "NORTH AMERICA NEBULA": "NGC7000",
    "PERSEUS DOUBLE CLUSTER": "DOUBLE CLUSTER",
    "NGC869": "DOUBLE CLUSTER",
    "GALACTIC CENTER": "MILKY WAY CORE",
}


def _resolve(name: str):
    key = " ".join(name.strip().upper().split())
    key = ALIASES.get(key, key)
    if key in PLANETS:
        return key.title(), PLANETS[key]()
    if key in CATALOG_DB:
        body = ephem.readdb(CATALOG_DB[key])
        return key, body
    raise ValueError(
        f"Unknown object {name!r}. Call list_catalog for supported names."
    )


def _observer(lat: float, lon: float, elevation_m: float = 0.0) -> ephem.Observer:
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = elevation_m
    obs.pressure = 0  # geometric horizons, no refraction guesswork
    return obs


def _utc(d: ephem.Date) -> dt.datetime:
    return ephem.Date(d).datetime().replace(tzinfo=dt.timezone.utc)


def _fmt(when: dt.datetime | None, tz_offset_hours: float) -> dict[str, str] | None:
    if when is None:
        return None
    local = when + dt.timedelta(hours=tz_offset_hours)
    return {
        "utc": when.strftime("%Y-%m-%d %H:%M UTC"),
        "local": local.strftime("%Y-%m-%d %H:%M"),
    }


def _night_start(date: str, tz_offset_hours: float) -> dt.datetime:
    """Local noon on `date`, as UTC - the anchor for 'the night of <date>'."""
    day = dt.date.fromisoformat(date)
    return dt.datetime.combine(day, dt.time(12, 0), tzinfo=dt.timezone.utc) - dt.timedelta(
        hours=tz_offset_hours
    )


def _compute_window(
    lat: float, lon: float, date: str, tz_offset_hours: float, elevation_m: float
) -> dict[str, Any]:
    obs = _observer(lat, lon, elevation_m)
    anchor = _night_start(date, tz_offset_hours)
    sun = ephem.Sun()

    obs.date = anchor
    obs.horizon = "-0:34"
    sunset = _utc(obs.next_setting(sun))
    sunrise = _utc(obs.next_rising(sun))

    obs.date = anchor
    obs.horizon = "-18"
    try:
        dark_start = _utc(obs.next_setting(sun, use_center=True))
        dark_end = _utc(obs.next_rising(sun, use_center=True))
        darkness_hours = round((dark_end - dark_start).total_seconds() / 3600, 2)
        note = ""
    except (ephem.AlwaysUpError, ephem.NeverUpError):
        dark_start = dark_end = None
        darkness_hours = 0.0
        note = (
            "No astronomical darkness on this date at this latitude "
            "(sun stays above -18 degrees). Nautical twilight is the darkest it gets."
        )
    return {
        "sunset": sunset,
        "sunrise": sunrise,
        "dark_start": dark_start,
        "dark_end": dark_end,
        "darkness_hours": darkness_hours,
        "note": note,
    }


def _samples(dark_start: dt.datetime, dark_end: dt.datetime, step_minutes: int = STEP_MINUTES):
    cur = dark_start
    while cur <= dark_end:
        yield cur
        cur += dt.timedelta(minutes=step_minutes)


@server.tool()
def list_catalog() -> dict[str, Any]:
    """List every object name object_visibility accepts, plus common aliases."""
    return {
        "planets_and_moon": sorted(PLANETS),
        "deep_sky_and_stars": sorted(CATALOG_DB),
        "aliases": ALIASES,
    }


@server.tool()
def dark_window(
    lat: float,
    lon: float,
    date: str,
    tz_offset_hours: float = 0.0,
    elevation_m: float = 0.0,
) -> dict[str, Any]:
    """Sunset, astronomical darkness window and sunrise for the night of `date`.

    Args:
        lat: Site latitude in decimal degrees (north positive).
        lon: Site longitude in decimal degrees (east positive).
        date: Evening date of the night, YYYY-MM-DD.
        tz_offset_hours: Local UTC offset for the site, e.g. 2 for CEST.
        elevation_m: Site elevation in metres.
    """
    w = _compute_window(lat, lon, date, tz_offset_hours, elevation_m)
    return {
        "site": {"lat": lat, "lon": lon, "elevation_m": elevation_m},
        "night_of": date,
        "tz_offset_hours": tz_offset_hours,
        "sunset": _fmt(w["sunset"], tz_offset_hours),
        "astronomical_dark_start": _fmt(w["dark_start"], tz_offset_hours),
        "astronomical_dark_end": _fmt(w["dark_end"], tz_offset_hours),
        "sunrise": _fmt(w["sunrise"], tz_offset_hours),
        "darkness_hours": w["darkness_hours"],
        "note": w["note"],
    }


@server.tool()
def moon_info(
    lat: float,
    lon: float,
    date: str,
    tz_offset_hours: float = 0.0,
    elevation_m: float = 0.0,
) -> dict[str, Any]:
    """Moon phase, illumination, rise/set and how much of the dark window it spoils.

    Args:
        lat: Site latitude in decimal degrees (north positive).
        lon: Site longitude in decimal degrees (east positive).
        date: Evening date of the night, YYYY-MM-DD.
        tz_offset_hours: Local UTC offset for the site, e.g. 2 for CEST.
        elevation_m: Site elevation in metres.
    """
    w = _compute_window(lat, lon, date, tz_offset_hours, elevation_m)
    obs = _observer(lat, lon, elevation_m)
    midpoint = w["sunset"] + (w["sunrise"] - w["sunset"]) / 2
    obs.date = midpoint
    moon = ephem.Moon(obs)
    illumination = round(float(moon.phase), 1)

    obs.date = _night_start(date, tz_offset_hours)
    obs.horizon = "-0:34"
    try:
        moonrise = _utc(obs.next_rising(ephem.Moon()))
    except (ephem.AlwaysUpError, ephem.NeverUpError):
        moonrise = None
    obs.date = _night_start(date, tz_offset_hours)
    try:
        moonset = _utc(obs.next_setting(ephem.Moon()))
    except (ephem.AlwaysUpError, ephem.NeverUpError):
        moonset = None

    moon_up_fraction = None
    max_moon_alt = None
    if w["dark_start"] and w["dark_end"]:
        pts = list(_samples(w["dark_start"], w["dark_end"]))
        up = 0
        alts = []
        body = ephem.Moon()
        for when in pts:
            obs.date = when
            body.compute(obs)
            alt_deg = float(body.alt) * 180.0 / ephem.pi
            alts.append(alt_deg)
            if alt_deg > 0:
                up += 1
        moon_up_fraction = round(up / len(pts), 2)
        max_moon_alt = round(max(alts), 1)

    prev_new = ephem.previous_new_moon(midpoint)
    age_days = round(float(ephem.Date(midpoint) - prev_new), 1)
    if illumination < 2:
        phase_name = "new moon"
    elif illumination > 98:
        phase_name = "full moon"
    elif age_days < 14.77:
        phase_name = "waxing crescent" if illumination < 50 else "waxing gibbous"
    else:
        phase_name = "waning gibbous" if illumination > 50 else "waning crescent"

    return {
        "night_of": date,
        "phase": phase_name,
        "illumination_percent": illumination,
        "moon_age_days": age_days,
        "moonrise": _fmt(moonrise, tz_offset_hours),
        "moonset": _fmt(moonset, tz_offset_hours),
        "moon_up_fraction_of_dark_window": moon_up_fraction,
        "max_moon_altitude_deg": max_moon_alt,
        "dark_window": {
            "start": _fmt(w["dark_start"], tz_offset_hours),
            "end": _fmt(w["dark_end"], tz_offset_hours),
            "hours": w["darkness_hours"],
        },
        "note": w["note"],
    }


@server.tool()
def object_visibility(
    lat: float,
    lon: float,
    date: str,
    object_name: str,
    tz_offset_hours: float = 0.0,
    elevation_m: float = 0.0,
    min_altitude_deg: float = 20.0,
) -> dict[str, Any]:
    """Altitude track of one object across the night's astronomical dark window.

    Args:
        lat: Site latitude in decimal degrees (north positive).
        lon: Site longitude in decimal degrees (east positive).
        date: Evening date of the night, YYYY-MM-DD.
        object_name: Object to check; see list_catalog.
        tz_offset_hours: Local UTC offset for the site, e.g. 2 for CEST.
        elevation_m: Site elevation in metres.
        min_altitude_deg: Altitude counted as observable.
    """
    name, body = _resolve(object_name)
    w = _compute_window(lat, lon, date, tz_offset_hours, elevation_m)
    if not w["dark_start"]:
        return {
            "object": name,
            "night_of": date,
            "observable": False,
            "reason": w["note"] or "no astronomical darkness",
        }

    obs = _observer(lat, lon, elevation_m)
    track = []
    best_alt = -90.0
    best_time = None
    above = 0
    for when in _samples(w["dark_start"], w["dark_end"]):
        obs.date = when
        body.compute(obs)
        alt = round(float(body.alt) * 180.0 / ephem.pi, 1)
        az = round(float(body.az) * 180.0 / ephem.pi, 1)
        track.append(
            {
                "time_local": (when + dt.timedelta(hours=tz_offset_hours)).strftime("%H:%M"),
                "altitude_deg": alt,
                "azimuth_deg": az,
            }
        )
        if alt > best_alt:
            best_alt, best_time = alt, when
        if alt >= min_altitude_deg:
            above += 1

    hours_above = round(above * STEP_MINUTES / 60.0, 2)
    magnitude = None
    try:
        magnitude = round(float(body.mag), 1)
    except (AttributeError, TypeError):
        pass

    return {
        "object": name,
        "night_of": date,
        "magnitude": magnitude,
        "max_altitude_deg": round(best_alt, 1),
        "max_altitude_time": _fmt(best_time, tz_offset_hours),
        "hours_above_min_altitude": hours_above,
        "min_altitude_deg": min_altitude_deg,
        "observable": hours_above >= 1.0,
        "dark_window": {
            "start": _fmt(w["dark_start"], tz_offset_hours),
            "end": _fmt(w["dark_end"], tz_offset_hours),
            "hours": w["darkness_hours"],
        },
        "altitude_track": track[::3],  # every hour
    }


if __name__ == "__main__":
    server.run()
