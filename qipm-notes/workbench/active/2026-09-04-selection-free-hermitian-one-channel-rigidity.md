# Selection-free Hermitian one-channel rigidity

Status: One-ball and additive product theorems independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High; priority not assessed

## Result

Let \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), put
\(a=\dim_{\mathbb R}\mathbb F\), and fix an order cap \(R\geq2\).  Suppose
that \(B_2^s\) has a finite affine lift over a product of cones
\(H_+^{r_i}(\mathbb F)\), \(r_i\leq R\), and nonnegative rays.  Reduce the
lift to its minimal product-cone face and assume relative Slater.

In the one-channel divisible regime

\[
                         s-1=a(R-1),                         \tag{1}
\]

the restricted standard product log-determinant satisfies

\[
 \boxed{\nu_{\rm std,slice}\geq2}                            \tag{2}
\]

unless \(R=2\) and \(s=a+1\).  In that exceptional case
\(H_+^2(\mathbb F)\) is the rank-two spin factor and a trace-one slice
gives \(B_2^{a+1}\) with parameter one.  Thus the exact selection-free
standard-barrier value in (1) is

\[
 \begin{cases}
  1,&R=2,\ s=a+1,\\
  2,&R>2.
 \end{cases}                                                \tag{3}
\]

No global primal or dual selection is assumed.  The obstruction uses the
entire convex fiber of normalized support certificates.  Consequently,
the bounded projection-singular gap left by the general Hermitian cap
theorem can occur only in the divisible cases
\(s-1=q a(R-1)\) with \(q\geq2\).

## 1. Standard form and boundary orders

Write the affine lifted slice as

\[
 \mathcal S=\{X=(X_i)_i\in K:\ \mathcal A X=b,\quad
                                  \pi X=x\},              \tag{4}
\]

where \(K\) is the stated Hermitian-product cone after minimal-face
reduction.  Relative Slater supplies \(X^\circ\in\operatorname{ri}K\)
whose projection \(x^\circ\) lies in \(\operatorname{int}B_2^s\).
For a support \(v\in S^{s-1}\), let \(\mathcal D(v)\) be the set of
positive dual tuples satisfying the genuine normalized identity

\[
             \langle X,Y\rangle=1-v^T\pi X
                    \qquad\text{on the whole affine slice}.       \tag{5}
\]

Finite-dimensional conic duality and relative Slater make
\(\mathcal D(v)\) nonempty.

Suppose for contradiction that \(\nu_{\rm std,slice}\leq1\).  If
\(X\in\mathcal S\) projects to \(v\), the segment from \(X^\circ\) to
\(X\) lies in the relative interior for every positive segment
parameter.  The product determinant vanishes at \(X\) to order
\(\sum_i\operatorname{nullity}_{\mathbb F}X_i\).  The one-dimensional
barrier-gradient inequality therefore gives

\[
              \sum_i\operatorname{nullity}_{\mathbb F}X_i\leq1
       \qquad\text{for every }X\text{ over every }v.       \tag{6}
\]

For any \(Y\in\mathcal D(v)\), (5) vanishes on every such \(X\).
Self-duality and termwise nonnegativity imply blockwise complementarity,
so

\[
              \operatorname{rank}_{\mathbb F}Y
                 :=\sum_i\operatorname{rank}_{\mathbb F}Y_i\leq1.
                                                               \tag{7}
\]

## 2. Convexity makes every certificate fiber a singleton

The fiber \(\mathcal D(v)\) is convex.  If it contained two rank-one
tuples supported on different Hermitian lines or in different product
blocks, their midpoint would have total rank two, contradicting (7).
Thus the whole fiber lies on one positive rank-one ray.  Two distinct
points on that ray cannot both satisfy (5): their images under the linear
coefficient map would be distinct positive multiples of the same
functional, whereas both equal the nonzero normalized functional
\(1-v^Tx\).  Hence

\[
                            \mathcal D(v)=\{Y(v)\}.        \tag{8}
\]

These singleton fibers vary continuously.  Indeed,

\[
       \langle X^\circ,Y(v)\rangle=1-v^Tx^\circ
          \in[1-\|x^\circ\|,1+\|x^\circ\|].              \tag{9}
\]

Because every block of \(X^\circ\) is positive definite in the reduced
face, (9) uniformly bounds \(Y(v)\).  Any limit of certificates along
\(v_j\to v\) remains positive and satisfies (5), hence equals the unique
\(Y(v)\).  This proves continuity.  The positive lower bound in (9)
also prevents the certificate from passing through zero, so its unique
active product-block label is locally constant and therefore constant on
the connected sphere.

## 3. The projective embedding contradiction

Let the fixed active block have order \(r\leq R\).  Sending a support to
the \(\mathbb F\)-line carrying its rank-one certificate gives a continuous
map

\[
                 \Phi:S^{s-1}\longrightarrow
                           \mathbb F P^{r-1}.              \tag{10}
\]

