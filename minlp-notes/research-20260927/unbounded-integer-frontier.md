# Removing integer bounds at fixed continuous Hessian span

Date: 2026-09-27. Status: proof and
[independent adversarial review](unbounded-integer-review.md) completed, with
a separate root review. The algebraic projection construction below is the
new step. Its combination with established integer-witness bounds and the
other results of this batch removes all input bounds from the feasibility
result for fixed parameters. Priority is not established.

## Result and scope

Let

\[
 C=\{(z,x)\in\mathbb R^k\times\mathbb R^n:
       A(z,x)\le b,\ E(z,x)=e,\ q_i(z,x)\le0\ (i=1,\ldots,m)\}
\]

have rational input data of total explicit binary length \(N\ge2\).
Each \(q_i\) has degree at most two and a positive-semidefinite full Hessian
in \((z,x)\). Put

\[
 h=\dim_{\mathbb Q}\operatorname{span}
       \{\nabla^2_{xx}q_i:i=1,\ldots,m\},\qquad
 Y=\{z\in\mathbb R^k:\exists x\ (z,x)\in C\}.
\]

No variable bounds, Slater condition, or rational continuous feasible point
are assumed. The set \(C\) is closed and convex; its projection \(Y\) is
convex and semialgebraic. The proof does not require a separate closedness
assumption for \(Y\).

**Small integer witness theorem.** There is an effective absolute
constant \(c\) such that, if \(Y\cap\mathbb Z^k\ne\varnothing\), then it
contains \(z^*\) satisfying

\[
 \log_2(2+\|z^*\|_\infty)
      \le N^{c(h+1)(k+1)^4}.                         \tag{1}
\]

Consequently, using the independently reviewed
[continuous-radius theorem](unbounded-hessian-span.md) and the
[bounded integer-projection theorem](mixed-integer-span-frontier.md), exact
feasibility of \(C\cap(\mathbb Z^k\times\mathbb R^n)\) is decidable in
polynomial Turing time for every fixed \(k,h\). The algorithm can produce a
feasible integer assignment. It need not produce an exactly feasible rational
continuous vector, since such a vector need not exist.

This is a polynomial-time statement for fixed parameters, not an FPT running
time claim. It also gives exact optimization and unboundedness classification
for a rational convex quadratic objective depending only on the integer
variables, as proved below. It does not establish an algorithm for arbitrary unbounded
objectives involving the continuous variables, or an MILP preserving
*every* unbounded feasible integer assignment.

It also decides any supplied rational threshold for a jointly convex
quadratic objective: append its threshold inequality, which increases the
continuous Hessian span by at most one. Recovering such an unrestricted
optimum and classifying its unboundedness are separate questions.

## Why a large formula can give a small witness

