# September 29 continuation: results and closing record

Date: 2026-09-30 (round 4 added 2026-10-01). On 2026-09-30 the user asked to finish the current
directions and their possible extensions without starting new ones. This
record collects the results, their verification and their limits. The
[synthesis](SYNTHESIS.md) gives the full account; the
[consolidated certificate table](open-instances-summary.md) lists every
instance. Nothing in this continuation has been committed.

*Round 3 (2026-09-30).* Five open questions listed in the notes were then
followed up, within the same directions: window exactness at bang-bang
switches, singular arcs, the upper half of the covering characterization,
waterno2_06 (separator branching) and ann_cumene_tanh. Each result was
independently reviewed (the theory notes through two or three confirmation
rounds); the items below and the open questions are updated accordingly.

*Round 4 (2026-09-30 to 2026-10-01).* Five more listed open questions were
followed up, again within the same directions: an algorithm that matches
Theorem 3.4 without knowing `x*`, split-robust lower bounds on uniform
chains, certificates at bang-bang switches with `kappa_tau < 0` and several
switches, waterno2_06 with cell-dependent slopes, and the eg_* instances.
Each was independently reviewed (waterno2_06 after the round, because a
usage limit interrupted its first review); the user then asked to finish
the current work and stop.

"Verified" or "reviewed" means checked by a research agent that did not
write the material, usually with its own code; it is not journal peer
review. An unsuccessful literature search does not establish novelty; each
note states what was examined.

## Main contributions

1. **Structure and the cost of spatial branch-and-bound**
   ([face-exact note](theory-face-exact/face-exact-exponential.md),
   [decomposition note](theory-decomposition/decomposition-certificates.md)).
   - Single-tree spatial B&B with termwise McCormick relaxations needs at
     least `0.57 (5/3)^n` leaves (`eps <= 1e-4`; with bound tightening,
     leaves plus `2n` per round) on a path-structured family with a unique
     nondegenerate interior minimizer (every branching rule, node order,
     incumbent and same-relaxation tightening). The bound is about fixed
     termwise relaxations: it also holds for a convex QP written with
     separate bilinear terms.
   - Decomposition certificates (cells on separators, affine Lagrangian
     child minorants, leaf covers of bags) exist with size
     `O(|T| C^{w+1} log(|T|/eps))` under quadratic growth, Lipschitz factor
     gradients, vertex-vanishing relaxation error and a cell-width
     condition (the construction is centred at `x*`), so treewidth replaces
     dimension; constant child bounds provably need `Omega(eps^{-1/2})`
     cells (proved for a child of the root with a one-dimensional
     separator); width lower bounds hold for every tree decomposition of
     separable block families; an adaptive algorithm without knowledge of
     `x*` (with monotone relaxations) achieves
     `O(|T| (C sqrt|T|)^{w+1} log(|T|/eps))`, and its extra factor is real
     for this level-synchronous algorithm.
   - Round 3 ([covering note](theory-decomposition/covering-upper-half.md)):
     a graded exact split (`theta_e = (2E_e+1)/(2n)`) discounts each edge's
     error by its own separator margin `w_e/(2n)` (the factor is optimal
     for bounds of this form); with a one-dimensional kink bound (Lemma 2,
     now sharp; Theorem 3 uses its earlier constant 8) it settles the upper half of the covering characterization in the
     exact-bag model for trees with one-dimensional separators (cells per
     separator at most `O(n log)` times the covering number; upper bound
     only). Refinement driven by one-edge band brackets can stall (an
     explicit two-edge example). For decomposition certificates only a
     partial result holds: aligned certificates satisfy a proved
     sufficient condition (Proposition 5), but the resulting size bound is
     a sketch (at best reading (R2)); reading (R1) stays open.
   - The separation is rigorous but relative to fixed termwise relaxations
     and a fixed factorization: freely chosen splits make per-bag
     relaxations exact on trees, and a split-robust lower bound exists only
     qualitatively (bases about 1.003 proved analytically and 1.05
     computer-evaluated; the method cannot exceed about 1.063; restricted
     split classes on a gadget family).
   - Round 4 ([adaptive-matching note](theory-decomposition/adaptive-matching.md)):
     for path decompositions (any width) with `∇F(x*) = 0`, the
     graded-refinement algorithm GR, which knows neither `x*` nor the
     constants and uses no local solver, certifies `eps` with
     `|T| C^{w+1} log(|T|/eps)` boxes (times one more logarithm for unknown
     constants), the form of Theorem 3.4 (Theorem 2, proved; the proved base
     is quadratic in `M_a/c_g` and its constants are numerically vacuous;
     in floating-point runs it needs 12.1k–17.1k boxes per bag, flat in `n`
     up to 256). The key is a localization lemma for minimizing
     configurations of the relaxed dynamic program; trees remain open
     (Conjecture 7). The bound-driven rule of the covering note provably
     needs `Omega(n^{3/2} log(1/eps))` cells on a quadratic path.
   - Round 4 ([robust-chains note](theory-robust-lb/robust-chains.md)):
     on uniform chains with symmetric couplings and a nondegeneracy
     hypothesis, the balanced split has certificates of size independent
     of `n`, so no split-robust lower bound growing with `n` exists there
     for split classes that contain the balanced split (the unsplit
     factorization and `b_d` relative to the gadget base split are not such
     classes; the exponential bound of the face-exact note's Theorem 2 is then a
     property of the unsplit factorization); a chiral chain gives a
     split-robust exponential bound without gadgets for factorable class-(a)
     splits, with tiny bases (about 1.001–1.009 proved analytically, 1.023
     computer-evaluated in floating point); a meaningful base was not
     achieved.
   - Prior work: cluster-problem estimates (Neumaier 2004;
     Wechsung–Schaber–Barton 2014); the repository's September 28 lower
     bound for relaxations with gap at least `alpha q_B` (constrained note,
     Theorem 3.1); MILP B&B lower bounds and separations at treewidth 2
     that rely on ties (Basu et al. 2023; Dey–Shah 2022); discrete AND/OR
     and BTD search; worst-case bounds `(C n/eps)^{O(w)}` (Zhang–Sun 2022;
     Bienstock–Muñoz 2018); Berenguel et al. (2013) as the algorithmic
     precursor for one shared variable; Robertson–Cheng–Scott (2025) for
     the first-order copy error; Griewank–Toint (1984) for the chordal
     escape. Not found in the literature audit: the face-exact lower bound
     at a unique nondegenerate minimizer, the instance-dependent
     certificate bound (decomposition note, Theorem 3.4) and the slope lower
     bound. The
     reviewers rate the separation modest and meaningful for solvers only
     qualitatively.
