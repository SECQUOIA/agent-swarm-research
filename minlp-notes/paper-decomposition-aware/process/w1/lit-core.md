# Related-work memo: certified coordinate grids, filtering, conditioned complexity, exact output

Date: 2026-10-03. Cluster key: `lit-core`. Companion files:
`lit-core.bib` (checked BibTeX), `lit-core-proofs.tex` (paper fragment with
two new propositions and a draft related-work subsection),
`lit-core-report.md` (verdict, issues, placement, open questions), and
`checks/lit_core_cell_equivalence.py` (exact-arithmetic support check).

Page locators are printed page numbers when a journal page is shown, else
PDF pages (marked "PDF p."). "Read" means the cited statement was checked in
the primary full text. "Abstract" means only the abstract or publisher
summary was available. Nothing below is a priority clearance; absence of a
match in searches is not proof of novelty.

## 1. Summary of findings

| Contribution | Closest prior work | Relation | Threat |
|---|---|---|---|
| (1) Unary node correction `L w^2/8` makes a finite-grid tree DP a valid continuous lower bound | Bajaj and Hasan 2020 (Optim. Lett. 14:1011-1026), Theorem 1; Hasan 2018 edge-concave underestimators; alphaBB separation formula (Maranas-Floudas 1994; Adjiman et al. 1998, p. 1141) | The single-box inequality `F >= min_vertices F - (L/8) sum_i Delta_i^2` under an upper bound on diagonal Hessian entries is published (Bajaj-Hasan). New: the node-separable form; it equals the minimum of these bounds over all cells of a product grid (proved in `lit-core-proofs.tex`, Prop. `prop:lc-cellwise`), so one tree DP evaluates it in `K^p` table work instead of enumerating `K^n` cells with `2^n` vertices; integer unit intervals; conditional version for filtering | High for the inequality; medium for the contribution as reformulated |
| (2) Min-marginal interval filtering with full-history certificate | OBBT, probing and aggressive bounds tightening (Belotti et al. 2009, Sec. 4.1 and 4.3; Puranik-Sahinidis 2017, pp. 11-14; Ryoo-Sahinidis 1996); max-marginals by two-pass message passing (Wainwright-Jaakkola-Willsky 2005, Sec. V.A; Kohli-Torr 2006); cost-based filtering; dead-end elimination incl. continuous rotamers (Gainza et al. 2012) | The filter is the standard rule "drop a region whose relaxation bound exceeds the incumbent", with all per-interval bounds obtained from one pair of message passes. The history argument is standard branch-and-bound proof logic. New only through its use: retained coordinate hulls shrink with the mesh under global growth | High (as a stand-alone contribution) |
| (3) Accuracy-independent grid sizes under quadratic growth; `f(p,kappa) poly(I+q)` | Cluster problem: Du-Kearfott 1994; Neumaier 2004, Sec. 15 (preprint pp. 43-44); Wechsung-Schaber-Barton 2014; Kannan-Barton 2017, Thm 3 and Remark 5 (pp. 651-653). Optimistic optimization: Munos 2011, Cor. 1 and Example 2. Perevozchikov 1990. Treewidth/conditioning: Bhathena et al. 2026; Del Pia-Khajavirad 2026 | B&B theory already shows that second-order bounds plus a nondegenerate minimizer give a box count independent of the tolerance, but locally, asymptotically, and exponential in dimension and Hessian conditioning. Optimistic optimization gives exponential rates when growth matches smoothness, also exponential in dimension. No found work gives a global, non-asymptotic count with treewidth replacing dimension, or the `f(p,kappa)poly(I+q)` bit bound for nonconvex/mixed box QP | Medium (mechanism known; formal result not found) |
| (4) Exact rational output | Vavasis 1990 (TR 90-1099 Sec. 2: max-active optimizer, PD reduced Hessian, Edmonds); Del Pia-Dey-Molinaro 2017, Thm 3; continued fractions (Grötschel-Lovász-Schrijver 1988, Thm 5.1.9, p. 137); Kozlov-Tarasov-Khachiyan 1980 rounding | Each ingredient is classical; the rational-height lemma of the report reproduces Vavasis's argument. New: only the composition with the FPT approximation (exact output in `f(p,kappa) poly(I)` without knowing `g`) | Low for the composition, high for any ingredient-level novelty claim |

