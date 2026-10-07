# Independent audit of sparse kernel mathematics

Date: 2026-10-05. Scope: the full-preordering rounding theorem, the ordinary-module kernel interface and exact-consistency transfer, finite SDP duality, and the fixed quadratic lower example and its first two orders. This audit rederived the mathematical steps rather than treating historical review verdicts as premises. It used the source notes and their proof reviews. It performed no literature research, experiment reruns, project-wide verification, CI inspection, commits, or changes to the original notes.

## Assessment and required presentation repairs

No substantive error was found in the core finite-order theorems under their stated box, total-degree, running-intersection, and moment-consistency assumptions. The following are repairs or clarifications needed for a standalone paper, rather than counterexamples to the notes.

| Finding | Severity | Source locator | Required treatment |
| --- | --- | --- | --- |
| The ordinary-module objective degree check is implicit in the author notes. | Expository gap | `sparse-putinar-kernel.md:267–274, 377–394`; `sparse-putinar-exact-consistency.md:214–230` | State explicitly that `deg f_b <= v_b d_infty <= v_b s <= v_b D <= R`; the transformed objective also has degree at most `v_bD`. |
| Intermediate polynomials in the univariate coefficient estimate can have degree greater than `D`. | Important truncation clarification | `sparse-putinar-kernel.md:218–265`; fresh review, lines 86–97 | Apply coefficient-norm inequalities to the intermediate polynomials, but evaluate the truncated functional only on the combined polynomial `A_b g_b-g_b`, whose degree is at most `v_bD <= R`. |
| Primal attainment is available, although the rounding argument does not need it. | Useful missing lemma | SDP consequences in `sparse-kernel-rounding.md:338–359`, `sparse-putinar-kernel.md`, Section 6 | Include the monomial moment compactness proof below if attainment of a finite SDP is stated. Do not infer primal attainment merely from primal Slater. |
| Finite SDP dual attainment differs from exact polynomial separator attainment in the infinite marginal problem. | Material distinction | Same SDP passages; `quadratic-sharpness.md:207–219` | Prove finite SDP duality through Slater; separately retain the quadratic example's nonpolynomial separator obstruction. These statements are consistent. |
| The inverse-square lower example gives a matching upper rate for the full preordering, but the proved ordinary-module upper bound has logarithms. | Claim boundary | `quadratic-sharpness.md:168–190`; ordinary-module rate theorem | State `Theta(r^-2)` for the preordering example. The same witnesses give an ordinary-module `Omega(r^-2)` lower bound, with the proved upper bound `O(log^3(r)/r^2)`. No logarithmic sharpness result follows. |
| Equality with the measure optimum at all higher orders is unproved. | Unproved extension, already correctly marked | `quadratic-exact-gap-frontier.md:257–275` | Use only the exact order-one and order-two conclusions. Numerical agreement does not justify `rho_r=-2E_{2r}(h)` for `r>=3`. |
| The box support conclusion cannot be changed to preservation of arbitrary additional constraints. | Material scope boundary | Limit sections of all three kernel notes | The kernel laws are box supported. Extra input localizers do not imply that smoothed/corrected laws satisfy their constraints. |
| Uniformity in bag count requires retaining the coefficient budget. | Material normalization boundary | `sparse-putinar-exact-consistency.md:48–64, 273–295` | Write `gap/C_f <= O_{w,d_infty}(log^3 R/R^2)`, with zero-budget objectives handled as exact. Absolute error and SDP size can grow with the number of bags. |

The preordering coefficient normalization `A`, the ordinary-module coefficient normalization `C_f`, the common shift `Delta_w`, all displayed kernel mass constants, and the lower-bound constants were checked independently as described below.

## Standalone assumptions and theorem statements

Let a finite tree have bags `B_b` covering the variables. Assume running intersection: the bags containing any variable form a connected subtree. Put `v_b=|B_b|` and `w=max_b v_b >= 1`. Work on the product box `[-1,1]^n`; any different rectangular box used in the quadratic example is transported by a specified invertible affine coordinate change. Let

`f=sum_b f_b(x_{B_b})`, with real polynomial `f_b`, and let `f*` be its box minimum.

An order-`R` ordinary-module feasible family consists of real linear functionals on the local polynomial spaces of total degree at most `2R`, satisfying

1. `L_b(1)=1`;
2. adjacent bags agree on all separator polynomials of total degree at most `2R`;
3. `L_b(q^2)>=0` for `deg q<=R`;
4. `L_b((1-x_i^2)q^2)>=0` for `deg q<=R-1` and `i in B_b`.

For the full preordering at order `r`, replace item 4 by positivity of every `q^2 prod_{i in I}(1-x_i^2)` whose total degree is at most `2r`, including the empty product. No representing-measure assumption is imposed on either family.

