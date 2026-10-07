# Final independent GPT proof review: setting, kernels, and sharpness

Date: 2026-10-05. Reviewer: GPT, independent of the manuscript writers.

## Verdict and limits

**The current Sections 02–05 pass this mathematical review.** I found no unresolved fatal, major, or moderate proof defect, and no source edit is required by this review. I independently reconstructed the theorem chain rather than relying on previous acceptance: finite box SDP duality; full-preordering compatible-density rounding; the ordinary-module signed-density transfer and its explicit parameter bounds; the fixed quadratic lower bound; and the exact order-one and order-two values. A separate GPT subreviewer reconstructed Section 05 and obtained an additional independent hand check of its Gram identity. Their agreement supplements the derivations below.

The verdict applies to the hashes below. It is a scoped proof verdict, not acceptance of the entire submission, a machine-checked proof, or a publication-priority verdict. I also checked the abstract, introduction, and discussion claims that summarize this chain. The later recourse, regularity, extension, and rationalization proofs are assigned to other reviewers; their front-matter summaries are not independently proved by this review. A final hash check detected concurrent revisions to Sections 00, 01, 05, and 10; I reread those revised files and checked the added order-one nonrepresentability argument before recording the final hashes.

The paper now states the necessary distinctions correctly: a feasible truncated functional need not be a measure; the objective of an arbitrary feasible moment family need not be a lower bound; the exact local-measure relaxation need not equal the finite SDP; ordinary modules do not license generator products; and attained finite box SDP certificates do not establish boundary attainment for private-degree-two recourse. The ordinary-module bound is uniform in bag count and tree shape only after retaining the specified local coefficient budget, with width and degree fixed.

The missing completed bibliography and final literature ledger are integration dependencies, not defects in these proofs. I used the supplied `LITERATURE-PRELIMINARY.md` and retained source notes for attribution boundaries. I did not browse, retrieve primary sources, conduct new literature research, rerun experiments or historical checkers, build the paper, inspect CI, or run project-wide verification. Numerical calibration entries were treated as retained records and were not recalculated.

## Scope and snapshot

I read `AGENTS.md`, `evidence/BRIEF.md`, `main.tex`, `macros.tex`, all of Sections 00–05, and Section 10. The primary mathematical comparisons used `sparse-kernel-rounding.md`, `sparse-putinar-kernel.md`, `sparse-putinar-exact-consistency.md`, `quadratic-sharpness.md`, and `quadratic-exact-gap-frontier.md` in `research-20260928/solver`. I inspected the previous setting and kernel review evidence to identify previously fragile steps, then rederived those steps in the current source. Prior review conclusions were not used as mathematical premises.

Current manuscript SHA-256 hashes:

| File | SHA-256 |
| --- | --- |
| `main.tex` | `206dd022e955dc7981b3e400cce0d05060c5181dd10b73c8e93eb864888331df` |
| `macros.tex` | `00b454c4dcc72727d78c77817d3cab911a3d7f2205efd4af467a9407e27c04bb` |
| `sections/00-abstract.tex` | `62d688f2d5b10d9e69c1cc6df5155c62f3d14db79c25c7864bbf55347eae5aee` |
| `sections/01-introduction.tex` | `51384bd368b9ab33f4d8b2da423b1faa5c98be6fbffc97c3ed48b0d1d3e364d5` |
| `sections/02-setting.tex` | `6db76f3db9195300a335e61feba66c387692e4e40dc59951fb2b50b020e8936b` |
| `sections/03-kernels.tex` | `aa99f3f741b7fd0d61d4bd395b4a4f236589952d1c721645aac6985f7f1c8a2a` |
| `sections/04-ordinary.tex` | `c259609d74d3ef5520d2bf1773eb363391c119ec2df0202abf278aa0191556e4` |
| `sections/05-sharpness.tex` | `d9e05f07c613115c042ba16121fdd371609c996c4720d37870418cef5a3706a3` |
| `sections/10-discussion.tex` | `db5d120d53ea703679191cfa8ada8b43513fedd0827157bfad9434526e037dcb` |

Evidence and primary mathematical source-note hashes:

