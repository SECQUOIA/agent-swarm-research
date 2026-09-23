# Stage 1, round 1, independent review 04

- **Verdict:** MINOR.
- **Major findings:** None.
- **Minor findings:** R04-01.

## Coverage

I read all frozen manuscript text in `process/snapshots/stage01-round01/`: `main.tex`, `macros.tex`, `sections/01-foundations.tex`, and `references.bib`. Locations below refer to the frozen `sections/01-foundations.tex`. I read the assignment, `process/review-protocol.md`, `process/stage-01-author.md`, and the Stage 1 scope requirements in `process/scope-proposal.md`. I did not read another report from this round or edit manuscript files.

I checked the actual arguments in the two complete canonical bilinear dependencies, `results/mccormick-gap-degeneracy-bound.md` and `results/mccormick-hereditary-density-characterization.md`, and the probability, independence, mixture, and box-transfer arguments in `results/positive-multilinear-degree-upper-bound.md`. The latter's later degree theorem is outside the frozen Stage 1 claims. Earlier review labels were not used as proof.

After reading `literature/AGENTS.md`, I inspected these relevant primary-source passages:

- `[[luedtke2012-some-results-on-the-strength]] p.2-3`, `p.5`, `p.8-9`, and `p.15-17`: vertex formulas, recursive single-product scope, positive common upper envelopes, box expansion, positive coloring bound, and the frustrated four-cycle example. Theorems 4, 5, and 8 in the local authors' manuscript match the expressly qualified manuscript citations.
- `[[boland2017-bounding-the-gap-between-the]] p.3-7`: signed growth and exactness statements, half-integral cut identities, induced-cut implication, and the earlier random-sign argument.
- `[[davidson2007-norms-of-schur-multipliers]] p.3-7` and `p.11`: real projective/Schur comparison, weighted continuous density bound, and its proof. In particular, using Theorem 2.4 avoids the rounding in Theorem 2.3.
- `[[mccormick1976-computability-of-global-solutions-to]] p.1`: the historical scope and bibliographic first page. No technical theorem here depends on a newly checked proof from that article.

I checked important displayed source formulas against the original PDFs, including rendered Luedtke pp.8-9, Boland p.4, and Davidson–Donsig pp.6-7, with images under `verification/reviewer04/`. I also directly extracted the original Davidson–Donsig p.4 and Luedtke p.15 to check the projective inequality and both coloring constants.

