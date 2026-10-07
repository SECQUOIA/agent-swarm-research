"""One-time prose and dependency edits for integration review r2; no experiments."""
import hashlib
import json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
P = R / 'publication'


def edit(path, replacements):
    text = path.read_text()
    for old, new in replacements:
        assert old in text, (path, old)
        text = text.replace(old, new)
    path.write_text(text)
    print(path.relative_to(R))


edit(R / 'open-instances-summary.md', [
    ('within 1.2e-6 (camshape100) and 3.8e-5 (lnts50)', 'within 1.3e-6 (camshape100) and 3.9e-5 (lnts50)'),
    ('The wrong claims occur only for\n  some random seeds.', 'Whether a run is wrong depends on the random seed and version:\n  p0 is wrong in 4/10 tried seeds on binary 10.0.2 and 0/10 on master,\n  while p4 is wrong in all 10 tried seeds on both 10.1.0 and GAMS/SCIP 10.0.3.'),
    ('CAMINO’s Gurobi optimality claim is refuted by a feasible point.', "CAMINO's Gurobi 13.0.0 optimality claim is refuted by a feasible point; the data do not record Gurobi's termination status, and the cause is unknown."),
])
edit(R / 'bound-audit/audit-report.md', [
    ('Updated 2026-10-03', 'Updated 2026-10-04; responses to integration reviews r1 and r2 on 2026-10-04'),
    ("exactly feasible witnesses that refute SCIP's seed-dependent wrong\noptimality claims", "exactly feasible witnesses that refute SCIP's wrong optimality claims\n(seed- and version-dependent)"),
])
edit(P / 'literature/control/report.md', [('Martín', 'Martin'), ('within 1.2e-6', 'within 1.3e-6')])
edit(P / 'literature/small/report.md', [
    ('exactly feasible point 6.4531031593842274', 'exactly feasible point 6.4531031593842275'),
    ('exactly feasible point 5.7605396164535106', 'exactly feasible point 5.7605396164535107'),
    ('The paper should state which part of the independent verification is by sampling, unless the separate full recheck has replaced it.', 'Every leaf is certified under A1/A2; 10,404 leaves are also certified without the libm assumption.'),
])
edit(P / 'literature/network/report.md', [
    ('914.012, ours (10.8%)', '914.012, ours (≤ 10.82%)'),
    ('2233.821, ours (6.9%)', '2233.821346, ours (≤ 6.90%)'),
    ('5023.983, ours (4.9%)', '5023.983, ours (≤ 4.90%)'),
    ('6963.795, ours (5.9%)', '6963.795181, ours (≤ 5.90%)'),
])
edit(P / 'eg-recheck/report.md', [
    ('| CPU s |', '| wall s (summed over chunks) |'),
    ('38 chunks, 41,162 s CPU in total', '38 chunks, 41,162 wall s (summed over chunks)'),
])
with (P / 'eg-recheck/report.md').open('a') as f:
    f.write('\nIntegration review r2, issue 4 (2026-10-04): the timing column and its total are wall seconds summed over chunks, measured with time.time(); concurrent sums are not scheduler elapsed time. No full recheck was rerun.\n')
edit(P / 'eg-recheck/summarize.py', [
    ('CPU time {t:.0f}s', 'wall time {t:.0f}s (summed over chunks)'),
    ("{tot['time']:.0f}s CPU in the certification chunks", "{tot['time']:.0f}s wall time summed over certification chunks"),
])
with (P / 'reviews/eg-recheck-review-r1.md').open('a') as f:
    f.write('\nImplementation clarification (2026-10-04, integration review r2 issue 4): the 41,162 s labelled CPU seconds above is wall time summed over chunks (time.time()), with 5,372 s scheduler elapsed wall time; the review findings and stored timing data are unchanged.\n')
