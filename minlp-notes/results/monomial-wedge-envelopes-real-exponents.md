# Convex hull of a bounded two-variable monomial with real exponents on a wedge

Date: 2026-09-22. Status: proofs written by the root agent; numerical checks
against sampled LP envelopes passed (`code/monomial_wedge/check_envelopes.py`).
A subsequent audit corrected the degree-zero claim and added the omitted
cases with one zero exponent; the six regimes with nonzero individual
exponents were unchanged. The earlier review verdict must be read with these
corrections (see the [review record](../notes/review-monomial-wedge-envelopes.md)). Novelty: extends Belotti (Math. Program. 2025,
"Convex envelopes of bounded monomials on two-variable cones") from positive
exponents to arbitrary real exponents, answering his open item for
`a_1, a_2 < 0` and covering ratio terms `x_1^{a}/x_2^{b}`. A literature check
(2026-09-22, web and local corpus) found no source treating negative or
mixed-sign exponents on a wedge with value bounds; Belotti (Section 6) and
Yang–Zhang (limitations section) both flag negative exponents as untreated,
and no 2025–2026 paper citing Belotti other than Yang–Zhang was found. An
unsuccessful search does not establish novelty.

## Summary

Belotti describes the convex hull of the graph of `f(x) = x_1^{a_1} x_2^{a_2}`
with `a_1, a_2 > 0` over the set `D = {x in W : l <= f(x) <= u}`, where
`W = {x > 0 : p x_1 <= x_2 <= q x_1}` is a wedge, in terms of two functions: a
function constant on parallel chords of the level curves that is exact on the
two boundary rays, and a function affine along rays from the origin that is
exact on the two level curves. This note shows that the same two functions,
together with `f` itself and the affine interpolant of the four corner points,
describe the hull for every real exponent pair with `beta = a_1 + a_2 != 0`.
There are six regimes when both exponents are nonzero (Theorem 1); a zero
individual exponent gives a univariate special case. Degree zero requires
separating the convex hull from its closure (Remark 2). Two of the six
regimes are Belotti's; four extend the classification: both
exponents negative, and the three mixed-sign regimes distinguished by
`kappa = a_+ / |a_-|` and by whether `beta >= 1`. In each regime the lower
envelope is `max(l, g)` and the upper envelope is `min(u, g')`, where `g`
(`g'`) is a convex minorant (concave majorant) of `f` among the four
candidates (numerically the only one in each regime), and `conv(D)` is the
wedge intersected with one convex level set and one half-plane. The mechanism is uniform: quasi-convexity or quasi-concavity of
`f` (decided by the exponent signs and `kappa`) fixes which of the chord
function and the ray function is a minorant, and the sign of `beta` and of
`beta - 1` fixes which is convex.

The result matters for global solvers because two-variable signomial terms
with mixed exponents (`x^2/y`, `sqrt(x)/y`, the Hazen–Williams head-loss term
`Q^{1.852} D^{-4.87}` in flow rate and diameter, `x^a y^{-b}` in kinetics and
pressure drop) are otherwise relaxed by introducing auxiliary variables and
composing envelopes, while ratio bounds `p <= x_2/x_1 <= q` are exactly the
wedge constraints produced by bound propagation on a ratio. The pure ratio
`x/y` has `beta = 0` and is treated separately in Remark 2.

## 1. Setting and the four candidate functions

Fix `a = (a_1, a_2) in R^2` with `beta := a_1 + a_2 != 0`, `0 < p < q`, and
`0 < l < u`. Let

```
W = {x in R^2 : x_1 > 0, p x_1 <= x_2 <= q x_1},   P = {x in W : x_2 = p x_1},   Q = {x in W : x_2 = q x_1},
f(x) = x_1^{a_1} x_2^{a_2},   D = {x in W : l <= f(x) <= u},   C_xi = {x in W : f(x) = xi}.
```

`E_L(f, D)` (lower envelope) is the convex hull of the epigraph of `f` over
`D`, and `E_U(f, D)` (upper envelope) the convex hull of the hypograph, as in
Belotti's Definition 2. We identify them with functions on `conv(D)`.

**Lemma 1 (rays and level curves).** For `r in [p, q]` and `xi > 0` the ray
`{x_2 = r x_1}` meets `C_xi` in exactly one point,

```
e(r, xi) = xi^{1/beta} e(r, 1),    e(r, 1) = (r^{-a_2/beta}, r^{1 - a_2/beta}).
```

