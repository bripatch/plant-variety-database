---
license: cc-by-4.0
language:
- en
pretty_name: Plant Variety Database
size_categories:
- 10K<n<100K
source_datasets:
- original
tags:
- agriculture
- horticulture
- gardening
- botany
- plant-science
- usda
- hardiness-zones
- nutrition
- companion-planting
- tabular
configs:
- config_name: varieties
  data_files: varieties.csv
- config_name: planting_calendar
  data_files: planting_calendar.csv
- config_name: companion_plants
  data_files: companion_plants.csv
- config_name: nutrition
  data_files: nutrition.csv
- config_name: zones
  data_files: zones.csv
- config_name: categories
  data_files: categories.csv
- config_name: sources
  data_files: sources.csv
---

# Plant Variety Database

An open dataset that **joins cultivar-level seed-catalog data with USDA hardiness zones and per-zone monthly planting calendars** — 1,972 varieties × 13 zones × 12 months, fully sourced, CC BY 4.0.

The hero rows aren't the 1,972 varieties (USDA PLANTS already has ~98K species). They're the joins:

- **20,728** variety × zone planting-calendar entries (indoor sow / transplant / direct sow / harvest windows)
- **21,880** companion-plant pairings with relationship and reason
- **2,327** outbound citations to extension factsheets, breeder pages, and USDA records (92% of varieties carry at least one)
- **1,036** USDA FoodData Central nutrition records joined to growable varieties

