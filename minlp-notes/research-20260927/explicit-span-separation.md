# Explicit algebraic bounds from the Hessian span

Date: 2026-09-27. Status: proof, independent adversarial review, and targeted
exact checks completed. This is a quantitative refinement of
the batch's Hessian-span theorem, not a claim of new elimination theory.

The value theorem in [the unbounded-domain note](unbounded-value-optimization.md)
can avoid block quantifier elimination. A minimal representation of the KKT
gradient makes the selected multiplier root nonsingular. A finite-dimensional
multiplication determinant then gives an explicit degree bound and a direct
coefficient bound, even if other complex KKT components have positive
dimension.

For a rational convex quadratic program with finite optimum, let `n` be its
number of continuous variables and let `h` be the dimension of the linear
span of its constraint Hessian matrices. The objective Hessian is excluded.
The optimal value is annihilated by a nonzero integer polynomial of degree
at most

\[
 (2n+1)^{\min(h,n)}.                                      \tag{1}
\]

The coefficient bit length remains \(N^{O(h+1)}\), where \(N\) is total
explicit rational input length. A more explicit bound in the coefficients
of the reduced KKT polynomials is given below. Neither strict feasibility
nor finite-dimensionality of the full complex KKT variety is assumed.
Feasibility and finite attainment, and convergence of the regularized values,
are established in the linked note; this note replaces only its elimination
step.

## 1. Choose independent active gradients

Use the active affine restriction in the linked proof. Its rational
parametrization \(x=x_0+Vu\) has \(d\le n\) free variables and coefficients
of polynomial bit length. The retained convex constraint polynomials span
at most an \(h\)-dimensional space as whole polynomials. Therefore their
gradients at each fixed point span a space of dimension at most \(h\).

For \(\varepsilon>0\), the regularized problem is

\[
 \min_u q_0(u)+\varepsilon\|u\|^2
 \quad\text{subject to}\quad q_i(u)\le\varepsilon.
                                                               \tag{2}
\]

It has a unique optimum, strict feasibility, and nonnegative KKT multipliers.
Among representations of the negative objective gradient as a nonnegative
combination of currently active constraint gradients, choose one with minimal
support \(J\). Its coefficients are positive and its gradient columns are
linearly independent: a nontrivial dependence would allow a change in weights
that preserves nonnegativity and removes a positive weight. In particular,

\[
 s=|J|\le\min(h,d).
\]

This is a reduction using numerical gradients at the selected optimum.
The earlier whole-polynomial restriction is essential to the bound by `h`.
The reduced multipliers preserve stationarity and complementarity. Their
Lagrangian Hessian is positive definite because every constraint Hessian is
positive semidefinite and the objective includes \(2\varepsilon I\).

There are finitely many supports. Fix one occurring along a sequence
\(\varepsilon_\nu\downarrow0\). Throughout the remaining proof, `J` is this
one support, although its multiplier values may diverge along the sequence.

Write \(q_i(u)=\tfrac12u^TQ_i u+a_i^Tu+c_i\), and set

\[
 \begin{aligned}
 M&=Q_0+2\varepsilon I+\sum_{i\in J}\lambda_iQ_i,\\
 \Delta&=\det M,\qquad
 p=-\operatorname{adj}(M)\left(a_0+\sum_{i\in J}\lambda_i a_i\right),\\
 G_i&=\tfrac12p^TQ_i p+\Delta a_i^Tp+(c_i-\varepsilon)\Delta^2,
                  &&i\in J,\\
 A&=\Delta^2,\\
 B&=\tfrac12p^TQ_0p+\Delta a_0^Tp+c_0\Delta^2+
                                             \varepsilon p^Tp.
 \end{aligned}                                                   \tag{3}
\]

At a selected KKT point, \(u=p/\Delta\), \(G_i=0\), and its regularized
value is \(w=B/A\), with \(A>0\).

The selected root of \(G_1=\cdots=G_s=0\), viewed as equations in
\(\lambda\) for fixed \(\varepsilon\), is nonsingular. Indeed,

