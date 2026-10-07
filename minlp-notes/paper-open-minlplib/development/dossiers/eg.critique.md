# Critique of dossier `eg.md` (eg_int_s, eg_disc_s, eg_disc2_s)

Date: 2026-10-04. Independent critic; I did not write the dossier, the search
code, the certifier or the reviews. Paths are relative to `research-20260929/`
(R/) unless stated otherwise. My scripts and logs are in
`paper-open-minlplib/development/dossiers/checks/eg/critique/`. They ran in
`/tmp/egcrit`, single-threaded. Nothing under R/ or literature/ was changed,
and no long computation was rerun.

## Verdict

**Corrections needed. Nothing found invalidates a claimed bound or primal
point.** The three dual bounds, the primal points and the gaps hold as stated.

One new finding matters for the rigor statements. The dossier says route S-F
uses no library function, and that Lemma A1 (facts F1–F4) turns A1 into a
proof. Both statements are incomplete. Route S-F and route R both evaluate
integer powers `x ** 3` and `x ** 4`. On this machine numpy computes these with
Intel SVML `__svml_pow8_ha`, a vendor routine with no proved error bound. The
accuracy they need is weak, about 1e-12 relative against an observed 1.2e-16,
so no result changes. But:

- the trust bases in Sections 3.2, 3.4, 3.6, 3.7 and 9 need a pow hypothesis;
- the two certificates of eg_disc2_s parts 0 and 2–7 share this routine;
- a cheap rerun can remove the hypothesis from S-F (about 3 CPU-h).

Route S-I (outward-rounded intervals, `egtm`, `kan_iv`, `ia`) uses no library
function in any bound, as the dossier says. Its part-1 replay for eg_disc2_s
has a small side condition, however (correction C2).

## What I checked and agree with

- **Theorem values.**
  - L, U, the binary64 values, the display differences and the gaps match
    `checks/eg/r2/logs/displays.log` and the run logs.
  - Final lines of `int9_final`, `int9_ni3`, `disc9_p*`, `disc9_ni3_p*`,
    `disc2_9_p0..7` and the review's `disc2_9_ni_p1`: done=True, open 0, the
    stated certified values and statistics.
  - Run I part 1: 55,971 boxes, lp_close 215.
- **Leaf counts, pieces and margins.**
  - 1,114,361 leaves and 1,769,947 pieces; 213,351 pieces in part 1
    (`verify_disc2_p1.log`), so 1,556,596 in parts 0 and 2–7.
  - 98,234 leaves with margin +∞ and 327,384 split leaves; margin
    distribution as in `margins2.log`.
- **Per-piece costs.** 5.7, 7.4, 7.3, 9.2 and 7.1 ms per piece in the review
  logs (eg_int_s, eg_disc_s p0/p1, eg_disc2_s p1, p0 sample). This supports
  the 5.3–9.2 ms range. 10,864 exp arguments per piece = 4 × 28 × 97.
- **Lemmas 2–6, 8 and 9.** Re-derived:
  - both remainder families;
  - φ''' = φp(p² + 6b) and φ'''' = φ(p⁴ + 12bp² + 12b²);
  - the signs of the weak-duality combination and the c_lo/ghi/glo
    directions in `egbb._combine`;
  - the FBBT rounding directions;
  - the invariant of `BB.run`, including incumbent updates inside an
    iteration.
- **Proposition A2′.** Re-derived from `indep_cert.py` lines 95–218:
  - Taylor path: 1.1e-14 − 3u + (1e-13 − γ₉₉) = 9.97e-14;
  - natural path: about 1.09e-13.
  - I agree, with the ulp count corrected (C5) and the pow interaction noted
    (C1).
- **The exp path.**
  - numpy 2.5.1; float64 exp dispatches to X86_V4 on a Xeon w5-2565X with
    AVX-512.
  - `DOUBLE_exp_X86_V4` calls `__svml_exp8_ha@plt` (6 call sites) and
    `exp@plt` (1 call site, the fallback).
- **fexp constants.** I checked them exactly without trusting mpmath. This
  complements the dossier's `table_exact.py`, which checks only the kan_iv
  table and LN2:
  - |ln2/64 − L1 − L2| ≤ 1.8e-28 against the rational series;
  - L1 has 32 bits;
  - L1 lies below ln2/64 by a relative 2.75e-10 (`logs/l1l2.log`).
- **Other numbers.**
  - Literature numbers: CAMINO values and differences 5.201056, 0.431290 and
    0.244594; old GAMS World point; S-B-MIQP 2.2e-7.
  - Campaign rows 57–65.
  - MINLPLib page values and dates.

## Corrections

**C1 (major; not invalidating). A library power function is used by S-F and R.**

