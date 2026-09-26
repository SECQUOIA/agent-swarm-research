# Proofs of Theorem 12 and Proposition 11

Date: 2026-09-23. Companion to [theory.md](theory.md), Sections 4b and 5. Status:
complete proofs by a subagent, with numerical checks; not yet independently reviewed.

## Summary

- **Theorem 12 is true.** Below it is stated precisely and proved. The needed
  regularity is: each univariate function `h_k` is `C^2` on an open interval
  around `v_a(x*)`, its argument's value at `x*`. This gives `o(w^2)`
  remainders, uniform on compact shape sets. If every `h_k` is `C^3`, or only
  has a locally Lipschitz `h_k''`, the remainders are `O(w^3)`. The recursion for
  `ell` and `E` is given explicitly in A.1. The sketch in theory.md misses one step: when `h'(a*) != 0`, the
  univariate `mid` rule clips the argument at an interval endpoint, and the
  sketch does not show that this clipping is inactive at second order. Property
  (P_k) below closes that gap: up to `o(w^2)`, the composite McCormick relaxation is
  never weaker than natural interval bounds. The same property shows that the
  variant which clips `cv_k`/`cc_k` at the interval bounds has the same
  expansion.
- **Correction to theory.md (Theorem 12 hypothesis).** Theorem 12 assumes `x*`
  is in the interior of `B_0`, yet theory.md uses it for Proposition 11, where
  `x*` lies on the boundary. The interior assumption is not needed: the proof
  uses only smoothness of the factors near `x*`, and the expansion holds for every
  compact set of shapes, including degenerate ones with zero extents. The
  corrected statement is Theorem 12 below.
- **Minor imprecisions in the sketch.** The recursion also depends on the values
  `v_k(x*)`, through sign selections, and on `h_k'(a*)`, not only on gradients,
  `ell` and `h''`. When `h'(a*) = 0`, the point `z^min` of the `mid` rule can
  jump anywhere in the interval, but this has no effect because the term is
  multiplied by `h'(a*) = 0`.
- **Proposition 11 is true.** The needed uniformity assumption (T_∂) is
  uniformity on compact subsets of the closed cone of admissible shapes, which
  includes shapes with vanishing active extents. Theorem 12 delivers it. The
  proof gives free-width contraction by a factor at most `lambda` per round in the `u_F`
  gauge after one step, active widths `<= (epsilon + (G_0 + o(1)) w_k^2)/g_i`, and
  a matching lower bound for one step (Lemma B1). No statement in theory.md
  Section 5 was found to be false.
- **Numerical checks** (A.5, B.4). The error `|(cv - v)/w^2 + E^cv|` decreases
  linearly in `w`, over all factors of 9 hand-picked expressions at 23 points
  and 25 random factorable DAGs. For Proposition 11, exact iterated OBBT gives
  a free-width ratio of 0.724745, matching `rho(1) = 0.724745`. The ratio
  `width_1(B_{k+1})/(epsilon - m_k)` tends to 1. For `epsilon > 0`, the stall
  constants match the predictions to 4 digits.

---

## Part A. Theorem 12

### A.1 Definitions

**Factorable function.** `v_1, ..., v_m` with `v_i = x_i` for `i <= n`. For
`k > n`, each factor is one of the following: a constant `c`; `v_a + v_b`;
`c v_a`; `v_a v_b` (with `a = b` allowed); or `h_k(v_a)`, where `a, b < k` and
`h_k` is a real function of one variable. Set `f = v_m`.

**Natural interval arithmetic** on a box `B = [x^L, x^U]`:
`[x_i^L, x_i^U]` for `x_i`; `[c, c]` for a constant; endpoint sums for sums;
`c[a^L, a^U]` for scalings (endpoints swapped if `c < 0`);
`[min P, max P]` with `P = {a^L b^L, a^L b^U, a^U b^L, a^U b^U}` for products;
and the exact image `[min_Z h, max_Z h]` of `Z = [a^L, a^U]` for `h(v_a)`.

**Composite McCormick relaxation** (McCormick 1976; in the form of Mitsos,
Chachuat and Barton, SIAM J. Optim. 20 (2009) 573–601, which states the
univariate composition with `mid` and the product rule below). Write
`a = v_a(x)`, `[a^L, a^U]` for its interval, and `cv_a`, `cc_a` for its
relaxations.

- Variables: `cv = cc = x_i`. Constants: `cv = cc = c`.
- Sums: `cv = cv_a + cv_b`, `cc = cc_a + cc_b`. Scaling by `c >= 0`: `c cv_a`,
  `c cc_a`. Scaling by `c < 0`: `cv = c cc_a`, `cc = c cv_a`.
- Products (MCB 2009 product rule):
  ```
  alpha1 = min(b^L cv_a, b^L cc_a),  alpha2 = min(a^L cv_b, a^L cc_b),
  beta1  = min(b^U cv_a, b^U cc_a),  beta2  = min(a^U cv_b, a^U cc_b),
  cv = max(alpha1 + alpha2 - a^L b^L, beta1 + beta2 - a^U b^U),
  gamma1 = max(b^L cv_a, b^L cc_a),  gamma2 = max(a^U cv_b, a^U cc_b),
  delta1 = max(b^U cv_a, b^U cc_a),  delta2 = max(a^L cv_b, a^L cc_b),
  cc = min(gamma1 + gamma2 - a^U b^L, delta1 + delta2 - a^L b^U).
  ```
  For two variables this is McCormick's bilinear envelope.
- Univariate: with `Z = [a^L, a^U]`, `h^cv_Z` and `h^cc_Z` the convex and
  concave envelopes of `h` on `Z`, `z^min` any minimizer of `h^cv_Z` on `Z`, and
  `z^max` any maximizer of `h^cc_Z` on `Z`,
  `cv = h^cv_Z(mid(cv_a, cc_a, z^min))`, `cc = h^cc_Z(mid(cv_a, cc_a, z^max))`.
  Here `mid` is the median of three numbers.

The relaxed objective is `phi_B = cv_m`. Validity (`cv_k <= v_k <= cc_k` and
`v_k in [v_k^L, v_k^U]` on `B`) is standard and is used below.

