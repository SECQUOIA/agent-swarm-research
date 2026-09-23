#!/usr/bin/env python3
"""Build Paper A only and require clean references and zero overfull boxes."""
import json
from pathlib import Path
import sys

PAPER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PAPER / 'verification'))
from build_and_check import build

if __name__ == '__main__':
    result = build('complexity')
    result['passed'] = result['passed'] and result['overfull_boxes'] == 0
    destination = PAPER / 'complexity/build/build-check.json'
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('passed', 'returncode', 'overfull_boxes',
          'errors', 'undefined_references', 'undefined_citations', 'duplicate_labels')}))
    sys.exit(0 if result['passed'] else 1)
