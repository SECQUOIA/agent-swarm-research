# One-parameter planar paths: a quasipolynomial projection bound

Date: 2026-09-05. Status: two independent complete proof audits PASS;
author `pooling_all_two_review`. See the
[first review](review-one-parameter-path-projection.md) and
[second review](review-one-parameter-path-projection-second.md).
Priority has not been established.

The investigation sought exponentially many parameter cells in endpoint
feasibility, rather than in a dense cost response. The current outcome
is a quasipolynomial upper bound under explicit assumptions. No
exponential lower-bound construction or polynomial upper bound has been
established. Global pool mass and quality balances are not covered by
this path-only statement.

## 1. Candidate theorem and encoding

Let `lambda` range over a compact rational interval. For every fixed
`lambda`, consider the scalar path constraints

```
(x_(i-1),x_i) in P_i(lambda),  i=1,...,h.
```

Each `P_i(lambda)` is given by linear inequalities in its two path
coordinates whose coefficients are rational polynomials in `lambda`
of degree at most a fixed `d`. Include known finite rational bounds on
every path coordinate, uniformly in `lambda`. Fibers can be empty,
one-dimensional, or points. All coefficients are explicitly encoded;
arbitrary high-degree polynomials in a succinct circuit are not allowed.

Let `N` be the full input encoding length, including all rows,
coefficients, and coordinate bounds. The candidate conclusion is an
exact endpoint relation represented on at most

```
N^(O(log(h+1)))
```

parameter cells. Each cell is an open interval or an isolated point,
with algebraic endpoints of polynomial degree and encoding length. On
each cell the endpoint relation has polynomially many linear rows in
`(x_0,x_h)`, with integer-polynomial coefficients in `lambda`, each of
polynomial degree and bit length. The construction has quasipolynomial
bit complexity of the same form.

Thus a `2^(Omega(N))` number of necessary parameter cells cannot occur
in this representation under these assumptions. The claim permits a
superpolynomial number, such as `N^(Theta(log N))`; it does not establish
that this number is necessary.

## 2. Pointwise ingredient

The independently reviewed [planar composition theorem](../results/pooling-degree-two-boundary-projection.md)
says that the composition of two bounded planar convex relations with
`m_1,m_2` rows has a planar description with at most
`16(m_1+m_2+2)` rows. Its proof uses the convex lower and concave upper
boundaries and counts the crossings of a univariate convex graph with
each level. The statement includes lower-dimensional relations.

For the parameterized construction, we may use a larger absolute
constant and retain the four endpoint bounding-box rows permanently.
A full-dimensional polygon has one necessary original inequality per
facet. A bounded line segment can be specified by two opposite rows
enforcing its affine hull and at most two endpoint rows. A point in the
plane has an irredundant description with at most four inequalities.
Consequently a polynomial-size Fourier--Motzkin candidate list for a
composition has a subset of at most
`C(m_1+m_2+2)` rows, for an absolute constant `C`, defining the same
nonempty relation. This subset can be selected by ordinary planar
redundancy checks. Empty relations can instead be recorded as false.

## 3. One composition on a common parameter cell

Suppose the child descriptions have fixed row lists on an open interval
`I`. Their coefficients are integer polynomials in `lambda`, of degree
at most `D`. Work with the three coordinates `(x,y,z)` and eliminate
the shared coordinate `y`.

First split at roots of the coefficients of `y`. On an open subinterval,
each such coefficient is either identically zero or has a fixed nonzero
sign. Fourier--Motzkin elimination then combines every positive/negative
pair. If two rows are

```
a_i*x+b_i*y+c_i*z <= e_i,
a_j*x+b_j*y+c_j*z <= e_j,
```

with `b_i>0>b_j`, their new row is `-b_j` times row `i` plus `b_i`
times row `j`. It contains no `y`. There are at most
`O((m_1+m_2)^2)` candidate rows, including rows with zero `y`
coefficient. All new coefficients have degree at most `2D`. No division
or algebraic root is used to form a row. Pairs from the same child are
included; these can create necessary univariate endpoint bounds.