Let `rho` denote the infimum of the objective over that specified feasible family. An arbitrary feasible moment objective is not by itself a lower bound on `f*`. The optimum `rho` and any feasible dual SOS certificate are lower bounds.

### Full-preordering theorem

Expand `f_b=sum_alpha c_{b,alpha} T_alpha`, where `T_alpha` is the tensor Chebyshev basis. Put

`d=max_b deg f_b`, `A=sum_b sum_alpha |c_{b,alpha}| sum_i alpha_i^2`.

For integer `r>=max(w,d)` set `m=floor(r/w)+1`. Every feasible family admits a global probability law with exactly its constructed bag marginals and

`|E_nu f-sum_b L_b(f_b)| <= 3A/(2m^2+1)`.

Thus `0<=f*-rho_r<=3A/(2m^2+1)<=3w^2 A/(2r^2)`. Finite SDP duality also gives `f-rho_r` in the sum of the specified local truncated preorderings, with real SOS coefficients. This theorem requires the products of box generators.

### Exactly consistent ordinary-module theorem

Write `f_b=c_{b,0}+g_b`, `g_b=sum_{alpha!=0}c_{b,alpha}T_alpha`, `C_b=sum_{alpha!=0}|c_{b,alpha}|`, and `C_f=sum_b C_b`. Let `d_infty` be the largest coordinate Chebyshev degree of the nonzero objective coefficients; take zero if there are none. Put `W=sum_b osc(f_b)<=2C_f`.

Choose integers `s>=max(2,d_infty)` and even `N>=2`. Define

`C_s=(2s^2+1)/(3s)`, `D=2(s-1)(N+1)`, `delta=2^{-(N+1)}`,

`eta=((N+1)/C_s)(d_infty^2/s^2+3d_infty^2/(2s)) + sqrt(2(D+1))*delta`,

`Gamma_v=(1+eta)^v-1`, `B=s^2(N+1)/C_s`,

`Delta_w=sum_{j=2}^w binom(w,j) delta^j B^{w-j}`.

Assume `R>=wD`. Every feasible ordinary-module family has an exactly consistent corrected family of genuine bag probability laws, and a global law with those marginals, satisfying

`|E_nu f-sum_b L_b(f_b)| <= sum_b C_b Gamma_{v_b}+Delta_w W <= C_f(Gamma_w+2Delta_w)`.

The same expression bounds `f*-rho_R`. Finite SDP duality gives a sparse ordinary-module certificate for `f-f*` plus that error, at total degree at most `2R`.

For fixed `w,d_infty`, the parameter prescription in the source gives

`f*-rho_R <= C_f O_{w,d_infty}(log^3(R)/R^2)`

for all sufficiently large orders, with the threshold and implicit constant independent of bag count and tree topology. If `C_f=0`, all local objectives are constant and the gap is zero. The threshold and constant are not uniform for growing width.

These theorem statements depend on the exact interval positivity and finite SDP duality statements listed at the end of this report. All other kernel algebra is developed below.

## Moment positivity and finite SDP attainment

For any tensor Chebyshev polynomial with `|alpha|<=R`,

`1-T_alpha^2 = sum_i (1-x_i^2) U_{alpha_i-1}^2 prod_{j<i} T_{alpha_j}^2`.

Indices with `alpha_i=0` contribute zero. Each multiplier is a square, and its degree is at most `|alpha|-1`. Therefore this is an ordinary-module certificate of total degree at most `2|alpha|`; no products of different box generators occur. It implies `0<=L(T_alpha^2)<=1`. Positivity of `L((a+bT_alpha)^2)` for all real `a,b` gives `|L(T_alpha)|<=1`.

This proof applies to both hierarchies. The use needed in the kernel objective estimate is only the range `|alpha|<=R`. The notes do not need to assume coefficient bounds on arbitrary degree-`2R` Chebyshev polynomials.

A separate elementary argument gives compactness of the entire finite feasible moment set. For a monomial `x^alpha` with `|alpha|<=R`, square positivity gives `L(x^{2alpha})>=0`. If `alpha_i>0`, the single-generator test with `q=x^{alpha-e_i}` gives

`L(x^{2alpha}) <= L(x^{2(alpha-e_i)})`.

Iteration gives `0<=L(x^{2alpha})<=1`. For any multi-index `beta` with `|beta|<=2R`, split `beta=alpha+gamma` with `|alpha|,|gamma|<=R`. Moment Cauchy–Schwarz yields

`|L(x^beta)|^2 <= L(x^{2alpha})L(x^{2gamma}) <= 1`.

All coordinates of every local moment vector are bounded. PSD constraints and moment consistency are closed. Since the number of bags and moments is finite, the feasible set is compact and nonempty. Any objective defined through degree `2R` attains its finite minimum. This argument uses only single-generator constraints and therefore also applies to the stronger preordering.

