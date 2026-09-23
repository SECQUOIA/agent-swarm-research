# Stage 1, round 1 — independent reviewer 4

**Assessment: PASS on mathematical substance, with one required minor correction. No major issue found.**

Scope: all frozen TeX, bibliography, checker, snapshot utility, README, and coverage map in `paper-power-flow/process/snapshots/stage01-round01`. I assessed foundations and the resistive reduction; the AC model and later developments are explicitly later-stage work. I did not read other reviewer reports or change the manuscript. I read `literature/AGENTS.md` and changed no literature files.

## Required minor correction

**M1 — State the direction of the homeomorphism consistently.** In `sections/02-resistive.tex:207–214`, Proposition 2.3 calls its map “The bijection of Lemma 2.2” and then says “The inverse is the coordinate projection.” But Lemma 2.2 explicitly defines its bijection in the other direction: restriction from feasible network voltages onto `S_Phi`. That restriction already is the coordinate projection. The proof of Proposition 2.3 instead takes the source-to-network extension as its forward map. All the asserted mathematical properties are true, but the direction is inconsistent. Replace the opening with an explicit statement such as: “The extension map from `S_Phi` to the feasible voltage set constructed in Lemma 2.2 is a homeomorphism whose coordinate functions and inverse coordinate functions are rational over Q. Its inverse is the coordinate projection onto the buses `X_x`.” This is a local clarification, not a gap in the reduction.

## Substantive audit

- **ETR source and citation locations:** I read the archived Art Gallery full text at p.11 and visually checked the original PDF p.11. Definition 5 really has all three forms `x=1`, `x+y=z`, and `xy=1`, with variables in `[1/2,2]`; Theorem 7 states completeness. Coincident names are permitted by its formulation. Normalizing `x=1` to `xx=1` is valid because the interval is positive and does not add variables or equations. The citation deliberately distinguishes the archived STOC/arXiv numbering from the JACM version, avoiding a false journal locator. The Dynamic Toolbox Sections 1.1 and 1.2 at pp.1–2 support the stated complexity conventions and inclusions.
- **Membership and encoding:** Positive finite rational voltage bounds and rational injection intervals produce a polynomial-size system of quadratic inequalities. Clearing denominators atom by atom has polynomial bit complexity. No trigonometric or irrational data enter this stage.
- **Copies and repeated variables:** The tail allocation rule requires at most two extensions per request: zero if the available tail is correct, one if its parity is wrong, two if it is used and has the desired parity. A previously allocated tail can later acquire the second path edge while retaining degree at most three. Never allocating a bus twice prevents parallel gadget edges when names repeat. Unused named variables remain actual free source coordinates rather than being silently discarded.
- **Gadget equations:** The pinned copy equation is `a+b=5/2`; addition gives `z-x-y=0`. For inversion, `C_I` first gives `v_I=x`; the injection at `I` gives `v_W=2x-1+1/x`; the injection at `D` gives `y=v_W-2x+1`. This yields exactly `xy=1`. The conductance-2 edge is incident to the second complemented x copy, consistent across the table, diagram, prose, and new checker. The auxiliary range `[2 sqrt(2)-1,7/2]` is correct, with the minimum at `1/sqrt(2)` and maximum at 2.
- **Completeness and absence of hidden restrictions:** Every nongadget injection is bounded throughout the whole prescribed box by `4*3*2*(7/2)=84`, strictly below 85. The argument therefore does not merely check the intended witnesses; no free-injection bus removes any recovered source solution. The dissipation identity is correct. Every voltage is uniquely specified by the source coordinates; positive x excludes division singularities. The actual solution-set equivalence is sound in both directions, including empty instances and isolated unused variables.
- **Size and fixed data:** Three requests per equation, at most two extensions per request, and two new buses/two lines per extension give at most `12m` path buses and `12m` path lines. An inversion adds four buses and six lines; addition is smaller. Thus `n+16m` and `18m` are valid upper bounds. All bus data belong to the displayed finite sets, all conductances belong to `{1,2}`, and max degree is three. The binary index length assertion is valid for canonical relabeling of variable names.
- **Code agreement:** I compared the new checker with the prior repository construction `code/power_flow_existential_reals/dc_resistive_build_and_check.py` and the reduction in `results/ac-power-flow-existential-reals.md`. The new code uses the same complement-tail allocation and gadget incidence. Its deliberate replacement of individual nonbinding free bounds by the common interval `[-85,85]` agrees with this manuscript. Its residual checks evaluate all original bus injections, including intentionally unsatisfied source assignments. It does not claim to solve general target infeasibility or to replace the converse proof.
- **Consequences:** The NP-collapse and PSPACE conclusions follow from completeness and the stated standard inclusions. The warning that irrationality alone does not disprove NP membership is correct. The stage does not overclaim hardness for load-only networks, trees, approximate feasibility, or AC semantics.

## Reproducible verification

Artifacts are under repository-relative `paper-power-flow/verification/reviewer4/stage01-round01/`.

1. `exact-check.log`: reran the frozen standard-library checker with Python 3. It passed **12,751 exact original-network profiles, including 606 source solutions**. Structural checks cover repeated/unused variables, empty input, residual identities, distinct copies, simple graphs, degree, fixed numerical data, size, and dissipation.
2. `build.log` and `build/`: compiled the frozen manuscript with `latexmk -pdf -interaction=nonstopmode -halt-on-error` into my own output directory. Final build succeeded with six pages and no undefined references/citations, overfull boxes, or other LaTeX warnings in the final log.
3. `manuscript-layout.txt`: extracted and read the compiled manuscript. All main equations, the table, figure references, and citations appear in the PDF.
4. `etrinv-source-p11.png`: independent render of the original Art Gallery PDF p.11, visually confirming source equations and theorem numbering lost in the extracted equations.
5. `manifest-check.log`: verified all ten frozen input SHA-256 hashes against `manifest.json`.

## Optional suggestions

None needed for stage completion. I do not recommend extra numerical experiments or changes to valid constants merely to tighten them. The proof and existing exact regression evidence are sufficient for this stage once M1 is clarified.

Artifact packaging note: the review artifacts were relocated byte-for-byte from the repository-root `verification/reviewer4/` directory into `paper-power-flow/verification/reviewer4/`. Historical command and build logs retain their actual original paths.
