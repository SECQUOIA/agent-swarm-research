# Cluster `limits`: structural limits — verification report

Date: 2026-10-03.

Outputs:

- `limits-proofs.tex`: a self-contained section, "Structural limits", with
  complete proofs. It compiles inside a wrapper that uses the main-text
  preamble; the only warnings are the expected undefined citations.
- `checks/`: exact-arithmetic scripts, listed in Section 6.

## 1. Verdict

**Sound, with fixes.** Every claim in this cluster was re-derived, and the
numbers were re-checked with exact rational arithmetic. No claim was found to
be false. The problems are scope, wording, and missing results:

- **Missing result.** The reports never prove that the dependence on κ is
  necessary. Del Pia–Khajavirad (DK) hardness cannot supply this, because
  their instances need not have a unique optimizer. I added a
  unique-optimum reduction (Proposition `lim:prop:unique`) and its
  corollary.
- **Scope of the message example.** The unit-box message obstruction is well
  conditioned only in ν/g. In terms of κ it has κ = 2^{2m+5}. Only the
  expanding-box companion has κ ≤ 80, so the paper must use the companion.
- **Unproved qualitative claims.** Several statements had no theorem behind
  them: "product domains do work", "set growth does not localize", and
  "local corrections fail" in general. Each now has a short proposition
  with a proof.
- **Improvements.** Several results were strengthened (Section 4).

## 2. What was verified

### (a) Conditional-moment witness

`check_conditional_moment.py`, Part A, is an independent re-derivation using
sympy and Fraction. Every number checks:

- **Expansion identity.**
  `F_h − 1/4 = 16δ² + 2[(1−v)u₁u₂ + v(1−u₁)(1−u₂)] + (u₁+u₂+v)/16`
  holds as a polynomial identity.
- **Optimum.** The minimizer `(h/8,0,0,0)` is unique, with value 1/4.
- **Growth.** g = 1/22 is valid. The proof uses
  `‖x−x*‖² ≤ 2δ² + (11/8)‖w‖²`, which needs h ≤ 1, and `Σw ≥ ‖w‖²`.
  Since 22/16 = 11/8, the constant is exact for this argument.
- **Hessian.** `H + 2I = 16r₁r₁ᵀ + 16r₂r₂ᵀ + 2e_se_sᵀ`, and
  `H(0,1,−1,0) = −2(0,1,−1,0)`. So ν = 2 exactly, and L = H_ss = 32/h².
- **Separator moments.** Both bags give 1/2, 5/16, 7/32 for orders one to
  three. The fourth moments differ: 11/64 versus 41/256.
- **Relaxation gap.** The relaxed value is 3/32, so the gap is 5/32.
- **PSD completion.** `Σ = aaᵀ/16 + 3bbᵀ/16` restricts exactly to both bag
  moment matrices. Both residual squares have zero pseudo-expectation.
  E[u₁v] = E[u₂v] = 3/8.
- **McCormick.** All global McCormick inequalities hold with s ∈ [0,2h].
- **Violated inequality.** The witness violates
  `u₁u₂ + v − u₁v − u₂v ≥ 0` with pseudo-expectation −1/8. This is
  Padberg's triangle inequality, and it couples variables on both sides of
  the separator.

What the witness refutes: any bound
`OPT − R ≤ C(p, ν̄/g)·ν̄·Σ w_i²` for the cell-conditioned local moment
relaxation. This relaxation has exact bag measures and separator moments
matched through order 3, even with a global PSD completion and McCormick
added. On this family p = 3 and ν/g ≤ 44 are fixed while the occupied
widths tend to zero. It is not a lower bound for adaptive filtering, and it
does not touch error bounds in terms of L (the gap 5/32 is far below
L·Σw²/8 = 64).

**Wording fix (minor).** The text says "g = 1/22 … so ν/g = 44". It should
say that g = 1/22 is a *valid* constant, so ν/g ≤ 44.

### (b) DK width-two reduction

The construction was checked against the PDF, Theorem 3, equations (20)–(24).
`check_dk_conditioning.py` assembles the dense Hessian independently by
expanding every square. It covers 50 instances (dense for B ≤ 4096, residual
form up to B = 2⁶⁴+5) and 150 weight cases, and confirms:

- **Exact curvature.** The maximum diagonal is exactly 10 (attained by the
  z and w variables), so L = 10.
- **Unique zero.** The only binary solution is (1,0), so v* is the unique
  zero.
- **Binary witness (0,1).** Ψ = D⁻² and ‖y′−v*‖² ≥ 2ℓ. Hence
  **κ ≥ 20ℓD² ≥ 80ℓB²**, which is exponential in N = 5m+7 for B = 2^m.
