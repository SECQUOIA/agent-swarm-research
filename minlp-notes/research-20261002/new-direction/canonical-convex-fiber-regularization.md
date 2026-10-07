# Canonical convex-fiber limits: rates need quantitative constants

Date: 2026-10-02. Status: independently reviewed degree-based growth lemma,
conditional point rates, and a moving-core counterexample. These results
do not give a polynomial-bit exact-point extraction theorem under convexity alone.
No external search or priority claim is made.

For a fixed convex polynomial fiber, degree bounds the growth exponent
independently of dimension. Its coefficient can nevertheless require
exponentially many bits. Moreover, the minimum-norm fiber selector can be
discontinuous at the optimal core, even when the core value has quadratic
growth. Both issues matter when an exact optimizer is represented as a
regularization limit.

## 1. Fixed-fiber growth has an exponent no larger than the degree

Let \(Y\) be a nonempty compact polytope, and let \(f\) be a polynomial
of degree at most \(d\ge1\), convex on \(Y\). Write
\(f^*=\min_Y f\) and \(S=\operatorname*{argmin}_Y f\).

**Lemma.** There is a constant \(c>0\) such that

\[
             f(y)-f^*\ge c\operatorname{dist}(y,S)^d
                         \qquad(y\in Y).
 \tag{1}
\]

The claim is existential. It does not bound the bit length of \(c^{-1}\)
in terms of the input.

