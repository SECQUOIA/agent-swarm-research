# Scout report: duality gaps and primal recovery in decomposition methods

Area: `decomposition-duality-gaps`. Date: 2026-09-28. Status: scouting only.
Nothing here has been independently reviewed. The propositions in Section 3
are first-pass author work, checked by small exact computations. They are not
verified results.

Scratch files are in `research-20260928b/scouting/decomposition-duality-gaps/`:

- `local_sf_checks.py` and its output `local_sf_checks.out`: exact LP and MILP
  computations for the "local Shapley–Folkman" question (Section 3A);
- `scenario_grouping_checks.py` and its output `scenario_grouping_checks.out`:
  exact group-Lagrangian duals for stochastic integer recourse (Section 3B);
- `sources/`: downloaded text of arXiv 1411.1973, 2002.07745, 2010.14446,
  2408.12761, 2411.12085 and 2605.14273;
- `arxiv_query.py`, `arxiv_search.py`, `abs.sh`, `oa.py`: search helpers.

Commands run (targeted only; no project-wide checks, no CI inspection):
`python3 local_sf_checks.py` and `python3 scenario_grouping_checks.py`, both
completing without error. HiGHS (through SciPy 1.18) solved every LP and MILP.

## Summary

- **The suggested "local Shapley–Folkman" question has a negative answer as
  posed.** No gap bound that depends only on degree or treewidth of the
  block–row incidence graph can hold. Paths (degree 2, treewidth 1) already
  give gaps linear in the number of coupling rows `m`. The sharp structural
  parameter in the Udell–Boyd setting is the `rho`-weighted matching number
  of that incidence graph. First-pass work proves it is an upper bound and
  that it is attained for every incidence pattern. The result is correct but
  easy, and its originality is modest.
- **For integer domains with exact feasibility, local bounds fail
  completely.** A parity chain has one fractional block at the dual optimum
  and a gap of `n/2`.
- **Best candidate: scenario-group decomposition for integer recourse under
  continuous uncertainty.** In this regime, scenario-wise Lagrangian duals
  keep a gap of order one, even as the expected recourse function becomes
  convex. Grouping scenarios reduces the gap at a rate set by the discrepancy
  of the scenarios' phases modulo the recourse periodicity lattice. Measured
  rates are about `1/k` for phase-stratified groups, `1/sqrt(k)` for random
  groups, and almost no improvement for the common "bundle similar scenarios"
  rule. A 1-D theory is sketched below; the multi-dimensional theory is open.
- Overall score for the area's best candidate: **4/10**. The local
  Shapley–Folkman line scores 3/10.

## 1. Frontier map

Notation: separable problem `min sum_i f_i(x_i)` subject to `m` linking rows
`sum_i A_i x_i <= b` (or `= b`), with `n` blocks. `rho_i` is a nonconvexity
measure of block `i`. "Dual" means the Lagrangian dual of the linking rows.
For compact blocks it equals the value of the problem in which every block
is convexified.

### 1.1 Classical Shapley–Folkman gap bounds

- **Aubin–Ekeland (1976, MOR 1(3); from memory, not re-read).** Gap at most
  `min(m+1, n) * max_i rho_i`, with nonconvexity measured on the block image
  sets. The linking constraints may be nonlinear, provided they are separable.
- **Bertsekas, Lauer, Sandell and Posbergh (1983, IEEE TAC; from memory).**
  For unit commitment, the relative gap tends to zero as the number of units
  grows with `m = T` demand rows. Bertsekas, *Convex Optimization Theory*
  (2009, §5.7), states separable gap estimates.
- **Udell–Boyd (COAP 2016; local slug
  `udell2016-bounding-duality-gap-for-separable`, fulltext re-read for the
  definitions).** Blocks have compact domains `S_i`, `rho(f)` is finite only
  for convex domains, and `m~` counts all equality rows plus the largest number
  of simultaneously active inequality rows. Some solution of the convexified
  problem satisfies `f(x*) <= p_hat + sum_{i<=min(m~,n)} rho_[i]`. The bound is
  tight. A random linear objective over the optimal face finds such an extreme
  point. The count `m~` is global and ignores which blocks each row touches.
- **Kerdreux–Colin–d'Aspremont (MOR 2023; local
  `kerdreux2023-stable-bounds-on-the-duality`).** They prove stable and
  approximate Shapley–Folkman bounds, and note that only active linking
  constraints matter. For nonconvex domains the conclusions take a
  perturbed-right-hand-side form.
- **Bi–Tang (SIOPT 2020; local `bi2020-duality-gap-estimation-via-a`).** A
  `k`-extreme refinement gives `gap <= sum_i rho_i^{k_i}` with
  `1 <= k_i <= m+1` and `sum_i k_i <= m+n`. It includes a network-flow
  application.
