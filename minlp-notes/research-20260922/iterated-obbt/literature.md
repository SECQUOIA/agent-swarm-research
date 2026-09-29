# Iterated OBBT: literature investigation

Date: 2026-09-23. Status: literature report for `plan.md` (novelty questions)
and `theory.md` (Propositions 2–3, Theorems 4 and 6, Propositions 7–8).
Scope: theory of iterating optimality-based bound tightening (OBBT, also called
range reduction, domain reduction, bound contraction) to a fixed point; rates
near a minimizer; solver practice; empirical evidence.

**Reading status.** I read the full texts of Caprara–Locatelli (2010),
Caprara–Locatelli–Monaci (2016), Ryoo–Sahinidis (1996), Zamora–Grossmann (1999),
the Gleixner et al. (2017) preprint, and the local KB copies of Puranik–Sahinidis
(2017), Belotti et al. (2012), Ryoo–Sahinidis (1995), Tawarmalani–Sahinidis
(2004) and Castro (2023). Delegated searches read the full texts of Kannan–Barton
(2017, 2018), Du–Kearfott, Schichl–Neumaier, Neumaier (2004), the power-systems
papers, and the solver source code listed in Section 3. The following were
**not accessible**: the Locatelli–Schoen book chapter (SIAM 2013, §5.5
"Domain reduction", pp. 335–357; only its table of contents was checked), the
Faria–Bagajewicz papers (only abstracts and a secondary description were
available), Wechsung–Schaber–Barton (2014), Bompadre–Mitsos (2012), Kannan's
thesis, and the primary ANTIGONE JOGO paper. A negative search does not prove
novelty.

**Access update, 2026-09-27.** The historical access statement above describes
the initial pass. The [cluster follow-up](literature-cluster.md) read the
Wechsung and Kannan theses. The 2026-09-26 library and inbox reviews then
packaged Kannan’s thesis and the journal originals of both Caprara papers,
Kannan–Barton (2017), and Wechsung–Schaber–Barton (2014). The latter is now
read directly: its second-order prefactor thresholds appear on PDF pages 8–9
([[wechsung2014-the-cluster-problem-revisited]] p.8-9). These sources
confirm the distinctions below between fixed-point results, clustering, and
OBBT contraction rates. They do not establish the absence of a rate theorem
in all literature.

## 0. Findings

**Known (with proofs):**

1. Iterated OBBT gives a monotone decreasing sequence of boxes. The sequence has
   a limit, and that limit is a valid reduction. Caprara and Locatelli (2010)
   say explicitly that the iteration is in general "just convergent to the final
   result after infinitely many iterations" (p. 126).
2. **Characterization of the one-variable limit.** Iterating OBBT on one
   variable `x_k` with the other bounds fixed (ISDR) has the same limit as
   NRDR. NRDR fixes `x_k = t`, bounds the resulting restricted problem to get
   the value function `h_k(t)`, and keeps `{t : h_k(t) >= l*}` (maximization
   form). This holds under Assumptions 2–4, which are satisfied for Lipschitz
   `f` with concave-envelope relaxations (Theorem 1 p. 131; Corollary 1
   p. 134).
3. **Order independence.** For any monotone reduction operator, the limit of
   cyclic sweeps over all variables does not depend on the variable order
   (Caprara–Locatelli 2010, Proposition 1, p. 135).
4. **When the limit is exact.** The limit equals the ideal box `B_UB` (the box
   hull of the `UB`-level set) for a two-variable class: objective of
   `x_1, x_2` only, concave and monotone in each variable, Lipschitz, over a
   convex feasible set. With `UB = f*` and a unique optimal projection, the
   limit is a single point (Caprara–Locatelli–Monaci 2016, Theorem 1, p. 521).
   Three small counterexamples show that slightly larger classes can stall
   completely, with no reduction at all even with `UB = f*` (§3.1,
   pp. 522–524).
5. **Contrast with FBBT.** For feasibility-based propagation (FBBT), the limit
   is the greatest fixed point of a monotone deflationary lattice operator. The
   limit is reached finitely only in special cases (Theorem 3.3: never, if the
   limit has lower affine dimension). Convergence can be geometric, for example
   ratio `1/a` in Example 2.4. For linear constraints the limit is computable by
   one LP (Belotti et al. 2012, Theorems 3.1, 3.3, 4.1). Belotti et al. note
   that iterated OBBT ("OBBT*") may likewise "fail to converge to the respective
   limit points" (p. 5). No complexity result for the OBBT limit was found.

**Apparently open (no published statement found):**

