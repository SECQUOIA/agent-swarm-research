# Review: exact integer projections for vector polynomial fitting

Date: 2026-09-27. This is an independent application and significance review.
The corollary below follows from the batch's Hessian-span theorems; it is
not a separate priority claim. The algebra and modeling reduction pass this
review. Practical benefits and novelty relative to all robust-fitting
literature remain unestablished.

## 1. The application that the theorem actually covers

Let

\[
 P_x(t)=\sum_{j=0}^{d}x_jt^j,\qquad x_j\in\mathbb R^r.
\]

The input consists of rational sample parameters \(t_i\), rational response
vectors \(y_i\in\mathbb Q^r\), rational squared tolerances
\(\tau_i\ge0\), and rational affine restrictions on the coefficients and
binary variables \(z\). The intended observation decision is

\[
 z_i=0\quad\Longrightarrow\quad
 \|P_x(t_i)-y_i\|_2^2\le\tau_i.                 \tag{1}
\]

Thus \(z_i=1\) permits discarding a whole vector observation. It does not
require its residual to exceed the tolerance. Minimizing
\(\sum_i w_i z_i\), with nonnegative rational weights, is a weighted
maximum-consensus model, possibly with additional affine restrictions on
which observations may be discarded. Statements about which observation is a
statistical outlier require assumptions beyond this optimization model.

For a supplied rational coefficient box, choose valid rational constants
\(M_i\ge0\) and write (1) as

\[
 q_i(x,z):=\|P_x(t_i)-y_i\|_2^2-\tau_i-M_i z_i\le0.  \tag{2}
\]

Its full Hessian in \((x,z)\) is positive semidefinite: all appearances of
\(z\) are affine. Order \(x\) by polynomial coefficient, and define
\(v_d(t)=(1,t,\ldots,t^d)^T\). Then

\[
 \nabla^2_{xx}q_i
   =2v_d(t_i)v_d(t_i)^T\otimes I_r
   =2\sum_{\ell=0}^{2d}t_i^\ell H_\ell,          \tag{3}
\]

where the \((a,b)\) block of \(H_\ell\), indexed from zero, is
\(I_r\) when \(a+b=\ell\), and zero otherwise. Consequently

\[
 h\le\min(m,2d+1).                              \tag{4}
\]

The response values and tolerances affect only affine and constant terms,
so they do not increase this bound. Neither do arbitrary rational affine
linking constraints, additional affine-linked continuous variables, or
bounded integer variables appearing only in those affine rows.

The [integer-projection theorem](mixed-integer-span-frontier.md) therefore
gives a rational MILP of polynomial total encoding length for every fixed
\(d\), even when both \(r\) and the number of observations grow. Its
integer variables are precisely the original integer variables, and its
feasible integer assignments are exactly those of (1). The statement
preserves every feasible discard pattern, not just the optimal count.

The theorem does **not** preserve the original continuous coefficient
fibers. A coefficient vector returned directly from the MILP can violate
the original norm constraints; the selected pattern has some exactly
feasible coefficient vector. Likewise, this construction alone does not
give an exact polynomially encoded continuous estimator. Rational linear
objectives depending only on the original integer variables are preserved.

Polynomial formulation size does not imply a polynomial-time algorithm
for maximum consensus when the number of binary decisions grows. The
fixed-integer-dimension algorithmic consequence applies only if the total
number of integer variables is fixed.

## 2. Valid discard constants, including initially unbounded coefficients

With a box \(|x_{j\ell}|\le R\), put

\[
 A_i=R\sum_{j=0}^{d}|t_i|^j,\qquad
 U_i=\sum_{\ell=1}^{r}(A_i+|y_{i\ell}|)^2,
 \qquad M_i=\max\{0,U_i-\tau_i\}.                \tag{5}
\]

The triangle inequality bounds every squared residual by \(U_i\).
Thus row (2) imposes the intended tolerance when \(z_i=0\), and is
automatic on the box when \(z_i=1\). These constants are rational and
have polynomial binary length in the explicitly encoded box and data.
Tighter interval bounds can improve the constants but are unnecessary for
the existence result.

The coefficient box need not be supplied initially. Here is the precise
use of the [small feasible-point theorem](unbounded-hessian-span.md).

