# Consistency relaxations on tree decompositions: split classes, bands of exact splits, and h/p/hp refinement

Date: 2026-09-30. Workstream "theory-consistency" of the September 29
program. Status: **reviewed, rechecked, confirmed; revised three times.**
An independent review
([`../reviews/consistency-review.md`](../reviews/consistency-review.md))
checked every proof and found them correct, but asked for corrections of
interpretation, numbers and attribution. A recheck
([`../reviews/consistency-recheck.md`](../reviews/consistency-recheck.md))
confirmed the first revision's numbers. It also found one false claim, one
flawed argument, a lost log and imprecise citations. The second revision
added a proof (Proposition 5.8(b)) and a short limit argument (Section 3,
Remarks). A confirmation
([`../reviews/recheck-consistency-confirm.md`](../reviews/recheck-consistency-confirm.md))
checked both step by step and found them correct; it raised six minor
points. The third revision fixes them. It also adds a short proof,
proposed in the confirmation and checked again here, that the T1 gap stays
strictly above the lower end of Theorem 3.1 at every finite coupling `K`
(Section 3, Remarks). The third revision was confirmed by
[`../reviews/consistency-confirm-r1.md`](../reviews/consistency-confirm-r1.md)
(no mathematical error; its two optional points were applied by the root at
the end of Section 12). Section 12 lists the changes of all three revisions.
Proofs are complete unless a step is marked "sketch". All computations are
floating-point LPs (HiGHS through scipy); they are illustrations, not
certified values. Scripts and logs are in this directory (Section 11).

Cited notes:

- [D] decomposition note, [`../theory-decomposition/decomposition-certificates.md`](../theory-decomposition/decomposition-certificates.md)
  (Lemma 1.1, Proposition 2.6, Theorem 3.4, Observation 4.2);
- [R] robust-lower-bound note, [`../theory-robust-lb/robust-lower-bound.md`](../theory-robust-lb/robust-lower-bound.md)
  (Lemma 1.2, Proposition 3.3);
- [S] September 28 sparse-rate notes: [`quadratic-sharpness.md`](../../research-20260928/solver/quadratic-sharpness.md),
  [`affine-recourse-rate-boundary.md`](../../research-20260928/solver/affine-recourse-rate-boundary.md),
  [`active-region-rates.md`](../../research-20260928/solver/active-region-rates.md), and the
  [closing summary](../../research-20260928/closing-research-results.md);
- [O] open-instances report, [`../open-instances/open-instances-report.md`](../open-instances/open-instances-report.md).

## Summary

**Setting.** `F = sum_t F_t(x_{V_t})` on a box with a rooted tree
decomposition. Each separator `S_e` carries a linear space `Phi_e` of test
functions that contains the constants. A split `phi = (phi_e)` subtracts
`phi_e` from the child bag of edge `e` and adds it to the parent bag. The
split relaxation is

```
rho(Phi) = sup_{phi in Phi} sum_t min_{X_t} vex(F_t^phi),      gap(Phi) = f* - rho(Phi).
```

**Main answers.**

- **(A) Duality: holds; known in substance.** For any per-bag relaxation
  given by a weak*-compact convex set of normalized functionals (exact bag
  measures, pseudo-moment sets), `rho(Phi)` equals the minimum over bag
  measures whose neighbouring separator marginals agree on `Phi_e`
  (Theorem 1.1). Continuity of `F_t` and `Phi_e` and compactness are the
  only conditions. This is cost-shifting (reparametrization) duality of
  graphical models, weighted CSP and sparse moment relaxations. The
  *per-bag* envelope step loses nothing, because `min vex f = min f`. A
  per-bag envelope bound with a joint minimum is the same relaxation with
  `Phi + affine` (Proposition 1.3). Per-factor envelopes such as McCormick
  or alphaBB are weaker when a bag holds several factors.
- **(B) Approximation bound: proved in a sharper form. It holds with one
  joint exact split and fails if the infimum is taken separately on each
  edge.**
  - *One separator.* Let `Band = {psi : f* - V <= psi <= U}` be the set of
    exact splits, where `U` is the child-side and `V` the parent-side value
    function of the separator. Then exactly
    `gap(Phi) = 2 dist_inf(Phi, Band)` (Theorem 2.1). The right quantity is
    the sup-norm distance to the band, not to the value function. Errors
    count only where the band is thin, that is, near optimal separator
    values. The constant 2 is exact.
  - *Trees.* `2 max_e dist(Phi_e, Band_e) <= gap <= 2 inf_{psi exact} sum_e dist(psi_e, Phi_e)`
    (Theorem 3.1).
    - The upper end is attained (T1, separable middle bag).
    - The lower end is also attained in nontrivial instances. In the random
      three-bag instances T3 it is attained in 515 of 900 cases. In 93 of
      those, both per-edge distances are positive, so the sum is strictly
      larger. In T1 it is approached as the coupling `K -> inf`, by the
      bound `gap <= 2 E_n + Lip(r)^2/(4K)`, where `r` is the error of the
      best degree-`n` approximant of `|s|` (Section 3). At every finite
      `K` the T1 gap stays strictly above `2 E_n` (also proved in
      Section 3).
    - With the DP split on a path, the upper bound is the deterministic
      finite-horizon form of the approximate-LP bound of de Farias–Van
      Roy.
  - *The infimum must be over one joint exact split.* In Proposition 3.3
    each band contains a constant, yet the constant-class gap is 1. In
    random three-bag instances the sum of per-edge band distances is below
    the gap in 247 of 900 cases.
- **(C) Lower bounds.** For one separator the identity makes the
  approximation error the exact quantity.
  - *Kink at a pinch point* (an optimal separator value, where the band
    has zero width). Polynomials of degree `n` lose `Theta(1/n)` even when
    the band opens quadratically around it (Proposition 5.6, lower bound
    `1/(30(3+c)n)`).
  - *Zero-width kinked band.* `n gap -> 2 beta = 0.5603` (Bernstein's
    constant). Computed: 0.5602 at `n = 64`. For a positive band width the
    same limit is a conjecture. Its heuristic support is weak, and the
    limit may be smaller (Section 5.4).
  - *Piecewise constants.* Closed form, first order in the cell width. It
    reproduces Proposition 2.6 of [D] in this model.