It is injective.  If \(\Phi(v)=\Phi(w)\), then \(Y(v)\) and \(Y(w)\)
are positive multiples of the same rank-one projector.  Applying the
coefficient map in (5), and comparing the constant coefficient one,
forces the multiplier to be one and then \(v=w\).

Compactness of the source makes \(\Phi\) a topological embedding.  Covering
dimension gives

\[
       s-1\leq\dim_{\mathbb R}\mathbb F P^{r-1}
             =a(r-1)\leq a(R-1)=s-1.                    \tag{11}
\]

Thus \(r=R\), and invariance of domain makes the image of (10) open in
\(\mathbb F P^{R-1}\).  It is also compact and hence closed, so connectedness
forces a homeomorphism

\[
                        S^{a(R-1)}\cong\mathbb F P^{R-1}. \tag{12}
\]

For \(R>2\), this is impossible.  In the real case,
\(\pi_1(\mathbb RP^{R-1})\cong\mathbb Z/2\) while the sphere is simply
connected.  In the complex case, \(H^2(\mathbb CP^{R-1};\mathbb Z)\ne0\)
while \(H^2(S^{2(R-1)};\mathbb Z)=0\).  In the quaternionic case,
\(H^4(\mathbb HP^{R-1};\mathbb Z)\ne0\) while
\(H^4(S^{4(R-1)};\mathbb Z)=0\).  For \(R=2\), the familiar identities
\(\mathbb RP^1\cong S^1\), \(\mathbb CP^1\cong S^2\), and
\(\mathbb HP^1\cong S^4\) are exactly the direct spin exceptions.
This proves (2).

## 4. Sharpness and scope

When \(R>2\), split the \(s=a(R-1)+1\) ball coordinates into one group of
size \(a(R-1)\) and one scalar group.  A Hermitian Schur block of order
\(R\) handles the first group and an order-two
\(\mathbb F\)-Hermitian Schur block restricted to one real coordinate
handles the last coordinate.  The standard restricted parameters add to
two.  When \(R=2\), the direct trace-one spin slice has parameter one.
These constructions prove (3).

The theorem concerns the standard product Jordan log-determinant after
affine restriction.  It does not lower-bound arbitrary custom barriers or
unrestricted quantum interior-point iterations.  Rays cause no exception:
a rank-one ray certificate has a zero-dimensional projective target and
cannot contain an embedded positive-dimensional support sphere.

### Mixed-dictionary corollary

The proof is unchanged for a finite, repeatable dictionary of real,
complex, and quaternionic Hermitian block types.  Put

\[
 B=\max_i\bigl\{a_i(R_i-1)\bigr\},\qquad
 a_i=\dim_{\mathbb R}\mathbb F_i,
\]

and suppose \(s-1=B\).  A hypothetical parameter-one lift again selects
one fixed rank-one block and embeds \(S^B\) into
\(\mathbb F_iP^{r_i-1}\).  Dimension forces
\(a_i(r_i-1)=B\), and invariance of domain forces this projective space to
be a sphere.  Hence \(r_i=2\) and \(B=a_i\in\{1,2,4\}\).  Therefore the
mixed-dictionary value is one exactly when the dictionary contains the
matching direct spin factor \(Q_{B+2}\); otherwise the grouped value two
is optimal.  This corollary also permits arbitrary scalar rays.

## 5. Additive product theorem by global-certificate compression

The same obstruction adds across source rows.  Let

\[
                         C=(B_2^s)^b,\qquad
                         s-1=a(R-1),\quad R>2,             \tag{13}
\]

and let an arbitrary finite affine lift of \(C\) use
\(\mathbb F\)-Hermitian blocks of orders at most \(R\), together with
rays.  Then there are genuine pure-row support certificates
\(Y^1,\ldots,Y^b\) at one simultaneous contact
\((u_1,\ldots,u_b)\) such that, for every \(\lambda_d>0\),

\[
 \boxed{
  \sum_i\operatorname{rank}_{\mathbb F}
       \left(\sum_{d=1}^b\lambda_dY_i^d\right)\geq2b.
 }                                                           \tag{14}
\]

Every primal tuple in the final simultaneous-contact fiber satisfies

\[
 \boxed{\sum_i\operatorname{nullity}_{\mathbb F}X_i\geq2b.}   \tag{15}
\]

Consequently the exact unrestricted affine-lift standard-barrier value is

\[
                         \nu_{\rm std,slice}^{\min}=2b.       \tag{16}
\]

Here is the compression argument.  The proof in Sections 1--3 yields the
following intrinsic one-ball lemma: if nonempty compact convex certificate
fibers over \(S^{s-1}\) satisfy the whole-ball slack identity and every
block order is at most \(R\), then some fiber contains a certificate of
total rank at least two.  Otherwise convexity makes every fiber a
continuous rank-one singleton and repeats the impossible projective
embedding (10)--(12).

