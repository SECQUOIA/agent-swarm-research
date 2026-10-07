# Review of signed normalization and rational certificate size

Date: 2026-10-02. Scope: independent proof review of
[the proposed-point certificate](geometric-box-point-certificate.md),
focusing on its scale, metric, and bit accounting. The parent review
separately checks the radial certificate argument. No tests, external
searches, or CI checks were run for this supplement.

The positive-margin theorem passes these checks. Its factor-sixteen
guarantee concerns the stated normalized metric. The author applied
the minor metric-comparison qualification identified below.

## Scale and signed branches

After the first-order check, the linear displacement term is nonnegative
on every feasible ray. The separate endpoint check rejects each allowed
axis endpoint whose objective increment is nonpositive. For candidates
that pass both checks, the minimum endpoint increment `M` is positive,
and each tested signed unit vector belongs to the normalized shell.
Consequently the optimal normalized margin satisfies `g<=M`.

The proposed choice

```
L=2 max{M, max_(i,s) A_ii (w_i^s)^2}
```

therefore has both properties needed by the proof: `L>=2g`, and every
fixed-sign quadratic diagonal coefficient is at most `L/2`. The first
property justifies the initial trial's factor-sixteen comparison. The
second bounds the independent-rounding error. No positivity of the
diagonal coefficients is required. For a purely linear objective, `M`
supplies a positive scale even when all quadratic coefficients vanish;
for negative diagonal terms, rounding contributes a nonpositive error.

This is a bound on fixed-sign branches. The normalized function need
not have any finite global coordinate semiconcavity bound across zero.
For example, `F(d)=d_1^2+d_2^2+d_1 d_2`, with first-coordinate side
widths `1,2` and `d_2=1`, gives one-sided normalized derivatives `1,2`
at `z_1=0`. Sign-preserving rounding never crosses that kink, and zero
is kept fixed. Thus it preserves both the normalized coordinate mean
and the physical displacement mean, which is exactly what the
off-diagonal and linear expectation identities require.

## Metric distortion

Let `w_min,w_max` be the smallest and largest positive allowed side
widths. For every displacement,

```
w_min^2 ||z||_2^2 <= ||d(z)||_2^2 <= w_max^2 ||z||_2^2.
```

In the nonnegative-margin case, these inequalities imply
`w_min^2 g_E <= g <= w_max^2 g_E`. A successful certificate therefore
gives physical Euclidean growth at least
`(sigma+b_delta/n)/w_max^2`. Returning the simpler value
`sigma/w_max^2` loses at most the stated factor
`16(w_max/w_min)^2` relative to the best physical margin.

The loss is real for this normalization. On `[-epsilon,1]`, the
objective `F(x)=x^2` at candidate zero has physical margin one, but
normalized margin `epsilon^2` and proposed scale `L=2`. Hence the
normalized conditioning is `2/epsilon^2`. An aspect-independent
physical-conditioning claim does not follow.

**Applied scope qualification.** The displayed comparison between `g`
and `g_E` is now explicitly restricted to the nonnegative-margin
case. For negative margins its stated order need not hold. On
`[0,1] x [0,2]`, `F=x_1^2+x_2^2-3x_1x_2` at zero passes both
preliminary checks, but `g_E=-1/2` and
`g=(5-sqrt(45))/2`. These violate the unqualified comparison.
All conclusions following a positive certificate satisfy the required
qualification. The draft also explicitly distinguishes fixed-sign
curvature from global semiconcavity.

## Rational size and graph width

The input length explicitly includes the rational proposed point and
box endpoints. Substitution of fixed coordinates, translation by the
point, and computation of signed widths and endpoint increments have
polynomial bit cost. They preserve the pair-interaction graph: signed
widths change unary and pair factor values, not their variable scopes.

For clarity, let `D` clear all denominators after fixed-coordinate
substitution, including the proposed point and remaining endpoints.
Its bit length is polynomial in the original input length. The
normalized unary linear coefficients, quadratic coefficients, and
endpoint increments have denominators dividing `D^3`. At a trial,
the unsigned grid has common denominator
`T=n 2^(r(K+1))`; reflection does not change it. A common denominator
for corrected table values divides
`D^3 2^(2r+3) T^2`. Its bit length is polynomial in the input length
and `rK`. This also covers the final root correction `sigma/n`.

Each finite DP message selects a sum of assigned factor values. It
does not multiply their denominators across bags. Numerator sizes add
only the input coefficient sizes and the logarithm of the number of
terms. Exact comparison, grid construction, and certificate verification
therefore have the claimed bit cost.

Each variable has at most `2K-1` signed states, so no enumeration of
orthants is needed. At the successful trial,
`K=O(sqrt(kappa) log(2n sqrt(kappa)))` and
`r=O(1+log(kappa))`. Absorbing powers of `log n` into a
parameter-dependent factor times a fixed power of `n` gives
`f(p,kappa) poly(I)` with an absolute input exponent. Here `kappa`
is the normalized ratio `L/g`; the rational side widths can make it
large even when physical Euclidean conditioning is small.
