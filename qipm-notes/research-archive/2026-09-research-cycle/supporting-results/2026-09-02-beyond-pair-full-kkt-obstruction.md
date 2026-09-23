# Beyond signed pairs: obstructions to a bounded hard full-KKT direction

Date: 2026-09-02

## Question and outcome

Can one replace scalar signed-copy pairs by rotations, simplex/permutation
states, circulations, or public antisymmetric sources and obtain all of the
following simultaneously?

1. linear dimension and bounded row/column degree;
2. bounded coefficients and one-bit-local input dependence;
3. public, simply preparable Newton right-hand sides;
4. primal and slack starts bounded above and below by positive constants;
5. a coordinatewise bounded complete Newton direction; and
6. a parity-hard primal component occupying constant mass in that full state.

No such construction was found.  Two algebraic obstructions cover the natural
attempts:

- a global Newton work identity applies to arbitrary LP equality matrices;
- a two-input block-flow theorem applies to constant-dimensional orthogonal
  copy encodings, including swaps, simplex permutations, and real rotations.

The block theorem shows that changing the local representation does not remove
the dual accumulation.  A linear hard output region behind a bounded interface
still forces an \(\Omega(P)\) equality-multiplier coordinate at constant local
scale.  Public antisymmetric sources can cancel one parity class but not both.
For signed pairs, and for swaps after restricting to their one-dimensional
antisymmetric mode, the input-incidence theorem in
`2026-09-02-signed-copy-cut-multiplier-conservation.md` also rules out
replacing the small interface by linearly many independently hard interfaces
while retaining linear size and one-bit locality.  An analogous incidence
theorem for arbitrary orthogonal block labels is not proved here.

This is not an impossibility theorem for every sparse LP formulation.  It
leaves open arbitrary nonorthogonal mixed-mode constraints, input-dependent
sources whose loading is charged in a different oracle, and output interfaces
that omit or quotient the equality multipliers.

## 1. A representation-independent Newton work identity

At a positive primal--dual start, write the standard Newton equations as

\[
\begin{aligned}
 A\Delta x&=r_p,\\
 A^T\Delta y+\Delta s&=r_d,\\
 S^0\Delta x+X^0\Delta s&=r_c.
\end{aligned}
\tag{1}
\]

Put

\[
 H=(X^0)^{-1}S^0,
 \qquad g=(X^0)^{-1}r_c-r_d.
\tag{2}
\]

Eliminating \(\Delta s\) gives

\[
                       H\Delta x-A^T\Delta y=g.
\tag{3}
\]

Taking the inner product with \(\Delta x\) yields the exact identity

\[
 \boxed{
 r_p^T\Delta y
 =\Delta x^TH\Delta x-g^T\Delta x.}
\tag{4}
\]

This uses no sparsity, graph, sign, rank, or centrality assumption.  In
particular, if \(g=0\), \(H\succeq\rho I\), and
\(\|r_p\|_1\le R\), then

\[
                  \|\Delta y\|_\infty
                  \ge\frac{\rho\|\Delta x\|_2^2}{R}.
\tag{5}
\]

Thus a constant-scale primal correction with \(\Theta(P)\) squared norm and
a root-sparse public primal residual forces an \(\Omega(P)\) multiplier for
**every** equality representation.  Redundant rows and branching do not help
unless they also enlarge the primal right-hand-side norm or the public source
term in (4).

The term \(g^T\Delta x\) is the genuine loophole.  It can cancel the scalar
work in (4).  A fixed public \(g\), however, cannot cancel two separated
parity codewords locally after their common public components are subtracted.
The next theorem makes that statement precise for block-copy encodings.

## 2. Orthogonal block-copy model

Let each graph vertex \(v\) carry a constant-dimensional real code block
\(z_v\in\mathbb R^k\).  The block may be a linear difference projection of
nonnegative LP variables.  A copy edge \(e=(u,v)\) imposes

\[
                         z_v-U_ez_u=0,
 \qquad U_e^TU_e=I_k.
\tag{6}
\]

