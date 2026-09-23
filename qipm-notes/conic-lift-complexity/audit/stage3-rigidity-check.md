# Independent Stage 3 rigidity check

This is a bounded mathematical check of the proposed refinement and its
supporting rigidity arguments. The workbench labels were not treated as
proofs. No manuscript section was edited.

## Conclusions

1. The proposed fixed-generic-pattern refinement is correct for B >= 2,
   under the hypothetical bounded lift and parameter assumptions below.
2. It does not rule out collapse of one fixed pattern over exceptional
   fibers. I did not prove the missing no-collapse statement or construct
   a ball-lift counterexample.
3. The wide-cap face-codimension argument is correct. Its homogenization
   requires the explicit positivity argument given below.
4. The one-channel proof gives a lower bound of two when it starts from
   parameter strictly below two. Starting only from parameter at most one
   excludes equality at one but leaves an unsupported gap (1,2).
5. The one-channel theorem must be stated as an optimum over lifts, or
   as an implication for lifts attaining parameter one. Availability of
   a matching spin factor does not make every lift have parameter one.

## 1. Precise fixed-pattern proposition

Let F be R, C, or H, let a=dim_R F, R>=2, B=a(R-1), q>=2,
and n=qB. Consider a bounded affine lift of the unit ball in R^(n+1)
over finitely many Hermitian cones of orders at most R and nonnegative
rays, after minimal-face reduction and with relative Slater. Suppose its
restricted standard product log-determinant has parameter nu<q+1.

For v in S^n let P(v) be its entire primal fiber and D(v) its entire
normalized genuine certificate fiber. Let E_i(v) be the span of all
ranges in block i over D(v), and define

    Z = {v : sum_i dim_F E_i(v) <= q-1}.

Ray blocks contribute zero or one. Suppose the previously established
local curvature theorem is used to obtain the following facts:

- every primal tuple over S^n has total nullity at most q;
- on a dense open semialgebraic set U, every certificate has rank at
  least q, the primal and dual fibers are singletons, and exactly q
  full-order blocks have primal corank one; all other blocks are interior;
- Z is semialgebraic and dim Z <= n-B.

If B>=2, there is one set J of q full-order block labels such that the
active labels are J at every point of U. The choice of U can be refined
without changing this conclusion.

### Proof of singleton fibers off Z

For any v, choose a sequence in U converging to v. Boundedness gives a
convergent subsequence of the corresponding primal tuples. The limit X0
belongs to P(v). Nullity cannot decrease under a matrix limit, so X0 has
nullity at least q; the determinant-order bound gives equality.
Every certificate in D(v) is complementary to X0. Consequently
sum dim E_i(v)<=q. If v is outside Z, equality holds. A finite convex
average of certificates realizes all of these range spans simultaneously;
its total rank is q. (Choose finitely many certificates whose ranges span
the finite-dimensional spaces, and use strictly positive averaging
weights.) Its complementarity with every member of P(v) forces every
such member to have nullity at least q, and hence exactly q.

The fiber is a compact affine section of the product cone. If it had a
nonzero affine chord through a relative-interior fiber point, extend that
chord maximally. At an endpoint a previously positive eigenvalue in the
minimal product face must vanish: otherwise the endpoint remains in the
relative interior of that face and the chord extends. Its nullity would
exceed q. Thus P(v) is a singleton for v outside Z.

### Local constancy of generic labels near v outside Z

Write X(v) for this unique tuple. Every sequence of generic tuples over
points tending to v converges to X(v): compactness supplies subsequential
limits, and every such limit belongs to the singleton P(v).

Choose one such sequence with constant label set J, using the finite
number of possibilities. Each of its q active blocks remains singular
in the limit. The nullity bound q therefore forces these blocks to have
corank exactly one and every other block to be positive definite.
By compactness and convergence just proved, all generic tuples over a
sufficiently small neighborhood of v have those other blocks positive
definite. They have q active labels, hence their active labels must be
exactly J. This proves local constancy in the form actually needed; no
continuity of an arbitrarily chosen exceptional fiber selector is assumed.

### Connectedness completes the argument

Let C=closure(Z) in S^n. Semialgebraicity gives dim C=dim Z<=n-B<=n-2.
The complement S^n\C is connected (indeed path connected): one may use
Alexander duality, since H^(n-1)(C;Z/2)=0, or the standard semialgebraic
general-position path argument. On this complement the locally defined
generic label set is locally constant, so it is one fixed J.

Every nonempty generic pattern region is open in S^n and therefore meets
S^n\C, since C has empty interior. Thus no second generic pattern can
exist anywhere in U. This proves the proposition.

### What is not proved

