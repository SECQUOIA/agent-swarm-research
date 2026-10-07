# Decomposition certificates for spatial branch-and-bound: complexity and an exponential separation

Date: 2026-09-29. Workstream 2 (Theory A) of the
[program](../PROGRAM.md). Status: **reviewed, revised and rechecked.**
An independent review ([`reviews/decomposition-review.md`](../reviews/decomposition-review.md))
checked every proof and found them correct; a recheck
([`reviews/decomposition-recheck.md`](../reviews/decomposition-recheck.md))
confirmed the revision and asked for four small fixes. A check of the
computations centred at a non-dyadic `x*`
([`reviews/decomposition-nondyadic-check.md`](../reviews/decomposition-nondyadic-check.md))
found two table entries to correct (Section 8.2). A confirmation
([`reviews/decomposition-nondyadic-confirm-r1.md`](../reviews/decomposition-nondyadic-confirm-r1.md))
found Section 8.2 correct apart from two wording errors, fixed in
Section 8.3. A second confirmation
([`reviews/decomposition-nondyadic-confirm-r2.md`](../reviews/decomposition-nondyadic-confirm-r2.md))
found Section 8.3 correct apart from one misstatement about the first
confirmation's count, fixed in Section 8.4. A third confirmation
([`reviews/decomposition-nondyadic-confirm-r3.md`](../reviews/decomposition-nondyadic-confirm-r3.md))
checked Section 8.4; its one wording point was applied by the root. Section 8
lists all changes; the fixes of Section 8.1 (including the base-rounding
correction and the scope of Observation 4.2) have not been rechecked. An
adaptive algorithm that does not know `x*` is now proved in
[`extension-adaptive.md`](extension-adaptive.md) (Theorem A.5; Section 8.5). Proofs are complete
where the status table says "proved". Computations are floating-point
illustrations, not certified counts. Scripts and logs are in this directory.

Notation and results from the constrained note
([`instance-dependent-node-complexity.md`](../../research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md),
cited as "[C]") are used without change: `a_i`, `q_B`, `w(B)`, `Q(x, r)`,
`N_inf`, Theorem 3.1 and Theorem 6.3 of [C].

## Summary

The question is whether spatial branch-and-bound (B&B) that follows a tree
decomposition of the factor hypergraph can be exponentially cheaper than
single-tree spatial B&B that uses **the same per-factor relaxations**, on
problems with a unique nondegenerate global minimizer.

Main results (all for `F = sum_c f_c` on a box, factors of bounded arity):

1. **Model (Section 1).** A decomposition certificate consists of cells on
   every separator box, an affine minorant of the subtree value function on
   each cell, and a local cover of each bag box by leaves. Each leaf carries a
   convex relaxation that combines the bag's factor relaxations with convex
   minorants of the children's cell minorants. Validity is checked leaf by
   leaf by convex programs (Lemma 1.3). Size is the number of leaves plus
   cells. The natural algorithm is a dynamic program over the tree whose
   affine child bounds are Lagrangian bounds for the copy constraints of the
   separator variables (Section 1.5).
2. **Instance-dependent upper bound (Theorem 3.4).** Assume quadratic growth
   `F - f* >= c_g |x - x*|^2` on the box, factors with `M_a`-Lipschitz
   gradients, and relaxations with vertex-vanishing error (U^q) (alphaBB,
   McCormick). Use slopes equal to the gradient, at `x*`, of the sum of the
   factors in each subtree, and cells and leaves whose widths grow in
   proportion to the distance from `x*`. Then the certificate has root bound
   `>= f* - eps` and size `O(|T| (C k sqrt(K_1 (1+Delta) w) M_a/c_g)^{w+1} log(|T|/eps))`,
   where `k` bounds the number of bags containing a variable and `Delta` the
   number of children (`k = 2`, `Delta = 1`, `K_1 = 1` for paths).
   No smoothness of value functions is used, cells far from the optimum are
   handled by the same argument, the center may be off by `h`, and
   multipliers with total error `O(sqrt(eps))` suffice. The condition on the
   width ratio `theta` does not depend on `n`, but it is real: computations
   show that above a threshold the copy error repeats in every bag and the
   root gap grows linearly in `n` (Remark 3.6).
3. **Why slopes matter (Proposition 2.6).** With constant child minorants
   (zero slopes), a separator whose optimal multiplier is `lambda* != 0`
   needs at least `|lambda*|/(6 sqrt(M_F eps))` cells. This is the first-order
   copy error, now as a lower bound on certificate size.
4. **Single-tree lower bound (Corollary 2.1).** On the path family
   `F_n(x) = sum_i (x_i^2 - kappa x_i^4) + b sum_i x_i x_{i+1}` on `[-1,1]^n`
   (unique nondegenerate minimizer 0), every single-tree certificate with
   alphaBB on the bilinear factors has at least
   `0.068 sqrt(n) (2e/pi)^{n/2} log(0.2/(n eps))` leaves for `b = 0.8`,
   `kappa <= 1/6`. The general threshold: growth is exponential when the
   geometric mean of the per-variable alphaBB weights exceeds
   `pi/(4e) ≈ 0.289` times the geometric mean of the Hessian eigenvalues.
   The face-exact note's Theorem 1 (imported) applies to the same
   relaxation and to termwise McCormick and gives at least `0.57 (5/3)^n`
   leaves for `eps <= 1e-4`, without the `log(1/eps)` factor.
5. **Separation (Theorem 4.1).** On the same family with the same
   termwise relaxations (each bilinear term relaxed alone, by alphaBB or
   McCormick), decomposition certificates of size `O(n log(n/eps))` exist;
   with alphaBB every certificate for the path decomposition needs
   `Omega(n log(1/eps))` leaves. With alphaBB, for every `eps <= 1e-4` the
   ratio of the proven single-tree bound to the proven decomposition bound is
   at least `3e-10 (2e/pi)^{n/2}/sqrt(n)` (`(2e/pi)^{1/2} = 1.3154892`); with McCormick it is at least
   `c (5/3)^n/(n log(n/eps))`, exponential for each `eps` but not uniformly
   as `eps -> 0`.
   The constant from the proof is large (about `3.4e7`). Computed
   certificates have about `3.1e3` leaves per bag per halving of `h`; the
   proven single-tree bound overtakes them from `n = 29` (`eps = 1e-6`), and
   a toy bisection tree with the same relaxation already exceeds them at
   `n = 9` (199,240 against 198,446 leaves, `eps = 1e-4`; Section 5.4).
6. **Lower bounds in the width (Section 2).** A bag lemma transfers the
   integral and covering lower bounds of [C] to each bag. Consequences:
   `exp(Omega(w)) log(1/eps)` leaves at nondegenerate minima (disjoint
   blocks of size `w+1`) when the relaxation gap is large enough,
   `alpha/lambda_geo > pi/(4e)` (below that threshold this route gives no
   exponential), and `v (n/(w+1))^{1+(w+1)/2} (c alpha/eps)^{(w+1)/2}`
   leaves for flat blocks, for **every** tree decomposition of width `w`.
   The flat bound also shows that the `n^{Theta(w)}` factor from splitting
   the tolerance across bags is necessary.
7. **Worst case (Theorem 3.3).** With zero slopes and a uniform grid of
   side `h = min(eps/(4(k-1)G|T|), sqrt(2 eps/(alpha' A |T|)))`, size
   `2|T| ceil(s0/h)^{w+1}`, where `G` is a Lipschitz constant of the bag
   functions: of the form
   `(C n/eps)^{O(w)}`, like Zhang–Sun's bound for nested decomposition. It is
   not new in substance; under ETH a bound `poly(n) g(w, eps)` with a
   polynomial independent of `w` is false for absolute accuracy (literature
   audit, C2).