- **Locations.**
  - Bottom line: "S-F … own exp (fexp, no libm)".
  - §3.2: hypotheses for eg_disc2_s parts 0 and 2–7.
  - §3.4: rows "must be trusted" and "enclosures".
  - §3.6: F1–F4 and "A1 then stops being an assumption".
  - §3.7: Lemma S.
  - §8.3: option (f), "route R needs only (H0) and Lemma A1"; conclusion
    "not needed for the theorem at all".
  - §9: rigor sentence "a library-free exponential".
- **Problem.**
  - `retry/egfast.py` line 259 computes `tau ** 3` twice in `e3`. `e3` is
    the error bound of the cubic moment tensor in the third-order branch,
    which the final runs C, E and G used.
  - `reviews/eg-retry-review-checks/indep_cert.py` computes `tau ** 3`
    (line 163, `e3`), `p ** 3` (line 193, R2) and `p ** 4` (line 194, R4).
  - For float64 arrays, numpy evaluates `x ** k` with k ∉ {−1, 0, 0.5, 1, 2}
    through `np.power`. `** 2` is `np.square`.
  - `DOUBLE_power_X86_V4` calls `__svml_pow8_ha@plt`, with `pow@plt` as the
    fallback.
  - F1–F4 cover +, −, ×; Lemma S covers fexp and IEEE operations. Neither
    covers pow.
- **Evidence** (`logs/libpaths.log`, `logs/powtest.log`).
  - On 300,000 samples, `x**3` differs from `x*x*x` in 26.7% of cases and
    `x**4` differs from `(x*x)*(x*x)` in 50.4%. `np.power(x, 3.0)` equals
    `x**3` bit for bit.
  - The largest error against exact Fraction powers is 1.12u (20,000
    samples).
  - `x**2` equals `x*x` bit for bit.
  - grep finds no power or libm call in the bounds of `egtm.py`, `kan_iv.py`,
    `ia.py`, `egbb.py` or r1's `own_ia.py`. The only exp/`**` uses there are
    in the split-score and row-choice heuristics.
- **Needed accuracy.** These are my estimates, by the slack argument of
  Proposition A2′; they still need to be written out.
  - Route R: p³ and p⁴ enter R2 and R4 linearly. The two (1+1e-12) factors
    on P absorb a relative shortfall δ ≲ 1e-12, jointly with A2′ at 9.9e-14.
    For τ³ in e3, dE < 1e-6 is asserted, so δ up to about 6e-10 is absorbed.
  - Route S-F: a shortfall δ·e3 is absorbed by the about 3e-12 relative slack
    of `infl(infl(cub + cubU)(1+SL))`.
  - So a hypothesis such as "np.power (SVML `__svml_pow8_ha`) has relative
    error ≤ 1e-12 on the arguments used" suffices: about 4,500 ulp, against
    an observed 1.12u.
  - It is weaker than A2′ (446 ulp) but of the same kind: a vendor routine
    without a proof.
- **Fix.**
  1. State this hypothesis in Lemma S, Lemma A1, the §3.2 hypotheses for
     eg_disc2_s parts 0 and 2–7 and the §3.4 table.
  2. Note that the two certificates of those parts share this routine.
  3. To remove it from S-F, rerun run G parts 0 and 2–7 from a /tmp copy of
     egfast.py with `tau*tau*tau`. The two roundings are covered by the
     existing (M+4)u slack. Compare the logs with `disc2_9_p*.log`. Cost:
     about 10,900 CPU-s at the original load (about 3 CPU-h), or about 1.5 h
     wall on 2 cores, probably less on a quiet machine. This is cheaper than
     option (g) and gives parts 0 and 2–7 a certificate under (H0) and
     Lemma S only.
  4. In option (f), also audit `np.power`. There are about 8,148 values per
     piece; a float check against fl(x·x·x) with an explicit γ₂ bound costs
     about 0.1 ms per piece. Replacing the powers by products instead would
     lose the bit-for-bit reproduction of `res/`.
  5. Change the §9 sentence accordingly.

**C2 (minor). The S-I certificate of eg_disc2_s part 1 used the pre-guard
`dual_value`.**

- **Locations.** §3.2 "(H0) only (route S-I)" for i7 ∈ [24, 27]; §3.4
  "complete for … eg_disc2_s part 1"; §8.6.
- **Evidence.**
  - `reviews/eg-retry-review-checks/logs/disc2_9_ni_p1.log` has mtime
    2026-10-01 01:06:08.
  - The guard entered `retry/egbb.py` later (mtime 11:57:32; retry §10
    item 3).
  - The guard reruns (`retry/logs/guard/*`, `compare.log`) cover runs A–E
    and G–I only.
