# Root review of the first model draft

Snapshot: first `sections/02-model.tex`, read 2026-10-05 before the complete
manuscript existed. These are concrete issues to resolve in the final draft.
The model and its tie example otherwise provide a clear useful introduction.

1. **Scope correction.** The statements that every positive result uses a
   rare fallback are false for lattice-based native integer low-rank closure
   and strong-field component optimization. Those methods solve every draw
   without such a fallback. Describe fallback as the common design of the
   closure theorems and explicitly identify these alternatives. Similarly a
   finite law requires a way to handle ties, not necessarily this architecture.
2. **Representation correction.** The regret proposition is valid, but its
   exact-optimum specialization can have algebraic or implicit endpoints.
   The claim that its endpoints are rational and exactly computable holds
   only when a rational lower enclosure and feasible rational point are used
   (or the underlying result has rational output). For general outputs obtain
   rational certified endpoints by finite-precision evaluation, with its
   additional error charged to delta. Exact algebraic expressions can be
   retained in the mathematical bound without calling them rational.
3. **Scope correction.** The original-objective approximation paragraph must
   exclude strong-field theorems, whose sufficient noise scale cannot be made
   arbitrarily small. A Gaussian-like sampler has support radius larger than
   sigma; calibrate regret using the actual support radius. Merely taking
   sigma proportional to epsilon is not its stated all-draw guarantee.
4. **Wording.** The perturbation models are different, but overlap in special
   cases (all coordinates as core, or T=identity). Replace the unqualified
   assertion that the models are not nested by the precise point that their
   guarantees do not automatically transfer.
5. **Wording.** Distinguish promises needed for correctness from assumptions
   needed only for the complexity bound, rather than saying a correctness
   premise may be needed only for running time.
6. **Output scope.** Implicit graph constraints need a charted implicit
   descriptor. Their feasible set is a graph, not an original-coordinate box
   or relative polytope, and their reduced objective need not be a polynomial.
   Define the certified chart, its unique reduced patch optimizer, and its
   exact feasible lift, with the derivative/evaluation oracle contract. The
   existing box-patch format alone does not describe this result. Explicit
   polynomial graph maps are a simpler charted special case.
7. **Feasibility of approximations.** An implicit graph can have no rational
   full feasible point: H(y)=y^2-2=0 with y in [1,2] is an example. Its output
   may give rational free coordinates and an exact algebraic dependent lift,
   or rational approximations to the full coordinates that need not be
   feasible. Do not promise an exactly feasible fully rational point for this
   class. Original-objective certificates must evaluate an exactly feasible
   lift, with certified value intervals; arbitrary coordinate approximations
   cannot be substituted in the regret proposition.
8. **Units and accounting.** Certificate encoding length belongs in I;
   certificate verification work belongs in the runtime. Do not include the
   latter in a definition of binary input length.
9. **Noise terminology.** Use noise scale sigma in the general model. It is
   the half-width for the uniform grid law and the standard-deviation scale
   of the Gaussian proxy; it is not the Gaussian-like sampler's support
   half-width.
10. **Integration repetition.** The current recourse section already states
   the star counterexample, rotating-fiber examples, and rank-separation
   proposition, with full proofs assigned to Appendix E. The boundary section
   should explain their implications and cross-reference them instead of
   repeating the same formal statements and proofs in Appendix G. Reconcile
   `prop:lim:local` with `ex:rec:star`, `prop:lim:rotating` with
   `ex:rec:fiber`, and `prop:lim:rank` with `prop:rec:rank` after the draft
   is complete. This preserves coverage and improves the reading order.

No experiment or literature search was performed for this review.
