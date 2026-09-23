# Stage 1 corrections

The correcting author read `stage1-assessment.md` and all five independent
Stage 1 reports. All eight consolidated minor issues are addressed. No
theorem, proof conclusion, or later-stage material was changed.

| Assessment issue | Change | Verification |
| --- | --- | --- |
| 1. Abstract hypotheses | `main.tex` now states the nonnegative bound `max{m-2,0}`, assumes `s >= 2`, and requires a finite repeatable dictionary with a non-ray factor and `B > 0`. | Compared with the universal local lemma and rank-frontier theorem; the abstract no longer includes the ray or interval exceptions in the ceiling formula. |
| 2. Definable contact data | The generic-selection lemma explicitly uses a definable `C^2` patch, the definable normalized outward-normal contact map, and definable local coordinates. The curvature section begins with a definable parametrization. | These are precisely the inputs needed for the stated cell-decomposition argument. |
| 3. Basic definitions | Defined the polar body at the first introduction of `C`; defined `Q_m` before the dimension-resource corollary. | Both definitions precede their first uses and fix the polar normalization and total cone-dimension convention. |
| 4. Restricted-barrier wording | The final foundations paragraph states that ambient rank remains a valid barrier parameter after restriction, but need not be the least such parameter. | This permits equality as well as strict improvement and retains the distinction from an intrinsic barrier bound for the projected body. |
| 5. Norm terminology | The primitive-perspective lemma now says “norm induced by the trace inner product.” | The formula `||w||^2 = <w,w>` and all constants are unchanged. |
| 6. Norm-tree attribution | Added `BTN2001` to the bibliography and cited the original recursive representation in the related-work paragraph and attaining proof. Explicitly excluded that representation itself from the contribution. | Checked the original author-hosted published PDF, Section 2, printed pp. 198–199, equation (5); see source verification below. |
| 7. Polar-degree comparator | The Fawzi–Safey El Din comparison now says algebraic-boundary degree “of the polar body.” | This agrees with the theorem described in the independently checked local source and review 4. |
| 8. Distinct resources | Added an introductory paragraph separating factor count, total cone-space dimension, support-fiber certificate rank, ambient Jordan rank/standard barrier parameter, and the least restricted parameter. It specifies the optimization objective of the main rank theorem. | Read against the later definitions and resource corollary; no resource is identified with a different invariant. |

## Primary-source verification

On 2026-09-20, located and read Ben-Tal and Nemirovski, *On Polyhedral
Approximations of the Second-Order Cone*, Mathematics of Operations
Research 26(2) (2001), 193–205, DOI
[10.1287/moor.26.2.193.10561](https://doi.org/10.1287/moor.26.2.193.10561),
using the [author-hosted published PDF](https://www2.isye.gatech.edu/~nemirovs/Mor-LorentzAppr_2001.pdf).
Section 2 starts on printed p. 198. Its first step introduces binary
generations of norm variables. Equation (5), on printed p. 199, gives the
three-dimensional Lorentz constraints and states their exact projection
equivalence before passing to polyhedral approximations. This verifies the
precise construction attributed in the manuscript. The manuscript's
variable-arity resource matching is proved there, not attributed to a
formula absent from this source. The original local literature package
remains untouched; its prior unread status does not describe this new
online verification.

## Build and final checks

`conda run -n qipm --live-stream make` completed successfully in the paper
directory and produced a nine-page `main.pdf`. The full build transcript
is `stage1-corrections-build.log`. Initial passes reported the newly added
citation pending BibTeX; the final `main.log` and `main.blg` contain no
undefined references/citations, LaTeX warnings, or overfull/underfull box
warnings. `latexmk` reports all targets up to date. The eight corrections
were reread in context, with no additional Stage 1 defect identified.
