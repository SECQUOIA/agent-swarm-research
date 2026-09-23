# Independent review: rank-one parametric joint optimization

Date: 2026-09-05. Verdict: **PASS** for
[the rank-one observation](rank-one-parametric-linear-programs.md).
The auxiliary-variable elimination is elementary and source-qualified;
separate novelty is not asserted.

First reject an empty parameter interval. For a nonzero rational
rank-one matrix, a rational factorization `D=u*v^T` of polynomial
encoding length is obtained by taking a nonzero column and dividing
the other columns' entries by one nonzero entry of that column.
For fixed `x`, put `z=v^T*x`. The image of the nonempty parameter
interval under multiplication by `z` is exactly
`[lambda_lower*z,lambda_upper*z]` if `z>=0` and the reversed interval
if `z<=0`. At `z=0`, both branches force `w=0`.

Substituting `u*w` for the parameterized matrix term therefore gives
exactly the stated union of two rational polyhedra after eliminating
the parameter. Conversely, any point of either branch recovers a
legal parameter as `w/z` when `z!=0`; either endpoint works when
`z=0`. No division by zero or missing sign condition occurs. The
original fixed objective depends only on the retained `x`, so two
ordinary LPs determine feasibility and the joint optimum. An
unbounded branch objective implies an unbounded original objective
through the same pointwise reconstruction. Rank zero needs one LP.

If all original variables are bounded, then `z` and `w` are bounded
as well. A nonempty branch is compact and has an optimal rational
vertex. Standard rational LP bit bounds and the single ratio `w/z`
give polynomial binary encoding for a recovered optimum. A small
nonzero denominator does not invalidate this bit bound: numerator
and denominator already have polynomial binary length.

I directly inspected
[Boveroux, Carvalho, Lodi, and Louveaux](https://orbi.uliege.be/bitstream/2268/345162/1/OntheComplexityofLinearProgramswithparametricConstraintMatrices.pdf),
Sections 3.1 and 3.3. The latter treats one nonzero perturbation column;
the added coordinate `z` puts each sign branch in that setting.
The former's hardness construction has exactly two nonzero columns:
the fixed-one column has coefficients `+1,-1` in the two factor rows,
and the second-factor column has coefficient `+1` in the epigraph
row. Their supports are disjoint and both columns are nonzero, so
the perturbation rank is exactly two. This rank restriction is an
observation about the cited construction, not a new hardness reduction.

For its threshold version, every source variable except the epigraph
variable is already bounded by the displayed static constraints.
Adding the decision row `t<=K` bounds that remaining nonnegative
variable without changing the perturbation matrix or the yes/no
answer. The fixed-one-parameter bounded-fiber NP lemma therefore
applies to this restricted decision family. The large source integers
give ordinary hardness; no strong-hardness inference is justified.

The scope exclusions are necessary. A varying right-hand side adds
a parameterized fixed-one column before rank is measured. A direct
parameter term in the objective is not preserved by minimizing the
two fixed linear objectives here. True max-min bilevel optimization
does not permit choosing an arbitrary feasible inner point and is
not solved by this projection. I did not rely on the source's
separate max-min theorem for any conclusion in this audit.