For Slater, use the product normalized arcsine measure in every bag. Every nonzero polynomial square of an allowed degree has strictly positive integral. Multiplying by any permitted product of box generators retains strict positivity: that weight is positive on the open box, and a nonzero polynomial cannot vanish on its open interior. Every moment and localizing matrix is consequently positive definite. The bag measures satisfy all consistency equalities. Redundant equality constraints do not destroy strict feasibility on the equality affine space.

Finite SDP Slater duality now gives no primal-dual gap and an attained finite SOS dual. The separator equality multipliers are polynomials in their edge separators; they have opposite signs in the two endpoint identities. Summing the identities cancels them and leaves

`f-rho_R=sum_b q_b`,

where `q_b` belongs to the specified local cone at total degree at most `2R`. The normalizing scalar multipliers sum to `rho_R`. Adding the nonnegative constant `rho_R-f*+E` gives `f-f*+E` in the same cone.

This argument supplies real SOS coefficients. It establishes neither rational certificate output nor its bit complexity. It does not imply attainment of an infinite marginal separator problem.

## Full-preordering kernel reconstruction

Source: `sparse-kernel-rounding.md`, Sections 3–6, particularly lines 118–177, 192–241, 245–285, and 289–359.

Let `b_j=(m-|j|)_+`, `a_k=sum_j b_j b_{j-k}`, and `g_k=a_k/a_0`. The coefficients of `|sum_{j=0}^{m-1}e^{ijt}|^2` are `b_j`; squaring this Fourier polynomial therefore gives

`J_m(t)=|sum_{j=0}^{m-1}e^{ijt}|^4/a_0 = 1+2 sum_{k=1}^{2m-2}g_k cos(kt)`.

Direct summation gives `a_0=m^2+2sum_{j=1}^{m-1}j^2=(2m^3+m)/3`. Autocorrelation gives `g_k>=0`; Cauchy–Schwarz gives `g_k<=1`. The zero tail beyond `2m-2` agrees with the Fourier degree.

The identity

`a_0-a_1=(1/2)sum_j(b_j-b_{j-1})^2=m`

follows because there are `2m` nonzero unit differences. As `J_m` is a probability density on the circle,

`1-g_k=E[1-cos(kt)] <= k^2 E[1-cos(t)] = 3k^2/(2m^2+1)`.

For completeness, the pointwise trigonometric inequality follows from `|sin(ku)|<=k|sin(u)|`, obtained by expanding the geometric sum or induction. It remains valid for the zero Fourier tail; no small-frequency restriction is needed.

Let `mu` be normalized arcsine measure. The polynomial

`K_m(x,y)=1+2sum_{k=1}^{2m-2}g_k T_k(x)T_k(y)`

is half the sum of `J_m(theta-phi)` and `J_m(theta+phi)` for `x=cos(theta)`, `y=cos(phi)`. It is nonnegative on the square, integrates to one in either coordinate, and satisfies

`int T_k(y)K_m(x,y)dmu(y)=g_k T_k(x)`.

For fixed output `y_i`, interval positivity gives `K_m(x_i,y_i)=sigma_{0,i}+(1-x_i^2)sigma_{1,i}`, with square degrees at most `m-1` and `m-2`, respectively. Multiplying these certificates across a bag introduces exactly the products allowed by the full preordering. Every certificate term has total degree at most `2v_b(m-1)<=2r`. Thus `h_b(y)=L_b(prod_i K_m(x_i,y_i))` is nonnegative without a representing measure for `L_b`.

Integrating any removed coordinate replaces its kernel by the polynomial identity one. A separator marginal is exactly `L_b(prod_{i in S}K_m(x_i,y_i))`, which has source degree at most `2|S|(m-1)<=2r`. Shared moment agreement gives exact shared densities. The resulting bag laws have mass one.

The objective calculation is diagonal in the tensor Chebyshev basis. Its mode multiplier is `prod_i g_{alpha_i}`; its deviation from one is at most `sum_i(1-g_{alpha_i})`. Since the objective modes have `|alpha|<=d<=r`, the preceding moment bound applies. Summing gives precisely `3A/(2m^2+1)`. Local additive constants contribute zero to `A` and zero error.

For the finite grid, `N_grid=m+floor(d_infty/2)` gives `2N_grid-1>=2(m-1)+d_infty`. Equal-weight Gauss–Chebyshev quadrature integrates bag densities, density times objective, and every marginalized kernel exactly. Thus discrete bag laws have matching separator marginals and retain the objective expectation. This validates the fixed-grid comparison in the source. Dynamic programming uses at most `O(sum_b N_grid^{v_b})` table entries and `O(tN_grid^w)` operations after evaluating objective tables; the latter accounts for all child-message additions. The quadrature nodes are algebraic, but an arithmetic count is not a bit-complexity claim.

## Ordinary-module kernel reconstruction

Source: `sparse-putinar-kernel.md:143–275`. The proof below reconstructs the source difference identity rather than accepting it as an external kernel lemma.

