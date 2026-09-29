# Exact unconstrained minimization of strongly SOS-convex quartics

Date: 2026-09-28. Status: the complete proof and SOS consequence passed
[fresh adversarial review](posslp-unconstrained-quartic-adversarial-review.md).
The root developed this extension of the
[certified cubic-root reduction](posslp-certified-cubic-root-reduction.md).
Publication priority is unestablished.

The result is a polynomial reduction from PosSLP to deciding
whether the minimum of a rational, globally strongly SOS-convex quartic
is negative. The minimum is promised to be nonzero. The polynomial
comes with a polynomial-size rational positive definite Hessian Gram.
There are no constraints on its optimization domain.

The construction uses the earlier arithmetic sign simulation and a
cubic perturbation. Strong convexity gives an explicit bound on how
far that perturbation can lower the objective below its value at the
old minimizer. An extra small signal makes this change too small to
reverse the encoded sign.

## 1. The arithmetic input and two distinct signals

An integer straight-line program using zero, one, addition,
subtraction, and multiplication has output \(V\). PosSLP asks
whether \(V>0\). The companion construction first replaces the
output by \(W=2V-1\), a nonzero integer with the same positivity
test. Its macro circuit has \(T\) arithmetic macros. Its small
parameter \(\delta>0\) and output signal \(s\) satisfy

\[
 d\le2^T,\qquad
 |s-W\delta^d|\le B_T\delta^{d+1},\qquad
 B_T\delta\le2^{-30},\qquad
 |s|\le2^{-29}.
 \tag{1}
\]

Here \(d\ge1\) is a proof annotation, and the large number
\(B_T\) is not printed in the instance. The order bound follows
because orders start at one, a product adds two predecessor orders,
and an addition macro retains the equal input order. In particular,

\[
 \operatorname{sign}s=\operatorname{sign}W,
 \qquad |s|\ge\tfrac12\delta^d>0.
 \tag{2}
\]

Append \(r=T+1\) further gates of the form

\[
 S(z)=(1+3z^2)^{1/3}-1
\]

starting at \(\delta\), and denote the final signal by
\(\epsilon\). These are new gates, distinct from the output
signal's gate. Since \(0<S(z)\le z^2\) for \(z>0\),

\[
                  0<\epsilon\le\delta^{2^r}.
 \tag{3}
\]

The interval construction is rebuilt with the enlarged raw-gate
bound. Specifically, set

\[
 q=2T+5,\qquad Q_*=q+9T+r+1,\qquad
 \delta_0=1000^{-(Q_*+3)},
 \tag{4}
\]

generate \(\delta=S^{\circ q}(\delta_0)\), and use boxes
\([1-w_i,1+w_i]\) with \(w_i=1000^i\delta_0\) for
the raw gates. There are at most \(Q_*\) such gates, so every
width is at most \(1000^{-3}\). The companion proof's exact
interval estimates apply unchanged, including to the appended gates.
Its error estimate (1) remains valid: the smaller printed initial
parameter only strengthens its required upper bound. The macro
topology, hence \(T\), is fixed before (4), so this definition
is not circular.

All coefficients and endpoints have polynomial bit length. There is
no rational constant of doubly exponential bit length in the output.

## 2. A rational quartic with the two signals at its zero

Apply the reviewed
[signed-root realization](signed-odd-root-circuit-quartic.md) to the
whole enlarged circuit. Write \(N\) for its number of retained
power coordinates. It returns a rational quartic \(F\), a unique
zero \(p\), and a rational matrix \(M\succ0\) such that

\[
 F\ge0,\quad F(p)=0,\quad \nabla F(p)=0,
 \qquad
 z^{\mathsf T}\nabla^2F(X)z
   =(z,X\otimes z)^{\mathsf T}M(z,X\otimes z).
 \tag{5}
\]

The quartic, the matrix, and their rational coefficients have
polynomial total size. The common normalization factor is

\[
 \kappa=\max_i\frac1{1-w_i}<2.
\]

Let \(a\) and \(b\) be the distinct first-power coordinates
of the appended signal and arithmetic output, respectively. Define
the rational affine polynomials

\[
                   u(X)=X_a-\kappa,\qquad
                   v(X)=X_b-\kappa.
 \tag{6}
\]

