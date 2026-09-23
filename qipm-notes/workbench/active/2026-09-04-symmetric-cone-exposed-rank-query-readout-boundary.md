# Same-instance query/readout bounds at the symmetric-cone exposed-rank frontier

Status: Candidate theorem; independently hostile-audited
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the derivation; Albert encoding is explicitly real-coordinate,
not an octonionic quantum-state model

## Main conclusion

Fix a repeatable dictionary of simple Euclidean Jordan algebras (EJAs), let
\[
 B=\max_i a_i(r_i-1)>0,
\]
and choose one factor \(V\) attaining \(B\).  Here \(r\) is its rank and
\(a\) its Peirce constant.  In the divisible case
\[
                   s=qB+1,\qquad q\ge2,\qquad n=s-1=qB,       \tag{1}
\]
the \(q\)-block Peirce-perspective lift has a balanced hidden-sign family of
ball-support objectives for which, on every hidden instance:

1. the minimum total Jordan rank of a normalized exposing certificate is
   exactly \(q\);
2. a public Slater reference has exact support-minor scale \(\Delta=1\), so
   for \(0<\epsilon<1\), every forward \(\theta\)-Dikin sequence from it
   to objective gap \(\epsilon\) needs at least
   \[
             {\sqrt q\log(1/\epsilon)\over-\log(1-\theta)}    \tag{2}
   \]
   chords in the restricted standard Jordan-logdet metric;
3. the normalized projected optimizer state, and real-coordinate amplitude
   states of the structured lifted optimizer and standard-barrier central
   checkpoints, require one clean sign query, conditional on charged exact
   preparation of their public magnitude states; and
4. for every fixed \(0<\epsilon<1/8\), an explicit classical feasible
   projected or lifted \(\epsilon\)-optimal solution with worst-case success
   at least \(2/3\) costs
   \(\Theta_\epsilon(n)=\Theta_\epsilon(qB)\) quantum or randomized raw
   sign queries.

The scalar optimum and all norms are public.  The movement, state, and
readout statements hold simultaneously but are not multiplied.

If \(r_{\mathcal L}(v)\) denotes minimum certificate rank for support \(v\),
there is again an exact formulation obstruction:
\[
 \boxed{\displaystyle
   \inf_{\mathcal L}\sup_v r_{\mathcal L}(v)=q,
   \qquad
   \sup_v\inf_{\mathcal L}r_{\mathcal L}(v)=1.}              \tag{3}
\]
The first equality is the audited all-simple-EJA selection-free theorem.
For the second, an objective-dependent orthogonal change of the projection
sends the chosen support to the north pole, where one top primitive
idempotent is a rank-one certificate.  Exposed-rank geometry therefore
cannot give a formulation-independent raw-query lower bound unless learning
and implementing the reformulation is charged.

## 1. Balanced signs in full half-Peirce groups

Fix a primitive idempotent \(c\in V\), put \(d=e-c\), and use the trace inner
product.  The real half-Peirce space \(V(c,1/2)\) has dimension
\[
                         \dim_{\mathbb R}V(c,1/2)=a(r-1)=B.  \tag{4}
\]
Choose a public real orthonormal basis in each of \(q\) copies.  For
\(\sigma\in\{-1,1\}^n\), define
\[
 g_\sigma={1\over\sqrt n}(\sigma_1,\ldots,\sigma_n)
            =(g_{\sigma,1},\ldots,g_{\sigma,q}),
 \qquad v_\sigma=(g_\sigma,0).                              \tag{5}
\]
Every full group has
\[
                     \|g_{\sigma,G}\|_c^2={B\over n}={1\over q}. \tag{6}
\]
Thus \(v_\sigma\) is a unit ball support, its support optimum is one, and
its unique projected optimizer is \(x_\sigma^*=v_\sigma\).

Use the Peirce-perspective lift
\[
 X_G=(1-b)c+\sqrt2\,w_G+z_Gd\succeq0,
 \qquad \sum_{G=1}^qz_G=1+b.                                \tag{7}
\]
The rank-two Peirce identity gives
\[
 X_G\succeq0
 \iff 1-b\ge0,\ z_G\ge0,\ (1-b)z_G\ge\|w_G\|_c^2,           \tag{8}
\]
so (7) projects exactly onto \(B_2^s\).  At the unique projected optimizer,
equality and (6) force the unique structured lift
\[
                   b=0,\qquad z_G={1\over q},\qquad
                   w_G=g_{\sigma,G}.                        \tag{9}
\]

## 2. Exact certificate rank and exact scale

