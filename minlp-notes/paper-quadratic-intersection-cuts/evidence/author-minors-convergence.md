# Author report: minors and successive cuts

Owned manuscript files:

- `sections/06-minors.tex`
- `sections/07-repeated-cuts.tex`
- `appendices/D-minors.tex`
- `appendices/E-convergence.tex`

The audit, exact-data provenance, and complete proof corrections are recorded in `evidence/audit-minors-convergence.md`. This report maps the final text to all substantive source developments. Existing notes, reviews, code and logs were read without modification. A convergence subauthor independently audited and authored the two `cv:` files; I checked their final text, labels and targeted compilation together with the `mi:` files.

## Numbered results and complete proof locations

| Original ID | Final statement label | Complete proof | Disposition |
| --- | --- | --- | --- |
| minor Prop. 1 | `mi:polar` | Main section 06 | Retained. Canonical signature coordinates and both determinant signs included. Implementation identity distinguished from experimental source fidelity. |
| minor Lemma 2(1)–(3) | `mi:free-cones` | Main section 06 | Retained. Direct conification proof replaces a source-dependent argument. Equation and sublevel corner bounds identified. |
| minor Prop. 3(1) | `mi:orbit` | `mi:orbit-proof` in D | Retained. Full direct maximality proof and positive-scalar uniqueness. |
| minor Prop. 3(2) | `mi:orbit` | `mi:orbit-proof` | Retained. Left/right and transposition parameter identities proved. |
| minor Prop. 3(3) | `mi:orbit` | `mi:orbit-proof` | Retained. Exact point-rule family, dimension, both transformation types and equivariance. |
| minor Prop. 3(4) | `mi:orbit` | `mi:orbit-proof` | Retained. Rotation family and unique positive polar intersection; negative-scalar interpretation disambiguated. |
| minor Prop. 3(5) | Paragraph after `mi:orbit` | Family identities already proved | Retained. All four linear parameter spaces, dimensions and strict apex condition stated. |
| minor Prop. 4 | `mi:certificates` | Main section 06 | Retained. LMIs, monotonicity, SDP size and rational dual test; strict apex-feasible set is positively scale-invariant rather than a zero-containing cone. |
| minor Prop. 5 | `mi:support` | `mi:support-proof` in D | Retained with independent support. Minimum existence and support reduction proved directly, then signature/tangent-quotient argument. |
| minor Lemma 6 | `mi:pencil` | `mi:pencil-proof` in D | Retained. Rank-one nonzero contact, positive determinant tangent direction, pencil determinant and sign included. |
| minor Cor. 7 | `mi:embedding` | Main section 06 and `mi:comparison-certificates` in D | Retained. Slice, bound equality, dimensional limitation, exact selected comparisons and complete embedded witnesses. |
| minor Thm. 8(1) | `mi:examples` | `mi:example-data`, exact face systems/table, `mi:example-proof` in D | Retained. Full dimension, unique cost-one tangent minimizer, KKT and unrestricted attainment via `fd:attainment`. |
| minor Thm. 8(2) | `mi:examples` and `mi:pencil` | `mi:example-proof` | Retained. A's complete pencil and all five exact interval restrictions. |
| minor Thm. 8(3) | `mi:examples` | `mi:example-proof` | Coarse 9/20 orbit upper certificate retained as standalone theorem. Narrower archived orbit/point-rule/rotation intervals and numerical polar value retained in computational evidence, because tight endpoint matrices were not saved. |
| minor Thm. 8(4) | `mi:examples` | End of `mi:example-proof` | Retained. Full-row-rank certificate map proved structurally; positive definiteness survives perturbation; corner-value continuity completed. |
| minor Thm. 9 | `mi:examples` | `mi:example-data`, exact face table, `mi:example-proof` | Retained. S1's support one, strict inactive multipliers, all four transverse products, and portable 779/1000 orbit upper certificate. Tight intervals remain archived evidence. |
| minor Prop. 10 | `mi:contact` | Main section 06 | Retained. Every-minimizer necessary contact condition, exact contact cone and dimension, support-one polar hyperplane condition. Generic measure-zero claim not promoted from heuristic. |
| minor Prop. 11 | `mi:scaling` | `mi:scaling-proof` in D | Retained. Exact all-family bounds and one-variable scaling; numerical rotation asymptotic remains numerical. |
| multiround Lemma 1 | `cv:cone-depth` | Main section 07 | Retained. Cone distance depth, normalized-ray mass proof and full-space rays. |
| multiround Thm. 2 | `cv:uniform-depth` | Main section 07 | Retained. Compact exact loop with nonempty feasibility, closed constraints and persistent cuts; convergence of all accumulation points and objective values. |
| multiround Cor. 3 | `cv:pointed-convergence` | Main section 07 | Retained as a sufficient condition. Uniform pointedness is separate from the depth theorem. |
| multiround Remark 3a | `cv:one-term` | Main section 07 | Retained as explicit corollary. Maximum-distance and maximum-residual cases; no arbitrary selection claim. |
| multiround Lemma 4(a) | Residual-distance proof in `cv:one-term` and after `cv:rule-steps` | Main section 07 | Retained with distinct indices. |
| multiround Lemma 4(b) | `cv:rule-steps`(a) | `cv:ball-proofs`, `cv:scip-definition`, `cv:scip-ball` in E | Retained. Complete analytical Case-4 formula, exceptional directions, closedness, convexity, violated-side freeness and exact box-dependent ball bound. |
| multiround Lemma 4(c) | `cv:rule-steps`(b) | `cv:ball-proofs`, `cv:orbit-ball` | Retained. Both signed matrix embeddings and singular-value ball proof. |
| multiround Lemma 4(d) | `cv:rule-steps`(c) | End of `cv:ball-proofs` | Retained only for idealized uniform θ accuracy, geometric weights, or fixed positive perturbation τ with normalized costs. No implication from absolute bisection tolerance. |
| multiround Prop. 5 | `cv:shallow-optimal` | Main section 07 | Retained with varying-objective scope. Stronger explicit exact ratio-one maximal set, exact depth, distance one and fixed-box embedding added. |
| multiround Prop. 6(1) | `cv:stalling` | `cv:stalling-proof` in E | Retained. Direct maximality and initial-default-set coordinate images. |
| multiround Prop. 6(2) | `cv:stalling` | `cv:successive-halfspaces`, `cv:stalling-rays`, `cv:stalling-pointedness` in E | Retained. Full induction, optimal basis, positive costs, fixed violation, suboptimal limit and explicit uniform-pointedness bound. |
| multiround Prop. 7 (§3.3) | `cv:dual-ties` | Main section 07 | Retained. Exact intercept equality, relative-interior feasible point, supported optimal face and additional zero reduced costs. Scope is the corner LP only. |

