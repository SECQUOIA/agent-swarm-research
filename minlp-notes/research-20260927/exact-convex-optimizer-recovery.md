# Exact optimizers for convex quadratic systems of fixed Hessian span

Date: 2026-09-27. Status: candidate theorem; independent
[adversarial review](exact-convex-optimizer-review.md) and a separate root
rereading found no gap. Publication priority remains unestablished.

The [unbounded-domain value theorem](unbounded-value-optimization.md)
classifies infeasibility and objective unboundedness and constructs a finite
optimal value exactly. This note adds an exact optimal vector. Its coordinates
can be irrational, and the feasible set can be unbounded or have empty
interior. The only structural parameter is the dimension of the span of the
constraint Hessians. The objective Hessian can be arbitrary positive
semidefinite.

The output construction uses classical algebraic recognition. The additional
argument bounds the algebraic complexity of the minimum-norm optimizer when
the optimal objective value enters as one algebraic constant. Only constant
terms become algebraic, so general linear algebra over number fields is
unnecessary.

A subsequent [ordered-perturbation proof](ordered-perturbation-optimizer.md)
improves the canonical optimizer's coordinate height to \(N^{O(h+1)}\)
and bounds its entire coordinate field's degree by
\((2n+1)^{\min(h,n)}\). The recovery algorithm below can use those
stronger bounds. The one-algebraic-constant proof is retained as a separate
route; its displayed \(N^{O((h+1)^2)}\) bound is no longer the strongest
bound in this research package.

## 1. Statement and dependencies

Consider

\[
 \min\{q_0(x):x\in F\},\qquad
 F=\{x\in\mathbb R^n:Ax\le b,\ Ex=e,\ q_i(x)\le0\ (1\le i\le m)\},
\]

where all input data are rational and every quadratic Hessian, including
that of the objective, is positive semidefinite. Let \(N\ge2\) be the
explicit binary input length and put

\[
 h=\dim_{\mathbb Q}\operatorname{span}\{\nabla^2q_i:1\le i\le m\}.
\]

**Theorem.** There is a deterministic algorithm with running time
\(N^{\operatorname{poly}(h+1)}\) which reports infeasibility, reports that
the objective is unbounded below, or returns the finite optimum and an
optimal vector exactly. Each real algebraic output coordinate is represented
by its primitive integer minimal polynomial and a rational interval
containing exactly the intended real root. Thus the algorithm is polynomial
time for every fixed \(h\). It is not an FPT claim with an exponent
independent of \(h\).

In the finite case the returned vector is the unique minimum-norm point of
the set of optimizers. Its coordinate degrees and minimal-polynomial
coefficient bit lengths are at most

\[
 N^{O((h+1)^2)}.                                      \tag{1}
\]

No variable bounds, rational feasible-point promise, Slater condition, or
genericity assumption is imposed. The theorem gives an exact coordinatewise
description of one common optimizer. It does not give a rational optimizer,
an unboundedness ray, a sharp dependence on \(h\), or a practical complexity
estimate.

The proof uses the following previously recorded results.

- The [value theorem](unbounded-value-optimization.md) supplies exact status
  classification and, in the finite case, an algebraic optimal value
  \(\theta\) of degree and coefficient bit length \(N^{O(h+1)}\). Finite
  attainment is the classical result of Terlaky and Luo--Zhang cited there.
- The [canonical feasible-point proof](algebraic-witness-recovery.md)
  supplies the rational-input minimum-norm construction. Sections 2 and 3
  below extend its coefficient argument to the constant \(\theta\).
- The [algebraic-recognition audit](algebraic-recognition-source-review.md)
  records Kannan--Lenstra--Lovasz's exact recovery theorem and elementary
  bounds for factors, conjugate separation, and isolating intervals.

## 2. Only the constant terms need algebraic coefficients

Assume the optimum is finite. Classical attainment gives a nonempty closed
convex optimal set

\[
 F^*=F\cap\{x:q_0(x)-\theta\le0\}.
\]

