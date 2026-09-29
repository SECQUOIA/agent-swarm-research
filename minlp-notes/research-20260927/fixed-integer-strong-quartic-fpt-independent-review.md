# Independent review of the FPT quartic candidate-list theorem

Date: 2026-09-28. Reviewer: `fixed_quartic_fpt_adversary`, assigned only
after the proof strategy was frozen. A separate fresh reader,
`radius_fpt_source`, checked the preprocessing bound, radius, and primary
integer-query interface. Neither reviewer developed the submitted proof.

Reviewed draft: [fixed-integer-strong-quartic-fpt.md](fixed-integer-strong-quartic-fpt.md),
SHA256 `4819e48aded828a9dd335e19e759425c0e59262dc731a31504a312c65e039e97`.

**Finding.** No substantive correctness or FPT accounting gap was found
in the submitted candidate-list theorem. Its exact-selection consequences
correctly depend on the separately reviewed continuous observable
comparison theorem. The review found a stronger conclusion: this algorithm
contains every optimal integer block. The author has independently
rechecked that strengthening; the final amended statement was then
read in full and accepted as recorded below.

## 1. Fixed oracle targets and the transcript argument

The proposed algorithm rejects every queried integer point after recording
feasible queries. This is a legitimate execution of the cited feasibility
algorithm for the fixed empty set. Each returned inequality is rational,
valid on the empty set, and strictly excludes its query. The deterministic
gradient routine depends only on the original input and the query, so the
oracle is a fixed function rather than an adaptive choice depending on
an unknown incumbent.

At a query where the approximate gradient vanishes, the list algorithm
stops. Completing its empty-set oracle there with the explicit inequality
\(x_1\le z_1-1\) proves that this stopping execution is a prefix of a
valid full oracle execution. The completion has the same answer-size
and time bound. The case \(k=0\) is handled separately before this
construction. Thus the running-time proof does not presume that the
list already has an optimum, or define an incumbent before termination.

The draft's final convex-hull transcript argument is correct. A stronger
and simpler version also resolves any concern about extending a finite
transcript to a total oracle with controlled cost. Suppose a particular
global optimal block \(w\) is absent from the completed list. Hardcode
\(w\), whose encoding is \(O(k(1+\langle R\rangle))\), into an
oracle for the singleton \(\{w\}\). Return membership exactly when
the query equals \(w\). At every other query use the original domain
or gradient cut. For a feasible query \(z\ne w\), the estimate

\[
q(z)^{\mathsf T}(w-z)
\le g(w)-g(z)-\frac\mu4\|w-z\|^2
\le-\frac\mu4
\]

makes that cut valid for the singleton. A zero approximate gradient at
such a query is impossible, because it would make \(z\) the unique
integer minimizer. Domain cuts also retain \(w\). This is a total
valid oracle with the same polynomial answer cost; equality to the
hardcoded point is cheap. Since the actual execution never queried
\(w\), its entire transcript agrees with this singleton oracle and
would incorrectly report emptiness. Therefore every optimal block must
occur in the list. An early zero-gradient stop also has this property,
because the queried point is the unique optimum.

The preservation estimate uses \(g(w)\le g(z)\), so it continues
to hold after other optimal queries have been recorded and rejected.
It does not rely on a positive objective gap or on exact value queries.

## 2. Uniform running time and the strongest source contract

