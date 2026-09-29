# Novelty check for theory.md (convex envelopes of sigma(a^T x + b) over a box)

Date: 2026-09-22. Scope: Theorem 1 ((P), (D), the functions `g_psi` and their cuts),
the "Computing (D)" section, Corollary 2 (order polytopes), and Corollary 3
(products of simplices), as in theory.md on this date. theory.md was not modified.

## Verdict in brief

- **The probabilistic core of Step 2 is already known.** The identity
  `M_x = {mu : mu <=_cx T_x}` is a special case of Mao and Wang (2015),
  Proposition 3.2. Their proof uses the same Strassen coupling and the same
  conditional-expectation construction. Combined with the standard identity
  `vex f(x) = min E f(X)` over `E X = x`, form (P) follows in a few lines.
  I found no paper that states (P) as a convex-envelope result.
- **Special cases of the envelope are known.** Concave `sigma` (or convex `sigma`
  for the concave envelope) is covered by TRX 2013, Corollary 3.14, which
  Tjandraatmadja et al. 2020 restate. The ReLU case is covered by Anderson et al. 2020.
  Convex and S-shaped `sigma` are covered by Carrasco–Muñoz 2026, Theorem 1,
  through a recursive formula over the box only.
- **Appears new.** I found no source that states the following:
  1. A characterization of `vex_B sigma(a^T x)` for arbitrary continuous `sigma`.
     This includes `sigma` with two or more inflection points in `I`: `sin`,
     cubics, GELU, and SiLU when `I` contains both of its inflection points.
     Confidence that the stated result is new: moderate to high.
  2. The dual (D), which describes the envelope as a supremum of Lovász extensions
     of `S -> psi(a(S))` over concave minorants `psi`, together with the cut family
     `h_{psi,pi}`, whose validity needs only feasibility of `psi`. Confidence:
     moderate to high. The ingredients are standard, but I found no paper that
     combines them for nonconvex, nonconcave `sigma`.
  3. Simplex localization for every continuous `sigma`: for `x` in `Delta_pi`,
     `vex_B f(x) = vex_{Delta_pi} f(x)`. This also gives the extensions of the
     envelope to order polytopes and products of simplices. Confidence: moderate.
     The statement is implicit in Mao–Wang's construction. For supermodular
     functions it is TRX Theorem 3.3 and Corollary 3.4.
- **How to position the result:** as a unifying characterization for arbitrary
  continuous `sigma`, obtained by combining the lower-convex-set theorem of
  Mao and Wang with the expectation form of the convex envelope and with Lovász
  extensions. It generalizes TRX Cor. 3.14 and extends Carrasco–Muñoz beyond
  STFE activations and beyond boxes. The paper should cite Mao–Wang as the
  source of Step 2, not reprove it as new. The practical contribution is the
  certificate-style cut family and the semi-infinite convex program (D) with
  `n+1` variables. The paper should not claim a closed form. For S-shaped
  `sigma`, it should defer to Carrasco–Muñoz.

## Source-by-source findings

### 1. Carrasco and Muñoz, arXiv 2410.23362v2 (30 Mar 2026), Math. Program. 2026 (doi 10.1007/s10107-026-02363-z). Full text read.

- **Setting.** The paper studies `S = {(x,y) in D x R : y = sigma(w^T x + b)}` with
  `D` a **box** only (Sec. 1, Sec. 3.1). It mentions polytopes only when
  describing [Anderson et al.; Tjandraatmadja et al.].