Additional result added in this cluster (see `lit-core-proofs.tex`):
Proposition `prop:lc-necessity` shows that, unless P = NP, no algorithm
approximates the value of a treewidth-two continuous box QP within `2^{-q}`
in time `poly(I+q)`. Corollary `cor:lc-illconditioned` deduces that every
NP-hardness reduction at treewidth two must produce non-unique or
super-polynomially ill-conditioned instances. Remark `rem:lc-eth` notes the
ETH reason why `2^{Omega(p)}` is unavoidable. Together these make both
parameters of `f(p,kappa)` necessary.

## 2. Contribution (1): corrected grid lower bound

### 2.1 Closest prior: edge-concave vertex bounds

- **Bajaj and Hasan, "Deterministic global derivative-free optimization of
  black-box problems with bounded Hessian", Optim. Lett. 14(4):1011-1026
  (2020; online 2019).** Abstract and the publisher's article page
  (section list, Theorem 1, Property 1) were read; full text is paywalled.
  Assumption: "a global upper bound on the diagonal Hessian elements is
  known". Theorem 1: `LB = min_{v in V} [f(x^v) - Theta sum_i (x_i^v -
  x_i^m)^2]` over the `2^n` box vertices, `x^m` the box midpoint. Property 1:
  maximum separation `(Theta/4) sum_i (x_i^u - x_i^l)^2`. With `Theta = L/2`
  (needed for edge-concavity of `f - Theta sum (x_i - x_i^m)^2`; the exact
  constant convention of the paper was not checked) this is exactly the
  report's per-cell correction `L Delta^2/8`. They embed it in box branch
  and bound. Relation: same inequality, same assumption (upper coordinate
  curvature, function values only). Difference: one box at a time with
  `2^n` vertex evaluations; no grid, no tree decomposition, no node-separable
  form, no complexity bound. Threat: high for the inequality.
- **Hasan, "An edge-concave underestimator ...", JOGO 71(4):735-752 (2018).**
  Abstract (RePEc). Subtracting a positive quadratic makes the function
  edge-concave (componentwise concave); its convex envelope is vertex
  polyhedral and gives an LP relaxation. Follow-ups: Bajaj-Hasan,
  JOGO 77(3):487-512 (2020) for dynamic optimization; Nath Roy-Hasan, JOGO
  (online 2025-11-25) "separable edge-concave underestimator" uses `n+1`
  vertices instead of `2^n` (abstract; no DP or sparsity).
- **Vertex polyhedral envelopes.** Tardella 2004 (Frontiers in Global
  Optimization, pp. 563-573); Meyer-Floudas 2005 (Math. Program.
  103:207-224); Misener-Floudas 2012 (Math. Program. 136:155-182) use
  edge-concave relaxations in MIQCQP. SCIP 8 documents edge-concave cuts
  (Bestuzheva et al. 2025, Sec. 2.3.6, local package) — metadata of SCIP
  paper not added to the bib.
- **alphaBB.** Adjiman, Dallwig, Floudas, Neumaier 1998, Part I, p. 1141
  (read): maximum separation `d_max = (1/4) sum_i alpha_i (x_i^U - x_i^L)^2`,
  attributed to Maranas-Floudas 1994. The report's correction is the
  alphaBB separation with `alpha = L/2`, applied with the opposite sign
  (to make `F` coordinatewise concave rather than convex).

### 2.2 New statement proved in this cluster

`lit-core-proofs.tex`, Proposition `prop:lc-cellwise`:
(a) deterministic proof of validity of every cell bound (replaces the
randomized-rounding proof of the report's Lemma 3.1); (b) the corrected
grid minimum `beta = min_y [F(y) - D(y)]` equals `min_C beta(C)` over all
cells `C` of the product grid, where `beta(C)` is the Bajaj-Hasan vertex
bound with effective widths; (c) for a coordinate interval `I=[a,a^+]`,
`min{beta(C): C_i = I} = min_{v in {a,a^+}} (m_i(v)+d_i(v)) - L Delta_i(I)^2/8
>= min{m_i(a), m_i(a^+)}`, a free sharpening of the report's retention test
that preserves both properties used by the localization lemma.
Exact-arithmetic support: `checks/lit_core_cell_equivalence.py`
(120 random instances, `n <= 3`, nonuniform grids, mixed integer/continuous
coordinates; identity (b) and (c) hold exactly; random-point validity spot
checks pass). Run time about 5 s.

Defensible novelty statement: "The cell bound is the edge-concave vertex
bound of [Bajaj-Hasan 2020]. To our knowledge, its node-separable form,
which turns the minimum over all cells of a product grid into a factorized
min-sum problem solvable on a tree decomposition, has not been used
before." Do not claim the inequality.

### 2.3 Other comparators (lower threat)

- **Piecewise-linear and sawtooth relaxations of squares.** Beach,
  Hildebrand, Huchette 2022 (JOGO 84:869-912; read): Yarotsky sawtooth MIP
  formulation of `x^2`, diagonal perturbation to separate a quadratic. Beach,
  Burlacu, Bärmann, Hager, Hildebrand 2024 (COAP 87:835-891; read): depth-`L`
  sawtooth interpolation overestimates `x^2` on `[0,1]` by at most
  `2^{-2L-2}`, and the sawtooth relaxation shifts each approximant down by
  that amount (PDF pp. 8-12). This equals `L_curv Delta^2/8` with curvature 2
  and `Delta = 2^{-L}`. Dong-Luo 2018 (arXiv:1811.08122, Thm 1, PDF pp. 8-9;
  read via local package): `|y-x^2| <= [max(l^2,u^2)+1]^2/2^{2nu-2}` with
  `nu` binaries. Relation: same second-order error, applied termwise to
  squares in a MIP. Differences: per-term, needs a MIP solver, no DP. Note:
  the 2022 paper's authors are Beach, Hildebrand, Huchette; Burlacu and
  Hager are coauthors of the 2024 COAP paper.
- **Grid search bounds.** Lipschitz passive grids and sequential methods
  (Piyavskii 1972; Shubert 1972; Nesterov 2004, Sec. 1.1 uniform grid
  method — section locator from memory, not rechecked). de Klerk, Lasserre,
  Laurent, Sun 2017 (MOR 42:834-853; arXiv v2 introduction read): grid search
  over the hypercube with denominator `k` converges at rate `O(1/k^2)` by
  Taylor's theorem. These give the classical mesh-squared error; none
  combines it with tree DP.
- **Vavasis 1992 (Math. Program. 57:279-311; read):** interpolates the
  concave part of an indefinite QP linearly on a grid over the `t` negative
  directions and solves one convex QP per subcube; the dual arrangement of
  the present one (here positive curvature is corrected and negative
  curvature is free).

## 3. Interval/coarse-state DP for continuous variables

- **Raphael, "Coarse-to-fine dynamic programming", IEEE TPAMI
  23(12):1379-1390 (2001).** Author PDF read (Sec. 2, Sec. 3, Appendix).
  Superstates with optimistic (lower-bound) arc costs make each coarse DP a
  lower bound; superstates along the current optimal path are refined; the
  algorithm stops at a provably optimal path. A continuous-state version on
  rectangles is given, with a convergence proposition under a unique
  maximizer (Appendix). Worst case may refine everything; no complexity
  bound. This is the closest conceptual predecessor for "coarse states with
  optimistic costs give a certified DP lower bound and are refined near the
  optimum". Differences: chain DP, problem-specific arc bounds (exact
  minimization over superstate pairs), no generic curvature correction, no
  rate. A referee in vision/AI is likely to know it.
- **Peng, Hazan, McAllester, Urtasun, ICML 2011, pp. 729-736.** Official
  title "Convex Max-Product over Compact Sets for Protein Folding" (the PDF
  title is "Convex Max-Product Algorithms for Continuous MRFs with
  Applications to Protein Folding"). Sec. 4.2 (read): "interval convex
  max-product" bounds potentials from below on interval cells, so the value
  of the discrete MRF is a lower bound on the continuous MRF, and refines
  intervals with positive primal mass; provably converges to the value of
  the continuous Lagrangian relaxation. Differences: factorwise interval
  bounds, dual relaxation rather than exact tree DP, no rate.
- **Dvijotham et al., Constraints 22:24-49 (2017).** Theorem 2, pp. 16-17
  (read): interval DP on trees for OPF; constraint violation at most
  `zeta eps`, cost at most OPT, at most `n zeta' eps^{-5}` PropBound calls.
  The arXiv HTML numbers it Theorem 4.1.
