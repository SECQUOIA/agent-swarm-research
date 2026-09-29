# Independent review of the rational quaternion sign reduction

Date: 2026-09-28. Reviewer: `/root/quaternion_compiler_final_review`.
Status: proof review passed; publication priority remains unestablished.

The reviewed version of
[the reduction](quaternion-circuit-posslp-reduction.md) has SHA-256
`e9d0f6955777010090d4e1b1a9046c9d95b81470b1ba8a7bc8cb234e55bb42c5`.
I did not develop the construction. I independently reconstructed the
quaternion identities, signal bounds, cancellation argument, and size
calculation. I found no substantive correction to request.

The conclusion justified by this review is the stated PosSLP completeness
of a selected coordinate sign for shared rational unit-quaternion circuits,
with the fixed four constants and a nonzero final coordinate in the lower
reduction. The quartic realization is a separate theorem. Neither this
review nor the sign reduction proves that an objective perturbation
preserves a rational minimizer.

## Exact identities and positive scalar parts

Direct multiplication gives
\[
 q(\mathbf i q\mathbf i^{-1})
  =(w^2-x^2+y^2+z^2,\;2wx,\;2xz,\;-2xy).
\]
For a unit quaternion its first entry is \(1-2x^2\). In particular,
the asserted projection is exactly the identity when \(x=0\), including
when the other imaginary entries are nonzero. Conjugation by
\(c=(1,1,1,1)/2\) gives \((w,z,x,y)\), with the orientation used in
the multiplication construction.

The commutator identity follows because
\((rq)\bar q\bar r=\mathbf1\). Multiplication by unit quaternions
preserves norm. When \(w,s\geq0\),
\[
 \|q-\mathbf1\|^2=2(1-w)
      =\frac{2\|v\|^2}{1+w}\leq2\|v\|^2,
\]
so the looser factor two used in the proof is valid. Applying the triangle
inequality to \(\bar q\bar r-\mathbf1\) proves the stated commutator
remainder bound. No independent additive error occurs when either vector
is exactly zero.

The projection estimate follows from
\[
 \operatorname{vec}P(q)-2x e_1
       =(2x(w-1),2xz,-2xy),\qquad
       |w-1|\leq\|v\|^2.
\]
The assumptions \(w\geq0\) and \(\|v\|\leq1/2\) make the asserted
constant four valid. The subsequent uses of this estimate meet both
assumptions. In particular, for arithmetic input signals
\(\|v\|,\|u\|\leq2B\delta\leq2^{-29}\), so the product has positive
scalar part. For the commutator,
\(\|[q,R(r)]-\mathbf1\|\leq8B^2\delta^{a+b}<1\); rotation leaves
the scalar part unchanged. Finally, the scalar part of every projection
is positive because its input selected coordinate has magnitude below
\(1/2\). Positivity is needed only for these signal-level quantities,
not for each internal multiplication involving the fixed generators.

## Tiny-signal generator

Under the generator invariant, \(\|v\|\leq2x\). The third component
of \(v\times R(v)\), which becomes the selected component after
rotation, is \(x^2-yz\). Consequently
\[
 |U_x-2x^2|
 \leq 2|yz|+4(2x)^2(4x)
 \leq4096x^4+64x^3
 \leq65x^3.
\]
The last inequality uses \(x\leq2^{-16}\), with ample slack.
This gives \(x^2\leq U_x\leq3x^2\), while the exact commutator norm
bound gives \(\|\operatorname{vec}U\|\leq8x^2\) and
\(U_w\geq1-8x^2>1/2\). Thus
\[
 x^2\leq2U_wU_x\leq6x^2,
 \qquad
 \|\operatorname{vec}_{2,3}P(U)\|
        \leq2(3x^2)(8x^2)=48x^4
        \leq64(2U_wU_x)^2.
\]
These inequalities preserve the complete invariant, including strict
positivity. Iterating \(x_{j+1}\leq6x_j^2\) gives
\(x_j\leq(6x_0)^{2^j}/6\). The fixed initial point satisfies
\(6x_0<2^{-16}\), which establishes the bound used to choose the
initial arithmetic signal. This reasoning is uniform in the number of
iterations; the exact checks below are only supplemental evidence.

## Uniform arithmetic errors and cancellation

I checked the constants against the full vector error, rather than only
the selected entry. For addition at order \(d\), the inherited errors,
cross product, and scalar-part corrections are bounded by
\[
 (2B+4B^2+16B^3)\delta^{d+1}.
\]
The vector of the unprojected product has norm at most
\(5B\delta^d\). Doubling the inherited error and adding the projection
error gives
\[
 (4B+108B^2+32B^3)\delta^{d+1}
          \leq144B^3\delta^{d+1}.
\]
This estimate allows exact cancellation of the two leading coefficients.
It does not assert that a signal with zero leading coefficient is the
identity.

