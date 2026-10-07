# Independent S5a review — reviewer 3

Reviewed file: `complexity/sections/08-design.tex`, all 749 lines.

Initial SHA-256: `85ea7d7942ab63a9a94d4a91dd10b9e3b30b736982a4f58c6a2af52007807295`.

Final SHA-256: `85ea7d7942ab63a9a94d4a91dd10b9e3b30b736982a4f58c6a2af52007807295`.

## Verdict

Pass with one minor correction. I found no major mathematical, complexity, recovery, or scope defect in the frozen section. In particular, **the new fixed-measurement theorem for independent polynomial-law cycle polytopes with the stated rational local capacities is supported by its complete proof**. Its argument does not require quadratic root formulas, bounded law degree, bounded cycle size, bounded parameter dimension, or a common algebraic field for all cycles.

This is an independent assessment of the supplied proof and its identified predecessors, not a claim of exhaustive priority research. The source access limits below remain relevant.

## Findings

### Minor R3-1: use absolute coefficients in the linear-value error budget

**Location:** `08-design.tex:353–355`, proof of `thm:a-design-independent`.

The instruction to refine until the sum of each rational coefficient times its enclosure width is below the requested error omits absolute values. The coefficients `gamma_C` may be negative. Signed products can cancel or make the stopping test true before the value enclosure is accurate. For example, one coefficient `gamma_C=-1` and an enclosure of width one pass a signed test against any positive tolerance, though the value uncertainty is still one.

**Correction:** require `sum_C |gamma_C| width(I_C) <= eps`, or give every root error at most `eps/[2(1+sum_C |gamma_C|)]`. Ignore zero coefficients. The earlier `thm:a-weight-cactus-region` already uses an absolute-coefficient budget.

**Why minor:** this is a local omission in an error-bound instruction. The exact optimizing scenario is unaffected, and the corrected refinement still takes polynomial bit time. It does not affect the measurement theorem, whose separate error estimate already uses absolute direction coefficients.

### Major findings

None found.

## Mathematical coverage and checks

### Exact monotone root optimization

I checked the whole theorem and proof, including equality and the arithmetic recovery step.

- Strict increase gives exactly the two displayed LP tests. A convex combination of vertex evaluations at any parameter's root proves that vertex roots bracket that root. This proves attainment without needing a prior continuity theorem or a derivative lower bound.
- Every vertex of a bounded H-polytope has a full-rank collection of active normals in the ambient parameter dimension, including a lower-dimensional polytope represented by inequalities. Otherwise a sufficiently small displacement in either direction along the nullspace of the active normals stays feasible. Thus the ambient Cramer bound is applicable.
- Clearing denominators across rows and polynomial pieces has polynomial bit length. The bound `(t+1) Delta P_0` covers the specialized polynomials uniformly. Strict increase prevents an identically zero positive-width specialized piece; continuity covers breakpoint roots.
- Taking the primitive squarefree part of a product accounts for common factors, distinct roots of one polynomial, and repeated roots. The stated discriminant estimate yields a weaker but sufficient separation bound with polynomial logarithm. This is a bit-complexity argument using dense numerical degree, not sparse binary exponents.
- In the maximum algorithm, the LP-selected vertex has a root between the lower bracket endpoint and the global maximum. Both are vertex roots, so a bracket narrower than the common separation bound forces equality. The minimum version has the correctly reversed LP and uses the upper bracket endpoint. Initial-bracket endpoint optima and equality tests do not break these invariants.
- Successive coordinate optimization stays on faces of the original polytope. Coordinate values and the initial objective equality therefore inherit bounds from original vertices; the argument does not compound unspecified LP encoding bounds over many iterations.
- Piece selection, squarefree extraction, and isolation produce the exact local output promised. The `t=0` and repeated-root cases are covered. The assumptions exclude degree zero on a nontrivial bracket.

### Passivity, existence, reorientation, and the scalar reduction

I compared this reduction with `thm:a-pre-existence`, `lem:a-pre-block`, and `lem:a-pre-cycle` in `01-preliminaries.tex`.

The primitive lower bound has the right sign on both tails, and the sum is coercive for every fixed admissible parameter. Strict convexity gives a unique flow. Orthogonality to the conservation kernel gives potentials without a full-row-rank assumption on the incidence matrix. Nonzero flow points strictly down the potential, excluding a directed cycle; a source-to-sink decomposition gives the stated conservative bound `B=sum_v |b_v|`.