For a fixed binary pattern, remove every discarded observation row, retain
the other norm rows, and substitute that pattern into all affine links.
This is a rational convex quadratic system whose Hessian span is still at
most \(2d+1\). Its encoding length is bounded by a fixed polynomial in
the original input length \(N\), uniformly over all patterns. The
small-point theorem supplies a computable radius

\[
 R=2^{N^{O(d+1)}}                               \tag{6}
\]

after increasing the absolute constant in the exponent, such that every
nonempty pattern fiber has a feasible representative with all continuous
coordinates in \([-R,R]\). If additional continuous variables occur in
the affine links, include those coordinates in this common box as well.
No pattern enumeration is used to compute the radius.

Adding this one box preserves the existence of a feasible representative
for every pattern simultaneously. Use (5) to obtain finite discard
constants, and then apply the bounded integer-projection theorem. The
composed construction is polynomial in \(N\) for fixed \(d\); a
conservative parameterized statement is \(N^{\operatorname{poly}(d+1)}\)
because the radius's encoding length enters the subsequent construction.

This argument permits arbitrary rational affine links depending on the
binary decisions. If extra bounded integer variables are present, their
substitution length is uniformly polynomial as well. The argument does
not remove the requirement for bounds on additional unrestricted integer
variables.

The box is a bound on one representative per feasible pattern. It is not
a bound on every possible fit. It therefore cannot be inserted into an
unbounded continuous-objective problem without a separate argument that
the relevant objective values are preserved.

## 3. Multivariate inputs and extensions that retain the span bound

For \(p\) input coordinates and total degree at most \(d\), write

\[
 P_x(t)=\sum_{\alpha\in\mathbb N^p:\,|\alpha|\le d}
                x_\alpha t^\alpha.
\]

The \((\alpha,\beta)\) Hessian block of a squared Euclidean residual
is \(2t_i^{\alpha+\beta}I_r\). Grouping equal sums yields

\[
 h\le \#\{\gamma\in\mathbb N^p:|\gamma|\le2d\}
       =\binom{p+2d}{2d}.                       \tag{7}
\]

Every exponent with total degree at most \(2d\) can be split into two
nonnegative exponents of total degree at most \(d\), so this is the
natural product-space count. The integer-projection conclusion remains
polynomial for fixed \(p,d\), with growing response dimension and sample
count. It is not polynomial uniformly in arbitrary \(p,d\).

A common rational positive-semidefinite output weight \(W\), replacing
the squared norm by \((P_x(t_i)-y_i)^TW(P_x(t_i)-y_i)\), replaces each
\(I_r\) above by \(W\) and leaves the bound unchanged. More generally,
if the sample weights \(W_i\) lie in a known fixed-dimensional rational
matrix space of dimension \(s\), their Hessian span is at most
\(s\binom{p+2d}{2d}\). Arbitrary unrelated sample-specific weight
matrices need not satisfy a bounded-span hypothesis.

Introducing one separate residual vector \(e_i\) per observation and
putting the norm constraints on those new variables gives Hessians with
disjoint supports. Their span can have dimension \(m\). The proof must
use (3) in the original coefficient variables, or eliminate those residual
variables before measuring the parameter.

## 4. Comparators and cases where this is not a compelling application

**Ordinary scalar polynomial regression is a weak motivation.** If
\(r=1\) and the threshold is a rational radius \(\epsilon_i\), then
\(|P_x(t_i)-y_i|\le\epsilon_i\) is already two rational linear
inequalities. Polynomial evaluation is linear in its coefficients. A
standard big-M MILP handles the discard decisions directly. Writing a
scalar threshold instead as a rational squared value \(\tau_i\) can
introduce an irrational square root, but this arithmetic distinction is
not a persuasive main application. For fixed scalar polynomial degree,
the number of continuous coefficient variables is also fixed, so general
fixed-dimensional methods are another serious comparator.

The intended example has **growing vector response dimension**, Euclidean
residuals, and one shared discard decision per complete vector. In that
setting the continuous dimension is \((d+1)r\), and a norm ball in the
residual coordinates is not polyhedral when \(r\ge2\). Standard MILP
formulations for coordinatewise or polyhedral norm residuals concern a
different feasible set. The proposed result preserves only the finite
integer projection of the Euclidean model, so it does not claim to give a
polyhedral representation of a Euclidean ball.

