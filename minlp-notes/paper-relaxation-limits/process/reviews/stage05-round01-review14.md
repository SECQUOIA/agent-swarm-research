# Stage 5, round 1: independent review 14

**Verdict: PASS.** No major or minor defect found. The order-one lifted lower bound and the separate order-one upper certificate are valid under the stated full-box quadratic moment oracle. The source comparisons preserve the distinctions among continuous covers, integer refutations, and their objective thresholds.

## Coverage

I read all of the frozen files below, including every theorem and proof:

- `process/snapshots/stage05-round01/sections/13-xor-quadratic-hulls.tex`, lines 1–333.
- `process/snapshots/stage05-round01/sections/14-monomial-reformulations.tex`, lines 1–228.
- `process/snapshots/stage05-round01/sections/15-finite-certificates-affine.tex`, lines 1–218.

The shared dependencies read were the foundation and certificate conventions in frozen `sections/01-foundations.tex`, lines 1–195; all of frozen `sections/11-coordinate-domains-lifts.tex`; all of frozen `sections/12-relative-blocks-cuts.tex`; frozen `macros.tex`; and the four Stage 5 entries in frozen `references.bib`. The unrelated bilinear theorems later in file 01 are not dependencies of this review. I checked the earlier vertex-law argument, local-oracle contract, coordinatewise interpolation boundary, and the explicit clique-cut escape argument directly. I did not re-audit the earlier fractional-cardinality source theorem, which Stage 5 does not use as an input to its new lower bound.

I read `process/review-protocol.md`, both Stage 5 assignments, the full author ledger `process/stage-05-author.md`, focus 14 in `process/stage05-reviewer-focus.json`, `process/order-one-monomial-refinement.md`, the scope proposal, and the frozen primary-source record. I read all three complete canonical sources and all four mapped correction audits, relative to the repository root:

- `results/spatial-bb-quadratic-cut-exponential-lower-bound.md`.
- `results/spatial-bb-monomial-lift-exponential-lower-bound.md`.
- `notes/spatial-bb-affine-branching-barrier.md`.
- `notes/review-spatial-bb-beyond-clique.md`.
- `notes/review-spatial-bb-beyond-clique-second.md`.
- `notes/review-spatial-bb-bounded-monomial-lift.md`.
- `notes/review-spatial-bb-affine-branching-barrier.md`.

Those older audits were read for corrections and coverage, not treated as proof. I read no peer report from the current review round, delegated no work, and made no manuscript edits.

## Findings

None requiring repair. In particular, the source's constant-vector typographical error is not reproduced in the manuscript; the source parameter boundary is avoided; the fixed-gap conclusion is not inferred from a satisfiability refutation; and the newly promoted order-one statements do not silently use cubic node moments.

## Independent verification

### Transfer, local constraints, and genuine quadratic moments

In file 13, lines 85–146, fixing every endpoint-restricted coordinate to a contained witness gives a normalized functional by literal substitution. No pseudo-conditioning is required. If a localizer has generator-degree sum `a` and square-multiplier degree `d`, then `a+2d<=2r`. Endpoint interpolation expands each nonconstant univariate factor into nonnegative multiples of endpoint indicators. At most `a` such factors occur. Their product `I` is idempotent after Boolean reduction, including repeated or inconsistent factors, and

`I P^2 = (I P)^2`, with `deg(IP)<=a+d<=2r`.

Both expressions are available through original degree `4r`. Local equalities vanish at the fixed witness or both endpoints, and multiplication preserves their zero Boolean reduction within the stated budget. Marginalizing a genuine degree-two Boolean law and fixing the restricted coordinates realizes every resulting first, diagonal, and cross moment inside the actual coordinate product. This remains true for nonclosed sets because the law has finite endpoint support.

An unaffected clause retains zero pseudo-cost. A changed clause has cost in `[0,1]` by positivity of `(1±chi_A)^2`; degree six is available. There are at most `Delta|R|` changed clauses. Certification therefore requires `|R|>=m T_*/Delta`. A witness-containing product has exactly one allowed Boolean endpoint in each restricted coordinate and both elsewhere, so its witness fraction is `2^{-|R|}`. The union bound applies to overlapping arbitrary covers and gives the claimed lower count. The charged-cover convention prevents free deletion of feasible regions from evading this argument.

The signed realization lemma correctly includes the constant Gram vector. Entries of absolute value one identify equal or opposite unit vectors; other classes are orthogonal. Fix the constant class to one and use independent unbiased signs for the other classes. The prescribed means and every pair moment follow, including negative orientations and deterministic coordinates.

### Width, existence, normalization, and constants

