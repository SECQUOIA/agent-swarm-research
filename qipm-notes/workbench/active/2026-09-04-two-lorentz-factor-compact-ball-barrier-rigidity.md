# Two-factor compact rigidity closes the quotient-two Lorentz barrier seam

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High; the theorem is only for exactly two Lorentz factors

## Result

Fix \(a,b\geq1\). Let \(S\) be a bounded affine slice of

\[
                         Q_{a+2}\times Q_{b+2}
\]

which meets the interior of both factors, and suppose that an affine map
projects \(S\) exactly onto the \((a+b+1)\)-dimensional Euclidean ball
\(B_2^{a+b+1}\). Then the standard product Lorentz barrier restricted to
\(S\),

\[
       F(z_1,z_2)=-\log\det_J z_1-\log\det_J z_2,          \tag{1}
\]

satisfies

\[
                              \boxed{\nu(F)\geq3}.          \tag{2}
\]

The two-level norm-chain lift attains equality. Hence the exact standard
barrier value among compact full-Slater lifts of \(B_2^{a+b+1}\) using
exactly \(Q_{a+2}\times Q_{b+2}\) is three.

Taking \(a=b=c=d-2\) closes every quotient-two divisible case
\[
       s-1=2(d-2)
\]
for factor-count-minimal pure capped-Lorentz lifts. It does not yet exclude
a counterexample which uses more Lorentz factors or additional rays and
switches the two productive channels across projection-singular seams.
Such a formulation would use extra cone factors to lower, rather than
raise, the restricted standard-barrier parameter.

## 1. Homogenization inside the same product cone

Write the affine hull of \(S\) as \(A\subset\mathbb R^{a+b+4}\), and first
remove affine-variable kernels so that points of \(A\) are the two
displayed cone coordinates. Since
\(S=A\cap(Q_{a+2}\times Q_{b+2})\) is bounded and contains a
product-interior point, \(0\notin A\). If

\[
                         L=\operatorname {span}A,
\]

there is a linear functional \(\ell:L\to\mathbb R\) with

\[
                         A=\{z\in L:\ell(z)=1\}.           \tag{3}
\]

Moreover

\[
             \ell(z)>0\qquad
             (0\ne z\in C:=L\cap(Q_{a+2}\times Q_{b+2})). \tag{4}
\]

Indeed, a nonzero cone point with \(\ell=0\) would be a recession direction
of \(S\). If \(\ell(z)<0\), adding a suitable positive multiple of \(z\)
to a product-interior point of \(S\) would produce such a nonzero
\(\ell=0\) cone point. Thus \(C\) is exactly the cone over the compact base
\(S\).

Homogenizing the affine projection gives a linear map

\[
                         \Pi:L\longrightarrow\mathbb R^{a+b+2}
\]

such that

\[
                         \Pi(C)=Q_{a+b+2}.                 \tag{5}
\]

The first target coordinate is \(\ell\). In particular,

\[
                         \ker\Pi\cap C=\{0\}.              \tag{6}
\]

Because \(S\) projects onto an \((a+b+1)\)-dimensional body,
\(\dim L\geq a+b+2\). The next section excludes dimensions \(a+b+2\) and
\(a+b+4\). Therefore \(L\) is a hyperplane in
\(\mathbb R^{a+b+4}\).

## 2. The endpoint dimensions are impossible

Suppose first that \(\dim L=a+b+2\). Then (5) makes \(\Pi|_L\) a linear
isomorphism. In coordinates on \(L\), membership in \(C\) is given by two
Lorentz inequalities. Let \(f_i\) be the determinant quadratic of the
\(i\)-th cone coordinate. Every point on the boundary quadric of
\(Q_{a+b+2}\) makes at least one \(f_i\) vanish. The nondegenerate
quadratic defining \(Q_{a+b+2}\) is irreducible, so it divides one of
\(f_1,f_2\). Both have degree two. This is impossible: the matrix ranks of
\(f_1,f_2\) are at most \(a+2,b+2\), respectively, whereas the target
determinant has rank \(a+b+2>\max\{a+2,b+2\}\). Neither \(f_i\) vanishes
identically, because \(L\) contains a point interior in both product
factors.

Now suppose that \(L=\mathbb R^{a+b+4}\). Write

\[
                         \Pi(x,y)=P_1x+P_2y.               \tag{7}
\]

