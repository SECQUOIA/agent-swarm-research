# Independent publication-value challenge

Date: 2026-09-19. Reviewer: fresh subagent
`/root/publication_challenge`. This reviewer did not author the algorithm,
theory, generated instances, solver repairs, or experiment protocol. The
assessment covers the current development notes, frozen study protocol, and
independent theory, solver, harness, instance, and conic reviews. The main
study was running during this review. No partial performance results were
inspected or used, and no solver runs were performed.

## Preliminary verdict

The work has a credible route to a careful computational publication. The
current mathematical results and implementation repairs do not, by
themselves, establish a strong new-method contribution. The decisive question
is whether the completed study teaches a reproducible, useful lesson about
radial versus point separation within the same GDP master. A negative or
modest result can answer that question. More benchmark rows without an
interpretable result cannot.

The independent reviews support mathematical and experimental readiness
within the stated scope. Their approval must not be converted into approval
of scientific novelty, practical importance, or a journal acceptance claim.
This preliminary assessment cannot declare publication readiness before the
scheduled results, repetitions, ablations, and final data audit exist.

## What is substantive, and what is established

The study's useful feature is its controlled comparison. ESH and ECP use the
same original GDP, polyhedral master, incumbent policy, initialization,
solver, and numerical acceptance rules. This can distinguish an oracle's
effect from a software-package difference. The accompanying witnesses,
solver-bound checks, explicit failures, and retained schedules make a result
inspectable. Those are important conditions for a scientific claim, although
good experimental hygiene is not itself a new optimization result.

