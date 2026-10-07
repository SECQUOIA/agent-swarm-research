# Assessment: what the two-copy convex point reduction changes

Date: 2026-10-02. Scope: independent significance and correctness
assessment of the actual
[two-copy quartic construction](convex-point-radical-comparison.md).
The separate full proof review is owned by another reviewer. This note
does not claim NP-hardness, a complexity separation, or publication priority.

The reduction identifies a substantial arithmetic requirement for any
extension from strongly convex residual recourse to arbitrary convex
residual point output. It applies to a point close to **any** optimizer,
not just to a minimum-norm or lexicographic selector. Its implications
depend on the requested output and on whether running time is deterministic
or only an expectation.

## 1. The actual reduction supports the stated implication

I read the complete saved proof. The two comparison copies have opposite
linear couplings to their bounded auxiliary variables. Their strong
convexity makes each original zero face have exactly one candidate
minimizer. Its inward derivative gives the claimed equivalence between
the sign of the radical comparison and whether the auxiliary coordinate
is zero. The upper-bound derivative has the correct sign for both copies,
so reversing the coupling does not introduce an exception at one.

The quartic coupling is nonnegative. Each base copy is bounded below by
its own optimal value, and the appropriate endpoint of `y` attains the
sum of those two values while making the coupling zero. Hence **every**
optimizer must minimize both base copies. Their uniqueness fixes all
base coordinates, and the one positive auxiliary coordinate forces
`y=0` or `y=1`. This avoids the escape in the preceding canonical-selector
example, where a different optimizer could be chosen easily.

The division-free Hessian calculation proves convexity throughout the
closed box, including points where one or both auxiliary coordinates
vanish. Its two negative square-completion terms affect distinct base
coordinates; their bounds are not incorrectly added to the same diagonal.
The two tree decompositions connect through the two `y` bags without
increasing their maximum size beyond three. Thus degree four, bounded
coefficient magnitudes, and treewidth at most two are supported by the
actual construction.

The equality preprocessing also checks. In the multiquadratic field
containing all radicals, every nonsquare radical has trace zero by
transitivity, while an integer has trace equal to that integer times
the extension degree. An integer sum of positive radicals would therefore
equal the sum of its perfect-square terms, contradicting positivity of
the remaining terms. Only integer square-root tests are needed by the
reduction; it need not compute or factor the extension field.

After this preprocessing, the output coordinate is separated by a
constant: `y*=0` or `y*=1`. Distance at most `1/4`, in Euclidean or maximum
norm, is sufficient to decide the strict comparison. No objective-gap
to coordinate-gap conversion is assumed in this last step.

## 2. The output distinction is decisive

| Promised output | Consequence of this reduction |
| --- | --- |
| Any point within distance `1/4` of an optimizer, in deterministic polynomial time | A deterministic polynomial-time Square Root Sum algorithm |
| An always-correct point algorithm with expected polynomial work | A Las Vegas expected-polynomial Square Root Sum algorithm |
| A compact exact optimizer descriptor with polynomial-time coordinate evaluation | The same implication, by requesting only constant coordinate precision |
| A compact formula with no efficient coordinate evaluator | No such implication; the original convex program already defines the optimizer |
| Certified objective intervals of requested width, or an approximate optimal core | The construction does not turn fixed requested precision into the radical decision |

The last distinction is concrete. Changing the decisive coordinate away
from its optimal endpoint can cost only a multiple of the square of a
very small auxiliary coordinate. Excellent objective accuracy can coexist
with a wrong order-one `y` coordinate. Polynomial dependence on the number
of requested **value** bits is therefore compatible with the reduction;
the requested precision needed to resolve a particular arithmetic
comparison may itself be large.

The reduction does not settle every possible meaning of an exact value
certificate. In particular, a symbolic value with unrestricted exact
comparison operations is stronger than a requested-bit interval oracle.
No claim about that stronger interface follows merely from the displayed
constant-distance point reduction.

## 3. Core-only smoothing cannot hide the residual comparison

The independent noisy core in the construction has fixed dimension one,
fixed curvature two, fixed projected growth one, and fixed noise scale.
Its optimum is explicitly computable for every sample. The residual
comparison problem and its decisive `y` coordinate do not change at all.

Therefore a proposed merely-convex-residual extension with expected
polynomial setup and polynomial expected coordinate evaluation would
solve the comparison in expected polynomial time. This remains true if
the finite noise grid is chosen from the input: draw that grid's sample,
run the purported algorithm, and inspect its constant-precision `y`
output. A correct sample answer gives the same original decision on
every draw. The expected guarantee yields Las Vegas time, not a
deterministic worst-case polynomial bound.

