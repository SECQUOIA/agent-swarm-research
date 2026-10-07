# Integration review of the point-output report sections

Date: 2026-10-03. Verdict: **pass, with minor presentation corrections**.
No mathematical blocker, changed theorem constant, or dropped structural
promise was found. This was a read-only review of the report sources;
the reviewer did not edit them.

The actual saved files reviewed were
[Section 2](../../document/sections/02-global-points.tex) and
[Section 3](../../document/sections/03-domain-boundary.tex), with
[the input/output contracts](../../document/sections/01-contracts.tex)
read for context. The reference arguments were the already accepted
[global extension](../../global-point/theorem.md),
[original positive-core review](review.md), and
[quartic-reduction review](hardness-audit.md), with the two historical
quartic notes reread to check the common amplifier constants.

## Global theorem

The theorem retains global convexity, explicit sparse rational input,
numerical-degree dependence, an arbitrary rational polyhedron, exact
feasibility of rational output, and one fixed minimum-norm selector.
Convexity certification is charged, and the zero-variable case is
separate. The claim is not enlarged to binary-degree or circuit input.

The tangent quadratic constant `K_D=(D+1)D^(D+2)`, averaged-Hessian
curvature bound, Farkas certificate sign, coefficient bound
`B_r=(r+1)2^r r^r`, and Hoffman factor all match the reviewed theorem.
The radius argument still bounds the affine slope from both sides and
proves bounded equal-value representatives before asserting attainment.
The global error bound uses only a bounded optimizer, not a bound on
all feasible points.

The fixed-selector schedule retains denominator
`4*8^(D-1)*R^D*Gamma^D`, rather than incorrectly reusing the bounded-set
factor two. Its proof allows the projection onto the original optimizer
set to lie outside the radius box. The regularized minimizer lies inside
that box, and sparse evaluation survives affine-hull reduction. The
simultaneous objective-precision dependence matches the companion.

## Cubic and quartic boundary

The cubic theorem retains boundedness, rational polyhedral constraints,
degree at most three, convexity on the actual domain, and the original
Euclidean norm. Affine-hull reduction precedes the PSD Hessian argument.
The reflection factor `1+R/rho`, transverse denominator `384MR^2`,
integer-minor eigenvalue estimate, gradient row in the optimizer slice,
and exact-feasibility repair are unchanged. The selector constant
`1024 R_x^4 Gamma_P^4` is correct.

Both quartic reductions still concern convexity on the box. The report
does not claim an unconditional complexity separation, uniform point
conditioning, or bounded width for the PosSLP construction. The two
base curvature bounds, amplifier coefficient `1/192`, Hessian identity,
and endpoint uniqueness argument match the accepted notes. The source
signal `2A-1` handles zero PosSLP output. The radical equality reduction
retains its positive-summand assumption and does not assume a
factorization algorithm.

## Minor corrections sent to the integrating author

1. In Section 2, the displayed definitions of `ell` and `c` contain
   literal `],da` instead of the differential spacing `]\,da`
   (lines 61 and 63 at review time). Replace the commas with `\,`.
2. In Section 2's Bregman estimate, write “For `E>0`, on
   `0<=t<=E^(-1/D)`...” before the interval calculation. The following
   zero-gap paragraph is already correct; the qualification simply
   avoids an undefined expression at zero.
3. In Section 3, qualify the endpoint-curvature formula as applying
   before optional whole-objective scaling. The preceding paragraph
   permits that scaling, which multiplies this curvature too.
4. In Section 3's unit-box coefficient discussion, state that the
   radical construction discards the aggregate constant term. The
   complete companion already does so; the clarification connects its
   bounded collected coefficients to the report's theorem.

These do not require changes to the proved statements or any new
research. For additional proof readability, “assume `H_c` has positive
rank for the next estimate” can be inserted after the affine branch,
before introducing its smallest positive eigenvalue. The branch is
already handled correctly, so this is optional.

## Checks and limits

Commands used were complete targeted `cat` reads of the two TeX files,
the contract section and both historical quartic reductions, together
with `rg -n` and a targeted `sed -n` reread of the current global theorem.
The review was analytic and did not rerun already completed arithmetic
diagnostics or compile the report. The author separately reported a
successful targeted build. Local-link, paired-fence, and whitespace
checks for this review are recorded by the review-directory check.
No project-wide verification or CI inspection was performed.