- **Dey–Xu (arXiv 2601.19003; local `dey2026-...`).** They prove
  `OPT(b+E·1) - E <= DUAL(b) <= OPT(b)` with `E` the Hausdorff nonconvexity.
  Under smooth hidden convexity with fixed `m`, `E -> 0` as the number of
  blocks `k -> infinity`. The setting has `B^(i)` with `m` rows, fixed while
  `k` grows (fulltext checked). Integer blocks are excluded.
- **Hübner (arXiv 2503.02464; local).** Probabilistic bounds for partially
  nonconvex problems, for example `Pr(gap = 0) >= C(|C|, m+1)/C(|I|, m+1)`,
  with an electricity-market study.
- **Dubois-Taine–d'Aspremont (MP 2025; arXiv 2406.18282; local).** A
  constructive Frank–Wolfe method with Shapley–Folkman steps:
  `sum_i f_i(x_i) <= v* + 2 D_C/sqrt(K+1) + (m+1) max rho(f_i)` with the stated
  feasibility residual.
- **Dubois-Taine, Pfeiffer, Oudjane, Seguret and Bach (arXiv 2602.06637, Feb
  2026; abstract checked).** A stochastic dual subgradient phase followed by
  block-coordinate Frank–Wolfe. It needs `O(1/eps^2 + N/eps^(2/3))` conjugate
  calls, and recovers Shapley–Folkman gap bounds in the nonconvex case.
- **Bonnans, Liu, Oudjane, Pfeiffer and Wan (SIOPT 2023; arXiv 2204.02366;
  abstract checked).** For aggregative problems with a smooth cost of the
  aggregate, the relaxation gap tends to zero as `N -> infinity`
  *independently of the aggregate dimension*. Soft (smooth) coupling therefore
  escapes the dependence on `m`; hard constraints do not.
