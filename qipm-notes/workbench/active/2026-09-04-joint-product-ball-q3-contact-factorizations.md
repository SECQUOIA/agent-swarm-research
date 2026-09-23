# Joint smooth \(Q_3\) contact factorizations for products of balls

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the fixed-contact theorem; full-lift implication explicitly conditional

## Executive result

Let

\[
 C=(B_2^s)^k,
 \qquad s\geq3,
 \qquad k\geq2,
\]

and fix positive weights \(\lambda_a\) with
\(\sum_{a=1}^k\lambda_a=1\).  The smooth weighted contact stratum is

\[
 M=(S^{s-1})^k,
 \qquad
 y_\lambda(z)=(\lambda_1z_1,\ldots,\lambda_kz_k)\in C^\circ .
\]

Its two-point slack is

\[
 S_\lambda(x,z)
 =1-\langle x,y_\lambda(z)\rangle
 =\sum_{a=1}^k\lambda_a(1-\langle x_a,z_a\rangle).       \tag{1}
\]

Write \(n=\dim M=k(s-1)\), and let \(L_{\rm contact}\) denote the minimum
over the globally labelled bi-\(C^1\) factorizations in (8).  Then:

1. every globally labelled bi-\(C^1\) factorization of (1) by \(L\)
   copies of \(Q_3\) satisfies

   \[
                          L\geq n+1=k(s-1)+1;                 \tag{2}
   \]

2. there is an explicit globally \(C^\infty\), nowhere-zero factorization
   of (1) by

   \[
                    L=ks-\lfloor k/2\rfloor                 \tag{3}
   \]

   copies of \(Q_3\), obtained by pairing the ball factors and sharing one
   stereographic chart within every pair;

3. consequently, for two balls the minimum among globally labelled
   bi-\(C^1\) contact factorizations is exact:

   \[
        L_{\rm contact}\big((B_2^s)^2;\lambda\big)=2s-1.     \tag{4}
   \]

For \(k\geq3\), (2)--(3) leave only the additive gap
\(\lceil k/2\rceil-1\):

\[
 ks-k+1\leq L_{\rm contact}
          \leq ks-\lfloor k/2\rfloor.                        \tag{5}
\]

The construction already disproves the conjecture that this contact slack
forces the separate-coordinate count \(ks\).  The remaining gap cannot be
settled by the phase-immersion obstruction or by stable tangent-bundle
characteristic classes: \((S^{s-1})^k\) embeds as a hypersurface in
\(\mathbb R^{n+1}\).  Any stronger lower bound must use more of the full
two-point identity (1).

This is a theorem about the fixed smooth contact stratum.  It is not a
construction of a \(Q_3^{ks-\lfloor k/2\rfloor}\) affine lift of the whole
product body.
Conversely, every full lift with globally smooth selected contact factors
restricts to the setting above, so (2) is a valid conditional lower bound
for such lifts.  The nonsmooth full boundary of \(C\) is never treated as a
smooth contact manifold.

## 1. The fixed weighted contact stratum

The polar of the Cartesian product is

\[
 C^\circ
 =\left\{y=(y_1,\ldots,y_k):
                 \sum_{a=1}^k\|y_a\|_2\leq1\right\}.        \tag{6}
\]

For \(z\in M\), \(y_\lambda(z)\in\partial C^\circ\), and for
\(x\in M\),

\[
 \langle x,y_\lambda(x)\rangle
 =\sum_a\lambda_a=1.
\]

Thus (1) is a genuine restriction of the product body's slack operator.
Mixed differentiation at \(z=x\) gives

\[
 H_x=-d_xd_zS_\lambda(x,z)|_{z=x}
     =\bigoplus_{a=1}^k\lambda_a g_{S^{s-1},x_a},             \tag{7}
\]

a positive-definite metric of rank \(n=k(s-1)\).  On the primal side,
\(M\) is the smooth all-active stratum of the product's manifold-with-corners
boundary; it is not a smooth open piece of \(\partial C\).  On the polar side,
all blocks of \(y_\lambda(z)\) are nonzero, so this weighted stratum avoids the
nonsmooth zero-block loci of \(\partial C^\circ\).

## 2. The saturated \(+1\) lower bound

Let

\[
 S_\lambda(x,z)=\sum_{i=1}^L\langle A_i(x),B_i(z)\rangle,
 \qquad A_i(x),B_i(x)\in Q_3,                                \tag{8}
\]