- **(D) Instances.**
  - *Affine (Lagrangian) classes.* The gap is 0 iff the per-bag
    Lagrangians with the copy multipliers at `x*` are globally minimized at
    `x*` (Proposition 5.1).
  - *Regularity at pinch points.* On boxes with `C^{1,1}` data every value
    function is semiconcave. So at interior pinch points the band is
    differentiable, with no kinks (Lemma 4.2), and affine splits are second
    order there.
  - *Piecewise-affine cells* (Proposition 5.4). On a one-dimensional
    separator the gap is at most `max_D ((M_L+M_U)/2) r_D^2 - w_min(D)`,
    with kinks allowed anywhere; in higher dimensions this needs a pinch
    point in the cell or a `C^{1,1}` side. It gives `O(h^2)` on uniform
    meshes. For one separator under quadratic growth (and, for `k >= 2`,
    a `C^{1,1}` child-side value function near the pinch point), shell
    meshes need `O(max(16 Mk/c, 16)^{k/2} log(1/eps)) + O_eps(1)` cells
    (Corollary 5.5). This is an idealized analogue of Theorem 3.4 of [D];
    the tree version is open.
  - *Polynomials.* Analytic band elements give exponential rates.
    `C^{1,1}` band elements give `O(n^-2)`. On boxes, such an element
    would exist under an interior-pinch hypothesis and an open-boundary
    hypothesis (`w_e >= delta_0 > 0` on `∂X_e`) if the sketch of
    Proposition 4.3 (Ilmanen–Bernard insertion) were completed. Kinks at
    pinch points give `Theta(1/n)`; they need constraints or nonsmooth
    data.
  - *Link to the repository's rates: lower bounds only.* In the ideal
    relaxation (exact bag measures, separator moments of degree `2R`) the
    band identity gives the exact value. This explains the lower bounds and
    their mechanism: `Omega(R^-1)` from kinks at pinch points, and the
    `R^-2` of the quadratic example.
    - The `O(R^-2)` upper rates of [S] are only consistent with this. They
      also depend on the per-bag relaxation error (Proposition 1.4, not
      analysed here). An independent route exists only through Proposition
      4.3, which is a sketch.
    - Corollary 5.7 is derived from [S]'s theorem, so it cannot explain it.
    - [S] already proved the identities `v_n = -2 E_n(h)` and
      `eta_n = -2 E_n` (its Propositions 1 and 2). The lower bounds
      `-rho_R >= 2 E_{2R}` follow from them. Evaluating the approximation
      errors raises the constants of their explicit lower bounds by factors
      of about 7.9 and 11.8. These factors are asymptotic and numerical
      (Bernstein's constant and floating-point `E_n`), not certified.
  - *hp classes.* With cells aligned at the kinks, piecewise-analytic band
    elements give errors `C exp(-(log rho/J) N)`, exponential in the
    number `N` of split coefficients (`1.65e-10` at `N = 26`). Take
    dyadic bisection toward a kink that is not on a cell boundary, where
    each piece of the band element extends analytically across the kink.
    Then the error is at most `C' exp(-beta_1 sqrt(N))`, with
    `beta_1 = sqrt(log 2 · log rho)` (Proposition 5.8(b), elementary). The
    measured `log(gap)/sqrt(N)` is about -0.9 to -1.0.
  - *Cost.* `N` is only a proxy. The real cost is the number of bag
    subproblems (a product of the incident cell counts) times the block
    size set by the degree (Proposition 5.9). In that cost,
    piecewise-affine shells can be cheaper than hp when the band opens
    quadratically.
- **(E) Solvers.** Section 6 gives a *heuristic* adaptive rule:
  1. start from affine splits with multipliers from a local solve;
  2. refine only separators whose band is thin;
  3. split at detected kinks (active-set changes);
  4. raise the degree where the coefficients decay geometrically.

  On trees, applying one-separator decisions edge by edge with the
  original bands is unsafe (Proposition 3.3). Decisions should use the
  reduced bands of Corollary 3.4. These bound the gap by Corollary 3.4,
  but they need the parent-side value functions of the reduced problems,
  which is a global computation. The joint dual marginals are an
  untested alternative.

  The open-instance certificates of [O] are the affine case plus "full
  class", that is, merging bags, on short windows. The theory suggests
  intermediate steps (quadratic or per-cell affine splits); these are
  untested.
- **(F) Literature.** Section 8.
  - *Known in substance:*
    - the duality (A);
    - the one-sided bound "gap `<= 2 ×` approximation error, with constants
      in the class" (de Farias–Van Roy ALP);
    - its positive-width sufficiency form (Grimm–Netzer–Schweighofer's
      splitting lemma, 2007; quantitative version by
      Korda–Magron–Ríos-Zertuche);
    - the bracket form of the one-separator gap ([R, Proposition 3.3]);
    - the zero-width identity (Han–Jiao–Weissman; [S]);
    - the pinch-regularity fact (semiconcave analysis);
    - hp approximation rates;
    - the structural analogy with moment-constrained optimal transport.
  - *New as far as found:*
    - the exact identity `gap = 2 dist(Phi, Band)` with its clipping proof,
      and the max-over-cells formula;
    - the tree lower bound `2 max_e` and the counterexample to per-edge
      control;
    - the kinked-pinch `Omega(1/n)` bound;
    - the idealized shell count.

    All are elementary. An unsuccessful search does not establish
    novelty.

## 0. Setting and notation

- `X = prod_i [l_i, u_i]`. A rooted tree decomposition `(T, {V_t})` with
  running intersection; root `r`. For `t != r` the edge `e = e(t)` joins
  `t` to its parent `p(t)`; its separator is `S_e = V_t ∩ V_{p(t)}`, with
  `k_e = |S_e|`. Write `X_t = X_{V_t}`, `X_e = X_{S_e}`, `ch(t)` for the
  edges to the children of `t`, and `c(e)` for the child end of `e`.
- `F = sum_t F_t(x_{V_t})` with `F_t` bounded on `X_t` (continuous where
  stated). `f* = inf_X F`.
- A **class** `Phi_e` is a linear space of bounded functions on `X_e` that
  contains the constants. `Phi = prod_e Phi_e`.
- **Split.** For `phi = (phi_e)`,
  `F_t^phi = F_t + sum_{e in ch(t)} phi_e(x_{S_e}) - phi_{e(t)}(x_{S_{e(t)}})`
  (no last term at the root). Then `sum_t F_t^phi = F` identically.
- **Split relaxation.** `rho(Phi) = sup_{phi in Phi} sum_t inf_{X_t} F_t^phi`,
  and `gap(Phi) = f* - rho(Phi) >= 0`. By Proposition 1.3 this is also the
  bound with per-bag convex envelopes.
- **Value functions of an edge.** Let `A_e = sub(c(e))` be the child side
  and `B_e` the rest of the tree. Define
  - `U_e(s) = inf {sum_{t in A_e} F_t(x_{V_t}) : x_{S_e} = s}` (the
    subtree value function `phi*_t` of [D, Lemma 1.1]);
  - `V_e(s) = inf {sum_{t in B_e} F_t(x_{V_t}) : x_{S_e} = s}`;
  - `L_e = f* - V_e`.
- **Separator margin** `w_e = U_e - L_e = U_e + V_e - f* >= 0`. Its zero
  set, the **pinch set**, consists of the optimal separator values.
- **Band** `Band_e = {psi : X_e -> R bounded, L_e <= psi <= U_e}`.
- **Exact splits.** `E = {psi : sum_t inf_{X_t} F_t^psi = f*}`. The DP
  split `psi_e = U_e` is exact ([D, Observation 4.2]), and so is the DP
  split of every other root.
- `dist(f, Phi) = inf_{phi in Phi} sup |f - phi|`, and
  `dist(Phi, Band) = inf {sup|phi - psi| : phi in Phi, psi in Band}`.

## 1. Duality (claim A)

**Theorem 1.1 (duality; known in substance).** Assume:

- each `X_t` is compact and each `F_t` is continuous;
- each `Phi_e ⊂ C(X_e)` is a linear subspace containing the constants;
- for each bag, `M_t` is a convex set of linear functionals on `C(X_t)`,
  compact in the weak* topology, with `L(1) = 1` for every `L in M_t`.

Put `rho_M(Phi) = sup_{phi in Phi} sum_t min_{L in M_t} L(F_t^phi)`. Then

```
rho_M(Phi) = min { sum_t L_t(F_t) : L_t in M_t,  L_{c(e)}(phi_e) = L_{p}(phi_e) for all e and phi_e in Phi_e },
```

where `phi_e` is read as a function on each end bag. The minimum is
attained, and it is `+inf` if no consistent family exists.

*Proof.* Put `f(L, phi) = sum_t L_t(F_t^phi)` on `M × Phi`, with
`M = prod_t M_t`. Then
`f(L, phi) = sum_t L_t(F_t) + sum_e [L_{p(e)}(phi_e) - L_{c(e)}(phi_e)]`.

- `M` is convex and compact in the product weak* topology.
- `f(·, phi)` is affine and continuous.
- `f(L, ·)` is linear and continuous for the sup norm on `Phi`, because
  every `L_t` is a bounded functional.

Sion's minimax theorem gives `sup_phi min_L f = min_L sup_phi f`. The inner
supremum over the vector space `Phi_e` is `0` if `L_{p(e)}` and
`L_{c(e)}` agree on `Phi_e`, and `+inf` otherwise. □

**Examples.**

1. `M_t = P(X_t)` (probability measures). Then `min_L L(f) = min_{X_t} f`:
   exact bag minima. The dual family is a family of bag measures whose
   separator marginals agree on `Phi_e`. This is Lemma 1.2 of [R] on trees.
   - With `Phi_e = C(X_e)` the marginals are equal and the measures glue
     (Vorob'ev), so `rho = f*` ([D, Observation 4.2]).
2. Moment relaxations. Replace `C(X_t)` by `H_t`, the polynomials of degree
   at most `2R` in `x_{V_t}`.
   - `M_t` is the set of normalized functionals that are nonnegative on the
     truncated quadratic module of the bag's box generators
     `(u_i - x_i)(x_i - l_i)`, for example `1 - x_i^2`. It is then compact:
     localizing constraints bound the even moments, and positive
     semidefiniteness bounds the rest.
   - With the linear generators `u_i - x_i` and `x_i - l_i` alone,
     compactness can fail at low order. In 1D at order 1, `L(x^2)` is
     unbounded.
   - `Phi_e` is the separator polynomials of degree at most `2R`.
   - The dual is then the sparse Lasserre moment relaxation (Waki et al.
     2006; Lasserre 2006).
   - On a tree decomposition every representation `F = sum_t q_t` by bag
     polynomials is a polynomial split of the given one. Proof: for a leaf
     `u`, `q_u - F_u = -sum_{t != u}(q_t - F_t)` does not depend on the
     variables of `V_u \ S_u`, so it is a polynomial of `x_{S_u}`. Remove
     `u` and repeat. This is [R, Lemma 1.1] extended from paths to trees.
   - So the sparse SOS bound is `sup` over polynomial splits of the sum of
     bag SOS bounds.

**Proposition 1.2 (attainment).** Let `X` be a box, `Phi_e`
finite-dimensional, and let each `M_t` contain the point evaluations of
`X_t`. Then the supremum in Theorem 1.1 is attained.

*Proof.* Let `g(phi) = sum_t min_{M_t} L(F_t^phi)`. It is concave and finite
on a finite-dimensional space, hence continuous.

- For a direction `d`, put `D_t = sum_{e in ch(t)} d_e - d_{e(t)}`. Then
  `g(phi + sigma d) <= C(phi) + sigma sum_t min_{X_t} D_t`.
- `sum_t D_t = 0` identically, so `sum_t min D_t <= 0`, with equality only
  if every `D_t` is constant on `X_t`.
- In that case, going up from the leaves, every `d_e` is constant.
- So on the quotient by the constants (the lineality space `d_e = const`),
  `sum_t min D_t <= -kappa |d| < 0` on the unit sphere. The superlevel sets
  of `g` are bounded modulo constants, and `g` attains its maximum. □

**Proposition 1.3 (the envelope step loses nothing).** Let the bags be
boxes.

1. For every split, `min_{X_t} vex_{X_t} F_t^phi = min_{X_t} F_t^phi`.
2. For classes of continuous functions (`Phi ⊂ C`), the joint-minimum
   envelope bound
   `LB_env(phi) = min_{x in X} sum_t vex_{X_t}(F_t^phi)(x_{V_t})` satisfies
   `sup_{phi in Phi} LB_env(phi) = rho(Phi + Aff)`, where `Aff` is the class
   of affine functions. For the discontinuous cellwise classes of Section 5,
   this holds with `vex` read as the closed (lower semicontinuous) convex
   envelope (sketch below, from the review).
3. In particular `rho(Aff) = min_{x in X} sum_t vex_{X_t} F_t(x_{V_t})`: the
   affine class is exactly the per-bag convex-envelope relaxation of the
   given split.

*Proof.*

1. `vex f <= f`, and the constant `min f` is a convex minorant.
2. `vex f(p) = min {∫ f dnu : nu in P(X_t), mean nu = p}` (Jensen's
   inequality one way, Carathéodory the other).
   - So `LB_env(phi)` is the minimum of `sum_t ∫ F_t^phi dmu_t` over bag
     measures with consistent means.
   - Consistent means give one point `x`, because a variable shared by
     several bags lies in a subtree of them and consistency propagates
     along it.
   - By Theorem 1.1 with bag functions `F_t^phi` and class `Aff`, this
     equals `sup_{a in Aff} sum_t min F_t^{phi + a}`. Take the supremum over
     `phi`.
3. Take `Phi` = the constants in item 2. □

*Sketch for cellwise classes (item 2 with lower semicontinuous envelopes;
not written out in full).*

- Replace each `F_t^phi` by its lower semicontinuous hull. This changes
  neither the infimum over `X_t` nor the closed convex envelope, because
  every lower semicontinuous minorant of a function is a minorant of its
  hull.
- For a bounded lower semicontinuous `f` on a box,
  `cl vex f(p) = min {∫ f dnu : nu in P(X_t), mean nu = p}` still holds.
  The minimum is attained, and `nu -> ∫ f dnu` is lower semicontinuous in
  the weak* topology.
- Sion's theorem needs only this lower semicontinuity in the measures, so
  the proof of item 2 goes through.

So a single-tree B&B node bound with per-factor envelopes and the best
split of a class `S` ([R]) is `rho(S + Aff)` on the node box, when each
factor is one bag. Per-bag convexification never costs anything beyond the
class. Per-factor envelopes (McCormick, alphaBB) inside a bag of several
factors are weaker, and Proposition 1.4 applies to them.

**Proposition 1.4 (other per-bag relaxations).** Suppose
`M_t ⊇ P(X_t)` (a valid relaxation). Let
`delta_t(f) = min_{X_t} f - min_{M_t} L(f) >= 0` be the bag relaxation error.
Then for every `phi in Phi`

```
gap_P(Phi) <= gap_M(Phi) <= [f* - sum_t min F_t^phi] + sum_t delta_t(F_t^phi).
```

*Proof.* `min_{M_t} <= min_{P(X_t)}` gives the left inequality. For the
right one, insert `phi` in the definition of `rho_M`. □

The error `delta_t` depends on the split. alphaBB needs `alpha` at least the
curvature of `F_t^phi`; a moment relaxation needs order
`R >= deg(phi_e)/2`. A richer class makes the bags harder to relax. This is
the only place where the class and the bag relaxation interact.

## 2. One separator: the band identity (claims B and C)

Consider one edge `e` with all other edges given the full class of bounded
functions. By Observation 4.2 of [D], the two sides then behave like two
super-bags `A`, `B`, with `G_A = sum_{t in A} F_t` and `G_B` defined
likewise, value functions `U`, `V`, `L = f* - V`, and `Band = {L <= psi <= U}`.
This is made precise in the proof of Theorem 3.1. Assume the
projections of both side domains onto `S` equal `X_S`, and that `U`, `V`
are bounded.

**Theorem 2.1 (band identity).** For every linear `Phi ⊂ B(X_S)` that
contains the constants,

```
sup_{phi in Phi} [inf (G_A - phi) + inf (G_B + phi)] = f* - Delta(Phi),
Delta(Phi) = inf_{phi in Phi} [ sup (phi - U) + sup (L - phi) ] = 2 dist_inf(Phi, Band).
```

If `Phi ⊂ C(X_S)` and `U`, `L` are continuous, the band may be restricted
to continuous functions.

*Proof.*

- *First equality.* `inf(G_A - phi) = inf_s (U - phi) = -sup(phi - U)` and
  `inf(G_B + phi) = inf_s(V + phi) = f* - sup(L - phi)`.
- *Upper bound on `Delta`.* For `psi in Band` and `phi in Phi`:
  `phi - U <= phi - psi` and `L - phi <= psi - phi`. So the bracket is at
  most `osc(phi - psi) = 2 inf_c sup|phi - psi - c|`. Because `Phi + R = Phi`,
  the infimum over `phi` is at most `2 dist(psi, Phi)`.
- *Lower bound on `Delta`.* Fix `phi` with `a = sup(phi - U)` and
  `b = sup(L - phi)`. Then `a + b >= sup(L - U) = -inf w = 0`, because
  `f* = inf(U + V)`. No pinch point needs to exist.
  - Shift `phi` by a constant so that `a, b >= 0`.
  - Clip: `psi = min(max(phi, L), U)`. Then `psi` lies in `Band` (and is
    continuous if `phi`, `L`, `U` are).
  - `phi - psi` takes values in `[-b, a]`, so
    `2 dist(Phi, Band) <= osc(phi - psi) <= a + b`. □

*Constants.* Constants telescope, so `rho(Phi) = rho(Phi + R)` for every
class. The hypothesis "`Phi` contains the constants" therefore costs
nothing. For a class without constants, read the identity with `Phi + R`.

**Corollary 2.2.**

1. *Exactness.* `gap = 0` iff `dist(Phi, Band) = 0`. For finite-dimensional
   `Phi` and continuous `U`, `L`, the infimum is attained, so this happens
   iff `Phi` contains a function of the band, up to a constant.
2. *Zero width.* If `U = L` (every separator value is optimal), then
   `gap = 2 dist(U, Phi)`. With `Phi = P_n` this is the moment-matching
   identity of Han–Jiao–Weissman (Lemma 25), used in Propositions 1 and 2
   of [S].
3. *Two-sided bounds with value functions.* Since `U` and `L` are both in
   the band,
   `2 max(dist(U, Phi), dist(L, Phi)) - sup w <= gap <= 2 min(dist(U, Phi), dist(L, Phi))`.
4. *Localization.* For any `I ⊂ X_S`,
   `Delta(Phi; X_S) >= Delta(Phi|_I; I)`, where the right side uses the
   restrictions of `U` and `L` to `I`.
5. *Dual form.* By Theorem 1.1, for continuous data,
   `Delta = sup {∫ L dbeta - ∫ U dalpha : alpha, beta probability measures on X_S agreeing on Phi}`.
   A gap needs a "fooling pair" of separator laws that the class cannot
   tell apart and that the value functions price differently.

*What the identity says about (B).* The right error is not
`dist(phi*_e, Phi_e)` for the value function itself. It is the sup-norm
distance to the band. The band has width `w(s)`, which is zero on the
pinch set and grows away from it. So errors far from optimal separator
values are free up to `w(s)`. This is the precise form of "kinks away from
`x*` are harmless" ([D, Remark 3.5]) and of the band form of [R,
Proposition 3.3], whose gadget values the identity reproduces (Section
7.6).

**Proposition 2.3 (cellwise classes: the worst cell decides).** Let
`{D}` be a finite partition of `X_S`, and
`Phi = {sum_D 1_D phi_D : phi_D in Phi_D}`, where each `Phi_D` is a linear
space of bounded functions on `D` that contains the constants. Then

```
gap(Phi) = max_D g_D,     g_D = inf_{phi_D in Phi_D} [ sup_D (phi_D - U) + sup_D (L - phi_D) ],
```

where `g_D` may be negative on cells where the band is wide. For piecewise
constants, `g_D = sup_D L - inf_D U`.

*Proof.*

- `>=`: for any `phi`, `sup(phi - U) >= sup_D(phi_D - U)`, and likewise for
  the other term.
- `<=`: let `G = max_D g_D + eps`. For each cell pick `phi_D` whose bracket
  is at most `G`, and shift it by a constant so that both terms are at most
  `G/2`. □

So with exact bag minima, errors do not accumulate over the cells of one
separator. Only the worst cell counts. The discontinuous class is never
worse than the continuous spline class on the same mesh, and it costs the
same number of bag subproblems (Proposition 5.9).

## 3. Trees

**Theorem 3.1.** Let each `F_t` be bounded and each `Phi_e ⊂ B(X_e)`
linear, containing the constants. Then

```
2 max_e dist(Phi_e, Band_e)  <=  gap(Phi)  <=  2 inf_{psi in E} sum_e dist(psi_e, Phi_e)  <=  2 sum_e dist(U_e, Phi_e).
```

*Proof.*

- *Upper bound.* Let `psi in E` with `inf F_t^psi = m_t` and
  `sum_t m_t = f*`. For `phi in Phi` let `r_e = phi_e - psi_e`, with range
  `[alpha_e, beta_e]`.
  - Then `F_t^phi = F_t^psi + sum_{e in ch(t)} r_e - r_{e(t)}`, so
    `inf F_t^phi >= m_t + sum_{e in ch(t)} alpha_e - beta_{e(t)}`.
  - Summing, `rho(Phi) >= f* - sum_e osc(r_e)`.
  - Minimizing `osc(phi_e - psi_e)` over `phi_e in Phi_e` gives
    `2 dist(psi_e, Phi_e)`, because the constants are in `Phi_e`.
  - The last inequality takes `psi = U`, the DP split.
- *Lower bound.* Fix `e`. Enlarging the classes can only raise the bound.
  So `rho(Phi) <= rho(Phi')`, where `Phi'_e = Phi_e` and
  `Phi'_{e'} = B(X_{e'})` for every `e' != e`.
  - For fixed `phi_e`, the supremum over the other edges splits into one
    supremum per side.
  - On the child side it is a supremum over all bounded splits of the
    subtree `A_e`, with the bag function of `c(e)` replaced by
    `F_{c(e)} - phi_e`.
  - [D, Observation 4.2] with infima in place of minima (the DP value
    functions of bounded data are bounded, so they belong to the full
    class) makes this equal to `inf_{A_e}(G_A - phi_e)`. The same holds on
    the parent side.
  - So `rho(Phi')` is the left side of Theorem 2.1, and
    `gap(Phi) >= gap(Phi') = 2 dist(Phi_e, Band_e)`. □

**Proposition 3.2 (exact splits and bands; sequential construction).**

1. Every exact split satisfies `psi_e in Band_e + const` for every `e`.
2. Conversely, let `u` be a leaf with edge `e`. Take any `psi_e in Band_e`,
   and form the reduced tree `T \ {u}` with parent bag function
   `F_{p(u)} + psi_e`. It has the same optimal value `f*`, and every exact
   split of the reduced tree, together with `psi_e`, is an exact split of
   `T`.

*Proof.*

1. Summing the bag inequalities `F_t^psi >= m_t` over `A_e`, the inner
   splits telescope: `G_A - psi_e >= sum_{A_e} m_t`. Likewise on the other
   side. The two sums of `m_t` add up to `f*`.
2. The leaf bag has `F_u - psi_e >= U_e - psi_e >= 0`. The reduced problem
   has value `inf_s (V_e + psi_e) >= f*`, since `psi_e >= L_e`, with
   equality at a pinch point. □

The exact splits are therefore built by choosing band elements one leaf
at a time. The bands of later edges depend on earlier choices. They are
not a product of the original bands, and Proposition 3.3 shows that this
matters.

**Proposition 3.3 (per-edge band distances do not control the gap).** Take
`s1, s2 in [0, 1]`, three bags `a(s1)`, `b(s1, s2)`, `c(s2)` on a path, with

```
a = 10 (1 - s1),   c = 10 (1 - s2),   b = s1 + s2 - s1 s2,
```

and constant classes `Phi_1 = Phi_2 = R`.

- Each band contains a constant, so `dist(Band_e, R) = 0` for both edges.
- Yet `gap(R) = 1`.

*Proof.*

- `F` is multilinear, so its minimum over the square is at a vertex:
  `f* = F(1,1) = 1`. With constant splits,
  `rho = min a + min b + min c = 0`, so the gap is 1.
- Edge 1: `U_1 = 10(1 - s1)`, and
  `V_1(s1) = min_{s2}[s1 + s2 - s1 s2 + 10(1 - s2)] = 1`, attained at
  `s2 = 1` because the coefficient of `s2` is `-9 - s1 < 0`. So
  `L_1 = 0 <= 0 <= U_1`, and the constant `0` is in `Band_1`.
- Edge 2 is symmetric. □

More generally, take `b = s1 s2 + M (s1 + s2 - 2 s1 s2)` with
`1/2 < M < 1`. Then `2 dist(Band_e, R) = 1 - M` on each edge, and the sum
`2(1 - M)` is below the gap 1. `check_tree.py` (T2) reproduces `M = 0.8`:
0.2 + 0.2 against 1.

So inequality (B) of the task holds with the infimum over one joint exact
split, and fails if the infimum is taken separately on each edge.

**Remarks.**

1. *Where the gap sits between the ends of Theorem 3.1.* T1 uses bags
   `-|s1|`, `|s1| - |s2| + K(s1 - s2)^2` and `|s2|`, with `Phi = P_n` on
   both edges.
   - `K = 0`: the middle bag is separable and the upper end, the sum
     `4 E_n(|s|)`, is attained.
   - `K -> inf`: `s1 = s2` is enforced in the limit, the errors on the two
     edges cancel in the middle bag, and the gap tends to the lower end
     `2 E_n`.
     - *Proof of the limit.* Here `f* = 0`, and both bands are single
       functions with `2 dist(Band_e, P_n) = 2 E_n(|s|)`. Let `p` be a best
       approximant of `|s|` in `P_n`, take `phi_1 = phi_2 = -p`, and put
       `r = |s| - p`. The three bags become `-r(s1)`,
       `r(s1) - r(s2) + K (s1 - s2)^2` and `r(s2)`. The middle bag is at
       least `inf_d (-Lip(r)|d| + K d^2) = -Lip(r)^2/(4K)`. So
       `2 E_n <= gap <= osc(r) + Lip(r)^2/(4K) = 2 E_n + Lip(r)^2/(4K)`.
     - *Values.* `check_revision2.py` evaluates this bound for the computed
       best approximants: `Lip(r) = 1.40` (`n = 4`) and `2.40` (`n = 8`).
       At `K = 100` it gives `gap/2E_n <= 1.036` and `<= 1.208`. Grid LPs
       give 1.0008 and 1.0132 for `n = 4` (161- and 321-point grids). Grid
       gaps are lower estimates, because `f* = 0` is attained on the grid.
       The grid values of `2 E_n` in the denominators are within about
       `1e-4` (relative) of the Remez value. So for `n = 4`, `K = 100` the
       ratio lies between about 1.013 and 1.036.
     - The value 1.0000 at `K = 1000` is a grid artifact: the grid enforces
       `s1 = s2`. The bound gives at most 1.0036.
     - *Proof that the gap stays strictly above `2 E_n` at every finite
       `K`.* The confirmation proposed this proof (its remaining problem
       2); it was checked again here. Take any split in `P_n`, written
       `phi_e = -p_e`, and put `r_e = |s| - p_e`. The bags become
       `-r_1(s1)`, `r_1(s1) - r_2(s2) + K (s1 - s2)^2` and `r_2(s2)`, so
       `rho(p_1, p_2) = -max r_1 + m_B + min r_2`, where `m_B` is the
       minimum of the middle bag. Taking `s1 = s2` gives
       `m_B <= min_s (r_1 - r_2)`, so
       `-rho >= X := max r_1 - min r_2 + max_s (r_2 - r_1)`.
       - *Step 1: `X` bounds both oscillations.* Evaluating `r_2 - r_1` at
         a maximizer of `r_2` gives `X >= osc(r_2)`; at a minimizer of
         `r_1` it gives `X >= osc(r_1)`. Also `osc(r_e) >= 2 E_n`, with
         equality only if `p_e = p + const`, because the best
         approximation `p` is unique.
       - *Step 2.* So `-rho = 2 E_n` would force `r_e = r - c_e` for
         constants `c_e`. Then `r_1 - r_2 = c_2 - c_1`, and
         `-rho = osc(r) + (c_2 - c_1) - m_B`.
       - *Step 3: the middle bag falls strictly below `c_2 - c_1`.* `r` is
         not constant, because `|s|` is not a polynomial. It is a
         polynomial on each side of 0 and continuous, so `r'(s0) != 0` at
         some interior point `s0 != 0`. With `s2 = s0` and
         `s1 = s0 - delta sign(r'(s0))`, the middle bag equals
         `c_2 - c_1 - |r'(s0)| delta + O(delta^2) + K delta^2`, which is
         below `c_2 - c_1` for small `delta > 0`. So `m_B < c_2 - c_1` and
         `-rho > osc(r) = 2 E_n`, a contradiction.
       - *Conclusion.* `-rho(p_1, p_2) > 2 E_n` for every split. The
         supremum is attained (Proposition 1.2), so `gap > 2 E_n` for every
         `n` and every `K >= 0`.
       - *Numbers.* `check_revision3.py` evaluates step 3 for the split
         `-p` with `n = 4`. There `r_1 = r_2 = r`, and the middle-bag
         minimum lies below `min_s (r_1 - r_2) = 0` by at least
         `4.70e-3`, about `4.889e-4` and `4.909e-5` at `K = 100, 1000, 10^4`,
         close to `Lip(r)^2/(4K)`. The confirmation's grid LPs with up to
         2561 points give `gap/2E_4 >= 1.01477` at `K = 100` (lower
         estimates). A grid cannot show the excess at large `K`, because
         the optimal `delta` is about `|r'(s0)|/(2K)`.
   - Between these the gap interpolates (Section 7.4). Separators of one
     bag that share variables, or are tightly coupled, let errors cancel.
     Separable bags do not.
   - *The lower end is attained in other instances.* In T3 (Section 7.4)
     `gap = 2 max_e dist(Phi_e, Band_e)` holds to `1e-7` in 515 of 900
     cases. In 93 of them both per-edge values exceed `1e-4`, so the sum is
     strictly larger. An example is trial 2 with degree 0: the gap is
     1.4298 = `2 dist(Band_2)`, while `2 dist(Band_1)` = 0.3157.
     - A sufficient condition follows from the proof of the lower bound.
       Suppose the enlarged relaxation `Phi'` used there for the maximizing
       edge `e` has an optimal split whose components on the other edges
       lie in their classes `Phi_{e'}`. Then `rho(Phi) = rho(Phi')`, and
       the lower end is attained.
     - The first revision said the lower end is attained "only in trivial
       cases". That was wrong and is withdrawn.
2. *A sharper upper bound is not exact either.* Replacing `sum_e osc(r_e)`
   by `Q = sum_t sup(-R_t)`, with `R_t = sum_{e in ch(t)} r_e - r_{e(t)}`,
   also upper-bounds the gap. It can still exceed it: `Q > gap` in 249 of
   900 random instances. No exact tree formula is known.

**Corollary 3.4 (sequential bound).**

- Eliminate the edges from the leaves to the root. When edge `e` is
  reached, its child side has been reduced to one bag, and the choices for
  the earlier edges have been absorbed into their parent bags.
- Choose `phi_e in Phi_e`. Let
  `Delta_e(phi_e) = sup(phi_e - U'_e) + sup(L'_e - phi_e)` be the one-edge
  bracket of the reduced problem.

Then `gap(Phi) <= sum_e Delta_e(phi_e)`.

*Proof.* Let `u` be a leaf with edge `e`.

- `inf (F_u - phi_e) = -sup(phi_e - U_e)`.
- The reduced tree, with parent bag `F_{p(u)} + phi_e`, has optimal value
  `f* - sup(L_e - phi_e)`.
- Every split of the reduced tree, together with `phi_e`, is a split of
  `T` with the same bag functions. So
  `rho(Phi) >= -sup(phi_e - U_e) + rho(reduced)`. Induct. □

*What carries over edge by edge.* Suppose every bag's incident separators
are pairwise disjoint (for example the path of pairs `{x_i, x_{i+1}}`) and
the data are `C^{1,1}` on a box.

- Absorbing `phi_e(x_{S_e})` does not involve the variables of the later
  separators.
- The domains stay products.
- So the semiconcavity constants of Lemma 4.1 carry over to every reduced
  problem, even for discontinuous `phi_e`.
- Hence bounds that need only semiconcavity and semiconvexity
  (Proposition 5.4(a)) apply edge by edge.

*What does not carry over.*

- Quadratic growth and positive band width need not survive.
- If `phi_e = L_e`, the reduced problem is flat in `x_{S_e}`, and the next
  separator margin can vanish.
- For bags whose separators overlap, the constants may also accumulate
  (not quantified here).

## 4. Regularity at pinch points

**Lemma 4.1 (semiconcavity).** Assume the domain is a box and each `F_t`
is `M_t`-semiconcave in the separator variables uniformly in the others,
that is, `F_t - (M_t/2)|x_S|^2` is concave in `x_S` (for example
`C^{1,1}` data).

- Then `U_e` is `M_A`-semiconcave with `M_A = sum_{t in A_e, V_t ∩ S_e != ∅} M_t`.
- `V_e` is `M_B`-semiconcave, so `L_e` is `M_B`-semiconvex.

*Proof.* The other variables of the side range over a box that does not
depend on `s`. An infimum of concave functions is concave. □

The product structure is essential. If constraints tie the private
variables to the separator, value functions can have convex kinks:
`min {z : z >= s, z >= -s} = |s|`. This is the affine-recourse example of
[S].

The next lemma is a standard fact of semiconcave analysis (compare
Cannarsa–Sinestrari 2004). It also follows at once from Ilmanen's lemma: a
`C^{1,1}` function inserted between the two functions touches both at `s*`.
What this note adds is the reading "value-function bands have no kinks at
interior pinch points".

**Lemma 4.2 (pinch regularity).** Let `s*` be an interior point of `X_e`
with `w_e(s*) = 0`. Let `U_e` be `M_U`-semiconcave and `L_e`
`M_L`-semiconvex near `s*`. Then `U_e` and `L_e` are differentiable at
`s*` with the same gradient `g`, and near `s*`

```
A(s) - (M_L/2)|s - s*|^2  <=  L_e(s)  <=  U_e(s)  <=  A(s) + (M_U/2)|s - s*|^2,     A(s) = U_e(s*) + g^T (s - s*).
```

*Proof.* Let `g` be a supergradient of `U_e` at `s*` in the semiconcave
sense and `h` a subgradient of `L_e`. Then, for small `v`,
`L(s*) + h^T v - (M_L/2)|v|^2 <= L(s* + v) <= U(s* + v) <= U(s*) + g^T v + (M_U/2)|v|^2`,
and `L(s*) = U(s*)`. Put `v = tau (h - g)` and let `tau -> 0+`; this gives
`h = g`. So both generalized differentials are the same singleton, and
both functions are differentiable. □

*Consequences.*

- For box problems with `C^{1,1}` data, the value functions cannot have
  kinks at interior pinch points. Kinks may occur elsewhere, where the band
  is wide.
- The tangent `A` lies within `(max(M_L, M_U)/2)|s - s*|^2` of the band, so
  affine splits are second order at pinch points. The distances cross:
  `A` can lie below `L` by up to `(M_U/2)|s - s*|^2`.
- By the envelope theorem, `g` is the multiplier of the copy constraint of
  `S_e` at the optimum.
- At boundary pinch points the argument gives `h - g` in the normal cone
  only, so kinks in the normal direction are possible (for example
  `U = 0`, `L = s` on `[-1, 0]`). Affine band elements still exist
  locally.
- This refines Robertson–Cheng–Scott's table (order 2 for Lagrangian
  bounds with `C^2` value functions, order 1 for Lipschitz ones). On boxes,
  semiconcavity is automatic, and only the regularity at the pinch points
  matters.

