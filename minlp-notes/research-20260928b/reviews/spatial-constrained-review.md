# Adversarial review: instance-dependent node complexity of spatial branch-and-bound with constraints

Date: 2026-09-28. Scope:
[`../bb-complexity/spatial-constrained/instance-dependent-node-complexity.md`](../bb-complexity/spatial-constrained/instance-dependent-node-complexity.md)
("the note"). The review focuses on Sections 4–8 and checks that the fixes from the
[earlier review](spatial-bb-review.md) were carried over correctly. The reviewer
did not write the note and did not edit it. Reviewer scripts and logs are in
[`spatial-constrained/`](spatial-constrained/). They do not reuse the author's code.

## Verdict

No counterexample to any numbered theorem, lemma or proposition was found. Every
proof in Sections 4–8 was checked step by step, and all hold under their stated
hypotheses except in the places listed below. The independent computations
agree with every checked claim, and they reproduce the author's Example 5.3
node counts exactly.

The problems are:

- **One hidden hypothesis.** The proof of Lemma 5.5 assumes that `P_ex` is
  polyhedral near `z*`. The statement does not include this assumption, and
  neither do Theorems 5.7 and 7.1(c), which use the lemma.
- **Two constant slips.**
  - Remark 3.7 drops a factor `2^n` when it transcribes the earlier review's
    ratio.
  - Corollary 6.5(b) states `10^n` where the proof gives `20^n`.
- **Remarks that are wrong or overstated as worded:**
  - the first remark after Theorem 8.2 (transversal directions);
  - the orbit-dimension claim for symmetric problems (8.1);
  - "the stratified form is necessary" (8.2);
  - the statement that McCormick violates (G^LB) (after Lemma 1.1);
  - calling `S_∞` a curve (Proposition 4.4(b));
  - the reach remark after Lemma 4.2;
  - the identification of `Phi_alpha` with Munos's profile (6.1);
  - "(G^LB) is preserved" when exact constraints are added for symmetry
    breaking.
- **A proof sketch.** Theorem 8.2(d) is labelled "proved", but its proof is a
  sketch.
- **Notation clash.** In Theorem 6.7, `K` denotes both the number of strata and
  the doubling constant of (R2).
- **Novelty.** Kannan–Barton (2017, Section 3.2) already treat clustering on
  nearly feasible, infeasible points with a good objective value. That is the
  precedent for the infeasible-side mechanism of Section 5, and the note does
  not cite it. Lemma 4.1 combines standard geometric-measure-theory tools; its
  new part is the per-box arcsine bound.

| Claim | Verdict | Main point |
|---|---|---|
| Carry-over of the earlier review's fixes (Sections 1–3) | correct with one fix | all fixes present; Remark 3.7 ratio should be `2(4 pi^2 Lambda/(alpha n))^(n/2)` |
| Lemma 1.1 (McCormick gap) | correct; fix one sentence | shows failure of (G^pt), not of (G^LB) |
| Lemma 4.1 (key lemma) | correct | proof checked; numerically at most 0.71 of the bound (d = 1) and 0.43 (d = 2) over optimized boxes |
| Lemma 4.2 (two-point constant ⇒ local multiplicity 1) | correct; fix remark | Federer transfer needs `S` relatively open in `Sigma` |
| Lemma 4.3 (graphs) | correct | |
| Proposition 4.4 (comb; curvature is not enough) | correct; wording | `S_∞` has infinitely many components; a connected spiral also works |
| Theorem 4.5 (i)–(iii) (stratified integral bound) | correct | |
| Theorem 4.6 (covering bound), Corollary 4.7 | correct | |
| Lemma 5.1, Theorem 5.2 (tube dichotomy) | correct | (D) verified on all leaves of three test trees |
| Example 5.3 (isotropic / anisotropic / propagation) | correct | counts reproduced exactly |
| Theorem 5.4 (Lagrangian transfer, covering) | correct | one-directional transfer (lower bounds only), not an equivalence |
| Lemma 5.5 ((OD) near KKT points) | correct with fix | "`P_ex` polyhedral near `z*`" must be in the statement |
| Proposition 5.6 (integral form via a shift) | correct | |
| Theorem 5.7 (`log(1/eps)` for constraint-gap schemes) | correct with the Lemma 5.5 fix | log growth confirmed on two instances |
| Lemma 6.1, Theorems 6.2, 6.4 | correct | Lemma 6.1 verified level by level on two 4-ary trees |
| Theorem 6.3 (covering characterization) | correct; fix interpretation | needs the sup over `eta`; a single-scale version fails with uniform constants |
| Corollary 6.5 | correct with fix | constant `20^n`, not `10^n` |
| Theorems 6.6, 6.7 (integral characterization under (R)) | correct; rename one symbol | `K` is used for two things |
| Proposition 6.8, Remarks 6.9, 6.10 | correct | |
| Theorem 7.1 (a), (b) | correct | lower prefactor `(alpha/M_L)^(d/2)` verified; the uniqueness hypothesis conflicts with Example 7.3 (two minimizers) |
| Theorem 7.1 (c) | correct with fix | needs a nonzero multiplier and the Lemma 5.5 fix |
| Theorem 7.2 (Morse–Bott) | correct | |
| Example 7.3 | correct | (QG) constants checked numerically |
| 8.1 (exponent = half the box dimension) | correct | |
| 8.1 symmetric problems | correct with fixes | orbit dimension at points of `M`; (G^pt), not (G^LB), is preserved |
| 8.2 (active constraints) | mostly correct | "necessary" holds only for isolated boundary minimizers |
| Corollary 8.1 (tightening) | correct | constants exponential in `n` and depend on `Lambda/alpha` |
| Theorem 8.2 (a)–(c), (e) | correct | 1D exact check: `N_opt ≈ 4.19 eps^(-1/2)` against bound `0.333 eps^(-1/2)` |
| Theorem 8.2 (d) | correct, proof sketched | constants and hypotheses not written out |
| Remarks after Theorem 8.2 | first remark wrong as worded | contradicts the third remark |
| Section 9 computations | consistent | two lower-bound entries re-derived in closed form; the sphere sweeps were not re-run |
| Section 10 novelty | incomplete | Kannan–Barton 2017 Section 3.2 missing |