Signed copies have \(k=1\), a two-state simplex uses a swap permutation, and
rotation encodings use real orthogonal \(U_e\).  First allow one nonzero
scalar \(r_e\) to scale all \(k\) equations on edge \(e\); the physical
vector force is

\[
                         f_e=r_e\Delta y_e\in\mathbb R^k.
\tag{7}
\]
More generally, a nonsingular block row scaling \(R_e\) gives
\(f_e=R_e^T\Delta y_e\), and every statement below remains valid with
\(B=\max_e\|R_e\|_{\rm op}\).  This is the exact stationarity contribution;
calling \(r_e\) a diagonal scale would be ambiguous when \(k>1\).

Consider an output region \(S\) whose internal copy matrices and all local
Newton data are public.  Assume the internal connection is flat: there are
public orthogonal transports \(G_v\) such that

\[
                         U_e=G_vG_u^T
 \qquad(e=(u,v)\text{ internal to }S).
\tag{8}
\]

Trees, arborescence fanouts, DAG copies with path-consistent transports,
permutation copies satisfying the same flatness condition, and any cycle with
trivial public holonomy satisfy (8).  A general DAG with inconsistent merging
paths need not.  Define transported corrections
\(\widehat z_v=G_v^T\Delta z_v\).

After eliminating local slack corrections and projecting stationarity onto
the code block, assume it has the form

\[
 \operatorname{div}_U(f)_v=D_v\Delta z_v+g_v,
 \qquad D_v\succeq\rho I_k,
\tag{9}
\]

where \(g_v\) is public and common to both input instances.  At a
coordinatewise constant-scale primal/slack start, an orthogonal compression
of \((X^0)^{-1}S^0\) to a fixed code subspace has a constant positive lower
bound.  The exact decoupled equation (9), however, additionally requires that
the code subspace be invariant or that all coupling to complementary modes be
absorbed into a source \(g_v\) that is numerically common to the two inputs.
Pair-asymmetric public objectives and complementarity right-hand sides may be
absorbed into \(g_v\) only when their resulting projected source is common.

## 3. Two-parity block-flow obstruction

### Theorem 1 (orthogonal-copy cut law)

Take two inputs with opposite parity, denoted \(+\) and \(-\), but the same
public start and Newton right-hand sides.  Suppose throughout \(S\) their
transported code corrections have a common separation

\[
             \widehat z_v^+-\widehat z_v^-=w,
             \qquad \|w\|_2\ge2a>0.
\tag{10}
\]

Assume that the internal transports \(U_e\), gauges \(G_v\), matrices
\(D_v\), and source vectors \(g_v\) in (9) are the same numerical objects for
the two inputs.  The matrices \(D_v\) may vary with \(v\), and need not
commute with one another.  Separate lower bounds
\(D_v^p\succeq\rho I\) are not sufficient if the two metrics differ: already
in one dimension, \(z^+=2,z^-=1,D^+=1,D^-=2\) has nonzero separation but
\(D^+z^+-D^-z^-=0\).

If \(\partial S=\varnothing\), the assumptions above are inconsistent with
\(\rho,a>0\).  Otherwise, if \(|r_e|\le B\) on the boundary (or
\(\|R_e\|_{\rm op}\le B\) in the block-scaled version), then

\[
 \boxed{
 \max_{p\in\{+,-\}}
 \|\Delta y_{\partial S}^p\|_{2,\infty}
 \ge\frac{\rho a|S|}{B|\partial S|}.}
\tag{11}
\]

Here \(\|\cdot\|_{2,\infty}\) is the largest Euclidean norm of one
constant-dimensional row-multiplier block.  Consequently, a linear output
region behind \(O(1)\) rows has an \(\Omega(P)\) multiplier on at least one
parity class.

#### Proof

Transport (9) by \(G_v^T\).  Orthogonality preserves the eigenvalue bound:

\[
                  \widehat D_v:=G_v^TD_vG_v\succeq\rho I.
\]

