# Independent review of integer-only objectives over unbounded MISOCP

Date: 2026-09-28. Scope: the [exact optimization reduction](integer-objective-misocp.md)
for a rational convex quadratic objective depending only on the integer
variables of a rational mixed-integer second-order cone system. The reviewer did not
develop this extension. The already reviewed
[unbounded MISOCP feasibility theorem](unbounded-misocp-frontier.md) and its
compressed projection formula are treated as dependencies.

**Finding.** No gap was found in the saved manuscript. For fixed integer dimension
\(k\) and squared continuous Hessian span \(h\), it gives exact
polynomial-time optimization, including infeasibility and unboundedness
classification, and returns an optimal integer assignment and rational
objective value in the finite case. The reviewer first reconstructed the
reduction from its stated claims, then checked the complete saved manuscript,
including its additional exact continuous-point output.

## 1. Integer values supply attainment

Let \(q(z)\) be the rational objective, and let \(L>0\) clear
the denominators of its actual polynomial coefficients, including its
constant term. The product of the displayed denominators suffices and has
polynomial bit length. Then \(p=Lq\) has integer coefficients.
The values \(p(z)\) at feasible integer assignments form a subset
of \(\mathbb Z\). If this set is nonempty and bounded below, it
has an achieved least element. This argument does not require the real
integer-coordinate projection to be closed, the continuous fibers to be
bounded, or continuous optimization to attain its infimum.

For the real projection \(Y\) of the original conic feasible set,
consider

\[
 E=\{(z,u):z\in Y,\ p(z)\le u\}.
\]

The set \(Y\) is convex, and \(p\) is convex, so \(E\)
is convex. With \(z,u\) integral, its minimum last coordinate is
exactly the minimum of \(p\); every optimal pair has
\(u=p(z)\). Replacing this epigraph inequality by an equality
would generally destroy convexity and is not part of the argument.

## 2. The imported size theorem bounds an optimum

