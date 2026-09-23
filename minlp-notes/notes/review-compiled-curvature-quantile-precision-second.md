# Independent second review: compiled curvature quantiles

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Candidate: [compiled curvature quantiles](compiled-curvature-quantile-precision.md).
Verdict: **PASS for the final seven-bit theorem and its certified integration
dependency**. The initially conditional audit was completed after independently
checking [the analytical lemma](certified-positive-polynomial-curvature-quantiles.md).
The resulting dense-input polynomial-time construction has no remaining
unproved analytical dependency identified by this review.

The finite curvature theorem and scalar parity comparison were separately
checked in [the curvature audit](review-accuracy-dependent-curvature-precision-second.md).
The circuit construction used here is Section 1 of the promoted
[rational-power result](../results/rational-power-compiled-integer-precision.md).

## Mass certificates and indexed bisection

If some nonlinear coefficient is positive, the density is positive on a
nonempty interior interval and `M>0`. Otherwise the exact affine graph
requires zero integers and is handled separately.

With `zeta=1/512`, an absolute-error certificate for `Mhat` gives
`M<=U=max(zeta,Mhat+zeta)<=M+2zeta`, including the case where the maximum
selects `zeta`. The rational number `B=1+sum k(k-1)c_k/epsilon` bounds
the density, because the density's linear branch is at most `f''/epsilon`
and positive coefficients imply `f''(x)<=f''(1)`.
Both `B` and `U` have polynomial encoding under the assumed evaluator.
Moreover `M<=B`, so the chosen index length `L` is polynomial in the
original dense input size; this fact does not depend on a bound for the
unknown optimum integer count.

At a queried point, the interval `[Fhat-zeta,Fhat+zeta]` contains the true
cumulative mass. Each strict comparison therefore makes a valid bracket
update. An uncertain comparison gives mass error at most `2zeta`.
For a target at most `M`, the bracket always contains a preimage, even
if that preimage is a whole flat interval. After the prescribed number
of strict steps, the mass width is at most `zeta`, since `F` is
`B`-Lipschitz. For a target above `M`, a strict right update is impossible:
`Fhat-zeta<=F<=M<t`. Thus the bracket stays adjacent to 1, giving mass
error at most `zeta+(t-M)<=3zeta` at termination.

The deliberately looser bound `4zeta` is therefore valid for every
interior knot. The forced left endpoint is exact; the forced right endpoint
has discrepancy `|M-U|<=2zeta`, so it also satisfies that bound.
No positive lower bound on the density, monotonicity of the approximate
evaluator, or monotonicity of the computed knots is required.

All query points are dyadic with at most one more fractional bit than the
number of strict steps. Padding early returns gives a common output
precision. A deterministic evaluator with a uniform polynomial running-time
bound yields a polynomial-time indexed routine, with early termination
implemented using a flag. The endpoint index `q=N` can be recognized with
one extra internal carry bit; it does not require a new declared binary.
The `L=0` case directly returns the single interval with endpoints 0 and 1.

## Reversed intervals, chord error, and coverage

For the final choice `N>=(5/2)U`, two consecutive computed endpoints have
mass distance at most

```
U/N+8zeta <= 2/5+1/64 = 133/320.
```

This bounds the density integral on the interval between them regardless
of their order. The finite interval estimate therefore bounds its normalized
endpoint Taylor remainder by `81529/102400<13/16`, and its chord gap by
`13epsilon/16`. A repeated endpoint gives a zero-length segment and zero
chord gap. The piecewise-linear input path from `R_0=0` to `R_N=1` is
continuous, so its image contains every input in `[0,1]`. Its potentially
reversed segments do not introduce inputs outside that interval.

## Endpoint arithmetic and the compiled band

At a dyadic endpoint, downward rounded exponentiation produces monomial
values in `[0,1]` and below their exact values. If a common monomial
error is at most `min(1,epsilon/(8C))`, where `C=sum c_k>0`, the weighted
nonlinear error is at most `epsilon/8`. When the minimum equals 1 this
still follows from `C<=epsilon/8`. A fixed precision at least the endpoint
precision and `ceil(log2(D/eta))` gives the required enclosure by the
reviewed rounded-power induction. Its bit length is polynomial in the
dense input and tolerance encoding.

The circuit outputs only bounded dyadic coordinates and monomial values;
rational coefficients and the affine term are applied by linear equations.
Its AND/NOT gate constraints force all internal continuous wires to Boolean
values once the index bits are integral. Products with the common continuous
interpolation parameter are exact because one factor is a forced Boolean
wire. Thus only the `L` index bits require integrality declarations.

