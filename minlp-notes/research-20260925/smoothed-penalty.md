# Rational right-hand-side perturbations and exact norm penalties

Date: 2026-09-25. Status: proof independently reviewed; primary-literature
comparison completed within the recorded search scope. The conditioning
mechanism is classical. The precise finite-grid penalty statement and
sharpness comparison are a useful companion to the worst-case result;
originality of the combined statement remains provisional. See the
[independent proof review](smoothed-penalty-review-second.md),
[geometry note](smoothed-penalty-geometry.md), and
[literature review](smoothed-penalty-novelty.md).

This work follows the worst-case
[penalty encoding obstruction](parametric-exploration.md), but studies a
different question: which penalty bound holds with high probability after
randomizing the right-hand side? It does not claim that solving the perturbed
problem solves the original problem.

## Setting

There are at most \(K\geq1\) integer assignments, indexed by a finite set
\(Z\). For each \(z\), let \(X_z\) be a nonempty compact convex native
continuous feasible set, \(r_z:X_z\to\mathbb R^m\) an affine residual map,
and \(f_z:X_z\to\mathbb R\) a continuous convex objective. Here \(m\geq1\).
Suppose common finite bounds satisfy

\[
 L\leq f_z(x)\leq U\qquad(x\in X_z,\ z\in Z),
 \qquad M=U-L.
\]

Empty native slices can be omitted. These assumptions are structural
promises; no efficient recognition algorithm is asserted.

For a right-hand side \(b\in\mathbb R^m\), define

\[
 v(b)=\min\{f_z(x):z\in Z,\ x\in X_z,\ r_z(x)=b\},
\]

with value \(+\infty\) if infeasible, and define the zero-multiplier norm
penalty value

\[
 p_\rho(b)=\min_{z\in Z,\,x\in X_z}
   \{f_z(x)+\rho\|r_z(x)-b\|_\infty\}.
\]

The residual images \(C_z=r_z(X_z)\) are compact convex sets. Their boundaries
are ambient topological boundaries, so a lower-dimensional image has
\(\partial C_z=C_z\). Let \(\operatorname{dist}_\infty\) denote distance
in the infinity norm.

## A deterministic margin bound

**Lemma 1.** Suppose \(d>0\), \(v(b)<\infty\), and

\[
 \operatorname{dist}_\infty(b,\partial C_z)>d
 \qquad\text{for every }z\in Z.
\tag{1}
\]

Then

\[
 p_{M/d}(b)=v(b).
\tag{2}
\]

For every \(\rho>M/d\), every minimizer defining \(p_\rho(b)\) satisfies
\(r_z(x)=b\), and the minimizer sets agree with the original problem.

**Proof.** Write \(v_z(b)\) for the optimum on a fixed equality-feasible
slice. If \(b\in C_z\), condition (1) implies that the closed cube
\(b+[-d,d]^m\) belongs to \(C_z\). Consider \(x\in X_z\) with residual
distance \(t=\|r_z(x)-b\|_\infty>0\). The point

\[
 u'=b-\frac d t(r_z(x)-b)
\]

belongs to \(C_z\); choose \(x'\in X_z\) with \(r_z(x')=u'\).
The convex combination

\[
 x_b=\frac d{d+t}x+\frac t{d+t}x'
\]

belongs to \(X_z\), and affinity gives \(r_z(x_b)=b\). Convexity of
\(f_z\) yields

\[
 v_z(b)\leq\frac d{d+t}f_z(x)+\frac t{d+t}U,
\]

so

\[
 f_z(x)\geq v_z(b)-\frac{U-v_z(b)}d t
          \geq v(b)-\frac Md t.
\tag{3}
\]

The same final inequality is immediate if \(t=0\).

If instead \(b\notin C_z\), a closest point in \(C_z\) lies on its
boundary. Thus (1) gives \(t>d\) for every \(x\in X_z\), and

\[
 f_z(x)+\frac Md t\geq L+M\geq v(b).
\]

