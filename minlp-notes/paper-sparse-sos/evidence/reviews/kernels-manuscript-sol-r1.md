# Independent manuscript review: Sections 3–5

Reviewer: Sol, independent of the authors of these sections. Date: 2026-10-05.

## Verdict and scope

The revised Sections 3–5 support their mathematical claims. I found no unresolved fatal or major proof gap. The proofs establish the full-preordering inverse-square bound, the ordinary-module finite-order bound and fixed-width logarithmic inverse-square rate, the fixed quadratic separator obstruction, and the exact values at orders one and two. The claims remain distinct: the preordering example has a proved exact inverse-square rate; the ordinary-module example has an inverse-square lower bound and the stated logarithmic inverse-square upper bound.

Six issues in the first snapshot required correction. Their dispositions appear below. The author applied the repairs, and I inspected those edits once against the proofs. The final verdict applies to the revised hashes, not to an unspecified moving draft.

This review covers `sections/03-kernels.tex`, `sections/04-ordinary.tex`, and `sections/05-sharpness.tex`, using the current setting and macros. I compared the written proofs with `evidence/AUDIT-KERNELS.md`, the kernel and exact-consistency source notes, and the quadratic sharpness and exact-gap source notes. I also read `evidence/BRIEF.md` and `evidence/ARCHITECTURE.md`. Literature verification belongs to Luna and is outside this review. No experiment, archived numerical recalculation, build, CI inspection, or project-wide check was performed. I edited only this review.

## Snapshot record

SHA-256, first snapshot of the three reviewed sections:

| File | Hash |
| --- | --- |
| `sections/03-kernels.tex` | `66a236a3e4e41bbd2d8818152e1832a873d8dabc6ab3d274737c56c325acda03` |
| `sections/04-ordinary.tex` | `da0c19fa37ded950c7998a89db2a6210bf7776cae92b779438b059fae801bbe3` |
| `sections/05-sharpness.tex` | `422f8173034988914a5fa2848f6a37150adfa1d98810f745f61d1d64c71590a4` |

SHA-256, revised snapshot inspected for the final disposition:

| File | Hash |
| --- | --- |
| `sections/02-setting.tex` | `6db76f3db9195300a335e61feba66c387692e4e40dc59951fb2b50b020e8936b` |
| `sections/03-kernels.tex` | `aa99f3f741b7fd0d61d4bd395b4a4f236589952d1c721645aac6985f7f1c8a2a` |
| `sections/04-ordinary.tex` | `ca6da25fad4c8f14502e8599d96ecac40e327fd858bf49fd47a3712f07355197` |
| `sections/05-sharpness.tex` | `92835b3988400ec22a363886b66abe8663cd9ca341d1f97d3b5f545e033588f9` |
| `macros.tex` | `00b454c4dcc72727d78c77817d3cab911a3d7f2205efd4af467a9407e27c04bb` |

The source audit used here has hash `c3529d3e5c118b083e92b0a6fc6464a9798abb0450f8189d322cfa6d33518b52` (`evidence/AUDIT-KERNELS.md`). Original locators in the findings refer to the first snapshot; revised locators refer to the second table.

## Findings and repairs

### R1. Grid comparison overstated for an arbitrary feasible point — moderate, resolved

Original locator: `03-kernels.tex:387–388`, following `cor:pre-grid`.

The text said that the grid optimum was within the rounding error of every feasible SDP objective. Rounding proves only

`grid optimum <= L(f) + error`

for an arbitrary feasible moment family. A feasible objective can be far above the grid optimum, so the reverse inequality cannot hold in general.

The necessary repair was to state the one-sided comparison for every feasible point and reserve the two-sided comparison for an optimal SDP point. For that point, `rho_r <= f* <= grid optimum` supplies the missing side.

Revised locator: `03-kernels.tex:387–389`. The text now makes exactly this distinction. Resolved.

### R2. Empty bags lacked a defined correction constant — moderate, resolved

Original locator: `04-ordinary.tex:404–408`, definition of `Delta_v`.

The setting permits individual empty bags, but the definition began at `v >= 1` and the proof later used `Delta_{v_b}`. Define the empty sum for every `v >= 0`; then `Delta_0 = Delta_1 = 0`. The empty-bag density is the scalar one and needs no correction. The common correction by `Delta_w` still works because `Delta_v` is nondecreasing from zero.

Revised locators: `04-ordinary.tex:409–414` and `:440–444`. Both conventions are explicit. Resolved.