Choose the source contacts successively.  After choosing rows
\(1,\ldots,d-1\), set

\[
 W_i^{d-1}=\sum_{e<d}\operatorname{Ran}_{\mathbb F}Y_i^e,\qquad
 P_i^{d-1}=P_{(W_i^{d-1})^\perp}.                         \tag{17}
\]

Pure-row complementarity puts every primal tuple on the entire remaining
source cylinder in the compressed faces
\(P_i^{d-1}H_+^{r_i}(\mathbb F)P_i^{d-1}\).  Compress the whole original
row-\(d\) certificate fiber by \(Y_i\mapsto P_i^{d-1}Y_iP_i^{d-1}\).
Relative Slater uniformly bounds the original normalized certificates,
so these image fibers remain nonempty, compact, convex, and closed-graph.
They satisfy the genuine row-\(d\) ball slack identity on the whole future
cylinder.  The one-ball lemma therefore selects \(u_d\) and an original
certificate \(Y^d\) whose compressed total rank is at least two.

For a positive Hermitian matrix \(Y=CC^*\) and an orthogonal projection
\(P=P_{W^\perp}\),

\[
 \operatorname{rank}_{\mathbb F}(PYP)
   =\dim_{\mathbb F}(W+\operatorname{Ran}_{\mathbb F}Y)
      -\dim_{\mathbb F}W.                                  \tag{18}
\]

Thus each stage adds at least two dimensions to the total range span.
After \(b\) stages its dimension is at least \(2b\).  Positive Hermitian
range additivity gives (14), and complementarity of every final primal
fiber with every selected pure-row certificate gives (15).  Boundary
determinant order proves the lower bound in (16).  Separate two-group
Hermitian Schur lifts attain two per source, proving equality.

The same proof works sourcewise for a repeatable mixed Hermitian
dictionary in the critical regime of the mixed-dictionary corollary,
provided no source has a matching direct rank-two spin factor.  Each
compressed one-ball step either has strictly less projective capacity than
the source sphere or reaches equality in a non-spherical projective space,
so it again contributes two new range dimensions.  Here “contains” a
matching spin includes permitting the corresponding order-two face of a
larger same-field block.

## Audit checklist

1. Check that \(\nu\leq1\) gives (6) for every boundary tuple, not merely
   a selected tuple.
2. Check that convexity plus total rank at most one makes each normalized
   certificate fiber a singleton.
3. Check the uniform boundedness/closed-graph continuity argument after
   minimal-face reduction.
4. Check injectivity of the projective range map and all three projective
   space exclusions.
5. Check the two-block grouped upper construction and the ray-factor edge
   case.
6. Check the all-field sequential compression identities (17)--(18) and
   the mixed-dictionary extension.

## Independent hostile audit

The audit checked that the boundary determinant-order test applies to
every tuple in every boundary fiber.  It then verified the decisive
fiber argument: blockwise complementarity bounds every normalized
certificate by total rank one, convexity forces the entire certificate
fiber onto one product-cone ray, and the normalized affine functional
fixes its scalar.  Minimal-face Slater gives a uniform trace bound and
rules out a nonzero positive zero-functional recession, so the singleton
field is globally continuous.

The audit also checked that the nonzero rank-one field cannot change
product-block labels, that equal projective ranges force equal normalized
support functionals, and hence that (10) is injective.  Dimension plus
invariance of domain gives (12); the fundamental-group/cohomology
exclusions leave exactly the three \(R=2\) projective-line spheres.  The
two-block grouped upper construction and the ray-factor case also pass.
The audit returned **PASS** with no correction.

The additive extension in Section 5 received a separate hostile audit.
After earlier source rows are fixed at contact, every primal tuple on the
remaining cylinder annihilates the accumulated certificate ranges.
Consequently compression by (17) preserves the exact row-\(d\) slack
identity.  The original relative-Slater tuple uniformly bounds the
normalized certificate fibers before compression, so their images are
nonempty compact convex closed-graph fibers; a zero image cannot represent
the nonzero normalized row slack.  The intrinsic one-ball argument
therefore supplies compressed rank at least two.

For positive Hermitian matrices over all three fields,
\(\ker(PYP)=\ker(C^*P)\) when \(Y=CC^*\), which proves the range-increment
identity (18).  Also
\(\ker(\sum_d\lambda_dY_i^d)=\bigcap_d\ker Y_i^d\) for
\(\lambda_d>0\), so the accumulated span is exactly the aggregate range.
Final-fiber complementarity and determinant order then give (15)--(16).
The mixed-dictionary version uses only the same projective-capacity
dichotomy; excluding a matching rank-two spin face is precisely what
forces a two-unit increment.  The audit returned **PASS**.

A second, topology-only audit independently checked the dimension equality,
invariance-of-domain step, and the \(\pi_1/H^2/H^4\) exclusions.  It also
confirmed that the three projective lines are exactly the rank-two spin
exceptions.  It returned **PASS** with no correction.
