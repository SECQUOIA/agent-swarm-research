# Selection-free one-channel rigidity for every symmetric cone

Status: Core theorem and metric corollary independently hostile-audited
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the stated theorem and scope

## Result

Let \(\mathcal K=\prod_iK_i\) be a finite repeatable dictionary of simple
symmetric cones, together with optional nonnegative rays.  Write \(V_i\)
for the Euclidean Jordan algebra of \(K_i\), \(r_i\) for its rank, and
\(a_i\) for its Peirce constant.  Set
\[
                  B=\max_i a_i(r_i-1).                         \tag{1}
\]
Assume \(B>0\).
Suppose \(B_2^s\), with
\[
                         s-1=B,                                \tag{2}
\]
has an arbitrary finite affine lift by factors from this dictionary.
Reduce to the minimal product-cone face and assume relative Slater.
For the standard product Jordan log-determinant restricted to the lifted
affine slice,
\[
 \boxed{\displaystyle
 \nu_{\rm std,slice}=1
 \quad\Longleftrightarrow\quad
 \text{the dictionary contains a spin factor }Q_{B+2}.}        \tag{3}
\]
If no such factor is available, the exact value is two.

Thus selection-free one-channel equality is impossible not only for
non-spin real, complex, and quaternionic PSD factors, but also for the
exceptional Albert cone \(H_+^3(\mathbb O)\): at its critical capacity
\(B=8(3-1)=16\), every affine lift of \(B_2^{17}\) has
\(\nu_{\rm std,slice}\geq2\).

No global primal or dual certificate selection is assumed.

## 1. Parameter one makes certificate fibers singleton rays

For \(v\in S^{s-1}\), let \(\mathcal D(v)\) be the nonempty convex fiber
of positive genuine normalized certificates satisfying
\[
             \langle X,Y\rangle=1-v^T\pi X
             \quad\text{on the whole affine slice}.             \tag{4}
\]
If \(\nu_{\rm std,slice}\leq1\), the determinant order along a segment
from any primal tuple over \(v\) to a relative-Slater tuple gives total
primal Jordan nullity at most one.  Complementarity in (4) therefore
gives total Jordan rank at most one for every \(Y\in\mathcal D(v)\).

The midpoint of two rank-one positive tuples supported on different
extreme rays or different product factors has total rank two.  Convexity
therefore puts the whole fiber on one product-cone ray, and normalization
in (4) fixes its scalar:
\[
                         \mathcal D(v)=\{Y(v)\}.                 \tag{5}
\]
For a fixed relative-Slater tuple \(X^\circ\),
\[
 \langle X^\circ,Y(v)\rangle=1-v^T\pi X^\circ
   \in[1-\|\pi X^\circ\|,1+\|\pi X^\circ\|].                    \tag{6}
\]
Strict positivity of \(X^\circ\) in every reduced factor makes the
singleton field uniformly bounded and bounded away from zero.  Closed
graph then proves continuity.  Its active factor label is locally
constant and hence constant on the connected sphere.

## 2. Primitive-ray topology

Let \(K_j\) be the fixed active factor.  Projectivizing the unique
rank-one certificate gives a continuous map
\[
             \Phi:S^B\longrightarrow\mathcal P(V_j),            \tag{7}
\]
where \(\mathcal P(V_j)\) is the compact manifold of primitive Jordan
rays.  The map is injective: equal rays make the two certificates
positive scalar multiples, and comparison of the normalized constant
coefficient in (4) fixes the scalar and then \(v\).

For every simple EJA,
\[
                    \dim_{\mathbb R}\mathcal P(V_j)
                       =a_j(r_j-1)\leq B.                        \tag{8}
\]
Covering dimension and invariance of domain force equality in (8) and a
homeomorphism
\[
                       S^B\cong\mathcal P(V_j).                 \tag{9}
\]
The classification of simple EJAs lists these primitive-ray manifolds:
\[
\begin{array}{c|c}
V_j&\mathcal P(V_j)\\ \hline
H_r(\mathbb R)&\mathbb RP^{r-1}\\
H_r(\mathbb C)&\mathbb CP^{r-1}\\
H_r(\mathbb H)&\mathbb HP^{r-1}\\
\text{spin factor }Q_{m+2}&S^m\\
H_3(\mathbb O)&\mathbb OP^2 .
\end{array}                                                     \tag{10}
\]
Among positive-dimensional entries, the manifold is a sphere exactly
for a spin factor; the familiar
\(\mathbb RP^1,\mathbb CP^1,\mathbb HP^1\) cases are themselves the
rank-two spin factors.  For higher projective spaces, fundamental group
or intermediate cohomology excludes a sphere.  In particular
\(\mathbb OP^2\) has nonzero \(H^8\), unlike \(S^{16}\).
This proves the lower direction in (3).

