# A short-step, condition-one free-\(S_+^3\) Newton direction can require linear input work

## Status and theorem in one paragraph

This note strengthens the free-\(S_+^3\) central-state construction by moving the
lower bound to one Newton solve from a public, exactly feasible point.  The original
barrier gradient and KKT right-hand side are public, the ambient barrier Hessian is the
identity, and the equality-reduced Hessian has condition number exactly one.  All
constraint rows have two entries in \(\{-1,+1\}\), scalar row and column degree are at
most two, public cost matrices have eigenvalues in
\([1-1/(16\sqrt P),1+1/(16\sqrt P)]\), and the feasible cone is linearly
isomorphic to the genuinely non-SOCP cone \(S_+^3\).  The public start has exact
Newton decrement \(2/33\), inside the universal full-step neighborhood for a
standard self-concordant function.  Nevertheless, the
normalized free primal Newton direction consists of two orthogonal parity-dependent
states.  Preparing it, or the normalized full primal direction, to constant trace
distance from raw coherent sparse access, or from the canonical normalization-three
KKT block encoding in Section 4.3, requires \(\Omega(N)\) queries.  This is a
data-access lower bound.  A separate fixed-observable argument gives the same
linear bound for the normalized complete primal-plus-multiplier KKT solution.
The primal result is robust to a constant relative residual in the
equality-reduced system: relative residual \(\eta\) leaves signed decoder
bias at least \(1-2\eta^2\).  This statement does not apply to the unreduced
saddle KKT residual, because that matrix is separately ill-conditioned by
\(\Theta(P^2)\).

The same short-step instance gives a direct oracle-synthesis theorem:
constructing a normalization-one block encoding of the orthogonal projector
onto \(\ker A_\sigma\), to operator error \(1/16\), requires
\(\Omega(P)\) raw queries including setup.  One supplied projector call
otherwise exposes parity with constant bias.  This isolates the access cost
of the input-dependent nullspace projection itself.

## 1. Sparse SDP family

Let \(N\ge1\), \(K=16N\), and \(P=2K+N=33N\).  The input is
\(\sigma=(\sigma_1,\ldots,\sigma_N)\in\{-1,+1\}^N\), with parity
\[
p=\prod_{j=1}^N\sigma_j.
\]
There are \(P\) blocks \(X_i\in S_+^3\).  Consecutive blocks obey
\[
X_i=G_iX_{i-1}G_i^T, \tag{1}
\]
where the first \(K-1\) and final \(K\) edges have \(G_i=I_3\), while the intervening
\(N\) edges, in order, have
\[
G_i=D_{\sigma_j}:=\operatorname{diag}(\sigma_j,1,1). \tag{2}
\]
Define
\[
H_{12}=E_{12}+E_{21},\qquad H_{13}=E_{13}+E_{31}.
\]
Set the public anisotropy scale
\[
\delta_P=\frac1{16\sqrt P}. \tag{3a}
\]
The public block costs are
\[
C_i=\begin{cases}
I_3+\delta_PH_{12},&0\le i<K,\\
I_3,&K\le i<K+N,\\
I_3+\delta_PH_{13},&K+N\le i<P.
\end{cases} \tag{3}
\]
Thus every cost has spectrum in \([1-\delta_P,1+\delta_P]\).  The SDP is
\[
\min\left\{\sum_i\langle C_i,X_i\rangle:(1),\ X_i\succeq0\right\}. \tag{4}
\]

Let \(R_0=I_3\) and \(R_i=G_i\cdots G_1\).  The feasible cone is exactly
\[
(X_0,\ldots,X_{P-1})=(R_0ZR_0^T,\ldots,R_{P-1}ZR_{P-1}^T),
\qquad Z\in S_+^3. \tag{5}
\]
It is therefore linearly isomorphic to \(S_+^3\), which has no finite second-order
cone lift.  In particular, this is not an SOCP in disguise.

Use Frobenius-isometric coordinates
\[
\operatorname{svec}(X)=
(X_{11},\sqrt2X_{12},\sqrt2X_{13},X_{22},\sqrt2X_{23},X_{33}). \tag{6}
\]
Congruence by \(D_\sigma\) is the diagonal map
\[
Q_\sigma=\operatorname{diag}(1,\sigma,\sigma,1,1,1). \tag{7}
\]
Each edge therefore contributes six scalar rows, each with two nonzeros of magnitude
one.  Each scalar variable occurs in at most two rows.  A hidden bit affects exactly
two coefficient values on public locations.  The homogeneous right-hand side is zero.
The equality matrix \(A_\sigma\) has full row rank \(6(P-1)\), and
\(\dim\ker A_\sigma=6\).

## 2. A public feasible point and public original KKT right-hand side

Set the barrier parameter to \(\mu=1\) and take
\[
X_i^{(0)}=I_3\qquad(0\le i<P). \tag{8}
\]
This point is public, strictly positive definite, and exactly feasible for every input,
because every \(G_i\) is orthogonal.  For the primal barrier objective
\[
\Phi(X)=\sum_i\langle C_i,X_i\rangle-\sum_i\log\det X_i, \tag{9}
\]
the ambient block gradient and Hessian at (8) are
\[
g_i=C_i-I_3,
\qquad
\mathcal H_i[Y]=Y. \tag{10}
\]
Both are public.  Explicitly, \(g_i=\delta_PH_{12}\) on the first \(K\)
blocks, zero on the middle \(N\), and \(\delta_PH_{13}\) on the final \(K\).
Its complete svec norm is the absolute constant
\[
\|g\|_2^2=4K\delta_P^2=\frac1{132},
\qquad \|(-g,0)\|_2=\frac1{\sqrt{132}}. \tag{10a}
\]

In svec coordinates the equality-constrained Newton equations are
\[
\begin{bmatrix}
I&A_\sigma^T\\
A_\sigma&0
\end{bmatrix}
\begin{bmatrix}\Delta x\\\Delta y\end{bmatrix}
=-
\begin{bmatrix}g\\0\end{bmatrix}. \tag{11}
\]
The entire right-hand side is public: the primal residual is exactly zero and the
gradient is given above.  Only the sparse coefficient matrix on the left contains the
hidden signs.

## 3. Exact condition-one reduction and Newton direction

Every feasible primal direction has a unique root coordinate \(Y\in S^3\):
\[
\Delta X_i=R_iYR_i^T. \tag{12}
\]
Since every \(R_i\) is orthogonal,
\[
\sum_i\|\Delta X_i\|_F^2=P\|Y\|_F^2. \tag{13}
\]
The pullback of the public gradient is
\[
\begin{aligned}
g_{\mathrm{red}}
&=\sum_iR_i^Tg_iR_i\\
&=K\delta_P(H_{12}+pH_{13}).
\end{aligned} \tag{14}
\]
Here every first-group congruence is \(I_3\), every final-group congruence is \(D_p\),
and \(D_pH_{13}D_p=pH_{13}\).

