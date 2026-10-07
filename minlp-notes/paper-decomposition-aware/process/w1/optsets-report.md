# Cluster report: nonunique optimal sets (KEY = optsets)

Scope: the report subsections "Compact descriptions of nonunique optimal sets"
and "Polynomial boundary output with an explicit margin" in
`research-20261002-decomposition/document/extensions.tex`. I also checked the
results they depend on: the endpoint full-set note, the diagonal-class
discovery note, the proximal set-growth generator, the stationary-face
recovery lemma, and the boundary active-face theorem with its integer-label
filter and convex-patch test.

The paper fragment is `optsets-proofs.tex`. It gives complete proofs and uses
only main-text lemmas (cited by their `main.tex` labels).

## Verdict

**Sound with fixes.** I re-derived every claim in the cluster. I found no
critical error and no false main statement. All constants checked out:
`99/256`, `theta^2 K <= 1/8`, the fresh-box radius, the recovery radius
`tau = 1/(4nR)`, and the patch thresholds `g/32`.

Two major problems are about what the paper proves, not about the
mathematics:

1. The unknown-growth theorem for the diagonal class depends on a proximal
   candidate generator and a recovery lemma. The report states that their
   proofs "remain in the identified companion notes", so the paper is not
   self-contained.
2. The boundary-output paragraph defers the search schedule, the integer-label
   fixation and the patch certificate to "the boundary companion".

The fragment closes both gaps with complete proofs. It also adds several
sharpenings, listed under "Developments" below.

## (a) Endpoint Bellman-residual identity: verified

- **Identity.** Independent endpoint rounding keeps the linear and
  off-diagonal terms and adds `H_ii Var/2` to each diagonal term. Taking
  expectations of the telescoped residual sum gives
  `F(x) - F* = sum r_t pi_t + (1/2) sum (-H_ii)(x_i-l_i)(u_i-x_i)` on the whole
  continuous hull. The sign is correct.
- **Simpler proof.** DP correctness is not needed. Three facts suffice:
  - every residual is nonnegative, by definition of a minimum;
  - the residuals telescope;
  - traceback gives an endpoint assignment whose residuals are all zero.

  The identity then shows `F >= M_root` on the hull, and the traceback point
  shows the value is attained. So `M_root = F*`, and endpoint optimality
  follows as a by-product. A checker needs only the tables, nonnegativity of
  the residuals, and one zero-residual assignment. Any nonnegative
  reparameterization with an attained root constant describes the same set.
- **Integer coordinates.** Rounding an interior integer label is used only in
  the analysis; the identity is a polynomial identity on the hull. The
  description keeps integrality as a separate constraint and never enumerates
  interior labels.
- **Coordinates with `H_ii = 0`.** Interior values are allowed exactly when
  the whole rounding support is optimal. The `x+y-2xy` example confirms that
  having optimal corners in every coordinate projection is not enough.
- **Coordinates with `H_ii < 0`.** Interior points, real or integer, are
  excluded.
- **Boundary case (minor).** The hypothesis `H_ii <= 0` is not needed for
  two-label integer coordinates. On `{l, l+1}`, replace `H_ii x^2/2` by its
  chord. This covers all binary QPs.
- **Size.** At most `n + N 2^p` factored equations of degree at most `p`. Each
  message entry is a sum of monomial values at one endpoint assignment, so all
  bit lengths are polynomial in `I`.
- **Exact checks.** `check_endpoint.py` tested 60 random instances on path and
  branching decompositions, with mixed continuous, integer and two-label
  coordinates. It checked:
  - 1,500 exact identities at random hull points;
  - the characterization at 96,758 rational test points;
  - 300 projection dynamic programs against brute force over all `3^n`
    patterns, plus dimension, downward closure and attainment.

  Sixteen instances had more than one optimal test point and seven had a
  positive-dimensional optimal set.

## (b) Diagonal certificate, invariance and unknown-growth discovery: verified

- **Identity.** Both sides are quadratics with the same value, gradient and
  Hessian at `xbar`. The boundary-gradient signs are correct. A compact form:
  `lambda_i(xbar) = 2|dF_i(xbar)|/(u_i-l_i)` for every `i`, since interior KKT
  coordinates have zero gradient.
