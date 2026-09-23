# Second review: unconditional error budgets and rational allocation

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Verdict: **PASS**, under the stated positive-coefficient, unconditional-body,
dense-degree, and rational separation-oracle assumptions.

Reviewed independently:

- `notes/positive-separable-unconditional-error-precision.md`.
- `notes/rational-log-product-convex-body-oracle.md`.

This review checks mathematical correctness and the claimed polynomial
rational construction. It does not establish publication priority. The
underlying weak optimization theorem is classical and correctly credited.

## The whole-body lower bound is valid

Convexity and invariance under every coordinate sign change imply that
the full coordinate box with opposite corners `-|u|` and `|u|` is contained
in `K` whenever `u in K`. Hence coordinatewise absolute domination is valid.

The midpoint of two exact graph points whose integer lifts have the same
parity is admitted by convexity. Its error is the Jensen vector `J`, so
`J in K`. The nonlinear coefficients make `J` coordinatewise nonnegative;
affine terms cancel. Taking compact closures of the parity supports
preserves both statements by continuity and closedness of `K`.

The previously reviewed scalar estimate gives

```
J_j(x,y) >= sum_i (C_ji/D_i^2)
                    (x_i^(D_i/2)-y_i^(D_i/2))^2.
```

The coordinate power map is a homeomorphism of the active cube, including
when some `D_i` are odd. Thus the transformed compact supports still cover
the unit cube. For independent points chosen uniformly in a transformed
support of positive volume, the original Jensen vector is evaluated at
their inverse images. This is a bounded measurable vector in the closed
convex set `K`, and therefore its expectation belongs to `K`. Coordinatewise
domination then yields

```
C p in K,       p_i=2 Sigma_ii/D_i^2.
```

The variance cap `Sigma_ii<=1/4` gives `p_i<=1`. Hadamard's inequality and
the volume-covariance inequality apply to this transformed uniform measure.
The resulting support volume is at most

```
omega_r (r+2)^(r/2) product_i(D_i/sqrt(2)) sqrt(D_K).
```

The parity cover proves the stated lower bound. This reasoning does not
assume that the power map preserves Lebesgue measure or convexity. Inactive
coordinates can be removed by the same affine output subtraction and
projection used in the base theorem; these operations preserve the error
vector and do not add integer variables.

## The Taylor rectangle gives an admissible rational formulation

For a positive feasible allocation, choose original-coordinate dyadic
widths `h_i<=sqrt(p_i)/D_i`. The second derivative estimate gives the
componentwise remainder bound `0<=f-T<=Cp/2`. The interval constraints
`T<=w<=T+Cp/2` both contain the exact graph and imply
`|w-f|<=Cp/2`. Since `Cp in K`, domination places every admitted error in
`K`.

The reviewed shared prefix-power recurrences remain exact for all integer
degrees. They use `O(D_i L_i)` bounded continuous variables and rows, with
the original `L_i` prefix bits and no additional integers. In particular,
the construction does not need a finite exact linear description of `K`.
All depths can be chosen by exact rational comparisons, and dense degree
encoding makes the recurrence count polynomial in the input size.

## The allocation hypograph has the required explicit geometry

The oracle lemma is valid even for signed `C` and a non-symmetric, possibly
unbounded `K`, provided the stated centered inner ball and strong rational
separation oracle are supplied. The allocation feasible set is compact
because it is a closed subset of `[0,1]^r`.

Write `c=1+sum |C_ji|` and choose `delta=2^(-b)` with
`delta r c<=rho_0/4`. Then `delta 1` is feasible and the positive optimum
satisfies `D>=delta^r`. Since every allocation coordinate is at most one,
each coordinate of any product maximizer is at least `delta^r`.

The note's hypograph with `a=delta^r/4` consequently excludes no maximizer.
Its proposed center and radius satisfy all constraints:

- `p_0=delta 1/2` has coordinate margins at least `delta/4`, and
  `sigma<=delta/(16r)`.
