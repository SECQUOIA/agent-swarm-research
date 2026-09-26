# Independent review of the relative-gap direct-product bound

Date: 2026-09-05. Reviewer: independent `spatial_sdp_review` agent.
Reviewed: `notes/spatial-bb-relative-gap-investigation.md`.

**Verdict: PASS within the stated global node-oracle and single-tree
certificate model.** Tensor positivity with a total-degree truncation is
valid. The objective threshold, product-cover exponent, increasing-concave
cost interpretation, and squared-index asymmetry claim are correct. The
explicit decomposition limitation is essential and is stated properly.
This review does not establish novelty.

## Block certificates and objective estimate

The parameters satisfy `q0=t-2r+2>=1` and `q0<=t`. A block with
`|R_b|<q0` retains at least `2r-1` coordinates of each endpoint witness
type, by the same integer rounding argument used in the reviewed
higher-order theorem. Its constructed functional is therefore feasible
for every allowed block preordering and equality constraint. Its penalty
value is bounded by

```
|M_b intersect R_b| p(1-p)
<= |R_b|/(2t)
<= |R_b|/(2q0).
```

For `|R_b|>=q0`, evaluation at the contained witness is feasible, and
its penalty is `1/2-1/(4t)<=1/2<=|R_b|/(2q0)`. Thus the same objective
upper bound applies uniformly to both types of block functionals.
Both have first moments in `[0,1]` and demand expectation `K`.

The total cost satisfies the exact decomposition

```
C(x)=sum_b sum_i x_(b,i)
     +sum_b sum_i x_(b,i)(1-x_(b,i))
     +sum_b sum_i d_(b,i)x_(b,i).
```

The first term is exactly `GK` under every feasible functional. The
perturbation contributes at most `G eta`. Consequently the proposed
upper bound `GK+sum_b |R_b|/(2q0)+G eta` is correct.

## Tensor positivity under a global total-degree budget

Define the global moment of a monomial by multiplying its block moments.
Every local factor is defined because each block degree is at most the
monomial's total degree, which is at most `2r`. This definition extends
linearly to a well-defined functional on the required polynomial space.

For `g=prod_b g_b` and a global polynomial `p` of degree `d`, the assumption
`deg(g)+2d<=2r` gives `deg(g_b)+2d<=2r` separately for every block.
Therefore the matrix

```
M_b(alpha,beta)=L_b[g_b x_b^alpha x_b^beta],
deg(alpha),deg(beta)<=d,
```

is defined and PSD. Its PSD property is exactly the block preordering
inequality for `g_b` and every block polynomial of degree at most `d`.
The tensor product of these matrices is PSD. The principal submatrix
indexed by tuples of monomials with total degree at most `d` is also PSD.

For those retained indices, every entry has global degree at most
`deg(g)+2d<=2r` and equals the corresponding entry of the global
localizing matrix by the definition of the global functional. This
proves `L[g p^2]>=0` even when `p` couples all blocks. The discarded
tensor entries need not correspond to available global moments. They
serve only to construct a larger PSD matrix and cause no truncation gap.

For a demand equality from block `b` multiplied by a global monomial of
degree at most `2r-1`, factor the resulting expression into the block
`b` equality moment and moments of all other blocks. The first factor
vanishes by the block equality constraints, at a degree at most `2r`.
Linearity handles arbitrary global multipliers. Products involving
several demand equalities are therefore also zero. Locally valid
polynomial equalities, when included, obey the same argument.

## Independent numerical and exact checks

Supplementary checks used order `r=2`, two blocks of nine variables,
and demand `7/2`. The fractional-cardinality functional and exact
witness evaluation were combined in all three cases: two fractional
blocks, one fractional block and one evaluation block, and two evaluation
blocks.

For each case, the full global degree-two monomial basis included repeated
powers and had 190 indices. Its moment matrix was numerically PSD, with
smallest eigenvalue between `-1e-14` and zero up to rounding. A localizing
matrix for a lower slack in one block times an upper slack in the other
block, with all global linear square multipliers, was also PSD. Every
demand equality times every monomial of total degree at most three was
checked in exact rational arithmetic: 2,660 identities per case passed.
These checks supplement the exact tensor proof; they do not replace it.

Provenance note (added after the 2026-09-24 repository audit): the program and
raw output for these reviewer checks were not archived. The reviewer's own
runs above remain reviewer-reported and unarchived. The committed author
checker is `code/spatial_bb_lower_bound/check_relative_gap.py`.

