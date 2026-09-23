# Stage 1, round 2 — reviewer 06

**Verdict: PASS.** No substantive major or minor finding. The accepted round-1 repairs are present, and the restored finite computation establishes the stated finite full-signing results. The convex geometry, cut characterization, and norm transfer are consistent with the distinctions between the relaxation models.

## Coverage

I read all frozen manuscript text under `process/snapshots/stage01-round02/`: `main.tex`, `macros.tex`, `references.bib`, `sections/01-foundations.tex`, and `sections/appendix-finite-signings.tex`. I also read the frozen `verification/check_complete_signings.py`, inspected the manifest, and visually inspected PDF pages 11–12 containing the printed program, witnesses, and bibliography. All 19 files recorded in the frozen manifest match their recorded SHA-256 hashes.

I read `process/stage-01-round02-review-assignment.md`, `process/review-protocol.md`, `process/stage01-round01-adjudication.md`, `process/stage01-corrections.md`, and the Stage 1 coverage and common dependencies in `process/scope-proposal.md`. The canonical mathematical dependencies reviewed were:

- `results/mccormick-gap-degeneracy-bound.md`, including its separate degeneracy proof, bipartite refinement, finite examples, and scope qualifications.
- `results/mccormick-hereditary-density-characterization.md`, including the full-support perturbation argument and Schur-multiplier transfer.
- The foundation, deficiency, independence, and nonnegative-box arguments in `results/positive-multilinear-degree-upper-bound.md` (I also read the remainder of this note; its later degree bound is outside the frozen stage).

After reading `literature/AGENTS.md`, I checked the relevant primary-source passages:

- `[[luedtke2012-some-results-on-the-strength]] p.4-9` and `p.15`: recursive product relaxations, vertex laws, common upper attainment and its domain, and the coloring bound. Important equations and theorem numbers were checked through direct text extraction from `original.pdf`, including pages 8–9 and 15 of the specified 23-page manuscript.
- `[[boland2017-bounding-the-gap-between-the]] p.1-6`, `p.10-12`: definitions, Lemma 1 and Corollary 1, the older dimension bound, cycle exactness, and the stated Misener–Smadbeck–Floudas predecessor. I checked the central formulas and predecessor statement against the original PDF.
- `[[davidson2007-norms-of-schur-multipliers]] p.1-7`: norm definitions, Theorem 1.2 and the real constant convention, and the distinction between integer-pattern Theorem 2.3 and weighted-matrix Theorem 2.4. I checked the displayed inequalities using original-PDF extraction, since the stored fulltext omits several displayed formulas.
- `[[mccormick1976-computability-of-global-solutions-to]] p.1-3` for the introductory historical statement and region-bound framework; no new theorem in this manuscript depends on an unread part of that source.

