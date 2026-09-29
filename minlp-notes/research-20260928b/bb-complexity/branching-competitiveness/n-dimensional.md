# Competitive node-local branching in n dimensions

Continuation of [`competitive-branching.md`](competitive-branching.md) (the
"main note"), whose model, notation and 1D results are assumed. Date:
2026-09-29. Status: first-pass proofs with exact-arithmetic checks.

The recheck
[`../../reviews/competitive-recheck.md`](../../reviews/competitive-recheck.md)
confirmed Theorem N3, including its exact counts, together with Lemma N4,
Proposition N5 (conditional on Theorem A), Lemma N6 and Examples N1. It
corrected three statements, fixed in place here: the direction of the
radius-criterion failure, the published guillotine bounds, and the tolerances
in Lemma N6. The floating-point experiments of Sections 4–6 were not
rechecked.

## Summary

The question: in `n >= 2` dimensions, is there a node-local rule within a
constant factor `C_n` of the optimal tree on every exact-gap instance? It
remains **open** for the natural candidate `omega` (Conjecture 1 of the main
note), which splits at the relaxation minimizer along its most central
coordinate. This file adds four things.

1. **Why the 1D theory does not transfer (Section 2).**
   - Of the 1D criterion "valid iff `|r| <= rho(c)`", only the "if"
     direction survives in 2D. `|r| <= rho(c)` still implies validity in
     every dimension, but a valid box can have `|r| > rho(c)`. Also, an
     invalid box need not contain the global proximal point. Explicit
     examples are given.
   - In any dimension, splitting along coordinate `i` at the minimizer raises
     the node value at the old minimizer by exactly that coordinate's gap
     term. `omega` is the greedy rule for that quantity, which motivates the
     conjecture but proves nothing.
2. **Theorem N3: splitting every coordinate at the minimizer (`multi`) is not
   competitive (Section 3).** The instance is `f(x,z) = x^2` on `[0,1]^2`:
   - `multi` needs at least order `eps^(-1/2) log(1/eps)` nodes;
   - an explicit guillotine certificate has about `1.21 eps^(-1/2)` boxes.

   An exact computation gives ratios from 1.6 to 15 over
   `eps = 1e-2 ... 1e-8`, while `omega` stays between 0.96 and 1.68. The
   mechanism is that the coordinates shrink at different rates. In this
   workstream it is the first rigorous negative result for a rule that splits
   at the exact relaxation minimizer. It shows that the choice of which
   coordinates to split matters in `n >= 2`, a question the 1D theory cannot
   address.
3. **Guillotine versus arbitrary certificates (Section 4).**
   - Because validity passes to sub-boxes, any certificate can be refined into
     a guillotine one.
   - This gives the self-contained bound `N_guill <= (2 N_opt - 1)^n`, and
     `N_guill <= 1 + C_n log(1/eps) N_opt` via Theorem A, which assumes a
     cube root box.
   - Published binary-space-partition bounds for tilings give
     `N_guill <= 2 N_opt - 1` in 2D (Berman–DasGupta–Muthukrishnan 2002) and
     `N_guill = O(N_opt^((n+1)/3))` for `n >= 3` (Hershberger–Suri–Tóth
     2005). These are known here from their abstracts, read through the
     recheck.
   - In exact grid experiments (MILP against DP), non-guillotine "pinwheel"
     optima appeared on coarse grids. They disappeared when the grid was
     refined, so no genuine overhead was found.
4. **Exact separable and non-separable 2D comparisons (Sections 5 and 6).**
   The rules are compared with the exact guillotine optimum restricted to
   candidate grids.
   - `omega` and a largest-deficit rule stay within a factor of about 2 of it
     on every family tried (maximum 1.91). Slow upward drift appears on two families:
     "sharp × quadratic" for all minimizer rules, and anisotropic quadratics
     for the deficit rule.
   - `multi` grows.
   - For separable instances, `N_opt` is bracketed by the largest 1D
     certificate (slice bound) and the product of 1D certificates.

Answers to the three questions posed for this round:

- **(1) Separable objectives.** Neither a proof nor a counterexample for
  `omega` or the largest-deficit rule. The all-coordinates variant `multi` is
  disproved (Theorem N3; the instance is separable).