### R3. The normalization obstruction needed its exact hypotheses — moderate, resolved

Original locator: `04-ordinary.tex:234–245`, `rem:normalization-obstruction`.

The unrestricted statement that an SOS kernel cannot be exactly normalized is false: the constant kernel one is normalized and SOS. The leading-source-coefficient argument instead proves that a globally SOS polynomial kernel with exact normalization against a measure of full interval support must be independent of the source variable. A nontrivial approximation kernel with source dependence is therefore excluded by these hypotheses.

This argument also does not exclude kernels certified nonnegative only on the interval by its quadratic module. The Jackson kernel of Section 3 is an explicit reason to preserve that distinction. An ordinary module can contain individual interval certificates, but products of those certificates need not belong to the multivariate ordinary module.

Revised locator: `04-ordinary.tex:236–251`. The title and proof now specify global SOS, source dependence, the constant-kernel exception, and the interval-certificate distinction. Resolved.

### R4. Nonnegativity of the weight cited an inapplicable subclaim — minor, resolved

Original locator: `04-ordinary.tex:350`, proof of `lem:residual-products` part (b).

Part (a) proves positivity only when the number of residual factors is at most one. Part (b) holds for every set of residual factors. Its lower bound follows directly because `G` is a product of SOS kernels and hence SOS within the degree budget.

Revised locator: `04-ordinary.tex:355`. It now cites the SOS representation at the start of the proof. Resolved.

### R5. Intermediate Fourier equality omitted a factor one half — moderate, resolved

Original locator: `05-sharpness.tex:168–170`, proof of `lem:fejer-lower`.

The integral of `cos^2(theta) cos(k theta)` over `[0, pi/2]`, divided by pi, is

`sin(k pi/2)/(2 pi) * (1/k - k/(k^2-4))`

for odd `k >= 3`. The first snapshot omitted the factor one half in this middle expression. Its final coefficient `-2 sin(k pi/2)/(pi k(k^2-4))` was already correct, as were the final lower-bound constants.

Revised locator: `05-sharpness.tex:168–170`. The middle equality now contains `1/(2 pi)`. Resolved; no theorem constant needs changing.

### R6. Calibration prescription incorrectly covered the alternate row — minor, resolved

Original locator: `04-ordinary.tex:561–566`, `rem:calibration`.

The surrounding prose attributed the displayed prescription to all table rows even though the last row uses a different pair of parameters. The necessary repair was editorial: limit the prescription to the first three rows and state that the last row is an alternate choice. I did not recompute the numerical entries.

Revised locator: `04-ordinary.tex:570–577`. The description now identifies the first three rows and the final alternate pair. Resolved.

## Section 3: proof and contract verification

### Kernel and truncated positivity

Locators: `lem:jackson` (`03-kernels.tex:58–125`), `lem:pre-density` (`:135–195`), and `rem:ker-degree` (`:197–222`).

The triangular coefficients and their autocorrelation produce a nonnegative trigonometric polynomial. The normalization `a_0 = (2m^3+m)/3` and the identity `a_0-a_1=m` give the displayed damping constant. The inequality `1-cos(k theta) <= k^2(1-cos theta)` also covers frequencies beyond the kernel support, where the multiplier is zero. Thus the assertion for all frequencies is proved rather than inferred from the supported ones.

The averaged circle kernel is a polynomial in the two cosine variables, is nonnegative on the box, and preserves the arcsine mass identically as a polynomial in the source variable. Its Chebyshev action is diagonal. These facts alone would not prove positivity of a pseudomoment density. The written proof supplies the needed interval certificates and then tensors them: for a set `I` of box generators, the square factor has degree at most

`v(m-1) - |I| <= r - |I|`.

The full product term therefore belongs to the order-r preordering. This is exactly the constraint tested by the truncated functional. The proof does not silently give a representing measure to that functional. The counterexample in `rem:ker-degree` correctly explains why pointwise positivity without this degree-bounded certificate is insufficient.

### Mass, separators, objective, and width

Locators: `lem:pre-density`, `thm:pre` (`03-kernels.tex:231–285`), and `rem:ker-gluing` (`:287–302`).

Mass preservation is a polynomial identity, so local densities have mass one without an assumption about measures representing the original moments. For each separator, the transformed source polynomial has degree at most `2|S|(m-1) <= 2r`. Edge consistency can therefore be applied to that very polynomial. The resulting separator densities agree identically, which is stronger than equality of finitely many output moments.