\[
 \frac{\partial u}{\partial\lambda_j}
       =-M^{-1}\nabla q_j(u),
 \qquad
 \frac{\partial G_i}{\partial\lambda_j}
       =-\Delta^2\nabla q_i(u)^TM^{-1}\nabla q_j(u).             \tag{4}
\]

The derivative of the factor \(\Delta^2\) vanishes from the second
expression because \(q_i(u)-\varepsilon=0\). The matrix in (4) is negative
definite, since the selected gradients are independent. Nonsingularity is
only asserted at the selected root. Other roots and components may be
singular or positive-dimensional.

## 2. An elementary elimination lemma

Here is the algebraic statement needed for (3). It is useful to keep the
parameter `epsilon` separate from the variables being eliminated.

Let

\[
 G_1,\ldots,G_s,A,B\in\mathbb Z[\varepsilon,\lambda_1,\ldots,\lambda_s]
\]

have total degree at most \(a\ge1\) in \(\lambda\), degree at most \(b\)
in \(\varepsilon\), and coefficient \(\ell_1\)-norm at most
\(2^\tau\), with \(\tau\ge1\). Suppose a sequence of real numbers
\(\varepsilon_\nu\ne0\) tends to zero and there are corresponding roots
\(\lambda_\nu\) of the `G` system such that

\[
 \det\left(\frac{\partial G}{\partial\lambda}
                (\varepsilon_\nu,\lambda_\nu)\right)\ne0,
 \quad A(\varepsilon_\nu,\lambda_\nu)\ne0,
 \quad
 \frac{B(\varepsilon_\nu,\lambda_\nu)}
      {A(\varepsilon_\nu,\lambda_\nu)}\longrightarrow\theta.
                                                               \tag{5}
\]

Put

\[
 D=a+1,\qquad L=D^s,\qquad T=a(s+1),
 \qquad
 K=L\bigl[\tau(T+1)+2+\lceil\log_2 L\rceil\bigr].             \tag{6}
\]

**Elimination lemma.** There exists a nonzero
\(P\in\mathbb Z[w]\) with \(P(\theta)=0\),
\(\deg P\le L\), and coefficient \(\ell_1\)-norm at most \(2^K\).
The case \(s=0\) is included: there are no root equations and `L=1`.

### 2.1 Make the quotient finite by a controlled deformation

Introduce \(\delta\) and deform the equations to

\[
 F_i=G_i+\delta\lambda_i^D=0\qquad (i=1,\ldots,s).             \tag{7}
\]

Over \(\mathbb Q(\varepsilon,\delta)\), use a monomial order that first
compares total \(\lambda\)-degree. The leading monomials are the pairwise
coprime \(\lambda_i^D\). Thus the `F` polynomials form a Groebner basis,
and the quotient has the basis

\[
 \mathcal B=\{\lambda_1^{\alpha_1}\cdots\lambda_s^{\alpha_s}:
                              0\le\alpha_i<D\},
 \qquad |\mathcal B|=L.                                      \tag{8}
\]

For clarity, coprimality gives the basis assertion directly: the
S-polynomial for `i,j` reduces to zero by substituting
\(\lambda_i^D=-G_i/\delta\) and
\(\lambda_j^D=-G_j/\delta\). Every replacement strictly decreases
total degree. The same statements hold after specializing any real
\(\varepsilon\) and any nonzero \(\delta\); no exceptional value of
\(\varepsilon\) changes a leading coefficient.

Let \(M_A,M_B\) be the multiplication matrices of `A,B` in (8). Their
entries are Laurent polynomials in \(\delta\) with integer-polynomial
coefficients in \(\varepsilon\). An unreduced product of a basis monomial
and `A` or `B` has total \(\lambda\)-degree at most `T`. Each replacement
lowers that degree by at least one. Hence at most `T` replacements occur
along any branch of the reduction.

Consequently,

\[
 \widetilde M_A=\delta^T M_A,\qquad
 \widetilde M_B=\delta^T M_B
\]

have integer-polynomial entries with

