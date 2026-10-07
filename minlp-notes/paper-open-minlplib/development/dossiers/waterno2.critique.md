# Critique of the waterno2 dossier (`waterno2.md`)

Date: 2026-10-04. Role: independent critic. `R/` means `research-20260929/`.
Nothing under `R/` or `literature/` was edited or executed in place. My two
check scripts and their logs are in
`paper-open-minlplib/development/dossiers/waterno2-critique-checks/`.

## Verdict

**Corrections needed. Nothing invalidates a claimed bound or point.**

- I re-derived Proposition 1, Lemma 2, the folding identity, Theorem 3,
  Lemma 4, Lemma 5 and Lemma 6, including the relaxation inequalities. All
  are correct as stated, apart from the small wording points below.
- I checked Lemma 5 against the period-0 rows and redid its arithmetic
  exactly. The bound E_{0,3} ≤ 5.69762709925 ≤ 5.6976271 holds.
- I recomputed every headline number from the stored files with exact
  arithmetic and found no wrong number. This covers:
  - the duals, primals and gaps;
  - the ratios over the listed duals and the shares of the gap closed;
  - the primal improvements;
  - the μ values and node counts;
  - the listed MINLPLib values in `pages.json`;
  - the leaf-pair counts.
- I read `vbb2.py`'s float propagation and `vbb.solve` and found no
  validity error. In particular, `vbb.solve` reports "infeasible" only after
  root FBBT or root OBBT, both without cutoff.

The main omission is the reproduction track
(`R/publication/reproduction/water-audit/`). It re-ran the authors' full rbb
certification for all five instances, and it replayed 1,564 vbb2 tasks of
certB. The dossier does not mention it, and the replays change two of the
dossier's statements:

1. **The rbb pipeline is not deterministic end to end.** For waterno2_18 and
   waterno2_24, the replay certified slightly lower (still valid) values
   than the claimed ones.
2. **There is much more replay evidence than the 21 runs the dossier
   reports.**

Neither point affects validity. The claimed values rest on the original rbb
run and on the vbb2 recheck at the stored targets.

## 1. Corrections

**C1 (major for the reproducibility text; validity not affected). The
replay statements are incomplete, and the authors' pipeline is not
deterministic.**

*Where:* §0 "Proof status", §3.9 "Replay costs", §6, W1 and W11.

*Problem:* The dossier says the B&B is "deterministic (replayed here bit for
bit on 21 saved runs)". It omits the reproduction track's replays, and one
of them contradicts the dossier's picture.

*Evidence* (`waterno2-critique-checks/logs/replay_audit.log`, read from
`R/publication/reproduction/water-audit/logs/wTT_certify.log`):

- The command `certify.py T logs/mult_TT_w1_impl.json 1 … 3 300000 3600`
  was re-run in a clean checkout for all five instances.
- 06, 09 and 12 reproduce exactly: 263.735099441, 824.834692454 and
  2089.754565439. The per-period rbb node counts are identical too.
- **18 gives 4790.820086219, against the claimed 4790.820715376.** Two
  periods differ:
  - p1: certified −167.636525 with 13,599 nodes, against the stored
    −167.636025419696 with 13,749 nodes;
  - p7: −239.168789 with 12,997 nodes, against −239.16865952038214 with
    13,001 nodes.
- **24 gives 6576.150434342, against the claimed 6576.151388415.** One
  period differs: p14 gives 253.055563 with 82,955 nodes, against the stored
  253.0565166272879 with 83,527 nodes.
- The cause is the target rule. `certify.py` re-derives each target from
  time-limited SCIP runs, and in these three periods SCIP returned different
  incumbents. Given the same target, rbb reproduces the same tree.
- This difference is not documented anywhere in `R/`; a grep for the two
  values finds only the raw logs.
- `R/publication/reproduction/README.md:388–406` says that this command
  "regenerates" the original period certificate. It labels the replay wall
  times (221.25 / 772.61 / 994.20 / 2385.66 / 3210.92 s) as "prior author
  certificate runtime". READINESS line 139 quotes the same numbers.
