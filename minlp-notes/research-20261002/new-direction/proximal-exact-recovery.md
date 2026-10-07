# Exact quadratic recovery without isolated optimizers

Date: 2026-10-02. Status: complete exact-recovery extension of the
[proximal growth-grid theorem](proximal-growth-grid.md). A
[fresh adversarial review](proximal-exact-recovery-adversary.md), with a
second independent reviewer, found no substantive gap. Targeted
exact-arithmetic examples pass. This note makes no literature-priority
claim.

For a rational mixed-integer box quadratic program, a sufficiently accurate
point near the optimal set determines a face on which linear stationarity
equations recover an exact optimizer. The optimal set may contain a
continuum. Neither its cardinality nor the number of its connected
components is a parameter.

The resulting fixed-parameter algorithm **requires a supplied valid growth
bound**. Its objective interval and exactness guarantee depend on that
promise. The final rational checks do not turn it into the
growth-independent certificate of the unique-optimizer pruned-grid theorem.

## 1. Model and conclusion

Consider

\[
 F(x)=x^TQx+b^Tx+a,\qquad x\in X=\prod_{i=1}^n X_i,
 \tag{1}
\]

where \(Q\) is symmetric, all data are rational, and each \(X_i\) is a
bounded closed interval \([\ell_i,r_i]\) or its intersection with the
integers. Round
integer endpoints inward, reject empty domains, and eliminate fixed
coordinates. Substitution can introduce new coefficient denominators;
all constants below refer to the resulting quadratic and its original,
unrefined box. The case with no remaining coordinate is immediate, so
assume \(n\ge1\).

Supply a tree decomposition of the quadratic factors with largest bag
size \(p\). Let \(I\) include the rational data, the decomposition, and
the supplied parameters. A known rational \(L>0\) bounds the upper
coordinate curvature. Write

\[
 f^*=\min_XF,\qquad S=\operatorname*{argmin}_X F.
\]

The nonempty optimal set \(S\) is compact. Supply a rational
\(\kappa\ge1\) for which

\[
 F(x)-f^*\ge\frac L\kappa\operatorname{dist}(x,S)^2
       \qquad(x\in X).
 \tag{2}
\]

Thus \(L/\kappa\) is a trusted positive lower bound on the growth
constant. No uniqueness or isolation assumption is imposed.

**Theorem.** Under (2), the proximal growth-grid algorithm followed by one
rational linear-feasibility problem returns an exact rational optimizer
and its exact value in

\[
 f(p,\kappa)(I+1)^C
 \tag{3}
\]

bit operations for an absolute constant \(C\). The additional recovery
problem has polynomial bit complexity and does not enumerate integer
assignments or optimal components.

Some positive constant in the set-growth inequality exists for every
bounded quadratic program over a polytope, by Luo and Sturm,
*Error Bounds for Quadratic Systems*, Theorem 3.3 (manuscript p. 11;
published chapter pp. 383--404, 2000;
[verified primary source](../../literature/papers/luo2000-error-bounds-for-quadratic-systems/paper.md)).
The finite-slice argument in
[the approximation note](proximal-growth-grid.md) extends that classical
qualitative fact to bounded mixed boxes. It does not provide the valid
numerical `kappa` required in (2), nor a polynomial bound on its size.
The recovery algorithm and its exactness guarantee continue to depend
on the supplied quantitative promise.

## 2. Arithmetic constants from the unrefined problem

Choose a common positive integer denominator \(D\) of every entry of
\(Q,b,a\) and every box endpoint, after the preprocessing above. Account
for factors of two when converting off-diagonal monomials to a symmetric
matrix. Set

\[
 B=DQ,\qquad C_0=\max\{1,\max_{i,j}|B_{ij}|\},\qquad
 H=(2nC_0)^n,
 \tag{4}
\]

and

\[
 R=DH,\qquad V=DR^2=D(DH)^2,\qquad
 \tau=\frac1{4nDH}.
 \tag{5}
\]

These quantities have polynomial binary length. Their numerical values
are not enumerated.

The minimum-face height argument in
[the rational box-QP note](../geometric-dp/exact-box-qp.md) proves that
some optimizer has a common coordinate denominator at most \(R\), and
that \(f^*\) has reduced denominator at most \(V\), even when \(S\)
is not discrete. In brief, fix an optimal integer assignment and choose
an optimizer on a continuous-box face of minimum dimension. Its free
Hessian is nonsingular: a null direction would preserve the objective
until reaching a smaller face. In the scaled coordinates \(u=Dx\),
the free equations have integral matrix \(2B_{JJ}\) and integral
right-hand side. Their determinant has magnitude at most \(H\).
Cramer's rule and substitution into (1) give \(R\) and \(V\).

