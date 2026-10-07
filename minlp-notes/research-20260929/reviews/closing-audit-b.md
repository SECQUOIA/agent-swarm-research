# Closing audit B: novelty, significance, honesty and unresolved review issues

Date: 2026-09-30. Auditor: closing auditor B, an independent research agent
that did not write any of the material. Scope:
[`closing-research-results.md`](../closing-research-results.md) and
[`SYNTHESIS.md`](../SYNTHESIS.md), checked against the
[literature audit](../literature/decomposition-bb-prior.md), the novelty,
status, limitation and revision sections of every note, and every review,
recheck and confirmation in this folder. I edited no file. Nothing was
committed.

*Provenance.* My environment does not allow me to write report files, so
this text was returned to the root for saving verbatim.

**Method.**
- I read both closing documents and the literature audit in full.
- I read the Summary, status, novelty, limitation and revision sections of
  every theory note, the scaling study, the census and every instance
  report.
- I read the verdict, remaining-issue and suggested-edit sections of every
  file in `reviews/`, including the verification reports in subfolders.
- For each issue a review raised, I checked with `grep` whether the note
  under review contains the fix or an explicit refusal.

Only targeted commands were run: `cat`, `sed`, `grep` and `awk` on files in
this continuation folder, and one `python3 -c` computing
`sqrt(2e/pi) = 1.315489246958914`. There was no project-wide verification,
and CI was not inspected. I did not recheck any mathematics or rerun any
computation. Every finding below compares text with text.

## 1. Verdict in brief

The closing record and the synthesis are honest in most places. Most
sections separate proved results from computations, call novelty
provisional and keep the negative results. The problems are the following.

1. **One statement is wrong.** SYNTHESIS Section 3b says the lower end of
   the tree sandwich is "approached, not attained". The consistency note
   says it is attained in 515 of 900 random instances. The claim that it is
   attained only in trivial cases was withdrawn after the recheck.
2. **The last three SYNTHESIS sections are out of date.** They predate the
   completion work: "What this means for solvers", "Novelty position" and
   "Open questions".
   - They still say "Eleven open instances" and "certificates for the 11
     instances"; 28 are now closed.
   - "The second certification wave is testing ..." describes a wave that
     has finished.
   - Several open questions have been answered or reformulated.
   - "SCIP 10 behaves as predicted" contradicts the notes, which place
     default SCIP outside the theorems' relaxation class.
3. **Several novelty claims lack the qualifiers that the literature audit
   and the reviews require.**
   - Closing item 1 has no prior-work qualifier at all.
   - The SYNTHESIS "not found elsewhere" list covers two things with prior
     results. The repository's own September 28 note already gives rigorous
     single-tree lower bounds for alphaBB-type relaxations. ex6_2_* already
     has ε-global solutions (McDonald–Floudas).
   - The consistency item says "one direction was known", but the note
     lists five components as known in substance.
   - That item also claims to "explain" the lower bounds of the
     September 28 sparse-moment rates. The September 28 identities already
     gave those lower bounds.
4. **Several theorem summaries drop hypotheses that limit their reach.**
   - The transfer theorem also needs interior optimal controls, uniform
     convergence of the Euler KKT points, the Euler scheme and an exact
     strict `C^4` calibration.
   - The `n ≥ 2` result holds only in the local formulation. It does not
     feed into the transfer theorem.
   - Theorem 3.4 is an existence result centred at `x*`, and its `c_g` is
     global.
   - Of the "three remedies, each proved", only the first is proved in
     general. The second is proved for the convex variant only; the third is
     supported by computation.
5. **The closing's verification paragraph overstates the fix-and-confirm
   process.** Three revisions were never rechecked. Several review chains
   end with minor items that were neither applied nor declined (Section 4).
6. **Most negative results are kept, but not all.**
   - The coupling note and the split-robust bound's tiny base are kept and
     clearly labelled.
   - The SYNTHESIS does not mention the eg_* failure.
   - The closing record omits the failure of the generic cell-constant DP.
   - Neither document mentions the earlier pindyck failure, and the wave-2
     report has no pointer to the extension that closed it.
   - Neither document mentions the prototype's failures on probe3.

What is right, and should stay:
- The closing header's definitions of "verified" and "reviewed", and its
  "novelty assessments are provisional".
- The KAN caveat (the claims concern a relaxation of exactly infeasible
  models).
- "Marginal for camshape100 and lnts50".
- "prior ε-global solutions exist" for ex6_2_*.
- The bound-audit presentation: 11 beyond the 1e-6 convention, 7 of them
  below 1e-4, 8 at tolerance scale.
- "Modest, largely negative" for the coupling note.
- "Only qualitatively" for the split-robust bound.
- The separation being "relative to fixed termwise relaxations and a fixed
  factorization".

## 2. Novelty and significance

**N1. Closing item 1 has no prior-work qualifier.**
- *Location.* `closing-research-results.md`, lines 17–36.
- *Problem.* Items 2–4 each carry a novelty line; item 1 does not. The
  literature audit rates C1, C2 and C4 "partially known" and names the
  antecedents. The decomposition review calls the separation "a clean,
  rigorous statement ... appears new, but it is modest", and meaningful
  for solvers "only qualitatively".