The original Szarek article was not locally available. The [publisher page](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/58/2/101277/on-the-best-constants-in-the-khinchin-inequality) confirms its metadata; its download returned HTTP 403. I independently checked the real Rademacher theorem, constant, and attribution in equation (1) of the primary research article [Eskenazis–Nayar–Tkocz, Distributional stability of the Szarek and Ball inequalities](https://arxiv.org/html/2301.09380v2). I did not read or reprove Szarek's original proof.

## Findings

1. **R04-01 — MINOR: State the tolerance convention in the certificate definition.** Location: lines 180–183, particularly “worse incumbents require weakly higher targets.” The usual intended conventions make this correct, but the text does not specify them: write `epsilon >= 0` and `0 <= theta <= 1` (or `< 1` if a nontrivial relative target is intended). The relative target `(1-theta)U` is nondecreasing in the incumbent only for `theta <= 1`; for example, at `theta=2`, increasing `U` decreases the target. Also qualify granting `U=f*` in the relative convention by `f*>0`, since that convention was introduced only for positive `U`. These are local definition clarifications; the frozen stage asserts no spatial lower theorem whose proof depends on the omitted conventions.

## Independent verification

**Probability foundations and exact marginals.** Independent endpoint sampling preserves each physical coordinate mean and the expectation of every multiaffine monomial. It therefore sends each graph point into the vertex graph hull, establishing both envelope formulas without assuming any compatibility between individually optimal factor laws. The finite vertex polytope also gives attainment and piecewise-affine boundary continuity.

For the circle construction, the failure arcs are projections of consecutive intervals in the real line. Each has length at most one and therefore its stated circle measure. Their union is the projection of one interval of total length `sum(1-x_i)`, whose measure is the minimum of that length and one. This verifies normalization, the exact singleton probabilities, and the extremal joint probability, including zero/one coordinates and total failure length exactly one. Unused coordinates can be added independently.

The common-threshold law has `P(X_i=1)=x_i` for every original coordinate at once, and each support's joint-success event has measure its smallest mean. For a fixed anchor, `D_e=X_anchor-product(X_i)` is pointwise either zero or one. Consequently `E D_e=u_e-E product(X_i)` under every admissible law. Positivity is exactly what allows the simultaneous upper envelope and weighted deficiency maximum. Discarding affine supports is essential to interpreting the displayed common-upper formula and is explicitly directed in the proposition.

A convex mixture of full admissible laws remains normalized and preserves every mean. Its deficiency expectation is the corresponding weighted sum. Nonnegativity permits dropping contributions from terms not handled by a particular law; it does not require independence between factors. The independence estimate handles both stated classes, including an anchor of mean zero; its omitted one-low-coordinate class is deliberately not claimed to be handled.

**Strict box-transfer example.** For the single product on `[1,2]^3` at `(3/2,3/2,3/2)`, the common endpoint threshold law gives upper value `9/2`. In endpoint indicators with success count `k`, the vertex value is `2^k >= 2k`. The uniform law on the six vertices with `k=1` or `k=2` has all means `1/2`, attains lower value `3`, and proves the original gap is `3/2`. Expansion gives `1+sum p_i+sum p_i p_j+p_1p_2p_3`, whose separate lower envelopes sum to `5/2`; its termwise gap is `2`. Thus the stated inequality direction `T_original <= T_expanded` is correct and can be strict. The full hull gap remains invariant under the coordinate bijection.

**Cut and graph arguments.** Pairing any sign vector with its negative at equal probabilities preserves all half means and its quadratic value. Fixing outside coordinates to one contributes only an affine function, so the grid identities have the claimed full scope. In the cell argument, a relation component with neither a fixed value nor an odd complementation cycle has one genuine free parameter; inactive inequalities remain slack under a sufficiently small perturbation. Hence its half-integral vertex conclusion is valid. Concavity of `H` then gives the comparison on each whole cell, including zero-gap points.

I rederived the factors of two in polarization: `Q(s)-Q(t)=2v^T A u`, so half the oscillation equals the maximum bipartite block norm. Khinchin and a locally maximal squared-weight cut give `R >= (sum row norms)/4`. Fractional load bounded by induced density gives `L <= sqrt(rho) sum row norms`, and hence the constant four. The degree and bipartite constants follow from counting absolute edge weights twice and once, respectively. The four-cycle with one negative edge attains the stated bipartite sharpness. The separate degeneracy coloring proof has the same constants.

The positive coloring probability, signed-cycle cut criterion, density/degeneracy/arboricity comparisons, average-density counterexample, zero-weight conventions, coefficient scaling, and induced-subgraph localization all check out. The whole-center supremum proof uses continuity only for `L_V/R_V` on nonzero coefficient vectors; it correctly avoids assuming continuity of `c*` when support disappears.

**Random signs.** Only the edge signs must be independent. For each fixed vertex configuration, multiplication by its deterministic edge products preserves the independent Rademacher law. Quotienting vertex configurations by global reversal leaves `2^(h-1)` choices, and the additional positive/negative exponential sum yields the factor `2^h`. Jensen therefore gives `E Z <= h log(2)/lambda + m lambda/2`. The displayed optimizing lambda and bound `sqrt(2mh log 2)` follow. At least one signing is no worse than the average, and extending its signs outside a densest induced subgraph leaves the face witness unchanged. This verifies finite existence, full support, and the absence of any connectivity or cross-configuration independence assumption.

**Prior-theory transfer.** For the symmetric pattern, rectangle counting gives `beta <= rho`, and the same densest set on both axes gives equality. With `M=sign(A)`, the pairing is `2L`; the projective dual bound uses the real sign bilinear norm. Polarization on the continuous sign cube yields `||A||_(infinity->1) <= 4R`, producing exactly `L <= 4 K_G sqrt(rho) R`. Mean zero gives the stated factor-two comparison with the Sidon constant, and bipartite sign reversal gives equality. No new norm principle or unrestricted algorithmic consequence is claimed.

**Finite checker.** I wrote and ran `verification/reviewer04/check_probability.py`. It passed:

- Exact rational normalization and marginal checks for threshold, circle, independent, and mixed laws at all 780 mean vectors in dimensions one through four with means in `{0,1/4,1/2,3/4,1}`; all support upper probabilities and deficiency mixture identities were checked.
- The exact strict box-transfer example above.
- Exact enumeration of sign expectations on all 63 nonempty labeled graphs on four vertices, followed by a floating-point comparison to the logarithmic random-sign bound. The final logarithm/square-root comparison is numerical; the enumerated averages and antipodal identities are exact.

## Remaining limits

The finite checker supports the analytic review and cannot establish the universal theorems. Sharp real Khinchin, max-flow/min-cut, and the cited Schur norm theorems remain established external inputs. I did not conduct an exhaustive priority search or settle the missing Davidson–Donsig journal pagination. The bibliography identifies that article by DOI and does not invent pages. The best universal density constant and later-stage probability/spatial results are outside this stage's resolved claims. Apart from R04-01, I found no defect in theorem truth, constants, support quantifiers, proof completeness, or the assigned Stage 1 coverage.