**Proposition 4.3 (a `C^{1,1}` band element; sketch).** Assume the
hypotheses of Lemma 4.1 on a box, with `U_e` and `V_e` Lipschitz. Assume
also that the band is open on the boundary: `w_e >= delta_0 > 0` on
`∂X_e`. Then `Band_e` contains a `C^{1,1}` function `psi` with
`Lip(∇psi) <= M'`, where `M'` depends only on `M_A`, `M_B`, the Lipschitz
constants, `diam X_e` and `delta_0`.

*Sketch.*

1. Extend `L + (M/2)|s|^2` (convex) and `U - (M/2)|s|^2` (concave) to
   `R^k` by suprema and infima of supporting affine functions.
2. Subtract, respectively add, `K dist(s, X_e)^2` with
   `K >= G'^2/(8 delta_0)`. The extensions stay ordered outside the box,
   because `L - U <= -delta_0 + G' d - 2K d^2 <= 0` at distance `d`. They
   are `(M + 2K)`-semiconvex and `(M + 2K)`-semiconcave.
3. Apply Ilmanen's lemma in Bernard's quantitative form: the operator
   `R_t = Ť_t T_{2t} Ť_t` pinches between the two functions, and its value
   is `t`-semiconvex and `t`-semiconcave (Bernard 2010, Theorem 3).

Gaps in the sketch:

- The extension estimate in step 2 omits the `M |s|^2` terms, which do not
  cancel outside the box. A local version of the extension is needed.
- The localization needed because Bernard states the theorem for bounded
  functions on a Hilbert space is not written out.
- Pinch points on the boundary are not covered by this route. □

For polynomial box problems the rate this proposition yields
(Proposition 5.5(b)) also follows unconditionally from the repository's
kernel theorem; see Corollary 5.7.

## 5. Instances (claim D)

### 5.1 Affine classes: Lagrangian splits and an exactness criterion

**Proposition 5.1.** Let the bags be boxes and the `F_t` continuous.

1. `rho(Aff) = min_{x in X} sum_t vex_{X_t} F_t(x_{V_t})` (Proposition 1.3).
2. `gap(Aff) = 0` iff there is an affine split `phi` such that one point
   `x̄` minimizes every `F_t^phi` over `X_t`. Then `x̄` is a global
   minimizer. Conversely, for an exact affine split, every global minimizer
   `x*` minimizes every `F_t^phi`.
3. If `x*` is interior, the `F_t` are `C^1`, and an exact affine split
   exists, then its slopes are
   `lambda_{e,i} = sum_{t in A_e, i in V_t} ∂_i F_t(x*)` for `i in S_e`.
   These are the copy-constraint multipliers of [D, Lemma 3.2].
   Exactness can therefore be checked by one local solve followed by one
   global minimization per bag, each over `|V_t|` variables.
4. For one separator, `gap(Aff) = 0` iff `cav L <= vex U` on `X_S`, and
   in general `gap(Aff) = 2 dist(Aff, Band)`.

*Proof.*

2. `sum_t F_t^phi(x̄) = F(x̄) >= f* >= rho`. Equality of the bag minima with
   their values at one point forces the equalities. For the converse,
   `sum_t F_t^phi(x*) = f* = sum_t min F_t^phi`, so every term is at its
   minimum.
3. Each interior bag minimum has zero gradient. Going up from the leaves,
   `lambda_{e(t),i} = ∂_i F_t + sum_{e in ch(t), i in S_e} lambda_{e,i}`.
4. An affine function lies between `L` and `U` iff it separates the convex
   hull of the hypograph of `L` from the epigraph of `U`. The last claim is
   Theorem 2.1. □

This is the exactness mechanism of the dtoc5 and lnts certificates of [O].
There the multipliers were taken from a primal point, and per-stage global
minimality followed from convexity of the stage Lagrangian at the costate
(Mangasarian/Arrow-type sufficiency) or from the linear-tangent structure.
Wald–Globerson's tightness result for convex-decomposable continuous MRFs
is the special case in which every `F_t^phi` is convex.

### 5.2 Piecewise constants (separator branching with constant bounds)

By Proposition 2.3, `gap(PC) = max_D (sup_D L - inf_D U)`. Therefore:

- *Upper bound.*
  `gap(PC) <= max_D (min(osc_D L, osc_D U) - w_min(D)) <= max_D (G diam(D) - w_min(D))`,
  with `G` a Lipschitz constant. This is first order in the cell width.
- *Lower bound (the analogue of [D, Proposition 2.6]).*

**Proposition 5.2.** Let the separator be one-dimensional. Let `L` be
monotone with `|L'| >= |lambda|/2` on `W = [s* - r_1, s* + r_1]`, and let
`w <= (M/2)(s - s*)^2` on `W`, with `r_1 = sqrt(2 eps/M)`. If
`gap(PC) <= eps`, then at least `|lambda|/sqrt(2 M eps)` cells meet `W`.

*Proof.* Take `s1 < s2` in `D ∩ W` and `lambda > 0`. Then
`sup_D L - inf_D U >= L(s2) - U(s1) = L(s2) - L(s1) - w(s1) >= (|lambda|/2)(s2 - s1) - (M/2) r_1^2`.
So every cell meets `W` in length at most `2(eps + eps)/|lambda|`, and
`2 r_1/(4 eps/|lambda|)` cells are needed. □

Compare the bound `|lambda*|/(6 sqrt(M_F eps))` of [D, Proposition 2.6].
With adaptive cells the count is also `O(|lambda|/sqrt(c eps))`, where `c`
is the curvature of `w` (Section 7.2 measures `2.5/sqrt(eps)`).

### 5.3 Piecewise affine cells: `O(h^2)` and shells

**Proposition 5.4 (per-cell bounds for the affine class).** Let
`w_min(D) = min_D w`. Let `r_D` be the circumradius of the cell `D` about a
center `s_D`.

- (a) *One-dimensional separator.* Let `L` be `M_L`-semiconvex and `U` be
  `M_U`-semiconcave on the interval `D`. Then
  `g_D <= ((M_L + M_U)/2) r_D^2 - w_min(D)`.
- (b) *Any dimension, cell touching the pinch set.* Suppose there is a
  point `s*` in the interior of `X_e` with `w(s*) = 0`, and `L`, `U` are
  semiconvex and semiconcave on the convex set `X_e`. Then for every cell
  `D`, `g_D <= ((M_L + M_U)/2) max_{s in D} |s - s*|^2`.
- (c) *Any dimension, smooth side.* If `U` (or `L`) has an `M`-Lipschitz
  gradient on `D`, then `g_D <= M r_D^2 - w_min(D)`.

Since `gap(PA) = max_D g_D` (Proposition 2.3), each bound on all cells
bounds the gap.

*Proof.*

- (a) `Lt = L + (M_L/2)(s - s_D)^2 - (M_L/2) r_D^2` is convex with
  `Lt <= L`, and `Ut = U - (M_U/2)(s - s_D)^2 + (M_U/2) r_D^2` is concave
  with `Ut >= U`.
  - The shifted functions `Lt + w_min/2` (convex) and `Ut - w_min/2`
    (concave) are ordered.
  - On an interval, the chord of the convex function lies above it, the
    chord of the concave function lies below it, and the two chords are
    ordered at both endpoints. So the chord `l` of `Lt + w_min/2` lies
    between the two functions.
  - Then `l - U <= (M_U/2) r_D^2 - w_min/2` and
    `L - l <= (M_L/2) r_D^2 - w_min/2`.
- (b) By Lemma 4.2, applied with the global subgradient inequalities of
  semiconvex and semiconcave functions on `X_e`:
  `A - (M_L/2)|s - s*|^2 <= L <= U <= A + (M_U/2)|s - s*|^2` on all of
  `X_e`. Take `l = A`.
- (c) Take `l` the first-order Taylor polynomial of `U` at `s_D`. Then
  `l - U <= (M/2) r_D^2`, and `L - l <= U - w_min - l <= (M/2) r_D^2 - w_min`. □

*(a) is special to dimension one.* On the unit square,
`L = max(0, x + y - 1)` is convex and `U = min(x, y)` is concave, with
`L <= U`.

