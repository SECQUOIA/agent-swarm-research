# Recourse theory audit

Date: 2026-10-05. Scope: fixed private polytopes, affine private recourse, the inverse-order boundary example, and regular projected multiplier rates. This audit independently reconstructs the mathematical arguments from the supplied source notes and their reviews. It does not determine literature priority, rerun experiments, or claim formal verification.

The stated recourse results pass the mathematical audit. No fatal error was found. The principal safeguards are the rectangular degree convention, redundant private quadratic bounds, the one-degree kernel reserve for affine recourse, complete recourse with a fixed constraint matrix, and the stronger half-degree certificate for the multiplier commutator. A new order-unit argument below fills a useful omission: the sparse rectangular moment and certificate values agree, and every strict suboptimal certificate level is attained. Boundary certificate attainment is not established.

## Findings and severity

| Severity | Finding | Required manuscript treatment |
| --- | --- | --- |
| Critical if omitted; correct in sources | Private affine localizers do not bound second moments. Without the quadratic bounds, even a nonnegative, private-convex quadratic objective can give an all-order relaxation value of minus infinity. | Include the quadratic bounds in the hierarchy, not merely in a proof sketch. |
| Critical if conflated; correct in sources | The private-degree-two rectangular hierarchy differs from the total-degree full-preordering hierarchy used in the inverse-order example. | Define both. Transfer lower bounds through actual local measures; do not compare the finite cones without a proof. |
| Critical if extended; correct in sources | Arbitrary multivariate Lipschitz projected multipliers are not covered by the regularity theorem. | State weighted absolute tensor Chebyshev coefficients or coordinatewise Hölder/Lipschitz dependence. |
| Major proof boundary; already repaired in sources | Commutator frequencies can exceed total shared degree `r`. The bound `|L(T_alpha)| <= 1` for `|alpha| <= r` is insufficient. | Retain the lemma with `sum_i ceil(alpha_i/2) <= r` and its certificate proof. |
| Major proof boundary; correct in sources | Without a degree reserve, source means or source second moments of a full-order kernel may exceed the functional's domain or localizer allowances. | Use `m = ceil(r/s)` for affine recourse, with `r >= max(s+1,d)`. |
| Major theorem boundary; correct in sources | Complete recourse alone does not make fibers Hausdorff continuous if the private constraint matrix depends on shared variables. | Keep the fixed-matrix hypothesis. Do not extend the Hoffman argument to bilinear rows. |
| Major interpretive omission; repaired here | Primal rounding does not by itself imply a dual certificate bound. The source notes deliberately avoid strong-duality claims. | Use the order-unit proof in Section 7 if the manuscript states equality of moment/certificate values or certificate existence with slack. Do not infer boundary attainment. |
| Major if strengthened; correct in sources | Strict private convexity and Lipschitz primal solutions do not imply continuous projected multipliers. | Keep an explicit dual regularity hypothesis; qualify any QP sensitivity corollary by LICQ and a closed-domain boundary hypothesis. |
| Moderate | SDP dimensions have a shared-width exponent, but rate constants can grow with private dimension, objective degree, row count, and conditioning. | State finite SDP dimensions and fixed-data rates separately from accuracy complexity or numerical runtime. |
| Moderate | A feasible moment objective is not automatically a certified lower bound. | Distinguish the moment optimum, an arbitrary feasible moment value, and a feasible dual certificate. |

Exact source locators for these findings are given in the sections below. There is no reason to stop the paper on mathematical grounds within this scope.

## 1. Exact hierarchy and coefficient contract

Source: `research-20260928/solver/partial-kernel-rounding.md`, lines 39–146; `affine-recourse-kernel-upper.md`, lines 31–139; `active-region-rates.md`, lines 36–89. The degree and size counts are independently checked in `partial-kernel-fresh-review.md`, lines 15–61, and `affine-recourse-upper-review.md`, lines 62–86 and 326–330.

Let a finite tree index shared bags `S_b` satisfying running intersection and covering all shared variables. Each bag owns a disjoint private vector `y_b in R^{p_b}`. Write `k_b = |S_b|` and `s = max(1,max_b k_b)`. Shared variables range over their entire box. Private decisions are continuous. A private variable occurring in more than one bag is outside these statements.

The local domain is

\[
 V_{b,r}=\mathbb R[u_{S_b}]_{\le 2r}\otimes
                 \mathbb R[y_b]_{\le 2}.
\]

Both degree bounds are total degrees within their respective variable groups. They are not a bound on the sum of shared and private degrees. In particular, `u^alpha y_i y_j` with `|alpha| = 2r` belongs to the domain. This distinction controls the SDP size and must appear before the positivity constraints.

Put `z=(1,y^T)^T`, `w_I(u)=prod_{i in I}(1-u_i^2)`, and impose the following local conditions:

\[
 L_b\bigl(w_I[q_0(u)+q(u)^Ty]^2\bigr)\ge0,
       \qquad \deg q_i\le r-|I|,
\tag{H1}
\]

\[
 L_b\bigl(w_Iq(u)^2(1-y_j^2)\bigr)\ge0,
       \qquad \deg q\le r-|I|.
\tag{H2}
\]

For a fixed private polytope described by affine inequalities `g_j(y) >= 0`, add

\[
 L_b(w_Iq^2g_j)\ge0,\qquad \deg q\le r-|I|.
\tag{H3-fixed}
\]

For affine recourse

\[
 P_b(u)=\{y\in[-1,1]^{p_b}: A_by\le a_b+B_bu\},
\]

