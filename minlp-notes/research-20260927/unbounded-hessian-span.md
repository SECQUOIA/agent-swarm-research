# A small feasible point from bounded Hessian span

Date: 2026-09-27. Status: proof and two independent adversarial reviews
completed. Publication priority remains unestablished.

A nonempty rational convex quadratic system has a feasible point of
polynomial coordinate bit magnitude when the span of its Hessian matrices
has fixed dimension. Explicit continuous variable bounds are unnecessary.
The point itself can be irrational. This extends the present batch's
Hessian-span results from bounded to unbounded continuous domains and removes
the continuous-box assumption from its exact MILP integer-projection theorem.

The proof modifies [the value-height argument](hessian-span-reduction.md):
minimize the squared Euclidean norm, and use its coercivity in place of the
input box. No constraint qualification is imposed on the original system.

## 1. Small-point theorem

Let

\[
 S=\{x\in\mathbb R^n:Ax\le b,\ Ex=e,\ q_i(x)\le0
                  \ (i=1,\ldots,m)\},
 \qquad
 q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i,
 \qquad Q_i\succeq0.
\]

All data are rational. Let \(N\ge2\) be the total explicit binary input
length, including dimensions and all listed coefficients, and put

\[
 h=\dim_{\mathbb Q}\operatorname{span}\{Q_1,\ldots,Q_m\}.
\]

**Theorem.** If \(S\ne\varnothing\), its minimum-norm point \(x^*\)
exists, and

\[
 \theta:=\|x^*\|_2^2
\]

satisfies a nonzero integer polynomial whose degree and coefficient bit
lengths are at most \(N^{C(h+1)}\), for an effective absolute constant
\(C\). After increasing \(C\) if needed,

\[
 \|x^*\|_2\le 2^{N^{C(h+1)}}.                    \tag{1}
\]

Thus one can compute an integer radius \(R\) with
\(\log_2 R\le N^{O(h+1)}\) such that

\[
 S\ne\varnothing
 \quad\Longleftrightarrow\quad
 S\cap[-R,R]^n\ne\varnothing.                    \tag{2}
\]

The radius is uniform over all inputs of the stated length and parameter.
Computing it uses an effective sufficiently large constant from quantitative
elimination; no active constraints or feasible point need to be known. This
is an asymptotic algorithmic bound, not a calibrated practical radius.

### 1.1 Existence and the active affine restriction

The set \(S\) is closed. For any \(\bar x\in S\), intersecting \(S\)
with the closed ball of radius \(\|\bar x\|_2\) gives a nonempty compact
set. Therefore \(\|x\|_2^2\) attains its minimum on \(S\). Strict
convexity also makes its minimizer unique, although uniqueness is not needed
for the algebraic bound.

Fix a minimizer \(x^*\). Keep every affine equality, turn affine
inequalities active there into equalities, and delete all other affine
inequalities. Keep precisely the native quadratic inequalities active there.
The resulting problem has the same minimum norm: any retained feasible point
with a smaller norm squared would, by convexity and the deleted rows' strict
slack at \(x^*\), give a better original point on a sufficiently short
segment from \(x^*\).

Let \(I\) be the retained quadratic indices. Choose
\(B\subseteq I\), \(|B|=s\le h\), whose Hessians form a basis of the
retained Hessian span. For each \(i\in I\), rational linear algebra gives

\[
 Q_i=\sum_{j\in B}c_{ij}Q_j.
\]

The polynomial \(q_i-\sum_{j\in B}c_{ij}q_j\) is affine and vanishes
at \(x^*\). Add all these affine equations. This restriction retains
\(x^*\), so it retains the minimum. Parameterize their affine solution
space, together with the previously retained affine equations, as

\[
 x=x_0+Vu,\qquad u\in\mathbb R^d,
\]

where \(V\) has full column rank. A rational parameterization with
coefficient bit lengths polynomial in \(N\) follows from determinant bounds
for linear elimination. The same bounds apply to the \(c_{ij}\). Their
construction depends on which rational rows were selected, but their bit
bounds do not depend on the unknown coordinates of \(x^*\).

Write \(\widetilde q_i(u)=q_i(x_0+Vu)\). These restricted convex
quadratics satisfy the polynomial identities