- **(2) General smooth `f` in 2D.** The failure of Proposition 1(a) is made
  explicit. Adversarial and structured instances were tested against exact
  grid optima; no counterexample to Conjecture 1 was found. No `C_n` bound was
  proved, with or without log log.
- **(3) Guillotine overhead.** Answered in 2D, open for `n >= 3`.
  - In 2D, `N_guill <= 2 N_opt - 1`, so the overhead ratio
    `(2 N_guill - 1)/(2 N_opt - 1)` is below 2.
  - For `n >= 3`, `N_guill = O(N_opt^((n+1)/3))`, and also
    `N_guill <= 1 + C_n log(1/eps) N_opt` for a cube root box.
  - Whether exact-gap valid families can force superlinear overhead for
    `n >= 3` is open.
  - No instance with any overhead was found once grids were fine enough.

Commands and outputs are in Section 8. No project-wide checks were run.

## 1. Setting

The main note's model applies throughout:

- a box `X0 ⊂ R^n`;
- the exact-gap relaxation `f_B = f - alpha q_B`, with `f + alpha |y|^2`
  convex unless stated;
- the incumbent `f*` and tolerance `eps`;
- `m = f - f* + eps`;
- a box is valid iff `m >= alpha q_B` on it.

Benchmarks:

- `N_opt` is the least certificate (any partition into valid boxes).
- `N_guill` is the least guillotine certificate.
- The best tree has `T_opt = 2 N_guill - 1` nodes.

Rules, all splitting at the relaxation minimizer `y_B`:

- `omega`: along the coordinate `i` maximizing
  `a_i(y_B) = (y_{B,i} - l_i)(u_i - y_{B,i})`;
- `deficit` (separable `m` only): along the coordinate with the most negative
  per-coordinate value `F_i(B_i)` among those with `a_i > 0`;
- `multi`: along every coordinate with `a_i(y_B) > 0` simultaneously;
- `bis`: widest-side bisection, for reference.

For separable `m(y) = sum_i m_i(y_i)`, the node value separates:

```
min_B (m - q_B) = sum_i F_i(B_i),     F_i([l,u]) = min_{t in [l,u]} ( m_i(t) - alpha (t - l)(u - t) ),
```

and `y_B` is the vector of the 1D minimizers.

## 2. What changes in n dimensions

### 2.1 Only one direction of the radius criterion survives

In 1D, Proposition 1 of the main note shows two things: (a) an interval is
valid iff its half-width is at most `rho(c)`, and (b) an invalid interval
contains a global proximal point.

- **The "if" half of (a) holds in every dimension.** With
  `M(c) = min_{X0} (m + alpha |y - c|^2)`, the identity
  `q_B(y) = |r|^2 - |y - c|^2` gives `min_B phi_B >= M(c) - alpha |r|^2`. So
  `|r| <= rho(c)` implies validity.
- **The "only if" half of (a) fails in 2D** (example `k = 10` below).
- **(b) fails in 2D** (example `k = 4` below).
- The first version of this section said that the criterion fails "in both
  directions". That was imprecise, and the recheck corrected it.

**Examples N1.** Take `alpha = 1`, root `[0,1]^2`, `B = [1/2, 1] x [0, 1]`
with centre `c = (3/4, 1/2)` and `|r|^2 = 1/16 + 1/4 = 5/16`. Let
`m = eps + k (x - 3/10)^2`, independent of `z`.

- **`k = 4`: `B` is invalid, but its global proximal point is outside it.**
  - On `B`, the `x`-part of `phi_B` has derivative
    `8(x - 0.3) - (1.5 - 2x) > 0`, so its minimum is on the facet `x = 1/2`,
    with value `0.16`.
  - The `z`-part has minimum `-1/4` at `z = 1/2`. So
    `min_B phi_B = eps - 0.09 < 0`.
  - The global proximal point of `m` at `c` is `x = (0.3k + 0.75)/(k+1) = 0.39`
    (with `z = 1/2`), outside `B`.
  - So the relaxation minimizer `(1/2, 1/2)` lies on a facet with
    `a_1 = 0`, and the rule must choose a coordinate.
