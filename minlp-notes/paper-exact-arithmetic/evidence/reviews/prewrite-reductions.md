# Independent prewriting audit: exact-comparison reductions

Date: 2026-10-05. This is an internal mathematical audit, not external peer review or a priority determination.

## Verdict and scope

I reconstructed the arguments rather than relying on the historical reviews. I found no substantive mathematical gap in the stated certified cubic-root, unconstrained quartic, rational-optimizer coordinate, Boolean-closure, adaptive integer-sign, variable-degree upper-bound, circuit interior-Gram, strongly monotone cubic-zero, or binary-extraction results. The conclusions remain valid with their stated representation and promise boundaries. The proofs need to be assembled in the manuscript: a reference to a repository construction is not a complete proof.

The audit covers the six assigned September 27 notes and their proof dependencies, the Boolean and adaptive compilers in `research-20260928/algebra`, and all four notes in `research-20261003-arithmetic/reviews/exact-core/general-degree`. At the root's request, I also audited the strongly monotone cubic-zero note and the September 28 binary-extraction/full-joint-Gram note. I read the relevant existing reviews after reconstructing the main arguments; their passed status is not the basis of this verdict. I did not browse, investigate literature, run mathematical scripts, conduct computational experiments, or inspect CI. The literature agent must verify the three cited algorithmic source interfaces used in the upper bounds: convex approximation, effective quantifier elimination, and the rational rounded ellipsoid cut-or-stop result. Nothing below establishes novelty.

The following are requirements for a complete manuscript, rather than unresolved objections to the theorems:

1. State the exact encoding, sharing, and gate-count conventions before giving a reduction. A circuit is a directed acyclic graph, not an expanded formula or expanded fraction list.
2. Include the full positive definite Hessian Gram proof and rational coefficient projection. Positivity of a Hessian biform on tensor vectors alone does not establish positive definiteness of its Gram matrix.
3. Distinguish the semantic global-curvature promise from an ordinary language with a checked rational Hessian certificate. Specify the fixed negative output for every malformed certificate.
4. Retain polynomially bounded degree in the variable-degree upper result. Unary degree is one sufficient convention. Sparse binary exponents without this bound are outside the proof.
5. State the effective quantifier-elimination bound used to fix a universal polynomial accuracy schedule. Do not leave a data-dependent or uncomputable choice of Newton iteration count.
6. Prove the bounded universal SLP interpreter when stating adaptive closure. Boolean closure for a fixed list of queries is not by itself an adaptive-closure proof.

## 1. Cubic-root sign simulation

Source: `research-20260927/posslp-certified-cubic-root-reduction.md`, especially equations (2)--(16), lines 63--300. The construction is sound.

Write

\[
A(z)=(1+3z)^{1/3}-1,\quad S(z)=A(z^2),\quad
H(z)=\tfrac12\{S(A(z))+S(A(-z))\},
\]
\[
P(x,y)=A\bigl((H(x+y)-H(x-y))/4\bigr).
\]

The analytic branches are the branches taking value one before subtracting one. The binomial expansion gives `A(z)=z+O(z^2)`, hence `H(z)=z^2+O(z^4)` because `H` is even. Exact evenness gives `P(x,0)=P(0,y)=0`. The quadratic leading term is `xy`. These statements are algebraic identities between analytic functions; they remain true when the same wire is supplied twice and when the leading coefficient of a signal is zero.

For `|z|<=1/12`, the segment from zero to `z` remains in a disk where `|1+3z|>=3/4`. Integrating the derivative gives `|A(z)|<=2|z|`; integrating the second derivative gives the real estimate `|A(z)-z|<=2z^2`. This also justifies the complex bound needed for Cauchy estimates, rather than treating a real derivative estimate as an automatic complex estimate.

On `|x|,|y|<=r=1/100`, the four inner `A` outputs have magnitude at most `0.04`, their `S` outputs at most `0.0032`, and the final `A` argument at most `0.0016`. Every branch is analytic on a neighborhood of the closed polydisk and `|P|<1`. Cauchy's coefficient bound is therefore `|p_ij|<=r^(-i-j)`. Exact axis vanishing eliminates all terms with `i=0` or `j=0`; subtracting `xy` also eliminates `(i,j)=(1,1)`. For `s=|x|/r,t=|y|/r<=1/4`, the remaining geometric series gives

\[
|P(x,y)-xy|\le\frac{|xy|}{r^2}
\left(\frac1{(1-s)(1-t)}-1\right)
\le\frac{2}{r^3}|xy|(|x|+|y|).
\]

The last inequality follows from `1/((1-s)(1-t))-1=(s+t-st)/((1-s)(1-t))` and `((1-s)(1-t))^(-1)<=16/9<2`. Thus the stated `K=2^24` is safe. This factor of `|xy|` is essential when two signal orders differ; a bare `O((|x|+|y|)^3)` bound would not support the homogenization proof.

For an integer circuit, first use `W=2V-1`; then `W` is a nonzero integer and `W>0` exactly when `V>0`. Represent each integer value by numerator and denominator signals of a common assigned order, with leading coefficients `(V_i,1)`. Multiplication uses `P(f_a,f_b),P(g_a,g_b)`. Addition/subtraction first cross-multiplies the signals, then uses `A` on the equal-order numerator terms. Initial zero is the exact signal `A(delta-delta)=0`; its assigned order one is a bookkeeping convention, not a claim of nonzero leading coefficient.

Count every such macro, including zero initialization, in `T`. Set `B_0=2`, `B_j=64 K B_(j-1)^3`. Then `log_2 B_j=16*3^j-15`. Under `delta<=2^-30/B_T`, the induction

\[
|C|\le B_j,\qquad |f-C\delta^d|\le B_j\delta^{d+1},\qquad
|f|\le2B_j\delta^d
\]

holds for every available signal after macro `j`. For equal-order addition, inherited error is at most `2B delta^(d+1)` and the `A` error at most `32B^2 delta^(2d)`, so the total is at most `34B^2 delta^(d+1)`. For multiplication, inherited error is at most `3B^2 delta^(a+b+1)` and the `P` error at most `16KB^3 delta^(a+b+1)`. Both fit the recurrence. Smallness guarantees the analytic bounds at every use. No step divides by a signal or its leading coefficient, so complete cancellation is covered. At the final numerator, the error is less than `delta^d/2`, whereas the integer leading coefficient has magnitude at least one.

The tiny parameter is generated rather than printed. Take `q=2T+5`, `Q=q+9T+1`, `delta_0=1000^(-(Q+3))`, and `delta=S^q(delta_0)`. Since `0<S(z)<=z^2` for positive `z`,

\[
0<\delta\le\delta_0^{2^q}<2^{-4\,2^q},\qquad
4\,2^q=2^{2T+7}>16\,3^T+30.
\]

This gives the required error budget. The topology fixes `T` before the choice of the parameter, so there is no circularity.