Put `b_j=(1-j/s)_+` for `j>=1`, and `b_0=1`. Define

`S_s(x,y)=1+2sum_{j=1}^{s-1}b_j T_j(x)T_j(y)`.

Its trigonometric form is half the sum of two Fejer probability densities, so it is nonnegative on the square. Orthogonality gives

`M_s(x)=int S_s(x,y)^2 dmu(y)=1+2sum_{j=1}^{s-1}b_j^2 T_j(x)^2`.

The maximum bound is `C_s=1+2sum b_j^2=(2s^2+1)/(3s)`. Compose the nonnegative kernel with itself:

`R_s(u,v)=int S_s(u,z)S_s(z,v)dmu(z)=1+2sum b_j^2 T_j(u)T_j(v)>=0`.

Using `2T_j(x)^2=1+T_j(T_2(x))` yields `M_s(x)=(C_s+R_s(T_2(x),1))/2`. Since `T_2(x)` is again in the interval, `C_s/2<=M_s<=C_s`. Hence `z=1-M_s/C_s` lies in `[0,1/2]` on the interval.

For even `N`,

`sum_{j=0}^N z^j=(1/2)[1+sum_{j=0}^{N/2-1}(z^j(1+z))^2+(z^{N/2})^2]`.

Thus `p=C_s^{-1}sum z^j` is globally SOS after substitution, and `Q(x,y)=p(x)S_s(x,y)^2` is globally SOS in the source for each fixed output. The source degree is at most `D=2(s-1)(N+1)` and the output degree is at most `2(s-1)`. Each square in the fixed-output representation has degree at most `D/2`.

Its mass polynomial is exactly `n=pM_s=1-z^{N+1}`. It is globally SOS because `p` and `M_s` are globally SOS. On the interval `1-delta<=n<=1`, with residual `r=1-n=z^{N+1}` satisfying `0<=r<=delta`. These are interval bounds; `r` is not generally a globally nonnegative polynomial.

### Direct derivation of the coefficient difference identity

Let `Kq=int q(y)S_s(x,y)^2 dmu(y)` and `a_j=1-b_j=min(j/s,1)`. Integrate `(T_k(y)-T_k(x))S_s(x,y)` against the second factor of `S_s`, using `2T_jT_k=T_{j+k}+T_|j-k|`. This first gives

`KT_k-M_sT_k = -a_k T_k + sum_{j>=1} b_j(b_{j+k}-b_j)T_jT_{j+k} + sum_{j>=1}b_j(b_|j-k|-b_j)T_jT_|j-k|`.

All sums are finite. In the second sum, pair its term `j=l+k` with the first sum's term `j=l`: their combined coefficient is `-(b_l-b_{l+k})^2`. The term `j=k` combines with `-a_k T_k` to give `-a_k^2T_k`. The terms `1<=j<k` pair with `k-j` and give half the sum of their squared differences. Therefore

`KT_k-M_sT_k = -a_k^2T_k - sum_{j=1}^s(a_{j+k}-a_j)^2 T_jT_{j+k} -(1/2)sum_{j=1}^{k-1}(a_{k-j}-a_j)^2 T_jT_{k-j}`.

The term at `j=s` is zero. The formula is valid at `k=0` with empty sums, and at `k=s`. It gives the source equation (16), including all endpoint indices and signs.

For `0<=k<=s`, the coefficient norm of every product `T_iT_j` is one, and `a_j` is `1/s`-Lipschitz on the index set. The three groups are bounded by

`k^2/s^2`, `k^2/s`, and `(k-1)k^2/(2s^2)`.

Their sum is at most `k^2/s^2+3k^2/(2s)`. Chebyshev multiplication is coefficient-norm submultiplicative. Expansion of `M_s` gives `||z||_1=(C_s-1)/C_s`, hence `||p||_1<=(N+1)/C_s`.

For a degree-at-most-`D` polynomial `q`, Chebyshev orthogonality and weighted Cauchy–Schwarz give `||q||_1<=sqrt(2D+1)||q||_infty<=sqrt(2(D+1))||q||_infty`. Apply this to `n-1`, with sup norm at most `delta`. The identity

`AT_k-T_k=p(KT_k-M_sT_k)+(n-1)T_k`

then gives exactly the stated univariate error bound. The two terms on the right can have degree greater than `D`; their sum has degree at most `D`, because `AT_k` comes from a kernel of source degree at most `D` and `k<=s<=D`. This distinction must be explicit before any truncated functional evaluation.

Tensor expansion gives `||A_bT_alpha-T_alpha||_1<=Gamma_{v_b}` for `alpha_i<=d_infty`. Each transformed mode has source degree at most `v_bD`. The original objective has degree at most `v_b d_infty<=v_bD`. Thus the complete error polynomial has degree at most `v_bD<=R`, and applying the moment coefficient bound is legitimate.

