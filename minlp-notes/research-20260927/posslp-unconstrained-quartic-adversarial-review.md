# Independent review of the cubic tilt for unconstrained minimization

Date: 2026-09-28. Reviewer: `/root/unconstrained_posslp_adversary`.
Status: the complete
[unconstrained reduction](unconstrained-quartic-posslp-reduction.md)
passes this fresh review. The reviewer read its complete first exposition
after independently reconstructing the mathematical argument below.

The reviewer did not develop the proposed reduction. I independently
read the complete [certified cubic-root circuit proof](posslp-certified-cubic-root-reduction.md),
checked its inputs to the reviewed
[signed odd-root realization](signed-odd-root-circuit-quartic.md), and
reconstructed the cubic perturbation argument. I use the signed-root
realization as a previously reviewed theorem; this report does not
repeat its entire exposing-quadratic construction. I did not rely on the
other review of the cubic-root circuit proof.

No mathematical gap was found. The result remains a complexity lower
bound for exact comparison. It gives neither an unconditional
superpolynomial lower bound nor NP-hardness, and it does not establish
priority over all equivalent formulations.

## The scale estimate

Let the certified circuit have an output signal \(s\), assigned order
\(d\), and macro count \(T\), with

\[
 0<\delta\le2^{-30}/B_T,
 \qquad \tfrac12\delta^d\le |s|\le2^{-29},
 \qquad 1\le d\le2^T.
\]

The order bound follows inductively: a product adds its two input
orders, and an addition keeps the common order of its inputs. The
largest order therefore at most doubles at each macro. The nonzero
integer coefficient \(W=2V-1\) supplies the lower bound on \(|s|\).

Append \(r=T+1\) applications of
\(S(z)=(1+3z^2)^{1/3}-1\) to \(\delta\). Then the final signal
\(\epsilon\) obeys

\[
             0<\epsilon\le\delta^{2^{T+1}}.
\]

The total gate allowance \(Q\) must include these appended gates
**before** choosing \(\delta_0=1000^{-(Q+3)}\) and the interval
widths. Rebuilding the original small-parameter circuit with this
larger \(Q\) only decreases \(\delta_0\); every analytic estimate
continues to apply. The new gates have exactly the already checked
radicand form \(3\xi^2-6\xi+4\), so the same direct interval bound
applies without examining their true values.

All boxes are positive and have widths at most \(1000^{-3}\).
The common normalization in the signed-root theorem therefore satisfies
\(1\le\kappa<2\). If \(p\) denotes its unique zero, define
the two distinct affine coordinate functions

\[
 u(X)=X_{\epsilon,1}-\kappa,
 \qquad v(X)=X_{o,1}-\kappa.
\]

Writing \(a=|v(p)|\), one has
\(u(p)=\kappa\epsilon>0\), \(a=\kappa|s|>0\), and
\(a\le2^{-28}<1/8\). Moreover,

\[
 \frac{u(p)^2}{a/2}
 \le4\kappa\delta^{2^{T+2}-d}
 \le4\kappa\delta^{3\cdot2^T}<1.
\]

For the last strict inequality even \(\delta\le1/4\) suffices.
Thus \(u(p)^2\le a/2\). No exponentially long rational constant
or order expansion is required: \(T+1\) is the number of new gates,
and the powers in this paragraph are proof bounds.

## A fully explicit rational Hessian Gram

Let the two coordinate indices be \(a_0,b_0\), and let
\(y\) be a Hessian test direction. For
\(h(X)=-u(X)^2v(X)\), differentiation gives

\[
 y^{\mathsf T}\nabla^2h(X)y
 =-2(X_{b_0}-\kappa)y_{a_0}^2
  -4(X_{a_0}-\kappa)y_{a_0}y_{b_0}.
\]

On the full basis \(z=(y,X\otimes y)\), define a rational
symmetric matrix \(B\) by the following nonzero entries:

\[
 \begin{aligned}
 B_{y_{a_0},y_{a_0}}&=2\kappa,\\
 B_{y_{a_0},y_{b_0}}=B_{y_{b_0},y_{a_0}}&=2\kappa,\\
 B_{y_{a_0},X_{b_0}y_{a_0}}
 =B_{X_{b_0}y_{a_0},y_{a_0}}&=-1,\\
 B_{y_{b_0},X_{a_0}y_{a_0}}
 =B_{X_{a_0}y_{a_0},y_{b_0}}&=-2.
 \end{aligned}
\]

