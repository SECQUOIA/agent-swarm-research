# Exact selection-free exposed rank for real PSD2 lifts of product balls

Status: Proved and independently hostile-audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High on the proof; priority not established

## Result

Let
\[
                     C=\prod_{d=1}^b B_2^{s_d},\qquad s_d\geq2,
\]
have a finite affine lift over a product of real \(2\times2\) PSD cones
and scalar PSD rays.  Reduce once to the minimal face and assume relative
Slater.  Then there are genuine
pure-row support certificates \(Y^1,\ldots,Y^b\) at one simultaneous
contact \(u\) such that, for all \(\lambda_d>0\),

\[
 \boxed{
  \sum_i\operatorname{rank}\left(\sum_d\lambda_dY_i^d\right)
                         \geq \sum_{d=1}^b(s_d-1).}        \tag{1}
\]

Every primal lift fiber over \(u\) consequently satisfies

\[
 \boxed{\sum_i\operatorname{nullity}X_i
                         \geq\sum_{d=1}^b(s_d-1).}        \tag{2}
\]

Separate binary norm chains attain the exposed-rank bound in (1), and at a
generic simultaneous contact they attain (2).  Thus the exact minimax
selection-free exposed rank, for any fixed positive weights \(\lambda_d\),
is

\[
 \boxed{
  \inf_{\text{affine PSD2 lifts}}
  \sup_{\substack{u\in\prod_dS^{s_d-1}\\
                   Y^d\in\mathcal D_d(u_d)}}
  \sum_i\operatorname{rank}\left(\sum_d\lambda_dY_i^d\right)
       =\sum_{d=1}^b(s_d-1).}                            \tag{3}
\]

Here the positive weights \(\lambda_d\) are arbitrary and do not affect
the rank.  Formula (3) uses the favorable exposing certificate, as does the
exposed-rank movement theorem.  The chain has a unique certificate, so the
upper bound is independent of this choice.

This differs sharply from the globally bi-\(C^1\) Hermitian theorem, whose
real order-two value is \(\sum_ds_d\).  Unique, continuous, semialgebraic
certificate fibers can therefore lie one unit per source below the smooth
frontier.  Their rank drops at norm-tree seams.

## 1. One-ball intrinsic lemma

Consider any semialgebraic family \(\mathcal E(v)\) of nonempty tuples in
products of \(\mathbb S_+^2\) and rays such that

\[
                    \langle A(u),Z\rangle=1-u^Tv          \tag{4}
\]

for every \(u\in B_2^s\), every \(v\in S^{s-1}\), and every
\(Z\in\mathcal E(v)\).  Here \(A(u)\) may be any semialgebraic feasible
primal selection; no global continuity is assumed.

> **Lemma 1.**  Some \(v\) satisfies
> \[
>                  \min_{Z\in\mathcal E(v)}
>                       \sum_i\operatorname{rank}Z_i\geq s-1.        \tag{5}
> \]

Choose semialgebraically, for every \(v\), a certificate of minimum total
rank, and choose a semialgebraic primal fiber \(A(u)\).  Such a choice does
not require compact fibers: total rank takes finitely many integer values,
the fiberwise minimum is attained by some element of every nonempty fiber,
and quantifier elimination makes the minimum-rank incidence semialgebraic.
Finite
semialgebraic stratification gives a nonempty open
contact stratum on which both selections are \(C^1\) and the selected block
ranks are constant.  Differentiate (4) tangentially at a diagonal contact.
Its mixed derivative is the rank-\((s-1)\) sphere metric.

For one \(2\times2\) PSD block, complementarity leaves only three cases.

- If the dual block has rank zero, its mixed contribution is zero.
- If it has rank two, the primal block is the cone vertex.  The derivative
  of a differentiable cone-valued map at a vertex is zero, so again its
  mixed contribution is zero.
- If it has rank one, the complementary primal block has rank at most one,
  and the standard PSD cross-channel bound makes its mixed contribution
  have real rank at most one.

A scalar ray likewise contributes at most zero to the curved sphere
metric: at contact one factor is zero, and differentiability into a pointed
ray kills its derivative there.  Hence

\[
 s-1\leq\operatorname{rank}\left(\sum_iH_i\right)
       \leq\sum_{i:\operatorname{rank}Z_i=1}1
       \leq\sum_i\operatorname{rank}Z_i.                 \tag{6}
\]

At any point of the common open stratum, the selected certificate realizes
the fiberwise minimum, proving (5).  Only generic local differentiability
is used; the selection may be singular on the complement.

## 2. Compression of global certificate fibers

