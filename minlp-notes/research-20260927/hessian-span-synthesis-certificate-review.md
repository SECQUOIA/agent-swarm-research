# Scope review of the common-field and certificate synthesis

Date: 2026-09-27. This is a fresh review of the updated
[main-results synthesis](hessian-span-main-results.md), covering its
sharper arithmetic precision, constructive common-field outputs, finite
continuous certificates, rational infeasibility certificates, and succinct
unboundedness certificates. It compares those statements with the saved
dependency notes and their completed reviews. It does not repeat the
general proof audits or establish publication priority.

The final saved synthesis has no unresolved scope error from this review.
One description of the curved minimizer sections required correction:
the aggregate is minimized over the current polyhedron, and need not be
globally minimized there. The author corrected that description and
independently rechecked the example below. I reread the corrected text.

## 1. Sharper precision and constructed algebraic outputs

The [direct number-field precision argument](algebraic-coefficient-span-precision.md)
and its [independent review](algebraic-coefficient-span-review.md) support
the improved boxed bound

\[
 \log_2\max(1,C)\le N^{O(h+1)}
\]

for the Hölder constant, with the unchanged exponent \(2^{-h}\).
The field degree and absolute logarithmic coefficient height enter the
terminal-margin estimate linearly. Composing those estimates with the
existing common-field facial argument therefore does not require an
exponent quadratic in \(h\).

The synthesis correctly updates both the principal-result table and the
distance-and-penalty discussion. Its sufficient rational-quadratic penalty
coefficient now has \(N^{O(h+1)}\) bits. This remains a fully boxed,
nonempty mixed-integer statement; slice convexity suffices, and the
objective can be indefinite because only its whole-domain Lipschitz bound
is used. The remaining \(N^{O((h+1)^2)}\) statement concerns a
conservative composition of the MILP construction with the continuous
radius bound. It is not a stale claim about the Hölder constant.

The [common-field construction](constructive-common-field-recovery.md)
and its [review](constructive-common-field-review.md) now justify the
stronger exact-output contract: one isolated primitive real algebraic
generator and rational coordinate polynomials, with polynomial overhead
in the supplied joint-degree and coefficient-height bounds. Its input
includes certified approximations to the same selected tuple. Separate
coordinate polynomials without selected embeddings would not suffice.

The synthesis retains the sharper field-degree bound

\[
 D(n,h)=\max_{0\le s\le\min(h,n)}2^s\binom ns
\]

and \(N^{O(h+1)}\) representation coefficient bits. It does not infer
the joint degree by multiplying individual coordinate degrees. Its
description of norm interpolation includes the necessary correction when
a sampled linear combination has smaller degree: its minimal polynomial
must be raised to the field-degree quotient. Constructing this common
field does not by itself improve the composed optimization algorithm's
running-time exponent; the synthesis retains the established
\(N^{\operatorname{poly}(h+1)}\) continuous recovery bound.

Substitution in native affine and quadratic rows gives univariate sign
queries of polynomial size. The synthesis properly distinguishes checking
primal feasibility from proving global optimality. Its verifier discussion
also does not trust an unverified label that the defining polynomial is
minimal. Exact root isolation and univariate sign determination handle
the supplied representation independently.

## 2. Finite continuous optimality certificates

The [certificate theorem](algebraic-primal-dual-certificates.md) and
[proof review](algebraic-certificate-proof-review.md) establish existence,
encoding size, and polynomial verification of an optimality certificate.
They do not establish an end-to-end polynomial algorithm for extracting
every exposing multiplier. The synthesis states this distinction in its
certificate table and in its open questions. Constructing the primal
common-field point does not close that remaining construction gap.

At most \(h\) curved sections precede a final KKT identity. Every
coefficient lies in the field of the canonical primal optimizer, so the
field degree remains at most \(D(n,h)\), and total certificate length
is \(N^{O(h+1)}\). This does not mean every aggregate uses only
\(h\) original rows. The underlying theorem allows at most \(n+1\)
positive native and polyhedral multipliers per exposing record and at
most \(n\) in the final record. The synthesis makes no stronger support
claim.

The original synthesis wording described the section as the aggregate's
affine minimizer set. That wording could incorrectly suggest an
unconstrained global minimum. Consider

\[
 P=\{x:x\ge0\},\qquad q(x)=x^2+x\le0.
\]

The feasible set is \(\{0\}\), and the exposing aggregate \(q\)
has minimum zero on \(P\). Its global minimum is instead
\(-1/4\) at \(-1/2\). The certificate uses the nonnegative
quadratic and supporting-linear terms on the current polyhedron, then
imposes affine equations making both vanish. The corrected synthesis
states exactly that construction. These sections preserve all original
feasible points; they need not be faces of the polyhedron.

The certificate proves feasibility and global continuous optimality of the
supplied point. Its sound verifier need not certify the point's
minimum-norm property. Most importantly, applying the certificate to a
fixed integer assignment proves optimality only in that continuous fiber.
The synthesis explicitly excludes a certificate of global finite
mixed-integer optimality from this result.