For multiplication of orders \(a,b\), the cross-product remainder is
at most \(3B^2\delta^{a+b+1}\). The commutator remainder is at most
\(64B^3\delta^{a+b+1}\). After multiplying the former bound by two
and applying the projection estimate, the total error is at most
\[
 (12B^2+128B^3+256B^4)\delta^{a+b+1}
          \leq396B^4\delta^{a+b+1}.
\]
Here \(a+b\geq2\) is sufficient to absorb the projection's higher
power of \(\delta\). All leading coefficients and all four gate error
bounds fit \(2^{20}B^4\). These absolute bounds are valid when either
leading coefficient is zero, including when the actual input quaternion
is not the identity. This point closes the relevant cancellation issue.

## Homogeneous pairs, parameter order, and circuit size

The pair construction preserves the common signal order. Multiplication
gives coefficients \((4C_aC_b,4D_aD_b)\). Addition and subtraction
give
\[
 \bigl(8(C_aD_b\mathbin\pm C_bD_a),8D_aD_b\bigr).
\]
The denominator coefficient is a positive integer, even for a zero
numerator gate. The use of \(P\) on the denominator is necessary and
correct: it supplies the factor two introduced by \(A\) on the
numerator.

The compiler topology, and therefore its macro count \(T\), depends
only on the input arithmetic circuit. The tiny-signal generator is then
chosen with \(r=2T+2\); its operations are not circularly included in
the already fixed count \(T\). The resulting recurrence gives
\[
 \log_2 B_T=(41\cdot4^T-20)/3<14\cdot4^T,
 \qquad
 0<\delta<2^{-64\cdot4^T}.
\]
Since \(64\cdot4^T\geq30+\log_2B_T\), the smallness hypothesis
holds at every gate, including previously built signals when a later
larger bound is used. At the output,
\(C=DW\) is a nonzero integer and the selected-entry error is less
than \(\delta^d/2\). Hence it cannot reverse or cancel the leading
term. Replacing the input output by \(W=2V-1\) is essential to this
nonzero conclusion.

All macros have constant-size circuits over the four stated constants.
The generator and the arithmetic compiler together use \(O(T+r)\)
raw group operations. Repeated occurrences of an input refer to the
same circuit node. Expanding the represented word, the rational
coordinates, \(B_T\), or \(\delta^d\) is unnecessary and would not
be polynomially bounded. The proof does not claim such an expansion.
The upper reduction uses positive common denominators and four integer
numerator circuits. Unit inversion is conjugation, so it introduces no
division or sign uncertainty.

## Targeted exact checks and their limits

I wrote and ran
[an independent Fraction-based checker](check_quaternion_signal_bounds_review.py):

```text
python3 research-20260927/check_quaternion_signal_bounds_review.py
PASS: 36 generator cases; 900 gate cases; 240 nonzero residuals after leading-coefficient cancellation; 30 parameter comparisons.
```

The generator cases include points close to \(x=2^{-16}\), transverse
norm close to \(64x^2\), and both signs of the transverse product.
The gate cases use positive, negative, and zero leading coefficients;
different input orders; several transverse-error directions; and bounds
from one through \(2^{40}\). Every input signal promise, output norm,
and tested error bound is checked with exact rational arithmetic. The
240 nonzero cancellation residuals explicitly challenge the incorrect
stronger assertion that zero leading coefficients must yield identity
quaternions.

These are finite tests. They do not prove the universal inequalities,
the polynomial-time reduction, any novelty claim, or the quartic
realization. The universal conclusions above come from the independent
derivations. No project-wide checks, CI checks, or Lean verification
were run for this review.

A targeted `python3 -` check also passed for final newlines and trailing
whitespace in the two review artifacts, and for local links and math
delimiters in this review. The targeted `git diff --check --` command
reported no issue; the explicit file checks also cover new files that
Git does not yet track.

## Literature and significance limits

I read the existing
[primary-source comparison](quaternion-circuit-posslp-prior.md).
I did not conduct an additional literature search or independently audit
its primary sources. The proof review therefore supplies no independent
publication-priority evidence. The near-identity commutator method and
compressed matrix representations have substantial prior, as that note
explains.

The proved predicate is the sign of one coordinate of a shared circuit's
output. It is not group identity testing, the sign of an explicitly
listed polynomial-length word, or a lower bound for irrational optimizer
output. These distinctions are material to both the complexity claim
and any later application. Subject to the separate realization theorem,
the relevant additional capability is hardness of coordinate comparison
even when the unique bounded optimizer is rational. No solver speedup
follows from this hardness result.
