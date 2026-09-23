# Additive optimization with a well-conditioned fixed-box follower

Date: 2026-09-05. Status: reviewed predecessor; the final theorem is in
[the promoted result](../results/bilevel-conditioned-box-additive-algorithm.md). This investigates the conditioning boundary of
[scalar-leader box-QP hardness](../results/bilevel-scalar-leader-spd-box-np-completeness.md).

## 1. Model and candidate theorem

Fix leader dimension `r`. Let `X subset [0,1]^r` be a nonempty rational
polytope, given by an explicit inequality list. The follower is

```
z(x)=argmin { (1/2)z^T Qz+(c+D x)^Tz : z in [0,1]^N },
```

with rational symmetric positive-definite `Q`. The upper objective is

```
H(x)=a^Tz(x)+b^Tx.
```

There are no upper constraints involving the follower. All coefficient
magnitudes are unrestricted; their rational bit lengths belong to the
input. Put `A=||a||_1` and

```
mu=1/||Q^(-1)||_infinity,
K=||Q||_infinity ||Q^(-1)||_infinity.
```

Both are positive computable rationals. For symmetric `Q`,

```
mu<=lambda_min(Q),
K<=N*kappa_2(Q).
```

**Candidate theorem.** For rational `0<epsilon<=1`, one can find a rational
leader `xhat in X`, and its exact rational follower response, such that

```
H(xhat)<=min_(x in X)H(x)+epsilon*A
```

in time polynomial in rational input length, `K`, and `1/epsilon`, for
fixed `r`. The exponent depends on `r`. The numerical magnitudes of `c,D,b`
do not enter the enumeration bound. If `a=0`, ordinary LP solves the
leader objective exactly.

In particular, polynomially bounded spectral condition number gives a
fully polynomial normalized additive scheme even with arbitrary
binary-encoded follower cost coefficients and leader linear costs.
Absolute error `epsilon_abs` follows by setting
`epsilon=min(1,epsilon_abs/A)` when `A>0`. Thus its complexity may depend
on `A/epsilon_abs`; polynomial bit length of `A` alone does not bound that
numerical ratio. Polynomial dependence on `1/epsilon` is not polynomial
dependence on the bit precision `log(1/epsilon)`.

## 2. Coordinate saturation limits the relevant cost range

For each follower coordinate define

```
m_i^-=sum_j min(Q_ij,0),
m_i^+=sum_j max(Q_ij,0),
R_i=m_i^+-m_i^-=sum_j |Q_ij|>0.
```

If `c_i+D_i x>=-m_i^-`, its unique optimal coordinate is `z_i=0`.
Indeed, at any `z_i>0` the derivative is at least
`Q_ii z_i+c_i+D_i x+m_i^->0`; decreasing that coordinate would improve
the objective. If `c_i+D_i x<=-m_i^+`, its optimal coordinate is `z_i=1`:
at `z_i<1` the derivative is at most
`Q_ii(z_i-1)+c_i+D_i x+m_i^+<0`. The positive diagonal follows from
positive definiteness. Both conclusions include equality at the thresholds.

Thus a coordinate can vary only in its cost slab

```
-m_i^+ <= c_i+D_i x <= -m_i^- .                        (1)
```

Its width in the scalar cost coordinate is `R_i`, independent of the
magnitude of `c_i,D_i`.

Partition leader space by the at most `2N` affine hyperplanes at the two
thresholds of (1). Enumerate their realizable sign conditions on `X`,
including zero signs, and take the closures of these sign cells in `X`.
These are compact rational polytopes covering `X`; for fixed `r` there
are `N^{O(r)}` cells. Identically constant tests may be processed directly.
For linear systems, replacing the strict signs of a nonempty sign cell
by weak signs gives its closure: mix any point satisfying the weak system
with a point realizing all its strict signs. Feasibility and rational
sample points for such sign conditions are computable by linear
programming; standard fixed-dimensional arrangements give a polynomial
enumeration rather than testing all sign patterns.

Within each closed cell `C`, every coordinate outside a set `J` is frozen
to zero or one. Namely, freeze any coordinate whose sign-cell label places
it at or beyond a saturation threshold. The threshold proofs above remain
valid on the closure. Coordinates in `J` satisfy the two weak slab bounds
throughout `C`, and may include coordinates that reach saturation at its
boundary. Zero rows of `D` inside a slab are allowed in `J`: although their
own direct parameter coefficient is zero, coupling can make them vary.

