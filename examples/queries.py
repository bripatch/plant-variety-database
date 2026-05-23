"""
Example queries against the Wind River Greens Plant Variety Database.

Data source: https://plants.windrivergreens.com (CC BY 4.0)

Run: python examples/queries.py
"""

import pandas as pd
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"

varieties = pd.read_csv(DATA / "varieties.csv")
calendar = pd.read_csv(DATA / "planting_calendar.csv")
companions = pd.read_csv(DATA / "companion_plants.csv")
nutrition = pd.read_csv(DATA / "nutrition.csv")


def days_to_int(s):
    """'75-85' -> 80, '60' -> 60, NaN -> NaN. First number wins for ranges."""
    if pd.isna(s):
        return None
    n = pd.Series([s]).str.extract(r"(\d+)")[0]
    return float(n.iloc[0]) if not n.isna().all() else None


# 1. Fast-maturing tomatoes for short-season zones
print("=== Tomatoes ripening in under 70 days, zone 4 compatible ===")
fast_toms = varieties[
    (varieties.category == "tomato")
    & (varieties.usda_zone_min <= 4)
    & (varieties.days_to_harvest.apply(days_to_int) < 70)
]
print(fast_toms[["name", "days_to_harvest", "growing_difficulty"]].to_string(index=False))

# 2. What to start indoors in March if you live in zone 6
print("\n=== Start indoors in March, zone 6 ===")
march_z6 = calendar[
    (calendar.usda_zone == 6)
    & (calendar.indoor_sow_start.fillna("").str.lower().str.startswith("march"))
]
print(march_z6[["variety_slug", "category", "indoor_sow_start", "indoor_sow_end"]].head(20).to_string(index=False))

# 3. Beneficial companions for tomatoes
print("\n=== Beneficial companions for tomatoes ===")
tomato_ids = varieties[varieties.category == "tomato"].id
tom_comps = companions[
    companions.variety_id.isin(tomato_ids) & (companions.relationship == "beneficial")
]
top = tom_comps.companion_name.value_counts().head(10)
print(top.to_string())

# 4. Most vitamin-C rich edibles in the dataset
print("\n=== Top 10 by vitamin C (mg/100g) ===")
top_c = nutrition.merge(varieties[["id", "name", "category"]], left_on="variety_id", right_on="id")
print(top_c.nlargest(10, "vitamin_c_mg")[["name", "category", "vitamin_c_mg"]].to_string(index=False))

# 5. Container-friendly varieties for small spaces
print("\n=== Container-friendly varieties ===")
container = varieties[varieties.is_container_friendly == True]
print(f"{len(container)} container-friendly varieties across {container.category.nunique()} categories")
print(container.category.value_counts().head(10).to_string())