Along every ray `t -> t x` (`x in W`, `t > 0`), `f(t x) = t^beta f(x)` is
strictly monotone (increasing iff `beta > 0`) and takes every positive value.
`D` is compact.

*Proof.* On the ray, `f(x_1, r x_1) = r^{a_2} x_1^beta`, so `f = xi` iff
`x_1 = (xi r^{-a_2})^{1/beta}`, which gives `e(r, xi)`; homogeneity of degree
`beta` gives the scaling. `D` is closed in `W` and its `x_1`-coordinates lie
between `min_r (l r^{-a_2})^{1/beta}` and `max_r (u r^{-a_2})^{1/beta}` over
`r in [p, q]` (or with `l, u` swapped when `beta < 0`), so `D` is bounded and
bounded away from the origin. □

**Lemma 2 (parallel chords; the chord function `phi`).** Let
`v = e(q, 1) - e(p, 1)`. Then `v != 0`, and there is a linear form
`s(x) = eps (v_2 x_1 - v_1 x_2)`, `eps in {1, -1}`, such that

1. `s > 0` on `W`, and `sigma := s(e(p, 1)) = s(e(q, 1)) > 0`;
2. for every `xi > 0`, `s(e(p, xi)) = s(e(q, xi)) = sigma xi^{1/beta}`: the
   chord `[e(p, xi), e(q, xi)]` lies on the line `{s = sigma xi^{1/beta}}`, and
   all these chords are parallel;
3. every `x in W` lies on exactly one such chord, namely the one of level
   `phi(x) := (s(x)/sigma)^beta`, and `phi` is constant on each chord, equals `f`
   on `P cup Q`, is convex on `W` when `beta >= 1` or `beta < 0`, and concave
   when `0 < beta <= 1` (affine when `beta = 1`).

*Proof.* If `v = 0` then `q^{-a_2/beta} = p^{-a_2/beta}`, forcing `a_2 = 0`, and
then `q^{1} = p^{1}`, a contradiction. The form `s_0(x) = v_2 x_1 - v_1 x_2`
vanishes on `v` and is nonzero on `e(p, 1)` (otherwise `e(p, 1)` would be
parallel to `v = e(q,1) - e(p,1)`, hence to `e(q, 1)`, impossible for points on
distinct rays); choose `eps` so that `s(e(p, 1)) > 0`. Since `s(v) = 0`,
`s(e(q, 1)) = s(e(p, 1)) = sigma`. Every point of `W` is a nonnegative
combination of `e(p, 1)` and `e(q, 1)`, so `s > 0` on `W`. Item 2 follows from
linearity of `s` and `e(r, xi) = xi^{1/beta} e(r, 1)`. For item 3, the line
`{s = s(x)}` meets the rays `P`, `Q` at `e(p, xi)`, `e(q, xi)` with
`sigma xi^{1/beta} = s(x)`, i.e. `xi = phi(x)`; `x` lies between them because
`W` is the cone spanned by the two rays. `phi = f` on `P cup Q` because
`phi(e(r, xi)) = xi = f(e(r, xi))` for `r in {p, q}`. Convexity: `phi` is the
composition of the positive linear form `s/sigma` with `t -> t^beta`, which is
convex on `t > 0` iff `beta notin (0, 1)` and concave iff `beta in (0, 1]`. □

**Lemma 3 (shape of `f`).** On `R^2_{>0}`:

1. `a_1, a_2 > 0`: every superlevel set `{f >= xi}` is convex; `f` is concave
   iff `beta <= 1`.
2. `a_1, a_2 < 0`: `f` is convex; every sublevel set `{f <= xi}` is convex.
3. `a_1 > 0 > a_2` (the case `a_2 > 0 > a_1` is symmetric), with
   `kappa := a_1/|a_2|`: if `kappa < 1` every superlevel set is convex; if
   `kappa > 1` every sublevel set is convex, and `f` is convex iff `beta >= 1`.
   (`kappa = 1` is `beta = 0`, excluded.)
4. If exactly one exponent is zero, write `f(x) = x_j^b`, `b != 0`.
   Both positive sublevel and superlevel sets are half-spaces in the positive
   orthant. The function is convex for `b < 0` or `b >= 1`, concave for
   `0 < b <= 1`, and affine for `b = 1`.