Subtracting the weighted endpoint rounding error from the true chord gives
`-epsilon/8<=y-f(x)<=13epsilon/16`. The band
`y-13epsilon/16<=w<=y+epsilon/8` contains the true graph value and admits
only errors between `-15epsilon/16` and `15epsilon/16`. Restoring the affine
part at the actual interpolated input is exact, including on reversed
segments. Construction size and coefficient encoding are polynomial under
the cumulative-integration assumption.

## Count and computational boundary

The finite parity comparison gives `M<=48*2^p_conv`. Consequently
`(5/2)U<=120*2^p_conv+5/512<128*2^p_conv`, so taking the ceiling logarithm
gives `L<=p_conv+7`, including `L=0` and `p_conv=0`.

Only fixed absolute accuracy is needed in the cumulative evaluations, but
their certified bit cost is an essential dependency. The argument cannot
replace that dependency with numerical quadrature or an unconditioned
evaluation oracle. No claim for sparse binary-encoded degrees or for
multivariate mixtures follows from this audit.

## Checked improvement of the additive constant

The author adopted this review's improvement from eight to seven extra
binaries. It uses

```
L=max(0,ceil(log2((5/2)U))),    N=2^L.
```

Then adjacent mass is at most `2/5+1/64=133/320`, and the normalized
Taylor bound is

```
(133/320)^2+(3/2)(133/320)=81529/102400 <13/16.
```

Keep endpoint error `epsilon/8`, and use
`y-13epsilon/16<=w<=y+epsilon/8`. Its total error is at most
`15epsilon/16`. Finally
`(5/2)U<=120*2^p_conv+5/512<128*2^p_conv`, proving `L<=p_conv+7`.
All other proof and computational conditions remain the same.

The analytical audit below closes the dependency for the improved count.

## Certified cumulative integration: bounds and branch decisions

Let `H=f''/epsilon` and use the analytical note's notation
`U_H=max(1,H(1))`; this is distinct from the mass upper bound `U` above.
Nonnegative coefficients imply `H'>=0`, `H'<=dU_H`, and both relevant
integrands are at most `U_H` on `[0,1]`. A dyadic cutoff with
`2^(-J)<=zeta/(16U_H)` loses at most `zeta/16`, with polynomial `J`.

The branch polynomial `P=(1-x)^2 H-1` has degree at most `d+2` and is
nonzero because `P(1)=-1`. For positive `x`, `H(x)>0`, so comparing its
sign is exactly equivalent to choosing the smaller density branch.
Square-free preprocessing and isolation of all distinct real roots permit
removing at most `d+2` intervals of width
`zeta/[16U_H(d+3)]`. Their total lost mass is below `zeta/16`.
Clipping these intervals to the cutoff or prefix cannot increase the loss.
The remaining sign decisions are exact rational polynomial evaluations.
Multiple roots, tangencies, and roots coinciding with a query endpoint
do not introduce an unresolved sign test.

