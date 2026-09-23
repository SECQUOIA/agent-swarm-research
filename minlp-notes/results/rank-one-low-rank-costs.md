# Exact optimization for rank-one flow blocks with low-rank costs

Status: complete proof independently audited on 2026-09-04; the rank-one specialization
also passed exact-arithmetic checks against exhaustive margin-pattern enumeration.
See [the independent review](../notes/review-rank-one-cost-rank.md).
The projected-box method has close established precedents. Novelty is provisional for the
row-and-column bounded rank-one set, its shared variable total, and its fractional objective;
no novelty is claimed for low-rank zonotope optimization itself.

## Model and cost parameter

Let

```
K = { W >= 0 : rank(W)<=1, l<=W1<=u, l'<=Wᵀ1<=u' },
```

where all bounds are finite nonnegative rationals with `l<=u` and `l'<=u'`
coordinatewise (inconsistent input bounds are rejected). We minimize `⟨C,W⟩` for a rational matrix
`C` of size `m×n`. For nonzero `W`, write its margins as `x=W1`, `y=Wᵀ1`, with common total
`S=1ᵀx=1ᵀy>0`. Then `W=xyᵀ/S`. Feasible totals form the rational interval
`I=[max(1ᵀl,1ᵀl'),min(1ᵀu,1ᵀu')]`; an empty interval means infeasibility.

Define the interaction rank of `C` by

```
k = rank(D),       D_ij = C_ij-C_i1-C_1j+C_11.
```

This is exactly the minimum rank of `C-a1ᵀ-1bᵀ` over row and column cost vectors `a,b`.
Indeed, with `H_m=I_m-1_m e_1ᵀ` and `H_n=I_n-e_1 1_nᵀ`,
`D=H_m(C-a1ᵀ-1bᵀ)H_n`. Multiplication cannot increase rank, so `rank(D)` is a lower bound;
choosing `a_i=C_i1` and `b_j=C_1j-C_11` attains it. Thus rational Gaussian elimination gives
in polynomial time a decomposition

```
C = a1ᵀ + 1bᵀ + UVᵀ,       U in Q^(m×k), V in Q^(n×k).
```

The margin objective becomes

```
aᵀx+bᵀy + (Uᵀx)ᵀ(Vᵀy)/S.                       (1)
```

No signs are imposed on costs or factors. Rank zero gives additive path costs and an LP in
the margins. The matrix dimensions may both be arbitrarily large.

## Theorem 1: polynomial time for fixed interaction rank

For every fixed `k`, minimizing `⟨C,W⟩` over `K` is polynomial-time solvable in the rational
input bit model. An optimal matrix can be returned exactly using rational arithmetic and at
most one square root. The dependence on dimensions is `(m+n)^(O(k+1))`; this is an XP
statement in interaction rank, not a fixed-parameter tractability claim.

### A projected-box lemma

A linear image of a box with `h` coordinates in dimension at most `d` is a zonotope: a translate
of a sum of `h` line segments. For fixed `d`, its vertices can be enumerated in polynomial
time, with a corresponding corner of the original box for every enumerated vertex.

For completeness, the number of vertices is at most
`2 sum_(j=0)^(d-1) binomial(h-1,j)` when the effective dimension is positive and the nonzero
generators number `h`; in dimension zero there is one vertex. One way to see the bound is to
associate an exposed vertex with a full-dimensional region of the central hyperplane arrangement
`g_iᵀt=0`, where `g_i` are the generators. In each region the signs select a unique maximizing
endpoint of every generator. The usual induction adding one hyperplane bounds the number of
regions by the displayed sum. Lower-dimensional and repeated generators only reduce the bound.

An elementary enumeration algorithm adds the segments one at a time. Given the current vertex
list, translate it by the new generator, take the union with the original list, deduplicate,
and retain precisely the vertices of its convex hull. Whether a candidate belongs to the convex
hull of the other candidates is an LP with rational data. Attach to each candidate the original
box corner obtained by its endpoint choices. Intermediate vertex lists obey the same polynomial
bound; every stored point is a sum of rational input generators. This proves polynomial running
time and polynomial bit length for fixed `d`, without assuming general position.

A second elementary fact is that every vertex of a polytope sliced by one hyperplane is either
an original vertex or a point on an original edge. To prove it, let `F` be the smallest face
containing the slice vertex `v`. Then `v` is in the relative interior of `F`. If `dim(F)>=2`,
intersection with one hyperplane through `v` leaves a nonzero feasible direction in both signs,
contradicting extremality in the slice. Thus `dim(F)<=1`.

### Proof of the theorem

Form the two projected boxes

