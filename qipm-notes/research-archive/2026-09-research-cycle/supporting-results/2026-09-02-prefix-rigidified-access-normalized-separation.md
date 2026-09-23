# Access-normalized separation for the prefix-rigidified Newton system

## Main conclusion

For the prefix-rigidified family in
`2026-09-02-prefix-rigidified-condition-one-newton-hardness.md`, the Newton
correction at the public start admits a canonical orthogonal decomposition

\[
 \Delta x=p_\sigma+Wz,\qquad
 p_\sigma=(A'_\sigma)^\dagger(b'-A'_\sigma x^0).            \tag{1}
\]

The complete reduced solve is public:

\[
 M=\frac{22}{27H^2}I,qquad z=z_*\mathbf1,qquad Mz=g,
\]

with public scalars \(z_*,g_*\).  Its normalized matrix is the identity, its
access-normalized inverse factor is exactly one, and its normalized right-hand
side and solution states require zero raw coefficient queries.

In contrast, preparing the canonical particular-correction state
\(|p_\sigma/\|p_\sigma\|\rangle\) to constant trace error requires
\(\Omega(N)=\Omega(P)\) raw coefficient queries.  Thus the end-to-end lower bound
does not merely say that some unspecified loading stage is hard: in the
Moore--Penrose gauge, all raw-query hardness can be localized to the affine
feasibility correction.  The exponent is tight because querying all \(N\) signs
suffices.

## 1. Primal feasibility equations at the public start

Use the public start and exact endpoint from the source note.  At node \(i\),

\[
 d_i^0=0,\qquad h_i^0=\frac{20}{27}H_i,\qquad
 q_i^0=\frac53H_i,\qquad t_i^0=\frac59H_i.
\]

The exact endpoint has

\[
 d_i^1=H_i\tau_i,\qquad h_i^1=H_i,\qquad
 q_i^1=\frac54H_i,\qquad t_i^1=\frac34H_i.                 \tag{2}
\]

Let

\[
 r_p=b'-A'_\sigma x^0.
\]

Every solution \(p\) of \(A'_\sigma p=r_p\) must therefore have

\[
 p_{d,i}=H_i\tau_i,qquad p_{h,i}=\frac7{27}H_i.           \tag{3}
\]

The cap equation at the start has residual \(20H_i/27\), so

\[
 p_{q,i}+p_{t,i}-2p_{h,i}=-\frac{20}{27}H_i,
 \qquad
 p_{t,i}=-\frac29H_i-p_{q,i}.                             \tag{4}
\]

At a rigidified prefix node \(i<T\), the new row uniquely fixes

\[
 p_{q,i}=-\frac5{12}H_i.                                  \tag{5}
\]

At a free node \(i\ge T\), \(p_{q,i}\) is the sole affine degree of freedom.

## 2. Exact Moore--Penrose correction

At a free node, the squared norm depending on \(p_q\) is

\[
 \frac12(p_q^2+H^2)+\left(\frac7{27}H\right)^2
 +\left(-\frac29H-p_q\right)^2.                           \tag{6}
\]

Its unique minimizer is

\[
 p_q=-\frac4{27}H,qquad p_t=-\frac2{27}H.                \tag{7}
\]

Equivalently, (7) is characterized by orthogonality to the surviving null
vector, because

\[
 W_i^Tp=\sqrt{\frac23}\left(\frac{p_q}{2}-p_t\right)=0.   \tag{8}
\]

The augmented matrix has full row rank and its kernel is spanned by these free
\(W_i\)'s.  Equations (3)--(8) therefore prove that this vector is precisely

\[
 p_\sigma=(A'_\sigma)^\dagger r_p.                        \tag{9}
\]

Explicitly, at every free node,

\[
 p_{\sigma,i}=H\left(
 \frac{\tau_i}{2}-\frac2{27},
 -\frac{\tau_i}{2}-\frac2{27},
 \frac7{27},-\frac2{27}
 \right).                                                  \tag{10}
\]

At a prefix node the null mode has been removed, so \(p_\sigma\) equals the full
Newton direction shown in the source note.

## 3. The reduced solve is completely public

The exact direction has \(\Delta q_i=-5H/12\) at every free node.  Subtracting
(7),

\[
 (\Delta q_i-p_{q,i})=-\frac{29}{108}H.                   \tag{11}
\]

Since adding \(W_i z_i\) changes \(q_i\) by
\(\sqrt{2/3}\,z_i\), the reduced coefficient vector is

\[
 z_i=-\frac{29}{72}\sqrt{\frac23}\,H
     =-\frac{29}{108}\sqrt{\frac32}\,H,qquad i\ge T.    \tag{12}
\]

It is the same public scalar at all \(P-T\) reduced coordinates.  From the
audited start calculation,

\[
 M:=W^T(X^0)^{-1}S^0W=mI,qquad
 m=\frac{22}{27H^2}.                                      \tag{13}
\]

Consequently the exact reduced right-hand side is

\[
 g=Mz=mz_*\mathbf1,                                      \tag{14}
\]

which is also public and uniform.  The hidden dependence of the Moore--Penrose
correction in the projected Newton equations cancels exactly into the public
quantity (14).

Normalize the block encoding at its exact norm \(\alpha_M=m\).  Then

\[
 M/\alpha_M=I,qquad \kappa(M)=1.                         \tag{15}
\]

For the standard inverse-state success/sensitivity factor,

\[
 \alpha_M\frac{\|M^{-1}g\|}{\|g\|}
 =m\frac{\|z\|}{m\|z\|}=1.                               \tag{16}
\]

The corresponding two-inverse filtering parameter is also exactly one:

\[
 \rho_M:=\alpha_M
 \frac{\|M^{-2}g\|}{\|M^{-1}g\|}
 =m\frac{m^{-2}\|g\|}{m^{-1}\|g\|}=1.                   \tag{16c}
\]

Equivalently, rescaling the public equation by \(m^{-1}\) gives
\(Iz=z\).  Preparing \(|g/\|g\|\rangle\),
\(|z/\|z\|\rangle\), or \(|Wz/\|Wz\|\rangle\) requires no raw
coefficient queries: they are respectively uniform reduced-coordinate states and
their image under the public sparse isometry \(W\).  Absolute factors such as
\(\|M^{-1}\|=27H^2/22\) cancel from the normalized inverse-state task exactly as
shown in (16).

Thus every usual multiplicative reduced-solve parameter---block normalization,
inverse scale relative to the right-hand side, condition number, and normalized
RHS preparation---is constant or free in the raw-query accounting.

Recovery from reduced to nullspace coordinates also has unit condition: \(W\) is
an isometry.  Moreover, the Moore--Penrose choice makes

\[
 \langle p_\sigma,Wz\rangle=0,
 \qquad
 \|\Delta x\|^2=\|p_\sigma\|^2+\|Wz\|^2.                 \tag{16a}
\]

Both norms are public because their squared coordinate formulas do not depend on
the signs.  Given coherent preparations of their normalized states, the standard
two-term linear-combination construction prepares their normalized sum with
success probability

\[
 \frac{\|p_\sigma\|^2+\|Wz\|^2}
 {(\|p_\sigma\|+\|Wz\|)^2}\ge\frac12.                    \tag{16b}
\]

Thus, once the affine-correction state is available, applying \(W\) and combining
the two orthogonal pieces costs only a constant access-normalization factor.  No
asymptotic recovery loss is needed to explain the lower bound.

## 4. The canonical affine correction is linearly hard

Let \(S\) be the \(K=16N\) output plateau nodes, where \(\tau_i=p_N\).  Define
the fixed norm-one diagonal observable

\[
 O_S=\sum_{i\in S}
 (|u_i\rangle\langle u_i|-|v_i\rangle\langle v_i|).       \tag{17}
\]

From (10), on every output node

\[
 u_i^2-v_i^2=(u_i-v_i)(u_i+v_i)
 =-\frac4{27}p_NH^2.                                     \tag{18}
\]

The squared free-node norm is

\[
 C_pH^2,qquad C_p=\frac{851}{1458},                      \tag{19}
\]

while a prefix node, where \(p_\sigma=\Delta x\), has squared norm

\[
 DH_i^2,qquad D=\frac{16139}{23328}<\frac7{10}.          \tag{20}
\]

Since \(C_p<D\) and the height sum obeys

\[
 \sum_iH_i^2<\frac{53}{3}NH^2,
\]

we obtain

\[
 \left|\left\langle
 \frac{p_\sigma}{\|p_\sigma\|},O_S
 \frac{p_\sigma}{\|p_\sigma\|}
 \right\rangle\right|
 >\frac{(64/27)NH^2}{(7/10)(53/3)NH^2}
 =\frac{1920}{10017}>\frac16.                             \tag{21}
\]

Its sign is \(-p_N\).  A state within trace distance \(1/100\) changes the
expectation by at most \(1/50\), leaving constant sign bias.  A fixed number of
measurements therefore computes parity.

Every coherent raw sparse LP query is simulated by at most one hidden-sign query,
while all public data and reduced-solve oracles above require none.  Quantum
parity has bounded-error query complexity \(\Omega(N)\).  Hence:

**Theorem 1 (canonical affine-correction lower bound).**  Even when an algorithm
is granted free exact oracles for \(W,M,M^{-1},g,z,Wz\), the public start, and all
reduced central-path data, preparing a density operator within trace distance
\(1/100\) of

\[
 \left|(A'_\sigma)^\dagger
 (b'-A'_\sigma x^0)\right\rangle
\]

(with the ket denoting normalization) requires
\(\Omega(N)=\Omega(P)\) raw coefficient queries.

The same free grants do not weaken the existing \(\Omega(P)\) lower bound for the
full normalized Newton direction \(|\Delta x/\|\Delta x\|\rangle\), because every
granted channel is input-independent.  Conversely, querying all \(N\) signs,
forming their prefixes, and loading (10) takes \(O(N)=O(P)\) raw queries.  The
canonical affine-correction query complexity is therefore \(\Theta(P)\).

## 5. Pipeline consequence and scope

For the canonical orthogonal decomposition (1), the reduced solve has zero raw
query cost and unit access-normalized inverse factor, while construction of the
particular correction has tight cost \(\Theta(P)\).  Any constant-stage pipeline
that implements this decomposition and outputs the original-primal direction
must therefore pay \(\Omega(P)\) in its particular-correction/loading stage if
all reduced operations are free.

For an arbitrary decomposition, kernel components can be shifted between the
chosen particular solution and the reduced vector.  It is therefore not
representation-invariant to say that every possible ``particular solution'' is
individually hard.  The representation-invariant statement is the original
end-to-end theorem: after granting every input-independent reduced operation for
free, the total remaining coefficient-query cost is \(\Omega(P)\).  The
Moore--Penrose gauge strengthens this by providing one canonical decomposition in
which the hard stage is identified exactly.

The theorem counts local sparse coefficient queries.  It excludes free
input-dependent advice, a free oracle for \((A'_\sigma)^\dagger r_p\), a free
original-coordinate loading map, or a batch oracle that aggregates the hidden
signs.  It is not a lower bound in the condition number of a supplied QLS, and it
does not assert that the full equality-normal or KKT matrix is well conditioned.
The dynamic range remains \(H=\Theta(\sqrt P)\).

The result is best stated as a **tight access-normalized affine-correction oracle
separation**: a scalar reduced inverse problem can have unit normalized solve
factor and zero raw-query complexity while its canonical original-coordinate
feasibility correction has \(\Theta(P)\) raw-query complexity.
