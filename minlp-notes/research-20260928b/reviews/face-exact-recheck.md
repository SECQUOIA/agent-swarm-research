# Recheck of the revised face-exact note

Date: 2026-09-29. Reviewed document:
[`bb-complexity/spatial-face-exact/face-exact-node-complexity.md`](../bb-complexity/spatial-face-exact/face-exact-node-complexity.md)
(the "note"), as revised after the first review
[`face-exact-review.md`](face-exact-review.md). Scope: the six substantive revisions listed in
Section 11 of the note. Scripts and logs are in [`face-exact-recheck/`](face-exact-recheck/).

All scripts are my own. I read the note's `face_bb.py` and `instances.py` only to see how the
incumbent rule `INC` is implemented and which incumbents were used. No code from the note or the
first review is imported. I did not edit the note and did not commit.

## Verdict

The revised propositions and Example 3.12(b) are correct. My main finding is new: the replacement
conjecture, Conjecture 7.1', is false as stated (item 6).

| # | Claim | Verdict | Main point |
|---|---|---|---|
| 1 | Prop 5.4(a)–(c): 3 nodes without a clamp; bound `1 + 4 beta^-(k0+1)/(1-beta)` with a clamp | Correct | Two slips in the proof wording, neither affects the bound (Section 1) |
| 2 | Prop 5.5: Cantor set `K_beta`; `>= 0.0745 eps^-1/2` nodes at `a = 1/6`, `beta = 1/5` | Correct | One slip in proof (i), step 3. The table shows floating-point counts, which exceed the exact ones by 2–18. Section 5.4 extends the `eps^-1/2` rate to all of `K_beta`, which is not proved and is false uniformly (Section 2) |
| 3 | Prop 5.4(d): incumbent branching takes 3 nodes on the kink | Correct for the modelled rule, with ties broken toward `x` | The statement omits the tie rule. The code tests the incumbent coordinate, not the incumbent point as in the quoted rule; this is harmless for every reported run. `INC` equals bisection on `tilt(0.03)` and `diag` only because the incumbent is the root centre (Section 3) |
| 4 | Example 3.12(b): `N_cov >= 1/(2 sqrt(eps))` | Correct | Proof checked by hand and in exact arithmetic (Section 4) |
| 5 | Prop 4.7: `Theta(1/eps)` with the quadtree | Correct | Every quadtree leaf certified valid in exact arithmetic (Section 5) |
| 6 | Conjecture 7.1' | Well-posed once the quantifiers are fixed. Consistent with every example in the note. **False** | A curved variant of Prop 4.7 has `L(eps) = O(eps^-3/4)` but `N_cov = Omega(1/(eps log(1/eps)))` (Section 6) |

## 1. Proposition 5.4(a)–(c)

**(a)** is correct. For fixed `y`, the envelope of `c(x-a)(y-b)` is a maximum of two affine
functions of `x` with slopes `c(l_y - b)` and `c(u_y - b)`, both of absolute value `< L`.

Check [A] of `kink_exact.py` solves the lifted node LP exactly by rational vertex enumeration
on 471 random rational boxes, for four parameter sets `(L, c, b)` that include both signs of `c`.
There are no mismatches:

- straddling boxes: `LB = -|c| w_y (a-l_x)(u_x-a)/w_x`, and every optimal vertex has `x = a`;
- `y` then sits at relative position `rho = (a-l_x)/w_x` if `c < 0`, and at `1 - rho` if `c > 0`;
- non-straddling boxes: `LB >= 0`, so they are valid at `eps = 0`.

My exact branch-and-bound simulator uses these closed forms only after this check.

**(b)** is correct. Check [B] runs 65 values of `a` at `eps` in `{1e-2, 1e-6, 0}` and gets 3 nodes
every time.

**(c)** is correct, including the new proof that tracks `D = beta^k min(rho_k, 1 - rho_k)`. I
rederived the count:

- Straddling nodes form a subtree.
- At `x`-level `k`, the `y`-split trees have fewer than `beta^-(k+1)` leaves, because those leaves
  have `w_y > beta^(k+1)` and are disjoint in `y`. So the level has fewer than
  `2 beta^-(k+1)` straddling nodes.
- All internal nodes are straddling, and a binary tree has `1 + 2 (internal nodes)` nodes. This
  gives the stated bound.

