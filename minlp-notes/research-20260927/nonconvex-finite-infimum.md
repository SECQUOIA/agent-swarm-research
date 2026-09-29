# Finite infima of nonconvex quadratic systems with few Hessian directions

Date: 2026-09-27. Status: proof, a fresh independent review, a separate
algebra-only review, and a root reread completed; no gap was found.
Publication priority remains unestablished.

The algebraic value bound extends to unbounded nonconvex domains even when
the infimum is not attained. The proof uses two ordered limits: remove a
small perturbation inside a fixed box, then let the box grow. Interchanging
these limits would be incorrect.

## 1. Statement

Let

\[
 S=\{x\in\mathbb R^n:Ax\le b,\ Ex=e,\ q_i(x)\le0
                                   \ (i=1,\ldots,m)\}
\]

be defined by rational affine rows and rational quadratic polynomials. No
convexity, boundedness, or constraint qualification is assumed. Let \(q_0\)
be an arbitrary rational quadratic objective, and let

\[
 h=\dim_{\mathbb Q}\operatorname{span}
                   \{\nabla^2q_i:i=1,\ldots,m\}.
\]

The objective Hessian is excluded from \(h\). Let \(N\ge2\) denote
the total explicit binary input length, including the objective.

**Finite-infimum theorem.** If \(S\ne\varnothing\) and
\(\theta=\inf_{x\in S}q_0(x)>-\infty\), then \(\theta\) is a root
of a nonzero integer polynomial whose degree and coefficient bit lengths
are \(N^{O(h+1)}\). The bound does not require attainment.

For every fixed \(h\), a deterministic algorithm with an NP oracle can
classify the problem as infeasible, unbounded below, or having finite
infimum. In the last case it returns the exact infimum as a primitive
integer minimal polynomial and a rational isolating interval. Its running
time and oracle-query lengths are polynomial in \(N\) for fixed \(h\).
This is an \(\mathrm{FP}^{\mathrm{NP}}\) statement, not a polynomial-time
algorithm without an oracle. No optimizer or attainment decision is claimed.

The proof uses the reviewed
[nonconvex perturbation argument](nonconvex-hessian-span-frontier.md) and
[finite-quotient elimination lemma](explicit-span-separation.md). Its new
step is retaining the growing radius as a coefficient parameter through
that lemma, then extracting its leading coefficient after the inner limit.

## 2. A two-parameter version of the elimination lemma

Let

\[
 G_1,\ldots,G_s,A,B
       \in\mathbb Z[R,\varepsilon,\lambda_1,\ldots,\lambda_s]
\]

have degree at most \(a\ge1\) in \(\lambda\), bounded finite degree
in \(R,\varepsilon\), and coefficient \(\ell_1\)-norm at most
\(2^\tau\), \(\tau\ge1\). Suppose:

- \(R_\nu\to+\infty\);
- for each \(\nu\), there is a sequence
  \(\varepsilon_{\nu,\mu}>0\) tending to zero, with roots
  \(\lambda_{\nu,\mu}\) of the \(G\) system at that parameter;
- those roots satisfy
  \(\det(\partial G/\partial\lambda)\ne0\) and \(A\ne0\);
- \(B/A\to v_\nu\) as \(\mu\to\infty\), and
  \(v_\nu\to\theta\in\mathbb R\) as \(\nu\to\infty\).

Set

\[
 D=a+1,\quad L=D^s,\quad T=a(s+1),\quad
 K=L\left[\tau(T+1)+2+\lceil\log_2L\rceil\right].       \tag{1}
\]

**Ordered-limit lemma.** Some nonzero \(P\in\mathbb Z[t]\) satisfies
\(P(\theta)=0\), \(\deg P\le L\), and \(\|P\|_1\le2^K\).
The statement includes \(s=0\), with \(L=1\).

### Proof

Repeat the finite-quotient construction over
\(\mathbb Q(R,\varepsilon,\delta)\), deforming the equations to

\[
 G_i+\delta\lambda_i^D=0.
\]

