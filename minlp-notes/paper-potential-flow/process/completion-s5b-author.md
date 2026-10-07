# S5b author handoff: correlations, dissipation, and rational feasibility

Status: author work complete and frozen for the required five independent reviews. This is not stage acceptance. No reviewers were spawned by this author. Work was confined to the potential-flow worktree; no commit was made, Paper B was not edited or built, and managed literature stores were not changed.

## Delivered scope

The new `complexity/sections/09-correlations-energy.tex` has 872 lines and is integrated immediately after `08-design.tex`. Only `complexity/main.tex` and `complexity/references.bib` differ among previously accepted build inputs; every accepted section 01–08 retains its accepted S5a hash. The bibliography additions are Lobo et al. (1998), Raber (2022), and Shannon–Hagelbarger (1956). The entire build-input hash map is in `completion-s5b-build.json`.

The section supplies standalone proofs for all four requested promoted results and the shared-cycle note. It uses explicit cross-references to the accepted cactus capacity LP and SRS reductions rather than repeating those proofs. No mathematical theorem depends on an unpublished repository note or companion paper.

| Manuscript label | Content |
| --- | --- |
| `ex:a-corr-shared` | Shared two-cycle curved image, exact missing midpoint, unique interior linear-flow maximum, positive unit-weight interpretation; no hardness claim. |
| `thm:a-corr-hardness` | Actual-resistance bounded-coefficient Max-Cut polytopes, paired triangles for all-edge total flow, paired prefix bridges for minimum dissipation and prescribed unit-transfer potential drop, exact graph counts and cut identities. |
| `eq:a-corr-cut-flow`, `eq:a-corr-cut-energy` | Exact optimum identities; rational dyadic thresholds, constant 7/512 decision gaps, unary bounds, restricted NP/coNP membership, 1/256 value and rational scenario-output hardness. |
| `thm:a-corr-energy-max` | Any-graph maximum dissipation, direct Fenchel equality proof, exact two-SOC lift including zero cases, compact optimizer bounds, rational affine-hull reduction and relative-interior center, explicit polynomial-bit inner/outer radii and globally Lipschitz objective, Dadush exact feasible rational output, original-profile recovery. |
| `cor:a-corr-energy-capacity` | Exact cactus capacity composition, including lower-dimensional filtered polytopes and singletons; explicit classical cycle-linearization credit. |
| `prop:a-corr-certificate` | Exact original-instance global design certificate, arbitrary potential gauge, LP-dual global upper and Fenchel chosen-profile lower bounds, exact zero-gap triangle and implementation limits. |
| `prop:a-corr-irrational` | Ordinary positive-width upper-capacity rank-two SP instance forces irrational resistance; full state, bounds and irreducibility; smaller equality example, filtered-hull failure, precise rank and output distinction. |
| `thm:a-corr-lipschitz` | High-circulation-cycle proof of the all-graph linear resistance bound through zero and reversing flows, extended to directional coefficients. |
| `prop:a-corr-sharper` | New fourfold sharper coefficient perturbation bound, proved by regularized electrical sensitivity and endpoint compact limits. |
| `cor:a-corr-strict-margin` and following paragraphs | Box rounding and witness-size bounds, new rational-polytope extension, conditional recovery from an approximate center versus initial feasibility search; pressure bounds and gauge. |
| final subsection | Nonconvex upper-pressure triangle and exact lower-pressure conic extension, with degenerate-boundary rational-output limitation. |

The term dissipation is expressly the constitutive quantity `sum beta |x|^3=b^T pi`, not literal compressor power. The section does not turn fixed absolute-error hardness into relative-error, normalized-objective, fixed-rank, or delivered-throughput hardness.

## NEW developments requiring explicit review by every reviewer

1. **Directional extension of the elementary all-graph bound.** The reorientation by the flow difference swaps old and new directional coefficient pairs, preserving their bounds and maximum change. For positive circulation increment, the new directional law increment dominates the beta_L-scaled symmetric increment on same-sign and sign-crossing branches. The residual at fixed flow is at most delta times its square. This establishes the existing `2mM delta/beta_L` estimate for independent directional coefficients, including zero and reversed flows.
2. **Fourfold strengthening proposed during the lead audit and fully developed by the author.** Proposition `a-corr-sharper` proves `||Delta x||_infinity <= M/(2 beta_L) sum_e q_e <= mM delta/(2 beta_L)`, where `q_e` is the symmetric coefficient change or the maximum of the two directional changes. The proof adds rho times flow, uses joint C1 implicit differentiation in cycle coordinates, derives the single-edge response `(d_e/r_e)(j^(e)-1_e)`, establishes its unit electrical-flow bound directly, and integrates. Only convergence at the two endpoints as rho decreases is needed; it follows from compactness and variational optimality, including zero flows. Neither an optimal constant nor novelty of electrical sensitivity itself is claimed.
3. **Strict-margin witness size on an arbitrary bounded rational positive coefficient polytope.** A rational dyadic center near the unknown strictly feasible real profile defines a small rational box meeting the polytope. A vertex of that intersection has polynomial bit length and remains physically feasible by the sensitivity bound. This extends the size/existence conclusion beyond boxes without claiming coordinatewise rounding preserves correlations or finding the unknown initial strict design. Recovery is polynomial if an adequately accurate center is supplied.

