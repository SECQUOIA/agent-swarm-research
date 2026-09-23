# Independent review: finite-bulk transfer of risk-sensitive mobility orders

Reviewed 2026-09-07 by `review_singular_exchange`.

The optimized positive-moment orders in [risk-sensitive-mobility.md](risk-sensitive-mobility.md), now independently verified in [the scalar review](review-risk-sensitive-mobility.md), transfer to the full bulk–surface model. A uniform bounded remainder is unnecessary: the graded trial designs have a uniform `O_q(log(1/M))` bulk remainder, which is smaller than every relevant moment scale.

The proof uses a general logarithmic estimate for a one-dimensional wall. It requires only a positive lower mobility bound and a bounded nonnegative rate with a uniformly positive integral. It uses no derivatives or upper bound of the mobility coefficient, so its constants do not silently depend on derivatives of the budget-dependent graded shape.

## A general positive-background lemma

Let `Gamma` be a fixed periodic one-dimensional wall of length `P`. Assume

\[
0\le k\le K_0,\qquad\int_\Gamma k\ge\kappa>0,
\quad D(s)\ge m>0,\quad\int_\Gamma D<\infty.
\tag{1}
\]

Constants may depend on `P,K0,kappa` and the fixed bulk data, but not on the detailed coefficient `D`. Fix units and take `0<m<=1` for the following estimates. Use the natural closed energy form, and define

\[
H_D=-\partial_s(D\partial_s)+k,
\qquad h=H_D^{-1}1,\quad J=\int h,\quad w=kh.
\]

The positive lower bound on `D` makes the energy domain a subspace of `H1(Gamma)`. Smooth tests and their energy closure define the operator even if `D` is integrable and unbounded above. Its positive inverse exists under (1).

To check coercivity directly, write `bar f=P^-1 int f`. Weighted anchoring and the periodic Poincare inequality give

\[
\kappa|\bar f|^2
\le2\int k|f|^2+2K_0\int|f-\bar f|^2
\le2\int k|f|^2+C\int|f'|^2.
\]

Therefore