In the transported coordinates, every internal edge is an ordinary vector
copy edge.  Explicitly, an internal edge \(e=(u,v)\) has transported force
\(\widehat f_e=G_v^Tf_e\): its contribution is \(+\widehat f_e\) at \(v\)
and \(-\widehat f_e\) at \(u\).  For a boundary edge, transport its
stationarity contribution at the unique endpoint in \(S\).  This is
\(G_v^Tf_e\) for an entering edge and
\(-G_u^TU_e^Tf_e\) for an exiting edge, and in either case its norm is
\(\|f_e\|_2\).

Subtract the \(-\) stationarity equation from the \(+\) equation and sum over
\(S\).  The common transported sources \(G_v^Tg_v\) and all internal forces
cancel.  Writing
\(F_\partial\) for the signed sum of these boundary-force differences,

\[
                       F_\partial=
                       \sum_{v\in S}\widehat D_vw.
\tag{12}
\]

Taking the inner product with \(w\) gives

\[
 w^TF_\partial
 =\sum_{v\in S}w^T\widehat D_vw
 \ge\rho|S|\|w\|_2^2.
\]

Thus \(\|F_\partial\|_2\ge\rho|S|\|w\|_2\ge2\rho a|S|\).
On the other hand, the triangle inequality and (7) give

\[
 \|F_\partial\|_2
 \le B|\partial S|
 \left(
  \|\Delta y_{\partial S}^+\|_{2,\infty}
 +\|\Delta y_{\partial S}^-\|_{2,\infty}
 \right).
\]

At least one term is therefore at least the right side of (11). \(\square\)

The theorem is a strong-monotonicity statement.  It does not require the
individual source vectors in (9) to point in a common cone.  This is why a
rotation or higher-dimensional permutation does not evade the scalar
positive-flow theorem.

### Varying but coherently separated codewords

The common-vector hypothesis (10) can be weakened.  It is enough that there
is one public unit vector \(h\) and a constant \(a>0\) such that

\[
 h^T\widehat D_v
  (\widehat z_v^+-\widehat z_v^-)
 \ge2\rho a
 \qquad(v\in S).
\tag{13}
\]

The same proof takes the inner product of the boundary identity with \(h\).
This covers public periodic sign or rotation patterns after applying their
known local decoding transports.

## 4. Candidate encodings and why they fail

### 4.1 Swap and simplex/permutation copies

Encode a Boolean state by a two-coordinate simplex vector, with a hidden bit
acting by the swap matrix.  More generally, use a constant-dimensional
permutation representation.  A public uniform start makes the local Newton
metric positive definite and permutation invariant on the nontrivial code
subspace.  In a public output-copy region downstream of the hidden
computation, the accumulated **public internal** permutations provide the
transports \(G_v\); the two possible parity seeds then decode to codewords
with one fixed constant separation \(w\).  If hidden permutations remain
inside \(S\), Theorem 1 does not apply unless one can choose a common public
flat transport for both inputs.

A fanout tree or redundant bounded-degree copy graph therefore satisfies
Theorem 1.  Its descendant output region has a constant-size seed cut and
forces an \(\Omega(K)\) multiplier.  Giving it \(\Theta(K)\) independent
boundary channels avoids that one cut.  For a two-state swap, its
antisymmetric mode is a scalar signed copy, so the local-input incidence
frontier then charges \(\Omega(KN)\) sensitive coefficient incidences.  For
\(K=\Theta(N)\), this realization has quadratic rather than linear size,
while the raw parity lower bound remains only \(\Omega(N)\).  The same
incidence conclusion for a general permutation representation requires an
additional faithful-label argument; Theorem 1 alone does not supply it.

### 4.2 A bounded cyclic rotation candidate

The most promising circulation attempt uses a real quarter-turn

\[
 J=\begin{pmatrix}0&-1\\1&0\end{pmatrix}
\]

and, for \(N\) divisible by four, the local equations

\[
                         z_i=\sigma_iJz_{i-1}.
\tag{14}
\]

Close the cycle with

