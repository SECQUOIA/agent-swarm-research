# Group-holonomy trace-one SDPs: conjugacy-class optima and condition-one Newton hardness

## Status and genuinely new content

This note generalizes the signed qutrit triangle to matrix-valued holonomy.  A path of
local orthogonal transports is coupled to three public anisotropy sectors.  Eliminating
the path gives a free trace-one \(S_+^{3d}\) problem whose effective cost is the
connection adjacency matrix of a triangle.  Its scalar optimum is an explicit
conjugacy-invariant function of the accumulated group word.

For the natural permutation representation of \(S_3\), the construction uses
\(9\times9\) PSD blocks and its scalar optimum distinguishes the identity,
transposition, and three-cycle conjugacy classes.  Restricting each input symbol to the
identity or one fixed transposition gives an \(\Omega(N)\) raw-query lower bound for
optimal-value estimation and for a public-start Newton direction state.  Every
nonzero equality coefficient in this example has a public value in
\(\{-1,+1\}\); only its sparse predecessor position is input dependent.  At that start,
the ambient barrier Hessian is scalar, the equality-reduced Hessian has condition number
exactly one, the Newton decrement is \(\sqrt2/30\), and the scalar
primal-barrier saddle KKT sparsity graph is a forest.  On the parity
restriction, both the complete primal-plus-multiplier KKT state and an
explicit constant-normalization KKT block encoding retain linear query
hardness.  Synthesizing the normalization-one tangent projector from raw
symbols also has tight \(\Theta(N)\) query complexity, although applying a
supplied projector to the public gradient has signal probability \(24/41\).
Thus the earlier
treewidth-one obstruction extends to an ambient nonabelian, gauge-invariant word
observable.  The proved query-hard subfamily itself is only the abelian subgroup
\(\{e,t\}\cong\mathbb Z_2\); the lower bound is therefore not an intrinsically
nonabelian word-query lower bound.

The group-connection spectrum below is classical.  The candidate new result is its
combination with a sparse trace-one SDP reduction, a public original Newton right-hand
side, and a sharp raw-access lower bound.  No claim of priority is made without a
broader literature search.

## 1. Orthogonal word and sparse copied cone

Fix an orthogonal representation \(U:G\to O(d)\) of a finite group and put
\[
k=3d.
\]
Let \(g_1,\ldots,g_N\in G\) be the input symbols and define the ordered word and its
representation by
\[
w=g_Ng_{N-1}\cdots g_1,
\qquad
W=U_w=U_{g_N}\cdots U_{g_1}. \tag{1}
\]
As before, set
\[
K=16N,\qquad P=2K+N=33N,
\qquad q=\frac KP=\frac{16}{33}. \tag{2}
\]
There are \(P\) blocks \(X_i\in S_+^k\).  Consecutive blocks satisfy
\[
X_i=\mathcal D_iX_{i-1}\mathcal D_i^T, \tag{3}
\]
where the first \(K-1\) and final \(K\) transports are identity and the intervening
\(N\) transports, in input order, are
\[
\mathcal D_{g_j}=\operatorname{diag}(U_{g_j},I_d,I_d). \tag{4}
\]
Add the public normalization
\[
\operatorname{tr}X_0=1. \tag{5}
\]
Writing \(R_0=I_k\) and \(R_i=\mathcal D_i\cdots\mathcal D_1\), the feasible set is
exactly
\[
X_i=R_iZR_i^T,
\qquad Z\succeq0,\quad \operatorname{tr}Z=1. \tag{6}
\]
It is therefore linearly isomorphic to the full density spectrahedron in dimension
\(k\).  Its conic hull is \(S_+^k\), which has no lift over a finite product of
second-order cones for \(k\ge3\).

For completeness, the compact-base homogenization has no closure loophole.
If the density spectrahedron had a lift
\(\{\pi(y):y\in{\cal K},Ay=b\}\) over a finite product of Lorentz cones,
replace \(Ay=b\) by \(Ay=tb\) and impose \(t\ge0\).  For \(t>0\), the matrix
projection is exactly \(t\) times a density matrix.  For \(t=0\), any
homogeneous lift direction \(y\in{\cal K}\cap\ker A\) can be added with
arbitrary nonnegative scale to one feasible lift; compactness forces
\(\pi(y)=0\).  The homogenized projection is therefore exactly \(S_+^k\).
Fawzi's no-lift theorem for \(S_+^3\), together with the fact that \(S_+^3\)
is a face of \(S_+^k\), gives the stated conclusion for every \(k\ge3\).

If every \(U_g\) is a signed permutation, congruence in Frobenius-isometric svec
coordinates is also a signed permutation.  Explicitly, if a signed permutation sends
\(e_a\) to \(\varepsilon_a e_{\pi(a)}\), it sends the diagonal svec basis element
\(E_{aa}\) to \(E_{\pi(a)\pi(a)}\), and sends
\((E_{ab}+E_{ba})/\sqrt2\) to \(\varepsilon_a\varepsilon_b\) times the corresponding
normalized off-diagonal basis element.  Thus no \(\sqrt2\) factors enter the scalar
copy coefficients.  Every scalar copy row in (3) then has
exactly two nonzeros of magnitude one, and every scalar block-coordinate occurs in at
most two equality rows, including (5).  The trace row has \(k\) nonzeros.  Thus for
every fixed representation the scalar row and column degrees are bounded constants.
The explicit nonabelian example below uses ordinary permutation matrices and \(k=9\).

The equality matrix has full row rank
\[
\frac{k(k+1)}2(P-1)+1, \tag{7}
\]
leaving the \(k(k+1)/2-1\)-dimensional trace-zero root tangent space.  To see
this directly, order the copy rows by block.  Each new block appears with an
identity coefficient in its own \(k(k+1)/2\) rows, so the copy rows are
independent.  Their kernel is exactly the \(k(k+1)/2\)-dimensional root family
(6).  The trace row is nonzero on that kernel (take \(Z=I_k\)), and hence is
independent of all copy rows.

## 2. Public costs and the connection triangle

