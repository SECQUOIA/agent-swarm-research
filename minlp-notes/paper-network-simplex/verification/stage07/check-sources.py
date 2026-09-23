"""Check final exposition inputs, references, coverage, and accepted data.

Run from any directory. This checks repository consistency, not mathematical
correctness or bibliographic priority. Stage 6 owns the unchanged code/data.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re


def main():
    paper = Path(__file__).resolve().parents[2]
    root = paper.parent
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    inputs = {}

    def visit(path):
        assert path.is_file(), path
        assert path not in inputs, ('repeated input', path)
        text = path.read_text()
        inputs[path] = text
        for name in re.findall(r'\\input\{([^}]+)\}', text):
            visit(paper/(name if name.endswith('.tex') else name+'.tex'))

    visit(paper/'main.tex')
    source = '\n'.join(inputs.values())
    labels = re.findall(r'\\label\{([^}]+)\}', source)
    assert all(n == 1 for n in Counter(labels).values())
    references = set()
    for group in re.findall(r'\\(?:[cC]ref|eqref|ref)\{([^}]+)\}', source):
        references.update(group.split(','))
    assert references <= set(labels), references-set(labels)
    bibliography = (paper/'references.bib').read_text()
    keys = re.findall(r'@\w+\{([^,]+),', bibliography)
    assert len(keys) == len(set(keys))
    citations = set()
    for group in re.findall(r'\\cite\w*(?:\[[^]]*\])*\{([^}]+)\}', source):
        citations.update(group.split(','))
    assert citations == set(keys), {'missing': citations-set(keys), 'uncited': set(keys)-citations}
    assert r'\author{}' in source
    assert not re.search(r'\b(?:TODO|FIXME|provisional)\b', source, re.I)
    coverage = (paper/'process/coverage.md').read_text()
    assert '| Pending |' not in coverage
    locators = set(re.findall(r'\b(?:sec|subsec|thm|lem|prop|cor|ex|rem|tab|fig):[a-z0-9-]+', coverage))
    assert locators <= set(labels), locators-set(labels)
    readme = (paper/'README.md').read_text()
    links = re.findall(r'\[[^]]*\]\(([^)]+)\)', readme)
    expected_output = paper/'verification/stage07-validation.json'
    for link in links:
        target = paper/link.split('#')[0]
        assert target.exists() or target == expected_output, target

    accepted = paper/'process/snapshots/stage06-accepted'
    unchanged = ['02-compression.tex', '03-structured-oracles.tex',
                 '04-bounded-rank.tex', '05-universality.tex']
    for name in unchanged:
        assert digest(paper/'sections'/name) == digest(accepted/'sections'/name)
    for table in (paper/'tables').glob('08-*.tex'):
        assert digest(table) == digest(accepted/'tables'/table.name)
    stage6 = json.loads((paper/'verification/stage06-validation.json').read_text())
    checked_dependencies = []
    for name, old_digest in stage6['sha256'].items():
        if name.startswith('code/'):
            assert digest(root/name) == old_digest, name
            checked_dependencies.append(name)
    raw = paper/'verification/stage06-benchmarks.json'
    assert digest(raw) == '373ce70b3839c12a206b193e9952d856f585da400f902bda773a725a609f73ac'
    data = json.loads(raw.read_text())
    case = data['optimization'][2]
    assert case['name'] == 'all_labels_global_but_few_per_block'
    expected = {'full': 7215, 'global': 7215, 'initial': 495, 'eliminated': 367}
    for run in case['runs']:
        for method, count in expected.items():
            assert run['measurements'][method]['stats']['variables'] == count
    assert 0.029 <= case['summary']['full']['total_seconds']['median'] <= 0.032
    assert 0.009 <= case['summary']['initial']['total_seconds']['median'] <= 0.012
    result = {'status': 'PASS', 'input_files': len(inputs), 'labels': len(labels),
              'used_reference_labels': len(references), 'bibliography_entries': len(keys),
              'coverage_locators': len(locators), 'README_links': len(links),
              'unchanged_accepted_proof_sections': unchanged,
              'unchanged_production_dependencies': checked_dependencies,
              'accepted_benchmark_and_tables_unchanged': True,
              'accepted_intro_counts_and_rounded_times_checked': True}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'unchanged_production_dependencies'}, indent=2))


if __name__ == '__main__':
    main()