## Exact normalization, residual positivity, and common correction

Source: `sparse-putinar-exact-consistency.md:66–243`. This is the central ordinary-module transfer. The following audit does not assume that products of interval-nonnegative polynomials remain positive under a truncated ordinary-module functional.

Define `Qbar(x,y)=Q(x,y)+r(x)`. Its output integral is identically one as a source polynomial, and it is box nonnegative. For a bag,

`hbar_b(y)=L_b(prod_{i in B_b}Qbar(x_i,y_i))`

has mass exactly one. Its marginal on a separator `S` is exactly `L_b(prod_{i in S}Qbar(x_i,y_i))`, since every removed factor integrates to one. This source polynomial has degree at most `|S|D<=R`, so moment consistency gives equal separator densities. At this stage the densities can be signed.

For a fixed output and a residual subset `J` of size `j`, put `G=prod_{i notin J}Q_i`, `H=prod_{i in J}r_i`. The globally SOS polynomial `G` has degree at most `(v-j)D`. The interval polynomial `delta^2-r_i^2` has a single-generator interval certificate of degree at most `2D`. In the telescoping identity

`delta^{2j}-prod_{i=1}^j r_i^2 = sum_{i=1}^j delta^{2(j-i)}(delta^2-r_i^2)prod_{l<i}r_l^2`,

multiply each term by `G`. Every other multiplier is SOS, so each term remains in the ordinary module. Its degree is at most `(v-j+2i)D<= (v+j)D<=2R`. Consequently

`0<=L(GH^2)<=delta^{2j}L(G)`.

Write `G=sum_l q_l^2`, with `deg q_l<=(v-j)D/2`. For every real `a,b`, all squares in `G(a+bH)^2` have degree at most `(v+j)D<=2R`. Its weighted two-by-two moment matrix is PSD, giving

`|L(GH)|^2<=L(G)L(GH^2)<=delta^{2j}L(G)^2`.

Thus `|L(GH)|<=delta^j L(G)`, including `L(G)=0` without division. This uses the full available moment degree `2R`.

For each fixed output, `||S_s(.,y)||_1<=s`, so `||Q(.,y)||_1<=s^2(N+1)/C_s=B`. Since `deg G<=(v-j)D<=R`, coefficient evaluation gives `0<=L(G)<=B^{v-j}`.

Expansion of the tensor `Qbar` has a nonnegative term with no residuals. Terms with one residual are also nonnegative, since the residual has a single-generator interval certificate, multiplied by globally SOS factors; their degree is at most `vD`. Only terms with two or more residuals need a lower bound. They give

`hbar_b(y)>=-Delta_v>=-Delta_w`.

The monotonicity follows from `B>=1` and, more explicitly,

`Delta_{v+1}=(B+delta)Delta_v+v B^{v-1}delta^2`.

Define the common correction `h_b^+=(hbar_b+Delta_w)/(1+Delta_w)`. Each corrected density is nonnegative and has mass one. The product-arcsine reference density is one in each bag and has reference separator density one after marginalization. Since every bag uses the same scalar, all corrected separator densities still agree exactly, even for unequal bag sizes. Different bagwise scalars would not give this conclusion.

The signed objective calculation is valid because `Abar 1=1` and `Abar T_k=AT_k` for every positive mode `k`. Tensor expansion and the valid degree range therefore give

`|int f_b hbar_b dmu^{B_b}-L_b(f_b)|<=C_b Gamma_{v_b}`.

The correction identity is

`int f_b h_b^+ dmu-int f_b hbar_b dmu = Delta_w(int f_b dmu-int f_b h_b^+ dmu)`.

Both integrals on the right are expectations under genuine probability measures. Their difference is at most `osc(f_b)`. No probability bound is applied to the signed density. Summing gives `sum C_b Gamma_{v_b}+Delta_w W`; constants cancel exactly. This is why there is no additional edge-count factor.

### Degree ledger

| Polynomial or certificate | Maximum total degree | Use |
| --- | ---: | --- |
| `Q_i`, `Qbar_i`, `n_i`, `r_i` | `D` | Kernel source input |
| Bag tensor kernel, transformed objective, original objective | `vD<=R` | Evaluation through Chebyshev coefficient bounds |
| Separator tensor kernel | `|S|D<=R` | Moment consistency |
| `G` | `(v-j)D<=R` | SOS and coefficient bound |
| `GH` | `vD<=R` | Signed expansion term |
| `GH^2` | `(v+j)D<=2R` | Weighted square positivity |
| Each term of `G(delta^{2j}-H^2)` | `(v+j)D<=2R` | Ordinary-module residual bound |
| Single-residual expansion certificate | `vD<=R` | Ordinary-module nonnegativity |
| Square factor `q_lH` | `(v+j)D/2<=R` | Weighted Cauchy–Schwarz |