Together these estimates show that the penalty value is at least \(v(b)\).
An original optimal point attains \(v(b)\), proving (2). Increasing the
coefficient strictly above \(M/d\) adds a strictly positive amount at
every point with nonzero residual, proving the minimizer-set statement.
This includes \(M=0\): zero penalty is value-exact, while a positive
penalty is needed for the stated minimizer-set conclusion. \(\square\)

This proof requires no differentiability or computed dual multiplier.
Equivalently, at an interior feasible right-hand side, bounded convex slice
values have a bounded subgradient. The direct convex-combination proof makes
the global nature of the estimate explicit.

## An elementary convex-boundary tube estimate

Let \(Q=b_0+[-\sigma,\sigma]^m\), with \(\sigma>0\). Write
\(\mathbb P_Q\) for uniform Lebesgue probability on \(Q\).

**Lemma 2.** For every nonempty closed convex set \(C\subseteq\mathbb R^m\)
and every \(t\geq0\),

\[
 \mathbb P_Q\{\operatorname{dist}_\infty(B,\partial C)\leq t\}
 \leq\min\{1,2mt/\sigma\}.
\tag{4}
\]

For \(C=\mathbb R^m\), interpret distance to its empty boundary as
\(+\infty\).

**Proof outline, expanded in the independent geometry note.** Expand \(C\)
one coordinate at a time by the segment \([-s,s]e_i\). A coordinate fiber
of a convex set is an interval. Expanding an interval by that segment
increases its length after clipping to the corresponding coordinate range
of \(Q\) by at most \(2s\). Fubini's theorem and telescoping over the
coordinates give

\[
 \operatorname{vol}(((C+[-s,s]^m)\setminus C)\cap Q)
 \leq 2ms(2\sigma)^{m-1}.
\]

Eroding sequentially by the same coordinate segments shrinks each clipped
interval fiber by at most \(2s\), and gives the identical estimate for
\((C\setminus(C\mathbin{\ominus}[-s,s]^m))\cap Q\).
For \(s>t\), the boundary \(t\)-tube belongs to the union of these inner
and outer shells. Divide their total volume by \((2\sigma)^m\), then let
\(s\downarrow t\). This yields (4). The argument includes unbounded and
lower-dimensional convex sets. \(\square\)

The estimate itself is established convex conditioning geometry in an
elementary cube formulation. No novelty claim is made for a general
convex-boundary tube principle.

## Finite rational perturbations

For an integer \(N\geq1\), define the centered grid

\[
 G_N=\left\{b_0+\sigma
   \left(\frac{2j_1+1-N}{N},\ldots,
         \frac{2j_m+1-N}{N}\right):
      j_i\in\{0,\ldots,N-1\}\right\}.
\]

Its coordinates are the midpoints of the \(N^m\) equal cells of \(Q\).
If \(B\) is uniform on \(Q\), rounding to cell centers gives a uniform
\(\widehat B\in G_N\) with

\[
 \|B-\widehat B\|_\infty\leq\sigma/N.
\]

Distance to a fixed closed set is one-Lipschitz. Lemma 2 therefore gives

\[
 \mathbb P\{\operatorname{dist}_\infty(\widehat B,\partial C)\leq d\}
 \leq \min\left\{1,2m\left(\frac d\sigma+\frac1N\right)\right\}.
\tag{5}
\]

This transfer accounts for boundary-aligned grid atoms. A continuous-noise
statement alone would not justify a discrete perturbation guarantee.

**Theorem 3.** Assume \(b_0,\sigma,\epsilon,L,U\) are rational, with
\(\sigma>0\) and \(0<\epsilon<1\). Choose

\[
 N\geq\left\lceil\frac{4mK}{\epsilon}\right\rceil,
 \qquad d=\frac{\sigma\epsilon}{4mK},
 \qquad \bar\rho=\frac{4mKM}{\sigma\epsilon}.
\tag{6}
\]

For a uniformly sampled \(\widehat B\in G_N\), with probability at least
\(1-\epsilon\), either the original equality-constrained problem is
infeasible at \(\widehat B\), or