Each addition macro uses one raw root gate; each product uses nine. All radicands are affine combinations of individual predecessor roots and their squares. For the topologically numbered raw gates, take `w_i=1000^i delta_0`, `L_i=1-w_i`, `U_i=1+w_i`. There are at most `Q` gates and `w_i<=1000^-3`. Except at the first parameter gate, the radicand equals one at the all-one input. Direct signed interval deviation is at most `13w_(i-1)`: the addition coefficient sum is at most six, a square gate gives `12w+3w^2<=13w`, and the final product coefficient sum is `3/2`. Combining repeated occurrences of a predecessor can only improve this bound; keeping occurrences separate is also safe. The interval endpoints satisfy

\[
(1-w_i)^3\le1-2w_i\le1-13w_{i-1},\quad
(1+w_i)^3\ge1+3w_i\ge1+13w_{i-1}.
\]

The first parameter gate is checked directly. Printed parameter constants and interval endpoints have `O(Q)` bits. Thus the construction proves its interval certificate on all inputs; it does not infer the certificate from the unknown true root values.

## 2. Signed odd-root realization and full Hessian Gram

Sources: `signed-odd-root-circuit-quartic.md`, equations (2)--(18), lines 57--373; `sos-convex-quartic-realization.md`, equations (5)--(16), lines 79--246; the abstract global Hessian estimates in `general-strongly-convex-quartic-singleton.md`, equations (13)--(20). The signed-root argument does not require reconstruction of a common minimal polynomial.

Degrees `d_i=2n_i-1>=3` must be unary or otherwise polynomially bounded by input length. Normalize each signed box by `alpha_i=sigma_i kappa xi_i`, where `sigma_i` is the box sign and `kappa=max(1,1/min_i min(|L_i|,|U_i|))`. Then `alpha_i>=1`. The transformed coefficients are exactly

\[
c'_i=\sigma_i\kappa^{d_i}c_i,\qquad
a'_{ije}=\sigma_i\sigma_j^e\kappa^{d_i-e}a_{ije}.
\]

Reciprocal powers are allowed when `d_i-e<0`; their exponents have magnitude at most `2N`, where `N=sum n_i`. Coefficient and endpoint bit lengths remain polynomial. State the stronger useful quantitative fact: the numerical values `log A` and all later precision exponents are polynomially bounded by input length, not merely that the binary encoding of `log A` is short.

Introduce coordinates for powers through `n_i`. The `N` residuals are the power-chain equations and the terminal equation `X_(i,n_i-1) X_(i,n_i)-b_i(X)`. They have one real common zero by triangular induction and uniqueness of odd real roots. The local Jacobian determinant is `d_i alpha_i^(d_i-1)`; the global Jacobian is block lower triangular. Its determinant magnitude is at least one. The source states gradient bounds with `V=4NA^N`; explicitly add `||J||_F<=V`, which follows by summing the local derivative entries and the total affine coefficient norm. This yields `sigma_min(J)>=V^(-(N-1))=:nu`, not just a bound from individual row norms.

For one gate, index the exposing matrix by `j=0,...,n-1`; this indexing should be explicit in the manuscript. Put `ell_j=X_(j+1)-alpha X_j`, `X_0=1`, and use the tridiagonal matrix with diagonal `alpha^(d-1-2j)` and adjacent entries `alpha^(d-2-2j)/2`. It is `D T_0 D`, with `D_jj=alpha^(n-1-j)` and `T_0` having diagonal one and adjacent entries `1/2`. Its smallest eigenvalue is at least `(n+1)^-2`. The exposing identity on the power curve is

\[
P_\alpha(t,t^2,\ldots,t^n)
=(t-\alpha)^2\sum_{h=0}^{d-1}\alpha^{d-1-h}t^h
=(t-\alpha)(t^d-\alpha^d).
\]

The local centered matrix has lower bound `h_0=[N^2(N+1)^2 A^(2N)]^-1` and upper bound `L_0=8A^(2N+2)`. Restoring the predecessor radicand gives

\[
E_i^*(p+u)=u_i^T H_i u_i-u_{i,1}\sum_{j<i,e}a_{ije}u_{j,e}.
\]

There are no residual linear terms. Use `rho=(h_0/(2NA))^2`, `omega_i=rho^(i-1)`. After rescaling blocks by `sqrt(omega_i)`, each cross entry has magnitude at most `A sqrt(rho)/2`; its row sum is at most `h_0/4`. Thus the total centered form has lower bound `gamma=h_0 rho^(k-1)/2`, with the stated upper bound `W`. This is a bound on all directions, including reused gates.

Rational approximation must stay in the exact vanishing space. For local ordinary monomials `M`, let `R_M=M-m_(w(M))`, where `m_h` is the rational quadratic representative of the power `t^h`. Then

\[
E_i^*=S_i-\alpha_i T_i+\sum_M\beta_M(\alpha_i)R_M,
\quad S_i=X_{i,n_i}^2-b_iX_{i,1},\quad
T_i=X_{i,n_i-1}X_{i,n_i}-b_i.
\]

Every displayed rational polynomial vanishes at the true circuit point. Approximating the scalar coefficients therefore leaves the zero exact. The total coefficient error is at most `k B_0 theta`, with `B_0=A+1+32N^2(A+1)^(2N)`. The quadratic matrix error is bounded by the same coefficient one-norm. Its gradient error at `p` is at most `2A^N kB_0 theta`. The source's choices of `theta` give `G(p+u)=ell^T u+u^T H u`, `mI<=H<=LI`, `||ell||<=epsilon`, where `m=gamma/2`, `L=W+1`.

Root approximation is polynomial bit time at this requested precision. On `[1,A]`, a retained power has derivative at most `N A^(N-1)`, so an affine radicand interval has width at most `C=NA^N` times the largest predecessor width. Its certified lower endpoint is at least one, and the odd-root derivative is at most one there. Outward root rounding with mesh `eta` gives `D_i<=C max_(j<i) D_j+2eta`. Taking `eta<=2^-P/[4k(C+1)^k]` is sufficient for root error `2^-P`. Unary exponentiation, rational bisection, and all endpoint sizes are polynomial in input length and `P`.

Here is the abstract certificate lemma that must be included once and reused. Suppose the centered rational quadratics satisfy

\[
G=\ell^Tu+u^THu,\quad r_j=b_j^Tu+u^TT_ju,
\]
\[
H\succeq mI,\quad\|H\|\le L,\quad\|T_j\|\le1,\quad
\|b_j\|\le V,\quad\sum_j b_jb_j^T\succeq\nu^2I.
\]

For `F_0=G^2+epsilon sum r_j^2`, use the full coordinate vector `(v,u tensor v)`. Define