- `||Cp_0||<=rho_0/8`, while a radius-`sigma` perturbation changes `Cp`
  by at most `c sigma<=rho_0/8`.
- The center has at least two units of log-hypograph slack. On the ball,
  coordinates are at least `delta/4`, so the log-product variation is at
  most `(4r/delta)sigma<=1/4`. The last-coordinate perturbation is also
  at most `1/4`.
- The lower last-coordinate margin is
  `t_0+B=rb(r-1)+r+2>=3`.

Thus the stated closed inner ball is valid. The proposed outer radius is
conservative and valid because the coordinate box has diameter at most
`sqrt(r)` and the last coordinate lies in `[-B,0]`. All radii, centers,
and their binary encodings have polynomial size. Exponentially small
inner radii cause no violation of the claimed binary complexity.

## Rational weak separation and classical optimization match

After the exact linear and `Cp in K` checks, compute a rational interval
for `ell=sum log p_i` with radius `eta/2`. If the query is above its upper
endpoint, the displayed rational tangent is a valid strict separating
inequality by concavity. Otherwise lowering the last coordinate to
`min(t,ell)` produces a point of the hypograph within distance `eta`.
The lower last-coordinate bound is preserved because
`ell>=-r(rb+2)ln(2)>-B`.

I checked the scanned primary source, rather than relying on its ambiguous
OCR: Grötschel, Lovász and Schrijver, *The ellipsoid method and its
consequences in combinatorial optimization*, [printed page 172, definitions
(5) and (6), and page 177, Theorem (3.1)](https://ir.cwi.nl/pub/10046/10046D.pdf).
Its weak-separation convention requires a normal with Euclidean norm at
least one. Dividing a nonzero rational strong normal by its infinity norm
therefore meets that convention; the tangent normal already meets it
through its last-coordinate coefficient. The source's weak optimization
guarantee is simultaneous distance at most the requested accuracy and
additive objective loss at most that accuracy. The note uses exactly this
guarantee, with explicitly known inner and outer balls in dimension
`r+1>=2`.

Polynomial rational log evaluation is also sufficient here. One can range
reduce a positive rational to `[1,2]` by powers of two and use the series
for `log u=2 atanh((u-1)/(u+1))`; its argument has absolute value at most
`1/3`. A polynomial number of terms in the requested binary precision,
with directed rational error bounds, gives the required intervals. The
range exponent and rational tangent entries have polynomial bit length
because `p_i>=a`.

## Exact feasibility repair and count constants pass

For a weak optimizer `y`, choose a nearest point `z` in the compact
hypograph. The note's repaired rational point is the convex combination
of `z` and a point in the explicit inner ball, because

```
y_f = sigma z/(sigma+rho)
      +rho [center+(sigma/rho)(y-z)]/(sigma+rho).
```

This proves exact feasibility without computing `z`. With
`rho=nu sigma/[4(B+sigma+1)]`, its objective loss is bounded by
`rho+(rho/sigma)B<nu`; hence its allocation product is at least
`exp(-nu)D`. Every implemented operation in this final repair is rational.

For `nu=1`, allocation approximation costs at most `1/(2 ln 2)` in the
binary count. Combining the base volume constant
`A<sum log2 D_i+3r` with the grid bound proves
`p_out<=p_conv+2 sum log2 D_i+4r+1`.

For the quadratic corollary, the Hessian convention is important and is
used correctly: with `f_j=(1/2)sum h_ji x_i^2+affine` and `C_ji=h_ji`,
the expected Jensen vector is exactly `(1/4)C diag(Sigma)`. Thus
`p_i=Sigma_ii/4` is feasible. The square model has error dominated by
`Cp/8`, so the previous trace-allocation proof yields the sharper stated
`p_out<=p_conv+5r+1` guarantee under the same body assumptions.

I reran `code/quadratic_rank/check_unconditional_allocation_repair.py`:
all 24 rational repair cases passed. This is supporting arithmetic
evidence; it is not an implementation or empirical test of the imported
GLS optimization algorithm. No unresolved proof or encoding defect was
found in the two reviewed notes.