The pairwise coprime leading monomials \(\lambda_i^D\) give the fixed
quotient basis with exponents below \(D\) in every variable. After
multiplying the multiplication matrices for \(A,B\) by \(\delta^T\),
their entries are integer polynomials in \(R,\varepsilon,\delta\),
with coefficient norm at most \(2^{\tau(T+1)}\). This bound uses the
coefficient norm in **all** parameter variables. Multiplication and addition
have the same norm estimates whether the coefficient ring is
\(\mathbb Z[\varepsilon]\) or \(\mathbb Z[R,\varepsilon]\).

Introduce \(\zeta\) and form the determinant

\[
 H(R,\varepsilon,\delta,t,\zeta)
  =\det(t\widetilde M_A-\widetilde M_B-\zeta\delta^T I_L).
                                                               \tag{2}
\]

Its leading \(\zeta\) coefficient is \((-\delta^T)^L\), so it is
nonzero. Its degree in \(t\) is at most \(L\) and its coefficient
norm is at most \(2^K\).

Extract the coefficient of the lowest occurring power of \(\zeta\),
then the coefficient of the lowest occurring power of \(\delta\).
Exactly as in the original lemma, nonsingularity of each selected root
allows an implicit-function branch as \(\delta\to0\), and the
corresponding multiplication-matrix eigenvalue makes the extracted
polynomial vanish. We obtain a nonzero
\(Q(R,\varepsilon,t)\in\mathbb Z[R,\varepsilon,t]\) satisfying

\[
 Q\left(R_\nu,\varepsilon_{\nu,\mu},
             (B/A)_{\nu,\mu}\right)=0                 \tag{3}
\]

for every selected \((\nu,\mu)\). This remains valid when a particular
specialization makes an extracted coefficient identically zero; the
original lemma's factor argument expressly permits that case.

Let \(r\) be the least \(\varepsilon\)-exponent in \(Q\), and write

\[
 Q(R,\varepsilon,t)=\varepsilon^r V(R,t)
                         +O(\varepsilon^{r+1}),\qquad V\ne0.
\]

Fix \(\nu\), divide (3) by \(\varepsilon_{\nu,\mu}^r\), and
let \(\mu\to\infty\). All coefficients in this inner limit have
the fixed finite parameter \(R_\nu\). Thus

\[
 V(R_\nu,v_\nu)=0.                                  \tag{4}
\]

Finally let \(\ell\) be the **largest** \(R\)-exponent in \(V\),
and write

\[
 V(R,t)=R^\ell P(t)+\sum_{j<\ell}R^j P_j(t),\qquad P\ne0.
\]

Divide (4) by \(R_\nu^\ell\) and let \(\nu\to\infty\).
The bounded convergent sequence \(v_\nu\) makes every lower-power
term vanish, giving \(P(\theta)=0\). Coefficient extraction never
increases the norm or the degree in \(t\), proving (1).

There is no uniform convergence claim in \(R\), no diagonal selection
of \(\varepsilon\) as a function of \(R\), and no requirement that
the primal or multiplier vectors converge in the outer limit.

## 3. Lift and exhaust the feasible set by boxes

As in the nonconvex certificate note, choose a Hessian basis, introduce
\(y_j=\tfrac12x^TB_jx\), and write the lifted system as

\[
 w=(x,y)\in P,\qquad F_j(w)=0\quad(j=1,\ldots,h),       \tag{5}
\]

where \(P\) is a rational polyhedron and every \(F_j\) is quadratic.
All lift data have polynomial bit length in \(N\). Define

\[
 P_R=P\cap[-R,R]^{n+h},\qquad
 v(R)=\min\{q_0(x):w\in P_R,\ F_j(w)=0\ (1\le j\le h)\}.
                                                               \tag{6}
\]

For all sufficiently large \(R\), this compact set is nonempty:
any one original feasible point has finite lifted coordinates. The sets in
(6) increase with \(R\) and their union is the entire lifted feasible
set. Therefore, when the original infimum is finite,

\[
 v(R)\downarrow\theta\quad\text{as }R\to+\infty.       \tag{7}
\]

