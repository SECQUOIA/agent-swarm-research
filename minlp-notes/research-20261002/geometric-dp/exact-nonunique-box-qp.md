# Exact mixed-integer box QP with finitely many optimal coordinate values

Date: 2026-10-02. Status: arithmetic transfer supported by
[fresh independent review](../reviews/exact-nonunique-box-qp-adversary.md)
and targeted exact checks. The underlying
[coordinate-anchor theorem](../new-direction/projection-anchors.md)
has its own proof-review and literature record.
The rational-height and reconstruction facts are those of
[exact box QP](exact-box-qp.md); they are standard ingredients, not a
separate novelty claim.

The uniqueness assumption can be removed from the exact rational box-QP
corollary. Let `S` be the finite set of global optimizers and define

```
A = sum_i |pi_i(S)|,
```

the total number of distinct optimal coordinate values. At fixed bag
size, an exact optimizer and value can be found in bit complexity
polynomial in the input length, `A`, and the curvature/growth ratio.
Neither the optimal set, its coordinate values, their separation, nor the
growth constant need be supplied. The count can be polynomial even when
the number of complete optimal vectors is exponential.

The algorithm terminates whenever the optimal set of the rational mixed
box QP is finite. The quantitative assumptions on `A` and conditioning
control its polynomial-time guarantee. This does not cover an arbitrary
positive-dimensional optimal set with the same bound.

## 1. Setting and exact arithmetic facts

Use the rational mixed-integer box-QP input and supplied decomposition of
[exact-box-qp.md](exact-box-qp.md). All continuous and integer coordinates
are included in the gridded vector `x`; there are no additional fully
enumerated variables outside its metric in this corollary. Let `I` be
the binary input length, `N` the number of bags, `M` the number of
quadratic factors, `p` the maximum bag size, and `n>=1` the number of
nonfixed coordinates. Integer endpoints are rounded inward first.

Assume `S=argmin_X F` is finite and nonempty, and write

```
F(x)-f* >= g dist(x,S)^2,       x in X,       g>0.           (1)
```

Take `L=max_i 2Q_ii` when this is positive and set
`kappa=max(1,L/g)`. If every diagonal curvature is nonpositive, endpoint
DP already solves the problem exactly, as in the preceding corollary.

Choose a common integer `D` clearing the rational quadratic data, all
supplied factor coefficients, and all box endpoints. Write
`F=(x^T Hx+h^T x+k)/D` with integral symmetric `H`, and set

```
C = max(1,max_(i,j)|H_ij|),
Delta = (2nC)^n,    R=D Delta,    V=D R^2.                  (2)
```

Enlarging `D` to clear the factor representation does not affect the
height proof. Its bit length remains polynomial in `I`.

Every point of finite `S` is isolated. Its free continuous Hessian is
therefore positive definite: a singular free direction would produce a
short segment of optima in its fixed integer slice. The Cramer argument
in Lemma 1 of the preceding note applies to *every* point of `S`, not
merely to one selected optimizer. Each optimizer has a common coordinate
denominator at most `R`, and `f*` has reduced denominator at most `V`.

The same note proves the value-denominator bound even when the optimal
set is not finite. Consequently, bounded-denominator value isolation and
exact feasibility/objective checks certify an accepted answer without
trusting either (1) or finiteness of `S`.

**Qualitative growth lemma.** Finiteness of `S` implies the existence of
some `g>0` in (1) for a quadratic on a compact mixed box.

*Proof.* If not, choose points outside `S` with
`[F(x_j)-f*]/dist(x_j,S)^2 -> 0`. Compactness makes the objective gaps
tend to zero. Choose a nearest optimizer for each point. Because `S`
is finite, pass to a subsequence with the same nearest optimizer `s*`;
then `x_j->s*`. Integer coordinates eventually equal those of `s*`.
If all coordinates are integer this is already a contradiction.

Otherwise write `x_j-s*=t_j u_j`, where `t_j->0`, `||u_j||=1`, and
pass to `u_j->u`. In the fixed integer slice, first-order optimality gives
`ell dot u_j>=0`, where `ell=grad F(s*)`. The exact expansion is

```
[F(x_j)-f*]/t_j^2 = (ell dot u_j)/t_j + u_j^T Q u_j.
```

It implies `ell dot u=0` and `u^T Q u<=0`. The limit has zero integer
components and feasible signs at active continuous bounds, so a short
ray `s*+tau u` is feasible. Optimality forces `u^T Q u=0`. The ray is
then a nontrivial segment of global optimizers, contradicting finite `S`.
QED.