| File | SHA-256 |
| --- | --- |
| `evidence/BRIEF.md` | `613c8c829190c229d570bf572efcdadf5ee8b7d09dfc5d984871281b7c379c85` |
| `evidence/LITERATURE-PRELIMINARY.md` | `28e6a49a5b60663366bfc9aed098214bf8e3275389bc0d65b47d53ca5bc145fa` |
| `solver/sparse-kernel-rounding.md` | `36535218c51a68540c3bfac6bcf028e0ccacdf4374c5ff7f4654c954fc7e70cb` |
| `solver/sparse-putinar-kernel.md` | `5922329756f9e436366eb29c3675bf1b129743053d11cc43259f6247839e736b` |
| `solver/sparse-putinar-exact-consistency.md` | `a3a63e51fafc751ea9ff1e25c42991bdc0a1fe8bcbe34d8150426f41cf353cfc` |
| `solver/quadratic-sharpness.md` | `a2a2ba6c8c186a9fcf5bfe0f4ccc96fb0efe2305ac399dec529a22ee01795bf4` |
| `solver/quadratic-exact-gap-frontier.md` | `d8eaecfac46d171341879320f7480714f4d74f098c2a21842eb1b0366fb95b83` |

## Findings by severity

| Severity | Unresolved findings |
| --- | --- |
| Fatal: central result false or unavailable | None found |
| Major: material missing proof or hypothesis | None found |
| Moderate: incorrect finite-order constant, domain, or comparison | None found |
| Minor requiring a correction | None found |
| Integration dependency outside this proof verdict | Final bibliography, source locators, and literature/priority reconciliation |

In particular, the degree margins, weighted Cauchy–Schwarz argument, empty-bag convention, normalization obstruction, grid comparison, Fourier factor one half, and exact-order witnesses are checked in their current form. Their presence is not accepted merely because they were listed as repaired in earlier reviews.

## Section 02: finite-dimensional contracts

### Polynomial consistency, cones, and weak duality

Locators: `02-setting.tex:56`, `lem:zero-decomposition`; `:140`, `def:cones`; `:167`, `def:sparse-hierarchy`; `:198`, `lem:weak-duality`.

The leaf-removal proof of decompositions of zero is correct. A monomial using a leaf coordinate outside its parent separator can occur in no other bag, so the entire leaf polynomial depends only on the separator. Moving it to the parent preserves the degree bound and running intersection. Constants, subset bags, and empty bags do not invalidate the argument. This supplies the polynomial cancellation needed for weak duality and identifies the finite SDP dual with the displayed sparse certificate cone.

The ordinary cone allows only the constant SOS term and one generator at a time. The full preordering allows products indexed by subsets and reduces the degree available to the square by the number of generators. Negative allowances are explicitly absent. Thus every tested polynomial lies in the degree-2r space, and the matrix-count distinction is correct.

The inequalities between the four values have the right directions. A point evaluation is a feasible preordering family; a preordering-positive family is ordinary-module-positive; and an ordinary certificate is a preordering certificate. Applying the zero-decomposition lemma cancels every separator contribution under a feasible family. No lower-bound claim is made for the objective of an arbitrary feasible family.

### Cauchy–Schwarz, half-degree Chebyshev bounds, compactness, and Slater

Locators: `02-setting.tex:230`, `lem:moment-cs`; `:241`, `lem:cheb-moment`; `:268`, `lem:compact`; `:288`, `lem:slater`.

The moment Cauchy–Schwarz statement uses a specified polynomial space and weight. Its zero-norm implication is valid for a PSD bilinear form and does not require division. Later applications must establish positivity for their chosen space; Section 04 does so explicitly.

For `|alpha| <= r`, the identity for `1-T_alpha^2` has one generator in each summand and a square root of degree at most `|alpha|-1`. It belongs to the ordinary module of order `r`. Together with moment PSD this proves both `0 <= L(T_alpha^2) <= L(1)` and `|L(T_alpha)| <= L(1)`. The proof does not pretend to bound all degree-2r Chebyshev moments this way.

Compactness is proved independently in monomials. Repeated generator tests lower `L(x^(2alpha))` to `L(1)` when `|alpha| <= r`; every monomial through degree `2r` splits into a product of two monomials through degree `r`, so moment Cauchy–Schwarz bounds its absolute value by one. The feasible family is nonempty, closed, and bounded. This proves finite values and primal attainment for both box SDPs without a representing-measure assertion.

The common product-arcsine family satisfies all separator equalities and makes every permitted moment and localizing matrix positive definite: each nonzero square times its permitted generator product has positive integral on the open box. Empty bags contribute a positive one-by-one constant matrix. The finite conic dual consists of local cone memberships plus scalar normalizations and polynomial separator multipliers. The zero-decomposition lemma supplies the converse identification, not just one direction. Primal strict feasibility and a finite optimum yield no gap and attained dual certificates. Redundant affine consistency equalities do not undermine this PSD strict-feasibility condition.

