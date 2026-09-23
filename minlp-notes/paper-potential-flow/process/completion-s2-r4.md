# Independent S2 review — reviewer 4

Verdict: **pass**. No valid major or minor findings identified.

Reviewed the complete 773-line `complexity/sections/04-laws.tex`, with the relevant definitions, structural reductions, algebraic primitives, and recovery arguments in Sections 01–03. Reviewed file SHA-256: `d093dd506dfc56dca3aa3e3a39af2d7bc9f6e841eab4734c6b572c7a833968ff`. No other S2 review reports were read. No manuscript or shared build files were changed.

## Findings

- Major findings: **none**.
- Minor findings: **none**.

## Checks supporting the verdict

1. **Dense polynomial input and admissibility (lines 14–94).** The root partition enumerates only polynomially many univariate derivative roots. Between these roots, each minimizing coefficient endpoint is fixed. Nonnegativity plus the coefficient-identity LP correctly distinguishes strictly increasing laws from laws with a constant interval, including isolated derivative zeros. Refinement by breakpoint unions does not enumerate combinations. Dense degrees and rational coefficient heights remain polynomial in the explicit input.

2. **Transfer of nomination faces (lines 96–137).** Centered convolution preserves the value at zero, monotonicity, and therefore the acyclic physical-flow bound. Adding the positive linear term supplies the positive differential resistances needed by the preceding block-ordering and path-forcing arguments. Compactness gives uniform state convergence without requiring an effective smoothing rate. Fixing parameters at a joint optimizer justifies the same graph-defined face family for joint optimization.

3. **Growing algebraic degree and coefficient recovery (lines 139–170).** Fixed total dimension, rather than fixed polynomial degree, is what makes the sign-vector enumeration and quantifier elimination polynomial. The sample has one common algebraic representation per local core. Recovery uses only polynomially many support cells, subsets of fixed cardinality, fixed-size determinants, and polynomially many sums in that same field. It does not combine the independently generated fields of different blocks.

4. **Polynomial-law pressure and exact arc results (lines 172–310).** The basis bounds have polynomial rational encoding length. The centered smoothing sensitivity proof allows nonmonotone individual bases and signed coefficient intervals. Rational nomination recovery preserves the selected face and balance exactly; independent coefficient rounding stays inside the original intervals. The selected active block supplies all free core nominations, while disaggregation preserves the core objective. Exact arc comparison is confined to the target block, and fixing coefficients before transferring an arc optimizer to pressure faces is valid. The proof correctly avoids claiming rational near-optimal arc inputs for arbitrary polynomial laws.

5. **SRS reduction (lines 318–379).** The circulation equation is strictly increasing and the weak inequality directions, including equality, are correct. For fixed reduced even-denominator `p/q`, the data `c_i=a_i^(q/2)` and `beta_i=a_i^(-(p-1)/2)` contribute exactly `sqrt(a_i)` at zero circulation. Clearing denominators preserves polynomial binary length and the physical root. The distinction between SRS-hard exact comparison, NP-hardness, and additive approximation is maintained.

6. **Quadrature and rational enclosure complexity (lines 394–495).** The truncation bound is uniform at zero. On the radius-one disk about `3/2`, the analytic integrand is bounded as claimed; the Taylor remainder and positive Gaussian weights give the displayed error estimate. Both panel count and quadrature order are linear in accuracy bits for fixed alpha. The Legendre recurrence produces a polynomial-size dense polynomial. Univariate root isolation and the rational weight formula provide polynomial-time enclosures. Taking fixed rational powers increases each individual algebraic degree by only a fixed factor; products within a term still have polynomial degree and height. There is no requirement to form a field containing every node. Upward dyadic rounding preserves positivity and the displayed sensitivity bound gives polynomial precision. Exact normalization and expansion of polynomially many linear factors retain polynomial degree, coefficient height, and construction cost.

7. **Extension to every fixed rational exponent greater than one (lines 497–537): valid.** Odd integer powers are exact. Every remaining exponent has the stated unique decomposition `q=2j+1+2alpha`. Choosing the scaling exponent as a multiple of the fixed denominator makes `T^(2alpha)` rational with polynomial length. Each rational summand is a positive multiple of `x^(2j+3)/(x^2+c)`; its displayed derivative proves strict increase on the whole real line, including across zero. The positive quadratic denominators never vanish. Fixed `j` preserves polynomial dense expansion. This covers exponents above three as well as `(1,3)`, including even integers.

8. **Clearing rational laws in fixed dimension (lines 539–573).** The product of denominators is positive everywhere. Its degree is bounded by a sum of input degrees and its dense multivariate expansion is polynomial because the core dimension is fixed. The additional objective variable and linking equation add only one to fixed dimension/count. The supplied physical path-drop bound can safely bound the objective variable even though the conserved-flow core contains nonphysical points: every feasible cycle-equation solution is a physical state.

9. **Uniform state error and original-law recovery (lines 575–751).** The signed-power increment inequality is correct for both equal and opposite signs. Pairing with the circulation cancels potential gradients. Selecting the largest flow discrepancy yields the stated exponent bound; the two cases below and above one justify using the common fixed integer `H`. The pressure estimate follows from the original-law derivative bound. Original-law nomination and resistance sensitivities, the inverse arc estimate, and the rational LP/disaggregation recovery do not require exact fractional-law state computation. All required precision is polynomial in input size and accuracy bits. The value interval and witness budgets are conservative and correct.

10. **Exact versus additive scope (lines 753–773).** The fixed-family restriction is explicit and necessary for this construction's panel count and fixed powers. The theorem does not imply exact capacity comparison for fractional laws, and does not claim rational physical states. The example `1.852=463/250` has the asserted even denominator.

## Primary-source checks

- [Johansson and Mezzarobba, *Fast and Rigorous Arbitrary-Precision Computation of Gauss–Legendre Quadrature Nodes and Weights*](https://marc.mezzarobba.net/ecrits/JohanssonMezzarobba_Legendre_v3_2018.pdf), Sections 1 and 7.2, supports the supplementary arbitrary-precision enclosure citation. Section 1 explicitly states polynomial bit bounds and the weight formula. The manuscript's algebraic root-isolation argument also supplies an implementation-independent route.
- [Bonito and Pasciak, *Numerical Approximation of Fractional Powers of Elliptic Operators*, arXiv manuscript](https://arxiv.org/pdf/1307.0888), equation (37), Lemma 3.4, and Remark 3.1, has the cited uniform half-line approximation with positive terms. Substituting `lambda=1/t` gives positive fractions vanishing at zero and the stated endpoint extension. Section 3.2 supplies the dyadic Gaussian-quadrature precedent.

The verdict concerns this section's mathematical and bit-complexity arguments and their inspected dependencies. It does not claim implementation benchmarking or an exhaustive historical priority search.