- Both equal `xy` at the four vertices, so no affine function lies between
  them. The affine gap is `1/2`.
- For `U + delta` with `0 < delta < 1/2`, the affine *cell bracket* `g_D`
  is `1/2 - delta > 0`, even though the band has width `delta`.
  (`U + delta` is not the band of a problem, since `inf w > 0`.)
- In dimension `k >= 2`, convex kinks of `L` and concave kinks of `U` can
  therefore block affine splits at first order. This is why (b) and (c)
  need a pinch point or a smooth side.
- With `delta = 0` this is the band of a box problem with bilinear data
  (observed by the review):
  - child bag `u s1 + (1 - u) s2`, `u in [0, 1]`, so `U = min(s1, s2)`;
  - parent bag `v (1 - s1 - s2)`, `v in [0, 1]`, so `L = max(0, s1 + s2 - 1)`
    and `f* = 0`.

  The pinch set is the whole boundary of the square. So with smooth box
  data, boundary pinch sets can defeat affine splits at first order in 2D.
  The interior hypothesis of Lemma 4.2 carries real weight.

*Uniform cells.* Consider a one-dimensional separator of a box problem
with `C^{1,1}` data.

- Lemma 4.1 gives the hypotheses of (a).
- So cells of width `h` give `gap(PA) <= (M_L + M_U) h^2/8`, with kinks
  allowed anywhere.
- In dimension `k`, (c) gives `M k h^2/4` when `U_e` is `C^{1,1}`.

**Corollary 5.5 (shells: `O(log(1/eps))` cells for one separator;
tiling corrected after review).** Assume:

- a unique pinch point `s*`, in the interior of `X_e`;
- quadratic growth of the separator margin, `w_e(s) >= c |s - s*|^2`. This
  follows from quadratic growth of `F` with the same `c`, because
  `w_e(s) = inf {F - f* : x_S = s}`;
- for `k >= 2`: `U_e` has an `M`-Lipschitz gradient on a ball
  `B(s*, rho_0)`. This holds, for example, at a nondegenerate interior
  minimizer, by the implicit function theorem.

Let `Q = Q(s*, rho_0/sqrt(k))` be the sup-norm cube inscribed in the ball.
Its side is `q0 = 2 rho_0/sqrt(k)`. Let `s_e` be the largest side of `X_e`.

- Inside `Q`, build the shell partition of [D, Lemma 3.1] around `s*`,
  with central side `h = sqrt(4 eps/(M k))` and `theta` the largest power
  `2^{-mu}` (`mu >= 0` an integer, as [D, Lemma 3.1] requires) that is at
  most `sqrt(4 c/(M k))`. So `theta <= 1`, and `theta = 1` when
  `c >= M k/4`.
- On `X_e \ Q`, use a grid aligned with `∂Q` whose cubes have diameter at
  most `c rho_0^2/(2 k G)`, where `G` is a Lipschitz constant of `U_e` and
  `L_e`.

Then, for `eps` small enough that `h <= q0`, `gap(PA) <= eps` with at most

```
(log2(q0/h) + 2)(4/theta)^k + O((1 + G s_e k^{3/2}/(c rho_0^2))^k)   cells,   that is,   O(max(16 M k/c, 16)^{k/2} log(1/eps)) + O_eps(1).
```

Here `(4/theta)^k <= max(16 M k/c, 16)^{k/2}`. If `theta < 1`, then
`theta > (1/2) sqrt(4 c/(M k))`, so `4/theta < 4 sqrt(M k/c)`. If
`theta = 1`, then `(4/theta)^k = 16^{k/2}`. The second case matters: for
`k >= 2` nothing ties `c` to `M`, and when `c > M k` the bound
`4 sqrt(M k/c)` is below 4. In dimension 1, (a) replaces (c): the
smoothness assumption and the outer region are not needed.

*Proof.*

- *Inside `Q`.* A cube of side `sigma` has `r = sigma sqrt(k)/2`. Central
  cubes give `M k h^2/4 <= eps`. Outer shell cubes have
  `sigma <= theta d_inf <= theta d`, where `d_inf` and `d` are the sup-norm
  and Euclidean minimum distances of the cube to `s*`. So
  `M r^2 <= M k theta^2 d^2/4 <= c d^2 <= w_min`. Apply (c).
- *Outside `Q`.* Every point has Euclidean distance at least
  `rho_0/sqrt(k)` from `s*`, so `w >= c rho_0^2/k`. On a cube of diameter
  at most `c rho_0^2/(2 k G)`, the constant `(sup_D L + inf_D U)/2` gives a
  negative bracket. □

*Trees.*

- By Corollary 3.4, uniform piecewise-affine cells on paths with scalar,
  pairwise-disjoint separators give `gap <= sum_e (M_{L,e} + M_{U,e}) h^2/8`.
- The shell count does not transfer this simply. A reduced problem can
  lose quadratic growth: absorbing a split near the bottom of a band
  removes the separator margin seen by later edges.
- A tree version needs a drift analysis like the one in Theorem 3.4 of
  [D]. There, a copy-drift condition forces `theta ~ c_g/M`, against
  `theta ~ sqrt(c/M)` for one separator here.
- **For trees the shell count is open in this model.**

Comparison with Theorem 3.4 of [D] (one separator):

- Same shells, same `log(1/eps)`, same need for slopes.
- The base is `max(16 M k/c, 16)^{k/2}` per separator of dimension `k`.
  [D] has `(C M sqrt(w)/c_g)^{w+1}` per bag, because it also pays for
  branching inside bags and for copy drift.
- The split relaxation separates the consistency cost across separators
  (this section) from the relaxation cost inside bags (Proposition 1.4).

### 5.4 Polynomial classes and the sparse moment rates

**Proposition 5.5 (polynomial rates for one separator).**

- (a) If `Band` contains `psi` analytic and bounded by `M` in the Bernstein
  ellipse `E_rho` of `X_S = [-1, 1]`, then `gap(P_n) <= 4 M rho^{-n}/(rho - 1)`.
- (b) If `Band` contains `psi in C^{1,1}(X_S)`, `X_S` a `k`-dimensional box,
  then `gap(P_n) <= 2 C_k Lip(∇psi)/n^2`.
- (c) Proposition 5.6 below: a kink at a pinch point gives
  `gap(P_n) = Theta(1/n)`, even when the band opens quadratically.

*Proof.* Theorem 2.1 gives `gap <= 2 E_n(psi)`. For (a) use the Chebyshev
truncation bound (Trefethen, *Approximation Theory and Approximation
Practice*, Theorem 8.2). For (b) use the multivariate Jackson theorem for
functions with Lipschitz gradient (for example Bagby–Bos–Levenberg 2002);
the constant `C_k` is not computed here. □

**Proposition 5.6 (kinked pinch: `Omega(1/n)`).** Take the model band on
`[-1, 1]` with `U = -|s|` and `L = -|s| - c s^2`, `c >= 0`. Then for
`n >= 1`

```
gap(P_n) >= 1 / (30 (3 + c) n),
```

and `gap(P_n) <= 2 E_n(|s|) ~ 2 beta/n`, with Bernstein's constant
`beta = 0.2801694990`.

More generally, let `I = [s* - r, s* + r]` and suppose there are an affine
`A` and constants `kappa > 0`, `c >= 0` with `U <= A - kappa|s - s*|` and
`L >= A - kappa|s - s*| - c (s - s*)^2` on `I`. Then, by Corollary 2.2(4)
and scaling,
`gap(P_n) >= kappa r/(30 (3 + c r/kappa) n)`.

*Proof.*

1. *Set-up.* Let `p in P_n` achieve bracket value `2 delta`, and center it
   so that `max(p - U) = max(L - p) = delta`. If `delta >= min(1/8, 1/n)`
   the claim holds. So assume `delta < min(1/8, 1/n)`. From `s = 0`,
   `|p(0)| <= delta`.
2. *Divided difference.* `q(s) = (p(s) - p(0))/s` is a polynomial of
   degree `n - 1`. The band gives:
   - for `s > 0`: `-1 - c s - 2 delta/s <= q(s) <= -1 + 2 delta/s`;
   - for `s < 0`: `1 - 2 delta/|s| <= q(s) <= 1 + c|s| + 2 delta/|s|`.

   Hence `|q| <= C := 3 + c` for `|s| >= delta`, `q(4 delta) <= -1/2`, and
   `q(-4 delta) >= 1/2`. So `|q'(xi)| >= 1/(8 delta)` for some
   `|xi| <= 4 delta`.
3. *`q` stays bounded in the gap `[-delta, delta]`.*
   - The even part is `r(s^2)`, with `r` of degree at most `(n-1)/2` and
     bounded by `C` on `[delta^2, 1]`.
   - Chebyshev's extremal property bounds `r` on `[0, delta^2]` by
     `C |T_m(-(1 + delta^2)/(1 - delta^2))| <= C ((1 + delta)/(1 - delta))^m`.
   - The odd part is `s u(s^2)`, with `|u| <= C/delta` on `[delta^2, 1]`.
     The same bound gives `|s u(s^2)| <= C ((1+delta)/(1-delta))^m` for
     `|s| <= delta`.
   - With `delta < 1/n` and `delta < 1/8`,
     `((1+delta)/(1-delta))^{(n-1)/2} <= exp(8/7)`. So
     `max_{[-1,1]} |q| <= 2 e^{8/7} C <= 6.3 C`.
4. *Conclusion.* Bernstein's inequality at `|xi| <= 1/2` gives
   `|q'(xi)| <= (n-1) 6.3 C/0.866 <= 7.3 C (n-1)`. With step 2,
   `delta >= 1/(58.4 C (n-1))`, so `gap = 2 delta >= 1/(30 C n)`.
5. *Upper bound.* `psi = U` lies in the band. The asymptotics of `E_n(|s|)`
   are Bernstein's theorem. □

Numerically `n gap(P_n)` keeps rising for `c = 0.5, 2, 8` (Section 7.1).
At `n = 128` the grid-LP values are 0.49, 0.42 and 0.33. These are lower
estimates: the fine-grid re-evaluations give 0.50, 0.48 and 0.53.

The bound of Proposition 5.6 is loose. The ratio of the computed gap to
the bound is `30 (3 + c) n gap` (`check_revision2.py`; values for
`n <= 32` agree with the review's R3):

- about 18 to 72 for `2 <= n <= 32`;
- 105 to 330 at `n = 1`;
- 51.0, 63.1 and 107.5 at `n = 128` for `c = 0.5, 2, 8` (from the lower
  estimates).

Among the computed degrees (`n = 1, 2, 3, 4, 8, 16, 32, 64, 128`), the
ratio grows with `c` at `n = 1` and for `n >= 16`. It falls with `c` at
`n = 2, 3, 4` (at `n = 2` it is 35.0, 25.0 and 18.3 for `c = 0.5, 2, 8`),
and it is not monotone at `n = 8` (40.0, 36.5, 39.2)
(`check_revision3.py`).

*Conjecture.* `n gap(P_n) -> 2 beta` for every `c >= 0`. The heuristic:
at the resolution `1/n` of degree-`n` polynomials, the band width `c s^2`
is negligible near the pinch point. This heuristic is weak. The band width
`c s^2` exceeds the error scale `1/n` once `|s| >~ 1/sqrt(c n)`. So
outside a shrinking neighbourhood of 0 the band is not negligible, and the
limit may be smaller than `2 beta`. The data are consistent with either
outcome and do not show the limit.

**Curvature jump at a pinch point.** Take `U = -(s_+)^2` and
`L = U - c s^2`.

- `c = 0` is the quadratic example of [S], where the gap is
  `Theta(n^{-2})` (proved there).
- For `c >= 1` the band contains `-s^2`, so the gap is 0 for `n >= 2`.
- For `0 < c < 1`:
  - no polynomial of any degree lies in the band, because the second
    derivative at 0 would have to lie in `[-2c, 0] ∩ [-2 - 2c, -2]`;
  - `O(n^{-2})` is proved, because `U` is `C^{1,1}` and lies in the band
    (Proposition 5.5(b));
  - the computed `n^2 gap` levels off at values that fall steeply with
    `c`: about `0.28`, `0.03`, `0.004`, `5e-4` and `7e-6` for
    `c = 0, 0.1, 0.3, 0.5, 0.8`;
  - the matching `Omega(n^{-2})` is **numerical only**.

**What this says about the repository's sparse rates (lower bounds
only).** In the ideal relaxation (exact bag measures, separator moments
through degree `2R`), the gap is exactly `2 dist(P_{2R}, Band)` for one
separator. It is a lower bound for the sparse SDP gap, because actual
measures are feasible for the SDP. So the identity explains the lower
bounds and their mechanism.

For the upper rates it does not explain [S]:

- the SDP gap also contains the per-bag relaxation error
  (Proposition 1.4), which is not analysed here;
- the only independent route to `dist(P_n, Band) = O(n^-2)` is
  Proposition 4.3, which is a sketch and needs an interior pinch point;
- Corollary 5.7 is derived from [S]'s theorem.

| Repository result ([S], closing summary) | Band structure at the pinch set | Consequence here |
|---|---|---|
| Sparse box preordering `O(R^-2)`; ordinary module `O(log^3 R/R^2)` | Box, polynomial data: `U` semiconcave, `L` semiconvex (Lemma 4.1); pinch points `C^1` (Lemma 4.2) | Consistent: `O(R^-2)` for the ideal relaxation, conditional on Proposition 4.3 (a sketch). The SDP rate also needs the bag relaxation error |
| Quadratic example, `Omega(R^-2)` | Zero width, curvature jump of `(y_+)^2` | Value `2 E_{2R}((y_+)^2)` ([S], Proposition 1). `n^2 gap` = 0.2880, 0.2836, 0.2814 at `n = 64, 128, 256`, decreasing, extrapolated limit about 0.279. So the gap is about `0.070/R^2`, against the elementary `2/(27 pi (2R+2)^2)`, about `0.0059/R^2` |
| Affine recourse `Theta(R^-1)` | Constraints `z >= ±y` give `V = \|y\|`, a convex kink; zero width | Value `2 E_{2R}(\|y\|)` ([S], Proposition 2), asymptotically `beta/R = 0.280/R` (Bernstein), against the elementary `1/(9 pi (R+1))`, about `0.035/R` |
| Regular multipliers give `O(R^-2)` | Lipschitz multiplier = `∇U` (envelope theorem), so `U in C^{1,1}` | Consistent with Proposition 5.5(b) for the ideal relaxation |
| Fixed private polytope gives `O(R^-2)` | Private domain independent of the separator, so Lemma 4.1 applies | No kinks at pinch points |

Both identities in the second and third rows were already proved in [S]
(Propositions 1 and 2). The only gain here comes from evaluating the
approximation errors.

- *Affine recourse.* The asymptotic ratio is `9 pi beta = 7.92`. At finite
  `R`, the ratios are 11.5, 9.8, 8.9, 8.4 and 8.2 for `R = 2, 4, 8, 16, 32`.
- *Quadratic example.* The asymptotic ratio is about 11.8. At
  `R = 2, 4, 8, 16, 32` it is 42, 23.5, 16.9, 14.2 and 13.0.
- All finite-`R` ratios were recomputed here from the E1 and E2 values of
  Section 7.1; they agree with the review's.
- These are asymptotic or floating-point values, not certified finite-`R`
  bounds. Certification would need interval de la Vallée Poussin bounds.

**Corollary 5.7 (derived from [S], so not an explanation of it).** For
polynomial objectives on boxes with one separator, combining Theorem 2.1
with the repository's sparse preordering theorem ([S], `O(R^-2)`) gives
`dist(P_{2R}, Band) = O(R^-2)`.

- For each `n`, the band contains an element within `O(n^{-2})` of `P_n`.
- The element may depend on `n`; no single band function with
  `E_n = O(n^{-2})` is claimed.
- No boundary hypothesis is needed.

*Summary of the dichotomy.* Measured against the band, polynomial
approximation of separator value functions gives the exact ideal-relaxation
gap. This explains the lower bounds: `Omega(R^-1)` when constraints create
kinks at optimal separator values (Proposition 5.6), and `Theta(R^-2)` in
the quadratic example. The `O(R^-2)` upper rates of [S] for semiconcave
value functions are consistent with it, and are explained by it only
conditionally on Proposition 4.3 and on a separate analysis of the bag
relaxation error. Only the pinch set matters: a kink away from the optimal
separator values, as in E4, leaves the degree-2 class exact. The explicit
band element there is `T - kappa (s - 0.3)^2` for any
`kappa in [1.296, 1.5]`.

### 5.5 hp classes: piecewise polynomials on adaptively refined cells

**Proposition 5.8 (hp classes for a piecewise-analytic band element).**
Let `X_S = [a, b]` and let the band contain `psi` that is analytic on each
closed piece `[c_{j-1}, c_j]`, `j = 1..J`. That is, the affine image of
`psi` on the piece extends analytically to the Bernstein ellipse `E_rho`
and is bounded by `M` there. Since `rho > 1`, the ellipse contains a
complex neighbourhood of the closed piece, including its endpoints. For
example, `-|s - c0| + (entire function)` qualifies, but
`|s - c0|^{4/3}` does not.