- Any convergence *rate* for iterated OBBT. The only quantitative statements
  are per-step lower bounds on progress that are used to prove convergence
  (Caprara–Locatelli 2010 p. 131; Caprara–Locatelli–Monaci 2016 p. 520).
- Linear contraction with ratio of order `sqrt(tau/mu)` down to width of order
  `sqrt(epsilon/mu)` under quadratic growth, quadratic contraction to `O(epsilon)`
  at sharp minima, or any scaling law of the fixed-point width in the cutoff
  slack `epsilon`.
- Exact rates for model problems such as `x^2 + y^2 + a x y` with McCormick
  relaxations, and the tangent-map / cone-spectral-radius characterization in
  `theory.md`.
- Finite termination, and the complexity of computing the OBBT fixed point.
- A stopping rule with a certified bound on the remaining tightening. The
  inspected rules use round caps, improvement tolerances, or a box-volume
  factor of 0.95. Some have a finite-termination argument (see Ryoo–Sahinidis
  below); that does not bound the distance to the OBBT limit.

The ingredients of `theory.md` Propositions 2–3 are classical: the
`sqrt(epsilon/gamma)` radius of the near-optimal set (Kannan–Barton 2017,
Lemma 8) and the marginals bound `(U - L)/lambda` (Ryoo–Sahinidis 1995,
Theorem 2). No such combined statement about iterated OBBT was found in the
sources inspected.
Propositions 2–3 should therefore be presented as elementary consequences, not
as new principles. Theorems 4 and 6 and Propositions 7–8 have no counterpart
that I found.

## 1. Theory of the iterated OBBT limit (question 1)

### 1.1 Caprara and Locatelli, "Global optimization problems and domain reduction strategies", Math. Program. 125 (2010) 123–137

Full text read (doi:10.1007/s10107-008-0263-4).

- **Setting.** Maximize a nonconcave `f` over `F ∩ B`, with `F` closed, convex
  and bounded. There is a concave overestimator `g` that depends on the box
  (Remark 1, p. 125). Only the objective is nonconvex. `l*` is the incumbent
  value.
- **SDR (p. 127).** Solve `min/max {x_k : g(x) >= l*, x ∈ F ∩ B}` (eq. 4), the
  "quite popular" OBBT with an objective cutoff.
- **ISDR (p. 127).** Iterate SDR on a *single* variable `x_k`: rebuild
  `g_i` on the box `B_i`, in which only `x_k`'s bounds have changed (eq. 6),
  and stop when nothing changes. The paper states: "The above procedure either
  terminates after a finite number of iterations, or generates an infinite
  nondecreasing sequence {l_k^i} of lower bounds and an infinite nonincreasing
  sequence {u_k^i} of upper bounds. In both cases the values `l_k^ISDR = sup_i
  l_k^i`, `u_k^ISDR = inf_i u_k^i` define a valid domain reduction."
- **NRDR (p. 128, eqs. 9–11).** `h_k(t) = max{g_k^t(x_{-k}) : x_{-k} ∈ F_k^t ∩
  B_{-k}}`, where `g_k^t` overestimates `f` with `x_k = t` fixed. The new bounds
  are the inf and sup of `{t : h_k(t) >= l*}`. The name refers to removing the
  nonlinearities that involve `x_k`.
- **Observations 1–2 (p. 129).** NRDR dominates SDR (Assumption 1) and ISDR
  (Assumption 2).
- **Theorem 1 (p. 131).** Under Assumption 2 (the overestimator with `x_k` fixed
  is no worse), Assumption 3 (continuity in `x_{-k}` and `t`) and Assumption 4,
  `[l^NRDR, u^NRDR] = [l^ISDR, u^ISDR]`. Assumption 4 is a bracketing bound
  `g_i(x^{(k)}(t)) <= g_k^t(x_{-k}) + eta* min{t - l_k^i, u_k^i - t}`.
  - The proof is by contradiction. If the ISDR limit stopped short, each step
    would advance by at least `rho_k/eta* > 0`, which contradicts boundedness.
    This is a convergence argument, **not a rate**.
- **Corollary 1 (p. 134).** If `f` is Lipschitz with constant `L`
  (Assumption 5) and `g_i`, `g_k^t` are concave envelopes, Assumptions 2–4 hold
  with `eta* = 2L` (Observations 4–6), so ISDR = NRDR.
- **Interpretation (p. 129).** "iterating the standard domain reduction has the
  same effect as removing all the nonlinearities involving variable x_k in (1)
  and studying the resulting relaxation." This is the paper's answer to what
  the limit relaxation is: the one-variable limit is as tight as branching
  infinitely finely on `x_k` alone (my paraphrase). It is exact in `x_k` only
  when the restricted problems are relaxed exactly.