For every group put
\[
 A={1\over2q},\qquad
 Y_G=Ac-{g_{\sigma,G}\over\sqrt2}+H_G,
 \qquad
 H_G={1\over2A}P(g_{\sigma,G})c.                            \tag{10}
\]
The universal rank-one completion identity
\[
 A P\!\left(c-{g_{\sigma,G}\over\sqrt2A}\right)c
   =Ac-{g_{\sigma,G}\over\sqrt2}
        +{1\over2A}P(g_{\sigma,G})c                         \tag{11}
\]
shows that \(Y_G\succeq0\) has Jordan rank one.  Moreover,
\[
 \operatorname{tr}H_G={\|g_{\sigma,G}\|_c^2\over4A}
                     ={1\over2},
\]
and direct affine pairing gives the genuine normalized slack identity
\[
                  \sum_G\langle X_G,Y_G\rangle
                       =1-g_\sigma^Tw.                      \tag{12}
\]
Every half-Peirce coefficient in (10) is nonzero groupwise.  Any positive
certificate matching it must therefore have a nonzero block in every group.
Hence the minimum total Jordan rank is exactly
\[
                         Q=\sum_G\operatorname{rank}_JY_G=q. \tag{13}
\]

Take the public Slater reference
\[
                         X_G^c=c+q^{-1}d.                    \tag{14}
\]
Since a primitive idempotent has trace one, the sole positive eigenvalue of
\(Y_G\) is
\[
                         \lambda_Y=\operatorname{tr}Y_G
                                  ={q+1\over2q}.             \tag{15}
\]
Let \(u_G=Y_G/\lambda_Y\) be its primitive support idempotent.  The
\(c\)-coefficient in (10) yields
\[
 \langle c,u_G\rangle={A\over\lambda_Y}={1\over q+1},
 \qquad
 \langle d,u_G\rangle={q\over q+1}.                         \tag{16}
\]
The rank-one compression of the reference is therefore
\[
 P(u_G)X_G^c=\lambda_Xu_G,\qquad
 \lambda_X=\langle u_G,X_G^c\rangle={2\over q+1}.            \tag{17}
\]
Thus \(\lambda_Y\lambda_X=1/q\) in every block, for every hidden string and
every simple EJA type.  The exposed-minor scale is exactly
\[
 \Delta
   =Q\left[\prod_{G=1}^q
       \det_{u_G}(Y_G)\det_{u_G}(P(u_G)X_G^c)\right]^{1/Q}
   =q[(1/q)^q]^{1/q}=1.                                    \tag{18}
\]
The support-minor theorem gives
\[
 d_F\!\left(X^c,\{X:1-v_\sigma^T\pi X\le\epsilon\}\right)
       \ge\sqrt q\log(1/\epsilon),\qquad0<\epsilon<1.        \tag{19}
\]
A forward \(\theta\)-Dikin chord has metric length at most
\(-\log(1-\theta)\), proving (2).

## 3. Exact oracle and state contracts

Use the clean index oracle
\[
 O_\sigma|j,z\rangle=|j,z\oplus b_j\rangle,\qquad
 \sigma_j=(-1)^{b_j}.                                      \tag{20}
\]
The coefficient oracle for (5), with exact values or additive error below
\(1/(2\sqrt n)\), is equivalent up to constant query overhead.  Public data
include the EJA type, its multiplication table or other chosen classical
representation, \(c,d\), the half-Peirce bases, index routing, the lift,
all common magnitudes, and the reference.  A full classical output means an
explicit real-coordinate list, not a succinct circuit, state-preparation
oracle, or sample/query data structure.

One phase-kickback query prepares
\[
                       |x_\sigma^*\rangle
          ={1\over\sqrt n}\sum_{j=1}^n\sigma_j|j\rangle.     \tag{21}
\]
Equation (9) shows that the structured lifted optimizer has public
\(c,d,z\) coordinates and hidden signs only in its half-Peirce coordinates.
For each standard-barrier central multiplier, direct stationarity of
\[
 -\log\det X_G
 =-(r-2)\log z_G-\log((1-b)z_G-\|w_G\|^2)
\]
in the half-Peirce variables forces
\[
                w_G=t\,g_{\sigma,G},\qquad b,z_G
                \ \hbox{public and group-independent},      \tag{22}
\]
for a public scalar \(t\).  Hence a public magnitude-state preparation,
followed by one coherently controlled sign query on the half-Peirce slots,
prepares the real-coordinate amplitude state of either structured object.
Each copy, public amplitude-table construction, index routing, EJA
arithmetic, and numerical precision remains a separate cost.