- **`k = 10`: `B` is valid, although `M(c) < |r|^2`.** Here
  `M(c) = eps + (k/(k+1)) (0.45)^2 ≈ eps + 0.184 < 5/16`. On `B`, the minimum
  of the `x`-part is `0.4` at `x = 1/2`, so `min_B phi_B = eps + 0.15 > 0`.

So validity is not a radius condition, and "invalid" does not imply that
the proximal point is inside the box.

### 2.2 The key inequality and the greedy reading of `omega`

The main note (Section 6.2) shows that the three facts of Lemma 2 still
combine in `n` dimensions to a single inequality summed over coordinates. That
inequality does not constrain the split coordinate.

One exact identity survives. Split `B` along coordinate `i` at `y = y_B`. On
the child `B'` that contains `y`, `a_i^{B'}(y) = 0` while every other gap term
is unchanged. So

```
phi_{B'}(y) = phi_B(y) + alpha a_i^B(y).
```

`omega` therefore maximizes the increase of the node value at the old
minimizer. It is the "one-step greedy" coordinate choice. The children's
minimizers can move, so this is not a proof of anything. It does explain why
`omega` avoids the failure mode of Theorem N3: `omega` never splits a
coordinate whose gap term at the minimizer is small compared with another
coordinate's.

## 3. Theorem N3: multisection at the minimizer is not competitive

**Instance.** Take `alpha = 1`, `X0 = [0,1]^2` and `f(x, z) = x^2`. Then
`f* = 0`, `m = eps + x^2`, and `f + |y|^2` is convex. The near-optimal set
is the edge `x = 0`. Closed forms:

```
F_x([l,u]) = eps + l u - (l+u)^2/8,  minimizer (l+u)/4 interior,   if u > 3l;
F_x([l,u]) = eps + l^2,              minimizer l (an endpoint),     if u <= 3l;
F_z([c,d]) = -(d-c)^2/4,             minimizer (c+d)/2.
```

`multi` splits `z` at the midpoint of every invalid node, and splits `x` at
`(l+u)/4` exactly when `u > 3l`. (For the first line: minimize
`eps + 2x^2 - (l+u)x + lu`; the stationary point `(l+u)/4` lies inside
`[l,u]` iff `u > 3l`; otherwise the function increases on `[l,u]`.)

**Theorem N3.** On this instance, for `0 < eps <= 1/100`:

- (a) `N_guill <= 1/sqrt(2 eps) + 1/(2 sqrt(eps)) + log2(1/(2 sqrt(eps))) + 3 <= 1.21 eps^(-1/2) + log2(eps^(-1/2)) + 3`.
- (b) `multi` has at least `sum_{k=2}^{K} (k - 1) 4^k >= (K - 1) 4^K`
  internal nodes, where `K = floor(log_16(5/(36 eps)))`. Hence
  `T_multi >= 0.186 (K - 1) eps^(-1/2)`.

Since `K >= (1/4) log2(1/eps) - 2`, `T_multi/T_opt` grows at least like
`c log(1/eps)` with an explicit `c > 0`, so `multi` is not
`C_n`-competitive.

*Proof of (a).* Build a guillotine certificate.

1. **Strips.** Cut `x` at `h = 2 sqrt(eps)`, `2h`, `4h`, ..., giving strips
   `S_0 = [0, h]` and `S_k = [2^(k-1) h, 2^k h]` (the last one truncated at
   1). Then cut each strip in `z`.
2. **`S_0`.** Here `F_x = eps - h^2/8 = eps/2`. With `z`-pieces of width
   `sqrt(2 eps)`, `F_x + F_z >= eps/2 - eps/2 = 0`. That takes
   `ceil(1/sqrt(2 eps))` pieces.
3. **`S_k`.** Here `u <= 2l < 3l`, so `F_x = eps + l^2 >= l^2`. With
   `z`-pieces of width `2l`, the box is valid. That takes at most
   `1/(2l) + 1` pieces, with `l = 2^(k-1) h`.
4. **Sum.** `sum_k 1/(2^k h) <= 1/h = 1/(2 sqrt(eps))`. The number of strips
   is at most `log2(1/h) + 2`. Adding up gives (a). □

*Proof of (b).*