## 1. Were the earlier review's fixes incorporated?

Every item in the earlier review's verdict table was checked against Sections
1–3 of the note:

- (G) is stated only at feasible points, for the projected lifted value.
- The relative-tolerance reduction and the caveat for incumbents accepted
  within a feasibility tolerance are included (the reduction was re-derived in
  all three sign cases).
- Pruning by infeasibility and exact arithmetic are covered.
- Inherited bounds are covered, and children are recorded when a bound comes
  from sub-boxes.
- Frames are decomposed per round.
- Objective-cutoff propagation is excluded.
- The AM–GM loss is noted, and the low-rank row claims a lower bound only.
- In Theorem A, `F = X0` is marked as essential, and the tighter count
  `(sqrt(kappa n)+2)^n` is used.
- The extra term is dropped from Theorem C's `Lambda`.
- The (QD) condition is corrected (Lemma 3.6).
- The sparse-digit correction to the sharp-minimum row is included.
- The McCormick lower bound is stated as proved for widest-side bisection only.
- The novelty wording follows the earlier review.

**One slip (Remark 3.7).** From
`(alpha n/pi^2)^(n/2) I <= N_opt <= |T_bis| <= 1 + 2^(n+1) Lambda^(n/2) I`, the
ratio of the constants is

```
2^(n+1) Lambda^(n/2) (pi^2/(alpha n))^(n/2) = 2 (4 pi^2 Lambda/(alpha n))^(n/2),
```

as in the earlier review, not `2 (pi^2 Lambda/(alpha n))^(n/2)`. With
`Lambda = K(alpha' n/4 + 1)`, the next line should read
`2 (pi^2 K (kappa + 4/(alpha n)))^(n/2)`. The note's version understates the
ratio by `2^n`. The qualitative point, that the ratio does not depend on `eps`
but depends on `K`, `kappa` and `K/alpha`, is unaffected.

**Lemma 1.1, last paragraph.** "They violate (G^LB_alpha) for every
`alpha > 0`, because the gap is 0 on edges where `q_B > 0`" does not follow as
written. A zero pointwise gap on edges contradicts (G^pt_alpha). (G^LB_alpha)
bounds `LB(B)`, which can be lower elsewhere. Suggested wording: "They violate
(G^pt_alpha) for every `alpha > 0`. (G^LB_alpha) fails as well on the
face-exact example: it has a 2-leaf certificate for every `eps`, which Theorem
4.6 rules out under (G^LB_alpha) because the optimal set is a segment."

## 2. Section 4: key lemma and stratified lower bounds

**Lemma 4.1: correct.** Each step checks:

- Cauchy–Binet gives `sum_I det(U_I)^2 = 1`.
- `J_I` is continuous (it does not depend on the choice of orthonormal basis),
  so `S^I` is Borel.
- AM–GM is applied over the coordinates in `I` only, using `q_B >= sum_{i in I} a_i`.
- The integrand depends only on `y_I`, so the area formula for the linear map
  `pi_I` on the `d`-rectifiable set `S^I ∩ B ∩ A` applies. The Jacobian is the
  tangential Jacobian `J_I`.
- The multiplicity is at most `M^I(S; A ∩ B)`.
- The arcsine integral equals `pi` on every interval.

`sigma = H^d` restricted to an embedded `C^1` manifold equals the Riemannian
volume, so there is no measure-theoretic gap. The bound is vacuous when
`M^I = inf`, and the text says so.

*Numerics* ([`key_lemma_stress.py`](spatial-constrained/key_lemma_stress.py),
[log](spatial-constrained/key_lemma_stress.log)). The integrator is
independent of the author's. On each run of constant dominant coordinate it
integrates in `theta` with `y_i = l_i + w_i sin^2 theta`, so the integrand is
bounded and there is no quadrature singularity. The multiplicity is computed
per box.

- Sanity checks: the circle in `[-1,1]^2` gives exactly `2 pi`, and the unit
  sphere in `[-1,1]^3` gives `2 pi` (error `1e-3`). Three comb teeth match the
  closed form of Proposition 4.4 to 6 digits, and the limit `I/k = 1.84030`
  matches the note.
- Search: 1500 random boxes per curve and 500 per surface, then Nelder–Mead on
  the worst cases. The largest values of (integral)/(bound with the local
  multiplicity) were:
  - curves (`d = 1`): 0.7071 (lines, circle), 0.709 (ellipse with axes 1 and
    0.1), 0.56–0.58 (helices in `R^3`);
  - surfaces in `R^3` (`d = 2`): 0.42 (sphere, ellipsoid), 0.30–0.43 (planes).