The proof has two wording slips. Neither affects the bound:

- Line 1399 says each straddling node "has at most one non-straddling child". The final `x` split
  at `a`, at level `k0`, has two. The bound still follows from the identity
  `nodes = 1 + 2 * internal <= 1 + 2 * (straddling nodes)`.
- Step 4 puts the `y` split at relative position `clamp(rho_k, ...)`. That holds for `c < 0`. For
  `c > 0` it is `clamp(1 - rho_k, ...)`. The count only needs each child to keep at least `beta` of
  its parent's width.

Check [C] compares exact counts with the bound for `beta` in `{1/5, 1/10, 3/10, 9/20}`, with 50 or
more values of `a` each, including `beta - 10^-j` and `1 - beta + 10^-j`. The count is at
`eps = 0` where affordable and at `1e-8` otherwise:

- no violations; the largest ratio of count to bound is 0.52;
- `k0` grows as `a` approaches a clamp point from the outer side;
- for `a = 0.1999` (`k0 = 5`), the `eps = 0` tree has 22703 nodes, against the bound 78126.

## 2. Proposition 5.5

**(i)** is correct:

- `K_beta` is uncountable and Lebesgue-null;
- its closure is the attractor of two maps of ratio `beta`, of dimension `log 2/log(1/beta)`
  (0.4307 for `beta = 1/5`);
- `beta/(1+beta)` has period 2.

Check [E] verifies the following for `beta` in `{1/5, 1/10, 1/3, 9/20}`:

- the survivors after `k` steps are `2^k` intervals of total length `(2 beta)^k`, for `k <= 8`;
- the point `beta/(1+beta)` stays in the outer parts along its period-2 orbit.

One slip, in step 3 of proof (i): the right branch of `T` maps `(1-beta, 1]` onto `(0, 1]`, not
`[0, 1)`. Because the outer intervals are half-open, the itineraries that end in a constant run
(`R L L L ...`, `L R R R ...`, and so on) give *no* point of `(0,1)`. So "every infinite sequence
gives a point" should read "every sequence that is not eventually constant". There are still
uncountably many such sequences, so the conclusion stands.

**(ii)** is correct. I checked steps 3–7 by hand. At level `k' < k` the children have bound
magnitude above `(1/36) 5^(-2k') >= 5 eps`. The straddling children at level `k'+1` have magnitude
above `eps`. Finally `(1/5)(7.2)^(-1/2) = 0.07454`.

In exact arithmetic (check [D]), `LP(1,.2)` with widest-side selection takes 13, 39, 167, 547,
1513, 4917 and 19537 nodes for `eps = 1e-2, ..., 1e-8`. That is 17–26 times the proved bound. The
counts of the following rules match the note exactly:

- `x`-only selection;
- `SCIPdef` (widest side);
- bisection;
- `LP(1,0)`, `LP(1,.1)` and `INC`;
- the scout's `a = 1/3` rows for `SCIPdef`.

Two presentation problems:

- **The `LP(1,.2)` counts in the note are floating-point counts.** The note gives 169, 549, 1515,
  4921, 19541, and 19325 for `a = 0.1999`. The exact counts are 167, 547, 1513, 4917, 19537, and
  19307. Check [H] replays the rule in binary floating point and reproduces the note's numbers
  exactly. The cause is width ties `w_y = w_x`. Exactly, these ties go to `x`. In floating point,
  rounding makes some `w_y` slightly larger, so `y` is split once more. The proved bound is
  unaffected. But the text calls the runner's bound "exact closed-form" and speaks of an exact
  rational replay. It should say that the table counts are floating-point, or replace them with the
  exact counts.
