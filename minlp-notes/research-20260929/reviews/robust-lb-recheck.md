# Recheck of the revised note "Split-robust lower bounds for single-tree spatial branch-and-bound on paths"

Date: 2026-09-30. Note: `research-20260929/theory-robust-lb/robust-lower-bound.md`
(revised version, 1222 lines; changes listed in its Section 10). First review:
`reviews/robust-lb-review.md`. I did not write the note or the first review.
Scripts and logs are in `reviews/robust-lb-recheck-checks/`. Following
`AGENTS.md`, I ran only targeted checks: no project-wide verification and no
CI. I did not commit anything or edit the note. No earlier copy of the note
exists (the folder is untracked), so I judged each revised statement against
the evidence, not against a diff.

## Verdict in brief

I found no mathematical error in the revision. Every revised proof step I
checked is correct, and every new number I recomputed agrees with the note.
The remaining fixes are small: one wrong citation remark, and four places where
the wording claims slightly more than the evidence shows.

| Item | Verdict |
|---|---|
| 1. Lemma 1.3 via upper semicontinuity; lifted-relaxation paragraph | **correct**; two small precision fixes (R3, R4) |
| 2. `gamma_d <= 2 E_d(L)` and `gamma_{2k+1} = gamma_{2k}` | **correct**; both proofs checked; numbers agree to 8 digits |
| 3. `gamma_10 = 0` at the reference parameters | **confirmed, now exactly**: rational certificate verified by exact root counting |
| 4. b6 rerun: 2, 16, 128 leaves with the theorem's base split | **confirmed** by my own code (G = 1, 2, 3) and by rerunning the authors' code (G = 1, 2; balanced G = 2 gives the old 44) |
| 5. The 1.063 ceiling | **correct at the reference parameters**; the corner-box value holds for every class. "On this family" is too broad (R2). |
| 6. Crossovers ~850 / ~15,000 and ~140 / ~3,300 | **correct**: 850, 15,044, 138, 3,327 |
| 7. Section 1.5 citations | **all exist and say what is claimed**; the Cooper et al. quote is verbatim. The Falk (1974) *Oper. Res.* citation is right. **But the Falk 1969 paper does exist** (R1). |
| 8. Nothing silently strengthened | **no strengthening in the mathematics**; four wording overstatements (R2, R5, R6, R7) |

Main evidence:

- **`gamma_10 = 0`.** An even degree-10 polynomial `rho = y^2 q(y)` with
  rational coefficients satisfies `L <= rho <= U` on `[-1,1]`. Sturm root
  counting in exact arithmetic finds no root of any of the four defining
  polynomials on its closed interval. The minimum slack is `4.6e-4`. So
  `gamma_10 = 0` exactly, not only to `1.7e-11`.
- **Leaf counts.** My B&B, which shares no code with the authors' or the first
  review's, gives the following at `eps = 1e-4`:
  - b6: 2, 16, 128;
  - b4: 10, 172, 2,592;
  - class (a): 20, 600, 12,336.

  There are no ambiguous boxes. Decision margins are at least `1.4e-5`, and
  bound brackets are at most `2.5e-6` wide.
- **`gamma_d` table.** A primal moment LP, written from scratch, gives
  `gamma_2..gamma_9` equal to the note's values to 8 digits. The same holds
  for `E_2..E_12`. `gamma_d <= 2 E_d` holds with margin at least `1.8e-3`,
  and odd degrees add nothing.

## 1. Lemma 1.3 (revised proof) and the lifted-relaxation paragraph

**Upper semicontinuity.** The argument is correct.

- `F^r_{B_k}` is a sum of convex envelopes of continuous functions over
  compact rectangles. So it is convex and finite on the box `B_k`: each
  envelope lies between the factor minimum and the factor.
- Rockafellar, *Convex Analysis*, Theorem 10.2 states that a convex function
  is upper semicontinuous relative to any locally simplicial subset of its
  domain. A box is a polytope, hence locally simplicial. The attribution to
  Gale, Klee and Rockafellar is right: "Convex functions on convex polytopes",
  Proc. AMS 19 (1968) 867–873 (checked on Crossref).