### Interval certificates, gluing, and rectangular scope

Locators: `02-setting.tex:328`, `lem:interval-sos`; `:359`, `lem:gluing`; `:400`, `def:rec-model`; `:441`, `def:rec-hierarchy`.

The interval theorem includes zero polynomials, constants, and odd degrees. The conversion of the odd-degree endpoint representation uses `1 +/- x = ((1 +/- x)^2 + 1-x^2)/2` and has the stated even degree bound. Multiplication across distinct coordinates gives preordering certificates; it is not asserted to stay in the ordinary module.

The gluing induction uses the running-intersection implication `B_child intersect U_previous = S_parent`, so it attaches only new coordinates and preserves previous marginals. Standard Borel disintegration applies. Arbitrary versions on null separator events do not change the resulting marginals. The finite union of zero-probability local infeasibility events proves the support claim. Empty separators give products.

The private hierarchy keeps shared degree `2r` and private degree two, with distinct private vectors per bag and scalar shared separator consistency. Its degree allowances are legal: a nonconstant affine shared row has allowance reduced by one, giving shared degree at most `2r-1`, and constant rows use at most `2r`. Private quadratic tests remain in the rectangular domain. This formulation is not silently compared by inclusion with a total-degree hierarchy. Boundary recourse dual attainment is not asserted by the box Slater lemma. The later quantitative recourse proofs remain outside my assigned proof verdict.

## Section 03: exactly consistent full-preordering rounding

### Kernel normalization and explicit constants

Locators: `03-kernels.tex:44`–`:115`, `lem:jackson` and `eq:ker-kernel`.

The triangular sequence autocorrelation is precisely the Fourier expansion of the fourth power of the Dirichlet sum. Its normalizing coefficient is

`a_0 = m^2 + 2 sum_{j=1}^{m-1} j^2 = (2m^3+m)/3`.

Its coefficients are nonnegative, at most `a_0`, and vanish beyond `2m-2`. The squared-difference identity has exactly `2m` nonzero unit differences, so `a_0-a_1=m`. Therefore `1-gamma_1=3/(2m^2+1)`. Positivity of the normalized circle kernel and `1-cos(kt) <= k^2(1-cos t)` give the displayed damping estimate for every frequency, including frequencies above support. The averaged circle expression is nonnegative on the square. Arcsine orthogonality gives exact mass and diagonal action, with the factor two in the kernel canceling the factor one half in nonconstant Chebyshev orthogonality. The constant case `m=1` works separately through the same formulas.

### Truncated positivity and exact separator laws

Locators: `03-kernels.tex:135`–`:194`, `lem:pre-density`; `:196`–`:222`, `rem:ker-degree`; `:231`–`:276`, `thm:pre`.

Pointwise box nonnegativity alone would not suffice for a truncated functional. For each fixed output, the interval certificate of a source factor has square degree at most `m-1`, or `m-2` if its generator is present. After multiplication over a bag, the square root in the term indexed by `I` has degree at most

`v_b(m-1)-|I| <= r-|I|`.

This is exactly the local preordering constraint available. Thus the polynomial density is positive despite the absence of a local representing measure. The order-one counterexample in `rem:ker-degree` is feasible and yields the stated negative value for `(1-x)(1-y)`; it explains why a degree count without the certificate is insufficient.

Integration removes each eliminated kernel factor by an identity in the source variable. The remaining separator polynomial has source degree at most `2|S|(m-1) <= 2r`, so edge moment consistency identifies the two separator densities as functions. The output laws have mass one and agree as actual measures on separators. Tree gluing is therefore applicable.

The objective proof uses only coefficients of total degree at most `d <= r`. This is the needed half-degree margin. Tensor damping is bounded by the sum of coordinate damping terms, producing exactly `3 A(f_b)/(2m^2+1)` for a bag and exactly `3 A/(2m^2+1)` after summation. No extra edge count appears. For `m=floor(r/w)+1`, every bag meets the positivity degree condition and `m>r/w` gives `3w^2 A/(2r^2)`. Constants and individual empty bags are preserved. The claim is about every feasible family; infimization and weak duality then give the hierarchy gap.

The explicit conditional gluing formula at `03-kernels.tex:287` is also valid at zero separator density: nonnegativity and a zero fiber integral make that fiber irrelevant to the bag law. It supplies a direct alternative to the standard disintegration result.

### Grid and certificate contracts

