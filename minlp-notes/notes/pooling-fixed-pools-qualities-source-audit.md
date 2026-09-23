# Fixed pools and qualities: source discrepancy and constructive direction

Date: 2026-09-05. Status: source discrepancy resolved after the user-supplied
published paper became available; constructive application under review.
Coordinated with the constructive core/block
investigation in [this note](constructive-minlp-new-direction.md).

## A source discrepancy resolved by the final paper

Haugland, *The hardness of the pooling problem*, MAGO 2014 proceedings,
printed page 31, Proposition 5, states NP-hardness with one quality and
either two pools or two sources and two terminals. The preceding paragraph
explicitly discusses swapping the counts of pools and qualities. Thus the
two-pool wording is present in the source and is not a mistaken reading of a
table. Section 4 says its theoretical results will be proved in the full
version; the proceedings provide no proof of this proposition.

Primary URL: [MAGO 2014 proceedings](https://www.hpca.ual.es/~MAGO14/MAGO14-Proceedings.pdf).
The PDF was retrieved and its text read directly; temporary local extraction
is `/tmp/pooling-mago-proceedings.txt` (not a permanent literature package).

However, Boland, Kalinowski, Rigterink, *A polynomially solvable case of the
pooling problem* (2017), Table 2 and Section 4, do not list a two-pool
hardness result. Their Open Problem 4 specifically asks whether polynomial
algorithms exist with two pools and bounds on inputs, outputs, and qualities.
Their table cites Haugland's published 2016 paper for the hardness cases it
does list. The [primary paper](https://optimization-online.org/wp-content/uploads/2015/08/5059.pdf)
was read, including its model and table.

The [published 2016 abstract](https://link.springer.com/article/10.1007/s10898-015-0335-y)
mentions one-quality hardness, two-source/two-terminal hardness, and degree
bounds, but does not mention two-pool hardness. Initially the full paper was
unavailable. Later in this run the user supplied it, and the local package
was promoted. Its Section 6, printed page 214 (local extraction p.16),
explicitly leaves open bounded pool count combined with a bound on the
minimum of the source, terminal, and quality counts.
[[haugland2016-the-computational-complexity-of-the]] p.16

Thus the final paper supplies no two-pool/one-quality hardness obstruction
and explicitly asks the relevant bounded-pool question. The earlier
proceedings statement should not be carried forward as a verified result.
This audit does not infer the author's reason for changing the statement.

## Candidate fixed-pool/fixed-quality application of the core/block theorem

For standard pooling with no direct input-to-output arcs, fixed numbers
`p` of pools and `k` of qualities appear to fit the proposed fixed-core,
fixed-block-dimension elimination theorem even when the number of inputs and
outputs is unbounded. This would be stronger in a different direction than
fixing the number of inputs and pools. The key distinction is that source
capacity constraints are local to input blocks.

Use core variables `q_lk` (pool qualities), `t_l` (throughputs), and `z`
(total cost). There are `pk+p+1` core variables. Pool bounds on `t` and
global min/max input-quality bounds on `q` are core constraints. The target
aggregate vector is

```
b(q,t,z) = (t_l for l, t_l for l, q_lk*t_l for l,k, z),
```

of dimension `r=2p+pk+1`.

Input `i` contributes a block `x_i∈R^p`, with missing arcs set to zero,
nonnegative arc bounds and `Σ_l x_il≤C_i`. Its linear aggregate contribution
is

```
(x_il for l, 0 for l, λ_ik*x_il for l,k, Σ_l c_il*x_il).
```

Output `j` contributes a block `y_j∈R^p`, with missing arcs set to zero,
nonnegative arc bounds, `Σ_l y_lj≤C_j`, and output specifications
`Σ_l (q_lk-μ_jk)y_lj≤0` (with the analogous lower bounds if desired).
Its aggregate contribution is

```
(0 for l, y_lj for l, 0 for l,k, Σ_l c_lj*y_lj).
```

The exact pooling equations say that the sum of all these independent block
contributions equals `b(q,t,z)`. The decision threshold is `z≤K`. Every
block dimension is `p`, the aggregate dimension is fixed, all blocks are
bounded, and coefficients depend polynomially on the fixed core. Thus the
support-function/semialgebraic-arrangement machinery under development
appears to apply. The input count does not enter any dimension bound.

This observation was sent immediately to the constructive agent and root
for independent development. It needs full checking. It does not claim an algorithm merely from
fixing the number of nonlinear variables in an arbitrary LP: the independent
small blocks and fixed aggregate dimension are essential.

## Direct arcs require separate treatment

Unrestricted direct input-to-output arcs destroy this particular block
description: direct flows couple an unbounded number of input and output
capacity rows. Replacing them by new pools does not preserve fixed `p`.
Thus this candidate uses the precise no-direct-arc model of Boland et al.
The fixed-input/fixed-pool application being developed separately can allow
direct arcs because its aggregate input capacity count is fixed.
