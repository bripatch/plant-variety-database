# Kaggle Dataset Submission

Paste the fields below into [kaggle.com/datasets/new](https://www.kaggle.com/datasets/new) when creating the dataset. Upload the seven CSVs from `data/`.

---

## Title (max 50 chars)

```
Plant Variety Database: 1,972 cultivars × USDA zones
```

## Subtitle (max 80 chars)

```
Cultivar-level seed-catalog data joined with hardiness zones and planting calendars
```

## License

`CC BY 4.0` — Attribution required.

## Tags

Pick from Kaggle's controlled vocabulary (search and click during upload):

- `agriculture`
- `botany`
- `biology`
- `environment`
- `food`
- `gardening` (if available, else fall back to `food`)
- `tabular`
- `csv`
- `exploratory data analysis`
- `data visualization`

## Cover image

Optional but boosts CTR. Use any of these (no rights issues):

- A zone-map screenshot from plants.windrivergreens.com (e.g. `/state/california` shows a USDA-zone choropleth)
- A still of a vegetable variety from the live site (use an actual photo, not DALL-E)
- A schematic showing the join: `varieties` ↔ `planting_calendar` ↔ `zones`

## Description (markdown body)

```markdown
# Plant Variety Database

An open dataset that **joins cultivar-level seed-catalog data with USDA hardiness zones and per-zone monthly planting calendars** — 1,972 varieties × 13 zones × 12 months, fully sourced, CC BY 4.0.

The hero rows aren't the 1,972 varieties (USDA PLANTS already has ~98K species). They're the joins:

- **20,728** variety × zone planting-calendar entries (indoor sow / transplant / direct sow / harvest)
- **21,880** companion-plant pairings with relationship and reason
- **2,327** outbound citations to extension factsheets, breeder pages, and USDA records
- **1,036** USDA FoodData Central nutrition records joined to growable varieties

## Why this dataset

USDA PLANTS gives you species-level taxonomy but no cultivars and no planting calendars. Johnny's Selected Seeds catalog gives you cultivar-level days-to-maturity but no zone-by-zone schedule. NC State Extension gives you growing prose but no structured cultivar database.

**This dataset is the join.** Hand-cleaned variety rows linked to a planting calendar for every USDA zone they grow in, with companion plants, common pests/diseases, and USDA nutrition data per 100g — all in flat CSVs with verifiable source citations.

## Files

| File | Rows | What it is |
|------|------|------------|
| `varieties.csv` | 1,972 | One row per cultivar — name, scientific name, days to harvest, plant size, sun/water/soil, USDA zones, pest/disease |
| `categories.csv` | 30 | Plant category index (tomato, herb, rose, succulent, etc.) |
| `zones.csv` | 13 | USDA hardiness zones 1-13 with temperature ranges, frost dates, growing-season length |
| `planting_calendar.csv` | 20,728 | Variety × zone — when to start indoors, transplant, direct-sow, harvest |
| `companion_plants.csv` | 21,880 | Beneficial and harmful plant pairings with reasons |
| `nutrition.csv` | 1,036 | Per-100g nutrition from USDA FoodData Central |
| `sources.csv` | 2,327 | Outbound citations per variety |

Foreign keys: every `variety_*.csv` row joins back to `varieties.csv` via `variety_id` or `variety_slug`.

## Sample analyses this dataset enables

- **Climate-zone migration modeling** — pair `usda_zone_min`/`max` with future-zone projections to find cultivars going viable/unviable.
- **Companion-planting graph analysis** — 21,880-edge undirected graph with relationship labels, ready for graph-DB ingestion.
- **Nutrition × growability joins** — "which high-vitamin-K leafy greens grow in zone 4?" in one query.
- **Agricultural ML** — clean labeled cultivar data with consistent feature schema.
- **Garden-app data** — drop-in zone-aware planting calendar without re-licensing per source.

## Provenance

Every variety is backed by at least one real data source — no AI-generated plant facts:

- **NC State Extension** — 1,794 varieties (91%): zones, height, light, growth rate
- **Johnny's Selected Seeds** — 939 varieties (48%): cultivar-level days to maturity, spacing, disease resistance
- **USDA PLANTS Database** — 506 varieties (26%): species-level characteristics
- **USDA FoodData Central** — 1,036 nutrition records

92% of varieties (1,822 of 1,972) carry at least one verifiable outbound citation. See `sources.csv`.

## Updates

This dataset is auto-refreshed monthly from the live production database. The GitHub repo at [github.com/bripatch/plant-variety-database](https://github.com/bripatch/plant-variety-database) tracks the latest export; the live interactive version (per-county zone maps for all 50 US states + 13 Canadian provinces, growing guides, troubleshooting trees, companion-plant prose) is at [plants.windrivergreens.com](https://plants.windrivergreens.com).

## License

CC BY 4.0 — free to share, adapt, and build on for any purpose including commercial, with attribution.

**Suggested attribution:** Plant variety data from [Wind River Greens Plant Database](https://plants.windrivergreens.com) (CC BY 4.0).

## Citation

```bibtex
@misc{windrivergreens_plantdb_2026,
  author       = {{Wind River Greens}},
  title        = {Plant Variety Database: A cultivar-level dataset with USDA hardiness zones and per-zone planting calendars},
  year         = {2026},
  version      = {1.0.0},
  url          = {https://github.com/bripatch/plant-variety-database},
  howpublished = {GitHub repository},
  note         = {CC BY 4.0. Live tool: \url{https://plants.windrivergreens.com}}
}
```
```

---

## Notes for submission

- **Visibility:** Public.
- **Collaborators:** None for now.
- **DOI:** Kaggle will not assign one automatically. If you want a DOI later, mirror the same tagged release to Zenodo (free, GitHub-integrated).
- **Discussion:** Enable. Researcher questions about schema/joins are exactly the comments we want.
- **Update cadence:** Re-upload manually each month after the GitHub Actions auto-refresh fires (1st @ 08:00 UTC). Kaggle has no native GitHub sync.
