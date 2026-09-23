# Stage 4, round 1 — reviewer 14

Major findings: 0

Minor findings: 0

No concrete mathematical, source-attribution, coverage or synthesis defect requiring correction was identified. This is a bounded review, not a guarantee of correctness or publication priority.

## Reviewed scope

I read all 1,297 lines of `sections/04-vector.tex`, the complete abstract, introduction and conclusion, the stage task and lenses, process and review protocol, bibliography and coverage inventory. I reconstructed the proofs independently. I compared all ten canonical stage-4 result statements and their distinct mechanisms, and the eleven explicitly substantive supporting developments, with the original result/note texts. The original files were inspected for their statements, development structure and consequential supporting passages; this was not a reread of every historical audit.

Relevant accepted dependencies were checked, including the scalar indexed endpoint compiler, mass-accurate quantile procedure, hybrid cell-count and chord-error guarantees, and Jensen superadditivity. The parity/contact, finite-disjunction and rational log-product interfaces had been read and independently reviewed in my preceding stage assignments; the accepted stage-1/2 hashes are unchanged. The current stage-3 text was used for the computational interfaces, rather than silently assuming its pre-correction snapshot. Root's audit was read only after reconstructing the new manuscript proofs and was used as a source locator, not as mathematical evidence.

All eleven snapshot hashes were checked against the actual files:

| File | SHA-256 |
| --- | --- |
| `abstract.tex` | `db2b95f525fdfc786c9c24b46f41693892131a8103f249d27dbc012d53e323a3` |
| `coverage.md` | `d8b2ed835cfcdfac31b48197cd7a4da7c0e9bac0f73b2dfab6a3571d34a8e1cf` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `026577c84ea4f9c0ff19361708694be45ce88a5a4e911a9b902852f826d1ba9c` |
| `references.bib` | `60fd73a2eec8fd2bc999cf2c407c6a571c590b087786c78647cc1bb7a59a1693` |
| `sections/00-introduction.tex` | `6940bf7c1017d82a8ea00af76575aa88da76f2ef26290b4b3872fd0bba152b16` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `8e271531b4c705a1333b49f170b20e987359ed5e7d1b05866030bccb69040803` |
| `sections/04-vector.tex` | `d9369569aa0711c3652dcf28929ea4be5884c534f18e371038fbdfc7edb6252d` |
| `sections/05-conclusion.tex` | `2bfb1f16aaa317e5b49dd171ccd9648c7a320343f23ec13acbf6a38b1955ad6e` |

## Independent mathematical assessment

1. **Refinement and overlay.** The strict concave-gap level cuts give `2H-1` cells, including flat maxima and duplicate cuts. Restriction preserves component chord-error bounds. In the implicit merge, counting right endpoints on one known rational grid gives exact order statistics without enumerating the arrays. I checked duplicate cells and the containing-source-cell lookup, including the final endpoint. The common deterministic bisection tree orders quantile outputs by target even when separately computed approximate mass values are not monotone. The common denominator is supplied by polynomially many piece endpoints and a single dyadic precision. This is stronger than merely bounding each individual denominator. All vector components use the same input interpolation weight.

2. **Box/facet curvature bases.** The finite maximum determinant and rational determinant-doubling constructions select original convex outputs. Signed representation coefficients can therefore be bounded using the sum of nonnegative selected gaps. I checked the counts `4r-1`, `8r-1`, the compiled factors below `2^12 r` and `2^13 r`, and the facet rounding budget. Compactness and nonnegative facet coefficients force every component affine in the rank-zero case. The half-body band for coupled errors is necessary and used correctly.

3. **Maximum product and rational spanners.** The first-order supporting inequality holds on every feasible positive segment. Expanding the product at `(1-1/m)b+v/m` proves the factor-seven bound for an `e^-1` product approximation; the one-dimensional case is treated separately. For the generic spanner, the seed determinant controls inverse-basis objectives before exchanges begin. A fixed rounding grid followed by the central-ball convex combination gives exact feasibility and at most one-quarter objective loss. Determinant doubling terminates in polynomially many exchanges, and fixed denominators control later oracle inputs. This addresses a real bit-complexity obligation, not just a bound on the number of arithmetic operations.