**Shapes and uniformity.** For `d = (d^-, d^+) in R^{2n}_{>=0}` let
`D(d) = prod_i [-d_i^-, d_i^+]`, `B_w = x* + w D(d)` and `x_w = x* + w xi` with
`xi in D(d)`. For a compact `K ⊂ R^{2n}_{>=0}`, let
`S_K = {(d, xi) : d in K, xi in D(d)}`, which is compact. A quantity is
`O_K(w^j)` if it is bounded by `C w^j` on `S_K` for `0 < w <= w_K`. It is
`o_K(w^2)` if its supremum over `S_K`, divided by `w^2`, tends to 0. For a real
number `t`, write `t^+ = max(t, 0)` and `t^- = max(-t, 0)`.

**Tangent data** (the recursion). Let `a* = v_a(x*)`, `b* = v_b(x*)` and
`p_k(xi) = grad v_k(x*)^T xi`. Define `[ell_k^L(d), ell_k^U(d)]`,
`E_k^cv(d, xi)` and `E_k^cc(d, xi)` by the following rules.

- `x_i`: `p = xi_i`, `[ell^L, ell^U] = [-d_i^-, d_i^+]`, `E^cv = E^cc = 0`.
  Constant: `p = 0`, `ell = [0, 0]`, `E = 0`.
- Sum: `ell` and `E` add componentwise.
- `c v_a`: for `c >= 0`, `ell = c ell_a`, `E^cv = c E_a^cv`, `E^cc = c E_a^cc`.
  For `c < 0`, `ell = [c ell_a^U, c ell_a^L]`, `E^cv = |c| E_a^cc`,
  `E^cc = |c| E_a^cv`.
- `v_a v_b`: `p = b* p_a + a* p_b`, `[ell] = b*[ell_a] + a*[ell_b]`
  (interval arithmetic), and
  ```
  E^cv = b*^+ E_a^cv + b*^- E_a^cc + a*^+ E_b^cv + a*^- E_b^cc
         + min{ (p_a - ell_a^L)(p_b - ell_b^L), (ell_a^U - p_a)(ell_b^U - p_b) },
  E^cc = b*^+ E_a^cc + b*^- E_a^cv + a*^+ E_b^cc + a*^- E_b^cv
         + min{ (ell_a^U - p_a)(p_b - ell_b^L), (p_a - ell_a^L)(ell_b^U - p_b) }.
  ```
- `h(v_a)`: with `h1 = h'(a*)`, `h2 = h''(a*)` and
  `s_a = (p_a - ell_a^L)(ell_a^U - p_a)`, set `p = h1 p_a`, `[ell] = h1 [ell_a]`, and
  ```
  E^cv = (h2^-/2) s_a + h1^+ E_a^cv + h1^- E_a^cc,
  E^cc = (h2^+/2) s_a + h1^+ E_a^cc + h1^- E_a^cv.
  ```

`[ell_k]` is natural interval arithmetic applied to the linearized factor
sequence over `D(d)`. By induction `p_k(xi) in [ell_k^L(d), ell_k^U(d)]` for
`xi in D(d)`, because interval arithmetic contains the linearized values. So
every factor of the form `p - ell^L` or `ell^U - p` is nonnegative, and
`E_k^{cv,cc} >= 0`. Also by induction, `ell_k` is continuous and positively
homogeneous of degree 1 in `d`, and `E_k` is continuous and positively
homogeneous of degree 2 in `(d, xi)`.

### A.2 Statement

**Theorem 12.** Let `x* in R^n`. For every univariate factor `v_k = h_k(v_a)`,
suppose `h_k` is `C^2` on an open interval containing `v_a(x*)`. Let
`K ⊂ R^{2n}_{>=0}` be compact. Then there is `w_K > 0` such that, for
`0 < w <= w_K`, all intervals and relaxations on `B_w` are defined. Moreover,
for every factor `k`, uniformly on `S_K`:

```
(I_k)  v_k^{L,U}(B_w) = v_k(x*) + w ell_k^{L,U}(d) + O_K(w^2),
(R_k)  cv_k(x_w) = v_k(x_w) - w^2 E_k^cv(d, xi) + o_K(w^2),
       cc_k(x_w) = v_k(x_w) + w^2 E_k^cc(d, xi) + o_K(w^2),
(P_k)  v_k^L(B_w) - cv_k(x_w) <= o_K(w^2),   cc_k(x_w) - v_k^U(B_w) <= o_K(w^2).
```

If each `h_k''` is Lipschitz near `v_a(x*)` (for example `h_k in C^3`), every
`o_K(w^2)` can be replaced by `O_K(w^3)`. Consequently, with `g = grad f(x*)`,

```
phi_{B_w}(x_w) = f(x*) + w g^T xi + w^2 Q(d, xi) + o_K(w^2),
Q(d, xi) = xi^T grad^2 f(x*) xi / 2 - E_m^cv(d, xi).
```

The box `B_0` plays no role. If `x*` lies on the boundary of `B_0`, apply the
theorem with `K` restricted to shapes for which `B_w ⊆ B_0` (Part B).

### A.3 Lemmas

**Lemma A1 (mid).** Let `cv <= v <= cc`, `v in Z = [L, U]` and `z in Z`. Then
`m = mid(cv, cc, z)` lies in `[cv, cc] ∩ Z`. If `z = L`, then `m = max(cv, L)`. If
`z = U`, then `m = min(cc, U)`.

*Proof.* Since `cv <= cc`, `m` is the projection of `z` onto `[cv, cc]`, so
`m in [cv, cc]`. If `z < cv`, then `m = cv`, with `L <= z < cv <= v <= U`. If
`z > cc`, then `m = cc`, with `L <= v <= cc < z <= U`. Otherwise `m = z in Z`.
If `z = L <= v <= cc`, the projection is `max(cv, L)`. The case `z = U` is
symmetric. QED.

**Lemma A2 (Lipschitz envelopes).** If `psi` is `Lambda`-Lipschitz on
`[alpha, beta]`, its convex and concave envelopes there are `Lambda`-Lipschitz.

*Proof.* Let `c` be the convex envelope. The affine functions
`A_beta(y) = psi(beta) - Lambda(beta - y)` and
`A_alpha(y) = psi(alpha) - Lambda(y - alpha)` are minorants of `psi`, so
`c >= A_beta` and `c >= A_alpha`. Since `c <= psi` and `A_beta(beta) = psi(beta)`,
we get `c(beta) = psi(beta)`, and likewise `c(alpha) = psi(alpha)`. For
`alpha <= y < y' <= beta`, the three-chord inequality for convex `c` gives