- The value `1/sqrt 2` in `d = 1` is attained by a segment lying on a box edge
  (integral `pi`, bound `pi sqrt 2`). So the constant is sharp to within about
  `sqrt 2` when the multiplicity is 1.
- The author reports 6.2518 as the largest circle value found, which is below
  the `2 pi` of the bounding square. The reviewer's search confirms that the
  bounding square is a local maximum at exactly `2 pi`
  ([`circle_sup.log`](spatial-constrained/circle_sup.log)). The author's search
  was simply weak; the claim is unaffected.

**Lemma 4.2: correct.** The proof is complete:

- The singular values of `pi_I` restricted to `T_y S` are at most 1, so
  `sigma_d >= J_I >= binom(n,d)^(-1/2)`.
- Only `y in S^I` is used.
- The global fibre count is correct: the sub-boxes have diameter
  `< rho_*`, and a point on a shared face only helps.

The remark after the lemma should read "every **relatively open** subset `S`
of a `d`-dimensional `C^1` submanifold `Sigma` with `reach(Sigma) >= tau`". The
two-point constant is defined with `T_y S`, which equals `T_y Sigma` only if `S`
has the same dimension as `Sigma`. Federer's Theorem 4.18(2) gives the
inequality for every `r < reach`, and the limit gives `tau`. The unit circle
attains equality: the numerical maximum ratio is exactly 1.000000
([`qg_example73.log`](spatial-constrained/qg_example73.log)).

**Lemma 4.3: correct.** It uses Taylor's theorem with the integral remainder
for vector-valued `phi` on the convex `U`, and `|h| <= |z - y|` because `h` is
the `T`-component of `z - y`.

**Proposition 4.4: correct, with one wording fix.**

- Part (a) and the closed form were verified.
- In part (b), `S_∞` is an embedded one-dimensional `C^∞` submanifold with
  infinitely many components, not "a curve".
- A connected counterexample also exists: the spiral
  `rho(theta) = r(1 + 1/(1+theta))`, `theta >= 0`. It is embedded, its
  curvature is `O(1/r)`, and it has infinite length inside `[-2r, 2r]^2`. Since
  `q_B` is bounded there, the integral is infinite.
- So bounded curvature fails even for connected strata. Positive reach is the
  right hypothesis, as the note says.

**Theorem 4.5: correct.**

- (i) follows directly from (V) and Lemma 4.1.
- (ii): every point of `S_♭ ∩ C` lies within sup-distance `r_*` of a vertex
  in every coordinate. Points with the same `{-,+}` label on a common fibre are
  within `2 r_* sqrt(n-d) = rho_*`, so Lemma 4.2 applies. Ties are harmless,
  because a point labelled `-` is within `r_*` of `l_i`. The constant
  `2^(n-d) binom(n,d) C_{n,d}` is correct.
- (iii) is Theorem 3.1 restricted to `S`.

A sanity case for (ii): let `F` be the comb of `k` horizontal lines in
`[0,1]^2`, with `f ≡ 0` written in DC form so that the gap is exactly `q_B`.

- Boxes whose top and bottom edges lie on consecutive lines, with width
  `2 sqrt(eps)`, form a certificate of about `(k+1)/(2 sqrt eps)` boxes.
- Form (ii) gives `k/(8 sqrt 2 pi sqrt eps) ≈ 0.056 k eps^(-1/2)`.
- Form (i) gives `0.225 eps^(-1/2)`, losing the factor `k`, as the note says.

**Theorem 4.6 and Corollary 4.7: correct.** Theorem 3.2 does follow, with the
same constant. In 4.7(b), `log(1/delta) = (1/2) log(1/eps) + O(1)` is
correctly handled.

## 3. Section 5: constraint-gap schemes

**The (T) hypothesis.** An alphaBB relaxation `g - beta q_B <= 0` has relaxed
set exactly `{v <= beta q_B}`. The same holds for two-sided equalities, and for
several constraints with `beta = min beta_j`. The secant of a concave
constraint such as `|y|^2 >= 1` is a natural uniform (T) scheme with
`beta = 1`. One modelling point is implicit: convex constraints that the
relaxation keeps exactly must be placed in `P_ex`. Otherwise tube points that
violate them are not in `R_B`, and (T) fails.

**Lemma 5.1 and Theorem 5.2: correct.** Super-optimal points satisfy
`beta d_i^2 <= beta q_C < v`, and the vertex-cube cover follows.

**Example 5.3: correct.**

- (a): the middle slab's relaxed set is `{z_2 = 0}`, the bottom slab is empty,
  and the top slab has bound 0. So `N_opt <= 3` for every `eps`. The Summary's
  "needs 3 leaves" should read "has a 3-leaf certificate".
- (b): the strip lies in `W(eps, 2 eps)`, which gives `(5/16)(2 eps)^(-1/2)`.
  The point `(0.05, -1.2)` makes every bottom box of `z_2`-only bisection
  relaxed-feasible, with `a_1 = 1.5625 >= 1.2`.
- (c) is immediate.
- The upper bound uses (U^q_1), `kappa = 1`, `L = 1` and
  `c_g = 1/s0`; all were checked.

The reviewer's code
([`constraint_gap_checks.py`](spatial-constrained/constraint_gap_checks.py),
[log](spatial-constrained/constraint_gap_checks.log)) derives the node bound
separately (roots in `z_2` for each `z_1`, then a golden-section search). On 240
random boxes it never exceeds a brute-force grid minimum. It reproduces the
author's counts exactly:

