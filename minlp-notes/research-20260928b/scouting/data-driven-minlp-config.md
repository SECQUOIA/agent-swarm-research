# Scout report: data-driven configuration of spatial branch-and-bound (area `data-driven-minlp-config`)

Date: 2026-09-28. Scratch files: `research-20260928b/scouting/data-driven-minlp-config/`.

## Summary

Learning theory for configuring branch-and-bound exists only for MILP. It
covers mixtures of variable-selection scores, cut parameters (Chvátal–Gomory,
GMI, cut-generating functions), node selection and neural-network policies.
Every result assumes one of two things. Either each node has finitely many
possible actions, or the continuous parameter enters only through root cuts.
No searched source (web, arXiv API, local library) gives a sample-complexity,
pseudo-dimension or dispersion result for spatial branch-and-bound (sBB). In
particular none covers its continuous branching point. That point is a real
tunable parameter: SCIP, ANTIGONE, BARON and COUENNE branch at
`clip(lambda*xhat + (1-lambda)*mid, [l+beta*w, u-beta*w])` with default
`lambda` values from 0.25 to 1.00 (Speakman–Lee 2018, Table 1).

First-pass results (details in Section 3):

- **Itinerary doubling (Lemma 1, proved).** Branch at `l + a(u-l)`. As `a`
  ranges over any open interval, the root-to-leaf path containing a fixed
  point `x*` takes `Theta(2^k)` distinct forms at depth `k`. This is the
  mechanism behind exponentially many tree-size pieces in the depth, even
  for a 1-D instance with one parameter. The step from paths to tree-size
  changes is only sketched.
- **Upper bound (Proposition 3, proof sketch).** For 1-D polynomial instances
  with an alphaBB bound, the tree-size function `a -> N(a)` has at most
  `O(m D 2^D)` pieces, where `D = O(log(rho/eps)/log(1/(1-a_min)))`. Hence the
  pseudo-dimension is `O(log(1/eps))`, whatever the tree size or cluster
  effect.
- **Computations.** For nondegenerate minima with second-order bounds, the
  number of constant pieces grows as about `eps^(-1/2)`, that is, by a factor
  of about 3.2 per decade of `eps`. This holds in 1-D (double well, clean
  quadratic model) and in 2-D. It holds for both the pure fraction rule and the
  solver-style `lambda` rule, although the `lambda` rule starts later.
- **Shattering certificate.** Seven 1-D instances are shattered by the
  one-parameter branching-point class, so the pseudo-dimension is at least 7
  for `eps >= 3.2e-9`. All 128 sign patterns were rechecked in exact rational
  arithmetic.
- **Relaxation strength behaves differently.** With nested relaxations, an
  incumbent fixed at `f*` and parameter-independent split geometry, tree size
  is monotone in relaxation strength. The pseudo-dimension is then at most 1
  (Observation 4). The swept `alphaBB` multiplier was monotone in all runs.
- **No grid of branching points is safe (Theorem C, sketch).** For every finite
  set `G` of branching fractions there should be an `(n+1)`-variable
  nonconvex instance on which every `a in G` needs `2^{Omega(n)}` nodes, while
  an open interval of `a` needs 3 nodes. The construction combines a
  disjunctive gadget (verified numerically) with the repository's continuous
  Jeroslow family.

**Honest assessment.** The upper bounds are routine applications of the
Goldberg–Jerrum (GJ) and piecewise-decomposability templates. The lower bounds
and the discretization result follow Balcan et al. (JACM 2024) and Nguyen &
Nguyen (arXiv:2608.17343, Aug 2026), with a new mechanism (itinerary doubling)
specific to continuous splits. On smooth instance distributions the average
tree size is smooth in the parameter, so tuning is statistically easy in
practice. A sibling report (`spatial-bb-theory.md`, unreviewed Theorem A)
suggests that no branching rule beats bisection by more than a
`C_n log(1/eps)` factor in the alphaBB-gap model. That caps the solver value
of learning branching points.

**Recommendation: 3/10.** The direction is feasible and clean, but its
significance for MINLP is low and its originality is only moderate.

## 1. Frontier map

### 1.1 Proved results for MILP (the templates)

**Balcan, Dick, Sandholm, Vitercik, "Learning to branch".** ICML 2018;
extended as JACM 2024, doi 10.1145/3637840. Checked in arXiv:1803.10150v2,
full text.

- *Setting:* B&B on MILPs with `n` binary variables. Variable selection
  maximizes `mu*score1 + (1-mu)*score2`. The cost is tree-constant, for
  example tree size.
- *Lemma 3.3 / Theorem 3.7:* for path-wise scores, `[0,1]` splits into at most
  `2^{n(n-1)/2} n^n` intervals of constant tree, so `Pdim = O(n^2)`.
- *Lemma 3.8 / Theorem 3.9 / Corollary 3.10:* for `d` arbitrary scores and a
  tree cap `kappa`, there are at most `n^{2(kappa+1)}` hyperplanes, so
  `Pdim = O(d kappa log n + d log d)`.
