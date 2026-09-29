# FPT candidate lists for strongly convex quartics with mixed linear constraints

Date: 2026-09-28. Status: the full proof passed
[fresh independent adversarial review](mixed-linear-strong-quartic-candidate-list-review.md),
including a separate primary-source check of initialization and both
approximation calls. This extends the reviewed
[unconstrained-fiber candidate-list theorem](fixed-integer-strong-quartic-fpt.md).
The new ingredient is a polynomial-time rational cut for a constrained
fiber, including degenerate polyhedra. The root independently derived
the cut and the complementary-slackness estimate that eliminates any
need to bound a particular optimal multiplier. Publication priority is
unestablished.

Consider

\[
 \min\{f(z,y):z\in\mathbb Z^k,\ y\in\mathbb R^n,
                       Az+By\le c\},
\tag{1}
\]

where the constraint data and the coefficients of the degree-at-most-four
polynomial \(f\) are rational. A rational \(\mu>0\) is supplied,
with the promise

\[
                 \nabla^2 f(z,y)\succeq\mu I_{k+n}
                       \quad\text{everywhere}.
\tag{2}
\]

Let \(L\ge2\) denote total explicit binary input length. The number
of continuous variables and constraints is unrestricted.

**Theorem.** There is a deterministic algorithm using ordinary rational
computation, with no PosSLP or other exact nonlinear-comparison oracle,
that either certifies mixed-integer infeasibility or outputs a finite
list of feasible integer blocks containing **every** integer block of
every global optimizer of (1). Its running time and total output length
are at most

\[
                              a(k)L^C,
\tag{3}
\]

for a computable function \(a\) and an absolute constant \(C\).
The polyhedron may be unbounded, deficient dimensional, or have
degenerate or redundant constraints. No Slater assumption is made.

The list may contain nonoptimal blocks. Exact selection among their
constrained continuous fiber minima is a separate task. This theorem
does **not** assert that general constrained quartic value comparison
reduces to one PosSLP query or is deterministically in
\(\mathsf P^{\mathrm{PosSLP}}\). The currently reviewed
[polyhedral exact-comparison bounds](polyhedral-strong-quartic-unambiguous-upper.md)
have different scope from the unconstrained continuous theorem. A
supplied full positive definite rational Hessian Gram can provide (2),
but such a Gram is not required by the promise version above.

## 1. Initialization, attainment, and a box

