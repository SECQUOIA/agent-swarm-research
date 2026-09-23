# Stage 1, round 1: independent reviewer 5

**Verdict: PASS on mathematical substance; one required minor correction. No major issue found.**

Reviewed the frozen `process/snapshots/stage01-round01` manuscript, macros, references, README, and exact checker. This is a review of foundations and the resistive reduction only; the planned introduction and AC development are outside this stage. I did not read other reviewers' reports or modify the snapshot.

## Required finding

1. **Minor — direction of the bijection is reversed in Proposition 2.3.** Location: `sections/02-resistive.tex:207–214`, compared with Lemma 2.2 at lines 168–169. The lemma explicitly defines the restriction map from feasible network voltages **to** the source solution set as its bijection. The proposition then calls the inverse of that same bijection the coordinate projection, although coordinate projection is the lemma's forward map. The proof instead treats the source-to-network extension as forward. Both maps exist and are rational and continuous, so this does not affect the reduction or the homeomorphism claim. State the orientation explicitly, for example: “The extension map from (S_\Phi) to the feasible voltage set constructed in Lemma 2.2 is a homeomorphism … Its inverse is coordinate projection.”

## Mathematical audit

- **Source problem and membership:** The stated ETR-INV definition, interval ([1/2,2]), repeated variable names, and source hardness agree with Definition 5 and Theorem 7 in the archived original art-gallery PDF, printed p.11. I checked the original PDF's text as well as the knowledge-base extraction. Replacing (x=1) by (xx=1) is valid under positivity. Rational RPF membership uses polynomially many quadratic terms and polynomial bit length; no real-arithmetic computation assumption is hidden in this argument.
- **Complement paths:** A degree-two unit-conductance bus pinned to voltage 1 and injection (-1/2) imposes (a+b=5/2). Complementation preserves the whole source interval. The allocation algorithm needs at most two extensions per request: a used endpoint of the right parity requires two; a wrong-parity endpoint needs one; an unused right-parity endpoint needs none. Extending a previously allocated endpoint raises its degree to at most three. Distinct requests correctly handle all variable-identification patterns, including self-inversion.
- **Addition:** The pinned injection expands to (1/2+z-x-y), so injection (1/2) imposes exactly (x+y=z). Positive-domain equations such as (x+y=x) correctly produce infeasibility rather than needing special preprocessing.
- **Inversion:** The equation at (C_I) forces (v_I=x). The equation at (I) then uniquely gives (v_W=2x-1+1/x). Substitution into the degree-three equation at (D) gives (y=1/x), with the coefficient 2 and injection (-5/2) both correct. The auxiliary voltage range is valid: the minimum is (2\sqrt2-1) and the maximum (7/2). The table, diagram, and algebra agree about every edge and conductance.
- **Completeness and uniqueness:** All fixed equations are verified in the converse direction. Extra currents at value buses cause no unintended equation because their injection intervals are free within the voltage box. The estimate (4\cdot3\cdot2\cdot(7/2)=84<85) establishes this for every box point. Every auxiliary voltage is uniquely determined, so the solution-set result really is a bijection and homeomorphism, including isolated unused variables and empty instances.
- **Size and fixed data:** Each source equation makes three requests, at most six extensions, hence at most twelve path buses and twelve path edges. Adding at most four gadget buses and six gadget edges yields the claimed (n+16m), (18m) bounds. Simple-graph and degree-three claims are correct, and all displayed finite numerical sets match the construction.
- **Consequences:** The conditional NP statement follows from standard polynomial reductions and (\mathrm{NP}\subseteq\exists\mathbb R\). The text correctly distinguishes irrational witnesses from nonmembership in NP and exact feasibility from decimal approximations. The dissipation identity and signed-injection convention agree. No balance equation has been silently omitted from the specified electrical model.

## Verification and presentation

- Independently ran the frozen checker: **12,751 exact original-network profiles; 606 source solutions; PASS**. The checker exercises original graph injections and residuals, not only the eliminated equations. Its finite nature is properly acknowledged; the converse for arbitrary network voltages comes from the proof, not from these tests.
- Built the frozen manuscript with `latexmk` into my own verification directory: six-page PDF, successful final build, no final undefined references/citations or overfull/underfull diagnostics.
- Inspected the rendered inversion diagram and nearby equations. The graph is legible, distinguishes pinned buses clearly, and uses the same neighbor structure as the table. General exposition is sufficient to reconstruct the reduction without consulting repository notes.
- Artifacts are in `verification/reviewer5/stage01-round01/`: checker output, independent build, extracted layout, rendered pages, and the source-definition extract. The archived primary sources used are `literature/papers/abrahamsen2022-the-art-gallery-problem-is/original.pdf` (printed p.11) and `literature/papers/abrahamsen2019-dynamic-toolbox-for-etrinv/fulltext.md` (Section 1.1, pp.1–2). No new external source was required.

## Optional improvements, not acceptance conditions

- The path display in equation (7) uses consecutive mathematical minus signs as edges. A proper horizontal connection symbol would look more polished, although the current meaning is unambiguous.
- When the full introduction is written, preserve the present explicit scope concerning voltage-pinned/fixed-injection buses and general signed-injection intervals. This avoids readers mistaking the theorem for one about more restricted conventional bus specifications. The current stage already makes this distinction adequately.