1. **Product structure.** Every internal node is split in `z` at its
   midpoint, so a node at depth `D` has a dyadic `z`-interval of width
   `2^-D`. Validity depends on the `z`-interval only through its width.
   - So at depth `D` the nodes are all pairs (x-interval, dyadic
     `z`-interval of depth `D`) with the same history, and they are all
     valid or all invalid together.
   - An `x`-interval with `u <= 3l` is never split in `x` again. It persists
     to deeper levels, paired with finer `z`-intervals.
2. **The left spine.** `[0, 1]` splits in `x` at `1/4`, and in general
   `[0, 4^-k]` splits at `4^-(k+1)`. So `J_k = [l, 4l]`, with `l = 4^-(k+1)`,
   appears as an `x`-interval at depth `k + 1`.
3. **Inside `J_k`.** Since `4l > 3l`, `J_k` splits at `5l/4`. Generally let
   `R_0 = J_k` and `R_j = [r_j, 4l]` with `r_{j+1} = (r_j + 4l)/4`, so
   `r_j` increases to `4l/3`. Because `4l > 3 r_j`, each `R_j` splits at
   `r_{j+1}` into `L_{j+1} = [r_j, r_{j+1}]` and `R_{j+1}`.
   - `L_{j+1}` satisfies `r_{j+1} <= 4l/3 < 3 r_j`, so it is never split in
     `x` again.
   - `L_j` appears at depth `k + 1 + j`.
4. **Invalidity.** `F_x(L_j) = eps + r_{j-1}^2 < eps + (4l/3)^2 = eps + 16^-k/9`,
   strictly, since `r_{j-1} < 4l/3`.
   At depth `D <= 2k`, the `z`-width `2^-D` gives
   `F_z = -4^-D/4 <= -16^-k/4`. So every node `L_j x J` at depth
   `D in [k+1+j, 2k]` is invalid provided `eps < (1/4 - 1/9) 16^-k = (5/36) 16^-k`.
5. **These nodes are in the tree.** Validity passes to sub-boxes, so all
   ancestors of an invalid node are invalid. Each ancestor was split exactly
   as described: `R_{j-1}` has an interior `x`-minimizer, and every node
   splits `z`.
6. **Distinct nodes.** The nodes `L_j x J` for different
   `(k, j, D, J)` are distinct. `J` ranges over all `2^D` dyadic intervals.
7. **Count.** For `2 <= k <= K`, the condition in step 4 holds by the choice
   of `K`. Counting only `D = 2k` for each `j = 1, ..., k-1` gives at least
   `(k-1) 4^k` internal nodes per `k`.
8. **Numbers.** Also `4^K > (1/4) (5/(36 eps))^(1/2) = 0.0932 eps^(-1/2)`,
   and `T >= 2 (internal) + 1`. □

**Exact check** (`multi_lb.py`, exact rationals for `eps >= 1e-8`). The
ratios use `T_opt <= 2 N_cert - 1`.

| `eps` | `multi` | `omega` | `deficit` | `bis` | certificate `N` | `T_multi/T_opt >=` | `T_omega/(2N-1)` |
|---|---|---|---|---|---|---|---|
| `1e-2` | 45 | 35 | 35 | 43 | 14 | 1.67 | 1.30 |
| `1e-3` | 117 | 87 | 87 | 123 | 38 | 1.56 | 1.16 |
| `1e-4` | 789 | 231 | 231 | 379 | 121 | 3.27 | 0.96 |
| `1e-5` | 5013 | 935 | 935 | 1531 | 375 | 6.69 | 1.25 |
| `1e-6` | 13205 | 3751 | 4775 | 4091 | 1180 | 5.60 | 1.59 |
| `1e-7` | 74645 | 10919 | 19111 | — | 3727 | 10.02 | 1.47 |
| `1e-8` | 353173 | 39591 | 39591 | — | 11772 | 15.00 | 1.68 |

- The proved lower bound, `2 sum (k-1) 4^k + 1`, is met in every row. It is
  weak: the internal-node bound is only 912 at `eps = 1e-6`.
- The observed growth of `multi` is faster than the proved `log` factor.
- Separately, on anisotropic smooth minima
  `m = eps + (x - a)^2 + g (z - b)^2` (`aniso.py`), `multi`'s ratio to the
  exact guillotine grid optimum grows as follows, while `omega` stays at 1.44
  to 1.51:

  | `g` | ratios at `eps = 1e-3, 1e-5, 1e-7, 1e-9` |
  |---|---|
  | 0.05 | 2.06, 2.76, 3.12, 3.81 |
  | 0.01 | 1.88, 3.01, 3.47, 4.19 |