- (a) *Aligned cells: exponential in the number of split coefficients
  (trivial given the alignment).* Take the cells to be the pieces and
  degree `p` on each. Then

  ```
  gap <= 4 M rho^{-p}/(rho - 1),     N = J (p + 1)   so   gap <= (4 M rho/(rho - 1)) exp(-(log rho / J) N).
  ```

- (b) *Unaligned breakpoint, dyadic bisection.* Let `J = 2`, with one
  breakpoint `c` inside `(a, b)`, and let `psi` be continuous, hence
  Lipschitz with some constant `G`.
  - Bisect `m` times toward `c`: at each step, split the *kink cell* at its
    midpoint. The kink cell is the cell that contains `c`; once `c` is a
    common endpoint of two cells, it is the left one of them. (From then
    on every cell lies in one closed piece. The proof below still
    applies: the inclusion argument bounds every cell other than the kink
    cell, and the oscillation bound bounds the kink cell.)
  - Use degree `p` on the `m` other cells, and degree 1 on the kink cell.

  Then

  ```
  gap <= max( 4 M rho^{-p}/(rho - 1),  G (b - a) 2^{-m} ),     N = m (p + 1) + 2.
  ```

  With `p = ceil(m log 2/log rho)` this gives `gap <= C 2^{-m}`, with
  `C = max(4 M/(rho - 1), G (b - a))`, and
  `N <= (log 2/log rho) m^2 + 2m + 2`. That is,
  `gap <= C' exp(-beta_1 sqrt(N))`, with
  `beta_1 = sqrt(log 2 · log rho)` and `C' = C rho e^{beta_1 sqrt 2}`.

*Proof.* By Proposition 2.3, `gap = max_D g_D`. By Theorem 2.1 on each
cell, `g_D <= 2 E_{p_D}(psi|_D)`.

- (a) Proposition 5.5(a) on each cell.
- (b), cells other than the kink cell. Such a cell `D` lies in one closed
  piece `I`. Bernstein ellipses are monotone under inclusion:
  `E_rho(D) ⊂ E_rho(I)`.
  Indeed, with `R = (rho + 1/rho)/2 >= 1`,
  `E_rho(I) = {z : |z - a_I| + |z - b_I| < |I| R}`. If
  `|z - a_D| + |z - b_D| < |D| R`, the triangle inequality gives
  `|z - a_I| + |z - b_I| < |D| R + (|I| - |D|) <= |I| R`. So Proposition
  5.5(a) applies on `D` with the same `rho` and `M`, however close `D` is
  to `c`.
- (b), the kink cell. It has width `(b - a) 2^{-m}`, so
  `2 E_1(psi|_D) <= 2 E_0(psi|_D) = osc_D psi <= G (b - a) 2^{-m}`.
- (b), counting. There are `m` cells with `p + 1` coefficients and one
  cell with 2. The choice of `p` makes `4 M rho^{-p}/(rho - 1)` at most
  `4 M 2^{-m}/(rho - 1)`. Put `beta_0 = log 2/log rho`. Solving
  `N <= beta_0 m^2 + 2m + 2` for `m` gives
  `m >= sqrt((N - 2)/beta_0) - 1/beta_0`. Since
  `(log 2)/sqrt(beta_0) = sqrt(log 2 · log rho) = beta_1` and
  `2^{1/beta_0} = rho`, this gives
  `2^{-m} <= rho exp(-beta_1 sqrt(N - 2)) <= rho e^{beta_1 sqrt 2} exp(-beta_1 sqrt(N))`. □

Kinks, that is, breakpoints of piecewise-analytic band elements, cost
nothing if a cell boundary sits on them (a). If no cell boundary sits on
the kink, grading needs its approximate location, for example bisection
toward a detected kink, as a branch-and-bound would do. Then (b) gives
`C' exp(-beta_1 sqrt(N))` in the sup norm. With dyadic bisection toward
the kink, the measured `log(gap)/sqrt(N)` stays near `-1` (Section 7.5).

*Why the distance to the kink does not matter in (b).* The first revision
argued that the cells left behind by bisection sit at "a fixed relative
distance from the kink". For dyadic bisection that is false (next
paragraph), but under the hypothesis of Proposition 5.8 it is also
unnecessary. A cell next to the kink is as good as any other cell of its
piece. `check_revision2.py` confirms this for the note's test function
(Section 7.5). Take the level-4 cell `[0.25, 0.375]`, whose distance to
`c0 = 1/sqrt 7` is only 0.047 of its half-width. Its errors `2 E_p`,
`p = 1..4`, are within factors 0.7 to 1.7 of those on the same-width cell
`[0.125, 0.25]`.

*Algebraic singularities at breakpoints (not proved here).* If a piece's
analytic continuation is singular at the breakpoint, as for `|s|^{4/3}`
from `min_x (x^4/4 - s x)`, Proposition 5.8 does not apply, and the
relative distance of the cells to the breakpoint matters.

- Dyadic bisection does not keep this distance bounded below. For
  `c0 = 1/sqrt 7`, the distance of each cell left behind to `c0`, divided
  by the cell's half-width, is 0.047 at level 4 and 0.071 at level 11. At
  the other levels up to 15 it is between 0.48 and 1.91.
- The effect is visible. For `-|s - c0|^{4/3} + 0.3 sin(3s) + 0.2 s^2`,
  the errors on the level-4 cell exceed those on `[0.125, 0.25]` by
  factors 2.0, 4.2, 54 and 181 for `p = 1..4` (`check_revision2.py`).
- A geometric mesh around an approximately known breakpoint `c~` keeps
  the relative distance bounded below. It has cells
  `[c~ + sigma^{j+1}, c~ + sigma^j]` and their mirror images, and a
  central cell that contains the breakpoint. Classical hp theory then
  suggests a rate `exp(-b' sqrt(N))` for some `b' > 0`, but this is not
  proved here.
- For sup-norm free-knot, variable-degree approximation of `x^beta` see
  DeVore–Scherer (1980). Gui–Babuška (1986) treat singularities at mesh
  nodes in the energy norm.
- Semialgebraic value functions of polynomial problems in 1D are
  piecewise algebraic and can have such singularities.

**Proposition 5.9 (what a degree of freedom costs).** Let each edge carry
a cellwise class with box cells `P_e` and degrees `p_D`.

- The number of split coefficients is
  `N_e = sum_{D in P_e} binom(k_e + p_D, k_e)`. In the measure form these
  are the consistency equations of edge `e`.
- The bag bound `inf_{X_t} F_t^phi` splits over the common refinement of
  the incident partitions. So bag `t` has
  `n_t <= prod_{e incident to t} |P_e|` subproblems, with equality for
  disjoint separators and product cells.
- Each subproblem minimizes the smooth function `F_t ± phi_{e,D}` over a
  box of dimension `|V_t|`. With a dense moment relaxation of order
  `R_t >= max(deg F_t, max p)/2`, it costs a PSD block of side
  `binom(|V_t| + R_t, R_t)` plus localizing blocks.
- In measure form: one measure per subproblem, and
  `sum_e N_e` linear consistency equations.

*Consequences.*

- `N` is not the cost driver. It is a proxy that is meaningful only in the
  idealized exact-bag model. All `N` comparisons in this note (Sections 6
  and 7.5) are proxy comparisons, not cost comparisons.
- The cell counts multiply the subproblems of each incident bag. On a path
  of pairs, `n_t = J_{e(t)} J_{child}`, so shells with `O(log(1/eps))`
  cells per separator cost `O(log^2(1/eps))` fixed-size subproblems per
  bag.
- Aligned hp reaches `eps` with `p ~ log(1/eps)`. The incident blocks then
  have side `binom(|V_t| + p/2, p/2) ~ (log(1/eps))^{|V_t|}/|V_t|!`.
- So when the band opens quadratically, piecewise-affine shells can be
  cheaper in real cost than hp, already for `|V_t| >= 3`. When the band
  has zero width, shells do not apply: piecewise-affine cells then need
  `eps^{-1/2}` cells, and hp is cheaper.
- [D] avoids this product by letting bag leaves meet several cells, at the
  price of copy drift.
- Raising the degree on one cell enlarges every subproblem of the two
  incident bags that meets the cell. The block side grows like
  `R^{|V_t|}/|V_t|!`.
- The discontinuous class is never worse than the continuous spline class
  and costs the same.

## 6. Consequences for solvers (claim E)

**What decides the refinement, per separator.** Only the part of the
separator where the band is thin needs attention: the pinch set and its
neighbourhood, where `w_e` is below the target. There are four cases.

1. *`C^1` pinch, analytic nearby.* This is automatic at interior pinch
   points of box problems with smooth data (Lemma 4.2).
   - Affine splits are second order.
   - Piecewise-affine shells need `O(log(1/eps))` cells for one separator
     (Corollary 5.5; for trees this is open).
   - Raising `p` on the pinch cell converges geometrically.
2. *Curvature jump at a pinch point* (`C^{1,1}`, not `C^2`), for example an
   active-set change of a private variable at the optimal separator value.
   - Polynomials give only `n^-2`.
   - A cell boundary at the jump restores the geometric rate.
3. *Kink at a pinch point.* This needs constraints coupling private and
   separator variables, or nonsmooth data.
   - Polynomials and misaligned cells lose `Theta(1/n)` or first order
     (Proposition 5.6).
   - A cell boundary must be placed at the kink (h-refinement); then `p`.
4. *Kinks and curvature jumps away from the pinch set* are harmless while
   the band is wider than the target. Do not refine there.

**Adaptive rule (heuristic).** The rule below is a heuristic. Parts of it
are justified for one separator.

- *Justified parts.* Step 1 follows from Proposition 5.1(2)–(3): local
  multipliers are the only candidate slopes for an exact affine split at an
  interior `C^1` optimum. The check certifies only if `x̂` is a global
  minimizer. That kinks away from the pinch set are harmless follows from
  Proposition 2.3 and E4.
- *Heuristic.* The decay threshold (0.8) and the kink detector were tested
  on one 1D function.
- *Unsafe on trees.* Applying step 3 edge by edge with the *original*
  `U_e` and `w_e` is not justified. After earlier splits are absorbed, the
  bands can be thinner (Corollary 3.4). Proposition 3.3 shows that
  original-band diagnostics can report zero loss on every edge while the
  gap is 1. On trees, base the decisions on the reduced bands of the
  sequential elimination. By Corollary 3.4 they bound the gap, but they
  need the parent-side value functions of the reduced problems. The joint
  dual marginals of Theorem 1.1 are a possible alternative that has not
  been tested.

1. Solve a local problem. Take affine splits with the copy multipliers
   (Proposition 5.1(3)). Solve each bag globally.
   - If `sum_t min F_t^phi` reaches the incumbent, stop: the affine class
     is exact.
   - Otherwise the bags whose minimizers leave `x̂` identify the separators
     to refine. In the dual, their separator marginals disagree outside the
     class.
2. On a flagged separator, sample the child-side values `U_e(s)` at a few
   points of the cells carrying the dual mass (parametric subtree solves),
   and record the private minimizer `y*(s)`.
3. For each such cell:
   - if `w_e` is known to exceed the target on the cell (from quadratic
     growth estimates or current bounds), leave it;
   - else, if `y*(s)` changes active set or jumps inside the cell, split
     at the detected location (aligned h);
   - else, if the Chebyshev coefficients of the samples decay
     geometrically (factor below about 0.8), raise `p` by one;
   - else bisect.
4. Choose between candidate refinements by predicted gain per unit cost
   (Proposition 5.9). A new cell adds `prod_{other incident edges} |P_e'|`
   subproblems. A degree step grows the incident blocks polynomially.

On the one-dimensional test (Section 7.5), this rule with kink-location
splitting reaches about `3e-10` (a grid-LP lower estimate) with `N = 32`
coefficients on 6 cells. With midpoint bisection instead, it needs
`N = 124` on 42 cells. Uniform piecewise-affine cells with `N = 512` stall
at `3.7e-3`, and one global polynomial with `N = 33` reaches `1.6e-2`.
These are comparisons in the proxy `N`, not in cost (Proposition 5.9). On a
zero-width band like this one, hp is also cheaper in cost. With a band that
opens quadratically, piecewise-affine shells can be cheaper.

**Relation to the open-instance certificates [O].**

- *dtoc5 and lnts.* The certificates are affine splits with multipliers
  from a primal point, checked by per-stage global minimization. That is
  the exactness criterion of Proposition 5.1: for dtoc5 the stage
  Lagrangian is convex at the costate; for lnts see [O, Section 3].
- *camshape.* The generic cell-constant DP failed. This is consistent with
  Proposition 5.2 and Theorem 3.1.
  - Constants lose first order in the cell width at every separator with a
    nonzero multiplier.
  - The upper bound adds these losses over the `n` separators.
  - [O, Section 8.1] measured that the per-stage constraint scale falls
    like `1/n^2`, so cells of width `O(1/n^2)` were needed.
  - The certificate that worked used bound propagation, not a split class.
- *optcdeg2.*
  - The Lagrangian failed only in windows where `lam_t < 0` made the
    `v`-terms concave, so the bag minima jumped to interval ends. In band
    terms, the band there contains no affine function.
  - The certificate made the head window exact, which amounts to the full
    class on those separators.
  - Cells in `v` alone with fixed multipliers failed because they cannot
    represent a band element that couples `y` and `v`. The report's remedy
    ("multipliers re-optimized per cell") is exactly the piecewise-affine
    class of Section 5.3.
- *lukvle10.* The pair Lagrangian was nonconvex only at the end transient.
  Three pairs were kept exact and a 2D interval B&B was run on the entry
  separator. That is h-refinement with full classes on a short window.
- *Suggested, untested.* Quadratic or per-cell affine splits on the
  offending separators (E4 shows a case where degree 2 closes a gap that
  affine splits cannot) might replace some exact windows.

## 7. Numerical checks

All values are optimal values of floating-point LPs on grids. For one
separator the LP computes `Delta(Phi)` of Theorem 2.1 directly. The grid
value is a lower estimate of the continuum gap (fewer constraints).
Re-evaluating the optimal split on a grid 10 to 25 times finer gives an
upper estimate. The two agree to the digits shown unless noted.

### 7.1 Polynomial classes (`check_band_1d.py`, `check_pinch_rates.py`)

The examples all have `f* = 0` and separator `s in [-1, 1]`.

- E1: `U = L = -|s|` (affine recourse).
- E2: `U = L = -(s_+)^2` (quadratic example).
- E3: `U = L = (s+2) - (s+2) log(s+2)` (analytic, singular at `-2`).
- E4: `U = 0.7 s - s^2 - 0.5|s + 0.5|` and `L = T - 1.5(s - 0.3)^2`, where
  `T` is the tangent of `U` at `s* = 0.3` (slope `-0.4`). The kink of `U`
  lies away from the pinch point, and `w = 0.5 (s - 0.3)^2` for
  `s >= -0.5`.
- E5(c): `U = -(s_+)^2`, `L = U - c s^2`.
- E6(c): `U = -|s|`, `L = U - c s^2`.

| n | E1 gap (`n gap`) | E2 gap (`n^2 gap`) | E3 gap | E4 gap | E6(0.5) `n gap` |
|---|---|---|---|---|---|
| 1 | 1.0 | 0.5625 | 0.264 | 1.205 | — |
| 2 | 0.2500 (0.500) | 0.1716 (0.686) | 2.3e-2 | 0 | 0.333 |
| 4 | 0.13524 (0.541) | 0.02763 (0.442) | 5.1e-4 | 0 | 0.357 |
| 8 | 0.069379 (0.555) | 5.549e-3 (0.355) | 6.8e-7 | 0 | 0.381 |
| 16 | 0.034936 (0.559) | 1.233e-3 (0.316) | < 2e-11 | 0 | 0.409 |
| 32 | 0.017500 (0.5600) | 2.901e-4 (0.297) | < 1e-13 | 0 | 0.437 |
| 64 | 0.0087539 (0.5602) | 7.030e-5 (0.288) | < 1e-13 | 0 | 0.463 |
| 128 | — | — | — | — | 0.486 (lower estimate; upper 0.502) |

- E1 reproduces Bernstein's constant: `2 beta = 0.5603`.
- E4 is exact from `n = 2`: the kink away from the pinch point is harmless.
  The zeros are exact, as the explicit band element
  `T - kappa (s - 0.3)^2`, `kappa in [1.296, 1.5]`, shows. The LP's
  fine-grid re-evaluations rise to `7e-5` at `n = 64` and are only
  tolerance effects.
- E2: `n^2 gap` is still decreasing at `n = 64`. `check_revision.py`
  computes 0.28802, 0.28358 and 0.28138 at `n = 64, 128, 256`. The
  differences halve, so the limit is about 0.279.