- In the replay, SCIP's incumbents (feasibility tolerance 1e-6) lie below
  the certified bounds: by 5.0e-4 (18 p1), 3e-5 (18 p7) and 8.5e-4 (24 p14).
  This is not a contradiction. Both rbb and vbb2 certified those bounds (see
  the recheck tables), and the recheck documents tolerance effects of up to
  about 4e-3 (`waterno2-recheck.md` §3, item 4). A careful reader may still
  ask, so the paper should say it.
- The reproduction track also replayed 1,564 vbb2 tasks of certB: 1,008
  records and all 556 leaf checks (`water-audit/data/vrebound_certB_sample.jsonl`).
  All 1,564 are identical to the review's results in status, exact bound and
  node count (my recount).

*Fix:*

- Say that the B&B codes are deterministic for fixed targets and a fixed
  software stack, but that the authors' `certify.py` pipeline is not.
- Report that a full replay of that pipeline reproduced 06, 09 and 12
  exactly and gave valid but weaker values for 18 and 24.
- State that the claimed values rest on the original rbb run and on vbb2 at
  the stored B_t.
- For the paper's reproducibility section, give a replay with the stored
  targets: `run_period.py T t … my_implied_TT.json` for vbb2, or an rbb
  driver that takes B_t as targets.
- Add the 1,564 identical vbb2 replays and the rbb replays to §6 and W1.
- In W11, say that READINESS's times are clean-checkout replay wall times
  (3 workers).
- Add `reproduction/README.md:388–406` to the W5 list.

**C2 (minor). The cost estimates in W1 and W2 should use the larger replay
sample.**

*Where:* §3.9, W1 and W2.

*Problem:* The dossier's 2.4× speed-up comes from 20 tasks. The six path
records dominate that figure, and the review ran them during peak load.
Excluding them, the dossier's own 14 random records ran only 1.25× faster.
The 1,564-task reproduction replay is a better basis: it ran 2.79× faster
on 500 random "rest" records and 300 random leaf checks, and 3.5–4.3× faster
on the early groups.

*Fix:* A full certB re-bounding should take about 214,979 / 2.8 ≈ 77,000 s,
i.e. **about 20–30 CPU-hours on an unloaded machine**. The 60 CPU-hours
figure is the loaded-machine measurement. Two related figures follow:

- W2's exact-propagation option becomes about 60–120 CPU-hours, not 75–240.
- The rbb replay of 09–24 cost 20,822 s of user time (5.8 CPU-hours,
  including SCIP). This is the measured price of re-running the rbb line.

**C3 (minor). The checker estimate in W1 is unsupported.**

*Where:* W1, "Optional strengthening".

*Problem:* The dossier estimates "a checker pass of perhaps 10–20%". Storing
the leaf boxes and dual vectors is not enough. Every node box was shrunk by
FBBT (and the root box by OBBT) before its bound was computed, and a checker
must re-verify those shrinkings to establish the cover. Propagation
dominates the run time: `vbb.py` spends 92% of 66 ms per node there, and
`vbb2.py` takes 18–22 ms per node (`waterno2-recheck.md` §1.2).

*Fix:* Say that the checker cost is uncertain. It could approach the B&B
cost unless each tightening is stored with a short justification, such as
the row that implies it.

**C4 (minor). The SCIP scope statement is inaccurate.**

*Where:* §7.4 and the SCIP item of §9.

*Problem:* The dossier says that all four versions, including master
a01de2c, report wrong values on periods 0, 4 and 5, and that only the cell
pair depends on the seed. In fact, master is wrong on period 0 in 0 of 10
seeds, and every case depends on the seed.

*Evidence:* `R/publication/scip-bug/report.md` §3.2:

- p0: wheel 4/20, master 0/10;
- p4: 10/10 on 10.1.0, 9/10 on master;
- p5: 4/10 on master.

*Fix:* Write "for some random seeds, wrong optimal values on periods 0, 4
and 5 (period 0 not on master in the 10 seeds tried) and on one cell-pair
subproblem". Keep "up to 3.8" for the periods, and add 9.4 for the pair, as
in that report's §7.