The cones \(P_1(Q_{a+2})\) and \(P_2(Q_{b+2})\) lie in \(Q_{a+b+2}\).
If \(r\) spans an extreme ray of \(Q_{a+b+2}\), write
\(r=P_1x+P_2y\) using (5). Extremality forces
every nonzero summand to lie on the ray of \(r\). Hence every extreme ray
of \(Q_{a+b+2}\) lies in

\[
                         \operatorname {Ran}P_1
                         \ \cup\ \operatorname {Ran}P_2. \tag{8}
\]

The two ranges have dimensions at most \(a+2\) and \(b+2\), both strictly
less than \(a+b+2\). But the irreducible light quadric of \(Q_{a+b+2}\)
cannot be contained in a union of two proper linear subspaces. This
contradicts (8).

## 3. Hyperplane classification and the product-sphere obstruction

We now have

\[
 C=(Q_{a+2}\times Q_{b+2})\cap
       \{(x,y):\langle \alpha,x\rangle+
                         \langle \beta,y\rangle=0\}.       \tag{9}
\]

If a linear functional on a Lorentz cone has no nonzero cone zero, it
belongs to the interior of the dual cone or to its negative. Since (9)
contains a point interior in both factors, if neither \(\alpha\) nor
\(\beta\) has a nonzero cone zero, then they have opposite definite signs.
Lorentz-cone
automorphisms and positive rescaling put (9) in the normal form

\[
 C_0=\{((t,u),(t,v)):t\geq\|u\|_2,\ t\geq\|v\|_2\},
 \quad u\in\mathbb R^{a+1},\ v\in\mathbb R^{b+1}.         \tag{10}
\]

This is the cone over \(B_2^{a+1}\times B_2^{b+1}\). Its nonzero proper
faces have dimensions one, \(a+2\), or \(b+2\): the base faces are
respectively

\[
 \{p\}\times\{q\},\qquad
 \{p\}\times B_2^{b+1},\qquad
 B_2^{a+1}\times\{q\}.                                   \tag{11}
\]

In particular, \(C_0\) has no two-dimensional face, and its projectivized
extreme-ray space is \(S^a\times S^b\).

For an extreme ray \(R\) of \(Q_{a+b+2}\), the inverse image

\[
                         C_0\cap\Pi^{-1}(R)                \tag{12}
\]

is a face of \(C_0\). Since \(\dim\ker(\Pi|_L)=1\), its linear span has
dimension at most two. It is nonzero by (5), so (11) forces (12) to be a
single extreme ray. After normalizing the target and source heights, the
unique inverse rays vary continuously: otherwise compactness and (6)
give a convergent subsequence whose limit violates uniqueness. We obtain
a continuous injection

\[
                          S^{a+b}\longrightarrow S^a\times S^b. \tag{13}
\]

Invariance of domain makes its image open, while compactness makes it
closed. The product is connected, so (13) would be a homeomorphism onto
\(S^a\times S^b\). This contradicts intermediate cohomology:
\[
 H^a(S^a\times S^b;\mathbb Z)\ne0,\qquad
 H^a(S^{a+b};\mathbb Z)=0.                               \tag{13a}
\]
Thus the definite-sign case (10) cannot project onto \(Q_{a+b+2}\).

It follows that \(\alpha\) or \(\beta\) has a nonzero zero on its Lorentz
cone. Such a zero may be chosen on an extreme ray: restrict the functional
to a compact spherical base of the corresponding Lorentz cone and use
either its boundary zero or the intermediate value theorem between
opposite signs. Without loss of generality choose

\[
                  0\ne x\in\operatorname {Ext}(Q_{a+2}),
                  \qquad\langle \alpha,x\rangle=0.         \tag{14}
\]

Then \((x,0)\) is an extreme ray of \(C\).

## 4. The forced third determinant power

By (4), the ray in (14) meets the compact base \(S\). At that point the
first Lorentz block is nonzero of Jordan rank one and nullity one, while
the second block is the cone vertex and has Jordan nullity two. A segment
from this point to a product-interior point therefore gives

\[
        \det_J z_1(\sigma)\det_J z_2(\sigma)
                    =\gamma\sigma^3+O(\sigma^4),
        \qquad \gamma>0.                                  \tag{15}
\]

Thus \(F(\sigma)=-3\log\sigma+O(1)\). The one-dimensional
barrier-gradient inequality forces \(\nu(F)\geq3\), proving (2).

