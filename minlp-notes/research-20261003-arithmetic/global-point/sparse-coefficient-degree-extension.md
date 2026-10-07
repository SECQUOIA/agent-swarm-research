# Point approximation with sparse coefficients and variable degree

Date: 2026-10-03. This note proves an extension of the
[bounded global-convex point theorem](../../research-20261002/new-direction/globally-convex-polynomial-point-oracle.md).
Its purpose is to remove the fixed-degree restriction without expanding a
sparse polynomial into the full monomial basis or enumerating a multivariate
interpolation grid. It makes no claim for succinct arithmetic circuits or
running time polynomial in the logarithm of the degree.

## Statement

Let `f` be a rational polynomial, convex on all of `R^n`, supplied by its
nonzero coefficients and exponent vectors. Let `D>=max(2,deg f)`. Let
`P={x:Bx<=b}` be a nonempty bounded rational polytope with supplied rational
coordinate bounds. Write `I` for the binary input length, excluding any
unary padding of `D`, and `S=argmin_P f`.

One can compute a rational `Gamma>=1` in `poly(I,D)` bit work, with
`log Gamma=poly(I,D)`, such that

```text
dist_2(x,S) <= Gamma (f(x)-min_P f)^(1/D)
    for x in P and 0<=f(x)-min_P f<=1.                 (1)
```

Consequently the minimum-Euclidean-norm point of `S` has a deterministic
feasible rational Cauchy oracle with bit work `poly(I,D,q)` at distance
accuracy `2^(-q)`. A certified objective-gap request can be met
simultaneously; if its accuracy is separately `2^(-p)`, the bound is
`poly(I,D,q+p)`. The polynomial here is uniform in `D`; in particular, the
result is polynomial time when the degree is supplied in unary or is
polynomially bounded in the input length.

Global convexity remains a promise or a separately charged certificate.
The theorem does not claim that arbitrary global convexity can be recognized
in polynomial time. Empty or zero-dimensional instances are treated as in
the original theorem.

## 1. Replace sample gradients by coefficient rows

Combine duplicate monomials and write `f(z)=sum_alpha a_alpha z^alpha`.
Let `J` be the union of exponent vectors `alpha-e_i` with `a_alpha!=0` and
`alpha_i>0`. Define the rational matrix

```text
M_(beta,i)=(beta_i+1) a_(beta+e_i),  beta in J,         (2)
```

where a missing coefficient is zero. If the input has `m` nonzero
monomials, `|J|<=nm`. Thus `M` is constructed by sparse differentiation
and coefficient collection in polynomial work. For every `d in R^n`,

```text
grad f(z)'d = sum_(beta in J) (Md)_beta z^beta.
```

It follows directly that

```text
Md=0  iff  grad f(z)'d=0 for all z
      iff  f(z+td)=f(z) for all z and all real t.       (3)
```

This identification uses no interpolation algorithm. The interpolation
below is only an inequality used to bound these explicitly known rows.

## 2. A coefficient bound that does not require enumerating its grid

For `r>=1`, set

```text
B_r=(r+1)2^r r^r.
```

If a polynomial `p` has degree at most `r` in each of `n` variables and
`|p(z)|<=V` for every `z in [0,1]^n`, then every coefficient of `p`
has absolute value at most

```text
B_r^n V.                                             (4)
```

Indeed, use univariate Lagrange nodes `j/r`, `j=0,...,r`. The denominator
of the `j`th Lagrange basis polynomial has absolute value
`j!(r-j)!/r^r>=r^(-r)`. The sum of absolute coefficients of its numerator
is at most `2^r`, because each factor is `t-a` with `a in [0,1]`.
The sum of the coefficient norms of all basis polynomials is therefore
at most `B_r`. Tensor interpolation and the triangle inequality give
total coefficient norm at most `B_r^n V`, which implies (4).

The proof mentions `(r+1)^n` evaluation nodes, but the algorithm neither
constructs them nor evaluates the polynomial at them. It only constructs
the integer `B_r^n`. Its binary length is `O(nr log(r+1))`.

## 3. A uniform gradient bound

Fix `y in S`, `x in P`, `d=x-y`, and `E=f(x)-f(y)`. The Bregman argument
in Sections 2--3 of the original theorem applies uniformly to every real
`c in [0,1]^n`; rationality or membership in a finite sample set is not
needed for that argument. Here are constants independent of the degree
being fixed.

Choose a rational `U>=max(1,sup_P ||x||_infinity)`, set `K=U+2`, and
compute

```text
V_f = sum_alpha |a_alpha| K^|alpha|,
G_f = sum_alpha |a_alpha| |alpha| K^(|alpha|-1),
H   = max(1,2V_f+2G_f(U+1)),
C_D = (D+1)D^D,
J_D = (D+1)D^(D+1),
W   = H+3^D C_D,
C_* = 1+J_D W.                                      (5)
```

The term with `|alpha|=0` in `G_f` is interpreted as zero. All these
constants have binary length polynomial in `I,D` and are computed in
that amount of bit work.

To recall the essential steps, put
`h(u)=f(y+u)-f(y)-grad f(y)'u`. Global convexity gives `h>=0` everywhere,
and optimality and convexity give `0<=grad f(y)'d<=E` and
`0<=h(sd)<=E` for `s in [0,1]`. Univariate interpolation yields

