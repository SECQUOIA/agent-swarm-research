# Sparse Putinar bounds from nearly normalized SOS kernels

Date: 2026-09-28. Research theorem with completed independent proof and
prior-work reviews. Publication priority remains unestablished.

## Scope and candidate contribution

For polynomial optimization on a box with a junction-tree objective
decomposition, the ordinary sparse quadratic-module hierarchy admits an
unconditional error bound of order `log^3(R)/R^2`, at moment order `R`.
The construction converts every feasible collection of local truncated
moment functionals into genuine local probability laws, bounds their
separator mismatch, and repairs it into a global box-supported law.

The squared Fejér kernel and its SOS polynomial normalization come from
[Gribling, de Klerk and Vera, arXiv:2605.31496](https://arxiv.org/html/2605.31496),
Sections 3.1–3.5. Those authors establish the corresponding dense rate.
The candidate addition here is the sparse transfer: the normalization error
has a univariate interval certificate, so it remains controlled after
multiplication by the other SOS kernel factors. Exact normalization is
unnecessary. This addresses the ordinary sparse Putinar hierarchy, which
uses `|B|+1` PSD matrices per bag instead of the `2^|B|` products in the
[preordering result](sparse-kernel-rounding.md).

The theorem concerns the box alone. It does not preserve additional hard
constraints or integrality, prove a practical SDP speedup, or establish
priority. Its algorithmic implication is a quantitative guarantee for a
standard sparse SDP relaxation, with the degree growth controlled by bag
width. Numerical conditioning, useful constants, extraction costs, and
extensions to constrained MINLP remain separate questions.

## 1. Problem and sparse hierarchy

Let `B_1,...,B_t` cover `{1,...,n}` and form the nodes of a tree satisfying
running intersection. Set `w=max_b |B_b|>=1`. Minimize

\[
 f(x)=\sum_{b=1}^t f_b(x_{B_b}),\qquad x\in[-1,1]^n,
 \qquad f^*=\min f.
\]

An order-`R` feasible sparse Putinar point consists of linear functionals
`L_b` on polynomials of total degree at most `2R` in `B_b`, with
`L_b(1)=1`, equal adjacent separator moments through degree `2R`, and

\[
 L_b(q^2)\ge0 \quad(\deg q\le R),\qquad
 L_b((1-x_i^2)q^2)\ge0 \quad(i\in B_b,\ \deg q\le R-1).
 \tag{1}
\]

Write `rho_R=inf sum_b L_b(f_b)`. Point evaluations are feasible, so
`rho_R<=f*`. A feasible moment point's own objective need not be a lower
bound; the relaxation optimum or a feasible SOS dual certificate supplies
the lower bound.

Expand each local objective in tensor Chebyshev polynomials,

\[
 f_b=c_{b,0}+g_b,\qquad
 g_b=\sum_{\alpha\ne0}c_{b,\alpha}T_\alpha,
 \qquad C_b=\sum_{\alpha\ne0}|c_{b,\alpha}|.
 \tag{2}
\]

Let `C_f=sum_b C_b`, `v_b=|B_b|`, and
`d_infty=max alpha_i` over nonzero objective coefficients; take
`d_infty=0` for a constant objective. Define
`Omega_b=max f_b-min f_b` on its bag box and `W=sum_b Omega_b`.
Then `||g_b||_infty<=C_b` and `W<=2C_f`.

## 2. Explicit finite-order statement

Choose integers `s>=max(2,d_infty)` and even `N>=2`. Set

\[
 D=2(s-1)(N+1),\qquad
 \delta=2^{-(N+1)},\qquad a=1-\delta,
 \qquad C_s={2s^2+1\over3s},
\]

\[
 \eta={N+1\over C_s}
       \left({d_\infty^2\over s^2}+{3d_\infty^2\over2s}\right)
       +\sqrt{2(D+1)}\,\delta,
 \qquad \Gamma_v=(1+\eta)^v-1.
 \tag{3}
\]

For an edge `e=bc`, write `S_e=B_b intersect B_c`. Put `epsilon_e=0`
if `S_e` is empty, and otherwise put

\[
 k_e=\max(|B_b\setminus S_e|,|B_c\setminus S_e|),
 \qquad \epsilon_e=1-a^{k_e}\le w\delta.
 \tag{4}
\]

**Theorem 1 (finite-order sparse rounding).** Suppose `R>=wD`.
Every feasible point `(L_b)` of (1) has a global box-supported probability
law `nu` satisfying

\[
 \left|\int f\,d\nu-\sum_bL_b(f_b)\right|
 \le E_{s,N}:=
 \sum_b C_b\bigl(\Gamma_{v_b}+1-a^{v_b}\bigr)
       +W\min\left(1,\sum_e\epsilon_e\right).
 \tag{5}
\]

Consequently,

\[
 0\le f^*-\rho_R\le E_{s,N}.
 \tag{6}
\]

The degree condition deliberately leaves a factor-two margin: kernel
outputs have degree at most `R`, allowing coefficient-norm error bounds
to be evaluated safely under the truncated functionals. Positivity of
the kernel itself would only require degree at most `2R`. We do not
silently assume bounds on all degree-`2R` tensor Chebyshev moments.

**Corollary 2 (rate).** For fixed objective and bag tree,

\[
 f^*-\rho_R=O\left({\log^3 R\over R^2}\right).
 \tag{7}
\]

More explicitly, choose `N=2 ceil((3/2)log_2 s)` and take `s` sufficiently
large that `w eta<=1`. Then, for `R>=wD`,

\[
 E_{s,N}\le wC_f\left[
 e(3d_\infty^2+1){N+1\over s^2}
                  +{2t-1\over2s^3}\right].
 \tag{8}
\]

Here `e` is Euler's number. Choosing `s` of order `R/(w log R)` proves
(7). The leading term scales as
`O(C_f w^3 (d_infty^2+1) log^3(R)/R^2)`; the displayed repair term is
`O(C_f t w^4 log^3(R)/R^3)` for fixed `w,t`. This asymptotic statement
does not hide a claim that the repair term is small uniformly in `t`.

## 3. Kernel construction and its verified interface

Let `mu` be normalized arcsine measure on `[-1,1]`. Define

\[
 S_s(x,y)=1+2\sum_{j=1}^{s-1}(1-j/s)T_j(x)T_j(y),
 \quad M_s(x)=\int S_s(x,y)^2\,d\mu(y)
             =1+2\sum_{j=1}^{s-1}(1-j/s)^2T_j(x)^2.
 \tag{9}
\]

The source kernel `S_s` is nonnegative on the square. Indeed, if
`x=cos theta`, `y=cos phi`, then it is the average of the classical
Fejér densities at `theta-phi` and `theta+phi`.
Orthogonality and `|T_j|<=1` give `M_s<=C_s`.
For completeness, define

\[
 R_s(u,v)=\int S_s(u,z)S_s(z,v)\,d\mu(z)
       =1+2\sum_{j=1}^{s-1}(1-j/s)^2T_j(u)T_j(v).
\]

Both kernel factors are nonnegative, hence `R_s>=0` on the square.
Using `2T_j(x)^2=1+T_j(T_2(x))` gives

\[
 M_s(x)=\tfrac12\bigl(C_s+R_s(T_2(x),1)\bigr),
 \qquad C_s/2\le M_s(x)\le C_s.
 \tag{10}
\]

Let

\[
 z_s(x)=1-M_s(x)/C_s,\qquad
 p_{s,N}(x)={1\over C_s}\sum_{j=0}^N z_s(x)^j,
 \qquad Q(x,y)=p_{s,N}(x)S_s(x,y)^2.
 \tag{11}
\]

Evenness of `N` is essential. The identity

\[
 \sum_{j=0}^N z^j={1\over2}\left[
 1+\sum_{j=0}^{N/2-1}z^{2j}(1+z)^2+z^N\right]
 \tag{12}
\]

proves that `p_{s,N}` is a globally SOS polynomial. Thus, for each fixed
`y`, `Q(.,y)` is globally SOS. Its source degree is at most `D`; its
`y` degree is at most `2(s-1)`. Its mass polynomial is

\[
 n(x)=\int Q(x,y)\,d\mu(y)=p_{s,N}(x)M_s(x)
      =1-z_s(x)^{N+1}.
 \tag{13}
\]

Since `0<=z_s<=1/2` on the interval,

\[
 a\le n(x)\le1,\qquad n\text{ is globally SOS},
 \qquad \deg n\le D.
 \tag{14}
\]

Global SOS of `n` follows either from (9),(11) or integration of a
finite-degree SOS Gram representation. The normalization residual is
exponentially small in `N`, rather than of the same size as the smoothing
error. This distinction is what makes separator repair inexpensive.

Let `A q(x)=int q(y)Q(x,y)dmu(y)`. For `0<=k<=s`,

\[
 \|AT_k-T_k\|_{1,\mathrm{cheb}}
 \le {N+1\over C_s}
          \left({k^2\over s^2}+{3k^2\over2s}\right)
           +\sqrt{2(D+1)}\,\delta.
 \tag{15}
\]

Here is a derivation keeping the degree count explicit. Extend
`a_j=min(j/s,1)` for `j>=0` and write
`Kq=int q(y)S_s(x,y)^2 dmu(y)`. Chebyshev product identities give

\[
 KT_k-M_sT_k
  =-a_k^2T_k
   -\sum_{j=1}^s(a_{j+k}-a_j)^2T_jT_{j+k}
   -\tfrac12\sum_{j=1}^{k-1}(a_{k-j}-a_j)^2T_jT_{k-j}.
 \tag{16}
\]

Every product `T_iT_j` has Chebyshev coefficient norm one. The map
`j -> a_j` has increments bounded by distance divided by `s`, so

\[
 \|KT_k-M_sT_k\|_{1,\mathrm{cheb}}
 \le k^2/s^2+k^2/s+(k-1)k^2/(2s^2)
 \le k^2/s^2+3k^2/(2s).
 \tag{17}
\]

The Chebyshev norm is submultiplicative because
`T_iT_j=(T_{i+j}+T_|i-j|)/2`. The expansion of `M_s` shows
`||z_s||_(1,cheb)=(C_s-1)/C_s<=1`, hence
`||p_(s,N)||_(1,cheb)<=(N+1)/C_s`.
For a univariate polynomial `q` of degree at most `D`, orthogonality and
Cauchy–Schwarz imply

\[
 \|q\|_{1,\mathrm{cheb}}\le\sqrt{2(D+1)}\|q\|_\infty.
\]

Apply this to `n-1`, whose degree is at most `D` and sup norm at most
`delta`. Now
`AT_k-T_k=p_(s,N)(KT_k-M_sT_k)+(n-1)T_k` proves (15).
This uses the direct degree `D=2(s-1)(N+1)`; no degree convention from
the source is imported into the estimate.

For a bag of size `v`, let `A_b` be the tensor product of `A`. Repeated
use of the product difference identity and (15) gives

\[
 \|A_bT_\alpha-T_\alpha\|_{1,\mathrm{cheb}}
       \le(1+\eta)^v-1=\Gamma_v
       \quad(\alpha_i\le d_\infty).
 \tag{18}
\]

## 4. Polynomial densities under ordinary-module positivity

For each bag, define

\[
 Q_b(x,y)=\prod_{i\in B_b}Q(x_i,y_i),\qquad
 h_b(y)=L_b(Q_b(\cdot,y)),\qquad
 Z_b=\int h_b\,d\mu^{B_b}.
 \tag{19}
\]

Products of SOS polynomials are SOS. The degree is at most `v_bD<=R`,
so (1) implies `h_b>=0`. This argument uses no products of box generators.

The univariate polynomials `n-a` and `1-n` are nonnegative on the
interval and have even degree at most `D`. The classical univariate
interval SOS theorem gives representations in
`Sigma[x]+(1-x^2)Sigma[x]`, with each summand of degree at most `D`.
Multiplying such a representation by a globally SOS polynomial preserves
membership in the ordinary multivariate quadratic module.

For fixed separator output `y_S`, put

\[
 Q_S(x_S,y_S)=\prod_{i\in S}Q(x_i,y_i),\qquad
 h_S(y_S)=L_b(Q_S(\cdot,y_S)).
 \tag{20}
\]

Adjacent moment agreement makes `h_S` independent of the choice of
endpoint bag. Define `h_empty=1`. Integrating out `B_b\S` in (19)
gives the unnormalized marginal

\[
 h_{b,S}(y_S)=L_b\left(Q_S(\cdot,y_S)
                        \prod_{i\in B_b\setminus S}n(x_i)\right).
 \tag{21}
\]

Let `P_j` be the product of the first `j` mass polynomials in the
removed coordinates. The identities

\[
 1-P_j=(1-n_j)P_{j-1}+(1-P_{j-1}),
\]
\[
 P_j-a^j=(n_j-a)P_{j-1}+a(P_{j-1}-a^{j-1})
 \tag{22}
\]

show inductively that both polynomials have ordinary-module
representations of degree at most `jD`: all `P_j` are globally SOS,
and no two box generators are multiplied together. Multiply (22) by
the SOS polynomial `Q_S`. The resulting degree is at most
`(|S|+j)D<=R<=2R`. Applying (1) proves the pointwise bounds

\[
 a^{|B_b\setminus S|}h_S\le h_{b,S}\le h_S,
 \qquad a^{v_b}\le Z_b\le1.
 \tag{23}
\]

For any separator, `Z_S=int h_S dmu^S` similarly lies in
`[a^|S|,1]`. In particular it is positive. Define actual probability
laws `nu_b` with density `h_b/Z_b` and the reference separator law
`eta_S` with density `h_S/Z_S`. Since `Z_b<=Z_S`, (23) implies the
measure domination

\[
 (\nu_b)_S\ \ge\ a^{|B_b\setminus S|}\eta_S.
 \tag{24}
\]

For adjacent bags `b,c`, both normalized separator marginals dominate
`a^k_e eta_S`. Their common mass is at least `a^k_e`, so, with total
variation defined as `sup_A |P(A)-Q(A)|`,

\[
 \operatorname{TV}((\nu_b)_{S_e},(\nu_c)_{S_e})
         \le1-a^{k_e}=\epsilon_e.
 \tag{25}
\]

An empty separator has a unique probability law and TV zero. These
estimates avoid division by a possibly small density and remain valid
where `h_S` vanishes.

## 5. Objective approximation and global repair

For every tensor Chebyshev polynomial with `|alpha|<=R`,

\[
 |L_b(T_\alpha)|\le1.
 \tag{26}
\]

Indeed,

\[
 1-T_\alpha^2
 =\sum_i(1-x_i^2)U_{\alpha_i-1}(x_i)^2
                         \prod_{j<i}T_{\alpha_j}(x_j)^2
 \tag{27}
\]

is an ordinary-module representation of degree at most `2|alpha|`;
zero indices contribute zero. It bounds `L_b(T_alpha^2)` by one.
Moment PSD then gives `L_b(T_alpha)^2<=L_b(T_alpha^2)`.
All terms of `A_b g_b-g_b` have degree at most `v_bD<=R`, so (18),(26)
imply

\[
 |L_b(A_bg_b-g_b)|\le C_b\Gamma_{v_b}.
 \tag{28}
\]

Fubini for finite polynomial sums gives
`Z_b int g_b dnu_b=L_b(A_b g_b)`. Thus the identity

\[
 \int g_b\,d\nu_b-L_b(g_b)
 =L_b(A_bg_b-g_b)+(1-Z_b)\int g_b\,d\nu_b
\]

and (23),(28) yield

\[
 \left|\int f_b\,d\nu_b-L_b(f_b)\right|
 \le C_b(\Gamma_{v_b}+1-a^{v_b}).
 \tag{29}
\]

Constants in `f_b` cancel exactly. In particular normalization creates
no artificial error for adding a constant to the objective and requires
no reciprocal lower bound on `Z_b` in (29).

We now use a general elementary repair lemma. Couple the separator
marginals of each adjacent pair of bag laws by maximal coupling; its
disagreement probability is their TV distance. Lift each edge coupling
to the full two bag laws using their conditional distributions given
the separator. The resulting pair law on each tree edge has the original
bag laws as its marginals. Tree gluing of these pair laws gives a joint
tuple `(Y_b)_b` preserving every bag law and satisfying

\[
 \Pr[\text{at least one edge separator disagrees}]
       \le\min(1,\sum_e\epsilon_e).
 \tag{30}
\]

All spaces are standard Borel, so the stated conditional laws and
couplings exist. On the agreement event, running intersection makes
the bag tuple a single global box point. On its complement output any
fixed box point, for example zero. This measurable map defines `nu`.
Each local objective changes by at most its oscillation, hence

\[
 \left|\int f\,d\nu-\sum_b\int f_b\,d\nu_b\right|
       \le W\min(1,\sum_e\epsilon_e).
 \tag{31}
\]

Combining (29),(31) proves (5). Since `nu` is box supported,
`f*<=int f dnu`; taking the infimum over feasible moment points proves
(6). The [independent repair note](putinar-tree-repair.md) develops
stronger tree-sensitive versions of (31), but they are not needed here.

For the rate, `N=2 ceil((3/2)log_2 s)` gives
`delta<=1/(2s^3)`. From `C_s>=2s/3` and `s>=2`, the first term of
(3) is at most `3d_infty^2(N+1)/s^2`. Its second term is at most
`(N+1)/s^2`, so

\[
 \eta\le(3d_\infty^2+1)(N+1)/s^2.
\]

When `w eta<=1`, `Gamma_v<=e v eta`. Also
`1-a^v<=v delta` and `sum_e epsilon_e<=(t-1)w delta`.
Use `W<=2C_f` in (5) to prove (8).
Finally, for all sufficiently large `R`,
`s=floor(R/(8w log_2(R+2)))` satisfies `s>=max(2,d_infty)` and
`wD<=R`, while `s` is of order `R/(w log R)`. This proves (7) for
all sufficiently large orders, rather than only a subsequence.

## 6. Sparse polynomial certificate consequence

The product-arcsine moments give a strictly feasible point for all moment
and single-generator localizing matrices: each permitted nonzero square
has positive integral, including after multiplication by `1-x_i^2`.
These local moments satisfy the separator equalities. The objective is
bounded by (26). Finite-dimensional SDP Slater duality therefore gives
dual attainment and no gap. Consequently,

\[
 f-\rho_R\in\sum_b\left\{
 \sigma_{b,0}+\sum_{i\in B_b}(1-x_i^2)\sigma_{b,i}:
 \sigma_{b,i}\text{ SOS},\quad
 \deg\sigma_{b,0},\ \deg((1-x_i^2)\sigma_{b,i})\le2R
 \right\}.
 \tag{32}
\]

The separator multiplier polynomials cancel when the local dual
identities are summed. By (6), `f-f*+E_(s,N)` has a certificate of the
same form, after adding a nonnegative constant. This is an existence
statement for real SOS coefficients, without a rational coefficient or
bit-complexity guarantee.

## 7. Literature boundaries and verification status

The kernel construction, coefficient approximation method, and dense
rate are prior. The assertions assessed by the independent prior audit are
the ordinary-module separator inequalities (23)–(25) and their use to
transfer the dense exponent to the sparse hierarchy without a polynomial
separator dual-attainment assumption. The older sparse rate and the
distinction from generalized-moment results are discussed in the
[preordering audit](prior-independent.md) and the completed
[ordinary-module audit](sparse-putinar-prior.md). No equivalent result was
located in those searches; that does not establish priority.

The parallel prior audit identified earlier public statements that rule
out a broad claim of the first second-order sparse rate:
[Magron's Lorentz Center slides, 7 July 2025](https://homepages.laas.fr/vmagron/slides/lorentz25.pdf),
logical slide 23/44, and
[TENORS Learning Week 2 slides, 16 February 2026](https://homepages.laas.fr/vmagron/nlmoment.pdf),
logical slide 35/90, display an `O(d^-2)` two-bag full-preordering bound
and mention a sparse Putinar rate without specifying its exponent.
These statements require direct comparison with this ordinary-module
transfer and its assumptions; they do not justify calling the present
rate new merely because an inspected journal theorem has a slower bound.

Every mathematical step above is supplied explicitly except the standard
univariate interval SOS theorem, existence of regular conditional laws
and maximal couplings on standard Borel spaces, and finite SDP duality.
The proof does not require a local representing measure for `L_b`.
It does not use a sparse polynomial message or separator dual that may
fail to attain. Additional hard constraints are not preserved by its
smoothing or repair maps. The width and coefficient dependence have not
been optimized. The [fresh proof review](sparse-putinar-fresh-review.md)
found no substantive defect. The dedicated prior audit is complete.
The [exact-consistency strengthening](sparse-putinar-exact-consistency.md)
removes the additional tree-size term and has its own
[final adversarial audit](signed-kernel-final-audit.md).

Targeted command run:

```text
python research-20260928/solver/check_sparse_putinar_kernel.py
```

Result: 99 exact univariate basis identities and coefficient bounds passed
for 18 parameter pairs, as did an exact two-bag example with strict
normalization mismatch and the predicted separator domination. The script
checks the geometric SOS identity, mass residual, source degree, residual
identity (16), and coefficient estimates with rational arithmetic.
It is not a proof for all degrees or for arbitrary pseudomoments.
The separate tree-repair script is recorded in its companion note.
No project-wide checks or CI inspection were performed.