\[
 \deg_\varepsilon\le b(T+1),\qquad
 \deg_\delta\le T,\qquad
 \|\text{entry}\|_1\le2^{\tau(T+1)}.                         \tag{9}
\]

For the norm estimate, regard each reduction as a branching replacement of
a monomial by the terms of one `G` polynomial. The sum of absolute
coefficients increases by at most \(2^\tau\) per level. The initial sum
is at most \(2^\tau\), and branch depth is at most `T`. Term collection
cannot increase this bound.

### 2.2 Remove permanent undefined-value factors

Introduce a second independent indeterminate \(\zeta\) and form

\[
 H(\varepsilon,\delta,w,\zeta)=
 \det\bigl(w\widetilde M_A-\widetilde M_B
                                      -\zeta\delta^T I_L\bigr).  \tag{10}
\]

This is a nonzero integer polynomial: its leading \(\zeta\) coefficient
is \((-\delta^T)^L\). Its degree in `w` is at most `L`. Expanding the
determinant and using (9) gives

\[
 \|H\|_1\le L!\,2^{L[\tau(T+1)+2]}\le2^K.                   \tag{11}
\]

Let \(k\) be its smallest \(\zeta\)-exponent with nonzero coefficient,
and write

\[
 H=\zeta^k H_k(\varepsilon,\delta,w)+O(\zeta^{k+1}),
 \qquad H_k\ne0.                                            \tag{12}
\]

This step is needed because other roots may satisfy `A=B=0`. Setting
\(\zeta=0\) directly could make the determinant identically zero.

Fix one parameter \(\varepsilon_\nu\) and selected nonsingular root from
(5). The real implicit function theorem gives a root
\(\lambda(\delta)\) of (7) near \(\delta=0\), with
\(\lambda(0)=\lambda_\nu\) and \(A\ne0\) along the branch. Define
\(w(\delta)=B/A\) there. For each sufficiently small nonzero real
\(\delta\), evaluation at this root is a nonzero common left eigenvector
of the multiplication matrices. Therefore the specialization of (10) has
the polynomial factor

\[
 \delta^T\bigl(A(\varepsilon_\nu,\lambda(\delta))w
             -B(\varepsilon_\nu,\lambda(\delta))-\zeta\bigr).
\]

The expression in parentheses is coprime to \(\zeta\), because its
coefficient of `w` is nonzero. Since the full determinant is divisible by
\(\zeta^k\), the remaining factor is also divisible by \(\zeta^k\).
It follows that

\[
 H_k(\varepsilon_\nu,\delta,w(\delta))=0.                    \tag{13}
\]

This argument remains valid if specialization makes `H_k` identically zero
or increases the determinant's order in \(\zeta\). It does not require
excluding finitely many parameter values.

### 2.3 Take the two limits in the required order

Let \(j\) be the least \(\delta\)-exponent in the nonzero polynomial
`H_k`, and write

\[
 H_k=\delta^j R(\varepsilon,w)+O(\delta^{j+1}),\qquad R\ne0.
\]

Divide (13) by \(\delta^j\) and let \(\delta\to0\). For every
selected \(\nu\),

\[
 R\left(\varepsilon_\nu,
        B(\varepsilon_\nu,\lambda_\nu) /
        A(\varepsilon_\nu,\lambda_\nu)\right)=0.             \tag{14}
\]

Finally let \(r\) be the least \(\varepsilon\)-exponent in `R`, and
write

\[
 R(\varepsilon,w)=\varepsilon^rP(w)+O(\varepsilon^{r+1}),
 \qquad P\ne0.
\]

Divide (14) by \(\varepsilon_\nu^r\) and use (5). This gives
\(P(\theta)=0\). Each coefficient-extraction step preserves the degree
bound in `w` and cannot increase coefficient norm. This proves the lemma.
The multipliers themselves need not stay bounded.

## 3. Apply the lemma to quadratic optimization