- **Fractional witness (1/B, 1).** Ψ = cq/B and dᵀHd = −2c(q²+1).
  Hence **ν/g ≥ 2B(q+1/q) ≥ 4B**, for any square weights and endpoint
  weight c.

Implications for the core theorem:

1. **Consistency.** On these instances the bound f(3,κ)·poly(I) ≥ κ^{3/2}
   is exponential, so strong NP-hardness is not contradicted. DK's forest
   algorithm needs no growth assumption, so the two results are
   complementary, as main.tex already says.
2. **DK alone does not show that κ is needed.** The theorem assumes a
   unique optimizer, and DK instances (NO instances, or YES instances with
   several solutions) generally lack one. The new Proposition
   `lim:prop:unique` gives a deterministic reduction in which **every**
   image has a unique minimizer and κ ≤ 2^{n+3}n²(1+2nM). It refines DK's
   Remark 2, a weak NP-hardness reduction with bags {s_{i−1}, s_i, x_i},
   in three ways: a stronger concave penalty makes Φ concave, a
   lexicographic linear term makes the minimizer unique, and the growth
   constant is computed explicitly.
   - **Corollary.** Unless P = NP, no algorithm runs in poly(I+q+log κ) at
     p = 3. So f(3,κ) cannot be polylogarithmic in κ.
   - **Complexity boundary.** f is polynomial in κ for fixed p. So at fixed
     p the boundary lies between κ ≤ I^{O(1)} (polynomial, by
     Theorem `thm:exact`) and κ ≤ 2^{O(I)} (NP-hard).
3. **ν/g is not refuted either.** Because ν/g ≥ 4B, DK does not refute a
   future ν/g-parameterized algorithm.

### (c) Exponential complete messages

The proof was re-derived line by line.

**Unit-box version.** g = 1/8 and ν ≤ 1/4 are correct. However the maximum
diagonal is 4^{m+1}, so **κ = 2^{2m+5}**. This version is "well
conditioned" only in ν/g ≤ 2.

**Expanding-box companion** (S_t ∈ [0, 2^t−1]):

- g = 1/8 and L = 10 (the S_m diagonal is 4, the z diagonals 7/4), so
  **κ ≤ 80**.
- There are exactly 2^m zeros of μ(v) − v², so at least 2^{m−1}
  pieces are needed, also for min-of-quadratics (lower-envelope)
  representations.
- I = O(m²).

`check_misc_limits.py` checks m = 2..7: growth at random points, the
diagonals, H + P_z/4 ⪰ 0, the integer zero set, and the negative
directions.

**Decision: include the companion in the main text as the motivation for
grids** (Proposition `lim:prop:messages`), where outline-v0 already places
it. The contrast is sharp:

- forests: linearly many pieces (DK);
- width 3 with κ ≤ 80: exponentially many pieces;
- corrected grids: poly(m+q).

Related work to cite: Murty (1980), exponential parametric LP complexity;
Bhathena et al. (2026), margin-based pruning of exponentially many
quadratic pieces.

### (d) The assembled section

`limits-proofs.tex` contains:

| Failure mode | Result | Status |
|---|---|---|
| no quantitative growth / conditioning | Prop. `lim:prop:unique` + Cor. `lim:cor:nopolylog` | complete proof (new) |
| fine-grained form | Rem. `lim:rem:eth` (κ^δ necessary under ETH) | conditional on cited result |
| DK reduction | Rem. `lim:rem:dk` (κ ≥ 20ℓD², ν/g ≥ 4B) | complete argument |
| exponent of κ | Prop. `lim:prop:oracle` ((κ/8p)^{p/2} − 1 evaluations) | complete proof |
| dependence on p, white box | Rem. `lim:rem:oracle` (Max-Cut at κ = 1) | complete short argument |
| exact messages | Prop. `lim:prop:messages` | complete proof |
| set growth instead of point growth | Prop. `lim:prop:setgrowth` | complete proof (new) |
| no product domain | Prop. `lim:prop:constraints` (NP-hard at p = 3, κ = 1) | complete proof |
| local corrections | Prop. `lim:prop:star` (any e(\|B\|,L,h) fails) | complete proof |
| local moments | Lemma `lim:lem:mixture`, Def. `lim:def:moments`, Prop. `lim:prop:moments` (every finite order fails), Rem. `lim:rem:moments` | complete proofs (new) |

### Other source claims re-checked (all correct)

