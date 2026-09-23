# Same-instance query/readout bounds at the Hermitian exposed-rank frontier

Status: Candidate theorem; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the internal derivation in the fixed-lift,
fixed-reference model; literature novelty and unrestricted-QIPM transfer remain
separate questions

## Main conclusion

Fix \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), put
\(a=\dim_{\mathbb R}\mathbb F\), fix a Hermitian PSD order cap \(R\ge2\),
and take the divisible ball dimension
\[
             s=qB+1,\qquad B=a(R-1),\qquad q\ge2.             \tag{1}
\]
For the rotated Hermitian perspective lift with \(q\) order-\(R\) blocks,
there is a balanced hidden-sign family of support objectives such that,
on every member of the family:

1. the minimum exposing-certificate rank is exactly \(q\), and a public
   Slater reference has the exact exposed-minor scale \(\Delta=1\);
2. every forward \(\theta\)-Dikin sequence from that reference to objective
   gap \(\epsilon\) needs
   \[
          {\sqrt q\log(1/\epsilon)\over-\log(1-\theta)}       \tag{2}
   \]
   chords in the fixed restricted standard-logdet metric;
3. a normalized projected optimizer state, and normalized states of the
   symmetry-reduced lifted optimizer or central checkpoints, take one clean
   sign-oracle query from charged public amplitude states; but
4. for every fixed \(0<\epsilon<1/8\), a full classical
   \(\epsilon\)-optimal projected solution, or an explicit lifted solution,
   with success probability at least \(2/3\) costs
   \(\Theta_\epsilon(s-1)=\Theta_\epsilon(qB)\) quantum or randomized raw
   sign queries.

These are simultaneous movement/state/readout statements, not a product.
The scalar optimum is public.

There is also an exact obstruction to a formulation-independent hard
support.  If \(r_{\mathcal L}(v)\) is the minimum total rank of a normalized
certificate for support \(v\), then over all admissible capped Hermitian
lifts
\[
 \boxed{
  \inf_{\mathcal L}\sup_v r_{\mathcal L}(v)=q,
  \qquad
  \sup_v\inf_{\mathcal L}r_{\mathcal L}(v)=1.}               \tag{3}
\]
The first identity is the audited selection-free minimax theorem.  For the
second, rotate the projection of a perspective lift so that the chosen
support becomes its north pole, which has a rank-one certificate.  Thus the
hard support may depend on the formulation.  A geometry-only minimax cannot
give one fixed coefficient-oracle adversary against objective-dependent
formulations unless the cost of learning the objective and compiling the
rotation is charged.

## 1. Fixed perspective lift and balanced supports

Write a ball point as \(x=(w,b)\), with
\(w=(w_G)_{G=1}^q\in(\mathbb F^{R-1})^q\).  Put \(\delta=1-b\) and use
\[
 X_G=\begin{pmatrix}
       \delta&w_G^*\\ w_G&z_GI_{R-1}
     \end{pmatrix}\succeq0,
 \qquad \sum_{G=1}^qz_G=1+b.                                 \tag{4}
\]
This is an exact full-Slater lift of \(B_2^s\).  The fixed standard barrier
is \(F(X)=-\sum_G\log\det_{\mathbb F}X_G\).

Let \(n=s-1=qB\), choose a public real orthonormal coordinate basis for
\((\mathbb F^{R-1})^q\), and let
\[
 c_\sigma={1\over\sqrt n}(\sigma_1,\ldots,\sigma_n),
 \qquad \sigma_j\in\{-1,1\},
 \qquad v_\sigma=(c_\sigma,0).                               \tag{5}
\]
Here (5) specifies real coordinates; within each field block it gives
\(\|c_{\sigma,G}\|^2=1/q\).  Hence \(v_\sigma\in S^{s-1}\), every group is
nonzero, the support optimum over the projected ball is one, and its unique
projected optimizer is \(x_\sigma^*=v_\sigma\).

## 2. Exact rank and the uniform scale \(\Delta=1\)

