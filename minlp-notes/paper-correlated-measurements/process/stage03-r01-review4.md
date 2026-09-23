# Stage 3 independent review 4

Date: 2026-09-13. Reviewer focus: the scalar Gaussian-message predecessor reduction, actual primary-source priority comparisons, and broad mathematical correctness of the approximation stage.

I read `literature/AGENTS.md`, both Stage 3 manuscript files, the relevant accepted locality interfaces, and the coverage map. I did not read other reviewers' reports, edit the manuscript, touch the unrelated paper, or spawn agents. Stages 4–6 are outside this gate.

## Verdict

**No MAJOR issue found. One MINOR clarification should be made before acceptance.** The scalar predecessor reduction is mathematically sound in its expressly limited spectral-rounding computational model. The manuscript correctly declines a first scalar-FPTAS claim. The relative-cover claims are proved under their explicit representations and the novelty language is appropriately confined to the combined guarantee.

## Findings

### MINOR R4-1: explicitly distinguish scalar parameter from scalar observation

Location: `appendices/approximation.tex:53–55`, read with `sections/03-approximation.tex`, Theorem `thm:trace-fptas`, item 1, and the scalar predecessor discussion.

“Take the scalar class of Theorem ...” identifies a **scalar observation/noise class**, whereas the theorem expressly permits input-sized parameter dimension. The appendix then uses scalar sensitivities, a scalar artificial parameter, and `1/(1+I)`; its reduction consequently also requires **p=1**. The intended scope is inferable from “single unobservable target,” the formulas, and the subsequent growing-rank-target caveat, so this is not a defect in the argument. It should nevertheless be stated directly where the reduction's assumptions are introduced.

Suggested fix: begin that paragraph with “Take the scalar observation class ... with one parameter (p=1), cardinality only, and 1≤k≤n; infeasible cardinalities and zero signal are handled directly.” The explicit upper cardinality limit also makes the padding used later unambiguous. Preserve the existing distinction that this does not recover the input-sized-parameter weighted-trace theorem or spacing constraints.

## Scalar predecessor verification

I inspected the authoritative local original PDF for Mahalanabis–Štefankovič, arXiv:1209.5991, by a fresh layout-preserving extraction. Relevant source locations are printed pp.13–18 and pp.30–38, especially Note 1, Definition 18/Eq.37, Eqs.39–43, Observation 33, Lemmas 41–42, and Theorem 43. I checked the following directly:

- Theorem 43 has the stated condition-number-dependent runtime and an at-most-budget total posterior-variance objective. It is not literally a theorem about an unobservable focused target. The manuscript appropriately presents restrictions and weights as proof adaptations.
- Eq.39 and Eq.40 really do put the inverse **after** taking the private-coordinate principal precision block. The manuscript's 3/5 versus 1/2 example is correct. The positive local target cost at a singleton bag with empty outgoing separator removes this discrepancy; every earlier private cost has zero target weight. The Schur-complement information messages retain their meaning. Binary bag copies can meet the source's degree-three tree convention without moving the target into an earlier private set.
- Candidate restrictions preserve observed-set witnesses under rounding. For the focused target construction the only nonzero variance comparison is scalar inversion, so no unproved generic weighted-cost identity is needed to rescue the printed private-block formula.
- Dyadic rescaling leaves the model rational and gives the asserted noise and sensitivity bounds. The artificial innovation variance makes latent covariance positive definite even if all original process variances vanish. The bounds on the two triangular transfer norms imply the displayed regularization and condition-number estimates.
- The latent-chain/observation triangles admit the stated width-three decomposition; the Gaussian vertex count is 2n+1. The target posterior identity, lower bound on a best nonempty schedule, choice of alpha, relative-information conversion, and cardinality-only padding are correct. A common nonnegative scalar prior preserves the approximation ratio.
- The distinction between an arithmetic/spectral-net reduction and an explicit rational Turing implementation is necessary and correctly stated. There is no unsupported inference of a rational implementation of the source's spectral rounding net.

## Primary-source contribution audit

I inspected the following actual primary materials, rather than relying solely on the repository's summaries:

- Brown–Laddha–Singh, final *Operations Research Letters* 57 (2024), 107186, NSF-hosted original PDF (`/tmp/correlated-stage03-sources/brown.pdf`), especially Theorems 2–3 on p.2 and the normalization/guess/filter/force construction on pp.3–5. The source does give the broader independence-oracle matroid PTAS, randomization and an accuracy-dependent exponent. The manuscript credits those features and does not claim normalization or multiple criteria separately as new. The browser's new NSF fetch timed out, but the complete original already present locally was inspected.
- Berstein et al., primary author report [Optimization Online, 1725.pdf](https://optimization-online.org/wp-content/uploads/2007/07/1725.pdf), Theorems 1.1/1.3 and Section 4, Proposition 4.2/Lemmas 4.3–4.4, printed pp.14–18. The fixed-distinct-value oracle restriction, pseudo-polynomial represented-matroid algorithm, squared positive minors, interpolation, and witness self-reduction agree with the manuscript's attributions. The product-grid implementation is an equivalent explicit realization, not presented as newly discovered algebraic machinery.
- Indyk et al., primary arXiv:1807.11648v2, Section 6.1/Proposition 6.2 (printed pp.21–22) and Section 6.2: the earlier coreset is explicitly objective independent, followed by fractional budget optimization and criterion rounding. The manuscript correctly credits objective independence and identifies the different integral-object, two-sided-cover quantifier.
- Mahabadi–Vuong2026, complete primary PDF, Appendix C/Definition 32 and Theorems 33–36; I also checked the current [PMLR publisher page](https://proceedings.mlr.press/v300/mahabadi26a.html). The source's distributional replacement and subsequent rounding are accurately distinguished from a 1±eta representative for every target integral matrix.
- The local original Mahalanabis source described above. Its priority consequence is affirmatively developed, not inferred from a search failure or a secondary summary.

I also read the manuscript's explicit lower-envelope, interior-profile, cancellation and finite-field witnesses. Each is mathematically correct and supports the limited distinction actually claimed. I did not conduct an exhaustive literature-absence search, and the manuscript does not purport to prove such an absence. No unchecked source is used in this review as evidence that an earlier theorem does not exist.

## Broader mathematical checks

I read the trace-FPTAS and spectral-cover proofs end to end. The fixed-p normalization is reversible on the exact range, forced owners provide the lower floor, maximum-volume replacement proves coverage, and signed floor residuals yield a two-sided spectral error bound even with variable path length. The dependence on fixed p, fixed contraction promises, exact full-packet feasibility, and characteristic-zero matroid representation is explicit. The matroid proof preserves original rank under restriction and deletion, handles dependent forced owners, and avoids coefficient-cancellation mistakes. The D/E/A and estimable-contrast consequences respect singular ranges and do not claim a multiplicative logdet approximation. I found no major error in these arguments.

The coverage map includes the scalar prior reduction, general-decay and partial-packet trace consequences, growing dimensions, full-packet hardness boundary, DAG cover, represented-matroid extension, criterion consequences and prior-art qualifications. I found no Stage 3 family omitted relative to that map.

## Independent exact checks

New code and output, with no imports from historical producers or reviewer implementations:

- `verification/stage03-review4/check.py`
- `verification/stage03-review4/results.json`

Command: `code/research_20260912/.venv/bin/python paper-correlated-measurements/verification/stage03-review4/check.py`.

Result: **PASS**. Two rational three-time fixtures cover 16 selected subsets, signed transitions, unequal noise/sensitivity scales, an entirely degenerate original latent process, and a partially degenerate process. Exact principal-minor tests check the regularization inequalities, direct joint conditioning checks `Var(target|Z_S)=1/(1+I_+(S))`, and exact inverse sparsity checks confirm every precision edge fits the proposed width-three bags. The accuracy conversion and 3/5 versus 1/2 local-cost witness are also checked. These small instances support the proof audit; they are not a claimed performance experiment or formal verification of the theorem.

The temporary full-text extraction of a third-party original was removed after inspection; only original reviewer code and results remain in the verification directory.
