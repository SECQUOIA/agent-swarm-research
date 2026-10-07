# Referee report: split-robust lower bounds (`theory-robust-lb/robust-lower-bound.md`)

Date: 2026-09-30. Independent adversarial review; the reviewer did not write
the note. Scope: the five items of the review request plus significance.
Checks are in [`robust-lb-review-checks/`](robust-lb-review-checks/) (scripts
and `logs/`). Following `AGENTS.md`, only targeted checks were run; no
project-wide verification, and no CI status or logs were consulted.

## Verdict

The mathematics is correct. I found no false statement and no gap in
Lemmas 1.1–1.3, Propositions 2.1–2.4, Lemma 3.1, Propositions 3.2–3.3,
Lemma 4.1 or Theorems 4.2–4.3. The fixes below concern one mislabelled
numerical row, missing literature positioning, and several statements that
need to be sharpened.

- **Required fix (numerics).** The class-b6 chain counts in Section 6.4
  (`44`, `919` with 15 unresolved) were computed with a base split that
  differs from the one in Theorem 4.2/4.3(3). With the theorem's base split,
  the authors' own code and my independent code both give 2, 16 and 128
  leaves (0 unresolved). So the claim "b4 and b6 grow as fast as class (a)"
  is wrong for b6. The b6 growth is 2.0 per variable, not 2.75.
- **Required addition (positioning).** Lemma 1.2 is known in substance.
  With affine `S` it is the Falk/Dür–Horst/Nowak identity: the Lagrangian dual
  of a copy (variable-splitting) formulation equals the sum of block convex
  envelopes. With general `S` it is the continuous, restricted-class form of
  reparametrization or cost-transfer duality: Schlesinger/Werner, dual
  decomposition, and OSAC/VAC in weighted-CSP branch and bound, which chooses
  the best split at each node. The note cites none of this.
- **New quantitative facts from this review.**
  1. `gamma_10 = 0` at the reference parameters, so class b10 closes the
     gadget root gap.
  2. `gamma_d <= 2 E_d(L)` always, so class-(b_d) bases for this family are
     `1 + O(E_d)`.
  3. The tilted-volume method of Theorem 4.2 cannot give more than about
     1.063 per variable on this gadget, even with exact gadget bounds. The
     computed 1.0516 is already within about 1% of this ceiling.
- **Significance.** The result is a valid qualitative robustness statement:
  no split from a fixed finite-dimensional class, chosen per node and even
  with knowledge of `x*`, avoids exponential growth. The constants carry no
  practical weight: the analytic bound reaches 21 leaves at `n = 1000`. The
  family is a direct sum of 3-variable gadgets joined by links weaker than
  `1.4e-3`, so the mechanism is a product effect, not propagation along a
  path.

| Claim | Verdict | Verified here |
|---|---|---|
| Lemma 1.1 (splits on a path are univariate redistributions) | correct | by hand |
| Lemma 1.2 (moment form via Sion) | correct; known in substance (Section 7) | hypotheses checked by hand; zero duality gap observed numerically on every box (check 2/3) |
| Lemma 1.3 (runs give S-covers) | correct with a minor fix (F5) | by hand |
| Prop 2.1 (PROGRAM `c = 0` solved at root, balanced split) | correct (needs incumbent `<= eps`, F6) | proof + grid (check 5) |
| Prop 2.2 (convexifying weights near `x*`) | correct | by hand |
| Prop 2.3 (centred chords reduce to one chord) | correct; scope statement must be narrowed (F7) | proof + 4 random instances (check 5) |
| Prop 2.4 (edge-concave boxes exact) | correct | proof + 4 random instances (check 5) |
| Lemma 3.1 (gadget facts) | correct | proof + brute force, 4 parameter sets (check 1) |
| Prop 3.2 (five-point fooling, `gamma = y1^2(1-A)/A`) | correct, and optimal for (a)/(b2)/(b3) | closed form + independent LP (check 1, 2) |
| Prop 3.3 (band form; exact for large `d`) | correct; add `gamma_d <= 2E_d` and `gamma_10 = 0` (F3) | proof; `E_d` bracketed two-sidedly (check 5); `gamma_d` (check 2) |
| Lemma 4.1 (weak links keep a unique nondegenerate interior minimizer) | correct | proof + sampling (check 1) |
| Thm 4.2 (tilted volume) | correct | by hand |
| Thm 4.3(1) analytic `exp((gamma G - eps - delta(G-1))/Lambda)` | correct | constants recomputed (check 1) |
| Thm 4.3(2) computed `1.1628^G` | correct as a floating-point evaluation; no violation found | rerun + adversarial search (check 4, 4b) |
| Thm 4.3(3) class `b_d` | correct; state the base split explicitly (F2) | gaps (check 2) |
| Section 5 (Theorem 3.4 applies, `O(n log(n/eps))`) | correct; clarify the 20–22-leaf figure (F8) | hypotheses checked by hand; `c_g` by sampling |
| Section 6 counts | class (a) and b4 reproduced exactly; **b6 row mislabelled (F1)** | independent reimplementation (check 3, 3b) |