- Upper semicontinuity is the right direction. If `z_n -> z` with
  `F(z_n) > UBD - eps`, then `F(z) >= limsup F(z_n) >= UBD - eps`.
- I checked the density claim against the frame pieces of [C, Section 2]:
  `S_i^- = prod_{j<i} [l'_j,u'_j] x [l_i,l'_i] x prod_{j>i} [l_j,u_j]`.
  - Every point of a piece that lies outside `B_{k+1}` was removed.
  - The points inside `B_{k+1}` lie on the face `y_i = l'_i`.
  - For a nondegenerate piece (`l_i < l'_i`), the removed points are
    therefore dense.
- The Jensen step is unchanged and correct. The means of an S-consistent
  family agree because `S` contains the affine functions, the common mean
  lies in the box `Sp`, and `vex_{(B_k)_e} f^r_e` is convex on a set that
  contains the support.
- The review's alternative fix (continuity of the envelope) would also work.
  Upper semicontinuity needs less.

**R3 (small).** The statement of Lemma 1.3 lets a round remove points with
`F^r_{B_k}(y) > UBD - eps` "for some `r in S`". The proof fixes one `r` per
round. If different points may use different `r`, the proof still works after
one change: apply the same theorem to `sup_{r in S} F^r_{B_k}`. This function
is convex, and it is finite because `F^r_{B_k} <= f` for every `r`. For the
Jensen step, take an `r` that comes within `eta` of the supremum at `z`, and
let `eta -> 0`. Add one sentence, or state in the lemma that each round uses
one `r`.

**Lifted-relaxation paragraph: correct, with one precision fix (R4).**

- The projected value `phi_{B_k}(y)` is convex.
- An S-consistent family on the factor boxes of `Sp` gives a lifted point that
  is feasible for the `B_k` relaxation at `x = z`. This holds because the edge
  sets contain moment vectors of measures on `(B_k)_e`, and the shared lifts
  lie in `S`. Its objective is `sum_e ∫ f_e dnu_e`.
- Leaves are covered because the lifted bound is at most `LB_S`.
- **R4.** "If the relaxation is feasible at every point of `B_k`, it is
  finite" also needs `phi_{B_k} > -inf`. For example, require the lifted edge
  sets to be bounded, as they are for McCormick, RLT or moment relaxations on
  a box. The edge case cannot create a wrong piece: an improper convex
  function is `-inf` on the relative interior of its domain, so nothing
  interior is removed. It is still cleaner to say "feasible and bounded
  below".

## 2. `gamma_d <= 2 E_d(L)` and `gamma_{2k+1} = gamma_{2k}` (Proposition 3.3(3))

Both proofs are correct.

- **Upper bound.** Take `rho` a best approximation of `L`. Then
  `max(L - rho) <= E_d`, and `max(rho - U) <= max(rho - L) <= E_d` because
  `U >= L`.
- **Evenness.** `L` and `U` are even. `y -> -y` maps `rho` to `rho(-y)`
  without changing either maximum. By convexity of `max`, the even part does
  not increase either maximum. Even polynomials of degree `<= 2k+1` are those
  of degree `<= 2k`.
- **Sign convention.** Lemma 1.2 shifts `+rho` into factor 1 and `-rho` into
  factor 2. With `min_x g_1 = -L` and `c y^2 + min_z g_2 = U`, this gives
  `LB = sup_rho [min(rho - L) + min(U - rho)]`, as the note states.
  `gamma_d >= 0` because `L(0) = U(0)`.