**Some common data restrictions make sample rows redundant.** For
example, with degree one, affine response data
\(y_i=a+bt_i\), a common tolerance, and all sample parameters between
the two endpoints, the squared residual is a convex function of the
sample parameter. Enforcing the endpoint rows then enforces all
intermediate rows. Arbitrary response data do not have that property.
For instance, use parameters \(0,1/2,1\), responses
\(0,2e_1,0\), and squared tolerance \(1/4\). No affine vector
polynomial fits all three: the endpoint constraints imply
\(\|P(1/2)\|\le1/2\), whereas the middle constraint implies
\(\|P(1/2)\|\ge3/2\). Every pair can be fitted exactly by an affine
polynomial. This is a check of nonredundancy, not a hardness result.

**The input samples are fixed.** Fitting unknown sample locations,
minimizing orthogonal distance to a polynomial curve, imposing rotations
or orthogonality, and treating polynomial degree selection through
unboundedly many terms require new analysis. Those models generally do
not retain the joint convex quadratic structure in (2). The result does
not cover geometric fitting merely because the fitted object is called a
polynomial curve.

**Current practical formulations are serious comparators.** The
construction here can use enormous worst-case radii and approximation
depths. It proves existence of an exact rational formulation of the
integer patterns; it does not establish a stronger continuous relaxation,
better conditioning, faster branch-and-bound, or an advantage over modern
mixed-integer conic methods.

## 5. Primary sources examined and precise comparison

1. Tat-Jun Chin, Yang Heng Kee, Anders Eriksson, and Frank Neumann,
   [Guaranteed Outlier Removal with Mixed Integer Linear Programs](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Chin_Guaranteed_Outlier_Removal_CVPR_2016_paper.pdf),
   CVPR 2016. Read Sections 1--3, especially equations (3)--(4) and
   (19), and the discussion following (19). They formulate
   maximum-consensus selection using binary discard decisions. Scalar
   absolute residuals and vector polyhedral norms have direct MILP
   formulations. Their Euclidean vector-residual formulation uses
   second-order cones, so their MILP-based removal method does not apply
   directly. The present corollary concerns a structured subfamily of
   vector residual maps, and a rational MILP preserving their integer
   projection. It does not extend their general projective residual model,
   whose affine denominator is not present here.

2. Andres Gomez and Jose Neto,
   [Outlier detection in regression: conic quadratic formulations](https://optimization-online.org/wp-content/uploads/2023/05/Least_Trimmed_Squares-4.pdf),
   June 2023 manuscript. Read the abstract, introduction, Section 2, and
   the opening convexification results of Section 3. Their target includes
   least trimmed squares, with a binary decision multiplying each squared
   residual in the objective. They develop stronger conic formulations
   without big-M constraints. This is a different objective from the
   prescribed-tolerance feasibility model reviewed here. It supplies a
   strong practical comparator and cautions against claiming that a large
   theoretical MILP improves solver performance.

Searches also included combinations of “maximum consensus,” “vector
residual,” “polynomial fitting,” “multivariate least trimmed squares,”
and “mixed integer.” These searches were not an exhaustive audit of
multiresponse robust regression. No claim that this application is new
follows from failure to find the same corollary.

## 6. Review conclusion and verification scope

The Hessian expansion, joint convexity, uniform representative radius,
discard constants, and multivariate product-space count are valid. The
strongest precise application statement is a polynomial-size rational
MILP preserving all feasible sample-selection patterns for fixed-degree
vector polynomial fitting, with optional rational affine links and no
extra integer variables. The statement allows growing response dimension
and does not require initially bounded continuous coefficients, provided
the small-point theorem is used as above.

This review checked the algebra and the implication between formulations,
and examined the two primary-source comparisons. It did not independently
reprove quantitative elimination in the underlying Hessian-span theorem,
run solver experiments, or establish priority. No numerical tests or
project-wide verification were run for this review; the application
identities and the nonredundancy example are proved explicitly above.
