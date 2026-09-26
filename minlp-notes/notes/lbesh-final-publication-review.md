# Final independent scientific review of LB-ESH development

Reviewer: `/root/final_publication_review`, 2026-09-19. This reviewer did
not author the method, implementation, theory, instances, protocol,
diagnostic, or study analysis. The review asks whether the developed topic
can support a strong, defensible computational or methodological publication
within its stated scope. It does not predict journal acceptance. The
separate final numerical audit supplies the detailed data checks.

**Final verdict: ready within the narrow computational and methodological
scope.** The topic is sufficiently developed to support a rigorous,
defensible publication on radial versus point separation in this
NLP-assisted perspective-OA solver for convex GDP. All declared evidence
is complete, the independent numerical audit has passed, and the final
interpretation answers a concrete design question with both favorable
and unfavorable findings. I identify no remaining development or experiment
required for that scoped contribution.

This verdict does not establish a major new algorithmic or theoretical
advance. The practical effect of changing the separator is modest and does
not transfer uniformly to the external set. A strong publication in the
intended scope must make the controlled comparison and its limits central;
claims of a new framework, broad practical superiority, or an effective
separation-only solver would exceed the evidence. Journal fit and editorial
acceptance remain decisions beyond this readiness review.

## Mathematical substance

I independently reconstructed the perspective identity, both separation
margins, the compactness arguments, the geometric repair construction, the
intersection counterexample, and the representation example. I found no
remaining mathematical defect in the qualified statements.

The strongest mathematical content is the precise distinction among valid
cuts, fixed-residual separation, a completed fractional residual check, and
an objective-gap certificate. In particular, a finite valid approximation
can provide a useful lower bound while its last LP point remains outside
the perspective relaxation. The study must retain this distinction when
comparing stalled LP phases with cone references. The fixed lambda cutoff
in the executable implementation is different from the residual-calibrated
rule analyzed in the theory.

The repair bound concerns one disjunction. The example with `x^2 <= y`,
`y <= 0`, and objective `-x` correctly shows why intersecting that hull with
global rows can change a linear residual estimate into a square-root value
error. The compactness proof gives convergence in value when residuals and
master optimality errors vanish; it does not supply a rate or finite exact
termination. The single-tree result explicitly depends on enforcement of
old lazy cuts and bounded or controlled fractional separation work.

These are useful methodological clarifications. Their proofs are elementary
consequences of convexity, boundedness, and valid relaxation bounds. They
should support the computational question rather than carry a claim of a
major new convergence theory.

## Contribution relative to established work