`(c(y') - c(y))/(y' - y) <= (c(beta) - c(y))/(beta - y) <= (psi(beta) - A_beta(y))/(beta - y) = Lambda`

when `y' < beta`; the case `y' = beta` is immediate. Symmetrically, the slope
is at least `(c(y') - c(alpha))/(y' - alpha) >= -Lambda`. For the concave
envelope, apply this to `-psi`. QED.

**Lemma A3 (envelope of a `C^2` function on a short interval).** Let `h` be
`C^2` on `[a* - r, a* + r]`, let `c = h''(a*)`, and let
`omega(s) = sup{ |h''(y) - c| : |y - a*| <= s }`. Then `omega(s) -> 0`, and if
`h''` is `M`-Lipschitz, `omega(s) <= M s`. For every `Z = [L, U]` contained in
`[a* - s, a* + s]` with `s <= r`, and every `y in Z`:

```
| h(y) - h^cv_Z(y) - (c^-/2)(y - L)(U - y) | <= omega(s) s^2,
| h^cc_Z(y) - h(y) - (c^+/2)(y - L)(U - y) | <= omega(s) s^2,
```

and `h^cv_Z - h'(a*) id` and `h^cc_Z - h'(a*) id` are
`(s sup_{|y-a*|<=s} |h''|)`-Lipschitz on `Z`.

*Proof.* Let `q(y) = h(a*) + h'(a*)(y - a*) + (c/2)(y - a*)^2` and
`rem = h - q`. Then `rem(a*) = rem'(a*) = 0` and `|rem''| <= omega(s)`, so
`|rem| <= omega(s) s^2/2 =: eta` on `Z`. Envelopes are monotone and commute with
adding constants, so `conv q - eta <= conv h <= conv q + eta`, and hence
`|(h - conv h) - (q - conv q)| <= 2 eta`. If `c >= 0`, then `conv_Z q = q`. If
`c < 0`, then `q` is concave and `conv_Z q` is its chord. The chord is convex
and lies below `q` on `Z`. Any convex minorant of `q` lies below the chord,
because it lies below `q` at the endpoints. The difference `q - chord` is a
quadratic with leading coefficient `c/2` that vanishes at `L` and `U`, so it
equals `(|c|/2)(y - L)(U - y)`. The concave envelope is symmetric. For the
Lipschitz claim, envelopes commute with adding affine functions, so
`h^cv_Z - h'(a*) id` is the convex envelope of `psi = h - h'(a*) id`. On `Z`,
`|psi'| <= s sup|h''|`, and Lemma A2 applies. QED.

**Lemma A4 (monotone argmin).** If `h' > 0` on `Z = [L, U]`, then `L` is the unique
minimizer of `h^cv_Z` and `U` is the unique maximizer of `h^cc_Z`. If `h' < 0`,
the roles of `L` and `U` are exchanged.

*Proof.* Let `mu = min_Z h' > 0`. The affine function
`h(L) + mu (y - L)` is a convex minorant of `h`, so
`h^cv_Z(y) >= h(L) + mu (y - L) > h(L) >= h^cv_Z(L)` for `y > L`. The concave
case is symmetric. QED.

**Lemma A5 (sign selections).** Let `s_w` be a coefficient with
`|s_w - s*| <= C w`, and let `cv <= v <= cc` with `cc - cv <= C' w^2`. Define
`v~ = cv, cc, v` according to whether `s* > 0`, `s* < 0` or `s* = 0`. Then
`min(s_w cv, s_w cc) = s_w v~ + rho`. Here `rho = 0` if `s* != 0` and
`w < |s*|/C`, and `|rho| <= C C' w^3` if `s* = 0`. The same holds for `max`,
with `cv` and `cc` exchanged in the definition of `v~`.

*Proof.* The minimum is `s_w cv` if `s_w >= 0` and `s_w cc` if `s_w <= 0`. If
`s* != 0`, the sign of `s_w` is that of `s*` for `w < |s*|/C`. If `s* = 0`, both
`min(s_w cv, s_w cc)` and `s_w v` lie in the interval `s_w [cv, cc]`, whose
length is at most `C w C' w^2`. QED.

### A.4 Proof of Theorem 12

Let `R_K = max_{d in K} |d|_inf`. Then `|xi|_inf <= R_K` on `S_K`, and
`B_w ⊆ x* + w R_K [-1,1]^n`. By induction over `k`, each `v_k` is `C^2` on a
neighbourhood `N` of `x*`. Choose `N` so small that the argument of each
univariate factor stays in the interval where `h_k` is `C^2`. Taylor's theorem
then gives, uniformly on `S_K`,

```
(T1)  v_k(x_w) = v_k(x*) + w p_k(xi) + O_K(w^2).
```

We prove `(I_k)`, `(R_k)` and `(P_k)` by induction over `k`. By `(I_k)`, every
interval `[v_k^L, v_k^U]` lies in `v_k(x*) + [-C_k w, C_k w]`, so for small `w`
the arguments of univariate factors stay where `h_k` is `C^2`. This makes all
objects well defined. The constants below depend only on `K` and the factorable
function. Continuity of `E` on the compact set `S_K` gives
`cc_a - cv_a = w^2(E_a^cc + E_a^cv) + o_K(w^2) = O_K(w^2)`.

*Variables, constants.* `ell` is exact and `cv = cc = v`, so `E = 0` and `(P)`
holds.

*Sums and scalings.* The expansions add. For `(P)`,
`v^L - cv = (a^L - cv_a) + (b^L - cv_b) <= o_K(w^2)`. For `c < 0`,
`v^L - cv = c a^U - c cc_a = |c| (cc_a - a^U) <= o_K(w^2)`, and
`cv = c cc_a = c a - w^2 |c| E_a^cc + o_K(w^2)`.

*Products `v_k = v_a v_b`.*

`(I_k)`: each vertex product is
`a^i b^j = a* b* + w (b* ell_a^i + a* ell_b^j) + O_K(w^2)`. The functions
`min` and `max` are 1-Lipschitz for the sup norm, and
`min_{i,j}(b* ell_a^i + a* ell_b^j) = min_i b* ell_a^i + min_j a* ell_b^j`.
This gives `ell_k = b*[ell_a] + a*[ell_b]`.

`(R_k)`: by `(I_a)` and `(I_b)`, the coefficients `b^L, b^U` are within
`O_K(w)` of `b*`, and `a^L, a^U` are within `O_K(w)` of `a*`. By Lemma A5,

