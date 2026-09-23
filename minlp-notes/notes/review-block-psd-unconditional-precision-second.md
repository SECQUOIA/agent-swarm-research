# Second review: block PSD precision with unconditional errors

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Verdict: **PASS** for both main notes and the thin-domain scope example.

Reviewed independently:

- `notes/block-psd-unconditional-error-precision.md`.
- `notes/rational-block-logdet-convex-body-oracle.md`.
- `notes/block-psd-domain-correlation-obstruction.md`.

This audit establishes no publication priority. Convex log-determinant
optimization, rational PSD separation, and weak optimization are correctly
treated as established ingredients.

## Matrix coordinates, compactness, and explicit radii

For the independent upper-triangular coordinate map, the squared matrix
Frobenius norm counts off-diagonal entries twice. Thus
`||Delta P||_F<=sqrt(2)||Delta u||_2`. The trace map's coordinate matrix
must likewise double its off-diagonal coefficients; the note explicitly
does so.

With `c=1+sum |C_ji|`, the operator norm of `C` is at most `c`. The
independent-coordinate vector for `delta I` has norm `delta sqrt(N)`.
Therefore `delta N c<=rho_0/4` ensures its image is in the known inner
ball of `K`. The determinant optimum exists on the closed, bounded
matrix-cap set. It is positive, at least `delta^N`. Since every capped
eigenvalue is at most one, every eigenvalue of every determinant optimizer
is at least `delta^N`. The lower cap `a=delta^N/4` excludes no maximizer.

The hypograph is compact and convex in its stated Euclidean coordinates.
Its proposed radius-`sigma` ball passes each check:

- Matrix perturbations have operator norm at most `2sigma`, and
  `sigma<=delta/(32N)`. Around `P_0=delta I/2`, the least eigenvalue
  remains above `delta/4>=a`, and the greatest remains below one.
- `||Cu_0||<=c delta sqrt(N)/2<=rho_0/8`. Image perturbations have
  norm at most `c sigma<=rho_0/8`.
- The log-determinant coordinate gradient consists of inverse diagonal
  entries and doubled inverse off-diagonal entries. Its norm is at most
  `sqrt(2)||P^(-1)||_F<=4sqrt(2N)/delta<=8N/delta` throughout the ball.
  Its variation is therefore at most `1/4`.
- At the center, the log determinant is
  `-N(b+1)ln 2>=-N(b+1)=t_0+2`; the last-coordinate perturbation is
  at most `1/4`.
- The lower last-coordinate margin is
  `t_0+B_0=Nb(N-1)+N+2>=3`.

The outer radius is also valid: each independent matrix entry has absolute
value at most one under the spectral caps, so its coordinate distance from
the center is bounded by `sqrt(q)`, and its last-coordinate distance is at
most `B_0`. The claimed radius `2(B_0+q+1)` is conservative. All numbers
have polynomial rational encoding; their possible exponentially small
magnitudes are compatible with binary polynomial complexity.

## The rational weak separation interface is sufficient

For a rational query, spectral-cap separation uses a rational negative
quadratic-form witness for either `P_b-aI` or `I-P_b`. The witness yields
a linear inequality in the independent coordinates, with the off-diagonal
factor two. The rational symmetric elimination argument in the reviewed
correlation-matrix oracle supplies such witnesses with polynomial bit
length: positive pivots admit Schur complements; a negative diagonal is
already a witness; a zero diagonal with a nonzero off-diagonal entry yields
an indefinite two-dimensional restriction. Determinant bounds control the
rational congruence computations. No enumeration of all principal minors
is required by this algorithm.

Once the spectral and image constraints pass, every block is bounded
below by `aI`. Its determinant is an exactly computable positive rational,
and its inverse is an exactly computable rational matrix, both of
polynomial encoding length. Approximating the sum of scalar logarithms
to an interval of radius `eta/2` needs only polynomially many bits. One
may approximate each summand to radius `eta/(2B)` when there are `B`
blocks. Range reduction and the convergent rational series for the scalar
logarithm give such certified intervals.

Concavity of log determinant makes the displayed tangent globally valid
on the positive definite cone. Its last-coordinate coefficient is one;
it strictly separates a query above the computed upper interval endpoint.
For any other query passing the checks, lowering the last coordinate to
the exact log determinant places it in the hypograph within distance
`eta`. This does not cross its lower bound, because

```
sum_b log det P_b>=N log a=-N(Nb+2)ln 2>-B_0.
```