- *Fix.* Add a last bullet to item 1:
  > Prior work: cluster-problem estimates (Neumaier 2004;
  > Wechsung–Schaber–Barton 2014); the repository's September 28 lower
  > bound for relaxations with gap at least `alpha q_B` (constrained note,
  > Theorem 3.1); MILP B&B lower bounds and separations at treewidth 2 that
  > rely on ties (Basu et al. 2023; Dey–Shah 2022); discrete AND/OR and BTD
  > search; worst-case bounds `(C n/eps)^{O(w)}` (Zhang–Sun 2022;
  > Bienstock–Muñoz 2018); Berenguel et al. (2013) as the algorithmic
  > precursor for one shared variable; Robertson–Cheng–Scott (2025) for the
  > first-order copy error; Griewank–Toint (1984) for the chordal escape.
  > Not found in the audit: the face-exact lower bound at a unique
  > nondegenerate minimizer, Theorem 3.4 and the slope lower bound. The
  > reviewers rate the separation modest and meaningful for solvers only
  > qualitatively.

**N2. Closing item 1 drops hypotheses.**
- *Location.* `closing-research-results.md`, lines 20–36.
- *Problems.*
  - `0.57 (5/3)^n` holds for `eps <= 1e-4` and `r >= 1/2`. With bound
    tightening, the count is leaves plus `2n` per tightening round.
  - Theorem 3.4 also needs Lipschitz factor gradients, vertex-vanishing
    relaxation error and a cell-width condition. It is an existence result
    centred at `x*`, but "have size" reads as if every certificate had that
    size.
  - Proposition 2.6 is proved only for a child of the root with a
    one-dimensional separator.
  - The width lower bounds are for separable block families.
  - Theorem A.5 assumes monotone relaxations (M). The "real" extra factor
    is proved only for level-synchronous refinement.
  - The base 1.05 is computer-evaluated, not interval-certified.
- *Fix.*
  - Line 21: after "`0.57 (5/3)^n` leaves" add "(eps <= 1e-4; with bound
    tightening, leaves plus 2n per round)".
  - Lines 27–29: replace "have size" with "exist with size". After "under
    quadratic growth" add ", Lipschitz factor gradients, vertex-vanishing
    relaxation error and a cell-width condition (the construction is
    centred at x*)".
  - After "`Omega(eps^{-1/2})` cells" add "(proved for a child of the root
    with a one-dimensional separator)".
  - Replace "width lower bounds hold for every tree decomposition" with
    "width lower bounds hold for every tree decomposition of separable
    block families".
  - After "without knowledge of `x*`" add "(with monotone relaxations)".
    Replace "its extra factor is real" with "its extra factor is real for
    this level-synchronous algorithm".
  - Line 36: replace "(bases about 1.003–1.05)" with "(bases about 1.003
    proved analytically and 1.05 computer-evaluated; the method cannot
    exceed about 1.063; restricted split classes on a gadget family)".

**N3. Closing item 2 overstates "explains" and understates prior work.**
- *Location.* `closing-research-results.md`, lines 41–43.
- *Problem.* The consistency note (Summary D and F) says the September 28
  notes already proved the identities `v_n = -2E_n(h)` and
  `eta_n = -2E_n`, from which the lower bounds follow. The note itself
  evaluates the approximation errors, which raises the constants by about
  7.9 and 11.8 (asymptotic, floating point). The note lists five components
  as known in substance: the duality, the one-sided bound (de Farias–Van
  Roy), its positive-width form (Grimm–Netzer–Schweighofer 2007;
  Korda–Magron–Ríos-Zertuche), the zero-width identity (Han–Jiao–Weissman;
  September 28 notes) and the bracket form.
- *Fix.* Replace the last two sentences with:
  > Proposition 5.1 gives an exact criterion for when affine splits
  > suffice. For the September 28 sparse-moment rates, the lower bounds
  > already followed from identities proved there; this note evaluates the
  > approximation errors (constants about 8x and 12x higher, asymptotic,
  > floating point). Known in substance: the duality, the one-sided bound
  > (de Farias–Van Roy), its positive-width form (Grimm–Netzer–Schweighofer;
  > Korda–Magron–Ríos-Zertuche), the zero-width identity
  > (Han–Jiao–Weissman). New as far as found, and elementary: the exact
  > identity, the tree lower bound and counterexample, the kink bound, the
  > shell count.

**N4. Closing item 3: "New" is unqualified and hypotheses are missing.**
- *Location.* `closing-research-results.md`, lines 49–56.
- *Problems.*
  - The notes say "not found stated; all are elementary ... Searches were
    limited" (bang-bang report, Section 6) and "modest novelty"
    (calibration note, Section 6). They name Maurer–Pickenhain (1995) as
    related prior work.
  - Theorem 5.2 needs an exact strict `C^4` calibration, compact state and
    control sets, interior optimal controls, uniformly convergent Euler KKT
    points and the Euler scheme. Bang-bang arcs, singular arcs and state
    constraints fall outside it. The calibration note adds that strict
    smooth global calibrations are rare outside constructed or LQ-like
    cases.
  - The fixed-duration window is conditional on the assumptions of
    Corollary 4.3 (recheck-calibration-confirm, remaining point 1).
  - The `n ≥ 2` criterion holds only in the local formulation. It "does
    not feed into the transfer theorem" (extension-n2, Summary item 4).
