# Author report: constraints section

Date: 2026-10-05. Lane: constrained theory. Owned manuscript file:
`sections/constraints.tex` (Section 8 in the current build, pages 45–61 of
91). No appendix file was needed: every proof is complete in the section.
The root may move the graph-example verification (`ex:graph-con`) or the
explicit history examples to an appendix if a shorter main text is wanted;
no other section depends on their location.

Inputs read: the brief, `AGENTS.md`, October `theory/constrained-obbt.md`,
`document/constraints.tex`, `theory/check_constrained_obbt.py`,
`reviews/theory-review.md`, `theory/remaining-benefit.md`,
`implementation.md`, the September `theory.md`, the repository note on
error-bound transfer, `evidence/audit-constraints.md`, the relevant parts of
`audit-certificates.md` and `audit-rates.md`, `INTEGRATION-NOTES.md`,
`literature-audit.md` (preliminary), `literature-references.bib`, and the
current drafts of `foundations`, `certificates`, `cutoff`, `residual`,
`local-rates`, and `algorithms` for notation and labels. The independent
review `review-constraints-r1.md` arrived while I worked; all its required
corrections are applied (see below).

## Structure of the section

1. `sec:supports-con` — lifted LP setting in the paper's notation
   (`z=(x,y)`, affine objective `v`, `p=(-ell,u)`, signed objectives
   `c_i`), the Jacobi endpoint map, and a precise classification of rows:
   fixed rows; box and cutoff rows (fixed coefficients, affine right-hand
   sides); rebuilt McCormick rows (endpoint coefficients, product
   right-hand sides, auxiliary coefficient ±1).
2. `sec:dual-regions-con` — dual envelope with the finite dual-vertex
   representation (concave, piecewise affine, continuous support); cutoff
   multiplier with a two-sided bracket; exact basis regions with the
   converse (complete availability under a polytope premise); exact
   ranging; `ex:cutoff-con`.
3. `sec:brackets-con` — primal–dual bracket after an incumbent improvement;
   exact no-change threshold (an "if and only if" statement); decision
   classes; `ex:cutoff-bracket-con`.
4. `sec:rebuilt-con` — the precise treatment of changing McCormick
   matrices: frozen-row lemma (valid envelope, but frozen OBBT is
   idempotent and its comparison matrix is zero); counterexample to naive
   dual reuse; corrected stored-dual bound; basis certificates with
   parameter-dependent matrices and the Lagrangian derivative formula,
   made explicit for McCormick rows; positive-normalization special case.
5. `sec:cover-con` — comparison matrix from a complete region cover
   (general smooth-region version covering fixed and rebuilt matrices);
   finite exact coverage test; input corollary for `thm:residual`;
   `ex:switch-con`.
6. `sec:equality-con` — exact equality example with quadratic convergence
   at positive cutoff; restricted tangent contraction.
7. `sec:repair-con` — feasible-repair width theorem, linear-repair
   corollary, `alpha<1` limits, fully worked graph example.
8. `sec:histories-con` — two explicit misleading histories, as instances of
   `prop:history` in the residual section.
9. `sec:summary-con` — scope table `tab:scope-con` and the implementation
   boundary.

## Corrections relative to the archived sources

- **Rebuilt McCormick rows.** The October note said only that rebuilt rows
  violate the fixed-matrix premise and need "separate verification". The
  section now states exactly what holds: (a) frozen rows of an earlier box
  give valid dual envelopes under lifted monotonicity, but frozen-row OBBT
  stops after one round, so a frozen comparison matrix is zero and would
  falsely certify no remaining motion (`lem:frozen-con`, `ex:switch-con`);
  (b) old multipliers combined with rebuilt right-hand sides are invalid,
  with an exact counterexample that excludes an original sublevel point
  (`ex:rebuilt-dual-con`: 41/64 versus true support 41/40 and feasible
  `x=1`); (c) the residual-corrected stored dual is valid and needs only
  box bounds when auxiliary coefficients are fixed
  (`prop:corrected-dual-con`, 71/64); (d) exact supports are given by basis
  certificates with parameter-dependent matrices, whose derivatives are the
  Lagrangian sensitivities (`prop:rebuilt-basis-con`,
  `eq:lagrangian-derivative-con`), made explicit for McCormick rows.
