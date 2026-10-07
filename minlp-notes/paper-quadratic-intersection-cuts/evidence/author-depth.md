# Depth author report

Owned manuscript files:

- `sections/04-depth.tex`;
- `appendices/B-depth.tex`.

The audit is `audit-depth.md`. No existing research note, review, computation,
macro file, bibliography file or other author's manuscript file was changed.

## Final mathematical scope

The main section has complete hypotheses for finite rays, positive objective
weights and a finite feasible corner bound. The depth guarantee requires no
rank assumption. Its published low-depth expression is the elementary
stronger denominator bound
`2/(sqrt((1+D^2)^2+4D^2)+1+D^2)`, which joins continuously to the original
large-depth expression at one. The original simple low-depth estimate remains
explicitly stated. Depth zero is treated as a supremum result.

The family A/B sharp-order conclusion distinguishes the analytic lower
constant `sqrt(2)-1` from the computer-assisted upper constant `77/50=1.54`.
The appendix gives the complete hand reduction to finite rational leaf
certificates, their format, exclusion arithmetic, coverage argument and counts.
The submission evidence must include their complete machine-readable lists.
Five rational lower witnesses are printed in full, with normalized-coordinate
scope. The independent lower checks use saved fixed heights, without invoking
the numerical height search. The alternative orbit upper bound has a printed
rational dual witness and elementary coefficient bounds, replacing dependency
on the historical root-counting producer.

The fixed-rule guarantees concern Case 4 in the unit bilinear representation,
in its given coordinates. The uncompleted quadratic first-root step is
distinguished from the completed step. The condition-number formulation
requires full row rank; its preceding lower bound does not. The prescribed
condition number/depth example is exact for both completed and uncompleted
rule sets while the full orbit family attains its optimum.

The new contact theorem resolves the former boundary question. Under a unique
support-one contact and strictly positive tangent heights at the other
vertices, closed interval feasibility is equivalent to exactness as a
supremum; strict LP-vertex interval feasibility is equivalent to attainment.
The perturbation lemma supplies one direction. For the other direction,
explicit singular-limit constructions remove the source proof's unstated
full-dimensionality requirement. No family-B contact equivalence is claimed.
The cylinder counterexample is analytic on `0<d<7/128`, with exact uniqueness
and explicit interval separation. The angle counterexample states an A gap,
without implying a B gap.

Raw orbit matrices are `G=F^T`, avoiding the global feasible coordinate set
`X`. The normalized linear ray coefficient is `ell_j`, avoiding the global
cut coefficient `a_j(C)`. Scalar depth widths X and Y retain their meaning.

## Original statements mapped to the manuscript