For a \(d\times d\) matrix \(T\), let \(H_{ab}(T)\) be the symmetric \(3d\times3d\)
block matrix with \(T\) in block \((a,b)\), \(T^T\) in block \((b,a)\), and zeros
elsewhere.  Set
\[
u=\frac1{10},\qquad \gamma=\frac uq=\frac{33}{160}. \tag{8}
\]
The public local costs are
\[
C_i=\begin{cases}
kI_k+uH_{23}(I_d)+\gamma H_{12}(I_d),&0\le i<K,\\
kI_k+uH_{23}(I_d),&K\le i<K+N,\\
kI_k+uH_{23}(I_d)+\gamma H_{13}(I_d),&K+N\le i<P.
\end{cases} \tag{9}
\]
The anisotropic part of every local cost has operator norm at most
\(\sqrt{u^2+\gamma^2}<1/4\).  Hence all local costs are positive definite, with
spectrum in \((k-1/4,k+1/4)\), uniformly in \(N\) and the word.

Consider the averaged trace-one SDP
\[
\min\left\{\frac1P\sum_i\langle C_i,X_i\rangle:(3),(5),\ X_i\succeq0\right\}. \tag{10}
\]
The primal is strictly feasible at \(X_i=I_k/k\).  The dual is strictly feasible by
taking every equality multiplier to be zero and every block slack to be \(C_i/P\).
Thus both Slater conditions hold.  The feasible set is compact by (6), so
the primal optimum is attained; conic strong duality gives dual attainment
and equality of the primal and dual optimal values.

The baseline edge \(H_{23}(I_d)\) is invariant under every \(R_i\).  The first anchor
is in the root frame, and the last anchor is pulled through
\(\operatorname{diag}(W,I_d,I_d)\).  Since \(q\gamma=u\), (10) eliminates exactly to
\[
\min\{\langle\overline C_W,Z\rangle:Z\succeq0,\ \operatorname{tr}Z=1\}, \tag{11}
\]
where
\[
\overline C_W=kI_k+uA_W,
\qquad
A_W=\begin{pmatrix}
0&I_d&W^T\\
I_d&0&I_d\\
W&I_d&0
\end{pmatrix}. \tag{12}
\]
The matrix \(A_W\) is the connection adjacency of a triangle whose holonomy is \(W\).
For every \(Q\in O(d)\),
\[
A_{Q^TWQ}=\operatorname{diag}(Q,Q,Q)^TA_W
\operatorname{diag}(Q,Q,Q). \tag{13}
\]
Thus its spectrum, and every scalar optimization output in (11), depends only on the
orthogonal conjugacy class of the holonomy.  This is a gauge-invariant word observable,
not a coordinate label at the end of a path.

## 3. Exact holonomy-spectrum formula

Let \(e^{i\theta}\) be an eigenvalue of the complexification of \(W\).  On the
three-dimensional sector generated by a corresponding eigenvector, \(A_W\) becomes
\[
\begin{pmatrix}
0&1&e^{-i\theta}\\
1&0&1\\
e^{i\theta}&1&0
\end{pmatrix}. \tag{14}
\]
Its characteristic equation is
\[
\lambda^3-3\lambda-2\cos\theta=0. \tag{15}
\]
Consequently
\[
\operatorname{spec}(A_W)=
\bigcup_{e^{i\theta}\in\operatorname{spec}(W)}
\left\{2\cos\frac{\theta+2\pi\ell}{3}:\ell=0,1,2\right\}, \tag{16}
\]
with algebraic multiplicity.  In particular, the exact scalar optimum is
\[
v(W)=k+u\min_{e^{i\theta}\in\operatorname{spec}(W),\ \ell\in\{0,1,2\}}
2\cos\frac{\theta+2\pi\ell}{3}. \tag{17}
\]
Equation (17) is a class function of the represented word.  Whenever two promised word
classes give separated values of (17), estimating the SDP optimum transfers the query
complexity of distinguishing those word classes.

## 4. Explicit nonabelian example: all conjugacy classes of \(S_3\)

Take the natural permutation representation of \(S_3\) on three symbols.  Then
\(d=3\) and every SDP block is \(k=9\) dimensional.  The represented eigenphases are
\[
\begin{array}{c|c}
\text{conjugacy class}&\operatorname{spec}(W)\\ \hline
\text{identity}&1,1,1\\
\text{transposition}&1,1,-1\\
\text{three-cycle}&1,e^{2\pi i/3},e^{-2\pi i/3}.
\end{array} \tag{18}
\]
Using (16),
\[
\lambda_{\min}(A_W)=
\begin{cases}
-1,&w=e,\\
-2,&w\text{ is a transposition},\\
2\cos(8\pi/9),&w\text{ is a three-cycle}.
\end{cases} \tag{19}
\]
The three values are distinct.  Therefore the scalar optimum of one fixed sparse SDP
family identifies all three conjugacy classes:
\[
v(W)=
\begin{cases}
89/10,&w=e,\\
44/5,&w\text{ is a transposition},\\
9+\frac15\cos(8\pi/9),&w\text{ is a three-cycle}.
\end{cases} \tag{20}
\]
This is genuinely nonabelian information.  It cannot be removed by a root-frame
orthogonal gauge because the three effective costs have different spectra and different
scalar optima.  More precisely, this class function does not factor through the
abelianization \(S_3/[S_3,S_3]\cong\mathbb Z_2\): the identity and three-cycles have
the same image in the abelianization but different values in (20).  This observation
concerns the unrestricted scalar observable, not the query-hard promise in Section 5.

## 5. Linear raw-query lower bound for the scalar optimum

Restrict each input symbol to \(g_j\in\{e,t\}\), where \(t\) is one fixed
transposition.  Then
\[
w=t^{z_1+\cdots+z_N}
\]
is the identity for even parity and a transposition for odd parity.  The two optimal
values in (20) differ by exactly \(1/10\).  Thus additive error smaller than \(1/20\)
determines parity by thresholding at \(177/20\).  The same threshold works
for relative error \(1/200\), because
\[
\frac{199}{200}\frac{89}{10}>\frac{177}{20}
>\frac{201}{200}\frac{44}{5}.
\]
More generally, the two relative-error intervals are disjoint exactly below
the minimax radius \(1/177\).

