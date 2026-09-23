# One pool, one quality, and an unrestricted bypass graph

Date: 2026-09-05. Status: a later fixed-contract hardness candidate is under
review; no upper-flow-bound-only classification is proved.

The [copy-gadget candidate](pooling-one-pool-bypass-copy-hardness.md)
developed after the initial obstacles below encodes bounded-coefficient
linear systems through bypass flows. It uses one physical quality with
lower and upper bounds, exact supplies and demands, and only one mixing
pool. Independent reviewers are checking the full construction. The
[source comparison](pooling-single-quality-bypass-novelty.md) records a
prior broad hardness claim and why novelty must be qualified.

The current target is standard pooling with one pool, one quality, arbitrary
input and output counts, arbitrary direct input-output arcs, and shared
input capacity constraints. This case is distinct from the reviewed
two-pool/two-output hardness theorem, which requires growing quality
dimension, and from the constructive fixed-pool/fixed-quality theorem with
controlled bypass structure.

## Source boundary

Haugland's final model excludes direct arcs and explains that they can be
subdivided into degree-one pools. That operation does not preserve a bound
on the number of pools, so the single-pool polynomial result does not by
itself settle this target. See
[[haugland2016-the-computational-complexity-of-the]] p.4 and the local
source audit for exact model details.

Baltean-Lugojan and Misener's
[*Piecewise parametric structure in the pooling problem*](https://d-nb.info/1149002905/34)
proves a single-quality, one-pool algorithm under assumptions dropping
source and pool capacities and fixing output demands. Its Remark 4.6
broadly asserts hardness upon relaxing those assumptions, but the displayed
argument invokes polynomial systems rather than giving a reduction with
the current cardinalities. This is a prior claim requiring careful
comparison, not evidence that the present question is unstudied.

Searches with `single pool`, `one quality`, `direct`, `bypass`, `capacity`,
and `complexity` returned these familiar sources and later summaries;
no independently checked reduction for the precise target has yet been
identified. A claim of new classification would require a further audit.

## Why the immediate methods do not settle it

Fixing the scalar pool quality `q` gives a polynomial-size LP. However,
the parametric LP can have many changing bases; one nonlinear scalar alone
does not justify polynomial exact optimization. In particular the output
constraints contain

```
sum_i (lambda_i-mu_j) z_ij + (q-mu_j)y_j <= 0,
```

while the pool equality is

```
sum_i (lambda_i-q)x_i = 0.
```

Shared input bounds couple the `x_i` and bypass variables `z_ij` across
outputs. Eliminating output flow balance moves the `q` coefficients onto
bypass terms; it does not remove that coupling or reduce it to a fixed
number of aggregate rows.

The positive-product hardness construction encoded each defining source
polytope inequality as a separate quality. Reusing it here would require a
new way to encode an arbitrary high-dimensional polytope through a single
quality and a bypass network. A direct replacement by transportation
constraints has not been established. It would be invalid simply to assume
that every rational polytope has the required network representation.

## Constructive structural extensions worth checking

A bounded vertex cover of the bypass bipartite graph appears sufficient
for the fixed-pool/fixed-quality core-and-block theorem, even when the
number of bypass arcs grows. If the cover consists of inputs `I0` and
outputs `J0`, put their pool-adjacent and mutual arcs into the core.
Each uncovered input then has only a fixed number of pool and `J0` arcs;
each uncovered output has only a fixed number of pool and `I0` arcs.
The aggregate constraints needed at covered nodes and pools have fixed
dimension. This candidate application has been sent to the constructive
theorem's author for full formulation and review.

Similarly, a bound on the largest connected component of the bypass graph
lets all input/output variables of each component form one fixed-size
block. These observations do not settle unrestricted bypass graphs.