At \(v=(c,0)\), the normalized dual certificate in every group is
\[
 S_G=\begin{pmatrix}
       \alpha&-c_G^*/2\\ -c_G/2&Z_G
     \end{pmatrix},qquad
 \alpha={1\over2q},qquad
 Z_G={q\over2}c_Gc_G^*.                                      \tag{6}
\]
It is positive semidefinite of \(\mathbb F\)-rank one,
\(\operatorname{tr}_{\mathbb F}Z_G=1/2\), and coefficient matching gives
\[
                  \sum_G\langle X_G,S_G\rangle=1-v^Tx.       \tag{7}
\]
Because every \(c_G\ne0\), positivity and the fixed off-diagonal coefficient
force every certificate block to be nonzero.  Thus the minimum total rank
is exactly
\[
                            Q=\sum_G\operatorname{rank}S_G=q. \tag{8}
\]

Choose the public Slater reference
\[
X_G^c=\operatorname{Diag}(1,q^{-1}I_{R-1})
                    \qquad(G=1,\ldots,q),                    \tag{9}
\]
corresponding to \(b=0,w=0,z_G=1/q\).  The sole positive eigenvalue of
\(S_G\) is
\[
             \lambda_S=\alpha+\operatorname{tr}Z_G
                       ={q+1\over2q}.                         \tag{10}
\]
Its unit range vector has squared top-component norm \(1/(q+1)\) and
bottom-component norm \(q/(q+1)\).  Therefore the rank-one compression of
\(X_G^c\) has eigenvalue
\[
             \lambda_X={1\over q+1}+{q\over q+1}{1\over q}
                       ={2\over q+1}.                         \tag{11}
\]
The support-principal-minor scale is consequently independent of every
hidden sign and of the field:
\[
 \Delta=Q\left[\prod_{G=1}^q\lambda_S\lambda_X\right]^{1/Q}
       =q\left[(1/q)^q\right]^{1/q}=1.                       \tag{12}
\]
The exposed-rank distance theorem now gives
\[
 d_F\!\left(X^c,\{X:1-v_\sigma^T\pi X\le\epsilon\}\right)
                     \ge\sqrt q\log(1/\epsilon),             \tag{13}
\]
for \(0<\epsilon<1\).  Each forward \(\theta\)-Dikin chord has metric
length at most \(-\log(1-\theta)\), proving (2).  The metric, lift,
reference, accuracy scale, and coefficient are the same for every hidden
string.

## 3. Oracle and output hierarchy

Use the clean bit oracle and real-coordinate amplitude encoding throughout
this section:
\[
             O_\sigma|j,z\rangle=|j,z\oplus b_j\rangle,
             \qquad \sigma_j=(-1)^{b_j}.                     \tag{14}
\]
A coefficient oracle for (5), with exact values or error below
\(1/(2\sqrt n)\), is equivalent up to constant query overhead.  Public
metadata include \(n,q,R,\mathbb F\), the common coefficient magnitude,
all norms, the lift, and the reference point.  A full classical projected
output means an explicit numerical list of all \(n+1\) coordinates; a
succinct circuit, state-preparation oracle, or sample/query data structure
is a different output contract.

Preparing the uniform state and applying one phase-kickback query gives the
normalized projected optimizer state
\[
                         |x_\sigma^*\rangle
             ={1\over\sqrt n}\sum_{j=1}^n\sigma_j|j\rangle.  \tag{15}
\]
The structured lifted optimizer has
\(b=0,z_G=1/q,w_G=c_{\sigma,G}\); only its off-diagonal real coordinates
depend on \(\sigma\).  Likewise, strict convexity, radial first-order
optimality, and the block-unitary and group symmetries force every
standard-barrier central checkpoint for objective \(v_\sigma\) to have public
scalar coordinates and \(w_G=t c_{\sigma,G}\) for a public real scalar \(t\).
Thus, assuming charged
exact preparation of the corresponding public magnitude state, one clean
phase query prepares the normalized projected or full structured state.
The amplitude-table construction, arithmetic precision, and every state
copy remain separate costs.

