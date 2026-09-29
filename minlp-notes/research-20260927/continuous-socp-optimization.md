# Exact affine optimization over SOCP systems with few squared-Hessian directions

Date: 2026-09-28. Status: complete reduction proof;
[independent review](continuous-socp-optimization-review.md) found no gap
conditional on the stated theorem inputs, whose separate reviews are complete.
The [minimum-norm optimizer encoding theorem](nonconvex-attainment-and-optimizer.md)
and its [review](nonconvex-attainment-review.md) supply the attainment and
canonical-point bounds. No separate novelty claim
is made for bisection, algebraic recognition, or minimum-norm selection.

For a rational continuous SOCP with an affine objective, rational threshold
decisions recover the exact finite infimum even when it is not attained.
A bound for a minimum-norm optimizer, when one exists, also permits an exact
attainment decision. Exact value comparisons then simulate feasibility on
the optimal face without introducing algebraic coefficients into a conic
oracle.

## 1. Input and theorem inputs

Let

\[
 F=\{x\in\mathbb R^n:Lx\le a,\ Ex=e,
       \ \|A_ix+b_i\|_2\le c_i^Tx+d_i\quad(1\le i\le m)\},
 \qquad f(x)=u^Tx+v,                                      \tag{1}
\]

with rational explicitly encoded data. A supplied rational box can be
included among the affine rows, but none is required. Put

\[
 q_i(x)=\|A_ix+b_i\|_2^2-(c_i^Tx+d_i)^2,
 \qquad
 h=\dim_{\mathbb Q}\operatorname{span}
          \{2(A_i^TA_i-c_ic_i^T):1\le i\le m\}.             \tag{2}
\]

The quadratic description retains every sign condition
\(c_i^Tx+d_i\ge0\). Its native quadratics need not be convex; the
original SOC set \(F\) is closed and convex. The parameter depends on
the given representation.

Let \(N\ge2\) be total binary input length. For coefficient-sensitive
accounting, let \(S\ge2\) bound variables, rows, cone coordinates,
scalar coefficient positions, and index lengths in a dense encoding, and
let \(\tau\ge1\) bound each rational coefficient's numerator and
denominator bit lengths, including the objective. Dense expansion changes
structural size only by a fixed polynomial factor. All constants implicit
below are effective and absolute.

The reduction uses these separate inputs:

1. [Exact SOCP feasibility](socp-hessian-span-frontier.md) for rational
   systems of squared-Hessian span \(s\), with or without a box, has
   bit cost
   \[
                  (\tau+1)^{O(1)}S^{O(s+1)}.                \tag{3}
   \]
   The coefficient-size exponent is independent of \(s\). Arbitrary
   rational affine rows are allowed, and no Slater assumption is made.
2. The [finite-infimum theorem](nonconvex-finite-infimum.md), including
   its reviewed coefficient-sensitive refinement, bounds every finite
   infimum of a rational quadratic objective on a nonempty quadratic
   system. In our input it gives a nonzero integer annihilator with
   \[
       D\le S^{O(h+1)},\qquad H\le(\tau+1)S^{O(h+1)},       \tag{4}
   \]
   where \(D\) bounds degree and \(H\) bounds coefficient bits.
   The theorem does not require attainment. Passing to the primitive
   minimal polynomial retains these forms of bound.
3. The reviewed [attained-optimizer theorem](nonconvex-attainment-and-optimizer.md)
   states that, if a rational quadratic objective attains its infimum on
   a rational quadratic system, some global minimum-norm optimizer has
   common-field degree \(S^{O(h+1)}\) and coordinate minimal-polynomial
   coefficient bits \((\tau+1)S^{O(h+1)}\). The objective Hessian is
   excluded from \(h\). This is the additional substantive input for
   Sections 4--6.
4. The reviewed [algebraic recognition input](algebraic-recognition-source-review.md)
   and [common-field recovery theorem](constructive-common-field-recovery.md)
   recover an exact selected algebraic value, or tuple, from effective
   degree and height bounds and certified approximations. Their overhead,
   query count, and requested precision are polynomial with absolute
   exponents in those bounds. The tuple theorem requires a joint-field
   degree bound, not just separate coordinate degree bounds.

**Exact-value corollary.** From inputs 1, 2, and 4, there is a deterministic
algorithm that classifies (1) as infeasible, unbounded below, or having finite
infimum. In the finite case it returns the exact infimum as a primitive
integer minimal polynomial and a rational isolating interval. Its time and
output length are