## 3. Rational infeasibility certificates

The [rational refinement](rational-infeasibility-certificates.md) and
[independent review](rational-infeasibility-review.md) justify the
synthesis's displayed identity

\[
 \sum_i w_iq_i(x)
 =\gamma+\tfrac12(x-c)^TH(x-c),\qquad
 w_i\ge0,\quad\sum_iw_i=1,\quad\gamma>0.
\]

All affine inequalities, and both sides of each equality, join the row
list. The weights, center, and margin are rational; at most \(n+1\)
weights are positive. Their total binary length is
\(N^{O(h+1)}\). Here the problem is continuous, so \(h\) counts
the full native Hessian matrices. Verification requires rational
arithmetic and the PSD property, not algebraic recovery or an optimizer.

The proof preserves exact kernel equations when rounding the positive
weights. Merely preserving their positivity and normalization would not
preserve a finite global minimum. The synthesis records this essential
qualification without presenting the existence proof as a full
certificate-extraction algorithm. Polynomial conversion is conditional
on receiving the initial controlled common-field positive aggregate.

The repeated-squaring example gives \(\Omega(2^h)\) bits in the
rational weights of every positive aggregate in this explicit format,
even without normalization. The synthesis correctly limits this to the
certificate representation. It implies no lower bound for arbitrary
proof systems, decision running time, or a complexity-class separation.
Likewise, refuting continuous feasibility cannot refute a mixed-integer
system whose continuous relaxation is feasible. A fixed-fiber application
refutes that fiber only.

## 4. Succinct unboundedness certificates

The [escape theorem](succinct-unboundedness-curves.md) and its
[integer-increment review](all-integer-escape-review.md) have two distinct
construction scopes, both preserved in the synthesis.

For rational jointly convex quadratic data whose continuous objective is
unbounded below, a supplied rational radius \(R\ge1\) gives a
polynomial-time construction of one integer-coefficient increment circuit.
Its cost and size are polynomial in \(N+\operatorname{bits}(R)\),
without fixed dimension or Hessian span. The same circuit works for every
continuously feasible anchor in the radius box. It has zero constant term,
preserves feasibility for real \(T\ge1\), and decreases the objective
by exactly \(\gamma T\), with \(\gamma>0\). Integrality of
designated coordinates is preserved at integer parameter values. This
does not assert feasibility throughout \(0<T<1\), or that the
integer coordinates remain numerically unchanged. The latter possible
wording ambiguity was removed from the table during review.

The complete mixed-integer certificate additionally needs an exactly
feasible anchor. Constructing and checking that anchor in polynomial size
uses fixed integer dimension \(k\) and fixed continuous-block Hessian
span \(h\). The objective remains jointly convex but is excluded from
this anchor parameter. The continuous anchor can be irrational and is
encoded in one real number field. Thus unrestricted increment construction
does not imply unrestricted polynomial-time mixed-integer feasibility.

Intermediate coordinate projections preserve continuous attainable values;
they need not preserve integrality of projected anchors. Integral
increments in the original coordinates supply the final integrality
conclusion. The synthesis's certificate statement does not claim the
stronger intermediate property.

The circuit can represent polynomials of exponential degree. Its verifier
checks the prescribed local projection, domination, and assembly rules,
without expanding the curve or solving general arithmetic-circuit identity
testing. The synthesis retains that distinction, and does not promise a
decreasing straight ray or a rational constant anchor.

## 5. Contribution restraint and verification record

The synthesis attributes primitive-element and rational-univariate
representation mechanisms to established methods. It treats the
qualitative Hölder exponent as a structural consequence of existing conic
theory, distinguishes the arithmetic refinement, and attributes positive
aggregate alternatives and extended duality to their predecessors.
Obuchowska's older boundedness classification and continuous/mixed-integer
unboundedness equivalence are explicitly credited. The candidate addition
there is the integer-increment circuit and its local verification format,
not a new boundedness classification. No priority claim is inferred from
the literature search.

The pending nonconvex-NP and fixed-parameter output-lower-bound directions
are absent from the synthesis. Its fixed-parameter-tractability question
remains open rather than being answered by a certificate-format bound.

I read the complete saved synthesis, the five principal new dependency
notes, and their relevant proof reviews. A separately delegated reviewer
read the rational-infeasibility and unboundedness notes with their reviews
and prior audits, and independently confirmed the same construction and
parameter distinctions. The aggregate-minimum counterexample above was
checked directly by completing the square, then independently rechecked
by the synthesis author. The corrected final Section 7 was reread.

An inline `python` command checked only this new review for local Markdown
link existence, paired inline and display math delimiters, control
characters, trailing whitespace, and a final newline. Those checks passed.
They establish document consistency, not the general theorems. No
mathematical test was rerun, and no numerical experiment, Lean
formalization, project-wide verification, or CI inspection was performed.