*Proof.* Level curves: `f(x) = xi` iff `x_1^{a_1} = xi x_2^{-a_2}`. In case 3,
`x_1 = xi^{1/a_1} x_2^{1/kappa}`; since `a_1 > 0`, `{f >= xi} = {x_1 >= xi^{1/a_1} x_2^{1/kappa}}`,
which is convex iff `t -> t^{1/kappa}` is convex iff `kappa <= 1`, and
`{f <= xi} = {x_1 <= xi^{1/a_1} x_2^{1/kappa}}` is convex iff `t^{1/kappa}` is
concave iff `kappa >= 1`. In case 1, `{f >= xi} = {x_1 >= xi^{1/a_1} x_2^{-a_2/a_1}}`
with a convex right-hand side. Case 2: `log f = a_1 log x_1 + a_2 log x_2` is
convex, so `f` is convex and its sublevel sets are convex. Convexity of `f`
itself: the Hessian of `f` has entries `f_11 = a_1(a_1 - 1) f/x_1^2`,
`f_22 = a_2(a_2 - 1) f/x_2^2`, `f_12 = a_1 a_2 f/(x_1 x_2)`, with determinant
`a_1 a_2 (1 - beta) f^2/(x_1^2 x_2^2)`. In case 3 (`a_1 > 0 > a_2`), `f_22 > 0`
and the determinant is `>= 0` iff `beta >= 1`, which also gives `f_11 >= 0`
(as `a_1 >= 1 + |a_2|`); so `f` is convex iff `beta >= 1`. In case 1 the
determinant is `>= 0` iff `beta <= 1`, and then `a_i <= 1` so `f_ii <= 0`:
`f` is concave iff `beta <= 1`. In case 4, monotonicity and the second
derivative `b(b - 1)t^{b - 2}` give the assertions directly. □

For nonzero individual exponents, we say the data are in **Case A** if the superlevel sets of `f` are convex
(regimes 1 and 3 with `kappa < 1`) and in **Case B** if the sublevel sets are
convex (regimes 2 and 3 with `kappa > 1`). With one zero exponent both cases
apply and `phi = f`; the univariate case is given separately below.

**Lemma 4 (chord comparison).** In Case A, `phi <= f` on `W`; in Case B,
`phi >= f` on `W`. In both cases `phi = f` on `P cup Q`.

*Proof.* Let `x in W` and `xi = phi(x)`. By Lemma 2, `x` lies on the chord
`[e(p, xi), e(q, xi)]`, whose endpoints are in `C_xi`. In Case A the chord lies
in the convex set `{f >= xi}`, so `f(x) >= xi`; in Case B it lies in `{f <= xi}`.
Equality on the rays is Lemma 2. (For nonzero individual exponents the inequality is strict off the rays, since
the level curves are strictly convex or concave graphs of power functions with
exponent different from `0` and `1`, but strictness is not needed.) □

**The ray function `H`.** Put

```
c = (u - l) / (u^{1/beta} - l^{1/beta}),   z_0 = l - c l^{1/beta},   h(tau) = z_0 + c tau^{1/beta},   H(x) = h(f(x)).
```

Then `h(l) = l`, `h(u) = u`, `h` is strictly increasing on `(0, infinity)`
(`c > 0` and `tau^{1/beta}` increasing when `beta > 0`; `c < 0` and `tau^{1/beta}`
decreasing when `beta < 0`), `H = f` on `C_l cup C_u`, and
`H(t x) = z_0 + c f(x)^{1/beta} t` is affine in `t` along every ray. Moreover:

- `h >= tau` on `[l, u]` when `beta >= 1` or `beta < 0`, and `h <= tau` on
  `[l, u]` when `0 < beta <= 1`. (For `beta >= 1`, `tau^{1/beta}` is concave and
  `c > 0`, so `h` is concave and lies above its chord, which is the identity;
  for `0 < beta < 1`, `h` is convex; for `beta < 0`, `tau^{1/beta}` is convex and
  `c < 0`, so `h` is concave.)
