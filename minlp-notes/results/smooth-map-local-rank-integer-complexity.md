# Smooth graph approximation: local noncommutative rank and integer precision

Date: 2026-09-05. Status: independently reviewed; see `notes/review-nonquadratic-integer-precision.md`
and `notes/review-nonquadratic-integer-precision-second.md`.
The oscillatory-integral and noncommutative-rank theorems are established.
The proposed contribution is their use for graph-contact volume and
mixed-integer precision. Publication priority is unestablished.

## The bounds

Let `B` be a bounded closed full-dimensional box in `R^n`. Let
`F=(f_1,...,f_m)` be real `C^infinity` on an open neighborhood of `B`.
Define the pointwise and global Hessian ranks by

```
r_loc=max_(x in interior B) ncrank(span_j {∇²f_j(x)}),
r_all=ncrank(span_{x in B, j} {∇²f_j(x)}).
```

Ranks are over the complex free skew field; all Hessians are real
symmetric. The global span is finite-dimensional, being a subspace of
the symmetric `n`-by-`n` matrices. These are ranks of matrix spaces,
not dimensions of those spaces. Necessarily `0<=r_loc<=r_all<=n`.

Use the whole-graph, componentwise vertical error, and convex-lift
integer-dimension definitions from
`quadratic-system-noncommutative-rank-complexity.md`. In particular,
every exact graph point on `B` must be admitted, every admitted point
has error at most `ε`, integer ranges may be unbounded, and the convex
lift need not be closed. Denote the minimum integer dimension by
`p_conv(ε)` and the minimum binary dimension of linear lifts by
`p_bin(ε)`.

**Theorem 1 (local-to-global bounds).** As `ε` decreases to zero,

```
(r_loc/2)log2(1/ε)-O_(F,B)(1)
 <= p_conv(ε) <= p_bin(ε)
 <= (r_all/2)log2(1/ε)+O_(F,B)(1).                        (1)
```

If `r_loc=r_all=r`, both minima equal
`(r/2)log2(1/ε)+O_(F,B)(1)`. In particular, if the Hessian space has
full noncommutative rank at any one interior point, both leading
coefficients are `n/2`.

The smooth upper bound permits a number of rows polynomial in `1/ε`
for fixed data. It does not assert a number of rows polynomial in
`log(1/ε)` for an arbitrary smooth function.

**Theorem 2 (fixed-degree polynomial compactness).** If every output is
a polynomial of degree at most a fixed integer `D>=2`, the upper bound
in (1) has a binary linear formulation with
`O_(F,B,n,m,D)((1+log(1/ε))^D)` rows and variables. The binary count is
still at most `(r_all/2)log2(1/ε)+O_(F,B)(1)`. Coefficients are arbitrary
fixed real numbers; no preprocessing bit-complexity claim is made.
Affine systems have an exact zero-binary linear formulation.

For a polynomial system with full pointwise noncommutative rank,
Theorems 1 and 2 provide a matching integer precision law with a
formulation of size polynomial in the precision depth.

## The classical analytic estimate

We use the local nondegenerate mixed-Hessian estimate: for real smooth
`Φ(X,Y)`, `X,Y in R^N`, and a smooth compactly supported amplitude `a`
with `det ∂²_(X,Y)Φ !=0` on its support, the operator

```
T_λ g(X)=integral exp(iλΦ(X,Y)) a(X,Y)g(Y) dY
```

satisfies

```
||T_λ||_(L²->L²)<=C λ^(-N/2),    λ>=1.                  (2)
```

