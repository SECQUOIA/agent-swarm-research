# Alternative perturbation proof of the low-dimensional polynomial bound

Date: 2026-09-28. Status: independent proof review completed. No gap was
found in the statement below, with the qualifications recorded here. A
second reviewer independently checked the genericity argument. This is a
supporting bound for the common-range optimization work, not a novelty
claim or an algorithm for constructing the generic perturbation. The
[main review](common-range-lowdim-review.md) gives a simpler deduction
from classical quantifier elimination. This alternative is retained for
its explicit degree estimate and the checks of the ordered limits.

Let

\[
 D=\{u\in\mathbb R^r:p_i(u)\le0\ (1\le i\le m)\}
\]

be nonempty, where the rational polynomials \(p_i\) and a rational
objective \(g\) have degree at most four. Each rational coefficient has
numerator and denominator bit lengths at most \(\tau\ge1\). There is
an effective function \(F\), depending only on \(r\), with the following
properties:

- If \(\theta=\inf_D g\) is finite, it has a nonzero integer annihilator
  of degree at most \(5^{2r}\) and coefficient bits at most
  \(F(r)(\tau+\log(m+1)+1)\).
- If the infimum is attained, some optimizer of minimum Euclidean norm
  has coordinate annihilators satisfying these bounds. The common field
  has degree at most \(5^{2r^2}\), and a rational univariate description
  has total bits at most \(F(r)(\tau+\log(m+1)+1)\), after increasing
  \(F\).

The case \(r=0\) is the constant-objective case and is immediate. The
argument below assumes \(r\ge1\). Equalities can be represented by
opposite weak inequalities. No convexity, boundedness, constraint
qualification, or attainment assumption is needed for the first claim.

## 1. Regularization and the unknown boxes

For every \(\varepsilon>0\), set

\[
 g_\varepsilon(u)=g(u)+\varepsilon\|u\|^2,
 \qquad v_\varepsilon=\min_D g_\varepsilon.
\]

Since \(g\ge\theta\) on the closed set \(D\), the regularized objective
is coercive on \(D\). Its global minimizer set is nonempty and compact.
Choose a box \([-R_\varepsilon,R_\varepsilon]^r\) containing this whole
set strictly in its interior. The radius may depend on \(\varepsilon\),
and no encoding bound for it is used. For every fixed \(a\in D\),

\[
 \theta\le v_\varepsilon
 \le g(a)+\varepsilon\|a\|^2.
\]

Taking \(\varepsilon\downarrow0\), followed by feasible \(a\) with
\(g(a)\downarrow\theta\), proves \(v_\varepsilon\to\theta\).
The regularized minimizers need not remain bounded in this limit.

Choose integer quartics \(P_0,P_1,\ldots,P_m\), as justified below.
For fixed \(\varepsilon\), minimize

\[
 g(u)+\varepsilon\|u\|^2+\eta P_0(u)
\]

on its chosen box subject to

\[
 p_i(u)-\eta+\eta^2P_i(u)\le0.
\]

Every fixed original feasible point survives for sufficiently small
positive \(\eta\). In particular, an exact regularized minimizer
survives. Compactness and uniform convergence on the fixed box imply
that every cluster point of perturbed global minimizers, as
\(\eta\downarrow0\), is a global minimizer of \(g_\varepsilon\) on
\(D\). All these limits are strictly inside the box. Consequently every
perturbed minimizer is interior for all sufficiently small \(\eta\):
otherwise a sequence of boundary minimizers would have a boundary cluster
point. Thus no box row occurs in the selected KKT systems. This is the
reason the unknown radii do not enter their coefficients.

It would be incorrect to minimize the perturbed quartic over an unboxed
set. Even \((1+\varepsilon)u^2-\eta u^4\) on \(\mathbb R\) is
unbounded below for every \(\eta>0\). The box is essential during the
analytic argument, although its boundary disappears before elimination.

## 2. Uniform genericity and dependence on the row count

For a selected subset of \(s\le r\) rows, allow all degree-at-most-four
coefficients of its constraints \(f_i\) and objective \(f_0\) to vary
independently. Over the complex numbers, generic coefficients have:

1. linearly independent gradients at every common zero of the selected
   constraints;
2. a nonsingular full bordered KKT matrix at every KKT solution.

Generic \(r+1\) constraints have no common zero. The bad coefficient
tuples in each assertion are contained in a proper algebraic hypersurface
of degree depending only on \(r\).

Here is a direct justification. For gradient dependence, introduce a
projective vector \([\lambda]\in\mathbb P^{s-1}\) and impose
\(f_i(u)=0\) and \(\sum_i\lambda_i\nabla f_i(u)=0\). For fixed
\((u,[\lambda])\), these are \(s+r\) independent linear conditions on
coefficients: use the constraint constants and the linear coefficients of
one constraint with nonzero multiplier. The incidence dimension is one
less than coefficient-space dimension, so its coefficient projection has
proper closure. The same dimension calculation, using only constants,
handles \(r+1\) simultaneous zeros.