\[
                  (\tau+1)^{O(1)}S^{O(h+1)}
                         \le N^{O(h+1)}.                    \tag{5}
\]

**Attainment and optimizer corollary.** Using input 3 as well, the same
bound permits deciding whether a finite infimum is attained.
If it is, the algorithm returns the unique global minimum-norm optimizer
\(x^*\) in one common field:

\[
 P(\alpha)=0,\qquad x_j^*=b_j(\alpha),\qquad
 b_j\in\mathbb Q[T],\quad \deg b_j<\deg P,                  \tag{6}
\]

where \(P\) is primitive, integer, and irreducible and a rational interval
isolates the intended real root \(\alpha\). The common-field degree is
\(S^{O(h+1)}\), and total output length and time satisfy (5).
For fixed \(h\), these are polynomial-time statements. They are not
fixed-parameter bounds \(g(h)N^C\) with an absolute exponent \(C\).
The case \(n=0\) is handled by rational comparisons and the empty tuple;
below assume \(n\ge1\).

## 2. Feasibility, unboundedness, and the finite value

First decide whether \(F\) is empty using (3). If it is nonempty,
let \(\theta=\inf_F f\), possibly \(-\infty\). Compute an effective
integer coefficient-bit bound \(H\) from (4). Cauchy's root bound gives

\[
                  |\theta|<M:=2^{H+2}                     \tag{7}
\]

whenever \(\theta\) is finite. The bound is computed from input size
and \(h\), not from an already known optimizer or infimum.

Query feasibility of \(F\cap\{f\le-M-1\}\). If feasible, (7)
rules out a finite infimum, so report unboundedness below. Conversely an
unbounded-below objective satisfies every finite threshold somewhere.
This returns a classification; no recession-ray certificate is asserted.
The threshold is an affine row and does not increase \(h\).

In the finite case, bisect \([a,b]=[-M-1,M+1]\), preserving
\(a\le\theta\le b\) and a feasible upper threshold \(b\).
At a midpoint \(t\), feasibility of \(F\cap\{f\le t\}\)
replaces \(b\) by \(t\); infeasibility replaces \(a\) by \(t\).
The initial upper threshold is feasible because \(b>\theta\).
If \(t=\theta\) and the infimum is unattained, the answer is no, and
the enclosing invariant still holds. No strict-inequality oracle is needed.

An interval of width at most \(2^{-p}\) gives a midpoint approximation
with error less than \(2^{-p}\). Its construction uses
\(O(H+p+1)\) rational feasibility queries. The recognition theorem
recovers the minimal polynomial from sufficiently accurate approximation,
with precision polynomial in \(D,H\); further root isolation selects
the intended root. This proves exact recovery even in the unattained case.

## 3. Cost of the exact-value subroutine

It is useful to record the cost for any rational affine objective and
rational SOC domain with structural size \(S_q\), coefficient bits
\(\tau_q\), and squared-Hessian span \(s\). Equations (3)--(4)
apply with these parameters. The root bound, the bisection count, and the
recognition precision are bounded by

\[
                 (\tau_q+1)^{O(1)}S_q^{O(s+1)}.             \tag{8}
\]

Every threshold query retains the same native cone maps and adds one
affine objective row. Its structural size is \(S_q^{O(1)}\), independent
of precision. Its coefficient bits have the bound (8). Applying (3)
raises those bits only to an absolute power. Multiplying by the query
count and recognition overhead therefore gives

\[
 T_{\rm value}(S_q,\tau_q,s)
             \le(\tau_q+1)^{O(1)}S_q^{O(s+1)}.              \tag{9}
\]

This subroutine first detects an empty domain and otherwise returns the
classification and exact finite value. For a nonempty compact domain it
always returns a finite attained value. Its internal rational LP lift can
gain rows and variables with precision. That lift is used only to solve
the feasibility query; it is never structural input to a later algebraic
bound. This distinction prevents an unnecessary quadratic exponent in
\(h\).

## 4. A universal box decides attainment

Assume the additional attained-optimizer input in Section 1. If the finite
value \(\theta\) is attained, its optimal set

\[
                      F^*=\{x\in F:f(x)=\theta\}           \tag{10}
\]

is nonempty, closed, and convex. The squared norm attains its minimum on
this set by restricting to a closed ball through any one optimizer.
Strict convexity gives a unique minimizer \(x^*\). Thus the point in
the attained-optimizer theorem must be this same \(x^*\).

