# Independent assessment of the Hessian-span package

Date: 2026-09-27. Reviewer: `hessian_package_assessment`.

The boxed Hessian-span value theorem and its exact integer-projection
consequence appear correct under their stated assumptions. This fresh review
found no substantive proof gap. It did find a material omitted precedent and
a weakness in the example used to explain the advance. These affect novelty
and significance claims, rather than the theorem itself.

The strongest defensible contribution is a uniform polynomial precision
bound for *continuous feasibility after fixing the integer variables*, with
exponent controlled by the span of the continuous Hessian blocks. Established
rational polyhedral approximations then preserve all feasible integer
assignments, with no extra integer variables. Exact integer preservation by
fine rational approximations was already published for pure integer balls
and ellipsoids. The present package should not claim that general mechanism
as new.

This assessment concerns the versions of
[the value proof](hessian-span-reduction.md),
[the continuous decision proof](hessian-span-exact-feasibility.md), and
[the integer-projection proof](mixed-integer-span-frontier.md)
read on this date, together with their existing reviews and literature audit.
Two fresh subreviews checked the value argument and primary-source novelty
comparisons. Their positive conclusions are supporting evidence; the
arguments below were also examined independently by this reviewer.

**Correctness of the value theorem.** The active-system restriction is the
critical structural step. Deleting inactive rows cannot introduce a lower
objective value: any allegedly better point gives a better nearby point on
its segment to the original optimizer, and that nearby point satisfies all
deleted rows. Turning active affine rows into equations preserves this
argument. The affine differences obtained from Hessian dependencies vanish
at the chosen optimizer and have rational coefficients of polynomial bit
length. Thus imposing them preserves the optimum and makes the *entire
restricted polynomials*, including their gradients, span a space of dimension
at most \(h\).

Conic sparsification must then use these polynomial coefficient vectors.
Dependence of numerical gradients alone would give a dimension bound based
on the number of primal variables. The written proof uses the correct
vectors, keeps only currently active rows, and therefore preserves
stationarity, complementarity and nonnegative multipliers. Negative
coefficients in the chosen Hessian basis cause no problem. The separate
ball multiplier costs one additional parameter.

The remaining delicate points also check out. The regularized stationarity
matrix is positive definite. All unsupported native constraints remain in
the polynomial feasibility conditions. A fixed support along a subsequence
is sufficient for the quantified limit formula; multipliers need not stay
bounded. Polynomial coefficient heights follow from rational elimination
and one common denominator for the restricted input coefficients, rather
than from an unjustified bound on the number of expanded monomials.

The primary quantitative source is Basu's survey, Theorem 2.27, available
locally as
`research-20260925/publication-sources/basu-2014-author-survey.txt`,
lines 784–805. The fresh value subreview read the explicit coefficient-bit
bound there. With two quantifier blocks of sizes \(1\) and at most \(h+3\),
one free variable, polynomial input coefficient height and degree \(O(N)\),
it gives the required \(N^{O(h+1)}\) degree and height. This is a use of the
source theorem, not a reproof of quantifier elimination.

The cases \(h=0\), zero-dimensional affine restriction, singular native
Hessians, and failed Slater conditions do not invalidate the argument. One
small wording improvement is to qualify the reverse implication from
system (5) by “for \(0<\varepsilon<1\).” Formula (6) already supplies that
condition, so the conclusion is unaffected.

**Correctness of the exact discrete consequence.** The maximum-violation
epigraph is nonempty even on an infeasible original integer fiber. Explicit
integer bounds make substitution length uniformly polynomial without
enumerating integer assignments. Applying the value theorem to this
epigraph gives the needed alternative: its minimum is zero or at least one
uniform \(\Delta>0\).

The discounted-tent proof correctly shows that allowing slack in the tent
chain cannot improve the weighted sum. Rational weighted-square
decomposition avoids irrational Cholesky coefficients. Positive square
weights are essential and follow from the *full* positive semidefinite
Hessians. The resulting lower approximation has a uniform additive error
below \(\Delta\). Every integer vector in the outer approximation therefore
has an exact original feasible fiber. Its displayed continuous coordinates
need not be feasible; the package states this distinction correctly.

