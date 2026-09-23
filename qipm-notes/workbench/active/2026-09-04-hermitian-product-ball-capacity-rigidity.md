# Hermitian curvature saturation for products of balls

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Theorem

Let

\[
                  C=\prod_{a=1}^h B_2^{s_a},\qquad
                  M=\prod_{a=1}^h S^{p_a},\qquad p_a=s_a-1\geq1,       \tag{1}
\]

and put \(n=\sum_ap_a\).  Suppose every extreme-row slack

\[
                         1-x_a^Tz                                      \tag{2}
\]

has globally labelled \(C^1\) factors over a finite product of real,
complex, or quaternionic Hermitian PSD cones:

\[
  1-x_a^Tz=
   \sum_i\operatorname{Re}\operatorname{tr}
       \bigl(X_i(x)Y_i^a(z)\bigr),qquad
  X_i,Y_i^a\in H_+^{r_i}(\mathbb F_i),\qquad r_i\geq2.               \tag{3}
\]

Write \(a_i=\dim_{\mathbb R}\mathbb F_i\in\{1,2,4\}\) and

\[
                         c_i=a_i\left\lfloor{r_i^2\over4}\right\rfloor.
                                                                         \tag{4}
\]

Then

\[
                              n\leq\sum_i c_i.                           \tag{5}
\]

Moreover, equality in (5) is possible only if, after removing factors whose
full slack term vanishes,

1. every block has order \(r_i=2\); and
2. the multiset of source tangent dimensions \(\{p_a\}\) equals the
   multiset \(\{a_i\}\).

Conversely, this exceptional profile is attained by one direct
\(H_+^2(\mathbb F_i)\cong Q_{a_i+2}\) factor for each matching source
ball.  Thus, unless the product consists blockwise of two-, three-, and
five-dimensional balls matched to real, complex, and quaternionic
order-two cones,

\[
                         \boxed{\displaystyle\sum_i c_i\geq n+1.}      \tag{6}
\]

For a fixed field \(\mathbb F\), saturation occurs exactly for products of
\(B_2^{a+1}\), represented by order-two blocks over that field.

The exclusion of scalar ray factors in (3) is substantive.  A ray has zero
mixed-curvature capacity but can carry nonzero global slack and can destroy
the injectivity step below.  The theorem also applies if rays are present
but their full slack terms vanish.  No statement for arbitrary active ray
factors is claimed.

## Proof

At a simultaneous contact \(z=x_a\), put

\[
 q_i=\operatorname{rank}_{\mathbb F_i}\sum_aY_i^a(x_a),qquad
 p_i'=\operatorname{rank}_{\mathbb F_i}X_i(x).                           \tag{7}
\]

