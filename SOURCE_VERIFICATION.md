# Source verification notes — 11 October 2026

This is a factual follow-up to the [automated quality audit](QUALITY_REPORT.md) of the original 39-record Crossref sample. It does not change a dataset row or its checksum. It is not a clinical evidence review.

| Sample DOI | Source check | Result |
|---|---|---|
| `10.31525/ct1-nct03904472` | [ClinicalTrials.gov NCT03904472](https://clinicaltrials.gov/study/NCT03904472) | The DOI suffix corresponds to an interventional study registration. Registration does not establish published results. |
| `10.31525/ct1-nct04228146` | [ClinicalTrials.gov NCT04228146](https://clinicaltrials.gov/study/NCT04228146) | The DOI suffix corresponds to an interventional study registration. Registration does not establish published results. |
| `10.1093/sleepj/zsx050.441` | [Publisher record](https://academic.oup.com/sleep/article-abstract/40/suppl_1/A164/3781714), [official 2017 abstract supplement](https://sleepmeeting.org/wp-content/uploads/2018/10/abstractbook2017.pdf) | The DOI identifies an item in a conference abstract supplement (pages A164–A165). It should not be treated as a full paper from the generic `journal-article` source type. |
| `10.1093/sleep/21.8.847` | [Publisher issue](https://academic.oup.com/sleep/issue/21/8?browseBy=volume), [PubMed PMID9871947](https://pubmed.ncbi.nlm.nih.gov/9871947/) | The title and source metadata correspond to a canine model study. This join used title/journal/year/pages; our exact DOI PubMed query did not match. |
| `10.1093/sleep/2.3.289` | Original Crossref title | The title mentions a rat. Independent methods verification remains open. |

We checked all **14** empty-author records against PubMed using exact DOI matching. Two had matching PubMed records: [PMID28364452](https://pubmed.ncbi.nlm.nih.gov/28364452/) and [PMID28364466](https://pubmed.ncbi.nlm.nih.gov/28364466/). The other **12** had no exact DOI match in this check. That does not prove their author names are unavailable. The original sample retains the 14 empty author lists; this note does not replace or license source records.

Source links identify where observations came from. No abstracts, article bodies, source author lists, registry descriptions or trial results are republished here. A future curated dataset needs its own inclusion rules, source attribution, rights review and clinical appraisal before any stronger quality claim.
