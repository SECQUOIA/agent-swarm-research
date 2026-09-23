"""Portable standard-library stage 5 checks; writes logs and an exact summary."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REFERENCE = HERE.parent / 'reference'


def main():
    if not __debug__:
        raise RuntimeError('Run without -O')
    manifest = json.loads((REFERENCE / 'origin-manifest.json').read_text())
    for name, item in manifest.items():
        actual = hashlib.sha256((REFERENCE / name).read_bytes()).hexdigest()
        if actual != item['sha256']:
            raise RuntimeError(f'Original artifact hash mismatch: {name}')
    scripts = [REFERENCE / name for name in ('check_rounding.py', 'check_rounding_review.py',
               'check_fixed_budget_review.py', 'check_grid_transfer_review.py')]
    scripts.append(HERE / 'check_new_results.py')
    summary = {'original_artifacts_verified':len(manifest), 'checks':[]}
    for script in scripts:
        result = subprocess.run([sys.executable, str(script)], cwd=HERE,
                                text=True, capture_output=True)
        (HERE / (script.stem + '.log')).write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(f'{script.name} failed; see its log')
        summary['checks'].append({'script':script.name, 'output':result.stdout.strip()})
        print(f'PASS {script.name}', flush=True)
    (HERE / 'check-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(f'All stage 5 checks passed; {len(manifest)} original artifact hashes match.')


if __name__ == '__main__':
    main()