\[
                         z_0-Jz_N=e_1.
\tag{15}
\]

Since \(J^N=I\), writing \(p=\prod_i\sigma_i\) gives

\[
 z_0(p)=(I-pJ)^{-1}e_1
       =\frac12\begin{pmatrix}1\\p\end{pmatrix}.
\tag{16}
\]

Both parity classes are bounded, and their internal two-dimensional states
are orthogonal after normalization.  Moreover

\[
 z_i=\tau_iJ^iz_0(p),
\]

so a public inverse rotation \(J^{-i}\) makes every one of the \(N\) blocks
carry the same parity codeword, up to the prefix sign \(\tau_i\).  That sign
is irrelevant to a block-local density-matrix or POVM decoder, because it is
a phase within the conditioned block; it is not one common global phase of
the coherently concatenated vector.  In the former output model this appears
to remove the explicit output plateau.

It does not yield a bounded full Newton direction.  In the clean
constant-scale case \(H=I\) and \(g=0\), the only nonzero primal source is the
two-coordinate closure right-hand side.  Every block has
\(\|z_i\|_2^2=1/2\).  Equation (4) therefore gives

\[
                     e_1^T\Delta y_{\rm close}
                     =\sum_{i=0}^{N}\|z_i\|_2^2
                     =\frac{N+1}{2}.
\tag{17}
\]

Thus the closure multiplier grows linearly.  Consistently, although
\(I-pJ\) is uniformly invertible as a two-dimensional monodromy matrix, the
full sparse **constraint** operator has a singular value \(\Theta(1/N)\): the
fixed quarter-turn is distributed over \(N\) local propagation steps.  This
statement has an exact spectral proof.  Put \(\tau_i=\prod_{j=1}^i\sigma_j\)
and make the orthogonal variable gauge
\(w_i=\tau_iJ^{-i}z_i\), together with the corresponding orthogonal row
gauges.  The propagation rows become
\(w_i-w_{i-1}\), while the closure row becomes

\[
                         w_0-pJw_N.
\tag{18}
\]

Let \(A_p\) denote this \(2(N+1)\)-dimensional twisted-cycle difference
operator.  Complexifying the two-dimensional blocks diagonalizes \(pJ\),
whose eigenvalues are \(\{+i,-i\}\) for either value of \(p\).  The singular
values of \(A_p\) are

\[
 2\left|\sin\!\left(
       \frac{2\pi\ell\mathbin\pm\pi/2}{2(N+1)}
             \right)\right|,
 \qquad \ell=0,\ldots,N.
\tag{19}
\]

Consequently,

\[
 \sigma_{\min}(A_p)=2\sin\frac{\pi}{4(N+1)}=\Theta(N^{-1}),
 \qquad
 \sigma_{\max}(A_p)=2\cos\frac{\pi}{4(N+1)}=\Theta(1).
\tag{20}
\]

The associated eliminated saddle matrix
\(\left(\begin{smallmatrix}I&A_p^T\\A_p&0\end{smallmatrix}\right)\)
has a still smaller absolute eigenvalue \(\Theta(N^{-2})\), because its paired
eigenvalues are
\((1\pm\sqrt{1+4s^2})/2\) for singular values \(s\) of \(A_p\).