## 3. Matching constructions

A spin factor \(Q_{B+2}\) has a trace-one affine slice equal to
\(B_2^{B+1}\), and the restricted standard barrier has parameter one.
This proves the exceptional direction of (3).

If no matching spin factor is present, choose a factor attaining (1), a
primitive idempotent \(c\), and put \(d=e-c\).  Its Peirce cross-space
\(V(c,\tfrac12)\) has real dimension \(B\).  The affine Peirce--Schur
slice
\[
                  x=s\,c+d+u,\qquad u\in V(c,\tfrac12),          \tag{11}
\]
satisfies, after a fixed normalization of the cross-space Euclidean norm,
\[
            x\succ0\quad\Longleftrightarrow\quad
            s>\|u\|^2,\qquad
            \det x=s-\|u\|^2.                                  \tag{12}
\]
It therefore handles \(B\) ball coordinates with one scalar perspective
variable.  A second copy of the same repeatable nonray factor, restricted
to any one-dimensional Peirce cross-space, handles the final coordinate
through a second quadratic perspective.  With the two perspective variables
summing to one, the restricted standard barrier is a sum of two
one-parameter paraboloid barriers and has exact parameter two.  This
matches the lower bound: restriction gives the upper bound two, while a
boundary point with both quadratic perspective slacks zero makes both
determinants vanish linearly along a segment to the interior, giving
boundary order two.

## 4. Additive product theorem

The obstruction adds across source balls.  Suppose the dictionary has no
matching \(Q_{B+2}\), and let an arbitrary affine lift represent
\((B_2^{B+1})^b\).  Then there are genuine pure-row certificates
\(Y^1,\ldots,Y^b\) at one simultaneous contact such that every positive
aggregate obeys
\[
 \boxed{\displaystyle
 \sum_i\operatorname{rank}_J\!
       \left(\sum_{d=1}^b\lambda_dY_i^d\right)\geq2b
       \quad(\lambda_d>0).}                                    \tag{13}
\]
Every primal tuple in the final simultaneous-contact fiber has total
Jordan nullity at least \(2b\).  Hence the exact selection-free standard
restricted-barrier value for this product is \(2b\).

Choose source contacts sequentially.  If \(c_i^{d-1}\) is the join of
the support idempotents of certificates already chosen in factor \(i\),
compress the full original row-\(d\) certificate fiber into the
complementary face by
\[
                Y_i\longmapsto P(e_i-c_i^{d-1})Y_i.             \tag{14}
\]
Whole-cylinder complementarity preserves the normalized row slack.
Relative Slater uniformly bounds the original fibers, so the compressed
images are nonempty compact convex closed-graph families.  Reduce the
remaining cylinder sublift to its minimal face.  All surviving primitive
capacities are at most \(B\), and a capacity-\(B\) face still cannot be a
spin factor under the hypothesis; for example, an Albert rank-two face
has capacity \(8<16\).  The one-ball
theorem says that some image certificate has total rank at least two:
otherwise every image fiber would be a continuous rank-one singleton and
would produce the forbidden primitive-ray embedding.

For every symmetric cone, Peirce support compression satisfies
\[
 \operatorname{rank}_J(P(e-c)y)
   =\operatorname{rank}_J(c\vee\operatorname{supp}y)
       -\operatorname{rank}_Jc.                                \tag{15}
\]
Thus each stage adds at least two to the total support join.  The support
of a positive aggregate is the join of the individual supports, proving
(13).  Final-fiber complementarity gives the nullity statement, and
boundary determinant order gives the barrier lower bound.  Independent
two-group constructions from Section 3 attain \(2b\).

Equation (13) is an additive existence theorem for selected pure-row
certificates.  It does not assert that the minimum rank over the full
aggregate-objective certificate fiber is additive.

### QIPM-facing metric corollary

Fix positive weights \(\lambda_d\) in (13), use the selected aggregate as
the optimization objective, and put
\[
 Q=\sum_i\operatorname{rank}_J
       \left(\sum_{d=1}^b\lambda_dY_i^d\right)\geq2b.
\]
For any fixed interior reference point \(X^c\), let \(\Delta_c>0\) be the
exposed-minor scale of this aggregate slack. The path-independent
[exposed-rank Dikin theorem](2026-09-04-symmetric-cone-exposed-rank-dikin-lower-bound.md)
gives, for every lifted feasible point of objective gap at most
\(0<\epsilon<\Delta_c\),
\[
 d_F\bigl(X^c,\{\operatorname{gap}\leq\epsilon\}\bigr)
 \geq \sqrt Q\log\frac{\Delta_c}{\epsilon}
 \geq \sqrt{2b}\log\frac{\Delta_c}{\epsilon}.            \tag{16}
\]
Thus a trajectory starting within distance \(D_0\) of \(X^c\), whose
counted rounds move standard-barrier distance at most \(D\), needs
\[
 T\geq
 \frac{\bigl[\sqrt{2b}\log(\Delta_c/\epsilon)-D_0\bigr]_+}{D}.
                                                               \tag{17}
\]
For at most \(m\) feasible Dikin chords of starting local norm at most
\(\eta<1\) per round, one may take
\(D=m\log(1/(1-\eta))\).