The unnormalized root-coordinate Newton objective is consequently
\[
\langle g_{\mathrm{red}},Y\rangle+\frac P2\|Y\|_F^2. \tag{15}
\]
Its Hessian is exactly \(P I_{S^3}\), so its condition number is one.  Equivalently,
the map
\[
\mathcal W_\sigma(Y)=\frac1{\sqrt P}
(R_0YR_0^T,\ldots,R_{P-1}YR_{P-1}^T) \tag{16}
\]
is an isometric nullspace basis and
\[
\mathcal W_\sigma^*I\mathcal W_\sigma=I_{S^3}. \tag{17}
\]
Thus the ambient and orthonormally reduced barrier Hessians both have condition number
exactly one.  The orthonormal reduced coordinate is not the unnormalized root
coordinate: if \(U\) denotes the coordinate used in (16), then
\(U=\sqrt P\,Y\).  Accordingly its Newton solution is
\(-a\sqrt P(H_{12}+pH_{13})\); after normalization it is the same state as the
root-coordinate solution below.

Solving (15) gives the exact free root direction
\[
\Delta Z_p=-a(H_{12}+pH_{13}),
\qquad
a=\frac{K\delta_P}{P}=\frac1{33\sqrt P}. \tag{18}
\]
Every physical block is \(\Delta X_i=R_i\Delta Z_pR_i^T\).  Its Frobenius norm is
\(2a\), independent of the block and of parity.  Also
\[
\|\Delta Z_p\|_{\mathrm{op}}=a\sqrt2<\frac1{100}, \tag{19}
\]
so the full Newton step \(I_3+\Delta X_i\) remains uniformly positive definite.
The complete primal direction has bounded block scale, not an \(N\)-dependent
amplification.

The restriction of (9) to the feasible affine space is a standard
self-concordant function.  Its Newton decrement at the public point is
\[
 \lambda(X^{(0)})=\|\Delta x\|_2=2a\sqrt P
 =\frac2{33}<0.061. \tag{19a}
\]
Thus this instance is inside the universal full-Newton-step neighborhood:
the Dikin-ellipsoid theorem ensures that the full step stays in the domain, and
the standard self-concordant Newton estimate gives
\[
 \lambda(X^{(0)}+\Delta x)
 \le\left(\frac{\lambda(X^{(0)})}{1-\lambda(X^{(0)})}\right)^2
 =\frac4{961}. \tag{19b}
\]
These are representation-independent self-concordant guarantees.  They do not
assert membership in any particular paper's primal-dual centrality neighborhood
or by themselves prove an end-to-end iteration bound.

## 4. Orthogonal free-direction states and the query lower bound

Let \(|12\rangle\) and \(|13\rangle\) denote the second and third standard basis
states in the svec ordering (6).  Normalizing (18) as an amplitude-encoded vector gives
\[
|d_p^{\mathrm{free}}\rangle
=\frac{|12\rangle+p|13\rangle}{\sqrt2}, \tag{20}
\]
up to an irrelevant global phase.  Therefore
\[
\langle d_p^{\mathrm{free}}|O|d_p^{\mathrm{free}}\rangle=p,
\qquad
O=|12\rangle\langle13|+|13\rangle\langle12|. \tag{21}
\]
The fixed observable \(O\) has norm one.  The two ideal direction states are
orthogonal and a fixed measurement recovers parity with certainty.  A state within
trace distance \(1/100\) of the correct state still recovers parity with bounded error.

The same conclusion holds, with no dilution, for the normalized full primal direction.
Every accumulated congruence is \(R_i=D_{\tau_i}\) for a prefix sign
\(\tau_i\in\{-1,+1\}\), and it multiplies both \(H_{12}\) and \(H_{13}\) by the
same \(\tau_i\).  Hence the two nonzero svec coordinates of block \(i\) are
\[
(-\sqrt2a\tau_i,-\sqrt2ap\tau_i). \tag{22}
\]
Let \(O_{\mathrm{all}}\) be the direct sum of the fixed swap (21) on all \(P\)
blocks.  It has norm one, and every block direction is an eigenvector with the same
eigenvalue \(p\).  Therefore
\[
\langle d_p^{\mathrm{full}}|O_{\mathrm{all}}|d_p^{\mathrm{full}}\rangle=p. \tag{23}
\]
The fixed measurement distinguishes the two ideal full-direction states perfectly;
trace error \(1/100\) leaves success probability at least \(99/100\).

The raw coherent oracle returns a requested value of the scalar equality matrix on one
of its two public nonzero positions.  Such a query is simulated, also in superposition,
with at most one standard query to the corresponding input bit \(\sigma_j\); public
edges need no input query.  Hence a \(q\)-query preparation algorithm followed by
(21) or (23) gives a \(q\)-query bounded-error quantum algorithm for parity.  The
bounded-error quantum query complexity of parity is \(\Omega(N)\).  Since \(P=33N\),
we obtain:

> **Theorem 1 (condition-one Newton-state hardness).**  For the SDP family (4), the
> public point (8), and the public KKT right-hand side (11), any quantum algorithm with
> raw coherent sparse-coefficient access that prepares either the normalized free
> primal Newton direction (20) or the normalized full primal direction within trace
> distance \(1/100\) uses \(\Omega(N)=\Omega(P)\) input queries.  This holds although
> the ambient barrier Hessian and its equality-nullspace reduction both have condition
> number exactly one, all constraint incidence degrees are at most two, all nonzero
> constraint magnitudes are one, and all cost eigenvalues lie in
> \([1-\delta_P,1+\delta_P]\).  The public start has Newton decrement \(2/33\);
> its full Newton step remains in the cone, with next decrement at most \(4/961\).

### 4.1 Robust approximate reduced solves

The lower bound does not require an exact reduced solve.  For arbitrary
\(Y\in S^3\), define

\[
 r_{\rm red}(Y)=PY+g_{\rm red}.                         \tag{23a}
\]

Since \(P\Delta Z_p+g_{\rm red}=0\), the relative-residual promise

\[
 {\|r_{\rm red}(Y)\|_F\over\|g_{\rm red}\|_F}\le\eta             \tag{23b}
\]

is exactly equivalent to

\[
 \|Y-\Delta Z_p\|_F\le\eta\|\Delta Z_p\|_F.            \tag{23c}
\]

Assume \(0\le\eta<1\), so \(Y\ne0\), and put

