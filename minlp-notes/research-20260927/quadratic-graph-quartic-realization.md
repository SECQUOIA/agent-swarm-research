# Polynomial-size quartic realization of the quadratic graph of a zero

Date: 2026-09-28. Status: quantitative construction and its field
consequence passed a [fresh independent review](quadratic-graph-quartic-realization-review.md).
This supersedes the exploratory candidate of the same name.
Publication priority remains unestablished.

**Theorem.** Let \(n\ge1\). A rational quartic \(f\) is promised
to have minimum zero and is supplied with a rational positive definite
full Hessian Gram \(A\) on \((a,y\otimes a)\). In deterministic
polynomial time in this expanded input, one can construct a rational
SOS quartic \(B(y,z)\) whose unique zero is
\[
 w_*=(p,(p_ip_j)_{1\le i\le j\le n}),                 \tag{1}
\]
where \(p\) is the minimizer of \(f\). The algorithm also returns
a positive definite rational full Hessian Gram for \(B\), with
\(\nabla^2B\succeq I\). The quartic and both certificates have
polynomial total bit length. The number of variables is
\(N=n+n(n+1)/2\). Neither \(p\) nor its minimal polynomial is
expanded. The zero-minimum promise is not decided by this algorithm.

The established ingredients are approximate convex optimization and
the reviewed small-gradient exposing-quadratic Hessian construction.
The additional step is a rational quadratic lift that vanishes exactly
at (1) while its gradient can be made small by approximation.

## 1. Quantitative data and rational approximation

Put \(h=n+n^2\) and
\[
 \rho=\frac{\det A}{(\operatorname{tr}A)^{h-1}},\quad
 U=\operatorname{tr}A,\quad
 P=1+\frac{\|\nabla f(0)\|_1}{\rho}.                 \tag{2}
\]
Then \(A\succeq\rho I\) and \(\nabla^2f\succeq\rho I\).
The unique minimizer satisfies \(\|p\|\le P\), since strong
monotonicity gives
\(\rho\|p\|^2\le-\nabla f(0)^{\mathsf T}p\).
Every rational bound in (2) has polynomial bit length.