- **(convexenergy).** F − OPT ≥ g/(2(g+ν))·dᵀ(H+2νI)d.
- **Convex-recourse envelope.** E_λ − λ‖c‖²/2 is concave, and the growth
  constant gλ/(2g+λ) is correct, giving ratio 2 + λ/g.
- **Star example.** The values 0, 23/32 and 31/16 are correct, as are
  V_h − V = m·dist(x/4,G)² and the cell rejection.
- **Conditional-recourse interface.** The inequalities U ≤ OPT + e + η and
  "retained ⇒ W_B(v) ≤ OPT + 2(e+η)" are correct. Retention of the
  optimizer's cell also holds.
- **x³ − 6x on [1,2].** Optimizer √2, value −4√2 (−5.657 < −5 = f(1)).
- **x⁴.** Unique optimizer without quadratic growth.
- **DK citations in main.tex Section 1.** O(n²) forests,
  ‖Q‖max ≤ 5 and ‖c‖∞ ≤ 4 at treewidth two, quartic paths strongly
  NP-hard: all match the source.
- **Qualitative growth lemma.** Re-derived; correct.

## 3. Issues

| # | Severity | Location | Issue | Fix |
|---|---|---|---|---|
| 1 | major | main.tex §1; structural-limits story | DK hardness does not show that κ must enter: DK instances need not have a unique optimizer, which the theorem requires. No reduction with a unique optimizer exists in the report. | Add Prop. `lim:prop:unique` + Cor. `lim:cor:nopolylog` and the boundary paragraph. Proofs complete; checked on 9,550 instances and 27,300 growth points. |
| 2 | major (if misused) | message obstruction note; any "well-conditioned" citation | The unit-box family has κ = 2^{2m+5}; it is well conditioned only in ν/g. | Use the expanding-box companion (κ ≤ 80) in the paper, as Prop. `lim:prop:messages` does. |
| 3 | minor | extensions.tex, conditional-moment paragraph | "growth g = 1/22 … ν/g = 44": g = 1/22 is only a valid constant. | Write "valid growth constant 1/22, hence ν/g ≤ 44". |
| 4 | minor | extensions.tex, same paragraph | "not a lower bound against … all moment hierarchies; matching the fourth moment excludes this witness" is now superseded. | Replace with Prop. `lim:prop:moments`: every finite order k fails at p = 3. Keep the 4-variable instance as a remark. |
| 5 | minor | extensions.tex, "Coupled constraints" | "The product-domain hypothesis does mathematical work" has no theorem. | Prop. `lim:prop:constraints`. The constraint-barrier note supplied L = 1 and L/c = 2n+3; since F is affine, every L > 0 is valid, so κ = 1. |
| 6 | minor | extensions.tex, nonunique optima | "set growth need not localize" is stated without proof. | Prop. `lim:prop:setgrowth`: for Σ(x_i − x_{i+1})², every corrected-grid certificate of accuracy ε needs ≥ 1 + 1/(2√ε) nodes per coordinate. |
| 7 | minor | extensions.tex, "global grid correction" | Refutes only e = \|B\|Lh²/8 at m = 32. | Prop. `lim:prop:star`: for every e and every m > max(16, 32e+8+16ε), any correction depending only on (\|B\|, L, h) fails. |
| 8 | minor | geometric-dp oracle-limits note | The smooth-bump construction has constant 192 and needs derivative bounds. | A simpler min{gp, L‖x−c‖²/2} family suffices for the semiconcavity hypothesis and gives (κ/(8p))^{p/2} − 1. Keep the smooth bump only if derivative oracles are wanted. |
| 9 | minor | Rem. `lim:rem:eth` | It relies on the ETH lower bound for Subset Sum holding on instances whose numbers have O(n) bits. Jansen–Land–Land was checked only through publisher and repository abstracts (statement: no 2^{o(n)}‖I‖^{O(1)} algorithm). The bit-length form follows from the textbook 3-SAT reduction with sparsification, but it was not checked against the paper. | Check JLL16 / IPZ01 before submission, or keep it as a remark. |
| 10 | minor | bit-serial note | It says the square weights cannot repair the family. That is true for ν/g. For κ = L/g, larger square weights increase L, which only strengthens the bound. | Clarify the wording. |

No critical issue was found.

## 4. Developments on the open questions

**(a) Every finite moment order fails — resolved.** Previously it was open
whether higher-order separator moments defeat the obstruction. New
Proposition `lim:prop:moments` (complete proof): for every r ≥ 1 there is a
family with bag size 3, a unique minimizer, OPT = 1/4, ν ≤ 2 and a valid
growth constant g_r = 1/(8r(1+8(2r−1)²)), independent of h. The order
(2r−1) local moment relaxation has a gap of at least (2r+1)/(16r) ≥ 1/8,
while all occupied widths are O(h).

