# Exact separator consistency by a common density correction

Date: 2026-09-28. Optional strengthening of
[sparse-putinar-kernel.md](sparse-putinar-kernel.md), with an independent
adversarial proof review. Publication priority remains unestablished.

The nearly normalized SOS kernel gives a sparse Putinar rate through
small separator errors. This note gives an alternative transfer with
exact separator consistency and an error proportional to the total local
coefficient norm, uniformly in the number of bags. Its degree requirement
has worse dependence on bag width. It uses the same established univariate
kernel; the candidate new step is a quantitative correction of the signed
bag densities.

## 1. Notation and finite-order theorem

Use the problem, sparse moment hierarchy, and notation of the companion
note: bags have sizes `v_b<=w`, local functionals satisfy the ordinary
box quadratic module at order `R`, and `C_b` is the Chebyshev coefficient
norm after removing the constant coefficient of `f_b`. Let
`C_f=sum_b C_b` and `W=sum_b osc(f_b)<=2C_f`.

Use the source kernel `Q(x,y)=p_(s,N)(x)S_s(x,y)^2`, source degree
`D=2(s-1)(N+1)`, and mass polynomial

\[
 n(x)=\int Q(x,y)\,d\mu(y)=1-z_s(x)^{N+1},
 \quad 0\le z_s(x)\le\tfrac12\quad(x\in[-1,1]).
\]

Take `s>=max(2,d_infty)`, even `N>=2`, and `R>=wD`. Write

\[
 r(x)=1-n(x),\qquad 0\le r(x)\le\delta=2^{-(N+1)}
       \quad(x\in[-1,1]),
\]

\[
 B={s^2(N+1)\over C_s},\qquad C_s={2s^2+1\over3s},
 \qquad
 \Delta_w=\sum_{j=2}^w {w\choose j}\delta^j B^{w-j}.
 \tag{1}
\]

An empty sum is zero. Let `eta` and `Gamma_v=(1+eta)^v-1` have the
same values as in the companion note, equation (3).

**Theorem 1 (uniform transfer in the number of bags).** Every feasible
sparse Putinar moment point admits a global box-supported probability
law `nu` with

\[
 \left|\int f\,d\nu-\sum_bL_b(f_b)\right|
 \le \sum_b C_b\Gamma_{v_b}+\Delta_w W
 \le C_f\left((1+\eta)^w-1+2\Delta_w\right).
 \tag{2}
\]

The same expression bounds `f*-rho_R` from above. There is no separate
factor depending on `t` or the tree diameter. The original theorem can
have a better width dependence because it can take a smaller `N`.
The finite-SDP duality argument in the companion note also gives a sparse
ordinary-module certificate for `f-f*` plus the right-hand side of (2),
with each local summand of degree at most `2R`.

## 2. Exactly normalized kernel and signed bag densities

Define

\[
 \overline Q(x,y)=Q(x,y)+r(x).
 \tag{3}
\]

Then `int Qbar(x,y)dmu(y)=1` identically as a polynomial in `x`.
The kernel is nonnegative on the box, but it need not be globally SOS
in `x`. Its tensor product therefore need not be positive under an
ordinary-module functional. We do not treat box nonnegativity as an
SOS certificate.

For each bag, let

\[
 \overline h_b(y)=L_b\left(\prod_{i\in B_b}
                                  \overline Q(x_i,y_i)\right).
 \tag{4}
\]

These are signed polynomial densities of mass exactly one. Their
separator marginals match exactly, because integrating a removed factor
in (4) replaces it by the constant one and the remaining polynomial
uses only the shared moments. All these polynomials have source degree
at most `v_bD<=R`.

The key remaining requirement is a common lower bound on the densities,
independent of the bag index.

## 3. A weighted pseudomoment bound for products of residuals

Fix a bag of size `v` and an output point `y`. For a subset `J` of its
coordinates, with `j=|J|`, put

\[
 G(x)=\prod_{i\notin J}Q(x_i,y_i),\qquad
 H(x)=\prod_{i\in J}r(x_i).
 \tag{5}
\]

The polynomial `G` is globally SOS and has degree at most `(v-j)D`.
For each residual factor, the interval polynomial `delta^2-r(x_i)^2`
is nonnegative and has degree at most `2D`. Its univariate interval
SOS certificate, multiplied by `G` and earlier residual squares, is
an ordinary-module certificate. Telescoping the product gives

