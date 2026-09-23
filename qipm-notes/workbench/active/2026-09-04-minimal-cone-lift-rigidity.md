# Rigidity of minimum-dimensional cone lifts

Status: Proved; independently audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High

## Theorem

Let \(C\subset\mathbb R^N\), \(N\geq1\), be a full-dimensional compact
convex body. Suppose \(C\) has an exact lift over a proper cone
\(K\subset E\) with

\[
 \dim E=N+1,                                          \tag{1}
\]

allowing an arbitrary affine slice, linear projection, and unrestricted
free variables. Then minimal-face reduction cannot decrease the cone
dimension: every proper cone lift of a full-dimensional compact
\(N\)-body needs at least \(N+1\) cone coordinates. Thus the reduced lift
uses all of \(K\).

Then the lift is rigid. There is a linear isomorphism

\[
 T:E\longrightarrow\mathbb R\times\mathbb R^N
\]

such that

\[
 \boxed{T(K)=\operatorname{hom}(C):=
 \{(t,tx):t\geq0,\ x\in C\}.}                        \tag{2}
\]

Moreover, after free-variable elimination and minimal-face reduction, the
reduced cone-coordinate slice is carried to \(\{1\}\times C\), and the
output projection on that slice is an affine isomorphism. (Invisible fibers
of the original free variables need not be rigid.) Thus every
proper cone lift using the information-theoretic minimum \(N+1\) cone
coordinates is merely the homogenization lift in different linear
coordinates; it has no genuine auxiliary lifting dimension.

Every full-dimensional compact \(N\)-body has minimum possible total cone
dimension \(N+1\): the lower bound is part of the dimension argument below,
and homogenization supplies equality. Hence (2) classifies every lift
attaining that exact minimum, without any smoothness or tameness assumption.

## Proof

The standard boundedness argument eliminates unrestricted free variables,
and the affine output on the slice extends to a linear map. First pass to
the minimal face \(F\) containing a relative-interior feasible point and
work in \(\operatorname{span}F\), so the reduced lift is proper. Write it as

\[
 C=\pi(F\cap L).                                      \tag{3}
\]

where \(L=z_0+L_0\) meets \(\operatorname{int}_{\operatorname{span}F}F\)
and \(\pi:\operatorname{span}F\to\mathbb R^N\) is linear.

Because \(C\) is full-dimensional, the restriction of \(\pi\) to the
direction space \(L_0\) has rank \(N\). Therefore

\[
 \dim L\geq N.                                       \tag{4}
\]

If \(\dim F\leq N\), (4) forces \(\dim F=\dim L=N\), hence
\(L=\operatorname{span}F\). Then \(C=\pi(F)\) is a
convex cone. A bounded convex cone is a singleton, contradicting full
dimension. Thus every cone lift has \(\dim F\geq N+1\), proving the general
dimension lower bound. Under (1), \(F=K\).  The alternative
\(\dim L=N+1\) would give \(L=E\), so \(C=\pi(K)\) would again be a
bounded cone and hence a singleton.  Equations (1) and (4) therefore force

\[
 \dim L=N,
 \qquad \pi|_{L_0}:L_0\to\mathbb R^N\text{ is bijective}. \tag{5}
\]

In particular, \(S:=K\cap L\) is affinely isomorphic to \(C\).  It is
compact because it is the image of compact \(C\) under the inverse affine
isomorphism.

The hyperplane \(L\) cannot contain zero: otherwise it is linear,
\(K\cap L\) is a cone, and its bounded linear image \(C\) is a singleton.
Thus choose a linear
functional \(\ell\in E^*\) with

\[
 L=\{z:\ell(z)=1\}.                                  \tag{6}
\]

Boundedness of \(S\) and properness of the slice imply

\[
 \ell(z)>0\qquad\text{for every }z\in K\setminus\{0\}. \tag{7}
\]

To prove this directly, fix \(w\in L\cap\operatorname{int}K\). If some
nonzero \(z\in K\) had \(\ell(z)=0\), then
\(w+tz\in S\) for every \(t\geq0\), contradicting boundedness. If instead
\(\ell(z)<0\), then

