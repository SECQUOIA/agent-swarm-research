# Independent Stage 5c review — reviewer 4

Overall verdict: **accept**. I found no major or minor issue in the frozen Stage 5c section, its material mathematical dependencies, or the inspected literature comparisons. All seven new formal results have sound proofs under their stated hypotheses. The algorithms are theoretical polynomial bit algorithms for fixed structural parameters; the diagnostic is correctly presented as finite supporting evidence.

I read `completion-s5c-review-instructions.md` first. I reviewed all of `complexity/sections/10-weighted-blocks.tex`, its integration in `main.tex`, the new bibliography entries, the build/check manifests, and the diagnostic source. I did not read author, lead, peer, or historical review reports, communicate with other reviewers, or use subagents. This report is my only workspace modification. No manuscript, code, managed literature, or Paper B file was changed; no commit was made.

Initial and final SHA256 of `complexity/sections/10-weighted-blocks.tex`:

`fdb90d578a0a915b66fb443dcc530731d1f2647da6e437a3a0e1ebe093cebdb1`

Both match the supplied frozen hash. I also independently checked all 17 manuscript input hashes in the build manifest against the current files; all match.

## Explicit result verdicts

| Result | Verdict | Main reason |
| --- | --- | --- |
| `lem:a-wblk-local`, conditional block values | Accept | Exact block independence, fixed-dimensional box projection, and correct uniform continuity bounds give the stated graph and recovery interface. |
| `lem:a-wblk-univariate`, uniform rational approximation | Accept | The annihilator and exceptional set have polynomial encodings; short bands and analytic panels cover the whole interval; interpolation and rational node errors have explicit polynomial bit bounds. |
| `cor:a-wblk-scalar-sum`, scalar sums | Accept | Common rational endpoints permit polynomial-size summation without compositing the summands' algebraic fields, and the error and rounding budgets suffice. |
| `thm:a-wblk-line`, affine nomination line | Accept in all three coefficient models | Local conditional optimization, scalar summation, independent local recovery, and original-coordinate rounding establish both output guarantees. |
| `cor:a-wblk-line-polynomial`, fixed dense piecewise-polynomial laws | Accept | Fixed-dimensional elimination remains polynomial for growing dense degree; derivative bounds and monotonicity supply the required Lipschitz interface. The fixed-law restriction is explicit. |
| `thm:a-wblk-hybrid`, fixed total exceptional rank | Accept in all three coefficient models | There are only `d + kappa + 1` retained variables. Exact exceptional projection precedes approximation, and the cactus construction extends using local nominations alone. Recovery and the error ledger are valid. |
| `cor:a-wblk-hybrid-box`, balanced boxes | Accept in all three coefficient models | The resistance-independent face reduction preserves attainable objective values and does not increase exceptional rank; face selection and rational lifting fit within the stated accuracy. |

The final discussion also passes: it identifies a remaining interface needed by these algorithms, credits classical ingredients, and makes no unsupported hardness, impossibility, or exact-comparison necessity claim.

## Mathematical checks

### Conditional graphs and coefficient elimination

In Section 10, lines 44–84, the tree weights satisfy `Aw=c`, and hence the objective is the sum of the edge drops with those weights. The block aggregation sets partition the original vertices for each fixed block. This makes each block's physical state depend only on its own affine aggregated nomination and its own coefficients. Independent local maximizers can therefore be assembled at every common nomination; the displayed maximum identity is exact.

I checked the full proof of `lem:a-blk-boxlp` in `03-block-rank.tex`, lines 396–524. Its support-function formulation eliminates a box with arbitrarily many coordinates by retaining only the fixed number of image coordinates. It enumerates realizable signs of the polynomials `eta^T W_e(z)` in fixed dimension, rather than all box corners. The disjunction of guarded support inequalities remains correct on ties. Universal elimination has a fixed number of variables, fixed input degree, and polynomial coefficient length. In Section 10 the objective supplies precisely one additional row, regardless of objective support.

Recovery by exposed image vertices is valid also for a lower-dimensional zonotope: an exposing direction can be perturbed off all finitely many nonzero column hyperplanes without changing its unique maximizing image. At most `k+2` affinely independent image vertices suffice in `R^(k+1)`. Their convex coefficients and the lifted box coordinates lie in the same ordered field as the supplied core. The proof does not depend on that core being an optimizer of the box lemma itself. This justifies its later use at the hybrid surrogate sample.