For sharpness, split the \(a+b+1\) projected coordinates into
\(x_G\in\mathbb R^{a+1}\) and \(x_H\in\mathbb R^b\), and use

\[
       (t,x_G)\in Q_{a+2},\qquad (1,t,x_H)\in Q_{b+2}.     \tag{16}
\]

It projects exactly onto \(B_2^{a+b+1}\). Homogenization makes (1) a
four-logarithmically-homogeneous barrier restricted to a compact base, so
the standard base-restriction argument gives \(\nu\leq3\). At
\((x_G,x_H,t)=(0,e_1,0)\), the first block is zero and the second is a
nonzero boundary point, so (15) gives the reverse inequality. Hence the
exact value is three.

## 5. A compact affine seam model shows the remaining obstruction

Compactness, affine determinant structure, and the bound \(\nu=2\) do not
by themselves force a third determinant power. Consider the compact
full-Slater slice of two real \(2\times2\) PSD cones

\[
 X_1(x)=
 \begin{pmatrix}x&0\\0&1-x\end{pmatrix},\qquad
 X_2(x,t)=
 \begin{pmatrix}x+t&t\\t&1\end{pmatrix}.                  \tag{17}
\]

Its feasible set is

\[
       0\leq x\leq1,\qquad x+t-t^2\geq0,                  \tag{18}
\]

which is compact and has interior. The restricted standard barrier is

\[
       -\log\!\bigl(x(1-x)\bigr)-\log(x+t-t^2).            \tag{19}
\]