```text
|h(2td)| <= C_D E(1+2|t|)^D.
```

For `p_c(t)=h(c-y+td)`, global convexity gives

```text
0<=p_c(t)<=h(2(c-y))/2+h(2td)/2.
```

The first term is bounded using `|2c-y|_infinity<=U+2` and (5). For
`0<E<=1`, take `R=E^(-1/D)`. Then `0<=p_c(t)<=W` on `[0,R]`.
The univariate derivative interpolation bound gives
`|p_c'(0)|<=J_D W/R`. Adding the constrained first-order term proves

```text
|grad f(c)'d| <= C_* E^(1/D),  c in [0,1]^n.           (6)
```

If `E=0`, then `h(td)` vanishes identically. The midpoint inequality
bounds `p_c` on the whole real line, so this polynomial is constant and
`p_c'(0)=0`. Thus (6) also holds at zero gap.

Apply (4) with `r=D-1` to `p(z)=grad f(z)'d`. Equations (2) and (6)
give, row by row,

```text
|(Md)_beta| <= B_(D-1)^n C_* E^(1/D).                 (7)
```

In particular, differences of constrained minimizers lie in `ker M`.
Together with (3), this proves the exact optimizer-slice identity

```text
S={x in P:Mx=My}.                                    (8)
```

## 4. Effective error bound and point output

Clear the denominators of `M` with a positive integer `Q`, and write
`A=QM`. Scale the rows of the inequality matrix `B` to integers by
positive multipliers. Let `C>=1` bound the absolute entries of both
integer matrices, and set `N=max(1,|J|)`. The integer-minor Hoffman bound
from Section 5 of the original theorem is uniform in the right-hand
side and gives

```text
dist_2(x,S) <= (nC)^(n-1) ||A(x-y)||_2.
```

For `n>=1`, a valid explicit choice is therefore

```text
Gamma=max(1,(nC)^(n-1) Q N B_(D-1)^n C_*).            (9)
```

The formula also covers a constant objective, when `M` has no rows:
the residual and distance to `S=P` are both zero. The zero-variable
case is handled separately. Matrix sizes and coefficient lengths are
polynomial in the sparse input length, and (5), (9) show
`log Gamma=poly(I,D)`.

The original value-to-point conversion requests gap
`(2^(-q)/Gamma)^D`, requiring `O(Dq+D log Gamma)` accuracy bits.
For the fixed minimum-norm selector, use precisely the original
Tikhonov schedule with this `D` and `Gamma`:

```text
epsilon=2^(-q),
tau=epsilon^(2D-2)/(2*8^(D-1)*R_x^D*Gamma^D),
eta=tau*epsilon^2/4,
```

where `R_x>=max(1,sup_P ||x||_2)` is a rational input-computable bound.
Both coefficient lengths and the necessary regularized value precision
are polynomial in `I,D,q`.

The [convex value interface](../../research-20261002/new-direction/convex-polytope-value-interface.md)
is uniform for this sparse representation.
Exact evaluation of the polynomial and gradient at rational ellipsoid
query points uses polynomial work in their bit length, `I`, and `D`.
The usual bounding and Lipschitz constants have polynomial binary
length by coefficient majorization on the supplied box. The interface
does not require dense expansion, degree-dependent dimension reduction,
or recognition of global convexity. Rational affine-hull maps can be
used through direct composition during evaluation, with the original
sparse polynomial retained. More explicitly, for `x=x_0+Tw`, retain the
original-space bound `W>=sup_P |f|` and use
`G_w=||T^T||_(1->1) G_x`, where `G_x>=sup_P ||grad f||_1` is computed
by sparse coefficient majorization. The chain rule evaluates
`grad_w f(x_0+Tw)=T^T grad f(x_0+Tw)` exactly. Relative inner and outer
radii come entirely from rational LP geometry. The final tangent-LP
certificate and its Hessian bound are computed in the original
coordinates. Thus Section 1 of that interface gives the stated uniform
`poly(I,D,q)` bit bound. Its separate fixed-degree real-algebraic
fallback in Section 2 is not used here.

## Representation boundary

For a sparse polynomial with binary exponent vectors, its degree can be
exponential in `I`. In that case this theorem is polynomial in the
numeric degree, not in `I` alone. The coefficient heights in (5), the
value precision, and exact rational polynomial evaluation all depend on
that numeric degree. No running time polynomial in the binary input
length alone follows for arbitrarily large binary-encoded degrees.

Similarly, an arithmetic circuit may represent a polynomial whose full
coefficient list is exponentially larger than the circuit. The coefficient
matrix construction here uses the supplied explicit sparse list, so it
does not establish a circuit-input theorem.

## Review and scoped checks

An independent actual-file review passed the coefficient-row construction,
the tensor coefficient inequality, the global Bregman and zero-gap steps,
the rational Hoffman composition, the selector schedule, and the uniform
sparse value-oracle argument. The review also checked the original point
theorem and the convex value interface. Local links, paired code fences,
control characters, and trailing whitespace were checked for this note;
a scoped `git diff --check` passed. No project-wide verification or CI
inspection was performed.