- **Invariance across optima.** The report's gradient-update argument is
  correct. A cleaner and more informative proof uses the Lagrangian dual
  `psi(lambda) = inf_x [F - (1/2) sum lambda_i (x_i-l_i)(u_i-x_i)]`. The class
  is exactly the set of instances with `max psi = F*`. Any dual maximizer
  `lambda` and any optimizer `xbar` satisfy complementarity and stationarity of
  the Lagrangian, which forces `lambda = lambda(xbar)` and `H + Lambda >= 0`.
  This gives invariance, uniqueness of the multiplier, and the equivalence of
  "some optimizer" and "every optimizer" in one step (fragment, Lemma
  `lem:diagcert`).
- **Proximal generator under set growth: verified line by line.**
  - The fresh box contains a nearest optimizer because
    `dist <= 2 sqrt(Kn) h <= rho h`.
  - Rounding variance: the enclosing interval is generated from its inner
    endpoint, so its length is at most `h + theta|s_i - c_i|`. Unit integer
    intervals give zero variance.
  - Mesh energy: `D <= L n h^2/4 + eta ||y-c||^2` with `eta = L theta^2/4`.
  - Gap: the width bound `(Lnh^2/4)(1+theta^2/2)(1+4K theta^2) <= 99/256 L n h^2`
    holds with `theta <= 1/4` and `K theta^2 <= 1/8`.
  - Induction: `99/256 K n h_j^2 <= 2 K n h_{j+1}^2 <= 4 K n h_{j+1}^2`.
  - Grid count: at most `10/theta * ceil(log2(n+2))`, well under the cap.
  - Denominators divide `omega_0 2^{j + mu K_theta}`.
  - With a false guess, grid sizes, stage counts and denominators are still
    bounded, and every center stays feasible.
- **Simplification.** Discovery needs neither the promise-dependent lower
  bound `LB_j` nor the `epsilon` schedule of the note. The distance bound
  `dist(y_j,S)^2 <= 99/256 K n h_j^2` directly sets the stage budget: the least
  `J` with `4^J tau^2 >= 4 K n s^2`.
- **Recovery lemma: verified.**
  - Integer coordinates agree.
  - Selection is unambiguous because widths are at least `1/omega > 2 tau`.
  - `J` is contained in `J_0`.
  - Every point of the stationary polytope `P` is optimal (exact expansion).
  - The vertex denominator is at most `R`, by expanding along unit rows to a
    minor of `omega H` of size at most `(nC_H)^n`.
  - The slack bound is `q(s) <= 3/(8R) < 1/R`.
  - Every feasible point of the selected system is optimal, with no
    nonsingularity assumption.

  `main.tex` already contains this argument inside the proof of Theorem
  `thm:generalfinite`. The paper should state it once as a lemma and use it
  twice.
- **Can the generator go in the paper compactly?** Yes. With `lem:round`,
  `eq:mesh` and the counting in `lem:states` reused, it fits in about one page
  (fragment, Lemma `lem:proximal`).
- **Discovery theorem: verified.**
  - Acceptance is sound under every guess.
  - At the first `K >= L/g` (so `K <= 2 kappa`), the candidate is within
    `tau/2` of `S`, the LP vertex is optimal, and invariance makes the test
    pass whichever component was found.
  - Cost is `f(p,kappa) poly(I)`, and in fact polynomial in `kappa` and `I` for
    fixed `p`.
  - Termination on the class is unconditional, because a set-growth constant
    always exists (Luo–Sturm, Theorem 3.3; I checked the statement in the
    local copy).
- **Exact checks.**
  - `check_diagonal.py`: 4,000 exact identities, including points outside the
    box; 185 invariance moves between optimal components; 98,112 full-set grid
    comparisons; trap rejection; the tilted two-segment example; and a
    Subset-Sum instance whose optimal set is exactly its 4 solutions, each
    certified.
  - `check_proximal.py`: the proximal invariants at every stage on a flat
    diagonal and on the tilted two-segment example (with its growth constant
    `1/12` checked on a grid), plus the full discovery loop. In the trap
    example the guesses `K=1,2,4` give the origin at every stage `<= 33` and
    are rejected; `K=8` is accepted at `(1,1)`.

