# Independent depth and closure review

## Verdict

The reviewed depth and closure mathematics passes. No unresolved theorem or
certificate-reduction defect remains. The final claims distinguish positive
and nonnegative costs, limiting values and attainment, unrestricted orbit
parameters and parameters whose generators contain the vertex, and exact
certificates and numerical records.

This review covers `sections/04-depth.tex`, `sections/05-closures.tex`,
`appendices/B-depth.tex`, and `appendices/C-closures.tex`. The support-one
contact approximation and closed-interval theorem were independently reviewed
in `review-contact.md`; their required unique-contact, positive-height and
finite-vertex hypotheses are retained. I additionally reviewed the cylinder
threshold counterexample and angle construction. A delegated reviewer
independently checked both fixed-corner factor constructions and the sharp BP
coefficient claims.

## Findings and repairs

| Severity | Label or location | Finding | Resolution |
| --- | --- | --- | --- |
| Minor | `cl:unbounded` | The parameter in the displayed cost vectors needed an explicit positive range. | The theorem now states `epsilon>0`. |
| Minor | `cl:sdp-certificate` proof | Positive definiteness of the vertex matrix requires interior membership. | The proof now says the vertex is in the orbit set's interior. |
| Minor | `dp:certified-sharpness` | The lower witness is rational in the normalized frame; a general original-coordinate matrix need not be rational. | The theorem now states this coordinate qualification. |
| Minor | `dp:box-proof` | The vertical-line exclusions are asserted for positive-determinant parameters. | The universal exclusion conclusion now refers to admissible normalized matrices. |
| Minor | `dp:dual-depth` | The displayed parameter-dependent matrix is singular at `u=0`. | Its PD conclusion now explicitly states `0<u<=u_*`; the polynomial bounds themselves include zero. |
| High, transient | Depth notation rename | Replacing the substring `a_j` also corrupted the suffixes of `omega_j`, `alpha_j`, and `lambda_j`. | The author restored all six occurrences. Targeted final searches confirm the intended macros. No mathematical change resulted. |
| Minor, final integration | `dp:fixed-rule-sharp-proof` | Renaming the raw matrix also changed the scalar width `widetilde X` to `widetilde G` in one sentence. | The root restored `widetilde X=widetilde Y=vD`; final targeted searches found no remaining `widetilde G`. |

The strengthened small-depth function was reviewed after its introduction.
Its two formulas agree at `D=1`, and its value at zero is one. The simpler
lower bound `1/(1+2D^2)` remains a valid corollary on `D<=1`.

The retained weaker A upper bound now has a complete elementary polynomial
sign proof in the appendix. Its printed coefficient bounds remove a proof
dependency on historical root-counting receipts. The bound remains weaker
than the exact completed-family upper bound, and is described accordingly.

## Depth proof checks

- Finite rays, positive costs and a nonempty feasible corner give an attained
  finite positive corner optimum. The scaled rays cancel objective scaling
  correctly. Every contracted simplex has `q>0`, and its limiting simplex
  has `q>=0`.
- The stated bilinear symmetries transport orbit sets and upward completions
  by congruence and preserve depth. The discriminant claim correctly excludes
  a zero denominator. Constant restrictions and forward grazing are treated
  separately.
- The centered cylinder slack, exit formula, uniform curvature bound and
  large-depth coefficient estimate are correct. The zero-depth limit proves
  equality of suprema and makes no attainment claim. The discriminant-margin
  refinement covers nondecreasing restrictions and both kinds of finite
  forward hits.
- The fixed-ray shallow family has the stated unique feasible optimum and
  depth. The completed-family collapse proof treats invertible and rank-one
  matrix limits separately. Its planar limit plus the upward ray is full
  dimensional; interior persistence justifies passing S-freeness to this
  limit. The two horizontal vertices and the third vertex yield the claimed
  contradictions.
- The finite upper-bound reduction applies to all admissible completed
  parameters, including generators that do not contain the vertex. Its six
  point conditions, bounded lowering intervals, and vertical-line necessary
  condition are correct. The exact determinant-maximum identity was checked
  symbolically. Positive matrix scaling covers eight cube facets; finite
  prefix-free paths with exact Kraft sum one cover their closed boxes. The
  four exclusion rules have the required whole-box signs.
- All five printed lower witness matrices pass their four rational PD/PSD
  tests. The epsilon threshold and all four L thresholds agree exactly with
  the displayed fractions. These are feasible witnesses, not optimality
  assertions.
- The prescribed condition-number construction and pure rescaling
  obstruction have the stated corner values, depth, singular values,
  attained orbit exactness, and completed fixed-rule exits. The fixed-rule
  theorem is correctly restricted to the exact `w-xy<=0` Case-4 representation
  with source constant zero. Its rectangular full-row-rank condition-number
  argument is valid.
- The cylinder threshold example has the printed face polynomial, Hessian
  determinant and ray determinant. The face minimum and homogeneous radial
  bound establish unique contact throughout `0<d<7/128`. Its two interval
  separation inequalities exclude every positive parameter, including the
  common endpoint `t=1`. The subsequent angle rescaling preserves the
  required bilinear family values.

## Closure proof checks