## Unnumbered developments and scoped evidence

| Source development | Final disposition and location |
| --- | --- |
| General determinant signature `(2,2)` and equality of rank-one projection with singular locus for four distinct indices | Explicit at the start of section 06. This is the domain of all main minor results. |
| Full homogeneous maximal-set classification versus three-parameter orbit | Prior-work context after `mi:orbit`, citation `MPS2025`. No essential original proof depends on that classification. A's unrestricted attainer proves the orbit can be a proper subfamily. |
| Minor instance B | Full data, face proof, tangent intervals, KKT, portable upper certificate and explicit lower parameter in D. This exactly establishes a smaller gap than the selected second bilinear instance. B's stored tight witnesses were checked directly; computational evidence may retain its narrow bracket. |
| Three embedded bilinear exact brackets | Full embedded data and all six exact witnesses at `mi:comparison-certificates`, with the corner-minimum proofs supplied by foundations. Both-end comparisons are standalone. |
| Narrow A/S1 and point-rule/rotation exact verification intervals | Preserved as archived verification outputs in computational evidence. Missing endpoint witness matrices explicitly recorded in the audit. Coarse complete certificates are used for the headline theorems. |
| Twenty-four rounded-corner strict gaps | Preserved as one-sided archived ratio upper bounds in computational evidence. They are not used to establish a lower ratio or a smaller gap than a bilinear example. Missing full dual retention also recorded. |
| Numerical polar values and scaling rotation `≈4√δ` | Remain numerical and outside essential proofs. |
| Random-minor frequency, LP reoptimization, exact-search construction frequencies, adversarial margin behavior | Computation author owns section 08/appendix F. Selected example comparisons do not imply a general family ordering or comparable-search worst case. |
| Polar formula fidelity and separator defaults/Ipopt guard | Computation author owns implementation and experimental scope. `nlhdlr_quadratic` explicit-minor formula remains source reading without a matching run. |
| Principal positive-determinant trace uniqueness | New explicit numbered statement `mi:principal`, complete main proof. Full singular locus, PSD for positive trace and NSD for negative trace. |
| Principal negative determinant | `mi:other-minors` records the different `(2,1)` signature and cites the established homogeneous characterization; no positive-trace theorem extrapolation. |
| Rank-one PSD projection, NSD halfspaces and domination by at most two PSD inequalities | `mi:other-minors`, prior-work context with indefinite-apex and strict interior hypotheses restored. The source separator need not choose the same test vectors. |
| One-diagonal projection closure and larger forbidden-set-free families | `mi:other-minors`, complete square-root and boundary-limit proof. Bound-aware maximal family optimization remains open. |
| Stalling example's best orbit cut closes the true gap in one round | End of section 07: `C_{sqrt ε}` yields `εx+y≥2sqrt ε`. This reinforces that the adversarial construction is not a failure of the bound-optimal rule. |
| Finite γ observations | Section 07 makes no infinite-trajectory conclusion from finite statistics; computation author reports observations separately. |
| Root tie counts and explanation of trajectory losses | Theory `cv:dual-ties` retained; numerical associations and causal qualifications belong to computation. No theorem claims that ties or shorter steps cause slower loops. |

