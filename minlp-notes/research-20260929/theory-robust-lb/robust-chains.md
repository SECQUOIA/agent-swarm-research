# Split-robust lower bounds on uniform chains

Date: 2026-09-30. Continuation of the workstream "theory-robust-lb" of the
September 29 program. Status: **revised after review rounds 1 to 5**
(changes listed in Section 10). The round-5 changes (wording only) were
confirmed by `../reviews/round4-nits-confirm.md` (verdict verified,
optional nits only; root update 2026-10-01). Proofs are complete unless a step is marked
"sketch". Computations are floating point (HiGHS through scipy, numpy,
Clarabel and SCS through cvxpy) unless stated otherwise; apart from the two
lower bounds of Lemma A.4 below, none is interval-certified. Exact checks:
the symbolic identities of Propositions C.1 and C.5 and of Lemma A.4, and
the positive-definiteness of the unbounded direction in Section 4.6, were
checked with sympy (exact polynomial arithmetic); the finite facts about
WALL used in Lemma A.4 (root counts of rational polynomials, and two lower
bounds on rational grids with a Lipschitz bound) were checked in exact
rational arithmetic, and the two lower bounds again with interval
arithmetic (mpmath). The fooling value of Proposition A.3 was evaluated in
closed form with 30-digit arithmetic (mpmath). Lean was not used: the key
finite facts are polynomial identities and rational computations that
sympy and Python fractions already check exactly. Scripts and logs are in
[`chains/`](chains/) (Section 9).

Cited notes:

- [R] robust-lower-bound note, [`robust-lower-bound.md`](robust-lower-bound.md)
  (Lemmas 1.1–1.3, Proposition 2.1, Theorem 4.2, Section 4.3);
- [F] face-exact note, [`../theory-face-exact/face-exact-exponential.md`](../theory-face-exact/face-exact-exponential.md)
  (Theorems 1 and 2, Section 9.2);
- [K] consistency note, [`../theory-consistency/consistency-relaxations.md`](../theory-consistency/consistency-relaxations.md)
  (Theorem 1.1, Proposition 1.3, Theorem 2.1, Proposition 3.2).

## Summary

**Question.** [R] proves an exponential lower bound on single-tree spatial
branch-and-bound that holds for every per-node split in natural classes. Its
family is built from nearly independent three-variable gadgets joined by
links weaker than `1.4e-3`, and its proved bases are 1.003 (analytic) and
1.05 (computed) per variable. [R] has no split-robust bound for uniform
chains such as `sum_i u(x_i) + b sum_i x_i x_{i+1}`. Is there one, ideally
with a meaningful base? Or is there none?

**Answer, in three parts.**

1. **Uniform chains with symmetric couplings: under a nondegeneracy
   hypothesis (H1), no lower bound that grows with `n` exists (Section 2).
   Without (H1) this fails for the fixed balanced split (Section 2.5).**
   Take `f_n = sum_i u(x_i) + sum_i w(x_i, x_{i+1})` with
   `w(x, y) = w(y, x)`; the program's chains `w = b x y` are the main
   case.
   - *Bulk exactness (Proposition A.1, proved).* With the balanced split
     (half of each interior `u` in each of its two factors), every interior
     factor is the same symmetric pair function
     `phi(x, y) = (u(x) + u(y))/2 + w(x, y)`. Its minimum equals the ground
     energy per bond, because the alternating configuration `(a, c, a, c, ...)`
     built from a minimizer `(a, c)` of `phi` reaches it. Hence the root gap
     of this fixed split is at most `max(u(a), u(c)) - min u` for every `n`.
     If additionally `u` is minimized at the bulk point `t` (with
     `(a, c) = (t, t)`), the root is exact. [R, Proposition 2.1] is the case
     `t = 0`.
   - *Covers of size independent of `n` (Theorem A.2, proved).* Suppose
     `phi` has a unique, nondegenerate, diagonal minimizer `(t, t)` with
     quadratic growth (hypothesis (H1)). Then the fixed balanced split admits
     certificates whose size depends on `eps` but not on `n`: branch only on
     the first and last `k(eps)` variables. So, under (H1), no lower bound
     that grows with `n` holds for any class that contains the balanced
     split: the fixed balanced split itself, classes (a) and (a0), and `b_d`
     relative to the balanced base split. Not every class of [R] contains
     the balanced split. The fixed unsplit split does not, and `b_d`
     relative to another base split (such as the gadget base split of [R])
     contains it only if the two base splits differ by polynomials of degree
     at most `d`.
   - *Without (H1): a linear lower bound for the fixed balanced split
     (Proposition A.3, Section 2.5; example from the review).* On the chain
     WALL (`u = 1.022 t + 0.189 t^2 + 1.774 t^3 + 1.086 t^4`, `w = 0.962 x y`)
     the bulk alternates and, for even `n`, the optimum contains one domain
     wall whose position is free: there are `n/2` exactly degenerate global
     minimizers (global optimality proved for every even `n >= 4` by a
     class-(a0) split, Lemma A.4). Every cover for the fixed balanced split
     at `eps < 0.01134` has at least `n/2` boxes, for every even `n >= 4`.
     Classes (a) and (a0) are exact at the root of WALL for every `n`
     (Lemma A.4, proved with exact arithmetic for the finite facts), so
     this does not extend to them. Whether some symmetric chain without (H1)
     defeats class (a) is open.
   - *Numerics.* On a uniform chain designed to have a boundary-layer gap
     (the end variables sit in a second well of `u`), branch-and-bound
     needs:
     - with the balanced split and a spread-based branching rule:
       **10 leaves for every `n` from 5 to 16**, at `eps = 1e-4` and `1e-6`;
     - with widest-side bisection: linear growth (3 leaves per variable);
     - with the unsplit factorization of [F, Theorem 2]: a root gap that
       grows by 0.125 per variable, and growing trees.

     On WALL with the fixed balanced split, the counts for even `n` grow
     linearly (`n - 1` leaves with the spread rule, 4 to 22 with bisection
     for `n = 4..16`); odd `n` and class (a) need one leaf.

   So, under (H1), the exponential bound of [F, Theorem 2] is a property of
   the unsplit factorization. The mechanism is classical in Aubry–Mather
   theory: a split is exact in the bulk when the split class contains a
   *sub-action* of the bond function, and for symmetric bonds the constant
   function is one (Section 6).

2. **Pinned windows give the product structure on any path (Section 3,
   proved).** Fix every `(k+1)`-th variable at its value in `x*`. The
   S-consistent families of the windows between the fixed variables then
   combine into an S-consistent family of the chain (Lemma B.1). This turns
   [R, Theorem 4.2] into a product bound over windows. The weak links are
   no longer needed, and any product reference measure is allowed
   (Theorem B.2).

3. **Translation-invariant chains with a chiral coupling: a split-robust
   exponential bound without gadgets or weak links (Section 4).** The
   chiral chain is

   ```
   f_n(x) = sum_i a x_i^2 + b sum_i x_i x_{i+1} + (g/2) sum_i x_i x_{i+1} (x_{i+1} - x_i),   a = b + ev,
   ```

   on `[-1,1]^n`, with `0 < ev < g <= b/2`. Here `ev` sets the flatness of
   the valley (smallest Hessian eigenvalue at least `2 ev`) and `g` the
   chirality.
   - *Minimizer (Proposition C.1, proved; identity checked by sympy).* The
     cubic split `h(t) = -(g/2) t^3` makes every factor nonnegative. So
     `f_n >= (ev/2)|x|^2`, `x* = 0` is the unique, nondegenerate, interior
     minimizer for every `n`, and class `b_3` is exact at the root.
   - *Gap (Proposition C.2, proved).* Class (a), here
     `span{1, t, t^2, u} = P_2`, and the fixed balanced split have a root
     gap of at least `(n-1)(g - ev)^2/(4g) - a q`, where `q = (g - ev)/(2g)`,
     by an explicit two-point fooling family. The grid LP finds the same
     per-bond value, so this family is optimal on the grid.
   - *Lower bound (Theorem C.3, proved).* Every single-tree run with
     per-factor envelopes and any per-node class-(a) split, even one chosen
     with knowledge of `x*`, needs exponentially many leaves. At
     `(b, g, ev) = (0.6, 0.3, 0.05)` the bases per variable are:
     - fully analytic (no computation): 1.0009 with windows of length 7,
       rising with the window length to 1.006 (`k = 20`) and 1.0087
       (`k = 100`); the supremum over `k` is `exp(g_inf/5.6) = 1.0093`, not
       attained;
     - 1.0033 with the LP-computed window gap and analytic transport;
     - 1.023 computer-evaluated (LP window gaps on cores);
     - at most 1.058 for the method itself with windows of length 7 and
       Lebesgue reference measure (ceiling from exact corner boxes;
       heuristically about 1.16 for long windows).

     Observed growth is about 1.75 per variable (spread rule) and 2.3
     (bisection) up to `n = 12`. With the chirality `(g/2)(x y^{2m} - x^{2m} y)`
     the same construction defeats `P_{2m}` (positive gap for small `ev`)
     and is closed by `P_{2m+1}` (Proposition C.4). As for the gadget
     family, the family must depend on the degree.
   - *Scope (Proposition C.5, proved; identity from the review).* Theorem
     C.3 concerns factorable relaxations whose shared univariate lifts are
     `x_i` and `x_i^2` (class (a); per-factor envelopes, McCormick, RLT,
     `2x2` PSD cuts on shared `x_i^2` auxiliaries). It does not concern
     moment-SOS solvers. The minimal-order sparse moment-SOS relaxation
     (order 2, pair cliques) is exact at the root of the chiral chain
     *under a condition on the box constraints*: each box constraint is
     localized in every clique that contains its variable (or in one
     clique, in the orientation of the certificate), or the ball constraint
     `2 - x_i^2 - x_{i+1}^2 >= 0` is added in every clique. Without such a
     condition it can fail (Section 4.6): with each linear box constraint
     attached to one clique in the opposite orientation and no ball
     constraint, the root gap is 0.0553 at `n = 5` and 0.2072 at `n = 8`;
     with univariate multipliers for linear box constraints (the basic form
     of Waki et al.) the relaxation is unbounded (proved); with moment
     bounds added its gap at `n = 5` is 0.0628 for `|y_alpha| <= 1` and
     0.699 for the bounds Waki et al. use after scaling the variables to
     `[0, 1]`. A ball with a loose radius (`2M^2 - x_i^2 - x_{i+1}^2`,
     `M = 2` or `10`) leaves a gap too. All SDP values are floating point.

**Meaningful base: not achieved (Section 5).** On both families the
volume-type counting with Lebesgue reference measure (tilted volume with
windows) is limited by corner boxes far from `x*`. It yields at most about
`exp(c · gap/curvature)` per variable, and split-robust gaps are a few
percent of the curvature scale here. Only Lebesgue measure was computed;
Theorem B.2 allows other product measures, which were not optimized. The
computed bases stay near 1.02–1.03, as in [R]. Two attempts to bracket the
true minimal certificate size from above failed: "sparse-narrow" covers
were certified only for one size (`n = 8`, intervals of width 0.1, worst
box at the edge of the tolerance); if that width sufficed for all `n`, they
would give about 2.7 per variable, worse than branch-and-bound. The true
growth of minimal certificates for the chiral chain is not known.

**For solvers.**

- On uniform chains with symmetric couplings that satisfy (H1), split each
  unary term evenly between its two factors. Then branch where the
  relaxation's factor measures spread (in practice, near the ends). Growth
  with `n` there comes from the factorization (the unsplit one) or from the
  branching rule (bisection grew linearly in the example), not from the
  relaxation class. Without (H1) a fixed even split can fail: on WALL it
  needs at least `n/2` boxes for every even `n >= 4` (Proposition A.3),
  while letting the solver reweight `u` (class (a) or (a0)) closes the
  root for every `n` (Lemma A.4).
- Translation invariance alone does not make a chain easy for factorable
  relaxations. A chiral bond needs a sub-action outside the split class.
  Adding the monomial `t^3` to the class (one more lifted univariate
  variable per separator) closes the chiral chain at the root. Theorem C.3
  concerns factorable MINLP relaxations with shared `x_i` and `x_i^2`
  auxiliaries. Sparse moment-SOS relaxations of order 2 share `x_i^3` and
  `x_i^4`; they are exact at the root when each box constraint is
  localized in every clique that contains its variable (or in one clique,
  in the orientation of the certificate), or when a ball constraint
  `2 - x_i^2 - x_{i+1}^2 >= 0` is added per clique (Proposition C.5). How
  an implementation places the box constraints matters: one clique per
  linear box constraint in the opposite orientation leaves a root gap,
  and univariate multipliers for linear box constraints leave the
  relaxation unbounded, or with a gap once the
  moments are bounded (Section 4.6; gaps floating point).

**Novelty.** Prior work and novelty are discussed in Section 6. The
period-two argument and sub-actions are classical. What is new here, as far
as found:
- their use for node counts of spatial branch-and-bound;
- the pinning lemma;
- the chiral family.

The WALL example and the moment-SOS identity of Proposition C.5 come from
the review of the first version. The class-(a0) split of Lemma A.4 and the
moment-SOS variants with a gap (Section 4.6) come from the second review.
Added here in round 2: the exact-arithmetic proof of the factor minima in
Lemma A.4, the ball-constraint certificate of Proposition C.5(d), the
unboundedness proof for univariate multipliers and the dependence on the
ball radius. The gaps with Waki et al.'s scaled moment bounds and the
ball-radius runs up to `n = 32` come from the third review and were
reproduced here.

An unsuccessful search does not establish novelty.

## 1. Setting

The notation is that of [R, Section 1].

- A path objective is `f(x) = sum_{e=1}^{n-1} f_e(x_e, x_{e+1})` on a box
  `X0 = prod [L_i, U_i]`.
- A split class `S` assigns to each interior variable `i` a linear space
  `S_i` of univariate functions that contains the affine functions. Its
  splits are `f_e^r = f_e + r_{e+1}(x_{e+1}) - r_e(x_e)` with `r_i in S_i`.
- `LB_S(C)` is the per-factor envelope bound of the best split of the class
  for the box `C`. By [R, Lemma 1.2] it equals
  `min { sum_e ∫ f_e dnu_e : nu S-consistent on C }`. S-consistent means
  that the two factor measures containing `x_i` have marginals that agree on
  `S_i`.
- A finite family of boxes covering `X0` with `LB_S(C) >= f* - eps` for
  every member is an *S-cover* (certificate). `N_S(eps)` is its least size.
  By [R, Lemma 1.3], `#leaves + 2n #rounds >= N_S(eps)` for every
  single-tree run with per-node splits from `S`, any branching rule and
  same-relaxation bound tightening.

Two facts are used repeatedly.

- **Monotonicity in the class.** If `S ⊆ S'`, then `LB_S <= LB_{S'}`, so
  `N_{S'}(eps) <= N_S(eps)`. In particular, an upper bound on certificates
  for one *fixed* split (the class of affine shifts of that split, `P_1`) is
  an upper bound for every class that contains it.
- **Factor minima.** `LB_S(C) >= sum_e min_{C_e} f_e^r` for every `r in S`.
  With `r = 0` this is the sum of the factor minima of the base split.

Base splits.

- The *balanced split* of `sum_i u(x_i) + sum_e w(x_e, x_{e+1})` gives every
  interior factor `phi(x_e, x_{e+1})`, with
  `phi(x, y) = (u(x) + u(y))/2 + w(x, y)`. The first and last factors get in
  addition `u(x_1)/2` and `u(x_n)/2`.
- The *unsplit factorization* gives factor `e` the term `u(x_e) + w(x_e, x_{e+1})`,
  and the last factor `u(x_n)` as well. This is the factorization of
  [F, Theorem 2].
- For `u` in the class (classes (a), (a0)) the two base splits generate the
  same class.

## 2. Uniform chains with symmetric couplings

Throughout this section,

```
f_n(x) = sum_{i=1}^n u(x_i) + sum_{i=1}^{n-1} w(x_i, x_{i+1})   on [-1,1]^n,    w(x, y) = w(y, x),
```

with `u`, `w` continuous. The program's chains have `w = b x y`.

### 2.1 Bulk exactness

**Proposition A.1.** Let `m = min_{[-1,1]^2} phi`, attained at `(a, c)`.
For every `n >= 3`:

1. every interior factor of the balanced split has minimum `m`, and the sum
   of the factor minima is at least `(n-1) m + min u`;
2. `f*_n <= (n-1) m + max(u(a), u(c))`; in particular `f*_n / n -> m`;
3. the root gap of the balanced split (per-factor envelopes, or just the
   factor minima) is at most `max(u(a), u(c)) - min u`, whatever `n` is;
4. if `a = c = t` and `u(t) = min u`, the balanced split is exact at the
   root for every `n`, and `(t, ..., t)` is a global minimizer.

*Proof.*
1. Interior factors are `phi`. The end factors are `phi + u/2`, with
   minimum at least `m + min u/2`.
2. Evaluate `f_n` at `(a, c, a, c, ...)`. Every bond is `phi(a, c)` or
   `phi(c, a)`, and both equal `m` because `phi` is symmetric. The ends add
   `(u(x_1) + u(x_n))/2 <= max(u(a), u(c))`. Together with item 1,
   `(n-1) m + min u <= f*_n <= (n-1) m + max(u(a), u(c))`.
