# Independent audit of constraints, finite states, and rational certificates

Date: 2026-10-05. This report is mathematical review evidence, not submission text.

## Verdict and scope

The three supporting source results survive independent reconstruction under their stated assumptions. No fatal defect was found. The constrained ordinary-module transport proof needs its degree-preserving polynomial-difference certificate; pointwise Lipschitz continuity alone cannot replace that certificate under truncated moments. The rational construction needs positive objective slack and full monomial Gram bases. Its complexity is polynomial in expanded SDP dimensions, not the original polynomial input size. The constrained results do not establish attained dual certificates merely from a global error bound.

Two coherent completions are proved below:

1. The common exact-consistency density correction extends to the finite-state ordinary-module hierarchy if the correction for each label is multiplied by that label's mass. The resulting labels remain feasible exactly, and the coefficient-normalized ordinary rate has no additional bag-count factor.
2. The corrected density in the continuous constrained model dominates a scaled version of the original SOS density. This lets the same exact-consistency transfer control violations without invoking a separate tree disagreement event. It retains the established constrained rate and aligns that extension with the paper's central transfer.

Both are proof developments, not novelty claims. The second is optional; it is not needed to validate the existing source theorem. No extension to label-dependent boxes or generic rational constrained cones is justified here.

Sources read: `AGENTS.md`, `paper-sparse-sos/evidence/BRIEF.md`, `general-constraints-kernel.md`, `general-constraints-fresh-review.md`, `mixed-discrete-extension.md`, `mixed-discrete-review.md`, `rational-sparse-certificates.md`, `rational-certificates-review.md`, `sparse-kernel-rounding.md`, `sparse-putinar-kernel.md`, `sparse-putinar-exact-consistency.md`, and the statement and local-measure construction of `affine-recourse-rate-boundary.md`, all solver notes under `research-20260928/solver/`.

## 1. Global geometric repair is an indispensable assumption

Let the bags form a finite running-intersection tree covering all continuous coordinates. Write

\[
 K=\{x\in[-1,1]^n:g_{bj}(x_{B_b})\ge0\ \forall b,j\}\ne\varnothing,
 \quad V(x)=\sum_{b,j}(-g_{bj}(x_{B_b}))_+^2.
\]

The required hypothesis is

\[
 \operatorname{dist}_2(x,K)\le H V(x)^{\alpha/2}
 \quad\forall x\in[-1,1]^n,
 \qquad H\ge0,\quad0<\alpha\le1.
 \tag{GEB}
\]

It is a bound to the global feasible intersection in the original coordinate space. Local bag error bounds do not imply it with the same exponent or constant.

A concrete obstruction uses bags `{x,y}` and `{y,z}`, with

\[
 g_1=y-x^2,\qquad g_2=-y.
\]

For the first local constraint, replacing `y` by `max(y,x^2)` stays in its bag box and repairs it at distance at most `(-g_1)_+`. For the second, replacing `y` by `min(y,0)` does the same. Thus both local sets have linear repair bounds with constant one. Globally, however, `K={x=y=0}` times the free `z` interval. At `(t,0,0)`, distance is `|t|` and `V=t^4`. A global linear bound would require `|t|<=H t^2`, which fails near zero. A possible global exponent must satisfy `alpha<=1/2`. Both local constraints are concave and separately strictly feasible, but they do not have a common Slater point. This is also a direct reason to exclude assertions based on different bagwise Slater points.

Once a single global law `sigma` satisfies `int V d sigma<=U` and `int f d sigma<=M+E`, (GEB) supplies the exact repair conclusion

\[
 \exists\nu\text{ supported on }K:\quad
 \int f\,d\nu\le M+E+L_f H U^{\alpha/2}.
 \tag{1}
\]

Here `L_f` is a Euclidean Lipschitz constant on the entire box. A constructive measurable-selection theorem is unnecessary: choose a finite epsilon-net in compact `K`, send each box point to its nearest net point with fixed tie breaking, and obtain a Borel map whose distance is at most `dist(x,K)+epsilon`. Lipschitz continuity and Jensen yield (1) with an additional `L_f epsilon`. Compactness of the probability laws on `K` and continuity of `f` give (1) in the limit. This proves existence of a repaired law and a feasible point no worse than its mean. It does not prove efficient global projection.

If all extra generators are concave and one common box point satisfies every `g>=sigma_0>0`, the interpolation

\[
 y=(1-\theta)x+\theta x_0,\quad
 \theta=v/(\sigma_0+v),\quad v=\max_{b,j}(-g_{bj}(x))_+
\]

is feasible, giving (GEB) with `alpha=1` and `H=2 sqrt(n)/sigma_0`. This is an elementary proof and does not need an external convex error-bound theorem. Hoffman bounds for polyhedra and general semialgebraic Hölder bounds are optional contextual statements requiring exact citations and hypotheses; they need not be used in the main proof. The exponent is generator dependent: replacing an inequality by a vanishing high power may worsen this route even if the set remains the same.

## 2. Full-preordering constrained theorem: contract and reconstruction

For a bag let `q_I=prod_{i in I}(1-x_i^2)`. The required conditions, through total degree `2R`, are

\[
 L_b(q_I p^2)\ge0,\qquad L_b(g_{bj}q_Ip^2)\ge0
\]

whenever the displayed product has degree at most `2R`. All bags are normalized and agree on all separator polynomials through `2R`. Ordinary extra localizers `L_b(g p^2)>=0` alone do not suffice for this particular preordering kernel. No product of two distinct extra constraints is needed. A full preordering in all supplied generators is stronger and also meets the contract.

Put

\[
 d=\max(1,\max_b\deg f_b,\max_{b,j}\deg g_{bj}),\quad
 R\ge\max(2d,d+w),\quad
 m=\lfloor(R-d)/w\rfloor+1,\quad D_m=2m^2+1,
\]

and, in the tensor Chebyshev basis,

