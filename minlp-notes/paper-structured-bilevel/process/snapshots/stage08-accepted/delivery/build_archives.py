"""Export only standalone submission inputs; retain measured file identities."""
from pathlib import Path
import hashlib
import json
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
DELIVERY = PAPER / 'delivery'
DIRECTORIES = (
    'bilevel_bounded_power', 'bilevel_dense_box', 'bilevel_nonconvex',
    'bilevel_one_resource', 'bilevel_parameterized', 'bilevel_reopened',
    'bilevel_response', 'bilevel_vertex_integrity', 'parametric_path_lp',
)
MEASURED = {
    'paper-structured-bilevel/code/compressed_solver.py':
        'paper-structured-bilevel/verification/correction-agent/stage06/measured-compressed-solver.py',
    'paper-structured-bilevel/code/run_experiments.py':
        'paper-structured-bilevel/verification/stage06-author/measured-run-experiments.py',
    'paper-structured-bilevel/code/check_full_task.py':
        'paper-structured-bilevel/verification/stage06-author/measured-check-full-task.py',
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()

def export(stem, files):
    manifest = {name: sha(data) for name, data in sorted(files.items())}
    files['SHA256.json'] = json_bytes(manifest)
    target = PAPER / (stem + '.zip')
    with ZipFile(target, 'w', compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            entry = ZipInfo(stem + '/' + name, date_time=(2026, 9, 9, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    return {'path': target.name, 'files': len(files), 'bytes': target.stat().st_size,
            'sha256': sha(target.read_bytes()), 'content_manifest': manifest}

def main():
    source_paths = [PAPER/'main.tex', PAPER/'references.bib', PAPER/'figures/contacts.pdf']
    source_paths += sorted((PAPER/'sections').glob('*.tex'))
    source_paths += sorted((PAPER/'appendices').glob('*.tex'))
    source_paths += sorted((PAPER/'data').glob('table-*.tex'))
    assert len(source_paths) == 17
    source = {str(p.relative_to(PAPER)): p.read_bytes() for p in source_paths}
    source['README.md'] = (DELIVERY/'README-source.md').read_bytes()

    supplement = {}
    def add(path, name=None):
        path = Path(path)
        key = name or str(path.relative_to(ROOT))
        assert key not in supplement, key
        supplement[key] = path.read_bytes()
    for directory in DIRECTORIES:
        for path in sorted((ROOT/'code'/directory).iterdir()):
            if path.suffix in ('.py', '.json') and path.name != 'verification_summary.json':
                add(path)
    for directory, pattern in [('code', '*.py'), ('data', '*'), ('figures', '*')]:
        for path in sorted((PAPER/directory).glob(pattern)):
            if path.is_file():
                add(path)
    for name in (
        'stage02-author/check_support_recovery.py',
        'stage04-author/check_sharp_modulus.py',
        'stage05-author/run_checks.py',
        'stage05-author/check_padding_and_recovery.py',
    ):
        add(PAPER/'verification'/name)
    for name in MEASURED.values():
        add(ROOT/name)
    author = PAPER/'verification/stage06-author'
    for name in (
        'initial-optional-package-failure.txt', 'experiments-initial-failure.log',
        'experiments-initial-partial.json', 'experiments-resumed.log',
    ):
        add(author/name)
    for path in sorted(author.glob('worker-*.json')):
        add(path)
    for name in (
        'diagnostics.json', 'full-task-checks.json', 'full_task.log',
        'convex_certificates.log', 'review_one.log', 'review_two.log',
        'check_scalar_examples.log',
    ):
        add(author/name, 'paper-structured-bilevel/data/recorded-diagnostics/'+name)

    record_path = 'paper-structured-bilevel/data/stage06-results.json'
    record = json.loads(supplement[record_path])
    mapping = {}
    for current, expected in record['input_hashes'].items():
        measured = MEASURED.get(current, current)
        assert sha(supplement[measured]) == expected, measured
        mapping[current] = {'measured_path': measured, 'measured_sha256': expected,
                            'current_sha256': sha(supplement[current])}
    provenance = {
        'record_path': record_path,
        'record_sha256': sha(supplement[record_path]),
        'input_mapping': mapping,
        'measured_workers': 60,
        'notes': [
            'The three measured source versions are immutable archival copies, not executable entry points at their archival paths.',
            'The current solver adds constraints = tuple(constraints); recorded calls used reusable lists or tuples.',
            'The current driver adds prepared-input archival and output-directory creation outside worker timing.',
            'The current helper adds output-directory creation and iterator regression assertions.',
            'Current-source correctness reruns do not replace or relabel the measured times.',
            'Historical comparator records are retained separately and used different cache and repetition protocols.',
        ],
    }
    supplement['measurement-provenance.json'] = json_bytes(provenance)
    (DELIVERY/'measurement-provenance.json').write_bytes(supplement['measurement-provenance.json'])
    supplement['README.md'] = (DELIVERY/'README-supplement.md').read_bytes()
    supplement['verify_archive.py'] = (DELIVERY/'verify_archive.py').read_bytes()
    supplement['requirements.txt'] = b'sympy==1.14.0\nnumpy==2.5.1\nscipy==1.18.0\nmatplotlib==3.11.1\n'
    artifacts = [export('structured-bilevel-latex-source', source),
                 export('structured-bilevel-computational-supplement', supplement)]
    (DELIVERY/'archive-manifest.json').write_bytes(json_bytes(artifacts))
    for artifact in artifacts:
        print(artifact['path'], artifact['files'], artifact['bytes'], artifact['sha256'])

if __name__ == '__main__':
    main()