**Mechanism.** `multi` splits every coordinate whose minimizer is interior,
and different coordinates shrink at different rates. Here `x` shrinks by a
factor about 4 per level near the edge, while `z` shrinks by 2. So `multi`
creates many thin `x`-intervals, each paired with all `2^D`
`z`-intervals: a product structure that the optimal certificate avoids.
On the anisotropic family with `g = 0.01` and `eps = 1e-7`
(`leafshape.py`), the leaves of `multi` have aspect ratios `w_z/w_x` up to
`2^6`, against at most `2^2` for `omega`.

## 4. Guillotine versus arbitrary certificates

**Lemma N4 (guillotine refinement).** Let `P` be any certificate with `N`
boxes in `R^n`. Then:

- (a) `N_guill` is at most the size of any binary space partition of `X0` by
  axis-parallel cuts whose cells each lie inside a box of `P`.
- (b) `N_guill <= (2N - 1)^n`.
- (c) Consequently `(2 N_guill - 1)/(2 N_opt - 1) <= 2 (2 N_opt - 1)^(n-1)`.

*Proof.*

- (a) The cells of such a partition are sub-boxes of valid boxes, hence
  valid. Its cuts form a tree, so the cells form a guillotine certificate.
- (b) Along axis `i`, the faces of `P` take at most `2N` distinct values,
  including the root's two faces. Cutting `X0` along all of them, one axis
  after another, is a guillotine partition into at most `(2N - 1)^n` grid
  cells. Each cell lies in one box of `P`, because every box is a union of
  cells.
- (c) This follows from (b) with `N = N_opt`. □

**Proposition N5 (via Theorem A).** Under the scout's two-sided gap
hypothesis with `F = X0` and a cube root box,
`N_guill <= 1 + 4^n (sqrt(kappa n) + 4)^n J_eps N_opt`.

*Proof.* Uniform bisection trees are guillotine and their leaves are
valid, so `N_guill` is at most the number of bisection leaves. Apply
Theorem A. □

**Published bounds, applied through Lemma N4(a).**

Any partition whose cells lie inside boxes of a certificate is itself a
certificate, because validity passes to sub-boxes. So every
binary-space-partition bound for tilings by boxes transfers to `N_guill`.

- **2D.** Berman, DasGupta and Muthukrishnan, "Exact size of binary space
  partitionings and improved rectangle tiling algorithms" (SIAM J. Discrete
  Math. 2002). Their abstract, as reported by the recheck, states a
  binary-space-partition bound of `2n - 1` for `n` rectangles that tile the
  space.
  - Applied to an optimal certificate: `N_guill <= 2 N_opt - 1`.
  - So `(2 N_guill - 1)/(2 N_opt - 1) < 2`.
  - Earlier, Paterson and Yao (1992) had given linear-size partitions for
    orthogonal segments in the plane.
- **`n >= 3`.** Hershberger, Suri and Tóth, "Binary space partitions of
  orthogonal subdivisions" (SIAM J. Comput. 2005). Every subdivision into
  `N` boxes in dimension `n >= 3` has such a partition of size
  `O(N^((n+1)/3))`, tight for `n = 3`.
  - Applied to an optimal certificate: `N_guill = O(N_opt^((n+1)/3))`.
  - This is far better than Lemma N4(b).
  - Their lower bound shows that general 3D subdivisions can need
    superlinear partitions (`Omega(N^(4/3))`).
- **Caveat.** Neither this note nor the recheck read the full texts. The
  size is counted in cells (fragments), which for a tiling equals the number
  of leaves.
- **Open.** Whether exact-gap valid families can force such superlinear
  overhead is open. Proposition N5 caps any such overhead at
  `C_n log(1/eps)` for a cube root box.

**Experiments** (`overhead_search.py`, `overhead_replay.py`,
`overhead_fine.py`).

- **Method.** On random separable and polyhedral 2D instances, compute:
  - the exact guillotine optimum on a grid (DP, `gdp.c`);
  - the exact unrestricted optimum on the same grid (HiGHS MILP).