3. This follows from items 1 and 2.
4. Item 1 gives `LB >= (n-1) m + u(t) = f_n(t, ..., t) >= f*_n >= LB`. □

So the ground energy per bond equals the minimum of one symmetric bond.
Ground states can always be taken of period at most two. The balanced split
therefore loses nothing in the bulk, and the whole root gap sits at the two
ends.

*Contrast with the unsplit factorization.* Its factors are
`u(x) + w(x, y)` in the interior. Their minimum is below `m` in general,
and then the root gap grows linearly in `n`. This is the mechanism behind
the exponential bound of [F, Theorem 2]. In the example of Section 2.4 it
grows by 0.125 per variable, while the balanced gap stays at 0.0049.

### 2.2 Certificates of size independent of `n`

**Hypothesis (H1).** There are `t in (-1, 1)` and `kappa > 0` with
`phi(x, y) - m >= kappa ((x - t)^2 + (y - t)^2)` on `[-1,1]^2`. So the
minimizer `(t, t)` of `phi` is unique, diagonal and nondegenerate.
Moreover, `u`, `w` are `C^1`, and `phi(., t)` has a Lipschitz derivative.

Put `psi = phi - m >= 0` and define the constants:

- `M` with `psi(x, t) <= M (x - t)^2` on `[-1, 1]`. It exists because
  `psi(t, t) = 0` and `∂_x psi(t, t) = 0` (interior minimum);
- `L` a Euclidean Lipschitz constant on `[-1,1]^2` of every factor that
  occurs: `phi`, the end factors `phi + u(x)/2` and `phi + u(y)/2`, and,
  for `n = 2`, the single factor `phi + (u(x) + u(y))/2`;
- `Delta_0 = (u(t) - min u)/2`.

**Theorem A.2.** Assume (H1) and `Delta_0 > 0` (if `Delta_0 = 0`, the root
is exact by Proposition A.1(4)). Let `eps > 0`,
`k = 1 + ceil(4 M Delta_0/(kappa eps))` and `N = ceil(8 sqrt(2) (k-1) L/eps)`.
Then for every `n >= 2` there is a cover of `[-1,1]^n` by at most
`N^{2k}` boxes, each with `sum_e min_C F_e >= f*_n - eps`, where `F_e` are
the balanced-split factors. Hence

```
N_S(eps; n) <= N^{2k}     for every n >= 2 and every class S that contains the balanced split.
```

*Proof.* Subtract `(n-1) m`. Then
`g_n = f_n - (n-1) m = sum_e psi(x_e, x_{e+1}) + u(x_1)/2 + u(x_n)/2`. Write
`T_k(x_1, ..., x_k) = u(x_1)/2 + sum_{e<k} psi(x_e, x_{e+1})` for the cost
of a left end block and `sigma_k = min T_k`. The right end block is the same
function read backwards, because `psi` is symmetric.

1. *Upper bound on `g*_n` for `n >= 2k`.* Let `x` minimize `T_k`.
   - By (H1),
     `kappa sum_{e<k} (x_e - t)^2 <= T_k(x) - u(x_1)/2 <= sigma_k - min u/2 <= Delta_0`,
     since `sigma_k <= T_k(t, ..., t) = u(t)/2`.
   - So some `j <= k - 1` has `(x_j - t)^2 <= Delta_0/(kappa (k-1))`.
   - Glue `x_1, ..., x_j`, then `t` repeated, then the mirror image
     `x_j, ..., x_1` (this needs `n >= 2j + 2`, implied by `n >= 2k`).
   - The bonds `psi(t, t)` vanish, and `T_j(x) <= T_k(x) = sigma_k`
     because `psi >= 0`. So
     `g*_n <= 2 sigma_k + 2 M Delta_0/(kappa (k-1)) <= 2 sigma_k + eps/2`.
2. *Cover for `n >= 2k`.* Partition `[-1,1]^k` into `N^k` cubes of side
   `h = 2/N`.
   - Use the boxes `C = C_L × [-1,1]^{n-2k} × C_R`, with `C_L` from this
     grid and `C_R` from its mirror image.
   - Each middle factor is `psi >= 0`. For `z in C_L`, each left factor
     satisfies `min_{C_e × C_{e+1}} F_e >= F_e(z_e, z_{e+1}) - sqrt(2) L h`.
   - So the left block contributes at least
     `sigma_k - sqrt(2)(k-1) L h >= sigma_k - eps/4`, and likewise the
     right block.
   - Hence `sum_e min_C F_e >= 2 sigma_k - eps/2 >= g*_n - eps`. There are
     `N^{2k}` boxes.
3. *Cover for `n < 2k`.* Use the uniform grid on all `n` coordinates. Each
   box has `sum_e min F_e >= g*_n - sqrt(2)(n-1) L h >= g*_n - eps`, and
   there are `N^n <= N^{2k}` boxes. Every factor here is `phi`, an end
   factor, or (for `n = 2`) the single factor, so `L` applies to each.

The last claim follows from monotonicity in the class (Section 1). □

The bound is astronomically large: `log N(eps) = O(eps^{-1} log(1/eps))`.
Its point is that it does not depend on `n`. Under (H1) the linearized bulk
recursion is hyperbolic, because `A > |B|` for the Hessian
`[[A, B], [B, A]]` of `psi` at `(t, t)`. Optimal boundary layers should then
approach `t` geometrically, so `k = O(log(1/eps))` would suffice and the
size would be quasi-polynomial in `1/eps`. This is a sketch: the local
stable-manifold estimate is standard, but it is not written out here. In
the example of Section 2.4, `|x*_i - t|` falls from 0.51 to 0.05, 0.005
and 0.0005 at `i = 1, 2, 3, 4`.

**Remarks.**

- *Ends.* The proof uses only the bulk. Chains whose two end unaries differ
  from `u` are covered as well: replace `u(x_1)/2` by the end term
  `u_1(x_1) - u(x_1)/2` and redefine `Delta_0` with it.
- *Alternating bulk.* If `phi` is minimized off the diagonal at
  `(a, c)`, `a != c`, the bulk ground state alternates. For even `u` the
  substitution `x_i -> (-1)^i x_i` changes `w = b x y` into `-b x y` and
  makes the ground state constant. Then (H1) may hold for the new chain
  (the balanced split commutes with the substitution).
  - In general, the same proof works when the phases preferred by the two
    ends are compatible with the parity of `n` (sketch).
  - Otherwise the frustration must sit somewhere, and the argument does not
    apply. Two cases were observed (Section 2.5). It may sit at a chain
    end: for `u = t^2 + 1.5 t`, `b = 1.2` and even `n = 6..12`, the grid-DP
    minimizer and its mirror image each have the defect at one end, and
    configurations with both ends in the `-1` phase are worse by at least
    0.149 (floating point). Or the optimum may contain a domain wall whose
    position is free: on WALL there are `n/2` exactly degenerate global
    minimizers for every even `n >= 4` (Lemma A.4), and the fixed balanced
    split then needs at least `n/2` boxes (Proposition A.3). (The first
    version said that the second case always occurs; the first example
    shows that it does not.)
- *What a solver must do.* The cover in the proof branches only on the
  first and last `k` variables. A rule that branches where the factor
  measures of the relaxation spread finds such covers in the example
  (Section 2.4). Widest-side bisection does not; it also branches the bulk.

### 2.3 Why (H1) matters

The balanced split is exact in the bulk because the constant function is a
sub-action of the symmetric bond `phi`: `phi(x, y) + 0 - 0 >= m` everywhere
(Section 6). What (H1) adds is a margin: away from `(t, t)` every bond costs
at least `kappa` times the squared distance. This margin is what makes long
boundary layers impossible and lets the middle factors be bounded by `0`.
Some such condition is needed: on WALL (Section 2.5), where the bulk
minimizer is off the diagonal and a domain wall can move freely, the fixed
balanced split has no cover of size independent of `n`. Every cover at
`eps < 0.01134` has at least `n/2` boxes for every even `n >= 4`
(Proposition A.3; the wall configurations are global minimizers by
Lemma A.4, so this holds for all such `n`, not only for the sizes
computed).

### 2.4 Numerical check (`chains/uniform_design.py`, `run_uniform.py`, `roots_uniform.py`)

PROGRAM-like uniform chains are easy. For `u = t^2 - kappa t^4 + c t` with
`(kappa, c, b)` in `{(0.1, 0, 0.8), (0.1, ±0.3, 0.8), (0.4, 0.3, 0.5), (0.6, 0.2, ±0.4)}`
and `n <= 12`:

- the balanced split is exact at the root to `1e-9`, even when `x*` has
  boundary layers (for `(0.6, 0.2, -0.4)` the minimizer is the corner
  `(-1, ..., -1)` for `n >= 3`, so that set is not interior);
- class (a) is also exact at the root to `1e-9`, with one exception: at
  `(0.1, -0.3, 0.8)`, `n = 12`, its column generation did not close and
  brackets the gap only in `[-1.1e-6, 2.0e-4]`;
- source: `logs/explore_uniform.log`.

A random search over 1,600 quartic `u` found no chain satisfying (H1) with
a balanced root gap above `5e-3` (`logs/search_uniform_*.log`). A scratch
rerun, not kept, showed that most draws fail (H1) or have a boundary
minimizer (5 of 300 passed the filter).

**The design chain UD.** To see the theorem at work, the example needs end
variables that sit in a nonconvex region. Take `b = 0.6` and a `C^1`
piecewise quadratic `u`:

```
u(x) = 0.168 - 1.44 x + 3 x^2        on [-1, 0.3],
       -0.237 + 1.26 x - 1.5 x^2     on [0.3, 0.6],
       1.023 - 2.94 x + 2 x^2        on [0.6, 1].
```

- The bulk point is `t = 0.2`, with `u(t) = 0` and `u'(t) = -2 b t`.
- A second, deeper well lies at `0.735`, with `u = -0.057`.
- `phi` has its unique minimum `0.024` at `(0.2, 0.2)`. The grid estimate of
  `kappa` is 0.061, so (H1) holds.
- The end variables sit in the second well. For `n = 8`,
  `x* = (0.713, 0.148, 0.205, 0.200, 0.200, 0.205, 0.148, 0.713)`.
- The smallest Hessian eigenvalue of `f_8` at `x*` is 3.82, so `x*` is
  nondegenerate.
- On the DP grid the best configuration with `x_1 <= 0.45` is worse by only
  0.0017 (`logs/checks_note.log`).

Root gaps (`logs/roots_uniform.log`; column-generation brackets, both ends
agree to the digits shown):

| n | 3 | 4 | 5 | 6 | 8 | 10 | 12 | 16 |
|---|---|---|---|---|---|---|---|---|
| balanced split | 0 | 0.0062 | 0.0047 | 0.0049 | 0.0049 | 0.0049 | 0.0049 | 0.0049 |
| unsplit factorization | 0.171 | 0.288 | 0.421 | 0.542 | 0.792 | 1.042 | 1.292 | 1.791 |
| class (a) | 0 | 3.6e-4 | 6.1e-4 | ≤1e-6 | ≤1e-6 | ≤1e-6 | ≤1e-5 | ≤5e-6 |

Leaves of branch-and-bound. Every pruned box has a dual bound and every
split box a fooling family, as in [R, Section 6.1]. Rules:

- `bisect` is widest-side bisection;
- `spread` branches on the variable whose marginals in the node's fooling
  family have the largest variance.

Logs: `logs/bb_uniform.log`, `logs/bb_uniform_unsplit.log`. Counts at
`eps = 1e-4`; the balanced-split rows are the same at `1e-6`.

| relaxation, rule | n = 3 | 4 | 5 | 6 | 7 | 8 | 10 | 12 | 14 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|
| balanced split, spread | 1 | 11 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| balanced split, bisect | 1 | 12 | 14 | 17 | 20 | 23 | 29 | 35 | 41 | 47 |
| unsplit, spread | 8 | 17 | 27 | 40 | 55 | 79 | – | – | – | – |
| unsplit, bisect | 15 | 42 | 47 | 68 | 102 | 144 | – | – | – | – |
| class (a), spread, `eps = 1e-6` | 1 | 5 | 5 | 1 | 6 | 2 | 7 | 8 | 19 | 19 |

- With the spread rule, the balanced split needs the same 10 leaves for
  every `n >= 5`, as Theorem A.2 predicts.
- Bisection grows linearly, by 3 leaves per added variable, at both
  tolerances.
- The unsplit factorization grows by about 1.57–1.58 per variable on
  average over `n = 3..8` (`(79/8)^{1/5}` with the spread rule,
  `(144/15)^{1/5}` with bisection); the last step, `n = 7 -> 8`, is
  1.41–1.44. Its root gap grows linearly.
- Class (a) closes most of the end gap at the root. Its counts at
  `eps = 1e-6` are small but not monotone in `n` (its root gap is between
  `1e-6` and `1e-5` there); with bisection they reach 27 at `n = 16`.

### 2.5 Without (H1): end defects and free domain walls (`chains/wall_check.py`, `chains/revision2_chains.py`)

This section was added after the first review. The chain WALL and the
claim of Proposition A.3 were supplied by the reviewer; everything below was
recomputed here. Lemma A.4 was added after the second review.

**The chain WALL.**

```
u(t) = 1.022 t + 0.189 t^2 + 1.774 t^3 + 1.086 t^4,    b = 0.962,    f_n = sum_i u(x_i) + b sum_i x_i x_{i+1}   on [-1,1]^n.
```

Facts (`logs/wall_basic.log`, floating point, unless marked "exact"; the
exact versions are in `logs/revision2_wall.log`):

- `u' > 1 > b` on `[-1, 1]` (exact, Lemma A.4(1); the minimum of `u'` is
  1.0151; the first version used a grid of 400,001 points). So `u` is
  increasing, and `min u = u(-1) = -1.521`.
- Let `c = 0.33772319890448544...` be the unique root in `[-1, 1]` of
  `u'(c) = 2b` (exact root count, Lemma A.4(1)).
- `phi` attains its minimum `m = phi(-1, c) = -0.8608039` exactly at
  `(-1, c)` and `(c, -1)` (proved in Lemma A.4(2); a grid of `2001^2`
  points agrees). The best diagonal value is larger by 0.291, and
  `phi(-1, -1) - m = 0.302`. So (H1) fails, and the bulk ground state
  alternates between `-1` and `c`.
- *Odd `n`.* The alternating configuration `(-1, c, -1, ..., c, -1)` has
  value `(n-1) m + u(-1)`, which is the lower bound of Proposition A.1(1).
  So it is a global minimizer, and the balanced split is exact at the root
  (proved; Lemma A.4(3)).
- *Even `n`.* Both ends prefer `-1`, which is incompatible with
  alternation. For `j = 1, ..., n/2` let `x^(j)` be the configuration with
  `x^(j)_i = c` if `i` is even and `i < 2j`, or `i` is odd and `i > 2j`, and
  `x^(j)_i = -1` otherwise. It alternates except for the bond
  `(2j-1, 2j)`, where both values are `-1` (the wall). Every `x^(j)` has
  `n - 2` bonds of value `m`, one bond `phi(-1, -1)` and both ends at `-1`,
  so `f_n(x^(j)) = (n-2) m + phi(-1, -1) + u(-1)` for every `j`. The `n/2`
  configurations are exactly degenerate.
- *Global optimality.* Proved for every even `n >= 4` by Lemma A.4(4)
  below. Floating-point checks that preceded the proof: for `n = 2..16`,
  grid DP (2001 points) with L-BFGS-B polishing returns this value
  (difference at most `4e-15`), and the class-(a) root bound
  (column-generation lower bound) agrees with it to `5e-7` for
  `n = 3..16`.

**Lemma A.4 (WALL: exact factor minima and a class-(a0) split).** The
split of item 4 was supplied by the second review, which checked
`min H = H(-1, c)` by exact real-root isolation and 40-digit evaluation.
The proofs of items 1 and 2 below, with exact arithmetic for the finite
facts, were done here. Put `H(x, y) = u(x) + u(y) + b x y - b (x + y)`
(a function; not to be confused with the boxes `H_j` of
Proposition A.3).

1. `u' > 1 > b` on `[-1, 1]`, and `u'(t) = 2b` has exactly one root `c` in
   `[-1, 1]`. Hence `t -> u(t) - 2bt` has its unique minimizer on
   `[-1, 1]` at `c`.
2. `min phi = m = phi(-1, c)` on `[-1, 1]^2`, attained only at `(-1, c)`
   and `(c, -1)`. Likewise `min H = H(-1, c) = 2m + b`.
3. For odd `n >= 3`, the balanced split is exact at the root, and
   `(-1, c, -1, ..., c, -1)` is a global minimizer.
4. Let `n >= 4` be even. Take the split with shifts (relative to the
   balanced split) `r_i = b t - u(t)/2` for even `i` and
   `r_i = u(t)/2 - b t` for odd `i`, `2 <= i <= n - 1`. Its factors and
   their minima over `[-1, 1]^2` are:
   - first bond: `u(x_1) + b x_2 (x_1 + 1)`, minimum `u(-1)`;
   - last bond: `u(x_n) + b x_{n-1} (x_n + 1)`, minimum `u(-1)`;
   - odd bonds `e = 3, 5, ..., n - 3`: `b (x_e + 1)(x_{e+1} + 1) - b`,
     minimum `-b`;
   - even bonds `e = 2, 4, ..., n - 2`: `H(x_e, x_{e+1})`, minimum
     `2m + b`.

   The factor minima add up to `(n-2) m + phi(-1, -1) + u(-1)`, the value
   of the wall configurations. Hence every `x^(j)` is a global minimizer,
   and this split, which lies in class (a0) (and in `b_4`, because `u` is
   quartic), is exact at the root.

