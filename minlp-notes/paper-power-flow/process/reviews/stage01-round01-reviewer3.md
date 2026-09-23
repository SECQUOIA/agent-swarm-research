# Stage 1, round 1 — independent reviewer 3

## Verdict

PASS subject to two minor corrections. I found no major issue or mathematical gap in the resistive completeness theorem. The AC extension and integrated introduction are outside this frozen stage's scope.

Reviewed snapshot: `process/snapshots/stage01-round01`. I did not read any other new review. Main manuscript sources were not edited.

## Required minor corrections

1. **Direction of the bijection changes without notice.** In `sections/02-resistive.tex:167–169`, Lemma 2.2 explicitly calls the restriction from the feasible voltage set to `S_Phi` the bijection. Proposition 2.3 at lines 207–209 then says “The bijection of Lemma ...” has the coordinate projection as its inverse. For the map actually specified in the lemma, the coordinate projection is the map itself; the inverse is the extension. The underlying rational homeomorphism is correct, and its proof establishes both maps. State the proposition using an explicitly directed extension map `F:S_Phi -> F_RPF`, with inverse the coordinate projection, or call it “The inverse of the restriction bijection in Lemma ...”. Keep that direction consistent with the abstract and subsequent developments.

2. **The abstract omits the verification qualification from the certificate consequence.** `main.tex`, last sentence of the abstract, says “polynomial certificates for exact feasibility would imply NP = exists R.” Polynomial size alone is insufficient; polynomial-time verification is needed. The corollary and surrounding discussion state the correct requirement. Replace the abstract sentence with “Consequently, polynomial-size certificates verifiable in polynomial time for every feasible instance would imply ...”, or a comparably precise formulation. This is a local clarity/correctness issue; it does not affect the theorem or its proof.

## Verification and substantive assessment

- **Physical convention:** Direct derivation from Ohm's law gives the stated net supply `v_i sum_j g_ij(v_i-v_j)`. The sign of the constant-power loads in the complement and inversion gadgets is correct. Pairing the two directed contributions of each edge proves the stated nonnegative dissipation identity. No independent zero-total-injection equation is missing from this lossy network model.
- **Bus assumptions:** The model explicitly allows simultaneous prescribed voltage and prescribed injection, as used by every pinned bus, and broad bounded injections on variable-voltage buses. It states the absence of extra line-flow limits. Thus the reduction does not silently rely on a conventional fixed-voltage source or load-only restriction that the model lacks.
- **Pinned and addition gadgets:** A pinned degree-two bus with injection `-1/2` imposes the complement sum `5/2`. A pinned addition bus with injection `1/2` imposes `x+y=z`. The neighborhoods are insulated from subsequent construction.
- **Inversion gadget:** Independently eliminating the three fixed-injection equations gives `v_I=x`, `v_W=2x-1+1/x`, and `y=v_W-2x+1`. Positive voltage makes division valid. The minimum and maximum of the auxiliary voltage over the complete source interval are correctly calculated. Table 1 and Figure 1 both match these exact neighborhoods and conductances; the figure clearly states that path edges are omitted.
- **Copy allocation and degenerate cases:** The end-of-path allocation rule takes at most two extensions per request, with at most one gadget edge on each value bus. It keeps buses distinct even for all variable-identification patterns. Both impossible repeated-variable additions and the feasible repeated-variable inversion are represented correctly. Unused variables and the empty instance do not break equivalence or the homeomorphism.
- **Free injections and size:** The uniform `84` upper bound applies throughout the voltage box, so the interval `[-85,85]` cannot inadvertently exclude a profile. Six path extensions per equation use at most 12 buses and 12 lines; adding the largest gadget gives exactly the claimed upper bounds `n+16m` buses and `18m` lines. Graph simplicity and maximum degree three follow from the actual allocation rule.
- **Complexity:** Membership is a polynomial-size quadratic formula after clearing rational denominators. The bounded ETR-INV source, normalization `x=1` to `xx=1`, and polynomial encoding arguments suffice for hardness. The certificate obstruction is stated correctly in the corollary. The text does not infer failure of NP membership from irrationality alone.
- **Source verification:** I checked the archived original Art Gallery PDF, page 11, independently using `pdftotext`, including Definition 5's three equation forms and interval `[1/2,2]`, and Theorem 7's completeness statement. Their numbering and version qualification agree with the manuscript. I also read the cited Dynamic Toolbox complexity conventions.
- **Reproducible checks:** Running the snapshot checker returned `PASS: 12751 exact original-network profiles; 606 source solutions.` This supplies finite regression evidence, not the reverse-direction proof, which I checked analytically above.
- **Build and visual inspection:** `latexmk` completed successfully in my own output directory. The final log contains no warning or overfull/underfull box report. I rendered and visually inspected pages 3–4, including the gadget table and figure; labels, incidence, conductances, and layout are clear.

Verification output is under `verification/reviewer3/stage01-round01/` (build log and PDF, rendered pages, and source-definition extraction).

## Optional suggestions

None needed for this stage. Broader physical interpretation and comparisons are already assigned to later stages and are not defects of this frozen draft.