The objective comparison uses the Section 2 Chebyshev moment estimate only for degrees at most r. The stated standing condition `d <= r` supplies this margin; merely putting the objective in the degree-2r coefficient space would not suffice. Tensor damping is bounded by summing the coordinate damping errors. This gives the exact `3A/(2m^2+1)` budget with no additional factor counting bags or edges.

For `m=floor(r/w)+1`, every bag satisfies `v(m-1) <= r`, and `m > r/w` gives the displayed coarser inverse-square constant. The parameter works at every allowed integer order, including `m=1`. Individual empty bags cause no difficulty: products are one and their density is one.

The explicit conditional gluing formula deals with zero separator density by choosing an arbitrary reference conditional measure there. Nonnegativity and the zero integral over that fiber ensure that this does not alter any required marginal. The running-intersection tree then produces the global law. No separator multiplier or infinite-dimensional dual attainment is invoked.

### Finite grid extraction and certificates

Locators: `lem:ker-quadrature` (`03-kernels.tex:311–330`), `cor:pre-grid` (`:332–392`), and `cor:pre-certificate` (`:394–414`).

The cosine midpoint grid integrates the first `2N-1` Chebyshev degrees exactly. The proof of the geometric sum handles even and odd frequencies; the complex sum need not itself vanish for odd frequencies, but its real part does. The tensor rule then integrates each density, objective times density, and separator marginal exactly.

The choice `N_g=m+floor(d_infty/2)` satisfies

`2N_g-1 >= 2m-2+d_infty`

for both parities of `d_infty`. Hence it covers the output degree of `f_b h_b`. Grid probabilities have mass one and exactly agreeing separator marginals. A global grid law has expected objective within the rounding error, and its support contains a point no worse than that expectation. R1 records the precise comparison with an arbitrary feasible input objective.

The stated dynamic-programming count is a table-operation bound after the bag tables are formed. Summing `children(b)+1` over the tree gives `2t-1`, hence at most `2t N_g^w` elementary comparisons/additions at that stage. The text does not turn this into a claim about an arbitrary MINLP or SDP solution time.

The certificate uses finite box SDP dual attainment from Section 2. Starting with the attained certificate at `rho_r`, add the nonnegative scalar `rho_r-f*+E` to one bag. This proves membership of `f-f*+E` in the stated truncated sparse cone. It is a real-coefficient finite-dimensional certificate. It does not assert rational coefficients or polynomial attainment in a different, infinite-dimensional separator dual.

## Section 4: proof and contract verification

### SOS kernel, normalization, and approximation degree

Locators: `lem:sos-kernel` (`04-ordinary.tex:86–122` and its proof following `lem:mod-defect`), `lem:mod-defect` (`:124–172`), `rem:normalization-obstruction`, and `lem:mod-signed` (`:269–318`).

The squared Fejer kernel has a mass polynomial between `C_s/2` and `C_s`, with `C_s=(2s^2+1)/(3s)`. The residual parameter therefore lies between zero and one half on the interval. The finite geometric-series identity for even N represents the correction polynomial as a sum of squares, with square-factor degree `(s-1)N`. Multiplication by the initial SOS kernel yields the stated source degree

`D=2(s-1)(N+1)`.

The mass `omega=pM` is globally SOS, now stated explicitly. Its residual `varrho=1-omega` is nonnegative only on the interval in the proof and bounded there by `delta=2^{-(N+1)}`. Global nonnegativity of this residual is unnecessary and should not be inferred. The normalized signed operator preserves constants exactly.

I checked the defect identity by pairing the two Fejer coefficients indexed by l and l+k. The difference-of-squares terms and the unpaired low-frequency terms give the stated coefficient-norm bound

`k^2/s^2 + 3k^2/(2s)`

for `k <= s`. Endpoint summands with vanishing coefficient are harmless. The kernel coefficient budget is `Lambda=s^2(N+1)/C_s`; the residual coefficient norm follows from orthogonality and weighted Cauchy–Schwarz, using its degree D and interval supremum delta. This gives the stated `sqrt(2(D+1)) delta` term.

Some separate summands in the approximation identity may have degree above D. The manuscript explicitly applies the moment functional only to their combined difference, whose degree is at most D for `k <= s <= D`. This distinction is necessary and is present. For the tensor operator, the combined polynomial has degree at most `vD <= r`; hence the Section 2 moment coefficient estimate applies. The original objective also has degree at most `v d_infty <= vD` under the theorem hypotheses.