In file 13, lines 187–243, closure under bounded-width XOR resolution gives a unique sign for each derived support, since opposite signs derive the empty contradiction. On supports of size at most `floor(w/2)`, the relation defined by derivability of the symmetric difference is transitive: the resulting difference still has size at most `w`. Signed class vectors consequently give the entire character Gram matrix. Its quadratic form proves positivity for arbitrary polynomial squares, not merely polynomials on one small variable subset. Directly defining moments through `w` also handles odd widths; positivity stops at `floor(w/2)` as required.

The density-eight specialization has a positive width constant from Theorem 11. With `k=3`, `gamma=delta=1/4`, and density exponent zero, the denominator is `1/4` and the density condition is `8>=1+8 log 2`. Shrinking the width constant absorbs integer rounding. The manuscript does not rely on the non-strict constant notation in Theorem 12 to establish positivity of that constant.

The random-sign count is binomial for each fixed assignment even when supports overlap. The displayed exponential-moment calculation gives `Pr(V<=2n)<=exp(-n)` at `t=1`, so a union over assignments fails with probability at most `exp(-(1-log 2)n)=o(1)`. For each occurrence count, differentiating its binomial generating function gives `E[D_i 2^{D_i}]=48(1+3/n)^{8n-1}`. The deletion bound and Markov therefore need no independence between occurrence counts or between the events. The union of failure events has probability less than one for every sufficiently large `n`.

After at most `n` deletions, `7n<=m<=8n`, every retained degree is at most 64, and every assignment violates at least `n` retained clauses. Multiaffinity gives the same continuous optimum, at least `1/8`. Restricting the same source functional to smaller degrees proves simultaneous orders. Both tolerance targets are at least `1/16`, so the exponent is `7n/(16·64)=7n/1024`. The derivative and symmetric-Hessian row-sum bounds in lines 315–330 count respectively one and two contributions per incident clause and have the stated normalization.

### Lifted order one, graph identities, and parity rank

In file 14, all lifted polynomials of degree `2r` pull back within `2rD`. In a localizer, the parity-indicator product and multiplier have degrees at most `Da` and `Dd`, respectively. Their square therefore needs at most `2D(a+d)<=4rD`. This proves the complete stated preordering even for repeated or overlapping parities. Every allowed graph-identity product vanishes as a literal polynomial after pullback within degree `2rD`.

A lifted linear square pulls back to a square of degree at most `D`, so the augmented quadratic matrix is PSD. Each of its entries is a signed original character moment on at most `2D` coordinates; all diagonal entries equal one. The signed realization lemma supplies a Boolean law. Each restricted lifted coordinate has endpoint mean, forcing that coordinate almost surely and placing this law in the full node product. The law need not be graph-supported. The graph identities were separately verified for the polynomial functional.

The objective identity survives substitution exactly. The sufficient condition `rD>=2` makes square degrees up to six available, so the clause-cost argument remains valid at `r=1`. No other step needs `r>=2`. The original formulation still needs `r>=2` to evaluate its cubic objective. For the quadratic formulation, `D=3`, the objective is linear, and source width `12r` suffices, including `r=1` for large `n`.

The parity equations of a witness-containing node are consistent. A row basis has exactly the same support union as all rows, since a column absent from the basis is absent from its span. Thus `|C|<=D rank(A_R)` and the exact witness fraction `2^{-rank(A_R)}` gives the claimed exponent. Repeated restrictions cannot falsely increase rank. The counts `N=n+2m<=17n`, `7n/3072`, and `7N/52224` are correct. The degree/region tradeoff is necessary only within `4rD<=an`, and its polynomial-count claim is explicitly in original dimension.

### Both upper certificates and affine obstructions

The order-two Bernstein expansion in file 15 uses all eight corners and products of three normalized slacks. Its coefficients are nonnegative by the definition of the clause minimum. Clause oscillation is at most `3h/2`, and `h=2/ceil(3/epsilon)<=2epsilon/3`, including `epsilon>=3`. The graph-transfer identity has degree three and is available at order two.

At order one, the full-box law and the two graph equations on moments give

`|L[v]-a_i a_j a_k| <= |E[u(x_k-a_k)]| + |a_k| |E[x_i x_j]-a_i a_j| <= h+2h`.

Every expectation here has degree at most two. This bounds the clause cost by its lower-corner value minus `3h/2`. The displayed quadratic `q_e` is nonnegative on the full box by the same pointwise estimates, and its identity with the clause cost uses only the two quadratic graph equations with constant multipliers. Thus the `M^n` bound and `48^n` specialization do not assume hidden cubic moments or pointwise graph equations for the law.