Mechanism:

- **Parity.** The left chain realizes 2s/h ~ Bin(2r,½) conditioned on even
  values, and the right chain conditioned on odd values. The finite
  difference Σ(−1)^k C(2r,k)k^j = 0 for j < 2r matches all moments below
  order 2r.
- **Reduction.** Eliminating the chains leaves
  `Ψ − 1/4 = 2Π + τ(U+V)` with `Π = e₂(u) + e₂(v) − UV + V`, which is
  multilinear and equals (a−b)(a−b−1)/2 ≥ 0 at vertices.
- **Smallest case.** The original 4-variable example is the r = 2 case
  without chains (same gap 5/32, same τ = 1/16).
- **Contrast.** Exact separator laws give no gap at all (gluing argument in
  the remark), so the obstruction is specific to finite orders.

Checked exactly for r = 1..4: the symbolic reduction identity, vertex values
of Π, moments, gap, growth at random points, and the PSD part of the
Hessian.

**(b)/(e) Necessity of κ — resolved in the P ≠ NP form.** No
poly(I+q+log κ) algorithm exists at p = 3, by Proposition `lim:prop:unique`.
The ETH form (no κ^δ·I^C algorithm for some δ > 0) holds conditionally on
the cited fine-grained result.

**(e) Optimality of κ^{p/2} — resolved in the value-oracle model.**
Proposition `lim:prop:oracle`: (κ/(8p))^{p/2} − 1 evaluations are necessary
for error below Lp/κ, deterministic or randomized (success probability at
most (Q+1)(8p/κ)^{p/2}). The capped algorithm uses (C√κ·log(p+2))^p per
stage. The exponent p/2 is therefore optimal; the remaining gap is
(C√p·log p)^p times the number of stages.

In the white-box model, Max-Cut with a tie-breaking term gives NP-hardness
at κ = 1 when p is unbounded. So the dependence on p cannot be polynomial
unless P = NP (classical).

**White-box κ^{Ω(p)} lower bound — not resolved.** I sketched a route
without completing it:

- reduce from k-Clique (no f(k)N^{o(k)} algorithm under ETH);
- k integer choice variables in a core bag;
- lookup gadgets for adjacency, as one-hot or thermometer chains of width
  O(1) hanging off the core, giving p = k + O(1);
- randomized isolation (Mulmuley–Vazirani–Vazirani) to obtain a unique
  optimizer with polynomial weights.

The obstacles:

- Deterministic tie-breaking among N^k cliques forces κ ≥ N^{Ω(k)}, which
  destroys the bound.
- Randomized isolation would give the result only under randomized ETH.
- The growth constant of the mixed integer/continuous gadget chains must be
  shown to be at least 1/poly(N).

This is reported as open.

**ν/g-parameterized algorithm — still open; sharpened.** Neither the DK
reduction (ν/g ≥ 4B) nor any finite-order local-moment relaxation can settle
it in either direction. The new Proposition `lim:prop:moments` shows that a
proof must use information beyond finite-order separator moments, for
example:

- full separator laws;
- inequalities that couple both sides of a separator, such as Π ≥ 0 or
  Padberg triangles;
- selective refinement.

**Set growth — partly resolved (negative).** Corrected-grid certificates
cannot achieve poly(log 1/ε) size under set growth when the projections of
the optimal set are continua (Proposition `lim:prop:setgrowth`). Whether
non-grid certificates (for example, Bellman-residual identities) can give
f(p, L/g_set)·poly(I) remains open.

## 5. Classical versus new, and placement