8. **Dependence on the factorization (Section 4.1).** The proved
   single-tree mechanism belongs to one factorization: bilinear terms relaxed
   alone. Merging the unary terms into the bilinear factors ("balanced
   split") removes it (Corollary 2.1 base 0.930, or exact near `x*`); a toy
   single tree then loses its `eps`-dependence but still grows about
   2.3–2.5 times per variable, with no proof (open). With arbitrary
   functional splits no lower bound can hold uniformly for relaxations that
   are exact at factor minima (such as convex envelopes): splitting by the
   conditional margins of Lemma 1.1 makes per-factor envelopes exact at the
   root, so one node (single tree) or `2|T| - 1` members (decomposition)
   suffice (Observation 4.2). This says nothing about a fixed rule such as
   alphaBB or about restricted split classes.

**Significance.** Theorem 3.4 is the main new result: a certificate-size
bound for recursive decomposition-aware spatial B&B at a unique minimizer,
with no regularity of value functions, explicit control of copy drift along
chains, and inexact centers and multipliers. The separation (Theorem 4.1) is
rigorous but relative to a fixed termwise relaxation and factorization; it is
a clean version of the cluster effect of termwise relaxations, removed by
paying relaxation error per bag. SCIP's default PSD-minor cuts escape both
single-tree bounds, so the theorem does not explain the program's SCIP
counts. The decomposition side is an existence result centered at `x*`; an
algorithm that finds such certificates without knowing `x*` is proved in
[`extension-adaptive.md`](extension-adaptive.md) (Theorem A.5), with size
`O(|T| (C sqrt|T|)^{w+1} log(|T|/eps))`; matching Theorem 3.4 without `x*`
remains open.

Not proved: a two-sided characterization of the decomposition certificate
size by covering numbers of bag projections of near-optimal sets (only the
lower half, Theorem 2.5, is proved; see [`extension-adaptive.md`](extension-adaptive.md),
Part B, for the later results); an adaptive algorithm that does not know `x*`
and matches Theorem 3.4 (Section 3.4 sketches one; Theorem A.5 of the
extension proves the weaker size `O(|T| (C sqrt|T|)^{w+1} log(|T|/eps))`);
improvement of the worst-case
exponent from `w+1` to `(w+1)/2`.

## Status

| Item | Content | Status |
|---|---|---|
| Lemma 1.1 | DP margin identity `F - f* = sum_t g_t` | proved |
| Lemma 1.3 | validity of decomposition certificates (also when pairs of boxes that only touch are omitted; remark after the lemma) | proved |
| Lemma 1.4 | chain inequality | proved |
| Lemma 1.5 | unfolding: root bound = Lagrangian over configurations | proved |
| Corollary 2.1 | single-tree lower bound on the path family, explicit constants | proved |
| Lemma 2.2 | bag lemma (integral form) | proved |
| Proposition 2.3 | `exp(Omega(w))` at nondegenerate minima, when `alpha/lambda_geo > pi/(4e)` | proved |
| Proposition 2.4 | flat blocks: `eps^{-(w+1)/2}` and tolerance-splitting factor | proved |
| Theorem 2.5 | covering lower bound on bag projections | proved |
| Proposition 2.6 | constant minorants need `Omega(eps^{-1/2})` cells | proved for a child of the root with a 1D separator; general case sketched |
| Lemma 3.1 | shell partitions | proved |
| Lemma 3.2 | telescoping identity for slopes | proved |
| Theorem 3.3 | worst case `(C n/eps)^{O(w)}` | proved |
| Theorem 3.4 | instance-dependent `O(\|T\| C^{w+1} log(\|T\|/eps))` under (QG) | proved |
| Remark 3.5 | inexact center (sup-norm `h_0 = O(sqrt(eps/\|T\|))`) and multipliers | proved (perturbation term in Theorem 3.4); corrected after review |
| Remark 3.6 | copy drift above the `theta` threshold accumulates along the chain | observed numerically (Section 5.4, and the review's `b` sweep); mechanism explained |
| Section 3.4 | adaptive algorithm without knowledge of `x*` | sketched only here; an algorithm with size `O(\|T\| (C sqrt\|T\|)^{w+1} log(\|T\|/eps))` is proved in `extension-adaptive.md` (Theorem A.5); matching Theorem 3.4 without `x*` remains open |
| Conjecture 3.7 | two-sided covering characterization | conjecture |
| Theorem 4.1 | separation on the path family (termwise alphaBB or McCormick), ratio `>= 3e-10 (2e/pi)^{n/2}/sqrt(n)` for `eps <= 1e-4` | proved; second term of (a) imported from the face-exact note, Theorem 1 |
| Section 4.1 | balanced split: exponential single-tree growth without `eps`-dependence | observed in the review's toy B&B only; open |
| Observation 4.2 | arbitrary splits make per-factor envelopes exact at the root (size 1, or `2\|T\| - 1` for decomposition certificates) | proved; measure form classical (Vorob'ev 1962; Lasserre 2006) |

## 1. Model

### 1.1 Problem, tree decomposition, value functions

- `X0 = prod_{i=1}^n [L_i, U_i]`, side `s0 = max_i (U_i - L_i)`.
- `F(x) = sum_{c in C} f_c(x_c)`, where each factor `c` is a subset of `[n]`
  (its scope) and `f_c` is continuous on `X0_c`. `f* = min_{X0} F`,
  `m = F - f*`, `E(eta) = {x in X0 : m(x) <= eta}`.
- A **rooted tree decomposition** `(T, {V_t})` of the factor hypergraph: a
  rooted tree `T` with root `r`, bags `V_t subset [n]` covering `[n]`, every
  scope contained in some bag, and for every variable `i` the set
  `T_i = {t : i in V_t}` is a subtree (running intersection). Width
  `w = max_t |V_t| - 1`. We assume that no bag is contained in its parent
  (such bags can be merged into the parent), so `|S_t| <= w`. Each factor is
  assigned to one bag containing its
  scope; `a_t(x_{V_t}) = sum_{c assigned to t} f_c(x_c)`, so
  `F(x) = sum_t a_t(x_{V_t})`.
- `p(t)` is the parent of `t != r`, `ch(t)` the children, `sub(t)` the subtree
  rooted at `t`. The **separator** is `S_t = V_t ∩ V_{p(t)}` (`S_r = ∅`), and
  `R_t = V_t \ S_t`. `W_t = union_{s in sub(t)} V_s`.
- Parameters: `k = max_i |T_i|` (the largest number of bags containing one
  variable), `Delta = max_t |ch(t)|`. For the path decomposition of a path
  (bags `{i, i+1}`), `k = 2` and `Delta = 1`.
- Running intersection gives two facts used below. A variable of `W_t \ S_t`
  appears only in bags of `sub(t)`. A variable of `V_t` that appears in a bag
  outside `sub(t)` lies in `S_t`.

The **subtree value function** of `t` is

```
phi_t(s) = min { sum_{u in sub(t)} a_u(x_{V_u}) : x in X0_{W_t}, x_{S_t} = s },   s in X0_{S_t}.
```

By the running intersection property it satisfies the dynamic programming
(DP) recursion `phi_t(s) = min_{y in X0_{R_t}} G_t(s, y)` with the **local
objective** `G_t(z) = a_t(z) + sum_{u in ch(t)} phi_u(z_{S_u})` for
`z in X0_{V_t}`, and `phi_r = f*`. Define the **conditional margin**
`g_t(z) = G_t(z) - phi_t(z_{S_t}) >= 0`.

**Lemma 1.1 (DP margin identity).** For every `x in X0`,
`m(x) = sum_t g_t(x_{V_t})`.

*Proof.* `sum_t g_t = sum_t a_t + sum_t sum_{u in ch(t)} phi_u(x_{S_u}) - sum_t phi_t(x_{S_t})`.
Every `u != r` appears once in the middle sum (through its parent) and once in
the last sum, so the two cancel except for `phi_r = f*`. □

The lemma is not used in the proofs below; it shows how the global margin
splits into nonnegative local margins, one per bag.

### 1.2 Relaxations and hypotheses

A **per-factor relaxation** assigns to each factor `c` and each box `B_c`
(in the coordinates of `c`) a convex function `f_{c,B}` on `B_c` with
`f_{c,B} <= f_c` there. The single-tree node bound on a box `B` is
`LB(B) = min_B sum_c f_{c,B_c}`, as in [C, Section 1.2] and the program's
shared model.

- **(U^q_{alpha'})** per factor: `f_c(z) - f_{c,B}(z) <= alpha' q_{B_c}(z)`
  for all boxes and `z in B_c`. Since `q_{B_c} <= |c| w(B)^2/4`, the error of
  bag `t` on a box `B` is at most `alpha' A_t w(B)^2/4` with
  `A_t = sum_{c assigned to t, c relaxed} |c|` and `A = max_t A_t`.
  Per-factor alphaBB with parameter `alpha_c` satisfies this with
  `alpha' = max alpha_c`; McCormick envelopes of `b x_i x_j` satisfy it with
  `alpha' = |b|/2` ([C, Lemma 1.1]). Convex factors kept exact contribute 0.
- **(G_alpha)** per-factor gap: `f_c(z) - f_{c,B}(z) >= sum_{i in c} alpha_{c,i} a_i^{B}(z)`.
  Exact alphaBB `f_{c,B} = f_c - alpha_c q_{B_c}` has
  `alpha_{c,i} = alpha_c`. McCormick does not satisfy (G) for any positive
  weights ([C, Lemma 1.1]).
- **(QG)** quadratic growth: `m(x) >= c_g |x - x*|_2^2` on `X0` for some
  `x* in X0` and `c_g > 0`. It holds when the global minimizer is unique and
  satisfies second-order sufficient conditions (interior: `∇^2 F(x*) ≻ 0`),
  by compactness; it also holds at a unique vertex or face minimizer with
  linear growth, with `c_g` divided by the diameter.
- **(L^{1,1})** each `a_t` is `C^1` on a neighbourhood of `X0_{V_t}` and
  `∇ a_t` is `M_a`-Lipschitz in the Euclidean norm on `X0_{V_t}`.

### 1.3 Decomposition certificates

Boxes below are closed, axis-parallel and nondegenerate. For a box `B` in
the coordinates `V_t`, `B_S` is its projection onto coordinates `S`.

**Definition 1.2 (decomposition certificate).** Fix a rooted tree
decomposition with factor assignment and a per-factor relaxation. A
decomposition certificate consists of:

1. for every `t != r`, a finite family `P_t` of boxes (**cells**) with
   pairwise disjoint interiors covering `X0_{S_t}`, and for every cell `D` an
   affine function `l_{t,D}(s) = lambda_{t,D}^T s + beta_{t,D}`
   (the **cell minorant**); for the root, a number `l_r`;
2. for every `t`, a finite family `L_t` of boxes (**local leaves**) with
   pairwise disjoint interiors covering `X0_{V_t}`;
3. for every leaf `B in L_t` and child `u in ch(t)`, a convex function
   `psi_{u,B}` on `B_{S_u}` (the **child bound**) with

   ```
   (CM)   psi_{u,B}(s) <= l_{u,D'}(s)   for every D' in P_u and every s in B_{S_u} ∩ D';
   ```

such that, with the **leaf relaxation**
`Rel_{t,B}(z) = sum_{c assigned to t} f_{c,B_c}(z_c) + sum_{u in ch(t)} psi_{u,B}(z_{S_u})`,

```
(LC)   Rel_{t,B}(z) >= l_{t,D}(z_{S_t})   for every B in L_t, every D in P_t with D ∩ B_{S_t} ≠ ∅,
                                           and every z in B with z_{S_t} in D,
```

and at the root `Rel_{r,B}(z) >= l_r` for all `B in L_r`, `z in B`. The
certificate **proves tolerance `eps`** if `l_r >= f* - eps` (in practice
`l_r >= UBD - eps` for an incumbent value `UBD >= f*`).

Its **size** is `sum_t |L_t| + sum_{t != r} |P_t|`. In all constructions
below `|P_t| <= |L_t|`, so size and number of leaves agree within a factor 2.

*Remarks on the definition.*

- *Checking.* For affine `l_{t,D}` and convex `Rel_{t,B}`, (LC) for one pair
  `(B, D)` is one convex program over the box `B ∩ (D x R^{R_t})`. For affine
  `psi_{u,B}`, (CM) is a finite set of affine inequalities on boxes, checked
  at vertices. A leaf may meet several cells of its own separator and of its
  children's separators. This is what keeps the leaf count linear in
  `log(1/eps)` in Theorem 3.4; requiring each leaf to lie in one cell of each
  child would force product partitions and `log^2(1/eps)` leaves. The price
  is in the checks: (LC) takes one convex program per (leaf, cell) pair, and
  for shell certificates the pairs are 3–5 times the leaves at the tested
  `h` and their ratio grows like `log(1/h)` (Section 4, "What is counted").
- *Slopes.* Constant minorants are the case `lambda_{t,D} = 0`. The
  constructions of Section 3 use one slope `lambda_t` per separator and the
  child bound `psi_{u,B}(s) = lambda_u^T s + min{beta_{u,D'} : D' in P_u, D' ∩ B_{S_u} ≠ ∅}`,
  which satisfies (CM).
- *Single tree as a special case.* One bag `V_r = [n]` gives exactly the
  single-tree certificates of [C, Section 1.3] with `N_opt = |L_r|`.

### 1.4 Validity

**Lemma 1.3 (validity).** If (CM) and (LC) hold, then
`l_{t,D}(s) <= phi_t(s)` for every `t != r`, `D in P_t` and `s in D`, and
`l_r <= f*`.

*Proof.* Induction from the leaves of `T` upwards. Let `s in D in P_t`.
Choose `y` attaining `phi_t(s) = G_t(s, y)` (a minimum of a continuous
function on a compact set) and put `z = (s, y)`. Some leaf `B in L_t`
contains `z`, and `D ∩ B_{S_t}` contains `s`, so (LC) applies to `(B, D, z)`.
For each child `u`, `z_{S_u}` lies in some cell `D' in P_u`; (CM) and the
induction hypothesis give `psi_{u,B}(z_{S_u}) <= l_{u,D'}(z_{S_u}) <= phi_u(z_{S_u})`.
With `f_{c,B} <= f_c`,
`l_{t,D}(s) <= Rel_{t,B}(z) <= a_t(z) + sum_u phi_u(z_{S_u}) = G_t(z) = phi_t(s)`.
The root is the same with no separator. □

So a certificate proving tolerance `eps` certifies `f* >= l_r >= UBD - eps`.

*Touching pairs.* The proof needs (LC) only for pairs `(B, D)` whose
interiors meet in the separator coordinates, `int B_{S_t} ∩ int D ≠ ∅`, and
(CM) only for cells `D'` with `int B_{S_u} ∩ int D' ≠ ∅`. Given `z = (s, y)`
with `s in D`, take points `z_k -> z` of `X0_{V_t}` with
`(z_k)_{S_t} in int D`, each in the interior of some leaf (leaf interiors are
dense). Some leaf `B` contains infinitely many of them. It is closed, so it
contains `z`, and `int B_{S_t}` meets `int D`. The child cell `D' ∋ z_{S_u}`
is chosen in the same way from points of `int B_{S_u}`. So if a computation
omits only pairs of boxes that touch, its bounds are still valid, but its
`beta` values and `l_r` can be higher than those of Lemma 1.5. Definition 1.2
is not changed, and the lower bounds of Section 2 use it as stated. Section 5
uses this remark.

**Lemma 1.4 (chain inequality).** Under (CM) and (LC), for every `x in X0`
there are leaves `B_t in L_t` with `x_{V_t} in B_t` for all `t`, such that

```
l_r <= sum_t sum_{c assigned to t} f_{c,(B_t)_c}(x_c).
```

Consequently, under (G), `m(x) + (f* - l_r) >= sum_t sum_{c at t} sum_{i in c} alpha_{c,i} a_i^{B_t}(x)`.

*Proof.* Top-down. At the root choose `B_r ∋ x_{V_r}`; then
`l_r <= Rel_{r,B_r}(x)`. At a node `t` reached with a cell `D_t ∋ x_{S_t}`
that meets `(B_{p(t)})_{S_t}` (both contain `x_{S_t}`), choose
`B_t ∋ x_{V_t}`; then `D_t ∩ (B_t)_{S_t} ∋ x_{S_t}`, so (LC) gives
`l_{t,D_t}(x_{S_t}) <= Rel_{t,B_t}(x)`. In `Rel_{p,B_p}(x)` bound each child
term by (CM): `psi_{t,B_p}(x_{S_t}) <= l_{t,D_t}(x_{S_t})` for a cell
`D_t ∋ x_{S_t}`. Substituting recursively gives the first claim. The second
follows from `f_{c,B} <= f_c - sum_i alpha_{c,i} a_i^B`. □

Lemma 1.4 says that a decomposition certificate implicitly defines, for each
`x`, a "virtual box" `{x' : x'_{V_t} in B_t for all t}` on which the
single-tree validity inequality of [C, (V)] holds. The number of virtual
boxes can be exponential in `n` while the certificate is small; this is the
source of the separation.

**Lemma 1.5 (unfolding).** Suppose one slope `lambda_t` per separator is
used, `psi_{u,B}` as in the remark above, and each `beta_{t,D}` is chosen as
large as (LC) allows:
`beta_{t,D} = min { Rel_{t,B}(z) - lambda_t^T z_{S_t} : B in L_t, B_{S_t} ∩ D ≠ ∅, z in B, z_{S_t} in D }`,
and `l_r = min_{B in L_r} min_B Rel_{r,B}`. A **configuration** is a choice,
for every `t`, of a leaf `B_t in L_t` and a point `z^t in B_t`, and for every
`t != r` of a cell `D_t in P_t` with `z^t_{S_t} in D_t` and
`D_t ∩ (B_{p(t)})_{S_t} ≠ ∅`. Then

```
l_r = min over configurations of  sum_t sum_{c at t} f_{c,B_t}(z^t_c) + sum_{t != r} lambda_t^T (z^{p(t)}_{S_t} - z^t_{S_t}).
```

*Proof.* Substitute the definition of `beta` into `Rel` recursively. A
minimum of a sum of independent minima is the minimum over joint choices. □

This is a Lagrangian relaxation of the copy constraints
`z^t_{S_t} = z^{p(t)}_{S_t}`: the copies are decoupled except that both lie
in, or next to, the same cell, and `lambda_t` is the multiplier.

### 1.5 The algorithm

**Fixed-slope decomposition B&B.**

1. *Incumbent and slopes.* Compute a local minimizer `x̂` (for example by a
   local NLP solver) and `UBD = F(x̂)`. Set
   `lambda_t = ∇_{S_t} (sum_{s in sub(t)} a_s)(x̂)`, the gradient with
   respect to the separator variables of the factors below the separator. At
   an interior nondegenerate `x̂` this is the multiplier of the copy
   constraint of `S_t` in the local solve, and equals `∇ phi_t(x̂_{S_t})`
   when `phi_t` is differentiable there.
2. *Partitions.* Choose cells `P_t` and leaves `L_t` (Section 3 uses shells
   around `x̂` whose widths grow linearly with the distance).
3. *Bottom-up pass.* In post-order, compute `beta_{t,D}` by the convex
   programs of Lemma 1.5, one per pair `(B, D)` with `B_{S_t} ∩ D ≠ ∅`.
4. *Root.* If `l_r >= UBD - eps`, stop: the certificate proves tolerance
   `eps` (Lemma 1.3). Otherwise the minimizing configuration identifies, for
   every bag, the leaf and cell that attain the bound; refine those (split
   them), improve `x̂` if a better point was found, and repeat step 3 on the
   ancestors of the refined bags.

*Precursor.* Berenguel, Casado, García, Hendrix and Messine (J. Glob.
Optim. 56(3):1101–1121, 2013) proposed this algorithm in a special case:
subfunctions that share one common variable (a star with one separator),
interval bounds instead of convex relaxations, one interval B&B list per
subfunction with a copy of the common variable, and combined bounds that
take, for each other list, the smallest bound among its boxes whose
common-variable interval meets the current one (their Theorem 2). That is
the copy relaxation with zero slopes and implicit cells. Their results are
bound-validity and pruning rules; they give no complexity bound, lower
bound or separation (read in full by the recheck,
`reviews/decomposition-recheck.md`, Section 4).

Step 4 is the analogue of best-first node selection. Only the certificate
sizes (existence of small certificates) are analysed below; the number of
refinement rounds of step 4 is not (Section 3.4).

### 1.6 Integer separator variables

Let some variables be integer: `X0_i = {L_i, ..., U_i}`. Boxes become
products of intervals intersected with the integer lattice in the integer
coordinates, and each relaxation `f_{c,B}` is taken on the continuous hull
of `B_c`. Lemmas 1.3–1.5 hold unchanged, because their proofs only evaluate
functions at domain points, and a cell of `P_t` may fix an integer separator
variable to a single value ("exact fixing"). In Lemma 1.5 the minimum over
`z in B` is over the continuous hull of `B`, so configurations range over
continuous hulls; this is what the drift bounds of Section 3 use. For integer separator variables
fixed in every cell of `P_t` and in every leaf of `L_{p(t)}`, the drift
terms of Section 3 vanish in those coordinates: `z^t_i = z^{p(t)}_i` for
every configuration. The counts of Section 3 then gain a factor
`prod_{i in S_t, i integer} (U_i - L_i + 1)` per separator (and per parent
bag), with no dependence on `eps` from those coordinates.

## 2. Lower bounds

### 2.1 Single tree: the path family

The anisotropic form of [C, Theorem 3.1] (remark after its proof): if every
member `C` of a family covering `X0` satisfies
`m(y) + eps >= sum_j alpha_j a_j^C(y)` on `C`, then
`|P| >= (n/pi^2)^{n/2} (prod_j alpha_j)^{1/2} ∫_{X0} (m + eps)^{-n/2}`.
(AM–GM gives `sum_j alpha_j a_j >= n (prod_j alpha_j a_j)^{1/n}`, and each
arcsine integral equals `pi`.) Under (G) with per-factor alphaBB, a
single-tree certificate satisfies this with `alpha_j = sum_{c ∋ j} alpha_c`,
since `LB(C) <= F_C(y) = F(y) - sum_c alpha_c q_{C_c}(y)`. By [C, Lemma 2.1]
the same holds for the leaf-and-piece family of any B&B run with
same-relaxation bound tightening.

**Corollary 2.1 (single-tree lower bound at a nondegenerate minimizer).**
Assume per-factor alphaBB with per-variable weights `alpha_j`, and
`m(x) <= (1/2)(x - x*)^T H (x - x*)` on `X0` with `H ≻ 0`. Let
`r_in = min_i min(x*_i - L_i, U_i - x*_i)` and `R^2 = lambda_min(H) r_in^2/2`.
Then every single-tree certificate at tolerance `eps` has

```
|P| >= 2 (2n/pi)^{n/2} (prod_j alpha_j / det H)^{1/2} Gamma(n/2)^{-1} J_n(R/sqrt(eps)),
J_n(T) = ∫_0^T t^{n-1} (1+t^2)^{-n/2} dt >= (e^{-1/2}/2) log(T^2/n)   for T^2 >= n.
```

As `eps -> 0`, `J_n(R/sqrt eps) = (1/2) log(1/eps) + O_n(1)`, and by
Stirling the bound is
`(1 + o(1)) sqrt(n/pi) (4e/pi)^{n/2} (alpha_geo/lambda_geo)^{n/2} (1/2) log(1/eps)`,
with `alpha_geo = (prod alpha_j)^{1/n}` and `lambda_geo = (det H)^{1/n}`. The
bound grows exponentially in `n` iff `alpha_geo/lambda_geo > pi/(4e) ≈ 0.2890`.
(The program's "about 0.58 times the Hessian scale" uses the rate-table
convention `m ≈ gamma |y|^2` of [C, Section 3.8], that is `gamma = lambda/2`.)

*Proof.* The ellipsoid `{(1/2)(x-x*)^T H (x-x*) <= R^2}` lies in the
Euclidean ball of radius `r_in` around `x*`, hence in `X0`. Restrict the
integral to it and substitute `x = x* + sqrt(2) H^{-1/2} y`:
`dx = 2^{n/2} (det H)^{-1/2} dy`, and the integrand becomes
`(|y|^2 + eps)^{-n/2}`. Polar coordinates give
`|S^{n-1}| ∫_0^R r^{n-1} (r^2+eps)^{-n/2} dr = (2 pi^{n/2}/Gamma(n/2)) J_n(R/sqrt eps)`.
Multiply by `(n/pi^2)^{n/2} (prod alpha_j)^{1/2}`. For the bound on `J_n`:
for `t >= sqrt n`, `(1 + t^{-2})^{-n/2} >= e^{-n/(2t^2)} >= e^{-1/2}`, so
`J_n(T) >= e^{-1/2} ∫_{sqrt n}^T dt/t`. □

**The path family.** For `n >= 2`, `kappa in [0, 1/6]` and
`0 < |b| < 1 - kappa`, let `X0 = [-1,1]^n` and

```
F_n(x) = sum_{i=1}^n phi(x_i) + b sum_{i=1}^{n-1} x_i x_{i+1},     phi(t) = t^2 - kappa t^4.
```

Factors: the unary factors `phi(x_i)` and the bilinear factors
`b x_i x_{i+1}`. This is the program's probe (`scratch/probe3.py`) with the
linear terms removed (`c = 0`). Facts:

- `phi'' = 2 - 12 kappa t^2 >= 0` on `[-1,1]`, so the unary factors are
  convex and are kept exact.
- *Growth.* `x_i^4 <= x_i^2` and `2|x_i x_{i+1}| <= x_i^2 + x_{i+1}^2` give
  `F_n(x) >= (1 - kappa - |b|) |x|^2`. So `x* = 0` is the unique global
  minimizer, `f* = 0`, and (QG) holds with `c_g = 1 - kappa - |b|`.
- *Upper quadratic.* `F_n(x) <= sum x_i^2 + b sum x_i x_{i+1} = (1/2) x^T H x`
  with `H = tridiag(b, 2, b)`. So the hypothesis of Corollary 2.1 holds on
  all of `X0`, with `r_in = 1`.
- *Nonconvexity.* For `kappa = 0.1`, `b = 0.8` and `n >= 3`, the Hessian at
  `(1, ..., 1)` is `tridiag(0.8, 0.8, 0.8)`, which has the negative
  eigenvalue `0.8 - 1.6 cos(pi/(n+1))`. So `F_n` is not convex.
- *Relaxation.* The Hessian of `b x_i x_{i+1}` is constant with eigenvalues
  `±|b|`, so alphaBB needs `alpha = |b|/2` on every box, whatever
  box-dependent rule computes it (interval Hessians included). Hence
  `alpha_j = |b|` for `2 <= j <= n-1` and `alpha_1 = alpha_n = |b|/2`, and
  `prod_j alpha_j = |b|^n/4`.
- *Determinant.* With `cosh theta_b = 1/|b|`,
  `det H = |b|^n sinh((n+1) theta_b)/sinh(theta_b)`, and
  `lambda_min(H) = 2 - 2|b| cos(pi/(n+1)) >= 2(1 - |b|)`.
  So `lambda_geo -> |b| e^{theta_b} = 1 + sqrt(1 - b^2)`, and the growth
  condition of Corollary 2.1 reads `|b|/(1 + sqrt(1-b^2)) > pi/(4e)`, that is
  `|b| > 0.5333` (numerically; Section 5).
- *Explicit constants for `b = 0.8`.* `theta_b = ln 2`, `sinh theta_b = 3/4`,
  `det H <= (4/3) 1.6^n`, `R^2 >= 0.2`. With
  `Gamma(n/2) <= sqrt(4 pi/n) (n/(2e))^{n/2} e^{1/(6n)}`, for
  `eps <= 0.2/n`:

  ```
  N_single(eps) >= 0.068 sqrt(n) (2e/pi)^{n/2} log(0.2/(n eps)),     (2e/pi)^{1/2} ≈ 1.31549.
  ```

  (Computation: `2 (2n/pi)^{n/2} 0.5^{n/2} (3/16)^{1/2} (n/(4pi))^{1/2} (2e/n)^{n/2} e^{-1/(6n)} (e^{-1/2}/2) = 0.0741 e^{-1/(6n)} sqrt n (2e/pi)^{n/2}`, and `e^{-1/12} > 0.92`.)
  The exact integral bound is evaluated in Section 5.

The lower bound covers every single-tree run in the sense of [C, Lemma 2.1]:
any adaptive branching, node order, valid incumbent, and bound tightening
that uses the same relaxation. Corollary 2.1 itself needs the alphaBB gap
in every coordinate and does not cover McCormick relaxations of the bilinear
factors, which are face-exact. The face-exact note's Theorem 1 (workstream
Theory B) does: it needs only a gap of at least `|b| d_i d_{i+1}` per
bilinear term (its hypothesis (M_b)), which both termwise McCormick and the
alphaBB relaxation above satisfy, and gives at least
`(5/3)^n exp(-(5/9)(1 + 1.25 eps))` leaves on this family, with a larger base
but no `log(1/eps)` factor (Theorem 4.1(a)). Neither bound covers relaxations
of aggregated expressions (for example convexity detection on the whole
quadratic part), PSD or SDP cuts, or other factorizations of the objective
(Section 4.1).

### 2.2 The bag lemma

**Lemma 2.2 (bag lemma, integral form).** Let a decomposition certificate
prove tolerance `eps`. Let `t` be a bag, `K subset V_t` with `|K| = kk`, and
`alpha_i > 0` (`i in K`) such that for every box `B`,
`sum_{c at t} (f_c - f_{c,B_c}) >= sum_{i in K} alpha_i a_i^B` on `B`. Then
for every `x̄ in X0`

```
|L_t| >= (kk/pi^2)^{kk/2} (prod_{i in K} alpha_i)^{1/2} ∫_{X0_K} (m(x̄_{-K}, y) + eps)^{-kk/2} dy.
```

*Proof.* For `y in X0_K` put `x = (x̄_{-K}, y)`. Lemma 1.4 gives a leaf
`B in L_t` with `x_{V_t} in B` and, dropping all other (nonnegative) gap
terms, `m(x) + eps >= sum_{i in K} alpha_i a_i^B(y)`. Hence
`(m(x) + eps)^{-kk/2} <= sum_{B in L_t : y in B_K} (sum_{i in K} alpha_i a_i^B(y))^{-kk/2}`
for every `y`. Integrate over `X0_K`; each term contributes at most
`(pi^2/kk)^{kk/2} (prod alpha_i)^{-1/2}` by AM–GM and the arcsine integral. □

The lemma holds for every tree decomposition and every factor assignment. It
counts leaves of one bag; separator cells are not needed for it, because the
leaves of a bag cover the whole bag box, separator coordinates included.

### 2.3 Exponential dependence on the width at nondegenerate minima

**Proposition 2.3.** Let `d = w + 1` and `n = K d`. Split `[n]` into `K`
blocks of size `d` and let `F(x) = sum_{k=1}^K g(x^{(k)})`, one factor per
block, on `X0 = ([-1,1]^d)^K`. Assume `g - g* <= (1/2)(y - y*)^T H_g (y - y*)`
on `[-1,1]^d` with `H_g ≻ 0`, and a relaxation of `g` with gap
`>= alpha q_B` (for example exact alphaBB). Then for **every** tree
decomposition of width `w` and every certificate proving tolerance `eps`,

```
size >= K * [bound of Corollary 2.1 with n := d, alpha_j := alpha, H := H_g].
```

In particular the size is at least
`c K sqrt(d) (4e alpha/(pi lambda_geo(H_g)))^{d/2} log(1/eps)` for small
`eps`, exponential in `w` when `alpha/lambda_geo(H_g) > pi/(4e)`.

*Proof.* Each block is the scope of a factor, so some bag contains it; that
bag has at most `d` variables, so it equals the block. The factor of block
`k` is assigned to that bag `t_k`, and the `t_k` are distinct. Apply
Lemma 2.2 at `t_k` with `K = ` block `k` and `x̄ = x*`: then
`m(x̄_{-K}, y) = g(y) - g*`, and the integral is bounded as in
Corollary 2.1. Sum over `k`. □

The instance is separable, so a solver with component detection would split
it. The point is only that no decomposition certificate avoids the
single-tree cost inside a bag: exponential dependence on `w` is necessary in
this model at nondegenerate minima. For matching upper bounds see
Theorem 3.4, whose base is `(C M_a/c_g)^{w+1}`.

### 2.4 Flat blocks: `eps^{-(w+1)/2}` and the cost of splitting the tolerance

**Proposition 2.4.** Let `d = w + 1`, `n = K d`, `X0 = ([0,1]^d)^K`, and
`F(x) = sum_k g(x^{(k)})` with one factor per block. Assume `g = g*` on a
box `R_g subset [0,1]^d` of volume `v > 0`, and a relaxation of `g` with gap
`>= alpha q_B`. Then for every tree decomposition of width `w` and every
certificate proving tolerance `eps`,

```
size >= v K (alpha d K/(4 (d+2) eps))^{d/2}.
```

*Proof.* As in Proposition 2.3 the block factors sit in distinct bags `t_k`
with `V_{t_k} = ` block `k`; let `N_k = |L_{t_k}|`.
1. For `x in R := R_g^K`, `m(x) = 0`. Lemma 1.4 gives
   `eps >= alpha sum_k Q_k(x^{(k)})`, where
   `Q_k(y) = min { q_B(y) : B in L_{t_k}, y in B }` (a measurable function:
   a minimum of finitely many continuous functions on closed sets).
2. `q_B(y) <= s` forces `d_i(y)^2 <= a_i(y) <= s` for all `i`, so `y` lies
   within sup-distance `sqrt s` of a vertex of `B`; inside `B` this set has
   volume at most `2^d s^{d/2}`. For `y` uniform on `R_g`,
   `P(Q_k(y) <= s) <= N_k 2^d s^{d/2}/v`.
3. With `s_0 = (v/(2^d N_k))^{2/d}`,
   `E[Q_k] >= ∫_0^{s_0} (1 - N_k 2^d s^{d/2}/v) ds = s_0 d/(d+2) = d v^{2/d}/(4 (d+2) N_k^{2/d})`.
4. Averaging step 1 over `x` uniform on `R`:
   `eps >= (alpha d v^{2/d}/(4(d+2))) sum_k N_k^{-2/d}`. By convexity of
   `N -> N^{-2/d}`, `sum_k N_k^{-2/d} >= K (sum_k N_k/K)^{-2/d}`. Solve for
   `sum_k N_k`. □

*Remarks.*
- The bound is tight in `K` and `eps`, up to factors `C^d` (of the order
  of `((d+2) alpha'/alpha)^{d/2}/v`), for this family: bags equal to blocks,
  no separators, and a uniform grid of side `h` in each block with
  `K alpha' d h^2/4 <= eps` give `K ceil(1/h)^d` leaves.
- In terms of `n`: `size >= v (n/d)^{1 + d/2} (alpha d/(4(d+2) eps))^{d/2}`.
  The factor `n^{d/2}` beyond the number of bags is the price of splitting
  the tolerance `eps` among `K` independent bags. So a bound
  `poly(n) (C/eps)^{O(w)}` with the degree of the polynomial independent of
  `w` is impossible in this model for absolute accuracy. This matches the
  literature audit's ETH remark (C2), here unconditionally and for
  certificate size.
- A single tree on the same instance needs at least
  `(alpha n/pi^2)^{n/2} v^K eps^{-n/2}` leaves ([C, Theorem 3.1]).

### 2.5 Covering form on bag projections

**Theorem 2.5.** Let a certificate prove tolerance `eps`, and for each bag
`t` let `K_t subset V_t` be a set of coordinates on which the factors at `t`
have gap `>= alpha sum_{i in K_t} a_i^B` on every box. Then for every
`eta >= 0`,

```
size >= sum_t |L_t| >= sum_t 2^{-|K_t|} N_inf( pi_{K_t}(E(eta)), 2 sqrt((eps + eta)/alpha) ).
```

*Proof.* For `x in E(eta)`, Lemma 1.4 gives leaves `B_t ∋ x_{V_t}` with
`alpha sum_t sum_{i in K_t} a_i^{B_t}(x) <= eta + eps`. Hence for each `t`
and `i in K_t`, `d_i(x) <= sqrt((eps+eta)/alpha)` in `B_t`, and `x_{K_t}` lies
in the cube of side `2 sqrt((eps+eta)/alpha)` around a vertex of
`(B_t)_{K_t}`. The `2^{|K_t|} |L_t|` such cubes cover `pi_{K_t}(E(eta))`. □

This is the bag-projection analogue of [C, Theorem 4.6]. It gives each bag
the whole tolerance `eps`. Proposition 2.4 shows that the budget must in
fact be shared; a lower bound that shares it in general (not only for
products) is open.

### 2.6 Constant minorants cluster on separators

**Proposition 2.6.** Let `t` be a child of the root with a one-dimensional
separator `S_t = {i}`, and suppose all minorants on `P_t` are constant.
Assume `x*` is the unique global minimizer, interior, `F` is `C^2` with
`||∇^2 F|| <= M_F` on `X0`, and `phi_t` is `C^1` on
`I = [s* - rho_0, s* + rho_0]` (`s* = x*_i`) with `|phi_t'| >= |lambda*|/2`
there, where `lambda* = phi_t'(s*) != 0`. If
`eps < min(lambda*^2/(36 M_F), M_F rho_0^2/4)`, every certificate proving
tolerance `eps` has `|P_t| >= |lambda*|/(6 sqrt(M_F eps))`.

*Proof.* Let `r_1 = sqrt(eps/M_F)`, so `2 r_1 <= rho_0`.
1. Take a root leaf `B` and `z in B`, and a cell `D in P_t` containing
   `z_i`. By (LC) at the root, (CM), and Lemma 1.3 for the other children,
   `f* - eps <= a_r(z) + sum_{u != t} phi_u(z_{S_u}) + beta_{t,D}`, and
   `beta_{t,D} <= min_D phi_t` (Lemma 1.3 at `t`). So
   `phi_t(z_i) - min_D phi_t <= eps + G_r(z) - f*`.
2. For `s in D` take `z = (x* + (s - s*) e_i)_{V_r}`. Then
   `G_r(z) <= F(x* + (s-s*) e_i) <= f* + (M_F/2)(s-s*)^2`, because
   `∇F(x*) = 0`. So `phi_t(s) - min_D phi_t <= eps + (M_F/2)(s-s*)^2` for all
   `s in D`.
3. Let `D` meet `J = [s*, s* + r_1]` and let `D'` be its intersection with
   the window `[s* - r_1, s* + 2 r_1] subset I`; `D'` is an interval of length
   at least `min(w(D), r_1)`. On `D'`, `phi_t` is monotone with slope at least
   `|lambda*|/2` in absolute value, so step 2 at the maximizer of `phi_t` on
   `D'` gives `|lambda*| len(D')/2 <= eps + 2 M_F r_1^2 = 3 eps`.
4. If `w(D) >= r_1`, then `r_1 <= 6 eps/|lambda*|`, which contradicts
   `eps < lambda*^2/(36 M_F)`. So every cell meeting `J` has width at most
   `6 eps/|lambda*|`, and at least `r_1 |lambda*|/(6 eps)` of them are needed
   to cover `J`. □

At an interior nondegenerate unique minimizer, `phi_t` is `C^2` near `s*` by
the implicit function theorem (the subtree problem has the unique
nondegenerate minimizer `x*_{W_t \ S_t}` given `s*`), so the hypothesis on
`phi_t` holds for some `rho_0 > 0` whenever `lambda* != 0`. For deeper nodes
the same argument applies to the minimizing chain once one shows that the
root slack `f* - l_r` bounds the sum of the slacks along it; this is
**sketched only**. With the slope `lambda_t = lambda*` the count drops to
`O(log(1/eps))` (Theorem 3.4). This is Robertson–Cheng–Scott's order
distinction (first-order constant bounds, second-order Lagrangian bounds;
literature audit, C2), now as a lower bound on certificate size.

## 3. Upper bounds

### 3.1 Shell partitions and the telescoping identity

**Lemma 3.1 (shell partition).** Let `X` be a box in `R^kk` with sides at
most `s0`, `p in X`, `h > 0`, and `theta = 2^{-mu}` with an integer
`mu >= 0`. Let `J = max(0, ceil(log2(s0/h)))`. There is a partition
`Pi(p; h, theta)` of `X` into at most `(J+1)(4/theta)^kk` boxes with
pairwise disjoint interiors such that every member `B` satisfies
`w(B) <= max(h, theta dist_inf(B, p)) <= h + theta dist_inf(B, p)`.

*Proof.* Split `Q(p, h)` into the `2^kk` cubes of side `h` with vertex `p`.
For `j = 1..J`, lay the grid of side `g_j = theta 2^{j-1} h` on
`Q(p, 2^j h)`, anchored at its lower corner; it has `4/theta` cells per axis,
and the boundary of `Q(p, 2^{j-1} h)` lies on grid lines because
`2^{j-1} h/g_j = 1/theta` is an integer. Keep the grid cells not contained in
`Q(p, 2^{j-1} h)`; their interiors miss that cube, so their sup-distance to
`p` is at least `2^{j-1} h`, and their side is `g_j <= theta dist_inf`. The
kept cells of all levels tile `Q(p, 2^J h)`, which contains `X` because
`2^J h >= s0`. Intersect with `X` and drop degenerate pieces; clipping
decreases widths and increases distances. Each level contributes at most
`(4/theta)^kk` pieces and the central cube `2^kk <= (4/theta)^kk`. □

**Lemma 3.2 (telescoping identity).** For each variable `i` let `top(i)` be
the root of the subtree `T_i`. Given a configuration (Lemma 1.5), define the
**consistent point** `x in X0` by `x_i = z^{top(i)}_i`. For a point
`x° in X0` define the slopes

```
lambda_t(x°) = ∇_{S_t} ( sum_{s in sub(t)} a_s )(x°),     that is   lambda_{t,i} = sum_{s in sub(t) ∩ T_i} ∂_i a_s(x°_{V_s}).
```

Then `sum_t ∇a_t(x°_{V_t})^T (z^t - x_{V_t}) = sum_{t != r} lambda_t(x°)^T (z^t_{S_t} - z^{p(t)}_{S_t})`.

*Proof.* Fix `i`. For `t in T_i`, `z^t_i - x_i` telescopes along the path
from `t` up to `top(i)`: it is the sum of `z^u_i - z^{p(u)}_i` over the
nodes `u != top(i)` on that path. The nodes `u in T_i \ {top(i)}` are
exactly those with `i in S_u`, and `u` lies on the path from `t` iff
`t in sub(u)`. Exchange the sums:
`sum_{t in T_i} ∂_i a_t(x°) (z^t_i - x_i) = sum_{u : i in S_u} (z^u_i - z^{p(u)}_i) sum_{t in sub(u) ∩ T_i} ∂_i a_t(x°)`.
Sum over `i`. □

At an interior nondegenerate `x°`, `lambda_t(x°)` is the multiplier of the
copy constraint of `S_t` and equals `∇ phi_t(x°_{S_t})` (envelope theorem).
The proofs below use only the definition.

Combining Lemma 3.2 with Lemma 1.5: for slopes `lambda_t = lambda_t(x*)`,
the Lagrangian value of a configuration, with exact factors, is

```
Phi(config) = sum_t a_t(z^t) - sum_{t != r} lambda_t^T (z^t_{S_t} - z^{p(t)}_{S_t})
            = F(x) + sum_t [ a_t(z^t) - a_t(x_{V_t}) - ∇a_t(x*_{V_t})^T (z^t - x_{V_t}) ].      (3.1)
```

`z^t` and `x_{V_t}` differ only in the coordinates `S_t` (the others have
`top(i) = t`). Each bracket is a first-order Taylor remainder, except that
the gradient is taken at `x*` instead of `x`.

### 3.2 Worst case

**Theorem 3.3 (worst case, zero slopes).** Assume (U^q_{alpha'}) and
`|a_t(z) - a_t(z')| <= G |z - z'|_inf` on `X0_{V_t}` for all `t`. Put all
cells and leaves on one product grid with cell side at most `h` in every
coordinate, use zero slopes, and choose `beta` as in Lemma 1.5. Then
`l_r >= f* - |T| (2 (k-1) G h + alpha' A h^2/4)`. With
`h = min(eps/(4 (k-1) G |T|), sqrt(2 eps/(alpha' A |T|)))` the certificate
proves tolerance `eps` and has size at most `2 |T| ceil(s0/h)^{w+1}`.

*Proof.* In a configuration, `D_t` and `(B_{p(t)})_{S_t}` are intersecting
grid cells, so `|z^t_i - z^{p(t)}_i| <= 2h`, and `|z^t_i - x_i| <= 2(k-1)h`
along paths of at most `k-1` edges. With zero slopes the value is
`sum_t sum_{c at t} f_{c,B_t}(z^t) >= sum_t a_t(z^t) - sum_t alpha' A h^2/4 >= F(x) - |T|(2(k-1) G h + alpha' A h^2/4)`,
and `F(x) >= f*`. Lemma 1.5 gives the claim. Each bag has at most
`ceil(s0/h)^{|V_t|}` leaves and each separator at most `ceil(s0/h)^{|S_t|}`
cells. □

This is `(C n/eps)^{O(w)}` with `C` depending on `G`, `k` and `s0`. It needs
no uniqueness and no smoothness. It is not new in substance: Zhang–Sun
(2022, Corollary 1) give `T (1 + 2LDT/eps)^d` iterations for nested
decomposition, Bienstock–Muñoz give LP sizes of the same type with scaled
accuracy, and grid DPOP has the same error accounting (literature audit,
C2). By Proposition 2.4 the factor `|T|^{(w+1)/2}` from splitting the
tolerance cannot be removed in this model; whether the exponent `w+1` of
`1/eps` can be lowered to `(w+1)/2` in the worst case is open (value
functions with concave kinks make constant and affine child bounds first
order there).

### 3.3 Instance-dependent bound under quadratic growth

**Theorem 3.4.** Assume (QG) with minimizer `x*` and constant `c_g`,
(L^{1,1}) with constant `M_a`, and (U^q_{alpha'}). Let `k`, `Delta`, `w`,
`A`, `|T|` be as in Section 1, and put

```
D_k = sum_{j=1}^{k-1} Delta^j,   K_1 = max(1, (k-1) sum_{j=0}^{k-2} Delta^j),
Q   = M_a^2 w k/c_g + M_a w/2 + alpha' A.
```

Let `theta = 2^{-mu}` be such that

```
(T1) theta <= 1/2,   4 theta sqrt((k-1) D_k) <= 1/2,
(T2) theta^2 k (48 K_1 (1+Delta) Q + alpha' A) <= c_g/2,
```

and let `0 < h <= h_0 = (eps/(4 |T| (768 K_1 Q + 3 alpha' A)))^{1/2}`.
Build the certificate with a center `x̂ in X0` satisfying `|x̂ - x*|_inf <= h`,
cells `P_t = Pi(x̂_{S_t}; h, theta)`, leaves `L_t = Pi(x̂_{V_t}; h, theta)`,
slopes `lambdâ_t` with `nu^2 = sum_t |lambdâ_t - lambda_t(x*)|_2^2`, and
`beta` as in Lemma 1.5. If

```
(T3) nu <= min( sqrt(eps (768 K_1 Q + 3 alpha' A)/(3072 w)),  sqrt(eps c_g/(384 w k (1+Delta))) / theta ),
```

then `l_r >= f* - eps`, and the size is at most
`2 |T| (4/theta)^{w+1} (log2(s0/h) + 2)`.

With `theta` the largest admissible power of `1/2` and `h = h_0`,
`1/theta = O( k sqrt(K_1 (1+Delta) w) M_a/c_g + sqrt(k K_1 (1+Delta)(M_a w + alpha' A)/c_g) + sqrt((k-1) D_k) )`
and

```
N_dec(eps) <= 2 |T| (4/theta)^{w+1} ( (1/2) log2( 4 |T| s0^2 (768 K_1 Q + 3 alpha' A)/eps ) + 2 ).
```

For paths and other decompositions with `k = 2`, `Delta = 1`: `K_1 = 1`,
`D_k = 1`, and the base is `O(M_a sqrt(w)/c_g)` when `M_a >= c_g` and
`alpha' A <~ w M_a^2/c_g` (both hold on the path family).

*Proof.* Fix a configuration and its consistent point `x`; let
`X = |x - x*|_2`. Notation: `rho_t = |x_{V_t} - x*_{V_t}|_inf`,
`r_t = |x_{V_t} - x*_{V_t}|_2`, edge drifts
`d_t = |z^t_{S_t} - z^{p(t)}_{S_t}|_inf` (`d_r = 0`), bag drifts
`Delta_t = |z^t - x_{V_t}|_inf`. Each variable lies in at most `k` bags, so
`sum_t rho_t^2 <= sum_t r_t^2 <= k X^2`.

1. *Widths.* By Lemma 3.1 and `|x̂ - x*|_inf <= h`, a member `B` of a shell
   partition containing a point `z` has `w(B) <= 2h + theta |z - x*|_inf`
   (using `theta <= 1`). Hence
   `w(B_t) <= 2h + theta (rho_t + Delta_t)` and
   `w(D_t) <= 2h + theta (rho_t + Delta_t)`.
2. *Drift recursion.* `z^t_{S_t} in D_t`, `z^{p}_{S_t} in (B_p)_{S_t}` and the
   two boxes intersect, so
   `d_t <= 4h + theta (rho_t + rho_p + Delta_t + Delta_p)`. The bag drift
   telescopes along at most `k-1` edges:
   `Delta_t <= sum_{j=0}^{k-2} d_{anc_j(t)}`, and
   `Delta_p <= sum_{j=1}^{k-1} d_{anc_j(t)}`, where `anc_j` is the `j`-th
   ancestor. With `theta <= 1/2`,
   `d_t <= a_t + 4 theta sum_{j=1}^{k-1} d_{anc_j(t)}` with
   `a_t = 2(4h + theta(rho_t + rho_{p(t)}))`.
3. *Solving it.* Write this as `d <= a + Gamma d` with `Gamma >= 0`
   entrywise and strictly "upward" (from a node to its ancestors), hence
   nilpotent. Iterating, `d <= sum_{j >= 0} Gamma^j a` (a finite sum).
   `Gamma` has row sums at most `4 theta (k-1)` and column sums at most
   `4 theta D_k` (a node has at most `D_k` descendants within `k-1`
   generations), so `||Gamma||_2 <= 4 theta sqrt((k-1) D_k) <= 1/2` by (T1),
   and `|d|_2 <= 2 |a|_2`. Now
   `|a|_2^2 <= 12 (16 |T| h^2 + theta^2 (1 + Delta) sum_t rho_t^2)`, so

   ```
   sum_t d_t^2 <= 48 (16 |T| h^2 + theta^2 (1+Delta) k X^2).
   ```

   An edge drift `d_s` enters `Delta_t` for `t = s` and for descendants of
   `s` within `k-2` generations, so by Cauchy–Schwarz
   `sum_t Delta_t^2 <= K_1 sum_t d_t^2`.
4. *Error terms.* By Lemma 1.5 and (U^q), `l_r >= min over configurations of Phi - E_rel`,
   with `Phi` computed with the slopes `lambdâ` and
   `E_rel = sum_t alpha' A w(B_t)^2/4`. By (3.1), (L^{1,1}), and
   `|z^t - x_{V_t}|_2 <= sqrt(w) Delta_t` (at most `w` coordinates differ),
   each bracket in (3.1) is at least
   `-(M_a r_t sqrt(w) Delta_t + (M_a w/2) Delta_t^2)`: the Taylor remainder
   at `x` plus `|∇a_t(x) - ∇a_t(x*)| <= M_a r_t`. The slope error adds at
   most `sum_t |lambdâ_t - lambda_t|_2 sqrt(w) d_t <= sqrt(w) nu |d|_2`. So
   `Phi - E_rel >= F(x) - E` with

   ```
   E = sum_t [ M_a sqrt(w) r_t Delta_t + (M_a w/2) Delta_t^2 + (alpha' A/4) w(B_t)^2 ] + sqrt(w) nu |d|_2.
   ```

5. *Absorbing into the margin.* Young's inequality with weight
   `c_g/(4k)` gives
   `M_a sqrt(w) r_t Delta_t <= (c_g/(4k)) r_t^2 + (M_a^2 w k/c_g) Delta_t^2`.
   Also `w(B_t)^2 <= 3(4h^2 + theta^2 rho_t^2 + theta^2 Delta_t^2)`. Hence,
   with `Q` as defined (it dominates `M_a^2 w k/c_g + M_a w/2 + 3 alpha' A theta^2/4`),

   ```
   E <= (c_g/4) X^2 + Q sum_t Delta_t^2 + 3 alpha' A |T| h^2 + (3/4) alpha' A theta^2 k X^2 + sqrt(w) nu |d|_2.
   ```

   From step 3, `Q sum Delta_t^2 <= 48 K_1 Q (16 |T| h^2 + theta^2 (1+Delta) k X^2)`,
   and `|d|_2 <= sqrt(48) (4 sqrt(|T|) h + theta sqrt((1+Delta) k) X)`, so
   `sqrt(w) nu |d|_2 <= 4 sqrt(48 w |T|) nu h + (c_g/8) X^2 + 96 w nu^2 theta^2 (1+Delta) k/c_g`.
6. *Collecting.* The coefficient of `X^2` is at most
   `c_g/4 + c_g/8 + theta^2 k (48 K_1 (1+Delta) Q + alpha' A) <= c_g/4 + c_g/8 + c_g/2 < c_g`
   by (T2). The remaining terms are
   `|T| h^2 (768 K_1 Q + 3 alpha' A) + 4 sqrt(48 w |T|) nu h + 96 w nu^2 theta^2 (1+Delta) k/c_g`;
   the first is at most `eps/4` by the choice of `h`, and the other two are
   at most `eps/4` each by (T3) and `h <= h_0`. So `E <= c_g X^2 + (3/4) eps`,
   and by (QG) `Phi - E_rel >= f* + c_g X^2 - E >= f* - eps` for every
   configuration.
7. *Count.* By Lemma 3.1 each bag has at most `(J+1)(4/theta)^{|V_t|}` leaves
   and each separator at most `(J+1)(4/theta)^{|S_t|}` cells, with
   `J + 1 <= log2(s0/h) + 2`. □

**Remark 3.5 (what the theorem needs, and what it does not).**

- *No regularity of value functions.* The proof never uses `phi_t`. It
  compares each configuration with its consistent point and pays the copy
  error with the global margin. Far from `x*`, value functions may have
  kinks and cell minorants may be poor relative to `phi_t`; this does not
  matter, because there the error is at most `M_a r_t sqrt(w) Delta_t`,
  first order in the drift but with a coefficient proportional to the
  distance from `x*`, and the drift is itself at most `theta` times that
  distance. Robertson–Cheng–Scott's statement (affine child bounds are second
  order only with `C^2` value functions and optimal multipliers) concerns
  the accuracy of a cell bound relative to the cell minimum; the certificate
  needs accuracy only relative to the global margin, and that is what
  (QG) provides.
- *Uniqueness.* (QG) with a single point `x*` is used twice: the slopes are
  gradients at one point, and the margin grows away from that point. With a
  continuum of minimizers the multipliers vary along it and one slope per
  separator cannot be right everywhere (Section 6).
- *Inexact center and multipliers.* The center may be off by `h` in
  sup-norm and the slopes by `nu = O(sqrt(eps))` in total Euclidean norm,
  with constants independent of `|T|` and `n`. The sup-norm requirement is
  the binding one: the center needs `|x̂ - x*|_inf <= h <= h_0 = O(sqrt(eps/|T|))`,
  otherwise the central cells are too wide and the `|T| h^2` term exceeds
  `eps`. A Euclidean error `O(sqrt(eps))` does not give this, because it can
  sit in one coordinate. Slopes computed at `x̂` satisfy
  `nu <= k^{3/2} M_a |x̂ - x*|_2` (each `lambda_{t,i}` sums at most `k`
  gradients, and each coordinate lies in at most `k - 1` separators). So a
  local solve with `|x̂ - x*|_inf <= h_0` suffices; when `n = O(|T|)` (for
  example on paths) it also gives `nu <= k^{3/2} M_a sqrt(n) h_0 = O(sqrt(eps))`.
  Quadratically convergent local methods reach this cheaply.
- *Zero slopes.* If `lambda_t(x*) = 0` for all `t` (for example the path
  family with `c = 0`), constant minorants are enough. Otherwise
  Proposition 2.6 shows that they are not.
- *Constants.* (T2) makes `1/theta` of order `k sqrt(K_1 (1+Delta) w) M_a/c_g`,
  so the base `(4/theta)^{w+1}` is a condition number raised to the power
  `w+1`. The constants are far from sharp: on the path family (T2) asks
  for `theta = 2^{-10}`, while `theta = 1/16` works for every tested `n` and
  `theta = 1/8` fails for `n > 16` (Section 5.4, Remark 3.6).

**Remark 3.6 (the copy-drift condition is not an artifact).** Condition
(T2) asks that the copy error in each bag, `M_a r_t sqrt(w) Delta_t` with a
drift `Delta_t` of order `theta` times the distance from `x*`, be paid by
that bag's share of the margin, of order `c_g r_t^2`. It does not depend on
`n`. If it fails, the error is not merely lost once: configurations can
repeat a bad pattern in every bag. Section 5.4 shows this on the path
family. With `theta = 1/8` the minimizing configuration alternates
`x_i ≈ ±0.5` against copies at `∓0.625`. The parent leaf and the child cell
only touch, so the drift is the sum of both widths. Each bag then contributes
about `-0.00625` instead of a positive margin, and the root gap grows
linearly in `n` once `n > 16`. With `theta = 1/16` the gap is `O(|T| h^2)`
for all tested `n`. The review swept `b` (at `h = 2^-6`, `n = 24` and 40):
the largest admissible `theta` is 1/4 for `b = 0.5, 0.6`, 1/8 for `b = 0.7`,
and 1/16 for `b = 0.8, 0.85`. It follows the threshold `(1-b)/(2b)` of the
alternating mechanism, which is linear in the curvature margin along the
alternating direction, as the order `theta ~ c_g/M_a` in (T2) predicts. So
the dependence of `theta` on the conditioning is real; only the constant in
(T2) is loose.

### 3.4 Toward an algorithm that does not know `x*`

The certificate of Theorem 3.4 is centered at `x̂` close to `x*`. The fixed-slope
algorithm of Section 1.5 obtains `x̂` from a local solve. If `x̂` is within
`h` of the global minimizer, Theorem 3.4 applies as stated. If `x̂` is a
nonglobal local minimizer, the certificate built around it remains valid
(Lemma 1.3) but its root bound may be below `UBD - eps`; the minimizing
configuration then points to a region of lower relaxed value, which the
algorithm refines and where it can restart the local solve. A complexity
bound for this loop is **not proved**. A cleaner route would be an analogue
of uniform bisection ([C, Lemma 6.1]): refine every leaf and cell that takes
part in some configuration of value below `UBD - eps`, level by level. The
difficulty is that "taking part" is a property of whole configurations, not
of single boxes, so the localization step of [C, Lemma 6.1] does not carry
over directly.

### 3.5 Covering characterization: what is and is not proved

For (QG) instances, Theorems 2.5 and 3.4 match up to factors `C^{w+1}` and
`log(|T|/eps)`: every bag needs at least one leaf, at most
`O((4/theta)^{w+1} log(|T|/eps))` suffice, and at a nondegenerate minimizer
with gap in all bag coordinates Lemma 2.2 gives `Omega(log(1/eps))` leaves
per bag. This is the analogue of [C, Theorem 6.3] for regular instances.

**Conjecture 3.7.** Under (L^{1,1}), (U^q) and (G_alpha), and a hypothesis
on the near-optimal sets that makes copy errors second order along them
(to be found), `N_dec(eps)` lies within factors `C^{w+1} poly(|T|) log(1/eps)`
of

```
Psi(eps) = min over eps_1 + ... + eps_|T| = eps of  sum_t sup_{eta >= 0} N_inf( pi_{V_t}(E(eta)), sqrt((eps_t + eta)/alpha) ).
```

Obstacles: (i) the upper bound of Theorem 3.4 needs one multiplier per
separator; along a positive-dimensional optimal set the multipliers vary,
cells would need their own slopes, and the telescoping identity (Lemma 3.2)
then leaves mismatch terms whose size is not controlled; (ii) the lower
bound with a shared tolerance is proved only for products (Proposition 2.4);
Theorem 2.5 gives each bag the whole tolerance.

## 4. The separation theorem

**Theorem 4.1.** Let `n >= 3`, `X0 = [-1,1]^n`, `kappa = 0.1`, `b = 0.8`,
and `F_n(x) = sum_{i=1}^n (x_i^2 - kappa x_i^4) + b sum_{i=1}^{n-1} x_i x_{i+1}`.
Both models use the same per-factor relaxations: the unary factors (convex on
`[-1,1]`) exactly, and each bilinear factor `b x_i x_{i+1}` by alphaBB with
`alpha = |b|/2 = 0.4` on every box. `F_n` is nonconvex on `X0`, and `x* = 0`
is its unique global minimizer, nondegenerate, with `f* = 0`.

(a) *Single tree.* Every single-tree certificate at tolerance `eps`, and
the leaves plus tightening pieces of every single-tree B&B run covered by
[C, Lemma 2.1] (any branching, node order, valid incumbent and
same-relaxation tightening), has at least

```
N_single(eps) >= max( 0.068 sqrt(n) (2e/pi)^{n/2} log(0.2/(n eps)),  (5/3)^n exp(-(5/9)(1 + 1.25 eps)) )
```

members. The first term (Corollary 2.1, proved here) is positive for
`eps < 0.2/n`, grows like `log(1/eps)`, and has base `(2e/pi)^{1/2} ≈ 1.31549`;
the exact integral bound `L_n(eps)` is tabulated in Section 5 (for example
`L_40(1e-6) = 3.9e5`, `L_80(1e-6) = 2.9e10`). The second term is the
face-exact note's Theorem 1 (Corollary 1.3 there; imported, not re-proved
here). It is at least `0.57 (5/3)^n` for `eps <= 1e-4` and has no
`log(1/eps)` factor.

(b) *Decomposition, upper bound.* For the path decomposition (bags
`{i, i+1}`, root `{1, 2}`) there is a decomposition certificate proving
tolerance `eps` with constant cell minorants (here `lambda_t(x*) = 0`) and

```
size <= 3.36e7 (n-1) ( (1/2) log2( 1.96e6 (n-1)/eps ) + 2 ).
```

(c) *Decomposition, lower bound.* For the same decomposition every
certificate proving tolerance `eps` has at least
`0.2778 (n-1) log(1 + 0.6/eps)` leaves.

Consequently, for every `eps <= 1e-4`,
`N_single(eps)/N_dec(eps) >= 3e-10 (2e/pi)^{n/2}/sqrt(n)`, where `N_dec` is the
bound in (b): exponential in `n`, uniformly in `eps`.

*McCormick variant.* With McCormick envelopes of the bilinear factors in
both models, the second term of (a) and part (b) still hold (McCormick
satisfies (M_b) and (U^q_{0.4})), so
`N_single/N_dec >= c (5/3)^n/(n log(n/eps))` for `eps <= 1e-4`: exponential
in `n` for each `eps`, but not uniformly as `eps -> 0`. Part (c) and the first
term of (a) need the alphaBB gap (G) and do not transfer.

*Proof.* The facts about `F_n` and the first term of (a) are Section 2.1
(Corollary 2.1 with the explicit constants for `b = 0.8`). For the second
term, the relaxation satisfies the face-exact note's hypothesis (M_b): the
gap of alphaBB on `b x_i x_{i+1}` is
`(|b|/2)(a_i + a_{i+1}) >= (|b|/2)(d_i^2 + d_{i+1}^2) >= |b| d_i d_{i+1}`,
because `a_i >= d_i^2`. Its hypothesis (Q_2) on `R = [-1,1]^n` is the upper
quadratic `m(x) <= |x|^2 + b sum x_i x_{i+1}` of Section 2.1. Then
`rho = 2/(2b) = 1.25`, `S = 3/2`, `lambda = 5/9` and `eps'' = 1.25 eps`, and
its Theorem 1(a) gives the second term, for certificates and (by its
Lemma 1.2) for leaves plus tightening pieces of runs.

(b) Apply Theorem 3.4 with `x̂ = x* = 0` and exact slopes, so `nu = 0`.
Constants: `k = 2`, `Delta = 1`, `w = 1`, `D_k = K_1 = 1`,
`|T| = n - 1`, `s0 = 2`, `c_g = 1 - kappa - |b| = 0.1`, `alpha' = 0.4`,
`A = 2` (only the bilinear factor of each bag is relaxed). `M_a = 2.8`: the
Hessian of a bag function is `[[phi''(z_1), b], [b, 0]]` or, in the last
bag, `[[phi''(z_1), b], [b, phi''(z_2)]]`, with `0.8 <= phi'' <= 2`, so its
spectral norm is at most `2 + 0.8`. Then
`Q = 2.8^2 * 2/0.1 + 1.4 + 0.8 = 159.0`. (T1) requires `theta <= 1/8`.
(T2) requires `theta^2 * 2 * (96 * 159.0 + 0.8) <= 0.05`, that is
`theta <= 1.28e-3`; take `theta = 2^{-10}`, so `(4/theta)^2 = 4096^2`.
`h_0^2 = eps/(4 (n-1)(768 * 159.0 + 2.4)) = eps/(4.885e5 (n-1))`. The size
bound of Theorem 3.4 is
`2 (n-1) 4096^2 (log2(2/h_0) + 2) = 3.36e7 (n-1) ((1/2) log2(4 * 4.885e5 (n-1)/eps) + 2)`.

(c) Lemma 2.2 at each bag `{t, t+1}` with `K = {t, t+1}`, weights
`alpha_t = alpha_{t+1} = 0.4` and `x̄ = 0`. The bag is the only bag containing
the scope of `b x_t x_{t+1}`, so that factor is assigned to it. With
`y = (x_t, x_{t+1})`, `m(0, y) <= (1/2) y^T H_2 y`, `H_2 = [[2, b],[b, 2]]`,
`det H_2 = 4 - b^2`, `lambda_min(H_2) = 2 - |b|`, and the ellipsoid argument
of Corollary 2.1 with `n = 2` (where `J_2(T) = (1/2) log(1 + T^2)` exactly)
gives
`|L_t| >= (|b|/pi^2) (2 pi/sqrt(4 - b^2)) log(1 + (2 - |b|)/(2 eps)) = 0.2778 log(1 + 0.6/eps)`.

*Ratio.* Write `L2 = log2(1/eps)`.
- If `eps <= 0.04/n^2`, then `0.2/(n eps) >= eps^{-1/2}`, so the first term
  of (a) is at least `0.034 sqrt(n) (2e/pi)^{n/2} log(1/eps)`. Also
  `(n-1)/eps <= 0.2 eps^{-3/2}` and `L2 >= log2(225) > 7.8`, so the bound in
  (b) is at most
  `3.36e7 n ((1/2)(18.6 + 1.5 L2) + 2) <= 3.36e7 n * 2.2 L2 <= 1.07e8 n log(1/eps)`.
  The ratio is at least `3.1e-10 (2e/pi)^{n/2}/sqrt(n)` (`0.034/1.07e8 = 3.18e-10`).
- If `0.04/n^2 < eps <= 1e-4`, the second term of (a) is at least
  `0.57 (5/3)^n`, and `1/eps < 25 n^2` gives (b) `<= 3.36e7 n (14.8 + 1.5 log2 n)`.
  This case is nonempty only for `n >= 21`. The ratio divided by
  `(2e/pi)^{n/2}/sqrt(n)` is
  `0.57 (1.26696)^n/(3.36e7 sqrt(n) (14.8 + 1.5 log2 n))` (`1.26696 = (5/3)/sqrt(2e/pi)`), which is increasing
  in `n >= 3` and equals `1.2e-9` at `n = 3`. □

A grid evaluation over `3 <= n <= 300` and `1e-40 <= eps <= 1e-4` gives a
smallest ratio of `1.26e-9 (2e/pi)^{n/2}/sqrt(n)` (`logs/revision_checks.log`;
the script normalizes by `(2e/pi)^{n/2}`). The base must not be rounded up:
with `1.3155^n` in place of `(2e/pi)^{n/2}` the statement fails for
`n >~ 2.8e5` at astronomically small `eps` (recheck, Section 1).

*Scope of the theorem.*

- *Relaxations.* The relaxations are the same on both sides, and the
  single-tree bounds cover every adaptive single tree with them. The second
  term of (a) needs only (M_b), which termwise McCormick satisfies, and (b)
  holds for McCormick too ((U^q_{0.4}), [C, Lemma 1.1]). So **the separation
  also holds for termwise McCormick**, with the `eps`-free single-tree bound
  `0.57 (5/3)^n` for `eps <= 1e-4` (the `log(1/eps)` growth of the first term
  needs the alphaBB gap in every coordinate). Not covered: cuts on
  aggregated expressions (for example convexity detection on the quadratic
  part), SCIP's default PSD-minor cuts (face-exact note, Section 7.4), and
  other factorizations of the same objective (Section 4.1).
- The program's SCIP probe adds linear terms `c_i x_i`. For an interior
  global minimizer `x*`, `m(x) <= (1/2)(x - x*)^T H (x - x*)` still holds
  (Taylor with `∇F(x*) = 0` and `∇^2 F <= H` in the PSD order, since
  `phi'' <= 2`), so the first term of (a) holds with
  `R^2 = lambda_min(H)(1 - |x*|_inf)^2/2`, and the second with
  `r = 1 - |x*|_inf` in place of 1 (face-exact note, Corollary 1.3).
  (b) holds if the minimizer is unique and nondegenerate, with the slopes
  `lambda_t(x*) != 0` and a constant `c_g` that is not explicit. With zero
  slopes, Proposition 2.6 then forces `Omega(eps^{-1/2})` cells.
- *What is counted.* Size counts leaves and cells. The work of the DP is
  one convex program per (leaf, cell) pair with `B_{S_t} ∩ D ≠ ∅`. For an
  interior bag at `theta = 1/16` the pairs are 3.04, 3.78, 4.47 and 4.81 times
  the leaves at `h = 2^-4, 2^-8, 2^-12, 2^-14` (at most 10, 51, 115 and 147
  cells per leaf; `logs/revision_checks.log`, reproducing the review). The
  ratio grows by about 0.17 per halving of `h`, so shell certificates need
  `Theta(|T| C^{w+1} log^2(|T|/eps))` programs, one log factor more than
  their size. Each program is `(w+1)`-dimensional, while a single-tree leaf
  is `n`-dimensional. The review suggests one program per leaf,
  `beta_{t,D} = min { min_{z in B} (Rel_{t,B}(z) - lambda_t^T z_{S_t}) : B in L_t, B_{S_t} ∩ D ≠ ∅ }`.
  It is valid (it only lowers `beta`), and in Theorem 3.4 the drift bound
  becomes `w(B_t) + w(D_t) + w(B_p)`; the resulting constants are not
  written out here.
- *Constants and crossovers.* The constant in (b) comes from the
  conservative condition (T2). In the computations (Section 5.4)
  `theta = 1/16` suffices for every tested `n`, and the certificates have
  about `3.1e3` leaves per bag per halving of `h`. At `eps = 1e-6`:
  - the face-exact term of (a) exceeds the computed certificate size from
    `n = 29` on (28 at `eps = 1e-4`), and Corollary 2.1's exact integral from
    `n = 46`; counting convex programs instead of leaves, from 32 and 51
    (review);
  - proven against proven, the single-tree bounds exceed (b) from `n = 49`
    (face-exact term) and `n = 86` (Corollary 2.1 closed form).

  Actual single trees are far above the lower bounds. The review's toy
  bisection B&B with this relaxation (incumbent `f*`, widest-side
  bisection, Frank–Wolfe bounds) needs 60,094 leaves at `n = 8` and 199,240
  at `n = 9` for `eps = 1e-4`. The computed certificates have 173,608 and
  198,446 leaves (`logs/E1_scaling.log`, `logs/revision_checks.log`), so an
  actual tree exceeds the unoptimized certificate already at `n = 9`. This
  compares one algorithm with a certificate centered at `x*`; it shows that
  both proven bounds are loose, not that an algorithm achieves the
  certificate size.

### 4.1 Dependence on the factorization

The same objective can be written as a sum of factors on the same path
decomposition in several equally cheap ways. Theorem 4.1 is about one of
them. Write `g_i(t) = t^2 - kappa t^4`. Corollary 2.1 bases
`sqrt(4e/pi * weight/lambda_geo)`, with `lambda_geo = 1.6` and interior
weight `2 alpha` (`logs/revision_checks.log`, reproducing the review's
table):

| factors | alphaBB `alpha` computed on | `alpha` per factor | interior weight | base |
|---|---|---|---|---|
| `b x_i x_{i+1}` alone, `g_i` exact (this note) | any box | 0.400 | 0.800 | **1.3155** |
| `g_i + b x_i x_{i+1}` (PROGRAM probe) | root box | 0.247 | 0.494 | 1.034 |
| same | boxes near `x* = 0` | 0.140 | 0.281 | 0.780 |
| `g_i/2 + g_{i+1}/2 + b x_i x_{i+1}` ("balanced") | root box | 0.200 | 0.400 | **0.930** |
| balanced | each box (exact where convex) | 0 on `abs(x)_inf <= 0.577` | 0 | none |

- In this note's relaxation the convex unary terms are exact and add no gap,
  so how they are distributed among factors does not matter. What changes
  the result is merging them into the bilinear factors before relaxing.
  That is a different relaxation of the same cost.
- *Balanced split, root-box `alpha`.* The base is below 1, so Corollary 2.1
  gives no exponential bound; the review computes `L_n(1e-6) = 0.83, 0.16,
  0.012` at `n = 10, 40, 80`. The face-exact theorem does not apply either:
  the gap of one factor is `0.2(a_i + a_{i+1})`, which at the center of a
  cube is `0.4 d_i d_{i+1}`, below the `0.8 d_i d_{i+1}` that (M_b) requires.
- *Balanced split, box-dependent `alpha`.* Every factor is convex on
  `abs(x)_inf <= sqrt((1-b)/(6 kappa)) = 0.577`, so one box certifies that
  cube and there is no clustering at `x*`. In the review's toy B&B
  (`reviews/decomposition-review-checks/split_bb.py`) the leaf counts no
  longer depend on `eps`, but they still grow about 2.3–2.5 times per
  variable, from the outer region `abs(x)_inf > 0.5` (for example 23, 60, 140,
  322, 768, 1,792 and 4,173 leaves at `n = 4..10` with the inner cube as one
  leaf). **No lower bound for this growth is proved; it is open.** The
  decomposition side also gets cheaper under this split, because the bags
  are exact near `x*`.

So the `eps`-uniform separation of Theorem 4.1 is a property of relaxing
each bilinear term alone (alphaBB or McCormick). An `eps`-independent
exponential separation under the balanced split looks plausible from the
toy runs but is unproved.

**Observation 4.2 (no lower bound holds uniformly over all splits).** Let
`(T, {V_t})` be a tree decomposition of the factor hypergraph of `F`. If
arbitrary functional splits `F = sum_t ã_t(x_{V_t})` are allowed, the split
`ã_r = f* + g_r`, `ã_t = g_t` (`t != r`), with the conditional margins
`g_t` of Section 1.1, has per-factor convex envelopes whose sum is exact at
the root. So one node certifies every tolerance `eps >= 0` in a single
tree, and one leaf per bag and one cell per separator (size `2|T| - 1`, the
smallest possible) do so in a decomposition certificate.

*Proof.* By Lemma 1.1, `F = f* + sum_t g_t`, and each `g_t` depends only on
`x_{V_t}`. Each `g_t >= 0`, so `0` is a convex minorant and
`vex_B g_t >= 0` on every box `B`. Hence the root bound is
`f* + min_x sum_t vex_{X0} g_t(x_{V_t}) >= f* + sum_t min vex_{X0} g_t >= f*`,
and it is at most `F(x*) = f*`, so it equals `f*`. (Also
`g_t(x*_{V_t}) = 0`, because the restriction of `x*` is optimal for every
subtree given its separator values.) For the decomposition certificate,
take `L_t = {X0_{V_t}}`, `P_t = {X0_{S_t}}`, zero cell minorants, `psi = 0`
and `l_r = f*`; (LC) reads `vex g_t >= 0` in each bag and
`f* + vex g_r >= f*` at the root. □

*Scope.* The observation rules out lower bounds that hold uniformly over all
splits, for single trees and for separations alike, whenever the per-factor
relaxation is exact at factor minima (its minimum over each box equals the
factor's minimum there), as convex envelopes are, and even the constant
minorant `min_B ã_t` is. It says nothing about a fixed relaxation rule such
as alphaBB, whose gap `alpha q_B` is positive inside every box, or about
restricted split classes, such as distributing the given unary terms
(Section 4.1). A fixed split's envelope bound is itself a Lagrangian bound:
`vex_B f(x) = min {∫ f dnu : nu on B, mean nu = x}`, so per-factor envelopes
enforce only first-moment consistency of the bag copies; the split above
builds the optimal nonlinear cost shift into the factors (recheck,
Section 2.1).

Dually, in measure form (the coordinator's observation, checked): relax
`min F` to probability measures `mu_t` on `X0_{V_t}`, one per bag, with
equal marginals of `mu_t` and `mu_{p(t)}` on `S_t`, and objective
`sum_t ∫ a_t dmu_t`. Such measures glue on a tree (Vorob'ev 1962, for
consistent families of measures along running-intersection families; used in
Lasserre's 2006 sparse moment relaxations; in discrete graphical models this
is tightness of the local polytope on junction trees). Sample `x_{V_r}` from
`mu_r`; going down the tree, sample `x_{R_t}` from the conditional law of
`mu_t` given `x_{S_t}` (a disintegration, which exists on these compact
metric spaces). By running intersection, `x_{S_t}` has already been sampled
with law equal to the `S_t`-marginal of `mu_{p(t)}`, which is that of `mu_t`,
and the variables `R_t` are new. By induction the law of `x_{V_t}` is
`mu_t`, so the relaxation value is `∫ F dmu >= f*`: the local-consistency
relaxation is exact. Its Lagrangian dual over separator functions (cost
shifting) is an optimization over splits, and the split above attains the
dual optimum (the `phi_t` are continuous).

References (checked at the bibliographic level): N. N. Vorob'ev,
"Consistent families of measures and their extensions", Theory Probab.
Appl. 7 (1962); J. B. Lasserre, "Convergent SDP-relaxations in polynomial
optimization with sparsity", SIAM J. Optim. 17(3) (2006).

The split uses the value functions, so it is as hard to compute as the
problem itself, and envelopes of the `g_t` are not computable in general.
The observation only shows that single-tree lower bounds must fix the
factorization and the per-factor relaxation, or restrict the admissible
splits. The theorems of this note are statements about a fixed termwise
relaxation, not about search structure alone.

## 5. Numerical checks

All computations are in double precision (the single-tree integrals in
30-digit `mpmath`). The certificate DP computes every `beta_{t,D}` by exact
convex minimization over the sub-box (nested bisection on monotone
derivatives, 60 steps each), so root bounds are accurate to about `1e-12`;
shell boundaries are floating-point numbers, so coverage holds up to
rounding of order `1e-16`. (Leaf, cell) pairs are found by a closed
intersection test on these rounded edges. Around a non-dyadic `x*`
(Sections 5.2–5.3), an edge shared by two boxes can be computed by different
operations on each side and differ by one rounding unit. The unwidened test
of the first version therefore missed pairs that touch in exact arithmetic:
26 to 7,657 per certificate. The test is now widened by `1e-12`
(`PAIR_TOL` in `dp_certificate.py`). In every certificate of Sections
5.2–5.3 this recovers exactly the pairs of Definition 1.2
(`check_pairs_exact.py`). Only two zero-slope entries of the `n = 8` table in
Section 5.3 change. The first-version values were still valid lower bounds:
no pair whose boxes overlap with positive length was lost, so the remark
after Lemma 1.3 applies. At `x* = 0` (Section 5.4) all edges are dyadic and
exact, and nothing changes. These are illustrations, not certified counts.
Family: `b = 0.8`, `kappa = 0.1`, alphaBB `alpha = 0.4` on bilinear factors,
unary factors exact.

### 5.1 Single-tree lower bound (`single_tree_lb.py`, `logs/single_tree_lb.log`)

Exact integral bound `L_n(eps)` of Corollary 2.1, the closed form
`0.068 sqrt(n) (2e/pi)^{n/2} log(0.2/(n eps))`, and the growth per variable
`(L_n/L_{n'})^{1/(n-n')}`:

| n | `L_n(1e-4)` | `L_n(1e-6)` | `L_n(1e-8)` | closed form at `1e-6` | growth per variable (`1e-6`) |
|---|---|---|---|---|---|
| 4 | 5.03 | 8.27 | 11.5 | 4.41 | 1.46 |
| 10 | 33.4 | 60.6 | 87.7 | 33.0 | 1.37 |
| 20 | 629 | 1.23e3 | 1.83e3 | 675 | 1.34 |
| 40 | 1.82e5 | 3.87e5 | 5.92e5 | 2.12e5 | 1.33 |
| 80 | 1.24e10 | 2.92e10 | 4.61e10 | 1.60e10 | 1.32 |

- The closed form is below the exact bound in every row, as it must be.
- The growth per variable tends to the predicted `sqrt(2e/pi) = 1.3155`.
- The exponential-growth threshold is `|b| > 0.53334`
  (`|b|/(1 + sqrt(1 - b^2)) = pi/(4e)`); at `b = 0.5` the asymptotic base is
  `0.963 < 1`, so this route gives no exponential bound there.
- Sanity check of the ellipsoid restriction: for `eps = 1e-3`, the bound
  from the full integral over `X0` is 1.979 (`n = 2`, quadrature) and
  `3.03 ± 0.03` (`n = 3`, Monte Carlo), above the ellipsoid bounds 1.778 and
  2.496.
- The bounds are small in absolute terms for small `n` (for example 8 leaves
  at `n = 4`). They are lower bounds on every run; the program's SCIP probe
  (with McCormick-type relaxations and linear terms, so not covered) used
  thousands of nodes at `n = 8–10`.

### 5.2 Validity (`run_experiments.py E3`, `logs/E3_validity.log`)

For small instances the cell minorants were compared with grid value
functions `phi_t^grid >= phi_t` (minimum over a grid of 2001 values of the
next variable, computed by DP). Validity (Lemma 1.3) predicts
`l_{t,D}(s) <= phi_t(s) <= phi_t^grid(s)`. Largest value of
`l_{t,D}(s) - phi_t^grid(s)` over all grid points and cells:

| n | c | theta | h | slopes | `f*` | root `l_r` | max `(l - phi^grid)` |
|---|---|---|---|---|---|---|---|
| 4 | seed 0 | 1/8 | 2^-6 | affine | -0.0150131 | -0.0151597 | -5.2e-7 |
| 4 | seed 0 | 1/8 | 2^-6 | zero | -0.0150131 | -0.0168793 | -5.2e-7 |
| 6 | seed 0 | 1/8 | 2^-8 | affine | -0.0278448 | -0.0278619 | -2.3e-7 |
| 6 | seed 0 | 1/8 | 2^-8 | zero | -0.0278448 | -0.0294135 | -1.1e-6 |
| 6 | seed 1 | 1/4 | 2^-5 | affine | -0.0706494 | -0.2053542 | -1.1e-5 |
| 5 | 0 | 1/2 | 2^-4 | either | 0 | -0.2820615 | -1.1e-4 |

No violation; every root bound is below `f*`. Here "seed s" means
`c ~ U(-0.2, 0.2)^n` from `numpy.random.default_rng(s)`; `x*` was computed by
a grid DP followed by L-BFGS-B (`|∇F(x*)|_inf <= 1e-9`, interior).

This check is one-sided: `phi^grid` overestimates `phi_t`, so a violation
smaller than the grid error would go undetected, and the margins above are
of that size. The review evaluated `phi_t` accurately (grid DP, then
L-BFGS-B over the subtree variables) at the endpoints and midpoint of every
cell and found worst values of `l_{t,D}(s) - phi_t(s)` of `-1.4e-7`
(`n = 5`, seed 0, `theta = 1/8`, `h = 2^-6`) and `-1.8e-6` (`n = 6`,
seed 1, `theta = 1/4`, `h = 2^-5`), well above floating-point error
(`reviews/decomposition-review-checks/logs/valid_*.log`).

### 5.3 Affine versus zero slopes (`E2`, `E4`)

`n = 8`, `c` seed 0 (`x*` interior; slopes `lambda_t(x*)` between `-0.10`
and `0.07`), `theta = 1/8` (`logs/E2_slopes.log`, rerun with the widened
pair test; in the first version the zero-slope gaps at `h = 2^-2` and `2^-4`
were `1.72e-1` and `3.12e-2`, Section 8.2):

| h | gap `f* - l_r`, affine slopes | gap, zero slopes | size |
|---|---|---|---|
| 2^-2 | 1.03e-1 | 1.88e-1 | 11061 |
| 2^-4 | 6.42e-3 | 3.17e-2 | 22005 |
| 2^-6 | 4.01e-4 | 8.94e-3 | 32949 |
| 2^-8 | 2.51e-5 | 2.44e-3 | 43893 |
| 2^-10 | 1.57e-6 | 2.23e-3 | 54837 |
| 2^-12 | 9.80e-8 | 2.23e-3 | 65781 |
| 2^-16 | 3.83e-10 | 2.23e-3 | 87669 |

With affine slopes the gap falls by 16 for every factor 4 in `h` (second
order, about `1.6 h^2`) while the size grows by a constant per halving of `h`
(linear in `log(1/h)`). With zero slopes the gap stalls at `2.2e-3`.

`n = 3`, `c` seed 0 (`lambda_1 = 0.0315`), `h = 2^-14`, varying `theta`
(`logs/E4_theta.log`):

| theta | gap, affine | gap, zero | size |
|---|---|---|---|
| 1/2 | 1.7e-9 | 1.60e-3 | 1429 |
| 1/4 | 1.3e-9 | 1.32e-4 | 5533 |
| 1/8 | 1.3e-9 | 2.56e-5 | 21773 |
| 1/16 | 1.3e-9 | 5.66e-6 | 86445 |
| 1/32 | 1.3e-9 | 3.84e-6 | 344275 |

With zero slopes the gap scales like `theta^2` until it reaches the floor
`2 |lambda_1| h = 3.84e-6` set by the central cells: exactly the first-order
copy error of Proposition 2.6 (drift up to `2h` times slope `|lambda|`). To
reach tolerance `eps` with zero slopes one needs `h <= eps/(2|lambda|)` and
`theta = O(sqrt(eps))`, hence `Omega(eps^{-1/2})` cells; with affine slopes
`theta = 1/2` and `h = O(sqrt(eps))` suffice for this three-variable
instance (larger `n` needs smaller `theta`; Section 5.4).

### 5.4 Size versus `n` and `eps`, and the `theta` threshold (`E1`, `E5`, trace)

`c = 0` (`x* = 0`, all slopes 0), `theta = 1/16`, smallest `h = 2^{-j}` with
root gap at most `eps` (`logs/E1_scaling.log`, `logs/E1b_n64.log`):

| n | eps | h | gap `f* - l_r` | size | size/(n-1) | single-tree LB `L_n(eps)` |
|---|---|---|---|---|---|---|
| 4 | 1e-2 | 2^-3 | 9.4e-3 | 27856 | 9285 | 1.84 |
| 4 | 1e-4 | 2^-7 | 3.7e-5 | 64976 | 21659 | 5.04 |
| 4 | 1e-6 | 2^-10 | 5.7e-7 | 92816 | 30939 | 8.27 |
| 4 | 1e-8 | 2^-13 | 8.9e-9 | 120656 | 40219 | 11.5 |
| 8 | 1e-4 | 2^-8 | 2.5e-5 | 173608 | 24801 | 18.2 |
| 8 | 1e-6 | 2^-11 | 3.9e-7 | 238696 | 34099 | 32.1 |
| 8 | 1e-8 | 2^-14 | 6.1e-9 | 303784 | 43398 | 46.1 |
| 16 | 1e-4 | 2^-8 | 5.7e-5 | 372312 | 24821 | 198 |
| 16 | 1e-6 | 2^-11 | 8.9e-7 | 511896 | 34126 | 376 |
| 16 | 1e-8 | 2^-15 | 3.5e-9 | 698008 | 46534 | 556 |
| 32 | 1e-2 | 2^-5 | 7.7e-3 | 481144 | 15521 | 1.53e3 |
| 32 | 1e-4 | 2^-9 | 3.0e-5 | 865912 | 27933 | 1.92e4 |
| 32 | 1e-6 | 2^-12 | 4.7e-7 | 1154488 | 37242 | 3.96e4 |
| 32 | 1e-8 | 2^-15 | 7.3e-9 | 1443064 | 46551 | 6.01e4 |
| 64 | 1e-4 | 2^-9 | 6.2e-5 | 1760056 | 27937 | 1.47e8 |
| 64 | 1e-6 | 2^-12 | 9.7e-7 | 2346616 | 37248 | 3.34e8 |

Observations.

- The gap is about `0.24 (n-1) h^2` in every row with small `h` (for
  example `7.3e-9` against `0.24 * 31 * 2^-30 = 6.9e-9`). This is the
  `|T| h^2` accumulation of Theorem 3.4 and is why `h` must scale like
  `sqrt(eps/n)`.
- The size per bag is about `3.1e3` per halving of `h` and depends on `n`
  only through `j`, so the total is `Theta(n log(n/eps))`, as Theorem 3.4
  predicts.
- **Absolute sizes.** The computed certificates are small compared with the
  proof's constant (Theorem 4.1(b)) but not small compared with the
  single-tree lower bound at moderate `n`. At `eps = 1e-6` the decomposition
  certificate has about `3.7e4` leaves per bag, and Corollary 2.1's bound
  overtakes the computed certificate size only near `n ≈ 45–50`
  (`L_40 = 3.9e5`, `L_60 = 1.1e8`; 46 in the review's exact computation). At
  `n = 64` Corollary 2.1's bound
  is 140 times the computed certificate size (`3.3e8` against `2.3e6`). With
  the face-exact term of Theorem 4.1(a), the proven single-tree bound
  overtakes the computed certificates already at `n = 29` (`eps = 1e-6`).
  The separation is asymptotic. Two caveats cut the other way. The proven
  bounds are lower bounds: the review's toy bisection B&B with the same
  relaxation needs 199,240 leaves at `n = 9`, `eps = 1e-4`, against 198,446
  for the computed certificate (and the program's SCIP probe needed `2.9e4`
  nodes at `n = 10` with other relaxations). And the shell certificates are
  not optimized (uniform `theta` in all directions and over the whole bag
  box).

**The `theta` threshold** (`logs/debug_n_theta.log`, `logs/E5_theta_threshold.log`).
Root gap at `h = 2^-8`, `c = 0`:

| theta | n = 16 | 18 | 20 | 24 | 28 | 32 | 48 | 64 |
|---|---|---|---|---|---|---|---|---|
| 1/8 | 5.7e-5 | 1.25e-2 | 2.50e-2 | 5.00e-2 | 7.50e-2 | 1.00e-1 | 2.00e-1 | 3.00e-1 |
| 1/16 | 5.7e-5 | 6.5e-5 | 7.3e-5 | 8.9e-5 | 1.04e-4 | 1.20e-4 | 1.84e-4 | 2.47e-4 |
| 1/32 | 5.7e-5 | 6.5e-5 | 7.3e-5 | 8.9e-5 | 1.04e-4 | 1.20e-4 | – | – |

With `theta = 1/8` the gap grows by `0.00625` per added variable beyond
`n = 16`; with `theta <= 1/16` it grows like `|T| h^2` only. The minimizing
configuration at `theta = 1/8` (`trace_config.py`,
`logs/trace_n20_mu3.log`) alternates `x_t ≈ ±0.5` with copies of `x_{t+1}`
at `∓0.625`: each parent leaf touches the next child cell only at a face,
the drift is `0.125`, and each bag evaluates
`phi(0.5) + 0.8 * 0.5 * (-0.625) ≈ -0.00625` instead of a positive margin
(Remark 3.6). The chain pays a fixed entry and exit cost, which is why the
effect starts only at `n ≈ 16`.

## 6. Limitations and open problems

1. **Relaxation class and factorization.** Corollary 2.1 needs the alphaBB
   gap in every coordinate; the face-exact note's Theorem 1 extends the
   single-tree bound, without the `log(1/eps)` factor, to every relaxation
   with a termwise McCormick-size gap, so Theorem 4.1 holds for termwise
   McCormick. alphaBB on an isolated bilinear term is dominated by McCormick
   (its convex envelope) and is not used by solvers. The bounds are about a
   fixed termwise relaxation and factorization:
   - SCIP's default PSD-minor cuts escape both single-tree bounds (face-exact
     note, Section 7.4), and so do cuts on aggregated expressions and
     convexity detection; the SCIP probe counts are therefore not explained
     by Theorem 4.1;
   - merging the unary terms into the bilinear factors ("balanced split",
     Section 4.1) removes the proved `eps`-dependent mechanism; the toy
     single tree still grows about 2.3–2.5 times per variable, but no lower
     bound is proved for that growth (open);
   - with arbitrary functional splits no lower bound can hold uniformly
     (Observation 4.2).
2. **Constants.** Theorem 3.4's constants are far from sharp: (T2) asks for
   `theta = 2^{-10}` on the path family, while `theta = 1/16` works in the
   computations. The base of the exponential, a condition number raised to
   the power `w+1`, is plausible in form (Remark 3.6 shows the dependence on
   `M_a/c_g` is real) but not shown to be necessary.
3. **Knowledge of `x*`.** The certificate is centered at a point within `h`
   of `x*` and uses multipliers accurate to `O(sqrt(eps))`. Theorem 3.4
   bounds the size of the certificate, not the work of an algorithm that has
   to find such a point. An adaptive algorithm is only sketched here
   (Section 3.4); `extension-adaptive.md` (Theorem A.5) proves one with size
   `O(|T| (C sqrt|T|)^{w+1} log(|T|/eps))`, and matching Theorem 3.4 without
   `x*` remains open.
   Certifying that a local solution is global is the whole difficulty, so
   this gap matters.
4. **Uniqueness.** The instance-dependent bound needs (QG) to a single
   point. For optimal sets of positive dimension, multipliers vary along the
   set and one slope per separator is not enough; Conjecture 3.7 is open.
   Degenerate instances are covered only by the worst-case bound
   (Theorem 3.3) and the flat lower bound (Proposition 2.4). Even with a
   unique minimizer, `c_g` is a global constant and can be tiny: a second
   local minimizer with value `f* + delta` at distance `D` forces
   `c_g <= delta/D^2`, so the base becomes at least
   `(C M_a D^2/delta)^{w+1}`, no better in form than Theorem 3.3 when
   `delta ~ eps`. A stronger version would use local (QG) near `x*` plus a
   margin away from it, with `theta` growing with the distance, or
   multi-center shells with slopes per region; the latter runs into the
   mismatch terms of Conjecture 3.7, obstacle (i).
5. **Worst-case exponent.** Theorem 3.3 has `eps^{-(w+1)}`; the lower bound
   of Proposition 2.4 has `eps^{-(w+1)/2}`. Closing this gap needs a way to
   handle concave kinks of value functions.
6. **Shared tolerance.** The covering lower bound (Theorem 2.5) gives each bag
   the whole tolerance. Only for products (Proposition 2.4) is the sharing
   proved.
7. **Proposition 2.6** is proved for a child of the root with a
   one-dimensional separator; deeper nodes are sketched only.
8. **Fixed decomposition and cost measure.** The certificate is tied to one
   tree decomposition; the choice matters, and search tied to a fixed
   decomposition can lose to dynamic orderings in the discrete setting
   (Bacchus–Dalmao–Pitassi; literature audit, C4). Sizes count leaves and
   cells; per-leaf work (low-dimensional convex programs) is not counted,
   which favours the single tree. Single trees that represent many children
   implicitly (MUSE-BB) are not covered by the single-tree lower bound in
   its current cost measure.
9. **Clique families with pairwise factors.** Propositions 2.3 and 2.4 use
   one factor per block. For a clique of pairwise factors, a decomposition may
   assign the pair factors to different bags, so no single bag need carry the
   gap in all clique coordinates. Lemma 1.4 still sums the gaps of all bags
   at each point, but the leaves involved belong to different bags, and the
   integral argument of Lemma 2.2 does not factor. A lower bound for that
   case is open.
10. **Integer variables.** Section 1.6 is a remark: the lemmas carry over, and
   fixing integer separator variables removes drift in those coordinates.
   No integer-specific lower bound is given.
11. **Novelty.** Worst-case bounds of the type of Theorem 3.3 are known
    (Zhang–Sun 2022; Bienstock–Muñoz; grid DP), and discrete separations for
    unpruned AND/OR search are classical (Dechter–Mateescu). The literature
    audit found no instance-dependent bound like Theorem 3.4 and no
    separation between single-tree and decomposition-aware spatial B&B with
    the same relaxations at a unique nondegenerate minimizer. Berenguel et
    al. (JOGO 2013), read in full by the recheck, is the precursor of the
    algorithm for one common variable (interval B&B with one list per
    subfunction, copy relaxation, zero-slope combined bounds; Section 1.5),
    with validity and pruning rules but no complexity results. An
    unsuccessful search does not establish novelty.

Open questions, in the order I would attack them:

- An adaptive algorithm (refinement of active leaves and cells) with a size
  bound comparable to Theorem 3.4, without knowledge of `x*`.
- A single-tree lower bound for the balanced split (Section 4.1) and for
  relaxations with PSD-minor cuts, to connect Theorem 4.1 to solver practice.
  (Termwise McCormick is covered by the face-exact note's Theorem 1.)
- Conjecture 3.7, starting with Morse–Bott optimal sets along a path.
- Whether `(C M_a/c_g)^{w+1}` is necessary, for example on a grid family
  where the bag lemma gives `(alpha/lambda)^{(w+1)/2}` only.

## 7. Commands run

All commands were run from
`research-20260929/theory-decomposition/` with Python 3.13, NumPy 2.5.1,
SciPy 1.18.0 and mpmath 1.3.0. These are targeted checks of this note only;
no project-wide verification was run and no CI results were consulted.

| Command | Log | Result |
|---|---|---|
| `python3 single_tree_lb.py` | `logs/single_tree_lb.log` | `L_n(eps)` table of Section 5.1; closed form below exact bound in every row; growth per variable `-> 1.3155`; threshold `\|b\| = 0.53334`; ellipsoid bound below full integral for `n = 2, 3` |
| `python3 run_experiments.py E3` | `logs/E3_validity.log` | no validity violation; `max(l - phi^grid) < 0` in all 8 runs |
| `python3 run_experiments.py E2` | `logs/E2_slopes.log` | affine slopes: gap `≈ 1.6 h^2`; zero slopes: gap stalls at `2.2e-3` |
| `python3 run_experiments.py E4` | `logs/E4_theta.log` | zero slopes: gap `∝ theta^2` down to the floor `2\|lambda\| h`; affine: `1.3e-9` for all `theta` |
| `python3 run_experiments.py E1` (with `theta = 1/16`, stopped after `n = 32`) | `logs/E1_scaling.log` | Section 5.4 table; gap `≈ 0.24 (n-1) h^2`; size `Theta(n log(n/eps))` |
| `python3 run_experiments.py E1b` | `logs/E1b_n64.log` | `n = 64` rows of Section 5.4 |
| inline sweep (same code as `E5`, `n = 16..32`, `theta = 1/8, 1/16, 1/32`) | `logs/debug_n_theta.log` | `theta` threshold table of Section 5.4 |
| `python3 run_experiments.py E5` | `logs/E5_theta_threshold.log` | `n = 32, 48, 64` at `theta = 1/8, 1/16` |
| `python3 trace_config.py 20 3 8` | `logs/trace_n20_mu3.log` | alternating drift configuration of Remark 3.6 |
| `python3 revision_checks.py` (after review) | `logs/revision_checks.log` | pair counts 3.04–4.81 times leaves; `n = 9` certificate 198,446 leaves, gap `2.9e-5`; crossovers 28/29 (face-exact vs computed), 49–50 (face-exact vs Theorem 4.1(b)), 85–89 (Corollary 2.1 vs (b)); uniform ratio `>= 1.26e-9 (2e/pi)^{n/2}/sqrt(n)` on the grid; factorization bases 1.3155, 1.034, 0.780, 0.930, 0 |
| after the non-dyadic check: `python3 run_experiments.py E2` (widened pair test) | `logs/E2_slopes.log` (replaced) | zero-slope gaps at `h = 2^-2, 2^-4`: `1.876e-1`, `3.174e-2` (first version `1.719e-1`, `3.122e-2`); every other line identical (`diff`) |
| after the non-dyadic check: `python3 run_experiments.py E3`; `python3 run_experiments.py E4` (widened pair test) | compared with `logs/E3_validity.log`, `logs/E4_theta.log` (kept) | output identical, all 8 E3 runs and all 6 E4 rows (`theta = 1/2 … 1/64`) |
| after the non-dyadic check: `python3 revision_checks.py` (widened pair test) | compared with `logs/revision_checks.log` (kept) | identical (`x* = 0`) |
| after the non-dyadic check: `python3 check_pairs_exact.py` | `logs/check_pairs_exact.log` | 20 partitions of E2, E3, E4 and `x* = 0`: the unwidened test missed 26–7,657 touching pairs per certificate of Sections 5.2–5.3 (30,442 at `theta = 1/64`), 0 at `x* = 0`; none with positive overlap, none spurious; widened set = exact set in all 20; smallest gap between non-meeting boxes `9.5e-7`; largest edge rounding error `2.2e-16` |
| after the non-dyadic check: inline evaluation of the E2 certificates at `h = 2^-2, 2^-4` with `PAIR_TOL = 0` and `1e-12` | none | zero-slope gaps `1.7193e-1 -> 1.8756e-1` and `3.1222e-2 -> 3.1740e-2`; affine `1.02928e-1 -> 1.02942e-1` and `6.42227e-3` (unchanged) |
| after the confirmation: `python3 compare_pair_tol.py` (about 4 min) | `logs/compare_pair_tol.log` | roots with `PAIR_TOL = 0` and `1e-12` at full precision for all E2, E3 and E4 certificates except E4 at `theta = 1/64`: of 32 with non-dyadic `x*`, the unwidened root is higher in 3 (E2 at `h = 2^-2`, both slopes; `h = 2^-4`, zero slopes) and bit-identical in 29; the two E3 certificates at `x* = 0` are identical |
| after the confirmation: `python3 run_experiments.py E2` (after the docstring edit) | compared with `logs/E2_slopes.log` (kept) | identical (`diff`) |
| after the second confirmation: inline driver that loads `chunked()`, the row-chunked copy of `certificate()` in `reviews/decomposition-nondyadic-confirm-r2-checks/all_roots.py`, and evaluates E4 at `theta = 1/32` and `1/64`, both slopes, `PAIR_TOL = 0` and `1e-12` (17 min, peak memory 0.84 GB) | `logs/theta64_chunked.log`, `logs/theta64_chunked.time` | `theta = 1/32`: all four roots equal those of `logs/compare_pair_tol.log` (original `certificate()`); `theta = 1/64`: roots bit-identical at both tolerances, `-0.0097876251980369196` (affine) and `-0.0097914614120943721` (zero), as in the second confirmation; gaps `1.268e-09`, `3.837e-06` and size 1,374,385, as in `logs/E4_theta.log` |
| after the second confirmation: inline `shells()` at `theta = 1/64` | none | bag 0 has 686,738 leaves and its separator 1,793 cells: 9.85 GB for a dense `float64` array, 1.23 GB for each Boolean array |

A first run of `E1` with `theta = 1/8` (log not kept) gave a root gap of
`0.09998` at `n = 32` for every `h`; investigating it produced Remark 3.6 and
the threshold table. The scripts are `single_tree_lb.py`,
`dp_certificate.py` (certificate DP, shell partitions, grid value
functions), `run_experiments.py` and `trace_config.py`.

## 8. Revision after review

The review ([`reviews/decomposition-review.md`](../reviews/decomposition-review.md),
checks in `reviews/decomposition-review-checks/`) verified all proofs and
constants. Changes made, each checked against the review's logs or by
`revision_checks.py`:

1. **Uniformity in Theorem 4.1.** The claim "uniformly in `eps <= 0.2/n`"
   was false with the closed form, which is 0 at `eps = 0.2/n`. Theorem
   4.1(a) now takes the maximum of the Corollary 2.1 closed form and the
   face-exact bound, and the ratio statement is
   `N_single/N_dec >= 3e-10 (2e/pi)^{n/2}/sqrt(n)` for every `eps <= 1e-4`,
   with a two-regime proof (`eps <= 0.04/n^2` uses Corollary 2.1, larger
   `eps` uses the face-exact bound). A grid check gives `1.26e-9` as the
   smallest constant.
2. **Remark 3.5.** Removed "`theta = 1/2` works" (contradicted by
   Section 5.4); now `theta = 1/16` works for all tested `n` and `1/8` fails
   for `n > 16`. The center accuracy is stated in sup-norm,
   `|x̂ - x*|_inf <= h_0 = O(sqrt(eps/|T|))`; a Euclidean `O(sqrt(eps))` error
   is not enough. Remark 3.6 cites the review's `b` sweep.
3. **Counting convex programs.** Replaced "counting relaxation solves only
   strengthens the separation" by the pair count: one convex program per
   (leaf, cell) pair, 3.04–4.81 times the leaves at `h = 2^-4..2^-14`
   (`theta = 1/16`), growing like `log(1/h)`, so `log^2` programs overall.
   The review's one-program-per-leaf variant is mentioned, with constants
   not written out. The same point is added to the "Checking" remark of
   Section 1.3.
4. **Proposition 2.3.** The Summary and status table now say that
   `exp(Omega(w))` holds only when `alpha/lambda_geo > pi/(4e)`.
5. **Stronger single-tree bound and McCormick.** The note's relaxation
   satisfies (M_b) (`(|b|/2)(a_i + a_{i+1}) >= |b| d_i d_{i+1}`), so the
   face-exact note's Theorem 1 gives `(5/3)^n exp(-(5/9)(1 + 1.25 eps)) >=
   0.57 (5/3)^n` for `eps <= 1e-4`; it covers termwise McCormick, so the
   separation holds for termwise McCormick (ratio `c (5/3)^n/(n log(n/eps))`,
   exponential for each `eps` but not uniform as `eps -> 0`, because
   Corollary 2.1 and part (c) need the alphaBB gap). Crossovers recomputed: the
   face-exact bound exceeds the computed certificates from `n = 29`
   (`eps = 1e-6`) and Theorem 4.1(b) from `n = 49`. The review's toy
   bisection tree exceeds the computed certificate at `n = 9` (199,240
   against 198,446 leaves; the certificate count was recomputed here).
   Sections 2.1, 4, 5.4, 6 and the Summary are updated. The face-exact
   theorem is imported, not re-proved here.
6. **Factorization dependence (new Section 4.1).** Bases for other
   factorizations (recomputed); the balanced split removes the proved
   mechanism, and the eps-independent growth seen in the review's toy runs
   is stated as open. Observation 4.2 (checked here): with arbitrary splits,
   splitting by the conditional margins of Lemma 1.1 makes per-factor
   envelopes exact at the root; equivalently, locally consistent bag
   measures glue on a tree, so the local-consistency relaxation is exact. No
   lower bound can hold uniformly over splits.
7. **Significance.** A paragraph in the Summary: Theorem 3.4 is the main new
   result; the separation is rigorous but relative to a fixed termwise
   relaxation and factorization; SCIP's PSD-minor cuts escape both
   single-tree bounds.

Smaller changes: Proposition 2.4's tightness is "in `K` and `eps`, up to
factors `C^d`"; Section 1.6 notes that configurations range over continuous
hulls; Section 5.2 notes that the grid validity check is one-sided and cites
the review's sharper check; Section 6, item 4 states how a small global
`c_g` (a second local minimizer at `f* + delta`, distance `D`) degrades
Theorem 3.4 to `(C M_a D^2/delta)^{w+1}`.

### 8.1 Second round, after the recheck

The recheck ([`reviews/decomposition-recheck.md`](../reviews/decomposition-recheck.md))
confirmed the proofs and the first-round changes, and asked for four fixes,
all made:

1. **Base rounding.** `sqrt(2e/pi) = 1.3154892`, and the ratio statements
   used `1.3155^n`, which rounds the base up; the statement then fails for
   `n >~ 2.8e5` at astronomically small `eps`. All ratio statements now use
   `(2e/pi)^{n/2}` (Summary item 5, status table, Theorem 4.1, this
   section), and case 1 of the proof gives `3.1e-10` (`0.034/1.07e8 =
   3.18e-10`) instead of `3.2e-10`. Re-verified: case 1 gives
   `3.18e-10 (2e/pi)^{n/2}/sqrt(n)`; case 2 (nonempty only for `n >= 21`)
   gives at least `1.16e-9` times the same, with base
   `(5/3)/sqrt(2e/pi) = 1.26696` and the normalized ratio increasing in `n`
   (checked for `3 <= n < 2000` and by the derivative argument). So the
   stated `3e-10 (2e/pi)^{n/2}/sqrt(n)` holds for all `n >= 3` and
   `eps <= 1e-4`. The grid check in `revision_checks.py` already normalized
   by `(2e/pi)^{n/2}`.
2. **Observation 4.2.** The decomposition side needs `2|T| - 1` members
   (one leaf per bag, one cell per separator), not one node; the root-bound
   step now reads `>=` and adds `<= F(x*) = f*`; the measure form is called
   the dual and cites Vorob'ev (1962) and Lasserre (2006); a scope paragraph
   says it rules out lower bounds uniform over all splits for relaxations
   exact at factor minima (convex envelopes) and says nothing about fixed
   rules such as alphaBB or restricted split classes.
3. **Center in `X0`.** Theorem 3.4 now requires `x̂ in X0` (Lemma 3.1
   assumes the center lies in the box, and the gradient bounds are on
   `X0`). The summary base `O(M_a sqrt(w)/c_g)` is qualified by
   `alpha' A <~ w M_a^2/c_g`.
4. **Berenguel et al. (2013).** Cited in Section 1.5 as the precursor of
   the algorithm for one common variable, and in Section 6, item 11; the
   earlier "not done" remark is removed. The possible link between their
   losses at tight tolerance and Proposition 2.6 is not claimed (the
   recheck did not check their separator multipliers).

### 8.2 Third round, after the non-dyadic check

The check of the computations centred at a non-dyadic `x*`
([`reviews/decomposition-nondyadic-check.md`](../reviews/decomposition-nondyadic-check.md))
asked whether the closed (leaf, cell) test of `dp_certificate.py` loses
pairs through rounding, as the first RC runs of `extension-adaptive.md` did.
It found two table entries to correct and asked for six changes. Each was
verified here independently: `check_pairs_exact.py` (new) evaluates the pair
test on exact rational edges with its own code, and E2, E3, E4 and
`revision_checks.py` were rerun with the widened test (Section 7). The proofs
were not touched except for the new remark after Lemma 1.3.

1. **Section 5.3, `n = 8` table.** The zero-slope gaps are now `1.88e-1` at
   `h = 2^-2` and `3.17e-2` at `h = 2^-4` (full precision `1.8756e-1` and
   `3.1740e-2`; first version `1.7193e-1` and `3.1222e-2`). The affine gap
   at `h = 2^-2` moves from `1.02928e-1` to `1.02942e-1` and still prints as
   `1.03e-1`. No other cell changes. The text below the table (`≈ 1.6 h^2`,
   the stall at `2.2e-3`) still holds. Checked by the E2 rerun and by
   evaluating both certificates with `PAIR_TOL = 0` and `1e-12`.
2. **Section 5, opening paragraph.** It now says that pairs are found by a
   closed test on rounded edges, what the unwidened test missed, and that
   the first-version values were valid lower bounds. Checked with
   `check_pairs_exact.py`: the unwidened test missed 1,173, 4,294, 6,170
   and then 6,458 touching pairs per E2 certificate (`h = 2^-2, 2^-4, 2^-6`,
   then `2^-8 … 2^-16`), 1,626, 3,732, 545 and 0 in E3, and 26, 118, 479,
   1,936 and 7,657 in E4 (`theta = 1/2 … 1/32`; 30,442 at `theta = 1/64`,
   a row that is in the log but not in the note). It missed no pair with
   positive-length overlap and added no spurious pair. The widened pair set
   equals the exact one in all 20 partitions checked, including two at
   `x* = 0`, where nothing is missed. The smallest gap between a leaf and a
   cell that do not meet is `9.5e-7`, far above `1e-12`, and the largest
   rounding error of an edge is `2.2e-16`. These counts agree with the
   check's.
3. **Validity of the first-version values (remark after Lemma 1.3,
   new).** (LC) and (CM) are needed only for pairs whose interiors meet.
   Since no such pair was lost, the first-version values were gaps of valid
   bounds. These bounds are at least the bound of Lemma 1.5; they were
   higher in the three E2 certificates of item 1 and identical at full
   precision in the other 31 E2, E3 and E4 certificates with non-dyadic
   `x*` (Sections 8.3 and 8.4). The
   argument follows the check's Section 4.3 and was written out and
   checked here. Definition 1.2 and the lower bounds of Section 2 are
   unchanged. The status table notes the remark in the row of Lemma 1.3.
4. **`dp_certificate.py`.** Both closed tests in `certificate()` are
   widened by `PAIR_TOL = 1e-12`, as in `adaptive/ls_lib.interval_pairs`,
   so reruns compute the certificate of Lemma 1.5. Only `run_experiments.py`
   and `revision_checks.py` call `certificate()` (checked by `grep`). The
   other importers (`trace_config.py`, `adaptive/rc_lib.py`,
   `adaptive/ls_lib.py`, `adaptive/check_staircase.py`) use `shells()` and
   other helpers, which did not change.
5. **Logs.** `logs/E2_slopes.log` is replaced by the rerun; `diff` shows
   only the two changed entries. The first-version output is reproduced in
   the check's `logs/E2_closed.log`. E3, E4 (all six rows) and
   `revision_checks.py` print identical output with the widened test, so
   their logs are kept.
6. **Bearing on `extension-adaptive.md` (not edited here).** Its
   Section A.5 says that a dropped touching pair makes the computed `l_r`
   "too high, so it is not a valid bound". By the remark after Lemma 1.3,
   such an `l_r` can be higher than the bound Lemma 1.5 defines but remains
   valid as long as no pair with positive-length overlap is lost. That
   condition was verified here only for this note's runs, not for RC. The
   `adaptive/rc_lib.py` docstring says only that the dropped pair "makes l_r
   too high", which is correct, so it needs no change. Section D of
   `extension-adaptive.md` says that the non-dyadic computations of this
   note were not checked; items 1 and 2 answer that. The extension note is
   left to its own revision.

### 8.3 Fourth round, after the confirmation of Section 8.2

The confirmation
([`reviews/decomposition-nondyadic-confirm-r1.md`](../reviews/decomposition-nondyadic-confirm-r1.md))
found the changes of Section 8.2 correct and reported two wording errors.
Both were verified here and fixed. No number in a table, no proof and no
status-table entry changes.

1. **Section 8.2, item 6 misquoted `adaptive/rc_lib.py`.** It said that the
   `rc_lib.py` docstring calls such an `l_r` "not a valid bound". The
   docstring says only "(which makes l_r too high)", which is correct, and
   the file was last changed (10:16) before the check was written (11:21).
   Only Section A.5 of `extension-adaptive.md` says "not a valid bound".
   The error came from the check's Section 4.3. Item 6 now quotes
   Section A.5 only, says that the `rc_lib.py` wording is correct and needs
   no change, and says "can be higher" instead of "is higher". Checked by
   `grep` of both files and by their modification times.
2. **`dp_certificate.py` docstring.** "which gives a bound higher than
   Lemma 1.5's" now reads "which can give a bound higher than Lemma 1.5's".
   `compare_pair_tol.py` (new) evaluates the E2, E3 and E4 certificates
   with `PAIR_TOL = 0` and `1e-12` and prints the roots at full precision.
   Of the 32 with non-dyadic `x*`, the unwidened root is higher in 3 (E2 at
   `h = 2^-2`, affine and zero slopes, by `1.38e-5` and `1.56e-2`; E2 at
   `h = 2^-4`, zero slopes, by `5.18e-4`), bit-identical in 29 and lower in
   none. The confirmation's 34 certificates are these 32 plus the two E3
   certificates at `x* = 0`. The two E4 certificates at `theta = 1/64` were
   not recomputed in this round: the dense pair arrays of `certificate()`
   need more than 10 GB there. The earlier E4 rerun (Section 7) printed the
   same gaps for them to four significant digits; Section 8.4 adds their
   full-precision roots. Rerunning E2 after the edit reproduces
   `logs/E2_slopes.log`.
3. **Section 8.2, item 3** had the same overstatement: it called the
   first-version bounds "higher than the bound of Lemma 1.5". It now says
   they are at least that bound, higher in the three E2 certificates above
   and identical in the 29 others recomputed. Checked by the same run.
4. **Header.** It now cites the confirmation and says that the fixes of
   Sections 8.1 and 8.3 have not been rechecked.

### 8.4 Fifth round, after the second confirmation

The second confirmation
([`reviews/decomposition-nondyadic-confirm-r2.md`](../reviews/decomposition-nondyadic-confirm-r2.md))
found the changes of Section 8.3 correct, reproduced every changed number bit
for bit, and reported one misstatement. It was verified here and fixed. No
number in a table, no proof and no status-table entry changes.

1. **Section 8.3, item 2 misstated the first confirmation's count.** It said
   that the first confirmation's count of 34 includes the two E4
   certificates at `theta = 1/64`. It does not. That confirmation's
   `run_all.sh` runs E4 only for `theta = 1/2 … 1/32` (`run_tol.py 1e-12
   E4m5`, `mu = 1..5`), its E4 log has five rows, and it lists "The E4 root
   at `theta = 1/64`" under "Not rechecked here". Its 34 certificates are the
   16 E2, the 8 E3 (two of them at `x* = 0`) and the 10 E4 certificates at
   `theta = 1/2 … 1/32`: the 32 with non-dyadic `x*` of Section 8.3 plus the
   two E3 certificates at `x* = 0`. So its count (higher in 3 of 34, the
   other 31 identical) is the count of Section 8.3 (3 higher, 29 identical)
   plus the two certificates at `x* = 0`. The clause is deleted,
   and item 2 now says what the 34 are. Checked by reading the first
   confirmation's `run_all.sh`, `run_tol.py`, `logs/E4m5_tol1e-12.log` and
   Section 4, and by counting the certificates that `E2()`, `E3()` and
   `E4()` of `run_experiments.py` build.
2. **Roots at `theta = 1/64` (new).** The second confirmation (its
   Section 2.1) evaluated the two E4 certificates at `theta = 1/64` with a
   row-chunked copy of `certificate()` and found bit-identical roots at both
   tolerances. The copy splits the leaf rows into blocks of 20,000 and
   otherwise uses the same comparisons, pair order and `min_subbox` calls
   (read here against `certificate()`); the second confirmation checked it
   bit for bit against the original on the other 34 certificates. Rerun here
   with the same copy (Section 7): at `theta = 1/64` the roots are
   `-0.0097876251980369196` (affine) and `-0.0097914614120943721` (zero) at
   both tolerances, as in the second confirmation, and the gaps and size
   match `logs/E4_theta.log`. A control run at `theta = 1/32` gives exactly
   the roots of `logs/compare_pair_tol.log`. So of the 34 E2, E3 and E4
   certificates with non-dyadic `x*`, the unwidened root is higher in 3 and
   bit-identical in 31; none is lower. Section 8.3, item 2 now points here,
   and Section 8.2, item 3 now says "identical at full precision in the
   other 31" instead of "identical in the 29 other certificates recomputed
   at full precision (Section 8.3)". Section 8.3, item 3 records the earlier
   wording and is left as it was.
3. **Memory estimate.** Section 8.3, item 2 and the `compare_pair_tol.py`
   docstring said that the dense pair arrays of `certificate()` need about
   20 GB at `theta = 1/64`. Bag 0 has 686,738 leaves and its separator
   1,793 cells (computed here with `shells()`), so the dense `float64` array
   `np.where(meet, cbeta, inf)` alone takes 9.85 GB, and each Boolean array
   1.23 GB; the second confirmation estimates about 14 GB. Both places now
   say "more than 10 GB", and the docstring points to
   `logs/theta64_chunked.log`. Only the docstring changed, so the script's
   output does not change (the file still parses).
4. **Header.** It now cites the second confirmation and says that the fixes
   of Sections 8.1 and 8.4 have not been rechecked.


*Root edit (2026-09-30):* Section 8.4 item 1 reworded as suggested by the
third confirmation (`reviews/decomposition-nondyadic-confirm-r3.md`): the two
counts cover 34 and 32 certificates, and the first confirmation's wording is
paraphrased, not quoted. No number or conclusion changed.

### 8.5 Root edits in the closing revision (2026-09-30)

- **Header.** It now says that the third confirmation checked Section 8.4
  and that only the Section 8.1 fixes (base rounding, `x̂ in X0`, the scope
  of Observation 4.2, Berenguel et al.) remain unrechecked.
- **Pointer to the extension.** The Summary's "Significance" and "Not
  proved" paragraphs, the status row of Section 3.4 and Section 6, item 3
  now point to `extension-adaptive.md`, whose Theorem A.5 proves an adaptive
  algorithm without knowledge of `x*` with size
  `O(|T| (C sqrt|T|)^{w+1} log(|T|/eps))` (under the hypotheses of
  Theorem 3.4 plus monotone relaxations). Matching Theorem 3.4 without `x*`
  remains open. No result of this note changes.
- **Table rendering (closing audit, 2026-09-30).** In the status table
  (Status section) and the table of commands (Section 7), the `|` characters
  inside code spans (`|T|`, `|b|`, `|lambda|`) split the rows into extra
  cells in GitHub-flavoured Markdown. They are now escaped as `\|`. The
  text is unchanged.