- **Why it matters.** The pre-guard code returns an invalid positive bound if
  vl < 0 and S.lo < 0. This is very unlikely (Σ_obj y = 1 by LP duality; the
  guarded rerun of S-F part 1 saw a minimum Σy of 0.9999999999999998) but was
  not logged for this replay.
- **Fix.** Either state the side condition, or rerun the replay under
  `check_guard.py` from a /tmp copy: about 5,755 s at the original load
  (about 1.6 CPU-h). S-F (guard-checked) and R certify this part too, so no
  result is at risk.

**C3 (minor). The publisher correction has been read.**

- **Locations.** §7 ("**not read**"), issue 12, eg-12, and the corresponding
  "Must not claim"/literature caveats.
- **Evidence.**
  `literature/papers/go2026-publisher-correction-parabolic-approximation-relaxation/`
  (added 2026-10-04, status "read"). In its fulltext, Table 17 on PDF p. 39
  gives:
  - eg_int_s, SCIP orig: 9085.1 s, 6.5 | 6.5;
  - eg_disc_s, SCIP*: 3.6 | 5.8;
  - eg_disc2_s, SCIP: −1.1 | 6.3.

  The headers still read "primal value | dual value". The asterisk and the
  exclusion sentence are kept.
- **Fix.** Cite J. Glob. Optim. 95 (2026) 1095–1141 (the correction) and drop
  the "unread" caveat. Keep the reversed column reading. The literature small
  report's §9.2 note is stale; that is for its owner.

**C4 (minor). The instance-list dual has an explanation.**

- **Location.** §2 ("I did not establish why"; "bold marks as on the
  pages").
- **Evidence.**
  - `publication/minlplib-status/data/part_a.json` marks three duals bold on
    each page:
    - eg_int_s: BARON 0.14309125, SCIP 6.32629896 and SHOT 0;
    - eg_disc_s: BARON −0.2567667, SCIP 3.36596129 and SHOT 0;
    - eg_disc2_s: ANTIGONE −5.22577638, SCIP −1.48945961 and SHOT 0.
  - MINLPLib `doc.html` says: "The 1st, 2nd, and 3rd best bound are in bold."
  - The listing duals 0., −0.2568 and −5.2258 equal the third-best page dual
    in all three cases.
- **Fix.** Show all three bold duals. Say that the listing dual equals the
  third-best (bold) page dual. This is an observation consistent with
  doc.html; the rule itself is not documented there.

**C5 (minor). The ulp count is off by one.**

- **Locations.** Bottom line, Proposition A2′, §8.3(a), eg-2.
- **Evidence.** 9.9e-14 / 2⁻⁵² = 445.9, so "ε ≤ 9.9e-14, at least 446 ulp"
  is inconsistent. The proved tolerance 9.967e-14 corresponds to 448.9 ulp.
- **Fix.** Write "9.9e-14 (≥ 445 ulp)" or "9.96e-14 (≥ 448 ulp)". Apply C1's
  joint statement with pow.

**C6 (minor). One cost figure omits the recordings.**

- **Location.** §8.3(f), "Interval auditor: about 6.3–8.4 CPU-h for all
  leaves".
- **Evidence.** 1,933,502 × (5.3 + 6.5 … 9.2 + 6.5) ms = 22,800–30,400 s =
  6.3–8.4 h. The fexp figure (4.3–6.4 CPU-h) includes the ≈1,650 s needed to
  regenerate the eg_int_s/eg_disc_s recordings; this figure does not.
- **Fix.** 6.8–8.9 CPU-h with the recordings.

**C7 (minor). §3.7 overstates the replays.**

- **Location.** §3.7, "closed exactly the same boxes … on more than 250,000
  boxes".
- **Evidence.** Only the logged statistics are identical, and run I part 1
  differs (55,971 vs 55,973 boxes). This contradicts the dossier's own
  issue 9.
- **Fix.** Write "identical logged statistics (except one box in run I
  part 1)".

**C8 (minor). Issue 10 misplaces the overstatement.**

- **Location.** Issue 10 / eg-10.
- **Evidence.**
  - The eg-recheck report concerns eg_disc2_s only, so its remark does not
    claim anything for eg_int_s.
  - For eg_disc2_s, "several orders of magnitude" is itself too strong. By
    the dossier's own numbers, 1.0e-9 against ≈2e-11 is a factor of about
    50. Against the ≈1e-12-relative padding (5.6e-12 absolute) it is about
    180.
- **Fix.** Write "about two orders of magnitude" for eg_disc2_s and keep the
  eg_int_s caveat.

**C9 (minor). The flush-to-zero remark in (H0) is not established.**