*Proof.* Subtract \(f^*\), so the minimum is zero. The
[affine-section lemma](affine-convex-fiber-certificate.md#1-every-optimal-fiber-is-an-affine-section-of-its-box)
applies to a polytope just as to a box: if \(A=\operatorname{aff}S\),
then \(S=Y\cap A\). If \(S=Y\), (1) is immediate. Otherwise choose
\(a\in\operatorname{relint}S\), and let \(L=A-a\).

First consider a polynomial \(p\) of degree at most \(d\), convex and
nonnegative on \([0,1]\), with \(p(0)=0\). It is nondecreasing there.
For \(0<t\le1\), interpolate \(p(1)\) from the \(d+1\) nodes
\(jt/d\). The absolute Lagrange coefficients sum to at most
\((2d)^dt^{-d}\), since each numerator factor has magnitude at most
one and the denominator for node \(j\) has magnitude
\((t/d)^d j!(d-j)!\). Thus

\[
             p(t)\ge (2d)^{-d}t^d p(1).
 \tag{2}
\]

Next suppose a convex polynomial has an isolated minimizer \(a\) on a
compact polytope \(P\). Every unit direction in the polyhedral tangent
cone of \(P\) at \(a\) extends a common distance \(\rho>0\) while
remaining in \(P\): choose \(\rho\) smaller than the finitely many
positive slacks divided by their constraint-normal lengths. The feasible
unit directions form a compact set. The minimum \(\beta\) of
\(f(a+\rho u)\) on that set is positive, because \(a\) is the only
minimizer. Apply (2) along each ray up to radius \(\rho\). Put
\(D_P=\max\{\rho,\operatorname{diam}P\}\). If
\(t=\|z-a\|\le\rho\), (2) gives
\(f(z)\ge(2d)^{-d}\beta(t/\rho)^d\). If \(t\ge\rho\), monotonicity
gives \(f(z)\ge\beta\), while \(t\le D_P\). Hence both ranges satisfy

\[
                    f(z)\ge\alpha\|z-a\|^d\quad(z\in P)
 \tag{3}
\]

with the explicit positive choice
\(\alpha=(2d)^{-d}\beta/D_P^d\). A singleton \(P\) needs no estimate.

Apply this observation to the transverse polytope
\(P=Y\cap(a+L^\perp)\), whose only minimizer is \(a\). To compare it
with all of \(Y\), choose a relative ball of radius \(r>0\) about
\(a\) inside \(S\), and let
\(T=\max_{y\in Y}\|\operatorname{proj}_L(y-a)\|\). If \(L\ne\{0\}\),
then \(T\ge r>0\); take \(\theta=r/(r+T)<1\). For each \(y\), a suitable
point of that relative ball cancels its \(L\)-component in a convex
combination, giving

\[
 z=a+\theta\operatorname{proj}_{L^\perp}(y-a)\in P,
                         \qquad f(z)\le\theta f(y).
 \tag{4}
\]

Explicitly, combine \(y\) with
\(a-\theta\operatorname{proj}_L(y-a)/(1-\theta)\in S\).
For \(L=\{0\}\), simply use \(\theta=1\) and \(z=y\).

Finally, the polyhedral error bound supplies a finite \(H\) such that

\[
             \operatorname{dist}(y,S)
                 \le H\operatorname{dist}(y,A)\qquad(y\in Y).
 \tag{5}
\]

For completeness, this bound follows from finitely many projection cones.
If \(s\) is a nearest point of \(S\) to \(y\), then \(w=y-s\)
lies both in the feasible tangent cone of \(Y\) at \(s\) and in
\(L^\perp+N_Y(s)\). There are only finitely many such pairs of polyhedral
cones. Their intersection cannot contain a nonzero vector in \(L\): if
\(w=b+n\), with \(b\perp L\), \(n\in N_Y(s)\), and \(w\in L\),
then \(\|w\|^2=\langle w,n\rangle\le0\). On the unit sphere of each
nonempty closed intersection, \(\|\operatorname{proj}_{L^\perp}w\|\)
therefore has a positive minimum. The reciprocal of the smallest such
minimum gives (5).

Combining (3)--(5) proves (1), with
\(c=\alpha\theta^{d-1}H^{-d}\). \(\square\)

The ingredients \(\beta,r,H\), and the affine hull itself may be hard
to compute or poorly conditioned. The proof does not replace those
quantitative obligations with a degree-only constant.

## 2. Tikhonov convergence at a fixed core

Let \(a\) be the unique minimum-norm point of \(S\), and let

\[
 y_\lambda=\operatorname*{argmin}_{y\in Y}
                       \{f(y)+\lambda\|y\|^2\},\qquad\lambda>0.
\]

Choose \(R>0\) with \(\|y\|\le R\) on \(Y\). The regularized
minimizer is unique. Comparison with \(a\) gives

\[
 f(y_\lambda)-f^*\le
       \lambda(\|a\|^2-\|y_\lambda\|^2),
                    \qquad\|y_\lambda\|\le\|a\|.
 \tag{6}
\]

Put \(e=\operatorname{dist}(y_\lambda,S)\), and choose a nearest
\(s\in S\). Since \(\|s\|\ge\|a\|\), (1) and (6) imply

\[
                   ce^d\le2R\lambda e.
\]

Also \(a\) is the projection of zero onto \(S\), so
\(\langle a,s-a\rangle\ge0\). Using (6) once more gives

\[
 \|y_\lambda-a\|^2
 \le2\langle a,s-y_\lambda\rangle\le2Re.
\]

For \(d>1\), these inequalities yield the sufficient rate

\[
 \|y_\lambda-a\|
 \le\sqrt{2R}\left(\frac{2R\lambda}{c}\right)^{1/(2(d-1))}.
 \tag{7}
\]

For \(d=1\), every \(0<\lambda<c/(2R)\) already gives
\(y_\lambda=a\). A constant objective is immediate for every
\(\lambda>0\). These are sufficient estimates, not sharp exponent
claims.

## 3. Moving the core requires a coordinated accuracy schedule

Consider the degree-three polynomial

\[
 F(v,y)=v^2(2-y),\qquad v\in[-1,1],\quad y\in[0,1].
 \tag{8}
\]

It is affine, hence convex, in the residual coordinate. Its core value is
\(V(v)=v^2\), with unique interior optimizer \(v^*=0\) and quadratic
growth constant one. Nevertheless,

\[
 S(0)=[0,1],\quad s_0(0)=0,
 \qquad S(v)=\{1\},\quad s_0(v)=1\quad(v\ne0).
 \tag{9}
\]

Thus exact fiber minimization at nonzero approximations to the optimal
core never approaches the canonical point. The regularized selector is

\[
                 s_\lambda(v)=\min\{1,v^2/(2\lambda)\}.
 \tag{10}
\]

Along \(v\to0\), the choices \(\lambda=v^4\), \(\lambda=v^2\),
and \(\lambda=|v|\) give limits one, one-half, and zero, respectively.
Independent limits in core precision and regularization are insufficient.

There is a precise sufficient interface. Suppose
\(\|F_{yv}\|_2\le B\) on the product box. Strong monotonicity from
the regularizer gives

\[
 \|s_\lambda(v)-s_\lambda(w)\|
                         \le\frac B{2\lambda}\|v-w\|.
 \tag{11}
\]

If a feasible computed point \(\widehat y\) has certified objective
gap at most \(\eta\) for the regularized fiber at \(\widehat v\),
strong convexity also gives
\(\|\widehat y-s_\lambda(\widehat v)\|\le\sqrt{\eta/\lambda}\).
Combining these with a valid fixed-fiber constant \(c\) at \(v^*\)
proves, for \(d>1\),

\[
 \|\widehat y-s_0(v^*)\|
 \le\sqrt{\eta/\lambda}
       +\frac B{2\lambda}\|\widehat v-v^*\|
       +\sqrt{2R}\left(\frac{2R\lambda}{c}\right)^{1/(2(d-1))}.
 \tag{12}
\]

Each term needs its own certified bound. Convexity and a degree bound
alone do not supply a usable numerical value of \(c\).

## 4. Global regularization also has a conditional rate

Suppose the original problem has a unique optimal core \(v^*\), with

\[
 V(v)-V(v^*)\ge g\|v-v^*\|^2,\qquad g>0,
\]

and let \(a\) be the minimum-norm point of its optimal residual fiber.
Let \((v_\lambda,y_\lambda)\) be any global minimizer of
\(F(v,y)+\lambda\|y\|^2\). No uniqueness of this regularized global
minimizer is needed. Comparison with \((v^*,a)\), and the original global
lower bound \(F\ge F^*\), give

\[
 F(v_\lambda,y_\lambda)-F^*\le\lambda R^2,
 \quad\|y_\lambda\|\le\|a\|,
 \quad\|v_\lambda-v^*\|\le R\sqrt{\lambda/g}.
 \tag{13}
\]

If \(\|F_v\|\le G\) on the product box, then

\[
 F(v^*,y_\lambda)-F^*
               \le\lambda R^2+GR\sqrt{\lambda/g}.
\]

Use (1) in the exact optimal fiber and the same minimum-norm projection
inequality as in Section 2. This proves

\[
 \|y_\lambda-a\|
 \le\sqrt{2R}\left(
       \frac{\lambda R^2+GR\sqrt{\lambda/g}}c
                           \right)^{1/(2d)}.
 \tag{14}
\]

Thus qualitative convergence holds with a sufficient exponent
\(1/(4d)\) as \(\lambda\downarrow0\). The constants still matter.

## 5. Why these rates do not establish polynomial-bit point extraction

The independently derived
[regularization precision obstruction](regularization-point-precision-obstruction.md)
gives a degree-four polynomial, jointly convex on a box, with input length
\(O(n\log n)\) and a unique optimizer. At a point one unit from that
optimizer, the objective gap is at most \(2^{-2^n}\). Therefore every
constant \(c\) in (1), for any fixed exponent, satisfies

\[
                    \log_2(1/c)\ge2^n.
\]

The same example proves that its exact isotropic Tikhonov minimizer
requires \(\log_2(1/\lambda)\ge2^n\) merely to achieve a fixed
constant point accuracy. Adding an independent quadratic core preserves
core quadratic growth and does not remove this residual obstruction.
The original point problem in that example has a simpler structural
solution, so this is a limitation of the regularization route, not a
general point-optimization lower bound.

Consequently a compact definition by a convergent regularization sequence
is not, by itself, a polynomial-bit point-evaluation algorithm. The
degree-based exponent in Section 1 does not repair the missing constant.
Equations (12) and (14) are useful sufficient interfaces when their
quantitative constants are supplied and charged; they cannot justify a
uniform polynomial precision schedule under mere residual convexity.

## Verification record

[Independent actual-file review](regularization-limit-independent-review.md#compact-convex-polynomial-growth-and-conditional-rates)
passed the affine cancellation, finite-cone polyhedral error bound,
scalar interpolation, outer-ray scale, and all
conditional regularization rates. The moving-core example and the
distinction between a degree-based exponent and an input-size modulus
also passed review. No literature-priority claim is made for the growth
lemma.

An inline `python3 - <<'PY'` command passed 240 exact checks of the
interpolation bound and regularization examples. It used convex
polynomials with explicitly squared second derivatives, checked the
moving-core selector's box KKT signs, and checked a quartic fixed-fiber
regularization path. Two further symbolic identities verified a coupled
quadratic example's global regularized stationarity equations. The same
command checked whitespace, paired math delimiters, and local links.
The scoped command
`git diff --check -- research-20261002/new-direction/canonical-convex-fiber-regularization.md`
passed. These examples supplement the proof; they do not establish a
uniform numerical bound on its constants.

No external search, index modification, project-wide checks, or CI
inspection was performed by this task.