Apply Lemma 1 sequentially as in the intrinsic real one-channel theorem.
After choosing rows \(e<d\), let

\[
 W_i^{d-1}=\sum_{e<d}\operatorname{Ran}Y_i^e,
 \qquad P_i^{d-1}=P_{(W_i^{d-1})^\perp}.                 \tag{7}
\]

Every primal fiber in the whole future-coordinate cylinder kills
\(W_i^{d-1}\), by termwise PSD complementarity with the earlier genuine
row certificates.  Compress the original row-\(d\) certificate fiber:

\[
 \mathcal E_d(v)=\{(P_i^{d-1}Y_iP_i^{d-1})_i:
                         Y\in\mathcal D_d(v)\}.           \tag{8}
\]

This is a nonempty semialgebraic family.  Compactness, boundedness, and
closed graph are unnecessary: minimum integer rank is attained by an
actual image element, and semialgebraic choice supplies a preimage.
Against any semialgebraic primal selection in the whole cylinder it
satisfies the exact one-ball identity (4).  Lemma 1 therefore
chooses \(u_d\) and a genuine preimage
\(Y^d\in\mathcal D_d(u_d)\) with

\[
        \sum_i\operatorname{rank}(P_i^{d-1}Y_i^dP_i^{d-1})
                                                   \geq s_d-1.     \tag{9}
\]

For PSD \(Y=CC^T\),

\[
 \operatorname{rank}(P_{W^\perp}YP_{W^\perp})
    =\dim(W+\operatorname{Ran}Y)-\dim W.                 \tag{10}
\]

Thus row \(d\) adds at least \(s_d-1\) new range dimensions.  At the final
contact,

\[
                    \sum_i\dim W_i^b
                              \geq\sum_{d=1}^b(s_d-1),   \tag{11}
\]

and every final primal fiber kills \(W_i^b\), proving (2).  Positive PSD
range additivity gives

\[
 \operatorname{Ran}\left(\sum_d\lambda_dY_i^d\right)
      =\sum_d\operatorname{Ran}Y_i^d=W_i^b,              \tag{12}
\]

which proves (1).

## 3. Exact binary norm-chain attainment

For \(s=2\), the single trace-one \(\mathbb S_+^2\) slice is the required
chain and has one rank-one support certificate.  Assume below that
\(s\geq3\).

Let

\[
 M(\tau,z_1,z_2)=
   \begin{pmatrix}\tau+z_1&z_2\\z_2&\tau-z_1\end{pmatrix}.
\]

For one ball, introduce \(t_1,\ldots,t_{s-2}\) and impose

\[
 \begin{aligned}
 X_1&=M(t_1,x_1,x_2)\succeq0,\\
 X_j&=M(t_j,t_{j-1},x_{j+1})\succeq0
                         &&(2\leq j\leq s-2),\\
 X_{s-1}&=M(1,t_{s-2},x_s)\succeq0.
 \end{aligned}                                           \tag{13}
\]

The nested norm inequalities project exactly to \(B_2^s\), and choosing
strictly increasing positive \(t_j<1\) over \(x=0\) proves Slater.

For \(v\in S^{s-1}\), put
\(\rho_j=(\sum_{\ell=1}^{j+1}v_\ell^2)^{1/2}\).  The unique dual
certificate is

\[
 \begin{aligned}
 Z_1&={1\over2}M(\rho_1,-v_1,-v_2),\\
 Z_j&={1\over2}M(\rho_j,-\rho_{j-1},-v_{j+1})
                                  &&(2\leq j\leq s-1).
 \end{aligned}                                           \tag{14}
\]

Indeed,
\(\operatorname{tr}(M(a,b,c)M(d,e,f)/2)=ad+be+cf\), so the terms
telescope to \(1-v^Tx\).  Conversely, write a general dual block as
\(M(\alpha_j,\beta_j,\gamma_j)/2\).  Coefficient matching gives

\[
 \beta_1=-v_1,\quad\gamma_1=-v_2,\quad
 \beta_j=-\alpha_{j-1},\quad\gamma_j=-v_{j+1},\quad
 \alpha_{s-1}=1.                                        \tag{15}
\]

PSD gives
\(\alpha_1\geq\rho_1\) and
\(\alpha_j\geq(\alpha_{j-1}^2+v_{j+1}^2)^{1/2}\).  Since
\(\|v\|=1=\alpha_{s-1}\), every inequality is equality, proving (14) and
uniqueness.  Each block has rank one if \(\rho_j>0\) and is zero otherwise,
so every certificate has rank at most \(s-1\), with equality on a dense
open set.  Taking products of independent chains proves the upper bound in
(3).

