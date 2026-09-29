# Independent adversarial review of quadratic sharpness

Date: 2026-09-28. Reviewer: a fresh agent that did not author the argument.

Reviewed [quadratic-sharpness.md](quadratic-sharpness.md) in full and the
theorem/interface in [sparse-kernel-rounding.md](sparse-kernel-rounding.md).
I found no mathematical defect in the sharpness proof. The explicit lower
bound, its conversion into actual local measures, the direction of the
hierarchy comparison, and the dense certificate are correct as stated.
This review does not establish priority or replace the separate literature
audit. The broader kernel theorem was read to check its applicability here,
not subjected to another complete proof review.

## 1. Local minimization and approximation duality

For `y>=0`, the first local minimum is `-y^2`, attained at `x=y`,
and the second is `y^2`, attained at `z=0`. For `y<=0`, their values
are both zero, attained at `x=0` and `z=-y`. These choices stay in
the stated boxes, including at both endpoints.

Consequently the optimization over bag measures reduces exactly to the
difference of the two integrals of `h(y)=y_+^2`. Their separator marginal
laws can be chosen freely subject to their stated moment agreement;
the deterministic conditional minimizers realize any such choice.

The argument proving `v_n=-2 E_n(h)` has the correct sign and the factor
two. The polynomial space is a closed finite-dimensional subspace of
`C([-1,1])`. Since `h` is not a polynomial, its distance from this space
is strictly positive for every finite `n`. Hahn--Banach applied to this
distance gives a norm-one functional annihilating the polynomial space
and taking value `E_n(h)` on `h`; Riesz represents it by a signed measure
of total variation one. Annihilation of constants makes the two Jordan
masses exactly `1/2`. Placing the positive part in the first bag yields
the negative objective claimed in the note. Compactness of the spaces
of probability measures, continuity of the local costs, and closedness
of the moment constraints also justify the word “minimum” in `v_n`.

## 2. Fourier witness: signs, normalization, and support

The Fourier convention in the note is consistent: a cosine coefficient
is multiplied by `1/2` when integrated against its matching cosine under
normalized circle measure. The coefficient for odd positive `k` is

\[
 c_k=-\frac{4\sin(k\pi/2)}{\pi k(k^2-4)}.
\]

For example, `c_1=4/(3 pi)`, `c_3=4/(15 pi)`, and
`c_5=-4/(105 pi)`. The apparently exceptional sign of the `k=1`
denominator is harmless: every frequency in the witness is at least
three because `N` is even and at least two.

Multiplying `sin(2Nt)` by the Fejér series yields frequencies
`N+1,...,3N-1` with precisely the triangular weights stated. There is
no missing factor two. Substituting `t=theta-pi/2` makes the cosine
coefficient `-w_k sin(k pi/2)`. The even-frequency terms are sine
terms and have zero pairing with the even function `H(theta)`.
The remaining pairings are all positive:

\[
 \frac12 c_k[-w_k\sin(k\pi/2)]
 =\frac{2w_k}{\pi k(k^2-4)}\quad(k\text{ odd}).
\]

Because `N` is even, the odd positive offsets below `N` are
`1,3,...,N-1`, and their sum is `N^2/4`. Pairing the offsets on
both sides of `2N` therefore gives

\[
 2\sum_{\substack{1\le j<N\\j\ {m odd}}}(1-j/N)=N/2.
\]

Every denominator is positive and strictly less than `27N^3`.
The displayed pairing is thus at least `1/(27 pi N^2)`.
The Fejér kernel has integral one and is nonnegative, so
`int |Q_N| <= 1` follows directly from `|sin|<=1`. All its
frequencies exceed `n`; this annihilates every polynomial of degree
at most `n` after the cosine substitution. Finally, the choice of
the smallest even `N>=n+1` ensures `N<=n+2`. These observations
prove the exact lower-bound constant in the note.

The pushforward through cosine cannot invalidate the argument through
cancellation: it preserves the strictly positive pairing with `h`.
More explicitly, its density relative to normalized arcsine measure is
the real polynomial

\[
 q_N(y)=-\sum_{\substack{N<k<3N\\k\ {m odd}}}
             w_k\sin(k\pi/2)T_k(y).
\]

This is the even part of `Q_N` in circle coordinates. Pushforward does
not increase total variation, so its zero total mass implies that each
Jordan part has mass `t` satisfying `0<t<=1/2`. Dividing by `t`
can only increase the positive pairing to at least twice the bound in
(8). Hence (9), including its factor two, is valid. The two lifted
bag laws have the correct support and agree on all separator moments
through the required degree.

## 3. Hierarchy comparison and the affine interface

Actual bag measures are feasible for every local preordering positivity
constraint at the chosen truncation. They need not share moments above
degree `2r`, because the stated sparse hierarchy does not require those
moments. The objective of their truncated functionals is negative.
Taking an infimum therefore gives `rho_r` less than or equal to that
objective, which is exactly the direction needed for (10).

