# PSD nullity gives an exact restricted log-det frontier

Status: Proved; literature-screened; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated global-selection and standard-barrier scope

## Result

Let \(N\geq4\), and let \(B_2^N\) have an exact strictly feasible affine
lift over

\[
                 K=\prod_{i=1}^L\mathbb S_+^{r_i},
                 \qquad 2\leq r_i\leq R.                    \tag{1}
\]

Assume that the full ball slack

\[
                         1-x^Tz,\qquad x,z\in S^{N-1},      \tag{2}
\]

has globally labelled \(C^1\) primal and dual contact factors

\[
  1-x^Tz=\sum_i\operatorname{tr}(X_i(x)Y_i(z)),
  \qquad X_i(x),Y_i(z)\succeq0,                            \tag{3}
\]

and that \(X(x)=(X_i(x))_i\) is a boundary point in the closure of the
same affine slice used by the lift.  Restrict the standard product
log-determinant barrier to the strictly feasible affine slice:

\[
                         F(Z)=-\sum_i\log\det Z_i.           \tag{4}
\]

Then its least self-concordant-barrier parameter satisfies

\[
                 \boxed{\nu(F|_{\rm slice})
                    \geq \left\lceil {N\over R-1}\right\rceil.} \tag{5}
\]

The bound is exact for every \(R\geq2\).  Partition the \(N\) coordinates
into

\[
                         k=\left\lceil {N\over R-1}\right\rceil \tag{6}
\]

groups of size at most \(R-1\), and use the grouped Schur-complement lift

\[
 Z_G(s_G,x)=
 \begin{pmatrix}s_G&x_G^T\\x_G&I_{|G|}\end{pmatrix}\succeq0,
 \qquad \sum_Gs_G=1.                                      \tag{7}
\]

After eliminating the fixed identity blocks,

\[
        -\sum_G\log\det Z_G
        =-\sum_G\log(s_G-\|x_G\|^2),                       \tag{8}
\]

whose exact parameter, including the equation \(\sum_Gs_G=1\), is \(k\).
Consequently, within the globally contact-selected class above,

\[
 \boxed{\displaystyle
   \min_{\substack{\text{PSD lifts of }B_2^N\\r_i\leq R}}
       \nu_{\rm std,slice}
       =\left\lceil {N\over R-1}\right\rceil.}              \tag{9}
\]

Equation (9) is about the standard product log-determinant after affine
restriction.  It is not a lower bound for arbitrary coupled barriers on a
slice, and it is not a lower bound on the actual number of IPM or QIPM
iterations.

## 1. Boundary nullity is the exact vanishing order

Let an affine space \(\mathcal A\) meet
\(\prod_i\mathbb S_{++}^{r_i}\), let
\(\bar Z\in\mathcal A\cap K\), and choose
\(Z^\circ\in\mathcal A\cap\operatorname{int}K\).  Along

\[
              Z_i(\tau)=(1-\tau)\bar Z_i+\tau Z_i^\circ,
              \qquad 0<\tau\leq1,                           \tag{10}
\]

put \(c_i=\operatorname{nullity}\bar Z_i\).  Congruence by
\((Z_i^\circ)^{-1/2}\) reduces the determinant to

\[
 \det Z_i(\tau)
 =\det Z_i^\circ\,
   \det\!\left(\tau I+(1-\tau)
       (Z_i^\circ)^{-1/2}\bar Z_i(Z_i^\circ)^{-1/2}\right).
                                                                    \tag{11}
\]

The positive eigenvalues in (11) approach positive constants and every
zero eigenvalue contributes exactly one factor \(\tau\).  Hence, with
\(c=\sum_i c_i\),

\[
\begin{aligned}
 f(\tau)&:=F(Z(\tau))=-c\log\tau+g(\tau),\\
 f'(\tau)&=-{c\over\tau}+O(1),\\
 f''(\tau)&={c\over\tau^2}+O(1),                            \tag{12}
\end{aligned}
\]

where \(g\) is analytic at zero.  The defining gradient inequality of a
\(\nu\)-self-concordant barrier, restricted to this line, gives

\[
                         |f'(\tau)|^2\leq\nu f''(\tau).      \tag{13}
\]

Taking \(\tau\downarrow0\) proves the reusable lemma

\[
                  \boxed{\nu(F|_{\mathcal A})
                         \geq\sum_i\operatorname{nullity}\bar Z_i.} \tag{14}
\]

No transversality of the affine slice is needed.

## 2. Curvature carried per unit of primal nullity

