# Publication-readiness assessment: convex GDP supporting cuts

The topic is ready to write as a strong, carefully scoped computational and
methodological paper. No major development or additional experiment remains
necessary for that scope. Fresh independent numerical and scientific reviews
accepted the completed evidence and claims. This is a research-readiness
judgment, not a prediction of journal acceptance.

The defensible contribution is a controlled computational study of radial
supporting cuts and point tangents in the same NLP-assisted GDP solver.
It explains a modest, reproducible tradeoff: radial separation can reduce
cut and search work, but pays more for each separation. Formulation and
tree policy have larger effects in these tests. The mathematical analysis
states the conditions under which the cuts and termination arguments apply
and corrects earlier claims that exceeded those conditions.

The cut family is established perspective outer approximation. The work
supports a focused computational and methodological paper. It supplies no
priority claim for perspective cuts, universal oracle dominance, or general
superiority over conic optimization. Its practical impact is modest; its
value rests on the controlled comparison, explanatory measurements, explicit
failure cases, and reproducible evidence.

| Finding | Evidence and qualification |
| --- | --- |
| ESH improves the tested single-tree policies modestly. | On 33 held-out controls, ESH solves all 33 with hull and big-M; ECP solves 32 and 31. These outcomes repeat in all three runs. Common-solved shifted wall means favor ESH by about 4–6%, with related instances, a fixed solver seed, and shared interior initialization. This is not a comparison of independently optimized ESH and ECP implementations. |
| Fewer cuts do not imply proportionate speed gains. | The held-out comparisons have fewer cuts and LP iterations under ESH, while cut generation costs roughly 5.5–6.6 times as much. Arithmetic-mean NLP and node savings concentrate in harder cases; some medians are tied or worse. Component times can overlap and must not be added. |
| Exact conic structure matters. | The quadratic conic baseline solves all nine controls with a shifted wall mean of about 0.46 seconds, versus 2.28 seconds for ESH hull single-tree. The continuous cone roots serve a separate relaxation-checking role. |
| The generated-suite advantage does not extend to the legacy solve counts. | ESH and ECP have equal accepted counts in every matched legacy configuration. Single-tree ESH is slightly slower and multi-tree ESH slightly faster on common solved models without norm objectives in this one run; those differences are not established as robust. |
| Integer-point NLP recovery matters in this prototype. | Disabling it solves only 1 of 72 pilot runs, versus 69 of 72 matched primary runs. The failures include absent incumbents and valid incumbents with open gaps. This is an implementation limitation, not a theorem that NLP solves are necessary. |
| Numerical and interface details can change a comparison. | The separate Gurobi trig tolerance follow-up validates all nine witnesses and closes six gaps. The legacy initialization follow-up removes documented writer/unused-variable problems, validates 23 of 24 witnesses, and closes 11 gaps. Original records remain intact; follow-ups are separate cohorts. |

The full record contains 1,464 benchmark runs and 420 cone-reference solver
calls using independent formulations: 42 continuous roots and 27 assignments for each of 14
small instances. Forty roots have an optimal status and two have an
inaccurate optimal status; the latter remain separately qualified numerical
estimates. All 174 optimal fixed-assignment witnesses pass the original-model
checker. Independent audits found no bound contradictions or disagreement
with the recorded original-model validation decisions. These are numerical
checks under stated tolerances, not exact-arithmetic certificates.

The 51 generated controls cover six function families and two principal
structures, with shared parameters, related sizes, and few seeds. The 27
legacy models add external context but have qualified scope: eight compact
smooth extracted models, six requiring an epigraph argument, and thirteen
broader stress cases. They do not establish broad nonquadratic application
performance. The proposed residual-calibrated fractional rule is proved
under its assumptions but is not the fixed-cutoff policy tested here.

The preparation package is organized as follows:

- [Final study results](lbesh-study-results.md), including denominators,
  ablations, references, repeated timings, and retained negative findings.
- [Claim and evidence register](lbesh-claim-evidence.md),
  [theory](lbesh-development-theory.md), and
  [literature positioning](lbesh-development-literature.md).
- [Independent scientific review](lbesh-final-publication-review.md),
  [numerical review](lbesh-review-results.md), and
  [NLP-disabled diagnosis](lbesh-nonlp-ablation-diagnosis.md).
- [Reproduction instructions](../code/minlp_solver_lab/LBESH_RESEARCH.md),
  [frozen study protocol](lbesh-study-protocol.md), and
  [development and verification log](lbesh-development-log.md).

Writing should center on the matched policy comparison and its limitations.
The scalar and multidimensional diagnostics explain a geometric mechanism;
they do not prove that representation sensitivity caused every GDP timing
difference. Broader application claims, a new fractional policy, or a more
robust separation-only implementation would be further research topics.