So classes (a) and (a0) are exact at the root of WALL for every `n` (for
`n = 2` there is a single factor, whose envelope is exact).

*Proof.*
1. `u' - 1 = (543/125) t^3 + (2661/500) t^2 + (189/500) t + 11/500` has no
   real root in `[-1, 1]` and is positive at `0`; `u' - 2b` has exactly one
   root in `[-1, 1]`, with `u'(-1) - 2b = -151/500 < 0 < 4571/500 = u'(1) - 2b`
   (sympy root counting on rational polynomials, exact). And `b = 0.962`.
2. *`phi`.* `∂_y (2 phi) = u'(y) + 2 b x > 1 + 2 b x >= 0` when
   `x >= -1/(2b)`. For such `x`,
   `2 phi(x, y) >= 2 phi(x, -1) = u(x) - 2bx + u(-1) >= u(c) - 2bc + u(-1) = 2m`,
   with equality only at `(c, -1)` (item 1). The case `y >= -1/(2b)` is
   symmetric. The rest, `[-1, -1/(2b))^2`, lies in `[-1, -1/2]^2`. There
   `|∂_x (2 phi)|, |∂_y (2 phi)| <= sum_i i |u_i| + 2b <= 13`, so an exact
   rational grid of step `1/200` gives `2 phi >= -1.17663 - 13/200 = -1.2416`,
   while `2m <= 2 phi(-1, 0.3377232) = -1.7216`.
   *`H`.* `∂_y H = u'(y) + b (x - 1) > 1 + b (x - 1) >= 0` when
   `x >= 1 - 1/b = -0.0395`. For such `x`,
   `H(x, y) >= H(x, -1) = u(x) - 2bx + u(-1) + b >= H(-1, c)`, with equality
   only at `(c, -1)`; the case `y >= 1 - 1/b` is symmetric. The rest lies
   in `[-1, 0]^2`, where the exact grid of step `1/200` gives
   `H >= -0.5590 - 13/200 = -0.6240 > H(-1, c) = -0.7596`. Finally
   `H(-1, c) = u(-1) + u(c) - 2bc + b = 2m + b`.
3. By Proposition A.1(1) and item 2, the factor minima of the balanced
   split add up to at least `(n-1) m + min u = (n-1) m + u(-1)`, the value
   of the alternating configuration.
4. The factors follow from `f_e^r = f_e + r_{e+1}(x_{e+1}) - r_e(x_e)`
   (sympy for `n = 4..30`; also by hand: each interior `u(x_i)` moves
   entirely into the even bond containing `x_i`, and `±b x_i` balances it).
   The shifts lie in `span{t, u}`, which is class (a0).
   - First bond: `x_1 + 1 >= 0`, so the minimum over `x_2` is at
     `x_2 = -1`, which leaves `u(x_1) - b (x_1 + 1)`; this is increasing
     because `u' > b`, so the minimum is `u(-1)`. The last bond is the
     mirror image.
   - Odd bonds: `(x + 1)(y + 1) >= 0`.
   - Even bonds: item 2.

   There are `n/2 - 1` even bonds and `n/2 - 2` odd bonds, so the minima
   add up to `2 u(-1) - b (n/2 - 2) + (n/2 - 1)(2m + b) = (n-2) m + 2 u(-1) + b`,
   and `phi(-1, -1) = u(-1) + b`. So `LB >= sum of the factor minima = f_n(x^(j)) >= f*_n >= LB`. □

Checks (`chains/revision2_chains.py wall` → `logs/revision2_wall.log`;
independent second route `chains/revision2_independent.py wall` →
`logs/revision2_independent_wall.log`):

- exact: the root counts and values of item 1; the split identity for
  `n = 4, 6, ..., 30` (factors built directly) and for `n = 4..14` (built
  from the shifts `r_i`); the sum of the minima against the wall value with
  `n` symbolic; the two rational grids of item 2;
- interval arithmetic (mpmath, outward rounding, `64 x 64` boxes): `H >= -0.6231`
  on `[-1, 1 - 1/b]^2` and `2 phi >= -1.2321` on `[-1, -1/(2b)]^2`;
- floating point: the critical points of `H` on `[-1, 1]^2` (corners, edge
  critical points, interior critical points from a resultant) have
  lowest value `H(-1, c)` at the mirror pair, and the next one is higher
  by 0.5756; a `4001^2` grid agrees. The review reported the same numbers
  from exact real-root isolation and 40-digit evaluation.

**Proposition A.3 (fixed balanced split on WALL).** Let `n >= 4` be even.
Let `S` be the fixed balanced split (`P_1` relative to the balanced base
split). Put `Delta_W = 0.01134327...` (value below). Then every S-cover at
tolerance `eps < Delta_W` has at least `n/2` boxes. So every single-tree
run with this fixed split has `#leaves + 2n #rounds >= n/2`
[R, Lemma 1.3]. (The first version assumed that the `x^(j)` are global
minimizers, checked in floating point for `n <= 16`; Lemma A.4 proves
this for every even `n >= 4`.)

*Proof.*
1. For `j < j'`, the configurations `x^(j)` and `x^(j')` differ exactly at
   the indices `i = 2j, ..., 2j'-1`. At each such index one of them is `-1`
   and the other is `c`.
2. Let a box `C` contain `x^(j)` and `x^(j')` with `j < j'`.
   - Then `C_i ⊇ [-1, c]` for `2j <= i <= 2j'-1`, and `C_i` contains the
     common value at the other indices.
   - `x^(j+1)` differs from `x^(j)` only at `2j` and `2j+1`, so `x^(j+1)` is
     in `C`.
   - Hence `C` contains the *adjacent-pair box* `H_j`, the smallest box
     containing `x^(j)` and `x^(j+1)`. It has `[-1, c]` at the coordinates
     `2j` and `2j+1` and the common point values elsewhere; in particular
     `x_{2j-1} = x_{2j+2} = x_1 = x_n = -1` on `H_j`.
3. On `H_j` every factor is constant except the three factors
   `phi(-1, y)`, `phi(y, z)` and `phi(z, -1)`, where
   `(y, z) = (x_{2j}, x_{2j+1}) in [-1, c]^2`. The end terms
   `u(x_1)/2` and `u(x_n)/2` are constants. Fix `s in (0, 1)` and
   `t in (-1, c]`, put `ybar = -s + (1-s) c` and `p = s (1 + c)/(1 + t)`
   (`p <= 1` exactly when `t >= s c - (1 - s)`), and take the family:
   - middle factor: `s δ_{(-1, c)} + (1 - s) δ_{(c, -1)}`;
   - left factor: the point mass at `y = ybar`;
   - right factor: `(1 - p) δ_{z = -1} + p δ_{z = t}`;
   - point masses at `x^(j)` on all other factors.

   The left factor's mean is the middle factor's `y`-mean. The right
   factor's mean is `p t - (1 - p) = s (1 + c) - 1 = s c - (1 - s)`, the
   middle factor's `z`-mean. So the family is mean-consistent, that is,
   S-consistent. Since `f* = const + phi(-1, -1) + 2m` and `phi` is
   symmetric, its value is `f* - Delta(s, t)` with

   ```
   Delta(s, t) = m + p phi(-1, -1) - phi(-1, ybar) - p phi(-1, t).
   ```

   At `s = 779/10000`, `t = 467/2000` (then `ybar = 0.23351`, `p = 0.08448`):
   `Delta = 0.011343271507206581694271604894` (closed form with `c` from
   the cubic to 40 digits, evaluated with 30-digit arithmetic;
   `logs/wall_family.log`). By [R, Lemma 1.2],
   `LB_S(H_j) <= f* - Delta_W` with `Delta_W` this value. (A first attempt
   here with `t = ybar` and `s = 31/400` gave 0.0113430; the optimum of the
   closed form over `(s, t)` is 0.01134327, at `(0.07789, 0.23352)`.)
4. `LB_S` is monotone under inclusion, so every box containing two of the
   `x^(j)` has `LB_S <= f* - Delta_W < f* - eps`. A member of an S-cover
   therefore contains at most one `x^(j)`. The cover contains all `n/2` of
   them. □

The gain comes from the left factor: at `ybar`, `phi(-1, ·)` lies 0.0105
below its chord between `-1` and `c` (`logs/wall_family.log`). This is
possible because `u` is not convex on `[-1, c]` (`u'' < 0` on about
`(-0.78, -0.04)`). Class (a0), which can move weight of `u` between the two
factors of a variable, closes this gap on `H_j` (checks below); the fixed
split cannot.

Checks (`logs/wall_family.log`, `logs/wall_classes.log`):

- The mean-consistent LP of the three factors on a grid of `[-1, c]^2`
  (401 points per axis) gives `Delta = 0.0113430`, a valid lower bound on
  the gap because grid families are feasible. The column-generation bound
  of the fixed split on `H_1` and `H_2` for `n = 6` gives `0.0113433` at
  both ends of its bracket. So the closed-form family is optimal up to
  about `1e-7`. (An 801-point grid LP was started and stopped after 11
  minutes on the loaded machine; it was not needed.)
- On the same boxes the class bounds of (a0), `b2`, `b3`, `b4` and (a)
  (all relative to the balanced base split) close the gap (at most
  `4e-7`). So the argument is specific to the fixed split.
- Classes (a) and (a0) are exact at the root for `n = 3..16` (brackets at
  most `5e-7`), in agreement with Lemma A.4, which proves this for every
  `n`.
- The root gap of the fixed balanced split is `0` for odd `n` and
  `0.0205 (n/2 - 1)` for even `n = 4..16` (0.0205 at `n = 4`, 0.1436 at
  `n = 16`). It cannot keep growing: by Proposition A.1(1) it is at most
  `f* - (n-1) m - u(-1) = phi(-1, -1) - m = 0.302` for every `n`. So the
  root gap stays bounded while the minimal cover grows linearly.

Leaves of branch-and-bound on WALL at `eps = 1e-4` (`logs/bb_wall.log`;
rules as in Section 2.4):

| relaxation, rule | n = 4 | 6 | 8 | 10 | 12 | 14 | 16 | odd `n = 3..15` |
|---|---|---|---|---|---|---|---|---|
| fixed balanced split, spread | 3 | 5 | 7 | 9 | 11 | 13 | 15 | 1 |
| fixed balanced split, bisect | 4 | 7 | 10 | 13 | 16 | 19 | 22 | 1 |
| class (a), spread and bisect | 1 | – | 1 | – | 1 | – | 1 | – |

The counts grow linearly, consistent with Proposition A.3. Neither the
proposition nor the counts show exponential growth.

**An end defect instead of a wall.** For `u = t^2 + 1.5 t` and `b = 1.2`
(`logs/wall_endfrust.log`, grid DP, floating point):

- `phi` has its minimum `-0.35125` at `(-1, 0.45)`, off the diagonal, so
  (H1) fails and the bulk alternates.
- For odd `n = 3..11` the minimizer is `(-1, 0.45, ..., 0.45, -1)`.
- For even `n = 6..12` the grid-DP minimizer is
  `(-0.3, -0.75, 0.3, -1, 0.45, -1, ..., 0.45, -1)`; its mirror image has
  the same value. The defect sits at one end.
- Configurations with both `x_1, x_n <= -0.9` (this includes every
  configuration whose two ends are in the `-1` phase, so that the defect
  lies inside the chain) are worse by 0.149 (`n = 6`) and 0.157
  (`n = 8..12`).
- For `n = 4` the minimizer is the symmetric configuration
  `(-0.605, -0.242, -0.242, -0.605)`.

Covers for this chain were not analysed.

## 3. Pinned windows

**Lemma B.1 (pinning).** Let `f = sum_e f_e` be a path objective and `S` a
split class. Let `C` be a box, `J` a set of indices no two of which are
adjacent, and `p_J in C_J`. Every factor then has at most one index in
`J`. (`J` may contain the end indices `1` and `n`. They lie in one factor
only, so they carry no consistency condition, and the proof below is
unchanged. The first version required `J` to be interior; Theorem C.3 uses
an end index when `k + 1` divides `n`.)

- Assign each factor to the window (maximal run of indices outside `J`)
  that contains its other index. So a window `W` owns its inner factors and
  the factors joining it to the pinned neighbours.
- Let `V_W(C_W; p)` be the minimum of the window's factor integrals over
  families in which:
  - inner factors carry measures on their boxes;
  - a factor `(j, i)` with `j in J` carries `delta_{p_j} ⊗ mu` with
    `mu in P(C_i)`;
  - the marginals of the two factors containing any index of `W` agree on
    `S`.

Then

```
LB_S(C) <= sum_W V_W(C_W; p_J).
```

*Proof.* Put the optimal window families together. At a pinned index both
factors have the marginal `delta_{p_j}`, so they agree on everything. At
window indices the families agree by construction. The value is the sum of
the window values. By [R, Lemma 1.2] the left side is the minimum over all
S-consistent families. □

**Theorem B.2 (tilted volume over pinned windows).** Let `x*` be a global
minimizer with `x*_J` in the interior of `X0_J`, and let `W_1, ..., W_G` be
the windows.

- Put `f_W(x_W; x*) = ` the window's part of `f` with the pinned values
  `x*_J`. Then `sum_W f_W(x*_W; x*) = f*`.
- Put `D_W(B) = V_W(B; x*_J) - f_W(x*_W; x*)` for boxes `B ⊆ X0_W`.
- For each window choose any probability measure `pi_W` on `X0_W`, and for
  `mu > 0` put `Phi_W(mu) = sup_B pi_W(B) exp(mu D_W(B))`.

Then every S-cover at tolerance `eps` satisfies

```
|P| >= exp(-mu eps) prod_W Phi_W(mu)^{-1}.
```

*Proof.*
1. Let `Y_delta = {x in X0 : |x_j - x*_j| <= delta for j in J}`. Give it
   the measure `pi_delta = (prod_W pi_W) ⊗ (uniform on the
   `delta`-intervals)`. The cover covers `Y_delta`, so
   `sum_{C in P} pi_delta(C) >= 1`.
2. If `pi_delta(C) > 0`, pick `p_j in C_j` within `delta` of `x*_j`.
3. `V_W(.; p)` depends on `p` only through the boundary factors, so it is
   Lipschitz in `p` with some constant `Lip_W`.
4. Lemma B.1 and `LB_S(C) >= f* - eps` give
   `sum_W D_W(C_W) >= -eps - delta sum_W Lip_W`.
5. As in [R, Theorem 4.2],
   `pi_delta(C) <= prod_W pi_W(C_W) <= exp(mu(eps + delta sum Lip_W)) prod_W pi_W(C_W) exp(mu D_W(C_W))`.
   Sum over `P`, use `Phi_W`, and let `delta -> 0`. □

**Remarks.**

- *What changes against [R, Theorem 4.2].* That theorem needs links weaker
  than `2 alpha = 1.4e-3`, so that `0` stays the minimizer and products of
  marginals cost little. Pinning needs no weak links: the windows are
  evaluated at the true `x*`, whatever the coupling. The price is one
  variable per window.
- *Window gaps.* The exponential bound needs `Phi_W(mu) < 1` for some
  `mu`. The full window box gives `exp(-mu gamma_W)`, where
  `gamma_W = -D_W(X0_W)` is the window's class gap with the boundary fixed
  at `x*`. So a positive window gap is necessary.
- *Symmetric uniform chains give nothing here.* Lemma B.1 gives
  `LB_S(X0) <= sum_W V_W(X0_W; x*_J)`, and each `V_W <= f_W(x*_W; x*)`
  (point masses at `x*`). So the window gaps add up to at most the root gap
  of the chain. By Proposition A.1 that root gap is bounded in `n` for
  symmetric couplings, and it is zero when `u(t) = min u`. So Theorem B.2
  cannot produce growth in `n` there, consistent with Theorem A.2.
- *Gap transport.* For `S = P_d`, the transport argument of
  [R, Section 4.3(a)] works window by window. Affine images of a
  `P_d`-consistent family are `P_d`-consistent. So
  `Phi_W(mu) <= exp(-mu gamma_W)` for `2 mu Lambda_j <= 1`, where
  `Lambda_j` bounds `|∂_j|` of the window factors containing `j`, summed
  over those factors.
- *Leftover windows.* Windows with `Phi_W(mu) <= 1` can be dropped from the
  product. This is how windows of a different length (for example a short
  last window) are handled in Theorem C.3.
- *Reference measures.* [R] used Lebesgue measure only. Theorem B.2 allows
  any product measure. Only Lebesgue measure was used here; other measures
  were not optimized (Section 5).

## 4. Chiral chains

### 4.1 The family

With `a = b + ev`, `0 < ev`, `0 < g`, define the bond

```
W(x, y) = (a/2)(x^2 + y^2) + b x y + (g/2)(x y^2 - x^2 y),
```

and the chain `f_n = sum_{e} W(x_e, x_{e+1}) + (a/2)(x_1^2 + x_n^2)`, that
is,