\[
 C(p)=\sum_\beta|p_\beta|,\quad
 A(p)=\sum_\beta|p_\beta|\sum_i\beta_i^2,\quad
 A_f=\sum_b A(f_b),\quad G=\sum_{b,j}C(g_{bj})A(g_{bj}).
\]

The valid finite-order conclusion is

\[
 f^*-\rho_R\le {3A_f\over D_m}
       +L_fH\left({12G\over D_m}\right)^{\alpha/2}.
 \tag{2}
\]

The degree reserve is essential but introduces only an additive fixed-degree cost. The source kernel has preordering degree at most `2w(m-1)<=2(R-d)`. Multiplying it by `(a+b g)^2` costs at most `2d`, and multiplying by `g` uses precisely the stated additional localizers. Consequently `F_y(p)=L_b(K_b p)` has the required conditional PSD property and `F_y(g)>=0`. Cauchy--Schwarz gives

\[
 (-g(y))_+^2 L_b(K_b)\le L_b(K_b(g(x)-g(y))^2).
 \tag{3}
\]

When `L_b(K_b)=0` the right side is nonnegative; no normalization by that density is used.

After integration, the residual is

\[
 A_b(g^2)-2gA_bg+g^2,
\]

of total degree at most `2 deg(g)<=2d<=R`. Therefore the valid moment bound `|L_b(T_beta)|<=1` applies; no unjustified degree-`2R` coefficient estimate occurs. The multiplier loss is at most `3 sum_i beta_i^2/D_m`. Tensor Chebyshev multiplication gives

\[
 C(pq)\le C(p)C(q),\quad
 A(pq)\le C(p)A(q)+A(p)C(q).
\]

The second formula follows from the average squared frequency in `T_aT_b=(T_{a+b}+T_{|a-b|})/2`, coordinate by coordinate, including zero indices. Thus the residual coefficient norm is at most `12 C(g)A(g)/D_m`. Exact kernel normalization makes the smoothed bag laws agree exactly, so one and the same global law has objective error `3A_f/D_m` and expected violation `12G/D_m`. Applying (1) proves (2).

For fixed problem data and fixed width, (2) is `O(R^{-alpha})`. The objective term is `O(R^{-2})`; the repair term determines the asserted general exponent. Neither width, generator normalization, `H`, nor `L_f` is uniform unless explicitly bounded. The source affine-recourse example with linear constraints has genuine supported local measures producing a `Theta(1/R)` separator-matching gap. Those measures remain feasible after adding redundant box generators or taking stronger full local preorderings. It therefore makes power one sharp for the broad `alpha=1` class. It does not show sharpness for every geometry or necessity of the ordinary-module logarithm.

## 3. Ordinary constrained theorem: the transport argument and logarithms

The ordinary local cone uses only squares, singleton box localizers, and `g_{bj}` times squares. Let

\[
 Q(x,y)=p_{s,N}(x)S_s(x,y)^2,\quad
 D=2(s-1)(N+1),\quad \delta=2^{-(N+1)},\quad a=1-\delta,
\]

where `s>=max(2,d_infty)`, `N>=2` is even, and `R>=wD+2d`. The source kernel `Q_b=prod Q` is globally SOS of degree at most `v_b D`. Its mass factors `n=int Q dmu` are globally SOS, satisfy `a<=n<=1`, and have degree at most `D`. Write

\[
 c_s={4\over s C_s}\le{6\over s^2},\qquad C_s={2s^2+1\over3s}.
\]

The direct squared-displacement estimate is valid. With `x=cos theta`, `y=cos phi`, the kernel `S_s` is the average of two Fejér kernels. Convexity of a square and the cosine difference inequality yield

\[
 J_s(x)=\int(x-y)^2 S_s(x,y)^2d\mu(y)
 \le\sum_{j\in\mathbb Z}(b_j-b_{j-1})^2={2\over s},
 \quad b_j=(1-|j|/s)_+.
\]

There are exactly `2s` nonzero differences of magnitude `1/s`. Since `0<=p_{s,N}<=2/C_s`, the globally SOS polynomial `j_s=p_{s,N}J_s` satisfies `0<=j_s<=c_s` and has degree at most `D+2`. The even-degree interval SOS theorem gives a certificate for `c_s-j_s` in the singleton interval module with the same degree bound. This certificate is necessary to apply the inequality under a pseudomoment functional.

A second indispensable certificate is, for fixed output `y`,

\[
 A(g)\sum_i A_i(g)(x_i-y_i)^2-(g(x)-g(y))^2
 \in Q_{\rm box,\,deg(g)},
 \quad A_i(g)=\sum_\beta|c_\beta|\beta_i^2,
 \tag{4}
\]

with total representation degree at most `2 deg(g)`. To reconstruct it, telescope each tensor Chebyshev difference. Index the terms by `ell=(beta,i)` with `beta_i>0`, set `w_ell=|c_beta| beta_i^2` and write

\[
 g(x)-g(y)=\sum_\ell w_\ell t_\ell r_\ell(x),\quad
 t_\ell=x_i-y_i,\quad \sum_\ell w_\ell=A(g).
\]

The factor `r_ell` is the signed normalized divided difference
`(T_k(x_i)-T_k(y_i))/(k^2(x_i-y_i))` times earlier source Chebyshev factors and later constant output factors. Its divided-difference extension is polynomial of degree `k-1` and is bounded by one on the interval. Each nonconstant univariate factor has an interval certificate for one minus its square. Telescoping one minus the product of those squared factors multiplies the certificates only by squares, leaving one box generator per term and total degree at most `2(|beta|-1)`. Thus `1-r_ell^2` is in the ordinary box module at that degree. The exact weighted-square identity

\[
 A\sum_\ell w_\ell t_\ell^2
 -(\sum_\ell w_\ell t_\ell r_\ell)^2
 =A\sum_\ell w_\ell t_\ell^2(1-r_\ell^2)
   +\sum_{\ell<k}w_\ell w_k(t_\ell r_\ell-t_k r_k)^2
\]