Locators: `03-kernels.tex:311`, `lem:ker-quadrature`; `:332`, `cor:pre-grid`; `:379`–`:392`, comparison prose; `:394`, `cor:pre-certificate`.

The midpoint cosine rule annihilates all nonconstant Chebyshev modes through degree `2N-1`. For odd frequency its complex geometric sum is purely imaginary, which is enough; the proof does not mistakenly require the complex sum to vanish.

With `N_g=m+floor(d_infty/2)`, both parities satisfy `2N_g-1 >= 2m-2+d_infty`. Tensor quadrature integrates the density, its objective product, and every removed-coordinate integral exactly. The finite bag masses are nonnegative, normalized, and have equal separator marginals. Hence the global grid law has the same expected objective as the continuous rounded law. Some grid point is no worse than its mean.

The precise contract is one-sided for an arbitrary feasible input: `G <= L(f)+E`. For an optimal input, weak duality also gives `rho <= f* <= G`, so `0 <= G-rho <= E`. The current prose makes this distinction. The tree program accounts for incoming messages: the sum of `1+#children(b)` is `2t-1`, so the stated `2t N_g^w` bound on additions and comparisons is conservative. This count starts after local tables are available and is in exact real arithmetic; no bit-cost conclusion follows.

The certificate is obtained from the attained finite box dual at `rho_pre`, then enlarged by a nonnegative constant. It has the specified degree `2r` and real coefficients. Neither rational coefficients nor an attained infinite-dimensional polynomial separator dual is assumed.

## Section 04: ordinary-module transfer

### Squared kernel and approximation interface

Locators: `04-ordinary.tex:18`–`:26`, cone obstruction; `:59`–`:121`, `lem:sos-kernel`; `:126`–`:175`, `lem:mod-defect`; `:177`–`:236`, kernel proof.

The displayed ordinary-module obstruction has PSD moment and single-generator localizing matrices, yet evaluates the two-generator product to `-1/8`. This is an explicit check that preordering positivity cannot be imported into this argument.

The Fejér mass polynomial obeys `C_s/2 <= M_s <= C_s`: composition of the nonnegative Fejér kernel gives `M_s=(C_s+R_s(T_2(x),1))/2`. Thus `0 <= z_s <= 1/2` on the interval. For even `N`, the geometric sum has the exact displayed SOS identity. Its square roots have degree at most `(s-1)N`; multiplication by `Phi_s`, of degree `s-1`, gives source degree

`D=2(s-1)(N+1)`.

The mass `omega=p M_s=1-z_s^(N+1)` is globally SOS. The residual `varrho=z_s^(N+1)` is interval-nonnegative, has degree at most `D`, and has interval supremum at most `delta=2^(-(N+1))`. No global SOS assertion about the residual is required. Adding the residual gives an exactly normalized source kernel, fixes constants, and leaves positive-degree images unchanged.

I reconstructed the defect identity by separating the last product sum into indices below, at, and above `k`. The paired terms at `l` and `l+k` produce a negative squared coefficient difference; the index `k` produces `-bar_chi_k^2 T_k`; and symmetrization below `k` gives the factor one half in the last sum. For `k <= s`, the respective norm contributions are at most `k^2/s^2`, `k^2/s`, and `k^2/(2s)`. These give the stated `k^2/s^2+3k^2/(2s)` bound.

The Chebyshev coefficient estimates are also justified independently: `||Phi_s||_ch <= s`, `||z_s||_ch=(C_s-1)/C_s <= 1`, and `||p||_ch <= (N+1)/C_s`. Thus `||Psi(.,u)||_ch <= Lambda=s^2(N+1)/C_s`. Orthogonality and weighted Cauchy–Schwarz give `||varrho||_ch <= sqrt(2(D+1)) delta`. Multiplication by a Chebyshev mode does not increase that norm.

The separate terms in the approximation identity can have degree above `D`. The manuscript evaluates only their combined difference, whose degree is at most `D` for the permitted modes `k <= s <= D`. Tensoring produces degree at most `vD <= r`. Both transformed and original local objectives therefore remain in the range where the Section 02 Chebyshev moment bound is proved. This is a material truncation safeguard and is present.

### Normalization obstruction

Locator: `04-ordinary.tex:238`–`:254`, `rem:normalization-obstruction`.