\[
 p_{\bar\rho}(\widehat B)=v(\widehat B).
\tag{7}
\]

On the same event, every coefficient strictly larger than \(\bar\rho\)
also gives equality of minimizer sets whenever the problem is feasible.

**Proof.** By (5) and a union bound over at most \(K\) images,

\[
 \mathbb P\{\exists z:
  \operatorname{dist}_\infty(\widehat B,\partial C_z)\leq d\}
 \leq 2mK\left(\frac d\sigma+\frac1N\right)\leq\epsilon.
\]

Outside that event Lemma 1 applies whenever the original problem is
feasible. \(\square\)

The rational number \(\bar\rho\), the grid parameter \(N\), and one
sampled point have encoding length polynomial in the supplied rational
data, \(m\), and \(\log K\), when the smallest allowed \(N\) is used.
For bounded integer variables, the product of their numbers of possible
values supplies a valid \(K\), and its logarithm has polynomial length in
the encoded integer bounds. Neither grid generation nor computing (6)
requires enumerating the slices or their images. Uniformly drawing each
coordinate index uses \(O(\log N)\) expected random bits by rejection
sampling. This is an encoding guarantee, not a polynomial-time global
optimization algorithm or a polynomial numerical-magnitude bound.

## Feasibility and local stability

The theorem deliberately states an infeasibility-or-exactness alternative.
It does not guarantee that the perturbation produces a feasible instance.
In particular, if every image is lower dimensional, most perturbations
are infeasible.

If one known slice satisfies \(Q\subseteq C_{z_0}\), every sampled point
is feasible, and the exactness probability is at least \(1-\epsilon\)
without an alternative. More generally, if feasibility has probability at
least \(p_0>0\), the conditional failure probability given feasibility is
at most \(\epsilon/p_0\). To obtain conditional failure at most
\(\epsilon\), apply the construction with \(\epsilon p_0\) instead.

At a point satisfying (1), the feasible integer assignments are unchanged
throughout \(b+[-d/2,d/2]^m\). Each feasible slice value is Lipschitz there
with constant at most \(2M/d\) in the infinity norm, by applying (3) in
both directions at centers in that smaller cube. Taking the minimum over
the common finite set of feasible assignments preserves that Lipschitz
bound. Thus the same good event also gives a local modulus for the
mixed-integer value function and a uniform exact penalty \(2M/d\) on
that smaller neighborhood.

This is local stability of the perturbed instance. It does not transfer
an optimum to the original right-hand side \(b_0\). In the earlier
one-binary chain example, moving \(b\) from zero past
\(\delta_n=2^{-2^n}\) changes the optimum from zero to minus one. A
perturbation large enough to remove the penalty obstruction can cross that
integer-feasibility boundary. Any claimed original-instance transfer
requires an additional robustness or distance certificate.

## Scalar sharpness and a limit on expected numerical size

The numerical dependence on \(K/\epsilon\) cannot be removed in general,
even with a robust feasible slice and scalar residuals.

Take one slice with residual image \([0,1]\) and constant cost zero, and
\(K-1\) slices with singleton residuals \(j/K\), cost minus one,
\(1\leq j\leq K-1\). Here \(K\geq2\), all native sets are compact
convex, all objectives are constant, and \(M=1\). Draw \(B\) uniformly
on \([0,1]\). Except at finitely many points, the primal value is zero.

Fix \(b\in(0,1)\) outside the singleton atoms, and suppose
\(t=|b-j/K|>0\). Mix the singleton point
with any point from the zero-cost slice whose residual relative to \(b\)
has the opposite sign. If the latter residual magnitude is \(s>0\), use
weights \(s/(s+t)\) and \(t/(s+t)\). The mean residual is zero, the
mean cost is \(-s/(s+t)\), and the mean absolute residual is
\(2st/(s+t)\). Therefore, for **every** multiplier, its augmented
subproblem value is at most

\[
 \frac{s}{s+t}(-1+2\rho t).
\]

If \(\rho<1/(2t)\), this is strictly below the primal optimum. Thus the
least penalty for the dual optimized over unrestricted multipliers is at
least \(1/(2t)\). For every \(T\geq K\), the disjoint intervals