The same construction can be scheduled with a single refinement: list
all signed pair candidates first, and then use signs of the `y`
coefficients to decide which candidates apply on each cell. At an
isolated parameter where a nonzero polynomial coefficient vanishes,
its original row is treated as a row without `y` at that parameter.

Let the resulting candidate endpoint rows be
`A_r(lambda)*x+B_r(lambda)*z<=C_r(lambda)`, and let their number be `k`.
Split further at roots of every nonzero minor of orders one, two, and
three in their augmented row matrix `(A_r,B_r,C_r)`. Include the fixed
bounding-box rows. There are `O(k^3)` such polynomials, each of degree
`O(D)`. Identically zero polynomials cause no split. This introduces
only `O(k^3 D)` additional roots on the current cell.

These sign cells preserve the data needed for exact planar redundancy:

- Two row boundaries intersect uniquely precisely when their normal
  determinant is nonzero.
- At such an intersection, whether every other row is satisfied is
  determined by the appropriate augmented determinant and the sign
  of the normal determinant.
- Every nonempty bounded planar polyhedron has a vertex at an
  intersection of two independent row boundaries, including point and
  segment cases.

Choose a sample in one open sign cell and select a small equivalent
subset of candidate rows there, keeping the bounding box. That same
subset stays equivalent throughout the cell. Indeed, every potential
vertex of the selected bounded polyhedron has invariant feasibility
and invariant satisfaction of every omitted row. Validity on all
vertices gives validity on the whole selected polyhedron. Empty
fibers likewise remain empty on a sign cell. This argument does not
assume that the selected polygon has nonempty interior.

At isolated roots, evaluate signs and planar feasibility in the real
algebraic field of that parameter and select a small equivalent subset
there as well. Retain the selected symbolic polynomial rows with the
singleton parameter cell. Do not carry all unpruned quadratic candidate
lists up the tree at exceptional points.

## 4. Balanced recursion and cell count

Compose the path in a balanced binary tree. If helpful, pad the path
to a power of two by bounded identity relations; endpoint feasibility
is unchanged. The pointwise row-count recurrence is

```
m_parent <= C*(m_left+m_right+2).
```

Logarithmic depth therefore keeps every retained row list polynomial
in `N`. Before pruning, a node produces only polynomially many candidate
rows and minor polynomials on each common child cell.

In one parameter, overlaying two partitions requires only the union of
their breakpoints. It has `O(L_left+L_right)` cells, rather than the
product of the two cell counts. Refining a common cell by the local
minor polynomials multiplies its number of cells by at most a polynomial
in `N`. Hence

```
L_parent <= N^c * (L_left+L_right)
```

for an absolute constant `c` when `d` is fixed. Iterating over
`O(log(h+1))` levels gives the stated quasipolynomial bound. The bound
also covers all intermediate cells and row lists, up to another
polynomial factor.

This argument uses one parameter essentially: it does not replace the
overlay of multidimensional semialgebraic partitions by a sum without
further justification.

## 5. Degrees, coefficient heights, and exact computation

Fourier--Motzkin combination uses two products and an addition for each
new coefficient. Along the padded balanced tree, degree at most doubles
per level. It is therefore `O(d*h)`. Integer coefficient bit lengths
satisfy the analogous doubled-height recurrence, with an additional
`O(log(d*h+1))` convolution term per level. They remain polynomial in
the original input length. Clearing rational denominators in each
original fixed-degree row also has polynomial cost.

The minor polynomials have degree `O(d*h)` and polynomial coefficient
height. Exact univariate root isolation and root comparison thus use
polynomial bit time per polynomial and produce polynomially encoded
algebraic boundaries. Rational samples between consecutive distinct
roots have polynomial bit length by the usual root-separation bounds.

At a singleton cell the parameter has polynomial algebraic degree. Its
field does not grow through composition: all row coefficients are
integer polynomials evaluated at this same parameter. Comparisons and
planar intersections are performed in that field. Symbolic row
selection, rather than adjoining new roots, preserves the preceding
degree and height bounds.

