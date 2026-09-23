# Winner-take-all holonomy SDP with one global trace budget

Date: 2026-09-02

## Main theorem

Coupling \(G\) intrinsic triangle-holonomy gadgets by one global trace budget
turns their spectra into a minimum.  One odd hidden parity among the \(G\)
paths changes the exact SDP optimum by the constant \(1/10\).  The resulting
value problem has tight raw-query complexities

\[
 Q=\Theta(N\sqrt G),\qquad R=\Theta(NG),                     \tag{1}
\]

where each path contains \(N\) private signs.  There are
\(L=33GN\) constant-size PSD blocks, so

\[
 Q=\Theta(\sqrt{NL}),\qquad R=\Theta(L)                      \tag{2}
\]

up to the fixed factor 33.

The global trace is implemented by a public chain of free scalar
accumulators.  Every scalar constraint row has at most five nonzeros and
every scalar column has at most two.  At the public feasible start
\(X_{g,i}=I/(3G)\), \(t_g=g/G\), and barrier parameter \(\mu=1/(GP)\), the
PSD-root reduced Hessian, after eliminating the public accumulators and copy
rows, is exactly the scalar \(9G I\) on all \(6G-1\) feasible root
directions.  The Newton decrement is \(1/\sqrt{150}\), and the undamped step
has minimum PSD-block eigenvalue \(14/(45G)\).

> **Theorem (winner-take-all OR-of-parities SDP).**  For every \(G,N\ge1\),
> there is a strictly primal and dual feasible product SDP with \(33GN\)
> blocks in \(\mathbb S_+^3\), \(O(G)\) free public bookkeeping scalars,
> bounded public costs, scalar row sparsity at most five, and scalar column
> sparsity at most two.  Its optimum is \(29/10\) if all \(G\) path parities
> are even and \(14/5\) if at least one is odd.  For every
> \(\epsilon<1/20\), additive-\(\epsilon\) value estimation has bounded-error
> quantum query complexity \(\Theta(N\sqrt G)\); relative-\(1/100\)
> estimation has the same bound.  Randomized classical query complexity is
> \(\Theta(NG)\).  At the public point above, the PSD-root primal
> log-barrier Hessian has condition number one, all unreduced right-hand
> sides are public, and the full primal Newton step is strictly feasible.
> The feasible spectrahedron has no lift over a finite product of
> second-order cones.

The optimizer statement is robust.  Exact feasibility and objective error
\(\delta\) force trace mass at least \(1-10\delta\) onto odd winning groups.
For the original sparse rows, equality residual
\(O((GP)^{-1/2})\) and constant objective error still force a
trace-normalized PSD output to identify a winning group with constant
probability and to reveal whether any winner exists.  A neighboring-instance
mixture proves that the \((GP)^{-1/2}\) residual order is necessary.

## 1. Signed paths and the sparse global trace budget

Let

\[
 K=16N,\qquad P=2K+N=33N.                                  \tag{3}
\]

For each group \(g\in[G]\), take a path of \(P\) blocks
\(X_{g,0},\ldots,X_{g,P-1}\in\mathbb S_+^3\).  Its private input is

\[
 \sigma_{g,1},\ldots,\sigma_{g,N}\in\{-1,+1\},\qquad
 h_g=\prod_{j=1}^N\sigma_{g,j}.                              \tag{4}
\]

Consecutive blocks obey

\[
 X_{g,i}=G_{g,i}X_{g,i-1}G_{g,i}^T.                         \tag{5}
\]

The first \(K-1\) edges and final \(K\) edges are identity congruences.  The
intervening \(N\) edges, in input order, use

\[
 D_{\sigma_{g,j}}=\operatorname{Diag}(\sigma_{g,j},1,1).    \tag{6}
\]

Let \(R_{g,0}=I\) and let \(R_{g,i}\) be the accumulated congruence.  Then
(5) is equivalent to

\[
                         X_{g,i}=R_{g,i}Z_gR_{g,i}^T,
                         \qquad Z_g\succeq0.                 \tag{7}
\]

The first \(K\) blocks have \(R_{g,i}=I\), and the final \(K\) blocks have
\(R_{g,i}=D_{h_g}\).

Introduce free public scalars \(t_1,\ldots,t_G\) and impose

\[
 \begin{aligned}
 t_1-\operatorname{tr}X_{1,0}&=0,\\
 t_g-t_{g-1}-\operatorname{tr}X_{g,0}&=0 &&(2\le g\le G),\\
 t_G&=1.
 \end{aligned}                                                \tag{8}
\]

For \(G=1\), the first and last equations simply impose
\(t_1=\operatorname{tr}X_{1,0}=1\).  Eliminating the \(t_g\)'s turns (8)
into the one global trace budget

\[
                         \sum_{g=1}^G\operatorname{tr}Z_g=1. \tag{9}
\]

Thus the eliminated PSD-root feasible set is

\[
 \mathcal B_G=\left\{(Z_1,\ldots,Z_G):
 Z_g\succeq0,\ \sum_g\operatorname{tr}Z_g=1\right\}.        \tag{10}
\]

