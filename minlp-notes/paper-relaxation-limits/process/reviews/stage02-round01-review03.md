# Stage 2, round 1, independent review 03

- **Verdict:** PASS.
- **Findings:** No major or minor defect identified in the assigned frozen Stage 2 text.
- **Additional focus:** Boundary means, zero gaps, degree and cutoff endpoints, and degenerate parameters.

## Coverage

I read the frozen files under `process/snapshots/stage02-round01/`: `main.tex`, `macros.tex`, `references.bib`, `sections/01-foundations.tex`, `sections/02-universal-positive.tex`, `sections/03-cubic-equal-means.tex`, `sections/appendix-positive-couplings.tex`, and `sections/appendix-cubic-certificates.tex`. I checked the shared vertex-law, monomial-envelope, deficiency, independence, positive-box transfer, and positive-bilinear arguments used by this stage. I did not re-audit the accepted finite-signing enumeration, which is not a new Stage 2 dependency.

I read `process/review-protocol.md`, `process/stage-02-review-assignment.md`, `process/stage-02-author-assignment.md`, `process/stage-02-author.md`, and the Stage 2 scope rows and shared proof requirements in `process/scope-proposal.md`. I read all ten canonical result files listed by those rows:

- `results/positive-multilinear-gap.md`
- `results/positive-multilinear-degree-upper-bound.md`
- `results/positive-multilinear-sharp-degree-growth.md`
- `results/positive-multilinear-second-order-upper.md`
- `results/positive-multilinear-coefficient-removal.md`
- `results/positive-cubic-gap.md`
- `results/positive-cubic-analytic-family.md`
- `results/positive-cubic-two-level-family.md`
- `results/positive-cubic-rounding-upper-bound.md`
- `results/positive-multilinear-equal-marginals.md`

I also inspected the relevant older source-review corrections, including the analytic Bernstein slack, the alternate two-level parameters, the finite 32/52-variable certificates, zero-gap qualifications, scalar-mixture optimality scope, and the fixed-cutoff reciprocal expansion. These older notes were cross-checks, not proof substitutes. I did not read another current-round report, edit manuscript text, or use subagents.

After reading `literature/AGENTS.md`, I checked Luedtke–Namazifar–Linderoth's local extracted text and original PDF p.22, and Sherali's extracted text and original PDF pp.252–253 (PDF pages 8–9). The original PDFs were read with fresh `pdftotext -layout` extraction where equations in the stored Markdown were missing. I visually read the author's existing image `/tmp/stage02-hoeffding-p5.png`, which reproduces Hoeffding's printed p.16 and Theorem 2, equation (2.6). I did not independently retrieve Hoeffding's PDF or inspect its other pages.

## Independent verification and mathematical evidence

### 1. Shared foundations and zero gaps

The full graph hull reduces to vertex laws because conditional independent endpoint rounding preserves each multiaffine monomial and every mean. The common threshold law attains every positive monomial's upper envelope. Thus a term deficiency is the nonnegative indicator of anchor success and failure elsewhere, and summing term guarantees under one global law is valid even when other components of a mixture are ignored.

At a boundary point, an anchor of mean zero makes its term identically zero under every feasible law; if all nonanchor means equal one, its term is effectively affine. In both cases its term gap and every deficiency vanish. No division by a zero term gap is needed. Fixed nonnegative physical coordinates can be removed, with zero coefficients deleted; if only affine terms remain, both gaps vanish. The transfer to nonnegative boxes uses the correct inequality `T_original <= T_expanded` and equality of full hull gaps. It does not require equality between original and expanded termwise lower envelopes.

### 2. Dyadic construction and its endpoint choices

The support counts and means in `thm:dyadic-exact` give `T=L`, `n=2^L+L`, degree `2^(L-1)+1`, and the stated occurrence count. The upper-tail rearrangement is simultaneous because all anchor payoff functions are increasing functions of the same failure count and the anchors have no mutual constraint beyond their singleton means.

The affine certificate is valid at every real nonnegative failure count. Its integrated constant is `(L-s)2^(-s)`. The resource profiles have expectations `B_q=(L-q+2)2^(-q)` and are supported on equality points of that certificate. Since `B_s>B_(s+1)`, the mixture denominator never vanishes. At a cutoff equality the mixture is simply one profile; either adjacent admissible value of `s` gives the same hull gap. The smallest allowed case, `L=2`, uses `s=1` and gives `H=3/2`. No nonexistent `s=0` or `s=L` is needed.