proves (4). Constant constraints give the zero identity. This argument avoids the invalid inference that multivariate pointwise nonnegativity automatically implies module membership.

Multiply (4) by the globally SOS `Q_b`, evaluate at each fixed `y`, then integrate the resulting scalar inequality. This order does not require a measurable choice of interval SOS certificates. The degree is at most `v_bD+2d<=R`, safely within the source's reserve. The product mass identity gives

\[
 c_s-j_s(x_i)\prod_{\ell\ne i}n(x_\ell)
 =c_s(1-\prod_{\ell\ne i}n(x_\ell))
 +(c_s-j_s(x_i))\prod_{\ell\ne i}n(x_\ell),
\]

which is an ordinary-module certificate of degree at most `v_bD+2`. It follows that

\[
 \int(-g(y))_+^2 h_b(y)d\mu_b(y)\le c_s A(g)^2,
 \quad h_b=L_b(Q_b).
 \tag{5}
\]

The source's approximate-consistency repair therefore gives

\[
 U_{s,N}=c_s\sum_{b,j}{A(g_{bj})^2\over a^{v_b}}
       +\Bigl(\sum_{b,j} C(g_{bj})^2\Bigr)\varepsilon_T,
 \quad\varepsilon_T=\min(1,\sum_e\varepsilon_e),
\]

and `f^*-rho_R<=E_{s,N}+L_fH U_{s,N}^{alpha/2}`. This existing theorem is sound.

With `N=2 ceil((3/2)log_2 s)` and a fixed tree, `delta=O(s^{-3})`, `epsilon_T=O(s^{-3})`, `U=O(s^{-2})`, whereas the objective error is `E=O(log(s)/s^2)`. Since the degree `D` is `Theta(s log s)`, moment order `R` permits `s=Theta(R/log R)` at fixed width. Thus

\[
 U=O(\log^2 R/R^2),\quad
 E=O(\log^3 R/R^2),\quad
 f^*-\rho_R=O((\log R/R)^\alpha),\quad0<\alpha\le1.
 \tag{6}
\]

The objective term still has three logarithms; the squared-violation improvement has two. Raising `U` to `alpha/2` explains the logarithm in the constrained objective rate. There is no further degree or logarithmic factor hidden in (4). The additional reserve `2d` is additive for fixed data. The approximate-consistency version is not uniform in tree size.

## 4. Optional coherent constrained transfer using exact consistency

This replaces the separate tree disagreement argument by the main paper's common density correction. Use the same ordinary SOS kernel, the same constrained degree reserve, and

\[
 r_i(x_i)=1-n(x_i),\quad
 B={s^2(N+1)\over C_s},\quad
 \Delta_w=\sum_{j=2}^w\binom wj\delta^j B^{w-j},
\]

with `Delta_0=Delta_1=0`. The exactly normalized signed kernel product gives `hbar_b=L_b(prod_i(Q_i+r_i))`. Its residual-subset expansion has nonnegative zero-residual term `h_b`, nonnegative singleton-residual terms, and each subset of size `j>=2` is bounded below by `-delta^j B^{v_b-j}`. Consequently

\[
 \overline h_b\ge h_b-\Delta_w,
 \quad h_b^+={\overline h_b+\Delta_w\over1+\Delta_w}
 \ge {h_b\over1+\Delta_w}.
 \tag{7}
\]

The corrected laws have mass one and matching separators. The difference between `h_b^+` and `h_b/(1+Delta_w)` is a nonnegative density of mass `(1+Delta_w-Z_b)/(1+Delta_w)`, where `Z_b=int h_b>=a^{v_b}`. Since `sup(-g)_+^2<=C(g)^2`, (5) and (7) give

\[
 \int(-g)_+^2 h_b^+d\mu_b
 \le {c_s A(g)^2+C(g)^2(1+\Delta_w-a^{v_b})\over1+\Delta_w}.
\]

The common global law with these marginals thus satisfies

\[
 \int V\,d\sigma\le
 U^{\rm exact}_{s,N}:=
 {c_s\sum_{b,j}A(g_{bj})^2
 +\sum_{b,j}C(g_{bj})^2(1+\Delta_w-a^{v_b})\over1+\Delta_w}.
 \tag{8}
\]

Let the constant-free objective coefficient budgets be `C_b`, let `W=sum_b osc(f_b)`, and let `Gamma_v=(1+eta)^v-1` be the established ordinary kernel coefficient-error factor. The same law satisfies objective error

\[
 E^{\rm exact}_{s,N}=\sum_b C_b\Gamma_{v_b}+\Delta_w W.
 \tag{9}
\]

Equations (1), (8), and (9) prove the finite-order constrained gap bound. This requires no new geometric theorem and has no separate factor in the number of edges or bags. Its sums, `H`, and `L_f` still scale with the actual problem.

Take the exact-consistency parameter choice

\[
 N=2\left\lceil\max\left({3\over2},{w+1\over4}\right)\log_2s\right\rceil.
 \tag{10}
\]

At fixed width, `delta=O(s^{-3})` and
`Delta_w=O_w(log^{w-2}(s)/s^3)` for `w>=2`, hence `Delta_w=o_w(s^{-2})`. The latter inference uses the fact that every fixed power of a logarithm is `o(s)`; it is not uniform in growing width. Thus `Uexact=O(s^{-2})`, `Eexact=O(log(s)/s^2)`, and (6) remains valid. The order-to-bandwidth constant now depends on width through (10), as it already does in the main exact-consistency theorem.

This argument controls violation rather than preserving the extra constraints during smoothing. Global repair remains necessary. It supplies no dual attainment for constrained problems. It is a valid option if the paper wants one common transfer mechanism throughout; otherwise retain the original constrained theorem and do not advertise extra uniformity.

## 5. Finite-state full-preordering result and edge cases

Let each bag be `(C_b,D_b)`, where `C_b` contains continuous variables and `D_b` finite-state variables, and let `A_b` be its explicitly listed permitted local labels. All continuous coordinates share the same fixed box for every label. The globally permitted assignments

