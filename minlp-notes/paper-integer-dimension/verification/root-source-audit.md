# Root source and mathematical audit

## Initial source checks

- Read the local full text of Lubin, Vielma, and Zadik, *Mixed-integer convex representability*, Lemma 4.1 (PDF page 12). The integer parity argument is established there; it does not require bounded integer ranges. The source assumes a closed convex defining set, but the actual midpoint reasoning needs only convexity, so extension to nonclosed convex lifts must be proved explicitly in this manuscript.
- Local literature metadata has the author order Lubin–Zadik–Vielma for the journal paper, whereas the journal precursor and journal record use Lubin–Vielma–Zadik. Manuscript bibliography must follow the actual version cited. Earlier arXiv:1611.07491 and journal precursor arXiv:1706.05135 are distinct versions.
- Confirmed the published GGOW source is *Foundations of Computational Mathematics* 20 (2020), 223–290, DOI 10.1007/s10208-019-09417-z. Its capacity and shrinking theorems are prior results; the proposed contribution here is their application to whole-graph formulation precision.
- Confirmed both Beach et al. discretization papers have published 2024 versions: Part I, 87:835–891, DOI 10.1007/s10589-023-00543-7; Part II, 87:893–934, DOI 10.1007/s10589-024-00554-y. Cite those versions when appropriate.
- Targeted web searches for mixed-integer/noncommutative-rank and integer-dimension/quadratic-approximation combinations did not locate a directly matching precision theorem. This is a bounded search, not proof of priority.

## Independent stage 1 derivation checks

- Checked the common-parity midpoint implication and the use of closures of input contact sets. Taking these closures preserves the continuous midpoint error inequality without requiring the projected lift itself to be measurable or closed.
- Re-derived the symmetric shrunk-subspace coordinate lemma: with V=sum H_j U, Z=U intersect V-perp and W=V intersect U-perp, symmetry forces H_j Z subset W. Adjoint projection maps give dim Z-dim W=dim U-dim V. Precision exponents (0,1,1/2) on (Z,W,(Z+W)-perp) therefore sum to ncrank/2.
- Checked the real-subspace descent: supermodularity of the deficiency and invariance under conjugation force U+conjugate(U) to retain maximal deficiency.
- Checked the compact residual-product construction, including x=1 and zero-bit coordinates. Binary-times-continuous terms are exact; residual McCormick/square triangles contain the graph with error h_i*h_j/4. The construction preserves every exact graph point.
- Re-derived positive-perspective homogenization and the fixed-t lower slice. Only binary-times-t needs product inequalities; unbounded continuous auxiliary variables can be homogenized directly. No corresponding unbounded-general-integer product formulation is asserted.

## Reproducible checks

All seven selected existing stage 1 scripts passed under the repository conda environment. The timestamped stage1 manifest records script hashes, interpreter version, runtime, and separate complete outputs. Exact and floating-point components retain the scope stated by their original scripts; passing them does not prove a universal theorem.

## Primary full-text follow-up

- Retrieved the published GGOW PDF and inspected Theorems 1.4, 1.17, and 1.18. The complex-field matrix-evaluation and shrinking characterizations match the needed hypotheses. The distinction between rank computation and construction of shrinking coordinates must remain explicit.
- Retrieved Nicola arXiv:0805.4122 and checked Definition 1.1 and the following paragraph on printed page 3. Constant scalar Hessian rank does imply the local affine-gradient-fiber condition. The manuscript gives its own partial-Legendre derivation, so this geometric dependency is also explained directly.
- Located the recent Choi–Fattahi–Han–Gómez–Lozano preprint arXiv:2608.22815. Read its abstract and model on pages 1–2. It studies convexification of quadratic epigraphs with original indicator decisions and decision diagrams. This is adjacent to, but is not a statement of, the whole-graph auxiliary-integer precision law. This initial model comparison does not constitute a full-paper novelty audit.
- Direct retrieval of the linked Hörmander PDF failed with HTTP 500. The web index supplies the original article; its exact theorem still needs direct examination or verification against the available Wolff exposition. Record retrieval failure rather than imply successful local access.

- Retrieved Wolff's March 2002 notes from a scholar-hosted mirror after the UBC source timed out. Read Theorem A and its proof sketch on printed pages 50–51: the compact-support, smoothness, and nonvanishing mixed-Hessian assumptions give the required L2 operator bound with exponent -n/2. The TT* kernel and Schur-test proof match the manuscript's intended local derivation.