Bit reversal provides exactly `min(2^j,R)` hit prefixes for each level, and XOR shifts distribute the conditional failure count uniformly across leaves. This closes the gap between the abstract surrogate and the original nested polynomial. The manuscript correctly limits exact attainment to nested partitions. Its arbitrary-partition proof treats `r=0` and zero restricted mass separately; Jensen only weights the set where `r>0`. The dense LP has valid realizations in both directions, including ignoring states of probability zero.

Homogenization preserves the original gaps exactly on the padding face. Continuity gives approximation at interior points, with no assertion that the exact face formula remains true after perturbation. Degree and dimension interpolation use the largest admissible dyadic example and preserve the leading constant for every sufficiently large integer parameter.

### 3. Universal harmonic and older dyadic laws

For every allowed real `M>=d-1`, with integer `d>=2`, one has `M>=1`, `h_p>=p`, and `1<=A_p<=Lambda`. The harmonic probabilities therefore lie in `[0,1]`, integrate exactly to `p`, and use the explicit never-fail convention at `p=0`. At the endpoint `d=2, M=1`, the normalizer is one and the kernel reduces to failure on `U<=p`; no singularity occurs. Low coordinates of mean `1/2` are consistently included in the low class.

When the one-low gap is positive and `p_max<t_e`, the integration interval lies inside the anchor's success interval. An inactive coordinate has `p<t/M`, so omitted mass is at most `(d-1)t/M=eta*t`. On active coordinates the kernel is at least `p/(Lambda*t)`. Conditional independence and the exponential union bound give exactly the displayed curve. If `p_max>=t_e`, `z=1` and the harmonic guarantee becomes zero, as required.

The function `F` decreases continuously from one; at `eta=1` its value at one is zero, without destroying strict decrease of `J` or uniqueness of its root. The convex tangent gives a normalized positive mixture. The crossing proves optimality only for the two scalar guarantee curves, as the text explicitly says.

For the Lambert certificate, direct integration gives

`integral_z^1 (1/v-eta)^2 dv = 1/z-1+2*eta*log(z)+eta^2*(1-z) <= 1/z`.

At `w=1`, the proposed `A=w-1/(2w)` is `1/2`; the logarithmic comparison still holds and the denominator remains positive. The theorem appropriately does not apply that certificate when `w<1`. The tuned cutoff satisfies `Lambda=N+log N` and `eta=1/N`; rescaling its denominator introduces only `O((log N)^2/N)=o(1)`. For the fixed `eta=1` reciprocal refinement, integrating the cubic Taylor remainder bounds the multiplied error by `1/(12*alpha^2)`. The omitted endpoint and logarithmic terms are `O(log Lambda/Lambda)`, and the mean value theorem then yields the claimed `-1/(2w)` correction.

The older finite harmonic bound uses a nonempty interval because `Lambda>=16`; the older leading-constant proof has positive `b-3 log b` for `b>=6`. The distinct dyadic proof has `K=1` at `d=2`; its largest admissible power-of-two choice exists whenever `N(s)>0`. The tail lemma treats `S=0`, `S=u`, and `S>u` correctly. These arguments define laws from the entire marginal vector and degree allowance, independently of the objective's support.

### 4. Coefficient removal and finite sampling

The cloning proof equates entire feasible expectation intervals: group averages followed by conditional independent original rounding give one inclusion, and identical clones within each original group give the reverse. Homogeneity ensures the common factor `m^d`; distinct original supports and clone choices remain distinct.

The vertex and termwise-gap error events use the same independent retention indicators, but their union bound does not assume independence between events. Each summand has range length at most one. The exponent dominates `nm log 2` for the stated fixed `n,s,d` and choice of `K`; the normalized error tends to zero even at the smallest allowance `d=2`. Positive original hull gap justifies eventual division and convergence. No fixed-dimension or deterministic small-support conclusion is asserted.

For the 25,000-variable application, the failure logarithm is negative even after replacing `log 2` by one. The loss in `T-2H` is exactly `5t`, and the remaining normalized margin is `3131/2275-1/2=3987/4550>0`. Nonemptiness and strictly interior means then imply positive hull gap.

### 5. Cubic certificates and continuous inequalities

I replayed the printed frozen finite checker in exact integer/rational arithmetic. Every one of the `7^3+9^3+65^3` count inequalities and all `17^2` two-level inequalities passed, together with primal means, probabilities, equality of objective and affine bound, and displayed ratios. Count symmetry is the mathematical reason these finite checks cover all original binary vertices. Conditional uniform subsets restore every individual mean; checking count means alone without this realization would not suffice.

