# A linear lower bound for a full sparse QIPM Newton direction

Date: 2026-09-02

## Main result

The linear-size plateau-gain LP has a public all-ones primal--dual start whose
Newton right-hand side is independent of every hidden sign. Nevertheless, one
amplitude encoding of the **full** primal--dual Newton direction reveals the
parity of all \(N\) signs. Preparing that state to trace distance \(1/100\)
therefore needs at least \(N/2=\Omega(P)\) raw coefficient queries. The result
survives a fixed relative error in the direction.

After exact Schur preconditioning, the relevant two-block KKT matrix has
absolute spectral condition number \(\varphi^2\). Even a state of a
\(10^{-3}\)-relative-residual solution of this preconditioned system, at trace
error \(1/200\), still needs at least \(N/2\) total raw queries. Arbitrary
offline preprocessing is allowed, provided its raw queries are counted.

The underlying LP and its central path are proved in
[2026-09-02-linear-size-robust-gain-parity-lp.md](2026-09-02-linear-size-robust-gain-parity-lp.md).
The theorem here is about the first infeasible-start Newton correction, not a
late feasible central-path tangent.

## The LP and its public Newton system

Let \(N\ge2\), \(K=16N\), and \(P=17N+1\). The nodes are
\(i=0,\ldots,N+K\), with public heights

\[
 H_i=2^{\min\{i,T\}},\qquad
 T=\left\lceil\frac12\log_2N\right\rceil,\qquad
 H=2^T\in[\sqrt N,2\sqrt N).
\tag{1}
\]

The first \(N\) edges have hidden signs
\(a_i=\sigma_i\in\{-1,+1\}\), and the last \(K\) edges have \(a_i=1\).
Put

\[
 \tau_0=1,\qquad \tau_i=\prod_{j=1}^i a_j,
\tag{2}
\]

so \(\tau_i=p_N:=\prod_{j=1}^N\sigma_j\) on every copy node
\(i=N+1,\ldots,N+K\). At node \(i\), the nonnegative variables are
\((u_i,v_i,h_i,t_i)\), with \(d_i=u_i-v_i\) and \(q_i=u_i+v_i\). The
equalities are

\[
\begin{aligned}
 d_0&=1,&d_i-g_ia_id_{i-1}&=0,\\
 h_0&=1,&h_i-g_ih_{i-1}&=0,\\
 &&q_i+t_i-2h_i&=0,
\end{aligned}
\qquad g_i=H_i/H_{i-1},
\tag{3}
\]

and the objective coefficient at each node is \(c_i=(2,2,1,1)\).
Write the equalities as \(A_\sigma x=b\). The matrix has \(n=4P\) columns,
\(m=3P\) full-rank rows, row and column sparsity at most four, and coefficients
of magnitude at most two.

Start the standard infeasible primal--dual method at

\[
 x^0=s^0=\mathbf1,\qquad y^0=0,\qquad \mu^0=1.
\tag{4}
\]

This point is strictly positive and exactly complementarity-centered,
\(X^0s^0=\mathbf1\), but is deliberately primal and dual infeasible. For any
public fixed centering target \(\theta\in[0,1]\), its Newton equations are

\[
\begin{aligned}
 A_\sigma\Delta x&=b-A_\sigma\mathbf1,\\
 A_\sigma^T\Delta y+\Delta s&=c-\mathbf1,\\
 \Delta x+\Delta s&=(\theta-1)\mathbf1.
\end{aligned}
\tag{5}
\]

The complete right-hand side is public. On \(\mathbf1\), every difference
expression is zero because \(u_i-v_i=0\), including the signed predecessor
term. Hence the difference residual is one at the root and zero elsewhere.
The reference-transition residuals are \(g_i-1\), every cap residual is
\(-1\), and the dual and complementarity residuals are public. Only local KKT
entries contain hidden signs.

The square three-block KKT matrix has dimension \(2n+m=11P\), row and column
sparsity at most four, and entries bounded by two. Full row rank of \(A_\sigma\)
makes (5) nonsingular.

## Closed form of the direction

Let \(x^+=\mathbf1+\Delta x\). The first equation in (5) makes \(x^+\)
equality feasible, so

\[
 d_i^+=H_i\tau_i,\qquad h_i^+=H_i,\qquad q_i^++t_i^+=2H_i.
\tag{6}
\]

Eliminating \(\Delta s\) and projecting on the input-independent null vector

