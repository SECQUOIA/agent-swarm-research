#!/usr/bin/env python3
"""Archive a review round's manuscript sources and immutable content hashes."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('round', help='For example stage1-round1 or whole-round1')
args = parser.parse_args()
files = sorted(list((PAPER/'sections').glob('*.tex')) + list(PAPER.glob('*.tex')) + [PAPER/'references.bib', PAPER/'coverage.md'])
missing = [str(p) for p in files if not p.exists()]
if missing:
    parser.error('Missing review inputs: '+', '.join(missing))
destination = PAPER/'reviews'/args.round
destination.mkdir(exist_ok=True)
manifest = dict(round=args.round, frozen_utc=datetime.now(timezone.utc).isoformat(), files={
    str(p.relative_to(PAPER)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
manifest_path = destination/'snapshot.json'
if manifest_path.exists():
    parser.error('A snapshot already exists for this round; choose a new round name.')
for path in files:
    destination_file = destination/'source'/path.relative_to(PAPER)
    destination_file.parent.mkdir(parents=True, exist_ok=True)
    destination_file.write_bytes(path.read_bytes())
manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')
print(manifest_path)