For the affine halfspace, zero mean of a nonnegative random variable `S` would force zero second moment, contradicting `E[S^2]=n`. Symmetry gives witness mass at least one half. For the substitution obstruction, `t<min(r-1,ceil(n/2))` gives at least `t+1` unfixed coordinates. Selecting `a+1` negative signs gives an admissible indicator of degree at most `r-1` and exact localizer value `-2^{-(a+1)}`. The `r=1` conclusion is correctly vacuous. These are method obstructions and do not establish a stronger branching lower or upper bound.

### Primary sources and focus-14 comparison audit

I read `../literature/AGENTS.md` before accessing originals. All four primary PDFs were accessible. Independent SHA-256 calculations matched every digest in the frozen `verification/stage05-primary-sources.json`. Text extraction and page renders are under `verification/reviewer14/stage05-round01/`.

- **Schoenebeck:** the full 19-page author version at `/tmp/minlp-relaxation-limits-sources/schoenebeck-full.pdf` was read, with detailed checking of the random model, Definition 10, Theorems 11–12, the full Lemma 13 construction, and the appendix width argument. Printed pages 7, 8, 10, and 11 were also visually inspected. Its normalized constant vector has squared norm one despite the subsequent printed norm-zero typo. The manuscript's theorem numbering and author-version designation are correct. The [author PDF](https://schoeneb.people.si.umich.edu/papers/LasserreNew.pdf) was also accessible through the web tool.
- **Ahmadi–Dash–Hua–Stellato:** I directly read the abstract and introduction, Definitions 1–2, Theorem 1, and Sections 6.1–6.2 including both algorithms, from `../literature/papers/ahmadi2026-disjunctive-sum-of-squares/original.pdf`; printed page 32 was visually inspected. Their polynomial algorithm uses simplicial cones intersected with the sphere and a fixed-degree SOS bounding problem. The matrix version uses simplices and its stated semidefinite inner approximation. The stopping test uses tolerance times `1+|L|+|U|`. File 15 claims only their positive-tolerance termination statement, not an identical absolute-tolerance convention or a lower bound for those algorithms. [Version 1 metadata](https://arxiv.org/abs/2605.28674v1) agrees with the bibliography.
- **Beame et al.:** I read the abstract and introduction through the main result statements and related/subsequent-work discussion in `/tmp/stage05-author-sources/stabbing.pdf`; PDF page 4, printed page 3, was visually inspected. Theorem 1 is quasipolynomial size. Integral coefficients and thresholds justify discarding the open slab between integer negations. The manuscript neither calls this polynomial size nor transfers its region rule to a continuous cover. [Version 3 metadata](https://arxiv.org/abs/1710.03219v3) confirms the 2023 version; the bibliography also records the preliminary ITCS 2018 version.
- **Fleming et al.:** I read the abstract and introduction through Theorems 1.1–1.5 in `/tmp/stage05-author-sources/branch-cut.pdf`; PDF page 5, printed page 4, was visually inspected. Theorem 1.3 measures the CNF encoding and gives size `|F|^{O(log m)}`. Theorem 1.4 concerns the coefficient-restricted subsystem `SP*`. File 15 retains both qualifications. [Version 2 metadata](https://arxiv.org/abs/2102.05019v2) matches the bibliography.

The final threshold comparison is correct: perfect unsatisfiability gives at least one violated Boolean clause, hence normalized `1/m`; multiaffinity extends that lower bound to the cube, but does not strengthen it to `1/16`. Nothing in the inspected source statements supplies the missing constant-gap inference.

### Independent exact checks and presentation

`verification/reviewer14/stage05-round01/check_identities.py`, run with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python`, writes `independent-checks.json` in the same directory. It independently checks the order-one cut identity, the cubic graph identity, and the complete Bernstein interpolation identity symbolically, together with exact rational/integer checks of deletion sufficiency, all displayed exponents, and grid base 48. I also checked an explicit 16-point full-cube law: take independent uniform `x_i,x_j,x_k,u` and set `v=u x_k`. Both graph equations hold in expectation, while eight support points violate `u=x_i x_j`. This illustrates why moment graph equations do not imply graph support. It is not evidence for the asymptotic lower bound.

I visually inspected frozen manuscript pages 73 and 75, covering the upper-certificate statements and the source comparison. They are legible, with no clipping or unresolved citation visible. I did not rerun the author's build or adopt the author's finite-check counts as my own. An unavailable optional Python PDF-rendering module was bypassed with `pdftoppm`; no source access remained blocked.

## Remaining limits

This review does not establish priority or exhaust the literature. It checks the inspected comparison statements rather than every proof in the three comparison papers. The external linear-width theorem remains a cited primary mathematical input; the manuscript's degree conversion is independently proved. The exact quadratic-box-hull oracle is not asserted tractable, and the stronger coupled-cut and affine-branch models remain outside the lower bounds. These are explicit scope limits, not defects.
