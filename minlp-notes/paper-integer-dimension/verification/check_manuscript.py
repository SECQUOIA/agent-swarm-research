#!/usr/bin/env python3
"""Check manuscript references and review snapshot consistency."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

PAPER = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--snapshot')
args = parser.parse_args()
files = sorted(PAPER.glob('*.tex'))+sorted((PAPER/'sections').glob('*.tex'))
texts = {str(p.relative_to(PAPER)): p.read_text() for p in files}
text = '\n'.join(texts.values())
labels = re.findall(r'\\label\{([^}]+)\}', text)
refs = [key.strip() for group in re.findall(r'\\(?:[Cc]ref|[Cc]refrange|eqref|ref|pageref)\{([^}]+)\}', text) for key in group.split(',')]
refs += re.findall(r'\\[Cc]refrange\{[^}]+\}\{([^}]+)\}', text)
cites = [key.strip() for group in re.findall(r'\\cite\w*\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}', text) for key in group.split(',')]
bibkeys = re.findall(r'@\w+\s*\{\s*([^,]+),', (PAPER/'references.bib').read_text())
report = dict(duplicate_labels=sorted(k for k,v in Counter(labels).items() if v>1),
              unresolved_references=sorted(set(refs)-set(labels)),
              duplicate_bibliography_keys=sorted(k for k,v in Counter(bibkeys).items() if v>1),
              unresolved_citations=sorted(set(cites)-set(bibkeys)),
              tex_files=len(files), labels=len(labels), bibliography_entries=len(bibkeys))
if args.snapshot:
    manifest=json.loads((PAPER/args.snapshot).read_text())
    report['snapshot_mismatches']=[name for name,digest in manifest['files'].items()
                                  if hashlib.sha256((PAPER/name).read_bytes()).hexdigest()!=digest]
print(json.dumps(report, indent=2))
raise SystemExit(int(any(report[k] for k in report if k not in ['tex_files','labels','bibliography_entries'])))
