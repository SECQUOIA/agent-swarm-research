# Independent proof review: partial kernel rounding

Date: 2026-09-28. Review of
[partial-kernel-rounding.md](partial-kernel-rounding.md), including the
kernel definitions in [sparse-kernel-rounding.md](sparse-kernel-rounding.md).
This review concerns correctness and the stated dimension counts. A
separate audit addresses prior work and novelty.

## Verdict

I found no substantive gap in the stated theorem with conditions (7)--(9).
The rectangular shared/private degree convention supports every operation
in the proof. Scalar separator consistency suffices because each private
vector occurs in one bag and is recovered as a measurable function of that
bag's shared coordinates. The finite-grid conclusion also follows with the
stated quadrature order.

This is a proof review, not a formal verification. It checks the displayed
argument and its assumptions; it does not establish priority, numerical
reliability, bit complexity, or practical solver performance.

The review found a stronger negative result than the draft's original
Section 3: omitting (9) can make the relaxation unbounded below at every
allowed finite order even when the original problem is nonnegative and
convex quadratic in its one private variable. The complete argument appears
below. A fresh subagent independently checked the non-SOS obstruction,
closed-cone separation, and feasibility construction and found no gap. That
review also observed that normalizing the separator functional is optional
for the unboundedness construction.

## 1. Rectangular cone and degree audit

The local domain is the tensor product of shared polynomials of total
degree at most `2r` and private polynomials of total degree at most two.
Thus high shared degree does not reduce the allowed private degree.

- In (7), an affine private polynomial with shared coefficients of degree
  at most `r-|I|` has square times `w_I` of shared degree at most `2r` and
  private degree at most two. Its matrix is indexed by all shared monomials
  of degree at most `r-|I|` times `1,y_1,...,y_p`.
- In (8), the affine private factor contributes no shared degree. The same
  scalar shared monomial basis is valid. In (9), the private degree is two
  and the shared bound is unchanged.
- For the Chebyshev bound, `T_alpha y_i` has shared degree at most `r` and
  private degree one. Its square and its product with `y_j` belong to the
  domain. The product `T_alpha^2(1-y_i^2)` is allowed in (9).
- At fixed output `v`, each product-kernel certificate term is
  `w_I q_I(u)^2` with `deg q_I <= k_b(m-1)-|I| <= r-|I|`.
  Multiplication by an arbitrary constant affine form in the private
  vector is therefore allowed in (7). Multiplication by `g_bj` and
  `1-y_i^2` is allowed in (8) and (9).
- Every kernel or separator-kernel input has shared total degree at most
  `2k_b(m-1) <= 2r`. Integrating output variables never requires higher
  input moments.
- The estimate uses only objective multi-indices of total degree at most
  `d <= r`. The stronger hypothesis `r>=d`, rather than merely `2r>=d`,
  is used in the mixed-moment bound and must remain explicit.

For a fixed bag, there are `binom(2r+k_b,k_b)` shared monomials and
`binom(p_b+2,2)` private monomials. This gives (11). The vector square
matrix has `(p_b+1)binom(r-|I|+k_b,k_b)` rows, as in (10); each scalar
localizer has `binom(r-|I|+k_b,k_b)` rows. There are `2^k_b` products and
`J_b+p_b` scalar localizers per product. These counts establish polynomial
SDP dimensions in private dimension and in `r` at fixed shared width.
They do not bound numerical solution time or bit complexity.

## 2. Bounded mixed moments

The telescoping Chebyshev identity uses only the singleton shared box
weights, with square degrees at most `|alpha|-1`. Therefore (7) implies
`0 <= L(T_alpha^2) <= 1` for `|alpha|<=r`.

For a private index `i>0`, (7) gives
`L(T_alpha^2 y_i^2)>=0`, while (9) gives
`L(T_alpha^2 y_i^2)<=L(T_alpha^2)<=1`. For `i=0`, use `z_0=1`.
Likewise `L(z_j^2)<=1` for every `j`. The moment matrix from (7) with
`I` empty is positive semidefinite, so its Cauchy--Schwarz inequality gives