The statement has the correct hypotheses. For a polynomial kernel globally nonnegative in the source for every output, its highest nonzero source degree must be even and its leading coefficient must be nonnegative throughout the output interval. Exact normalization forces that coefficient's integral to vanish. Continuity and full arcsine support force it to vanish identically, a contradiction. Consequently a globally SOS exactly normalized polynomial kernel is source-independent. The constant kernel is an exception to usefulness, not a counterexample to this correctly stated conclusion. The argument does not exclude kernels positive only on the source interval or certified with interval generators.

### Residual products and degree ledger

Locators: `04-ordinary.tex:271`, `lem:mod-signed`; `:333`–`:386`, `lem:residual-products`; `:388`–`:407`, `tab:mod-ledger`.

For a residual subset of size `j` in a bag of size `v`, let `G` be the product of the `v-j` globally SOS factors and `H` the product of residuals. Write `G=sum_l q_l^2` with `deg q_l <= (v-j)D/2`.

The zero-residual term is SOS. A single residual has an interval certificate of degree at most `D`; multiplying it by `G` creates only one generator in each term and has degree at most `vD`. Hence these terms are nonnegative under ordinary positivity. General residual products are not declared positive.

For the crucial upper bound, the telescoping identity for `delta^(2j)-H^2` has one factor `delta^2-varrho_i^2` at a time, multiplied by preceding residual squares and a nonnegative scalar. That factor has an interval certificate of degree `2D`. After multiplication by `G` and the preceding squares, the complete certificate degree is at most

`(v-j+2l)D <= (v+j)D <= 2r`.

The corresponding generator multiplier has degree at most `2r-2`. There is never a product of two distinct generators. Also `GH^2=sum_l(q_l H)^2`, where `deg(q_l H) <= (v+j)D/2 <= r`. This proves

`0 <= L(GH^2) <= delta^(2j)L(G)`.

The same margin makes `G(a+cH)^2` an allowed SOS for every real `a,c`. Thus the weighted two-by-two moment matrix is PSD and

`|L(GH)|^2 <= L(G)L(GH^2) <= delta^(2j)L(G)^2`.

This includes `L(G)=0` with no division. Nonnegativity of `L(G)` comes from its SOS representation for every `j`, not from the single-residual claim. Its upper bound uses `deg G <= r` and its Chebyshev norm, giving `L(G) <= Lambda^(v-j)`. All four residual-product conclusions follow within the actually retained moment space.

### Common correction and normalized objective error

Locators: `04-ordinary.tex:411`–`:481`, `Delta_v`, `thm:mod`.

Expanding the exactly normalized tensor kernel gives signed densities of mass one and exactly equal separator densities. Terms with two or more residual factors give the common lower bound `bar_h_b >= -Delta_vb`. For `Lambda >= 1`, the displayed recurrence

`Delta_(v+1)=(Lambda+delta)Delta_v+v Lambda^(v-1)delta^2`

proves monotonicity for positive `v`, while `Delta_0=Delta_1=0` handles the initial cases. The same `Delta_w` is therefore valid for every bag.

The shift and rescaling `(bar_h_b+Delta_w)/(1+Delta_w)` give true probability densities. Marginalization adds exactly the same scalar on every separator, including empty separators, so consistency survives differing bag sizes. For an empty bag both densities remain one and its constant objective is exact. Independent bag-dependent corrections would not have this property.

The objective correction uses the exact rearrangement `I_plus-I_bar = Delta_w(I_reference-I_plus)`. The right-hand side compares two true expectations and is bounded by `Delta_w osc(f_b)`. No range bound is improperly applied to the signed expectation `I_bar`. The tensor coefficient comparison gives `C_b Gamma_vb`, because its source degree is at most `v_bD <= r`. Summing proves the stated absolute error and the gap, without an extra bag or edge count. Additive constants cancel exactly. The explicit `C_f=sum_b C_b` still scales with the decomposition; the theorem does not normalize by the coefficient norm of the combined global polynomial after cancellations.

### Explicit rate for every sufficiently large order

Locators: `04-ordinary.tex:498`–`:562`, `cor:mod-rate`; `:564`–`:570`, uniformity prose; `:600`–`:617`, certificate corollary.

The proof chooses parameters at the actual order `r`, not just on a subsequence:

`c_w=max(3,(w+1)/2)`, `ell_r=log_2(r+2)`,

`s=floor(r/(2w(c_w+3)ell_r))`, `N=2 ceil((c_w/2)log_2 s)`.

The first threshold gives `s >= max(2,d_infty)`, and `N` is an even integer at least two. Since `N+1 <= (c_w+3)ell_r`, the actual degree satisfies `wD <= r`. The floor bound gives `s >= r/(4w(c_w+3)ell_r)`.