- *Fix.*
  - Replace "New: a transfer theorem (strict smooth calibration ⇒ exact
    certificates for fine transcriptions, compact controls needed);" with
    "Not found stated in limited searches, and elementary: a transfer
    theorem (an exact strict C^4 continuous calibration with compact state
    and control sets, interior optimal controls and uniformly convergent
    Euler KKT points gives exact certificates for all fine Euler
    transcriptions; bang-bang arcs, singular arcs and state constraints are
    outside it);".
  - After "regular switch" add "(under the assumptions of Corollary 4.3
    and Theorem 2.3)".
  - Replace "in dimension `n ≥ 2` existence is decided locally by one
    number `eta_L`" with "in dimension `n ≥ 2`, in the local formulation,
    existence is decided by one number `eta_L` (this answers the
    continuous existence question only and does not feed into the transfer
    theorem, whose global form can fail even when eta_L > 0)".
  - Add "Related prior work: Maurer–Pickenhain (1995), quadratic
    verification functions via Riccati equations."

**N5. The same omissions in SYNTHESIS Section 8.**
- *Location.* `SYNTHESIS.md`, lines 335–342 and 354–364.
- *Fix.*
  - Lines 339–342: replace "gives exact certificates for every
    sufficiently fine transcription, provided the control set is compact"
    with "gives exact certificates for every sufficiently fine Euler
    transcription, provided the calibration is exact, strict and C^4, the
    state and control sets are compact, the optimal controls are interior
    and the Euler KKT points converge uniformly".
  - At the end of the `n ≥ 2` bullet add: "This settles the continuous
    existence question in the local formulation only. The transfer theorem
    needs the global form, which can fail even when eta_L > 0 (Example C, a
    floating-point blow-up); a transfer theorem for local calibrations is
    open."

**N6. SYNTHESIS novelty position.**
- *Location.* `SYNTHESIS.md`, lines 400–403.
- *Problems.*
  - Rigorous single-tree lower bounds at a nondegenerate minimizer already
    exist in the repository's September 28 constrained note (Theorem 3.1)
    for relaxations with gap at least `alpha q_B`. The literature audit
    (C1) and the decomposition review both say so, and Corollary 2.1 is
    that theorem on a path. What this continuation adds is the face-exact
    case; "(especially face-exact ones)" hides this.
  - "certificates for the 11 instances" is out of date; there are 28.
  - ex6_2_7 and ex6_2_5 have prior ε-global solutions (McDonald–Floudas
    1997) by a known method.
- *Fix.* Replace the sentence from "Not found elsewhere:" to the end with:
  > Not found elsewhere: rigorous single-tree lower bounds at a unique
  > nondegenerate minimizer for face-exact (termwise McCormick) relaxations
  > (for relaxations with gap at least alpha q_B such bounds are in the
  > repository's September 28 constrained note, Theorem 3.1, and the
  > cluster-problem literature predicted the growth as estimates);
  > instance-dependent decomposition-certificate bounds; the slope lower
  > bound; the RLCT characterization; and rigorous certificates for the 28
  > closed instances (ex6_2_7 and ex6_2_5 already had ε-global solutions,
  > McDonald–Floudas 1997, by a known method; camshape100 and lnts50 were
  > already within 1.2e-6 and 3.8e-5 relative of closure).

**N7. "The case usually described as costing only `log(1/eps)` nodes".**
- *Location.* `SYNTHESIS.md`, lines 21–25.
- *Problem.* The cluster-problem literature already estimates exponential
  growth in `n` near nondegenerate minima (literature audit, C1). The
  `log(1/eps)` statement concerns `eps` at fixed `n`.
- *Fix.* Replace the phrase with "the case whose cost grows only like
  `log(1/eps)` at fixed `n` (September 28 notes); the cluster-problem
  literature estimated exponential growth in `n` here (Neumaier 2004;
  Wechsung–Schaber–Barton 2014), and Theorem 1 makes this rigorous for
  termwise relaxations at treewidth 1".

**N8. "Structure-aware duality certificates" and "in every closed case".**
- *Location.* `SYNTHESIS.md`, lines 35–41; `closing-research-results.md`,
  lines 78–80; `open-instances-summary.md`, lines 106–117.
- *Problems.*
  - Not all 28 closures are duality certificates along a structure.
    hvycrash is an exact identity; pindyck uses concavity on a polytope;
    etamac uses hidden convexity; ex6_2_* uses a known Gibbs tangent-plane
    method; powerflow uses an SDP dual. The SDP dual's tightness on the
    IEEE 30-bus case agrees with Lavaei–Low (wave-3 verification,
    Section 4).
  - "The obstacle was the relaxation, not the amount of branching" is an
    interpretation. No experiment tested it.
  - The summary says "The certificates all combine a decomposition along
    the model's chain or period structure", which is false for the
    instances above. It also calls the consistency theory "under review",
    which is out of date.
  - The closing's list of mechanisms omits SDP duality.