Complementarity gives \(p_i'+q_i\leq r_i\).  Simultaneous mixed
differentiation of all rows in (3) writes the nondegenerate product metric
on \(T_xM\) as a sum of block forms of real rank at most
\(a_ip_i'q_i\).  Therefore

\[
 n\leq\sum_i a_ip_i'q_i
   \leq\sum_i a_i\left\lfloor{r_i^2\over4}\right\rfloor,               \tag{8}
\]

which proves (5).

Assume equality.  Every positive block saturates every inequality in (8)
at every \(x\).  Thus it is strictly complementary with balanced ranks,
and those ranks are constant on the connected manifold \(M\).  If the
primal rank is \(\lfloor r_i/2\rfloor\), use its range; if it is
\(\lceil r_i/2\rceil\), use its kernel.  This gives a \(C^1\) support map
to the same balanced Grassmannian in either case.  The standard support
differential identifies the full mixed-curvature channel with its tangent
space:

\[
 G_i=\operatorname{Gr}_{\lfloor r_i/2\rfloor}
             (\mathbb F_i^{r_i}),\qquad \dim_{\mathbb R}G_i=c_i.        \tag{9}
\]

The combined support map

\[
                           \Pi:M\longrightarrow\prod_iG_i              \tag{10}
\]

has injective derivative: a vector in \(\ker d\Pi\) annihilates every
block mixed form in (8), hence the nondegenerate product metric.  Equality
of dimensions makes \(\Pi\) a local diffeomorphism.

The full slack family makes \(\Pi\) globally injective.  If
\(\Pi(x')=\Pi(x)\), then every \(Y_i^a(x_a)\) is supported in
\(\ker X_i(x)=\ker X_i(x')\).  Substitution in (3) gives

\[
                      1-(x_a')^Tx_a=0\qquad(a=1,\ldots,h),              \tag{11}
\]

so \(x'=x\).  Compactness now makes (10) a diffeomorphism.

It remains to classify when a product of balanced Hermitian
Grassmannians can be diffeomorphic to a product of spheres.  A real
balanced Grassmannian of order \(r\geq3\) has fundamental group
\(\mathbb Z/2\).  Indeed, in the homogeneous-space fibration
\(S(O(k)\times O(r-k))\to SO(r)\to\operatorname{Gr}_k(\mathbb R^r)\),
the identity component maps surjectively on \(\pi_1(SO(r))\), while the
fiber has two components; the homotopy exact sequence gives the claim.
Since \(\pi_1(M)\) is free abelian, no such real factor can occur.  The
remaining real case is
\(\operatorname{Gr}_1(\mathbb R^2)=S^1\).

For a complex balanced Grassmannian of order \(r\geq3\), the degree-two
Schubert class has nonzero square over \(\mathbb F_2\).  For a
quaternionic balanced Grassmannian of order \(r\geq3\), the degree-four
Schubert class has nonzero square.  In contrast, in the positive-degree
mod-two cohomology of a product of spheres every element has square zero:
the Frobenius square of each square-free monomial generator vanishes.
Thus the only complex and quaternionic targets are

\[
          \mathbb CP^1=S^2,\qquad \mathbb HP^1=S^4,                    \tag{12}
\]

both arising at order two.

Consequently \(\prod_iG_i\) is a product of spheres of dimensions
\(a_i\in\{1,2,4\}\).  The graded indecomposable quotient

\[
          H^{>0}(-;\mathbb F_2)/(H^{>0}(-;\mathbb F_2))^2               \tag{13}
\]

of a product-of-spheres cohomology ring records one generator in each
sphere dimension.  The diffeomorphism (10) therefore forces equality of
the multisets \(\{p_a\}\) and \(\{a_i\}\).  This proves necessity.

For sufficiency, use the standard Lorentz identification
\(H_+^2(\mathbb F)\cong Q_{a+2}\) and the direct ball slack factorization
for each source independently.  Capacities add to \(n\), proving the
claimed sharpness and the integer gap (6).

## Scope and relation to prior notes

The local rank calculation is the Hermitian support-channel theorem in
[Saturated PSD factors induce Grassmannian
submersions](2026-09-04-psd-support-grassmannian-submersion.md).  The new
ingredient here is that the **full product-row slack** makes the joint
support map injective, upgrading a covering obstruction to a diffeomorphism
classification.  For homogeneous real products with sphere dimension at
least two, (6) recovers and broadens the strict capacity law in
[PSD column packing shares full product-ball slack
rows](2026-09-04-psd-column-packing-product-balls.md).

For the topological input, Sankaran and Sarkar's
[*Degrees of Maps between Grassmann
Manifolds*](https://www.imsc.res.in/~sankaran/Papers/grassojm.pdf)
records that the integral cohomology ring of a quaternionic Grassmannian is
the degree-doubled ring of the corresponding complex Grassmannian.  Pieri's
formula gives \(\sigma_1^2=\sigma_2+\sigma_{1,1}\), with the terms outside
the relevant rectangle omitted; this is nonzero as soon as the projective
line case is left.  These are classical Grassmannian facts.  No novelty is
claimed for them separately.

The theorem is conditional on globally labelled \(C^1\) full-slack
factors and on the absence of active zero-capacity ray terms.  It is a
formulation-capacity statement, not an extension-complexity result for
arbitrary nonsmooth lifts and not an IPM/QIPM iteration lower bound.

## Audit record

An independent hostile audit checked the balanced-rank equality step, the
odd-order range/kernel convention, the support-map differential and global
injectivity, the real Grassmannian fundamental group (including
\(\operatorname{Gr}_2(\mathbb R^4)\)), the complex and quaternionic
Schubert-square obstruction, the product-of-spheres indecomposable quotient,
and the order-two Lorentz attainments.  No mathematical gap was found.