\[
\mathcal D(b,T)_{i,(k,j)}=2b_kT_{ij}+4b_iT_{kj},
\]
\[
C=2\ell\ell^T+2\epsilon\sum_j b_jb_j^T,\qquad
D=\mathcal D(\ell,H)+\epsilon\sum_j\mathcal D(b_j,T_j),
\]
\[
Q=8\operatorname{vec}H\operatorname{vec}H^T+4H\otimes H
+\epsilon\sum_j\{8\operatorname{vec}T_j\operatorname{vec}T_j^T+4T_j\otimes T_j\},
\quad M=\begin{pmatrix}C&D\\D^T&Q\end{pmatrix}.
\]

Differentiating each square proves the Hessian identity exactly. Crucially `T_j tensor T_j >=-I` holds on the full tensor space, including when `T_j` is indefinite. Therefore

\[
C\succeq2\epsilon\nu^2I,\quad Q\succeq(4m^2-4\epsilon N)I,
\quad \|D\|\le6\sqrt N\,\epsilon(L+NV).
\]

If `epsilon<=min(1,m^2/(2N),nu^2 m^2/[36N(L+NV)^2])`, then `Q>=2m^2I` and the Schur complement is at least `(3/2)epsilon nu^2 I`. This proves `M` positive definite on the entire space of dimension `N+N^2`. The separate scalar radial Hessian estimate gives the specific global modulus. Put `D_*=L+NV` and `r=||u||`. The degree-two part has Hessian at least `2epsilon nu^2 I`. The cubic part has norm at most `12epsilon D_* r`, by differentiating `2(b^T u)(u^T T u)`. For the quartic part, the identity

\[
\nabla^2(u^TTu)^2=8(Tu)(Tu)^T+4(u^TTu)T
\]

gives lower bound `4(m^2-epsilon N)r^2 I>=2m^2 r^2 I`. The indefinite residual matrices contribute the negative term `-4epsilon N r^2 I`; their squared forms must not be presumed convex. Summing and completing the radial square gives

\[
\nabla^2F_0\succeq
\left[2m^2\left(r-3\epsilon D_*/m^2\right)^2
+2\epsilon\nu^2-18\epsilon^2D_*^2/m^2\right]I
\succeq\tfrac32\epsilon\nu^2I.
\]

The factor `N` in the Gram smallness condition must not be dropped merely because the weaker ordinary-convexity calculation lacks it.

To make the certificate rational, translate by `S_p=[[I,0],[-p tensor I,I]]`, so `M_X=S_p^T M S_p`. With `q_*=2m^2`, `s_*=(3/2)epsilon nu^2`, `B_D=6N epsilon(L+NV)`, and `||p||<=K_p`, one explicit lower bound is

\[
M_X\succeq\eta_*I,\qquad
\eta_*={\min(s_*,q_*)\over(2+2(B_D/q_*)^2)(2+K_p)^2}.
\]

Its logarithmic size is polynomial. Once the rational quadratics are fixed, `b_j` and `ell` are affine in the formal center, `H,T_j` are constant, and the translated Gram entries have degree at most two in that center. Their coefficient bit lengths are polynomial. More explicitly, a coefficient one-norm bound `C_M` on these entries gives a first-derivative bound `2C_M(1+K_p)` per coordinate on a unit neighborhood; summing over entries and coordinates gives an explicit polynomial-dimension Lipschitz factor. This proves that polynomially many center bits suffice for Frobenius error below `eta_*/4`. Retained-power derivatives control those center bits. No exact field representation is needed.

For every Hessian monomial `gamma`, form the zero-one symmetric matrix `E_gamma` whose ordered entry `(i,j)` is one precisely when the corresponding basis product equals `gamma`. Their supports partition the matrix entries, so they are Frobenius-orthogonal. With the rational Hessian coefficient `c_gamma`, project a rational symmetric approximation `T` by

\[
\mathcal P(T)=T+\sum_\gamma E_\gamma
{c_\gamma-\langle E_\gamma,T\rangle_F\over\|E_\gamma\|_F^2}.
\]

This is exact rational orthogonal projection onto the coefficient equations. It fixes `M_X` and is nonexpansive, leaving a positive definite rational certificate with the exact Hessian identity. Off-diagonal entries are counted twice both in the projection equation and in the biform. Finally choose `epsilon=t^2` dyadic and scale by `1/(epsilon nu^2)`. The output has `N+1` rational quadratic square factors, degree exactly four, unique zero `p`, global Hessian at least `(3/2)I`, and a full rational positive definite Hessian Gram. All operations and printed outputs have polynomial bit size.

## 3. Feasibility, unit-cube optimization, and unconstrained value hardness

Source: `unconstrained-quartic-posslp-reduction.md`, equations (1)--(15), lines 21--298, and the two transfer sections at the end of the cubic-root reduction. Both transfers are valid.

For feasibility, `F<=0` restricts the variables to the single zero; the rational affine comparison of the designated first-power coordinate encodes the sign. This is degenerate exact feasibility. For unit-cube optimization, all normalized power coordinates lie in `(0,4)`, since the normalized roots are less than two and only powers one and two are retained. The box with designated lower endpoint `kappa` and all upper endpoints eight contains the zero exactly in the yes branch. Nonnegativity and compactness give zero optimum in the yes branch and positive optimum in the no branch. The rational affine map from `[0,1]^N` has diagonal scales eight or `8-kappa>6`, so the Hessian is at least `36I`. The full Gram changes by an invertible rational map on the full basis. The cube has a strict interior point; the added zero-threshold inequality does not inherit that Slater property. No uniform polynomial-bit positive gap follows.

For unconstrained value hardness, append `r=T+1` distinct square-signal gates starting at `delta`; their final signal satisfies `0<epsilon<=delta^(2^r)`. Rebuild all boxes with the larger raw-gate bound before generating `delta_0`. This preserves the analytic proof and polynomial certificate size. The final arithmetic signal satisfies `d<=2^T`, `|s|>=delta^d/2`, and the sign of `s` is the sign of `2V-1`.

At the zero of the realized quartic, choose distinct coordinates `a,b` and set `u=X_a-kappa`, `v=X_b-kappa`; then `u_0>0`, `v_0!=0`, `|v_0|<=1/8`, and `u_0^2/|v_0|<=1/2`. The last estimate follows from `2^(r+1)-d>=1`, not from a printed lower bound on either tiny signal.

The cubic `P=-u^2 v` has full Hessian Gram `B` with constant entries `B_(z_a,z_a)=2kappa`, `B_(z_a,z_b)=B_(z_b,z_a)=2kappa` and cross entries `B_(z_a,X_b z_a)=-1`, `B_(z_b,X_a z_a)=-2`, together with symmetric mates. Its biform is exactly `-2(X_b-kappa)z_a^2-4(X_a-kappa)z_a z_b`. Distinctness of `a,b` avoids overlapping entries and is also used in the gradient norm. Its Frobenius norm is `sqrt(12kappa^2+10)<8`.