## 4. Scope

The theorem optimizes exposed dual rank and proves an associated boundary
nullity lower bound.  The companion arbitrary-cap note computes the exact
restricted standard-logdet parameter of the binary norm chain as
\(2s-3\): vertex seams have larger primal nullity than a generic contact.
This is not an arbitrary-barrier or QIPM iteration lower bound.

There is a precise obstruction to obtaining the missing nullity unit from
topology alone.  If one assumes every boundary fiber contains a point of
nullity \(s-1\), semialgebraic stratification produces a surjective
rank-saturated phase incidence over \(S^{s-1}\), but not an unbranched
cover or a continuous phase selector.  Already for \(s=3\), the phase
space of two nonzero PSD2 boundary blocks is a torus, and the quotient of
an elliptic curve by its involution is a finite branched cover
\(T^2\to S^2\).  It has rank-one phases everywhere and loses differential
rank only at the branch points.  This abstract example is not asserted to
come from an affine ball lift.  It proves that compactness,
semialgebraicity, and phase topology by themselves cannot establish the
selection-free standard-barrier \(+1\); a proof must use the affine slack
identities or determinantal geometry to exclude branching.
The audited [nullity-seam reduction](2026-09-04-selection-free-psd2-nullity-seam-obstruction.md)
records the full certificate-span argument and the exact remaining
integrability question.

The contrast with the global-\(C^1\) value \(\sum_ds_d\) is the main regularity
lesson.  Semialgebraic generic strata suffice for the local \(b(s-1)\)
law in the homogeneous case, but the missing one unit per source is genuinely global topology and
is lost at the chain's rank-drop seams.

The certificate-fiber compression mechanism is developed in
[the selection-free critical real theorem](2026-09-04-affine-psd-sequential-compression-without-selections.md).
The companion [arbitrary-cap Lorentz
theorem](2026-09-04-selection-free-exposed-rank-premium-counterexample.md)
proves the one-ball formula
\(\lceil(s-1)/(d-2)\rceil\) and constructs its unique-certificate grouped
norm chain.  The present note supplies the fully detailed heterogeneous
PSD2 product induction and its exact favorable-aggregate minimax
quantifiers.
A targeted literature screen found block-triangular PSD-rank compression
and semialgebraic SDP sensitivity results, but no exact
\(\sum_d(s_d-1)\) support-certificate minimax theorem for products of balls.
Priority remains subject to specialist review.

## Audit checklist

1. Verify semialgebraic minimum-rank/minimum-norm selection and existence of
   one common open \(C^1\) contact stratum.
2. Recheck the rank-two-dual/vertex-primal derivative-zero case and scalar
   rays in (6).
3. Verify that compressed image fibers remain semialgebraic and nonempty,
   and that minimum-rank selection plus a genuine global preimage require
   neither compactness nor a closed graph.
4. Check the product induction and quantifier order in (3).
5. Recheck chain exactness, dual coefficient matching, uniqueness, and all
   seam ranks.

## Independent hostile audit

The audit first selected a minimum-total-rank certificate
semialgebraically.  The minimum-rank locus is definable because the rank
sublevel sets are closed semialgebraic, and definable choice followed by
finite stratification gives a common full-dimensional \(C^1\) contact
stratum with a semialgebraic primal selector.  At such a contact, a
rank-two dual \(2\times2\) block forces the primal block to the vertex and
has zero derivative channel; a rank-one dual has mixed capacity at most
one; rank-zero blocks and rays have zero capacity.  The rank-\((s-1)\)
sphere metric therefore proves the fiberwise minimum bound in Lemma 1.

The compressed image fibers in (8) remain nonempty and semialgebraic.
Earlier genuine
pure-row certificates put every future-cylinder primal fiber in their
common kernels, so compression preserves the exact row identity.  The
PSD range formula (10) counts exactly the new range increment.  Retaining
one semialgebraically selected original preimage at each stage makes all
final certificates genuine, and positive weights turn their aggregate
ranges into joins.  This proves (1)--(2) with the stated
favorable-certificate quantifiers in (3), without an unjustified dual-fiber
boundedness assumption.

Finally, direct coefficient matching in the binary chain gives (15).
The terminal equality \(\alpha_{s-1}=1=\rho_{s-1}\) forces equality
backward in every PSD recursion, so the displayed certificate is unique.
Its total rank is at most \(s-1\) and equals \(s-1\) on a dense open
support set.  Independent products of the chains therefore attain the
lower bound exactly.  No correction was required.