- **Hoang et al., AAMAS 2020, pp. 502-509.** Theorems 5.1-5.2 (local
  package): discretized DPOP error `|F| m delta`; AC-DPOP error
  `|F|(m+|A|k alpha delta) delta` under gradient bounds.
- **Troullinos et al., IJCAI 2022, pp. 518-526:** quadtree-adaptive Max-Sum;
  guarantees left as future work. **Munos-Moore 2002** (ML 49:291-323):
  variable-resolution discretization for control. **Heidari et al. 1971**
  (WRR 7:273-282): DDDP corridors around a trial trajectory, may stop at a
  local optimum. **Leaver-Fay, Kuhlman, Snoeyink, PSB 2005, pp. 16-27**
  (read): treewidth DP and adaptive two-level states; Theorem 2.2 bounds
  the error by `2 eps |E_2|`.
- **Sun, Telaprolu, Lee, Savarese, AISTATS 2012, pp. 1134-1142**
  (abstract): exact discrete MAP by branch and bound over label sets with
  fast bound evaluation.

None gives a state count independent of the target accuracy.

## 4. Contribution (2): filtering

- **Belotti, Lee, Liberti, Margot, Wächter, OMS 24:597-634 (2009).** Read.
  Sec. 4.1 OBBT; Sec. 4.3 (preprint p. 11) Aggressive Bounds Tightening:
  "FBBT is applied to portions of B that exclude x̂^k. The portions yielding
  a problem that is infeasible or a lower bound above the cutoff value ...
  can be excluded", per variable. This is the report's retention rule with a
  different relaxation.
