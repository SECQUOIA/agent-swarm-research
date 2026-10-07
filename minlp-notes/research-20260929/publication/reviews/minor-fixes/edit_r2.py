"""Apply the scoped round-2 prose corrections; reject missing targets."""
from pathlib import Path

P = Path(__file__).resolve().parents[2]


def edit(path, pairs):
    f = P/path
    text = f.read_text()
    for old,new in pairs:
        assert old in text, (path,old)
        text = text.replace(old,new)
    f.write_text(text)


edit('primal/lnts/report.md',[
 ('**Verifier dual:** the full value from reviews/open-instances-verification/verification-report.md at margin 1e-12 (0.5546687649381242, 0.5545954011663566, 0.5545770161025291, 0.5545724137001325).',
  '**Verifier dual:** certified N·h2 at margin 1e-12, shown here rounded down as 0.5546687649381242, 0.5545954011663565, 0.5545770161025290 and 0.5545724137001325. The older review displays for lnts100 and lnts200 were rounded to nearest and lie above N·h2; they are not lower bounds as displayed.'),
 ('The summary\'s "gap after 5.5e-13" holds against the verifier dual. Against the truncated displayed dual, the gap is 5.8e-13 to 6.2e-13.',
  'Against the certified verifier dual, each gap is at most 5.55e-13. Against the summary dual displays, the per-instance upper bounds are 5.79e-13, 6.12e-13, 5.84e-13 and 5.88e-13. The summary\'s 5.5e-13 is rounded to nearest and must be corrected.'),
 ('**Not possible:** a fully rational point. With θ rational and nonzero, cos θ is transcendental (Lindemann–Weierstrass), so an interval existence proof is required.',
  '**No fully rational point exists.** If all θ_j and h were rational, vx_N = 45 would require Σ w_j cos θ_j = 45/(50h) to be rational, with h > 0 and positive weights w_j. Lindemann–Weierstrass makes e^{iα} for distinct algebraic α linearly independent over the algebraic numbers. After grouping equal |θ_j|, every nonzero angle gives a strictly positive coefficient of e^{i|θ_j|}, so rationality forces every θ_j = 0. Then py_N = 0, contradicting py_N = 5. This is the linear-independence argument in independent review r1, item 8. Our construction uses an interval existence proof.'),
 ('The displayed primal values (e.g. 0.5546687649387) remain valid upper bounds.',
  'The summary primal displays for lnts50, lnts200 and lnts400 are valid upper bounds. For lnts100, replace 0.5545954011669 by 0.5545954011670: the old display lies below the exact point objective.'),
 ('The gap of about 5.5e-13 is set by the dual margin, not by the primal point.',
  'The gap to the certified verifier dual is at most 5.55e-13 and is set by the dual margin. Against the summary dual displays, use the four upper bounds in Section 1.'),
 ('- mutation_test.py\n', '- mutation_test.py\n- minor_review_check.py and logs/minor_review_check.log: valid second-step and old-vector checks\n'),
 ('## Commands run (from the agent\'s structured return)',
  'The historical `logs/run_all.stdout` and `logs/lnts_primal_50_100_200_400.json` predate the second-step centre correction; their contraction widths are obsolete. Use `logs/minor_review_check.log` for current widths. The reviewer reran the corrected construction in `../../reviews/minor-fixes-review-r1/scratch-A/lnts_repro/`; a round-2 byte comparison confirms that all four resulting point files equal the stored files. No construction was rerun in round 2.\n\n## Commands run (from the agent\'s structured return)'),
 ('max diff 3.25e-15..3.54e-15', 'max diff approximately 3.25e-15..3.54e-15'),
 ('The remaining gap of about 5.5e-13 (1e-12 relative)', 'The remaining gap of at most 5.55e-13 (about 1e-12 relative)'),
 ('The summary\'s displayed (truncated) duals give gaps of 5.8e-13 to 6.2e-13, slightly above the summary\'s \'5.5e-13\'. The 5.5e-13 figure holds only against the verifier\'s full dual values.',
  'The summary dual displays give upper gaps 5.79e-13, 6.12e-13, 5.84e-13 and 5.88e-13. The 5.55e-13 upper bound applies to certified N·h2 and to the safe verifier displays above.'),
 ('give upper distances 3.25e-15–3.54e-15', 'give distances approximately 3.25e-15–3.54e-15, all below 3.6e-15'),
])
edit('primal/chain/report.md',[
 ('`reviews/cops-verification/verification-report.md` (two tables), and `reviews/closing-audit-a.md`.',
  '`reviews/cops-verification/verification-report.md` (a bullet list and a table), `reviews/closing-audit-a.md`, `publication/reviews/solver-campaign-review-r1.md` and `publication/solver-runs/report.prev.md`. The reproduction documents also show these decimals with a caveat; they are outside this revision\'s edit scope.'),
 ('The main summary table shows the valid compact range "5.06862 … 5.07226".',
  'The main summary table shows the valid compact dual range "5.06862 … 5.07226", but its gap cell must change from ≤ 1.0e-14 to ≤ 1.01e-14.'),
])
edit('primal/dtoc5-lukvle10/report.md',[
 ('# Exactly feasible primal points for dtoc5 and lukvle10 ', '# Exactly feasible primal points for dtoc5 and lukvle10'),
 ('The row violation is 3.48e-15.', 'The maximum row violation of p5 is 3.48e-15.'),
 ('- The claim that the lukvle10 KKT point is a local minimizer is numerical only; no second-order proof was attempted. Validity of the primal value does not depend on it.',
  '- No local or global optimality proof for the lukvle10 KKT point was attempted. Validity of the primal point does not depend on optimality.'),
 ('- dtoc5: the gap is now measured against an exactly feasible point.',
  '- dtoc5: replace the summary primal display 5.38967211918114 by 5.389672119181141. The old decimal remains valid as a dual display but lies below the exact point objective. The gap is now measured against an exactly feasible point.'),
])
edit('primal/powerflow/report.md',[
 ('In 0039r, e363 has slack 6.8e-13 and e386 has slack 2.1e-13, and the next smallest are 4.3e-4, 1.08e-3 and 2.3e-3.',
  'In 0039r, e363 has slack 6.8e-13 and e386 has slack 2.1e-13. The next-smallest inactive slack is 4.3e-4 at e215 in 0030p, 1.08e-3 at e346 in 0039p, and 2.3e-3 at e306 in 0039r.'),
])
edit('primal/water-ann-kan/report.md',[
 ('so none of this has been independently reviewed.', 'independent review r1 later verified the numerical claims with its own code.'),
 ('10.82%, 6.89%, 4.87% and 5.90%', '10.82%, 6.90%, 4.87% and 5.90%'),
])
edit('audit-ir/report.md',[
 ('35 values with a nonempty fractional part show', '35 displayed entries (18 distinct strings) with a nonempty fractional part show'),
 ('there are 38 values with 11–19 digits; counting trailing integer zeros gives 46 with 11–20 digits.',
  'there are 38 displayed entries with 11–19 digits; counting trailing integer zeros as significant (for example in −10000000000.) gives 46 displayed entries with 11–20 digits.'),
 ('None of these values is in a flagged pair; three are in display ties (fac1, fac2, waternd_fosspoly0).',
  'None of these values is in a flagged pair. Values on three instances (fac1, fac2, waternd_fosspoly0) occur in 17 display-tie pairs.\n- The 10th-significant-digit slack floor no longer follows from a display limit. Retain it as an explicit conservative choice: an independent exact check finds that it changes the slack of 0 of the 158 screened pairs, so no screened-pair class changes.'),
])
edit('eg-recheck/report.md',[
 ('  - The reviewer\'s tree-bookkeeping check passed on all 8 parts.',
  '  - The reviewer\'s tree-bookkeeping check passed on all 8 parts. Review r1 also supplied an exact tree-free guillotine proof (`../reviews/eg-recheck-r1/own_cover.py`, `../reviews/eg-recheck-r1/logs/own_cover.log`).'),
])
edit('scip-bug/report.md',[
 ('**Seed-dependent case** (cell pair; claims 55.69 or 65.12): it is a **real error, not a tolerance effect**.',
  '**Seed-dependent case** (cell pair): claims 56.492 and 65.12 are refuted by the exactly feasible witness. The 55.69 claims are not refuted (Section 6).'),
 ('It has the same cause: a strong-branching child on 10.0.2, a tree node on master.',
  'In the instrumented seeds (8 and 14), the same cause was observed: a strong-branching child on 10.0.2, a tree node on master.'),
 ('So no consistent reading of the model makes SCIP\'s answers right. The claims are wrong for the decimal model and wrong under SCIP\'s own tolerance-based notion of feasibility.',
  'For these five examined solutions, the wrong claims are refuted for the exact decimal model and under SCIP\'s tolerance-based feasibility checks; the returned vectors also fail exact binary64 feasibility. This does not refute every scanned claim, including the low claims discussed in Section 6.'),
 ('All traced cutoffs involve the 0.7 station', 'All instrumented cutoffs in Section 5.3 (seeds 8 and 14) involve the 0.7 station'),
 ('| `PROGRESS.json` | state for successors |',
  '| `PROGRESS.json` | state for successors |\n| `minor_review_check.py`, `logs/minor_review_check.log` | raw-log scan recount and exact small-model comparisons |\n| `sources/` | saved issue #162/#190 bodies and comments; provenance and hashes in `sources/MANIFEST.md` |'),
 ('This was checked on master and on 10.1.0 by the author, and on 10.0.2 and 10.0.3 by review r1 (`../reviews/scip-bug-r1/rv_runs.log`).',
  'Witness acceptance was checked on master, 10.1.0, 10.0.2 and 10.0.3.'),
 ('These exact case comparisons are recorded in `logs/minor_review_check.log`.',
  'The inequality follows exactly because 0.8 < ((0.2 + 1.337)/1.6)².'),
 ('Review r1 proposed an untested explanation:', 'One untested explanation is:'),
])