There is an explicit LP Newton realization with the claimed \(H=I,g=0\), a
public source, and no signed LP variables.  Let \(C_\sigma\) be the ungauged
constraint operator in (14)--(15), let \(r\) be zero except for \(e_1\) in
the closure block, and define the orthonormal difference projection
\[
 P=2^{-1/2}[I,-I],\qquad PP^T=I.
\tag{21}
\]
Use nonnegative LP variables \(x=(x^+,x^-)\) and equality matrix
\(A_\sigma=C_\sigma P\).  Since
\(A_\sigma A_\sigma^T=C_\sigma C_\sigma^T\), this LP matrix has exactly the
same nonzero singular values as the code constraint operator.  At the public
positive start
\[
 x^0=s^0=\mathbf1,\qquad y^0=0,
 \qquad b=r,\qquad c=\mathbf1,
\tag{22}
\]
one has \(P\mathbf1=0\).  Hence the primal Newton right-hand side is the
public vector \(r=b-A_\sigma x^0\), the dual right-hand side is zero, and a
centering choice with \(r_c=0\) gives exactly \(H=I,g=0\).  The Newton
equations imply
\[
 \Delta x=P^TC_\sigma^T\Delta y,
 \qquad z:=P\Delta x=C_\sigma^T\Delta y,
 \qquad C_\sigma z=r.
\tag{23}
\]
Therefore \(z=C_\sigma^{-1}r\),
\(\|\Delta x\|_2=\|z\|_2\), and (17) holds without a hidden constant:
\[
 r^T\Delta y=\|\Delta x\|_2^2=\|z\|_2^2=(N+1)/2.
\tag{24}
\]

The choice \(r_c=0\) is the clean work/spectral special case, not a
zero-progress limitation.  At the same start, choose any target
complementarity \(\widehat\mu=\theta\), so

\[
                    r_c=(\theta-1)\mathbf1,
             \qquad g=(\theta-1)\mathbf1.
\tag{25}
\]

Because \(P\mathbf1=0\), one also has
\(A_\sigma\mathbf1=0\).  The Newton solution is therefore

\[
 \Delta x=(\theta-1)\mathbf1+P^Tz,qquad
 \Delta s=-P^Tz,qquad
 z=C_\sigma^{-1}r,
\tag{26}
\]

with exactly the same \(\Delta y\) as above.  Indeed,
\(A_\sigma\Delta x=r\),
\(A_\sigma^T\Delta y+\Delta s=0\), and
\(\Delta x+\Delta s=(\theta-1)\mathbf1=r_c\).
Consequently the multiplier work remains

\[
 r^T\Delta y=\|z\|_2^2=\frac{N+1}{2}.
\tag{27}
\]

In particular, \(\theta=1/2\) is an exact Newton step that halves the target
complementarity.  Since
\(\|P^Tz\|_\infty=1/(2\sqrt2)\), the full step is strictly positive with the
uniform margins

\[
 \min_i(x_i^0+\Delta x_i)
    =\frac12-\frac1{2\sqrt2}>0,
 \qquad
 \min_i(s_i^0+\Delta s_i)
    =1-\frac1{2\sqrt2}>0.
\tag{28}
\]

It also retains constant primal parity mass.  The public vector
\(-\mathbf1/2\) is orthogonal to \(P^Tz\), since \(P\mathbf1=0\).  There are
\(4(N+1)\) nonnegative LP variables, so

\[
 \left\|-\frac12\mathbf1\right\|_2^2=N+1,
 \qquad
 \|P^Tz\|_2^2=\|z\|_2^2=\frac{N+1}{2},
\]

and the hard code component has exactly

\[
 \frac{\|P^Tz\|_2^2}{\|\Delta x\|_2^2}
 =\frac{(N+1)/2}{(N+1)+(N+1)/2}=\frac13
\tag{29}
\]

of the squared primal-direction norm.  Thus even a constant-factor centering
step with a constant-mass hard primal component retains the linear closure
multiplier.

The LP has four nonnegative variables per two-dimensional code block,
coefficients of magnitude at most \(1/\sqrt2\), bounded row and column
degree, and one-bit-local coefficient dependence.  Its \(b,c,x^0,s^0\) and
Newton source are public.  In the clean \(\theta=1\) case,
\(\|\Delta x\|_\infty=1/(2\sqrt2)\) and
\(\Delta s=-\Delta x\).  In the progress case \(\theta=1/2\),
\(\|\Delta x\|_\infty=1/2+1/(2\sqrt2)\) and
\(\|\Delta s\|_\infty=1/(2\sqrt2)\), with positivity already quantified in
(28).  Thus positive/negative encoding changes only the constant local
representation, not the exact work balance.