where all factor maps are globally labelled and \(C^1\).  The universal
tangent-pairing bound for a three-dimensional proper cone gives

\[
 \operatorname{rank}\bigl(-dA_i(x)^*dB_i(x)\bigr)\leq1.
\]

For completeness, this bound is direct here.  At \(z=x\), the left side of
(8) is zero and every cone pairing is nonnegative, so each channel is
complementary.  If either factor is the vertex, its two-sided derivative is
zero.  Otherwise, pointwise write
\(A_i=a_i(1,p_i)\), \(B_i=b_i(1,-p_i)\) with \(p_i\in S^1\).  Differentiating
at that point cancels the scale derivatives and gives

\[
 -\langle dA_i(x)u,dB_i(x)v\rangle
 =a_i(x)b_i(x)\langle dp_i(x)u,dp_i(x)v\rangle,
\]

which has rank at most \(\dim T_{p_i(x)}S^1=1\).

Equation (7) therefore first implies \(L\geq n\).

Suppose for contradiction that \(L=n\).  Rank subadditivity is then
saturated at every \(x\).  Every channel has rank one everywhere, so neither
\(A_i(x)\) nor \(B_i(x)\) can be the cone vertex.  Indeed, the two-sided
derivative of a \(C^1\) cone-valued map at the vertex is zero, which would
annihilate its mixed channel.

Write

\[
 A_i(x)=a_i(x)(1,p_i(x)),\qquad
 B_i(x)=b_i(x)(1,-p_i(x)),                                   \tag{9}
\]

with \(a_i,b_i>0\) and \(p_i:M\to S^1\).  Complementarity on the
diagonal gives the same phase in the two maps.  Since \(s\geq3\),

\[
 \pi_1(M)=\pi_1((S^{s-1})^k)=0.
\]

Each \(p_i\) therefore has a global \(C^1\) lift
\(p_i=(\cos\theta_i,\sin\theta_i)\), \(\theta_i:M\to\mathbb R\).
Differentiating (9) in (8), with the zeroth- and first-order terms killed by
diagonal complementarity, gives exactly

\[
 H_x=\sum_{i=1}^n a_i(x)b_i(x)
                   d\theta_i(x)\otimes d\theta_i(x).         \tag{10}
\]

Hence

\[
 \Theta=(\theta_1,\ldots,\theta_n):M\longrightarrow\mathbb R^n
\]

has invertible derivative everywhere.  It is a local diffeomorphism.
Its image is both open and compact, which is impossible for a nonempty
subset of \(\mathbb R^n\).  This proves (2).

More generally, if all factors in (8) are nowhere zero, the same argument
shows that \(\Theta:M\to\mathbb R^L\) is an immersion.  Thus the phase
argument actually gives

\[
                   L\geq \operatorname{imm}_{\mathbb R}(M), \tag{11}
\]

the Euclidean immersion dimension of the contact manifold.

## 3. Why topology cannot improve (2)

The product \(M=(S^{s-1})^k\) has a smooth codimension-one embedding in
\(\mathbb R^{n+1}\).  A short induction proves this without characteristic
classes.  The base sphere is a hypersurface.  If a compact orientable
hypersurface \(N^m\subset\mathbb R^{m+1}\) has global unit normal \(\nu\),
then, after adding \(p\) zero coordinates, its normal bundle in
\(\mathbb R^{m+p+1}\) is the trivial \((p+1)\)-plane bundle spanned by
\(\nu\) and the new coordinate directions.  The boundary of a sufficiently
small tubular neighborhood is therefore

\[
                         N\times S^p\hookrightarrow
                         \mathbb R^{m+p+1}.                   \tag{12}
\]

Starting from \(S^{s-1}\) and taking \(p=s-1\) at every step gives the claimed
embedding of \((S^{s-1})^k\).
Its \(n+1\) coordinate differentials span \(T^*M\) everywhere.  Therefore
the immersion/exact-one-form consequence of (10) is sharp at \(n+1\), as
are obstructions depending only on the stable tangent bundle.  This does
not exclude a different cohomological invariant of the full two-point
factorization.

This does **not** manufacture the positive weights and full off-diagonal
identity required in (8).  It only isolates where a stronger obstruction
would have to enter.

## 4. Shared stereographic factorizations

### 4.1 One group of at least two balls

Put \(D=ks\) and define the canonical spherical embedding

\[
 X(x)=(\sqrt{\lambda_1}x_1,\ldots,
       \sqrt{\lambda_k}x_k)\in S^{D-1}.                       \tag{13}
\]