The argument deliberately removes closure(Z), rather than assuming Z is
closed. Over Z, a fiber can have several limiting tuples, each with the
same q active labels but different kernel lines. Their convex combinations
can have smaller nullity. The compact chord argument no longer applies
because it requires all points of the fiber to have nullity q. Likewise,
the projective kernel map is not thereby defined on Z.

An equal-dimensional injective map from the generic open set into a
product of projective spaces gives no contradiction by itself: a sphere
with one point deleted and an affine chart in the target are both R^n.
The no-collapse issue must use additional structure. The fixed-pattern
proposition is a genuine reduction of the open mechanism, not a proof of
the conjectured q+1 frontier. When B=1 the dimension bound permits a
separating codimension-one set and this proof gives no fixed-pattern
conclusion.

## 2. Compact affine homogenization and the codimension bound

Let S=A intersect K be the compact lifted feasible set in cone coordinates,
with A=x0+W, x0 in int K, and nonempty full-dimensional ball image. Free
variables have already been eliminated. Since S is bounded,
W intersect K={0}. Also x0 is not in W, since otherwise x0 would be a
nonzero recession direction. Therefore L=R x0+W admits a linear height
h with h(x0)=1 and h(W)=0.

Every nonzero X in L intersect K has positive height. Height zero would
put X in W intersect K. If h(X)<0, then
X+(-h(X))x0 is a nonzero member of W intersect K: the height is zero,
and it is an interior cone point because (-h(X))x0 is interior and
X is in K. This is also impossible. Thus

    L intersect K = {t Z : t>=0, Z in S}.

The affine projection homogenizes to a linear map Pi with image the
Lorentz cone of dimension n+2. In particular Pi restricted to L is
surjective. If k is its kernel dimension, dim L=n+2+k.

For nonzero X over a target extreme ray, let E be the span of the minimal
product-cone face containing X. Every H in L intersect E gives two-sided
small feasible perturbations of X. Both target perturbations lie in the
target cone, whose minimal face at Pi(X) is a ray. Hence
Pi(L intersect E) is contained in that ray's span and

    dim(L intersect E) <= k+1.

Writing N=dim K and D=N-dim E, Grassmann's inequality gives
k+1 >= (n+2+k)+(N-D)-N, hence D>=n+1.

For a Hermitian block of order r<=R and nullity m, the face codimension is

    m + a*m*(2*r-m-1)/2 <= m*(B+1).

A zero ray contributes codimension and nullity one. Thus D<=(B+1)nullity.
For n=qB and B>=q-1, nullity at most q-1 would imply

    qB+1 <= (q-1)(B+1) = qB+1-(B-q+2) < qB+1,

which is impossible. Under nu<q+1 every boundary tuple therefore has
nullity exactly q. Compact fibers are singletons; compactness gives a
continuous inverse boundary lift. Generic saturation and constant total
nullity fix the same q full-order corank-one blocks globally. The
projective-kernel map is injective by either the face-span argument or
genuine support-certificate comparison. Invariance of domain would make
S^(qB) homeomorphic to (F P^(R-1))^q. The latter has nonzero mod-two
cohomology in degree a, with 0<a<qB. The contradiction is valid.

## 3. One-channel checks

Assume capacity B>0 and ball dimension B+1. If nu<2, every boundary
tuple has integer total nullity at most one. Every normalized certificate
has total rank at most one, and is nonzero. The midpoint of two positive
rank-one tuples on different extreme rays has rank at least two. Therefore
each convex certificate fiber is contained in one extreme ray.

Normalization fixes the scalar on that ray: evaluating the whole-slice
identity at any feasible lift of the origin gives pairing one. Thus each
fiber is a singleton. A fixed Slater tuple bounds these singletons above
and away from zero, and their graph is closed, so they form a continuous
field on the compact sphere. Its active product factor is constant.

Equal projective certificate rays imply equal support directions, by the
whole-slice slack identity (or evaluate once at an origin lift to fix the
scalar and then compare all ball points). The resulting injection S^B
into the primitive-ray manifold forces equal dimensions and a
homeomorphism. The primitive-ray classification excludes every
nonmatching-spin case, including the Albert cone. Therefore nu>=2 in
those cases. A matching spin factor attains one; the two-group Peirce
perspective construction attains two otherwise.

The conclusion is about the infimum over admissible lifts. It is false
that every lift has parameter one whenever the dictionary contains a
matching spin factor: redundant genuine factors can increase the
restricted standard parameter.

For the product extension, the compressed full certificate fibers retain
compactness, convexity, and a closed graph because the original fibers
are uniformly compact and compression is linear. One must use these
full images, rather than an arbitrary selected compressed certificate.
The same rank-one singleton argument then applies on the remaining
source sphere. A proper face of a simple cone strictly decreases its
primitive-ray capacity, so reduction cannot create a matching-capacity
spin face where none was available before. The support-join rank identity
then adds two per source. These checks support the product argument,
conditional on the already established all-EJA compression identity.
