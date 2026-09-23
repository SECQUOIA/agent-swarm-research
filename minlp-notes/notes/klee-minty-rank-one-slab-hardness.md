# One concave coordinate on a path with one aggregate slab

Date: 2026-09-05. Status: two independent written proof reviews PASS,
with independent exact arithmetic tests. Broad rank-one concave quadratic hardness
is established prior work. The scope investigated here is a path of
linear two-variable inequalities plus one scalar aggregate with two bounds.
No degree-two pooling hardness claim follows without a physical interface.

## 1. A telescoping vertex certificate

Fix rational `0<epsilon<1/2`, put `x_0=0`, and let `P_epsilon` be

```
0<=x_1<=1,
epsilon x_(j-1)<=x_j<=1-epsilon x_(j-1),    j=2,...,n.
```

Define the linear function

```
L(x)=x_n-(1-epsilon) sum_(i=1)^(n-1) epsilon^(2(n-i)-1) x_i
```

and the concave quadratic `F(x)=L(x)-x_n^2`. Then

```
F(x)=sum_(j=1)^n epsilon^(2(n-j))
       (x_j-epsilon x_(j-1))(1-epsilon x_(j-1)-x_j).       (1)
```

Indeed each product expands as
`x_j-x_j^2-epsilon x_(j-1)+epsilon^2 x_(j-1)^2`. With the indicated
weights, all intermediate squares cancel, leaving `-x_n^2`; collecting
the linear coefficients gives `L`.

Both factors in every summand are nonnegative on `P_epsilon`, and
all weights are positive. Consequently `F>=0` there. Equality holds
exactly when each coordinate attains one of its two conditional endpoint
bounds. Those choices give precisely the `2^n` Klee–Minty vertices.
The two bounds never coincide because `epsilon<1/2` and every preceding
coordinate belongs to `[0,1]`. The Hessian of `F` is exactly
`-2 e_n e_n^T`, so it has rank one and only one curved coordinate.

For a vertex encoded by bits `u_j`, its recursion is

```
x_j=u_j+(1-2u_j) epsilon x_(j-1).
```

Thus `|x_j-u_j|<=epsilon`. Every vertex has rational coordinates of
polynomial bit length in `n` and the rational encoding of `epsilon`.

## 2. An ordinary NP-complete threshold problem

Take a SUBSET SUM instance of positive integer weights `w_1,...,w_n`
and integer target `B`, with `0<=B<=W=sum_i w_i`. Set
`epsilon=1/(8W)` and intersect the path polytope with the single slab

```
B-1/4 <= sum_i w_i x_i <= B+1/4.                         (2)
```

Consider deciding whether `min F(x)<=0` on this polytope. If a bit
vector `u` attains the subset sum, its Klee–Minty vertex has

```
|sum_i w_i x_i-B| <= epsilon W = 1/8,
```

so it satisfies (2) and has `F=0`. Conversely `F<=0` on the path
polytope forces a vertex. For its bits,

```
|sum_i w_i u_i-B| <= 1/4+1/8 = 3/8 < 1.
```

The left expression is an integer, so it is zero. This proves the
reduction. The powers of `epsilon` in `L` have polynomial bit length,
so the instance is polynomially encoded.

The slab polytope is always nonempty under the stated target range.
The zero point lies in the path polytope, and the all-one vertex has
weighted sum at least `W-1/8`. Convex interpolation reaches any integer
`B<W`; for `B=W`, the all-one vertex lies in the slab. Thus the
minimum is finite and attained on a nonempty compact set. It is zero
for yes instances and positive for no instances.

Membership in NP has a direct certificate here: give the endpoint bit
vector, construct its rational vertex by the recursion, and verify the
slab. Equation (1) verifies its zero objective automatically. Hence this
restricted threshold problem is NP-complete. No strong-hardness,
inverse-polynomial objective gap, or approximation consequence is claimed.

This is one dense aggregate with **two** bounds, not one additional
halfspace. The nonlinear row itself also has a dense linear part.
The complete constraint graph therefore should not be called a path:
the path restriction describes the local linear inequalities after the
global aggregate and quadratic condition are separated out.

### 2.1 Fixed local coefficients by padding

The local coupling coefficient can be fixed to `epsilon=1/4`. Choose
the least integer `r>=0` with `4^(-(r+1))<=1/(8W)`. Place the `n` free
coordinates at positions `1, r+2, 2r+3, ...` along a Klee–Minty path
of dimension `N=n+(n-1)r`. Impose the additional singleton upper bound
`x_j<=1/2` on each intervening padding coordinate. Use the same
telescoping objective `F` on the entire path and put the subset-sum
slab only on the free coordinates.