The cactus block decomposition makes effective nominations independent of every law parameter. Consistently orienting a cycle leaves one circulation with rational offsets, and selecting a reference-edge flow puts that circulation in `[-B,B]`. Replacing an input law by `-g_e(-x;theta)` is essential for nonodd laws and preserves continuity, strict increase, zero at the origin, and affine parameter dependence. Reflected boundaries and then translated boundaries remain rational. Binomial expansion of shifted dense polynomials increases coefficient bit lengths polynomially and does not increase degree. The union of partitions has polynomial size; there is no Cartesian product of edge pieces.

The section correctly treats correlated-family admissibility as a promise and does not borrow the independent-box validation result beyond its scope. Zero nominations and the edgeless graph are separated before a nontrivial root bracket is used.

### Global correlations, capacity signs, and original witnesses

For a strictly increasing cycle equation, the lower capacity `q_C>=a_C` is equivalent to `H_C(a_C,theta)<=0`; the upper capacity is equivalent to `H_C(b_C,theta)>=0`. These are rational affine inequalities even for polynomial laws. The proof correctly converts an originally reversed arc and a negative coefficient in a local linear inequality. A zero circulation coefficient is a constant test.

Conjoining the inequalities with the original global parameter polytope is exact. Feasible rational polyhedra have rational witnesses of polynomial encoding length, so neither irrational physical roots nor tight capacity equality requires algebraic parameter output. Robust checks have the correct directions: maximize the lower-end evaluation and minimize the upper-end evaluation. A strict failed test gives a rational violating scenario. If incompatible scalar bounds cause an immediate rejection, any rational point of the promised nonempty original polytope violates their conjunction; this degenerate branch does not require an algebraic witness.

Individual arc extrema over the original or nonempty capacity-filtered global polytope remain instances of the root theorem. Rational shifts and signs preserve the local algebraic-degree bound. There is no claim that these extrema can be chosen independently. For example, two identical cycles sharing the same parameter can have `q_1=q_2` throughout their uncertainty domain, although both marginal intervals have positive width. The text expressly excludes transferring the independent flow box and coupled convex minimization to that globally correlated image.

### Independent cycle intervals and rational profile recovery

Joint continuity and strict root signs give continuity of the root map, including one-sided behavior at bracket endpoints. The image of each compact connected parameter polytope is therefore its whole closed interval. The product conclusion follows only after imposing independence between cycles.

For a rational target, both LP objectives and optimum values are rational. The displayed interpolation coefficient lies in `[0,1]`, and substitution gives exactly zero balance, including affine constant terms. The equal-value branch requires both values to be zero and is correctly handled. No inversion of a constitutive law or division by an edge flow is used.

Clipping is legitimate because each permitted capacity depends on at most one free circulation. A new endpoint is either an old algebraic endpoint with a stored rational profile or a rational clipping value recoverable by interpolation. Equality, rational singleton intervals, and inherited irrational singleton intervals are all covered. Parameter profiles need not be vertices after clipping. Rational linear objective optimization chooses endpoint signs cycle by cycle and hence requires no exact comparison of independent algebraic sums; only its additive value instruction needs R3-1.

### Convex minimization and exact final feasibility

The absolute monomial sums give valid rational value and gradient bounds with polynomial encoding length. Removing fixed coordinates avoids a false interior-ball assumption on a lower-dimensional box. The rational inner interval and frozen-coordinate construction covers intervals too narrow to contain the selected rational interior enclosure, including irrational singletons.

The projection from a feasible flow to the surrogate costs at most `2m eta` in one-norm. Returning from a surrogate point to feasibility changes only frozen coordinates and costs at most `m eta`; each affected edge changes by at most `eta`. Thus the surrogate remains inside the expanded flow box where the convexity promise and derivative bound apply. Recovery uses exact rational targets on retained intervals and stored exact endpoint profiles on frozen ones, so its capacity guarantee is exact.

I rederived the Lipschitz extension. The derivative of the perspective expression with respect to its scale is at least one, so partial minimization selects `t(z)`. The support calculation gives the stated subgradient because its multiplier `K` is positive. The choice of zero subgradient for `t` on the closed cube remains valid at the boundary; ties outside permit a signed active coordinate. Applying support inequalities in both directions gives the claimed global Lipschitz bound. Thus cube-only convexity suffices for a global convex value oracle after extension.

The rational affine composition evaluates the original dense polynomial without needing to expand a potentially much larger multivariate coefficient list. Polynomial degree controls the sizes of rational powers and oracle answers. The ellipsoid invocation has a rational centered cube, explicit radii, a global convex Lipschitz objective, and an exact rational value oracle. The cited theorem explicitly returns a rational point in the body. The total recovery loss `2mG_f eta+eps/2+mG_f eta<=11eps/16` is correct in both branches of the definition of `eta`. No root inverse condition number is invoked.

### Coupled convex performance hardness