```
alpha1 = b^L a~ + O(w^3),  beta1 = b^U a~ + O(w^3),
alpha2 = a^L b~ + O(w^3),  beta2 = a^U b~ + O(w^3),
```

with the same `a~ in {cv_a, cc_a, a}`, chosen by the sign of `b*`, in `alpha1`
and `beta1`, and the same `b~`, chosen by the sign of `a*`, in `alpha2` and
`beta2`. This is the key point: when `a* != 0`, the endpoints `a^L` and `a^U`
have the same sign for small `w`. When `a* = 0`, the selection only costs
`O(w^3)`. Using `b^L alpha + a^L beta - a^L b^L = alpha beta - (alpha - a^L)(beta - b^L)`
and `b^U alpha + a^U beta - a^U b^U = alpha beta - (a^U - alpha)(b^U - beta)`,

```
(*)  cv_k = M(a~, b~) + O(w^3) = a~ b~ - min{ (a~ - a^L)(b~ - b^L), (a^U - a~)(b^U - b~) } + O(w^3),
```

where `M` is McCormick's bilinear underestimator on
`Pi = [a^L, a^U] x [b^L, b^U]`. Since `a~ - a = O(w^2)` and `b - b* = O(w)`,

`a~ b~ = ab + b*(a~ - a) + a*(b~ - b) + O(w^3)`.

By `(R_a)`, `b*(a~ - a) = -w^2 (b*^+ E_a^cv + b*^- E_a^cc) + o(w^2)`. The two
cases are `a~ = cv_a` with `b* > 0`, and `a~ = cc_a` with `b* < 0`. The term
`a*(b~ - b)` is analogous. Next,
`a~ - a^L = (a - a^L) + O(w^2) = w (p_a - ell_a^L) + O(w^2)` by (T1) and `(I_a)`,
and likewise for the other three differences. So each product in the `min` of
`(*)` equals `w^2` times the corresponding product in `E_k^cv`, plus `O(w^3)`.
Because `min` is 1-Lipschitz, `cv_k = v_k - w^2 E_k^cv + o(w^2)`. The concave
side is the same argument with `max` selections, using
`b^L alpha + a^U beta - a^U b^L = alpha beta + (a^U - alpha)(beta - b^L)` and
`b^U alpha + a^L beta - a^L b^U = alpha beta + (alpha - a^L)(b^U - beta)`.

`(P_k)`: `M` is the convex envelope of `alpha beta` on `Pi`, so
`M >= min_Pi alpha beta = v_k^L` on `Pi`. `M` is Lipschitz, with constant
`max(|a^L| + |b^L|, |a^U| + |b^U|) = O(1)` in the sup norm. By
`cv_a <= a <= cc_a`, `a in [a^L, a^U]` and `(P_a)`, `(P_b)`, the point
`(a~, b~)` lies within sup-distance `o(w^2)` of `Pi`. With `(*)`, this gives
`cv_k >= v_k^L - o(w^2)`. The concave side is symmetric.

*Univariate `v_k = h(v_a)`.* Let `Z = [a^L, a^U]`. By `(I_a)`,
`Z ⊆ [a* - s_w, a* + s_w]` with `s_w = C w`.

`(I_k)`: on `Z`, `h(y) = h(a*) + h'(a*)(y - a*) + O(w^2)`, and the minimum over
`Z` of `h'(a*)(y - a*)` is `w min(h'(a*) ell_a^L, h'(a*) ell_a^U) + O(w^2)`.

`(P_k)`, which holds exactly: let `m = mid(cv_a, cc_a, z^min)`. By Lemma A1,
`m in Z`, since `z^min in Z` and `a in Z`. So
`cv_k = h^cv_Z(m) >= min_Z h^cv_Z = min_Z h = v_k^L`. Here the constant
`min_Z h` is a convex minorant of `h`, and `h^cv_Z <= h`. Similarly
`cc_k <= v_k^U`.

`(R_k)`: write

```
cv_k = h(a) - [h(a) - h^cv_Z(a)] + [h^cv_Z(m) - h^cv_Z(a)].
```

By Lemma A3, the first bracket is
`(h''(a*)^-/2)(a - a^L)(a^U - a) + omega(s_w) s_w^2`, which equals
`w^2 (h''(a*)^-/2) s_a + o(w^2)`. This holds in every case, including
`h''(a*) = 0` and sign changes of `h''` inside `Z`, because the comparison is
with the quadratic model, not with the convexity type of `h` on `Z`. By Lemma
A1, `m, a in Z` and `|m - a| <= cc_a - cv_a = O(w^2)`. By the Lipschitz part of
Lemma A3,

`h^cv_Z(m) - h^cv_Z(a) = h'(a*)(m - a) + O(w) O(w^2)`.

It remains to find `h'(a*)(m - a)`.

- `h'(a*) = 0`: the term is 0. Here `z^min` may be anywhere in `Z` and may
  jump with `w`; this does not matter.
- `h'(a*) > 0`: for small `w`, `h' > 0` on `Z`. By Lemma A4, `z^min = a^L`, and
  by Lemma A1, `m = max(cv_a, a^L)`. Hence
  `m - a = (cv_a - a) + (a^L - cv_a)^+`. By `(P_a)`, `(a^L - cv_a)^+ = o(w^2)`,
  so `m - a = -w^2 E_a^cv + o(w^2)`. This is the step missing from the sketch:
  without `(P_a)`, the clipping at `a^L` could change the second-order term.
- `h'(a*) < 0`: `z^min = a^U` and `m = min(cc_a, a^U)`. By `(P_a)`,
  `m - a = w^2 E_a^cc + o(w^2)`, so `h'(a*)(m - a) = -w^2 |h'(a*)| E_a^cc + o(w^2)`.

Adding the three parts gives `cv_k = v_k - w^2 E_k^cv + o(w^2)`. The concave side
uses `z^max`, which is `a^U` if `h' > 0` and `a^L` if `h' < 0`.

*Remainder order.* If each `h_k''` is Lipschitz, then `omega(s) = O(s)` in
Lemma A3. Every remainder in the induction is then `O(w^3)`, including those
in `(P_k)`.

*Consequence for `phi`.* `v_m` is `C^2` near `x*`, so
`v_m(x_w) = f(x*) + w g^T xi + (w^2/2) xi^T grad^2 f(x*) xi + o_K(w^2)`, or
`O_K(w^3)` if `v_m` is `C^3`. Combine this with `(R_m)`. QED.

