# Adversarial review of the geometric-grid extensions

Date: 2026-10-02. Reviewed:
[extensions.md](../geometric-dp/extensions.md) and
[oracle-limits.md](../geometric-dp/oracle-limits.md).
This review checks the mathematics and computation model. It does not
establish originality or practical solver performance.

The revised extensions pass this review. In particular, the rational
denominator argument supports the stated bit-complexity bound, projected
growth is sufficient when finite states are fully enumerated, and the
point-oracle lower bound is valid. Two qualifications found during review
have been incorporated into the extension note: rational geometric data
for rational table arithmetic, and the extra trial multiplier for bags
with no gridded coordinates. No further mathematical correction is needed.

## 1. Certified tables and exact integer stopping

The unknown-growth exact-integer schedule is complete. On the first safe
trial, its chosen horizon satisfies
\(nh_J^2\le\theta^2\) and
\(B\le1/(4\theta^2)\). Thus the exposed integer vector has squared
error at most \(1/4\) and equals the optimizer. One further stage has
zero correction. Earlier trials can stop only on an actual valid
certificate; otherwise they contribute the stated geometric work sum.

The finite-precision formulas also hold. A uniform assembled-table error
\(\Delta\) gives the certified interval

\[
[\widetilde F(y)-D(y)-\Delta,
  \widetilde F(y)+\Delta].
\]

Its width is \(D(y)+2\Delta\). With
\(\Delta\le Lnh^2/16\), the recurrence coefficient
\(2L/(5c)\), invariant constant
\(\max\{1,6L/(11c)\}\), and final width \(Lnh^2\) are correct.
Only error control on the finite grids is required.

Rational objective entries alone would not make the corrected tables
rational. The revised Section 3 now explicitly assumes rational
\(L\), interval endpoints, initial center, and grid parameters, which
makes the penalties rational too. This resolves the arithmetic gap in the
initial version. The cost of producing certified approximations remains
an explicit additional assumption.

The value-lattice argument is valid. Once a feasible integer objective
value \(U\in Q^{-1}\mathbb Z\) is isolated exactly, a valid bound
\(\mathrm{LB}>U-1/Q\) excludes every smaller attainable value. A
certified interval of width strictly less than \(1/Q\) isolates its
one attainable lattice value. This provides an exact certificate without
requiring the unrounded numerical gap to equal zero.

## 2. Rational-polynomial bit complexity

Section 5's common-denominator argument is sound. It addresses the main
possible source of hidden arithmetic growth: repeated recentering.

For coordinate \(i\), its original endpoints, initial center, and the
global scale \(s\) have denominators dividing \(Q_i\), with
\(O(b)\) bits. At stage \(j\), an untruncated geometric distance
after \(k\) steps has denominator dividing

\[
\operatorname{den}(s)2^{j+r(k-1)}.
\]

Adding it to a previously selected center takes the least common
multiple of powers of two. The new exponent is their maximum, rather
than their sum. Clipping uses an original endpoint. Therefore the proposed
\(E=J+Cr2^r(J+1)\) bounds the dyadic exponent throughout all stages.
Coordinate magnitudes stay within the original box, so their numerator
and denominator bit lengths are \(O(b+E)\).

For a monomial with exponents \(\alpha_i\), its coordinate denominator
divides

\[
\left(\prod_i Q_i^{\alpha_i}\right)
2^{E\sum_i\alpha_i}.
\]

The total degree is at most \(d\), so one global factor
\(2^{DE}\) suffices; a factor \(2^{nDE}\) is unnecessary.
Using \(D=\max\{2,d\}\) also covers every squared interval length.
Consequently all factor values and corrections have denominators dividing
the displayed common denominator

\[
8\operatorname{den}(L)
\left(\prod_a\operatorname{den}(a)\right)
\left(\prod_i Q_i^D\right)2^{DE}.
\]

Every finite DP message selects a sum of assigned factor and correction
values in its subtree. Assigned terms occur once, so neither branching
nor depth introduces another denominator factor. The stated magnitude
bound controls the numerators. Together these yield

\[
H=O\bigl((T+nD+1)b+DE+\log(T+n+1)\bigr).
\]

Rational arithmetic must reduce fractions after operations, as the note
requires. Individual unreduced cross-products have only a constant
multiple of these bit lengths. Elementary multiplication, division, gcd,
and comparison are covered by the conservative \(O(H^3)\) charge.
Repeated squaring gives the stated monomial-operation count, and child
message additions total over tree edges. Thus the stated \(O(AH^3)\)
bound is a sufficient bound for the described implementation, with input
reading and supplied decomposition accounted for as specified.

The pure-integer simplification is also valid: coordinate values and
retained interval lengths are integers, so neither \(Q_i\) nor a grid
dyadic denominator enters objective or message values. The trial-step
arithmetic still needs \(O(b+J+r)\) bits before taking floors, which
the proposed \(H_{\mathbb Z}\) includes.