The closed sign-cell treatment does not introduce false directional scenarios. At a nonzero flow the correct directional interval is selected; at zero its contribution is zero for either sign. The symmetric model keeps one shared coefficient per edge, and inactive directional coefficients remain unrestricted within their own original intervals.

The bounds in lines 86–106 have the correct factor. The nomination difference gives an edge-flow change at most `(T_B/2)||z-z'||_infinity`; multiplication by the edge-law Lipschitz constant `2 beta_U B_0` yields the stated `K_B`. Maximizing over the same compact coefficient box preserves the bound. Aggregation cannot increase total positive nomination, so the global physical-flow bound also applies locally. Chord flow equals its fundamental circulation coordinate with the chosen zero-chord tree routing.

### Scalar approximation

I checked each part of lines 133–278, including the following potential failure points.

* A quantifier-free graph must have a value-dependent vanishing polynomial at every generic graph point. Otherwise its signs remain unchanged in a neighborhood and it cannot describe a function graph. Removing contents and repeated factors affects only finitely many specializations; continuity restores the annihilating identity there. Reducibility and branch selection cause no problem.
* The product degree is bounded by the sum of input degrees. In two variables, dense multiplication, subresultants, primitive parts, squarefree extraction over `Q(t)`, and the resultant all have polynomial degree and bit bounds. The construction does not require fixed degree.
* The nonzero polynomial `H_*` includes leading-coefficient zeros and root collisions. Real quantifier elimination of `Re H_*(u+iv)=Im H_*(u+iv)=0` followed by isolation computes the finite set of distinct real parts of complex roots. It does not require enumerating or combining a large collection of number fields. Nonreal branch points are correctly included.
* The padded bands have total length at most `eta/(16K)`. A midpoint approximation of accuracy `eta/8` therefore gives error below `eta/4` on every merged component. The endpoint bands ensure complete coverage even when the exceptional polynomial is constant.
* Outside the bands, every exceptional real part is at least `d(t)` away. Padding remains valid after merging, and omitted real parts outside `[-1,2]` cannot violate the asserted bound. The geometric recursion has polynomially many panels and polynomial rational endpoint encodings.
* The closed complex disks avoid every root of `H_*` by at least `3 rho/4`. Nonvanishing leading coefficient, simple roots, and a root bound give holomorphic continuation on a neighborhood of each disk. Simple connectivity prevents monodromy there; continuity of the real function prevents switching between distinct roots on a panel.
* The leading coefficient bound `|lambda|(3 rho/4)^k0` and coefficient bound for `|t|<2` give the stated Cauchy root bound. The rational encoding of this bound is polynomial even when its magnitude is large.
* With `h <= R/16`, the contour remainder is at most `(16M/15)(2/15)^(q+1) <= M 2^(-q)`. The Lagrange basis bound at equally spaced nodes yields a rational-node error at most `eta/8`. Hence the constructed rational interpolant has error at most `eta/4`, stronger than the lemma requires. The necessary node precision is polynomial, and expanding the rational interpolant requires only polynomially many factors of polynomial bit length.

This reasoning handles nonsmooth real branch switches within bands, near-nonreal singularities, an external pole close to the interval, repeated input factors, constant functions, and endpoints. Adjacent pieces need not agree, but both remain valid at their common endpoint.

### Scalar summation, the line theorem, and dense laws

For the scalar-sum corollary, sorting all rational endpoints produces only polynomially many common intervals. On each, selecting one covering polynomial for each summand gives total uniform error `a=eps/16`. A surrogate maximum interval of width `eps/8`, followed by a sample at least `L-eps/16`, gives true loss at most `5eps/16`. Rational argument rounding adds at most `eps/4`, giving at most `9eps/16`. Negative summands and near cancellation require no special separation bound.

The line theorem uses tolerance `eps/2` for this task and reserves `eps/4` for coefficient rounding, so it has slack. Singleton nomination intervals reduce to independent local algebraic computations with separately refined value intervals. Recovering and rounding a list of local coefficients never requires a primitive element containing roots from all blocks. The output consists of original parameters; it need not contain a rational physical state.

For the polynomial-law extension, the arrangement of breakpoint equations is polynomial in fixed dimension `1+r0`, including all boundary strata. Dense expansion of the substituted laws remains polynomial because the dimension is fixed and numerical degree is at most polynomial in input length. Continuity makes neighboring law formulas agree. Strict monotonicity suffices both for the unique physical state and for the acyclic difference-flow estimate. The absolute coefficient sums give valid bounds on values and one-sided derivatives on the bounded flow interval, with polynomial bit length. No uncertain-polynomial-law extension or sparse large-exponent complexity claim is made.