The reviewer checked the primary
[Khachiyan--Porkolab paper](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
printed pages 207--208, both in the local full text and the openly accessible
PDF. Theorem 1.1 bounds an optimal integer point for minimization of the last
coordinate of a convex set specified by a Boolean first-order formula.
Its bound depends on atomic degree and coefficient bit length, free dimension,
and quantified block dimensions; it does not depend on the number of atomic
predicates. Closedness and full dimension are not assumptions.

Append the polynomial predicate \(p(z)\le u\) to the compressed
formula for \(Y\). It adds one free coordinate and no quantified
variables. The block sizes remain \(1,1,h+1\), and atomic degrees
and individual coefficient lengths remain polynomial in the full input
length \(N\), including the objective. Theorem 1.1 therefore gives
an effective bound

\[
 B=2^{N^{C(h+1)(k+2)^4}}
\]

for a sufficiently large absolute constant \(C\), such that some
optimal pair has all coordinates of absolute value at most \(B\)
whenever the optimum is finite. In particular, its last coordinate lies
in \([-B,B]\). This uses the theorem's *optimal-point* statement;
a bound merely on some feasible epigraph point would not justify the
lower bound on the optimum.

The large Boolean formula is used only to prove this uniform bound. Applying
the paper's running-time theorem directly to that formula would introduce
its potentially exponential size and is not needed here.

## 3. A threshold has a rational conic encoding preserving the span

Rational symmetric elimination of the PSD quadratic coefficient matrix gives

\[
 p(z)=\sum_{j=1}^r d_j\ell_j(z)^2+a^Tz+c,
 \qquad d_j>0,
\]

where \(r\le k\), and all \(d_j\), homogeneous linear forms
\(\ell_j\), and affine coefficients are rational with polynomial
bit length. Singular PSD matrices cause no obstruction: a zero diagonal
in a PSD residual matrix has a zero row and column, which can be omitted.
The nonzero pivots and elimination coefficients are ratios of minors, so
the usual determinant bounds control their encoding lengths. No irrational
square root of \(d_j\) is required.

Introduce continuous variables \(s_j\). The proposed cone row is
equivalent to the intended epigraph:

\[
 \|(2\ell_j(z),s_j-1/d_j)\|_2\le s_j+1/d_j
 \quad\Longleftrightarrow\quad
 s_j\ge d_j\ell_j(z)^2.
\]

Indeed, the squared residual is exactly

\[
 4\ell_j(z)^2-4s_j/d_j.
\]

The forward implication follows by squaring the cone inequality. Conversely,
the right side implies \(s_j\ge0\), hence the cone's right-hand
side is positive; the squared inequality then implies the unsquared one.
Thus no spurious branch is introduced by a negative cone right-hand side.
Adding

\[
                 \sum_j s_j+a^Tz+c\le t
\]

is exactly equivalent, after projecting out the \(s_j\), to
\(p(z)\le t\). For the reverse projection choose
\(s_j=d_j\ell_j(z)^2\). The affine-objective case \(r=0\)
requires only the final affine row.

Each added squared residual is affine in all continuous variables
\((x,s)\), so its continuous Hessian is zero. Original continuous
Hessians acquire only zero rows and columns. Their span therefore remains
exactly \(h\), and the number of integer variables remains \(k\).
The number of additional continuous variables and rational encoding length
are polynomial. Convexity also follows directly from the norm formulation.

## 4. Classification and exact search

First decide original feasibility. On a nonempty instance, query the
threshold \(p(z)\le-B-1\). If the objective is unbounded below,
this query is feasible. If it is bounded below, discrete attainment and the
optimal-point bound make the query infeasible. Thus this single query
classifies unboundedness correctly.

In the finite case, \(-B-1\) is an infeasible threshold and \(B\)
is a feasible threshold. Integer bisection maintains these endpoint
properties and terminates at consecutive thresholds in \(O(\log B)\)
queries. Each threshold has polynomial bit length for fixed \(k,h\),
and the cone encoding above allows the unbounded MISOCP feasibility algorithm
to answer each query with the same parameters. A returned assignment at the
least feasible threshold must attain that threshold, since \(p(z)\)
is integral. Dividing by \(L\) gives the exact rational optimum.

The auxiliary integer epigraph coordinate is used for the existence bound
only. It is not introduced in the algorithm's threshold queries. No sharp
overall running-time exponent follows just from the displayed bound on
\(B\); composition with the feasibility algorithm must also be counted.
Polynomial time for fixed parameters does follow.

## 5. Output and contribution boundaries

The feasibility oracle returns an integer assignment with a nonempty
original continuous fiber. Its rational MILP output in the continuous
coordinates need not itself be conically feasible. The optimization
reduction alone therefore promises an optimal integer assignment and exact
value. An exact continuous optimal point can additionally be recovered by
substituting that assignment into the original system and applying the
separately reviewed [SOCP witness recovery theorem](socp-exact-witness-recovery.md).
Substitution preserves the continuous Hessian span, and its coefficient
length is polynomial for fixed parameters. Any feasible point of that fiber
is optimal because the objective depends only on \(z\). This full-point
output depends on the recovery theorem and should be identified as such.

There is no claim here for objectives involving continuous variables.
For example, minimizing \(x\) subject to \(x,y\ge0\) and
\(xy\ge1\) is a rational SOCP with finite unattained infimum.
The discrete-value argument is unavailable in that setting.

The integer epigraph, rational rotated-cone identity, and discrete bisection
are established reductions. Khachiyan--Porkolab already treats convex
polynomial integer optimization when the relevant total formula dimensions
are fixed. The contribution of this corollary is inherited from the
compressed projection and unbounded MISOCP feasibility results that permit
unrestricted continuous dimension. This review does not establish novelty
of that underlying package or a separate novelty claim for the corollary.

## 6. Verification record

The verification consists of an independent proof reconstruction, direct
checking of the exact cone identity and PSD decomposition boundary,
inspection of the primary integer size-bound theorem, and comparison with
the saved manuscript. Its optional finite-case restriction to
\([-B,B]^k\) is valid because an optimum remains in that box; the
negative-threshold query for unboundedness correctly retains the unbounded
integer domain. The full continuous-point output properly identifies its
separate recovery dependency.

An inline `python -` document check passed final-newline,
trailing-whitespace, control-character, paired-math-delimiter, and all
three local-link checks for this review. These are document checks, not
proof verification. No numerical experiment, Lean proof, project-wide
verification, or CI inspection was used.