Let \(x^*\) be its unique minimum-norm point. Existence follows by
intersecting \(F^*\) with any nonempty norm sublevel set; strict convexity
of the norm squared gives uniqueness. The Hessian span of the defining
quadratics for \(F^*\) has dimension at most \(h+1\).

Introduce a symbolic scalar \(T\) and write these quadratic polynomials
as \(r_i(x,T)\). All are rational polynomials; only the added objective
row depends on \(T\), through its constant term \(-T\). Fix the active
rows at \((x^*,\theta)\). Retain every original affine equality. Replace active affine inequalities by
equations and delete inactive affine and quadratic inequalities. The
minimum norm remains unchanged: a smaller-norm point satisfying the retained
rows would give a smaller-norm original point on a sufficiently short
segment from \(x^*\). Convexity preserves retained inequalities, and
strict slack preserves each deleted inequality along that segment.

Choose a basis of the retained rational Hessian matrices, of size
\(s\le h+1\), and express every retained Hessian in that basis. The
coefficients \(c_{ij}\) are rational and have polynomial bit length in
\(N\). Add the affine equations

\[
 r_i(x,T)-\sum_{j\in B}c_{ij}r_j(x,T)=0.              \tag{2}
\]

At \(T=\theta\), all these equations hold at \(x^*\), because all
retained quadratic rows are active there. Their left-hand coefficients in
\(x\) are rational; their right-hand sides are affine functions of
\(T\). The same holds for the active original affine rows. Consequently
the full affine system has the form

\[
 Lx=d+Te,\qquad L,d,e\text{ rational}.                \tag{3}
\]

Choose independent rows and a nonsingular column minor of the rational
matrix \(L\). Solving its pivot coordinates in terms of the free
coordinates gives

\[
 x=a+Tb+Vu,\qquad u\in\mathbb R^d,                  \tag{4}
\]

where \(a,b,V\) are rational, \(V\) has full column rank, and every
coefficient has polynomial bit length in \(N\). To justify the last
claim, clear rational denominators in (3) and apply Cramer's rule to the
chosen minor. Its size and entry bit lengths are polynomial in \(N\);
the determinant and every numerator therefore have polynomial bit length.
The coefficient matrix is independent of \(T\), so its determinant is
a nonzero rational constant. No division by an algebraic quantity occurs.

The remaining dependent equations become affine consistency equations in
\(T\). They hold at \(T=\theta\). They can be retained in every
formula below; nothing requires (4) to solve the original affine system at
other values of \(T\).

After substitution, each retained row has the form

\[
 \widetilde r_i(u,T)=\tfrac12u^TH_i u+\ell_i(T)^Tu+c_i(T),
\]

where \(H_i\) is rational positive semidefinite, \(\ell_i\) is
affine in \(T\), and \(c_i\) has degree at most two. All coefficients
have polynomial bit length in \(N\). At \(T=\theta\), (2) gives
whole-polynomial identities, including the affine and constant terms.

## 3. A bound for every coordinate of the canonical optimizer

Fix \(T=\theta\) temporarily. Minimize

\[
 f(u,T)=\|a+Tb+Vu\|_2^2
\]

under the retained rows relaxed to
\(\widetilde r_i(u,T)\le\varepsilon\), where
\(0<\varepsilon<1\). If there are no free coordinates, each output
coordinate is \(a_j+b_j\theta\). For \(b_j\ne0\), substitute
\(T=(z-a_j)/b_j\) into \(P_\theta(T)\) and clear rational
denominators; for \(b_j=0\), use the linear polynomial of \(a_j\).
These operations give the desired degree and height bound. Otherwise the objective Hessian
is \(H_f=2V^TV\succ0\).

The parameter of \(x^*\) is strictly feasible for every positive
\(\varepsilon\). Coercivity gives a unique relaxed minimizer;
Slater's condition supplies KKT multipliers. Its norm is at most
\(\|x^*\|\), since \(x^*\) is an available competitor. Every
accumulation point as \(\varepsilon\downarrow0\) is retained-feasible
and has minimum norm. The restricted feasible set is convex and contains
\(x^*\), so strict convexity makes this minimizer unique. Thus the
reconstructed relaxed minimizers converge to \(x^*\).

