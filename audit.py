#!/usr/bin/env python3
"""Deterministic title/metadata audit; never a clinical classification."""
import hashlib
import html
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'sleep-discovery.jsonl'
EXPECTED_SHA256 = '1db7da5e2d54812b5ce9eee93615f2f8815e6e9d529bc69cd1b2cdabbdf521d3'
FIELDS = ('id', 'doi', 'titles', 'author_names', 'journal_names', 'publisher', 'crossref_type', 'publication_date_parts', 'doi_url', 'query_memberships', 'source_endpoint', 'retrieved_at_utc')
RELEVANCE = re.compile(r'\b(?:sleep\w*|insomnia|circadian|apnea|apnoea|sono)\b', re.I)


def normalized_title(title):
    text = unicodedata.normalize('NFKC', html.unescape(title)).casefold()
    return ' '.join(re.findall(r'\w+', text))


def main():
    before = DATA.read_bytes()
    digest = hashlib.sha256(before).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError('Pinned sample checksum mismatch; audit aborted')
    rows = [json.loads(line) for line in before.decode('utf-8').splitlines()]
    if len(rows) != 39:
        raise ValueError('Expected exactly 39 records')
    doi_groups, title_groups = defaultdict(set), defaultdict(set)
    years, queries = Counter(), Counter()
    audits = []
    for row in rows:
        ident = row['id']
        doi_groups[row['doi'].casefold()].add(ident)
        titles = row.get('titles', [])
        for title in titles:
            title_groups[normalized_title(title)].add(ident)
        dates = row.get('publication_date_parts', [])
        years[str(dates[0][0]) if dates and dates[0] else 'missing'] += 1
        queries.update(set(row.get('query_memberships', [])))
        flags = []
        if row['doi'].casefold().startswith('10.31525/ct1-'):
            flags.append({'code': 'candidate_registry_record', 'reason': 'DOI prefix 10.31525/ct1-; registry identity requires verification'})
        for title in titles:
            if re.search(r'\b(?:rat|canine)\b', title, re.I):
                flags.append({'code': 'title_animal_model', 'reason': 'Title explicitly contains Rat or Canine; not a verified study classification'})
            if re.match(r'^0442\b', title):
                flags.append({'code': 'candidate_conference_abstract', 'reason': 'Title starts with numeric conference-style marker 0442; publication type requires verification'})
            if re.search(r'</?[A-Za-z][^>]*>', title):
                flags.append({'code': 'title_markup', 'reason': 'HTML/XML-like tag detected'})
            if re.search(r'<|>', title):
                flags.append({'code': 'title_literal_angle_bracket', 'reason': 'Literal angle bracket present; this is not necessarily markup'})
            if len(title) > 150:
                flags.append({'code': 'title_long', 'reason': 'Title length exceeds 150 characters; formatting/repetition merits inspection'})
            if len(re.sub(r'[^A-Za-z]', '', title)) >= 20 and title.upper() == title:
                flags.append({'code': 'title_all_caps', 'reason': 'At least 20 alphabetic characters, all uppercase'})
            if title != title.strip() or re.search(r'\s{2,}', title):
                flags.append({'code': 'title_whitespace', 'reason': 'Leading/trailing or repeated whitespace'})
        evidence = sorted({match.group(0).casefold() for title in titles for match in RELEVANCE.finditer(title)})
        audits.append({'id': ident, 'title_relevance_terms': evidence, 'direct_title_relevance': bool(evidence), 'flags': flags})
    duplicates = lambda groups: [{'value': key, 'record_ids': sorted(ids)} for key, ids in sorted(groups.items()) if len(ids) > 1]
    doi_values = [r['doi'].casefold() for r in rows]
    after = hashlib.sha256(DATA.read_bytes()).hexdigest()
    if digest != after:
        raise RuntimeError('Source changed during audit')
    report = {
        'audit_method': 'deterministic title/metadata rules only; no semantic, clinical, expert or publisher credibility review',
        'record_count': len(rows), 'metric_denominator': '39 records unless explicitly stated otherwise; query memberships may overlap',
        'sha256_before': digest, 'sha256_after': after, 'source_unchanged': True,
        'field_completeness': {field: {'missing_key_count': sum(field not in r for r in rows), 'empty_value_count': sum(field in r and not r[field] for r in rows), 'nonempty_count': sum(bool(r.get(field)) for r in rows)} for field in FIELDS},
        'doi_duplicate_record_count': len(doi_values) - len(set(doi_values)),
        'doi_duplicate_groups': duplicates(doi_groups), 'normalized_title_duplicate_groups': duplicates(title_groups),
        'title_normalization': 'HTML-unescape, Unicode NFKC, casefold, retain Unicode word tokens separated by one space; compare across different record IDs',
        'publication_year_distribution': dict(sorted(years.items())), 'query_membership_counts': dict(sorted(queries.items())),
        'direct_title_relevance_count': sum(r['direct_title_relevance'] for r in audits),
        'flag_record_counts': dict(sorted(Counter(code for r in audits for code in {f['code'] for f in r['flags']}).items())),
        'crossref_type_counts': dict(Counter(r['crossref_type'] for r in rows)),
        'classification_limit': 'Crossref journal-article is a source metadata type, not clinical publication classification. All candidate flags require verification; no records removed.',
        'record_audits': audits,
    }
    (ROOT / 'quality-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('record_count', 'direct_title_relevance_count', 'flag_record_counts', 'source_unchanged')}, indent=2))


if __name__ == '__main__':
    main()
