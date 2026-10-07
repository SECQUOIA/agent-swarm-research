# Independent manuscript review brief

Review the actual manuscript snapshot named in the task, rather than treating
the source notes or prewriting audits as a proof of the manuscript. The user
requires a coherent, complete paper suitable for a reputable journal, with
clear language, precise original contributions, verified proofs, and careful
relations to prior work. No optimization experiments should be rerun.

Reviewers may read the local mathematical source notes and Luna's literature
audit. They must not perform literature research themselves: the user requires
GPT Luna with max reasoning for that work. Send source requests to the parent.
Do not edit another author's manuscript files during an independent review.

For each issue, state its severity, exact source location, mathematical reason,
and a concrete repair or counterexample. Distinguish missing proof from false
statement. Check every theorem's model, finite law, bit complexity, and output
contract. Do not approve on the basis of successful compilation.

In particular:

1. Does independent noise remain independent in each counting argument? Are
   adaptive states bounded by a deterministic count rather than conditioned
   incorrectly on survival?
2. Does pruning preserve a global optimizer across all bags and feasible
   constraints? Is the rounding allowance global where it needs to be?
3. Does every exact closure have a sound check, a proved stopping event, a
   base-selected finite sampler, and a same-draw exact fallback?
4. Are finite atoms, ties, singular optima, original versus artificial bounds,
   integer singletons, and lower-dimensional faces handled?
5. Are polynomial-bit and parameter-dependent-bit samplers distinguished?
   Is every claimed fixed-parameter polynomial exponent independent of the
   structural parameter? Are numerical scales stated outside bit length?
6. Do every-draw output length, expected computation, arbitrary-precision
   refinement, implicit patch descriptors, shared algebraic roots, and sums
   across components each have the claimed contract?
7. Are recourse restrictions solved globally, including certified lower values?
   Are core-dependent feasibility and qualitative strict convexity excluded
   where the proof needs fixed feasibility or a uniform modulus?
8. Do any reductions assume convexity or curvature after noise conditioning
   without a uniform pre-draw bound?
9. Are scientific results self-contained up to cited classical theorems? Are
   source-note paths and review history absent from the scientific proof chain?
10. Do the introductory claims, table, examples, and limitations agree with the
    proved results and Luna's direct primary-source comparisons? Is a proved
    algorithmic limitation incorrectly stated as a hardness theorem?

Every report should give a publication-readiness decision for its assigned
scope, remaining blockers, and a list of checks actually performed. Preserve
qualified novelty statements when the evidence supports only a narrow claim.