## 3. Response variation inside one cell

The frozen coordinates have the same values for all leaders in `C`.
The remaining follower problem has positive-definite Hessian `Q_JJ`,
fixed box, and parameter-dependent linear cost `D_J x` plus a constant.
The variational inequalities at two leaders `x,x' in C` imply

```
mu ||z(x)-z(x')||_2^2
 <= -(D_J(x-x'))^T (z_J(x)-z_J(x')).
```

Cauchy--Schwarz therefore gives

```
||z(x)-z(x')||_2 <= ||D_J(x-x')||_2/mu.                (2)
```

The lower eigenvalue bound is valid for every principal submatrix.

Put `E=D_J/mu` and let `q=rank(E)<=r`. If `q=0`, the response is constant
on `C`, so minimizing `b^Tx` over `C` already gives its best upper value.
Otherwise choose `q` independent columns of `E`. Among its `q`-row
subsets, choose one of maximum absolute determinant in these columns.
This takes polynomial time for fixed `r`. Let `B` be the selected full
rows of `E`.

Every row of `E` is a linear combination of these basis rows with each
coefficient having absolute value at most one. This follows from Cramer's
rule and maximality of the chosen minor: replacing one selected row by
any other row cannot increase its determinant magnitude. Agreement on the
selected independent columns implies agreement on all columns, since
those columns span the column space of `E`.

Consequently, if

```
||B(x-x')||_infinity<=delta,
```

then every row of `E(x-x')` has magnitude at most `q*delta`, and (2) gives

```
||z(x)-z(x')||_2<=sqrt(N)*q*delta.                     (3)
```

For a selected basis row coming from coordinate `i in J`, the slab gives
an explicit interval for `B_i x`:

```
(-m_i^+-c_i)/mu <= B_i x <= (-m_i^--c_i)/mu.
```

Its width is `R_i/mu<=K`. These interval endpoints can be large, but have
polynomial rational bit length. Their widths, which determine the grid
size, depend only on the condition quantity `K`.

## 4. Grid only the response-relevant coordinates

Take `delta=epsilon/(N*r)` for `r>=1`. Cover each of the `q` basis-coordinate
intervals by adjacent closed intervals of length at most `delta`. Their
Cartesian product uses at most

```
(2+K*N*r/epsilon)^q
```

rectangles. For each rectangle, intersect its inverse image under `B`
with `C`. If nonempty, minimize the direct leader cost `b^Tx` on that
compact rational polytope by LP and retain one rational optimizer.
There is no need to grid `b^Tx` or bound the numerical magnitude of `b`.
Evaluate the exact follower and upper objective at every retained leader,
and return the best candidate over all cells.

To prove the guarantee, let `xstar` be a global leader minimizer, which
exists because the fixed-box unique response is continuous and `X` is
compact. Choose a cell and basis rectangle containing it. The retained LP
optimizer `xhat` from that rectangle obeys

```
b^T xhat<=b^T xstar.
```

Both leaders belong to the same cell and have basis-coordinate differences
at most `delta`. By (3),

```
a^T[z(xhat)-z(xstar)]
 <= ||a||_2 ||z(xhat)-z(xstar)||_2
 <= A*sqrt(N)*r*delta
 <= epsilon*A.
```

The direct leader term does not increase. The globally best retained
candidate is therefore within the claimed additive error.

The total number of candidates is bounded by

```
N^{O(r)} (2+K*N*r/epsilon)^r.                          (4)
```

A fixed number of additional LP operations per candidate and polynomial-
time exact rational convex-QP optimization preserve the asserted bit
complexity. QP solutions here are rational of polynomial bit length:
for an active box face, the free coordinates solve a nonsingular principal
linear system. Classical polynomial-time convex-QP algorithms, together
with rational recovery, give exact evaluation. This is an established
algorithmic ingredient rather than a new inner QP solver.