It has a strict PSD point \(Z_g=I/(3G)\), with public accumulators
\(t_g=g/G\).

In isometric-svec form, every copy row has two nonzeros.  The first row in
(8) has four, an interior accumulator row has five, and the anchor has one.
Every root diagonal column occurs in its first copy row and one accumulator
row.  Every free \(t_g\) column occurs in at most two rows.  Hence

\[
                         d_{\rm row}\le5,\qquad d_{\rm col}\le2.           \tag{11}
\]

Only the \(12\) and \(13\) copy coefficients on each signed edge depend on
the input.

## 2. Public anisotropy triangles

Put

\[
 H_{ab}=e_ae_b^T+e_be_a^T,\qquad
 u=\frac1{10},\qquad q=\frac KP=\frac{16}{33},\qquad
 \gamma=\frac uq=\frac{33}{160}.                            \tag{12}
\]

Within every group, use the public local costs

\[
 C_{g,i}=\begin{cases}
 3I+uH_{23}+\gamma H_{12},&0\le i<K,\\
 3I+uH_{23},&K\le i<K+N,\\
 3I+uH_{23}+\gamma H_{13},&K+N\le i<P.
 \end{cases}                                                 \tag{13}
\]

Every local cost has spectrum in \((11/4,13/4)\), because
\(\sqrt{u^2+\gamma^2}<1/4\).  The free scalars have zero objective
coefficient.  The SDP objective is

\[
                         \frac1P\sum_{g=1}^G\sum_{i=0}^{P-1}
                         \langle C_{g,i},X_{g,i}\rangle.     \tag{14}
\]

Pulling each group to its root gives

\[
 \frac1P\sum_iR_{g,i}^TC_{g,i}R_{g,i}
 =3I+u(H_{12}+H_{23}+h_gH_{13})=:\overline C_{h_g}.           \tag{15}
\]

Its spectra are

\[
 \operatorname{spec}(\overline C_+)=\{16/5,29/10,29/10\},
 \qquad
 \operatorname{spec}(\overline C_-)=\{31/10,31/10,14/5\}.   \tag{16}
\]

The SDP is strictly dual feasible.  In the formulation with free \(t_g\)'s,
take every equality multiplier zero; stationarity in each free scalar is
then zero, and the PSD slack blocks \(C_{g,i}/P\) are positive definite.
The point following (10) proves strict primal feasibility in the conic
variables.

## 3. Winner-take-all optimum

After eliminating paths and accumulators, the SDP is

\[
 \begin{aligned}
 \text{minimize}\quad&\sum_{g=1}^G
                   \langle\overline C_{h_g},Z_g\rangle,\\
 \text{subject to}\quad&Z_g\succeq0,\qquad
                   \sum_g\operatorname{tr}Z_g=1.
 \end{aligned}                                                \tag{17}
\]

Let \(v_h=\lambda_{\min}(\overline C_h)\).  Every feasible tuple obeys

\[
 \sum_g\langle\overline C_{h_g},Z_g\rangle
 \ge\sum_gv_{h_g}\operatorname{tr}Z_g
 \ge\min_gv_{h_g}.                                           \tag{18}
\]

Equality is attained by putting all trace mass on a minimum eigenvector in a
group attaining \(\min_gv_{h_g}\), with the other root blocks zero.  Hence

\[
 \boxed{\operatorname{OPT}=\min_gv_{h_g}
 =\begin{cases}
 29/10,&h_g=+1\text{ for every }g,\\
 14/5,&h_g=-1\text{ for at least one }g.
 \end{cases}}                                                 \tag{19}
\]

If \(b_g=(1-h_g)/2\) records whether group \(g\) has odd raw parity, the
optimum encodes \(\operatorname{OR}(b_1,\ldots,b_G)\) with gap \(1/10\).
The dual of (17) gives the same formula: its trace multiplier \(s\) is
maximized subject to \(\overline C_{h_g}-sI\succeq0\) for every group.

## 4. Tight raw-query complexity

The supports, accumulator rows, right-hand sides, and costs are public.  A
fixed-position row or column value query is simulated coherently using at
most one query to the corresponding input sign; this includes superposition
queries.

The query normalization can be made exact.  Use the canonical isometric-svec
value oracle that XORs the requested coefficient's sign bit into a target.
Every hidden slot is one of the two coefficients
\(\pm\sigma_{g,j}\) in the \(12\) and \(13\) copy rows of edge \((g,j)\).
Public reversible address arithmetic maps a queried row or column slot to
\((g,j)\), or to a dummy address containing zero.  One raw bit-oracle call
then acts directly on the coefficient sign target; it works coherently in
superposition and needs no second call to uncompute a stored answer.  The
inverse and externally controlled calls cost one query as well.  Conversely,
one fixed hidden copy slot exposes \(\sigma_{g,j}\), so one coefficient query
implements one raw sign query.  Hence canonical coefficient and raw-sign
queries have exactly unit query normalization on the hidden input.  A
clean-output arithmetic-value convention can instead cost a factor two by
compute--phase--uncompute, which changes no asymptotic statement.