The first matrix ranges in a compact affine base of \(S_+^2\), and the
second in the affine base with bottom-right entry one. Each restricted
log-determinant has gradient parameter one. Explicitly, for
\[
 f_1(x)=-\log[x(1-x)],\qquad f_2(a,b)=-\log(a-b^2),
\]
their squared gradient norms in their Hessian metrics are
\[
 {f_1'(x)^2\over f_1''(x)}
 ={(1-2x)^2\over x^2+(1-x)^2}\leq1,
 \qquad
 \nabla f_2^T(\nabla^2f_2)^{-1}\nabla f_2=1.              \tag{19a}
\]
Restriction to the joint affine slice \(a=x+t,\ b=t\) cannot increase
the dual gradient norm, and therefore gives \(\nu\leq2\). At
\((x,t)=(0,0)\) or \((0,1)\), both matrices have nullity one, so the
determinant-order test gives \(\nu\geq2\). Thus (19) has exact parameter
two.

Over the seam \(x=0\), the feasible fiber is the interval \(0\leq t\leq1\).
Its interior has total nullity one, while its endpoints have total nullity
two. No block is zero anywhere on this seam. Locally its determinant is
the ideal switching model
\[
                         x\,[x+t(1-t)].                   \tag{20}
\]

This example is not a lift of \(B_2^3\). It proves that determinant order,
compactness, convex fibers, and local affine integrability cannot exclude
the equality-saving seam. The product-sphere target argument in Section 3
is essential.

## 6. What remains open

The proof uses the face lattice of a hyperplane section of exactly
\(Q_{a+2}\times Q_{b+2}\). Under a hypothetical parameter-two lift with
additional
cone factors, generic ball contacts still use exactly two nonzero boundary
channels, but their labels can change. At a singular support, a compact
fiber can realize the pattern (20) while a normalized dual channel
disappears. The two-factor hyperplane classification no longer applies.

Therefore a full solution of the bounded divisible case must either:

1. reduce every parameter-two multi-factor lift to an essential
   two-factor sublift; or
2. rule out active-label switching by using the global ball slack
   identities, not compactness or local determinant geometry alone.

The theorem above shows that any counterexample in the quotient-two regime
must be deliberately nonminimal in factor count.

## 7. Literature boundary and novelty caution

The construction side is classical. Ben-Tal and Nemirovski,
[*Lectures on Modern Convex Optimization*, Chapter
3](https://doi.org/10.1137/1.9780898718829.ch3), develop Lorentz-cone
modelling and recursive norm epigraphs. Vielma, Ahmed, and Nemhauser,
[*A Lifted Linear Programming Branch-and-Bound Algorithm for Mixed-Integer
Conic Quadratic Programs*](https://doi.org/10.1287/ijoc.1070.0256),
Section 3, explicitly decompose a high-dimensional Euclidean norm through a
tower of smaller Lorentz constraints. Thus the norm-chain lift (16), as a
construction principle, is not new.

The general lift framework is also established. Gouveia, Parrilo, and
Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://arxiv.org/abs/1111.3164), characterize proper cone
lifts by slack-operator factorizations. Fawzi,
[*On Representing the Positive Semidefinite Cone Using the Second-Order
Cone*](https://doi.org/10.1007/s10107-018-1233-0), formalizes
second-order-cone rank and proves a different SOC nonrepresentability
result for the real \(3\)-by-\(3\) PSD cone. Saunderson,
[*Limitations on the Expressive Power of Convex Cones without Long Chains
of Faces*](https://arxiv.org/abs/1902.06401), gives lift obstructions based
on neighborliness and face-chain length. Aubrun, La Piana, and
Müller-Hermes,
[*Factorization through Lorentz
cones*](https://arxiv.org/abs/2606.27825), study which positive linear maps
factor through direct sums of Lorentz cones. These sources do not classify
full-Slater affine slices of exactly two prescribed Lorentz factors that
project onto a larger Lorentz cone.

The optimal ambient barrier parameters of Lorentz cones and their products
follow from the classical symmetric-cone theory of Güler--Tunçel and
Cardoso--Vieira. Those results do not determine the gradient parameter after
restriction to a compact affine slice: in the present setting the ambient
product parameter is four, while the sharp restricted value is three.

A targeted primary-source search through 2026 did not locate a theorem
combining the endpoint-dimension exclusion, hyperplane-section
classification, and product-sphere obstruction used here. In particular,
no screened cone-lift paper turns uniqueness of inverse extreme rays into a
forbidden injection \(S^{a+b}\to S^a\times S^b\), nor derives from it the
forced order-three determinant degeneration and exact restricted barrier
value. The topological ingredients--invariance of domain and the
cohomology of a product of spheres--are standard and are not themselves
novel.

The conservative label is **candidate exact two-factor compact-rigidity
synthesis**. It is an exact result only for a bounded, full-Slater lift by
the two displayed Lorentz factors. It is not an SOC extension-complexity
lower bound for arbitrary numbers of factors, and it does not resolve the
multi-factor label-switching seam in Section 6. This is a targeted negative
screen, not an exhaustive priority determination.

## Audit checklist

1. Check that boundedness gives the strictly positive homogenizing
   functional (4) and the properness condition (6).
2. Check the irreducible-quadratic arguments excluding the two endpoint
   dimensions.
3. Verify the face dimensions of the cone over
   \(B_2^{a+1}\times B_2^{b+1}\) and the singleton inverse-ray argument.
4. Check the invariance-of-domain and cohomology contradiction in (13).
5. Check that (14) forces exact determinant order three on the compact
   base.
6. Verify the exact parameter and seam nullities in (17)--(20).

## Independent hostile audit

The audit independently reconstructed the homogenization. Boundedness
makes the base functional strictly positive on every nonzero point of
\(C=L\cap(Q_{a+2}\times Q_{b+2})\), so \(C\) is exactly the cone over
\(S\), and the homogenized projection is proper on cone rays. When
\(\dim L=a+b+2\), irreducibility of the target light quadric forces it to
divide one pulled-back determinant, contradicting the strict rank bounds
\(a+2,b+2<a+b+2\). When \(L\) is the full
\((a+b+4)\)-dimensional product space, extremality would put the whole
target light cone in the union of two proper linear ranges, which is
impossible.

In the remaining hyperplane case, definite opposite normal functionals
do give the cone over \(B_2^{a+1}\times B_2^{b+1}\). Its only nonzero
proper face dimensions are \(1,a+2,b+2\). Since an inverse image of a
target extreme ray has span dimension at most two, it is a unique source
extreme ray. Proper normalization makes the inverse continuous, hence
gives the claimed injection
\(S^{a+b}\hookrightarrow S^a\times S^b\). Invariance of domain would make
it a homeomorphism, contradicted by intermediate cohomology. In the other
hyperplane case an extreme cone zero produces \((x,0)\), with determinant
orders \(1+2=3\). The norm-chain upper bound and matching order-three point
are exact.

Finally, the audit checked the local seam model directly.  Its feasible
set is compact, both displayed restricted determinant barriers have
parameter one, and restriction of their product barrier has parameter at
most two.  At either seam endpoint the two rank-one nullities give the
matching lower bound two, while an interior seam point has only one
nullity.  Thus the example supports exactly the limited obstruction
claimed in Section 5 and is not presented as a ball lift.  No mathematical
defect was found.