## (c) Polynomial boundary output: verified; recommended for an appendix

- **Soundness: verified.**
  - The retained box contains every optimizer.
  - Integer-label filter: a label whose adjacent intervals are all unit
    intervals has zero correction, so its min-marginal bounds every point with
    that label.
  - Weak sign tests preserve the minimum; strict tests preserve every
    minimizer.
  - Patch: `|H(x)-H(c)|` has row sums at most `C_3 r`, and the spectral norm
    is at most the largest row sum.
- **Termination: verified.**
  - Under uniqueness, a sound reduction can only fix active coordinates.
  - With `r <= gamma/(4 C_2)`, the midpoint test fixes every active
    coordinate.
  - The remaining coordinates are interior, so `H_JJ(x*) >= 2g` by two-sided
    growth.
  - The thresholds give `2 C_3 r <= g/32` and `sigma <= g/32`.
  - Stage count: `poly(I) + O(log kappa + B_gamma)`.
- **Dovetailing.** Phase `q` allots fewer than `2^{q-1}` operations, so the
  total is `O(sqrt(kappa) A_*)`. Dovetailing is necessary: a too-coarse trial
  may run forever within its cap. Interleaving whole stages instead would put
  the bag size into the exponent of `B_gamma`.
- **Minor.** The sign test should require the original bound to be an
  endpoint of the current retained interval. The report's wording omits this.
- **Judgment.** The result is correct but secondary to the paper's story. It
  needs three small lemmas (label filter, monotone reduction, patch) that are
  not in the main text. It fits as an appendix that answers "what exact output
  means for polynomials with irrational boundary optima". If space is tight,
  keep a one-paragraph remark and drop the theorem.

## Issues

| # | Severity | Location | Issue | Fix (verified) |
|---|---|---|---|---|
| 1 | major | extensions.tex, end of "Compact descriptions..." | The unknown-growth theorem depends on the proximal generator and the recovery lemma, which are "in companion notes". The paper is not self-contained. | Include Lemma `lem:proximal` (set-growth proximal stage) and Lemma `lem:recovery` (extracted from `thm:generalfinite`). Complete proofs are in the fragment. |
| 2 | major | extensions.tex, "Polynomial boundary output" | Search schedule, integer-label fixation and patch certificate are deferred to "the boundary companion". | Appendix `app:boundary` gives Lemmas `lem:labelfilter`, `lem:monotone`, `lem:patch` and Theorem `thm:boundary` with full proofs. Otherwise drop the paragraph. |
| 3 | minor | extensions.tex, boundary paragraph | The midpoint sign test must require the original bound to be an endpoint of the current retained interval. | Stated in Lemma `lem:monotone`. |
| 4 | minor | extensions.tex, boundary paragraph | "Existing examples have exponentially large `B_gamma`" is unproved in the paper, and it shows only that the bound is weak, not that the method needs it. | Proposition `prop:margin`: on `G_n` (degree 4, bag size 3, `kappa = 140/9`), every successful certificate of this form contains a rational with reduced denominator at least `2^{4*2^n-2}`. So the cost is intrinsic to rectangular sign certificates. |
| 5 | minor | extensions.tex, endpoint paragraph | Notation clashes with the main text: `Q` (used for `F-D`), `D` (correction and denominator), `l` versus `a,b` bounds, `x'Qx` versus `x'Hx/2` in the same subsection. | Fragment uses `F = x'Hx/2 + b'x + c`, `Lambda` for multipliers, `omega` for the denominator, and `l,u` for bounds. |
| 6 | minor | extensions.tex, endpoint paragraph | The hypothesis `Q_ii <= 0` is stated for all coordinates. | Remark `rem:endpointext`: it is needed only for coordinates with at least three feasible values (chord substitution on `{l,l+1}`). The proofs also extend to multilinear plus separable concave objectives. |
| 7 | minor | extensions.tex, endpoint paragraph | The value of the full-set description is undersold. "Factored polynomial equations" leaves open whether any query about `S` can be answered. | Corollary `cor:facecsp`: optimal faces are the solutions of a tree-structured 3-label constraint problem. Uniqueness, dimension, counting, projection and linear optimization over `S` all take `2^{O(p)} poly(I)`. |
| 8 | minor | extensions.tex, diagonal paragraph | Classical status is attributed only to Li–Wu–Quan. The duality characterization, which is the cleanest proof of invariance, is not stated. | Lemma `lem:diagcert`(iii) and Remark `rem:shor`: the class is exactly the set where the box-Lagrangian dual (Shor relaxation) is exact. Add Jeyakumar–Rubinov–Wu (2006) and Qiu–Yıldırım (2023); see citation status below. |
| 9 | minor | proximal note (to be imported) | The `epsilon`/promise-interval stage budget is more complicated than needed. | Use the direct distance bound and the budget `4^J tau^2 >= 4Kns^2` (Theorem `thm:diagdiscovery`). |
| 10 | minor | extensions.tex, diagonal paragraph | The scope gap is not stated: within the class, finding an optimizer can be hard without `kappa`, while the value is a convex-relaxation value. | Proposition `prop:sshard`: a Subset-Sum construction at bag size 3 is in the class whenever feasible, with `F* = 0` known. Exact discovery and uniqueness are NP-hard, and unless P=NP, `kappa` is superpolynomial on this family. |