### Every-order rate conversion

Put `kappa=max(3,(w+1)/2)` and `N=2ceil((kappa/2)log_2 s)`. Then

`kappa log_2 s<=N<kappa log_2 s+2`, `delta<=1/(2s^kappa)`, and `B<=3s(N+1)/2`.

The binomial remainder obeys

`Delta_w<=binom(w,2)delta^2(B+delta)^{w-2}`.

For fixed width at least two its order is at most `log^{w-2}(s)/s^3`, hence it is `o_w(log(s)/s^2)`. Width one gives zero correction. Also

`eta<=(3d_infty^2+1)(N+1)/s^2`.

To check the residual part of this bound, use `D+1<=2s(N+1)` and `delta<=1/(2s^3)` to get `sqrt(2(D+1))delta<=sqrt(N+1)/s^{5/2}<=(N+1)/s^2`. The other part follows from `C_s>=2s/3`.

Once `w eta<=1`, `Gamma_w<=e w eta`. To cover every sufficiently large order rather than a subsequence, one valid explicit choice is

`s=floor(R/[2w(kappa+3)log_2(R+2)])`.

When `s>=2`, the preceding bound on `N` gives `wD<=2ws(kappa+3)log_2 s<=R`. Eventually the fixed degree and small-`eta` conditions also hold. Since `s` is of order `R/log R` with a width-dependent constant, the normalized error has order `log^3 R/R^2`. The constant does not involve bag count.

## Gluing and the optional approximate-consistency variant

The exact laws constructed above can be glued without invoking a separate deep marginal theorem. Root the bag tree. If a child bag has separator `S` with its parent and new variables `C`, write its continuous corrected density as `h_b(y_S,y_C)` and its marginal density as `h_S(y_S)`. Where `h_S>0`, use the conditional kernel

`h_b(y_S,y_C)/h_S(y_S) dmu^C(y_C)`.

Where `h_S=0`, assign any fixed probability law, for example `mu^C`. The exceptional set has zero separator probability. Integrating shows that the bag law is recovered, including on the zero-density set. Running intersection ensures that the child's intersection with all previously attached variables is exactly its parent separator. Induction therefore constructs a global law preserving all bag marginals. The same argument, with sums, proves finite-grid gluing. Empty separators are harmless.

This explicit density construction can replace a citation to regular conditional distributions for the central box kernel proof. General standard-Borel disintegration is still useful for recourse and other extensions whose laws need not have these polynomial densities.

I also checked the companion approximate-consistency route in `sparse-putinar-kernel.md`, Sections 4–5. Its SOS mass products satisfy `a^k<=prod n_i<=1` under the ordinary module by induction using only one interval certificate per term and globally SOS multipliers. Multiplying by a separator SOS kernel preserves the degree bound. Thus the pointwise marginal domination and the normalized direction `Z_b<=Z_S` are correct. With total variation defined as `sup_A |P(A)-Q(A)|`, a shared dominated probability component of mass `a^{k_e}` gives discrepancy at most `1-a^{k_e}`, with no factor two.

Maximal coupling can be lifted to full bag laws and then glued along the tree of bag copies. A union bound controls disagreement by `min(1,sum_e epsilon_e)`. On complete agreement running intersection gives a global point; on failure a fixed box point changes the objective by at most `W`. This proves the companion finite bound, but that route has an extra edge-count contribution. The exact common correction is the more appropriate central theorem for bag-count uniformity. No claim in this audit relies on numerical coupling construction.

## Fixed quadratic sharpness and finite-order examples

Sources: `quadratic-sharpness.md:10–219`; `quadratic-exact-gap-frontier.md:17–249`. I rederived the separator minima, approximation duality, Fourier witness, affine coefficient budget, and certificate scope. I also performed an independent symbolic identity check of the long order-two certificate, rather than rerunning its experiment or verification script.

For `x,z in [0,1]`, `y in [-1,1]`, let

`f=x^2-2xy+y^2+z^2+2yz`, `h(y)=max(y,0)^2`.

The local minima are `-h(y)` and `h(y)`, attained at `x=max(y,0)` and `z=max(-y,0)`. Both choices are in their prescribed intervals. Moreover `f=(y-x+z)^2+2xz>=0`, and its minimum is zero.

### Actual local measures and approximation duality

If separator laws match moments through degree `n`, their best conditional private choices reduce the objective to `-int h dmu_1+int h dmu_2`. Any degree-at-most-`n` polynomial cancels between the laws, giving a lower objective bound `-2E_n(h)`.

For equality, the polynomial space is a closed finite-dimensional subspace of `C([-1,1])`. The distance functional on its span with `h` extends by Hahn–Banach to a norm-one functional annihilating that polynomial space and taking value `E_n(h)` on `h`. Riesz gives a signed measure of total variation one. Annihilation of constants makes its two Jordan masses exactly one half. Doubling the positive and negative parts yields matching-moment probability laws whose objective is `-2E_n(h)`. Thus `v_n=-2E_n(h)`. Compactness of the probability-law space and closedness of the moment constraints justify the word minimum. This identity concerns actual local measures, not automatically truncated SOS cones.