\[
 W_i=\sqrt{\frac23}
 \left(\frac12e_{u_i}+\frac12e_{v_i}-e_{t_i}\right)
\tag{7}
\]

gives \(W_i^T\Delta x=-W_i^Tc\). Solving with (6) yields

\[
\begin{aligned}
 \Delta x_{u_i}&=\frac{4H_i-8+3H_i\tau_i}{6},&
 \Delta x_{v_i}&=\frac{4H_i-8-3H_i\tau_i}{6},\\
 \Delta x_{h_i}&=H_i-1,&
 \Delta x_{t_i}&=\frac{2H_i-1}{3}.
\end{aligned}
\tag{8}
\]

Thus the primal correction is independent of \(\theta\).

Split the multiplier as
\(\Delta y=(\alpha,\beta,\gamma)\), corresponding to the difference,
reference, and cap rows. Define

\[
 R_{2,j}=\sum_{i=j}^{N+K}H_i^2,\qquad
 R_{1,j}=\sum_{i=j}^{N+K}H_i.
\tag{9}
\]

Back substitution in the gain-incidence blocks gives

\[
\begin{aligned}
 \alpha_j&=\tau_j\frac{R_{2,j}}{2H_j},\\
 \beta_j&=\frac{7R_{2,j}+(4-9\theta)R_{1,j}}{3H_j},\\
 \gamma_j&=\frac{2H_j+2}{3}-\theta.
\end{aligned}
\tag{10}
\]

These formulas also directly verify (5).

## A full-direction parity decoder

Let \(S=\{N+1,\ldots,N+K\}\) be the copy suffix and put

\[
 A_S=\sum_{j\in S}\alpha_j^2
 =\frac{H^2}{4}\sum_{\ell=1}^{K}\ell^2.
\tag{11}
\]

If \(M=P-T\) is the number of plateau nodes, then

\[
 \frac{\sum_{j\ge T}\alpha_j^2}{A_S}
 =\frac{\sum_{\ell=1}^{M}\ell^2}{\sum_{\ell=1}^{K}\ell^2}
 \le\left(\frac{M}{K}\right)^3
 \le\left(\frac{35}{32}\right)^3.
\tag{12}
\]

For the gain prefix,

\[
 \sum_{j<T}H_j^{-2}<\frac43,\qquad
 \sum_iH_i^2<\left(17N+\frac43\right)H^2,\qquad H^2<4N.
\tag{13}
\]

Since \(R_{2,j}\le\sum_iH_i^2\), (11)--(13) imply

\[
 \frac{\sum_{j<T}\alpha_j^2}{A_S}
 <\frac{(17+4/(3N))^2}{256}<1.22,
 \qquad
 \|\alpha\|_2^2<3A_S.
\tag{14}
\]

Monotonicity of the heights gives \(R_{1,j}/R_{2,j}\le1/H_j\le1\). Hence

\[
 \frac43
 \le\frac{\beta_j}{|\alpha_j|}
 =\frac{14}{3}
   +\frac{2(4-9\theta)}{3}\frac{R_{1,j}}{R_{2,j}}
 \le\frac{22}{3}.
\tag{15}
\]

On the copy suffix \(H_j=H\ge2\), the lower bound improves to
\(\beta_j/|\alpha_j|\ge3\). Thus

\[
 \|\beta\|_2^2<\frac{484}{3}A_S.
\tag{16}
\]

Equation (8) gives \(\|\Delta x\|_2^2<3\sum_iH_i^2\). Since
\(\Delta s=(\theta-1)\mathbf1-\Delta x\),

\[
 \|\Delta s\|_2^2<14\sum_iH_i^2,\qquad
 \|\gamma\|_2^2<2\sum_iH_i^2.
\tag{17}
\]

The ratio of \(\sum_iH_i^2\) to (11) is less than
\(12(17N+4/3)/K^3\). For \(N\ge2\), the three terms in (17), including
\(\|\Delta x\|^2\), contribute less than \(A_S/4\). Therefore

\[
 \|w_\sigma\|_2^2<165A_S,\qquad
 w_\sigma:=(\Delta x,\Delta y,\Delta s).
\tag{18}
\]

Define the fixed norm-one observable

\[
 O_S=\sum_{j\in S}
 \left(|\alpha_j\rangle\langle\beta_j|
       +|\beta_j\rangle\langle\alpha_j|\right).
\tag{19}
\]

All \(\alpha_j\) on \(S\) have sign \(p_N\), and every \(\beta_j\) is
positive. Hence