\[
 |b-j/K|<1/(2T)\qquad(1\leq j\leq K-1)
\]

lie in \([0,1]\) and have total length \((K-1)/T\). Consequently

\[
 \mathbb P\{\rho^*(B)>T\}\geq\frac{K-1}{T},\qquad T\geq K.
\tag{8}
\]

This matches the order of the high-probability \(K/\epsilon\) numerical
bound in dimension one. The example is an oracle/slice-model sharpness
statement; no compact encoding of an arbitrary family of \(K\) slices
is asserted.

An even smaller example shows why no finite expected numerical penalty
follows. Take the anchor slice \([-1,1]\), cost zero, and one singleton
at zero, cost minus one. For \(b\in(-1,1)\setminus\{0\}\), value
exactness requires and is achieved at

\[
 \rho^*(b)=\frac1{2|b|},\qquad
 \lambda=-\rho^*(b)\operatorname{sign}(b).
\]

Necessity follows from the mixture above. For sufficiency, the anchor's
penalized cost is nonnegative because \(|\lambda|=\rho\), and the
singleton's penalized cost is \(-1+2\rho|b|=0\). Uniform continuous
noise therefore gives \(\mathbb E[\rho^*(B)]=+\infty\), despite a
finite expected logarithm. The finite-grid theorem asserts high
probability only; its exceptional atoms also preclude an automatic
expected-encoding conclusion.

## Prior results and significance assessment

Primary comparisons are recorded separately in
[smoothed-penalty-novelty.md](smoothed-penalty-novelty.md).
The closest existing ingredients include:

- Lefebvre--Schmidt's finite-penalty argument, which treats feasible
  convex integer slices through dual multipliers and infeasible slices
  through positive residual separation.
- Dunagan, Spielman, and Teng, *Smoothed Analysis of Renegar's Condition
  Number for Linear Programming*,
  [open primary manuscript](https://www.cs.yale.edu/homes/spielman/Research/lpcond.pdf).
  Its convex-boundary probability estimates make small distance to
  infeasibility unlikely under perturbations. Its Gaussian formulation
  and conditioning conclusions differ from the explicit rational grid
  and norm-penalty statement here; the broad principle is established.
- Bürgisser and Amelunxen, *Robust Smoothed Analysis of a Condition
  Number for Linear Programming*,
  [version 3 manuscript](https://arxiv.org/pdf/0803.0925v3), Theorem 3.3
  and Corollary 3.4, whose convex-body tube estimates give a further
  direct geometric antecedent. The first version had the title
  *Uniform Smoothed Analysis* and different theorem numbering.

The bounded search does not establish novelty. A positive assessment would
need to rest on the combined finite-grid, finite-integer-union,
penalty-encoding statement and its limitations, not on inventing a new
conditioning principle. The elementary tail example helps identify what
is and is not improved: worst-case exponential encoding can disappear
with high probability, while large numerical penalties and substantial
changes in the original optimizer remain possible.

## Verification record

The main deterministic repair argument was independently derived by the
root agent and by the author; the coordinate-fiber geometric proof was
developed by a separate agent and checked independently. The proof reviewer
also checked the local Lipschitz consequence and all sharpness formulas.
Its only requested main-text correction restricted the multiatom mixture
argument to interior right-hand sides; this has been applied.

The targeted command
`python research-20260925/check_smoothed_penalty_review_second.py`
passed 363 exact piecewise-linear penalty cases, 150 exact box/grid tube
cases, and 1,216 exact optimized-penalty sharpness cases. The checker was
written and first run by the independent reviewer, then rerun by the
author. The geometry reviewer separately checked 187,272 rational clipped
interval cases; the literature reviewer checked 78 threshold cases and
504 balanced mixtures. Those finite calculations check arithmetic,
constants, and representative boundary cases. They do not establish the
uniform convex-set theorem, certify novelty, or test a solver. No Lean
verification, project-wide checks, or CI inspection were performed for
this note.