- **Puranik and Sahinidis, Constraints 22:338-376 (2017).** Read (local
  package): optimality-based reduction may remove feasible points if all
  better solutions remain (pp. 11-12); probing with the objective bound
  (pp. 12-14); cluster effect and second-order bounds (p. 15).
- **Ryoo-Sahinidis 1996** (JOGO 8:107-138; meta), **Gleixner et al. 2017**
  (JOGO 67:731-757; read: OBBT with objective cutoff, Lagrangian variable
  bounds).
- **Min-marginals.** Wainwright, Jaakkola, Willsky 2005, Sec. V.A,
  pp. 3705-3706 (read): max-marginals of tree distributions, eqs. (33)-(36),
  computed by max-product on trees, attributed there to Dawid 1992 and
  others. Kohli-Torr 2006, ECCV LNCS pp. 30-43, DOI 10.1007/11744047_3
  (read): min-marginal energies, exact for trees by BP, dynamic graph cuts
  for submodular binary MRFs. Aji-McEliece 2000 (GDL; meta). Dawid 1992
  (meta).
- **Cost-based filtering and DEE.** Focacci, Lodi, Milano 1999 (CP'99,
  pp. 189-203; meta); Desmet et al. 1992 (Nature 356:539-542; meta);
  Gainza, Roberts, Donald 2012 (PLoS Comput. Biol. 8:e1002335; PMC full
  text): iMinDEE prunes continuous rotamer voxels when a lower bound from
  minimized pairwise energies plus an interval term exceeds the incumbent
  (Eq. 7, Propositions 1-2), with a guarantee that the minimized GMEC is
  found. This is the closest "provable pruning of continuous label
  regions" precedent.
- **Max-marginal thresholds.** Weiss-Taskar 2010 (AISTATS, PMLR 9:916-923;
  abstract): structured prediction cascades filter states by max-marginal
  thresholds, learned to balance filtering error against efficiency. Parisot et al. 2014 (MedIA
  18:647-659; read per local package): min-marginal-guided label and grid refinement,
  heuristic.
- **Certificates.** Cheung, Gleixner, Steffy, IPCO 2017, LNCS pp. 148-160
  (VIPR; meta): checkable branch-and-bound certificates. The report's
  "full-history" certificate has the same logic: every pruned region is
  certified at the time it is pruned against a then-valid incumbent.