2. **Consistency relaxations** ([note](theory-consistency/consistency-relaxations.md)).
   For one separator the relaxation gap equals exactly twice the sup-norm
   distance from the split class to the band of exact splits; on trees it is
   sandwiched by edge distances (the per-edge version is false); kinks force
   `Theta(1/n)` for degree-`n` polynomial classes. Proposition 5.1 gives an
   exact criterion for when affine splits suffice. For the September 28
   sparse-moment rates, the lower bounds already followed from identities
   proved there; this note evaluates the approximation errors (constants
   about 8x and 12x higher, asymptotic, floating point). Known in
   substance: the duality, the one-sided bound (de Farias–Van Roy), its
   positive-width form (Grimm–Netzer–Schweighofer; Korda–Magron–Ríos-Zertuche),
   the zero-width identity (Han–Jiao–Weissman). New as far as found, and
   elementary: the exact identity, the tree lower bound and
   counterexample, the kink bound, the shell count.
3. **Discrete calibrations and bang-bang transcriptions**
   ([calibration note](theory-calibration/scouting.md),
   [bang-bang note](theory-bangbang/report.md),
   [n ≥ 2 extension](theory-bangbang/extension-n2.md)). Every certificate
   that closed a transcribed control or variational instance here is a
   discrete calibration (classical framework). Not found stated in limited
   searches, and elementary: a transfer theorem (an exact strict `C^4`
   continuous calibration with compact state and control sets, interior
   optimal controls and uniformly convergent Euler KKT points gives exact
   certificates for all fine Euler transcriptions; bang-bang arcs, singular
   arcs and state constraints are outside it); the window law (under the
   hypotheses (W1)–(W5) of the bang-bang note's Theorem 2.3,
   non-tangential calibrations fail for a fixed duration around a regular
   switch and tangential ones on `O(1 + e_h/h)` stages); every `C²`
   calibration exact on the trajectory is tangential (the no-jump case of
   Osmolovskii–Maurer's Riccati test); in dimension `n ≥ 2`, in the local
   formulation, existence is decided by one number `eta_L` (this answers
   the continuous existence question only and does not feed into the
   transfer theorem, whose global form can fail even when `eta_L > 0`), and
   the "no conjugate point" reading of the earlier conjecture is false.
   Related prior work: Maurer–Pickenhain (1995), quadratic verification
   functions via Riccati equations.
   - Round 3, window exactness
     ([note](theory-bangbang/window-exactness.md)): the window-exactness
     assumption of the bang-bang note's Theorem 4.1 is decided by the sign
     of the switch self-curvature `kappa_tau = b(x*(tau))^T w`, shared by
     every `C²` calibration exact on the trajectory. Under Theorem 4.1's
     hypotheses plus an exact terminal term and `b(x*(tau)) != 0`:
     `kappa_tau > 0`: no window is needed (and `e_h <= c_* sqrt(h)` with a
     specific small `c_*` suffices); `kappa_tau = 0` (with `e_h = O(h)`):
     one `O(1)`-stage window is exact; `kappa_tau < 0`: on grids with a
     fractional stage every window of `o(1/h)` stages falls short by order
     `h^2` for the transferred calibration (for LQ data, for all quadratic
     families with the discrete costate slopes that are exact over
     `R^n × U` after the window and at the terminal; families exact only
     over the state boxes are not covered). `kappa_tau` is, up to a factor, the
     switch cross term of the Osmolovskii–Maurer quadratic form; its role
     here was not found stated in short searches.
   - Round 3, singular arcs ([note](theory-bangbang/singular-arcs.md)):
     exact `C²` calibrations are tangential along a singular arc, which
     implies Goh's condition, and imply Kelley's condition (classical
     conditions in calibration form); for Euler, the sign of `b^T w`
     decides whether tangential families certify fractional stages
     (`b^T w > 0`, given `e_h = o(sqrt(h))`) or whether, for families with
     Hessians changing by `O(h)` per stage, every fractional stage fails
     and a smooth KKT point is a saddle (the optimum chatters in E2 and
     catmix; observed, not proved); an accessory symbol explains the
     chattering of the COPS catmix transcription (heuristic: the chattering
     gain agrees within 3% against a smooth reference with free junction
     stages, and the most negative Hessian eigenvalue there lies within
     0.1% of the finite-section estimate; at the oscillating KKT point (the
     saddle) that eigenvalue lies 21% below the symbol minimum, and the gain
     comparison depends on the reference by up to a factor 3.2; no
     rigorous catmix certificate this way).
   - Round 4, `kappa_tau < 0` and several switches
     ([note](theory-bangbang/kappa-negative.md)), for LQ-structured data:
     node-specific `kappa`-limited calibrations give only
     `epsilon`-certificates, with `Theta(log(h^2/epsilon))` nodes (leading
     order; lower bound for a stated family class); lifted calibrations
     that treat the fractional control as a parameter give an exact bound on
     a central node (proved under a neighbour-margin condition and
     `e_h = o(sqrt h)`) and exact rational certificates of the discrete
     optimum on every documented grid of the scalar toys (float screening
     only on the two-state example A−; that few outer nodes suffice is
     heuristic); the discrete optimum does
     not chatter at leading order. Theorems A and B extend switch by switch
     to several switches (sketch level); a tangential calibration across
     close switches needs a new coupling condition; with terminal rows the
     terminal condition is needed only on `ker C` (with the fixed-endpoint
     rate assumed).
4. **Certificates for open MINLPLib instances and a validity audit**
   ([summary](open-instances-summary.md), [audit](bound-audit/audit-report.md)).
   - 31 instances listed as open were closed for the models as written:
     lnts50–400, dtoc5, camshape100–800 (exact optima), lukvle10, optcdeg2
     (to 9.0e-16), hvycrash (objective constant on the feasible set),
     ex6_2_7, ex6_2_5 (an ε-global method, McDonald–Floudas 1997, very
     likely solved them; not confirmed), etamac, pricing050, chain50–400,
     catmix100–800, powerflow0030p/0039p/0039r, pindyck (after an
     entrywise interval-Hessian attempt failed; wave-2 report, Section 7),
     and in round 4 eg_int_s, eg_disc_s and eg_disc2_s (to a relative 1e-9
     against exactly feasible points; second-order Taylor models that keep
     the signed cancellation of the Gaussian-kernel rows; eg_int_s had been
     solved in floating point by SCIP 8.1 in the literature).
     Improvements over the best single-solver bounds are marginal for
     camshape100 and lnts50. For lnts50–400, dtoc5, lukvle10, chain50–400
     and powerflow0030p/0039p/0039r the primal side is a point feasible to
     row violations of 1e-20 to 8e-12; closure is measured against its
     value, and no exactly feasible point was constructed.
   - The six KAN instances' intended network relaxations are certified to
     about 1e-10, and their OSIL models are proved to have no exactly
     feasible point; waterno2_06–24 duals rise by factors of 1.6–6.2 (gaps
     4.9–10.8% remain), and in round 3 separator branching raised
     waterno2_06 from 263.735099 to 272.584700 (gap 7.26% → 3.78%; all
     8,958 pair bounds re-bounded independently); ann_cumene_tanh has a
     finite dual bound, first −4024.495 (gap 19%; verified with caveats),
     then in round 3 −3386.5403 (gap 0.194%; independently re-certified);
     in round 4 cell-dependent slopes raised waterno2_06 to 278.230573
     (gap 1.67%; all 49,315 pair bounds re-bounded independently). The
     eg_* instances, which failed in wave 3, were closed in round 4 (above).
   - Negative: the generic cell-constant separator DP failed on camshape100
     (cells of width `O(1/n^2)` needed, consistent with Proposition 2.6),
     and branching on part of the separator failed on optcdeg2; the working
     certificates used affine child bounds with good multipliers.
   - 19 listed solver dual bounds on 15 instances are proved invalid by
     exactly feasible points (11 beyond MINLPLib's 1e-6 convention, 7 of
     them below common 1e-4 gap tolerances; 8 at tolerance scale). SCIP
     10.0.2 returned wrong optimal values on waterno2 period subproblems
     (an invalid in-tree bound reduction; not reported upstream). Several
     listed primal values are tolerance-feasible points below exact optima.
   - The mechanisms are classical (Lagrangian and SDP duality,
     Mangasarian-type sufficiency, Sturm comparison, tangent-plane tests,
     calibration, concavity certificates, exact identities); the
     contribution is the certificates and the interpretation (not tested
     experimentally) that relaxations, not branching, were the obstacle.

## Secondary and supporting results

- [RLCT note](rlct/rlct-node-complexity.md): for `C^{1,1}` objectives and
  relaxations with an alphaBB-type quadratic gap, node counts of spatial
  B&B lie within factors that do not depend on `eps` of a face-stratified
  integral (the factors depend on `n` and instance constants; the upper
  constants are exponential in `n`); for analytic objectives with interior
  minimizers the exponent is `n/2 − lambda` (real log canonical
  threshold), with a counterexample at boundary minimizers and exponents
  from Watanabe's learning coefficients.
- [Computation](computation/scaling-study.md): SCIP 10 node counts grow
  about fivefold per two added variables on path-structured instances; a
  chain dynamic-programming B&B with valid bounds solves 8192-variable
  instances of the amp 0.2 family (on probe3, amp 0.3, one of five seeds
  exceeds the pair cap at `n = 2048` and no setting solves `n = 8192`;
  bounds rest on a rounding analysis, not interval arithmetic).
- [Census](treewidth-census/census-report.md): 13.6% of large nonconvex
  MINLPLib instances have small factor-incidence width and 62.7% small
  nonlinear-term width (small means a heuristic width upper bound of at
  most 12; a root computation, not independently reviewed; it does not
  show that width causes the difficulty). In MINLPLib's listing before this work,
  constant-width families (waterno2, camshape, lnts) became open as they
  grew; lnts and camshape have since been closed (in our reading, the
  obstacle was the relaxation).
- [Coupling note](theory-coupling/coupling.md) (modest, largely negative):
  dense linear rows raise the small-width share only from about 15%
  (baseline 14.8%: it first removes objective and objective-defining rows
  and takes the smaller of two width bounds, hence above the census's
  13.6%) to 17%; Shapley–Folkman bounds the gap, not the certificate.
- [Literature audit](literature/decomposition-bb-prior.md): prior work on
  AND/OR search, MILP B&B separations, two-stage and nested decomposition,
  Bienstock–Muñoz, and an ETH obstruction to `poly(n) g(w, eps)` bounds.

## Verification

The [README](README.md) links each note's reviews. Every extension and
most second-round revisions were checked by a fresh agent; the completion
phase ran two workflows (`finish-sept29-continuation`, 28 agents;
`finish-round2`, 24 agents) that closed the remaining verification gaps
(all waterno2 periods, catmix400/800, the unchecked audit pairs). Not
rechecked: the decomposition note's Section 8.1 fixes (including the base
rounding), the face-exact note's post-recheck fixes (Section 13, item 5),
the scaling study's revision (Section 9, including the prototype's
rounding argument), and the root-applied wave-3 corrections. The last
checks of the calibration, coupling, RLCT, bang-bang `n ≥ 2`, pindyck and
powerflow-extension notes raised minor wording items. The closing revision
(2026-09-30) applied them in the notes, with a dated entry in each, and
updated several note headers that predated their latest review; it left
unapplied only script changes (coupling M8 and the `jn_lifted_cert.py`
docstring label; the pindyck script's log overwrite) and the optional RLCT
item O3. These root edits have not been rechecked. Reviews found and removed errors including: two false
statements in the root's own program page (an alphaBB growth claim and a
"solved at the root" claim), a false premise about unique interior
minimizers, leaf counts made too small by uncertified QP-solver bounds in a
first version of the toy B&B, a rounded-up separation base that made a
uniform statement false for huge `n`, a boundary-minimizer counterexample
to the RLCT conjecture, wrong citations in the bang-bang note, a missing
hypothesis and a compactness counterexample in the transfer theorem, the
exact infeasibility of the KAN models, and dropped touching pairs in the
certificate code.

