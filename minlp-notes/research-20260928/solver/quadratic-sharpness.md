# A fixed quadratic makes the sparse inverse-square rate sharp

Date: 2026-09-28. Status: proved and passed a
[fresh independent review](sharpness-fresh-review.md), with targeted exact
checks. The [focused prior audit](sharpness-prior.md) supports a qualified
contribution assessment; publication priority is unestablished. This note
supplies its approximation lower bound directly, rather than assuming a
quoted asymptotic approximation theorem.

Consider two bags `(x,y)` and `(y,z)`, with

\[
 x,z\in[0,1],\qquad y\in[-1,1],\qquad
 f(x,y,z)=x^2-2xy+y^2+z^2+2yz.                         \tag{1}
\]

This fixed quadratic has minimum zero. Its sparse box preordering
relaxations have gap of exact order `r^-2`: the companion kernel theorem
gives the upper bound, and the construction below gives a lower bound.
The lower bound persists when each local moment functional is required
to have an actual representing measure. Finite information shared
across the separator alone causes the gap.

## 1. The separator function

Write `h(y)=(max(y,0))^2`. For every `y in [-1,1]`,

\[
 \min_{0\le x\le1}(x^2-2xy)=-h(y),\qquad
 \min_{0\le z\le1}(y^2+z^2+2yz)=h(y).                 \tag{2}
\]

The minimizers are `x=max(y,0)` and `z=max(-y,0)` respectively.
Thus the minimum is zero for every fixed separator value. Equivalently,

\[
 f=(y-x+z)^2+2xz\ge0.                                 \tag{3}
\]

Let `v_n` be the minimum sum of the two local expected costs over
probability measures on their respective rectangles whose `y` moments
agree through degree `n`. The measures are otherwise unrestricted.
For `n>=0`, let

\[
 E_n(h)=\inf_{p\in\mathbb R[y],\ \deg p\le n}
                         \|h-p\|_{\infty,[-1,1]}.
\]

**Proposition 1.** `v_n=-2 E_n(h)`.

**Proof.** For separator laws `mu_1,mu_2`, the best local conditional
choices in (2) give cost `-int h dmu_1+int h dmu_2`. For any polynomial
`p` of degree at most `n`, moment agreement cancels its integrals, and
the difference of the `h` integrals is at most `2||h-p||_infty`.
This proves `v_n>=-2E_n(h)`.

For the reverse inequality, the standard dual characterization of
distance from the finite-dimensional subspace of degree-at-most-`n`
polynomials gives a signed measure `nu` of total variation one,
annihilating that subspace, with `int h dnu=E_n(h)`. This follows by
Hahn--Banach and the Riesz representation theorem on `C([-1,1])`.
Its total mass is zero, so its positive and negative parts each have
mass one half. Their doubles are probability measures with the same
first `n` moments. Use the positive part for the first bag and the
negative part for the second, with the conditional choices in (2).
The resulting cost is `-2E_n(h)`. The function `h` is not a polynomial,
so `E_n(h)>0`; no zero-norm case is needed. This proves the identity.

The exact identity uses the classical functional-analytic duality.
The explicit lower bound below needs neither that duality nor SDP
strong duality.

## 2. An elementary approximation lower bound

**Lemma 2.** For every integer `n>=1`,

\[
 E_n(h)\ge\frac1{27\pi(n+2)^2}.                        \tag{4}
\]

**Proof.** Put `H(theta)=h(cos(theta))`. For odd positive `k`, its
cosine Fourier coefficient is

\[
 c_k=\frac2\pi\int_0^{\pi/2}\cos^2\theta\cos(k\theta)\,d\theta
     =\frac{-4\sin(k\pi/2)}{\pi k(k^2-4)}.             \tag{5}
\]

This follows by writing `cos^2(theta)=(1+cos(2theta))/2`
and integrating the three cosine frequencies. No denominator in (5)
vanishes for odd `k`.

Choose the smallest even integer `N>=n+1`, so `N<=n+2`. Let

\[
 F_N(t)=\frac1N\left|\sum_{j=0}^{N-1}e^{ijt}\right|^2
       =\sum_{|j|<N}\left(1-\frac{|j|}{N}\right)e^{ijt}.
\]

This Fejer kernel is nonnegative and has integral one against
normalized circle measure. Define

\[
 Q_N(\theta)=\sin(2N(\theta-\pi/2))F_N(\theta-\pi/2).
                                                               \tag{6}
\]

Its integral absolute value is at most one. Multiplication of its
Fourier series gives

\[
 Q_N(\theta)=\sum_{k=N+1}^{3N-1}
 w_k\sin(k(\theta-\pi/2)),\qquad
 w_k=1-\frac{|k-2N|}{N}.                               \tag{7}
\]

In particular every Fourier frequency has magnitude greater than
`n`. Hence `int p(cos(theta)) Q_N(theta) dtheta/(2pi)=0`
for every degree-at-most-`n` polynomial `p`. The cosine coefficient
of `Q_N` at `k` is `-w_k sin(k pi/2)`. Orthogonality and (5) give

\[
 \begin{aligned}
 \int H(\theta)Q_N(\theta)\frac{d\theta}{2\pi}
 &=\frac2\pi
   \sum_{\substack{N<k<3N\\k\text{ odd}}}
                  \frac{w_k}{k(k^2-4)}\\
 &\ge\frac1{27\pi N^2}.                              \tag{8}
 \end{aligned}
\]