Defensible statement: "The filter is optimality-based bounds tightening in
which all interval bounds come from one pair of message passes. What is new
is the localization: under global quadratic growth, every retained
coordinate hull lies within `O(sqrt(n kappa) h)` of the corrected
minimizer." Threat as a stand-alone contribution: high.

## 5. Contribution (3): accuracy-independent state counts

### 5.1 Cluster problem in branch and bound (closest mechanism)

- **Neumaier, Acta Numerica 13:271-369 (2004), Sec. 15, preprint pp. 43-44 (read).**
  If bounds over boxes of diameter `eps` have accuracy `K eps^{s+1}`, the
  number of uneliminated boxes near a nondegenerate minimizer is, for
  `s = 1` (second order), "essentially independent of eps" but "may still
  grow exponentially with the dimension, and it is especially large for
  problems where the Hessian at the solution is ill-conditioned".
- **Du and Kearfott 1994** (JOGO 5:253-265; meta; content via Neumaier and
  Kannan-Barton): first analysis; at least second-order bounds are needed.
- **Wechsung, Schaber, Barton 2014** (JOGO 58:429-438; abstract from MIT
  DSpace record; full text not retrievable): a threshold on the
  second-order prefactor eliminates clustering; a conservative prefactor is
  given for alphaBB.
- **Kannan and Barton 2017** (JOGO 69:629-676; read): Theorem 3 and
  Remark 5 (pp. 651-653): with a lower-bounding scheme of order `beta*`,
  the number of width-`delta` boxes covering the nearly optimal region
  scales as `O(eps^{n(1/2 - 1/beta*)})`, so it is independent of `eps` for
  second-order schemes; Lemma 8 uses local quadratic growth.

Relation to (3): the same phenomenon — second-order bounds plus quadratic
growth make the active region at mesh `h` have size `O(sqrt(kappa) h)`. The
report's contraction lemma is the global, non-asymptotic, constructive
version, and its filtering is coordinatewise, so the count is
`K = O(sqrt(kappa) log n)` per coordinate and `K^p` per bag instead of
`(C sqrt(kappa))^n` boxes. This is the defensible difference.

### 5.2 Optimistic optimization and log-complexity under matched growth

- **Munos, NIPS 2011, pp. 783-791 (read).** Theorem 1 and Corollary 1:
  near-optimality dimension `d = 0` gives loss `c gamma^{(n/C)-1}`
  (exponential rate); Example 2: for `f` locally equivalent to
  `||x - x*||^alpha` and semi-metric `c||x-y||^beta` with `beta = alpha`,
  `d = 0`. SOO attains nearly the same without knowing the semi-metric.
  The constant `C` (packing number) is exponential in the dimension. This is
  the analogue of "growth constant not needed" and of `log(1/eps)` rates.
- **Perevozchikov 1990** (USSR CMMP 30(2):28-33; abstract from Math-Net.Ru):
  for Lipschitz functions whose `eps`-optimal sets have measure
  `O(eps^{rn})`, branch-and-bound uses `O(eps^{-n(1-r)})` values, and
  `O(ln(1/eps))` when `r = 1`.

### 5.3 Proximity and scaling (integer domains)

- **Hochbaum-Shanthikumar 1990** (JACM 37:843-862; read): proximity
  `n Delta` between scaled and fine solutions; logarithmic dependence on
  range for separable convex optimization over linear constraints.
- **Cook, Gerards, Schrijver, Tardos 1986** (Math. Program. 34:251-264;
  meta) and **Granot-Skorin-Kapov 1990** (Math. Program. 47:259-268;
  abstract read): proximity `n Delta(A)` for linear and separable quadratic
  IP, extended to nonseparable mixed-integer QP.
- **Hunkenschröder, Koutecký, Levin, Vu 2026** (Math. Program., online
  2026-03-18; arXiv:2505.22212 read via local package): separable convex
  IP with small coefficients and bounded primal/dual treedepth in
  `g(td, ||A||) n log(max(||u-l||, ||b||))` (Thms 1-2, p. 3); an
  `n log ||u - l||` comparison lower bound for the box case.
- **Eisenbrand et al. 2025** (MOR 50:2141-2156; abstract): IP is FPT in a
  numeric measure and a sparsity measure of `A`; extends to separable
  convex objectives.