At a zero of `F`, a padding coordinate must choose its lower branch:
its upper branch is at least `3/4` and violates its singleton bound.
Between successive free coordinates there are therefore `r` exact
multiplications by `1/4`. Each free coordinate differs from its endpoint
bit by at most `4^(-(r+1))`; the first free coordinate is exactly its
bit. Conversely, every choice of free bits extends to a zero of `F`
by taking the lower branch at all padding positions. The same `1/8`
weighted error and `1/4` slab argument now proves NP-hardness. The
all-zero and all-one-free-bit patterns also prove the same nonempty
compactness promise. A certificate consists of the free bits.

Because `r=O(log W)`, this is a polynomial construction. Thus the local
linear inequalities may use only coefficients `0, +/-1, +/-1/4` and
right-hand sides `0, 1/2, 1`. The dense slab weights and geometric
objective coefficients still have varying binary encodings. This is
ordinary NP-completeness, with no strong-hardness claim. The extra
singleton bounds preserve the local path graph. Both independent
reviewers approved this corollary in their written addenda. The second
reviewer's exact checker also verified 1,016 padded endpoint identities
and 661 fixed-coefficient slab target comparisons.

## 3. Consequence for fixed-core decompositions

Set the nonlinear core to the single coordinate `q=x_n`. At fixed `q`,
all remaining conditions form a bounded linear fiber. Away from the slab
and the quadratic row's linear aggregate, the variables form scalar
blocks coupled along a path. Thus fixed core dimension, scalar local
blocks and a fixed number of global aggregate rows do not suffice for
a polynomial algorithm if independent blocks are replaced by general
path-coupled blocks. This contrasts with the repository's
[constructive independent-block theorem](../results/fixed-core-block-polyhedral-optimization.md).
It does not conflict with that theorem, whose independence assumption is
essential and absent here.

## 4. A short parabolic proof of the known exponential shadow

For any fixed `epsilon<1/2`, every vertex maps under
`x -> (x_n,L(x))` to the parabola `(t,t^2)`. Distinct vertices have
distinct `t`: the final endpoint bit chooses disjoint intervals, and
within either interval the endpoint recurrence is invertible; induct
backwards. There are therefore `2^n` such projected vertices.

For a vertex with terminal coordinate `t`, the linear functional
`2t x_n-L(x)` satisfies everywhere on the path polytope

```
2t x_n-L(x) <= 2t x_n-x_n^2
              = t^2-(x_n-t)^2 <= t^2.
```

Equality requires `F=0` and `x_n=t`, hence that unique vertex.
This is a direct exposing tangent certificate. Equivalently, with
`c_i=(1-epsilon)epsilon^(2(n-i)-1)` for `i<n`, the objective
`sum_(i<n)c_i x_i+(2t-1)x_n` uniquely exposes it. All exposing price
parameters belong to `[-1,1]`.

Exponential Klee–Minty shadows are already established by
[Gärtner, Helbling, Ota and Takahashi](https://arxiv.org/pdf/1308.2495),
Section 4. Equation (1) is recorded as a useful alternative proof and
vertex certificate; its separate priority is unclaimed.

## 5. Prior work and verification status

Pardalos and Vavasis, *Quadratic programming with one negative eigenvalue
is NP-hard* (1991), already establish broad concave rank-one hardness;
[primary article](https://doi.org/10.1007/BF00120662). The new investigation
must not claim that broad boundary. The potentially useful distinction
is the exact local path/one-dense-slab structure and the explicit
vertex-forcing identity. A targeted initial search did not identify this
particular formulation, but this is not a complete novelty audit.

Two independent reviewers checked the identity, endpoint characterization,
subset-sum rounding bounds, ordinary NP membership, compactness, fixed-core
consequence, and parabolic exposing proof:

- [First review](review-klee-minty-rank-one-slab.md): six symbolic identities
  and 72 exact continuous quadratic minima over clipped polytopes, checking
  2,784 candidate vertices including new slab-edge intersections.
- [Second review](review-klee-minty-rank-one-slab-second.md): 2,246 exact
  identity, interior-positivity and tangent checks, plus 661 subset-sum
  target comparisons on 28 instances.
- [Author checker](../code/parametric_path_lp/check_rank_one_slab.py):
  eight symbolic dimensions, 1,508 vertex and rounding checks, 1,009
  target comparisons, and 40 strict-interior controls.

These are exact rational checks of finite instances; the proofs establish
the general statements. The primary Pardalos–Vavasis publisher abstract
was inspected directly on 2026-09-05 and expressly states concave
quadratic hardness with one concave direction. The restricted path/slab
claim remains subject to a broader priority audit.