Separator consistency uses the exactly normalized signed operator, with source degree at most `|S|D <= r`. It is not an approximation statement about separator masses.

### Weighted Cauchy–Schwarz and one-generator certificates

Locators: `lem:residual-products` (`04-ordinary.tex:331–387`) and `tab:mod-ledger` (`:390` onward).

Write `G` for the product of the SOS kernels in the nonresidual coordinates and `H` for the product of j residuals. Then `G=sum q_l^2`, with `deg q_l <= (v-j)D/2`.

The j=0 and j=1 terms are nonnegative under an ordinary-module functional: the former is SOS; the latter multiplies an interval certificate for one residual by G and uses at most one box generator. The total degree is at most vD.

For general j, the telescoping identity for `delta^{2j}-H^2` uses one factor `delta^2-varrho_i^2` at a time and only squares of previously encountered residuals. The interval certificate for that factor has degree at most 2D. After multiplication by G and those squares, its complete term has degree at most

`(v-j+2l)D <= (v+j)D <= 2r`.

Each localizing term contains one generator, with multiplier degree at most `2r-2`. There is no unlicensed product of distinct box generators. Also `GH^2` is SOS because `deg(q_l H) <= (v+j)D/2 <= r`.

The same degree bound makes `L(G(a+cH)^2)` nonnegative for every real a,c. The resulting two-by-two PSD form gives

`|L(GH)|^2 <= L(G)L(GH^2) <= delta^{2j}L(G)^2`.

The proof includes `L(G)=0` without division. Nonnegativity of `L(G)` comes from its SOS representation, as corrected in R4. Its upper bound uses the Chebyshev coefficient budget and `deg G <= r`, not a nonexistent degree-2r moment coefficient bound.

### Common correction and finite-order rounding

Locators: definition of `Delta_v` (`04-ordinary.tex:409–414`) and `thm:mod` (`:416–484`).

Only terms with at least two residual factors contribute to the negative-density bound. Summing their absolute upper bounds gives

`Delta_v=sum_{j=2}^v binom(v,j) delta^j Lambda^{v-j}`.

The recurrence `Delta_{v+1}=(Lambda+delta)Delta_v+v Lambda^{v-1}delta^2`, together with `Lambda >= 1` and `Delta_0=Delta_1=0`, proves monotonicity. A single `Delta_w` thus corrects every bag, including bags of different sizes and empty bags.

Adding that same multiple of the product arcsine density and dividing by `1+Delta_w` preserves all separator marginals exactly. Bag-dependent correction sizes would generally break this equality; the common correction is doing essential work.

The correction error is bounded using two true probability laws. From

`I_+ - I_bar = Delta_w (I_ref-I_+)`,

its magnitude is at most `Delta_w osc(f_b)`. This avoids incorrectly applying a range bound to the signed expectation `I_bar`. Summing gives the finite-order error `sum_b C_b Gamma_{v_b} + Delta_w W`, and then `C_f(Gamma_w+2Delta_w)`. Constants in each `f_b` cancel. No extra bag or edge factor has entered beyond the chosen summed objective budget.

### Parameters, constants, and every sufficiently large order

Locators: `cor:mod-rate` (`04-ordinary.tex:496–560`), the discussion at `:562–568`, and `cor:mod-certificate` (`:598–615`).

The parameter choice is explicit:

`c_w=max(3,(w+1)/2)`, `ell_r=log_2(r+2)`,

`s=floor(r/(2w(c_w+3)ell_r))`, `N=2ceil((c_w/2)log_2 s)`.

The first threshold gives `s >= max(2,d_infty)`. It also gives the degree constraint at the actual order r, because `N+1 <= (c_w+3)ell_r` and `wD <= 2ws(N+1) <= r`. This establishes a bound for every sufficiently large integer order, not merely a selected subsequence.

The smoothing estimate uses `delta <= s^{-3}/2`, `C_s >= 2s/3`, and `D+1 <= 2s(N+1)`. They give

`eta <= (3d_infty^2+1)(N+1)/s^2`.

The floor estimate `s >= r/(4w(c_w+3)ell_r)` supplies the factor 16. The second threshold implies `w eta <= 1`, so `Gamma_w <= e w eta`. The resulting first coefficient is exactly the displayed `16e w^3(3d_infty^2+1)(c_w+3)^3`.

Taylor's formula gives `Delta_w <= binom(w,2) delta^2(Lambda+delta)^{w-2}`. Using `Lambda+delta <= 2s(N+1)` and `2c_w >= max(6,w+1)` gives