\[
 \mathcal A=\{a:a_{D_b}\in A_b\ \forall b\}
\]

are nonempty. Running intersection applies separately to every continuous and finite-state variable.

For each permitted label use a functional `L_{b,a}` through total degree `2r`, with box-preordering positivity, mass `tau_{b,a}=L_{b,a}(1)>=0`, and `sum_a tau_{b,a}=1`. For every edge, every finite-state separator assignment `s`, and every continuous separator polynomial through degree `2r`, require

\[
 \sum_{a\in A_b:a|_{S_D}=s}L_{b,a}(p)
 =\sum_{a\in A_c:a|_{S_D}=s}L_{c,a}(p).
 \tag{11}
\]

The empty fiber has sum zero, and an empty finite-state separator has one empty label. Restricting (11) to labels present on both sides is invalid: incompatible shared allowed values would otherwise produce a spuriously feasible hierarchy. Individual full-bag labels are not equated across an edge.

At `r>=max(w,d)` with `w=max_b |C_b|>=1`, the source theorem gives

\[
 |\mathbb E_\nu f-\sum_{b,a}L_{b,a}(f_{b,a})|
 \le {3\over2(\lfloor r/w\rfloor+1)^2+1}
       \sum_{b,a}\tau_{b,a}A(f_{b,a})
 \le {3 A_{\rm mix}\over2(\lfloor r/w\rfloor+1)^2+1},
\]

where `A_mix=sum_b max_{a in A_b} A(f_{b,a})`. The bound is independent of the number of labels as an additional factor, although enumerating labels can be exponential and their costs enter the displayed budget. Kernel normalization and (11) give exact mixed separator measures; tree gluing yields a law supported on globally permitted finite labels.

For any label, singleton box positivity alone gives

\[
 0\le L_{b,a}(T_\beta^2)\le\tau_{b,a},\quad
 |L_{b,a}(T_\beta)|\le\tau_{b,a}\qquad(|\beta|\le r).
 \tag{12}
\]

The bound follows from the ordinary-module telescoping certificate for `1-T_beta^2` and moment Cauchy--Schwarz. It contains no division by a label mass. If `tau=0`, all diagonal entries in the degree-`r` Chebyshev moment basis vanish; PSD makes every entry vanish. Products of two degree-at-most-`r` polynomials span all polynomials through `2r`, so the entire functional vanishes. Zero-mass densities and objective errors therefore vanish exactly.

A null separator receives arbitrary conditional laws; these do not change any bag marginal. The finite union of forbidden-label events is null in the glued law. In all-discrete models (`w=0`), the masses alone are consistent bag probabilities and the relaxation is exact, including order zero. Empty continuous bags are positive scalar mass blocks; no fictitious `r/w` is formed.

## 6. Completed ordinary-module finite-state theorem

This development is not stated in the source mixed note. It follows rigorously from the same mass-scaled ordinary moment inequalities and the main exact-consistency proof.

### 6.1 Model and precise finite-order statement

Use the finite-state model and separator equations (11), now through degree `2R`. Replace each labelled preordering by the ordinary box conditions

\[
 L_{b,a}(p^2)\ge0\quad(\deg p\le R),\qquad
 L_{b,a}((1-x_i^2)p^2)\ge0\quad(i\in C_b,\deg p\le R-1).
 \tag{13}
\]

Normalize only the sum of label masses in each bag, not the individual masses. Let `rho_R^mix` be the minimum or infimum of the summed labelled objectives. Write

\[
 f_{b,a}=c_{b,a,0}+g_{b,a},\quad
 C_{b,a}=\sum_{\beta\ne0}|c_{b,a,\beta}|,\quad
 \Omega_{b,a}=\operatorname{osc}_{[-1,1]^{C_b}} f_{b,a}\le2C_{b,a}.
\]

Let `d` be the largest total objective degree and `d_infty` its largest coordinate degree. If `w>=1`, choose `s>=max(2,d_infty)`, even `N>=2`, and `R>=max(d,wD)`, with `D`, `delta`, `B`, and `Delta_w` as above. The explicit ordinary coefficient-error factor is

\[
 \eta={N+1\over C_s}\left({d_\infty^2\over s^2}
                  +{3d_\infty^2\over2s}\right)
       +\sqrt{2(D+1)}\,\delta,
 \quad\Gamma_v=(1+\eta)^v-1.
\]

The separate condition `R>=d` makes objective moment control explicit; it is in fact implied by `s>=d_infty` and `R>=wD` when `w>=1`.

**Theorem.** Every feasible collection in (11), (13) admits a global law supported on `mathcal A times [-1,1]^n` satisfying

\[
 \left|\mathbb E_\nu f-\sum_{b,a}L_{b,a}(f_{b,a})\right|
 \le \sum_{b,a}\tau_{b,a}C_{b,a}\Gamma_{v_b}
       +\Delta_w\sum_{b,a}\tau_{b,a}\Omega_{b,a},
 \quad v_b=|C_b|.
 \tag{14}
\]

Define the a priori coefficient budget

\[
 C_{\rm mix}=\sum_b\max_{a\in A_b}C_{b,a}.
\]

Then the right side of (14) is at most

\[
 C_{\rm mix}(\Gamma_w+2\Delta_w).
 \tag{15}
\]

Consequently `0<=f^*-rho_R^mix<=` (15). The sharper bound (14) is weighted by the actual label masses of the given moment collection; (15) is the data-only bound applicable to the optimum. Constants that depend on labels alone create no smoothing or correction error. If `w=0`, the labelled hierarchy is exactly the consistent finite-state probability model, so its gap is zero at order zero.

### 6.2 Mass-scaled signed density proof

By (12) with `r=R`, `|L_{b,a}(T_beta)|<=tau_{b,a}` for all `|beta|<=R`. Define