- **Location.** (H0), "Route R would also tolerate flush-to-zero".
- **Evidence.** The moment error terms e1–e3 have no absolute pad of their
  own. A flushed product is covered only through dw·τᵏ ≥ 1e-300·τᵏ, which
  fails for τ below about 1e-4.
- **Fix.** Drop the remark. (H0) assumes gradual underflow anyway.

**C10 (minor). The Lemma A1 table omits roundings of the padding operations.**

- **Location.** §3.6 table.
- **Evidence.** The table leaves out fl(tl − dt), fl(Elo − err),
  fl(exp·(1 ∓ 1e-14)), fl(tlo ∓ 1e-14|tlo|) and fl(glo − pad). Each adds up
  to u of the padded quantity. The headroom covers them, but some stated
  factors shrink; for example, the exponent ends need 10u against 90u, which
  is 9×, not 10×.
- **Fix.** Include these roundings in the appendix version.

**C11 (minor). The choice of auditor for option (f).**

- **Location.** §8.3(f).
- **Problem.**
  - `fexp` is the author's code. Using it as auditor makes the
    "independent" route R depend on the author's exp lemma and on the shared
    kan_iv table.
  - The existing independent interval exp of review r1 (`own_ia.py`) is not
    a usable alternative.
- **Evidence** (`logs/r1exp.log`). r1's exp has relative width up to 4.9e-13
  on [−700, −600] and runs at about 2.1 µs per argument, because it reduces
  by k·ln2 in interval arithmetic.
- **Fix.**
  - If independence matters, write a fresh outward-rounded Cody–Waite
    auditor with exact m·L1 (the dossier's own second option), or state the
    coupling.
  - Audit against A2′ (ε = 9.9e-14) rather than A2. That relaxes the
    required auditor width to below about 1.98e-13. kan_iv (3.45e-13) and
    r1 (4.9e-13) still fail this requirement.

## The A1/A2 options re-assessed

| option | the dossier's assessment | my assessment |
|---|---|---|
| (a) Proposition A2′ | proved; ε ≤ 9.9e-14 | correct; ulp count (C5); must be stated jointly with pow (C1) |
| (b) re-frame on routes S | removes A2 from the theorem with no computation | removes A2, but S-F still needs the pow hypothesis (C1); S-I part 1 has the guard side condition (C2). Removing pow from S-F: rerun run G parts 0 and 2–7 with products, about 3 CPU-h |
| (c) prove an SVML exp bound | expert days; not recommended | agreed; it would also be needed for `__svml_pow8_ha` |
| (d) margin argument | cannot remove A2 | agreed. Combined with (e) it could weaken A2 by several orders of magnitude for row and LP leaves (r1 already covers every leaf with margin ≤ 4.7e-3 … 7.2e-2 per part), but it needs per-leaf sensitivities, records no tolerance for side or Farkas leaves, and remains an assumption |
| (e) outward-rounded recheck of small-margin leaves | done for 10,404 leaves | agreed. Extending r1's code to all 968,640 remaining leaves would cost about 0.2 s per leaf (r1 logs: 1,992 s for 9,074 leaves; 237 s for 1,400), that is roughly 50 CPU-h, with a risk of piece-cap failures because it has no LP. Not competitive |
| (f) exp-audited rerun of route R | 3.1–4.8 CPU-h (parts 0 and 2–7); 4.3–6.4 CPU-h (all) | costs are correct (the interval variant is 6.8–8.9 CPU-h, C6). It must also audit np.power (negligible cost). Auditor independence: C11 |
| (g) S-I replay of parts 0 and 2–7 | 11–23 CPU-h | correct (based on high-load timings, so conservative); it is the only option that is free of both Lemma S and libm |

## Checks run (all in /tmp/egcrit; logs in `checks/eg/critique/logs/`)

- `./libpaths.sh`: numpy dispatch, and objdump call targets of
  `DOUBLE_exp_X86_V4` and `DOUBLE_power_X86_V4`.
- `python3 powtest.py`: whether `**3` and `**4` are pow or products, and
  their error against exact Fractions.
- `python3 l1l2.py`: exact check of the fexp Cody–Waite constants against
  the rational ln 2 series.
- `python3 r1exp.py`: width and speed of r1's interval exp, run on a copied
  excerpt.
- Read-only: `grep` for `**`, `np.exp` and libm calls in `egfast.py`,
  `egtm.py`, `egbb.py`, `kan_iv.py`, `ia.py`, `indep_cert.py` and
  `own_ia.py`; `ls --time-style=full-iso` of the replay log, `egbb.py` and
  the guard logs; the run and verify logs; `part_a.json`; `doc.html`; the
  KB entry of the correction.