- *Theorem 3.1 (limits of data-independent discretization):* fix
  `1/3 < a < b < 1/2` and even `n >= 6`. There are infinite families of
  distributions with expected size `Omega(2^{(n-9)/4})` for `mu` outside
  `(a,b)` and size `O(1)` almost surely for `mu` inside. This holds for every
  node-selection policy, and the construction uses Jeroslow's instance.

**Balcan, DeBlasio, Dick, Kingsford, Sandholm, Vitercik.** STOC 2021;
arXiv:1908.02894, full text.

- *Theorem 3.3:* if the dual class is `(F,G,k)`-piecewise decomposable, then
  `Pdim = O((d_F* + d_G*) log(d_F* + d_G*) + d_G* log k)`.
- *Theorem 3.6:* this is tight up to logarithmic factors. In particular,
  sequence alignment attains `Omega(log n)` with `n` threshold boundaries.
- *Lemma 3.8:* one-parameter functions with at most `B` oscillations have
  pseudo-dimension `O(ln B)`.

**Balcan, Prasad, Sandholm, Vitercik, tree-search configuration.** NeurIPS
2021; arXiv:2106.04033, full text.

- *Theorem 3.1:* for Chvátal–Gomory cuts, a tiny parameter change moves the
  tree size from constant to `2^{(n-1)/2}`.
- *Theorem 5.2 (generic tree search):* with `kappa` rounds, finite action sets
  `T_j`, and scores linear in the parameters,
  `Pdim = O(d kappa sum_j log T_j + d log d)`.
- *Future work:* GMI and lift-and-project families "would call for new
  techniques".

**Balcan, Prasad, Sandholm, Vitercik, improved bounds.** CP 2022;
arXiv:2111.11207, full text.

- *Theorems 3.4 and 3.5:* for path-wise action and node scores, with depth
  limit `Delta`, `Pdim = O(Delta^2 log k + Delta log b)`. Here `k` and `b` are
  the branching and action-set sizes defined in that paper.
- The bound is polynomial in **depth**, not in node count. The authors call it
  exponentially smaller than the node-count bound.

**Balcan, Prasad, Sandholm, Vitercik, GMI cuts.** NeurIPS 2022;
arXiv:2204.07312, full text.

- *Theorem 4.5:* for a cut `alpha^T x <= beta` added at the root, at most
  `O(14^n (m+2n)^{3n^2} tau^{5n^2})` hypersurfaces of degree `<= 5` partition
  the parameter space into regions of constant tree.
- *Theorem 5.1:* the pseudo-dimension can be infinite if cut parameters depend
  arbitrarily on the instance.
- *Theorem 5.5 (GMI):*
  `Pdim = O(m log(abU) + m n^3 log(m+n) + m n^3 log tau)`.
- *Key distinction (their Section 1.2):* earlier work had "only a finite
  number of states each node ... could be in". GMI parameters create
  infinitely many child problems. Their analysis handles continuous
  parameters that enter **root cuts only**.

**Cheng, Khalife, Fiedorowicz, Basu.** NeurIPS 2024; arXiv:2402.02328
(theorem statements grepped). Pseudo-dimension bounds for neural-network
(sigmoid or ReLU) instance-to-algorithm maps (Theorems 2.5 and 2.6), applied
to branch-and-cut.

**Cheng, Basu.** arXiv:2505.11636, May 2025.

- *Setting:* scoring functions with a `(Gamma, gamma, beta)` piecewise-
  polynomial structure (Definition 3.1), which includes ReLU MLPs. Action sets
  are finite, with `|A_k^s| <= rho_k`.
- *Theorem 3.3:* the cost dual is piecewise constant.
- *Proposition 3.4 (linear policies):* `Pdim = O(W M sum_k log rho_k)`.
- The parameter enters only through action scores. A continuous branching
  point, which changes the child problem itself, is outside the framework.

**Cheng, Basu.** arXiv:2601.23249, Jan 2026 (abstract checked). Local
score-based policies can produce trees exponentially larger than optimal,
through signal misalignment and tie-breaking sensitivity. The paper treats
MILP only.

**Khalife, Lodi.** arXiv:2506.00252, 2025. *Theorem 3.2:* learning CG-cut
weights through a class `F` requires `m = Omega(VCdim(F[n])/eps)` samples,
for both gap-closed and tree-size scores. These are the first quantitative
sample-complexity lower bounds for learning to cut.

**Cheng, Basu.** arXiv:2405.13992, 2024 (abstract). Sample complexity for
choosing cut-generating functions. MILP only.

### 1.2 General frameworks (all MILP-agnostic)

- **Goldberg–Jerrum, refined by Bartlett–Indyk–Wagner** (COLT 2022,
  arXiv:2206.07886, Definitions 3.1–3.2 and Theorem 3.3). If "cost > r" is
  decided by an algorithm using `+,-,*,/` and sign tests, with degree `Delta`
  and predicate complexity `p`, then `Pdim = O(n log(Delta p))` for `n`
  parameters.
- **Balcan, Nguyen, Sharma** (TMLR 2025, arXiv:2409.04367, overview read).
  The Pfaffian GJ framework handles computations involving `exp`, `log` and
  other Pfaffian functions.