Bounding every lifted coordinate by the same \(R\) is enough. No
quadratic expression in \(R\) is needed in the box rows, and no numerical
upper bound on an original feasible point is used in the encoding argument.

## 4. Radius-dependent affine charts

Every affine row of \(P_R\) has a coefficient vector independent of
\(R\), and a right-hand side affine in \(R\). For any subset of active
rows, select independent coefficient rows. Rational elimination of these
rows gives

\[
 w=a+bR+Vu,                                           \tag{8}
\]

where \(a,b,V\) are rational and have polynomial coefficient bit lengths
in \(N\). The matrix \(V\) has full column rank. In particular, neither
its entries nor the denominators in (8) depend on the numerical size of
\(R\).

Any remaining selected row becomes an affine consistency equation in
\(R\). Either it vanishes identically or it holds at at most one value
of \(R\). Across the finitely many row subsets, discard all these
exceptional radius values. There are still arbitrarily large positive
integers available for \(R\). Every active affine system at a retained
radius is one of the identically consistent charts (8).

This covers affine equalities, dependent active rows, and changing active
faces. The number of charts may be exponential; their individual coefficient
bit bounds are uniform, and only one chart is eventually used for the
annihilator proof.

## 5. One generic perturbation works along the parameter family

Choose quadratic perturbation polynomials \(P_0,P_1,\ldots,P_h\) in
\(w\) and consider, inside the fixed box polyhedron \(P_R\),

\[
 \min\ r_\varepsilon(w):=q_0(x)+\varepsilon P_0(w)
 \quad\text{subject to}\quad
 |F_j(w)+\varepsilon^2P_j(w)|\le\varepsilon.           \tag{9}
\]

Use the genericity lemma in Section 4 of the
[nonconvex certificate proof](nonconvex-hessian-span-frontier.md): on a
positive-dimensional affine chart, active gradients are independent and
both the multiplier Hessian and the bordered KKT matrix are nonsingular;
more active nonlinear rows than the chart dimension are excluded.

For every fixed \(R\) and nonzero \(\varepsilon\), restriction of
arbitrary ambient perturbation quadratics to (8) is surjective onto all
quadratics in the free variables. Consequently each nonzero bad-set
polynomial, after substitution of (8)--(9), is a nonzero polynomial in
\((R,\varepsilon,\text{perturbation coefficients})\). Its degree is
at most \(2^{\operatorname{poly}(N)}\). Take one nonzero coefficient
in its expansion in **both** \(R\) and \(\varepsilon\), and avoid
the product of these coefficients over all charts and oriented active
subsets. The integer-grid argument gives a single choice of the \(P_j\)
with polynomial-bit integer coefficients, independent of \(R\).

After this choice, every bad polynomial in \((R,\varepsilon)\) is
nonzero. The values of \(R\) at which it vanishes identically as a
polynomial in \(\varepsilon\) form a finite set: they must be roots
of any one nonzero coefficient polynomial in \(R\). Discard the finite
union of these sets. For each remaining fixed \(R\), all the generic
conclusions hold for every sufficiently small positive \(\varepsilon\).
The admissible smallness threshold may depend on \(R\).

At most one orientation of any band can be active, so there are at most
\(h\) active nonlinear rows. The perturbation argument never requires
that a path be generic uniformly over every numerical radius.

## 6. Inner minimizers and a fixed chart subsequence

Fix a sufficiently large, nonexceptional \(R\). An original optimizer
in (6) satisfies the bands in (9) for sufficiently small \(\varepsilon\).
The perturbed feasible set is closed and contained in compact \(P_R\),
so the perturbed optimum exists. Uniform convergence of
\(r_\varepsilon\) to \(q_0\) on this one compact polyhedron and the
usual subsequence argument give

\[
 \min\text{(9)}\longrightarrow v(R)
                       \quad\text{as }\varepsilon\downarrow0.  \tag{10}
\]

For the lower bound, every primal cluster point satisfies all equations in
(5), and hence has objective at least \(v(R)\). The original optimizer
gives the upper bound. Coercivity is unnecessary inside a fixed box; the
objective and all native Hessians may be indefinite.

