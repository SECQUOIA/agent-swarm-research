# Scouting brainstorm: theory directions with solver impact (2026-09-22)

Author: research scout agent. The repository was read but not modified. Its README
and `results/` were skimmed only to avoid duplicates (row hulls of separable concave
terms, univariate links, composite univariate envelopes, vertex binarization, pooling,
potential flow, cluster-free B&B, CIA, precision and complexity results). The
directions below were chosen by expected impact on solvers, not by the repository's
history.

"Known" statements cite papers I am confident about unless marked *(unverified)*. A
failed literature search does not establish novelty.

## 0. Common thread and the numerical sanity checks run for this note

The strongest ideas below share one tool: **convex order and comonotone couplings**.
For `f(x) = sigma(a^T x + b)` on a box `B = [l,u]`, take a relaxation point `xbar`.
The convex envelope value is `inf E sigma(a^T X + b)` over random `X` in `B` with
`E X = xbar`. Everything depends only on the law `nu` of `T = a^T X + b`.

**Key lemma (proof sketch, checked numerically).** Flip coordinates so that `a > 0`
and set `p_i = (xbar_i - l_i)/(u_i - l_i)`. Let `mu*(xbar)` be the law of `a^T V + b`,
where `V` is the random staircase vertex: sort the `p_i` in decreasing order, draw one
uniform `U`, and set `V_i = u_i` if `U < p_i` and `V_i = l_i` otherwise. `mu*` has
`n+1` atoms. Then the laws of `T` that can be achieved are exactly
`{nu : nu <=_cx mu*(xbar)}`.

- Necessity: each `a_i X_i` is `<=_cx` its two-point endpoint law with the same mean.
  Among couplings, the comonotone sum is maximal in convex order, and comonotone sums
  preserve convex order (Dhaene et al., Insurance Math. Econ. 2002).
- Sufficiency: Strassen (1965) gives a martingale coupling `E[S|T] = T` with
  `S ~ mu*`. Then `X' = E[V|T]` lies in `B`, has mean `xbar`, and satisfies
  `a^T X' + b = T`.

Consequences:
1. `conv env_B f (xbar) = inf { E_nu sigma : nu <=_cx mu*(xbar) }`, and the concave
   envelope is the corresponding `sup`. This holds for **any** continuous `sigma`, not
   only convex or S-shaped ones.
2. The optimal representation uses only points of the staircase (Kuhn) simplex that
   contains `xbar`. The Kuhn triangulation therefore "generates" the envelope of
   every ridge function.
3. The remaining problem is one-dimensional with `n+1` atoms. In stop-loss form it is
   `min ∫ sigma''(tau) U_nu(tau) dtau` over convex `U_nu` squeezed between `(m-tau)^+`
   and `U_mu*`. Its optimum fuses runs of consecutive atoms inside the convex pieces
   of `sigma`.

**Checks run** (scripts in `/tmp/ridge_check.py`, `/tmp/r1check.py`,
`/tmp/budget_check*.py`, `/tmp/simp_check.py`):
- Ridge envelope, n=3, 12 random instances (sigmoid, SiLU, sin, -sigmoid). The
  convex-order formula matched a 25^3-point box-grid LP to within 3e-5, the grid
  error. It was much tighter than the univariate envelope on the auxiliary
  `t = a^T x`, for example -0.638 against -0.894 for `sin` (f = 0.954).
- Rank-one concave envelope `(b^T x)^2` on a box, n=5, mixed-sign `b`. The
  sign-flipped staircase value equals the vertex-LP envelope exactly. It is much
  smaller than the univariate secant used by eigenvector-secant cuts, for example
  5.21 against 12.31.
- Products of simplices (one-hot inputs), 100 instances: the comonotone quantile sum
  is convex-order maximal in all of them, so the theory extends.
- Box ∩ {sum x = k} (uniform-matroid base polytope), 100 instances: **no maximal law
  exists in 23**. The reduction does **not** extend to budget or mixture polytopes.
  Candidate 4 addresses this.

---

## 1. Ridge-function hulls for arbitrary univariate `sigma`, by convex order

