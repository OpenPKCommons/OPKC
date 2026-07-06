# The `output/` directory

This directory holds the combined viral-kinetics dataset produced by the ingestion pipeline. There are two versions of the CSV, and understanding the difference matters:

| File | What it is | Tracked in git? |
| --- | --- | --- |
| `combined_cleaned_data_staged.csv` | The **latest build** from the ingestion pipeline. Regenerated whenever anyone runs `create_schema.py`. Think of it as a draft — it may reflect in-progress changes, experimental studies, or bug fixes that haven't been reviewed yet. | **No** (gitignored) — it lives only on the machine where it was generated. |
| `combined_cleaned_data_published.csv` | The **published** dataset — the version the [openpkcommons.org](https://openpkcommons.org) website reads and serves to the public. | **Yes** — committed to the repo, so the deployment server pulls it on every webhook. |

## The workflow

1. **Regenerate**: Someone runs the ingestion pipeline from the repo root:
   ```
   python3 code/ingest_studies/create_schema.py
   ```
   This writes/overwrites `output/combined_cleaned_data_staged.csv`.

2. **Review** the staged file locally. Load it in a notebook, inspect it, spot-check a few studies. If you want to preview it on the website itself, temporarily point the site at the staged file (or just eyeball the CSV — up to you).

3. **Publish** when you're happy. This is a deliberate, manual step:
   ```
   # From the repo root:
   cp output/combined_cleaned_data_staged.csv output/combined_cleaned_data_published.csv
   ```
   Then commit and push:
   ```
   git add output/combined_cleaned_data_published.csv
   git commit -m "Publish updated dataset"
   git push
   ```
   Once you push to GitLab, the webhook fires and the live website updates.

## FAQ

**Q: The staged file doesn't exist on my machine — where do I get it?**
Run the pipeline (`python3 code/ingest_studies/create_schema.py`). It's gitignored on purpose, so you always generate a fresh one locally.

**Q: I regenerated but my staged file looks weird — did I break the site?**
No. The site reads `_published.csv`, not `_staged.csv`. Nothing changes for the public until you copy staged → published and push.

**Q: Can I just delete `_published.csv` and always use `_staged.csv`?**
No — the website (and the deployment server) is configured to read `_published.csv`. Removing it will break the site.