edit(P / 'reproduction/README.md', [
    ('12,378 s total CPU', '12,378 s (sum of part wall times; 38 min elapsed)'),
    ("manifest still needs the integrating agent's rebuild after all edits.", 'manifest was rebuilt by this integration implementation task on 2026-10-04 after all covered edits; the default package check passed.'),
    ('zero failures. The saved chunks took about **41,162 CPU s** in total.', 'zero failures. The 38 chunk timing fields sum to about **41,162 s of per-chunk wall time** (time.time()); up to 12 chunks ran concurrently, and the scheduler finished after **5,372 s**.'),
    ('This copies the stored evidence, hides the source trees and original cache,', 'This requires Linux **bwrap (bubblewrap)** and **strace** on PATH. It writes\nto a fresh disposable output directory by default and removes its temporary\nscientific copy on success. It copies the stored evidence, hides the source\ntrees and original cache,'),
    ('| interval sample | derived leaves, saved `sample_{A,B,C}_p{k}.npz` |', '| interval sample | derived leaves, pinned OSIL, `minF_p{k}.npy` for sample C; saved `sample_{A,B,C}_p{k}.npz` |'),
])
readme = P / 'reproduction/README.md'
text = readme.read_text()
anchor = 'Aggregate the recorded parts with `python3 summary.py`'
assert anchor in text
text = text.replace(anchor, "The eg_disc_s display 5.760539610694994 is 2.4e-16 above the certifier's\nbinary64 bound; it is valid because the independent retry review certified\nevery leaf against this exact decimal, under the same A1/A2 assumptions.\nThe eight final disc2_9_p{k}.npz checkpoints are byte-identical by\nconstruction: each records an empty final queue.\n\n" + anchor)
readme.write_text(text)
edit(P / 'reproduction/report.md', [
    ('Some primal closure values are\n   only tolerance feasible.', 'The original closures used tolerance-feasible points; exactly\n   feasible points now cover all 13 (publication/primal/).'),
    ('the required final manifest step for the integrating agent.', 'the final manifest step owned and completed by this integration implementation task on 2026-10-04.'),
    ('**The main `manifest.json` was not rebuilt.** The integrating agent must run\n`rebuild_manifest.py` and the default `check_package.py` after all edits are\nfinal. Passing the selected groups below does not validate manifest hashes.', '**The main `manifest.json` was rebuilt on 2026-10-04 by this integration\nimplementation task**, after all covered edits and the result-map rebuild.\nThe default `check_package.py` passed. The selected-group results below\nare historical; the final default result is recorded in the r2 response.'),
])

# These are source copies, kept local and ignored; their hashes join the tracked manifests.
for family, name, origin in (
        ('network', 'MATPOWER-manual-8.1.txt', 'pdftotext -layout of MATPOWER manual 8.1, https://matpower.org/docs/MATPOWER-manual-8.1.pdf; extracted 2026-10-04'),
        ('control', 'qplib_index.html', 'https://qplib.zib.de/; saved primary page from the r2 licence check')):
    path = P / 'literature' / family / 'sources' / name
    manifest = path.parent / 'MANIFEST.md'
    raw = path.read_bytes()
    with manifest.open('a') as f:
        f.write(f'\n| {name} | {origin} | ' + (f'{len(raw)} | ' if family == 'network' else '') + hashlib.sha256(raw).hexdigest() + ' |\n')

path = P / 'reproduction/files-to-commit.json'
data = json.loads(path.read_text())
manifests = {'MANIFEST.md', 'manifest.tsv'}
removed = []
for key, values in data.items():
    if not isinstance(values, list):
        continue
    keep = []
    for value in values:
        if '/publication/literature/' in value and '/sources/' in value and Path(value).name not in manifests:
            removed.append(value)
        else:
            keep.append(value)
    data[key] = keep
data['note'] += ' Literature reports, checks, logs and source SHA-256 manifests must be committed. Copied literature sources stay local and untracked; the paper data release must not redistribute copyrighted sources.'
data['local_untracked_literature_sources'] = dict(policy='All publication/literature/*/sources/ copies stay local and untracked, except the SHA-256 manifests. Do not redistribute copyrighted sources in the paper data release.', removed_from_commit_dependencies=removed)
data['integration_review_r2_dependencies'] = ['.gitignore', 'research-20260929/publication/READINESS.md', 'research-20260929/publication/integration/', 'research-20260929/bound-audit/audit-report.md', 'research-20260929/open-instances-summary.md']
data['literature_files'] = sorted(str(p.relative_to(R.parent)) for p in (P / 'literature').rglob('*') if p.is_file() and '__pycache__' not in p.parts and ('sources' not in p.parts or p.name in manifests))
path.write_text(json.dumps(data, indent=2) + '\n')