- *Fix.*
  - SYNTHESIS line 35: replace "Structure-aware duality certificates" with
    "Instance-specific certificates (Lagrangian and SDP duality,
    calibrations, comparison, concavity and exact identities)".
  - SYNTHESIS line 39: replace "in every closed case the obstacle was"
    with "in our reading of every closed case, the obstacle was".
  - Closing line 80: replace "the diagnosis that relaxations, not
    branching, were the obstacle" with "the interpretation (not tested
    experimentally) that relaxations, not branching, were the obstacle".
    Add "SDP duality" to the list on line 78.
  - Summary lines 109–112: replace "The certificates all combine" with
    "Most certificates (lnts, dtoc5, lukvle10, optcdeg2, chain, catmix,
    waterno2) combine", and add "The others use an exact identity
    (hvycrash), a Gibbs tangent-plane test (ex6_2_*), hidden convexity
    (etamac), concavity on a polytope (pindyck) or an SDP dual
    (powerflow)." Replace "which is under review" with "(reviewed and
    confirmed)".

**N9. Consistency attribution in the SYNTHESIS.**
- *Location.* `SYNTHESIS.md`, lines 199–203.
- *Problem.* The recheck required crediting Grimm–Netzer–Schweighofer
  (2007); the note does so, but the SYNTHESIS credits only
  Korda–Magron–Ríos-Zertuche and de Farias–Van Roy.
- *Fix.* Replace the last sentence with: "Known in substance: the duality;
  the one-sided bound (de Farias–Van Roy; on paths the tree upper bound is
  their approximate-LP bound); its positive-width form
  (Grimm–Netzer–Schweighofer 2007, quantitative in
  Korda–Magron–Ríos-Zertuche); the zero-width identity (Han–Jiao–Weissman;
  the September 28 notes); the bracket form (robust-lower-bound note,
  Proposition 3.3)."

**N10. Chordal credit and the scope of Observation 4.2.**
- *Location.* `SYNTHESIS.md`, lines 130–139.
- *Problem.* The face-exact recheck required crediting Griewank–Toint
  (1984). Convexity "near `x*`" needs positive definite blocks, not merely
  PSD ones. The scope of Observation 4.2 (asked for by the decomposition
  recheck) is missing, and so is the classical source of its measure form.
- *Fix.*
  - Line 134: after "near `x*`" add "(with positive definite blocks;
    Griewank–Toint 1984, Theorem 4, and their local convexification)".
  - Line 139: replace "So no lower bound can hold uniformly over all
    splits." with "So no lower bound can hold uniformly over all splits for
    relaxations that are exact at factor minima, such as convex envelopes;
    this says nothing about fixed rules such as alphaBB or about restricted
    split classes. The measure form is classical (Vorob'ev 1962; Lasserre
    2006)."

**N11. Coupling, Theorem 5.1.**
- *Location.* `SYNTHESIS.md`, lines 214–217.
- *Fix.* After "needs `C(n+1,(n+1)/2)` leaves on a one-row instance"
  insert "(without bound tightening; the count is Jeroslow's and the
  dynamic program is Vavasis's (1992); the contribution is the transfer to
  continuous spatial branching with Lagrangian bounds)".

**N12. RLCT: "within constant factors".**
- *Location.* `SYNTHESIS.md`, lines 309–311;
  `closing-research-results.md`, lines 84–86.
- *Problem.* The constants are exponential in `n` (RLCT note, Section 9:
  `12^n Lambda_2^(n/2)`). The result concerns alphaBB-type relaxations.
- *Fix.* In both files, replace "within constant factors of" with "within
  factors that depend only on `n` (exponential in `n`) of". Add "for
  alphaBB-type relaxations" after "uniform bisection" (SYNTHESIS) and
  after "node counts of spatial B&B" (closing).

**N13. Conditions and rounding in SYNTHESIS Section 1.**
- *Location.* `SYNTHESIS.md`, lines 55–66.
- *Problems.*
  - `0.57 (5/3)^n` needs `eps <= 1e-4` and `r >= 1/2`, and Theorem 1
    needs `D/(2b) <= 1.99`.
  - "base `1.31549`" rounds `sqrt(2e/pi) = 1.3154892` up. This is the same
    kind of rounding that the decomposition recheck found made a uniform
    statement false.
  - The decomposition note says alphaBB on an isolated bilinear term is
    dominated by McCormick and not used by solvers.
- *Fix.*
  - Line 59: "For the probe family this is `0.57 (5/3)^n` (eps <= 1e-4,
    r >= 1/2; the theorem needs D/(2b) <= 1.99)."
  - Line 65: "base `sqrt(2e/pi) ≈ 1.3154892`".
  - Line 64: after "Per-factor alphaBB on the bilinear terms" add
    "(dominated by McCormick and not used by solvers; kept for its
    eps-dependence)".

**N14. Missing limits.**
- *Location.* `closing-research-results.md`, Limits, lines 136–149;
  `SYNTHESIS.md`, Section 2, lines 82–91.
- *Problem.* The decomposition note (Section 6, items 3, 4 and 8) and the
  face-exact note (Section 11) state these limits; the closing does not.
- *Fix.* Add to Limits:
  - "The decomposition upper bound is an existence result centred at x*.
    Its constant c_g is global: a second local minimizer within delta of f*
    at distance D makes the base (C M_a D^2/delta)^{w+1}, no better than
    the worst case when delta ~ eps."
  - "The single-tree lower bounds do not cover MUSE-BB-type multisection
    in their cost measure, branching on lifted variables or
    objective-cutoff propagation."
  - "Computations use one solver (SCIP 10) and floating-point prototypes;
    the census is a root computation with heuristic widths and was not
    independently reviewed."

  Add the `c_g` sentence to SYNTHESIS Section 2, after the Theorem 3.4
  bullet.