The [publisher page for Szarek's article](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/58/2/101277/on-the-best-constants-in-the-khinchin-inequality) confirms its bibliographic metadata. The publisher PDF download and EuDML access returned HTTP 403. I therefore did not inspect Szarek's original proof; I treated the sharp real Khinchin inequality as the stated classical external input. I did not inspect the Misener–Smadbeck–Floudas original, and the manuscript accurately identifies its attribution as indirect through Boland et al. I read no other round-2 report and edited no manuscript file.

## Findings

None requiring repair.

The earlier accepted issues are resolved: nonnegative absolute tolerance and the relative range are explicit; granting the best incumbent under the stated relative normalization requires positive optimum; all exact-factor-one assertions exclude empty effective support; the empty Sidon quantity is defined; the introduction restricts positive common upper attainment to nonnegative boxes; the Luedtke manuscript version is specified; and the cycle predecessor is credited without claiming direct inspection.

## Independent verification

### Geometry and relaxation models

For a multiaffine function, independent endpoint sampling puts every graph point in the vertex graph polytope. Its compact vertical sections give the two optimizing vertex-law formulas. Finite polyhedral lower and upper surfaces justify the claimed piecewise-affine continuity, including box boundaries. At a fixed mean, separate scalar graph hulls allow independent choices of each factor's vertical value, so their summed width is exactly the displayed termwise gap. This differs from requiring one joint law for the sum.

The monomial lower-envelope construction on the circle preserves each failure marginal even when consecutive intervals wrap; their union covers the circle once their total length reaches one. The common-threshold law simultaneously attains the upper endpoints of all positive monomials. Thus the deficiency identity has the correct maximizing direction. The independent-law estimate handles its stated two cases, including zero deficiency at endpoints.

The positive-box transfer correctly retains equality for the full gap and only an inequality for the original versus expanded termwise gaps. It does not assume that expansion preserves incidence structure. The warning about recursive McCormick relaxations is supported by the single-product positive-box counterexample in the Luedtke source. The certificate definition separately counts regions certified by the specified oracle; it makes no inference from a scalar vertical-gap ratio to a constrained objective ratio or tree bound.

### Induced cuts and density

At a half-valued face, the symmetric law on an extremizing sign vector and its negative has all required means and gives `H = R_W/2`; the exact term widths give `T = L_W/2`. Fixed coordinates equal to one contribute only affine terms on the active face. The arrangement argument covers every cell vertex: a component of active equality/complement relations either has a fixed value, is forced to one half by odd complementation parity, or permits a perturbation and cannot define a vertex. Since `H` is concave and `T` is affine on each cell, `T-cH` is convex there for every `c >= 0`. The extension from cell vertices is valid.

I independently checked the polarization constants: `Q(s)-Q(t)=2 v^T A u`, hence maximizing half the difference gives the rectangular infinity-to-one norm across a partition. The sharp Khinchin row estimate and a locally maximal squared-weight cut give `R >= (1/4) sum_i ||a_i||_2`. The fractional-orientation network has minimum relevant cut capacity `m-|E(U)|+t|U|`, so its least feasible uniform vertex load is precisely the induced density. Summing weighted Cauchy–Schwarz counts each absolute edge weight once. This yields the stated density constant 4; the degree and bipartite constants also have the stated factors of two.

The random-sign estimate counts `2^(h-1)` sign vectors and both signs of the exponential, giving `h log 2`, not an independence assumption across configurations. Restriction and extension preserve the witnessing face. The whole-graph supremum proof legitimately zeroes coefficients, then uses continuity of the full-center ratio on the nonzero coefficient sphere to recover the full-support supremum. It does not require continuity of `c*` as support disappears.

### Schur transfer and duality

For the symmetric adjacency pattern, counting an edge twice only when both endpoints lie in `R intersect C` gives `beta(P) <= rho_G`; taking equal densest row and column sets gives equality. The projective-norm pairing is

`2L = <A, sign(A)> <= pi(sign(A)) ||A||_(infinity->1)`.

With `p=(u+v)/2`, `q=(u-v)/2`, the identity `u^T A v=2[Q(p)-Q(q)]` and multiaffinity imply `||A||_(infinity->1) <= 4R`. Combining this with the real Grothendieck bound and weighted-pattern upper bound gives exactly `L <= 4 K_G sqrt(rho_G) R`. No assertion about convex lift size follows or is made. The mean-zero and bipartite arguments for the Sidon comparison also have the correct constants.

### Exact finite verification

I wrote `verification/reviewer06/round02/check.py`. It independently enumerates normalized signings in Gray-code order and updates the **quadratic values** directly with exact integers. It does not use the manuscript's cut-mask formula. It also executes the verbatim printed appendix program and directly evaluates every displayed witness on every induced face. The output is `verification/reviewer06/round02/checks.json`.

| n | Representatives | Minimum R | M_n |
| --- | ---: | ---: | ---: |
| 2 | 1 | 1 | 1 |
| 3 | 2 | 2 | 3/2 |
| 4 | 8 | 4 | 3/2 |
| 5 | 64 | 4 | 5/2 |
| 6 | 1024 | 5 | 3 |
| 7 | 32768 | 8 | 21/8 |

All witness extrema agree with the table. For K7 the exact range histogram is `{8: 3240, 10: 20664, 12: 8864}`. The extended K6 witness has quadratic extrema `(-9,11)`, center ratio `21/10`, and maximum face ratio `3`. The printed program returns `[1,2,4,4,5,8]`.

Switching normalization is complete and unique because a switching preserving every positive root-star edge has equal signs at all vertices and changes no coefficient. The all-face formula `F_n = max_(2<=k<=n) M_k` follows analytically from restriction and extension, so the finite search need only optimize full centers. The appendix's initial range bound is valid: the difference of two cut weights is a sum of at most `binom(n,2)` signed coefficients with multipliers in `{-1,0,1}`. The computation is an exhaustive exact verification of these finite instances, not merely numerical evidence from selected witnesses.

## Remaining limits

I did not rebuild the PDF or audit later-stage scripts that happen to be included in the frozen manifest. The new appendix is readable and unclipped in the inspected PDF pages. The universal proofs were checked mathematically, not formally verified by a proof assistant. The finite enumeration establishes no formula for larger complete graphs and no exact arbitrary-real-coefficient extremum. The sharp Khinchin input and indirect predecessor source have the access limits stated above. None of these limits creates an unresolved defect in the scoped Stage 1 manuscript.