\[
 \widetilde q_i=\sum_{j\in B}c_{ij}\widetilde q_j,
 \qquad
 \nabla\widetilde q_i=\sum_{j\in B}c_{ij}
                              \nabla\widetilde q_j.     \tag{3}
\]

If \(d=0\), the selected point is rational with polynomial bit length,
and the theorem follows directly. Assume \(d>0\). The objective

\[
 \widetilde q_0(u)=\|x_0+Vu\|_2^2
\]

has Hessian \(Q_0=2V^TV\succ0\). In particular, it is coercive. No
auxiliary ball and no perturbation of the objective are needed.

### 1.2 Regularization needs an existing bound, not an encoded bound

For \(0<\varepsilon<1\), let

\[
 \theta_\varepsilon=
 \min\{\widetilde q_0(u):
                \widetilde q_i(u)\le\varepsilon\ (i\in I)\}.
                                                               \tag{4}
\]

The parameter \(u^*\) of \(x^*\) is strictly feasible. Coercivity gives
an optimizer \(u_\varepsilon\), and

\[
 \widetilde q_0(u_\varepsilon)\le
 \widetilde q_0(u^*)=\theta.                            \tag{5}
\]

Consequently all these optimizers belong to one compact sublevel set of
\(\widetilde q_0\). The number \(\theta\) in (5) is not yet bounded
or known numerically; neither is needed to establish compactness. Every
sequence \(\varepsilon\downarrow0\) has a convergent subsequence of
optimizers. Its limit satisfies all retained rows at right-hand side zero,
so it has objective at least \(\theta\). Together with (5), this proves

\[
 \theta_\varepsilon\longrightarrow\theta
            \quad\text{as }\varepsilon\downarrow0.      \tag{6}
\]

This use of an unknown norm bound is not circular. The number \(\theta\)
does not occur as a coefficient in the formulas below; it appears only in
the existence and convergence proof.

Slater's condition holds for each relaxed problem (4), so a KKT certificate
exists. Its native multipliers affect stationarity only through
\(\eta=\sum_{i\in I}\lambda_i c_i\in\mathbb R^s\), by (3).
Conic Caratheodory applied to the currently active rows replaces those
multipliers by nonnegative multipliers supported on at most \(s\le h\)
active rows. The contribution to stationarity is unchanged, and
complementarity is preserved because only active rows are used.

### 1.3 Elimination and coefficient bounds

Along some sequence \(\varepsilon\downarrow0\), one multiplier support
\(J\subseteq I\), \(|J|\le h\), occurs infinitely often. Fix it. Write
the restricted polynomials as
\(\widetilde q_i(u)=\tfrac12u^TQ_iu+a_i^Tu+c_i^0\), including the
objective \(i=0\). For \(\lambda\ge0\), put

\[
 M=Q_0+\sum_{i\in J}\lambda_iQ_i\succ0,\qquad
 \Delta=\det M>0,\qquad
 p=-\operatorname{adj}(M)\left(a_0+\sum_{i\in J}\lambda_i a_i\right).
\]

Stationarity is equivalent to \(u=p/\Delta\). The following polynomial
system, denoted \(\mathcal K_J(\varepsilon,w,\lambda)\), encodes KKT:

\[
 \lambda_i\ge0\ (i\in J),\qquad \Delta>0,
\]
\[
 G_i:=\tfrac12p^TQ_ip+\Delta a_i^Tp+
                     (c_i^0-\varepsilon)\Delta^2\le0\quad(i\in I),
\]
\[
 \lambda_iG_i=0\quad(i\in J),\qquad
 G_0:=\tfrac12p^TQ_0p+\Delta a_0^Tp+(c_0^0-w)\Delta^2=0.
                                                               \tag{7}
\]

Every original retained row is present in (7), including rows outside the
multiplier support. For \(0<\varepsilon<1\), every solution therefore has
\(w=\theta_\varepsilon\), by KKT sufficiency for convex optimization.
The selected support subsequence supplies solutions approaching the original
minimum. Hence the formula in the single free variable \(a\),

\[
 \forall\gamma\;\left[\gamma\le0\ \lor\
 \exists\varepsilon,w,\lambda:\quad
 0<\varepsilon<1,\quad\varepsilon<\gamma,\quad
 -\gamma<w-a<\gamma,\quad
 \mathcal K_J(\varepsilon,w,\lambda)\right],          \tag{8}
\]