### Explicit inverse-square witness

For odd positive `k`, integration of `cos^2 theta=(1+cos 2theta)/2` over the positive half of cosine gives

`c_k=(2/pi)int_0^{pi/2}cos^2 theta cos(k theta)dtheta = -4sin(kpi/2)/[pi k(k^2-4)]`.

Choose the smallest even `N>=n+1`, hence `N<=n+2`. The density `Q_N(theta)=sin(2N(theta-pi/2))F_N(theta-pi/2)` has absolute integral at most one under normalized circle measure. Its positive frequencies are `N+1,...,3N-1`, with weights `w_k=1-|k-2N|/N`. Every frequency exceeds `n`, so it annihilates `p(cos theta)` for all polynomials of degree at most `n`.

Its cosine coefficient at odd `k` is `-w_k sin(kpi/2)`. Pairing with `h(cos theta)` has the correct factor one half from Fourier orthogonality, giving

`int h(cos theta)Q_N(theta)dtheta/(2pi) = (2/pi)sum_{N<k<3N, k odd} w_k/[k(k^2-4)]`.

All frequencies used here are at least three, so the denominators are positive. The odd weights sum to `N/2`: pair the offsets `2N-j` and `2N+j`, for odd `j<N`. Each denominator is less than `27N^3`, giving a pairing at least `1/(27pi N^2)`. This proves `E_n(h)>=1/[27pi(n+2)^2]`.

Push the signed circle law through cosine. Its variation is at most one and its pairing stays positive. Its equal Jordan masses `t` satisfy `0<t<=1/2`. Dividing each Jordan part by `t` produces two probability laws matching moments through `n`, with `h`-integral difference at least `2/[27pi(n+2)^2]`. Lift them by the deterministic private minimizers. These are actual locally supported measures, so every local module or preordering positivity test holds.

Taking `n=2r` gives `-rho_r>=2/[27pi(2r+2)^2]` for either local hierarchy. The direction follows because a moment relaxation infimum is at most the witness objective.

After `x=(u+1)/2`, `z=(v+1)/2`, the Chebyshev local splits are

`f_1=3/8+u/2+T_2(u)/8-uy-y`,

`f_2=7/8+T_2(y)/2+T_2(v)/8+v/2+vy+y`.

Their `A` contributions are `4` and `6`, so the full-preordering bound is `-rho_r<=30/[2(floor(r/2)+1)^2+1]<=60/r^2` for `r>=2`. This proves sharp exponent two for that preordering and for the actual-local-measure hierarchy. It does not prove removal of logarithms from the ordinary-module upper theorem.

The dense degree-four certificate uses

`xz=(xz)^2+z^2 x(1-x)+x^2 z(1-z)+x(1-x)z(1-z)`.

Together with `f=(y-x+z)^2+2xz`, this is a dense order-two full-preordering certificate using quadratic interval generators. It contains a product of distinct generators. The claim is not a dense ordinary-module certificate. With all linear endpoint generators in the dense preordering, the `xz` term itself is a product and exactness already occurs at degree two.

Any exact split into nonnegative bag polynomials must be `x^2-2xy+p(y)` and `y^2+z^2+2yz-p(y)`: the intersection of the two bag polynomial rings is `R[y]`. The separator minima force `p=h`, impossible for a polynomial. This establishes failure of exact polynomial separator attainment at every finite degree, while preserving the finite SDP dual-attainment statement proved earlier.

### First two orders

At order one the local preordering and ordinary module coincide. The identity

`x^2-2xy+y^2/2+y/2+1/8 = (2x-y-1/2)^2/2+x(1-x)`

and its reflection give a lower bound `-1/4`. The positive atomic law with masses `3/4` at `(0,-1/2)` and `1/4` at `(1,3/2)` has PSD moment matrix and generator expectations `0` and `1/4`. It is a representation of a feasible truncated functional, not a rectangle-supported measure. Its reflected second-bag law matches separator moments through degree two and gives total objective `-1/4`. Therefore both sparse order-one bounds equal `-1/4`.

The actual-local-measure value is `v_2=-(3-2sqrt(2))`, strictly larger. The polynomial `y^2/2+(sqrt(2)-1)y` has uniform error `(sqrt(2)-1)^2/2`, attained with alternating signs at four ordered points. A strictly better degree-two polynomial would force three sign changes in its difference from this polynomial. Thus this approximation value is exact. It follows that a degree-specific local SOS membership claim cannot be inferred solely from the optimal polynomial majorant.

