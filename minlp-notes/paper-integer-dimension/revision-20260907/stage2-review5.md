# Stage 2 independent review 5

**No supported major or minor finding.** I read all 1,296 lines of the frozen `sections/01-foundations.tex` and all 1,571 lines of `sections/02-quadratic-finite.tex`, including proofs, examples, implementation paragraphs, and unnumbered estimates. I compared both files and the bibliography with `revision-stage1-round1/source`, and read `stage2-author.md` and `stage2-literature.md`. I did not read other current reviewer reports or edit manuscript sources.

The review supports passing this stage. It is a substantive mathematical review, not a guarantee that an independent future reader cannot identify another issue.

## Whole-stage coverage

I reconstructed the representation/parity closure arguments; elementary square/product constructions and constants; scalar and one-sided quadratic laws; principal compression, real symmetric shrinking, capacity/covariance proofs and examples; smooth oscillatory contact bounds, global allocation, constant-rank tubes and perspectives; finite covariance comparison and certificates; rational rank and matrix-function algorithms; the complete inexact geodesic algorithm; grouped, total-absolute and oracle output budgets; input quotient; logdet allocation, PSD blocks, diagonal/feature/forest results; and the hardness reductions. This includes all unnumbered algorithm estimates and examples, not just changed passages.

Critical checks were the capacity scaling exponent `2r`; cancellation of the tensor evaluation dimension in the smooth volume exponent; actual polyhedral tubes in original coordinates; polynomial precision without spectral gaps; recurrence on rounded stored iterates; exact feasibility repairs; effective output dimension versus active input rank; preservation of correlated domains; and polynomial replication in the positive-optimum hardness proof. These checks did not expose a defect.

## Independent source checks

I followed `literature/AGENTS.md` and did not alter the literature database. Primary passages inspected during this review include:

- Garg–Gurvits–Oliveira–Wigderson: local arXiv v4 full text for Theorems 1.4 and 1.17, and fresh extraction from `original.pdf` around Theorem 2.18. The integral capacity lower bound is `n^(-2n)` for unnormalized integral Kraus operators; it supports the manuscript's `D_H^(-2r) r^(-2r)` estimate. The source's rank/evaluation equivalences support the manuscript's imported algebraic characterizations. Local locators: [[garg2020-operator-scaling-theory-and-applications]] p.4-5, p.9-10, p.26-27.
- IQS v6 Theorem 1.5/Lemma 5.3 and Volcic v2 Section 2.1 support, respectively, rational shrunk-subspace computation/field extension and the involution needed for Hermitian free-field pencils. The manuscript supplies its own principal compression and real descent proofs.
- Wolff, March 2002 notes, printed pp.50–51: Theorem A and its composed-kernel/Schur proof match the local oscillatory estimate. I did not independently retrieve Hörmander's original article; the manuscript's included local proof and this complete primary exposition suffice for the checked application.
- [Nicola's published article](https://www.impan.pl/shop/publication/transaction/download/product/90263), printed pp.208–209: Definition 1.1 and the following paragraph state the affine-fiber property for constant Hessian rank. The revised published metadata and page locator agree with the primary PDF.
- Zhang–Sra, Corollary 8, PDF p.8: the curvature factor depends on the comparison-point distance. Its unprojected triangle inequality followed by nonexpansive projection remains applicable to a stored iterate slightly outside the smaller projection ball, as in this manuscript. [Primary proceedings page](https://proceedings.mlr.press/v49/zhang16b.html).
- Criscitiello–Boumal, Appendix I, Proposition I.1: the stated affine-invariant curvature lower bound is `-1/2`; the manuscript safely uses `-1`.
- GLS 1981, printed p.172 Definition (5) and the separation/optimization theorem: I specifically checked that this version's weak optimization compares against the **actual body**, rather than an eroded body. Consequently the objective guarantees used before the correlation and central-ball repairs are justified. Cached original: `build/source-cache/gls1981.pdf`.
- Dadush–Peikert–Vempala, Theorem B.5, printed p.38: the rational ellipsoid matrix, possibly real center, and `(d+1)sqrt(d)` factor agree with the import. The known inner volume rules out its small-volume alternative, and symmetry removes the center. Cached original: `build/source-cache/dpv2011.pdf`.
- Del Pia 2026, Theorem 2: inspected the local primary full text and [current arXiv record](https://arxiv.org/abs/2607.29386). Rational orthogonal near-diagonalization with polynomial Turing complexity is explicitly stated; the manuscript also proves the residual version it needs. Local locator: [[pia2026-rational-jacobi-rotations-and-the]] p.15.
- Yarotsky v3 and Beach et al.: the folding identity and dyadic interpolant are inherited. The revised width-`e_p` band explicitly converts the interpolant into an approximation retaining every square graph point, with unchanged binary count. This accurately separates the antecedent upper construction from the arbitrary-lift lower comparison.

## Novelty, scope, and optional preferences

The changes make local attribution more precise without introducing a broader priority claim. The repaired product illustration now establishes its stated domain scope. Nothing found in this source review contradicts the already qualified nc-rank graph-approximation novelty assertion, but this review does not certify priority over all literature.

The section lengths and many distinct mathematical tools will demand effort from readers, but the new proof roadmap and the division between rank-rate and finite-accuracy algorithms help. I have no additional required editorial correction supported by this review.