This lemma is qualitative. Near-tied distant solutions can still make the
largest valid `g` very small.

## 2. A sufficient trial

For a dyadic trial ratio `theta=2^(-m-1)`, set

```
eps_theta = min(1/(4V^2), L theta^2/(16R^4)),
rho = 1/(4R^2).
```

Choose `h=s 2^-J`, where `J` is the least nonnegative integer with

```
4 L n h^2 <= eps_theta.                                   (3)
```

This is a rational choice satisfying the coordinate-anchor theorem's
core-width requirement. Powers of two and rational comparisons compute it.

Initialize each coordinate anchor set by `C_i={a_i}` and run the
coordinate-anchor-union algorithm with this fixed `h` and `theta`.
It retains every anchor and repeatedly minimizes the corrected objective
over the shared union grids. If it reaches `D(y)<=eps_theta`, its exact
lower bound obeys

```
LB <= f* <= F(y),    F(y)-LB = D(y) <= eps_theta.           (4)
```

Reconstruct the unique denominator-at-most-`V` rational `v` in
`[LB,F(y)]`. For every coordinate, reconstruct a denominator-at-most-`R`
rational in `[y_i-rho,y_i+rho]`, if one exists. Accept only if every
coordinate is obtained, the vector satisfies the intervals and prescribed
integrality, and its exact objective equals `v`. If this reconstruction
fails, abandon the trial. Interval separation and rational reconstruction
are exactly as in the preceding note.

**Lemma 2.** A trial with `theta^2<=g/(4L)` succeeds after finitely many
anchor solves.

*Proof.* This is the admissibility threshold of the coordinate-anchor
theorem. Its finite-projection progress bound guarantees a point satisfying
(4). Choose a nearest optimizer `s*` to that point. Then

```
||y-s*||^2 <= eps_theta/g
           <= 1/(64R^4)
            < rho^2.
```

Every coordinate interval contains the corresponding coordinate of the
same optimizer `s*`; the uniform height bound makes reconstruction exact.
All coordinates, including integers, are in the metric, so there is no
uncontrolled discrete assignment to preserve. In fact integer coordinates
already equal those of `s*` because the distance is less than one.
The value interval isolates `f*`, and final verification succeeds. QED.

If a different model includes finite-state variables outside the metric,
retaining their approximate-solve assignment is not automatically valid.
One must reoptimize those states after reconstructing the exposed optimum,
or supply another recovery argument. No such extra variables are hidden
in the present statement.

## 3. The operation count

The coordinate-anchor theorem gives the failed-solve bound

```
T <= sum_i |pi_i(S)| ceil_+(log_(sqrt(2))(s_i/tau)),
tau = sqrt(eps_theta)/(sqrt(2Ln) theta),
```

where `ceil_+(u)=max(0,ceil(u))`. One anchor contributes at most

```
q0 = O(1 + theta^-1 log(1+theta s/h))
```

grid nodes per coordinate. Each coordinate has at most `T+1` anchors.
The total exact table-operation bound is

```
O((N+M) q0^p (T+1)^(p+1)),                                (5)
```

with the ordinary bag-index factors. It includes all failed solves and
the final successful one. Grid generation, sorting, and union formation
add only polynomial factors in these quantities.

For a dyadic `theta` within a fixed factor of the admissible threshold,
`theta^-1=O(sqrt(kappa))`. The bit lengths of (2), the rational input,
and the target accuracy imply

```
J = poly(I) + O(log kappa),
T = A [poly(I) + O(log kappa)],
q0 = O(sqrt(kappa)[poly(I)+O(log kappa)]).
```

Thus (5) is polynomial in `I,A,kappa` at fixed `p`. There is no
enumeration of the complete optimum set or of its Cartesian product.
The parameter `A` appears only in the analysis.

## 4. Rational denominators do not grow with the number of anchors

The earlier single-center bit theorem cannot simply be cited for a changed
algorithm. Here the required extension is elementary and particularly
useful: fixed-offset source grids have a common denominator independent
of the number of accumulated anchors.

Write `theta=2^-r`, `r=m+1`. A source grid on one side of an anchor `c`
has untruncated distances

```
t_k = h sum_(ell=0)^(k-1) (1+theta)^ell.
```

The coordinate-grid count bounds the number of steps by
`K=O(2^r(J+1))`, uniformly over every anchor in the box. Because `s` has
denominator dividing `D`, each `t_k` has denominator dividing

```
D 2^(J+rK).
```