Relation: the same "large domain costs only its logarithm" goal, reached by
proximity for separable convex objectives with structured linear
constraints. The report has nonseparable nonconvex objectives on a box with
a growth promise. Threat: low.

### 5.4 Treewidth and conditioning for QP

- **Del Pia and Khajavirad 2026** (arXiv:2609.35595v1, read): Theorem 1
  (PDF p. 4): forest box QP in `O(n^2)` operations, strongly polynomial.
  Theorem 2 (p. 18): quartic minimization strongly NP-hard on a path.
  Theorem 3 (p. 20): strongly NP-hard at treewidth two with `Q, c` integral,
  `||Q||_max <= 5`, `||c||_inf <= 4`. Theorems 4-6 (pp. 27-38): classes of
  unbounded treewidth via binary endpoint variables. Their Lemma 20 (from
  Khajavirad [22]) uses a parameter also called `kappa` (number of rows to
  delete before all principal submatrices are PSD) — a notation clash with
  the report's `kappa = max(1, L/g)`.
- **Khajavirad 2026** (arXiv:2604.25033v2; abstract): exact polynomial
  classes for sparse box polynomial optimization; Turing model for
  quadratics.
- **Bhathena et al. 2026** (arXiv:2603.02103v1; read): Definition 5
  (`(k,eta)`-margin), Theorem 1 (`O(n omega^2 delta k^{2 delta} 4^{Delta_{m+1}})`
  time) under polynomial volume growth; dependence on conditioning.
  Trees: Math. Program. 218:291-336 (2026), exact `O(n^2)` (cited by Del
  Pia-Khajavirad, p. 16).
- **Bienstock-Chen 2024** (arXiv:2411.11722; read via local package):
  treewidth FPTAS with `1/eps` dependence for convex block-indicator QP.
- **Eiben, Ganian, Knop, Ordyniak, AAAI 2019** (read): Theorem 8 (p. 5):
  IP in `O((2d+1)^{omega+2}|I|)` given a width-`omega` decomposition of the
  mixed primal graph and maximum domain `d`; Corollary 11 (p. 6): IQP FPT
  in maximum domain and treewidth; Theorem 4: NP-hard without structure.
  Ganian-Ordyniak 2018 (AIJ 257:61-71; meta); Lokshtanov 2015
  (arXiv:1511.00310; abstract): IQP FPT in `n + a`.
- **Bienstock and Muñoz 2018** (SIOPT 28:1121-1150; read): Theorem 4
  (preprint p. 2): LP of size `O((2pi/eps)^{omega+1} n log(pi/eps))` with
  scaled tolerances; p. 2 and Appendix A (pp. 23-25): improving the
  `1/eps` dependence to polynomial in `log(1/eps)` is impossible unless
  P = NP, by a subset-sum construction.
- **Vavasis 1992** (p. 32 per local package): better dependence on
  `log(1/eps)` would contradict NP-hardness. **Del Pia 2026 Jacobi**
  (arXiv:2607.29386v1; read): Theorem 1 (pp. 1-2), and the `1/eps`
  dependence cannot be dropped because QP with one negative eigenvalue is
  NP-hard (Pardalos-Vavasis 1991).

Defensible novelty statement for (3): "To our knowledge, no earlier result
gives a running time `f(p,kappa) poly(I+q)` — or an exact algorithm in time
`f(p,kappa) poly(I)` — for nonconvex or mixed-integer box QPs. The closest
mechanism, the cluster analysis of branch and bound, is local, asymptotic
and exponential in the dimension." Threat: medium.

### 5.5 Quadratic growth and unknown constants

- Luo-Tseng 1993 (Ann. OR 46:157-178; meta); Drusvyatskiy-Lewis 2018 (MOR
  43:919-948; arXiv v2 read: Thm 3.3, Cor. 3.6-3.7: error bound and
  quadratic growth equivalence and linear convergence, convex setting);
  Necoara-Nesterov-Glineur 2019; Karimi-Nutini-Schmidt 2016 (meta).
  Roulet-d'Aspremont 2020 (SIOPT 30:262-289; meta): restart schemes adapt
  to unknown sharpness. Relation: QG is the standard condition for
  `log(1/eps)` iteration counts of local methods; the report uses it
  globally for a nonconvex mixed problem, and the "guess `theta`, cap the
  state count" schedule is a standard doubling/restart device.