\[
 |y\rangle={\operatorname{svec}(Y)\over\|Y\|_F},
 \qquad
 |v_p\rangle={\operatorname{svec}(\Delta Z_p)\over
                         \|\Delta Z_p\|_F}.             \tag{23d}
\]

The sign omitted in (20) is a global phase, and all statements below are
projective.  Let \(\theta\) be the acute angle between the two rays in (23d).
The distance from the unit vector \(|v_p\rangle\) to the line spanned by
\(Y\) is \(\sin\theta\).  The particular point
\(Y/\|\Delta Z_p\|_F\) on that line is within distance \(\eta\) by (23c),
so

\[
 |\langle v_p|y\rangle|^2=\cos^2\theta\ge1-\eta^2.      \tag{23e}
\]

The operator \(pO\) has \(|v_p\rangle\) as a \(+1\) eigenvector and has
spectrum contained in \([-1,1]\).  There are no cross terms between this
eigenvector and its orthogonal complement.  Therefore

\[
 \boxed{
 p\langle y|O|y\rangle
 \ge 2|\langle v_p|y\rangle|^2-1
 \ge1-2\eta^2.}                                        \tag{23f}
\]

The fixed POVM \((I\pm O)/2\), with its outcome used as the parity guess,
thus succeeds with probability at least \(1-\eta^2\).  Every fixed
\(\eta<1/\sqrt2\) therefore leaves a fixed positive parity advantage.  In
particular, \(\eta\le1/10\) gives signed observable bias at least \(49/50\)
and success probability at least \(99/100\).  If a quantum output state is
itself within trace distance \(\delta\) of \(|y\rangle\langle y|\), the
success probability is at least

\[
                         1-\eta^2-\delta.                \tag{23g}
\]

Thus Theorem 1 remains an \(\Omega(P)\) raw-query lower bound for preparing
the normalized state of any reduced direction satisfying (23b), for example
with \(\eta=1/10\) and \(\delta=1/100\).  The guarantee is adversarial over
all such approximate solutions; it is not a perturbative claim about one
particular solver.  The same robust lower bound holds under the canonical
block-encoding access of Section 4.3: each call to that block encoding is
implemented by one sign query, and the decoder above does not use exactness of
the returned Newton state.

The constant in (23f) is sharp under only (23c).  If \(|w_p\rangle\) is the
\(-1\) eigenvector of \(pO\) in
\(\operatorname{span}\{|12\rangle,|13\rangle\}\), then the vector

\[
 (1-\eta^2)|v_p\rangle
 +\eta\sqrt{1-\eta^2}|w_p\rangle                       \tag{23h}
\]

is at distance exactly \(\eta\) from \(|v_p\rangle\), before its own
normalization, and its normalized \(pO\)-expectation is exactly
\(1-2\eta^2\).

There is also a physical feasible-direction version.  Lift any approximate
root matrix by

\[
 \widetilde{\Delta X}_i=R_iYR_i^T.                     \tag{23i}
\]

This direction satisfies the original homogeneous equalities exactly.  The
relative full-direction error equals the reduced error because every
congruence is orthogonal.  Moreover, the svec sign gauge \(Q_{\tau_i}\)
multiplies both coordinates swapped by \(O\) by the same sign, so

\[
 {\langle\operatorname{svec}(\widetilde{\Delta X}),
       O_{\rm all}\operatorname{svec}(\widetilde{\Delta X})\rangle
  \over\|\widetilde{\Delta X}\|_F^2}
 =\langle y|O|y\rangle.                                \tag{23j}
\]

Hence (23f)--(23g) hold without dilution for the normalized full feasible
direction.  The unit step from the public point also remains strictly inside
the cone.  Indeed,

\[
 \lambda_{\min}(I_3+Y)
 \ge1-\|\Delta Z_p\|_{\rm op}-\|Y-\Delta Z_p\|_F
 \ge1-a\sqrt2-2a\eta.                                  \tag{23k}
\]

For \(a=1/(33\sqrt P)\), \(P\ge33\), and \(\eta\le1/10\), the last
quantity is greater than \(99/100\).  Thus every block
\(I_3+\widetilde{\Delta X}_i=R_i(I_3+Y)R_i^T\) is positive definite with the
same margin.

This robustness is specifically a theorem about the orthonormally reduced
residual (23b), or equivalently direct relative error (23c), followed by the
exact feasible lift (23i).  It must not be inferred from a constant residual
in the unreduced saddle system (11).  Section 5 shows that the inverse norm
of that KKT matrix is \(\Theta(P^2)\), so the generic residual-to-error bound
loses that factor.  Even approximate primal feasibility alone has a
\(\Theta(P)\) loss: a unit right singular vector of \(A_\sigma\) at its
smallest nonzero singular value is distance one from \(\ker A_\sigma\) but
has equality residual \(\Theta(P^{-1})\).  Additional solver-specific
structure would be needed for an unreduced-residual theorem.

The raw-query bound is tight.  The free state can be prepared after computing parity,
and the full product-cone direction has the following direct QRAM-free preparation.

### 4.2 Matching coherent upper bounds

For a node \(i\), define its accumulated edge sign
\[
r_i=\prod_{\substack{1\le j\le N\\K+j-1\le i}}\sigma_j.
\]
Thus \(r_i=1\) on the first \(K\) nodes, is the appropriate prefix parity on
the next \(N\) nodes, and equals \(p\) on the final \(K\) nodes.  Since
\(R_i=D_{r_i}\), equations (12) and (18) give
\[
\Delta X_i=-a r_i(H_{12}+pH_{13}).
\]
Consequently, up to an irrelevant global phase, the normalized full direction is
\[
|d_p^{\mathrm{full}}\rangle
=\frac1{\sqrt{2P}}\sum_{i=0}^{P-1}r_i|i\rangle
  (|12\rangle+p|13\rangle).
\]
This identity also rechecks the equal-block normalization underlying (23): every
block has the same squared norm and therefore weight \(1/P\).

Extend the standard bit oracle by one public dummy input \(z_0=0\), so
\(\sigma_0=+1\).  A query with its target in \(|-\rangle\) is the phase oracle
\(|j\rangle\mapsto\sigma_j|j\rangle\).  Start from the public state
\[
\frac1{\sqrt{2P}}\sum_{i=0}^{P-1}|i\rangle(|12\rangle+|13\rangle).
\]
For each \(j=1,\ldots,N\), let \(b=0\) on coordinate \(|12\rangle\) and
\(b=1\) on coordinate \(|13\rangle\), and reversibly compute
\[
c_j(i,b)=[i\ge K+j-1]\mathbin\oplus b.
\]
Conditioned on \(c_j=1\), put \(j\) in the query-address register; otherwise
put the public dummy address zero there.  Make one phase query and uncompute the
address and predicate.  On the \(|12\rangle\) component the accumulated phase is
\[
\prod_j\sigma_j^{[i\ge K+j-1]}=r_i,
\]
while on the \(|13\rangle\) component it is
\[
\prod_j\sigma_j^{[i\ge K+j-1]\oplus1}=r_ip,
\]
because \(\sigma_j^2=1\).  The resulting state is exactly the normalized full
direction displayed above.