## Classical versus new

- **Endpoint full-set theorem.**
  - Classical: endpoint optimality for coordinatewise concave or multilinear
    objectives. Rosenberg (1972) for multilinear polynomials on the cube [not
    checked]; Del Pia–Khajavirad (2026) for nonpositive diagonals [checked in
    the local knowledge base]. Min-sum messages and nonnegative tree
    reparameterizations (Dechter 1999; Wainwright–Jaakkola–Willsky 2005). For
    purely discrete problems, the set of optimal labelings as the solution set
    of a constraint problem built from zero (tight) reparameterized entries
    goes back to the max-sum literature (Werner 2007, IEEE TPAMI 29(7)) [not
    checked].
  - New as far as I know: the exact identity on the continuous hull with the
    variance term, the `{L,U,*}` face-pattern constraint problem covering
    interior points, and the query algorithms (projection, dimension,
    uniqueness, counting).
- **Diagonal certificate.**
  - Classical: box-Lagrangian sufficient conditions. Jeyakumar–Rubinov–Wu, J.
    Global Optim. 36 (2006), 471–481 [existence and title confirmed by web
    search; statement not read]. Li–Wu–Quan (2015), Corollary 2 eq. (14), as
    identified by the companion notes [publisher page blocked; not
    re-verified]. Lagrangian duality and Shor relaxation exactness (standard).
  - Related: exactness characterizations for RLT and SDP-RLT relaxations of box
    QP (Qiu–Yıldırım, arXiv:2303.06761 [abstract verified]); sparsity-based
    Shor exactness (Kojima–Kim–Arima 2026 local-to-global; Azuma et al. 2023
    [knowledge-base summaries checked]). None of these find an optimizer under
    unknown growth.
  - New: invariance used as the acceptance mechanism of an unknown-growth,
    decomposition-aware exact search (Theorem `thm:diagdiscovery`), and the
    hardness of exact discovery inside the class without `kappa`
    (Proposition `prop:sshard`). The construction is essentially Del
    Pia–Khajavirad's Remark 2 (weak NP-hardness, Subset Sum, bags
    `{s_{i-1}, s_i, x_i}`) [checked in the local knowledge base]; the
    observation that it lies in the certificate class is new.
- **Value-oracle barrier.** The classical hidden-bump technique of
  information-based complexity (Nemirovski–Yudin 1983) [citation not checked].
  The `k`-dimensional set-growth version with `kappa = 1` is a short
  adaptation; its role in the paper is to separate point growth from set
  growth.
- **Proximal generator.** Proximal terms and grids are standard. The fresh-box
  set-growth analysis is the repository's own; I know of no direct prior
  statement.
- **Recovery lemma.** In the spirit of the vertex and height arguments behind
  "QP is in NP" (Vavasis 1990) [record only; not read].
- **Boundary output.** Monotonicity propagation (Araya–Trombettoni–Neveu
  2010), Bernstein enclosures and strongly convex patches are classical. The
  new parts are the schedule with its margin-dependent bound and the two
  sharpness propositions.

## Placement recommendations