At each perturbed minimizer, restrict the active affine rows to their chart.
The remaining affine rows are strictly slack locally, so the minimizer is
a local minimizer in that chart. The genericity lemma gives an ordinary
KKT certificate and the two nonsingular matrices. For each fixed \(R\),
select a sequence \(\varepsilon\downarrow0\) with one constant chart
and one constant oriented active subset. There are finitely many choices.
Along a sequence \(R_\nu\to+\infty\), select the same chart and active
subset for every inner sequence.

If this chart has dimension zero, then \(w=a+bR\). Its limiting inner
value is the quadratic polynomial \(q_0(a+bR)\), with rational
coefficients of polynomial bit length. A finite limit as \(R\to\infty\)
forces the coefficients of its positive powers to vanish. The remaining
constant is a rational number with polynomial bit length, proving the
theorem in this case. Assume henceforth that the chart dimension is
\(d>0\), and let \(s\le h\) denote the active nonlinear count.

## 7. The common parameterized KKT system

Stationarity on the selected chart has the form

\[
 M(R,\varepsilon,\lambda)u=-a_0(R,\varepsilon)
                         -\sum_{i=1}^s\lambda_i a_i(R,\varepsilon).
\]

Its determinant \(\Delta\) is nonzero at the selected roots. Set the
adjugate numerator to \(p\); then \(u=p/\Delta\). Substitute this
expression into the \(s\) active equalities and multiply by
\(\Delta^2\), obtaining

\[
 G_i(R,\varepsilon,\lambda)=0\quad(i=1,\ldots,s).      \tag{11}
\]

As in the preceding proof, the multiplier Jacobian at the selected roots
is \(-\Delta^2 JM^{-1}J^T\), where \(J\) is the active-gradient
matrix. Nonsingularity of both \(M\) and the bordered KKT matrix makes
this Jacobian nonsingular. No definiteness assumption is used.

The objective value \(r_\varepsilon(a+bR+Vp/\Delta)\) is a rational
output \(B/A\), with \(A=\Delta^2\) before denominator clearing.
All these expressions have degree \(O(d+1)\) in the multipliers and
polynomial degree in \(R,\varepsilon\). Their coefficient norm has
logarithm polynomial in \(N\). In particular, the radius occurs as a
formal variable: the bound does not include \(\log R_\nu\).

The reason is that substitution of (8) makes the coefficients of the
restricted quadratics polynomials in \(R\) of degree at most two.
Denominators remain fixed rational input denominators. Determinants,
adjugates, and quadratic substitution raise degrees by only \(O(d)\)
and increase logarithmic coefficient norms polynomially. A common positive
integer clears every denominator; multiplying \(A,B\) by the same
factor preserves their ratio.

Equations (7), (10), and (11) meet the ordered-limit lemma's assumptions.
Take \(a=O(d+1)\), \(s\le h\), and \(\tau=N^{O(1)}\) there.
Its conclusion gives the finite-infimum annihilator with degree and
coefficient bit lengths \(N^{O(h+1)}\).

### Why the order of limits is essential

On \(xy=1\), \(x,y\ge0\), and \(x,y\le R\), minimize
\(x-\varepsilon y^2\). For \(R\ge1\), the value is

\[
 v_\varepsilon(R)=1/R-\varepsilon R^2,
 \qquad Rv_\varepsilon(R)+\varepsilon R^3-1=0.
\]

The ordered limit \(\varepsilon\downarrow0\), then \(R\to\infty\),
is zero. Taking \(\varepsilon=1/R\) instead gives divergence to
\(-\infty\). Extracting the lowest \(\varepsilon\) power first gives
\(Rt-1\), whose highest \(R\) coefficient is \(t\). Reversing the
extractions gives \(\varepsilon\), then the constant one. The proof
uses exactly the valid order and makes no diagonal-limit claim.

## 8. Separate structural size from coefficient bit length

The dependence on coefficient size can be tracked more precisely. Let
\(S_0\ge2\) bound the number of scalar coefficient positions, rows,
variables, and the bit lengths of their indices. Let \(\tau_0\ge1\)
bound the numerator and denominator bit lengths of each rational input
coefficient. A dense encoding may be used; replacing a sparse quadratic
input by this encoding increases structural size only polynomially.