Then \(z^{\mathsf T}Bz=y^{\mathsf T}\nabla^2h(X)y\).
The sum of the absolute entries is \(6\kappa+6<18\), so
\(\|B\|_2<18\).

Suppose the signed-root theorem returns
\(y^{\mathsf T}\nabla^2F(X)y=z^{\mathsf T}Mz\), with
\(M\succ0\) rational of dimension \(H\). Put

\[
 \mu=\frac{\det M}{(\operatorname{tr}M)^{H-1}}>0,
 \qquad \lambda=\left\lceil\frac{19}{\mu}\right\rceil.
\]

Each eigenvalue of \(M\) is at most \(\operatorname{tr}M\),
so its smallest eigenvalue is at least \(\mu\). Consequently
\(\lambda M+B\succeq I\). The polynomial

\[
                         G=\lambda F-u^2v
\]

has the supplied rational positive definite Hessian Gram
\(\lambda M+B\), and \(\nabla^2G(X)\succeq I\) globally.
The determinant, trace power, ceiling, and matrix operations have
polynomial bit complexity because the supplied matrix has polynomial
dimension and coefficient length. The value of \(\lambda\) can be
large, but its binary length is polynomial. Adding the cubic term does
not change the degree-four homogeneous part, so \(G\) is still a
quartic.

The author's final exposition improves this conservative scale to
\(\lambda=\lceil9/\mu\rceil\). I independently checked its
sharper norm estimate: the three constant-block entries contribute
\(12\kappa^2\) to the squared Frobenius norm, and the two
symmetric cross-entry pairs contribute \(2+8=10\). Therefore
\(\|B\|_F^2=12\kappa^2+10<58<64\), which validates the
author's smaller scale without changing any argument.

## The sign comparison and the nonzero promise

Since \(F\ge0\) and \(F(p)=0\), differentiability gives
\(\nabla F(p)=0\). The output and appended-scale coordinates are
different, hence

\[
 G(p)=-u(p)^2v(p),\qquad
 \|\nabla G(p)\|^2=4u(p)^2v(p)^2+u(p)^4.
\]

If \(v(p)>0\), then \(\min G\le G(p)<0\).
If \(v(p)<0\), write \(a=|v(p)|\) and \(q=u(p)^2\).
The standard strong-convexity inequality, minimized over its quadratic
lower bound, gives

\[
 \min G\ge qa-\tfrac12(4qa^2+q^2)\ge\tfrac12qa>0.
\]

The second inequality follows from the exact decomposition

\[
 qa-\tfrac12(4qa^2+q^2)-\tfrac12qa
 =q\left[a\left(\tfrac14-2a\right)
            +\tfrac12\left(\tfrac a2-q\right)\right],
\]

whose two terms are nonnegative when \(a\le1/8\) and
\(q\le a/2\). Strong convexity also makes \(G\) coercive, so
the minimum exists and is unique. Thus the reduction excludes a zero
minimum in both cases. It does not need to compute the minimizer of
\(G\), which is generally different from \(p\).

## The additional positive-branch rational SOS consequence

After the main proof passed, the author proposed the following
additional consequence. I checked it independently. If a rational
quartic \(G\) has a rational Hessian Gram \(A\succeq I\)
on the full basis and \(m=\min G>0\), then \(G\) has a
rational positive definite polynomial Gram on the full monomial
basis of degree at most two.

Let \(p_*\) be its minimizer. By continuity and rational density,
choose a rational point \(q\) close enough to \(p_*\) that

\[
 c=G(q)-\tfrac12\|\nabla G(q)\|^2>0.
\]

This is an existence choice, with no polynomial bit bound asserted.
Write \(d=X-q\), \(g=\nabla G(q)\), and

\[
 S_q(X)=G(X)-G(q)-g^{\mathsf T}d-\tfrac12\|d\|^2.
\]

The Hessian of \(G-\tfrac12\|X-q\|^2\) has rational
Gram \(A-\operatorname{diag}(I_N,0)\succeq0\). Rational
PSD factorization followed by the exact identity

