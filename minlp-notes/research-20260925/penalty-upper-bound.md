# An exponential encoding upper bound for exact norm penalties in quadratic models

Date: 2026-09-25. Status: proof independently reviewed; source-version and
constant corrections incorporated and rechecked.
This is a quantitative consequence of classical convex duality and effective
real algebraic geometry. Its role is to complement the explicit lower bound
in [the penalty construction](parametric-exploration.md), not to claim a new
general small-point theorem.

## Statement and encoding model

Consider rational data in

\[
 v=\min\{f(x,z):(x,z)\in X,\quad r(x,z)=Ax+Bz-b=0\},
 \qquad x\in\mathbb R^n,\ z\in\mathbb Z^p,              \tag{1}
\]

where \(n\ge1\), \(r\) has \(m\ge1\) coordinates, and:

1. The native set \(X\) is described by explicit finite rational boxes for
   every variable and rational inequalities \(g_i(x,z)\le0\). The total
   degree of every \(g_i\) and of \(f\) is at most two. Native affine
   equalities can be represented by two affine inequalities.
2. For each integer assignment, \(f(\cdot,z)\) and all
   \(g_i(\cdot,z)\) are convex. The integer assignment need not have a
   nonempty native slice.
3. The original feasible set in (1) is nonempty. For every integer assignment
   whose original slice is feasible, there is a point satisfying its linking
   equalities and all native affine inequalities, with every native
   nonlinear inequality strict. Here affine and nonlinear refer to the
   continuous variables after fixing the integer assignment. No quantitative
   Slater margin is supplied.

Write \(s\) for the number of native inequalities, including the boxes.
Let \(N\) denote the ordinary explicit binary input length, including all
coefficients and bounds. The model uses ordinary expanded quadratic
polynomials, not succinct arithmetic circuits or exponents in a special
number representation. Empty native integer slices are discarded.

**Theorem.** Under these assumptions, an integer \(\rho\ge1\) exists such
that, for either \(\nu=\|\cdot\|_\infty\) or
\(\nu=\|\cdot\|_1\),

\[
 \min_{(x,z)\in X}\{f(x,z)+\rho\nu(r(x,z))\}=v,         \tag{2}
\]

and every minimizing point in (2) satisfies \(r=0\). Its ordinary binary
encoding can be chosen to have length

\[
 \operatorname{bit}(\rho)
       \le (N+1)\,2^{O(n)}.                              \tag{3}
\]

The implicit constant is absolute for quadratic input. More precisely, after
integer substitution and denominator clearing, if all the polynomial systems
used below have coefficient bitsize at most \(\tau\), the bound is

\[
 \operatorname{bit}(\rho)
  \le (\tau+\log(s+m+n+2)+n+\operatorname{bit}(F))
          2^{O(n)},                                      \tag{4}
\]

where \(F\ge1\) is any integer bound for \(|f|\) on the supplied box.
Such \(F\) has polynomial, and under the explicit total-length convention
linear, bit length in \(N\). The bound does not put the number of quadratic
constraints in the exponent separately from continuous dimension.

In particular, the augmented Lagrangian dual is exact at this penalty, already
with multiplier zero. The theorem concerns a sufficient penalty; it neither
computes the smallest exact penalty nor gives a polynomial-time algorithm
that prints its ordinary binary representation.

## The effective algebraic bound used

For positive integers \(k,d,s_0,\tau\), let a polynomial family in
\(\mathbb Z[w_1,\ldots,w_k]\) contain at most \(s_0\) polynomials of
degree at most \(d\), with coefficient bitsize at most \(\tau\).
Basu and Roy's Theorems 3 and 4 give explicit radii that respectively contain
all bounded components of every **weak sign condition** and meet every
nonempty component of every weak sign condition. Here a weak sign condition
is a conjunction of polynomial equalities and weak inequalities. See the
[final author manuscript](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf),
printed page 5, and its proofs on pages 12–14. Their formulas, with the
conservative correction specified below, imply, for \(d\le3\), radii with