\[
 |L(T_\alpha z_i z_j)|^2
 \le L(T_\alpha^2 z_i^2)L(z_j^2)\le1.
\]

This argument bounds signed off-diagonal moments too. It requires no
representing measure and no positivity of the full coefficient matrix
`H_b`. The entrywise coefficient norm counts both symmetric off-diagonal
entries. Consequently it counts each linear coefficient `a_i` once and
each ordered quadratic matrix entry once, exactly as stated.

## 3. Conditional matrices, zero density, and gluing

The scalar kernel preordering certificate and (7), tested against each
constant vector in `R^(p_b+1)`, prove `M_b(v)>=0` pointwise. No matrix SOS
certificate for `Q_b(v)` is involved. The matrices `M_b` depend polynomially
on output variables even though the chosen positivity certificate need not
vary continuously in those variables.

For affine `g(y)=gamma_0+gamma^T y`, (8) gives
`gamma_0 h+gamma^T ell>=0`; division by positive `h` proves private
feasibility. Condition (9) and matrix positivity give
`0<=Y_ii<=h`. When `h=0`, every diagonal entry of `M` is zero, hence every
entry is zero by the two-by-two positive semidefinite minors. Defining the
conditional private vector by any fixed point of `P_b` on this set is
valid and measurable.

The positive Schur complement statement for `h>0` is
`Y-h^(-1)ell ell^T>=0`. Its trace product with `Q_b(v)>=0` is nonnegative,
which is exactly the one-sided inequality (18). At `h=0`, both sides of
(18) vanish. This closes a boundary case that must not be handled by
formal division by zero.

Integrating a kernel factor against normalized arcsine measure deletes it.
The remaining separator polynomial is in the agreed degree space. Thus
adjacent *shared* laws agree. Running intersection gives a global shared
law, and assigning each distinct private block its measurable bag function
preserves all local laws. No private cross-bag consistency is needed under
the stated ownership assumption; dropping that assumption would invalidate
this argument.

The feasible product set is compact and nonempty, and the objective is
continuous. Thus a point with objective at most the rounded expectation
exists. Every feasible moment objective is at least `f*` minus the error,
so the infimum defining `rho_r` is finite; attainment of that infimum and
strong duality are unnecessary.

## 4. Objective estimate and finite-grid conclusion

The kernel eigenvalue identity remains valid for shared objective degrees
above the kernel degree: both the output integral and the corresponding
multiplier are zero. All multipliers lie in `[0,1]`. Therefore the
coefficient error uses

\[
 0\le1-\prod_i g_{\alpha_i}
 \le\sum_i(1-g_{\alpha_i})
 \le\frac{3\sum_i\alpha_i^2}{2m^2+1}.
\]

Combining this with the mixed-moment bound gives exactly the normalization
in (12). The final relaxed estimate follows from `m>r/s`. Constant shared
coefficients give `A=0`, and exactness is consistent with ordinary convex
quadratic mean rounding. No two-sided cost estimate survives that averaging.

The quadrature order is sufficient: if `d_infty=2a`, the matrix expression
has individual degree at most `2m+2a-2`, while `2N-1=2m+2a-1`; if
`d_infty=2a+1`, both bounds equal `2m+2a-1`. The bag masses and separator
marginals use still lower degree. At each positive-mass grid point,
`F_b(v)<=f_b(v,ybar_b(v))`, and zero-mass points have `M_b(v)=0`.
Consequently the same exact quadrature identity bounds the expected sum of
local QP minima. Finite junction-tree gluing then proves (22).

The `O(t N^s)` arithmetic/comparison count allows each parent to combine all
child messages: `sum_b children(b) N^k_b <= (t-1)N^s`. The QP values must
already be computed. Exact QP and algebraic-grid access are mathematical
oracles here. Evaluating many QPs, solving the SDP numerically, obtaining
certified rational outputs, and conditioning constants are separate costs.