For KKT, solve the constraint constants from feasibility and the
objective's linear coefficients from stationarity. This identifies the
universal incidence with an affine space whose dimension equals that of
coefficient space. The bordered determinant is not identically zero:
take \(f_i=u_i\) for \(i\le s\),
\(f_0=\sum_{j>s}u_j^2\), and \(u=\lambda=0\). Its determinant is
\((-1)^s2^{r-s}\). The singular subincidence therefore has smaller
dimension, and so does its projected closure. This argument covers
\(s=0\) and \(s=r\); invertibility of the unbordered Hessian is not
needed.

Cover the projective multiplier space by its \(s\) normalization charts.
These incidences involve only a number of variables and equations bounded
in terms of \(r\), of degrees bounded in terms of \(r\). Affine Bezout,
the degree bound under linear projection, and a containing hypersurface
give the asserted effective degree bound. The same degree conventions and
sources are recorded in Section 4 of the
[quadratic genericity proof](nonconvex-hessian-span-frontier.md).

Substitute

\[
 f_i=p_i-\eta+\eta^2P_i,
 \qquad f_0=g+\varepsilon\|u\|^2+\eta P_0.
\]

Over \(\mathbb Q(\varepsilon,\eta)\), this is an invertible affine
change of the selected coefficient variables. Each bad-locus polynomial
therefore remains nonzero. In each pullback select one nonzero coefficient
in its expansion in \((\varepsilon,\eta)\), and multiply these selected
polynomials over all relevant subsets. The product is nonzero and its
degree in the perturbation coefficients is at most
\(F(r)(m+1)^{r+1}\). The elementary integer-grid lemma gives one tuple
of perturbations with coefficient bits

\[
 F(r)+O(r\log(m+1)).
\]

This bound does not depend on \(\tau\). After this choice, discard the
finitely many \(\varepsilon\) where some bad polynomial becomes
identically zero in \(\eta\). For each remaining fixed
\(\varepsilon\), all sufficiently small positive \(\eta\) are good.
No uniform tail in \(\eta\) is required.

The product or its coefficient grid is not constructed by the proposed
algorithm. Enumerating those objects would not itself give a fixed
parameter algorithm. Their role is to prove that a suitably small tuple
exists.

## 3. Elimination and the nested limits

At a selected perturbed minimizer, the box is inactive. Genericity makes
the active set have size \(s\le r\), gives the usual KKT multipliers,
and makes the KKT root nonsingular. The equations in variables
\((u,\lambda)\) are

\[
 f_i(u)=0\quad(i\in J),\qquad
 \nabla f_0(u)+\sum_{i\in J}\lambda_i\nabla f_i(u)=0.
\]

There are \(r+s\le2r\) equations and variables. Their total degree in
these variables is at most four. Their degrees in the formal parameters
are bounded absolutely. Clear denominators using only the objective and
the selected at-most-\(r\) input rows. Their coefficient norm logarithms
are at most \(F(r)(\tau+\log(m+1)+1)\). Clearing denominators across
all \(m\) rows would unnecessarily destroy the claimed logarithmic
dependence on \(m\).

For each admissible \(\varepsilon\), take an inner
\(\eta\downarrow0\) subsequence with constant active support. Along an
outer \(\varepsilon\downarrow0\) subsequence, one of these finitely
many supports recurs. There is now one polynomial family, independent of
all radii, with perturbed objective values tending first to
\(v_\varepsilon\) and then to \(\theta\).

Apply the [finite-quotient lemma](explicit-span-separation.md), with its
coefficient ring extended to two formal parameters and with output equal
to the perturbed objective. Use total degree \(a=4\), and eliminate
\(r+s\) root variables. The resulting nonzero polynomial has output
degree at most \(5^{r+s}\le5^{2r}\) and coefficient bits bounded as
above. In the lemma's notation, extract the lowest nonzero coefficients
first in its auxiliary eigenvalue parameter \(\zeta\), then its
deformation parameter \(\delta\), then \(\eta\), and finally
\(\varepsilon\). Each extraction preserves the degree bound and does
not increase coefficient norm. The limit arguments use nonsingularity
only at the selected specialized roots. The root variables, including
the multipliers, need not be bounded in the outer limit.

Specialization may make an intermediate coefficient polynomial vanish
identically at one parameter value. It cannot invalidate the identity
along the selected sequence, and a nonzero polynomial has only finitely
many such exceptional specializations. This is the same ordered-limit
argument checked in the
[finite-infimum review](nonconvex-finite-infimum-review.md).