## 6. Contribution (4): exact output

- **Vavasis, "Quadratic programming is in NP", IPL 36(2):73-77 (1990).**
  The Cornell technical report TR 90-1099 (February 1990, 11 pages) was
  retrieved from Cornell eCommons (scanned; read by OCR). Sec. 2 (TR
  pp. 3-6): among global minima choose one with the most active
  constraints (ties: most zero coordinates); the reduced Hessian on the
  active affine subspace is positive semidefinite, and positive definite
  because a null direction could activate another constraint; the
  optimizer solves two linear systems and has polynomial encoding length by
  Edmonds's theorem. The report's Lemma 5.1 (rational height) is this
  argument specialized to boxes with an explicit Cramer bound. The IPL
  page numbers of these passages were not checked.
- **Del Pia, Dey, Molinaro 2017** (Math. Program. 162:225-240; read):
  Theorem 3 restates Vavasis: a global optimizer of a rational QP that
  attains its minimum solves a rational linear system of small complexity.
- **Continued fractions.** Grötschel-Lovász-Schrijver 1988, Sec. 5.1
  (pp. 134-137), Theorem (5.1.9), p. 137 (read): best approximation with
  bounded denominator in polynomial time; Sec. 1.3 remarks that a rational
  number with known denominator bound can be recovered exactly from an
  approximation. Schrijver 1986, Sec. 6.1 (not rechecked).
- **Kozlov-Tarasov-Khachiyan 1980** (read per source ledger): exact
  rational convex QP by rounding an approximate solution.
- **Uniqueness implies quadratic growth.** Contesse 1980 (Numer. Math.
  34:315-332; abstract read): for QP, second-order necessary conditions for
  local minima are sufficient and second-order sufficient conditions are
  necessary. Hence a strict local minimizer of a QP has local quadratic
  growth; global growth on a compact box follows by compactness. Bonnans-
  Ioffe 1995 (meta) for nonisolated minima; Luo-Sturm 2000, Thm 3.3
  (PDF pp. 11-12 per the source ledger) for set-valued error
  bounds. The report's Lemma 5.2 is a standard argument and should be
  presented as such.
- **Polynomials.** Bienstock, Del Pia, Hildebrand 2023 (Math. Program.
  197:661-692; read): encoding-size dichotomies and irrational optima for
  degree three and higher (Thm 2.6, pp. 4-8; Prop. 2.11). Supports the
  report's remark that exact continuous polynomial output needs separate
  obligations.

Defensible statement: "Exact recovery uses only classical tools (rational
height [Vavasis; Del Pia-Dey-Molinaro] and continued fractions
[Grötschel-Lovász-Schrijver]); the new point is that the conditioned
approximation bound transfers to exact output with `O(log kappa) + poly(I)`
accuracy bits, without knowing `g`." Threat: low as stated; high if
ingredients are claimed.

## 7. Background a referee will expect

Binary/discrete treewidth DP and relaxations: Bertelè-Brioschi 1972;
Lauritzen-Spiegelhalter 1988; Crama-Hansen-Jaumard 1990; Dechter 1999;
Aji-McEliece 2000; Bienstock-Özbay 2004 (level-`omega` Sherali-Adams exact
for packing IPs of treewidth `omega - 1`, as described by Bienstock-Muñoz,
preprint p. 3); Wainwright-Jordan 2004 TR 671 (read title page and
abstract); Laurent 2009, Sec. 8.1-8.2, author PDF pp. 89-102 (read: sparse Putinar
Theorem 8.9; LP of size `O(n 2^kappa)` for partial `kappa`-trees, author PDF
pp. 101-102);
Waki et al. 2006; Lasserre 2006. Global optimization: Horst-Tuy 1996
(vertex optimality of concave minimization); Rosenberg 1972 (multilinear
functions on boxes attain extrema at vertices; meta). Complexity:
Bodlaender 1996; Impagliazzo-Paturi-Zane 2001; Lokshtanov-Marx-Saurabh
2018 (arXiv 1007.5450 Thm 1 read: no `(2-eps)^{tw}` algorithm for
independent set under SETH). Indefinite QP approximation: Vavasis 1992;
Hildebrand-Weismantel-Zemmer 2016; Del Pia 2023; Del Pia 2026; De Loera et
al. 2008 (fixed-dimension mixed-integer FPTAS). Sparse SDP exactness:
Khajavirad 2026 (arXiv:2601.18545). All are in `lit-core.bib`.