The degree caveat is substantive. For
\(F(x)=x^2+x^{2^k}\) on \([0,1/2]\), the claimed constants
\(c=1\) and \(L=3\) hold for \(k\ge3\). At \(1/2\), the
reduced denominator is exactly \(2^{2^k}\): its numerator
\(2^{2^k-2}+1\) is odd. Exact rational tables therefore require
exponential output length in the binary exponent's bit length. The note
correctly restricts its polynomial-time claim to polynomially bounded
numerical degree, fixed width, and bounded conditioning.

## 3. Fully enumerated finite states

The projected-growth extension is valid. Fix a feasible finite-state
assignment \(z\). Because the gridded product domain is independent of
\(z\), coordinate rounding of \(x\) keeps \(z\) and feasibility
unchanged. Uniform coordinate semiconcavity supplies the same expected
rounding bound. The inequality

\[
F(x,z)-f^*\ge c\|x-x^*\|^2
\]

then controls exactly the coordinates being recentered. No metric,
uniqueness, growth, or curvature is needed in the fully enumerated states.
All globally optimal pairs must still share the same exposed vector
\(x^*\); that remains a substantive assumption.

Equivalently, the finite lower envelope \(\min_zF(x,z)\) preserves
coordinate semiconcavity: after subtracting the common coordinate
quadratic, an infimum of concave functions is concave. Keeping \(z\)
explicit in the DP preserves the supplied factor scopes. There is no
claim that eliminating \(z\) preserves those scopes.

If the gridded coordinates are integer, the lattice-separation argument
identifies their shared optimum. On the next stage their correction is
zero; the exact DP's lower-bound identity then forces its chosen finite
states to attain the global optimum. Multiple optimal finite-state
assignments cause no problem. The \(n_x=0\) case correctly reduces to
one ordinary finite-state DP.

The refined table count in (13) is valid for one trial. Its factor
\(d_t\) accounts for explicitly retained state combinations, while
\(p_t\) controls the resolution exponent. A qualification was needed
for multiple unknown-growth trials: when \(p_t=0\), its work has no
geometrically increasing factor \(\theta^{-p_t}\), so a universal
geometric multiplier does not bound that term's repetitions. The revised
note now includes an additional \(m^*+1\) factor for these terms, or
permits the coarser bound using a positive global gridded-coordinate
exponent. This resolves the cost issue without changing any certificate
or convergence claim.

Discrete feasibility relations can be represented by forbidden table
entries if their scopes are included and they involve only fully
enumerated states. Restrictions involving rounded coordinates would need
a separate feasible-rounding argument, as the note states.

## 4. Private recourse

The recourse extension is sound under its explicit assumptions. Compact
fixed private feasible sets and joint continuity give attained minima.
Subtracting the common coordinate quadratic before taking the infimum
preserves concavity. The projected objective therefore has the stated
summed coordinate-curvature bound.

The certified private oracle supplies both lower values and feasible
witnesses. Midpoint table values have the asserted error bounds, and the
selected witnesses combine because private variables share no constraints.
This gives a feasible original-model upper bound, not only a bound on an
unreconstructed reduced objective. The note correctly charges global
private optimization and feasible reconstruction to the runtime.

The parameter-dependent-set counterexample \(f(x)=|x|\) is correct
and explains why affine dependence in a private objective alone does not
justify inherited semiconcavity. Depending on fully enumerated states is
different: conditional on those states, the private set stays fixed during
rounding. The proposed combined extension respects this distinction.

## 5. Point-oracle lower bound

The lower-bound note passes this review and a delegated independent
review. Its bump is smooth through the support boundary, has one global
minimizer, and satisfies global quadratic growth on the feasible cube.
The derivative formulas are correct. The displayed estimates actually give

\[
\partial_{ii}f_z\le(8/e+8)D/r^2<12D/r^2.
\]

The largest valid growth constant lies between \(D/p\) and \(4D/p\),
and the smallest valid upper coordinate-curvature bound lies between
\(2D/r^2\) and \(12D/r^2\). Thus the supplied conditioning ratio
is within a constant factor of the best possible ratio for these functions.
It is not an artifact of an arbitrarily loose supplied bound.

The packing count and its conversion to
\(\Omega_p((L/c)^{p/2})\) are correct. Along an all-zero transcript,
each query tests at most one disjoint open support, and the final output
can cover only one additional support. Smoothness makes boundary queries
uninformative even when the complete derivative jet is supplied.

For randomized algorithms with a uniform query cap, fixing the random seed
gives the same zero-answer path. The first hit for any candidate must occur
on that path. Averaging over uniformly hidden centers therefore gives the
stated success bound \((q+1)/N\). The result concerns a query cap,
not an expected-query budget.

The note's scope restrictions are essential and present: these are smooth
point-oracle instances, not an oracle lower bound for explicit polynomial
input. An explicit bump formula reveals its center. The construction does
not establish optimal logarithmic factors, optimal bit complexity, or
practical runtime.

## 6. Verification record

This review used algebraic inspection and the read-only commands
`cat research-20261002/geometric-dp/extensions.md`,
`cat research-20261002/geometric-dp/oracle-limits.md`, and targeted
`sed -n` reads to confirm the two revisions. A delegated reviewer
independently checked the oracle construction and adaptive/randomized
adversaries. No executable checks were repeated, and no external sources,
project-wide verification, or CI inspection were used.