The affine cut construction, boundary search, selected-structure NLPs, and
single-tree implementation are established ingredients. The literature note
correctly acknowledges that relationship. An independent check of primary
sources confirms that [Serrano, Schwarz, and Gleixner](https://arxiv.org/abs/1905.08157)
derive supporting-hyperplane separation as Kelley separation of a particular
reformulation. [Bestuzheva, Gleixner, and Vigerske](https://arxiv.org/abs/2103.09573)
already give a computational study of perspective cuts in a general solver,
including cases where better relaxations do not produce better mean runtime.
[Coey, Lubin, and Vielma](https://arxiv.org/abs/1808.05290) combine LP outer
approximation, conic cuts, subproblems, and branch-and-bound integration, with
explicit attention to numerical tolerances. These precedents do not prove
identity of the complete LB-ESH implementation. They do rule out claiming
those ingredients as the new result.

The theory's useful content is its precise scope: fixed-tolerance separation,
the weighted residual at small indicators, a geometric repair bound for one
disjunction, and the failure of a linear objective-error bound after global
intersection. These clarify what an implementation may claim. Most proofs
are short consequences of convexity and compactness. They are supporting
analysis for a computational study, rather than sufficient evidence of a
major theoretical advance. No proof of literature priority is required, but
the absence of a matching search result is not a priority argument.

The exponential example is particularly clear, but its limitation matters.
Its ECP recurrence is Newton iteration for the scalar boundary equation;
the representation can slow that recurrence while leaving the feasible
interval unchanged. The linear lower bound on master iterations makes the
effect quantitative. It is a useful diagnostic and illustration of the
known gauge interpretation. It is not a GDP-specific hardness result, a
worst-case runtime separation, or a new principle of ESH. Counting a complete
line search as one operation while counting every ECP function evaluation
separately would exaggerate the result.

## Minimum additional evidence

The frozen study should finish without changing its scheduled comparisons
to favor preliminary outcomes. Its final analysis must explain at least one
repeatable pattern: for example, a regime in which fewer master iterations
repay line-search work, a regime where they do not, or a formulation/tree
interaction that changes that tradeoff. The explanation needs measured
solver and cut-generation work, not merely an aggregate speed ranking. The
pattern need not be an ESH victory.

A small supplementary representation experiment would supply the most
direct missing link between the theory and this implementation. Declare it
as supplementary, retain its own protocol, and include unfavorable outcomes:

1. Use equivalent rows that preserve the feasible set, objective, variable
   bounds, anchor, and initial master. Include a modest parameter grid rather
   than a single extreme exponential coefficient.
2. Stop at a common geometric or objective accuracy. Raw nonlinear residuals
   are not comparable after a change in constraint representation.
3. Record master separation iterations, root iterations, function and
   gradient evaluations, and elapsed time. Use ordinary root-search code;
   inserting a known analytical root would test a different oracle.
4. Include a multidimensional or actual disjunct-level case in addition to
   the scalar recurrence. A disk with a fixed anchor and convex increasing
   transformations of its defining row is sufficient to test the geometric
   mechanism; it should not be called an application benchmark.
5. Check whether equal exact ESH halfspaces remain sufficiently similar under
   the implemented root tolerance and row scaling. Attribute discrepancies
   to finite arithmetic or implementation policy rather than ignoring them.

This is a bounded diagnostic, not a request for a new benchmark collection.
If completed frozen-study measurements already demonstrate the mechanism
with comparable evidence, a separate diagnostic is optional. Conversely,
the scalar example alone cannot establish that the mechanism matters in
the GDP experiments.

For a stronger theoretical contribution, the residual-calibrated fractional
rule is a plausible development direction, but the current implementation
does not use it. A theorem about that rule cannot be claimed as the tested
algorithm's behavior. Implementing it, proving a new error bound, or adding
a policy selector is not required for the narrower computational paper.
Those would be additional research topics, not automatic readiness chores.

## Comparison limits that affect interpretation

**The ECP control pays for the ESH initialization policy.** This is appropriate
for isolating the cut-point rule. It does not compare two independently
optimized methods, because ECP does not inherently need strict interiors.
Describe it as a matched policy comparison. A supplementary ECP variant
without interior-point construction is necessary only if making a broader
claim that ESH is practically superior to an ECP implementation optimized
for ECP. The current comparison remains useful without that broader claim.

**Continuous conic references are relaxation references.** They can check
the target bound and root approximation error. They cannot stand in for
mixed-integer conic or conic-OA runtimes. The exact quadratic mixed-integer
baseline supplies that context on its supported subset. Without a general
mixed-integer conic baseline, restrict performance claims about cone-
representable nonquadratic examples to the solvers actually tested. No such
baseline is needed to establish a within-implementation ESH/ECP difference.

**Six generated laws do not constitute six independent applications.** The
models have two main structures, shared parameters, related sizes, and few
seeds. These are valuable mechanism controls. The separate legacy instances
add external context but are chiefly quadratic or affine; they do not by
themselves establish practical relevance on public nonquadratic GDP models.
A claim of broad application advantage would require external nonquadratic
models. A study explicitly limited to the stated mechanisms does not.

**Matched timing and full-schedule success answer different questions.** A
common-solved runtime comparison conditions on success. PAR10 includes
failure but depends on the declared timeout and penalty. Report both,
alongside actual failure counts and family/size results. Repeated launch
orders measure runtime stability, not robustness to solver search seeds.
The startup cost may dominate easy instances; report it as part of the
declared end-to-end task and use component observations to interpret it.

**Numerical optimality is an appropriate experimental claim.** Independently
checked primal witnesses and trustworthy solver-reported global bounds,
with stated tolerances, are acceptable for this numerical study. An exact
arithmetic or interval proof for every benchmark is not a prerequisite.
Do not silently upgrade those records into rigorous certificates, and
investigate any contradiction between a lower bound and an independently
validated feasible objective before reporting solved counts.

## Claims to reject

- A new cut family, or intrinsically stronger limiting relaxation than
  ordinary perspective outer approximation.
- General dominance of ESH over ECP cuts, or a runtime complexity advantage
  inferred from the scalar iteration example.
- The convex hull of the complete GDP from intersecting separate disjunction
  hulls with global rows and logic.
- Exact numerical certification from the conditional exact-arithmetic
  convergence argument or a solver's `optimal` status.
- A hull-feasible root after a stall, cap, or fixed-weight no-cut pass without
  checking the claimed residual criterion.
- An inherent inability of conic methods to handle nonquadratic functions,
  or a proof of nonrepresentability from the absent trig translation.
- General solver superiority from aggregate results on these related
  generated models, or an untouched held-out set after the disclosed
  pre-freeze continuous-reference calculation.

## Plausible publication scope and final decision rule

The plausible scope is an optimization-computation or mathematical-software
paper on radial versus point separation for perspective-cut OA of bounded,
smooth convex GDP. The theory would establish the contracts and explain
specific mechanisms; the experiments would supply the main contribution.
A completed controlled study, these corrected stopping contracts, and an
actual-oracle diagnostic can together be enough for a credible publication
in that scope. No additional new algorithm or major theorem is inherently
required. For example, a supported finding that radial cuts reduce some
master work but usually fail to repay line-search and initialization costs,
with specific formulation/tree interactions, would resolve a useful design
question even though its practical impact is modest. This is a readiness
standard for a defensible manuscript, not a prediction of editorial acceptance.
A short technical paper is a better fit if the only nontrivial result is
the representation diagnostic and the large study adds little insight.
A broad new-algorithm or major-theory framing is not justified by the
current evidence.

I would consider the narrower work ready for drafting when a fresh final
review confirms: every scheduled result is accounted for; numerical claims
survive independent witness/bound and contradiction checks; repeated and
family-level results support at least one clear substantive conclusion;
the mechanism is supported beyond a handpicked scalar example; and all
conclusions observe the comparison limits above. There is no required
minimum speedup or universal win. A careful negative finding can meet this
standard if it resolves the intended question and gives useful evidence
about why the added oracle work fails to pay.

If the final data show only small, unstable differences without a mechanism,
the honest result is a sound implementation and an inconclusive study.
That would not establish readiness for a strong publication. The remedy
would be a targeted new scientific question, rather than recasting routine
integration as theoretical novelty.

This note changed no source files. Verification consisted of independent
reading of the named local notes and reviews, direct inspection of the
three linked primary-source abstracts, and reconstruction of the role of
the scalar recurrence. No solver, benchmark, project-wide check, or CI
inspection was performed. A final results-based addendum remains pending.

## Supplementary diagnostic review

The coordinator subsequently commissioned the bounded actual-oracle
representation experiment suggested above. I independently reviewed its
code, saved data, and final author note, replayed all cases, and checked its
arithmetic and call accounting. The [independent diagnostic review](lbesh-review-oracle-diagnostic.md)
finds that it satisfies the mechanism-diagnostic requirement: it confirms
representation sensitivity, counts the real bisection work, and explicitly
demonstrates the lack of universal ESH cut dominance. It supplies supporting
evidence for a modest computational paper even if the main results are
negative. It does not by itself explain the completed GDP benchmark or
settle overall publication readiness; final study analysis remains necessary.