\[
 \log_2 R\le (\tau+\log(s_0+1)+1)\,2^{O(k)}.           \tag{5}
\]

Consequently a nonempty finite union of basic closed sets defined by these
polynomials has a point within the latter radius: apply Theorem 4 to a
nonempty branch. If the entire union is bounded, every branch and each of
its components is bounded, so Theorem 3 bounds every point in the union.
The applications below have exactly this form. No assertion about arbitrary
Boolean combinations or strict sign conditions is needed.

For reproducibility, the following integer exponents safely majorize the
two source radii. Write \(\operatorname{bit}(a)\) for the binary length of
a positive integer. Set

\[
 K=(2d+1)(2d)^{k-1},\qquad D_b=k(2d-1)+2,
\]

\[
 E_{\rm bounded}=
 \operatorname{bit}(k)+\operatorname{bit}(K+1)
 +2KD_b
  [2\tau+\operatorname{bit}(K)+k\operatorname{bit}(d+1)
       +\operatorname{bit}(s_0)+3].                      \tag{6}
\]

For the meeting radius, put

\[
\begin{aligned}
 d'&=\max\{2(d+1),6\},& D&=k(d'-2)+2,\\
 H&=d'(d'-1)^{k-1},\\
 t_0&=2\tau+k\operatorname{bit}(d+1)
                 +\operatorname{bit}(2d')+\operatorname{bit}(s_0),\\
 t_1&=D[t_0+4\operatorname{bit}(2D+1)+\operatorname{bit}(H)]
          -2\operatorname{bit}(2D+1)-\operatorname{bit}(H),\\
 t_2&=t_1+2(k-1)\operatorname{bit}(H)+(2k-1)\operatorname{bit}(k),\\
 T&=H[t_2+\operatorname{bit}(H)+2\operatorname{bit}(2D+1)+1],\\
 E_{\rm meeting}&=
 \operatorname{bit}(2DH(2H-1)+1)\\
 &\quad +(2H-1)[T+\operatorname{bit}(2H-1)
                  +\operatorname{bit}(2DH+1)+H\operatorname{bit}(H)].
\end{aligned}                                             \tag{7}
\]

Then \(2^{E_{\rm bounded}}\) and \(2^{E_{\rm meeting}}\) suffice for
the respective radii. Equation (6) bounds the source's factor
\(\sqrt{k}(K+1)\) by a power of two. Equation (7) drops the outer square
root and includes \(H\operatorname{bit}(H)\) inside the last bracket.
The extra term covers \(\operatorname{bit}(H!)\), which appears in the
proof on printed page 12 but is absent from the printed Theorem 4 formula.
We retain this conservative term rather than rely on the smaller statement.
With fixed \(d\), (6)–(7) have the growth in (5), absorbing polynomial
factors in \(k\) into the exponential.

The first draft used the superseded 2009 manuscript. Independent source
review found that the June 2010 version both changes the constants and
restricts the bounded-component statement to weak sign conditions. The
current proof uses the later formulas and applies them only to basic closed
sets and finite unions of such sets.

## Feasible slices: a bounded multiplier certificate in at most 2n variables