- **`O(1/d^2)` uniformly in `y1`.** The claim that the gap bound "depends
  only on `y1` and is `O(1/d^2)`" is right. It is even uniform in `y1`,
  because `L'` is 2-Lipschitz for every `y1` (Jackson's theorem).

Numbers (`check_gamma.py`, `logs/check_gamma.log`). A primal moment LP on a
grid, refined by an exchange step, gives lower bounds on `gamma_d`. Exact
piecewise evaluation of the dual shift gives upper bounds. `E_d(L)` is
bracketed the same way.

| d | `gamma_d` bracket | `E_d(L)` bracket | note |
|---|---|---|---|
| 2, 3 | 0.07611862 (both ends) | 0.04508395 | 0.07612; `E_2 >= 0.0451` |
| 4, 5 | 0.00777012 | 0.0100901 | 0.00777; `E_4 >= 0.0101` |
| 6, 7 | 0.00237272 | 0.00263494 | 0.00237; `E_6 >= 0.00263` |
| 8, 9 | 0.00077575 | 0.0025362 | 0.00078; `E_8 >= 0.00254` |
| 10 | `[0, 0]`; exactly 0 by the certificate below | 0.00171649 | 0; `E_10 >= 0.00172` |
| 12 | `<= 1.5e-6` numerically; 0 because `gamma_10 = 0` | 0.00091098 | `E_12 >= 0.00091` |

A brute-force check of the partial minima (Lemma 3.1) agrees to `2e-8`.
`max(U - L) = 0.039220 = eps_v + eta (1-y1)^2`. The statement
"`gamma_d in [2E_d - 0.0392, 2E_d]`, lower end vacuous at `d = 4`" is right:
`2E_4 - 0.0392 = -0.019`.

## 3. `gamma_10 = 0` (recomputed with my own LP, and made exact)

The note's evidence for `gamma_10 = 0` has two parts:

- the band LP value 0 on a grid, which is only a lower bound and so proves
  nothing here;
- the relaxation LP's dual bound `-1.7e-11`, which gives `gamma_10 <= 1.7e-11`
  in floating point.

That supports the claim but does not prove exactly 0. I made it exact.

- Near `y = 0` the band is `[y^2, (1+eps_v) y^2]`. So write `rho = y^2 q(y)`
  with `q` even of degree 8.
- An LP that maximizes the margin in the `q`-band gives margin `2.8e-3`.
- I rounded the coefficients to rationals with denominator `1e9`. In units of
  `1e-9`, `q(y) = 1002795549 + 419528334 y^2 - 3338707087 y^4 + 4161904633 y^6 - 1593496982 y^8`.
- With `y1 = 19/50`, `eta = 1/20`, `eps_v = 1/50`, the following have no root
  on the closed interval (sympy `count_roots`, exact) and are positive at the
  midpoint:
  - `q - 1` and `1 + eps_v - q` on `[0, y1]`;
  - `y^2 q - 2 y1 y + y1^2` and `(1+eps_v) y^2 - (1-eta)(y-y1)^2 - y^2 q` on
    `[y1, 1]`.
- Hence `L <= rho <= U` on `[-1,1]`, `LB_{b10}(root) >= 0`, and
  `gamma_10 = 0` exactly. Since `gamma_9 = gamma_8 >= 0.000775 > 0` (a grid
  lower bound), degree 10 is the threshold.
- The consequence in the note is also right. With `delta = 0` and the
  theorem's base split, the chain's root bound is `G · 0 = f*`, so class b10
  prunes the reference chain at the root once `UBD <= eps`.

**Suggestion.** The certificate could replace "by LP" in Section 3.3 and in
the status table.

## 4. The b6 rerun (Section 6.4, revision item 1)

- **Authors' logs.** `logs/bb_jobs2.log` shows b6 = 2, 16, 128 with
  `base="gadget"` and 0 ambiguous boxes. It shows b6 = 44 with the balanced
  split at G = 2, and b4 = 10, 172, 2,592 and class (a) = 600, 12,336 with the
  gadget base split. `logs/bb_jobs1.log` shows the same b4 counts under the
  balanced split. The only ambiguous boxes anywhere are the 15 in the
  superseded balanced b6 run at G = 3, as Section 6.1 says.
- **Code.** In `robust_bb.py`, `base_weights(n, "gadget")` gives:
  - factor `(x_g, y_g)`: `u(x_g)` and half of `c y_g^2`;
  - factor `(y_g, z_g)`: the other half and `u(z_g)`;
  - connecting factor: nothing.

  This is the base split of Theorem 4.2. `run_job.py` defaults to it for
  chains. `bb()` and `Relax()` still default to `"balanced"`. This is harmless
  for the G = 1 scripts (`b10_gap.py`, `ceiling_check.py`), because at `n = 3`
  the two base splits coincide.
- **Rerun of the authors' code** (`rerun_authors_b6.py`,
  `logs/rerun_authors_b6.log`, 25 s): b6 gives 2 (G = 1) and 16 (G = 2) with
  the gadget split, and 44 (G = 2) with the balanced split.