- **Others.** Murota–Tamura (DAM 2024; local) prove a discrete
  Shapley–Folkman theorem for integrally convex sets, with `infinity`-norm
  proximity `(1-1/n) min(n,m)`. Askari–d'Aspremont–El Ghaoui (arXiv
  2102.06742) study sparse programs. Diamandis–Angeris (arXiv 2408.12761;
  fulltext grep) treat nonconvex fixed-cost network flows: at most
  (#nodes + 1) edges are nonintegral, which is the global count again.
  Kominers (arXiv 2604.04889) applies Shapley–Folkman to sumsets and is not
  relevant here.

### 1.2 Primal recovery with feasibility guarantees (integer blocks)

- **Vujanic, Mohajerin Esfahani, Goulart, Mariéthoz and Morari (Automatica
  2016; arXiv 1411.1973; fulltext read, lines 213–610).** Theorem 3.1 tightens
  row `k` by `rho_k = m * max_i (max H_ik x_i - min H_ik x_i)`. Under
  uniqueness (Assumption 2.4), every recovered solution at the dual optimum of
  the tightened problem is then feasible. Theorem 3.3 gives, under a Slater
  point with slack `zeta`, `J(x) - J* <= (m + ||rho||_inf / zeta) max gamma_i`.
  **Theorem 3.4 is already a row-local refinement.** It replaces `m` by
  `rank([H_i]_{i in I_k})`, the rank of the columns of blocks touching row
  `k`. Remark 3.5 sums the largest such changes. The *performance* bound still
  carries the global factor `m`.
- **Falsone–Margellos–Prandini (Automatica 2019; arXiv 1706.08788; abstract).**
  Iterative tightening reaches feasibility in finite time with better bounds.
  **Camisa–Notarnicola–Notarstefano (IEEE TAC 2022; arXiv 2010.14446;
  fulltext grep).** Primal decomposition with restriction `b - sigma`, finite-
  time feasibility, and asymptotic and finite-time suboptimality bounds.

### 1.3 Exact integer feasibility: Steinitz proximity

- **Cslovjecsek, Eisenbrand, Hunkenschröder, Rohwedder and Weismantel (SODA
  2021; arXiv 2002.07745; fulltext read, Section 4).** Consider block ILPs with
  `r` linking rows whose blocks are replaced by their integer hulls (a
  Dantzig–Wolfe / Lagrangian-strength relaxation). An optimal vertex has at
  most `r` non-integral blocks (Lemma 5). Some optimal integer solution
  satisfies `||x* - z*||_1 <= (r Delta G)^{O(r)}`, *independent of the number
  of blocks `n`* (Theorem 4; statement (3) gives `(2r Delta G + 1)^(r+4)`).
  Proposition 3: the plain LP relaxation can be `Omega(n)` far.
  Consequently the Lagrangian gap with exact feasibility is at most
  `||c||_inf (r Delta G)^{O(r)}`. This is the integer counterpart of
  Shapley–Folkman, at an exponential price in `r` and for linear objectives
  only.
- **Ligthart (arXiv 2606.30330, June 2026, revised Sept 22 2026; abstract
  checked).** Value functions `b -> min{f(x): Ax = b, x in Z^n_+}` with
  separable convex `f` are convex-extensible on every coset `r + M Z^m`, where
  `M` depends only on `A`. The paper applies this to FPT algorithms for
  two-stage stochastic and `n`-fold IPs. It does not treat approximations or
  duality gaps.

### 1.4 Decomposable zero-gap duals

- **Cifuentes–Dey–Xu (IPCO 2025; arXiv 2411.12085; fulltext grep).**
  Redundant constraints make the Lagrangian dual exact while it stays
  decomposable, including over tree decompositions of sparse MIPs. They give
  multiplicative bounds for packing and covering. Stated open questions: an
  easier subproblem per iteration, and tightness of the bounds in their
  Theorems 9–10.
- **Exact augmented Lagrangian chain.** Boland–Eberhard; Feizollahi–Ahmed–Sun;
  Gu–Ahmed–Dey; Bhardwaj et al.; Lefebvre–Schmidt. These are local slugs
  `gu2020-...`, `bhardwaj2024-...` and `lefebvre2025-...`; the repository's
  2026-09-22 scout records the open penalty-size questions.
- **Zhang–Jiang, "Generalized Dual Decomposition" (arXiv 2605.14273, May
  2026; fulltext grep).** Nonlinear regularizers `g_i` with `sum_i g_i(x) = 0`
  give strong duality for two-stage mixed-integer programs. Piecewise-constant
  regularizers on a finite partition of `X` are `eps`-optimal under complete
  continuous recourse and compactness (Proposition 5). Binary first stage has a
  finite encoding. The paper gives no rate in terms of scenario grouping.

### 1.5 Stochastic integer and MINLP decomposition

- **Carøe–Schultz (ORL 1999; from memory).** Dual decomposition of
  nonanticipativity. The dual equals the problem with each scenario's feasible
  set convexified and a common first stage.
- **Chen–Luedtke (local `chen2022-on-generating-lagrangian-cuts-for`).** The
  bound from all Lagrangian cuts equals the nonanticipative Lagrangian dual
  (Theorem 3). Lagrangian-cut Benders methods therefore inherit every
  scenario-dual gap.
- **Belyak–Oliveira (ITOR 2025; local).** p-branch-and-bound over a finite
  relaxation of nonconvex stochastic MIQCQPs.
- **Scenario grouping.** Sandıkçı, Kong and Schaefer (MP 2013; from memory)
  prove a monotone hierarchy of group-subproblem bounds. Ryan, Ahmed, Dey et
  al., "Optimization-driven scenario grouping" (IJOC 32, 2020; confirmed by
  OpenAlex metadata; content from memory, not re-read), find groupings by
  optimization and heuristics. No discrepancy or lattice theory was found.
- **Romeijnders line** (metadata confirmed via OpenAlex; content from memory
  and the local note).
  - Total-variation bounds on expectations of periodic functions (MP 2016).
  - A convex approximation with a uniform error bound for mixed-integer
    recourse (SIOPT 2016, with Schultz, van der Vlerk and Klein Haneveld).
  - Totally unimodular recourse (SIOPT 2015).
  - Higher-order TV bounds (CMS 2018).
  - Mean-CVaR recourse (MP 2020).
  - Loose Benders (MP 2021) and converging Benders (OR 2023).
  - Random second-stage cost, where error bounds scale with `E||q||_1`
    (arXiv 2206.01605).
  - Risk-averse recourse (COAP 2024) and pragmatic DRO (SIOPT 2024).
  - Kryeziu (arXiv 2608.00245; local
    `kryeziu2026-residual-centering-and-error-bounds`): centered-residual
    certificates.

  All treat convex *approximations* of the expected recourse function for
  MILP recourse. None treats decomposition duals or nonlinear recourse costs.
- **Multistage.** Zou–Ahmed–Sun SDDiP (MP 2019; from memory): Lagrangian cuts
  are tight for binary states. Zhang–Sun (MP 2022; local): SDDP for multistage
  MINLP with generalized conjugacy cuts, matching lower bounds exponential in
  the state dimension, and an exact penalty assumption. Füllner–Rebennack
  NC-NBD (2022) and their SDDP review (2025) (local): open items include
  cheaper nonconvex cuts and regularization.

### 1.6 Unit commitment and convex hull pricing

- Convex hull prices are the Lagrangian dual prices for the balance rows. The
  following sources were checked by abstract only:
  - Andrianesis–Bertsimas–Caramanis–Hogan (arXiv 2012.13331): Dantzig–Wolfe
    computation of convex hull prices.
  - Tanji–Kamri–Glineur–Madani (arXiv 2504.01474): dual first-order methods.
  - Ahunbay–Bichler–Dobos–Knörr (arXiv 2312.07071): approximate
    competitive-equilibrium pricing.
  - Ghosh–Lesage-Landry–Taylor (arXiv 2607.11590): copositive
    characterization of convex hull prices.
  - Hübner 2025: market days at equilibrium.
- No source in this list, and none checked in this run, bounds uplift or the
  gap by network structure beyond active-constraint counts.

### 1.7 Source log

The arXiv id, local slug, or DOI is given in Section 1. The table below
records what was actually checked.

| Source | Checked |
|---|---|
| Udell–Boyd 2016 | local fulltext: setup, `m~`, Theorem 1, tight example |
| Kerdreux et al. 2023; Bi–Tang 2020; Dey–Xu 2026; Hübner 2025; Murota–Tamura 2024; Dubois-Taine–d'Aspremont 2025 | local read notes; Dey–Xu fulltext setup |
| Vujanic et al. 2016 (1411.1973) | fulltext lines 150–620 |
| Camisa et al. (2010.14446); Diamandis–Angeris (2408.12761); Cifuentes–Dey–Xu (2411.12085); Zhang–Jiang (2605.14273) | fulltext grep of the key statements |
| Cslovjecsek et al. (2002.07745) | Section 4 fulltext |
| Ligthart (2606.30330); Dubois-Taine et al. (2602.06637); Bonnans et al. (2204.02366); Falsone et al. (1706.08788); Askari et al. (2102.06742); van Beesten–Romeijnders (2206.01605); convex hull pricing papers | abstracts |
| Romeijnders line; Ryan et al. 2020 | OpenAlex metadata only |
| Aubin–Ekeland; Bertsekas; Carøe–Schultz; Zou–Ahmed–Sun; Sandıkçı et al.; Linderoth–Shapiro–Wright; Mak–Morton–Wood; Hoberg–Rothvoss; Koksma's inequality | from memory, not re-verified |

Searches:

- arXiv API: `all:"Shapley-Folkman"` and `all:"Shapley Folkman"`, full
  lists from 2016 onward reviewed.
- arXiv HTML search: `convex hull pricing`; `integer recourse convex
  approximation`; `scenario grouping stochastic integer`; `stochastic dual
  dynamic integer programming`; `"duality gap" "mixed-integer" Lagrangian`.
- OpenAlex: Romeijnders topics, scenario grouping, unit-commitment gaps, and
  uplift bounds.

The WebSearch budget for the session was exhausted early. The arXiv API,
Semantic Scholar and OpenAlex were intermittently rate-limited, so coverage of
journal-only work (economics uplift literature, Romeijnders-group 2024–2026
papers, QMC in stochastic programming) is incomplete. **An unsuccessful search
does not establish novelty.**

## 2. Open questions

### Q0 (the suggested "local Shapley–Folkman" question): closed at first-pass level

*Can the gap be bounded by a function of the degree or treewidth of the
block–row incidence graph, instead of `m`?* In the natural sense the answer
is no, by Section 3A. Section 3A also identifies the exact worst-case
parameter. What remains is an easy note, not a research problem; see the
assessment in Section 3A.

### Q1 (best candidate): discrepancy law for grouped scenario decomposition with integer recourse

**Setting.** Consider an SAA two-stage program
`min_{x in X} c'x + (1/S) sum_s v(h_s - T x)`. Here `X` is a polytope, or
mixed-integer with an integral hull. The recourse is
`v(t) = min{q'y : W y >= t, y in Z^p_+}` with integer `W`, and the `h_s` are
drawn from a continuous distribution. Partition the scenarios into groups of
size `k`, and let `D_Pi` be the Lagrangian dual of the group nonanticipativity
constraints for partition `Pi`.

**Question.**

1. Prove `P - D_Pi <= C(W,q) * [avg_G Disc_L(phases of G) + beta]`. The
   phases are the `h_s` modulo the recourse periodicity lattice `L`; for
   example, `L = M Z^m` with `M` built from the basis determinants of `W`, as
   in the Gomory, Eisenbrand–Rothvoss and Ligthart periodicity results. The
   term `beta` bounds the mass of scenarios near the boundaries of the LP
   decision cones.
2. Prove a matching lower bound for per-scenario decomposition (`k = 1`) that
   stays bounded away from zero as the density's total variation tends to
   zero.
3. Characterize the achievable rates:
   - phase-stratified groups: `O(1/k)` in dimension 1; `O(k^{-1/m})` or
     `O(log^m k / k)` in higher dimensions;
   - random groups: `Theta(k^{-1/2})`;
   - similarity bundling: no improvement until `k` is comparable to `S`.

**Evidence that it is open.** The Romeijnders line bounds the error of
*convex approximations*. It does not bound decomposition duals, and its
"pseudo-valid" cuts are not valid lower bounds. Chen–Luedtke's Theorem 3 shows
that per-scenario Lagrangian cuts cannot beat the scenario dual. Grouping
papers (Sandıkçı et al.; Ryan et al.) give monotonicity and optimization-based
groupings, not rates. Generalized Dual Decomposition achieves exactness
through functional multipliers, again without grouping rates.

**Closest prior art to check before any novelty claim:**

- SAA lower bounds computed with Latin hypercube or QMC sampling
  (Linderoth–Shapiro–Wright 2006; Homem-de-Mello 2008; Leövey–Römisch 2015).
  Stratified sampling reduces the bias of group-subproblem bounds by a related
  mechanism.
- Crainic et al. on PH scenario grouping.

### Q2: exact-feasibility gaps with `r` linking rows, polynomial or exponential in `r`

For feasible block ILPs with `r` linking rows, is the Dantzig–Wolfe
(Lagrangian) gap at most `poly(r, Delta, G) * ||c||_inf`? The best available
bound via Cslovjecsek et al. is `(r Delta G)^{O(r)} * ||c||_inf`.
Shapley–Folkman achieves `poly(r)` only with right-hand-side perturbation or
Vujanic-type tightening. The MINLP-block version is a further question.

**Evidence.** Cslovjecsek et al. bound `l1` proximity, not the gap. The
bin-packing configuration LP is an instance with identical blocks and
`r = d` item types. There the additive gap is at most `min(d, O(log OPT))`
(Hoberg–Rothvoss; from memory), and the modified integer round-up property
(MIRUP) conjecture says it is at most 1. The dimension-free form of the
question is therefore a famous open problem, and I did not check IP
lower-bound papers for gap (rather than running-time) lower bounds.
Feasibility is low.

### Q3: total-variation bounds for separable-convex (MINLP) integer recourse

Extend the Romeijnders-type uniform error bounds
`sup_x |Q(x) - Q_tilde(x)| <= C * TV(f)` from linear to separable convex
recourse costs, for example quadratic ones. Ligthart's coset-wise convexity is
the natural tool: average the coset convex extensions under a uniform phase,
and control the remainder by a weighted total variation. The weight grows with
the discrete slope of `V`, so polynomial-growth costs need moment weights.

**Evidence.** Van Beesten–Romeijnders 2022 handle random *linear* costs.
Ligthart applies periodic convexity only to FPT algorithms. No nonlinear
recourse result was found, but journal-only work was under-searched.
Feasibility is moderate; significance is moderate to low.

## 3. First-pass mathematics

### 3A. The "local Shapley–Folkman" question (suggested candidate)

Setting of Udell–Boyd: `f_i : S_i -> R` is lsc on a compact *convex* `S_i`,
`f_hat_i` is its convex envelope, and `rho_i = sup (f_i - f_hat_i)`. There are
linear rows `A x <= b` and `G x = h`. Let `Gamma` be the bipartite incidence
graph with block `i` adjacent to row `j` whenever block `i` has a nonzero
coefficient in row `j`. Let `nu_rho(Gamma)` be the largest total `rho` over
the blocks of a matching in `Gamma`. This is computable by the assignment
problem, or by LP by Egerváry's theorem.

**Proposition L1 (weighted-matching Shapley–Folkman bound).** Let `x*` be an
extreme point of the optimal set of the lifted convexified problem
`min sum t_i` with `(x_i,t_i)` in `epi f_hat_i`, and let `J` be its active
rows. Then

```
p* - d*  <=  f(x*) - p_hat  <=  sum_{i in K} rho_i  <=  nu_rho(Gamma_J)  <=  sum_{i<=min(m~,n)} rho_[i],
```

where `K` is the set of blocks with `(x_i*, t_i*)` not extreme in
`epi f_hat_i`, and `Gamma_J` is `Gamma` restricted to the active rows.

*Proof sketch.*

1. At an optimum, `t_i* = f_hat_i(x_i*)`. Blocks outside `K` sit at extreme
   points of `epi f_hat_i`, where `f_i = f_hat_i`.
2. Each `i` in `K` has a direction `(d_i, s_i)` with `d_i != 0` that keeps
   `(x_i*, t_i*) ± (d_i, s_i)` in `epi f_hat_i`.
3. Suppose `sum_{i in K} lambda_i A_J d_i = 0` with `lambda != 0`. Moving
   along `eps * lambda_i (d_i, s_i)` keeps the active rows fixed and the
   inactive rows feasible for small `eps`. Either one sign improves the
   objective, contradicting optimality, or both signs stay optimal,
   contradicting extremality. Hence the vectors `A_J d_i` are linearly
   independent.
4. Each vector `A_J d_i` is supported on the rows of block `i`. Choose `|K|`
   rows giving a nonsingular square submatrix. A nonzero term of its Leibniz
   expansion is a matching of `K` into rows along nonzero entries.

The last inequality holds because any matching has at most `m~` edges.
Strong duality `d* = p_hat` holds for the convexified problem (Udell–Boyd,
Appendix A). ∎

Two refinements follow from the same proof:

- **Rank (Rado-matroid) refinement.** Every subset `K'` of `K` satisfies
  `|K'| <= rank(A_J` restricted to the columns of `K')`.
- **Flexibility (contraction) refinement.** Polyhedral convex blocks (with
  `rho = 0`) that are not extreme at `x*`, such as strictly uncongested lines,
  also belong to `K`. They consume independence. In a transport network with
  node-injection generators, the uncongested lines at `x*` form a forest, and
  the number of fractional generators is at most the number of connected
  components of the graph of uncongested lines. This bound is a posteriori.

**Proposition L2 (the bound is attained for every incidence pattern).** Take
any `Gamma` and any `rho >= 0`, and a maximum-weight matching `mu` with
matched blocks `B`. Build the following instance:

- matched blocks: `S_i = [0,1]` with the tent cost
  `f_i = rho_i (1 - |2x - 1|)`, so `f_hat_i = 0`;
- unmatched blocks: `S_i = {0}`;
- matched rows: equalities with coefficient 1 on the matched edge and
  `eps` on the other incidences, right-hand side chosen so that `x_B = 1/2`;
- unmatched rows: slack inequalities.

For small `eps`, the square system is nonsingular, so the feasible set is the
single point `x_B = 1/2`. The gap is then `sum_{i in B} rho_i = nu_rho(Gamma)`.
Hence

```
sup over instances with incidence Gamma and nonconvexities rho of (p* - d*)  =  nu_rho(Gamma).
```

**Corollary L3 (no degree or treewidth bound).** Suppose every row touches at
least one block and every block lies in at most `Delta_B` rows. Then
`nu(Gamma) >= m / Delta_B`, since every vertex cover has at least that size
(Kőnig). Hence the worst-case gap is at least `(m / Delta_B) rho` even at
degree 2 and treewidth 1. For the path incidence, `nu = m`.

**Proposition L4 (parity chain: exact feasibility with integer domains is not
local).** Take binary blocks `x_1..x_n` (`n` even) and `y`, rows
`x_i + x_{i+1} = 1` and `x_n + 2y = 1`, and cost `-1` on odd `x_i`.

- The dual equals the LP value `-n/2`, with the single fractional block
  `y = 1/2`.
- The integer optimum is `0`, so the gap is `n/2`.
- Relaxing only the `y` row to `[0,2]` restores the value `-n/2`.

So the perturbation-form bounds (Kerdreux, Dey–Xu) remain `O(1)` here. Their
translation into exact-feasibility gaps must pay the sensitivity of the value
function to the right-hand side, which is global. The same structure defeats
any clustering of the path into subpaths, because all clusters share the
mixing weight through the cross rows.

**Computations** (`local_sf_checks.out`):

| Check | Result |
|---|---|
| A: path, binary blocks, rows `2x_i + 2x_{i+1} >= 1` | Direct `max_lambda L(lambda)` gives `m/4`, integer optimum `m/2`; gap `= m/4` for `m = 4..64` |
| B: path, `[0,1]` domains, `f = min(8x, 1)` | Gap `= m/4`; `m/2` fractional blocks |
| C: parity chain | Gap `= n/2` for `n = 4..64`, with exactly 1 fractional block; the perturbed optimum equals the dual |
| D: 200 random degree-2 incidences, heterogeneous `rho` | 0 violations of `gap <= sum_K rho <= nu_rho(Gamma_J)`; mean values: gap 1.44, `sum_K rho` 7.51, `nu` 9.81, Udell–Boyd active bound 15.52 |
| D: tightness construction, 20 random degree-3 incidences | Gap `= nu_rho(Gamma)` to `4e-15` |
| E: grid transport networks, 9–36 nodes, 4 capacity levels | #fractional generators `<=` #components of uncongested lines in all 16 cases (equality in every case). Uncongested: 1 fractional generator, gap `<= F`. Heavy congestion: gap grows with node count |

**Assessment.**

- Q0 is answered. The worst-case gap is governed by the weighted matching
  number of the incidence graph, which is `Theta(m)` at bounded degree.
- Positive effects of sparse structure come only from:
  - small matching or rank structure;
  - flexibility of polyhedral convex parts, which reduces to an
    active-constraint count in a projected (PTDF-like) formulation;
  - smooth soft coupling (Bonnans et al.).
- The results are correct but elementary. Vujanic et al.'s Theorem 3.4 is
  already row-local on the feasibility side. Matching arguments for basic
  solutions are standard in LP rounding.
- No source checked states L1–L2 for gap bounds, but the originality is
  modest. Significance for solvers is limited to a posteriori certificates
  and to identifying where to repair.
- **Score 3/10.**

### 3B. Best candidate: grouped scenario decomposition (Q1)

**1-D model.** First stage `x in [0, L]` (continuous). Integer recourse gives
`F_s(x) = c x + V(ceil(h_s - x))`. Suppose `V(t) = a t + b + pi(t)` for
`t >= t0`, with `pi` periodic of period `M`, and all `h_s - L >= t0`. Define

```
Psi(u) = a (ceil(u) - u) + pi(ceil(u)).
```

`Psi` is `M`-periodic and `F_s(x) = (c - a) x + a h_s + b + Psi(h_s - x)`.
For a group `G` of size `k`, `F_G` is the average of `F_s` over `G`. Let
`theta_s = h_s mod M`, and let `D_M(theta_G)` be the extreme (arc)
discrepancy on the circle `R/MZ`. `Var_M(Psi)` is the variation of `Psi` over
one period, and `mu_Psi` its mean.

**Proposition S1 (upper bound).**

```
P - D_Pi  <=  2 Var_M(Psi) * sum_G p_G D_M(theta_G).
```

*Proof sketch.*

1. `F_G(x) = A_G(x) + R_G(x)`, where
   `A_G(x) = (c - a) x + a h_bar_G + b + mu_Psi` is affine and
   `R_G(x) = mean_{s in G} Psi(theta_s - x) - mu_Psi`.
2. Koksma's inequality on the circle is uniform in the shift `x`, because the
   discrepancy is translation invariant. It gives
   `delta_G = sup_x |R_G(x)| <= Var_M(Psi) D_M(theta_G)`.
3. Hence the envelope satisfies `conv F_G >= A_G - delta_G`, while
   `F_G <= A_G + delta_G`.
4. By Carøe–Schultz, `D_Pi = min_x sum_G p_G conv F_G(x)`. Therefore
   `D_Pi >= min_x A(x) - delta_bar` and `P <= min_x A(x) + delta_bar`, where
   `A = sum_G p_G A_G` and `delta_bar = sum_G p_G delta_G`. ∎

Only the periodic part must be equidistributed within each group. The convex
part, here `A_G`, may be arbitrary and may differ across groups, because the
argument uses only convexity of `A_G`.

**Proposition S2 (per-scenario obstruction).** Let `L >= 2M` and `c = a`, so
the convex part is flat. For `k = 1`, every `x` in `[M, L - M]` lies between
two minimizers of `Psi(h_s - ·)` at most a period apart. So
`conv F_s(x) <= a h_s + b + min Psi` there. The population objective is within
`||Phi||_inf TV(f)` of the constant `a E h + b + mu_Psi`, where `Phi` is a
periodic primitive of `Psi - mu_Psi`. Hence

```
gap(k = 1)  >=  mu_Psi - min Psi - ||Phi||_inf TV(f),
```

which tends to `mu_Psi - min Psi` as the distribution is smoothed. For simple
integer recourse, `mu_Psi - min Psi = 1/2`, although the expected objective
becomes flat, and hence convex. In the setting of Chen–Luedtke's Theorem 3
(all per-scenario Lagrangian cuts give exactly the nonanticipative dual),
Benders with all per-scenario Lagrangian cuts stalls at the same value. I have
not checked whether their setting admits a continuous first stage; the
identity is standard Lagrangian-cut theory, but this should be confirmed.

**Computations** (`scenario_grouping_checks.out`; `S = 2048` SAA scenarios;
exact envelopes via lower hulls).

Simple recourse `F = x + ceil(h - x)`, `h ~ N(10, 9)`, `X = [0, 2]`. The SAA
objective ranges only over `[10.407, 10.434]` for `x` in `X`. Predicted `k=1`
gap: `1/2`.

| k | 1 | 4 | 16 | 64 | 128 |
|---|---|---|---|---|---|
| similar-h bundles | .485 | .472 | .427 | .293 | .162 |
| random | .485 | .264 | .133 | .060 | .041 |
| phase-stratified (mod 1) | .485 | .117 | .028 | .0063 | .0027 |

Two-variable recourse `V = min{3y1 + 5y2 : 2y1 + 3y2 >= t}`, with `c = 1.5`
(the LP slope) and period 2. Predicted `k=1` gap:
`mu_Psi - min Psi = 1.0`.

| k | 1 | 4 | 16 | 64 | 128 |
|---|---|---|---|---|---|
| random | .974 | .497 | .259 | .113 | .078 |
| stratified mod 1 (wrong period) | .974 | .350 | .138 | .048 | .028 |
| stratified mod 2 (correct period) | .974 | .348 | .073 | .015 | .008 |

Observed rates: roughly `c/k` for correct stratification (`c` between 0.4
and 1.2 in the two examples), roughly `c/sqrt(k)` for random groups (`c`
between 0.5 and 1.0), and slow decay for similarity bundling. The
period of the recourse lattice matters: stratifying modulo 1 when the true
period is 2 is visibly slower.

**Attack plan.**

1. **1-D theorem with exact constants.** Cover the SAA and population versions
   and the lower bound S2. Include integer first stage: when `T` has
   non-integer entries, the phases still shift with `x`. When `T` is integer
   and `x` is integer, the phases do not move, and the obstruction disappears.
2. **Separable recourse in `m` dimensions.** Take
   `v(t) = sum_j V_j(ceil(t_j))`. The periodic part is a sum of 1-D periodic
   functions, so Koksma–Hlawka with Hardy–Krause variation applies. This
   gives `O(k^{-1/m})` with lattice stratification, or
   `O(log^{m-1} k / k)` with digital-net-like phase assignment of given
   scenarios.
3. **General integer `W`.** Use the asymptotic periodicity of the MILP value
   function (Romeijnders et al., SIOPT 2016; recalled, to be re-read):
   `v = LP part + psi_B` in shifted decision cones, with lattice
   `L_B = W_B Z^m`. Group within each cone class. Bound the non-periodic
   remainder by the scenario mass within `diam(TX) + R` of cone boundaries.
   *Main technical risk:* the discontinuity sets of `psi_B` are not
   axis-parallel in general, so Hardy–Krause variation may be infinite. The
   fallback is isotropic discrepancy, with rate `O(k^{-1/m})`.
4. **Separable-convex recourse (links to Q3).** Replace additive periodicity
   by Ligthart's coset-wise convexity. The error term then carries the local
   discrete slope of `V`, so it needs moment weights.
5. **Grouping algorithms.** Sort by phase in 1-D; use a space-filling-curve
   order modulo `L` in `m` dimensions. Compare with Ryan et al. grouping and
   random bundles inside a PH or dual-decomposition code (mpi-sppy
   "bundles", or DSP). Use SSLP/SIZES-like instances with continuous
   right-hand sides and a continuous first stage.
6. **Lower bounds.** Show `Theta(k^{-1/2})` for random groups by the
   Kolmogorov–Smirnov scale, and that similarity bundling does not improve
   until `k` is comparable to `S`.

**Difficulty and risk.**

- Steps 1–2: days to two weeks, low mathematical risk.
- Step 3: one to three months, medium risk from boundary regions and the
  variation issue.
- Step 4: open-ended.
- Prior-art risk is real. Stratified or QMC sampling in SAA lower bounds
  exploits a related mechanism, and PH practitioners know empirically that
  grouping dissimilar scenarios helps.
- Applicability risk: the phenomenon needs integer recourse,
  continuous-valued right-hand-side uncertainty with enough spread, and
  first-stage decisions that move the right-hand side continuously. Random
  `T` or `q` gives each scenario a different lattice.

## 4. Significance

**Consequences that would be proved (if Q1 is completed).**

- Explicit bounds on the Lagrangian bound quality of scenario-group
  decomposition, as a function of group size and grouping rule.
- A proof that per-scenario duals, and Lagrangian-cut Benders, keep an
  order-one gap in a regime where the true objective is nearly convex.
- A rule for grouping that is optimal up to constants in 1-D.

**Plausible solver benefits.**

- Better scenario bundling in PH and dual-decomposition bounders, such as
  mpi-sppy Lagrangian spokes and DSP. A group size of about 10 with
  stratification matches about 100 with random grouping in the computations
  above.
- A principled choice of `k` for a target gap.
- Complementarity with spatial branching on the first stage. Branching
  shrinks the envelope interval; grouping flattens the periodic part.

**Speculative.**

- Multistage extensions (SDDiP-like cuts with continuous states).
- MINLP recourse through periodic convexity.
- Use as a preprocessing step in general stochastic MINLP solvers.

**Still needed for practical value.**

- Evidence that the regime is common in benchmark and application instances.
- Computable periodicity lattices, since `M` can be large.
- Coping with the multi-dimensional discrepancy curse.
- The cost of subproblems that grow with `k`.
- Validation against optimization-driven grouping.

For Q0 (local Shapley–Folkman), the proved consequences are the worst-case
characterization `sup gap = nu_rho(Gamma)`, the degree/treewidth
impossibility, and the parity-chain obstruction. These clarify when sparse
coupling can help. They do not enable a new solver capability beyond cheap a
posteriori certificates, since fractional blocks are identified anyway.

## 5. Recommendation

- The literature on Lagrangian and Shapley–Folkman gaps for separable
  problems is mature: Aubin–Ekeland, Udell–Boyd, Kerdreux et al., Bi–Tang,
  constructive Frank–Wolfe recovery, Dey–Xu's smooth asymptotics, and
  Vujanic-type tightening, which already includes a row-local rank
  refinement.
- The suggested "local Shapley–Folkman" direction closes quickly. No
  degree- or treewidth-based bound exists (paths give `Theta(m)` gaps). The
  sharp worst-case parameter is the `rho`-weighted matching number of the
  block–row incidence graph (Propositions L1–L2). Exact integer feasibility
  is not local at all (parity chain).
- The most promising residual direction is Q1: discrepancy-controlled gaps
  for grouped scenario decomposition of stochastic programs with integer
  recourse under continuous uncertainty.
  - It has a clean 1-D theory with a per-scenario `Theta(1)` obstruction and
    measured `1/k`-versus-`1/sqrt(k)` separations.
  - Its originality is moderate, with prior-art risk from QMC/LHS-based SAA
    bounds and scenario-grouping heuristics.
  - The regime is real but narrow, and the general-`W` extension carries
    technical risk.
- Q2 (exact-feasibility gap polynomial in `r`) is significant but touches the
  MIRUP-type frontier and is unlikely to yield soon.
- Q3 (total-variation bounds for separable-convex recourse via Ligthart's
  2026 periodic convexity) is a reasonable, likely-new but narrow follow-up.
- **Score for the area's best candidate (Q1): 4/10.** Local Shapley–Folkman:
  3/10. Q2: 3/10. Q3: 4/10.
- Pursue Q1 only if a quick prior-art check on stratified/QMC group bounds
  (Linderoth–Shapiro–Wright; Homem-de-Mello; Ryan et al. 2020; Crainic et al.)
  comes back clean.