Fix a feasible integer assignment \(z\), and suppress it in notation. The
Slater assumption, with strictness required only for nonlinear inequalities,
gives a primal optimum \(x^*\), nonnegative inequality multipliers \(\mu\),
and linking multipliers \(\lambda\) satisfying the convex KKT conditions.
This is the same slice regularity used in Lefebvre and Schmidt's
[Assumption 5 and Theorem 14](https://optimization-online.org/wp-content/uploads/2024/07/exact-penalty-for-minlp-1.pdf).

The number of multiplier variables can be reduced before applying (5).
Let \(e=\operatorname{rank}(A)\), and choose \(e\) independent rows
\(J\) of \(A\). Project stationarity onto the quotient by the row space
of \(A\). In this vector space of dimension \(n-e\), the projected vector
\(-\nabla f(x^*)\) lies in the cone generated by the active inequality
gradients. Conic Carathéodory gives a representation using at most \(n-e\)
of them. Let \(I\) be their indices. The remaining difference lies in the
row space of \(A\) and can be represented using the rows in \(J\).

There is therefore a KKT certificate with \(|I|+|J|\le n\), satisfying

\[
\begin{aligned}
 &g_i(x)\le0\quad(1\le i\le s),\qquad r(x)=0,\\
 &\mu_i\ge0,\quad g_i(x)=0\quad(i\in I),\\
 &\nabla f(x)+\sum_{i\in I}\mu_i\nabla g_i(x)
                      +\sum_{j\in J}\lambda_j A_j^T=0.
\end{aligned}                                             \tag{8}
\]

This is a nonempty rational semialgebraic set in at most \(2n\) variables.
Every polynomial has degree at most two. Since every selected inequality
was active at the original KKT point, requiring its value to be zero
preserves nonemptiness and implies complementarity at every new certificate.
There are at most \(s+m+3n\) polynomials before padding.
Pad with zero coordinates if needed to use exactly \(2n\) variables, and
use the count \(s_0=s+m+4n+1\) as a uniform upper bound.

After clearing positive denominators, Theorem 4 supplies a point satisfying
(8) with every coordinate bounded in absolute value by

\[
 R_M=2^{E_{\rm meeting}(2n,2,s_0,\tau)}.                 \tag{9}
\]

The active sets in this argument can depend on the slice. Only their sizes
and the coefficient bound matter; they need not be found to obtain the
uniform numerical bound. Setting omitted linking multipliers to zero gives
\(\|\lambda_z\|_1\le nR_M\).

For every point of the native slice, convexity and stationarity show that
the Lagrangian in (8) is globally minimized at its KKT point. Complementarity
then gives

\[
 f(x,z)+\lambda_z^T r(x,z)\ge v_z
       \quad\text{for all }x\in X_z,                    \tag{10}
\]

where \(v_z\) is the optimum of the original feasible slice. Indeed, the
native terms \(\sum\mu_i g_i\) are nonpositive on \(X_z\), so deleting
them only increases the Lagrangian. Consequently

\[
 f(x,z)+\rho\|r(x,z)\|_\infty
 \ge v_z+(\rho-nR_M)\|r(x,z)\|_\infty.                 \tag{11}
\]

This argument bounds one suitable multiplier certificate. It does not claim
that every optimal multiplier is bounded; redundant constraints may produce
unbounded multiplier sets.

## Infeasible slices: a bounded reciprocal graph

Fix a nonempty native slice \(X_z\) with no point satisfying \(r=0\).
Compactness and continuity imply
\(\delta_z=\min_{x\in X_z}\|r(x,z)\|_\infty>0\).
Consider

\[
\begin{split}
 T_z=\{(x,t):\;&x\in X_z,\ t\ge0,\\
             &-1\le t r_j(x,z)\le1\quad(1\le j\le m),\\
             &\text{at least one }t r_j(x,z)\text{ equals }1
                                      \text{ or }-1\}.
\end{split}                                               \tag{12}
\]

It is exactly the graph of \(t=1/\|r(x,z)\|_\infty\). In particular,
it is nonempty, compact, and described without quantifiers using at most
\(s+2m+1\) polynomials of degree at most two. The disjunction in its final
line introduces no new polynomial or variable. Apply Theorem 3 to the
basic closed branches in (12):

\[
 \delta_z^{-1}\le
 R_D=2^{E_{\rm bounded}(n+1,2,s+2m+1,\tau)}.             \tag{13}
\]

This proof uses no Slater assumption on infeasible slices, no distance
minimizer KKT system, and no assertion that a positive minimum is rational.
It bounds every point of the reciprocal graph rather than only one sample.

## Combining the bounds and accounting for integer variables

Choose an integer \(F\ge1\) bounding \(|f|\) on the supplied full box.
For example, an integer bound \(H\ge1\) on all coordinate magnitudes and
the sum \(C\) of the absolute values of the objective coefficients give
\(F=1+\lceil C H^2\rceil\). Let

\[
 E=\max\{E_{\rm meeting}(2n,2,s+m+4n+1,\tau),
          E_{\rm bounded}(n+1,2,s+2m+1,\tau)\},
 \qquad \rho=(n+2F+1)2^E.                               \tag{14}
\]

For feasible slices, (11) is strictly above \(v_z\ge v\) whenever the
residual is nonzero. For infeasible slices, (13) gives

\[
 f+\rho\|r\|_\infty\ge -F+\rho/R_D>F\ge v.
\]

An original optimum attains \(v\) in the penalized problem. This proves
value and solution exactness for the infinity norm. The 1-norm is no smaller
and vanishes at exactly the same points, proving that case as well.

It remains to justify that \(\tau\) is uniform over all integer assignments.
All integer coordinates have magnitude at most \(2^{O(N)}\) from their
explicit boxes. There are at most \(O(N)\) explicitly encoded monomials.
The product of all input denominators has bit length \(O(N)\); multiplying
by it clears each original polynomial. Substituting bounded integer
coordinates into a degree-two monomial increases its coefficient bit length
by only \(O(N)\). Summing the input monomials adds \(O(\log N)\) bits.
Differentiation adds at most one bit, and introducing multiplier or reciprocal
variables does not increase coefficient heights. A common positive
denominator therefore clears every polynomial in (8) and (12) with
\(\tau=O(N)\), under any standard explicit encoding differing by constant
factors. This clearing step changes neither the linking residual used in
the penalty nor the multiplier coordinates in (8).

No factor equal to the number of integer assignments enters the bound.
The same (14) works on all of them. Substituting the fixed degrees and
dimensions into (6)–(7), and using \(\operatorname{bit}(F)=O(N)\), proves
(3)–(4). The integer \(E\) itself has polynomial encoding length, so this
proof gives a succinct exponent specification. The ordinary binary
representation of \(\rho\) still requires the number of bits in (3).

## What this establishes, and what it does not

The chain construction has \(n+1\) continuous variables and needs
\(2^n\) penalty bits despite bounded coefficients. The upper bound here is
exponential in continuous dimension with a polynomial input-size prefactor.
Thus the two bounds match at the scale of exponential dependence on that
dimension. They do not give identical bases or a tight bound in the sparse
input length, which contains variable-index encoding costs.

The upper bound is a classical algebraic-geometric corollary combined with
the feasible/infeasible-slice proof of exactness. Its strongest supporting
observations are the sparse degree-two KKT certificate in at most \(2n\)
variables and the degree-two reciprocal graph. Neither a new small-point
bound nor a general new exact-penalty theorem is claimed.

The next result gives a sharper boundary: a fixed number of nonlinear
quadratic inequalities permits polynomial-bit exact penalties, even with
arbitrarily many continuous variables and affine inequalities.

## Fixed-number-of-quadratics source caution

Grigoriev and Pasechnik's
[quadratic-map sampling paper](https://arxiv.org/pdf/cs/0403008), Theorem 1.2,
provides polynomial-size algebraic sampling for a fixed number of quadratic
map components. Its Theorem 1.5 states an optimization extension but defers
the proof to a continuation. The
[ITCS 2026 paper on pure-state consistency](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.83/LIPIcs.ITCS.2026.83.pdf),
printed page 6, explicitly reports that this proof remained unavailable and
proves a bounded approximation result instead. The fixed-quadratic-count
conclusion below does not use Theorem 1.5. It uses convexity to reduce a
regularized KKT system to few variables, followed by ordinary effective
quantifier elimination.

Generic algebraic-degree formulas for QCQP also require a separate
degeneracy and coefficient-height argument. The following proof supplies
those steps by perturbation and a quantified limit formula, rather than
assuming generic data.

The later paper's full [arXiv version](https://arxiv.org/html/2411.03096v2)
is a closer comparator than its approximation theorem alone. Sections
6.3–7.2, equations (98) and (101), express feasibility and optimization
through formulas in few real variables, and Theorem 7.2 bounds algebraic
representations and integer coefficient sizes. Section 8.5, Corollary 8.14
and equation (115), explicitly apply that framework to QCQP with a fixed
total number of constraints, without convexity assumptions. After the
convex affine-face reduction below and its added bounding ball, squared
slack variables turn the remaining inequalities into a bounded
quadratic-map zero set. Thus the
full source provides direct precedent for polynomial-height optimal
values when the nonlinear count is fixed. The present proof gives a
direct convex KKT derivation with the explicit \(N^{O(k+1)}\) dependence
and its exact-penalty consequence. It does not establish priority for the
value lemma, and no priority claim rests on the unavailable older proof.
Likewise, [Nie and Ranestad's algebraic-degree result](https://arxiv.org/abs/0802.1233)
treats generic polynomial optimization, including QCQP. Its abstract was
checked for scope; it was not used as the coefficient-height theorem here.

## Polynomial-bit penalties with a fixed number of nonlinear quadratics

Write \(k\) for an upper bound on the number of native inequalities that
are nonlinear in \(x\) after fixing any integer assignment. All other
assumptions and the explicit encoding convention remain as above.

**Refinement.** There is an integer penalty giving value and solution
exactness at multiplier zero with

\[
 \operatorname{bit}(\rho)\le N^{O(k+1)}.                 \tag{15}
\]

The constants in the exponent are absolute. Thus a fixed number of
nonlinear convex quadratic inequalities gives a polynomial encoding bound,
independent of the number of affine rows. The result does not require a
supplied quantitative Slater margin. It allows degeneracy, dependent affine
rows, singular quadratic Hessians, and infeasible integer slices without
Slater. This is an existence bound; the proof does not provide an algorithm
that finds the relevant active affine face in polynomial time.

The main ingredient is a bound on nonzero optimal values of convex QCQPs
with few nonlinear inequalities. We prove it first.

### A value bound that allows arbitrary affine constraints

**Lemma.** Consider minimization of a rational convex quadratic objective
over a nonempty bounded set described by a rational polyhedron with explicit
finite coordinate bounds and at most \(k\) convex quadratic inequalities.
Let \(L\ge2\) be its explicit input length, and let \(\theta\) be its
optimum. If \(\theta\ne0\), then

\[
 |\theta|\ge 2^{-L^{O(k+1)}}.                           \tag{16}
\]

No constraint qualification is assumed. In fact, \(\theta\) is a root
of a nonzero integer polynomial of degree \(L^{O(k+1)}\) and coefficient
bitsize \(L^{O(k+1)}\).

**Proof: removing inactive affine rows.** Let \(x^*\) be an optimum.
Let \(H\) be the affine space obtained by making all affine inequalities
active at \(x^*\) into equalities, together with any original equalities.
There is a neighborhood of \(x^*\) in \(H\) in which every omitted
affine inequality holds, because it has positive slack at \(x^*\).
Consequently \(x^*\) is a local minimizer over \(H\) and the nonlinear
quadratic inequalities alone. This feasible set is convex, so it is also a
global minimizer there. More explicitly, any point of lower objective value
would yield, along its segment to \(x^*\), points of lower value within
that neighborhood, a contradiction.

Choose a maximal independent subsystem of the rational equations defining
\(H\). Gaussian elimination gives a rational parametrization

\[
 x=x_0+Vu,\qquad u\in\mathbb R^d,
\]

whose coefficients have polynomial bit length in \(L\). The free
coordinates \(u\) can be chosen as a subset of the original coordinates
of \(x\). If \(d=0\), evaluating the objective at the rational point
proves the lemma directly. Otherwise the original supplied coordinate bound
\(|x_j|\le B\), with integer \(B\ge1\) of polynomial bit length,
implies \(\|u^*\|^2\le dB^2\). Add the inequality

\[
 \|u\|^2\le dB^2+1.
\]

It is strict at \(u^*\), retains the same optimum, and makes the new set
compact. After substitution, the problem has a convex quadratic objective
\(q_0\), at most \(h=k+1\) convex quadratic inequalities \(q_i\le0\),
no affine constraints, and rational coefficient bitsize polynomial in
\(L\). In this count it is harmless if some of these \(q_i\) become
affine or constant. The added ball is one of the \(q_i\).

**Proof: a regularization with few dual variables.** For \(0<\varepsilon<1\)
consider

\[
 \theta(\varepsilon)=
 \min\left\{q_0(u)+\varepsilon\|u\|^2:
                       q_i(u)\le\varepsilon\ (1\le i\le h)\right\}.
                                                               \tag{17}
\]

The original point \(u^*\) strictly satisfies all these inequalities.
The relaxed ball bounds every feasible point uniformly for
\(0<\varepsilon<1\), and the objective is strictly convex. Thus an
optimum and KKT multipliers \(\lambda_i\ge0\) exist. Write

\[
 q_i(u)=\tfrac12u^TQ_i u+a_i^Tu+c_i,
 \qquad Q_i\succeq0\quad(0\le i\le h).
\]

Stationarity is

\[
 M(\varepsilon,\lambda)u=-a_0-\sum_i\lambda_i a_i,
 \qquad
 M=Q_0+2\varepsilon I+\sum_i\lambda_iQ_i\succ0.
                                                               \tag{18}
\]

Let \(\Delta=\det M>0\) and
\(p=-\operatorname{adj}(M)(a_0+\sum_i\lambda_i a_i)\).
Both \(\Delta\) and the coordinates of \(p\) are polynomials of
degree at most \(d\) in \((\varepsilon,\lambda)\), and \(u=p/\Delta\).
For \(1\le i\le h\), set

\[
 G_i=\tfrac12p^TQ_i p+\Delta a_i^Tp+(c_i-\varepsilon)\Delta^2,
\]

and set

\[
 G_0=\tfrac12p^TQ_0p+\Delta a_0^Tp+(c_0-w)\Delta^2
                    +\varepsilon p^Tp.
\]

The following quantifier-free polynomial system \(\mathcal K\) exactly
describes certificates that \(w=\theta(\varepsilon)\):

\[
 \Delta>0,\quad \lambda_i\ge0,\quad G_i\le0,\quad
 \lambda_iG_i=0\ (1\le i\le h),\quad G_0=0.             \tag{19}
\]

Necessity follows from KKT and (18). Conversely, (19) reconstructs a primal
point with feasibility, stationarity, and complementarity for a convex
problem, so it certifies optimality. All polynomials in (19) have degree at
most \(2d+2\). Their integer coefficient bitsizes after denominator
clearing are polynomial in \(L\): determinant expansion takes products
of at most \(d\) affine entries and sums at most \(d!\) such products.
This gives polynomial coefficient height even though the number of
monomials in these few-variable polynomials need not be uniformly
polynomial when \(k\) varies.

Uniform boundedness and compactness give
\(\theta(\varepsilon)\to\theta\) as \(\varepsilon\downarrow0\).
For the upper limit, substitute \(u^*\) into (17). For the lower limit,
take a convergent subsequence of minimizers along a sequence attaining the
lower limit; its limit satisfies every unrelaxed inequality and therefore
has objective at least \(\theta\).

**Proof: a quantified limit and its coefficient height.** The singleton
\(\{\theta\}\) is defined by the following formula with one free
variable \(v\):

\[
 \forall\eta\ \Bigl[\eta\le0\ \lor\
  \exists\varepsilon,w,\lambda\,
  \bigl(0<\varepsilon<1,\ \varepsilon<\eta,\
       -\eta<w-v<\eta,\ \mathcal K(\varepsilon,w,\lambda)\bigr)\Bigr].
                                                               \tag{20}
\]

There are two quantifier blocks, of sizes \(1\) and \(h+2\), and one
free scalar. The degree bound is \(O(d+1)\), and the coefficient bitsize
is polynomial in \(L\). Effective real quantifier elimination gives an
equivalent quantifier-free formula whose polynomial degrees and coefficient
bitsizes are \(L^{O(k+1)}\). The precise source used is Basu, Pollack, and
Roy's bound, stated as Theorem 2.27 on printed page 16 of
[Basu's author survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf).
For block sizes \(b_1,b_2\), its degree exponent is
\(O(b_1)O(b_2)\), and its output integer bitsize is the input bitsize
times that degree bound, with an additional constant factor in the exponent
for the one free variable. Here this exponent is \(O(k+1)\).

After removing identically zero polynomials from the formula, at least one
remaining polynomial must vanish at \(\theta\). Otherwise every sign
in the formula would be locally constant there, contradicting that the
formula defines a singleton. This proves the asserted degree and height
bound. If \(\theta\ne0\), remove any power of the indeterminate dividing
that polynomial and apply the ordinary Cauchy bound to the reciprocal
polynomial. An integer polynomial with coefficient bitsize \(T\) has no
nonzero real root of magnitude below \(1/(1+2^T)\). This proves (16).
\(\square\)

### Applying the value bound to all integer slices

For a nonempty infeasible native slice, minimize \(t\) subject to its
native constraints and

\[
 -t\le r_j(x,z)\le t\quad(1\le j\le m),\qquad 0\le t\le R,
\]

where \(R\) is any rational box-derived upper bound on every residual
magnitude. This problem is nonempty and compact, has at most \(k\)
nonlinear inequalities, and has positive optimum \(\delta_z\). The
lemma therefore gives uniformly

\[
 \delta_z\ge2^{-N^{O(k+1)}}.                            \tag{21}
\]

For a feasible original slice with at least one nonlinear inequality, let
\(P_z\) denote its native affine constraints together with \(r=0\),
and define

\[
 \sigma_z=\max\{t:x\in P_z,\ q_i(x,z)+t\le0
                \text{ for every nonlinear native row }i,\ 0\le t\le1\}.
                                                               \tag{22}
\]

Refined Slater gives \(\sigma_z>0\). The negative of (22) is a compact
convex QCQP with at most \(k\) nonlinear inequalities and objective
\(-t\). Applying the lemma gives

\[
 \sigma_z\ge2^{-N^{O(k+1)}}.                            \tag{23}
\]

Let \(\bar x\) attain (22), and take any convex KKT certificate for the
original optimum \(x^*\). Write \(\mu\) for its nonlinear native
multipliers. The Lagrangian is globally minimized at \(x^*\).
Evaluating it at \(\bar x\), where linking residuals vanish and native
affine terms are nonpositive, gives

\[
 v_z\le f(\bar x,z)-\sigma_z\sum_i\mu_i,
 \qquad \sum_i\mu_i\le 2F/\sigma_z.                    \tag{24}
\]

The remaining stationarity vector
\(b_*=-\nabla f(x^*,z)-\sum_i\mu_i\nabla q_i(x^*,z)\)
has magnitude at most \(2^{\operatorname{poly}(N)}(1+2F/\sigma_z)\).
It lies in the cone generated by the active native affine normals and the
signed linking normals \(A_j^T,-A_j^T\). Conic Carathéodory permits a
representation using linearly independent generators, at most \(n\) of
them. Choose a nonsingular square row minor of their column matrix. All its
entries are rational input coefficients. Cramer's rule bounds the inverse
matrix entries by \(2^{\operatorname{poly}(N)}\), uniformly over the
selected columns and rows. The coefficients in this conic representation
are therefore at most \(2^{N^{O(k+1)}}\). Combining coefficients of the
signed linking normals gives another valid KKT certificate with

\[
 \|\lambda_z\|_1\le2^{N^{O(k+1)}}.                    \tag{25}
\]

This reconstruction keeps the already bounded nonlinear multipliers and
uses only active affine normals, so complementarity is preserved. If there
are no nonlinear rows, omit \(\mu\) and use the same rational cone
argument directly; no Slater slack is needed.

Substitution of bounded integer coordinates changes the encoded size of
these auxiliary problems by only a polynomial factor, uniformly over all
assignments. Equations (21) and (25), combined with the strict inequalities
in the proof of (14), give an integer penalty of bit length
\(N^{O(k+1)}\). The same penalty works for the infinity norm and the
1-norm. This proves the refinement.

### Significance and limits of the refinement

The chain lower bound uses a growing number of nonlinear quadratic
inequalities. The refinement shows that this feature is necessary for
superpolynomial penalty encoding within the stated compact convex model:
with a fixed number of such inequalities, arbitrarily many affine rows and
continuous variables do not recreate that obstruction.

The reusable step is the passage from a high-dimensional convex quadratic
value problem to a first-order formula with \(O(k)\) real variables.
Convexity justifies deleting inactive affine rows, and positive definite
regularization permits rational elimination of all primal coordinates.
The limiting formula handles degeneracy without an algebraic-degree
genericity assumption. The final claim concerns encoding length, not a
practical penalty rule or an efficient exact MINLP algorithm. Computing
useful bounds, exploiting the active affine structure, and obtaining
numerically reasonable penalties remain separate tasks.

This is a derived exact-penalty consequence of classical convex duality,
rational linear algebra, and effective quantifier elimination. The proof
does not establish that the few-quadratic value lemma or the resulting
penalty boundary is absent from the prior literature. Publication priority
for this particular consequence has not been established. The proved
contribution to this research batch is the explicit encoding boundary
and its proof under the stated assumptions.

## Verification record

The [independent fixed-count review](penalty-fixed-quadratic-count-review.md)
accepted the refinement, including its quantified limit, coefficient
height, Slater margin and multiplier reconstruction. A separate root
check reread the entire refinement and the coefficient-height clause of
Basu's Theorem 2.27. An exact symbolic example in the review checks the
determinant identities; it does not replace the all-dimensional proof.
The [publication audit](publication-penalty-fixed-k-audit.md) independently
rechecked the refinement, tested a degenerate example with divergent
perturbed multipliers, and tightened the Kamminga–Rudolph comparison to
include its explicit fixed-constraint QCQP result. No change to the
accepted theorem or proof was needed.

Independent reviews accepted the KKT sparsification, reciprocal graph, and
uniform coefficient-height arguments. A separate source review identified
the superseded manuscript and the final version's factorial discrepancy.
After these corrections, equations (6)–(7) were independently checked here
against rendered pages 5 and 12 of the final Basu–Roy PDF, as well as extracted
text. Replacing complementarity products by selected active equations was
also checked directly: it preserves the original witness and keeps every
resulting point a valid convex KKT certificate.

The targeted source checks used `pdftotext -layout` and `pdftoppm` on the cited
Basu–Roy PDFs, followed by visual inspection of final pages 5 and 12. No
generic QCQP solver, Lean build, project-wide test, or CI inspection was used.
The formulas are conservative theoretical bounds rather than numerically
tested penalty selection rules. Independent review supports the proof; it
does not establish that every argument in the cited algebraic-geometry paper
has been independently reproved.