Take a uniform coordinate minimal-polynomial height bound
\(H_*\le(\tau+1)S^{O(h+1)}\) from that theorem, and compute

\[
               R=2^{H_*+2},\qquad B=[-R,R]^n.                \tag{11}
\]

Cauchy's bound shows that \(x^*\in B\) whenever an optimizer exists.
The construction of \(R\) does not assume that attainment has already
been decided. This is an optimizer bound; a box known only to contain
some feasible point would not suffice.

Apply the exact-value subroutine to \(C=F\cap B\). If \(C\) is
empty, the finite infimum is unattained. Otherwise compactness gives an
attained minimum \(\beta=\min_C f\), and

\[
              \theta\text{ is attained on }F
                   \quad\Longleftrightarrow\quad\beta=\theta. \tag{12}
\]

For the forward direction, \(x^*\in C\) gives equality. For the
reverse direction, a minimizer on compact \(C\) is an original
optimizer. Both values are exactly represented real algebraic numbers, so
equality is decided by polynomial-time univariate root comparison, with
their isolating intervals selecting the intended roots. Numerical closeness
alone is not used.

The box adds only \(2n\) affine rows. Its coefficient bits are
\((\tau+1)S^{O(h+1)}\), while its structural size stays polynomial
in \(S\). Substitution in (9) preserves (5).

## 5. Feasibility on the optimal face using rational queries

Suppose (12) has established attainment, and set
\(C^*=C\cap F^*\). It is compact and convex and contains \(x^*\).
There is no need to submit the algebraic equation \(f=\theta\) to
the rational feasibility oracle.

Let \(K\) consist of rational closed affine restrictions and, optionally,
one rational squared-norm bound \(\|x\|_2^2\le r\), \(r\ge0\).
The latter has the rational SOC form

\[
                 \|(2x,r-1)\|_2\le r+1.                    \tag{13}
\]

Its squared residual is \(4\|x\|_2^2-4r\), so it adds only the
Hessian direction \(8I\). Every queried system therefore has
squared-Hessian span at most \(h+1\).

Define an exact Boolean oracle \(\mathcal E(K)\) as follows. Decide
whether \(C\cap K\) is empty. If it is, answer no. Otherwise compute
\(\beta_K=\min_{C\cap K} f\) by (9), and answer yes exactly when
\(\beta_K=\theta\). Then

\[
             \mathcal E(K)=\text{yes}
                  \quad\Longleftrightarrow\quad
                         C^*\cap K\ne\varnothing.           \tag{14}
\]

Indeed \(C\cap K\) is compact, all its objective values are at
least \(\theta\), and its minimum is attained. This last point is
essential: equality of an unattained infimum with \(\theta\) would
not imply (14). All underlying SOCP data are rational. The sole operation
involving \(\theta\) is a comparison of two recovered algebraic values.

## 6. Recover one fixed canonical optimizer

Use (14) in place of ordinary feasibility in the minimum-norm approximation
argument from [SOCP witness recovery](socp-exact-witness-recovery.md).
Here are the invariants explicitly.

For each requested accuracy \(p\ge1\), start afresh from \(B\), and
write \(\delta=2^{-p}\) and \(\nu=\|x^*\|_2^2\). Bisect
\([0,nR^2]\) for \(\nu\) using \(\mathcal E(\|x\|_2^2\le r)\).
Maintain \(\ell\le\nu\le u\) with a feasible upper cap, and stop
when \(u-\ell\le\delta^2/16\). The initial upper cap is feasible;
the initial lower endpoint need not be infeasible. Put

\[
                    G=C^*\cap\{x:\|x\|_2^2\le u\}.        \tag{15}
\]

This is a nonempty set, and every \(y\in G\) satisfies
\(\|y\|_2^2\le\nu+\delta^2/16\). Convexity of \(C^*\)
and minimum-norm optimality give

\[
 \langle x^*,y-x^*\rangle\ge0,\qquad
 \|y-x^*\|_2^2\le\|y\|_2^2-\nu,
 \qquad \|y-x^*\|_2\le\delta/4.                           \tag{16}
\]

Now bisect the coordinate intervals of \(B\), retaining a nonempty
intersection with \(G\). Test the closed lower half with (14); if
infeasible, retain the closed upper half. Their union is the current
interval, so feasibility persists, including on boundaries. Keep the norm
cap fixed and store only the two current endpoints per coordinate. Stop
when every width is at most \(\delta\). For the rational midpoint
\(c\) of the final box, some \(y\in G\) in that box gives

