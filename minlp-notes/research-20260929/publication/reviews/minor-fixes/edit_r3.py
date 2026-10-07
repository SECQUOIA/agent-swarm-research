"""Apply only round-3 track fixes; preserve snapshots before each write."""
from pathlib import Path
import hashlib
import json

W = Path(__file__).resolve().parent
P = W.parents[1]
R = P.parent
B = W / 'before-r3'
B.mkdir(exist_ok=True)

def save(f):
    rel = f.relative_to(R).as_posix()
    dest = B / rel.replace('/', '__')
    if not dest.exists():
        dest.write_bytes(f.read_bytes())
    return rel

def write(f, text):
    save(f)
    f.write_text(text)

def replace(f, old, new, count=None):
    text = f.read_text()
    assert old in text, (f, old)
    if count is not None:
        assert text.count(old) == count, (f, old, text.count(old))
    write(f, text.replace(old, new))

# Preserve scientific logs and point files; no scientific code is imported.
protected = {}
for track in ['primal/chain', 'primal/lnts', 'primal/powerflow',
              'primal/water-ann-kan', 'scip-bug', 'audit-ir']:
    for directory in ['logs', 'points']:
        for f in sorted((P / track / directory).rglob('*')):
            if f.is_file():
                protected[f.relative_to(R).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
(W / 'protected-r3.json').write_text(json.dumps(protected, indent=2) + '\n')

f = P / 'scip-bug/report.md'
replace(f, 'For these five examined solutions, the wrong claims are refuted for the exact decimal model and under SCIP\'s tolerance-based feasibility checks; the returned vectors also fail exact binary64 feasibility. This does not refute every scanned claim, including the low claims discussed in Section 6.',
        'Of these five examined solutions, three are refuted wrong claims: pumps_default (1.198), p0 seed 0 (169.9503) and pair2236 seed shift 7 (65.124) lie above exactly feasible witnesses that SCIP itself accepts. tiny2 with default settings returns the correct decimal optimum −1.337, and pair2236 seed 0 returns the low claim 55.689773, which is not refuted (Section 6). All five returned vectors fail exact binary64 feasibility; this was not checked for the other scanned claims.', 1)
replace(f, 'All instrumented cutoffs in Section 5.3 (seeds 8 and 14)',
        'All instrumented cutoffs in Section 5.3', 1)
replace(f, 'Logs: `logs/cli_{master,10.1.0}_fm336_{readsol,default}.log`.',
        'Logs: `logs/cli_{master,10.1.0}_fm336_{readsol,default}.log` (10.0.2/10.0.3 acceptance: `../reviews/scip-bug-r1/rv_runs.log`).', 1)

f = P / 'primal/lnts/report.md'
replace(f, 'Σ w_j cos θ_j = 45/(50h) to be rational, with h > 0 and positive weights w_j.',
        'Σ w_j cos θ_j = 45/(100h) to be rational, with h > 0 and trapezoid weights w = (1/2, 1, …, 1, 1/2).', 1)
replace(f, '- points/lnts{50,100,200,400}_point.json',
        '- logs/review_r2_check.log: round-2 stored-box and old-vector check\n- points/lnts{50,100,200,400}_point.json', 1)
replace(f, 'checked |control| < 1e-110', 'checked \\|control\\| < 1e-110', 1)
replace(P / 'primal/powerflow/report.md', 'Checked ||I − C J(X)||∞',
        'Checked \\|\\|I − C J(X)\\|\\|∞', 1)

f = P / 'audit-ir/report.md'
replace(f, 'This is the coarsest rounding the page display could have applied.',
        'The 10th-digit floor is a conservative choice; it changes no screened pair (Section 1).', 1)
replace(f, "and define the count: 35 with a nonempty fractional part, 38 without that filter, or 46 counting trailing integer zeros.",
        'and define the counts as displayed entries (35 with a nonempty fractional part, 38 without that filter, or 46 counting trailing integer zeros).', 1)

f = P / 'primal/water-ann-kan/report.md'
replace(f, 'but by the same author, independent review r1 later verified',
        'but by the same author. Independent review r1 later verified', 1)
replace(f, 'Use 1.68% for an upward two-decimal percentage display, now measured against an exactly feasible point.',
        'Use 1.68% for an upward two-decimal display; the gap is measured against an exactly feasible point.', 1)
replace(f, '| 3 | Changed waterno2_12 to 6.90% and added assertions against the exact rational percentage gaps. |',
        '| 3 | Changed waterno2_12 to 6.90% and waterno2_06 from 1.67% to 1.68%; added assertions against the exact rational percentage gaps. |', 1)
f = P / 'literature/control/report.md'
replace(f, '| 7 | Corrected the MINOTAUR integration cell. |',
        '| 7 | Corrected the MINOTAUR integration cell. |\n| 9 | Propagated the rigorous lnts gap display from 5.5e-13 to ≤ 5.55e-13 in Sections 1 and 3. |', 1)

f = P / 'primal/chain/report.md'
replace(f, 'The overly rounded decimals 5.072261493982863 (chain50) and 5.068917341793162 (chain200) occur in',
        'The overly rounded decimals 5.072261493982863 (chain50) and 5.068917341793162 (chain200) were used in', 1)
replace(f, 'and `publication/solver-runs/report.prev.md`. The reproduction documents',
        "and `publication/solver-runs/report.prev.md` (chain200's value only in the first two). The reproduction documents", 1)

# Older documents: only the specific display/gap corrections in review item 3.
for rel in ['open-instances-wave2/cops/report.md',
            'reviews/cops-verification/verification-report.md',
            'reviews/closing-audit-a.md',
            'publication/reviews/solver-campaign-review-r1.md']:
    f = R / rel
    replace(f, '5.072261493982863', '5.0722614939828627')
    if '5.068917341793162' in f.read_text():
        replace(f, '5.068917341793162', '5.0689173417931616')
f = R / 'open-instances-wave2/cops/report.md'
replace(f, '| 5.0722614939828627 | 9.4e-15 |', '| 5.0722614939828627 | 9.7e-15 |', 1)
replace(f, '| 5.0689173417931616 | 9.0e-15 |', '| 5.0689173417931616 | 9.4e-15 |', 1)
replace(R / 'reviews/cops-verification/verification-report.md',
        'are 9.4e-15, 9.9e-15, 9.0e-15 and 1.0e-14, as claimed.',
        'are 9.4e-15, 9.9e-15, 9.0e-15 and 1.0e-14, as claimed (against the original binary64 displays).', 1)
for rel in ['reviews/open-instances-verification/verification-report.md',
            'reviews/closing-audit-a.md']:
    replace(R / rel, '0.5545954011663566', '0.5545954011663565')
f = R / 'reviews/open-instances-verification/verification-report.md'
for old, new in [('0.5545770161025291', '0.5545770161025290'),
                 ('0.554577016047626', '0.5545770160476259'),
                 ('0.5545724136452299', '0.5545724136452298')]:
    replace(f, old, new)

f = W / 'FILES-r2.json'
entries = json.loads(f.read_text())
entries.append('primal/water-ann-kan/logs/minor_review_check.log')
write(f, json.dumps(sorted(set(entries)), indent=2) + '\n')
f = W / 'commands-r2.json'
entries = json.loads(f.read_text())
entries.append(dict(entries[0], note='Final strengthened-check rerun; output mtime 2026-10-03 22:54:24, recorded retrospectively from round-2 evidence.'))
write(f, json.dumps(entries, indent=2) + '\n')
f = W / 'response-r2.md'
replace(f, 'Changed waterno2_12 6.89% → 6.90% in the report and integration cell.',
        'Changed waterno2_12 6.89% → 6.90% in the report and integration cell, and waterno2_06 1.67% → 1.68% in the report.', 1)
replace(f, 'The exact per-instance summary gap replacements are listed.',
        'The exact per-instance summary gap replacements are listed. Propagated ≤ 5.55e-13 to literature/control/report.md Sections 1 and 3.', 1)

# record_r3.py regenerates the historical patch with GNU newline markers.
print('Applied assigned report, older-document and historical record corrections.')
