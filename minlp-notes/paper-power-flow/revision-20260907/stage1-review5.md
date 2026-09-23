# Stage 1 independent review 5

Verdict: **No major issues; one minor correction.** The revised introduction identifies a credible central contribution, gives a useful result map, and makes substantially careful comparisons with the relevant physical models and mathematical tools. This verdict concerns the frozen Stage 1 introduction and bibliography and their consistency with the manuscript; it is not a completed independent audit of every electrical gate proof.

## Scope and independent checks

Read the entire frozen introduction and bibliography, the author report and literature audit. Checked the foundation/model/source-problem definitions, the AC encoding and transfers, structural construction, algebraic statements and proofs, arithmetic appendix, and residual-family/separation statements and proofs against the introduction. No other Stage 1 reviewer reports were read. No manuscript files were edited or subagents used.

Independently inspected primary-source extracts for Bienstock–Verma (model at the start and Section 1.3), Lehmann–Grastien–Van Hentenryck (model and star hardness), Jeeninga–De Persis–van der Schaft (model, contribution statements and Theorem 3.22), Dynamic Toolbox (Theorem 1, rational-equivalence definition, Lemma A and its Boolean preprocessing), Mareček–McCoy–Mevissen (Theorem 1 and Corollary 2), Bienstock–Muñoz (Theorem 7 and Corollary 8), Farivar–Low (Theorem 2 and the recovery discussion), Jafarpour et al. (Theorems 3.6 and 4.1), and Jeronimo–Perrucci–Tsigaridas (Example 13). The latter extraction loses exponent typography, so I relied only on its clear repeated-power construction and explicit double-exponential conclusion, not a newly transcribed exponent formula.

Fresh searches included `"power flow" "existential theory of the reals"`, `"power flow" "universality" feasibility`, `"resistive power" "hardness"`, `"power flow" "R-complete"`, `"power flow" "ETR"`, and `"Exact Feasibility" "resistive"`. Results were mostly noisy and did not reveal a competing restricted-resistive existential-real theorem. This is not proof of priority. Primary online records independently corroborated [Jafarpour et al.](https://epubs.siam.org/doi/10.1137/18M1242056), [Delabays et al.](https://arxiv.org/abs/1512.04266), [Mareček et al. v2](https://arxiv.org/abs/1412.8054v2), and [Bienstock–Del Pia–Hildebrand](https://arxiv.org/abs/2011.08347). The manuscript's qualified and model-specific novelty sentence is consistent with the available evidence.

## Required minor correction

**R5-1 — A pinned voltage alone does not impose the stated affine constraint.** Locator: frozen `sections/00-introduction.tex:46`, “A voltage-pinned bus imposes an affine relation on neighboring voltages.”

The construction requires both a prescribed nonzero voltage and a prescribed injection to impose an affine equality. If the injection is free within a redundant interval, pinning the voltage alone imposes no such equality; the manuscript's own connecting buses provide that case. The complete paper explains the distinction correctly later, so this is a minor local imprecision, not a reduction error. It matters in the proof-strategy summary because simultaneous voltage/injection pinning is also the key model distinction from some prior resistive feasibility work.

Proposed correction: “A bus with prescribed voltage and injection imposes an affine relation on neighboring voltages.” This also surfaces the essential model choice earlier without adding a new paragraph.

## Substantive assessment

- The opening singles out the solution-preserving electrical arithmetic realization and simultaneous graph/data restrictions. It does not treat a list of secondary corollaries as unrelated headline discoveries. The interpretation of existential-real completeness and the open NP-versus-ER separation is sound.
- The contribution map matches the actual theorem scopes. In particular, it does not attribute planar/unit-conductance restrictions to the quantitative residual family, and it correctly distinguishes rational equivalence for compact basic closed sets from semialgebraic homeomorphism for arbitrary compact semialgebraic sets.
- The AC comparison credits winding and angle recovery, and identifies the actual additional step as a rational polynomial encoding of branch choices and zero winding. The frozen crossing-count/lift construction supports that description, including negative rational cosines and unequal magnitudes. The fixed and shrinking-angle conventions remain distinct.
- The earlier AC hardness rows concern different physical restrictions, and the prose explicitly prevents an inference that the new result subsumes lossless fixed-magnitude hardness or gives hardness on resistive trees. The table is selective but not inaccurate.
- The comparison with Gan–Low and Jeeninga et al. states the material independently prescribed operating constraints rather than claiming that signed demands are new. It does not conflate a matrix characterization or exact relaxation with a polynomial-time exact Turing algorithm.
- The Dynamic Toolbox qualification is substantiated: its rational-equivalence definition agrees with the present ratio-of-polynomials interpretation, its Theorem 1 has the broad claimed scope, and the manuscript supplies an independent compact basic-closed invariant and a nonbasic compact example. The conjunction-only construction has the unique-extension and coordinate-recovery structure asserted in the introduction. The text appropriately preserves credit for ETR-INV hardness and arithmetic identities while declining to import the Boolean extension claim.
- The residual discussion credits the general known double-exponential scale and identifies the electrical family and gadget residual transfer as the additional developments. It avoids a general running-time lower bound or an unpromised approximate-feasibility conclusion. The cited Bienstock–Muñoz theorem/corollary locators exist in the local primary arXiv text and concern scaled approximation as described.
- New bibliography entries inspected have matching authors, titles and available metadata. Version-specific preprint citations are justified where theorem numbering or a particular assertion matters.

## Optional presentation preference, not a required issue

The second numbered contribution combines AC semantics and algebraic solution-set consequences. Separate short labels within that item, or a four-part map, might help a reader interested mainly in algebraic geometry. The current ordering is coherent and already supported by cross-references; I do not consider this necessary for Stage 1 acceptance.

## Limits and later-stage attention

The numerical section's existing JPT journal Theorem 1.1 locator should be verified against the journal version or replaced by an explicitly versioned preprint locator during its scheduled substantive stage. This is already identified in the author handoff and is not a new Stage 1 error. Final synthesis should align abstract and conclusion with the reviewed claims and eliminate legacy process wording where present. Nothing in this Stage 1 review justifies claiming that the later proof audit or final manuscript review is already complete.
