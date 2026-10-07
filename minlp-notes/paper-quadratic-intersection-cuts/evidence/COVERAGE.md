# Coverage of the authorized intersection-cut topic

The paper combines the in-scope September and October developments into one
argument. Existing research notes are unchanged. Their mathematical and
empirical claims are corrected or qualified in the manuscript. No essential
proof relies on a research note, a promised future paper, or an unavailable
computational witness.

| Source | Manuscript coverage | Detailed disposition |
| --- | --- | --- |
| `research-20260928b/sfree/optimal-intersection-cuts.md` | Sections 2–3 and Appendix A: unrestricted cuts, attainment, dominant closure, ray support, inertia, algorithms, complexity, Lorentz geometry, rank-one example, determinant orbit, completions, tangent pencils, rational obstructions and wedge. Sections 8 and Appendix F preserve numerical diagnostics. | `author-foundations.md`, `audit-foundations.md`; numerical items in `author-computation.md`. |
| `research-20261001/intersection-literature/note.md` | Introduction and citations throughout: CGF sufficiency, prior free-set/depth selection, quadratic-free characterizations, rotation subfamily, lattice-free closure comparison, solver context. New search narrows the claims further. | `literature-audit.md` and `references.bib`. |
| `research-20261001/ratio-bound/note.md` | Section 4 and Appendix B: invariant scaled depth, improved continuous lower bound, discriminant margin, sharp families, fixed-representation conditioning loss, contact intervals, cylinder threshold, and angle obstruction. | `author-depth.md`, `audit-depth.md`, `review-contact.md`. |
| `research-20261001/orbit-closure/note.md` | Section 5 and Appendix C: coefficient descriptions, finite tight combinations, smooth-face criterion, dimension gain, A/B/BP gaps, support-one improvement, finite and infinite factors, exact certificates and recorded numerical surveys. | `author-closures.md`, `audit-closures.md`. |
| `research-20261001/minor-sets/note.md` | Section 6 and Appendix D: full minor orbit, polar choice, equivariance, parameter dimensions, support and pencil, exact rational examples, bilinear embedding, scaling and principal-minor distinctions. Section 8 and Appendix F preserve numerical comparisons. | `author-minors-convergence.md`, `audit-minors-convergence.md`; numerical items in `author-computation.md`. |
| `research-20261001/multiround/note.md` | Section 7 and Appendix E: exact compact cutting loop, depth/pointedness criteria, uniform step rules, shallow bound-optimal cuts, explicit suboptimal limit and dual ties. Section 8 and Appendix F: paired trajectories, tested policies and limitations. | `author-minors-convergence.md`, `author-computation.md`. |
| `research-20261001/scip-rule-fidelity/note.md` | Section 8 and Appendix F: source formula and numerical conventions, ray comparison populations, corner-oracle corrections, zero-rate faces, rejection and scaling diagnostics, implementation provenance. | `author-computation.md`, `audit-computation.md`. |
| `research-20261001/scip-set-selection/note.md` | Section 8 and Appendix F: actual heuristic direction searches, root cohorts and strengthening, floored-criterion degeneracy, qualified full-solve and debug records, withdrawn uncontrolled timing inference. | `author-computation.md`, `audit-computation.md`. |
| `research-20261001/CLOSEOUT.md`, reviews and certificates | Used to identify superseded claims, then checked against actual proofs and retained records. Complete certificate data are preserved in the companion. | All audit reports; companion manifest. |

The focused author reports contain statement-by-statement mappings, including
source theorem numbers. Process histories and failed searches are evidence
records, not mathematical premises. Binary separation and the three-variable
box hull are different topics and are outside this paper.

## Additional mathematical development

- A closed orbit set containing the optimal simplex can be perturbed to an
  admissible set containing each smaller simplex. This resolves the previously
  open support-one contact boundary case. The closed interval criterion is
  necessary and sufficient for supremum equality under the stated unique
  contact and positive-height hypotheses; strict apex membership characterizes
  attainment. Rank-one limits are handled constructively, with no dimension
  assumption.
- The small-depth lower bound uses its exact denominator, making the bound
  continuous at depth one and retaining the simpler original estimate.
- Three explicit rational cuts and an explicit rational LP dual prove the
  support-one closure improvement `0.99536116`, without depending on the
  archived sixty-cut vertex enumeration.
- An explicit positive definite parameter attains the BP coefficient minimum
  `7/2`, replacing an infimum and numerical-attainment discussion.
- Compact independent face and matrix certificates make the headline bilinear
  and minor examples self-contained. Fine results whose complete endpoint
  matrices were not retained remain reported verification records, rather
  than essential theorem dependencies.
- The elementary wedge maximality proof, explicit cylinder-sharpness range,
  singular-parameter cases, and uniform-pointedness calculation close gaps in
  the source explanations.
- The corner algorithm uses the sharper support parameter
  `min(rank(P), rho(q))`. The efficacy proof supplies an explicit bounded
  epigraph and its inner and outer balls for the weak-oracle reduction.
  An elementary midpoint proof gives `conv(S) = R^3` for the bilinear feasible
  set, so the cone-containment condition is equivalent to positive spanning
  in this case.

## Material corrections and exclusions

- Convexity of the closure of a complement alone does not make it a free set.
  The reverse-convex statement uses a convex open complement.
- Varying an affine apex does not make the plain point rule produce every
  maximal affine free set. The asymptotic-contact quadrant is an exact
  counterexample; the complete free-direction orbit result remains valid.
- Tangent-pencil signs depend on orientation. Both affine and homogeneous
  formulas state their sign conditions explicitly.
- The fixed-rule determinant-root identity applies to the uncompleted orbit
  set; completion membership and exits are treated separately.
- The four-ray lower bound requires `0 < epsilon <= sqrt(2)`.
- A principal-minor halfspace classification requires an indefinite apex.
- The ten antiparallel-ray corner values and the near-boundary numerical ratio
  are corrected. Numeric thresholds and reduced-cost floors remain explicit.
- Corner optimality does not imply full-LP dominance, round dominance, or solve
  speed. These false implications are excluded.
- The actual inside-SCIP experiment searches point-rule directions; it does
  not implement the full orbit-LMI rule. The single-orbit-round intervention
  belongs to the external loop.
- Incomplete closure searches, missing fine-bracket witnesses, the debug
  audit's unresolved diagnostics, and uncontrolled cross-batch timing are
  never promoted to completed certificates or performance conclusions.

## Independent review

Separate reviews cover the contact theorem, corner/orbit foundations,
depth/closures, minor/convergence results, editorial integration, and
literature attribution. `verification/FINAL.md` records the final integrated
document and companion checks. The reviews are internal mathematical and
editorial checks; they do not claim journal peer review.