```
f_n(x) = a sum_i x_i^2 + b sum_i x_i x_{i+1} + (g/2) sum_i x_i x_{i+1} (x_{i+1} - x_i)    on [-1,1]^n.
```

- It is translation invariant, cubic, and of treewidth 1.
- The unary terms are convex. The nonconvexity comes from the chiral term
  `x y (y - x)`, which is antisymmetric. It is not a coboundary
  `h(y) - h(x)`, because its mixed second derivative `2(y - x)` is not zero.
- Here class (a) is `span{1, t, t^2, u} = P_2` because `u = a t^2`. It
  consists of the weights of the unary terms plus quadratic and linear
  shifts. `P_1` is the fixed balanced split with per-factor envelopes.
- Base splits may differ only by univariate functions [R, Lemma 1.1]. The
  chiral term stays in its bond, so these classes do not depend on the base
  split.

**Proposition C.1 (minimizer; exactness of `b_3`).** Let `0 < g <= b/2` and
`h(t) = -(g/2) t^3`.

1. `W(x, y) + h(x) - h(y) = (x + y)^2 (b/2 + (g/2)(y - x)) + (ev/2)(x^2 + y^2) >= (ev/2)(x^2 + y^2)`
   on `[-1,1]^2`.
2. `f_n(x) >= (ev/2)|x|^2` for every `n >= 2`. So `x* = 0` is the unique
   global minimizer and lies in the interior. The Hessian at `0` has
   eigenvalues `2a + 2b cos(k pi/(n+1)) > 2 ev`.
3. The fixed cubic split `r_i = h` makes every factor nonnegative and zero
   at `0`. So class `b_3` (and the single split `h`) is exact at the root
   for every `n`.

*Proof.*
1. This is a polynomial identity; sympy confirms it
   (`logs/chiral_certificate.log`). The bracket is nonnegative because
   `|y - x| <= 2` and `g <= b/2`.
2. Telescope:
   `f_n = sum_e [W + h(x_e) - h(x_{e+1})] + [(a/2) x_1^2 - h(x_1)] + [(a/2) x_n^2 + h(x_n)]`.
   - The end brackets are `(t^2/2)(a ± g t) >= ((a - g)/2) t^2 >= 0`.
   - Every variable lies in at least one bond, so item 1 gives the bound.
   - The Hessian at `0` is `2a I + b A`, with `A` the path adjacency
     matrix.
3. The factors of the split `h` are exactly these brackets. □

Grid DP with L-BFGS-B polishing gives `f*_n = 0` and `x* = 0` for
`n <= 40` at `(b, g, ev) = (0.6, 0.3, 0.05)`, `(0.6, 0.3, 0.1)` and
`(0.6, 0.45, 0.05)` (`logs/chiral_dp.log`). The last case has `g > b/2`,
outside the proposition. This suggests, without proving it, that the
threshold `g <= b/2` is sufficient but not sharp.

### 4.2 The gap of class (a)

**Proposition C.2.** Let `0 < ev < g` and `q = (g - ev)/(2g)`. Let `nu` be
the law on `[-1,1]^2` with mass `q/(1+q)` at `(-1, 1)` and `1/(1+q)` at
`(q, -q)`. Use `nu` for every factor.

- The family is `P_2`-consistent. The `x`-marginal is the law of a
  variable `p` and the `y`-marginal is the law of `-p`, where `E p = 0` and
  the second moments are equal.
- Its value is `-(n-1)(g - ev)^2/(4g) + a q`.

Hence, for every `n`, the root gaps of class (a) and of the fixed balanced
split are at least

```
(n-1) g_inf - a q,      g_inf = (g - ev)^2/(4g).
```

*Proof.* On the antiferromagnetic line, `W(p, -p) = ev p^2 + g p^3`. So
`E W = [q/(1+q)](ev - g) + [1/(1+q)](ev q^2 + g q^3) = q(g q + ev - g)`,
which is minimized at `q = (g - ev)/(2g)` with value `-(g - ev)^2/(4g)`.
The end terms add `(a/2)(E x_1^2 + E x_n^2) = a E p^2 = a q`. □

The mechanism has two parts.

- A `P_2`-consistent family may give `x_i` one law in factor `i - 1` and
  its mirror image in factor `i`, as long as the mean is `0`. The cubic
  chiral term then contributes `g E p^3 < 0` in every bond.
- A true configuration cannot do this. Around any closed loop the chiral
  terms are paid back, and Proposition C.1 is the bookkeeping.

**Numbers** (`logs/chiral_bulk.log`, `logs/chiral_roots_ev05.log`).

- *Per-bond LP.* The translation-invariant per-bond LP on a 201 × 201 grid
  ("bond measures whose two marginals agree on `S`") gives:
  - `P_1`, `P_2`: 0.05208 at `ev = 0.05` and 0.03333 at `ev = 0.1`
    (`g = 0.3`). These are the closed forms `5/96` and `1/30`, attained by
    the two-point family above.
  - `P_3`, `P_4`, and equal marginals: `0`.
- *Root gaps* at `(0.6, 0.3, 0.05)`; column generation, both ends of the
  bracket agree:

| n | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 12 |
|---|---|---|---|---|---|---|---|---|---|
| `P_1` (balanced split) | 0 | 0.0756 | 0.1122 | 0.1797 | 0.2205 | 0.2839 | 0.3270 | 0.3881 | 0.4922 |
| `P_2` (class (a)) | 0 | 0.0115 | 0.0503 | 0.0976 | 0.1477 | 0.1990 | 0.2508 | 0.3027 | 0.4068 |
| `P_3` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

From `n = 6` on, the `P_2` gap grows by 0.050–0.052 per added variable,
approaching `g_inf = 0.0521`.

### 4.3 Exponential lower bound

**Theorem C.3.** Let `0 < ev < g <= b/2`. Consider any single-tree run as
in [R, Lemma 1.3], with per-factor envelopes (or any weaker per-factor
relaxation) and, at each node, any split of class (a), chosen per node and
possibly with knowledge of `x* = 0`. Let `k >= 1`, and pin at `0` the
variables with indices `k+1, 2(k+1), ...` that are at most `n`. This gives
`G = floor((n+1)/(k+1))` windows of length `k`, and one leftover window of
length `r = n - G(k+1)` when `1 <= r <= k - 1`. (If `k + 1` divides `n`, the
last pinned index is the end index `n`; Lemma B.1 allows this.) Then:

1. (analytic) Let `Lambda = 2a + 2b + g`. If `(k-1) g_inf > a q`, then
   `#leaves + 2n #rounds >= exp(-mu eps) exp(mu ((k-1) g_inf - a q))^G` with
   `mu = 1/(2 Lambda)`. This is exponential in `n`, with base
   `exp(((k-1) g_inf - a q)/(2 Lambda (k+1)))` per variable.
2. (values) At `(b, g, ev) = (0.6, 0.3, 0.05)` and `k = 7`:
   - `Lambda = 2.8`, and item 1 gives **1.0009 per variable** (fully
     analytic; longer windows give more, see below);
   - with the LP-computed window gap `gamma_7 = 0.1477` (floating point)
     instead of the bound of Proposition C.2, transport gives
     `exp(gamma_7/(2 · 2.8))` per window, about **1.0033 per variable**;
   - the core/point-mass evaluation of [R, Section 4.3(b)] gives
     `Phi = 0.8314` at `mu = 2.112`, about **1.023 per variable**, so
     `#leaves + 2n #rounds >= exp(-2.112 eps) 1.2028^G`.

*Proof.*
1. By Proposition C.1, `x* = 0`. A window with its two neighbours fixed at
   `0` is exactly the `k`-chain, because `W(0, y) = (a/2) y^2` and
   `W(x, 0) = (a/2) x^2`. So `f_W(x*) = 0` and `D_W = LB` of the `k`-chain.
   The same holds for a window at the end of the chain, whose outer
   neighbour does not exist: the end term `(a/2) x^2` of the chain plays the
   role of `W(0, x)`.
2. Proposition C.2 applied to the `k`-chain gives
   `gamma_W >= (k-1) g_inf - a q`.
3. `P_2` is invariant under affine maps, so gap transport applies (remark
   after Theorem B.2). The constants `Lambda_j`:
   - `d_x W = (a - g y) x + y (b + (g/2) y)`. For `y in [-1, 1]`, `a - g y > 0`
     and `b + (g/2) y > 0` (because `g <= b/2 < a`), so
     `max_x |d_x W| = a - g y + |y| (b + (g/2) y)`. This is increasing in
     `y` on `[0, 1]` and decreasing on `[-1, 0]`, with values `a + b - g/2`
     at `y = 1` and `a + b + g/2` at `y = -1`. So
     `max_{[-1,1]^2} |d_x W| = a + b + g/2`.
   - `d_y W = (a + g x) y + x (b - (g/2) x)`. The same argument gives
     `max |d_y W| = a + b + g/2`, attained at `x = 1`.
   - A window variable lies in two window factors. An interior one has
     `Lambda_j <= 2a + 2b + g`. A window end lies in one bond and in the
     factor `(a/2) x^2` (pinned neighbour or chain end), so
     `Lambda_j <= 2a + b + g/2`. Hence `Lambda_j <= Lambda = 2a + 2b + g`.
     (The first version used the cruder `2a + 2b + 3g`.)
4. *Leftover window.* For item 1, transport gives
   `Phi_r(mu) <= exp(-mu gamma_r) <= 1`, because `gamma_r >= 0` (point
   masses at `x*` are feasible). Theorem B.2 with Lebesgue measure,
   dropping the leftover factor, gives item 1.
5. Item 2 uses the same theorem with the LP fooling value for
   `gamma_7(theta)` on the cores `K_theta = [-theta, theta]^7`
   (`theta = 0.2, 0.25, ..., 1`). Boxes not containing `K_0.2` are bounded
   by point masses through the separable bound
   `f_k(p) <= sum_j c_j p_j^2`, with `c_j = a + b + g` inside and
   `a + (b+g)/2` at the ends (`c = a` when `k = 1`). That bound uses
   `|x y|(|x| + |y|) <= x^2 + y^2` on `[-1,1]^2`.
6. *Leftover window in item 2.* At `mu = 2.112` transport does not apply
   (`2 mu Lambda > 1`), so the leftover window needs its own bound. For a box
   `B` of the `r`-window let `p` be its point nearest to `0`. Then
   `D(B) <= f_r(p) <= sum_j c_j p_j^2`, and coordinate by coordinate
   `(|B_j|/2) exp(mu c_j p_j^2) <= 1` if `0 in B_j`, and
   `<= sup_{0 < d <= 1} ((1-d)/2) exp(mu c_j d^2)` otherwise (then
   `|B_j| <= 1 - |p_j|`). So
   `Phi_r(mu) <= prod_j max(1, sup_d ((1-d)/2) exp(mu c_j d^2))`. At
   `mu = 2.112` the suprema are `0.5` (the limit `d -> 0`) for `c = a` and
   `c = a + (b+g)/2`, and `0.8138` for `c = a + b + g` (grid of `2·10^5` points;
   `logs/revision1_leftover.log`). So `Phi_r(2.112) <= 1` for every `r`,
   and the leftover factor can be dropped. (The first version omitted this
   step. The review checked `Phi_r(2.13) <= 1` for `r <= 6` numerically; the
   product bound above covers every `r` and every `mu < 2.3085`.) □

The constants of item 2 are floating point. The fooling values come from LP
families whose consistency residuals are at the LP tolerance; the maxima
over `d` in the point-mass bound are grid maxima. In the binding
configuration the largest term is the core step `0.75 -> 0.8` (0.8314). The
next largest are the core steps `0.7 -> 0.75` and `0.8 -> 0.85` (0.8284
each), `0.65 -> 0.7` (0.8201) and `0.85 -> 0.9` (0.8190); the point-mass
term is 0.8138 (`logs/checks_note.log`). So the base is limited by how fast
the window gap falls on smaller cores: `gamma_7(theta) = 0` for
`theta <= 0.35`, and 0.0103 at `theta = 0.6`.

*Fully analytic bases for longer windows* (`logs/revision1_analytic.log`).
Item 1 needs `k >= 7` at `(0.6, 0.3, 0.05)`, where
`g_inf = 5/96 = 0.0521` and `a q = 0.2708`. Its base per variable is
`exp(((k-1) g_inf - a q)/(5.6 (k+1)))`:

| k | 7 | 8 | 10 | 15 | 20 | 30 | 50 | 100 | limit |
|---|---|---|---|---|---|---|---|---|---|
| base per variable | 1.0009 | 1.0019 | 1.0032 | 1.0051 | 1.0061 | 1.0072 | 1.0080 | 1.0087 | `exp(g_inf/5.6) = 1.0093` |

With the first version's `Lambda = 3.4` the same values are 1.0008 to 1.0071
(`k = 7..100`). The bound of Proposition C.2 is far below the LP window gap
(`0.0417` against `0.1477` at `k = 7`), so a better analytic window gap
would raise these bases.

Bases for other window lengths, with LP window gaps
(`logs/chiral_bounds_P2.log`, `logs/chiral_bounds_P1.log`; ceilings from
`logs/revision1_corner.log`):

| class | k | `gamma_k` (LP) | transport base with LP gap | computed base per variable | ceiling per variable (Section 5) |
|---|---|---|---|---|---|
| `P_2` (class (a)) | 4 | 0.0115 | 1.0004 | 1.0031 | ≤ 1.0075 |
| `P_2` | 5 | 0.0503 | 1.0015 | 1.0138 | ≤ 1.027 |
| `P_2` | 6 | 0.0976 | 1.0025 | 1.0207 | ≤ 1.044 |
| `P_2` | 7 | 0.1477 | 1.0033 | 1.0234 | ≤ 1.058 |
| `P_1` (balanced split) | 6 | 0.1797 | 1.0046 | 1.0344 | ≤ 1.083 |
| `P_1` | 7 | 0.2205 | 1.0049 | 1.0329 | ≤ 1.088 |

### 4.4 Higher chirality defeats `P_{2m}`

**Proposition C.4.** Replace the chiral term by `(g/2)(x y^{2m} - x^{2m} y)`
with `m >= 1`, and put `h_m(t) = -(g/2) t^{2m+1}` and
`S_m(x, y) = sum_{j<m} x^{2j} y^{2(m-1-j)}`.

1. `W + h_m(x) - h_m(y) = (x + y)^2 (b/2 + (g/2)(y - x) S_m) + (ev/2)(x^2 + y^2)`.
   So for `0 < g <= b/(2m)` the conclusions of Proposition C.1 hold, with
   `P_{2m+1}` exact at the root.
2. For every `g > 0` there is `ev_0(m, g) > 0` such that for
   `0 < ev < ev_0` the per-bond `P_{2m}` gap is positive. If also
   `g <= b/(2m)`, then `x* = 0` by item 1, the root gap grows linearly in
   `n`, and the argument of Theorem C.3 gives an exponential lower bound for
   every per-node split in `P_{2m}`. The windows must be long enough for the
   bulk gap to beat the end terms, and the base is above 1 but not
   computed.

*Proof.*
1. This is again a polynomial identity (sympy, `m = 1, 2, 3`). Use
   `|y - x| <= 2` and `S_m <= m` on `[-1,1]^2`.
2. The curve `p -> (p, p^3, ..., p^{2m+1})`, `p in [-1, 1]`, is odd and
   spans `R^{m+1}`. The convex hull of a set that is symmetric about `0`
   and spans the space contains `0` in its interior. So for small `c > 0`
   the point `(0, ..., 0, -c)` lies in the convex hull. By Carathéodory's
   theorem it is the vector of the first `m+1` odd moments of some law of
   `p` on `[-1, 1]`.
   - The bond law of `(p, -p)` is `P_{2m}`-consistent, because the odd
     moments up to `2m - 1` vanish.
   - Its per-bond value is `ev E p^2 - g c`, which is negative for small
     `ev`. □

Computed per-bond LP values for `m = 2`, `(b, g) = (0.6, 0.15)`
(`logs/chiral_bulk.log`):

| `ev` | `P_1`, `P_2` | `P_3`, `P_4` | `P_5`, `P_6`, equal marginals |
|---|---|---|---|
| 0.02 | 0.0374 | 0.0020 | 0 |
| 0.005 | 0.0460 | 0.0070 | 0 |

As for the gadget family of [R, Section 3.3], a fixed chain is exact for
large degree, and the gap of the defeated class shrinks as the degree
grows.

### 4.5 Branch-and-bound counts

Leaves at `(b, g, ev) = (0.6, 0.3, 0.05)` (`chains/polychain.py`). The
class bound is computed by column generation. The factor minima of the
shifted cubic factors come from corners, edge critical points and interior
critical points (Sylvester resultant), plus a small grid. A self-test on
300 random quartics never returned a value above a 801 × 801 grid minimum
(`logs/polychain_selftest.log`). Logs: `logs/bb_chiral.log`,
`logs/bb_chiral2.log`; `eps = 1e-4` unless stated.

