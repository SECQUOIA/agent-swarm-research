# Independent review of the five-variable Horn witness and minor obstruction

Date: 25 September 2026.

Both claims pass this review, subject to the scope qualifications below.
The later three-variable counterexample is stronger as a counterexample to
the disjoint-multiplier relaxation; see
[its independent review](three-positive-disjoint-counterexample-review.md).

## Five-variable witness

Let `H` have diagonal entries one, entries `-1` on the edges of a five-cycle,
and entries `+1` on its other off-diagonal positions. For nonnegative `x`,

\[
x^THx=\left(\sum_i x_i\right)^2-4\sum_{ij\in E(C_5)}x_ix_j\ge0.
\]

One elementary proof of the inequality fixes the sum of coordinates and
maximizes the edge sum. If two nonadjacent vertices have positive weight,
move all their combined weight onto whichever has the larger weighted
neighbor sum; this does not decrease the edge sum and reduces support.
Repeat until the support is a clique. The five-cycle is triangle-free,
so the remaining support has at most two vertices, and its product is at
most one quarter of the squared total weight. This proves the required
inequality without a numerical copositivity test. Zero is attained on the
cube, including at the origin.

With `epsilon=10^-6`, the proposed moments are

\[
y_S=\epsilon^{|S|}\alpha_S,
\]

where `alpha_empty=1`, singletons have coefficient `1/10`, cycle edges
have coefficient `13/20`, other pairs have coefficient `1/10`, and larger
sets have coefficient one. A monomial with one squared coordinate has
moment `epsilon^degree` if it is just that square, and
`40 epsilon^degree` otherwise. There are 112 moments including the fixed
constant, hence 111 free coordinates.

The exact objective is

\[
\epsilon^2[5-2(5)(13/20)+2(5)(1/10)]
=-\epsilon^2/2=-1/(2\cdot10^{12}).
\]

For a disjoint multiplier, let `I` be its coordinates fixed to an
`x_i` factor and `J` its coordinates fixed to a `1-x_j` factor. Scale the
affine moment matrix by `diag(1,epsilon^-1,...)` and divide by
`epsilon^|I|`. The resulting matrix is

\[
A_I+\sum_{\varnothing\ne T\subseteq J}(-\epsilon)^{|T|}A_{I\cup T}.
\]

Every leading matrix `A_I` has smallest eigenvalue greater than `1/100`.
For `I` empty, it is a principal submatrix of the full six-dimensional
matrix. The smallest eigenvalue of that full matrix is

\[
\frac{25-11\sqrt5}{40}>\frac1{100}.
\]

Indeed, the four nonconstant cycle modes give the eigenvalues of
`(9/10)I+(11/20)A(C_5)`, while the constant mode and the intercept form a
two-dimensional block with diagonal entries `1,5/2` and off-diagonal
entry `sqrt(5)/10`, whose minimum eigenvalue is much larger.

For `I` nonempty, the lower block is `39I+11^T` and the top-left entry is
at least `1/10`. After subtracting `(1/100)I`, the lower block is at least
`(3899/100)I`. If `|I|=1`, the squared norm of the off-diagonal vector is
at most `4(13/20)^2=169/100`. If `|I|>=2`, it is at most three. In both
cases the Schur complement is strictly positive, proving the same bound.

Every entry of every `A_I` has absolute value at most 40. The perturbation
therefore has spectral norm at most

\[
240[(1+\epsilon)^5-1]<0.00144<0.01.
\]

This proves strict feasibility of all 243 matrices analytically. The bound
actually evaluates to approximately `0.0012000024`.

Two targeted commands were run:

```text
python /tmp/threeplus/horn_check.py
python research-20260925/verify_horn_disjoint_review.py
```

The first passed all 243 exact Sylvester checks. The independent second
checker uses `Fraction` symmetric elimination, checks all 243 actual
matrices and all 243 leading matrices shifted by `-(1/100)I`, and checks
the perturbation and objective arithmetic. Its smallest actual LDL pivot
was `49/1964`. No project-wide or CI checks were run.