Independently differentiating the scalar cubic residual gives a positive definite `(a,b)` Hessian with determinant 248. For `c<=3/10`, the boundary stationary point has vanishing `b` derivative and negative `a` derivative, which proves the constrained minimum by convexity. For `c>=3/10`, unrestricted quadratic minimization is a valid lower bound even if the minimizer leaves the square. I independently recomputed those two eliminated polynomials and expanded all five Bernstein rows read directly from the frozen manuscript. Their smallest coefficient is exactly `901/120000`. The lower endpoint consequently reduces to `1610000/743033`. The manuscript correctly distinguishes convergence of these lower certificates from a claim that the actual analytic-family ratios converge to that value.

The two rational two-level identities expand exactly. Their equality atoms have the stated means, and conditional Bernoulli sampling gives the required finite correction in the opposite envelope direction. Thus those actual family ratios are squeezed to their respective limits. The quantitative padding losses, `1840/1000` for the 25-variable weighted example and `120*(20/1000)=12/5` for the 52-variable unit example, require no independence involving padding coordinates. The latter polynomial has exactly 4,320 distinct cubic supports.

For the orientation law, sorted nested exclusions yield the exact sum `sum_j 2^(-j)*a_(j)`; the decreasing-average argument applies down to one nonanchor coordinate. In the cubic three-law proof, the four one-low subcases cover all ordered nonnegative failure means, including equality boundaries. The all-high proof uses increasing functions on the unit interval and avoids division when the term gap vanishes. The quadratic cases are separately supplied. The three limiting test configurations and weights `3/31,4/31,24/31` cancel both free mixture coefficients, proving exactly the limited optimality statement advertised.

### 6. Equal means and source attribution

For `0<u<1`, the adjacent-count distribution handles integral `nu` by assigning zero probability to the second count; it never needs an out-of-range count. The binomial-zero convention covers counts below the degree. Comparing with independent rounding gives `q_(n,d)<=u^d<u`, including `d=n`, so every displayed denominator is positive. At `u=0` or `u=1` all gaps vanish and the ratio theorem correctly excludes these points. Removing a zero nonlinear part is also necessary and explicitly required.

The discrete convexity proof supplies both exact attainment by `E_d` and the common-law upper bound for arbitrary positive polynomials. The floor/ceiling optimizer includes the crossover integer and the `u<=1/2` regime. The dimension-free limit follows by selecting one finite maximizing degree and taking its fixed-degree limit; no exchange of an infinite maximum and a limit is assumed.

Sherali's original equation (13) and Theorem 3 match the displayed whole-cube formula with his degree parameter renamed `d`. Luedtke's original p.22 gives precisely the positive-coefficient nonnegative-box conjecture contradicted by the dyadic family. Hoeffding's theorem uses independent bounded summands and the squared range-length denominator; applying it to the average and then rescaling gives the manuscript's two-tail specialization. The manuscript also proves the needed specialization directly.

## Verification artifacts

`verification/reviewer03/stage02-round01/check_exact.py` and its log contain the finite-checker replay and independent checks of:

- Direct interval integration of the actual orientation and cubic failure laws on 546 rational quadratic/cubic tuples, including 128 zero-gap cases.
- Dyadic resource profiles and every cutoff tie for `L=2,...,30`.
- Equal-mean formulas near both boundary means, at integral `nu`, and across all degrees for dimensions through 14.
- The exact finite sampling margin and negative failure logarithm bound.

`verification/reviewer03/stage02-round01/check_symbolic.py` and its log contain independent symbolic elimination, exact expansion of the actual frozen Bernstein rows, the slack and reduced lower endpoint, and both two-level identities. All checks passed. Finite grid checks are supplementary sanity checks; the continuous coupling claims rest on the preceding universal proofs. The finite integer count certificates, by contrast, are exhaustive for their explicitly finite original vertex problems.

## Remaining limits

I found no missing item explicitly required by the Stage 2 assignment and author ledger. Later-stage material and the planned introduction/abstract integration are outside this round. I did not independently rebuild or visually audit the complete manuscript PDF; this review addresses mathematical content and source matching. The finite-signing appendix remains accepted background.

I make no publication-priority or literature-absence claim. My direct Hoeffding source inspection is limited to the existing image of the theorem page. The exact cubic supremum, optimal finite-degree constants, a matching second-order lower asymptotic, and optimality over broader coupling families remain open as stated; none is needed for the proved results.
