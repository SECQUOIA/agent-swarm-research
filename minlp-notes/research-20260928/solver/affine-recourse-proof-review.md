# Independent proof review of the affine-recourse rate boundary

Date: 2026-09-28.

Reviewed: [affine-recourse-rate-boundary.md](affine-recourse-rate-boundary.md),
the initial draft with upper bound `4 sqrt(6)/sqrt(2r^2+1)`.
The author then incorporated the factor-two strengthening identified in
this review, and the reviewer re-read the updated theorem and certificate.
The reviewer did not edit the main draft. This is a proof audit, not a
priority determination. No project-wide checks or CI checks were run.

## Verdict

No invalid step was found in the stated theorem or its proof. The
finite-order measure obstruction, the explicit inverse-degree bound, and
the full-preordering degree accounting all hold under the stated
assumptions. The proof has a simple strengthening: its sparse upper-bound
constant can be divided by two. The model is continuous, and the result
concerns this particular sparse decomposition and separator information;
the draft states these limitations correctly.

## Exact local-measure gap

The identity `eta_n=-2E_n` has the correct sign and factor.

For any feasible bag measures with separator marginals `alpha,beta`, the
objective is at least `-int |y| d alpha + int |y| d beta`. The lifts
`x=sign(y)` and `z=|y|` are measurable and feasible, including at zero, and
attain this bound. Thus taking the infimum over the measures is equivalent
to the negative of the maximum of `int |y| d(alpha-beta)`.

Hahn--Banach applies to the closed finite-dimensional polynomial subspace
of `C([-1,1])`. The distance `E_n` is positive because `|y|` is not a
polynomial on that interval. The norm-one annihilating functional is a
signed measure of total variation one. Annihilation of the constant
polynomial gives zero mass, so each Jordan part has mass exactly one-half.
Doubling those parts gives probability measures, and their expectation
difference is `2E_n`. This proves attainment of the extremal difference
without any assumption about SDP attainment or strong duality.

As a separate exact check, `E_2=1/8`: the polynomial `y^2+1/8` has uniform
error `1/8`. Put mass one-half at each of `-1/2,1/2` for `alpha`, and masses
`1/8,3/4,1/8` at `-1,0,1` for `beta`. Their moments agree through degree
two and their absolute-value expectations differ by `1/4=2E_2`. This also
checks the orientation of the two bag marginals.

Actual measures are feasible for every listed preordering positivity
test, so `rho_r <= eta_(2r)=-2E_(2r)` is valid. It does not presuppose that
general feasible truncated functionals have representing measures.

## Fejer witness

Let `s=theta-pi/2`. Expanding the witness gives

```
Q_N = -cos(2Ns)
      - sum_(j=1)^(N-1) (1-j/N)
          [cos((2N-j)s)+cos((2N+j)s)].
```

Every frequency lies between `N+1` and `3N-1`, so all degree-at-most-`n`
polynomials in `cos(theta)` are annihilated. The signs are correct:
for positive even `k`, the shifted cosine has absolute-value correlation
`-2/[pi(k^2-1)]`; for odd `k` the correlation is zero. Every surviving
term of the displayed expansion therefore has positive correlation.

For even `N`, the sum of surviving weights is
`1+2 sum_(j even, 1<=j<N)(1-j/N)=N/2`. Bounding all squared frequencies
by `9N^2` gives the claimed `1/(9pi N)` lower bound. Nonnegativity and
normalization of the Fejer kernel give `int |Q_N|<=1`, even though the
witness itself changes sign. Pushing forward along `cos(theta)` or simply
bounding the composed approximation error justifies its use as a
uniform-approximation dual witness. The resulting theorem constant
`2/[9pi(2r+2)]=1/[9pi(r+1)]` is correct.

## Kernel approximation and sparse certificate

The scalar kernel note defines an even circle probability density `J_m`.
For fixed `y=cos(theta)`, its pushforward under `T -> cos(theta+T)` has
the claimed arcsine kernel density. To check this directly, integrate a
test function over the two preimages `phi` and `-phi`; the resulting
density is `[J_m(theta-phi)+J_m(theta+phi)]/2`.

The displacement estimate follows from
`|cos(theta+T)-cos(theta)|^2 <= 2(1-cos(T))`, integration, and
Cauchy--Schwarz. No pointwise relation between the signs of `t` and `y`
is assumed. The inequality
`0 <= |y|-y sign(t) <= 2|t-y|` holds separately when the signs agree,
when they disagree, and when either variable is zero. Its integration
establishes the approximation bound with the stated `delta_m`.

The identity `K_m(-y,-t)=K_m(y,t)` and symmetry of arcsine measure make
`s_m` odd. Since `K_m` has even degree bound `2m-2`, this improves the
degree of `s_m` to `2m-3`. Therefore `y s_m` has degree at most `2m-2`.
No parity assumption about arbitrary interval-positive polynomials is
needed: the interval representation is used with an even degree *bound*,
and applies to polynomials of smaller, possibly odd, degree as well.