- **Independent reimplementation** (`check_bb.py`, `logs/check_bb.log`).
  - With `delta = 0` and the gadget base split, the connecting factors vanish,
    so the chain bound is the sum of gadget bounds.
  - Each gadget bound is reduced to a band problem on the interval `Cy`, using
    closed-form partial minimizers over `Cx` and `Cz`. It is solved by an
    exchange LP (upper bound) and exact minimization of the dual shift on
    every quadratic piece (lower bound).
  - The tree uses widest-side bisection with first-index ties.
  - At `eps = 1e-4` (G = 1, 2, 3):

    | class | leaves | min prune margin | min split margin |
    |---|---|---|---|
    | b6 | 2, 16, 128 | `5.2e-5` | `2.3e-3` |
    | b4 | 10, 172, 2,592 | `1.0e-4` | `2.5e-4` |
    | a | 20, 600, 12,336 | `3.3e-5` | `1.4e-5` |

    There are no ambiguous boxes. Brackets are at most `2.5e-6` wide.
  - The growth rates (2.00 for b6, 2.47 for b4, 2.74 for class (a) per
    variable, from G = 2 to G = 3) follow.

## 5. The 1.063 ceiling (Section 4.4)

**Correct at the reference parameters.**

- On the corner box `[-1,-0.48] x [-1,-0.873] x [-1,-0.813]`, every term of
  both factors is nondecreasing in `|x|, |y|, |z|`. So with the split `r = 0`,
  both factor minima lie at the vertex nearest 0. There, `V_S = min_B g = g(vertex) = 2.712390`
  for **every** class `S`.
- This matters for Theorem 4.3(3). The same cap on `mu` applies to class
  `b_d`, as the note uses.
- `(vol/8) exp(mu V) = 0.7905, 1.0368, 1.3599` at `mu = 2.3, 2.4, 2.5`. The
  threshold is `mu0 = 2.3867`.
- The ceiling is `exp(mu0 gamma) = 1.1992` per gadget and 1.0624 per variable
  (1.0628 with `mu = 2.4`). The computed 1.0516 lies 1.07% below it.
- A scan over all corner boxes (`check_ceiling_params.py`) finds essentially
  the same box and `mu0`. So the review's box is the best corner box.

**R2 (wording).** The ceiling depends on the parameters.

- For the other parameter sets tried, the best corner box gives the following
  caps:

  | parameters | cap per variable |
  |---|---|
  | (0.38, 0.01, 0.005) | 1.073 |
  | (0.30, 0.01, 0.005) | 1.068 |
  | (0.45, 0.01, 0.005) | 1.072 |
  | (0.30, 0.005, 0.002) | 1.070 |
  | (0.38, 0.05, 0.1) | 1.041 |