```
Z_x = { (1ᵀx,Uᵀx,aᵀx) : l<=x<=u },
Z_y = { (1ᵀy,Vᵀy,bᵀy) : l'<=y<=u' }.
```

Each has effective dimension at most `k+2`, with at most `m` and `n` generators respectively.
Their vertex counts are `O_k((m+1)^(k+1))` and `O_k((n+1)^(k+1))`. Enumerate their vertices
and corner witnesses by the lemma.

Fix a positive total `S`. On the slices of `Z_x` and `Z_y` at first coordinate `S`, expression
(1) is affine in either projected margin when the other is fixed. Therefore an optimum exists
at vertices of both slices: first minimize over one slice and choose a vertex, then minimize
over the other slice and choose a vertex. Neither step increases the objective.

Enumerate all pairs of vertices in each projected box. This includes the endpoints of every
edge; the additional segments stay inside the projected box and are harmless. A segment whose
endpoint totals differ defines a unique projected margin affine in `S` on the closed interval
between those totals. Its box witness is the same affine interpolation of the two corner
witnesses. Also include each vertex alone as a candidate at its fixed total. Segments with
equal endpoint totals can be omitted: vertices of a slice that lie on such a segment are
already covered by original vertices, by the minimal-face argument above.

Pair each row candidate with each column candidate and intersect their total intervals with
`I`. Discard empty intersections. A pair of singleton or mixed singleton/segment candidates
is evaluated at its common positive total, if any. On every nonsingleton positive interval,
projected margins and their box witnesses are affine in `S`; consequently (1) has the form

```
f(S)=alpha*S+beta+gamma/S
```

with rational coefficients of polynomial bit length. Its minimum is attained at a positive
endpoint, or at `S=sqrt(gamma/alpha)` when `alpha>0`, `gamma>0`, and the point is in the interval.
Constant functions need any feasible total; all other coefficient sign cases are monotone or
have only an interior maximum. If an interval includes zero, include `W=0` separately when
feasible. This is the correct continuous extension because `|⟨C,W⟩|<=||C||_max*S`.

Every candidate is feasible, and every fixed-total slice-vertex optimum appears in the list.
Therefore minimizing all candidates produces a global optimum. There are polynomially many
vertex pairs and paired intervals for fixed `k`. Rational endpoints have polynomial bit
length; interior values are `beta+2sqrt(alpha*gamma)`. Exact comparisons use sign-aware
squaring of rational expressions. Interpolating the stored corners at the selected total and
forming `W=xyᵀ/S` stays in the same quadratic field, with polynomial-size encodings. Thus both
the exact optimization and reconstruction run in polynomial time for fixed `k`. If `I={0}`,
zero is the sole feasible matrix; this is handled before enumeration. This proves the theorem. □

The proof can instead use a rank factorization `C=UVᵀ` without additive coordinates. For fixed
ordinary rank `rho`, the projected dimension is at most `rho+1`, and the same method applies.
Interaction rank is the more useful parameter when an arbitrary additive path-cost component
is present.

## Theorem 2: a near-linear arithmetic algorithm for rank-one costs

If the cost matrix is supplied as `C=pqᵀ`, its optimum over `K` and optimal margins
representing `W=xyᵀ/S` can be computed using `O((m+n)log(m+n))` arithmetic operations and comparisons, with polynomial bit
complexity. For a dense matrix known to have rank at most one, factorization and verification
add `O(mn)` arithmetic operations. Explicitly materializing all entries of `W` likewise
takes `O(mn)` additional work. The zero cost matrix is immediate.

Proof. At fixed total `S`, define four continuous-knapsack values

```
A_-(S)=min { pᵀx : l<=x<=u, 1ᵀx=S },
A_+(S)=max { pᵀx : l<=x<=u, 1ᵀx=S },
B_-(S)=min { qᵀy : l'<=y<=u', 1ᵀy=S },
B_+(S)=max { qᵀy : l'<=y<=u', 1ᵀy=S }.
```

The scalar images of the two margin polytopes are the intervals `[A_-,A_+]` and `[B_-,B_+]`.
Their product is minimized at one of the four endpoint pairs, regardless of signs. Hence the
fixed-total optimum is

```
min_(sigma,tau in {-,+}) A_sigma(S)*B_tau(S)/S.            (2)
```

Each extremum is a continuous-knapsack value: start at the lower bounds and fill available
capacities in increasing coefficient order for the minimum, decreasing order for the maximum.
Sorting takes `O(m log m+n log n)` comparisons. Each of the four value functions is continuous
piecewise affine, with at most its margin dimension many filling breakpoints. Prefix sums of
capacities and weighted capacities give all piece coefficients in linear additional work.

