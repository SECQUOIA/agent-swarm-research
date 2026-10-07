# Critique of the dossier `powerflow`

Critic: independent reviewer, 2026-10-04. I did not write the dossier. `R/` means
`research-20260929/`. My scripts and logs are in `checks/powerflow-critique/`
(README.txt lists inputs, patches and commands). Every run used a scratch copy in
`/tmp/pfcrit`, one thread. Nothing under `R/` or `literature/` was imported, executed or
edited.

## Verdict

**Corrections needed. Nothing invalidates a claimed result.**

- The three dual bounds hold. I re-derived Lemma 1, Proposition 2, Lemma 3, Lemmas 4–5,
  Theorem B's covering argument, Proposition 6 and the Krawczyk argument, and found no gap.
- I also ran two new replays:
  - The 0030p certificate on the 0039 reviewer's independently read rows. The value equals
    `bound_exact` exactly, and A is positive definite.
  - The angle-free 0039p variant with the reviewer's code (own OSIL reader; Cholesky, exact
    residual and Gershgorin). This settles the dossier's only open computation (PF-3).
- Every number I checked against its source is correct, except the items below.
- The corrections fall into these groups:
  - one mathematical misstatement (the eigenvalue "split" in §3.6);
  - one wrong set of identifiers (0039r balance rows);
  - one wrong description of prior work (Chen–Atamtürk–Oren);
  - an incomplete and partly wrong location list for the unsafe 0039r display;
  - a false "not documented" statement about MINLPLib;
  - several wording fixes.

## What I checked

| check | how | result |
|---|---|---|
| angle-free 0039p (dossier PF-3) | reviewer's `verify_leaves.py`, copied to /tmp; angle multipliers set to 0; rows from `own_osil`/`own_relax`; 50-digit λ_min, 60-digit Cholesky, exact residual, Gershgorin (`logs/noangle_0039p.log`, 9 s) | all 6 leaves PD at ε = 0 (λ_min 4.29e-9 … 5.80e-8; decisive leaf 4.60e-8); minimum **41869.05148528834**, floor·10¹² = 41869051485288344; equals the dossier's value |
| control for the patched copy | same script with stored multipliers (`logs/control_0039p.log`) | reproduces the review: 41869.051485240394, decisive λ_min −1.094e-9 |
| 0030p certificate on independently read rows | stored 332 multipliers on the reviewer's `own_relax` rows; reviewer's exact Lagrangian; my natural-order exact LDLᵀ; Gershgorin route (`logs/root0030p_ownrows.log`) | const + inner = stored `bound_exact` exactly (576.8934122988004698491596317863177375044); 60 positive pivots (min 1.12e-7) |
| Proposition 6 (J-commutation) on 0039r | own ElementTree read of the OSIL; every 2×2 block of every quadratic row (`logs/jcheck.log`) | all 262 rows (184 flow, 78 voltage) commute exactly with J |
| eigenvalue pairs | 50-digit eigenvalues (`logs/eigpair.log`) | 0030p: 4.00111498512691e-9 twice; 0039p decisive leaf: −1.09429999213631e-9 twice, and +4.60033383239604e-8 twice when angle-free |
| vertex planes, all 15 tight leaves | own exact enumeration (`logs/planes.log`) | 4 planes per leaf, H ≥ F at all 8 vertices; on every leaf 2 planes touch 4 vertices and 2 touch 5 |
| containment, leaf identity, gaps, displays | `misc_exact.py` | both exact points lie in their decisive leaves; exact W_NN(x*) = F (v₂ = 1.0424182700750…); gaps, displays and improvements as in §5; root envelope error 7.216e-3 |
| leaf rows | GAMS text of 0039p/0039r (`e64, e65, e156, e157, e397, e407, e581, e591, e307`) | 0039p as stated; 0039r balance rows differ from §3.5 (C2) |
| MATPOWER case39 | `network/sources/matpower_case39.m` | buses 30–38 are leaves; 2–30, 6–31, 10–32 and 22–35 have r = 0 and b = 0; there are 12 tapped branches (23–36 has τ = 1); gen 30 data as stated |
| status, solver, primal, verification sources | `fetched.json`, `instances.html`, `doc.html`, `results_table.md`, primal report and logs, the 0039 and wave-3 reviews, closing-confirm r1/r2, reproduction logs | all match except C4, C5 and C9 |
| literature | KB full texts: Chen–Atamtürk–Oren, Lavaei–Low, Oustry et al., Jansson et al. 2007, Gopalakrishnan et al.; KB metadata | Lavaei–Low, Oustry, Jansson, Gopalakrishnan and PF-12 are correct; Chen et al. is misdescribed (C3) |

## Corrections

**C1. §3.6, "Floating-point multipliers split the double zero eigenvalue into a pair"
(line 492), and "4.00126e-9 and 4.00143e-9, a pair".**

