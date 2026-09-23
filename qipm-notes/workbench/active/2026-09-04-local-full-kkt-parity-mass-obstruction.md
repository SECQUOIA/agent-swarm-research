# Local full-KKT parity--mass obstruction

Status: Proved; independently algebra-checked  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorem; moderate-to-high on apparent novelty  
Question: Can any nonorthogonal bounded local gadget close the paper's
bounded-scale full-KKT parity-amplifier problem?

## Theorem

For each \(\sigma\in\{\pm1\}^N\), let
\((u_\sigma,v_\sigma,z_\sigma)=(\Delta x,\Delta y,\Delta s)\) solve

\[
 A_\sigma u_\sigma=r_p,\qquad
 A_\sigma^Tv_\sigma+z_\sigma=r_d,\qquad
 S_\sigma^0u_\sigma+X_\sigma^0z_\sigma=r_c,
\]

with common public right-hand sides. Assume:

1. \(a\leq(X_\sigma^0)_{ii},(S_\sigma^0)_{ii}\leq b\);
2. \(|(A_\sigma)_{ij}|\leq B\), and the union support of \(A_\sigma\) has
   row and column degrees \(d_r,d_c\);
3. every position of \(A,X^0,S^0\) depends on at most one input bit;
4. a fixed symmetric contraction \(Q\) decodes parity with margin \(\delta\):

\[
 \chi(\sigma)u_\sigma^TQu_\sigma
 \geq\delta\|u_\sigma\|^2,
 \qquad \chi(\sigma)=\prod_j\sigma_j;
\]

5. the primal block has mass at least \(\eta\) in the normalized complete
   direction:

\[
 \|u_\sigma\|^2\geq
 \eta(\|u_\sigma\|^2+\|v_\sigma\|^2+\|z_\sigma\|^2).
\]

Put \(\kappa_\eta=\sqrt{\eta^{-1}-1}\). Then

\[
 \boxed{
 N\leq\frac{8}{(a/b)\delta^2}
 \left[B\sqrt{d_rd_c}\,\kappa_\eta
 +\frac ba(1+\kappa_\eta)\right].
 }
\]

Thus fixed scale, coefficient bound, local degree, decoder margin, and primal
mass permit only \(N=O(1)\). No arbitrarily large bounded-scale local parity
amplifier exists, even without assuming linear dimension, orthogonal copies,
cut structure, or coordinatewise bounded directions. This closes open problem
F1 under its natural one-bit-local public-source interpretation.

## Cross-instance work identity

For neighbors \(\tau=\sigma^j\), set

\[
 q=u_\tau-u_\sigma,\quad E=A_\tau-A_\sigma,\quad
 U=X_\tau^0-X_\sigma^0,\quad V=S_\tau^0-S_\sigma^0.
\]

Cross-pairing primal feasibility with dual stationarity and subtracting the
complementarity equations gives the exact identity

\[
 \boxed{
 q^T(X_\tau^0)^{-1}S_\tau^0q
 =(Eu_\tau)^Tv_\sigma-(Eu_\sigma)^Tv_\tau
 -q^T(X_\tau^0)^{-1}(Vu_\sigma+Uz_\sigma).
 }
\]

Opposite parity and the fixed-observable margin imply

\[
 \|q\|\geq\frac\delta2(\|u_\sigma\|+\|u_\tau\|).
\]

Sum the boxed identity over all oriented Boolean-cube edges. With

\[
 P^2=\sum_\sigma\|u_\sigma\|^2,\quad
 D^2=\sum_\sigma\|v_\sigma\|^2,\quad
 Z^2=\sum_\sigma\|z_\sigma\|^2,
\]

the positive left side is at least

\[
 \frac ab\frac{\delta^2N}{2}P^2.
\]

One-bit locality makes the changed-entry sets disjoint across bits.
Cauchy--Schwarz on those entries and the union support gives

\[
 \sum_{\sigma,j}|\text{two }E\text{-terms}|
 \leq4B\sqrt{d_rd_c}\,PD.
\]

The two start-variation terms contribute at most

\[
 4\frac ba(P^2+PZ).
\]

Finally \(D/P,Z/P\leq\kappa_\eta\), proving the theorem. The cross-work
identity was also checked numerically on random nonsymmetric sparse KKT
systems.

## Stronger public-start law

