# Exact unbounded MISOCP optimization for integer-only objectives

Date: 2026-09-28. Status: supporting consequence; proof and fresh
[independent adversarial review](integer-objective-misocp-review.md)
completed, with no gap found. This note extends the reviewed
[unbounded feasibility result](unbounded-misocp-frontier.md). The discrete
epigraph argument is established machinery and was already used for the
[native convex quadratic class](unbounded-integer-frontier.md#convex-quadratic-objectives-in-the-integer-variables).
No separate novelty claim is made for this optimization corollary.

A rational convex quadratic objective depending only on the integer
coordinates can be optimized exactly over an unbounded rational MISOCP when
the integer dimension and squared continuous Hessian span are fixed. A finite
optimal value is rational and attained. This discrete-value argument does
not apply to an objective involving continuous coordinates.

## 1. Statement

Let \(z\in\mathbb Z^k\), \(x\in\mathbb R^n\), and let the feasible
set consist of rational affine rows and rational cone rows

\[
                 \|A_i(z,x)+b_i\|_2\le c_i^T(z,x)+d_i.
                                                               \tag{1}
\]

No variable bounds or Slater assumption are imposed. Set

\[
 h=\dim_{\mathbb Q}\operatorname{span}
     \{2(A_{ix}^TA_{ix}-c_{ix}c_{ix}^T):i\}.                    \tag{2}
\]

Let \(f(z)\) be a rational convex quadratic, including the affine and
constant cases. The total explicit input length \(N\ge2\) includes the
objective. Convexity here means that the objective Hessian is positive
semidefinite on \(\mathbb R^k\), not merely on the feasible integer
assignments.

**Theorem.** For fixed \(k,h\), a deterministic polynomial-time Turing
algorithm reports exactly one of the following:

1. the feasible set is empty;
2. the objective is unbounded below;
3. an optimal integer assignment \(z^*\), the exact rational minimum
   \(f(z^*)\), and an exactly feasible algebraic continuous vector
   \(x^*\) in one explicitly represented number field.

In the third case the minimum is attained. The exact continuous vector can
be omitted if only the assignment and objective value are wanted. Its
construction uses the separate
[SOCP witness-recovery theorem](socp-exact-witness-recovery.md). All output
lengths and running times are polynomial for fixed \(k,h\); no bound of
the form \(g(k,h)N^C\) with an absolute exponent is asserted.

## 2. Integer objective values and an optimal-pair bound

Choose a positive integer \(D\) clearing every actual polynomial
coefficient of \(f\), including its constant term. A product of the
denominators suffices and has polynomial bit length. If a quadratic form is
written with a factor \(1/2\), include that factor when computing the
monomial coefficients. Then

\[
                 p(z)=Df(z)\in\mathbb Z[z_1,\ldots,z_k].       \tag{3}
\]

In particular \(p(z)\) is an integer whenever \(z\) is integral.
For any nonempty feasible set, its attainable \(p\)-values form a
nonempty subset of \(\mathbb Z\). If that subset is bounded below, it
has a least element, achieved by a feasible assignment and some point in its
continuous fiber. No compactness assertion is involved.

For the size bound only, introduce one more integer coordinate \(u\) and
the epigraph inequality

\[
                             p(z)\le u.                       \tag{4}
\]

Let \(Y\subseteq\mathbb R^k\) be the original real projection onto
\(z\), and put

\[
          \widehat Y=\{(z,u)\in Y\times\mathbb R:p(z)\le u\}.
                                                               \tag{5}
\]

The real cone system is convex, so \(Y\) is convex. Convexity of \(p\)
therefore makes \(\widehat Y\) convex. Neither projection needs to be
closed. For every feasible integral \(z\), the choice \(u=p(z)\) is
integral. Hence minimizing integer \(u\) in (5) is exactly equivalent to
minimizing \(p\) on the original mixed-integer set.

The compressed formula for \(Y\) in the unbounded feasibility proof has
quantifier block dimensions \(1,1,h+1\), and atomic polynomial degrees
and coefficient bit lengths polynomial in \(N\). Append the predicate
(4). It has no continuous variables and needs no new quantified variables;
only the free integer-coordinate count increases to \(k+1\). Its
coefficient sizes remain polynomial after (3).

Apply the optimization form of
[Khachiyan--Porkolab (2000), Theorem 1.1](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf)
directly to \(\widehat Y\), with \(u\) its last coordinate. Whenever
a finite optimum exists, the preceding discreteness argument establishes
the attainment hypothesis of that theorem. It gives an optimal integer pair
whose coordinates have polynomial bit length for fixed \(k,h\), independent
of the possibly large number of atoms in the compressed formula.
Consequently, for an effective absolute constant \(C\), the conservative
choice

\[
              B=2^{\lceil N^{C(h+1)(k+2)^4}\rceil}             \tag{6}
\]

satisfies

\[
  \|z^*\|_\infty\le B,\qquad |p(z^*)|\le B                 \tag{7}
\]

for some optimal assignment whenever the objective is finite. The constant
in (6) is fixed uniformly before deciding whether the instance has a finite
optimum. The extra \(+2\) is conservative; no sharp exponent is needed.

As in the feasibility proof, we use only the imported witness bound. Running
the general first-order optimization algorithm on the large compressed
formula would not establish a polynomial running time.

## 3. Rational SOC threshold queries preserve the span

The algorithm will query feasibility of \(p(z)\le t\) for integer
thresholds \(t\). An affine \(p\) adds only an affine row. For a
general convex quadratic, write

\[
          p(z)=z^TQz+a^Tz+c,\qquad Q\succeq0.
\]

Rational symmetric elimination gives

\[
                 z^TQz=\sum_{j=1}^r d_j\ell_j(z)^2,\qquad
                 d_j\in\mathbb Q_{>0},                       \tag{8}
\]

where each \(\ell_j\) is a rational homogeneous linear form and
\(r\le k\). All coefficients have polynomial bit length. This is
rational \(LDL^T\) factorization, not a factorization using square
roots. To see why zero pivots cause no problem, a zero diagonal entry in a
PSD matrix has a zero row and column, by its two-by-two principal minors.
Skip those entries; a positive pivot leaves a PSD Schur complement.
The resulting entries are ratios of input minors, giving the polynomial
coefficient bound.

For each summand introduce a **continuous** variable \(s_j\) and impose
the rational cone row

\[
       \|(2\ell_j(z),\ s_j-1/d_j)\|_2\le s_j+1/d_j.           \tag{9}
\]

Squaring and subtracting the right-hand square gives exactly

\[
                  4\ell_j(z)^2-4s_j/d_j.                     \tag{10}
\]

Since \(d_j>0\), (9) is equivalent to
\(s_j\ge d_j\ell_j(z)^2\): the latter inequality also implies the
nonnegative right side required by the cone. Together with

\[
                       \sum_j s_j+a^Tz+c\le t,                \tag{11}
\]

these rows are equivalent, after projecting out \(s\), to
\(p(z)\le t\). The forward lift can take equality in every
\(s_j=d_j\ell_j(z)^2\); the reverse direction follows by summing.

The expanded continuous tuple is \((x,s)\). Every new squared residual
(10) has **zero Hessian in \((x,s)\)**: its only quadratic terms involve
the integer coordinates. Every old squared Hessian is embedded by adding
zero rows and columns. Thus the continuous Hessian span remains exactly
\(h\). No integer variable is introduced in the actual threshold queries.
Their rational data have encoding length polynomial in \(N+\log(2+|t|)\).

This is the point that permits convex quadratic, rather than merely affine,
integer objectives. A generic conic epigraph reformulation should not be
assumed to preserve the span without checking its squared Hessians.

## 4. Exact algorithm

First decide original feasibility using the unbounded MISOCP theorem. If
infeasible, report that outcome. Otherwise construct \(B\) in (6), and
query

\[
                             p(z)\le -B-1.                    \tag{12}
\]

Use (9)--(11) when the objective has a nonzero quadratic part. If the
objective is unbounded below, (12) is feasible. If it is bounded below, its
integer-valued scale attains a minimum, and (7) puts that minimum at least
at \(-B\); then (12) is infeasible. Thus (12) classifies unboundedness
exactly. It does not inspect the boundedness of the continuous relaxation.

In the remaining finite case, maintain an infeasible lower threshold
\(a=-B-1\) and a feasible upper threshold \(b=B\). The latter is
feasible by (7). Query \(t=\lfloor(a+b)/2\rfloor\). If the query is
feasible replace \(b\) by \(t\); otherwise replace \(a\) by \(t\).
After \(O(\log B)\) calls the two integers are consecutive, and \(b\)
is the exact minimum of \(p\). A final feasible query at threshold \(b\)
returns an integer assignment \(z^*\). Its objective must equal \(b\),
since the preceding threshold \(b-1\) is infeasible. Return \(b/D\)
as the exact rational minimum of \(f\).

Every query has the original \(k,h\), and polynomial input length for
fixed parameters. The feasibility oracle returns an assignment with
polynomial bit length; alternatively (7) permits imposing the conservative
box \([-B,B]^k\) during the finite-case bisection. The unboundedness
query (12) must use the unbounded oracle and must not restrict the integer
variables to a box justified only for finite optima.

For an exact continuous optimizer, discard all temporary epigraph variables
and substitute the returned \(z^*\) into the **original** rational cone
system. Its continuous Hessian span is at most \(h\), its encoding length
is polynomial, and its fiber is nonempty. Apply the independently reviewed
continuous SOCP witness-recovery theorem. It returns an exactly feasible
algebraic vector \(x^*\) represented in one number field. Every point of
this fiber is optimal because the objective depends only on \(z\).
Thus recovery adds polynomial overhead for fixed parameters and establishes
the theorem's full output statement.

## 5. Scope, prior work, and significance

The epigraph and integer-threshold search are standard. Khachiyan--Porkolab
already optimizes the last integer coordinate over convex semialgebraic
sets and provides the optimal-point bound used here. Directly quantifying
every continuous coordinate in that result retains the continuous dimension
in its exponent. This note combines its optimal-point bound with the
Hessian-span projection and exact MISOCP feasibility results. Its additional
technical check is that a rational SOC representation of integer quadratic
thresholds preserves the continuous Hessian span. This is a supporting
capability of the preceding research, not a separate foundational advance.

The same discrete-objective argument was previously documented in this
repository for native convex quadratic constraints. The present feasible
class includes rational cone rows whose squared Hessians are indefinite.
Neither native PSD attainment nor a continuous-to-integer unboundedness
equivalence is used. The
[SOC boundary examples](socp-unboundedness-boundaries.md) show why those
properties cannot simply be transferred.

For instance, the rational rotated-cone system \(zt\ge1\),
\(z,t\ge0\), with integral \(z\) and continuous \(t\), has infimum
zero for the objective \(t\), but does not attain it. This does not
contradict the theorem because that objective contains a continuous
coordinate. The objective coefficients must also be rational: without a
common integer scale, the discrete-value argument no longer applies.

The capability established here is exact global optimization and
unboundedness classification for discrete quadratic costs over a broad
conic feasible region. This covers, for example, an objective that charges
only integer design or operating decisions while continuous variables
certify physical feasibility. The existence of a polynomial algorithm does
not establish useful precision bounds, competitive solver performance, or
an efficient implementation. Those remain separate questions.

## 6. Verification record

The primary Khachiyan--Porkolab text, printed pages 207--208, was read from
the repository PDF, including its exact optimal-point hypothesis and the
absence of atomic-predicate count from the witness bound. The proof checks
the distinction between this bound and the formula-dependent running time.
The rational cone identity and unchanged continuous Hessian span were
verified symbolically in the proof. A fresh reviewer independently
reconstructed the argument and then checked the saved manuscript. The review
found no gap in the optimal-pair bound, rational threshold lift, unboundedness
classification, exact search, or original-fiber witness recovery.

An inline `python -` command checked this note and the updated unbounded
feasibility note for existing local links, paired math delimiters, final
newlines, trailing whitespace, and control characters; it passed. These are
document checks, not proof verification. No numerical experiment, Lean
formalization, project-wide verification, or CI inspection is claimed.
