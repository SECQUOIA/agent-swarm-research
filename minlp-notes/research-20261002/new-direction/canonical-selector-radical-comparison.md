# Canonical point evaluation contains radical-sum comparison

Date: 2026-10-02. Status: an independently reviewed direct reduction
separating minimum-norm selection from the selection of any optimizer.
This is an arithmetic comparison implication, not an NP-hardness result
or an impossibility claim. No external search or priority claim is made.

For a rational polynomial of degree four, convex on a bounded rational
box, producing a rational point within Euclidean distance \(1/4\) of
the minimum-norm optimizer can decide Square Root Sum. The construction
has a tree decomposition with largest bag size three and bounded numerical
coefficients. Yet producing a point near some optimizer in the same family
has a direct polynomial-time method.

## 1. The established active-bound comparison construction

Start from binary-encoded positive integers \(a_1,\ldots,a_n\) and an
integer \(B\), with decision predicate

\[
                         \sum_i\sqrt{a_i}\le B.
 \tag{1}
\]

Handle the elementary out-of-range cases as in the reviewed
[active-bound reduction](convex-active-set-radical-comparison.md). That
construction produces, in polynomial time, a rational cubic \(H(w)\) on
a rational box \(W\), with a distinguished coordinate \(t\in[0,1]\).
It has these proved properties:

\[
 \nabla^2H(w)\succeq I/16\quad(w\in W),
 \qquad w^*=\operatorname*{argmin}_{w\in W}H(w)
                              \text{ is unique},
 \tag{2}
\]

and

\[
 t^*=0\quad\Longleftrightarrow\quad\sum_i\sqrt{a_i}\le B,
 \qquad\text{otherwise }0<t^*<1.
 \tag{3}
\]

The box intervals lie in \([0,2]\), apart from their positive lower
endpoints where needed; they are not all the unit interval. Coefficient
magnitudes and box widths have absolute bounds, and coefficient bit
lengths are polynomial in the source input. A supplied tree decomposition
has largest bag size three. The previous note proves (2)--(3), including
the equality case in (1), and records independent actual-file review.

## 2. A convex quartic turns the comparison into a visible selector jump

Append \(y\in[0,1]\), put \(\varepsilon=1/192\), and define

\[
             F(w,y)=H(w)+\varepsilon t^2(y-1)^2.
 \tag{4}
\]

This is a rational polynomial of degree at most four with polynomial
encoding length. Its only new factor has scope \(\{t,y\}\). Attaching
that bag to any old bag containing \(t\) preserves the decomposition's
largest bag size three.

The objective is jointly convex on \(W\times[0,1]\). To verify this
without a division by \(t\), write \(u=1-y\), and let \((p,q)\) be a
Hessian direction, with \(p_t\) the distinguished component of \(p\).
Then

\[
\begin{split}
 (p,q)^T\nabla^2F(w,y)(p,q)
   &=p^T\bigl(\nabla^2H(w)-6\varepsilon u^2 e_te_t^T\bigr)p
                         +2\varepsilon(tq-2up_t)^2\\
   &\ge\tfrac1{32}\|p\|^2\ge0.
\end{split}
 \tag{5}
\]

Here \(u^2\le1\), \(6\varepsilon=1/32\), and (2) supplies the other
\(1/16\). The certificate remains valid when \(t=0\).

Since \(F(w,y)\ge H(w)\ge H(w^*)\), and \(y=1\) attains equality
at \(w=w^*\), the entire optimal set is exactly

\[
 S=\begin{cases}
       \{w^*\}\times[0,1],&t^*=0,\\
       \{(w^*,1)\},&t^*>0.
    \end{cases}
 \tag{6}
\]

Thus the affine-section geometry is particularly simple in both cases.
The unknown distinction is whether this affine hull has dimension one
or zero.

## 3. Constant-accuracy canonical evaluation decides the predicate

The minimum-norm point of \(S\) is unique. Because its \(w\)-part is
fixed in both cases, its last coordinate is

\[
 y_{\rm can}=\begin{cases}
        0,&\sum_i\sqrt{a_i}\le B,\\
        1,&\sum_i\sqrt{a_i}>B.
       \end{cases}
 \tag{7}
\]

Suppose an algorithm returns a rational feasible point within Euclidean
distance \(1/4\) of the minimum-norm optimizer for every convex quartic
box instance of this form. Its last coordinate is at most \(1/4\) in
the first case and at least \(3/4\) in the second. Comparing that rational
coordinate with \(1/2\) decides (1).

Consequently a uniform \(\operatorname{poly}(I+q)\) point evaluator
for a compact exact **minimum-norm** selector, together with a
polynomial-time construction of its descriptor, would yield a
polynomial-time Square Root Sum comparison algorithm. Only the fixed
accuracy \(q=2\) is needed here. The implication does not depend on
computing an exact zero from an approximate number; (7) creates an
order-one gap between the two canonical answers.

Likewise, an exact affine-hull extraction algorithm that reports the
dimension of \(\operatorname{aff}S\) in polynomial time would decide
(1), by (6). Writing \(S\) as the box intersected with its affine hull
does not discharge that extraction obligation.

## 4. Selecting any optimizer avoids this comparison

The point \((w^*,1)\) is an optimizer in both cases of (6). The uniform
modulus in (2) permits certified rational approximation of \(w^*\) in
\(\operatorname{poly}(I+q)\) bit time by the established
[convex-patch evaluation lemma](convex-patch-evaluation.md).
Appending \(y=1\) produces a feasible rational point within the same
distance of an optimizer of (4).

The same observation gives a compact exact descriptor for one optimizer:
the unique box minimizer of \(H\), with the additional coordinate fixed
to one. It requires neither the active-bound decision in (3) nor the
dimension decision in (6).

This construction therefore distinguishes four obligations:

- Describing one optimizer with certified arbitrary-precision evaluation
  is easy for this family.
- Evaluating the minimum-norm optimizer contains the exact comparison (1).
- Extracting the exact optimal affine hull and its dimension also contains
  that comparison.
- Merely stating the polynomial KKT system supplies neither a general
  point-evaluation algorithm nor an exact affine-hull extraction algorithm.

No separation of complexity classes is asserted. The reduction does not
show that approximating **some** optimizer of an arbitrary convex
polynomial box problem is hard, and it does not establish a general
algorithm for that task. It explains why minimum-norm selection or exact
affine-hull extraction is a stronger output contract than the original
request for one optimizer.

The separate [paired construction](convex-point-radical-comparison.md)
extends the comparison implication to approximating any optimizer in a
different family. Here the arbitrary-selection route remains easy, making
the distinction from minimum-norm selection explicit.

## Verification record

An inline `python3 - <<'PY'` command checked five symbolic identities,
including the Hessian square decomposition and its uniform lower bound.
It also passed 80 exact optimizer-set fixtures for rational strongly
convex base objectives, including a positive distinguished coordinate at
a 400-bit scale. These fixtures check the new selector mechanism; the
radical-sum base construction has its own linked verification record.
The same command checked this file's whitespace, paired math delimiters,
and local links. The scoped command
`git diff --check -- research-20261002/new-direction/canonical-selector-radical-comparison.md`
passed. An initial symbolic check compared two differently expanded
expressions structurally; checking their expanded difference corrected
that diagnostic without changing the identity or the note.

[Independent actual-file review](canonical-selector-radical-independent-review.md)
passed the Hessian certificate, complete optimal-set description,
minimum-norm distinction, constant-accuracy comparison, and output scope.
No external search, index modification, project-wide checks, or CI
inspection was performed by this task.
