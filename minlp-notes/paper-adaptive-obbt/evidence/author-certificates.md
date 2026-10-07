# Author report: certificates, cutoff, and residual sections

Lane: certificates. Files owned and written: `sections/certificates.tex`,
`sections/cutoff.tex`, `sections/residual.tex`. No other manuscript file was
edited. All three files contain complete text and proofs; no placeholders
remain.

## Inputs read

- `AGENTS.md`, `evidence/BRIEF.md`, `evidence/INTEGRATION-NOTES.md`,
  `evidence/literature-audit.md` (preliminary), `evidence/bibliography-aliases.json`.
- October study: `theory/remaining-benefit.md`, `document/certificates.tex`,
  `document/foundations.tex`, `document/constraints.tex`,
  `document/implementation.tex`, `document/evidence.tex`,
  `theory/certificates.py`, `theory/certified_driver.py`, both check scripts
  and their saved outputs, `reviews/theory-review.md`,
  `reviews/check_theory_review.py`, and the campaign solver source (to confirm
  what the measured policy implements).
- September study: `theory.md` (stall, row condition, near-optimal hull).
- Audits and reviews: `audit-certificates.md` (complete), `audit-constraints.md`
  and `audit-rates.md` (relevant parts), `review-certificates-r1.md` (all
  rounds), `review-constraints-r1.md` (shared-section items).
- Other lanes' drafts, for labels and overlap: `foundations.tex`,
  `local-rates.tex`, `constraints.tex`, `algorithms.tex`, `experiments.tex`.

## Content and labels

`certificates.tex` (`sec:certificates`): lifted witnesses; monotonicity versus
lifted monotonicity (`ex:lambda`); reference family with a gap-form proof of
lifted monotonicity (`lem:reference-family`, `eq:mccormick-gap`); current-round
ceilings (`prop:current-round`, `ex:halving`); relaxation-sound steps, witness
pools and protection (`thm:protected`); short exact certificates for fixed boxes
(`prop:fixed-box`); combining certificates (`prop:join`); exact ceilings at the
limit (`cor:limit-ceilings`, `ex:sharp-halving`); objective ceilings
(`cor:objective-ceiling`, `ex:three-variable`); original feasible points
(`cor:original-points`); integer rounding, cuts and branching
(`prop:integer-rounding`, `ex:child`); finding versus checking
(`prop:round-check`, `ex:round-check`).

`cutoff.tex` (`sec:cutoff`): pool face threshold (`prop:face-threshold`); exact
expiry cutoff of a box (`prop:box-threshold`); mixing (`prop:mixing`,
`ex:mixing-hull`); exact pool frontier (`prop:frontier`); cutoff response and
screening thresholds (`prop:cutoff-response`, `ex:frontier`); changed boxes;
continuing versus restarting (`prop:continue`); reuse table (`tab:reuse`).

`residual.tex` (`sec:residual`): endpoint map and invariant order intervals
(`lem:invariant-interval`); remaining-movement theorem (`thm:residual`,
hypothesis `eq:matrix-lipschitz`, `eq:supersolution`, `eq:tail-bound`); least
majorant (`prop:least-majorant`); noncontracting direction (`ex:inactive`);
valid residual information (`cor:witness-residual`); Heron example
(`ex:heron`); cutoff decreases (`cor:cutoff-tail`, `prop:fixed-point-shift`);
histories (`ex:ratio`, `prop:history`); finding versus checking a matrix.

## Corrections relative to the October sources

1. **After-round residual bound.** The archived text said the after-round
   bound is `e - d_actual`, "not `e - dbar`". This is false. With `dbar >= d`
   and `dbar + M e <= e`, the exact tail after the first Jacobi round is at most
   `M e <= e - dbar`, and more generally `p_m - p_inf <= M^m e`
   (`thm:residual`). The bound concerns the exact image `p_1`, not a partially
   updated state; a one-line example shows the difference.
2. **Weaker sensitivity hypothesis.** The theorem now needs the comparison only
   for ordered pairs, `F(p)-F(q) <= M(p-q)` for `q <= p`, which a two-sided bound
   implies. Neither convexity of the region nor `rho(M) < 1` is needed for the
   trajectory bound.
3. **Objective ceiling needs only projected monotonicity.** The October text
   assumed lifted nesting with a common objective. The value ceiling
   `L(C_k) <= L(P) <= v(z)` follows from monotonicity of the projected
   objectives. Lifted monotonicity is needed only to reuse the stored lifted
   vector itself as a feasible LP point (screening, mixing, warm starts).
   `ex:lambda` gives a natural formulation (convex-combination weights, objective
   `v=s`) that is monotone but not lifted monotone.
4. **Lower bound in the objective ceiling.** The subtracted lower bound must
   bound this relaxation's value at the starting box; substituting a bound on the
   original optimum is wrong (three-variable example: relaxation value `-3`,
   optimum `0`).