- anisotropic widest-side: 9, 45, 189, 381, 1533, 6141, 6141;
- isotropic widest-side: 29, 93, 253, 1021, 3069, 8189, 32765.

The Theorem 5.2 bound lies below the leaf counts at every `eps`.

**Theorem 5.4: correct.**

- Step 1: `f(z) <= f* - eps - (eta+eps)` once
  `eta + eps <= mu_0^2/(9 C_2)`.
- Step 2: (D) at the super-optimal point `z`.
- Step 3: `t_* <= r` is equivalent to `eta + eps <= c_1 mu_0/(3 beta)`.
- `4r = 2 sqrt((eta+eps)/alpha_eff)` with `alpha_eff = mu_0 beta/(12 c_1)`.

This is a one-directional transfer: constraint gaps give lower bounds as if
there were an objective gap `alpha_eff`. It is not an equivalence of the two
gaps.

**Lemma 5.5: correct with one fix.** The following steps check:

- LICQ makes the system for `ê` solvable.
- The KKT identity gives `grad f(z*)·ê = -(sum mu*_j + sum |lambda*_k|)`.
  Exact constraints and constraints with zero multiplier contribute 0, because
  they have `grad·ê = 0` or a zero multiplier.
- The descent and violation estimates hold with the stated `c_1`.
- Inactive constraints keep their slack.

However, the last step uses "`P_ex` polyhedral near `z*`, which we assume", and
the lemma statement does not include this. Theorem 5.7 and Theorem 7.1(c)
inherit the gap. There are two fixes:

- *Simplest:* add to Lemma 5.5 the hypothesis "the active constraints of `P_ex`
  are affine near `z*`", and cite it in Theorems 5.7 and 7.1(c).
- *General:* replace the ray `y + t e` by a `C^1` curve that holds the active
  exact constraints at their values at `y`, with initial velocity `e`. LICQ and
  the implicit function theorem give such curves uniformly for `y` near `z*`.
  Theorem 5.4 then needs `|z - y| <= (1 + O(t)) t`, which changes only the
  constants.

**Proposition 5.6: correct.** (D) at `Z(y)` gives
`(m+eps)^(-d/2) < (A_1/beta)^(d/2) q_C(Z(y))^(-d/2)`. The area formula for the
injective `C^1` map `Z` and Lemma 4.1 on `S'` then give the bound. The sets
`Z^(-1)(C)` cover `S` because `Z(S) ⊆ X0` and `P` covers `X0`.

**Theorem 5.7: correct, given the Lemma 5.5 fix.** All five steps were
checked:

- A translation preserves Jacobians, fibres and the partition into `S^I`,
  hence also `M^I`.
- `grad m~(0) = 0` holds because `z*` minimizes `m >= 0` on
  `S_loc ⊆ F` and `m~` is `C^2`.
- `||D psi - I|| <= 1/2` gives injectivity and a ball in the image.
- The Jacobian bound
  `j_0 = 2^(-d)(1 + sup ||D phi||^2)^(-d/2)` follows from `Z_0 = G' ∘ psi ∘ G^(-1)`.
- The layer-cake step and the constant `theta_0 (d/4) M_L^(-d/2) log(M_L r_1^2/(2 eps))`
  are correct.
- The third smallness condition of Theorem 5.4 is not needed here, and the
  proof correctly does not use it.

"SOSC is not needed" is right: only the upper bound
`m <= (M_L/2)|y - z*|^2` on `S_loc` is used.

*Numerics.* Two instances were checked; in each, the lower bound lies below
the counts and the tube dichotomy (D) holds on every leaf.

1. `f = z_2 + z_1^2` with `-z_2 <= 0` loosened isotropically
   (`d = 1`, multiplier 1, instance F1 in the log).
   - Widest-side counts are 17, 29, 39, 51, 61, 73, 85 for
     `eps = 1e-1 … 1e-7`, about +11 per decade.
   - The explicit Proposition 5.6 bound, with `A_1 = 3`, `j_0 = 1`,
     `M(S') = 1` and `r = 1/6`, is 0.13 … 1.81.
   - The isotropic three-slab boxes have bounds -1.2 and -0.6, so they are not
     a certificate, consistent with the theorem.
   - With anisotropic loosening the three-slab certificate is valid (bounds
     `inf, 0, 0`). Yet widest-side bisection still grows logarithmically (9 …
     73), because bisection is not instance-optimal.
2. `min |y - c|^2` subject to `|y| >= 1`, with the secant relaxation (a genuine
   (T_{0,1}) scheme; `d = 1`) ([`reverse_convex_tube.log`](spatial-constrained/reverse_convex_tube.log)).
   - Counts are 19 … 159 for `eps = 1e-1 … 1e-9`, adding 10–24 nodes per
     decade.

The note could cite instance 2 as a natural example: a convex objective with an
active reverse-convex constraint.

**Remark 5.8** is accurate. The curved-stratum question is correctly left open.

## 4. Section 6: upper bounds and characterization

**Lemma 6.1: correct.**

- The witness `z in R_D` lies in `D ∩ P_ex ⊆ X0 ∩ P_ex`, so (EB) applies.
- (Lip) is used on the segment `[y, z] ⊆ X0`.
- The index-distance-2 argument gives `5^n`.
- `sum_{j<j_0} 2^(nj) <= 2^(n j_0)`.

