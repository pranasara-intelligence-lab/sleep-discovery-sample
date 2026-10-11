# Sleep discovery sample — deterministic quality report

Audited all **39 records** on 11 October 2026. This is title/metadata screening only, not semantic, clinical, expert or publisher credibility review. No records were changed or removed.

## Results

| Check | Result |
|---|---|
| Direct title relevance | 39/39 contain sleep, insomnia, circadian, apnea, apnoea or Portuguese sono |
| DOI duplicates | 0/39 duplicate records |
| Normalized-title duplicate groups | 0 across distinct record IDs |
| Source type | 39/39 marked journal-article by Crossref; this does not classify clinical study type |

Query membership counts are counts of unique records per original query; memberships overlap and are retrieval provenance, not reviewed labels.

- `circadian rhythm sleep`: 10/39 records
- `cognitive behavioral therapy insomnia`: 10/39 records
- `insomnia`: 10/39 records
- `obstructive sleep apnea`: 10/39 records

## Field completeness

All 12 allowlisted fields are present in all 39 records. Empty values are reported below; a nonempty field does not imply factual accuracy or completeness.

| Field | Nonempty / 39 | Empty / 39 |
|---|---|---|
| id | 39 | 0 |
| doi | 39 | 0 |
| titles | 39 | 0 |
| author_names | 25 | 14 |
| journal_names | 39 | 0 |
| publisher | 39 | 0 |
| crossref_type | 39 | 0 |
| publication_date_parts | 39 | 0 |
| doi_url | 39 | 0 |
| query_memberships | 39 | 0 |
| source_endpoint | 39 | 0 |
| retrieved_at_utc | 39 | 0 |

## Publication years

Year comes from the first supplied publication_date_parts entry; dates have not been independently verified.

| Year | Records / 39 |
|---|---|
| 1980 | 1 |
| 1991 | 1 |
| 1992 | 1 |
| 1993 | 1 |
| 1994 | 1 |
| 1996 | 2 |
| 1998 | 2 |
| 2002 | 1 |
| 2005 | 2 |
| 2006 | 2 |
| 2007 | 2 |
| 2008 | 1 |
| 2009 | 4 |
| 2010 | 1 |
| 2011 | 2 |
| 2012 | 1 |
| 2016 | 3 |
| 2017 | 1 |
| 2018 | 1 |
| 2019 | 1 |
| 2020 | 4 |
| 2021 | 1 |
| 2022 | 1 |
| 2025 | 2 |

## Records requiring follow-up

Flags are candidates or formatting observations, not confirmed study classifications. Every row remains in the original sample. Multiple flags can apply to one record. There are 2 candidate registry records, 2 titles mentioning animal models and 1 candidate conference abstract.

| Record ID | Flag | Reason |
|---|---|---|
| `doi:10.1016/j.beth.2020.02.002` | title_long | Title length exceeds 150 characters; formatting/repetition merits inspection |
| `doi:10.1016/j.smrv.2022.101693` | title_long | Title length exceeds 150 characters; formatting/repetition merits inspection |
| `doi:10.1055/s-0046-1820556` | title_all_caps | At least 20 alphabetic characters, all uppercase |
| `doi:10.1093/sleep/17.6.551` | title_long | Title length exceeds 150 characters; formatting/repetition merits inspection |
| `doi:10.1093/sleep/2.3.289` | title_animal_model | Title explicitly contains Rat or Canine; not a verified study classification |
| `doi:10.1093/sleep/21.8.847` | title_animal_model | Title explicitly contains Rat or Canine; not a verified study classification |
| `doi:10.1093/sleep/28.1.104` | title_long | Title length exceeds 150 characters; formatting/repetition merits inspection |
| `doi:10.1093/sleepj/zsx050.441` | candidate_conference_abstract | Title starts with numeric conference-style marker 0442; publication type requires verification |
| `doi:10.1093/sleepj/zsx050.441` | title_literal_angle_bracket | Literal angle bracket present; this is not necessarily markup |
| `doi:10.1093/sleepj/zsx050.441` | title_long | Title length exceeds 150 characters; formatting/repetition merits inspection |
| `doi:10.1093/sleepj/zsx050.441` | title_all_caps | At least 20 alphabetic characters, all uppercase |
| `doi:10.31525/ct1-nct03904472` | candidate_registry_record | DOI prefix 10.31525/ct1-; registry identity requires verification |
| `doi:10.31525/ct1-nct04228146` | candidate_registry_record | DOI prefix 10.31525/ct1-; registry identity requires verification |
| `doi:10.5665/sleep/32.4.499` | title_long | Title length exceeds 150 characters; formatting/repetition merits inspection |

The title markup rule detects HTML/XML-like tags; none were found. Literal `<` and `>` in one title are flagged separately. Six titles exceed 150 characters, two are all capitals, and none have leading/trailing or repeated whitespace. These rules do not detect every title defect.

Normalized-title comparison uses HTML unescaping, Unicode NFKC, case folding and Unicode word tokens separated by spaces. It compares titles across different record IDs and does not detect semantic duplicates.

## Integrity and reproducibility

SHA256 before and after the audit are identical:

```text
1db7da5e2d54812b5ce9eee93615f2f8815e6e9d529bc69cd1b2cdabbdf521d3
```

Machine-readable per-record decisions and exact denominators: [quality-report.json](quality-report.json). Re-running the audit replaces only that report.

From this directory:

```sh
python3 audit.py
python3 validate.py
python3 load-sample.py sleep-discovery.jsonl
node fetch-sample.mjs sleep-discovery.jsonl
```

Public download examples (Python standard library, Node >=22, or cURL):

```sh
python3 load-sample.py
node fetch-sample.mjs
sh fetch-sample.sh /tmp/sleep-discovery.jsonl
python3 load-sample.py /tmp/sleep-discovery.jsonl
```

All download examples pin Hugging Face commit `6e62f6614cfebfdb1b319a0f081e24ba46e27f87`. Python and JavaScript verify the known SHA256 before parsing exactly 39 rows. cURL refuses non-HTTPS URLs and redirects and fails on HTTP errors; run the printed validation command afterward. No paid API calls, patient data or API keys are involved.

Local Python/JavaScript loading, the existing validator, and Python/JavaScript/shell syntax checks passed. Network download execution is not claimed by these local checks.

CC0 applies only to this factual metadata compilation, as documented in [RIGHTS_LEDGER.md](RIGHTS_LEDGER.md). No linked article, abstract or full-text rights are granted.