The residual satisfies `delta <= s^(-c_w)/2 <= s^(-3)/2`. Together with `C_s >= 2s/3` and `D+1 <= 2s(N+1)`, this gives

`eta <= (3d_infty^2+1)(N+1)/s^2`.

Substitution of the floor bound yields `w eta <= 16w^3(3d_infty^2+1)(c_w+3)^3 ell_r^3/r^2`. The second threshold makes this at most one, so `Gamma_w <= e w eta`. This produces the first displayed constant, including its factor `16e`.

For `w >= 2`, Taylor's formula yields `Delta_w <= binom(w,2) delta^2(Lambda+delta)^(w-2)`. The inequalities `Lambda+delta <= 2s(N+1)` and `2c_w >= max(6,w+1)` give

`Delta_w <= binom(w,2) 2^(w-4) (N+1)^(w-2)/s^3`.

Multiplying by two and substituting `s^(-3) <= 64w^3(c_w+3)^3 ell_r^3/r^3` gives exactly the second coefficient `binom(w,2)2^(w+3)w^3(c_w+3)^(w+1)` and power `ell_r^(w+1)/r^3`. For `w=1`, the correction is zero. For each fixed width, the second term is lower order than `ell_r^3/r^2`. Both thresholds eventually hold for every integer order, with no dependence on bag count or coefficients. The `C_f=0` case is exact independently of these parameters.

The certificate corollary again uses finite box dual attainment plus a nonnegative constant. Enlarging the finite-order error to the rate bound is legitimate because it only adds another nonnegative constant. The table's first three rows and alternate final row are correctly distinguished; the decimal evaluations themselves were not recomputed in this review.

## Section 05: lower bounds and exact finite orders

### Local-measure identity and explicit annihilating witness

Locators: `05-sharpness.tex:32`–`:59`, `lem:moment-matching-general`; `:87`–`:122`, `prop:moment-matching`; `:126`–`:192`, `lem:fejer-lower`.

Hahn–Banach separates a function at positive distance from the finite-dimensional polynomial subspace by a norm-one annihilating functional. Riesz representation then gives a signed measure of total variation one. Since constants are annihilated, its Jordan masses are each one half. Doubling the Jordan parts proves the attained moment-matching value `2E_n`. The zero-error case is explicitly harmless.

For this instance the local minima are exactly `-varphi` and `+varphi`, and their minimizing selectors lie inside their respective rectangles. Consequently `v_n=-2E_n(varphi)`. These integration functionals are feasible for both cones, giving `rho_mod <= rho_pre <= v_(2r)`. The reverse inclusion, and hence general equality of the SDP and local-measure values, is not asserted.

The explicit Fejér witness is independently sufficient for the lower bound. The smallest even `N >= n+1` has `2 <= N <= n+2`, and every frequency in the witness exceeds `n`. Orthogonality therefore annihilates all shared moments through degree `n`. The circle construction, its even part, and nonnegative Fejér envelope give total variation at most one.

Direct integration gives, for odd `k`,

`int varphi T_k dmu = sin(k pi/2)/(2pi) * (1/k-k/(k^2-4)) = -2 sin(k pi/2)/(pi k(k^2-4))`.

The intermediate factor one half is present and correct. Supported odd frequencies have `3 <= k < 3N`, so their denominators are positive and below `27N^3`. The odd triangular weights sum to `N/2`. Hence the signed pairing is at least `1/(27pi N^2)`. The equal nonzero Jordan masses are at most one half; normalizing them therefore gives at least twice that pairing. This proves the stated probability-measure lower bound for every `n >= 0`, including `n=0`.

### Fixed quadratic sharpness and scope

Locators: `05-sharpness.tex:196`–`:283`, `thm:quad-sharp` and its interpretation.

Putting `n=2r` gives the exact lower coefficient `1/(54pi(r+1)^2)`. The transformed local Chebyshev expansions have budgets `A(f_1)=4`, `A(f_2)=6`, and `C_f=21/8+25/8=23/4`. The full-preordering theorem applies with `w=d=2`, giving the upper bound `30/(2(floor(r/2)+1)^2+1)` and its coarser `60/r^2` bound. The ordinary theorem gives only the displayed logarithmic upper bound. Thus exact inverse-square order is proved for the preordering and for the local-measure value, not for the ordinary module.

The dense degree-four certificate is correct: the bracket `(xz)^2+z^2 g_x+x^2 g_z+g_xg_z` equals `xz`. All generator products and square degrees are permitted in the dense order-two preordering. The statement about linear endpoint generators is a separate dense preordering claim, with the same actual-measure lower witnesses.