For the supplied positive definite Gram `M`, let `h=N+N^2`, `mu=det(M)/(tr M)^(h-1)` and `lambda=ceil(9/mu)`. The eigenvalue product bound gives `M>=mu I`; thus `lambda M+B>=I`. The rational matrix and `lambda` have polynomial bit length. Put `G=lambda F-u^2v`. It remains a quartic and has global Hessian at least identity, so its unique minimum exists.

At the old zero, `G(p)=-u_0^2 v_0` and `||grad G(p)||^2=4u_0^2v_0^2+u_0^4`. Positive `v_0` gives a negative minimum. For negative `v_0=-t`, strong convexity and completion of the square give

\[
\min G\ge G(p)-\tfrac12\|\nabla G(p)\|^2
=u_0^2(t-2t^2-u_0^2/2)\ge u_0^2t/2>0.
\]

Both branches are strict, so the same lower reduction serves strict and weak minimum comparisons. The perturbation gives no rational-minimizer promise.

The positive branch is in the rational SOS interior. Choose a rational center `q` near the minimizer with `c=G(q)-||grad G(q)||^2/2>0`. The Hessian Gram after subtracting `||X-q||^2/2` is at least `diag(0,I)`. Taylor integration uses

\[
\int_0^1(1-t)(U+tV)^2dt=\tfrac12(U+V/3)^2+(V/6)^2.
\]

It supplies all translated quadratic factors `d_i d_j`, where `d=X-q`. Completion adds affine factors `d_i+grad_i G(q)` and a positive constant. Their coefficient vectors span every polynomial of degree at most two, proving a positive definite ordinary rational polynomial Gram. A rational PSD matrix has rational weighted LDL squares; binary expansion of each positive rational weight converts it into rational unweighted squares. No polynomial expanded certificate bound follows from this existence argument. Flipping the integer input to `1-V` makes the original yes branch positive and proves membership hardness. This does not supply an equality lower bound or a general rational-SOS membership upper bound.

## 4. Cubic-root comparison upper bound

Source: `posslp-certified-cubic-root-upper.md`, lines 43--222. Its separation and Newton estimates are sound, including exact equality.

Let `L>=2` count the full printed encoding, so `n<=L`, each rational numerator/denominator has magnitude at most `2^L`, and the sum of denominator lengths is at most `L`. Positive interval endpoints give `2^-L<=xi_i<=2^L`. For the product `D` of denominators in gate coefficients and threshold, `D<=2^L` and `alpha_i=D xi_i` satisfies a monic equation over preceding algebraic integers:

\[
\alpha_i^3=D^3c_i+\sum_{j<i}(D^2a_{ij}\alpha_j+Db_{ij}\alpha_j^2).
\]

Every coefficient here is an integer. Thus all `alpha_i` are algebraic integers, by transitivity of integrality. The joint field degree is at most `3^n`. Every complex embedding satisfies `|xi_i|<=M=(2L+1)2^L<=2^(3L)` by triangular induction, since a radicand is bounded by `2^L(1+LM+LM^2)<=M^3`. Real interval bounds are not imposed on complex conjugates.

If `xi_o-r` is nonzero, `beta=D(xi_o-r)` is a nonzero algebraic integer. Its norm is a nonzero integer, and all other conjugate factors are at most `2^(4L+1)`. Consequently

\[
|\xi_o-r|\ge2^{-L-(4L+1)(3^L-1)}\ge2^{-2^{6L}}=:g.
\]

The gap is generated by `6L` squarings of `1/2`, not printed as an expanded fraction.

For a positive cube root `eta` in `[2^(-(L+1)),2^(L+1)]`, Newton from `x_0=2^(L+1)` gives

\[
x_{t+1}=(2x_t+z/x_t^2)/3,\quad
e_{t+1}={e_t^2(3+2e_t)\over3(1+e_t)^2}
\le\min(e_t^2,2e_t/3).
\]

All iterates are positive and above `eta`. After `4L+6` steps the relative error is at most `1/2`; after another `10L`, absolute error is at most `varepsilon=2^(L+1-2^(10L))`. The radicand approximation at gate `i` changes by at most `2^(4L) E_(i-1)`. If `E_(i-1)<=2^(-7L-1)`, its radicand remains positive and its cube root remains in the initialization interval. The cube-root derivative is at most `2^(2L+2)`. Thus

\[
E_i\le2^{6L+2}E_{i-1}+\varepsilon
\le2^{(6L+3)i}\varepsilon.
\]

The numerical inequalities displayed in the source hold for all `L>=2`, giving both `E_i<=2^(-7L-1)` and final `E_n<=g/8`. This is an inductive positivity proof, not an assumption that approximating a signed radicand preserves positivity.

The strict comparison output `q=widehat(xi_o)-r-g/2` is positive exactly when `xi_o>r`; equality gives a negative margin at least `3g/8`. Rational division is eliminated with positive denominators by

\[
(N_a,D_a),(N_b,D_b)\longmapsto(N_aD_bN_b,D_aN_b^2).
\]

All divisors are nonzero by the positivity proof. Sharing gives polynomial total circuit size despite enormous expanded fractions. Check topology, coefficient format, positive ordered intervals, and direct signed interval inclusions before construction; every invalid input maps to a fixed negative integer circuit. Hence this is an ordinary many-one completeness result for the checked language, not only a promise result.

## 5. Rational-optimizer coordinate hardness

Sources: `quaternion-circuit-posslp-reduction.md`, equations (4)--(22); `unit-quaternion-circuit-quartic-realization.md`, equations (3)--(14); and `rational-optimizer-posslp-coordinate-comparison.md`. The quaternion route is needed to preserve rationality; the cubic-root route does not establish that promise.

For a unit quaternion `q=(w,x,y,z)`, conjugations `T` and `R` give the exact projection

\[
P(q)=qT(q)=(1-2x^2,2wx,2xz,-2xy).
\]

The commutator identity

\[
[q,r]-1=2(0,v\times u)\bar q\bar r
\]

implies a norm bound `2||v||||u||` and, for nonnegative scalar parts, leading-term error at most `4||v||||u||(||v||+||u||)`. These are absolute estimates and include zero leading coefficients. Use `A(q,r)=P(qr)` and `M(q,r)=P(R([q,R(r)]))`.

The small-signal generator preserves `0<x<=2^-16`, `||(y,z)||<=64x^2`, positive scalar part, and gives `x^2<=x'<=6x^2`. The rotated cross product has selected leading coordinate `2(x^2-yz)`; the source's bounds `|U_x-2x^2|<=65x^3`, `||vec U||<=8x^2`, and transverse output norm `<=48x^4` all follow directly from the commutator estimate. Starting at the fixed rational unit constant `q_0`, after `j` generator steps, `0<x_j<2^(-16*2^j)`.

A signal with order `d`, integer coefficient `C`, and bound `B` obeys `||vec q-C delta^d e_1||<=B delta^(d+1)`. Under `B delta<=2^-30`, inversion, projection, equal-order addition, and multiplication preserve this property with new bound `2^20 B^4`. Their coefficient updates are respectively `-C`, `2C`, `2(C+D)`, and `4CD`. The inherited multiplication error is proportional to the product order; no nonzero coefficient or transverse-coordinate promise is required.