**Target theorems.**
- (A) For any continuous `sigma` and box `B`,
  `conv{(x, sigma(a^T x+b)) : x in B}` is described pointwise by the formula above.
  If `sigma` has `k` inflection points, the envelope and a supergradient can be
  evaluated in `O(n log n + n k)` univariate operations. This yields an exact
  separator: the supergradient gives a globally valid linear cut.
- (B) Slabs: for `P = B ∩ {alpha <= a^T x + b <= beta}`, the achievable laws are
  `{nu <=_cx mu* : supp nu ⊆ [alpha,beta]}`. Hence the projected ideal formulation of
  any disjunction over slabs has an exact 1-D separator. Examples: a piecewise-linear
  approximation of `sigma` with binaries, hard-tanh or clipped activations,
  flow-direction binaries, and ReLU as a special case (Anderson et al.). The mixture
  law is `sum_j z_j nu_j <=_cx mu*` with `supp nu_j ⊆ slab_j`.
- (C) The same holds on products of simplices (one-hot categorical inputs) and on
  mixed box × simplex domains.
- (D) Characterization of when the univariate envelope on the auxiliary variable is
  already exact, with a quantitative gap bound depending on the box geometry. This
  tells solvers when to separate.

**Why it matters.** Embedded neural-network surrogates with sigmoid, tanh, SiLU, GELU
or softplus activations (OMLT, gurobi-ml, PySCIPOpt-ML, MeLOn/MAiNGO). Also logistic
and probit constraints, `exp/log/power(a^T x)` terms in MINLPLib, angle-difference
`sin/cos` terms, and Weymouth or Hazen–Williams equations written in terms of potential
differences. The components affected are a nonlinear-handler separator (SCIP), a
cut callback (Gurobi), and bound propagation along ridges. For ReLU, Anderson et al.
reported large gains from per-neuron ideal cuts. Comparable root-gap gains are
plausible for smooth activations but have not been measured.

**Known.**
- Anderson, Huchette, Ma, Tjandraatmadja, Vielma, Math. Program. 183 (2020): ideal
  formulations for convex piecewise-linear activations over polytopes.
- Tjandraatmadja et al., NeurIPS 2020: optimal single-neuron ReLU relaxations.
- Tawarmalani, Richard, Xiong, Math. Program. 138 (2013): concave envelope of convex
  `g(a^T x)` on a box (staircase / Lovász).
- Wilhelm, Wang, Stuber, JOGO 85 (2023): univariate envelopes of activations only.
- **Carrasco & Muñoz, arXiv 2410.23362, Math. Program. 2026 (closest).** Box
  domains, `sigma` convex or S-shaped (one inflection point, the "STFE" property). A
  recursive formula built from perspectives of lower-dimensional envelopes. They say a
  clean closed form is difficult. There are no slabs or binary indicators, no simplex
  inputs, and no functions with two or more inflection points. SiLU and GELU have two
  inflection points, near ±2.4 for SiLU; the paper's appendix handles SiLU by
  reflection, which appears valid only on restricted ranges *(my reading; verify)*.
- DRO and actuarial work on comonotone extremal distributions may contain the key
  lemma for convex `g` (the supermodular case). For non-convex `g`, I did not find it
  *(search incomplete)*.

**Main difficulty.**
- A clean algorithm for the 1-D fusion problem with several inflection points,
  including partially split atoms.
- Supergradients at ties in the sort order.
- Numerically safe cuts.
- A projected (not extended) description for (B).
- Deciding whether a compact extended formulation exists for smooth `sigma`.

**Validation.**
- A SCIP 10 nonlinear handler through PySCIPOpt that detects `sigma(sum a_i x_i + b)`.
  Compare against default SCIP (auxiliary-variable univariate envelopes) and against
  a reimplementation of Carrasco–Muñoz on S-shaped cases.
- Gurobi 13: add cuts through `cbCut` on models with general-constraint
  `y = sigma(t)`, `t = a^T x + b`. BARON as an external baseline.