The stationarity equation is field-independent and gives
\(w_G=t_Gg_{\sigma,G}\) with a real scalar \(t_G\).  Block permutations,
together with equal group norms and uniqueness, force the common scalar
and common \(z_G\).  Equivalently, this is consistent with transitivity of
the compact automorphism stabilizer of \(c\) on the unit sphere of
\(V(c,1/2)\): the usual orthogonal, unitary, or compact symplectic action
in the three matrix series, the ordinary orthogonal action for spin
factors, and the \(\operatorname{Spin}(9)\) spin action on \(S^{15}\) for
the Albert algebra.  These automorphisms are used only as structural
symmetries and are not assumed to have efficient quantum implementations.

This statement uses ordinary complex quantum amplitudes to encode a public
real coordinate vector.  For a spin factor, these are its \(m+2\) real EJA
coordinates.  For the Albert algebra, these are its \(27\) real coordinates,
with each hidden group occupying the \(16\)-dimensional real half-Peirce
space.  No octonion is treated as a quantum amplitude, and no efficient
quantum circuit for a general Albert automorphism or Jordan product is
assumed.  The one-query statement concerns only applying the diagonal hidden
sign pattern after the public magnitude state and routing are supplied.

## 4. Constant-accuracy full-output lower bound

Any feasible projected point of support gap at most \(\epsilon\) obeys
\[
                  \|x-v_\sigma\|_2^2
                    \le2(1-v_\sigma^Tx)\le2\epsilon.         \tag{23}
\]
Sign decoding therefore makes at most \(2\epsilon n\) Hamming errors on a
successful explicit output.

After \(T\) clean bit queries, purification and deferred measurement give
the Fourier expansion
\[
 |\psi_\sigma\rangle
   =\sum_{\substack{S\subseteq[n]\\|S|\le T}}
        \left(\prod_{j\in S}\sigma_j\right)|a_S\rangle.      \tag{24}
\]
The final ensemble lies in a subspace of dimension at most
\(D_T=\sum_{j=0}^T\binom nj\).  Holevo's bound limits the information in
every classical output to \(\log_2D_T\).  Under uniform hidden signs and
worst-case success at least \(2/3\), the average decoded distortion is at
most
\[
                         d_\epsilon={1+4\epsilon\over3}.     \tag{25}
\]
For \(0<\epsilon<1/8\), binary rate distortion and the binomial entropy
bound imply
\[
 n[1-H_2(d_\epsilon)]
   \le I(\sigma;\widehat\sigma)
   \le\log_2D_T
   \le nH_2(T/n),                                           \tag{26}
\]
when \(T\le n/2\).  Therefore
\[
 T\ge nH_2^{-1}\!\left(1-H_2(d_\epsilon)\right)
        =\Omega_\epsilon(n),                                \tag{27}
\]
with the inverse on \([0,1/2]\); \(T>n/2\) is already linear.  Reading all
signs gives \(O(n)\), proving \(\Theta_\epsilon(n)\) for quantum algorithms
and hence randomized algorithms.  An explicit feasible lifted solution has
the same lower bound because the public projection gives a projected point
with the same gap.  Arbitrary approximate-value oracles require a separate
reduction.

For completeness, if \(\epsilon<1/(8n)\), (23) forces coordinate error below
\(1/(2\sqrt n)\), so every sign and parity are recovered.  This sharper
pointwise corollary is not needed for the constant-accuracy result.

## 5. Formulation-dependent support and compilation

For admissible lifts through the fixed dictionary, the selection-free
theorem gives
\[
                   \inf_{\mathcal L}\sup_v r_{\mathcal L}(v)=q. \tag{28}
\]
Fix a support \(v_0\), choose a public orthogonal ball map \(U\) with
\(Uv_0=e_b\), and replace the projection by
\(\pi_U=U^{-1}\circ\pi\).  The support \(v_0\) now pulls back to the north
pole.  There the certificate conditions have zero half-Peirce and tail
parts; putting unit top mass on \(c\) in one block gives rank one.  Rank zero
cannot normalize a nonzero support slack, so
\[
                    \inf_{\mathcal L}r_{\mathcal L}(v_0)=1. \tag{29}
\]
This proves (3).

For the balanced signs, let
\(u=(n^{-1/2}(1,\ldots,1),0)\), let \(D_\sigma\oplus1\) be the
real-coordinate sign operator, and choose a fixed public orthogonal \(U_0\)
with \(U_0u=e_b\).  Then
\[
            U_\sigma=U_0(D_\sigma\oplus1),\qquad
            U_\sigma v_\sigma=e_b.                          \tag{30}
\]
One coherent use of \(U_\sigma\) costs one sign query plus the public
\(U_0\).  In contrast, an explicit classical description of \(U_\sigma\),
exactly or within operator norm below \(1/2\), reveals every sign through
\(U_0^TU_\sigma\) and costs \(\Theta(n)\) raw queries.  Coherent use and
explicit compilation are different resources.  The gate/arithmetic cost of
the generally dense public \(U_0\) is not included in this query count.
Geometry alone supplies no uniform oracle-compilation lower bound.