\[
 \int_0^1(1-t)(U+tV)^2\,dt
 =\tfrac12(U+V/3)^2+(V/6)^2
\]

shows that \(S_q\) is a sum of rational polynomial squares.
Positive rational weights cause no field extension: every positive
rational is a finite sum of rational squares. Completing the square
gives

\[
                G=S_q+\tfrac12\|d+g\|^2+c.
\]

For strictness, use
\(A-\operatorname{diag}(I_N,0)\succeq
\operatorname{diag}(0,I_{N^2})\). The displayed integral formula
then makes the chosen SOS for \(S_q\) include
\((d_i d_j/6)^2\) for every \(i,j\): apply it to
\(U=q_jd_i\), \(V=d_i d_j\). These factors span all
quadratic homogeneous polynomials in \(d\). The final norm term
and the positive constant span the affine polynomials in \(d\).
Together the rational factors span the entire polynomial space of
degree at most two. Their coefficient Gram is therefore positive
definite; translating from \(d\) to \(X\) preserves this
property by an invertible rational basis change.

Thus the original reduction's \(V\le0\) branch lies in the
rational SOS interior, whereas its \(V>0\) branch is not even
nonnegative. Precomposing the circuit transformation with
\(V\mapsto1-V\) reverses the answer on integer inputs and
gives a many-one PosSLP reduction to rational or real SOS membership
within the supplied strict Hessian class. This is a consequence of
the restricted quartic reduction and rational Taylor decomposition,
not a new general SOS-convexity principle. No polynomial certificate
length or certificate recovery algorithm follows from the rational
density step.

## Adversarial checks on the circuit dependency

I checked the full analytic argument rather than only its final signal
bound. The key safeguards survive scrutiny: the product macro vanishes
exactly on both coordinate axes; the analytic coefficient estimate
therefore bounds its error by \(|xy|(|x|+|y|)\); the homogenized
addition inputs have equal orders; zero integer intermediate values are
allowed in the uniform error induction; and all raw radicands use only
affine combinations of roots and their squares. The interval proof uses
direct signed evaluation, so it does not incorrectly exploit
correlations among predecessor variables.

The squared-signal radicand has interval error at most
\(12w+3w^2\le13w\). The coefficient sum for the product's final
raw gate is \(3/2\). The factor-1000 increase between successive
box widths comfortably absorbs both bounds. Enlarging the raw gate
allowance as described above preserves polynomial box length.

The cube-root parameter chain represents an extremely small positive
number, but all root outputs remain near one. Thus it does not violate
the signed-root theorem's promise that supplied root boxes avoid zero.

## Verification and limits of the comparison

The independently written
[exact checker](check_posslp_unconstrained_tilt_review.py) passed with

```text
python3 research-20260927/check_posslp_unconstrained_tilt_review.py
```

It verifies the cubic Hessian Gram identity, the exact gradient norm,
the no-case margin identity, and the two Taylor/completion identities
using symbolic rational arithmetic.
It does not verify the entire circuit construction, the implementation
of the signed-root theorem, or the asymptotic bit bounds. Those parts
were checked as proofs. No Lean proof, project-wide tests, or CI checks
were run for this review.

Two primary-source comparisons were checked. Tarasov and Vyalyi's
[arithmetic-circuit and SDP paper](https://arxiv.org/pdf/cs/0512035)
already establishes arithmetic-circuit hardness for exact SDP.
Consequences for SDP in general should therefore not be presented as
new. Bläser, Dutta, and Jindal's
[Nullstellensatz paper](https://goravjindal.github.io/assets/pdf/soda26-hn.pdf),
Theorems 2.3–2.4, establishes hardness for biquadratic nonnegativity and
recognizing quartic convexity. These theorem statements do not supply
the promised convexity certificate or the unconstrained minimization
restriction studied here. This is a scoped comparison, not a complete
novelty search.

The substantive strengthening over singleton feasibility is that the
new objective has a nonzero optimum on the whole space and a strict
global Hessian certificate. There is still no inverse-polynomial
separation from zero. No obstruction to efficient approximate
optimization follows without an exact stopping requirement. The
positive-branch rational SOS consequence is justified separately
above; its existence argument does not give a short certificate.