## Proof and scope corrections

1. Replaced the external essential maximality and conification arguments for minor cones with direct proofs.
2. Made the positive-scalar interpretation of the polar sign explicit. The negative polar cone is not a second point-rule member at the same apex.
3. Supplied minimum existence and independent-support reduction directly, kept the hypothesis on each supported minimizer, and separated tangent directions with determinant zero from the positive-determinant pencil lemma.
4. Supplied fixed exact polar matrices, all feasible face stationary values, complete portable coarse dual data, and the singular-face uniqueness argument. Narrow archived results whose matrices were discarded are kept outside essential proofs.
5. Completed the A robustness proof with a structural rank-four argument and both semicontinuity directions.
6. Distinguished full singular loci, rank-one PSD projections and one-diagonal closures. Independent review caught a draft wording edit that omitted “indefinite apex” from the NSD-halfspace context; that hypothesis is restored.
7. Made every convergence hypothesis explicit, promoted the supported one-term transfer, and proved the default/orbit ball inclusions without depending on source notes.
8. Restricted optimized-rule convergence to a uniform multiplicative θ guarantee with positive fixed τ where required. Numerical bisection accuracy is not that guarantee.
9. Replaced pairwise-angle reasoning for the stalling cones with an explicit separating-vector bound. The objective is fixed in that counterexample; it changes in the local-optimal/shallow example.
10. Removed two unsupported extrapolations: finite small γ values cannot prove `inf_r γ_r=0`, and raw bound-optimal nonconvergence is not known to require flattening. For default and idealized geometric rules, bounded-box step guarantees do make loss of uniform pointedness necessary for a counterexample within the stated exact loop.
11. The stalling choices are images of the initial default set and use a box relaxation. They are not successive default-SCIP choices or a McCormick-relaxation example.
12. Tie forcing applies only to a corner minimizer's support; it neither forces an extra tie for support one nor establishes a causal solver claim.
13. Geometric matrix directions are named `D_edge` in 06/D, preserving the shared plain `D` for scaled vertex depth.

## Open extensions preserved

The remaining mathematical extensions are minor orbit exactness under stronger quantitative conditioning, minor orbit ratios under invariant margin bounds, minor orbit-closure exactness, and bound-aware families for one-diagonal minors. The scaling example excludes an invariant guarantee for the fixed polar/rotation choice and does not settle these questions. The natural default and raw bound-optimal root-loop rules without a verified depth condition remain open. A natural failing rule, rather than an adversarial maximal-set choice, is not supplied.

Practical extensions remain better tie breaking after reoptimization, multiround use inside a solver, explicit-minor nonlinear-handler fidelity, schedules, causality of shorter steps/ties, and cheap look-ahead corner potential. They are retained as extensions, not obligations of an established theorem or positive performance claims.

## Checks actually run

Only targeted checks were run; these results are not CI checks.

- Read `AGENTS.md`, manuscript brief/contract/macros, both source notes, all their completed reviews, relevant corrected closeout text, saved certificate logs and relevant producer code. No experiment or producer was run.
- Standard-library exact fraction arithmetic re-derived the three polar matrices and all 31 fixed face systems per example. Passed: no singular systems, all positive-barycentric stationary values nonnegative, unique stated zeros.
- Standard-library parsing, PD determinant tests and exact matrix multiplication checked 17 retained certificates: six coarse upper tuples, three r1 lower parameters, two B tight endpoint witnesses and six embedded endpoint witnesses. Passed after correcting a parser that initially consumed an unrelated diagnostic line. No numerical solver, search or import of experiment code.
- Targeted temporary-wrapper `pdflatex -interaction=nonstopmode -halt-on-error` initially compiled 06/D successfully and identified one 12.63pt overfull polar-matrix display. Font size adjusted for that display.
- Final temporary-wrapper two-pass `pdflatex -interaction=nonstopmode -halt-on-error` compiled only 06/07/D/E successfully, with zero overfull/error diagnostics. The temporary PDF was 19 pages; temporary files were removed. Foundation references and bibliographic entries remain the lead's integration responsibility.
- The shared-notation rename to `D_edge` initially also changed three capitalized prose words, which the targeted compile immediately caught. Those words were restored. Repeating the same targeted two-pass compilation after the corrected rename passed with zero overfull/error diagnostics.
- Targeted Python structure/reference check on the four owned TeX files: 42 unique owned labels, balanced environments, all `mi:`/`cv:` references resolve. Passed.
- Final targeted whitespace/reference check: six owned TeX/evidence files have clean trailing whitespace; the 42 labels remain unique and all owned semantic references resolve. Passed.
- The convergence subauthor independently checked balanced braces/environments, internal references and clean whitespace. A separate read-only mathematical reviewer checked its two files and found sound arguments after two notation fixes. The root's independent `review_minors_loop` review covers the final four-file text separately.

No project-wide verification, CI inspection, new computation experiment, literature research, background job, or existing-source mutation occurred.
