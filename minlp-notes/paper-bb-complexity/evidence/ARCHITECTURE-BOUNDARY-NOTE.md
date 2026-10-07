# Boundary note: closed removed pieces after domain reduction

Short independent check by the boundary-scope Opus reviewer, 2026-10-05.
`ARCHITECTURE.md` did not exist when this note was written (last checked
23:16 EDT), so this note does not assess the architecture itself. It checks the
boundary defect against the source notes, compares it with the repair in
`AUDIT-SPATIAL.md`, Section 2.3, and lists what the architecture and the
chapter writers must carry. Source names: "constrained note" is
`research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md`;
other notes are named by directory. Line numbers refer to the current files.

## 1. Verdict

- The defect is real. It is not limited to degenerate retained boxes or to
  feasibility-based reduction. A closed frame slab contains the face it shares
  with the retained box. Points on that face were not removed. So on that face
  neither "the piece contains no feasible point" nor "every feasible point of
  the piece was removed by the relaxation" holds. Section 2 gives three
  hand-checkable counterexamples with nondegenerate retained boxes. Excluding
  dimension-collapsing reductions therefore does not remove the defect.
- The ownership repair in `AUDIT-SPATIAL.md`, Section 2.3, is correct as far as
  I checked. I re-read the downstream proofs in the constrained note that use
  the leaf-and-piece family: Theorems 3.1–3.3, 4.5, 4.6 and 5.2, Theorem 5.4,
  Proposition 5.6 (and Theorem 5.7 through it), Theorem 6.2 and Corollary 8.1.
  Each uses validity only at the point being certified, the geometry of one
  closed box that contains the point, and, for integrals, Borel measurability.
  Owned sets supply all three. The face-exact centroid proof (September 28
  note, Theorem 3.6) also needs convex owners, which the half-open rectangular
  rule supplies. I did not re-read Theorems 7.1, 7.2 and 8.2.
- In the first version of the audit I read (file time 23:05), the repair stated
  validity only at owned *feasible* points and counted only owners that meet
  `F`. The constraint-gap (tube) results need the dichotomy (D) at owned
  *infeasible* points and a count of all owners. The revised audit (23:10) adds
  this as "Owned tube dichotomy" with the count `K_all`, and
  `REVIEW-GEOMETRY-REPAIR-R1.md` reached the same conclusion independently. The
  point is resolved. Section 3, item 1, records my independent derivation as a
  confirmation.
- `AUTHORING-CONVENTIONS.md` (owned sets `A_e`, closed test boxes `C_e`,
  separate `N_cover`, `N_rect`, `N_tree`, separate event costs) is consistent
  with the repair.

## 2. Counterexamples with nondegenerate retained boxes

Notation is the constrained note's. R-inf is feasibility-based reduction and
R-rel is same-relaxation reduction. `S_1^-` is the closed lower slab of the
frame decomposition in coordinate 1. It uses the old box in every later
coordinate.

**E1 (objective gap; falsifies Lemma 2.1(b) and (d)).** Let `X0 = [0,1]^2` and
`f(y) = y_1`, and keep the linear constraint `y_1 >= 1/2` exactly
(`P_ex = {y_1 >= 1/2}`). Use `R_B = B ∩ P_ex` and `f_B = f - alpha q_B`, so
(G^pt_alpha) holds with equality. Then `f* = 1/2`, and the optimal set is
`{1/2} x [0,1]`. Take `eps < alpha/4`. At the root, either of two rounds raises
`l_1` to `1/2`:

- FBBT on the constraint, an R-inf round;
- OBBT on `y_1` with `UBD = f*`, an R-rel round. The point `(1/2, 1/2)` lies in
  the OBBT sublevel set, because `f_{B_0}(1/2,1/2) = 1/2 - alpha/2 <= 1/2 - eps`.

The retained box `[1/2, u'_1] x [0,1]` is nondegenerate, and
`S_1^- = [0,1/2] x [0,1]`.

- At `y = (1/2, 1/2)`, `m(y) = 0` and `q_{S_1^-}(y) = 0 + 1/4`. So (V) fails on
  `S_1^-`. This contradicts both bullets of Lemma 2.1(b) (lines 397–401). The
  R-inf piece meets `F`, and the R-rel piece contains a feasible point that was
  not removed.