**C5 (minor). The row list of Lemma 5 is incomplete.**

*Where:* §3.7.

*Problem:* The proof also uses these rows, which the list omits:

- e50, the second D pump's curve;
- e516, Q_D = x362 + x374 (through the copy x225);
- e81, the fixed demand d_0;
- the monomial rows e900/e901, e924/e925, e1170, e1172 and e1174/e1175.

It also uses the bound x542 ≤ 1.

*Fix:* Complete the list. The proof itself is correct. My exact recheck
gives q ≤ 0.52558379…, Q_D ≤ 1.05116759 and E_{0,3} ≤ 5.69762709925.

**C6 (minor). The per-period margins for waterno2_06 belong to the
superseded wave-2 bound.**

*Where:* §10, item 5, and W9.

*Problem:* The 06 margins (0.127, 2.871, 1.346, 14.083, 0.689, 0.038) sum to
19.153, which is f − 263.735, the wave-2 bound. For certB, the per-period
margins along x*'s cells sum to f − 280.436 = 2.452. The remaining
280.436 − 278.231 = 2.205 is the DP gap between x*'s path and the minimizing
path. So "margins sum exactly to f(x*) − bound" holds only for the
Proposition 1 certificates.

*Fix:* Label the 06 chart as wave 2, or use only 09–24. For certB, show the
pair margins along x*'s cells plus the DP term.

**C7 (minor). The §9 wording contradicts W5.**

*Problem:* §9 says "Each period or pair bound was computed by a rigorous
branch and bound … recomputed by a second …". Leaf-pair bounds were not
computed by B&B.

*Fix:* Write "each period bound and each of the 49,315 pair-box (record)
bounds used by the certificate …; the 79,919 finite leaf-pair bounds follow
by an exact linear correction, and 556 of them were also re-bounded
directly".

**C8 (minor). The W5 list of stale displays is incomplete.**

Add these locations:

- "gap 1.67%" in `R/README.md:43`, `R/open-instances-wave2/waterno2/report.md:9`
  (header) and `R/root-research-log.md:476`;
- "factors of 1.6–6.2" in `R/closing-research-results.md:216`;
- "remaining gaps 4.9–10.8%" in `R/SYNTHESIS.md:408`. The exact gap of
  waterno2_09 is 10.8115%, so 10.8% is not an upper bound;
- `R/publication/reproduction/README.md:388–406` (see C1).

**C9 (minor). The Huang mismatch is inferred, not shown.**

*Where:* §1.1, §7.1 and W6.

*Problem:* "From 3 periods on, Huang's multi-period models differ" assumes
that SCIP 5.0.1's gap-0 value of 215 is correct. This paper itself documents
wrong SCIP optimal values on these models.

*Fix:* Write "Huang's reported 3-period optimum 215 is incompatible with
waterno2_03's listed point of value 115.0045167. Either the models differ
(the dissertation mentions model corrections, p. 129) or the reported value
is wrong. In either case, Huang's numbers cannot be compared." The
recommendation not to compare stands.

**C10 (minor). "Bit for bit" overstates the replay.**

*Where:* §3.9 and W1.

*Problem:* For certified runs, the stored bound equals the target by
construction. The informative matches are therefore the status and the node
count. Determinism also depends on SciPy/HiGHS (SciPy 1.18.0 here), which
the environment line does not record.

*Fix:* Write "identical status, bound and node count", and record the SciPy
version.

**C11 (minor wording).**

- §7.3: "its quadratic-growth and unique-minimizer assumptions fail" should
  read "are not established; the uniform-grid run (223.0) shows that the
  recipe fails at practical cell sizes".
- §3.8: "+∞ only when propagation without cutoff proves the root box empty"
  should read "only when root propagation or root OBBT, both without cutoff,
  proves the root box empty". Emptiness found inside the tree returns the
  target, not +∞.
- §3.5, remark: Theorem 3 with one cell "reproduces" Proposition 1; write
  "is at least as strong as". The value 263.735935 is a float sum of rbb
  bounds and was not separately certified.