- **Section 5.4 (line 1609) overgeneralizes.** It says that on the Cantor set "the count grows at
  least like `eps^(-1/2)`". That is proved only for `a = 1/6`. The proof works for orbits whose
  relative positions stay away from 0 and 1. It is false uniformly on `K_beta`, and false as a
  liminf for suitable points of `K_beta`.

  Check [F] takes `a in K_1/5` whose orbit has a run of `m` left steps from level 2 on. At level 2
  every straddling box has a bound of magnitude at most `beta^(3+m)/6`. For larger `eps` the tree
  stops there:

  | `m` | nodes, `eps = 1e-2 ... 1e-10` | smallest `nodes * sqrt(eps)` |
  |---|---|---|
  | 0 (`a = 1/6`) | 13, 39, 167, 547, 1513, 4917, 19537, 51381, 154165 | 1.23 |
  | 4 | 15, 37, 37, 37, 63, 527, 5553, 46735, 154165 | 0.063 (at `1e-6`) |
  | 8 | 15, 37, 37, 37, 37, 37, 37, 89, 917 | 0.0028 (at `1e-9`) |

  The last two values are below the constant 0.0745 proved for `a = 1/6`.

  An itinerary with runs of unbounded length gives `liminf N(eps) sqrt(eps) = 0`. At the `eps`
  just above the pruning threshold of the `i`-th run, `N` is bounded by the Proposition 5.4(c)
  count up to level `k_i`. So `N sqrt(eps) = O(beta^(m_i/2))`. What holds for every `a` in
  `K_beta` is `N(eps) -> infinity`.

## 3. Proposition 5.4(d) and the incumbent-branching model

**The quoted rule.** I checked the quotation in the local copy of Tawarmalani–Sahinidis
(`literature/papers/tawarmalani2002-.../fulltext.md`, lines 12411–12416, PDF page 243). The rule
is "bisection of the largest nonconvex interval, with the modification that the branching point is
set to the incumbent whenever the latter lies in the current subdomain and is not one of the
end-points of the interval of the selected branching variable". So widest-side selection with an
incumbent point is a faithful model.

**(d) needs the tie rule.** The proof says "the root is a square, so `x` is selected". That holds
only with ties broken toward `x`. The statement of (d), unlike (b) and (c), does not say so.

Check [G] runs `a = 1/3` for `eps = 1e-2, ..., 1e-6`:

| selection | incumbent | test | nodes |
|---|---|---|---|
| ties to `x` | any, e.g. `(a, 1/2)` or `(a, 0)` | either | 3 |
| ties to `y` | `(a, 1/2)` | either | 7 |
| ties to `y` | `(a, 0)` | coordinate | 7 |
| ties to `y` | `(a, 0)` | point in box (the quoted rule) | 17, 49, 193, 513, 1537 |

The last row grows like bisection. The root is split in `y` at the midpoint, since `y* = 0` is an
endpoint. The child `[0,1] x [1/2,1]` then does not contain the incumbent, so it is bisected
forever. So "3 nodes for every `a`" should add "(ties to `x`)". Any robustness claim should note
that the face is placed only in nodes that contain the incumbent.

**Implementation.** `face_bb.py` (lines 217–222) splits at `xstar_i` whenever `xstar_i` is strictly
inside the node's interval, whether or not the node contains the incumbent point. Section 8.1
describes this coordinate test, and Section 5.3 quotes the containment test. The two agree on every
reported run:

- In the 2D runs (`kink`, `kinkT`, `iso`, `tilt`, `diag`), the root is split in `x` at the
  incumbent. Each child contains the incumbent on its boundary and has `w_y = 1 > w_x`, so it is
  next split in `y` at the incumbent. After that, no node's interval strictly contains an
  incumbent coordinate.
- In the 3D runs (incumbent `(a, 1/2, 1/2)`), `x` is split at `a` at the root. The other two
  incumbent coordinates are the midpoints of the unsplit interval `[0, 1]`, so the two tests give
  the same point there, and no later interval strictly contains them.

The note should still say that the coordinate test is what was run.

**`INC` against bisection.** Section 8.4 (line 2026) and Section 5.4 (line 1626) explain the
equality of `INC` and bisection on `tilt(0.03)` and `diag` by "one incumbent point fixes only one
face". The exact equality (1747 and 4091 nodes) has a simpler cause. The incumbent used there is
`(1/2, 1/2)`, the root centre, so every `INC` split coincides with a bisection split.

**Summary claim.** Line 110 says incumbent branching "realizes the `O(1)` certificates of Section
4". That is shown only for the kink family. For Theorem 4.5 a similar argument is plausible, but
it is not in the note.

## 4. Example 3.12(b)

The claim is correct. I checked each step:

- `f = (X + D/2)^2 + 3D^2/4`, so `argmin f = {x = a, y = z}`. On the plane `y = z`, `f = X^2`.
- `C' ∩ R'` is a box in `(x, y)`. Its centre `(x_c, y_c, y_c)` lies in `C ∩ F`. Since
  `y_c` is the midpoint of `[l_y,u_y] ∩ [l_z,u_z]`, both `d_y` and `d_z` are at least `w'_y/2`.
  Lemma 2.1(c) on `xy` and `-xz` gives `Gamma >= w'_x w'_y/2`.