Any additive-\(\epsilon\) estimate of (19) with \(\epsilon<1/20\),
thresholded at \(57/20\), computes

\[
                         \operatorname{OR}_G\circ
                         \operatorname{PARITY}_N.             \tag{20}
\]

The same threshold works for relative error \(1/100\), because
\[
 {101\over100}{14\over5}<{57\over20}
 <{99\over100}{29\over10}.                                 \tag{20a}
\]

Here is a direct adversary proof, already on the promise of zero or one odd
group.  Let \(E,O\subseteq\{0,1\}^N\) be the even- and odd-parity strings,
and define the \(|E|\times|O|\) matrix
\[
 B_{xy}=\mathbf1[|x-y|_1=1].                                \tag{Q1}
\]
Every row and column of this even-to-odd hypercube incidence matrix has sum
\(N\), and the uniform vectors attain that singular value.  If
\(\Delta_j(x,y)=\mathbf1[x_j\ne y_j]\), then
\(B\circ\Delta_j\) is the permutation matrix
\(x\mapsto x\oplus e_j\).  Therefore
\[
                         \|B\|=N,
 \qquad                  \|B\circ\Delta_j\|=1.              \tag{Q2}
\]

Restrict the input to
\[
 \mathcal D_0=E^G,
 \qquad
 \mathcal D_1=\bigsqcup_{a=1}^G
        E^{a-1}\times O\times E^{G-a}.                       \tag{Q3}
\]
For the sector whose odd block is \(a\), put
\[
 C_a=I_E^{\otimes(a-1)}\otimes B\otimes I_E^{\otimes(G-a)},
 \quad C=[C_1\ C_2\ \cdots\ C_G],
 \quad \Gamma=\begin{pmatrix}0&C\\C^T&0\end{pmatrix}.      \tag{Q4}
\]
The odd sectors are disjoint, so
\[
 CC^T=\sum_{a=1}^G I_E^{\otimes(a-1)}\otimes BB^T\otimes
                       I_E^{\otimes(G-a)}.                  \tag{Q5}
\]
The summands commute, have norm \(N^2\), and share the uniform tensor
eigenvector with eigenvalue \(N^2\) for every summand.  Hence
\[
                              \|\Gamma\|=N\sqrt G.           \tag{Q6}
\]
Filtering by raw query \((a,j)\) annihilates every odd sector other than
\(a\), because its block-\(a\) factor is an identity.  In sector \(a\), the
filter replaces \(B\) by the perfect matching \(B\circ\Delta_j\).  Thus
\[
                     \|\Gamma\circ\Delta_{a,j}\|=1          \tag{Q7}
\]
for every raw position.  The positive-weight adversary ratio is exactly
\(N\sqrt G\), and the standard adversary theorem proves
\[
 Q_{1/3}(\mathcal D_0\text{ versus }\mathcal D_1)
                              =\Omega(N\sqrt G).             \tag{21}
\]
This witness gives the same result as perfect adversary composition, which
is established prior art rather than a new query-lower-bound technique.

The SDP value is \(29/10\) on \(\mathcal D_0\) and \(14/5\) on
\(\mathcal D_1\).  For every \(\epsilon<1/20\), their allowed output
intervals are disjoint, and thresholding at \(57/20\) transfers (21) to
value estimation without another query.  Exact unit access normalization
above introduces no hidden oracle factor.

The matching upper bound is explicit and QRAM-free.  With
\(\sigma_{g,j}=(-1)^{z_{g,j}}\), put a raw bit-oracle answer register in
\(|-\rangle\) and, for fixed component address \(|g\rangle\), query the
\(N\) public edge indices in order.  Phase kickback implements the clean
marker

\[
 |g\rangle\longmapsto
 \prod_{j=1}^N(-1)^{z_{g,j}}|g\rangle=h_g|g\rangle           \tag{21a}
\]

with exactly \(N\) raw queries and no parity or prefix garbage.  Grover
search over \(g\) therefore uses \(O(N\sqrt G)\) raw queries,
\(O(N\sqrt G\log(GP))\) elementary routing gates, and
\(O(\log G+\log P)\) workspace at constant failure probability.  It needs
neither a parity table nor QRAM.  Together with (21),

\[
 Q_{\epsilon}(\operatorname{OPT})=\Theta(N\sqrt G)
 \qquad\text{for every }\epsilon<1/20,                      \tag{21b}
\]

including on the zero-or-one-winner promise.  Under that promise, exact
one-solution amplitude amplification followed by exact parity verification
also computes the value with zero error in \(\Theta(N\sqrt G)\) queries: on
the zero-winner input the search may return an arbitrary component, which
the final exact verification rejects.
At the non-strict additive-error endpoint \(\epsilon=1/20\), the public
midpoint \(57/20\) is valid for both values and uses zero queries; hence the
constant-accuracy threshold is sharp.  Full circuit, optimizer-recovery, and
exact-versus-unrestricted-query details are recorded in
`2026-09-02-winner-take-all-global-trace-search.md`.

