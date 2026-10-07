"""Write exact integration replacements; read but never modify target documents."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent
R = W.parents[2]
P = R/'publication'
items = []


def add(target, old, new, reason):
    assert old in (R/target).read_text(), (target,old)
    items.append(dict(target=target,old=old,new=new,reason=reason))


target = 'open-instances-summary.md'
text = (R/target).read_text()
cells = {
    'lnts50': [(4,'5.79e-13')],
    'lnts100': [(3,'0.5545954011670'),(4,'6.12e-13')],
    'lnts200': [(4,'5.84e-13')],
    'lnts400': [(4,'5.88e-13')],
    'dtoc5': [(3,'5.389672119181141')],
    'chain50–400': [(3,'exact-point objectives within 1.01e-14 of the duals'),(4,'≤ 1.01e-14')],
    'ex6_2_5': [(3,'−70.752077833447705')],
    'powerflow0039p': [(3,'41869.0515113203')],
    'powerflow0039r': [(3,'41869.0515113210')],
    'eg_int_s': [(3,'6.4531031593842275 (exactly feasible)')],
    'eg_disc_s': [(3,'5.7605396164535107 (exactly feasible)')],
    'eg_disc2_s': [(6,'verified on all 1,114,361 leaves under A1/A2; separate outward-rounded interval sample: 10,404 leaves of parts 0 and 2–7')],
    'waterno2_06': [(3,'282.888038 (exactly feasible)'),(4,'1.68% (3.78%; 7.26%)')],
    'waterno2_09': [(3,'914.012 (exactly feasible)'),(4,'10.82%')],
    'waterno2_12': [(3,'2233.821346 (exactly feasible)'),(4,'6.90%')],
    'waterno2_18': [(3,'5023.983 (exactly feasible)'),(4,'4.87%')],
    'waterno2_24': [(3,'6963.795181 (exactly feasible)'),(4,'5.90%')],
    'ann_cumene_tanh': [(2,'**−3386.5403** (wave 3: −4024.495, first rigorous finite dual found for this MINLPLib model; the identical exp twin was closed in floating point)'),(3,'−3379.9823940 (exactly feasible)')],
}
for name, changes in cells.items():
    line = next(s for s in text.splitlines() if s.startswith('| '+name+' |'))
    parts = [s.strip() for s in line.strip('|').split('|')]
    for index,new in changes:
        old = parts[index]
        # Match the whole original row for an unambiguous integration edit.
        updated = parts.copy(); updated[index] = new
        nextline = '| '+' | '.join(updated)+' |'
        items.append(dict(target=target,old=line,new=nextline,reason=f'{name}: column {index+1}, {old} -> {new}'))
        line = nextline; parts = updated

add(target,
    'For lnts50–400, dtoc5, lukvle10, chain50–400 and\npowerflow0030p/0039p/0039r, the primal side is a point feasible to row\nviolations of 1e-20 to 8e-12; closure is measured against its value, and no\nexactly feasible point was constructed.',
    'For lnts50–400, dtoc5, lukvle10, chain50–400 and\npowerflow0030p/0039p/0039r, exactly feasible points have now been constructed\nand independently reviewed in publication/primal/. The gaps use the upper\nends of their objective enclosures. The lnts gap cells use the displayed\nsummary duals; against the certified verifier N·h2 bounds the gaps are at\nmost 5.55e-13. The lukvle10 KKT agreement is numerical and does not prove\nglobal optimality; attributing its remaining gap to the dual requires that\nadditional assumption.', 'Replace the obsolete tolerance-only claim and state gap conventions.')
add(target,
    'Displayed dual bounds are truncated or rounded outward, so each displayed\nvalue is itself a valid bound.',
    'Displayed dual bounds are truncated or rounded outward, so each displayed\nvalue is itself a valid bound. Numeric primal bounds are rounded upward for\nminimization and downward for maximization. A point objective enclosure\ncan give a tighter gap than subtraction of the two displayed bounds.',
    'State display directions and distinguish exact-point gaps from display subtraction.')
add(target,
    '(all\nindependently verified, eg_disc2_s partly by sampling;',
    '(all\nindependently verified, eg_disc2_s on every leaf under A1/A2 with a separate interval sample;',
    'Remove the obsolete eg coverage qualifier.')
add(target,
    'for 13 of them the\nprimal side is only tolerance feasible, see the note below the first\ntable)',
    'exactly feasible primal points now also cover the 13 formerly tolerance-only instances, see the note below the first\ntable)', 'Remove the second stale tolerance-only claim.')

audit = 'bound-audit/audit-report.md'
add(audit,
    '- **Display precision.** Values are shown with at most 10 significant digits\n  and at most 8 decimals, and trailing zeros are dropped.',
    '- **Display precision.** Values are shown with at most 8 decimals; there is\n  no 10-significant-digit limit. Counts refer to displayed entries, not\n  distinct numbers: 35 entries (18 distinct strings) with a nonempty\n  fractional part have 11–17 digits from the first through last nonzero\n  digit; dropping the fractional-part filter gives 38 entries with 11–19\n  digits; counting trailing integer zeros as significant gives 46 entries\n  with 11–20 digits (for example −10000000000.). Trailing fractional zeros\n  are dropped.', 'Correct precision and define all three entry counts.')
add(audit,
    '  - For each listed dual, the **slack** is half a unit in its last shown\n    digit, but never less than half a unit in the 10th significant digit.\n    For the value 0, the slack is 5e-9.',
    '  - For each listed dual, the **slack** is half a unit in its last shown\n    digit, but never less than half a unit in the 10th significant digit.\n    This floor is an explicit conservative choice, not a consequence of a\n    display limit. It changes the slack of 0 of the 158 screened pairs and\n    therefore changes no screened-pair class. It changes 17 display-tie\n    pairs on three instances: fac1, fac2 and waternd_fosspoly0.\n    For the value 0, the slack is 5e-9.', 'Keep the floor with its actual justification and checked effect.')
add(audit,
    '  dated 17 Sep 2013: eniplac (a 6-digit value) and spring (8 digits).',
    '  dated 17 Sep 2013: eniplac (a 6-digit value) and spring (8 digits).\n  The five spring (i-r) solver-point pairs need not be solver errors:\n  display rounding explains their listed conflict, while the underlying\n  stored solver bounds are unknown. The spring SCIP objective difference\n  of about 1e-9 comes from bisection and feasibility tolerance; it is not\n  an independent objective disagreement.', 'Integrate qualified spring wording without changing classes or counts.')

for target in ['open-instances-wave2/cops/report.md','reviews/cops-verification/verification-report.md',
               'reviews/closing-audit-a.md','publication/reviews/solver-campaign-review-r1.md',
               'publication/solver-runs/report.prev.md']:
    for old,new in [('5.072261493982863','5.0722614939828627'),('5.068917341793162','5.0689173417931616')]:
        if old in (R/target).read_text():
            add(target,old,new,'Use a chain dual display below the exact binary64 certificate; apply to every occurrence.')

# Exercise the ordered edits in memory only. This also checks multi-cell rows.
for target in {v['target'] for v in items}:
    current = (R/target).read_text()
    for v in (v for v in items if v['target'] == target):
        assert v['old'] in current, (target,v['reason'])
        current = current.replace(v['old'],v['new'])
(W/'integration-r2.json').write_text(json.dumps(items,indent=2,ensure_ascii=False)+'\n')

out = ['## Exact old → new integration edits (round 2)', '',
       'Apply these ordered edits; the target files were read only. The machine-readable list is [integration-r2.json](integration-r2.json). Each replacement was tested in memory against the current files. All new numeric primal displays are checked in [check_r2.log](check_r2.log).', '']
for target in dict.fromkeys(v['target'] for v in items):
    out += [f'### `{target}`','']
    for v in (v for v in items if v['target'] == target):
        out += [v['reason'],'','Old:','```text',v['old'],'```','New:','```text',v['new'],'```','']
(W/'integration-r2.md').write_text('\n'.join(out))
print('PASS:',len(items),'ordered exact integration replacements; no target file written.')