- **Uniform grids with 8–12 points.** 139 instances completed. One had a
  pinwheel optimum (5 boxes, no free cut) against a guillotine optimum of 6.
  It was a grid artefact: both coordinates have their kink at `1/2`, which is
  not a grid point of `linspace(0, 1, 12)`.
- **Grids that also contain all kinks.** 353 instances completed. One
  pinwheel optimum appeared again (5 against 6). Refining the grid while
  keeping the kinks gave:

  | uniform points | 12 | 23 | 45 | 67 | 89 |
  |---|---|---|---|---|---|
  | `N_guill` on the grid | 6 | 6 | 6 | 6 | 5 |

  So a 5-box guillotine certificate exists with finer cuts, and this pinwheel
  is not evidence of overhead either.
- **Conclusion.** No instance with guillotine overhead was found. Proving
  `N_guill > N_opt` for some valid family would need continuous cut positions
  (for example interval branch-and-bound over tree shapes). This was not
  attempted.

## 5. Separable instances

### 5.1 Bracketing `N_opt`

For separable `m = sum_i m_i`, choose constants so that `min m_i = eps_i`,
with `sum_i eps_i = eps` (a split of the tolerance). Let `N^1(g)` denote the
least 1D certificate for a 1D function `g` in the main note's sense
(`g >= alpha q` on every piece).

**Lemma N6.** For every `i`,

```
N^1( m_i + sum_{j≠i} eps_j )  <=  N_opt  <=  N_guill  <=  prod_i N^1(m_i).
```

The two sides use different tolerances.

- **Lower bound.** `m_i + sum_{j≠i} eps_j = (m_i - eps_i) + eps` is
  coordinate `i`'s 1D problem at the **full** tolerance `eps`. It does not
  depend on the split.
- **Upper bound.** It uses 1D certificates at the **smaller** per-coordinate
  tolerances `eps_i`, and can be minimized over the split.
- The first version did not say this; the recheck pointed it out.

*Proof.*

1. **Upper bound.** Take a 1D certificate for each `m_i` and form the product
   boxes. Each factor has `F_i >= 0`, so each product box is valid. The
   product is guillotine.
2. **Lower bound, setup.** Fix `i`. Let `t_j` be a minimizer of `m_j`, and
   consider the line `{y : y_j = t_j for all j ≠ i}`.
3. **Boxes meeting the line.** The boxes of an optimal certificate that meet
   this line cut it into a 1D partition. For such a box `C`,
   `F_j(C_j) <= m_j(t_j) - alpha a_j(t_j) <= eps_j` for `j ≠ i`, so validity
   gives `F_i(C_i) >= -sum_{j≠i} eps_j`.
4. **Conclusion.** That condition says `C_i` is valid for the 1D function
   `m_i + sum_{j≠i} eps_j`. So the 1D partition is a 1D certificate for that
   function. □

The two sides can differ by a large factor. At a nondegenerate smooth
minimum, the lower bound and the true value are both about `log(1/eps)`,
while the product is about `log(1/eps)^n`. The lemma locates `N_opt` but does
not decide competitiveness.

### 5.2 Exact comparisons against the guillotine grid optimum

- **Method.** `sep_families.py` and `aniso.py` compute each rule's leaves and
  the exact guillotine optimum restricted to a candidate grid.
  - The grid has 17 uniform points, the kinks, and a geometric grid of 4
    points per octave around the minimizers, down to `sqrt(eps)/16`.
  - The grid optimum is an upper bound on `N_guill`, so the ratios below are
    **lower bounds** on the true loss when it exceeds 1.
- **Results.** Ratios `leaves/N_guill_grid` at `eps = 1e-3, 1e-5, 1e-7`:

| Family (`x` × `z`) | `omega` | `deficit` | `multi` | `bis` |
|---|---|---|---|---|
| sharp × sharp | 1.00, 1.00, 1.00 | 1.00, 1.00, 1.00 | 1.00, 1.00, 1.00 | 2.75, 4.0, 6.0 |
| sharp × quadratic | 1.25, 1.50, 1.73 | same | same | 1.88, 2.17, 2.53 |
| shallow kink × quadratic | 1.40, 1.53, 1.63 | 1.50, 1.53, 1.63 | 2.2, 2.0, 2.0 | 1.9, 2.0, 2.21 |
| quadratic × quadratic | 1.47, 1.61, 1.60 | 1.47, 1.54, 1.65 | 2.07, 2.07, 2.00 | 1.67, 1.64, 1.85 |
| quadratic × 0.05 quadratic | 1.50, 1.49, 1.51 | 1.50, 1.55, 1.70 | 2.06, 2.76, 3.12 | 1.67, 1.60, 1.63 |