5. **Cutoff threshold.** `max_W v` is a safe whole-pool threshold but not sharp.
   The exact subpool threshold is the face threshold `tau_W(P)`, and mixing
   cannot lower it for the same box. The exact compatibility cutoff of a
   prescribed box is `tau(P) = max_F mu_F(P)`, including the empty-set case.
6. **Cuts.** Preserving a certificate under an added row needs lifted
   monotonicity of the modified family plus witness satisfaction; witness
   satisfaction alone does not restore projected order.
7. **Cutoff perturbation.** The October fixed-point comparison assumed a uniform
   joint estimate in `(p,U)`. A sensitivity bound at the old fixed point alone
   suffices (`prop:fixed-point-shift`). That comparison needs `rho(M) < 1`
   (counterexample `F(s,t)=(s,t/2)`), whereas the trajectory bound after a cutoff
   decrease (`cor:cutoff-tail`) needs no spectral condition.
8. **Valid residual sources.** An exact complete sequential round's movement is
   a valid upper residual (`lem:sequential`(b)); selective, interrupted and
   outward-rounded movements are not.
9. **Infeasibility wording.** A protected box rules out emptiness of the
   relaxation cutoff sets; the October phrase about an "infeasible cutoff" was
   replaced by the statement that the pool may consist of relaxation-only points.
10. **Node scope.** An incumbent supplies a protected singleton and an invariant
    region only if it lies in the current box.

## Developments beyond transcription

1. `prop:fixed-box`: a box is fixed exactly when a witness pool exists; at most
   `2n` points suffice; for rational polytopes, rational lifted witnesses exist,
   so the exact checker is complete as a test of a prescribed box.
2. `prop:join`: union of pools certifies the hull; merging an incumbent
   singleton with a stalled box.
3. `cor:limit-ceilings`: under the foundations' closedness condition the
   Jacobi limit has a short pool and its ceilings equal the exact remaining
   movement, for Jacobi and complete sequential rounds. `ex:not-fixed` shows the
   failure without closedness; `ex:sharp-halving` shows exact ceilings without
   finite termination.
4. `prop:round-check` and `ex:round-check`: the rebuilt check after a round
   succeeds no later than the round that starts at a finitely reached fixed box,
   never succeeds for asymptotic convergence, and can fail at a fixed box
   depending on the returned optimal vertex. The text states what the check adds
   over the "no-progress round" observation and explains primal versus dual
   roles.
5. Original-point proposals (`cor:original-points`) as a solve-free discovery
   route that survives every valid reduction.
6. `prop:cutoff-response`: the pooled support is concave, nondecreasing,
   continuous, and affine between pool values; exact screening thresholds for
   future incumbents follow. `ex:frontier` computes one (threshold `5/2`).
7. `prop:continue`: resuming OBBT after a cutoff decrease never ends worse than
   restarting, and reaches the same limit under closedness.
8. `prop:least-majorant`: a supersolution exists iff the Neumann series
   converges, the series is the least majorant, and a rational weighted-norm
   certificate gives an explicit majorant.
9. `cor:witness-residual`: current-round ceilings are valid upper residuals, so
   the tail theorem can be applied without solving support problems.
10. `prop:history`: any strictly decreasing finite history is produced by both a
    stalling and a converging valid family satisfying closedness.
11. `ex:child`: the three-variable stall does not pass to the branching child
    `[0,1] x [-1,1]^2` (face value `1/2 > 0`).
12. `ex:heron`: exact error identity `G(u)-r=(u-r)^2/(2u)` proving convergence
    and quadratic rate.

## Integration notes for the root

- **Terminology** follows `foundations.tex`: "monotonicity" for
  `eq:monotonicity`, "lifted monotonicity" for lifted inclusion with a common
  objective, "fixed box". "Protected box" means a fixed box with a checked
  finite pool and threshold.
- **Labels renamed to match `constraints.tex`.** `thm:residual` and
  `eq:matrix-lipschitz` are now the labels in `residual.tex`; constraints'
  references resolve without change. The alias plan in INTEGRATION-NOTES
  (`thm:residual -> thm:residual-tail`, `eq:matrix-lipschitz ->
  eq:order-lipschitz`) is obsolete and must not be applied.
  `eq:matrix-lipschitz` labels the ordered-pair inequality; the two-sided bound
  of `thm:cover-con` implies it.
- **External labels my files use:** `sec:foundations`, `eq:validity`,
  `eq:monotonicity`, `eq:projected`, `eq:closed-family`, `lem:order`,
  `lem:sequential`, `lem:sublevel-hull`, `lem:fixed-persist`,
  `prop:fixed-limit`, `ex:not-fixed`; `sec:local-rates`, `cor:face-test`,
  `prop:quadratic-rows`, `ex:many-term`, `ex:shape-change`,
  `ex:finite-square`; `sec:constraints`, `prop:threshold-con`,
  `sec:histories-con`; `sec:algorithms`, `thm:closure`; `sec:experiments`.
  All existed at the time of the last build.
