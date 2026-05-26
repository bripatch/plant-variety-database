# Plant Variety Database

An open dataset that **joins cultivar-level seed-catalog data with USDA hardiness zones and per-zone monthly planting calendars** — 1,972 varieties × 13 zones × 12 months, fully sourced, CC BY 4.0.

The hero rows aren't the 1,972 varieties (USDA PLANTS already has ~98K species). They're the joins:

- **20,728** variety × zone planting-calendar entries (indoor sow / transplant / direct sow / harvest windows)
- **21,880** companion-plant pairings with relationship and reason
- **2,327** outbound citations to extension factsheets, breeder pages, and USDA records (92% of varieties carry at least one)
- **1,036** USDA FoodData Central nutrition records joined to growable varieties

The full interactive version — variety pages, planting calendars per zone, companion-plant prose, troubleshooting guides, and per-county zone maps for all 50 US states + 13 Canadian provinces — lives at **[plants.windrivergreens.com](https://plants.windrivergreens.com)**.

## Also available on

| Host | Link |
|------|------|
| GitHub (canonical) | [github.com/bripatch/plant-variety-database](https://github.com/bripatch/plant-variety-database) |
| Kaggle | [kaggle.com/datasets/windrivergreens/plant-variety-database](https://www.kaggle.com/datasets/windrivergreens/plant-variety-database) |

The GitHub repo is canonical and auto-refreshes monthly. Mirrors are kept in sync but may lag by up to a month.

## Why this dataset exists

USDA PLANTS gives you species-level taxonomy but no cultivars and no planting calendars. Johnny's Selected Seeds catalog gives you cultivar-level days-to-maturity but no zone-by-zone schedule and no nutrition. NC State Extension gives you growing prose but no structured cultivar database. Hardiness zone shapefiles give you a map but no variety information.

**This dataset is the join.** 1,972 hand-cleaned variety rows, each linked to a planting calendar for every USDA zone it grows in, with companion plants, common pests and diseases, and (where applicable) USDA nutrition data per 100g — all in flat CSVs with verifiable source citations.

## What's in the data

| File | Rows | What it is |
|------|------|------------|
| [`data/varieties.csv`](data/varieties.csv) | 1,972 | One row per cultivar — name, scientific name, days to harvest, plant size, sun/water/soil needs, USDA zones, pest/disease info |
| [`data/categories.csv`](data/categories.csv) | 30 | Plant category index (tomato, herb, rose, succulent, etc.) |
| [`data/zones.csv`](data/zones.csv) | 13 | USDA hardiness zones 1–13 with temperature ranges, frost dates, growing-season length |
| [`data/planting_calendar.csv`](data/planting_calendar.csv) | 20,728 | Variety × zone — when to start indoors, transplant, direct-sow, harvest |
| [`data/companion_plants.csv`](data/companion_plants.csv) | 21,880 | Beneficial and harmful plant pairings with reasons |
| [`data/nutrition.csv`](data/nutrition.csv) | 1,036 | Per-100g nutrition (calories, macros, vitamins, minerals) from USDA FoodData Central |
| [`data/sources.csv`](data/sources.csv) | 2,327 | Outbound citations per variety — links to extension factsheets, breeder pages, USDA records |

All files are UTF-8 CSV with a header row, double-quoted escaping for embedded commas/newlines. Foreign keys: every `variety_*.csv` row joins back to `varieties.csv` via `variety_id` or `variety_slug`. `planting_calendar.csv` and `nutrition.csv` join to `zones.csv` and FDC respectively.

<details>
<summary><b>Field reference for <code>varieties.csv</code> (click to expand)</b></summary>

| Column | Type | Notes |
|--------|------|-------|
| `id` | integer | Primary key |
| `category` | string | Lowercase slug — joins to `categories.slug` (tomato, herb, rose, …) |
| `name` | string | Display name including cultivar — e.g. `Cherokee Purple Tomato 'Cherokee Purple'` |
| `slug` | string | URL slug — joins to `*.variety_slug` across other files |
| `scientific_name` | string | Genus + species (+ cultivar epithet where known) |
| `description` | string | 1-3 sentence overview |
| `days_to_harvest` | string | Range or value — e.g. `60-80`, `70`, or `null`. Parse with regex when filtering numerically. |
| `days_to_germination` | string | Same shape as `days_to_harvest` |
| `plant_height` | string | Free-form — e.g. `4-6 ft`, `12 in` |
| `plant_spacing` | string | Free-form — e.g. `18-24 in` |
| `sun_requirement` | string | `full_sun`, `partial_sun`, `partial_shade`, `full_shade` |
| `water_requirement` | string | `low`, `medium`, `high` |
| `soil_type` | string | Free-form |
| `soil_ph` | string | Range — e.g. `6.0-7.0` |
| `growing_difficulty` | string | `beginner`, `intermediate`, `advanced` |
| `is_container_friendly` | boolean | `true` / `false` |
| `growing_season` | string | `cool`, `warm`, `year_round` |
| `sowing_method` | string | `direct_sow`, `transplant`, `both` |
| `color`, `size`, `shape`, `flavor_profile` | string | Sensory / appearance fields where applicable |
| `culinary_uses` | string | Free-form, semicolon-separated |
| `is_heirloom`, `is_hybrid` | boolean | Cultivar provenance flags |
| `usda_zone_min`, `usda_zone_max` | integer | Hardy zone range, 1-13 |
| `disease_resistance` | string | Free-form |
| `common_pests`, `common_diseases` | string | Semicolon-separated lists |
| `source_database` | string | Comma-separated list — `nc_state`, `johnnys`, `usda_plants` |
| `url` | string | Permalink to the live variety page on plants.windrivergreens.com |

</details>

## Use cases

A few research adjacencies this dataset enables:

- **Climate-zone migration modeling** — pair `usda_zone_min`/`usda_zone_max` with future-zone projections (e.g. USDA PHZM) to see which cultivars become viable / unviable in a given county over time.
- **Agricultural ML training** — clean, labeled cultivar data with consistent feature schema for taxonomy, growability, and nutrition classification tasks.
- **Garden-app / smart-home / IoT data** — drop-in zone-aware planting calendar without re-licensing per-source data per platform.
- **Nutrition × growability joins** — `nutrition.csv` + `varieties.csv` lets you ask "which high-vitamin-K leafy greens grow in zone 4?" in one query.
- **Companion-planting network analysis** — `companion_plants.csv` is a 21,880-edge undirected graph (with relationship labels) suitable for graph-DB ingestion or polyculture optimization.
- **Education** — pre-cleaned, sourced data for K-12 / undergraduate horticulture and ag-science curricula.

## Quick start

```python
import pandas as pd

varieties = pd.read_csv("data/varieties.csv")
calendar  = pd.read_csv("data/planting_calendar.csv")
nutrition = pd.read_csv("data/nutrition.csv")

# Tomatoes that mature in under 80 days and grow in zone 7
tomatoes_z7 = varieties[
    (varieties.category == "tomato")
    & (varieties.usda_zone_min <= 7)
    & (varieties.usda_zone_max >= 7)
    & (varieties.days_to_harvest.str.extract(r"(\d+)")[0].astype(float) < 80)
]
print(tomatoes_z7[["name", "days_to_harvest", "growing_difficulty"]])

# When to start each variety indoors in zone 6
z6 = calendar[calendar.usda_zone == 6]
print(z6[["variety_slug", "indoor_sow_start", "outdoor_transplant_start"]].head(20))

# High-vitamin-K leafy greens that overwinter in zone 4
leafy_z4 = varieties[varieties.category.isin(["lettuce", "kale", "chard", "spinach", "arugula"])]
high_k = nutrition.merge(leafy_z4, on="variety_slug").query("vitamin_k_mcg > 100 and usda_zone_min <= 4")
print(high_k[["name", "vitamin_k_mcg", "usda_zone_min", "usda_zone_max"]])
```

See [`examples/queries.py`](examples/queries.py) for more.

## What's NOT in this export

This dataset is the **structured index**. Long-form editorial content stays on the site:

- Per-variety growing guides, history, harvest/storage notes
- Troubleshooting trees (with HowTo schema)
- Companion-planting prose narratives
- Succession-planting schedules
- Per-cultivar source citations rendered in context

Every row has a `url` column — link out for depth.

## Sources & verification

Every variety in this dataset is **backed by at least one real data source** — no AI-generated plant facts. Two layers of provenance:

**Per-variety data origin** — the raw feeds that built each variety's record (`source_database` column on `varieties.csv`; most rows combine 2-3 sources):

| Source | Varieties | Contributes |
|--------|-----------|-------------|
| NC State Extension | 1,794 (91%) | Zones, height, light, growth rate, growing guides |
| Johnny's Selected Seeds | 939 (48%) | Cultivar-level days to maturity, spacing, disease resistance |
| USDA PLANTS Database | 506 (26%) | Species-level characteristics |

**Outbound citations** — verifiable links to original factsheets/data per variety (`sources.csv`, 2,327 entries; 1,822 of 1,972 varieties (92%) carry at least one):

| Source type | Distinct varieties |
|-------------|-------------------|
| USDA FoodData Central (nutrition) | 1,036 |
| Breeder pages (Johnny's Selected Seeds) | 799 |
| Extension factsheets (NC State, UGA) | 481 |
| Botanical gardens (Missouri Botanical Garden) | 11 |

## Updates

This dataset auto-refreshes from the live production database **monthly** via GitHub Actions (1st of each month, 08:00 UTC). The live site at [plants.windrivergreens.com](https://plants.windrivergreens.com) updates continuously; this snapshot batches changes into a single monthly commit.

For academic use, pin to a specific [tagged release](https://github.com/bripatch/plant-variety-database/releases) — those are immutable. The `main` branch tracks the latest export and will change over time.

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)

Free to share, adapt, and build on for any purpose — including commercial — **as long as you credit Wind River Greens with a link back to [plants.windrivergreens.com](https://plants.windrivergreens.com)**.

### Suggested attribution

> Plant variety data from [Wind River Greens Plant Database](https://plants.windrivergreens.com) (CC BY 4.0).

### Citation (BibTeX)

For academic use, cite a specific tagged release — each release is an immutable snapshot:

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

## Issues, corrections, contributions

Spot a wrong zone, a misclassified variety, or a missing companion-planting relationship? Open an issue — corrections are very welcome and flow back into the live site.

## About

Wind River Greens is a small microgreens farm in Milton, Georgia. The plant database started as a tool for our customers and grew into one of the larger free, sourced, zone-aware variety datasets on the open web.
