# Stage 1 author record

Scope: physical framework, exact calibrations, support theorem, two-scale necessity, and complete sufficient criteria. This draft is intentionally a compiling partial manuscript. The abstract describes only the completed stage; synthesis and bibliography belong to the later planned stage. No author name or affiliation has been invented.

## Files

- `main.tex`: standard article project, common theorem environments and notation.
- `sections/framework.tex`: canonical state measure, exact bath, surface heat capacity, full-state/energy TV identity, normalization, centered and secant calibrations, global and local bounds.
- `sections/thresholds.tex`: weak three-support iff theorem, exact two-atom exception, unequal-scale necessity under positive weak phase laws, positive-mixture sufficiency and iff corollary, density-tail sufficiency and physical iff theorem.

## Critical checks and decisions

1. Used a general reference measure and a Radon–Nikodym derivative from the outset. There is no density assumption in the state law, support theorem, or phase decomposition. Densities enter only the explicitly continuous tail criterion.
2. Distinguished composite energy `\mathcal E_N`, physical bath temperature `T_B`, and inverse temperature `\beta_N`. The inverse temperature is specified in advance and may converge to a positive limit.
3. Proved the unnormalized exact bath likelihood is bounded on the whole real energy line, for every finite total energy and positive exponent. Admissibility consequently needs only nonzero probability below the cutoff, not an extra moment assumption.
4. Preserved the surface-density heat capacity `C_B=k_B c_N` and explained its finite `k_B` difference from canonical reservoir heat capacity. The physical density is exact, not a quadratic entropy surrogate.
5. The centered weight is bounded by one globally. This supplies uniform integrability in the support theorem without hidden tail assumptions.
6. All necessity arguments select good-likelihood energies from positive-probability events. No pointwise likelihood convergence at chosen centers is assumed. Positive likelihood handles the cutoff directly.
7. Retained the factor `theta(1-theta)` in the chord bound. Its proof gives the explicit uniform constant `1/(2e)` and supports both equal- and unequal-spacing arguments without separate derivative or Gaussian-density arguments.
8. Formulated two-phase necessity using an actual positive decomposition with phase weights bounded away from zero. In the other phase, concentration on the gap scale is enough. The fluctuating phase needs a weak limit with two support points, not a Gaussian or moments.
9. Proved the secant-calibrated global amplification bound, tangent envelope, and local flatness explicitly before using them. A fixed exponential moment yields an actual `L^2` bound for reservoir weights, avoiding a missing uniform-integrability step.
10. Exceptional positive mass has its own amplification estimate. A signed partition remainder is explicitly insufficient, and the condition depending only on exceptional mass is stated as conservative, not necessary.
11. The density-tail theorem includes the general concave residual-weight sufficient argument because it is the shortest complete proof of the physical tail criterion and will support the later smooth-bath/capillarity stage. It does not yet add the smooth-bath necessity or the finite boundary-scale conclusions.
12. The interfacial exponent is explicitly in `[1/2,1]`, which includes all finite-dimensional droplet exponents and makes the uniform gain/cost bound direct. No unsupported dimension-dependent microscopic claim is made.
13. Explained why local density limits with total phase weight one imply actual positive midpoint-conditioned weak phase limits, so the physical density iff corollary invokes the weaker verified necessity theorem without silently requiring a decomposition.

## Sources examined

- `research/reservoir-support-classification.md`
- `research/finite-bath-physical-extension.md`
- `research/phase-decomposition-reservoir-criterion.md`
- `research/verification/three-support-bath-review.md`
- `research/verification/phase-decomposition-review.md`

The manuscript supplies its own proofs of all results introduced at this stage. Literature attribution and a complete reference list remain the scheduled synthesis task; the current abstract makes no claim of priority.

## Open work outside this stage

Microscopic verification, including the unresolved inward short-range phase-energy control, is deliberately not asserted here and belongs to Stage 2. Shared reservoirs, exact Gaussian geometry, finite boundary-scale laws, capillarity-model consequences, literature positioning, and numerical figures belong to their assigned later stages. No mathematical step in the Stage 1 theorems is left as a conjecture or cited only to an internal note.

## Compilation

`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` succeeds and produces the nine-page `main.pdf`. The final log contains no warnings, undefined references, overfull boxes, or underfull boxes. Independent review is still required by the user-prescribed workflow.
