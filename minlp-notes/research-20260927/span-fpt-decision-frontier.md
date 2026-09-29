# A decision benchmark for an FPT Hessian-span algorithm

Date: 2026-09-28. Status: the reduction and the precision lower example
below are proved directly and have received an
[independent adversarial review](span-fpt-decision-review.md). They do not
establish either FPT tractability or parameterized hardness. The
[primary-source audit](span-fpt-prior-audit.md) separates the existing XP
algorithms and unrestricted decision-hardness results from that question.

The target is an exact feasibility algorithm with running time
`g(h) N^C`, where `C` is absolute and `h` is the span dimension of the
native Hessian matrices. The current local `N^{O(h+1)}` algorithms are
XP. The [common-range theorem](common-range-fpt-frontier.md) gives a
genuine FPT result for a different parameter. The present note isolates
a compact, strictly convex optimization family whose threshold decisions
an FPT matrix-span algorithm would have to handle. Its large algebraic
degree makes ordinary elimination expensive, but supplies no decision
lower bound.

## 1. Selected secular values

For block `i`, the input consists of positive rational numbers
`d_ij`, rational numbers `b_ij`, and dimension `r_i`. Define

\[
 f_i(x)=\frac12\sum_{j=1}^{r_i}d_{ij}x_j^2
              -\sum_{j=1}^{r_i}b_{ij}x_j,
 \qquad
 \beta_i=\min_{\|x\|_2\le1}f_i(x).
\]

The **selected secular-sum comparison** problem asks whether
`sum_i beta_i <= t` for a rational input `t`. Its parameter is the number
`k` of blocks; the block dimensions remain unrestricted. This is a name
for this note's explicit benchmark, not an established complexity class.

Each block has a unique minimizer. If

\[
 \sum_j b_{ij}^2/d_{ij}^2\le1,
\]

the unconstrained minimizer is feasible and
`beta_i = -sum_j b_ij^2/(2d_ij)` is rational. Otherwise there is a unique
positive number `lambda_i` satisfying

\[
 R_i(\lambda_i)=1,
 \qquad
 R_i(T)=\sum_j\frac{b_{ij}^2}{(T+d_{ij})^2}.       \tag{1}
\]

Indeed, `R_i` is strictly decreasing on `[0,infinity)`, starts above
one, and tends to zero. The KKT equations give

\[
 x_{ij}=\frac{b_{ij}}{d_{ij}+\lambda_i},\qquad
 \beta_i=-\frac12\left(\lambda_i+
                 \sum_j\frac{b_{ij}^2}{d_{ij}+\lambda_i}\right). \tag{2}
\]

The multiplier is normalized so that the Lagrangian uses
`lambda_i (||x||^2-1)/2`. Formula (2) follows from stationarity and
`||x_i||=1`; the factor of one half is part of the formula.

Clearing the denominators in (1) yields a polynomial of degree at most
`2r_i`. Repeated diagonal entries or zero `b_ij` can lower the degree and
can introduce denominator factors in an unreduced polynomial. The
definition always selects the unique positive solution of (1), so it does
not select arbitrary roots of the cleared polynomial. The value belongs
to the multiplier's number field by (2).

## 2. A parameter-preserving convex threshold reduction

**Proposition.** Selected secular-sum comparison reduces in polynomial
time to exact feasibility of rational globally convex quadratic
inequalities with Hessian span at most `k+1`. The resulting set is
contained in a product of Euclidean unit balls. All non-affine input
polynomials have positive-semidefinite Hessians, and its objective-budget
row has a positive-definite Hessian.

Use disjoint block variables and impose

\[
 \|x_i\|_2^2\le1 \quad(i=1,\ldots,k),\qquad
 \sum_i f_i(x_i)\le t.                            \tag{3}
\]

The minimum of the sum over the product is the sum of the minima:
each feasible block has `f_i(x_i)>=beta_i`, and the simultaneous unique
block minimizers attain equality. Thus (3) is feasible exactly when the
comparison answer is yes. The ball Hessians are twice the `k` block
identity matrices. The budget adds the single positive diagonal matrix
`diag(d_11,...,d_kr_k)`. This proves the span bound and all representation
claims. The data are copied with only rational linear and constant terms
added, so the construction has polynomial encoding length.

If `t > sum_i beta_i`, the system (3) has a strictly feasible point.
Start at the block minimizers and multiply every block by `1-epsilon`.
All ball inequalities become strict, and continuity preserves the strict
budget inequality for sufficiently small positive `epsilon`. If
`t = sum_i beta_i`, the feasible set is the single product minimizer,
because the sum objective is strictly convex. The set of ball constraints
itself always has the explicit strict point zero. Therefore the benchmark
does not depend on unboundedness, nonattainment, indefinite squared SOC
rows, or a difficult affine-row representation.

An FPT exact native-PSD feasibility algorithm in `h` would consequently
give an FPT algorithm in `k` for selected secular-sum comparison. This is
the implication established here. The converse for general Hessian-span
instances is not proved.

## 3. What the existing degree construction contributes

The [short-input degree construction](short-input-qcqp-degree-lower-bound.md)
uses precisely independent diagonal trust-region blocks of this type,
with positive rational objective weights absorbed into the `d_ij` and
`b_ij`. It supplies families for which

\[
 [\mathbb Q(\beta_1+\cdots+\beta_k):\mathbb Q]
     =\prod_{i=1}^k 2r_i.                         \tag{4}
\]