- This is not a corner case. Whenever OBBT moves a bound, the minimizer that
  defines the new bound lies in the closed slab and is retained. In E1 that
  minimizer is optimal.
- Suppose the run uses only the FBBT round. Every leaf in `[1/2,1] x [0,1]`
  meets `F`, and so does `S_1^-`. Hence `|P_F| = #leaves + 1`, while Lemma
  2.1(d) (lines 380–382) gives `|P_F| <= #leaves`.

**E2 (tube; falsifies Lemma 2.1(c)).** Let `X0 = [0,1] x [-1,1]`, and relax
`f(z) = z_2` exactly (`alpha = 0`). Keep `z_1 >= 1/2` exactly (in `P_ex`), and
relax `-z_2 <= 0` to `-z_2 <= q_B(z)`. Then
`R_B = {z in B ∩ P_ex : -z_2 <= q_B(z)}` is exactly the tube, so (T_{0,1})
holds, and `f* = 0`.

- Root OBBT on `z_1`, with `UBD = f*` and cutoff `UBD - eps`, sets `l'_1 = 1/2`.
  The removed points violate `P_ex`, so this is an R-rel round, and the run uses
  no R-inf round.
- For `eps < eps' <= 1/2`, the point `z = (1/2, -eps')` lies in
  `S_1^- = [0,1/2] x [-1,1]` and in the retained box.
- It has `v(z) = eps' < 1 - eps'^2 = q_{S_1^-}(z)` and `f(z) = -eps' < f* - eps`.
  Both alternatives of (D) fail, which contradicts Lemma 2.1(c)
  (lines 403–412).

Super-optimal, nearly feasible points like `z` are exactly what the Section 5
lower bounds count, so the error matters there.

**E3 (face-exact model with a polyhedral constraint; falsifies Lemma 1.2 of the
September 28 face-exact note).** Let `X0 = [0,1]^3` and `Q = {x_1 >= 1/2}`, and
let `f = x_1 + (x_2 - 1/2)^2 + (x_3 - 1/2)^2 + x_2 x_3`. Keep the convex part
exact and relax `x_2 x_3` by its McCormick envelope.

- The quadratic part in `(x_2, x_3)` is convex with stationary point
  `(1/3, 1/3)`. So the unique minimizer is `x* = (1/2, 1/3, 1/3)`, with
  `f* = 2/3`.
- FBBT on `Q` raises `l_1` to `1/2`. The closed slab `[0,1/2] x [0,1]^2`
  contains `x*`.
- At `x*`, the McCormick gap is `x_2 x_3 - max(0, x_2 + x_3 - 1) = 1/9`. So the
  slab is not valid for `eps < 1/9`. This contradicts "A piece of type (i)
  contains no point of `F`" (line 236).

## 3. Requirements for the repaired lemma

Adopt the ownership construction of the revised `AUDIT-SPATIAL.md`,
Section 2.3: half-open rectangular owners `A_e`, closed test boxes `C_e`,
retained boundaries carried forward, an emptying reduction recorded as one
terminal event, the owned tube dichotomy, and the counts `K_F` and `K_all`
(with `L` as defined there, including virtual probe events). The items below
confirm or add to it.

1. **Tube version (confirmation).** My independent derivation matches the
   audit's "Owned tube dichotomy".
   - *Statement.* Assume (T_{alpha,beta}) and a run with no R-inf round. Then
     for every element `e` and every `z in A_e ∩ P_ex`, either
     `v(z) > beta q_{C_e}(z)` or `f(z) - alpha q_{C_e}(z) >= f* - eps`.
   - *Key step, for a discarded R-rel owner from box `B`.* If
     `v(z) <= beta q_{C_e}(z) <= beta q_B(z)`, then (T) gives `z in R_B`. So `z`
     was removed by the cutoff, and
     `f(z) - alpha q_{C_e}(z) >= f(z) - alpha q_B(z) >= f_B(z) > UBD - eps`.
   - *Count.* Tube bounds count all owners, `K_all <= L + 2n R_rel`, because
     their witnesses can be infeasible. `K_F`, the number of owners that meet
     `F`, is the right count only for objective-gap bounds.