- Instances:
  - small MNIST/verification networks with tanh, sigmoid, SiLU or GELU activations
    (1–4 layers, 20–200 neurons);
  - MeLOn and Schweidtmann–Mitsos surrogate benchmarks;
  - PySCIPOpt-ML benchmark models;
  - MINLPLib instances containing `exp/log/pow/sin/cos` of multi-variable sums (a
    structural scan first).
- Metrics: root gap closed, time and nodes to optimality, and the number of instances
  solved within 1 h.

**Risk.** Correctness low (lemma proved in sketch and checked). Novelty
medium: the core S-shaped box case is now published; the contribution is generality
(any `sigma`), a non-recursive formula, slabs and ideal MIP formulations, and simplex
inputs. Impact medium-high for ML-embedded MINLP and unknown for MINLPLib.

## 2. Box-aware rank-one ("staircase") cuts for nonconvex QCQP, and a comonotone αBB

**Target theorems.**
- (A) For any `b`, `b^T X b <= Lambda_b(x)` is valid for `conv{(x, xx^T) : x in B}`.
  Here `Lambda_b` is the concave envelope of `(b^T x)^2` on `B`: a sign-flipped
  staircase function, piecewise linear with `n!` pieces and `O(n log n)` evaluation.
  It strictly dominates the univariate eigenvector-secant cut
  `b^T X b <= (L+U) b^T x - LU`. For integral `b` on `{0,1}^n` it contains the BQP
  clique-type inequalities.
- (B) Identity: `Lambda_b(x) = b^T M_s(x) b`. `M_s(x)` is the second-moment matrix of
  the comonotone/antitone staircase vertex for sign pattern `s = sign(b)`, with
  entries built from `min(p_i,p_j)` (same signs) or `max(0, p_i + p_j - 1)`
  (opposite signs) in normalized coordinates. Hence, for a fixed sign pattern `s`,
  the whole family says that `b^T (M_s(x) - X) b >= 0` for every `b` in the orthant
  of `s`. This is a copositivity-type condition. `M_s(x)` is piecewise linear in `x`;
  the constraint set is convex because each `Lambda_b` is concave. Separation is a
  sign-constrained eigenvalue problem. It is NP-hard in general, but a plain
  eigenvector test is exact whenever the top eigenvector of `X - M_s(x)` has sign
  pattern `s`. Alternating between the sign pattern and the eigenvector is a natural
  heuristic. Together with Shor's `X ⪰ xx^T`, this gives a "sandwich" relaxation.
- (C) Underestimator: for any decomposition `N = sum_k b_k b_k^T` with `Q+N ⪰ 0`,
  `x^T (Q+N) x − sum_k Lambda_{b_k}(x)` is a convex underestimator on the box. It is
  exact at vertices. With diagonal `N` it is exactly αBB, since
  `Lambda_{e_i}` is the secant of `x_i^2`. If all `b_k` share one sign pattern, it
  equals `x^T Q x − <N, D K(p(x)) D>`, where `K(p)_{ij} = min(p_i,p_j) − p_i p_j`
  (the Brownian-bridge covariance) and `D` is the diagonal matrix of box widths.
  With mixed sign patterns the value depends on the decomposition, not only on `N`.
  Target: an algorithm for the best decomposition (for a fixed sign structure the
  problem is concave in `N`), dominance over diagonal αBB and the spectral relaxations
  of Nohra–Raghunathan–Sahinidis, and a comparison with the Shor+RLT bound.

**Why it matters.** Nonconvex (MI)QCQP is Gurobi's core nonlinear class and a large
part of QPLIB and MINLPLib (BoxQP, pooling, QAP-like and QCQP instances). The cuts
are linear in `(x, X)` and cheap to separate, so an LP-based solver can use them. The
components affected are a cut separator (Gurobi and SCIP) and a convex
underestimator (BARON). The enveloped quantity in the numerical check shrank by a
factor of 1.3–2.4 relative to the secant; the effect on overall bounds is not measured.

**Known.**
- Saxena, Bonami, Lee, Math. Program. 2010/2011: eigenvector disjunctive and
  projected relaxations.
- Qualizza, Belotti, Margot (2012): linear relaxations of QCQP with eigenvector cuts
  on the PSD side.