| Result | Recommendation | Reason |
|---|---|---|
| Lemma `lem:endpointid` and Theorem `thm:endpointset` (endpoint residual identity, all optimizers) | main | The cleanest growth-free result for nonunique optima. It is decomposition-specific, short, and fits the story. |
| Corollary `cor:facecsp` (face-pattern constraint problem and queries) | main | One paragraph and a short proof. It turns "a description" into "every natural query in `3^p poly`". |
| Remark `rem:endpointext` (two-label coordinates, multilinear version) | remark | Easy extension; no new proof. |
| Lemma `lem:diagcert` (identity, full set, duality, invariance) | main | Needed by the discovery theorem. Present it as classical; the duality proof is short. |
| Proposition `prop:oraclebarrier` (value-oracle barrier) | main | A short structural limit that explains why set growth needs coefficient certificates while point growth does not. It matches the "structural limits" in the title. |
| Lemma `lem:proximal` (proximal stage under trusted set growth) | appendix | Complete one-page proof reusing main lemmas. State it in the main text. |
| Lemma `lem:recovery` (stationary-face recovery) | main | Already inside the proof of `thm:generalfinite`. Extract it and use it twice. |
| Theorem `thm:diagdiscovery` (unknown-growth discovery for the certificate class) | main | The only complete unknown-growth result for nonunique optima. Short once the lemmas are in place. |
| Proposition `prop:sshard` (hardness inside the class without `kappa`) | remark | Short proof. It justifies the parameterization and explains why the value is easier than the optimizer. |
| Theorem `thm:boundary` and Lemmas `lem:labelfilter`, `lem:monotone`, `lem:patch` | appendix | Correct but secondary. It needs three extra lemmas. Drop it if the appendix budget is tight, and keep a remark. |
| Propositions `prop:margin` and `prop:weakcompl` | appendix | Their sharpness only matters if Theorem `thm:boundary` is kept. |

## Developments on the open questions

1. **Full-set queries in the endpoint class (resolved).** The optimal set is a
   cubical complex given by a tree-structured 3-label constraint problem.
   Uniqueness, dimension, counting, projection and linear optimization over
   `S` all run in `2^{O(p)} poly(I)`. The proof is in the fragment and was
   checked by brute force.
2. **Diagonal class characterization (sharpened).**
   - Proved: the class is exactly the set where the box-Lagrangian dual
     `max psi` equals `F*`, and the dual maximizer is unique and equals
     `lambda(xbar)` at every optimizer.
   - Stated without proof (standard conic duality): `max psi` is the basic
     Shor SDP value, because the Shor relaxation here is strictly feasible and
     bounded. It is marked as a remark.
3. **Hardness inside the class (new, proved).** At bag size 3, finding an
   exact optimizer, or deciding uniqueness given one optimizer and the full
   description, is NP-hard (weakly, through Subset Sum). Combined with
   Theorem `thm:diagdiscovery`, `kappa` must be superpolynomial on that family
   unless P=NP. The parameter is therefore necessary, not an artifact.
4. **Efficient discovery for arbitrary unknown optimal sets (partial).**
   - Proved: every value/derivative-oracle algorithm needs
     `Omega(eps^{-k/2})` queries on `f = 0` in `[0,1]^k` (`kappa = 1`). This
     covers every grid certificate whose validity rests on function values and
     `L`, including the corrected-grid certificate with any irregular grids.
     It answers the suggested "lower bound for coordinate-hull
     representations" in a stronger, representation-free form.
   - Not obtained: a lower bound for explicit QPs.
   - Attempted: conditional hardness through a "switch" construction
     `F = z G(x)` (degree 3) or similar. It fails for a structural reason. If
     the easy side of the reduction gets its set growth from a value gap
     `delta`, then `kappa >= L/delta`, and the plain uniform corrected grid
     already certifies accuracy `delta/2` in time `(s sqrt(Ln/delta))^p`,
     which is polynomial in `kappa`. Any hardness proof must make
     exponentially fine accuracy necessary while keeping `kappa` small. This is
     a heuristic obstruction to a proof strategy, not a theorem.
   - The general question remains open.