- **Nguyen, Nguyen** (arXiv:2608.17343, Aug 2026). *Theorem 5.1:*
  `Pdim = O(p log T_f + p d log(M_f+d) + p d log Delta_f)` for piecewise-
  polynomial losses with an inner minimization, via block elimination.
  *Lemmas 5.2 and 5.3:* matching lower bounds, including `Omega(p log T_f)` in
  the number of pieces. Generic tightness is therefore already available.
- **Recent "provably data-driven" applications to optimization solvers.**
  - PDLP step size and primal weight (Prasad and Sharma, arXiv:2606.08638,
    June 2026).
  - Lagrangian multipliers for MILP, `Theta(s/sqrt N)` (Le, Nguyen, Nguyen,
    arXiv:2605.19052, May 2026).
  - Projection for QP (arXiv:2509.04524).
  - Multiple hyperparameters (arXiv:2602.02406).

  This pipeline is active, so an sBB instance of it is a natural next paper
  for these groups.
- **Known only by title in the arXiv listing:** dispersion (Balcan, Dick,
  Vitercik, arXiv:1711.03091), semi-bandit dispersion (arXiv:1904.09014),
  output-sensitive ERM (arXiv:2204.03569), and A* heuristics (Sakaue, Oki,
  arXiv:2205.09963).

### 1.3 MINLP and sBB: empirical work only

- **Ghaddar et al.** (IJOC 2023; local `ghaddar2023-learning-for-spatial-
  branching-an`). Quantile regression selects a branching rule in RAPOSa's
  RLT-based sBB. No guarantee (grep for "guarantee" and "generaliz": none).
- **González-Rodríguez et al.** (arXiv:2406.03626; local
  `rodriguez2025-learning-in-reformulation-linearization-technique`).
  Imitating strong branching node by node is myopic and weaker than the best
  static rule.
- **Berthold, Geis** (arXiv:2602.09996; local
  `berthold2026-learning-to-choose-branching-rules`). Regression with four
  features chooses between PreferInt and Mixed branching in Xpress. Shifted
  geometric-mean time falls 8–9%, and the model transfers from 9.6 to 9.8.
  No guarantee.
- **Kannan, Nagarajan, Deka** (IJOC 2025, arXiv:2301.00306, full text
  grepped). "Strong partitioning" chooses Alpine partition points by
  max-min. An ML approximation gives 2–4.5x average speedups. There is no
  statistical guarantee; the only guarantees concern the bundle method.
- **Speakman, Lee** (2018; local `speakman2018-on-branching-point-selection-
  for`). Volume-optimal branching points for trilinear hulls. The solver
  branching-point formula `(alpha, beta)` and Table 1 defaults: SCIP
  (1.00, 0.20), ANTIGONE (0.75, 0.10), BARON (0.70, 0.01), COUENNE
  (0.25, 0.20).
- **Gómez-Casares et al.** (arXiv:2403.02823, abstract). Computational study
  of branching-point strategies and bound tightening in RAPOSa, with ML
  selection.
- **González-Rodríguez et al.** (local
  `rodriguez2025-polynomial-optimization-tightening-rlt-based`). ML chooses
  among nine conic strengthenings of RLT, a form of empirical relaxation
  selection.
- **Kimiaei, Kungurtsev, Olimba** (arXiv:2508.06906, survey abstract). Lists
  generalization as an open challenge for ML in exact MINLP solvers.
- **Swisa, Katz** (arXiv:2512.10747, abstract). RL chooses splits in neural
  network verification. Empirical only.

### 1.4 Repository context

- `literature/topics/open-theory-challenges.md` item 5 asks for learned
  branching with a solver-independent guarantee, a safe fallback and
  distribution-shift diagnostics.
- `research-20260922/scouting/scout_literature.md` (Sections 2.8 and 4) and
  `scout_area678_convex_decomp_new.md` (C1) record the gap: there is "no
  sample-complexity theory for continuous branching points".
- `results/spatial-bb-exponential-lower-bound.md` gives a `2^{Omega(n)}`
  lower bound for every coordinate-branching rule and split point. Learning
  cannot help on that family, and I reuse it in Theorem C.
- Sibling scout `spatial-bb-theory.md` (same date): its Theorem A says
  bisection is within `C_n log(1/eps)` of the optimal certificate under a
  two-sided alphaBB gap. It is unreviewed.

### 1.5 Searches run, and what they found

- **WebSearch** (the session budget ran out partway). Queries:
  - sBB sample complexity / pseudo-dimension / branching point;
  - data-driven spatial branching MINLP generalization;
  - Cheng–Basu 2505.11636;
  - branching point pseudo-dimension nonconvex;
  - Pfaffian;
  - Bartlett–Indyk–Wagner;
  - "provably data-driven" global optimization;
  - strong partitioning;
  - "How hard is learning to cut".

  None returned sBB learning theory.
