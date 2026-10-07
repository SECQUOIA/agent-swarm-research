# Significance assessment: random linear tilts and quantitative growth

Date: 2026-10-02. This assessment reads the
[theorem](../new-direction/smoothed-linear-growth.md), its
[mathematical review](smoothed-linear-growth-adversary.md), and the
[prior-art audit](../prior-art/smoothed-linear-growth-prior.md). It evaluates
significance and claim boundaries, rather than repeating the completed proof
review. A separate agent independently assessed the classical-conjugacy
comparison below and reached the same conclusion.

The result is a useful quantitative conditioning lemma with a meaningful
finite-bit completion. Its strongest contribution is the connection to the
conditioned optimization algorithms. The continuous-noise proof is also a
short corollary of classical one-dimensional maximal inequalities and convex
conjugacy once the optimizer response is identified. It should not be
presented as a new genericity principle or new maximal-function theory.
Publication priority for the explicit bound remains unresolved.

## What the numerical bound adds

The theorem controls the entire feasible set at once: with probability at
least \(1-\rho\),

\[
 F_c(x)-\min_X F_c\ge g\|x-x^*\|^2\qquad\(x\in X\),
\]

where \(g\) has an explicit lower bound in terms of dimension, coordinate
range, perturbation density, and failure probability. For rational uniform
noise of amplitude \(\sigma\), the stated bound is

\[
 g\ge\frac{\rho\sigma}{24n^2W},
 \qquad W=\max_i\left(\max_X x_i-\min_X x_i\right).
\]

An assertion that the optimizer is unique, or that some positive \(g\)
exists, does not control the running time of an algorithm depending on
\(L/g\) or \(\nu/g\). The explicit numerical lower bound does. It controls
both near-optimal competitors close to the optimizer and distant regions
with nearly equal objective values. A local Hessian condition on the winning
face would not provide the latter control.

The bound for continuous noise needs neither smoothness of \(f\) nor a
semialgebraic description of \(X\). Its constant does not depend on the
number of faces, stationary points, or integer assignments. This uniformity
is useful. It is not an algorithm for arbitrary continuous objectives:
computable evaluations, lower bounds, and the structural assumptions of the
subsequent solver remain necessary.

According to the source checks in the prior-art audit, Lee and Phạm already
establish generic uniqueness and positive quadratic growth under linear
perturbations in the semialgebraic setting. Those results must receive
priority for that qualitative claim. Their open-dense or uniform local
stability conclusions also differ from an almost-everywhere pointwise
statement. The present result supplies a numerical probability estimate;
it does not reproduce every stability conclusion of those papers.

## How much of the argument is classical

Extend \(f\) by \(+\infty\) outside \(X\), and form its convex conjugate

\[
 H\(a\)=\max_{x\in X}\{a^Tx-f(x)\}.
\]

Compactness makes \(H\) finite and Lipschitz. Along any coordinate line its
one-sided derivatives are monotone and bounded by the corresponding
coordinate range. They are the optimizer responses, with a sign change
relative to the theorem's minimization convention. Their distributional
derivatives are finite positive measures. Applying the ordinary weak-
\((1,1)\) maximal bound to these measures gives the theorem's estimate for
large anchored secant slopes.

On the good event, this slope control gives a quadratic upper estimate for
\(H\) along each coordinate line through the sampled coefficient vector.
Fenchel's inequality turns that upper estimate into a lower bound for
\(f(x)-a^Tx\) in the corresponding coordinate displacement. Choosing a
largest displacement coordinate gives the Euclidean growth bound. The
draft proves this last step directly by comparing two tilted optimizers;
that is the same elementary duality mechanism.

Consequently, the continuous theorem is a short classical corollary in a
precise sense: the proof adds no new covering theorem, monotonicity theorem,
or conjugacy principle. Its potentially useful contribution is recognizing
and quantifying this combination for global optimization. A short proof
does not establish that the exact statement has already been published,
but it makes a strong novelty claim risky without a broader source check.

Even the qualitative extension to arbitrary continuous compact problems
has an elementary classical derivation. A bounded monotone scalar response
has a finite derivative almost everywhere. At such a point its nearby
anchored secants are bounded; its distant anchored secants are bounded by
the response's total range. Fubini's theorem gives finite anchored slopes
in every coordinate for almost every coefficient vector. The same growth
argument then gives some positive global modulus.

There is a second classical derivation. At almost every \(a\), Alexandrov's
theorem gives a quadratic expansion of the finite convex function \(H\),
so for sufficiently small \(v\),

\[
 H(a+v)\le H\(a\)+\langle x^*,v\rangle+C\|v\|^2.
\]

Fenchel's inequality implies

\[
 f(x)-a^Tx-\min_X(f-a^T\cdot)
 \ge \langle v,x-x^*\rangle-C\|v\|^2.
\]

Since \(X\) has bounded diameter, one fixed sufficiently small \(\alpha>0\)
allows \(v=\alpha(x-x^*)\) for every \(x\in X\), giving global quadratic
growth. These are analytic deductions from classical facts, not claims
that the prior-art audit located this exact corollary. They show why
non-semialgebraic qualitative generality alone is a weak novelty argument.