\[
 \overline Q(x,y)=Q(x,y)+r(x),\quad r=1-n,
 \qquad
 \overline h_{b,a}(y)=L_{b,a}(\prod_{i\in C_b}\overline Q(x_i,y_i)).
\]

Its mass is exactly `tau_{b,a}`. Integrating away continuous coordinates replaces their source factors by one. Summing the labels over the appropriate separator fiber and using (11) therefore gives exactly equal mixed signed separator densities. Empty continuous products equal one.

For a residual subset `J` with `j=|J|`, set `G=prod_{i notin J}Q(x_i,y_i)` and `H=prod_{i in J}r(x_i)`. Here `G` is globally SOS, `deg G<=(v_b-j)D`, and `deg H<=jD`. The interval certificate for `delta^2-r_i^2`, multiplied by `G` and prior residual squares, gives

\[
 0\le L_{b,a}(GH^2)\le\delta^{2j}L_{b,a}(G).
\]

Every term has total degree at most `(v_b+j)D<=2wD<=2R`. The weighted square form for `L_{b,a}(G .)` is positive on the pair `1,H`: if `G=sum q_l^2`, then `deg(q_l H)<=(v_b+j)D/2<=R`. Cauchy--Schwarz therefore gives

\[
 |L_{b,a}(GH)|\le\delta^j L_{b,a}(G)
               \le\tau_{b,a}\delta^j B^{v_b-j}.
 \tag{16}
\]

The last step uses the Chebyshev norm bound `C(Q(.,y))<=B` and moment control through degree `R`; `deg G<=v_bD<=R`. No claim about arbitrary degree-`2R` Chebyshev moments is made. No division by `L(G)` or `tau` is needed, so (16) remains valid at zero mass.

The `j=0` summand is nonnegative because its source polynomial is SOS. The `j=1` summands are also nonnegative: an interval certificate for nonnegative `r_i` multiplied by the other SOS kernel factors lies in the ordinary box module at degree at most `v_bD`. Summing (16) over `j>=2` and using `B>=1` yields

\[
 \overline h_{b,a}(y)\ge-\tau_{b,a}\Delta_{v_b}
                    \ge-\tau_{b,a}\Delta_w.
\]

Now make the mass-scaled common correction

\[
 h^+_{b,a}(y)=
 {\overline h_{b,a}(y)+\Delta_w\tau_{b,a}\over1+\Delta_w}.
 \tag{17}
\]

It is nonnegative and still has mass `tau_{b,a}`. This mass factor is essential: adding the same bare constant separately to every local label generally destroys separator fiber sums and bag normalization.

For a separator label `s`, the added reference density is

\[
 \Delta_w\sum_{a:a|_{S_D}=s}\tau_{b,a}.
\]

These sums agree on the two endpoints by (11) at `p=1`. The original signed densities also agree, and the denominator is common to every bag and label. Thus (17) gives genuine mixed bag probability laws with exact separators. Tree gluing produces a global law, and its finite-state support argument is exactly the one in Section 5. An empty continuous bag has `hbar=tau` and `h+=tau`; a zero-mass label has both densities zero. A missing separator fiber remains zero.

### 6.3 Objective identity and degree ledger

The exactly normalized univariate operator obeys `Abar 1=1` and `Abar T_k=A T_k` for positive `k`, by arcsine orthogonality. The tensor coefficient estimate therefore gives

\[
 C(\overline A_b g_{b,a}-g_{b,a})
 \le C_{b,a}\Gamma_{v_b}.
\]

All source polynomials here have total degree at most `v_bD<=R`, and `deg f_{b,a}<=d<=R`. Hence mass-scaled moment control gives

\[
 \left|\int f_{b,a}\overline h_{b,a}\,d\mu_b
       -L_{b,a}(f_{b,a})\right|
 \le\tau_{b,a} C_{b,a}\Gamma_{v_b}.
\]

Constants cancel because both terms have label mass `tau`. Rearranging (17),

\[
 \int f_{b,a}h^+_{b,a}\,d\mu_b
 -\int f_{b,a}\overline h_{b,a}\,d\mu_b
 =\Delta_w\left(\tau_{b,a}\int f_{b,a}\,d\mu_b
                  -\int f_{b,a}h^+_{b,a}\,d\mu_b\right).
\]

The two terms in parentheses are expectations under nonnegative measures of the same mass `tau`; their difference is at most `tau Omega_{b,a}`. This works without normalizing a zero-mass label. Summing proves (14), and bag mass normalization gives (15).

The complete degree ledger is: source signed densities at most `vD<=R`; singleton residual positivity at most `vD`; residual-square certificates and weighted Cauchy--Schwarz at most `(v+j)D<=2R`; coefficient-norm evaluation at most `vD<=R`; objective moment bound through `d<=R`; mixed separator source polynomial at most `|S_C|D<=R`, covered by the imposed equalities through `2R`. No additional factor of order or label count is hidden.

### 6.4 Rate and dual boundaries

With (10), fixed `w` and `d_infty`, and `s` sufficiently large, the established estimates give

\[
 \eta\le(3d_\infty^2+1)(N+1)/s^2,
 \quad \Gamma_w\le e w\eta\quad(w\eta\le1),
 \quad\Delta_w=o_w(\log(s)/s^2).
\]

Since `D=Theta_w(s log s)`, `s=Theta_w(R/log R)` is available for every sufficiently large `R`, by choosing the constant sufficiently small. Therefore

\[
 f^*-\rho_R^{\rm mix}
 \le C_{\rm mix}\,O_{w,d_\infty}(\log^3 R/R^2).
 \tag{18}
\]

There is no additional dependence on bag count, tree diameter, or number of labels outside the displayed coefficient budget and expanded SDP size. Width is fixed in this asymptotic statement. For `w=1`, `Delta_w=0`, but the ordinary source kernel coefficient estimate still has the same conservative logarithmic rate. This theorem does not require globally feasible continuous repair because the permitted continuous domain is the common box.

