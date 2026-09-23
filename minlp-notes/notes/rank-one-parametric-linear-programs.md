# A source-qualified rank-one parametric LP observation

Date: 2026-09-05. Status: supporting observation; the
[independent written audit](review-rank-one-parametric-linear-programs.md)
passes. The main elimination is a standard auxiliary-
variable reformulation, and separate novelty is unclaimed.

Consider

```
minimize c*x
subject to A*x + lambda*D*x <= b,
           x in X,
           lambda_lower <= lambda <= lambda_upper,
```

where all data are rational, `X` is a rational polyhedron, and the finite
parameter interval is given. Reject an empty interval before applying
the two-branch construction. The parameter occurs only through the
coefficient matrix. The right-hand side, the polyhedron `X`, and the
objective are independent of it.

## Rank one: two ordinary LPs

If `D=u*v^T`, introduce `z=v^T*x` and `w=lambda*z`. The projected
feasible set in `(x,z,w)` is exactly the union of two rational polyhedra:

```
A*x+u*w <= b, x in X, z=v^T*x,
z>=0, lambda_lower*z <= w <= lambda_upper*z;
```

and

```
A*x+u*w <= b, x in X, z=v^T*x,
z<=0, lambda_upper*z <= w <= lambda_lower*z.
```

For `z!=0`, reconstruct `lambda=w/z`; either pair of inequalities
places it in the required interval. For `z=0`, both force `w=0`, and
any parameter in the interval works. Thus feasibility and the joint
minimum of the fixed objective are obtained by solving two LPs. The
rank-zero case is already an LP.

When the feasible flow variables are bounded, an optimum is attained
whenever the system is nonempty. An optimal rational LP vertex and the
ratio above give a rational optimum of the original model with polynomial
binary encoding. More generally the two LPs detect infeasibility or an
unbounded objective directly.

This extends the one-nonzero-column case in Boveroux, Carvalho, Lodi and
Louveaux,
[*On the Complexity of Linear Programs with Parametric Constraint Matrices*](https://orbi.uliege.be/bitstream/2268/345162/1/OntheComplexityofLinearProgramswithparametricConstraintMatrices.pdf),
Section 3.3, PDF pages 10–11. Indeed, introducing `z` creates precisely
one parameter-dependent column; splitting its sign reduces to their
nonnegative-variable setting. It should not be presented as a new broad
parametric-programming technique.

## Rank two already contains the source hardness construction

The same manuscript's Section 3.1 encodes Matsui's positive product using
an auxiliary variable `s=1`, a parameter representing its first factor,
two opposing rows enforcing that factor through `lambda*s`, and one
product epigraph row containing `lambda*z_2`. The perturbation matrix
has two nonzero columns, one on `s` and one on `z_2`, with linearly
independent supports. Its rank is exactly two.

Therefore the cited reduction already proves ordinary NP-hardness of
the joint minimum at perturbation rank two. This is a restriction of
that source theorem, not a new reduction. The source's large binary
coefficients do not justify strong hardness. With explicit finite bounds
on the flow variables and a rational objective threshold, membership
in NP follows from the repository's fixed-parameter linear-fiber lemma.

## Scope that must not be dropped

A parameter-dependent right-hand side must be represented by an extra
fixed-one variable before measuring rank: the effective perturbation
matrix is then the augmented matrix containing that right-hand-side
column. Its rank may exceed the rank of the original matrix `D`.
A direct parameter term in the objective is likewise not handled by
the two linear objectives above. No claim here extends the formula
unchanged to either setting, or to a true bilevel max-min objective.
