# Exact convex quadratic values without input bounds

Date: 2026-09-27. Status: proof, primary-source inspection, and
[independent adversarial review](unbounded-value-review.md) completed.
Publication priority remains unestablished.

The Hessian-span value bound extends to arbitrary rational polyhedral domains.
Explicit variable bounds are unnecessary. For a fixed-dimensional span of the
constraint Hessians, one can decide infeasibility or objective unboundedness
and, in the remaining case, recover the exact optimal value as a real
algebraic number in polynomial Turing time. The objective Hessian is excluded
from the span parameter. No constraint qualification is assumed.

This note combines the batch's compressed KKT argument with a classical
closedness theorem for convex quadratic systems. Finite attainment is also
classical. The additional conclusion is the uniform algebraic degree and
coefficient bound controlled by the constraint Hessian span, and its
consequences for exact computation.

## 1. Statement

Let

\[
 F=\{x\in\mathbb R^n:Ax\le b,\ Ex=e,\ q_i(x)\le0
                         \ (i=1,\ldots,m)\},
 \qquad q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i.
\]

All data are rational, every \(Q_i\succeq0\), and the objective
\(q_0\) is a rational convex quadratic with \(Q_0\succeq0\).
There are no boundedness assumptions on \(F\). Write \(N\ge2\) for
the total explicit binary input length, including the objective, and

\[
 h=\dim_{\mathbb Q}\operatorname{span}\{Q_1,\ldots,Q_m\}.
\]

**Value theorem.** If \(F\ne\varnothing\) and
\(\theta=\inf_{x\in F}q_0(x)>-\infty\), then the infimum is attained
and \(\theta\) is annihilated by a nonzero integer polynomial whose
degree and coefficient bit lengths are at most

\[
 D,H\le N^{C(h+1)}                                  \tag{1}
\]

for an effective absolute constant \(C\). After increasing \(C\),

\[
 |\theta|<2^{N^{C(h+1)}+2},\qquad
 \theta\ne0\ \Longrightarrow\
 |\theta|>2^{-N^{C(h+1)}-2}.                         \tag{2}
\]

**Algorithmic corollary.** For every fixed \(h\), a deterministic
polynomial-time Turing algorithm reports exactly one of the following:

1. \(F=\varnothing\);
2. \(q_0\) is unbounded below on \(F\);
3. the finite optimal value, represented by its primitive integer minimal
   polynomial and a rational interval containing exactly the selected real
   root.

This statement does not yet construct an optimal continuous vector or a ray
certifying unboundedness. The output value may be irrational. The result is
polynomial time for fixed \(h\), rather than an FPT claim with an exponent
independent of \(h\).

## 2. The classical closedness input

Luo and Zhang's [1997 report, Theorem 1](https://papers.tinbergen.nl/97122.pdf)
establishes the following fact. For finitely many convex quadratic functions
\(f_i\), if systems \(f_i(x)\le\varepsilon_i^{(k)}\) are feasible
for positive right-hand sides tending to zero, then \(f_i(x)\le0\)
is feasible. The report's Corollary 2 deduces finite infimum attainment for
convex quadratic objectives over convex quadratic systems. Affine inequalities
have zero Hessian; affine equalities are pairs of affine inequalities. These
results therefore apply to \(F\) above without a Slater assumption.