To see the last inequality, `k>=3`, `k(k^2-4)<27N^3`, and,
because `N` is even, the triangular weights in (7) on odd indices
sum to `N/2`. Pair the weights at `2N-j` and `2N+j`, for positive
odd `j<N`, to check this sum directly.

Subtract any `p(cos(theta))` in (8), use annihilation and the
integral absolute-value bound of one, and take the infimum over `p`.
This proves (4).

## 3. Explicit local-measure witnesses and hierarchy gap

Push the signed circle measure with density `Q_N` forward by
`theta -> cos(theta)`. Its resulting signed measure `nu` has total
mass zero, total variation at most one, and annihilates every
polynomial through degree `n`. Equation (8) gives `int h dnu>0`.
Write its Jordan decomposition as `nu=nu_+-nu_-`, with each part
of mass `t`. Then `0<t<=1/2`. The laws

\[
 \mu_+=\nu_+/t,\qquad \mu_-=\nu_-/t
\]

are probability measures with matching first `n` moments, and

\[
 \int h\,d\mu_+-\int h\,d\mu_-
 \ge\frac2{27\pi(n+2)^2}.                             \tag{9}
\]

Give the first bag the law of `(max(Y,0),Y)` for `Y~mu_+`,
and the second the law of `(Y,max(-Y,0))` for `Y~mu_-`.
Both are supported on the correct local rectangle. All local
positivity tests of every degree hold, and their separator moments
match through degree `n`. Their objective is the negative of (9).

Let `rho_r` be the order-`r` sparse box preordering lower bound,
with all shared moments through degree `2r`. For `r>=2`, choose
`n=2r` above. These actual local measures supply feasible truncated
functionals, so

\[
 0-\rho_r\ge\frac2{27\pi(2r+2)^2}.                    \tag{10}
\]

An affine change `x=(u+1)/2`, `z=(v+1)/2` puts the model on
`[-1,1]^3`, keeps both bags of size two and the objective quadratic,
and preserves total degree and separator agreement. The companion
kernel theorem has coefficient budget `A=10` for this transformed
two-bag split, giving

\[
 0-\rho_r\le
 \frac{30}{2(\lfloor r/2\rfloor+1)^2+1}\le\frac{60}{r^2}.       \tag{10a}
\]

The independent reviewer obtained `A=10`, and the root separately
recomputed the two contributions as `4+6`. Thus the rate exponent two is sharp even for a
fixed quadratic objective, three continuous variables, and two
bags of size two.

## 4. Dense exactness and absence of a polynomial separator

The dense box preordering is exact already at order two. To see this
in the original coordinates, set `g_x=x(1-x)` and `g_z=z(1-z)`.
Then

\[
 xz=(xz)^2+z^2g_x+x^2g_z+g_xg_z.                       \tag{11}
\]

Together, (3) and (11) give an explicit degree-four dense preordering
certificate for `f>=0`. Under the affine change, `g_x` and `g_z`
are positive constant multiples of `1-u^2` and `1-v^2`.

Conversely, a decomposition of `f` into one nonnegative polynomial
on each original bag would have to be

\[
 x^2-2xy+p(y),\qquad y^2+z^2+2yz-p(y)
\]

for a polynomial `p`, because a polynomial belonging to both bag
variable rings depends only on `y`. Taking the two minima in (2)
forces `p=h`, which is impossible for a polynomial. This gives a
simple failure of exact polynomial separator attainment. With a
positive constant perturbation `delta`, the same reasoning requires
`h<=p<=h+delta`, which explains the approximation-theoretic rate.

## Scope and novelty status

This is a hierarchy limitation, not optimization hardness: the three
variable model is explicitly solved in (2). It shows why increasing
local strength alone cannot remove an error caused by finite separator
information. The dense certificate crosses the missing `(x,z)` pair;
it is not a certificate permitted by the two fixed bags.

Classical ingredients include polynomial approximation duality and
Fejer kernels. The identity between best approximation and moment-matching
probability laws in Proposition 1 is established prior; the audit locates
explicit statements in Han--Jiao--Weissman and Wu--Yang. It is included
as a transparent characterization, not claimed as new.

[Nie, Qu, Tang and Zhang, Example 6.7](https://link.springer.com/article/10.1007/s10107-025-02223-2)
already give a quartic two-bag problem with dense order-two exactness and
no finite sparse tightness. Their separator is rational and nonpolynomial.
Consequently nonattainment, dense-versus-sparse separation, and the
polynomial-separator obstruction are not new general phenomena. The
candidate addition here is a fixed **quadratic** example with a piecewise
quadratic separator and a sharp quantitative rate, including explicit
local-measure witnesses. The focused audit records additional comparisons
and did not locate an equivalent example; this does not establish priority.

The dense order-two statement uses the quadratic generators `x(1-x)`
and `z(1-z)`, equivalent to `1-u^2` and `1-v^2`. With all linear
endpoint generators in a dense preordering, (3) already gives a
degree-two certificate. This distinction does not affect the sparse
lower bound, whose witnesses are actual local measures.

The root ran

```
python3 -B research-20260928/solver/check_quadratic_sharpness.py
```

It passed the polynomial identities, nine exact integrated Fourier
coefficients, 128 rational lower-bound cases, and sixteen independent
Fourier convolutions. The fresh reviewer independently checked more
odd coefficients and weight sums with exact arithmetic and reconstructed
the full proof. These finite tests supplement the all-order argument;
they do not establish its universal conclusions or priority by themselves.
No Lean formalization, project-wide verification, or CI inspection was
performed for this result.
