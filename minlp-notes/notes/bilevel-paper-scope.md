# Proposed scope of the structured bilevel paper

Date: 2026-09-07. Editorial organization of reviewed results; this file adds
no theorem. The [classical comparison](bilevel-classical-positioning.md)
and [full scope map](bilevel-response-complexity-map.md) give the precise
qualifications and sources.

## Primary question and model

Lead with the question: when can a leader optimize globally against many
follower decisions whose interactions pass through only a few shared quantities?
The main result is the polynomial-size compressed description of the **global**
reaction graph, including nonconvex aggregate costs. It is stronger than a
stationarity description and depends on more than a small leader dimension.

Use the fixed-normal optimistic quadratic-block model as the primary theorem:
fixed leader dimension, aggregate dimension, shared-resource count, and local
block dimension; positive-definite local quadratic costs; a possibly nonconvex
explicit polynomial aggregate; many follower variables and local constraint
rows; explicitly encoded polynomial upper data. State the original feasibility,
compactness, and degree-encoding hypotheses directly from the
[block theorem](../results/bilevel-fixed-block-response-algorithm.md).
Recover the exact algebraic optimum under those hypotheses.

The proof should explain the convex local fibers first, then the bounded
number of compressed variables, and finally the comparison of competing
follower values that removes nonglobal stationary responses. Attribute local
elimination and fixed-dimensional algebraic tools before stating what their
combination establishes here.

Use “polynomial time for fixed structural dimensions.” The proved parameter
dependence is XP-type, not a formal FPT running time. Deng's classical positive
result fixes follower dimension, while the repository allows it to grow.

## Keep the guarantees separate

| Package | Response convention | Output and principal qualification |
| --- | --- | --- |
| Primary exact theorem | Optimistic global follower | Exact algebraic optimum; fixed structural dimensions and explicit degree encoding |
| Moving-normal and pessimistic extension | Explicitly stated tie and upper-feasibility conventions | Infimum/supremum and attainment decided separately; an optimal leader need not exist |
| Cost-near-optimal robustness | All responses within a cost budget of the nominal global minimum | Exact robust feasibility and value/attainment; fixed measurement dimension per upper criterion |
| Polynomial-local-cost approximation | Unique convex follower | Runtime polynomial in accuracy bits for prescribed additive error; rational leader satisfies base leader constraints and admits a feasible follower |
| Response-dependent upper constraints in approximation | Same unique follower | Unconditional bicriteria guarantee; exact rational upper feasibility needs a tightening modulus |
| Executable nonconvex specialization | Optimistic or universally feasible pessimistic | One aligned tariff and one concave quadratic aggregate; exact degree-two output and all true ties |

The accuracy-bit result is substantial enough to be a separate main theorem
or a companion paper if the exact and robust material makes one manuscript
too long. It should not be compressed into a claim that arbitrary nonlinear
followers can be solved exactly with rational outputs.

## Computational narrative

Use the [nonconvex scalar implementation](bilevel-nonconvex-scalar-algorithm.md)
to show the main mechanism in executable form. Explain the follower jump,
the capacity-constrained optimistic optimum versus unattained pessimistic
supremum, and the convexification example that invents false follower choices.
Report original-space independent checks and repeated runtime distributions.
Distinguish heterogeneous breakpoint counts from large repeated-type populations.

The earlier convex tariff sweep remains useful for scale, but cannot stand
in for a nonconvex implementation. Screening should be a secondary result
or appendix: its conditional transition bound is proved, while its existing
prototype lost the recorded MILP comparison. There is no established solver
advantage or calibrated industrial case study.

## Boundaries and claims to avoid

The existing polynomial-bit small gap already separates polynomial dependence
on `1/epsilon` from polynomial dependence on accuracy bits, subject to the
precise conditioned-box assumptions and `P!=NP`. Seeking an inverse-polynomial
absolute hardness gap in that same bounded-coefficient class would conflict
with its existing approximation algorithm. Strong hardness is not a missing
premise of the accuracy-bit separation.

Describe the other hardness and representation results as limits of the
structural approach. Do not say every fixed parameter has a matching necessity
theorem. Do not infer general treewidth tractability from fixed-core results,
or describe integer followers as an unfinished part of the continuous model.

The source package supports writing a theory paper with an exact computational
illustration. Submission still requires a coherent manuscript, appropriate
length and notation, and its normal review process. The current experiments
support correctness and demonstrate scope; they do not establish broad
practical superiority. Novelty remains a qualified comparison with the sources
actually checked.
