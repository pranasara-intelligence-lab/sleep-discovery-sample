#!/usr/bin/env python3
"""Fetch a small factual Crossref discovery sample; standard library only."""
import hashlib
import html
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
QUERIES = ["insomnia", "cognitive behavioral therapy insomnia", "circadian rhythm sleep", "obstructive sleep apnea"]


def clean(value):
    return " ".join(html.unescape(re.sub(r"<[^>]*>", "", str(value))).split())


def fetch(url):
    for attempt in range(3):
        try:
            request = Request(url, headers={"User-Agent": "PRANASARA-SleepDiscoverySample/0.1", "Accept": "application/json"})
            with urlopen(request, timeout=30) as response:
                return json.load(response)["message"]["items"]
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** (attempt + 1))


def main():
    records = {}
    requests = []
    for query in QUERIES:
        if requests:
            time.sleep(1)
        url = "https://api.crossref.org/works?" + urlencode({"query": query, "filter": "type:journal-article", "rows": 10})
        items = fetch(url)
        retrieved = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        requests.append({"query": query, "url": url, "retrieved_at_utc": retrieved, "returned_count": len(items)})
        for item in items:
            doi = str(item.get("DOI", "")).strip().lower()
            if not doi:
                raise ValueError("Crossref returned an item without a DOI")
            if doi in records:
                records[doi]["query_memberships"].append(query)
                continue
            records[doi] = {
                "id": "doi:" + doi,
                "doi": doi,
                "titles": [clean(title) for title in item.get("title", [])],
                "author_names": [clean(" ".join(filter(None, [author.get("given"), author.get("family")])) or author.get("name", "")) for author in item.get("author", [])],
                "journal_names": [clean(name) for name in item.get("container-title", [])],
                "publisher": clean(item.get("publisher", "")),
                "crossref_type": item.get("type"),
                "publication_date_parts": item.get("published", item.get("issued", {})).get("date-parts", []),
                "doi_url": "https://doi.org/" + quote(doi, safe="/"),
                "query_memberships": [query],
                "source_endpoint": "https://api.crossref.org/works/" + quote(doi, safe=""),
                "retrieved_at_utc": retrieved,
            }
    rows = [records[doi] for doi in sorted(records)]
    if not 0 < len(rows) <= 40:
        raise ValueError("Sample must contain between 1 and 40 records")
    payload = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode("utf-8")
    manifest = {
        "dataset": "PRANASARA sleep discovery sample",
        "version": "0.1.0",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "requests": requests,
        "record_count": len(rows),
        "dataset_file": "sleep-discovery.jsonl",
        "sha256": hashlib.sha256(payload).hexdigest(),
        "compilation_license": "CC0-1.0",
        "rights_basis": "https://www.crossref.org/documentation/retrieve-metadata/",
        "license_limitations": "CC0 applies to this factual metadata compilation only. No rights to linked articles, abstracts, full text or other excluded content are granted. Query memberships are retrieval provenance, not reviewed topic labels.",
        "review_status": "unreviewed discovery sample; not clinical evidence, a comprehensive corpus, or Apify Actor output",
    }
    # No output is replaced until every remote request and transformation succeeds.
    (ROOT / "sleep-discovery.jsonl").write_bytes(payload)
    (ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(rows), "sha256": manifest["sha256"]}))


if __name__ == "__main__":
    main()
