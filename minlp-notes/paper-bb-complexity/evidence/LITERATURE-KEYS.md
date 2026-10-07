# Literature keys and claim scope

These are the stable ASCII keys currently cited by the manuscript. Each entry
names the claim the source can support; the source comparison and read locators
are recorded in `LITERATURE.md`. A few optional or metadata-only entries remain
in `references.bib` without an in-text citation; their status is recorded in
`LITERATURE.md`. A citation does not imply that the source proves the paper's
stronger node-count, propagation, or all-node claims.

## Spatial branch-and-bound and cluster behavior

| Key | Appropriate claim |
|---|---|
| `duKearfott1994Cluster` | Interval B&B cluster bounds for retained boxes near unconstrained minimizers under positive curvature and specified interval-extension order. |
| `wechsungSchaberBarton2014Cluster` | Fixed-width covering and prefactor-sensitive cluster bounds near a unique unconstrained nondegenerate minimum; includes a conservative fixed-parameter alphaBB estimate. |
| `kannanBarton2017ConstrainedCluster` | Constrained cluster analysis separating near-optimal feasible regions from infeasible regions and comparing lower-bound convergence order and prefactors. |
| `bachocCesariGerchinovitz2021LipschitzCertificates` | Near-tight instance-dependent sample-query complexity for certified Lipschitz black-box optimization; not a spatial B&B node bound. |
| `daskalakisDiakonikolasYannakakis2016ChordAlgorithm` | Competitive oracle-call analysis for Pareto-curve approximation in a two-objective Comb-oracle model; a different resource and optimization problem. |

## Convexification, face exactness, and propagation

| Key | Appropriate claim |
|---|---|
| `mccormick1976Computability` | Foundational recursive convex/concave estimators for factorable nonconvex programs and convergence under subdivision. |
| `rikun1997MultilinearEnvelope` | Exact multilinear envelope formula and face structure on boxes. |
| `adjimanDallwigFloudasNeumaier1998AlphaBBTheory` | Established alphaBB diagonal-shift convex underestimator and boxwise Hessian condition; it does not state the paper's face-exactness or node-complexity result. |
| `schichlMarkotNeumaier2014ExclusionRegions` | Fixed-scale interval overestimation/clustering and validated exclusion regions around Karush–John points; not an objective-cutoff tree-size result. |
| `belottiCafieriLeeLiberti2012FBBT` | FBBT as a monotone deflationary interval operator, its greatest fixed point, and non-finite convergence examples. |

## Sparse regression and binary least squares

| Key | Appropriate claim |
|---|---|
| `pilanciWainwrightElGhaoui2015BooleanRelaxation` | Boolean/perspective relaxation characterization and the exact printed hypotheses and conclusion of Theorem 2; the theorem is specifically audited as contradicted under its printed per-entry-noise model. Do not cite it as a valid corrected phase transition. |
| `xieDeng2018BooleanRelaxation` | Equivalence and strength comparisons among Boolean, mixed-integer conic, and perspective formulations; no random-design threshold. |
| `dongChenLinderoth2015SparseRegression` | Strong perspective/SDP relaxations and exactness certificates for statistical variable selection; no B&B or random-design tree threshold. |
| `atamturkGomez2019RankOneConvexification` | Rank-one quadratic convexification and its rank-one exact-hull case for sparse regression. |
| `atamturkGomez2020SafeScreening` | Safe dual screening rules for ℓ₀ regression from perspective relaxations. |
| `wainwright2009SharpLassoThresholds` | Gaussian-design support-recovery thresholds for the Lasso under the paper's tuning and minimum-signal conditions; distinct from optimal-decoder ML thresholds. |
| `hansenHassibiDimakisXu2009NearOptimalDetection` | Square real-AWGN binary ML detection model and its stated $2\ln N$ achievability condition; the source's proof is a sketch and must be qualified for vanishing-error use. |
| `hassibiHansenDimakisAlshamaryXu2014OptimizedMCMC` | Separate square real-Gaussian ML-error lemma with an explicit diverging margin above $2\ln N$, alongside an MCMC analysis that leaves polynomial mixing unresolved. |
| `huLu2020LimitingPoissonMIMO` | Fixed-sequence box least-squares/sign-rounding recovery threshold under the stated Gaussian sampling and noise assumptions; not an all-node union or PWE normalization. |
| `mccoyTropp2014SteinerFormulas` | Master Steiner formula and chi-square mixture for projection of a standard Gaussian vector onto a fixed convex cone. |
| `hugSchneider2016RandomConicalTessellations` | Expected intrinsic-volume weights of Cover–Efron cones, yielding the aggregate binomial face-dimension law in the cited generator regime. |

