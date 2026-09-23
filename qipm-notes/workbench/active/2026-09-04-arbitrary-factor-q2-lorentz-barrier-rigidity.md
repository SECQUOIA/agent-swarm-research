# Arbitrary-factor wide-cap Lorentz barrier rigidity

Status: Proved and independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High; depends on the separately proved universal face-codimension lemma

## Theorem

Fix \(d\geq3\), put \(c=d-2\), and let \(q\geq2\) satisfy

\[
                              c\geq q-1.                  \tag{1}
\]

Let a bounded, full-Slater affine lift of

\[
                              B_2^{qc+1}                 \tag{2}
\]

use an arbitrary finite product of Lorentz cones of dimensions at most
\(d\), together with arbitrary nonnegative rays.  Remove redundant affine
variable kernels.  Then the standard product Jordan log-determinant
restricted to the lifted slice satisfies

\[
                         \boxed{\nu_{\rm std,slice}\geq q+1}. \tag{3}
\]

The grouped norm-chain lift attains \(q+1\).  Hence \(q+1\) is the exact
standard-barrier value throughout the divisible **wide-cap regime** (1),
with no factor-count-minimality assumption.

In particular, (3) closes every quotient-two case \(q=2\), including
arbitrarily many extra Lorentz factors and rays.  Extra factors cannot
globalize the compact label-switching seam left open by the exact
two-factor theorem.

## 1. Two global bounds

Homogenize the compact affine slice to

\[
              C=L\cap K\ \xrightarrow{\ \Pi\ }\ Q_{qc+2}. \tag{4}
\]

Suppose for contradiction that \(\nu_{\rm std,slice}<q+1\).  Since
determinant orders are integers, the determinant-order test gives

\[
                 \operatorname{nul}_J X\leq q             \tag{5}
\]

for every lifted tuple over every target extreme ray.

We use the universal face-codimension lemma.  If \(E_X\) is the span of the
minimal product-cone face containing such a tuple, \(N=\dim K\), and

\[
                         D(X)=N-\dim E_X,                 \tag{6}
\]

then every bounded proper lift satisfies

\[
                         D(X)\geq qc+1.                  \tag{7}
\]

For completeness, if \(k=\dim\ker(\Pi|_L)\), the two-sided tangent argument
at a target extreme ray gives

\[
                   \dim(L\cap E_X)\leq k+1.              \tag{8}
\]

Grassmann's inequality and \(\dim L=qc+2+k\) give

\[
 \dim(L\cap E_X)\geq(qc+2+k)+(N-D(X))-N,
                                                               \tag{9}
\]

and (7) follows.

## 2. Every boundary tuple has nullity exactly \(q\)

For any tuple \(X\), each unit of Jordan nullity contributes at most
\(c+1\) to \(D(X)\).  Indeed:

- a nonzero boundary point of \(Q_r\), \(r\leq d\), has nullity one and
  face codimension \(r-1\leq d-1=c+1\);
- the vertex of \(Q_r\) has nullity two and face codimension
  \(r\leq d=c+2\leq2(c+1)\); and
- a zero nonnegative ray has nullity one and face codimension one.

Thus

\[
                         D(X)\leq(c+1)\operatorname{nul}_JX. \tag{10}
\]

If \(\operatorname{nul}_JX\leq q-1\), then (1) gives

\[
 D(X)\leq(q-1)(c+1)
       =qc+1-(c-q+2)<qc+1,                               \tag{11}
\]

contradicting (7).  Together with (5), this proves

\[
                   \boxed{\operatorname{nul}_JX=q}       \tag{12}
\]

for every point in every lifted boundary fiber.

Every boundary fiber is therefore a singleton.  Indeed, a nontrivial
compact affine fiber has a relative-interior point in its minimal
product-cone face.  An endpoint of a maximal nonzero chord must leave the
relative interior of that face and hence increases total Jordan nullity by
at least one, contradicting (5) and (12).

Write the unique tuple over \(v\in S^{qc}\) as \(X(v)\).  Compactness and a
closed graph imply that

\[
                         v\longmapsto X(v)                \tag{13}
\]

is continuous.

## 3. The generic active \(q\)-tuple cannot switch

On a dense open semialgebraic subset of \(S^{qc}\), saturation of the
Lorentz cross-Peirce bound forces exactly \(q\) full-size \(Q_d\) factors
to be nonzero boundary rays; every other Lorentz and ray factor is
interior.  There are only finitely many possible active \(q\)-tuples.

For an active tuple \(I\), let \(U_I\) be the union of all generic regions
with that tuple, and take a convergent sequence inside \(U_I\).  Continuity
of (13) preserves the zero eigenvalue in every block
in \(I\).  No nonzero boundary ray in \(I\) can converge to its cone vertex,
because that raises its nullity from one to two while the other \(q-1\)
active nullities persist, contradicting (12).  No block outside \(I\) can
become singular for the same reason.  Thus the closure of the generic
region for \(I\) still has exactly the active tuple \(I\), with all its
blocks nonzero boundary rays and every other block interior.

