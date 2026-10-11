#!/usr/bin/env python3
"""Fail closed on schema, provenance, count and checksum errors."""
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse, quote

ROOT = Path(__file__).resolve().parent
QUERIES = {"insomnia", "cognitive behavioral therapy insomnia", "circadian rhythm sleep", "obstructive sleep apnea"}
KEYS = {"id", "doi", "titles", "author_names", "journal_names", "publisher", "crossref_type", "publication_date_parts", "doi_url", "query_memberships", "source_endpoint", "retrieved_at_utc"}


def validate():
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    payload = (ROOT / "sleep-discovery.jsonl").read_bytes()
    rows = [json.loads(line) for line in payload.decode("utf-8").splitlines()]
    assert 0 < len(rows) <= 40
    assert manifest["record_count"] == len(rows)
    assert manifest["sha256"] == hashlib.sha256(payload).hexdigest()
    assert manifest["compilation_license"] == "CC0-1.0"
    assert {request["query"] for request in manifest["requests"]} == QUERIES
    assert len(manifest["requests"]) == 4
    for request in manifest["requests"]:
        parsed = urlparse(request["url"])
        assert parsed.scheme == "https" and parsed.netloc == "api.crossref.org" and parsed.path == "/works"
        assert parse_qs(parsed.query) == {"query": [request["query"]], "filter": ["type:journal-article"], "rows": ["10"]}
        assert 0 <= request["returned_count"] <= 10
    dois = [row["doi"] for row in rows]
    assert len(set(dois)) == len(dois)
    assert dois == sorted(dois)
    for row in rows:
        assert set(row) == KEYS
        assert isinstance(row["doi"], str) and row["doi"].startswith("10.") and row["doi"] == row["doi"].lower()
        assert row["id"] == "doi:" + row["doi"]
        assert row["crossref_type"] == "journal-article"
        assert row["doi_url"] == "https://doi.org/" + quote(row["doi"], safe="/")
        assert row["source_endpoint"] == "https://api.crossref.org/works/" + quote(row["doi"], safe="")
        for key in ("titles", "author_names", "journal_names", "query_memberships"):
            assert isinstance(row[key], list) and all(isinstance(value, str) for value in row[key])
        # Literal inequalities can appear in titles; reject HTML/XML tags only.
        assert all(not re.search(r"</?[A-Za-z][^>]*>", title) for title in row["titles"])
        assert row["query_memberships"] and set(row["query_memberships"]) <= QUERIES
        assert len(row["query_memberships"]) == len(set(row["query_memberships"]))
        assert isinstance(row["publisher"], str)
        assert isinstance(row["publication_date_parts"], list)
        assert all(isinstance(parts, list) and 1 <= len(parts) <= 3 and all(isinstance(number, int) for number in parts) for parts in row["publication_date_parts"])
        assert datetime.fromisoformat(row["retrieved_at_utc"].replace("Z", "+00:00")).utcoffset().total_seconds() == 0
    print("PASS: {} unique DOI records; exact allowlist, provenance and SHA256 verified.".format(len(rows)))


if __name__ == "__main__":
    validate()