\[
 0\le L_b(GH^2)\le\delta^{2j}L_b(G).
 \tag{6}
\]

For clarity, the relevant product identity is

\[
 \delta^{2j}-\prod_{i=1}^j r_i^2
 =\sum_{i=1}^j\delta^{2(j-i)}(\delta^2-r_i^2)
                                      \prod_{\ell<i}r_\ell^2.
\]

After multiplication by `G`, every certificate term has degree at most
`(v+j)D<=2wD<=2R`. Each multiplier other than its single interval
generator is SOS. Thus (6) needs no preordering products.

The weighted functional `p -> L_b(Gp)` is positive on all squares
needed for the pair `1,H`: write `G=sum q_l^2`, and note that
`deg(q_l H)<=(v+j)D/2<=R`. Its Cauchy–Schwarz inequality gives

\[
 |L_b(GH)|^2\le L_b(G)L_b(GH^2)
              \le\delta^{2j}L_b(G)^2,
 \quad |L_b(GH)|\le\delta^jL_b(G).
 \tag{7}
\]

If `L_b(G)=0`, the same inequality gives `L_b(GH)=0`; no division is
needed. This argument uses the full moment order `2R`. In contrast,
coefficient-norm evaluation below only uses polynomials of degree at
most `R`.

For fixed `y in [-1,1]`,

\[
 \|S_s(\cdot,y)\|_{1,\mathrm{cheb}}
 \le1+2\sum_{j=1}^{s-1}(1-j/s)=s.
\]

The known geometric multiplier bound gives

\[
 \|Q(\cdot,y)\|_{1,\mathrm{cheb}}
 \le\|p_{s,N}\|_{1,\mathrm{cheb}}s^2
 \le B.
 \tag{8}
\]

The Chebyshev pseudomoment bound `|L_b(T_alpha)|<=1` for `|alpha|<=R`
therefore implies

\[
 0\le L_b(G)\le B^{v-j}.
 \tag{9}
\]

## 4. A common density correction

Expand (4) by subsets `J` of residual factors. The term for `j=0` is
nonnegative because its polynomial is SOS. Each `j=1` term is also
nonnegative: the residual is interval nonnegative and multiplying its
univariate interval SOS certificate by the other globally SOS factors
stays in the ordinary module, at degree at most `vD`.
For every term with `j>=2`, equations (7),(9) bound its possible negative
part by `delta^j B^(v-j)`. Hence

\[
 \overline h_b(y)\ge-\Delta_{v_b}\ge-\Delta_w.
 \tag{10}
\]

The last inequality uses `B>=1` and the nonnegative binomial expansion:
`Delta_v` is nondecreasing in `v`. For the present parameters,
`B=s^2(N+1)/C_s>1`.

Set

\[
 h_b^+(y)={\overline h_b(y)+\Delta_w\over1+\Delta_w}.
 \tag{11}
\]

These are genuine probability densities with exactly matching
separator marginals. Indeed the product-arcsine reference densities are
the constant one, and every bag uses the same `Delta_w`. Integrating
out coordinates preserves both the original signed separator density
and the added constant. Ordinary tree gluing yields a global
probability law `nu` whose bag densities are `h_b^+`.

## 5. Objective error and rate

Let `Abar q=int q(y)Qbar(x,y)dmu(y)`. Orthogonality gives

\[
 \overline A1=1,\qquad \overline AT_k=AT_k\quad(k\ge1).
 \tag{12}
\]

Thus its univariate Chebyshev approximation error is zero on constants
and bounded by `eta` on the relevant positive degrees. The same tensor
product estimate gives

\[
 \|\overline A_b g_b-g_b\|_{1,\mathrm{cheb}}
         \le C_b\Gamma_{v_b}.
 \tag{13}
\]

All source degrees are at most `R`; the Chebyshev moment bound and
finite polynomial integration imply

\[
 \left|\int f_b\overline h_b\,d\mu^{B_b}-L_b(f_b)\right|
          \le C_b\Gamma_{v_b}.
 \tag{14}
\]

Although `hbar_b` may be signed, both `h_b^+ mu^B_b` and `mu^B_b` are
probability laws. Rearranging (11) gives