| Source statement | Final statement or passage | Complete proof location |
| --- | --- | --- |
| Lemma N | `dp:symmetries` | Main proof with explicit matrix congruences, upward-completion transport and depth scaling. |
| Lemma R | `dp:orbit-equation` | First appendix subsection, determinant/trace identity. |
| Normalized frame | `dp:scaled-rays`, `dp:box-proof` | Main scaled-ray normalization; exact coordinates in certificate proof. |
| Centered cylinders and formula (1) | `dp:cylinder`, `dp:cylinder-step` | Main prints orbit matrix and scalar slack/root formula. |
| B membership and closedness | `dp:completion-membership`, `dp:lowering` | Full bounded-lowering/closedness proof in appendix. |
| Theorem A | `dp:depth-bound`, `dp:depth-guarantee` | Complete main proof; improved continuous low-depth branch and original elementary bound. |
| Theorem A Euclidean-depth remark | Paragraph after depth theorem | Vertical projection and diameter comparison, scoped to fixed coordinates. |
| Corollary A' | `dp:grazing` | Complete main discriminant/root proof, explicit D>=1. |
| Theorem B(1)--(2) | `dp:vanishing` | Expansion, unique optimum, transversal root, discriminants, exact depth; matrix fixed and nonsingular. Rounded condition number is calibration, not an exact constant. |
| Theorem B(3) depth lower bound | `dp:vanishing` referring to `dp:depth-bound` | Analytic guarantee. |
| Theorem B(3) fixed-rule step | `dp:fixed-rule-derivation` | Exact min of 2sqrt(epsilon) and z0, including epsilon<=4/9 threshold. |
| Theorem B(4) | `dp:dual-depth` | Printed rational Y matrices; trace identity; elementary polynomial coefficient lower bounds for full parameter interval. |
| Theorem B(5) | `dp:vanishing`, `dp:vanishing-proof` | Analytic completed-family limit proof, with simplified positive-determinant contradiction and explicit S-freeness of singular limit. |
| Theorem B2(1) | `dp:certified-sharpness` | `dp:box-proof`: all completed members, complete necessary conditions and rational facet exclusions. |
| Theorem B2(2) | `dp:certified-sharpness` | `dp:lower-witnesses`: full rational normalized witness, exact epsilon threshold. |
| Theorem B2 best-height comparison | `dp:calibration` | Proved lower comparison distinguished from unproved equality. |
| Theorem B3(1) | `dp:certified-sharpness`, `dp:tangent-family` | Main Cauchy--Schwarz expansion, exact L and depth estimates, ray discriminants. |
| Theorem B3(2)--(4) | Exact upper table in `dp:certified-sharpness` | `dp:box-proof`: four certificates, every positive L. |
| Theorem B3(5) | Exact lower table in `dp:certified-sharpness` | `dp:lower-witnesses`: full matrices/heights, exact individual L thresholds, common L>=17/5. |
| Asymptotic worst-case constants C* | Paragraph after `dp:certified-sharpness` | Defined separately for A/B, monotone limits, analytic lower and computer-assisted upper. |
| Section 3.3 coefficient 56.7 and heuristic 136.707 | `dp:calibration` | Numerical status, exact [136.7,137] distinction. Empirical progression is assigned to computation appendix. |
| Lemma S | `dp:fixed-rule-set`, `dp:fixed-rule-derivation` | Rotation/Sylvester derivation; correct first-root scope; counterexample completed step infinite. |
| Theorem S | `dp:fixed-rule-bound` | Complete main polynomial/spectral proof; full-row-rank qualification. |
| Proposition S2 | `dp:rescaling` | Complete appendix expansion, exact cylinder, fixed-rule step, piecewise condition number. |
| Proposition S3 | `dp:fixed-rule-sharp` | `dp:fixed-rule-sharp-proof`: exact corner/depth/conditioning, attained orbit witness, both rule steps. |
| Fixed-rule representation/rescaling limits | Paragraph after `dp:fixed-rule-sharp` | Unit form and coordinate dependence, no solver-performance implication. |
| Two-variable Case-2 distinction | End of `dp:fixed-rule-sharp-proof` | Exact relative discriminant and scaled-ray conditioning for `fd:fixed-rule`. |
| Theorem C(1) | `dp:contact-set`, `dp:contact-intervals` | Rank-one contact normalization, triangular matrix. B contact only mentioned as a limit on claims, not a B exactness theorem. |
| Theorem C(2) | `dp:interval` | Main determinant roots and trace condition via positive first entry. |
| Theorem C(3) attainment | `dp:contact-intervals` part 2 | Main proof; strict vertex interval membership exactly means PD. |
| Theorem C(3) supremum/strict gap | `dp:contact-intervals` parts 1,3 | New `dp:contact-approx` plus full `dp:contact-proof`; explicit two singular-limit constructions. |
| Theorem C(4) | `dp:cylinder-contact` | Complete main proof, zero denominator/product cases, strict LP-vertex condition. |
| Theorem C(5) | Final main tangent-pencil paragraph | Alpha fixed by zero-height PSD off-diagonal; separate residual diagonal conditions; cross-reference `fd:tangent-pencil`. |
| Proposition C2 | `dp:angles` | Complete main scaling proof using analytic C3 base, states A gap explicitly. |
| Proposition C3 | `dp:cylinder-sharp` | `dp:cylinder-sharp-proof`: exact face minimum, global unique contact, full dimension, interval separation; explicit d range. |
| Section 6.1 near-boundary ratio correction | `dp:calibration` | Preserved exact-check record [0.03052,0.03056], with missing archived full witness caveat; no theorem dependency. |
| Section 6.1 restricted B-search loss | B2 lower witness and calibrated comparison | Printed witness has vertex in its orbit generator; all-B upper supplies <0.22% restriction loss in stated epsilon range. No general completeness assertion. |
| Numerical ray/SCIP/random contact checks | Computation appendix | Empirical validation only; not used to prove analytic claims. |
| Open questions | Discussion handoff to lead | Exact constants, margin dependence, changed rule/Case 2, B interval tests and general minor depth remain open; A boundary question resolved. |

## Reviews and targeted verification

Independent derivation of the depth/cylinder/discriminant claims was delegated
to `depth_check`. It verified the boundary perturbation and proposed the two
singular-limit constructions. Its own independent checker `nr_symmetry`
confirmed those constructions. The lead's independent contact reviewer read
the actual main and appendix proofs and produced `review-contact.md` with no
remaining issue. The independent closure/depth reviewer checked the completed
collapse, the upper certificate reduction, all five lower rational witnesses,
fixed-rule results and C3, and supplied independently verified coefficient
bounds for the alternative dual certificate.

Targeted commands actually run by this author:

- Read-only `cat`, `sed`, `rg --files`, `rg -n`, and `nl -ba` on the owned
  topic's source, reviews, code and saved records. No CI was inspected.
- Inline SymPy expansion of C3's face polynomial and ray determinant.
- Inline fraction-only checking of the five printed saved lower witnesses and
  their exact thresholds: all four checks per witness passed.
- Inline parsing of the five upper compressed leaf records: exact leaf counts,
  completed eight-facet records, prefix-free paths and Kraft coverage passed;
  hashes are recorded in `audit-depth.md`. This check did not replay every
  leaf exclusion. Existing independent leaf-verification receipts were read.
- Inline SymPy verification of the printed alternative dual identity and
  coefficient lower bounds: all exact signs passed. An initial structural
  matrix equality assertion was replaced by elementwise expanded equality;
  the mathematical residual is identically zero.
- An isolated temporary LaTeX document containing only `04-depth.tex` and
  `B-depth.tex`, shared macros and stubs for the two external foundation
  labels was compiled with
  `pdflatex -interaction=nonstopmode -halt-on-error depth-check.tex`.
  The first attempted compile caught a substring-renaming mistake affecting
  omega/alpha/lambda macros; all were restored. A later compile identified
  long display lines, which were split. The final intended topic-only
  compilation passes three times with no warnings or overfull boxes.
- Topic-only inline document checks: 40 unique labels, no unresolved local
  references, both external foundation references identified, no malformed
  macros and no trailing whitespace in the four owned files.

No numerical experiments, solvers, search producers, project-wide
verification, external literature searches, CI checks or git-state mutations
were run. The isolated PDF is only a topic verification artifact in a
temporary directory; the lead owns final manuscript compilation and delivery.