The raw coherent sparse oracle must include the **position oracle**, not only a value
oracle on a fixed support.  For a permutation congruence, the two coefficient values
are public, but the predecessor scalar coordinate is selected by the local permutation
and is therefore input dependent.  Fix a public enumeration in which one slot is the
current-block coordinate and the other is the predecessor-block coordinate.  Under
the restricted promise, the latter location is one of two public column indices,
selected by \(z_j\); column access has the same property because \(t=t^{-1}\).

This gives a constant-query simulation, but its exact constant depends on the sparse
oracle convention.  A clean-output position oracle, whose specified action is to
write the answer in a blank register, can be simulated with one bit query followed by
a public reversible decoding of the two candidates (and its inverse is simulated in
reverse with one query).  By contrast, the canonical XOR convention
\[
 |r,\ell,c\rangle\longmapsto
 |r,\ell,c\mathbin\oplus f_z(r,\ell)\rangle
\]
on an arbitrary target \(c\) is always simulated with two bit queries: compute the
selector, XOR the selected public index, and uncompute the selector.  A public dummy
index handles input-independent branches coherently.  The value oracle needs no input
query.  All of these simulations are coherent over row or column queries in
superposition.  (For an unrestricted group alphabet the binary one-query structured
encoding is unavailable in general, but a constant-query simulation applies when a
group-symbol query returns the whole fixed-size symbol.)  The quantum query lower
bound for parity therefore gives:

> **Theorem 1 (\(S_3\) holonomy-value hardness under a parity restriction).**  In the \(S_3\) family above,
> estimating the scalar optimum of (10) to additive error \(1/25\), with bounded
> failure probability, requires \(\Omega(N)=\Omega(P)\) raw coherent sparse-matrix
> queries.  The same holds for relative error \(1/200\).  These statements remain
> true under the two-symbol restriction \(\{e,t\}\), while the
> unrestricted scalar optimum distinguishes all three conjugacy classes of the group
> word.

For fixed \(d\), the total scalar input dimension and number of nonzeros are
\(\Theta(P)\), so this is a linear lower bound in the displayed instance size.

## 6. Public-start, condition-one Newton theorem