The same determinant bound also controls vertices of stationary
polytopes whose free Hessian is singular. That second use of \(H\)
provides the recovery argument below.

## 3. A nearby feasible point identifies a recoverable face

**Recovery lemma.** Suppose \(y\in X\) satisfies

\[
 \operatorname{dist}(y,S)\le\tau/2.
 \tag{6}
\]

Fix every integer coordinate to its value in \(y\). For each continuous
coordinate, fix it to its lower bound if \(y_i\) is within \(\tau\)
of that bound, and fix it to its upper bound if it is within \(\tau\)
of that bound. Leave every other continuous coordinate free. Let \(J\)
be the remaining free coordinates. The linear system

\[
 \nabla_J F(x)=0
 \tag{7}
\]

together with these fixed values and the original box has a feasible
solution. Every such solution is a global optimizer.

The selection is unambiguous even for very narrow original intervals.
Every positive interval width is at least \(1/D\), whereas
\(2\tau\le1/(2D)<1/D\). Hence a coordinate cannot be selected at both
bounds. Fixed singleton coordinates were already removed.

*Proof.* Choose a nearest optimizer \(s\in S\), which exists by
compactness. Every integer coordinate agrees between \(y\) and \(s\),
because their Euclidean distance is less than one. Let \(A\) be the
continuous coordinates at a bound in \(s\), and let \(J_0\) be its
strictly interior continuous coordinates. Every coordinate in \(A\)
is selected at its correct bound, since its distance from \(y\) is at
most \(\tau/2\). Thus \(J\subseteq J_0\).

Fix the integer coordinates and the coordinates in \(A\) to their
values in \(s\), and consider the polytope

\[
 P=\{x\in X:\ x_A=s_A,\ x_{\rm int}=s_{\rm int},\quad
                       \nabla_{J_0}F(x)=0\}.
 \tag{8}
\]

It is nonempty, since first-order optimality at \(s\) gives the free
stationarity equations. Every point of \(P\) is optimal. Indeed, for
\(x\in P\), the displacement \(v=x-s\) is supported on \(J_0\),
and subtracting the stationarity equations gives
\(Q_{J_0J_0}v_{J_0}=0\). The exact quadratic expansion therefore yields

\[
 F(x)-F(s)=\nabla F(s)^Tv+v^TQv=0.
 \tag{9}
\]

Let \(E\subseteq J_0\) contain the extra continuous coordinates
selected at bounds by the rule based on \(y\). Define \(q(x)\) to be
the sum of their nonnegative slacks to their selected bounds:
use \(x_i-\ell_i\) for a selected lower bound and \(r_i-x_i\) for a
selected upper bound. At \(s\), every such slack is at most
\(\tau+\tau/2\). Consequently

\[
 0\le q(s)\le\frac{3n\tau}{2}=\frac3{8DH}<\frac1{DH}.
 \tag{10}
\]

We claim that \(\min_Pq=0\). To prove it, scale to \(u=Dx\).
All fixed-coordinate and box bounds now have integral right-hand sides.
The stationarity rows have the form

\[
 2B_{J_0J_0}u_{J_0}
   =-D^2b_{J_0}-2B_{J_0,A\cup{\rm int}}u_{A\cup{\rm int}}.
 \tag{11}
\]

Their coefficients and right-hand sides are integral. A vertex of this
nonempty bounded polytope is determined by independent stationarity and
bound rows. Those rows have entries of magnitude at most \(2C_0\).
For at most \(n\) free variables, the determinant expansion bounds
the magnitude of the resulting nonzero determinant by \(H\).
Hence every vertex has one common denominator at most \(H\) in the
\(u\) coordinates.