- `f^{1/beta} = x_1^{a_1/beta} x_2^{a_2/beta}` is positively homogeneous of
  degree one; it is concave when `a_1/beta, a_2/beta >= 0` (same-sign
  exponents; a weighted geometric mean) and convex when the two exponents have
  opposite signs (Lemma 3's determinant formula with `beta' = 1` gives a
  singular positive semidefinite Hessian). Hence `H` is concave when
  (same signs and `beta > 0`) or (mixed signs and `beta < 0`), and convex when
  (same signs and `beta < 0`) or (mixed signs and `beta > 0`).

**The corner interpolant `L`.** Let `s_xi = sigma xi^{1/beta}` and
`T = {e(p, l), e(q, l), e(p, u), e(q, u)}`. Define the affine function

```
L(x) = l + (u - l) (s(x) - s_l) / (s_u - s_l).
```

`L = f` on `T` (the two level-`l` corners have `s = s_l`, the two level-`u`
corners `s = s_u`), so the four lifted corner points are coplanar. `L` is
increasing in `s` when `beta > 0` and decreasing when `beta < 0`. Also
`conv(T) = W cap {min(s_l, s_u) <= s <= max(s_l, s_u)}`.

## 2. The convex hull of `D`

**Lemma 5.** In Case A, `conv(D) = Y_A := {x in W : f(x) >= l, phi(x) <= u}`;
in Case B, `conv(D) = Y_B := {x in W : f(x) <= u, phi(x) >= l}`. The condition
on `phi` is a half-plane: `phi <= u` iff `s <= s_u` (`beta > 0`) or `s >= s_u`
(`beta < 0`), and similarly for `phi >= l`.

*Proof.* Case A. `D subseteq Y_A` because `phi <= f <= u` on `D` (Lemma 4), and
`Y_A` is convex (a convex superlevel set, a half-plane and the wedge). Let
`x in Y_A setminus D`, so `f(x) > u >= phi(x)`. Choose `t'`, `t'' > 0` with
`f(t' x) = u` and `phi(t'' x) = u`; by homogeneity `t'^beta = u/f(x) < 1 <= t''^beta = u/phi(x)`,
so `t'` and `t''` lie on opposite sides of `1` (for either sign of `beta`,
because `t -> t^beta` is monotone with value `1` at `t = 1`) and
`x in [t' x, t'' x]`. Now
`t' x in C_u subseteq D`, and `t'' x` lies on the line `{s = s_u}` inside `W`,
i.e. on the chord `[e(p, u), e(q, u)]`, whose endpoints are in `D`. Hence
`x in conv(D)`. Case B is symmetric: `l <= f <= phi` on `D` gives
`D subseteq Y_B`; for `x in Y_B setminus D` we have `f(x) < l <= phi(x)`,
`t'^beta = l/f(x) > 1 >= t''^beta = l/phi(x)`, `t' x in C_l`, and `t'' x` on the
chord `[e(p, l), e(q, l)]`. □

The same ray argument gives the two facts used repeatedly below.

**Lemma 6 (level-value decompositions).** Let `x in W`.

- (u) If `f(x) <= u <= phi(x)` or `phi(x) <= u <= f(x)`, then `(x, u)` is a
  convex combination of points `(y, u)` with `y in C_u`; in particular
  `(x, u) in conv(epi(f, D)) cap conv(hyp(f, D))`.
- (l) If `f(x) <= l <= phi(x)` or `phi(x) <= l <= f(x)`, the same holds with
  `l` and `C_l`.

*Proof.* Take `t'` with `f(t' x) = u` and `t''` with `phi(t'' x) = u`; the
hypotheses put `t'^beta` and `t''^beta` on opposite sides of `1` (weakly), so
`x in [t' x, t'' x]`; `t' x in C_u` and `t'' x` is a convex combination of
`e(p, u), e(q, u) in C_u`. Lifting all points to height `u` gives the claim. □

## 3. Main theorem

**Theorem 1.** Let `beta != 0`, `0 < l < u`, `0 < p < q`, and let `phi`, `H`,
`L` be as in Section 1. Then `conv(D)` is given by Lemma 5, and on `conv(D)`
the lower and upper envelopes of `f` over `D` are as follows when both
individual exponents are nonzero.

| regime | exponents | `conv(D)` | `E_L` | `E_U` |
|---|---|---|---|---|
| I.1 | `a_1, a_2 > 0`, `beta >= 1` | `Y_A` | `max(l, phi)` | `min(u, H)` |
| I.2 | `a_1, a_2 > 0`, `beta <= 1` | `Y_A` | `max(l, L)` | `min(u, f)` |
| II | `a_1, a_2 < 0` | `Y_B` | `max(l, f)` | `min(u, L)` |
| III.A | mixed signs, `kappa < 1` (so `beta < 0`) | `Y_A` | `max(l, phi)` | `min(u, H)` |
| III.B1 | mixed signs, `kappa > 1`, `beta >= 1` | `Y_B` | `max(l, f)` | `min(u, L)` |
| III.B2 | mixed signs, `kappa > 1`, `0 < beta < 1` | `Y_B` | `max(l, H)` | `min(u, phi)` |

If exactly one exponent is zero, let `f(x) = x_j^b`, `b != 0`, and put
`t_- = min(l^{1/b}, u^{1/b})`, `t_+ = max(l^{1/b}, u^{1/b})`.
Then `D = W cap {t_- <= x_j <= t_+}` is convex, `phi = f`, `H = L`, and

| univariate regime | `E_L` | `E_U` |
|---|---|---|
| `b < 0` or `b >= 1` | `f` | `L` |
| `0 < b <= 1` | `L` | `f` |

At `b = 1`, `f = L`, so the rows agree.

Consequently `conv{(x, f(x)) : x in D} = {(x, z) : x in conv(D), E_L(x) <= z <= E_U(x)}`.
Regimes I.1 and I.2 are Belotti's Theorems 1–2 and Corollary 1 (with
`phi = f'_l`, `H = f'_u`, `L = f''_l`); the other four extend his classification,
subject to the novelty qualification above. In regimes
I.1 and III.A the two envelopes are both curved (a power of a linear form and a
power of `f`), in II and III.B1 the lower envelope is `f` itself and the upper
envelope is affine up to the cap `u`, and in III.B2 the roles of `phi` and `H`
are exchanged relative to I.1: `H` becomes the convex minorant and `phi` the
concave majorant.