This argument does not apply to the completed full-ambient-noise theorem.
Perturbing residual coefficients changes the comparison encoding itself.
Nor does it apply to a theorem with a supplied uniform residual modulus:
the new objective has a residual Hessian null direction at points with
both auxiliary coordinates zero. At its unique optimizer the relevant
curvature can be positive but arbitrarily small. The construction supplies
no controlled global point-growth or residual-conditioning parameter.

## 4. What width and curvature do, and do not, explain

This is already a convex problem: its negative curvature is zero.
Its primal interaction graph has constant treewidth and bounded numerical
coefficients.
Consequently a general unconditioned width-FPT algorithm for constant-
accuracy nonlinear optimizer coordinates would already have the radical-
comparison consequence on this class. Calling this an NP-hardness or
parameterized-hardness theorem would go beyond the proof.

The completed algorithms parameterized by point growth remain consistent
with the example. The decisive coordinate can have extremely small
curvature and growth despite bounded diagonal upper curvature. That
conditioning cannot be discarded solely because the objective is convex
or its interaction graph is narrow. In particular, the easy convex-QP
point-output baseline does not automatically extend to general convex
polynomials of fixed degree.

There is a separate unconditional representation-size observation for
**explicitly listed univariate coordinate polynomials, even sparse ones**.
Choose `n>=2` distinct prime radicands and `B=1`. The comparison is
strictly positive, so the minus copy has its auxiliary coordinate zero and retains the unperturbed
root

\[
                        s=\frac{\sum_i\sqrt{p_i}}{KM}.
\]

The multiquadratic extension has independent sign automorphisms. Distinct
signed sums are distinct and nonzero because the prime radicals are
linearly independent over the rationals. Thus `s` has `2^n` distinct real
conjugates, exactly `2^(n-1)` positive, paired by negation. Any nonzero
rational univariate polynomial vanishing at `s` must vanish at all these
conjugates. Descartes' rule of signs therefore requires at least
`2^(n-1)+1` nonzero coefficients. Sparse monomial listing cannot avoid the
exponential output length. A straight-line arithmetic circuit is a
different representation and is not covered by this listing bound.

The source promise and input size can be checked separately. With `B=1`
and `n>=2`, the sum of the positive prime radicals exceeds one, while
`1<2KM`, so the reduction takes its stated nontrivial branch and the
minus copy is indeed inactive. For a polynomial-length family, choose
the first `n` primes. Even the coarse bound `p_n<=2^n`, from repeated
Bertrand intervals, gives only `O(n^2)` bits for their list and its
rational normalization. This suffices for a superpolynomial output bound
in total input length; no efficient factorization or prime enumeration
is performed by the comparison reduction.

This size issue is independent of whether the comparison instance is
easy. The inactive root here has straightforward numerical evaluation by
summing square roots to the requested accuracy. It motivates joint,
circuit, or other compact algebraic descriptions.
It does not remove the point-evaluation implication when such a compact
description is additionally promised a polynomial-time coordinate oracle.

## 5. Recommended direction for the present investigation

The strongest positive direction remains structured recourse with exact,
checkable certificates. The
[interior-core integer-flow theorem](smoothed-interior-core-flow.md)
has precisely that structure: a polynomial residual-network certificate
selects a flow, leaving only the small core for algebraic completion.
Its proof does not require evaluating a generic high-dimensional convex
polynomial optimizer. Extending its boundary certificate or other
constrained recourse classes is a concrete route beyond the present
results.

For general convex polynomial residuals, keep value and coordinate output
as separate targets. A useful value-only theorem should specify certified
upper and lower intervals, a common finite-noise law, and a work bound in
the requested value bits. A full point theorem needs an additional
representation or extraction mechanism strong enough to address the
comparison consequence. Merely renaming the original optimization problem
as an exact implicit descriptor does not provide that mechanism.

The reduction justifies treating unconditioned full-point extraction as
an arithmetic frontier, while continuing quantitative-growth results,
value certification, and certificate-rich constrained recourse. It does
not justify abandoning these positive directions or asserting that a
general point theorem is impossible.

## Verification record

This assessment read the complete actual two-copy draft and independently
checked the endpoint forcing, Hessian-loss accounting, equality trace,
graph gluing, and output implications. The sparse univariate output bound
uses the independent-prime conjugates and Descartes' rule separately from
the comparison implication. The construction's quantitative diagnostic
and full proof review are owned by its author and designated reviewer and are not claimed as tests run here. A scoped inline Python
check passed for local links, whitespace, math delimiters, and control
characters. No external literature search, project-wide verification,
CI inspection, or index edit was made.
