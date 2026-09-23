# Independent novelty audit: switching-budget CIA

Date: 2026-09-04. Auditor: independent `fbbt` agent. Scope: [uniform-control obstruction and exact continuous one-switch minimax theorem](../results/cia-uniform-switching-obstruction.md), extended below to the [exact arbitrary-total two-switch theorem](../results/cia-exact-two-switch-worst-case.md). Mathematical correctness is covered by separate independent proof audits.

## Assessment

No prior correction of Sager–Zeile Conjecture 1, no published `n=5,N=45,s=1` uniform-control counterexample, and no earlier statement of the exact one-switch coefficient

`max{1/3,(n-1)^2/[n(2n-1)]}`

was found in this search. The counterexample plus the exact replacement theorem is therefore a plausible new result, with a more direct novelty claim than a general application of established rounding theory. This assessment is provisional: it reports what was checked and found, not proof that the literature contains no such result.

The most credible proposed contribution is: **disproof of the published multi-mode switching-budget conjecture, together with the sharp continuous one-switch replacement, its extremizers, and a constructive schedule**. Grid rounding by moving a switch to a nearest endpoint and the general use of integral discrepancy in mixed-integer control are established mechanisms and should not be presented as independent inventions.

## Exact source and the dissertation

Sager and Zeile, *On mixed-integer optimal control with constrained total variation of the integer control*, Computational Optimization and Applications 78 (2021), 575–623, state the conjecture in the final article as Conjecture 1, equation (7.6), printed page 615. The [publisher's article](https://link.springer.com/article/10.1007/s10589-020-00244-5) and [open final PDF](https://www.econstor.eu/bitstream/10419/288496/1/s10589-020-00244-5.pdf) agree with the repository's source. Section 7 concerns more than two modes; the proved sharp analysis in Section 6 is for two modes. Thus the new result must not be described as contradicting the proved two-mode theorem.

Zeile's 2021 dissertation, *Combinatorial Integral Decompositions for Mixed-Integer Optimal Control*, still lists the claim as **Conjecture 7.1** in Table 7.2, printed page 140. The table distinguishes proved bounds from conjectured equalities. Its Section 9.4.3, printed page 170, reports generic random tests with only two or three modes. Those tests do not cover the new five-mode obstruction. These specific thesis passages were available through indexed primary-PDF extracts; a complete fresh local download was unsuccessful, so this audit does not claim to have searched every dissertation page. [Author PDF](https://mathopt.de/publications/Zeile2021a.pdf); [university repository record and DOI](https://opendata.uni-halle.de/handle/1981185920/37645).

## Citation-forward search

An OpenAlex query for citations to DOI `10.1007/s10589-020-00244-5`, work `W3112114392`, returned **29 records**, with publication years through 2026. The raw response is saved at `literature/external-cia-novelty/citing-works-openalex-2026-09-04.json`. Some records are preprint/publication duplicates; 29 is the index's result count, not a count of distinct exhaustively inspected papers. OpenAlex was used for discovery and bibliography, not as authority for mathematical claims.

The returned titles concerned switching-cost algorithms, binary/TV polytopes, decomposition, integer-control optimality conditions, PDE control, quantum-control applications, and process examples. None advertised a resolution of the conjecture. This screen identified the closest documents below; it is not a substitute for obtaining and reading every citing paper.

## Closest adjacent work and distinctions

| Source | Checked evidence | Relevance and distinction |
|---|---|---|
| Bestehorn and Kirches, *Matching Algorithms and Complexity Results for Constrained Mixed-Integer Optimal Control with Switching Costs*, [open manuscript](https://optimization-online.org/wp-content/uploads/2020/10/8059.pdf) | Full PDF downloaded and text searched; abstract, definitions, main contribution, and bounds inspected. | Gives grid-scale rounding bounds, matching algorithms, and complexity for different switching-cost classes. Its `CIA`/`CIA-VC` definitions do not impose a fixed total number of switches. The tight coefficient `(2M-3)/(2M-2)` concerns a different problem and does not replace the new fixed-budget coefficient. |
| Zeile, Weber, and Sager, *Combinatorial Integral Approximation Decompositions for Mixed-Integer Optimal Control*, Algorithms 15(4):121 (2022), [DOI](https://doi.org/10.3390/a15040121) | Bibliographic record and accessible primary-text excerpts; publisher download was unavailable during this audit. | Develops the decomposition framework, alternative discrepancy formulations, state-error estimates, and recombination. No one-switch minimax resolution was found in the accessible material; full independent text inspection remains incomplete. |
| Gu, *An Improved Rounding Strategy for Relaxed Control Solutions of Mixed-Integer Optimal Control Problems*, Advances in Applied Mathematics 14(3):107–116 (2025), [publisher](https://www.hanspub.org/journal/paperinformation?paperid=108896), [PDF](https://pdf.hanspub.org/aam2025143_112624405.pdf) | Primary publisher abstract and PDF text available through the web tool. | Studies improvements to SUR and state-approximation accuracy over long horizons. The claimed result is convergence/error improvement, not a fixed switching-budget extremum or correction of the conjecture. The original Sager–Zeile article appears among its references. |
| *Extended formulations for binary optimal control problems*, [DOI](https://doi.org/10.1007/s10107-024-02162-4) | Citation-forward metadata and the original investigator's primary-source check, recorded in `cia-investigation.md`. | Binary-control convex formulations concern a different object from the multi-mode rounding minimax. This audit did not independently obtain the full article. |
| *Parabolic optimal control problems with combinatorial switching constraints, part III: branch-and-bound algorithm* (2025), [DOI](https://doi.org/10.1007/s10589-025-00654-3) | Primary-source discussion checked by the original investigator; independently found the article in broader searching. | Its primal-bound discussion uses AMDR. No sharp multi-mode one-switch constant was identified. Full independent text inspection remains incomplete. |

The matching manuscript was saved as `literature/external-cia-novelty/matching-2024.pdf` and `.txt`; the filename records the search indexing year, and should not be treated as independently verified final-publication metadata.

## Search coverage and limitations

The search included exact names/identifiers and topic variants:

- `Sager Zeile Conjecture 1`, `Sager Zeile conjecture`, `Sager Zeile counterexample`, `Sager Zeile corrigendum`, `Sager Zeile erratum`.
- Exact DOI searches with 2025 and 2026; an author publication-list screen; the 29-record citation-forward query.
- `combinatorial integral approximation one switch`, `one-switch rounding control`, `combinatorial integral approximation worst-case`, `combinatorial integral approximation minimax`, `CIA-TV bounds`, `CCIA conjecture`.
- Uniform-control and exact-number variants, including `switching 16/45`.

No correction notice appeared. Some broad mathematical queries produced mostly unrelated results, so their failure to find a match has little evidential weight. The strongest positive evidence is that the exact published conjecture and dissertation statement remain identifiable, while the inspected later theory addresses different questions.

Before publication, a human expert should check non-indexed manuscripts and the unavailable full texts, especially work of Sager, Zeile, Kirches, and Bestehorn. This research session did not contact any authors. The present result can responsibly be labeled **mathematically verified; no prior resolution found in a targeted primary-source and citation-forward search**.

## Extension: exact and asymptotic two-switch results

The audit was extended on the same date to [the equal-total two-switch theorem](../results/cia-two-switch-equal-masses.md) and [the global two-switch bound](../results/cia-two-switch-global-upper.md). Independent agents reviewed their mathematics separately; this section only assesses the literature boundary.

No earlier statement of any of the following was located:

- Uniform relaxed controls are worst-case among **all measurable temporal profiles with equal total allocation to each mode**, for two allowed switches and `n>=4`.
- The global arbitrary-total upper bound `T max{1/4,(n-1)^3/(3n^3-3n^2-5n+4)}`.
- The resulting exact continuous values `F_(4,2)=F_(5,2)=F_(6,2)=T/4`.
- The first mode-count correction `F_(n,2)=T/3-2T/(3n)+O(T/n^2)` as the number of modes grows with the switching budget fixed at two.

These are plausible additions to the new CIA results, subject to the same unavailable-text and indexing limitations as the first audit. The equal-total theorem has an explicit restricted domain; the intermediate global bound removes that domain restriction but by itself does not give the exact finite-`n` minimax for `n>=7`. The later exact theorem discussed below supersedes that gap.

### Prior bounds that materially limit the novelty claim

Sager–Zeile's **Corollary 6** and the unrestricted-grid CIA bound from Zeile–Robuschi–Sager, *Mixed-integer optimal control under minimum dwell time constraints*, **Corollary 1**, already provide the coefficient `(2n-3)/(2n-2)` multiplying an appropriate grid/block length. Applying the latter to three coarse blocks yields `F_(n,2)<=T(2n-3)/(3(2n-2))`. The repository's [many-mode investigation](cia-many-mode-switching-investigation.md) explains this application. [Sager–Zeile primary article](https://doi.org/10.1007/s10589-020-00244-5); [Zeile–Robuschi–Sager primary article](https://doi.org/10.1007/s10107-020-01533-x).

Accordingly, the leading limit `T/3` is not a credible independent novelty claim. The proposed improvement is the sharp coefficient of `1/n`: the established coarse-block upper bound expands as `T/3-T/(6n)+O(T/n^2)`, whereas the new upper bound matches the uniform lower bound through `T/3-2T/(3n)`. Merely Taylor-expanding an already known formula would not be new; the substantive step is a new arbitrary-total upper bound that closes the first-order gap.

The values `T/4` for four, five, and six modes agree with the continuous part of the original conjectured first branch. Thus these are proposed **proofs in particular cases of a broader false conjecture**, not counterexamples for those parameter values. The four-pure-block lower witness is already part of the original conjecture's lower-bound mechanism. The new content is the matching upper guarantee for arbitrary profiles and totals.

### Additional later papers screened

- Sager, Tetschke, and Zeile, [*A numerical study of transformed mixed-integer optimal control problems*](https://link.springer.com/article/10.1007/s12532-024-00263-x), Mathematical Programming Computation 16 (2024), 561–597: the primary full article defines CIA with a prescribed TV budget in Definition 9 and compares formulations/algorithms. Its asymptotic discussion concerns increasing discretization size, including objective values and local minima. No conjecture resolution or sharp increasing-mode two-switch expansion appeared in the inspected article.
- Makarow and Kirches, [*Sequential Rounding in Mixed-Integer Model Predictive Control*](https://optimization-online.org/wp-content/uploads/2025/03/autosam.pdf), 2025 manuscript: the primary indexed abstract concerns sequential reconstruction in MPC and practical asymptotic stability. This is not the fixed-horizon increasing-mode minimax regime. A fresh full-PDF fetch failed, so only that limited distinction is asserted.
- The earlier matching manuscript discussed above treats switching costs and fixed-grid rounding. Its bound does not itself establish the equal-total two-switch theorem or the new first-order mode-count coefficient.

Additional queries included `combinatorial integral approximation two switches`, `integral deviation two switches`, `CIA-TV sharp`, `combinatorial integral approximation asymptotic`, and variants using equal mode totals, allocation, and fixed switching budgets. Most generic equal-allocation searches returned unrelated applications and contribute little to the novelty assessment. No later mode-count/switch-budget asymptotic theorem overlapping the new coefficient was identified.

At this intermediate stage the recommended description was a conjecture correction, a sharp one-switch theorem, an exact equal-total two-switch theorem, and a sharp first finite-mode correction. The next section updates that assessment for the stronger result.

## Extension: exact arbitrary-total two-switch theorem

The [new exact theorem](../results/cia-exact-two-switch-worst-case.md) removes the remaining finite-mode gap and states

`F_(n,2)(T)=T max{1/4,(n-1)^3/[n(3n^2-3n+1)]}`, for every `n>=4`,

over **all measurable simplex-valued controls**, with no equal-total assumption. The quarter-horizon branch holds for `n=4,5,6,7`; the uniform branch is strictly larger for `n>=8`. The theorem also gives the exact one-sided minimax `(n-1)^3/[n(3n^2-3n+1)]` for `n>=4`.

No earlier statement of these formulas, the seven-to-eight-mode transition, or the supporting distinct-mode three-block reach theorem was found. The search included the primary and citation-forward sources above, then broadened to cumulative scheduling lag, bounded preemption, one-sided integral discrepancy, fluid scheduling, and monotone rectilinear path approximation. This is a qualified novelty assessment, not a proof of priority. Mathematical certification belongs to the separate proof reviews linked from the theorem file.

### What is and is not the new step

The constant-input recurrence gives the uniform lower bound directly. It does not establish that time-varying profiles with unequal totals cannot be worse. The new proof addresses precisely that quantifier: its aggregate excluded-pair inequality proves a three-distinct-mode reach guarantee for every admissible cumulative path. The heavy-mode lemma then supplies the two-sided guarantee. The equal-total theorem and intermediate upper bound are useful independently checked arguments, but the exact theorem now subsumes their minimax conclusions.

The four-pure-block lower witness, grid-scale rounding estimates, and leading `T/3` limit remain established ingredients. The expansion through `2T/(9n^2)` follows algebraically from the exact new formula; it need not be sold as a separate theorem. The exact finite-grid two-switch worst case and arbitrary switching budgets remain outside this claim.

### Closest scheduling interpretation found

Amir Aminifar's *Analysis, Design, and Optimization of Embedded Control Systems*, Chapter 5, studies cumulative service lag relative to constant task utilization. Theorem 5.4.1 gives lag-feasible scheduling, and Theorem 5.4.2 bounds Jfair's preemption count by three times that of a feasible optimum. Its proof uses the maximum contiguous execution interval allowed by upper and lower lag limits. This is a real conceptual overlap: cumulative deviation and switching/preemption count are competing quantities. But it concerns periodic tasks, fixed utilization shares, and an approximation guarantee on preemptions; it does not state the arbitrary time-varying finite-horizon two-switch minimax or its mode-count constant. These passages were checked in indexed primary-PDF text; a fresh complete download was not available. [University-hosted thesis PDF](https://www.diva-portal.org/smash/get/diva2%3A903971/FULLTEXT02.pdf).

The related primary bibliographic record identifies Aminifar, Eles, and Peng, *Jfair: A scheduling algorithm to stabilize control applications*, RTAS 2015, pp. 63–72, DOI `10.1109/RTAS.2015.7108417`. [University publication record](https://portal.research.lu.se/sv/publications/jfair-a-scheduling-algorithm-to-stabilize-control-applications/). The conference paper itself was not obtained in full during this audit.

Geometric searches for monotone rectilinear approximation and minimum-link paths mainly returned obstacle-routing and planar curve-simplification problems. None located the required fixed-speed, high-dimensional cumulative allocation minimax. This search has low negative evidential weight because the terminology is broad. Likewise, online-learning switching-budget regret bounds optimize a different objective and cannot be assumed to imply a prefix allocation-discrepancy theorem.

The most defensible current description is **a correction of the published multi-mode conjecture and exact continuous one- and two-switch minimax laws, with constructive schedules and identified worst-case controls**. The two-switch law is for `n>=4`. No prior exact resolution was found in the targeted primary-source and citation-forward audit, subject to the explicit full-text and indexing limitations above.

## Extension: three switches and arbitrary fixed block counts

This extension covers [the three-switch heavy-mode theorem](../results/cia-three-switch-heavy-mode.md), [the subsequent global three-switch bound](../results/cia-three-switch-global-upper.md), and [the arbitrary-block one-sided bound](../results/cia-arbitrary-block-one-sided-bound.md). It records a literature screen, not an additional mathematical certification. The first two files link their independent proof reviews; the arbitrary-block file was still marked as awaiting its separate reviews when inspected.

No previous matching statement was located for these claims:

- For `T<=5E`, a profile with some mode total exceeding `E` admits a full two-sided approximation of error at most `E` using at most three switches.
- The exact continuous plateau `F_(n,3)=T/5` for `5<=n<=11`, with the larger interval supplied by the subsequent global bound rather than by the heavy-mode lemma alone.
- The globally sharp first mode-count correction `F_(n,3)=T/4-5T/(8n)+O(T/n^2)`.
- For `1<=k<n`, the arbitrary-profile one-sided coefficient

  `C_(n,k)=[n(n-1)+(n-k)(n-k-1)]/[nk(2n-k-1)]`,

  and its consequence, for every fixed `k`, that both the arbitrary-profile one-sided minimax and the equal-terminal-mass two-sided minimax equal

  `T/k-(k+1)T/(2kn)+O_k(T/n^2)`.

The candidate arbitrary-block method removes a mode, distributes its relaxed allocation equally among the remaining modes, applies an inductive prefix schedule, and appends the removed mode. Targeted searches for this completion/append recurrence, one-sided CIA, mode removal, three switches, fixed activation-block counts, and cumulative discrepancy produced no matching primary-source theorem. Most broad scheduling/discrepancy results were unrelated, so their absence is weak evidence. The stronger evidence remains the previously inspected CIA sources and citation-forward screen above; unavailable full texts remain unavailable, and this update is not a new exhaustive citation census.

### Established ingredients and scope restrictions

The omitted-five-mode construction is an instance of the established omitted-mode lower mechanism. The value `T/5` in the stated small-mode range agrees with the corresponding branch of the earlier conjecture; these are proposed matching upper proofs in particular cases, not new lower witnesses. The Sager–Zeile multi-mode conjecture is false in other parameter ranges, as documented earlier in this audit. [Original primary article](https://doi.org/10.1007/s10589-020-00244-5).

The dimension-free leading values `T/4` and `T/k` already follow from coarse-block rounding using the known coefficient `(2n-3)/(2n-2)`. For `k` coarse blocks, that established upper coefficient expands as `1/k-1/(2kn)+O_k(n^-2)`. The proposed arbitrary-block result improves the coefficient of `1/n` to `(k+1)/(2k)`, matching the uniform lower bound. Its content is the new upper guarantee over temporal profiles, not the Taylor expansion itself. [Minimum-dwell primary article](https://doi.org/10.1007/s10107-020-01533-x).

The arbitrary-block theorem by itself is **one-sided for unrestricted terminal masses**. Its direct full two-sided consequence requires sufficiently small mode totals, including the equal-total case. At this intermediate stage it did not establish a universal arbitrary-total two-sided law for all switching budgets; the final universal-heavy-mode extension below now supplies that transfer. The intermediate three-switch global result leaves an order-`T/n^2` gap in the uniform-dominated regime; the subsequent exact result below closes that particular gap using a stronger prefix theorem.

The reviewed Jfair scheduling material above does not close these distinctions: it treats cumulative lag versus preemption for periodic fixed-utilization tasks, without the claimed arbitrary time-varying mode-removal recurrence or exact mode-count correction. No equivalent result was found in the checked scheduling material.

The responsible novelty label remains **candidate new upper bounds and exact special-case minimax values; no matching statement found in the targeted open-literature search**. This is weaker than proof of priority, and separate proof review remains required for any newly added formula.

## Extension: exact three-switch minimax for every n>=5

The [exact three-switch result](../results/cia-exact-three-switch-worst-case.md) now states

`F_(n,3)(T)=T max{1/5,1/[n((n/(n-1))^4-1)]}`, for every `n>=5`.

It yields the plateau `T/5` through eleven modes and uniform-input optimality from twelve modes onward. Its dependency is the [general four-distinct-mode reach theorem](../results/cia-general-four-block-reach.md), which also establishes the matching one-sided minimax for every `n>=5`. The reach proof is computer-assisted through exact finite rational and symbolic polynomial certificates, with a separate independent audit. The heavy-mode and transfer arguments are analytic. This novelty audit has not independently rechecked those certificates.

No prior exact three-switch formula, eleven-to-twelve-mode transition, or corresponding arbitrary-profile four-block reach guarantee was found in the targeted primary-source searches and earlier citation-forward screen. New exact-phrase and topic searches again located the original Sager–Zeile conjecture and later decomposition work, without a matching result. An indexed primary extract from the 2022 decomposition article concerns recombination of singular arcs; its four-arc discussion is not a theorem about a four-block minimax. A renewed full-page fetch was still rate-limited, so the earlier incomplete-reading limitation remains.

This upgrades the proposed mathematical contribution from a sharp first correction to an **exact continuous three-switch replacement law**, conditional on its documented proof verification. The known omitted-mode and uniform lower mechanisms remain ingredients. The earlier purely analytic global upper bound is a useful independent fallback. No assertion about exact finite-grid values or four or more allowed switches follows from this update.

## Final extension: universal heavy-mode transfer and every switching budget

This final scope update closes the investigation at the user's request to stop. It covers the already-written [universal heavy-mode theorem](../results/cia-universal-heavy-mode-rounding.md) and [arbitrary-switch global bound](../results/cia-arbitrary-switch-global-bound.md), whose separate proof reviews are linked in those files. This note screens novelty; it does not provide another independent audit of their proofs.

The heavy-mode theorem states that, for every integer s≥0 and every number of modes, T≤(s+2)E together with some terminal mode mass greater than E guarantees a full cumulative-error bound E using at most s switches. Its proof first obtains integral prefix rounding with a repeated mode, then reorders the prefix ending at its first repeat so that one mode occupies two adjacent unit intervals. The prefix occupation counts are preserved, so the suffix errors remain unchanged. Standard integral network-flow rounding is an established ingredient; the claimed additional step is the repeat-preserving prefix reordering with the full discrepancy guarantee.

The resulting exact structural identity is

`F_(n,k-1)(T)=max{T/(k+1),G^-_(n,k)(T)}`, for `1<=k<n`,

where G^- is the worst-case one-sided minimum among schedules with at most k blocks, allowing repeated modes. This is a reduction of the full minimax to the one-sided minimax, not an exact closed formula for the latter at every k. The known omitted-mode witness gives the first lower branch.

Combining the heavy-mode theorem with the reviewed arbitrary-block one-sided upper bound gives, over **all measurable profiles and arbitrary terminal totals**,

`F_(n,k-1)(T)<=T max{1/(k+1),[n(n-1)+(n-k)(n-k-1)]/[nk(2n-k-1)]}`,

for every `1<=k<n`. Thus the earlier one-sided-only caveat applies to that earlier standalone argument, not to the combined theorem. The combined theorem establishes the exact plateau

`F_(n,k-1)(T)=T/(k+1)` when `k>=2` and `k+1<=n<=k(k+1)/2`,

and, for every fixed k, the full arbitrary-profile expansion

`F_(n,k-1)(T)=T/k-(k+1)T/(2kn)+O_k(T/n^2)`.

The displayed plateau range is sufficient, not a claim that the plateau ends there. The separately established exact small-budget laws extend that range. The leading T/k and omitted-mode lower witness are established ingredients; the proposed additional content is the universal heavy-mode reduction, the matching arbitrary-profile plateau upper, and the sharp first finite-mode correction for every fixed budget. No exact finite-n formula for all larger budgets or exact finite-grid minimax is asserted.

A final targeted query pair for CIA heavy-mode switching and one-sided switching minimax located no matching theorem. It returned the already-screened original constrained-variation work, later penalty/decomposition papers, and numerical studies. The indexed primary text of the [2022 decomposition paper](https://www.mdpi.com/1999-4893/15/4/121), Section 3.4, explicitly introduces a switch-count constraint, omits that class from its next section, and directs readers to earlier bounds and reformulations. That passage does not supply the new structural identity or arbitrary-budget formula. Its complete text was not newly read in this closing check. The [2024 numerical study](https://link.springer.com/article/10.1007/s12532-024-00263-x) had already been inspected above.

No earlier matching universal heavy-mode lemma, exact full-to-one-sided identity, general plateau upper, or sharp first correction was found in the targeted primary-source and citation-forward search documented here. This remains a qualified negative search result, not proof of priority. The earlier unavailable-full-text limits and incomplete coverage of adjacent scheduling terminology remain material. No new research direction or additional citation census was started for this closing update.