- **Overlaps.** (a) `prop:history` (general history) and constraints'
  `sec:histories-con` (`prop:histories-con` plus the small-ratio knots) cover
  related ground; `residual.tex` cites `sec:histories-con` for the explicit
  histories. If space is needed, constraints could cite `prop:history` instead
  of repeating the construction. (b) `algorithms.tex` repeats the one-round
  detection argument inside `thm:closure`(c) with its own fixed-row example;
  it could cite `prop:round-check`(b,c). (c) Constraints'
  `cor:residual-input-con` restates `lem:invariant-interval` with a cover; this
  is consistent.
- **Packages and environments used:** amsthm environments `theorem`,
  `proposition`, `lemma`, `corollary`, `definition`, `example`; enumitem
  `[label=(\alph*)]`; booktabs and array column types
  `>{\raggedright\arraybackslash}p{...}` in `tab:reuse`; macros `\R`, `\hull`,
  `\conv`, `\norm`. No new macros.
- **Stale citation key in another lane:** `constraints.tex` line 143 cites
  `gleixner2017enhancements`; the alias file maps it to
  `gleixner2017-three-enhancements-for-optimization-based`.

## Citations used and requests

Keys used, all present in `references.bib`:
`gleixner2017-three-enhancements-for-optimization-based` (feasibility
filtering; side products of support solves for Lagrangian variable bounds),
`tarski1955fixpoint` and `caprara2010-global-optimization-problems-and-domain`
(order argument for monotone domain reduction), `jachymski2016perov`
(vector-valued contraction a posteriori estimates),
`mccormick1976-computability-of-global-solutions-to` (McCormick inequalities).
No new source is needed. Request for the literature lead: confirm that the
Gleixner et al. text supports both uses above, and that Jachymski and Klima is
an adequate source for Perov-type vector contraction estimates. No novelty or
priority claim is made; the text presents the order and contraction arguments
as standard and describes only the OBBT-specific certificate content.

## Review findings addressed

All open findings of `review-certificates-r1.md` and the corrections of
`audit-certificates.md` were applied: finite pools in `prop:current-round` and
`prop:round-check`; removal of the `-infinity` fiber discussion (foundations
assumes compact lifted sets); `v=s` in `ex:lambda`; lifted-monotonicity premise
for added rows; wording on discovery, original pools and merged ceilings; the
empty-cutoff-set case after `prop:box-threshold`; nonempty pools in the
frontier and response results; the face-threshold cost wording; the reuse-table
residual row; incumbent containment at a node; rational data for exact linear
solves; `ex:inactive` defined on every subbox; `prop:history` stated without
negative indices; the Heron error identity; precise history and cutoff-transfer
wording; replacement of the deleted local limit theorem and its `(L1),(L2)`
premises by `eq:closed-family`, `prop:fixed-limit` and `lem:sequential`;
`prop:continue` restricted to `U' >= f*`, the scope of `prop:fixed-limit`.

## Verification actually run

All commands were targeted; none is a project-wide or CI check.

1. Exact rational checks of every worked example, using the existing October
   checker module and no LP for the certificates themselves:
   `cd research-20261003-adaptive-obbt/theory && python3 -B -` (in-memory
   script). It checked the three-variable witnesses (threshold `0`, ceiling
   `-3`, exact square epigraphs), the child-box failure and its point of value
   `1/2`, the round-check example (vertex `(1/2,0)` rejected, `(1/2,1/4)`
   accepted), the half-interval at cutoff `1/4` and its first round `5/8`, mixed
   points failing the rebuilt secant, the cut removing `(0,-1/4)`, the frontier
   values `g(U)` at eight cutoffs, the corner face threshold, Heron iterates and
   `e=6/5`, `Me=9/20`, the observed-ratio data, and the halving map. One SciPy
   LP solve was used only as a floating sanity check of the child-box face value
   (`0.5`), which the text proves analytically. All assertions passed.
2. `python3 -B -` (in-memory script) checking the identities added in revision:
   output `PASS: Heron identity, convex-combination secant identity,
   row-condition values, Heron residual data`.
3. Targeted LaTeX build in `/tmp/certbuild`: the lead's preamble from
   `main.tex`, every existing section file, the appendices, and
   `references.bib`; `latexmk -pdf -interaction=nonstopmode -halt-on-error
   main.tex` exited 0. No warning, undefined reference, or box warning arises
   from my three files. Remaining warnings belong to other files
   (`gleixner2017enhancements` in constraints, `sec:precursor-details`).
   Rendered pages were inspected visually.
4. `python3 verification/check_sources.py` from the paper directory: reports
   only missing `abstract.tex` and `sections/discussion.tex`, undefined
   `sec:discussion` and `sec:precursor-details` in other files, and the stale
   key above. Nothing in my files.
5. A text scan of my files for placeholders, process words, and code references
   found none.

No numerical experiment was rerun, no literature search was made, and no CI
status or log was inspected.