**Remarks.**

1. *Degenerate cases covered.* The proof covers the following cases.
   - Zero-width first-order intervals. For example, `x y` at `x* = 0` has
     `ell = [0, 0]`, and a subsequent `h(xy)` gets no secant term because
     `s_a = 0`. Its interval has width `O(w^2)`, so the envelope gap is
     `O(w^4)`.
   - Products with factors equal to 0 at `x*` (Lemma A5 with `s* = 0`).
   - Inflection points `h''(a*) = 0` (Lemma A3).
   - Critical points `h'(a*) = 0`, where `z^min` or `z^max` is interior and
     may jump.
   - Degenerate shapes with zero extents.
2. *Interval clipping.* Some implementations replace `cv_k` by
   `max(cv_k, v_k^L)` and `cc_k` by `min(cc_k, v_k^U)`. By `(P_k)`, this changes
   the values by `o(w^2)`. Every rule is Lipschitz in its `(cv, cc)` inputs with
   `O(1)` constants, so the expansions and `E` are unchanged. In detail, by
   induction over `k`: clipping does not change the intervals; the rule for factor
   `k` applied to clipped inputs differs from the unclipped value by `O(1)` times
   the input differences, which are `o_K(w^2)` by induction (the univariate
   rule is `h^cv_Z` of a 1-Lipschitz `mid`, and `h^cv_Z` is Lipschitz with
   constant `max_Z |h'| = O(1)` by Lemma A2; the product rule has interval
   endpoints as coefficients); clipping is 1-Lipschitz and moves the unclipped
   value by `(v_k^L - cv_k)^+ = o_K(w^2)`. This clipped variant is Step 6 of
   Definition 9 of Scott, Stuber and Barton (2011), whose Theorem 4 gives the
   finite-box isotonicity (R2) that theory.md uses; that theorem does not cover
   the unclipped rule of A.1. The statement here is local and asymptotic
   (uniform on compact shape sets as `w -> 0`), not a bound on arbitrary boxes.
3. *Other univariate relaxations.* `E` depends on the rules. If
   `h^cv_Z` is replaced by a weaker convex underestimator whose gap is of
   order `w^2`, `E` changes. For example, writing `x^2` as the product `x * x`
   gives `E^cv = min{(xi + d^-)^2, (d^+ - xi)^2}` at `x* = 0`, instead of `0`
   for the univariate square. Section 4 of theory.md assumes squares are kept
   exact.
4. *Regularity.* `C^2` near the points `v_a(x*)` is the natural hypothesis. It is
   local, so no global condition on `B_0` or on the range of `h_k` over `B_0` is
   needed. If some `h_k` is only `C^{1,1}`, the scaled envelope gap need not
   converge. If `h_k` is not differentiable at `a*` (for example `|t|` at 0),
   the relaxation is not first-order exact there, and the theorem does not
   apply.
5. Because `E_m^cv` is bounded on `S_K`, the theorem also shows that
   `phi_B >= f - C w(B)^2` locally, consistent with Bompadre and Mitsos (2012). In
   addition, it identifies the second-order coefficient.

### A.5 Numerical check

Code: `code/proofs_checks/mccormick_expansion.py`. It implements the definitions
of A.1 directly: exact univariate ranges; exact convex and concave envelopes,
including one inflection point inside the interval, found by solving for the
tangent point; the MCB product rule; and the `mid` rule. It also implements
the recursion of A.1. For 300 random shapes per point, it measures
`max |(cv_k - v_k)/w^2 + E_k^cv|` and `max |(cc_k - v_k)/w^2 - E_k^cc|` over
**all factors** `k`. About 10% of the extents are set to zero, and about 40% of
the coordinates of `xi` are placed on faces of `D(d)`.

| expression | `x*` | w = 1e-1 | 1e-2 | 1e-3 | 1e-4 |
|---|---|---|---|---|---|
| `x*y*z` | (0.5, -0.7, 1.2) | 1.9e-1 | 1.9e-2 | 1.9e-3 | 1.9e-4 |
| `x*y*z` | (0, 0, 1) | 1.4e-1 | 1.4e-2 | 1.4e-3 | 1.4e-4 |
| `x*y*z` | (0, 0, 0) | 2.0e-1 | 2.0e-2 | 2.0e-3 | 2.0e-4 |
| `exp(x)*y` | (0.3, -0.4) | 1.1e-1 | 1.0e-2 | 1.0e-3 | 1.0e-4 |
| `exp(x)*y` | (0.3, 0) | 1.1e-1 | 1.0e-2 | 1.0e-3 | 1.0e-4 |
| `sin(x+y)*x` | (0.4, 0.3) | 2.8e-1 | 2.8e-2 | 2.8e-3 | 2.8e-4 |
| `sin(x+y)*x` (inflection, `h''=0`) | (0.2, -0.2) | 2.0e-1 | 2.0e-2 | 2.0e-3 | 2.0e-4 |
| `sin(x+y)*x` (all values 0) | (0, 0) | 2.0e-1 | 2.0e-2 | 2.0e-3 | 2.0e-4 |
| `sin(x+y)*x` (critical, `h'=0`) | (pi/4, pi/4) | 3.8e-1 | 3.9e-2 | 3.9e-3 | 3.9e-4 |
| `sin(x+y)*x` | (1, 2) | 1.9e-1 | 1.9e-2 | 1.9e-3 | 1.9e-4 |
| `(x*y)^2`, square as univariate | (0, 0) | 3.8e-2 | 3.8e-4 | 3.8e-6 | 3.8e-8 |
| `(x*y)^2`, square as univariate | (1, -0.5) | 5.4e-1 | 5.0e-2 | 5.0e-3 | 5.0e-4 |
| `(x*y)*(x*y)`, as product | (0, 0) | 5.3e-2 | 5.3e-4 | 5.3e-6 | 5.3e-8 |
| `(x*y)*(x*y)`, as product | (1, -0.5) | 9.3e-1 | 9.9e-2 | 1.0e-2 | 1.0e-3 |
| `log(1+x^2)*y` (zero-width `1+x^2`) | (0, 0.7) | 1.3e-1 | 1.3e-2 | 1.3e-3 | 1.3e-4 |
| `log(1+x^2)*y` | (0.5, -1) | 1.5e-1 | 1.5e-2 | 1.5e-3 | 1.5e-4 |
| `log(1+x^2)*y` | (0, 0) | 1.7e-1 | 1.7e-2 | 1.7e-3 | 1.7e-4 |
| `exp(-x*y)*z` | (0.6, 0.8, -1.1) | 1.7e-1 | 1.7e-2 | 1.8e-3 | 1.8e-4 |
| `exp(-x*y)*z` | (0, 0.5, 0) | 3.1e-1 | 5.6e-2 | 5.6e-3 | 5.6e-4 |
| `sin(x*y+z)` (`h'<0`, `h''=0`) | (0.5, 0.5, pi-0.25) | 1.9e-1 | 1.7e-2 | 1.7e-3 | 1.7e-4 |
| `sin(x*y+z)` | (0.3, -0.2, 1) | 2.9e-1 | 2.4e-2 | 2.4e-3 | 2.4e-4 |
| `cos(x)*cos(y) - x*y` (`h'=0`) | (0, 0) | 1.1e-2 | 1.1e-4 | 1.1e-6 | 3.8e-8 |
| `cos(x)*cos(y) - x*y` | (1.2, -0.4) | 1.1e-1 | 1.1e-2 | 1.1e-3 | 1.1e-4 |