By contrast, a classical projected vector \(\widetilde x\) obeying
\[
              \max_{1\le j\le n}
              |\widetilde x_j-\sigma_j/\sqrt n|
                         <{1\over2\sqrt n}                    \tag{16}
\]
reveals every hidden bit.  Its bounded-error quantum and randomized query
complexities are \(\Theta(n)\): read-all is an upper bound, and a successful
output computes parity, which has linear query complexity.  The same lower
bound applies to a lifted optimizer output accurate enough to recover its
top--bottom entries.  The scalar optimum \(1\), all coefficient norms, and
the exposed-rank scale are public, so no scalar-output lower bound exists.

An arbitrary feasible \(\epsilon\)-accurate projected point also satisfies
\[
     \|x-v_\sigma\|_2^2
       \le2(1-v_\sigma^Tx)\le2\epsilon.                       \tag{17}
\]
Decode a classical output coordinatewise, breaking zero ties arbitrarily.
Each incorrectly decoded sign contributes at least \(1/n\) to the squared
distance in (17), so a successful output has Hamming error at most
\(2\epsilon n\).

Here is a self-contained quantum lower bound that avoids demanding recovery
of every sign.  After \(T\) clean bit queries, a purified algorithm's final
states have an expansion
\[
       |\psi_\sigma\rangle
          =\sum_{\substack{S\subseteq[n]\\|S|\le T}}
                    \left(\prod_{j\in S}\sigma_j\right)|a_S\rangle.
                                                                    \tag{17a}
\]
Thus their span has dimension at most
\(D_T=\sum_{j=0}^T\binom nj\), and Holevo's bound limits the mutual
information in any classical output to \(\log_2D_T\).  For uniform hidden
signs, an algorithm that succeeds with probability at least \(2/3\) has
average decoded relative Hamming distortion at most
\[
                    d_\epsilon={1+4\epsilon\over3}.            \tag{17b}
\]
Binary rate distortion gives
\[
 n[1-H_2(d_\epsilon)]
     \le I(\sigma;\widehat\sigma)
     \le\log_2D_T
     \le nH_2(T/n)                                             \tag{17c}
\]
when \(T\le n/2\).  Consequently, for \(0<\epsilon<1/8\),
\[
 T\ge n\,H_2^{-1}\!\left(1-H_2(d_\epsilon)\right)
       =\Omega_\epsilon(n),                                   \tag{17d}
\]
where the inverse is on \([0,1/2]\); if \(T>n/2\), the same displayed
lower bound is automatic.  Reading all signs gives \(O(n)\), proving the
constant-accuracy \(\Theta_\epsilon(n)\) claim for quantum algorithms and,
a fortiori, randomized algorithms.
The same bound holds for an explicit feasible lifted output because the
public projection produces a feasible projected point with the same gap.

The stronger pointwise threshold remains useful: when
\(\epsilon<1/(8n)\), (17) implies
\(\|x-v_\sigma\|_2<1/(2\sqrt n)\), hence (16), so every sign and parity are
recovered.  The numerical encoding must represent the claimed feasible
point and accuracy.  A normalized quantum state is not a full classical
output.

## 4. Why the support cannot be uniform over formulations

For an admissible lift \(\mathcal L\), define
\[
 r_{\mathcal L}(v)=\min_{S\in\mathcal D_{\mathcal L}(v)}
                         \sum_i\operatorname{rank}_{\mathbb F}S_i. \tag{18}
\]
The selection-free theorem states
\[
            \inf_{\mathcal L}\sup_{v\in S^{s-1}}
                    r_{\mathcal L}(v)=q.                     \tag{19}
\]

Fix any particular support \(v_0\).  Choose an orthogonal ball automorphism
\(U\) with \(Uv_0=e_b\), replace the projection by
\(\pi_U=U^{-1}\!\circ\pi\), and leave all cone blocks and their order cap
unchanged.  Then support \(v_0\) in the rotated formulation pulls back to the
north-pole support \(e_b\).  For that support, the coefficient-matching
conditions specialize to lower blocks \(Z_G=0\)
and nonnegative scalars \(\alpha_G\) summing to one.  Taking one
\(\alpha_G=1\) and all others zero gives a normalized certificate of total
rank one.  No normalized nonzero slack has rank zero, so
\[
                    \inf_{\mathcal L}r_{\mathcal L}(v_0)=1.  \tag{20}
\]
Since \(v_0\) was arbitrary, (19)--(20) prove (3).