Fix a diagonal contact \(x=z\) in (3), and write

\[
 p_i=\operatorname{rank}X_i(x),\qquad
 q_i=\operatorname{rank}Y_i(x),\qquad
 c_i=r_i-p_i.                                               \tag{15}
\]

Termwise nonnegativity and the zero slack imply PSD complementarity, so

\[
                         p_i+q_i\leq r_i,\qquad q_i\leq c_i. \tag{16}
\]

Mixed differentiation of (3) on the two copies of \(S^{N-1}\) gives a
nondegenerate tangent pairing as a sum of PSD channels \(H_i\).  The usual
off-diagonal-block calculation, recalled in the
[PSD support--Grassmannian theorem](2026-09-04-psd-support-grassmannian-submersion.md),
yields

\[
 \operatorname{rank}H_i\leq p_iq_i
 \leq p_ic_i
 \leq(R-1)c_i.                                             \tag{17}
\]

Since the total tangent pairing has rank \(N-1\),

\[
                    N-1\leq\sum_i\operatorname{rank}H_i
                         \leq(R-1)\sum_i c_i.               \tag{18}
\]

Combining (14) and (18) already gives
\(\nu\geq\lceil(N-1)/(R-1)\rceil\).  This equals (5) unless

\[
                         N-1=h(R-1)                         \tag{19}
\]

for an integer \(h\).  The equality case in (18) is globally impossible;
that supplies the final integer unit.

## 3. Equality would cover a product of projective spaces

Assume (19) and, for contradiction, \(\nu<h+1\).  Equation (14) applies
at every contact, while (18) gives the reverse integer bound.  Therefore

\[
                    \sum_i c_i(x)=h\qquad(x\in S^{N-1}).    \tag{20}
\]

Every inequality in (17)--(18) is now equality.  Each block with positive
nullity has

\[
 r_i=R,\qquad c_i=q_i=1,\qquad p_i=R-1,                    \tag{21}
\]

and every zero-nullity block has zero mixed-curvature contribution.
The active set is locally constant.  Indeed, an active \(Y_i(x)\) is
nonzero and remains nonzero nearby, so complementarity keeps \(X_i\)
singular; (20) permits neither an additional singular block nor a further
rank drop.  Connectedness makes a fixed set \(I\) of exactly \(h\) blocks
active on the whole sphere.

For \(i\in I\), define the \(C^1\) support map

\[
 \pi_i:S^{N-1}\longrightarrow
       \operatorname{Gr}_{R-1}(\mathbb R^R)
       =\mathbb {RP}^{R-1},
 \qquad \pi_i(x)=\operatorname{Ran}X_i(x).                 \tag{22}
\]

The joint map

\[
 \Pi=(\pi_i)_{i\in I}:S^{N-1}
       \longrightarrow(\mathbb {RP}^{R-1})^h               \tag{23}
\]

is a local diffeomorphism.  To see this, if \(d\Pi(x)u=0\),
the off-diagonal support derivative in every active PSD block vanishes.
The corresponding \(H_i(u,\cdot)\) vanishes.  In an inactive block,
\(X_i(x)\succ0\) forces \(Y_i(x)=0\); a two-sided derivative of a \(C^1\)
PSD-valued map at the cone vertex is zero, so its channel also vanishes.
Nondegeneracy of the sum in (18) then forces \(u=0\).  Source and target
have the same dimension by (19), proving the claim.

Compactness makes (23) a finite covering.  This is impossible:

- if \(R=2\), the target is a positive-dimensional torus, whose universal
  cover is noncompact;
- if \(R\geq3\) and \(h\geq2\), the universal cover of the target is
  \((S^{R-1})^h\), whose intermediate cohomology differs from that of
  \(S^{N-1}\);