We inspected Theorem 1 and Corollary 2, including their proofs, on printed
pages 3--7. The report attributes the attainment result to Terlaky's 1985
work. The later article is Luo and Zhang, *On Extensions of the Frank-Wolfe
Theorems*, Computational Optimization and Applications 13 (1999), 87--110,
[DOI](https://doi.org/10.1023/A:1008652705980). The report supplies the theorem
numbering used here; the published bibliographic information was checked
against [the authors' institutional record](https://experts.umn.edu/en/publications/on-extensions-of-the-frank-wolfe-theorems/).

## 3. Value degree and height

### 3.1 Restrict at an attained optimizer

Assume feasibility and a finite infimum. The preceding classical result gives
an optimizer \(x^*\). Apply the active affine restriction from
[the bounded value proof](hessian-span-reduction.md).

Keep the original affine equations. Replace affine inequalities active at
\(x^*\) by equations, delete the inactive affine inequalities, and retain
only native quadratic rows active at \(x^*\). The reduced problem still
has value \(\theta\): a better retained-feasible point would, on a short
segment from \(x^*\), preserve the deleted rows' strict slack and improve
the original objective by convexity.

Let \(I\) be the retained quadratic indices. Choose \(B\subseteq I\)
whose Hessians form a basis of their span, with \(|B|\le h\), and write

\[
 Q_i=\sum_{j\in B}c_{ij}Q_j,\qquad c_{ij}\in\mathbb Q.
\]

Impose the affine equations
\(q_i-\sum_{j\in B}c_{ij}q_j=0\). They all hold at \(x^*\), so
the restricted problem has the same value. Rational elimination gives

\[
 x=x_0+Vu,\qquad u\in\mathbb R^d,
\]

with all coefficients of polynomial bit length in \(N\). These coefficient
bounds do not depend on the coordinates of \(x^*\). On this affine space,
the retained polynomials satisfy the whole-polynomial identities

\[
 \widetilde q_i=\sum_{j\in B}c_{ij}\widetilde q_j,
 \qquad
 \nabla\widetilde q_i=\sum_{j\in B}c_{ij}
                                  \nabla\widetilde q_j.          \tag{3}
\]

If \(d=0\), the value is rational with polynomial bit length. Assume
\(d>0\) below. Denote the retained optimizer's parameter by \(u^*\).

### 3.2 Regularized values converge without a compactness argument

For \(0<\varepsilon<1\), consider

\[
 \theta_\varepsilon=
 \min\{\widetilde q_0(u)+\varepsilon\|u\|_2^2:
                 \widetilde q_i(u)\le\varepsilon\ (i\in I)\}.
                                                               \tag{4}
\]

Its feasible set is closed and contains the strictly feasible point \(u^*\).
Its objective has Hessian \(\widetilde Q_0+2\varepsilon I\succ0\),
so it is coercive and has a unique minimizer \(u_\varepsilon\).
Slater's condition applies to each problem (4). It is not an assumption on
the original problem.

Using \(u^*\) as a competitor gives

\[
 \theta_\varepsilon\le\theta+\varepsilon\|u^*\|_2^2,
 \qquad \limsup_{\varepsilon\downarrow0}\theta_\varepsilon\le\theta.
                                                               \tag{5}
\]

For the reverse inequality, suppose some \(\delta>0\) and sequence
\(\varepsilon_k\downarrow0\) satisfy
\(\theta_{\varepsilon_k}\le\theta-\delta\). Since the norm
regularizer is nonnegative, the associated optimizers satisfy

\[
 \widetilde q_i(u_{\varepsilon_k})\le\varepsilon_k\quad(i\in I),
 \qquad
 \widetilde q_0(u_{\varepsilon_k})-(\theta-\delta)\le0.
\]

The closedness theorem applies to this finite system of convex quadratics,
including the shifted objective as one extra row. Its coefficients need not
be rational for this application. We can relax that last row by
\(\varepsilon_k\) as well, so every right-hand side is positive. It gives
a point satisfying all retained rows at zero and having objective at most
\(\theta-\delta\), contrary to their optimal value \(\theta\).
Therefore

\[
 \lim_{\varepsilon\downarrow0}\theta_\varepsilon=\theta.       \tag{6}
\]

No bound on the sequence \(u_\varepsilon\) is used. The shifted objective
row above is used only for this qualitative limiting argument; it is not
added to the sparse KKT system or to its native Hessian count.

### 3.3 Compress stationarity and eliminate the primal variables

At each regularized optimum, choose nonnegative KKT multipliers. By (3), the
native multiplier contribution to stationarity depends only on
\(\sum_{i\in I}\lambda_i c_i\in\mathbb R^{|B|}\). Conic
Caratheodory reduction using only currently active rows preserves this vector
with at most \(h\) nonzero multipliers. Stationarity is preserved by (3),
and complementarity is preserved because all selected rows are active.

Choose one support \(J\subseteq I\), \(|J|\le h\), that occurs along
a sequence \(\varepsilon\downarrow0\). Put

\[
 M=\widetilde Q_0+2\varepsilon I+
                            \sum_{i\in J}\lambda_i\widetilde Q_i\succ0,
 \quad \Delta=\det M,
 \quad p=-\operatorname{adj}(M)
                   \left(\widetilde a_0+\sum_{i\in J}\lambda_i
                                                     \widetilde a_i\right).
\]

Stationarity reconstructs \(u=p/\Delta\). Define

\[
 G_i=\tfrac12p^T\widetilde Q_i p+
          \Delta\widetilde a_i^Tp+
          (\widetilde c_i-\varepsilon)\Delta^2\quad(i\in I),
\]

and

\[
 G_0=\tfrac12p^T\widetilde Q_0p+
          \Delta\widetilde a_0^Tp+
          (\widetilde c_0-w)\Delta^2+\varepsilon p^Tp.
\]

Let \(\mathcal K_J(\varepsilon,w,\lambda)\) contain

\[
 \Delta>0,\quad \lambda_i\ge0\ (i\in J),\quad
 G_i\le0\ (i\in I),\quad
 \lambda_iG_i=0\ (i\in J),\quad G_0=0.              \tag{7}
\]

Every retained primal row occurs, including rows outside \(J\). Every
solution of (7) with \(\varepsilon>0\) is a KKT certificate for (4),
so its \(w\) equals \(\theta_\varepsilon\). The chosen sequence
has certificates with this support. All polynomial degrees are \(O(N)\),
coefficient bit lengths are polynomial in \(N\), and the number of
polynomials is polynomial in \(N\). Determinant expansions and common
denominator clearing have the same coefficient bounds established in the
[bounded proof, Step 3](hessian-span-reduction.md).

The formula

\[
 \forall\gamma\;\left[\gamma\le0\ \lor\
  \exists\varepsilon,w,\lambda\;
   \bigl(0<\varepsilon<1,\ \varepsilon<\gamma,
        -\gamma<w-a<\gamma,\ \mathcal K_J\bigr)\right]           \tag{8}
\]

defines exactly \(\{\theta\}\), by the fixed-support sequence and
(6). It has one universal variable, at most \(h+2\) existential variables,
and one free variable. Coefficient-sensitive block quantifier elimination
therefore gives degree and coefficient bit bounds \(N^{O(h+1)}\).
The source is Basu--Pollack--Roy, *Algorithms in Real Algebraic Geometry*,
Theorem 14.16, also stated as [Theorem 2.27 of Basu's author survey](https://arxiv.org/abs/1409.1534).
The input has a fixed number of blocks; the primal dimension only enters
the polynomial degree and coefficient size after stationarity elimination.

After zero polynomials are removed, some output polynomial must vanish at
\(\theta\). Otherwise every remaining sign would be constant in a
neighborhood, contradicting the singleton in (8). This proves (1). Cauchy's
bound applied to an annihilating polynomial gives the upper magnitude bound
in (2); after removing any powers of its indeterminate, the reciprocal
polynomial gives the nonzero lower bound. No algorithm needs to discover the
active set or the selected KKT support used in this proof.

## 4. Exact status and value computation

### 4.1 Infeasibility and unboundedness

First apply [exact continuous feasibility without a box](unbounded-hessian-span.md#2-exact-continuous-feasibility-without-a-box)
to \(F\). This is polynomial time for fixed \(h\). If it is nonempty,
compute the integer

\[
 B=2^{N^{C(h+1)}+2}
\]

using an effective constant sufficient for (2), and decide feasibility of

\[
 F\cap\{x:q_0(x)\le-B\}.                           \tag{9}
\]

If the finite optimum exists, it exceeds \(-B\), so (9) is infeasible.
If the objective is unbounded below, (9) is feasible. These are the only
possibilities for a nonempty \(F\). Thus one exact feasibility query
distinguishes them. The objective-threshold row increases the constraint
Hessian span by at most one. The threshold has \(N^{O(h+1)}\) bits.
Feeding this larger input to the unbounded feasibility algorithm still gives
polynomial time for every fixed \(h\). No sharp combined parameter exponent
is claimed here.

### 4.2 Certified value approximation

Assume the finite case. Start with \([-B,B]\), containing \(\theta\).
At each rational midpoint \(t\), decide feasibility of

\[
 F\cap\{x:q_0(x)\le t\}.                            \tag{10}
\]

Attainment ensures that (10) is feasible precisely when \(\theta\le t\).
Keep the half interval that contains \(\theta\). To obtain absolute
error less than \(2^{-s}\), only \(O(\log B+s)\) queries are needed.
Their bit lengths are polynomial in \(N^{O(h+1)}+s\); their native span
is at most \(h+1\). For fixed \(h\), this is polynomial in \(N+s\).
The rational interval is certified by exact decisions; the method does not
assume that numerical feasible points solve the original constraints.

### 4.3 Recovering the selected algebraic value

The primitive minimal polynomial of \(\theta\) has degree at most \(D\)
and coefficient bit lengths polynomial in \(D,H\). For example, Gauss's
lemma and Cauchy's bound applied to an annihilator give the sufficient
coefficient bound

\[
 H_{\min}\le(D+1)H+2D+O(1).
\]

The Kannan--Lenstra--Lovasz recognition algorithm recovers that polynomial
from an approximation requiring \(O(D^2+DH_{\min})\) accuracy bits,
in polynomial time in \(D,H_{\min}\). An additional approximation at a
standard root-separation precision gives a rational interval isolating the
correct real conjugate. The precise source theorem and an explicit
discriminant-based isolating-interval proof are recorded in the
[independent algebraic-recognition audit](algebraic-recognition-source-review.md).
All required approximation calls are supplied by Section 4.2. This proves the
algorithmic corollary.

## 5. Significance, prior work, and limits

The result removes boundedness from the batch's value and exact continuous
optimization statements. It applies with arbitrarily many variables and
constraints, degenerate feasible sets, and an objective Hessian independent
of the constraint span. It could support exact continuous-node decisions in
MINLP or exact value comparisons between integer assignments. These are
theoretical capabilities. Efficient implementations would still need much
sharper instance-dependent bounds and practical algebraic recovery.

The value-height reduction is the candidate contribution; attainment,
closedness, quantifier elimination, and algebraic recognition are established
ingredients. The [Hessian-span literature audit](hessian-span-prior.md)
compares fixed constraint-count, generic algebraic-degree, and exact
mixed-integer quadratic results. The unbounded extension does not alter
those priority qualifications. No failed search establishes originality.

Terlaky's [*On lp programming*, European Journal of Operational Research 22
(1985), 70--100](https://doi.org/10.1016/0377-2217(85)90116-X) is relevant
earlier work. Its bibliographic entry and abstract were checked; its full
proof was not independently inspected here. The attribution of finite
attainment to that paper follows Luo and Zhang's explicit statement.

Several boundaries matter:

- Convexity of the objective is used both in active-row deletion and in
  the closedness argument for (6). The theorem does not cover arbitrary
  indefinite objectives.
- This proof concerns continuous optimization. It does not infer mixed-
  integer attainment or a uniform bound on optimal integer assignments.
- The feasible-point radius theorem alone does not supply a radius
  containing an optimizer of an unrelated objective. We use value
  regularization and closedness to avoid that inference.
- Recovering the value does not directly recover an optimizer. Describing
  the optimal set by the algebraic threshold \(q_0\le\theta\) changes
  the coefficient domain; applying a rational-input witness algorithm to it
  requires an additional argument.
- The strong exact conclusions depend on fixing the Hessian-span dimension.
  There is no claim of a general polynomial-time exact QCQP algorithm.

## 6. Verification record

The author reread the active restriction, multiplier compression, determinant
coefficient bounds, and the finite-value cutoff independently of the original
bounded proof. The source check inspected Luo--Zhang Theorem 1 and Corollary 2
and their proofs. A separate agent completed an
[adversarial review](unbounded-value-review.md) of the unbounded value
argument, source applicability, and algorithmic consequences. The reviewer
then read the saved manuscript and independently checked the
Kannan--Lenstra--Lovasz primary theorem for its recovery step. The review
found no mathematical gap and prompted one wording correction: replacing
active inequalities by equations makes a reduced problem, not necessarily
an enlarged feasible set.

No numerical test or Lean formalization establishes the universal theorem.
The argument is a symbolic proof using the cited classical results. Local
checks were restricted to this manuscript: `git diff --check --
research-20260927/unbounded-value-optimization.md` and an inline `python -`
check of final newline, trailing whitespace, control characters, paired math
delimiters, and local Markdown links passed. Project-wide verification and
CI inspection were not run. These checks verify document integrity, not the
mathematical theorem.