The circuit uses exactly \(N\) sign-oracle calls, no QRAM, and
\(O(N\log P)\) elementary reversible gates: each iteration uses one comparison
against a public threshold and one controlled preparation of an \(O(\log N)\)-bit
query address.  Its workspace is \(O(\log P)\) qubits.  Uniform superposition over
the non-power-of-two public range \(P=33N\) can be synthesized to error
\(\epsilon\) with an additional
\(\operatorname{polylog}(P/\epsilon)\) public-gate cost.  All input-dependent
phases are exact.

Under the fixed-position coefficient oracle of Section 4, this is also one raw
coefficient query per loop iteration: route address \(j\) to either of the two
public coefficient positions carrying \(\sigma_j\), use phase kickback on its
sign bit, and route the dummy address to a public \(+1\) coefficient.  The
constant coefficient magnitude and its public minus-sign convention require no
additional oracle call.

For the free root-direction state (20), omit the node register and use
\(c_j=b\).  The same clean phase circuit uses exactly \(N\) queries and
\(O(N\log N)\) gates with logarithmic workspace.  If clean ancillary registers
are not required, one may instead run the standard exact parity algorithm, which
uses \(\lceil N/2\rceil\) queries, retain its deterministic parity output, and
prepare (20) conditionally.  Thus both the constant-dimensional free-direction
interface and the global product-direction interface have matching
\(\Theta(N)=\Theta(P)\) raw-query complexity.  The lower bounds for the two
interfaces are logically separate: orthogonality of (20) proves the former,
while the all-block swap observable (23), which cancels every prefix phase
\(r_i\), proves the latter without normalization dilution.

Here "free qutrit direction" means the svec amplitude encoding of a direction
in \(S^3\), supported on the two basis coordinates \(|12\rangle,|13\rangle\).
The indefinite Newton matrix itself is not being normalized as a qutrit density
operator.

### 4.3 Canonical KKT block-encoding lower bound

The raw-query reduction extends to a fully specified block encoding of the
unreduced Newton matrix, rather than to an abstract unitary with unspecified
junk blocks.  The short-step scaling \(\delta_P\) changes only the public
right-hand side, not this matrix or its block encoding.  Put

\[
 d=6P,\qquad m=6(P-1),\qquad
 M_\sigma=
 \begin{pmatrix}I_d&A_\sigma^T\\A_\sigma&0_m\end{pmatrix}
 \in\mathbb R^{(12P-6)\times(12P-6)}.
\tag{BE1}
\]

Every row of \(A_\sigma\) has absolute row sum two and every column has
absolute column sum at most two.  Therefore

\[
 \max_r\|(M_\sigma)_{r,*}\|_1
 =\max_c\|(M_\sigma)_{*,c}\|_1=3.
\tag{BE2}
\]

The equality in (BE2) is attained by an internal primal-chain coordinate:
its KKT row contains its identity entry and two incident equality entries.
The support and all magnitudes are public.  A hidden bit \(\sigma_j\) changes
two predecessor coefficients of \(A_\sigma\), on the \(12\) and \(13\)
coordinate chains, and hence the corresponding four symmetric positions of
\(M_\sigma\).

For each potential nonzero matrix position \((r,c)\), introduce a distinct
public entry label \(\lvert e_{rc}\rangle\), and introduce mutually
orthogonal row- and column-failure labels \(\lvert L_r\rangle\) and
\(\lvert R_c\rangle\).  Define

\[
\begin{aligned}
 \lvert\chi_r\rangle
 &=\sum_{c:(r,c)\in\operatorname{supp}M}
   \sqrt{\frac{|M_{rc}|}{3}}\,\lvert e_{rc}\rangle
   +\sqrt{1-\frac{\|(M_\sigma)_{r,*}\|_1}{3}}\,
       \lvert L_r\rangle,\\
 \lvert\phi_c^\sigma\rangle
 &=\sum_{r:(r,c)\in\operatorname{supp}M}
   \operatorname{sgn}(M_{rc}^\sigma)
   \sqrt{\frac{|M_{rc}|}{3}}\,\lvert e_{rc}\rangle
   +\sqrt{1-\frac{\|(M_\sigma)_{*,c}\|_1}{3}}\,
       \lvert R_c\rangle.
\end{aligned}
\tag{BE3}
\]

Distinct row states have disjoint entry and failure labels, so the
\(\lvert\chi_r\rangle\) form an orthonormal family.  The column states are
orthonormal by the same argument.  The shared label at \((r,c)\) gives

\[
 \langle\chi_r\mid\phi_c^\sigma\rangle
 =\frac{(M_\sigma)_{rc}}3.
\tag{BE4}
\]

The unitary completions can be fixed completely and publicly.  For each row,
use a separate seed label \(\lvert0,r\rangle\) and the real Householder
reflection that maps this seed to \(\lvert\chi_r\rangle\); these
constant-size row sectors are mutually orthogonal, so their direct sum, with
the identity on the public complement, defines a unitary \(L\).  Do the same
for the public base column states \(\lvert\phi_c^0\rangle\), in which every
hidden sign is set to \(+1\), to define \(R_0\).  Explicitly,

\[
 L\lvert0,r\rangle=\lvert\chi_r\rangle,
 \qquad
 R_0\lvert0,c\rangle=\lvert\phi_c^0\rangle.
\tag{BE5}
\]

Each state in (BE3) has at most three entry arms and one failure arm, so the
reflections are public constant-dimensional rotations controlled by the row
or column address.  Padded invalid addresses and all unused basis states are
completed by a fixed public bijection.  This specifies the junk action; it is
not an input-dependent existence choice.

On an entry label, reversibly test whether it is one of the four symmetric
KKT positions controlled by an input bit, and compute the corresponding
local index \(j\).  Let \(S_\sigma\) multiply each such label by
\(\sigma_j\) and act as the identity elsewhere.  The fixed public sign of
each coefficient, including the predecessor minus sign, already lies in
\(R_0\).  With the phase-sign oracle and a public dummy index
\(\sigma_0=+1\), \(S_\sigma\), its controlled version, and its adjoint each
use one coherent sign query.  Hence

\[
 R_\sigma=S_\sigma R_0,
 \qquad U_M=L^\dagger R_\sigma
\tag{BE6}
\]