- if \(h=1\), all inactive dual factors vanish identically.  If
  \(\pi_1(x')=\pi_1(x)\), then
  \(\operatorname{tr}(X_1(x')Y_1(x))=0\), and (3) gives
  \(1-(x')^Tx=0\), hence \(x'=x\).  Thus \(\pi_1\) would be an injective
  covering \(S^{N-1}\to\mathbb {RP}^{N-1}\), impossible for \(N-1\geq2\).

This contradiction proves \(\nu\geq h+1\) in the only residue case where
the elementary ceiling was short by one.  Equation (5) follows.

## 4. Exact matching construction and QIPM ledger

For (7), Schur complementation gives

\[
                         Z_G\succeq0
             \quad\Longleftrightarrow\quad
                         s_G\geq\|x_G\|^2.                  \tag{24}
\]

Thus (7) projects exactly to \(B_2^N\), is strictly feasible, and has a
unique boundary fiber.  The polynomial contact factors displayed in the
[PSD cap-resource ledger](2026-09-04-psd-order-cap-qipm-ledger.md) verify
the global \(C^1\) hypothesis.

For one group,
\(-\log(s_G-\|x_G\|^2)\) is a one-self-concordant barrier.  Products add
parameters and affine restriction does not increase them.  Conversely, at
any product extreme every matrix \(Z_G\) has nullity one, so (14) gives
the matching lower bound \(k\).  This proves (8)--(9).

The same grouped formulation has ambient normal-barrier parameter
\(\sum_G(|G|+1)=N+k\).  Thus affine restriction changes its certified
parameter from \(N+k\) to the exact value \(k\).  For example,

\[
\begin{array}{c|c|c}
R&\nu_{\rm std,slice}^{\min}&
  \nu_{\rm ambient}\text{ of the matching Schur lift}\\ \hline
2&N&2N\\
3&\lceil N/2\rceil&N+\lceil N/2\rceil\\
\Theta(\sqrt N)&\Theta(\sqrt N)&N+\Theta(\sqrt N)\\
R\geq N+1&1&N+1.
\end{array}                                                  \tag{25}
\]

The reduced Hessian is diagonal plus one rank-one term per group.  Its
one-hub augmented graph is a forest, and an exact Newton solve costs
\(O(N)\) field operations.  From a supplied central-neighborhood start, let
\(\Delta\) denote the initial objective-gap/scale term in the standard
short-step analysis.  The certificate is

\[
 O\!\left(\sqrt{\left\lceil N/(R-1)\right\rceil}
           \log{\Delta\over\epsilon}\right)
 \quad\text{rounds}                                       \tag{26}
\]

and

\[
 O\!\left(
 N\sqrt{\left\lceil N/(R-1)\right\rceil}
 \log{\Delta\over\epsilon}\right)
 \quad\text{exact field operations}.                       \tag{27}
\]

Under matched access and mandatory materialization of the full reduced
direction, the \(O(N)\) tree solve is a same-round classical replacement
for a quantum linear-system subroutine.  This does not cover coherent or
scalar output, quantum-only input access, finite precision, or arbitrary
external coupling.

## 5. Literature and novelty boundary

The standard fact that \(-\log\det\) has parameter equal to matrix order
on the full PSD cone is classical.  Güler and Tunçel characterize the
optimal parameter on homogeneous cones in *Mathematical Programming* 81
(1998), 55--76, DOI
[10.1007/BF01584844](https://doi.org/10.1007/BF01584844).
The lift/factorization correspondence is due to Gouveia, Parrilo, and
Thomas, *Mathematics of Operations Research* 38 (2013), DOI
[10.1287/moor.1120.0575](https://doi.org/10.1287/moor.1120.0575).

The nullity lemma (14) is an elementary specialization of the
self-concordant gradient inequality and is not claimed as standalone new.
A targeted search did not locate the combination of nullity order,
mixed-curvature capacity per nullity, and projective-space covering
rigidity, nor the exact cap-dependent restricted standard-barrier frontier
(9).  Novelty is plausible pending specialist review.

The restrictions are material:

- the theorem assumes a strictly feasible affine PSD-product lift and
  compatible globally \(C^1\) primal and dual full-contact selections;
- it concerns the specified restricted sum of log-determinants, not an
  arbitrary barrier on the affine slice or projected ball;
- it gives a parameter-driven upper-bound certificate, not an iteration
  lower bound; and
- finite-precision and input/output access costs require separate analysis.

## 6. Independent hostile audit

The auditor independently rederived the determinant-order lemma and the
PSD off-diagonal curvature calculation.  In the divisibility case it
checked that a hypothetical parameter below \(h+1\) fixes the total
nullity at \(h\) on every contact, forces exactly \(h\) active order-\(R\)
blocks with ranks \((R-1,1)\), and makes their active set globally constant.
It then verified that the joint support map is a local diffeomorphism and
that all three covering obstructions are complete, including the
cross-contact injectivity argument when \(h=1\).

The grouped Schur lift, order cap, unique boundary fibers, exact parameter,
and tree-solve ledger were also checked.  The audit caught one scope issue
in the first draft: a generic short-step bound must retain the initial
gap/scale term.  Equations (26)--(27) now state that term explicitly and
assume a supplied central-neighborhood start.  No mathematical correction
to (5) or (9) was required.