For randomized classical queries, the lower bound already holds under the
promise that either every group parity is even or exactly one uniformly
random group \(J\) is odd.  Let \(\mathcal D_0\) draw every group
independently and uniformly conditional on even parity.  Let
\(\mathcal D_1\) first choose \(J\) uniformly from \([G]\), draw that group
uniformly conditional on odd parity, and draw all other groups as under
\(\mathcal D_0\).

Couple the two executions by returning the same independent fair answers to
the first \(N-1\) distinct positions queried in each group.  On the last
unseen position, return the unique sign that realizes the required parity;
repeated queries return their stored answers.  This is the exact
conditional-uniform distribution under arbitrary adaptive interleaving.
The transcripts remain identical until the algorithm completes group \(J\).
On its \(\mathcal D_0\) path, a depth-\(r\) tree completes a set \(S\) of at
most \(\lfloor r/N\rfloor\) groups.  Since \(J\) is independent and uniform,
\[
 \operatorname{TV}\!\left(\mathsf{Tr}_{\mathcal D_0},
                           \mathsf{Tr}_{\mathcal D_1}\right)
 \le {\mathbb E|S|\over G}
 \le {r\over NG}.                                           \tag{21c}
\]
The coupling may include the common internal seed of a randomized
algorithm.  Worst-case success at least \(2/3\) makes the two output
probabilities differ by at least \(1/3\), so (21c) forces
\(r\ge NG/3\).  Reading all raw signs gives the matching deterministic
upper bound.  Thus \(R=\Theta(NG)\) both for the zero-versus-one promise and,
by restriction, for unrestricted OR.

## 5. Public-start condition-one Newton geometry

Use the product log-det barrier on the PSD blocks only:

\[
 \Phi_\mu(X)=\frac1P\sum_{g,i}\langle C_{g,i},X_{g,i}\rangle
             -\mu\sum_{g,i}\log\det X_{g,i}.                 \tag{22}
\]

The free accumulators have no barrier.  Take the public feasible point and
parameter

\[
                         X_{g,i}^0=\frac1{3G}I,\qquad
                         t_g^0=\frac gG,\qquad
                         \mu=\frac1{GP}.                     \tag{23}
\]

Every start block has inverse \(3GI\).  Thus the PSD-block gradient and
Hessian in isometric-svec coordinates are

\[
 g_{g,i}=\frac1P(C_{g,i}-3I),\qquad
 \nabla_X^2\Phi_\mu(X^0)=\frac{9G}{P}I.                      \tag{24}
\]

They are public.  All primal equality residuals, including the accumulator
rows, vanish.  The free-scalar stationarity residual is also public and zero.
All input dependence remains in the signed-copy operator on the left of the
unreduced Newton KKT equations.

More explicitly, if \(\mathcal A_\sigma\) denotes all copy and accumulator
rows and
\(H_0=\operatorname{Diag}((9G/P)I_X,0_t)\), one multiplier-sign convention
gives

\[
 \mathcal A_\sigma(\Delta X,\Delta t)=0,\qquad
 H_0(\Delta X,\Delta t)-\mathcal A_\sigma^*\Delta y=-(g,0).   \tag{24a}
\]

Both displayed right-hand sides are public.  The zero block in \(H_0\) is
why no ambient-Hessian condition number is claimed before the free variables
are eliminated.

Eliminate the public accumulator directions and copy rows.  A PSD-root
tangent is a tuple \(Y=(Y_1,\ldots,Y_G)\) satisfying

\[
                         \sum_g\operatorname{tr}Y_g=0.        \tag{25}
\]

The physical tangent blocks are \(R_{g,i}Y_gR_{g,i}^T\).  Summing their
quadratic forms from (24) gives

\[
 \boxed{\nabla^2_{\rm root}\Phi_\mu(X^0)=9G I_{6G-1}}        \tag{26}
\]

on (25).  Equivalently, the isometry

\[
 \mathcal W_\sigma(Y)=P^{-1/2}
       (R_{g,i}Y_gR_{g,i}^T)_{g,i}                           \tag{27}
\]

pulls the PSD-block Hessian back to \((9G/P)I_{6G-1}\).  Both forms have
condition number exactly one, including the \(G-1\) directions that
redistribute trace among groups.  This statement concerns the PSD-root
barrier metric after exact public elimination; the Euclidean saddle matrix
including unbarriered \(t_g\)'s is not asserted to have condition one.

Let

\[
                         A_h=H_{12}+H_{23}+hH_{13}.            \tag{28}
\]

Pulling (24) to group \(g\)'s root gives gradient \(uA_{h_g}\).  It is
trace zero, so projection onto (25) does not couple groups.  The root and
accumulator directions are

\[
                         \boxed{\Delta Z_g=-\frac{u}{9G}A_{h_g},
                         \qquad \Delta t_g=0.}                \tag{29}
\]

Since \(\|A_h\|_F^2=6\), the Newton decrement is

\[
 \lambda^2
 =\sum_{g=1}^G\left\langle uA_{h_g},
                   \frac1{9G}uA_{h_g}\right\rangle
 =\frac{2u^2}{3}=\frac1{150},
 \qquad \lambda=\frac1{\sqrt{150}}<0.082.                   \tag{30}
\]