is an exact normalization-three block encoding of the Hermitian KKT matrix:

\[
 \langle0,r\rvert U_M\lvert0,c\rangle
 =\frac{(M_\sigma)_{rc}}3,
 \qquad \alpha_M=3.
\tag{BE7}
\]

Every call to \(U_M\), \(U_M^\dagger\), or a controlled version costs one
hidden-sign query.  The KKT right-hand side \((-g,0)\), its normalized state,
and its norm \(1/\sqrt{132}\), as well as the row and column layouts and the
observables (21) and (23), are public.  The normalized right-hand-side state is
unchanged by the common scaling.
Thus an algorithm may use arbitrary input-independent gates and unlimited
public right-hand-side preparation without weakening the reduction.

> **Theorem 2 (canonical KKT-access hardness).**  If an algorithm supplied
> with the canonical block encoding (BE6)--(BE7) prepares either the free
> primal Newton-direction state (20) or the full primal Newton-direction
> state to trace distance at most \(1/100\), then it makes
> \[
>                         q_{\rm BE}\ge N/2=\Omega(P)
> \tag{BE8}
> \]
> calls to the block encoding, its adjoint, or controlled versions.

Indeed, replace each such call by the one-query implementation above and
apply the exact swap decoder (21) or the all-block swap decoder (23).  The
result is a bounded-error parity algorithm, whose acceptance polynomial has
degree at most twice its query count, whereas parity has approximate degree
\(N\).

The theorem is relative to the displayed canonical completion.  It does not
apply to an arbitrary input-dependent unitary completion supplied for free:
nonprincipal blocks could contain prefix products or parity even while the
encoded principal block remains \(M_\sigma/3\).  Any queries or preprocessing
used to build another completion must be charged to the algorithm.  Also,
normalization three is constant, but the matrix being encoded still has
\(\kappa_2(M_\sigma)=\Theta(P^2)\), as shown next.  The canonical theorem
therefore strengthens the access model of Theorem 1; it does not turn the
unreduced KKT solve into a condition-independent lower-bound instance.

### 4.4 Complete primal-plus-multiplier KKT-state lower bound

There is no loss of parity signal if the requested output is the normalized vector
containing both the primal direction and all equality multipliers in (11).  This
requires a separate calculation because the multiplier norm is much larger than the
primal norm.

Index path edges by \(e=1,\ldots,P-1\), and let \(\tau_i\) be the accumulated
sign at node \(i\), so \(R_i=D_{\tau_i}\), \(\tau_0=1\), and
the signed scalar incidence on each of the svec \(12\) and \(13\) coordinates is
\[
 (B_\sigma z)_e=z_e-(\tau_e\tau_{e-1})z_{e-1}.
\]
For the ordinary oriented path incidence \((Bz)_e=z_e-z_{e-1}\), define
\[
 T=\operatorname{diag}(\tau_0,\ldots,\tau_{P-1}),\qquad
 S=\operatorname{diag}(\tau_1,\ldots,\tau_{P-1}).
\]
Then, in the original fixed node and edge ordering,
\[
 B_\sigma=SBT. \tag{K1}
\]

Put
\[
c=\sqrt2\delta_P=\frac1{8\sqrt{2P}},
\]
the nonzero svec coefficient of \(\delta_PH_{12}\) or
\(\delta_PH_{13}\), and put
\(\alpha=K/P=16/33\).  The two nonzero primal-coordinate solutions of (11) are
\[
 d_{12,i}=-c\alpha\tau_i,\qquad
 d_{13,i}=-c\alpha p\tau_i. \tag{K2}
\]
Thus the short-step rescaling multiplies every component of both
\(\Delta x\) and \(\Delta y\) by the same public factor relative to the
unscaled construction.  It leaves the normalized complete KKT state and all
ratios below unchanged.
Define the public positive tent on the edges
\[
 v_e=
 \begin{cases}
 c(1-\alpha)e,&1\le e\le K,\\
 c\alpha(P-e),&K<e<P.
 \end{cases} \tag{K3}
\]
The equality multipliers in the original, ungauged row coordinates are exactly
\[
 y_{12,e}=\tau_ev_e,\qquad
 y_{13,e}=-p\tau_ev_{P-e}. \tag{K4}
\]
Here the subscripts \(12,13\) refer to the two scalar constraint rows on the
same edge in the public svec ordering.

To verify (K4), set \(\widetilde y=Sy\).  Equation (K1) turns
\(B_\sigma^Ty=-g-d\) into
\[
 B^T\widetilde y=c(\alpha{\bf1}-{\bf1}_{\rm pre})
\]
in the \(12\) channel.  The unique solution is (K3), since
\((B^Tv)_0=-v_1\), \((B^Tv)_i=v_i-v_{i+1}\), and
\((B^Tv)_{P-1}=v_{P-1}\).  In the \(13\) channel the right-hand side is
\(p\) times its node reversal.  If \(J\) reverses path edges, then
\(B^T(-Jv)\) is the node reversal of \(B^Tv\), proving (K4).
Multiplication by \(S\) converts back to the actual multiplier coordinates and
produces the same factor \(\tau_e\) in both channels.

Normalize the complete solution vector in the precise displayed KKT ordering:
\[
 |k_p\rangle=
 \frac{(\Delta x,\Delta y)}
 {\sqrt{\|\Delta x\|_2^2+\|\Delta y\|_2^2}},
\]
where \(\Delta x\) is block-major in the svec order (6), and \(\Delta y\) is
edge-major with the same six-coordinate order.  Let \(O_{\rm KKT}\) swap the
\(12\) and \(13\) coordinates within every primal block and also within the
six multipliers belonging to every edge, acting as zero on other coordinates.
This is a fixed public norm-one observable: it uses neither the sign gauges
\(S,T\), prefix products, nor parity.

Set
\[
 D=\sum_i d_{12,i}^2=Pc^2\alpha^2,\qquad
 V=\sum_e v_e^2,\qquad
 C=\sum_e v_ev_{P-e}. \tag{K5}
\]
Equations (K2) and (K4) give equal norms in the two channels and
\[
 \langle k_p|O_{\rm KKT}|k_p\rangle
 =p\,\frac{D-C}{D+V}. \tag{K6}
\]
This expectation has a uniform constant magnitude.  On the \(8N\) edges
\(8N\le e<16N\), \(v_e\ge136cN/33\), while (K3) gives
\(\max_e|v_e-v_{P-e}|\le16cN/33\).  Therefore, with
\(\beta=33/578\),
\[
\frac DV\le\frac{33}{578N^2}\le\beta,\qquad
\frac{\|v-Jv\|_2^2}{V}\le\beta,\qquad
\frac CV=1-\frac{\|v-Jv\|_2^2}{2V}\ge1-\frac\beta2. \tag{K7}
\]
It follows for every \(N\ge1\) that
\[
\left|\langle k_p|O_{\rm KKT}|k_p\rangle\right|
\ge\frac{1-3\beta/2}{1+\beta}
 =\frac{1057}{1222}>\frac67, \tag{K8}
\]
and its sign is \(-p\).  Measuring \(O_{\rm KKT}\) recovers parity with
success probability greater than \(13/14\).  Trace distance \(1/100\) from
the ideal state reduces this probability by at most \(1/100\).