In every regime the envelope is `max(l, g)` (resp. `min(u, g')`) where `g`
(`g'`) is a convex minorant (concave majorant) of `f` on `D` among the four
candidates `{f, L, phi, H}`. Table 2 records the shape of each candidate for
the six regimes with nonzero individual exponents; only
the "if" directions of its minorant/majorant column are proved and used, and the
numerical checks found exactly one distinct convex minorant and one distinct
concave majorant among the four in each sampled nondegenerate regime
(at `beta = 1` candidates coincide). The univariate cases also have
coincident candidates.

| candidate | exact on | minorant / majorant of `f` on `D` | convex / concave |
|---|---|---|---|
| `f` | `D` | both | Lemma 3 |
| `L` | `T` (four corners) | minorant if `f` concave; majorant if `f` convex (on `conv(T)`) | affine |
| `phi` | `P cup Q` | minorant in Case A, majorant in Case B (Lemma 4) | convex iff `beta notin (0,1)` |
| `H` | `C_l cup C_u` | minorant if `0 < beta <= 1`, majorant if `beta >= 1` or `beta < 0` | concave iff (same signs, `beta > 0`) or (mixed, `beta < 0`) |

### Proof

Throughout, "`g` is a convex minorant" means `g` is convex on `conv(D)` and
`g <= f` on `D`; then `epi(g)` is a convex set containing `epi(f, D)`, hence
`E_L >= g` on `conv(D)`. Since `f >= l` on `D`, also `E_L >= l`. Dually,
`E_U <= g'` for every concave majorant and `E_U <= u`. So in each regime it
suffices to show (i) the candidate is a convex minorant (concave majorant),
and (ii) tightness: for every `x in conv(D)`, the point `(x, max(l, g(x)))` lies
in `conv(epi(f, D))` (and `(x, min(u, g'(x))) in conv(hyp(f, D))`). Three
decompositions do all the work:

- **Chord decomposition.** If `l <= phi(x) <= u`, then `x` is a convex
  combination of `e(p, phi(x))` and `e(q, phi(x))`, both in `D`, and
  `f = phi(x)` at both; hence `(x, phi(x)) in conv(epi) cap conv(hyp)`.
- **Ray decomposition.** If `x in D`, then `x` lies between `t_l x in C_l` and
  `t_u x in C_u` on its ray, and since `H` is affine along the ray with
  `H(t_l x) = l`, `H(t_u x) = u`, the point `(x, H(x))` is the corresponding
  convex combination of `(t_l x, l)` and `(t_u x, u)`, both graph points over `D`.
- **Corner decomposition.** If `x in conv(T)`, `(x, L(x))` is a convex
  combination of the four lifted corners (all graph points over `D`), because
  `L` is affine.

Also recall Lemma 6 for the values `l` and `u`.

**Regimes I.1 and III.A (Case A; `phi` convex; `H` concave majorant).**
Here `beta >= 1` (I.1) or `beta < 0` (III.A), so `phi` is convex (Lemma 2) and a
minorant (Lemma 4); `H` is concave and `h >= tau` on `[l, u]`, so `H >= f` on
`D`: concave majorant. Tightness of `E_L = max(l, phi)` on `Y_A`: if
`phi(x) >= l` then `phi(x) in [l, u]` (as `phi <= u` on `Y_A`) and the chord
decomposition gives `(x, phi(x)) in conv(epi)`. If `phi(x) < l <= f(x)`, Lemma 6(l)
gives `(x, l) in conv(epi)`. Tightness of `E_U = min(u, H)`: if `x in D`, the ray
decomposition gives `(x, H(x)) in conv(hyp)`, and `H(x) = h(f(x)) <= h(u) = u`.
If `x in Y_A setminus D`, then `f(x) > u >= phi(x)`, Lemma 6(u) gives
`(x, u) in conv(hyp)`, and `H(x) = h(f(x)) > u` since `h` is increasing, so
`min(u, H(x)) = u`. □

