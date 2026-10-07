# Precedent and limits for direct aggregation cuts

Reviewed 2026-10-03. This note audits the mathematical inference proposed for
the second convexification study. It does not claim that constraint
aggregation, Lagrangian cuts, joint support, or bound-corrected floating-point
rows are new.

## The inference and its assumptions

Suppose the original constraints include

\[
g_i(x)+\ell_i(z)\le b_i,\qquad i=1,\ldots,m,
\]

where each \(\ell_i\) is affine. Let \(D\) contain every feasible value of
\(x\), including the required expression domains. For a fixed \(a\) and
fixed \(\lambda\ge0\), suppose a certified global lower bound gives

\[
a^Tx+\sum_i\lambda_i g_i(x)\ge\beta\quad(x\in D).
\tag{1}
\]

Then the original variables satisfy the linear inequality

\[
a^Tx-\sum_i\lambda_i\ell_i(z)
\ge\beta-\sum_i\lambda_i b_i.
\tag{2}
\]

Indeed, the defining rows imply
\(\sum_i\lambda_i g_i(x)\le\sum_i\lambda_i b_i-
\sum_i\lambda_i\ell_i(z)\). Substitution in (1) proves (2). A lower
bound suffices; an exact minimum is unnecessary for validity. No convexity,
constraint qualification, or optimality of the chosen multipliers is needed.
Equality rows may use signed multipliers; inequality rows may not, unless
their direction is also changed. Constants in the affine functions must be
collected into the final right-hand side exactly.

This is ordinary weak Lagrangian duality applied to the objective
\(a^Tx-\sum_i\lambda_i\ell_i(z)\): its Lagrangian, using these same
multipliers, is \(a^Tx+\sum_i\lambda_i g_i(x)-\sum_i\lambda_i b_i\).
The derivation is valid for nonconvex problems. The author's edition of
[Boyd and Vandenberghe, *Convex Optimization*, §§5.1.2–5.1.3 and 5.2.2,
pp. 216–217 and 225](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)
states this lower-bound principle and explicitly distinguishes weak from
strong duality. The formula above is our specialization of that principle.

Keeping the original nonlinear constraints and adding (2) avoids introducing
new graph equalities merely to express this cut. That is an implementation
choice. It gives no general runtime or relaxation-dominance theorem relative
to native SCIP.

## Closest primary precedents