add instead

\[
 L_b\bigl(w_Iq^2[a_b+B_bu-A_by]_j\bigr)\ge0,
        \qquad \deg q\le r-|I|-1.
\tag{H3-affine}
\]

Negative allowances mean absent constraints. The last allowance is conservative and correct: its displayed polynomial has shared degree at most `2r-1` and private degree at most one. A row with no shared dependence can use the larger fixed-domain allowance. This is optional strengthening; the source affine theorem does not need it.

Normalize `L_b(1)=1` and equate adjacent functionals on separator polynomials of shared total degree at most `2r`. All `2^{k_b}` shared box products are present. This is a full shared-box preordering with private matrix-square and scalar localizers, not a full preordering in all joint generators. Arbitrary products of private recourse inequalities are not imposed.

The objective is

\[
 f_b(u,y)=c_b(u)+q_b(u)^Ty+y^TQ_b(u)y=z^TH_b(u)z,
\qquad
 H_b=\begin{pmatrix}c_b&q_b^T/2\\q_b/2&Q_b\end{pmatrix}.
\]

Require polynomial shared coefficients, symmetric `Q_b`, and `Q_b(u) >= 0` on the entire shared box. Neither `H_b >= 0` nor a matrix-SOS representation of `Q_b` is required. Write

\[
 H_b(u)=\sum_\alpha H_{b\alpha}T_\alpha(u),\qquad
 d=\max\{|\alpha|:H_{b\alpha}\ne0\},\qquad
 \mathcal A=\sum_{b,\alpha}\|H_{b\alpha}\|_{1,\mathrm{entry}}
                                     \sum_i\alpha_i^2.
\]

Set `d=0` for the zero objective. The matrix entry norm counts both off-diagonal entries; the linear coefficients are consequently counted once and the ordered quadratic entries once each. The rate proofs use `d <= r`, not merely objective membership `d <= 2r`.

For `(H1)`, the PSD block has `(p_b+1) binom(r-|I|+k_b,k_b)` rows. The `(H2)` and fixed affine scalar localizers have `binom(r-|I|+k_b,k_b)` rows; affine-recourse localizers have `binom(r-|I|-1+k_b,k_b)` rows. The rectangular domain has

\[
 \binom{p_b+2}{2}\binom{2r+k_b}{k_b}
\]

monomials. At fixed shared width, these are polynomial dimension bounds in private dimension, row count, and order, with order exponents determined by shared width. They do not imply dimension-independent accuracy constants or solver runtime.

## 2. Conditional means and matrix Jensen without measures

Sources: `partial-kernel-rounding.md`, lines 170–281; `affine-recourse-kernel-upper.md`, lines 183–245 and 330–372; `partial-kernel-proof-review.md`, lines 67–124; `active-region-fresh-review.md`, lines 79–91.

The kernel input is the normalized positive squared-Fejer kernel from `sparse-kernel-rounding.md`, lines 119–207. Its multipliers satisfy `g_0=1`, `0 <= g_j <= 1`, `g_j=0` above `2m-2`, and

\[
 1-g_j\le \frac{3j^2}{2m^2+1}.
\]

For fixed output `v`, the tensor kernel `K_b(u,v)` has a shared preordering certificate with square degree at most `k_b(m-1)-|I|`. This certificate, not pointwise kernel positivity alone, permits application of a truncated functional.

For fixed private feasibility choose `r >= max(s,d)` and `m=floor(r/s)+1`. Applying `(H1)` to the kernel certificate and arbitrary constant affine private forms proves

\[
 M(v)=L(K_bzz^T)=\begin{pmatrix}h&\ell^T\\\ell&Y\end{pmatrix}\succeq0.
\]

Applying `(H2)` gives `0 <= Y_jj <= h`. Thus `h=0` implies `M=0`, by the PSD two-by-two minors. On `h>0`, the mean `ybar=ell/h` satisfies every affine fixed-private inequality. On `h=0`, choose a fixed point of the polytope. The resulting map is Borel. Normalization gives `int h dmu^{S_b}=1`.

For affine recourse choose `r >= max(s+1,d)` and

\[
 m=\lfloor(r-1)/s\rfloor+1=\lceil r/s\rceil\ge2.
\]

Then the kernel squares have degree at most `r-1-|I|`. Multiplying them by the square of an affine form in `(u,y)` is permitted by `(H1)`, so the conditional matrix on `(1,u,y)` is PSD. Its source shared diagonals satisfy

\[
 0\le L(K_bu_i^2)\le h.
\]

The upper bound is a genuine certificate calculation. To multiply a kernel term `w_I p^2` by `1-u_i^2`, add `i` to `I` if absent. If present, remove `i` from `I` and replace the square polynomial by `(1-u_i^2)p`. Its degree increases by two while the allowed degree increases by one; the one-degree reserve supplies the remaining degree. This verifies the allowance even for repeated generators.

Consequently `ubar=L(K_bu)/h` belongs to the shared box and `ybar` belongs to the private box. Applying `(H3-affine)` to the kernel certificate gives

\[
 a_b+B_b\overline u-A_b\overline y\ge0.
\]

Thus `ybar in P_b(ubar)`, not necessarily `P_b(v)`. At `h=0`, all shared and private diagonals and therefore all entries of the augmented conditional matrix vanish. Means can be set to zero there for algebraic expressions; feasible output decisions are assigned separately.

The private Schur complement gives `Y/h-ybar ybar^T >= 0`. Since `Q_b(v) >= 0`,