Empty shared bags and zero-dimensional private blocks cause no exception:
empty kernel products are one, the shared law is a singleton, and the
corresponding matrices reduce to their remaining coordinates. A
lower-dimensional private polytope likewise causes no issue because the
proof never uses strict SDP feasibility.

## 5. Stronger negative result when private quadratic bounds are omitted

**Proposition.** For every integer `r>=6`, there is an instance satisfying
all objective and feasible-set assumptions of the main theorem for which
the relaxation imposing (7)--(8), but omitting (9), has infimum `-infinity`.
The same fixed instance works at every such order.

Take one bag with shared variables `u=(x_1,x_2,x_3)` in `[-1,1]^3` and one
private variable `y` in `[-1,1]`, represented by the affine inequalities
`1-y>=0` and `1+y>=0`. Define the homogeneous Motzkin polynomial

\[
 q(x)=x_1^4x_2^2+x_1^2x_2^4+x_3^6
                  -3x_1^2x_2^2x_3^2.
\]

It is nonnegative by arithmetic--geometric mean, and the objective
`f(x,y)=q(x)y^2` is convex quadratic in `y` everywhere on the shared box.
Its true optimum is zero, attained at `y=0`. Its shared degree is six.

Let

\[
 C_r=\left\{\sum_{I\subseteq\{1,2,3\}}w_I(x)
               \sum_j a_{Ij}(x)^2:
                  \deg a_{Ij}\le r-|I|\right\}.
\]

**Step 1: `q` is outside every `C_r`.** If such a representation existed,
each `w_I(0)=1`, and `q(0)=0` would force every `a_Ij(0)=0`. Let `ell` be
the least vanishing order among the nonzero polynomials `a_Ij`. The leading
homogeneous component of the represented polynomial would be the sum of
the squares of their degree-`ell` components. This is nonzero and has degree
`2ell`. Since `q` is homogeneous of degree six, `ell=3`; every square
polynomial vanishes to order at least three, and its degree-six component
would express `q` as a sum of squares of homogeneous cubics.

Here is an elementary contradiction for that final possibility. The zero
coefficients of `x_1^6` and `x_2^6` force the `x_1^3` and `x_2^3`
coefficients in every cubic to vanish. Write each remaining cubic as

\[
 a x_1^2x_2+b x_1x_2^2+c x_1^2x_3+d x_2^2x_3
 +e x_1x_3^2+f x_2x_3^2+g x_1x_2x_3+h x_3^3.
\]

The zero coefficient of `x_1^4x_3^2` is `sum c^2`, and that of
`x_2^4x_3^2` is `sum d^2`, forcing `c=d=0` in every cubic. The zero
coefficients of `x_1^2x_3^4` and `x_2^2x_3^4` then force `e=f=0`.
The coefficient of `x_1^2x_2^2x_3^2` is now `sum g^2>=0`, contradicting
its coefficient `-3` in `q`.

**Step 2: `C_r` is closed.** Fix monomial vectors `v_I` of degree at most
`r-|I|`. Write each SOS as `v_I^T G_I v_I` with `G_I>=0`. For uniform
probability measure on the cube, each matrix

\[
 B_I=\int w_I(x)v_I(x)v_I(x)^T\,dx/8
\]

is positive definite: its quadratic form is the integral of a nonzero
polynomial square times a weight positive in the open cube. If a sequence
of polynomials in `C_r` converges coefficientwise, their integrals are
bounded. For any chosen PSD Gram representations these integrals equal
`sum_I tr(G_I B_I)`. Each nonnegative summand bounds
`lambda_min(B_I) tr(G_I)`, so all Gram matrices are bounded. A convergent
subsequence of the finite collection of PSD matrices gives a representation
of the limit. This proves closedness.