The proof gives bounds of the form

\[
 \deg P\le S_0^{C(h+1)},\qquad
 \log_2\|P\|_1\le(\tau_0+1)S_0^{C(h+1)}             \tag{12}
\]

after increasing one effective absolute constant \(C\). The same
coefficient-sensitive bound applies to the coordinate annihilators in the
nonconvex feasible-point theorem. Here is the accounting:

- Rational basis extraction and affine elimination use bounded-size
  determinants, giving coefficient bits
  \((\tau_0+1)S_0^{O(1)}\).
- The bad-set degree and the number of charts depend on structural size,
  not coefficient magnitudes. Thus the perturbation grid gives coefficient
  bits \(S_0^{O(1)}\), independently of \(\tau_0\).
- The reduced KKT polynomial coefficient norm has logarithm
  \((\tau_0+1)S_0^{O(1)}\). Determinant expansions and a common
  denominator preserve linear dependence on input coefficient bits.
- The explicit bound \(K\) in (1) is linear in that logarithmic norm;
  its remaining factors are \(S_0^{O(h+1)}\).
- Passing to minimal polynomials, a bounded primitive generator, and the
  trace-matrix representation multiplies height bounds by polynomials in
  the algebraic degree. Their coefficient-bit bounds remain linear in
  \(\tau_0+1\) times \(S_0^{O(h+1)}\).

Consequently a radius with
\(\log R\le(\tau_0+1)S_0^{O(h+1)}\) can be appended without
forcing a quadratic exponent in \(h\) upon a second application of these
bounds. The number of new affine rows is only linear in the dimension;
the structural size stays polynomial in \(S_0\), while the new coefficient
bit bound becomes \((\tau_0+1)S_0^{O(h+1)}\). Multiplication by another
\(S_0^{O(h+1)}\) preserves this form. This refinement concerns the
proved encoding bounds; any algorithmic consequence must also track its
own arithmetic and oracle costs.

## 9. Exact classification and value recovery with an NP oracle

Fix \(h\). Exact feasibility for the original system, or for that system
with a supplied rational objective threshold \(q_0(x)\le t\), is in NP
by the [algebraic-witness corollary](nonconvex-hessian-span-frontier.md).
The threshold increases the native Hessian span by at most one. A separate
[source audit](nonconvex-hessian-span-prior-audit.md) supplies the shorter
feasibility proof from classical Grigoriev--Pasechnik sampling and a
minimum-dimensional polyhedral face. The oracle consequence does not rely
on claiming that feasibility argument as new.

First query feasibility. If the answer is no, report infeasibility. Otherwise
use the degree and height bounds just proved, including the elementary
factor bound if needed, to compute an integer \(M\) of polynomial bit
length for fixed \(h\) such that every finite infimum of this input has
\(|\theta|<M\). For example, an annihilator coefficient-bit bound
\(H\) permits \(M=2^{H+2}\) by Cauchy's root bound.

Query feasibility with \(q_0\le-M-1\). If yes, the infimum cannot be
finite by the proved bound, and the problem is unbounded below. Conversely,
an unbounded-below objective satisfies this threshold somewhere, so this
test is exact. It returns a classification, not a recession ray.

In the finite case, start bisection at
\(a=-M-1\), \(b=M+1\). The lower threshold is infeasible and the
upper threshold is feasible. At every midpoint, use the NP threshold
oracle and replace the corresponding endpoint. The infimum always belongs
to \([a,b]\). If it is unattained and a midpoint equals it, the oracle
answers no, which still preserves this invariant. Thus bisection gives
certified rational approximations to \(\theta\) to any requested
absolute precision, with a number of queries polynomial in the number of
requested bits and \(\log M\).

