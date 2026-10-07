# Recourse citation verification

Status: final source-reading and bibliography lane for the 16 assigned keys.
This is a bounded citation audit, not a discovery round or priority clearance.
The 16 keys resolve to 14 distinct works. Bibliographic identity, source-content
reading, and presence in the local literature KB are recorded separately.

## Key reconciliation and read status

| Supplied key | Canonical bibliography key | Verified source identity | Source-content status |
|---|---|---|---|
| `baotic2016-gradient-value-function` | `baotic2016-gradient-value-function` | Mato Baotić, “Gradient of the Value Function in Parametric Convex Optimization Problems,” 2016, arXiv:1607.00366; no DOI or journal publication verified. | Read complete arXiv v1 PDF; no local KB package. |
| `baotic2016-value-gradient` | `baotic2016-gradient-value-function` | Same Baotić work as above. | Same source and status as above. |
| `bienstock2018-lp-formulations-for-polynomial-optimization` | same | Daniel Bienstock and Gonzalo Muñoz, “LP Formulations for Polynomial Optimization Problems,” SIAM Journal on Optimization 28(2):1121–1150 (2018), DOI 10.1137/15M1054079, arXiv:1501.00288. | Read local `paper.md` and `fulltext.md`; checked against local `original.pdf`. |
| `hoffman1952-approximate-solutions` | same | Alan J. Hoffman, “On Approximate Solutions of Systems of Linear Inequalities,” Journal of Research of the National Bureau of Standards 49(4):263–265 (1952), DOI 10.6028/jres.049.027. Local KB slug includes “on”; citation key retained. | Read local `paper.md` and `fulltext.md`; checked against local `original.pdf`. |
| `kahl2005-globally-optimal-estimates` | same | Fredrik Kahl and Didier Henrion, “Globally Optimal Estimates for Geometric Reconstruction Problems,” ICCV 2005, pp. 978–985, DOI 10.1109/ICCV.2005.109. | Read complete lawful LAAS author PDF; no local KB package. The official UCSD record has a singular-title variant and mislinks its PDF to a different Kahl work. |
| `lasserre2009-convexity-sdp` | same | Jean B. Lasserre, “Convexity in Semialgebraic Geometry and Polynomial Optimization,” SIAM Journal on Optimization 19(4):1995–2014 (2009), DOI 10.1137/080728214, arXiv:0806.3784. | Read complete lawful author PDF; no local KB package. |
| `lasserre2010-joint-marginal` | same | Jean B. Lasserre, “A ‘Joint+Marginal’ Approach to Parametric Polynomial Optimization,” SIAM Journal on Optimization 20(4):1995–2022 (2010), DOI 10.1137/090759240, arXiv:0905.2497. | Read complete arXiv v1 PDF; no local KB package. |
| `miller2025-sparse-matrix` | same | Jared Miller, Jie Wang, and Feng Guo, “Sparse Polynomial Matrix Optimization,” SIAM Journal on Optimization 36(2):503–533 (2026), DOI 10.1137/24M1719761, arXiv:2411.15479. Key follows the manuscript's preprint label; BibTeX year is the journal year, 2026. | Read complete arXiv v3 PDF; no local KB package. |
| `pena2018-hoffman-constants` | same | Javier Peña, Juan Vera, and Luis F. Zuluaga, “An Algorithm to Compute the Hoffman Constant of a System of Linear Constraints,” 2018 preprint, arXiv:1804.08418; no journal or DOI verified. | Read complete author manuscript; no local KB package. |
| `piazzon2018-chebyshev-grids` | same | Federico Piazzon and Marco Vianello, “A Note on Total Degree Polynomial Optimization by Chebyshev Grids,” Optimization Letters 12(1):63–71 (2018), DOI 10.1007/s11590-017-1166-1. | Read complete lawful author manuscript and checked grid estimate against PDF; no local KB package. |
| `qu2024-correlatively-sparse-lagrange` | same | Zheng Qu and Xindong Tang, “A Correlatively Sparse Lagrange Multiplier Expression Relaxation for Polynomial Optimization,” SIAM Journal on Optimization 34(1):127–162 (2024), DOI 10.1137/22M1515689, arXiv:2208.03979. | Read complete arXiv v2 PDF; no local KB package. |
| `tondel2003-an-algorithm-for-multi-parametric` | `tondel2003-an-algorithm-for-multi-parametric` | Petter Tøndel, Tor Arne Johansen, and Alberto Bemporad, “An Algorithm for Multi-Parametric Quadratic Programming and Explicit MPC Solutions,” Automatica 39(3):489–497 (2003), DOI 10.1016/S0005-1098(02)00250-9. Local KB slug has a `tndel...` typo; canonical BibTeX/manuscript key spells the author's name correctly. | Read local `paper.md` and `fulltext.md`; checked theorem conditions against local `original.pdf`. |
| `tondel2003-mpqp` | `tondel2003-an-algorithm-for-multi-parametric` | Same Tøndel–Johansen–Bemporad work as above. | Same source and status as above. |
| `wang2025-a-moment-sum-of-squares` | same | Feng Guo and Jie Wang, “A Moment-Sum-of-Squares Hierarchy for Robust Polynomial Matrix Inequality Optimization with Sum-of-Squares Convexity,” Mathematics of Operations Research 50(3):1734–1761 (2025), DOI 10.1287/moor.2023.0361. | Read local `paper.md` and `fulltext.md`; checked scope and theorem against local `original.pdf`. |
| `zhang2025-wasserstein-moment` | same | Shixuan Zhang and Suhan Zhong, “Moment Relaxations for Data-Driven Wasserstein Distributionally Robust Optimization,” 2025 preprint, arXiv:2505.19278; no DOI or journal venue verified. Inspected v2 is dated 2026-09-04. | Read complete arXiv v2 PDF; no local KB package. |
| `zhong2024-two-stage-polynomial` | same | Suhan Zhong, Ying Cui, and Jiawang Nie, “Towards Global Solutions for Nonconvex Two-Stage Stochastic Programs: A Polynomial Lower Approximation Approach,” SIAM Journal on Optimization 34(4):3477–3505 (2024), DOI 10.1137/23M1615516, arXiv:2310.04243. | Read complete arXiv v2 PDF; no local KB package. |