- *Problem.* The sentence contradicts Proposition 6:
  - A(w) commutes with J for every w, including the exact rationals of float multipliers.
  - So every eigenvalue of A(w) has even multiplicity, exactly.
  - Inexact multipliers *move* the double eigenvalue away from 0. They cannot split it.
  - The two float64 values are one double eigenvalue plus eigensolver rounding.
- *Evidence.* 50-digit eigenvalues:
  - 0030p: 4.00111498512691e-9 (twice);
  - 0039p decisive leaf: −1.09429999213631e-9 (twice);
  - the next pair is 0.7654;
  - 0039r rows commute exactly with J (`jcheck.log`), and polar rows commute by construction.
- *Fix.* "Inexact multipliers shift the double zero eigenvalue to a double eigenvalue of
  either sign. For 0030p it is +4.0011e-9; the 0039p decisive leaf has −1.0943e-9 and the
  0039r decisive leaf about −6.07e-10."
- Also say that Proposition 6 is the standard real representation of a Hermitian matrix.
  Lavaei–Low already report paired zero eigenvalues. Do not present it as new.

**C2. §3.5 Leaf data (line 368): the 0039r balance rows.**

- *Problem.* The dossier names the rows `x103 − x263 = 0` and `x195 − x273 = 0` for both
  models. In 0039r the flow variables have other indices.
- *Evidence.* GAMS 0039r gives:
  - `e397.. x64 - x263 =E= 0`;
  - `e407.. x156 - x273 =E= 0`;
  - e65 defines x64 and e157 defines x156.

  The 0039 review §2 has the same slip.
- *Fix.* "0039p: x103 − x263 = 0, x195 − x273 = 0 (e581, e591); 0039r: x64 − x263 = 0,
  x156 − x273 = 0 (e397, e407)."

**C3. §7, Chen–Atamtürk–Oren (line ~767) and the sentence "an affine image of their
coordinates".**

- *Problem.* Their set J_C does not have box bounds on Re W_ij and Im W_ij. It bounds:
  - W_ii and W_jj;
  - the phase ratio, L_ij W_ij ≤ T_ij ≤ U_ij W_ij, with W_ij ≥ 0.
- *Evidence.* The KB full text (the display (2a)–(2e) was lost in extraction) says:
  - "Let T_ij = αW_ij for some L_ij ≤ α_ij ≤ U_ij. Note that constraint (2d) restricts W_ij
    to be nonnegative";
  - "constraint (2c) models nodal phase angle difference bounds";
  - "valid bounds for constraint (2c): −L_ij = U_ij = √(U_iiU_jj/(W⁻)² − 1)".
- The leaf box is different. It bounds Im W_NL, W_LL − Re W_NL and W_LL, and leaves W_NN
  unbounded. It is not an affine image of J_C.
- *Fix.* Describe J_C correctly. Delete "an affine image of their coordinates". Say the leaf
  cut is the concave envelope of the same rank-one 2×2 relation under a different bound
  structure, which here comes from the generator P and Q boxes.
- Keep "do not claim novelty". Note that the closest unread prior work is probably the
  Coffrin–Hijazi–Van Hentenryck SDP-strengthening cuts (PF-10).

**C4. PF-1 and §5, locations of the unsafe 0039r display 41869.05148327244.**

- *Problem 1.* The extension report's Summary table shows **41869.05148327**, which is safe.
  Only the §3 table (line 102) has …244.
- *Problem 2.* The list misses these occurrences:
  - the 0039 review's verdict bullet (line 17): "41869051483272433/10¹² = 41869.05148327244".
    This equality is false; the rational is 41869.051483272433.
  - `publication/reproduction/result-map.json` (numeric_evidence);
  - the `LB` float in `bb3t.json`;
  - several reproduction and verify logs.
- *Problem 3.* The issue is not new. `reviews/closing-confirm-r1.md` (line 126) flagged it.
  That flag led to the summary's safe display.
- *Fix.* Correct the location list and credit closing-confirm r1. The resolution itself
  (cite …243 or the rational) is right.

**C5. §2, "The page's measure is not documented".**

- *Problem.* The statement is false. MINLPLib's `doc.html` defines INFEASIBILITY as "The
  maximal absolute violation of all problem constraints, including variable bounds…".
- *Fix.* "MINLPLib reports the maximal absolute violation, evaluated by MINLPLib on its
  stored point. Ours is a 50-digit evaluation of the decimal `.sol` values, with missing
  entries set to 0. The two need not agree." Quote both measures and name them.

**C6. §1.4, "At the optimum, v₃₀ = 1.06 and Qg = 1.4" (line 132).**

- *Problem.* The optimum is not known.
- *Fix.* "At p1 and at the exactly feasible point x* (where v₃₀ = 53/50 and Qg = 7/5 are
  fixed exactly)."

