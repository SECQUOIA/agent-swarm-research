# Integration decisions

## Root review of the first foundations draft

The statement `H_U subseteq P subseteq B_infinity` for every fixed box `P`
is false. The original sublevel hull and a protected fixed box are each
contained in the iteration limit, but neither must contain the other. For
example, take the exact relaxation of `f(x)=0` on `[-1,1]`, cutoff zero:
`H_U=[-1,1]`, whereas `P={0}` is also fixed. Replace the chain by the two
independent inclusions `H_U subseteq B_infinity` and
`P subseteq B_infinity subseteq B_k`. The endpoint ceilings remain valid.

The sublevel-hull proof should take closed hulls of
`S_U subseteq K_U(H_U) subseteq H_U`; it need not claim the original
sublevel points themselves attain every face unless their compactness is
assumed. The foundations assume attainment of the minimum, but have not
assumed continuity of `f` globally. The hull proof avoids that extra premise.

Replace the assertion that symmetry 'defeats' root tightening by the precise
statement that it can prevent convergence to a singleton. Separated
near-optimal points can still permit useful tightening. Extend the non-fixed
limit example to all subboxes by defining its projected objective on
`[a,s]` using `x<=g(s)`; the common framework requires all subboxes.

The fair-schedule equality can be proved without the extra decreasing-family
closedness premise. Partition any fair infinite directional schedule into
finite blocks, each containing every signed direction at least once. If block
end times are `t_j`, the block-end boxes satisfy
`T_U^{t_j}(B_0) subseteq C_{t_j} subseteq T_U^j(B_0)`: every individual
update contains the full Jacobi result on its input, and every complete block
is contained in the Jacobi result on its starting box. Taking intersections
gives the same Jacobi limit for every fair schedule. Decreasing-family
closedness is still needed to identify that common limit as a fixed box.
This is a refinement of the known order-independence argument, not a priority
claim. The simple complete-round sandwich already proves its special case.

The manuscript should use the completed audits, which supersede several
statements in the archived reports. These notes guide integration and review;
they are not manuscript text.

- The boundary result supplies a geometric upper enclosure after a preliminary
  round. It does not prove a contraction of the actual free-coordinate gauge in
  every round. Use the repaired terminal case and the active-width bound in
  terms of the prescribed enclosing scale. `audit-rates.md` supplies analytic
  counterexamples and a complete replacement proof.
- The two-variable rate on arbitrary interior boxes is a two-sided geometric
  bound and a kth-root rate. Exact multiplication occurs on the symmetric
  eigenvector boxes. Do not substitute convergence of successive ratios.
- The residual majorant applies to completed exact Jacobi states. For an upper
  initial residual `r`, the checked inequality `r+Me<=e` gives the after-round
  ceiling `Me<=e-r`. The old prohibition on subtracting an upper residual is
  incorrect under this inequality. An unprocessed or inexact current box is a
  different state. `audit-certificates.md` gives the corrected proof.
- Separate attainment of projected coordinate supports from attainment of
  lifted objective infima. A compact lifted family is a sufficient common
  premise. Projected monotonicity suffices for both box protection and an
  objective-value ceiling; lifted nesting is needed only for literal reuse of
  the same auxiliary coordinates.
- Include the sharp retained-pool face threshold and the full-face threshold
  for a prescribed box. Their value is exact cutoff compatibility. Neither is
  an inexpensive universal predictor or a condition for the existence of every
  possible protected box.
- Prefer the exact signed three-variable stall example to the old random
  observation that the row condition is not necessary. The strongly convex,
  diagonally dominant six-variable example separately disproves those proposed
  sufficient conditions. Both concern the stated termwise relaxation.
- Use the improved graph repair constant `L=1/2048`, giving the proved rate
  bound `1/3` at width at most `1/8`. The old `15/16` bound is valid but weaker.
- The finite strict-violation tests close the complete basis-cover obligation.
  Describe their possible combinatorial cost and do not imply the reference
  code automatically performs them.
