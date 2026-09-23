# Stage 1 independent review 4

Reviewed 2026-09-13. Scope: introduction, model/contract, literature evidence, inventory, and bibliography. I inspected `exact_model.py`, the domain and curvature interface in `convexity.py`, `safecut.py`, and the complete checking and master reconstruction paths in `driver.py`, alongside the current replay/soundness notes. I did not edit manuscript or checker code and did not repeat the full historical replay.

## Verdict

**No major Stage 1 issue found.** The mathematical contract is coherent, the main implementation claims match the inspected paths, and the novelty description is appropriately limited to the concrete integration and reliability study. Later proofs, experiments, formalization coverage, and packaging remain later-stage work; their absence is not a Stage 1 defect.

## Valid minor issues

1. **Complete the Coey bibliography record.** The entry `coey2020-outer-approximation-with-conic-certificates` omits volume and page range despite citing the published article. Add volume `12` and pages `249--293`; the author's [publication list](https://juan-pablo-vielma.github.io/publications/index_topic.html) supplies these fields. This is a bibliographic completeness issue, not a substantive positioning error.

2. **Disambiguate “restricted complete VIPR language.”** The introduction's MILP-checker paragraph calls the kernel an implementation of “a restricted complete VIPR language.” Here “complete” describes fully supplied/checkable derivations rather than logical completeness of the supported proof system or complete coverage of VIPR syntax. Although the surrounding manuscript makes the intended meaning recoverable, this phrase creates an avoidable ambiguity in a paper that correctly distinguishes soundness from completeness. Suggested replacement: “a restricted VIPR syntax with fully specified derivations,” or “a restricted subset of VIPR admitting only complete derivations.” Preserve the distinct phrase “complete certificate checking,” whose meaning is expressly defined in Section 2.

## Checks supporting the verdict

- Exact leaf semantics, the coefficient-aggregation counterexample, and the warning about arithmetic preceding extraction agree with `rational`, `exact_repn`, and `exact_sympy`. Original nonlinear subtrees are deliberately retained across zero scaling/cancellation, and domain validation precedes symbolic cut evaluation. This is a defensible loaded-tree semantics claim, not an unsupported claim of source-format equivalence.
- The box-wide domain restriction is stronger than feasibility-domain validity and is acknowledged as such. Half-lines/free variables are represented with missing finite bounds. Support points are checked against the propagated box; singular interval derivative evaluations cannot silently establish cuts. The mathematical subgradient contract is clearly distinguished from the implemented symbolic-gradient route.
- `prepare_model` reconstructs exact affine rows, objective constants/sense, nonlinear rows, and rational propagation. It rejects unsupported active GDP/logical/SOS components and nonlinear two-sided constraints. The paper does not claim a universal convexity recognizer or a general infeasibility pipeline.
- `check_certificate` defaults to full proof checking, regenerates the master, checks VIPR/master correspondence, and requires internal `validate_vipr` success before exposing a finite certified bound. Partial mode cannot expose one. An optional external checker is additional corroboration. These behaviors support the stated trust boundary.
- The primal-witness paragraph correctly distinguishes a feasible master solution from original nonlinear feasibility. Its bound on `U-p*` follows from the finite checked lower bound and the feasible upper witness; equality establishes attainment.
- The introduction does not claim first convex-MINLP certification, first safe cuts, first verified MILP checking, smaller geometric certificates, or solver speed superiority. The comparison with Halbig describes different evidence/checking procedures without claiming a nonexistent distinction between having and lacking certificates.
- I independently opened [Wood et al. v4](https://arxiv.org/html/2312.10420v4). Its introduction expressly separates the Why3 logical encoding from the implemented checking framework and discusses reliance on producer behavior and lifetime attributes in the reference checker. The Stage 1 characterization is fair.
- I independently checked the [primary Szeider CP record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2026.52). Its title, author, 2026 date, volume 379, pages 52:1--52:14, DOI, and black-box-to-rational-VIPR characterization agree with the bibliography and introduction. I found no reason to remove this recent adjacent work.

## Later-stage continuity notes (not revision demands for Stage 1)

Preserve the explicit trusted libraries/runtime assumption when writing executable-checker soundness. State the incumbent-conditioned invariant for the `sol` rule, and do not silently strengthen it to validity of every intermediate row on the full feasible set. Keep the original 299-to-289 cohort selection visible in the experiments and distinguish targeted regeneration from the historical replay. Describe actual formalized theorems rather than treating the existence of Lean infrastructure as formal coverage.