**C7. Theorem B and §3.7 (iv), planes that "pass through four vertices".**

- *Problem.* On every leaf, two of the four planes pass through five vertices.
- *Fix.* Write "at least four". Optionally explain the count:
  - on each face W_LL = const, F is a separable quadratic in (Pg, Qg), so its four vertex
    values are coplanar;
  - hence the concave envelope has exactly 4 facets;
  - the 4 planes are the whole envelope.

**C8. §3.5, "Shifts used … all other 0039r leaves: ε = 0".**

- *Problem.* These are the dossier's recomputed shifts, not the stored certificate's. The
  stored bounds imply ε = 1e-9 on three non-decisive 0039r leaves (own − stored = 4.38e-8)
  and 1e-10 on one (4.38e-9).
- *Fix.* Label the column "ε in my exact recomputation". Give the stored ε separately, or
  drop them, since only the decisive leaves matter.

**C9. §1.5, quote of `history_final.log`.**

- *Problem.* The quoted "rows_numerically_different 0" is the field of the comparison with
  the 2017 MINLPLib.jl conversion. The comparison of the current GAMS (via Convert) with the
  OSIL is the `control` field: "same (rows equal at 50-digit sample points; representation
  differs)" (`history.py`, `osil_compare.py`).
- *Fix.* Quote the control field. The conclusion is unchanged.

**C10. §1.4 and §3.5, sign of b.**

- *Problem.* In §1.3's π-model the leaf branch has series susceptance b_km = −55.2486….
  The b of §1.4 and §3.5 is −b_km = 1/x, rounded to 15 digits.
- *Fix.* Define b := −b_km > 0 once.

**C11. §3.5 "Angle-free variant … not yet independently reviewed", and PF-3.**

- *Update.* My replay with the reviewer's independent code confirms it:
  - all 6 leaves are PD at ε = 0;
  - the minimum is 41869.05148528834;
  - floor·10¹² = 41869051485288344.
- *Cost.* The replay took 9 s, not "1–3 CPU-minutes".
- *Fix.* Set PF-3 to "no new computation needed". The status is "replayed by the critic with
  the 0039 reviewer's code"; a formal review may still be wanted. Keep citing
  41869.05148485014.

## Additional issues

1. **(minor) The 0030r certificate is omitted.**
   - Wave 3 also certified powerflow0030r at 576.8934126255 (`open-instances-wave3/report.md`
     l. 89–90; network report §3.2).
   - The wave-3 verifier lists 0030r as "not checked".
   - The paper should omit it or label it unverified, and never use it for 0030p.
2. **(minor) §3.8, the 0039r Clarabel primal value.**
   - Clarabel's primal value 41867.779703029 lies *below* the exactly certified root dual
     41867.77970316397, by 1.3e-7 (`sdp0039r_root_tight.log`).
   - So it is not an upper bound on val(Shor), even at the 1e-7 level.
   - Say this when describing the plain-SDP gap of about 1.27 as numerical.
3. **(minor) §1.4 wording.**
   - "The plain SDP relaxes exactly this branch" restates an unchecked diagnostic ("only line
     1–29 had a 2×2 defect above 1e-6"; review §8). Label it as a diagnostic.
   - Write "cuts at bus 30 alone sufficed" instead of "only bus 30 needed cuts".
   - Buses 31, 32 and 35 are also lossless leaf generator buses with no charging. The
     identity applies to them as well.

## The dossier's issue list and cost estimates

- PF-1: correct in substance; locations need fixing (C4).
- PF-2: correct.
- PF-3: resolved (C11). The cost was overestimated: 9 s against 1–3 min.
- PF-4: correct. My replay of the 0030p multipliers on the independent rows adds the bound
  value itself.
- PF-5 to PF-8: correct.
- PF-9: correct. The half-day estimate for a rigorous primal SDP certificate is plausible.
  The near rank-2 W will need a positive-definiteness margin after exact projection, which
  costs objective accuracy.
- PF-10: needs C3. The reading estimate of 1–2 hours is plausible.
- PF-11 to PF-14: correct. PF-12 was confirmed against `paper.md`, `references.bib` and the
  full texts.
- The §9 "may/must not claim" lists are sound. Add "do not cite 0030r's wave-3 bound".

## Commands run (targeted only; from /tmp/pfcrit, one thread)

- `python3 own/jcheck.py`, `python3 own/planes.py`, `python3 own/misc_exact.py`
- `python3 rev/verify_leaves.py powerflow0039p bb3t noangle` (patched copy) and
  `… powerflow0039p bb3t`
- `python3 rev/root0030p_ownrows.py`, `python3 rev/eigpair.py`; the angle-multiplier listing ran inline and is saved as `anglemult.py`
- Read-only `grep`/`sed` on `R/`, the KB, the GAMS sources and the status pages.
- No SDP solve, no branch and bound, no project-wide check, no CI.