- Cost admission needs serial completed operations, or outstanding-work
  reservations. Keep the independent-baseline work model separate from the
  shared-machine experimental timings.
- September's corrected SCIP control/r5 solve counts are 573/563. Use 239
  first-round tightening trajectories. Old time and node summaries retain the
  old success rule; prefer the corrected solve table and unaffected diagnostic
  results. Do not infer typical behavior from the selected slow trajectories.
- The companion now includes every September result file and retained local
  model input, as well as the complete frozen October campaign. It preserves
  original source bytes. Its manifests state the weaker September input
  provenance and external solver/environment dependencies precisely.
- The numerical experimental policy implements current-round screening and
  heuristics, not the stronger protected-box or matrix-tail theory. State this
  once clearly and maintain it throughout the abstract, contributions, and
  results. No additional solves or overall speedup were demonstrated.
- The literature audit supports a narrow contribution claim for the explicit
  shape-dependent expansion, relaxation-specific rates/examples, and finite
  OBBT certificate formulations. Credit the classical mathematical ingredients
  and prior adaptive OBBT methods. Missing source text cannot support priority.

## Findings from independent manuscript reviews

- The archived sequential factor near 0.705 uses a variable-block scheme
  (both signed supports for one variable, then rebuilding). It does not
  establish a rate for the draft's signed-direction sequential operator.
  Remove the numerical claim or identify its separate operator precisely.
- Selective schedules need not inherit a contraction upper bound, but they do
  inherit Jacobi lower enclosures: after m individual updates they contain
  T_U^m(B). Avoid saying they inherit neither kind of bound.
- Current-round witness ceilings should explicitly use a finite nonempty W,
  so every displayed min/max is attained.
- The projected-objective codomain excludes minus infinity; do not invoke
  unbounded-below polyhedral fibers without aligning this convention.
- The actual per-LP time limit has a 1 ms floor. Pilot gain uses accepted
  proposed movement before SCIP integer rounding. Certificate generation may
  require up to 2n endpoint LPs; this is not a mandatory cost for every proposal.
  A history-dependent tangent pool can break lifted order; it need not do so
  in every pair of callbacks.

- Do not present the local sufficient conditions as a dichotomy. A valid
  monotone family can have neither positive-width fixed boxes nor geometric
  contraction; the independent foundations review supplies a scalar example
  with h_next=h*sqrt(1-h), h_k asymptotic to 2/k, and positive-cutoff
  limit epsilon^(1/3). The square-root floor is a conclusion under the
  stated strict-contraction assumptions, not a universal alternative.
- The September detailed timing/node summaries use the original success
  classification and are not corrected reanalyses. Remove affected summaries
  or label that original descriptive convention and its exclusions clearly.
- The lambda-weight example needs a common objective (e.g. v=s) to conclude
  projected-objective monotonicity from nesting of its (x,s) projection.

- Use current independent reviews as integration inputs: review-foundations-r1,
  review-local-r1, review-certificates-r1, review-constraints-r1, and
  review-evidence-r1. Authors are correcting some live snapshots already.
- The basis-region formula gives the gradient of its affine piece, not a
  gradient of the whole support value at a nondifferentiable shared boundary.
- Additional saved-data audit: of104 one-entry known-cutoff histories,97 have
  a completed unchanged first round,3 a capped unchanged first round, and4
  a capped productive first round. Of23 histories with a productive first
  round and unchanged second round,22 completed that second round and1 was
  capped. Do not label all23 as convergence. Counts100 nochange and7 cap
  overlap in3. No solver was rerun to make this distinction.

## Final integration reminders

- Root preflight in /tmp/adaptive-obbt-preflight-2xzef0ml compiled the
  available core and appendices (84 pages before front matter) with no fatal
  errors. Undefined cross-label aliases: prop:quadratic-row-stall should refer
  to prop:quadratic-rows; eq:matrix-lipschitz to eq:order-lipschitz;
  thm:residual to thm:residual-tail. Citation aliases are recorded separately.
  One overfull inline inequality in constraints should become display math.
