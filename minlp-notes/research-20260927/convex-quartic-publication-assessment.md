# Publication assessment of the convex quartic constructions

Date: 2026-09-28. Status: primary-source and significance audit with
[independent review](convex-quartic-publication-assessment-review.md);
publication priority is not established. The mathematical constructions have separate
proof reviews. This note assesses their scope, comparative strength, and
remaining literature risks. No author contact or publication was attempted.

The strongest current package is an explicit negative answer to the
quartic rational-point-witness question, followed by an effective
characterization of the algebraic numbers that can occur in such
singletons. The explicit example has the clearest connection to a
published open entry. The general realization is the more substantial
structural theorem. The Hessian Gram construction strengthens the latter
and makes it certifiable, but its matrix techniques have close precedents.
None of these results establishes decision hardness or a solver speedup.

## Claims and their relative strength

| Claim | Assessment | Qualification |
| --- | --- | --- |
| An integer, globally strongly convex quartic in two variables has minimum zero at a unique irrational point. | Strongest direct answer to a stated unresolved question; a credible short-paper result if priority survives further checking. | It changes the rational-point-witness entry, not the exact-decision complexity entry. |
| Every real algebraic number with exactly one real conjugate occurs in a rational strongly convex SOS quartic singleton, with a polynomial-time construction from its dense minimal polynomial. | Strongest structural result in the package. It gives an effective fixed-degree converse to the real-embedding obstruction. | The number of variables grows with the input degree; the obstruction itself is an elementary field argument. |
| The realization also has a polynomial-size positive definite rational Hessian Gram certificate. | Valuable strengthening that separates irrational feasibility from difficulty certifying convexity. | Interior Gram matrices, coefficient projection, and Schur-complement regularization are established tools. |
| Irrational minimizers, large algebraic degrees, or rational SOS quartics with a prescribed algebraic zero without convexity. | Insufficient standalone novelty claims. | Each already has elementary examples or strong prior results. |

The first claim is proved in
[the explicit construction](convex-quartic-irrational-zero.md). The second
and third are proved in
[the general construction](general-strongly-convex-quartic-singleton.md)
and [the rational Hessian certificate](sos-convex-quartic-realization.md).
Their reviews should remain attached to any consolidated presentation.
The phrase “publication-level” here is an assessment of the mathematical
contribution, not a prediction of acceptance or a certification of priority.

## The precise open entry answered