Represent each integer value by numerator/denominator leading coefficients `(C_i,D_i)` with `D_i>0` and `C_i=D_i V_i`. Multiplication gives the common factor four; cross-multiplied addition followed by projection gives the common factor eight. Count all signal operations in `T`, set `B_0=128`, `B_j=2^20 B_(j-1)^4`, so `log_2 B_j=(41*4^j-20)/3<14*4^j`. Generator depth `2T+2` gives `delta<2^(-64*4^T)<=2^-30/B_T`. The final numerator coefficient `D(2V-1)` is a nonzero integer, and its error is less than `delta^d/2`. Its selected rational coordinate is nonzero and has the required sign. Every raw gate is an exact rational unit quaternion, not merely a bounded approximation. Expanded coordinates are unnecessary.

For the quartic realization, one four-coordinate variable block per raw quaternion gate gives `N=4s`. Residuals are `X_i-c_i`, `X_i-X_a X_b`, and `X_i-bar(X_a)`. Their common zero is exactly the gate list. The Jacobian has identity diagonal blocks and determinant one. Each residual quadratic matrix has norm at most one, including repeated parents, whose square is `(w^2-x^2-y^2-z^2,2wx,2wy,2wz)`. Scalar residual gradient norms are at most three; a four-row gate Jacobian operator norm is also at most three by the sum of the identity and up to two orthogonal parent operators. Thus `V=4N`, `nu=V^(-(N-1))` suffice.

Let `q_i=|X_i|^2-1`. The exposing form is `E_i=q_i-2<p_i,r_i>` minus predecessor norm equations (`q_a+q_b` for multiplication, `q_a` for inversion). For multiplication,

\[
E_i=|X_i-p_i|^2-|X_a-p_i\bar X_b|^2
=|U_i|^2-|U_a-p_i\bar U_b|^2.
\]

This identity remains true when `a=b`. The negative term is bounded below by `-2(|U_a|^2+|U_b|^2)`, hence by `-4|U_a|^2` for repeated parents. With weights `omega_i=16^(-(i-1))`, each earlier block loses at most `4 sum_(i>j) omega_i<=4omega_j/15`. Consequently `(11/15)omega_* I<=H_*<=I`. Arbitrary fanout is covered by the geometric sum, not a distinct-parent assumption.

Approximate only the coefficients `p_i` multiplying residuals, so the zero is preserved exactly. Coordinate error `eta` gives `||H-H_*||<=8s eta`, `||ell||<=12s eta`. The stated `eta<=min(1,omega_*/(32s),epsilon/(16s))` gives `gamma I<=H<=2I`, `||ell||<=epsilon`, `gamma=omega_*/4`. Approximations are obtained by rounding each raw gate to a dyadic grid: multiplication error is at most `3e` while `e<=1`, and four-coordinate rounding adds at most `2h`. Thus every gate error is at most `h(3^s-1)`. A polynomial-bit grid `h<=eta/(2*3^s)` suffices without expanding exact fractions.

Apply the full Gram lemma from Section 2 with this data and `K_p<=N`. The resulting quartic has exactly the rational gate coordinates as its unique zero, minimum zero, `N+1` supplied rational square factors, full rational positive definite Hessian Gram, and Hessian at least `(3/2)I`. Coordinates lie in `[-1,1]`. Coordinate sign at threshold zero therefore preserves the PosSLP answer and all promises. The general upper bound below applies without requiring rationality. Recognizing rationality of an arbitrary optimizer is outside the theorem.

## 6. Strong-convexity upper bounds, including variable degree

Sources: `strong-convex-quartic-posslp-upper.md`, equations (5)--(18), and `strong-convex-polynomial-posslp-upper.md` in the assigned October 3 directory. These arguments are sound conditional on the stated standard bit-model approximation and effective one-block quantifier-elimination results. The literature agent should certify their exact source versions; I did not perform source research.

Inputs are explicitly listed rational polynomials `f,h`, positive rational `mu`, and a promise `Hessian f>=mu I` on all real points. In the general theorem, degrees are at most `L` under unary bounds. Include coefficients, exponent lists, dimension, and curvature number in `L`. For a derived determinant/trace curvature bound, enlarge `L` after computing it; its length is polynomial in the original encoding. A sparse dimension field alone does not force `n<=L` on malformed inputs. In the checked language, reject impossible dimensions/list lengths before allocating matrices; valid strongly convex polynomials contain a nonzero square coefficient for every variable at the origin, so there are at least `n` explicit monomials.

Strong monotonicity gives `||p||<=||grad f(0)||/mu<=2^(3L)`. Set `R=2^(4L)`. For quartics, `B=2^(20L)` bounds scalar values, gradient norms, Hessian norms, and Hessian Lipschitz constants for both `f` and `h` on that ball. For degrees at most `L`, `B=2^(16L^2)` does so: a derivative component of order `j<=3` is bounded by `2^(2L) L^j R^L`, and the tensor Frobenius factor is at most `L^(j/2)`. The combined logarithmic bound is below `16L^2`. Define `rho=mu/(4B)` and `epsilon_0=mu^3/(32B^2)`. Additive objective accuracy `epsilon_0` puts a rational initial point inside the radius-`rho` Newton neighborhood by strong convexity. The ball lies strictly within the radius-`R` ball.

The manuscript must state the bit-model convex approximation theorem used here, including explicit sparse encoding and polynomial dependence on degree and requested precision. Only polynomially many ordinary accuracy bits are requested. A standard rational ellipsoid weak-optimization theorem with the displayed search radius and gradient separation oracle is an alternative; no doubly exponential precision or PosSLP oracle is used for the initial point. The cited approximation corollary, if used, must be the convex result. A nonconvex reading of the source's separate proposition is not needed.

Exact Newton iterations satisfy

\[
e_{t+1}\le{B\over2\mu}e_t^2,\qquad
e_t\le{2\mu\over B}\,2^{-3\,2^t}.
\]

The integral Taylor identity proves the first estimate. It also keeps every iterate in the same neighborhood. Hessians are positive definite; rational LDL elimination without pivoting has nonzero positive pivots. A fixed branch-free circuit implements every step. Sparse differentiation creates polynomially many terms, and degree at most `L` permits their evaluation by polynomially many arithmetic gates. Share all prior Newton wires. Expanded fractions need not have polynomial length.

For `alpha=h(p)`, the real formula `exists X: grad f(X)=0 and z=h(X)` defines the singleton `{alpha}`. Clear denominators to get polynomial coefficient bits. A standard one-block quantifier-elimination theorem, with one free variable, gives degrees and coefficient bit lengths bounded by `2^(a(L))` for a fixed effective polynomial `a`. For variable degree, `n log D<=L log L` is polynomial; any additional polynomial input-count factors are absorbed in `a`. The proof must state an effective universal majorant, for example `a(L)=C L^C+32L^2+40L+10` for a sufficiently large fixed effective integer `C` supplied by that theorem. It is fixed once for the reduction, not chosen by inspecting the unknown optimizer. The reduction does not execute quantifier elimination.