Apply the established Kannan--Lenstra--Lovasz algebraic-recognition algorithm
to such an approximation and the proved degree and minimal-polynomial
coefficient bounds. Its required precision and bit complexity are polynomial
in the degree and logarithmic coefficient bound. A final approximation
below the discriminant root-separation bound selects the correct real root.
The exact theorem and bit-model statement are recorded in the
[primary-source audit](algebraic-recognition-source-review.md); the source
is [Theorem 1.19 of the 1988 paper](https://www.math.cmu.edu/~af1p/Teaching/AdditiveCombinatorics/LLLL.pdf).

Every query still has polynomial encoding length for fixed \(h\):
bisection increases coefficient bit lengths but only adds one quadratic
row. The recognition algorithm and all other deterministic steps are
polynomial in these degree and bit bounds. This proves the
\(\mathrm{FP}^{\mathrm{NP}}\) statement.

The distinction from attainment is real. The closed system
\(xy\ge1\), \(x\ge0\), has infimum zero for objective \(x\), but
has no point attaining it. Its one native indefinite Hessian has span one.

## 10. Bounded integer variables

The classification and exact-value consequence also holds for rational
total-degree-two mixed-integer systems with explicitly bounded integer
coordinates, when the span of the **continuous** Hessian blocks is fixed.
Joint convexity is not required. Each integer assignment has polynomial
bit length, and substituting it leaves a continuous quadratic system of
uniformly bounded coefficient size and the same span bound. Feasibility
with a rational objective threshold is in NP: guess the integer assignment
and the continuous algebraic certificate.

There are finitely many integer assignments. If any feasible slice is
unbounded below, so is the mixed-integer problem. Otherwise its finite
infimum is the least of the finitely many feasible slice infima, and equals
one of them. The uniform slice encoding bound therefore supplies the same
finite-value bound needed for Section 9. This gives exact classification and
the exact infimum in \(\mathrm{FP}^{\mathrm{NP}}\) for fixed continuous
Hessian span, with arbitrary numbers of bounded integer variables.

This does not return an attained mixed-integer optimizer or remove the
integer bounds. Neither conclusion follows merely from the value algorithm.

## 11. Prior work, interpretation, and remaining checks

Generic algebraic degrees of quadratic optimization are classical; the
closest comparisons for the underlying perturbation are in the
[nonconvex source discussion](nonconvex-hessian-span-frontier.md).
Algebraic value bounds followed by decision bisection and exact recognition
are established tools, not new algorithmic mechanisms.

A directly relevant finite-infimum antecedent is El Hilany and Tsigaridas,
[*Bounds on the infimum of polynomials over a generic semi-algebraic set
using asymptotic critical values*](https://arxiv.org/html/2407.17093v1),
Theorem 1. It gives algebraic degree and height bounds for potentially
unattained infima on its stated complete semialgebraic class. Its hypotheses
include closedness, connectedness, and smooth complete-intersection
conditions for the constraint-subset complex varieties. Its bounds depend
exponentially on the ambient dimension.
The proposed addition here is a uniform quadratic Hessian-span-dependent
bound permitting degenerate data, unbounded dimension, and arbitrarily
many affine and quadratic rows. The author and reviewer independently
inspected the introduction's definition and Theorem 1 in version 1; the
arXiv record listed no later version when checked. This limited comparison
does not establish priority. In particular, possible derivations from
parameterized quadratic-map sampling or other endpoint bounds still deserve
further investigation.

The possible solver capability is exact value classification and an exact
algebraic target for global optimization within a structural class. An NP
oracle represents substantial combinatorial work. The theorem does not
provide a practical algorithm, a speedup, or a short certificate of global
optimality. Extracting usable bounds and exploiting the structure of a
particular problem remain necessary for practical value.

The completed [independent review](nonconvex-finite-infimum-review.md)
checks affine consistency, genericity across the radius parameter, the
ordered coefficient extractions, finite-value classification, the bounded
integer extension, and the coefficient-sensitive accounting. Its separately
staffed algebra reviewer checked the ordered-limit lemma and its unchanged
degree and coefficient bounds. The root independently reread the complete
manuscript. Positive reviews are evidence, not a guarantee.

The review records exact SymPy checks of the limit-order counterexample;
those finite calculations do not establish the general theorem. The author
ran a targeted inline Python check of this note and the revised nonconvex
frontier note for control characters, trailing whitespace, final newlines,
and local links, plus a scoped `git diff --check` for those two files.
No Lean formalization, project-wide verification, or CI inspection was run.

## 12. Addendum: a shorter proof with unknown auxiliary boxes

Added 2026-09-28. Status: proof and a
[fresh independent review](finite-infimum-inactive-box-review.md) completed;
no gap was found.
This proof avoids a formal radius parameter. Sections 2--7 retain the
independently checked radius-parameter proof as an alternate, including its
more general leading-radius coefficient extraction. The theorem, the
coefficient-sensitive bounds, and the prior-work qualifications are unchanged.

### 12.1 Regularize on the original feasible set

Assume \(S\ne\varnothing\) and \(\theta=\inf_S q_0\) is finite.
For \(\varepsilon>0\), put

\[
 f_\varepsilon(x)=q_0(x)+\varepsilon\|x\|^2,
 \qquad v_\varepsilon=\min_{x\in S}f_\varepsilon(x).
                                                               \tag{13}
\]

Since \(q_0\ge\theta\) on the closed set \(S\), the regularized
objective is coercive on \(S\) and attains its minimum. No coercivity
outside \(S\) is claimed. Fix one feasible \(\bar x\). Every exact
regularized minimizer satisfies

\[
 \|x\|^2\le\|\bar x\|^2+
                    \frac{q_0(\bar x)-\theta}{\varepsilon}.
                                                               \tag{14}
\]

Consequently, for each fixed \(\varepsilon\), all its exact minimizers
and their lifts (5) lie in a bounded set. Choose an unknown finite integer
\(R_\varepsilon\) whose lifted box strictly contains all these points.
It may grow arbitrarily as \(\varepsilon\downarrow0\). Its magnitude,
encoding length, and dependence on \(\varepsilon\) will not enter any
polynomial or degree estimate.

The regularized values satisfy

\[
 \theta\le v_\varepsilon
                \le q_0(x)+\varepsilon\|x\|^2
                       \quad\text{for every fixed }x\in S.
\]

First let \(\varepsilon\downarrow0\), then take the infimum over that
fixed feasible \(x\). This proves \(v_\varepsilon\to\theta\). No
convergent sequence of regularized minimizers is required.

### 12.2 One perturbation tuple, independent of every auxiliary box

In the lifted polyhedron \(P\), use the perturbations

\[
 \begin{split}
 r_{\varepsilon,\eta}(w)
     &=q_0(x)+\varepsilon\|x\|^2+\eta P_0(w),\\
 |F_j(w)+\eta^2P_j(w)|&\le\eta\quad(1\le j\le h).
 \end{split}                                                   \tag{15}
\]

Choose the integer quadratic polynomials \(P_j\) using only the active
affine charts \(w=a+Vu\) of the original \(P\). The box rows are
excluded. The genericity proof in the
[attained-optimizer note](nonconvex-attainment-and-optimizer.md), Section 3,
applies with formal parameters \((\varepsilon,\eta)\): at every fixed
\(\varepsilon\) and \(\eta\ne0\), the perturbation coefficient map
onto each chart's objective and selected constraint quadratics is surjective.
Select a nonzero coefficient in these two parameters from each bad-set
polynomial and use the finite integer-grid argument simultaneously over all
charts and oriented active subsets.

This yields one tuple of perturbations with coefficient bits
\(S_0^{O(1)}\), independent of \(\tau_0\), \(\varepsilon\), \(\eta\),
and all \(R_\varepsilon\). The resulting bad polynomials in
\((\varepsilon,\eta)\) are nonzero. Only finitely many \(\varepsilon\)
make any one of them identically zero in \(\eta\). Exclude their finite
union. At each remaining positive \(\varepsilon\), all sufficiently
small positive \(\eta\) give independent active nonlinear gradients,
an invertible multiplier Hessian, and an invertible bordered KKT matrix.
The admissible \(\eta\)-tail may depend on \(\varepsilon\).

### 12.3 The unknown box becomes inactive

Fix such an \(\varepsilon\). Minimize (15) on
\(P\cap[-R_\varepsilon,R_\varepsilon]^{n+h}\). An exact global
minimizer of (13) is inside this box and satisfies the perturbed bands for
all sufficiently small \(\eta\), so the perturbed compact problem has
minimizers. Every cluster of these minimizers as \(\eta\downarrow0\)
satisfies all equations \(F_j=0\). Uniform convergence on this fixed box
and comparison with an exact minimizer show that its value of
\(f_\varepsilon\) is \(v_\varepsilon\).

Every such cluster therefore lies strictly inside the box by its choice.
If arbitrarily small \(\eta\) admitted a boundary minimizer, compactness
would produce a boundary cluster and a contradiction. Thus **all** perturbed
minimizers are box-interior for sufficiently small \(\eta\), at this
fixed \(\varepsilon\). Their KKT affine charts use only original rows
of \(P\). The unknown radius has disappeared before any algebraic
coefficient is formed. This argument does not require a uniform box, a
uniform \(\eta\)-threshold, or a semialgebraic choice of the boxes.

For each admissible \(\varepsilon\), select an \(\eta\)-sequence
with a constant chart and a constant oriented nonlinear active subset.
Then choose admissible \(\varepsilon_\nu\downarrow0\) and retain the
same chart/subset across infinitely many \(\nu\). These choices come
from a fixed finite family independent of all box sizes. The inner objective
limits are \(v_{\varepsilon_\nu}\), and their outer limit is \(\theta\).
Inner primal subsequences may be chosen for the compactness argument, but
there is no assumption of an outer primal or multiplier limit.

### 12.4 Two small-parameter coefficient extractions

If the selected chart has dimension zero, it is one fixed rational point
\(a\). The inner value is \(q_0(a_x)+\varepsilon\|a_x\|^2\), so its
outer limit is the rational number \(q_0(a_x)\), of polynomial coefficient
size. Otherwise use the same adjugate elimination as in Section 7, now with
formal coefficients in \(\mathbb Q[\varepsilon,\eta]\) and at most
\(h\) active multipliers. The multiplier Jacobian is nonsingular by the
same bordered-matrix Schur complement.

The rational output is the **perturbed objective value**
\(r_{\varepsilon,\eta}(a+Vp/\Delta)\). Its numerator and denominator,
and the reduced KKT equations, have multiplier degree \(S_0^{O(1)}\),
parameter degree \(S_0^{O(1)}\), and coefficient norm logarithm
\((\tau_0+1)S_0^{O(1)}\). No unknown radius appears. The finite-quotient
construction gives a nonzero relation

\[
 Q(\varepsilon,\eta,t)=0
\]

at every selected output, with output degree \(S_0^{O(h+1)}\) and
coefficient norm logarithm \((\tau_0+1)S_0^{O(h+1)}\).

Extract the lowest nonzero \(\eta\)-coefficient, divide by that power,
and take the inner limit at each fixed \(\varepsilon_\nu\). The resulting
nonzero polynomial \(V(\varepsilon,t)\) satisfies
\(V(\varepsilon_\nu,v_{\varepsilon_\nu})=0\). Extract its lowest
nonzero \(\varepsilon\)-coefficient and use
\(v_{\varepsilon_\nu}\to\theta\). The resulting nonzero integer
polynomial annihilates \(\theta\). Coefficient extraction preserves the
bounds, proving (12) again. Specializations that make an intermediate
coefficient identically zero cause no difficulty; its relation is then
identically satisfied at that specialization.

Primal divergence is compatible with this argument. On
\(xy=1\), \(x\ge0\), minimize \(q_0=x^2\). The infimum is zero
and is unattained. The exact regularized value is
\(v_\varepsilon=2\sqrt{\varepsilon(1+\varepsilon)}\), while
\(x_\varepsilon=(\varepsilon/(1+\varepsilon))^{1/4}\) and
\(y_\varepsilon=1/x_\varepsilon\) diverges. The value relation
\(t^2-4\varepsilon(1+\varepsilon)=0\) has lowest
\(\varepsilon\)-coefficient \(t^2\), which correctly vanishes at the
finite infimum. The proof needs precisely this finite scalar limit.