- Validity gives `area(C' ∩ R') <= 2(h^2 + eps)`. With `area(R') = 2h` and `h = sqrt(eps)`, this
  gives `N_cov >= 1/(2 sqrt(eps))`. The condition `eps <= min(a, 1-a)^2` keeps `R'` in the box.

`box_aligned_exact.py` confirms this in exact rational arithmetic:

- the identity holds at 2000 random points;
- the Lemma 2.1(a) gap agrees with the exact convex envelope, computed from the 4 vertices, on 1500
  rectangles and 3 coefficients;
- the centre inequality holds on 8510 random boxes with minimum ratio 1.0000, so it is tight;
- for the `K = 2` variant, `f >= X^2 + |D|` holds on 5000 points;
- the `K = 2` variant is nonconvex: `f(mid) = 1` exceeds the endpoint average `0.99`, for two points
  in the region `D > 0`.

For the smooth version, `N_opt = Theta(eps^(-1/2))`, not only `Omega`:

- `m` is a positive semidefinite quadratic form in `(X, D)`, so (QD) holds.
- Its eigenvalues are `1/2` and `3/2`, so `integral (m + eps)^(-3/2) = O(eps^(-1/2))`.
- Theorem 5.1(a) then gives the upper bound.

The note does not state this, but it supports the claim in Conjecture 7.1' that this example is
consistent. The node-count table for `box_aligned` (Section 8.4) was not rerun.

## 5. Proposition 4.7

The claim is correct, with `Theta(1/eps)`.

- **Lower bound.** `tau = 1/sqrt(2)`, attained by rectangles, and `H^2(S) = 1.29983`, so
  `tau H^2(S)/9 = 0.10212`.
- **Quadtree cases.** I rederived the three cases:
  - `h <= 2 eps`: `sup Gamma <= h/2`;
  - `D < 0`: `Gamma <= 2h(1-y) <= |D|(1-y) = m`;
  - `D > 0`: `Gamma <= 2hy <= D(1+y) = m`.
- **Count.** At side `h`, a refined square has `|i1 - i2 - (a1-a2)/h| < 3`, so there are at most
  `6/h` of them. Summing over dyadic `h > 2 eps` gives at most `6/eps` refinements, each adding 3
  leaves.
- **Optimal set (d).** Correct: 3000 rational points, no mismatches.

`path3_quadtree_exact.py` builds the quadtree for three rational `(a1, a2)` and
`eps = 1/10, 1/30, 1/100, 1/300`. It certifies every leaf exactly:

- A rational dual certificate proves `LB(C) >= -eps`. Exact vertex enumeration is the fallback,
  but it was never needed.
- All leaves are valid; the smallest certified `LB/eps` is `-0.94`.
- The leaf counts (46 to 4132) are below `1 + 18/eps`.
- Every level has at most `6/h` refinements.

## 6. Conjecture 7.1'

### 6.1 Well-posedness

`L(eps)` is a supremum of valid lower bounds on `N_cov`, so `L(eps) <= N_cov(eps) <= N_opt(eps)`.
It is therefore finite and well defined, and the conjecture says `N_opt = O~(L)`. The statement
should fix four things:

- the quantifiers: `C` and the polylog degree may depend on the instance, and `eps` ranges over
  `(0, eps0)`;
- the relaxation: termwise McCormick, (T);
- the phrase "applied to near-optimal sets", which does not fit Theorem 3.4 (Theorem 3.4 integrates
  `m` along lines); this is harmless;
- that Theorem 3.2 is excluded from `L`, and whether that is intended.

### 6.2 The note's own examples

None refutes the conjecture:

| example | `L(eps)` | `N_opt(eps)` |
|---|---|---|
| kink | `O(1)` | 2 |
| `tilt` | `(1/2) sqrt(theta/eps)` | at most `(1/2) sqrt(theta/eps) + 2` |
| `iso`, `diag` | `log(1/eps)` and `eps^(-1/2)` | matched under (QD) by Theorem 5.1 |
| Example 3.12(b) | `>= 1/(9 sqrt(eps))`, from Theorem 3.6 on the strip with `tau = 1/sqrt2`, `eta = eps` | `Theta(eps^(-1/2))` (Section 4 above) |
| Proposition 4.7 | `0.102/eps` | at most `1 + 18/eps` |
| Theorem 4.5 instances | – | `O(1)` |