- E6: `n gap` keeps rising: for `c = 0.5`, 0.36 → 0.49; for `c = 2`,
  0.20 → 0.42; for `c = 8`, 0.08 → 0.33 (`n = 4 → 128`). The `n = 128`
  values are lower estimates; the fine-grid re-evaluations give 0.50, 0.48
  and 0.53. This is consistent with `Theta(1/n)` (Proposition 5.6). A
  limit of `2 beta` is only conjectured.
- E5 (`n^2 gap`, lower estimates): for `c = 0.1`, 0.164, 0.065, 0.041,
  0.033, 0.030 at `n = 4..64`; for `c = 0.5`, 4.6e-3, 1.2e-3, 7.2e-4,
  5.8e-4, 5.3e-4; for `c >= 1`, 0.
  - For `n >= 32` and `c >= 0.3` the fine-grid upper estimates are loose
    (up to 60 times the lower ones), so those entries are lower estimates
    only.

### 7.2 Cellwise classes (`check_band_1d.py`)

Uniform meshes with `J` cells:

| J | E1c PC (`c0 = 1/sqrt 7`) | E1c PA | E4 PC (`gap/h`) | E4 PA (`gap/h^2`) |
|---|---|---|---|---|
| 4 | 0.5000 | 0.1845 | 1.030 (2.06) | 6.17e-2 (0.247) |
| 16 | 0.1250 | 5.79e-3 | 0.0956 (0.77) | 3.85e-3 (0.247) |
| 64 | 0.03125 | 5.37e-3 | 0.0154 (0.49) | 2.41e-4 (0.247) |
| 128 | 0.015625 | 4.80e-3 | 6.98e-3 (0.45) | 5.37e-5 (0.220) |

- Piecewise constants on E1c give exactly `h`, which matches the closed
  form of Proposition 2.3.
- On E1c the piecewise-affine gap stalls near `2ab/(a+b)`, where `a` is the
  distance from the kink to the dyadic node `0.375` next to it. This is a
  misaligned kink.
- On E4 the piecewise-affine gap is `O(h^2)`, below the one-dimensional bound
  `3h^2/8` of Proposition 5.4. That bound was checked cell by cell: the
  largest `g_D - bound_D` is negative for `J = 4..64`.
- Continuous hats give the same values as discontinuous piecewise-affine
  functions here.
- The two-dimensional example after Proposition 5.4 (`check_2d_sandwich.py`)
  has affine cell bracket `g_D` exactly `1/2 - delta` for
  `delta = 0, 0.1, ..., 0.5` (grid LP), although `M_L = M_U = 0` there.
  - It is a band gap only for `delta = 0`.
  - The log's value `-0.1` at `delta = 0.6` is a negative cell bracket, not
    a gap.
  - So the one-dimensional bound (a) indeed fails in dimension 2.
- Proposition 2.3 was checked against one joint LP for 9 meshes. The
  largest difference is 6.7e-8 (one case with gap ≈ 0); the rest are at or
  below 4e-13.
- Adaptive bisection on E4 until the per-cell gap is at most `eps`:

| eps | 1e-2 | 1e-3 | 1e-4 | 1e-5 | 1e-6 |
|---|---|---|---|---|---|
| PC cells (`cells × sqrt(eps)`) | 37 (3.7) | 96 (3.0) | 254 (2.5) | 854 (2.7) | 2586 (2.6) |
| PA cells | 6 | 8 | 11 | 14 | 16 |

Constants need `Theta(eps^{-1/2})` cells (Proposition 5.2). Affine cells
need `O(log(1/eps))` (Corollary 5.5).

### 7.3 Duality with explicit bags (`check_duality.py`)

- E1 with bags `-x s` (`x in [-1,1]`) and `z` (`|s| <= z <= 1`), and E4
  with a three-variable child bag, on aligned grids.
- The split LP, the measure LP of Theorem 1.1 and `f* - Delta` agree to
  `1e-8` for `n = 1, 2, 4, 6, 8`. Example: E1, `n = 4`, value
  `-0.13461538`.
- The optimal bag measures put no mass off the conditional minimizers.

### 7.4 Trees (`check_tree.py`; log regenerated in the second revision, Section 11)

T1: bags `-|s1|`, `|s1| - |s2| + K (s1 - s2)^2` and `|s2|`, with `P_n` on
both edges. The value `gap/(2 E_n)` measures where the gap sits between the
maximum (1) and the sum (2) of Theorem 3.1:

| K | 0 | 0.3 | 1 | 3 | 10 | 100 |
|---|---|---|---|---|---|---|
| `n = 4` | 2.000 | 1.815 | 1.580 | 1.323 | 1.127 | 1.001 |
| `n = 8` | 2.000 | 1.869 | 1.681 | 1.439 | 1.206 | 1.004 |

These are 161-point grid values, which are lower estimates. On a 321-point
grid the `n = 4`, `K = 100` value is 1.0132 (`check_revision.py`). The
bound `gap <= 2 E_n + Lip(r)^2/(4K)` of Section 3 gives at most 1.036
(`n = 4`) and 1.208 (`n = 8`) at `K = 100` (`check_revision2.py`). So the
lower end (ratio 1) is approached as `K -> inf`. It is not attained at any
finite `K` (proof in Section 3, Remarks, from the confirmation).

- T2: the Proposition 3.3 family with `M = 0.8`, constants. The gap is 1,
  while the per-edge values are `2 dist(Band_e) = 0.2` each. With affine,
  `P_2` or `P_4` classes the gap is 0.
- T3: 300 random three-bag instances with 5-point separators, classes of
  degree 0, 1 and 2 (900 cases).
  - `max_e <= gap <= Q <= joint bound` held in every case.
  - `Q > gap` in 249 cases (largest excess 1.76).
  - The per-edge sum `sum_e 2 dist(Band_e, Phi_e)` was below the gap in
    247 cases.
  - The lower end `2 max_e dist(Band_e, Phi_e)` equals the gap (to `1e-7`)
    in 515 cases. In 93 of them both per-edge values exceed `1e-4`, so the
    lower end is attained while the sum is strictly larger (for example
    trial 2, degree 0: gap 1.429786 = `2 dist(Band_2)`, while
    `2 dist(Band_1)` = 0.315654). This count was added in the second
    revision; it reproduces the recheck's count.

### 7.5 h, p and hp (`check_hp.py`)

Zero-width band `U = L = psi` with
`psi(s) = -|s - c0| + 0.3 sin(3s) + 0.2 s^2` and `c0 = 1/sqrt(7)`. Here
`N` is the number of split coefficients.

| strategy | N | gap |
|---|---|---|
| one cell, `p = 8 / 16 / 32` | 9 / 17 / 33 | 6.4e-2 / 3.2e-2 / 1.6e-2 |
| uniform PA, `J = 16 / 64 / 256` | 32 / 128 / 512 | 7.8e-3 / 5.5e-3 / 3.7e-3 |
| two cells split at `c0`, `p = 4 / 8 / 12` | 10 / 18 / 26 | 6.17e-3 / 2.42e-6 / 1.65e-10 |
| dyadic bisection toward `c0`, `m = 8 / 12 / 14` levels, best `p` | 42 / 86 / 100 | 3.7e-3 / 6.5e-5 / 5.0e-5 |
| adaptive, midpoint splits (tolerance 1e-3 / 1e-6 / 1e-9) | 31 / 65 / 124 | 9.8e-4 / 9.7e-7 / 9.5e-10 |
| adaptive, split at the detected kink (tolerance 1e-3 / 1e-6 / 1e-9) | 14 / 21 / 32 | 1.6e-4 / 5.4e-7 / 3.2e-10 (lower estimate) |

- Aligned hp is exponential in `N`. The `p = 12` value `1.65e-10` comes
  from `check_revision.py`, which applies the LP to the residual after
  Chebyshev interpolation, and it agrees with the review's Remez bracket.
  The first version, `1.3e-10`, was a grid-LP value at the solver
  tolerance. Grid-LP values below about `1e-9` in this table, such as the
  adaptive `9.5e-10` and `3.2e-10`, are lower estimates.
- `N` is a proxy, not a cost (Proposition 5.9).
- Dyadic geometric refinement gives `log(gap)/sqrt(N)` between `-0.86` and
  `-1.04` for `m = 4..14`. This is consistent with the bound of
  Proposition 5.8(b). The best uniform degree is only 4 or 6, and the kink
  cell dominates the gap at every `m` (`check_revision2.py`, check (2c)).
- Dyadic bisection leaves cells very close to the kink: at level 4 the cell
  `[0.25, 0.375]` is at distance 0.047 of its half-width from `c0`, and at
  level 11 at 0.071. This does not hurt here, because the pieces of `psi`
  extend to entire functions. On `[0.25, 0.375]`, the errors `2 E_p`
  (`p = 1..4`) are within factors 0.7 to 1.7 of those on `[0.125, 0.25]`.
  For the variant with `-|s - c0|^{4/3}`, the factors are 2.0, 4.2, 54 and
  181 (`check_revision2.py`; Section 5.5).
- Adaptive midpoint splitting gives `log(gap)/sqrt(N) ≈ -1.9` at 1e-9.
- A first version of the decay indicator treated round-off-level
  coefficients as algebraic decay and over-bisected (411 coefficients at
  1e-5). The logged version treats coefficients below `1e-13 × max` as
  converged.

### 7.6 Cross-check with [R] (`check_gadget.py`)

The band gap of the gadget of [R, Proposition 3.3] is `0.07612` for
`d = 2, 3`, and `0.00777`, `0.00237`, `0.00078` for `d = 4, 6, 8`. These
equal the values reported there.

## 8. Literature (claim F)

Sources were checked at the level stated. "Abstract" means only the
abstract or a secondary summary was read.

**Duality (A) is known in substance.**

- Cost shifting and reparametrization in graphical models and weighted CSP
  (the independent review of [R] reached the same conclusion):
  - Wainwright, Jaakkola, Willsky, MAP estimation via agreement on trees,
    IEEE Trans. Inf. Theory 2005;
  - Werner, a linear programming approach to the max-sum problem, IEEE
    Trans. PAMI 2007;
  - Sontag, Globerson, Jaakkola, Introduction to dual decomposition for
    inference (2011);
  - Cooper, de Givry, Schiex et al. on soft arc consistency and cost
    shifting, including per-node shifting in weighted-CSP B&B.
- For continuous variables, Wald and Globerson, Tightness results for
  local consistency relaxations in continuous MRFs, UAI 2014 (text read):
  - they define a "weak LCR" with test functions `psi_i` (their Eq. 8);
  - their dual (Lemma 3.1) is a reparametrization with multipliers
    `<delta, psi_i>`, which is Theorem 1.1 for pairwise models;
  - their Theorem 4.1 (tightness for convex-decomposable models with
    `psi_i = x_i`) is the convex case of Proposition 5.1.
- Moment-matching constraints between factors are also the fixed-point
  conditions of expectation propagation and expectation consistency
  (Heskes et al., JSTAT 2005; Opper–Winther, JMLR 2005; abstracts), in the
  sum-product rather than the min-sum setting.
- Sparse moment relaxations as the polynomial case: Waki et al. 2006;
  Lasserre 2006. Gluing on trees: Vorob'ev 1962.
- [R, Lemma 1.2] is the path case in this repository.

**The principle of (B), "relaxation error ≤ 2 × best approximation of the
value function in the class, with constants in the class", has direct
precursors.**

- de Farias and Van Roy, The linear programming approach to approximate
  dynamic programming, Oper. Res. 51 (2003):
  - the approximate LP restricts the cost-to-go to a linear architecture
    and gives a lower bound on it;
  - its error satisfies `||J* - Phi r~||_{1,c} <= (2/(1 - alpha)) min_r ||J* - Phi r||_inf`
    when the constant function is in the span. This is quoted from
    Lakshminarayanan–Bhatnagar–Szepesvári (arXiv 1704.02544), whose text
    was read; the NeurIPS 2001 version, also read, states the
    Lyapunov-weighted form (its Theorem 3.1);
  - its dual aggregates flow-balance constraints by the basis functions,
    the analogue of agreement on `Phi_e`;
  - The upper bound of Theorem 3.1 is the deterministic, tree-structured,
    undiscounted counterpart, and the constant `2` has the same origin
    (shifting the best approximant by a constant).
  - On a path with the DP split it *is* the deterministic finite-horizon
    ALP bound: the ALP constraints `Phi_t r_t <= g_t + Phi_{t+1} r_{t+1}`
    are the split relaxation. That case is known in substance.
  - New here are the infimum over all exact splits, the `2 max_e` lower
    bound, and the counterexample to per-edge control.
- Alfonsi, Coyaud, Ehrlacher, Lombardi, Approximation of optimal transport
  problems with marginal moments constraints, Math. Comp. 2021 (arXiv
  1905.05663v1; Section 5 read in the first two revisions, and the
  statements of Propositions 5.7 and 5.9 and Corollaries 5.8 and 5.10
  reread in the third):
  - marginal equalities are relaxed to agreement on test functions;
  - Proposition 5.1 gives `I^N <= I <= I^N + K/N` for piecewise-constant
    test functions and a `K`-Lipschitz cost on `[0, 1]^2`;
  - for piecewise-affine test functions, Section 5.2 gives "a rough
    calculation" (a Taylor heuristic) of why they "may lead to" `O(1/N^2)`
    for costs that are `C^1` with Lipschitz gradient. The authors add that
    "such kind of a result is not obvious";
  - the `O(1/N^2)` rates they prove are for two specific costs:
    - `W_1`, cost `|x - y|` (not smooth), for absolutely continuous
      marginals with a bounded density difference `rho_mu - rho_nu` and
      finitely many sign changes of `F_mu - F_nu` (Proposition 5.7,
      Corollary 5.8). They remark that boundedness of `rho_mu - rho_nu`
      near the sign changes suffices;
    - `W_2^2`, cost `|x - y|^2`, under bounded densities (Proposition 5.9,
      Corollary 5.10);
    - the proofs go through cumulative distribution functions;
  - so their rates depend on the cost and on the regularity of the
    marginals. They do not come from approximating the Kantorovich
    potentials, as the first version of this note said;
  - the structural analogy with Sections 5.2 and 5.3 (cellwise test
    functions; first against second order) stands.
- Korda, Henrion, Jones, Convergence rates of moment-sum-of-squares
  hierarchies for optimal control problems, Syst. Control Lett. 2017
  (abstract): an `O(1/log log d)` rate through polynomial approximation of
  the value function combined with effective Putinar bounds.
- Grimm, Netzer, Schweighofer (GNS), A note on the representation of
  positive polynomials with structured sparsity, Arch. Math. 89 (2007) 399–403
  (arXiv math/0611498v1; Lemma 3 and its proof read in the second
  revision):
  - to split `f = f_1 + f_2 >= eps > 0`, they take the separator fiber
    minimum `h(y) = min_x f_1(x, y) - eps/2`;
  - they show `f_1 - h >= eps/2` and `f_2 + h >= eps/2`, and approximate
    `h` by a polynomial (Weierstrass, no degree bound);
  - this is the qualitative sufficiency direction of Theorem 2.1 for a
    band of positive width, in the SOS setting.
- Nie, Qu, Tang, Zhang (Math. Program. 2026): the sparse hierarchy is tight
  iff `f - f_min` splits into nonnegative bag polynomials. This is
  Corollary 2.2(1) and Proposition 1.2 for SOS bags.
- Han, Jiao, Weissman (COLT 2018, Lemma 25): the zero-width case of
  Theorem 2.1 (via [S]).
- Korda, Magron, Ríos-Zertuche (KMR), Convergence rates for sums-of-squares
  hierarchies with correlative sparsity, Math. Program. 209 (2025)
  435–473. The bibliographic data were checked through Crossref. The text
  read is arXiv 2303.14824v1, the only arXiv version, which was read in
  the first two revisions. Lemma numbers here are those of arXiv v1; the published
  numbering was not checked.
  - KMR call their Lemma 11 "a version of [4, Lemma 3]", where [4] is
    Grimm–Netzer–Schweighofer (above);
  - to split `f = f1 + f2 >= eps`, they take
    `g(x) = min_y f2(x, y) - eps/2`, a one-sided value function shifted
    into the `eps`-widened band;
  - they approximate it by a Jackson polynomial to within `eps/2 - eta`;
  - this is the quantitative version of GNS's sufficiency direction, with
    first-order (Lipschitz) approximation and degree bounds;
  - neither lemma contains the equality or the clipping (necessity)
    direction.

**hp and value functions.**

- Cibulka, Korda, Haniš: spatio-temporal splitting of SOS programs for
  regions of attraction, with piecewise polynomials on cells and optimized
  split locations (IJRNC 2024, abstract). This is the closest found use of
  cell refinement for SOS relaxations. No rates relative to value-function
  regularity were seen.