**N15. Census and coupling baseline.**
- *Location.* `closing-research-results.md`, lines 93–99.
- *Fix.*
  - After "62.7% small nonlinear-term width" add "(heuristic width bounds
    at most 12; root computation, not independently reviewed; it does not
    show that width causes the difficulty)".
  - In the coupling bullet, write "from about 15% (baseline
    min(w_full, w_free), hence above the census's 13.6%) to 17%".

## 3. Proved, computed and plausible: "What this means for solvers"

**S1. "SCIP 10 behaves as predicted on these families."**
- *Location.* `SYNTHESIS.md`, line 376.
- *Problem.* Face-exact Sections 8 and 9.1 and decomposition Section 6,
  item 1 say default SCIP is outside both theorems' relaxation class, so
  the SCIP counts "are therefore not explained". The synthesis says the
  same in Section 3.
- *Fix.* Replace the first two sentences of the Evidence bullet with:
  > SCIP 10's node counts grow about fivefold per two added variables on
  > these families (n = 4–10; exponential and degree-5 polynomial fits are
  > not separated rigorously). Default SCIP is outside the theorems'
  > relaxation class (its minor separator adds PSD cuts), so the theorems
  > neither predict nor explain these counts. Constant-width MINLPLib
  > families become open as they grow; the census does not show that width
  > is the cause, since size, scaling and unbounded variables grow too.

**S2. Out-of-date counts and the "testing" sentence.**
- *Location.* `SYNTHESIS.md`, lines 377–378 and 384–385.
- *Fix.*
  - Replace "Eleven open instances yield to structure-aware duality in
    seconds to minutes." with "28 open instances were closed with
    instance-specific certificates; most use affine or state-dependent
    splits along chains plus short exact windows."
  - Replace "The second certification wave is testing how broadly this
    works." with "Waves 2 and 3 tested this. They closed 17 more instances,
    but eg_* failed, waterno2 remains 4.9–10.8% open, ann_cumene_tanh keeps
    a 19% gap, and several closures (hvycrash, ex6_2_*, etamac, pindyck,
    powerflow) did not use the tree mechanism."

**S3. The "Proved" bullet states an existence result as a solver cost.**
- *Location.* `SYNTHESIS.md`, lines 371–375.
- *Problem.* The certificates are built around `x*`. The only algorithm
  that does not know `x*` provably needs `Omega(n^2 log(1/eps))` leaves on
  this family (Proposition A.6). The proven single-tree bound overtakes
  computed certificates only from `n = 29`.
- *Fix.* After "on the same families with the same relaxations;" insert:
  "these certificates exist and are built around x*; an algorithm that does
  not know x* (Theorem A.5) needs O(n^2 log(n/eps)) leaves here, still
  polynomial, and provably Omega(n^2 log(1/eps)) for its level-synchronous
  rule; the proven single-tree bound overtakes computed certificates only
  from n = 29, so at practical sizes the separation is qualitative;".

**S4. "Three remedies, each proved to avoid the exponential".**
- *Location.* `SYNTHESIS.md`, lines 158–163.
- *Problem.* Clique-wise PSD cuts are proved exact only for `kappa = 0`.
  For `kappa = 0.1` the note gives no result, and default SCIP still grows
  by 2.1–2.3 per variable. The third remedy rests on the closed instances,
  which is computation, not proof.
- *Fix.* Replace the bullet with:
  > For solvers this suggests three remedies: decomposition-aware search
  > (proved on the path family, Section 2); consistency-strengthened
  > relaxations (clique-wise PSD cuts are proved exact for the convex
  > variant kappa = 0 only; sparse moment hierarchies with bag-uniform error
  > in the September 28 program); and tree Lagrangians with good
  > multipliers plus exact treatment of the few nonconvex windows
  > (supported by the closed instances of Section 5, not proved).

**S5. Open questions are out of date.**
- *Location.* `SYNTHESIS.md`, lines 405–416.
- *Problems.*
  - "data suggest about 2 per variable" is contradicted by the note, which
    reports 2.7–3.5 per variable for termwise B&B. The face-exact recheck
    said grid optima "cannot suggest a lower base".
  - "(lower half proved)" contradicts Theorem B.2. The lower half holds
    only with a `w`-dependent power of `|T|` and fails with a fixed-degree
    polynomial.
  - The adaptive algorithm without `x*` is now Theorem A.5.
  - Dense coupling is treated in the coupling note.
- *Fix.* Replace the section with:
  - A single-tree lower bound with a good base that is robust to how the
    objective is split, for problems nonconvex away from the minimizer (the
    split-robust method cannot exceed about 1.063 per variable).
  - The right base in Theorem 1 (termwise B&B grows 2.7–3.5 per variable;
    Conjecture 5.4 proposes `c 2^n`; grid optima are upper bounds) and a
    `log(1/eps)` factor with a good base.
  - An algorithm without knowledge of `x*` that matches Theorem 3.4; the
    level-synchronous algorithm pays `|T|^{(w+1)/2}`, and this is tight for
    it.
  - The upper half of the covering characterization beyond one separator
    (Conjecture B.5); the lower half holds with a `w`-dependent power of
    `|T|` and fails with a fixed-degree polynomial.
  - Dense coupling: whether the depth factor is necessary; an adaptive
    algorithm; a general lower bound for lifted certificates.
  - Window exactness at switches as a theorem; a transfer theorem for local
    calibrations; several switches; singular arcs; state constraints.
  - Closing waterno2, ann_cumene_tanh and eg_*.

