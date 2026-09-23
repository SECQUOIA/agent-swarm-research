# Stage 4 independent review 5

**No supported major or minor finding.** I read the entire frozen `reviews/revision-stage4-round1/source/sections/04-vector.tex` (1,308 lines), the complete abstract, introduction, conclusion and bibliography, and the relevant scalar, allocation, parity and finite-disjunction dependencies. I compared the vector changes with the frozen stage 3 source and inspected the current README, SUBMISSION-README and historical coverage marking. Author records supplied leads only. I did not consult other stage 4 reviewer reports or edit manuscript sources.

## Whole-stage mathematical coverage

The review covered level refinement and cover trimming; monotone implicit overlays and common denominators; box/facet original-output spanners; maximum-product allocation; effective-image radii and oracle pullbacks; the full fixed-grid spanner algorithm and positive-polar weak separator; both effective-image band constructions; shared separable bases and every table constant; separated power layers, cap sets and repeated convexification; all integer sections of the degree-32 product example; the hinge/Bernstein stability argument; triangular-wave polynomial encoding; arbitrary signed polynomial overlays; tilted-body conditioning; simplex bands; and the final lattice-free observation.

Critical checks included preservation of a common input and interpolation weight, exact membership after weak-oracle repair, uniformly bounded denominators across basis exchanges, rounding inside the nonlinear image, and integer counts independent of auxiliary circuit wires. The GLS objective comparison is with the actual body. I checked its original printed p.172 image: its weak-separator norm requirement is **at least** one, so rational infinity-norm rescaling in the manuscript meets that convention. The one-dimensional padding is supplied. The separable packing argument uses one basis across coordinates, and the factors in all six finite/compiled bounds agree with the local capacities and packing denominators.

The separation proofs account for unbounded integer labels and complete convex sections, including mixtures that are not initial witness-to-witness segments. The cap-set bound is not presented as an unbounded binary/general-integer gap. The degree and conditioning estimates in the nonconvex and tilted examples support their stated scope. No defect emerged from these checks.

## Independent primary-source checks

I followed `literature/AGENTS.md` and inspected these passages directly:

- **Plevrakis–Hazan:** cached published PDF text, Section 3.3, PDF p.8, explicitly combines approximate linear optimization with inherited spanner exchange. The [official proceedings page](https://proceedings.neurips.cc/paper/2020/hash/565e8a413d0562de9ee4378402d2b481-Abstract.html) and its cached official BibTeX confirm volume 33, pages 7637–7647 (2020). The revised locator is correct.
- **Lyu–Hicks–Huchette:** local primary v1 text, Section 3/Proposition 1, explicitly merges breakpoints and shares SOS2. The [version record](https://arxiv.org/abs/2304.14542v1) agrees with the bibliography's locator note. The [publisher](https://pubsonline.informs.org/doi/10.1287/opre.2023.0187) confirms volume 74(1), pages 484–499, January–February 2026; the earlier 2025 online date does not invalidate the stated issue year. Local passage: [[lyu2026-building-formulations-for-piecewise-linear]] p.6-8.
- **Ellenberg–Gijswijt:** cached arXiv:1605.09223v1, Theorem 4 on p.2 and proof on p.3, gives `3 m_((q-1)n/3)`. Specializing to characteristic three and optimizing the elementary generating-function bound gives the manuscript's constant. The [explicit version](https://arxiv.org/abs/1605.09223v1) is correctly named.
- **Averkov–Weismantel:** cached arXiv:1002.0948v2, definition on p.1 and Theorem 1.1 on p.2, gives the mixed-Helly identity for finite convex intersection certificates. The [version](https://arxiv.org/abs/1002.0948v2) is correctly identified; the manuscript does not convert that identity into an unsupported interval-cover theorem.
- **Other imported methods:** inspected Awerbuch–Kleinberg, Section 2.3/Propositions 2.2 and 2.4; GLS, Definitions (5)–(7) and Corollaries (3.4)–(3.5); Kelly–Maulloo–Tan, logarithmic NETWORK objective and proportional-fairness inequality (1); and Hartman's opening definition and local/global discussion. These support the scoped attributions, while the manuscript proves its graph-specific consequences.

Targeted searches also surfaced [van der Hulst–Walter's recent implied-integrality paper](https://link.springer.com/article/10.1007/s10107-026-02389-3). Its abstract, introduction and Section 6.2 concern integrality of fixed polyhedral sections and integer hulls; they do not contradict the stated graph-approximation comparison. Search results do not certify priority.

## Integration and readiness

The abstract and conclusion correctly distinguish the real-coefficient two-bit scalar theorem from the eleven-bit rational dense-polynomial compiler. The rank-dependent vector statements, input-dimension dependence for separable maps, explicit final oracle bands, and restricted scope of sparse/exponent representations are consistent with the proved results. The novelty language credits inherited methods and confines the qualified main claim to the nc-rank precision characterization.

The author/date fields are blank as requested. Documentation clearly separates historical review gates, current revision records and optional verification scripts from the standalone mathematical sources. The remaining one-input question is a research boundary, not a premise missing from a claimed theorem. No additional required correction or optional preference arose from this review.