I checked the triangle-chain topology, nomination placement, and split equation. Using distinct entry and exit vertices and bridges gives a simple cactus of maximum degree three. Each triangle has unit through-flow, direct resistance in `[1,16]`, and alternate total resistance four. The direct flow covers `[1/3,2/3]`; `z_i=3x_i-1` therefore realizes the full independent unit cube.

The sum of squared direct-flow differences is convex and equals Max-Cut on binary cube vertices. Coordinatewise endpoint selection establishes that some maximizing vertex exists. The objective's interaction graph is the input Max-Cut graph, distinct from the physical cactus; the proof does not impose a hidden degree bound on the objective.

The optimum is an integer. The half-integer robust bound gives the complement of integer-threshold attainment, and an absolute value error of one quarter permits exact integer recovery. Physical data are bounded constants and expanded objective data have polynomial magnitude, supporting strong hardness. Rational endpoint resistance choices and rational physical flows provide the claimed certificates only on the explicit family. The text does not infer general NP membership for algebraic performance comparisons.

### Fixed measurements and the new polynomial-law/capacity extension

I checked this proof directly, rather than treating the quadratic implementation as a proof of the extension.

For continuous polynomial-law polytopes, the preceding interval and recovery theorem supplies exactly the data the measurement algorithm needs: independently attainable constrained intervals, rational endpoint parameter profiles, local root degree at most the largest cycle law degree, and polynomial coefficient and isolation bounds. A rational clipped endpoint has degree one. Capacities do not introduce cross-cycle dependencies.

The measurement directions `a_C=RZ_C` remain rational. Algebraic interval lengths affect the selected measurement points but not the hyperplane arrangement. Scaling a strict sign witness gives the rational LP formulation with right-hand side one; feasible rational linear systems provide polynomial-bit representatives. Incremental insertion enumerates all nonempty strict sign regions in a polynomial count for fixed ambient dimension. Duplicate or dependent hyperplanes and zero-length segments cannot increase the bound beyond the claimed order.

A vertex of a lower-dimensional polytope still has an exposing cone with nonempty ambient interior. Choosing an exposing direction outside finitely many proper generator hyperplanes therefore selects its positive-length segment endpoints. Zero directions can be discarded, and zero-length segments may refine sign patterns without changing points. A point zonotope and absence of cycles are covered. Every candidate combines original rational endpoint profiles and therefore remains exactly admissible under local capacities.

In the finite quadratic model, I checked the earlier box-convex-hull theorem: independent finite scalar sets have a product convex hull, and each marginal endpoint is achieved by choices in the original lists. A box containing the finite measurement set contains its convex hull. Hence convex maximization can use those attainable projected vertices. This does not imply that capacity-filtered finite sets have the clipped interval hull; the theorem correctly excludes those filters.

The bounds `T_0` and `M_0` use absolute coefficients. Refining each selected circulation within `delta` changes each measurement by at most `M_0 delta`, stays in the enlarged derivative-bound box, and changes the objective by at most `eps/8`. Choosing the largest rational estimate loses at most `eps/4` in true value. Convexity is used only on the attainable zonotope; the enlarged box needs the derivative bound, not convexity. Dense degree and separately bounded univariate root encodings make each refinement and evaluation polynomial in input and accuracy bits. Multiplying by the arrangement candidate count gives the stated `N^{O(k)}` bound. Exact scenario maximization and exact candidate-value comparison are correctly left unclaimed.

Finally, rational PSD `LDL^T` elimination yields rational linear measurements without taking square roots. A zero PSD pivot has zero residual row and column, so the fixed-rank corollary covers singular matrices and the zero-rank case.

## Literature and dependency audit

I checked the relevant bibliography entries and the following primary sources. Comments in the bibliography about prior verification were not used as evidence.