defines exactly \(\{\theta\}\).

The formula has two quantifier blocks: one universal variable and at most
\(h+2\) existential variables. All input polynomials in (7) have degree
\(O(n+1)\), there are polynomially many of them, and their coefficient bit
lengths are polynomial in \(N\). To check the last assertion, first clear
the polynomially many restricted input denominators with one common positive
denominator of polynomial bit length. Determinant and adjugate coefficients
sum at most factorially many products of at most \(d\) entries, each with
at most \(|J|+1\) terms. Their logarithmic coefficient bounds are therefore
polynomial in \(N\). The denominators of the expanded expressions divide
a fixed \(O(d)\)-th power of that common denominator. Clearing them does
not require multiplying a separate denominator for every expanded monomial.

The coefficient-sensitive, fixed-block quantifier-elimination theorem of
Basu--Pollack--Roy, Theorem 14.16, yields a formula in \(a\) whose degrees
and coefficient bit lengths are \(N^{O(h+1)}\). This is also stated as
Theorem 2.27 in
[Basu's survey](https://arxiv.org/abs/1409.1534). The same precise theorem
and bit estimates are used in the [bounded value proof](hessian-span-reduction.md).
The possibly large number of supports or affine active sets is irrelevant:
one fixed formula with the stated bounds proves that a small annihilator
exists. The radius computation does not enumerate those sets.

After removing identically zero polynomials from the eliminated formula,
some remaining integer polynomial must vanish at \(\theta\). Otherwise
all its polynomial signs would be locally constant, contradicting that (8)
defines a singleton. If that polynomial has coefficient bit length \(H\),
the elementary upper Cauchy root bound gives

\[
 0\le\theta\le1+2^H.
\]

Together with \(H\le N^{O(h+1)}\), this proves (1) and (2).

### 1.4 A second proof of the radius using established sampling

The radius bound alone also follows from Grigoriev--Pasechnik's
[Theorem 1.2](https://arxiv.org/pdf/cs/0403008v3), independently of the
KKT elimination. After Section 1.1, consider

\[
 Z=\{u:\widetilde q_j(u)=0\ (j\in B)\}.
\]

This variety contains \(u^*\). Every point of \(Z\) satisfies every
retained quadratic, by (3), and therefore

\[
 u\in Z\quad\Longrightarrow\quad
 \|x^*\|_2\le\|x_0+Vu\|_2.                         \tag{9a}
\]

For \(s\ge1\), apply that sampling theorem to the quadratic map
\((\widetilde q_j)_{j\in B}\) and \(p(Y)=\sum_jY_j^2\), after
clearing rational denominators. It produces a point of \(Z\) represented
as \(u_i=g_i(\alpha)/g_0(\alpha)\), where \(f(\alpha)=0\),
\(f,g_0\) are coprime, and all these univariate polynomials have degree
and coefficient bit length \(N^{O(h+1)}\). In the case \(s=0\), take
\(u=0\) instead.

For each coordinate, the resultant

\[
 \operatorname{Res}_T(f(T),g_0(T)Y-g_i(T))
\]

is nonzero because \(f\) and \(g_0\) are coprime. It vanishes at
\(Y=u_i\), and determinant coefficient bounds keep its degree and
coefficient bit length at \(N^{O(h+1)}\). The upper Cauchy root bound
therefore bounds the sampled coordinates, and hence \(\|x_0+Vu\|_2\),
by \(2^{N^{O(h+1)}}\). Equation (9a) gives the claimed radius.

The sampled point need not satisfy the deleted inactive rows. It is used
only to bound the norm of the original feasible minimizer. This second proof
establishes (1)--(2); it does not on its own establish the annihilating
polynomial assertion for \(\theta\). The sampling theorem's statement,
including its coefficient bound and its definition of real univariate
representations, was inspected directly in the linked author text.

## 2. Exact continuous feasibility without a box

Append the box from (2), then apply
[the bounded exact-feasibility algorithm](hessian-span-exact-feasibility.md).
The box is affine, so it does not increase \(h\). Its full binary encoding
length, including one bound for every coordinate, is \(N^{O(h+1)}\).
Using the bounded algorithm as a black box gives the conservative bound

\[
 N^{O((h+1)^2)}                                      \tag{9}
\]

bit operations. Thus exact feasibility is polynomial for every fixed
Hessian-span dimension, with arbitrary continuous dimension, any number of
affine and quadratic rows, and no Slater assumption. Keeping coefficient
height separate from dimensions in the two successive elimination estimates
may sharpen (9); no sharper exponent is needed or claimed here.

This remains a decision statement. It does not assert a rational exactly
feasible point, a minimal polynomial for each coordinate, or an algorithm
that discovers the active set used in the radius proof.

## 3. Bounded integer variables and unbounded continuous variables

Consider variables \((z,x)\in\mathbb Z^k\times\mathbb R^n\), rational
affine rows, rational total-degree-two inequalities \(q_i(z,x)\le0\), and
explicit finite rational coordinate bounds on \(z\). Assume initially only
that every \(xx\) Hessian block is PSD, and define

\[
 h=\dim_{\mathbb Q}\operatorname{span}
                      \{\nabla^2_{xx}q_i\}.
\]

Every allowed integer assignment has polynomial bit length in the original
input length \(N\). Substituting any such \(z\) gives a rational convex
quadratic system in \(x\), with coefficient and total input bit lengths
bounded by one fixed polynomial in \(N\), uniformly over all assignments.
Total degree two makes the \(xx\) Hessian blocks independent of \(z\),
so their span dimension remains at most \(h\).

Apply the theorem with that uniform substitution-length bound. It gives one
integer \(R=2^{N^{O(h+1)}}\), computable before any integer assignment is
selected, such that

\[
 \{z\text{ in its input box}:\exists x\ q_i(z,x)\le0,
                                  \text{ affine rows}\}
 =
 \{z\text{ in its input box}:\exists x\in[-R,R]^n\
                      q_i(z,x)\le0,\text{ affine rows}\}.        \tag{10}
\]

The displayed sets restrict \(z\) to integer vectors. The argument is a
uniform size bound, not an enumeration of those vectors. It does not bound
every feasible \(x\): it preserves the existence of a continuous witness in
every feasible integer fiber.

Two consequences follow, with different convexity assumptions.

- If only the continuous slices are convex, fixed \(h\) feasibility is
  in NP: guess the bounded integer assignment and use (9) to decide its
  continuous fiber in polynomial time. The verifier can decide a fiber that
  has no rational exactly feasible point.
- If each **full** Hessian in \((z,x)\) is PSD, append the common box and
  apply [the exact integer-projection construction](mixed-integer-span-frontier.md).
  There is a rational MILP with exactly the same feasible integer
  assignments, no new integer variables, and construction time and encoding
  length \(N^{O((h+1)^2)}\). Consequently feasibility is polynomial in the
  Turing model for every fixed \(k,h\). Its returned integer assignment
  has an exactly feasible original continuous fiber; the returned continuous
  LP variables need not themselves satisfy the original quadratic rows.

The second statement uses full joint convexity for the polyhedral square
approximation, beyond the slice convexity sufficient for (10). Exact linear
optimization in \(z\) alone also transfers to the resulting MILP. A supplied
rational convex quadratic objective threshold can be treated as another
inequality, increasing the continuous Hessian-span dimension by at most one.

## 4. Prior work and the scope of the addition

The comparison concerns a parameter refinement, not the first small-point
bound or the first replacement of a convex integer set by a rational
polyhedron.

**General real algebraic bounds.** Standard sampling and elimination methods
already bound coordinates of points in nonempty semialgebraic sets. Their
general dependence is exponential in the number of variables. The
few-quadratic results of
[Grigoriev and Pasechnik](https://arxiv.org/abs/cs/0403008) instead exploit a
bounded number of quadratic-map components; their sampling theorem includes
coefficient-size information and is not restricted to convex systems.
Arbitrarily many affine and quadratic rows are permitted here, with a bound
depending on the span of their Hessian matrices. The active affine
restriction makes this possible without treating the affine parts as free
quadratic-map components. The present
[few-quadratic source audit](few-quadratic-value-bound-evidence.md) records
the exact inspected statements and the limits of that comparison.

**One quadratic row and mixed-integer optimization.**
[Del Pia's 2025 paper](https://arxiv.org/abs/2311.00099), Theorem 3, gives an
exact FPT algorithm in the integer dimension for a convex quadratic objective
over a rational mixed-integer polyhedron. Its decision machinery therefore
handles one convex quadratic sublevel row with affine rows, without requiring
an input box. It is stronger than the present polynomial-for-fixed-parameters
conclusion on that special class. The present candidate addition permits
arbitrarily many quadratic rows with fixed continuous Hessian span; no
improvement of Del Pia's parameter dependence is claimed. Theorems 2--3 and
the boundedness reduction in Section 4.2 were inspected in the current
[local author text](sources-hessian-span-prior/delpia-2025.txt).

**An exact integer-point polyhedral approximation is already known.**
[Kocuk, *Rational polyhedral outer-approximations of the second-order cone*
(2021)](https://optimization-online.org/wp-content/uploads/2019/12/7501.pdf),
Section 5, Proposition 7, constructs a rational polyhedral outer approximation
with exactly the same integer points for an intersection of integer-data
balls; the text also discusses ellipsoids with integral data. Its proof
selects approximation precision below the unit gap in the integer-valued
squared norm. It is direct precedent for the integer-projection transfer
principle. The present theorem permits existentially quantified continuous
variables, whose optimized residuals are not generally rational and have no
unit arithmetic gap. The new radius and the preceding Hessian-span gap
theorem supply bounds for those fibers. The rational polyhedral approximation
itself remains an established ingredient. Proposition 7 was inspected in the
open author PDF and the repository's
[local full text](../literature/papers/kocuk2021-rational-polyhedral-outer-approximations-of/fulltext.md).

**The unrestricted small-point claim would be false.**
[Bienstock, Del Pia and Hildebrand](https://arxiv.org/abs/2011.08347), Example
6.1, recalls the classical system

\[
 x_1\ge2,\qquad x_{i+1}\ge x_i^2\quad(i=1,\ldots,n-1).
\]

Every feasible point has \(x_n\ge2^{2^{n-1}}\), requiring exponentially
many bits just to encode that coordinate's magnitude. Its native Hessians
are the \(n-1\) independent coordinate matrices, so \(h=n-1\). This is
consistent with (1), and shows why the fixed-span condition has substance.
The example and its historical attribution were checked in the
[local full text](../literature/papers/bienstock2023-complexity-exactness-and-rationality-in/fulltext.md).

No equivalent unbounded convex quadratic small-point theorem parameterized
by this matrix-span dimension was identified in the inspected sources.
That is a qualified search result, not a priority claim. The broader
[Hessian-span prior-work audit](hessian-span-prior.md) supplies additional
comparisons with algebraic degree, exact feasibility, and convex integer
optimization.

## 5. Limitations and remaining work

- All inequalities must be weak and the continuous quadratics convex. Closedness,
  attainment of the norm minimum, Slater after right-hand-side relaxation,
  and KKT sufficiency are used explicitly.
- The radius bounds a feasible representative, not the whole feasible set.
  It need not preserve continuous objective values unless an objective
  threshold is included before deriving the radius.
- Bounded integer coordinates remain an assumption for the finite-size exact
  MILP projection. The continuous radius theorem does not supply a uniform
  bound over integer assignments of unbounded bit length.
- An arbitrary nonempty unbounded convex quadratic system need not be known
  to contain a rational point from this proof. The current batch's
  [irrational singleton](hessian-span-reduction.md) already rules out a
  universal rational-witness claim in the fixed-span class.
- The exponent and numerical constants are not practical estimates. Extracting
  sharper radius and residual bounds, exploiting instance structure, and
  comparing against direct conic methods are needed before asserting a
  computational advantage.

Verification so far consists of symbolic proof inspection, explicit bit-size
accounting, and targeted reads of the named primary sources and related
repository proofs. No numerical test could establish the universal radius
claim. No Lean formalization or project-wide checks have been run for this
extension. The independent reviews are
[unbounded-hessian-span-review.md](unbounded-hessian-span-review.md) and
[unbounded-span-review.md](unbounded-span-review.md). Both separately checked
the compactness, sparse KKT, coefficient, and mixed-integer arguments and
found no mathematical gap. A positive review is evidence, not a substitute
for the proof. A targeted inline Python check passed for this Markdown file
(control characters, trailing whitespace, final newline, and all 12 local
Markdown links). The scoped command
`git diff --check -- research-20260927/unbounded-hessian-span.md` also
returned successfully; the Python check covers the file's current contents
independently of Git tracking status.
