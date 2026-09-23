# Source audit: degree-independent integer count for positive pure powers

Date: 2026-09-05. Bounded primary-source assessment of
[the finite pure-power candidate](pure-power-degree-independent-integer-count.md).
Mathematical verification is assigned separately.

No matching theorem was found characterizing the minimum integer count over
all convex lifts of the whole graph, with an additive `O(r)` error uniform in
the coordinate degrees. The useful distinction is this universal comparison.
Adaptive interpolation of powers, logarithmic encodings of disjunctions,
and the midpoint parity obstruction all have established antecedents.

## Scope that the finite theorem actually establishes

There is one exponent `D_i` per coordinate, shared across all outputs;
coefficients are nonnegative and the output error body is unconditional.
The allocation depends on the coefficient matrix and error body, but not
the degrees. The power change of variables maps the entire cube onto itself,
so its use in the contact-set lower bound does not pay a Jacobian-volume
penalty. The resulting finite comparison applies even against convex lifts
with unrestricted integer coordinates.

The upper bound in this note allows real coefficients and a number of rows
exponential in the accuracy encoding. It is not a polynomial-size rational
algorithm. The separate compact reciprocal-interpolation investigation may
change this limitation, but it is not part of the theorem audited here.
Multiple distinct powers of the same coordinate do not automatically admit
the common transform used in this lower bound.

## Closest interpolation sources

Rote's [1992 Sandwich-algorithm paper](https://page.mi.fu-berlin.de/rote/Papers/pdf/The%2Bconvergence%2Brate%2Bof%2Bthe%2BSandwich%2Balgorithm%2Bfor%2Bapproximating%2Bconvex%2Bfunctions.pdf)
studies chord upper approximations and tangent lower approximations, with
several adaptive refinement rules and an optimal-order `O(N^-2)` error rate.
Thus using adaptive convex-function bands is established. This audit did
not identify a degree-uniform whole-formulation integer-count theorem there.

Frenzen, Sasao, and Butler,
[On the number of segments needed in a piecewise linear approximation](https://www.sciencedirect.com/science/article/pii/S0377042709008528)
(2010, DOI `10.1016/j.cam.2009.12.035`), is a particularly relevant predecessor
on optimal nonuniform segmentation and asymptotic segment counts. Its
publisher abstract was available through search, but full text could not be
opened in this audit. Do not describe its exact hypotheses or uniformity
in a varying family of powers as independently checked here. In particular,
an asymptotic statement for each fixed function does not establish a bound
uniform over degrees.

Wei, Hu, Wu, and Ding's
[2019 traffic-assignment paper](https://backend.orbit.dtu.dk/ws/files/194651519/Efficient_Computation_of_User_Optimal_Traffic_Assignment_via_Second_order_Cone_and_Linear_Programming_Techniques.pdf)
was checked in full at Section III.B, printed page 137014. Equation (15)
starts from a uniform-mesh estimate using the maximum second derivative;
Algorithm 1 then merges adjacent intervals after checking chord error.
This is direct prior use of adaptive power interpolation in network
optimization. Its convex objective permits an LP formulation whose optimum
uses adjacent interpolation points. That is different from requiring every
feasible lifted graph point to satisfy a uniform vertical error bound.

Lee, Skipper, Speakman, and Xu,
[Gaining or Losing Perspective for Piecewise-Linear Under-Estimators of Convex Univariate Functions](https://arxiv.org/pdf/2009.07178),
studies power functions in an on/off disjunction. Section 3 analyzes optimal
linearization-point placement using relaxation volume; Section 3.2 treats
nonquadratic powers, and Section 4 compares approximation volumes. This is
close on adaptive power approximation, but its volume criterion and on/off
relaxation are different from the present uniform whole-graph integer-count
minimum.

As a direct calculation, the curvature coordinate for `x^D` satisfies

```
integral_0^x sqrt(D(D-1)t^(D-2)) dt
  = 2 sqrt((D-1)/D) x^(D/2).
```

Thus equal spacing in `x^(D/2)` agrees with the familiar curvature-based
mesh principle. Its use as a mesh should not be presented as a surprising
new adaptive interpolation idea. The finite uniform chord bound and the
same transform's role in the universal lower bound are the relevant bridge.

## Binary encoding and lower-bound attribution

Vielma's [Embedding Formulations and Complexity for Unions of Polyhedra](https://arxiv.org/pdf/1506.01417),
Proposition 1 and Corollary 1, explicitly assign distinct binary codes to
polyhedra and use `ceil(log2 N)` bits for a union of `N` pieces. Section 2
separates the number of encoding bits from the size of the convex-hull
description. This extends the logarithmic disjunctive modeling work of
Vielma and Nemhauser. The candidate's binary cell-selection mechanism is
an application of this established idea; it does not establish compactness
merely by using few bits.

The obstruction for arbitrary integer lifts must credit Lubin, Zadik, and
Vielma, [Mixed-integer convex representability](https://arxiv.org/abs/1706.05135),
especially the midpoint/parity mechanism in Lemma 4.1 of the checked local
full text. The new proposed specialization controls the volumes of parity
supports after a nonlinear coordinate transform and combines them with the
coefficient/error-body allocation. It does not introduce parity counting.

## Claim boundary

A defensible contribution statement is: for positive pure powers sharing
one exponent per coordinate, a common power transform gives a finite
degree-independent characterization of minimum integer dimension up to
`O(r)`, including a lower bound against every convex lift and a matching
finite polyhedral construction. No exact prior match was found in this
bounded search. Do not claim first adaptive power interpolation, first
logarithmic encoding, or a compact rational degree-independent algorithm
from this finite theorem alone.