Unextendable local labels should be pruned before invoking primal Slater. Mass equations alone admit discrete junction-tree gluing; hence every such label has mass zero, and (12) forces its entire functional to vanish. Pruning therefore preserves the primal optimum. On the pruned model, take a positive distribution on every globally permitted finite assignment, independently of a product box measure of positive interior density. Every retained labelled moment matrix and singleton box localizer is positive definite, and every equality holds. The objective is bounded by the mass-scaled moments. Finite-SDP primal Slater gives dual attainment and no gap for this pruned SDP.

The dual certificate has labelled local SOS pieces and labelled separator multipliers. On a globally permitted assignment, summing the local identities cancels the separator multipliers. This is an identity on the permitted finite assignment space, or equivalently in a finite indicator-function representation. Do not describe it as an ordinary unlabelled polynomial certificate without defining that representation. No transfer of attained duality to an unpruned formulation is asserted. This argument gives real certificates, not an automatic rational size bound for the labelled cone.

The theorem is not a general MINLP runtime result. Label lists can be exponential; matrix bases depend on order and width. Additional continuous constraints, label-dependent boxes, integer rounding of a continuous surrogate, numerical inconsistency, and arbitrary numerical SDP accuracy are outside its contract. Direct tree-grid optimization remains an essential comparator. The preordering source's finite quadrature extraction result is valid, but its inverse-square grid conclusion must not be silently imported into this ordinary-module proof: (18) is the guarantee proved here.

## 7. Rational Gram certificates: exact assumptions and verified algebra

### 7.1 The necessary real membership promise

Fix rational `p=f-gamma`, rational `tau>0`, full bag monomial bases, and a finite box cone of order `r`. The sufficient condition is a real PSD representation of `p-tau` in that same finite cone. For the box-only hierarchy, primal Slater and the kernel bound establish this condition from

\[
 f^*-\gamma\ge E_r+\tau.
 \tag{19}
\]

For the ordinary box module, the exact-consistency coefficient bound may replace `E_r` in (19), with its own order conditions. The tree is needed for this rate-to-membership implication; it is not needed for rationalization once the membership promise is supplied.

A primal constrained gap alone does not establish (19)'s membership implication in a constrained dual cone. The global error bound (GEB) does not establish Slater. Equality constraints or empty interior can defeat the box-only strict-feasibility proof. Do not promise attained constrained certificates at the exact primal error threshold, or apply the rational theorem to additional-generator blocks, without a separate real cone-membership and conditioning argument. An independent common strict feasible open region can supply primal Slater for ordinary additional inequality localizers, but it is a separate assumption and equalities do not satisfy it.

Positive pointwise `p` at a fixed order is not a replacement for real finite-cone membership of `p-tau`. Slack zero is outside the stated rational margin and size guarantee.

### 7.2 Interior direction without a hidden Gram assumption

For full preorderings, blocks are indexed by `I subset B_b` and use all monomials of degree at most `r-|I|`; assume `r>=w>=1`. Let `D` be the sum of block sizes, `V` their total number of upper-triangular coordinates, `S` the largest block size, and `M` the number of distinct global bag-supported monomials through degree `2r`. Collect coefficients globally, including coincident monomials from different bags.

For each source diagonal `h=x^{2alpha}prod_{i in I}(1-x_i^2)`, the exact complement identity is

\[
 1-h=\sum_i\sum_{j=0}^{\alpha_i-1}
 (x_1^{\alpha_1}\cdots x_{i-1}^{\alpha_{i-1}}x_i^j)^2(1-x_i^2)
 +\sum_{q=1}^{|I|}(x^\alpha x_{i_q})^2
       \prod_{\ell<q}(1-x_{i_\ell}^2).
\]

The first sum telescopes to `1-x^{2alpha}` and the second to `x^{2alpha}(1-g_I)`. Every term is in an allowed block at degree at most `2r`: the second source has monomial degree `|alpha|+1` and generator cardinality `q-1`, whose sum is `|alpha|+q<=r`. This verifies boundary cases, not just interior positions.

Average `1=h+(1-h)` over all `D` source diagonals, including all bags. Each position receives its own positive baseline, so a rational diagonal tuple `H` satisfies

\[
 \mathcal A(H)=1,\quad H_{b,I}\succeq I/D,
 \quad\sum_{b,I}\operatorname{tr}H_{b,I}\le r+1.
\]

The trace bound counts exactly `1+|alpha|+|I|<=r+1` displayed squares per identity, with multiplicity. Thus real membership of `p-tau`, followed by addition of `tau H`, gives a real tuple representing `p` with margin `eta=tau/D` in every block. No strict Gram condition has been inferred merely from positivity of `p`.

For the ordinary module, restrict to empty and singleton `I`. The complement identity stays within that collection: its first part uses singleton generators; the second part for a singleton uses one empty-generator square. All later arguments remain valid with recomputed `D_Q,V_Q,S_Q`; `r>=1` suffices and `r>=w` is unnecessary for this corollary. Reduced term-sparsity bases need not contain these terms or the pivots below and are not covered.

### 7.3 Rational outer bound and expanded dimension dependence

Use the same global product-uniform expectation `ell` in every bag and let `W_{b,I}=ell(g_I v v^T)`. These rational matrices are positive definite because the weights are positive on the open box and a nonzero polynomial cannot vanish there almost everywhere. Their univariate factors are `1/(a+1)` and `2/((a+1)(a+3))` for even `a`, and zero for odd `a`. The integer

\[
 q_0=((2r+3)!)^{2w}
\]

clears every denominator. For a block of size `s`, its positive determinant is at least `q_0^{-s}` since `q_0 W` is an integer positive definite matrix. Each diagonal is at most one, so every eigenvalue is at most `s`. Therefore

\[
 W_{b,I}\succeq\lambda_0 I,
 \quad \lambda_0=q_0^{-S}S^{-(S-1)}.
\]

For PSD tuples representing `p`,

