#!/usr/bin/env python3
"""Validate the claim index: artifact hashes, safe relative paths, LaTeX label keys, displayed
values per instance, status labels per instance and per named component, and agreement of the
claim register (sections/I-reproduction.tex) with artifact/RUNS.md.  Standard library only."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

VERIFIED = 'verified by a separately written implementation'
# Register rows whose result is not a numeric display (identified by their first paper label).
NO_NUMERIC_DISPLAY = {'prop:kan-infeasible', 'tab:solvers'}
DISPLAY_KEYS = ('L', 'U', 'gap_abs', 'gap_rel')


def register_labels(text):
    """Paper labels of each row of the register's longtable (first column)."""
    raw = text.split('\\endhead', 1)[1].split('\\end{longtable}', 1)[0]
    rows = [x.strip() for x in re.split(r'\\\\\s*\n', raw) if ' &\n' in x]
    out = []
    for row in rows:
        labels = []
        for group in re.findall(r'\\[Cc]ref\{([^}]+)\}', row.split(' &\n', 1)[0]):
            labels.extend(group.split(','))
        out.append(labels)
    return out


def runs_labels(text):
    """Row numbers and the backticked labels of the 'Labels' field of each block of RUNS.md."""
    out = []
    for m in re.finditer(r'^### R(\d\d)\. .+?\n(.*?)(?=^### |^## |\Z)', text, re.M | re.S):
        # The field runs to the next field; continuation lines are indented.
        f = re.search(r'^- Labels: (.*?)(?=^- |\Z)', m.group(2), re.M | re.S)
        out.append((int(m.group(1)), re.findall(r'`([^`]+)`', f.group(1)) if f else []))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo-root', required=True, type=Path)
    ap.add_argument('--claims', type=Path, help='Defaults to <root>/paper-open-minlplib/artifact/claims.json.')
    a = ap.parse_args()
    root = a.repo_root.resolve()
    path = a.claims or root / 'paper-open-minlplib/artifact/claims.json'
    doc = json.loads(path.read_text())
    labels = set()
    for source in (root / 'paper-open-minlplib').rglob('*.tex'):
        # Ignore commented labels. An escaped percent sign is literal text.
        text = '\n'.join(re.split(r'(?<!\\)%', line, maxsplit=1)[0] for line in source.read_text().splitlines())
        labels.update(re.findall(r'\\label\s*\{([^}]+)\}', text))
    errors = []
    seen = set()
    hashes = {}
    records = 0
    choices = {'proved', VERIFIED, 'computed', 'floating-point output'}
    for entry in doc['claims']:
        cid = entry['claim_id']
        if cid in seen: errors.append(f'{cid}: duplicate claim id')
        seen.add(cid)
        if not entry['artifacts']: errors.append(f'{cid}: no artifacts')
        if entry['verification_label'] not in choices: errors.append(f'{cid}: unknown verification label')
        for label in set(entry.get('paper_labels', []) + [entry['paper_label']]):
            if label not in labels: errors.append(f'{cid}: missing LaTeX label {label}')
        if 'register_row' in entry:
            shown = entry['displayed_values']
            if entry['paper_label'] not in NO_NUMERIC_DISPLAY:
                if not shown: errors.append(f'{cid}: no displayed values')
                for name in entry['instances']:
                    if not any(k in shown.get(name, {}) for k in DISPLAY_KEYS):
                        errors.append(f'{cid}: no displayed value for {name}')
            words = entry.get('status_by_instance', {})
            by_instance = entry.get('verification_label_by_instance', {})
            if set(words) != set(entry['instances']) or set(by_instance) != set(entry['instances']):
                errors.append(f'{cid}: status per instance does not cover the instances')
            for name, label in by_instance.items():
                if label == VERIFIED and words.get(name) != 'verified':
                    errors.append(f'{cid}: {name} is labelled verified but its status is {words.get(name)}')
            by_component = entry.get('verification_label_by_component', {})
            if set(by_component) != set(entry.get('status_by_component', {})):
                errors.append(f'{cid}: status per component and its labels differ')
            if entry['verification_label'] == VERIFIED and (
                    any(v != VERIFIED for v in list(by_instance.values()) + list(by_component.values()))
                    or not entry['status'].startswith('verified')):
                errors.append(f'{cid}: row labelled verified, but an instance, a component or the row status is weaker')
        for item in entry['artifacts']:
            records += 1
            rel = Path(item['path'])
            if rel.is_absolute() or '..' in rel.parts:
                errors.append(f'{cid}: path must stay relative to repository root: {rel}')
                continue
            target = root / rel
            if not target.resolve().is_relative_to(root):
                errors.append(f'{cid}: path resolves outside repository: {rel}')
                continue
            if not target.is_file():
                errors.append(f'{cid}: missing artifact {rel}')
                continue
            if item['path'] not in hashes:
                sha = hashlib.sha256()
                with target.open('rb') as stream:
                    for chunk in iter(lambda: stream.read(1024*1024), b''): sha.update(chunk)
                hashes[item['path']] = sha.hexdigest()
            if hashes[item['path']] != item['sha256']:
                errors.append(f'{cid}: SHA-256 mismatch {rel}')
    if doc['claim_count'] != len(seen): errors.append('claim_count does not match unique entries')
    registered = {e['register_row']: e for e in doc['claims'] if 'register_row' in e}
    if sorted(registered) != list(range(1, doc['register_row_count'] + 1)):
        errors.append('register rows are missing or repeated')
    register = register_labels((root / doc['register_file']).read_text())
    runs = runs_labels((root / doc['runs_file']).read_text())
    if [n for n, _ in runs] != list(range(1, len(register) + 1)):
        errors.append(f'RUNS.md has rows {[n for n, _ in runs]}, the register {len(register)} rows')
    for (n, run), reg in zip(runs, register):
        if run != reg: errors.append(f'row {n}: labels {reg} in the register, {run} in RUNS.md')
        if n in registered and registered[n]['paper_labels'] != reg:
            errors.append(f'register-{n:02d}: index labels differ from the register')
    if len(register) != doc['register_row_count']: errors.append('register_row_count differs from the register')
    numbers = json.loads((root / doc['numbers_file']).read_text())
    mapped = [e['numbers_key'] for e in doc['claims'] if 'numbers_key' in e]
    expected = [f'claims_table[{i}]' for i in range(len(numbers['claims_table']))]
    if sorted(mapped) != sorted(expected): errors.append('reported-value claims are missing or repeated')
    if errors:
        for error in errors: print('ERROR:', error, file=sys.stderr)
        print(f'FAIL: {len(errors)} errors; {len(seen)} claims; {len(hashes)} files checked')
        return 1
    print(f'PASS: {len(seen)} claims; {records} SHA-256 references; {len(hashes)} distinct files; '
          'all paths, LaTeX labels, displayed values, status labels and register rows valid')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