\[
\|f\|_2^2\le C\left[\int|f'|^2+\int k|f|^2\right],
\quad Q_D[f]\ge cm\|f\|_2^2.
\tag{2}
\]

Thus `J<=C/m`. The energy and constant-test identities are

\[
\int D|h'|^2+\int kh^2=J,
\qquad\int w=P.
\tag{3}
\]

The positive source gives `h>=0`, hence `w>=0`. Since `D>=m`, `||h'||_2<=C/m`. The elementary one-dimensional bound by the mean and derivative gives

\[
\|h\|_\infty\le J/P+\sqrt P\|h'\|_2\le C/m,
\qquad\|w\|_\infty\le C/m.
\tag{4}
\]

No derivative of `D` occurred in this argument. For the cosine family, known sharper scalar estimates improve (4) to `||h||_infinity<=C m^(-3/4)`, but that improvement is unnecessary for the logarithmic conclusion.

## Why the bulk load grows at most logarithmically

Normalize Fourier coefficients by `hat w_n=P^-1 int w exp(-2pi i n s/P)`. Positivity and (3) give

\[
\widehat w_0=1,\qquad|\widehat w_n|\le1,\qquad
\sum_n|\widehat w_n|^2=P^{-1}\|w\|_2^2\le\|w\|_\infty.
\]

For `w-1`, the zero mode vanishes. Split its `H^(-1/2)` norm at an integer `N>=2`. The low modes contribute at most `C sum_(n=1)^N 1/n`, and the high modes contribute at most `C N^-1 sum_n|hat w_n|^2`. Choosing `N` comparable to `2+||w||_infinity` proves

\[
\boxed{\|w-1\|_{H^{-1/2}(\Gamma)}^2
\le C[1+\log(2+\|w\|_\infty)]
\le C[1+\log(1/m)].}
\tag{5}
\]

The first inequality is dimensionally independent of the mobility units because `w=kh` is dimensionless. The second is written in the fixed units specified above; an equivalent dimensional statement uses a fixed reference mobility inside the logarithm.

Now take a fixed bounded connected cross-section with sufficiently regular boundary for the trace map `H1(Omega)->H^(1/2)(Gamma)`, fixed positive transverse bulk diffusivity `Db`, constant affinity `K`, and fixed `u` in `L2(Omega)`. With `Z=A+KP`, `V=int u/Z`, and `B=KV^2/Z`, the Schur identity is

\[
D_{\rm flow}(D,k)=BJ(D,k)+R(D,k),\qquad R\ge0,
\]

\[
ZR=\sup_b\left[2L_D(b)-D_b\int_\Omega|\nabla b|^2-KS_D(b)\right],
\quad S_D(b)\ge0,
\]

\[
L_D(b)=\int_\Omega(u-V)b-KV\int_\Gamma wb.
\]

The load annihilates constants because `int w=P` and `int_Omega(u-V)=KPV`. Fix the mean-zero bulk gauge. Trace and Poincare estimates, with the duality in (5), give

\[
|L_D(b)|\le C[1+\|w-1\|_{H^{-1/2}}]\|\nabla b\|_2.
\]

Dropping the nonnegative Schur penalty and maximizing this scalar quadratic bound yields

\[
\boxed{0\le R(D,k)\le C[1+\log(1/m)].}
\tag{6}
\]

This is the required general lemma. It does not claim that the remainder is uniformly bounded or converges as `m` vanishes. The logarithm arises from the one-dimensional wall and its critical `H^(-1/2)` Fourier sum. The same conclusion should not be asserted for a higher-dimensional wall without redoing that estimate. It is also not uniform as bulk diffusivity tends to zero.

## Applying the lemma to the graded risk-sensitive trials

For the family

\[
k_c=(c+\cos s)^2,\qquad |c|\le2,
\]

we have `K0=9` and `int k_c=P(c^2+1/2)>=P/2`. Thus every constant in (6) is uniform in the random offset.

The verified scalar upper bounds use

\[
D_M(s)=A(r(s)+R)^{-\alpha},\qquad
\alpha=\frac{6q-4}{q+4},\qquad A\asymp R^{\alpha+6}.
\]

For every fixed `q>0`, `-1<alpha<6`. The distance `r(s)` ranges over a fixed compact interval. Consequently their essential minimum satisfies

\[
m_M:=\operatorname*{ess\,inf}D_M\asymp
\begin{cases}
R^6,&\alpha<0,\\
R^{\alpha+6},&\alpha\ge0.
\end{cases}
\tag{7}
\]

The normalization and the chosen scales

\[
R=M^{1/(6+\alpha)}\ (q<8/5),\quad
R=[M/\log(1/M)]^{1/7}\ (q=8/5),\quad
R=M^{1/7}\ (q>8/5)
\]

therefore imply `log(1/m_M)=O_q(log(1/M))`. The corners of the distance-based profile do not cause a difficulty for this lemma; only the positive lower bound and finite energy are used. If smooth coefficients are desired, comparable smooth approximations preserve these estimates.

It follows that

\[
\boxed{\sup_{|c|\le2}R(D_M,c)\le C_q[1+\log(1/M)].}
\tag{8}
\]

This avoids treating the budget-dependent derivative constants as fixed, which would invalidate a direct use of the earlier smooth-shape multiplier estimate.

## Transfer of all positive optimized moment orders

Assume `V!=0`, so `B>0`, and define the full-bulk objective

\[
\widetilde\Phi_q(M)=
\inf_{D:\int D=M}\mathbb E_c[D_{\rm flow}(D,c)^q].
\]

For arbitrary admissible designs, the smooth-test variational lower bound gives `D_flow>=BJ`, including the extended-value cases. This lower bound does not require asserting the Schur inverse identity for a design with infinite scalar response. Hence

\[
\widetilde\Phi_q(M)\ge B^q\Phi_q(M).
\]

For the explicit positive graded trial, the finite-response Schur identity and (8) give, for every fixed `q>0`,

\[
\mathbb E D_{\rm flow}^q
\le C_q\left[B^q\mathbb E J_c(D_M)^q+
(1+\log(1/M))^q\right].
\tag{9}
\]

Here `(x+y)^q<=C_q(x^q+y^q)` holds for all nonnegative `x,y` and every positive `q`; convexity of the power function is not assumed when `q<1`. Each verified scalar moment scale diverges as a strictly negative power of `M`, possibly multiplied by a logarithm, so the added logarithmic term is lower order.

Combining the scalar lower bounds and graded upper bounds proves

\[
\boxed{\widetilde\Phi_q(M)\asymp
\begin{cases}
M^{-q/4},&0<q<8/5,\\
M^{-2/5}[\log(1/M)]^{7/5},&q=8/5,\\
M^{(2-3q)/7},&q>8/5.
\end{cases}}
\tag{10}
\]

The constants may depend on the fixed moment order and bulk data. The threshold `8/5` and critical logarithm therefore survive finite bulk mixing. This is an order theorem, matching the scope of the scalar result; it does not identify optimal leading constants or a limiting optimizing profile.

A fixed molecular-diffusion contribution, or the isotropic surface contribution `(K/Z)M`, is also lower order and does not change (10). If the mean velocity is zero, the singular `BJ` term disappears and this argument does not give the displayed equivalents. No positive lower bound on arbitrary competing designs was imposed for the lower bound; it is used only by the explicit upper-bound trials.

## Independent numerical checks

I solved the conservative periodic discrete resolvent on 8,192 cell centers for the actual normalized graded coefficients, with mobility evaluated on cell faces. Sampled offsets were `c=0,0.5,1-R^2,1,1+R^2`. The Fourier norm uses the weights `(1+n^2)^(-1/2)` and includes the factor `2pi`.

| q | M | minimum mobility | sampled maximum `kh` | sampled maximum `||kh-1||_(H^-1/2)^2` |
|---:|---:|---:|---:|---:|
| 1 | 1e-4 | 1.178e-5 | 1.89362 | 0.07443 |
| 1 | 1e-8 | 1.063e-9 | 1.89812 | 0.00406 |
| 8/5 | 1e-4 | 6.429e-6 | 1.94439 | 0.07981 |
| 8/5 | 1e-8 | 4.377e-10 | 1.95048 | 0.00512 |
| 3 | 1e-4 | 2.322e-6 | 2.00312 | 0.08218 |
| 3 | 1e-8 | 6.972e-11 | 2.00735 | 0.00582 |

These fresh computations show no contradiction with the logarithmic bound and suggest that it is conservative for this particular trial family. They do not prove a uniform bounded remainder or its convergence. The analytic lemma deliberately establishes only the weaker estimate needed to transfer the moment orders.

The general positive-background lemma and this finite-bulk application have been independently derived here. Their novelty has not been investigated; the Fourier and trace estimates are standard tools. The research contribution under review remains the specific optimized transport-moment threshold and critical logarithm.
