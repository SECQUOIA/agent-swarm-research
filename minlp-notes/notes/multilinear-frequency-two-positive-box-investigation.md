# Frequency two on boxes with positive lower bounds

Date: 2026-09-04. Investigation assigned to the packing-audit agent.

The universal positive-box bounds `3/2` and `2` remain unresolved in this note.
The following exact family strengthens the existing bipartite obstruction: the ratio
can approach `3/2` even with only two original monomials and a bipartite dual multigraph.
The family was independently checked by the FBBT audit agent, including all eight
vertex inequalities and the extremizing distributions. No publication-novelty claim
is made for this scope example.

## A bipartite family with ratio approaching 3/2

For `0<ε≤2`, consider

```
f_ε(x,y,z)=(2/ε)xy+xyz,
x,y∈[1,1+ε], z∈[1,3],
xbar=ybar=1+ε/4, zbar=5/2.
```

Each variable appears in at most two original nonlinear terms. The dual graph has two
term vertices joined by the parallel edges for `x,y`, and one private-variable leaf
for `z`. It is bipartite.

Put `x=1+εa`, `y=1+εb`, `z=1+2c`. The normalized mean is
`(a,b,c)=(1/4,1/4,3/4)`. Affine contributions can be deleted separately from each
term because they change neither its gap nor the full polynomial's gap. The remaining
parts are

```
A=2εab,
B=ε²ab+2εac+2εbc+2ε²abc,
C=A+B=ε[(2+ε)ab+2ac+2bc+2εabc].
```

The individual lower envelope of `A` is zero at the chosen point. For `B` and `C`,
the affine lower bounds

```
B≥ε²(a+b+c−1),
C≥2ε(a+b+c−1)
```

hold at every binary vertex, and therefore throughout the cube by multilinear
interpolation. In vertex order `000,001,010,011,100,101,110,111`, their respective
residuals are

```
B residual: [ε²,0,0,ε(2−ε),0,ε(2−ε),0,ε(ε+4)],
C residual: [2ε,0,0,0,0,0,ε²,ε(3ε+2)].
```

The assumed range `0<ε≤2` ensures all residuals are nonnegative. The bounds have
mean values `ε²/4` and `ε/2`, respectively. They are attained by the following
binary distributions, all having the required coordinate means:

| Bound | Distribution |
|---|---|
| A lower | `000,001,011,101`, each with probability `1/4` |
| B lower | `001` with probability `3/4`; `110` with probability `1/4` |
| C lower | `001` with probability `1/2`; `011,100`, each with probability `1/4` |

The common comonotone distribution

```
P(000)=1/4, P(001)=1/2, P(111)=1/4
```

simultaneously attains every included positive normalized monomial's upper envelope.
Their product means are all `1/4`. Hence the full upper value after deleting affine
parts is `3ε/2+3ε²/4`. It follows exactly that

```
tbtgap = ε(3/2+ε/2),
chgap  = ε(1+3ε/4),
ratio  = 2(ε+3)/(3ε+4) → 3/2 as ε↓0.
```

Thus no bipartite bound strictly below `3/2` can hold uniformly on positive boxes.
This does not disprove a universal positive-box `3/2` bound. At `ε=2` the ratio is
one; it is greater than one throughout `0<ε<2`.

The same family can be written with unit coefficients. Divide the polynomial by
`2/ε` and set `z'=(ε/2)z`. Then it is `xy+xyz'` on
`x,y∈[1,1+ε]`, `z'∈[ε/2,3ε/2]`, at means
`x=y=1+ε/4`, `z'=5ε/4`. Positive scaling changes both gaps by the same factor,
and the coordinate transformation preserves the envelope problems. The ratio above
is unchanged. Thus growing coefficients are unnecessary for this obstruction.

## A basic two-term upper bound

For any two positive multilinear terms on a nonnegative box, the ratio is at most
two, without a frequency assumption. Their concave envelopes are simultaneously
attained by comonotone normalized coordinates. Let their separate gaps be `T_1,T_2`,
including positive coefficient weights. A common vertex distribution minimizing
term one gives its full deficiency `T_1`, while the expected deficiency of term two
relative to its concave envelope is nonnegative. Therefore the full hull gap is at
least `T_1`; it is similarly at least `T_2`. Thus

```
H≥max(T_1,T_2)≥(T_1+T_2)/2.
```

This observation does not extend to a bound independent of the number of original
terms merely by counting terms. It is not a proof of the desired general frequency-two
bound.

## Numerical exploration so far

A seed-fixed search considered two-term supports with shared variables and private
variables, dimensions `3,…,9`, and 300 marginal/box samples per dimension. At each
sample, the individual convex envelopes were solved by full binary-vertex LPs, and a
maximin coupling LP optimized the worst positive weighting of the two terms. No ratio
above approximately `1.295` appeared in these random samples. The analytic family
above approaches `1.5` and therefore exceeds that numerical search. This illustrates
why random samples are not reliable upper-bound evidence.

A separate search is examining arbitrary small dual multigraphs, retaining exact
original-term envelopes before optimizing coefficient weights. No theorem is inferred
from its finite floating-point computations.

## Forest exactness survives on arbitrary boxes