The coefficient is sharp at the exposed-rank level: the separate
two-group Peirce--Schur construction has aggregate rank \(2b\) at a
generic product support and standard restricted parameter \(2b\). If a
matching spin factor is available, separate direct spin lifts instead
have parameter and generic aggregate rank \(b\), giving the comparison
scale \(\sqrt b\). Equations (16)--(17) are geometric iteration
obstructions for the fixed standard Jordan barrier under bounded
intrinsic movement. They are not oracle-query or runtime lower bounds for
arbitrary QIPMs, custom barriers, infeasible trajectories, or rounds with
unbounded barrier-metric displacement.

## 5. Scope and prior-art boundary

The theorem concerns the standard product Jordan log-determinant after
restriction to an actual affine lift.  It is not a result for arbitrary
custom barriers and does not by itself lower-bound quantum queries or
runtime.

The Hermitian special case is proved separately in
[Selection-free Hermitian one-channel
rigidity](2026-09-04-selection-free-hermitian-one-channel-rigidity.md).
The additional point here is that the primitive-ray classification makes
the same selection-free obstruction uniform over every simple symmetric
cone, including the exceptional Albert factor.  The ingredients are
classical; see the Peirce and primitive-idempotent treatment in
[Faraut and Korányi](https://doi.org/10.1093/oso/9780198534778.003.0004).
The affine-lift barrier synthesis appears unlocated, and
priority is not claimed.

## Audit checklist

1. Verify that Jordan rank-one midpoint convexity makes every normalized
   certificate fiber a singleton.
2. Check uniform boundedness and continuity after minimal-face reduction.
3. Check the dimension and topology of every primitive-ray manifold,
   especially \(\mathbb OP^2\).
4. Verify the Peirce--Schur slice (11)--(12), including determinant
   normalization in spin and Albert factors.
5. Check that the two-group construction has restricted parameter exactly
   two and works for a repeatable dictionary.
6. Check Peirce support compression (15), positive-aggregate support
   joins, and the precise additive-existence quantifier in (13).
7. Check that (16)--(17) use the same selected aggregate slack as (13),
   and preserve the bounded-movement scope of the exposed-rank theorem.

## Independent hostile audit

The audit verified that parameter one bounds the determinant order of
every boundary tuple, so every genuine certificate has total Jordan rank
one.  Convexity and normalization make each fiber a singleton ray;
relative Slater supplies the uniform bound needed for continuity.  The
primitive-ray manifolds and dimensions in (10) are exactly the real,
complex, quaternionic, spin, and octonionic projective spaces shown.
Only the spin cases are spheres; in particular
\(H^8(\mathbb OP^2)\ne0\), excluding \(S^{16}\).

It also checked the Peirce--Schur formula (11)--(12), including the Albert
case and the fixed cross-norm normalization.  The repaired upper
construction uses a second copy of the same repeatable nonray factor for
the final quadratic perspective; a ray alone would not suffice.  Product
restriction gives parameter at most two, and simultaneous linear
vanishing of both perspective determinants gives the matching boundary
order two.

For the additive theorem, the support identity (15) follows from the
orthomodular rank identity for Peirce faces and holds also in the Albert
algebra.  Whole-cylinder complementarity preserves the next-row slack
after compression.  Minimal-face reduction cannot introduce a hidden
capacity-\(B\) spin face, positive aggregate supports are joins, and the
increments telescope to \(2b\).  The audit confirmed the stated
existence quantifier and returned **PASS**.

A separate hostile audit checked the QIPM-facing corollary (16)--(17).
The exposed-minor scale \(\Delta_c\) and rank \(Q\) belong to the same
selected positive aggregate certificate, so the path-independent
\(\sqrt Q\log(\Delta_c/\epsilon)\) distance theorem applies without a
quantifier swap.  The conversion to bounded intrinsic moves and to at most
\(m\) forward Dikin chords per round uses the correct denominator
\(m\log(1/(1-\eta))\).  The audit returned **PASS** and confirmed that the
statement is metric-geometric only: it is neither an arbitrary-barrier nor
a quantum-query/runtime lower bound.