The linear function \(q\) attains its minimum at such a vertex. In
\(u\) coordinates, \(Dq\) has integral coefficients and integral
constant term. A positive minimum would therefore be at least
\(1/(DH)\), contradicting (10). This also covers a zero-dimensional
polytope, using determinant one. Thus \(P\) contains an optimizer
\(s'\) meeting every selected bound.

Because \(J\subseteq J_0\), this \(s'\) satisfies (7) and all fixed
values, proving feasibility. Finally, let \(x\) be any feasible
solution to the selected-face system. The vector \(x-s'\) is supported
on \(J\), and subtracting their stationarity equations gives
\(Q_{JJ}(x-s')_J=0\). The same expansion as (9) proves
\(F(x)=F(s')=f^*\). This last argument needs no positive-definiteness
or nonsingularity assumption on \(Q_{JJ}\). QED.

## 4. The complete exact algorithm

Choose the largest dyadic target accuracy \(\varepsilon=2^{-q}\), with
integer \(q\ge0\), satisfying

\[
 \varepsilon\le
 \min\left\{1,\frac{L\tau^2}{4\kappa},\frac1{4V^2}\right\}.
 \tag{12}
\]

Run the proximal growth-grid algorithm with the supplied \(\kappa\)
until it returns a feasible point \(y\) and its promise-valid rational
interval

\[
 \ell\le f^*\le U=F(y),\qquad U-\ell\le\varepsilon.
 \tag{13}
\]

By (2) and (12), this point satisfies (6). The recovery lemma therefore
applies directly; no optimizer or optimal component has to be chosen by
the algorithm.

Reconstruct the unique rational of denominator at most \(V\) in
\([\ell,U]\), using rational reconstruction. It exists by the height
bound and equals \(f^*\). Uniqueness follows because two distinct
rationals with denominators at most \(V\) differ by at least
\(1/V^2\), which exceeds the interval length in (12).

Apply the bound-selection rule of Section 3 to \(y\), then solve (7)
and the remaining box constraints by rational linear programming. This
is linear feasibility; it does not ask a solver to minimize an indefinite
quadratic. Return a rational feasible solution \(\widehat x\) only
after checking its original box membership, required integrality, and
exact equality

\[
 F(\widehat x)=\widehat f,
 \tag{14}
\]

where \(\widehat f\) is the reconstructed value. Under the stated
promise, feasibility and equality are guaranteed by the recovery lemma.
These final checks establish consistency of the reconstructed output.
They do not validate (2), and a false supplied growth bound can invalidate
the global interval (13).

## 5. Complexity and scope

The required accuracy has

\[
 \log(1/\varepsilon)=\operatorname{poly}(I)+O(\log\kappa)
 \tag{15}
\]

when an accuracy exponent below zero is replaced by zero. The height
constants and \(\tau\) have polynomial binary length. The known
rational \(L\) has input-bounded binary length. The proximal theorem
therefore reaches (13) in the bound (3).

The subsequent comparisons, rational reconstruction, and linear program
have polynomial bit complexity. The linear program uses the original
quadratic coefficients, original continuous bounds, and integer values
whose sizes are bounded by the original integer domains. No approximate
continuous grid coordinate is substituted into its coefficients. A
rational feasible solution of polynomial encoding length can be returned.

The argument applies to arbitrary optimal sets of rational box QPs,
including unions of flat optimal faces. It does not extend the linear
recovery step to general nonlinear factor objectives or coupled feasible
constraints. It also does not provide an algorithm that can safely stop
without a valid supplied conditioning bound.

## 6. Targeted verification

An independent mathematical review checked the stationary-polytope
argument, common vertex denominators, integer agreement, tiny interval
widths, and the selected-face feasibility argument. It found no gap.
The fresh adversarial review linked above independently checked the
completed proof and its integration with the proximal algorithm. Its
exact-arithmetic verification passed 37 snapping cases, 112 stationary
polytope vertices, and 20 extra bound snaps.

An inline `python3 - <<'PY'` exact-arithmetic check, run with
`fractions.Fraction`, passed 16 recovery cases across eight quadratic
families. Cases included flat segments, disconnected flat components,
mixed integer assignments, bilinear corner minima, and linear optimal
faces. The check perturbed known optimizers within the stated radius,
selected bounds, solved the small stationary systems by exact vertex
enumeration, and compared the returned objective to the exact optimum.
This checks the recovery step; it is not an implementation of the full
proximal-grid algorithm or a performance claim for vertex enumeration.

The targeted document commands were
`git diff --check -- research-20261002/new-direction/proximal-exact-recovery.md`
and an inline `python3 - <<'PY'` check of trailing whitespace, paired
math delimiters, all local links, and the stated height and precision
constants. Both passed.

No external search, project-wide verification, or CI inspection was
performed.