`recourse-map.json` is the complete supplied-key-to-bibliography-key map. It
collapses both Baotić aliases and both Tøndel aliases; the local `tndel...`
slug is a package typo, not another source.

## Cited contracts, exact locators, and prose limits

| Work | Locator and source-supported claim | Manuscript status and limit/repair |
|---|---|---|
| Baotić (2016) | Corollary 3, arXiv v1 p. 5: for the strictly convex mp-QP with fixed (H\succ0), parameter-affine constraints, and full-dimensional feasible parameter set, LICQ at every feasible parameter gives (V\in C^1) on the interior and \(\nabla V=-S^T\lambda^*(x)\). | Sections 1 and 7 use this only as a parametric-QP sensitivity precedent. It does not prove differentiability at the closed-box boundary or general value-function smoothness; neither is claimed. The manuscript separately proves its closed-box sufficient proposition. |
| Bienstock–Muñoz (2018) | Theorem 4 / abstract, journal pp. 1121–1123 (arXiv pp. 1–2): bounded constraint-intersection treewidth \(\omega\) gives an approximate LP of size \(O((2\pi/\epsilon)^{\omega+1}n\log(\pi/\epsilon))\), with coefficient-scaled feasibility and objective error. Network extension: Theorem 7. | Introduction now uses this as a separate bounded-intersection-treewidth LP comparator. It does not prove the manuscript's Chebyshev recourse rate, junction-tree DP bound, or exact recourse theorem; the text no longer attributes those results to it. |
| Hoffman (1952) | Main theorem and proof, source pp. 1–2: with fixed matrix (A), a consistent (Ax\le b), and selected norms, distance to feasibility is bounded by a constant depending on (A) and the norms times the positive-residual norm. The bound is uniform over consistent right-hand sides. | Section 6's fixed stacked matrix and consistent moving right-hand sides meet this contract. Do not extend it to nonlinear rows or a matrix depending on shared variables. Current wording is supported. |
| Kahl–Henrion (2005) | Section 2.2, LAAS author PDF p. 3: partial relaxation linearizes only a limited subset of nonlinear PMI variables to reduce LMI size; that partial construction has no general asymptotic-convergence guarantee. A rank-one moment matrix on the lifted subset certifies a particular global optimum. | Sections 1, 2, and 6 now describe only limited-subset partial lifting and avoid a general convergence claim. Do not transfer full scalar-relaxation convergence from §2.1 to the partial relaxation. |
| Lasserre (2009) | Theorem 2.6, author PDF p. 6: for SOS-convex (f), a normalized positive truncated moment functional satisfies pseudomoment Jensen, (L_y(f)\ge f(L_y(X))), without a representing measure. Theorem 3.3 has separate finite-exactness assumptions. | Section 6 uses only the quadratic Jensen specialization. Do not imply Theorem 2.6 alone supplies a representing measure or finite convergence. Current use is supported. |
| Lasserre (2010) | §3, Theorem 3.5, arXiv v1 pp. 11–12: under compact parameter set, nonempty fibers, the stated joint-set assumptions, and prescribed parameter law \(\phi\), joint+marginal moment/SOS relaxations provide polynomial lower approximations converging in \(L^1(\phi)\); running maxima converge almost uniformly. | Section 7 calls this an established polynomial lower-approximation approach. It is qualitative, uses a growing joint degree and prescribed marginal, and does not prove fixed-private-degree convergence or sparse scalar-density gluing. Current use is supported. |
| Miller–Wang–Guo (2026 article) | §5, Theorem 5.1 and Example 5.1, arXiv v3 pp. 14–15: for matrix size (p=1), RIP plus local Archimedean certificates gives convergence; the explicit (p=2) example shows the matrix analogue can fail under those assumptions. | Section 6 uses this only to delimit generic matrix-valued sparse gluing. Do not say every sparse matrix hierarchy fails or scalar sparse convergence fails. Current wording is qualified. BibTeX uses the verified journal year 2026 although the inherited key has 2025. |
| Peña–Vera–Zuluaga (2018) | Introduction Eq. (1), source p. 1: (H(A)) depends only on fixed (A), uniformly over every right-hand side with a nonempty polyhedron. Proposition 1 and Proposition 3/proofs, pp. 3–6, cover constant characterizations and easy-to-satisfy constraints including box inequalities. | Section 6 uses it to clarify the uniform-right-hand-side and box-row version of Hoffman's bound. It neither gives a nonlinear error bound nor makes a sharp constant computationally available. Current use is supported. |
| Piazzon–Vianello (2018) | Lemma 1 and Proposition 2, author PDF pp. 3–4: for a total-degree-(n) polynomial on a hypercube, the product Chebyshev–Lobatto grid (X_{mn}) gives relative extrema error below \(2/m^2\); affine box changes preserve the estimate. | Section 6 says the manuscript's Chebyshev-grid bounds are “of this type.” The paper supports the polynomial-grid baseline, not the exact recourse rate, fiber projection repair, or junction-tree algorithm. Those exact statements come from the manuscript's corollary/proof. Current wording is supported. |
| Qu–Tang (2024) | §3, Eqs. (3.10)–(3.11), arXiv v2 pp. 9–10, constructs KKT/CS-LME expressions; §4.2, Theorem 4.2, gives convergence when a minimizer is KKT and each original local ideal module is Archimedean. Assumption 1 is algebraic nonsingularity: local constraint matrices have full column rank over complex points. | Section 7 describes the sparse KKT reformulation with multiplier equations and auxiliary variables. Do not call Assumption 1 real LICQ along the optimizer/recourse graph or attribute a quantitative rate for the unchanged affine-recourse hierarchy. Current use is supported. |
| Tøndel–Johansen–Bemporad (2003) | §3 and Theorem 1, article pp. 491–493 / local PDF pp. 2–4: under the source's nondegeneracy conditions, active-set critical regions give affine primal and multiplier policies and a piecewise-quadratic value; degeneracy is handled separately in §5. | Section 7 calls this a classical baseline under appropriate nondegeneracy assumptions. Do not infer unique multipliers without LICQ or claim a general-QP result. The manuscript's closed-box sufficient regime is separately stated and proved. |
| Guo–Wang (2025) | Problem (1), Assumption 1, hierarchy (21)–(23), pp. 2–5, and Theorem 7, pp. 15–16: the fixed-degree variables are decision variables (y), not uncertainty (x). The problem minimizes (f(y)) subject to \(\theta_i(y)\ge0\) and (P(y,x)\succeq0\) for every (x\in X\). It assumes SOS-convexity of (f,-\theta_i) in (y), PSD-SOS-convexity of \(-P(\cdot,x)\) in (y) for each (x\), compact (X), matrix-Archimedean uncertainty data, and Slater for convergence. The (y)-module degree is fixed at a selected decision degree while moment/localizing orders in (x) increase. | Introduction and Sections 2 and 6 now state this decision/uncertainty split precisely. It is not a fixed-degree uncertainty certificate and supplies no sparse recourse rate. The root has the exact supported one-sentence scope. |
| Zhang–Zhong (2025 preprint) | §4.1, Theorem 4.4 and proof Eq. (4.9), arXiv v2: under Assumption 1.1, bounded master set, a quadratic-module bound on second-stage (u), and stated degree conditions, the discrepancy is (O(r)) when the Wasserstein ball is parameterized by radius (r^p). Eq. (4.9) compares LPs with the same constraint matrix but perturbed right-hand sides controlled by private first-moment inconsistency. | Section 6 cites only a fixed-matrix first-moment sensitivity/repair precedent and states no Wasserstein rate. Do not label the source bound (O(\epsilon)) in actual (W_p)-radius \(\epsilon\): the source parameterization gives (O(\epsilon^{1/p})) under its assumptions. No prose change is needed. |
| Zhong–Cui–Nie (2024) | §2.1, discontinuous-recourse example immediately after Example 2.1, arXiv v2 p. 5: polynomial data with (xy=0) and box constraints yield value (-1) at (x=0), and 0 when (x\ne0). §4, Theorem 4.1, pp. 13–14, gives (L^1) convergence of polynomial lower approximations under an Archimedean joint module and continuous recourse value. | Section 6 says discontinuous recourse is a known phenomenon, which is supported. The cited example is not the manuscript's exact (P(u)=\{y\in[-1,1]:uy=0\}); do not identify them. The manuscript gives its own example, so no repair is needed. |

