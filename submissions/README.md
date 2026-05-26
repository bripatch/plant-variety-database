# Submission drafts

Ready-to-paste pitches for external dataset hosts. Both are mirrors of the main GitHub repo; the goal is **discovery + backlinks**, not forking the data.

| File | Target | Status |
|------|--------|--------|
| [`kaggle.md`](kaggle.md) | [kaggle.com/datasets/windrivergreens/plant-variety-database](https://www.kaggle.com/datasets/windrivergreens/plant-variety-database) | ✅ Live (May 26, 2026) |
| [`huggingface-README.md`](huggingface-README.md) | [huggingface.co/datasets/windrivergreens/plant-variety-database](https://huggingface.co/datasets/windrivergreens/plant-variety-database) | ✅ Live (May 26, 2026) |

## Other dataset hosts worth considering

- **data.world** — academic-leaning, allows linking back to source. Free for open data.
- **Zenodo** — assigns a DOI per release; GitHub integration auto-archives tagged releases. Worth doing once for the `v1.0.0` tag so the BibTeX citation has a DOI.
- **Datasets Search (Google)** — automatic if `schema.org/Dataset` JSON-LD is on plants.windrivergreens.com (already shipped). No submission needed.

## Refresh cadence reminder

The GitHub repo auto-refreshes monthly via GitHub Actions (1st @ 08:00 UTC). External mirrors don't sync automatically:

- **Kaggle:** re-upload manually each month (or skip — researchers will follow back to GitHub for latest)
- **Hugging Face:** `git pull` from GitHub → `git push` to HF, or set up an Action

Honestly, the discovery value is in being indexed at all. Monthly mirror updates are a nice-to-have, not a must.