**Regime I.2 (Case A; `f` concave).** `f` is concave (Lemma 3), so `min(u, f)`
is a concave majorant of `f` on `D` and `E_U <= min(u, f)`; tightness: on `D`,
`(x, f(x))` is a graph point and `f <= u`; on `Y_A setminus D`, `f > u >= phi`
and Lemma 6(u) gives `(x, u)`. For the lower envelope, `L <= f` on `conv(T)`
by concavity of `f` (`L` is affine and agrees with `f` at the four corners,
and every point of `conv(T)` is a convex combination of them), and on
`D setminus conv(T)`, where `s < s_l` (recall `beta > 0`), `L < l <= f`. So
`max(l, L)` is a convex minorant. Tightness: `Y_A cap {s >= s_l} = W cap {s_l <= s <= s_u} = conv(T)`
(on `Y_A`, `s <= s_u`; and `s >= s_l` means `phi >= l`, which forces `f >= l`),
where the corner decomposition gives `(x, L(x)) in conv(epi)`; on
`Y_A cap {s < s_l}` we have `phi(x) < l <= f(x)`, and Lemma 6(l) gives
`(x, l)`, while `L(x) < l` there. □

**Regimes II and III.B1 (Case B; `f` convex).** `f` is convex (Lemma 3), so
`max(l, f)` is a convex minorant and `E_L >= max(l, f)`; tightness: on `D`
graph points; on `Y_B setminus D`, `f(x) < l <= phi(x)` and Lemma 6(l) gives
`(x, l)`. For the upper envelope let `S_T = conv(T) = W cap {s between s_l and s_u}`.
On `S_T`, `L >= f` by convexity of `f`; on the remaining part of `Y_B`, which is
`{s beyond s_u}` (as `phi >= l` on `Y_B` means `s` is on the `s_l` side), `L > u >= f`.
So `min(u, L)` is a concave majorant. Tightness: if `x in Y_B` with `L(x) <= u`,
then `x in S_T` and the corner decomposition gives `(x, L(x)) in conv(hyp)`; if
`L(x) > u`, then `phi(x) > u >= f(x)` and Lemma 6(u) gives `(x, u)`. □

**Regime III.B2 (Case B; `phi` concave majorant; `H` convex minorant).** Here
`0 < beta < 1` with mixed signs: `phi` is concave (Lemma 2) and a majorant
(Lemma 4); `H` is convex (mixed signs, `beta > 0`) and `h <= tau` on `[l, u]`,
so `H <= f` on `D`. Tightness of `E_L = max(l, H)`: on `D`, the ray
decomposition gives `(x, H(x)) in conv(epi)`, and `H(x) = h(f(x)) >= h(l) = l`.
On `Y_B setminus D`, `f(x) < l <= phi(x)`, Lemma 6(l) gives `(x, l)`, and
`H(x) = h(f(x)) < h(l) = l`, so `max(l, H(x)) = l`. Tightness of
`E_U = min(u, phi)`: if `phi(x) <= u` then (as `phi >= l` on `Y_B`) the chord
decomposition gives `(x, phi(x)) in conv(hyp)`; if `phi(x) > u >= f(x)`, Lemma
6(u) gives `(x, u)`. □

**Univariate cases.** When `f = x_j^b`, the two points on each level curve
have the same `x_j`, so `s/sigma = x_j`, `phi = f`, and `H = L` is the secant
of `t^b` on `[t_-, t_+]`. The domain `D` is the intersection of the wedge
with that coordinate interval and is convex. The usual univariate
convexity/secant inequalities give the claimed bounds. They are tight:
`(x, f(x))` is a graph point, and the ray decomposition expresses
`(x, H(x)) = (x, L(x))` as a convex combination of two graph points. □

Finally, the identification of the graph hull with the region between the two
envelopes over `conv(D)` is the standard vertical-fiber fact for scalar graphs
over compact sets (Belotti cites Tawarmalani–Sahinidis; Yang–Zhang, Lemma 3.8).
This completes the proof of Theorem 1. □