> **Theorem 3 (complete KKT-state hardness).**  In the same raw coherent
> sparse-coefficient model, preparing the normalized complete KKT solution state
> \(|k_p\rangle\) of (11), including both the primal direction and the equality
> multiplier in the displayed sign convention and ordering, to trace distance
> \(1/100\) requires \(\Omega(N)=\Omega(P)\) input queries.

The theorem uses only same-edge pairings in the original row ordering.  The sign
gauge in its proof is an algebraic device and is not supplied to the decoder.  It
also applies verbatim to the canonical block encoding (BE6): substituting its
one-query implementation would otherwise give a bounded-error parity algorithm.

### 4.5 Nullspace-projector synthesis is parity-hard at short-step scale

The access obstruction can be isolated even more directly in the orthogonal
projector onto the feasible tangent.  For reference, the public scale already
used in (3) is

\[
 \delta_s:=\delta_P={1\over16\sqrt P}.
\tag{PB1}
\]

Thus the first \(K\) costs are \(I_3+\delta_sH_{12}\), the final \(K\)
costs are \(I_3+\delta_sH_{13}\), and the middle costs remain \(I_3\).
At \(X_i=I_3\) and \(\mu=1\), the ambient and equality-reduced Hessians are
still identity and the public gradient is

\[
 g_i^{(s)}=
 \begin{cases}
  \delta_sH_{12},&0\le i<K,\\
  0,&K\le i<K+N,\\
  \delta_sH_{13},&K+N\le i<P.
 \end{cases}
\tag{PB2}
\]

Let \(\Pi_\sigma\) be the Euclidean orthogonal projector in the full
\(6P\)-dimensional svec space onto \(\ker A_\sigma\).  The constrained
Newton direction is exactly

\[
                       \Delta x^{(s)}=-\Pi_\sigma g^{(s)}.
\tag{PB3}
\]

The norm calculation is exact.  Since \(\|H_{12}\|_F^2=
\|H_{13}\|_F^2=2\), \(K/P=16/33\), and there are \(K\) blocks of each
type,

\[
 \|g^{(s)}\|_2^2=4K\delta_s^2={1\over132}.
\tag{PB4}
\]

Eliminating the equalities as in Section 3 gives the root direction

\[
 \Delta Z_p^{(s)}
 =-{K\delta_s\over P}(H_{12}+pH_{13})
 =-{1\over33\sqrt P}(H_{12}+pH_{13}).
\tag{PB5}
\]

Every lifted block has the same Frobenius norm, so

\[
 \|\Pi_\sigma g^{(s)}\|_2^2
 =\|\Delta x^{(s)}\|_2^2={4\over1089}
 =\left({2\over33}\right)^2.
\tag{PB6}
\]

In particular, the Newton decrement is the absolute constant \(2/33\), so
the instance is at universal short-step scale as quantified in
(19a)--(19b).  If
\(\lvert\widehat g\rangle=g^{(s)}/\|g^{(s)}\|_2\), then

\[
 \|\Pi_\sigma\lvert\widehat g\rangle\|_2^2
 ={(4/1089)\over(1/132)}={16\over33}.
\tag{PB7}
\]

The public state \(\lvert\widehat g\rangle\) is a uniform signed-free
superposition over two public block ranges and can be prepared without an
input query.  Conditional on the projector signal sector, its state is the
normalized global direction in (23), up to a global minus sign.  Hence the
all-block swap \(O_{\rm all}\) has deterministic conditional eigenvalue
\(p\).

No postselection is needed for a robust synthesis lower bound.  Suppose a
raw-query circuit implements a normalization-one block encoding \(U_\sigma\)
with signal projector \(\Pi_{\mathrm{sig}}\) and principal block

\[
 B_\sigma
 =\Pi_{\rm sig}U_\sigma\Pi_{\rm sig}
   \big|_{\operatorname{ran}\Pi_{\rm sig}},
 \qquad
 \|B_\sigma-\Pi_\sigma\|\le\varepsilon.
\tag{PB8}
\]

Apply it once to the public signal input \(\lvert\widehat g\rangle\), and
measure \(O_{\rm all}\) on the output signal sector and zero on the junk
sector.  Put \(v_p=\Pi_\sigma\lvert\widehat g\rangle\) and
\(e_p=(B_\sigma-\Pi_\sigma)\lvert\widehat g\rangle\).  Then
\(pO_{\rm all}v_p=v_p\), \(\|v_p\|=4/\sqrt{33}\), and
\(\|e_p\|\le\varepsilon\).  Therefore

\[
\begin{aligned}
 p\,\langle O_{\rm all}\rangle
 &\ge {16\over33}-{8\over\sqrt{33}}\varepsilon-\varepsilon^2\\
 &\ge \gamma_\Pi,
 \qquad
 \gamma_\Pi:={16\over33}-{1\over2\sqrt{33}}-{1\over256}
 >0.393,
 \qquad \varepsilon\le{1\over16}.
\end{aligned}
\tag{PB9}
\]

Assign a fair random output on the zero eigenspace of the extended
observable.  Equation (PB9) then computes parity with success probability
greater than \(1/2+0.393/2>2/3\) after a single projector-encoding call.

> **Theorem 4 (nullspace-projector oracle-synthesis hardness).**  Any uniform
> raw-coefficient-query circuit which, for every input \(\sigma\), implements
> a normalization-one block encoding (PB8) of the orthogonal projector onto
> \(\ker A_\sigma\) with operator error \(\varepsilon\le1/16\) uses at least
> \(N/2=\Omega(P)\) coefficient queries.

The proof substitutes the circuit into the one-call decoder above and uses
the degree-\(N\) parity lower bound.  If an input-dependent setup uses
\(q_{\rm setup}\) queries and the first usable call uses
\(q_{\rm call}\) more, the precise conclusion is

\[
                         q_{\rm setup}+q_{\rm call}\ge N/2.
\tag{PB10}
\]

