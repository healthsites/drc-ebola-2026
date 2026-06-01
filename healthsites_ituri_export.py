import os, json, time, requests

API_KEY  = os.environ.get("HEALTHSITES_API_KEY", "YOUR_V3_TOKEN_HERE")
BASE_URL = "https://healthsites.io/api/v3/facilities/"
EXTENT   = "27.0,-3.0,31.5,2.5"

def fetch_page(page):
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
        raise ValueError(f"API returned string: {data}")
    return data

def main():
    features, page = [], 1
    print("Fetching Ituri health facilities (v3 API)...")
    while True:
        data          = fetch_page(page)
        page_features = data.get("features", [])
        if not page_features:
            print(f"  No more results at page {page}. Done.")
            break
        features.extend(page_features)
        print(f"  Page {page}: {len(page_features)} features (total: {len(features)})")
        time.sleep(0.5)
        page += 1

    if not features:
        print("No facilities returned — check your API key and extent.")
        return

    geojson = {
        "type":     "FeatureCollection",
        "name":     "healthsites_ituri_drc",
        "crs":      {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": features
    }
    out = "healthsites_ituri_drc.geojson"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    print(f"\nDone. {len(features)} facilities written to {out}")

main()