\[
 h(v)f_b(v,\overline y(v))\le \langle H_b(v),M_b(v)\rangle.
\tag{J}
\]

No feasibility of `ybar` at `v` is needed for this inequality. At `h=0`, both sides are zero. This argument uses only PSD matrices; it never treats the input functional as a measure.

For `|alpha| <= r`, the Chebyshev identity `1-T_n^2=(1-u^2)U_{n-1}^2`, tensor telescoping, `(H2)`, and Cauchy–Schwarz in `(H1)` yield

\[
 |L(T_\alpha z_i z_j)|\le1.
\]

Integrating the right side of `(J)` damps each coefficient by `prod_i g_{alpha_i}`. Therefore

\[
 \int\langle H_b(v),M_b(v)\rangle\,d\mu^{S_b}(v)
 \le L_b(f_b)+\frac3{2m^2+1}
      \sum_\alpha\|H_{b\alpha}\|_{1,\mathrm{entry}}\sum_i\alpha_i^2.
\tag{C}
\]

This remains valid for objective frequencies above the kernel support: their multiplier and output integral are zero, while the relevant input moments are bounded because `d <= r`.

Integrating out nonseparator coordinates removes normalized kernel factors. The remaining separator kernel has total input degree at most `2r`; exact moment consistency therefore gives equality of complete output separator distributions. A finite junction tree glues these scalar shared laws. Private decisions are then measurable functions of their own shared bags. There is no matrix-valued marginal gluing and no private cross-bag moment agreement.

The fixed-domain conclusion is

\[
 0\le f^*-\rho_r\le \frac{3\mathcal A}{2m^2+1}
       \le \frac{3s^2\mathcal A}{2r^2}.
\]

The rounding comparison is one-sided. Jensen can improve the private objective strictly. The theorem does not bound the absolute difference between the original moment cost and rounded cost.

## 3. Hoffman repair, complete recourse, and the inverse-order bound

Sources: `affine-recourse-kernel-upper.md`, lines 71–97, 246–328, and 417–437; `affine-recourse-upper-review.md`, lines 178–261. The claims are valid including paired inequalities, singular private Hessians, and lower-dimensional fibers.

Stack `C_b=[A_b;I;-I]`. A fixed-matrix Euclidean Hoffman constant `h_b^H` satisfies

\[
 \operatorname{dist}(y,\{z:C_bz\le e\})
   \le h_b^H\|(C_by-e)_+\|_2
\]

for all consistent right-hand sides. Complete recourse is exactly what makes the output right-hand side consistent at every `v` in the shared box. At the source-feasible conditional mean, the box residuals vanish and

\[
 (A_b\overline y-a_b-B_bv)_+
       \le [B_b(\overline u-v)]_+.
\]

The Euclidean projection `yhat=proj_{P_b(v)} ybar` hence satisfies

\[
 \|\widehat y-\overline y\|_2
       \le h_b^H\|B_b\|_2\|\overline u-v\|_2.
\tag{R}
\]

No Slater condition or common interior feasible point is used. Applying the same bound to all points of two fibers in both directions proves

\[
 d_H(P_b(v),P_b(w))\le h_b^H\|B_b\|_2\|v-w\|_2.
\]

Compactness and uniqueness of Euclidean projection then prove joint continuity of `(v,z) -> proj_{P_b(v)} z`: any subsequential projection limit is feasible, and Hausdorff approximation of each comparison point preserves the projection-minimality inequality. On `{h=0}`, use `proj_{P_b(v)}0`. This makes the repaired decision Borel and feasible everywhere.

For `D_m=2m^2+1`, `a_0=mD_m/3`, and

\[
 V_m=\frac{3(4m-3)}{2mD_m}<\frac6{D_m},
\]

conditional Cauchy–Schwarz gives

\[
 h\|\overline u-v\|_2^2
      \le\sum_i L(K_b(u,v)(u_i-v_i)^2).
\]

Normalization and the identities `1-g_1=m/a_0`, `1-g_2=(4m-3)/a_0` give exactly

\[
 \int L(K_b(u,v)(u_i-v_i)^2)\,d\mu^{S_b}(v)
     =V_m+\frac{3-2m}{a_0}L(u_i^2)\le V_m.
\]

The sign of the second coefficient uses `m >= 2`. Thus the expected source/output movement is at most `sqrt(k_b V_m)` under the positive shared law. Evaluation at source zero attains the intermediate square-displacement bound; this fact alone says nothing about sharpness of the objective gap.

Let

\[
 \Lambda_b=\max_{u,y\text{ in boxes}}\|q_b(u)+2Q_b(u)y\|_2,
\quad \Gamma_b=\Lambda_bh_b^H\|B_b\|_2,
\quad \mathcal R=\sum_b\Gamma_b\sqrt{k_b}.
\]

Both the conditional mean and its repair lie in the private box, so the segment between them stays there. The private gradient bound, `(R)`, `(J)`, and `(C)` prove

\[
 0\le f^*-\rho_r\le \frac{3\mathcal A}{D_m}+sqrt{V_m}\mathcal R
       \le \frac{3s^2\mathcal A}{2r^2}+
                        \frac{\sqrt3s\mathcal R}{r}.
\]

This is `O(1/r)` for fixed data. When all `B_b=0`, the repair contribution vanishes; the reserve can then be removed using the fixed-domain theorem.