- **arXiv API**:
  - `all:spatial AND branching AND learning` (40 hits; only the three
    empirical papers above are relevant);
  - `abs:"data-driven algorithm design"` (60 hits; all listed above where
    relevant);
  - `abs:"sample complexity" AND abs:"branch-and-bound"` (MILP papers only);
  - `abs:"branching point" AND learning` (nothing relevant);
  - `abs:"global optimization" AND abs:"pseudo-dimension"` (0 hits);
  - `abs:"algorithm configuration" AND (MINLP OR global optimization OR
    nonconvex)` (nothing relevant);
  - learning with OBBT, McCormick, and MINLP plus ML (empirical only).

  An unsuccessful search does not establish novelty. The arXiv API search is
  keyword-based and weak. Venue-only papers (INFORMS, CPAIOR, MPC) may be
  missed.

### 1.6 Why continuous branching points fall outside the templates

MILP analyses rely on a finite set of possible child problems per node. The
parameter only chooses among them. The GMI analysis allows a continuous
parameter to change the node problems, but only through root cuts in an LP
with a fixed tree depth of at most `n`. In sBB the branching fraction `a`
changes **every** node's box. Node endpoints are polynomials of degree
`<= depth` in `a`, and the depth is unbounded as `eps -> 0`. The GJ template
still applies, but three questions remain open: the resulting counts, their
tightness, and how depth rather than node count enters.

## 2. Open questions

**Q1 (tight complexity of the branching-point class).**

Setting:

- sBB on a 1-D polynomial `f` of degree `<= m` on `[0,1]`.
- alphaBB bound `LB(l,u) = min_{[l,u]} f(x) - rho(x-l)(u-x)`, with
  `rho <= rho_max`.
- Oracle or dynamic incumbent, prune if `LB >= UB - eps`.
- Branching at `l + a(u-l)`, with `a` in `[a_min, 1 - a_min]`.

Questions:

- Is `Pdim{Q -> N(Q,a)} = Theta(log(rho_max/eps))` for fixed `a_min`?
- Is the number of pieces `Theta(eps^{-1/2})` at a nondegenerate minimizer?
  More generally, is it `Theta(1/w_eps)`, where `w_eps` is the width below
  which boxes are pruned?
- In `n` dimensions with widest-edge branching, is
  `Pdim = Theta(n log(1/eps))`, up to `log n` factors? The upper bound
  `O(n log(1/eps) log n / a_min)` follows from the GJ template.
- For the solver rule `(lambda, beta)`, are the same statements true? The
  split point then depends on the relaxation minimizer, which is algebraic
  in the parameters.

*Evidence of openness:* the searches in Section 1.5 found no pseudo-dimension
result for sBB. The closest template, Balcan et al. CP 2022, gives
`O(Delta^2 log k + Delta log b)` only for finite action sets.

**Q2 (worst-case discretization versus smoothed dispersion).**

- **(a)** For every finite `G` in `(0,1)`, is there an `(n+1)`-variable
  QCQP-type instance? It should use secant or McCormick relaxations and a
  natural branching rule. Every `a in G` should need `2^{Omega(n)}` nodes,
  while a nonempty open interval of `a` needs `O(1)` nodes. The same question
  applies to the `(lambda, beta)` family.
- **(b)** Suppose the instance data have a density bounded by `K`, for
  example the minimizer locations or the coefficients. Is
  `a -> E N(Q,a)` Lipschitz, or `(w,k)`-dispersed, with constants
  `poly(K, n, log(1/eps), 1/a_min)`? If so, a data-independent grid of
  polynomial size is provably near-optimal. Online tuning would also have
  regret `O~(H sqrt(T log(1/eps)))`.

*Evidence:* part (a) is the continuous analogue of Balcan et al. Theorem 3.1.
I found no sBB version. Part (b) is supported by the experiment in Section
3.6. No dispersion analysis for any B&B tree-size function was found; the
searches covered only the MILP papers listed above.

**Q3 (relaxation-selection and relaxation-strength parameters).**

- **(i)** Take nested relaxations, an incumbent fixed at `f*` and
  parameter-independent branching geometry. Then tree size is monotone in
  strength (Observation 4, proved below).
- **(ii)** With a dynamic incumbent, or with split points at the relaxation
  solution as in all four solvers above, when does monotonicity fail?
- **(iii)** What is the pseudo-dimension of joint (relaxation choice,
  `lambda`, `beta`) policies when node bounds come from SDP relaxations?
  These are algebraic, not rational. Semi-algebraic elimination (Basu–
  Pollack–Roy, as in arXiv:2608.17343) should give a polynomial bound, but no
  one has written it for sBB.

The statistical part is routine. The hard part of repository item 3, a
cost-aware theory of when strength pays, is optimization structure rather
than sample complexity.

**Q4 (a statistical lower bound for learning, not only for uniform
convergence).**

- Is there a family of instance distributions on which any learner needs
  `Omega(log(1/eps)/eps'^2)` samples to find a branching fraction whose
  expected normalized tree size is `eps'`-optimal? This would be a
  fat-shattering lower bound at a scale comparable to the oscillation
  amplitude.
- *Obstacle:* in Section 3 the oscillation amplitude is `O(1)` nodes against
  trees of size `Theta(log(1/eps))`. A scale-sensitive lower bound would need
  larger oscillations. These probably require `n`-dimensional,
  cluster-effect instances.

## 3. First-pass mathematics for Q1, with Q2(a) as a companion

### 3.1 Model

- Branching at `l + a(u-l)` sends the child boxes of `[l,u]` to relative
  lengths `a` (L) and `1-a` (R).