At the public point
\[
X_i^{(0)}=I_k/k, \tag{21}
\]
all copy constraints and the trace constraint are exactly satisfied for every word.
Use product log-det barrier parameter
\[
\mu=1/P. \tag{22}
\]
For the averaged objective in (10), the original-coordinate gradient and Hessian at
(21) are
\[
g_i=\frac1P(C_i-kI_k),
\qquad
\mathcal H_i[Y]=\frac{k^2}{P}Y. \tag{23}
\]
The gradient, equality residual, and hence the complete original KKT right-hand side
are public.  Its norm is input independent:
\[
\|g\|_2^2=\frac{2d}{P}\left(u^2+2q\gamma^2\right),
\qquad
\|g\|_2^2=\frac{123}{400P}\quad\text{for the \(S_3\) example}. \tag{23a}
\]
The ambient Hessian is a scalar identity.
Writing \(\widetilde A_g\) for all copy rows and the trace row, one fixed
multiplier convention gives the complete scalar Newton system
\[
\begin{pmatrix}
(k^2/P)I&\widetilde A_g^T\\
\widetilde A_g&0
\end{pmatrix}
\binom{\Delta x}{y'}
=\binom{-g}{0}.                                           \tag{23c}
\]
Both vector right-hand sides are therefore public; the local transports
occur only in the sparse matrix on the left.

Every feasible direction is \(\Delta X_i=R_iYR_i^T\) with \(\operatorname{tr}Y=0\).
The map
\[
\mathcal W_g(Y)=\frac1{\sqrt P}
 (R_0YR_0^T,\ldots,R_{P-1}YR_{P-1}^T)                    \tag{23b}
\]
is an exact Frobenius isometry on that tangent.  Consequently
\[
\mathcal W_g^*\mathcal H\mathcal W_g=\frac{k^2}{P}I,
\]
in every Frobenius-orthonormal basis of the trace-zero symmetric space.
In the unnormalized physical root coordinate, the same reduced Newton
objective has gradient \(uA_W\) and Hessian \(k^2I\).  Since
\(\operatorname{tr}A_W=0\), the
exact root direction is
\[
\Delta Z_W=-\frac{u}{k^2}A_W. \tag{24}
\]
It is nonzero for every orthogonal \(W\), and
\[
\|\Delta Z_W\|_F^2=\frac{6du^2}{k^4}. \tag{24a}
\]
Thus its normalization is public and independent of the word; there is no hidden
variable norm or zero-direction sector in the state-output reduction.
Both the ambient and equality-reduced Hessians have condition number exactly one.
Moreover \(\|A_W\|\le2\) by (16), so
\[
\lambda_{\min}(I_k/k+\Delta Z_W)
\ge\frac1k-\frac{2u}{k^2}>0. \tag{25}
\]
The undamped full Newton step is strictly positive definite.

The decrement is also exact.  Orthogonality of \(W\) gives
\(\|A_W\|_F^2=6d=2k\), and hence
\[
\lambda^2
=\left\langle uA_W,(k^2I)^{-1}uA_W\right\rangle
=\frac{2u^2}{k},
\qquad
\lambda=u\sqrt{\frac2k}.                                  \tag{25a}
\]
For \(S_3\), \(k=9\) and \(\lambda=\sqrt2/30<1/20\).
The restriction of the product-barrier objective to the feasible affine
space is the standard self-concordant function
\(\langle\overline C_W,Z\rangle-\log\det Z\).  Therefore the Dikin theorem
guarantees the full step stays in its domain and
\[
\lambda_{\rm next}
\le\left(\frac{\lambda}{1-\lambda}\right)^2
=\frac{2u^2/k}{(1-u\sqrt{2/k})^2}.                         \tag{25b}
\]
In the \(S_3\) example this is
\(2/(30-\sqrt2)^2<1/400\).
This is a universal Newton-decrement statement, not a claim about a
paper-specific primal--dual neighborhood.
In the \(S_3\) example, (25) also gives the uniform post-step eigenvalue
margin \(44/405\).

In the \(S_3\) example, \(\|A_W\|_F^2=6d=18\).  For the identity and a
transposition \(t\),
\[
\frac{\langle A_I,A_{U_t}\rangle_F}{\|A_I\|_F\|A_{U_t}\|_F}
=\frac{4d+2\operatorname{tr}U_t}{6d}
=\frac79. \tag{26}
\]
With the convention
\(D_{\rm tr}(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1\), the two normalized
root-direction pure states therefore have trace distance
\[
\sqrt{1-(7/9)^2}=\frac{4\sqrt2}{9}. \tag{27}
\]
Both target states, including the fixed transposition \(t\), are public.  The symmetric
Helstrom measurement is therefore a fixed public measurement and, on either promise,
has conditional success probability
\[
\frac12\left(1+\frac{4\sqrt2}{9}\right)>0.81. \tag{27a}
\]
This decoder also covers arbitrary mixed outputs.  If the returned state is within
trace distance \(\delta\) of the appropriate target, every fixed POVM outcome
probability changes by at most \(\delta\), so (27a) decreases by at most \(\delta\).

There is also an elementary fixed observable.  Let \(\Pi\) project onto the three
svec coordinates corresponding to diagonal entries of the \((1,3)\) connection
block.  Frobenius isometry of svec gives \(\Pr(\Pi)=1/3\) for the identity and
\(1/9\) for a transposition.  The projector alone is not yet a bounded-error decision
rule on both promises.  The two-outcome POVM whose ``identity'' effect is
\[
E_e=\frac5{14}I+\frac9{14}\Pi \tag{27b}
\]
has success probability \(4/7\) on each promise, and a constant number of repetitions
amplifies that bias.  The Helstrom decoder already remains above \(2/3\) from one
returned state when \(\delta=1/100\).

The same raw parity reduction proves:

> **Theorem 2 (\(S_3\) condition-one Newton hardness under a parity restriction).**  From the public feasible
> point (21), public gradient (23), and public original KKT right-hand side, preparing
> any possibly mixed output state within trace distance \(1/100\) of the normalized
> free root primal Newton direction (24)
> requires \(\Omega(N)=\Omega(P)\) raw coherent coefficient queries.  The ambient and
> equality-reduced Hessians have condition number one.  The exact Newton decrement is
> \(\sqrt2/30\); the undamped step has minimum-eigenvalue margin at least \(44/405\),
> remains uniformly interior, and its next decrement is less than \(1/400\).

This output theorem uses the canonical natural-permutation basis and a fixed root
frame.  The scalar optimum is invariant under an arbitrary simultaneous orthogonal
gauge by (13), whereas the coordinates of the direction state and the explicit
projector \(\Pi\) are not.  A common **public** gauge conjugates both targets by the
same known svec unitary, preserving their overlap and optimal distinguishability.  An
unknown or input-dependent gauge would have to be supplied or learned and is outside
the fixed-measurement claim.

### 6.1 Complete KKT-state hardness on the parity restriction

The complete primal-plus-multiplier KKT state is also hard under the
two-symbol restriction.  Fix a public orthogonal matrix \(Q\) with
\[
Q^TU_tQ=\operatorname{diag}(-1,1,1).
\]
Applying \(\operatorname{diag}(Q,Q,Q)\) within every \(9\times9\) block is
a public coordinate change.  Apply the induced Frobenius-orthogonal
coordinate change also to every matrix-valued copy row and its multiplier;
the scalar trace row is fixed.  Thus the norm of the complete KKT vector is
preserved, and the corresponding observable can be conjugated back to the
original fixed row ordering.  The change leaves all cost couplings
\(H_{ab}(I_3)\), the trace row, and the scalar Hessian invariant.  The
nonzero KKT solution lies in the orthogonal direct sum of three outer
qutrit modes.  Two modes see only \(+1\) transports, while the remaining
mode sees the signed path with final parity \(h\).  The other cross-mode
sectors are present in the full system but have zero right-hand side and,
by nonsingularity of the KKT matrix, zero solution.

Use the KKT convention (23c), put
\[
\alpha=\frac{16}{33},\qquad
\beta=\frac{81}{P},\qquad
c=\frac{\sqrt2\gamma}{P},\qquad
d_0=\frac{\sqrt2u}{81},
\]
and let \(\tau_i\) be the prefix parity in the signed mode.  In each mode
the three active primal chains have amplitudes
\[
d_{12,i}=-d_0\tau_i,\qquad
d_{13,i}=-d_0h\tau_i,\qquad
d_{23,i}=-d_0,                                      \tag{30}
\]
where \(h=+1\) and \(\tau_i=1\) identically in either public mode.  Define
the public edge tent
\[
v_e=\begin{cases}
c(1-\alpha)e,&1\le e\le K,\\
c\alpha(P-e),&K<e<P.
\end{cases}                                         \tag{31}
\]
The only active copy multipliers in a mode are
\[
y'_{12,e}=\tau_ev_e,\qquad
y'_{13,e}=-h\tau_ev_{P-e};                           \tag{32}
\]
the \(23\) multiplier vanishes.  All cross-mode, diagonal, and trace-row
components vanish because their public right-hand sides are zero.  These
formulas follow from the signed-incidence gauge
\(B_\sigma=S_\tau BT_\tau\).

Let
\[
D=P d_0^2=\frac{11N}{109350},\quad
V=\sum_ev_e^2=\frac{289N}{4950}+\frac{17}{158400N},\quad
C=\sum_ev_ev_{P-e}=\frac{577N}{9900}+\frac1{9900N}.   \tag{33}
\]
Every mode has complete KKT norm squared \(3D+2V\).  Let
\(T_{\rm sign}\) swap the \(12\) and \(13\) primal coordinates and their
same-edge copy multipliers only in the signed internal mode, acting as zero
on both public modes and all other coordinates.  Conjugating back by the
fixed \(Q\) gives a public norm-one observable in the original coordinates.
On the normalized complete three-mode KKT solution,
\[
\langle T_{\rm sign}\rangle
=\frac{2h(D-C)}{3(3D+2V)}.                            \tag{34}
\]
Its sign is \(-h\), and for every \(N\ge1\),
\[
\left|\langle T_{\rm sign}\rangle\right|
=\frac{2239504N^2+3888}{6759216N^2+12393}
>\frac{33}{100}.                                     \tag{35}
\]
The inequality follows by cross multiplication: after subtracting
\(33/100\), the numerator is positive at \(N=1\) and its \(N^2\)
coefficient is positive.  The expectation tends to
\(139969/422451\approx0.331326\).

Use the two-outcome POVM \((I\mp T_{\rm sign})/2\), with the outcome labels
chosen using the known sign in (34).  Its ideal success probability is
\((1+|\langle T_{\rm sign}\rangle|)/2>0.665\) on either promise.  Trace
distance \(1/100\) changes either outcome probability by at most \(1/100\),
so its success remains above \(0.655\) for an arbitrary mixed returned state.
Three independent preparations and majority vote then exceed conventional
bounded error.  Therefore:

> **Theorem 2a (complete KKT-state hardness).**  On the \(S_3\)
> identity/transposition restriction, preparing the normalized complete
> solution \((\Delta x,y')\) of (23c), in the displayed unit-scaled equality
> rows and multiplier convention, to trace distance \(1/100\) requires
> \(\Omega(N)=\Omega(P)\) raw coefficient queries.

This is not a representation-invariant multiplier theorem: arbitrary row
rescaling changes the normalized multiplier sector.  The public \(Q\) above
is fixed once the transposition promise is fixed and costs no input query.

### 6.2 A fixed decoder for the global primal direction

The transposition restriction also gives a decoder that is invariant under
every prefix permutation.  Let \(J\) swap corresponding isometric-svec
coordinates in the \((1,2)\) and \((1,3)\) \(d\times d\) off-diagonal
blocks, and act as zero elsewhere.  On physical block \(i\), those two
matrix blocks of \(R_iA_WR_i^T\) are respectively
\(U_i\) and \(U_iW^T\), where \(U_i\) is the prefix permutation.  Hence

\[
 {\langle R_iA_WR_i^T,J(R_iA_WR_i^T)\rangle_F\over\|A_W\|_F^2}
 ={4\operatorname{tr}(U_i^TU_iW^T)\over6d}
 ={2\operatorname{tr}W\over3d}.
\tag{D1}
\]

The factor four in the numerator consists of the two Frobenius-isometric
cross terms created by the swap; omitting either term gives an incorrect
decoder.  For \(d=3\), (D1) equals \(2/3\) for the identity and \(2/9\) for the
fixed transposition.  The centered contraction

\[
                         T_G={9\over13}J-{4\over13}I
\tag{D2}
\]

has operator norm one: the eigenvalues of \(J\) lie in
\(\{-1,0,1\}\).  Writing \(h=+1\) for even parity and \(h=-1\) for odd
parity, (D1) gives

\[
 \langle T_G\rangle={2h\over13}
\tag{D3}
\]

on the normalized root direction and on every normalized physical block.
The direct sum of \(T_G\) therefore has the same expectation on the
normalized global primal direction.  The POVM \((I\pm T_G)/2\) has fixed
ideal success probability \(15/26\) on either promise.  Trace-distance error
\(1/100\), including for a mixed output, leaves success at least
\(15/26-1/100>0.56\); a constant number of repetitions reaches bounded
error.  Thus Theorem 2 also holds for the normalized global primal
Newton-direction state.

### 6.3 A canonical one-symbol-query KKT block encoding

The fact that a permutation symbol moves support positions requires a
different construction from a sign-only state preparation.  On the promise
\(g_j\in\{e,t\}\), the induced svec permutation \(\pi_t\) is an
involution, hence a disjoint union of public transpositions and fixed points.
One standard bit-symbol query can therefore apply
\(\pi_t^{z_j}\) to a coordinate label by XORing the orbit bit, without
computing and later uncomputing \(z_j\).

Put \(s=k(k+1)/2=45\), let
\(A_\sigma\in\mathbb R^{[s(P-1)+1]\times sP}\) be the copy-plus-trace
equality matrix, and label the two slots of copy row \((i,\ell)\) by
\(\lvert i,\ell,{\rm cur}\rangle\) and
\(\lvert i,\ell,{\rm pred}\rangle\).  Give each of the nine trace-row
slots its own public token.  Define the public row states with amplitude
\(1/3\) on every occupied token and the remaining amplitude on a distinct
row-failure label.  Thus a copy row has failure amplitude \(\sqrt{7/9}\),
while the trace row has no failure arm.

For primal column \((v,c)\), the column state has amplitude \(+1/3\) on
its current-row token when \(v\ge1\), amplitude \(-1/3\) on the outgoing
predecessor token

\[
                  \lvert v+1,\pi_{g_{v+1}}(c),{\rm pred}\rangle
\tag{BE1}
\]

when \(v<P-1\), and amplitude \(+1/3\) on its trace token when \(v=0\)
and \(c\) is diagonal.  A distinct column-failure label supplies the
remaining norm.  Every column has at most two tokens.  Bijectivity of
\(\pi_g\) makes the column supports disjoint, so both state families are
orthonormal.  Their overlap is exactly \((A_\sigma)_{rc}/9\).

Let \(L\) be a public unitary completion of the row-state preparation, and
let \(R_0\) prepare the column states with all hidden symbols set to the
identity.  These completions can be fixed as direct sums of public
constant-dimensional Householder reflections, with a public bijection on
unused basis states.  Let \(S_\sigma\) apply \(\pi_t^{z_j}\) to the
coordinate component of precisely the predecessor tokens on hidden edge
\(j\), acting identically elsewhere.  The orbit-bit implementation above,
routed to a public dummy symbol off those tokens and on every fixed-point
orbit of \(\pi_t\), uses one coherent symbol query.  Therefore

\[
 U_A=L^\dagger S_\sigma R_0,
 \qquad
 \langle0,r|U_A|0,c\rangle={(A_\sigma)_{rc}\over9}
\tag{BE2}
\]

is an exact normalization-nine rectangular projected-unitary encoding with
a fully public completion except for one local symbol query.

The Newton KKT matrix is

\[
 M_\sigma=
 \begin{pmatrix}(k^2/P)I&A_\sigma^T\\A_\sigma&0\end{pmatrix}
 =\mathscr A_\sigma+{k^2\over P}P_x,
 \qquad
 \mathscr A_\sigma=
 \begin{pmatrix}0&A_\sigma^T\\A_\sigma&0\end{pmatrix},
\tag{BE3}
\]

where \(P_x\) is the public primal-sector projector.  A side-qubit
multiplexing of \(U_A\) and \(U_A^\dagger\), followed by a public reordering,
block encodes \(\mathscr A_\sigma/9\).  The two branches have the forms
\(L^\dagger S_\sigma R_0\) and \(R_0^\dagger S_\sigma L\), so one common
middle call to \(S_\sigma\) implements the multiplexor with one symbol
query.  A two-term LCU with the public block encoding of \(P_x\) then gives
an exact block encoding of \(M_\sigma/\alpha_M\), where

\[
                  \alpha_M=9+{81\over P}<12.
\tag{BE4}
\]

All LCU rotations, invalid-address behavior, and junk completions are public.
A dummy identity symbol is queried on the \(P_x\) branch, so every ordinary,
adjoint, or externally controlled call uses at most one symbol query.

The KKT right-hand side, root/global layouts, decoder (D2), and the
publicly conjugated complete-state observable \(T_{\rm sign}\) from
Section 6.1 are public.  Replacing each canonical KKT call by its one-query
implementation and using (D3) or (35) proves the following sharp constant.
Indeed, trace-distance error \(1/100\) changes the expectation of a
norm-one observable by at most \(2/100\), so the measured expectation still
has the parity sign on every input.  That expectation is a real polynomial
of degree at most \(2q_{\rm BE}\) in the input bits.  Since the sign degree
of parity is \(N\), one has \(2q_{\rm BE}\ge N\); no success-probability
amplification is needed for this exact call count.

> **Theorem 3 (canonical group-KKT access).**  On the
> \(S_3\), \(\{e,t\}\) promise, preparing the normalized root primal,
> global primal, or complete primal-plus-multiplier Newton state to trace
> distance \(1/100\) from the canonical encoding above requires
> \[
>                         q_{\rm BE}\ge\lceil N/2\rceil=\Omega(P)
> \tag{BE5}
> \]
> block-encoding, adjoint, or controlled calls.

This is relative to the displayed completion.  An arbitrary
input-dependent completion supplied at unit cost could store the whole word
or its conjugacy class in junk blocks.  Any queries used to construct a
different completion must be charged.

### 6.4 Tangent-projector synthesis lower bound

Let \(\Pi_\sigma\) be the Euclidean projector onto the kernel of the full
copy-plus-trace equality matrix.  Projecting the Newton equation gives

\[
                  \Pi_\sigma g=-{k^2\over P}\Delta x.
\tag{NP1}
\]

For \(k=9,d=3\), equations (23)--(24) and
\(\|A_W\|_F^2=18\) give

\[
 \|\Delta x\|_2^2=P{u^2\over k^4}\,18={P\over36450},
 \qquad
 \|\Pi_\sigma g\|_2^2={9\over50P}.
\tag{NP2}
\]

The public gradient contains only the three mutually orthogonal connection
blocks, and \(\|H_{ab}(I_d)\|_F^2=2d=6\).  Hence

\[
 \|g\|_2^2={6u^2+12q\gamma^2\over P}={123\over400P},
 \qquad
 \|\Pi_\sigma|\widehat g\rangle\|_2^2={24\over41},
 \quad |\widehat g\rangle={g\over\|g\|_2}.
\tag{NP3}
\]

Conditional on the projector signal, the output is the normalized global
direction, so (D3) gives the unconditioned signed expectation

\[
                         h\,\langle T_G\rangle={48\over533}.
\tag{NP4}
\]

Suppose a raw-query circuit synthesizes a normalization-one block encoding
with principal block \(B_\sigma\) satisfying
\(\|B_\sigma-\Pi_\sigma\|\le\varepsilon\).  Apply it once to the public
state \(|\widehat g\rangle\), and measure \(T_G\) on the signal sector and
zero on junk.  With \(v=\Pi_\sigma|\widehat g\rangle\) and
\(e=(B_\sigma-\Pi_\sigma)|\widehat g\rangle\), the usual cross-term bound
gives

\[
 h\,\langle T_G\rangle
 \ge {48\over533}-2\sqrt{24\over41}\,\varepsilon-\varepsilon^2
 >0.065,
 \qquad \varepsilon\le{1\over64}.
\tag{NP5}
\]

The one-call output has a fixed positive parity bias.  Equivalently it can
be amplified a constant number of times to the conventional \(2/3\)
success threshold.  The sign-degree form of the parity polynomial bound
already yields the sharp query statement: its one-run acceptance
probability minus \(1/2\) sign-represents parity and has degree at most
twice the total number of setup-plus-call queries.

> **Theorem 4 (group tangent-projector synthesis).**  Any uniform raw-symbol
> query circuit that, for every \(\{e,t\}\) input, synthesizes a
> normalization-one block encoding of \(\Pi_\sigma\) to operator error
> \(1/64\) uses at least \(\lceil N/2\rceil=\Omega(P)\) raw queries,
> counting setup and the first usable call.

Thus \(q_{\rm setup}+q_{\rm call}\ge\lceil N/2\rceil\).  After linear
setup, later calls may be cheap.  The proof permits any completion actually
built by the counted circuit because it reads only the principal block.  A
projector oracle, prefix transports, or the word supplied for free changes
the access model; in that model one projector call already reveals parity.

The synthesis bound is tight up to a constant.  Let \(\rho_i\) be the
isometric-svec permutation induced by congruence with \(R_i\), and define
the isometry
\[
 W_\sigma|c\rangle={1\over\sqrt P}\sum_{i=0}^{P-1}
       |i,\rho_i(c)\rangle .
\tag{NP6}
\]
Let \(|\operatorname{tr}\rangle=k^{-1/2}\sum_{a=1}^k|aa\rangle\) and
\(Q_0=I-|\operatorname{tr}\rangle\langle\operatorname{tr}|\).  The exact
tangent projector is
\[
                         \Pi_\sigma=W_\sigma Q_0W_\sigma^\dagger .
\tag{NP7}
\]
To implement \(W_\sigma\), first prepare the public uniform node state.
For hidden edge \(j\), condition on the node lying beyond that edge and
apply the induced involution \(\pi_t^{z_j}\) to the svec coordinate.  In
the public orbit-bit encoding used above, one raw symbol query performs
that controlled involution.  Doing this for all \(N\) hidden edges costs
exactly \(N\) queries; reversing the sequence implements
\(W_\sigma^\dagger\).  Conjugating the public normalization-one block
encoding of \(|0\rangle\langle0|\otimes Q_0\) by these two circuits gives
an exact normalization-one block encoding of \(\Pi_\sigma\) with \(2N\)
raw queries.  It uses \(O(N\log P)\) elementary gates and logarithmic
workspace under the standard arithmetic model.  Hence Theorem 4 identifies
a tight \(\Theta(N)\) first-synthesis cost, not a repeated-call lower bound.

## 7. The scalar primal-barrier KKT graph is a forest

For permutation representations, each svec congruence in (3) is a permutation.  At the
public point (21), ignore diagonal self-loops from the scalar Hessian and view the
symmetric saddle KKT sparsity graph for the equality-constrained primal-barrier Newton
system as a bipartite graph of primal scalar variables and equality-multiplier variables.
The copy constraints form disjoint subdivided paths: bijectivity prevents paths from
branching or merging.  Coordinate permutations may make these paths cross in a layer
drawing, but a perfect matching between consecutive layers cannot identify two path
vertices.  Moreover, congruence by a permutation matrix maps diagonal matrix units
bijectionally to diagonal matrix units.  The \(k\) root diagonal coordinates touched
by the trace row therefore lie on \(k\) distinct path components before that row is
added.  The trace multiplier in (5) joins precisely those components through one new
star vertex, which creates one tree and no cycle.  Every remaining off-diagonal path
stays a separate tree.  Hence this complete primal-barrier saddle KKT graph is
a forest and has treewidth one.  This is the two-by-two system with blocks
\((\mathcal H,\mathcal A^T;\mathcal A,0)\).  It does not assert that every
primal--dual SDP Newton symmetrization, after introducing separate slack and
complementarity variables, has the same graph.

Combining this observation with Theorem 2 gives the precise obstruction:

> **Corollary 3 (treewidth-one does not remove holonomy loading).**  Even when the
> original primal-barrier saddle KKT graph has treewidth one and the equality-reduced primal
> Hessian has condition number exactly one, producing the reduced Newton solution state
> from raw local coefficient access can require linear query work.  Sparse elimination
> makes the arithmetic solve linear-time classically; it does not make the accumulated
> group word available at sublinear raw-query cost.

This statement concerns total access work, not parallel depth, and it does not claim
that the indefinite unreduced KKT matrix is condition one.

## 8. Sharp setup-versus-iteration accounting

Let \(S\) be the number of raw input queries used to build any preprocessing state or
data structure, and let \(q_t\) be the additional raw queries used during iteration
\(t\).  Any end-to-end QIPM which eventually returns either an additive-\(1/25\)
optimal value, the root direction state in Theorem 2, or the canonically
normalized complete KKT state in Theorem 2a obeys, on the transposition promise,
\[
S+\sum_tq_t\ge N/4 \tag{28}
\]
under the canonical XOR position-oracle convention of Section 5, up to harmless
integer rounding.  Each raw query then costs at most two bit queries in the reduction,
and bounded-error parity costs at least \(N/2\) bit queries.  Under the clean structured
position-oracle convention admitting the one-query simulation, the right-hand side
improves to \(N/2\).  Either convention gives the stated \(\Omega(N)\) total bound and
permits arbitrary quantum preprocessing and adaptive iterations.

The accounting is sharp up to the access-convention constant and cannot be strengthened
to an \(\Omega(N)\) lower bound per iteration.  On the restricted promise, compute
parity once with \(\lceil N/2\rceil\)
queries, store one bit, and thereafter form every reduced cost, central matrix, and
Newton direction using constant-dimensional public arithmetic and no further input
queries.  For unrestricted fixed-size \(G\), a classical pass reads and multiplies the
\(N\) group symbols in \(O(N)\) work, after which each reduced iteration costs only a
constant depending on \(G\).  Recovering all original physical blocks additionally
requires the prefix transports; they can be built in the same linear pass and stored in
linear memory.

Therefore the strongest valid generic conclusion is a first-use/setup obstruction:
\[
\boxed{\text{linear setup plus cheap reuse, or linear total online access before the
first intrinsic output}.} \tag{29}
\]
Any oracle that supplies \(W\), its conjugacy class, a nullspace basis, or a prefix
table at unit cost has already performed the hard aggregation and lies outside the raw
local-input model.

## 9. Scope and novelty calibration

The gauge reduction and spectral identity (16) are standard connection-graph ideas.
Equation (16) is the elementary three-cycle specialization obtained by decomposing an
orthogonal connection into holonomy eigensectors and solving the resulting cubic.
Permutation representations and the parity query bound are also standard.  None of
these components should be advertised as a new group-theory or spectral-graph fact.

There is also an important limit on the phrase *nonabelian hardness*.  The unrestricted
\(S_3\) objective is genuinely nonabelian in the precise sense given after (20), but
Theorems 1 and 2 restrict every symbol to one fixed order-two subgroup.  Their
\(\Omega(N)\) exponent is exactly the ordinary parity lower bound.  The theorems do not
prove a lower bound for distinguishing conjugacy classes of a genuinely noncommuting
ordered-word promise.  Establishing such a lower bound in the same local-symbol model
would be a separate result.

The potentially publishable conjunction is:

1. a bounded-incidence trace-one SDP whose **unrestricted scalar optimum** is a
   nonabelian conjugacy-class observable;
2. a public feasible IPM start with public original Newton right-hand side and an
   exactly condition-one reduced Hessian;
3. a scalar primal-barrier saddle KKT graph of treewidth one;
4. a tight linear setup/query obstruction for the free Newton state and optimal value;
5. on the parity restriction, an explicit constant-normalization block encoding and a
   linear call lower bound also for the complete KKT solution state; and
6. a sharp linear raw-query synthesis bound for the normalization-one tangent
   projector, with an explicit \(2N\)-query construction.

The construction is more expressive than the signed triangle because the hidden
invariant may be an arbitrary represented group word and the explicit \(S_3\) instance
separates all three conjugacy classes.  It is not stronger in its proved query exponent:
the linear lower bound still comes from restricting the word problem to parity.

Relevant primary sources for the standard ingredients and the closest algorithmic
comparison are:

* T. Gao, J. Brodzki, and S. Mukherjee,
  [*The Geometry of Synchronization Problems and Learning Group Actions*](https://arxiv.org/abs/1610.09051),
  for edge potentials, gauge, holonomy, and connection Laplacians; and A. Bandeira,
  A. Singer, and D. Spielman,
  [*A Cheeger Inequality for the Graph Connection Laplacian*](https://arxiv.org/abs/1204.3873),
  for the orthogonal connection-Laplacian setting.
* N. Reff,
  [*Spectral Properties of Complex Unit Gain Graphs*](https://arxiv.org/abs/1110.4554),
  and R. Mehatari, M. R. Kannan, and A. Samanta,
  [*On the adjacency matrix of a complex unit gain graph*](https://arxiv.org/abs/1812.03747),
  for gain-adjacency spectral theory.  These sources make the gauge/holonomy mechanism
  and cycle-spectrum dependence clear precedents for Sections 2--3.  A recent scalar
  continuation is L. Torres-Hugas, J. Duch, S. Gómez, and A. Arenas,
  [*Cycle holonomy induces higher-order constraints and controls remote synchronization
  transitions via twisted Laplacian spectra*](https://arxiv.org/abs/2604.19682), which
  studies how \(U(1)\) cycle holonomy controls a twisted-Laplacian spectrum, not an SDP
  or a query lower bound.
* S. Ling,
  [*Solving Orthogonal Group Synchronization via Convex and Low-Rank Optimization*](https://arxiv.org/abs/2006.00902),
  for semidefinite relaxations of orthogonal synchronization.  That SDP literature uses
  connection-valued measurements, but it does not give the copied trace-one reduction,
  the class-function optimum (20), or the raw-query Newton theorem here.
* M. Zhandry,
  [*Quantum Oracle Classification---The Case of Group Structure*](https://arxiv.org/abs/1510.08352),
  exactly characterizes a broad class of group-structured oracle problems that includes
  parity, but assumes a commutative range group and a homomorphism of a sampled function
  oracle.  D. Copeland and J. Pommersheim,
  [*Quantum query complexity of symmetric oracle problems*](https://arxiv.org/abs/1812.09428),
  study groups of unitary oracles and coset identification.  Neither model is the ordered
  list of local noncommuting symbols whose product conjugacy class is requested here;
  more importantly, the present lower bound does not resolve that missing problem because
  it uses only \(\mathbb Z_2\) parity.
* B. Augustino, G. Nannicini, T. Terlaky, and L. F. Zuluaga,
  [*Quantum Interior Point Methods for Semidefinite Optimization*](https://arxiv.org/abs/2112.06025),
  for SDP Newton systems and nullspace-based feasible quantum IPMs.  J. van Apeldoorn,
  A. Gilyén, S. Gribling, and R. de Wolf,
  [*Quantum SDP-Solvers: Better upper and lower bounds*](https://arxiv.org/abs/1705.01843),
  give general quantum LP/SDP value lower bounds.  S. Apers and S. Gribling,
  [*Quantum speedups for linear programming via interior point methods*](https://arxiv.org/abs/2311.03215v3),
  also include sparse-LP coefficient-query lower bounds obtained by embedding Boolean
  query problems into optimum estimation.  Hence a linear quantum lower-bound exponent
  for an optimization value is not by itself new; the possible contribution is the
  explicit bounded-incidence holonomy SDP together with its public-start Newton geometry.
* Generic quantum-linear-system lower bounds, such as D. Orsucci and V. Dunjko,
  [*On solving classes of positive-definite quantum linear systems with quadratically
  improved runtime in the condition number*](https://arxiv.org/abs/2101.11868), and
  H. Mori, Y. Kikuchi, M. Benedetti, and M. Rosenkranz,
  [*Sparsity-dependent Complexity Lower Bound of Quantum Linear System Solvers*](https://arxiv.org/abs/2601.16697),
  and Q. Wang and Z. Zhang,
  [*Tight Quantum Depth Lower Bound for Solving Systems of Linear Equations*](https://arxiv.org/abs/2407.06012),
  do not by themselves imply Theorem 2 from the condition number of the reduced Hessian:
  that Hessian is the identity, while its nullspace loading and the original KKT matrix
  depend on the queried transports.  Mori et al. are nevertheless a close mechanism-level
  precedent: their public-right-hand-side sparse QLS family also uses a locally queried,
  parity-carrying propagation/history system and proves linear state-generation hardness.
  Thus the parity propagation and canonical local block-encoding mechanism in Theorems
  2a--3 should not be claimed as new QLS machinery.  What those QLS papers do not state
  is the trace-one SDP/KKT realization, its unrestricted conjugacy-class value observable,
  or its condition-one *reduced* Newton geometry.  Conversely, Theorems 2--3 make no
  condition-number claim for the indefinite unreduced KKT matrix, so they are not stronger
  generic QLS lower bounds and should not be called constant-condition QLS lower bounds.
* R. Beals, H. Buhrman, R. Cleve, M. Mosca, and R. de Wolf,
  [*Quantum lower bounds by polynomials*](https://arxiv.org/abs/quant-ph/9802049),
  for the parity query lower bound, and H. Fawzi,
  [*On representing the positive semidefinite cone using the second-order cone*](https://arxiv.org/abs/1610.04901),
  for the non-SOCP-lift statement.  Passing from the compact trace-one base to its conic
  hull in Section 1 is an elementary homogenization, not a new lift obstruction.

A targeted open-primary-source search through September 2, 2026 found the standard
connection/gain-graph ingredients, synchronization SDPs, group-oracle query frameworks,
generic quantum LP/SDP lower bounds, and quantum SDP-IPM upper bounds, but no prior source
with this explicit conjunction of a copied trace-one holonomy SDP, an unrestricted
nonabelian class-function optimum, a public-right-hand-side condition-one reduced Newton
step, treewidth-one scalar KKT sparsity, and the fixed-completion block-encoding statement.
The QLS-level propagation mechanism has a clear collision with prior parity/history-system
lower bounds; the apparently new part is the optimization-native conjunction, not that
mechanism or the linear exponent.  This is evidence against an obvious exact collision,
not proof of bibliographic priority.