Complete recourse is not a substitute for fixed coefficients in the private variables. The source counterexample `P(u)={y in [-1,1]:uy=0}` has complete recourse but jumps from the whole interval at zero to a singleton elsewhere. Its fibers are not Hausdorff continuous. Jointly affine rows, not merely nonempty fibers, are used both when taking conditional means and when applying a uniform Hoffman bound.

## 4. Inverse-order sharpness and the hierarchy distinction

Sources: `affine-recourse-rate-boundary.md`, lines 28–193, 195–283, and 287–330; `affine-recourse-proof-review.md`, lines 22–74 and 99–173. The latter verifies the corrected factor-two certificate constant.

The problem

\[
 \min_{-1\le x,u\le1,\ 0\le z\le1,\ z\ge\pm u} -xu+z
\]

has bags `(x,u)` and `(u,z)`, local values `-|u|` and `|u|`, and minimum zero. Its total-degree hierarchy uses the full local generator lists `(1-x^2,1-u^2)` and `(1-u^2,z,1-z,z-u,z+u)` and degree at most `2r` in all bag variables together. This is a distinct hierarchy from Section 1.

For any continuous separator function `h`, the greatest difference of its expectations between probability laws matching polynomials through degree `n` equals `2 E_n(h)`, where `E_n` is best uniform polynomial approximation error. The proof requires the factor two: Hahn–Banach and Riesz give a norm-one signed annihilating measure with total mass zero, and its Jordan parts have mass one half. Doubling them gives the two probability laws. For `h=|u|`, lifting the first law to `x=sign(u)` and the second to `z=|u|` gives the ideal local-measure value `-2E_n(|u|)`.

The supplied Fejer witness has frequencies between `N+1` and `3N-1`, with `N` the even integer in `[n+1,n+2]`. It annihilates all polynomial frequencies through `n`, has integral absolute value at most one, and has positive absolute-value correlation at least `1/(9 pi N)`. The even-frequency triangular weights sum to `N/2`. Thus

\[
 E_n(|u|)\ge\frac1{9\pi(n+2)},\qquad
 -\rho_r\ge\frac1{9\pi(r+1)}.
\]

The total-degree certificate upper bound is independently valid. Let `s_m=K_m(sign)`, `delta_m=2 sqrt(6/D_m)`, and `p_m=u s_m+delta_m`. Then `s_m` is odd, of degree at most `2m-3`, `|s_m| <= 1`, and `p_m >= |u|`. The exact decomposition is

\[
 f+\delta_m=(p_m-xu)+(z-u s_m).
\]

Interval certificates for `p_m +/- u` combined with `(1 +/- x)/2=(1 +/- x)^2/4+(1-x^2)/4` put the first term in the first local preordering at degree `2m`. Interval certificates for `(1 +/- s_m)/2` combined with

\[
 z-u s_m=\tfrac12(1+s_m)(z-u)+\tfrac12(1-s_m)(z+u)
\]

put the second term in the second local preordering at degree `2m-1`. Full products `(1-u^2)(z +/- u)` are used. With `m=r`,

\[
 \frac1{9\pi(r+1)}\le-\rho_r\le-\lambda_r
       \le\frac{2\sqrt6}{\sqrt{2r^2+1}}.
\]

No second additive `delta_m` is needed. Both the moment and certificate gaps have exact order `1/r` in this total-degree hierarchy.

For the rectangular hierarchy, take `u` shared and `x,z` private. Rescale `z=(1+zeta)/2` to the model's private box and add the valid quadratic bounds. The same actual local measures satisfy every rectangular positivity constraint and match all required separator moments through `2r`. Therefore the same lower bound transfers. Section 3 supplies the matching inverse-order upper bound. This proves sharpness for the stated rectangular hierarchy without asserting equality between its finite cone and the total-degree cone.

The merged-bag dense identity has degree three, and splitting at `u=0` also gives degree-three exact branch certificates. These facts confirm that the example is an obstruction to the fixed sparse representation and finite polynomial separator communication. It is not a hardness theorem for optimizing the underlying problem.

## 5. Projected multipliers and the inverse-square repair

Sources: `active-region-rates.md`, lines 92–191 and 193–401; `active-region-fresh-review.md`, lines 17–108. The theorem leaves the hierarchy unchanged.

Stack the constraints as `Cy <= e+Du`, including box rows with zero rows in `D`. For each parameter choose an optimal point `y*(u)` and a KKT multiplier `lambda(u) >= 0` satisfying stationarity and complementarity. Pointwise existence follows from the normal cone of a nonempty polyhedron and convex differentiable optimality, including degenerate or lower-dimensional fibers. No constraint qualification is needed merely for this existence statement.

The substantive assumption concerns the projection

\[
 a(u)=D^T\lambda(u),
\]

not the full multiplier vector. The proof integrates only a bounded regular projection. It neither assumes nor needs a measurable or bounded full-multiplier selection.

At any output `v`, direct quadratic expansion gives the identity

\[
 f(v,y)-F(v)-\lambda(v)^T[e+Dv-Cy]
     =(y-y^*(v))^TQ(v)(y-y^*(v)).
\]

Source feasibility and matrix Jensen consequently imply

\[
 h(v)F(v)\le\langle H(v),M(v)\rangle
                   +a(v)^T[U(v)-v h(v)].
\tag{K}
\]

The sign is positive for `a^T(U-vh)`. The zero-density case follows from the augmented conditional matrix vanishing. Define the smoothing operator `K a(x)=int K_b(x,v)a(v)dmu(v)`. Integrating the correction gives `L(R)` with