At the zero, write \(u_0=u(p)=\kappa\epsilon>0\) and
\(v_0=v(p)=\kappa s\ne0\). Equations (1)--(3) imply

\[
 |v_0|\le\tfrac18,
 \qquad
 \frac{u_0^2}{|v_0|}
 \le2\kappa\delta^{\,2^{r+1}-d}
 \le4\delta\le\tfrac12.
 \tag{7}
\]

For the middle inequality, \(r=T+1\) and \(d\le2^T\)
make the exponent at least one. The last inequality follows already
from \(\delta\le2^{-30}/B_T\) and \(B_T\ge2\).
The signs of \(v_0,s,W\) agree.

## 3. A cubic perturbation preserves a strict Hessian certificate

Set \(P(X)=-u(X)^2v(X)\). Direct differentiation gives

\[
 z^{\mathsf T}\nabla^2P(X)z
   =-2(X_b-\kappa)z_a^2
                   -4(X_a-\kappa)z_a z_b.
 \tag{8}
\]

Here is an explicit rational symmetric Gram \(B\) on the full
basis \((z,X\otimes z)\). In its constant block set

\[
 B_{z_a,z_a}=2\kappa,\qquad
 B_{z_a,z_b}=B_{z_b,z_a}=2\kappa.
\]

Set the two cross entries

\[
 B_{z_a,X_bz_a}=-1,\qquad
 B_{z_b,X_az_a}=-2
\]

and their symmetric mates, and set all other entries to zero.
Its quadratic form is exactly (8), and

\[
                      \|B\|\le\|B\|_F
                         =\sqrt{12\kappa^2+10}<8.
 \tag{9}
\]

Let \(h=N+N^2\), and choose

\[
 \mu=\frac{\det M}{(\operatorname{tr}M)^{h-1}}>0,
 \qquad \lambda=\left\lceil\frac9\mu\right\rceil,
 \qquad G=\lambda F-u^2v.
 \tag{10}
\]

The standard eigenvalue product bound gives
\(\lambda_{\min}(M)\ge\mu\). Consequently

\[
                        \lambda M+B\succeq I_h.
 \tag{11}
\]

This is a supplied rational Hessian Gram for \(G\), and it
implies \(\nabla^2G(X)\succeq I_N\) at every real point.
Determinants of rational matrices of polynomial dimension and entry
bit length, the trace power, and the ceiling in (10) are computable
in polynomial time and retain polynomial bit length. The construction
therefore prints \(G\) and (11) in polynomial time.

The cubic perturbation does not change the nonzero quartic leading
part. Thus \(G\) has degree four. Global strong convexity implies
coercivity and gives a unique attained global minimum.

## 4. The minimum has exactly the required sign

At \(p\), equations (5)--(6) give

\[
 G(p)=-u_0^2v_0,\qquad
 \nabla G(p)=-2u_0v_0e_a-u_0^2e_b,
 \qquad
 \|\nabla G(p)\|^2=4u_0^2v_0^2+u_0^4.
 \tag{12}
\]

The coordinates are distinct, which is used in the squared norm.
If \(V>0\), then \(v_0>0\), and \(G(p)<0\).
Hence the global minimum is strictly negative.

If \(V\le0\), put \(t=|v_0|>0\). For a function with
Hessian at least the identity, Taylor's lower bound followed by
completion of the square gives

\[
\begin{aligned}
 \min_XG(X)
 &\ge G(p)-\tfrac12\|\nabla G(p)\|^2\\
 &=u_0^2\left(t-2t^2-\tfrac12u_0^2\right)\\
 &\ge\tfrac12u_0^2t>0.
\end{aligned}
 \tag{13}
\]

The final inequality uses \(t\le1/8\) and
\(u_0^2\le t/2\). Therefore

\[
 \boxed{\quad V>0\quad\Longleftrightarrow\quad
                   \min_{X\in\mathbb R^N}G(X)<0.\quad}
 \tag{14}
\]

The minimum is never zero, so \(<0\) can be replaced by
\(\le0\) for these instances. This proves
PosSLP-hardness under the explicit promise of a nonzero optimum and
the supplied rational positive definite Hessian Gram.

## 5. Rational SOS membership is hard in the same strict class

The positive branch has a rational positive definite polynomial Gram.
Here is the precise existence argument; it does not bound the size
of that Gram.