Remaining families, run with a coarser grid of 2 points per octave
(`sep_families2.py`):

| Family | `omega` | `deficit` | `multi` | `bis` |
|---|---|---|---|---|
| sawtooth × sawtooth (4 rigid breakpoints each), `eps = 1e-3` | 1.00 | 1.00 | 1.00 | 5.81 |
| sawtooth × quadratic | 1.18, 1.29, 1.63 | 1.18, 1.29, 1.37 | 1.41, 2.14, 3.05 | 2.76, 3.21, 4.16 |

- For sawtooth × sawtooth at smaller `eps`, the grid needed for the 4D DP
  table was too large, and those rows were skipped.
- For quartic × sharp at `eps <= 1e-5`, the grid admits no certificate at
  all, so no ratio is available.

**Targeted check of the drift** (`sharp_quad.py 1 4`): sharp `x` × quadratic
`z` over five decades, with finer `z`-grids (4 points per octave).

| `eps` | `1e-3` | `1e-5` | `1e-7` | `1e-9` | `1e-11` |
|---|---|---|---|---|---|
| `N_guill_grid` | 8 | 12 | 16 | 19 | 22 |
| `omega` leaves | 10 | 18 | 26 | 30 | 42 |
| ratio | 1.25 | 1.50 | 1.62 | 1.58 | 1.91 |
| `bis` ratio | 1.88 | 2.17 | 2.38 | 2.58 | 2.77 |

Both sequences grow linearly in `log(1/eps)`, `omega` at about twice the
slope of the grid optimum. This is consistent with a constant asymptotic
ratio of about 2 to 2.5, not with a growing one. Still, five decades cannot
exclude slow growth.

- **Reading.**
  - `omega` and `deficit` stay within about 2 of the grid optimum (maximum
    1.91, in the targeted check below).
  - Where `N_opt` is bounded (the sharp families), both minimizer rules are
    exactly optimal on the grid, while bisection grows like `log(1/eps)`.
  - The "sharp × quadratic" ratio of 1.25 → 1.73 grows slowly for all three
    minimizer rules. The targeted check below extends it to five decades and
    points to a constant slope ratio of about 2.
  - `deficit` drifts upward on the anisotropic family (1.50 → 1.78 at
    `eps = 1e-9`, `aniso.log`).

### 5.3 Status for separable instances

- No counterexample to `omega` or `deficit` was found.
- No proof exists. The main obstacle is that validity couples coordinates
  through `sum_i F_i >= 0`: surplus in one coordinate can pay for deficit in
  another.
- The slice bound shows that surplus can never help on the "cross" through
  the joint minimizer. Away from it, surplus trading makes non-product
  certificates optimal.
- A proof would need to charge `omega`'s splits to certificate boxes across
  this trading.

## 6. Non-separable 2D instances

`poly2d.py` gives exact node values for `H = max_k (a_k . y + b_k)` (a
maximum of planes) and `m = H - |y|^2`. The relaxation `phi_B` is convex and
piecewise linear, so its minimum over `B` is at an enumerable vertex: a corner
of `B`, a crossing of a breakline with `B`'s boundary, or a triple point.

`poly2d_exp.py` builds 30 random instances with 4–7 tangent planes and
`eps` between `1e-6` and `1e-3`. It compares `omega`, `multi` and `bis`
with the exact guillotine optimum on a grid. The grid contains triple-point
coordinates and `omega`'s own cuts, so the grid optimum is at most `omega`'s
leaves. Results are in Section 8.

Results (`poly2d_exp.log`, 30 instances, `N_guill_grid` between 1 and 8):

| Rule | max ratio | mean ratio |
|---|---|---|
| `omega` | 1.40 | 1.09 |
| `multi` | 2.00 | 1.47 |
| `bis` | 5.33 | 1.99 |