- **Comparison matrix.** The October Proposition C4 assumed affine pieces
  on polyhedral regions. `thm:cover-con` proves the bound for any finite
  cover by closed regions on which the support agrees with a C^1 function,
  handles single-point intersections and degenerate boxes, and states that
  the two-sided bound implies the ordered form `eq:matrix-lipschitz`. The
  October proof's appeal to agreement "at cell boundaries" is replaced by a
  partition argument that needs no separate continuity premise.
- **Coverage obligation closed.** The archived text left multiparameter
  coverage as an obligation. `prop:coverage-con` (developed in the audit)
  decides it by finitely many exact LPs, with the vertex-only pitfall and the
  combinatorial cost stated.
- **Basis availability.** Added the converse of the basis-region
  proposition under a nonempty-polytope premise, with the free-lift
  counterexample showing the premise is needed.
- **Witness reuse made exact.** The October statement that the
  least-objective optimal witness gives "the widest reuse interval" is
  sharpened to an exact threshold: the support is unchanged if and only if
  the new cutoff is at least the least objective on the optimal face
  (`prop:threshold-con`).
- **Gradient statement.** A support need not be differentiable at a shared
  region boundary; the section speaks only of the derivative of the
  certified affine value (review R1).
- **Equality example.** The positive-cutoff analysis now gives the exact
  identity `r_{k+1}-a=(r_k-a)^2/(sqrt(2r_k^2+2a^2)+r_k+a)`, hence quadratic
  convergence, and states the limit `min{r_0,a}` for every start (audit and
  review R3). The October "general affine-equality extension is direct"
  claim is replaced by a proved conditional result,
  `prop:restricted-tangent-con`, which also shows why a nonzero gradient
  does not matter on the nullspace and treats the zero-gauge case
  (review R4).
- **Repair theorem.** Assumptions are required only on `K_U(B)`; the
  neighborhood for the Lipschitz and growth estimates is derived
  (`rho = wbar + kappa(beta wbar^2)^alpha`); Hoffman's theorem is named as
  the source of linear error bounds for polyhedral sets; the corollary is
  interpreted as guaranteed progress and checked for consistency with
  protected boxes; transfer to complete sequential rounds cites
  `lem:sequential`.
- **Graph example.** Uses the audited one-sided constant `L=1/2048`
  (`lambda_0^2=43/672`). New: the factor `25/48` holds on the entire
  admitted family (all widths at most 1/2), and `1/3` for widths at most
  1/8; the October `15/16` is valid but weaker. Validity and whole-family
  monotonicity are proved, the bilinear gap by the AM–GM inequality. New
  variant: replacing the constraint's epigraph by endpoint tangents keeps
  the theorem applicable with `L=9/64` and factor `3/4`; replacing the
  objective squares by tangents makes this sufficient estimate
  noncontractive without proving failure of the operator (review wording).
- **Histories.** The general statement now lives in `prop:history`
  (residual section), which handles arbitrary decreasing histories. I
  removed my duplicate proposition and kept the two explicit examples, which
  the residual section cites as `sec:histories-con`. Added: any valid scalar
  comparison constant on an interval containing the long-history trajectory
  is at least 1, so `thm:residual` correctly certifies no tail.
- **October C9 example replaced.** The normalized-tangent example used an
  artificial tangent point `r/8+3/4`. It is replaced by `ex:switch-con`, a
  McCormick square with a coupling row (`min x^2`, `x+x^2<=1`), whose
  tangent coefficient changes every round. It shows the cover theorem
  across a basis switch, the residual bounds (6 and 3 versus actual 4 and 1),
  an observed-ratio failure (3/5 predicted versus 1), and the frozen-row
  pitfall. The normalization mechanism is kept as a short remark.
- **Removed** repository-path links and the reference to a repository note
  as a source for error-bound transfer.

## Developments beyond transcription