- Each word `w` in `{L,R}^k` has a box `[l_w(a), u_w(a)]`. Its endpoints are
  polynomials in `a` of degree `<= k` with integer coefficients, and they
  **do not depend on the rest of the tree**.
- The tree `T(a)` is the set of words all of whose proper prefixes are
  *expanded*, meaning not pruned.

### 3.2 Lemma 1 (itinerary doubling) — proved

Fix `x* in (0,1)`. Define `x_0 = x*` and `x_{k+1} = S_a(x_k)`, where
`S_a(x) = x/a` if `x < a` (digit L) and `S_a(x) = (x-a)/(1-a)` otherwise
(digit R). Then the depth-`k` box containing `x*` is the box of the word
formed by the first `k` digits.

1. On any `a`-interval where the first `k` digits are fixed, `x_k(a)` is
   continuous and strictly decreasing, for `k >= 1`.
   - L-step derivative: `(x_k' a - x_k)/a^2 < 0`.
   - R-step derivative: `(x_k'(1-a) - (1-x_k))/(1-a)^2 < 0`.
   - Both use `x_k' <= 0` and `x_k in (0,1)`.
2. A breakpoint of digit `j` is a point where `x_{j-1}(a) = a`.
   - Just left of it, digit `j` is R and `x_j -> 0+`. All later digits are
     L, and `x_k -> 0+`.
   - Just right of it, digit `j` is L and `x_j -> 1-`. All later digits are
     R, and `x_k -> 1-`.
3. Let `J` be a maximal interval with a constant `k`-prefix whose two
   endpoints are breakpoints. Then `x_k` decreases from 1 to 0 on `J`.
   - `x_k(a) - a` is strictly decreasing, from `1 - a_left > 0` to
     `-a_right < 0`.
   - So digit `k+1` has exactly one breakpoint in `J`, and `J` splits into
     two intervals of the same kind.
4. `|x_{k+1}'| >= |x_k'|/max(a, 1-a)`. So all depth-`k` intervals have
   length `O((1-a_min)^k)`.
5. Any open `a`-interval `I` therefore contains an interior depth-`k0`
   interval with `k0 = O(log(1/|I|)/log(1/(1-a_min)))`.

*Conclusion:* `I` contains at least `2^{k-k0}` distinct depth-`k` words for
`x*`. Numerically, for `x* = pi/10` and `a in [0.2, 0.8]`, the counts are
2, 3, 6, 12, 24, 47, 94, 186, 371, 741, … That is `3*2^{k-2}` up to rounding,
until the grid saturates (`itinerary.py`).

*Consequence, and its limits.* By Lemma 2, the path to `x*` is always expanded
while the box half-width exceeds `sqrt((1+rho)eps)/rho`. So the geometry of
the tree near `x*` passes through at least
`c * eps^{-log 2/(2 log(1/a_min))}` distinct itineraries.

Distinct itineraries do **not** immediately give distinct word-sets. When
`x*` crosses a shared endpoint, both adjacent boxes are usually expanded on
both sides. The word-set changes when a neighbor box crosses the Lemma 2
hyperbola.

*Sketch.* Inside an interior depth-`k` interval `J`, `x_k` sweeps from 1 to
0. Near the left end, the right neighbor `B+` of the `x*`-box `B` touches
`x*` and is expanded if its half-width is above threshold. Near the right
end, `B+` is at distance about `2 r_B` from `x*`. It is pruned when
`sqrt(1+rho) < 1 + 2 r_B/r_{B+}`, which holds, for example, for `rho = 2`
and comparable widths.

So each interior interval should contain at least one change in tree size.
This is the mechanism behind the observed piece counts. Writing it out is
part of step 2 in Section 3.8.

### 3.3 Lemma 2 (closed form in a clean model) — proved, and checked on 20,000 random boxes

- Take `f(x) = (x - x*)^2` with a fixed alphaBB shift `rho > 0`. This is a
  valid but conservative shift, as when `rho` is computed once on a larger
  box.
- For a box with center `m` and half-width `r`, let `d = m - x*`. If
  `|d| <= (1+rho) r`, then `LB = rho d^2/(1+rho) - rho r^2`.
- With the incumbent fixed at `f* = 0`, a node is expanded **iff**
  `r^2 - d^2/(1+rho) > eps/rho`.
- *Proof.* Minimize the convex quadratic `(x-x*)^2 - rho(x-l)(u-x)`. The
  stationary point is `(x* + rho m)/(1+rho)`. When
  `|d| > (1+rho) r`, the bound is attained at an endpoint and is at least 0,
  so the node is pruned, consistent with the criterion.
- The tree is the set of words whose proper prefixes all lie above this
  hyperbola in the `(m, r)` plane.

### 3.4 Proposition 3 (upper bound) — proof sketch, nothing beyond standard tools

- **Depth.** `LB >= f* - rho w^2/4`, so boxes of width
  `w <= w_eps = 2 sqrt(eps/rho)` are pruned. Depth-`k` widths are at most
  `(1-a_min)^k`. So every expanded node has depth
  `< D := log(1/w_eps)/log(1/(1-a_min))`.