On the 4-ary trees of the flat example (F0) and the KKT example (F1), with
`tau = 1/2`, `kappa = 1`, `Lambda = 1` and `1.89`, and `j_0 = 1`:

- every non-pruned level-`j` cube with `j >= j_0` satisfies both
  `eps < Lambda s_j^2` and the per-level count
  `<= 5^n N_j(E(Lambda s_j^2 - eps))`;
- the total stays below the lemma's right-hand side (for example, 32765 against
  820417 at `eps = 1e-7`).

**Theorem 6.2: correct.** Only members of `P` that meet `F` are used, so `|P|`
can be replaced by `|P_F|`. The tightening statement relies on this, and the
note should say so. The rule "a closed interval of length `2r` meets at most
`2r/s + 2` cells" is right.

**Theorem 6.3: correct.** The per-cube count `3^n` and the rescaling factor
`max(1, ceil(a))^n` are right.

The interpretation needs a fix. `Phi_alpha(eps)` is the supremum over all
`eta`. Up to constant factors in the scale, it is the **running supremum over
`eta >= eps`** of Munos's diagonal profile `N(E(eta), sqrt(eta))` for the
semi-metric `|x - y|^2`, not that profile at `eta = eps`. The difference
matters.

*Counterexample to a single-scale version with uniform constants.* Take
`K` well-separated local minimizers at level `f* + eta_1`, spaced more than
`4 sqrt(2 eta_1/alpha)` apart.

- For `eps < eta_1`, (V) forces each of them within sup-distance
  `sqrt(2 eta_1/alpha)` of a vertex of its certificate box. Hence
  `N_opt >= K/2^n`.
- Meanwhile `N_inf(E(eps), c sqrt(eps)) = O(1)` for every constant `c`.

So "N_opt is within `C log(1/eps)` of the covering number of `E(eps)` at scale
`sqrt(eps)`" is false with constants that do not depend on the instance. The
note's statement with the supremum over `eta` is correct.

**Theorem 6.4: correct.** The offset count `2r/s_j + 3` is right, and the upper
bound does not use (G^LB), as stated. It was checked on the F0 and F1 trees;
the bounds are very loose.

**Corollary 6.5: correct with a fix to (b).** Theorem 6.4 gives
`1 + 2^n [2^(n j_0) + 5^n (2 sqrt(Lambda/c_g)+3)^n sum_j N_j(M)]`, and a finite
`M` has `N_j(M) <= 2^n |M|`. So the constant is
`2^n · 5^n · 2^n = 20^n`, not `10^n`. Part (a) is correct; if
`dim_up(M) = 0`, the ratio tends to 0 anyway.

**Theorem 6.6: correct.**

- Steps 1–7 check, including the disjointness of `Q(z, s_j/2)` when the
  centres are pairwise more than `s_j` apart.
- The use of (R2) needs `m(z) <= K_R Lambda s_j^2 <= K_R t_0` and
  `s_j/2 <= r_0`; both are guaranteed by the choice of `j_1`.
- The geometric sum is at most `2 theta(x)^(-d)`.
- The corner count `(2 rho + 6)^n` is right.

**Theorem 6.7: correct.** Two small points:

- The symbol `K` in `c_low = (1/K) min_k …` is the number of strata (from
  Corollary 4.7(a)). Hypothesis (R) uses `K` for the doubling constant. Rename
  one of them.
- The restriction `eps <= t_0` is not needed for either inequality.

A related sanity point: if `M(S_k) < inf`, the area formula gives
`H^(d_k)(S_k) < inf`, so `I_k(eps)` is finite. The two sides are therefore
consistent.

**Proposition 6.8, Remarks 6.9 and 6.10: correct.** The following were
checked:

- clipping keeps `z*` a vertex, and cells without vertex `z*` have
  `|z - z*|_inf >= s` even after clipping;
- the odd-denominator argument;
- the binary-bisection count `(2^n - 1) 5^n N_j`.

## 5. Section 7: regular instances

**Theorem 7.1: correct.**

- (QG) follows from Theorem 1 of the cluster-free note applied to degenerate
  boxes. That theorem states the constant `gamma/4`.
- In (a), the lower bound follows from Theorem 4.5(ii) on a graph piece of
  `S_loc`, with `r_1` chosen so that `M_L r_1^2 < alpha r_*^2`. The prefactor
  `(alpha/M_L)^(d/2)` is right for the lower bound. `eps_0` depends on
  `alpha r_*^2` and `M_L r_1^2`.
- In (b), the sharp-growth derivation (steps 1–5) checks. When every active
  constraint is an equality, `F` is locally `{z*}` and the claim is trivial.

Three fixes:

- *Uniqueness.* The theorem assumes a unique global minimizer, but Example 7.3
  applies it with `k = 1`, where there are two minimizers `±e_1`. The proof
  extends directly to finitely many nondegenerate minimizers; state that.
- *(c).* "Some active non-exact constraint" should read "some active non-exact
  constraint with a nonzero multiplier". Under (SC) this is automatic for
  inequalities, but not for equalities. (c) also needs the Lemma 5.5 fix.
- *Wording.* In Section 8.2 and the comparison with Neumaier, "`Theta(log(1/eps))`
  with prefactor `(alpha/M_L)^(d/2)`" should say "lower-bound prefactor". The
  upper prefactor is of a different form (Open problem 2).

**Theorem 7.2: correct.**