The undamped step is strictly feasible:

\[
 Z_g^0+\Delta Z_g
 =\frac1G\left(\frac13I-\frac u9A_{h_g}\right).              \tag{31}
\]

For \(h_g=+1\), the eigenvalues inside parentheses are
\(14/45,31/90,31/90\).  For \(h_g=-1\), they are
\(29/90,29/90,16/45\).  Therefore

\[
                         Z_g^0+\Delta Z_g\succeq\frac{14}{45G}I.          \tag{32}
\]

Orthogonal congruence gives the same lower bound for every physical block.
Each root direction is trace zero, so (8) stays exact with \(\Delta t=0\).

The restriction of (22) to the feasible affine space is standard
self-concordant.  The Dikin theorem gives the input-independent
next-decrement bound
\[
 \lambda_{\rm next}
 \le\left({\lambda\over1-\lambda}\right)^2
 ={1\over(\sqrt{150}-1)^2}<{1\over126}.                    \tag{32a}
\]
The product cone has barrier parameter \(3PG\), so the central-path
duality-gap scale at \(\mu=1/(GP)\) is \(\mu(3PG)=3\).  The displayed start
is only near that central point, with decrement (30), so this is not an
exact primal--dual gap certificate for the start itself.

### 5.1 Exact Newton-state complexity and the output-dilution boundary

The normalized root-direction amplitude state in (29) has a much lower
query complexity than the winner-take-all objective.  Define
\[
 |a_h\rangle={|\operatorname{svec}(A_h)\rangle\over\sqrt6},
 \qquad
 |\Delta(h_1,\ldots,h_G)\rangle
 ={1\over\sqrt G}\sum_{g=1}^G|g\rangle|a_{h_g}\rangle .   \tag{32b}
\]
The omitted scalar in (29) is common to all inputs and contributes only a
global phase.  In isometric svec coordinates, \(|a_+\rangle\) has equal
positive amplitude on the \(12,23,13\) edge coordinates, while
\(|a_-\rangle\) flips only the \(13\) amplitude.  Prepare a uniform group
register and \(|a_+\rangle\).  For each raw edge index \(j=1,\ldots,N\),
make one phase-kickback sign query with address \(g\), controlled on the
local edge label being \(13\) (and route the other labels to a public dummy
sign).  The product of the \(N\) phases is \(h_g\), so this prepares (32b)
exactly with \(N\) raw queries, independently of \(G\), and leaves no parity
workspace.

This upper bound is tight for exact preparation up to a factor two.  Fix all
groups except group 1 to public inputs, and let \(z\in\{0,1\}^N\) be group
1's raw string.  For the output density matrix
\(\rho_z=|\Delta\rangle\langle\Delta|\), the fixed cross entry between its
group-1 \(12\) and \(13\) coordinates is
\[
 \langle1,12|\rho_z|1,13\rangle
 ={(-1)^{z_1+\cdots+z_N}\over3G}.                          \tag{32c}
\]
Every entry of the density matrix output by a \(q\)-query circuit is a
multilinear polynomial of degree at most \(2q\) in the raw bits.  Exact
equality in (32c) therefore forces \(2q\ge N\), because parity has exact
degree \(N\).  More generally, trace-distance error \(\delta\) changes this
cross entry by at most \(2\delta\).  Scaling (32c) by \(3G\) gives a uniform
parity approximation of error at most \(6G\delta\); any error strictly below
one still has degree \(N\), by orthogonality to the full parity character.
Hence
\[
 q\ge {N\over2}\quad\text{whenever}\quad
 \delta<{1\over6G},
 \qquad
 Q_{\rm exact}(|\Delta\rangle)=\Theta(N).                 \tag{32d}
\]

Constant trace error is different because normalization dilutes one
component among \(G\).  Since \(\langle a_+|a_-\rangle=1/3\), the all-even
target and a target with one odd group have overlap and trace distance
\[
 1-{2\over3G},\qquad
 D_{\rm tr}={2\sqrt{3G-1}\over3G}=\Theta(G^{-1/2}).        \tag{32e}
\]
Thus one constant-accuracy Newton state cannot decode the zero-versus-one
OR with constant bias; for sufficiently large \(G\), the public all-even
state is itself within any fixed error tolerance of every unique-winner
target.  Equations (32b)--(32e) rule out an
\(\Omega(N\sqrt G)\) Newton-state conclusion from the value theorem.  The
extra \(\sqrt G\) hardness belongs to winner-revealing optimizer or scalar
value outputs, not to this normalized public-start direction state.

## 6. Robust approximate optimizers and winner recovery

The winner-take-all conclusion is robust, but the output contract matters.
First consider an exactly feasible root tuple in (17), and let

\[
 m_-:=\sum_{g:h_g=-1}\operatorname{tr}Z_g.              \tag{33}
\]

If at least one odd group exists and the objective is at most
\(14/5+\delta_{\rm obj}\), then (18) gives

\[
 {14\over5}+{m_+\over10}
 ={14\over5}m_-+{29\over10}m_+
 \le\sum_g\langle\overline C_{h_g},Z_g\rangle
 \le {14\over5}+\delta_{\rm obj},
 \qquad m_+=1-m_-,
\]