- These are only upper bounds on the method's ceiling there. So "1.063" is a
  reference-parameter figure. The Summary ("cannot exceed about 1.063 per
  variable on this family"), the Open paragraph, and Section 6.5 ("on this
  gadget") should say "at the reference parameters". Alternatively they could
  say "about 1.06–1.07 for the parameter sets of Section 6.5". No conclusion
  changes.

**Theorem 4.3(3) addition.** "At most `exp(2.4 gamma_d) <= exp(4.8 E_d(L))`
per gadget at the reference parameters" is correct.

- For b4 this is 1.0188 per gadget, and for b6 1.0057.
- The `y1 = 0.3` figure "about 1.021" uses `2E_4`. The note labels the step
  "if the same cap on `mu` holds for `y1 = 0.3` (not checked)". I checked it.
  At `(0.30, 0.005, 0.002)` the best corner box gives `mu0 = 2.378 < 2.4`
  (`logs/check_ceiling_params.log`), so the statement holds:
  - with `2E_4`, at most 1.021 per variable;
  - with the known `gamma_4 = 0.0247`, at most 1.020 per variable.

  The note can drop "not checked".

## 6. Crossover estimates (Section 5)

`check_ceiling_crossover.py`, `logs/check_ceiling_crossover.log`.

- **Theorem 3.4 constants.** From the decomposition note, with `k = 2`,
  `Delta = 1`, `w = 1`, `K_1 = 1`, `s0 = 2`, `c_g = 3.61e-4`, `M_a = 16.4`,
  `alpha' = b'/2`, `A = 2`:
  - `Q = 1.49e6`;
  - (T2) forces `theta = 2^-21`, so `(4/theta)^2 = 7.04e13`;
  - the full size formula gives `N_dec(850) = 4.3e15 · 850`.
- **Crossovers** (`1.05156^n` computed, `1.00304^n` analytic):

  | comparison | computed base | analytic base |
  |---|---|---|
  | Theorem 3.4 size formula | `n = 850` | `n = 15,044` |
  | same, with the note's `4e15 n` shortcut | 849 | 14,998 |
  | gadget bags, `22 n/3` leaves | `n = 138` | `n = 3,327` |

  The note's "~850, ~15,000, ~140, ~3,300" are right.
- **Assumption in the bag count.** The gadget-bag count assumes 22 leaves per
  gadget at tolerance `eps/G`. Near `n = 3,300` this means `eps/G ≈ 1e-7` at
  `eps = 1e-4`. My code gives 22 leaves for one gadget at `eps = 1e-7` (class
  (a), no ambiguous boxes). At `1e-8` and below my solver's brackets are wider
  than `eps`, so those runs are inconclusive
  (`logs/check_bb_small_eps.log`). This supports the estimate, which the
  status table correctly calls an estimate.
- **Proved versus computed.** Only the analytic crossovers (15,000 and 3,300)
  rest on a fully proved single-tree constant. The computed base is a
  floating-point evaluation, as the note says elsewhere. The Summary's "The
  proved separation starts only near `n ≈ 850` (computed base)" could say
  "computer-evaluated" to match.

## 7. Section 1.5 citations

I checked each item at the bibliographic level (Crossref, publisher or author
pages) and, where accessible, against the abstract or text.

| Citation in the note | Exists | Supports the sentence |
|---|---|---|
| Falk, "Sharper bounds on nonconvex programs", Oper. Res. 22(2) (1974) 410–413 | yes (doi 10.1287/opre.22.2.410) | yes. The abstract says the generalized-multiplier and convex-envelope bounds "are the same if the original problem has only linear constraints, or if the problem is separable with certain properties". Applied to the copy formulation (linear copy constraints; the envelope of a block-separable function over a product of boxes is the sum of block envelopes), this gives the affine-`S` case. |
| Dür and Horst, JOTA 95 (1997) 347–369 | yes ("Lagrange duality and partitioning techniques in nonconvex global optimization") | yes. The abstract covers the duality gap under partitioning and branch-and-bound. |
| Nowak, Birkhäuser 2005 | yes (ISNM 152) | yes, as a general reference |
| Werner, IEEE TPAMI 29 (2007) 1165–1179 | yes | yes |
| Wainwright, Jaakkola, Willsky, IEEE TIT 51 (2005) 3697–3717 | yes | yes |
| Sontag, Globerson, Jaakkola, chapter in Sra, Nowozin, Wright (eds.), MIT Press 2011 | yes | yes |
| Wainwright and Jordan, FnT ML 1 (2008) 1–305 | yes | yes |
| Cooper et al., Artif. Intell. 174 (2010) 449–478 | yes (doi 10.1016/j.artint.2010.02.001) | yes. The author preprint contains verbatim: "Virtual arc consistency (VAC) can be seen as an approximation to OSAC that can be applied either during preprocessing or at every node of a search tree." It also says that OSAC was tried "during preprocessing", and that its LP "is the dual of the linear relaxation". |
| Ihler, Flerova, Dechter, Otten, UAI 2012 ("Join-graph based cost-shifting schemes") | yes | yes. Cost shifting in mini-bucket heuristics guides branch-and-bound. |
| Opper and Winther, JMLR 6 (2005) 2177–2204 | yes | yes. Two tractable distributions are made to agree on shared moments. |
| Grimm, Netzer, Schweighofer, Arch. Math. 89 (2007) 399–403 | yes | yes, as a short proof of the sparse representation theorem. The "two-clique instance" link to the band criterion is an analogy, and the note words it modestly. |
| Rockafellar, *Convex Analysis*, Thm 10.2; Gale, Klee, Rockafellar 1968 | yes | yes (Section 1 above) |

**R1 (factual fix).** The note says the review's Falk 1969 citation "was not
located". It exists: J. E. Falk, "Lagrange multipliers and nonconvex
programs", *SIAM J. Control* 7(4) (1969) 534–545, doi 10.1137/0307039
(Crossref; 106 citations in Semantic Scholar). I could not read its text
(paywalled), so its content is not checked here. Replace "was not located"
with the reference and "content not checked". Alternatively drop the sentence.
The substitution of Falk (1974), whose abstract supports the claim, is sound
either way.

The "What is new here" paragraph is appropriately hedged ("not on a
systematic survey").

## 8. Was anything silently strengthened?

**Mathematics.** Nothing is strengthened. The revised statements are:

- Lemma 1.3's proof;
- Proposition 2.1's incumbent condition;
- the Proposition 2.3 scope. I checked face-exact (M_b): a class-(a) split
  under a termwise relaxation adds only univariate gaps `>= 0`, so (M_b) and
  face-exact Theorem 1 hold for every such split, as stated;
- Proposition 3.3(3);
- the base split in Theorem 4.3;
- the ceiling;
- the Section 5 crossovers.

Each is either weaker than before, newly proved, or correctly labelled.

**Wording that claims more than the evidence** (all minor):

- **R5. "The review reproduced all class-(a), b4 and b6 counts"** (Summary 6,
  Section 6.1 "every class-(a), b4 and b6 count", Section 7, Section 8). The
  first review's independent code uses the `delta = 0` product identity, so
  it did not reproduce these rows:
  - the class-(a) row with `delta = 1e-3` (600, 12,330);
  - the `delta = 0.1` row (44, 108).

  Its log (`robust-lb-review-checks/logs/check3_bb.log`) covers only
  `delta = 0`. My code has the same limit. Say "all `delta = 0` counts".
- **R6. "`gamma_d <= 2E_d(L)` caps every class-(b_d) base from this family at
  `1 + O(1/d^2)`"** (Summary 4). The Section 8 sentence "Whether some path
  family defeats every fixed `d` with a base independent of `d` is open; for
  the gadget chains it is false" has the same problem, and more strongly.
  1. What is shown concerns the base that **Theorem 4.2 can prove**, not the
     growth of actual trees. Observed class-b6 trees grow 2.0 per variable at
     the reference parameters. Nothing in the note shows that the true tree
     sizes of `b_d` gadget chains have a base tending to 1 as `d` grows.
     Suggested text for Section 8: "for the gadget chains, the base that
     Theorem 4.2 can prove tends to 1 as `d` grows (Proposition 3.3(3));
     whether their true tree sizes do is not known."
  2. Even for the proved base, "every ... from this family" needs a cap on
     `mu` for all parameters. The note checks `mu < 2.4` only at the
     reference parameters. A one-line uniform cap closes this:
     - on `[-1,-1/2]^3` all couplings are nonnegative, so for every class and
       every admissible parameter choice, `V >= c/4 > 1/4` (split `r = 0`,
       each factor keeps its share of `c y^2`, and `y^2 >= 1/4`);
     - hence `(vol/8) exp(mu V) >= exp(mu/4)/64 >= 1` once
       `mu >= 4 ln 64 ≈ 16.6`;
     - so Theorem 4.2 gives at most `exp(16.6 gamma_d) <= exp(33.3 E_d(L))`
       per gadget. This is `1 + O(1/d^2)` uniformly in the parameters, because
       `E_d(L) <= C/d^2` with `C` independent of `y1`.

     With this sentence added, the Summary claim is proved as a statement
     about provable bases.
- **R2** (Section 5 above): "1.063 ... on this family" should say "at the
  reference parameters".
- **R7. Summary 6, "every pruned leaf carries a dual bound and every split box
  a primal fooling family, both checked".** The authors checked these only for
  class (a) with `G <= 2` (Section 6.1). Add "(checked for class (a),
  `G <= 2`)".

**Smaller wording points** (optional):

- Summary 3, "(about `1/d^2`)": the computed `E_d` are about `0.09/d^2` to
  `0.18/d^2`. "Of order `1/d^2`" is accurate.
- Summary 3, "positive for every `d` when the valley parameters are small":
  the quantifiers read the wrong way round, next to "zero for large `d` when
  the parameters are fixed". Say "for each `d`, positive when
  `eps_v + eta(1-y1)^2 < 2E_d(L)`".
- Section 3.4, "the band must be narrower than about `E_d(L)`": the
  sufficient condition from item 1 is width `< 2E_d(L)`.

## 9. Fixes

Required:

- **R1.** Section 1.5 and Section 10 item 2: Falk (1969) exists (SIAM J.
  Control 7 (1969) 534–545). Cite it with "content not checked", or drop the
  sentence. Do not say it was not located.

Recommended (wording; no result changes):

- **R6.** Summary 4 and Section 8: restrict the `1 + O(1/d^2)` statements to
  bases provable by Theorem 4.2. Add the uniform `mu < 16.6` cap. Replace "for
  the gadget chains it is false".
- **R5.** "All class-(a), b4 and b6 counts" becomes "all `delta = 0` counts"
  (Summary 6, Sections 6.1, 7, 8).
- **R2.** "1.063 on this family/gadget" becomes "at the reference parameters"
  (Summary, Open, Section 6.5).
- **R7.** Summary 6: "both checked" becomes "checked for class (a),
  `G <= 2`".
- **R3.** Lemma 1.3: one `r` per round, or one sentence on
  `sup_r F^r_{B_k}`.
- **R4.** Lifted paragraph: "feasible and bounded below".
- **Optional.** Cite the exact certificate for `gamma_10 = 0`
  (`reviews/robust-lb-recheck-checks/check_gamma.py`). Drop "not checked" from
  the `y1 = 0.3` cap in Theorem 4.3(3): `mu0 = 2.378` there. The status header
  and Section 8 can now say that the revision was rechecked.

## 10. Checks run

All commands were run from `research-20260929/reviews/robust-lb-recheck-checks/`
with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`, single-threaded and
time-limited. They are targeted checks only: no project-wide checks and no CI.
`PYTHONDONTWRITEBYTECODE=1` was set for the authors' code, so their directory
is unchanged.

| command | purpose | result (log) |
|---|---|---|
| `python3 check_gamma.py` | Lemma 3.1 partial minima; `gamma_d`, `E_d` brackets (own primal LP); `gamma_d <= 2E_d`; odd = even; exact `gamma_10 = 0` certificate | all confirmed; certificate: 0 roots on all four intervals (`logs/check_gamma.log`, 16 s) |
| `python3 check_bb.py {6,4,2} 1e-4 1 2 3` | independent leaf counts, theorem base split | b6 2/16/128, b4 10/172/2,592, a 20/600/12,336; 0 ambiguous (`logs/check_bb.log`, 80 s) |
| `python3 check_bb.py 2 {1e-7,1e-8,1e-9} 1` | gadget-bag count at small tolerance | 22 at `1e-7`; smaller `eps` inconclusive (bracket > `eps`) (`logs/check_bb_small_eps.log`) |
| `python3 rerun_authors_b6.py` | authors' `robust_bb.bb`, b6 | gadget split 2, 16; balanced split 44 (`logs/rerun_authors_b6.log`, 25 s) |
| `python3 check_ceiling_crossover.py` | corner box, `mu0`, ceiling; uniform `mu` cap; crossovers | `mu0 = 2.3867`, 1.0624 per variable; cap 16.64; crossovers 850 / 15,044 / 138 / 3,327 (`logs/check_ceiling_crossover.log`) |
| `python3 check_ceiling_params.py` | best corner box for six parameter sets | caps 1.041–1.073 per variable; `mu0 = 2.378` at `(0.30, 0.005, 0.002)` (`logs/check_ceiling_params.log`) |
| Crossref, Semantic Scholar, JMLR, INFORMS/RePEc, author preprint of Cooper et al. | Section 1.5 citations | Section 7 above |

Downloaded PDFs were kept in `/tmp` and deleted afterwards. The note and the
authors' files were not modified.