After paying that setup cost, later marginal calls may be cheap.  The theorem
allows any unitary completion actually synthesized by the counted circuit,
because the decoder reads only its principal block.  It is not a
block-encoding-call lower bound relative to a projector oracle supplied for
free: one such call already reveals parity with constant bias.  Nor does it
apply if prefix gauges, parity, or an input-dependent completion are given as
uncharged advice.  The result instead isolates the cost of constructing the
input-dependent nullspace projection that turns the ambient identity Hessian
into the condition-one reduced system.

#### Matching exact QRAM-free synthesis

The lower bound is tight up to an absolute factor, including on all six svec
coordinates.  Define the accumulated sign at node \(i\) by

\[
 r_i=\prod_{\substack{1\le j\le N\\K+j-1\le i}}\sigma_j,
\qquad
 \chi_\ell=
 \begin{cases}
  1,&\ell\in\{12,13\},\\
  0,&\ell\in\{11,22,23,33\}.
 \end{cases}
\tag{PU1}
\]

In the svec ordering (6), congruence by \(R_i=D_{r_i}\) is
\(\operatorname{diag}(1,r_i,r_i,1,1,1)\).  Hence the diagonal phase

\[
 F_\sigma|i,\ell\rangle=r_i^{\chi_\ell}|i,\ell\rangle
\tag{PU2}
\]

contains the complete input dependence of the nullspace isometry.  If
\(|u_P\rangle=P^{-1/2}\sum_{i=0}^{P-1}|i\rangle\), then

\[
 \mathcal W_\sigma|\ell\rangle
 =F_\sigma(|u_P\rangle|\ell\rangle).
\tag{PU3}
\]

Thus the \(11,22,23,33\) columns are the unsigned uniform node state in
their respective, mutually orthogonal coordinate sectors, while the \(12,13\)
columns are both the signed-prefix state
\(P^{-1/2}\sum_i r_i|i\rangle\).  In particular,