The matrices match the full system in Theorem 3, equation (17), of
[Khajavirad's v2 paper](https://arxiv.org/html/2601.18545v2#S3), with all five
vertices in `P` and `M` empty. This five-positive witness alone says
nothing about the three-positive open case. No claim of novelty is made
for the Horn matrix or its copositivity.

## Graph-minor obstruction

Use the source definition of `QP(G)`: node variables lie in `[0,1]`, edge
coordinates equal products, plus-loop coordinates are at least the
corresponding square, and minus-loop coordinates are at most the square,
before taking the convex hull. Assume the graph induced by plus-loop
vertices contains a `K_5` minor. Choose five disjoint connected branch
sets `C_a`, a spanning tree in each nonsingleton branch, representatives
`r_a`, and one graph edge `e_ab` between each pair of branches.

The affine functional

\[
F=\sum_{ij\text{ in the chosen trees}}(Y_{ii}+Y_{jj}-2Y_{ij})
\]

is nonnegative on `QP(G)`. On a generating point, write
`Y_ii=x_i^2+delta_i` at plus vertices, with `delta_i>=0`. Each summand is
`(x_i-x_j)^2+delta_i+delta_j`. Thus on `F=0`, each branch has a common
coordinate `t_a`, and every loop slack in a nonsingleton branch vanishes.
The same statements hold atom by atom in any convex representation of a
point of this face: a finite sum of nonnegative quantities can vanish
only when every positive-weight summand vanishes.

On this first face, impose the additional affine equality `L=0`, where

\[
L=1-2\sum_a x_{r_a}+\sum_a Y_{r_ar_a}
    +2\sum_{a<b}Y_{e_{ab}}.
\]

On each remaining generator,

\[
L=(1-\sum_a t_a)^2+\sum_a\delta_{r_a}\ge0.
\]

This proves the needed validity on the first face. It also settles the
singleton issue: a singleton branch's slack may survive `F=0`, but is
killed by `L=0`. It is unnecessary to assert that `L` is valid on the
whole original hull or that the second face is exposed there.

Project the final section to the symmetric five-by-five matrix whose
diagonal entries are `Y_rara` and whose off-diagonal entries are
`Y_eab`. Every projected atom is `tt^T` with `t>=0` and `sum t=1`.
Conversely, every such `t` extends to a source generator: use `t_a` on
branch `C_a`, set outside coordinates to zero, use exact products on all
edges, and use exact squares on every loop. Therefore the projection is
exactly

\[
B=\operatorname{conv}\{tt^T:t\ge0,\ \mathbf1^Tt=1\}
 =\{X\in\mathrm{CP}_5:\mathbf1^TX\mathbf1=1\}.
\]

The second equality follows by normalizing each nonzero nonnegative
vector in a completely positive decomposition; the normalized weights
are its squared coordinate sums. In particular, `B` is compact and its
conic hull is `CP_5`.

If `B` had a finite semidefinite lift, homogenize that lift with a
nonnegative scalar `lambda`. Positive `lambda` gives exactly positive
scalings of `B`. A lifted feasible direction with `lambda=0` and nonzero
visible coordinate would, when added repeatedly to any feasible lift at
`lambda=1`, make `B` unbounded. Compactness excludes this. Thus
homogenization represents exactly `cone(B)=CP_5`, with no extra visible
directions at zero scale.

[Bodirsky, Kummer, and Thom, *Spectrahedral shadows and completely
positive maps on real closed fields*](https://ems.press/content/serial-article-files/52505)
prove that the copositive cone of order at least five is not a
spectrahedral shadow in Corollary 3.18. Their Remark 3.17 records the
equivalence of this property for a closed convex cone and its dual.
Applying this to the dual pair of copositive and completely positive
cones rules out an SDP lift of `CP_5`, hence of `B`. Affine sections and
projections preserve spectrahedral shadows, so the original `QP(G)`
cannot have a finite SDP lift.

This proof permits arbitrary extra vertices, edges, and minus loops. The
branch sets must lie in the plus-induced graph; replacing that hypothesis
by a minor in the full graph is unsupported. The theorem is a sufficient
obstruction, with no converse for `K_5`-minor-free graphs. It rules out an
exact finite lift of the whole hull; it does not rule out useful SDP
approximations or exact treatment of particular objectives.

## Literature and novelty limits of this review

The two primary sources linked above were inspected directly, including
the precise LMI definition and the copositive/dual-cone obstruction.
Searches for sparse copositive spectrahedral cones, quadratic `K_5`
spectrahedral shadows, and completely positive graph-minor
representability did not locate an equivalent graph theorem. Those
unsuccessful searches do not establish novelty. The minor reduction is
an application of a known nonrepresentability theorem; any claim that
this graph formulation is new still requires a dedicated literature
audit.