- ADP with polynomial or quadratic value functions (Wang, O'Donoghue, Boyd,
  iterated Bellman inequalities, 2015; Summers et al., ADP via SOS, 2013;
  abstracts).
- hp-FEM approximation theory (Gui–Babuška 1986; Schwab 1998) covers
  singularities at mesh nodes in the energy norm. It does not cover the
  unaligned sup-norm case of Section 5.5. There, Proposition 5.8(b) gives
  an elementary bound when each piece extends analytically across the
  breakpoint. Algebraic singularities at breakpoints are not covered.
- Ilmanen's lemma (Ilmanen 1993; Bernard 2010, Theorem 3, text read;
  Fathi–Zavidovique 2010) supplies Proposition 4.3. Lemma 4.2 follows from
  it and is standard in semiconcave analysis (Cannarsa–Sinestrari,
  *Semiconcave functions, Hamilton–Jacobi equations, and optimal control*,
  2004).
- DeVore and Scherer, "Variable knot, variable degree spline approximation
  to `x^beta`", in *Quantitative Approximation*, Academic Press 1980
  (bibliographic level): sup-norm free-knot, variable-degree rates
  relevant to Section 5.5.
- Robertson, Cheng, Scott (JOGO 2025; via the literature audit): the
  order table that Lemma 4.2 refines.

**Novelty (revised after review).**

*Known in substance:*

- the duality (A);
- the zero-width identity (Han–Jiao–Weissman; [S]);
- the one-sided bound "gap `<= 2 ×` approximation error, with constants in
  the class" (de Farias–Van Roy's ALP), and its positive-width sufficiency
  form (Grimm–Netzer–Schweighofer 2007, Lemma 3; quantitative version in
  Korda–Magron–Ríos-Zertuche, Lemma 11);
- the bracket form of the one-separator gap ([R, Proposition 3.3 and
  Section 3.4]);
- the pinch-regularity fact (semiconcave analysis);
- hp approximation rates;
- the evaluation constants for [S]'s identities (Bernstein's constant is
  classical).

*New as far as found:*

1. the exact identity `gap = 2 dist(Phi, Band)` with its clipping proof,
   and the max-over-cells formula (Proposition 2.3);
2. the tree lower bound `2 max_e` and the counterexample to per-edge
   control (Proposition 3.3);
3. the kinked-pinch `Omega(1/n)` bound for positive band width
   (Proposition 5.6);
4. the idealized shell count (Corollary 5.5).

All four are elementary; their value is in organizing the quantity that
matters, namely the distance to the band localized at the pinch set. The
review's searches (Lagrangian bounds with restricted multiplier classes,
continuous-MRF dual decomposition, ALP) found no statement of items 1–2.
An unsuccessful search does not establish novelty.

## 9. Status

All proofs of the first version were checked by the independent review,
and the first revision by the recheck. The second revision (Section 12.2)
added two arguments, Proposition 5.8(b) and the T1 limit in Section 3. The
confirmation
([`../reviews/recheck-consistency-confirm.md`](../reviews/recheck-consistency-confirm.md))
checked both step by step, tested both numerically, and found them
correct. The third revision (Section 12.3) adds the proof that the T1 gap
stays strictly above `2 E_n` at every finite `K`. The confirmation proposed and
checked it; it was checked again here.

| Item | Content | Status |
|---|---|---|
| Theorem 1.1 | duality with compact convex per-bag relaxations | proved; known in substance (Section 8); generators stated for compactness |
| Proposition 1.2 | attainment for finite-dimensional classes | proved |
| Proposition 1.3 | per-bag envelopes lose nothing; joint envelopes = `Phi + Aff` | proved for continuous classes; lsc envelopes for cellwise classes: **sketch** |
| Proposition 1.4 | gap = consistency gap + bag relaxation error | proved |
| Theorem 2.1 | band identity `gap = 2 dist(Phi, Band)` (one separator) | proved (proof step fixed); zero-width case (HJW) and sufficiency direction (GNS; quantitative: KMR) prior |
| Corollary 2.2 | exactness, value-function bounds, localization, dual | proved |
| Proposition 2.3 | cellwise classes: worst cell decides; PC closed form | proved; checked against a joint LP |
| Theorem 3.1 | tree bounds `2 max_e <= gap <= 2 inf_E sum_e` | proved; upper end attained (T1); lower end attained in 515 of 900 T3 cases (93 with both edge terms positive), and in T1 approached as `K -> inf` but not attained at any finite `K` (limit proved in the second revision and checked in the confirmation; strictness proved in the confirmation, checked again here and added in the third revision); path/DP case = finite-horizon ALP bound |
| Proposition 3.2 | exact splits project into bands; sequential construction | proved |
| Proposition 3.3 | per-edge band distances do not bound the tree gap | proved (explicit example); T2, T3 |
| Corollary 3.4 | sequential bound `gap <= sum_e Delta_e`; which hypotheses carry over | proved |
| Lemma 4.1 | semiconcavity of value functions on product domains | proved |
| Lemma 4.2 | pinch regularity (interior) | proved; classical (semiconcave analysis) |
| Proposition 4.3 | `C^{1,1}` band element on boxes (interior pinch) | **sketch** (Ilmanen–Bernard; extension and localization not written) |
| Proposition 5.1 | affine exactness criterion, slopes = copy multipliers | proved |
| Proposition 5.2 | PC lower bound `\|lambda\|/sqrt(2 M eps)` cells | proved (1D) |
| Proposition 5.4 | PA per-cell bounds: (a) 1D `((M_L+M_U)/2) r^2 - w_min`; (b) pinch cells; (c) `C^{1,1}` side | proved; (a) checked numerically; (a) fails in 2D (explicit example, realized by bilinear box data with a boundary pinch set) |
| Corollary 5.5 | shells `O(max(16 Mk/c, 16)^{k/2} log(1/eps)) + O_eps(1)` cells, one separator (`k >= 2` needs `C^{1,1}` near `s*`) | proved (given [D, Lemma 3.1]); tiling corrected after review; `theta <= 1` case and box sides fixed in the second revision; tree version open |
| Proposition 5.5 | polynomial rates (analytic, `C^{1,1}`) | proved modulo cited Jackson constant |
| Proposition 5.6 | kinked pinch `gap(P_n) >= 1/(30(3+c)n)` | proved |
| `n gap -> 2 beta` for `c > 0` | limit for kinked pinch with positive width | conjecture; weak heuristic; the limit may be smaller |
| Curvature jump, `0 < c < 1` | `O(n^-2)` proved; `Omega(n^-2)` | lower half numerical only |
| Corollary 5.7 | `dist(P_n, Band) = O(n^-2)` for polynomial box problems | proved from [S]'s theorem; does not explain it |
| Section 5.4 link to [S] | exact ideal-relaxation values; lower bounds | lower bounds explained; upper rates only consistent (conditional on Proposition 4.3 and bag error) |
| Constants 7.9 and 11.8 | evaluation of [S]'s identities | asymptotic and floating point, not certified |
| Proposition 5.8(a) | aligned hp: `C exp(-(log rho/J) N)` | proved (trivial given alignment) |
| Proposition 5.8(b) | unaligned breakpoint, dyadic bisection: `gap <= C' exp(-beta_1 sqrt N)`, `beta_1 = sqrt(log 2 · log rho)` | proved (elementary; each piece extends analytically across the breakpoint; added in the second revision, checked in the confirmation); consistent with the numerics of Section 7.5 |
| algebraic singularity at a breakpoint | `exp(-b' sqrt N)` with geometric meshes | not proved; dyadic bisection does not keep relative distances bounded below; DeVore–Scherer for `x^beta` |
| Proposition 5.9 | cost accounting; `N` only a proxy | proved (counting) |
| Section 6 rule | adaptive h/p choice | heuristic; tested on one 1D function; edge-by-edge use with original bands unsafe on trees |

## 10. Limitations and open questions

- *Idealization.* The main results assume exact bag minima, equivalently
  per-bag convex envelopes. Weaker bag relaxations add a split-dependent
  error (Proposition 1.4) that is not analysed here beyond the statement.
- *Trees.*
  - The upper and lower bounds differ by up to the number of edges. Both
    ends are attained in some instances (the lower end in 515 of the 900
    T3 cases). In T1 the lower end is approached as `K -> inf` but not
    attained at any finite `K` (proved in Section 3). No exact tree
    formula is known; the bag-wise quantity `Q` is not one.
  - How much coupling in a bag lets separator errors cancel is not
    quantified.
  - The shell count of Corollary 5.5 is proved for one separator only;
    reduced problems can lose quadratic growth (Corollary 3.4).
- *Dimension.*
  - Proposition 5.4(a) and the kinks-anywhere statements hold for
    one-dimensional separators only.
  - In higher dimensions the affine class needs a pinch point in the cell
    or a `C^{1,1}` side (the example after Proposition 5.4).
  - Propositions 5.2, 5.6 and 5.8 are one-dimensional.
- *Proposition 4.3* is a sketch. Boundary pinch points are not covered by
  this route; for polynomial box problems, Corollary 5.7 covers them
  through the repository's theorem.
- *The curvature-jump rate for `0 < c < 1`.* Only its lower half is
  numerical, and the fine-grid brackets are loose for `n >= 32`.
- *The kinked pinch with positive width.* The limit `2 beta` is a
  conjecture with weak heuristic support; the limit may be smaller.
- *The sparse-rate link* explains the lower bounds only. The upper rates
  need the bag relaxation error and Proposition 4.3.
- *The factors 7.9 and 11.8* evaluate [S]'s own identities. They are
  asymptotic or floating-point, not certified.
- *hp.*
  - Unaligned breakpoints: `gap <= C' exp(-beta_1 sqrt(N))` is proved for
    dyadic bisection when each piece extends analytically across the
    breakpoint (Proposition 5.8(b)). Algebraic singularities at breakpoints are not
    covered. For them, dyadic bisection can leave cells very close to the
    breakpoint, and a geometric mesh around an approximately known
    breakpoint would be needed.
  - Rankings by `N` are proxy comparisons. In real cost, piecewise-affine
    shells can beat hp when the band opens quadratically.
  - The adaptive rule is a heuristic tested on one 1D function with a
    known kink detector (the second difference of samples). A solver would
    detect active-set changes of private minimizers instead.
  - On trees the rule should use the reduced bands of Corollary 3.4,
    which bound the gap but need parent-side value functions. The joint
    dual marginals are an untested alternative.
  - Multi-dimensional separators and cost-aware choices were not tested.
- *Solver relevance.*
  - Nothing here was run inside a B&B solver or on MINLPLib instances.
  - The link to the open-instance certificates is interpretive.
  - The suggested intermediate classes (P2 or per-cell affine on the
    failing windows) are untested.
- *Numerics.* All computations are floating point. Values below about
  `1e-7` are at the LP tolerance, except in `check_pinch_rates.py` and
  `check_hp.py`, which use `1e-10`.
- *Literature.* Several sources were checked through abstracts or
  secondary statements only (Section 8). Novelty is not established.

## 11. Commands run (all in this directory; targeted checks only)

```
python3 check_band_1d.py     # logs/check_band_1d.log   (95 s)
python3 check_pinch_rates.py # logs/check_pinch_rates.log (about 15 min)
python3 check_tree.py        # logs/check_tree.log (see note below; 18 s)
python3 check_hp.py          # logs/check_hp.log (run twice; second run fixed the decay indicator)
python3 check_duality.py     # logs/check_duality.log
python3 check_gadget.py      # logs/check_gadget.log
python3 check_2d_sandwich.py # logs/check_2d_sandwich.log
python3 check_revision.py    # logs/check_revision.log (first revision)
python3 check_revision2.py   # logs/check_revision2.log (second revision; 53 s)
python3 check_revision3.py   # logs/check_revision3.log (third revision; 9 s)
```

*Note on `logs/check_tree.log`.* The first version ran `check_tree.py`
twice; the second run added the per-edge count. `check_tree.py` then
opened its log in write mode at import time, and `check_revision.py`
imports it. Running `check_revision.py` in the first revision therefore
emptied the log. In the second revision the log is opened only under
`__main__` (the same fix was made in `check_hp.py`, which
`check_revision2.py` imports). T3 also gained the attainment count, and
`check_tree.py` was rerun to regenerate the log. The regenerated log agrees
line by line with the recheck's scratch rerun
(`../reviews/consistency-recheck-checks/logs/check_tree_rerun_scratch.log`),
apart from the four new lines of the attainment count. `logs/check_hp.log`
was not regenerated: the fix changes only where the file is opened.

Environment: Python 3.13, numpy 2.5.1, scipy 1.18.0 (HiGHS); second and
third revisions run with `OMP_NUM_THREADS=1`. No project-wide verification and no
CI inspection were done.

Files: `consistency_lib.py` (band LP, cellwise classes, bases),
`check_band_1d.py`, `check_pinch_rates.py`, `check_tree.py`, `check_hp.py`,
`check_duality.py`, `check_gadget.py`, `check_2d_sandwich.py`,
`check_revision.py`, `check_revision2.py`, `check_revision3.py`, `logs/`.

## 12. Revision after review

### 12.1 First revision (after the review)

The review ([`../reviews/consistency-review.md`](../reviews/consistency-review.md),
checks in `../reviews/consistency-review-checks/`) found every proof
correct. It asked for the corrections below. Each change was verified by
the author as stated. The recheck later confirmed these changes, except
where a pointer to Section 12.2 says otherwise.

1. **Quadratic example (F1).**
   - "`n^2 gap -> 0.288`" was wrong: 0.288 is the value at `n = 64`, and
     the sequence still decreases.
   - `check_revision.py` computes 0.28802, 0.28358 and 0.28138 at
     `n = 64, 128, 256`. The differences halve, so the extrapolated limit is
     about 0.279, and the ideal gap about `0.070/R^2`.
   - Changed in Sections 5.4 and 7.1.
2. **Improvement factors (F2).**
   - "About 8 and 12" became about 7.9 (`9 pi beta`) and about 11.8,
     asymptotic and numerical.
   - The finite-`R` ratios were recomputed from the Section 7.1 values.
   - Both identities are credited to [S] (Propositions 1 and 2). The gain
     comes only from evaluating the approximation errors.
3. **"Explains the rates" (F3).** Restricted to the lower bounds and to the
   ideal relaxation.
   - The `O(R^-2)` upper rates also need the bag relaxation error and
     Proposition 4.3 (a sketch).
   - Corollary 5.7 is derived from [S]'s theorem, so it cannot explain it.
     Its wording now claims a band element per `n`, not one fixed
     function.
4. **hp (F7–F9).**
   - The aligned `p = 12` value is `1.65e-10`, verified by residual LP and
     interpolant bounds in `check_revision.py`; the first version gave
     `1.3e-10`, a value at the solver tolerance. Small grid-LP values are
     labelled as lower estimates.
   - The Gui–Babuška citation for kinks inside cells was replaced by an
     elementary argument and DeVore–Scherer. The self-contradictory
     sentence about unknown kink locations was removed. (The elementary
     argument had a false step; replaced by Proposition 5.8(b), Section
     12.2, item 3.)
   - `N` is now called a proxy throughout. Proposition 5.9 compares real
     costs: piecewise-affine shells can be cheaper than hp when the band
     opens quadratically.
5. **Literature (F4, F5, F20).**
   - Alfonsi et al.'s rates come from the regularity of the cost (their
     Proposition 5.1 and the Taylor argument in Section 5.2). This was
     verified in arXiv 1905.05663. (Still imprecise; corrected in Section
     12.2, item 4.)
   - Lemma 4.2 is marked classical.
   - Korda–Magron–Ríos-Zertuche's Lemma 11 uses the sufficiency direction
     of the band identity with a positive-width band. This was verified in
     arXiv 2303.14824, and it is cited. (The qualitative form is due to
     Grimm–Netzer–Schweighofer; Section 12.2, item 5.)
   - The path/DP-split upper bound of Theorem 3.1 is identified with the
     finite-horizon ALP bound.
6. **Tree lower bound (F6).** "Attained" became "approached as
   `K -> inf`". `check_revision.py` gives ratios 1.0008 and 1.0132 at
   `K = 100` on 161- and 321-point grids (lower estimates). (This revision
   also added, without the review asking for it, that the lower end is
   attained "only in trivial cases". That claim was false; it was withdrawn
   in Section 12.2, item 1.)
7. **Solver rule (F14).** It is labelled heuristic in the summary and in
   Section 6. Edge-by-edge use with the original bands is flagged as
   unsafe on trees (Proposition 3.3). Decisions should use reduced bands or
   joint dual marginals. (Only the reduced-band route is backed by a
   result; Section 12.2, item 7(c).)
8. **Novelty.** Rewritten. New as far as found:
   - the exact identity with its clipping proof, and the max-over-cells
     formula;
   - the tree lower bound and the counterexample;
   - the kink bound;
   - the shell count.

   All are elementary.