Start with the lower endpoint as the single anchor of each coordinate,
and put `E=J+rK`. Every later anchor is either
an original clipped endpoint or a previous anchor plus or minus one of
these same offsets. Consequently all anchors and all continuous grid
coordinates always have denominator dividing `D 2^E`. Adding anchors
does not multiply independent denominators or increase `E`. Integer grid
coordinates are integers and satisfy the same bound automatically.

Every reduced rational factor value and unary correction has a denominator
dividing

```
W = 8 D^3 2^(2E).                                        (6)
```

Each DP message is a sum of selected factor and correction values, so its
denominator also divides (6), regardless of the number of anchors or tree
depth. Objective magnitudes and correction magnitudes on the input box
have polynomial-bit bounds. Therefore table entries, arithmetic
intermediates under reduced rational arithmetic, and grid comparisons
have bit lengths polynomial in `I` and `E`.

At an admissible trial, `E=poly(I,kappa)`. Combining this fact with (5)
gives a polynomial bit bound in `I,A,kappa` at fixed width. Computing
integer steps, sorting union grids, continued-fraction reconstruction, and
the final rational feasibility/objective check have polynomial bit costs
as well. No exact-real oracle remains in this corollary.

## 5. Unknown growth and unknown projection counts

Neither `g` nor `A` is needed by the implemented algorithm. For rounds
`q=1,2,...`, run trials `m=0,...,q` from the same lower-endpoint anchors,
with each trial limited to `2^q` elementary counted bit operations.
Count grid construction, rational arithmetic, DP, reconstruction, and
verification; interrupt an unfinished trial when its budget is exhausted.
Every accepted answer remains valid regardless of the trial parameter.

Some index `m*` is admissible and satisfies `m*=O(1+log kappa)`.
Its entire sufficient trial has a bit-work bound polynomial in
`I,A,kappa`. A round large enough to include `m*` and supply this work
budget therefore succeeds. Summing the budgets over preceding rounds
preserves a polynomial bound; the standard bounded-run simulation can
charge its bookkeeping as well. This establishes the following result.

**Theorem.** A rational mixed-integer box quadratic program with finite
optimal set has an exact terminating algorithm. At fixed bag size `p`,
its bit complexity is polynomial in `I,A,kappa`. In particular it is
polynomial in the binary input length when both `A` and `kappa` are
polynomially bounded. The algorithm requires none of `S,A,g` as input.
Its exact certificate is verified by rational DP lower bounds,
bounded-denominator value isolation, and a feasible rational vector with
that exact objective; certificate validity does not rely on the complexity
promises.

## 6. Significance and verification limits

This extends exact recovery beyond a unique optimum while paying for
distinct optimal coordinate values, which can be much fewer than complete
optimal vectors. For instance, sums of concave quadratic wells on
`[0,1]` have optimal coordinates in `{0,1}` and exponentially many complete
optima. Adding an independent strictly convex quadratic supplies positive
upper coordinate curvature and can retain this distinction. Such separable
examples illustrate the parameter; they are already easy directly.

The new arithmetic step is the anchor-independent denominator bound, plus
the observation that every isolated quadratic optimizer has bounded
rational height. Both are direct arguments. The substantive discovery
algorithm and its projection-count dependence are those of the
coordinate-anchor theorem, whose independent review is separate. No claim
of practical superiority, unrestricted MINLP tractability, or publication
priority follows from this corollary.

The [fresh arithmetic review](../reviews/exact-nonunique-box-qp-adversary.md)
found no substantive gap, conditional on the separately reviewed
coordinate-anchor progress theorem. Its inline exact checks covered
252 anchor rounds, 3,183 denominator checks, and recovery neighborhoods
around two distinct optimizers. Its requested clarification to initialize
exactly one anchor per coordinate has been applied.

The separate reproducible check command actually run was

```
python3 research-20261002/geometric-dp/checks/exact_nonunique_qp_checks.py > research-20261002/geometric-dp/checks/exact-nonunique-qp-results.json
```

The [script](checks/exact_nonunique_qp_checks.py) and
[results](checks/exact-nonunique-qp-results.json) record recovery of all
eight optima in both a continuous and a mixed variant, with 16 value and
64 coordinate reconstructions. Three arithmetic fixtures exercised
384 anchor rounds, 896 source grids, 12,715 grid-coordinate divisibility
checks, and fixed-denominator checks for factors, source and union
corrections, and message-like sums. Every continuous coordinate accumulated
at least 127 distinct anchors while respecting the same denominator bound.
All assertions passed.

These checks address the new reconstruction and denominator arguments;
they do not implement the complete anchor DP or measure its performance.
No project-wide verification or CI inspection was used.
