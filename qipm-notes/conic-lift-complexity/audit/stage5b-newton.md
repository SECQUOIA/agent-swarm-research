# Stage 5B author: Newton comparisons

Authored `sections/12c-newton-comparisons.tex`, 2026-09-20. No other manuscript, bibliography, source note, or literature file was edited.

## Source coverage

Read the complete root Stage 5 preparation, the complete mathematical developments in `psd-column-packing-newton-forest`, `psd-lorentz-reduced-oracle-equivalence`, `off-center-psd-packing-schur-obstruction`, `implicit-psd-fiber-recentering-access`, `latent-treewidth-lorentz-newton-systems`, `ball-formulation-latent-treewidth-tradeoff`, and the graph/resource sections of `psd-order-cap-qipm-ledger` and `ball-cap-latent-treewidth-pareto`. Read the sparse-Newton replacement synthesis. The section integrates their formulation-specific conclusions; existing geometric, barrier, and movement results are invoked rather than reproved here.

The broad quantum sampling-conditioning project and the fresh-input dynamic scale-maintenance lower-bound project are not asserted as formulation theorems. The scale-update identity, fixed-objective central-path caching boundary, and the prohibition on multiplying snapshot query costs by iteration counts are retained. The scalar/readout constructions are assigned to the query author.

## Independently developed correction and proof

The source's squared off-center upper comparison is valid but not sharp for exactly feasible source allocations. The new theorem proves the sharp first-power comparison `H0/L <= HD <= H0/mu`, with condition factor `L/mu` attained by the two-source correlation example. The proof does not assume the diagonal signed test matrix E is PSD: **E D E is PSD**, which is the matrix paired with residual order. Commutativity of E with the diagonal center and source-wise trace allocations then give the key exact M0 trace identity. Unequal positive group counts are permitted.

The section separately derives the complete reduced Newton gradient `2 rho^T M^-1 z + eta<c,U>` by completing the auxiliary square. Exact centered equality concerns matrix **and** right-hand side; the spectral theorem by itself does not identify Newton states. Approximate allocation error zeta changes the comparison to `H0/[L(1+zeta)] <= Hhat <= H0/[mu(1-zeta)]`, giving the old squared bound under spectral closeness alone. Affine infeasibility needs separate RHS terms.

The two-source counterexample uses W=0, so its auxiliary-gradient coupling vanishes and the stated Newton directions are valid, not merely inverse-Hessian vectors chosen without checking the RHS.

## Other checks and scope decisions

- The marginal function has exact standard parameter sum h_a. This is a statement about that function; the projected product body's intrinsic barrier optimum is not claimed to be sum h_a.
- Implicit recentering bit cost explicitly assumes common-denominator dyadic coordinates and exact interiority of the stored rational point. Dense Gram output is separately charged.
- The all-source scale lower bound is for jointly correct classical output, or a compiled value interface with joint readout correctness and no further input queries. It does not charge b sqrt(s) for one online coherent invocation. Exact 0-or-1 search with known single-mark amplitude followed by verification gives the all-source upper without an unnecessary log b.
- The one-hub Newton expansion may have negative or zero diagonal entries. The exact arbitrary-pivot Furer--Hoppen--Trevisan theorem handles these; no unsupported scalar leaf-pivot proof is used.
- Two-hub positive-diagonal augmentation uses square roots and is a real-arithmetic branch. Quasidefiniteness and a resolvent regularization estimate are proved; no unconditional floating-point guarantee is asserted.
- Raw/reduced grouped graph counts and binary-tree counts are proved. The regular smooth coordinate formulation reduces to width one; there is no claimed intrinsic regularity-width tax.
- The full-output comparison requires matched classical entry access, a common accepted Newton residual contract, and supplied width bounds for every admitted trajectory. Exact replacement need not reproduce a random quantum trajectory, only preserve the outer guarantee. State/scalar/coherent output and quantum-only access remain outside it.
- LSQR/CGLS is used only with consistent full-column-rank systems, zero initial guess, exact arithmetic, and charged forward/transpose products. Its residual bound follows from CG in the normal-equation energy norm.

## Verification performed

An isolated qipm `pdflatex -interaction=nonstopmode -halt-on-error` build produced a nine-page section without TeX errors or overfull/underfull boxes. The isolated build intentionally has no bibliography, so citation warnings are expected until integration. All labels are prefixed `newt:`.

Forty independent qipm NumPy checks at randomly generated feasible residuals with nonuniform source allocations and group counts (2,1) verified the first-power M comparisons, equality of direct constrained auxiliary minimization and the quotient formula, and the gradient from a finite difference of the reduced Newton quadratic. Maximum quotient discrepancy was 1.43e-14 and gradient discrepancy 2.49e-12. These checks support algebra only; the manuscript gives exact proofs.

## Literature consulted and verified

Local packages consulted: `literature/papers/furer2025-fast-gaussian-elimination-for-low/paper.md`, `paige1982-lsqr-an-algorithm-for-sparse/paper.md`, and `belovs2015-variations-on-quantum-adversary/paper.md`. Literature folders remain read-only.

Primary online checks:

- Furer--Hoppen--Trevisan final ESA 2025 PDF: https://drops.dagstuhl.de/storage/00lipics/lipics-vol351-esa2025/LIPIcs.ESA.2025.116/LIPIcs.ESA.2025.116.pdf . **Corollary 3 is verified on printed page 116:14**, giving O(k^2(m+n)) solve/inconsistency determination from a width-k decomposition with O(m+n) bags. (The rectangular RHS length in its printed wording has an evident typo, irrelevant to our square nonsingular application.) The arbitrary-field and accidental-cancellation scope comes from Theorem 1 and its proof.
- ECOS primary author text https://web.stanford.edu/~boyd/papers/pdf/ecos_ecc.pdf , Section IV-B.1, equations (11)--(13), explicitly gives signed two-hub sparse augmentation and positive downdated-base condition. Author publication page https://web.stanford.edu/~boyd/papers/ecos.html verifies ECC 2013, 3071--3076.
- Vanderbei primary author list https://vanderbei.princeton.edu/Publications.html and publisher https://epubs.siam.org/doi/10.1137/0805005 verify SIOPT 5(1), 100--113 (1995) and the every-symmetric-permutation exact factorization statement. No numerical stability result is inferred.
- LMRSS primary full text https://arxiv.org/pdf/1011.3020 and publisher https://doi.org/10.1109/FOCS.2011.75 establish adversary characterization for general function evaluation, sufficient for our finite-output direct-sum construction.
- Paige--Saunders primary text https://web.stanford.edu/group/SOL/software/lsqr/lsqr-toms82a.pdf and author references https://saunders.people.stanford.edu/references verify TOMS 8(1), 43--71 (1982).
- Augustino et al. primary publication https://quantum-journal.org/papers/q-2023-09-11-1110/ verifies final 2023 volume 7 article 1110 and hybrid inexact Newton scope.
- Dalzell et al. author full text https://davidbader.net/publication/2023-dcsblbssbkz/2023-dcsblbssbkz.pdf and publication page https://davidbader.net/publication/2023-dcsblbssbkz/ verify PRX Quantum 4(4), 040325 (2023), data/conditioning/readout comparison.

Targeted search for the packed residual Schur Hessian/allocation conditioning theorem did not identify a matching statement. This is not proof of priority. The section claims no new general matrix inequality, sparse augmentation, search bound, or linear-system primitive; its contribution is the explicit formulation theorem and its precise conditions.

## BibTeX additions for integrating author

```bibtex
@inproceedings{FurerHoppenTrevisan2025,
  author = {F{\"u}rer, Martin and Hoppen, Carlos and Trevisan, Vilmar},
  title = {Fast {Gaussian} Elimination for Low Treewidth Matrices},
  booktitle = {33rd Annual European Symposium on Algorithms (ESA 2025)},
  series = {Leibniz International Proceedings in Informatics},
  volume = {351}, pages = {116:1--116:15}, year = {2025},
  doi = {10.4230/LIPIcs.ESA.2025.116}
}
@inproceedings{DomahidiChuBoyd2013,
  author = {Domahidi, Alexander and Chu, Eric and Boyd, Stephen},
  title = {{ECOS}: An {SOCP} Solver for Embedded Systems},
  booktitle = {2013 European Control Conference (ECC)},
  pages = {3071--3076}, year = {2013},
  doi = {10.23919/ECC.2013.6669541}
}
@article{Vanderbei1995,
  author = {Vanderbei, Robert J.},
  title = {Symmetric Quasidefinite Matrices},
  journal = {SIAM Journal on Optimization},
  volume = {5}, number = {1}, pages = {100--113}, year = {1995},
  doi = {10.1137/0805005}
}
@inproceedings{LMRSS2011,
  author = {Lee, Troy and Mittal, Rajat and Reichardt, Ben W. and
            {\v S}palek, Robert and Szegedy, Mario},
  title = {Quantum Query Complexity of State Conversion},
  booktitle = {2011 IEEE 52nd Annual Symposium on Foundations of Computer Science},
  pages = {344--353}, year = {2011}, doi = {10.1109/FOCS.2011.75},
  url = {https://arxiv.org/abs/1011.3020}
}
@article{PaigeSaunders1982,
  author = {Paige, Christopher C. and Saunders, Michael A.},
  title = {{LSQR}: An Algorithm for Sparse Linear Equations and Sparse Least Squares},
  journal = {ACM Transactions on Mathematical Software},
  volume = {8}, number = {1}, pages = {43--71}, year = {1982},
  doi = {10.1145/355984.355989}
}
@article{AugustinoEtAl2023,
  author = {Augustino, Brandon and Nannicini, Giacomo and Terlaky, Tam{\'a}s and Zuluaga, Luis F.},
  title = {Quantum Interior Point Methods for Semidefinite Optimization},
  journal = {Quantum}, volume = {7}, pages = {1110}, year = {2023},
  doi = {10.22331/q-2023-09-11-1110}
}
@article{DalzellEtAl2023,
  author = {Dalzell, Alexander M. and Clader, B. David and Salton, Grant and
            Berta, Mario and Lin, Cedric Yen-Yu and Bader, David A. and
            Stamatopoulos, Nikitas and Schuetz, Martin J. A. and
            Brand{\~a}o, Fernando G. S. L. and Katzgraber, Helmut G. and
            Zeng, William J.},
  title = {End-To-End Resource Analysis for Quantum Interior-Point Methods and Portfolio Optimization},
  journal = {PRX Quantum}, volume = {4}, number = {4}, pages = {040325},
  year = {2023}, doi = {10.1103/PRXQuantum.4.040325}
}
```