The degree checks are as follows, with `m>=2`:

| Piece | Representation and largest degree |
| --- | --- |
| `p_m +/- y` | `sigma_0+(1-y^2)sigma_1`, each term of degree at most `2m-2` |
| `(1 +/- x)/2` | `(1 +/- x)^2/4+(1-x^2)/4`, degree two |
| First bag product | Degree at most `2m`, using only `1-x^2` and `1-y^2` |
| `(1 +/- s_m)/2` | Same interval representation, padded to degree `2m-2` |
| Second bag product | Degree at most `2m-1`, using only `z-y` or `z+y`, and optionally `1-y^2` |

Products of sums of squares remain sums of squares. All generator
products are squarefree products from the stated local lists. In
particular, `(1-y^2)(z-y)` and `(1-y^2)(z+y)` are permitted by the full
preordering. The draft correctly does not claim membership in the local
quadratic module.

### Strengthening of the upper constant

The second bag needs no additive constant. Set

```
A_m = y s_m + delta_m - xy,
B_m = z - y s_m
    = (1+s_m)(z-y)/2 + (1-s_m)(z+y)/2.
```

The original first-bag argument proves `A_m in T_(1,m)`, and the original
second-bag argument proves `B_m in T_(2,m)`. Their sum is `f+delta_m`.
Consequently, the same proof gives

```
1/[9pi(r+1)] <= -rho_r <= -lambda_r
             <= 2 sqrt(6)/sqrt(2r^2+1) <= 2 sqrt(3)/r.
```

This improves a nonsharp constant without changing the rate or claimed
scope. The original, larger bound remains correct.

The author applied this suggestion and independently checked the
strengthened algebraic identity. A second exact symbolic check by this
reviewer also passed. The updated theorem, Equation (19), Equation (22),
and conclusion `lambda_r>=-delta_r` agree.

## Dense certificate and nonexact decomposition

Expanding the three dense terms gives `z-xy` exactly. Their degrees are
at most three. Their multipliers are squares or a positive constant,
and the last term uses the allowed product `(1-x^2)z`. Thus the claimed
order-two full-preordering exactness is valid for the merged bag.

In any exact polynomial decomposition `f=a(x,y)+b(y,z)`, comparing the
terms involving `x` and `z` forces `a=-xy+p(y)` and `b=z-p(y)`. Local
nonnegativity then forces `p=|y|` on the interval, which a polynomial
cannot satisfy. This rules out an attained exact sparse certificate.
By itself, nonmembership would not rule out a zero, unattained dual gap;
the independent positive quantitative lower bound already rules that out
here. The draft's use of this argument as a qualitative explanation is
appropriate.

The proposed sign-branch corollary is also correct. For
`epsilon in {-1,1}`, add the branch generator `epsilon*y` to the first
bag. Then

```
f = (z-epsilon*y)
    + (epsilon*y)(1-epsilon*x)^2/2
    + (epsilon*y)(1-x^2)/2.
```

The first term belongs to the unchanged second bag. The last two terms
belong to the first bag's full preordering and have degree three.
Therefore each sign branch has an order-two exact sparse certificate
using the original bags. The branch generator is needed only in the
first bag for this argument. The two branches cover the original set.
Both identities were checked by exact symbolic expansion.

## Verification performed and limits

The targeted command actually run was a single inline Python script,
`python - <<'PY' ... PY`, using `fractions.Fraction` and `sympy`. It checked:

- The dense certificate identity by exact symbolic expansion.
- Fejer frequency extrema, even-frequency weight sums, and the rational
  coefficient of the correlation lower bound for every even `N` from two
  through 100.
- Exact Jackson normalization and the `1-g_1` formula for `m=2,...,41`.
- The largest nonzero odd index `2m-3` in the sign convolution, using
  `int sign(t) T_k(t) dmu = 2 sin(k pi/2)/(k pi)`.
- The moment matching and expectation difference of the explicit
  degree-two extremal measures above.

All checks passed. These finite checks detect sign, factor, and indexing
errors in representative instances; the preceding symbolic arguments
justify the statements for arbitrary orders. They do not mechanically
verify the use of Hahn--Banach, Riesz representation, or the univariate
interval positivity theorem. No Lean proof was attempted.

After the author's revision, a second targeted inline command
`python - <<'PY' ... PY`, using `sympy`, verified the identity with
abstract symbols `h=s_m(y)` and `d=delta_m`, and the displayed sign-branch
certificate separately for `epsilon=-1` and `epsilon=1`. All three
symbolic differences expanded to zero.

The rate exponent is consequential for this hierarchy because an
inverse-square guarantee on fixed private domains cannot extend to all
affine recourse domains. It is not a lower bound on optimizing the
underlying problem, which has the displayed small dense certificate.
Publication priority, equivalence with earlier sparse-certificate
examples, and the broader significance relative to existing quantitative
sparse positivity theorems require a separate literature comparison.
