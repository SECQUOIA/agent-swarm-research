# Adversarial review: node complexity of spatial branch-and-bound with face-exact relaxations

Date: 2026-09-29. Reviewed document:
[`bb-complexity/spatial-face-exact/face-exact-node-complexity.md`](../bb-complexity/spatial-face-exact/face-exact-node-complexity.md)
(the "note"). Context: [`PROGRAM.md`](../bb-complexity/PROGRAM.md), Q2 and Section 3.7 of the
[spatial scout report](../scouting/spatial-bb-theory.md), and the
[spatial review](spatial-bb-review.md). Reviewer scripts and logs are in
[`face-exact/`](face-exact/). They do not reuse the author's code. The reviewer did not write the
note and did not edit it.

## Verdict

The mathematical core of the note is sound. I checked every numbered result by hand:

- the gap lemmas (2.1–2.5);
- the lower bounds (Theorems 3.2, 3.4, 3.6 and 3.8, Lemma 3.7, Proposition 3.10, Corollaries 3.3,
  3.5 and 3.11);
- the exact constant for the tilted stratum (Proposition 3.13);
- the structure theorems (Lemma 4.1, Theorem 4.2, Corollary 4.3, Theorems 4.4 and 4.5);
- the oblivious-rule bound (Theorem 5.3);
- the strong-branching bound (Proposition 5.6), which I replayed in exact rational arithmetic.

All of these hold as stated or with small fixes. Independent code reproduces the note's kink-row
node counts exactly.

The errors are in side claims about which rules are cheap, in one conjecture, and in statements
about solver defaults:

1. **Proposition 5.4(b) is false for an uncountable null set of instances, and Conjecture 5.7 is
   false.** For `beta = 1/5` and `a = 1/6`, the relaxation point `xhat = a` lies in the clamped
   outer fifth of every straddling `x`-interval. So `R(1, 1/5)` never splits at `a`. With
   widest-side selection it needs at least `0.074 eps^(-1/2)` nodes (about `1.2–1.95 eps^(-1/2)`
   measured), while `N_opt = 2`. Step 3 of the proof ("a clamped split keeps `D`") is false.
   (Section 8.2.)
2. **Aligned strata in box-constrained problems do not automatically have linear transverse
   growth, and Conjecture 7.1 is false.** `f = (x-a)^2 + (x-a)(y-z) + (y-z)^2` on `[0,1]^3` has
   the aligned optimal segment `{x = a, y = z}`, quadratic transverse growth and
   `N_opt >= 1/(2 sqrt(eps))`. Conjecture 7.1 predicts `O(log(1/eps))` because `p* = 0`.
   (Section 7.3.)
3. **Solver defaults are misstated.**
   - SCIP 10's default branching point is not the relaxation point (`alpha = 1`). The parameters
     are `branching/midpull = 0.75`, `branching/midpullreldomtrig = 0.5` and
     `branching/clamp = 0.2`. So the effective `alpha` is `0.25` on nodes whose domain is at least
     half of the global domain, and `1 - 0.75 r` for relative width `r < 0.5`. In a real SCIP 10
     run on the scout's instance, the first split is at `11/24 = 0.75*(1/2) + 0.25*(1/3)`.
   - BARON, per Tawarmalani–Sahinidis (2002), sets the branching point to the incumbent when the
     incumbent lies inside the domain. That is exactly the "place a face on the optimum"
     mechanism.

   Every "SCIP (1, .2)" label and every statement about SCIP, BARON or ANTIGONE defaults needs
   rewording. (Section 8.4.)
4. **Proof gap.** Proposition 4.6(a) (bounded `N_opt` iff an exact certificate exists) is proved
   for `F = X0`. With linear constraints, the closure step of the proof fails. The statement may
   still hold. (Section 7.4.)
5. **Overstatements.**
   - "`tau` is the exact invariant" is too strong: `tau > 0` is sufficient for the lower bound,
     but aligned strata with `tau = 0` can still cost `eps^(-1/2)`.
   - Proposition 4.7's `Theta(1/eps)` is only proved as `Omega`. I supply the missing
     `O(1/eps)` construction and check it numerically.
   - The optimal set of Proposition 4.7 is larger than stated.
   - "The star-forest hypothesis cannot be dropped" is misleading, because the path `x1 - y - x2`
     *is* a star.
   - Example 3.12 is removed at the root by one RLT product.

**Novelty.** The node-count statements appear new in the sources I could check: the transversality
and `tau` lower bounds, the fractional-vertex-cover exponent, the exact tilted constant, and the
rule separations. Several ingredients are standard, however:

- Lemma 4.1 is a textbook convex-analysis fact.
- The McCormick gap formulas are classical.
- The first-order observation of Theorem 6.1(b) was anticipated for nondifferentiable
  unconstrained minimizers (Wechsung's thesis, as reported by Kannan–Barton).
- The mechanism behind Propositions 5.4–5.5 (branch at the optimum so that the relaxation is
  exact there) is the Shectman–Sahinidis finite branching scheme that BARON adopted. The note did
  not credit it, although it cites the book that describes it.

## Per-claim verdicts

Legend:

- **C**: correct;
- **CF**: correct with a fix;
- **G**: proof gap;
- **F**: false;
- **O**: overstated;
- **N**: numerical support only.

| Claim | Verdict | Main point |
|---|---|---|
| 1.1 model, monotonicity, Lemma 1.1 | C | |
| Lemma 1.2 (covered tightening) | C | Also covers every node relaxation that is pointwise weaker than termwise McCormick. Does not cover RLT products, cutoff propagation, parent bounds taken from children, or auxiliary-variable branching (Section 1) |
| Lemma 2.1 (a)–(d) | C | Classical |
| Lemma 2.2 (faces; vertex-cover zero set) | C | |
| Lemma 2.3 (mixed partial), Lemma 2.4 (chord) | C | 300 random joint trilinear envelopes: min ratios 1.0007 and 1.0025 |
| Lemma 2.5, Definition 2.6 | C | |
| Definition 2.7 (transversal), Definition 2.8 (`tau`) | C | |
| Theorem 3.6 (flat strata) | C | Centroid (Minkowski–Radon) step checked |
| Lemma 3.7 (a)–(d) | C | |
| Theorem 3.8, Lemma 3.9 (curved strata) | C | |
| "`tau` is the exact invariant for flat strata" (Summary) | O | Sufficient condition with a sharp constant on one instance; not a characterization |
| Lemma 3.1 (per-box integral, `J`) | C | Closed form matches direct quadrature; divergence at `s = 1` confirmed |
| Theorem 3.2, Corollary 3.3(a) | C | |
| Corollary 3.3(b) (one log is unavoidable) | C | The example is sharp, so it violates (QD); under (QD) the necessity of the log is open |
| Theorem 3.4, Corollary 3.5 | C | |
| Proposition 3.10, Corollary 3.11 (`tau*` exponent, attained) | C | |
| Example 3.12 | C | Removed at the root by the RLT product `x (y - z) = 0` |
| "Quadratic growth needs constraints"; "box-constrained aligned strata automatically have linear growth" | F | Counterexample A (Section 7.3) |
| Proposition 3.13 (tilted stratum, both bounds) | C | Reproved; grid check of the construction |
| Lemma 4.1 | C | Standard fact |
| Theorem 4.2, Corollary 4.3 | C | "(R) holds for a matching" needs a perfect matching |
| Theorem 4.4 (2D, 2-box certificate) | C | |
| Theorem 4.5 (star forests) | C | Hypothesis concerns the pair (G, K), not G |
| Proposition 4.7 (a)–(c) | C | The optimal set also contains `{y = 1, X1 <= X2}` |
| Proposition 4.7 "`Theta(1/eps)`" | O, now C | Only `Omega` was proved; reviewer's quadtree gives `O(1/eps)` |
| "Star-forest hypothesis cannot be dropped" | CF | The path `x1 - y - x2` is a star; what fails is "K = centres" |
| Proposition 4.6(a) | C for `F = X0`, G otherwise | Closure step with constraints |
| Proposition 4.6(b) | C | Necessity only; linear growth is not shown sufficient |
| Section 4.7 table, Conjecture 4.8 | C (as labeled) | |
| Theorem 5.1 (a), (b) | C | |
| Proposition 5.2, its Consequence | C | |
| Theorem 5.3 (oblivious rules) | C | |
| Proposition 5.4(a) and the Remark | C | |
| Proposition 5.4(b) | F | Fails for `a` in a Cantor set `K_beta` (e.g. `a = 1/6`, `beta = 1/5`); the clamp count in the proof is wrong for every `a` near a clamp point |
| Proposition 5.5 (a), (b) | C | For fixed `alpha < 1` only; SCIP's box-dependent `alpha` is not covered |
| Proposition 5.6 | C | Exact replay: 407 and 44965 nodes at `1e-4` and `1e-6`, path `1/3, 8/11, 5/13, 40/49`, `D = 45/3136` |
| Conjecture 5.7 | F | Refuted by `a = 1/6` (Section 8.2) |
| Open 7.5 "impossible in 2D for full segments" | F | The clamp, not the relaxation minimizer, moves the split off the face |
| Conjecture 7.1 | F | Counterexample A |
| Solver defaults (SCIP `(1, .2)`, "`alpha < 1` as in BARON") | F | Section 8.4 |
| Theorem 6.1 (a)–(c) | C | Novelty caveat (Section 11) |
| Section 8 kink row | reproduced exactly | Other rows not rerun |

## 1. Model and bound-tightening coverage (Lemmas 1.1, 1.2)

Lemma 1.1 is correct, and so is the proof of Lemma 1.2. A piece `S` removed from `B_k` satisfies
`Gamma_S <= Gamma_{B_k} < m + eps` on `S ∩ F` by monotonicity. The lower-bound proofs use only
two facts: validity of each box of the cover, and (2.1) on that box. Pieces therefore behave like
leaves.

Scope points that the note should state:

- **Weaker relaxations are covered.** If a node relaxation lies pointwise below termwise McCormick
  on the node box, its gap is larger, so validity is harder and all lower bounds hold. Examples:
  outer approximation of `g` by gradient cuts, and McCormick cuts inherited from ancestors and not
  re-separated. The phrase "relaxations of other types" in the "not covered" list is broader than
  needed.
- **Stronger relaxations are not covered, and they matter.** In Example 3.12 the RLT product of the
  equality `y - z = 0` with `x` gives `w_xy - w_xz = 0`. The relaxation then equals
  `gamma (x-a)^2` on `F`, so the root is pruned and `N = 1` against the proved `|c|/(2 sqrt(gamma eps))`
  for termwise McCormick. BARON, ANTIGONE and SCIP (via its RLT separator) generate such products.
  The note lists RLT as not covered, so this is a scope issue, not an error. But Example 3.12
  should say that its cost is an artifact of the missing constraint products. Counterexample A
  (Section 7.3) has no constraints and is not affected.
- **Other operations outside the model:**
  - *Bounds taken from children.* Strong branching or probing can set a parent's bound to the
    minimum of its children's bounds (spatial review, Section 1.1). The children must then be
    counted as the leaves.
  - *Branching on auxiliary variables.* SCIP's `constraints/nonlinear/branching/aux` is off by
    default (value 2147483647).
  - *Incumbents accepted within feasibility tolerance.* SCIP returned objective values down to
    `-9.99e-7 < f* = 0` in the runs of Section 8.4.
  - *Objective-cutoff propagation.* The note already excludes it.

## 2. Gap lemmas (Section 2)

- **Lemma 2.1.**
  - (a): the four identities `x_i x_j - (underestimator) = delta delta` give both sign cases.
  - (b), (c) and (d) follow as stated.
  - The maximum `|c| w_i w_j/4` is attained at the centre, because
    `min(p, q) <= sqrt(p q) = sqrt(a_i a_j)`.
- **Lemma 2.2.**
  - (a) is the standard face property of convex envelopes.
  - A zero-diagonal PSD matrix is zero. Hence "convex iff affine" holds for multilinear
    restrictions.
  - (b) is Lemma 2.1(b) summed over edges.
  - The summary's statement "the zero set is the union of faces whose fixed coordinates form a
    vertex cover" is correct.
- **Lemma 2.3.**
  - The two points `x ± (d_i e_i - s d_j e_j)` lie in `B`, and the average of `phi` over them is
    `phi(x) - |D| d_i d_j`. Correct.
  - Check [ENV] in `misc_checks.py` computes joint envelopes of 300 random trilinear functions by
    the vertex LP. The minimum of gap divided by the bound is 1.0007.
- **Lemma 2.4.** Correct. For the single-term claim with a general direction `v`, the chord of the
  2D face rectangle contains the projection of the chord of `B`. A longer chord only increases
  `(-t_-) t_+`, so the bound transfers. The random check gives a minimum ratio of 1.0025.
- **Lemma 2.5.** Correct. The alphaBB function `phi - alpha' q_B` has Hessian
  `grad^2 phi + 2 alpha' I`, which is PSD.

## 3. Transversality, `tau`, and the stratum lower bounds (Sections 2–3.3, Proposition 4.7)

- **Definition 2.7.** Correct. Complements of vertex covers are exactly the independent sets, so
  the two forms of the definition agree.
- **Theorem 3.6.** Correct.
  - For `C` in a valid cover, `K = S ∩ C` is convex.
  - Its centroid `g` lies in `S ∩ C`. By Minkowski–Radon, `x_i(g)` is at least `W_i(K)/(p+1)`
    from both `min_K x_i` and `max_K x_i`, and hence at least that far from `l_i` and `u_i`.
  - Validity at `g` and (2.1) bound `max_E W_i W_j`. The definition of `tau` then bounds
    `vol_p(K)`.
  - `vol_p` in `t`-coordinates equals `H^p`, because `V` is orthonormal.
- **Lemma 3.7.**
  - (a): `K* = {i : W_i <= sqrt(eta)}` covers every edge, and `K` lies in the parallelepiped
    defined by `J ⊆ K*`.
  - (b), (c): correct.
  - (d): `W_x W_y >= area(K)` for planar convex `K`, so `tau = 1`.
- **Theorem 3.8 and Lemma 3.9.** Correct.
  - `{i : d_i <= rho}` is a vertex cover because `d_i d_j <= rho^2` on every edge.
  - The localization to `2^|K|` corner cubes and the area-formula argument are standard.
  - (H) holds for every `r`, not only `r <= r0`.
- **"`tau(V, G)` is the exact invariant for flat strata" (Summary, Q1 bullet 4): overstated.** The
  proved statements are:
  - `tau > 0` gives `Omega(eps^(-p/2))`;
  - the constant is sharp on `tilt` (Proposition 3.13);
  - `tau > 0` is strictly weaker than transversality for `p >= 2` (Proposition 4.7).

  Nothing is proved about `tau = 0`. Aligned strata (`tau = 0`) cost `O(1)` in Theorem 4.4 but
  `Omega(eps^(-1/2))` in Example 3.12 and in counterexample A. So `tau` alone does not decide the
  exponent. "Exact" should be read only as "sharp constant on one instance".
- **Proposition 4.7.**
  - (a)–(c) are correct, and `tau = 1/sqrt(2)`.
  - For `a1 = 1/3` and `a2 = sqrt(2) - 1`: `H^2(S) = sqrt(2)(1 - |a1 - a2|) = 1.2998`, so the
    bound is `0.1021/eps`.
  - Reviewer LP (`path3_quadtree.py`): the orthant boxes have bounds `-0.1847`, `0`, `0` and
    `-0.3118`, which agrees with the note.
  - Three corrections:
    1. **Optimal set.** The note says `S = {X1 = X2}` is the optimal stratum. In fact `f = 0` also
       on `{y = 1, X1 <= X2}`, because `|D| + D = 0` for `D <= 0`. The grid check confirms
       `f = 0` there. The claims are unaffected: Theorem 3.6 needs only `S ⊆ argmin`, and the
       extra piece lies on the face `y = 1`, where the gap vanishes.
    2. **`Theta(1/eps)` was only `Omega(1/eps)`.** An upper bound follows from a quadtree in
       `(x1, x2)` with the full `y`-range. A square of side `h` is a leaf if `h <= 2 eps`, since
       then `sup Gamma <= h/2`. It is also a leaf if `min_Q |D| >= 2h`, since then:
       - for `D < 0`, `Gamma <= 2h(1-y) <= |D|(1-y) = m`;
       - for `D > 0`, `Gamma <= 2hy <= m`.

       At each scale `h`, `O(1/h)` squares are refined, so there are `O(1/eps)` leaves.
       Numerically, with every leaf's LP bound checked `>= -eps`, leaves times `eps` stays
       between 6.1 and 13.0 for `eps` from `1e-1` to `1e-3`.
    3. **Star forest.** The interaction graph `x1 - y - x2` is itself a star, with centre `y`.
       Theorem 4.5 is a statement about the pair `(G, K)`: `K` must be an independent vertex cover
       in which every vertex outside `K` has at most one neighbour in `K`. Proposition 4.7 shows
       that this condition on the *fixed coordinates* cannot be dropped. It does not show that
       star-forest graphs fail.
  - Remark: Proposition 4.7(a) also follows from Proposition 4.6(b). The direction `(1, 1, -1)`
    is concave for the `x1 y` term, and `m ≡ 0` along it inside the optimal plane.

## 4. The tilted stratum (Proposition 3.13)

**Correct, with matching bounds.**

- **Lower bound.** Theorem 3.6 with `p = 1` gives
  `tau H^1 / (2 sqrt(eps)) = sqrt(theta/(1+theta^2)) sqrt(1+theta^2) / (2 sqrt(eps)) = (1/2) sqrt(theta/eps)`.
- **Upper bound.**
  - Each step checks: `U = s + theta(t - h'/2)` on the right box, `Gamma <= s t`, and
    `m >= 1.5|U|`.
  - In the case `t < h'/2`, `s -> s t - 1.5|s - D|` is maximized at `s = D`, which gives
    `theta (h'/2 - t) t <= theta h^2/16 = eps`.
  - The left box follows by the substitution `t' = h' - t`.
  - When `eps >= theta/16`, one strip with `h' = 1` still works, which gives `N_opt <= 2`, as
    stated.
- **Grid check.** [TILT] in `misc_checks.py`, for `theta` in `{0.3, 0.03}` and `eps` in
  `{1e-3, 1e-5}`: the maximum of `gap - m - eps` over all `2K` boxes is at most `-1e-5`.

## 5. The certificate integral (Lemma 3.1, Theorem 3.2, Corollary 3.3)

- **Lemma 3.1.**
  - The region where `xi eta <= (1-xi)(1-eta)` is `xi + eta <= 1`. The Dirichlet integral gives
    `Gamma(1-s)^2/Gamma(3-2s)`, and scaling gives `|c|^(-s)(w w)^(1-s)`.
  - Direct 2D quadrature of the min form ([J]) matches the closed form: 2.259235 at `s = 0.25`
    and 6.283185 at `s = 0.5`. At `s = 0.75` and `s = 0.9` the agreement is within `2e-5` and
    `1.5%`; mpmath loses accuracy at the corner singularities, and the closed form is standard.
  - For `s = 1`, truncating at distance `delta` from the corners gives 39, 166 and 378 for
    `delta = 1e-2, 1e-4, 1e-6`. The growth is of order `log^2(1/delta)`, which confirms
    divergence.
  - The bound `J <= 2.3/(1-s)^2` holds because `Gamma(2-s) <= 1` and `min Gamma = 0.8856`.
- **Theorem 3.2.** Correct. The slice of a box is a product of the `k` matched rectangles, and
  `(w w)_r <= W_r` because `1 - s/k > 0`.
- **Corollary 3.3(a).** Correct.
- **Corollary 3.3(b).** Correct: `m <= (2 + max(b, 1-b))|x - a| = 2.586|x - a|`, and
  `integral (m + eps)^(-1) = (2/2.6) log(1/eps) + O(1)`.
  - Two caveats on "one log factor is unavoidable".
    1. The example is sharp, so it violates (QD). Whether a log loss is needed for (QD) instances,
       where Theorem 5.1(a) gives the matching upper bound, is not addressed.
    2. The gap between the proved loss `log^(2k)` and the necessary `log^1` is open. A product of
       `k` kinks shows that `log^1` is necessary for every `k`.

## 6. Concave slices and near-optimal boxes (Theorem 3.4 to Example 3.12)

- **Theorem 3.4.**
  - `C_z` is a box, because each matched pair involves only its own `t_r`.
  - The chord bound applies termwise with `kappa_r = |c_r|`, and the anisotropic AM–GM and arcsine
    step is correct.
  - For the joint case, `∂_ij phi` is constant on the line.
- **Corollary 3.5.** Correct: `integral_{-t0}^{t0} (M t^2 + eps)^(-1/2) = (2/sqrt(M)) arsinh(t0 sqrt(M/eps))`.
- **Proposition 3.10.** Correct. The centre of `C ∩ R` lies in `C ∩ F`, and `d_i >= w'_i/2`.
- **Corollary 3.11.** Correct.
  - The log-substitution LP is right, and so is the change of variables `z = (1 - x)/2`.
  - Converse: boxes of widths `W`, `rho'` and `rho'^2/W` satisfy `w_i w_j <= rho'^2` on every
    edge, for each pair of values of `z` with `z_i + z_j >= 1`.
  - The statement "`tau* <= n/2` with equality iff `G` has a fractional perfect matching" is LP
    duality.
- **Example 3.12.** The bound `|c|/(2 sqrt(gamma eps))` is correct. For the RLT caveat see
  Section 1, and for the claim that follows the example see Section 7.3.

## 7. Structure results (Section 4)

### 7.1 Lemma 4.1, Theorem 4.2, Corollary 4.3

- **Lemma 4.1.** The proof is correct.
  - It uses sublinearity of `h = g'(p0; ·)` on the cone of feasible directions, the bound
    `g(p0 + d) >= g(p0) + h(d)`, and `h(p0 - p) = g(p0) - g(p)`. The last holds because `g` is
    affine on the relatively open segment.
  - The fact is standard. The graph of `g` over `sigma` lies in the relative interior of one face
    of `epi g`, and normal cones of a convex set are constant on the relative interior of a face.
    Hence `∂g` is constant along `sigma`.
- **Theorem 4.2.** Correct.
  - (i) holds because `g = f* - phi` is convex along `sigma`.
  - (ii) follows from Lemma 4.1, with `grad phi(p0 + s v).u = grad phi(p0).u + s u^T C v`.
- **Corollary 4.3.**
  - (a) and (b) are correct. In (b), `gamma'^T grad^2 f gamma' = 0` forces `grad^2 f gamma' = 0`.
  - (c) is correct.
  - One fix: "(R) holds for a matching" needs a *perfect* matching. An isolated coordinate `i`
    has `C e_i = 0`.
  - The bipartite criterion "`A` square and nonsingular" is right.
  - (d) is correct.

### 7.2 Theorems 4.4 and 4.5

- **Theorem 4.4: correct, and the proof is short and complete.**
  - For `c > 0`, `r_+(y) >= c(y - L_y)` and `r_-(y) >= c(U_y - y)`. These match the corners
    `c(x-a)(y-L_y)` and `c(a-x)(U_y-y)` of the gap formula on the right and left boxes.
  - The case `c < 0` is symmetric. I checked both cases.
  - "Sharpness is forced" is accurate in 2D, because `C` is nonsingular there.
- **Theorem 4.5: correct.**
  - `tau^T C_KK tau = 0` because centres are pairwise non-adjacent.
  - Theorem 4.2(ii), applied along directions in `span(e_I)`, makes `rho(·; tau)` affine in
    `x_I`.
  - A nonnegative affine function on a box is at least the stated sum of slope times distance.
  - For each sign of `c_ki sigma_k`, the bounding corner of the McCormick gap is on the side where
    the slope term is minimized.
  - Hypothesis wording: see Section 3.

### 7.3 Counterexample A: box-constrained aligned strata with quadratic growth

The note says:

- "Section 4 shows that in box-constrained problems aligned strata automatically have linear
  transverse growth. Quadratic growth needs constraints" (after Example 3.12);
- "in box-constrained problems they automatically have the linear transverse growth that makes
  them cheap" (start of Section 4).

Both statements are true in 2D (Theorem 4.4) and for interior strata under (R). They are false in
general.

- **Instance.** `f = (x-a)^2 + (x-a)(y-z) + (y-z)^2` on `[0,1]^3`, with `a = 1/3`.
  - Take `g = (x-a)^2 + (y-z)^2 + ` linear terms, which is convex, and `phi = xy - xz`, relaxed by
    termwise McCormick.
  - `f = (X + D/2)^2 + 3D^2/4`, where `X = x - a` and `D = y - z`. So `argmin f` is the segment
    `{x = a, y = z}`.
  - Its tangent `(0, 1, 1)` lies in `span(e_y, e_z)`, and `{y, z}` is independent in
    `G = {xy, xz}`. So the stratum is aligned (`tau = 0`, `p = 1`) and lies in `ker C`.
  - The transverse growth is quadratic.
- **Lower bound.** The proof of Example 3.12 never uses the constraint except to restrict
  attention to the plane `y = z`. Here that plane is feasible without any constraint.
  - On `R' = {(x, y, y) : |x - a| <= h}`, `m = (x-a)^2 <= h^2`.
  - At the centre of `C ∩ R'`, `Gamma_C >= |c| w'_x w'_y / 2`.
  - Hence `N_cov >= h/(h^2 + eps) = 1/(2 sqrt(eps))` at `h = sqrt(eps)`.
- **Checks** (`box_aligned_quad.py`):
  - On a `61^3` grid, the zeros of `f` are exactly the segment.
  - Over 20000 random boxes, the minimum of `Gamma_C(centre)` divided by `(w'_x w'_y/2)` is
    1.0000.
  - A B&B with the reviewer's own Clarabel node QPs gives:

    | eps | bisection nodes | `R(1, .2)`, widest side | proved minimum nodes (`2 LB - 1`) |
    |---|---|---|---|
    | 1e-2 | 69 | 81 | 9 |
    | 1e-3 | 301 | 331 | 31 |
    | 1e-4 | 1227 | 1161 | 99 |

- **Consequence for Conjecture 7.1.** The instance satisfies every hypothesis of the conjecture:
  - box-constrained;
  - `g` convex and `phi` bilinear;
  - the optimal set is one compact `C^2` stratum with quadratic transverse growth;
  - `p* = 0`, because the segment has `tau = 0`.

  The conjecture predicts `O(log(1/eps))`, but `N_opt = Omega(eps^(-1/2))`. The conjecture is
  therefore false.
- **Robustness.**
  - The smooth instance is convex as a whole, so a solver that detects convexity would not
    branch.
  - The variant `f = (x-a)^2 + (x-a)(y-z) + K|y-z|` with `K > 1` is nonconvex. It has the same
    optimal segment and the same `1/(2 sqrt(eps))` bound, with growth that is quadratic in `x`
    and sharp in `D`.
  - Both variants survive RLT products of constraints, because there are none.
  - The factored McCormick form of `X·D` also costs `eps^(-1/2)`. Validity near `x = a` needs
    `|D_l| <= 2 sqrt(eps)` on boxes that meet the segment.
- **Repair.** The lower bound comes from a 2-dimensional *near-optimal* plane
  `{y = z, |x - a| <= sqrt(eps)}`, and that plane has `tau = 1/sqrt(2) > 0`. A corrected
  Conjecture 7.1 must measure `tau`-nondegenerate dimension on the near-optimal sets
  `{m <= eta}` at scale `eta ~ eps`, not only on the optimal set.

### 7.4 Proposition 4.6

- **(a), proof gap under constraints.** The limit argument is fine for `F = X0`. With a
  polyhedral `Q`, a limit box `B` can meet `F` only on a proper face of `B`. Then:
  - the approximating boxes `B_k` may miss `F` entirely, so they are valid vacuously;
  - `Gamma_B` at points of `F ∩ ∂B` is not controlled.

  The step "by continuity this extends to the closure" needs `F ∩ B ⊆ cl(F ∩ int B)` for each
  limit box. That holds when `F = X0`, or when `n = 2` and `F` is convex: a face of a 2D box
  fixes a coordinate, so the `xy` gap vanishes there. In `n >= 3`, a 2D face can carry a nonzero
  gap. I did not find a counterexample, and a repair by replicating neighbouring boxes seems
  plausible. So the statement is likely true, but as written it is proved only for `F = X0`.
- **(b): correct.**
  - A closed leaf contains an initial piece `[y*, y* + t1 v]` of the segment, because finitely
    many closed intervals that avoid 0 cannot cover `(0, delta)`.
  - The chord bound gives `m/t >= |c v_i v_j| (t1 - t)`.
- **Scope.** The Summary's phrase "It fails at any minimizer where `m` grows sublinearly" is
  accurate. The note does not claim that linear growth is sufficient, and it should not be read
  that way. The 2D table correctly labels the sharp-point row as conjectured.

## 8. Branching rules (Section 5)

### 8.1 Theorems 5.1, 5.2, 5.3

- **Theorem 5.1: correct.**
  - (a) is Theorem C with `tau` in place of `alpha' n/4`.
  - In (b), a non-pruned cube has `dist(y, S) < tau s_j^2/mu <= s_j`, so it lies within
    `2 s_j` of `S`, and at most `7^n` cubes meet each enlarged ball. The geometric sum even gives
    `2^(n+1)` in place of `2^(n+2)`.
  - The binary-version factor `2^n` is right.
  - For the scout's instance, `m >= 1.41|x-a| = 1.41 dist_inf`, so the claimed
    `Theta(eps^(-1/2))` for widest-side bisection is proved.
- **Proposition 5.2: correct.** The aspect ratio `<= 1/beta` is preserved by induction. Chains
  within a band have length at most `G`, and Mirsky's theorem splits a band into `G` antichains.
  The final sum gives `4 G (2/beta)^n Lambda^(n/2)`.
- **Theorem 5.3: correct.**
  - Step 1: the envelope at `(a, y-mid)` equals `-(|c| w_y/2) D_x`. The exact bound
    `-|c| w_y D_x (w_x - D_x)/w_x` is below it.
  - Steps 3–5 check.
  - Check [OBL] (`misc_checks.py`), widest-side bisection averaged over the non-dyadic grid
    `a_k = (k + 1/sqrt(2))/64`: the sums are 135, 568 and 1784 at `eps = 1e-3, 1e-4, 1e-5`,
    against the bounds 5.6, 17.7 and 55.9.

### 8.2 Counterexample B: Proposition 5.4(b) and Conjecture 5.7

Proposition 5.4(a) is correct: for fixed `y`, the envelope has slopes of absolute value
`<= |c| max|Y| < L`. The remark that extends it to Theorem 4.4's setting is also correct: the
one-sided derivatives of `m - Gamma_B` at `a` are `>= c(l_y - L_y) >= 0` and `>= c(U_y - u_y) >= 0`.

**Proposition 5.4(b) is false as stated.** Step 3 says: "A clamped split keeps
`D = min(a - l_x, u_x - a)`". It does not.

- **Near a clamp point.** With `beta = 0.2` and `a = 0.2 - 1e-6`:
  - the root split is clamped to `0.2`;
  - the straddling child `[0, 0.2]` then has `D = 1e-6`, not `0.2`.

  The number of clamps is about `log(0.2/(5D))/log 5`, not `1 + log(1/min(a, 1-a))/log(1/beta)`.
  With widest-side selection, each shrink of `w_x` is followed by `y`-splits that double the
  straddling column. The tree size therefore scales like `1/dist(a, clamp points)`.
  `kink_rules.py` [3] gives, at `eps = 1e-8`:

  | `a` | nodes |
  |---|---|
  | 0.199 | 4619 |
  | 0.1999 | 19305 |
  | 0.19999 | 5521 (still growing as `eps` decreases) |

  The note's formula predicts about 2 clamps for all of these.
- **The Cantor set `K_beta`.** For some `a` the tree is infinite. At every straddling node,
  `xhat = a`, and the clamp moves the split off `a` whenever `a` lies in an outer `beta`-part of
  the current `x`-interval. The new straddling interval is then exactly that outer part. Let
  `K_beta` be the set of `a` that stay in the (open) outer parts forever. It is:
  - a Cantor-type set of Hausdorff dimension `log 2/log(1/beta)`, which is `0.43` for
    `beta = 1/5`;
  - uncountable, of Lebesgue measure 0;
  - home to rationals. For example, `beta/(1 + beta) = 1/6`, the fixed point of the two-step map
    `t -> beta(1 - beta) + beta^2 t`.

  `kink_cantor.py` [A] replays the `x`-intervals for `a = 1/6` exactly: 12 consecutive clamped
  splits, with `a` never reached.
- **Counts for `a = 1/6`** (`L = 2`, `c = -1`, `N_opt = 2` by Theorem 4.4), `kink_cantor.py` [B],
  for `eps = 1e-2 ... 1e-8`:

  | rule | nodes | nodes times `sqrt(eps)` |
  |---|---|---|
  | `R(1, .2)`, widest side | 13, 39, 169, 549, 1515, 4921, 19541 | 1.2–1.95 |
  | bisection | 21 ... 24573 | 1.9–2.6 |
  | `R(1, .2)`, `x` only | 5 ... 23 | log growth |
  | `R(1, .2)`, product score | 5 ... 23 | log growth |
  | `R(1, .1)`, widest side | 3 at every `eps` | (`1/6` is not in `K_{0.1}`) |

- **Proof of a lower bound for `R(1, 1/5)` with widest-side selection at `a = 1/6`:
  `|T| >= 0.0745 eps^(-1/2)`.**
  1. Every straddling interval `I_k` has width `5^(-k)`, and `a` sits at relative position
     `rho` in `{1/6, 5/6}`. So a straddling box has bound `-(5/36) w_x w_y`.
  2. `yhat` is at relative position `rho`, so `y`-splits are clamped to relative position 0.2 or
     0.8.
  3. Let `k` be the largest index with `5^(-2k) >= 7.2 eps`.
  4. At every level `k' < k`, the column pieces with `w_y <= w_x` have `w_y > 0.2 w_x`. Their
     bound magnitude is at least `w_x^2/36 >= 5 eps`, so they are split in `x`.
  5. At level `k`, pieces with `w_y > w_x` have bound magnitude greater than `eps`, so they are
     split in `y` until `w_y <= 5^(-k)`.
  6. These pieces partition `[0, 1]` in `y`, so at least `5^k >= (1/5)(7.2 eps)^(-1/2)` of them
     are processed.
- **Consequences.**
  - Proposition 5.4(b) holds for `a` outside the null set `K_beta` (and its endpoints), with a
    constant `C(a, beta)` that is unbounded near the clamp points. It fails on `K_beta`.
  - The summary's "SCIP-type relaxation-point splitting has `O(1)` nodes on that family" and
    "solves the aligned kink in 3–7 nodes" hold only for the tested `a`.
  - The contrast with Proposition 5.5 survives in measure:
    - for `alpha = 1`, splitting is exact except on a null uncountable set;
    - for `alpha < 1`, splitting is exact only on a countable set.
  - **Conjecture 5.7 is false.** For `a = 1/6`, `|T| >= 0.0745 eps^(-1/2)`, while
    `C log(1/eps) N_opt = 2C log(1/eps)`.
  - The claim in Open 7.5 that "a counterexample to Conjecture 5.7 ... in 2D is impossible for
    full segments" is also false. The relaxation minimizer does lie on the face; it is the clamp
    that moves the split off it.
  - Product-score strong branching stays logarithmic on this instance, so Question 5.8 is still
    open.

### 8.3 Propositions 5.5 and 5.6

- **Proposition 5.5(a): correct for a fixed `alpha < 1`.** Along a fixed decision sequence, every
  endpoint has the form `lambda a + mu` with `lambda < 1`.
- **Proposition 5.5(b): correct.** `kink_rules.py` [4]: for `alpha` in `{0.75, 0.25, 0.7}` and
  `eps` from `1e-3` to `1e-8`, every count is below the stated bound (for example `43 <= 75` for
  Couenne's point at `1e-8`).
- **Proposition 5.6: correct.**
  - Independent exact rational replay (`prop56_exact.py`) reproduces:
    - the path `rho = 1/3, 8/11, 5/13, 40/49`;
    - the decisive comparison at `rho = 40/49`: `-0.008310` for `y` against `-0.009908` for `x`;
    - `D = 45/3136`.
  - The counts are 9, 47, 407, 3933 and 44965 nodes for `eps = 1e-2 ... 1e-6`. Each is at least
    `2D/eps - 1`; at `1e-6` the bound is 28698.
  - The straddling bound `-w_y (a - l_x)(u_x - a)/w_x` and `yhat` at relative position `rho`
    match the reviewer's vertex-enumeration bound to `7e-17` on 3000 boxes (`kink_rules.py` [1]).

### 8.4 Solver-default claims

The note takes its defaults from Speakman–Lee's Table 1: SCIP `(1, .2)`, ANTIGONE `(.75, .1)`,
BARON `(.7, .01)`, Couenne `(.25, .2)`. It then states:

- "SCIP-type splitting at the relaxation solution (`alpha = 1`)";
- "Any midpoint bias (`alpha < 1`, as in ANTIGONE, BARON and Couenne defaults)";
- "defaults `(1, 0.2)` for SCIP" (Section 5.3);
- the labels `SCIP(1,.2)` used throughout Section 8.

Speakman–Lee themselves say that SCIP "(mostly)" uses the relaxation point, and that "especially
in BARON" other factors, including "available incumbent solutions", supersede formula (1)
[[speakman2018-on-branching-point-selection-for]] p.3.

- **SCIP 10 (PySCIPOpt 6.2.1, checked with `getParam`).**
  - The parameters are `branching/midpull = 0.75`, `branching/midpullreldomtrig = 0.5` and
    `branching/clamp = 0.2`.
  - The branching point is `midpull_B * mid + (1 - midpull_B) * xhat`, clamped to the middle 60%.
    Here `midpull_B = 0.75`, multiplied by the relative domain width `r_B` when `r_B < 0.5`.
  - So the effective `alpha_B` is:
    - `0.25` (Couenne's value) on nodes with `r_B >= 0.5`;
    - `1 - 0.75 r_B` otherwise, which tends to 1 only as boxes shrink.
  - `scip_branchpoint.py`, scout instance, presolve off:
    - With propagation and separation off, the first `x` split is at `0.458333 = 11/24`, exactly
      `0.75*(1/2) + 0.25*(1/3)`.
    - With SCIP's defaults, root propagation first tightens `x` to `[0.2347, 0.4605]`. The split
      is at `0.344023 = 0.75*mid + 0.25*a`. The next split lands at `0.333336`, within `2.4e-6`
      of `a`.
    - Node counts:

      | setting | 1e-5 | 1e-6 | 1e-7 |
      |---|---|---|---|
      | defaults | 5 | 11 | 35 |
      | propagation and separation off | – | 112 | 315 |
      | `branching/midpull = 0` (the note's `R(1, .2)`) | 3 | 3 | 3 |

      With `midpull = 0` the count is 3 at every gap.
  - The reviewer's emulation of SCIP's point rule without propagation (`kink_rules.py` [2]) gives
    15, 51, 167, 723 and 913 nodes with widest-side selection, and 7, 11, 11, 11 and 19 with
    `x`-only selection, for `eps = 1e-2 ... 1e-6`.
- **Consequences for the aligned-kink results.**
  1. Proposition 5.4 concerns `alpha = 1`. That is SCIP with `branching/midpull = 0`, not SCIP's
     default.
  2. Even with `alpha = 1`, the 0.2 clamp makes the split exact only when `a` lies in the middle
     60% of the current box. That is the mechanism of counterexample B.
  3. SCIP's default is a box-dependent midpoint bias. Proposition 5.5(a) as proved covers only a
     constant `alpha < 1`. With `alpha_B` depending on the box width, the endpoints become
     polynomials in `a`. The countable-exception argument probably extends, but it is not proved.
  4. In practice the default's split converges to `a` very fast, because `alpha_B -> 1`. The
     observed counts sit between the 3 of `alpha = 1` and the roughly `eps^(-1/2)` growth of a
     fixed `alpha = 0.25`.
  5. The column labelled `SCIP(1,.2)` should be relabelled, for example "LP point `R(1, .2)`
     (SCIP with `midpull = 0`)". A column for SCIP's actual rule would be informative.
- **BARON.** Tawarmalani–Sahinidis describe BARON's branching point as a convex combination of the
  relaxation solution and the midpoint [[tawarmalani2002-convexification-and-global-optimization-in]]
  p.215. They also state that BARON adopts the finite branching scheme of Shectman–Sahinidis: "the
  branching point is set to the incumbent whenever the latter lies in the current subdomain and is
  not one of the end-points ... This renders the incumbent gapless" (p.243).
  - On the kink family, any optimal incumbent `(a, y*)` then gives a split exactly at `a`
    whenever `x` is selected.
  - So "BARON-type" `R(.7, .01)` does not model BARON, and "never splits at the optimal face" does
    not apply to BARON as documented.
  - Belotti et al. 2009 also describe branching at a known local optimum, following
    Shectman–Sahinidis, with a convexification "exact at the new bounds"
    [[belotti2009-branching-and-bounds-tightening-techniques]] p.18.
  - Current BARON and ANTIGONE defaults were not checked; they are closed source.
- **Couenne.** `(.25, .2)` agrees with [[belotti2009-branching-and-bounds-tightening-techniques]]
  p.18. The Couenne manual in the library does not list the branching-point options.

## 9. Convergence order (Section 6, Theorem 6.1)

- **(a): correct.** It reuses Theorem 5.1 and Proposition 5.2, and the order-`beta` extension is
  the same computation.
- **(b): correct.**
  - McCormick: Theorem 4.4.
  - alphaBB with `alpha = 1/2`:
    - the lower bound is the scout's Theorem D, `(1/2)(1/(8 eps))^(1/2)/4 = 0.0884/sqrt(eps)`;
    - the upper bound for bisection is Theorem 5.1(b), with `m >= 1.41|x - a|`.
  - First-order scheme: on `{x >= a}` the gap is at most `(x-a)(1.2 - y) <= (x-a)(2 - y + b) = m`,
    and the left box is symmetric.
  - Grid check [FO]: `max(gap - m) = 0` on both boxes.
- **(c): correct.**
- **Novelty.** See Section 11.

## 10. Computations reproduced

Independent code (`kink_rules.py`) with an exact piecewise-linear node bound reproduces the note's
kink row exactly at `eps = 1e-4 / 1e-6`:

| rule | nodes at `1e-4 / 1e-6` |
|---|---|
| bisection | 253 / 2045 |
| `R(1, .2)`, widest side | 3 / 3 |
| `R(.75, .1)`, widest side | 89 / 1581 |
| `R(.7, .01)`, widest side | 75 / 1983 |
| `R(.25, .2)`, widest side | 199 / 2439 |
| `R(.25, .2)`, product score | 21 / 33 |
| `R(.25, .2)`, min score | 407 / 44965 |

It also reproduces the scout's bisection sequence 21, 61, 253, 765, 2045. The other rows of
Section 8.2 were not rerun (`kinkT`, `tilt`, `diag`, `iso`, `aligned_quad`, the box QPs and
pooling). They are floating-point illustrations, as the note says.

## 11. Novelty

Sources read for this review:

- Speakman–Lee 2018 (p.3);
- Tawarmalani–Sahinidis 2002 (p.215, p.243);
- Belotti et al. 2009 (p.18, p.30);
- Kannan–Barton 2017 (p.2, p.18, p.41);
- Wechsung–Schaber–Barton 2014 (p.2).

These are local library copies. No web search was done. An unsuccessful search does not establish
novelty.

- **Known or standard:**
  - Lemma 2.1: McCormick 1976, Al-Khayyal–Falk 1983. The maximum gap at the centre is folklore.
  - Lemma 4.1: normal cones are constant on the relative interior of a face (Rockafellar, *Convex
    Analysis*), applied to `epi g`.
  - The Minkowski–Radon centroid bound.
  - The Dirichlet integral in Lemma 3.1.
- **Mechanism already known for branching points.** Branching at a known optimum or incumbent so
  that the relaxation is exact there (gapless) is the Shectman–Sahinidis (1998) finite branching
  scheme. It is adopted in BARON [[tawarmalani2002-convexification-and-global-optimization-in]]
  p.243 and discussed in [[belotti2009-branching-and-bounds-tightening-techniques]] p.18. The
  concave-minimization literature on `omega`-subdivision versus bisection (Tuy 1991; Horst–Tuy) is
  the older version of the question and was not examined. Propositions 5.4–5.6 and Theorem 5.3
  appear new as *node-count* statements. The note should credit the mechanism, and its Section 9
  sentence that BARON "gives up exact face placement" should be withdrawn.
- **First-order schemes at nondifferentiable minimizers.** Kannan–Barton report that Wechsung's
  thesis (Section 2.3) shows that first-order convergence may suffice in *unconstrained*
  optimization when the minimizer is a point of nondifferentiability
  [[kannan2017-the-cluster-problem-in-constrained]] p.2. The kink minimizers are such points. So
  the first-order part of Theorem 6.1(b) is anticipated. The new part is the comparison: McCormick
  and alphaBB have the same order and prefactor, yet `N_opt` is 2 for one and `Theta(eps^(-1/2))`
  for the other.
- **Probably new:**
  - the transversality and `tau` lower bounds with the explicit, sharp constant (Theorem 3.6,
    Proposition 3.13);
  - the fractional vertex cover exponent (Corollary 3.11);
  - the McCormick certificate integral (Theorem 3.2);
  - the aligned-segment certificates (Theorems 4.4 and 4.5).

  These are transfers of the scout's covering arguments, which the spatial review in turn
  classified as transfers of Lipschitz and bandit arguments. The new ingredient is the
  independent-set and vertex-cover geometry.
- **Leads not examined by the note or by me:**
  - Epperly–Pistikopoulos 1997 (reduced-space branching on a subset of variables). This is related
    to the vertex-cover view and to `tau*`.
  - Schöbel–Scholz 2010 and Scholz 2012 (convergence rate of geometric branch-and-bound and
    iteration counts).
  - Al-Khayyal–Sherali 2000, Shectman–Sahinidis 1998 and Falk–Soland 1969.
  - Bompadre–Mitsos 2012, which is not in the library.

## 12. Corrections requested in the note

1. **Summary, Section 5.3, Section 5.4, Section 8.1 table labels and Section 9.** Replace the
   SCIP, BARON and ANTIGONE default statements as described in Section 8.4. Label the `alpha = 1`
   rule "LP point, clamp 0.2 (SCIP with `branching/midpull = 0`)".
2. **Proposition 5.4(b).**
   - Restrict to `a ∉ K_beta` (a closed null set).
   - Replace step 3 with an argument that tracks the shrinking `D`.
   - Say that `C(a, beta)` is unbounded near clamp points.
   - Add the `a = 1/6` counterexample.
3. **Conjecture 5.7 and Open 7.5.** Withdraw or restate them, for example "for Lebesgue-almost
   every instance", and note the clamp mechanism.
4. **Summary Q1 bullet 4 and Section 3.3.** Drop "exact invariant". State that `tau > 0` is
   sufficient, with a sharp constant on `tilt`, and that `tau = 0` strata can cost
   `Omega(eps^(-1/2))`.
5. **After Example 3.12 and at the start of Section 4.** Restrict the automatic-linear-growth claim
   to `n = 2`, or to interior strata under (R). Add counterexample A. Mention the RLT fragility of
   Example 3.12.
6. **Conjecture 7.1.** Withdraw it, or reformulate it in terms of near-optimal sets at scale
   `eps`.
7. **Proposition 4.7.**
   - Record that the optimal set also contains `{y = 1, X1 <= X2}`.
   - Either prove `O(1/eps)` (the quadtree above) or write `Omega(1/eps)`.
   - Rephrase "star-forest hypothesis" as "the fixed coordinates must be the centres".
8. **Proposition 4.6(a).** State it for `F = X0`, or add the missing closure argument.
9. **Corollary 4.3(c).** Change "matching" to "perfect matching".
10. **Corollary 3.3(b).** Note that the example violates (QD).
11. **Section 9.**
    - Credit Shectman–Sahinidis and BARON's incumbent rule (T–S p.243; Belotti et al. p.18).
    - Credit Wechsung's thesis result as reported by Kannan–Barton p.2.
    - Say that Lemma 4.1 is standard.
12. **Lemma 1.2 scope.** Add that pointwise-weaker relaxations are covered, and that bounds taken
    from children, auxiliary-variable branching and tolerance-accepted incumbents are not.

## 13. Commands run

All commands were run from `research-20260928b/reviews/face-exact/`, with Python 3.13.11,
PySCIPOpt 6.2.1 (SCIP 10.0), HiGHS through SciPy 1.18.0, Clarabel and mpmath 1.3.0. Each log sits
next to its script.

| Command | Log | What it establishes |
|---|---|---|
| `python3 scip_branchpoint.py` | `scip_branchpoint.log` | SCIP 10 default parameters; actual split points and node counts on the scout instance under defaults, with propagation and separation off, and with `midpull = 0` |
| `python3 kink_rules.py` | `kink_rules.log` | Exact piecewise-linear node bound matches the closed form; the note's kink row reproduced; SCIP-rule emulation; clamp-count failure of Proposition 5.4(b); Proposition 5.5(b) bounds |
| `python3 kink_cantor.py` | `kink_cantor.log` | `a = 1/6`: exact clamp replay and counts refuting Proposition 5.4(b) and Conjecture 5.7 |
| `python3 prop56_exact.py` | `prop56_exact.log` | Exact rational replay of Proposition 5.6 |
| `python3 box_aligned_quad.py` | `box_aligned_quad.log` | Counterexample A: optimal set, key inequality, B&B counts against the proved bound |
| `python3 path3_quadtree.py` | `path3_quadtree.log` | Proposition 4.7: larger optimal set, orthant bounds, `O(1/eps)` quadtree certificate with LP-verified leaves |
| `python3 misc_checks.py` | `misc_checks.log` | Lemma 3.1 quadrature; Lemmas 2.3 and 2.4 for joint trilinear envelopes; Proposition 3.13 construction; Theorem 6.1(b) first-order scheme; Theorem 5.3 averages |

These are targeted checks. Floating-point results are illustrations. The Proposition 5.6 replay
and the `a = 1/6` interval replay use exact rational arithmetic. No project-wide checks were run,
CI was not inspected, the note was not edited, and nothing was committed.

## 14. What remains unchecked

- The `Theta(eps^(-1/2))` upper bound for `R(1, .2)` with widest-side selection at `a = 1/6`. Only
  the lower bound `0.0745 eps^(-1/2)` is proved; the counts suggest `Theta`.
- Whether Proposition 4.6(a) holds for general polyhedral `F`.
- Whether Proposition 5.5(a) extends to SCIP's box-dependent `alpha_B`, and SCIP's node growth for
  `eps` below its feasibility tolerance.
- BARON's and ANTIGONE's current branching-point defaults. They are closed source, and only the
  2002 book and Speakman–Lee's report were read.
- The Section 8.2 rows other than the kink row: `kinkT`, `tilt` counts for all rules, `diag`,
  `iso`, `sharp_pt`, `aligned_quad`, the box QPs and pooling. The author's HiGHS and Clarabel
  fallback runs were not rerun.
- Lemma 3.9's measure-theoretic details beyond the standard argument; the constants of
  Theorem 5.1(b) and Proposition 5.2 beyond the checks above; Section 6(a)'s order-`beta`
  extension.
- Theorem 4.5 was checked by hand only; the author's `star_check.py` was not rerun.
- Conjecture 4.8, Question 5.8, and whether a log loss is needed in Corollary 3.3 under (QD).
- The literature leads listed in Section 11.