If \(X^0,S^0\) are input-independent, the last two terms vanish. With

\[
 \rho=\lambda_{\min}((X^0)^{-1}S^0),
\]

one obtains

\[
 N\leq
 \frac{8B\sqrt{d_rd_c}}{\rho\delta^2}\frac DP,
\]

or equivalently

\[
 \frac DP=\Omega\!\left(
 \frac{\rho\delta^2N}{B\sqrt{d_rd_c}}
 \right).
\]

Hence some input has a large dual/primal direction ratio, and uniform constant
primal mass forces \(\rho=O(1/N)\), coefficient/degree growth, or a vanishing
decoder margin. This matches the repository's dual-homogeneity escape
\(\rho=\Theta(1/N)\) and the \(\Theta(N)\) multiplier growth of unscaled
copy/rotation gadgets.

## Scope and novelty

The existing local work identity is same-instance; earlier cut, signed-copy,
and orthogonal-copy theorems require special gadget structure. This theorem is
an adjacent-matrix identity aggregated over the whole Boolean cube and covers
arbitrary nonorthogonal mixed modes. Searches of the local corpus and targeted
KKT-sensitivity literature found no matching parity norm-ratio theorem. The
result is therefore apparently new, but priority is not guaranteed.

The material escape is a nonlocal input dependence in the start, RHS, decoder,
or recovery map. Such an object can already contain parity and its construction
must be charged; the theorem intentionally does not pretend otherwise.

## Product symmetric-cone extension

The identity is not specific to diagonal LP complementarity. On a real Hilbert
cone space, let

\[
 \mathcal A_\sigma u=r_p,qquad
 \mathcal A_\sigma^*v+z=r_d,qquad
 \mathcal C_\sigma u+\mathcal D_\sigma z=r_c.
\]

For adjacent inputs, the same subtraction gives

\[
 \langle q,\mathcal D_\tau^{-1}\mathcal C_\tau q\rangle
 =\langle Eu_\tau,v_\sigma\rangle-
  \langle Eu_\sigma,v_\tau\rangle-
 \langle q,\mathcal D_\tau^{-1}
 (\Delta C\,u_\sigma+\Delta D\,z_\sigma)\rangle.
\]

If
\(\operatorname{sym}(\mathcal D^{-1}\mathcal C)\succeq\rho I\), local
changes obey norm bounds \(L_C,L_D\), and all other locality hypotheses are
unchanged, hypercube aggregation yields

\[
 \boxed{
 N\leq
 \frac{8B\sqrt{d_rd_c}(Y/P)+4L_C+4L_D(Z/P)}
 {\rho\delta^2}.
 }
\]

For a product Euclidean Jordan algebra at an exact central point,
\(x\circ s=\mu e\), raw complementarity has
\(\mathcal C=L_s,\mathcal D=L_x\), and Peirce decomposition gives

\[
 L_x^{-1}L_s=\mu P(x^{-1})\succ0.
\]

If \(ae\preceq x,s\preceq be\), this operator lies between
\((a/b)I\) and \((b/a)I\). A public central start has \(L_C=L_D=0\); an
input-dependent one-bit-local block start has
\(L_C,L_D\leq2b/a\). The LP theorem and constants therefore extend to every
product symmetric cone, including SOCP and SDP blocks.

Nesterov--Todd scaling similarly produces the SPD metric \(F^*F\). The result
applies when \(F\) is public/common or its block-local input dependence is
charged. An arbitrary input-dependent dense scaling can destroy locality and
is outside the theorem.

Coercivity is essential. On \(\mathbb S_+^2\), take

\[
 X=\operatorname{diag}(1,10),\qquad
 S=\begin{bmatrix}11/2&9/2\\9/2&11/2\end{bmatrix}.
\]

Both have spectrum \(\{1,10\}\), yet for the symmetric direction
\(Q=\left[\begin{smallmatrix}-2&4\\4&-5\end{smallmatrix}\right]\),

\[
 \langle Q,L_X^{-1}L_SQ\rangle_F=-7/44.
\]

Thus raw AHO/Jordan scaling away from centrality need not be positive even
with bounded positive primal and slack matrices. Exact centrality restores
commutation; NT scaling restores positivity but may sacrifice locality. This
counterexample already transfers to \(\mathcal Q_3\cong\mathbb S_+^2\).