I directly read [Ari--Hildebrand v2, Definition 3.4 and Theorem 3.5](https://arxiv.org/html/2609.18266v2#S3.SS3),
[Hildebrand--Goess v2, Theorem 9 and Appendix B](https://arxiv.org/html/2409.05308v2),
and [Basu, Theorem 5.7 and Remarks 5.9--5.12](https://arxiv.org/html/2110.06172v6#S5.SS2).
The exact interface used in the draft is supported: integer queries,
rational strict separators, closed targets of arbitrary dimension,
an explicit containing box, and absolute polynomial exponents in the
radius and answer-cost bounds. Recursive queries are submitted in the
original integer coordinates. Empty sets are allowed. The underlying
appendix selects deterministic lattice routines.

This imports an existing FPT oracle theorem; it does not independently
reprove every rounding and lattice-bit argument in that theorem. Basu's
no-bisection observation is relevant prior work and is properly credited.
The draft correctly avoids the separate objective-bisection lemma whose
rational-value assumptions need not hold for quartic fiber minima.

The separate reader directly checked
[Hildebrand--Koeppe v3, Theorem 1.1(b)](https://arxiv.org/pdf/1006.4661v3).
Its bound specializes to deterministic
\(2^{O(k\log(k+1))}L^C\) integer linear feasibility with an
absolute \(C\), including unbounded rational polyhedra. Rowwise
denominator clearing is polynomial in the explicit input; for an
integer polynomial \(p\), the weak inequality \(p\le0\) is
equivalent on integer points to \(p-1<0\). Use degree bound two and
a constant objective. The returned coordinate encoding is bounded by
\(2^{O(k)}L^{O(1)}\), with an absolute exponent.

For the radius calculation, write \(b=\|\nabla f(0)\|_1\),
\(\Delta=C_0-f(0)\), and \(t=\|x\|\ge R\). Then

\[
 f(x)-C_0
 \ge t(\mu t/2-b)-\Delta
 >t(|\Delta|+1)-\Delta>0.
\]

Thus all optimizers and the initial feasible point lie inside the
specified radius. Coercivity and the closed feasible domain justify
attainment. Fixed degree makes the encoding of the radius polynomial
in the initial point's encoding and \(L\), giving
\(\langle R\rangle\le2^{O(k)}L^{O(1)}\).

The gradient routine always uses the original polynomial and coordinates.
Its input and output sizes are bounded by a fixed polynomial in
\(L+k+\langle R\rangle+t\). Substitution into the source theorem
therefore preserves \(2^{O(k\log(k+1))}L^C\), with absolute
\(C\). No polynomial exponent is composed through \(k\) affine
dimension reductions. This closes the critical FPT-versus-XP issue.

## 3. Gradient approximation and exact selection

The projected objective is smooth and globally \(\mu\)-strongly
convex: the fiber minimizer is unique, the fiber Hessian is invertible,
and the standard implicit-function argument gives the stated gradient.
I rechecked the explicit bounds \(D,S,K\). They bound the fiber
minimizer and the cross-Hessian on its unit neighborhood. The requested
objective error gives distance at most \(\eta\), and therefore
componentwise gradient error at most \(\mu/(4k)\). Its Euclidean
error is at most \(\mu/4\), including \(k=1\).

[Slot--Steurer--Wiedmer v1, Corollary 1.2](https://arxiv.org/html/2511.03440v1)
does return a rational approximate point, with ordinary polynomial bit
complexity and dimension included in the encoding. The fiber is
unconstrained, convex, and coercive, so its assumptions hold. If an
implementation expects an accuracy below one, it can request the
minimum of one and the displayed accuracy; that only strengthens the
guarantee. No exact value or stationary-point computation is used here.

The lattice margin follows from \(\|w-z\|\ge1\), absorbing
the first-order error into the strong-convexity quadratic term. It is
an integer-point statement and is not claimed as a separator of the
continuous objective sublevel.

The exact-selection construction uses a sum of two independent fiber
objectives and their difference as a polynomial observable. Its global
curvature remains at least \(\mu\). This is exactly the supplied-
curvature input model of the reviewed continuous theorem; full-basis
positive Gram closure is not assumed. All pairwise comparisons and all
threshold comparisons can be generated after the oracle-free list is
known. Squaring the FPT list-length bound preserves its form. The
result is a nonadaptive batch of PosSLP queries, not a many-one reduction
to one query. This review treats the separately reviewed continuous
observable theorem as a dependency rather than rechecking its complete
Newton and elimination proof.

## 4. Optimal-block count and significance

The proposed amendment's bound of \(2^k\) optimal integer blocks is
correct. If two distinct optimizers share coordinatewise parity, their
midpoint is an integer point of the convex polyhedron. Strong convexity
makes its projected value strictly smaller. Hence each parity class has
at most one optimizer. The bound is sharp for
\(f(z,y)=\sum_i(z_i-1/2)^2+\|y\|^2\) on an unrestricted integer
block. This is an elementary consequence, not a separate novelty claim.

The strongest direct quadratic comparator should remain visible:
[Del Pia v2, Theorem 3](https://arxiv.org/html/2311.00099v2) gives ordinary
FPT exact convex mixed-integer quadratic optimization with the number
of integer variables as parameter. It permits general mixed linear
constraints and does not require positive curvature. The present
quartic theorem permits richer objectives but has narrower domain and
curvature assumptions; exact selection is oracle-relative. It does not
subsume that quadratic theorem. I read its statement and the concluding
oracle discussion in Section 4.4 directly.

The contribution assessed here is the implementation of a coarse
rational integer-cut oracle for a large continuous quartic block,
together with the finite candidate-list separation of discrete search
from exact arithmetic. The general integer-query algorithm and the
no-bisection idea are established prior work. Practical speedups are
unproved. Focused searches did not identify an identical application,
but they do not establish publication novelty.

## 5. Targeted computational challenges

The independent script
[check_fixed_quartic_fpt_transcript_review.py](check_fixed_quartic_fpt_transcript_review.py)
uses exact rational arithmetic and a one-dimensional integer-feasibility
routine on affine lattice lines. Objective values are unavailable to
the search and are used only afterward to verify its output. The tests
include embedded deficient-dimensional domains, a transformed zero
normal, errors of norm exactly \(\mu/4\), exact ties, zero-gradient
early stops, and very large coordinate encodings.

Command actually run:

```text
python research-20260927/check_fixed_quartic_fpt_transcript_review.py
```

It passed 1,296 affine-line cases with 3,429 queries, including 216
tied-optimum cases and 42 zero-gradient early stops. Every optimal
point was retained, including ties after another optimum was cut off.
A box of radius \(2^{100}\) took 101 queries and retained both exact
optima. These finite tests challenge the transcript and cut mechanisms;
they neither prove the general theorem nor verify the imported
high-dimensional feasibility algorithm. No Lean, project-wide tests,
or CI inspection was used.

A targeted Python check of this review's local links, final newline,
and trailing whitespace also passed, as did:

```text
git diff --check -- research-20260927/fixed-integer-strong-quartic-fpt-independent-review.md research-20260927/check_fixed_quartic_fpt_transcript_review.py
```

## 6. Amendment check

The all-optima statement, singleton transcript proof, and parity bound
were independently derived above and sent to the author. The final
amended file was subsequently read in full at SHA256
`77122724ae61280d9911216b2a6a49bb4b44149927e00bd14b70a8bb8d9b89d4`.
Its changes correctly implement those conclusions, return every distinct
optimal block after the nonadaptive comparison batch, and add the direct
quadratic comparator and the verification limits. No substantive gap
was found in the amended argument. This final read also checked that the
stronger output statement is supported at the zero-gradient early stop,
for exact ties, and for the separate zero-integer-variable case.