and hence

\[
                         \boxed{m_-\ge1-10\delta_{\rm obj}.} \tag{34}
\]

This is sharp whenever the instance has both an odd and an even group:
put trace \(1-10\delta_{\rm obj}\) on an odd minimum eigenvector and trace
\(10\delta_{\rm obj}\) on an even minimum eigenspace.  Thus objective error
\(1/100\) forces at least \(9/10\) of the root trace onto winning groups, but
objective error \(1/10\) permits an optimizer supported entirely on a
nonwinner.  If

\[
 \rho(X)={\bigoplus_{g,i}X_{g,i}\over
                 \sum_{g,i}\operatorname{tr}X_{g,i}}       \tag{35}
\]

is the physical density matrix of an exactly feasible tuple, measuring its
public group register returns an odd group with probability exactly \(m_-\).
Trace-distance error \(\delta_{\rm state}\) reduces this probability by at
most \(\delta_{\rm state}\).  This proves genuine winning-component recovery,
not only detection of the low scalar value.

No uniqueness or strict-complementarity assumption is hidden here.  Several
odd groups may tie, and the even component minimum eigenspace is
two-dimensional; (34) and the group-register measurement use only the total
trace on the union of odd groups.  The output contract is specifically the
trace-normalized block-density state (35).  A normalized
\(\operatorname{svec}\)-amplitude encoding weights group \(g\) by
\(\sum_i\|X_{g,i}\|_F^2\), rather than by its trace, so the same decoder and
constants do not follow without an additional concentration or unique-winner
promise.

There is also a robustness theorem for the original sparse formulation,
including its accumulator rows.  Let

\[
 E_{g,i}=X_{g,i}-G_{g,i}X_{g,i-1}G_{g,i}^T
 \quad(1\le i<P),                                      \tag{36}
\]

and let \(r_1,\ldots,r_G,r_{\rm top}\) be the residuals of the \(G\)
accumulator equations and the final anchor in (8), in their displayed row
scaling.  Suppose arbitrary blocks \(X_{g,i}\succeq0\) and arbitrary free
accumulators obey

\[
 \sum_{g,i\ge1}\|E_{g,i}\|_F^2
 +\sum_{g=1}^G r_g^2+r_{\rm top}^2\le\epsilon^2,
 \qquad
 f(X):={1\over P}\sum_{g,i}\langle C_{g,i},X_{g,i}\rangle
 \le \operatorname{OPT}+\delta_{\rm obj}.               \tag{37}
\]

This is exactly the Euclidean equality residual in isometric-svec
coordinates.  Gauge each path to its root frame:

\[
 Z_{g,i}=R_{g,i}^TX_{g,i}R_{g,i},qquad
 D_{g,i}=Z_{g,i}-Z_{g,i-1}=R_{g,i}^TE_{g,i}R_{g,i}.      \tag{38}
\]

Write \(T_0=\sum_g\operatorname{tr}Z_{g,0}\).  Telescoping the accumulator
chain gives

\[
                         |T_0-1|\le\sqrt{G+1}\,\epsilon. \tag{39}
\]

For the physical average trace

\[
 \overline T={1\over P}\sum_{g,i}\operatorname{tr}X_{g,i},
\]

telescoping each path and applying Cauchy--Schwarz gives

\[
 |\overline T-1|
 \le\left(G+1+3G\sum_{\ell=1}^{P-1}{\ell^2\over P^2}\right)^{1/2}\epsilon
 \le\sqrt{GP+1}\,\epsilon.                              \tag{40}
\]

Similarly, with
\(\widehat C_{g,i}=R_{g,i}^TC_{g,i}R_{g,i}\) and
\(W_{g,j}=P^{-1}\sum_{i=j}^{P-1}\widehat C_{g,i}\),

\[
 f(X)=\sum_g\langle\overline C_{h_g},Z_{g,0}\rangle
       +\sum_{g,j\ge1}\langle W_{g,j},D_{g,j}\rangle,
\]

and the local spectral bound in Section 2 yields

\[
 \left|\sum_{g,j}\langle W_{g,j},D_{g,j}\rangle\right|
 <{13\over4}\sqrt{GP}\,\epsilon.                       \tag{41}
\]

Indeed,
\(\|W_{g,j}\|_F<(13\sqrt3/4)(P-j)/P\), and the sum of the
squared suffix weights is less than \(GP/3\).

Assume a winner exists, and put
\(m_+=\sum_{g:h_g=+1}\operatorname{tr}Z_{g,0}\).  Equations
(37), (39), and (41) imply

\[
 m_+\le10\delta_{\rm obj}
       +28\sqrt{G+1}\,\epsilon
       +{65\over2}\sqrt{GP}\,\epsilon.                  \tag{42}
\]

The physical average trace on even groups differs from \(m_+\) by at most
\(\sqrt{GP}\epsilon\).  Consequently, if

\[
 \delta_{\rm obj}\le{1\over100},
 \qquad
 \epsilon\le{1\over1000\sqrt{GP}},                     \tag{43}
\]