**V1. The closing's verification paragraph overstates the process.**
- *Location.* `closing-research-results.md`, lines 106–114.
- *Problem.* The paragraph says every substantive correction was rechecked
  and that fix-and-confirm loops ran "until the confirmer found no
  remaining issue".
  - Three revisions were never rechecked:
    - decomposition Section 8.1, which includes the base-rounding fix (the
      note's header says so);
    - face-exact Section 13, item 5 (there is no confirmation file);
    - scaling-study Section 9, which replaced the prototype's rounding
      argument (no review covers it).
  - The chains in Section 4 end with items that were neither applied nor
    declined. Root edits exist in only four notes.
- *Fix.* Either apply the Section 4 items and obtain a confirmation of
  decomposition Section 8.1 and scaling-study Section 9, or replace the
  sentences with:
  > Most substantive corrections were rechecked by a fresh agent.
  > Exceptions: the decomposition note's Section 8.1 fixes (including the
  > base rounding), the face-exact note's post-recheck fixes (Section 13,
  > item 5), the scaling study's revision (Section 9, including the
  > prototype's rounding argument) and the root-applied wave-3 corrections.
  > Minor items from the last confirmation of the coupling, calibration,
  > bang-bang n ≥ 2, RLCT, pindyck, powerflow0039 and wave-3 chains were
  > neither applied nor declined; closing audit B lists them.

## 4. Review issues never resolved or declined

I checked every chain. These chains are closed, with fixes applied or
explicitly declined:
- face-exact (the recheck's fixes are in Section 13, item 5; not
  re-confirmed);
- decomposition-adaptive (final: verified);
- consistency (root edit applied);
- robust-lb (final: no remaining problem);
- the bang-bang report (the r2 nit applied by root edit);
- the bound audit (final: verified);
- the first-wave, cops, waterno2 and wave-2 small verifications;
- the computation review (optional items explicitly not adopted);
- the refusals in the nondyadic confirmations.

The following chains are open.

**U1. coupling-recheck.md, M1–M8.** None was applied or declined; the root
log calls this recheck "verified without changes". The header of
`theory-coupling/coupling.md` (lines 5–8) still says the revision "has not
been rechecked".
- Line 48 still says convex costs "change the constant". M2 shows the
  factor is about `n^{-k/2}`.
- Line 1162 has 0.61–0.66; it should be 0.61–0.65.
- Lines 1120 and 1147: `1.73` should be `>= 1.729`.
- Line 1058: "for `n <= 7`" should be "for `3 <= n <= 7`".
- Line 1188: the model-of-computation wording (M7).
- Line 1260: cites Theorem 5.1(c) for the lifted certificate, which is
  part (d).
- Lines 1454–1455: the open counts 17 and 14 are not printed by any saved
  script (M8).
- Proposition 2.6(c) should say "global minimizer" (M3).

*Fix:* apply the recheck's "Suggested edits" 1–7 as worded there. Update
the header, and update the [K] citation, which still says "under
revision".

**U2. recheck-calibration-confirm.md, Section 3, items 1–4.** None was
applied or declined. The header of `theory-calibration/scouting.md`
(lines 4–12) still says the second revision "has not been rechecked".
- Item 1 matters for honesty: Summary item 4 (lines 103–107) states the
  fixed-duration window as fact, although it is conditional on
  Corollary 4.3.

*Fix:*
- Summary item 4: "under the assumptions of Corollary 4.3, the costate
  calibration fails on a time window of fixed duration, that is
  Theta(1/h) stages".
- Lines 1093–1098: "discrete states and controls are interior".
- Remark 5.2(e): "formal leading-order derivation", with the condition
  `K(T) < 0` and the binding stage near `T`.
- Optional:
  - "linear-size certificate, `O(N log N)` check" at lines 151, 336
    and 1480;
  - "when e_h = O(h)" in Section 10, item 6;
  - mention the transversality condition at line 634.
- Header: cite the confirmation.

**U3. ext-bangbang-n2-confirm.md, remaining items 1–10.** None was applied
or declined. The header of `theory-bangbang/extension-n2.md` still says
"the revision has not been re-checked independently".
- Item 1 matters for honesty: the bold "Consequence" (line 618) rests on a
  floating-point blow-up, and the sentence does not say so.
- Item 6: the journal version of Noble–Schättler exists (J. Math. Anal.
  Appl. 269 (2002) 98–128), but lines 1169 and 1282 say it "was not
  located".
- The Section 9 table is broken (lines 1043–1048).

*Fix:* apply items 1–10 as worded in the confirmation:
- the float caveat on the bold "Consequence" and the Section 4 bullet;
- delete the stray table header in Section 9;
- "m_t ≥ 0.44" at line 706;
- the `a_t` order in Proposition 12;
- "(G) with ε = 0 at every t ≠ τ" at lines 965 and 1197;
- the Noble–Schättler citation;
- a sentence that the pre-τ Lyapunov failures come from unreachable box
  states;
- the failed integration at line 556 and the Section 10 attribution;
- the wording of Theorem 1, step 1;
- the Maurer–Pickenhain title;
- the header.