For a putative sparse nonnegative decomposition of `f`, the polynomial-ring intersection forces `q_1=f_1+p(y)` and `q_2=f_2-p(y)`. Their fiber minima force `p=varphi`, which cannot be a polynomial. With slack `epsilon`, the same argument gives the necessary width condition `varphi <= p <= varphi+epsilon`, hence `epsilon >= 2E_(2r)(varphi)`. It does not infer that every such nonnegative local term has a certificate at the same order. The example is a limitation of the specified bags and separator information, not a hardness claim about optimizing this small instance.

### Order one: certificate, truncated witness, and local-measure value

Locators: `05-sharpness.tex:313`–`:352`, part (a) of `prop:exact-orders`.

The two reflected degree-two certificates add to `f+1/4`, and the two cones coincide at order one. The positive atomic law in the first bag has an outside atom, but its truncated matrix is PSD and its only generator tests have values zero and one quarter. Its separator mean is zero, its second moment is three quarters, and its first cost is minus one half. Reflection preserves these shared moments and gives second cost one quarter. Thus the total is exactly minus one quarter. The current text also proves that there is no alternate measure supported on the rectangle representing these moments: `xy <= x` there, but `L_1(xy)=3/8 > L_1(x)=1/4`. This is stronger than merely displaying an outside atom and correctly separates truncated feasibility from supported representation.

For `c=sqrt(2)-1`, the error of `S_1=y^2/2+cy` is odd and has alternating extremes at `-1,-c,c,1`, all of magnitude `c^2/2`. A strictly better degree-two polynomial would yield three sign changes in a degree-two difference, which is impossible. This proves `E_2=c^2/2` and the distinct local-measure value `v_2=-(3-2sqrt(2))` without identifying it with the SDP value.

### Order two: approximation and hand expansion of the Gram identity

Locators: `05-sharpness.tex:354`–`:404`, part (b), approximation and certificate.

Writing `t=sqrt(3)`, direct reduction using `t^2=3` gives

`p_star(y)=c_star y^3+y^2/2+(2t/3-1)y+E_star`.

This verifies the reflection identity. The factorization of `p_star-y^2`, together with `7-4t>0`, proves the lower majorant bound. Reflection then proves the upper width `2E_star`. The six distinct contact points `-1,-b,-a,a,b,1` give alternating errors for the cubic `p_star-E_star`. Any degree-four improvement would have a difference with five sign changes. Thus `E_3=E_4=E_star`; no numerical approximation input is needed.

I expanded the entire Gram right-hand side by powers of `x`. Let `h=(y+1)(y+a)`, `A=2-t`, `B=(3t-7)/4`, and `H=(3+2t)/36`, the indicated matrix entries. Useful exact reductions are

`b^2=2A`, `b^3=2a`, `k_star b^2=H`,

`k_star(b+a)^2=t/6`, `k_star b(b+a)=(1+t)/12`,

`(b+1)(b+a)=3b^2`.

The contributions from the first two entries of `V` and the `g_x` multiplier combine to

`x[A(x-b)^2+2B(x-b)(y-b)+(y-b)^2]+x^2(y-b)^2/6`.

Adding the remaining cross terms, `H(h-3bx)^2`, and the `g_y` term gives coefficient zero for `x^3`, coefficient one for `x^2`, coefficient `-2y` for `x`, and constant `p_star(y)`. This proves the displayed polynomial identity exactly. The separate GPT algebra audit obtained the same reduction.

The leading two-by-two minor of `G_0` is `(35t-58)/24`; the determinant is `(38-15t)/864`. The determinant of `G_1` is `(13t-22)/8`. These match the manuscript, and all are positive by the stated elementary comparisons. Thus the quadratic forms are SOS over the real field. The roots in `V` have degree two, while those in `U` and `Z` have degree one. Each generator term consequently has total degree four and uses one generator. This is a legal ordinary-module order-two certificate, not merely a pointwise nonnegative polynomial.

### Order-two actual-measure witness and majorant nonmembership

Locators: `05-sharpness.tex:406`–`:428`, explicit witness; `:438`–`:456`, `rem:shp-majorant`; `:458`–`:460`, higher-order frontier.

The three weights are positive and sum to one. Their first and third moments vanish. Useful hand reductions are

`a w_(-a)=1/9`, `b w_b=(9-4t)/9`,

`a^3 w_(-a)=(52-30t)/9`, `b^3 w_b=(60-34t)/9`.