4. **Positive polar and effective image.** Checked the explicit balls, feasible seeds and nonzero pulled-back separators. Exact feasible primal support points give either a valid positive-polar separator or a certified nearby feasible polar point. The construction uses weak polar access, as the source interface permits. The second spanner produces a parallelotope inside the effective body. Finite bases give the `8r^2-1` bound. Rational bases give chord gap `13P/64`; effective-coordinate rounding adds `P/16`, and the half-parallelotope band admits only `49P/64`. Restoring affine terms exactly keeps rounding errors in the nonlinear image. Comparator lifts are only restricted through their exact graph contacts; their other errors need not lie in that image.

5. **Separable vectors.** Reconstructed why one concatenated output-row basis works in every coordinate. Jensen superadditivity makes product-index distance control the shared scalarization gap. The generating-function bound for deleted integer `l1` balls yields the product packing. Combining capacities `12P_i` and `5832P_i` with the six stated tolerances gives the displayed finite/compiled constants. I checked that coordinate rounding budgets sum correctly, and that all components share each coordinate's index and interpolation weight. Rank-zero and inactive-coordinate cases are consistent.

6. **Positive-power obstructions.** Verified the oriented thirds margin `2177/2144>1`, its residue and binary-section consequences, and why each signed scalarization separately has a one-binary range-rectangle formulation. The midpoint estimate does not imply a valid full chord. Three distinct zero-sum residues give the cap-set restriction; the generating-function minimizer solves `4t^2+t-2=0`. The separate three-label proof checks arbitrary integer gaps and the second convexification inside the middle section. None of these results is used to claim a growing difference of optimum binary and general-integer counts for this one-input box family.

7. **Exact and nonconvex separations.** For the degree-32 curve, checked the three rational boxes and every possible middle integer section, not merely segments joining selected witnesses. Oriented thirds violations at product contacts yield exact counts `n` and `ceil(n log2 3)`. The upper constructions have the advertised different size guarantees. The hinge precursor and Bernstein stability argument retain a distinct robustness mechanism. For the triangular-wave family, the Bernstein variance bound gives uniform error `1/32`; the period/orientation representation contains the polynomial graph after thickening. Peaks and intervening troughs force distinct binary sections, while alternating crossings control actual degree. The theorem claims at most two general integers, rather than needing an unproved equality of that minimum.

8. **Arbitrary polynomial overlays and conditioning.** Root brackets and their complements give the stated number of shape pieces. Reconstructed all three directed band checks, including the bracket case and singleton cells; source-type flags can be computed continuous Boolean wires. For the tilted construction, the common quadratic makes both outputs convex while the difference projection preserves the scalar lower bound. The second-difference integral forces the stated growing radius ratio. Downward box and simplex bands prove the finite conditioning estimates using only the stated inner/outer containments, so the nonsymmetric extension is justified. Unconditional normalization and the earlier direct allocation bound are distinguished.

9. **Open boundary and synthesis.** The strict upper-violation sets are convex and their integer-coordinate projections are lattice free, while their union need not be convex. The manuscript does not mistake Helly infeasibility certificates for graph covers or parity for an integral Radon partition. The abstract, introduction, result map and conclusion agree with the established scopes: dense vector compilation, separately stated sparse scalar constructions, restricted separable multivariate inputs, and the unresolved one-input convex box constant-gap question. The tilted example, nonconvex example and growing-input product are not advertised as resolving that question.

## Coverage and source attribution

All ten canonical stage-4 developments are represented: exact convex box counts; box/facet separable curvature rank; separable oracle curvature rank; implicit convex-vector compilation; original-output curvature rank; facet curvature rank; oracle curvature rank; direct unconditional maximum-product compilation; nonconvex scalar degree gaps; and arbitrary polynomial-vector compilation. Their corresponding named theorems/propositions occur in `04-vector.tex`, and the precursor mechanisms remain alongside stronger bounds.