New statements with full proofs: the dual-vertex representation of the
support (`prop:dual-envelope-con`(b)); the two-sided cutoff-multiplier
bracket (`cor:cutoff-multiplier-con`); the exact threshold
(`prop:threshold-con`); `lem:frozen-con`; `prop:corrected-dual-con`;
`prop:rebuilt-basis-con` with McCormick derivative formulas;
`thm:cover-con` in the general smooth-region form;
`cor:residual-input-con`; the exact error identity in
`prop:equality-con`; `prop:restricted-tangent-con`; `cor:repair-rate-con`'s
guaranteed-progress and protected-box consistency statements; the global
`25/48` and tangent-variant rates in `ex:graph-con`; examples
`ex:rebuilt-dual-con` (including the LP-free corrected iteration
`u_{k+1}=u_k-u_k^2/4+1/4`) and `ex:switch-con`.

## Labels

Defined (all with suffix `-con` except the section label):
`sec:constraints`, `sec:supports-con`, `sec:dual-regions-con`,
`sec:brackets-con`, `sec:rebuilt-con`, `sec:cover-con`, `sec:equality-con`,
`sec:repair-con`, `sec:histories-con`, `sec:summary-con`,
`eq:endpoint-map-con`, `eq:mccormick-rows-con`, `eq:param-lp-con`,
`prop:dual-envelope-con`, `eq:dual-envelope-con`,
`cor:cutoff-multiplier-con`, `eq:cutoff-reduction-con`,
`prop:basis-region-con`, `eq:basis-value-con`, `eq:ranging-con`,
`ex:cutoff-con`, `eq:cutoff-example-con`, `prop:bracket-con`,
`eq:bracket-con`, `prop:threshold-con`, `ex:cutoff-bracket-con`,
`lem:frozen-con`, `ex:rebuilt-dual-con`, `prop:corrected-dual-con`,
`eq:corrected-dual-con`, `prop:rebuilt-basis-con`,
`eq:lagrangian-derivative-con`, `thm:cover-con`, `prop:coverage-con`,
`cor:residual-input-con`, `ex:switch-con`, `prop:equality-con`,
`prop:restricted-tangent-con`, `eq:repair-error-con`,
`eq:repair-distance-con`, `eq:repair-lipschitz-con`,
`eq:repair-growth-con`, `thm:repair-con`, `eq:repair-width-con`,
`cor:repair-rate-con`, `eq:repair-step-con`, `eq:repair-iterates-con`,
`ex:graph-con`, `ex:long-history-con`, `ex:small-ratio-con`,
`tab:scope-con`.

Used from other sections (all resolve in the current full build):
`sec:foundations`, `lem:order`, `lem:sequential` (foundations);
`sec:certificates`, `lem:reference-family` (certificates);
`sec:cutoff-thresholds` (cutoff); `sec:residual`, `thm:residual`,
`eq:matrix-lipschitz`, `eq:supersolution`, `lem:invariant-interval`,
`prop:fixed-point-shift`, `ex:heron`, `ex:ratio`, `prop:history`
(residual); `sec:local-rates`, `sec:local-rates-tangent`, `ass:tangent`,
`thm:tangent-contraction`, `prop:quadratic-growth`,
`prop:two-variable-cutoff-floor`, `rem:linear-equations` (local rates);
`sec:algorithms`, `prop:dual-residual` (algorithms); `sec:experiments`.
Other sections cite my `prop:restricted-tangent-con` (local rates),
`prop:threshold-con` (cutoff), `prop:corrected-dual-con` (algorithms), and
`sec:histories-con` (residual).

Environments and macros: `proposition`, `lemma`, `corollary`, `theorem`,
`example`, `\R`, `\norm`, `\hull`, `\mathfrak` and `\mathcal` (amssymb),
`booktabs` and `array` (ragged-right table columns). All are in the current
`main.tex`; no new macro is introduced.

## Citations used and requested

Used (keys in `references.bib`):

- `borrelli2003parametric` — affine optimizers and values on critical
  regions of right-hand-side parametric LPs (intro and after
  `prop:basis-region-con`). This entry is in the paper bibliography but not
  in the preliminary vetted `literature-references.bib`. The October theory
  review checked it against Section 3.2, equations (8)–(11). **Request:**
  literature lead to confirm this key for exactly that claim, or supply a
  vetted alternative (for example Gal and Nedoma, Management Science 1972).
