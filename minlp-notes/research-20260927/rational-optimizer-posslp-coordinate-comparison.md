# PosSLP-complete coordinate comparison with a rational quartic optimizer

Date: 2026-09-28. Status: substantive component theorems independently
reviewed; the composition was separately checked by the root, who
authored the quaternion realization. This composition check is not
presented as a fresh noncontributor review. Publication priority is
unestablished.

Exact coordinate comparison remains PosSLP-hard even when a rational
quartic is supplied with strong rational convexity certificates and its
unique optimizer is promised rational. The rationality promise does not
give a polynomial bound on the optimizer's expanded fractions.

## Problem and statement

An input consists of a rational quartic \(F\) in \(N\) variables,
a full positive definite rational Hessian Gram on
\((v,X\otimes v)\), a coordinate index \(j\), and a rational
threshold \(r\). The positive definite Gram implies global strong
convexity and a unique minimizer \(p\). The question is whether
\(p_j>r\).

**Theorem.** This
coordinate comparison problem is PosSLP-complete under polynomial-time
many-one reductions. Its lower bound already holds for inputs with
all of the following additional promises:

- \(p\in\mathbb Q^N\cap[-1,1]^N\).
- \(\min F=0\), with \(N+1\) supplied rational quadratic
  square factors.
- \(\nabla^2F\succeq(3/2)I\), with a supplied rational full
  positive definite Hessian Gram.
- The threshold is \(r=0\), and \(p_j\ne0\).

The upper reduction holds for the full certified class, so it also
holds when restricted to the rational-optimizer promise. This is a
promise restriction: no algorithm is asserted for recognizing whether
an arbitrary certified quartic has a rational minimizer.

## Lower reduction

Given an integer arithmetic circuit with output \(V\), apply the
[quaternion sign compiler](quaternion-circuit-posslp-reduction.md).
It returns a polynomial-size shared circuit over a fixed finite set
of rational unit quaternion constants, multiplication, and inversion.
The selected output coordinate is nonzero and has the sign of
\(2V-1\). All quaternion coordinates are rational and bounded by
one in absolute value.

Apply the
[unit-quaternion quartic realization](unit-quaternion-circuit-quartic-realization.md)
to this circuit. It produces the asserted quartic, square factors,
and full Hessian Gram in polynomial time. Its unique zero and minimizer
is exactly the list of all quaternion gate values, with no change
of coordinates. The selected coordinate of the selected gate therefore
satisfies
\[
                         p_j>0\quad\Longleftrightarrow\quad V>0.
\]
The optimizer is rational because every gate uses rational arithmetic.
The construction does not expand its exact coordinates. This proves
the lower bound and all stated promises.

If a normalization requiring the full Hessian Gram to be at least
identity is desired, compute its positive rational spectral bound
\(\rho=\det H/(\operatorname{tr}H)^{N+N^2-1}\), choose an
integer square above \(1/\rho\), and multiply the objective by
that square. This preserves the optimizer and rational square factors,
and has polynomial bit complexity.

## Upper reduction

The [general strong-convex-quartic upper bound](strong-convex-quartic-posslp-upper.md)
reduces optimizer-coordinate comparison to one PosSLP instance.
It first computes a polynomial-precision rational approximation,
then performs polynomially many Newton iterations as a shared exact
rational arithmetic circuit. Effective algebraic separation bounds
allow a final offset test that handles equality as well. A positive
rational global curvature lower bound is obtained from the supplied
full positive definite Hessian Gram by the determinant-over-trace
bound. Thus every assumption of that upper theorem is satisfied.

Combining the two polynomial-time many-one reductions proves the
claimed completeness. The upper construction does not require the
minimizer to be rational and does not supply a short expanded rational
minimizer when it is.

## Significance and limits

The arithmetic obstacle is present even when the optimizer field is
\(\mathbb Q\), the optimum value is the known rational number zero,
and the objective is explicitly a short rational sum of squares.
Rationality alone does not turn exact comparisons into ordinary
polynomial-time rational linear algebra. PosSLP-completeness is a
classification relative to a well-studied unresolved arithmetic
problem; it does not establish NP-hardness or a separation from P.

The theorem concerns a coordinate of the optimizer, not the sign of
the minimum value for quartics with a promised rational optimizer.
A perturbation used to encode that value can move the optimizer to
an irrational point. No rationality claim for such a perturbed
optimizer is made here.

For optimization solvers, the theorem identifies a limit on replacing
symbolic comparisons with expanded rational output merely because a
rational optimum is known to exist. Compact arithmetic circuits retain
the exact optimizer in the constructed instances. Developing useful
solver interfaces for such representations is a possible application,
not an algorithmic speedup proved by this result.

The [primary-source comparison](quaternion-circuit-posslp-prior.md)
credits matrix-circuit simulation and near-identity commutator methods.
It distinguishes compressed identity predicates from coordinate signs,
and does not establish publication priority. The proof of this
composition is short, but its substantive dependencies are the uniform
quaternion error bounds and the rational quartic realization; their
independent verification status is recorded in the linked notes.

The root independently checked the preserved coordinates, every added
promise, the rationality distinction, the optional full-Gram scaling,
and the general upper-bound interface. The author also read the full
quartic realization proof and its fresh independent review. The
component notes record exact mathematical checks. A targeted inline
documentation check of the six authored topic notes passed eighteen
local links, math delimiters, whitespace, control characters, and final
newlines; a targeted `git diff --check --` on those paths also passed.
No project-wide verification or CI inspection was performed.
