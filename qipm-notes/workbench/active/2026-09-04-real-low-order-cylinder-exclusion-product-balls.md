# Cylinder integrability excludes the last real low-order saturation cases

Status: Proved; independently hostile-audited twice  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

Let

\[
 C=\prod_{a=1}^h B_2^{s_a},\qquad
 M=\prod_{a=1}^h S^{p_a},\qquad p_a=s_a-1\geq1,
 \qquad n=\sum_a p_a.                                      \tag{1}
\]

Suppose the full extreme-row slack family has globally labelled
\(C^1\) factors over finitely many real, complex, or quaternionic
Hermitian PSD blocks and finitely many scalar rays:

\[
 1-x_a^Tz
 =\sum_i\operatorname {Re}\operatorname {tr}
       \bigl(X_i(x)Y_i^a(z)\bigr)
   +\sum_j\alpha_j(x)\beta_j^a(z),                         \tag{2}
\]

where all matrix and scalar factors are positive semidefinite or
nonnegative.  For a matrix block over \(\mathbb F_i\), put

\[
 a_i=\dim_{\mathbb R}\mathbb F_i,qquad
 c_i=a_i\left\lfloor {r_i^2\over4}\right\rfloor.          \tag{3}
\]

Then equality in the curvature-capacity bound

\[
                         \sum_i c_i=n                           \tag{4}
\]

is possible only if every positive block has order two and

\[
 \{p_a:a\in[h]\}
 =\biguplus_i
 \begin{cases}
   \{1\},&(\mathbb F_i,r_i)=(\mathbb R,2),\\
   \{2\},&(\mathbb F_i,r_i)=(\mathbb C,2),\\
   \{4\},&(\mathbb F_i,r_i)=(\mathbb H,2).
 \end{cases}                                               \tag{5}
\]

Thus the topology-compatible real order-three and order-four cases do
not occur for the full product-ball slack, even when arbitrary finitely
many active ray factors are present.  If an order-three or order-four
real block occurs, or if (5) fails, integrality sharpens (4) to

\[
                         \sum_i c_i\geq n+1.                    \tag{6}
\]

This closes the two exceptions left by the support-covering theorem in
[Active rays leave only two low-order real topological saturation
exceptions](2026-09-04-hermitian-product-ball-active-ray-covering.md).
The proof uses full-slack cylinder identities and is therefore stronger
in hypotheses than that theorem's purely topological final step.

## 1. What capacity equality already supplies

At a simultaneous contact \(z=x_a\), every summand in (2) vanishes.
The ray terms have zero mixed derivative on the contact tangent spaces.
Equality in (4) therefore makes every positive matrix block strictly
complementary with constant balanced ranks, and the normalized support
maps assemble into a finite covering

\[
 \Pi:M\longrightarrow
 \prod_i\operatorname {Gr}_{\lfloor r_i/2\rfloor}
                      (\mathbb F_i^{r_i}).                  \tag{7}
\]

The cited covering theorem excludes every complex and quaternionic order
above two and every real order above four.  It also identifies the
universal covers of the remaining targets as

\[
\begin{array}{c|c}
(\mathbb F,r)&\text{universal-cover factor}\\ \hline
(\mathbb R,2)&\mathbb R,\\
(\mathbb R,3),(\mathbb C,2)&S^2,\\
(\mathbb R,4)&S^2\times S^2,\\
(\mathbb H,2)&S^4.
\end{array}                                                \tag{8}
\]

The lift of (7) is a diffeomorphism between the universal covers.  In
degree two, a ring isomorphism between products of sphere cohomology
rings sends the generators by a signed permutation.  Indeed, if
\(u_1,\ldots,u_m\) are the degree-two sphere generators, then

\[
 \left(\sum_jb_ju_j\right)^2
       =2\sum_{j<k}b_jb_k u_ju_k,                           \tag{9}
\]

so a primitive square-zero class is exactly \(\pm u_j\).  Consequently
each surviving target \(S^2\) ruling is assigned to a distinct source
\(S^2\).  The degree-four indecomposable quotient similarly assigns every
target \(S^4\) to a distinct source \(S^4\).  Each target circle is nonconstant along
at least one source circle because the map on fundamental groups has
finite-index image.

We use only this assignment and not a product decomposition of the
covering map.

## 2. The cylinder lemma

Fix a matrix block \(i\), a row \(d\), and a row contact \(z=x_d\).
Termwise nonnegativity in (2) gives

\[
                         X_i(x)Y_i^d(x_d)=0.               \tag{10}
\]

Hold \(x_d\) fixed and vary any unrelated source coordinate \(x_a\),
\(a\ne d\).  If

\[
                         W=\operatorname {Ran}Y_i^d(x_d),  \tag{11}
\]

then (10) says

\[
                         W\subseteq\ker X_i(x)             \tag{12}
\]

along the whole \(x_a\)-cylinder.  Thus a nonzero unrelated row factor
forces the block support map, restricted to that source sphere, into the
locus of supports whose orthogonal complements contain one fixed nonzero
subspace.

### Real order three

The balanced primal rank is one or two, and the normalized support target
is \(\mathbb{RP}^2\).  If the primal rank is two, any nonzero \(W\) in
its one-dimensional kernel makes the kernel support constant.  If the
primal rank is one, its range line lies in \(W^\perp\).  For
\(\dim W=1\), this confines the image to
\(\mathbb{RP}(W^\perp)\cong\mathbb{RP}^1\); for \(\dim W=2\), it
makes the image constant.  In either case the lifted restriction
\(S^2\to S^2\) has degree zero.

It follows that if an order-three block's target \(S^2\) is assigned to
source \(a\), then