The normalizations meet the norm-at-least-one convention in the original
[GLS paper, definitions (5)--(6) on printed page 172 and Theorem (3.1) on
page 177](https://ir.cwi.nl/pub/10046/10046D.pdf). The source was checked
in the previous scalar-oracle audit, including its scanned norm inequality,
and its interface was reread for this review. Hypograph dimension is
`q+1>=2`, and both required balls are explicitly known. The source returns
simultaneous Euclidean distance and objective guarantees at the requested
binary accuracy, exactly as needed here.

## Central repair gives exact feasibility in the correct coordinates

Let `y` be the rational weak optimizer and `z` a closest hypograph point,
so `||y-z||_2<=rho`. The proposed repaired point is

```
y_f=sigma z/(sigma+rho)
    +rho [center+(sigma/rho)(y-z)]/(sigma+rho).
```

The bracketed point belongs to the known inner ball in independent-entry
coordinates. Convexity proves exact feasibility of `y_f`; no conversion
between matrix Frobenius and coordinate distance is made at this step.
Its objective loss is at most `rho+(rho/sigma)B_0<nu` for the stated
choice of `rho`. Its matrix coordinates are rational and its determinant
product is at least `exp(-nu)D`.

This proof works for an arbitrary rational linear map and any closed
convex `K` with the stated centered inner ball. It needs neither positivity
of that map nor symmetry, downward closure, or boundedness of `K`.
Compactness comes from the spectral caps. All oracle accuracy depths,
determinants, inverses, separating coefficients, and final repair operations
have polynomial rational complexity.

## The unconditional-body precision comparison passes

For PSD block Hessians, each midpoint Jensen vector is nonnegative and
belongs to `K`. Closedness preserves this on compact parity-support
closures. Averaging over two independent uniform points in a support gives

```
(EJ)_j=(1/4)sum_b tr(H_jb Sigma_bb).
```

The previous block covariance caps and `c_b>=4` give
`0<=E(P)<=EJ`. An unconditional convex body contains the coordinate box
generated by each of its members, so `E(P) in K`. The determinant and
volume estimates are consequently identical to the reviewed block theorem.

The block residual grid gives the simultaneous vector bound
`|w-f(x)|<=E(P)/8`; unconditional domination puts every error in `K`.
The rational allocation oracle loses less than one unit of natural log
determinant. Its explicit lower cap also supplies the polynomial-depth
minimum-eigenvalue bound needed by rational Jacobi. The latter constructs
`P_b/8<=P_tilde_b<=P_b/2`. Positivity of the Hessians implies
`0<=E(P_tilde)<=E(P)`, so this final grid repair remains in `K` without
any additional body oracle or an exact linear representation of `K`.
The determinant loss adds only `O(N)` binaries.

The block common-kernel quotient, affine output subtraction, and blockwise
domain normalization leave `K` unchanged. Congruence preserves PSD. The
original disjoint input blocks produce an actual product of zonotopes,
with the previously reviewed volume loss
`sum_(b:r_b>0) r_b log2[2r_b(r_b+1)]`. Domain restriction and restoration
use the original cube's exact rational linear lift and add no integers.
This proves the stated `O(sum r_b log(r_b+1))` overhead. Output dimension
and radius encodings affect computational size, not this additive count.

## The thin-domain obstruction is correct

The displayed rational coordinate change is invertible, with determinant
`delta/(1+delta)`, giving the claimed parallelogram area. The standard
`L`-bit square model for `x_1` has error at most `4^(-L)/4`. The exact
second-output correction lies in `[0,2delta+delta^2]`, and allowing that
whole interval gives worst-case error at most
`epsilon/4+2delta+delta^2<epsilon` for `delta=epsilon/16` and `L>=1`.
Every exact graph point is represented. The affine domain change thus
gives a valid rational formulation with at most `L` bits on the actual
parallelogram.

On the full product square, midpoint gaps bound the two coordinate
diameters of each compact parity support by `2sqrt(epsilon)` and
`2sqrt(epsilon)/(1+delta)`. Bounding its area by the product of these
diameters gives

```
p_conv>=log2[(1+delta)/(4epsilon)]>2L-2.
```

The gap between the full-product optimum and the actual-domain optimum
is therefore greater than `L-2` and is unbounded at fixed dimension and
block ranks. This example establishes the stated scope obstruction; it
does not assert that the actual-domain optimum is exactly `L`. No
unresolved proof or bit-complexity issue was found in these three notes.

I inspected and reran `code/quadratic_rank/check_block_logdet_repair.py`.
All 24 repair cases passed, including off-diagonal perturbations of the
weak optimizer. Spectral caps, Euclidean output-body feasibility, and
objective margins are checked in exact rational arithmetic; log-determinant
hypographs are checked at 100-digit precision. This supplements the proof
and does not implement or benchmark the classical weak optimizer.