The construction can also retain every composition tree for a cell.
Given a parameter value and feasible endpoint values, the original
path can be recovered by interval-slice intersections as in the
nonparametric theorem. This lifting observation is not needed for
the cell-count bound.

An immediate decision corollary is quasipolynomial-bit feasibility of
the full path with existential choice of its scalar parameter. Apply
one final minor-sign refinement if needed, including when `h=1`.
Endpoint emptiness is then constant on each open cell. Inspect one
rational sample in every open cell and each algebraic singleton; a
nonempty endpoint polygon gives a full feasible path.

A feasible witness can be chosen with polynomial algebraic degree and
encoding length. The selected parameter has those bounds. At that
parameter, the bounded full path LP has a vertex. Cramer determinants
for an active basis, using the original polynomial row coefficients,
express every coordinate as a rational function of that same parameter
with polynomial degree and coefficient height. Constructive interval
lifting is also compatible with this bound: retain symbolic rational
functions of the one parameter during its rational affine recurrences.
Degrees and heights increase by a constant factor per balanced level,
plus the polynomial size of the node's row coefficients. They therefore
remain polynomial. This argument avoids assuming that unrestricted
repeated algebraic inversions preserve small coefficient heights.

## 6. Application boundary and unsuccessful shortcuts

With a fixed number of pools and fixed affine quality rank, fixing the
pool-quality parameters makes a node's local constraints a bounded LP
in a fixed number of its pool arcs and its at most two bypass arcs.
Local elimination may give parameter-dependent planar relations. The
candidate theorem can apply to a single common scalar parameter once
these local descriptions and their parameter partitions meet the
stated encoding requirements.

It does not settle feasibility of the full pooling network with
unbounded attachments. Pool conservation and pool attribute balance
still contain dense sums over local flows eliminated along the paths.
There is no endpoint-only replacement for these sums in this proof.
The same limitation applies to a dense cost threshold.

There is a further simple restriction on physical lower-bound examples.
With one scalar quality and only upper output specifications, the local
output LPs are nested decreasing in the pool quality `q` before global
pool balances are imposed. A quality row is

```
q*w_pool + sum_i C_i*f_i <= U*(w_pool+sum_i f_i),
```

and `w_pool>=0`. Lowering `q` preserves this row and all other local
constraints. Input-node LPs are independent of `q`. Thus the projected
local path endpoint relations are nested decreasing in `q`, and their
nonempty-parameter set is an interval. This is the uniform-sign matrix
monotonicity principle, not a new theorem. It does not bound the number
of changing endpoint facets. Lower quality specifications, affine
attributes with opposing slopes, and the global identity
`q*T=sum_i C_i*y_i` do not inherit this simple nesting argument.

Two tempting lower-bound shortcuts fail:

- A dense-objective Klee--Minty shadow is not a counterexample to pure
  endpoint feasibility. Its additional value coordinate is a global
  accumulated sum.
- Inequalities `v_i>=abs(v_(i-1)-a)` do not force an iterated absolute-
  value computation. Existential intermediate values can be increased
  and may reduce a later absolute value. Additional equalities or a
  mechanism selecting the minimal value require separate justification.

Literature searches for one-parameter matrix-dependent 2VPI projection
and acyclic parametric Markov decision processes did not identify a
verified path-specific lower bound in this investigation. This is not
an exhaustive novelty search. The geometric and univariate-algebraic
ingredients are established tools; independent priority of their
quasipolynomial composition here has not been determined.

A related primary manuscript is Boveroux, Carvalho, Lodi and Louveaux,
[*On the Complexity of Linear Programs with Parametric Constraint Matrices*](https://orbi.uliege.be/bitstream/2268/345162/1/OntheComplexityofLinearProgramswithparametricConstraintMatrices.pdf).
Its Section 3.1 derives general single-scalar-parameter matrix-dependent
LP optimization hardness from Matsui's multiplicative problem. That
construction retains dense source constraints and does not give a
bounded planar-path endpoint counterexample. This manuscript is source
context only; the candidate bound above does not rely on any of its
theorems.