All eleven substantive supports were accounted for: conditioning/simplex estimates; finite continuous separable comparisons; the lattice investigation; hinge and Bernstein one-bit precursor; tilted-body transfer; the promoted nonconvex precursor pointer; bounded vector-power source positioning; positive-power scalarization/refinement obstruction and finite overlays; cap sets; the independent three-witness argument; and fixed-denominator rational polar spanners. Earlier numerical choices superseded by the exact degree-32 construction do not constitute missing theorems.

Consequential primary-source checks were as follows:

- **Awerbuch–Kleinberg, Section 2.3, Propositions 2.2/2.4 and Observation 2.3:** directly read the [author-hosted primary PDF](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf). Compact spanning sets, maximum determinants and determinant exchange are exactly the credited primitives. The manuscript supplies its own seed conditioning and rational-precision argument instead of borrowing an incompatible exact-oracle complexity bound.
- **Grötschel–Lovász–Schrijver:** directly read Definition (5), the known-ball convention, Theorem (3.1), and Corollaries (3.4)/(3.5) in `build/source-cache/gls1981.txt`. Weak optimization compares against every exact feasible point, as required here. The original dimension-at-least-two convention is handled by the stated product padding. The positive-polar implementation is correctly credited as an instance of established polar/anti-blocker access, with explicit new application-specific repairs.
- **Plevrakis–Hazan:** read Section 3.2 in the primary `plevrakis2020.txt`; it explicitly combines separation, approximate ellipsoid optimization and approximate barycentric spanners. Credit is appropriately limited to that antecedent combination.
- **Lyu–Hicks–Huchette:** read Section 3, Proposition 1 and equation (4) in the extracted primary `lyu2026.txt`. They use the union of breakpoints and one SOS2 vector for all functions of the same input. The manuscript distinguishes this explicit-list precedent from polynomial random access to exponentially long lists. The [publisher record](https://pubsonline.informs.org/doi/10.1287/opre.2023.0187) confirms the authors, title, volume 74(1), pages 484–499 and January–February 2026 issue; its 2025 online-publication date is compatible with citing the issue year 2026.
- **Kelly–Maulloo–Tan:** read Section 2 in the primary `kelly1998.txt`, including NETWORK's logarithmic objective and proportional-fairness inequality (1). Unit weights give the supporting sum used in the manuscript. The general-body approximation factor is proved locally rather than attributed to the network model.
- **Ellenberg–Gijswijt:** read Theorem 4 and its proof and Corollary 5 in `ellenberg2016.txt`, and checked the [published primary version](https://annals.math.princeton.edu/wp-content/uploads/annals-v185-n1-p08-p.pdf). The finite-field nontrivial-solution hypothesis specializes correctly to the distinct zero-sum contact residues. The manuscript credits the cap-set theorem and derives the finite generating-function constant itself.
- **Hartman and Averkov–Weismantel:** read the primary DC introduction in `hartman1959.txt`, and definition (H)/Theorem 1.1 in `averkov2012.txt`. The DC citation is historical context for a locally proved quadratic addition. The Helly identity and its finite-family scope are accurate and are used to delimit an unsuccessful argument, not as a graph-cover theorem.

These checks support the stated predecessor relationships. They are not an exhaustive search for prior whole-formulation comparison theorems. No assertion that classical spanners, shared SOS2, proportional fairness, cap sets, Bernstein approximation, DC decomposition or weak oracle equivalence originated here was found.

## Executed checks and limits

Executed a Python SHA-256 comparison for all eleven frozen inputs. Also independently checked with exact rational arithmetic the degree-32 box inequalities, both oriented contact violations, the positive-power thirds margins, the oracle-band slack, and seven capacity constants. These checks passed and supplement the proofs; they are not proof substitutes.

I did not run a shared LaTeX build, visually inspect the frozen manuscript PDF, rerun the repository's full supplementary script suite, implement the complete oracle/compiler, or formally verify the proofs. No manuscript, bibliography, original research or literature files were edited. There are no numbered correction findings or unresolved review questions from this pass.