At least one nonzero polynomial in the resulting univariate description vanishes at `alpha`: otherwise every sign test is locally constant, so the Boolean formula would define a neighborhood instead of a singleton. Removing the largest power of `z` leaves a nonzero integer constant coefficient. For a nonzero root of magnitude below one, `1<=degree*height*|alpha|`. Therefore

\[
\alpha\ne0\implies |\alpha|\ge2^{-2^{a(L)+1}}=:g.
\]

This argument uses the real singleton and does not assume that the complex gradient variety is zero dimensional. The source's example `(x^2+y^2)^2+x^2+y^2` indeed has a positive definite real Hessian while its complex critical locus contains a curve.

Generate `g` with `a(L)+1` squarings. After `k=a(L)+2` Newton steps,

\[
|h(x_k)-\alpha|\le B e_k
\le 2\mu\,2^{-12\,2^{a(L)}}\le g/8.
\]

This stronger bound explicitly cancels `B`; it also justifies the displayed general-degree estimate whose exponent lacks a separate `16L^2` term. The quartic note uses a more conservative estimate and remains correct.

With `widehat alpha=h(x_k)`, the five rational outputs

\[
\widehat\alpha-g/2,\quad\widehat\alpha+g/2,\quad
-\widehat\alpha-g/2,\quad-\widehat\alpha+g/2,\quad
g^2/4-\widehat\alpha^2
\]

are positive exactly for `alpha>0`, `alpha>=0`, `alpha<0`, `alpha<=0`, and `alpha=0`, respectively. The gap plus `g/8` error proves every case, including exact zero; the selected rational output is nonzero on every valid input. Positive-denominator division elimination then produces one PosSLP instance.

For a checked Hessian certificate, verify symmetry, rational format, topology/list dimensions, the coefficient identity, and positive definiteness before deriving `mu=det(M)/(tr M)^(m-1)`. In the general certificate format, the listed monomial vector must be linear in `v` and contain every `v_i`; then `||w(X,v)||^2>=||v||^2`. Sparse expansion of at most `m^2` products checks the identity in polynomial time. A semantic curvature promise cannot be rejected in this way without a certificate. On malformed certified inputs, return a fixed negative PosSLP circuit for every comparison language, including equality.

The strict and weak value/coordinate completeness statements follow from the restricted quartic lower bounds. Equality has the proved upper bound; none of the lower reductions discussed here proves equality hardness. The two-objective minimum comparison uses a disjoint-block sum for the objective and their difference for the observable. Separate curvature bounds suffice; a full positive definite Gram on the combined tensor basis is not implied by block separation. Strict feasibility gives a polynomial-size rational-circuit point, not necessarily a polynomial-size expanded rational point.

## 7. Boolean and adaptive closure

Sources: `research-20260928/algebra/posslp-boolean-closure-audit.md` and `adaptive-integer-sign-circuit-compilation.md`, especially the latter lines 78--203. Both proofs are valid. They should be supporting lemmas with restrained novelty language.

For `F_M(x)=2Mx/(M+x^2)`, if `1<=|x|<=M`, the sign is preserved and `1<=|F_M(x)|<=sqrt M`. A short proof of the lower bound is convexity of `t^2-2Mt+M` and its nonpositive values at `t=1,M`; the upper bound follows from AM--GM. With `M_j=2^(2^j)`, successive maps `F_(M_N),...,F_(M_1)` reduce magnitude to `[1,2]` in `N` stages. Generate the constants by sharing repeated squares.

For a fixed list of integer circuit outputs, use `2a_i-1`, which is nonzero and has the same positivity bit. A total `n`-gate circuit has height at most `2^(2^n)`; `N=n+2` is sufficient. On normalized signed values, `2(u+v)-3` implements AND and `2(u+v)+3` implements OR with absolute value between one and eleven. Applying `F_16` then `F_4` restores `[1,2]`; negation is `-u`. This is exact sign processing with no depth-dependent approximation. For a pair `(P,Q)`, `Q>0`, the compressor becomes `(2MPQ,MQ^2+P^2)` and Boolean addition uses positive denominator products. The final numerator has the desired sign. The result is for a polynomial explicit Boolean circuit and a polynomial explicit query list.

For adaptive closure, start with a binary integer arithmetic circuit of total size `S`, including Boolean inputs, constants, decoder/control arithmetic, and threshold gates `H(v)=1[v>0]`. Assume its designated output is Boolean on Boolean inputs. All exact intermediate values are integers and bounded by `B=2^(2^S)`. Define the error amplification bound `Lambda=3B` and budget `epsilon=2^(-2^(2S+4))`; then `epsilon Lambda^S<1/4` for every `S>=1`.

At a threshold gate, form `x=4 tilde(v)-2`. If the inherited error is at most `1/4`, integer separation gives `|x|>=1` with the exact threshold sign, and `|x|<=4B+3<=B^4=M_(S+2)`. Compress to magnitude `[1,2]`, then apply `G(x)=2x/(1+x^2)` exactly `2S+5` times. The first refinement gives magnitude at least `4/5`; every later error from sign squares because `1-G(t)=(1-t)^2/(1+t^2)`. The final `(1+z)/2` approximates the threshold bit with error at most `epsilon` and lies in `[0,1]`.

After gate `i`, maximum error is at most `epsilon Lambda^i`: addition/subtraction amplify error by two, multiplication by at most `2B delta+delta^2<=Lambda delta`, and a threshold replacement resets its own error to `epsilon`. The global budget validates the threshold margin at every step. Approximate decoder outputs need not be exact bits: all their original arithmetic gates are already included in this same induction. The final Boolean output is within `1/4` of zero or one. Pair arithmetic keeps all compressor/refinement denominators positive and yields final test numerator `2P-Q`. Size is `O(S^2)` with sharing.

For an oracle Turing machine with polynomial time/query bound `T`, unroll its Boolean configurations. At each time slot include a bounded query module whose answer is ignored when no query occurs. Parse its potentially answer-dependent query description with a Boolean circuit, reserve polynomially many instruction slots, compute address/opcode indicators, and select operands by sums of prior slot values times address bits. Unavailable addresses select zero, so every malformed query still gives defined arithmetic; conjoin the threshold result with a validity bit. Candidate arithmetic is selected with Boolean arithmetic. This enumerates addresses, not complete answer transcripts, and therefore costs polynomial size. Include all parser, decoder, selector, output-selection, and machine-control gates in `S` before applying the adaptive compiler. Hardwiring the ordinary input yields the single PosSLP instance. The construction establishes many-one completeness for `P^PosSLP` under these standard conventions; it is not an ordinary polynomial-time algorithm for PosSLP.

