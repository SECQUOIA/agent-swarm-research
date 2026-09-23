from pathlib import Path
import hashlib
import json
import re
import subprocess
import zipfile

EVIDENCE = Path(__file__).resolve().parent
PAPER = EVIDENCE.parent.parent
ROOT = PAPER.parent
DELIVERY = PAPER / 'delivery'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


before = json.loads((EVIDENCE / 'before-delivery-manifest.json').read_text())
current = json.loads((DELIVERY / 'manifest.json').read_text())
changed_inputs = [name for name, old in before['inputs'].items()
                  if digest(ROOT / name) != old]
assert changed_inputs == ['paper-network-simplex/sections/02-compression.tex'], changed_inputs
assert digest(DELIVERY / 'computational-supplement.zip') == before['artifacts']['computational-supplement.zip']['sha256']
assert current['payloads']['computational-supplement.zip'] == before['payloads']['computational-supplement.zip']
for name in ['submission.pdf', 'latex-source.zip', 'computational-supplement.zip', 'manifest.json']:
    assert (DELIVERY / name).read_bytes() == (EVIDENCE / 'rebuild' / name).read_bytes(), name
assert (PAPER / 'main.pdf').read_bytes() == (DELIVERY / 'submission.pdf').read_bytes()
standalone = EVIDENCE / 'standalone/latex-source'
assert (standalone / 'main.pdf').read_bytes() == (DELIVERY / 'submission.pdf').read_bytes()
issues = [line for line in (standalone / 'main.log').read_text().splitlines()
          if re.search(r'Warning:|undefined|Overfull|Underfull|Missing character|^!', line)]
assert not issues, issues
archive_counts = {}
for archive_name, expected in current['payloads'].items():
    with zipfile.ZipFile(DELIVERY / archive_name) as archive:
        top = archive.namelist()[0].split('/')[0]
        payload = {name.removeprefix(top + '/'): archive.read(name) for name in archive.namelist()}
        assert {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()} == expected
        for line in payload['MANIFEST.sha256'].decode().splitlines():
            sha, name = line.split('  ', 1)
            assert hashlib.sha256(payload[name]).hexdigest() == sha
        archive_counts[archive_name] = len(payload)
    assert digest(DELIVERY / archive_name) == current['artifacts'][archive_name]['sha256']
for name, sha in current['inputs'].items():
    assert digest(ROOT / name) == sha, name
for name, metadata in current['artifacts'].items():
    assert digest(DELIVERY / name) == metadata['sha256'], name
    assert (DELIVERY / name).stat().st_size == metadata['bytes'], name

snapshot = EVIDENCE.parent / 'final-round1'
frozen = json.loads((snapshot / 'sha256.json').read_text())
for name, sha in frozen.items():
    assert digest(snapshot / name) == sha, name
formal = re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}[\s\S]*?\\end\{\1\}')
count = 0
for old in (snapshot / 'paper-network-simplex').rglob('*.tex'):
    rel = old.relative_to(snapshot / 'paper-network-simplex')
    new = PAPER / rel
    old_envs = [m.group() for m in formal.finditer(old.read_text())]
    assert old_envs == [m.group() for m in formal.finditer(new.read_text())], str(rel)
    count += len(old_envs)
assert count == 66, count
before_sources = json.loads((EVIDENCE / 'before-source-hashes.json').read_text())
changed_sources = [name for name, sha in before_sources.items() if digest(PAPER / name) != sha]
assert changed_sources == ['sections/02-compression.tex'], changed_sources
assert '\\author{}' in (PAPER / 'main.tex').read_text()

edges = {(a, b) for a in range(1, 5) for b in range(a + 1, 5)}
tree = {(1, 2), (2, 3), (3, 4)}
observed_left = {(1, 3), (1, 4)}
observed_right = observed_left | {(2, 4)}

def cycle_rank(es):
    groups = [{v} for v in range(1, 5)]
    for a, b in es:
        ga = next(g for g in groups if a in g)
        gb = next(g for g in groups if b in g)
        if ga is not gb:
            ga.update(gb)
            groups.remove(gb)
    return len(es) - 4 + len(groups), len(groups)

assert edges - observed_left == tree | {(2, 4)}
assert edges - observed_right == tree
assert cycle_rank(edges - observed_left) == (1, 1)
assert cycle_rank(tree) == (0, 1)
subprocess.run(['git', 'diff', '--check', '--', 'paper-network-simplex'], cwd=ROOT, check=True)
info = subprocess.check_output(['pdfinfo', str(DELIVERY / 'submission.pdf')], text=True)
result = dict(changed_existing_manuscript_sources=changed_sources,
              added_manuscript_source='figures/observation-completion.tex',
              pages=int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1)),
              formal_environments_unchanged=count, frozen_hashes_verified=len(frozen),
              supplement_identical=True, archives_and_manifest_deterministic=True,
              standalone_pdf_identical=True, standalone_diagnostics=issues,
              archive_payload_counts=archive_counts,
              cycle_ranks={'left': 1, 'right': 0}, tree_connected=True,
              before_input_count=len(before['inputs']), changed_preexisting_inputs=changed_inputs,
              anonymous=True, diff_check=True)
(EVIDENCE / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