The predicted `E` at the root ranges up to about 4 in these cases, so the
limits are not trivial. Every error decreases by a factor of 10 per decade of
`w`, which is the `O(w^3)` remainder expected for `C^3` functions. Some cases
decrease faster, for example because of exact homogeneity at `x* = 0`. The
quantity `max (v_k^L - cv_k)^+/w^2` of property (P_k) is `O(w)` or below rounding
level `~1e-16/w^2` in all cases.

`code/proofs_checks/random_factorable.py` runs 25 random DAGs of depth 5 over
sums, scalings, products, `exp`, `sin`, `cos`, `sqr` and `log(0.5 + sqr)`. About
30% of the coordinates of `x*` are set to 0, and 60 shapes are used per DAG.
Every DAG whose error is above rounding level has `err(1e-4)/err(1e-3) <= 0.100`.

---

## Part B. Proposition 11

### B.1 Setting and assumption

Let `B_0 = [l, u]` and let `x*` be a global minimizer of `P`, with `f* = f(x*)`.
Let `A` be the set of indices with `x*_i = l_i`, and `F` its complement, with
`l_i < x*_i < u_i` for `i in F`. An active upper bound reduces to this case by
the substitution `x_i -> -x_i`. Let `g in R^n` satisfy `g_i > 0` for `i in A`
(strict complementarity) and `g_i = 0` for `i in F`. For McCormick relaxations,
`g = grad f(x*)` and these sign conditions are the KKT conditions with strict
complementarity.

*Admissible shapes.* Let `S = {d in R^{2n}_{>=0} : d_i^- = 0 for i in A}`, a
closed cone. Every box `B` with `x* in B ⊆ B_0` equals `x* + w D(d)` for some
`d in S` and any `w > 0`: its lower bound in `A` must be `l_i = x*_i`. Let
`G = {(d, xi) : d in S, xi in D(d)}`. For a free shape `d_F`, let `iota(d_F)` be
the shape with free part `d_F` and zero active extents. Define `iota(xi_F)`
similarly.

**Assumption (T_∂).** There is a continuous `Q : G -> R` such that, for every
compact `K ⊆ S`,

```
rho_K(w) = sup_{d in K, xi in D(d)} | phi_{x*+wD(d)}(x* + w xi) - f* - w g^T xi - w^2 Q(d, xi) | / w^2  ->  0.
```

The essential point is that `K` may contain shapes with `d_A^+ = 0` or with
small `d_A^+`. This is the uniformity near vanishing active extents that the
sketch in theory.md asks for. Continuity of `Q` is needed on the closed set `G`,
including those shapes. Theorem 12 provides (T_∂) for composite McCormick
relaxations of a factorable `f` whose univariate functions are `C^2` near the
relevant values, with `Q = xi^T grad^2 f(x*) xi / 2 - E_m^cv`. Theorem 12 holds on
every compact set of shapes, including degenerate ones, and needs only
smoothness near `x*`.

*Reduced objects.* Let `Q^F(d_F, xi_F) = Q(iota(d_F), iota(xi_F))`, and let
`Phi^F_c(d_F)` be the shape of the box hull of
`{xi_F in D_F(d_F) : Q^F(d_F, xi_F) <= c}`. By (R1) at `x*`, `Q(d, 0) <= 0`.

### B.2 One-step lemma

**Lemma B1.** Let `K_F` be a compact set of free shapes and let `delta > 0`.
Let `G_F(d_F) = -min_{xi_F} Q^F(d_F, xi_F) >= 0`. There are `wbar > 0` and
`sigmabar > 0` with the following property. Let `B = x* + w D(d)`, where
`d in S`, `d_F in K_F`, `|d_A^+|_inf <= sigmabar` and `w <= wbar`, and let
`U = f* + epsilon` with `epsilon >= 0`.

- (i) *Free part, upper bound.* If `epsilon <= delta w^2/2`, the free part of
  `T_U(B)` lies in `x*_F + w D_F(Phi^F_delta(d_F))`.
- (ii) *Free part, lower bound.* For every `epsilon >= 0`, `T_U(B)` contains
  `x* + w iota(xi_F)` for every `xi_F` with `Q^F(d_F, xi_F) <= -delta`.
- (iii) *Active widths, upper bound.* For every `epsilon >= 0` and `i in A`,
  `width_i(T_U(B)) <= (epsilon + (G_F(d_F) + delta/2) w^2)/g_i`.
- (iv) *Active widths, lower bound.* For every `epsilon >= 0` and `i in A`,
  `width_i(T_U(B)) >= min( w d_i^+, (epsilon + (G_F(d_F) - delta/2) w^2)/g_i )`.

*Proof.* Let `K = {d in S : d_F in K_F, 0 <= d_A^+ <= sigma_0}` for some fixed
`sigma_0 > 0`; `K` is compact. Let `omega` be a modulus of uniform continuity of
`Q` on the compact set `{(d, xi) : d in K, xi in D(d)}` in the sup norm. Choose
`sigmabar <= sigma_0` with `omega(sigmabar) <= delta/4`, and `wbar` with
`rho_K(w) <= delta/4` for `w <= wbar`. For `xi in D(d)`, the pair
`(iota(d_F), iota(xi_F))` is at sup-distance at most `|d_A^+|_inf <= sigmabar`
from `(d, xi)`, because `0 <= xi_A <= d_A^+`. Hence