\[
 \lambda_0\sum\operatorname{tr}Q_{b,I}
 \le\sum\operatorname{tr}(W_{b,I}Q_{b,I})
 =\ell(p)\le\|p\|_1.
\]

Bag overlaps create no multiplier or counting error because this is one global polynomial identity under one measure. Thus `R_out=1+||p||_1/lambda_0` bounds every feasible tuple's entries. Its bit length is polynomial in expanded dimensions and input length: `log(1/lambda_0)=O(S w r log(r+2)+S log(S+1))`, with `r+1<=S` for a nonempty bag. For the ordinary restricted cone, width is bounded by the explicit bag-list input even if `w>r`. Exponentially many preordering products and order-dependent bases are already included in `V,M`; no original-input polynomial-time conclusion follows.

### 7.4 Exact coefficient correction, including denominators

Every output monomial has one containing bag and total degree at most `2r`. Split its exponent as `beta=alpha+delta` with `|alpha|,|delta|<=r`. In that bag's empty-generator block choose a diagonal coefficient one if the exponents are equal, or a symmetric off-diagonal pair with each coefficient `1/2` otherwise. This tuple `Z_beta` maps to exactly `x^beta` and has aggregate Frobenius norm at most one. Distinct output exponents cannot share a position because a position has a unique exponent sum. Hence these are simultaneous pivots and give a global right inverse `A Z=id` and `||Z(c)||_F<=||c||_1`.

Round a real strict tuple to a grid of spacing `h=2^{-B_round}`, preserving symmetry, to obtain `Q0`, then set

\[
 Q=Q0+Z(p-\mathcal A(Q0)).
\]

A coefficient column has at most `2^w` generator-expansion terms with magnitude at most two. Thus

\[
 \|Q-Q^*\|_F\le2^{w+2}Vh.
\]

Taking `h<=eta/(2^{w+3}V)` leaves every block at least `(eta/2)I`. The coefficient equality is exact across all bags; this is not separate bagwise projection that might lose cancellations on overlaps.

The corrected denominator bound is `2 lcm(2^{B_round}, input coefficient denominators)`. The additional factor of two is necessary when an off-diagonal pivot halves an input coefficient with a larger two-adic denominator than the rounding grid. The former bound `lcm(2^{B_round+1}, input denominators)` is false in that case. The current source note and review already contain the correction. Numerator and denominator lengths are polynomial in the expanded data, including the input denominators and `log^+(1/tau)`.

### 7.5 Construction time versus existence

Rounding an unknown real strict tuple only proves rational witness existence. The source's separate construction correctly parameterizes the coefficient equality space by the `k=V-M` free upper-triangular coordinates:

\[
 Q(y)=Z(p)+U(y)-Z(\mathcal A(U(y))).
\]

Pivot columns make this a bijection onto the equality space. Its Lipschitz constant may be bounded by `beta=2^{w+2}V`. The free-coordinate body defined by `|y_j|<=R_out+1` and all blocks `Q(y)>=(eta/2)I` contains an unknown-center ball of known radius

\[
 a_{\rm in}=\min(1,\eta/(2\beta)),
\]

and lies in an origin-centered ball of radius `k(R_out+1)`. All bounds have polynomial encoding length. For `k=0`, directly evaluate the unique rational tuple; for `k=1`, rational interval bisection suffices.

At a rational query, exact symmetric elimination either verifies PSD or yields a rational negative quadratic witness. Positive diagonal pivots allow Schur complements; a negative diagonal is already a witness; when all remaining diagonal entries are zero but an off-diagonal entry is nonzero, one of `e_i+e_j` or `e_i-e_j` is a witness. Rational back substitution has polynomial bit length by determinant bounds. The quadratic witness defines a rational separating linear inequality in free coordinates. Under the feasibility promise its normal cannot be zero, since a constant negative value would exclude the promised feasible point.

For `k>=2`, deterministic polynomial-time construction therefore reduces to the standard *rational strong-feasibility ellipsoid theorem* with a known enclosing ball and known positive inner radius, whose inner center need not be supplied. The paper must cite that exact theorem and explicitly include rational rounding of ellipsoid updates to keep query bit lengths polynomial. An exact-real volume argument alone is insufficient for a Turing complexity claim. A theorem requiring an already supplied rational feasible starting point cannot construct the first rational point here; the de Klerk--Vallentin theorem described in the source is not a substitute. This is the principal external theorem contract still to pin to an exact authoritative statement through Luna.

A returned tuple can be checked without verifying the optimization promise. Rational PSD Grams and the exact polynomial identity already constitute a complete certificate. Optional rational `LDL^T` yields weighted rational squares. A positive rational weight `a/b` can be decomposed as `ab/b^2`; its binary integer expansion uses at most twice its bit length many integer squares by expressing an odd power of two as two equal squares. Thus unweighted rational-square output can also have polynomial total encoding length without integer factorization. This optional output conversion is not needed in the main theorem.

### 7.6 Unified box certificate theorem at the two hierarchy rates

The rational theorem should cover either finite cone rather than leading with only the preordering. For `T` equal to the full sparse box preordering or `Q` equal to the ordinary sparse box module, let `D_C` denote the sum of its Gram block sizes and use the full monomial bases for that cone. Let `E_C` be a proved rational upper bound on its finite-order primal gap, and suppose

\[
 f^*-\gamma\ge E_C+\tau,\qquad\gamma\in\mathbb Q,\quad
 \tau\in\mathbb Q_{>0}.
\]

For the box-only hierarchies, finite-SDP dual attainment gives real membership of `f-gamma-tau` in that same cone. The interior identity, moment outer bound, and coefficient right inverse then give rational Grams representing `f-gamma` exactly, with every block at least `tau/(2D_C)` positive definite. Witness bit length and the strong-feasibility construction complexity are polynomial in that cone's expanded dimensions, rational data length, and `log^+(1/tau)`.

For the preordering use the already rational explicit budget

\[
 E_T={3A_f\over2(\lfloor r/w\rfloor+1)^2+1}.
\]