- Burer & Letchford, SIOPT 2009: BoxQP and BQP projections. Padberg 1989: BQP.
- αBB (Androulakis, Maranas, Floudas 1995); nondiagonal αBB (Skjäl, Westerlund,
  Misener, Floudas, JOTA 2012).
- Nohra, Raghunathan, Sahinidis (SIOPT 2021; Math. Program. 2022).
- Anstreicher & Burer (2010): exact 2-D hulls. Dey, Kazachkov, Lodi, Muñoz: sparse
  PSD cuts.
- Muñoz–Serrano and Chmiela–Muñoz–Serrano: intersection cuts.
- Xu & Pokutta, arXiv 2608.03318 (Aug 2026): joint-range inequalities, which are
  different.
- The per-term envelope is classical (TRX 2013). The cut family in lifted space, the
  moment-matrix form, the separation method and the comonotone αBB appear new in my
  searches, but this is **not certain**.

**Main difficulty.** Separation over the choice of `b` (copositivity for a sign
pattern), managing the number of cuts, and proving dominance relative to Shor+RLT.

**Validation.** Implement in PySCIPOpt as a separator on BoxQP (Vandenbussche–
Nemhauser and Burer instances), QPLIB nonconvex QPs/QCQPs and MINLPLib QCQPs. Try
Gurobi 13 through user cuts on explicit product variables. Compare root bounds with
default, with added eigen-secant cuts, and with Shor+RLT (Mosek), then compare solve
times.

**Risk.** Correctness low, novelty medium, impact potentially high.

## 3. Network edge hulls with node-potential boxes and flow-direction binaries

**Target.** Apply candidate 1(B) to `q_e = psi(pi_i − pi_j)`. Here `psi` is inverse-S:
`sgn(d)·sqrt(|d|/c)` for Weymouth with squared pressures, and the analogous inverse
for Hazen–Williams exponent 1.852. The same applies to `sin/cos(theta_i − theta_j)` in
AC power flow. Pressure boxes on the two end nodes, flow bounds (a slab in `d`) and a
direction binary give a closed-form hull with three atoms. Extensions:
- chains of pipes and compressors (sums along paths);
- a proof that the hull strictly improves on the univariate relaxation of the
  auxiliary difference exactly when the relaxation point is away from the extreme
  vertices;
- a bound on the gain.

**Why it matters.** Gas nomination and design (GasLib), water design and operation
(`waterno2`, where listed dual bounds are known to be weak and the repository already
has tooling), and power networks (PGLib-OPF, QC relaxations). The components affected
are separation and propagation.

**Known.**
- Borraz-Sánchez et al. (2016): SOC relaxations for gas.
- Humpola & Fügenschuh: convex network design reformulations.
- Hijazi, Coffrin, Van Hentenryck (QC, 2017).
- Kocuk, Dey, Sun (ACOPF cycle cuts, 2016).
- I found no box-aware edge hull *(search incomplete)*.

**Main difficulty.** Theory is mostly a corollary of candidate 1. Gains may be small
when node boxes are symmetric: the middle staircase atom sits at `d = 0` on the
secant.

**Validation.** Water: SCIP and Gurobi on `waterno2_*`. Gas: GasLib-11/24/40/134 with
Weymouth. Power: angle-difference constraints on PGLib-OPF. Compare root and 30-minute
dual bounds.

**Risk.** Correctness low, novelty low-medium, impact uncertain (cheap to find out).

## 4. Ridge hulls on budget and mixture polytopes (box ∩ {1^T x = c})

**Target.**
- (A) Characterize the polytopes and directions for which convex-order maximal laws
  exist (conjecture: essentially products of simplices, up to affine maps and
  direction-specific exceptions).
- (B) For the budget case, exact separation via column generation. Linear
  optimization over the graph is a parametric 2-D LP (fractional knapsack with one
  equality) followed by a univariate minimization, so it is polynomial.
- (C) A tight polynomial relaxation using the best of `O(n)` "chain" laws, with an
  approximation guarantee.