Matrix inversion, row-basis determinants, grid endpoints and LP solutions
have polynomial bit lengths in the original input, `log K`, and
`log(1/epsilon)`. With the classical polynomial-bit QP solver, the only numerical
dependence on `K,1/epsilon` is the enumeration bound (4). The elementary
inner solver below adds polynomial dependence on `K` and gives the same
overall theorem. Scalar rescaling of the entire follower
objective leaves `K`, its slab-normalized row ranges, and the theorem
unchanged.

## 5. Basic limitations and comparison target

A naive uniform leader grid would use the global response Lipschitz bound
`||D||/lambda_min(Q)`, which can be exponentially large even when `Q` has
condition number one. For example, the scalar follower minimizing
`2^(-L)z^2/2-xz` on `[0,1]` responds as `clip(2^L x)`. Every coefficient
has magnitude at most one, yet the response slope is `2^L`. This shows
why a condition-number bound and absolute coefficient upper bounds do not
justify the naive grid. It is not a hardness example. Saturation slabs
avoid this dependence by reducing the parameter range where a coordinate
can move.

The algorithm does not impose extra upper constraints involving `z(x)`.
An approximate response cover need not preserve such constraints exactly
without an additional feasibility margin or a separate argument. It also
does not claim exact global optimization in polynomial time, or polynomial
time in accuracy bits rather than inverse tolerance.

Prior work on approximate parametric convex optimization and
regularization paths must be compared carefully: relative follower
duality-gap guarantees and path-following bounds involving parameter
slope constants differ from a response-space cover that supports a global
upper objective. A focused source audit is in progress at
[bilevel-conditioned-box-approximation-novelty.md](bilevel-conditioned-box-approximation-novelty.md).
The proposed contribution is the saturation/rational-basis reduction that
removes numerical `c,D,b` magnitudes from (4), not generic gridding,
variational-inequality sensitivity, maximum-volume bases, or convex QP.

## 6. Established ingredients and an elementary exact inner solver

The maximum-determinant row argument is the classical barycentric-spanner
construction; see [Awerbuch and Kleinberg (2004), Proposition 2.2](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf).
Their determinant replacement proof was checked directly. It is credited
here rather than claimed as new.

Polynomial-time convex quadratic programming is classical:
[Kozlov, Tarasov, and Khachiyan (1979)](https://www.mathnet.ru/eng/dan43059),
with the [fuller 1980 article](https://www.mathnet.ru/eng/zvmmf5189).
The primary bibliographic/abstract statements were checked; this work does
not independently re-audit their full algorithm.

For the present theorem one can instead supply the exact inner evaluation
by the following elementary method, because polynomial dependence on `K`
is already allowed. At a sampled rational leader, write the follower
linear coefficient as `t=c+D x`, and set `L=||Q||_infinity`. Starting at
zero, repeat the rational projected-gradient update

```
z_next=clip_[0,1](z-(Qz+t)/L).
```

Euclidean projection is nonexpansive, and
`0<mu<=lambda_min(Q)<=lambda_max(Q)<=L`. Therefore its contraction factor
is at most `1-mu/L=1-1/K`. Starting distance to the unique optimum is at
most `sqrt(N)`.

To recover that optimum exactly, clear a common denominator from all
entries of `Q,t`, producing an integer matrix and vector of entry magnitude
at most an integer `H>=1`. On any active box face, the free-coordinate
matrix is a nonsingular principal submatrix of this integer matrix.
Cramer's rule and the determinant bound give every optimal coordinate a
reduced rational denominator at most

```
B=N!*H^N.
```

The bound also covers coordinates zero and one. Its logarithm is polynomial
in the sampled input bit length. After

```
ceil(K) * [2 ceil(log_2 B)+ceil(log_2 N)+4]
```

iterations, every coordinate error is less than `1/(4B^2)`. Distinct
rationals with denominators at most `B` are separated by at least `1/B^2`.
Continued fractions therefore recover the unique true coordinate within
that error bound. Verify the reconstructed vector by exact box KKT tests.

Every iterate is rational. Its bit length grows at most linearly in the
number of updates times the input coefficient lengths, so this exact
procedure is polynomial in `K` and the sampled input length. The
reconstruction and verification are polynomial as well. This is an
alternative proof of the inner-oracle requirement, not a new projected-
gradient or rational-reconstruction method.