\[
 \int f_b h_b^+\,d\mu^{B_b}-\int f_b\overline h_b\,d\mu^{B_b}
 =\Delta_w\left(\int f_b\,d\mu^{B_b}
                     -\int f_b h_b^+\,d\mu^{B_b}\right),
\]

whose absolute value is at most `Delta_w osc(f_b)`. Summing this and
(14) proves (2).

For an explicit asymptotic choice, take

\[
 N=2\left\lceil\max\left(3/2,{w+1\over4}\right)
                                      \log_2s\right\rceil.
 \tag{15}
\]

For `w>=2`, `delta^2<=1/(4s^max(6,w+1))` and
`B<=3s(N+1)/2`. Taylor's theorem for `(B+x)^w` at zero, with its
nonnegative second derivative, gives

\[
 \Delta_w\le {w\choose2}\delta^2(B+\delta)^{w-2}
 \le {\binom w2\over4s^{\max(6,w+1)}}
                 \left({3s(N+1)\over2}+1\right)^{w-2}.
 \tag{16}
\]

For fixed `w>=2`, this is
`O_w(log^(w-2)(s)/s^3)=o_w(log(s)/s^2)`.
For `w=1`, `Delta_w=0`. Since (15) also gives `delta<=1/(2s^3)`,
the companion estimate remains valid:

\[
 \eta\le(3d_\infty^2+1)(N+1)/s^2.
\]

For fixed `w,d_infty`, choose `s` sufficiently large that `w eta<=1`.
Equation (2) then yields

\[
 f^*-\rho_R
 \le C_f\left[e w(3d_\infty^2+1){N+1\over s^2}
                                      +2\Delta_w\right]
       =C_f\,O_{w,d_\infty}\left({\log s\over s^2}\right).
 \tag{17}
\]

Taking `s` of order `R/log R` with its width-dependent constant proves
`f*-rho_R <= C_f O_(w,d_infty)(log^3(R)/R^2)` with constants independent
of the number of bags and tree topology. The order needed to certify a
fixed relative error per total coefficient norm is therefore uniform in
the number of bags for bounded width and bounded local degree.
For `w<=5`, (15) uses exactly the same multiplier degree parameter as
the companion approximate-consistency theorem; the uniformity in bag
count needs no additional asymptotic degree cost in this range.

This does not bound total SDP size independently of the number of bags.
At fixed width, the number of local PSD blocks still grows with `t`.
No claim is made that the displayed constants or width dependence are
practically competitive.

## 6. Review boundaries

The primary kernel source and prior-work boundaries are those of the
companion note. The [independent review](signed-density-review.md) checked
the weighted Cauchy–Schwarz degree bookkeeping, pointwise density bound,
exact separator consistency after the common shift, and uniformity in
`t`, and found no substantive defect. A second focused reviewer checked
the correction, objective identity, and rate. These reviews are supporting
evidence, not a formal verification or a novelty assessment.
A further [fresh final audit](signed-kernel-final-audit.md) independently
reconstructed the entire transfer, rechecked the smaller parameter choice
and finite SDP duality, and calibrated the conservative finite-order bound.
It also found no substantive defect.
It is a theorem about box optimization and does not preserve additional
hard local constraints or discrete domains. The common affine density
correction is elementary and is not separately claimed as new.

The targeted command

```text
python research-20260928/solver/check_sparse_putinar_kernel.py
```

passed the companion kernel checks, exact polynomial normalization of
`Qbar`, separator consistency for two distinct bag laws, monotonicity and
the Taylor bound for `Delta_w` on widths 1–8 at one parameter pair, and
an actual signed-density example corrected by a common shift.
These finite rational checks do not establish arbitrary-pseudomoment
positivity or universal degree claims. Those require the proof above.
No project-wide verification or CI inspection was performed.

The independent script was also rerun after the final parameter change:

```text
python research-20260928/solver/check_signed_density_review.py
```

It passed six exact residual-product identities, finite degree ledgers,
the correction identities, 256 finite rate-bound cases using (15), and
an exact ordinary-module pseudomoment example with
`L((1-x^2)(1-y^2))=-1/8`. That example is a useful warning against
assuming positivity of products of interval-nonnegative factors; its
degree parameters differ from this theorem and it is not a counterexample.