Slot, Steurer, and Wiedmer define their exact problem as deciding whether
a rational polynomial is nonpositive somewhere on a rational polyhedron.
Their compact witnesses are rational feasible points of polynomial bit
length. Table 1 separately lists the existence of such witnesses and the
complexity of exact decision. For globally convex quartics, both entries
are unknown. Appendix C gives a sextic irrational singleton and rules out
the corresponding univariate quartic example with rational minimum.
The latest arXiv landing page inspected on this date lists only the
5 November 2025 version 1.
[Primary paper, Table 1 and Appendix C](https://arxiv.org/html/2511.03440v1),
[version record](https://arxiv.org/abs/2511.03440).

There is also a STOC 2026 proceedings version, DOI
[10.1145/3798129.3800760](https://doi.org/10.1145/3798129.3800760).
The fresh audit found that record but could not retrieve its full text
from ACM or the institutional repository. Its current Table 1 wording
is therefore unverified. The
[latest-status audit](quartic-latest-status-prior.md) records those access
limits and the later citing papers actually inspected.

The repository's integer polynomial has

\[
 \{(x,y):F(x,y)\leq0\}
 =\{(\sqrt[3]2,\sqrt[3]4)\},
 \qquad \nabla^2F\succeq4124I.
\]

It therefore supplies a negative answer stronger than failure of a
polynomial bit bound: this nonempty feasible set contains no rational
point at all. It also works on the rational box \([1,2]^2\), with its
point in the box's interior. The exact-decision entry remains untouched.
The same instance has a short algebraic feasible-point description.

The safest current wording is “resolves the rational-point-witness
question recorded in Table 1 of the inspected version.” Calling it the
first resolution in the literature requires an additional priority
judgment. A current arXiv version record does not exclude proceedings,
author manuscripts, independent work, or results using other terminology.

### Minimal degree and dimension have a precise scope

For a single globally convex rational polynomial, degree four is the
lowest degree at which a nonempty nonpositive sublevel can lack a rational
point. An odd-degree polynomial of degree greater than one cannot be
globally convex. For a rational convex quadratic, either the sublevel
has interior and contains rational points, or its nonempty zero-level
minimum is attained on the rational affine system given by its gradient.
That system has a rational solution. The affine and constant cases are
immediate.

Two variables are also necessary at degree four. If the nonpositive
sublevel of a univariate convex quartic has positive length, it contains
a rational point. Otherwise it is a singleton \(\{a\}\), the minimum
is zero, and the irreducible polynomial \(p\) of \(a\) satisfies
\(p^2\mid F\). Hence \(\deg p\leq2\). A quadratic irreducible
polynomial with a real root has two real roots. Both would be zeros of
\(F\), contradicting the singleton. Thus \(a\) is rational.
This is the elementary mechanism behind the relevant univariate boundary.

These minimality statements concern one globally convex polynomial.
They do not apply to arbitrary polynomial descriptions of convex sets,
to convexity only on a restricted domain, or to several convex quadratic
constraints.

## Strong prior results and what remains different

**The same cubic point under domain-restricted convexity is old.**
Bienstock, Del Pia, and Hildebrand's Example 1 gives
\(h(x,y)=2x^3+y^3-6xy+4\) and the rational rectangle
\([1.259,1.26]\times[1.587,1.59]\), on which its nonpositive
sublevel is exactly \((\sqrt[3]2,\sqrt[3]4)\).
[Primary paper, Example 1](https://optimization-online.org/wp-content/uploads/2020/11/8105.pdf).
Moreover, direct differentiation gives
\(\nabla^2h=\left(\begin{smallmatrix}12x&-6\\-6&6y\end{smallmatrix}\right)\).
Its first leading minor is positive and its determinant
\(72xy-36\) is positive throughout that rectangle. Compactness gives
uniform strong convexity there. This last observation is our inference.
Thus the new distinction must be **global** strong convexity; irrational
exact feasibility for a function strongly convex on its feasible box is
already present in that example.

**SOS-convexity of the two-variable example is already an implication
of a known theorem.** Ahmadi and Parrilo's Theorems 5.1 and 5.6 prove that
every convex, nonhomogeneous bivariate quartic is SOS-convex. Their
Theorem 5.3 supplies the underlying biform result. This gives real
SOS-convexity of the explicit example once its convexity is proved; it
does not by itself provide the displayed rational certificate or its bit
bounds. The same automatic implication fails in higher dimensions.
[Primary paper](https://arxiv.org/pdf/1111.4587).

**Arithmetic interpolation is a direct construction ingredient.**
Krick, Mourrain, and Szanto construct rational SOS representations modulo
a univariate polynomial using root interpolation and rational rounding
with exact coefficient correction. The formal zero-target specialization
of their displayed Lagrange-pair identity supplies a real PSD Gram matrix
whose kernel is the evaluation vector at the sole real root. This is an
inference from their formula, not an application of their strictly
positive-target proposition. Their result does not state a globally
convex quartic realization.
[Primary paper, Section 2](https://arxiv.org/pdf/2112.00490).

This comparison suggests a simpler proof architecture. Approximate that
real Gram matrix rationally inside the exact space
\(v(T)^{\mathsf T}Bv(T)\equiv0\pmod p\). On the affine chart
\(v=(1,x)\), the quadratic part remains positive definite, its value at
the prescribed point remains exactly zero, and its gradient can be made
arbitrarily small. Those are precisely the inputs used by the quartic
convexification argument. This qualitative reduction does not require the
companion sandwich or the two-parameter affine pencil. The rational matrix
\(B\) need not be PSD; only its quadratic block remains positive
definite. For an irrational \(\alpha\) with irreducible minimal
polynomial of degree \(d\), a rational PSD matrix in this exact
vanishing space would satisfy \(Bv(\alpha)=0\), hence \(B=0\) by
power-basis independence. A shorter effective proof must integrate and
independently verify the quantitative approximation and bit bounds
sketched in the universal-realization audit before replacing the existing proof.

**There is also effective multivariate arithmetic prior.** Baldi, Krick,
and Mourrain's Theorem 2.1 gives rational weighted SOS representations
modulo radical zero-dimensional ideals for strictly positive targets.
Their later sections give degree and coefficient-height bounds and extend
to nonnegative targets under stated hypotheses. This generalizes the
univariate arithmetic machinery. These are identities modulo an ideal,
not a fixed-degree globally convex polynomial with prescribed zero set.
[Primary paper](https://arxiv.org/html/2410.04845v2).

**The Gram and regularization principles are established.** Ahmadi,
Chaudhry, and Zhang's Lemma 2 proves interior SOS-convexity of
\(\|x\|^2+\|x\|^{2k}\); Lemma 3 and Theorem 3 regularize suitable
Taylor polynomials with centered even norm powers. Their proof uses
positive definite Hessian Gram matrices and a Schur complement. These
are particularly close methodological precedents.
[Primary paper](https://arxiv.org/html/2311.06374v2).
The arithmetic issue is preserving an irrational zero with rational
coefficients: centering at that zero introduces algebraic coefficients,
while centering at a different rational point changes the gradient there.
The exact rational vanishing space addresses that issue.

Peyrl and Parrilo's rounding-and-projection method is direct prior for
turning a sufficiently interior numerical Gram matrix into an exact
rational certificate. The theorem under assessment adds a constructed
matrix and a polynomial precision bound; orthogonal coefficient
projection itself is not new.
[Primary paper, Section 3 and Proposition 8](https://www.mit.edu/~parrilo/pubs/files/PeyrlParrilo-ComputingSumOfSquaresDecompositionsWithRationalCoefficients.pdf).

An earlier degree-preserving result is Ahmadi and Hall's decomposition
of a polynomial of degree at most four as the difference of two
SOS-convex polynomials of degree at most four, with stronger
diagonal-dominance variants. Their interior
Hessian Gram construction is another close precedent. This preserves
the polynomial as a difference, rather than preserving a specified zero
as the minimum of one globally convex polynomial.
[Primary paper, Theorems 2--3 and Corollary 1](https://www.princeton.edu/~aaa/Public/Publications/dcdv12.pdf).

**Other quartic SOS regularization does not automatically preserve the
rational zero level.** Zhu and Cartis study when a sufficiently regularized
quartic, after subtraction of its attained minimum, is SOS. Their
stationary-point certificates and the subtraction can involve irrational
quantities. The inspected statements do not prescribe the minimizer's
field while retaining rational coefficients and minimum zero.
[Primary paper, version 2 of 2 April 2026](https://arxiv.org/html/2601.20418v2).

Further comparisons, including generic algebraic degree, convexification
by multiplication, and rational SOS descent, are recorded in
[the general prior audit](general-quartic-realization-prior.md) and
[the singleton field audit](singleton-field-characterization-prior.md).
They should be cited rather than presenting those ingredients as new.
The [fresh universal-realization audit](quartic-universal-publication-prior.md)
also compares exact moment extraction and records a quantitative version
of the proposed interpolation shortcut.

## The structural theorem's actual contribution

The necessary field condition is clean but elementary. A singleton of
finitely many rational convex polynomial sublevels is already isolated
by its active constraints. Every real embedding of its coordinate field
preserves the active equalities and hence fixes the point. The full
coordinate field has one real embedding. Its odd degree then ensures
that every real embedding of any coordinate subfield extends to a real
embedding of the full field. Thus every coordinate has exactly one real
conjugate. The [independent field review](singleton-field-characterization-prior-review.md)
checks the sometimes omitted subfield step.

The substantial converse realizes every permitted coordinate at the
lowest possible degree in the irrational singleton case, with global strong convexity, rational
SOS structure, prescribed rational minimum, and effective rational
convexity certificates. This is a stronger organizing theorem than an
isolated counterexample. The credible novelty target is this combination
of arithmetic prescription, exact zero preservation, fixed degree, and
polynomial bit bounds. Neither generic high algebraic degree nor the
field obstruction alone captures that contribution.

An elementary baseline must remain visible: quadratic lifting of the
equations \(x_j=x_1^j\) and \(p(x_1)=0\), followed by summing their
squares, already gives a polynomial-size rational SOS quartic with the
desired unique zero when \(p\) has one real root. It is generally
nonconvex. Also, a strongly convex rational univariate quartic can easily
have an irrational minimizer if its minimum need not be rational. These
examples explain why all of the theorem's qualifications matter.

For \(d>1\), the construction uses \(d-1\) variables for input degree
\(d\); rational coordinates are handled separately in one variable. It does not
claim an optimal dimension or matrix size, nor polynomial output in a
sparse encoding that might encode \(d\) in logarithmically many bits.
Dense input and the stated coefficient model are essential parts of the
algorithmic theorem.

## Significance for optimization and its limits

The proved solver consequence is a boundary on exact representations.
A method for exact convex polynomial feasibility cannot always finish by
returning a rational feasible point, even with integer input, a compact
rational box, global strong convexity, and rational certificates of
convexity and nonnegativity. Exact solvers therefore need a richer
representation or a different certificate on this class. The explicit
example is a useful small regression instance for that requirement.

The result does not rule out polynomial-size algebraic, symbolic, dual,
or other certificates. The constructed family itself comes with a short
algebraic description inherited from its input polynomial. A rational
SOS certificate can prove the lower bound zero without supplying a
rational minimizer. No conclusion about NP membership, NP-hardness,
decision lower bounds, or impossibility of polynomial-time exact
optimization follows from the absence of rational points alone.

Approximate optimization is compatible with every result here. Strong
curvature controls distance from an approximate objective value, and
rational points can approximate the irrational minimizer arbitrarily
well. The constraint \(F\leq0\) itself has no strictly feasible point
and has zero gradient at its feasible point; strong curvature and an
interior Hessian Gram certificate do not remove that boundary degeneracy.
Subtracting a positive constant from \(F\) gives a sublevel with
interior, whereas adding one makes the sublevel empty. Also, normalizing
the strong-convexity constant does not bound the Hessian above or give
favorable numerical conditioning.

Obtaining useful exact-recovery algorithms would require quantitative
degree, height, and separation bounds together with effective recovery
and verification procedures. The realization theorem identifies the
arithmetic range those procedures must accommodate; it does not supply
a general exact solver. Practical MINLP benefits remain plausible research
directions, rather than demonstrated computational improvements.

## Publication recommendation and unresolved prior risks

A focused manuscript should lead with the explicit globally convex
quartic and its precise rational-witness consequence. It can then present
the effective one-real-conjugate characterization as the main general
theorem, with rational Hessian certificates as a strengthening. The
small example should remain independently checkable even if the general
construction is reorganized. The case for a substantial paper rests more
on that general theorem than on enlarging the numerical coefficients or
adding another equivalent certificate to the example.

The remaining priority questions are specific:

1. Could a later manuscript or proceedings version already resolve the
   quartic rational-point-witness entry? The current version check and
   citation searches are evidence with limited coverage.
2. Does arithmetic real algebraic geometry already state an equivalent
   rational strongly convex quartic realization under terminology such
   as unique critical points, prescribed minimizers, or convex polynomial
   defining functions? The inspected neighboring results do not settle
   that question.
3. How much of the effective realization follows directly from the
   strongest quantitative interpolation theorem plus a standard
   regularization lemma? The proposed direct Gram route sharpens this
   issue and should be worked through before making a methodological
   novelty claim.
4. Are rational Hessian certificates already guaranteed for a broader
   class containing this construction with equally good bit bounds?
   Qualitative SOS-convexity and generic interior rounding alone should
   not be mistaken for a new certificate theorem.

Failed searches do not settle these questions. Conversely, a theorem
can be publishable as a new application of established tools; its
presentation should identify exactly which arithmetic conclusion was
missing, rather than inflate the novelty of the tools.

## Verification scope

This assessment re-read the construction statements, their proof reviews,
and the primary statements identified above. It independently checked the
minimality arguments and the restricted-domain Hessian comparison.
Fresh parallel audits cover the latest-paper search and the universal
realization's prior art. They are separate from the construction reviews.
The independent assessment review rechecked the incorporated scope and
source qualifications and found no remaining substantive error. A
separate [universal-prior review](quartic-universal-publication-prior-review.md)
checks that audit's claims; neither review certifies the new quantitative
shortcut as a replacement proof.

The [Lean verification record](convex-quartic-lean-verification.md) now
reports formal zero-set and irrationality proofs, actual directional
second derivatives bounded below by \(4096\|v\|^2\), and global
`ConvexOn`. That record distinguishes the formal constant from the
hand-proved constant \(4124\). This assessment did not rerun Lean and
does not independently certify its source fingerprint. Formal verification
supports correctness of the checked statements; it establishes neither
publication priority nor practical significance.

An inline `python - <<'PY'` command independently differentiated the
older cubic and checked its Hessian, determinant, positive rational lower
determinant bound on the stated rectangle, and indefinite Hessian at the
origin. The same command checked this file's final newline, whitespace,
control characters, math delimiters, and relative links. It passed.
The document checks were repeated after the review corrections.
`git diff --check -- research-20260927/convex-quartic-publication-assessment.md`
returned no diagnostics; the direct whitespace check also covers the new
untracked file. No project-wide verification or CI inspection was used.