| Result | Classical / closest prior work | New here | Recommendation |
|---|---|---|---|
| Prop. `lim:prop:unique` + Cor. | DK Remark 2 (weak NP-hardness, bags {s_{i−1},s_i,x_i}); Subset Sum (Karp; Garey–Johnson); tie-breaking is folklore | uniqueness for all images, explicit g and κ ≤ 2^{O(I)}, consequence for κ | **main** |
| Complexity boundary paragraph | — | κ ≤ I^{O(1)} in P vs κ ≤ 2^{O(I)} NP-hard at fixed p | **main** |
| Rem. ETH | IPZ01 sparsification; JLL16 Subset Sum ETH bound | transfer to κ^δ | **remark** |
| Rem. DK conditioning | DK Theorem 3 | κ ≥ 20ℓD², ν/g ≥ 4B on a unique-optimum subfamily | **remark** |
| Prop. oracle | hidden-needle argument (Nemirovski–Yudin 1983) | constants (κ/8p)^{p/2} under semiconcavity and growth; matches the algorithm's exponent | **main** (short), or appendix |
| Rem. Max-Cut width | classical | κ = 1 framing | **remark** |
| Prop. messages | Murty 1980 (exponential parametric LP); DK forests (linear arcs); Bhathena et al. 2026 (margin pruning) | width 3, κ ≤ 80, unique optimizer, ≥ 2^{m−1} pieces | **main** (motivation for grids) |
| Prop. set growth | — | elementary, new | **main** (short, nonunique section) or remark |
| Prop. constraints | running-sum Subset Sum encodings (DK Remark 2; Cifuentes–Parrilo) | NP-hard at p = 3, κ = 1 with a unique optimizer | **main** (short) |
| Prop. star | — | elementary; any local e fails | **main** (motivates the conditional-recourse interface) |
| Lemma mixture + Def. + Prop. moments | truncated moment vs measure; PSD completion (Grone et al. 1984); sparse Lasserre hierarchy (Lasserre 2006; Waki et al. 2006 — not checked); Padberg 1989 triangles | parity family defeating every finite order at p = 3 | **appendix**, with a one-paragraph summary in the main limits section |
| 4-variable instance | — | smallest witness; global PSD completion; violated triangle inequality | **appendix** (inside the moments remark) |
| Horn / preordering obstruction (box-preordering note) | Horn matrix copositive but not SPN (Hall–Newman, Diananda); Pólya | κ = 12 instance with no preordering certificate | **drop**; at most a one-sentence remark. Numbers re-checked: minors, ⟨Q,W⟩ = −1/4, diagonal 12/5. |
| Constraint slope obstruction (constraint-obstruction note) | — | concerns a different, abandoned algorithm | **drop** |

## 6. Checks run (all exact; targeted; no project-wide verification, no CI)

From `/workspace/minlp-notes/paper-decomposition-aware/process/w1/checks/`:

| Command | Result |
|---|---|
| `python3 check_conditional_moment.py` | ALL PASSED. Part A: identity, Hessian, moments, PSD completion, McCormick, triangle inequality, 1,200 growth points. Part B (r = 1..4): reduction identity, Π vertex values, moments to order 2r−1, gaps 3/16, 5/32, 7/48, 9/64, growth points, Hessian PSD part. |
| `python3 check_dk_conditioning.py` | PASS: 50 instances, 150 weight cases; max diagonal 10; κ ≥ 20ℓD²; ν/g ≥ 4B. |
| `python3 check_unique_hardness.py` | PASS: symbolic identity for n = 2..4; 9,550 Subset Sum instances; 27,300 growth points. |
| `python3 check_misc_limits.py` | ALL PASSED: star values; set growth on 300 random grids; messages m = 2..7; 1,274 constrained instances; oracle packing and growth. |
| `python3 check_horn_remark.py` | PASS. |

These finite checks support the proofs; they do not replace them. The
LaTeX fragment was compiled once in a temporary wrapper under `/tmp`, which
is outside the repository.

## 7. Bibliography entries needed (beyond references.bib)

- **GareyJohnson1979.** M. R. Garey, D. S. Johnson, *Computers and
  Intractability*, Freeman, 1979. Standard; not checked locally.
- **ImpagliazzoPaturiZane2001.** R. Impagliazzo, R. Paturi, F. Zane,
  "Which problems have strongly exponential complexity?", *J. Comput.
  System Sci.* 63(4):512–530, 2001. Not checked locally.
- **JansenLandLand2016.** K. Jansen, F. Land, K. Land, "Bounding the
  running time of algorithms for scheduling and packing problems",
  *SIAM J. Discrete Math.* 30(1):343–366, 2016,
  doi:10.1137/140952636. Bibliographic data checked through web listings;
  theorem content checked only through the abstract.
- **NemirovskiYudin1983.** A. S. Nemirovsky, D. B. Yudin, *Problem
  Complexity and Method Efficiency in Optimization*, Wiley, 1983. Not
  checked locally.
- **Padberg1989.** M. Padberg, "The Boolean quadric polytope: some
  characteristics, facets and relatives", *Math. Program.* 45:139–172,
  1989. In the local knowledge base.
- **Optional, for related work.**
  - Murty 1980, *Math. Program.* 19:213–219. In the local knowledge base.
  - Lasserre 2006, *SIAM J. Optim.* 17(3):822–843. Not checked.
  - Grone, Johnson, Sá, Wolkowicz 1984, *Linear Algebra Appl.*
    58:109–124. Not checked.
