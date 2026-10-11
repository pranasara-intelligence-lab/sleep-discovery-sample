---
license: cc0-1.0
pretty_name: PRANASARA Sleep Discovery Sample
tags:
- bibliographic-metadata
- sleep
- discovery
---

# PRANASARA Sleep Discovery Sample

A small, **unreviewed bibliographic discovery sample** retrieved from Crossref. It is not a clinical evidence dataset, comprehensive sleep corpus, validated topic classification, or Apify Actor output. Search relevance can produce noisy or tangential matches. Inclusion does not establish efficacy, reliability or applicability of a study. Titles and journal metadata are reproduced as registered; their quality varies.

Four searches request up to ten journal articles each: `insomnia`, `cognitive behavioral therapy insomnia`, `circadian rhythm sleep`, and `obstructive sleep apnea`. Results are deduplicated by case-insensitive DOI and sorted by DOI. Query memberships mean only that Crossref returned the record for a query. No title filter, manual relevance review, clinical appraisal, inferred evidence rating or generated summary is applied. Exact source request URLs, retrieval dates, record count and checksum are in `manifest.json`.

## Files and use

`sleep-discovery.jsonl` has one JSON object per line. `manifest.json` records collection provenance. `RIGHTS_LEDGER.md` documents reuse limits. Python 3.9+ is sufficient, with no third-party dependencies or paid services.

```sh
python3 fetch.py
python3 validate.py
```

Run these from this directory. Fetching makes sequential requests to the official Crossref REST API, at least one second apart, with 30-second timeouts and at most two retries per request. Network failure raises an error; no synthetic fallback is written. A later fetch changes the dataset and manifest because search results and retrieval timestamps change.

Load locally:

```python
import json
from pathlib import Path

records = [json.loads(line) for line in Path("sleep-discovery.jsonl").read_text(encoding="utf-8").splitlines()]
for record in records[:3]:
    print(record["doi"], record["titles"], record["query_memberships"])
```

## Quality audit and pinned developer examples

The [quality report](QUALITY_REPORT.md) audits all 39 records with reproducible metadata/title rules. There are no duplicate DOIs or normalized-title groups; **14 records have empty author lists**. Two registry candidates, two animal-title mentions and one conference-abstract candidate require verification. These are provisional flags, not clinical classifications. Original records remain unchanged. Per-record findings are in [quality-report.json](quality-report.json); reproduce them with `python3 audit.py`.

Load the pinned public release with its known SHA256 verified before parsing:

```sh
python3 load-sample.py
node fetch-sample.mjs
```

Python uses only its standard library; JavaScript requires Node >=22. Both also accept a local JSONL path for offline verification. For cURL, run `sh fetch-sample.sh /tmp/sleep-discovery.jsonl`, then `python3 load-sample.py /tmp/sleep-discovery.jsonl`. These examples use no API keys or paid calls. The pinned download remains the original 39-record release; a future collection requires its own audit and checksum.

## Field definitions

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable `doi:` identifier using lowercased DOI. |
| `doi` | string | Lowercased registered DOI. |
| `titles` | array of strings | Registered titles, markup stripped and whitespace normalized; empty if absent. Literal comparison symbols can remain. |
| `author_names` | array of strings | Registered given/family or organization names. Empty names may reflect incomplete source metadata. |
| `journal_names` | array of strings | Registered container titles. |
| `publisher` | string | Registered publisher; empty if absent. |
| `crossref_type` | string | `journal-article`, selected by the source filter. This is not a clinical study design label. |
| `publication_date_parts` | array of integer arrays | Crossref published date, falling back to issued date; `[year]`, `[year, month]` or `[year, month, day]`. Empty if absent. |
| `doi_url` | string | DOI resolver URL; linked content rights are separate. |
| `query_memberships` | array of strings | Queries that returned this DOI; unreviewed retrieval provenance. |
| `source_endpoint` | string | Canonical individual Crossref metadata lookup endpoint. Actual collection request URLs are in the manifest. |
| `retrieved_at_utc` | string | UTC ISO 8601 timestamp of first retrieval of this DOI. |

Only these fields are retained. Abstracts, article text, references, affiliations, emails, source license objects and other raw payload fields are excluded. Missing source lists stay empty; missing publisher stays an empty string. No missing factual value is invented.

## Rights and intended use

This generated factual metadata compilation is dedicated under **CC0-1.0**. Crossref describes bibliographic metadata facts as freely reusable in its [retrieval documentation](https://www.crossref.org/documentation/retrieve-metadata/). This designation grants no rights to linked articles, abstracts, full text, illustrations, or other excluded copyrighted content. See the rights ledger for the scope of the dedication.

Use this sample to inspect the schema, prototype DOI discovery and assess whether a future curated product would meet your needs. Clinical validation, deduplication beyond DOI, corrections to source metadata and topic review remain future work. No medical advice or patient-level data is included.