\[
 \langle i,\ell|\Pi_\sigma|i',\ell'\rangle
 =\frac{\delta_{\ell\ell'}}P
   (r_ir_{i'})^{\chi_\ell}.
\tag{PU4}
\]

This verifies explicitly that no phase is missing on the \(23\) coordinate:
both of its indices are fixed by \(D_{r_i}=\operatorname{diag}(r_i,1,1)\).

The phase (PU2) needs exactly \(N\) raw coefficient queries and no prefix
table.  For hidden edge \(j\), reversibly compute
\([i\ge K+j-1]\wedge\chi_\ell\).  Route the query address to a fixed public
coefficient position carrying \(\sigma_j\) when this predicate is one, and to
a public dummy \(+1\) coefficient otherwise.  One sign-bit phase-kickback query
then contributes the required factor \(\sigma_j\); uncompute the public routing
logic.  Repeating over \(j=1,\ldots,N\) gives (PU2).  A public minus sign in the
chosen equality coefficient is removed by a public phase.

Let \(U_0|0\rangle=|u_P\rangle\) be any public unitary completion and set

\[
 U_{W,\sigma}=F_\sigma(U_0\otimes I_6).
\]

Then \(U_{W,\sigma}|0,\ell\rangle=\mathcal W_\sigma|\ell\rangle\), and both
\(U_{W,\sigma}\) and its inverse use \(N\) coefficient queries,
\(O(N\log P)\) elementary gates, and \(O(\log P)\) work qubits.  To obtain a
normalization-one projector block encoding, add one signal qubit and use the
public reversible predicate

\[
 C_{\ne0}|a,i,\ell\rangle
 =|a\mathbin\oplus[i\ne0],i,\ell\rangle.
\]

The unitary

\[
 U_{\Pi,\sigma}
 =(I\otimes U_{W,\sigma})C_{\ne0}
  (I\otimes U_{W,\sigma}^\dagger)
\tag{PU5}
\]

satisfies

\[
 (\langle0|\otimes I)U_{\Pi,\sigma}(|0\rangle\otimes I)
 =U_{W,\sigma}(|0\rangle\!\langle0|\otimes I_6)
  U_{W,\sigma}^\dagger
 =\mathcal W_\sigma\mathcal W_\sigma^*=\Pi_\sigma.
\]

It is therefore an exact normalization-one block encoding in the
arbitrary-rotation model.  A call uses exactly \(2N\) raw coefficient queries,
\(O(N\log P)\) gates, and logarithmic workspace.  The exact reflection
\(2\Pi_\sigma-I\) is
\(U_{W,\sigma}(2|0\rangle\!\langle0|\otimes I_6-I)U_{W,\sigma}^\dagger\)
and has the same cost, without the signal qubit.  With a discrete
fault-tolerant gate set, synthesize the public range-uniform unitary \(U_0\) to
operator error \(O(\eta)\); this gives projector block error \(O(\eta)\) with
an additional \(\operatorname{polylog}(P/\eta)\) public-gate cost.  All
input-dependent phases remain exact.

This construction has \(q_{\rm setup}=0\) and \(q_{\rm call}=2N\), matching
(PB10) within a factor four.  Alternatively, querying and caching every prefix
has \(q_{\rm setup}=N\) and can make later raw-query cost zero, at the price of
building \(\Theta(P)\) input-dependent classical/QRAM data.  Thus the lower and
upper bounds agree on the setup-versus-first-call boundary as well as on the
linear exponent.

## 5. Reduced Hessian conditioning is not saddle KKT conditioning

Theorem 1 must not be paraphrased as saying that the unreduced matrix in (11) has
condition number one.  A diagonal sign gauge transforms each of the six coordinate
copies of \(A_\sigma\) into the ordinary incidence matrix of a path on \(P\) nodes.
Its nonzero singular values are
\[
s_j=2\sin\frac{j\pi}{2P},\qquad 1\le j<P. \tag{24}
\]
In particular, \(s_{\min}=\Theta(P^{-1})\) and \(s_{\max}=\Theta(1)\).

For a singular value \(s\) of \(A_\sigma\), the corresponding two eigenvalues of the
saddle matrix in (11) solve
\[
\lambda^2-\lambda-s^2=0,
\qquad
\lambda_\pm(s)=\frac{1\pm\sqrt{1+4s^2}}2. \tag{25}
\]
The primal nullspace also contributes eigenvalue one.  At the smallest \(s\),
\(|\lambda_-(s)|=\Theta(s^2)=\Theta(P^{-2})\), while the largest eigenvalue is
\(\Theta(1)\).  Consequently the ordinary spectral condition number of the unreduced
saddle KKT matrix is \(\Theta(P^2)\).

This distinction is useful in both directions:

* an algorithm that directly block-encodes (11) must charge its saddle conditioning;
* an algorithm claiming to exploit the condition-one reduced system must still build
  or apply an input-dependent nullspace representation such as (16).

Theorem 1 proves that the second route does not make the raw access cost disappear.
Applying the reduced representation, or producing its solution state, composes the
hidden signs along the chain and is parity-hard.

Theorem 4 strengthens this point at constant Newton decrement: synthesizing
the orthogonal nullspace projector even to constant operator error costs
\(\Omega(P)\) raw queries.  Its normalization is one and its signal
probability on the normalized public gradient is exactly \(16/33\), so
neither a poor block-encoding normalization nor postselection causes the
lower bound.

Theorem 3 shows separately that the large multiplier norm does not erase the parity
signal for this family.  It does not improve the conditioning of the unreduced
matrix: its state lower bound and the condition-one claim for the reduced primal
Hessian are distinct statements.

## 6. Relation to the unscaled central-state construction

The present short-step-scaled SDP has reduced effective cost
\[
\overline C_p=I_3+\frac1{33\sqrt P}H_{12}
 +p\frac1{33\sqrt P}H_{13}. \tag{26}
\]
Its central point and central Hessian retain parity dependence, but only at
\(O(P^{-1/2})\) scale; this note makes no constant-trace-separation claim for
those central states.  The companion
`2026-09-02-free-s3-parity-central-hessian.md` instead uses the same incidence
geometry with the unscaled anisotropy \(1/2\), obtaining constant central-state
separation but a growing Newton decrement at the public point.  Scaling does not
change any normalized Newton solution state because the whole KKT right-hand side
and solution scale together.  The present variant therefore trades central-state
separation for a universal short-step guarantee while preserving direction-state
hardness.

The result does not claim that every representation of the answer is hard.  An oracle
that directly supplies parity or all prefix products has performed the hard aggregation
in advance.  Building such a data structure from the raw coefficients costs
\(\Theta(N)\) classical input work on this family.

## 7. Literature and novelty status

The local-to-global sign product is a standard gauge/synchronization phenomenon, not a
new SDP primitive.  See T. Gao, J. Brodzki, and S. Mukherjee,
[*The Geometry of Synchronization Problems and Learning Group Actions*](https://arxiv.org/abs/1610.09051).
Classical SDP symmetry and invariant-subspace reductions are treated by F. Vallentin,
[*Symmetry in semidefinite programs*](https://arxiv.org/abs/0706.4233), and
F. Permenter and P. A. Parrilo,
[*Dimension reduction for semidefinite programs via Jordan algebras*](https://arxiv.org/abs/1608.02090).
The parity query lower bound itself follows from R. Beals et al.,
[*Quantum lower bounds by polynomials*](https://arxiv.org/abs/quant-ph/9802049).
The non-SOCP statement is due to H. Fawzi,
[*On representing the positive semidefinite cone using the second-order cone*](https://arxiv.org/abs/1610.04901).

The closest QIPM comparison is B. Augustino, G. Nannicini, T. Terlaky, and
L. F. Zuluaga,
[*Quantum Interior Point Methods for Semidefinite Optimization*](https://arxiv.org/abs/2112.06025),
whose feasible variant uses a nullspace representation of the Newton system.  Theorem 1
isolates a cost not measured by the condition number of an already formed reduced
Hessian: constructing or applying the input-dependent isometry (16), and hence the
reduced right-hand side (14), composes the hidden signs.

Generic quantum-linear-system lower bounds do not subsume Theorem 1.  D. Orsucci and
V. Dunjko,
[*On solving classes of positive-definite quantum linear systems with quadratically
improved runtime in the condition number*](https://arxiv.org/abs/2101.11868),
Q. Wang and Z. Zhang,
[*Tight Quantum Depth Lower Bound for Solving Systems of Linear Equations*](https://arxiv.org/abs/2407.06012),
and H. Mori et al.,
[*Sparsity-dependent Complexity Lower Bound of Quantum Linear System Solvers*](https://arxiv.org/abs/2601.16697),
prove worst-case QLS lower bounds for a supplied square-system oracle and a designated
inverse-solution state.  Their condition-number statements are existential worst-case
results, not per-instance lower bounds that follow merely because a displayed matrix
has large \(\kappa\).  In the present construction the unreduced saddle matrix (11)
does have \(\kappa=\Theta(P^2)\), but Theorems 1 and 3 give direct
raw-coefficient parity reductions for, respectively, its primal direction sector
and its normalized complete primal-plus-multiplier solution.

Conversely, the theorem should not be called a condition-one QLS lower bound.  The
identity operator in (17) is obtained only after using the input-dependent nullspace
basis \(\mathcal W_\sigma\).  If a conventional QLS interface supplied the reduced RHS
state \(|g_{\rm red}\rangle\), then solving the identity system would be trivial; that
state already contains the parity which raw access must aggregate.  This distinction is
also visible in G. H. Low and Y. Su,
[*Quantum linear system algorithm with optimal queries to initial state preparation*](https://arxiv.org/abs/2410.18178),
which explicitly separates access to a block encoding of the matrix from preparation
of the RHS state.  General state conversion (T. Lee et al.,
[*Quantum query complexity of state conversion*](https://arxiv.org/abs/1011.3020))
provides an abstract umbrella for input-dependent state generation, but not this sparse
SDP/KKT instantiation.

Generic quantum SDP lower bounds also use a different contract.  The lower bounds of
J. van Apeldoorn et al.,
[*Quantum SDP-solvers: Better upper and lower bounds*](https://arxiv.org/abs/1705.01843),
concern approximate optimization/value interfaces; this homogeneous family has the
same optimum, zero, for both parities.  They therefore do not imply direction-state
hardness here, and Theorem 1 does not strengthen them uniformly.  Theorem 8.4 of
S. Apers and S. Gribling,
[*Quantum speedups for linear programming via interior point methods*](https://arxiv.org/abs/2311.03215v3),
also proves an \(\Omega(\sqrt{ndr})\) row-query lower bound for additive LP
optimal-value estimation.  Thus a linear query exponent for a balanced sparse
optimization instance is not itself new; its output contract is again different from
the Newton-direction state required here.

A targeted primary-source search through September 2, 2026 found no prior theorem
combining a public feasible start, public original Newton RHS, identity ambient
Hessian, exactly condition-one but input-dependent free \(S_+^3\) reduction,
bounded-degree raw coefficient and canonical KKT block-encoding access, and
\(\Omega(P)\) preparation cost for the free primal, full primal, or complete
primal-plus-multiplier Newton state, with the primal result robust even for an
adversarial constant-relative-residual reduced solve and based at decrement \(2/33\).
The normalization-one nullspace-projector synthesis lower bound at the same
constant decrement makes the reduction-access separation explicit.  The
defensible novelty is this conjunction, not the parity exponent, gauge chain,
nullspace elimination, or an \(\Omega(\kappa)\) QLS bound.  The search does
not prove bibliographic priority.
