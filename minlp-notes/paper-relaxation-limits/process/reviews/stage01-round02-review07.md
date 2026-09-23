# Stage 1, round 2, review 07

**Verdict: PASS.** No major or minor defect identified in the assigned stage. The accepted round-1 repairs are present and mathematically consistent. The new finite results have a complete enumeration argument and reproducible exact output.

## Coverage

Read the complete frozen manuscript under `process/snapshots/stage01-round02/`: `main.tex`, `macros.tex`, `references.bib`, `sections/01-foundations.tex`, and `sections/appendix-finite-signings.tex`. Read the frozen `verification/check_complete_signings.py`, its recorded output, and the manifest. My checker verifies every manifest hash; it does not write into the snapshot.

Read the assignment, `process/review-protocol.md`, `process/scope-proposal.md` including all Stage 1 coverage rows, `process/stage01-round01-adjudication.md`, and `process/stage01-corrections.md`. Read the three canonical dependencies `results/mccormick-gap-degeneracy-bound.md`, `results/mccormick-hereditary-density-characterization.md`, and `results/positive-multilinear-degree-upper-bound.md`. Consulted their earlier correction context in `notes/audit-mccormick.md`, `notes/review-mccormick-density.md`, `notes/review-mccormick-hereditary-density.md`, and the final Schur update in `notes/sidon-gap-novelty.md`. No other round-2 review was read.

After reading `literature/AGENTS.md`, checked relevant primary-source sections:

- `[[luedtke2012-some-results-on-the-strength]] p.8-9` for vertex envelopes, Theorems 4–5, and the nonnegative-box condition; `p.15` for Theorem 8. Also read the recursive-relaxation counterexample discussion immediately before Section 3. Re-extracted the important formulas on pages 8–9 directly from the original PDF. The specifically identified [23-page author manuscript](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf) is accessible.
- `[[boland2017-bounding-the-gap-between-the]] p.3-6` for the signed cut identities, the 600 square-root-dimension bound, and the half-integral reduction; `p.10-12` for the cycle criterion and predecessor attribution. The [arXiv source](https://arxiv.org/abs/1507.08703) is accessible.
- `[[davidson2007-norms-of-schur-multipliers]] p.3-7` for the Schur factorization, projective norm inequality, and the weighted theorem. Re-extracted pages 4–7 from the original PDF because the stored Markdown loses displayed equations. The [author PDF](https://www.math.uwaterloo.ca/~krdavids/Preprints/DavDon_schur.pdf) is accessible. Its online pagination differs from the local original; the local page locators above refer to the package.
- Verified Szarek's publication metadata at the [publisher page](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/58/2/101277/on-the-best-constants-in-the-khinchin-inequality). Its PDF download returned HTTP 403; I did not inspect that original proof. The sharp real Khinchin inequality is treated as the stated classical input. I did not inspect the Misener–Smadbeck–Floudas original or McCormick's original paper.

## Findings

None requiring repair. The following checks explain the PASS rather than relying on earlier reviewer verdicts.

## Independent verification

### Computational proof and exact outputs

The independent checker is `verification/reviewer07/round02/check.py`; results are in `verification/reviewer07/round02/results.json`. It uses Python unbounded integers and `Fraction`, with no floating-point arithmetic or optimization solver.

I extracted and executed the literal program printed in the frozen appendix. It returns `[1, 2, 4, 4, 5, 8]` for K2 through K7. I then independently enumerated quadratic values, using a Gray-code traversal of coefficient signings and the update `Q_new(s) = Q_old(s) - 2 a_ij s_i s_j` for the changed edge. This does not reuse the appendix's cut-mask/population-count evaluation. The complete histograms agree with the frozen output:

| n | Representatives | Range histogram, written range:count |
| --- | ---: | --- |
| 2 | 1 | 1:1 |
| 3 | 2 | 2:2 |
| 4 | 8 | 4:8 |
| 5 | 64 | 4:12, 6:52 |
| 6 | 1024 | 5:12, 7:180, 8:390, 9:442 |
| 7 | 32768 | 8:3240, 10:20664, 12:8864 |

For n through 5 I additionally enumerated every signing without normalizing the root star. Each histogram count is exactly `2^(n-1)` times its normalized counterpart. This is an extra finite check of switching, not a substitute for the switching proof.

The proof of enumeration completeness is correct: multiplication by vertex signs permutes all arguments of Q; a positive root star fixes the switching class uniquely, since its stabilizer consists only of the two constant vertex sign vectors; fixing one vertex sign loses no Q value. The program's cut weight `c-2h` is exact. Its initializer exceeds every possible cut range, because a difference of two cuts has coefficient multipliers in {-1,0,1}. Thus the computation establishes both a lower bound on every candidate range and an attaining candidate, rather than recording only a good example.

Direct quadratic evaluation on every induced face verifies all five printed witnesses. Their full-center extrema are respectively `(-1,3)`, `(-2,6)`, `(-4,4)`, `(-5,5)`, and `(-7,9)`. The extended K6 witness has full-center extrema `(-9,11)`, ratio `21/10`, and maximum face ratio 3. Exact division gives the stated M sequence. Restriction of a full signing to a k-vertex face and arbitrary extension in the reverse direction prove `F_n = max_{2 <= k <= n} M_k`; the F sequence therefore follows without any unperformed search over continuous points.

### Analytic arguments throughout the stage

The vertex-law proof works at boundary points and after removal of fixed coordinates. The single-product failure intervals preserve the individual failure measures even when they wrap around the circle. The common-threshold law attains all positive upper envelopes at once; the deficiency maximization subtracts the common upper value from the full lower envelope. The two independent-rounding cases retain their correct constants. Positive affine expansion gives `T_original <= T_expanded`; it does not reverse that comparison or claim to preserve incidence.

At half-integral points, symmetrizing an extremizing sign vector gives zero singleton sign means and the exact identities `H=R/2` and `T=L/2`. The cell-vertex argument accounts for equality, complementation, fixed endpoints, and odd-complement cycles; remaining free components cannot be extreme points. Concavity of H and affinity of T on a cell yield the required extension to the full cube.

Polarization gives `R = max_S ||A_(S,T)||_(infinity to 1)` without an extra factor of two. A locally maximal cut for squared coefficients gives crossing row mass at least `1/sqrt(2)` of each full row norm. Applying sharp Khinchin to both sides produces `R >= sum_i ||a_i||_2 / 4`. The flow cut capacity is `m-|E(U)|+t|U|`, and `m+1` correctly excludes endpoint arcs from a smaller cut. Fractional edge loads then count each absolute coefficient once. The density, maximum-degree, bipartite, and separate degeneracy estimates follow with the printed constants, including isolated and zero rows.

The random-sign argument counts at most `2^h` exponentials after including both signs; Jensen and the displayed minimizing parameter give `sqrt(2mh log 2)`. Extending the signing outside a densest induced graph preserves the witnessing face. Compactness applies to the full-center ratio on `L=1`, where R is strictly positive, so perturbing zero entries justifies equality of suprema without claiming continuity of c* as support disappears.

The positive coloring probability, cut-parity criterion, graph-parameter comparisons, diluted dense-core example, and scale-invariance objection check out. The Schur transfer uses the weighted theorem's continuous parameter; rectangle counting gives beta=rho, matrix pairing gives `2L`, and the second polarization bounds the bilinear matrix norm by `4R`. Its use of older theory and its novelty limitation are accurate.

### Algorithms, encoding, and certificate scope

The only explicit computation asserted by this stage is finite exhaustive enumeration. Its running time grows exponentially in the number of free edges, and the text makes no polynomial-time claim. All encoded inputs in that computation are signs, small vertex labels, and integer masks; all objective comparisons are exact. Rational witness ratios are quotients of integers. There is no missing precision assumption for this finite proof.

The vertex LP is a mathematical characterization, not a promised compact representation or efficient exact-envelope algorithm. Positive expansion is expressly permitted to grow. The local squared-weight cut is an existence argument and does not assert a polynomial bound for arbitrary local improvement. The random-sign proof similarly asserts existence, not an efficient search algorithm. The flow argument only needs existence; its graph-density capacities are rational in any case.

The spatial-certificate definition correctly separates cover size from runtime and from unrestricted algorithms. For the repaired tolerances, the absolute target has slope 1 in the incumbent and the relative target has slope `1-theta>0`. Granting the optimum as incumbent in the relative convention now explicitly requires a positive optimum. Propagated or discarded feasible regions still need an accounted-for certificate. No future-stage lower bound is asserted here.

## Remaining limits

The finite checker establishes only the specified finite signing results. Universal claims were reviewed through their proofs and classical inputs, not inferred from those computations. I did not independently prove sharp Khinchin or audit all historical operator-theory proofs. Direct predecessor access remains limited as stated above; the manuscript expressly makes the Misener attribution indirect. I did not conduct a comprehensive novelty search, visually audit every PDF page, or rebuild the manuscript. Future-stage results and their algorithms are outside this review. None of these limits identifies a defect in the present Stage 1 scope.