- Strong separation gives the coefficient description for nonempty
  nonnegative coefficient families. The one-cut characterization uses
  strictly positive costs; it does not apply the limiting comparison to zero
  coordinates.
- In the tight-cut theorem, a bounded nonnegative aggregate bounds each slot
  whose limiting weight is positive. Slots with vanishing weights may be
  unbounded, but dropping their nonnegative contributions preserves
  domination. The surviving limiting weights still sum to one. Validity
  forces tightness at every minimizer; affine Caratheodory then gives at most
  N vectors. No boundedness assumption on V is missing.
- Smooth-face rigidity, the full off-support convex-domination criterion,
  the one-unused-ray corollary, and the bilinear support-two regularity
  argument are sound. They concern exactness and do not assert equality of
  suboptimal one-cut and closure values.
- The supporting-face proof of the N-factor gain is valid, including the
  limiting aggregate and its reduction to at most N vectors. Its abstract
  nonnegative-coefficient example attains the factor.
- The three-ray BP bound `a_1>=7/2` has an exact attained endpoint. The
  recession witness gives `lambda_2+lambda_3>=367/759` on the feasible corner
  for every positive inexpensive-ray cost.
- At Wcorner the dominant is exactly `lambda_4>=2`. The integer A certificate
  proves an infinite fixed-corner factor; the explicit B completion gives the
  exact dominant. The new BP congruence exchanges the two horizontal rays.
  Its complete case split proves the sharp coefficient sum and equality
  only at positive scalar multiples of the identity. The auxiliary depth
  lower bound has the necessary range `0<epsilon<=sqrt(2)`.
- The finite-hit factor proposition and the absence of a uniform factor
  across corners follow with their stated hypotheses. The latter conclusion
  applies to BP as well as A and B.
- The three printed support-one sets, all nine certified steps, principal
  minor bounds, explicit dual residuals, and dual objective were independently
  checked exactly. They prove the claimed closure lower bound without the
  sixty-set LP computation. The sixty-set value is correctly identified as
  the value of a finite relaxation.
- The box and coefficient-simplex certificate lemmas give complete
  implications. The appendix specifies every parameter chart, subdivision
  rule, coverage requirement, strict exclusion, distinct-ray rule, disk skip
  condition, and free-coordinate condition needed for the finite upper
  certificates. The printed BP lower-bracket witness passes exact principal
  minor checks. The local-factor facet projections, all six edge minima,
  objective and strict ratio were independently checked exactly.

## Evidence limits and verification record

I read the project instructions, brief and author contract, final main and
appendix fragments, author audits, the relevant source notes, saved exact
records, and the source of both closure checkers. Historical complete-check
receipts were inspected; the large archived subdivisions were not replayed.
The finite proofs require the complete rational records in the submission
companion, whose selection includes the named depth leaves and closure JSONs.

Actual targeted commands were `rg --files`, `rg -n`, `cat`, `sed`, `nl`,
`sha256sum`, and inline `python - <<'PY'` calculations using only standard
library `Fraction` or SymPy for the symbolic/rational checks itemized above.
The final symbolic assertions and fraction checks all passed. Two preliminary
SymPy structural comparisons rejected algebraically equal expressions;
comparison after symbolic simplification verified the identities. No
mathematical counterexample resulted.

No author TeX was modified by this reviewer. No experiment, solver,
certificate generator, archive verifier, numerical replay, literature search,
project-wide verification or CI inspection was run. This report is
independent mathematical review, not a new experimental verification of the
archived large certificates.

The final targeted `git diff --check -- evidence/review-closure-depth.md`
reported no whitespace errors. The actual final TeX snapshots checked are
identified below; integration may subsequently change formatting or references.

| File | SHA-256 |
| --- | --- |
| `sections/04-depth.tex` | `53c43d821a9e9f55cc8db66462a2bcbbb57fef8a5039df45316b9ded0942d40d` |
| `sections/05-closures.tex` | `b6e29be5b051e12957c3f9ec56f1c1189c6addb000f941142aa55299f3f792b8` |
| `appendices/B-depth.tex` | `4d4fac9953d0871f9c346424f5e5599e1779d4acf9e324c279c30a954117ac3e` |
| `appendices/C-closures.tex` | `0e989acc8bd21d1301d83ff70ee9f80e37b247c8012cc99f08ad3d07f334f3d2` |

## Final integration inspection

The final depth notation uses `ell_j` for the normalized linear ray
coefficient and `G=F^T` for a raw orbit matrix. The cost, step and
ray-coordinate macros remain `omega_j`, `alpha_j` and `lambda_j`. The added
explicit cylinder matrix gives the stated determinant inequality and a
strictly positive constant second diagonal entry. The new contact-completion
sentence correctly forces zero lowering at `q=0`. The added Case-2 comparison
has the stated relative discriminant and scaled-ray condition number. The
restricted-generator loss below 0.22 percent follows directly from the
existing exact lower and upper bounds in the stated epsilon range.

The closure appendix's vertical display of the three dual slacks and the
split six-edge table retain every previously checked numerator, denominator
and edge assignment. These changes do not alter the proofs. This final
inspection used targeted `rg`, `sed`, `nl` and `sha256sum`; no arithmetic
certificate or experiment was repeated.