The whole-polynomial identities from (2) compress the multiplier
contribution to stationarity into \(s\le h+1\) coordinates. Conic
Caratheodory, applied only to currently active rows, leaves at most \(s\)
nonzero multipliers and preserves complementarity. Fix one support \(J\)
that occurs along a sequence \(\varepsilon\downarrow0\), with
\(|J|\le h+1\). Define

\[
 M=H_f+\sum_{i\in J}\lambda_iH_i,\qquad
 \Delta=\det M>0,
\]
\[
 p=-\operatorname{adj}(M)
          \left(\ell_f(T)+\sum_{i\in J}\lambda_i\ell_i(T)\right).
\]

For nonnegative multipliers, \(M\) is positive definite. In particular,
\(\Delta\) is independent of \(T\), while \(p\) is affine in
\(T\). Stationarity is equivalent to \(u=p/\Delta\). Put

\[
 G_i=\tfrac12p^TH_i p+\Delta\ell_i(T)^Tp+
                              (c_i(T)-\varepsilon)\Delta^2.
\]

Let \(\mathcal K_J(T,\varepsilon,\lambda)\) contain the affine
consistency equations from (3), and

\[
 \Delta>0,\quad \lambda_i\ge0\ (i\in J),\quad
 G_i\le0\ \text{for every retained row},\quad
 \lambda_iG_i=0\ (i\in J).                           \tag{5}
\]

All retained primal rows occur, including rows outside \(J\). At
\(T=\theta\), every solution of (5) is sufficient for optimality of
the relaxed convex problem. Clearing fixed positive rational denominators
produces integer polynomial conditions. Their degrees are \(O(N)\),
their coefficient bit lengths are polynomial in \(N\), and their degrees
in \(T\) are at most two. Determinants introduce only polynomial
coefficient bit lengths; their possibly many monomials do not change this
coefficient bound.

Let \(P_\theta\) be the primitive minimal polynomial of \(\theta\),
and choose rational endpoints \(l<\theta<u\) such that \(\theta\)
is its only real root in \((l,u)\). The value-recovery theorem supplies
such a representation with degree and all encoding lengths bounded by
\(N^{O(h+1)}\). Set

\[
 \mathcal R(T):\quad P_\theta(T)=0,\quad l<T<u.
\]

For original coordinate \(j\), put

\[
 P_j=(a_j+Tb_j)\Delta+(Vp)_j.
\]

The formula in the one free real variable \(z\),

\[
 \forall\gamma\;\left[\gamma\le0\ \lor\
 \exists T,\varepsilon,\lambda:\quad
 \mathcal R(T),\quad 0<\varepsilon<1,\quad\varepsilon<\gamma,
 \quad -\gamma\Delta<P_j-z\Delta<\gamma\Delta,
 \quad\mathcal K_J(T,\varepsilon,\lambda)\right],     \tag{6}
\]

defines exactly \(\{x_j^*\}\). Indeed, \(\mathcal R\) forces
\(T=\theta\), independently of \(\gamma\). The selected support
sequence proves the forward implication; convergence of every relaxed
minimizer proves the reverse implication. Unbounded multipliers present no
problem.

There are only two quantified blocks: one universal variable and at most
\(h+3\) existential variables. The largest input degree and coefficient
bit length are \(N^{O(h+1)}\), because of \(P_\theta\).
Coefficient-sensitive block quantifier elimination, in the form of
Basu--Pollack--Roy Theorem 14.16 used in the
[value proof](hessian-span-reduction.md), therefore gives a formula whose
polynomials have degree and coefficient bit length
\(N^{O((h+1)^2)}\). Some nonzero output polynomial vanishes at
\(x_j^*\), since otherwise all its signs would be locally constant and
could not define a singleton. An integer factor bound passes the same
asymptotic bounds to the primitive minimal polynomial. This proves (1).