Closures belonging to distinct active tuples are therefore disjoint.  Their
finite union covers the sphere because the generic set is dense.  Since
\(S^{qc}\) is connected, exactly one closure is nonempty.  Hence one fixed
set of \(q\) full-size \(Q_d\) factors is active for **every** support
direction, and every other factor is interior everywhere on the lifted
boundary sphere.

## 4. The impossible product-sphere embedding

Normalize a nonzero boundary ray \((t,u)\in Q_d\) by \(u/t\in S^c\).  The
fixed active tuple gives a continuous map

\[
           \Phi:S^{qc}\longrightarrow (S^c)^q.           \tag{14}
\]

It is injective.  Suppose \(\Phi(v)=\Phi(w)\), and let \(E\) be the span of
the product face in which the \(q\) fixed factors are the corresponding
source rays and all other factors are unrestricted.  Both \(X(v)\) and
\(X(w)\) lie in the relative interior of \(K\cap E\).

For any \(H\in L\cap E\), sufficiently small two-sided perturbations
\(X(v)\pm\epsilon H\) remain in \(C\).  Since \(\Pi X(v)\) spans an extreme
ray of the target Lorentz cone, its space of actual two-sided feasible
directions is the span of that ray, and therefore

\[
                         \Pi H\in\operatorname{span}\{\Pi X(v)\}. \tag{15}
\]

After positive height normalization, both perturbed source points lie in
the boundary fiber over \(v\).  That fiber is a singleton, so

\[
                         L\cap E=\operatorname{span}\{X(v)\}.      \tag{16}
\]

Since \(X(w)\in L\cap E\) and both tuples have homogenizing height one,
\(X(w)=X(v)\), hence \(w=v\).  This proves injectivity.

The source and target of (14) are compact connected manifolds of the same
real dimension \(qc\).  Invariance of domain makes \(\Phi\) a homeomorphism
onto \((S^c)^q\).  This is impossible because, for \(q\geq2\),

\[
 H^c((S^c)^q;\mathbb Z/2)
       \cong(\mathbb Z/2)^q,
 \qquad
 H^c(S^{qc};\mathbb Z/2)=0.                               \tag{17}
\]

The contradiction proves (3).  The grouped norm-chain construction has
exact restricted parameter \(q+1\), proving sharpness.

## 5. Significance and remaining regime

The proof closes infinitely many genuinely multi-channel bounded cases and
allows arbitrarily many extra cone factors.  Its key step is the combination
of the factor-count-independent codimension budget (7) with the global
continuity of singleton boundary fibers.  This rules out the only local seam
mechanism known to preserve parameter \(q\).

For fixed \(q\), all caps \(d\geq q+1\) are now exact.  The only bounded
divisible pure-Lorentz cases left by this theorem have

\[
                              c\leq q-2,                  \tag{18}
\]

where (7) permits boundary tuples of nullity below \(q\) and
positive-dimensional singular fibers can still connect different generic
active patterns.  The general no-fold lemma remains open there.

This theorem concerns the restricted standard product Lorentz
log-determinant.  It is not a lower bound for arbitrary barriers or a query
lower bound for quantum algorithms.

## Audit checklist

1. Verify the universal face-codimension lemma (7) independently.
2. Check the per-nullity codimension estimate (10) and the strict comparison
   (11), including equality case \(c=q-1\).
3. Verify the compact-fiber endpoint argument and continuity of (13).
4. Check that closures of distinct generic active tuples are disjoint.
5. Verify (16) from actual two-sided feasible directions and singleton normalized
   fibers.
6. Check invariance of domain and the mod-two cohomology contradiction.

## Independent hostile audit

The audit independently rederived the universal codimension inequality
\(D(X)\geq qc+1\).  It checked the factorwise estimate
\(D(X)\leq(c+1)\operatorname {nul}_JX\) for nonzero Lorentz boundary
points, Lorentz vertices, and scalar-ray vertices.  When \(c\geq q-1\),
the comparison is strict for nullity at most (q-1), including the endpoint
\(c=q-1\).  The determinant-order upper bound therefore forces every point
of every boundary fiber to have nullity exactly \(q\).

The compact-chord argument then makes all boundary fibers singletons, and
closed incidence makes the singleton field continuous.  Grouping the dense
generic strata by their finite active-label tuples, continuity preserves
all \(q\) nonzero boundary rays on each closure.  Any new singular block or
ray vertex would raise nullity.  Thus distinct label closures are disjoint,
their union covers the connected sphere, and one label tuple is global.
Finally, equal normalized phases put two lifts in the same product-face
span.  Two-sided tangent lineality plus singleton normalization gives
\(L\cap E=\mathbb RX(v)\), proving injectivity of (14).  Invariance of domain
would identify \(S^{qc}\) with \((S^c)^q\), contradicting degree-\(c\)
mod-two cohomology.  The audit returned **PASS** with no mathematical
correction.