\[
 R(x)=\sum_i\{x_i\mathcal K(a_i)(x)-\mathcal K(v_i a_i)(x)\}.
\tag{R-comm}
\]

Although `a` need not be polynomial, `R` is a polynomial. It has individual degree at most `2m-2`, except for at most one coordinate of degree `2m-1`. Its total degree is at most `2k_b(m-1)+1 <= 2r-1`. This membership alone does not authorize bounding `L(R)` by a pointwise bound in several variables; positivity must be checked inside the truncated cone.

### 5.1. The stronger Chebyshev certificate

For every multi-index with `sum_i ceil(alpha_i/2) <= r`,

\[
 |L(T_\alpha)|\le1.
\tag{B}
\]

Here is a fully explicit proof of the univariate certificate input, avoiding an unexplained odd-degree degree loss. For `q >= 1`,

\[
 1+T_{2q}=2T_q^2,\qquad
 1-T_{2q}=2(1-x^2)U_{q-1}^2.
\]

For `q >= 0`, with `U_{-1}=0`,

\[
 1+T_{2q+1}=(1+x)(U_q-U_{q-1})^2,
\quad
 1-T_{2q+1}=(1-x)(U_q+U_{q-1})^2.
\]

Substitute `1 +/- x=((1 +/- x)^2+(1-x^2))/2`. Thus `1 +/- T_n` has a box-preordering certificate of degree at most `2 ceil(n/2)`. Constant indices are immediate.

For `z_i=T_{alpha_i}`, the parity identity

\[
 1+\epsilon\prod_{i=1}^kz_i
 =2^{1-k}\sum_{\substack{\eta\in\{-1,1\}^k\\\prod_i\eta_i=\epsilon}}
                        \prod_i(1+\eta_i z_i)
\]

then gives certificates for `1 +/- T_alpha`, of degree at most `2 sum_i ceil(alpha_i/2)`. Products remain in the full preordering since these are different coordinate generators. Applying `L` proves `(B)`. Every frequency of `(R-comm)` obeys the bound because `sum_i ceil(alpha_i/2) <= k_b(m-1)+1 <= r`.

### 5.2. Weighted tensor coefficients, including support-boundary modes

Assume

\[
 a_{bi}(u)=\sum_\alpha a_{bi\alpha}T_\alpha(u),\qquad
 \mathcal M=\sum_{b,i,\alpha}|a_{bi\alpha}|\max(1,2\alpha_i)<\infty.
\]

The weight is directional: it concerns the coordinate multiplying the corresponding component of the projection. Since it is at least one, it also gives absolute uniform convergence on the box.

The circle-kernel identity gives, for every `j >= 0`, including indices outside support,

\[
 |g_{j+1}-g_j|\le(2j+1)(1-g_1)=\frac{3(2j+1)}{D_m}.
\]

This follows by integrating `cos(j theta)-cos((j+1)theta)` and using `|sin((2j+1)theta/2)| <= (2j+1)|sin(theta/2)|` against the nonnegative circle kernel.

For a tensor coefficient with directional index `k >= 1`, the corresponding one-dimensional commutator is

\[
 \tfrac12(g_k-g_{k+1})T_{k+1}
       +\tfrac12(g_k-g_{k-1})T_{k-1},
\]

multiplied by `prod_{j != i} g_{alpha_j}`. Its absolute coefficient sum is at most `2k(1-g_1)`. At `k=0`, the expression is `(1-g_1)T_1`. When `k=2m-1`, the original multiplier is outside support, but the adjacent `g_{k-1}` term can still survive. It must be included. Frequencies farther outside support vanish; an out-of-range index in any other coordinate also kills the term. These facts justify the finite frequency support and prevent silently dropping support-boundary terms.

Apply `(B)`, absolute convergence, and the directional coefficient bound to obtain `|L(R)| <= 3 mathcal M/D_m`. Together with `(C)` and `(K)`,

\[
 0\le f^*-\rho_r\le \frac{3(\mathcal A+\mathcal M)}{D_m}
       \le\frac{3s^2(\mathcal A+\mathcal M)}{2r^2}.
\]

### 5.3. Coordinatewise Hölder or Lipschitz projections

Alternatively assume `a_{bi}(u)=phi_{bi}(u_i)`, `||phi_{bi}||_infty <= M_{bi}`, and

\[
 |\phi_{bi}(v)-\phi_{bi}(w)|\le H_{bi}|v-w|^\beta,
                  \qquad 0<\beta\le1.
\]

Normalization removes the other coordinates from `(R-comm)`, so `R=sum_i R_i(x_i)` with `deg R_i <= 2m-1`. Adding and subtracting `phi_i(x)` and using the pointwise kernel displacement bound give

\[
 R_i(x)\le\frac{3M_i}{D_m}+H_iV_m^{(1+\beta)/2}=:\epsilon_i.
\]

Indeed the remainder has absolute value at most `H_i int K_m(x,v)|x-v|^{1+beta}dmu(v)`, bounded by `H_i V_m^{(1+beta)/2}` using concavity and kernel normalization. Now `epsilon_i-R_i` is a nonnegative univariate polynomial of degree at most `2m-1`. The interval certificate requires at most degree `2m <= 2r`, and embeds in the shared scalar constraints. Therefore `L(R_i) <= epsilon_i`. This last certificate is why the estimate holds for pseudomoments without a representing measure.

The gap is consequently bounded by