Then

\[
                         S_\lambda(x,z)=1-X(x)^TX(z).         \tag{14}
\]

Because \(k\geq2\) and every weight is positive, the image \(X(M)\) is a
proper subset of the ambient sphere.  For example, a unit coordinate vector
\(q\) in the first block is not in \(X(M)\), since the norm of that block is
always \(\sqrt{\lambda_1}<1\).  Define

\[
 c(x)=1-q^TX(x)>0,
 \qquad
 F(x)=\frac{X(x)-(q^TX(x))q}{c(x)}\in q^\perp\cong\mathbb R^{D-1}. \tag{15}
\]

The stereographic chord identity is

\[
 1-X(x)^TX(z)
   ={c(x)c(z)\over2}\|F(x)-F(z)\|_2^2.                       \tag{16}
\]

Choose an orthonormal basis of \(q^\perp\), write
\(F=(f_1,\ldots,f_{D-1})\), and set

\[
\begin{aligned}
 U(t)&=\left({1+t^2\over2},{1-t^2\over2},t\right),\\
 V(t)&=\left({1+t^2\over2},-{1-t^2\over2},-t\right).
\end{aligned}                                                  \tag{17}
\]

Both maps take values on the nonzero boundary of \(Q_3\), and

\[
                         \langle U(t),V(u)\rangle
                         ={1\over2}(t-u)^2.                   \tag{18}
\]

For \(i=1,\ldots,D-1\), define

\[
             A_i(x)=c(x)U(f_i(x)),\qquad
             B_i(z)=c(z)V(f_i(z)).                            \tag{19}
\]

Equations (16)--(18) prove

\[
 S_\lambda(x,z)
 =\sum_{i=1}^{D-1}\langle A_i(x),B_i(z)\rangle.              \tag{20}
\]

Since \(c\) is bounded away from zero on compact \(M\), all maps in (19)
are globally \(C^\infty\) and nowhere zero.  Thus one shared
stereographic chart factorizes a group of \(g\geq2\) balls using \(gs-1\)
channels.  For \(g=2\), this is \(2s-1\), exactly one above the contact
dimension.

The saving is genuinely shared: the separate polynomial coordinate-square
construction uses \(gs\) channels on this group, while (19) removes one
channel.

### 4.2 Pair the product factors

Partition the \(k\) balls into \(m=\lfloor k/2\rfloor\) disjoint pairs and,
when \(k\) is odd, one singleton.  For a pair \(G=\{a,b\}\), put
\(\Lambda_G=\lambda_a+\lambda_b\), apply Section 4.1 to the normalized
weights \(\lambda_a/\Lambda_G,\lambda_b/\Lambda_G\), and multiply each of
its primal and dual Lorentz factors by \(\sqrt{\Lambda_G}\).  This gives its
unnormalized contribution

\[
 \lambda_a(1-x_a^Tz_a)+\lambda_b(1-x_b^Tz_b)
\]

with \(2s-1\) channels.  A singleton uses the standard \(s\)-channel
coordinate-square factorization

\[
 \lambda_a(1-x_a^Tz_a)
 =\sum_{j=1}^s
   \left\langle\sqrt{\lambda_a}\,U((x_a)_j),
                   \sqrt{\lambda_a}\,V((z_a)_j)\right\rangle,
\]

because (18) and \(\|x_a\|=\|z_a\|=1\) make the sum equal to the
left side.  Concatenating the independent positive factorizations gives

\[
 m(2s-1)+(k-2m)s=ks-\lfloor k/2\rfloor.                     \tag{20a}
\]

This proves (3).  When \(k=2\), (20a) equals \(2s-1=n+1\), and comparison
with (2) proves the exact count (4).

## 5. Optimality inside the one-common-scale chordal subclass

The stereographic construction cannot be iterated mechanically to remove
another coordinate while retaining one common radial scale.  Precisely,
suppose

\[
 S_\lambda(x,z)
 ={r(x)r(z)\over2}\|G(x)-G(z)\|_2^2,
 \qquad r(x)>0,\quad G:M\to\mathbb R^L.                     \tag{21}
\]

The right side is a sum of \(L+2\) separable kernels:

\[
 {r(x)r(z)\over2}\|G(x)\|^2
 +{r(x)r(z)\over2}\|G(z)\|^2
 -r(x)r(z)G(x)^TG(z),
\]