- Aßmann, Liers, Stingl, and Vera: read the local original PDF, Section 4.3.3, Proposition 4.9, Lemma 4.10, and Proposition 4.11, printed pages 20–21. Its cycle function has the opposite sign convention, and the interval inequalities match after that reversal. The frozen bibliography specifies arXiv:1808.10241v1, matching the locator convention. The manuscript appropriately attributes the quadratic interval-to-halfspace mechanism. [Primary preprint](https://arxiv.org/abs/1808.10241v1).
- Onn and Rothblum: read the local original PDF, Section 2.1 and Section 2.2, including Lemmas 2.1–2.3, Algorithm 2.5, and Theorem 2.6. These support the classical fixed-dimensional zonotope and normal-direction mechanism; the separate algebraic lengths and original passive-network recovery are additional arithmetic work in this section. The bibliography states the arXiv locator version. [Primary preprint](https://arxiv.org/abs/math/0309083).
- Agrawal and Boyd: checked the author PDF's quasiconvex sublevel framework and Section 3 feasibility bisection. It supports the classical bisection attribution, not by itself the exact polynomial-root recovery theorem. [Author PDF](https://web.stanford.edu/~boyd/papers/pdf/dqcp.pdf).
- Megiddo: read Section 2 of the original author-hosted article. It solves ratio optimization through parametric linear optimization and exact recovery. The section's limited predecessor attribution is defensible; its dense nonlinear-root bit proof is supplied separately. [Author PDF](https://theory.stanford.edu/~megiddo/pdf/rational.pdf).
- Boyd and Vandenberghe: checked Sections 3.2.5–3.2.6, on partial minimization and perspectives. These are the relevant convexity operations for the displayed extension. [Author textbook](https://www.seas.ucla.edu/~vandenbe/cvxbook/bv_cvxbook.pdf).
- Dadush: checked Theorem 2.5.9 and the encoding conventions in Section 2.5.1 of the thesis. The theorem uses a centered convex body, weak membership, and a global Lipschitz convex value oracle; it returns a rational point in the body with an additive objective guarantee. Those are the hypotheses the section establishes. [Thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf).
- Del Pia, Dey, and Molinaro: checked the October 10, 2018 author manuscript, Section 1.1 and Corollary 2's binary Max-Cut expression. This matches the bibliography's version note. The similarly named local `literature/inbox/delpia2017.pdf` is a different paper, identified from its title and not used to support this citation. [Correct author manuscript](https://arxiv.org/pdf/1407.4798).
- Ferrez, Fukuda, and Liebling: the publisher page failed to open, but I found and read the author manuscript, revised April 29, 2004, especially its introduction and Section 3. It confirms the fixed-rank binary convex quadratic zonotope predecessor. The manuscript is accessible despite the bibliography comment recording an earlier retrieval failure. [Full author manuscript](https://www.cs.mcgill.ca/~fukuda/download/paper/qpzono040429.pdf).
- Basu, Pollack, and Roy: the local PDF's text encoding is corrupted. I rendered and inspected its contents and Chapter 10 opening pages, including the separation corollary and Section 10.2's isolation setup. I did not reread the full root-isolation complexity proof. Polynomial bit isolation, squarefree extraction, and refinement are standard imports here, and the section's own height and separation argument supplies the required uniform precision bound. [Book record](https://doi.org/10.1007/3-540-33099-2).
- Mignotte: direct access to the original 1974 PDF was unsuccessful. A primary research article by Hinek and Stinson explicitly restates Mignotte's Theorem 2 in a height-versus-Euclidean-norm form sufficient for the displayed `H_s` bound. I also checked the mathematical use of the bound; no questionable factor-size inference is needed. I do not claim direct verification of the original article's precise norm-one formulation. [Primary restatement](https://cacr.uwaterloo.ca/techreports/2006/cacr2006-15.pdf).

Earlier manuscript dependencies read were the passive model, existence, block and cycle lemmas, and output conventions in `01-preliminaries.tex`; the law-family definition and validation proposition in `04-laws.tex`; prescribed-flow realization and its finite-set hardness argument in `05-boundaries.tex`; and the full flow-region/scenario-versus-value theorem and proof in `06-weighted.tex`. I also inspected `07-weighted-cactus.tex` while locating the latter dependency; its unrelated weighted-envelope claims are not needed for this verdict.

## Diagnostics and review limits

I ran a short direct Python diagnostic with exact SymPy and Fraction arithmetic, using `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python`:

- For the correlated cubic cycle equation `(1+t)q^3-(2+t)(1-q)^3`, `t in [0,7]`, the rational target `q=6/11` gives LP endpoint evaluations `-34/1331` and `603/1331`. The manuscript's interpolation returns the exact original parameter `t=34/91` and zero cycle residual.
- For a two-dimensional arrangement with repeated opposite directions, a zero direction, and a zero-length nonzero direction, exact rational slope enumeration produced eight sign regions and eight candidate points. A convex quadratic's maximum over those candidates equaled its maximum over all sixteen distinct box-corner images, exactly `126`.
- Exact symbolic identities checked nonodd reorientation and binomial translation through degree seven.

These are diagnostics of concrete boundary patterns, not proofs of the universal results. The universal conclusions above come from the proof audit. No shared manuscript build, full algorithm implementation, or numerical performance study was run.

I followed the supplied global AGENTS instructions and the S5a reviewer instructions. No applicable filesystem AGENTS file was found along the worktree's ancestor path or within the worktree. I did not read author, lead, build-check, adjudication, correction, peer, or historical review reports; I did not consult result-status assertions. I did not spawn agents or edit manuscript sources. Only this assigned review report was written in the repository; extraction and image diagnostics used `/tmp/s5a-r3`.