`|Q(d, xi) - Q^F(d_F, xi_F)| <= delta/4`.

A point `x = x* + w xi` of the set whose hull defines `T_U(B)` satisfies
`phi_B(x) <= f* + epsilon`. By (T_∂),

```
(**)  w g^T xi + w^2 Q(d, xi) <= epsilon + w^2 delta/4,     with g^T xi = sum_{i in A} g_i xi_i >= 0.
```

(i) Drop `g^T xi >= 0`. Then
`Q^F(d_F, xi_F) <= Q(d, xi) + delta/4 <= epsilon/w^2 + delta/2 <= delta`, so
`xi_F` lies in the set whose hull has shape `Phi^F_delta(d_F)`.

(iii) By `(**)`, `g_i xi_i <= g^T xi <= epsilon/w + w(-Q(d, xi) + delta/4)`, and
`-Q(d, xi) <= G_F(d_F) + delta/4`. Multiply by `w` and use `width_i = w max xi_i`
(the lower active bound stays at `l_i`).

(ii) For `xi = iota(xi_F)`, `g^T xi = 0` and `Q(d, xi) <= -delta + delta/4`, so
`phi_B(x) <= f* - w^2 delta/2 < U`.

(iv) Let `xi_F` minimize `Q^F(d_F, .)` and let `xi = (xi_F, t e_i)` with
`0 <= t <= d_i^+`. Then
`phi_B(x) <= f* + w g_i t + w^2 (-G_F(d_F) + delta/4 + delta/4)`, which is at most `U`
when `g_i t <= epsilon/w + w (G_F(d_F) - delta/2)`. QED.

Part (i) with (ii) states precisely that the free widths follow the reduced
tangent map: in scaled units, one OBBT step maps the free shape to a shape
between `Phi^F_{-delta}(d_F)` and `Phi^F_delta(d_F)`. Part (iii) with (iv) shows
that the active-width bound is sharp to first order, since `delta` is arbitrary.

### B.3 Proposition 11 and proof

**Proposition 11.** Assume (T_∂). Let `u_F >> 0`, `delta > 0` and
`lambda in (0,1)` satisfy `Phi^F_delta(u_F) <= lambda u_F`, and let `M >= 0`.
Define

```
G_M = -min{ Q(d, xi) : d in S, d_F = u_F, 0 <= d_A^+ <= M, xi in D(d) },
G_0 = G_F(u_F) = -min{ Q^F(u_F, xi_F) : xi_F in D_F(u_F) },
g_min = min_{i in A} g_i.
```

Then `0 <= G_0 <= G_M`, and there is `wbar > 0` with the following property.
Let `U = f* + epsilon` with `epsilon >= 0`. Let the initial box `B^0` satisfy
`x* in B^0 ⊆ x* + w_0 D(d^0)`, where `d^0_F = u_F`, `0 <= d^{0,+}_A <= M` and
`w_0 <= wbar`. Set `w^_k = lambda^{k-1} w_0` for `k >= 1`, and let `k_eps` be the
first `k >= 1` with `w^_k^2 < 2 epsilon/delta` (`k_eps = infinity` if
`epsilon = 0`).

- (a) *Free widths.* For `1 <= k <= k_eps`, the free part of `B^k` lies in
  `x*_F + w^_k D_F(u_F)`. This is linear contraction with ratio `lambda` in the
  `u_F`-gauge after the first step.
- (b) *Active widths.* `width_i(B^1) <= (epsilon + (G_M + delta/4) w_0^2)/g_i`. For
  `1 <= k <= k_eps`,
  `width_i(B^{k+1}) <= (epsilon + (G_0 + eta_k) w^_k^2)/g_i`, where
  `eta_k <= delta/2` and `eta_k -> 0` as `w^_k -> 0`. Specifically,
  `eta_k = omega(sigma_k) + rho(w^_k)` with `sigma_k = O(w^_{k-1})`.
  So the active widths are `O(epsilon)` plus `O` of the square of the free
  width.
- (c) *Limits.* If `epsilon = 0`, then `B^inf = {x*}`, the free widths are
  `O(lambda^k)`, and `width_i(B^{k+1}) = (G_0/g_i + o(1)) w^_k^2`, or smaller.
  If `epsilon > 0`, the free part of `B^inf` lies in
  `x*_F + sqrt(2 epsilon/delta) D_F(u_F)`, and
  `width_i(B^inf) <= (2 + 2 G_M/delta) epsilon / g_i`.

Since `Phi^F_delta(u_F) <= lambda u_F` holds for suitable `u_F` and `delta` for every
`lambda > r*(Phi^F)`, the free contraction rate is any number above `r*(Phi^F)`.

*Proof.* Let `K' = {d in S : d_F = u_F, 0 <= d_A^+ <= M'}` with
`M' = max(M, 1)`. `K'` is compact. Let `omega` be the modulus of continuity of
`Q` on `{(d, xi) : d in K', xi in D(d)}`, and let `rho = rho_{K'}`. Choose
`sigmabar <= 1` with `omega(sigmabar) <= delta/4`. Choose `wbar` such that
`rho(w) <= delta/4` for `w <= wbar` and

`C_sigma wbar <= sigmabar`, where `C_sigma = (delta/2 + G_M + delta/2)/(lambda g_min)`.

Iterates are nested, contain `x*` (Lemma 1), and lie in `B_0`, so every `B^k`
has the form `x* + w D(d)` with `d in S`. By Lemma 1(b), it suffices to bound
`T_U` applied to the enclosing box `x* + w D(d)`.

*Step 0 -> 1.* We have `T_U(B^0) ⊆ B^0`, so the free part of `B^1` lies in
`x*_F + w_0 D_F(u_F)`. The estimate `(**)` with `K'` and `rho(w_0) <= delta/4`
gives `g_i xi_i <= epsilon/w_0 + w_0 (G_M + delta/4)`, which is the first claim of
(b). If `k_eps > 1`, then `epsilon <= delta w_0^2/2`, so
`sigma_1 = max_i width_i(B^1)/w^_1 <= (delta/2 + G_M + delta/4) w_0/g_min <= sigmabar`.