Under `x=(u+1)/2` and `z=(v+1)/2`, the original box generators
`x(1-x)` and `z(1-z)` become `(1-u^2)/4` and `(1-v^2)/4`.
Positive constant factors preserve the preordering cone and the
substitution preserves total degree. The two bags have size two and
the transformed objective has degree two, so the companion theorem's
condition is exactly `r>=2` here.

An optional explicit upper constant follows from the given split. Its
Chebyshev expansions after substitution are

\[
 f_1=3/8+u/2+T_2(u)/8-uy-y,
\]

\[
 f_2=7/8+T_2(y)/2+T_2(v)/8+v/2+vy+y.
\]

They contribute respectively `4` and `6` to the companion coefficient
budget. Hence its theorem supplies

\[
 0-\rho_r\le
 \frac{30}{2(\lfloor r/2\rfloor+1)^2+1}\le\frac{60}{r^2}.
\]

Together with (10), this proves the claimed asymptotic exponent for
one fixed objective, independent of `r`. The same upper bound also
applies to the stronger relaxation using actual local measures with
only `2r` separator moments: its feasible set is smaller, so its value
lies between `rho_r` and zero, while the explicit witness supplies its
lower gap bound.

## 4. Dense certificate and exact sparse nonattainment

Both algebraic identities in Section 4 are correct. In particular,
`xz=(xz)^2+z^2 g_x+x^2 g_z+g_x g_z` is a valid full-preordering
certificate of degree four. Each coefficient required to be SOS is a
square or a positive constant. Together with `(y-x+z)^2`, it proves
dense exactness at order two. The certificate uses all three variables
in the dense cone; it is not available in the fixed two-bag cone.

The intersection of the two polynomial rings is exactly `R[y]`.
Thus any decomposition into two polynomials supported on the stated
bags must differ from the given objective split by opposite separator
polynomials. Nonnegativity of both terms forces that polynomial to
equal `h`. This rules out such an exact decomposition at every finite
degree, not merely the particular certificate tried in the note.

The significance statements stay within the proof: this is a limitation
of finite separator information, not a hard optimization instance.
It establishes no analogous lower or upper convergence statement for
general constrained MINLP, nor any solver running-time result. No
priority claim is made, appropriately; the classical approximation and
duality ingredients alone do not settle whether the fixed quadratic
hierarchy comparison already appears elsewhere.

## 5. Targeted independent checks and their limits

I ran the following inline exact-arithmetic check from the repository
root. It passed. No project-wide verification or CI inspection was run.

```bash
python - <<'PY'
from fractions import Fraction as F
import sympy as s
x,y,z,u,v=s.symbols('x y z u v', real=True)
f=x*x-2*x*y+y*y+z*z+2*y*z
gx=x*(1-x); gz=z*(1-z)
assert s.expand(f-((y-x+z)**2+2*x*z))==0
assert s.expand(x*z-((x*z)**2+z*z*gx+x*x*gz+gx*gz))==0
for N in range(2,202,2):
    weights={k:1-F(abs(k-2*N),N) for k in range(N+1,3*N)}
    assert sum(w for k,w in weights.items() if k%2)==F(N,2)
    lower=sum(2*w/F(k*(k*k-4)) for k,w in weights.items() if k%2)
    assert lower>=F(1,27*N*N)
    assert all(k>N for k,w in weights.items() if w)
for k in range(1,104,2):
    sinhalf=lambda j: 1 if j%4==1 else -1
    integral=F(sinhalf(k),2*k)+F(sinhalf(k-2),4*(k-2))+F(sinhalf(k+2),4*(k+2))
    assert 2*integral==F(-4*sinhalf(k),k*(k*k-4))
f1=((u+1)/2)**2-(u+1)*y
f2=y*y+((v+1)/2)**2+(v+1)*y
assert s.expand(f1-(s.Rational(3,8)+u/2+s.chebyshevt(2,u)/8-u*y-y))==0
assert s.expand(f2-(s.Rational(7,8)+s.chebyshevt(2,y)/2+s.chebyshevt(2,v)/8+v/2+v*y+y))==0
print('PASS: two global polynomial identities; Fejer odd weight and lower bounds for N=2,4,...,200; 52 odd Fourier coefficients; affine Chebyshev expansions (A=10).')
PY
```

The first attempt at this check stopped with a `TypeError`: expressing
the sine signs as `(-1)**((j-1)//2)` produced a float for the negative
frequency `j=-1`, which `Fraction` correctly rejected. The corrected
modulo-four sign function above uses exact integers, and the complete
rerun passed. This was a defect in the check script, not a counterexample
to the manuscript's identity.

The symbolic identities hold as polynomial identities. The loop checks
are finite consistency checks only; they do not prove the all-degree
claim. That claim rests on the analytic calculation in Section 2 above.
These checks do not verify Hahn--Banach, Riesz representation, Jordan
decomposition, the companion kernel theorem, or publication novelty.
No Lean formalization was attempted.