| class, rule | n = 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | growth per variable (last steps) |
|---|---|---|---|---|---|---|---|---|---|---|
| `P_2`, spread | 2 | 4 | 6 | 14 | 22 | 44 | 69 | 123 | 212 | 1.75 |
| `P_2`, bisect | 3 | 8 | 16 | 38 | 84 | 190 | 433 | 989 | 2,254 | 2.28 |
| `P_2`, spread, `eps = 1e-6` | 2 | 4 | 8 | 16 | 33 | 62 | 110 | – | – | 1.8 |
| `P_1`, spread | 6 | 10 | 32 | 61 | 159 | 298 | 718 | 1,275 | 3,378 | 2.2 |
| `P_1`, bisect | 32 | 142 | 455 | 1,257 | 3,204 | – | – | – | – | 2.6 |
| `P_3`, bisect | 1 | – | 1 | – | 1 | – | – | – | – | root exact |

- The growth is exponential and nearly independent of `eps`. One run
  (`P_2`, spread, `eps = 1e-6`, `n = 10`) had one LP failure and one
  undecided box; that box was branched.
- The rates are lower than for the gadget chain of [R] (2.7–2.85 per
  variable for class (a)). Smarter branching (spread) helps, but it does
  not remove the growth.
- These counts are floating-point illustrations. Unlike [R], they were not
  reproduced by independent code.

### 4.6 Scope: sparse moment-SOS relaxations (exact under a condition on the box constraints)

This subsection was added after the first review, which supplied the
decomposition below. The second review showed that the placement of the
box constraints matters; the first version stated exactness without that
condition. The cases with a gap and the comparison with the standard forms
were revised accordingly.

The relaxation considered: one moment sequence; moment matrices of order 2
on the cliques `{x_i, x_{i+1}}`; localizing matrices of order 1 (degree-2
multipliers) for the constraints that are attached to a clique; the
moments of the monomials of a single variable are shared by the two
cliques that contain it.

**Proposition C.5.** Let `0 < ev`, `0 < g <= b/2`. The order-2 sparse
relaxation above of the chiral chain on `[-1, 1]^n` has value `f* = 0`
for every `n >= 2` in each of the following cases:

- (a) the linear box constraints `1 - x_i >= 0` and `1 + x_i >= 0` are
  localized in every clique that contains `x_i`;
- (b) each linear box constraint is localized in one clique, in the
  orientation of the certificate: `1 - x_i` in clique `(i, i+1)` and
  `1 + x_i` in clique `(i-1, i)` (for `x_1` and `x_n`, the only clique);
- (c) `1 - x_i^2 >= 0` is localized in every clique that contains `x_i`;
- (d) the ball constraint `2 - x_i^2 - x_{i+1}^2 >= 0` is localized in
  every clique, and the box constraints of `x_1` and `x_n` are present in
  any of the forms above, linear or quadratic (a univariate multiplier
  suffices; the other box constraints are not used). More
  generally, the ball `2M^2 - x_i^2 - x_{i+1}^2 >= 0` suffices when
  `g (M^2 + 1) <= b + ev/2`; at `(0.6, 0.3, 0.05)` this means
  `M <= 1.0408`.

*Proof.* The bracket of Proposition C.1 decomposes as

```
W(x, y) + h(x) - h(y) = [(b/2 - g)(x + y)^2 + (ev/2)(x^2 + y^2)] + (g/2)(x + y)^2 (1 + y) + (g/2)(x + y)^2 (1 - x),
```

and the end terms as `(a/2) t^2 ∓ h(t) = ((a - g)/2) t^2 + (g/2) t^2 (1 ± t)`
(sympy, `logs/revision1_sos.log`). Every term is a sum of squares of degree
at most 4, or a sum of squares of degree 2 times a linear box constraint.
The `h` terms telescope as in Proposition C.1. `b/2 - g >= 0` is where
`g <= b/2` enters.

- (a), (b): in bond `(e, e+1)` the certificate uses `1 + x_{e+1}` and
  `1 - x_e`, and the end terms use `1 + x_1` and `1 - x_n` with the
  univariate multiplier `t^2`. All of these are localized in the clique
  where they are used, in both cases. So `f_n - 0` has a clique-wise
  Putinar certificate of order 2, and the relaxation has value at least
  `0 = f*`.
- (c): use `1 + y = (1 + y)^2/2 + (1 - y^2)/2` and the same for `1 - x`;
  this needs `1 - x_{e+1}^2` and `1 - x_e^2` in clique `(e, e+1)`, and
  keeps every degree at most 4.
- (d): `(1 + y) + (1 - x) = [(1 + y)^2 + (1 - x)^2 + (2 - x^2 - y^2)]/2`,
  so the last two terms of the bracket equal
  `(g/4)(x + y)^2 [(1 + y)^2 + (1 - x)^2] + (g/4)(x + y)^2 (2 - x^2 - y^2)`
  (sympy, `logs/revision2_sos.log`). This uses no linear box constraint.
  With `2M^2` in place of `2`, the first bracket becomes
  `((b - g (M^2 + 1))/2)(x + y)^2 + (ev/2)(x^2 + y^2)`, which is a sum of
  squares when `b - g (M^2 + 1) + ev/2 >= 0`, because
  `x^2 + y^2 >= (x + y)^2/2` (sympy, `logs/revision2_independent_sos.log`). □

**Other placements** (`chains/revision2_chains.py sos` →
`logs/revision2_sos.log`; rows marked † were added in round 3,
`chains/revision3_chains.py waki` → `logs/revision3_waki.log` and
`radius` → `logs/revision3_radius.log`; `n = 5, 8` at
`(b, g, ev) = (0.6, 0.3, 0.05)`; values of the moment relaxation with
Clarabel; `f* = 0`, so a negative value is the root gap with its sign
changed; floating point unless marked "proved"):

| box constraints | `n = 5` | `n = 8` | status |
|---|---|---|---|
| (a) linear, every clique | `1.9e-8` | `1.8e-8` | exact (C.5) |
| (b) linear, one clique, orientation of the certificate | `7.6e-9` | `1.0e-7` | exact (C.5) |
| linear, one clique, opposite orientation (`1 - x_i` in `(i-1, i)`, `1 + x_i` in `(i, i+1)`) | `-0.0553` | `-0.2072` | gap |
| † opposite orientation + Waki et al.'s scaled bounds `0 <= L(z^alpha) <= 1`, `z = (1 + x)/2` | `-0.0538` | `-0.1994` | gap |
| opposite orientation + ball, `M = 1` | `6.1e-8` | `1.3e-7` | exact (C.5(d)) |
| opposite orientation + ball, `M = 1.01` | `6.1e-8` | `1.3e-7` | exact (C.5(d), `M <= 1.0408`) |
| opposite orientation + ball, `M = 1.1` | `6.8e-8` | `1.1e-7` | no gap found (also none at `n = 16, 32` †) |
| † opposite orientation + ball, `M = 1.3` | `4.5e-8` | `8.8e-8` | no gap found (also none at `n = 16, 32`) |
| † opposite orientation + ball, `M = 1.5` | `1.6e-8` | `2.0e-7` | no gap found (also none at `n = 16, 32`) |
| opposite orientation + ball, `M = 2` | `1.9e-7` | `-0.0158` | gap at `n = 8` (and at `n = 16, 32` †) |
| opposite orientation + ball, `M = 10` | `-0.0427` | `-0.1782` | gap |
| linear, univariate multipliers (Waki et al., form (20)) | unbounded | unbounded | proved unbounded (below); Clarabel stops at `-7.0e6` and `-1.4e7` |
| same, with moment bounds `\|y_alpha\| <= 1` (our choice of bounds, not Waki et al.'s) | `-0.0628` | `-0.1263` | gap |
| † same, with Waki et al.'s scaled bounds `0 <= L(z^alpha) <= 1`, `z = (1 + x)/2` | `-0.6989` | `-1.3317` | gap |
| (c) `1 - x_i^2`, every clique | `1.1e-8` | `5.5e-8` | exact (C.5) |
| `1 - x_i^2`, one clique (either side) | `5.6e-9` | `5.0e-9` | no gap found |
| `1 - x_i^2`, univariate multipliers (with or without `\|y_alpha\| <= 1`) | `<= 9.4e-9` | `<= 1.2e-8` | no gap found |

- SCS agrees with Clarabel on every bounded row at `n = 5, 8` (for the
  opposite orientation without ball it reports "optimal_inaccurate" with
  `-0.05527` and `-0.20703`). The runs at `n = 16, 32` used Clarabel
  only.
- *Waki et al.'s scaled bounds* (†, round 3). Waki et al. do not use
  `|y_alpha| <= 1` for a box `[-1, 1]`. Their Section 5.6 maps each variable to
  `z = (1 + x)/2 in [0, 1]` and then adds `0 <= y_alpha <= 1` for the
  moments of `z`. Here this means `0 <= L(z_i^p z_{i+1}^q) <= 1` on every
  clique monomial of degree 1 to 4, written in the `x`-moments as
  `2^{-(p+q)} sum_{r <= p, s <= q} C(p, r) C(q, s) y_{x_i^r x_{i+1}^s}`.
  These are different linear constraints from `|y_alpha| <= 1`, and with
  univariate multipliers they leave a gap about ten times larger.
  Their constraints `0 <= z_i <= 1` are `1 ± x_i >= 0` up to a positive
  factor, with the same univariate localizing cones. Waki et al. also
  divide each polynomial by its largest coefficient; that multiplies the
  objective by a positive constant and does not change whether there is a
  gap. The values above are in the units of `f_n`.
- An independent implementation of the SOS side (Gram matrices of the
  Putinar certificate, maximizing the constant;
  `chains/revision2_independent.py sos` →
  `logs/revision2_independent_sos.log`) gives the same values from the
  other side of the duality: `-0.0553055` and `-0.2071798` for the
  opposite orientation (moment side `-0.0553053`, `-0.20718`), `0` and
  `-0.0158185` with the ball `M = 2`, and `0` for (a), (b) and the ball
  `M = 1`. For univariate multipliers it finds no useful certificate
  (Clarabel stops at its iteration limit with `-2.8e8` and `-4.3e8`).
- *Unboundedness with univariate multipliers (proved).* Take in every
  clique the moments `y_{x_i} = 0`, `y_{x_i^2} = 1/2`,
  `y_{x_i x_{i+1}} = 0`, `y_{x_i x_{i+1}^2} = -s`, the other cubic moments
  `0`, `y_{x_i^4} = 2T`, `y_{x_i^2 x_{i+1}^2} = T`, the other quartic
  moments `0`, with `T = 4 s^2 + 2`. The univariate moments are the same
  in every clique, so the cliques are consistent. The moment matrix splits
  into two blocks whose leading principal minors are positive polynomials
  in `s` (sympy), and the univariate localizing matrices of `1 ∓ x_i` are
  `[[1, ∓1/2], [∓1/2, 1/2]]`, positive definite. The objective is
  `a n/2 - (g/2)(n - 1) s`, which tends to `-inf` as `s` grows. (Dually:
  multipliers of degree 2 times linear constraints have degree 3, so the
  degree-4 part of the SOS term must vanish, and then nothing produces the
  mixed cubic terms of `f_n`.) A first attempt at this direction, with
  `y_{x_i^4} = y_{x_i^2 x_{i+1}^2}`, was not positive semidefinite; the
  log keeps only the corrected one.
- The ball radius matters: the bound `M <= 1.0408` of C.5(d) is
  sufficient, not necessary (`M = 1.1`, `1.3` and `1.5` show no gap at
  `n = 5, 8, 16, 32`; Clarabel values at most `5.3e-7`), but `M = 2` and
  `M = 10` leave gaps. For `M = 2` the gap is `0.0158`, `0.1328` and
  `0.3784` at `n = 8, 16, 32`, about 0.015 per variable from `n = 8` to
  `32` (†; the third review reported the same values).

**Relation to the standard forms** (local full texts in
`literature/papers/`; Section 6).

- *Lasserre (2006).* Assumption 3.2 partitions the constraints among the
  cliques, so each constraint is attached to exactly one clique, and
  (3.1) adds the redundant ball `n_k M^2 - |X(I_k)|^2 >= 0` per clique,
  with `|x|_inf < M` on the feasible set (Assumption 3.1), here
  `2M^2 - x_i^2 - x_{i+1}^2` with `M > 1`. With linear box constraints in
  the orientation (b) this form is exact for every `M`. With the opposite
  orientation it is exact for `M <= 1.0408` (proved) and shows no gap for
  `M = 1.1`, `1.3`, `1.5` (floating point, `n = 5, 8, 16, 32`; the third
  review also found none at `n = 12, 24`), and it has a gap for
  `M = 2` (`n = 8, 16, 32`) and `M = 10` (`n = 5, 8`).
  Listing a constraint once per clique (it is redundant to repeat it)
  gives case (a).
- *Waki, Kim, Kojima and Muramatsu (2006).* In the sparse SOS relaxation
  (20) the multiplier of a constraint is supported on the variables of
  that constraint (Section 4.2), so a bound constraint gets a univariate
  multiplier: unbounded with linear bounds. Section 5.4 strengthens (20)
  by supporting the multiplier on one maximal clique that contains the
  constraint's variables (the one-clique placements above, in either
  orientation), or on the union of all such cliques, which they used in
  their experiments (Section 6). The union variant contains the
  certificate of case (a), because a sum of SOS multipliers on the two
  cliques of `x_i` is an SOS multiplier on their union; this follows from
  the proof and was not computed. Section 5.5 adds the linearized valid
  inequalities `0 <= y_alpha <= rho^alpha` when `0 <= x_i <= rho_i`.
  Section 5.6 (Scaling) maps a box `eta_i <= x_i <= rho_i` to
  `z_i in [0, 1]` and adds `0 <= y_alpha <= 1` for the moments of `z`.
  With univariate multipliers these scaled bounds leave gaps 0.699
  (`n = 5`) and 1.332 (`n = 8`); with one clique per constraint in the
  opposite orientation, 0.0538 and 0.1994 (table above, floating point).
  The bounds `|y_alpha| <= 1` in the table are a simpler choice of ours,
  not Waki et al.'s; they also leave a gap. (Section 6 of the paper refers
  to the union-of-cliques support as "Section 5.5"; the heading in the
  local copy, both `fulltext.md` and `original.pdf`, is 5.4. Earlier
  versions of this note followed that cross-reference.)

Numerical confirmation of the first version (`logs/revision1_sos.log`,
unchanged): case (a) gives `1.9e-8` (`n = 5`) and `1.8e-8` (`n = 8`), and
case (c) gives `5.5e-8` (`n = 8`). As a control, the same relaxation that
shares only the moments of `x_i` and `x_i^2` between cliques (PSD moment
and localizing matrices kept) gives `-0.19904` at `n = 8`, which is the
class-(a) root gap of Section 4.2 (0.1990).

So Theorem C.3 is a statement about factorable MINLP relaxations whose
shared univariate lifts are `x_i` and `x_i^2` (class (a), [R, Section 1.3]:
per-factor envelopes, McCormick, RLT, `2x2` PSD cuts on shared `x_i^2`
auxiliaries). It is not a statement about moment-SOS solvers, in either
direction: those that localize the box constraints as in Proposition C.5
are exact at the root, and some of the other placements above have a root
gap or are unbounded, but how their trees grow was not studied. Not every
placement outside Proposition C.5 has a gap: the ball with `M = 1.1`,
`1.3` or `1.5`, and `1 - x_i^2` in one clique or with univariate
multipliers, showed none (floating point). This
is consistent with [R, Section 1.3], where the order-`r` sparse relaxation
is dominated by `b_{2r}`: `b_3` is exact here (Proposition C.1), and the
dominated relaxation may or may not be.

## 5. Why the proved bases stay small

**Corner boxes cap the tilted-volume method (Lebesgue measure).** With
Lebesgue reference measure, for any box `B`,
`Phi(mu) >= (vol(B)/vol) exp(mu V(B))`. Boxes in a corner far from `x*`
have large `V(B)`, and they reach 1 once `mu` exceeds a threshold `mu0`.
Then every admissible `mu` is below `mu0`, and the full window gives a base
of at most `exp(mu0 gamma_k)` per window. This cap concerns Lebesgue
measure only; for other product measures it was not computed.

- *Exact values on positive corner boxes.* On `B = prod_j [s_j, 1]` with
  `s_j >= 0`, every factor of the `k`-chain is nondecreasing in both
  arguments: for `x, y in [0, 1]`,
  `d_x W = (a - g y) x + y (b + (g/2) y) >= 0` and
  `d_y W = (a + g x) y + x (b - (g/2) x) >= 0` (using `a > g` and
  `g <= 2b`), and the end terms `(a/2) x^2` are nondecreasing. So each
  factor's minimum over `B` is at the lower corner, the factor minima of the
  base split add up to `f_k(s)`, and `LB <= min_B f_k = f_k(s)`. Hence
  `V(B) = f_k(s)` for every split class (proved). The negative corners
  give the same values by the symmetry `x -> -(reversed x)`.
- *Ceilings* (`logs/revision1_corner.log`). Minimizing
  `mu(s) = sum_j log(2/(1 - s_j)) / f_k(s)` (multistart L-BFGS-B,
  floating point) gives `mu0 <= 3.238, 3.153, 3.099, 3.062` for
  `k = 4, 5, 6, 7`. The class-(a) column-generation bound on the optimal
  box equals `f_k(s)`, as it must. The ceilings per variable,
  `exp(mu0 gamma_k/(k+1))`, are 1.0075–1.058 for class (a) and
  1.050–1.088 for the balanced split (`k = 4..7`); they are in the table of
  Section 4.3. A better search can only lower them.