- `gleixner2017-three-enhancements-for-optimization-based` — "storing dual
  information from OBBT solves and propagating it after later bound and
  cutoff changes is the principle of their Lagrangian variable bounds".
  **Request:** confirm this description against the paper's section on
  Lagrangian variable bounds.
- `hoffman1952-on-approximate-solutions-of-systems` — a polyhedral feasible
  set `{Gx<=g}` admits `dist_inf(x,S) <= kappa max_j (G_j x - g_j)_+` with
  `kappa` depending only on `G`. **Request:** confirm the norm and
  constant form are supported as stated.
- `mccormick1976-computability-of-global-solutions-to` — McCormick rows.

Requested, not cited (text is written without them):

- A standard source for right-hand-side ranging in LP sensitivity analysis
  (the text calls it classical).
- A source for transferring feasible growth to infeasible points through an
  error bound in exact-penalty theory (text: "as in exact-penalty
  arguments"); candidates from the repository's prior check are Anitescu,
  SIAM J. Optim. 15 (2005), equations (1.18)–(1.19), citing Bonnans and
  Shapiro, Theorem 3.113, and Clarke's exact penalty principle.
- `robinson1973-bounds-for-error-in-the-solution-set` is vetted but unused;
  I did not attribute any specific claim to it without its text.

No priority or novelty claim is made in the section.

## Coordination notes for the root

- `local-rates.tex`, `rem:linear-equations`, writes the equation as
  `Ax=Ax^*` and `ker A`. My proposition uses `Cx=c_0` and `ker C` because
  `A` is the LP constraint matrix throughout my section. Suggest the remark
  use `C`.
- Foundations item (b) writes products as `w_ij`; certificates and my
  section use auxiliary variables `y_k` with `z=(x,y)`. Suggest unifying
  foundations item (b).
- The residual section says that for relaxations given by linear programs
  my section derives the comparison matrix from an exact cover; this is
  consistent, including rebuilt rows (conditional on verifying
  `prop:rebuilt-basis-con` on the regions).
- The closing paragraph describes the additional experimental policy as
  validating each current dual bound with `prop:dual-residual` and
  screening with current-round witnesses, without stored envelopes, basis
  regions, covers, or repair constants, based on the October
  `implementation.md`. The algorithms writer may wish to confirm.

## Response to `review-constraints-r1.md`

- R1 (piece derivative versus support gradient): fixed after
  `eq:basis-value-con` and after `eq:lagrangian-derivative-con`.
- R2 (unchanged support versus unchanged endpoint): the three-class
  paragraph now requires the current endpoint to equal the old support.
- R3 (limit for every start): the interpretation now states the limit
  `min{r_0,a}`, convergence rather than reaching, and quadratic error decay.
- R4 (cutoff and zero gauge): `U=f^*+epsilon` is declared in
  `prop:restricted-tangent-con`, and the proof treats `t=0` directly.
- Minor: the corrected polynomial is restricted to `1<=u<=2`; the remark on
  tangent-relaxed objective squares now says the sufficient estimate fails,
  not the operator.
- The review's `psi` notation refers to an earlier snapshot; the lifted
  objective is now `v`, matching foundations and certificates.

## Verification actually run

All commands were run from `/workspace/minlp-notes` or temporary
directories outside the repository. They are targeted checks of this
section, not project-wide checks or CI results. No experiment was rerun and
no literature search was done.

1. Exact-arithmetic checks with `python3 -` (heredoc, `fractions.Fraction`
   only). An early run checked the planned constants. The final run below
   checks every number stated in the final text; it passed:

   ```text
   PASS ex:cutoff-con regions, exact ranging, multipliers 1,1/4,0, threshold 3, bracket [5/3,9/4]
   PASS ex:rebuilt-dual-con naive 41/64, corrected 71/64, exact 41/40, corrected map on [1,2]
   PASS ex:switch-con regions, slope 1/2 and 0, residual e=6, Me=3, ratio 1/6 -> 3/5
   PASS coverage strip example tau=1/2
   PASS prop:equality-con identity, bounds, and sqrt(2)-1 root
   PASS ex:graph-con constants, rates 25/48 and 1/3, tangent variant 3/4, 5184 grid points
   PASS explicit histories: N=2,3,8,32 and small-ratio 1/100 -> 1/990 versus 9/10
   ```

   The grid checks supplement the analytic proofs; they do not replace them.
   The script is reproduced at the end of this report.
2. Standalone LaTeX compile of `sections/constraints.tex` in `/tmp/con-build`
   with the `main.tex` theorem environments and stub labels for every
   external reference (`pdflatex`, twice): no errors, no overfull or
   underfull boxes, no undefined references.
3. Full manuscript build of a copy in `/tmp/paper-build` (`pdflatex`,
   `bibtex`, `pdflatex` twice), after my final edits: no LaTeX errors, no
   undefined references or citations anywhere in the paper, 91 pages. The
   scope table falls on page 60 inside the section. This copy was a check
   only; no shared file was changed.

```python
from fractions import Fraction as Q

def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))

def solve2(M, r):
    (a, b), (c, d) = M
    det = a * d - b * c
    assert det != 0
    return [(r[0] * d - b * r[1]) / det, (a * r[1] - c * r[0]) / det]

# Example ex:cutoff-con (variables x1,x2; maximize x1; cutoff x2 <= U).
def rows(U):
    return [((-1, 0), Q(0)), ((0, -1), Q(0)), ((1, 0), Q(3)), ((0, 1), Q(4)),
            ((1, -1), Q(1)), ((4, -1), Q(7)), ((1, 0), Q(5, 2)), ((0, 1), U)]
h = lambda U: min(1 + U, Q(7, 4) + U / 4, Q(5, 2))
for lo, hi, I, eta in [(Q(0), Q(1), [4, 7], Q(1)), (Q(1), Q(3), [5, 7], Q(1, 4)),
                       (Q(3), Q(4), [6, 7], Q(0))]:
    for k in range(0, 9):
        U = lo + (hi - lo) * k / 8
        R = rows(U)
        AI = [R[i][0] for i in I]
        z = solve2(AI, [R[i][1] for i in I])
        assert all(dot(a, z) <= r for a, r in R)
        pi = solve2([[AI[0][0], AI[1][0]], [AI[0][1], AI[1][1]]], [Q(1), Q(0)])
        assert min(pi) >= 0 and pi[1] == eta and z[0] == h(U) == dot(pi, [R[i][1] for i in I])
    for U in [lo - Q(1, 100), hi + Q(1, 100)]:
        if 0 <= U <= 4:
            R = rows(U)
            z = solve2([R[i][0] for i in I], [R[i][1] for i in I])
            assert not all(dot(a, z) <= r for a, r in R)
assert h(Q(2)) == Q(9, 4) and Q(9, 4) - Q(1, 4) * Q(3, 2) == Q(15, 8) and h(Q(1, 2)) == Q(3, 2)
assert Q(15, 8) - Q(1, 2) == Q(11, 8) > 1
assert 4 * Q(5, 2) - 7 == 3
m = (Q(2, 3) * Q(5, 2), Q(2, 3) * 3)
assert m == (Q(5, 3), Q(2)) and all(dot(a, m) <= r for a, r in rows(Q(2)))
print("PASS ex:cutoff-con regions, exact ranging, multipliers 1,1/4,0, threshold 3, bracket [5/3,9/4]")

# Example ex:rebuilt-dual-con (Heron family, r=1).
G = lambda u: (u * u + 1) / (2 * u)
u0, u1 = Q(2), Q(5, 4)
assert G(u0) == u1
pi = (Q(1, 4), Q(1, 4))
assert (2 * u0 * pi[0], -pi[0] + pi[1]) == (1, 0)
naive = pi[0] * u1 * u1 + pi[1]
assert naive == Q(41, 64)
assert 2 * u1 * 1 - 1 <= u1 * u1 and 1 <= u1 and 1 <= u1 * 1
assert 2 * u1 * pi[0] != 1
q = 1 - 2 * u1 * pi[0]
assert q == Q(3, 8) and naive + q * u1 == Q(71, 64) and G(u1) == Q(41, 40)
corr = lambda u: u - u * u / 4 + Q(1, 4)
for k in range(0, 41):
    u = 1 + Q(k, 40)
    assert corr(u) == pi[0] * u * u + pi[1] + (1 - u / 2) * u
    assert corr(u) >= G(u) and corr(u) - 1 == (u - 1) * (3 - u) / 4
    assert G(u) - 1 == (u - 1) ** 2 / (2 * u)
print("PASS ex:rebuilt-dual-con naive 41/64, corrected 71/64, exact 41/40, corrected map on [1,2]")

# Example ex:switch-con (s=x^2, coupling x+s<=1, cutoff s<=0).
def R(u):
    return [(-1, 0, Q(0)), (1, 0, u), (0, -1, Q(0)), (2 * u, -1, u * u), (-u, 1, Q(0)),
            (1, 1, Q(1)), (0, 1, Q(0))]
F = lambda u: min(u / 2, Q(1))
for k in range(1, 161):
    u = Q(k, 40)
    rr = R(u)
    if u <= 2:
        z, I, pi = (u / 2, Q(0)), [3, 6], [1 / (2 * u), 1 / (2 * u)]
        assert pi[0] * (2 * u - 2 * z[0]) == Q(1, 2)
    else:
        z, I, pi = (Q(1), Q(0)), [5, 2], [Q(1), Q(1)]
    assert all(a * z[0] + b * z[1] <= c for a, b, c in rr) and z[0] == F(u)
    A = [(rr[i][0], rr[i][1]) for i in I]
    assert [A[0][0] * pi[0] + A[1][0] * pi[1], A[0][1] * pi[0] + A[1][1] * pi[1]] == [1, 0]
traj = [Q(4)]
for _ in range(4):
    traj.append(F(traj[-1]))
assert traj == [4, 1, Q(1, 2), Q(1, 4), Q(1, 8)]
d = traj[0] - traj[1]; e = 2 * d
assert d == 3 and d + Q(1, 2) * e <= e and Q(1, 2) * e == 3
r = (traj[1] - traj[2]) / d
assert r == Q(1, 6) and (traj[1] - traj[2]) / (1 - r) == Q(3, 5)
print("PASS ex:switch-con regions, slope 1/2 and 0, residual e=6, Me=3, ratio 1/6 -> 3/5")

# Coverage test example.
x, t = Q(0), Q(1, 2)
assert t <= x + Q(1, 2) and t <= -x + Q(1, 2) and t <= 1
assert Q(1, 2) * (x + Q(1, 2)) + Q(1, 2) * (-x + Q(1, 2)) == Q(1, 2)
print("PASS coverage strip example tau=1/2")

# prop:equality-con exact error identity at rational square roots.
for r_, a_, root in [(Q(7), Q(1), Q(10)), (Q(17, 2), Q(7, 2), Q(13))]:
    X = 2 * r_ * r_ + 2 * a_ * a_
    assert root * root == X
    G1 = root - r_
    assert a_ < G1 < r_ and G1 - a_ == (r_ - a_) ** 2 / (root + r_ + a_)
    assert G1 - a_ <= (r_ - a_) / 2 and G1 - a_ <= (r_ - a_) ** 2 / (4 * a_)
t2 = (Q(-1), Q(1))
sq = (t2[0] * t2[0] + 2 * t2[1] * t2[1], 2 * t2[0] * t2[1])
assert (2 * sq[0] + 4 * t2[0] - 2, 2 * sq[1] + 4 * t2[1]) == (0, 0)
print("PASS prop:equality-con identity, bounds, and sqrt(2)-1 root")

# ex:graph-con constants and both variants on a rational grid.
tau, beta, mu, K = Q(1, 64), Q(1, 4), Q(63, 64), Q(1, 4)
assert 4 * (tau + Q(1, 2048) * K) / mu == Q(43, 672) < Q(13, 48) ** 2
assert Q(13, 48) + Q(1, 4) == Q(25, 48) and Q(13, 48) + Q(1, 16) == Q(1, 3)
assert 4 * (tau + Q(9, 64) * K) / mu == Q(13, 63) < Q(1, 4)
assert Q(1, 2048) - 2 * Q(1, 64) ** 2 == 0
n = 0
for l in [Q(-1, 4), Q(-3, 16), Q(-1, 32), Q(0)]:
    for u in [Q(0), Q(1, 32), Q(3, 16), Q(1, 4)]:
        for yb in [Q(0), Q(1, 4096), Q(1, 64), Q(1, 16)]:
            w = max(u - l, yb)
            for i in range(9):
                x = l + (u - l) * i / 8
                sec = (l + u) * x - l * u
                tan = max(2 * l * x - l * l, 2 * u * x - u * u)
                assert x * x - tan <= (u - l) ** 2 / 4 and sec - x * x <= (u - l) ** 2 / 4
                for j in range(9):
                    y = yb * j / 8
                    mB = min(u * y, l * y + yb * (x - l))
                    assert 0 <= mB - x * y <= (u - l) * yb / 4
                    f = x * x + y * y - x * y / 16
                    assert x * x + y * y - mB / 16 >= f - tau * w * w
                    fr = x * x + x ** 4 - x ** 3 / 16
                    dl = y - x * x
                    assert fr - f == dl * (x / 16 - 2 * x * x - dl)
                    assert fr >= mu * max(abs(x), x * x) ** 2
                    if x * x <= y <= sec:
                        assert dl <= beta * w * w and fr <= f + dl / 2048
                    if tan <= y <= sec:
                        assert abs(dl) <= beta * w * w and fr <= f + Q(9, 64) * abs(dl)
                    n += 1
print(f"PASS ex:graph-con constants, rates 25/48 and 1/3, tangent variant 3/4, {n} grid points")

# Histories (ex:long-history-con, ex:small-ratio-con).
for N in [2, 3, 8, 32]:
    dl = Q(1, 2 * N); sg = Q(1, 2) - dl
    stall = lambda s: min(s, max(sg, s - dl))
    def shrink(s):
        if s <= sg: return s / 4
        if s <= Q(1, 2): return sg / 4 + 3 * sg * (s - sg) / (4 * dl)
        return s - dl
    for Fm in (stall, shrink):
        vals = [Fm(k) for k in (Q(0), sg, Q(1, 2), Q(1))]
        assert vals == sorted(vals) and all(0 <= v <= k for k, v in zip((Q(0), sg, Q(1, 2), Q(1)), vals))
    a = b = Q(1)
    for k in range(N + 1):
        assert a >= Q(1, 2) and (a - dl) / a >= 1 - Q(1, N)
        a, b = stall(a), shrink(b)
        assert a == b
    assert a == sg and stall(a) == sg and shrink(b) == sg / 4
def interp(knots, s):
    for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
        if x0 <= s <= x1:
            return y0 + (s - x0) * (y1 - y0) / (x1 - x0)
st = [(Q(0), Q(0)), (Q(899, 1000), Q(899, 1000)), (Q(9, 10), Q(899, 1000)), (Q(1), Q(9, 10))]
sh = [(Q(0), Q(0)), (Q(1, 10), Q(0)), (Q(899, 1000), Q(1, 10)), (Q(9, 10), Q(899, 1000)), (Q(1), Q(9, 10))]
pa, pb = [Q(1)], [Q(1)]
for _ in range(4):
    pa.append(interp(st, pa[-1])); pb.append(interp(sh, pb[-1]))
assert pa[:3] == pb[:3] == [1, Q(9, 10), Q(899, 1000)] and pa[-1] == Q(899, 1000) and pb[-1] == 0
rr = (pb[1] - pb[2]) / (pb[0] - pb[1])
assert rr == Q(1, 100) and (pb[1] - pb[2]) / (1 - rr) == Q(1, 990)
print("PASS explicit histories: N=2,3,8,32 and small-ratio 1/100 -> 1/990 versus 9/10")
```

## Scope statements kept in the section

These are stated limits of the proved results, not missing proof steps:
the cover theorem for rebuilt rows is conditional on verifying the basis
conditions and derivative bounds on each region, which in several
parameters requires bounding rational functions; complete covers and the
coverage test can be combinatorially large; the repair constants involve
`x^*` and `f^*` and are analytic premises; the restricted tangent result is
conditional on a uniform restricted expansion and a strict contraction of
the restricted map; and the experimental policy implements none of the
stored-envelope, region-cover, or repair machinery.
