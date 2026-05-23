# Plant Variety Database

An open dataset of **1,972 plant varieties** across 30 categories — vegetables, herbs, flowers, fruit trees, ornamentals, and more — with growing requirements, USDA hardiness zones, planting calendars, companion plants, and USDA nutrition data.

Compiled from public extension-service data ([NC State Extension](https://plants.ces.ncsu.edu/), [USDA PLANTS Database](https://plants.usda.gov/), [USDA FoodData Central](https://fdc.nal.usda.gov/)) plus cultivar-level data from [Johnny's Selected Seeds](https://www.johnnyseeds.com/). 92% of varieties carry outbound citations to their original sources.

The full interactive version — variety pages, planting calendars per zone, companion-plant prose, troubleshooting guides, and per-county zone maps for all 50 US states — lives at **[plants.windrivergreens.com](https://plants.windrivergreens.com)**.

## What's in the data

| File | Rows | What it is |
|------|------|------------|
| [`data/varieties.csv`](data/varieties.csv) | 1,972 | One row per cultivar — name, scientific name, days to harvest, plant size, sun/water/soil needs, USDA zones, pest/disease info |
| [`data/categories.csv`](data/categories.csv) | 30 | Plant category index (tomato, herb, rose, succulent, etc.) |
| [`data/zones.csv`](data/zones.csv) | 13 | USDA hardiness zones 1–13 with temperature ranges, frost dates, and growing-season length |
| [`data/planting_calendar.csv`](data/planting_calendar.csv) | 20,728 | Variety × zone: when to start indoors, transplant, direct-sow, and harvest |
| [`data/companion_plants.csv`](data/companion_plants.csv) | 21,880 | Beneficial and harmful plant pairings with reasons |
| [`data/nutrition.csv`](data/nutrition.csv) | 1,036 | Per-100g nutrition (calories, macros, vitamins, minerals) from USDA FoodData Central |
| [`data/sources.csv`](data/sources.csv) | 2,327 | Outbound citations per variety — links to extension factsheets, breeder pages, USDA records |

All files are UTF-8 CSV with a header row, double-quoted escaping for embedded commas/newlines.

## Quick start

```python
import pandas as pd

varieties = pd.read_csv("data/varieties.csv")
calendar  = pd.read_csv("data/planting_calendar.csv")

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
```

See [`examples/queries.py`](examples/queries.py) for more.

## What's NOT in this export

The long-form editorial content stays on the site — growing guides, harvest/storage notes, history, troubleshooting (with HowTo schema), companion-planting prose, succession-planting schedules, and per-cultivar source citations are rendered live at [plants.windrivergreens.com](https://plants.windrivergreens.com). If you want depth on a single variety, link out to it — the URL is in every row.

This dataset is the **structured index**. The site is the depth.

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)

You are free to share, adapt, and build on this data — including for commercial use — **as long as you credit Wind River Greens with a link back to [plants.windrivergreens.com](https://plants.windrivergreens.com)**.

### Suggested attribution

> Plant variety data from [Wind River Greens Plant Database](https://plants.windrivergreens.com) (CC BY 4.0).

### Citation (BibTeX)

For academic use, cite a specific tagged release (each release is an immutable snapshot — see [Releases](https://github.com/bripatch/plant-variety-database/releases)):

```bibtex
@misc{windrivergreens_plantdb_2026,
  author       = {{Wind River Greens}},
  title        = {Plant Variety Database},
  year         = {2026},
  version      = {1.0.0},
  url          = {https://github.com/bripatch/plant-variety-database},
  howpublished = {GitHub repository},
  note         = {CC BY 4.0. Live tool: \url{https://plants.windrivergreens.com}}
}
```

## Sources & verification

Every variety in this dataset is **backed by at least one real data source** — no AI-generated plant facts. Two layers of provenance:

**Per-variety data origin** — the raw feeds that built each variety's record (`source_database` column on `varieties.csv`; most rows combine 2–3 sources):

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

This dataset auto-refreshes from the live production database **monthly** via GitHub Actions. The live site at [plants.windrivergreens.com](https://plants.windrivergreens.com) updates continuously; this snapshot batches changes into a single monthly commit.

For academic use, pin to a specific [tagged release](https://github.com/bripatch/plant-variety-database/releases) — those are immutable. The `main` branch tracks the latest export and will change over time.

## Issues, corrections, contributions

Spot a wrong zone, a misclassified variety, or a missing companion-planting relationship? Open an issue — corrections are very welcome. The data flows back into the live site.

## About

Wind River Greens is a small microgreens farm in Milton, Georgia. The plant database started as a tool to help our customers plan their gardens and grew into one of the larger free, sourced, zone-aware variety databases on the open web. Visit the live tool at [plants.windrivergreens.com](https://plants.windrivergreens.com).