Example 3.12(a) has a constraint and is outside the conjecture's scope. The `K = 2` variant has no
known upper bound, so it does not contradict the conjecture.

### 6.3 Counterexample: a curved version of Proposition 4.7

The tools in `L` handle flat near-optimal pieces (Theorem 3.6) and transversal curved ones
(Theorem 3.8). A curved, non-transversal near-optimal surface escapes both. The note itself says
that a curved version of Theorem 3.8 is "expected but not proved".

**Instance.** Let `psi(s) = -s - s^2/2`, `c0 = 3/4` and `D = x1 - x2 - c0`. On `[0,1]^3` set

```
G(D, y) = max_{s in [-1,2]} [ -s D - psi(s) y + psi(s) s ],     f = G(D, y) + D y.
```

- `g = G(x1 - x2 - c0, y)` is convex, as a maximum of affine functions, and semialgebraic.
- `phi = x1 y - x2 y - c0 y` is bilinear plus linear, with graph the path `x1 - y - x2`, and is
  relaxed by termwise McCormick.
- `m = f = max_s (D - psi(s))(y - s)`. This is `>= 0` (take `s = y`), and `= 0` on the ruled surface
  `Sigma = {D = psi(y)}`, because `psi` is decreasing.
- `m >= (D - psi(y))^2/12`: take `s = y - (D - psi(y))/8` in the maximum. The grid minimum of
  `m/(D - psi(y))^2` is 0.123.
- The tangent planes of `Sigma` contain `(1,1,0)`, so `Sigma` is not transversal. It is curved:
  `psi'' = -1`.

**Lower bound: `N_cov(eps) >= A/(2 eps (1 + ln(1/(2eps))))` with `A = 0.6148`.**

Parametrize `Sigma` by `(t, y)`, with `x1 = t + psi(y) + c0` and `x2 = t`. Let `C` be a box of a
valid cover and fix `y` in `[l_y, u_y]`.

1. The row slice `{t : (t + psi(y) + c0, t, y) in C}` is an interval of some length `ell`.
2. Its midpoint `p` lies in `Sigma ∩ C`, so `m(p) = 0`, and it has `d_x1, d_x2 >= ell/2`.
3. Lemma 2.1(c) on both terms gives `Gamma_C(p) >= ell d_y`. Validity gives
   `ell <= eps/d_y(y)`.
4. Integrating over `y`, the `(t, y)`-area of `Sigma ∩ C` is at most
   `2 int_0^(w_y/2) min(1, eps/d) dd <= 2 eps (1 + ln(1/(2eps)))`.
5. The `(t, y)`-area of `Sigma ∩ [0,1]^3` is `A = int_0^1 (1 - |psi(y) + c0|) dy = 0.6148`.

**Upper bounds on every tool in `L`.** Here `alpha <= 1` and `E ⊆ {x1y, x2y}`; a pair without
`y` fails (2.1) on boxes with `y` at a bound.

- **Theorem 3.6, `p = 2`.**
  - Taking `K = S` in the definition of `tau` gives the bound
    `max_E W_i W_j (S)/(9(eps+eta)) <= W_y(S)/(9(eps+eta))`.
  - The image of `S` in the `(D, y)` plane is convex and lies in the band
    `|D - psi(y)| <= w = sqrt(12 eta)`.
  - The midpoint of two of its points at `y`-distance `W_y` deviates from `psi` by `W_y^2/8`. So
    `W_y <= 4 sqrt(w)`.
  - Maximizing over `eta` gives `<= 0.48 eps^(-3/4)`.
- **Theorem 3.6, other `p`.**
  - `p = 1`: at most `1/(2 sqrt(eps))`.
  - `p = 3`: `tau = 0`, because boxes with `W_y -> 0` send the ratio to 0.
- **Theorem 3.8.** `K = {y}` is a vertex cover. Covering `S` by `ceil(1/(2 rho))` slabs
  `|y - xi| <= rho = sqrt((eps+eta)/alpha)` and applying (H) gives at most
  `1/(4 sqrt(eps)) + 1/2`, for every `p`.