The polynomials (3) have \(\lambda\)-degree at most \(a=2d\) and
\(\varepsilon\)-degree at most \(b=2d+1\). Clear their rational
coefficients by one common positive integer, multiplying `A` and `B` by
the same factor so their ratio is unchanged. The resulting coefficient
\(\ell_1\)-norm has logarithm \(\tau=N^{O(1)}\). This follows from
rational affine elimination, determinant expansions, and denominator
clearing, as detailed in the existing Hessian-span proof. The logarithm
of the number of expanded monomials is also polynomial in `N`.

Equations (4) and convergence of the regularized values verify the
elimination lemma's hypotheses. Therefore

\[
 \deg P\le(2d+1)^s\le(2n+1)^{\min(h,n)},
 \qquad
 \log_2\|P\|_1\le
 (2d+1)^s\left[\tau\bigl(2d(s+1)+1\bigr)+2+
                     \left\lceil s\log_2(2d+1)\right\rceil\right].
                                                               \tag{15}
\]

If `d=0`, the retained optimizer is rational with polynomial bit length,
and a degree-one annihilator follows directly. The same degree-one
conclusion holds when `h=0`, since then `s=0`.

With `K` as in (15), a nonzero value satisfies

\[
 2^{-(K+1)}<|\theta|<2^{K+1}.                                \tag{16}
\]

For the lower bound, remove powers of `w` from `P`, reverse the resulting
polynomial, and use the elementary Cauchy root bound. The upper bound is
the same bound applied directly. These deliberately loose strict bounds
avoid special cases at zero or unit magnitude.

### A conditional bound for several quantities in the same field

The elimination lemma also gives a joint algebraic-degree statement. Suppose
that, along the same selected roots in (5), finitely many ratios
\(B_j/A\) converge to finite numbers \(\theta_j\), and every `B_j` obeys
the same degree bound `a`. Then

\[
 [\mathbb Q(\theta_1,\ldots,\theta_r):\mathbb Q]\le L.          \tag{17}
\]

To prove this, apply the lemma to every rational linear combination of the
`B_j`. Changing coefficients changes the height bound but leaves the degree
bound `L` unchanged. Each \(\theta_j\) is algebraic. The primitive element
theorem in characteristic zero provides a rational linear combination of
these numbers that generates their joint field, and that combination has
degree at most `L`.

This statement is conditional on a common convergent sequence. It does not
assert convergence of the regularized primal variables. For example, to
include primal coordinates when convergence is known, use the common
denominator \(\Delta^2\) and coordinate numerators \(p_j\Delta\), whose
degree in the multipliers is still at most `2d`. No product of separate
coordinate-degree bounds is then needed.

### Mixed-integer values with an attained optimum

Consider rational quadratic inequalities \(q_i(z,x)\le0\) and a rational
quadratic objective in \((z,x)\in\mathbb Z^k\times\mathbb R^n\), together
with rational affine equalities and inequalities. Assume the constraint
polynomials and objective are convex in `x` for each fixed integer
assignment. Let `h` be the span dimension of the constraint Hessian
blocks in `x`, excluding the objective. If the global optimum is finite and
attained, its value has algebraic degree at most

\[
 (2n+1)^{\min(h,n)},                                         \tag{18}
\]

regardless of the number `k` of integer variables. Indeed, fix an optimal
integer assignment \(z^*\). Its continuous fiber has exactly the global
optimal value: a better point in that fiber would improve the mixed-integer
optimum. Substitution of \(z^*\) preserves rationality, convexity in `x`,
and the constraint Hessian span, so (1) applies. When `n=0`, the value is
rational and the bound is one.

For jointly convex rational quadratics, finite attainment follows from the
classical Bank--Mandel result examined in the
[attainment prior audit](mixed-integer-attainment-prior.md). For merely
slice-convex systems, attainment remains an explicit hypothesis here.

The coefficient bound uses the substituted-fiber input length \(N(z^*)\),
which is polynomial in the original input length plus the total bit length
of \(z^*\). It is not uniformly polynomial in the original input length
when `k` is unrestricted. For example, the jointly convex, purely integer
problem

\[
 \min z_k\quad\text{subject to}\quad
 z_1\ge2,\quad z_{j+1}\ge z_j^2\quad(j=1,\ldots,k-1)
\]

