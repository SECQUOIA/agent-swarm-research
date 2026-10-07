# Adversarial review of the proximal growth tail

Date: 2026-10-02. Scope: the actual text of
[`proximal-growth-tail.md`](../new-direction/proximal-growth-tail.md),
including an independent check of the uniform-volume argument.

## Verdict

The continuous bounded-density theorem, uniform-volume proof, and finite
rational-grid completion pass.
The proximal argument gives the sharp bound

\[
\Pr\{g_*<\varepsilon\}\le
2\varepsilon\sum_i\phi_iw_i
\]

for every continuous objective on a nonempty compact feasible set. No
convexity or definability assumption on the original optimization problem
is needed. This conclusion concerns the actual global growth modulus.

The initial completed draft had one missing assumption in its product
sharpness example, described below. The current text includes the
correction. No substantive mathematical gap remains in the reviewed
statements.

## Definition and measurability

For a nonsingleton feasible set, the definition of the largest growth
constant is valid. A minimum exists by compactness. If it is unique, the
infimum of the ratios is attained as a valid lower bound even when no
individual ratio equals that infimum. It is finite because there is some
other feasible point. If there are multiple minimizers, the largest
constant is zero.

The set admitting growth at least a fixed positive \(\varepsilon\) is
closed. Given convergent coefficient vectors and corresponding growth
certificates, compactness provides a convergent subsequence of the
optimizers. Passing each inequality to the limit proves the same
certificate at the limiting vector. Thus the strict bad-growth event is
open and measurable. The singleton convention is consistent with this
argument.

The note safely chooses a Borel null superset of the nondifferentiability
set of the finite Lipschitz convex function \(H\). Its preimage under the
continuous proximal map is Borel. The proof does not need a stronger
description of the nondifferentiability set.

## Proximal map and the quadratic-growth certificate

The quadratic proximal objective is coercive and strongly convex, so its
minimizer exists and is unique. Monotonicity of \(\partial H\) gives the
stated Lipschitz and monotonicity properties of \(P\) and \(Q=I-P\).
The identity

\[
P=\nabla\bigl(\|\cdot\|^2/2+\lambda H\bigr)^*
\]

has the correct scaling. Consequently its almost-everywhere derivative
is symmetric positive semidefinite and bounded above by the identity.
This is a statement about the convex conjugate in coefficient space;
the original objective may be nonconvex.

Every maximizing point defining \(H\) is a subgradient. At a
differentiability point this forces all maximizing points to equal the
gradient, which therefore belongs to the original feasible set, not
merely its convex hull. The signs and factor \(\lambda=2\varepsilon\)
in the substitution \(z=a+2\varepsilon x^*\) are correct and give
the claimed global quadratic-growth inequality for \(f-z^Tx\).

The reverse implication is not asserted or needed. The exceptional
preimage may contain points that already have growth exactly
\(\varepsilon\).

## Area formula and density integration

Applying the area formula on the bounded pieces of
\(E=P^{-1}(N)\) is valid. Their images lie in a null set, so the
integral of \(|\det DP|\) vanishes. Infinite multiplicities over
points of that null set do not change the zero integral. Taking a
countable union gives the almost-everywhere conclusion on all of \(E\).

At such a point, a symmetric matrix whose eigenvalues lie in \([0,1]\)
and whose determinant is zero has at least one zero eigenvalue.
Therefore \(\operatorname{tr}(I-DP)\ge1\). Outside \(E\) the trace
is nonnegative, so the displayed global indicator inequality is valid.

For every fixed value of the other coordinates, \(Q_i\) is a bounded,
nondecreasing, Lipschitz function of its own coordinate. Its derivative
is nonnegative and its integral over the real line is at most
\(\lambda w_i\). This uses absolute continuity on finite intervals
and then monotone convergence. Independence permits the bounded
one-dimensional density to be applied after conditioning. Fubini
identifies the section derivatives with the Jacobian entries outside a
null set. Absolute continuity of the joint distribution removes that
null set from the probability calculation.

The stated extension to uniformly bounded one-coordinate conditional
densities also follows by the same conditioning argument. The resulting
joint law is absolutely continuous: each marginal has a density, and
successive conditional densities are obtained by averaging the
full-coordinate conditional densities.

## Uniform-volume argument

This argument was also checked by a separate reviewer. Translating the
feasible set, with the objective expressed in the translated variables,
preserves every growth constant. It permits the displacement bound
\(|T_i(a)-a_i|\le\varepsilon w_i\).

At each regular point of the inner coefficient box, the expanding map
\(T\) reaches a good coefficient in the original box and satisfies
\(P(T(a))=a\). The closed good-growth set intersected with a closed
coefficient box is compact. Its image under \(P\) is compact and
contains the inner box except for a null set. The 1-Lipschitz volume
bound therefore proves the product estimate without assuming
measurability of an arbitrary forward image under \(T\).

If an inner interval disappears, the final linear upper bound is already
at least one. Zero coordinate widths cause no problem.

## Sharpness-example qualification

The scalar example correctly attains the constant \(2\). The draft's
following product sentence needed to retain the centered uniform assumptions:
for example, take