For the ordinary exact-consistency transfer a simple rational majorant avoids putting an irrational square root into the input promise. Set

\[
 \eta_{\rm rat}={N+1\over C_s}
   \left({d_\infty^2\over s^2}+{3d_\infty^2\over2s}\right)
   +2(D+1)\delta,
\]

so `eta_rat>=eta`, because `sqrt(2(D+1))<=2(D+1)`. Then take

\[
 E_Q=C_f\bigl((1+\eta_{\rm rat})^w-1+2\Delta_w\bigr).
\]

Every quantity is rational for rational polynomial data and integer parameters. Under the chosen width-dependent `N=Theta_w(log s)`, `delta=O(s^{-3})`, and `D=Theta_w(s log s)`, the replacement term `2(D+1)delta` is `O_w(log(s)/s^2)`. Thus this rational majorant retains the ordinary `C_f O_{w,d_infty}(log^3 R/R^2)` rate. An even tighter rational majorant using an integer upper bound on the square root is possible but unnecessary. The expression may be enlarged by any certified rational bound without affecting the membership logic. All-constant or all-discrete models can be handled separately; no division by width is needed in those cases.

This unified theorem makes the ordinary module conclusion direct. Its smaller block family changes the expanded dimensions and improves the per-column expansion count; it does not require a full-preordering certificate as an intermediate step. The membership promise must use the error theorem for the cone actually chosen.

## 8. External theorem contracts to route to Luna

No literature search was performed by this reviewer. The following exact source contracts should be obtained through the designated literature agent:

- **Even-degree univariate interval SOS.** If a real univariate polynomial of degree at most `2t` is nonnegative on `[-1,1]`, it has the form `sigma_0+(1-x^2)sigma_1`, with SOS terms satisfying `deg sigma_0<=2t` and `deg((1-x^2)sigma_1)<=2t`. Nonstrict positivity and vanishing endpoint or interior values must be permitted. Only the even-degree version is needed; the odd-degree representation should not be imported with the same generator without checking its degree convention.
- **Finite-SDP primal Slater.** A feasible point strictly inside every retained PSD cone, subject to affine equality constraints, and a finite primal optimum imply zero gap and attained dual optimum. Redundant equality rows do not defeat this statement. Apply it to the box-only cones and to the pruned finite-state cones; do not apply it merely because a constrained global error bound exists.
- **Rational strong feasibility.** A rational separation oracle of polynomial bit complexity, a known rational enclosing radius, and a known positive rational radius of some contained full-dimensional ball give polynomial-time rational feasibility with polynomial query/output bit length. The inner center is unknown; a supplied rational feasible start is not assumed. The proof needs the rounded rational ellipsoid implementation, not only the real-volume iteration estimate.
- **Standard-Borel disintegration and tree gluing.** Finite products of finite spaces and compact intervals admit regular conditional laws. Exactly consistent bag measures on a finite running-intersection tree admit a global law; null separators permit arbitrary conditional choices without changing marginals. The paper can give the short leaf-extension proof while citing the existence of conditional laws.
- **Optional geometric context.** If retained, Hoffman bounds and semialgebraic Hölder bounds need statements matching a global bound to a nonempty compact feasible intersection and the supplied residuals. The paper's actual concave common-Slater regime is proved directly and does not depend on these optional claims.

## 9. Recommended manuscript placement

The main constrained section should state the global bound prominently, give both hierarchy rates, and explain that they are primal guarantees. Include the explicit common-Slater example and the local-versus-global counterexample. The transport proof's divided-difference certificate is mathematically central; supply it in the main proof or a fully referenced proof appendix. The exact-consistency constrained option in Section 4 is preferable if the writer wants the main mechanism reused consistently, but it is not necessary to claim a stronger rate.

The finite-state extension is coherent enough for one main section: exact separator label sums, common continuous box, the preordering inverse-square rate, and the ordinary `log^3/R^2` coefficient-normalized rate. Put the detailed mass-scaled residual and pruning proofs in an appendix if length demands it. Promote the new ordinary theorem only after the independent fresh review requested by root. State all-discrete exactness and zero-mass handling in the theorem itself rather than hiding them in a footnote.

The rational result merits a short main certificate theorem with its membership/slack assumption, exact coefficient matching, expanded-size interpretation, and `tau/(2D)` margin. The diagonal interior certificate, explicit uniform moment determinant bound, right inverse, and rational ellipsoid reduction belong in a proof appendix. If the authoritative ellipsoid theorem contract cannot be pinned down, retain the independently proved polynomial-bit rational witness theorem and the exact-checkable rounding/correction rule; remove only the unconditional theoretical polynomial-time *construction* sentence. This does not affect the quantitative hierarchy results.

Do not merge the rational theorem with the constrained theorem or the labelled dual without a separate proof for those different cones. No efficient numerical extraction, numerical error certification, general MINLP runtime, practical speedup, or novelty of standard finite-state gluing and rational SOS recovery follows from this audit.

## 10. Verification record

This audit reconstructed the displayed symbolic identities, degree ledgers, measure normalization, label-fiber corrections, coefficient pivots, and bit-bound dependencies directly from the source proofs. It did not rerun any experiment or checker. Source notes' historical numerical and exact-arithmetic checks were treated as records, not as new verification by this reviewer. Source investigation used targeted file listings, `rg` searches, and `cat`/`sed` reads. The only file written was this report. Final document checks actually run were `wc -l -w paper-sparse-sos/evidence/AUDIT-EXTENSIONS.md` (649 lines, 5,928 words before this verification-record clarification) and `rg -n '7.6|eta_\{|ordinary-module finite|No fatal|Verification record' paper-sparse-sos/evidence/AUDIT-EXTENSIONS.md` (all requested theorem and record markers found). These were document checks, not mathematical tests or CI checks. No project-wide verification, CI inspection, source-note edit, commit, external message, or literature search was performed. The optional ordinary finite-state completion has a full proof here but awaits the independently assigned fresh reviewer before promotion.
