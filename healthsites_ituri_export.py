"""
healthsites_ituri_export.py
===========================
Fetches all health facilities in Ituri Province, DRC from the
healthsites.io API (v3) and writes a GeoJSON FeatureCollection to disk.

Part of the healthsites.io DRC Ebola 2026 response toolkit.
Repository: https://github.com/healthsites/drc-ebola-2026

Requirements:
    pip install requests

Usage:
    export HEALTHSITES_API_KEY="your_v3_token"
    python3 healthsites_ituri_export.py

API token registration: https://healthsites.io/enrollment/form
API documentation:      https://healthsites.io/api/docs/

────────────────────────────────────────────────────────────────────────
BOUNDING BOX SOURCE
────────────────────────────────────────────────────────────────────────
The Ituri Province bounding box is derived from the OCHA/OSM COD-AB
provincial boundary file for DRC:

  Source : OpenStreetMap DRC / opendatalabrdc
  HDX    : https://data.humdata.org/dataset/
             openstreetmap-dr-congo-provinces-boundaries-admin-level-2
  File   : rd_congo_admin_4_provinces.geojson
  Extent : west=27.4298, south=0.5196, east=31.3057, north=3.6835

────────────────────────────────────────────────────────────────────────
HEALTH ZONE REFERENCE DATA (Ituri, 36 health zones)
────────────────────────────────────────────────────────────────────────
The following HDX datasets provide authoritative health zone boundaries
for Ituri Province and can be used to spatially join or validate this
facility export:

1. GRID3 COD - Health Zones v3.0 (Ituri, CIESIN/MoH DRC, 2024)
   HDX  : https://data.humdata.org/dataset/grid3-cod-health-zones-v3-0
   File : GRID3_COD_Ituri_health_zones_v3_0.gpkg
   Note : Includes DHIS2 health zone codes. Supersedes earlier versions.
   Cite : CIESIN, Columbia University and Ministère de la Santé Publique,
          Hygiène et Prévention, DRC, 2024.

2. DRC Health Zone and Health Area Boundaries (DSNIS/WHO/MSF/GRID3, 2022)
   HDX  : https://data.humdata.org/dataset/drc-health-data
   File : RDC_Zones de santé.zip
   Note : 519 national health zones with DHIS2 codes; April 2022 update.

3. DPS Ituri (RDC) — OSM health sector data for Ituri Province
   HDX  : https://data.humdata.org/dataset/dps-ituri-rdc
   File : OSM_Ituri_FoSa_211201.gpkg
   Note : Formations Sanitaires (FoSa) extracted from OSM, Dec 2021.

Active outbreak health zones (as of May 2026):
   Mongbwalu, Rwampara, Bunia
   WHO sitrep: https://www.who.int/emergencies/disease-outbreak-news/
               item/2026-DON603
"""

import os
import json
import time
import requests
from datetime import date

# ── Configuration ─────────────────────────────────────────────────────────────

API_KEY  = os.environ.get("HEALTHSITES_API_KEY", "")
BASE_URL = "https://healthsites.io/api/v3/facilities/"

# Ituri Province bounding box [west, south, east, north]
# Derived from OCHA/OSM COD-AB DRC provincial boundary (see header above)
EXTENT = "27.4298,0.5196,31.3057,3.6835"

OUTPUT = "healthsites_ituri_drc.geojson"

# ── API ───────────────────────────────────────────────────────────────────────

def fetch_page(page: int) -> dict:
    """Fetch a single page of facilities from the healthsites.io v3 API."""
    if not API_KEY:
        raise ValueError(
            "HEALTHSITES_API_KEY environment variable is not set.\n"
            "Register for a token at: https://healthsites.io/enrollment/form"
        )
    params = {
        "api-key":         API_KEY,
        "extent":          EXTENT,
        "output":          "geojson",
        "flat-properties": "true",
        "page":            page,
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, str):
        raise ValueError(f"Unexpected API response: {data}")
    return data


def fetch_all() -> list:
    """Paginate through all results and return a flat list of GeoJSON features."""
    features, page = [], 1
    print(f"Querying: {BASE_URL}")
    print(f"  extent={EXTENT}")
    print(f"  output=geojson, flat-properties=true\n")
    while True:
        data          = fetch_page(page)
        page_features = data.get("features", [])
        if not page_features:
            print(f"  Page {page}: no more results.")
            break
        features.extend(page_features)
        print(f"  Page {page}: {len(page_features):>3} features  "
              f"(running total: {len(features)})")
        time.sleep(0.5)
        page += 1
    return features

# ── Output ────────────────────────────────────────────────────────────────────

def build_geojson(features: list) -> dict:
    """Wrap features in a standards-compliant GeoJSON FeatureCollection."""
    return {
        "type": "FeatureCollection",
        "name": "healthsites_ituri_drc",
        "description": (
            f"Health facilities in Ituri Province, DRC. "
            f"Exported {date.today().isoformat()} from healthsites.io. "
            f"Bounding box derived from OCHA/OSM COD-AB DRC provincial boundary: "
            f"https://data.humdata.org/dataset/"
            f"openstreetmap-dr-congo-provinces-boundaries-admin-level-2. "
            f"Health zone reference: GRID3 COD Health Zones v3.0 (Ituri): "
            f"https://data.humdata.org/dataset/grid3-cod-health-zones-v3-0. "
            f"Licence: ODbL 1.0 — https://opendatacommons.org/licenses/odbl/"
        ),
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": features,
    }


def main():
    print("healthsites.io — Ituri Province DRC facility export")
    print("=" * 52)

    features = fetch_all()

    if not features:
        print("\nNo facilities returned — check your API key and bounding box.")
        return

    geojson = build_geojson(features)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"\nExport complete.")
    print(f"  File     : {OUTPUT}")
    print(f"  Features : {len(features)}")
    print(f"  Size     : {size_kb:,.0f} KB")
    print(f"\nHealth zone reference data (HDX):")
    print(f"  GRID3 Ituri health zones v3.0:")
    print(f"  https://data.humdata.org/dataset/grid3-cod-health-zones-v3-0")


if __name__ == "__main__":
    main()