The conservative original rounding and pressure constants remain valid and explicit. The larger half-slack radius implied by the improved bound is also stated. All conic maximum-energy and hardness results retain symmetric quadratic laws; the directional development is confined to sensitivity and its consequences.

## Primary-source inspection and limits

The author read the four full promoted result statements, the shared-cycle supporting note and its review, the total-flow and energy derivation stubs, both mathematical reviews for each hardness result, both maximum-energy reviews, the operating-constraint investigation and review, the certificate-code audit, and the three focused correlation/energy literature assessments. The accepted definitions and Section 8 capacity/design results were inspected for integration. Notes are supporting evidence, not substitutes for manuscript proofs or priority clearance.

Primary passages inspected directly in this author turn:

- Dadush, *Integer Programming, Lattice Algorithms, and Deterministic Volume Estimation* (2012), Theorem 2.5.9, printed p. 48 / PDF p. 61, and adjoining computational conventions: centered convex body, weak membership, globally convex Lipschitz value oracle, rational point **inside** the body. Open primary URL: https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf. This is the precise output theorem invoked; the manuscript supplies every instance-specific radius and bit bound.
- Lobo, Vandenberghe, Boyd and Lebret (1998), Section 2.3, printed pp. 199–201 / PDF pp. 7–9: rational hyperbolic cone identity and geometric-mean construction. Open author copy: https://web.stanford.edu/~boyd/papers/pdf/socp.pdf. The two-cone construction is credited as established.
- Raber (2022), title page and Theorem 3.12, printed pp. 34–35: continuity in all positive resistance parameters for fixed nominations, via the compact parametric energy problem. Read from the local extracted primary thesis `literature/external-potential-flow-reopened/raber-2022.txt`; original PDF is adjacent. Open source: https://d-nb.info/1258349914/34. The new statements are explicit quantitative bounds, not a claim to originate continuity.
- Aßmann, Liers, Stingl and Vera, arXiv:1808.10241, Section 4.3.3, Proposition 4.9, Lemma 4.10 and Proposition 4.11, PDF pp. 20–21: cycle-root interval equivalence and affine coefficient restrictions. Open primary PDF: https://arxiv.org/pdf/1808.10241. The cactus composition is attributed to our already proved `a-design-global-capacity`, avoiding ambiguity that the original source itself proves the whole cactus theorem.
- Klimm, Pfetsch, Skutella and Strubberg, arXiv:2604.26882v1, Corollary 4, PDF pp. 7–8; Remark 8, PDF p. 12; and Theorem 11 with its discretization setup, PDF p. 18. Open source: https://arxiv.org/pdf/2604.26882v1. The comparison preserves conductance coordinates, installation/investment objective, and the condition that **all** variable conductance costs are positive. The author does not rely on Theorem 13; the lead reported an apparent printed algebra issue in one of its reductions. An incidental broad design-hardness sentence was removed, and no claim is made about that unneeded proof.
- Groß et al., *Algorithmic Results for Potential-Based Flows*, Section 3, equations (7)–(8) and the nearby KKT discussion, PDF p. 7: classical primitive energy and homogeneous conjugate duality. Open primary PDF: https://optimization-online.org/wp-content/uploads/2017/08/6185.pdf.
- Del Pia, Dey and Molinaro, *Mixed-integer Quadratic Programming is in NP*, Section 1.1, Corollary 2 proof, PDF p. 2: unweighted cut decision and its binary quadratic encoding. Open primary PDF: https://arxiv.org/pdf/1407.4798.
- Shannon and Hagelbarger (1956), *Concavity of Resistance Functions*, entire original two-page article reproduced photographically in *Collected Papers*, printed pp. 784–785 / PDF pp. 816–817. Read `/tmp/paper-a-shannon-collected.txt` lines 40593–40705 and visually inspected `/tmp/paper-a-shannon1956.png`. The displayed theorem and equation (1) establish joint concavity for linear two-terminal resistances. The author spelling is **Hagelbarger**. Original journal metadata: *Journal of Applied Physics* 27(1), 42–43, DOI 10.1063/1.1722193. The lead retrieved the open collection at https://www.jonglage.net/theorie/notation/siteswap-avancee/refs/books/Claude%20Shannon%20-%20Collected%20Papers.pdf; ordinary download succeeded although web opening the large file failed.