- **Class of `sigma`.** Definition 2 introduces the STFE property ("secant-then-function
  envelope"): on every interval, the univariate concave envelope is a secant from
  the left endpoint to a tie point `z_hat`, followed by `sigma` itself. Definition 1
  defines S-shaped functions as convex on `(-inf, z~]` and concave on `[z~, inf)`,
  so they have exactly one inflection point. The paper notes that convex,
  concave and S-shaped functions satisfy STFE.
- **Main result.** Theorem 1 (p. 5) is a **recursive** formula for
  `conc(f,[0,1]^n)`. It partitions the box into regions `R_f`, `R_l`, `R_1..R_n`
  (Definition 3). The envelope is `f` on `R_f` and linear on `R_l`. On `R_i` it is
  the perspective of the `(n-1)`-dimensional envelope on the facet `x_i = 1`.
  Evaluating it requires up to `n` univariate tie-point computations. The convex
  envelope is obtained by reflection: `sigma'(z) = -sigma(-z)` (p. 5).
- **What the paper says about non-S-shaped `sigma`.** The paper says it does not
  extend beyond these classes: "to the best of our knowledge, no prior work extends
  beyond this case" (convex `sigma`). It also notes that a closed form in the
  S-shaped case is hard to obtain, because the tie points change on faces (p. 7).
  The paper contains no statement about general continuous `sigma` or about
  `sigma` with two or more inflection points.
- **Tools not used.** The paper does not use convex order, Strassen's theorem,
  concave-minorant duality, or Kuhn/staircase simplices, except when it recovers
  TRX Cor. 3.14 as a check (eq. (4)–(6)). Its proof is an induction on `n`
  (Lemmas 9–14) together with Tawarmalani–Sahinidis 2002, Corollary 2, on
  envelopes restricted to faces.
- **SiLU claim.** Table 1 (App. A) lists SiLU as "S-shaped*", and App. A says SiLU
  "is concave and then convex; reflect the domain". This is inaccurate.
  `SiLU'' = 0` where `x tanh(x/2) = 2`, that is at `x = ±2.3994`, so SiLU is
  concave, then convex, then concave. Theorem 1 therefore applies only when `I`
  contains at most one of these points. GELU (inflection points `±sqrt 2`) is
  not listed. The draft covers both activations on every interval.
- **Overlap with the draft.** On the box, for STFE `sigma`, both papers
  characterize the same envelope. The draft's S-shaped remark ("To be checked
  against Carrasco–Muñoz") is fully covered by C–M Theorem 1. C–M's formula is
  explicit and recursive and needs no semi-infinite program.
- **What the draft adds.** Arbitrary continuous `sigma`; the (P)/(D) formulas
  that do not use recursion; localization to a single simplex; order polytopes
  and products of simplices; and cuts whose validity needs only feasibility of `psi`.

### 2. Tawarmalani, Richard and Xiong, Math. Program. 138 (2013) 531–577 (Optimization Online 2010/06/2640, preprint read)

- Theorem 3.3 (preprint p. 11): the concave envelope over `[0,1]^n` is the Lovász
  extension `f^K` if and only if `f` is supermodular on `{0,1}^n` and
  concave-extendable from the vertices. Equation (5) gives the min-over-permutations form.
- Corollary 3.4 (p. 12): the same holds over `S = [0,1]^n ∩ {x_i >= x_j, (i,j) in E}`
  with fixings. The text shows that Kuhn's triangulation subdivides `S`: a point
  sorted along a linear extension of the preorder lies in a Kuhn simplex whose
  vertices lie in `S`. This is exactly the geometric step of the draft's
  **Corollary 2**, but only for supermodular, concave-extendable functions.
- Corollary 3.14: for convex `f`, the concave envelope of `f(a_0 + sum a_i x_i)` over
  `[0,1]^n` is given by the switched Kuhn triangulation `K(T)`. The proof
  uses majorization (Karamata), which is the convex-order argument in its
  simplest form.
- Theorem 3.18 treats `f(sum x_i)` with convex `f` over a box cut by a constraint.
- **Nothing in TRX covers nonconvex `sigma` for the concave envelope, or nonconcave
  `sigma` for the convex envelope.** The draft's concave-`sigma` special case is exactly TRX Cor. 3.14.

### 3. He and Tawarmalani

- He and Tawarmalani, "Tractable relaxations of composite functions", Math. Oper. Res. 47 (2022)
  1110–1140, Theorem 2 as restated in He–Tawarmalani (2024), Proposition 4.4: if the outer function is
  concave-extendable from `vert(Q)` and supermodular over `vert(Q)`, then its concave
  envelope over a product of simplices `Q` is the minimum of staircase-simplex
  interpolations.
- He and Tawarmalani, "MIP relaxations in factorable programming" (SIAM J. Optim. 2024,
  arXiv 2310.07168; local copy `literature/papers/he2024-mip-relaxations-in-factorable-programming`),
  Section 4.2.1, Proposition 4.4 and Remark 5.4 use the same supermodularity
  hypotheses. The earlier version of this note conflated this paper with
  He, Liu and Tawarmalani, *Convexification Techniques for Fractional
  Programs* (arXiv 2310.08424), a separate work. The correction was checked
  against both local source texts on 2026-09-27.
- For `phi(z) = sigma(sum z_j)`, supermodularity together with concave-extendability
  holds essentially only for convex `sigma` on the concave-envelope side. **These
  papers give no envelope of `sigma(a^T x)` for S-shaped or multi-inflection
  `sigma`.** The staircase triangulation of a product of simplices, which the
  draft's Corollary 3 uses through tail sums and chains, is the triangulation
  these papers use.
- He and Tawarmalani, Math. Program. 2021 ("A new framework to relax composite
  functions"): I checked only the abstract and the citing papers, not the full
  text. Its tightness results rely on the same supermodular framework.

### 4. Anderson et al., Math. Program. 183 (2020); Tjandraatmadja et al., NeurIPS 2020 (arXiv 2006.14076, read)

- Anderson et al.: ideal formulations for the maximum of affine functions (ReLU and
  piecewise-linear convex `sigma`) over polytopes.
- Tjandraatmadja et al., Appendix A.1.2, Theorem 2: for **any convex** `rho` and
  `w >= 0`, `conv{y = rho(w^T x + b)}` over `[0,1]^n` is `{y >= g, y <= r_pi for all pi}`.
  Here `r_pi` are the Kuhn-simplex interpolations, and the proof uses the Lovász
  extension of a submodular set function. This restates TRX Cor. 3.14.
- Neither paper treats nonconvex `sigma`.

### 5. Neural-network verification literature on single neurons with general activations

- Wilhelm, Wang and Stuber, J. Glob. Optim. 85 (2023) 569–594: **univariate**
  envelopes of activations, including SiLU and GELU. They note that SiLU and GELU
  are concave, then convex, then concave. Their results are relevant only for the
  univariate subproblems.
- Zhang et al., ASE 2022 (arXiv 2208.09872), "Provably tightest linear approximation
  for sigmoid-like": linear bounds on the pre-activation interval (univariate)
  and a network-wise notion of tightness. The work does not address the
  `n`-dimensional hull.
- CROWN with general activations (Zhang et al. 2018), PRIMA (Müller et al. POPL 2022),
  and WraAct ("Convex Hull Approximation for Activation Functions", PACMPL/OOPSLA 2025):
  multi-neuron **over-approximations** for sigmoid and tanh. These methods are
  not exact and do not treat the single-neuron hull over the input box.
- Carrasco–Muñoz is the only exact `n`-dimensional result for nonconvex
  activations that I found.

### 6. Global-optimization literature on envelopes

- Crama 1993 and Lovász 1983: the Lovász extension is the concave envelope of a
  supermodular pseudo-Boolean function. The draft uses this in Steps 2(i) and 4.
- Jach, Michaels and Weismantel, SIAM J. Optim. 19 (2008): `(n-1)`-convex functions,
  that is, functions that are convex after fixing any one variable. For `n >= 2`,
  `sigma(a^T x)` is not of this type unless `sigma` is convex.
- Khajavirad and Sahinidis, Math. Program. 137 (2013), local copy read: a
  convex-program formulation using generating sets, and Proposition 2, which
  restates TRX Thm 3.3. The formulation is general. Carrasco–Muñoz note that it
  yields no explicit form for ridge functions, and I found none either.
- Meyer–Floudas (edge-concave functions), Locatelli and Schoen (bivariate functions
  over polytopes), Sherali 1997 (multilinear functions), and Barrera, Moreno and
  Muñoz 2022 (ray-concave functions) do not cover general ridge functions.
- Recent arXiv papers (2024–2026) that I checked do not overlap with the draft.
  These include superposition relaxations (2605.10854), KAN convexification by
  Graham scan (2604.03871, univariate), axis-aligned relaxations (2603.18458), and
  separable power functions over polytopes (2510.16595).

### 7. Probability and risk aggregation: where Step 2 is already known

- **Mao and Wang, "On aggregation sets and lower-convex sets", J. Multivariate Anal. 138 (2015)
  170–181**, preprint read, Proposition 3.2. They show
  `C_n(F_1..F_n) := {X_1+...+X_n : X_i <=_cx Y_i ~ F_i}` equals `{S : S <=_cx F_1^{-1}(U)+...+F_n^{-1}(U)}`.
  Take `F_i` to be the law of `a_i Bernoulli(x_i)`. Then `X_i <=_cx F_i` holds exactly
  when `X_i ∈ [0,a_i]` and `E X_i = a_i x_i`, so `C_n = M_x` and the comonotone sum is `T_x`.
  The proof is the draft's Step 2(ii): a Strassen coupling `E[Y|S] = S`, followed by
  `X_i = E[F_i^{-1}(F(Y)) | S]`. The inclusion `⊂` is Dhaene et al. 2002, Corollary 1,
  as cited by Mao–Wang. It goes back to Meilijson and Nádas 1979.
- Mao–Wang, Theorem 4.2, adds a further fact: every element of `C_n` is a
  **comonotone** sum of `X_i <=_cx F_i`. So a minimizer of (P) can be realized
  by a comonotone random point `X`. The draft does not use this.
- Step 1 (`vex f(x) = min E f(X)` over `E X = x`, with at most `n+2` atoms) is
  classical. See Rockafellar, Convex Analysis, Cor. 17.1.5, and the generalized
  moment problem (Kemperman 1968).
- The law-level duality `inf{∫sigma dmu : mu <=_cx nu} = sup{∫psi dnu : psi concave <= sigma}`
  is a Lagrangian duality for a convex-order constraint. It has the same type as
  martingale-transport duality with a free first marginal (Beiglböck,
  Henry-Labordère and Penkner 2013) and as stochastic-dominance duality with
  concave utilities as multipliers (Dentcheva and Ruszczyński 2003). I did not
  locate this exact statement. The draft proves it directly in finite dimension,
  which is short and self-contained. Treat it as standard in kind, not as a
  novelty claim.
- Bach, "Submodular functions: from discrete to continuous domains" (Math.
  Program. 2019), links comonotone (quantile) couplings to Lovász extensions for
  continuous submodular functions. This is related in spirit but does not
  concern envelopes.

## Mathematical check of the draft

Steps 1–4 are correct as written. Checked items: supermodularity of
`phi(a(S))` for convex `phi`; the interpolation bound on each Kuhn simplex;
the Strassen construction and `a^T E[v_K|S] = S`; the upper-concave-hull
argument in Step 3; the attainment argument when all `p_k > 0`; the
`-sqrt` counterexample (sup 0 is approached by `psi = -eps - s/(4 eps)` but not attained);
and the Edmonds/greedy identification of `h_{psi,pi}`. I also checked the
tail-sum map in Corollary 3 and the containment `Delta_pi ⊂ O(Q)` in Corollary 2.

I also ran a numerical check in `/tmp/nov/check.py`, which is not saved in the
repository. It solves three LPs on random instances with `n = 2, 3` and
`sigma = sin`, SiLU and `s^3 - 3s`:

- a grid LP for `vex_B f(x)`;
- (D), discretized;
- (P), discretized, with stop-loss constraints.

On all 18 instances the three values agree to discretization accuracy, at most
`2e-4` apart. The grid values are slightly higher in the coarse `n = 3` cubic cases,
as expected, because a coarse grid gives an upper bound. Most SiLU instances had
`vex = f` and tested little.

Issues, all minor:

1. **Corollary 2 terminology.** With the convention `i <=_Q j => z_i >= z_j`, an
   initial segment of a linear extension is a **down-set** (order ideal), not an
   up-set. The argument itself is correct.
2. **S-shaped bullet in "Computing (D)".** The claim is that the optimal `psi`
   is `sigma` on a right block of nodes and "one tangent line" on the left. This
   is unproven, and "tangent" may be wrong. At an optimum, the concavity
   constraint at the switch node may bind. The left affine piece would then
   extend the chord through the first two `sigma`-nodes, and it would not need
   to be tangent to `sigma`. I have not built an example of this. The right
   block can also be empty. Either prove the claim or replace it with a citation to
   Carrasco–Muñoz Theorem 1.
3. **Convex `sigma` bullet.** "The tangent at `a^T x`" needs a finite subgradient.
   At the endpoints of `I`, `x` is a vertex and the supremum may not be attained,
   which is consistent with the draft's attainment remark. Write "a supporting
   line (when it exists)".
4. **Missing citations in "Relation to known results".** Add Mao–Wang 2015
   (Prop. 3.2, Thm 4.2) as the source of Step 2. Add TRX Thm 3.3 and Cor. 3.4 for
   the Kuhn subdivision of order-constrained boxes. Add Tjandraatmadja et al.
   2020, App. A Thm 2. Correct the C–M SiLU scope as described above.

## Sources

- Carrasco, Muñoz: https://arxiv.org/abs/2410.23362 ; https://link.springer.com/article/10.1007/s10107-026-02363-z
- Tawarmalani, Richard, Xiong: https://optimization-online.org/2010/06/2640/ ; https://link.springer.com/article/10.1007/s10107-012-0581-4
- Tjandraatmadja et al.: https://arxiv.org/abs/2006.14076
- Mao, Wang: https://www.sciencedirect.com/science/article/pii/S0047259X14002668 (preprint https://www.math.uwaterloo.ca/~wang/papers/2015Mao-Wang-JMVA.pdf)
- He, Tawarmalani (MOR 2022): https://pubsonline.informs.org/doi/10.1287/moor.2021.1162
- Wilhelm, Wang, Stuber: https://link.springer.com/article/10.1007/s10898-022-01228-x
- Zhang et al. ASE 2022: https://arxiv.org/abs/2208.09872
- WraAct (PACMPL 2025): https://dl.acm.org/doi/10.1145/3763086