\[
 z'=z-\ell(z)w\in K\setminus\{0\},
 \qquad \ell(z')=0,
\]

reducing to the first contradiction. Pointedness gives \(z'\ne0\): equality
would imply \(z=\ell(z)w\), a negative multiple of \(w\), with both \(w\)
and \(z\) in \(K\). Thus \(\ell\in\operatorname{int}K^*\)
because its positive minimum on the compact set
\(K\cap\{z:\|z\|=1\}\) is nonzero. Hence \(S\) is a compact base of \(K\).

Every nonzero \(z\in K\) now has the unique representation

\[
 z=t s,qquad t=\ell(z)>0,qquad s=z/t\in S.          \tag{8}
\]

Define

\[
 Tz=(\ell(z),\pi z).                                  \tag{9}
\]

If \(Tz=0\), then \(z\in\ker\ell=L_0\) and
\(\pi z=0\); equation (5) gives \(z=0\). Since both spaces in (9) have
dimension \(N+1\), \(T\) is a linear isomorphism. For the representation
in (8),

\[
 Tz=(t,t\pi s),qquad \pi s\in C,                    \tag{10}
\]

and conversely every pair \((t,tx)\) with \(x\in C\) arises from the unique
\(s\in S\) satisfying \(\pi s=x\). This proves (2).

## Consequences for \(\ell_p\) balls

For \(1<p<\infty\), let

\[
 K_{p,N+1}=\{(t,u):t\geq\|u\|_p\}.
\]

The companion
[exact \(\ell_p\)-granularity theorem](2026-09-04-lp-ball-exact-cone-granularity.md)
shows that \(N+1\) is the minimum total cone dimension. The rigidity theorem
therefore says that every lift attaining it has a cone linearly isomorphic
to \(K_{p,N+1}\).

This matters for barrier accounting. One cannot replace the minimum-space
\(p\)-order cone by another \((N+1)\)-dimensional proper cone with a better
ambient logarithmically homogeneous self-concordant barrier. The optimal
parameter at minimum total dimension is an invariant of the homogenization
cone itself. The audited
[coupled \(p\)-cone barrier-premium theorem](2026-09-04-pcone-product-barrier-premium.md)
makes this numerical: every barrier on \(K_{p,N+1}\) has parameter at least
\(h(p)>2\) when \(p\ne2\), whereas \(K_{2,N+1}\) is Lorentz and has its
parameter-two hyperbolic barrier. Thus, among minimum-space lifts of
\(B_p^N\), a parameter-two ambient barrier exists if and only if \(p=2\).

## Scope and novelty

The linear-algebra rigidity proof does not require semialgebraicity,
definability, smoothness, or curvature. Unlike the finer blockwise
dimension-minus-two theorem, it applies to every full-dimensional compact
convex body and every finite-dimensional proper lifting cone.

The fact that a compact base determines its homogenization cone is standard;
see, for example, §5.2.2 of Blekherman--Parrilo--Thomas (eds.),
*Semidefinite Optimization and Convex Algebraic Geometry*.  The general
lift/slack-factorization framework and facial-reduction conventions are in
Gouveia--Parrilo--Thomas, *Mathematics of Operations Research* 38 (2013),
DOI [10.1287/moor.1120.0575](https://doi.org/10.1287/moor.1120.0575).
The useful formulation here is the equality case for arbitrary extended
formulations: dimension counting forces every \((N+1)\)-coordinate proper
cone lift to be exactly that base construction. A literature screen found
no explicit equality-rigidity theorem for arbitrary cone lifts, but
the argument is elementary enough that it should be treated as a useful
folklore-level structural lemma rather than a standalone novelty claim.

The barrier corollary uses Hildebrand's published three-dimensional
\(p\)-cone lower bound through the separately audited product-premium note.
It does not rely on a general equality-case classification for arbitrary
parameter-two cones.

## Audit record

An independent hostile audit checked free-variable elimination, minimal-face
reduction (including nonexposed minimal faces), all dimension equalities,
compactness of the base, strict positivity of \(\ell\), and the final cone
isomorphism. It found the theorem correct after the explicit
\(\dim L=N+1\) exclusion, pointedness, and reduced-slice clarifications
above. A later audit verified that the stronger \(h(p)>2\) corollary follows
directly from the independently audited product-premium theorem, so no
unpublished general Lorentz-cone characterization is needed.
