# Stage 1, round 1 — independent reviewer 1

Reviewed snapshot: `paper-power-flow/process/snapshots/stage01-round01`.
Scope: the entire frozen stage-1 manuscript, bibliography, checker, source coverage map, README, process file, and manifest. I did not read other reviewers' reports. AC results and the full introduction are intentionally deferred and are not omissions in this assessment.

**Assessment: no major issue found. One minor statement-direction inconsistency requires correction.** The resistive hardness reduction is mathematically sound under the explicitly defined input model. I found no counterexample or missing feasibility implication.

## Required finding

### R1-1 — Minor: identify the direction of the rational homeomorphism consistently

**Location:** `sections/02-resistive.tex:207–214`, Proposition “Preservation of the solution set,” compared with the restriction map explicitly called a bijection in Lemma “The complete network and proof of equivalence” at lines 167–169.

**Problem:** The lemma identifies the restriction map from the network solution set to the source solution set as its bijection. The proposition then refers to “The bijection of Lemma…” and says that its *inverse* is the coordinate projection. Taken literally, the inverse of that lemma's specified restriction map is the extension map, not the projection. The proposition's proof uses the other orientation. The mathematical fact is correct, but the statement leaves the direction inconsistent.

**Suggested correction:** Introduce the feasible voltage set `T_Φ` and say, for example, “The extension map `F:S_Φ→T_Φ` constructed in Lemma … is a homeomorphism with rational coordinate functions. Its inverse is the coordinate projection onto the buses `X_x`.” Alternatively, explicitly call it “the inverse of the restriction bijection” in the first sentence. No change to the construction or proof algebra is needed.

## Correctness audit

- **Source problem:** I independently read the archived original art-gallery PDF's page 11 using `pdftotext -layout`; Definition 5 allows exactly `x=1`, `x+y=z`, and `xy=1` on `[1/2,2]`, with variable names drawn without distinctness conditions. Theorem 7 states existential-real completeness. This confirms the manuscript's version-specific citation and normalization `x=1 ↔ x²=1` on the positive interval. I also checked the cited complexity discussion in *Dynamic Toolbox for ETRINV*, pp. 1–2. I read and followed `literature/AGENTS.md` and made no literature changes.
- **Membership:** Each original bus equation is quadratic, there are linearly many incident terms, and rational denominator clearing has polynomial bit length. The stated inclusions and conditional NP consequence have the correct direction. The manuscript correctly avoids inferring nonmembership in NP merely from irrational solutions.
- **Copying and fan-out:** A degree-two pinned bus enforces `a+b=5/2`. Successive complementation is an involution of the source interval. The endpoint allocation rule uses at most two extensions for every requested slot, including repeated names within one equation. Subsequent path extension does not make a previously allocated value bus exceed degree three. Unused named variables are retained.
- **Addition:** Expanding the pinned equation yields residual `z−x−y`. The distinct-copy allocation avoids parallel edges when names coincide. Equations such as `x+y=x` remain infeasible because all source variables are positive.
- **Inversion:** The original equations at `C_I`, `I`, and `D` respectively imply `v_I=x`, `v_W=2x−1+1/x`, and `y=v_W−2x+1`. The division is valid throughout the box. Substitution in the reverse direction satisfies all three equations. The auxiliary voltage range is `[2√2−1,7/2]`, strictly inside `[1,4]`. No free bus imposes an additional equation that would invalidate the reverse direction.
- **Full graph:** Fresh gadget buses and distinct requested buses ensure simplicity. Every degree and conductance claimed in the theorem follows from the explicit incidence description. The bound `|P_i|≤4·3·2·(7/2)=84<85` holds on the whole prescribed box and therefore genuinely makes every designated free injection redundant.
- **Both directions and uniqueness:** Every feasible target assignment determines a bounded source assignment through the roots, and the copy constraints and original gadget equations enforce every source relation. Conversely each source assignment has the displayed feasible extension. All auxiliary voltages are forced. Empty source sets, an empty instance, and isolated unused coordinates introduce no exception. Rational continuity follows from strict positivity of the denominators.
- **Size:** Three requests per normalized equation produce at most six path extensions, hence at most twelve path buses and twelve path lines. An inversion adds four buses and six lines. The theorem's `n+16m`, `18m`, and polynomial encoding bounds are correct, including normalized constant equations.
- **Model scope and physical interpretation:** The model explicitly allows singleton voltage/injection intervals and buses with interval injections, and does not assert a conventional fixed-slack or load-only restriction. The signed-injection and dissipation discussion is consistent with the equations. There is no implicit zero-loss balance condition.

## Reproducibility and presentation

I independently verified every SHA-256 entry in the frozen manifest and built the six-page manuscript using `latexmk`, with its output confined to my verification directory. The final LaTeX log has no unresolved citation/reference warning or overfull box warning. The checker passes with **12,751 exact original-network profiles, including 606 source solutions**.

The checker tests canonical extensions and original injection residual identities, including nonsatisfying assignments, repeated names, high fan-out, endpoints, free bounds, graph properties, and dissipation. It does **not** search all target voltages or prove infeasibility, and its docstring and output explicitly avoid claiming that. Universal reverse-direction correctness rests on the proof, which I checked separately above. I found no test-scope overclaim.

Artifacts: `paper-power-flow/verification/reviewer1/stage01-round01/` contains the isolated build, the frozen manifest check, exact-check output, and extracted original-source page 11.

No optional stylistic preferences are being promoted to required revisions.
