#!/usr/bin/env python3
"""Prepare the inputs of the paper in a disposable copy of the archive; never download.

    python3 paper-open-minlplib/artifact/prepare_paper_inputs.py

Run it after the setup of Section S7.1 (artifact/README.md): MINLPLIB_OSIL_ROOT holds the
archived OSIL files, and ~/.cache/minlplib/minlplib/osil (with HOME inside the copy) is a link
to that folder.  The script runs the archived prepare_inputs.py of the same copy, which restores
the saved inputs and checks every hash, and then accepts exactly one kind of shortfall: models
of its manifest that the paper does not use (NOT_NEEDED).  It exits with status 0 if and only if
the saved inputs were restored or found intact, the 69 models of the paper are present with the
SHA-256 of the manifest (and, where the number file records one, the same SHA-256 there), and
every missing model is one of NOT_NEEDED.  Standard library only.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
REPRO = ROOT / 'research-20260929/publication/reproduction'
NUMBERS = ROOT / 'paper-open-minlplib/data/numbers.json'
CACHE = '~/.cache/minlplib/minlplib/osil'
PAPER_MODEL_COUNT = 69  # tab:sem-hashes (43) and tab:audit-inputs (26)
# Models of the manifest of prepare_inputs.py that no table, theorem or audit statement of the
# paper uses; the archive does not contain them.
NOT_NEEDED = sorted([
    'alkyl', 'cecil_13', 'elf', 'ex7_3_5', 'ex8_2_1b', 'hda', 'heatexch_spec2',
    'hybriddynamic_fixedcc', 'hybriddynamic_varcc', 'oil', 'rsyn0815m04m', 'rsyn0820m03m',
    'rsyn0830m03m', 'rsyn0830m04m', 'sepasequ_complex', 'sepasequ_convent',
    'squfl010-040persp', 'squfl015-080persp', 'squfl020-040persp', 'squfl020-050persp',
    'squfl025-040persp', 'squfl030-100persp', 'squfl030-150persp',
    'waterno2_02', 'waterno2_03', 'waterno2_04'])


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def fail(message, details=None):
    if details:
        print(details, file=sys.stderr)
    print('FAIL: ' + message)
    return 1


def main():
    osil_root = os.environ.get('MINLPLIB_OSIL_ROOT')
    if not osil_root:
        return fail('MINLPLIB_OSIL_ROOT is not set; run the setup of Section S7.1 first')
    osil_root = Path(osil_root).resolve()
    cache = Path(os.path.expanduser(CACHE)).resolve()
    if cache != osil_root:
        return fail(f'{CACHE} resolves to {cache}, not to MINLPLIB_OSIL_ROOT={osil_root}; '
                    'set HOME inside the working copy and link the cache folder as in Section S7.1')
    # Never import or run anything outside this copy; prepare_inputs.py writes only into it.
    proc = subprocess.run([sys.executable, str(REPRO / 'tools/prepare_inputs.py')], cwd=ROOT,
                          capture_output=True, text=True)
    start = proc.stdout.find('{')
    try:
        report = json.loads(proc.stdout[start:]) if start >= 0 else None
    except json.JSONDecodeError:
        report = None
    if report is None:
        return fail(f'prepare_inputs.py stopped before its report (exit status {proc.returncode}); '
                    'a saved input or a model differs from its recorded hash',
                    proc.stdout + proc.stderr)
    missing = sorted(report['missing_osil'])
    other = [name for name in missing if name not in NOT_NEEDED]
    if other:
        return fail('models needed by the paper are missing: ' + ', '.join(other))
    if not missing and proc.returncode:
        return fail(f'prepare_inputs.py exited with status {proc.returncode}', proc.stderr)
    manifest = json.loads((REPRO / 'inputs/osil-models.json').read_text())
    recorded = {r['name']: r['sha256'] for r in manifest}
    paper = sorted(set(recorded) - set(NOT_NEEDED))
    if len(paper) != PAPER_MODEL_COUNT:
        return fail(f'the manifest names {len(paper)} paper models, not {PAPER_MODEL_COUNT}')
    numbers = json.loads(NUMBERS.read_text())['instances']
    for name, entry in numbers.items():
        stored = entry.get('size', {}).get('osil_sha256')
        if name not in recorded:
            return fail(f'{name} of the number file is not in the manifest')
        if stored and stored != recorded[name]:
            return fail(f'{name}: the number file and the manifest record different SHA-256')
    changed = [name for name in paper if not (osil_root / (name + '.osil')).is_file()
               or sha256(osil_root / (name + '.osil')) != recorded[name]]
    if changed:
        return fail('missing or changed paper models in MINLPLIB_OSIL_ROOT: ' + ', '.join(changed))
    print(json.dumps({'restored_saved_inputs': report['restored'],
                      'verified_osil': report['verified_osil'],
                      'paper_models_verified': len(paper),
                      'not_needed_by_the_paper': missing}, indent=2))
    print(f'PASS: saved inputs intact; all {len(paper)} paper models verified in {osil_root}; '
          f'{len(missing)} manifest models not needed by the paper are absent (listed above)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
