# Closeout audit: pooling and power-flow existential-real completeness

Date: 2026-09-05. Scope: final reconciliation of the three existing results,
their independent proof reviews, primary-source dependencies, and verification
claims. No new research direction was started. Verdict: **PASS after the
scope and verification wording corrections below**. This is an independent
closeout audit, not external peer review or a proof of novelty.

## Established statements and interfaces

- [General pooling](../results/pooling-existential-theory-of-reals.md):
  threshold decision is `∃R`-complete with one quality and both lower and
  upper quality bounds. Complementing the attribute gives two qualities
  with upper bounds only. Saturation is forced by a sum of capacity-bounded
  group totals; bypass-free arcs belong to at most two groups. Zero-flow
  pools have arbitrary qualities but contribute zero quality mass. The
  fixed-data chain variant preserves the argument, with at most one link
  and one gadget arc per forced pool in addition to its slack arc.
- [One pool with bypasses](../results/pooling-one-pool-bypass-existential-reals.md):
  the attribute count grows with the instance. Every pinned attribute is
  zero on that terminal's bypass source, which is essential to the product
  equation. Repeated-summand normalization is bijective because inversion
  determines the fresh variables uniquely. In an addition gadget the
  auxiliary value `2/z` is at most two because a feasible addition has
  `z=x+y≥1`. Saturation counts each bypass toward both its source and
  terminal capacities. These interfaces were rechecked against reviews A
  and B; no further mathematical correction was needed.
- [Resistive and AC power flow](../results/ac-power-flow-existential-reals.md):
  the resistive reduction uses positive real voltages, arbitrary signed
  injection intervals, maximum degree three, and fixed finite data.
  The AC transfer requires real line-angle differences bounded by `π/2`.
  Principal differences alone admit nonzero winding around cycles and do
  not justify the equal-angle lemma. The separate rectangular variant
  confines bus angles relative to a reference. Section 1's crossing-count
  encoding supplies polynomial-size existential-real membership for the
  real-angle model; its signs, half-open axis convention, unequal voltage
  magnitudes, and fundamental-cycle lift were checked again.

The conditional consequence is precisely: if one of these `∃R`-complete
decision problems belonged to `NP`, then `NP=∃R`. Irrationality alone would
not prove that consequence. Likewise, fixed pool and quality counts give
an NP upper bound through the linear-fiber certificate lemma, not a
general deterministic polynomial algorithm. The general pooling note now
states this distinction and the conditional nature of the boundary.

The algebraic-degree corollary uses more than field generation. The local
primary text of Abrahamsen–Miltzow, *Dynamic Toolbox for ETRINV*, Theorem 1
and Definition 5, gives rational equivalence and an affine coordinate
projection from the ETR-INV solution set to a compact singleton `{α}`.
For irrational `α`, its rational scale is nonzero, so a designated
coordinate has the same degree as `α`. Every flow in either pooling
construction is uniquely determined by those coordinates through rational
functions. The resistive voltages have the same property. Thus the
individual-coordinate degree claim and unique-flow claim are justified;
they are stronger than merely saying that several coordinates jointly
generate `Q(α)`. AC global phase freedom is not claimed to be unique.
Primary source: [Abrahamsen–Miltzow](https://arxiv.org/abs/1912.08674).

## Corrections applied at closeout

1. Qualified the power-flow introduction's equal-angle statement with the
   real-angle restrictions. A positive numerical bound on `sum f_i²` now
   counts as a solver consistency check, not a proof that all phases vanish.
2. Clarified that the bounded-data pooling threshold grows with instance
   size. All other data come from fixed finite sets; converting saturation
   to exact node throughput bounds removes the threshold entirely.
3. Clarified the approximation remark: polynomial-bit rounding permits
   small violations of all polynomial constraints. It does not give an
   exactly feasible rational optimum or near-optimum.
4. Removed an unsupported equivalence suggested between arbitrary
   one-quality upper-only pooling and the concave-product constraint
   satisfaction problem. The existing gadgets lose their equality pins
   when lower bounds are deleted. This attempt is unresolved; the related
   CSP literature is context, not a reduction or impossibility theorem.
5. Replaced universal literature-absence and priority statements in the
   two novelty notes with conclusions restricted to the sources searched.
   The power-flow novelty note now distinguishes the corrected angle
   semantics and the Bienstock–Verma lossless fixed-magnitude model.

## Reproducible verification

The previously temporary bounded-pooling audit is saved as
[check_bounded_exact.py](../code/pooling_existential_reals/check_bounded_exact.py).
Its machine-specific import path and an unused exploratory loop were
removed; substantive checks were preserved. It independently propagates
the intended rational flow, verifies every original capacity, conservation,
quality and objective equation on seven satisfiable cases, and checks
degree, data and construction-size bounds on 300 random systems. All pass.
It imports the builder, which imports `gurobipy`, but does not run a solver.

The new narrow regression test
[check_winding_count_exact.py](../code/power_flow_existential_reals/check_winding_count_exact.py)
uses exact rational rays at multiples of `π/4`, with three unequal positive
scales, and an independent integer-angle lift oracle. It passes **360
scaled line pairs and 4,136 cycles**, including **256 nonzero windings**.
It covers axis contacts, reversed arcs, quarter-turn boundaries, repeated
vertices and the four-cycle counterexample. No numerical trigonometry or
optimization solver is used. This finite check supports the already
reviewed analytical proof; it does not replace it.

From the repository root:

```bash
python code/power_flow_existential_reals/check_winding_count_exact.py
/home/sgusev/miniconda3/envs/minlp-notes/bin/python code/pooling_existential_reals/check_bounded_exact.py
```

Earlier Gurobi gadget runs remain numerical checks recorded in the result
files and reviews. They were not repeated merely to duplicate the same
confidence. A focused web-search refresh for pooling/power flow combined
with existential-real completeness found no relevant matching primary
source. Search absence does not establish novelty; the earlier detailed
source audits and their access/version limitations remain applicable.

## Closed scope

No unreviewed extension is promoted by this closeout. One-quality
upper-only general pooling remains unresolved by these methods. The
lossless fixed-magnitude AC model, unrestricted principal-angle-only AC
transfer, and exact complexity of the tree power-flow case are outside
the established result. Their status is recorded; they are not pending
tasks or claims of impossibility. The three established results and the
bounded-data pooling variant are ready for human mathematical review
with the qualifications above.