\[
 \frac{3\mathcal A}{D_m}
    +\sum_{b,i}\left(\frac{3M_{bi}}{D_m}
                      +H_{bi}V_m^{(1+\beta)/2}\right).
\]

Lipschitz projections give `O(r^-2)`; exponent `beta` gives `O(r^{-(1+beta)})`. No sharpness is established for intermediate exponents. Coordinatewise dependence is automatic for scalar bags but is a substantive hypothesis for multivariate bags. Arbitrary coupled polynomial master terms are still allowed.

### 5.4. Optimal selection and regular sharpness

The optimal private policy used to realize `F_b` need not be the pointwise optimizer originally used to exhibit regular projected multipliers. A Borel choice follows directly from Hoffman continuity: the unique minimizer of `f_b(u,y)+epsilon ||y||^2` is continuous on the shared box by compactness, fiber Hausdorff continuity, and strict convexity. As `epsilon` decreases to zero it converges to the minimum-norm optimizer. To check the last statement, compare with any optimizer `z`: optimality gives `f(y_epsilon) <= F+epsilon ||z||^2` and `||y_epsilon|| <= ||z||`. Every cluster point is optimal with minimal norm; uniqueness of that point forces convergence. The pointwise limit of continuous policies is Borel. Gluing the shared laws and assigning these policies realizes the integrated bound.

The regular sharp example is `x,z in [0,1]`, `z >= u`, and `f=x^2-2ux+z^2`, with shared `u`. Its local values are `-u_+^2` and `u_+^2`. The second bag admits multiplier `2u_+` on `u-z <= 0`, so its projection is `-2u_+`; the first bag has zero projection. After private affine scaling, `mathcal A=2`, `M=2`, and `H=2`. Thus

\[
 -\rho_r\le \frac{12}{2r^2+1}+2V_r<\frac{12}{r^2}.
\]

The actual separator measures constructed in `quadratic-sharpness.md`, lines 142–174, can be relifted with `x=u_+`, `z=u_+` on the new fibers. Their moment agreement through `2r` and expectation difference for `h=u_+^2` give

\[
 -\rho_r\ge\frac2{27\pi(2r+2)^2}.
\]

The original second-bag lift in `quadratic-sharpness.md` is `z=(-u)_+`; it must be changed to `z=u_+` for this new recourse problem. The transferable objects are the separator laws and their `h`-expectation difference. The source regular-rate note makes the new lift correctly at lines 460–473. Hence the regular rectangular example has exact order `r^-2`.

## 6. Classical sensitivity: a qualified sufficient route

Sources: `active-region-rates.md`, lines 403–425 and 477–492; supplied `active-region-prior.md`, lines 17–84 and 101–139. No new literature research was conducted for this audit.

A safe sensitivity corollary assumes a constant positive-definite private Hessian, affine private linear objective coefficients, fixed linear constraint matrix, affine right-hand side, and feasibility on an open neighborhood of the closed shared box. Assume LICQ at the optimal point throughout that neighborhood, including all active box rows. Then primal and multiplier policies are continuous piecewise affine on the box, and the multiplier projection is Lipschitz there. Strict complementarity is not needed for this statement.

The algebra behind this sufficient route is transparent. For an active independent row set `I`, solve the nonsingular KKT system

\[
 \begin{pmatrix}2Q&C_I^T\\ C_I&0\end{pmatrix}
 \begin{pmatrix}y\lambda_I\end{pmatrix}
 =\begin{pmatrix}-q(u)\\e_I+D_Iu\end{pmatrix}.
\]

It gives affine policies. Primal feasibility and multiplier nonnegativity describe their polyhedral regions. There are finitely many row sets. Uniqueness of the primal solution and, under LICQ, of the multiplier makes the valid affine policies agree at their region boundaries. A continuous function formed from finitely many affine pieces is Lipschitz on a compact convex box: subdivide each line segment across its finitely many polyhedral pieces and bound by the largest affine slope. The open feasible neighborhood avoids relying on an interior sensitivity statement at an unqualified boundary.

This route gives the coordinatewise theorem for scalar bags. In several shared dimensions, Lipschitz continuity alone does not establish the weighted absolute Chebyshev condition, and an oblique active-region boundary does not imply coordinatewise dependence. Therefore no general multivariate QP corollary follows from these assumptions alone in the audited result.

Strict convexity alone is insufficient. In the source example

\[
 \min_{|u|\le z\le1}(z^2+z)=u^2+|u|,
\]

the optimizer `z=|u|` is Lipschitz and recourse is complete. Near zero, the projected multiplier is `-(2u+1)` for `u>0` and `1-2u` for `u<0`. Its one-sided limits are minus one and plus one. No value assigned at zero makes the projection continuous. This explicitly separates primal regularity, private strong convexity, and the dual regularity needed for the rate theorem.

## 7. Rigorous completion: order unit, sparse quotient, and dual certificates

This section is an additional proof, not a claim already made in the source notes. It repairs the certificate interpretation if the manuscript wants more than the sources' primal rounding theorem. The source caution appears in `partial-kernel-rounding.md`, lines 418–422, and `affine-recourse-kernel-upper.md`, lines 369–372.

Let `C_{b,r}` be the local polynomial cone generated by sums of the `(H1)`, `(H2)`, and applicable `(H3)` displayed polynomials. It has exactly the degrees specified in Section 1. Let

\[
 W_r=\sum_b V_{b,r}
\]

be their sum as subspaces of the global polynomial ring. Define the global sparse certificate cone