- **Finite versus infinite (p. 126).** "while the iterated version is just
  convergent to the final result after infinitely many iterations, parametric
  analysis may return such a result after a finite time." The special classes
  where `h_k` is explicit are in the technical report [1] ("Domain reduction
  strategies: general theory and special cases", Univ. Torino, 2008), which
  I could not obtain.
- **§7, "Multiple domain reduction" (pp. 134–135).** Cyclic sweeps over all
  variables in a fixed order `P`, "iteratively repeat[ed] … until there are
  reductions (in practical implementations, large enough reductions)".
  **Proposition 1:** under Assumption 6 (monotonicity: a smaller input box
  gives a smaller output interval), `l_j^i → l̄_j` and `u_j^i → ū_j`, and the
  limits do not depend on `P`. The proof compares `nu` sweeps in one order with
  `nu n` sweeps in another.
- **Not in the paper:** rates, complexity, finite termination of the joint
  iteration, dependence on the cutoff, and nonconvex constraints.

### 1.2 Caprara, Locatelli and Monaci, "Theoretical and computational results about optimality-based domain reductions", Comput. Optim. Appl. 64 (2016) 513–533

Full text read (doi:10.1007/s10589-015-9818-5). Minimization form:
`min f(x_1..x_t)` over a closed convex `F`.

- **Lower limit (pp. 514–515).** `B_UB` is "the smallest box enclosing all
  feasible points … with function value not larger than UB", so
  `B_UB ⊆ B_DR ⊆ B` for every optimality-based reduction. The abstract says:
  "we can easily define a lower limit for the reduction which can be attained,
  but we can hardly guarantee that such limit is reached."
- **Notation (p. 516).** `S(v, w)` applies SDR at most `w` times per variable
  and at most `v` sweeps. `NR(v)` applies NRDR for `v` sweeps. By 2010
  Theorem 1, `NR(v) = S(v, ∞)`. The limit of cyclic sweeps is order independent
  (citing 2010).
- **Theorem 1 (p. 521).** Take `t = 2` under Assumption 1 (p. 518): `f(α, ·)`
  and `f(·, β)` concave and monotone, and `f` Lipschitz. This covers
  `x_2 - x_1^2`, `x_1 x_2` with positive variables, `x_2 - 1/x_1`,
  `1/x_1 + 1/x_2`, and linear multiplicative programs with two factors.
  Iterating feasibility-based reduction on one side and NRDR on the other side
  (the "Mixed DR") "either leads to an improved upper bound UB, or identifies a
  rectangle … `= B_UB`". With `UB = f*` and a unique optimal `(x_1, x_2)`, "the
  rectangle will be reduced to a single point".
  - Lemmas 1–2 (pp. 519–521) give only convergence. The step bound
    `l_1^{r+1} - l_1^r >= (h_1^r(ᾱ) - UB)/L` rules out a premature limit but
    gives no rate.
- **§3.1 counterexamples (pp. 522–524).** `NR(∞)` makes **no reduction at all**
  although `B_UB` is a single vertex and `UB = f*`, in three cases:
  - (a) three variables in a concave objective, `min -x1^2 - x2^2 - x3^2` over
    a polytope;
  - (b) two nonlinear variables plus a linear third;
  - (c) a non-monotone objective, `min -(x1-1/2)^2 - (x2-1/2)^2` over a pentagon.

  These are published precedents for complete stalling at `epsilon = 0`
  (compare `theory.md` Theorem 6 and Proposition 8, which concern convex
  quadratic objectives with McCormick relaxations; that setting is different
  and not covered by these examples).
- **Computation (LMP, `p ∈ {2,...,20}`, 250 instances; Table 2 p. 528).** Mean
  root gaps:

  | Strategy | S(0,0) | S(1,1) | S(1,10) | S(10,1) | S(10,10) | NR(1) | NR(∞) |
  |---|---|---|---|---|---|---|---|
  | Root gap (%) | 8.70 | 8.39 | 7.17 | 4.10 | 4.05 | 7.15 | 4.02 |

  Repeating sweeps over all variables matters much more than repeating the
  solve for one variable.
  - In B&B (Tables 3–4, p. 529ff.), `S(1,10)` and `S(10,10)` solve 169 and 168
    of 250 instances, against 141 without reduction.
  - For `p <= 5`, no reduction is fastest.
  - The authors conclude: "there is not a strategy which dominates the others"
    (p. 529).

### 1.3 Other theory items

- **Belotti, Cafieri, Lee, Liberti, "On feasibility based bounds tightening"
  (Optimization Online 2012; local KB).**
  - p. 5 defines OBBT* (rebuild the relaxation and re-run OBBT): "Both FBBT and
    OBBT* may fail to converge to the respective limit points: in practice,
    termination is enforced by stopping the procedures when progress is too
    slow."
  - Theorem 3.1 (p. 10): the Kleene/Tarski limit of a monotone deflationary
    operator is the greatest fixed point.
  - Theorem 3.3 (p. 12): FBBT never reaches a limit whose affine dimension is
    smaller than that of the start box.
  - Theorem 4.1 (p. 14): for linear constraints the FBBT limit is one LP.
  - Example 2.4 (pp. 8–9): `X_1 = [0, a^{-(2k-1)}]`, `X_2 = [0, a^{-2k}]`, a
    geometric rate.
  - Nothing on OBBT rates.
- **Gleixner, Berthold, Müller, Weltge, "Three enhancements for
  optimization-based bound tightening", J. Glob. Optim. 67 (2017) 731–757
  (ZIB-Report 15-16; preprint pp. 4–6, 12–13, 20).**
  - p. 4: "[14] present a theoretical study of an iterated version of OBBT",
    where [14] is Caprara–Locatelli 2010.
  - Example 1: `min{y - x : y = 0.1x^3 - 1.1x, x ∈ [-4,4], y ∈ [-2,2]}`, cutoff
    `U = 0` from the zero solution. "continuing to iterate between OBBT and the
    refinement of the relaxation would result in an infinite series of lower
    bounds on x that converge towards zero. The difficulty in iterating OBBT is
    its high computational cost" (p. 6). Their remedy is Lagrangian variable
    bounds (LVBs), "an approximation of iterated OBBT during the entire solving
    process" (p. 13).
- **Puranik and Sahinidis, Constraints 22 (2017) 338–376 (arXiv version,
  local KB).**
  - p. 12: "problem 26 can be solved iteratively to obtain further tightening.
    However, convergence to a fixed point can be slow."
  - p. 9: domain reductions in MINLP "are usually not iterated until they reach
    a certain level of consistency because attempting to establish consistency
    can lead to a prohibitively large computational effort".
  - p. 15: the cluster effect needs convergence order at least 2.
  - The survey calls OBBT without a cutoff a *feasibility*-based technique
    (p. 6).
- **Ryoo and Sahinidis, "A branch-and-reduce approach to global
  optimization", J. Glob. Optim. 8 (1996) 107–138 (full text read).**
  - Step 6 (pp. 116–117): after optimality- and feasibility-based reduction,
    "If the range reduction was successful in reducing the range of at least
    one variable of R_i by at least a prespecified amount δ > 0, then:
    Reconstruct R_i … Go to Step 4."
  - Proposition 3 (p. 117) proves this loop is finite because of `δ`.
  - Remark 3 gives an alternative: continue only if the lower bound improves by
    a fixed amount.
  - This is the earliest published stopping rule, justified only by
    finiteness.
  - The earlier CACE 1995 paper (local KB, p. 558, Remark 9) caps re-solves at
    MAXSOLVE, "thus avoiding the possibility of slow, asymptotic convergence of
    the bounds". Its Theorem 2 (p. 554) is the marginals test
    `x_j >= x_j^U - (U - L)/lambda_j`.
- **Tawarmalani and Sahinidis, Math. Program. 99 (2004) 563–591, §4 (local
  KB).** A Lagrangian-duality framework that re-derives the range reduction
  tests (Theorem 4.1) and a learning reduction. It says nothing about iteration
  or rates.
- **Zamora and Grossmann, "A branch and contract algorithm …", J. Glob. Optim.
  14 (1999) 217–249 (full text read).**
  - The "contraction operation" (§4, pp. 226–228) sequences single-bound
    contraction subproblems (`min/max x_i` over the relaxation plus the
    objective cutoff). It picks the bound farthest from the incumbent (the
    "focal point"). A step with step performance `SP < SP_min` marks that bound,
    and the operation stops when a fraction `F_CV` of variables is marked or at
    step caps (Step C10). The paper describes the operation only as having
    "finite termination" (p. 226). There is no convergence theory for the
    limit.
- **Cabassi, Consolini, Locatelli, Comput. Optim. Appl. 70 (2018) 61–90.** A
  feasibility-type bound tightening for monotone constraint systems. The
  component-wise maximum is the greatest fixed point (Knaster–Tarski). The
  method is finite under a superiority condition; otherwise it takes at most
  `sum u_i / epsilon` iterations (Observation 3.2) and converges for
  `epsilon = 0` (Corollary 3.1). This is not OBBT, but it is a related
  fixed-point analysis by the same group.
- **Locatelli and Schoen, *Global Optimization: Theory, Algorithms, and
  Applications*, SIAM 2013, §5.5 "Domain reduction" (pp. 335–357).** Not
  accessible. It is likely, but unverified, that it presents the 2010/2016
  material.

## 2. Rates near a minimizer (question 2)

No published rate for iterated OBBT was found. The closest pieces are:

- **Near-optimal set size.**
  - Kannan and Barton, "The cluster problem in constrained global
    optimization", JOGO 69 (2017), Lemma 8 (manuscript p. 19): under
    `∇f(x*)'d + d'∇²f(x*)d/2 >= gamma ||d||^2`, the `epsilon`-optimal feasible
    points lie in `{gamma ||x - x*||^2 <= 2 epsilon}`. Theorem 3 counts boxes
    with `r = sqrt(2 epsilon/gamma)`.
  - Neumaier 2004 (Acta Numerica §15, preprint p. 46): an incumbent optimal
    within `O(epsilon)` is only located to `O(sqrt(epsilon))`. Backboxing
    reduces such a box "until no significant improvement results".

  These papers give the **scale** of the lower limit `B_UB`. They do not give
  the rate of OBBT.
- **Marginals bound (single step).** Ryoo–Sahinidis 1995 Theorem 2 gives
  `w^+ <= (U - L)/lambda`. With `L >= f* - tau w^2`, this is `theory.md`
  Proposition 2 (sharp minima: quadratic contraction to `O(epsilon)`). The
  consequence is immediate but not stated anywhere I found.
- **Convergence order and domain reduction.**
  - Kannan and Barton, JOGO 71 (2018), manuscript p. 17: FBBT "is ineffective
    in boosting the convergence order" in full space.
  - Examples 17–18 (pp. 41–43): in reduced space, propagation raises the order
    from 1 to 2. The conclusion (p. 49) lists sufficient conditions on the
    propagation scheme for second-order convergence as future work.

  Domain reduction appears there only as something that raises the
  convergence order, not as box contraction with a rate.
- **Cluster literature without domain reduction.**
  - Du–Kearfott (1994) exclude acceleration procedures ("no acceleration
    procedures", abstract).
  - Wechsung–Schaber–Barton (2014) analyze bound convergence order and
    prefactors; the journal original is now read (PDF pp. 8–9).
    Bompadre–Mitsos (2012) was assessed from abstracts and Kannan–Barton’s
    summaries; that original remains unread in this review.
  - Schichl–Neumaier (SINUM 2004, preprint p. 6) and Schichl–Markót–Neumaier
    (JOGO 2014, pp. 5–6) state that constraint propagation has overestimation
    order 1 and "suffer[s] from the cluster effect".
- **Geometric rates in propagation (analogue).** Belotti et al. Example 2.4
  (ratio `1/a`); Puranik–Sahinidis p. 9, example `x1 + x2 = 0`,
  `x1 - q x2 = 0` (ratio `q`). These are FBBT on linear systems, not OBBT near
  a minimizer.
- **Model problems.** I found no exact rate for `x^2 + y^2 + a x y` with
  McCormick, or for any comparable model. The only published OBBT sequences
  with enough digits to read off a rate are Zamora–Grossmann's Tables 2–3
  (next item).
- **Published data consistent with a linear rate (my reading, not the
  authors').**
  - Zamora–Grossmann Example 1 (pp. 232–235):
    `min x1^2 + 2 x2^2 - 50 x1 - 80 x2 + 250` s.t. `x1 x2 + x1 = 50`, McCormick
    relaxation, cutoff at the global value `-667.131955`, strategy S2
    (contraction on `x2`, feasibility propagation to `x1`).
  - In Table 3 (p. 235), from step 5 on, every contraction step removes
    `SP ≈ 0.43` of the `x2` domain. The relative gap ratio per step is
    0.313, 0.332, 0.322, 0.328, 0.325, 0.326, 0.326, 0.326, 0.326 (computed
    from their column `ε(Ω0)`).
  - The gap ratio `≈ 0.326 ≈ (1 - 0.429)^2 = 0.326`. So the gap shrinks with
    the square of the width, and the width shrinks linearly, as a
    quadratic-growth plus order-2-relaxation analysis predicts.
  - This is a constrained minimizer (nonconvex equality) with a single-variable
    contraction schedule, so it is evidence, not a test, of `theory.md`
    Theorem 4.
- **Verdict.** The statements in question 2 (linear rate of order
  `sqrt(tau/mu)` to width of order `sqrt(epsilon/mu)`; quadratic to
  `O(epsilon)` at sharp minima; exact model rates) appear unpublished. The
  sharp-minimum case is a two-line consequence of the marginals bound. The
  other statements need the new argument in `theory.md`. Caveats: the Torino
  technical report and Locatelli–Schoen chapter remain unread. Kannan’s and
  Wechsung’s theses were subsequently read in the cluster follow-up.

## 3. Solver practice (question 3)

All claims below come from source code or official documentation unless marked
otherwise. Page numbers refer to the sources named.

- **SCIP** (`src/scip/prop_obbt.c`, checked from v3.2.1 to 11.0.0).
  - Fixed settings: `PROP_FREQ 0`, which means root node only; `PROP_DELAY
    TRUE`; priority -1000000; timing `AFTERLPLOOP`.
  - "only run once in a node != root". At the root, a repeated call continues
    with bounds not yet processed: "each variable direction is tested at most
    once per node" (Gleixner et al. p. 12).
  - **There are no rounds.** The source carries the todo "only run more than
    once in root node if primal bound improved or many cuts were added to the
    LP", present since v3.2.1.
  - Key defaults:
    - `itlimitfactor = 10` (times the root LP iterations), `minitlimit = 5000`;
    - `boundstreps = 0.001` (minimal relative improvement);
    - `onlynonconvexvars = TRUE` (since SCIP 8);
    - `applyfilterrounds = FALSE`, `minfilter = 2`;
    - `separatesol = FALSE`, `sepamaxiter = 10`;
    - `orderingalgo = 1` (greedy); `dualfeastol = 1e-9`;
    - `createbilinineqs = TRUE`; `indicators = FALSE` (SCIP 9).
  - Continuous bounds found are applied only after the probing pass, so all LPs
    in the pass use the same relaxation.
  - OBBT runs again at each restart's root (inference from the `initsol`
    reset).
  - The substitute for iterating is the `genvbounds` propagator: LVBs learned
    from OBBT duals are propagated at every node and globally on incumbent
    improvement (Vigerske–Gleixner 2017).
  - Gleixner et al. (2017, preprint p. 20): "OBBT alone does not give a
    significant speedup on average". OBBT plus LVB propagation gives 17–19% on
    instances that take at least 100 s (abstract and p. 20).
- **BARON.**
  - Options: `TDo`, `MDo`, `LBTTDo`, `OBTTDo` (optimality-based tightening),
    and `PDo` (number of probing problems, `-2` automatic). There is no public
    option for the number of passes.
  - Manual §5.3: reductions apply "at every node", and BARON "may repeat the
    reduction process" after rebuilding the relaxation. The repeat rule is not
    documented.
  - The published ancestors are the `δ`-threshold loop (1996, Prop. 3) and the
    MAXSOLVE cap (1995, Remark 9).
- **Couenne** (`src/bound_tightening/obbt.cpp`).
  - `#define MAX_OBBT_ATTEMPTS 1 // number of OBBT iterations at root node --
    fixed at one as for some instance it doesn't seem to do anything after
    first run`; `MAX_OBBT_ITER 1`.
  - OBBT runs at node depth `λ` with probability `2^(k - λ)`, where `k` is
    `log_num_obbt_per_level` (source default 1; the manual says 4). Each
    improved bound is applied immediately, followed by FBBT.
  - Only FBBT loops (`max_fbbt_iter = 3`). Belotti et al. (2009) justify the
    FBBT cap with a non-terminating example.
- **ANTIGONE and GloMIQO.**
  - GAMS options: `max_obbt_iterations = 30` and `obbt_improvement_bound =
    0.95`, described as "Bounds reduction improvement threshold needed to exit
    OBBT loop … if the parent bound improvement is less than this threshold,
    then child node won't try OBBT". Also `max_time_each_obbt = 10 s`.
  - Misener–Floudas (MIQCQP preprint, Optimization Online 3240): OBBT runs at
    the root "with the same volume improvement parameter 0.95" and continues in
    the tree while it tightens significantly. They justify stopping with an
    example of bounds that converge only asymptotically.
  - The `2^(λ - depth)` restart probability comes from Gleixner et al. p. 4
    (secondary source).
  - This is the only published rule based on relative (box-volume) progress.
- **Gurobi.** The `OBBT` parameter (-1 to 3, default -1 automatic) controls
  "the amount of work allowed … from moderate to aggressive". No stopping rule
  is documented.
- **Alpine.jl** (v0.5.8, `src/presolve.jl`).
  - Defaults: `presolve_bt_max_iter = 25`, `presolve_bt_improv_tol = 1e-3`,
    `presolve_bt_width_tol = 1e-2`, `presolve_bt_time_limit = 900`.
  - It iterates while the average and the maximum absolute range reduction
    both exceed `1e-3`, the widest range exceeds `width_tol`, and the gap
    exceeds `rel_gap`. Sweeps are Gauss–Seidel style.
  - The documentation is stale: it lists `max_iter = 9999` and
    `width_tol = 1e-3`.
  - Nagarajan et al. (JOGO 2019, p. 12): "The OBBT algorithm stops when
    cumulative bound improvement between successive iterations, measured in
    terms of the ℓ∞ norm, falls below specified tolerance values". Remark 1
    claims iteration "until convergence to a fixed point", without proof.
- **PowerModels.jl** (`src/util/obbt.jl`).
  - Defaults: `max_iter = 100`, `improvement_tol = 1e-3`,
    `min_bound_width = 1e-2`, `termination = :avg`, `time_limit = 3600`.
  - Sweeps are Jacobi style: the model is rebuilt only after a full sweep.
- **MAiNGO.**
  - Root: up to `PRE_obbtMaxRounds = 10` rounds, stopping when no bound moves
    by more than `1e-6`, plus one extra round with the objective cut after
    multistart.
  - At other nodes: one pass, run with probability `exp(-c · depth)`.
  - `LBP_obbtMinImprovement = 0.01` filters bounds that cannot improve by more
    than 1% of the width.
- **EAGO.** `obbt_repetitions = 3` and `obbt_depth = 6`; the loop breaks when
  the box is exactly unchanged.
- **Coramin.** `root_obbt_max_iter = 1000`; it stops when the average absolute
  improvements fall below `1e-3`. `obbt_at_new_incumbents = True` is the only
  default found that re-runs OBBT on incumbent improvement.
- **Octeract.** `OBBT_MAX_ITERATIONS = 1` ("maximum number of passes").
- **RAPOSa** (arXiv 2403.02823). One root pass, capped at 20% of the time
  limit.
- **Castro** (Ind. Eng. Chem. Res. 62 (2023) 11053–11066, local KB).
  - Algorithm step 3 repeats LP-based OBBT whenever the upper bound improves.
  - Text (pp. 11057–11058): "The take home message is that OBBT should be
    repeated every time a better upper bound is found."
- **Justification of stopping rules.** Every rule found is a round cap, an
  absolute or `ℓ∞` improvement tolerance, "no change", or a volume factor of
  0.95. The only stated reasons are finiteness (Ryoo–Sahinidis 1996 Prop. 3;
  Zamora–Grossmann) and avoiding asymptotic convergence (Ryoo–Sahinidis 1995
  Remark 9; Misener–Floudas; Belotti et al. 2009). **No rule is derived from a
  convergence-rate model.** A rule based on the observed contraction ratio (the
  `theory.md` §5 proposal) was not found.

## 4. Empirical evidence on iterating (question 4)

- **Power systems.** These loops are feasibility-based with no objective
  cutoff, except GO-OBBT and the Alpine/Bynum variants.
  - **Coffrin, Hijazi, Van Hentenryck (CP 2015, preprint p. 10, Fig. 2).**
    - The algorithm is an exact loop, "repeat … until I_o = I_n", with
      tolerance `1e-3` (p. 12).
    - "the number of iterations in the fixpoint computation is small (often
      less than 10)" (p. 12).
    - QC-N brings 90% of the NESTA cases below a 1% gap.
    - Theory: the "largest minimal or bound-consistent network … exists and is
      unique by monotonicity" (p. 9). No finiteness or rate result.
  - **IEEE TPS 2017** (manuscript p. 7): "repeated until a fixed-point is
    reached … around 5–10" rounds.
  - **Sundar et al.** (arXiv 1809.04565, Alg. 1 pp. 12–13): fixed-point loop,
    in practice PowerModels' average-improvement tolerance of `1e-3`/`1e-4`.
    No per-round data.
  - **Gopinath et al.** (PSCC 2020, arXiv 1910.03716).
    - Usually one iteration.
    - case89_pegase_api: 11.70% to 0.93% in 3 iterations.
    - case118_ieee_api (PGLib): 8.44% to 0.99% in 5.
    - case118_ieee_api (NESTA): 17.50% to 1.91% in 12 iterations. This run
      stalled above target before the time limit, which suggests a fixed point
      with a remaining gap.
  - **Bynum et al.** (IEEE TPS 34 (2019), manuscript pp. 2–3).
    - Stopping rule: "optimality gap improved less than 0.1% in 20
      iterations".
    - 118_ieee_api QC^ro: 43.9% to 8.7% in 11 iterations.
    - The RM variants run 74–84 iterations.
    - 89_pegase_api stalls at 9.1% after 55 iterations.
  - **Bynum et al. PSE 2018** (p. 5): tightening spreads about one bus-hop per
    Jacobi round from the reference bus. This is the only mechanistic
    per-round evidence found; it suggests the number of rounds scales with
    graph distance.
  - **Kocuk et al.** (MPC 2018, p. 26): fixed at 5 rounds "after initial
    calibration".
- **Alpine** (JOGO 2019, Fig. 7a p. 21, visual reading). Plain OBBT roughly
  halves the total width in round 1 and plateaus by about round 10. Partitioned
  (MIP) OBBT keeps shrinking toward 0 over 20 rounds. This matches the stalling
  and exact-limit dichotomy.
- **Caprara–Locatelli–Monaci 2016** (Table 2 p. 528, see §1.2). Sweeps over all
  variables roughly halve the LMP root gap (8.4% to 4.0%). The node counts fall
  by orders of magnitude, but time is better only for the harder classes.
- **Ryoo–Sahinidis 1996** (Table III, pp. 122–123). On the Al-Khayyal–Falk
  example, "after three cycles through Steps 4 to 6" of reduction, infeasibility
  is detected and "the algorithm terminates at the root node with no branching
  required".
- **Zamora–Grossmann 1999** (Tables 2–3 pp. 233–235; Example 3 p. 237).
  - Repeated contraction proves global optimality at the root with no
    branching: 19 steps with S1, 13 with S2, 11 in Example 3.
  - The geometric gap decay is analysed in §2.
  - Example 5 (Table 8, p. 245): 11 nodes with contraction (S1, S3) against
    157 without (S5). Contraction subproblems take 76–79% of CPU time.
- **Faria and Bagajewicz** (Comput. Chem. Eng. 35 (2011) 446–455; Ind. Eng.
  Chem. Res. 50 (2011) 3738–3753; AIChE J. 58 (2012) 2320–2335). Full texts not
  accessible.
  - AIChE J. abstract: an "interval elimination procedure" contracts "a set of
    variables that are not necessarily the ones being partitioned"; "Once bound
    contraction is exhausted the method increases the number of intervals or
    resorts to a branch and bound strategy".
  - A 2025 follow-up (Water Sci. Technol. 92(12), §2.1) describes the loop as
    "repeated with new bounds until they can no longer be contracted", with a
    tolerance. No theory or per-round data were seen.
- **Castro 2023** (Table 1 p. 11057).
  - With the local-solver UB (20% suboptimal), MIP-based OBBT on A2q is stuck
    at a 3.50% gap.
  - With the optimal UB, the gap falls 3.48% → 1.17% → 0.043% → 0.0013% →
    0.0003% as the relaxation is refined (`PMB^1..4`), and 26 of 140 variables
    are essentially fixed.

  This is strong evidence that the cutoff slack `epsilon` controls the limit,
  consistent with the `sqrt(epsilon)` floor.
- **In-house probe** (`plan.md`, from `../scouting/brainstorm2-solvercore.md`).
  - On 140 MINLPLib instances: 31.6% mean root gap closed after 1 round versus
    42.8% after up to 6 rounds.
  - 2.9 times fewer nodes on 41 instances.
  - Caveat: these runs used the optimal value as the cutoff.

## 5. Implications for this project

- **Cite as prior theory.**
  - Caprara–Locatelli 2010: existence of the limit, ISDR = NRDR, order
    independence.
  - Caprara–Locatelli–Monaci 2016: exact limit `B_UB` for a two-variable class;
    stalling counterexamples.
  - Belotti et al. 2012: FBBT fixed points and geometric rates.
  - Ryoo–Sahinidis: marginals bound and the finite `δ`-loop.
  - Kannan–Barton 2017: `sqrt(epsilon/gamma)` radius.
- **Novelty.**
  - `theory.md` Lemma 1 is Caprara–Locatelli §7 in different notation.
  - Proposition 2 is an immediate consequence of Ryoo–Sahinidis Theorem 2 and
    should be stated as such.
  - Propositions 3 and 7, Theorems 4 and 6, and Proposition 8 appear new. For
    Theorem 6 and Proposition 8, the closest precedent is the CLM 2016 §3.1
    counterexamples, which concern concave objectives and a different
    mechanism.
- **Empirical sanity check.** Zamora–Grossmann Table 3 gives a published
  constrained instance with a constant per-step width ratio of about 0.571 and
  gap ratio of about 0.326. Reproducing it with the tangent map of `theory.md`
  would be a good check.
- **Stopping rule.** An adaptive rule based on the observed contraction ratio,
  and re-running OBBT on incumbent improvement, is supported by Castro's
  evidence and by the SCIP todo. Its only default implementation found is
  Coramin's re-run on new incumbents, which uses an absolute tolerance. A
  rate-justified rule appears unpublished.