then measuring the group register of (35) returns an odd group with
probability greater than \(6/7\).  To check the constants, put
\(s=\sqrt{GP}\epsilon\le1/1000\).  Since \(P\ge33\),
\(\sqrt{G+1}\epsilon< s/4\); (42) and the extra physical-trace error give
even-group numerator less than
\(1/10+(81/2)s\), while (40) gives total denominator greater than
\(1-(33/32)s\).  Their ratio is less than \(1/7\).  A state within trace
distance \(1/100\) of (35) still returns a genuine odd component with
probability greater than \(6/7-1/100>5/6\).

The same state detects whether a winner exists without subsequently reading
the selected group's \(N\) signs.  Define the public Hermitian contraction

\[
 M={1\over2/5}\left(\bigoplus_{g,i}C_{g,i}-{57\over20}I\right).           \tag{44}
\]

Its norm is at most one because every local cost has spectrum in
\((11/4,13/4)\), and

\[
 \operatorname{tr}\left((\bigoplus_{g,i}C_{g,i})\rho(X)\right)
 ={f(X)\over\overline T}.                                \tag{45}
\]

Under (43), if a winner exists, (37) and (40) give the right-hand side of
(45) less than \(2.82\).  If no winner exists, (39)--(41) give it greater
than \(2.89\).  Therefore

\[
 \begin{cases}
  \operatorname{tr}(M\rho(X))<-3/40,&\text{some }h_g=-1,\\
  \operatorname{tr}(M\rho(X))>1/10,&\text{all }h_g=+1.
 \end{cases}                                             \tag{46}
\]

The fixed POVM \((I\pm M)/2\), with the negative outcome interpreted as
``winner exists,'' has constant bias.  Trace-distance error \(1/100\) leaves
a fixed positive bias, and a constant number of repetitions reaches bounded
error.

> **Robust approximate-optimizer theorem.**  For every input, let an
> algorithm prepare a state within trace distance \(1/100\) of (35) for some
> PSD blocks and free accumulators satisfying (37) with the tolerances (43).
> Then the state determines whether any group has odd parity with constant
> bias, so its preparation uses \(\Omega(N\sqrt G)\) raw coefficient queries.
> On every yes-instance, measuring the public group register of that state
> returns an actual odd winning group with probability greater than \(5/6\).

The query lower bound follows from Section 4.  The winning-label conclusion
is a property of the output distribution; verifying a measured label from
raw signs would cost another \(N\) queries, but verification is unnecessary
for the fixed-observable decision reduction.

The residual order in (43) is necessary.  On an all-even base input, for
each of the \(GN\) pairs \((g,j)\), flip only raw sign \(j\) in group \(g\)
and take the neighboring instance's exact optimizer supported on that newly
odd group with root matrix
\(Z_-^*=r_-r_-^T\), where \(r_-=(1,-1,1)^T/\sqrt3\).  Average these \(GN\)
physical optimizers.  The result is PSD, satisfies the accumulator equations
exactly, has global root trace one, and has objective exactly \(14/5\), even
though the base optimum is \(29/10\).  Under the base copy equations,
precisely the \(GN\) hidden transitions have nonzero residual.  After
conjugation to the base root frame, each residual is

\[
 {D_-Z_-^*D_--Z_-^*\over GN},
 \qquad D_-=\operatorname{Diag}(-1,1,1),
\]

and \(\|D_-Z_-^*D_--Z_-^*\|_F=4/3\).  Hence the total residual is

\[
                         {4\over3\sqrt{GN}}
 ={4\sqrt{33}\over3\sqrt{GP}}.                          \tag{47}
\]

Its density state makes (44) report that a winner exists although the base
input has none.  Thus the theorem has the sharp
\(\Theta((GP)^{-1/2})=\Theta(L^{-1/2})\) feasibility-residual scale, though
the numerical constant \(1/1000\) is not optimized.  Constant residual, or
even a sufficiently large constant times \(L^{-1/2}\), cannot force winner
detection under only PSD and the objective upper bound.

The objective upper bound is essential.  Approximate feasibility alone cannot
decode the OR: the public point (23) has zero equality residual and is strictly
PSD for every input, while being completely input independent.

## 7. Non-SOCP geometry

The root feasible set \(\mathcal B_G\) in (10) is compact and

\[
                         \operatorname{cone}(\mathcal B_G)
                         =(\mathbb S_+^3)^G.                  \tag{48}
\]

If \(\mathcal B_G\) had a lift over a finite product of second-order cones,
homogenizing that lift would give one for its conic hull.  Projecting the
conic hull onto one factor would then give a finite SOC lift of
\(\mathbb S_+^3\), contradicting Fawzi's theorem.  Hence neither the root
spectrahedron nor the original path-and-accumulator feasible set has a finite
SOC lift.

## 8. Caveats and novelty calibration