Merge their rational breakpoints with the endpoints of `I`. There are `O(m+n)` resulting
intervals. On each, every one of the four functions in (2) is quadratic divided by `S`.
Check its endpoints and positive minimum stationary point as in Theorem 1. A sweep through
the sorted breakpoints updates the four affine coefficients in constant work per breakpoint.
After choosing the best total and endpoint pair, reconstruct the two greedy margins in
`O(m+n)` work. Handle infeasibility and feasible zero as above. This proves the operation
bound; exact rational/radical arithmetic has polynomial bit cost. □

Irrational optima occur even here. Fix the first row and column sums to one and give the other
row and column bounds `[0,1]`. With `p=(3,1)`, `q=(2,1)`, the common total lies in `[1,2]` and
the objective is `(S+2)(S+1)/S=S+3+2/S`. Its minimum is `3+2sqrt(2)` at `S=sqrt(2)`.

## Corollary: exact Lagrangian block oracles with a fixed number of qualities

Suppose an isolated pool has additive operating costs and `K` input-quality vectors `Q_ik`,
with terminal quality constraints

```
sum_i (Q_ik-H_jk) W_ij <= 0,       j=1,...,n, k=1,...,K.
```

For any supplied rational nonnegative multipliers `lambda_jk`, dualizing these constraints
adds the cost matrix

```
Q Lambdaᵀ - 1 hᵀ,       h_j=sum_k lambda_jk H_jk.
```

Thus the resulting cost has interaction rank at most `K`. By Theorem 1, the exact Lagrangian
subproblem over the remaining rank-one and row/column margin bounds is polynomial-time solvable
for fixed `K`, with no bound on the number of inputs or terminals. Lower quality limits can be
handled by reversing the corresponding signs; repeated quality vectors do not increase their
span dimension. This is a consequence of the cost theorem and the displayed algebra, not a
claim of tractability for the full quality-constrained model. The remaining block constraints
must have precisely the stated margin-and-rank form. Other pool couplings need separate
handling, and no zero-duality-gap claim is made.

## A certified use of approximate low-rank costs

Suppose a supplied matrix `C_tilde` has fixed interaction rank and
`||C-C_tilde||_max<=delta`. For `S_max=min(1ᵀu,1ᵀu')`, every feasible matrix satisfies
`|⟨C-C_tilde,W⟩|<=delta*S_max`. Therefore solving the `C_tilde` problem exactly gives a feasible
matrix whose true cost is at most `2*delta*S_max` above optimum, and the two optimal values
differ by at most `delta*S_max`. These are elementary perturbation guarantees, not new
approximation-hardness or rank-approximation results. The decomposition and its error bound
must be available; finding a low-rank approximation in a chosen norm is a separate problem.

## PSE interpretation and novelty limits

Additive source and terminal costs have interaction rank zero. A fixed number of separable
source-to-terminal cost terms adds fixed interaction rank. Theorem 1 therefore identifies a
tractable family between additive quality-free pool costs and the unrestricted costs used in
the strong hardness construction, while allowing both pool degrees to grow. It applies to the
isolated block; additional quality constraints and coupling between pools require separate
analysis.

[Punnen, Sripratak and Karapetyan (2015)](https://repository.essex.ac.uk/22056/1/1212.3736v3.pdf)
already prove polynomial fixed-rank bipartite box quadratic optimization and a near-linear
rank-one special case. Their model has independent boxes and a bilinear-plus-linear objective;
it does not impose a common variable total with division by that total.
[Hladík, Černý and Rada (2021)](https://kam.mff.cuni.cz/~hladik/publ/b2hd-HlaCer2021c.html)
already use zonotope face enumeration for fixed-rank continuous box quadratic optimization.
The projected-box idea is therefore established. The specific slice-segment construction and
its exact square-root optimization for the present flow block were not found in the targeted
search; independent publishability is not established. See the investigation note for details.

## Exact computational check

`code/verify-rank-one-costs.py` compares the rank-one-cost greedy-envelope algorithm with an
independent exhaustive enumeration of both row and column bound patterns. The reference is
valid for arbitrary cost matrices and does not use the scalar-extrema shortcut. Both paths
use exact rational coefficients; rational-plus-square-root values are compared by sign-aware
squaring, without numerical tolerances. They share the elementary one-variable minimization
routine, so these checks primarily test the different candidate constructions.

On 2026-09-04, 160 seeded instances with signed factors, rational bounds, and dimensions one
through three passed: 111 feasible and 49 infeasible. Explicit regressions cover the irrational
optimum above, zero-only feasibility, and a singleton positive total. This is corroboration of
Theorem 2's algorithm, not an implementation of the general zonotope enumeration theorem.