Sections 1, 2, 6, and 7 use works from this lane as described above. Section
10 has no citation from this 16-key set. The current prose reflects the source
corrections sent to the root: qualified Kahl scope, precise Guo–Wang degree split,
Bienstock as a separate LP comparator, and no Zhang–Zhong Wasserstein-rate
attribution.

## Local KB packaging and complete unretrieved list

Four of 14 works have usable local KB packages and were compared with their
originals: Bienstock–Muñoz, Hoffman, Tøndel–Johansen–Bemporad, and Guo–Wang.
Ten packages are absent from the KB. All 14 distinct works' source contents were
nevertheless retrieved lawfully and read into the unique system-temp directory
`/tmp/minlp-recourse-review.t25399`; the ten items below are KB packaging
requests, **not** unread or unretrieved source content. The deduplicated list of
unretrieved full texts is empty.

Route the following ten package requests through the existing shared literature
owner and serialized `$lit` session. Do not start an independent session.

1. Baotić, “Gradient of the Value Function in Parametric Convex Optimization
   Problems” (2016), arXiv:1607.00366; no DOI verified:
   https://arxiv.org/pdf/1607.00366
2. Kahl and Henrion, “Globally Optimal Estimates for Geometric Reconstruction
   Problems” (ICCV 2005), DOI 10.1109/ICCV.2005.109; author copy:
   https://homepages.laas.fr/henrion/Papers/vision.pdf