- Certificates recently removed their duplicate fixed-limit theorem. Align
  cutoff/residual references with foundations eq:closed-family,
  prop:fixed-limit, and lem:sequential, rather than obsolete (L1)/(L2) and
  thm:limit-protected. The generic fixed-limit proof only needs every
  iterated cutoff set nonempty, rather than U>=f* specifically; declare the
  broader form if used for an arbitrary new cutoff.
- Every claimed incumbent-based invariant interval at a node requires that
  incumbent to lie in that node box. A global incumbent outside the box
  supplies a cutoff but does not supply that protected singleton.
- Remove the archived 0.705 numerical directional-rate claims unless a
  matching archived operator or analytic proof establishes them. The existing
  computation uses variable blocks, and main text has repeated this attribution.
  Exact scalar alternative is in review-foundations-r1.md; no numerical rerun
  is needed. New proposed-critical-example.tex has a complete independently
  checked sublinear/cubic-root-floor proof, valuable for the borderline case.
- Supplementary-material provenance must distinguish October frozen inputs
  from September retained inputs. Both studies' original source/results bytes
  are packaged, but September has weaker input lineage. Include precursor
  appendix in main.tex.

## Root dispositions after all first drafts were released

The older cross-label advice above is superseded. Final residual labels are
`thm:residual` and `eq:matrix-lipschitz`; all manuscript labels and citation
keys passed the source check. No additional alias replacement is needed.

- Root qualified the abstract's width/gap conclusions by strict comparison
  factor below one, scoped face stalling to sufficiently small scales, and
  stated smooth-factor assumptions.
- Introduction/discussion/local-rate consequences now allow singleton finite
  certificates and exact termination; tolerance stops are distinguished from
  proving the current box fixed. Closedness is stated for limit fixedness.
- Removed unsupported 'different mechanism' contrast with CLM2016 and all
  negative priority statements about earlier rate analyses. BM2012 gets generic
  convergence-order credit; Scott's monotonicity premises are explicit.
- Completed-round certificate proposition now checks complete lifted points
  on the rebuilt box, matching its counterexample and the reference algorithm.
- September final-solve savings did not offset OBBT cost; October per-run
  1.00501-second figure is an observed maximum, not a hard allowance.
- Cluster and local contraction conditions share a numerical threshold;
  strict and non-strict inequalities are not equated. Round-count formula
  handles zero starting gauge before taking a logarithm.
- Constraints history claim is limited to the scalar boxes of its proved
  construction. Failure to provide a tail bound is not certification of zero.
- Opus foundation review found box-relative five-point tangent rows can
  violate monotonicity even without history and a written overflow-proof gap.
  A new Opus revision task owns foundations/algorithms/front matter to repair
  these, add the useful order-only greatest-fixed-box lemma, and close minor
  findings. The numerical implementation was accepted as valid under its
  cutoff and arithmetic premises; this is a scope/proof correction.

The Opus revision and focused Sol checks completed those repairs. The final
manuscript has the order-only greatest-fixed-box lemma, separate closedness
premises, the exact moving-tangent counterexample, and the complete numerical
validation proof. The base bounded literature audit covers all 37 scientific references;
the separate software citation audit covers nine additional benchmark and
software entries. The final Sol source-integration review closes its
attribution findings. The final submission ZIP builds independently and matches
the 97-page PDF text. The earlier reminders above are historical review inputs;
the accepted reports and REVIEW-RESPONSES.md record their dispositions.

The final focused source-integration review (round 4) accepts all minor prose
corrections and the nine software citations. Both citation audits and the final
literature check are complete. All 14 reviewed source identities match the
released files; verification/package-check.json records the independent build
and verification/artifacts.json identifies the final PDF and ZIP files.
