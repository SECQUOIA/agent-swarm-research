# Fresh review of the convex rational SOS quartic degree bound

Date: 2026-09-28. Status: Sections 1–5 of the
[degree-bound note](quartic-zero-degree-adversarial.md) pass this
independent proof audit. The reviewer did not contribute to the
intersection or Cayley–Bacharach argument. Novelty is not assessed here.

The reviewed conclusion is the following. Suppose
\(F=\sum_jq_j^2\), with rational \(q_j\) of degree at most two,
is globally convex, has a unique real zero \(p\), and has positive
definite Hessian at that zero. Then, for \(n\geq4\),

\[
 [\mathbb Q(p):\mathbb Q]\leq2^n-5.
\]

The four-variable upper bound is therefore eleven. Rationality of the
individual quadratic summands is an explicit assumption. The result
does not follow merely from rational SOS-convexity; the separate
[descent counterexample](rational-sos-convex-descent.md) shows why that
distinction matters.

## Initial degree and reduction arguments

At the zero, the Hessian identity
\(\nabla^2F(p)=2J(p)^{\mathsf T}J(p)\) gives full Jacobian rank.
Selecting an invertible square minor makes \(p\) an isolated simple
complex zero of rational quadratic equations. Its coordinates are
therefore algebraic, and every conjugate point is simple for the same
selected equations. The isolated-point Bézout bound applies even if
other components exist. Every real field embedding gives the same
unique real zero; because the coordinates generate the field, the
embedding is the identity. Thus the joint degree is odd and at most
\(2^n-1\).

The quartic-flat reduction is valid. The zero set of the convex even
leading form is exactly its translation-invariance space. The limiting
convexity argument in Section 2 proves invariance, and coefficient
comparison makes this a rational linear subspace. Along such a
direction, the Hessian of the cubic part enters the full Hessian as a
linear pencil with an unrestricted real parameter. Positivity for both
signs forces that coefficient to vanish. Homogeneity then removes the
cubic dependence on the flat variable itself.

The remaining dependence on flat variables is quadratic with rational
coefficients. Its positive definite quadratic block follows from the
Hessian at \(p\), so the fiber minimizer is rational affine. Restriction
to this graph preserves rational SOS, convexity, unique zero, and the
joint coordinate field. The Schur complement preserves positive
definiteness at the zero. On the complementary variables, the quartic
leading form is positive definite. If every variable is removed, the
original zero is rational. These facts justify reducing to the case
with no real projective zeros at infinity.

## Positive-dimensional intersections

The weighted intersection count does not silently assume proper
intersection. A component of dimension \(r\) and degree \(e\) receives
weight \(2^r e\). A containing quadric retains it. A noncontaining
quadric cuts it properly, decreasing dimension by one, and the sum of
the reduced component degrees is at most twice its degree. Thus total
weight never increases. Multiplicities need not be retained to obtain
this upper bound, and retaining duplicate components only overcounts.
The union of the multiset still equals the required intersection.

Consequently simple isolated points each use at least one unit of the
initial weight \(2^n\), while any positive-dimensional component uses
at least two. This proves the first excess-component estimate used to
exclude degree \(2^n-1\).

For the length-three case, let \(W\) be the common projective zero set
of all original quadrics. After the flat reduction its only real point
is \(p\), which is isolated over the complex numbers. The incidence
argument for generic combinations is sound: outside \(W\), each point
imposes \(n\) independent linear conditions on the combination matrix.
The total incidence dimension equals that of the matrix parameter
space, so a generic fiber has dimension at most zero. Thus all positive
components of the generic intersection lie in \(W\). The nonzero
Jacobian conditions at finitely many conjugates are compatible open
conditions. They and the incidence condition are defined over the
rationals; rational matrices are Zariski dense, so a rational choice
exists.

The final component multiset may be chosen invariant under complex
conjugation: every step cuts by a rational equation and retains all
irreducible components with their repetitions. A total positive-component
weight below four could only be one degree-one projective curve.
Such a curve is a line. Conjugation invariance would define it over
the reals, and a real projective line has real points. This contradicts
its containment in the positive-dimensional part of \(W\). Hence a
positive component costs at least four. Together with \(2^n-3\)
simple conjugate points this would exceed the total weight budget.