**U4. rlct-recheck2.md, W1–W4 and the optional O1–O2.** None was applied or
declined; the root log calls this recheck "verified without changes". The
header of `rlct/rlct-node-complexity.md` (lines 3–7) says Section 11.1
"has not been re-reviewed". The status rows at lines 130 and 133 credit
the first recheck with confirming text it never saw.

*Fix:*
- W1: header and status rows: "recheck confirmed; second-round
  clarifications checked in reviews/rlct-recheck2.md".
- W2: note that the three-route agreement was checked at 1e-8 only.
- W3: line 1326: "after the H quadrature was fixed (recheck item R5)".
- W4: record one command at lines 1317 and 1466, and write "the other
  instances of Table 5.2" at line 1259.
- O1 and O2 are optional.

**U5. pindyck-review.md, Section 8, issues 1–5.** None was applied. In
`open-instances-wave2/small/pindyck-extension.md` the header (lines 3–6)
and Section 6 (line 303) still say the extension has not been reviewed.
- Issue 2 matters for honesty. Lines 249–253 claim that no entrywise
  interval method "over that box can succeed". report.md Section 7
  contradicts this: that method certified `p* ± 10`. The reviewer could not
  reproduce the supporting numbers, and their script was not kept.

*Fix:*
- Line 16: "gap ≤ 5.44e-14 (≈ 5.43e-14)".
- Lines 249–253: "Over the full price box [0, pmax], the λ_max(mid) +
  ρ(rad) test fails on the entrywise hull of sampled Hessians when corners
  are sampled (not part of the proof; the sampling script was not kept)."
- Line 283: "mpmath's to_float truncates toward zero; every conversion is
  followed by a one-ulp outward step or has ample slack".
- Add the uniqueness-radius step (radius ≤ 3.7e-13).
- Stop the script from overwriting its stored log.
- Header: "independently verified (reviews/pindyck-review.md)".

**U6. powerflow0039-review.md, Section 7, issues 1–3.** None was applied.
The header of `open-instances-wave3/powerflow/extension-report.md`
(lines 3–5) says "Not independently reviewed".

*Fix:*
- Line 37: give the tight-tolerance diagnostic value, or state the 1.1e-3
  error and that the angle rows are dropped.
- Note that the FINAL line of the log came from an earlier script version.
- Line 102: "3.3e-3 below obj(p1)".
- Update the header.

**U7. The wave-3 verification's corrections.** Correction 6 (the closed
volume is 40.07%) was not applied: line 289 of
`open-instances-wave3/report.md` still says 39.7%.
- Section 9, item 3 still says the extension "is under verification"; it
  was verified in powerflow0039-review.md.
- The Summary (lines 41–45) still reports 0039p and 0039r as not closed,
  with no pointer to the extension.
- Section 9, item 1 says "the Δ argument verified". The verifier wrote "Δ
  logic sound but not recomputed".

*Fix:*
- Line 289: "40.07% of the volume closed at the end of the run (39.7% at
  3399 s)".
- Section 9, item 3 and the Summary: point to the extension and its
  review.
- Section 9, item 1: "Δ logic checked but not recomputed; an independent
  bound that needs no Δ confirms the dual bounds".

**U8. Decomposition Section 8.1 was never rechecked.** The header of
`theory-decomposition/decomposition-certificates.md` (lines 4–20) says so.
It also still says Section 8.4 is unrechecked, although
decomposition-nondyadic-confirm-r3.md checked it. The note still calls an
adaptive algorithm "open" or "sketched only" (Summary, status row
"Section 3.4", Section 6 item 3), with no pointer to Theorem A.5 of
extension-adaptive.md.

*Fix:*
- Update the header: "r3 checked Section 8.4; the fixes of Section 8.1
  have not been rechecked".
- Obtain a confirmation of Section 8.1, or record the gap in the closing
  record (see V1).
- Add "An adaptive algorithm with size O(|T| (C sqrt|T|)^{w+1}
  log(|T|/eps)) is proved in extension-adaptive.md (Theorem A.5); matching
  Theorem 3.4 without x* remains open" in the three places above.

**U9. The root log's wording.** `root-research-log.md`, lines 285–286:
"Rechecks verified without changes: coupling (second round), RLCT (second
round)" can be read as "no changes needed". Both rechecks asked for edits.

*Fix:* "Rechecks found no error in coupling (second round) and RLCT
(second round); their minor wording, labelling and provenance edits
(coupling M1–M8, RLCT W1–W4) were not applied (see
reviews/closing-audit-b.md)."

## 5. Negative and modest results

| result | preserved and labelled in its note | closing record | SYNTHESIS |
|---|---|---|---|
| coupling note | yes ("largely negative" is the root's label; the note gives the census gain 14.8% → 17.2–17.4%) | yes, "modest, largely negative" | yes, Section 3c |
| split-robust bound: tiny base | yes, "no practical weight at realistic sizes" | yes, bases 1.003–1.05 (see N2 for "computer-evaluated") | yes, detailed |
| eg_* failure | yes (wave-3 report, Section 5) | yes (line 70) | **missing** (G1) |
| pindyck: earlier failure | yes (wave-2 report, Section 7, "failure"), but no forward pointer | **not mentioned** (G3) | **not mentioned** (G3) |
| generic cell-constant DP failure; optcdeg2 block-DP failure | yes (first-wave report, Sections 8 and 10) | **missing** (G2) | cell DP kept; block DP missing |
| ann_cumene_tanh: 19% gap, verified with caveats | yes | gap and caveat missing | gap and caveat missing (G1) |
| prototype failures on probe3, heavy tails, time units | yes (scaling study, Summary and Section 7) | **missing** (G4) | **missing** (G4) |
| waterno2 not closed | yes | yes (gaps remain; open question) | yes |

**G1. SYNTHESIS: eg_* and ann_cumene_tanh.**
- *Location.* `SYNTHESIS.md`, lines 284–293.
- *Fix.* After "gave ann_cumene_tanh its first finite dual bound" insert
  "(gap 19%; verified with caveats: the full 3600 s run was not
  repeated)". Then add: "The eg_* instances failed: reduced-space interval
  branch and bound on eg_int_s and eg_disc2_s stayed below the listed
  bounds after 600–1800 s because the Gaussian-sum enclosures are too
  loose; eg_disc_s was not run."

