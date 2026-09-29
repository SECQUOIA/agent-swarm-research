# What remains open after the interior Gram size lower bound

Date: 2026-09-28. Status: documented limitations and a research
candidate. No all-PSD Gram size lower bound is proved here.

The [reviewed interior-Gram theorem](interior-gram-bit-lower-bound.md)
constructs strictly positive, strongly SOS-convex rational quartics
with a supplied small strict Hessian Gram, whose rational positive
definite polynomial Grams all require exponentially many bits.
The same polynomials have small singular rational Grams. The stronger
question is to force large encoding length for every rational PSD
Gram, including singular ones, under these restrictions.

## A small minimum cannot settle the stronger question

The existing family is itself a counterexample to that inference:
\[
 f_k=\lambda F+u^2,\qquad
 F=\sum_{\ell=1}^{n+1}q_\ell^2,\qquad
 0<f_k(p)<4M^{-2^{k+1}}.
\]
The displayed rational squares give a small singular Gram. A tiny
Rayleigh quotient constrains the smallest eigenvalue, but a zero
eigenvalue has no positive rational determinant to separate from zero.
Consequently the determinant proof cannot be applied to every PSD
Gram without an additional argument excluding short singular Grams.

A possible stronger route would prove that a suitable Gram
spectrahedron has no rational boundary point. Real boundary points
necessarily exist for a nontrivial compact strictly feasible affine
slice. Rationality of such boundary points is a separate question.
No such exclusion is established for the quartic families here.

## Why the direct penalty transfer from known constrained bounds fails

The [independent constrained-SOS literature review](gram-bit-size-constrained-sos-prior-review.md)
checked two relevant precedents. O'Donnell's example forces large
Gram entries in degree-two constrained certificates, but already
has a small degree-four certificate. Squaring quadratic constraints
produces a quartic and loses the degree restriction needed by that
lower bound.

For the unique-zero chain used by Raghavendra and Weitz, the failure
has an exact pointwise explanation. Let \(m\ge1\), fix rational
\(0<\epsilon<1/2\), and put
\[
 q_i(y)=y_i^2-y_{i+1}\quad(i<m),\qquad q_m(y)=y_m^2.
\]
The common real zero is the origin, where
\(g(y)=\epsilon-y_1\) is strictly positive. Consider the direct
penalty
\[
                  f_\lambda=\lambda\sum_{i=1}^m q_i^2+g.
\]
At the rational point
\[
                   a_i=(2\epsilon)^{2^{i-1}},
\]
the first \(m-1\) residuals vanish and
\[
 f_\lambda(a)
       =\lambda(2\epsilon)^{2^{m+1}}-\epsilon.
\]
Therefore even nonnegativity requires
\[
                 \lambda\ge
                   \epsilon(2\epsilon)^{-2^{m+1}}.
\]
For \(\epsilon=1/4\), this is
\(\lambda\ge2^{\,2^{m+1}-2}\). Its ordinary binary length is
exponential. For \(m\ge2\), the coefficient of \(y_m^4\) in
\(f_\lambda\) is exactly \(\lambda\), so the expanded input
already contains that large number. A large Gram matrix cannot repair
the negative value when a small \(\lambda\) is used.

This calculation is a restatement of the evaluation mechanism in the
prior proof, not a new lower-bound technique. It was independently
checked in the cited source review. It rules out this particular
fixed-penalty transfer; it does not rule out other embeddings of
constrained certificate systems into Gram spectrahedra.

## A nearby nonrational Gram face remains a candidate

A more relevant starting point may be a rational strongly
SOS-convex zero quartic that is SOS over the reals but not over
\(\mathbb Q\), such as the reviewed quintic examples. One could
combine its root realization with an independent small-signal
cubic-root chain and add the square of that signal. The intended
positive family would approach a Gram face with no rational points,
instead of the rational face present in the short-certificate
construction above.

This is not yet an encoding lower bound. In a naive algebraic
separation estimate, the small signal decreases at order \(2^k\)
while the full cubic-root field can have degree \(3^k\). The
arithmetic-degree factor can consume the desired precision lower
bound. Thus simply applying a full-field norm or general Liouville
estimate does not justify the intended conclusion.

A useful next step would isolate a fixed-degree irrational condition
on rational Gram entries, or otherwise control approximation in the
small subspaces actually used by quadratic factors. Alternatively,
an explicit small singular Gram for this perturbed family would
disprove the proposed mechanism. Neither outcome has been obtained.

## Encoding and significance

The target concerns expanded rational matrices in the standard
quadratic monomial basis. A short shared arithmetic circuit for very
large rational entries is compatible with an expanded-size lower
bound. A proof about ordinary Gram certificates would also leave
other certificate systems and decision complexity open.

The demonstrated result already shows that insisting on a strictly
feasible rational Gram can impose a large output penalty even when
a short boundary SOS certificate is available. It does not show that
exact rational SOS certification itself requires that penalty.

## Completed outcome of the block-separation route

The investigation of additive blocks produced a different reviewed
result. The [quartic lifting theorem](rational-block-sos-splitting-obstruction.md)
embeds a rational non-SOS quartic block into a rational SOS of two
independent blocks. At zero minimum, every separated certificate has
zero constant shift, so no rational separated certificate exists.
For a strictly positive family, rational separated certificates do
exist but require exponentially many denominator bits, while an
unrestricted rational SOS remains polynomial-size.

The [strong-convexity supplement](strongly-sos-convex-block-splitting-obstruction.md)
establishes this positive certificate-size separation for strongly
SOS-convex quartics with polynomial-size rational Hessian certificates.
Those joint Hessian Grams are singular on the full tensor basis:
additive separation prevents a positive definite full Hessian Gram.
The individual Gram-entry bound uses two local PSD polynomial Grams,
each with its own constant coordinate. The unrestricted joint Gram
remains short, so this does not settle the all-PSD question posed here.

Thus a proposed rational block-splitting shortcut fails even at the
level of existence. Real block splitting cannot be used to infer a
rational split or a bound on its encoding length. The
[primary-source comparison](rational-block-sos-splitting-prior.md)
distinguishes this from established support projections that do
preserve rational certificates.