This proves that the chosen projective intersection is finite in the
case under contradiction. Its \(n\) quadrics form a complete
intersection of total length \(2^n\). Lower-dimensional embedded or
nonreduced residual structure is allowed; it is not discarded by this
conclusion.

## The residual length-three scheme

Let \(\Gamma\) be the reduced conjugate orbit. Each of its local
intersection rings has length one, by the Jacobian condition. Thus
its residual scheme \(R\) is disjoint from it and has length three.
It is defined over the rationals. Nothing here assumes that \(R\)
is reduced.

The proof that \(H_R(1)=3\) handles nonreduced schemes. If the rank
of restriction of linear forms were at most two, the linear ideal of
\(R\) would place it scheme-theoretically in a projective subspace
of dimension at most one. A length-three scheme cannot be a closed
subscheme of a reduced projective point. It would therefore lie on a
line. A nonzero section of \(\mathcal O_{\mathbb P^1}(2)\) has a
zero divisor of length two, counting multiplicity; it cannot vanish
on \(R\). Every defining quadric would consequently contain the
whole line, contradicting finiteness of the complete intersection.

A linear form avoiding the finite support of \(R\) is a unit after
local trivialization. Multiplication by it therefore transports the
surjective restriction map in degree one to every larger degree. This
justifies \(H_R(t)=3\) for all \(t\geq1\), including schemes with
nilpotents.

## Cayley–Bacharach and the real-point contradiction

I independently opened the primary EGH PDF and inspected printed page
195 as an image. Its modern Cayley–Bacharach statement applies to
mutually residual closed subschemes in a complete intersection, without
a reducedness hypothesis. Its shift is \(m=\sum_i d_i-n-1\).
For quadrics, \(m=n-1\); testing degree two gives the required
degree \(n-3\) on the residual scheme. The classical reduced-point
statement on page 196 also gives the earlier length-one step.
[Primary text, pp. 195–196](https://eisenbud.github.io/papers/pdfs/1993-002.pdf).

In the present notation the identity is

\[
 h^0(\mathcal I_\Gamma(2))-h^0(\mathcal I_Z(2))
   =h^1(\mathcal I_R(n-3)).
\]

Since \(n\geq4\), the Hilbert-function calculation makes the right
side zero. Equivalently, use the restriction exact sequence and
\(H^1(\mathbb P^n,\mathcal O(n-3))=0\). Every original quadric,
which vanishes on \(\Gamma\), must then vanish on \(R\).

A finite real scheme of odd total length has a real geometric point:
nonreal conjugate points contribute equal local lengths in pairs.
The resulting real point of \(R\) is disjoint from the conjugate
orbit. It cannot be at infinity because the leading quartic form is
positive definite, and it cannot be affine because the original
polynomial has only the zero \(p\). This contradiction excludes
degree \(2^n-3\). Combining it with the earlier exclusion of
\(2^n-1\) and oddness proves the asserted bound.

## Corrections, scope, and checks

No substantive proof correction was needed. One bibliographic correction
was reported to the author: the linked 1993 EGH paper is titled
*Higher Castelnuovo theory*, rather than the title initially given in
Section 4. This does not affect the theorem or page references.

This audit does not use EGH's conjectural higher-degree generalizations,
nor does it extrapolate their low-dimensional results. It verifies the
specific residual length-three application of the stated theorem.
The sharpness examples are outside this audit and have their own
independent reviews. No claim about higher-dimensional sharpness,
automatic rational SOS descent, or publication priority is established.

The source page was rendered locally with

```text
pdftoppm -f 9 -singlefile -scale-to 1900 -png research-20260927/quartic-degree-sources/eisenbud-green-harris-1993.pdf /tmp/eg-harris-review-p195
```

The proof was checked directly; no numerical tests were used as evidence
for the universal scheme statements. Targeted Markdown checks covered
local links, balanced displayed-math delimiters, and trailing whitespace.
No project-wide checks or CI inspection were performed.