### Hybrid theorem and full-box composition

In Section 10, lines 417–508, all exceptional circulations together number exactly `kappa`. The exact box projection uses `kappa` cycle rows and one weighted value row. Its support-function variables are temporary fixed-dimensional elimination variables. The final optimization retains only `z`, `q`, and `v`, totaling `d+kappa+1`. Large exceptional blocks and arbitrarily many coefficients therefore do not break the variable bound.

The cycle and bridge nominations depend on `z` alone by block aggregation. They do not depend on exceptional circulations or coefficients. I checked the fixed-law charts, square-root panels, common-part construction, interval threshold elimination with ties, complete circulation candidates, and the recovery paragraphs of `07-weighted-cactus.tex` through line 713. Those arguments use local cycles and their affine nominations, so extending them to the nonexceptional blocks of a general graph is legitimate. Pairwise surrogate comparisons are made within each cycle; the common sign decomposition in fixed nomination dimension avoids a Cartesian product of cycle choices. Lower-dimensional signs and zero-flow branches are included.

The growing surrogate degree is harmless: dense expansion in fixed dimension remains polynomial. Rational chart denominators retain nonzero conditions and can be cleared with a known sign or their square. Crucially, the box lemma is applied first to degree-two exceptional data, so its fixed-degree premise is not used after inserting growing-degree surrogates.

Here is the hybrid error ledger explicitly. Let `C(z)` be the exact conditional maximum of the nonexceptional blocks and `C_sel(z)` the recoverable candidate chosen by the surrogate. The cactus construction gives both `|S-C|<=a` and `|S-C_sel|<=a`, with `a=eps/16`. If `T=sup(v+S)`, independence and exact exceptional feasibility give `|OPT-T|<=a`. An interval `[L,U]` of width at most `eps/8` containing `T` gives enclosure `[L-a,U+a]` of width at most `eps/4`. A feasible sample with `v+S>L-eps/16` has recovered true value greater than `L-eps/16-a`. Its loss is therefore at most `eps/8+eps/16+2a=5eps/16`. Parameter rounding adds at most `eps/4`, giving total loss at most `9eps/16`, below `eps`. Open parts do not require attainment because the sampling threshold is strictly below the supremum.

Exceptional coefficient recovery takes place in the one polynomial-degree field of the sampled core. Each nonexceptional cycle uses only the field of the common nomination and its own local extension. Separately isolating their coordinates is polynomial. Rational LP inside the isolating box intersected with `P` preserves exact feasibility even when `P` is lower-dimensional. Rounding original coefficients inside their original intervals preserves the symmetric sharing requirement and directional independence. The global continuity estimate applies after changing nominations and coefficients; there is no requirement to remain in the same algebraic sign part.

I read the full nomination-face theorem and proof, `07-weighted-cactus.tex`, lines 68–239. Pruning and zero-objective block contraction preserve attainable objective values and rational lifts. The incidence-tree argument ensures a surviving block does not have two vertices identified, so its rank is unchanged; deleted blocks only decrease `kappa`. The two smoothing/perturbation stages give the claimed resistance-independent face family, including singleton bounds and lower-dimensional balanced boxes. Applying the hybrid theorem to each face with tolerance `eps/8` is valid. If face `j` has the largest lower endpoint, the best face optimum exceeds that face optimum by at most `eps/8`; its returned scenario adds at most another `eps/8` loss. Rational disaggregation and arbitrary allowed coefficients in removed blocks preserve the objective. The minimum uses `-c`, and a zero objective requires only rational feasibility.

## Dependencies and primary sources inspected

The material manuscript dependencies checked were existence/uniqueness, continuity/attainment, block decomposition, and computational/output conventions in `01-preliminaries.tex`; the smoothed adjoint and acyclic physical-flow bound in `02-cactus.tex`; the entire box-projection/recovery lemma in `03-block-rank.tex`; the dense-law input model in `04-laws.tex`; and the face, cactus-surrogate, nomination-continuity, and original-coefficient-continuity arguments in `07-weighted-cactus.tex`. The proofs are sufficient for their uses above. In particular, the coefficient continuity argument remains valid across zero flows after smoothing and taking a uniform compact-domain limit.