9. **Smaller fixes.**
   - F10: the tiling in Corollary 5.5 now uses the inscribed cube, and the
     constant `16^{k/2}` is explicit. (The `theta = 1` case and the box
     sides were fixed in Section 12.2, item 6.)
   - F11: box generators are stated for compactness of the moment sets.
   - F12: in Theorem 2.1, `a + b >= 0` follows from `inf w = 0`; a remark
     says the constants hypothesis costs nothing.
   - F13: Proposition 1.3(2) is restricted to continuous classes, with lsc
     envelopes for cellwise ones; the summary says "per-bag". (The lsc
     argument is written out as a sketch in Section 12.2, item 7(b).)
   - F16: `n gap -> 2 beta` for `c > 0` is a conjecture.
   - F18:
     - `58.1` became `58.4`;
     - the script docstrings were renumbered;
     - the 2D `delta > 0` values are called cell brackets `g_D`;
     - the E4 zeros are backed by the explicit band element
       `T - kappa (s - 0.3)^2`, `kappa in [1.296, 1.5]`, rederived here;
     - the review's bilinear box realization of the 2D example was
       added.
   - The curvature-jump entry now states that `O(n^-2)` is proved; only
     `Omega(n^-2)` is numerical.

Commands added in the first revision: `python3 check_revision.py` (about
3 minutes; `logs/check_revision.log`). Only this directory's targeted
checks were run; no project-wide verification and no CI inspection.

### 12.2 Second revision (after the recheck)

The recheck ([`../reviews/consistency-recheck.md`](../reviews/consistency-recheck.md),
checks in `../reviews/consistency-recheck-checks/`) recomputed the first
revision's numbers and found them right, and found no proof wrong. It
asked for the fixes below. Each point was verified before the text was
changed. Items 1 and 3 add arguments that had not been checked
independently at the time. (The confirmation later checked both and found
them correct; Section 12.3.)

1. **Lower end of Theorem 3.1: a false claim withdrawn.**
   - *What was wrong.* The first revision said the lower end "is attained
     exactly only in trivial cases, such as one edge". The review had said
     only that it *is* attained in trivial cases. The "only" was an
     unrequested strengthening, and the note's own data refute it.
   - *Check.* T3 in `check_tree.py` now counts attainment. The lower end
     equals the gap (to `1e-7`) in 515 of 900 cases. In 93 of them both
     per-edge values exceed `1e-4`; for example, trial 2 with degree 0 has
     gap 1.429786 = `2 dist(Band_2)`, while `2 dist(Band_1)` = 0.315654.
     This reproduces the recheck's count (`q3_tree_lower_end.py`) with the
     note's own script.
   - *T1 limit, now proved.* The Remarks after Proposition 3.3 now prove
     `gap <= 2 E_n + Lip(r)^2/(4K)`. `check_revision2.py` evaluates the
     bound: at `K = 100`, `gap/2E_n <= 1.036` (`n = 4`) and `<= 1.208`
     (`n = 8`). "At finite `K` the gap stays above `2 E_n`" is now
     labelled numerical. (It is proved in the third revision; Section
     12.3, item 2.) A sufficient condition for attainment is stated.
   - *Where.* Summary (B), Section 3 Remarks, Section 7.4, status table,
     Section 10, and a pointer in Section 12.1, item 6.
2. **Lost log restored.**
   - *What was wrong.* `check_tree.py` opened `logs/check_tree.log` in
     write mode at import time, and `check_revision.py` imports it. So the
     first revision's run of `check_revision.py` emptied the log (0
     bytes). Section 7.4 and the Summary's "247 of 900" had no log.
   - *Fix.* The log is now opened only under `__main__`, in `check_tree.py`
     and in `check_hp.py`, which `check_revision2.py` imports.
     `check_tree.py` was rerun (18 s).
   - *Check.* The regenerated log agrees line by line with the recheck's
     scratch rerun, apart from the four new attainment lines. Every value
     in Section 7.4 (T1 and T2 tables; T3: 249, 1.7646, 247) is
     unchanged. `logs/check_hp.log` was not touched: its timestamp is
     still 03:28 after the imports.
   - *Where.* Section 11 (note on `logs/check_tree.log`).
3. **Unaligned hp.**
   - *What was wrong.* The argument said that after bisection the other
     cells are "analytic at a fixed relative distance from the kink". For
     dyadic bisection this is false. `check_revision2.py` reproduces the
     recheck's relative distances for `c0 = 1/sqrt 7`: 0.047 at level 4
     and 0.071 at level 11. The status labels also disagreed ("gives",
     "sketched", "cited, not proved").
   - *Fix, different from the recheck's suggestion.* Under the hypothesis
     of Proposition 5.8 the relative distance is not needed at all. A cell
     inside a piece inherits the piece's Bernstein ellipse, because
     `E_rho(D) ⊂ E_rho(I)` for `D ⊂ I`. So instead of switching to a
     geometric mesh, the flawed sketch was replaced by a proof for dyadic
     bisection, Proposition 5.8(b). The relative distance does matter
     when a piece's continuation is singular at the breakpoint (algebraic
     singularities). For that case the note now states the need for a
     geometric mesh, as the recheck suggested, and keeps the case
     unproved.
   - *Check.* `check_revision2.py` compares the level-4 cell
     `[0.25, 0.375]` with the same-width cell `[0.125, 0.25]`. For the
     note's `psi`, the errors `2 E_p` (`p = 1..4`) differ by factors 0.7 to
     1.7. For the algebraic variant with `-|s - c0|^{4/3}` they differ by
     2.0, 4.2, 54 and 181. It also confirms that in the dyadic meshes of
     Section 7.5 the kink cell dominates the gap for every `m`.
   - *Labels.* Proposition 5.8(b) is "proved" in Section 5.5, the
     Summary, Section 8, the status table and Section 10. Algebraic
     singularities at breakpoints are "not proved" in Section 5.5, Section
     8, the status table and Section 10.
4. **Alfonsi et al.**
   - *What was imprecise.* Section 5 of arXiv 1905.05663v1 was reread. The
     Taylor argument for `C^{1,1}` costs is their "rough calculation", and
     they call such a result "not obvious".
   - *Fix.* Section 8 now says that their proved `O(1/N^2)` rates
     (Propositions 5.7 and 5.9, Corollaries 5.8 and 5.10) are for `W_1`
     and `W_2^2`, under regularity conditions on the marginals. The
     correction of the first revision stands: the rates do not come from
     approximating Kantorovich potentials.
5. **Credit to Grimm–Netzer–Schweighofer.**
   - *Check.* arXiv 2303.14824v1 (the only version) calls Lemma 11 "a
     version of [4, Lemma 3]", with [4] = GNS, Arch. Math. 89 (2007).
     GNS's Lemma 3 and its proof were read in arXiv math/0611498v1. It is
     the same construction (fiber minimum shifted by `eps/2`, then
     polynomial approximation), without degree bounds.
   - *Fix.* The Summary (F), Section 8 (new GNS entry and novelty list) and
     the status table credit the qualitative form to GNS and the
     quantitative version to KMR.
   - *Published KMR version.* The bibliographic data (Math. Program. 209
     (2025) 435–473) were confirmed through Crossref. The lemma number in
     the published version was not checked; the note cites arXiv v1.
6. **Corollary 5.5.**
   - "Largest power of 1/2 below" became "at most".
   - `s0` was undefined and stood for two boxes. It is replaced by `q0`,
     the side of `Q`, in the level count and by `s_e`, the largest side of
     `X_e`, in the outer term.
   - `theta <= 1` because [D, Lemma 3.1] requires `theta = 2^{-mu}` with
     `mu >= 0`. So `4/theta <= 4 sqrt(Mk/c)` fails when `c > Mk`, and the
     factor is now `max(16 Mk/c, 16)^{k/2}`. This was rederived from
     [D, Lemma 3.1] and changed in the corollary, the comparison paragraph
     (the stale `(Mk/c)^{k/2}`), the Summary and the status table.
   - The Summary now also states the `k >= 2` hypothesis (recheck, minor
     point 4).
7. **Wording.**
   - (a) Summary (D): `C^{1,1}` band elements on boxes are now conditional
     on completing the sketch of Proposition 4.3, including its
     open-boundary hypothesis.
   - (b) Proposition 1.3(2): the lower semicontinuous extension is written
     out after the proof and labelled a sketch; also in the status table.
   - (c) Solver decisions: the reduced bands of Corollary 3.4 are backed
     by a result but need parent-side value functions; the joint dual
     marginals are untested. Changed in the Summary (E), Section 6 and
     Section 10.
   - (d) Looseness of Proposition 5.6. "Factors of 30 to 70" became: about
     18 to 72 for `2 <= n <= 32`, 105 to 330 at `n = 1`, and 51.0 to 107.5
     at `n = 128`. These were computed in `check_revision2.py`: fresh
     graded-grid LPs for `n <= 32` (same method as
     `check_pinch_rates.py`), and the logged `n = 64, 128` values. The
     `n <= 32` values agree with the review's R3 data.
   - (e) E6 at `n = 128`: 0.49, 0.42 and 0.33 are labelled lower
     estimates. The upper estimates are 0.50, 0.48 and 0.53, from
     `logs/check_pinch_rates.log`. Changed in Sections 5.4 and 7.1.
   - (f) The Summary no longer calls `-rho_R >= 2 E_{2R}` an identity. It
     names [S]'s identities and says the inequality follows from them.
   - (g) Conjecture `n gap -> 2 beta`: the note now says that the
     heuristic is weak. The band is not negligible for
     `|s| >~ 1/sqrt(c n)`, so the limit may be smaller. Changed in the
     Summary (C), Section 5.4, the status table and Section 10.

Commands added in the second revision, run in this directory with
`OMP_NUM_THREADS=1`:

```
python3 check_tree.py        # logs/check_tree.log regenerated; T3 attainment count added (18 s)
python3 check_revision2.py   # logs/check_revision2.log: T1 bound, hp cell checks, Proposition 5.6 ratios (53 s)
```

Only these targeted checks were run. There was no project-wide
verification and no CI inspection.

### 12.3 Third revision (after the confirmation)

The confirmation
([`../reviews/recheck-consistency-confirm.md`](../reviews/recheck-consistency-confirm.md),
checks in `../reviews/recheck-consistency-confirm-checks/`) found all
seven fixes of the second revision applied correctly and no mathematical
error. It checked the two arguments added in the second revision
(Proposition 5.8(b) and the T1 limit) step by step, tested both
numerically, and found them correct. It raised six minor points, fixed
below. Each point was verified before the text was changed.

1. **Proposition 5.6: "so it grows with `c`" was false for small `n`.**
   - *Check.* `check_revision3.py` reads the lower estimates of the ratio
     `30 (3 + c) n gap` from `logs/check_revision2.log` and classifies
     each computed `n`. The ratio grows with `c` at `n = 1, 16, 32, 64,
     128`, falls at `n = 2, 3, 4` (35.0, 25.0, 18.3 at `n = 2`), and is
     not monotone at `n = 8` (40.0, 36.5, 39.2). This agrees with the
     confirmation.
   - *Fix.* Section 5.4: the clause was removed, and a new sentence states
     for which `n` the ratio grows with `c`. The ranges quoted there are
     unchanged.
2. **T1 at finite `K`: Section 10 stated as fact what the note labelled
   numerical.**
   - *Check.* The confirmation's proof was checked step by step: the bag
     bounds give `-rho >= X`; evaluating `max(r_2 - r_1)` at a maximizer
     of `r_2` and at a minimizer of `r_1` gives `X >= osc(r_e)`;
     `osc(r_e) >= 2 E_n`, with equality only for `p_e = p + const`,
     because the best approximation is unique. In that case
     `-rho = osc(r) + (c_2 - c_1) - m_B`, and a point `s0 != 0` with
     `r'(s0) != 0` gives `m_B < c_2 - c_1`. Such a point exists because
     `r` is continuous, not constant, and a polynomial on each side of 0.
     Proposition 1.2
     applies (box, finite-dimensional classes, exact bag minima), so the
     optimal split is attained. `check_revision3.py` illustrates step 3
     for the split `-p`. The middle bag lies below 0 by at least
     `4.70e-3`, about `4.889e-4` and `4.909e-5` for `n = 4`, and `1.14e-2`,
     `1.40e-3` and about `1.436e-4` for `n = 8`, at `K = 100, 1000, 10^4`. These
     are below the upper bound `Lip(r)^2/(4K)` and approach it as `K`
     grows. For `n = 4`, `K = 100` this gives `gap(-p)/osc(r) >= 1.03477`,
     the confirmation's value for that split.
   - *Fix.* The proof was added to Section 3, Remarks, credited to the
     confirmation. The Section 10 sentence is now a proved statement; it
     was reworded to cite the proof. The Summary (B), Section 7.4 and the
     status table now state strictness at finite `K` as proved instead of
     "numerical only".
3. **Alfonsi et al., `W_1` hypothesis.**
   - *Check.* The statements were reread in arXiv 1905.05663v1 (the text
     the recheck downloaded). Proposition 5.7 and Corollary 5.8 assume
     absolutely continuous `mu`, `nu`, at most `Q` sign changes of
     `F_mu - F_nu`, and `rho_mu - rho_nu in L^inf`. After Corollary 5.8
     the authors remark that boundedness near the sign changes suffices.
     Proposition 5.9 and Corollary 5.10 assume
     `rho_mu, rho_nu in L^inf`.
   - *Fix.* Section 8 now states the `W_1` hypothesis as a bounded density
     difference, with the authors' remark, and its reading note records
     the reread. The `W_2^2` entry ("bounded densities") was already right
     and is unchanged.
4. **"Pieces analytic up to the breakpoint (kink)."**
   - *Check.* The shorthand appeared in the Summary (D), Section 8, the
     status table and Section 10. `(s - c0)^{4/3}` is analytic on the open
     piece and continuous up to `c0`, so the shorthand could be read to
     cover it, but Proposition 5.8 excludes it.
   - *Fix.* All four places now say that each piece extends analytically
     across the breakpoint (the kink, in the Summary), which matches the
     hypothesis of Proposition 5.8.
5. **Notation and a loose sentence in Proposition 5.8(b).**
   - The rate `b = sqrt(log 2 · log rho)` clashed with the endpoint `b`
     of `X_S = [a, b]`. It is now `beta_1` in the proposition, its proof,
     the text after it, the Summary (D), the status table and Section 10.
     Other rates written with `b` were made explicit:
     `C exp(-(log rho/J) N)` for aligned cells, and `exp(-b' sqrt(N))`
     for the unproved geometric-mesh case. The constants
     `C = max(4 M/(rho - 1), G (b - a))` and `C' = C rho e^{beta_1 sqrt 2}`
     are now stated; `C'` agrees with the confirmation's.
   - "If `c` becomes a cell boundary, (a) applies" was replaced. The
     proposition now defines the kink cell: the cell containing `c`, or,
     once `c` is a common endpoint of two cells, the left one. Every other
     cell then lies in one closed piece, so the inclusion argument bounds
     it. The kink cell has width `(b - a) 2^{-m}`, so the oscillation
     bound applies to it. The bound, the count `N = m (p + 1) + 2` and the
     proof are otherwise unchanged.
   - *Check.* The counting was rederived: `p + 1 < beta_0 m + 2`, the
     quadratic gives `m >= sqrt((N - 2)/beta_0) - 1/beta_0`, and
     `2^{1/beta_0} = rho`.
6. **Status labels.** The header, the Section 9 preamble and the status
   table no longer call Proposition 5.8(b) and the T1 limit "not checked
   independently"; they cite the confirmation. The introduction and item
   1 of Section 12.2 now point to this section.

Commands added in the third revision, run in this directory with
`OMP_NUM_THREADS=1`:

```
python3 check_revision3.py   # logs/check_revision3.log: Proposition 5.6 ratio against c (read from logs/check_revision2.log); T1 step 3 for the split -p (9 s)
```

No other script was rerun. Items 3 to 6 change wording and notation only,
and the values quoted in item 1 were already in `logs/check_revision2.log`.
Only this targeted check was run. There was no project-wide verification
and no CI inspection.

*Root edit (2026-09-30), from `reviews/consistency-confirm-r1.md`:* the
constant in Proposition 5.8(a) is now written explicitly as
`4 M rho/(rho - 1)` (it differs from the `C` defined in part (b)); three
"at least" values that had been rounded up in the last digit are given to
four significant digits (4.889e-4, 4.909e-5, 1.436e-4), and the ratio bound
is quoted as 1.01477. No conclusion changed.

*Root edit (2026-09-30, closing audit):* the header now cites
`reviews/consistency-confirm-r1.md`. In the table of repository results in
Section 5.4 and the status table of Section 9, the `|` characters inside
code spans (`|y|`, `|lambda|`) split the rows into extra cells in
GitHub-flavoured Markdown; they are now escaped as `\|`. The text is
unchanged.