Direct matrix assembly for \(N=4,8,16,32,64\) verifies bounded primal
coordinates \(\|z\|_\infty=1/2\), the exact closure-multiplier component
\(e_1^T\Delta y_{\rm close}=(N+1)/2\), and smallest constraint singular
values approximately \(0.313,0.174,0.0924,0.0476,0.0242\), respectively,
in agreement with (20).

### 4.3 Circulations and periodic rotations

One may rotate the local code by a constant public angle so consecutive
stationarity demands point in different directions and appear to cancel.
The correct transported coordinates undo exactly those public rotations.
The Newton metric becomes \(G_v^TD_vG_v\succeq\rho I\), and Theorem 1 sums a
positive quadratic form in the common decoded separation.  Periodic rotations
therefore change the visible direction of the dual flow, not its required
work.

A genuinely source-free closed circulation is even more restrictive: summing
the transported stationarity equations gives zero boundary force but a
strictly positive right side, so no such constant-scale Newton correction
exists.  A closure or antisymmetric source restores solvability and must carry
the accumulated work.

### 4.4 Public antisymmetric source injection

Choosing the objective or complementarity right-hand side asymmetrically can
make \(g\) in (4) cancel the work for one designated codeword.  This does not
give a uniform two-parity construction.  In Theorem 1, the public source
\(g_v\) cancels exactly when the two instances are subtracted, leaving the
strongly monotone term \(D_v(z_v^+-z_v^-)\).  At least one parity class still
has the large boundary multiplier.

An input-dependent source can cancel both classes.  Direct pointwise loading
would place the parity-dependent codeword at \(\Theta(P)\) output locations,
while a coefficient oracle that returns those values from one address may
itself provide nonlocal parity access.  Either resource must be charged in a
complete lower-bound model.  The scalar signed-copy theorem charges a
bounded-degree, one-bit-local realization, but no general lower bound against
an implicit block-source construction is proved here.

### 4.5 Dense public primal residuals

A dense public \(r_p\) weakens (5), because \(r_p^T\Delta y\) can distribute
work among many bounded multiplier coordinates.  For a homogeneous parity
copy mode, however, public forcing contributes only a common particular
solution.  Subtracting the two parity instances removes that particular
solution, and Theorem 1 still applies to the hard homogeneous separation
behind any small interface.

To obtain \(\Theta(P)\) genuinely independent interfaces, one must propagate
the sensitivity of every input bit to each interface.  With bounded degree and
one-bit-local signed-copy or swap coefficients this costs \(\Omega(PN)\)
dependent incidences in the parity case.  Duplicating the entire parity
computation realizes this escape but has size \(\Omega(PN)\), so its
\(\Omega(N)\) query lower bound is not linear in the LP dimension.  For
general orthogonal block labels this conclusion is conditional on an
analogous incidence hypothesis.

## 5. Algorithmic representations

The obstruction concerns the literal complete Newton vector
\((\Delta x,\Delta y,\Delta s)\).  Several useful output models escape it,
but none supplies the requested bounded full-KKT state:

1. Return only the primal amplitude state.  The bounded-range condition-one
   theorem already gives linear raw-query hardness with bounded primal and
   slack scales; the large multiplier is omitted.
2. Return row forces or divergences modulo a circulation rather than canonical
   equality multipliers.  This is a different output interface.  Recovering
   the literal multipliers across the hard cut reintroduces the accumulation.
3. Rescale or precondition multiplier coordinates by \(1/P\).  If this is
   implemented as LP row scaling, coefficient magnitude or block-encoding
   normalization grows by \(P\).  If it is an output-only transform, recovery
   of the original full direction has the inverse scale.
4. Use dual homogeneity.  This is the known successful bounded-coordinate
   construction, but its positive slacks, objective, and complementarity scale
   are \(\Theta(1/P)\).

## 6. Literature and novelty calibration

Several ingredients of the obstruction are standard and are not claimed as
new.

