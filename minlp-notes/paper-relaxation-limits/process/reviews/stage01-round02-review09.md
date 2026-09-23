# Stage 1, round 2 — reviewer 09

**Verdict: PASS.** No substantive major or minor finding.

## Coverage

I read the entire frozen manuscript in `process/snapshots/stage01-round02/`: `main.tex`, `macros.tex`, `references.bib`, `sections/01-foundations.tex`, and `sections/appendix-finite-signings.tex`. I also read the frozen `verification/check_complete_signings.py` and independently replayed the actual program printed in the appendix.

I read `process/review-protocol.md`, the round-2 assignment, `process/stage01-round01-adjudication.md`, `process/stage01-corrections.md`, and the Stage 1 scope and shared-dependency requirements in `process/scope-proposal.md`. The canonical mathematical dependencies read were `results/mccormick-gap-degeneracy-bound.md`, `results/mccormick-hereditary-density-characterization.md`, and the preliminary deficiency, independence, and nonnegative-box-transfer sections of `results/positive-multilinear-degree-upper-bound.md`. These paths are relative to the repository root except the process and frozen-manuscript paths, which are relative to `paper-relaxation-limits/`.

After reading `literature/AGENTS.md`, I inspected the relevant primary-source passages:

- `[[luedtke2012-some-results-on-the-strength]] p.5-9` and `p.15`: recursive single-product exactness and its general-box limitation, vertex distributions, common upper attainment, the nonnegative-box condition, and the coloring bound. I checked the important formulas against direct text extraction from the original PDF on pages 8–9 and 15. The [exact author manuscript named in the bibliography](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf) opened successfully and has 23 pages.
- `[[boland2017-bounding-the-gap-between-the]] p.1-6` and `p.10-12`: the dimension bounds, half-integral cut identities and upper implication, the signed-cycle criterion and its predecessor attribution, and the relevant bibliography. Original PDF pages 3–6 confirm the theorem numbers, constants, and cut formulas.
- `[[davidson2007-norms-of-schur-multipliers]] p.1-9` and `p.11-12`: Theorems 1.2 and 2.4, their norm conventions, the continuous weighted theorem versus the rounded pattern theorem, and the relevant upper-bound argument. I checked the original PDF text on pages 4–7 because the knowledge-base extraction omits displayed equations. The [author-hosted paper](https://www.math.uwaterloo.ca/~krdavids/Preprints/DavDon_schur.pdf) was also retrievable.
- `[[mccormick1976-computability-of-global-solutions-to]] p.1-2`: the historical statement about factorable functions, convex underestimators, and successive subdivision.

The [publisher record for Szarek](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/58/2/101277/on-the-best-constants-in-the-khinchin-inequality) confirms the title, volume, year, pages, and DOI in the bibliography. Its full-PDF download returned 403, as did the EuDML page; I therefore did not directly audit Szarek's original proof. I did not inspect the Misener–Smadbeck–Floudas predecessor directly. The manuscript correctly makes that attribution through Boland et al. No other round-2 report was read.

## Findings

None. The earlier accepted repairs are complete within the assigned stage:

- The finite full-center constants and all-face constants are now both present, with different definitions, a complete finite search, and witnesses. The analytic restriction/extension proof identifies exactly which maximum the search determines.
- Absolute and relative tolerance ranges make the target monotonicity assertion correct; granting the best incumbent under this relative convention now requires a positive optimum.
- Exact factor-one statements use nonempty effective support, and the empty-support and Sidon conventions are consistent.
- The Luedtke manuscript is precisely retrievable; the cycle predecessor is acknowledged without pretending to have directly inspected it; and the introductory upper-attainment statement now has the required nonnegative-box qualifier.

The introduction and Schur subsection appropriately limit novelty. In particular, they identify the density order as an implication of prior theory, distinguish the explicit elementary constant from a new graph-norm principle, and do not claim that four is the best constant in all earlier literature. Citing Luedtke et al. as a source for a statement expressly called classical does not claim that they originated every underlying envelope fact.

## Independent verification

**General arguments.** I checked the vertex-law proof, the circle construction for the lower product envelope, the deficiency identity, the two independence cases, and the direction of the original-versus-expanded termwise-gap inequality. These constructions preserve every specified mean. The affine transformation introduces only affine extra terms for signed bilinear functions, so the arbitrary-box transfer is valid.

For the induced-cut characterization, the balanced pair of opposite sign vectors gives `H = R_W/2` and `T = L_W/2`. The active-equality argument for the arrangement cells covers fixed coordinates, odd complementation cycles, and free components; the latter cannot occur at a cell vertex. Convexity of `T-cH` on a cell therefore proves the global inequality, including boundary points.

Polarization gives `Q(s)-Q(t)=2 v^T A u` on complementary supports, so the cut-range identity has the right factor. Conditional on the cited sharp Khinchin inequality, the locally maximal squared-weight cut gives `R >= (1/4) sum_i ||a_i||_2`. Fractional orientation then yields `L <= sqrt(rho) sum_i ||a_i||_2`, proving the stated constant four. Degree and bipartite specializations, their induced-subgraph use, and the frustrated four-cycle equality case are consistent.

The random-sign estimate counts `2^h` exponential terms after fixing one vertex sign and allowing both signs of Q. Optimizing its bound gives `sqrt(2mh log 2)`. Restriction to a densest induced graph and extension to full support establish the per-graph quantifiers. Compactness on `L=1` and continuity of the full-center ratio suffice for the nonzero-coefficient supremum; continuity of `c*` is not needed.

For the prior-art transfer, the symmetric pattern has `beta(P)=rho(G)`. The pairing counts each edge twice, while polarization yields `||A||_(infinity to 1) <= 4R`. Combining these with the weighted Schur upper bound and the projective-norm inequality gives exactly `L <= 4 K_G sqrt(rho) R`. The real convention is consistent with the source's real Grothendieck formulation. The Sidon comparison and its bipartite equality follow from mean zero and sign reversal in one vertex part.

**Exact finite computation.** My independent checker is `verification/reviewer09/round02/check_signings.py`, with output in `check_signings.json`. It evaluates Q through an integer character matrix, independently of the appendix's cut-mask/population-count calculation. All matrix entries are integers and every Q value has absolute value at most 21, so the int64 calculation cannot overflow. It also executes the verbatim frozen appendix program with Python integers.

The minimum cut ranges for K2 through K7 were `[1, 2, 4, 4, 5, 8]`. The K5, K6, and K7 complete histograms were respectively `{4:12, 6:52}`, `{5:12, 7:180, 8:390, 9:442}`, and `{8:3240, 10:20664, 12:8864}`. Representative counts agree with `2^((n-1)(n-2)/2)`. Switching to a positive root star is unique up to the globally trivial switch, so these representatives cover every switching class.

Direct scalar evaluation gives the displayed witness extrema `(-1,3)`, `(-2,6)`, `(-4,4)`, `(-5,5)`, and `(-7,9)`. Extending the K6 witness by positive edges gives `(-9,11)` on K7 and retains `(-5,5)` on its six-vertex face. These yield center ratio `21/10` and face ratio three. The identity `F_n = max_{2 <= k <= n} M_k` follows analytically from restriction and extension, and therefore gives the listed all-face optima. These are exact finite results, not evidence for an unproved general-n formula.

## Remaining limits

I did not rebuild or visually inspect the frozen PDF; this report concerns its full TeX content, mathematics, source claims, and finite calculation. Szarek's sharp inequality remains an externally cited input whose original proof was inaccessible in this review. I made no comprehensive new priority search and no direct claim about the unread cycle predecessor. Larger-n full-signing optima, arbitrary-real finite optima, and optimal universal constants remain outside the finite computation's conclusions. The unwritten later stages are outside this gate.