If the original term intersection multigraph is a forest, the termwise relaxation is
exact on every box. Here each shared coordinate contributes an edge, so two shared
coordinates between the same pair of terms form a parallel-edge cycle and are excluded.
This standard junction-tree consequence was independently checked by the FBBT agent;
it is not presented as a new theorem.

Choose an optimal minimizing vertex distribution for each term at the prescribed
coordinate means. Root every component. Sample the root's distribution, then sample
each child's remaining coordinates from its own law conditional on the already
sampled shared coordinate. The two local laws give this coordinate the same Bernoulli
marginal. The child's other coordinates have not previously been sampled: otherwise
there would be a cycle or a second shared coordinate with its parent. Separator states
with probability zero are never reached, so their arbitrary conditional laws do not
affect the construction. Components can be sampled independently, and fixed
coordinates can first be substituted. Thus all local minima are attained together.

The same construction glues maximizing laws. Consequently both envelope values add,
and `T=H`. This stronger forest observation permits arbitrary signed multiaffine local
terms and arbitrary finite boxes; positivity is only needed for the separate coloring
argument below. The positive-box obstruction above depends on its parallel-edge
cycle and does not contradict forest exactness.

## Structural observations worth preserving

On a strictly positive box, normalize each variable's upper bound to one and write
its lower/upper ratio as `α_i∈(0,1]`. At a binary failure configuration `F`, an
original monomial has value proportional to

```
∏_(i∈F∩S_v) α_i = exp(−Σ_(i∈F∩S_v) w_i),
w_i=−ln α_i≥0.
```

Its deficiency problem is therefore a weighted graph-degree problem with a convex
decreasing exponential potential at each term vertex. The unit-box coverage reduction
is the limiting hard-coverage case. The same edge weight `w_i` occurs at both endpoints
because the box belongs to the variable, not to its incident term. Any proposed proof
or counterexample must retain that compatibility.

Affine expansion is valid for general degree bounds but can increase variable
frequency, so it cannot automatically transfer the unit-box frequency-two theorem.
The present two-term example makes that limitation concrete.

## A correct bipartite upper bound on arbitrary nonnegative boxes

There is a simple factor-two upper bound for the bipartite subclass. This argument
was independently checked by the FBBT audit agent.

Let `A,B` be the two color classes of the original term conflict graph, and include
positive coefficient weights in the separate gaps `T_v`. Distinct terms within one
color class have disjoint supports. Their individual convex-envelope minimizing
vertex distributions can therefore be sampled independently and joined into one
global distribution with the prescribed coordinate means; any remaining coordinates
can be filled by arbitrary correct-mean laws. Under this distribution, every term
in the chosen class attains its full gap. Every other term has nonnegative **expected**
deficiency relative to its own concave-envelope value. Common comonotone attainment
makes the sum of these concave-envelope values equal the full polynomial's concave
envelope. Consequently

```
H≥Σ_(v∈A)T_v,     H≥Σ_(v∈B)T_v,
T=Σ_v T_v≤2H.
```

The same reasoning gives a bound by the chromatic number for any original term
conflict graph: one color class has at least that fraction of the total term gap.
This proof works on arbitrary nonnegative boxes and does not use a degree bound.
Fixed coordinates may first be substituted. It does not establish the desired
universal constant for nonbipartite frequency-two graphs, whose chromatic numbers
can be large.

Thus the current rigorously established positive-box bipartite worst ratio lies
between `3/2` and `2`, with `3/2` approached by the unit-coefficient family above.
The exact value within that interval remains open in this investigation.

The small-dual-multigraph search in `code/multilinear_frequency_two_positive_box_search.py` has now completed: dimensions `4,…,10`, 500 proposed
samples per dimension, 3–6 term vertices, and variables assigned to two distinct term
vertices. Samples with degree-one terms or duplicate supports were skipped. Positive
lower/upper ratios included both values near zero and values near one. The coefficient
optimization used each original term's exact vertex-envelope LP, after subtracting
affine parts and rescaling for numerical conditioning. The largest sampled ratio was
approximately `1.391`. No ratio above `3/2` was found. This limited floating-point
search cannot settle either universal bound.

A subsequent differential-evolution search on two trilinear terms with two shared
coordinates and one private coordinate each used three seeds, each with population
96 and 250 iterations, on logit-parameterized box ratios and marginals in `[-8,8]`.
It approached approximately `1.499654` but found no value above `3/2`. This remains
floating-point exploratory evidence and supplies no universal upper bound.

A two-seed differential-evolution search on the doubled triangle (six variables,
three degree-four original terms, two shared variables for each pair of terms)
used population 120 and 200 iterations per seed, optimizing both box ratios and
marginals, with coefficient weights optimized by the maximin LP. It finished at a
largest sampled ratio of approximately `1.49999486`, again below `3/2`.

There is now a rigorously derived extension for boxes whose upper/lower ratios are
equal across coordinates in each connected component. See the master
[convex-cardinality factor theorem](../results/convex-cardinality-frequency-two-gap.md).
It restores bipartite exactness and the sharp odd-girth gap bound on that subclass.
The family in this note has unequal aspect ratios, which is why it remains an
obstruction. Arbitrary aspect ratios remain outside that theorem.