*Step k -> k+1, for 1 <= k < k_eps.* Suppose
`B^k ⊆ x* + w^_k D(d^k)` with `d^k_F = u_F` and
`d^{k,+}_A = sigma_k <= sigmabar`. Then `d^k in K'`, and
`epsilon <= delta w^_k^2/2` because `k < k_eps`. Lemma B1(i), with `K_F = {u_F}`
and the constants above, shows that the free part of `B^{k+1}` lies in
`x*_F + w^_k D_F(Phi^F_delta(u_F)) ⊆ x*_F + lambda w^_k D_F(u_F) = x*_F + w^_{k+1} D_F(u_F)`.
In the proof of Lemma B1(iii), use the exact continuity and remainder terms in place of
`delta/4`. This gives
`width_i(B^{k+1}) <= (epsilon + (G_0 + omega(sigma_k) + rho(w^_k)) w^_k^2)/g_i`.
Hence
`sigma_{k+1} <= (delta/2 + G_0 + delta/2) w^_k/(lambda g_min) <= C_sigma wbar <= sigmabar`.
This closes the induction and proves (a) and (b) for `k < k_eps`. For
`k = k_eps`, the active estimate of (b) still holds, because Lemma B1(iii) does
not need `epsilon <= delta w^2/2`. Since `sigma_k <= C_sigma w^_{k-1} -> 0`, we
get `eta_k -> 0`.

*(c)* If `epsilon = 0`, then `k_eps = infinity`, and (a) and (b) give the claims,
so `B^inf = {x*}`. If `epsilon > 0`, then `B^inf ⊆ B^{k_eps}`. So the free part
of `B^inf` lies in `x*_F + w^_{k_eps} D_F(u_F)` with
`w^_{k_eps} < sqrt(2 epsilon/delta)`. Also `B^inf ⊆ B^{k_eps+1}`. Apply the
active estimate at scale `w^_{k_eps}` if `k_eps > 1`, and the Step 0 estimate
at scale `w_0 < sqrt(2 epsilon/delta)` if `k_eps = 1`. Either way,
`width_i <= (epsilon + (G_M + delta/2)(2 epsilon/delta))/g_i`. QED.

**Remarks.**

1. The contraction factor is at most `lambda` in the `u_F`-gauge, not only close
   to `lambda`. This is an upper bound: `lambda` is any admissible bound with
   `Phi^F_delta(u_F) <= lambda u_F`, not a proved exact asymptotic rate. The slack `delta` absorbs the (T_∂) remainder, the active
   extents, which enter through the continuity of `Q`, and `epsilon`.
2. Without strict complementarity (`g_i = 0` for some `i in A`), coordinate `i`
   has no first-order term. It then behaves like a free coordinate restricted to
   one-sided extents (`d_i^- = 0`). The argument of Theorem 4 applies on the cone
   `S` with the tangent map in the coordinates `F ∪ {i}`, but Proposition 11 as
   stated does not cover this case.

### B.4 Numerical check

Code: `code/proofs_checks/prop11_obbt.py`. The example is
`f = x1 + x2^2 + x3^2 + a x2 x3 + b x1 x2` with `a = 1` and `b = 0.5` on
`B_0 = [0, 0.5] x [-0.4, 0.6] x [-0.5, 0.45]`. Here `x* = 0`, `f* = 0`,
`A = {1}`, `g_1 = 1` and `F = {2, 3}`. The composite McCormick relaxation is
`x1 + x2^2 + x3^2 + a McC(x2 x3) + b McC(x1 x2)`. Exact OBBT uses 6 convex
programs per round, solved with cvxpy and Clarabel in coordinates normalized
to the current box. Because `iota` sets the active extents to zero, the reduced
tangent map is that of Proposition 7, which predicts the free ratio
`rho(1) = 0.724745`. By Lemma B1(iii)-(iv), `width_1(B^{k+1})` is asymptotically
`epsilon - m_k`. Here `m_k` is the minimum of the free relaxation
`x2^2 + x3^2 + a McC(x2 x3)` over the free box of `B^k`, which equals
`-G_F w^2`.

With `epsilon = 0`, starting from the asymmetric box above:

| k | free width | active width | free ratio | `width_1(B^{k+1})/(eps - m_k)` |
|---|---|---|---|---|
| 0 | 1.000e+00 | 5.000e-01 | 0.715800 | 1.2349 |
| 6 | 1.404e-01 | 9.590e-03 | 0.724080 | 1.0315 |
| 12 | 2.030e-02 | 1.938e-04 | 0.724677 | 1.0043 |
| 18 | 2.941e-03 | 4.050e-06 | 0.724738 | 1.0006 |
| 24 | 4.261e-04 | 8.498e-08 | 0.724744 | 1.0001 |
| 27 | 1.622e-04 | 1.231e-08 | 0.724745 | 1.0000 |

The active width is about 0.246 times the square of the free width. It shrinks
quadratically relative to the free width, as claimed. The free shape converges
to an asymmetric box, about `[-0.46, 0.54]` in relative units, whose ratio is
still `rho(1)`. After about 28 rounds, when the active width is about 1e-8 and
the free width about 1e-4, the degenerate programs exceed Clarabel's accuracy
and the iteration stalls numerically. The script stops at that point.

With `epsilon > 0`, after 60 rounds, the free box is symmetric,
`[-h, h]^2`. The scaled map stalls when `Q_min(1) = 1 - a^2/4 <= epsilon/h^2`,
using the computation in Proposition 7. This predicts a free width of
`2 sqrt(epsilon/(1 - a^2/4)) = 2.3094 sqrt(epsilon)` and an active width of
`epsilon (1 + a/(1 - a^2/4)) = 2.3333 epsilon`. Measured values:

| epsilon | free width / sqrt(eps) | active width / eps |
|---|---|---|
| 1e-3 | 2.3094 | 2.3335 |
| 1e-5 | 2.3094 | 2.3334 |
| 1e-7 | 2.3097 | 2.3340 |

### Commands run (targeted checks only)

```
~/miniconda3/envs/exact-quadratic-hull/bin/python code/proofs_checks/mccormick_expansion.py
~/miniconda3/envs/exact-quadratic-hull/bin/python code/proofs_checks/random_factorable.py
~/miniconda3/envs/minlp-notes/bin/python code/proofs_checks/prop11_obbt.py
```

All three were run from inside `code/proofs_checks/` (the paths above are
relative to `iterated-obbt/`). No project-wide verification was run.