Together with `w_(-1)=(8-4t)/9`, these verify the two zero odd moments. Reflection preserves every even moment, so the two separator laws match all moments through degree four. Lifting uses selectors inside the rectangles. Their cost reduces to

`w_(-1)+w_(-a)a^2-w_b b^2=(24-14t)/9=-2E_star`.

Combining this actual-measure witness with the explicit ordinary-module certificate proves equality of both SDP values and `v_4`. It uses weak duality only and does not depend on numerical SDP solutions or attained dual optima.

The optimal degree-two majorant is not certifiable at order one. Evaluating a purported representation at `(0,-c)` forces the `g_y` coefficient to vanish and each affine SOS factor to vanish. The resulting coefficient equalities require `1 <= (1+2c)/2 = sqrt(2)-1/2 < 1`. This confirms why best separator approximation alone does not prove degree-specific local SOS membership. Equality at all higher orders remains openly conjectural; retained floating-point agreement is not used as a theorem premise.

## Front matter, discussion, and reader-facing contracts

Relevant locators: `00-abstract.tex:4`–`:14`; `01-introduction.tex:75`–`:107`, `:139`–`:200`, `:273`–`:294`; `10-discussion.tex:5`–`:27`, `:49`–`:71`, `:84`–`:126`.

The abstract and introduction correctly reserve an exact inverse-square gap for the quadratic preordering example and describe the ordinary bound with its coefficient normalization and logarithms. The introduction and discussion identify `2E_(2r)` as an exact identity for the paired local-measure models and as a lower bound for the finite SDPs. Their order-one and order-two comparison agrees with the explicit proofs.

The ordinary normalization obstruction is summarized with global source nonnegativity and source dependence, so it is not overstated. The ordinary transfer is attributed separately from the dense kernel and rate. The preordering inverse-square rate is expressly attributed as previously stated in lecture slides. The unresolved difference from the inspected published exponent is preserved. These are appropriate boundaries under the supplied literature evidence; fresh primary-source verification remains with the designated literature reviewer.

The grid discussion correctly states `G_r-epsilon_r <= f* <= G_r`, acknowledges that this gives a lower bound as well as a feasible solution, and makes no generic runtime or practical-speedup claim. Matrix sizes are distinguished from accuracy constants and total bag count. The discussion separately describes finite box certificate attainment, strict-level recourse certificates, and the lack of a general constrained dual-attainment conclusion. It leaves logarithm necessity, higher-order exact identities, growing-width behavior, and private-recourse ordinary-module transfer open.

The scoped theorem statements are usable: their degree conditions, parameters, coefficient budgets, domains, output laws, and finite-order errors are explicit. The problem-specific algebra and approximation proofs are supplied. Standard external facts are named and have the contracts needed here: interval positivity, Hahn–Banach/Riesz, regular conditionals, and finite conic Slater duality. The exposition repeatedly explains why the finite functional-to-measure step requires work, and does not obscure that step behind a qualitative convergence citation.

## Targeted verification record

This review used manual mathematical reconstruction. Read-only inspection used `rg --files`, `cat`, `nl -ba`, `sed -n`, and `wc -l` on the files listed above. The targeted snapshot command actually run was:

```text
sha256sum paper-sparse-sos/main.tex paper-sparse-sos/macros.tex paper-sparse-sos/sections/00-abstract.tex paper-sparse-sos/sections/01-introduction.tex paper-sparse-sos/sections/02-setting.tex paper-sparse-sos/sections/03-kernels.tex paper-sparse-sos/sections/04-ordinary.tex paper-sparse-sos/sections/05-sharpness.tex paper-sparse-sos/sections/10-discussion.tex paper-sparse-sos/evidence/BRIEF.md paper-sparse-sos/evidence/LITERATURE-PRELIMINARY.md research-20260928/solver/sparse-kernel-rounding.md research-20260928/solver/sparse-putinar-kernel.md research-20260928/solver/sparse-putinar-exact-consistency.md research-20260928/solver/quadratic-sharpness.md research-20260928/solver/quadratic-exact-gap-frontier.md
```

It completed successfully. A later targeted `sha256sum` over Sections 00–05, Section 10, and this review detected the concurrent changes described above and returned the final manuscript hashes after rereading. An `LC_ALL=C rg -n '[[:cntrl:]]'` check of this review found two stray control characters introduced while writing it; both were removed, and the repeated check found none. No test, experiment, historical checker, build, project-wide verification, or CI command was run. Only this review file was authored.