2. **State each lower-bound theorem once, for owned families.**
   - The theorems need only that the owners cover the relevant set (`F`, a
     sublevel set, a stratum, or `X0 ∩ P_ex`). Subadditivity then gives the
     sum, so the audit's partition is a convenient special case, not a
     requirement.
   - Closed covers, rectangular partitions and guillotine trees are the case
     `A_e = C_e`. So one lower-bound statement applies to `N_cover`, `N_rect`,
     `N_tree` and every run's owner count. It does not give
     `N_cover <= K_F`, because a run's owned family is not a fully valid closed
     cover (`REVIEW-GEOMETRY-REPAIR-R1.md` makes the same point).
   - In each proof, "`y in C`" becomes "`y in A_e`". Vertices, `q`, widths and
     arcsine integrals still use the closed box `C_e`.
3. **Use the follow-the-point proof.**
   - The cutoff note's Lemma 2.1 (lines 364–437) already has this form. It
     states pointwise certification, and its proof follows each feasible point
     through splits, reductions and propagation phases. The ownership
     construction is the same argument with explicit sets.
   - Its parenthetical at line 431, "R-inf pieces contain no feasible point",
     is false for closed pieces. It should read "R-inf rounds remove no feasible
     point".
4. **Keep per-round pieces for R-rel rounds.** Ownership fixes the retained
   boundary. It does not replace the earlier per-round fix: a merged frame
   still fails, because its closure need not lie in the box whose relaxation
   removed its points. Both fixes are needed.
5. **Do not claim bounds for leaves alone.** With tightening, the theorems bound
   leaves plus `2n` per R-rel round (owner events), not `N_opt` and not the
   leaf count. The sources prove nothing for leaves alone, and the discrete
   analogue fails (integer-core note, Proposition 1.9, line 526).

## 4. Where closed pieces remain correct

The paper can use one ownership lemma everywhere. It should not, however,
describe the following closed-piece arguments as wrong.