- §3.4: Lemma 2 also uses the fixed initial levels s_0 = σ, which are
  variable bounds, not equality rows. Say so in the hypothesis.

## 2. Additional issues and checks

**A1 (positive; strengthens W3). Both B&B model builders agree exactly with
the GAMS text.**

- W3 cross-checked only the reader `osilx.py`. I also compared the
  polynomial rows of `vmodel.poly` (used by vbb/vbb2) and `wmodel.load`
  (used by rbb) with an independent parse of the GAMS text, for every row of
  all five instances. 0 rows differ (`logs/cmp_builders.log`).
- I also checked that the GAMS equation counts are OSIL rows + 1 for all
  five files (the dossier's log shows only 09). All five files minimize
  `objvar`.
- So the chain from the GAMS text to the polynomials of both lines is now
  exact.

**A2 (verified). The listed MINLPLib values and the solved rule are
correct.**

- Every value and date in the §2 table matches `R/bound-audit/pages.json`.
- MINLPLib's documentation confirms the solved rule: at least 3 solvers
  within relative gap 1e-6
  (`literature/papers/vigerske2026-minlplib-documentation-database-snapshot-2026`).
- So 03 (SCIP equal to the primal, LINDO 4.9e-7 away, BARON 2.4e-5 away) and
  04 (only SCIP) are correctly described as unmarked.

**A3 (verified). The model description matches the rows.**

- The data of §1.3 match the period-0 dump: station coefficients, M_S, the
  head rows, the speed and symmetry rows, the virtual-flow rows and the
  balance rows.
- So does the flow-aliasing argument of §4: the root sums −bω/c are
  negative for A and B1, at least 1.95 for B2 and at most 0.032 for D.

**A4 (W1 severity).** For Mathematical Programming Computation, the paper's
reproducibility section must also address C1. Without a fixed-target
replay, a referee who follows the documented command will not regenerate
the stated 18 and 24 values.

## 3. The dossier's own issues, assessed

| item | assessment |
|---|---|
| W1 | Agree on substance. Add C1 to C3 and C10. |
| W2 | Agree. Rescale the cost (C2). |
| W3 | Resolved, and strengthened by A1. |
| W4 | Resolved. Lemma 5 is checked; complete its row list (C5). |
| W5 | Agree. Extend the list (C8), and align §9 with it (C7). |
| W6 | Agree, but soften the Huang inference (C9). |
| W7 | Agree. The binary64 claim checks out: an off station forces ω = fl(ω^min), and fl(ω^min)² falls below the bound fl((ω^min)²) for A, B2 and D. |
| W8 | Resolved. The equation counts and the minimization sense are now checked for all five instances. |
| W9 | The estimate for extending to 09 ("several hundred CPU-hours to reach about 3–5%") has no supporting data for the target gap. Present it as an order-of-magnitude guess or drop it. Relabel the 06 margins (C6). |
| W10 | Agree. Ghaddar et al. 2015 is the most important unread item. |
| W11 | Partly misdiagnosed: READINESS's times come from replays (C1). |
| W12 | Agree, as a necessary-condition check. |
| W13 | Agree. |
| W14 | Agree. No later independent review read the full primal method text. |

## 4. Commands run (targeted; no project-wide checks, no CI)

All runs used scratch copies in `/tmp/wn2crit` and at most one core.

- Exact recomputation of the gaps, ratios, shares, primal improvements, the
  Corollary 8 table and the Lemma 5 arithmetic, from copies of
  `certB_verify.json`, `cert_TT_w1_impl.json` and `waterno2_TT.exact.json`
  (inline Python).
- `python3 cmp_builders.py`: vmodel and wmodel rows against the GAMS text,
  for all five instances (`logs/cmp_builders.log`, seconds).
- `python3 replay_audit.py`: reproduction-track replays against the stored
  certificates (`logs/replay_audit.log`, seconds).
- `grep` and `sed` reads of the sources, reviews, `pages.json`, the
  literature records and the period-0 dump.