## 6. QIPM and novelty boundary

- This is a same-instance conjunction for one fixed Peirce-perspective lift:
  uniform rank \(q\), exact \(\Delta=1\), easy normalized state preparation,
  and hard explicit classical output.
- The movement theorem is restricted to the fixed standard Jordan-logdet
  barrier, the public reference (or a uniformly bounded metric
  perturbation), feasible paths, and bounded forward Dikin chords.  It is
  not an arbitrary-barrier, arbitrary-start, infeasible-trajectory, or
  unrestricted QIPM runtime lower bound.
- Movement and query/readout costs imply separate lower bounds or their
  maximum under a joint contract.  They are never multiplied.
- The state claim is an amplitude-encoding statement, not a claim that
  Jordan multiplication, central-parameter computation, or general EJA
  automorphisms are efficient quantum primitives.
- The certificate, Peirce perspective, phase-kickback, Holevo, and
  rate-distortion ingredients are standard separately.  The candidate
  contribution is their exact same-instance synthesis with the
  all-simple-EJA selection-free frontier and the field-independent
  calculation \(\Delta=1\).  A targeted surrounding-project screen did not
  locate this conjunction, but this is not an exhaustive priority claim.

## Audit checklist

1. Recheck (10)--(18) in every simple EJA normalization, especially
   \(\operatorname{tr}H_G=1/2\), the primitive support masses, and
   \(\Delta=1\).
2. Verify groupwise nonzero half-Peirce coefficients force exact minimum
   total rank \(q\).
3. Check the central-state symmetry claim for real, complex, quaternionic,
   spin, and Albert factors, and keep the state representation purely
   real-coordinate.
4. Recheck the constant-accuracy low-degree/Holevo/rate-distortion proof and
   explicit-output contract.
5. Verify the north-pole rank-one certificate and both quantifier orders.
6. Preserve fixed-standard-barrier scope and MAX-not-product language.

## Closure audit

The EJA normalization was checked directly.  Equation (11) makes every
\(Y_G\) rank one, and
\(\operatorname{tr}H_G=\|g_G\|^2/(4A)=1/2\).  Therefore its positive
eigenvalue is \((q+1)/(2q)\).  The primitive support has \(c\)- and
\(d\)-masses \(1/(q+1)\) and \(q/(q+1)\); pairing it with
\(X_G^c=c+q^{-1}d\) gives \(2/(q+1)\).  Their product is \(1/q\) in all
\(q\) blocks, so (18) indeed gives \(Q=q\) and \(\Delta=1\), independently
of EJA type.  Nonzero half-Peirce coefficients force every positive
certificate block to be nonzero, proving the matching minimum rank.

The central-state form follows directly from determinant stationarity in
the half-Peirce variables, with block symmetry fixing the public common
scalars.  The result is consistent with the classical, spin-factor, and
Albert stabilizer actions.  The encoded state is always an ordinary complex
quantum state whose amplitudes list **real coordinates**; no octonionic
amplitude or efficient Albert arithmetic is assumed.

For explicit output, feasibility gives
\(\|x-v_\sigma\|^2\le2\epsilon\), hence at most
\(2\epsilon n\) sign errors on a successful run.  Including failure
probability \(1/3\) gives average distortion
\((1+4\epsilon)/3<1/2\).  A \(T\)-query clean-bit algorithm has Fourier
degree at most \(T\), so its purified ensemble lies in a space of dimension
\(\sum_{j\le T}\binom nj\).  Holevo information, binary rate distortion,
and the binomial entropy bound therefore prove (26)--(27).  Public
projection transfers the lower bound from lifted to projected explicit
output.

Finally, an objective-dependent orthogonal change of projection sends any
fixed support to the rank-one north pole, establishing the second quantifier
order in (3); coherent use of the balanced-sign rotation costs one sign
query, whereas explicitly outputting it reveals all signs.  The closure
check found no mathematical correction.  A subsequent independent hostile
audit rechecked the EJA normalization, including Albert, the exact rank and
\(\Delta=1\), the movement conversion, the one-query state contract, the
Fourier--Holevo--rate-distortion output lower bound, and both formulation
quantifiers.  It returned **PASS** after replacing the potentially
ambiguous complex-isotropy sentence by the direct determinant-stationarity
argument above.  The MAX-not-product, fixed-formulation,
fixed-standard-barrier, and explicit-output restrictions remain essential.