The affine restriction and multiplier support need not be identified by the
algorithm: their existence proves uniform bounds on the point later recovered
by rational optimization queries. Cauchy's root bound now supplies an
effective radius

\[
 R=2^{N^{C(h+1)^2}},\qquad x^*\in[-R,R]^n,            \tag{7}
\]

after increasing an absolute constant \(C\). This is a complexity bound,
not a calibrated radius for an implementation.

## 4. Decide intersections of the optimal set using rational input

Although \(F^*\) may have an irrational defining constant, an exact
intersection oracle requires only rational optimization problems.

Let \(C\) consist of the box in (7), any additional rational affine
bounds, and optionally a rational norm sublevel inequality
\(\|x\|_2^2\le s\). First decide whether \(F\cap C\) is empty.
If it is nonempty, compute exactly

\[
 \eta_C=\min\{q_0(x):x\in F\cap C\}.               \tag{8}
\]

The domain in (8) is compact, so its minimum exists. Its input is entirely
rational. Its native Hessian span has dimension at most \(h+1\), because
the only possible new quadratic row is the norm inequality. Apply the
value algorithm and compare the two real algebraic numbers
\(\eta_C\) and \(\theta\). Since \(F\cap C\subseteq F\),
\(\eta_C\ge\theta\), and

\[
 F^*\cap C\ne\varnothing
 \quad\Longleftrightarrow\quad \eta_C=\theta.        \tag{9}
\]

This is a decision oracle, not a claim that the optimizer of a rounded
subproblem is exactly optimal. Neither irrational coefficients nor an
unboundedness question enter the rational subproblem (8).

For completeness, exact comparison is polynomial in the encodings of two
real algebraic numbers of polynomial degree and height. Normalize their
primitive irreducible polynomials. If they differ, their product is
squarefree; if they agree, use that one polynomial. Its nonzero integer
discriminant and Cauchy's root bound give a separation
\(2^{-\operatorname{poly}(D,H)}\) between distinct roots, where
\(D\) bounds degrees and \(H\) bounds coefficient bit lengths.
Refine each selected root to absolute error less than one eighth of this
separation.
They are equal exactly when their rational approximations differ by less
than half this separation; otherwise their order is the order of the
approximations. Polynomial-time refinement follows either from the same
certified value-bisection procedure or from real-root isolation. The
discriminant calculation is recorded explicitly in the
[algebraic-recognition audit](algebraic-recognition-source-review.md).

## 5. Approximate one fixed optimizer, then recognize it

Write \(\rho=\|x^*\|_2^2\). For a rational requested error
\(0<\tau\le1\), bisect \([0,nR^2]\) using (9) with the norm
threshold \(s\). Preserve a feasible upper threshold \(b\), and stop
when the interval width is at most \(\tau^2/16\). Then

\[
 K=F^*\cap[-R,R]^n\cap\{x:\|x\|_2^2\le b\}
\]

is nonempty, and \(b\le\rho+\tau^2/16\). The projection inequality
for the minimum-norm point of the closed convex set \(F^*\) is

\[
 \langle x^*,x-x^*\rangle\ge0\qquad(x\in F^*).
\]

It follows by differentiation along a feasible segment. Therefore

\[
 \|x-x^*\|_2^2\le\|x\|_2^2-\|x^*\|_2^2
                  \le\tau^2/16\qquad(x\in K).        \tag{10}
\]

Bisect the rational coordinate intervals of the box, preserving a nonempty
intersection with \(K\) through (9), until every interval has width at
most \(\tau\). If a lower half is infeasible, keeping the closed upper
half preserves feasibility. Let \(c\) be the final box midpoint.
Some \(y\in K\) belongs to that box, so

\[
 |c_j-x_j^*|\le |c_j-y_j|+|y_j-x_j^*|
               \le\tau/2+\tau/4<\tau.
\]

All queries have rational input. Their number and bit lengths are polynomial
in \(\log R+N+\log(1/\tau)\). Applying the fixed-span value algorithm
gives a procedure polynomial in the requested number of accuracy bits for
fixed \(h\). Every approximation refers to the same canonical optimizer;
the procedure does not switch between unrelated points of \(F^*\).