Suppose a rational quartic \(G\) has a full rational Hessian
Gram \(A\succeq I\) and \(\min G>0\). By continuity,
choose a rational \(q\) sufficiently close to its minimizer that

\[
 c=G(q)-\tfrac12\|\nabla G(q)\|^2>0.
\]

Put \(d=X-q\), \(g=\nabla G(q)\). Subtracting
\(\tfrac12\|X-q\|^2\) subtracts
\(\operatorname{diag}(I_N,0)\) from the Hessian Gram.
Rational Taylor SOS integration therefore makes

\[
 S_q=G(X)-G(q)-g^{\mathsf T}d-\tfrac12\|d\|^2
\]

a sum of rational polynomial squares. Completing the square gives

\[
                    G=S_q+\tfrac12\|d+g\|^2+c.
 \tag{15}
\]

Positive rational scalar weights are sums of rational squares. To
check strictness on the full quadratic monomial basis, note that
\(A-\operatorname{diag}(I_N,0)\succeq
\operatorname{diag}(0,I_{N^2})\). Its Taylor squares can thus
include \((d_i d_j/6)^2\) for all \(i,j\), using
\(\int_0^1(1-t)(U+tV)^2dt=\tfrac12(U+V/3)^2+(V/6)^2\).
Those factors span the quadratic homogeneous terms; the norm and
positive constant in (15) span the affine terms. Their rational
coefficient vectors span all polynomials of degree at most two,
giving a positive definite rational polynomial Gram. Translation
back from \(d\) to \(X\) is an invertible rational basis change.

Consequently, the reduction's \(V\le0\) branch is in the
rational SOS interior; its \(V>0\) branch is not nonnegative,
and hence is not real SOS. For a reduction to SOS **membership**,
first replace the integer circuit output \(V\) by \(1-V\).
Then \(V>0\) holds exactly when the new output is nonpositive.
This supplies a polynomial many-one reduction from PosSLP to rational
SOS membership, real SOS membership, or global nonnegativity within
the supplied strict Hessian class. Yes instances admit a rational
positive definite polynomial Gram.

The rational-center choice is only an existence argument. It gives
no polynomial bound on the center's bit length or the resulting SOS
certificate. The Taylor SOS principle is established prior theory;
this is a consequence of the restricted hardness construction.

## 6. Scope, verification, and significance

The problem is unconstrained optimization over all real coordinates.
The quartic is globally strongly convex, its minimum is attained and
unique, and its global convexity certificate is supplied with the
input. Hardness of recognizing convexity is irrelevant to this
reduction. A positive lower bound on the absolute optimum that uses
only polynomially many bits is not asserted.

The result gives a conditional arithmetic barrier for exact
quartic node-bound decisions, even under strong global curvature and
explicit convexity certification. It would not give a running-time
lower bound for numerical approximation, nor prove NP-hardness or
that PosSLP is outside polynomial time.

Exact SDP already encodes arithmetic circuit comparison, as shown by
[Tarasov and Vyalyi](https://arxiv.org/pdf/cs/0512035). A separate
[primary-literature audit](posslp-convex-quartic-prior.md) compares
the stronger predecessors and the specific unconstrained SOS-convex
formulation. The claimed addition
here is the restricted quartic realization, not arithmetic hardness
of general conic optimization. Priority remains unestablished.

The elementary argument in Sections 3--4 is independent of how the
baseline zero was built: it needs two distinct affine coordinate
signals satisfying (7) and a supplied rational positive definite
Hessian Gram. The simulation and its quantitative realization are
substantive dependencies, not consequences of strong convexity alone.

The fresh reviewer independently reconstructed the full analytic
sign simulation, its signed-root interface, all new scale and matrix
bounds, and the SOS consequence. The root read the resulting review
and rechecked its strict polynomial-Gram span argument. The reviewer
ran the independent exact check

```text
python3 research-20260927/check_posslp_unconstrained_tilt_review.py
```

It passed the cubic Hessian Gram, gradient norm, no-case margin, and
Taylor/completion identities. These finite checks supplement the
universal proofs and bit bounds; they do not test an implementation
of the full reduction. The root did not duplicate that execution.
No project-wide verification, CI inspection, or Lean formalization
was performed for this result.