## 1. Formalization (Lemmas 1.1–1.3)

**Lemma 1.1: correct.** The induction is right: `D_1 + ... + D_{k-1}` is a
function of `x_k` alone because it equals `-sum_{e>=k} D_e`. The identity
is needed on the whole product box, and it is assumed there. The
polynomial-degree remark is also right: `r_{k+1}(t) = D_k(a_k, t) + r_k(a_k)`.

**Lemma 1.2: correct.** I checked each hypothesis.

- *Step 1.* For a continuous function on a rectangle,
  `vex_B phi(p) = min{∫ phi dnu : mean nu = p}`. The minimum is attained
  because the set of measures with mean `p` is weak*-compact and the
  integral is weak*-continuous.
- *Sion.* The set `M` of mean-consistent families is a closed subset of a
  finite product of weak*-compact sets `P(A_e)`, so it is compact, and it is
  convex. `L(., r)` is affine and weak*-continuous because `f_e` and `r_i`
  are continuous. `L(nu, .)` is linear on the linear space `S = prod S_i`
  and continuous for the sup norm. Sion needs only one compact side, and `M`
  is that side.
- *Attainment.* `sup_r L(nu, r)` is lower semicontinuous (a supremum of
  continuous functions), so it attains its minimum on `M`.
- *Measurability.* Only Borel probability measures on compact metric spaces
  and continuous integrands occur, so there is no measurability issue.
- *Step 3.* Correct because `S` contains the affine functions. A useful
  consequence, implicit in the note: the class bound equals
  `sup_r sum_e min_{A_e} f_e^r`. So envelopes add nothing to the best split
  plus the factor minima, and the theorem also covers solvers that use only
  constant (interval-type) factor bounds with optimized splits.
- *Per-factor envelopes.* The term is used correctly: each envelope is taken
  over the factor's own rectangle `A_e`. Relaxations that keep unary terms as
  separate factors are dominated, because a sum of envelopes is at most the
  envelope of the sum.

Numerically, my independent column generation (y-only reduction, exact
piecewise minimization) closed the primal–dual gap to `1e-12` on every one of
the roughly 400 distinct boxes it met (checks 2 and 3). This is consistent
with a zero duality gap.

**Lemma 1.3: correct, one minor fix (F5).** A frame piece `S_i^±` is closed.
Its face shared with `B_{k+1}` contains points that were *not* removed, so
"`F^r_{B_k}(z) > UBD - eps` for all `z` in the piece" is not literally true.
The fix: the convex envelope of a continuous function on a rectangle is
continuous, so `F^r_{B_k} >= UBD - eps` on the closed piece, and that is all
the conclusion `LB_S(Sp) >= f* - eps` needs. The same issue is implicit in
[C, Lemma 2.1].

## 2. Section 2