- **Theorem 3.4.** The maximum matching has size 1, so the bound is at most `eps^(-1/2)/pi`.
- **Proposition 3.10.** A box with `m <= eta` has `W1 + W2 <= 2w` and `W_y <= 2w`, since
  `|psi'| >= 1` on `[0,1]`. So the bound is `vol/nu <= prod max(1, W_i/rho) <= 12^(3/2) = 41.6`.

So `L(eps) = O(eps^(-3/4))` and `N_opt/L >= c eps^(-1/4)/log(1/eps)`. No polylog factor covers
this. The numbers from `conj71_curved.py` are:

| `eps` | lower bound on `N_cov` | upper bound on `L` | ratio |
|---|---|---|---|
| 1e-6 | 2.18e4 | 1.49e4 | 1.46 |
| 1e-10 | 1.32e8 | 1.49e7 | 8.8 |
| 1e-16 | 8.3e13 | 4.7e11 | 176 |

The script also checks, numerically:

- `m >= 0`, and `m = 0` on `Sigma`;
- the growth constant;
- convexity of `G`, by 20000 midpoint tests;
- `A`;
- the slice inequality, on 24323 random boxes with no violation and minimum ratio 1.0000.

The script's checks are numerical; the proof above is what establishes the counterexample.

### 6.4 Suggested repair

Withdraw 7.1' or restate it as an open question. Add to `L` a slice bound of the kind used above:

- take segments of the near-optimal set in a direction `u` with `supp(u)` independent;
- use the gap at each segment's midpoint, weighted by the distance to the faces in the coordinates
  that are fixed along the segment;
- integrate over the family.

A curved version of Theorem 3.6 would serve the same purpose. The instance above would then give
`L >= c/(eps log(1/eps))`. Whether `N_opt = O~(1/eps)` holds there is open; I did not construct an
upper bound. The conjecture currently has no evidence beyond the examples in 6.2.

## 7. Requested corrections

1. Conjecture 7.1': withdraw it or restate it (Section 6). Fix the quantifiers and the relaxation.
2. Section 5.4, line 1609: restrict "grows at least like `eps^(-1/2)`" to `a = 1/6`, or to orbits
   bounded away from 0 and 1. For general `a` in `K_beta`, state only `N -> infinity`.
3. Proposition 5.4(d): add "(ties to `x`)". Note that the face is placed only in nodes that contain
   the incumbent.
4. Sections 5.3, 8.1 and 8.4: say that `INC` was run with the coordinate test. Attribute the
   equality of `INC` and bisection on `tilt` and `diag` to the centre incumbent.
5. Proposition 5.5(i), proof step 3: the right branch maps onto `(0, 1]`; restrict to itineraries
   that are not eventually constant.
6. Proposition 5.4(c), proof: the final `x` splits have two non-straddling children (use
   `nodes = 1 + 2 * internal`); the `y` position is `1 - rho` for `c > 0`.
7. Computations after Proposition 5.5: label the `LP(1,.2)` counts as floating-point, or use the
   exact ones: 167, 547, 1513, 4917, 19537, and 19307 for `a = 0.1999`.

## 8. Commands run

All were run from `research-20260928b/reviews/face-exact-recheck/` with Python 3.13, SciPy 1.18
(HiGHS) and `fractions`. All checks are targeted; no project-wide checks were run, and CI was not
inspected.

| Command | Output | Time |
|---|---|---|
| `python3 kink_exact.py > kink_exact.log` | parts [A]–[H] | 20 s |
| `python3 box_aligned_exact.py > box_aligned_exact.log` | Example 3.12(b) | 1.4 s |
| `python3 path3_quadtree_exact.py > path3_quadtree_exact.log` | Proposition 4.7 | 19 s |
| `python3 conj71_curved.py > conj71_curved.log` | Conjecture 7.1' counterexample | 0.6 s |
| `grep` in the local Tawarmalani–Sahinidis full text | quotation check | – |

## 9. Not checked

- The note's floating-point branch-and-bound tables other than the kink rows. These include the
  `box_aligned` counts, `SCIPdef` and `INC` on other instances, and product-score strong
  branching.
- Propositions 5.6 and 5.7, and every result that the note marks as unchanged.
- An upper bound on `N_opt` for the curved instance of Section 6.3.