\[
 p_N\langle w_\sigma/\|w_\sigma\||O_S|
                w_\sigma/\|w_\sigma\|\rangle
 >\frac{6}{165}=\frac2{55}>\frac1{30}.
\tag{20}
\]

### Theorem 1 (full sparse-KKT direction lower bound)

Any fixed-position sparse-coefficient-query algorithm whose unconditional
output is within trace distance \(1/100\) of
\(|w_\sigma/\|w_\sigma\|\rangle\) for every input makes at least \(N/2\)
raw coefficient queries.

Trace distance \(1/100\) changes (20) by at most \(1/50\), so the expectation
still has the sign of parity. An expectation after \(Q\) sign queries is a
real multilinear polynomial of degree at most \(2Q\). Its correlation with
full parity is positive, so its parity Fourier coefficient is nonzero and its
degree is at least \(N\). Thus \(2Q\ge N\). Every sparse LP or KKT query is
simulated coherently by at most one sign query.

The theorem is robust to an approximate direction: if

\[
 \|\widetilde w-w_\sigma\|_2\le\frac1{300}\|w_\sigma\|_2
\tag{21}
\]

and the output is within trace distance \(1/300\) of
\(|\widetilde w/\|\widetilde w\|\rangle\), its total distance from the exact
state is at most \(1/100\).

The result also applies to the Hermitian dilation and to a canonical sparse
block encoding built with \(O(1)\) calls to the sparse KKT oracles. It does not
apply to an unspecified block-encoding unitary whose unconstrained junk block
may encode arbitrary global information.

## Direct canonical block-encoding model

The literal full Newton system has the symmetric \(11P\)-dimensional form

\[
 M_\sigma^{(3)}=
 \begin{pmatrix}
 0&A_\sigma^T&I\\
 A_\sigma&0&0\\
 I&0&I
 \end{pmatrix},
 \qquad
 r_\theta^{(3)}=
 \begin{pmatrix}
 c-\mathbf1\\ b-A_\sigma\mathbf1\\
 (\theta-1)\mathbf1
 \end{pmatrix}.
\]

Its solution is \(w_\sigma=(\Delta x,\Delta y,\Delta s)\). Its support,
entry magnitudes, and right-hand side are public; its maximum absolute row or
column sum is six. Moreover,

\[
 \|r_\theta^{(3)}\|_2^2
 =3P+T+1+4P(1-\theta)^2.
\]