This quantifier gap has a concrete oracle meaning.  If a formulation must
be fixed before the hidden objective is queried, the fixed-lift family
(5) supplies the same-instance theorem (2), (15), and (16).  If the
formulation may instead depend on the complete objective at no cost, it can
rotate that objective to the easy north pole, and the exposed-rank argument
cannot identify one universal hard coefficient string.  The cost of
constructing or applying the dense objective-dependent rotation depends on
whether its output is classical or coherent; either cost is absent from the
geometric minimax.  Geometry alone does not determine an oracle-compilation
lower bound.

For the balanced sign family, the distinction is exact.  Embed
\(u=(n^{-1/2}(1,\ldots,1),0)\) in \(\mathbb R^s\), let
\(D_\sigma\oplus1\) be the sign operator fixing the last coordinate, and
choose a fixed public orthogonal \(U_0\) with \(U_0u=e_b\).  Then
\[
                       U_\sigma=U_0(D_\sigma\oplus1),
       \qquad U_\sigma v_\sigma=e_b.                         \tag{21}
\]
A coherent application of \(U_\sigma\) costs one clean phase-oracle query,
plus the public \(U_0\).  Thus an implicit quantum formulation oracle can
rotate the hard support to the rank-one north pole with constant raw-query
overhead per use; exposed rank cannot imply an \(\Omega(\sqrt q)\) raw-query
lower bound for state or scalar output.  In contrast, an explicit classical
description of \(U_\sigma\) reveals
\(D_\sigma\oplus1=U_0^TU_\sigma\), hence all \(n\) signs.  An exact
description, or one accurate to operator norm below \(1/2\), therefore costs
\(\Theta(n)\) raw queries under a full-description contract.  Repeated
coherent uses and one-time explicit compilation are different resources.

## 5. QIPM interpretation

- The fixed-lift result is a genuine same-instance conjunction: every
  hidden-sign instance has exposed rank \(q\), uniform \(\Delta=1\), easy
  normalized state output, and hard full classical output.
- It remains a fixed restricted-standard-barrier, feasible bounded-movement
  theorem from the displayed public Slater reference.  A start within
  uniformly bounded metric distance changes the lower bound only by the
  corresponding additive distance.  It is not an arbitrary-start,
  arbitrary-barrier, or unrestricted QIPM runtime lower bound.
- The movement lower and full-output query lower are simultaneous resources.
  They imply separate lower bounds, or their maximum under a joint contract;
  no product is asserted.
- Objective-dependent reformulation is precisely where a uniform query
  claim fails.  Any theorem allowing it must charge the queries, arithmetic,
  and data structure used to learn and implement the rotation.
- Equation (21) shows that even the rotation-compilation cost is
  output-model dependent: one query per coherent use versus \(\Theta(n)\)
  queries for an explicit classical matrix.  No generic compilation lower
  can ignore this distinction.
- In a combined logarithmically homogeneous primal--dual metric,
  Nesterov--Todd's \(\sqrt2\)-geodesicity again prevents a
  dimension-growing same-endpoint centrality tax.  The present movement
  theorem is restricted-primal.

## 6. Literature boundary