The OR, parity, Grover, and composition ingredients are established.  In
particular, Høyer, Lee, and Špalek,
[*Tight adversary bounds for composite functions*](https://arxiv.org/abs/quant-ph/0509067),
develop the costed adversary composition rule, and Belovs and Lee,
[*The quantum query complexity of composition with a relation*](https://arxiv.org/abs/2004.06439),
state the perfect Boolean negative-adversary composition identity that gives
an alternative route to (21).  The explicit witness in Section 4 uses only
the standard positive-weight adversary theorem.  Tight characterization by
the general adversary bound follows from
Reichardt,
[*Reflections for quantum query algorithms*](https://arxiv.org/abs/1005.1601).
The matching upper bound is standard search with an unknown number of marked
items, as in Boyer, Brassard, Høyer, and Tapp,
[*Tight bounds on quantum searching*](https://arxiv.org/abs/quant-ph/9605034).
For genuinely multivalued component optima, the corresponding abstract layer
is Dürr and Høyer's
[*A Quantum Algorithm for Finding the Minimum*](https://arxiv.org/abs/quant-ph/9607014);
the present two-value promise needs only search.
The parity factor is classical query-complexity folklore made precise, for
example, by Farhi, Goldstone, Gutmann, and Sipser,
[*A Limit on the Speed of Quantum Computation in Determining Parity*](https://arxiv.org/abs/quant-ph/9802045),
and by the polynomial method of Beals et al.,
[*Quantum Lower Bounds by Polynomials*](https://arxiv.org/abs/quant-ph/9802049).

The winner-take-all identity (18)--(19) is also not new machinery.  It is the
Rayleigh--Ritz principle applied to a block-diagonal cost, or equivalently
linear resource allocation over the simplex of block traces: one total trace
budget can be placed in a minimum-eigenvalue block.  No novelty should be
claimed for this direct-sum trace identity by itself.

There is a substantial optimization-methodology precedent.  Van Apeldoorn,
Gilyén, Gribling, and de Wolf,
[*Quantum SDP-Solvers: Better upper and lower bounds*](https://arxiv.org/abs/1705.01843),
Section 4, especially Theorem 29 and Corollary 30, embed a promise
\(\mathrm{MAJ}\circ\mathrm{OR}\circ\mathrm{MAJ}\) function into a two-value
LP optimum and transfer adversary composition to quantum LP and SDP value
lower bounds.  Apers and Gribling,
[*Quantum speedups for linear programming via interior point methods*](https://arxiv.org/abs/2311.03215v3),
Theorem 8.4, give a row-sparsity-aware variation and state both quantum and
randomized coefficient-query bounds.  Thus neither embedding a composed
Boolean problem into an optimization value, obtaining a constant objective
gap, nor separating quantum from randomized coefficient queries is new here.
Those earlier programs do not use parity holonomy, a single trace budget over
PSD components, or the public-start Newton geometry below.

For the randomized side, Ben-David and Kothari,
[*Randomized Query Complexity of Sabotaged and Composed Functions*](https://theoryofcomputing.org/articles/v014a005/),
provide general composition machinery.  The specialized \(\Theta(NG)\)
statement here does not require that machinery: the parity-conditioned
simulation in Section 4 is a complete Yao-style proof.

The non-SOCP fact is Fawzi,
[*On representing the positive semidefinite cone using the second-order
cone*](https://arxiv.org/abs/1610.04901).

The defensible candidate new part is therefore only the optimization-native
conjunction: one bounded-incidence public normalization chain converts sparse
intrinsic parity-holonomy components into an exact spectral minimum, producing
a constant-gap \(\operatorname{OR}\circ\operatorname{PARITY}\) value problem
while a public strictly feasible start retains a condition-one PSD-root
Hessian, constant decrement, and strictly feasible full step.  A targeted
open-primary-source search through September 2, 2026 found no theorem with
this complete conjunction.  This is evidence against an obvious exact
collision, not proof of priority.  The linear classical exponent, the
\(N\sqrt G\) quantum exponent, and the direct-sum minimum mechanism should not
be listed separately as new results.

The free accumulators keep scalar incidence bounded, but they are not barrier
variables.  Equation (26) is the exact Hessian after their public elimination,
not a condition-number statement about a singular ambient Hessian or the full
saddle KKT matrix.  Equality multipliers along the paths can grow.

The scalar value theorem is for the exact displayed equalities.  Section 6
proves robustness only under its explicit \(O((GP)^{-1/2})\) Euclidean
feasibility-residual contract, and the mixture (47) rules out a generic
constant-residual replacement.  Supplying path parities or eliminated root
costs has performed the hard composition.  If preprocessing uses \(S\) raw
queries and later adaptive iterations use \(q_t\) more before returning the
value or a decodable output from Section 6, then
\[
                            S+\sum_tq_t=\Omega(N\sqrt G).    \tag{49}
\]
The raw-coefficient theorem does not cover an arbitrary input-dependent
block-encoding completion supplied at unit cost.  Constructing such an
oracle, or a parity, prefix, nullspace, or eliminated-cost table, must be
charged to \(S\).  Finally, one normalized global
Newton-direction state is a compressed output and need not reveal the OR with
constant bias; Section 5 is a conditioning and public-residual theorem, not an
additional \(\Omega(N\sqrt G)\) state-preparation claim.