I independently consulted the primary-source records for
[Serrano, Schwarz, and Gleixner](https://arxiv.org/abs/1905.08157),
[Bestuzheva, Gleixner, and Vigerske](https://arxiv.org/abs/2103.09573), and
the full [Kronqvist–Misener manuscript](https://optimization-online.org/wp-content/uploads/2020/08/7957.pdf).
The first establishes the Kelley-reformulation interpretation of supporting
hyperplanes. The second studies perspective cuts computationally, including
cases where smaller trees do not improve mean time. The third already
combines ESH with disjunctive strengthening and avoids nonlinear-perspective
evaluation. These precedents rule out claiming those ingredients as the
new scientific result. They do not establish that the present controlled
comparison is redundant.

A defensible question remains: under the same GDP master, initialization,
incumbent policy, solver, and acceptance rules, when does a radial cut repay
its additional generation cost? Matching those policies makes differences
between ESH and ECP interpretable. It also limits the answer to that shared
implementation: ECP need not pay for strict interiors in an independently
optimized implementation.

The actual-oracle experiment answers a subsidiary question rather than
replacing the GDP study. It holds the geometry and anchor fixed, measures
ordinary root-search calls, uses common geometric stopping, and includes
an off-center non-dominance witness. Its scalar recurrence is a form of
Newton iteration; its contribution is the transparent executable diagnostic,
not a newly discovered principle. The centered ellipsoid examples are
deliberately favorable geometry. Their invariance and cut dominance cannot
be extended to arbitrary anchors or to complete solver trajectories.

## What the completed primary evidence establishes

The primary and repeated observations already support an interpretable
pattern: radial separation costs more per generated cut, while its matched
runs use fewer cuts and less measured search work on average. The modest
common-solved timing advantage persists in all three held-out single-tree
schedules. The additional solved cases also persist. This is stronger
evidence than a cut-count comparison or an isolated aggregate speed ranking.
It does not identify which component mediates each instance's time saving.

Inspection of the audited cohort medians sharpens that statement. Cuts and
LP iterations are lower under ESH in both means and medians in all four
held-out comparisons. Node and reduced-NLP counts are different: for hull
single, ESH/ECP median nodes are 9/8 and median NLP counts are 4.5/4,
although both arithmetic means favor ESH. Hull-multiple median nodes also
slightly favor ECP. Thus the measured search-work savings are concentrated
in harder cases and cannot be described as a uniform reduction. This does
not invalidate the aggregate cost tradeoff; it makes its scope explicit.

The limits are consequential. Most common-solved instances take only a few
seconds. Shared interior construction takes roughly a second, while
component costs overlap. Individual timing variation is of similar size to
some oracle differences. Repeated schedules use the same search seed and
the same related generated instances. No population-level or broad
statistical claim follows from the repeated direction.

The formulation and tree comparisons help place the separator effect in
context. Their measured differences exceed the ESH/ECP difference, and the
exact quadratic conic formulation is substantially faster on every complete
quadratic cohort considered in the analysis. These are substantive design
lessons that must remain in the final account. Generic-baseline solved
counts cannot cancel the supported conic comparison or establish that
expression-oracle separation is generally preferable.

The generated study has two principal structures, despite six function
families. The external legacy models contain no nonquadratic nonlinear
disjunct rows. They can test transfer and expose numerical limits, but cannot
turn these controlled examples into evidence of broad nonquadratic
application superiority. A narrow controlled-computation contribution does
not inherently require such a superiority claim.

## Supplementary results and their scientific implications

The completed external study limits transfer of the generated finding.
ESH and ECP have identical accepted counts in every matched legacy
configuration. In the expression-defined stratum without norm objectives,
single-tree ESH is slightly slower and multi-tree ESH slightly faster.
Those differences were not repeated. The conic formulation is faster on
the common supported cohort, with separate open-gap cases preventing a
coverage-dominance claim. The final account correctly preserves interface
errors and nonsmooth stress cases instead of treating them as evidence of
solver-search superiority.

The negative integer-point-NLP ablation is substantial. Only one of 72
runs solves, compared with 69 of the matched default runs. I independently
reconstructed the 53 stalls without an incumbent, nine stalls with accepted
incumbents but open gaps, nine time limits without incumbents, and one
solve. Every matched option pair differs only in `nlp_at_integer`, and
every ablation records zero reduced NLP calls. Interior NLP calls remain.

I independently read the callback, finalization, primal validator, and
cut-generation paths and reviewed the
[solver-free diagnosis](lbesh-nonlp-ablation-diagnosis.md). Its interpretation
is correct: `stalled` on this single-tree path follows a master-optimal
termination without satisfying the original incumbent/gap contract. The
records do not retain the rejected final candidates and cannot identify
the precise numerical cause. In particular, nine stalls retained feasible
incumbents, so lack of every feasible point is not a universal explanation.
The diagnosis appropriately separates observed failure from plausible
floating-point enforcement mechanisms.

This ablation rules out presenting the prototype as an effective
separation-only solver. It does not contradict the mathematical separation
contract or invalidate the matched NLP-assisted comparison. The findings
should concern the whole successful policy. Repairing and validating a
robust policy without integer-point NLPs would be a further development,
not a prerequisite for honestly reporting this negative ablation.

The optional fractional callback supplies another useful negative result:
it actually generates additional cuts, but gives no accepted-count gain
or persuasive timing improvement on the declared pilot set. These results
help answer which additions matter in the tested implementation. They do
not justify a universal policy recommendation.

The root comparison uses the same hull target and separates 40 optimal
cone statuses from two inaccurate statuses. Its normalized value
differences are numerical diagnostics rather than primal residuals or
certified objective errors. The 14 exhaustive small enumerations retain
all assignments and their statuses, and the accepted primary results agree
with their best feasible objectives within the declared tolerance. This
provides useful cross-formulation evidence without promoting numerical
infeasibility or cone dual estimates to exact certificates.

## Final evidence and decision

The final study accounts for 1,464 benchmark records and 420 cone-reference
solve calls: 42 roots and 378 fixed-assignment calls. The separate fresh
auditor revalidated witnesses, checked all schedules and source provenance,
found no cross-witness bound/status contradictions, and independently matched
6,122 final summary/pair fields. Its final secondary-query audit also accepts
the legacy, ablation/reference, repetition, and 33 followup-pair calculations.
I read the completed results note against those accepted evidence and scope
boundaries; I did not reimplement the whole numerical audit.

The baseline followups materially qualify interpretation. Tighter Gurobi
feasibility on all nine trig cases gives nine valid witnesses and six
accepted solves, while three large cases retain open gaps. Declared initial
values on all 24 affected legacy baseline pairs allow all solver calls to
return, with 23 valid witnesses and 11 accepted solves. The remaining
invalid farm witness is retained. The batch-processing Gurobi native log
reports a closed gap while the declared GAMS bound field is missing; the
study correctly describes this as missing interface evidence rather than
a solver-search failure. No original record is replaced or combined with
a followup through best-of selection.

The final scientific answer is therefore specific. Radial cuts show a
small repeatable benefit in the matched generated single-tree study, and
measured work explains the cost tradeoff. Formulation, tree management,
NLP-assisted incumbent recovery, and available conic structure matter more
in these experiments. External results and optional-cut ablations bound
the recommendation instead of being hidden. The representation diagnostic
explains a relevant geometric mechanism without claiming to identify the
cause of every GDP result. This is an informative answer to the declared
question, not merely an implementation plus an inconclusive timing table.

No arbitrary minimum speedup, statistical significance claim on dependent
controls, additional new theorem, or broader superiority claim is necessary
for that conclusion. Public nonquadratic application breadth, an optimized
standalone ECP comparison, a tested residual-calibrated fractional policy,
and robust separation-only incumbent recovery would support different or
broader questions. They are further research directions rather than hidden
unfinished requirements of this completed study.

## Review actions

Read the four development notes, literature comparison, frozen protocol,
claim register, publication challenge, primary/repeat results note, oracle
diagnostic, and independent theory, solver, harness, instance/cone, legacy
scope, and numerical-analysis reviews. Reconstructed the mathematical
arguments independently and consulted the primary sources linked above.
Solver-free `python -` queries inspected the held-out cohort means and
medians in `analysis_primary_v1/cohorts.json` and the matched observations
in `records.csv`; these use the independently audited exports rather than
a fresh raw-data recomputation. A further paired query corroborated the
concentration claim: in every comparison the highest-work quarter, ranked
by the maximum of the two methods' node counts, accounts for nearly all
or more than the total net node savings. Big-M single has 14 instances with
fewer ESH nodes, one tie, and 16 with more ESH nodes despite its lower mean.
No optimizer, project-wide verification, or CI inspection was run. This
review does not duplicate the independent numerical auditor's role.

Final reviewed SHA-256 values:

- Results note: `7d55fb9e688165818ebbdb4624d463998dd4f0ecd03c3b3c5ed0ea97fade38a3`.
  Provenance caveat (added 2026-09-25): this recorded digest does not match
  the only preserved version of `notes/lbesh-study-results.md` (SHA-256
  `b974bbd353029f4f3d50251be7f7474a6b379e9013ba5d81b3dece1b41ccbd15`, the
  single version in Git history before the 2026-09-25 wording corrections
  and the copy in `paper-lbesh/supplement/publication_bundle_v1.tar.gz`). Which bytes this
  review examined is not established; the mismatch may be a transcription
  error or a digest of an unretained intermediate version.
- Theory note: `7f1a0d0ee7c9d5719bcc58755dab9ba7961205730e61a2c070ecae8b1508909e`.
- Final analysis: `7662bd25a0f66672e959a9a1f222014a178eff6b0b355f39ba0726ed98f6d34c`.
- Final independent query audit: `4c25566982957200dd5246885ce8b36ebf9fea3cb928904c810b3fa5e0e4b3dd`.