This is Hörmander's theorem. An exact primary statement is
*Oscillatory integrals and multipliers on FL^p*, Arkiv för Matematik
11 (1973), Theorem 1.1, specialized to `p=2`,
[open original paper](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7179-11512_2006_Article_BF02388505.pdf).
The smoothness, support, and determinant assumptions were also checked
in Wolff's *Lectures in Harmonic Analysis*, revised March 2002,
Theorem A, printed pages 50–51,
[editor-hosted notes](https://personal.math.ubc.ca/~ilaba/wolff/notes_march2002.pdf).

The classical local proof uses `T_λ T_λ*`. After restricting to a small
neighborhood, the gradient in `Y` of `Φ(X,Y)-Φ(Z,Y)` has norm bounded
below by a constant times `|X-Z|`. Integration by parts gives a kernel
bound `C_M(1+λ|X-Z|)^(-M)`. Taking `M>N` and applying Schur's test gives
`||T_λ T_λ*||<=C λ^(-N)`, hence (2). This estimate, including its proof
method, is not a novelty claim.

## Matrix evaluation converts local rank to a real phase

Suppose first that the Hessians at an interior point `x_0` have full
noncommutative rank `n`. The matrix-evaluation characterization of this
rank supplies an integer `d>=1` and complex `d`-by-`d` matrices `B_j`
such that

```
M=sum_j B_j tensor ∇²f_j(x_0)
```

is invertible. This is the negation of condition (3) in GGOW,
*Operator Scaling: Theory and Applications*, Theorem 1.4,
[open published paper](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf).
The determinant is a polynomial with real coefficients in the entries
of the `B_j`. Nonvanishing at a complex tuple means it is not the zero
polynomial. A nonzero real polynomial cannot vanish at every real
tuple, so the witness can be chosen real. Fix such a real witness.

Write

```
D_j(x,y)=f_j(x)+f_j(y)-2f_j((x+y)/2),
X=(x_1,...,x_d),   Y=(y_1,...,y_d),
Φ(X,Y)=sum_(a,b,j) (B_j)_(ab) D_j(x_a,y_b).              (3)
```

Both `X` and `Y` have `N=nd` real coordinates. At the diagonal point
`X=Y=(x_0,...,x_0)`, the mixed Hessian is

```
∂²_(X,Y) Φ = -(1/2)sum_j B_j tensor ∇²f_j(x_0)
           = -(1/2)M.                                  (4)
```

It is invertible. By continuity choose a small closed box `Q` around
`x_0`, contained in the interior of `B`, such that this mixed Hessian
stays invertible on an open neighborhood of `Q^d times Q^d`. Choose
`a` smooth and compactly supported in that neighborhood, with `a=1`
on `Q^d times Q^d`. The midpoint arguments in (3) remain inside the
smooth domain. Thus (2) applies with constants fixed independently of
`ε` and of any contact set.

## The contact-volume lemma

**Lemma.** Under the preceding full-rank hypothesis, there are a box
`Q`, constants `C,ε_0>0`, such that every compact `S subset Q` satisfying

```
|D_j(x,y)|<=2ε     for all x,y in S and all j             (5)
```

has `vol_n(S)<=C ε^(n/2)` for `0<ε<=ε_0`.

**Proof.** Write `v=vol_n(S)` and
`K=sum_(a,b,j)|(B_j)_(ab)|>0`. On `S^d times S^d`, (3) and (5) give
`|Φ|<=2Kε`. Set `λ=(4Kε)^(-1)` and restrict `ε_0` so `λ>=1`. Then
`|λΦ|<=1/2`, so the real part of `exp(iλΦ)` is at least `1/2`.
Using the cutoff, which equals one on the relevant product set,

```
(1/2)v^(2d)
 <= Re integral_(S^d times S^d) exp(iλΦ(X,Y)) dX dY
 <= |<1_(S^d), T_λ 1_(S^d)>|
 <= C λ^(-nd/2) ||1_(S^d)||²_(L²)
 = C (4Kε)^(nd/2) v^d.
```

If `v=0` there is nothing to prove. Otherwise divide by `v^d` and take
the `d`th root. The result is `v<=C' ε^(n/2)`. ∎

The contact sets may have arbitrary geometry. The argument never
assumes that they are convex, connected, or have bounded aspect ratio.
This avoids an invalid direct perturbation of a quadratic determinant
bound on highly anisotropic sets.

## Integer parity and a partial-rank slice

Within `Q`, group all exact graph inputs by the parity of any feasible
integer lift of their graph point. These at most `2^p` sets cover `Q`.
For any two inputs in one group, their graph lifts have an integer
midpoint. Convexity admits that midpoint, and the error assumption
implies (5). Take closures inside `Q`; continuity preserves (5) and
the compact closures still cover `Q`. The lemma yields

```
vol_n(Q)<=2^p C ε^(n/2),
p>=(n/2)log2(1/ε)-O_(F,B)(1).                            (6)
```

This uses the established integer-parity mechanism of Lubin, Vielma,
and Zadik, *Mixed-integer convex representability*, Lemma 4.1; the
local algebra and analytic volume bound quantify it here.

For pointwise rank `r>0`, the Hermitian principal-pivot lemma proved in
`quadratic-system-noncommutative-rank-complexity.md` gives an index set
`I`, `|I|=r`, whose compressed Hessian pencil at `x_0` has full
noncommutative rank `r`. Fix all coordinates outside `I` to their
values at `x_0`. The restricted smooth system has a full-dimensional
`r`-box and full pointwise rank. Apply (6) in dimension `r`. Choose
an interior point attaining `r_loc`; the maximum is attained because
the set of possible integer ranks is finite. This proves the lower
bound in (1). The case `r_loc=0` needs only `p>=0`.

## Global Hessian structure gives the smooth upper bound

Choose a finite real basis of the global Hessian span, with
noncommutative rank `r_all`. The real shrunk-subspace and symmetry
lemmas in the quadratic theorem give a fixed orthogonal decomposition

```
R^n=Z directsum W directsum R,
H Z subset W    for every H in the global Hessian span,
(dim Z)-(dim W)=n-r_all.
```

In these coordinates every Hessian, at every input in `B`, has zero
`ZZ` and `ZR` blocks. Assign coordinate exponents

```
alpha_i=0 on Z,    alpha_i=1 on W,    alpha_i=1/2 on R.
```

Their sum is `r_all/2`, and every potentially nonzero Hessian entry
has `alpha_i+alpha_k>=1`.

The transformed original domain is a compact parallelepiped `P`.
Enclose it in a box with positive side lengths `b_i`. For a depth
parameter `T>=0`, partition coordinate `i` into `2^(ceil(alpha_i T))`
equal intervals, of width at most `b_i 2^(-alpha_i T)`. Coordinates
with exponent zero are left undivided. Intersect grid cells with `P`,
and discard empty intersections. Each remaining cell is a compact
convex polytope; choose a point `c` in it.

Uniform boundedness of the Hessians on `B`, the zero blocks, and the
integral Taylor remainder imply, throughout each cell,

```
|f_j(x)-f_j(c)-∇f_j(c)^T(x-c)| <= C_0 2^(-T),            (7)
```

with one finite constant `C_0` for all cells and outputs. Indeed, the
remainder is an integral of `sum_(i,k) H_(ik) Δ_i Δ_k`; each nonzero
term has `|Δ_i Δ_k|<=b_i b_k 2^(-T)`. The segment between `c` and `x`
stays in the original domain, where the stated derivative bounds and
zero entries hold.

Choose `T=max{0,log2(2C_0/ε)}` when `C_0>0`. On each cell, use the
polytope given by the affine Taylor approximation in (7), with an
output band of radius `ε/2`. It contains that cell's exact graph and
has graph error at most `ε`. The union has at most

```
N_cells<=2^(sum_i ceil(alpha_i T))
```

members. Any finite union of bounded polyhedra has a binary linear
encoding using `ceil(log2 N_cells)` bits: assign distinct binary codes
to its members and use their convex-hull disjunctive formulation, with
the code vector equal to the convex combination of member codes. An
integral code forces every positively weighted member to have that
same code, so the projected union is exact. Hence

```
p_bin<=sum_i ceil(alpha_i T)
      <=(r_all/2)log2(1/ε)+O_(F,B)(1).
```

If all Hessians vanish, the system is affine on `B` and is represented
exactly. This proves the general smooth upper bound.

## A compact upper formulation for polynomial maps

Suppose the outputs are polynomials of degree at most `D`. Under the
fixed coordinate change above, each forbidden Hessian entry is a
polynomial vanishing on a full-dimensional open set. It therefore
vanishes identically. The zero-block structure holds on all of `R^n`.
We may enclose and normalize the transformed domain to `[0,1]^n`,
retaining its original affine domain constraints, and use derivative
bounds on this larger box.

Let `L_i=ceil(alpha_i T)`, `h_i=2^(-L_i)`, and represent

```
y_i=A_i+rho_i,
A_i=sum_(l=1,...,L_i) 2^(-l) beta_(i,l),
beta_(i,l) binary,    0<=rho_i<=h_i.
```

As before, every input in the box admits this representation. Define

```
P_j(A,rho)=f_j(A)+sum_i (∂_i f_j)(A) rho_i.               (8)
```

The same integral Taylor estimate gives
`|f_j(y)-P_j(A,rho)|<=C_0 2^(-T)`. Choose `T` so this is at most
`ε/2`, and impose `|w_j-P_j(A,rho)|<=ε/2`.

Expression (8) can be represented exactly by a linear lift with the
existing input bits. Expand its fixed-degree polynomials in the
prefix sums. Each term is a product of at most `D` bits, or a product
of at most `D-1` bits times one residual. Repeated occurrences of one
bit can be removed because it is zero or one. A product of distinct
bits indexed by `J` is represented by a continuous variable `v_J` with

```
0<=v_J<=1,     v_J<=beta_b for b in J,
v_J>=sum_(b in J) beta_b-|J|+1.
```

Integral input bits force `v_J` to equal their product. A term
`v_J rho_i` has the exact four-row bounded-product formulation,
because `v_J` is already forced to be zero or one; it does not need
to be declared integer. An empty product is the constant one.
Therefore (8) introduces no new integer variables.

With fixed `n,m,D`, there are at most `O((1+sum_i L_i)^D)` expanded
terms and a bounded number of rows per term. This proves Theorem 2.
Unlike a separate cell enumeration, the polynomial prefix expressions
share the input bits across all outputs.

## Illustrations and limits

A scalar smooth function with nonsingular Hessian at one interior point
has coefficient `n/2`, even when that Hessian is indefinite. A product
of `k>=2` positive variables is a concrete polynomial case: at any
point `x` of the positive orthant, its Hessian is
`H=f(x)diag(1/x)(11^T-I)diag(1/x)`. Both diagonal factors are
invertible, and `11^T-I` has eigenvalues `k-1` once and `-1` with
multiplicity `k-1`, so `H` is nonsingular throughout the positive
orthant, in particular at every interior point of any positive box.
Thus its coefficient is `k/2`, with a compact formulation as above.

A rank-deficient polynomial example in four variables is

```
f(z_1,z_2,w,t)=z_1 w³+z_2(w+w²)+w t²+t⁴.
```

Its Hessian has the fixed zero blocks with `Z=(z_1,z_2)`, `W=w`, and
`R=t`, so `r_all<=3`. Its Hessian at `(1,1,1,1)` has rank three,
so `r_loc=r_all=3` on any box containing that point in its interior.
Its exact leading coefficient is therefore `3/2`, with a compact
`O((1+log(1/ε))⁴)` linear formulation. The symbolic script
`code/quadratic_rank/check_smooth_polynomial.py` checks these ranks and
zero blocks and verifies that all twelve Taylor residual terms have
precision weight at least one for exponents `(0,0,1,1/2)`. It passed.

For simultaneous outputs, full pointwise noncommutative rank suffices
even when every scalar combination of the Hessians is singular. The
matrix-evaluation step in (3) is what recovers the additional rank.

The theorem does not identify the answer when `r_loc<r_all`. Varying
Hessian null spaces or shrinking subspaces can matter. In particular,
the global span is only an upper-bound invariant for general smooth
functions. Its rank is not asserted to be the exact coefficient.
The investigation note `notes/nonquadratic-integer-precision-investigation.md`
records this limitation and the literature search.