3. Lasserre, “Convexity in Semialgebraic Geometry and Polynomial Optimization”
   (2009), DOI 10.1137/080728214; author manuscript:
   https://optimization-online.org/wp-content/uploads/2008/07/2025.pdf
4. Lasserre, “A ‘Joint+Marginal’ Approach to Parametric Polynomial Optimization”
   (2010), DOI 10.1137/090759240:
   https://arxiv.org/pdf/0905.2497
5. Miller, Wang, and Guo, “Sparse Polynomial Matrix Optimization” (2026 journal
   article; 2025 preprint), DOI 10.1137/24M1719761:
   https://arxiv.org/pdf/2411.15479v3
6. Peña, Vera, and Zuluaga, “An Algorithm to Compute the Hoffman Constant of a
   System of Linear Constraints” (2018 preprint), arXiv:1804.08418; no DOI or
   journal publication verified:
   https://arxiv.org/pdf/1804.08418
7. Piazzon and Vianello, “A Note on Total Degree Polynomial Optimization by
   Chebyshev Grids” (2018), DOI 10.1007/s11590-017-1166-1; author manuscript:
   https://www.math.unipd.it/~marcov/pdf/opticheb.pdf
8. Qu and Tang, “A Correlatively Sparse Lagrange Multiplier Expression
   Relaxation for Polynomial Optimization” (2024), DOI 10.1137/22M1515689:
   https://arxiv.org/pdf/2208.03979
9. Zhang and Zhong, “Moment Relaxations for Data-Driven Wasserstein
   Distributionally Robust Optimization” (2025 preprint), arXiv:2505.19278;
   inspected v2 posted 2026-09-04, no DOI verified:
   https://arxiv.org/pdf/2505.19278v2
10. Zhong, Cui, and Nie, “Towards Global Solutions for Nonconvex Two-Stage
    Stochastic Programs: A Polynomial Lower Approximation Approach” (2024),
    DOI 10.1137/23M1615516:
    https://arxiv.org/pdf/2310.04243v2

No KB files were changed in this lane.
