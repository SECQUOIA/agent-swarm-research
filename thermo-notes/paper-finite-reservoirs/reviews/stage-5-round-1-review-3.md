# Stage 5, round 1 — independent review 3

## Verdict

**No major issues found.** The synthesis accurately distinguishes the strongest physical theorems from exact Gaussian illustrations and assumed capillarity models. The principal prior-art distinctions are supported by the primary material I independently inspected. The relocation preserves the accepted short-range mathematics exactly. I found one minor asymptotic wording correction in the new conclusion.

I read the stage author handoff, revised main file, introduction, numerical section, conclusions, appendix opening and proof guide, added geometry attribution, bibliography, reproduction README, coverage audit, affected current repository summaries, and numerical/figure code. I did not read another current-round review or the coordinator's current literature-audit report as an authority. I did not edit the manuscript or delegate.

## Minor issue

**Use strict asymptotic growth language in the conclusion.** The first paragraph of `sections/conclusions.tex` says that three support points force “capacity larger than the square of its scale.” The theorem requires the ratio to diverge, not merely to exceed one or a fixed constant. Replace this with “capacity growing faster than the square of its scale,” or restate `c_N/b_N^2 -> infinity`. The introduction and abstract already state the condition correctly. This is a local wording issue, not a theorem defect.

## Literature and novelty assessment

The paper makes a suitably narrow claim: optimized full-law asymptotics for a prescribed canonical reference under the exact power-law bath, with necessity and actual positive-tail sufficiency separated. It expressly credits finite-bath ensembles, Gaussian ensembles, phase mixtures, conditioning results, supporting-quadratic geometry, and phase correlations. It does not base validity on an assertion that no predecessor exists.

I independently checked the following evidence:

- **Challa–Landau–Binder 1986.** I obtained the primary APS PDF directly, rather than relying on the coordinator audit. The text explicitly discusses the two weighted Gaussian peaks, the need for corrections between them, and the distinction between a volume-order Gaussian valley cost and the actual interfacial surface cost. The manuscript's attribution of both the gap/width description and the valley limitation is supported. Primary source: [Physical Review B 34, 1841](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevB.34.1841/fulltext).
- **Riera–Gogolin–Eisert 2012.** In the retained primary Appendix A, equations (19)–(29) express the strong-distance error through the bath entropy remainder; Appendix B, equations (33)–(35), gives the squared subsystem Hamiltonian scale divided by bath size. This supports the manuscript's acknowledgment of energy-range-squared sufficient control. The paper does not attribute its optimized two-phase necessity theorem to that reference or present the general sufficient scaling as newly discovered.
- **Diaconis–Freedman 1988.** The primary Berkeley report's abstract and introduction explicitly give conditional variation estimates for a growing block with `k/n -> 0` in regular exponential families, including a sharp leading error. The introduction accurately credits those results and distinguishes their independent-coordinate conditioning setting from the present interacting phase-mixture problem.
- **Griffin–Matty–Swendsen 2017.** Their primary equation (23) is the Euclidean norm of discrete energy-probability differences. Their Potts discussion explicitly says that the comparison temperature was optimized to reduce that norm. The current introduction accurately identifies this close finite-reservoir Potts precedent without conflating its metric or adjustable target with the manuscript's specified-target TV question.
- **Campisi 2007.** The retained primary text treats power-law ensembles and interprets their parameter through finite reservoir capacity. It is appropriate evidence that the equilibrium ensemble mechanism is established. The current framework separately fixes the surface-entropy convention, so it does not assume that every source's finite offset convention is identical.
- **Cohen–Rittenberg–Sadhu 2015.** Section 4.3 of the retained primary text explicitly states that degeneracy changes order-one contributions to shared information and discusses first-order coexistence. The present manuscript gives that work appropriate credit while reserving its narrower claim about an external bath-size window and a full microscopic KL proof.
- **Ramírez-Hernández–Larralde–Leyvraz 2008.** I checked the retained primary text in the preceding shared-bath review and rechecked the present citation's scope. Opposite-phase assignments and their switching are appropriately credited. The manuscript does not suggest that anticorrelated phases themselves were discovered here.
- **Corti–Ohadi–Fariello–Uline 2023.** I inspected the local primary full text and its publication metadata. It studies small ideal-gas contact and distinguishes phase-space-density and phase-space-volume entropy conventions. The conclusion uses this source narrowly to contextualize finite-size conventions and does not endorse all of its broader entropy arguments.
- **Mishin 2015 and Yoneta–Shimizu 2019.** I checked their primary arXiv records and abstracts. These support the stated finite-reservoir fluctuation and squeezed-ensemble/conversion scopes, respectively, and the journal metadata matches `refs.bib`: [Mishin](https://arxiv.org/abs/1507.05662), [Yoneta–Shimizu](https://arxiv.org/abs/1903.04111).
- **Borgs–Chayes–Helmuth–Perkins–Tetali.** The [primary arXiv record](https://arxiv.org/abs/1909.09298) confirms the 2022 third version used in the bibliography. It is presented as that version rather than given an invented journal publication. The manuscript's corrected BCT-only finite-volume proof remains separate from the later exterior convention.

The source list and comparison text do not establish exhaustive priority. The manuscript and reproduction README correctly make no such guarantee. I did not independently inspect the full inaccessible 1990 review; its current citation is limited to broad review scope, rather than a claim that all its derivations have been ruled out as predecessors. I found no unsupported specific novelty claim in the new text.

## Scientific synthesis and coverage

The introduction table correctly separates the ordinary `N` requirement, the two-phase `N^(3/2)` requirement under actual tail assumptions, and the `N^2` support obstruction. Its explicit distinction between symmetry-related phases at the same energy and distinct energy support points prevents a misleading inference for the q-fold Potts degeneracy.

The abstract and introduction correctly state that kinetic coordinates are optional for both microscopic threshold theorems. The shared-bath summary distinguishes complete canonical subsystem marginals from their joint product target and names the balancing reference. The boundary summary explains why an unrestricted TV optimum can abandon a phase. The conclusion retains the dimension-two boundary restriction, the large-q requirement, the additive-coupling assumption, and the distinction between microscopic theorems and a specified capillarity model.

I found the coverage mapping coherent. The weak-support theorem subsumes the earlier three-phase note, the physical boundary optimization strengthens the earlier crossover development, the short-range positive-moment proof resolves the earlier sufficiency gap, and the Gaussian contact-set optimum addresses escaping calibrations. The excluded survival, transport, kinetics, and unrelated droplet-stability directions do not provide a missing proof for this reservoir-accuracy manuscript. The retained capillarity and barrier diagnostics cover the relevant interfacial accuracy limitations without claiming a dynamical rate theorem.

## Proof relocation and presentation

I independently reconstructed the previous microscopic section by removing the new main-text proof guide, appending the short-range appendix content, and restoring the heading level. The reconstructed SHA-256 is

`4f6cfab2a45063487df9a706731ca9a670f7231f4825410a72c518e3c9061fe2`,

which matches the stated accepted Stage 2 round-2 file. This confirms that the substantive contour proof was not changed during relocation.

The main text now gives the microscopic theorem and a useful proof guide, while the source-sensitive contour estimates remain complete in Appendix A. Gaussian geometry and capillarity diagnostics are moved by input order with stable labels. This keeps the physical theorem route readable and preserves the comprehensive scope requested by the user. I found no broken logical dependency caused by the move. The Gaussian and capillarity sections remain visibly model-specific appendices rather than being blended into the short-range theorem.

## Numerical and bundle checks

I inspected the exact algorithm, independent-check code, figure code, numerical text, and data-provenance instructions. An AST comparison confirms that `canonical_energies` and `finite_bath` in the standalone copy are identical to their earlier independently checked implementations. The archive SHA-256 independently matches the README's value:

`93fed9507ceaf9126feb93e79ae5bbb295be185a56f9a84dabe0608e55aab2c1`.

The figure code uses the full energy/full-state TV field, not the spin marginal field, and computes its dotted limits from the unequal-variance secant weights. The derived values agree with the numbers quoted in the numerical section. I visually inspected the scaling figure: labels, curve identities, axis meanings, and the two boundary limits are clear. The second figure is explicitly identified in both prose and caption as evaluation of a limiting formula, rather than microscopic finite-size data.

The numerical section correctly distinguishes exact finite-sum formulas from their floating-point evaluation and does not claim interval-certified numerical results. The README states that large-N archival calculations were not rerun merely to regenerate figures. I checked the reported installed Python/NumPy/SciPy/Matplotlib versions against the environment; they match. The present build log has no undefined references or cited keys, overfull/underfull boxes, or warning lines.

I did not rerun the expensive occupation enumeration or repeat already completed quadratures, because no scientific algorithm changed in this stage and those repeated runs would not add a distinct check of the literature/synthesis work. The later whole-manuscript review remains necessary under the user's process; this report does not declare that later stage complete.
