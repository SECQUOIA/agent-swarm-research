# Least SOS coefficient fields: prior results and the precise comparison

Date: 2026-09-28. Status: targeted primary-source comparison complete;
publication priority remains unestablished. This is a literature and
significance audit, not a substitute for either construction's fresh
proof review.

The parent investigator independently read Scheiderer's construction
and Corollary 2.11, checked the degree-at-most-24 deduction below, and
reviewed the narrow significance statement. That check does not amount
to an independent reading of every other primary source in this note.

The [prime family](arbitrary-prime-strict-sos-field.md) prescribes
\(\mathbb Q(2^{1/p})\), for every prime \(p\geq5\), as the
smallest real field admitting either an SOS or a positive semidefinite
polynomial Gram matrix. Its integer quartics have a positive definite
integer Hessian Gram and coefficients of polynomial magnitude in
\(p\). The [tower family](exponential-least-sos-field.md) gives the
stronger quantitative conclusion \(\mathbb Q(2^{1/5^k})\) in
\(3k\) variables, with polynomial input and Hessian-certificate bit
length. The tower proof has now passed its fresh independent review.
Its [individual-coefficient strengthening](exponential-sos-individual-coefficient-degree.md)
also forces one algebraic certificate entry to have degree at least
\(5^k\), even when different entries use separate defining fields.

The strongest prospective addition is not irrationality of SDP
solutions, failure of rational SOS descent, or even an unbounded field
degree somewhere in semidefinite optimization. It is a uniform
arithmetic requirement on **every feasible polynomial Gram matrix**
of an explicitly constructed globally strongly SOS-convex rational
quartic, together with a matching field of construction.

## Scheiderer's exclusion of any prescribed field