- **Unconstrained problems, cutoff-only removal, finite convex relaxation.**
  This case has a short proof:
  1. Let `S` be a closed lower slab of positive width in coordinate `i`, and
     let `y` lie on its face shared with the retained box.
  2. For `0 < t <= t_0`, the points `y - t e_i` lie in `S` outside the retained
     box, so they were removed: `f_{B_k}(y - t e_i) > UBD - eps`.
  3. Convexity gives
     `f_{B_k}(y - t e_i) <= (1 - t/t_0) f_{B_k}(y) + (t/t_0) f_{B_k}(y - t_0 e_i)`.
     If `f_{B_k}(y) < UBD - eps`, the right side is below `UBD - eps` for small
     `t`, a contradiction. Hence `f_{B_k} >= UBD - eps` on all of `S`.

  Upper slabs are symmetric. This bears on three source notes:
  - *Robust-lower-bound note, Lemma 1.3 (lines 292–327).* It uses this
    argument through upper semicontinuity and is correct. Its S-cover test
    `LB_S(C) >= f* - eps` is a whole-box test, not a pointwise test at owned
    points. If a chapter uses S-covers, keep this closed-piece argument together
    with its hypotheses: no constraints, and a finite convex `sup_r F^r_{B_k}`.
  - *September 29 face-exact note, Lemma 1.2 (lines 219–235).* Its conclusion
    is correct. The proof sentence at line 232 ("consists of points `y` with
    `f_{B_k}(y) > UBD - eps`") is false on the retained face, so the proof needs
    this step or ownership.
  - *Constrained note.* Its node model allows nonconvex `f_B`, so even its
    unconstrained case needs ownership.
- **Constraints break this argument.** In E1–E3 the nearby removed points were
  removed because they are infeasible or outside `R_B`, not because of the
  cutoff. No limit argument applies.
- **Integer reductions are unaffected.** Rounded bounds such as
  `x_i <= l'_i - 1` leave an open strip with no lattice points between the
  removed piece and the retained box. The integer-core certificates hold on the
  closed piece. This agrees with `AUDIT-DISCRETE.md`, finding 6. Do not import
  the ownership machinery there.
- **Full-dimensional integrals and volumes** do not change in value. The counts
  in Lemma 2.1(d) and Corollary 8.1 still change. Lower-dimensional integrals,
  centroid arguments and covering arguments at specific points need ownership.

## 5. Source statements not to copy as written

| Source | Location | Problem | Use instead |
|---|---|---|---|
| constrained note | Lemma 2.1(b)–(d), lines 357–415 | closed pieces (E1, E2) | owned (V) and (D); owner counts |
| constrained note | Section 4 opening (634–639); Theorem 3.3 remark (526–529); Lemma 5.1 (930–931); Theorem 6.2 and its `P_F` remark (1274–1301) | cite the closed family | owned families; `K_F` or `K_all` |
| constrained note | Corollary 8.1(a)–(b), lines 1908–1920 | "because (R-inf) pieces do not meet `F`" is false | "R-inf owners contain no feasible point"; conclusion survives |
| Sept 28 face-exact note | Lemma 1.2, lines 223–242 | false when `Q` is present (E3) | ownership lemma |
| Sept 29 face-exact note | Lemma 1.2 proof, line 232 | false step, true conclusion | convexity step (Section 4) or ownership |
| cutoff note | Lemma 2.1 proof, line 431 | parenthetical false for closed pieces | "R-inf rounds remove no feasible point" |
| decomposition note | lines 445–447, 1011–1014 | cite the closed lemma; unconstrained, so conclusions survive | cite the repaired lemma |
| RLCT note | Theorem 3.1, lines 403–406 | same; face integrals are lower-dimensional, so boundaries matter | cite the repaired lemma |
| `bb-complexity/SYNTHESIS.md` | lines 50–52 | "`N_opt(eps) >= ...` for ... same-relaxation tightening" conflates the benchmark with run cost | bound owner events, `#leaves + 2n R_rel` |

## 6. Checks for the architecture once it exists

- The certificates chapter defines elements `(A_e, C_e)` and the tests at owned
  points: (V) at owned feasible points, and (D) at owned points of `P_ex`. The
  three benchmarks are the closed special case.
- One reduction lemma serves the whole paper:
  - it gives both counts: `K_F` for objective-gap bounds, and `K_all`, with no
    R-inf rounds, for tube bounds;
  - it names the excluded operations: objective-cutoff propagation (outside
    the propagation chapter), cuts beyond the relaxation, and reductions on
    lifted variables;
  - it keeps per-round pieces.
- The geometry, tube, face-exact and propagation chapters cite that lemma and
  do not restate closed versions. The face-exact chapter uses convex owners for
  its centroid arguments.
- Corollaries about tightening state the event count, not `N_opt` and not the
  number of leaves.
- If robust-lower-bound S-covers are included, their closed-piece argument is
  kept with its hypotheses and is not extended to constrained problems.

## 7. Record

Read:
- evidence files: `BRIEF.md`, `INCOMING-AUDITS.md`, `AUTHORING-CONVENTIONS.md`,
  `ISSUES.md`, `AUDIT-SPATIAL.md` (Sections 1–2 and its tube and propagation
  passages; Section 2.3 re-read after the 23:10 revision), the verdict and
  ownership sections of `REVIEW-GEOMETRY-REPAIR-R1.md`, and finding 6 of
  `AUDIT-DISCRETE.md`;
- the constrained note: Sections 1–2 in full, the theorems of Sections 3–6
  named in Section 1 above, and Section 8.3;
- the September 28 face-exact note: Sections 1.1–1.2 and Theorem 3.6;
- the cutoff note: Lemma 2.1;
- the September 29 face-exact, robust-lower-bound, decomposition and RLCT
  notes at the cited lines;
- the integer-core reduction theorem (Theorem 1.8) and `SYNTHESIS.md`.

Checks: hand arithmetic for E1–E3 and for the convexity step in Section 4. No
literature search, experiment, project-wide check, CI inspection, or edit
outside this file.