No new exhaustive priority search was performed. Older literature assessments include sources inspected only by abstract and an unread Hasler–Wang nonlinear-tolerance paper; none supplies a theorem dependency or unrestricted first-result claim in this section. The new sensitivity refinements use classical electrical differentiation and elementary compactness. Their precise constants and scope must be reviewed, not treated as novelty established by numerical checks.

## Verification and implementation boundary

`completion-s5b-checks.json` records every command, exact stdout and stderr, return code, elapsed time, script hash, hashes for all potential-flow Python dependencies, and the saved certificate hash. All 13 commands passed under `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python`:

- Total-flow numerical checker: 1,197 complete positive DAG states, 192 exact rational threshold gaps, 63 comparison graphs; largest physical residual `4.90909e-91`.
- Independent exact total-flow checker: 71 actual cacti, 1,068 exact physical profiles, 205 rational thresholds.
- Minimum-energy checker: 1,197 energy/pressure states, 192 exact rational threshold gaps, 63 paired-bridge cacti; largest local identity residual `3.68182e-91`.
- Maximum-energy exact checker: 180 projected cone cases, 1,080 necessity controls, 84 exact complete-graph states, 1,008 conjugate/cone witnesses, five interior constructions.
- Certificate audit checker: 99 exact certificates, 99 accepted gauge shifts, 151 malformed direct inputs rejected, 294 corrupt normal/optimized CLI files rejected.
- Numerical SOCP producer: six instances, all statuses `optimal`; **largest independently certified rational dissipation loss `2.732138286840706e-05`**. This gap is the achieved guarantee, not the solver tolerance.
- Saved triangle certificate: lower and upper `3/4`, selected lower `3/4`, exact suboptimality `0`.
- Ordinary-capacity/equality irrational examples and pressure/scalar checker, normal and `-O`: 1,369 exact scalar cases per run, full original algebraic states and interval/irreducibility checks passed.
- Independent operating-constraint checker, normal and `-O`: 5,329 scalar pairs, 350 high-flow circulations, 441 exact physical perturbation pairs including zeros/reversal; it also reruns the preceding checker under both Python modes.
- New `verification/check_s5b_sensitivity.py`, normal and `-O`: 3,150 directional scalar cases; 441 exact common-nomination physical pairs, including 200 strict sign reversals and 41 zero-endpoint pairs; 102 exact electrical response calculations, including 24 zero-flow responses; 12 simultaneous differentiated states. All passed. The checker uses unconditional exceptions so optimized Python does not disable validation.

These finite diagnostics do not prove universal mathematical bounds or global complexity statements. The numerical scripts produce states or certificates for selected families. Exact verifiers prove their encoded rational/algebraic facts and certificate gaps, not the existence of a general numerical producer. The conic implementation is not an implementation of the polynomial-bit centered-body algorithm. The certificate verifier accepts any potential gauge; its manuscript hypotheses were aligned with that valid implementation behavior.

`build_and_check.py` was imported and only `build('complexity')` was called. The final build has zero errors, undefined references, undefined citations, duplicate labels, and overfull boxes. Intermediate formatting defects were corrected before this freeze; the recorded JSON is the final passing build. No Paper B build was invoked.

## Frozen files

- `paper-potential-flow/complexity/sections/09-correlations-energy.tex`: `51b97d72b27619fa890ec977d9c9166beb5ee0c933edb3f29fa5df348e950f13`
- `paper-potential-flow/complexity/main.tex`: `381a2a85cbf1851ddb17e26f00b83f6978772b10da70e89ffe13dccc61e536ca`
- `paper-potential-flow/complexity/references.bib`: `f11d56b36dcffb3c9da8740ffebf7751edc18f35a9ffc1f16901fe9ffc3d719f`
- `paper-potential-flow/verification/check_s5b_sensitivity.py`: `5079f21df2e35aae67ce9ae068d3a91b2f6bb2a8e6dc971c32831cca8f4005ef`
- `paper-potential-flow/process/completion-s5b-build.json`: `ebda46d9626313f0d01b5ad9b6ae3193b237752ac4116818cae67f93e808672a`
- `paper-potential-flow/process/completion-s5b-checks.json`: `071806d92dc6e70e4a79149667e89653ac6fe79031afe78995917fdf8e07d4b9`
