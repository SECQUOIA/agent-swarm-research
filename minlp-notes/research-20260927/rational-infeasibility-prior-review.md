# Review of rational infeasibility certificates for native convex quadratics

Date: 2026-09-27. This focused audit reviews the proposed rational strengthening
of [the algebraic certificate note](algebraic-primal-dual-certificates.md). It
supplements [the broader prior-art audit](algebraic-certificate-prior.md).

The positive-aggregate existence claim is correct and classical. Rationality
also follows from a short argument specific to positive semidefinite native
Hessians. A bound of `N^{O(h+1)}` does not follow from rational density alone,
but it follows from a quantitatively controlled rationalization of the existing
algebraic aggregate, conditional on that aggregate's stated degree and height
bounds. No inspected prior theorem supplied this precise Hessian-span bound.
That search result does not establish publication priority.

## 1. The alternative already exists, including unbounded domains

Jeyakumar and Li's Theorem 2.5 states that infeasibility of finitely many
SOS-convex polynomial inequalities is equivalent to a simplex-weighted aggregate
equal to a strictly positive constant plus a sum of squares. Convex quadratics
and affine functions satisfy its hypotheses. Consequently it supplies exactly
the real positive aggregate needed here, without Slater or compactness.
Their Corollary 2.7 addresses failure of strict feasibility instead, with a
nonnegative aggregate and no strictly positive constant. These are different
alternatives. [Primary manuscript, Theorem 2.5 and Corollary 2.7](https://web.maths.unsw.edu.au/~gyli/papers/jl-zero-sum-final-18-07-13.pdf).

There is also a direct attainment route. Include the affine rows among the
functions `q_i`, with zero Hessians, and minimize `t` subject to
`q_i(x) <= t` for every row. This problem is feasible. If the original system
is infeasible, its objective is bounded below by zero. Luo and Zhang's
Corollary 2 gives attainment for a feasible convex QCQP with finite infimum.
The attained value must then be strictly positive. Their Theorem 1 directly
rules out infeasible convex quadratic systems admitting arbitrarily small
nonnegative right-hand-side relaxations. The paper attributes the attainment
result to Terlaky's earlier work; that earlier paper was not inspected here.
[Primary manuscript, Theorem 1 and Corollary 2, printed pp. 2–7](https://papers.tinbergen.nl/97122.pdf).

Thus an unbounded sequence with `max_i q_i(x) -> 0` cannot be the missing
case in this native class. The epigraph has a strict point because `t` can
always be increased, so KKT produces a positive aggregate. If affine rows are
instead retained as a polyhedron, use relative Slater on that polyhedron.
An empty polyhedron is handled by linear Farkas.

The PSD requirement applies to each polynomial in its supplied variables.
An arbitrary SOC constraint squared into a quadratic can have an indefinite
Hessian, even though its original feasible region is convex. The native result
does not apply to such a polynomial merely because it came from an SOCP.

## 2. Rationality follows while preserving the support

Here is a complete qualitative argument. Treat affine rows as zero-Hessian
quadratics, and start with real nonnegative weights whose aggregate has
positive global minimum. Normalize all weights to sum to one. Let `I` be
their positive support and write

\[
 H(\lambda)=\sum_{i\in I}\lambda_iQ_i,\qquad
 b(\lambda)=\sum_{i\in I}\lambda_i a_i,\qquad
 c(\lambda)=\sum_{i\in I}\lambda_i c_i.
\]

For every choice of strictly positive weights on this support,

\[
 \ker H(\lambda)=\bigcap_{i\in I}\ker Q_i=:W.
\]

This follows because a sum of nonnegative quadratic forms vanishes precisely
when each positive summand vanishes. The subspace `W` is rational. Finiteness
of the aggregate's minimum requires `b(lambda)` to be orthogonal to `W`.
Consequently keep the exact rational linear equations

\[
 \sum_{i\in I}\lambda_i=1,\qquad b(\lambda)\perp W
\]

when approximating the weights. Their solution space is a rational affine
space; rational points are dense in it. The original weights lie in its
relatively open positive orthant. On that neighborhood, the restriction of
`H(lambda)` to `W`'s orthogonal complement is positive definite. Its inverse,
and therefore the aggregate's minimum, vary continuously. A sufficiently
close rational point in this affine space preserves both the support and
strict positivity of the minimum.

For those rational weights, `H z = -b` is a consistent rational linear
system, hence has a rational solution. Define

\[
 \gamma=c+\tfrac12 b^Tz>0.
\]

The exact identity

\[
 \sum_i\lambda_iq_i(x)
 =\tfrac12(x-z)^TH(x-z)+\gamma
\]

proves infeasibility. All entries and checks are rational. Positive
semidefiniteness of `H` follows from the input PSD matrices and nonnegative
weights; an exact verifier can also check it directly.

Unconstrained coordinate rounding is invalid: it can violate `b perp W`,
making the rounded aggregate unbounded below. The strictly positive margin
is also essential to this rounding argument. It does not automatically prove
rationality of a zero-margin aggregate used only to refute strict feasibility.

## 3. What the quantitative argument must retain

Suppose the existing algebraic aggregate has all entries in a degree-`D`
number field, with absolute logarithmic heights bounded by `B`, where
`D, B <= N^{O(h+1)}`. The following steps preserve that order.
If its Hessian is zero, the conditions are simply `b = 0` and `c > 0`,
and rational linear elimination and approximation suffice. Otherwise:

1. Normalize all positive weights together. Heights increase by a factor
   polynomial in `N`. Every positive weight and the positive aggregate
   minimum have size at least `exp(-poly(N,D,B))`, by the elementary lower
   bound for a nonzero algebraic number of bounded degree and height.
2. Compute a rational basis of `W` and a rational complement. Their entry
   lengths are polynomial in `N`. The matrix `S = sum_{i in I} Q_i` has
   the same kernel. Its positive restriction has a smallest eigenvalue at
   least `exp(-poly(N))`, by rational determinant and norm bounds.
3. On a neighborhood retaining at least half of each positive weight,
   `H(lambda)` is bounded below on the complement by a positive weight
   times the restriction of `S`. The inverse and minimum therefore have
   perturbation bounds of size `exp(poly(N,D,B))`.
4. Use rational Gaussian elimination to parametrize the exact normalization
   and kernel-orthogonality equations. Approximate its free coordinates to
   `poly(N,D,B)` binary places. The resulting rational weights preserve the
   positive support and positive minimum and have `poly(N,D,B)` bits.
5. Rational elimination for `H z = -b` adds only a polynomial factor to the
   bit length. The number of supplied entries is polynomial in `N`.

These are ordinary fixed-kernel matrix estimates; no new field extension or
repeated factor depending on `D` at every facial-reduction round is required.
The dependence `poly(N,D,B) = N^{O(h+1)}` is the relevant conclusion.
This is a proof route, not an implementation or an independent audit of the
earlier optimizer degree and height theorem.

The support is preserved, so an initial aggregate with at most `n+1` positive
weights retains that bound. There is no bound on support in terms of `h`
alone, as the identical-Hessian example in the main note already shows.

## 4. A general rational-point theorem is relevant prior art

Safey El Din and Zhi's Theorem 1.1 finds rational points in convex
semialgebraic sets in `k` variables. With polynomial degrees at most `d`
and coefficient bits at most `sigma`, its rational output coordinates have
length `sigma d^{O(k^3)}`. Its bit-operation bound is
`sigma^{O(1)}(s d)^{O(k^3)}` for `s` defining polynomials.
[Primary manuscript, Theorem 1.1, printed p. 3](https://arxiv.org/pdf/0910.2973).

To compare it with the present certificate, scale the positive aggregate to
have minimum at least one. Its multiplier set is the spectrahedron

\[
 \left\{\lambda\ge0:
 \begin{pmatrix}
 H(\lambda)/2&b(\lambda)/2\\
 b(\lambda)^T/2&c(\lambda)-1
 \end{pmatrix}\succeq0\right\}.
\]

The rationality proof above makes this set rationally nonempty. Characteristic
polynomial coefficients express its PSD condition with polynomial degrees at
most `n+1`. The general rational-point theorem therefore gives a polynomial
bit bound when the total number of multiplier variables is fixed.

That parameter is not Hessian-span dimension. Many rows can share one
Hessian. Even after replacing weights by aggregate coefficients, the linear
term and constant leave up to `h+n+1` variables. The inspected theorem thus
does not directly yield a bound polynomial in `N` for fixed `h` alone.
The same distinction applies to fixed-number-of-quadratics results.

The defensible contribution is the parameter-sensitive rational encoding
corollary and its simple rational verifier. The positive aggregate, the use
of exact certificates, and rational approximation in a rational affine
space are established mechanisms. No stronger novelty conclusion is supported
by this audit.

## 5. Dependence on the span parameter is necessary for this format

The following elementary lower bound was derived during the parallel review;
it is not asserted as a new result in the literature. For `n >= 2`, consider

\[
 q_0=\tfrac12-x_1\le0,\qquad
 q_i=x_i^2-x_{i+1}\le0\quad(1\le i<n),\qquad
 q_n=x_n\le0.
\]

The system is infeasible, every Hessian is PSD, and `h = n-1`. Suppose
`sum_i lambda_i q_i` is globally strictly positive with nonnegative rational
weights. Evaluation at zero gives `lambda_0 > 0`. Put `d = 2^{n-1}` and
evaluate at `x_i = t^{2^{i-1}}`. All intermediate rows vanish, giving

\[
 \lambda_0(\tfrac12-t)+\lambda_n t^d>0.
\]

At `t = (1+1/d)/2`, this implies

\[
 \frac{\lambda_n}{\lambda_0}
 >\frac{2^{d-1}}{d(1+1/d)^d}
 >\frac{2^{d-1}}{3d}.
\]

The binary encoding of the two rational weights must therefore have
`Omega(d) = Omega(2^n)` bits in total. Common rescaling cannot hide this
ratio. The family has input length polynomial in `n`, so an unrestricted
polynomial bit bound is false for this certificate format. This does not
give a lower bound for other proof formats or contradict the proposed
fixed-`h` bound.

## 6. Verification record

This review used direct inspection of the three primary manuscripts linked
above, independent symbolic reasoning, and a parallel source search for native
rational quadratic certificates. A targeted `python -` command passed checks
for the new file's final newline, trailing whitespace, paired display-math
delimiters, and local links. The same command used `fractions.Fraction` to
check the chain evaluation and ratio bound exactly for `n=2,...,9`; the
symbolic argument above covers every `n >= 2`. No project-wide checks were
run and no CI status or logs were inspected.