**Remarks.**

1. *Boundary regimes agree.* For `beta = 1` with positive exponents, `phi` is
   affine and equals `L`, and `H = f` (since `c = 1`, `z_0 = 0`), so I.1 and
   I.2 give the same hull. For mixed signs with `beta = 1`, likewise `phi = L`
   and `H = f`, so III.B1 and III.B2 agree.
2. *Degree zero: the convex hull differs from its closure.*
   If `beta = 0`, write `k = a_2`, so `f(x) = (x_2/x_1)^k`.
   If `k = 0`, both exponents vanish: `D` is empty unless `l <= 1 <= u`,
   and otherwise the graph hull is `W x {1}`. Suppose `k != 0` and let
   `J = [p, q] cap {r > 0 : l <= r^k <= u}`. This set is an interval,
   a singleton, or empty. If empty, the graph hull is empty; if `J = {a}`,
   it is the single graph ray `{(t, at, a^k) : t > 0}`.

   If `J = [a, b]` with `a < b`, put
   `m = min(a^k, b^k)`, `M = max(a^k, b^k)`. The **ordinary convex hull** is

   ```
   {(x_1, x_2, z) : x_1 > 0, a < x_2/x_1 < b, m < z < M}
   union {(t, at, a^k) : t > 0}
   union {(t, bt, b^k) : t > 0}.
   ```

   To prove inclusion of every interior point, write `s = x_1`,
   `R = x_2/x_1`, `theta = (R - a)/(b - a)` and
   `lambda = (z - a^k)/(b^k - a^k)`. Both weights lie in `(0, 1)`, and
   the point is the convex combination, with weights `1 - lambda, lambda`,
   of the two graph points

   ```
   (s(1-theta)/(1-lambda), a s(1-theta)/(1-lambda), a^k),
   (s theta/lambda,       b s theta/lambda,       b^k).
   ```

   Conversely, attaining a boundary ratio requires every positively weighted
   graph point to lie on that boundary ray; attaining `m` or `M` requires
   every such point to have the same extremizing ratio, since `r^k` is
   strictly monotone. Thus no additional boundary points occur. Taking limits
   gives the **closed convex hull**

   ```
   {(x_1, x_2, z) : x_1 >= 0, a x_1 <= x_2 <= b x_1, m <= z <= M}.
   ```

   The attained value range `[m, M]` can be strictly smaller than `[l, u]`.
   For example, `f = x_2/x_1`, `1 <= x_2/x_1 <= 2`, and `l = 1, u = 2`
   exclude `(1, 1, 2)` from the ordinary hull, although it belongs to its
   closure. The earlier product-hull claim incorrectly treated boundary
   limits as attained points. Unlike the compact nonzero-degree case,
   interior fiber endpoints here are infima and suprema, not minima and maxima.
3. *Heuristic: why these candidates.* The three auxiliary candidates are the
   functions that agree with `f` on a natural generating set of `D` and are
   affine along a family of lines through it: `H` along rays from the origin
   (exact on the two level curves), `phi` along the parallel chords (exact on
   the two rays), `L` on the four corners. Which of them is convex is decided
   by the quasi-convexity type and the sign pattern of `beta`, `beta - 1`. This
   is an organizing principle for the case analysis, not a theorem: `f` itself
   appears when it is convex or concave, and the list is not claimed to be
   canonical.
4. *Half-plane form of the hull.* In all regimes `conv(D)` is the intersection
   of the wedge, one convex level set of `f` (a superlevel set in Case A, a
   sublevel set in Case B), and one half-plane in the linear form `s`. In
   regimes II and III.B1 the convex level set is `{f <= u}` with `f` convex, so
   `conv(D)` is described by convex inequalities in the original variables;
   in III.B2 `{f <= u}` is convex but `f` is not, and the chord function `phi`
   supplies the concave majorant instead.

## 4. What the result gives, and its limits

- **Exact relaxations for two-variable signomial terms on ratio-bounded
  domains.** For any term `x_1^{a_1} x_2^{a_2}` with `beta != 0`, bounds
  `l <= z <= u` on the term and ratio bounds `p <= x_2/x_1 <= q`, Theorem 1 gives
  the convex hull of the graph in closed form through the two envelope
  inequalities and the convex domain `conv(D)`. Its level-set description
  need not already use convex constraint functions: for example, in III.B2,
  `{x_1^{a_1}/x_2^{|a_2|} <= u}` with `a_1 > 0 > a_2` can be written as the
  convex inequality `x_1 - u^{1/a_1} x_2^{|a_2|/a_1} <= 0`.
  In the mixed-sign case with `kappa > 1` and `beta >= 1` (e.g. `x^2/y`)
  the hull is `{z >= f, z >= l, z <= min(u, L), f <= u, s on the right side}`,
  which is power-cone representable (second-order-cone representable for
  `x^2/y`, and for other rational exponents via towers of cones).