**Step 3: a normalized separating functional exists.** Finite-dimensional
separation of the closed convex cone `C_r` and `q notin C_r` gives a linear
functional `lambda` on shared polynomials of degree at most `2r` with
`lambda(C_r)>=0` and `lambda(q)<0`.

Its normalization is strictly positive. Indeed `lambda(1)>=0`. If it were
zero, the shared box identities imply
`0<=lambda(x^(2alpha))<=lambda(1)=0` for every `|alpha|<=r`. One such
identity expands `1-x^(2alpha)` by telescoping its coordinate products and
using

\[
 1-x_i^{2a}=(1-x_i^2)\sum_{j=0}^{a-1}x_i^{2j}.
\]

The resulting weighted squares have the required order. Every monomial of
total degree at most `2r` is a product of two monomials of degrees at most
`r`; Cauchy--Schwarz for the unweighted moment matrix would therefore make
`lambda` zero on its entire domain, contradicting `lambda(q)<0`. Scale
`lambda` so that `lambda(1)=1`.

**Step 4: feasible functionals with unbounded negative objective.** Let
`lambda_0` be evaluation at the shared origin. For each `R>=0`, define the
rectangular functional

\[
 L_R(a(x)+b(x)y+c(x)y^2)=\lambda_0(a)+R\lambda(c).
\]

It is normalized. For every permitted shared weight and affine private
square,

\[
 L_R(w_I(q_0+q_1y)^2)
 =\lambda_0(w_Iq_0^2)+R\lambda(w_Iq_1^2)\ge0.
\]

For the two affine private constraints,

\[
 L_R(w_Iq_0^2(1\pm y))=\lambda_0(w_Iq_0^2)\ge0.
\]

Thus (7)--(8) hold at every `R`. There are no separator constraints in a
single bag. But

\[
 L_R(q(x)y^2)=R\lambda(q)\longrightarrow-\infty.
\]

This proves the proposition. The missing private quadratic bounds are a
substantive safeguard, not merely a convenience for this proof technique.
The example does not imply that omitting them fails for every special
case; constant `Q`, for instance, has different structure.

## 6. Verification record and limits

The symbolic coefficient identities used in the elementary non-SOS proof
were checked using a targeted inline Python/SymPy command. For a generic
cubic without `x_1^3,x_2^3`, it expanded the square and asserted exactly:

```
[x_1^4 x_3^2] q_cubic^2 = c^2
[x_2^4 x_3^2] q_cubic^2 = d^2
[x_1^2 x_3^4] q_cubic^2 = e^2 + 2*c*h
[x_2^2 x_3^4] q_cubic^2 = f^2 + 2*d*h
[x_1^2 x_2^2 x_3^2] q_cubic^2 = g^2 + 2*a*f + 2*b*e + 2*c*d
```

The targeted command actually run was:

```bash
python - <<'PY'
import sympy as s
x,y,z=s.symbols('x y z')
a,b,c,d,e,f,g,h=s.symbols('a b c d e f g h')
q=a*x**2*y+b*x*y**2+c*x**2*z+d*y**2*z+e*x*z**2+f*y*z**2+g*x*y*z+h*z**3
p=s.Poly(q*q,x,y,z)
for exponent, expected in [((4,0,2),c*c),((0,4,2),d*d),((2,0,4),e*e+2*c*h),((0,2,4),f*f+2*d*h),((2,2,2),g*g+2*a*f+2*b*e+2*c*d)]:
    actual=p.coeff_monomial(exponent)
    assert s.expand(actual-expected)==0
    print(exponent, actual)
print('PASS: exact cubic-square coefficient identities for the elementary Motzkin non-SOS proof')
PY
```

All five assertions passed. This checks these algebraic expansions only.
It does not computationally verify separation,
closedness, gluing, or the full theorem. Those steps were checked by the
written arguments above. No project-wide tests or CI status/log checks were
run. No Lean formalization was attempted.
