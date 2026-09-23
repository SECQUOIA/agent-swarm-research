# Stage 1, round 1: independent review 5

Verdict: acceptable for this stage after two minor clarifications. No major
mathematical issue found in the setting, conjecture transcription, or source
plan. This is not a verdict on the unwritten main proof or consequences.

## Findings

1. **Minor: preserve the cited diagonal theorem's dimension restriction.**
   `sections/01-setting.tex:105–106` says that BDS Theorem 2.12 already gives
   the diagonal certificate characterization, while the ambient setting
   starts with n >= 1. The cited theorem explicitly assumes n >= 2. Add
   “for n >= 2” to this historical attribution. The one-variable extension
   may be elementary, but it should not silently be attributed to that
   theorem. The mathematical claim itself is not refuted by this issue.

2. **Minor: identify the matrices in the DMS PDLC assumption.**
   `sections/01-setting.tex:126–129` mentions a positive definite linear
   combination without specifying whether it is a combination of A_i or
   Q_i. DMS Theorem 2.4 uses the homogenized matrices Q_i. This distinction
   will matter for the planned weaker sufficient condition on A_i. Say
   “under a positive definite linear combination assumption on the
   homogenized matrices Q_i,” and, for a precise summary, mention n >= 3
   and a nonempty proper hull. The existing sentence is an incomplete
   summary rather than an explicitly false theorem.

## Checks and assessment

- Read `PROCESS.md`, the stage author report, coverage map, literature
  record, main file, macros, setting section, and entire bibliography.
  Inspected the coordinator's candidate-investigation record only to
  understand what is intentionally deferred. Did not read other reviews.
- Compared BDS arXiv v2 extracted primary text directly at Definition 2.1,
  Theorem 2.9, Theorem 2.12, Proposition 2.14, and Conjecture 3.3 in
  `/tmp/quadratic-paper-literature/bdsv2.txt`. The conjecture's nonconstant
  formulation is equivalent under nonemptiness, and the zero-inclusive
  multiplier cone introduces no logical discrepancy.
- Independently checked that a nonconstant convex quadratic has a proper
  strict sublevel set; that the strict homogenized set is invariant under
  every nonzero real scaling; and that HHC implies convexity of the full
  image for domain dimension at least three. The stated dimensional bound
  on that last observation is correct.
- Compared the DMS summary with Theorem 2.4 in the local primary full-text
  extraction. This identified minor finding 2.
- Compared the coverage map with all theorem/corollary/section headings in
  the canonical result and the topic references in the corrective audits.
  No omitted development was apparent at the planning level. Historical
  numerical tests are appropriately separated from proof evidence.
- Used web primary records to check Yildiran's abstract and Sheriff thesis
  metadata. The [author's institutional publication record](https://avesis.yildiz.edu.tr/yayin/f6f4caf5-f775-4896-93a2-f095fc4ba068/convex-hull-of-two-quadratic-constraints-is-an-lmi-set)
  confirms the two-aggregation description; the [Harvard record](https://dash.harvard.edu/entities/publication/73120378-b892-6bd4-e053-0100007fdf3b)
  confirms Sheriff, Jamin Lebbe, 2013 and the exact thesis title. A primary
  [Harvard PDF endpoint](https://dash.harvard.edu/bitstreams/620ecf61-bf48-4b50-bbad-918a328d0930/download)
  also appeared with readable text in search and may help stage 3, although
  I did not independently download or inspect its theorem statements.
- Inspected `build/main.log` using a targeted search for warnings, box
  errors, undefined references and output status. The saved build reports
  three pages and no matches for those warning/error terms. I did not rerun
  LaTeX, numerical experiments, project-wide checks, or CI inspection.

The bounded-search novelty language and explicit preprint-version locators
are suitably cautious. The unresolved Kojima–Tunçel closure issue is clearly
deferred rather than imported as an established equality into this stage;
it remains a required later-stage mathematical and bibliographic check.
