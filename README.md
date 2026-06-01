# healthsites.io DRC Ebola 2026 — Ituri Facility Data

Health facility data for Ituri Province, DRC, exported from [healthsites.io](https://healthsites.io) in support of the 2026 Ebola outbreak response.

healthsites.io data is currently supporting the active Ebola response in Ituri Province. The INRB-UMIE team is running an open epidemic dashboard at [https://inrb-umie.github.io/EBOV2026_Epidemic_Dashboard/](https://inrb-umie.github.io/EBOV2026_Epidemic_Dashboard/) drawing on the healthsites.io dataset of 3,974 DRC facilities (updated 21 May 2026).

---

## Contents

| File | Description |
|---|---|
| `healthsites_ituri_export.py` | Queries the healthsites.io v3 API and exports all Ituri facilities as GeoJSON |
| `package_ituri_data.py` | Zips the GeoJSON with a LICENSE.txt for distribution |
| `healthsites_ituri_drc.geojson` | Exported facility data (generated — see below) |

---

## Usage

### 1. Register for an API token

Register at [https://healthsites.io/enrollment/form](https://healthsites.io/enrollment/form) using your OpenStreetMap account.

### 2. Install dependencies

```bash
pip install requests
```

### 3. Export the data

```bash
export HEALTHSITES_API_KEY="your_v3_token"
python3 healthsites_ituri_export.py
```

This queries all facilities within the Ituri bounding box:

```
extent=27.0,-3.0,31.5,2.5
```

Covering the province including the active outbreak health zones.

### 4. Package for distribution

```bash
python3 package_ituri_data.py
```

Produces `healthsites_ituri_drc.zip` containing the GeoJSON and `LICENSE.txt`.

---

## Data

- **Source:** [healthsites.io](https://healthsites.io) / OpenStreetMap contributors
- **Licence:** [Open Database Licence (ODbL) 1.0](https://opendatacommons.org/licenses/odbl/)
- **API:** `GET https://healthsites.io/api/v3/facilities/`
- **Docs:** [https://healthsites.io/api/docs/](https://healthsites.io/api/docs/)

### Facility properties (flat-properties=true)

Each GeoJSON feature includes: `osm_id`, `osm_type`, `name`, `amenity`, `healthcare`, `operator`, `operator_type`, `source`, `speciality`, `contact_number`, `operational_status`, `opening_hours`, `beds`, `staff_doctors`, `staff_nurses`, `dispensing`, `completeness`.

---

## Licence

Data: [ODbL 1.0](https://opendatacommons.org/licenses/odbl/)
Code: [FreeBSD Licence](https://www.freebsd.org/copyright/freebsd-license.html)

See [healthsites.io licence page](https://github.com/healthsites/healthsites/wiki/healthsites.io-license) for full terms.