Its explicit coefficient bounds are essential: generic algebraic degree
alone would not establish a lower bound relative to input length. For
fixed `k`, that note gives arbitrarily large block-size scales `R`, input
length `N=O_k(R^2 log R)` for its existential short-weight version, and
degree `Omega_k(R^k)`. Its deterministic weight version also has an input
exponent independent of `k`, with a larger absolute exponent. Appending a
rational budget `t` changes the Hessian-span parameter by at most one.

Consequently a decision method that *first prints the full minimal
polynomial of this sum in dense form* cannot have an FPT running time in
`k`. The [sparse-output refinement](sparse-algebraic-output-boundary.md)
also defeats ordinary sparse minimal-polynomial lists after a small
rational objective translation. These are output and representation
obstructions. Neither establishes a lower bound for comparing the
selected sum with a rational number, using a determinant or circuit
representation, retaining separate number fields, or avoiding algebraic
reconstruction altogether.

In particular, (4) alone does **not** show that the sum can lie within
`2^{-N^{Omega(k)}}` of a rational budget of short encoding length. A
degree-based separation estimate is an upper bound on required
precision, not an example attaining it. Turning such an estimate into a
necessary precision claim would be a further substantive result.

Square-Root Sum is contained in the more general product-ball threshold
idea by setting the block objectives linear. It does not give the desired
parameterized obstruction: the classical radical separation bound already
yields `2^{O(k)} poly(N)` bit complexity when the number of radicals is
the parameter. The positive diagonal quadratic objectives in (1)--(2)
allow unbounded algebraic degree within each block, distinguishing this
benchmark from that elementary FPT consequence.

## 4. An actual precision obstruction, of a different size

There is a simple family showing that any *uniform residual-gap method*
needs exponential dependence on Hessian span. This is the familiar
repeated-squaring mechanism; it is included to distinguish a genuine
lower example from the unsupported inference after (4).

For `h>=1`, use variables `x_0,...,x_h`, the affine equation `x_0=1/2`,
the box `[0,1]^{h+1}`, and the convex inequalities

\[
 x_{i-1}^2-x_i\le0\quad(i=1,\ldots,h),\qquad x_h\le0. \tag{5}
\]

The `h` nonzero Hessians have disjoint coordinate supports and are
linearly independent. The system is infeasible: induction gives
`x_i >= 2^{-2^i} > 0`, contradicting the last inequality. Nevertheless
the boxed point `x_i=2^{-2^i}` satisfies all rows except the last, whose
residual is `2^{-2^h}`. Therefore, if

\[
 \alpha_h=\min_{x\in[0,1]^{h+1},\ x_0=1/2}
       \max(0,x_0^2-x_1,\ldots,x_{h-1}^2-x_h,x_h),
\]

compactness and infeasibility give

\[
 0<\alpha_h\le 2^{-2^h}.                          \tag{6}
\]

The coefficient magnitudes are constant, and either sparse or explicit
dense input encoding has size polynomial in `h`. Thus a guaranteed
positive residual gap for this family cannot have logarithmic reciprocal
bounded by a polynomial in `h`. This excludes a uniformly polynomial
precision bound with no parameter-dependent factor. It is fully
consistent with a bound `2^{poly(h)} N^C`, and therefore with FPT
feasibility. It also does not lower-bound the running time of a decision
algorithm: induction decides (5) immediately without numerical
approximation.

## 5. Consequence for the research direction

The most useful next target is a decision-specific separation or
certificate theorem, starting with the compact benchmark (3). A proof
that its nonzero rational-threshold gaps always have reciprocal logarithm
`g(k) N^C` would bypass the generic product-degree estimate for this
family. Here the bound must be uniform and effective, `N` includes the
rational budget, and the intended dichotomy is
`|sum_i beta_i-t|=0` or `|sum_i beta_i-t|>=2^{-g(k)N^C}`.
Such a bound would imply an FPT comparison algorithm: rational secular
bisection approximates each block optimum in time polynomial in input
length and requested accuracy, and an interval narrower than the supplied
nonzero gap distinguishes equality from either sign. It would not by
itself solve general Hessian-span feasibility.

A negative direction needs more than (4) or (6). It could supply an
explicit family with super-FPT required rational precision for the
chosen approximation strategy, or a parameter-preserving reduction from
a recognized parameterized decision problem. The latter would have to
retain native convex inequalities and `h` bounded by the source
parameter. The usual Boolean forcing inequalities, nonconvex polynomial
equalities, and convex maximization encodings do not meet that condition.

This is a useful narrowing of the problem, not a proposed principal
contribution. The primary-source audit does not locate an existing
algorithm or hardness theorem settling it, but an unsuccessful search
does not establish novelty. Full exact feasibility, generic optimizer
recovery, uniform approximation precision, and sparse arithmetic
representations remain separate questions.

## Verification record

The reduction is direct: product separability proves equivalence, and the
displayed Hessians give the parameter count. The secular formulas are
derived from strictly convex KKT conditions and a monotone univariate
equation. The repeated-squaring residual bound is exact. The accompanying
`python3 research-20260927/check_span_fpt_benchmark.py` passed. It checks
a nontrivial rational block's cleared
polynomial and value identity and exact instances of (5). It does not
verify an FPT theorem, prove a hardness lower bound, or recheck the full
degree constructions cited above. Targeted checks only; no project-wide
verification or CI inspection.