Gouveia--Parrilo--Thomas provide the general
[cone-lift/slack-factorization correspondence](https://arxiv.org/abs/1111.3164);
they do not study this objective-wise certificate-rank query model.
Beals--Buhrman--Cleve--Mosca--de Wolf give the standard
[quantum parity lower bound](https://arxiv.org/abs/quant-ph/9802049) used
for the exact all-sign corollary.  Van Dam's
[quantum oracle interrogation](https://arxiv.org/abs/quant-ph/9805006)
studies the corresponding approximate-recovery task.  Its fixed-distortion
examples use linear-in-\(n\) query counts with improved quantum constants;
the necessity of linear scaling here follows from (17a)--(17d), not from
that comparison alone.  Kerenidis--Prakash and
Augustino--Nannicini--Terlaky--Zuluaga give QIPM upper bounds for
[LPs and SDPs](https://arxiv.org/abs/1808.09266) and
[semidefinite optimization](https://arxiv.org/abs/2112.06025),
respectively; their output and access models do not state this exposed-rank
same-instance hierarchy or the formulation quantifier swap.

The certificate/Schur lift, phase-kickback preparation, low-degree query
expansion, Holevo/rate-distortion bounds, and parity reduction are standard
ingredients.  The candidate contribution is their exact
combination with the audited Hermitian exposed-rank minimax and the uniform
\(\Delta=1\) calculation.  A targeted primary-source screen did not find
this conjunction, but it was not an exhaustive priority determination.

## Audit checklist

1. Verify the real/complex/quaternionic trace and rank-one normalization in
   (6)--(12), especially \(\Delta=1\).
2. Check that every balanced support has minimum total certificate rank
   exactly \(q\).
3. Check which lifted central/checkpoint states are one-query preparable and
   keep public amplitude preparation charged.
4. Verify the low-degree span/rate-distortion full-output reduction, its
   \(d_\epsilon=(1+4\epsilon)/3\) constant, the all-sign corollary, and
   coefficient precision.
5. Verify the rotated north-pole rank-one certificate and both quantifier
   orders in (3).
6. Do not convert formulation-dependent support existence into a uniform
   raw-oracle lower bound or multiply movement by readout queries.

## Independent hostile audit record (2026-09-04)

The field-uniform certificate calculation was checked directly.  In each
group, (6) is rank one, \(\operatorname{tr}_{\mathbb F}Z_G=1/2\), and its
affine pairing contributes the required group coefficient in (7).  Since the
off-diagonal coefficient \(-c_G/2\) is nonzero in every balanced group, every
certificate has rank at least one in every group; (6) attains total rank
\(q\).  The range vector of (6) has top and bottom squared masses
\(1/(q+1)\) and \(q/(q+1)\), so the reference compression is
\(2/(q+1)\), the nonzero certificate eigenvalue is \((q+1)/(2q)\), and
their product is exactly \(1/q\).  Hence (12) gives \(\Delta=1\) with no
field-dependent missing factor.

The movement conclusion is valid for forward Dikin chords measured in the
displayed restricted standard-logdet metric and starting at \(X^c\).  A
forward chord of local norm at most \(\theta<1\) has Riemannian length at most
\(-\log(1-\theta)\); the triangle inequality and (13) give (2).  This does
not supply an arbitrary-start or unrestricted primal--dual QIPM lower bound.

The state/readout claims were also checked.  One clean bit-oracle call becomes
one phase-oracle call using a standard \(|-\rangle\) target.  Therefore the
one-query statements are exact only conditional on exact charged preparation
of the public magnitude state, public index-to-sign routing, and the required
arithmetic precision.  For any feasible projected \(x\),
\(\|x-v_\sigma\|_2^2\le 2(1-v_\sigma^Tx)\); thus
\(\epsilon<1/(8n)\) implies the strict coordinate threshold in (16), and a
successful full output reveals all signs.  For constant accuracy, purification
and deferred measurement preserve the degree-\(T\) Fourier expansion
(17a), even with input-independent randomness and adaptive computation.
The final ensemble is supported on a space of dimension at most \(D_T\), so
Holevo's bound applies to every classical output measurement.  The decoded
distortion calculation (17b), binary rate-distortion inequality, and binomial
entropy bound then give (17c)--(17d).  This proves the stated
\(\Theta_\epsilon(n)\) bound for each fixed \(\epsilon<1/8\) under the exact
clean-bit/index oracle; arbitrary approximate-value oracles require a
separate reduction.  Reading all signs gives the matching \(O(n)\) upper
bound.

Finally, the quantifier swap is exact within the stated admissible-lift class.
The selection-free frontier gives
\(\inf_{\mathcal L}\sup_v r_{\mathcal L}(v)=q\).  For each fixed \(v_0\),
the explicitly objective-dependent projection rotation above makes it a
north-pole support with a rank-one certificate, whereas rank zero cannot
normalize a nonzero support slack.  Thus
\(\sup_v\inf_{\mathcal L}r_{\mathcal L}(v)=1\).  Equation (21) further shows
that this rotation costs one sign-oracle query per coherent use for the
balanced family, despite requiring all signs under an explicit classical
matrix-output contract.  Neither observation makes the rotation free in a
runtime model: its use and implementation costs must be charged separately.