- The lower bound follows from Theorem 4.5(ii) with `S_♭ = M`.
- In the upper bound: a cube of side `2 s_j` meets at most `4^n` cells; the
  Niyogi–Smale–Weinberger volume bound
  `(1 - r^2/(4 tau^2))^(p/2) omega_p r^p >= (3/4)^(p/2) omega_p r^p` holds for
  `r <= tau`; and the geometric sum is right.
- The stated constant matches the derivation.

**Example 7.3: correct.**

- The secant margin is exactly `q_B`.
- (EB) holds with `kappa = 1`, provided `|y| <= 1` is placed in `P_ex`.
- The (QG) constants were checked on 400,000 random sphere points, including
  points near `M` ([`qg_example73.log`](spatial-constrained/qg_example73.log)).
  The minimum of `m/dist^2` was 0.2513 against the claimed 0.25, 0.2501 against
  0.25, 0.354 against 0.35, and 0.0503 against 0.05.
- The quartic example satisfies (R1)–(R3); in fact (R3) holds with
  `theta = 2`.

## 6. Section 8: consequences

**8.1, exponent formula: correct** under the stated hypotheses. The lower half
needs only (G^LB).

**8.1, symmetric problems: needs two fixes.**

- "`dim_box(M) >= max orbit dimension`" is false if the maximum is taken over
  all orbits. Take `SO(2)` acting on the unit disk and `f = |y|^2`: `M = {0}` is
  a fixed point, while generic orbits have dimension 1. Replace it with
  "`dim_box(M) >= dim(G·y)` for every `y in M`". Likewise, "each continuous
  symmetry direction costs `eps^(-1/2)`" holds only for directions that act
  nontrivially on `M`.
- "Keeping the added constraints exact preserves (G^LB)": adding exact
  constraints shrinks `R_B` and can raise `LB(B)`, so (G^LB) alone is not
  inherited. (G^pt) is inherited, because a feasible `y` stays in the smaller
  `R_B`. The upper-bound hypotheses (EB) and (QG) must also be re-checked for
  the new `F`. In the worked example they hold, since LICQ holds on the half
  circle.

**8.2: mostly correct.** "So the stratified form of Theorem 4.5 is necessary,
not a refinement" is overstated:

- For `p >= 1`, the covering bound (Theorem 4.6 with `eta = 0`) already gives
  the exponent `p/2`. For B3_all it gives order `eps^(-1)`.
- The stratified integral is needed for isolated minimizers on a boundary
  stratum (`p = 0`, for example B3_iso). There both the covering bound and the
  full-dimensional integral stay bounded as `eps -> 0`, while the true count and
  the stratified bound grow like `log(1/eps)`.

**Corollary 8.1: correct.** Two points should be stated:

- The constant in (b) is exponential in `n` and depends on `Lambda/alpha`.
- Under (G^pt_alpha), runs with (R-inf) rounds are also covered, because (R-inf)
  pieces do not meet `F`.

The paragraph on "interval evaluation … exact on boxes for monotone or
separable expressions, where (G) fails" is heuristic and should be labelled as
such. Cutoff FBBT also contracts domains by backward propagation, not only by
evaluating the range.

**Theorem 8.2: (a)–(c) and (e) correct; (d) sketched.**

- (a): `delta_B(y) = max_i d_i(y)` is the sup-distance to the vertex set, since
  the minimum over vertices splits coordinate by coordinate. The covering step
  is correct.
- (b): the offset `1 + ceil(kappa tau)` is right.
- (c): the volume-to-cover constant `2^(-n) omega_n (alpha^2/(8 M_f eps))^(n/2)`
  was re-derived.
- (e): the orthant integral `alpha^(-n)[1 + n log(alpha s0/(2 eps))]` is right.
- (d) is proved with "~" steps and Weyl's formula, without constants or a full
  list of hypotheses. It should either be written out, with (G^1_alpha),
  (U^1_tau), `m` comparable to `dist(·, M)^2` near `M`, and `m` bounded below
  away from `M`, or be labelled "proof sketched". The result itself is standard
  and correct.

*1D exact check* ([`first_order_1d.py`](spatial-constrained/first_order_1d.py),
[log](spatial-constrained/first_order_1d.log)). The instance is
`f = (y - 1/3)^2` with the vertex-Lipschitz bound, `L_B = 2 Lip`,
`alpha = 4/3` and `tau = 4`. The bound of a sub-interval is at least that of
the interval, so the greedy sweep gives the exact `N_opt`.

- `N_opt sqrt(eps)` tends to 4.19 over `eps = 1e-2 … 1e-10`.
- Bounds (a) and (c) give `0.333 eps^(-1/2)`. Bound (e) is lower by the log
  factor, as the note says.
- Bisection stays below the (b) bound.
- In 1D the log in (e) is not attained.