| Source | What it establishes or implements | Implication for this work |
|---|---|---|
| [Dey, Muñoz, and Serrano (2022), *On Obtaining the Convex Hull of Quadratic Inequalities via Aggregations*, SIAM J. Optim. 32(2), 659–686](https://doi.org/10.1137/21M1428583); [author manuscript](https://www2.isye.gatech.edu/~sdey30/AggQuadratics.pdf) | Nonnegative aggregation is a classical source of valid inequalities. Hull descriptions for three quadratics need additional hypotheses; their counterexamples prohibit an unconditional extension. | Do not present the aggregation principle as new or infer a complete hull from the validity of individual cuts. Their aggregation hull results differ from the bounded support subproblem in (1). |
| [Blekherman, Dey, and Sun (2024), *Aggregations of Quadratic Inequalities and Hidden Hyperplane Convexity*, SIAM J. Optim. 34(1), 98–126](https://doi.org/10.1137/22M1528215) | Gives structural conditions under which selected quadratic aggregations describe a convex hull, including results addressing closed inequalities. | There is substantial prior hull theory beyond the elementary multiplier inference. Its hypotheses cannot be omitted when citing completeness. |
| [Gleixner, Berthold, Müller, and Weltge (2017), *Three Enhancements for Optimization-Based Bound Tightening*](https://doi.org/10.1007/s10898-016-0450-4); [author manuscript, §2, Theorem 1 and Remark 3](https://optimization-online.org/wp-content/uploads/2016/03/5356.pdf) | Derives Lagrangian variable bounds from LP dual multipliers and propagates them in SCIP. These rows are redundant for the generating LP; their purpose is inexpensive propagation. | Obtaining a linear original-variable inequality by aggregation is established solver practice. Our prospective extra strength must come from certified joint optimization of original nonlinear functions, beyond merely aggregating the existing LP. |
| [Misener and Floudas (2012), *Global optimization of mixed-integer quadratically-constrained quadratic programs (MIQCQP) through piecewise-linear and edge-concave relaxations*](https://doi.org/10.1007/s10107-012-0555-6); [author's project description](https://wp.doc.ic.ac.uk/rmisener/project/global-optimisation-of-mixed-integer-nonlinear-programs/) | Integrates convexification of small groups of quadratic terms, including edge-concave aggregations, into global optimization. | Grouping terms before constructing affine estimators is also established. This term grouping should be distinguished from nonnegative aggregation of separate model rows. |
| [Garloff and Smith (2008), *Rigorous Affine Lower Bound Functions for Multivariate Polynomials and Their Use in Global Optimisation*, §5](https://d-nb.info/1097267482/34) | Uses interval Bernstein coefficients and a validated adjustment to obtain affine lower bounds despite roundoff and coefficient uncertainty. | Numerical proposals followed by rigorous affine-bound validation have direct precedent. The present certificate format and supported oracles must carry the implementation claims. |
| [Cook, Dash, Fukasawa, and Goycoolea (2009), *Numerically Safe Gomory Mixed-Integer Cuts*, INFORMS J. Comput. 21(4), 641–649](https://doi.org/10.1287/ijoc.1090.0324) | Generates provably valid cuts using floating-point arithmetic with controlled rounding. | Floating-point output can be mathematically valid, but a heuristic tolerance shift is not a substitute for an error bound. |
| [Eifler and Gleixner (2024), *Safe and Verified Gomory Mixed-Integer Cuts in a Rational Mixed-Integer Program Framework*](https://doi.org/10.1137/23M156046X); [arXiv:2303.12365v2, §§2.2–2.3 and 2.5, Lemmas 1 and 3, Corollary 2](https://arxiv.org/html/2303.12365v2) | Safely approximates rational rows, aggregates them with approximate multipliers, and scales them using bound-dependent corrections. Gives verification certificates for the resulting cuts. | Correcting the final rounded row using variable bounds is an established technique, including after scaling and back-substitution. |

The reviewed scope is the specific cited theorem, section, or abstract/project
description, not an exhaustive priority search over every implementation.
The Misener–Floudas comparison uses the publication abstract and the author's
description; no finer equivalence of algorithms is asserted.

## Correcting the final machine row

After all exact aggregation and collection, write the proved row as
\(c^Tw\ge d\). Here \(w\) lists unique original variables; entries of
\(x\) and \(z\) that refer to the same variable must be combined. Suppose
the actual exported coefficients are the finite binary64 values
\(\widehat c\). Treat those values as exact dyadic rationals and set
\(\delta_j=\widehat c_j-c_j\).

For valid bounds \(L_j\le w_j\le U_j\), define

\[
\eta=\sum_j\inf_{t\in[L_j,U_j]}\delta_jt
=\sum_j
\begin{cases}
\delta_jL_j,&\delta_j>0,\\
\delta_jU_j,&\delta_j<0,\\
0,&\delta_j=0.
\end{cases}
\]

Whenever these lower bounds are finite, the machine row

\[
\widehat c^Tw\ge\operatorname{roundDown}_{64}(d+\eta)
\tag{3}
\]

is valid. This follows immediately from
\(\widehat c^Tw=c^Tw+\delta^Tw\ge d+\eta\). The formula is the
greater-than-or-equal version of the bound-correction principle in the safe
cut literature above. Two finite bounds are sufficient but unnecessary:
positive \(\delta_j\) needs only a finite lower bound, negative
\(\delta_j\) only a finite upper bound, and zero needs neither. If the
needed bound is infinite, choose a different representable coefficient that
makes the correction finite, or reject the row. Multiplying zero by an
infinite floating-point bound must not enter the arithmetic.

All sums and coefficient differences in this argument must be exact or
rigorously enclosed in the required direction. Rounding the right-hand side
down by a fixed epsilon does not establish (3). Any subsequent coefficient
normalization, sparsification, aggregation, or substitution needs its own
correction. Solver feasibility tolerances and the solver's later presolve/LP
arithmetic remain outside a certificate for this submitted row alone.

## Completeness fails even with every exact support direction

The following elementary example is derived here to clarify the scope. It is
not a priority claim.

Let \(x\in[0,1]\), with the two original rows

\[
x^2\le\tfrac14,\qquad -x^2\le-\tfrac14.
\]

The feasible set is \(\{1/2\}\). Nevertheless, \(\bar x=1/4\)
satisfies every cut (2) produced over the unchanged box, for every
\(a\in\mathbb R\) and every \(\lambda_1,\lambda_2\ge0\), even
when (1) uses its exact minimum.

To prove this, put probability \(3/4\) at zero and \(1/4\) at one.
Then \(\mathbb E[X]=\mathbb E[X^2]=1/4\), so

\[
\beta=\inf_{x\in[0,1]}
\{ax+(\lambda_1-\lambda_2)x^2\}
\le\tfrac14a+\tfrac14(\lambda_1-\lambda_2).
\]

Since the proposed row is
\(ax\ge\beta-(\lambda_1-\lambda_2)/4\), it holds at
\(\bar x=1/4\). Thus even exhaustive direction search can leave a strict
gap to the convex hull of the original feasible set. Strengthening the
support domain using the constraints, or reasoning jointly about the
constrained feasible set, is a separate operation. Native domain propagation
may resolve this particular example; it does not change the stated limit of
the cut family on the unchanged box.

## Checks needed in an implementation or certificate

- Bind the certificate to original row identifiers, inequality sides,
  constants, variable identifiers, and the exact expression semantics used
  by the loaded model. Algebraic simplification must preserve domains.
- Certify the support for the chosen multipliers and coefficients, after
  their numerical selection. An approximate optimizer or LP dual vector is
  a proposal, not a lower-bound certificate.
- Use nonnegative multipliers for consistently oriented inequality rows.
  Do not discard unmatched nonlinear remainders when extracting a block.
- Record the support domain and all bounds used in (3). Bounds valid only
  below a search node yield a local cut; incumbent objective cutoffs can
  restrict validity to improving solutions and must be identified as such.
- Replay the collected and rounded original-variable row, not only the
  earlier nonlinear support inequality. Keep equality of row coefficients
  separate from approximate feasibility checks at sampled points.
- Report a bounded direction search as such. Failure to find a cut is not
  hull membership; exhaustive directions for this family do not in general
  recover the feasible-set hull either.

The defensible contribution statement is therefore an implemented,
model-bound, replayable combination of established aggregation and support
principles, with measured solver effects and explicitly stated oracle
classes. Broader novelty or universal solver benefit requires separate
evidence.