For \(\theta=1\), eliminate \(\Delta s=-\Delta x\) and set
\(y'=-\Delta y\). Define

\[
 \mathcal K_\sigma=
 \begin{pmatrix}I&A_\sigma^T\\A_\sigma&0\end{pmatrix},
 \qquad
 r=\binom{\mathbf1-c}{b-A_\sigma\mathbf1}.
\tag{22}
\]

This is a symmetric \((n+m)=7P\)-dimensional matrix. Its maximum row and
column sparsity is four, its largest entry magnitude is two, and its maximum
absolute row or column sum is exactly six. Its solution is
\((\Delta x,y')\). Removing the \(\Delta s\) block can only increase the
absolute expectation of (19), because the numerator is unchanged and the
normalization decreases.

Here is a completely specified magnitude-weighted block encoding. For each
actual nonzero entry \(M_{rc}\) of \(M=\mathcal K_\sigma\), introduce the
common label \(\lambda_{rc}=(r,c,0)\), together with private, mutually
orthogonal failure labels \(L_r,R_c\). Put

\[
\begin{aligned}
 |\chi_r\rangle
 &=\sum_c\sqrt{|M_{rc}|/6}\,|\lambda_{rc}\rangle
   +\sqrt{1-\sum_c|M_{rc}|/6}\,|L_r\rangle,\\
 |\phi_c\rangle
 &=\sum_r\operatorname{sgn}(M_{rc})\sqrt{|M_{rc}|/6}\,
             |\lambda_{rc}\rangle
   +\sqrt{1-\sum_r|M_{rc}|/6}\,|R_c\rangle.
\end{aligned}
\tag{23}
\]

Both displayed families are orthonormal and
\(\langle\chi_r|\phi_c\rangle=M_{rc}/6\). Choose fixed unitary completions
\(L|0^a,r\rangle=|\chi_r\rangle\) and
\(R_\sigma|0^a,c\rangle=|\phi_c\rangle\). Then

\[
 U_{\mathcal K}=L^\dagger R_\sigma
\tag{24}
\]

is an exact \((6,a,0)\) block encoding, with \(a=O(\log P)\).
For comparison, the literal uniform-four-slot sparse-access lemma gives
normalization
\(\sqrt{4\cdot4}\,\|\mathcal K_\sigma\|_{\max}=8\); (24) is its
magnitude-weighted state-preparation-pair refinement.

The encoding construction itself is standard and is not a novelty claim.
It is an explicit instance of the state-preparation-pair/q-norm
block-encoding framework of Gilyén et al.,
[*Quantum singular value transformation and beyond*](https://arxiv.org/abs/1806.01838),
and Clader et al.,
[*Quantum resources required to block-encode a matrix of classical
data*](https://doi.org/10.1109/TQE.2022.3231194).  At exponent \(p=1/2\),
the latter normalization is the geometric mean of the maximum absolute row
and column sums, which is six here.  Equations (23)--(24) are retained to fix
the entire oracle completion and its raw-sign query cost, not to claim a new
generic block-encoding lemma.

More explicitly, \(R_\sigma=S_\sigma R_0\). The support, magnitudes, failure
arms, and \(R_0,L\) are public. On an actual-entry label, \(S_\sigma\)
multiplies the amplitude by the one hidden sign belonging to that local KKT
entry, or by one if the entry is public. Its edge index is computed
reversibly, so \(S_\sigma\) uses exactly one coherent sign-phase query.
Therefore each call to \(U_{\mathcal K}\), \(U_{\mathcal K}^\dagger\), or a
controlled version uses exactly one sign query. The entire unitary completion
is fixed by this construction. Its nonprincipal blocks may depend **locally**
on a sign, but cannot encode an additional global predicate.

The right-hand side is public. More explicitly,

\[
 \|r\|_2^2=3P+T+1.
\tag{25}
\]

The top block has two entries \(-1\) per node. The lower block has one root
difference entry \(+1\), \(T\) gain-prefix reference entries \(+1\), and
\(P\) cap entries \(-1\). A public state-preparation unitary

\[
 U_r|0\rangle=|r/\|r\|\rangle
\tag{26}
\]

therefore uses no coefficient or sign queries.

### Corollary 1 (canonical block-encoding query lower bound)

The state-pair construction (23)--(24) applies verbatim to either
\(M_\sigma^{(3)}\) or \(\mathcal K_\sigma\), with normalization six and
exactly one sign query per block-encoding call. Any algorithm using either
canonical block encoding, its adjoint, unlimited calls to the corresponding
public RHS unitary, and input-independent gates that prepares the normalized
solution to trace distance \(1/100\) uses

\[
 q_{\rm BE}\ge\frac N2=\Omega(P)
\tag{27}
\]

block-encoding calls.

The proof is exactly the degree argument of Theorem 1 after replacing every
block-encoding call by its one-query sign-oracle implementation.
Thus this is a lower bound in a fully specified block-encoding interface, not
an appeal to the encoded top-left block while ignoring the unitary completion.
The normalization is constant, and right-hand-side preparation is free of
hidden input queries.

## Constant-conditioned preconditioned residual theorem

Set \(\theta=1\), eliminate \(\Delta s=-\Delta x\), and write
\(y'=-\Delta y\). Equation (5) becomes

\[
 \begin{pmatrix}I&A_\sigma^T\\A_\sigma&0\end{pmatrix}
 \binom{\Delta x}{y'}
 =\binom{\mathbf1-c}{b-A_\sigma\mathbf1}.
\tag{28}
\]

Let

\[
 \mathcal S_\sigma=A_\sigma A_\sigma^T,\qquad
 Q_\sigma=\mathcal S_\sigma^{-1/2}A_\sigma,\qquad
 Q_\sigma Q_\sigma^T=I.
\tag{29}
\]

Let
\[
 P_\sigma=\operatorname{Diag}(I,\mathcal S_\sigma^{-1/2}).
\]
In the standard SPD-preconditioner convention this is symmetric block
preconditioning by \(\operatorname{Diag}(I,\mathcal S_\sigma)\).  Explicitly,
\(\overline K_\sigma=P_\sigma K_\sigma P_\sigma\), the transformed unknown is
\(\overline w_\sigma=P_\sigma^{-1}(\Delta x,y')\), and the transformed
right-hand side is \(\overline r_\sigma=P_\sigma r_\sigma\).  Hence

\[
 \overline K_\sigma=
 \begin{pmatrix}I&Q_\sigma^T\\Q_\sigma&0\end{pmatrix},
 \qquad
 \overline w_\sigma=\binom{\Delta x}{\mathcal S_\sigma^{1/2}y'},
\tag{30}
\]

with the correspondingly transformed right-hand side
\(\overline r_\sigma\). The eigenvalues of \(\overline K_\sigma\) are \(1\)
on \(\ker Q_\sigma\) and

\[
 \frac{1+\sqrt5}{2},\qquad \frac{1-\sqrt5}{2}
\tag{31}
\]

on every coupled two-dimensional subspace. Therefore

\[
 \|\overline K_\sigma\|_2
 =\|\overline K_\sigma^{-1}\|_2=\varphi,\qquad
 \kappa_{\rm abs}(\overline K_\sigma)=\varphi^2.
\tag{32}
\]

The primal observable

\[
 O_x=\sum_{i\in S}
 \left(|D_i\rangle\langle h_i|+|h_i\rangle\langle D_i|\right),
 \qquad |D_i\rangle=\frac{|u_i\rangle-|v_i\rangle}{\sqrt2},
\tag{33}
\]

has norm one. A minimum-norm feasible-correction argument gives

\[
 \|\Delta x\|_2^2
 \le\frac{11}{3}\sum_iH_i^2
 \le\frac{11}{3}PH^2.
\tag{34}
\]

Indeed, decompose \(\Delta x\) orthogonally into the minimum-norm vector in
\(\operatorname{range}(A_\sigma^T)\) with the required primal residual and its
\(\ker A_\sigma\) component. The feasible candidate \(x^*-\mathbf1\) bounds
the first squared norm by
\(\sum_i[3(H_i-1)^2+1]\le3\sum_iH_i^2\). Equation (7) makes the second
squared norm exactly \(2P/3\).

Equation (8) implies

\[
 p_N\frac{\langle\Delta x|O_x|\Delta x\rangle}
                {\|\Delta x\|_2^2}
 =\frac{K\sqrt2H(H-1)}{\|\Delta x\|_2^2}
 >\frac16.
\tag{35}
\]

The primal block has a constant fraction of the preconditioned solution norm.
Indeed, \(\|\mathbf1-c\|_2^2=2P\), whereas the copied difference coordinates
give

\[
 \|\Delta x\|_2^2\ge\frac{KH^2}{2}\ge8N^2.
\tag{36}
\]

Writing \(\overline w=(\Delta x,\overline y)\), the first row of (30) gives
\(\|\overline y\|\le\|\mathbf1-c\|+\|\Delta x\|\). Since \(2P\le35N\),
(36) yields

\[
 \|\overline w_\sigma\|_2^2
 <\frac{29}{4}\|\Delta x\|_2^2.
\tag{37}
\]

Extending \(O_x\) by zero on the dual block, (35)--(37) imply

\[
 p_N\frac{\langle\overline w_\sigma|O_x|
                     \overline w_\sigma\rangle}
                {\|\overline w_\sigma\|_2^2}
 >\frac{2}{87}.
\tag{38}
\]

### Theorem 2 (residual-robust, constant-conditioned KKT lower bound)

Suppose an algorithm produces a density operator within trace distance
\(1/200\) of the normalized state of some nonzero
\(\widetilde{\overline w}\) satisfying

\[
 \|\overline K_\sigma\widetilde{\overline w}
       -\overline r_\sigma\|_2
 \le\frac1{1000}\|\overline r_\sigma\|_2.
\tag{39}
\]

Then its complete implementation makes at least \(N/2\) raw LP coefficient
queries.

Equations (32) and (39) give

\[
 \|\widetilde{\overline w}-\overline w_\sigma\|_2
 \le\varphi^2 10^{-3}\|\overline w_\sigma\|_2.
\tag{40}
\]

The normalized approximate and exact states are at trace distance at most
\(2\varphi^2/1000\). Including the output error, the total is

\[
 \frac1{200}+\frac{2\varphi^2}{1000}<\frac1{87}.
\tag{41}
\]

Equations (38) and (41) leave a strictly positive parity-signed expectation,
so the degree argument from Theorem 1 again gives \(Q\ge N/2\).

Theorem 2 is an end-to-end raw-input theorem. It allows any construction of a
block encoding of \(\overline K_\sigma\), its transformed right-hand side, and
the recovery/output map, but counts every raw coefficient query used by those
stages. If an exact data-dependent Schur preconditioner or its block encoding
is supplied as a free primitive, that oracle can already contain the answer
and no raw-input lower bound is possible.

### Proposition 2 (no matrix-only access--normalization tradeoff)

No lower bound depending only on the normalization and condition number of an
abstract preconditioned-matrix block encoding can hold on this family.

Indeed, the null space
\(\ker A_\sigma=\operatorname{span}\{W_i\}\) is public. Hence the row-space
projector

\[
 \Pi=A_\sigma^T(A_\sigma A_\sigma^T)^{-1}A_\sigma=I-WW^T
\]

is input-independent. Let \(Q_0\) be any public row isometry with
\(Q_0^TQ_0=\Pi\), and let \(Q_\sigma\) be as in (29). Then

\[
 O_\sigma=Q_\sigma Q_0^T
\]

is orthogonal and \(Q_\sigma=O_\sigma Q_0\). The dual-coordinate congruence
\[
 R_\sigma=\operatorname{Diag}(I,O_\sigma)
\]
therefore gives

\[
 R_\sigma^T\overline K_\sigma R_\sigma
 =\begin{pmatrix}I&Q_0^T\\Q_0&0\end{pmatrix},
\]

which is completely public, has norm \(\varphi\), and has condition
\(\varphi^2\). Input dependence has moved to the transformed right-hand side
and the recovery map.

The same obstruction has a concrete sparse form. Swapping \(u_i,v_i\) when
\(\tau_i=-1\), together with the corresponding sign gauge on difference rows,
maps \(A_\sigma\), the public start, and the untransformed Newton right-hand
side to the all-positive-sign instance. If this prefix gauge is supplied for
free, both matrix access and transformed solving can be public; original-state
recovery contains all the parity.

Thus constant normalization and constant condition can coexist with either
easy matrix access or hard recovery. The invariant statement is the charged
end-to-end ledger. If preprocessing uses \(q_{\rm set}\) raw queries, a solver
makes \(T_{\rm BE}\) preconditioned block-encoding calls costing
\(q_{{\rm BE},t}\) raw queries each, and RHS preparation plus recovery use
\(q_{\rm rhs},q_{\rm rec}\), then any output satisfying Theorem 2 obeys

\[
 q_{\rm set}+\sum_{t=1}^{T_{\rm BE}}q_{{\rm BE},t}
 +q_{\rm rhs}+q_{\rm rec}\ge\frac N2.
\]

This is tight in order. It is also the strongest factor-independent statement
available without restricting the admissible coordinate rotations,
preconditioner data structures, or recovery interface.

A complementary factor-specific result is proved in
[2026-09-02-schur-factor-access-normalization-frontier.md](2026-09-02-schur-factor-access-normalization-frontier.md):
for the signed gain block, an \(\alpha_P\)-normalized factor that gives Schur
condition \(K\) obeys the sharp frontier
\(\alpha_P\sqrt K=\Omega(N)\), and approximate inverse-factor block encodings
satisfy a stronger raw-access product bound.

## Transfer to the prefix-rigidified family

The residual-robust preconditioned theorem also holds for the family in
[2026-09-02-prefix-rigidified-condition-one-newton-hardness.md](2026-09-02-prefix-rigidified-condition-one-newton-hardness.md).
That family adds the public rows

\[
 q_i-\frac54h_i=0\quad(i<T)
\tag{42}
\]

and uses objective coefficients

\[
 c'_i=(1+\omega,1+\omega,1,1),\qquad
 \omega=\frac7{36H}.
\tag{43}
\]

At the all-ones start, each added-row residual is the public number \(-3/4\).
The hidden difference coefficients still multiply \(u_i-v_i=0\). Thus the
entire Newton right-hand side remains public.

On every free node \(i\ge T\), null projection now gives
\(\Delta q_i/2-\Delta t_i=-\omega\). Exact feasibility gives

\[
 \Delta q_i=\frac{4H-6-2\omega}{3},\qquad
 \Delta h_i=H-1,\qquad
 \Delta u_i-\Delta v_i=H\tau_i.
\tag{44}
\]

The prefix variables are fixed by feasibility. Directly from these formulas,

\[
 \|\Delta x\|_2^2<5\sum_iH_i^2,
 \qquad
 p_N\frac{\langle\Delta x|O_x|\Delta x\rangle}
                {\|\Delta x\|_2^2}>\frac18.
\tag{45}
\]

The numerator is unchanged:
\(K\sqrt2H(H-1)\). For the norm bound, each rigid prefix node contributes
less than \(5H_i^2\), and each free node less than \(4H^2\).

For the exact block preconditioner, the transformed primal right-hand side is
\(\mathbf1-c'=(-\omega,-\omega,0,0)\) per node. Using (36),

\[
 \frac{\|\mathbf1-c'\|_2}{\|\Delta x\|_2}<\frac{21}{100}.
\tag{46}
\]

Consequently the analogue of (37) improves to

\[
 \|\overline w_\sigma\|_2^2<\frac52\|\Delta x\|_2^2,
\tag{47}
\]

and the parity-signed expectation of \(O_x\) on the exact preconditioned
solution state exceeds \(1/20\). The condition number remains exactly
\(\varphi^2\). The errors in (39) and the output trace error \(1/200\) change
this expectation by less than \(2/87<1/20\). Hence Theorem 2 and the
\(N/2\) lower bound transfer unchanged.

Theorem 1's particular unscaled full-direction decoder is not asserted for
the rigidified family: the \(T\) additional row multipliers add coordinates
to the unscaled direction and require a separate mass bound. The primal
direction theorem and the stronger preconditioned full-state theorem above
do not have that issue.

## Offline preprocessing and the sharp boundary

Allow arbitrary nonuniform advice depending on \(N\) but not on \(\sigma\).
An offline quantum channel may make \(Q_{\rm pre}\) raw queries and retain
arbitrary classical data, qRAM structures, and quantum memory. An online
channel may use all retained resources, arbitrary preconditioners built from
them, intermediate measurements, and \(Q_{\rm on}\) further raw queries.
For one requested output, purification turns this whole pipeline into a
\(Q_{\rm pre}+Q_{\rm on}\)-query algorithm. Therefore both theorems imply

\[
 \boxed{Q_{\rm pre}+Q_{\rm on}\ge N/2.}
\tag{48}
\]

The same polynomial argument covers a heralded branch with any everywhere
positive success probability: the unnormalized joint success-and-sign
expectation has the sign of parity on every input, so it has a nonzero
degree-\(N\) Fourier coefficient. This avoids a postselection loophole.

There are two necessary limits.

1. A free input-dependent prefix gauge destroys the theorem. Swap \(u_i,v_i\)
   whenever \(\tau_i=-1\), and apply the corresponding diagonal sign gauge to
   the difference rows. This maps every signed instance, its public start and
   right-hand side, and its Newton direction to the all-positive-sign instance.
   Constructing or querying that gauge computes prefix parity and must be
   charged.
2. After \(\Theta(N)\) one-time preprocessing reads and stores all signs, later
   solves may use no additional raw queries. Thus (48) is tight for the first
   output; no positive amortized raw-query lower bound can hold under unlimited
   reuse of a complete sign table.

As a numerical audit, the full matrices were assembled and solved directly for
\(N=2,5,17\) and random signs. Equations (8) and (10) agreed with the numerical
solutions to between \(10^{-13}\) and \(10^{-10}\). The observed absolute
expectations in (20) were \(0.244\), \(0.203\), and \(0.184\), respectively,
well above the conservative \(1/30\) bound.

## Relation to existing results

The parity polynomial lower bound, endpoint padding, block KKT
preconditioning, and the warning that preconditioner application and
block-encoding construction must be charged are established ideas. In
particular, the three-point spectrum in (31), and hence the golden-ratio
condition number in (32), is the classical ideal-Schur-complement result of
Murphy--Golub--Wathen for saddle-point/KKT systems
([DOI:10.1137/S1064827599355153](https://doi.org/10.1137/S1064827599355153)).
Neither exact Schur preconditioning nor \(\kappa_{\rm abs}=\varphi^2\) is new
here. Other relevant comparators are Beals et al.,
[*Quantum Lower Bounds by Polynomials*](https://arxiv.org/abs/quant-ph/9802049);
Apers and Gribling,
[*Quantum speedups for linear programming via interior point
methods*](https://arxiv.org/abs/2311.03215);
Wu, Mohammadisiahroudi, and Terlaky,
[*A preconditioned inexact infeasible quantum interior point method for linear
optimization*](https://doi.org/10.1007/s10589-025-00750-4); and Lapworth and
Sünderhauf,
[*Preconditioned Block Encodings for Quantum Linear Systems*](https://arxiv.org/abs/2502.20908).

The access boundary must be stated precisely. The unpreconditioned sparse KKT
right-hand side in (5), and equivalently the right-hand side in (22), is public
and input-independent. The transformed right-hand side
\(\overline r_\sigma\) in (30) need not be public: applying
\(\mathcal S_\sigma^{-1/2}\) to its constraint block is data-dependent. Theorem
2 charges construction of both that state and a block encoding of
\(\overline K_\sigma\). If those two preconditioned access primitives were
instead supplied for free, a standard constant-condition QLSA could prepare
the designated solution state with polylogarithmic dimension dependence, and
the raw-coefficient lower bound would not apply. In fact, because (31) has only
three spectral values, inverse interpolation on that support has degree at most
two: at fixed output accuracy the supplied-preconditioned-oracle solve itself
needs only a constant number of matrix-oracle uses, apart from state preparation
and normalization. Adhikari's state-aware Krylov--query characterization makes
this finite-support distinction explicit
([arXiv:2510.11786](https://arxiv.org/abs/2510.11786)). Thus all linear hardness
in Theorem 2 must reside in implementing the preconditioned matrix/RHS access or
the final raw-coordinate output, exactly the stages that its ledger charges.

This is why generic QLS lower bounds are not the source of Theorem 2.
Orsucci--Dunjko lower-bound a designated positive-definite QLS solution under
sparse or block access ([arXiv:2101.11868](https://arxiv.org/abs/2101.11868)),
while Wang--Zhang and Mori et al. establish condition- and sparsity-dependent
QLS lower bounds ([arXiv:2407.06012](https://arxiv.org/abs/2407.06012),
[arXiv:2601.16697v2](https://arxiv.org/abs/2601.16697v2)). At constant supplied
condition number they do not yield an \(\Omega(P)\) raw-LP lower bound. Wu et
al. analyze a concrete data-dependent preconditioned infeasible QIPM and reduce
its Newton-system conditioning from \(O(\mu^{-2})\) to \(O(\mu^{-1})\), but give
an upper bound under QRAM and matrix-construction assumptions, not a lower bound
for the end-to-end preconditioner/RHS/output pipeline. Lapworth--Sünderhauf
show that composing preconditioned block encodings can incur normalization
overhead; they likewise do not prove the parity-based implementation lower
bound here. Low--Su's QLS algorithm and matching initial-state-preparation
lower bound explicitly separate matrix-oracle from right-hand-side-oracle cost
([arXiv:2410.18178](https://arxiv.org/abs/2410.18178)). That supports, but does
not originate, the accounting principle used here: their QLS input already
supplies both access primitives, whereas Theorem 2 starts from raw sparse LP
coefficients and lower-bounds their aggregate construction-and-output cost.

Mori et al. are the closest oracle-level antecedent: their public-RHS sparse
QLS instance also has a padded parity-history solution state and linear query
hardness, but its constant-error family has \(\kappa=\Theta(N)\) and is not an
LP Newton system. Apers--Gribling already prove linear sparse-LP
coefficient-query lower bounds for objective approximation, not a
Newton-direction state. Binkowski also studies a first all-ones Newton solve
([arXiv:2604.24362](https://arxiv.org/abs/2604.24362)), but through benchmark
runtime and tomography floors rather than a coefficient-query reduction.

For Corollary 1, the constant-six canonical encoding is not new: it is the
standard q-norm/state-pair encoding specialized to this KKT matrix.  The
corollary's content is instead the instance-specific reduction after fixing
that completion.  Wang--Zhang's block-QLSP lower bound and Mori et al.'s
sparse-QLS lower bound also build explicit local block encodings of
parity/chain matrices, but they are worst-case QLS constructions whose hard
families have growing condition number.  They do not imply the LP-native
central/Newton statement or the condition-one *reduced* geometry here.
Conversely, this corollary does not claim hardness for an arbitrary supplied
block encoding with unconstrained junk, or a constant-condition lower bound
for the full unpreconditioned KKT matrix.

The apparent new conjunction is narrower: a bounded-degree, linear-size LP
whose full primal--dual Newton direction for an **input-independent sparse-KKT
right-hand side** has a linear standard coefficient-query lower bound, together
with a fixed-relative-residual version after exact constant-condition Schur
preconditioning in which all preconditioned access construction is charged,
and an explicit offline--online query ledger. No located primary source states
this conjunction. This is evidence of apparent novelty, not proof of priority.
It should not be advertised as a constant-\(\kappa\) lower bound in the usual
QLS input model.

The result does not say that every Newton step on the family is hard. Once the
iterate is exactly feasible, directions confined to the public null basis can
be sign-independent. The obstruction here is the first infeasible-start
correction: it must construct the hidden affine feasible translation.

Status: **proof complete in the stated raw coefficient, canonical sparse-KKT,
and charged block-encoding models; apparently new after the targeted search.**