**Why it matters.** Mixture and blend surrogates (compositions summing to 1),
prospect-theory portfolio objectives `sum_s p_s u(r_s^T x)` with S-shaped `u` and
`sum x = 1`, and normalized neural-network inputs.

**Known.** Madow's systematic sampling and polymatroid Lovász theory are related.
Sorted systematic sampling is **not** maximal: numerically, stop-loss deficits reached
0.75, and 23% of instances have no maximal law.

**Difficulty.** Real, because the easy structure fails.

**Validation.** Same pipeline as candidate 1, plus portfolio instances with S-shaped
utility.

**Risk.** Medium-high.

## 5. Binary-input ridge sets `conv{(x, sigma(a^T x)) : x ∈ {0,1}^n}`

**Target.** A complexity dichotomy:
- For concave `sigma`, the lower side is a polymatroid (known; Atamtürk & Narayanan,
  ORL 2008).
- For S-shaped `sigma`, separation is weakly NP-hard (reduction from subset sum,
  expected), with a pseudo-polynomial DP.
- Polynomial for equal or few distinct weights.
- A lifting of the box hull (candidate 1) by integrality.

**Why it matters.** Binary-feature neural networks, chance constraints with binary
selections, and "probability of success" objectives.

**Risk.** Medium. Impact medium-low: the box hull plus branching may be enough.

## 6. Coordinate-plus-ridge composites `h(u, a^T x)` with `u` an independent variable

**Target.** Achievable joint laws are joint contractions of couplings of a two-point
law and the staircase law (conditional-independence gluing). This gives an exact
finite-dimensional envelope computation for `u·sigma(a^T x)`, `u·exp(a^T x)` and share
functions. For `h` supermodular, target a closed form via comonotone or antitone
couplings.

**Why it matters.** Flows times nonlinear properties in process models, gated units,
and rate expressions.

**Known.** He & Tawarmalani composite relaxations (Math. Program. 2021); He, Liu,
Tawarmalani on fractional programs (Math. Program. 213, 2025, via homogenization); the
`x·f(y)` disjunctive hulls are folklore.

**Risk.** Medium-high. Impact medium.

## 7. Layer (multi-neuron) hulls: when does joint convexification help?

**Target.**
- For convex ridges with the same sign pattern and nonnegative combinations, the
  joint envelope equals the sum of single-neuron envelopes (the same staircase
  vertex), so multi-neuron cuts gain nothing.
- A strict gain exists otherwise, and exact separation is NP-hard when `k` is part of
  the input.
- Polynomial for fixed `k` (zonotope enumeration).
- A practical rule for which neuron pairs to group.

**Known.** Singh et al. (k-ReLU, NeurIPS 2019); Müller et al. (PRIMA, POPL 2022);
Tjandraatmadja et al. (2020).

**Risk.** Medium. Impact medium: it guides PRIMA-style cut selection.

## 8. Spatial-branching tree-size model for ridge and rank-one relaxations

**Target.** An abstract model in the style of Le Bodic & Nemhauser (Math. Program.
2017) in which the gap shrinks quadratically with width. Show the optimal choice
between branching on linear forms and on coordinates, and the optimal branch-point and
aspect-ratio rule, with matching lower bounds.

**Known.** Branching on neuron pre-activations is standard in verification (GenBaB,
Shi et al. 2024 *(unverified title)*). Kannan & Barton on convergence order. The
repository's cluster results overlap.

**Risk.** Medium. Impact low-medium.

## 9. Softmax / log-sum-exp / multinomial-logit hulls

**Target.** Hardness of the concave envelope of LSE on a box (the vertex problem is a
concave-of-modular closure under fixed Bernoulli marginals; expected NP-hard by a
partition reduction), plus tractable relaxations with guarantees.

**Why it matters.** Choice-based pricing and assortment optimization, and attention
layers.

**Known.** Wei et al. (AISTATS 2023) convex bounds on softmax *(unverified details)*;
MNL market-share reformulations.

**Risk.** Medium-high.

## 10. Radial composites `g(sum h_i(x_i))` (Gaussian-process and RBF kernels, distance costs)