## 8. Circuit interior Grams

Source: `research-20261003-arithmetic/reviews/exact-core/general-degree/circuit-interior-gram.md`. Its result is valid and specifically needs the full strict quartic Hessian basis.

For the supplied full Gram `A`, compute `mu=det(A)/(tr A)^(m-1)`. The explicitly expanded observable `h=f-||grad f||^2/(2mu)` has degree at most six and polynomial input length, so use the variable-degree upper theorem, not only the degree-four observable theorem. At the minimizer, `h(p)=f(p)`. Its Newton circuit gives an exact rational center `q` with `|h(q)-h(p)|<=g/8`, independently of the minimum's sign. If `min f>0`, `c=h(q)>0`.

With `d=X-q`, `b=grad f(q)`, and `bar A=A-mu diag(I,0)`, let coefficient matrices in the full ordinary quadratic monomial basis `z` represent

\[
U=(d,q\otimes d),\quad V=(0,d\otimes d),\quad d+b/\mu.
\]

The exact circuit Gram is

\[
Q=\tfrac12(C_U+C_V/3)^T\bar A(C_U+C_V/3)
+\tfrac1{36}C_V^T\bar A C_V
+\tfrac\mu2 C_{\rm aff}^T C_{\rm aff}+c e_0e_0^T.
\]

Taylor integration and completion give `f=z^T Q z` on every valid input. No approximation enters this identity because the circuit center denotes an exact rational vector. Every divisor remains nonzero even when the minimum is zero or negative. The bound `bar A>=mu diag(0,I)` supplies every translated homogeneous quadratic through the second summand; the affine factors and positive constant complete a spanning family. Hence `Q` is positive definite if `min f>0`. Conversely, a positive definite full polynomial Gram would imply `f(X)>0` everywhere, since `z` contains one; strong convexity gives an attained minimum, so such a Gram is impossible when `min f<=0`.

Polynomial matrix dimensions and shared Newton references give polynomial total circuit size. This proves neither efficient ordinary-bit validation nor a short unweighted rational SOS circuit. Binary expansion of a circuit-encoded weight may have exponentially many terms. The proof also does not extend to an arbitrary incomplete Hessian monomial vector: the full quadratic spanning step is essential.

## 9. Strongly monotone cubic zeros

Source: `research-20260927/strong-monotone-cubic-posslp-upper.md`, lines 54--294; the local `monotone-warm-start-ellipsoid-source-audit.md` explains the rational rounded ellipsoid interface. I checked the mathematical application, including the retained common ball; the literature agent should verify the GLS source interface.

Let the explicitly encoded cubic map `T` satisfy global strong monotonicity with a supplied positive rational modulus `mu`. Differentiating the monotonicity inequality gives `sym J_T>=mu I`; conversely, integration proves monotonicity from this differential condition. Although `J_T` need not be symmetric, Cauchy--Schwarz applied to `v^T J_T v>=mu||v||^2` gives `||J_T v||>=mu||v||`. Thus every Jacobian is invertible and its inverse norm is at most `1/mu`.

Existence is part of the theorem, not a separate zero-existence promise. For a radius `s>||T(0)||/mu`, every boundary point satisfies `T(x)^T x>0`. Apply Brouwer to the map `x -> projection_to_ball(x-T(x))`. A fixed point satisfies the projection variational inequality `T(x)^T(y-x)>=0` for every point in the ball. Choosing `y=0` excludes the boundary; at an interior fixed point, choosing both signs of every sufficiently small direction forces `T(x)=0`. Strong monotonicity gives uniqueness and `||p||<=||T(0)||/mu<=2^(3L)`.

The explicit bounds `R=2^(4L)`, `Q=[-R,R]^n`, `B=2^(30L)`, and `rho=mu/(4B)` are conservative and valid. On the radius-`nR` ball, `B` bounds the map norm, Jacobian norm, Jacobian Lipschitz constant, and observable gradient. Derivative coefficient factors of three, six, and four together with `nR<=2^(5L)` fit this exponent for every `L>=2`. The radius-`rho` neighborhood of the zero lies strictly inside `Q`.

At a rational query point outside `Q`, give the coordinate central cut retaining `Q` before applying any bounded-domain map estimate. Inside `Q`, evaluate `T` exactly and accept if `||T(x)||^2<=(mu rho)^2`. Acceptance implies `||x-p||<=rho`. For a failed test, the Jacobian bound gives `||T(x)||<=B||x-p||`, and thus

\[
T(x)^T(p-x)\le-\mu\|x-p\|^2
<-\mu^3\rho^2/B^2.
\]

The normal `T(x)` is nonzero. Set

\[
\delta={\mu^3\rho^2\over2B^3}={\mu^5\over32B^5}.
\]

For every `y` with `||y-p||<=delta`, the cut expression changes by at most `B delta`, which is only half the strict margin above. Consequently every failed query retains the same ball `B(p,delta)`, and this ball lies inside `Q` because `delta/rho=mu^4/(8B^4)<1`. Merely retaining the point `p`, or different balls at different queries, would not suffice; the fixed-radius proof is essential and is present.

Run the rational rounded central-cut ellipsoid algorithm from the radius-`nR` ball with terminal volume `nu=(delta/n)^n/2`. A cube of side `delta/n` centered at `p` lies in the retained ball, so its volume exceeds `nu`. Each nonaccepting cut retains this common set, so the algorithm cannot reach its prescribed small-volume alternative. It must accept in polynomial bit time. The routine need not decide membership in the unknown retained ball; it only needs the cut-or-stop containment consequence of the ellipsoid proof. Normalize the rational cut normal to infinity norm one after evaluation. Use the rounded algorithm with enlargement and its containment theorem, not arbitrary rounding of ideal ellipsoid updates. In dimension one, rational interval bisection gives the same result directly.

Newton then uses `x_next=x-J_T(x)^(-1)T(x)`. The same integral identity as in the gradient case gives `e_next<=B e^2/(2mu)` and the same doubly accurate shared rational circuit. To obtain a branch-free linear solve, form the positive definite normal system `J^T J d=J^T T(x)` and use rational LDL elimination. Its solution is exactly `J^(-1)T(x)`; symmetric elimination must not be applied directly to a nonsymmetric `J`. The normal-equation condition number does not affect symbolic circuit size.

The formula `exists x: T(x)=0 and z=h(x)` defines a real singleton, so the earlier effective quantifier-elimination separation and five final predicates apply verbatim. The checked full Gram format represents only `v^T J_T(x)v`, hence only its symmetric part; this is sufficient for the modulus by integration. Verify the exact biform identity, matrix symmetry, dimensions, and positive definiteness, derive the curvature bound, enlarge `L`, and reject invalid certificates before circuit construction. The gradient quartic examples supply matching order-comparison lower bounds. No equality lower bound or constrained variational-inequality upper bound follows.