- Random polyhedral instances have small certificates, so none stresses the
  rules much.
- This is weak evidence. Structured non-separable families (tilted sharp
  valleys, facet-minimizer situations like Example N1 at many scales) were not
  run with exact grid optima.

## 7. Conjecture and what a proof needs

**Conjecture 1 (restated).** For each `n` there is a `C_n` such that
`omega` has `T <= C_n N_guill` (strong form: `C_n N_opt`) on every
exact-gap instance.

Evidence and obstacles:

- **Supporting.**
  - The exact comparisons of Sections 3, 5 and 6 show ratios up to about 2
    against grid optima.
  - The greedy identity of Section 2.2 explains why `omega` avoids the
    product over-refinement of Theorem N3.
- **Against the naive proof.**
  - Lemma 2 of the main note has no `n`-dimensional analogue, because the
    inequality sums over coordinates.
  - Nodes crossing a certificate box need not be nested.
  - Surplus trading between coordinates (Section 5) means the relevant
    certificate is not a product.
- **A likely route.** A charging scheme on pairs (certificate box, facet),
  with the greedy identity of Section 2.2 bounding how often `omega` can
  split near a given facet without progress. This is a research question, not
  a sketch of a proof.

## 8. Computations

All commands were run from this directory, single-threaded
(`OMP_NUM_THREADS=1`), with logs next to the scripts. `gdp.c` is compiled with
`gcc -O2 -shared -fPIC -o libgdp.so gdp.c`.

- `python3 multi_lb.py`: Theorem N3 in exact rationals, with the explicit
  certificate checked in floats. Output: the table in Section 3; all
  assertions passed (`multi_lb.log`).
- `python3 aniso.py`: anisotropic quadratics, with exact grid guillotine
  optima (`aniso.log`, excerpt in Section 3).
- `python3 aniso_flat.py`: degenerate and strongly anisotropic variants, with
  no DP (`aniso_flat.log`). `multi/omega` reaches 3.0 (flat `z`) and 4.3
  (`10 (x-a)^2 + 0.01 (z-b)^2`) at `eps = 1e-6`.
- `python3 leafshape.py`: leaf aspect ratios of `omega` and `multi`
  (`leafshape.log`).
- `python3 sep_families.py`: the first table of Section 5.2
  (`sep_families.log`). The run was stopped during the sawtooth family,
  because its grid needed a 4D DP table of several GB.
- `python3 sep_families2.py`: the sawtooth and quartic families with coarser
  grids (`sep_families2.log`).
- `python3 sharp_quad.py 1 4`: the targeted drift check (`sharp_quad_1_4.log`).
- `python3 overhead_search.py 300 150 1` and
  `python3 overhead_search.py 300 150 2 knots`, then
  `python3 overhead_replay.py 1 40`, `python3 overhead_replay.py 2 149 knots`
  and `python3 overhead_fine.py`: Section 4 (`overhead_*.log`).
- `python3 poly2d_exp.py 30 7`: Section 6 (`poly2d_exp.log`).
- `python3 search_sep2d.py {omega,deficit,multi} 5 4 150 1`: random
  separable hill-climbing (`ss_*.log`). The best ratio was 1.33 for every
  rule; random instances are too easy.

Floating-point caveats: all separable and polyhedral runs use floats with a
rounding guard of `1e-12`. Only `multi_lb.py` (the rule simulations) is
exact. No project-wide checks were run and CI was not inspected.

## 9. Open questions

1. Conjecture 1 for `omega`, in `n = 2` first. Separable instances are the
   natural first case.
2. Whether the largest-deficit rule is competitive on separable instances.
   Its mild upward drift on anisotropic quadratics is unexplained.
3. The exact growth of `multi`. Theorem N3 proves `Omega(log(1/eps))`; the
   numerics look faster.
4. Guillotine overhead for `n >= 3`. Can exact-gap valid families force
   the superlinear overhead that general subdivisions allow? The 2D case is
   settled by the published `2 N_opt - 1` bound (known here from its
   abstract).
5. A lower bound above 1 for every I1 rule in `n >= 2` that grows with `n`.
   The main note's Theorem 3 gives only `5/3`, and its `n`-dimensional
   embedding was not checked.