**Remarks after Theorem 8.2.** The first remark ("The exponents double only in
the directions along `M`. Transversal quadratic directions contribute 1/2 each
in both regimes") contradicts the third ("A second-order gap removes the
transversal loss entirely"). The exponents are `p/2` and `(n+p)/2`:

- along `M`, the contribution goes from 1/2 to 1 per direction;
- transversal directions contribute 0 under a second-order gap and 1/2 each
  under a first-order gap.

What is the same in both regimes is the tube width `eps^(1/2)`; what changes is
the cell side (`eps^(1/2)` against `eps`). Reword accordingly.

## 7. Section 9 computations

The reviewer did not re-run the sphere and ball sweeps. Checks done:

- Two lower-bound entries were re-derived in closed form.
  - S2_circ at `1e-6`: `sqrt(1.1) · 2 pi · 10^3/(pi sqrt 2 · 4) = 370.8`.
  - S3_circ at `1e-6`:
    `1.1 · 4 pi · atan(sqrt(0.5/eps))/sqrt(0.5 eps)/(8.5473 · 6) = 598.2`.
    For S3_circ the boundary-sphere bound (0.598 `eps^(-1/2)`) exceeds the
    optimal-circle bound (0.303 `eps^(-1/2)`), so the column label "boundary
    sphere" is accurate.
- `M(S) <= 2n` for the sphere and `M <= 4` for the great circle in `R^3` were
  checked. For the circle, `S^{3}` is empty, because `J_3 = 0` on the circle.
- The exponents and ratios quoted in Tables 9.1 and 9.2 match the author's
  logs.

The computations illustrate the exponents but do not measure `N_opt`, as the
note says.

## 8. Reviewer computations

Commands run from `research-20260928b/reviews/spatial-constrained/`:

| Command | What it checks | Result |
|---|---|---|
| `python3 key_lemma_stress.py > key_lemma_stress.log` | Lemma 4.1 on circle, ellipse, lines, helices, sphere, ellipsoid and planes; Proposition 4.4 closed form | largest ratio to the bound: 0.709 (`d = 1`) and 0.429 (`d = 2`); sanity values exact |
| `python3 circle_sup.py \| tee circle_sup.log` | largest circle integral over boxes | the bounding square is a local maximum at `2 pi` |
| `python3 constraint_gap_checks.py > constraint_gap_checks.log` | own node bound against a grid; Example 5.3 counts; Theorem 5.2; (D) on leaves; Lemma 6.1 per level; Theorem 6.4; Proposition 5.6 bound on a KKT instance | author's counts reproduced exactly; no violations |
| `python3 reverse_convex_tube.py \| tee reverse_convex_tube.log` | Theorem 5.7 on a secant-relaxed reverse-convex constraint | logarithmic growth; (D) holds on all leaves |
| `python3 first_order_1d.py > first_order_1d.log` | Theorem 8.2(a), (b), (c), (e) with exact 1D `N_opt` | all bounds hold; `N_opt ≈ 4.19 eps^(-1/2)` |
| `python3 qg_example73.py \| tee qg_example73.log` | (QG) constants of Example 7.3; two-point constant of the circle | constants confirmed; the circle attains equality |

All runs are floating point and certify nothing. The node bounds come from
closed forms, golden-section search or exact 1-D duals; the first two were
validated against brute-force grids. The theorems rest on their proofs. No
project-wide checks were run, CI was not inspected, and nothing was committed.

## 9. Novelty assessment

**Sources.**

- Local full texts read:
  - Neumaier (2004), Section 15 (the cluster passage, including "in the
    formulas, `n` must be replaced by `n − a`");
  - Kannan–Barton (2017): abstract, Sections 2–3 (the definitions of the
    regions `X_1 … X_5`, Lemmas 1–3, and Section 3.2 on `X_3`) and the
    conclusion;
  - the repository's cluster-free note (Theorem 1).
- Searched with grep: Wechsung et al. (2014), Du–Kearfott (1994) and the local
  Kannan thesis (for the definition of pointwise convergence).
- Web search was exhausted (200 of 200 calls). Eight arXiv API queries went
  through WebFetch; two more failed with HTTP 503 and 429 errors. They covered
  lower bounds for branch-and-bound box counts, the cluster problem, certified
  Lipschitz sample complexity, near-optimality dimension, tree size for spatial
  branch-and-bound, certified smooth global optimization, error certificates,
  and certified zeroth-order global optimization. They found nothing closer
  than Bachoc–Cesari–Gerchinovitz (2102.01977).
- For Munos (2011), Bachoc et al. (2021), Bouttier et al. and Hansen–Jaumard–Lu,
  the reviewer relies on the earlier review's reading (Section 9 there).

**By claim.**

- **Section 5 (tube dichotomy, Theorems 5.2, 5.4, 5.7).** Kannan–Barton (2017)
  split the domain into regions `X_1 … X_5`. `X_3` is the set of infeasible
  points with violation at most `eps^f` and objective at most `f* + eps^o`. The
  paper states that "clustering can occur both on nearly-optimal and
  nearly-feasible regions" (abstract). Their Lemmas 2–3 and Section 3.2 give
  worst-case, fixed-width *upper* estimates of the number of boxes covering
  `X_3`, in terms of the convergence order at infeasible points. This is the
  precedent for the infeasible-side mechanism, and the note's Section 10 should
  cite it. Not found in the sources checked:
  - the lower-bound form for adaptive trees;
  - the tube hypothesis (T);
  - the contrast between isotropic and anisotropic loosening;
  - the Lagrangian transfer with `alpha_eff`;
  - the `log(1/eps)` bound of Theorem 5.7.

  Originality: modest to moderate. This is the most original part of the note.
- **Lemma 4.1.** The ingredients are standard geometric measure theory:
  - choosing a coordinate projection with Jacobian at least
    `binom(n,d)^(-1/2)` via Cauchy–Binet;
  - the area formula with a multiplicity (Banach indicatrix) function;
  - bounding the multiplicity by reach (Federer's two-point inequality, as used
    in manifold-learning covering arguments).

  The new part is the per-box arcsine bound for `q_B^(-d/2)` on strata, which
  was not found in the sources checked. Originality: modest. The note should
  say that the tools are standard.
- **Theorem 4.5 and Proposition 4.4.** A natural application. Originality:
  modest.
- **Theorem 4.6 and Corollary 4.7.** The covering form of Theorem D, which the
  earlier review rated as a standard packing argument. Originality: low.
- **Section 6.** Lemma 6.1 and Theorems 6.2–6.4 are the level-by-level count
  (Perevozchikov, Munos DOO) plus an error bound, as in the constrained cluster
  analyses. Theorem 6.3 is the second-order, constrained analogue of the
  two-sided Lipschitz characterization of Bachoc et al., and the note credits
  it. Theorems 6.6 and 6.7 are the integral form, analogous to Bachoc et al.'s
  Theorem 1 and the scout's Theorem C. Originality: low to modest.
- **Section 7.** Theorem 7.1 is a rigorous, all-scales version of Neumaier's
  heuristic, and the note credits it. Theorem 7.1(b) and Proposition 6.8 match
  Kannan–Barton's observation that first-order convergence can suffice when
  `f` grows linearly on feasible directions. Theorem 7.2 is new in this form.
  Originality: modest.
- **Section 8.** The exponent formula is the near-optimality-dimension
  statement for the semi-metric `|x - y|^2`. The tightening corollary was
  already derived in the earlier review (Section 3 there). Theorem 8.2(a) and
  (e) are the Lipschitz covering argument (the earlier review's Section 9.3)
  and the Bachoc et al. integral, written for boxes. The note should say so
  explicitly instead of listing it only as a "first-order analogue".
  Originality: low.

Overall, the novelty claim in Section 10 is defensible once Kannan–Barton 2017
Section 3.2 is added as the precedent for Section 5. That claim is: rigorous
lower bounds for relaxation-based spatial branch-and-bound with adaptive trees,
same-relaxation tightening and constraints, as far as the bounded search found.
An unsuccessful search does not establish novelty.

## 10. Precise corrections

1. Remark 3.7: ratio `2 (4 pi^2 Lambda/(alpha n))^(n/2) = 2 (pi^2 K (kappa + 4/(alpha n)))^(n/2)`.
2. Lemma 1.1, last paragraph: "violate (G^pt_alpha)"; justify the failure of
   (G^LB) by the face-exact example and Theorem 4.6.
3. Remark after Lemma 4.2: "relatively open subset of a `d`-dimensional `C^1`
   submanifold".
4. Proposition 4.4(b): "one-dimensional submanifold with infinitely many
   components"; optionally add the connected spiral.
5. Lemma 5.5 statement: add "the active constraints of `P_ex` are affine near
   `z*`", or use curves as described in Section 3. Carry the change into
   Theorems 5.7 and 7.1(c).
6. Theorem 5.4 and the Summary: describe the result as a transfer, not an
   equivalence. Summary item 4: "has a 3-leaf certificate".
7. Theorem 6.2: note that `|P|` may be replaced by `|P_F|`.
8. Section 6.1 Interpretation: `Phi_alpha` is the running supremum over
   `eta >= eps` of Munos's diagonal profile. Add the counterexample to a
   single-scale version.
9. Corollary 6.5(b): `20^n` instead of `10^n`.
10. Theorem 6.7: rename the number of strata (for example `K_S`); drop
    `eps <= t_0`.
11. Theorem 7.1: allow finitely many minimizers, or change Example 7.3. In (c),
    require a nonzero multiplier. In 8.2 and the Neumaier comparison, say
    "lower-bound prefactor".
12. Section 8.1: orbit dimension at points of `M`; (G^pt), not (G^LB), is
    preserved when exact constraints are added; re-check (EB) and (QG).
13. Section 8.2: restrict "necessary" to isolated boundary minimizers.
14. Theorem 8.2(d): write the proof out with hypotheses and constants, or
    label it "proof sketched" in the status table.
15. First remark after Theorem 8.2: reword as in Section 6 above.
16. Section 8.3, last paragraph: label the interval-evaluation explanation as
    heuristic.
17. Section 10: cite Kannan–Barton 2017 Section 3.2 as the precedent for
    Section 5; say that Lemma 4.1 uses standard geometric-measure-theory tools;
    say that Theorem 8.2(a) and (e) are the Lipschitz covering argument in box
    form.

## 11. What remains unchecked

- The sphere and ball sweeps (Tables 9.1 and 9.2) were not re-run with
  independent branch-and-bound code. Only two lower-bound entries were
  recomputed, and the quoted exponents were checked against the author's logs.
- No computation measured `N_opt` in 2D or 3D. The guillotine-DP estimates the
  reviewer considered were not run.
- Open problems 1–8 and the conjecture in Open problem 2 were not reviewed.
- Literature:
  - the full texts of Munos (2011), Bachoc et al. (2021) and Hansen–Jaumard–Lu
    (the earlier review's reading is relied on);
  - the interval-analysis box-count literature (Ratschek–Rokne, Csendes–Ratz,
    Kearfott 1996, Schöbel–Scholz);
  - the geometric-measure-theory and manifold-learning literature, for earlier
    per-box integral bounds of the Lemma 4.1 type;
  - work after 2021 extending Bachoc et al. to smooth or constrained settings,
    where the arXiv queries were cut short by rate limits;
  - Kannan–Barton (2018, JOGO 71) itself, as opposed to the local thesis text.
- The general fix to Lemma 5.5 by curves (for nonlinear exact constraints) is
  sketched here, not written out.