has `h=0` and degree-one optimal value \(2^{2^{k-1}}\). Its sparse input
has \(O(k\log k)\) bits, whereas any nonzero integer annihilator of that
value requires a coefficient with \(\Omega(2^k)\) bits, by Cauchy's root
bound. This elementary corollary concerns algebraic degree; it supplies
neither a polynomial-time algorithm for unrestricted `k` nor a new
attainment theorem.

## 4. Prior results, contribution, and limitations

Canny's *Generalized Characteristic Polynomials*,
[1988 report, Theorem 3.2, printed pages 6--7](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1988/Archive/CSD-88-440.pdf),
already proves that the first nonzero perturbation coefficient of a
generalized resultant retains projections of proper components. The report's
following section applies this to isolated solutions in the presence of
higher-dimensional components. We inspected the scanned theorem and proof.
The published version is [JSC 9 (1990), 241--250](https://doi.org/10.1016/S0747-7171(08)80012-0).
The deformation principle in this note is established elimination theory.

[Pogudin, *Persistent components in Canny's generalized characteristic
polynomial*, Section 2, Proposition 1](https://arxiv.org/html/2401.01948v2#S2),
reviews this result and its generalizations. Its examples show why extra
components cannot casually be removed by a genericity assertion or by taking
two perturbations. Our construction needs a nonzero annihilator containing
the selected value; it does not try to characterize all its roots.

[Nie and Ranestad, Theorem 2.2 and the QCQP specialization](https://mathweb.ucsd.edu/~njw/PUBLICPAPERS/polyoptdeg_siopt5.pdf)
give the sharper generic QCQP degree \(2^s\binom ds\). Their stated
nongeneric extension assumes a zero-dimensional KKT system. We inspected
that theorem statement. The present construction uses the selected root's
nonsingularity, allows unrelated positive-dimensional components, and tracks
coefficient size explicitly. We do not claim that (15) is an optimal degree
bound or that standard intersection theory cannot improve it.

The additional optimization step is the use of minimal active gradient
support after the whole-polynomial restriction. It permits a nonsingular
system with at most `h` multiplier variables, despite arbitrary numbers of
original variables and constraint rows. The resulting contribution is an
explicit, independently checkable refinement of this batch's span theorem.
It does not by itself establish the priority of the broader span theorem.

This proof does not provide a practical algorithm for selecting the unknown
active affine restriction or support. The polynomial may contain many
extraneous factors. Worst-case precision remains large. Its immediate use is
to replace an implicit elimination bound by a degree formula and transparent
arithmetic estimates; sharper constants or practical numerical certification
would require further work.

## 5. Verification record

The [independent written review](explicit-span-resultant-review.md) checks
the quotient construction, the two perturbations, the order of
specialization, the KKT derivative, the explicit norm bound, and (17).
The reviewer also independently proposed the multiplication-matrix route.
These are overlapping proof contributions and checks, rather than wholly
independent discovery of the proof. After the complete argument was saved,
the root agent independently reread Sections 1--4 and rechecked the KKT
derivative, support reduction, quotient basis, degree and norm accounting,
the three coefficient extractions, and the `d=0` and `s=0` cases. That
separate review reported no gap.

A fresh reviewer checked the mixed-integer scope corollary (18), including
the attained-fiber argument and the repeated-squaring height obstruction.
That review prompted an explicit statement that quadratic constraints are
inequalities; convexity of a quadratic polynomial alone would not justify
allowing its zero set as an equality constraint.

A separate checker ran
`python research-20260927/check_explicit_span_resultant.py` successfully.
The [worked adversarial cases](explicit-elimination-adversary.md) include
a permanent `A=B=0` factor, an unrelated positive-dimensional component,
and a parameter specialization where `R(0,w)` vanishes identically. A
counterexample after dropping nonsingularity confirms that this assumption
cannot simply be omitted from the stated lemma. These calculations check
specific algebraic obstructions, not the general theorem.

The author checked this note's local links, trailing whitespace, control
characters, and final newline with a targeted Python command. No
project-wide verification or CI inspection was run. No Lean formalization
was undertaken.