**Target.** Envelope theory when the inner function is separable and convex. The
pushforward of `X_i` through `h_i` is no longer a convex-order down-set.

**Known.** Schweidtmann et al. (2021): Gaussian processes in deterministic global
optimization with McCormick relaxations.

**Risk.** High.

## 11. Pump and compressor affinity-law hulls

**Target.** Hulls of degree-2 homogeneous sets `h = s^2 H(q/s)` (and power) with speed
bounds and on/off indicators.

**Why it matters.** Pump scheduling and gas compressor stations.

**Known.** Parts appear in the water pump-scheduling literature (e.g., Bonvin,
Demassey, Lodi) *(unverified scope)*.

**Risk.** Medium. Impact medium but narrow.

## 12. Tree-ensemble consistency hulls (discarded)

The field is crowded. Mišić (OR 2020) is the base formulation. Later work gives ideal
single-tree formulations and a reciprocity with multilinear optimization over
products of simplices (Operations Research, 2023–24). A new strong theorem looks
unlikely. **Discard.**

### Other ideas discarded as known or incremental

- Optimal piecewise-linear breakpoints or sawtooth relaxations (Beach, Hildebrand,
  Huchette, and others; also the repository's precision results).
- Intersection and monoidal cuts for QCQP (Muñoz, Serrano, Chmiela).
- Perspective cuts for nonconvex on/off constraints (Bestuzheva, Gleixner, Vigerske).
- The perspective of the candidate-1 hull with an indicator (a Balas corollary).
- OBBT and FBBT theory.
- SDDP and Lagrangian cuts (Zhang & Sun).
- Bilinear terms with an integer factor (Gupte, Ahmed, Cheon, Dey).
- Two-dimensional bilinear projections (Müller et al., in SCIP).
- Pooling, row hulls and cluster analysis (the repository).

---

## Ranking (top 4)

1. **Candidate 1: convex-order ridge hulls.** This is one theorem with a short proof
   that is checked numerically. It covers every activation and every ridge term
   (sigmoid, tanh, SiLU, GELU, sin, inverse-S network laws). It also gives ideal MIP
   formulations over slabs, one-hot inputs and an `O(n log n)` separator. It extends
   Anderson et al., TRX 2013 and Carrasco–Muñoz (2026) with a single mechanism. The
   main risk is partial overlap with Carrasco–Muñoz, so the paper should lead with
   generality, the non-recursive formula and slabs.
2. **Candidate 2: staircase rank-one cuts and comonotone αBB for QCQP.** This has the
   largest potential audience (Gurobi MIQCP, BARON) and cheap linear cuts. The
   numerical check shows much tighter envelopes of `(b^T x)^2` than the
   eigenvector-secant cuts. The novelty check is less complete than for candidate 1.
3. **Candidate 3: network edge hulls.** This is the fastest route to measurable
   evidence on instances where the repository already found weak dual bounds
   (`waterno2`). It also covers GasLib and PGLib. Its theory depends on candidate 1,
   and its gains are uncertain.
4. **Candidate 7: layer hulls.** It gives a crisp "no gain versus strict gain"
   characterization that prevents wasted multi-neuron separation. It is chosen over
   candidate 4 because candidate 4's easy structure already failed numerically
   (23/100). Candidate 4 remains the natural follow-up if mixture and portfolio
   applications matter most.

## Sources consulted

- Carrasco & Muñoz: https://arxiv.org/abs/2410.23362 (Math. Program. 2026,
  https://link.springer.com/article/10.1007/s10107-026-02363-z)
- Tjandraatmadja et al.: https://arxiv.org/abs/2006.14076
- Wilhelm, Wang, Stuber: https://link.springer.com/article/10.1007/s10898-022-01228-x
- Nohra, Raghunathan, Sahinidis: https://arxiv.org/abs/2010.04822
- He, Liu, Tawarmalani: https://arxiv.org/abs/2310.08424
- Xu & Pokutta: https://arxiv.org/html/2608.03318
- Tree-ensemble reciprocity: https://pubsonline.informs.org/doi/10.1287/opre.2022.0150
- PRIMA: https://arxiv.org/pdf/2103.03638
