#!/usr/bin/env python3
"""Create a standalone Paper A source archive from the repository or an extracted archive."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
CODE_NAMES = (
    'certified_envelope', 'certified_envelope_benchmarks', 'check_certified_envelope_review',
    'check_envelope_bregman_review', 'check_envelope_certificate_review',
    'check_goal_flow_certificate_review', 'check_reopened_joint_weighted_review',
    'energy_design_certificate', 'envelope_bregman_bounds', 'envelope_rational_certificates',
    'envelope_socp_checks', 'exact_weighted_cactus', 'goal_flow_certificate',
    'series_parallel_envelope_checks',
)
DATA_NAMES = ('certified_envelope_example', 'envelope_certificate_example',
              'certified_envelope_water_topology_instance', 'certified_envelope_benchmark_results',
              'energy_design_certificate_example', 'exact_weighted_cactus_example')


def sources():
    files = [p for p in (PAPER/'complexity').rglob('*')
             if p.suffix in ('.tex', '.bib') and 'build' not in p.parts]
    files += [PAPER/'verification/build_and_check.py']
    files += [p for p in (PAPER/'verification').glob('check_*.py') if p.name != 'check_coverage.py']
    files += list((PAPER/'reproducibility').glob('*.py'))
    files += list((PAPER/'reproducibility').glob('*.md'))
    files += list((PAPER/'reproducibility').glob('requirements*.txt'))
    files += [ROOT/'code/potential_flow_mpd'/f'{name}.py' for name in CODE_NAMES]
    files += [ROOT/'code/potential_flow_mpd'/f'{name}.json' for name in DATA_NAMES]
    return sorted(set(files))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=PAPER/'dist')
    args = parser.parse_args()
    pdf = PAPER/'complexity/build/main.pdf'
    check = PAPER/'complexity/build/build-check.json'
    if not pdf.is_file() or not check.is_file() or not json.loads(check.read_text())['passed']:
        raise SystemExit('Run reproducibility/build_paper.py successfully before packaging.')
    current = {p.relative_to(PAPER).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in (PAPER/'complexity').rglob('*')
               if p.suffix in ('.tex', '.bib') and 'build' not in p.parts}
    if current != json.loads(check.read_text())['input_sha256']:
        raise SystemExit('Manuscript inputs changed since the clean build; rebuild first.')
    args.output.mkdir(parents=True, exist_ok=True)
    archive = args.output/'potential-flow-paper-a.tar.gz'
    with tempfile.TemporaryDirectory(prefix='potential-flow-package-') as temp:
        target = Path(temp)/'potential-flow-paper-a'
        for source in sources():
            dest = target/source.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
        shutil.copy2(PAPER/'reproducibility/README.md', target/'README.md')
        shutil.copy2(pdf, target/'paper.pdf')
        evidence = target/'evidence'
        evidence.mkdir()
        shutil.copy2(check, evidence/'build-check.json')
        # Final portable replay records contain commands, outputs, and package versions.
        for name in ('exact-replay.json', 'numerical-replay.json'):
            source = PAPER/'reproducibility'/name
            if not source.is_file():
                source = ROOT/'evidence'/name
            if source.is_file():
                shutil.copy2(source, evidence/name)
        manifest = {p.relative_to(target).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted(target.rglob('*')) if p.is_file()}
        (target/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
        with tarfile.open(archive, 'w:gz') as out:
            out.add(target, arcname=target.name)
    shutil.copy2(pdf, args.output/'paper-a.pdf')
    result = {'archive': archive.name, 'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
              'pdf': 'paper-a.pdf', 'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
              'files': manifest}
    (args.output/'package-manifest.json').write_text(json.dumps(result, indent=2)+'\n')
    print(f'Created {archive.name}: {len(manifest)+1} files, including manifest.json')


if __name__ == '__main__':
    main()