**Prop 2.1: correct.** It is trivial once stated: every balanced factor is
`>= (1 - kappa - |b|)|xy| >= 0`. Grid check: minimum `-1e-16` over
`kappa in {0, .1, .5, .9, 1}`, `|b| = 1 - kappa`. The control `kappa = 0.1`,
`b = 0.95` gives `-0.05`, as expected. Fix F6: "pruned for every `eps >= 0`"
needs an incumbent `UBD <= eps`, for example `f(0) = 0`. The consequence
matters for the program. The 2.3–2.5 growth of the decomposition review's
toy runs (`reviews/decomposition-review-checks/split_bb.py`, which uses
box-dependent per-factor alphaBB, confirmed) is an alphaBB artifact. So
SYNTHESIS.md Section 3 ("toy runs with the split factorization still grow
2.3–2.5 per variable") and face-exact Section 9.3 ("whether exact per-factor
envelopes with a split need exponentially many leaves is open") should be
updated for `c = 0`.

**Prop 2.2: correct.** One detail: in Lemma 9.1 the leftover `p_n e_n e_n'`
goes to the last block, which is consistent with `beta_n = D_n`.

**Prop 2.3: correct; narrow the scope statement (F7).**

- The Sion step is valid: `prod K_e` is compact and convex, and the
  objective is bilinear.
- The infimum over free `alpha_i` forces `s_{e-1,i} = s_{e,i}`.
- The sign choice realizing `-sum |b_e| w_e w_{e+1}` exists on a path.
- Numerically, `inf_r Gamma_r` equals the single chord of `f` to 5 digits in
  4 random instances, including instances with negative curvatures (check 5).

The note says that "the proofs of face-exact Theorems 1–2 ... cannot be made
split-robust". That is right for **Theorem 2** (per-factor envelopes) only.
**Theorem 1 (termwise McCormick) is already split-robust in its own class.**
Under any class-(a) split the bilinear term is still relaxed by McCormick
alone, and moved unary or quadratic pieces only add nonnegative secant or
underestimator gaps. So (M_b) holds for every split, and Theorem 1 applies
unchanged. The Summary bullet should say this. Otherwise readers of the
synthesis may think Theorem 1 is weakened.

**Prop 2.4: correct.** The vertex-polyhedral envelope, the fact that a
Bernoulli law is determined by its mean, and the Markov gluing are all
right. In 4 random edge-concave instances the grid-LP envelope bound equals
the minimum of `f` over the vertices (check 5).

## 3. The gadget (Section 3)

**Lemma 3.1: correct.** Every item was rederived by hand and checked by
brute force (check 1):

- `u` is continuous and `C^1` at `z1` (jump `1e-13`), and `u'(1) = b'`;
- partial minima `h1`, `h2` agree with a `1e-4` grid to `3e-10` and `2e-8`;
- the `K` formula holds exactly, and `max K = eps_v + eta(1-y1)^2`;
- Hessian determinant `2 y1^2 b'^2 eps_v/eta`, smallest eigenvalue `4.97e-3`;
- outside the slab the Hessian has a negative eigenvalue;
- on `2e6` samples, `min g/(x^2+z^2) = 2.8e-3 >= alpha = 7.2e-4`. The
  Section 5 constant `c_g = min(alpha, eps_v)/2 = 3.6e-4` is valid but
  conservative: the sampled ratio is `2.5e-3`.

**Prop 3.2: correct.**

- The closed form gives `gamma = 0.07611862`.
- My independent LP gives `[0.07611862, 0.07611862]` for b2 and b3, so the
  five-point fooling is optimal.
- The LP also finds an asymmetric 4-point fooling with the same value for
  b2. It agrees on `P_2` but not on `y^3`, which is harmless.
- The fixed balanced split gives `0.125507`, as in Table 6.3.
- Moments: `nu_1` and `nu_2` agree for `k <= 3` and differ at `k = 4`
  (`0.113` vs `0.337`).

**Prop 3.3: correct; add two facts (F3).**

- Item 1 and item 2 (Weierstrass argument) are correct.
- The grid values of `E_d(L)` are valid lower bounds. I bracketed them
  two-sidedly (grid LP lower bound; sup error of the LP polynomial on `2e6`
  points as upper bound): `E_2..E_12` equal the note's values to 5 digits.
- **Upper bound, missing from the note:** `gamma_d <= 2 E_d(L)`. Take `rho`
  a best approximation of `L`, and use `U >= L`. So `gamma_d` lies in
  `[2E_d - width, 2E_d]`. This two-sided form is more informative than
  item 1 alone. It shows that the class-(b_d) gaps of this family, and hence
  their bases, are `O(E_d) = O(1/d^2)` for every parameter choice.
- **`gamma_10 = 0` at the reference parameters** (independent LP, primal and
  dual both `0` to `1e-12`). Since the band is even, `gamma_9 = gamma_8`.
  So "exact for large `d`" means `d = 10` here, and class b10 solves the
  reference chain with `delta = 0` at the root. Sections 3.3, 3.4 and 8
  should say so.
- The band criterion of Section 3.4 is the two-clique, univariate-separator
  instance of the known sparse-decomposability criterion. See Section 7.

## 4. Chains and Theorem 4.3

**Lemma 4.1: correct.** `2 alpha = 1.444e-3`. The Hessian argument (a
nonnegative function with zero value and gradient at `0` has a PSD Hessian
there) is right. Treewidth 1 holds for `delta > 0`.

**Theorem 4.2: correct.**

- The product coupling of marginals on the connecting factor is consistent
  for *any* `S`, because the marginals are identical.
- `|E z E x| <= 1` gives the `delta(G-1)` term.
- The volume step is the standard tilted-volume argument.

One observation: for `delta = 0` the chain bound is *exactly* the sum of
gadget bounds. The shifts at `z_g` and `x_{g+1}` cannot help:
`min(A + r) + min(-r) <= min A`. My reimplementation uses this identity.

**Section 4.3(a) and Theorem 4.3(1): correct.**

- The images of the fooling measures under the affine maps stay inside `B`
  and agree on `P_3`.
- `|T_j t - t| <= 2(1 - rho_j)`.
- `Lambda_y` correctly adds both factors' `y`-Lipschitz constants.
- `|u'| <= b'`.
- `rho e^{a(1-rho)} <= 1` for `a <= 1`.
- Constants recomputed by grid: `Lambda = 8.356`, base `1.00915` per gadget,
  `1.00304` per variable.
- On 3,000 random boxes, `V_upper - Dhat_transport <= -0.085` (check 4).

**Section 4.3(b) and Theorem 4.3(2): correct as a floating-point
evaluation.**

- The case split into `Psi`, intermediate cores and the full cube is
  exhaustive.
- The slab-volume bound `(1 + theta_{i+1})/2` is right.
- The separable `Psi` bound has the right direction. The interval minima on
  fine points are upper bounds on the minima, which is the safe direction.
- Core gaps are valid foolings on grid points. My LP reproduces
  `gamma(theta)` at `theta = 0.46 ... 1` exactly.
- One wrong-direction approximation: `fmax`, the maximum over fine points,
  under-estimates the true maximum by about Lipschitz × `h/FINE`, around
  `1e-3` in the exponent. It enters only the "no grid point inside" terms,
  which are not binding. So this is cosmetic, but the note's "grid sandwich"
  wording overstates rigor.
- Rerun: `bound_eval.py 100` reproduces `mu = 2.224`, base `1.16278` per
  gadget, `1.05156` per variable (20 s).
- **Adversarial check (check 4).** A box with
  `(vol/8) exp(mu V(B)) > 0.86001` at `mu = 2.224` would refute the claim. I
  searched 3,000 random boxes plus hill climbing from structured and random
  starts, using certified lower bounds on `V`. The largest value found is
  `0.84427`, the full cube. So the true `Phi(2.224)` lies in
  `[0.8443, 0.8600]`, and the computed bound is tight to within 2%.

**New: a ceiling on the method (check 4b; F4).** Take exact gadget bounds
(`Dhat = V`).

- The full cube gives `Phi(mu) >= exp(-mu gamma)`.
- Corner boxes with `V > 0` take over sharply. At `mu = 2.4`, the box
  `[-1,-0.48] x [-1,-0.873] x [-1,-0.813]` gives `(vol/8) e^{mu V} = 1.037`.
  This value increases with `mu`, because `V > 0` on that box.
- Hence Theorem 4.2 cannot give more than `exp(2.4 gamma) = 1.2004` per
  gadget, i.e. **1.063 per variable**, whatever `Dhat` is used. At
  `mu = 2.3` the best found is `1.1913`.

The note's remark "a better reference measure *or exact gadget bounds on all
sub-boxes* might help" is therefore half wrong. Exact gadget bounds cannot
lift the base above 1.063 per variable. The gap to the observed 2.85 must be
closed by a different counting argument (non-uniform reference measure,
multiscale or tree-structured counting), not by better per-box estimates.

**Theorem 4.3(3): correct.**

- The optimal family exists by Lemma 1.2, and transport works for any
  measure.
- F2: Theorem 4.3 should restate the base split, for (b2) and (b3) as well
  as (b_d): "all unary terms in the gadget factors". The class depends on it
  when `u(z)` is not a polynomial.
- With `gamma_d <= 2E_d`, every base from this family is at most
  `exp(~2.4 · 2E_d(L))` per gadget, for example `<= 1.021` per variable at
  `d = 4` (`y1 = 0.3`). The note's 1.0158 is close to that.

**"Per node, with knowledge of `x*`": correct.** `LB_S` is a supremum over
the whole class, so no information helps.

## 5. Decomposition side (Section 5)

**Correct.** Checked:

- (QG) with `c_g = (1 - delta/(2alpha)) min(alpha, eps_v)/2`;
- (L^{1,1}) with `M_a` about 16.4 (factor-2 Hessian norm, `u'' <= b'^2/(2 eta)`);
- (U^q) with `alpha' = max(b'/2, delta/2)`. Factor 1 with `c y^2` is convex,
  factor 2 has minimum Hessian eigenvalue `>= -b'`, and alphaBB is a convex
  minorant, hence below the envelope.

Theorem 3.4 then gives `O(n log(n/eps))`.

Clarifications (F8):

- The "20–22 leaves per gadget" for `delta = 0` are **class-(a) per-node**
  counts, not fixed-natural-split counts. Under the fixed natural split,
  factor 2 (`u(z) + b' y z`, determinant `-b'^2`) is nonconvex at `x*`, so a
  per-gadget tree clusters at `x*`. Both are legitimate (the same class on
  both sides), but the text should say which.
- Rough crossovers with Theorem 3.4's constants: (T2) forces
  `theta = 2^-21` and `(4/theta)^2 ≈ 7e13`. The proved separation therefore
  starts near `n ≈ 850` with the computed base and `n ≈ 15,000` with the
  analytic base. With gadget bags at `delta = 0` (22 leaves per gadget) it
  starts near `n ≈ 140` and `n ≈ 3,300`. The note says only "at large `n`".
  Giving these orders of magnitude would be more honest.
- For `delta = 0` the problem is separable, and any solver with component
  detection (for example SCIP's components presolver) splits it. The weak
  links `delta > 0` exist to defeat that. Say so.

## 6. Numerics (Section 6)

**Independent reimplementation** (`gadget_indep.py`, no import of the
authors' code):

- The class bound is reduced to a pair of measures on `y` alone, using the
  closed-form partial minimizers `x*(y)` and `z*(y)`.
- Column generation gives a primal fooling (upper bound) and a dual split
  with exact piecewise-polynomial minimization (lower bound).
- The B&B uses the product identity for `delta = 0`, widest-side bisection
  with first-index ties, and midpoints.

| run | note | this review |
|---|---|---|
| class (a), `eps = 1e-2`, G = 1, 2, 3 | 10, 204, 3,952 | 10, 204, 3,952 |
| class (a), `eps = 1e-4`, G = 1, 2, 3 | 20, 600, 12,336 | 20, 600, 12,336 |
| class (a), `eps = 1e-6`, G = 1, 2, 3 | 22, 628, 12,696 | 22, 628, 12,696 |
| b4, `eps = 1e-4`, G = 1, 2, 3 | 10, 172, 2,592 | 10, 172, 2,592 |
| **b6, `eps = 1e-4`, G = 1, 2, 3** | **2, 44, 919 (15 unresolved)** | **2, 16, 128 (0 unresolved)** |
| root gaps env / b2 / b3 / b4 / b5 / b6 / b8 / b10 | 0.1255 / 0.07612 / 0.07612 / 0.00777 / 0.00777 / 0.00237 / 0.00078 / – | 0.125507 / 0.0761186 / 0.0761186 / 0.0077701 / 0.0077701 / 0.0023727 / 0.0007758 / **0** |

- **Decision margins.** At `eps = 1e-4` every pruned box clears `-eps` by at
  least `3.3e-5`, and every split box has a fooling at least `1.4e-5` below
  `-eps`. So the class-(a) counts are robust to rounding. This review
  independently confirms the `G = 3` counts, which the note lists as not
  re-verified.
- **F1 (required): the b6 discrepancy.** `robust_bb.bb` defaults to
  `base="balanced"`. For the chain this puts half of `u(z_g)` (and half of
  `y1^2 x_{g+1}^2`) into the connecting factor `(z_g, x_{g+1})`. For class
  (a) this is immaterial, because `u_i` is in `S_i`. For `b_d` it changes
  the class: `u(z_g)/2` cannot be moved back by polynomials. So it is not
  the class of Theorems 4.2/4.3(3).
  - Running the **authors' own** `bb` with the theorem's base split
    (`check3b_authors_base.py`, which monkeypatches `base_weights`) gives
    b6 = 2, 16, 128, matching my code. The b4 counts happen to coincide
    under both base splits.
  - Required changes:
    - relabel or replace the b6 row;
    - change "b4 and b6 grow as fast as class (a)" (b6 grows 2.0 per
      variable from G = 2 to 3, versus 2.74);
    - drop the Section 8 caveat about 15 unresolved boxes;
    - add a `base` option to `robust_bb.py`;
    - say which base split each table row uses.
- **F9 (wording).** Section 6.1 says every leaf is "certified in floating
  point". `verify_leaves.py` compares against a grid plus L-BFGS-B estimate,
  which is an upper estimate of each factor minimum. That is a consistency
  check, not a certificate. Use "checked".
- **PROGRAM rows.** These match `logs/bb_jobs1.log`. Not rerun (tangential;
  Prop 2.1 proves the `c = 0` row).

## 7. Significance and prior work

**Is the robustness result meaningful?**

It is meaningful as a qualitative separation, and weak as a quantitative
one.

- *For.* It answers the right question. Observation 4.2 shows that
  unrestricted splits kill every lower bound. The note shows that every
  fixed finite-dimensional split class leaves an additive, per-block gap
  that single-tree B&B pays for exponentially, even with per-node splits
  chosen with knowledge of `x*`. The "shape incompatibility" mechanism, and
  the band criterion that pins down exactly which univariate function a
  class must contain, are the most reusable parts.
- *Against.*
  1. The bases are tiny. The analytic bound gives 1.35 leaves at `n = 100`
     and 21 at `n = 1000`. The computed 1.0516 per variable needs `n ≈ 275`
     for `10^6`. The method itself cannot exceed about 1.063 per variable
     (Section 4).
  2. The family is a direct sum of gadgets with links below `1.4e-3`. The
     lower bound is a product effect that a solver with component detection
     avoids when `delta = 0`. The path structure is nominal.
  3. The classes are fragile. The gap disappears for:
     - b10 at the reference parameters;
     - any class that contains `h1(y)` (piecewise quadratic with kinks at
       `±y1`);
     - envelopes over the 3-variable gadget blocks, because `g >= 0`
       (listed by the note as not covered).

     For class (b_d), the base is `1 + O(1/d^2)` for this family whatever
     the parameters (`gamma_d <= 2E_d`).
  4. The synthesis's open question asks about "the best cheap per-factor
     relaxations". The note answers it for restricted split classes on a
     designed family, not for the PROGRAM family, where the answer is
     "solved at the root" (Prop 2.1).

**Is Lemma 1.2 of independent interest?** Modestly, as a clean interface.
Its substance is known, and the note should say so and cite it. Citations
below are from the reviewer's memory and should be checked at the
bibliographic level before use.

- *Affine `S`:*
  - Falk, SIAM J. Control 7 (1969);
  - Dür and Horst, JOTA 95 (1997);
  - Nowak, *Relaxation and Decomposition Methods for MINLP* (2005). The
    Lagrangian dual of block splitting with copy constraints equals the
    sum of block convex envelopes. Nowak is already in the program's
    literature audit.
- *General `S` (reparametrization or cost shifting):*
  - Schlesinger's equivalent transformations; Werner, IEEE TPAMI 29 (2007);
  - Wainwright, Jaakkola and Willsky, IEEE TIT 51 (2005);
  - Sontag, Globerson and Jaakkola, "Introduction to dual decomposition"
    (2011).

  The maximum over reparametrizations of the sum of factor minima is the
  dual of the local-consistency LP, which is exact on trees. Observation 4.2
  is the continuous tree case.
- *B&B with the best split per node:* Cooper, de Givry, Sánchez, Schiex,
  Zytnicki and Werner, "Soft arc consistency revisited", AIJ 174 (2010),
  OSAC/VAC in toulbar2; Ihler, Flerova, Dechter and Otten, UAI 2012
  (cost-shifting). These are the discrete ancestors of "`LB_S` with a
  per-node split". They answer the review request's question about prior
  work on "optimal splitting".
- *Consistency only on features:* expectation-consistent inference (Opper
  and Winther, JMLR 6 (2005)) and EP's weak consistency (Wainwright and
  Jordan, FnT ML 1 (2008), Section 4.3). There the factor beliefs agree only
  on expected sufficient statistics. `LB_S` is the zero-temperature analogue
  with statistics `S_i`.
- *Partial separability and optimal splitting:* Griewank and Toint (1984),
  already cited in the face-exact note.
- *Sparse moment, SA and RLT:*
  - Class (b_{2r}) dominates order-`r` sparse Lasserre with pair cliques (the
    note's remark is correct). It also dominates degree-`d` sparse RLT or
    Sherali–Adams with shared univariate monomials, since exact edge
    measures satisfy all their constraints.
  - The band criterion of Proposition 3.3 is the two-clique, degree-`d`
    instance of the sparse decomposability criterion: exactness if and only
    if `f - f*` splits into clique-wise nonnegative parts. See Grimm, Netzer
    and Schweighofer, Arch. Math. 89 (2007), and Nie, Qu, Tang and Zhang,
    arXiv 2406.06882 (the latter is in the program's audit).
- *Relation to the repository's sparse Putinar work.* The uniform-in-bags
  error of `research-20260928/solver/sparse-putinar-exact-consistency.md` is
  additive over bags (`sum_b C_b Gamma_{v_b}`). The gadget chain with
  `delta = 0` has a fixed-degree gap of exactly `G gamma_d`, so an additive
  per-bag error at fixed degree cannot be improved in form. This transfers to
  sparse Lasserre only for a polynomial version of the gadget, which the
  note leaves as a sketch.

**The product (tilted-volume) argument.** A direct-sum lower bound for
single-tree B&B is folklore in MIP; it motivates component branching. I
found no rigorous spatial-B&B statement of this form. Theorem 4.2's
formulation (each block may be loose if others are tight, traded off with
an exponential weight) is clean and seems worth keeping. This is based on
memory only; no literature search was run in this review.

## 8. Fixes

Required:

- **F1.** Section 6.4: the b6 row (and, for clarity, all `b_d` rows) must
  use the base split of Theorem 4.2, or be labelled "balanced base split, a
  different class". Correct values: b6 = 2, 16, 128. Revise the growth
  sentence and the Section 8 caveat, and add a `base` option to
  `robust_bb.py`.
- **F10.** Add a prior-work paragraph for Lemma 1.2, Observation 4.2 and the
  band criterion (Section 7 above). Present Lemma 1.2 as a restatement, not
  a new result.

Recommended:

- **F2.** Theorem 4.3: restate the base split for (b2), (b3) and (b_d).
- **F3.** Prop 3.3 and Sections 3.3, 3.4, 8: add `gamma_d <= 2E_d(L)` (so
  `gamma_d` lies in `[2E_d - width, 2E_d]`), `gamma_10 = 0` at the reference
  parameters, and `gamma_{2k+1} = gamma_{2k}` by evenness.
- **F4.** Section 4.4 "Where the constant is lost" and Section 8: exact
  gadget bounds cannot lift Theorem 4.2 above about 1.063 per variable for
  this gadget (full cube versus corner boxes at `mu ≈ 2.4`). Only a
  different counting argument can.
- **F5.** Lemma 1.3: closed frame pieces need `>=` via continuity of the
  envelope.
- **F6.** Prop 2.1: state the incumbent (`UBD <= eps`, for example
  `f(0) = 0`).
- **F7.** Prop 2.3 and the Summary: the impossibility concerns
  centred-chord proofs for per-factor envelopes (face-exact Theorem 2).
  Face-exact Theorem 1 (termwise McCormick) is invariant under class-(a)
  splits.
- **F8.** Section 5: say that the 20–22 leaves per gadget are class-(a)
  counts. Give the crossover orders (`n ≈ 850` and `15,000`, or `140` and
  `3,300` for gadget bags). Mention component detection for `delta = 0`.
- **F9.** Section 6.1: "certified" becomes "checked". Update Section 8: the
  `G = 3` class-(a) and b4 counts are now independently reproduced.
- **F11.** Section 1.3 "lifted view": Lemma 1.3's tightening-piece argument
  is stated for `F^r` only. To claim coverage of lifted relaxations with
  OBBT (for example sparse Lasserre), state the removal rule in terms of
  that relaxation. The same Jensen argument then applies.
- **Downstream.** SYNTHESIS.md Section 3 (the "toy runs still grow 2.3–2.5"
  sentence) and face-exact Section 9.3 (the open question for split
  envelopes) should cite Prop 2.1.

## 9. Checks run

All from `research-20260929/reviews/robust-lb-review-checks/` (reruns from
`theory-robust-lb/`), `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`, one core.
All are targeted; no project-wide checks, and no CI.

| command | purpose | result (log) |
|---|---|---|
| `python3 constants.py`, `band_check.py`, `band_Ed.py` (authors', in `theory-robust-lb/`) | rerun | identical to the note (`logs/rerun_*.log`) |
| `python3 bound_eval.py 100` (authors') | rerun Thm 4.3(2)–(3) | `mu = 2.224`, 1.16278 per gadget, 1.05156 per variable; b4 1.00362, b6 1.00145 (`logs/rerun_bound_eval.log`, 20 s) |
| `python3 check1_analytic.py` | Lemma 3.1, Prop 3.2, constants, 4 parameter sets | all identities hold; hypothesis-violating control gives no gap (`logs/check1_analytic.log`) |
| `python3 check2_rootgaps.py` | independent root and core gaps | table in Section 6; `gamma_10 = 0` (`logs/check2_rootgaps.log`) |
| `python3 check3_bb.py {2,4,6} eps G...` | independent B&B counts | Section 6 table (`logs/check3_bb.log`) |
| `python3 check3b_authors_base.py {b6,b4,a} G...` | authors' B&B with theorem base split | b6 2, 16, 128; b4 172; a 600 (`logs/check3b_authors_base.log`) |
| `python3 check4_phi_search.py` | adversarial search on `Phi(2.224)`; transport inequality | max 0.84427 < 0.86001; transport margin `<= -0.085` (`logs/check4_phi_search.log`) |
| `python3 check4b_ceiling.py` | ceiling of Theorem 4.2 with exact `V` | `<= 1.2004` per gadget, 1.063 per variable (`logs/check4b_ceiling.log`) |
| `python3 check5_props.py` | Props 2.1, 2.3, 2.4; `E_d` bracket | all consistent (`logs/check5_props.log`) |

A `__pycache__` directory created in `theory-robust-lb/` by the reruns was
removed. The note and the authors' files were not modified.