Finally apply Kannan--Lenstra--Lovasz's
[Theorem 1.19](https://www.math.cmu.edu/~af1p/Teaching/AdditiveCombinatorics/LLLL.pdf),
*Polynomial Factorization and Nonrandomness of Bits of Algebraic and Some
Transcendental Numbers*, Mathematics of Computation 50 (1988), 235--250.
Given degree bound \(D\), coefficient magnitude bound \(A\), and an
approximation with \(O(D^2+D\log A)\) certified bits, its algorithm
recovers the primitive minimal polynomial in polynomial time in
\(D,\log A\). Bound (1) supplies polynomial bounds for fixed \(h\),
and the preceding procedure supplies the required approximations. Further
approximation using the discriminant separation bound supplies a rational
interval containing exactly the intended real root for every coordinate.

Composing the polynomial bounds gives the stated conservative
\(N^{\operatorname{poly}(h+1)}\) running time. No claim is made that
the exponent in the coordinate bound (1) is also the exponent of the entire
algorithm.

## 6. Significance, prior work, and limits

This completes exact continuous optimization for the candidate Hessian-span
class: one can return an optimal point as well as decide a threshold or
recover an optimal value. Exact coordinate recovery also applies after an
integer assignment has been selected by the batch's mixed-integer results,
provided its continuous slice satisfies the assumptions above. Recovering
an integer assignment and proving its optimality remain the responsibilities
of those separate mixed-integer algorithms.

The result permits arbitrarily many constraints, variables, and Hessian
rank when the linear span of the constraint Hessian matrices has fixed
dimension. It does not establish exact polynomial-time optimization for
general convex QCQP. The square-root-sum encoding and parameter comparisons
in [the prior-art audit](hessian-span-prior.md) still apply.

The following ingredients are established: finite attainment, strict-convex
tie breaking by norm, active-face restriction, KKT sufficiency, conic
Caratheodory, fixed-block elimination, projection inequalities, algebraic
recognition, and exact algebraic comparison. The potential contribution is
their combination through a parameter-sensitive degree and coefficient
bound, including the one-algebraic-constant extension above. Priority for
this result has not been established. This note adds no independent novelty
claim for the recovery mechanism.

In particular, Chandrasekaran--Tamir's *Optimization problems with algebraic
solutions: quadratic fractional programs and ratio games*, Mathematical
Programming 30 (1984), 326--339,
[pp. 326--328](https://www.tau.ac.il/~atamir/opt_84.pdf), already connects
degree and coefficient bounds, decision bisection, and exact optimization.
The previously recorded comparison inspected those introductory pages and
does not amount to an exhaustive screening of that article. The present
claim concerns the separate Hessian-span class.

Coordinatewise algebraic output is an exact representation by construction.
It is not, merely by its format, a polynomial-size independently checkable
multivariate feasibility certificate. A common-field representation and
efficient independent verification are separate questions. The theorem also
does not establish a computational speedup over current numerical solvers;
its significance is exact Turing tractability without strict feasibility or
rational optimal points.

## 7. Verification record

The proof explicitly checks the rational affine matrix in (3), constant
denominator clearing, the unique selected root in (6), every retained primal
row in (5), compactness of the rational optimization subproblems, and
convergence to one fixed output point. An independent reviewer read the
complete proof and found no gap; a second reviewer checked the affine
restriction, and the root agent independently reread the full proof and
algorithm. No numerical experiment or Lean proof is asserted to
verify the general theorem. Primary algebraic-recognition source inspection
and the existing detailed source audit support the algorithmic recovery
step. The source inspection checked KLL's Theorem 1.19 and Explanation 1.18
on printed page 241, including the reciprocal reduction and integer bit
complexity. A targeted Python check of this file passed for local-link
existence, trailing whitespace, control characters, final newline, and
paired math delimiters. No project-wide checks or CI inspection were run.