I inspected these primary-source statements directly:

* Vigneron, local original `literature/vigneron-2011-algebraic-sums-manuscript.pdf`, dated October 21, 2011: Section 2.1, printed p. 5; Section 2.3, p. 7; Theorem 6 and proof, pp. 8–9; Section 3.2, pp. 9–10. These establish the nonnegative constant-description interface, polynomial-in-`1/eps` approximation, the bit-model extension, and approximate summation over a common arrangement. Section 10 describes these distinctions accurately.
* [Borcea–Bøgvad–Shapiro, arXiv:math/0409353v2](https://arxiv.org/pdf/math/0409353v2), Theorems 2–3, printed p. 3, with Definitions 2, 4–6 on pp. 2–3. These concern the dominant branch and exponential convergence off the specified exceptional locus; they do not themselves provide Section 10's full-interval rational bit interface.
* [Binyamini–Novikov, arXiv:1802.07577v2](https://arxiv.org/pdf/1802.07577v2), Section 1.1.1 and Theorem 1, printed p. 2; the definition of input degree complexity preceding that theorem; Section 1.5, pp. 12–13; and algebraic-map/cell complexity in Section 2.2, p. 15. Their polynomial chart bounds are geometric complexity bounds. The manuscript's modest distinction from a rational coefficient-bit algorithm in prescribed common coordinates is justified.
* [Yomdin, arXiv:1406.1719v2](https://arxiv.org/pdf/1406.1719v2), Definitions 5.1–5.2, printed pp. 22–23, and Theorem 5.6 with proof, pp. 23–24. These support the stated logarithm-cubed degree-based parametric approximation comparison, rather than approximation of a function in its prescribed original argument.
* [Petras, publisher abstract](https://www.sciencedirect.com/science/article/pii/S0377042701005866), JCAM 145(2), 345–359 (2002). Direct opens failed, but the publisher page's indexed abstract was returned by search and inspected in full. It supports enclosure algorithms for functions under representation assumptions. I did not inspect the full article or rely on a detailed rate.
* Basu, `literature/papers/basu2014-algorithms-in-real-algebraic-geometry/original.pdf`: Definitions 2.12–2.13 and Section 2.2.2, pp. 9–10; sampling discussion and Theorem 2.16, pp. 11–12; Theorem 2.27, p. 16. I checked the displayed elimination output counts, degree bounds, and integer bit bounds against the manuscript. They support polynomial bit complexity for fixed total dimension, including growing numerical degree. I attempted text extraction of the local BPR 2006 original, but its text encoding was unreadable; I do not claim direct inspection of its individual chapter statements. Basu's readable primary survey provides the relevant precise statements and references.

These checks support the comparison actually made. They do not establish an exhaustive priority result over all approximation literature, and the manuscript does not claim one.

## Diagnostic and build evidence

I read the full `verification/check_s5c_scalar_approximation.py` and independently reran it with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python`. It exited successfully and reproduced the manifest's four fixture records. Its SHA256 is `ae633732ca9ea4f47986eb2d46ab0c35590f0bc8fdbfad5767a8d2d11ca4985e`.

The fixtures are an implicit quintic, a real branch switch, near-nonreal branch points, and a nearby external pole. The run checked geometry on 988, 896, 904, and 1038 constructed panels respectively; it interpolated selected panels, not every panel. It checked exact interpolation identities, rational remainder inequalities, and 170/170/170/85 certified sampled errors. Coefficient sizes reach 172713 bits in the external-pole fixture. The use of explicit `require` checks means the tests remain active under `python -O`; the supplied checks manifest records a successful optimized-mode run as well. I did not repeat that second execution.

The diagnostic uses supplied exceptional-root descriptions and function-specific value oracles. It neither implements general graph elimination nor constructs or optimizes a full network. Its finitely sampled function-error checks do not prove uniform accuracy; the separate contour and Lipschitz arguments do that. These limitations are clearly acknowledged in the source, output, and checks manifest.

The build manifest records a successful forced `latexmk` build, zero errors, unresolved references/citations, duplicate labels, or overfull boxes. I verified its current input hashes rather than rerunning a build that would modify build artifacts. `main.tex` includes the new section before the conclusion, and the four new bibliography entries have the inspected titles and locators.

## Findings and repairs

Major findings: none.

Minor findings: none.

Required repairs: none. I have no optional changes that need to delay acceptance. The source-access and diagnostic limitations above are review limitations, not manuscript defects.
