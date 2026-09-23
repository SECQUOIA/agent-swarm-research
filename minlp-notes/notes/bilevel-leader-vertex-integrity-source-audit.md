# Source audit: leader vertex integrity and the path obstruction

Date: 2026-09-05. This is a bounded source assessment of
[the reviewed result](../results/bilevel-leader-vertex-integrity-boundary.md), not an independent
full proof review or a priority certificate.

The proposed exact algorithm is best presented as a structural application of
classical piecewise linear elimination and fixed-dimensional arrangements.
The path construction is a useful explicit numerical obstruction. No directly
matching theorem for this precise diagonal box bilevel model was found in the
sources checked. The surrounding structural ideas are established, and one
older continuous scheduling paper requires a particularly careful comparison.

## Structural predecessors and graph distinctions

Dvořák, Eiben, Ganian, Knop, and Ordyniak, *The complexity landscape of
decompositional parameters for ILP: Programs with few global variables and
constraints*, Artificial Intelligence 300 (2021), 103561, extends their IJCAI
2017 paper. Its [open final paper](https://eprints.whiterose.ac.uk/id/eprint/179460/1/1-s2.0-S0004370221001120-main.pdf),
Section 1.1 and Table 1, explicitly studies deleting a small collection of
global variables or constraints to leave small independent components.
Its positive and negative results also depend on coefficient restrictions;
Section 5 uses bounded coefficient types. This is a direct antecedent for
the decomposition idea, but not a theorem about arbitrary rational capped
affine functions on continuous boxes. Its incidence graph counts constraint
vertices and local integer variables; the present leader graph excludes
arbitrarily many follower ramps. A generic MILP encoding can therefore have
large remaining components even when the proposed leader parameter is fixed.

Briański, Lassota, Pekárková, Pilipczuk, and Reuter, *On Integer Programs That
Look Like Paths*, [October 2025 preprint](https://arxiv.org/pdf/2510.22430),
Theorem 1, proves integer feasibility hard when the **constraint graph** is
a path and the matrix coefficients are bounded by eight. Each variable
occurs in at most two consecutive constraints. This is not the same graph
as the proposed path of leader variables. Its introduction reviews earlier
Subset Sum based sparse ILP hardness. Cite it as evidence that numerical
hardness on simple graphs is established; do not identify its stronger
coefficient restriction with the present continuous bilevel restriction.

The candidate's positive running time has an exponent depending on the core
size and component size. Call this polynomial time for fixed parameters or
an XP result, not FPT. Bounding vertex integrity is the established name for
this type of graph restriction; no new graph parameter is needed.

## Closest continuous piecewise linear source

Meuleau, Morris, and Yorke-Smith, *A Variable Elimination Approach for Optimal
Scheduling with Linear Preferences* (2008),
[author-hosted paper](https://homepage.tudelft.nl/0p6y8/papers/n58.pdf), treats
continuous domains and nonconvex piecewise linear preferences. Definitions
1–2 and the problem formulation on PDF page 2 permit the relevant local
functions. Lemmas 1–2 and Theorem 1 on PDF pages 3–4 establish closure under
summing and eliminating variables. The proof selects affine policies on
faces and compares their affine values: this is a close predecessor for
the candidate's local elimination mechanism.

The abstract's broad fixed-treewidth polynomial wording needs qualification.
The complexity discussion immediately before Algorithm 1 on PDF page 4
explicitly includes the maximum number of pieces in a function in the
**current bucket**. It does not bound that quantity polynomially in the
original input through all eliminations. Theorem 1 itself is a closure
theorem, not an original-input polynomial complexity theorem. The present
path example is compatible with that closure result and shows why the
intermediate representation size must be counted.

## Explicit intermediate-piece growth from the candidate

The following observation is independent of any complexity assumption.
Let the candidate's local penalties be

```
rho_i(t) = min(|t|, |t-r_i|),
V_n(t) = min {x_0 + sum_i rho_i(x_i-x_(i-1)) :
             x_0,...,x_(n-1) in [0,1], x_n=t}.
```

The minimum exists. All its terms are nonnegative, so `V_n(t)=0` precisely
when `x_0=0` and every increment belongs to `{0,r_i}`. Consequently its zero
set is exactly the normalized subset sums. Take
`a_i=2^(i-1)`, `W=2^n-1`, and `r_i=a_i/W`. There are `2^n` distinct isolated
zeros `k/W`. At every point strictly between consecutive zeros the value
is positive. Any exact representation by affine functions on intervals
therefore needs at least two nondegenerate pieces between each consecutive
pair of zeros: a single affine function vanishing at both endpoints would
vanish throughout. Thus at least `2(2^n-1)` pieces are needed. The original
path contains only a constant number of pieces per factor and has polynomial
rational encoding length (at most quadratic in `n`).

This establishes growth faster than every polynomial in that input length
for the natural left-to-right elimination representation. It does not
exclude a different implicit representation, and is not a new assertion
that dynamic programming can have large messages. It provides a concrete
example within the exact continuous model of the cited scheduling paper.

The final result strengthens this observation using identical factors:
`rho_(1/2)(x_i-x_(i-1)/2)` on every edge. Its exact message is
`dist(t,{j/2^n:0<=j<2^n})` and has `2^(n+1)-1` maximal affine pieces.
All local coefficients belong to a fixed finite alphabet; the structured
description has linear size. Weighted telescoping gives the distance lower
bound, while changing only the last state of a zero-cost trajectory gives
the upper bound. Two independent reviews passed this extension. The binary
contraction mechanism is elementary and no priority is claimed for it.
This strengthens the explicit representation-size example, not the weak
Subset Sum hardness reduction: the uniform family's global minimum is
trivially zero, and its distance formula itself is an implicit description.

## Recommended scope

Retain the paired result as an explicit supporting boundary: fixed core and
small leader components allow exact rational optimization despite arbitrarily
many local ramps; a path alone allows weak numerical NP-hardness. Credit the
local vertex, arrangement, elimination, clipping, and Subset Sum ingredients.
The bounded-coefficient path has gap `1/W`, not a constant gap. Multiplying
the objective by `W` changes coefficient magnitudes. Neither statement proves
strong NP-hardness with bounded numerical data, or rules out algorithms
polynomial in inverse additive tolerance. The source check supports these
qualifications and does not establish publication priority for the combined
restriction.