- **Sign changes of one word.** Set
  `P_w(a, x) = f(x) - rho(x - l_w)(u_w - x) - f* + eps`. Its degree is `m` in
  `x` and `<= max(m, 2)|w|` in `a`. The expansion predicate `E_w(a)` means
  `min over x in [l_w, u_w] of P_w < 0`. It can change only where the
  minimum is 0. That happens at an endpoint (degree `<= m|w|` in `a`) or at a
  root of `Res_x(P_w, dP_w/dx)(a)` (degree `O(m|w|)`). Degenerate identically
  zero resultants are handled by perturbing `eps`.
- **Pieces.** `T(a)` is determined by the values `E_w(a)` for `|w| < D`. So
  there are at most `1 + sum_{|w|<D} O(m|w|) = O(m D 2^D)` pieces, and
  `Pdim <= D + O(log(m D))`.
  - For `a_min = 1/2 - delta` this is `(1/2) log2(rho/(4 eps)) (1+O(delta))`.
  - The bound does **not** depend on tree size, so cluster effects do not
    enter. This mirrors the depth-based CP 2022 bound for MILP.
- **Dynamic incumbent.** Best-first order adds pairwise comparisons: at most
  `4^{D+1}` pairs, each with `poly(m) D` sign changes. This gives
  `Pdim <= 2D + O(log(mD))` (sketch).
- **`n` dimensions** with widest-edge branching and LP (McCormick/RLT)
  bounds:
  - words range over `[n] x {L,R}`, and width comparisons are polynomial
    tests;
  - LP values are piecewise rational, with `<= C(M, n')` bases;
  - the result is `Pdim = O(D_n log n + n' log M)` per parameter, with
    `D_n <= n D`.

  This is a routine GJ-template bound.

### 3.5 Observation 4 (relaxation strength) — proved, folklore level

Assume:

- nested bounds, `LB_t(B)` nonincreasing in `t` for every box `B`;
- the incumbent fixed at `f*`;
- split geometry that does not depend on `t`.

Then the expanded set of words is monotone in `t`, so `N(Q,t)` is monotone.
Monotone dual functions give pseudo-dimension `<= 1`: two threshold
functions of `t` cannot realize the pattern (0,1). This contrasts with Q1,
where the pseudo-dimension grows as `log(1/eps)`.

Computation (`sbb1d.c`, rule 3, dynamic incumbent): the alphaBB multiplier
`t in [1,4]` gave a nondecreasing tree size with 9/11/13 pieces for
`eps = 1e-4/1e-6/1e-8`.

### 3.6 Computations (`results-summary.txt` holds all numbers)

**Instances and conventions.**

- Tilted double well: `16(x-.2)^2(x-.75)^2 + .05x`. The alphaBB `rho` is
  computed on the root box. Oracle incumbent. `a` ranges over `[0.2, 0.8]`.
- Piece counts were checked on a 10x finer grid. They are exact where they
  agree and lower bounds otherwise.

**Piece counts by tolerance.**

| eps | pieces, 1-D double well | pieces, 1-D clean model | pieces, 2-D (`P1(x)+P2(y)+0.5xy`) | max tree size (1-D / 2-D) |
|---|---|---|---|---|
| 1e-3 | 53 | 54 | 337 | 29 / 109 |
| 1e-4 | 172 | 192 | 1088 | 41 / 141 |
| 1e-5 | 545 | 595 | 3547 | 49 / 173 |
| 1e-6 | 1710 | 1902 | ≈11150 | 53 / 203 |
| 1e-7 | ≈5810 | 6278 | ≈35200 | 65 / 245 |
| 1e-8 | ≈17060 | 19132 | — | 75 / — |

- Each column grows by about 3.2 per decade, which is `eps^{-1/2}` and
  proportional to `1/w_eps`.
- This is exponential in tree size and depth, and polynomial in `1/eps`.
- The tree size itself takes only 14–74 distinct values.

**Other variants.**

- *Dynamic incumbent with best-first order:* essentially the same counts
  (170, 530, 1655, 5734 for `eps = 1e-4` to `1e-7`).
- *Box-dependent `rho`:* at most 17 pieces for all `eps`. The bound becomes
  exact once the box is in the convex basin, so the tree is finite and
  independent of `eps`.
- *Solver rule* (sweep `lambda`, `beta = 0.1`): 3, 5, 9, 17, 50, 123, 350,
  961, 2621, 7634 pieces for `eps = 1e-3` to `1e-12`. The growth factor
  reaches about 2.7–2.9 per decade later than under the pure fraction rule,
  and the trees are shallower (maximum depth 17 versus 43 at `eps = 1e-10`).

**Numerical pitfall (2-D).** Widest-edge ties recur *identically in `a`*.
Both coordinates are split by the same fractions, so equal widths reappear.
Without a relative tie tolerance, floating-point rounding decides the ties.
The run then produced about 270,000 spurious pieces on a 2M grid. Any
ERM-by-enumeration for sBB must handle such structural ties.

**Shattering certificate** (`shatter.py`, `verify_shatter.py`).