\[
                         Y_i^d\equiv0\qquad(d\ne a).       \tag{13}
\]

Otherwise (12) would contradict the nonzero, in fact primitive, degree
on its assigned source.

### Real order four

Here the primal and dual ranks are both two and the oriented target is

\[
             \operatorname {Gr}_2^+(\mathbb R^4)
                         \cong S^2_+\times S^2_-.          \tag{14}
\]

Its two ruling classes are assigned to two distinct source \(S^2\)
factors, say \(a\) and \(b\).  Suppose an unrelated row factor is
nonzero, so that (12) holds.  If \(\dim W=2\), the range plane is
constant.  If \(\dim W=1\), all range planes lie in the fixed
three-space \(W^\perp\), hence in

\[
             \operatorname {Gr}_2^+(W^\perp)\cong S^2.    \tag{15}
\]

Under the Hodge decomposition in (14), the inclusion (15) is the graph
of an isometry \(S^2_+\to S^2_-\).  It therefore has homology class
\((1,1)\) or \((1,-1)\), up to signs and multiplicity.  A restriction
representing one assigned ruling has class \((\pm1,0)\) or
\((0,\pm1)\), so it cannot factor through (15).

Apply this first by varying source \(a\).  It gives
\(Y_i^d\equiv0\) for every \(d\ne a\), in particular for \(d=b\).
Varying source \(b\) gives the same conclusion with \(a,b\) exchanged,
so \(Y_i^d\equiv0\) for every row \(d\).  This contradicts the positive
balanced dual rank forced by equality.  Hence

\[
                         \boxed{\text{no real order-four block occurs}.}
                                                               \tag{16}
\]

For completeness, the Hodge assertion used above is elementary.  An
oriented plane with unit simple bivector \(\omega\) maps to the normalized
self-dual and anti-self-dual parts \((\omega_+,\omega_-)\).  If the plane
lies in \(W^\perp\), the three-dimensional Hodge star on \(W^\perp\)
identifies these two components by an orthogonal map.  The two projections
of (15) therefore both have degree \(\pm1\).

## 3. An order-three block would isolate one forbidden ball factor

Assume an order-three real block \(i\) remains, assigned to a source
\(a\) with \(p_a=2\).  Equation (13) says this block serves no other row.
We next show that no other positive block serves row \(a\).

After (16), every other target factor in (8) is assigned to one source.
If that source is a sphere of dimension two or four, distinctness of the
indecomposable assignments makes it different from \(a\).  If it is a
circle, its support is nonconstant along at least one source circle,
again different from \(a\).  Along that assigned or nonconstant source
cylinder, a nonzero \(Y_j^a(x_a)\) would be a fixed nonzero subspace of
every kernel by (12).  For an order-two Hermitian block, the complementary
kernel is one \(\mathbb F\)-line, so its normalized support would be
constant.  For another order-three block, the preceding order-three
argument gives the same contradiction.  Therefore

\[
                         Y_j^a\equiv0\qquad(j\ne i).       \tag{17}
\]

Fix all primal coordinates other than \(x_a\).  Row \(a\) of (2) now
restricts to

\[
 1-x_a^Tz
 =\operatorname {tr}\bigl(X_i(x_a)Y_i^a(z)\bigr)
   +\sum_j\widetilde\alpha_j(x_a)\beta_j^a(z),qquad x_a,z\in S^2.
                                                               \tag{18}
\]

The scalar factors remain nonnegative and \(C^1\).  At every contact,
ray terms have zero mixed derivative, so the single PSD block carries the
full rank-two tangent metric.  Its complementary ranks are one and two,
and its projective support map is a submersion.  Thus (18) satisfies the
hypotheses of
[The apparent \(\mathbb S_+^3\) saturation exception is
impossible](2026-09-04-psd3-saturation-exclusion.md), which rules it out.
Hence

\[
                         \boxed{\text{no real order-three block occurs}.}
                                                               \tag{19}
\]

Combining (16), (19), and the previously audited covering classification
proves (5)--(6).

## Scope and novelty boundary

The proof requires the full product-ball row identities (2), globally
labelled \(C^1\) factors, finitely many rays, and exact capacity equality.
It does not apply to an abstract covering of products of spheres, to an
unlabelled lift without a global selection, or to arbitrary smooth convex
bodies.  The order-three final step specifically uses the quadratic
three-ball affine-pencil obstruction.

The topology of real Grassmannians and the Hodge model
\(\operatorname {Gr}_2^+(\mathbb R^4)\cong S^2\times S^2\) are classical.
The cylinder-support incompatibility and its use to close the two
product-ball formulation exceptions appear to be new, but no priority
claim is made without a dedicated literature search.

## Independent hostile audits

Three independent audits reconstructed the proof without assuming that
the lifted covering splits as a product.  They checked that primitive
square-zero degree-two classes assign the two order-four rulings to
distinct literal source-sphere slices.  They also verified that
\(\operatorname {Gr}_2^+(W^\perp)\) has class
\((\pm1,\pm1)\) in \(S^2\times S^2\), so it cannot carry either assigned
ruling.  Applying the two assigned cylinders therefore deletes every row
factor of an order-four block.

For order three, the audits checked both balanced-rank conventions and
the deletion of every nonassigned contribution, including real order-two
circle targets via a source-circle slice of nonzero winding.  After fixing
the other primal coordinates, the remaining identity has exactly one
saturated \(\mathbb S_+^3\) block and finitely many nonnegative \(C^1\)
ray factors.  This matches every hypothesis of the independently audited
one-ball impossibility theorem.  No correction was found.