The theorem also does not prove neighborhood-uniform tilt stability. Its
slope bound anchors every secant at one realized coefficient, rather than
bounding the response between every nearby pair of coefficients. The
deterministic local equivalences in Drusvyatskiy and Lewis are relevant
background, not an interchangeable statement of the probabilistic result.

## Why finite-bit sampling matters

The rational-grid argument closes a real gap between a continuous-noise
theorem and an exact rational algorithm. A measure-zero exceptional set may
contain every point of a particular finite grid. Rounding continuous noise
therefore cannot be justified by almost-sure genericity alone.

For a rational QP, the draft bounds the number of affine pieces of a scalar
optimizer response and then the number of interval components of its bad
set. Length plus component count controls how many points of a rational
grid can be bad, including isolated bad points. The grid is exponentially
large but represented implicitly; only its logarithmic size enters the
random-bit and coefficient-length bounds. The same reasoning covers long
integer domains and bounded rational polytopes without enumerating their
assignments or faces.

This provides polynomial-bit perturbations with a controlled numerical
growth modulus. That is stronger than merely sampling outside an algebraic
exceptional set. The ingredients are standard face counting, parametric
quadratic algebra, and one-dimensional grid counting. Beier and Vöcking
already establish the importance of quantitative discrete isolation and
finite random bits. Thus finite precision itself is not a new concept;
the useful completion here is retaining continuous distance growth for
rational QPs. The source audit has not established priority for that
completion.

## What the solver corollaries mean

The linear perturbation preserves the interaction graph, Hessian, and
negative inertia. On the good event it bounds the growth ratio used by the
reviewed algorithms. Under the stated numerical scale assumptions this
gives exact certified optimization of the sampled objective in polynomial
work, for each fixed supplied bag size on mixed boxes, or each fixed
negative inertia on continuous bounded rational polytopes.

The numerical assumptions are material. Polynomial binary input length
does not make \(W,L,\nu,\sigma^{-1}\), or \(\rho^{-1}\) polynomial in
value. The exponent may depend on the fixed bag size or negative inertia.
Substituting an inverse-polynomial random growth bound does not establish
FPT in either structural parameter alone. The polytope result does not
supply a general mixed-integer convex recourse oracle.

A capped implementation always obeys its selected work budget and may
report failure. Its probability of returning an exact certified answer
is at least \(1-\rho\). This is not a bound on the expected time of an
uncapped solver required to finish on every sampled instance. In the
rational theorem the sampling grid itself also depends on \(\rho\), so
one cannot integrate bounds obtained by changing \(\rho\) as though they
concerned one fixed finite distribution.

The inverse-modulus issue already occurs in one dimension. Let
\(X=[-R,R]\), \(f=0\), and let \(c\) be uniform on
\([-\sigma,\sigma]\). For \(c\ne0\), the largest valid global growth
constant is exactly (g_*\(c\)=|c|/(2R)). Hence

\[
 \Pr\{g_*\le t\}=\frac{2Rt}{\sigma}
 \quad\left(0\le t\le\frac{\sigma}{2R}\right),
 \qquad \mathbb E[1/g_*]=\infty.
\]

This shows that linear lower-tail order is unavoidable for the class,
although it says nothing about optimal dimension dependence. The example
itself is easy to solve; it illustrates why a runtime estimate by an
inverse power of the modulus does not automatically yield an expected
runtime estimate.

Finally, solving the sampled objective changes the optimization question.
There is a useful but weaker transfer to the original objective. If
\(|c_i|\le\sigma\), coordinate widths are \(w_i\), and \(y\) is
\(\delta\)-optimal for \(f+c^Tx\), comparison with an original optimizer
gives

\[
 f\(y\)-\min_X f\le\delta+\sigma\sum_i w_i.
\]

Thus sufficiently small noise gives an approximation to the original
problem. Choosing its amplitude for an original error target
\(\varepsilon\) generally makes the runtime depend polynomially on
\(1/\varepsilon\), instead of retaining polynomial dependence only on
accuracy bits. Noise small enough to preserve an exponentially tiny
original decision gap can similarly destroy the numerical polynomial-work
guarantee. The theorem gives no general exact-recovery claim for the
unperturbed problem.

For solver design, the result supplies a principled way to analyze
conditioning after deliberate linear perturbation. It does not convexify
the Hessian, remove other local minima, or demonstrate that a numerical
local solver will find the global optimum. The algorithmic conclusion
comes from the separate certified global algorithms; no practical speedup
has been measured here.

The defensible positioning is an explicit global-growth probability bound,
its finite-precision realization for QPs, and consequences for conditioned
global solvers. Generic uniqueness, qualitative growth, maximal-function
theory, and discrete finite-bit isolation are established background.
The quantitative statement may still be a useful contribution, but the
current evidence supports a carefully scoped result rather than a broad
priority claim about smoothed optimization.

Verification consisted of targeted document reads and independent analytic
comparison. A targeted `python3` check of this file passed after correcting
inline math delimiters; it checked trailing whitespace, paired math
delimiters, and local Markdown link targets. No new external literature search, executable optimization
test, project-wide verification, or CI inspection was performed for this
assessment.