The degree frontier is also valid: for a globally strongly monotone quadratic map, its symmetric Jacobian is affine and positive definite on every line, so all linear coefficients vanish. Subtract the constant symmetric linear part to obtain a field `U` satisfying `partial_i U_j+partial_j U_i=0`. Differentiate the three pair identities and combine them to get `2 partial_i partial_j U_k=0`. Hence the map is affine. Cubic degree is the first possible degree in this hardness chain.

## 10. Known-value binary extraction and the full joint Gram refinement

Source: `research-20260928/algebra/binary-extraction-known-value.md`, lines 14--170. Both variants are sound, but their certificate promises must be kept distinct.

Use the rational-optimizer reduction to obtain `F>=0`, unique zero `p` in `Q^N intersect [-1,1]^N`, `Hessian F>=(3/2)I`, and designated `p_j!=0`. Consider one integer variable `z`, constraints `0<=z<=1`, `z-1<=x_j<=z`, and objective `H=F(x)+(z-1/2)^2`. Every feasible objective is at least `1/4`. Exactly one of the two fibers contains `p`, and equality forces `x=p`, so the unique mixed optimizer is `(p,1[p_j>0])`. Both fibers are nonempty because `x=0` is feasible for either bit; each fiber is closed and coercivity gives attainment. The losing value is strictly larger than `1/4`. The known exact value and one-bit output do not avoid the coordinate comparison.

Only two constraint normals involve continuous variables, namely `e_j` and `-e_j`, so the continuous matrix rank is exactly one. Do not add full continuous box constraints when stating that rank. The optimizer is bounded; the feasible domain is generally unbounded. The losing fiber's optimizer need not be rational. The extraction question is a promised unique-optimizer decision predicate, rather than recognition of uniqueness or of the supplied optimum value.

The objective has global curvature at least `3/2` and short rational square factors. If the source full Gram is `Q`, put `rho=det(Q)/(tr Q)^(d-1)` and `eta=min(1,rho/2)`. Subtracting `eta` on its constant direction block leaves a rational PSD Gram, and the scalar `2-eta` gives a strong SOS certificate for `H-(eta/2)||(x,z)||^2`. This certificate modulus is not necessarily `3/2`. It is impossible for this basic objective to have a positive definite Gram on the full joint basis: at `x=0` in the pure `z` direction, the biform is the constant two, while the full basis includes the growing coordinate `z s`. A positive definite Gram would force growth with `z^2`.

The correction restoring a full joint positive definite Gram is

\[
\widehat H=F(x)+(z-1/2)^2
+\epsilon z(z-1)\|x\|^2+\tfrac14 z^2(z-1)^2,
\quad \epsilon=\min\{\rho/4,1/(100N)\}>0.
\]

It leaves every integer-fiber objective value unchanged, because both added terms vanish at the only allowed integers zero and one. Thus the known optimum, unique rational bounded mixed optimizer, one binary variable, and rank one are unchanged.

Write `t=z-1/2` and group the full joint Hessian basis as `(w,s,tv,xs,ts)`, where `w=(v,x tensor v)`. Its length is `N+N^2+1+N+N+1=(N+1)(N+2)`, exactly the full direction-and-coordinate-times-direction dimension. Differentiation gives the additional biform

\[
-\tfrac\epsilon2\|v\|^2+2\epsilon t^2\|v\|^2
+2\epsilon\|x\|^2s^2+8\epsilon t(x^Tv)s
+\tfrac74s^2+3t^2s^2.
\]

Let `E` project onto the constant direction part of `w`, and let `d_0` be supported on `x tensor v` with `d_0^T w=x^T v` and `||d_0||^2=N`. The Gram has diagonal blocks `A=Q-epsilon E/2`, `7/4`, `2epsilon I`, `2epsilon I`, `3`, and the sole added cross block `b=4epsilon d_0` between `w` and `ts`. Since `A>=rho I/2`,

\[
b^T A^{-1}b\le32\epsilon^2N/\rho
\le8\epsilon N\le2/25<3.
\]

The Schur complement is positive and all other diagonal blocks are positive. This proves full-space Gram positive definiteness. Replacing `tv` by `zv-v/2` and `ts` by `zs-s/2` is an invertible rational full-basis congruence. Matrix dimensions, entries, the derived positive modulus, and all construction steps have polynomial binary size. No optimizer coordinates are used in constructing the correction.

Global positivity follows separately. Since `F(x)>=3||x-p||^2/4`, `||p||^2<=N`, and `||x||^2<=2||x-p||^2+2||p||^2`,

\[
F(x)-\epsilon\|x\|^2/4\ge-\epsilon N/2.
\]

For `u=t^2>=0`, `u+(u-1/4)^2/4>=1/64`. Dropping the nonnegative `epsilon t^2||x||^2` gives `widehat H>=1/64-epsilon N/2>=17/1600>0`. The leading `z^4` coefficient is `1/4`, so its degree is exactly four. The refined promise supplies a full positive definite Hessian Gram and some positive rational global modulus. It does not retain the specific `3/2` modulus or a supplied short objective SOS factorization. In particular, the signed correction term cannot simply be added to the base SOS factors as a square.

There is no inverse-polynomial branch-gap promise in either reduction. In the base version, the losing gap is at least `3p_j^2/4`; the feasible boundary point `p-p_j e_j` gives upper bound `M p_j^2/2`, where `M` is the Hessian norm bound on the unit box. This explains why fixed objective accuracy does not imply correct binary extraction. A polynomial-time exact extraction algorithm in either promised class would put PosSLP in P; no unconditional exclusion of such an algorithm, NP-hardness claim, or practical numerical lower bound follows.

## 11. Verification record and handoff

All mathematical checks in this audit were analytic reconstruction and source-note inspection. No finite calculation was treated as proof. Historical symbolic and rational checks were read only as recorded evidence; none was rerun. The targeted documentation commands actually run for this report were:

```text
git diff --check -- paper-exact-arithmetic/evidence/reviews/prewrite-reductions.md
git diff --no-index --check /dev/null paper-exact-arithmetic/evidence/reviews/prewrite-reductions.md
```

Both produced no whitespace diagnostics. The second explicitly checks the contents of this new, untracked file; the first alone would not establish that. These are whitespace checks, not mathematical tests, compilation, or CI results. No project-wide verification or CI inspection was performed.

The writers may use the proof chain above without an unresolved mathematical assumption. They still need the literature agent's vetted statements for polynomial-time convex approximation, effective one-block quantifier elimination, and the rounded ellipsoid cut-or-stop result, and must include those statements with the assumptions used here. No other new source dependency is needed for the reductions. The safest presentation gives the abstract quartic/full-Gram lemma once, then the cubic-root and quaternion realizations as two applications, followed by the separate perturbation and common Newton upper theorem. The strongly monotone extension adds its independent warm-start proof; the binary extraction corollary adds the full joint correction without importing the base variant's stronger objective-certificate promises.
