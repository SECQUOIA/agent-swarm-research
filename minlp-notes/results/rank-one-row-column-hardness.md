# Linear optimization over rank-one matrices with row and column sum bounds is strongly NP-hard

Status: proof checked by an independent agent, with corrections applied; computationally
sanity-checked; not externally refereed. An open-literature search on 2026-09-04 found no prior
resolution; this is a novelty assessment, not a guarantee. Theorem 1 proves the conjecture
stated by Dey, Kocuk and Santana (J. Global Optim. 77:227–272, 2020, Section 3.1, after
Theorem 4; arXiv:1902.00739) — local copy
`literature/papers/dey2020-convexifications-of-rank-one-based/`.

## Setting

For bound vectors `l ≤ u` in `R^{n1}_+` and `l' ≤ u'` in `R^{n2}_+` define, as in Dey–Kocuk–Santana,

```
U^row(l,u)   = { W ∈ R_+^{n1×n2} : l_i  ≤ Σ_j W_ij ≤ u_i  ∀i,  rank(W) ≤ 1 },
U^col(l',u') = { W ∈ R_+^{n1×n2} : l'_j ≤ Σ_i W_ij ≤ u'_j ∀j,  rank(W) ≤ 1 }.
```

These are the rank-one substructures of the pooling problem: `W_ij` is the flow from input
`i` through a pool to output `j`; proportional splitting at the pool forces `rank(W) ≤ 1`;
row bounds are input-flow bounds, column bounds are output-flow bounds. Dey–Kocuk–Santana
show that `conv U^row` and `conv U^col` are polyhedral with polynomial-time separation, that for
`n1 = n2 = 2` the set `conv(U^row ∩ U^col)` is SOC-representable and need not be polyhedral, and
conjecture that linear optimization over `U^row ∩ U^col` is NP-hard. Jalilian and Kocuk
(Optim. Eng. 27:317–367, 2026; online 2025; arXiv:2306.10810) give an SOC representation of the hull of the set with
row, column and total-sum bounds whose size is exponential in `n1, n2`.

Problem (P): given `C ∈ Q^{n1×n2}` and finite nonnegative rational bounds, compute `min { ⟨C,W⟩ : W ∈ U^row(l,u) ∩ U^col(l',u') }`.

## Lemma 1 (parametrization by row and column sums)

Let `W ≠ 0` be in `U^row ∩ U^col`, let `r_i = Σ_j W_ij`, `c_j = Σ_i W_ij` and `S = Σ_i r_i = Σ_j c_j > 0`.
Then `W = r cᵀ / S`. Conversely, for every `r ∈ [l,u]`, `c ∈ [l',u']` with `Σ_i r_i = Σ_j c_j = S > 0`,
the matrix `r cᵀ / S` lies in `U^row ∩ U^col` and has row sums `r` and column sums `c`.
Consequently

```
U^row ∩ U^col  \ {0}  =  { r cᵀ / S :  r ∈ [l,u],  c ∈ [l',u'],  eᵀr = eᵀc = S > 0 },
⟨C, r cᵀ / S⟩ = rᵀ C c / S .
```

Proof. A nonzero nonnegative rank-one matrix can be written `W = x yᵀ` with `x, y ≥ 0`
(pick an entry `W_ij > 0`, flip the sign of both factors if needed; then `W_kj = x_k y_j ≥ 0`
with `y_j > 0` gives `x_k ≥ 0` for all `k`, and similarly `y ≥ 0`). Then `r_i = x_i (eᵀy)`,
`c_j = y_j (eᵀx)`, `S = (eᵀx)(eᵀy)`, so `r_i c_j / S = x_i y_j = W_ij`. The converse is a direct check. ∎

So (P) is the bilinear fractional program

```
min  rᵀ C c / (eᵀ r)   s.t.  r ∈ [l,u],  c ∈ [l',u'],  eᵀ r = eᵀ c,          (P')
```

