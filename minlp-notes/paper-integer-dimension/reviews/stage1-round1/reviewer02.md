# Stage 1, round 1 — reviewer 02

Primary lens: convex lifts, parity contacts, unrestricted integer ranges, topology and measurability.

Major findings: 0

Minor findings: 2

## Snapshot and coverage

I computed SHA-256 hashes for all five frozen files. All match `snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |

I read the complete 1,206-line mathematical stage, the process and review protocol, bibliography, macros, main file, and coverage inventory. I reconstructed the main mathematical arguments rather than relying on the prior audit verdicts. I compared relevant original proofs in the square/product, interaction-graph, scalar-rank, one-sided inertia, covariance, noncommutative-rank, smooth-map, constant-rank, and perspective result files. I also inspected the rational-construction statement, the parity/epigraph extension note, the nonquadratic investigation, and selected original square and noncommutative-rank audits.

Primary-source checks covered Lubin–Vielma–Zadik's midpoint lemma, GGOW Theorems 1.4 and 1.17 and capacity passages, Nicola's Definition 1.1 and following paragraph, and Wolff's Theorem A and proof on printed pages 50–51. The latter three were read from the supplied primary-source text cache. I did not independently audit every bibliography item or the full IQS rational algorithm. I did not inspect every later-stage supporting note or certify completeness of the repository-wide inventory. The deferred polynomial-bit theorem was checked for consistency of stated scope, not reproved here. I did not compile or visually inspect the PDF.

## Assessment

I found no major mathematical defect in this stage. In particular, the arbitrary-convex-lift lower bounds do not silently assume bounded integer ranges, measurable sections, closed projections, or convex parity classes. The constructive upper bounds use actual polyhedral members or explicit linear product encodings. The constant-rank charts select polyhedra in the original coordinates; they are not imposed as nonlinear coordinate constraints on a convex lift.

This assessment is a bounded independent review, not a guarantee of correctness or priority.

## Findings

1. **MINOR — repeated multiplication typo in the smooth upper proof.** Location: `sections/01-foundations.tex:974`, `:977`, and `:992`, proof of `thm:smooth-ranks`. The expressions `C_0,2^{-T}` and `2C_0,2^{-T}` contain literal commas where multiplication is intended. This makes the displayed remainder estimate and error-budget choice formally malformed. The intended bound follows from the preceding zero-block argument and agrees with the original smooth-map result, so this is a notation defect rather than a theorem error or substantive proof gap. Replace the commas by spaces or `\,`, giving `C_0 2^{-T}` and `2C_0 2^{-T}`. In the polynomial paragraph, it would also help to say explicitly that the fixed constant is enlarged to bound Hessians on the enclosing box after normalization.

2. **MINOR — capacity equivalence needs a more precise source locator.** Location: `sections/01-foundations.tex:529–541`, the introductory citation for `eq:shrunk`, `eq:evaluation`, and `eq:capacity`. The cited GGOW Theorem 1.4 gives the singularity, matrix-evaluation, shrinking, and rank-decreasing equivalences; Theorem 1.17 gives the general-rank zero-rectangle characterization. Neither displayed theorem itself states the positive-capacity equivalence. GGOW defines capacity in Definition 2.6 and treats the capacity connection elsewhere, including the opening of Section 2.3 and the discussion of Gurvits's result near the end of Section 6. Add a separate accurate locator/source for positive capacity rather than presenting all three formulas as located in Theorems 1.4 and 1.17. The underlying equivalence is established, and the manuscript additionally proves a capacity-free qualitative determinant estimate, so this is an attribution/locator issue rather than an unsupported main theorem. Source checked: [GGOW, published primary PDF](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf).

## Checks supporting the assessment

- **Parity and topology:** for each residue class, witnesses are chosen only for the particular endpoints being averaged. Their average is feasible with an integer index. Closing the graph-input sets in compact `D` preserves the continuous pairwise error condition because the error body is closed. This does not assert feasibility of lifted limit points. Compactness then supplies precisely the measurability, coordinate extrema, and finite volume subadditivity used later. The attribution to the midpoint mechanism is supported by [Lubin–Vielma–Zadik, Lemma 4.1, printed page 12](https://optimization-online.org/wp-content/uploads/2017/06/6082.pdf).
- **Finite disjunction:** binary coordinates at a vertex force every positive weight to share that exact binary code. Boundedness kills inactive recession vectors; a common recession cone permits their absorption into the active member. This checks both versions stated in the lemma, including `N=1`.
- **Finite constants:** I checked the square midpoint factor, the product area integral and width argument, the signed maximal-simplex determinant estimate, covariance expansion, and rearrangement of the principal-compression finite lower bound. The closures need not be convex for any of these uses.
- **Quadratic and smooth rank:** the Hermitian principal-pivot induction respects multiplication order; the real descent and symmetric shrinking arguments give the claimed zero blocks and exponent sum. In the smooth estimate the matrix-evaluation phase has the claimed mixed Hessian, the cutoff is one on the Cartesian contact product, and the product-volume powers cancel correctly. The local proof does not require boundary regularity of the contact.
- **Upper formulations and perspectives:** shared prefixes retain the endpoint 1; residual product errors add with absolute coefficients; polynomial bit-product variables are forced integral without new integer declarations. Positive perspective homogenization scales arbitrary continuous auxiliaries directly and uses bounded product rows only for binaries. Division by positive `t` proves both graph retention and error scaling.
- **Executed numerical check:** an independent SciPy `linprog` check maximized the relaxed folding objective for depths 1–7 at 65 equally spaced inputs per depth (455 LPs). Every optimum agreed with the exact folding-sequence value; maximum objective discrepancy was zero in the reported floating-point computation. This supports the folding construction but does not replace its proof. The checker was executed inline and created no repository file.

No manuscript or bibliography edits were made.