## 4. Attainment and one common algebraic point

If \(g\) attains \(\theta\), its closed optimal set has a point
\(\bar u\) of minimum norm \(c\). Every global minimizer
\(u_\varepsilon\) of the regularized problem satisfies

\[
 \theta+\varepsilon\|u_\varepsilon\|^2
 \le g(u_\varepsilon)+\varepsilon\|u_\varepsilon\|^2
 \le\theta+\varepsilon c^2.
\]

Thus all exact regularized minimizers have norm at most \(c\), and
\(g(u_\varepsilon)\to\theta\). Their outer cluster points are
minimum-norm optimizers. Select one joint nested subsequence converging
to one such point \(u^*\). Applying the same elimination family to
each coordinate output yields its coordinate annihilators. It is
essential that every coordinate uses this same limiting point.

Since there are only \(r\) coordinates, multiplying their individual
degree bounds is harmless here:

\[
 [\mathbb Q(u^*):\mathbb Q]\le(5^{2r})^r=5^{2r^2}.
\]

For completeness, the common representation retains linear dependence
on the height bound. Let \(K\) bound the coordinate-annihilator bits,
and let \(Q\) be the product of their nonzero leading coefficients.
Then every \(Q u_j^*\) is an algebraic integer and
\(\log|Q|\le rK\). Some
\(\alpha=\sum_j k^{j-1}u_j^*\), with
\(0\le k\le(r-1)d(d-1)/2\) and
\(d=[\mathbb Q(u^*):\mathbb Q]\), is primitive: each pair of distinct
field embeddings excludes at most \(r-1\) choices of \(k\).

Set \(\gamma=Q\alpha\). Cauchy's root bound controls every conjugate
of \(\gamma\) by \(2^{F(r)(K+1)}\); its monic integer minimal
polynomial consequently has coefficient bits \(F(r)(K+1)\). Recover
each \(Q u_j^*\) in the basis \(1,\gamma,\ldots,\gamma^{d-1}\)
using the trace matrix
\(T_{ab}=\operatorname{Tr}(\gamma^{a+b})\). Its integer entries and
the right-hand sides
\(\operatorname{Tr}(Q u_j^*\gamma^b)\) have bits bounded by
\(F(r)(K+1)\). The trace pairing is nonsingular in characteristic
zero, so Cramer's rule gives rational coordinate coefficients with the
same form of bound. The nonzero integer discriminant also gives a
dyadic isolating interval of that bit length for the chosen real root.
This proves the claimed total representation bound without multiplying
height exponents through an ambient-dimensional tower.

## 5. Literature and verification limits

The unknown-box argument has an explicit precedent in
[Jeronimo--Perrucci--Tsigaridas, Theorem 14](https://mate.dm.uba.ar/~perrucci/On_the_minimum_pol_funct.pdf):
for a compact minimizing set, they use a containing ball and show its
constraint is absent from the selected limiting equations. Their
Theorem 15 gives a degree bound under attainment alone. These source
statements and proofs were inspected. The two ordered regularizations
here also handle a finite unattained infimum and select a minimum-norm
optimizer when attainment holds.

[El Hilany--Tsigaridas, Theorem 1](https://arxiv.org/pdf/2407.17093)
gives unattained-infimum bounds under its complete smooth-intersection
assumptions. That source does not impose the same assumptions as this
lemma. This limited comparison does not establish novelty: more general
effective real-algebraic methods may already imply the bound needed
here.

The review checked genericity, coefficient dependence, the disappearance
of the unknown box, ordered coefficient extraction, and the common-field
conversion. A separate reviewer checked the incidence and finite-grid
arguments. A targeted exact symbolic calculation checks the escaping
regularized example described in the verification record below. None of
these checks constitutes Lean verification or an implementation of the
claimed parameterized optimization algorithm.

Verification record: an inline `python` command using SymPy checked the identity
\(v_\varepsilon^2=4\varepsilon(1+\varepsilon)\) for minimizing
\((1+\varepsilon)x^2+\varepsilon y^2\) over \(xy\ge1\),
\(x,y\ge0\), using
\(x=t\), \(y=1/t\),
\(\varepsilon=t^4/(1-t^4)\), and
\(v_\varepsilon=2t^2/(1-t^4)\), \(0<t<1\). It also checked
stationarity of the reduced one-variable objective and the bordered
determinant \((-1)^s2^{r-s}\) for all \(1\le r\le6\),
\(0\le s\le r\) (27 cases). The command passed. The example has
\(y\to\infty\) and \(v_\varepsilon\to0\), so a uniform outer
bound on minimizing points cannot be assumed. Only targeted checks were
run; project-wide verification and CI were not inspected.
