# Stage 4, round 1 — independent review 5

## Verdict

**No major issues found. Two minor exposition/attribution corrections are needed.** The bounded-rank separation theorem, new finite-basis recovery theorem, coefficient-transfer lemma, and new five-product K4 construction are mathematically sound in their stated scope. The seven-product source construction is also preserved correctly.

## Findings

1. **R5-S04-01 — minor: the closing predecessor comparison should not suggest a different balance model.** Location: `sections/04-bounded-rank.tex`, lines 519–523, especially “on a different graph with balance inequalities.” Khademnia–Davarnia's Section 3 explicitly represents equality balances by pairs of opposite inequalities, and their Example 2 is within that network specialization. Thus the quoted wording can recreate the misleading equality/inequality distinction that was already corrected in Section 2 of this manuscript. The material distinction is a projection-cone aggregation weight versus a necessary coefficient ratio on actual observed-product coordinates. Remove “with balance inequalities,” or explicitly say that their balances are expressed using inequalities and that this alone is not a different equality-flow domain. The existing distinction between their dual multiplier and the present facet-ratio conclusion should remain. This is minor: it is a local attribution clarification and does not affect any proof or erase the substantive coefficient-result distinction. Evidence: the repository PDF's Section 3 opening and Example 2; extracted passages are retained in `verification/reviewer5/stage04-round01/khademnia.txt`, lines 202–206 and 603 onward.

2. **R5-S04-02 — minor: state that the five-product modification changes the balance vector, not merely the reference coordinates.** Location: the last sentence of Remark 6.9, `sections/04-bounded-rank.tex`, lines 512–514: “Changing the reference on 01 ... makes the residual support face an edge instead of a point.” Earlier sections correctly allow arbitrary reference flows for one fixed domain, but translating reference coordinates within that domain cannot change the dimension of an exposed face. Here the construction changes `v_01` **and defines the new balances by `b=Av`**, so it changes the flow polytope itself: the balances move from `(-3/2,-1/2,1/2,3/2)` to `(-5/4,-3/4,1/2,3/2)`. Add “and the associated balances” or equivalent wording. This is minor because both constructions already display the correct distinct balance vectors; only the explanatory sentence blurs a meaningful distinction between coordinate choice and instance modification.

## General mathematical review

- Checked the signed-normal construction from the original chord-coordinate matrix, repeated-normal right-hand sides, and observed state slices. The signed normal matrix retains total unimodularity and the signed coordinate rows. At zero state weight, any feasible state is correctly forced to zero.
- Checked the local positive-circuit proof, including minimal dependence, unit primitive coefficients from TU minors, and completeness by Farkas' lemma. Opposite normals can coexist in a minimal positive dependence only as their own pair, giving the claimed cancellation/unit product coefficients.
- Checked the ternary primitive edge-direction and transformed-edge properties, including lower-dimensional state polytopes. The tight-row rank argument is valid without a full-dimensionality assumption.
- Checked the objective arrangement, its pointed chambers, complete support-ray family, and extension of support linearity to chamber closures. The proof covers segments, points, and lower-dimensional sums; it does not assume that the sum is full-dimensional.
- Checked the support-dual basis formula, existence of an optimal independent-support dual even for a degenerate primal, integrality of multipliers, and the stronger transformed-direction cofactor argument giving `H_s` rather than a loose matrix-product estimate.
- Recomputed `H_1,...,H_4 = 1,1,2,5`. Checked that product indices cannot repeat within a selected nonsingular support basis or across states, and that chord coordinates preserve the corresponding flow coefficient bounds. The rational row normalization is explicit and does not claim a primitive-integer bound after clearing simplex denominators.
- Checked the library enumeration and sparse state counts behind the `2^{O(r^2)} N` separation bound. The theorem properly includes preprocessing, separates observation grouping, and claims rational arithmetic rather than unit bit costs. It makes no unsupported production runtime claim.

## Independent scrutiny of the new recovery theorem

Theorem 6.6 is correct. In particular:

1. The suffix support inequalities give exactly `Q_i` intersected with the translated remaining Minkowski sum; the signs in equation (80) are correct.
2. The permissible polytope is nonempty by the maintained aggregate invariant and bounded because it lies in `Q_i`.
3. A vertex of a bounded lower-dimensional polytope still has a full ambient-rank set of active defining rows, because otherwise two-sided small null motions contradict extremality. Thus enumerating full nonsingular row bases does not miss degenerate states.
4. The recovery normals depend only on the block library. With `2^{O(s^2)}` normals, enumerating all `s`-row bases and checking all inequalities has the stated `2^{O(s^3)}` bound per local state.
5. The rational encoding argument handles sequential recovery correctly: each step introduces at most one selected basis determinant into a shared denominator, so denominator encoding length grows additively in the number of states. The initial data denominators have polynomial combined length, and bounded state points and fixed inverse matrices also bound numerators and rejected candidates.
6. Positive-weight normalization and local default states reconstruct a compact global decomposition through the accepted block theorem. Dense output remains a separate cost.

I implemented an independent exact rank-three check using primal vertex enumeration to obtain state supports, then the manuscript's fixed-normal recovery logic without importing repository implementation code. It recovered **126 state vectors across 36 families**, including point states and slices with fixed coordinates. Every recovered state met all original state inequalities, every remaining aggregate met the suffix supports, and every final remainder was zero.

## Independent scrutiny of both K4 constructions

The new five-product construction is correct:

- Recomputed the incidence matrix, `Av`, `C`, and the aggregate arc vector.
- Derived the observed state forms `(p,q,p)` and `s(1,-1,0)` directly from the five observation equations.
- Verified the asymmetric scaled interval on arc `01` and the symmetric intervals on the remaining arcs.
- The residual support bound in direction `(1,1,1)` gives the necessary condition `2p+q >= 0`.
- The proposed `s=q/2` and residual vector sum to the fixed aggregate and satisfy all arc bounds throughout the claimed neighborhood. The residual fourth coordinate indeed lies in `(3/16,11/48)`.
- The section lemma correctly transfers this local half-plane to a necessary observed-product coefficient ratio. Two-dimensional local section interior forces all valid affine equations to have zero coefficients on the two free coordinates, so affine-equation changes cannot remove the ratio.

My independent exact original-flow check examined a **361-point rational grid** inside the stated neighborhood. It verified **185 feasible witnesses** against every original arc bound, incidence equation, aggregate equation, and fixed/free observed-product coordinate. The other **176 points** have a strict exact residual-support obstruction. This does not replace the neighborhood proof, which I checked separately.

The seven-product symmetric variant is retained accurately, including its state directions, exact local half-plane, and witness construction. Its residual support face is a point; the altered-balance five-product instance has a nontrivial residual support edge. Neither construction is confused with the earlier single-source/single-sink forest-complement K4 example.

## Executable evidence

`verification/reviewer5/stage04-round01/check_rank3.py` and `check_rank3.json` contain the independent exact checks. They also reconstruct the K4 library with **7 edge directions, 18 support rays, and 128 normal bases**, verify the ternary transformed-edge condition and multiplier bound, and enumerate **544 recovery bases** after harmless duplicate-normal consolidation. All checks passed.

## Coverage, build, and presentation

Read `results/network-simplex-bounded-rank-hull.md` in full. All substantive statements are represented: the finite local certificates, support library, coefficient bound, grouping and complexity qualifications, classical-method attribution, and original seven-product sharpness example. The new recovery theorem resolves the source note's explicit open constructive-recovery question with a larger stated parameter factor. The five-product example strengthens rather than replaces the older result. Historical implementation counts can appropriately be treated in the later implementation/verification section.

Built a private copy of the frozen snapshot. The PDF has **27 pages**; the final log has no warnings, undefined citations/references, or overfull/underfull boxes. Visually inspected pages **23 and 25**, containing the recovery proof and both K4 constructions. The displays fit the margins and are readable. The proofs explain the main subtle points sufficiently for a reader without the source notes.

## Limitations and independence

This review does not establish priority, audit future computational claims, or verify every bibliographic metadata field with publishers. Exact computational evidence concentrates on rank three; the general parameter bounds were reviewed through their proofs. I did not read other current-round reports, coordinate findings, spawn agents, edit manuscript sources, or build in the frozen snapshot.