[Khachiyan and Porkolab (2000)](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
Theorem 1.1, bounds an optimal integer point in a convex semialgebraic set
described by a first-order Boolean formula. If its polynomial degrees are
at most \(D\), individual integer coefficients have binary length at most
\(L\), and quantifier blocks have sizes \(n_1,\ldots,n_\omega\), the
coordinate bit bound is
\(L D^{O(k^4)\prod_i O(n_i)}\). Crucially, this bound does not depend on
the number of atomic predicates. Their sentence preceding
the theorem reduces feasibility to optimization by appending an integer
coordinate fixed to zero. Thus feasibility uses \(k+1\) in place of \(k\).
The theorem permits arbitrary Boolean formulas and does not require the set
to be closed or full-dimensional.

We will describe \(Y\) by a possibly exponentially large disjunction of
small algebraic charts, inside three quantifier blocks of sizes at most
\(1,1,\max\{1,h\}\). Each atomic polynomial has degree and coefficient bit
length \(N^{O(1)}\). This description is used only to prove (1). The
algorithm does not generate it or invoke the integer-optimization algorithm
on it. A quantifier-free consequence is recorded because it explains the
algebraic structure, but is unnecessary for the integer-witness argument.

## Projection lemma

**Lemma.** The set \(Y\) admits a quantifier-free Boolean description whose
atomic integer polynomials have degree at most

\[
 D=N^{O(h+1)}
\]

and coefficient bit length at most

\[
 L=N^{O((k+1)(h+1))}.                              \tag{2}
\]

The number of atoms is not claimed polynomial. Only convexity of the
continuous slices is needed for this lemma; joint convexity is used later to
apply the convex integer-witness theorem to \(Y\).

### 1. Active affine restrictions at a minimum-norm feasible point

Fix \(z\in Y\). The nonempty closed fiber
\(C_z=\{x:(z,x)\in C\}\) has a unique minimum-norm point \(x^*\).
Let \(I\) denote its active quadratic rows and \(K\) its active affine
inequalities. Retain all affine equalities. Replace rows in \(K\) by
equalities, and delete inactive affine inequalities and inactive quadratic
rows. The resulting enlarged problem still has \(x^*\) as its unique
minimum-norm point. Indeed, if a retained-feasible point had smaller norm,
a sufficiently short segment from \(x^*\) toward that point would satisfy
the deleted strict inequalities and have smaller squared norm. Convexity
preserves the retained quadratic inequalities along the segment.

Choose \(J_0\subseteq I\) indexing a basis of the active \(xx\) Hessians.
Its cardinality is at most \(h\). There are rational coefficients
\(c_{ij}\), with polynomial bit length, such that

\[
 \nabla^2_{xx}q_i=\sum_{j\in J_0}c_{ij}\nabla^2_{xx}q_j
                  \qquad(i\in I).
\]

The differences

\[
 r_i(z,x)=q_i(z,x)-\sum_{j\in J_0}c_{ij}q_j(z,x)
\]

are affine in \(x\), with coefficients affine in \(z\) and constants
quadratic in \(z\). Since every row in \(I\) is zero at \(x^*\), impose
\(r_i(z,x)=0\) for all \(i\in I\). Together with the retained affine
equalities these form

\[
 B(z)x=d(z).                                      \tag{3}
\]

Every entry of \(B\) is affine in \(z\), and every entry of \(d\) has
degree at most two. Their rational coefficients have polynomial bit length.
The point \(x^*\) satisfies (3). On its affine solution space the **whole**
active quadratic polynomials, including their affine parts and constants,
satisfy \(q_i=\sum_{j\in J_0}c_{ij}q_j\).

### 2. Rational rank charts with parameter-dependent coefficients

For each possible choice of \(I,K,J_0\), consider all pivot minors for
(3). Choose a nonsingular \(r\)-by-\(r\) submatrix of \(B(z)\), with
determinant \(\delta(z)\), using specified rows and columns. Solve its
pivot equations in terms of the remaining \(d=n-r\) coordinates \(u\):

\[
 x=a(z)+V(z)u.                                    \tag{4}
\]

The free-coordinate rows of \(V\) form an identity matrix. The entries of
\(a,V\) are rational functions with common denominator \(\delta\).
Require \(\delta\ne0\), \(B a=d\), and \(B V=0\). Clearing
denominators in these equalities gives polynomial chart conditions. They
ensure that (4) parameterizes exactly the complete solution set of (3).
They also ensure rank \(r\): the nonzero pivot gives the lower bound, while
the \(n-r\) independent columns of \(V\) lie in its kernel. The case
\(r=0\) uses \(a=0,V=I,\delta=1\) and the same consistency conditions.

The degrees of these rational numerators and chart polynomials are
\(N^{O(1)}\), and their coefficient bit lengths are \(N^{O(1)}\).
This follows directly from determinant expansion: matrix dimensions and
entry degrees are bounded by \(N\), and the number of terms affects the
logarithm of coefficient magnitudes only polynomially. These bounds do not
depend on how many rank charts are considered.

If \(d=0\), the fiber candidate is simply \(x=a(z)\); substitute it in
all original rows and clear denominators by positive even powers. This is
already a quantifier-free chart of the required degree and height. Assume
below that \(d>0\).

### 3. A rational family with at most \(h\) multiplier variables

For fixed \(z\) satisfying the chart conditions, let
\(p_i(u)=q_i(z,a+Vu)\) for \(i\in I\). Write

\[
 p_i(u)=\tfrac12u^T H_i u+g_i^T u+\beta_i.
\]

All \(H_i\) are PSD, and \(p_i=\sum_{j\in J_0}c_{ij}p_j\).
For \(\varepsilon>0\), minimize

\[
 \phi(u)=\|a+Vu\|^2
       \quad\text{subject to}\quad p_i(u)\le\varepsilon\quad(i\in I).
                                                               \tag{5}
\]

The original \(x^*\) is strictly feasible. The objective is coercive and
strictly convex because \(V\) has full column rank. Hence (5) has a unique
minimizer and nonnegative KKT multipliers. Its squared norm is at most
\(\|x^*\|^2\). As \(\varepsilon\downarrow0\), its points converge to
\(x^*\): they are bounded, every accumulation point satisfies (3) and all
retained unrelaxed rows, and \(x^*\) uniquely minimizes norm there.

The stationarity contribution of the native multipliers depends only on
\(\sum_{i\in I}\lambda_i c_i\), where
\(c_i=(c_{ij})_{j\in J_0}\in\mathbb R^{|J_0|}\). Conic Caratheodory
reduces this vector to a nonnegative combination of at most \(|J_0|\le h\)
generators drawn from the currently positive multipliers. Let \(J\subseteq I\)
be that support. It preserves stationarity. Complementarity is also
preserved, although it will not be needed in the formula below.

For any fixed support \(J\), \(|J|\le h\), and any \(\lambda\ge0\),
the stationary point of \(\phi+\sum_{j\in J}\lambda_jp_j\) is unique:

\[
 M(z,\lambda)=2V^TV+\sum_{j\in J}\lambda_jH_j\succ0,
\]
\[
 u(z,\lambda)=-M(z,\lambda)^{-1}
          \left(2V^Ta+\sum_{j\in J}\lambda_jg_j\right),
\qquad X_J(z,\lambda)=a+Vu(z,\lambda).             \tag{6}
\]

By adjugates, \(X_J\) is a rational function of \(z,\lambda\). Its
numerators and a common denominator have degree \(N^{O(1)}\) and coefficient
bit length \(N^{O(1)}\), uniformly over all charts and supports. One can
first clear the powers of \(\delta\) in \(M\), take its determinant and
adjugate, and then clear the remaining \(\delta\) factors. The common
denominator is nonzero on the chart whenever \(\lambda\ge0\), by the
positive definiteness just proved. No determinant sign is assumed when
clearing inequalities; an even power of that denominator is used.

There are finitely many supports. Along a sequence
\(\varepsilon\downarrow0\), one support \(J\) occurs infinitely often.
For that support the corresponding \(X_J(z,\lambda)\) converge to \(x^*\).
The multipliers themselves need not be bounded.

### 4. An exact formula using bounded approximation

For each chart and support, form the following first-order formula, with
free variable \(z\): the chart conditions hold, and

\[
 \exists R>0\quad\forall t>0\quad\exists\lambda\ge0:
 \quad \|X_J(z,\lambda)\|^2\le R,
\]
\[
 q_i(z,X_J(z,\lambda))\le t\quad(i=1,\ldots,m),
\]
\[
 A(z,X_J(z,\lambda))-b\le t,\qquad
 -t\le E(z,X_J(z,\lambda))-e\le t.                \tag{7}
\]

Vector inequalities are interpreted componentwise. Include an explicit
nonzero guard for the common rational-point denominator; this is already
implied by the rank conditions and nonnegative multipliers. After clearing
denominators by positive even powers, these are polynomial predicates of
degree and coefficient bit length \(N^{O(1)}\). The universal quantifier
is written formally as an implication from \(t>0\). If \(J\) is empty,
the last quantifier block can be omitted or padded by one unused variable.

For the chart and fixed support obtained from an original feasible fiber,
(7) holds: take \(R>\|x^*\|^2\), and choose a sufficiently late element
of the convergent subsequence for any given \(t>0\). Every original row
is satisfied to error at most \(t\), including rows deleted when defining
the auxiliary minimum-norm problem.

Conversely, if (7) holds for any chart or support, take \(t=1/j\) and its
associated points \(X_J\). Their norms are bounded by \(\sqrt R\).
A convergent subsequence exists. Continuity of every original row gives a
point of \(C_z\) in its limit. Thus (7) cannot certify an infeasible fiber,
even if its selected active set did not arise from an actual optimizer.

The disjunction over all charts and supports therefore describes exactly
\(Y\). This is not merely a description of its closure: the bound \(R\)
is chosen separately at a **fixed** free value \(z\), and only continuous
fiber coordinates are taken to a limit.

### 5. Elimination and the atom bounds

Apply coefficient-sensitive block quantifier elimination separately to each
formula (7). It has three blocks of sizes \(1,1,|J|\le h\), at most
\(N^{O(1)}\) predicates, degree \(N^{O(1)}\), coefficient bit length
\(N^{O(1)}\), and \(k\) free variables. Khachiyan--Porkolab Proposition
2.1 states the needed bound explicitly: output degree is bounded by the
input degree raised to the product of \(O(n_i)\) over blocks; output
coefficient bit length is at most the input bit length times the input
degree raised to \((k+1)\prod_i O(n_i)\). In particular these bounds are
independent of the number of predicates. The underlying result is due to
Basu and coauthors; the equivalent coefficient-sensitive block bound is used
in the other Hessian-span notes.

This gives (2). Taking the disjunction of the resulting quantifier-free
chart formulas does not change the maximum degree or coefficient length of
any atom. It can increase formula length dramatically, which is permitted
here. This proves the projection lemma.

## Direct integer-witness proof and algorithm

Pad every chart's multiplier tuple with unused variables to length
\(\max\{1,h\}\). Put the finite disjunction of chart conditions and the
cleared predicates in (7) inside one common quantifier prefix

\[
 \exists R>0\quad\forall t>0\quad
              \exists\lambda\in\mathbb R^{\max\{1,h\}}.
\]

Nonnegativity is required for the used multipliers inside each disjunct.
The zero-dimensional charts use their directly substituted point \(a(z)\),
check the original rows exactly, and impose \(\|a(z)\|^2\le R\); they do
not use the multiplier tuple. The result still defines exactly \(Y\).
The forward implication already gives one chart and support valid for every
\(t\). For the reverse implication, the chart and support may vary with
\(t\), but every witness is an actual continuous vector of squared norm
at most the same \(R\), satisfying every original row to error at most
\(t\). Taking \(t\downarrow0\) and a convergent subsequence again gives
an exactly feasible continuous vector. The formal unrestricted universal
quantifier uses the implication from \(t>0\).

Joint convexity makes \(Y\) convex. Apply Khachiyan--Porkolab Theorem 1.1
directly to this first-order formula, after adjoining an integer coordinate
equal to zero. Its atom degrees and coefficient lengths are \(N^{O(1)}\),
and the product of its block-size factors is \(O(h+1)\). Thus the integer
witness coordinate bit bound is

\[
 N^{O(1)}\bigl(N^{O(1)}\bigr)^{O((k+1)^4)(h+1)}
       =N^{O((h+1)(k+1)^4)},
\]

which proves (1). Alternatively, applying their quantifier-free special case
to the projection lemma gives the same bound. No quantifier elimination is
performed by the eventual feasibility algorithm.

Choose an effective rational integer-coordinate box containing every point
of the size promised by (1). If the original mixed-integer set is nonempty,
this box retains at least one feasible integer assignment. It is harmless
if other feasible assignments are removed. Its bounds have polynomial bit
length for fixed \(k,h\).

Substitution of any integer assignment in this box produces a convex
continuous quadratic system of polynomial encoding length for fixed
\(k,h\), with Hessian span at most \(h\). The continuous minimum-norm
radius theorem supplies a uniform continuous-coordinate
box retaining a feasible point of every nonempty such fiber. Adding these
two boxes yields an equifeasible bounded instance. Apply the proved bounded
MILP reduction and fixed-integer-dimension MILP feasibility. Repeated
polynomial encoding growth can increase the exponent in \(N\); no sharp
combined running-time exponent is claimed.

The proof uses the large chart formula only to establish the witness bound.
The actual algorithm computes a conservative uniform size bound from the
input length and parameters, constructs the bounded reduction, and solves
it. It never enumerates active sets, rank charts, or the formulas (7).

## Convex quadratic objectives in the integer variables

**Corollary.** For fixed \(k,h\), a rational convex quadratic objective
\(f(z)\), including an affine objective, can be optimized exactly over the
mixed-integer set above in polynomial Turing time. The algorithm reports
infeasibility or unboundedness below; in the remaining case it returns an
optimal integer assignment and the exact rational optimal value. It does not
promise an exact continuous optimizer. A separate
[independent review](integer-objective-review.md) found no gap in this
strengthened corollary.

Choose a common positive denominator \(L\) for every polynomial coefficient,
including the constant term, so that \(p(z)=Lf(z)\) has integer coefficients.
Use the actual monomial coefficients if the input displays a factor \(1/2\)
in front of a quadratic form. Then \(p(z)\in\mathbb Z\) for integer \(z\),
and the encoding lengths of \(L,p\) are polynomial in the input length.
For the witness argument append an integer coordinate \(w\), and the
convex quadratic epigraph inequality

\[
 p(z)\le w.                                      \tag{8}
\]

The full Hessian of \(p(z)-w\) is PSD, and its \(xx\) block is zero.
The augmented integer projection is convex and admits the same chart
construction, with (8) added. Its continuous Hessian span remains \(h\),
while it now has \(k+1\) free integer coordinates. Every feasible original
assignment permits \(w=p(z)\), which is integral. Thus minimizing integer
\(w\) in the augmented system is exactly equivalent to minimizing \(p(z)\)
in the original one. Apply the optimization form of
Khachiyan--Porkolab Theorem 1.1 directly, rather than adding a coordinate
fixed to zero. After absorbing the polynomial encoding overhead into an
effective absolute constant, set

\[
 B=2^{\lceil N^{c(h+1)(k+2)^4}\rceil}.             \tag{9}
\]

If a finite minimum exists, the theorem gives an optimal pair \((z^*,w^*)\)
with \(\|z^*\|_\infty,|w^*|\le B\). The constant in (9) can be chosen
uniformly before knowing whether the objective is bounded. Here \(N\)
includes the objective data, and can be increased to two if necessary.

First decide original feasibility. If feasible and \(p\) is bounded below,
its minimum is attained because all feasible \(p(z)\) are integers: a
nonempty subset of \(\mathbb Z\) bounded below has a smallest element.
The equivalent augmented problem attains its minimum too, so the optimal-pair
bound applies. It follows that the additional
exact feasibility query

\[
 (z,x)\in C,\quad z\in\mathbb Z^k,\quad p(z)\le-B-1              \tag{10}
\]

is feasible if and only if the objective is unbounded below. Indeed, an
unbounded objective satisfies every finite threshold, whereas a finite
minimum has value at least \(-B\). The input of (10) has polynomial
encoding length for fixed \(k,h\). Its added constraint is jointly convex
and has zero continuous Hessian, so the feasibility theorem applies with
the original \(k,h\).

If (10) is infeasible, the optimal integer value lies in \([-B,B]\).
Maintain an infeasible lower threshold \(a=-B-1\) and a feasible upper
threshold \(b=B\); feasibility of the latter follows from the optimal-pair
bound. Binary-search integer thresholds with the exact feasibility queries
\(p(z)\le\lfloor(a+b)/2\rfloor\). Each query preserves \(k,h\) and has
polynomial input length for fixed parameters. After \(O(\log B)\) queries,
\(b=a+1\), and \(b\) is the exact optimal value of \(p\).

A final query at \(p(z)\le b\) returns an integer assignment \(z^*\)
with a nonempty original continuous fiber. Optimality implies \(p(z^*)=b\),
so the original objective value is exactly \(b/L\). The auxiliary integer
coordinate \(w\) was used only in the witness proof. The actual threshold
queries keep precisely the original integer variables.

The argument uses the discreteness of the objective values twice, for
attainment and for the optimization form of the integer-witness theorem.
It does not justify the same conclusion for an objective containing
continuous variables.

## Literature comparison and limitations

The small integer point theorem itself is established prior work.
Khachiyan--Porkolab Theorem 1.1 is essential here, including its independence
from the number of predicates. A direct use of their theorem on the original
formula \(\exists x\ (z,x)\in C\) has an exponent depending on the
continuous dimension \(n\). The proposed contribution is a different
projection description with bounded degree and height in terms of \(h\),
although that description may be long.

[Del Pia, *Convex quadratic sets and the complexity of mixed integer convex
quadratic programming*](https://arxiv.org/abs/2311.00099), Proposition 4 in the
examined version, gives a stronger FPT exact feasibility result for one
convex quadratic inequality with affine rows and unbounded variables. That
result is not improved on its own class. Here the number of quadratic rows
may grow, their affine terms are unrestricted, and only the span of their
continuous Hessian matrices is fixed. The case of many PSD matrices in a
fixed matrix span is not equivalent to assuming one quadratic row.

The proof does not yield a compact exact MILP for the entire unbounded
integer projection. Truncating to the witness box preserves nonemptiness,
not all feasible integer assignments. Nor does it show an FPT dependence on
\(k,h\), a useful numerical bound, or an implementation advantage over
existing solver methods. Those require further work.

Dependence on the number of integer variables is necessary for a polynomial
witness bound, even when \(h=0\). Consider the purely integer chain

\[
 z_1\ge2,\qquad z_{j+1}\ge z_j^2\quad(j=1,\ldots,k-1).
\]

Each quadratic row is jointly convex, and there are no continuous variables,
so the continuous Hessian span is zero. Induction gives
\(z_k\ge2^{2^{k-1}}\); equality is feasible. Thus every feasible integer
assignment needs at least \(2^{k-1}+1\) bits for its last coordinate,
whereas the sparse input has \(O(k\log k)\) bits. This classical repeated-
squaring mechanism is a direct limitation, not a novelty claim. The theorem
fixes \(k\) as well as \(h\).

No claim is made for merely slice-convex systems whose joint feasible set is
nonconvex: the projection lemma still applies, but the convex integer-witness
theorem need not. Positive-semidefinite full Hessians are a sufficient
checkable condition for the convexity required by the algorithmic conclusion.

The literature search examined the original Khachiyan--Porkolab theorem and
quantifier-elimination bounds, Del Pia's one-row theorem, and the earlier
Hessian-span prior audit. No equivalent fixed-continuous-Hessian-span theorem
was identified in that search. This does not establish novelty.

## Verification record

This note records a symbolic proof construction. No computation or Lean
verification establishes the projection equivalence or complexity bound.
The important proof obligations are the parameter-dependent rank charts,
the fixed-support subsequence, positive-denominator clearing, boundedness in
(7), the coefficient-height bound independent of chart count, and the exact
scope of the imported integer-witness theorem. The linked independent review
found no remaining gap after correction of a background closedness assertion.
Its targeted exact script checks exceptional rank charts, diverging
multipliers, and denominator signs; these checks do not verify the general
proof. No project-wide verification or CI inspection was performed.