The root-difference resultant is nonzero even when the two annihilators
share factors. Shared roots contribute powers of the difference variable.
The stated degree and height bounds give a uniform separation of distinct
slice optima. Threshold bisection consequently identifies an optimal integer
assignment for fixed integer dimension and fixed \(h\). This is not a proof
of exact continuous-optimizer recovery, nor does the conservative argument
preserve the original sharp parameter exponent after threshold substitution.
The manuscript appropriately limits its claim.

The compact formulation provides an additional simplification: setting the
number of integer variables to zero reduces exact continuous feasibility
to rational linear programming. Thus the earlier ellipsoid argument is a
useful independent route, but is no longer an essential algorithmic
dependency once the compact formulation is established.

**A material primary precedent.** Kocuk,
[*Rational Polyhedral Outer-Approximations of the Second-Order Cone*](https://optimization-online.org/wp-content/uploads/2019/12/7501.pdf)
(2021), Proposition 7, printed pp. 20–21, constructs a rational polyhedral
outer approximation having exactly the same integer points as an
intersection of balls with integral centers and radii. Section 5 states
that the argument also applies to integral ellipsoids. The proof chooses
relative error below \(\sqrt{1+1/R_i^2}-1\), using the gap between consecutive
integer squared distances. The lifted description uses additional
continuous variables. This reviewer independently opened and checked the
proposition and surrounding discussion after the fresh source subreview
located it.

This is direct prior art for the approximation-to-exact-integer mechanism.
It does not supply the present theorem for projected mixed continuous
fibers: minimizing violation over a continuous fiber produces an algebraic
number, whose positive gap is not an elementary denominator bound. The
Hessian-span height theorem supplies that missing uniform precision bound.
The literature comparison should distinguish this extension explicitly.

**Relation to the local fixed-count theorem and other primary sources.**
The proof in
[05-fixed-count.tex](../paper-exact-penalties/sections/05-fixed-count.tex)
already supplies the active affine-face argument, regularized KKT
elimination, the two-block limit formula, and the same BPR height theorem
for a fixed number of native quadratic rows. The present proof adds active
Hessian-dependence equations and multiplier compression to replace that
count by matrix-span dimension. This is a coherent strengthening, but most
of its algebraic machinery is inherited from the local work and established
real-algebraic methods.

The supplied prior audit correctly identifies Nie–Ranestad's generic
QCQP algebraic degree, Grigoriev–Pasechnik's quadratic-map sampling bounds,
and Kamminga–Rudolph's few-quadratic methods as substantial precedents.
Polynomial algebraic degree for a fixed quadratic count is not new.
Neither degree alone nor a sampling statement with all affine rows counted
as quadratic-map components is the exact height theorem used here.

Del Pia's
[*Convex Quadratic Sets and the Complexity of Mixed Integer Convex
Quadratic Programming*](https://arxiv.org/abs/2311.00099)
already gives a stronger fixed-parameter exact result in its one-quadratic
setting, without the present explicit box assumption and with stronger
optimizer output. The new class permits many native quadratic rows and a
growing continuous dimension. Khachiyan–Porkolab's quantified
semialgebraic theorem does not immediately eliminate the cost of a growing
existential continuous block. These distinctions, rather than a broad
claim to the first exact convex mixed-integer method, are the proper
comparison.

The local primary text of Lubin, Yamangil, Bent and Vielma,
[*Polyhedral approximation in mixed-integer convex optimization*](https://arxiv.org/abs/1607.03566),
was also examined. Its extended conic outer-approximation algorithm and
finite convergence analysis are relevant formulation precedents. Its
strong-duality requirements and iteration analysis do not establish the
uniform rational formulation-size bound here. The present theorem gives
no new branch-and-bound bound or observed speedup.

**A stronger example separating the parameter from PSD-generator counts.**
The diagonal moment-curve example in the value note has a limitation.
Although its \(m\) input matrices generate \(m\) extreme rays of their own
cone, every matrix is a nonnegative combination of three fixed PSD
coordinate-block matrices. A three-quadratic epigraph formulation therefore
handles that family. It does not establish a separation from all bounded
common-generator reformulations.

The following replacement gives the required stronger statement. For
distinct rational numbers \(t_1,\ldots,t_m\), \(m\ge3\), and any positive
integer \(r\), let

\[
 Q_r(t)=
 \begin{pmatrix}I_r&tI_r\\tI_r&t^2I_r\end{pmatrix}.
\]

These matrices are PSD of rank \(r\). Their span has dimension three,
because the coefficient vectors \((1,t,t^2)\) at three distinct parameters
are linearly independent. The sum of any two distinct matrices is positive
definite: their kernels have trivial intersection. Their aggregate range
therefore has dimension \(2r\).

Suppose one common family of nonzero PSD matrices \(H_1,\ldots,H_p\),
not necessarily in this three-dimensional span, represents every input by

\[
 Q_r(t_i)=\sum_{j=1}^p a_{ij}H_j,
 \qquad a_{ij}\ge0.
\]

If \(a_{ij}>0\), then every \(v\in\ker Q_r(t_i)\) obeys

\[
 0=v^TQ_r(t_i)v=\sum_j a_{ij}v^TH_jv,
\]

so \(v^TH_jv=0\), hence \(H_jv=0\) by PSD. Thus

\[
 \operatorname{range}H_j\subseteq
 \operatorname{range}Q_r(t_i)
 =\{(u,t_i u):u\in\mathbb R^r\}.
\]

The displayed ranges for distinct parameters intersect only at zero.
A nonzero \(H_j\) can therefore appear with positive coefficient for at most
one input matrix. Every input requires at least one such generator, proving

\[
 p\ge m.
\]

This shows that fixed span dimension three is more general than
a fixed number of shared PSD quadratic generators, even allowing
generators outside the input span and aggregate rank tending to infinity.
It does not rule out every conceivable extended nonlinear formulation;
the obstruction concerns this specific common-generator reduction.
The root and the fresh source subreview independently checked the argument.

**Significance judgment and remaining uncertainty.** The package has a
credible theoretical contribution: exact rational MILP representations of
the integer projections of a larger convex quadratic class, together with
exact decision and optimal integer assignment for fixed integer dimension.
This is more consequential than only enlarging a sufficient-penalty bound.
The proposed structural recognition is computable by rational matrix rank,
and the improved example shows the parameter need not conceal a bounded
number of PSD generators.

The contribution is still an extension of known few-quadratic algebraic
methods combined with known approximation machinery. The missing Kocuk
comparison weakens any claim that the formulation mechanism itself is
original. No equivalent theorem for the stated mixed continuous Hessian-span
class was found in this limited review, but that does not establish
priority or publication significance. A publishable presentation should
foreground the continuous-fiber height theorem and compare the exact
assumptions and outputs, while avoiding claims of a general MINLP
breakthrough.

Practical value would require explicit usable precision estimates, evidence
that useful models have small span after reasonable reformulation, and
tests of formulation size and LP strength. None follows merely from a
polynomial worst-case encoding bound. Recovering exact algebraic continuous
solutions and eliminating input bounds are separate research questions;
extensions developed after this assessment need their own review.

**Verification record.** The targeted reads were `cat`, `sed` and `rg`
over the named notes, the local fixed-count proof, and relevant literature
full texts. Open web searches used Hessian span, linearly independent
quadratic constraints, and exact integer-preserving polyhedral
approximations; only primary papers were used for substantive comparisons.
The fresh source subreview supplied the Kocuk lead, which was independently
checked through the open author PDF.

A targeted inline Python/SymPy command constructed \(Q_r(t)\) for

```
r in (1,2,3),  t in (-2,-1,0,1,2).
```

It checked exact matrix-span rank three, each matrix rank \(r\), aggregate
rank \(2r\), and full rank of each concatenated pair of range bases. All
checks passed. They challenge indexing and block placement; the general
generator obstruction is established by the kernel proof above. No
project-wide verification, CI inspection, solver experiment, or Lean proof
was run for this assessment.