For rational \(0<\eta\le1\), a rational point \(q\) with
\(\|q-p\|\le\eta\) can be computed in time polynomial in the
input and \(\log(1/\eta)\). Apply
[Slot, Steurer, and Wiedmer, *Hesse's Redemption*, Corollary 1.2](https://arxiv.org/html/2511.03440v1)
to \(f\) on \([-P-1,P+1]^n\), with objective tolerance
\(\min\{1,\rho\eta^2/2\}\). Strong convexity implies
\[
 \frac\rho2\|q-p\|^2\le f(q)-f(p)\le\frac\rho2\eta^2.
                                                               \tag{3}
\]
The source's Proposition 3.2 and Appendix D supply the rational
bit-model ellipsoid implementation. The box has polynomial encoding
and contains the minimizer. No exact feasibility or exact-minimum
oracle is used.

## 2. Exact exposing quadratics with uniform bounds

Let \(m=n(n+1)/2\), and let \(C\) duplicate symmetric entries,
so \(C(y_i y_j)_{i\le j}=y\otimes y\). Its singular values lie
between \(1\) and \(\sqrt2\). For rational \(q\), introduce
invertible affine coordinates
\[
 d=y-q,\qquad s_{ij}=z_{ij}-q_i y_j-q_j y_i+q_iq_j.       \tag{4}
\]
On the graph they satisfy \(s_{ij}=d_i d_j\). Define
\[
 \begin{aligned}
 G_q(y,z)={}&f(q)+\nabla f(q)^{\mathsf T}d\\
 &+\int_0^1(1-t)
 \begin{pmatrix}d\\q\otimes d+tCs\end{pmatrix}^{\mathsf T}
 A\begin{pmatrix}d\\q\otimes d+tCs\end{pmatrix}\,dt.
 \end{aligned}                                                   \tag{5}
\]
The integral uses only \(1/2,1/6,1/12\), so \(G_q\) is a
rational quadratic. Taylor's identity gives the exact restriction
\[
                   G_q(y,(y_iy_j))=f(y).                         \tag{6}
\]
Thus \(G_q(w_*)=0\) for every rational \(q\).

The following bounds hold uniformly for \(\|q-p\|\le1\):
\[
 J=4(P+2),\quad m_0=\frac{\rho}{48J^2},\quad
 L_0=10U(P+2)^2J^2,\quad K=2P^2.                                \tag{7}
\]
The graph point has norm at most \(K\). The quadratic-part matrix
\(H_q\) of \(G_q\) satisfies
\[
                       m_0I\preceq H_q\preceq L_0I.             \tag{8}
\]
Indeed, the integrated Euclidean form on
\((d,q\otimes d,Cs)\) has matrix
\[
 \tfrac12I_n\ \oplus\
 \left(\begin{pmatrix}1/2&1/6\\1/6&1/12\end{pmatrix}
                                  \otimes I_{n^2}\right).
\]
The scalar block has determinant \(1/72\) and trace \(7/12\),
so its least eigenvalue is at least \(1/42>1/48\). Hence the
integral is at least \(\rho(\|d\|^2+\|s\|^2)/48\).
The linear parts of (4) and its inverse have norms at most
\(2+2\|q\|\le J\), proving the lower bound. For the upper
bound, use \(\|A\|\le U\), \(\|q\|\le P+1\),
\(\|C\|^2\le2\), and
\(\|a+tb\|^2\le2\|a\|^2+2\|b\|^2\); these are smaller
than the stated \(L_0\).

To bound the exposing gradient without circular precision choices,
form the rational polynomial vector
\[
                    \Phi(q,t)=\nabla_{y,z}G_q(t,(t_it_j)).        \tag{9}
\]
Let \(d_\Phi\) be its total degree and \(S_\Phi\) the sum of
the absolute values of all coefficients, and put
\[
                  D_\Phi=1+d_\Phi S_\Phi(P+2)^{d_\Phi}.          \tag{10}
\]
The degree is an absolute constant; symbolic expansion has polynomial
size. The Jacobian in \(q\) has operator norm at most \(D_\Phi\)
on the box with all coordinates of magnitude at most \(P+1\).
This follows by bounding its norm by the sum of absolute derivative
entries. At \(q=t=p\), (5) is a homogeneous quadratic in
\((d,s)\), because \(f(p)=0\) and \(\nabla f(p)=0\).
Thus \(\Phi(p,p)=0\), and the mean-value inequality gives
\[
                  \|\nabla G_q(w_*)\|
                    \le D_\Phi\|q-p\|.                         \tag{11}
\]
All constants above have polynomial logarithmic size before choosing
\(q\).

## 3. Rational residuals with a conditioned Jacobian

Put \(r_{ij}=y_i y_j-z_{ij}\). Replace two factors in every cubic
monomial of \(\nabla f(y)\) by the corresponding \(z_{ij}\),
leaving lower-degree terms unchanged. This gives a rational quadratic
vector \(a(y,z)\) with \(a(y,(y_i y_j))=\nabla f(y)\).
Let \(R=(a,r)\) be the resulting \(N\) residuals. Their unique
common real zero is \(w_*\): \(r=0\) enforces the graph, and
\(a=0\) then gives the unique stationary point of \(f\).

For the Jacobian at \(w_*\),
\[
                  |\det J_R|=\det\nabla^2f(p)\ge\rho^n.          \tag{12}
\]
The change from \((y,z)\) to \((y,r)\) has determinant of
absolute value one. In those coordinates the derivative is block
triangular with diagonal blocks \(\nabla^2f(p)\) and identity.

Here are sufficient rational coefficient bounds:
\[
 \begin{aligned}
 W_0&=1+\sum_j\|R_j\|_1,& C_0&=2W_0,\\
 W&=2NW_0(1+K),& V&=\max\{1,W/C_0\},\\
 \nu&=\min\{1,\rho^n/(C_0W^{N-1})\},&
 \widetilde R_j&=R_j/C_0.
 \end{aligned}                                                   \tag{13}
\]
A quadratic's quadratic-part matrix has norm at most its coefficient
one-norm. Its gradient on the ball of radius \(K\) has norm at
most twice that one-norm times \(1+K\). Thus \(\|J_R\|\le W\).
The determinant product bound gives
\[
 \begin{gathered}
 \widetilde R_j(w_*+u)=b_j^{\mathsf T}u+u^{\mathsf T}T_j u,\\
 \|T_j\|\le1,\quad \|b_j\|\le V,\quad
                 \sum_jb_jb_j^{\mathsf T}\succeq\nu^2I.         \tag{14}
 \end{gathered}
\]
For the last assertion, the scaled determinant is at least
\(\rho^n/C_0^N\) and the scaled operator norm is at most
\(W/C_0\). All bounds have polynomial bit length.

## 4. Full positive definite Hessian Gram

Choose a positive rational square \(\epsilon=t_0^2\) with
\[
 \epsilon\le\min\left\{1,\frac{m_0^2}{2N},
             \frac{\nu^2m_0^2}{36N(L_0+NV)^2}\right\}.           \tag{15}
\]
A sufficiently small dyadic \(t_0\) has polynomial encoding.
Compute \(q\) to tolerance
\(\eta=\min\{1,\epsilon/D_\Phi\}\) using (3). Then
\[
 G_q(w_*+u)=\ell^{\mathsf T}u+u^{\mathsf T}Hu,
 \quad m_0I\preceq H\preceq L_0I,\quad\|\ell\|\le\epsilon.
                                                               \tag{16}
\]
The candidate quartic is
\[
                    B_*=G_q^2+\epsilon\sum_j\widetilde R_j^2.   \tag{17}
\]
It has an explicit rational SOS and unique zero \(w_*\).
It is exactly quartic because \(H\succ0\).

We repeat the ordinary-matrix argument from
[the reviewed singleton Hessian construction](sos-convex-quartic-realization.md).
For symmetric \(T\) and vector \(b\), define
\[
 D(b,T)_{i,(k,j)}=2b_kT_{ij}+4b_iT_{kj},\qquad
 \|D(b,T)\|\le6\sqrt N\|b\|\|T\|.
\]
A centered Hessian Gram on \((v,u\otimes v)\) is
\(M_c=\left(\begin{smallmatrix}C&D\\D^{\mathsf T}&Q\end{smallmatrix}\right)\),
where
\[
 \begin{aligned}
 C&=2\ell\ell^{\mathsf T}+2\epsilon\sum_jb_jb_j^{\mathsf T},\\
 D&=D(\ell,H)+\epsilon\sum_jD(b_j,T_j),\\
 Q&=8\operatorname{vec}(H)\operatorname{vec}(H)^{\mathsf T}
                  +4H\otimes H\\
  &\quad+\epsilon\sum_j
      [8\operatorname{vec}(T_j)\operatorname{vec}(T_j)^{\mathsf T}
                                       +4T_j\otimes T_j].
 \end{aligned}                                                   \tag{18}
\]
Differentiating each squared quadratic proves the identity. In
particular, the possibly negative tensors \(T_j\otimes T_j\)
are retained. Equations (14)--(16) give
\[
 \begin{aligned}
 C&\succeq2\epsilon\nu^2I,&Q&\succeq2m_0^2I,\\
 \|D\|&\le6\sqrt N\epsilon(L_0+NV),&
 C-DQ^{-1}D^{\mathsf T}&\succeq\tfrac32\epsilon\nu^2I.
 \end{aligned}                                                   \tag{19}
\]
Indeed \(Q\succeq(4m_0^2-4\epsilon N)I\), and the Schur
subtraction is at most
\(18N\epsilon^2(L_0+NV)^2/m_0^2\le\epsilon\nu^2/2\).

Set
\[
 \begin{gathered}
 q_0=2m_0^2,\quad s_0=\tfrac32\epsilon\nu^2,\quad
 B_D=6N\epsilon(L_0+NV),\\
 \gamma=\frac{\min\{s_0,q_0\}}
               {(2+2(B_D/q_0)^2)(2+K)^2}>0.                    \tag{20}
 \end{gathered}
\]
Completing the block square proves
\(M_c\succeq\min(s_0,q_0)I/(2+2(B_D/q_0)^2)\).
Translation from \(u=w-w_*\) gives
\[
 S_{w_*}=\begin{pmatrix}I&0\\-w_*\otimes I&I\end{pmatrix},
 \qquad M_w=S_{w_*}^{\mathsf T}M_cS_{w_*}\succeq\gamma I.        \tag{21}
\]
Here \(\|S_{w_*}^{-1}\|\le2+K\), and \(\gamma\) has
polynomial rational bit length.

## 5. Exact rational recovery

The displayed \(M_w\) is not asserted rational. Once \(q\),
\(G_q\), and the residuals are fixed, replace the center formally
by a variable \(v\) in (18)--(21), using the gradient data
\(\nabla G_q(v)\) and \(\nabla\widetilde R_j(v)\).
This gives a symmetric rational polynomial matrix \(\mathcal M(v)\)
of degree at most four, with \(\mathcal M(w_*)=M_w\).
It need not be a correct Hessian Gram at other centers.
Let \(d_M\le4\) be its degree, \(S_M\) the sum of absolute
coefficient values, and
\[
                     L_M=1+d_MS_M(K+2)^{d_M}.                   \tag{22}
\]
Bounding the derivative by its coefficient sum proves
\(\|\mathcal M(v)-\mathcal M(w_*)\|_F\le L_M\|v-w_*\|\)
when the points have norm at most \(K+1\).

Compute a further rational \(\widehat p\) with error
\[
 \delta\le\min\left\{1,\frac1{2P+2},
                     \frac{\gamma}{8L_M(2P+2)}\right\}         \tag{23}
\]
using (3). Its graph point \(v\) has distance at most
\((2P+2)\delta\) from \(w_*\):
\(\|pp^{\mathsf T}-\widehat p\widehat p^{\mathsf T}\|_F
 \le(\|p\|+\|\widehat p\|)\|p-\widehat p\|\), and restricting to symmetric
coordinates only decreases the norm. Thus
\(T=\mathcal M(v)\) is rational with
\(\|T-M_w\|_F\le\gamma/8\).

For the full Hessian monomial vector \(Z=(b,w\otimes b)\),
let \(E_\alpha\) be the symmetric zero-one matrix selecting all
ordered pairs whose product is monomial \(\alpha\). These matrices
have disjoint supports. If \(c_\alpha\) is its coefficient in
\(b^{\mathsf T}\nabla^2B_*(w)b\), set
\[
 \widehat M=T+\sum_\alpha E_\alpha
       \frac{c_\alpha-\langle E_\alpha,T\rangle_F}
                            {\|E_\alpha\|_F^2}.                \tag{24}
\]
This rational orthogonal affine projection fixes \(M_w\) and is
nonexpansive. Therefore it gives an exact rational Hessian Gram
\(\widehat M\succeq7\gamma I/8\).
All matrix dimensions are polynomial; all formal-center degrees are
fixed; all majorants above have polynomial logarithmic size. Hence
both approximation calls, the fixed-degree symbolic operations,
and the rational projection take polynomial bit time and output size.
Rational LDL verifies final positivity. Scaling \(B_*\) by
\(2/\gamma\) gives the claimed \(B\) with Hessian at least
identity. Positive rational weights become polynomially many rational
squares by binary expansion of numerator times denominator; integer
factorization is unnecessary. This completes the construction.

## 6. Strongly SOS-convex blocks with the established field obstruction

Apply the theorem to the reviewed tower quartic \(f_k\) in
\(3k\) variables and its supplied Hessian Gram. Write the companion
in [the rational quartic block lift](rational-block-sos-splitting-obstruction.md)
as \(g_k(y,z)\). The new \(B_k(y,z)\) is rational SOS with the
same lifted zero and full positive definite rational Hessian Gram.
Let \(C_k\) be any rational symmetric Hessian Gram for \(g_k\).
A rational integer \(T_k\) with polynomial bit length makes
\[
                       C_k+T_k A_{B_k}\succeq I,                 \tag{25}
\]
using determinant-over-trace for the positive matrix's margin and
the sum of absolute entries of \(C_k\) as a norm upper bound.
Then \(\widetilde g_k=g_k+T_kB_k\) is strongly SOS-convex with
the same zero, and \(f_k+\widetilde g_k\) has a polynomial-size
rational SOS.

For every real field \(E\), a separated SOS or separated PSD
polynomial Gram over \(E\) exists exactly when
\(2^{1/5^k}\in E\). The zero-shift argument forces a certificate
of \(f_k\), proving necessity by the reviewed field theorem.
For sufficiency, specialize the joint rational SOS at the tower
point \(p_k\in E^{3k}\), and use the established certificate for
\(f_k\). A finite algebraic coefficient list inherits the reviewed
individual-degree lower bound \(5^k\).

The variable count remains \(O(k^2)\), so the last bound is
\(5^{\Theta(\sqrt N)}\) in total variables. The joint polynomial
is strongly SOS-convex with a polynomial-size rational Hessian SOS
certificate. Every positive semidefinite full joint Hessian Gram is singular
because the blocks are independent. Unrestricted SOS certificates
remain short and rational.

## Prior comparison and review status

The primary approximation source was read at Corollary 1.2, its proof,
and the ellipsoid interface. Approximate minimization is established
prior, as are Taylor integration and the matrix conditioning tools.
The exposing-quadratic residual estimates are explicitly inherited
from the reviewed singleton notes. The proposed addition is closure
under the quadratic graph lift with polynomial rational input and
certificate size, and the stated strong-convexity field consequence.
The [block-SOS primary audit](rational-block-sos-splitting-prior.md)
compares related sparse representations; publication priority remains
unestablished. No arbitrary nonlinear graph theorem is claimed.

The quantitative proof passed a fresh independent review, including
a separate source and rational-recovery audit. The reviewer checked
the two final clarifications: the capped objective tolerance and the
second approximation's notation. No mathematical correction was
required. The root independently reconstructed all uniform bounds,
the certificate recovery, and the field consequence.

The reviewer ran the retained
[exact checker](check_quadratic_graph_quartic_realization_review.py).
It passed the Taylor graph identity, zero exposing gradient, and
residual determinant in dimensions one and two. A one-variable case
also passed the formal-center degree, true-center Hessian identity,
exact projection, and Frobenius contraction checks. These finite
checks support the identities; the all-dimension inequalities and
bit complexity are justified by the proof and source theorem.

A limited additional search used the phrases "SOS-convex graph
quartic polynomial lift", "strongly convex quartic Veronese", and
"sum of squares quadratic graph convex". The root reported mostly
graph-theoretic SOS, Lyapunov, and ordinary monomial-lifting material,
without identifying an equivalent arithmetic closure theorem.
This does not establish novelty. The relevant primary comparisons
remain the Taylor SOS theorems, convex approximation, and the scoped
singleton-realization literature audit already cited.

No floating-point experiment or Lean formalization was used, and no
project-wide verification or CI inspection was performed.