\[
 C_r=\sum_b C_{b,r}\subseteq W_r,
\qquad
 \lambda_r=\sup\{\lambda:f-\lambda\,1\in C_r\}.
\]

This definition uses global polynomial equality; it is not a direct-product cone without identification of overlapping coefficients.

### 7.1. Every local rectangular monomial is dominated by the constant

For a monomial `u^alpha z_i z_j` in `V_{b,r}`, split `alpha=beta+gamma` with `|beta|,|gamma| <= r`. Put `a=u^beta z_i`, `b=u^gamma z_j`. Such a split exists for every `|alpha| <= 2r`.

First `1-u^{2beta}` belongs to the scalar shared cone at order `r`: telescope the coordinate product and use

\[
 1-u_i^{2h}=(1-u_i^2)\sum_{ell=0}^{h-1}(u_i^{ell})^2.
\]

All weighted square degrees are at most `r-1`. If `i=0`, this proves `1-a^2 in C_{b,r}`. If `i>0`, use

\[
 1-a^2=(1-u^{2beta})+u^{2beta}(1-y_i^2),
\]

whose second term is `(H2)` with square polynomial `u^beta`. The same argument gives `1-b^2 in C_{b,r}`. Finally

\[
 1\pm ab=\tfrac12\{(1-a^2)+(1-b^2)+(a\pm b)^2\}\in C_{b,r}.
\tag{OU}
\]

The square `(a +/- b)^2` is allowed by `(H1)` with empty `I`: it is affine in the private vector and every shared coefficient has degree at most `r`. This proves `(OU)` for constants, private linear monomials, and private quadratic cross monomials as well as pure shared monomials. It needs no private affine localizer and no convexity assumption on the objective. The private square bounds are essential to this proof.

### 7.2. Correct global coefficient quotient

Consider the summation map from the direct sum of local polynomial spaces onto `W_r`. Its kernel is generated by adjacent separator differences: a polynomial on an edge separator placed in one endpoint and its negative placed in the other.

To prove this, work monomial by monomial. A monomial containing a private variable belongs to only its owning bag, so it creates no identification. For a shared monomial with support `J`, all bags containing `J` form a connected subtree. Indeed, running intersection makes the bags containing each coordinate connected; the intersection of these subtrees is connected when nonempty. All occurrences of that monomial can therefore be moved along edges of this subtree. On each such edge the monomial is a separator polynomial of degree at most `2r`. Any local coefficient vector with zero global sum is a combination of these edge differences. Constants obey the same argument on the entire tree.

Thus exactly consistent local moment functionals descend to a well-defined global linear functional `F` on `W_r`, and conversely a global functional restricts to exactly consistent local functionals. Local normalization becomes the single condition `F(1)=1`; local positivity becomes `F(C_r) >= 0`. There is no extra consistency condition involving private moments.

### 7.3. Interior order unit and compact primal feasible set

Choose a global monomial basis of `W_r`, assigning each monomial to one bag that contains it. By `(OU)`, `1 +/- e in C_r` for every basis monomial `e`, and `1 in C_r`. If `g=sum_e c_e e` and `sum_e |c_e| <= 1`, then

\[
 1+g=\left(1-\sum_e|c_e|\right)1
          +\sum_e|c_e|[1+\operatorname{sign}(c_e)e]\in C_r.
\]

Consequently `1` is in the interior of `C_r` in `W_r`; the coefficient `ell_1` ball around it is contained in the cone. No claim that `C_r` is closed is needed.

For any `F in C_r^*`, `(OU)` gives `|F(e)| <= F(1)` for every basis monomial. In particular, `F(1)=0` forces `F=0`. Normalized feasible moments have all basis coordinates in `[-1,1]`. They form a closed, bounded, nonempty finite-dimensional set: closedness follows from the positivity and equality constraints, and a feasible global point supplies a nonempty evaluation functional. Thus the moment optimum `rho_r` is finite and attained.

### 7.4. Equality of values and strict-slack attainment

Let `p=f-rho_r 1`. For every nonzero `F in C_r^*`, the preceding bound gives `F(1)>0`, so normalize and obtain

\[
 F(p)=F(1)\left(\frac{F(f)}{F(1)}-\rho_r\right)\ge0.
\]

The zero functional also has nonnegative value. Finite-dimensional separation, equivalently the bipolar theorem, gives `p in closure(C_r)`.

For any `epsilon>0`, `epsilon 1` is an interior point of `C_r`. Therefore `p+epsilon 1 in C_r`. Here is an elementary argument that avoids assuming closedness: choose `p_n in C_r` close enough to `p` that `epsilon 1+(p-p_n)` remains inside the coefficient ball around `epsilon 1` contained in `C_r`; add `p_n`. Hence

\[
 f-(\rho_r-\epsilon)1\in C_r\qquad\text{for every }\epsilon>0.
\]

Weak duality gives `lambda_r <= rho_r`, while these certificates give the reverse inequality for the supremum. Thus

\[
 \boxed{\lambda_r=\rho_r,\qquad
           f-\lambda 1\in C_r\ \text{for every }\lambda<\rho_r.}
\]

The primal optimum is attained. The dual supremum need not be attained at `lambda=rho_r` by this argument: only membership of `f-rho_r 1` in the cone closure has been shown. Lower-dimensional fibers do not invalidate this proof and do not create a hidden Slater assumption. Conversely, the proof does not assert closedness of the global sparse cone.

