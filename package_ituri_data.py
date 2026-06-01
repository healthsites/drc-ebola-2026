"""
package_ituri_data.py

Packages healthsites_ituri_drc.geojson together with a LICENSE.txt
into a distributable zip file ready for email attachment.

Usage:
    python3 package_ituri_data.py
"""

import zipfile
import os
from datetime import date

GEOJSON_FILE = "healthsites_ituri_drc.geojson"
OUTPUT_ZIP   = "healthsites_ituri_drc.zip"

LICENSE_TEXT = """\
healthsites.io — Ituri Province DRC Health Facilities
======================================================
Export date : {date}
Source      : healthsites.io (Global Healthsites Mapping Project)
API query   : https://healthsites.io/api/v3/facilities/
              ?extent=27.0,-3.0,31.5,2.5&output=geojson&flat-properties=true
Coverage    : Ituri Province, Democratic Republic of Congo
              Bounding box: 27.0°E, 3.0°S — 31.5°E, 2.5°N
Upstream    : OpenStreetMap contributors

------------------------------------------------------------------------
DATA LICENCE: Open Database Licence (ODbL) 1.0
------------------------------------------------------------------------
You are free to:
  - Share  : copy, distribute and use the database
  - Create : produce works from the database
  - Adapt  : modify, transform and build upon the database

As long as you:
  - Attribute   : credit healthsites.io and OpenStreetMap contributors
                  in any public use or redistribution
  - Share-Alike : any adapted database must also be offered under ODbL
  - Keep open   : any redistribution must include a version free of
                  technological access restrictions

Full licence text: https://opendatacommons.org/licenses/odbl/
healthsites.io licence page:
  https://github.com/healthsites/healthsites/wiki/healthsites.io-license

------------------------------------------------------------------------
ATTRIBUTION
------------------------------------------------------------------------
© healthsites.io contributors and OpenStreetMap contributors.
Data is available under the Open Database Licence.
Cartography (if any) is available under CC BY 4.0.

When citing this dataset please use:
  healthsites.io ({year}). Health facility data for Ituri Province, DRC.
  Retrieved {date} from https://healthsites.io
  Licence: ODbL 1.0 — https://opendatacommons.org/licenses/odbl/


""".format(date=date.today().isoformat(), year=date.today().year)


def main():
    if not os.path.exists(GEOJSON_FILE):
        print(f"ERROR: {GEOJSON_FILE} not found.")
        print("Run healthsites_ituri_export.py first.")
        return

    with zipfile.ZipFile(OUTPUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(GEOJSON_FILE)
        zf.writestr("LICENSE.txt", LICENSE_TEXT)

    original_kb = os.path.getsize(GEOJSON_FILE) / 1024
    zipped_kb   = os.path.getsize(OUTPUT_ZIP) / 1024

    print(f"Packaged:  {OUTPUT_ZIP}")
    print(f"  GeoJSON : {original_kb:,.0f} KB  →  zip: {zipped_kb:,.0f} KB")
    print(f"  Contains: {GEOJSON_FILE}, LICENSE.txt")


main()