\[
X=\prod_i[-w_i/2,w_i/2],\quad f=0,\quad
c_i\sim\operatorname{Unif}[-\sigma_i,\sigma_i]
\]

independently, with \(\phi_i=1/(2\sigma_i)\). Then
\(g_* = \min_{i:w_i>0}|c_i|/w_i\), and the stated product tail is
exact within its displayed range.

An arbitrary separable linear objective need not have that distribution.
For \(X=[-1/2,1/2]\), \(f(x)=2x\), and
\(c\sim\operatorname{Unif}[-1,1]\), the modulus is at least one.
At \(\varepsilon=1/4\), the actual bad probability is zero, whereas
the unrestricted product formula would give \(1/4\). This is a missing
example hypothesis, not an obstruction to the general upper bound. The
current text now explicitly takes a product of the centered uniform
examples, resolving the issue.

## Finite rational-grid completion

An independent reviewer also checked this completion, with a separate
focused check of the face-candidate argument; both found no defect.

The quadratic candidate fact is valid on lower-dimensional compact
polytopes as well as boxes. At a minimizer in the relative interior of
its smallest face, the Hessian restricted to the face tangent is positive
semidefinite and the tangential gradient vanishes. A null direction
therefore preserves the objective until a face boundary is reached.
Repeatedly reducing the dimension produces a minimizer on a face with
positive definite tangent Hessian, or a vertex. This argument applies
separately to each integer assignment of a mixed box.

There is at most one stationary candidate for each qualifying face.
Its dependence on a scalar coefficient is affine, and its feasibility
set is an interval, possibly empty, unbounded, or a singleton. The same
facts apply to the modified objective: subtracting
\(\varepsilon\|y-x_r(t)\|^2\) leaves a Hessian independent of
\(t\), while its linear coefficients are affine in \(t\). It is
not necessary that only one modified linear coefficient varies.

The Boolean certificate is equivalent to positive global growth. For
sufficiency, the modified face candidates include a global minimizer,
so checking every feasible modified candidate proves the full growth
inequality. That inequality itself proves that the proposed original
candidate is an optimizer; no preliminary ranking of the original
candidates is required. For necessity, positive growth gives a unique
optimizer, which the original candidate fact must recover. Singularity
and multiple original minimizers therefore create no missing case.

Every score comparison has degree at most two in \(t\). The count

\[
K\le 2F+4F^2,\qquad
2K+1\le 8(F+1)^2=C
\]

includes original and modified feasibility endpoints, polynomial roots,
and individual breakpoint cells. Empty feasibility intervals and
identically zero comparisons require no extra breakpoints. The component
bound is uniform over fixed values of the other coefficients and over
all positive \(\varepsilon\). The list of qualifying modified faces
may change with \(\varepsilon\), but its size and all polynomial-degree
bounds remain the same.

The \(M\)-point grid includes both endpoints and has spacing
\(2\sigma/(M-1)\). Its cumulative distribution function differs from
the continuous uniform one by at most \(1/M\), including one-sided
limits at atoms. A union of at most \(C\) intervals or points therefore
has probability discrepancy at most \(2C/M\). Replacing marginals
successively gives the stated \(2nC/M\) discrepancy even when some
coordinates are already discrete.

Consequently the entire tail, with one fixed grid size, satisfies

\[
\Pr_{\rm grid}\{g_*<\varepsilon\}
\le \frac{\varepsilon}{\sigma}\sum_iw_i+\beta,
\qquad
\beta=\frac{2nC}{M},
\qquad \varepsilon>0.
\]

The additive term is independent of \(\varepsilon\). Applying this
bound at \(\varepsilon+\delta\) and sending \(\delta\downarrow0\)
also proves the same bound for \(\{g_*\le\varepsilon\}\), and
\(\Pr(g_*=0)\le\beta\). The grid guarantee permits tie atoms;
it does not establish uniqueness on every sample or finite inverse-growth
moments without further argument.

The choices
\(\varepsilon=\rho\sigma/(2\sum_iw_i)\) and
\(M\ge32n(F+1)^2/\rho\) allocate at most \(\rho/2\) to each
tail term. The powers-of-two sampling and polynomial bit-length claims
follow from \(\log M=O(\log F+\log(n/\rho))\). The face counts in
the stated families have polynomial logarithms, including binary-encoded
integer intervals. No face enumeration is part of the sampler.

## Algorithmic scope

Substituting the rational growth bound into \(L/g_*\) and
\(\nu/g_*\) gives the displayed constants in Section 9. Linear
perturbations preserve the Hessian and interaction graph. The claims
retain the earlier fixed-parameter and numerical-scale assumptions.
This review validates the substitution and does not repeat the separate
reviews of the optimization algorithms. The note correctly refrains
from inferring expected work from the tail alone.

## Verification scope

This review checks the written mathematics and the stated probability
events. It makes no literature-priority claim and does not infer expected
solver work or recovery of an unperturbed optimizer. No executable
optimization test, project-wide verification, or CI inspection was used.

The targeted `python -` document check on this review passed trailing
whitespace, final newline, paired math delimiters, and local-link checks.