Each audited gap estimate `f*-rho_r <= E_r` therefore also bounds the dual supremum gap. An actual certificate is guaranteed at every level `f*-E_r-epsilon`, with arbitrary strict positive slack. This is an existence theorem over the real coefficients. It does not give an algorithm for finding the Gram matrices, a rational-size bound, or certificate attainment without slack.

## 8. Finite grids, constants, and theorem dependencies

Sources: `partial-kernel-rounding.md`, lines 351–400; `affine-recourse-kernel-upper.md`, lines 374–415; `partial-kernel-fresh-review.md`, lines 124–198; `affine-recourse-upper-verification.md`, lines 38–42.

For fixed-domain recourse, `N=m+floor(d_infty/2)` Gauss–Chebyshev nodes integrate the polynomial matrix surrogate, whose individual degree is at most `2m-2+d_infty`. For affine repair use `N=m+floor(max(d_infty,2)/2)`: the displacement polynomial has individual target degree up to `2m`, requiring `N >= m+1` even when the shared objective is constant or linear. The density masses and separator marginals normalize and match exactly under these quadratures. The private QP value function need not be a polynomial or smooth.

Local QP minimization improves the pointwise rounded cost. Once all `sum_b N^{k_b}` QP values exist, junction-tree dynamic programming needs `O(tN^s)` arithmetic/comparison operations. This excludes computing the QP tables, numerical solution/certification, and bit complexity. Direct smoothing of a true optimizer also gives related grid approximation bounds; the SDP theorem's additional content is comparison with every feasible moment collection and its corresponding lower relaxation.

The coefficient budget `mathcal A` sums over bags, so no additional bag-count multiplier is introduced by the proof. It can grow like the number of private quadratic entries and includes the squared shared frequencies. A crude private gradient bound is

\[
 \Lambda_b\le\sum_\alpha\|q_{b\alpha}\|_2+
                 2\sqrt{p_b}\sum_\alpha\|Q_{b\alpha}\|_2.
\]

Hoffman constants depend on the fixed constraint matrix, including its conditioning and dimension. Projected multiplier budgets `mathcal M`, `M_{bi}`, and `H_{bi}` can also grow with private dimension and problem data. Fixing shared width controls the SDP order exponent; it does not control these constants. To meet accuracy `epsilon`, the sufficient order is of inverse-square-root scale for the fixed/regular bounds and inverse scale for generic affine recourse only when the corresponding data budgets are held fixed.

The dependency contracts are:

| Result | Required ingredients | What is not concluded |
| --- | --- | --- |
| Fixed private-domain inverse-square rate | Running intersection; disjoint continuous private blocks; fixed nonempty compact private polytopes; rectangular private degree two; full shared preordering; private square bounds; `Q >= 0` on box; `r >= max(s,d)`; positive kernel | Shared-dependent feasibility, private integrality, generic nonconvex private cost, ordinary-module rate |
| Generic affine inverse-order rate | Fixed theorem's matrix/moment ingredients; affine rows with fixed `A`; complete recourse; reserved localizer degrees; `r >= max(s+1,d)`; uniform fixed-matrix Hoffman bound | Bilinear constraint rows, incomplete recourse, small conditioning constants, efficient repair computation |
| Regular projected multiplier rate | Same affine hierarchy and complete recourse; pointwise KKT pairs; weighted absolute tensor Chebyshev projection budget or coordinatewise Hölder/Lipschitz projection | Arbitrary multivariate Lipschitz projections, automatic regularity from strict convexity, multiplier computation in the SDP |
| Sharpness of affine and regular rectangular exponents | Actual matching separator measures; correct private lifts; Section 3 or Section 5 upper bounds | Equality with ideal local-measure optimum at each finite order, optimal leading constants, optimization hardness |
| Sparse moment/certificate equality with slack | Rectangular square cones and private square bounds; running intersection and exact separator consistency; nonempty primal evaluation set; finite-dimensional separation | Closedness or boundary attainment of the sparse certificate cone, rational bit complexity |

## 9. Verification record for this audit

No computational experiment, SDP solve, source checker, project-wide verification, or CI inspection was rerun. This audit uses direct proof reconstruction and the existing records as supplied evidence.

Read-only commands actually used were `cat AGENTS.md paper-sparse-sos/evidence/BRIEF.md`; the scoped file search `rg --files research-20260928/solver | rg 'partial-kernel|affine-recourse|active-region|fresh|proof|verif'`; `wc -l` on the five recourse review files; `nl -ba` on the four primary notes, five corresponding reviews, three verification notes, and `quadratic-sharpness.md`; selected `sed -n` ranges for long notes; and a scoped `rg -n` for kernel definitions and degree statements in `sparse-kernel-rounding.md`. The supplied `active-region-prior.md` was read for its sensitivity hypothesis statements. No external literature searches were performed.

Existing exact finite checks support the source identities and degree formulas but do not replace the general proofs. In particular, `active-region-verification.md`, lines 19–28, records 1,237 tested commutator frequencies above total degree `r`, and `active-region-fresh-review.md`, lines 148–159, correctly labels all three numerical SDP statuses `optimal_inaccurate`. Those numerical values are not rigorous certificates. The new order-unit argument in Section 7 has been proved symbolically here and should receive an independent mathematical review before publication.

The only new targeted artifact check was an inline `python3 - <<'PY' ... PY` command reading this audit with `pathlib.Path`, asserting a final newline, no trailing whitespace, equal counts of display-math opening and closing delimiters, and equal counts of `pmatrix` opening and closing delimiters. It passed for the 612-line first completed audit. This is a formatting check, not a mathematical proof check or a CI result.