For order two, put `s=sqrt(3)`, `a=3s-5`, `b=s-1`, `A=(3+2s)/18`, `E=-4/3+7s/9`, and `p=A(y+1)(y+a)^2`. Direct factorization gives `p-y^2=A(y+7-4s)(y-b)^2` and `p(y)+p(-y)=y^2+2E`. Thus `0<=p-h<=2E`. The six ordered contacts `-1,-b,-a,a,b,1` have errors `0,2E,0,2E,0,2E`. Consequently `p-E`, although cubic, is a best degree-four approximation, by the five required sign changes in any strictly better difference polynomial.

The source's long local identity `x^2-2xy+p(y)=V^TQV+g_xW^TRW+g_y kZ^2` was independently expanded symbolically in this audit. The exact residual is zero. Its leading principal minors are exactly

`Q: 2-s, (35s-58)/24, (38-15s)/864`,

`R: 2-s, (13s-22)/8`.

They are positive: `s<2`, `35^2*3>58^2`, `13^2*3>22^2`, and `15s<30<38`. Also `k>0`. The quadratic forms are therefore SOS, and all complete summands have degree at most four. Reflection certifies `f+2E` in the sparse ordinary module.

The supplied first separator law on `-1,-a,b` has positive masses `(8-4s)/9`, `5/18+s/6`, `-1/6+5s/18`. I independently checked exact total mass one, vanishing first and third moments, and objective `-2E` after reflection and lifting. Reflection matches all moments through degree four. Thus

`rho_2^Q=rho_2^T=v_4=8/3-14sqrt(3)/9`.

This exact conclusion does not use floating-point SDPs, the general Hahn–Banach identity, or finite SDP strong duality. No all-order degree-specific certificate was established; the higher-order conjecture must remain outside the paper's theorem claims.

## External statements needed from the literature agent

No literature search was conducted by this auditor. The writer can use the explicit kernel proofs above without importing possibly imprecise source degree conventions. The following exact standard statements still need appropriate primary references, or proofs where preferred.

1. **Non-strict univariate interval positivity with degree bounds.** If `p>=0` on `[-1,1]` and `deg p<=2d`, then `p=sigma_0+(1-x^2)sigma_1`, where `sigma_0` is SOS of square factors of degree at most `d`, and `sigma_1` is SOS of square factors of degree at most `d-1`. This includes polynomials whose actual degree is odd but is bounded by the even cap, and includes zeros on the interval. An untruncated or strict-positivity theorem is insufficient for this proof. Affine interval variants follow by substitution.
2. **Finite SDP primal Slater theorem.** Strict feasibility on the equality affine space and a finite primal optimum imply no gap and attained dual optimum. Redundant equalities are allowed after restriction to their affine solution space. Primal attainment here is supplied independently by compactness.
3. **Hahn–Banach and Riesz representation on a compact interval**, with equality between the functional norm and total variation norm of its representing finite signed measure. This is needed only if the exact characterization `v_n=-2E_n(h)` is retained; the explicit lower witness and both finite-order SDP values do not require it.
4. **Normalized Gauss–Chebyshev quadrature exactness through degree `2N-1`**, if the finite grid consequence is included. It could alternatively be proved directly by the finite cosine sums at `(2j-1)pi/(2N)`.
5. **Standard-Borel conditional laws and maximal coupling**, only for the approximate-consistency theorem or extensions beyond polynomial-density gluing. The central exact-density theorem has the explicit conditional construction above.

Novelty and prior-work comparison are outside this mathematical audit. The brief's restriction against claiming the sparse preordering inverse-square rate as new must remain. The paper must distinguish established univariate kernels and dense rates from its particular sparse exact-consistency transfer.

## Verification actually performed

Read-only `cat`, `nl -ba`, `sed`, `rg --files`, and `wc -l` commands inspected the assigned source notes, `AGENTS.md`, the paper brief, and the relevant independent reviews. These were targeted reads.

One new targeted symbolic command was run: `python3 -B - <<'PY' ... PY` with SymPy, reconstructing the order-two Gram certificate from its displayed coefficients, expanding its residual as a polynomial, computing the two sets of leading principal minors, checking the witness total mass and odd separator moments, checking its objective, and expanding the order-one certificate. Results:

```text
Order-two polynomial certificate: exact zero residual.
Leading principal minors: [2 - sqrt(3), -29/12 + 35*sqrt(3)/24,
19/432 - 5*sqrt(3)/288] [2 - sqrt(3), -11/4 + 13*sqrt(3)/8]
Order-two witness: exact mass, odd moment cancellation, and objective verified.
Order-one local identity: exact zero residual.
```

All-degree kernel estimates, moment positivity, compactness, residual degree ledgers, exact marginal consistency, gluing, and the explicit Fourier lower bound were checked by the mathematical derivations in this report. The symbolic check establishes only the concrete finite identities it computes. Historical experimental records were read as records and were not rerun. No project-wide check or CI result is claimed.