- Equation (4) is the usual energy/virtual-work identity for a KKT saddle
  system, obtained by eliminating the slack block and pairing the two
  remaining equations.  Schur complements, multiplier stability, and
  conditioning of such systems have a large classical literature; see
  Benzi--Golub--Liesen,
  [*Numerical solution of saddle point
  problems*](https://doi.org/10.1017/S0962492904000212).
- Graphs with orthogonal edge transports are standard graph-connection
  objects.  Singer--Wu,
  [*Vector Diffusion Maps and the Connection
  Laplacian*](https://arxiv.org/abs/1102.0075),
  and Bandeira--Singer--Spielman,
  [*A Cheeger Inequality for the Graph Connection
  Laplacian*](https://arxiv.org/abs/1204.3873),
  use orthogonal parallel transports and gauge/synchronization viewpoints.
  Trivializing a flat connection and cancelling internal transported fluxes
  in a cut are therefore not new operations.
- Vector- or sheaf-valued conservation and flow--cut principles are also
  established at substantially greater generality; see Krishnan,
  [*Flow-Cut Dualities for Sheaves on
  Graphs*](https://arxiv.org/abs/1409.6712).
  Recent matrix-weighted consensus work also derives graph-cut conditions
  for vector-valued agreement; for example, Chen et al.,
  [*Subspace Consensus of Matrix-Weighted
  Networks*](https://arxiv.org/abs/2607.06970).
  These works do not concern LP Newton multipliers or quantum output states.
- The Fourier diagonalization in (18)--(20) is the standard spectrum of a
  twisted cyclic difference operator.  The resulting
  \(\Theta(N^{-1})\) constraint singular value and
  \(\Theta(N^{-2})\) small saddle eigenvalue are not standalone novelty
  claims.

Interior-point analyses already use graph Laplacians and electrical flows;
Mądry,
[*Navigating Central Path with Electrical
Flows*](https://arxiv.org/abs/1307.2205),
is a representative primary source.  Published QIPM analyses such as
Kerenidis--Prakash,
[*A Quantum Interior Point Method for LPs and
SDPs*](https://arxiv.org/abs/1808.09266),
Mohammadisiahroudi--Fakhimi--Terlaky,
[*Efficient use of quantum linear system algorithms in inexact infeasible
IPMs for linear optimization*](https://arxiv.org/abs/2307.14445),
and Apers--Gribling,
[*Quantum speedups for linear programming via interior point
methods*](https://arxiv.org/abs/2311.03215),
analyze algorithms, conditioning, or conventional LP query lower bounds.  A
targeted search found no theorem in them, or in the connection and flow
literature above, that lower-bounds a literal full-KKT
equality-multiplier block from a parity-separated output region.

Theorem 1 itself is a short strong-monotonicity-plus-cut argument on a flat
orthogonal connection.  The defensible candidate contribution is not a new
connection-Laplacian or flow-cut law, but its **QIPM gadget-design
application**: two input instances cancel every public source, while a
coherently decoded codeword separation and a uniformly positive Newton
metric force boundary multiplier work.  Combined with separately charged
one-bit incidences in the signed or swap cases, this rules out the listed
bounded full-direction parity amplifiers.  No general incidence theorem for
arbitrary orthogonal block labels is proved here.  Absence from a targeted
search is not proof of priority, so this synthesis should be described as
apparently new rather than as the first such result.

## 7. Status and scope

The global identity (4) is elementary saddle-system algebra.  The two-input
block-copy theorem applies to constant-dimensional orthogonal copies on a
public flat output region, with a common projected metric and common numerical
source on the two inputs.  Within that exact scope it explains in one argument
why swaps, simplex permutations, public periodic rotations, and bounded-degree
fanout do not beat the inverse-scale price.

The result does not cover every sparse LP.  In particular, a candidate using
nonorthogonal block maps with carefully balanced expanding and contracting
directions, constraints that mix the hard code subspace with symmetric local
modes, or a different compressed dual output may fall outside Theorem 1.
Such a candidate must still charge coefficient normalization, conditioning,
input-dependent source preparation, and recovery to the literal Newton
coordinates.  No bounded-scale, linear-size example satisfying all requested
properties was found.