- The first version used a random search over 60 corner boxes, with the
  column-generation dual bound for `V`. It found `mu0 = 3.4–4.1` and
  ceilings 1.009–1.078 (class (a)) and 1.058–1.119 (balanced split). The
  review's local corner search found `mu0 = 3.07` at `k = 7`; the value
  above confirms it.
- *Long windows (heuristic).* `mu0` decreases with `k`: 3.00, 2.93, 2.89
  and 2.875 for `k = 10, 20, 50, 100`, towards the uniform-bulk value
  `min_s log(2/(1-s))/((a+b) s^2) = 2.863` (at `s = 0.832`). If
  `gamma_k/(k+1)` tends to the per-bond value `g_inf = 0.052`, which was
  not checked beyond `k = 12`, the method cannot exceed about
  `exp(2.863 · 0.052) ≈ 1.16` per variable on this family with Lebesgue
  measure. The first version said that `mu0` stays near 3.5–4 and gave
  about 1.2; that came from the coarse random search.
- [R] found 1.063 for the gadget.

**The reason is a ratio, not a family.** The ceiling is about
`exp(c · (class gap per variable)/(curvature of f away from x*))` with
`c` of order 1.

- In both families the split-robust gap is a few percent of the curvature
  scale. For the chiral chain, `g_inf <= g/4 <= b/8`, against bond
  curvature `2(a + b) ≈ 4b`. The constraint `g <= b/2` comes from the
  certificate of Proposition C.1.
- The face-exact bound for termwise McCormick reaches 5/3 per variable
  [F, Theorem 1] because the McCormick gap at box centres, `b w_i w_j/4`,
  is of the same order as the curvature.
- A class that contains the good splits leaves only a "residual" gap.
- So a meaningful base by volume counting needs a family whose split-robust
  gap is comparable to its curvature. Neither family has this, and we do
  not know one.

**The class gap needs large boxes.** In the chiral windows,
`gamma_7(theta)` vanishes for `theta <= 0.35` and is 7% of
`gamma_7(1)` at `theta = 0.6`. The fooling uses points at `±1` and `±q`, so
boxes that exclude the outer points lose most of the gap. Such boxes are
genuinely easier. This is not an artefact of the counting.

**Non-uniform reference measures.** Theorem B.2 allows them, and the
reviews of [R] suggested them. They were not optimized here, and the
ceilings above do not apply to them.

- Moving mass toward `x*` hurts: small boxes near `0` are exact, so they
  gain weight without paying `exp(-mu gamma)`.
- Moving mass away from the corners helps only until the core step (the
  binding term above) takes over.
- We expect at most a modest gain. This expectation was not computed.

**Upper side: an attempt that failed** (`chains/sparse_narrow.py`,
`logs/sparse_narrow.log`). Do boxes that are full in all coordinates but
every `p`-th one, which is narrow, form a certified cover? For class (a)
at `eps = 1e-4`:

- With `p = 4` (windows of three, whose gap is zero when pinned exactly),
  no width works down to intervals of width 0.2. A narrow interval away
  from `0` acts as a non-zero boundary value, and windows with such
  boundaries have gaps.
- With `p = 3`, at `n = 8` only (two narrow coordinates), the boxes are
  certified at interval width 0.1 (20 intervals per narrow coordinate) and
  not at widths 0.2 or 0.5. The worst box has lower bound `-0.99992e-4`, at
  the edge of the tolerance. If the same width sufficed for every `n`, this
  would give `20^{n/3}`, about 2.7 per variable, which is worse than
  branch-and-bound. This extrapolation rests on one size and was not
  checked.

So the true growth of minimal certificates for the chiral chain is
bracketed only by about 1.02 (computed lower bound; 1.0009–1.009 fully
analytic) and the branch-and-bound counts (about 1.75 per variable up to
`n = 12`, an upper bound only for those `n`).

## 6. Relation to prior work

Literature examined: the local folder `literature/` (no paper package on
ergodic optimization, Aubry–Mather theory or turnpikes; its index was
searched by author and keyword), the program's audit
[`../literature/decomposition-bb-prior.md`](../literature/decomposition-bb-prior.md),
and open web sources on 2026-09-30. Bibliographic data were checked by web
search. Where text was read, this is said.

- **Discrete Aubry–Mather theory and sub-actions.** For a chain
  `sum_k L(x_k, x_{k+1})`, the ground energy per particle is the
  "minimizing holonomic value" `L̄`. A *sub-action* is a continuous `u` with
  `u(y) - u(x) <= L(x, y) - L̄`; calibrated sub-actions solve min-plus
  (Lax–Oleinik) eigenproblems. We read the introduction of Garibaldi and
  Thieullen, "Minimizing orbits in the discrete Aubry–Mather model",
  Nonlinearity 24 (2011) 563–611, which gives exactly these definitions and
  cites Aubry and Le Daeron (Physica D 8 (1983) 381–422) and Mather for the
  Frenkel–Kontorova model. The definition is given there for `Z^d`-periodic
  interactions.
  - In the language of this note: if `S` contains a sub-action `h` of the
    bond function, the split `r_i = h` makes every bulk factor at least
    `L̄`, so the class is exact in the bulk. Conversely, by LP duality (as
    in [K, Theorem 1.1] and [K, Proposition 1.2] for attainment), the
    per-bond LP of Section 4.2 has value `L̄` only if `S` contains a
    sub-action. This converse is a sketch; the end terms are not treated.
  - The relaxation `LB_S` is the restriction of the holonomic (Mañé)
    measures to measures whose two marginals agree only on `S`.
  - Mañé's holonomic measures were checked at the bibliographic level only;
    the related discrete paper of D. Gomes is known to us only through the
    citation in Garibaldi–Thieullen.
- **Ergodic optimization.** "Adding a coboundary" to reveal maximizing
  measures is the central tool of the field (Jenkinson, "Ergodic
  optimization in dynamical systems", Ergod. Th. Dynam. Sys. 39 (2019)
  2593–2618, abstract read). Lipschitz calibrated sub-actions exist for
  Lipschitz potentials (Contreras, Lopes and Thieullen, "Lyapunov
  minimizing measures for expanding maps of the circle", Ergod. Th. Dynam.
  Sys. 21 (2001) 1379–1409; bibliographic level).
- **Polynomial auxiliary functions.** Restricting the sub-action
  (auxiliary function) to polynomials of degree `d`, and finding it by
  convex optimization, is the method of Tobasco, Goluskin and Doering,
  "Optimal bounds and extremal trajectories for time averages in nonlinear
  dynamical systems", Phys. Lett. A 382 (2018), arXiv:1705.07096 (abstract
  read). That paper treats continuous time, and its bounds are sharp as
  `d -> inf`. Our `P_d` classes are the discrete, finite-chain analogue.
  Propositions C.2 and C.4 are explicit examples where the degree-`d`
  bound is not sharp and degree `d + 1` is.
- **Symmetric couplings and period two.** That a symmetric pair function
  has a period-at-most-two ground state is an elementary observation. We
  did not find it stated in this form; the closest are statements on
  periodic ground states of lattice models with symmetric interactions
  (web search; not read in detail).
- **Turnpikes.** Exponential convergence of optimal boundary layers to the
  bulk optimum (the sketch after Theorem A.2) is a turnpike property; see
  Zaslavski, *Turnpike Properties in the Calculus of Variations and Optimal
  Control*, Springer 2006 (bibliographic level).
- **Cost shifting.** The relation of `LB_S` to dual decomposition,
  reparametrization and weighted-CSP soft arc consistency is in
  [R, Section 1.5] and [K, Section 8].