- **What remains for practical value.** Ratio bounds are natural in some
  models (blending, dilution, Hazen–Williams) but solvers work with variable
  boxes; Belotti's own discussion of the box-versus-wedge trade-off applies
  unchanged. The box hull with value bounds remains open (his item (c)), and the
  `n >= 3` mixed-sign wedge case is not treated here. No solver-performance
  experiment was run.
- **Verification scope.** Proofs by hand and independent review, with the
  subsequent corrections described above. `code/monomial_wedge/check_envelopes.py`
  compares the predicted `conv(D)`, `E_L`, `E_U` with LP envelopes over dense
  samples of graph points for 26 exponent pairs covering all six regimes,
  swapped mixed signs, exact `beta = 1` cases, and zero individual exponents.
  Signed violations are checked separately from finite-sample approximation
  error; these floating-point checks do not prove validity or exactness.
  Targeted degree-zero checks illustrate the boundary-ray restriction,
  unattained interior endpoints, closure limits, and constant case.

## 5. Literature

- **Belotti (2025), Math. Program., DOI 10.1007/s10107-025-02212-5, arXiv:2308.12650.**
  Positive exponents: regimes I.1 and I.2 (his Propositions 5–6, Lemma 6,
  Theorems 1–2, Corollary 1), the upper envelope for `n > 2`, and the volume
  of the hull. Section 6 asks about `a_1, a_2 < 0` and guesses a hull "similar to
  the case `beta <= 1`"; regime II confirms this with the roles of `l` and `u`
  exchanged (lower envelope `f` itself, upper envelope the affine corner
  interpolant, hull `{f <= u} cap` half-plane).
- **Yang, Zhang (2026), IJOCTA, "Flat lower envelopes solve bounded monomial
  convexification on two-variable cones".** `n >= 3`, positive exponents: the
  lower envelope over `W_ij` is flat. Their Section 4.3 lists negative exponents
  as open; this note settles them for `n = 2` only.
- **Nguyen, Richard, Tawarmalani (2018), "Deriving convex hulls through lifting
  and projection", Math. Program.** Hulls of `x_1^{b_1} x_2^{b_2} >= x_3` and
  `<= x_3` over boxes with bounds on `x_3` for `b_1 = 1 <= b_2` and related
  cases; box domains, not wedges; positive exponents.
- **Tawarmalani, Sahinidis (2001, 2002).** Convex envelope of `x/y` over a box
  (the fractional case `a = (1, -1)`, `beta = 0`, on a box rather than a wedge)
  and the theory of convex extensions used for the graph-hull identification.
- **Anstreicher, Burer, Park (2021).** Bilinear terms with product bounds on a
  box (`a = (1, 1)`, box domain): SOC pieces on a partition; illustrates why the
  box version of the present question is harder.
- **Locatelli, Schoen (2014), Math. Program. 144; Locatelli (2016), JOGO 66;
  Jach, Michaels, Weismantel (2008), SIAM J. Optim. 19(3).** Envelopes of
  bilinear and fractional bivariate functions over polytopes and of
  `(n-1)`-convex functions over boxes; a wedge intersected with a box is a
  polytope, but the value bounds `l <= f <= u` make `D` non-polyhedral, so these
  results do not apply directly (they would give the envelope of `x/y` on a
  wedge-box without value bounds).
- **Zamora, Grossmann (1999), JOGO 14.** Convex underestimator of `x_1/x_2` on
  a box; not an envelope on a wedge.
- **Khajavirad, Michalek, Sahinidis (2012), Math. Program. 137.** Signomials
  with real nonzero exponents (including negative ones) over boxes via
  convex-transformable intermediates: supporting-hyperplane relaxations, not
  envelopes.
- **He, Liu, Tawarmalani (2025), Math. Program.** Projective correspondence
  between fractional and polynomial hulls; could in principle transfer
  positive-exponent results to some negative-exponent cases, but does not treat
  wedges with value bounds.
- **Khajavirad, Sahinidis (2013).** Products of convex and componentwise
  concave functions; not specialized to wedges with value bounds.