**G2. Closing: first-wave failures and the ann_cumene_tanh caveat.**
- *Location.* `closing-research-results.md`, item 4, lines 57–80.
- *Fix.*
  - Add the bullet: "Negative: the generic cell-constant separator DP
    failed on camshape100 (cells of width O(1/n^2) needed, consistent with
    Proposition 2.6), and branching on part of the separator failed on
    optcdeg2; the working certificates used affine child bounds with good
    multipliers."
  - Line 69: after "ann_cumene_tanh has its first finite dual bound" add
    "(gap 19%; verified with caveats)".

**G3. The earlier pindyck failure.**
- *Location.* `open-instances-wave2/small/report.md`, line 25 and
  Section 7 (lines 340–398); header lines 3–4;
  `closing-research-results.md`, line 63.
- *Problem.* The failure is kept and labelled, but the report does not
  point forward. It ends "SCIP's −1437.94 remains the only listed bound".
- *Fix.*
  - Section 7 heading: add "(superseded: pindyck-extension.md closes
    pindyck; verified in ../../reviews/pindyck-review.md)".
  - Table row: add "see pindyck-extension.md (closed)".
  - Header: "independently verified (Section 11)".
  - Closing line 63: replace "pindyck" with "pindyck (after an entrywise
    interval-Hessian attempt failed; wave-2 report, Section 7)".

**G4. The prototype's failures.**
- *Location.* `closing-research-results.md`, lines 89–92; `SYNTHESIS.md`,
  lines 233–238.
- *Fix.*
  - Closing: replace "solves 8192-variable instances" with "solves
    8192-variable instances of the amp 0.2 family (on probe3 one of five
    seeds exceeds the cap at n = 2048 and no setting solves n = 8192; bounds
    rest on a rounding analysis, not interval arithmetic)".
  - SYNTHESIS: extend "Limits" with "; failures and heavy tails on probe3
    (amp 0.3); prototype times are wall-clock under load, SCIP times CPU".

**G5. Rocket LINDO bounds.**
- *Location.* `SYNTHESIS.md`, lines 272–275.
- *Fix.* Replace "(methanol50, rocket100/200/400)" with "(methanol50 by
  1.2%; rocket100/200/400 by about 1e-7 relative, below MINLPLib's 1e-6
  tolerance and outside the audit's 19 pairs)".

## 6. Out-of-date status lines (low priority)

These lines say a result is unchecked when a later confirmation exists.
They understate the verification rather than overclaim, but they mislead
readers of the individual notes.

- **`theory-robust-lb/robust-lower-bound.md`, lines 13–14.** It says "The
  third revision has not been rechecked". robust-lb-confirm-r1.md
  confirmed it with no remaining problem.
- **`theory-bangbang/report.md`, lines 8–9.** It says "that third revision
  has not been re-checked independently". bangbang-root-fixes-confirm-r2.md
  confirmed it. The root edit at line 972 cites
  bangbang-root-fixes-confirm.md; the source was -r2.md.
- **`open-instances-wave2/waterno2/report.md`.** The header says "not
  independently reviewed". The verification section says "The other 48
  periods ... were not rechecked"; waterno2-recheck.md later certified all
  63 (with code shared with the first verifier).
- **`open-instances-wave2/cops/report.md`, Section 7.** It says
  "catmix400/800 duals were checked by code reading only";
  catmix-recheck.md later recomputed them independently.
- **`open-instances-wave2/small/report.md`, header.** It says "Not yet
  independently reviewed"; Section 11 records the verification.
- **`README.md`.**
  - Line 19 links the bang-bang "confirmation of fixes" to
    bangbang-root-fixes-confirm.md, whose verdict is "Fixes needed". Link
    -r2.md instead.
  - Line 18 omits recheck-calibration-confirm.md.
  - Line 13 omits the three nondyadic confirmations.
  - Line 23 should say the census is "not independently reviewed".

## 7. What I did not check

- No mathematics was rederived and no computation was rerun. Every finding
  compares a statement with the note or review that supports it.
- I did not read the literature sources themselves. The attributions above
  are those that the notes, the literature audit and the reviews record.
- I did not check PROGRAM.md or the September 28 notes beyond the passages
  cited in this continuation's notes.

Commands run: `cat -n`, `sed -n`, `grep -n`, `awk` and `find` on files
under `research-20260929/`, and
`python3 -c "import math; print(math.sqrt(2*math.e/math.pi))"`. No
project-wide verification, no CI inspection, no edits, no commits.