5. **Boundary output under point growth alone (sharpened).** Two proved
   propositions:
   - `prop:margin`: the `B_gamma` cost is intrinsic to rectangular sign and
     patch certificates. It is not an artifact of the analysis.
   - `prop:weakcompl`: without strict complementarity, the certificate format
     fails completely, even with `kappa = 24`, degree 4 and one bag. The
     instance `W = u^2 + w_1^2 + w_2^2 + 3w_1w_2 + u(w_1-w_2)` with
     `u = x^2 - 1/2` has sign-indefinite derivatives on every box around the
     optimizer and an indefinite Hessian there.

   The same instance has a short global identity certificate. This points to
   correlation-keeping certificates (sums of squares plus boundary products).
   No parameterized-size construction of such certificates is known; this
   remains open.
6. **Proximal generator in compact form (resolved).** Lemma `lem:proximal`
   gives the complete proof with the simplified budget.

## Remaining open questions in the cluster

- An exact algorithm for explicit box QPs under unknown set growth with running
  time `f(p,kappa) poly(I)`, beyond the endpoint and diagonal classes; or a
  conditional lower bound for explicit QPs.
- Exact implicit output for polynomials under point growth with weakly
  complementary active coordinates, or with tiny margins without paying
  `B_gamma`. Certificates that keep cross-coordinate correlations seem
  necessary (Propositions `prop:margin`, `prop:weakcompl`).
- Whether a set-growth analogue of min-marginal filtering exists with an
  independently checkable certificate and bounded state counts when the
  optimal set has bounded "complexity" (for example, finitely many components
  of bounded size).
- Whether membership in the diagonal class can be certified or refuted
  efficiently under bounded width and `kappa`.

## Citation status (for `references.bib`)

- `QiuYildirim2023`: Y. Qiu, E. A. Yıldırım, "On Exact and Inexact RLT and
  SDP-RLT Relaxations of Quadratic Programs with Box Constraints",
  arXiv:2303.06761 (2023). Abstract verified on arXiv; journal version not
  checked.
- `JeyakumarRubinovWu2006`: V. Jeyakumar, A. M. Rubinov, Z. Y. Wu, "Sufficient
  global optimality conditions for non-convex quadratic minimization problems
  with box constraints", J. Global Optim. 36 (2006) 471–481. Title and venue
  appear in search results and citing works. Volume, pages and theorem content
  were not read.
- `LiWuQuan2015`: already in the bibliography. The publisher page redirected
  to a login, so I could not re-verify Corollary 2 eq. (14).
- `LuoSturm2000`: Theorem 3.3 confirmed in the local copy (polytope, single
  quadratic, exponent 1/2).
- `DelPiaKhajavirad2026`: Theorem 3 (treewidth-2 strong NP-hardness),
  Theorem 2 (degree-4 path) and Remark 2 (Subset-Sum construction, bags
  `{s_{i-1},s_i,x_i}`) confirmed in the local full text. Formulas were
  partially lost in the extraction.
- Optional and not checked: Rosenberg 1972 (multilinear vertex property);
  Werner 2007 TPAMI (max-sum constraint problem of optimal labels);
  Nemirovski–Yudin 1983 (hidden-bump lower bounds).

## Verification record (targeted, local)

These are local targeted checks, not CI. Commands run from
`paper-decomposition-aware/process/w1/checks/`:

- `python3 -B check_endpoint.py`: passed. 60 instances, 1,500 identities,
  96,758 characterization points, 300 projection dynamic programs.
- `python3 -B check_diagonal.py`: passed. 4,000 identities, 185 invariance
  moves, 98,112 full-set points, trap rejection, Subset-Sum class membership.
- `python3 -B check_proximal.py`: passed. Stage invariants, the discovery loop
  (flat diagonal, tilted segments, trap rejected for `K=1,2,4` and accepted at
  `K=8`), and the origin at every stage `<= 33` for `K <= 4`.
- `python3 -B check_boundary.py`: passed. Symbolic identities for `G_n`
  (`n = 1..4`) and `W`, curvature formulas, the indefinite minors, and exact
  growth samples.
- `pdflatex` of the fragment in a minimal wrapper (`checks/texbuild/`): no
  errors. The only undefined references are main-text labels and bibliography
  keys, as expected.

All checks are finite exact-arithmetic diagnostics. They support the proofs
but do not replace them.