The integer-polynomial specialization of
[Sagraloff and Mehlhorn, Theorem 36, printed page 41](https://arxiv.org/pdf/1308.4088)
gives polynomial bit complexity in degree, coefficient encoding, and
requested isolating width. This source was checked directly. Clearing
rational denominators and taking the square-free part preserve polynomial
encoding. The argument requires dense degree, as stated.

## Complex analyticity and quadrature error

Dividing each dyadic layer into `16 max(1,d)` pieces gives, on every
retained square-root interval of length `ell` and center `c`,
`ell/c<=1/[16 max(1,d)]`. Intersections with branch intervals preserve
this ratio. On the complex disk `|z-c|<=ell`, write `z=c(1+w)`.
Every monomial of degree at most `d` then has argument bounded by `1/8`
and magnitude at most twice its value at `c`. Positive coefficients keep
`H(z)` inside an open right-half-plane sector. Thus the principal square
root is holomorphic in a neighborhood of this closed disk and has modulus
at most `2U_H`. This includes constant positive `H` and arbitrarily small
positive coefficients; no unproved separation from a complex root is used.

Cauchy's coefficient bound gives uniform Taylor error
`4U_H*4^(-q)` after degree `2q-1` on the half-radius integration interval.
Positive Gauss-Legendre weights sum to the interval length, and the rule
is exact through that degree. Therefore its error is at most
`8U_H ell*4^(-q)`. Summing lengths, rather than the number of panels,
gives total error at most `8U_H*4^(-q)<=zeta/16` for the stated order.
The imported positivity and polynomial exactness are supported by the
directly checked [NIST DLMF Section 3.5(v)](https://dlmf.nist.gov/3.5#v).
The analytic error estimate itself is proved in the note.

## Rational nodes, weights, and arithmetic conditioning

For normalized length-one Gaussian weights, the standard formula
`w=1/[(1-r^2)P_q'(r)^2]` and positivity give
`(qH_q)^(-2)<=w<=1`, where `H_q=(q+1)(2q)!` bounds the coefficient
sum. Hence the denominator is at least one. Derivatives of that denominator
have bounds with `O(q log q)` bits. In particular rational node refinement
to polynomially many bits gives the required relative weight error while
preserving positivity. Endpoint proximity causes no hidden problem:
`1-r^2>=(qH_q)^(-2)` follows from the same formula and derivative bound.
This reuses the conditioning argument independently checked in the
[Stieltjes and compact-power audit](review-compact-pure-power-interpolation-second.md).

Map the isolating intervals into each rational panel and, if needed, clip
them to that panel; the true Gaussian node remains inside. Monotonicity
of `H` encloses its node value by rational endpoint evaluations.
An interval width at most
`zeta^2/[16384 max(1,d)U_H]`, for example, bounds the variation of its
square root by `zeta/128`. Additional rational square-root bisection to
error at most `zeta/128` gives a total absolute value error `zeta/64`.
All these precisions have polynomial bit length even when `H` is tiny.

Set the relative weight error to `delta=zeta/(64U_H)` and the function
error to `e=zeta/64`. Exact node values are at most `U_H`, so on a panel
the error is at most `ell[delta U_H+(1+delta)e]<ell*zeta/16`.
Its sum is at most `zeta/16`. No joint number field for all nodes is
constructed. Node isolation, rational polynomial evaluation, and square-root
bisection suffice.

There are polynomially many panels and quadrature nodes. All endpoints
and approximations have polynomial encoding. Exact polynomial-branch
antiderivatives and their evaluations therefore have polynomial bit length;
the product of polynomially many rational denominators has a bit length
equal to the sum of their bit lengths. Summing the four error budgets
(cutoff, root neighborhoods, analytic quadrature, numerical quadrature)
gives at most `zeta/4`, leaving the stated slack for a certified rational
estimate. This proves the cumulative integration algorithm required by the
compiled theorem.

## Stronger input-accurate inverse, also checked

The analytical note additionally proves an input-accurate inverse, although
the compiled construction needs only mass accuracy. For a positive term
`a x^m` of `H`, define `h_0=a(eta/4)^m` and
`kappa=(eta/4)min(1,h_0)`. On
`[eta/4,1-eta/4]`, both branches of the density are at least `kappa`:
the linear branch uses `1-x>=eta/4`, and the square-root branch uses
`sqrt(h_0)>=min(1,h_0)`.

Every interval of length `eta` contains a centered subinterval of length
`eta/2` inside this interior range. Its mass is therefore at least
`eta*kappa/2`. The rational number `kappa` has polynomial encoding because
`m<=d` is densely bounded. Evaluating both the prefix and total mass to
`mu=eta*kappa/64` gives error at most `2mu` in their difference for any
quantile parameter in `[0,1]`. Strict comparisons preserve the bracket;
an uncertain comparison gives true mass error at most `4mu`, smaller than
the preceding modulus. It therefore certifies input error below `eta`.
Otherwise ordinary dyadic bisection terminates with that input accuracy.
Endpoint quantiles are exact. Requests with `eta>1/2` may use the algorithm
at `eta=1/2`. No dependence polynomial in `1/theta` or `1/eta` is hidden.

This closes both stated analytical outputs and the seven-bit compiled
construction for dense positive-polynomial input. No numerical quadrature
experiment is used as a substitute for the proof. Publication priority
and extensions beyond the stated positive-coefficient dense model are
separate questions.

## Supporting exact checks

The checker `code/quadratic_rank/check_compiled_curvature_mass_knots.py`
was inspected and rerun successfully: 109 exact indexed mass-cell
certificates and 545 exact graph-band checks, sampling grids through
4,194,304 cells without enumerating them. It uses constant-curvature
examples whose cumulative density is piecewise rational, including a
downward-rounded mass oracle with the permitted error. These checks
support the bisection, endpoint rounding, and revised seven-bit constants;
they do not test the general polynomial quadrature implementation, whose
correctness rests on the analytical audit above.