## Analytic singularities and Gaussian concentration inputs

| Key | Appropriate claim |
|---|---|
| `lin2017LearningCoefficient` | Analytic marginal-likelihood/sublevel asymptotics on compact semianalytic domains, including boundary contributions; an analytic input, not a B&B theorem. |
| `laurentMassart2000ChiSquare` | Upper and lower chi-square tail inequalities in Lemma 1 and equations (4.3)–(4.4), for $x>0$. |
| `davidsonSzarek2001LocalOperatorTheory` | Gaussian extreme singular-value inequalities in the chapter's stated matrix normalization. |
| `davidsonSzarek2003Corrigendum` | Correction restoring the missing $\sqrt{d}$ scale in the cited 2001 Gaussian-tail display. |

## Integer lower bounds, lattice inputs, and decomposition

| Key | Appropriate claim |
|---|---|
| `deyDubeyMolinaro2023BranchAndBoundLowerBounds` | Pairwise-conflict and leaf lower-bound mechanisms for abstract general integer-split B&B trees; different from the paper's semantic convex-hull class number. |
| `kaibelWeltge2015LowerBoundsBranchAndBound` | Hiding-set lower bounds for integer formulation complexity without auxiliary variables; not itself a B&B tree-size theorem. |
| `basuConfortiCornuejolsZambelli2010MaximalLatticeFree` | Full-dimensional maximal lattice-free polyhedron has at most $2^n$ facets, with the theorem's full-dimensionality and lattice-free hypotheses. |
| `skenderi2021RandomLatticesSiegel` | Haar mean-value identity for all nonzero vectors of a unimodular lattice, including its Borel $L^1$ test-function conditions and normalization. |
| `marinescuDechter2009AndOrBranchAndBound` | Finite-domain AND/OR B&B complexity controlled by pseudo-tree depth/treewidth and mini-bucket bounds. |
| `deGivrySchiexVerfaillie2006TreeDecomposition` | Separator-conditioned weighted-CSP BTD+ search bounds in finite domains. |
| `bienstockMunoz2018LpFormulations` | Approximate LP formulations for bounded-treewidth polynomial optimization with explicit dependence on accuracy and structural parameters. |

## Scope notes

- The Hu–Lu box decoder and the Pilanci–Wainwright–El Ghaoui
  perspective relaxation are separate results with different models and
  normalizations. Hu–Lu's single-sequence threshold does not justify a union
  over all B&B nodes.
- For PWE Theorem 2, the source states iid $N(0,1)$ design entries, iid
  per-entry $N(0,\gamma^2)$ noise, ridge $\rho=\sqrt n$, and the condition
  $n>c_0(\gamma^2+\|w^*_S\|^2)\log d/w_{\min}^2$, with claimed exactness
  probability at least $1-2e^{-c_1n}$. The finite-dimensional audit in
  `LITERATURE.md` shows the fixed-SNR limit is strictly below one under that
  printed model. Do not transfer the contradiction or proposed repairs to a
  shrinking total-noise model.
- Hansen–Hassibi–Dimakis–Xu (2009) and Hassibi et al. (2014) are square
  real-Gaussian ML-decoding inputs; the latter makes the diverging margin
  explicit. Hu–Lu is a distinct box-relaxation decoder. None proves the
  paper's all-node certificate probability.
- For Lin (2017), use the compact-semianalytic-domain analytic sublevel
  asymptotic theorem when a root-box face contributes. It allows the restricted
  analytic gap to be nonnegative only on the closed box/face. An identically
  zero face is handled by the manuscript's separate scaling convention, not
  called an ordinary RLCT pair.
- The Jeroslow parity construction in the manuscript is self-contained and
  carries no priority claim; no Jeroslow key is retained. The original Siegel
  theorem is likewise not claimed as directly inspected: the accessible
  Skenderi theorem is cited for the exact normalization.
- Unread, metadata-only, rejected-ingest, and post-cutoff candidates are not
  citation keys. Their status and relevance are recorded in `LITERATURE.md`
  and the run account.
