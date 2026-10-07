# Effective optimizer approximation on arbitrary rational polyhedra

Date: 2026-10-03. Status: proof complete; independent review and targeted
diagnostics are recorded in [verification.md](verification.md).

This note extends the [bounded fixed-degree point theorem](../../research-20261002/new-direction/globally-convex-polynomial-point-oracle.md)
in two ways: the polyhedron can be unbounded, and the degree need not be
fixed. It gives all constants by rational computation from an explicit
sparse polynomial. It retains the global convexity promise. It does not
apply to polynomials that are convex only on their feasible region.

The existence of small minimizers, polynomial-time objective-gap
approximation, and polynomial-time detection of unboundedness on this
input class are prior results of Slot, Steurer, and Wiedmer,
[*Hesse's Redemption*, Theorem 1.1 and Corollary 1.2](https://arxiv.org/html/2511.03440v1#S1.SS2).
The contribution developed here is an explicit error bound, a fixed
minimum-norm point oracle, and a direct construction of the constants.
The proof supplies its own radius calculation; it does not assume the
objective itself is strongly convex or expand a polynomial after an
affine substitution. Publication priority for the point theorem remains
subject to the [literature reconciliation](../literature/source-audit.md).

## 1. The theorem and its representation

Let `f` be a rational polynomial, promised convex on all of `R^n`, and
let `P={x:Bx<=b}` be a rational polyhedron. Supply the nonzero monomials
of `f`, with rational coefficients and exponent vectors. Combine equal
monomials first. Let `I` be their binary encoding length together with
the constraints, and let `D=max(2,deg f)`. The constant and affine cases
therefore use `D=2`.

There is a deterministic algorithm with the following properties.

1. It checks emptiness of `P` and unboundedness of `f` below on `P` in
   `poly(I,D)` bit work.
2. In the remaining case, `f` attains its minimum. The algorithm computes
   positive rationals `R>=1` and `Gamma>=1`, with
   `log R+log Gamma=poly(I,D)`, such that the minimum-norm optimizer
   `p` satisfies `||p||_2<=R` and

   ```text
   dist_2(x,S) <= Gamma (f(x)-f*)^(1/D)
      for every x in P with 0<=f(x)-f*<=1,             (1)
   S=argmin_P f,   f*=min_P f.
   ```

   The error bound is valid on the original, possibly unbounded,
   polyhedron, not just inside the constructed box.
3. For every integer `q>=0`, it returns a rational feasible point within
   `2^(-q)` of the same point `p`, in `poly(I,D,q)` bit work. A rational
   certified objective enclosure of width `2^(-q_f)` can be returned
   simultaneously in `poly(I,D,q+q_f)` bit work.

The polynomial work bounds are uniform in `D`. Thus they are polynomial
in the actual input size when exponents are unary, or the numerical
degree is polynomially bounded by that size. They do not assert a bound
polynomial in the logarithm of an arbitrarily large degree, or a theorem
for succinct arithmetic-circuit input. Verification of the convexity
promise is not an uncharged part of the algorithm.

The zero-variable case is direct constraint and objective evaluation.
Assume `n>=1` below. Empty polyhedra are detected by rational LP.

## 2. A computable quadratic lower bound

Set

```text
K_D=(D+1)D^(D+2).
```

For any `a,x in R^n`, put `d=x-a` and
`h(t)=f(a+td)-f(a)-t grad f(a)'d`. Global convexity implies `h>=0`,
`h(0)=0`, and `0<=h(t)<=h(1)` on `[0,1]`. Interpolate this degree-at-most
`D` polynomial at `j/D`, `j=0,...,D`. Each Lagrange denominator has
absolute value at least `D^(-D)`. Its numerator's second derivative
at zero is the sum of at most `D(D-1)` products, each of absolute value
at most one. Consequently

```text
0 <= h''(0) <= K_D h(1),

f(x) >= f(a)+grad f(a)'(x-a)
                 +(x-a)' Hess f(a) (x-a)/K_D.         (2)
```

This deliberately loose inequality also covers degree zero and one.
Sharper degree constants are known: the proof of Ahmadi, Chaudhry, and
Zhang's [Lemma 5](https://arxiv.org/html/2311.06374v2#S4) gives the underlying
tangent-quadratic bound used in *Hesse's Redemption*, Section 4.1.
The elementary estimate (2) is sufficient for polynomial bit bounds.

Integrate (2) with respect to uniform Lebesgue measure on `[0,1]^n`.
Define the rational matrix, vector, and scalar

```text
M   = integral Hess f(a) da,
ell = integral [grad f(a)-2 Hess f(a)a/K_D] da,
c   = integral [f(a)-grad f(a)'a+a'Hess f(a)a/K_D] da.
```

All integrals in this note are over the unit cube. They are computed
term by term using `integral a^alpha da=product_i 1/(alpha_i+1)`.
Sparse differentiation, coefficient collection, and these integrals
take `poly(I,D)` bit work; there are at most `n^2` Hessian entries and
at most `n^2` differentiated terms per original monomial. We obtain

```text
f(x) >= c+ell'x+x'Mx/K_D   for every x in R^n.         (3)
```

The matrix `M` is positive semidefinite. Its kernel `L` is exactly the
common kernel of all Hessians. Indeed, if `d'Md=0`, the continuous
nonnegative polynomial `a -> d'Hess f(a)d` has integral zero and hence
vanishes on the cube. Polynomial identity extends this to all `R^n`.
Positive semidefiniteness gives `Hess f(a)d=0` everywhere. The reverse
inclusion is immediate. In particular,

```text
grad f(x)'d=grad f(0)'d   for every d in L and every x. (4)
```

Let `Pi` be the orthogonal projection onto `U=range M`. Compute it
rationally by taking any full-column-rank rational basis `E` for `U`
and using `Pi=E(E'E)^(-1)E'`; put `Pi=0` if `M=0`. Define

```text
g0=grad f(0),     w=-(Id-Pi)g0,     ell_U=Pi ell.
```

These data have polynomial encoding length by rational linear algebra.
Equations (4) and the definitions show

```text
f(x)=f(Pi x)-w'x,      ell=ell_U-w.                   (5)
```

No orthonormal irrational basis and no expanded transformed polynomial
are needed. This is the rational nonlinear-subspace/affine-direction
decomposition that also underlies the cited prior work.

For a fully explicit curvature constant, choose an integer `Q_M>=1`
clearing the denominators of `M`, and let
`C_M=max(1,max_ij |(Q_M M)_ij|)`. Set

```text
rho=1/[K_D Q_M (n C_M)^(n-1)].                        (6)
```

If `M` has positive rank `r`, the product of the `r` nonzero eigenvalues
of the integer PSD matrix `Q_M M` is a positive integer: it is its
`r`th elementary symmetric polynomial, the sum of principal `r`-minors.
Every eigenvalue is at most `n C_M`. Thus its least positive eigenvalue
is at least `(n C_M)^(-(r-1))`. It follows that

```text
x'Mx/K_D >= rho ||Pi x||_2^2.                        (7)
```

If `M=0`, both sides of (7) are zero, so the same positive formula is
valid. Every constant in (6) is explicitly computable and has polynomial
bit length.

## 3. Unboundedness and a radius for an attaining optimizer

Find a rational feasible point `a in P` by exact LP, and set `F=f(a)`.
Solve the rational linear feasibility problem

```text
w=B'lambda+M z,        lambda>=0.                    (8)
```

If (8) is infeasible, the polar-cone form of Farkas' lemma supplies a
direction `d` with `Bd<=0`, `Md=0`, and `w'd>0`. Rescale it so `w'd=1`.
Then `a+td in P` and (5) gives `f(a+td)=f(a)-t` for `t>=0`. This is
a rational certificate of unboundedness.

If (8) is feasible, take a rational solution of polynomial encoding
length and put

```text
v=M z,     A=||ell_U-v||_1,     beta=c-lambda'b.
```

For `x in P`, equations (3), (5), (7), and `w'x<=lambda'b+v'Pi x`
give

```text
f(x) >= beta-A ||Pi x||_2+rho ||Pi x||_2^2.           (9)
```

This is a finite global lower bound, so the two LP branches exactly
distinguish boundedness from unboundedness. For every `x in P` with
`f(x)<=F`, a valid explicit bound from (9) is

```text
||Pi x||_2 <= T,
T=1+(A+|F-beta|+1)/rho.                              (10)
```

For if `r>T`, then `r>1` and `rho r-A>|F-beta|+1`, making
`rho r^2-Ar>F-beta`.

The one-sided constraint inequality also gives
`w'x<=lambda'b+||v||_1 T`. For the other side, convexity at zero and
(5) imply

```text
w'x=f(Pi x)-f(x)>=f(0)-||g0||_1 T-F.
```

It follows that `|w'x|<=W_0` on this sublevel, where

```text
W_0=1+|lambda'b|+||v||_1 T+|f(0)|+||g0||_1 T+|F|.   (11)
```

This uses a separate lower estimate for `w'x`; one-sided inequalities
`Bx<=b` do not bound `|w'x|` by themselves.

Stack `M` and `w'` into a rational matrix `J`. Choose an integer
`Q_J>=1` clearing its denominators, and put `J_Z=Q_J J`. Scale each
row of `B` by a positive integer to get an integer matrix `B_Z`.
Let `C>=1` bound all entries of `J_Z` and `B_Z`, and set

```text
H=(n C)^(n-1),
m_0=max_ij |M_ij|,
Y=Q_J(n^2 m_0 T+W_0),
R=1+||a||_1+H(||J_Z a||_1+Y).                        (12)
```

For every `y in P` with `f(y)<=F`, the slice
`Z_y={x in P:J_Z x=J_Z y}` is nonempty. The rational-row Hoffman
inequality, valid even for an irrational right-hand side, gives

```text
dist_2(a,Z_y)<=H ||J_Z(a-y)||_2.                      (13)
```

The [integer-minor proof](../../research-20261002/new-direction/globally-convex-polynomial-point-oracle.md#5-a-coefficient-height-hoffman-bound-makes-the-constant-effective)
uses a linearly independent set of at most `n` active constraint and
equality rows. Their least singular value is at least `1/H`; projection
onto the slice and the signs of the inequality multipliers give (13).
It requires neither boundedness nor a rational right-hand side.

Since `My=M Pi y`, (10)--(11) imply `||J_Z y||_1<=Y`. The projection
`y'` of `a` onto `Z_y` therefore has `||y'||_2<R`. Moreover,
`M(y'-y)=0` and `w'(y'-y)=0`, so (5) gives `f(y')=f(y)`.

Thus every point of the sublevel `f<=F` has an equally good feasible
representative in the ball of radius `R`. A minimizing sequence can be
replaced by such representatives. Compactness and continuity show that
the finite infimum is attained in that ball. The nonempty closed convex
set `S` has a unique minimum-norm point `p`, and `||p||_2<=R`.
The rational `R` in (12) has `log R=poly(I,D)` and is computed in
that amount of bit work.

## 4. A global effective error bound from sparse gradient coefficients

This section applies the [sparse coefficient-row proof](sparse-coefficient-degree-extension.md),
with one useful strengthening: its constants only need a bound on one
optimizer `y`, not on every feasible point `x`. Choose `y=p`, whose
norm is bounded by (12).

For every exponent vector `alpha` in the input and every index `i`
with `alpha_i>0`, include `alpha-e_i` in a set `E_f`. Form the rational
matrix

```text
N_(gamma,i)=(gamma_i+1) f_(gamma+e_i),  gamma in E_f. (14)
```

Missing coefficients are zero. With `s` input monomials there are at
most `ns` rows. The identity

```text
grad f(z)'d=sum_(gamma in E_f)(Nd)_gamma z^gamma
```

shows that `ker N` is exactly the global translation-invariance space
of `f`.

Here are complete constants. Put `U=max(1,R)`, `K=U+2`, and compute

```text
V_f=sum_alpha |f_alpha| K^|alpha|,
G_f=sum_(|alpha|>0) |f_alpha| |alpha| K^(|alpha|-1),
H_f=max(1,2V_f+2G_f(U+1)),
C_D=(D+1)D^D,       J_D=(D+1)D^(D+1),
C_*=1+J_D(H_f+3^D C_D),
r=D-1,             B_r=(r+1)2^r r^r.                (15)
```

Fix any `x in P`, `d=x-p`, and `E=f(x)-f*` in `[0,1]`. The global
Bregman argument proves

```text
|grad f(c)'d|<=C_* E^(1/D)   for every c in [0,1]^n.  (16)
```

For completeness, `h(u)=f(p+u)-f(p)-grad f(p)'u` is globally
nonnegative, and `0<=h(sd)<=E` on `[0,1]`. Interpolation gives
`|h(2td)|<=C_D E(1+2|t|)^D`. Convexity gives
`0<=h(c-p+td)<=h(2(c-p))/2+h(2td)/2`.
The first term is bounded using only `||p||_infinity<=U`, not a bound
on `x`. For `E>0`, this polynomial in `t` is bounded by
`H_f+3^D C_D` on `[0,E^(-1/D)]`. Its derivative at zero is bounded
by `J_D` times that bound times `E^(1/D)`. Adding
`0<=grad f(p)'d<=E` proves (16). If `E=0`, the first interpolation
polynomial vanishes identically; the second is bounded on the whole
line and hence constant. This gives (16) with zero right-hand side.

Tensor Lagrange interpolation on the conceptual grid
`{0,1/r,...,1}^n` bounds every coefficient of a polynomial of individual
degree at most `r` by `B_r^n` times its supremum on the cube. Indeed,
each univariate basis polynomial has coefficient norm at most
`2^r r^r`, and there are `r+1` of them. The algorithm never enumerates
this grid: it constructs the rows (14) directly. Thus

```text
|(N(x-p))_gamma| <= B_r^n C_* E^(1/D).               (17)
```

At zero gap, (17) shows that all optimizers lie in the same affine
slice of `ker N`. Conversely, invariance preserves their values, so

```text
S={x in P:Nx=Np}.                                    (18)
```

Choose a positive integer `Q_N` clearing the denominators of `N`, and
let `C_N>=1` bound all entries of `Q_N N` and `B_Z`. Put

```text
k_N=max(1,number of rows of N),
Gamma=max(1,(n C_N)^(n-1) Q_N k_N B_r^n C_*).         (19)
```

Apply the same right-hand-side-uniform Hoffman inequality to (18).
Equations (17)--(19) prove (1). All matrices have polynomially many
entries and all constants have polynomial bit length: in particular,
`log B_r^n=O(nD log(D+1))`. This proves the uniform `poly(I,D)`
construction of `Gamma`.

## 5. The fixed minimum-norm oracle

Set `Q=P intersect [-R,R]^n`. This bounded rational polytope contains
`p`, and its minimum value agrees with `f*`. Let `epsilon=2^(-q)` and
choose

```text
tau=epsilon^(2D-2)/(4*8^(D-1)*R^D*Gamma^D),
eta=tau epsilon^2/4.                                 (20)
```

Let `x_tau` be the unique minimizer of `f(x)+tau||x||_2^2` on `P`.
It exists because `f` is bounded below and the regularizer is coercive
on the closed set `P`. Comparison with `p` gives

```text
||x_tau||_2<=||p||_2<=R,
0<=f(x_tau)-f*<=tau R^2<=1.                          (21)
```

In particular it belongs to `Q` and is also the minimizer of the
regularized problem on `Q`. Let `s` be its nearest point in `S`, and
write `e=||s-x_tau||_2`. Because `p in S`, `e<=2R`. Comparison of the
regularized objective at `s` and `x_tau`, followed by (1), gives

```text
e^D/Gamma^D <= f(x_tau)-f*
            <=tau e(2||x_tau||_2+e)<=4R tau e.        (22)
```

For `e>0`, (20) implies `e<=epsilon^2/(8R)`; the case `e=0` is
immediate. The projection characterization of the minimum-norm point
of `S` is `p'(s-p)>=0`. Together with (21), it yields

```text
||x_tau-p||_2^2
   <=2||p||_2^2-2p'x_tau
   <=2p'(s-x_tau)<=2R e<=epsilon^2/4.                (23)
```

Solve the rational convex polynomial `f+tau||x||_2^2` on `Q` to
certified objective gap at most `eta`. Its strong convexity modulus
is `2tau` in the original coordinates, so the returned feasible
rational point `x` satisfies

```text
||x-x_tau||_2<=sqrt(eta/tau)=epsilon/2.
```

Together with (23) this proves `||x-p||_2<=epsilon`. The selector `p`
depends only on the input problem, not on `q` or solver choices.
The additional factor two in the denominator of (20), compared with
the earlier bounded-domain schedule, allows the projection `s` onto
the original unbounded optimizer set to have norm larger than `R`.

## 6. Value optimization, certificates, and uniform bit work

The [convex polytope value interface](../../research-20261002/new-direction/convex-polytope-value-interface.md#1-convex-value-interface)
applies to `Q` and the regularized objective. Its fixed-degree wording
can be replaced by `poly(I,D,q)` for the present explicit sparse input.
The necessary changes are precise:

- Keep the sparse polynomial in its original coordinates. After an
  affine-hull map `x=x_0+B_0 u`, evaluate the composition by evaluating
  this map and then the sparse polynomial. Compute gradients by the
  chain rule. Do not expand the composed polynomial.
- Compute function, gradient, and Hessian majorants on the original
  box by sparse coefficient sums. For reduced coordinates, multiply
  gradient bounds by a rational matrix norm of `B_0'`.
- Exact evaluation and derivative evaluation have work polynomial in
  the query bit length, the sparse input length, and the numerical
  degree. All inner and outer radii, constraint operations, and
  feasible-output repairs in the interface use rational LP and are
  independent of a fixed-degree assumption.

The precision required by (20) has
`O(Dq+D log R+D log Gamma+D)` bits. Strong convexity is used through
these binary lengths, not through numerical work proportional to
`1/tau`. No real-algebraic fallback is used here.

To request both point accuracy and an objective enclosure of width
`delta`, compute a rational `G>=max(1,sup_Q ||grad f||_2)` by sparse
majorization. Run the point oracle at accuracy at most
`min(epsilon,delta/(2G))`, and independently obtain a lower bound
`ell<=f*` with `f*-ell<=delta/2` from the value interface on `Q`.
Then `[ell,f(x)]` has width at most `delta`. Both endpoints are rational.
For `delta=2^(-q_f)`, the combined work bound is `poly(I,D,q+q_f)`.

A tangent LP dual certificate from the value interface is independently
checkable for optimization over `Q`. Its validity for the original
polyhedron uses the proved radius reduction. This is a mathematical
certificate contract conditional on global convexity; it is not a new
implementation of a general convexity recognizer or an ellipsoid solver.

## 7. What this settles and what it does not

For explicit sparse globally convex polynomial objectives and arbitrary
rational polyhedra, this closes the proposed unbounded-domain and
variable-degree extensions in the ordinary Turing model. It also gives
one consistent optimizer selection across all precision queries.

It does not turn coordinate approximation into an exact sign, zero,
active-set, or optimizer-equality test. It does not guarantee a short
expanded algebraic representation of the optimizer. It does not extend
the global-convex premise to convexity only on a bounded domain.
Those distinctions are part of the arithmetic-output classification,
not gaps in the present theorem.