\[
            |c_j-x_j^*|\le\delta/2+\delta/4<2^{-p}.         \tag{17}
\]

The midpoint need not be feasible. It approximates the same fixed global
minimum-norm optimizer at every requested accuracy. A previous request's
final box can exclude \(x^*\), which is why each request restarts from
\(B\).

The additional attained-optimizer theorem supplies

\[
 [\mathbb Q(x_1^*,\ldots,x_n^*):\mathbb Q]
          \le S^{O(h+1)},\qquad
 H_*\le(\tau+1)S^{O(h+1)}.                                \tag{18}
\]

This is a bound on one joint field, not a product of individual coordinate
degrees. Equations (17)--(18) meet the common-field recovery theorem's
input model and yield (6), with the intended real embedding selected.

For the final time bound, put \(\sigma=\lceil\log_2R\rceil\).
There are polynomially many norm and coordinate bisections in
\(S,\sigma,p\), with absolute polynomial exponents. Each query has
structural size \(S^{O(1)}\), span at most \(h+1\), and coefficient
bits at most \((\tau+\sigma+p+1)S^{O(1)}\). By (9), including
the exact comparison in (14), the approximation cost is

\[
 T_{\rm approx}(p)
       \le(\tau+\sigma+p+1)^{O(1)}S^{O(h+1)}.              \tag{19}
\]

Common-field recovery requests only polynomially many accuracies, each
polynomial in \(n\), the joint degree, and \(H_*\). Both its
maximum precision and its remaining overhead are
\((\tau+1)^{O(1)}S^{O(h+1)}\). Since
\(\sigma\le(\tau+1)S^{O(h+1)}\), substituting these bounds in
(19) proves (5) for optimizer recovery as well. No coefficient-size
quantity is raised to a power depending on \(h\).

## 7. Checks, examples, and scope

An exactly represented optimizer can be checked against every original
affine row, each squared cone row, and its affine sign condition using the
common-field sign procedure. To check the objective, let \(P_\theta\)
and \((a_\theta,b_\theta)\) represent the recovered \(\theta\), with
nonroot endpoints. Check \(P_\theta(f(x))=0\) and
\(a_\theta<f(x)<b_\theta\) in the point's own field. This verifies
\(f(x)=\theta\) without constructing a compositum. Correctness of the
algorithm establishes that \(\theta\) is the infimum; a feasible-point
representation alone does not certify that lower bound or the minimum-norm
selection.

Finite nonattainment occurs already with one squared-Hessian direction:

\[
       \|(2,x-y)\|_2\le x+y,\qquad x,y\ge0,
       \qquad\min x.                                     \tag{20}
\]

The squared residual is \(4-4xy\), so the feasible set is
\(x,y\ge0\), \(xy\ge1\). The infimum is zero and is unattained.
For any \(R\ge1\), its minimum in \([-R,R]^2\) is \(1/R>0\),
which illustrates the exact distinction used in (12).

An attained irrational value needs only the rational cone
\(\|(1,1)\|_2\le x\) and the objective \(\min x\). Its optimizer
and value are \(\sqrt2\), and its squared-Hessian span is one.
Thus rational exact output is insufficient even in this small class.

This is an algorithmic consequence of the linked value, optimizer-encoding,
and rational conic-decision results. Priority for exact optimization on the
whole class is not established here. In particular, the
[SOCP prior audit](socp-hessian-span-prior.md) derives feasibility throughout
the case \(h\le1\) from earlier algebraic bounds; this note makes no
separate novelty claim for optimization at \(h=1\).

This note concerns continuous variables and affine objectives. It gives
no mixed-integer optimization theorem, no algorithm for general nonconvex
quadratic optimization, and no extension to a convex quadratic objective
through an irrational Cholesky factor. No practical numerical constants
or empirical solver advantage are asserted. The proof needs no interior
point, bounded original feasible set, or rational feasible-point promise.

The author ran `python -` with a targeted inline script checking this
file's local links, paired math delimiters, trailing whitespace, control
characters, and final newline. SymPy checks in the same command verified
the norm-cone residual, the residual and Hessian in (20), the boundary
point \((1/R,R)\), and the irrational optimizer example. These checks
passed. They do not implement recognition, the optimization algorithm, or
the universal degree and height bounds.

The saved [independent review](continuous-socp-optimization-review.md)
found no gap in the reduction conditional on its stated theorem inputs.
Their separate reviews are also complete. No project-wide checks or CI
inspection were performed.