The full interactive version — variety pages, planting calendars per zone, companion-plant prose, troubleshooting guides, and per-county zone maps for all 50 US states + 13 Canadian provinces — lives at **[plants.windrivergreens.com](https://plants.windrivergreens.com)**.

## Why this dataset exists

USDA PLANTS gives you species-level taxonomy but no cultivars and no planting calendars. Johnny's Selected Seeds catalog gives you cultivar-level days-to-maturity but no zone-by-zone schedule and no nutrition. NC State Extension gives you growing prose but no structured cultivar database. Hardiness zone shapefiles give you a map but no variety information.

**This dataset is the join.** 1,972 hand-cleaned variety rows, each linked to a planting calendar for every USDA zone it grows in, with companion plants, common pests and diseases, and (where applicable) USDA nutrition data per 100g — all in flat CSVs with verifiable source citations.

## Files

| File | Rows | What it is |
|------|------|------------|
| `varieties.csv` | 1,972 | One row per cultivar — name, scientific name, days to harvest, plant size, sun/water/soil needs, USDA zones, pest/disease info |
| `categories.csv` | 30 | Plant category index (tomato, herb, rose, succulent, etc.) |
| `zones.csv` | 13 | USDA hardiness zones 1-13 with temperature ranges, frost dates, growing-season length |
| `planting_calendar.csv` | 20,728 | Variety × zone — when to start indoors, transplant, direct-sow, harvest |
| `companion_plants.csv` | 21,880 | Beneficial and harmful plant pairings with reasons |
| `nutrition.csv` | 1,036 | Per-100g nutrition (calories, macros, vitamins, minerals) from USDA FoodData Central |
| `sources.csv` | 2,327 | Outbound citations per variety |

All files are UTF-8 CSV with a header row. Foreign keys: every `variety_*.csv` row joins back to `varieties.csv` via `variety_id` or `variety_slug`.

## Quick start

```python
from datasets import load_dataset

# Load any single config:
varieties = load_dataset("bripatch/plant-variety-database", "varieties", split="train")
calendar = load_dataset("bripatch/plant-variety-database", "planting_calendar", split="train")

# Tomatoes that mature in under 80 days and grow in zone 7:
import pandas as pd
df = varieties.to_pandas()
tomatoes_z7 = df[
    (df.category == "tomato")
    & (df.usda_zone_min <= 7)
    & (df.usda_zone_max >= 7)
    & (df.days_to_harvest.str.extract(r"(\d+)")[0].astype(float) < 80)
]
```

## Use cases

- **Climate-zone migration modeling** — pair `usda_zone_min`/`usda_zone_max` with future-zone projections (e.g. USDA PHZM) to see which cultivars become viable / unviable in a given county over time.
- **Agricultural ML training** — clean, labeled cultivar data with consistent feature schema for taxonomy, growability, and nutrition classification tasks.
- **Garden-app / smart-home / IoT data** — drop-in zone-aware planting calendar without re-licensing per-source data per platform.
- **Nutrition × growability joins** — `nutrition.csv` + `varieties.csv` lets you ask "which high-vitamin-K leafy greens grow in zone 4?" in one query.
- **Companion-planting network analysis** — `companion_plants.csv` is a 21,880-edge graph with relationship labels.

## Field reference (varieties.csv)

| Column | Type | Notes |
|--------|------|-------|
| `id` | int | Primary key |
| `category` | str | Lowercase slug — joins to `categories.slug` |
| `name` | str | Display name including cultivar |
| `slug` | str | URL slug — joins to `*.variety_slug` |
| `scientific_name` | str | Genus + species (+ cultivar epithet) |
| `days_to_harvest` | str | Range or value — e.g. `60-80`, `70`, or `null`. Parse with regex when filtering numerically. |
| `days_to_germination` | str | Same shape as `days_to_harvest` |
| `plant_height`, `plant_spacing` | str | Free-form imperial — e.g. `4-6 ft`, `18-24 in` |
| `sun_requirement` | str | `full_sun`, `partial_sun`, `partial_shade`, `full_shade` |
| `water_requirement` | str | `low`, `medium`, `high` |
| `soil_ph` | str | Range — e.g. `6.0-7.0` |
| `growing_difficulty` | str | `beginner`, `intermediate`, `advanced` |
| `growing_season` | str | `cool`, `warm`, `year_round` |
| `usda_zone_min`, `usda_zone_max` | int | Hardy zone range, 1-13 |
| `is_heirloom`, `is_hybrid`, `is_container_friendly` | bool | |
| `disease_resistance`, `common_pests`, `common_diseases` | str | Semicolon-separated lists |
| `source_database` | str | Comma-separated — `nc_state`, `johnnys`, `usda_plants` |
| `url` | str | Permalink to the live variety page |

## Sources & verification

Every variety in this dataset is **backed by at least one real data source** — no AI-generated plant facts:

| Source | Varieties | Contributes |
|--------|-----------|-------------|
| NC State Extension | 1,794 (91%) | Zones, height, light, growth rate, growing guides |
| Johnny's Selected Seeds | 939 (48%) | Cultivar-level days to maturity, spacing, disease resistance |
| USDA PLANTS Database | 506 (26%) | Species-level characteristics |
| USDA FoodData Central | 1,036 | Nutrition per 100g |

92% of varieties (1,822 of 1,972) carry at least one verifiable outbound citation in `sources.csv`.

## Updates

Auto-refreshed **monthly** from the live production database via GitHub Actions (1st of each month, 08:00 UTC). The canonical source is the GitHub repo: [github.com/bripatch/plant-variety-database](https://github.com/bripatch/plant-variety-database). This Hugging Face mirror is re-synced on the same cadence.

For reproducible research, pin to a specific tagged release on GitHub — those are immutable. The `main` revision on Hugging Face tracks the latest export and will change over time.

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

Free to share, adapt, and build on for any purpose — including commercial — **as long as you credit Wind River Greens with a link back to [plants.windrivergreens.com](https://plants.windrivergreens.com)**.

## Citation

```bibtex
@misc{windrivergreens_plantdb_2026,
  author       = {{Wind River Greens}},
  title        = {Plant Variety Database: A cultivar-level dataset with USDA hardiness zones and per-zone planting calendars},
  year         = {2026},
  version      = {1.0.0},
  url          = {https://github.com/bripatch/plant-variety-database},
  howpublished = {GitHub repository, Hugging Face mirror},
  note         = {CC BY 4.0. Live tool: \url{https://plants.windrivergreens.com}}
}
```

## Issues, corrections, contributions

Spot a wrong zone, a misclassified variety, or a missing companion-planting relationship? Open an issue on the [GitHub repo](https://github.com/bripatch/plant-variety-database/issues) — corrections flow back into the live site and propagate here on the next monthly refresh.