rule = ('The saved master `QuadHandler::addDefaultBounds` rule chooses the smallest finite lower bound m and largest finite upper bound M separately. It sets the lower default to −100|m| and the upper default to 100|M| when the corresponding finite bound is outside the near-zero tolerance; otherwise it uses −1000 or +1000. The 99,997 upper defaults are consistent with the original x50001 = 1 bound giving upper default 100. The 99,983 lower defaults imply 14 additional finite lower bounds, presumably from presolve; their values and the lower default cannot be inferred. Every branch gives a negative lower default. The saved reference point has listed coordinates in [1.460728991e-5, 8.057243524908399] and omitted zero coordinates, so it is contained without knowing that lower default (`checks/dtoc5_reference_check.log`). The exact benchmark revision may differ from master.')
edit('literature/control/report.md',[
 ('The master-source rule in `QuadHandler::addDefaultBounds` scales the largest applicable finite bound magnitude by 100 (or uses ±1000 when none exists). For QPLIB_8585\'s sole finite bound x50001 = 1, this gives [−100, 100]. Re-fetching the QPLIB reference point matched the r2 SHA-256 and confirmed max |x| = 8.057243524908399, within that box (`checks/dtoc5_reference_check.log`). The benchmarked revision v0.4-50-g456fd8cc may differ from the saved master source, so the inference does not prove which default values that run used.', rule),
 ('Saved master source implies [−100, 100] from x50001 = 1, containing the reference point (max |x| = 8.06); the exact benchmark revision may differ.',
  'Saved master source supports upper default 100; the lower default is unknown because 14 extra variables already had finite lower bounds. It is negative under the rule, so the nonnegative reference point (max 8.06) is contained. The benchmark revision may differ.'),
 ('Master source implies [−100, 100] from x50001 = 1, but its log does not state the values and the exact benchmark revision may differ.',
  'Master source supports upper default 100 and a negative lower default of unknown magnitude; the warning counts show 14 extra finite lower bounds. The log does not state the defaults and the exact benchmark revision may differ.'),
 ('explained inference [−100,100], re-fetched the reference point and confirmed its scale 8.06, revision caveat',
  'corrected in round 2 to an upper default 100 and an unknown negative lower default; confirmed saved reference-point containment and the revision caveat'),
 ('at the 2e-10 relative level', 'at about 1.2e-10 for coefficients and 2.5e-10 for bounds'),
 ('constants rounded at about 2e-10', 'coefficients rounded at about 1.2e-10 and bounds at about 2.5e-10'),
 ('\n## Response to review', '\n\n## Response to review'),
])
edit('literature/control/checks/README.md',[
 ('coefficient and bound differences (all <= 2.5e-10).',
  'coefficient and bound differences (bound maximum about 4.7e-10; QPLIB_3177 about 2.5e-10).'),
])
prev = P/'literature/control/report.prev.md'
prev.write_text('> Historical round-0 copy. Superseded by [report.md](report.md); use that report for current claims.\n\n'+prev.read_text())
edit('literature/network/report.md',[
 ('Göß et al. 2026 list', 'Göß 2026 lists'),
 ('tables pp. 42,48,56,59,69,72', 'Table 5, pp. 69 and 72'),
 ('per-instance Table 5, pp. 69 and 72', 'Table 5, pp. 69 and 72'),
 ('Present ours as "the first rigorous certificate"', 'Present ours as "the first rigorous certificate found for this MINLPLib model"'),
 ('https://www.tuhh.de/ti3/jansson/vsdp/', 'https://www.tuhh.de/ti3/jansson/vsdp_cj.html'),
 ('inferred from the Default logs', 'inferred from the checked Default R3_H1_N4.log'),
 ('inferred from Default logs reading only limits/time = 7200', 'inferred from the checked Default R3_H1_N4.log reading only limits/time = 7200'),
 ('as in their Table 4', 'as in arXiv v2 Table 4'),
 ('In the source paper no method converged in 1e5 s', 'In arXiv v2 no method converged in 1e5 s'),
 ('All scripts are in `checks/`, each with a `.log` next to it.',
  'All scripts are in `checks/`, each with a `.log` next to it. `minor_review_check.py` and its log record the saved-source checks added for the minor-fix revision.'),
])
print('Applied round-2 track prose corrections.')
