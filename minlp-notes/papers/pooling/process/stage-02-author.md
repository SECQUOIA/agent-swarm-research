# Stage 2 author record

Author: `/root/stage02_author`. Draft: `sections/02-algebraic-complexity.tex`.
Status: complete sole-author draft, frozen for the required full-stage review round. This is an author completion record, not a review verdict.

## Scope delivered

- Full ETR-INV to no-bypass pooling reduction: forcing costs and threshold, variable complements, reciprocal emissions, quality conversion, inverse pools, both equation gadgets, range enforcement for unused variables, complete forward/reverse checks, capacity bookkeeping, degree/bit bounds, and rational bijection of arc-flow sets (`s2:etr-complete`, `s2:bijection`).
- Full finite-data chain refinement, including request allocation, at most `6m+2n` links, every node type's degree, lower bounds on slack/diluent, constant data versus growing threshold, and preservation of the bijection (`s2:bounded`).
- Upper-only complementary attributes, feasibility via positive exact node totals, and careful zero-flow/threshold scope (`s2:variants`).
- Separate complete one-pool bypass construction, collision-free mathematical fresh-variable normalization, every pin, auxiliary range checks, both directions, dense encoding size, and rational bijection (`s2:one-pool-etr`).
- Arbitrary algebraic-degree singleton consequence, narrowed to the compact basic-closed source route; transferred to both finite-data degree-bounded and one-pool constructions (`s2:algebraic-witness`).
- Root's corrected small irrational example, independently verified and written as a full global optimization proof with all physical data (`s2:tiny-irrational`).
- Fixed-dimensional linear-fiber basis-index NP theorem with lower-dimensional vertices, determinant sign clearing, degree/height bounds, a concrete determinant interpolation algorithm, and primary-source exact bit-complexity attribution (`s2:fiber-np`).
- Pooling NP scopes for fixed pool times quality count/rank/product count; fixed pool and input counts; all zero-throughput and no-outlet cases; arbitrary bypass coupling/contracts/costs; and the established one-pool no-bypass active-product certificate (`s2:pooling-np`, `s2:no-bypass-np`).
- Distinction between exact certificate membership, algebraic flow values, and polynomial-size rational points when every polynomial constraint may have a specified absolute residual tolerance. No algorithm or exact-feasibility guarantee is inferred from rounding.

Stage 1 source was not edited. No subagents were used. Root owns builds and independent physical checks. No new TeX package was required.

## Source verification and narrow correction

Read `literature/AGENTS.md` before using the literature. Read the original result files, relevant historical audits, accepted foundations, and original checking code. Historical PASS labels were not treated as proof.

Read Abrahamsen--Adamaszek--Miltzow's ETR-INV Definition 5 and Theorem 7 in the local arXiv text; the bibliography explicitly makes those locators arXiv-version locators. Title and all three author names were checked against the original title page; the attached article metadata points to JACM 69(1), article 4 (2022), DOI 10.1145/3486220. The DOI endpoint returned 403 during this author's check; the accessible primary arXiv record confirms title, authors, and version history but labels the version as the 2018 STOC manuscript. Root retains responsibility for the independent metadata audit.

Read Abrahamsen--Miltzow's original *Dynamic Toolbox for ETRINV*, including the exact transformations C--G on PDF pp.8–18 and the original diagrams on pp.16 and 18. Root discovered that Lemma A's general strict-inequality/disjunction preprocessing leaves inverse auxiliaries free on inactive disjuncts; see `root-stage-02-check.md`. The author independently agrees. Our input `p(x)=0, c<=x<=d` has no strict predicate or disjunction, so we use uniquely defined weak slacks and entirely bypass that step. No general compact semialgebraic universality theorem is asserted by this pooling section.

Checks of the applicable remaining route:

1. Lemma C introduces only constants and uniquely evaluated addition/multiplication gates. Applied to the basic-closed singleton with explicit slacks, it gives a compact graph over the singleton.
2. Lemma D introduces a nonzero rational scaling through a uniquely determined squaring chain, and the multiplication replacement `(epsilon*x)(epsilon*y)=epsilon^2*z`, with `epsilon*(epsilon*z)=epsilon^2*z`. Projection followed by division by epsilon recovers the original variables; the radius argument is used only on an already compact set.
3. Lemma E translates coordinates to `x+1`, uses affine companion values, rewrites sums and products, and enforces `x>=0` through a variable `x+1/2` whose global lower bound is `1/2`. All companion values are uniquely affine or quadratic in the original small coordinates. Its notation `x+Delta=1` can be expressed in the stated addition language as `(x+Delta)+(1/2)=3/2`, using the constructed constants. Taking the original scale sufficiently small keeps each finitely many companion expressions inside `[1/2,2]`; the `x+1/2` boundary uses the known nonnegativity. The companion `x+3/4+Delta` is near `7/4`, also inside the range. We do not need the source's overbroad list of companion constant terms.
4. Lemma F's original Figure 2 computes `average=((x+1)+(y+1))/2`, squares it and the two inputs, and combines them by its stated shifted additions/halvings to obtain `(x+1)(y+1)`. The introduced quantities are unique polynomial values. All squaring arguments remain near one.
5. Lemma G's original Figure 3 starts from `x+1`, takes its reciprocal and that of `x+3/2`, and forms the difference `(x+4)/(3x+3)-2/(2x+3)=(2x^2+5x+6)/(6x^2+15x+9)`. Doubling and subtracting `2/3` gives `2/(2x^2+5x+3)`; its reciprocal and the last affine operations yield `(x+1)^2`. All divisions have positive denominators near zero, and every gate value is uniquely determined. These direct checks suffice without relying on the general printed quotient-bound lemma's notation.

The narrow route therefore preserves a rational singleton and a nonzero affine recovery of its original coordinate. Promised intervals contain every solution and need not become extra constraints in our ETR-INV instance. Only the applied external transformations, not their unrelated general universality claims, are relied upon.

For the NP verifier, read the original BPR 1996 title page and Section 1.3, especially Theorem 1.3.3 and the definition of “well-behaved” algorithms bounding intermediate integer bit lengths. The primary theorem directly supplies fixed-dimensional polynomial bit complexity. The repository survey's Theorem 2.18 pointer belongs to a different version and was not reused.

Read Haugland's original 2016 paper, including its title page, lower-bound convention following equations (5)–(8), and Theorem 2's active-product linearization. The historical one-pool review's assertion that lower bounds appear only in Section 4 is incorrect. The manuscript uses its own explicit model and attributes only the established active-product argument to Haugland.

Bibliography additions preserve the four existing accepted entries. The newly added source keys are `abrahamsen2022-the-art-gallery-problem-is`, `abrahamsen2019-dynamic-toolbox-for-etrinv`, `basu1996-on-the-combinatorial-and-algebraic`, and `haugland2016-the-computational-complexity-of-the`.

## Exact checks and layout

Added `verification/check_etr_source_identities.py`, a focused symbolic check of both original source diagrams, plus exact rational interval enclosures for every diagram coordinate on the whole box `|x|,|y|<=10^-6`. It checks identities, denominator positivity, and `[1/2,2]` ranges; it is not another pooling forward checker. Command:

`/workspace/local-home/miniconda3/envs/minlp-notes/bin/python papers/pooling/verification/check_etr_source_identities.py`

Result: `PASS: both source diagram identities, nonzero denominators, and exact full-box range bounds`.

The initial symbolic assertion used `cancel` directly on a nested rational residual and SymPy retained an uncombined reciprocal expression. Applying `together` before `cancel` gives exact zero. No mathematical identity or test threshold was changed.

Root separately reports 104 exact one-pool physical witnesses, 980 normalized equations, 1775 pins, and a rerun of the bounded checker on seven rational systems and 300 structural cases. Those outputs are recorded in `root-stage-02-check.md`; they supplement the proof's universal reverse direction and are not claimed as formal certification.

Root's forced `latexmk -g` build produced a 22-page stage1+2 PDF without final warnings. The author visually inspected manuscript pp.12 and 19 (gadget table and full certificate theorem/proof); both are readable with no clipping. Two later wording-only self-check corrections clarify constant normalization and explicitly cover defining-domain polynomial degrees. Root can run the final tracked build before taking the frozen snapshot.

## Retained boundaries

One-attribute upper-quality-only ETR hardness remains unresolved. Feasibility with zero lower flow bounds is not made hard by the objective-forcing reductions. Fixed-dimensional NP membership is not a polynomial algorithm, does not assert rational optimal flows, and does not imply strong hardness. General compact-semialgebraic universality is not needed and is not claimed. Approximation statements allow residual error in every original polynomial constraint and do not establish exact feasible rational witnesses.