Round 3 ran one workflow (`extensions-round3`, 26 agents): each task had an
author, an independent reviewer and, where fixes were needed, alternating
fix and confirmation agents until a confirmation returned "verified"
(window exactness and singular arcs after three confirmation rounds, the
covering note after two; the waterno2 and ann results were verified at the
first review, with full independent re-bounding and re-certification). The
root then applied the reviewers' remaining minor wording items and three
changes to the bang-bang note that the window-exactness work found (a
factor-2 slip in the proof of Theorem 4.1, fixed with `mu' < mu`; a
missing hypothesis: Theorem 4.1's conclusion `B = f*` also needs an exact
terminal term, which (H1)–(H5) do not contain; a stage-only qualifier on
"the tangential family fails on none"; the terminal hypothesis was added
to the theorem's statement only after the check below found it missing). A two-agent workflow
(`round3-root-edits-confirm`) checked these root edits and the integration
below; the root applied its findings (including removal of an unsupported
agreement figure for catmix and several dropped hypotheses). The fixes
after that check were confirmed by a second check
(`round3-root-fixes-confirm-r2`), which raised two minor and six optional
wording items; the root applied them, and a third check
(`round3-root-fixes-confirm-r3`) returned "verified" with optional nits
only, which the root then applied (record-keeping and wording; not
rechecked).

Round 4 ran `extensions-round4` (26 agents) with the same structure. A
usage limit stopped the first review of the waterno2 cell-slopes work; it
was rerun in `finish-round4`, which also applied the remaining minor items
of the eg, robust-chains and `kappa < 0` notes with fresh confirmations,
and `finish-round4-final` applied the waterno2 review's seven wording and
bookkeeping items and the remaining optional nits, each with a
confirmation. The optional nits of those last confirmations
(`waterno2-cellslopes-confirm-r1.md` Section 3; `round4-nits-confirm.md`
Section 4, items 1–3) were left unapplied. The root integrated round 4
into this record, `SYNTHESIS.md`, `open-instances-summary.md` and the
READMEs; a two-agent independent check (`round4-root-integration-check`)
found one error (a computer-evaluated base called proved) and several
dropped qualifiers, which the root fixed (see `root-research-log.md`; the
fixes were not rechecked).

Targeted commands run by the root (others are recorded in each note):

```
python3 research-20260929/treewidth-census/census.py k 12   # k = 0..11
python3 research-20260929/treewidth-census/analyze.py
python3 research-20260929/treewidth-census/families.py
python3 research-20260929/scratch/chain_boxqp.py 10 20 40 80
python3 research-20260929/scratch/probe2.py n 1e-4             # n = 2..6
python3 research-20260929/scratch/probe3.py 1e-4 0.1 2 4 6 8 10 12 16 20
```

For the closing revision the root ran two inline Python checks: a link check
over the edited documents (603 links, all resolve) and exact-rational
checks of the corrected displayed values (outward rounding of the chain,
catmix and lnts bounds; the lnts gaps; the waterno2 ratios; the optcdeg2
bracket; the PROGRAM.md node ratios). The ex6_2_5 and lukvle10 displays in
`open-instances-summary.md` were then checked against their certified
interval ends, recomputed by the two scripts in
`reviews/closing-confirm-r2-checks/`. No project-wide checks were run and CI
was not inspected.

## Limits

- The single-tree lower bounds concern fixed termwise relaxations; SCIP's
  PSD-minor cuts and convexity detection on aggregated expressions escape
  them, and the proven crossovers are at large `n`.
- The single-tree lower bounds do not cover MUSE-BB-type multisection in
  their cost measure, branching on lifted variables or objective-cutoff
  propagation.
- The decomposition upper bounds need quadratic growth and are existence
  results centred at `x*`. Their constant `c_g` is global: a second local
  minimizer within `delta` of `f*` at distance `D` makes the base
  `(C M_a D^2/delta)^{w+1}`, no better than the worst case when
  `delta ~ eps`. The characterization by covering numbers is only partly
  settled.
- The certificates are instance-specific and some rely on floating-point
  interval arithmetic with documented assumptions (IEEE rounding, mpmath
  intervals); the eg_* bounds rest on a hand-derived floating-point error
  analysis, reproduced box for box by an interval model for eg_int_s,
  eg_disc_s and the optimum-containing part of eg_disc2_s, while the other
  seven eg_disc2_s parts were re-certified independently only on a sample
  of leaves (110,676 of 979,044); KAN claims concern a relaxation of
  exactly infeasible models;
  13 of the 31 closures are measured against tolerance-feasible primal
  points.
- Computations use one solver (SCIP 10) and floating-point prototypes; the
  census is a root computation with heuristic widths and was not
  independently reviewed.
- The O(h) discretization rate needed by the window law is established for
  linear problems but unverified for nonlinear ones; window exactness is
  proved for `kappa_tau >= 0` (with `b(x*(tau)) != 0` and rate hypotheses;
  `B = f*` also needs an exact terminal term) and fails for
  `kappa_tau < 0` on grids with a fractional stage, within transferred
  calibrations; there no certificate with windows of fixed duration was
  built.
- Novelty assessments are provisional.

## Open questions left by this continuation

- A single-tree lower bound with a good base that is robust to how the
  objective is split, for problems nonconvex away from the minimizer
  (round 4: none growing with `n` exists for symmetric uniform chains under
  a nondegeneracy hypothesis, for split classes that contain the balanced
  split; tiny bases for chiral chains).
- An algorithm without knowledge of `x*` that matches Theorem 3.4 on
  branching tree decompositions and without `∇F(x*) = 0` (solved for path
  decompositions with `∇F(x*) = 0` in round 4), with practical constants.
- The upper half of the covering characterization for decomposition
  certificates in reading (R1) and for separators of dimension 2 or more
  (settled in round 3 for the exact-bag model on trees with
  one-dimensional separators).
- Certificates at bang-bang switches with `kappa_tau < 0` beyond LQ data,
  and a proof that lifted certificates need only a few outer nodes; a
  transfer theorem for local calibrations; asymptotics for close switches;
  state constraints; for singular arcs, a global catmix calibration and the
  discrete rate near junctions. (Round 3 answered the window-exactness
  question under the hypotheses of the bang-bang note's Theorem 4.1 plus
  an exact terminal term and `b(x*(tau)) != 0`, within transferred `C²`
  calibrations.)
- Closing waterno2 (waterno2_06 is at 1.67% after cell-dependent slopes;
  09–24 were not attempted with separator branching) and ann_cumene_tanh
  (the remaining boxes lie along a nearly flat constraint surface).