Independent reproduction (2026-09-25): a new checker written from this
section and the fractional-cardinality lemma,
[`review_relative_gap_repro.py`](../code/spatial_bb_lower_bound/review_relative_gap_repro.py),
with saved output
[`review_relative_gap_repro-2026-09-25.log`](../code/spatial_bb_lower_bound/review_relative_gap_repro-2026-09-25.log),
reruns the three configurations (`r = 2`, two nine-variable blocks, demand
`7/2`, `q0 = 1`). It does not use the author checker. In each configuration
it reproduces exactly 2,660 exact demand-times-monomial identities
(`2 · C(21,3)`, all monomials of total degree at most three with repeated
powers). The 190-index moment matrix passes an exact rational PSD test, and
its floating-point smallest eigenvalue lies between `-1e-14` and zero. Instead
of the single cross-block localizer described above, it checks all 162
lower-slack-times-upper-slack localizers across the two blocks, with the 19
global linear multipliers; all pass exact PSD tests. The evaluation blocks
use restricted boxes chosen by the reproduction, because the review does not
record its boxes.

## Relative threshold and product counting

Every block's true penalty optimum is `1/4`, so
`OPT>=G(K+1/4)`. On a pruned domain containing a witness, the chain is

```
GK+sum_b |R_b|/(2q0)+G eta
>= value of the constructed feasible functional
>= node lower bound
>= (1-theta)OPT
>= (1-theta)G(K+1/4).
```

Rearrangement gives exactly

```
sum_b |R_b| >= 2q0 G [1/4-theta(K+1/4)-eta]
              = 2q0 G tau.
```

For a fixed product domain, the witness-containment event factors across
blocks because the witness partitions are independent and domain membership
factors by coordinate. Each block fraction is at most

```
min((2/3)^|A_b|,(2/3)^|D_b|)
=(2/3)^max(|A_b|,|D_b|)
<=(2/3)^(|R_b|/2).
```

Multiplying these inequalities gives the claimed uniform coverage bound
`(2/3)^(q0 G tau)`. The reciprocal union bound supplies the number of
pruned cover members without requiring disjoint domains or a particular
branching sequence.

For the explicit example, `tau=17/128`, `q0=2`, and `n=6G`, yielding
exponent `17G/64=17n/384`. For every fixed hierarchy order, one may fix
`t>=2r-1` and then choose a sufficiently small fixed relative tolerance.
This statement does not assert one uniform positive relative tolerance
for arbitrarily increasing `r` with this construction.

## Increasing costs, uniqueness, and asymmetry modulo demands

Every cost has derivative `2-2x+d>0` throughout `[0,1]` and second
derivative `-2`. The conserved linear term shifts each block objective
by `K`, so the previous strict-concavity and sorted-coefficient proof
gives the unique stated minimizing vertex in every block. Their product
is the unique global minimizer.

For the explicit coefficients, set `L=3t` and
`c=eta/(L n^2)`. The coefficients in block `b` are

```
c[(b-1)L+i]^2,  i=1,...,L.
```

They are positive and globally distinct. Each is at most `eta/L`,
so each block sum is at most `eta`.

The feasible set has the stated demand affine hull: the point with all
coordinates `K/L` lies strictly inside every capacity bound. A coordinate
permutation preserving the feasible set must therefore preserve the row
space of the demand matrix. That row space consists of vectors constant
on each block. The image of a block indicator is a zero-one vector in
this space with exactly `L` unit entries; since all blocks have size `L`,
it must be one whole block indicator. Thus a feasible-set symmetry maps
whole blocks to whole blocks.

The quadratic part and unperturbed linear part are permutation invariant.
If the full objective is preserved on the feasible set, the change in its
coefficient vector must be constant on each block. There is also a
condition that the resulting constant objective shift is zero; the
argument only needs the necessary blockwise-constant condition.

A translation of two finite sorted coefficient lists preserves successive
differences. In block `b` these differences are

```
c[2((b-1)L+i)+1],  i=1,...,L-1.
```

Their first entries already distinguish every block. Consequently no
two distinct blocks have coefficient lists equal up to translation,
and every block must be fixed. Within one block, a permutation of its
finite coefficient set cannot equal a nonzero translate of that same
set, as comparison of its minimum shows. The translation is zero and
distinct coefficients force the identity permutation. This proves the
claimed stronger asymmetry modulo the demand equations.

## Essential interpretation

The result concerns one tree whose node lower bounds come from the stated
global truncated polynomial oracle. The fixed-dimensional components can
instead be solved separately and their certified bounds added. That is a
short certificate outside this single-tree model, and the candidate says
so explicitly. Granting each component's exact nonlinear lower-bound
inequality at every node would also defeat the example immediately.

The argument therefore supports a precise separation between global
fixed-order moment bounds plus one spatial tree and certificates that
reuse separate component solutions. It does not establish hardness of
the allocation problem or show that a solver detecting decomposition
must use exponentially many operations.