`Delta_w <= binom(w,2) 2^{w-4}(N+1)^{w-2}/s^3`.

Multiplying by two and inserting the floor bound yields the displayed second coefficient `binom(w,2) 2^{w+3}w^3(c_w+3)^{w+1}` and power `ell_r^{w+1}/r^3`. For fixed w this is smaller than the leading `ell_r^3/r^2` term. The proof and interpretation correctly make no growing-width assertion. If `C_f=0`, the objective is a sum of constants and the hierarchy is exact; no asymptotic parameter choice is needed.

The finite ordinary-module certificate again relies on the attained finite box dual in Section 2. Replacing its finite-order error by a larger displayed rate bound only adds a nonnegative scalar SOS term. R6 is solely a description of existing calibration records, which were not independently rerun.

## Section 5: proof and contract verification

### Moment matching and the local-measure value

Locators: `lem:moment-matching-general` (`05-sharpness.tex:32–64`) and `prop:moment-matching` (`:102–122`).

The Hahn–Banach and Riesz argument produces a signed annihilating measure of total variation one when the approximation error is positive. Constants belong to the approximation space, so the positive and negative Jordan masses are each one half. Scaling them to probability measures explains the factor two in the matching-measure extremum. The zero-error case is separately harmless.

For the example, minimizing the first local objective over its private interval gives `-varphi(y)` and minimizing the second gives `varphi(y)`. Lifting the matched separator measures along these minimizers preserves all separator moments and uses actual local measures on the rectangles. Consequently `v_n=-2E_n(varphi)` and

`rho_r^mod <= rho_r^pre <= v_{2r}`.

These inequalities do not establish equality at arbitrary finite orders, and the manuscript does not treat them as doing so. The identity `f=(y-x+z)^2+2xz` verifies the true optimum zero independently.

### Explicit Fourier lower bound

Locator: `lem:fejer-lower` (`05-sharpness.tex:126–192`).

The chosen even N lies between `n+1` and `n+2`. All frequencies of the witness exceed n, so Chebyshev orthogonality proves annihilation. Its signed density is the even part of a shifted sine times a Fejer kernel; reflection and the triangle inequality bound its total variation by one. That is the needed normalization, rather than a bound on its pointwise size.

After R5, the exact Fourier coefficient is `-2 sin(k pi/2)/(pi k(k^2-4))`. The chosen signs make every retained contribution positive. The sum of the positive odd weights is `N/2`; their frequencies are less than `3N`. The displayed integral is therefore at least `1/(27 pi N^2)`. Normalizing the two Jordan parts, whose common mass is at most one half, gives an expectation difference at least twice that number. Division by two in the moment-matching lemma leaves

`E_n(varphi) >= 1/(27 pi(n+2)^2)`.

For `n=2r`, the local-measure gap is at least `1/(54 pi(r+1)^2)`. All positivity strengthenings accepting actual local measures inherit this separator lower bound.

### Sharp rate, dense certificate, and finite sparse nonattainment

Locator: `thm:quad-sharp` (`05-sharpness.tex:196–282`).

After affine normalization of the two private intervals, the Chebyshev weighted budgets are `A_1=4`, `A_2=6`, and `A=10`; the coefficient budgets are `21/8` and `25/8`, totaling `23/4`. Substitution into Section 3 gives the stated preordering upper bound and its coarse `60/r^2` form. Together with the lower bound this proves the exact inverse-square order for that cone and for the matching local-measure value. Section 4 supplies the qualified logarithmic inverse-square upper bound for the ordinary module.

The dense order-two identity uses products of generators, with complete terms of degree at most four. It is a dense preordering certificate. The alternate degree-one endpoint generators give the stated lower-degree dense preordering interpretation. Neither construction proves an ordinary-module certificate where a generator product is absent.

The argument excluding a finite sparse certificate for f itself forces a polynomial separator function to coincide with the nonpolynomial fiber value `varphi`. This concerns the zero gap certificate. It is consistent with attainment of the finite SDP dual at its strictly negative value. The written proof keeps those claims separate.

### Order one

Locator: `prop:exact-orders` (`05-sharpness.tex:297–350`).

The sum of the explicit bag identities certifies `f+1/4` in the ordinary order-one module. The two cones coincide at this order because the product of two quadratic generators has degree four.

The upper witness integrates a positive measure with an atom outside the rectangle. This is acceptable here: its degree-two moment matrix is PSD and the only localizing tests are the scalar generator expectations, which are zero and one quarter. Reflection gives matching separator moments zero and three quarters, and the total objective is minus one quarter. The manuscript explicitly distinguishes this truncated functional from a local measure supported on the bag.