together with the value `0` for `W = 0` when `0 ∈ [l,u] × [l',u']` (the constraint `S > 0` is open,
but values along `S → 0` tend to `0`, so the minimum over the compact `W`-space is the minimum of
the infimum of (P') and, if feasible, `0`).

## Theorem 1 (strong NP-hardness)

Problem (P) is strongly NP-hard. More precisely, the decision problem "is the optimal value of
(P) at most 0?" is NP-hard already when all bounds are in `{0,1}` and every entry of `C` is an
integer of absolute value at most `max(n1,n2)^2`.

Proof. Reduction from MAXIMUM EDGE BICLIQUE (Peeters, Discrete Appl. Math. 131:651–654, 2003):
given a bipartite graph `G = (L ∪ R, E)` and an integer `k` (WLOG `1 ≤ k ≤ |E|`), decide whether
there are `A ⊆ L`, `B ⊆ R` with `A × B ⊆ E` and `|A|·|B| ≥ k`. This problem is NP-complete; since its
only numerical datum is `k ≤ |E|`, it is strongly NP-complete.

Let `p = |L|`, `q = |R|`, `n = max(p,q)`, `M = n^2`. Build an instance of (P) with
`n1 = 1 + p + n` rows and `n2 = 1 + q + n` columns, indexed as follows:

- row `0` and column `0` are *fixed*: `l_0 = u_0 = 1`, `l'_0 = u'_0 = 1`;
- rows `1..p` correspond to `L`, columns `1..q` correspond to `R`, with bounds `[0,1]`;
- the remaining `n` rows and `n` columns are *dummies* with bounds `[0,1]`.

Cost matrix: `C_00 = k`; for `i ∈ L`, `j ∈ R`: `C_ij = −1` if `(i,j) ∈ E` and `C_ij = M` otherwise;
all other entries (fixed row/column against `L`, `R` or dummies, and all dummy entries) are `0`.

Because the fixed row has a positive lower bound, `W = 0` is infeasible, so by Lemma 1 the
optimal value of (P) is `min rᵀ C c / S` over (P'). Since `S > 0`, the optimal value is `≤ 0`
iff there is a feasible `(r,c)` with `N(r,c) := rᵀ C c ≤ 0`. Writing `x ∈ [0,1]^p` for the
`L`-part of `r` and `y ∈ [0,1]^q` for the `R`-part of `c`, and using `r_0 = c_0 = 1`,

```
N(r,c) = k + Σ_{i∈L, j∈R} C_ij x_i y_j =: k + Q(x,y),
```

which does not depend on the dummy entries.

Claim A (dummies decouple the coupling constraint). For every `(x,y) ∈ [0,1]^p × [0,1]^q`
there are dummy values making `(r,c)` feasible for (P'): the dummy rows must contribute
`eᵀy − eᵀx` more than the dummy columns, which is achievable because each dummy block can take
any total in `[0,n]` and `|eᵀy − eᵀx| ≤ n`. Hence the feasible `(x,y)` in (P') are exactly
`[0,1]^p × [0,1]^q`.

Claim B (vertex property). There is a feasible `(x,y)` with `k + Q(x,y) ≤ 0` iff there is a
binary one. Indeed, `Q` is linear in `x` for fixed `y`, so minimizing over `x ∈ [0,1]^p` attains
at a vertex `x' ∈ {0,1}^p` with `Q(x',y) ≤ Q(x,y)`; then minimizing over `y` with `x'` fixed
gives `y' ∈ {0,1}^q` with `Q(x',y') ≤ Q(x,y)`.

For binary `x = 1_A`, `y = 1_B`: `Q = −|E ∩ (A×B)| + M · |(A×B) \ E|`. If `A × B ⊄ E` then
`Q ≥ M − (|A||B| − 1) ≥ n^2 − n^2 + 1 = 1`, so `k + Q ≥ k + 1 > 0`. If `A × B ⊆ E` then `k + Q = k − |A||B|`,
which is `≤ 0` iff `|A||B| ≥ k`. Therefore the optimal value of (P) is `≤ 0` iff `G` has a
biclique with at least `k` edges. The construction is polynomial and all numbers are
polynomially bounded, which gives strong NP-hardness. ∎

Remarks.

1. The same construction with `C_00 = k` replaced by a general constant and with nonzero
   entries in the fixed row and column shows that every instance of *bipartite Boolean
   quadratic programming* `min { xᵀ Q y + aᵀx + bᵀy : x ∈ {0,1}^p, y ∈ {0,1}^q }` embeds in (P);
   the fixed row and column generate the linear terms and the constant, the dummies remove the
   coupling `eᵀr = eᵀc`. So the threshold question "is the optimum of (P) at most 0" is at least as
   hard as every bipartite Boolean quadratic threshold question. (No approximation-hardness
   statement is claimed: the objective of (P) is a ratio whose optimum changes sign.)
2. A weaker reduction from PARTITION needs no dummies. For positive integers `a_i`, set
   `A = Σ_i a_i`, use fixed row and column sums `r_0 = c_0 = 1`, and bounds
   `0 ≤ r_i,c_i ≤ a_i` for `i ≥ 1`. Set `C_ij = 1 − 1_{i=j}` on the number block,
   `C_i0 = a_i`, `C_0j = −A`, and `C_00 = A²/4`; scaling by four gives integer costs.
   Feasibility implies `s := Σ_{i≥1} r_i = Σ_{i≥1} c_i`, and
   `N(r,c) = (s − A/2)² + Σ_i r_i(a_i − c_i) ≥ 0`.
   Equality forces `s = A/2` and, whenever `r_i > 0`, `c_i = a_i ≥ r_i`.
   If `r_i = 0`, also `c_i ≥ r_i`; equality of the totals therefore forces `c_i = r_i`
   for every index. Thus each `r_i = c_i` is either `0` or `a_i`, giving a partition.
   Conversely a partition gives equality. This proves hardness in dimension `m+1` on each
   side even with the objective bounded below by zero throughout the feasible set.
3. Hardness also survives when *all* lower bounds are zero and all upper bounds
   are one. The exact penalty argument in `rank-one-zero-lower-hardness.md`
   removes the two fixed margins used here and preserves the reduction's
   inverse-polynomial decision gap. The relevant threshold is negative;
   feasibility of the zero matrix does not decide that question.

## Corollary 1 (no uniformly constructible, efficiently optimizable compact hull)

Unless P = NP, there is no polynomial-time algorithm that, given `n1, n2` and the bounds, writes
down an extended formulation of `conv(U^row(l,u) ∩ U^col(l',u'))` of polynomial size (number of
variables, constraints and coefficient bit-lengths) that is either polyhedral or conic with a
polynomial-time solver. Such an algorithm would solve the decision problem of Theorem 1: in a
"no" instance Claim B gives `N(r,c) ≥ 1` on the *whole* feasible set, so the optimum of (P) is at
least `1/S_max ≥ 1/(2n+1)`, while in a "yes" instance it is `≤ 0`; an absolute error at most `1/(8n+4)` in the
optimal value therefore decides the instance by comparison with `1/(4n+2)`, which is within reach of polynomial-time LP/conic
solvers (for the conic case under the usual well-posedness assumptions). This is consistent
with the SOC representation of Jalilian and Kocuk (arXiv:2306.10810) being exponential in the
dimensions, and shows that the SOC representation of Dey–Kocuk–Santana's Theorem 4 (the `2 × 2`
case) cannot be extended to an efficiently constructible polynomial-size family for general
`n1, n2`. (The existence of a small but non-constructible extended formulation is not excluded by
this argument; ruling that out would require an unconditional extension-complexity bound.)

## Theorem 2 (fixed number of rows or columns is polynomial)

For finite rational input, problem (P) admits an exact algorithm with running time
`d 2^d · poly(n1,n2,B)`, where `d = min(n1,n2)` and `B` is the total input bit length.
In particular, it is polynomial-time solvable for every fixed number of rows or columns.
An optimal solution can be encoded using rational numbers and at most one square root.

Proof. Transpose if needed so `m := n1 = d`, and set `N := n2`. The admissible totals form
`I = [max(eᵀl,eᵀl'), min(eᵀu,eᵀu')]`. If this interval is empty the problem is infeasible;
if `I = {0}`, its only feasible matrix is zero. In all other cases apply Lemma 1 for `S > 0`,
and include zero with objective value zero as a candidate when `0 ∈ I`.

Fix `S > 0`. The feasible margins are the independent polytopes
`P_S = [l,u] ∩ {eᵀr = S}` and `Q_S = [l',u'] ∩ {eᵀc = S}`. For fixed `r`, the minimization
`min_{c∈Q_S} rᵀCc` is continuous knapsack: order `w_j = (Cᵀr)_j` increasingly, start at `c=l'`,
and raise the entries to their upper bounds in that order until their sum reaches `S`.
The value `φ_S(r) = min_{c∈Q_S} rᵀCc` is concave in `r`, being a minimum of linear functions.
Its minimum on `P_S` therefore occurs at a vertex. Each such vertex has all but at most one
coordinate at a bound: two strictly interior coordinates could otherwise be perturbed in
opposite directions while preserving the sum, contradicting extremality.

Enumerate a free coordinate `k` and a choice of lower or upper bound for every other coordinate.
There are at most `m 2^{m−1}` patterns, including descriptions of vertices with every coordinate
at a bound. For each pattern, `r(S)` is affine in `S`, and its validity interval is obtained
by intersecting `I` with the lower and upper bounds on `r_k(S)`. Empty intervals are discarded.
The weights `w_j(S)` are affine. There are at most `N(N−1)/2` crossing totals unless two weights
are identical, in which case a fixed index order breaks ties. Partition the validity interval
at these rational crossings. Within each resulting interval the greedy order is constant;
the cumulative capacities give at most `N` further rational breakpoints. Thus there are
`O(N³)` intervals per row pattern on each of which both margins are affine in `S`.
Ties and interval endpoints cause no problem: each adjacent greedy order remains optimal
at a tie, and the affine descriptions agree in value there. Singleton intervals are also checked.

On such an interval the objective has the form
`f(S) = αS + β + γ/S` with rational coefficients. Evaluate positive endpoints, and also
`S = sqrt(γ/α)` when `α > 0`, `γ > 0`, and that point belongs to the interval.
These are all possible interior minima except a constant function, for which any feasible
point suffices. If `α,γ < 0`, the stationary point is a maximum and must not use the
minimum-value formula below. Degenerate zero coefficients give monotone or constant functions.
At an endpoint `S=0`, use the zero matrix: since `|⟨C,W⟩| ≤ max_ij|C_ij| S`, the objective
extends continuously there with value zero.

All rational breakpoints and coefficients have bit length polynomial in `B,n1,n2`: they use
only polynomially many sums, products, and divisions of the input rationals. Interior minimum
values are `β + 2 sqrt(αγ)` with `α,γ > 0`; endpoint values are rational. Ordering two candidates
uses sign checks followed by at most two squarings of rational expressions (equivalently,
comparison of real algebraic numbers of degree at most four), with polynomial bit complexity.
Checking interval membership for a positive square root uses a single squaring with the
appropriate sign checks. The chosen `S`, the affine margins, and `W = rcᵀ/S` consequently have
polynomial-size exact encodings in one quadratic number field. The enumeration factor is
`m 2^{m−1}`; all remaining work per pattern is polynomial with exponent independent of `m`.
This proves the claimed running time and exact output representation. ∎

## Corollary 2 (NP-completeness, rational certificates, and quadratic optima)

For arbitrary dimensions and finite rational data, deciding whether a feasible matrix has
`⟨C,W⟩ ≤ t`, for rational threshold `t`, belongs to NP. Together with Theorem 1, this decision
problem is strongly NP-complete. Every yes instance has a feasible matrix with entirely
rational entries and polynomial encoding length. Every nonempty instance has an optimal
solution whose entries belong to one real number field of degree at most two over the
rationals, also with polynomial encoding length. Theorem 2 and this corollary, including the
rational-certificate strengthening, have been independently reviewed; see
`notes/review-rank-one-certificates.md`.

Proof. Compactness gives an optimum. If zero is optimal, it supplies a rational certificate.
Otherwise take an optimal positive total `S*`. As in Theorem 2, first choose an optimal row
vertex for this total and then a column vertex minimizing the objective with that row fixed.
Both margins therefore have all but at most one coordinate at bounds. Fix their two patterns.
The totals for which both patterns are feasible form a closed rational interval `J`; each
margin is affine in `S` there. For `S > 0`, the objective on this family is
`αS + β + γ/S`. Since the family contains a global optimum, minimizing over `J` gives a global
optimum too. The endpoint and stationary-point argument of Theorem 2 produces an optimal total
that is either rational or `sqrt(γ/α)` with positive rational `α,γ`, and hence produces an
optimal matrix in a single quadratic number field. If the chosen interval includes zero,
the continuous zero extension is handled exactly as in Theorem 2.

The two patterns, their interval endpoints, and `α,β,γ` have polynomial bit length. Explicitly,
each margin has the form `r(S)=e_k S+b`, `c(S)=e_h S+d`, where the fixed components of `b,d`
are input bounds and the free components are negatives of sums of bounds. The coefficients
are `α=C_kh`, `β=e_kᵀCd+bᵀCe_h`, and `γ=bᵀCd`. These expressions have fixed degree and use
polynomially many rational sums and products. This proves the polynomial encoding bound for
the quadratic optimum.

For the stronger rational feasibility certificate, take the two patterns supplied by any
positive optimal witness with value at most `t`. On their rational interval `J`, the threshold
inequality is equivalent, for `S>0`, to

```
q(S) := αS² + (β−t)S + γ ≤ 0.
```

The minimum of this rational quadratic over `J` is attained at a rational endpoint or,
when `α>0`, at the rational stationary point `(t−β)/(2α)` if it lies in `J`.
If the minimum is negative, its total is positive: when `0∈J`, the feasible affine margins
satisfy `r(0)=c(0)=0`, so `q(0)=0`. If the minimum is zero, a positive witness also minimizes
`q`; a positive endpoint is rational, and an interior minimizer is the rational stationary
point unless `q` is constant. In the constant case, take any positive rational point of `J`.
Thus there is a positive rational total of polynomial bit length satisfying the threshold,
and its margins and matrix `rcᵀ/S` are rational with polynomial bit length.

A certificate can therefore consist of both patterns and that rational total. The verifier
reconstructs the margins, checks their bounds and equal positive totals, and checks
`rᵀCc ≤ tS` using rational arithmetic. It need not check optimality. Zero is verified separately
against the lower bounds and threshold. Theorem 1 supplies strong NP-hardness. ∎

Quadratic numbers are needed for exact optima in general. For a `2×2` instance with `C=I`,
`r_0=c_0=1`, and `0≤r_1,c_1≤1`, equal totals force `r_1=c_1=S−1`, with `1≤S≤2`.
The objective is `S−2+2/S`, whose unique minimum is `2√2−2` at `S=√2`.
The rational-certificate assertion concerns rational thresholds and does not assert that
an exact optimizer is always rational.

This establishes a complexity boundary for the isolated rank-one block with arbitrary
source-to-terminal costs: bounding either matrix dimension gives tractability, while allowing
both to grow gives strong NP-hardness. Standard single-pool tractability with a bounded number
of inputs was already established by [Boland, Kalinowski and Rigterink](https://arxiv.org/abs/1508.03181)
and [Haugland and Hendrix](https://doi.org/10.1007/s10957-016-0890-5) for their pooling models.
Theorem 2 should therefore be presented as an algorithm for the present general-cost block,
not as the first bounded-input pooling tractability result.

## Computational check

`code/rank_one_hardness/verify_reduction.py` builds random maximum-edge-biclique instances
(brute-forced) and random PARTITION instances, constructs the (P) instances of Theorem 1 and
Remark 2, and solves the sign-equivalent bilinear program `min rᵀCc` over `r ∈ [l,u]`, `c ∈ [l',u']`,
`eᵀr = eᵀc` (the numerator of (P'); the sign of its optimum equals the sign of the optimum of (P)
because `S ≥ 1` in these instances) with Gurobi's global nonconvex solver, checking that
`min ≤ 0` holds exactly when the combinatorial answer is "yes". For biclique "no" instances the
bilinear optimum is provably `≥ 1`; for PARTITION "no" instances it is positive but no explicit
lower bound is proved (observed values `≥ 0.25`), so the numerical threshold `10⁻³` is a heuristic
there. Output in
`code/rank_one_hardness/verify_output.txt`.

## Relevance for PSE

The single-pool rank-one block is a standard target for pooling convexification. Theorem 1
rules out a uniform polynomial-time method for exact linear optimization over that block
with arbitrary costs, and Corollary 1 rules out uniformly constructible polynomial-size hull
formulations equipped with the stated polynomial-time optimization guarantees. It does not
rule out exact exponential-size SOC formulations, useful compact joint relaxations, or
cutting-plane methods that may require superpolynomial work. Complexity alone does not justify
omitting valid bounds or choosing one particular relaxation in a practical algorithm.

The cost assumption matters. If the path cost is additive, `C_ij = a_i + b_j`, then
`⟨C,W⟩ = aᵀr + bᵀc`, and this quality-free block reduces to a linear program in the margins.
The reduction uses nonadditive source-to-terminal costs. Its direct PSE relevance is the
complexity of general linear optimization or separation in a relaxation subproblem, where
such objective coefficients can arise, rather than hardness of every standard quality-free
single-pool operating-cost model. The fixed-dimension algorithm can be useful for isolated
blocks of small pool degree; extra quality constraints or coupling between pools require
separate analysis.

## Literature assessment

The [Dey–Kocuk–Santana author manuscript](https://www2.isye.gatech.edu/~sdey30/RankonePool.pdf)
explicitly states the linear-optimization hardness conjecture immediately after Theorem 4.
The [Jalilian–Kocuk published article](https://doi.org/10.1007/s11081-025-09997-6) proves an
SOC hull representation whose size is exponential and develops practical joint relaxations.
The reduction uses the NP-completeness result in [Peeters (2003)](https://doi.org/10.1016/S0166-218X(03)00333-0).
Targeted open-web searches on 2026-09-04 found no earlier resolution of the exact conjecture.
The reduction technique itself is elementary and related to established bilinear encodings of
biclique problems; novelty is claimed provisionally for its application to this precise
row-and-column-bound set. See `notes/audit-rank-one.md` for search terms and proof audit details.