so its ordinary functional rank is at most \(L+2\).

The left side has rank exactly \(D+1=ks+1\).  Indeed, the constant function
and the \(D\) coordinate functions of the product spheres are linearly
independent, and (14) has coefficient inertia \((1,D)\).  Consequently

\[
                              L\geq D-1=ks-1.                 \tag{22}
\]

Thus (19) is optimal among all squared-feature factorizations using one
common scale across all \(k\) blocks.  The paired construction escapes this
bound by using a different common scale for each pair.  Reaching the
topological lower bound for \(k\geq3\) would require still stronger sharing
between these scale groups or a different nonlocal identity.

## 6. Lift and barrier implications

Any full \(Q_3^L\) lift of \(C\) whose selected primal and dual contact
factors are globally \(C^1\) on the weighted stratum restricts to (8).
Therefore

\[
                       L\geq k(s-1)+1.                        \tag{23}
\]

The exact optimal self-concordant barrier parameter of the unchanged
ambient product \(Q_3^L\) is \(2L\), even allowing coupled barriers.  This is
an ambient-cone statement: it is not a lower bound for a barrier defined only
on the affine feasible slice or directly on \(C\), and it does not by itself
imply an iteration lower bound for every interior-point method.  Hence
such a regular pure-\(Q_3\) formulation has

\[
                  \nu_{\rm ambient}\geq2[k(s-1)+1].          \tag{24}
\]

The separate smooth coordinate lifts of the \(k\) balls use \(ks\) factors
and attain \(\nu_{\rm ambient}=2ks\).  The stereographic factorization in
Section 4 does not by itself close this formulation gap because it only
factors the fixed weighted contact restriction, not the full slack operator.
For comparison, nonsmooth norm-tree lifts use \(k(s-1)\) factors and lie
exactly at the curvature count that (2) rules out under global bi-contact
regularity.

## 7. Literature screen and novelty boundary

The general equivalence between proper cone lifts and full slack-operator
factorizations is due to Gouveia, Parrilo, and Thomas, *Mathematics of
Operations Research* 38 (2013), DOI
[10.1287/moor.1120.0575](https://doi.org/10.1287/moor.1120.0575).  The
second-order-cone-rank literature includes Fawzi's nonrepresentability work,
*Mathematical Programming* 2019, DOI
[10.1007/s10107-018-1233-0](https://doi.org/10.1007/s10107-018-1233-0), and
Saunderson's bounded-face-chain obstruction, *SIAM Journal on Optimization*
30 (2020), DOI
[10.1137/19M1245670](https://doi.org/10.1137/19M1245670).  Hirsch's immersion
classification is in *Transactions of the AMS* 93 (1959), DOI
[10.2307/1993453](https://doi.org/10.2307/1993453).
The recent paper of Aubrun, La Piana, and Müller-Hermes,
[*Factorization through Lorentz
cones*](https://arxiv.org/abs/2606.27825), studies which positive linear maps
factor through direct sums of Lorentz cones.  Its positive-map setting does
not state a smooth fixed-contact count, the paired construction above, or the
exact two-ball result.

Targeted searches for SOC rank or smooth SOC factorizations of Cartesian
products of Euclidean balls did not locate the fixed-stratum \(+1\) theorem,
the paired stereographic construction, or the exact two-ball count (4).
Novelty is therefore plausible for this regular-contact synthesis,
not for stereographic projection, tubular neighborhoods, immersion theory,
or the general lift/factorization correspondence separately.

## 8. Open exact question

For \(k\geq3\), determine whether arbitrary globally smooth, possibly
channel-asymmetric \(Q_3\) contact factors can attain

\[
                            L=k(s-1)+1,
\]

or whether the full two-point identity forces an intermediate count up to
\(ks-\lfloor k/2\rfloor\).  Sections 3 and 5 sharply delimit two failed
approaches: topology stops at the lower endpoint, while one global
common-scale chordal construction stops at \(ks-1\).  A valid improvement
must share channels across the distinct pair scales without losing cone
positivity.

## Audit record

An independent hostile audit checked the cone-vertex argument, the exact
phase-square formula and its sign, the Euclidean immersion dimension, the
stereographic identity and its factor of \(1/2\), positivity of the common
scale, scaling of both factors in each pair, the paired channel count, the
common-scale functional-rank bound, and the distinction between a fixed
contact factorization and a full lift. No mathematical defect remained
after narrowing one overbroad topology sentence and correcting (21).