For the local-measure value, `S_1(y)=y^2/2+(sqrt(2)-1)y` has four alternating extremal errors of magnitude `(sqrt(2)-1)^2/2`. A strictly better quadratic would differ from it by a degree-two polynomial with three sign changes, which is impossible. This proves `v_2=-(3-2sqrt(2))` without a numerical approximation calculation.

### Order two: approximation, Gram identity, and witness

Locators: `05-sharpness.tex:352–433`, especially `eq:shp-p-identities` and `eq:shp-gram`.

The two polynomial identities prove `0 <= p_star-varphi <= 2E_star` and give six alternating extrema. The sign-change argument then proves both `E_3=E_star` and `E_4=E_star`, with `E_star=7sqrt(3)/9-4/3`. There is no reliance on an imported numerical best-approximation assertion.

I checked the Gram identity independently by grouping coefficients in x and using `s^2=3`, where `s=sqrt(3)`. The coefficients of powers zero, one, and two are respectively `p_star(y)`, `-2y`, and one; the coefficients of powers three and four vanish. Useful reductions include `b^2=4-2s`, `b^3=2a`, `(b+1)(b+a)/b=3b`, `k_star b^2=c_star/2`, `k_star(b+a)^2=s/6`, and `k_star(b+a)b=(s+1)/12`. These recover the stated entries and cross terms.

The displayed principal minors of `G_0` and `G_1` are correct and positive. The degree-two vector V gives an SOS of degree four, and the affine vectors U and Z multiply one quadratic generator at a time. Thus the identity is in the order-two ordinary module, not merely nonnegative on the rectangle. Reflection and the second polynomial identity certify `f+2E_star`.

The witness masses are positive and sum to one. Their odd separator moments of degrees one and three vanish; reflection automatically preserves the even moments. The writer has expanded these identities in the revised proof. The lifted local measures have objective

`-w_b b^2+w_{-1}+w_{-a}a^2=-2E_star`.

The certificate and witness sandwich therefore proves `rho_2^mod=rho_2^pre=v_4=-2E_star`, without an SDP solver or dual-attainment assumption.

### A nonnegative majorant need not be a low-order module certificate

Locator: `rem:shp-majorant` (`05-sharpness.tex:436–458`).

At the indicated zero, the assumed order-one representation forces the affine SOS factors to vanish and removes the second generator coefficient. Comparing the coefficients then gives the three Gram sums in the proof. Cauchy–Schwarz would require `1 <= 1/2+(sqrt(2)-1)=sqrt(2)-1/2 < 1`, a contradiction. This is a valid degree-specific nonmembership example; it does not deny a certificate at a higher order.

The statement about higher-order equality is explicitly open. Existing computational records are described as evidence, not used as a theorem proof.

## Dependencies and final disposition

The proof contracts use the running-intersection property, normalized and exactly consistent local truncated functionals, the stated box cones with complete degree bounds, and the degree-r Chebyshev moment estimate. Section 3 needs the full preordering; Section 4 needs the ordinary module and its stricter `r >= wD` margin. Section 5 lower witnesses use actual local measures except for the clearly identified order-one truncated witness.

The finite certificate corollaries use the finite sparse coefficient quotient and strict feasible box moment family from Section 2. These differ from recourse duality: the private-degree-two recourse cone is not asserted closed, and its separate order-unit argument establishes a supremum and certificates for every strict `lambda < rho`, without boundary attainment. Nothing in Sections 3–5 improperly imports finite box attainment into that recourse statement.

The revised setting permits individual empty bags; Section 4 now has the required zero-dimensional convention. Purely private examples can be embedded using the explicitly allowed unused shared coordinate. The all-discrete order-zero extension belongs to its separately stated hierarchy and is not implicitly covered by the positive-order box theorems.

The local proofs are present in the main sections and are readable without the research notes or this evidence directory. Standard measure representation, finite-dimensional separation, and interval SOS facts are supplied or clearly isolated in the setting. Source or priority verification remains a separate literature task.

Actual targeted checks were scoped `rg -n` locator searches, `sed -n` proof reads, `wc -l` snapshot inspection, and `sha256sum` on the reviewed files. The first `wc` also confirmed that this report did not yet exist. No test suite or build was run. All six required repairs are resolved in the revised snapshot; no further mathematical repair is requested by this review.