## 8. Corrections to existing statements and internal notes

1. Report Sec. 1 and abstract: the correction is presented without
   attribution. Cite Bajaj-Hasan 2020, Hasan 2018 and the alphaBB
   separation formula, and state the node-separable reformulation as the
   contribution (see `lit-core-report.md`, issue M1).
2. Report Lemma 5.1: credit Vavasis 1990 for the argument.
3. Report Lemma 5.2: credit second-order QP theory (Contesse 1980).
4. Report Sec. 3.2 "familiar junction-tree computation": add
   Bertelè-Brioschi 1972, Lauritzen-Spiegelhalter 1988 and, for
   min-marginals, Wainwright et al. 2005 Sec. V.A.
5. Internal note `research-20261002/prior-art/minmarginal-prior.md`: the
   Kohli-Torr DOI `10.1007/11744023_45` is wrong; Crossref gives
   `10.1007/11744047_3` (the KB package is correct).
6. Internal note `tree-sensitivity-audit.md`: the third author of the SEA
   2022 adaptive-refinement paper is Kuhnke, not Kuhn.
7. Task brief: "Beach, Burlacu, Hager, Hildebrand" conflates two papers:
   Beach-Hildebrand-Huchette 2022 (JOGO) and Beach-Burlacu-Bärmann-Hager-
   Hildebrand 2024 (COAP).
8. Peng et al. 2011: the official ICML title is "Convex Max-Product over
   Compact Sets for Protein Folding".
9. Source ledger, Vavasis 1990: "original full text was unavailable". The
   Cornell TR version is now available and was read (scan, OCR).
10. Del Pia-Khajavirad's `kappa` (Lemma 20) differs from the report's
    `kappa`; add a footnote if both are discussed.

## 9. Search log (2026-10-03)

Web searches (standard and extended modes), with representative phrasings:
- "treewidth quadratic growth global optimization dynamic programming grid
  fixed-parameter box-constrained quadratic";
- "fixed-parameter treewidth condition number / quadratic growth nonconvex
  QP box log(1/epsilon)";
- "tree decomposition quadratic growth mixed-integer quadratic FPT
  curvature growth ratio exact rational";
- "certified lower bound grid dynamic programming tree decomposition
  interpolation error second derivative correction";
- "semiconcave discretization lower bound min-sum continuous graphical
  model MAP guarantee";
- "adaptive discretization dynamic programming quadratic growth
  polylogarithmic accuracy sparse factor graph";
- "approximation scheme polynomial optimization hypercube bounded treewidth
  discretization";
- "branch-and-bound exact MAP continuous MRF Lipschitz";
- "coarse-to-fine dynamic programming optimistic bounds";
- "edge-concave underestimator maximum separation vertex polyhedral";
- "convex max-product continuous MRF interval grid";
- "continuous rotamers iMinDEE provable pruning";
- "cluster problem revisited second-order prefactor";
- "optimistic optimization near-optimality dimension exponential rate";
- "Perevozchikov complexity global extremum";
- "sparse nonconvex QP DP discretization tree decomposition 2026".
They located the Bajaj-Hasan, Raphael, Peng et al., cluster-problem,
Munos and Perevozchikov comparators, which were not in the earlier project
audits, and no result matching the report's main theorem. Crossref was used
for all DOI metadata; arXiv abstract pages for arXiv records.

Access limits: Bajaj-Hasan 2020, Hasan 2018, Wechsung et al. 2014,
Du-Kearfott 1994, Contesse 1980 and Granot-Skorin-Kapov 1990 were not read
in full (paywall or blocked repository); statements above are limited to
their abstracts or publisher summaries. Dawid 1992, Focacci et al. 1999,
Desmet et al. 1992, Ryoo-Sahinidis 1996, Cook et al. 1986 and the textbooks
are cited for standard facts at metadata level only.