[Scheiderer, *Sums of squares of polynomials with rational coefficients*,
JEMS 18 (2016), 1495–1513](https://ems.press/content/serial-article-files/32129),
Corollary 2.11, proves the following stronger predecessor than merely
failure over \(\mathbb Q\): any prescribed real number field can
be excluded as an SOS field by a rational real-SOS ternary quartic
form. The theorem covers larger dimensions and even degrees too,
without asserting convexity.

Excluding one field does not imply unbounded necessary field degree.
Here is our deduction from the paper's quartic norm construction.

Let \(L\) be the splitting field of the defining quartic extension.
Then \([L:\mathbb Q]\leq24\). The four conjugate linear factors
can be paired by complex conjugation. Selecting one factor from each
pair gives a quadratic \(g\) with coefficients in \(L\) and
\(f=g\overline g\). Hence

\[
 f=\left(\frac{g+\overline g}{2}\right)^2+
   \left(\frac{g-\overline g}{2i}\right)^2.
\]

The square factors lie in \(L(i)\cap\mathbb R\), of degree
at most 24 because complex conjugation has order two on \(L(i)\).
Thus these quartic examples have some bounded-degree SOS field.
This does not bound the necessary field degree for arbitrary quartics
with a growing number of variables.

## Cubic descent failures and strictly positive forms

[Laplagne, *Sum of squares decomposition of positive polynomials with
rational coefficients*](https://arxiv.org/pdf/2312.16801), Section 3.1
and Proposition 3.1, displays a rational quaternary quartic form that
is SOS over \(\mathbb Q(\sqrt[3]2)\) but not over
\(\mathbb Q\), credited to Capco, Laplagne, and Scheiderer.
Theorem 3.4 gives a strictly positive rational quartic form in eight
variables with the same failure of rational descent and the same
cubic field available for an SOS. Its construction joins that
arithmetic block with a boundary SOS block and uses a dual functional.
It does not claim global convexity, a positive definite Hessian Gram,
an exact least coefficient field, or a growing necessary field degree.
The earlier [three-variable comparison](three-variable-rational-sos-descent-prior.md)
records the 2019 announcement and the geometric obstruction to
converting the displayed form to the present strict convex class by
a projective change of chart.

Strict positivity of a form is not the same as a positive definite
polynomial Gram matrix. Nor is a positive definite **Hessian** Gram
the same as a positive definite Gram for the polynomial. The present
quartics have a zero and therefore singular polynomial Grams, despite
their strictly positive Hessian certificates.

## Gram fields and SOS fields need separate arguments

[Chua–Plaumann–Sinn–Vinzant, *Gram Spectrahedra*, Lemma 1.6 and
Remark 1.7](https://arxiv.org/pdf/1608.00234), proves equivalence
between a rational PSD Gram and a rational SOS, and explicitly warns
that the corresponding assertion over an arbitrary ordered field is
false. A matrix positive in one ordering need not factor as squares
over that field. The paper also discusses algebraic degrees of linear
optimization on Gram spectrahedra; these concern selected optimizing
points and their ranks, rather than the least field of any feasible
Gram. Proposition 4.3, for example, addresses generic binary sextics.

The constructions here must therefore prove both parts of their field
claim. The necessity argument uses the kernel of an arbitrary PSD
Gram at the real zero and coefficient comparison over a field
extension; it does not factor that Gram over its coefficient field.
Sufficiency uses a rational Hessian SOS and an explicit Taylor
integration identity at the minimizer. It supplies unweighted squares
over the specified field directly. This avoids an unjustified appeal
to general SOS descent over an ordered field.

## High algebraic degree in SDP is established prior theory

[Nie–Ranestad–Sturmfels, *The Algebraic Degree of Semidefinite
Programming*](https://arxiv.org/pdf/math/0611562), studies coordinates
of optimal solutions of generic rational SDPs. The degree is computed
through critical points of a linear functional on a fixed-rank
determinantal locus. Its genericity, fixed-rank, and optimization
hypotheses matter. A high-degree selected optimum need not imply that
all feasible points of that SDP have high degree, and it does not
alone identify a family of polynomial Grams of strongly SOS-convex
quartics.

There is nonetheless a simple way to make an optimal-point obstruction
into an all-feasible-point obstruction for **general** spectrahedra.
This is our deduction, included to avoid overstating the distinction.
Take a rational primal-dual SDP pair for which optima are attained and
there is zero duality gap. Impose primal feasibility, dual feasibility,
and equality of the two objective values. The last condition is a
rational linear equation in the primal and dual variables. The joint
set is a rational spectrahedron, and every feasible pair is optimal.
Whenever the original optimum forces an arithmetic field, the joint
feasible set inherits that requirement without inserting an irrational
objective value into its description. This construction provides no
identification with a full polynomial Gram spectrahedron, let alone
one belonging to a strictly SOS-convex quartic.

There is an even simpler warning about common fields. Independent
rational singleton pencils for positive square roots of distinct
primes can be put in block diagonal form. Every feasible tuple then
generates a multiquadratic field of exponential degree, although each
individual coordinate has degree two. A lower bound for a **joint**
coefficient field must not be presented as a lower bound for one
coefficient without an additional proof. The tower paper supplies
that separate proof: an order-\(5^k\) automorphism of the radical's
normal closure cannot lift to a group embedded in a product of
symmetric groups of degrees all below \(5^k\). This audit also
read and reconstructed that argument; it is not inferred merely from
the large degree of the common field.

## Exact LMI algorithms and their examples

[Henrion–Naldi–Safey El Din, *SPECTRA — a Maple library for solving
linear matrix inequalities in exact arithmetic*, Sections
4.1–4.5](https://perso.lip6.fr/Mohab.Safey/Articles/HeNaSa17.pdf),
includes a rational pencil whose spectrahedron is the singleton
\(\{\sqrt2\}\), sampled points of degrees 10 and 12, and a
cubic Gram point for a Scheiderer rational-SOS counterexample.
The degree-12 example is a boundary sample of a two-dimensional
spectrahedron; the displayed matrix at the origin is positive
definite. Thus that sample's degree is not a necessary degree for
arbitrary feasible points. These are exact-algebraic computation
results and examples, not a strict SOS-convex least-field theorem.

## What would be new if the remaining prior search finds no equivalent result

The prime construction contributes an explicit arithmetic family with
small integer data and a direct integer Hessian Gram. The reviewed
tower construction gives the more consequential separation: rational
minimum and a short
strict rational convexity certificate coexist with a prescribed
exponential-degree field in every exact SOS and every PSD polynomial
Gram. Neither conclusion follows directly from the inspected descent,
generic SDP, or low-rank Gram results.

This is a claim about arithmetic representations of one standard
certificate system. It is not a decision-hardness theorem. It does not
exclude efficient numerical optimization, rational certificates with
denominators, or short radical/circuit descriptions of the required
field. Exponential growth is in the tower length or number of
variables; polynomial input size gives a superpolynomial field-degree
requirement without an asserted exponential bound in the full dense
input bit length. The separately proved necessity of a large-degree
individual coefficient gives a dense minimal-polynomial output lower
bound even when entries use separate algebraic representations. It
still gives no lower bound for sparse or circuit descriptions.

## Search scope and unresolved prior questions

The primary sources above were opened and the relevant statements
read on 2026-09-28. Searches included combinations of `Gram
spectrahedra field`, `sum of squares coefficient field minimal degree`,
`SOS-convex rational field`, `spectrahedron feasible point exponential
algebraic degree`, and `sum of squares field extension degree`.
The search also surfaced results about the **number of squares**,
Pythagoras numbers, and rational-function denominator degrees; these
do not answer the coefficient-field question.

Remaining priority holes are substantial: a theorem may characterize
fields of all Gram points under different terminology; a realization
theorem for rational spectrahedra as polynomial Gram faces may transfer
an older arithmetic example; and an unpublished or later version of
the Capco–Laplagne–Scheiderer work may contain stronger field claims.
Even a general Gram realization would need to preserve a rational
positive definite Hessian Gram to reproduce the present conjunction.
No failed search is treated as proof of novelty. No publication,
author contact, project-wide verification, or CI inspection was made.

Targeted document checks used Python to verify local Markdown links,
control characters, and paired display/inline math delimiters; they
passed. `git diff --check -- research-20260927/exponential-sos-field-prior.md
research-20260927/arbitrary-prime-strict-sos-field.md` also passed.