- **Sparse moment-SOS relaxations** (added in round 1, corrected in
  round 2). The relaxation of Proposition C.5 is a variant of the
  correlative-sparsity relaxations of Waki, Kim, Kojima and Muramatsu,
  "Sums of squares and semidefinite program relaxations for polynomial
  optimization problems with structured sparsity", SIAM J. Optim. 17
  (2006) 218–242, and of Lasserre, "Convergent SDP-relaxations in
  polynomial optimization with sparsity", SIAM J. Optim. 17 (2006), doi
  10.1137/05064504x. It is not either of them as stated (the first
  version said it was). Local copies in `literature/papers/`. We read both
  abstracts; in Lasserre's paper Assumptions 3.1 and 3.2, the redundant
  ball constraints (3.1), Example 3.3, the relaxation (3.5) and
  Remark 3.5(ii); in Waki et al. Sections 4.2–4.3 (multiplier of a
  constraint supported on that constraint's variables, relaxation (20)),
  5.4 (multipliers on one clique or on a union of cliques), 5.5 (valid
  inequalities `0 <= y_alpha <= rho^alpha` for `0 <= x_i <= rho_i`), 5.6
  (scaling to `[0, 1]`, then `0 <= y_alpha <= 1` on the scaled moments)
  and the description of the experiments in Section 6. Section numbers are
  the headings of the local copy (`fulltext.md` and `original.pdf`); the
  paper's Section 6 cites the support enlargement as "Section 5.5".
  - Lasserre assigns each constraint to exactly one clique (the sets
    `J_k` partition the constraints) and adds a ball constraint per
    clique.
  - Waki et al.'s basic form (20) uses multipliers supported on the
    constraint's own variables, which for a bound constraint is a
    univariate multiplier.
  - Proposition C.5 localizes each box constraint in every clique that
    contains its variable (case (a)), in one clique in a fixed orientation
    (case (b)), or adds a ball with `M = 1` (case (d)). Section 4.6 lists
    which of the standard forms this covers and which have a gap.

  That a degree-3 chain has an exact order-2 certificate, and that other
  placements leave a gap, are direct checks, not results taken from these
  papers.
- **Domain walls.** Free domain walls (discommensurations) in
  frustrated or modulated chains are classical in the Frenkel–Kontorova
  literature cited above (bibliographic level). Their effect on
  branch-and-bound covers (Proposition A.3) is what is used here.

*What appears new*, as far as found:

- Theorem A.2 as a statement about certificate sizes of spatial
  branch-and-bound;
- the pinning lemma and its use to remove weak links from [R, Theorem 4.2];
- the chiral family as a natural translation-invariant family on which a
  fixed-degree split class fails while the next degree succeeds;
- the per-bond closed form `(g - ev)^2/(4g)`;
- Proposition A.3 (from the first review; made unconditional by
  Lemma A.4, whose split came from the second review): a linear lower
  bound for a fixed split caused by a free domain wall.

All are elementary. An unsuccessful search does not establish novelty.

## 7. Status

| Item | Content | Status |
|---|---|---|
| Prop A.1 | symmetric bonds: balanced split exact in the bulk; root gap `<= max(u(a),u(c)) - min u`; exact if `u(t) = min u` | proved |
| Thm A.2 | under (H1), certificates of the balanced split of size `N(eps)` independent of `n` (`n >= 2`); no growing lower bound for any class containing it | proved; the quasi-polynomial `N(eps)` is a sketch |
| Section 2.4 | UD chain: 10 leaves for `n = 5..16` (balanced, spread); unsplit gap +0.125 per variable | computed (floating point) |
| Prop A.3 | WALL (no (H1)), even `n >= 4`: `n/2` degenerate wall minimizers; every fixed-balanced-split cover at `eps < 0.01134` has `>= n/2` boxes | proved (global optimality of the walls by Lemma A.4; until round 2 it was a hypothesis checked for `n <= 16`); fooling value in closed form, 30-digit evaluation |
| Lemma A.4 | WALL: `min phi = phi(-1, c)`; balanced split exact for odd `n`; a class-(a0) split exact for even `n >= 4`; so classes (a), (a0) root-exact and the walls global minimizers for every `n` | proved; root counts, split identity and the two grid bounds in exact arithmetic (sympy, fractions), grid bounds also by interval arithmetic |
| Section 2.5 | WALL: B&B linear in `n` for the fixed split; root gaps. `u = t^2 + 1.5t`, `b = 1.2`: even-`n` defect at a chain end | computed (floating point) |
| Lemma B.1 | pinning | proved |
| Thm B.2 | tilted volume over pinned windows, any product reference measure | proved |
| Prop C.1 | chiral chain: `f_n >= (ev/2) sum_i x_i^2`, unique interior nondegenerate `x* = 0`, `b_3` root-exact (`g <= b/2`) | proved; identity checked exactly (sympy) |
| Prop C.2 | class-(a) and balanced-split root gap `>= (n-1)(g-ev)^2/(4g) - a q` | proved; LP shows the family is optimal on the grid |
| Thm C.3 | exponential lower bound for every per-node class-(a) split; analytic base for all `ev < g <= b/2` (`Lambda = 2a + 2b + g`); at `(0.6, 0.3, 0.05)`: 1.0009 (`k = 7`) to 1.0087 (`k = 100`) fully analytic, 1.0033 with the LP gap, 1.023 computed; leftover windows handled | item 1 proved; item 2 uses LP fooling values (floating point) and grid maxima |
| Prop C.4 | degree `2m+1` chirality: `P_{2m+1}` exact (`g <= b/(2m)`), `P_{2m}` gap for small `ev` | proved (existence); values computed for `m = 2` |
| Section 4.5 | chiral B&B: 1.75 (spread), 2.3 (bisect) per variable for class (a) | computed; not independently reproduced |
| Prop C.5 | order-2 sparse moment-SOS relaxation (pair cliques) exact at the root of the chiral chain when the box constraints are localized in every clique of their variable, or in one clique in the orientation of the certificate, or with the ball `2 - x_i^2 - x_{i+1}^2` per clique | proved; identities checked exactly (sympy); SDP values `<= 1.3e-7` (floating point) |
| Section 4.6 | other placements: gaps 0.0553 (`n = 5`) and 0.2072 (`n = 8`) for one clique in the opposite orientation; univariate multipliers unbounded, gap at `n = 5` of 0.0628 with `\|y_alpha\| <= 1` and 0.699 with Waki et al.'s scaled bounds; ball with `M = 2`, `10` leaves gaps (`M = 2`: 0.378 at `n = 32`); some placements outside C.5 show no gap (ball `M = 1.1`–`1.5`: runs at `M = 1.1`, `1.3`, `1.5` and `n = 5, 8, 16, 32`, and at `n = 12, 24` in the third review; the radii in between rely on the value being nonincreasing in `M` (proved in the fourth review, `../reviews/robust-lb-chains-confirm-r3.md`, Section 1), so that no gap at `M = 1.5` means none at smaller `M` for the same `n`. Also `1 - x_i^2` in one clique or univariate) | gaps computed (floating point; moment and SOS sides agree for the opposite orientation, moment side only for the moment bounds); unboundedness proved |
| Section 5 | ceilings of the method with Lebesgue measure (`<= 1.058` per variable for class (a), `k = 7`; about 1.16 for long windows, heuristic); sparse-narrow covers not competitive at `n = 8` | `V` exact on positive corner boxes (proved); `mu0` by local optimization (floating point) |

## 8. Limitations and open problems

- **The base.** No meaningful base was proved. On the chiral chain the
  computed base (1.023 per variable) is about as small as for the gadget
  chain, and the fully analytic one is 1.0009–1.009. Section 5 explains why
  volume-type counting with Lebesgue measure cannot do much better on these
  families. A meaningful split-robust base needs either a family whose
  split-robust gap is comparable to its curvature, or a counting argument
  that is not volume-based (or a reference measure that was not tried).
  All are open.
- **Uniform chains without (H1).** Theorem A.2 assumes a constant bulk
  ground state with a margin (H1). Without it the fixed balanced split can
  need `n/2` boxes (Proposition A.3, WALL). Open: whether some symmetric
  chain without (H1) gives a growing (or exponential) lower bound for class
  (a), (a0) or `b_d`; and how covers behave when the frustration sits at a
  chain end (the example `u = t^2 + 1.5 t`, `b = 1.2` was not analysed).
  (Round 1 listed as open that the wall configurations are global
  minimizers for all even `n`; Lemma A.4 proves it.)
- **Quantitative turnpike.** The explicit `N(eps)` of Theorem A.2 is
  `exp(O(eps^{-1} log(1/eps)))`. The quasi-polynomial version is a sketch.
- **Branching rules.** Theorem A.2 bounds minimal certificates. The spread
  rule found small ones in the example. No theorem says that a practical
  rule finds them in general. Widest-side bisection grew linearly in the
  example; whether it can grow exponentially on symmetric uniform chains
  was not tested beyond this example.
- **Chiral chains.**
  - Proposition C.1 needs `g <= b/2`. The DP suggests that `x* = 0` holds
    beyond it (`g = 0.45`), but larger `g` was not used.
  - Nonconvex even unary terms (for example `-kappa x^4`) keep the fooling
    `P_2`- and `u`-consistent, so class (a) with `u` in the class should
    still fail. The certificate of Proposition C.1 would need
    `kappa <~ ev`. This is untested.
  - Only one parameter point was run through branch-and-bound.
- **Numerics.**
  - All counts are floating point.
  - The cubic factor minimization is a careful floating-point procedure,
    not an enclosure.
  - The chiral counts were not reproduced by independent code.
  - The computed bases use LP fooling values and grid maxima.
  - The WALL counts use the same code as the other uniform-chain counts;
    they agree with the counts reported by the review, whose code we have
    not seen.
  - The moment-SOS gaps of Section 4.6 are floating point, at one
    parameter point and `n = 5, 8` (the ball rows with `M = 1.1`, `1.3`,
    `1.5` and `2` also at `n = 16, 32`).
    The moment side and an independently written SOS side agree where both
    were computed (opposite orientation, with and without the ball
    `M = 2`); the gaps with `|y_alpha| <= 1` and with Waki et al.'s scaled
    bounds were computed here on the moment side only (Clarabel and SCS).
    The third review's own code gives the same values for univariate
    multipliers. The fourth review's own code reproduces all three rows
    (univariate multipliers with either bound, and the opposite
    orientation with the scaled bounds) from both the moment and the SOS
    side, floating point (`../reviews/robust-lb-chains-confirm-r3.md`,
    Section 2.3). With the ball `M = 2` the gap grows by about 0.015 per
    variable from `n = 8` to `32`. How the other gaps grow with `n`, and
    whether the relaxations with a gap need large trees, was not studied.
- **Scope of the relaxation.** As in [R]: per-factor relaxations dominated
  by per-factor envelopes, with shared univariate lifts in the class. For
  the chiral chain the class is `P_2`, that is, factorable MINLP
  relaxations with shared `x_i` and `x_i^2` auxiliaries. Not covered: cuts
  on three or more variables, convexity detection of the whole objective,
  objective-cutoff propagation, and lifted variables outside the class.
  Adding `t^3` as a shared lift already closes the chiral chain, and so
  does the minimal-order sparse moment-SOS relaxation when the box
  constraints are localized as in Proposition C.5 (every clique of the
  variable, or one clique in the orientation of the certificate, or a
  ball with `M = 1` per clique). With other placements that relaxation can
  have a root gap or be unbounded (Section 4.6). Theorem C.3 says nothing
  about moment-SOS solvers either way.

## 9. Files and commands

All commands were run from `chains/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` on a shared machine. They are
targeted runs. No project-wide checks were run, and CI was not consulted.

| File | Purpose | Command → log |
|---|---|---|
| `explore_uniform.py` | PROGRAM-like uniform chains: `phi` minimizer, `f*_n`, balanced and class-(a) root gaps | `python3 explore_uniform.py` → `logs/explore_uniform.log` |
| `search_uniform.py` | random quartic uniform chains with (H1) and a balanced root gap | `python3 search_uniform.py SEED` (seeds 1–4) → `logs/search_uniform_*.log` |
| `uniform_design.py` | the UD chain (piecewise quadratic `u`) and design trials | `python3 uniform_design.py` → `logs/uniform_design.log` |
| `bb_rules.py`, `run_uniform.py` | B&B with rules `bisect`/`spread` on UD (robust_bb class bounds) | `cat jobs_uniform.txt \| xargs -P 6 -L 1 sh -c 'timeout 3600 python3 run_uniform.py $0 $@'` → `logs/bb_uniform.log`; same with `jobs_uniform2.txt` (unsplit base) → `logs/bb_uniform_unsplit.log` |
| `roots_uniform.py` | UD root gaps: balanced, unsplit, class (a) | `python3 roots_uniform.py` → `logs/roots_uniform.log` |
| `polychain.py` | class bounds for polynomial bond factors (resultant-based factor minima), B&B; self-test | `python3 polychain.py` → `logs/polychain_selftest.log` |
| `chiral.py` | chiral chain: sympy certificate, per-bond LP, DP, root gaps | `python3 chiral.py certificate` → `logs/chiral_certificate.log`; `bulk 0.6 0.3 0.05`, `bulk 0.6 0.3 0.1`, `bulk 0.6 0.15 0.02 2`, `bulk 0.6 0.15 0.005 2` → `logs/chiral_bulk.log`; `dp ...` → `logs/chiral_dp.log`; `roots 0.6 0.3 0.05 2 ... 12` → `logs/chiral_roots_ev05.log` (and `0.1` → `_ev10`) |
| `run_chiral.py` | one chiral B&B job | `cat jobs_chiral.txt \| xargs -P 8 -L 1 sh -c 'timeout 11000 python3 run_chiral.py $0 $@'` → `logs/bb_chiral.log`; `jobs_chiral2.txt` → `logs/bb_chiral2.log` |
| `chiral_bounds.py` | `Lambda_j`, `gamma_k(theta)`, analytic and computed bases, corner ceilings | `python3 chiral_bounds.py 0.6 0.3 0.05 D 4 5 6 7` (`D = 2`, `1`) → `logs/chiral_bounds_P2.log`, `logs/chiral_bounds_P1.log` |
| `sparse_narrow.py` | sparse-narrow covers (Section 5) | `python3 sparse_narrow.py 0.6 0.3 0.05 2 1e-4 7 4 0.5 0.25 0.2 0.125 0.1` and `... 8 3 0.25 0.1 0.05` → `logs/sparse_narrow.log` |
| `checks_note.py` | UD coefficients, `x*` margin and Hessian; binding term of the computed chiral bound | `python3 checks_note.py` → `logs/checks_note.log` |
| `wall_check.py` (revision) | WALL: `u'`, `c`, `phi`, DP `f*_n`, wall configurations, root gaps of env/(a0)/(a); the fooling family of Proposition A.3 (grid LP and 30-digit closed form); class bounds on adjacent-pair boxes; end-defect example; B&B | `python3 wall_check.py basic` → `logs/wall_basic.log`; `family` → `logs/wall_family.log`; `classes` → `logs/wall_classes.log`; `endfrust` → `logs/wall_endfrust.log`; `cat jobs_wall.txt \| xargs -P 6 -L 1 sh -c 'timeout 3600 python3 wall_check.py bb $0 $@'` → `logs/bb_wall.log` |
| `revision1_chiral.py` (revision) | chiral chain: `max abs(d W)`, fully analytic bases, leftover-window suprema, exact corner ceilings, moment-SOS identity and SDP | `python3 revision1_chiral.py lambda` → `logs/revision1_lambda.log`; `analytic` → `logs/revision1_analytic.log`; `leftover` → `logs/revision1_leftover.log`; `corner` → `logs/revision1_corner.log`; `sos` → `logs/revision1_sos.log` |
| `revision2_chains.py` (round 2) | Lemma A.4 in exact arithmetic (root counts, split identity, sum of minima, rational grids with a Lipschitz bound) plus floating-point cross-checks; moment side of the order-2 sparse relaxation of the chiral chain for 15 placements of the box constraints (Clarabel, SCS) and the sympy identity of C.5(d) | `python3 revision2_chains.py wall` → `logs/revision2_wall.log`; `python3 revision2_chains.py sos 5 8` → `logs/revision2_sos.log` |
| `revision2_independent.py` (round 2) | second route for Lemma A.4 (split from the shifts `r_i`, end-bond minima, interval bounds); SOS side of the relaxation for six placements; the ball identity with general `M`; the unbounded direction for univariate multipliers | `python3 revision2_independent.py wall` → `logs/revision2_independent_wall.log`; `sos` → `logs/revision2_independent_sos.log` (part (F) of that log was regenerated with `direction` after the first direction was found not to be PSD) |
| `revision3_chains.py` (round 3) | moment side of the order-2 sparse relaxation of the chiral chain: univariate multipliers with `\|y_alpha\| <= 1` (rerun) and with Waki et al.'s scaled bounds `0 <= L(z^alpha) <= 1`, `z = (1 + x)/2`; opposite orientation with the scaled bounds; opposite orientation with the ball `M = 1.1, 1.3, 1.5, 2` at `n = 5, 8, 16, 32` (Clarabel; SCS at `n <= 8`) | `python3 revision3_chains.py waki` → `logs/revision3_waki.log`; `radius` → `logs/revision3_radius.log` |

Approximate compute: every run finished within minutes (single thread per
run, at most 8 runs in parallel), except the class-(a) bisection run of the
chiral chain at `n = 12` (718 s). The whole set of runs took well
under an hour of wall time. The revision runs took about half an hour of
wall time in total; the longest was the grid LP with 801 points per axis in
`wall_check.py family`. The round-2 runs took a few minutes in total (the two SDP
scripts about 1.5 minutes each; the WALL checks a few seconds). The round-3
runs took 13 s (`waki`) and 25 s (`radius`).

## 10. Revision after review

### 10.1 Round 1

Each item below was first checked independently here, then the note was
changed. All checks are targeted runs from `chains/` (commands in
Section 9); no project-wide verification was run and CI was not consulted.
No count in Sections 2.4 and 4.5 changed.

1. **Part 1 headline overclaimed (WALL).** *Review:* "no lower bound that
   grows with `n` exists" for uniform symmetric chains, including the fixed
   balanced split, holds only under (H1); counterexample WALL. *Check:*
   `wall_check.py basic`, `family`, `classes` and the B&B runs
   (`logs/wall_*.log`, `logs/bb_wall.log`).
   - `u' >= 1.015 > b`; `phi` is minimized off the diagonal at `(-1, c)`,
     `c = 0.3377232`; for even `n = 4..16` the `n/2` wall configurations
     have the same value, and grid DP with polishing and the class-(a)
     dual bound agree with it (floating point).
   - The adjacent-pair argument holds (proof written out in
     Proposition A.3). The fooling value is reproduced: a closed-form family
     with `s = 779/10000`, `t = 467/2000` gives
     `Delta = 0.0113432715...` (30 digits), and the column-generation
     bracket on `H_1`, `H_2` (`n = 6`) is `0.0113433` at both ends.
   - The B&B counts are reproduced exactly: spread `3, 5, ..., 15`,
     bisection `4, 7, ..., 22` for even `n = 4..16`, one leaf for odd `n`;
     class (a) needs one leaf.
   - New here: classes (a0), `b2`, `b3`, `b4` also close the gap on `H_j`,
     and (a0) is root-exact like (a). So the linear bound is specific to the
     fixed split. Also, the root gap of the fixed split on WALL stays below
     `phi(-1, -1) - m = 0.302` for every `n` (Proposition A.1), although the
     minimal cover grows.

   *Change:* Summary item 1 now says "under (H1)" and states the WALL
   result; new Section 2.5 with Proposition A.3; Section 2.3 (retitled "Why
   (H1) matters"), the remarks of Section 2.2, "For solvers", and
   Sections 6, 7 and 8 updated. Theorem A.2 is unchanged, as the review
   said.
2. **Domain-wall remark.** *Review:* "Otherwise the optimum contains a
   domain wall whose position is nearly free" is not always true
   (`u = t^2 + 1.5 t`, `b = 1.2`). *Check:* `wall_check.py endfrust`. For
   even `n = 6..12` the grid-DP minimizer has its defect at one end
   (mirror image equal); forcing both ends into the `-1` phase costs at
   least 0.149. For `n = 4` the minimizer is symmetric. *Change:* the remark
   in Section 2.2 now lists both observed cases, and Section 2.5 documents
   the example. The first version's statement is withdrawn.
3. **Relaxation scope.** *Review:* the minimal-order sparse moment-SOS
   relaxation is exact at the root of the chiral chain, by a decomposition
   of the bracket of Proposition C.1. *Check:* `revision1_chiral.py sos`:
   sympy confirms the decomposition, the end terms and the quadratic-box
   variant exactly; the order-2 sparse SDP gives values at most `6e-8`
   (`n = 5, 8`); the control that shares only `x_i`, `x_i^2` gives
   `-0.19904`, the class-(a) root gap. *Change:* new Section 4.6 with
   Proposition C.5; Summary item 3 (scope bullet), "For solvers",
   Section 6 (references) and Section 8 (scope) now say that Theorem C.3
   concerns factorable MINLP relaxations with shared `x_i`, `x_i^2`
   auxiliaries, not moment-SOS solvers.
4. **"Every split class considered in [R] contains the balanced split."**
   *Check:* [R, Section 1.2 and Theorem 4.3]: `b_d` there is taken
   relative to the gadget base split, and the fixed unsplit split is
   studied in [R, Sections 2.1 and 6.2]. The statement is false.
   *Change:* Summary item 1 now lists the classes that contain the balanced
   split and says which classes of [R] do not.
5. **Corner-box cap for "any reference product measure".** *Check:* only
   Lebesgue measure was used in `chiral_bounds.py`, and Section 5 said that
   other measures were not optimized. *Change:* the Summary and Section 5
   now restrict the cap to Lebesgue measure.
6. **Leftover windows in Theorem C.3.** *Check:* the first version's proof
   used `G` full windows and did not treat the remaining variables; at
   `mu = 2.112` transport does not apply. *Change:* Theorem C.3 now states
   the window bookkeeping (leftover length `r = n - G(k+1)`; when `k + 1`
   divides `n` the end index is pinned, which Lemma B.1 now allows). Item 1
   handles the leftover window by transport (`gamma_r >= 0`). Item 2 uses a
   point-mass product bound,
   `Phi_r(mu) <= prod_j max(1, sup_d ((1-d)/2) exp(mu c_j d^2))`; at
   `mu = 2.112` every supremum is at most `0.8138 < 1`, so every factor is
   1 (`logs/revision1_leftover.log`). This covers every `r` and every
   `mu < 2.3085`, consistent with the review's check `Phi_r(2.13) <= 1`
   for `r <= 6`. A remark after Theorem B.2 says that windows with
   `Phi_W <= 1` may be dropped.
7. **Binding terms in Section 4.3.** *Check:* `logs/checks_note.log` lists
   the terms; four core terms (0.8284, 0.8284, 0.8201, 0.8190) exceed the
   point-mass term (0.8138). *Change:* the sentence is corrected.
8. **"1.0033 analytic" depends on the LP gap.** *Check:* 1.0033 is
   `exp(gamma_7/(2 · 2.8 · 8))` with the LP value `gamma_7 = 0.14772`. With
   the bound of Proposition C.2 (`0.0417` at `k = 7`) and the first
   version's `Lambda = 3.4` the base would be 1.0008. We proved
   `max |d_x W| = max |d_y W| = a + b + g/2` for `g <= b/2` (proof in
   Theorem C.3, step 3; grid check at five parameter points,
   `logs/revision1_lambda.log`), so `Lambda = 2a + 2b + g = 2.8`. *Change:*
   Theorem C.3(1) uses `Lambda = 2a + 2b + g`; the fully analytic bases are
   1.0009 (`k = 7`), 1.0061 (`k = 20`), 1.0087 (`k = 100`), with supremum
   `exp(g_inf/5.6) = 1.0093` (`logs/revision1_analytic.log`), matching the
   review. The 1.0033 is now labelled "with the LP-computed window gap",
   and the table column is renamed.
9. **Ceilings were loose.** *Check:* a new, proved observation makes the
   corner values exact: on positive corner boxes every factor is
   nondecreasing, so `V(B) = f_k(s)` for every class. Minimizing
   `sum_j log(2/(1-s_j))/f_k(s)` gives `mu0 <= 3.062` at `k = 7` (review:
   3.07) and ceilings 1.058 (class (a), review: 1.058) and 1.088 (balanced
   split) at `k = 7` (`logs/revision1_corner.log`). The column-generation
   bound on the optimal box equals `f_k(s)`. *Change:* new ceilings in the
   table of Section 4.3 and in Section 5; the claim "`mu0` stays near
   3.5–4" and the estimate 1.2 are withdrawn; for long windows `mu0`
   decreases towards 2.86, which suggests about 1.16 per variable
   (heuristic).
10. **Minor items.**
    - *Unsplit UD growth.* From `logs/bb_uniform_unsplit.log`: the average
      over `n = 3..8` is `(79/8)^{1/5} = 1.58` (spread) and
      `(144/15)^{1/5} = 1.57` (bisection); 1.4 was the last step. Corrected
      in Section 2.4.
    - *Sparse-narrow extrapolation.* `logs/sparse_narrow.log` has a single
      size (`n = 8`, two narrow coordinates), and the worst box is at
      `-0.99992e-4` against `eps = 1e-4`. The Summary and Section 5 now say
      that `20^{n/3}` is an unchecked extrapolation from one size.
    - *Lipschitz constant of Theorem A.2.* For `n = 2` the single factor is
      `phi + (u(x) + u(y))/2`, which the first version's `L` did not
      cover. The definition of `L` now includes it, the theorem is stated
      for `n >= 2`, and step 3 of the proof says which factors occur.
    - *Formatting.* A `|x|` inside the status table (Proposition C.1 row)
      broke the table; it is now written `sum_i x_i^2`.

### 10.2 Round 2

Each item below was first checked independently here, then the note was
changed. All checks are targeted runs from `chains/` (commands in
Section 9); no project-wide verification was run and CI was not
consulted. No count or root gap in Sections 2.4, 2.5, 4.2 and 4.5
changed.

1. **Moment-SOS scope statements dropped the condition of
   Proposition C.5.** *Review:* the Summary scope bullet, "For solvers"
   and Section 8 said without condition that the order-2 sparse
   moment-SOS relaxation is exact at the root of the chiral chain, while
   Proposition C.5 proves this only when every box constraint is localized
   in every clique that contains its variable. Reported: with each box
   constraint in one clique in the opposite orientation and no ball, gaps
   0.0553 (`n = 5`, Clarabel and SCS) and 0.2072 (`n = 8`); exact again
   with the ball `2 - x^2 - y^2` per clique; Waki et al.'s form (20)
   effectively unbounded with linear bounds, gap 0.0628 at `n = 5` with
   `|y_alpha| <= 1`. Section 6 called C.5's relaxation that of Waki et al.
   and Lasserre, which it is not. *Check:*
   - Literature (local full texts): Lasserre's Assumption 3.2 partitions
     the constraints among the cliques and (3.1) adds a ball constraint
     per clique; Waki et al.'s (20) uses multipliers supported on the
     constraint's own variables (Section 4.2), with the strengthenings of
     Sections 5.4–5.6. The review's description is correct. (Corrected in
     round 3: this item first said "Sections 5.5 and 5.6", following the
     paper's own cross-reference in its Section 6; see Section 10.3.)
   - `revision2_chains.py sos 5 8` (moment side) reproduces every reported
     value: `-0.0553053` and `-0.20718` (opposite orientation; SCS
     `-0.05527`, `-0.20703`, "optimal_inaccurate"), at most `1.3e-7` with
     the ball `M = 1`, `-0.0627682` at `n = 5` with `|y_alpha| <= 1`
     (and `-0.126265` at `n = 8`). A rerun gave identical values.
   - An independently written SOS side (`revision2_independent.py sos`)
     gives `-0.0553055` and `-0.2071798` for the opposite orientation and
     `0` with the ball `M = 1`, so both sides of the duality agree.
   - New here: (i) the univariate form with linear bounds is unbounded,
     proved by an explicit direction whose moment matrices have positive
     leading principal minors (sympy); (ii) a sympy identity gives a
     certificate with the ball alone (C.5(d)), valid for the ball
     `2M^2 - x^2 - y^2` when `g (M^2 + 1) <= b + ev/2` (`M <= 1.0408`
     here); (iii) the radius matters: `M = 2` leaves a gap of 0.0158 at
     `n = 8` (both sides agree) and `M = 10` gaps at `n = 5` and `8`;
     (iv) quadratic box constraints `1 - x_i^2` showed no gap in any
     placement tried (floating point).
   - Written out here, but not new: one clique per constraint in the
     orientation of the certificate is exact (case (b), proved by the same
     certificate as case (a)). The review had already stated this
     (`../reviews/robust-lb-chains-confirm-r1.md`, Section 2.1). The
     round-2 version of this list put it under "New here"; corrected in
     round 3 (Section 10.3).

   *Change:* Proposition C.5 restated with the cases (a)–(d) and their
   proofs; its parenthetical "this case was not checked" replaced by the
   table of placements (floating point, as labelled), the unboundedness
   proof and a comparison with Lasserre's and Waki et al.'s forms;
   Section 4.6 retitled. The Summary scope bullet, "For solvers",
   Section 6 (C.5's relaxation is a variant of the standard forms, not
   either of them; what was read), Section 7 (C.5 row and a new row) and
   Section 8 (scope, numerics) now state the condition.
2. **WALL statements about all `n` rested on checks for `n <= 16`.**
   *Review:* the Summary and "For solvers" said that classes (a) and (a0)
   are root-exact on WALL, and Section 2.3 that the fixed balanced split
   has no cover of size independent of `n`, while the global optimality
   of the walls (the hypothesis of Proposition A.3) and the root exactness
   were checked in floating point for `n <= 16` only. The review supplied
   a class-(a0) split for even `n >= 4`, with `min H = H(-1, c)` checked by
   exact real-root isolation and 40-digit evaluation (not
   interval-certified). *Check* (`revision2_chains.py wall`,
   `revision2_independent.py wall`):
   - The split: sympy, factors built directly (`n = 4..30`) and built from
     the shifts `r_i` (`n = 4..14`); by hand in Lemma A.4(4). The shifts
     lie in `span{t, u}`, so the split is of class (a0).
   - The minima of the end and odd bonds follow from `u' > b`, which is
     exact (root count).
   - `min H = H(-1, c)`: proved here without enumerating critical points.
     For `x >= 1 - 1/b`, `H` increases in `y` because `u' > 1`; the rest
     lies in `[-1, 0]^2`, where an exact rational grid with a Lipschitz
     bound gives `H >= -0.6240`, 0.136 above `H(-1, c)`. Interval
     arithmetic gives `-0.6231`. The floating-point enumeration of
     critical points reproduces the review's next candidate (0.5756
     higher), and a `4001^2` grid agrees.
   - The minima add up to the wall value for every `n` (sympy with `n`
     symbolic; by hand via `H(-1, c) = 2m + b`).
   - Also found: the odd-`n` statement of Section 2.5 ("proved") relied on
     `min phi = phi(-1, c)`, which the first version had checked only on
     a `2001^2` grid. The same method proves it (Lemma A.4(2); margin
     0.48 on the remaining square, exact grid and interval arithmetic).

   *Change:* new Lemma A.4 in Section 2.5 (statement, proof, checks); the
   hypothesis of Proposition A.3 removed; the Facts of Section 2.5 mark
   what is exact; Section 2.3 and the remark in Section 2.2 state the
   bound for every even `n >= 4`; the Summary and "For solvers" cite
   Lemma A.4; Section 7 (Proposition A.3 row, new Lemma A.4 row,
   Section 2.5 row); the open item of Section 8 removed; the header says
   which checks are exact or interval-based.

### 10.3 Round 3

Review: `../reviews/robust-lb-chains-confirm-r2.md`, Section 3. Each item
was first checked independently here, then the note was changed. Checks
are targeted runs from `chains/` (`revision3_chains.py`, Section 9) and a
reading of the local copy of Waki et al.; no project-wide verification was
run and CI was not consulted. No proved statement changed, and no value
already in the note changed.

1. **Section 4.6 closing paragraph overgeneralized (minor).** *Review:* the
   sentence "those with the other placements above have a root gap or are
   unbounded" is contradicted by three rows of the note's own table
   (opposite orientation with the ball `M = 1.1`; `1 - x_i^2` in one
   clique; `1 - x_i^2` with univariate multipliers), all without a gap in
   floating point; the review adds `M = 1.3` and `1.5` with no gap up to
   `n = 32`. *Check:* the three rows are in the table (from
   `logs/revision2_sos.log`: at most `1.1e-7`, `5.6e-9`, `1.2e-8`).
   `revision3_chains.py radius` (Clarabel, `n = 5, 8, 16, 32`; SCS at
   `n = 5, 8`) gives at most `5.3e-7` for `M = 1.1`, `1.3`, `1.5` at every
   `n`, and for `M = 2` the gaps `0.0158`, `0.1328`, `0.3784` at
   `n = 8, 16, 32` (no gap at `n = 5`), as the review reported. The
   sentence was wrong as written. *Change:* the sentence now reads "some of
   the other placements above have a root gap or are unbounded" and names
   the placements without a gap; table rows for `M = 1.3`, `1.5` and the
   larger `n` added (marked †); the radius bullet, the Lasserre paragraph,
   the Section 7 row and the numerics item of Section 8 updated. The
   other scope statements (Summary, "For solvers", Section 8) already said
   "can".
2. **Waki et al.: section numbers and the "analogue" (minor).** *Review:*
   in the local copy, Section 5.4 is the multiplier support (one clique or
   a union of cliques), 5.5 the valid inequalities
   `0 <= y_alpha <= rho^alpha`, 5.6 "Scaling"; the note cited 5.5 and 5.6.
   And `|y_alpha| <= 1` is not Waki et al.'s bound for `[-1, 1]`: they
   scale to `z = (x + 1)/2 in [0, 1]` and add `0 <= L(z^alpha) <= 1`,
   which with univariate multipliers gives gaps 0.699 (`n = 5`) and 1.332
   (`n = 8`). *Check:*
   - Read `literature/papers/waki2006-sums-of-squares-and-semidefinite/fulltext.md`
     (lines 569–613) and the PDF text (`pdftotext -layout original.pdf`):
     the headings are 5.4 "Supports for Lagrange multiplier polynomials",
     5.5 "Polynomial valid inequalities and their linearization", 5.6
     "Scaling". Section 5.6 defines `z_i = (x_i - eta_i)/(rho_i - eta_i)`,
     the scaled problem (37) with `0 <= z_i <= 1`, and adds
     `0 <= y_alpha <= 1`. Section 6 says the multiplier support was
     replaced by the union of cliques "as mentioned in Section 5.5" and
     refers to "the valid inequalities of the form `0 <= y_alpha <= 1`
     given in Section 5.6". So only the support reference is off by one in
     the paper; the note's "Section 5.6 adds `0 <= y_alpha <= rho^alpha`"
     was wrong (that is 5.5), and "Section 5.5 strengthens (20) by
     supporting the multiplier on one maximal clique" was wrong (that is
     5.4).
   - `revision3_chains.py waki` (own moment-side code; Clarabel and SCS
     agree to at least 6 significant digits on every row): univariate
     multipliers with the scaled bounds give
     `-0.6988746` (`n = 5`) and `-1.331693` (`n = 8`), the review's values.
     The rerun with `|y_alpha| <= 1` reproduces `-0.06276815` and
     `-0.1262654`. New here: with one clique per constraint in the
     opposite orientation the scaled bounds do not close the gap
     (`-0.05375`, `-0.19942`, against `-0.0553`, `-0.2072` without them).
   - The univariate localizing cones of `z_i >= 0`, `1 - z_i >= 0` equal
     those of `1 ± x_i >= 0` (positive factor and a linear change of
     basis), and Waki et al.'s coefficient normalization multiplies the
     objective by a positive constant; so the computed relaxation is their
     form (20) with the Section 5.6 bounds, up to that constant.

   The "analogue" remark was inaccurate: `|y_alpha| <= 1` is our own
   choice, not their construction. The conclusion (a gap) holds and is
   stronger with their bounds. *Change:* the Waki paragraph of Section 4.6
   rewritten (5.4, 5.5, 5.6 described by their headings; the "analogue"
   remark withdrawn; the scaled bounds and their gaps stated; a note on the
   paper's cross-reference); a new bullet under the table defines the
   scaled bounds; two table rows (†) added and the `|y_alpha| <= 1` row
   labelled as our choice; Section 6 (what was read), the Summary scope
   bullet, Section 7 and Section 8 updated; the section numbers in
   Section 10.2, item 1 corrected with a note.
3. **Credit for case (b) (nit).** *Review:* Section 10.2, item 1 listed
   case (b) under "New here", but the round-2 review had already stated it
   as proved by the same certificate. *Check:*
   `../reviews/robust-lb-chains-confirm-r1.md`, Section 2.1: "*Proved* for
   the 'every clique' setting and for the one-clique assignment in the
   right orientation (the same certificate)." The credit was wrong.
   *Change:* in Section 10.2, item 1, case (b) moved out of "New here" to a
   separate line that credits the review. The Summary's novelty paragraph
   did not claim it and is unchanged on this point.

### 10.4 Round 4

Review: `../reviews/robust-lb-chains-confirm-r3.md` (verdict: the round-3
changes are correct; one accuracy nit in its Section 4.1 and optional
wording in its Section 4.2). Each item was first checked here against the
logs, then the note was changed. Only wording changed: no proved statement
and no value changed. Checks were targeted reruns (listed at the end of
this subsection); no project-wide verification was run and CI was not
consulted.

1. **Section 8: the third review's cross-check was attributed too broadly
   (nit).** *Review:* the numerics item said that the third review's own
   code gives the same values for the gaps with `|y_alpha| <= 1` and with
   Waki et al.'s scaled bounds. The third review computed these bounds
   only with univariate multipliers, so it did not check the row
   "opposite orientation + scaled bounds". *Check:* in
   `../reviews/robust-lb-chains-confirm-r2-checks/d2_sdp.log` every row
   with `"ybound": true` or `"zbound": true` has `"place": "uni"` (or
   `"uni_quad"`), and there is no opposite-orientation row with either
   bound. The fourth review's `e1_waki.log`
   (`../reviews/robust-lb-chains-confirm-r3-checks/`) has the three rows
   (univariate multipliers with `|y_alpha| <= 1`, univariate multipliers
   with the scaled bounds, opposite orientation with the scaled bounds) on
   both the moment and the SOS side, and they agree with the note's
   values. The attribution was too broad. *Change:* Section 8 now says that
   the third review reproduced the values for univariate multipliers, and
   cites the fourth review's two-sided check (Section 2.3 of that review)
   for all three rows, including the opposite-orientation row. As the
   review notes, the Section 7 row ("moment side only for the moment
   bounds") describes the note's own computations and is unchanged.
2. **Lasserre paragraph: "`n <= 32`" (optional).** *Review:* the runs were
   at `n = 5, 8, 16, 32`, not at every `n <= 32`; the third review added
   `n = 12, 24`. *Check:* `logs/revision3_radius.log` has `M = 1.1`, `1.3`,
   `1.5`, `2` at exactly `n = 5, 8, 16, 32`;
   `../reviews/robust-lb-chains-confirm-r2-checks/d5_radius_n.log` has the
   same radii at `n = 12, 16, 24, 32`, with largest value `1.12e-8` for
   `M <= 1.5` [round 5: was "values at most `1.2e-8`"; Section 10.5].
   `M = 10` was run only at `n = 5, 8` (`logs/revision2_sos.log`).
   *Change:* the paragraph now gives the values of `n` (`n = 5, 8, 16, 32`,
   and `n = 12, 24` from the third review) and says "floating point"
   instead of "computed"; the `M = 10` gap is marked with `n = 5, 8`.
3. **Section 8: which ball rows were run at `n = 16, 32` (optional).**
   *Review:* only `M = 1.1`, `1.3`, `1.5`, `2` were run there, not
   `M = 1`, `1.01`, `10`. *Check:* `logs/revision3_radius.log` (the only
   source of `n = 16, 32` values in the note) contains those four radii
   only; `M = 1`, `1.01`, `10` appear only in `logs/revision2_sos.log`, at
   `n = 5, 8`. *Change:* the parenthetical now names the four radii.

Not applied: the review's third optional point (state that the value of
the relaxation is nonincreasing in `M`, so that the `M = 1.5` run implies
the `M = 1.1` and `1.3` results at the same `n`). It was not among the
items addressed in this round. The review proves it in its Section 1; the
note's statements do not depend on it.

Commands run for this round (from `chains/`, with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`; output to a temporary
directory and compared with `diff`):

| Command | Result |
|---|---|
| `python3 revision3_chains.py radius` | identical to `logs/revision3_radius.log` (9 s) |
| `python3 revision3_chains.py waki` | identical to `logs/revision3_waki.log` (19 s) |
| `python3 e1_two_sides.py waki`, run in `../reviews/robust-lb-chains-confirm-r3-checks/` (the fourth review's script) | result lines identical to its `e1_waki.log` (29 s) |

All three are floating-point SDP solves (Clarabel, SCS); none is
certified. The other evidence for this round was read from existing logs:
`logs/revision2_sos.log`, and `d2_sdp.log` and `d5_radius_n.log` of the
third review.

### 10.5 Round 5

Review: `../reviews/robust-lb-chains-final-confirm-r1.md` (the fifth
review; verdict: verified, all three round-4 changes correct and the
refusal acceptable). It listed only optional points (its Section 5). Each
was checked here against the logs and the fourth review, then the note was
changed. Only wording changed: no proved statement and no value changed.
No solver was run in this round. No project-wide verification was run and
CI was not consulted.

1. **Section 7 row "ball `M = 1.1`–`1.5` up to `n = 32`" (optional; the
   review's Sections 5.1 and 5.2).** *Review:* read as an interval, the
   range rests on the value being nonincreasing in `M`. That fact is
   proved in the fourth review, not in the note, and Section 10.4 had
   declined to state it. "Up to `n = 32`" is the same loose wording that
   round 4 corrected in the Lasserre paragraph. *Check:* the fourth review,
   Section 1, proves the fact. The localizing matrix of
   `2M^2 - x^2 - y^2` in the basis `(1, x, y)` is `2M^2 M_1` minus a
   matrix that does not depend on `M`, and the order-1 moment matrix `M_1`
   is PSD at every feasible point. So raising `M` keeps every feasible
   point feasible, and the value cannot increase. The argument was checked
   here.
   `logs/revision3_radius.log` has `M = 1.1`, `1.3`, `1.5` at exactly
   `n = 5, 8, 16, 32` (values from `1.59e-8` to `5.23e-7`), and
   `../reviews/robust-lb-chains-confirm-r2-checks/d5_radius_n.log` has them
   at `n = 12, 16, 24, 32`. *Change:* the Section 7 row now names the three
   radii run and these values of `n`. It also says that the radii in
   between rely on the monotonicity in `M`, and cites the fourth review,
   Section 1, for its proof. The note's own claims for the three tested
   radii do not change.
2. **Section 10.4, item 2: "values at most `1.2e-8`" (cosmetic; the
   review's Section 5.3).** *Check:* the largest value for `M <= 1.5` in
   `d5_radius_n.log` is `1.121682e-8` (`M = 1.1`, `n = 32`). "At most
   `1.2e-8`" was true but loose. "At most `1.12e-8`" would be slightly
   false, because `1.1217e-8 > 1.12e-8`. *Change:* the text now gives the
   largest value, `1.12e-8`, and a bracket records the old wording.

The Summary's "ball-radius runs up to `n = 32`" was left unchanged. It
describes the third review's runs, which do go up to `n = 32`
(`n = 12, 16, 24, 32`).

Evidence for this round was read from existing files:
`logs/revision3_radius.log`, `d5_radius_n.log` of the third review (both
tabulated with a one-off Python script, with no solver run), and
Section 1 of the fourth review.