First find a rational mixed-integer feasible point \(x_0=(z_0,y_0)\),
or certify infeasibility, in deterministic FPT time with parameter \(k\).
One precise primary source suffices for this step: Del Pia,
[*Convex quadratic sets and the complexity of mixed integer convex
quadratic programming*](https://arxiv.org/html/2311.00099v2), Theorem 3,
applied to the constant quadratic objective zero on the given
polyhedron. The feasible case has an attained finite optimum, and the
algorithm returns a rational feasible point. Its encoding length is
bounded by its FPT running time.

If \(k=0\), return the singleton empty integer vector after this
feasibility check. Coercivity guarantees an optimizer in the nonempty
polyhedron, and it necessarily has that integer block. Below assume
\(k\ge1\), as required for the positive-dimensional integer-query
algorithm.

Put \(F_0=f(0)\), \(a_0=\nabla f(0)\), and \(C_0=f(x_0)\).
Define

\[
 T_0=\|a_0\|_1+|C_0-F_0|+1,
 \qquad R=2+\left\lceil2T_0/\mu\right\rceil.
\tag{4}
\]

The strong-convexity inequality
\(f(x)\ge F_0+a_0^{\mathsf T}x+\mu\|x\|^2/2\) shows that
\(f(x)>C_0\) whenever \(\|x\|\ge R\). The original feasible
set is closed and nonempty, and \(f\) is coercive, so a minimum
exists. Every optimizer has its integer block in \([-R,R]^k\).
Only the integer block is truncated; continuous fibers remain subject
to their full original inequalities. The bit length of \(R\) is
\(a_1(k)L^{C_1}\) with an absolute \(C_1\).

Let

\[
 D=\{z\in[-R,R]^k:\exists y, Az+By\le c\},
 \qquad g(z)=\min\{f(z,y):By\le c-Az\}\quad(z\in D).
\tag{5}
\]

The set \(D\) is a compact rational polyhedron. Every nonempty
fiber has a unique minimizer, by coercivity and (2). Partial minimization
makes \(g\) strongly convex on \(D\): apply the joint strong-
convexity inequality to the two fiber minimizers and drop the squared
continuous displacement. Unlike the earlier unrestricted-fiber case,
we do not assume that \(g\) is differentiable or extends as a finite
convex function to all of \(\mathbb R^k\).

## 2. Infeasible fibers give rational projection cuts

At an integer query \(z\), first check the explicit box inequalities.
If they hold, use rational linear programming on
\(By\le c-Az\). In the infeasible case obtain a rational Farkas
certificate

\[
       \alpha\ge0,\qquad B^{\mathsf T}\alpha=0,
                \qquad\alpha^{\mathsf T}(c-Az)<0.
\tag{6}
\]

Then \(\alpha^{\mathsf T}Aw\le\alpha^{\mathsf T}c\) is valid
for the entire projection and strictly violated at \(z\). Rational LP
provides this certificate in polynomial time and bit length in the
query and fixed data. In the feasible case it instead provides a
rational feasible point \(\bar y\) of polynomial encoding length.
No explicit inequality description of the projection is constructed.

## 3. A primal-dual residual gives an integer-valid objective cut

Fix a feasible integer query \(z\). Let \(\widehat y\) be any
rational feasible fiber point, and let \(\lambda\ge0\) be rational.
Define

\[
 \begin{split}
 s&=c-Az-B\widehat y\ge0,\\
 r_y&=\nabla_y f(z,\widehat y)+B^{\mathsf T}\lambda,\\
 E&=\lambda^{\mathsf T}s+\frac{\|r_y\|^2}{2\mu},\\
 q&=\nabla_z f(z,\widehat y)+A^{\mathsf T}\lambda.
 \end{split}
\tag{7}
\]

For every feasible \((w,v)\), joint strong convexity gives a
quadratic lower bound at \((z,\widehat y)\). The multiplier inequality
\(\lambda^{\mathsf T}(A(w-z)+B(v-\widehat y))\le
\lambda^{\mathsf T}s\) and completion of the square in
\(v-\widehat y\) yield

\[
 f(w,v)\ge f(z,\widehat y)+q^{\mathsf T}(w-z)
                +\frac\mu2\|w-z\|^2-E.
\tag{8}
\]

Taking the minimum over \(v\), and using
\(f(z,\widehat y)\ge g(z)\), proves

\[
        g(w)-g(z)\ge q^{\mathsf T}(w-z)
                           +\frac\mu2\|w-z\|^2-E.
\tag{9}
\]

If \(E\le\mu/4\), every distinct feasible integer block \(w\)
has \(\|w-z\|\ge1\), and hence

\[
          g(w)-g(z)\ge q^{\mathsf T}(w-z)
                              +\frac\mu4\|w-z\|^2.
\tag{10}
\]

Consequently \(q=0\) certifies that \(z\) is the unique optimal
integer block in the full feasible projection. Otherwise the rational
inequality

\[
                         q^{\mathsf T}(x-z)\le-\mu/4
\tag{11}
\]

strictly excludes its query and retains every other feasible integer
block with objective no greater than the query's value. Equation (8)
is a Lagrangian strong-convexity lower bound; no novelty is claimed for
that general lower-bound technique. The application requires an ordinary
polynomial-time construction of the small residual in (7), which we
give next.

## 4. Constructing the residual certificate without a Slater point

Assume \(n\ge1\); if \(n=0\), exact rational evaluation of
\(\nabla_z f\) already supplies (10). Write
\(h(y)=f(z,y)\), and let \(p\) be its minimizer over the fiber.
From the rational feasible \(\bar y\) in Section 2 compute

\[
 A_z=\|\nabla h(0)\|_1+|h(\bar y)-h(0)|+1,
 \qquad Y=2+\left\lceil2A_z/\mu\right\rceil.
\tag{12}
\]

The same coercive inequality as before gives \(\|p\|<Y\). All
quantities have polynomial bit length in the query and the fixed data.
Let \(m=k+n\), \(C=\max\{1,\sum_\gamma|f_\gamma|\}\), and set

\[
 S=2+R+Y,\qquad G=1+4mCS^3,\qquad K=1+12mCS^2.
\tag{13}
\]

Then \(\|\nabla h(p)\|\le G\), and the operator norm of
\(\nabla^2h\) is at most \(K\) throughout the unit neighborhood
of \(p\). These follow by differentiating the explicit quartic and
bounding the coefficient sums. Put

\[
 \delta=\min\left\{1,\frac{\mu}{16(G+1)},\frac{\mu}{4K}\right\}.
\tag{14}
\]

Ordinary convex polynomial approximation returns a rational feasible
\(\widehat y\) with

\[
                  h(\widehat y)\le h(p)+\mu\delta^2/2.
\tag{15}
\]

Use Slot--Steurer--Wiedmer,
[*Hesse's Redemption*](https://arxiv.org/html/2511.03440v1), Corollary 1.2.
It returns an actual feasible rational point on a rational polyhedron;
the requested accuracy has polynomial encoding length. Since \(p\)
minimizes a differentiable convex function on the fiber,
\(\nabla h(p)^{\mathsf T}(\widehat y-p)\ge0\). Strong convexity
and (15) therefore imply \(\|\widehat y-p\|\le\delta\).

Polyhedral first-order optimality gives a multiplier \(\lambda_*\ge0\)
such that

\[
 \nabla h(p)+B^{\mathsf T}\lambda_*=0,
 \qquad\lambda_*^{\mathsf T}(c-Az-Bp)=0.
\tag{16}
\]

No constraint qualification is needed: the normal cone of a polyhedron
is generated by the normals of its active inequalities, even on a
deficient-dimensional face. Equalities may be represented by two
opposite inequalities. Formula (16) asserts existence of a real
multiplier; the construction never computes it or assumes it rational.

The key estimate avoids any bound on \(\|\lambda_*\|\). With
\(s=c-Az-B\widehat y\), complementary slackness and stationarity
give the exact identity

\[
 0\le\lambda_*^{\mathsf T}s
     =\nabla h(p)^{\mathsf T}(\widehat y-p)
     \le G\delta.
\tag{17}
\]

Also
\(\|\nabla h(\widehat y)+B^{\mathsf T}\lambda_*\|
 =\|\nabla h(\widehat y)-\nabla h(p)\|\le K\delta\).
Thus the convex quadratic function of \(\lambda\)

\[
 \mathcal E(\lambda)=s^{\mathsf T}\lambda+
       \frac{\|\nabla h(\widehat y)+B^{\mathsf T}\lambda\|^2}{2\mu}
\tag{18}
\]

satisfies

\[
 \min_{\lambda\ge0}\mathcal E(\lambda)
 \le \mathcal E(\lambda_*)
 \le G\delta+\frac{K^2\delta^2}{2\mu}
 \le\frac{3\mu}{32}.
\tag{19}
\]

Its input is rational of polynomial length: \(s\),
\(\nabla h(\widehat y)\), \(B\), and \(\mu\) are known
rationals. It is globally convex and nonnegative on the nonempty
orthant. Its minimum is attained even if its multiplier sublevels are
unbounded: the image
\(\{(B^{\mathsf T}\lambda,s^{\mathsf T}\lambda):\lambda\ge0\}\)
is a closed polyhedral cone, and the objective
\(t+\|\nabla h(\widehat y)+u\|^2/(2\mu)\) has a nonempty compact
sublevel in the image coordinates \((u,t)\), since \(t\ge0\).
An image minimizer lifts to a nonnegative multiplier. This attainment
argument was supplied by the independent reviewer and rechecked by the
author. Solve this ordinary rational convex quadratic problem to
additive error at most \(\mu/8\), again using convex polynomial
approximation, or using the classical exact convex QP algorithm.
The resulting rational \(\widehat\lambda\ge0\) obeys

\[
        E=\mathcal E(\widehat\lambda)\le7\mu/32<\mu/4.
\tag{20}
\]

It therefore supplies (7)--(11). No active set has been guessed or
identified, and the encoding size of a particular exact multiplier is
irrelevant. Only two ordinary convex approximations and rational linear
programming were needed. Degenerate active constraints can make
\(\lambda_*\) nonunique, but do not affect (17) or (19).

## 5. Applying the integer-query algorithm

Use the deterministic integer-query feasibility theorem stated precisely
in Section 1 of the reviewed
[FPT candidate-list note](fixed-integer-strong-quartic-fpt.md), with
radius \(R\). Initialize the candidate list with \(z_0\).
At every query outside the box or with an infeasible fiber, return the
box or Farkas cut. At every other query, append its integer block,
construct \(q\) by Section 4, and return (11). If \(q=0\), stop
instead, since that recorded block is the unique integer optimum.
Never send a membership confirmation to the feasibility algorithm.
All procedures and tie choices can be made deterministic and depend
only on the fixed data and the query; no incumbent value is used.

The answer routine has polynomial bit complexity in \(L\),
\(\langle R\rangle\), and the query length. Rational LP produces
short feasible or Farkas data. The bounds (12)--(14), the two convex
approximations, and the rational cut then have polynomial size and cost
with absolute exponents. No affine lattice parametrization changes this
oracle's input: the feasibility theorem queries it in original integer
coordinates. Combining this bound with (4) of the earlier note gives
\(a(k)L^C\) total time, including the initial feasible-witness step.

Termination and optimizer retention use exactly the reviewed
empty-set and singleton arguments. Every returned cut is a strict
separator of its query and vacuously valid for the fixed empty set.
A possible zero-normal early stop is viewed as a prefix of an empty-set
oracle completed by an arbitrary strict separator. Thus the ordinary
FPT feasibility bound proves termination without exact value comparisons.

If an optimal integer block \(w\) were omitted, complete the same
oracle by accepting exactly \(w\). All other answers remain valid
for \(\{w\}\): domain cuts retain it, and (10) retains it at every
different feasible query, including a tied optimum. A zero normal is
impossible at a different query. This fixed singleton oracle has the
same polynomial answer bound, since \(w\) has \(O(k\langle R\rangle)\)
bits. The actual run never queried \(w\), so its identical transcript
would falsely certify singleton emptiness. Every optimal block is in
the list.

The number of optimal blocks is at most \(2^k\). Two distinct optimal
integer blocks of the same parity would have an integer midpoint;
averaging their continuous optimizers preserves all linear constraints,
and joint strict convexity produces a smaller objective. This parity
bound is elementary and sharp, as in the earlier note.

## 6. Exact selection and the strongest prior comparison

All candidates have nonempty rational polyhedral fibers and a unique
continuous minimizer. A rational threshold test for the original optimum
is the disjunction of the corresponding constrained fiber tests.
Pairwise comparisons can be expressed by a separable sum of two fiber
objectives and a difference observable on the product polyhedron.
Thus any applicable exact constrained-fiber comparison oracle can be
used nonadaptively after list construction. Its precise complexity must
be carried into the resulting full algorithm; the candidate theorem
does not by itself make that oracle polynomial time.

The reviewed unambiguous constrained upper bound and the separately
reviewed
constraint-rank algorithm concern this remaining continuous selection
step. Their combinations with the present theorem should be stated and
reviewed separately. In particular, the rank of the continuous matrix
in a pairwise product fiber is at most \(2\operatorname{rank}(B)\),
but no rank-dependent exact-selection theorem is proved in this note.

Del Pia's Theorem 3 already gives ordinary deterministic exact FPT
convex mixed-integer **quadratic** optimization under arbitrary mixed
linear constraints, without strong curvature. The present theorem uses
that established result only for initial linear feasibility. It concerns
quartic objectives and gives an ordinary FPT list containing all optimal
integer blocks, while leaving nonlinear exact selection explicit.
It neither subsumes Del Pia's theorem nor shows ordinary FPT exact
quartic optimization. Del Pia's Section 4.4 explains why a projected
value oracle alone does not automatically implement the requisite
integer-convex optimization oracles.

The geometric search is the established Basu/Hildebrand--Göß integer-
query framework; its non-bisection optimization precedent is credited
in the earlier note. The residual inequality (8) is a standard
Lagrangian lower-bound argument. The proposed contribution is their
complete quantitative combination for arbitrary-dimensional constrained
quartic fibers, using exact rational feasible approximations and a
convex quadratic multiplier problem without Slater or active-set data.
Priority remains subject to further literature comparison, including
inexact generalized Benders and value-function oracle formulations.

The [independent review](mixed-linear-strong-quartic-candidate-list-review.md)
reconstructed the new primal-dual construction, including lower-
dimensional fibers, ties, redundant constraints, and unbounded optimal
multiplier sets. A separate reader checked Del Pia's initialization
theorem and the actual-feasible-point guarantees of the two ordinary
convex approximation calls. The reviewer requested the explicit
\(k=0\) dispatch above; the author independently checked that correction.

Targeted author command actually run:

```text
python research-20260927/check_mixed_linear_candidate_cut.py
```

It passed 66 exact constrained-fiber cases with rescaled active normals,
equality fibers, redundant multipliers, Farkas projection cuts, and the
residual constants. One case has multiplier \(10^{100}\) while the
residual bound stays independent of that norm. The separate reviewer
checker passed 4,240 residual certificates, 26,480 primal-dual
inequalities, 22,240 integer margin checks, 1,360 Farkas certificates,
and 540 nonempty candidate-list simulations retaining all optimizers.
These finite checks challenge the construction; they do not implement
the general FPT algorithm or establish its running time. No implementation
speedup, Lean formalization, project-wide verification, or CI inspection
is claimed.