- Clean model, `rho = 2`, `a in [0.4, 0.6]`, grid of 4,000,001 points.
- Greedy search found 7 shattered instances. Their `(x*, eps, threshold)`
  triples are listed in `results-summary.txt`; `eps` runs from `10^-1.5` to
  `10^-8.5`, adding about one instance per decade.
- All 128 patterns were re-verified with exact `Fraction` arithmetic. So
  `Pdim >= 7` holds rigorously for this model class.

**Distribution experiment.**

- Setup: 2000 random double wells, `eps = 1e-6`.
- *Pure fraction rule:* about 1041 pieces per instance on a 3001-point grid.
  Yet the mean tree size is a smooth bowl: 35.4 at `a = 0.2`, minimum
  25.59 at `a = 0.504`, 35.6 at `a = 0.8`. The largest jump between adjacent
  grid points is 0.13. Split-sample overfitting is negligible
  (25.674 versus 25.606 at the test optimum).
- *Solver rule:* `lambda = 1` gives 19.0 versus 25.65 at the midpoint.
  - With `lambda = 1`, `beta <= 0.15` gives 19.0.
  - `beta = 0.2` (SCIP-like) gives 19.22.
  - `lambda = 0.25` (COUENNE's value, here with `beta = 0.1`) gives about
    23.5.
  - So tuning matters by about 0–25% depending on the default, on this toy
    distribution.

### 3.7 Theorem C sketch (no finite grid of branching points is safe) — gadget verified, composition not yet written out

**Gadget.**

- Variable `y in [0,1]`.
- Convex constraint `y in [a', b']`.
- Reverse-convex constraint `-(y-a)(y-b) <= 0`, that is, `y <= a` or
  `y >= b`, with `a < a' < b' < b`. So the gadget is infeasible.
- With secant relaxations, the root is relaxation-feasible. After one split
  at `theta`, both children are infeasible iff `theta` lies in an interval
  `G_good`. Its endpoints are algebraic in `(a,b,a',b')`.

Numerical `G_good` values (`gadget.py`):

- `(0.3,0.7,0.45,0.55)`: `(0.4667, 0.5333)`;
- `(0.2,0.8,0.36,0.70)`: `(0.5333, 0.5556)`;
- `(0.2,0.8,0.365,0.705)`: `(0.5424, 0.5616)`;
- `(0.2,0.8,0.30,0.70)`: empty.

By continuity `G_good` can be made nonempty and arbitrarily short. Its
location moves continuously, so it can be placed in a gap of any finite grid
`G`.

**Composition.**

- Add the continuous Jeroslow feasibility block: `x_i(1-x_i) <= 0` and
  `sum x_i = n/2` with `n` odd.
- Under secants, one split of `x_i` at any point fixes `x_i` to 0 or 1 in the
  relaxation. The sum is not an integer, so some free `x_i` is always
  fractional and hence violated.
- The relaxation stays feasible while at most `(n-1)/2` variables are fixed
  to each value. So every child where `y` is not resolved roots a Jeroslow
  tree with `2^{Omega(n)}` nodes.
- The rule is: branch on the widest variable whose nonconvex constraint is
  violated, with `y` winning root ties.
  - If `a in G_good`, the tree has 3 nodes.
  - Otherwise `y`'s width drops to `max(a, 1-a) < 1`. Width-1 violated
    `x_i` are then chosen, and the tree is `2^{Omega(n)}`.

*Missing:*

- a written proof of the placement claim, which needs explicit formulas for
  the endpoints of `G_good`;
- a check that the width-based rule never returns to `y` before the Jeroslow
  block forces exponential size;
- a check of the `(lambda, beta)` variant.

A single instance suffices; no mixture distribution is needed as in Balcan
et al.

### 3.8 Attack plan and difficulty

1. **Formalize Proposition 3 and its `n`-dimensional GJ version** for LP
   bounds. *Risk:* low. *Effort:* days.
2. **Prove `Pdim = Omega(log(1/eps))` in 1-D.**
   - Restrict `a` to `[1/2 - delta, 1/2 + delta]` with `delta ~ 1/N`, so
     depth-`k` widths agree within constant factors for `k <= N/delta`.
   - Use Lemma 1's nested splits and Lemma 2's hyperbola criterion. Show
     that a single threshold `r_i` splits every pattern cell of the previous
     instances.
   - The greedy search used a different `x*` per instance, which suggests
     that decorrelating instances matters.
   - *Risk:* medium, because uniformity of `r_i` across cells is the crux.
     *Effort:* 1–2 weeks.
3. **Show pieces are `Theta(1/w_eps)` at nondegenerate minima.** This refines
   the `2^D` count. *Risk:* medium to high; it needs control of which words
   ever lie near the hyperbola boundary.
4. **Write out Theorem C and the `(lambda, beta)` version.** *Risk:* low.
5. **Q2(b) dispersion under smoothed minimizer locations.** Estimate the
   density of level-`k` breakpoints from `|dx_k/da|` versus `|dx_k/dx*|`.
   *Risk:* medium.
6. **Real-solver check.** Sweep SCIP's `branching/midpull` and
   `branching/clamp`, or an equivalent, on a MINLPLib family. This measures
   actual tuning gains. It is decisive for significance and was not done
   here.

## 4. Significance

**Proved here, or checked exactly:**

- Lemma 1: `Theta(2^k)` itineraries of `x*` (distinct paths, not yet distinct tree sizes).
- Lemma 2: the closed-form criterion.
- Observation 4: monotonicity, hence `Pdim <= 1`, for nested relaxation
  strength.
- The exact-arithmetic certificate `Pdim >= 7` for the 1-D branching-point
  class.

**Sketch-level, likely provable:**

- Proposition 3: `Pdim = O(log(1/eps))` in 1-D; GJ-type polynomial bounds in
  `n` dimensions for branching points, relaxation-selection weights,
  bound-tightening frequency and alphaBB scaling.
- Theorem C: failure of every finite grid of branching points.

These establish that continuous sBB parameters are PAC-learnable with
polynomial samples. The branching point needs a precision-dependent sample
size, which MILP variable selection does not.

**Plausible:**

- tight `Theta(log(1/eps))` pseudo-dimension;
- `Theta(eps^{-1/2})` pieces at nondegenerate minima;
- dispersion under smoothed instance distributions, which would justify
  coarse grid tuning of `(lambda, beta)`.

**Speculative:** solver gains.

- The toy experiments show 0–25% node reductions from tuning `(lambda, beta)`
  relative to published defaults.
- The sibling Theorem A (unreviewed) caps gains over bisection at
  `C_n log(1/eps)` in the alphaBB-gap model.
- Learned components never affect validity; clamping `beta > 0` keeps
  exhaustiveness. So the "safe fallback" of repository item 5 is automatic
  and not a research question.

**Needed for practical value:**

- measured tuning gains on a real solver and instance family;
- robustness across formulations and solver versions (item 5), which this
  theory does not address;
- handling of structural ties and floating-point effects.

## 5. Recommendation

The area gives a tidy paper: the first sample-complexity and structure
results for configuring spatial branch-and-bound. It would contain an
itinerary-doubling mechanism, a precision-dependent `Theta(log(1/eps))`
pseudo-dimension for the branching point, a monotone contrast for relaxation
strength, and a "no safe grid" theorem. Feasibility is high: most pieces are
proved or sketched here, with exact computational support.

It is, however, largely an application of mature templates. These are
GJ/Pfaffian bounds, piecewise decomposability with generic tight lower bounds
(arXiv:2608.17343), and the Balcan et al. discretization gadget. A group
already publishing "provably data-driven" solver papers could produce it
quickly.

Its consequences for MINLP solvers are weak. Smooth instance distributions
make tuning statistically easy. Worst-case gains over bisection appear to be
at most logarithmic in `1/eps`. The theory says nothing about the real
bottleneck of item 5, which is transfer across formulations and solvers.

I would not make this a flagship direction. If pursued, keep it to a short
note, steps 1, 2 and 4 of Section 3.8. A real-solver sweep (step 6) should
come first to confirm that the parameter matters.

**Score: 3/10** (significance 3, feasibility 8, originality 4).

## Appendix: local commands run (targeted; no project-wide checks, no CI)

All commands ran under `research-20260928b/scouting/data-driven-minlp-config/`.

- **Build:**
  - `gcc -O2 -o sbb1d sbb1d.c -lm`
  - `gcc -O2 -o sbb2d sbb2d.c -lm`
  - `gcc -O2 -o quadmodel quadmodel.c`
  - `quadmodel_bin.c`, compiled the same way
- **1-D sweeps:**
  - `[FIXEDRHO=1] ./sbb1d c0..c4 eps mode rule lo hi N [extra]`, over
    `eps = 1e-2` to `1e-12`
  - modes: oracle and dynamic incumbent
  - rules 0–3; grids of 2e5 and 2e6 points
- **2-D sweeps:** `./sbb2d P1 P2 0.5 eps 0 0.2 0.8 N` for `eps = 1e-2` to
  `1e-7`, on grids of 2e5 and 2e6 points. Sweeps were rerun after the
  tie-tolerance fix.
- **Distribution experiment:** 2000 instances via
  `xargs -P 34 ... ./sbb1d ...` for rules 0, 1 and 2.
- **Python scripts:**
  - `python3 itinerary.py`
  - `python3 gadget.py`
  - `python3 shatter.py` (7 instances found)
  - `python3 verify_shatter.py` (128/128 patterns exact)
  - a check of Lemma 2 on 20,000 random boxes (0 mismatches)
- **Raw sweep outputs** (1.8 GB) were deleted after being summarized in
  `results-summary.txt`. The binaries were also removed and must be rebuilt
  before rerunning `shatter.py` and `verify_shatter.py`, which call
  `./quadmodel_bin`.
- **Sources:** `src/*.txt` holds pdftotext extracts of the arXiv papers
  examined.

Files:

- `research-20260928b/scouting/data-driven-minlp-config.md` (this report)
- `research-20260928b/scouting/data-driven-minlp-config/results-summary.txt`
- `sbb1d.c`, `sbb2d.c`, `quadmodel.c`, `quadmodel_bin.c`, `itinerary.py`,
  `gadget.py`, `shatter.py`, `verify_shatter.py`, `analyze.py`, `arxivq.sh`
