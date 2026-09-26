# Aggregation certificates for a trivial convex hull of a quadratic system

Date: 2026-09-21. Status: proof written by the root agent; numerical sanity
checks passed (`code/quadratic_aggregation/check_examples.py`: the Section 5
example, and 30 random two-quadratic systems in which every convex certificate
is trivial and every random target point was exhibited as a midpoint of two
points of `S`; no saved output of this SCS-based run was located, and the
archived PASS of `paper-quadratic-aggregation/supplement/check_examples.py`
belongs to a different, exact-arithmetic program); two independent
adversarial reviews passed (the first on Theorem 1 and Corollaries 1–3 with cosmetic corrections, the second on
Corollaries 4–5 with one substantive correction to a parenthetical, all applied
([review record](../notes/review-quadratic-aggregation-certificate.md)).
Novelty: the statement is Conjecture 3.3 of Blekherman, Dey and Sun (SIAM J.
Optim. 34(1), 2024, arXiv:2210.01722), stated there as open. A web check on
2026-09-21 found no later resolution; the follow-up by Blekherman and Dunbar
(arXiv:2405.18282) treats three quadrics and does not discuss this question.
An unsuccessful search does not establish novelty.

**Formal verification, 2026-09-22.** Theorem 1, Lemmas 1–3, and the HHC
specialization are now proved in Lean. The [topic package](../formal/topics/27-quadratic-aggregation/README.md)
maps all 12 obligations to 11 modules; targeted builds, the 178-declaration
axiom audit, and all module kernel replays passed. The formal proof uses the
shorter limiting argument in Section 3.4 below. Corollaries 1–5, Lemma 4,
examples, and literature claims are outside this formal scope.

## Summary

Let `f_i(x) = x^T A_i x + 2 b_i^T x + c_i`, `i in [m]`, be quadratic functions
on `R^n`, `S = {x : f_i(x) < 0 for all i}` the open set they describe, and
`f^h : R^{n+1} -> R^m` the homogenized quadratic map
`f^h(x, t) = (x^T A_i x + 2 t b_i^T x + c_i t^2)_i`. Blekherman, Dey and Sun
(BDS) call `f^h` *hidden hyperplane convex* (HHC) when the image of every
linear hyperplane of `R^{n+1}` under `f^h` is convex. Under HHC they prove
(their Theorem 2.8, for `n >= 3`) that whenever `S` is nonempty and `conv(S)` is not the whole
space, `conv(S)` is the intersection of the "good" aggregated inequalities
`sum_i lambda_i f_i(x) < 0`, `lambda >= 0`. They also show that aggregations
certify `S = empty` (Proposition 2.12) and certify `conv(S) = R^n` in all cases
but one (Proposition 2.13), and conjecture that the remaining case never
occurs:

> **Conjecture 3.3 (BDS).** Suppose `f^h` has HHC and `S` is nonempty. Then
> `conv(S) != R^n` if and only if there is a nonzero `lambda >= 0` with
> `sum_i lambda_i A_i` positive semidefinite and
> (`sum_i lambda_i A_i != 0` or `sum_i lambda_i b_i != 0`).

This note proves the conjecture (Theorem 1). The proof uses only the convexity
of the images of the hyperplanes `{alpha^T x = s t}` for one normal `alpha`
(a supporting normal of `conv(S)`) and arbitrarily large `s`, so the theorem
holds under a weaker "asymptotic" hyperplane-convexity hypothesis. The new
ingredient is a uniform separation constant between the polyhedral cone of
aggregated quadratic parts and the positive semidefinite cone (Lemma 3), which
turns a limiting family of certificates into a contradiction. Corollaries: the
same characterization holds for the closed system `{f_i <= 0}` when the strict
system is feasible; under HHC every one of the three regimes (empty set, whole
space, proper hull) is certified by aggregations; deciding whether
`conv(S) = R^n` reduces to finitely many semidefinite programs; the Shor
semidefinite relaxation is the whole space only when the hull is; and for
three quadratics the hypothesis reduces to a positive definite combination of
the quadratic parts alone. An explicit
example (Section 5) shows that hidden convexity of `f^h` on `R^{n+1}` alone
does not suffice, so the hyperplane hypothesis is used essentially.

## 1. Setting and notation

Throughout, `n >= 1`, `m >= 1`, and all data are real. Write

```
Q_i = [ A_i  b_i ; b_i^T  c_i ]  in Sym_{n+1},
A_lambda = sum_i lambda_i A_i,  b_lambda = sum_i lambda_i b_i,  c_lambda = sum_i lambda_i c_i,
f_lambda = sum_i lambda_i f_i,  Q_lambda = sum_i lambda_i Q_i,
g_i(x) = x^T A_i x   (the quadratic part of f_i).
```

For `xhat = (x, t) in R^{n+1}`, `f_i^h(xhat) = xhat^T Q_i xhat`, so
`f_i^h(x, 1) = f_i(x)` and `f_i^h(x, 0) = g_i(x)`. Let

```
S   = {x in R^n : f_i(x) < 0 for all i},
S^h = {xhat in R^{n+1} : f_i^h(xhat) < 0 for all i}.
```

`S^h` is an open cone, symmetric under `xhat -> -xhat`, and `(x, t) in S^h`
with `t != 0` if and only if `x / t in S`. For `alpha in R^n`, `alpha != 0`,
and `s in R` put

```
H_{alpha, s} = {(x, t) in R^{n+1} : alpha^T x = s t},    E = {(x, t) : t = 0}.
```

**Definition (BDS, Definition 2.1).** A quadratic map `phi : R^d -> R^m` has
*hidden hyperplane convexity* (HHC) if `phi(H)` is convex for every linear
hyperplane `H` of `R^d`. Since `phi(mu xhat) = mu^2 phi(xhat)`, each image
`phi(H)` is a cone containing `0`; when convex it is a convex cone.

**Definition (this note).** `f^h` has *asymptotic hyperplane convexity* if for
every nonzero `alpha in R^n` there are real numbers `s_1 < s_2 < ...` with
`s_k -> +infinity` such that `f^h(H_{alpha, s_k})` is convex for every `k`.
HHC implies asymptotic hyperplane convexity.

Call a nonzero `lambda >= 0` a *convex certificate* if `A_lambda` is positive
semidefinite, and a *nontrivial convex certificate* if in addition
`(A_lambda, b_lambda) != (0, 0)`. Let

```
K = {lambda in R^m_+ \ {0} : A_lambda PSD},     Ttilde = {lambda in R^m : A_lambda = 0 and b_lambda = 0}.
```

A convex certificate `lambda` is trivial exactly when `lambda in Ttilde`; then
`f_lambda` is the constant `c_lambda`, and if `S` is nonempty then `c_lambda < 0`
(evaluate at any point of `S`).

## 2. Main theorem

**Theorem 1.** Let `f^h` have asymptotic hyperplane convexity (in particular,
let `f^h` have HHC) and let `S` be nonempty. Then

```
conv(S) != R^n   if and only if   a nontrivial convex certificate exists.
```

The "if" direction needs no convexity hypothesis; the "only if" direction is
the content of Conjecture 3.3.

The proof occupies Section 3. Section 4 gives corollaries, Section 5 the
example showing the hypothesis is used essentially, Section 6 the comparison
with the literature.

## 3. Proof of Theorem 1

### 3.1 The easy direction

Let `lambda` be a nontrivial convex certificate. For `x in S`,
`f_lambda(x) = sum_i lambda_i f_i(x) < 0` because `lambda >= 0` is nonzero and
every `f_i(x) < 0`. So `S` is contained in `C = {x : f_lambda(x) < 0}`. Since
`A_lambda` is PSD, `f_lambda` is convex and `C` is convex, hence
`conv(S) subseteq C`. Finally `C != R^n`: if `A_lambda != 0`, pick an
eigenvector `v` of `A_lambda` with eigenvalue `mu > 0`; then
`f_lambda(r v) = mu r^2 + O(r) -> +infinity`. If `A_lambda = 0` but
`b_lambda != 0`, then `f_lambda(r b_lambda) = 2 r |b_lambda|^2 + c_lambda -> +infinity`.
Either way some point has `f_lambda >= 0`, so `conv(S) != R^n`. (This is the
observation preceding Proposition 2.13 in BDS.)

### 3.2 Three lemmas

**Lemma 1 (no recession direction).** If `conv(S) != R^n`, then there is no
`v in R^n` with `g_i(v) < 0` for all `i`; equivalently `E cap S^h` is empty.

*Proof.* Suppose `g_i(v) < 0` for all `i`. Fix any `y in R^n`. For real `M`,
`f_i(y + M v) = M^2 g_i(v) + 2 M (v^T A_i y + b_i^T v) + f_i(y)`, which tends to
`-infinity` as `|M| -> infinity`. Hence `y + M v` and `y - M v` lie in `S` for
all large `M`, and their midpoint `y` lies in `conv(S)`. Thus `conv(S) = R^n`,
a contradiction. Points of `E cap S^h` are exactly the pairs `(v, 0)` with all
`g_i(v) < 0`. □

**Lemma 2 (a sweeping family of hyperplanes missing `S^h`).** Suppose
`conv(S) != R^n` and let `alpha != 0`, `beta` satisfy `alpha^T x < beta` for
all `x in S`. Then `H_{alpha, s} cap S^h` is empty for every `s >= beta`.

*Proof.* Let `(x, t) in H_{alpha, s} cap S^h`. If `t = 0`, Lemma 1 is
contradicted. If `t != 0`, replacing `(x, t)` by `(-x, -t)` if necessary (both
`H_{alpha, s}` and `S^h` are symmetric under negation) we may assume `t > 0`;
then `x / t in S` and `alpha^T (x / t) = s >= beta`, contradicting validity. □

Such `alpha, beta` exist whenever `conv(S) != R^n`: `conv(S)` is an open convex
set (the convex hull of an open set is open), so any `y` outside it can be
separated: there is `alpha != 0` with `alpha^T x <= alpha^T y =: beta` on
`conv(S)`, and openness makes the inequality strict on `S`.

**Lemma 3 (uniform separation of a polyhedral cone from a closed cone).**
Let `P` and `D` be closed cones in a finite-dimensional normed space
with `P cap D = {0}`, and let `P` be finitely generated. Then there is `kappa > 0`
with `dist(p, D) >= kappa |p|` for all `p in P`. (Convexity of `D` is not
needed; in the application `D` is convex.)

*Proof.* If `P = {0}` any `kappa` works. Otherwise the set `P cap {|p| = 1}` is
compact (`P` is closed because finitely generated cones are closed), the
function `p -> dist(p, D)` is continuous, and it is positive on this set because
`D` is closed and contains no unit vector of `P`. Let `kappa > 0` be its
minimum. For general `p in P \ {0}`, `dist(p, D) = |p| dist(p / |p|, D) >= kappa |p|`
by homogeneity of `D`. □

We apply Lemma 3 to the linear map

```
pi : R^m -> Sym_n x R^n,    pi(lambda) = (A_lambda, b_lambda),
```

with `P = pi(R^m_+) = cone{pi(e_1), ..., pi(e_m)}` and
`D = {(A, b) : A PSD}`, using the norm `|(A, b)| = (|A|_F^2 + |b|^2)^{1/2}`.
For this norm, `dist((A, b), D) = |A_-|_F`, where `A_-` is the negative part of
`A` (project `A` onto the PSD cone and keep `b`), and `|A_-|_F <= sqrt(n) |mu_min(A)|`
where `mu_min` is the smallest eigenvalue.

### 3.3 The hard direction

Assume asymptotic hyperplane convexity, `S != empty`, and `conv(S) != R^n`, and
suppose for contradiction that **no nontrivial convex certificate exists**, that
is, `K subseteq Ttilde`. Then `P cap D = {0}`: if `lambda >= 0` and
`A_lambda` is PSD, either `lambda = 0` or `lambda in K subseteq Ttilde`, and in
both cases `pi(lambda) = 0`. Let `kappa > 0` be the constant of Lemma 3 and put
`kappa' = kappa / sqrt(n)`.

Fix `alpha != 0`, `beta` with `alpha^T x < beta` on `S` and a sequence
`s_k -> +infinity` such that `f^h(H_{alpha, s_k})` is convex; discard the
finitely many `k` with `s_k < max(beta, 1)`, so that every remaining `s_k` is
positive (Step 1 divides by `s_k`) and at least `beta` (Lemma 2 applies).

**Step 1: a certificate on each hyperplane.** Fix `k` and write `s = s_k`,
`H = H_{alpha, s}`. By Lemma 2, `f^h(H)` does not meet the open negative
orthant `-R^m_{++}`. Both `f^h(H)` (by hypothesis) and `-R^m_{++}` are
convex, and the second is open, so there is `lambda != 0` with
`sup_{z in -R^m_{++}} lambda^T z <= inf_{y in f^h(H)} lambda^T y`. The
supremum is `0` if `lambda >= 0` and `+infinity` otherwise, and the infimum is
at most `lambda^T f^h(0) = 0`. Hence `lambda >= 0`, `lambda != 0`, and
`lambda^T f^h(xhat) = xhat^T Q_lambda xhat >= 0` for all `xhat in H`. Normalize
`sum_i lambda_i = 1` and call this vector `lambda(k)`. Every point of `H` is
`(x, alpha^T x / s)` for a unique `x in R^n`, so the certificate reads

```
phi_k(x) := x^T A_{lambda(k)} x + (2/s_k) (alpha^T x)(b_{lambda(k)}^T x) + (c_{lambda(k)} / s_k^2)(alpha^T x)^2 >= 0   for all x in R^n.   (1)
```

**Step 2: the limit certificate is trivial.** The vectors `lambda(k)` lie in the
standard simplex. Pass to a subsequence along which `lambda(k) -> lambda*`. For
each fixed `x`, the last two terms of (1) tend to `0`, so
`x^T A_{lambda*} x >= 0`. Thus `A_{lambda*}` is PSD and `lambda* >= 0` is
nonzero, so `lambda* in K subseteq Ttilde`: `A_{lambda*} = 0`, `b_{lambda*} = 0`
and, since `S` is nonempty, `c* := c_{lambda*} < 0`. Consequently
`c_{lambda(k)} -> c* < 0`, and there is `k_0` with `c_{lambda(k)} < 0` for all
`k >= k_0` in the subsequence.

**Step 3: the certificates cannot be nearly convex.** Fix `k >= k_0` in the
subsequence, write `lambda = lambda(k)`, `s = s_k`, and let
`rho = |pi(lambda)| = (|A_lambda|_F^2 + |b_lambda|^2)^{1/2}`.

If `rho = 0`, then `A_lambda = 0`, `b_lambda = 0`, so `lambda in K` is a trivial
certificate and (1) at `x = alpha` reads `c_lambda |alpha|^4 / s^2 >= 0`,
contradicting `c_lambda < 0`. Hence `rho > 0`.

Since `pi(lambda) in P`, Lemma 3 gives `|(A_lambda)_-|_F >= kappa rho`, hence
`mu := mu_min(A_lambda) <= -kappa' rho`. Let `u` be a unit eigenvector of
`A_lambda` for `mu`. Evaluate (1) at `x = u`: using `u^T A_lambda u = mu`,
`|(alpha^T u)(b_lambda^T u)| <= |alpha| |b_lambda| <= |alpha| rho`, and
`c_lambda (alpha^T u)^2 / s^2 <= 0`,

```
0 <= phi_k(u) <= -kappa' rho + (2 |alpha| / s) rho = rho (2 |alpha| / s - kappa').
```

Because `rho > 0`, this forces `s_k <= 2 |alpha| / kappa'`. But `s_k -> +infinity`
along the subsequence, so for large `k` the inequality fails. This contradiction
shows that a nontrivial convex certificate exists. □

**Remarks on the proof.**

1. The only convexity used is that of `f^h(H_{alpha, s_k})` for the one normal
   `alpha` of a supporting halfspace and a sequence `s_k -> infinity`. In the
   Grassmannian of hyperplanes of `R^{n+1}`, these hyperplanes converge to
   `E = {t = 0}`, the hyperplane at infinity of the affine chart `t = 1`. So the
   theorem says: convexity of the hyperplane images *near the hyperplane at
   infinity* certifies a trivial hull. Convexity of `f^h(E)` alone (hidden
   convexity of the quadratic parts `A_1, ..., A_m`) is Proposition 2.13 of BDS
   and does not suffice for the converse; see Section 5.
2. The constant `kappa` depends only on `A_1, ..., A_m, b_1, ..., b_m`; the
   argument gives no bound on the size of the certificate `lambda`, and none is
   needed.
3. Nothing in the proof requires `n >= 3` or `m >= 2`. For `m = 1` the theorem
   reduces to the elementary fact that a single open quadratic inequality with
   nonempty solution set has a proper convex hull exactly when its quadratic part
   is PSD and the function is not constant (cf. BDS Lemma 5.3, which treats the
   case of exactly one negative eigenvalue; the indefinite case follows from
   Lemma 1). For `m = 2`, HHC is
   automatic by Dines' theorem and the certificate statement is due to Yildiran
   (2009); the present proof gives it a different, dimension-free argument.

### 3.4 The verified compactness proof

The Lean proof obtains the same theorem with one compactness argument and
no eigenvalue estimates. Fix `x_0 in S` and use Step 1 to choose positive
levels `s_k -> infinity` and nonzero nonnegative weights `lambda(k)`.
Write their aggregates as `(A_k,b_k,c_k)`. Strict feasibility gives

```
c_k < -x_0^T A_k x_0 - 2 b_k^T x_0.
```

In (1), the coefficient of `c_k` is a nonnegative square. Replacing `c_k`
by this upper bound therefore preserves nonnegativity. The pair `(A_k,b_k)`
is nonzero: otherwise `c_k<0` and (1) at `x=alpha` is impossible.
Normalize it by `rho_k = norm(A_k,b_k)`. These normalized pairs belong to
the compact unit section of the closed finitely generated cone `P` from
Section 3.2. A subsequence converges to `(A_*,b_*) in P` of norm one.

After division by `rho_k`, the replacement for the constant is a fixed
continuous linear function of the normalized pair. Thus its contribution
vanishes with `s_k^(-2)`, and the cross term vanishes with `s_k^(-1)`.
For every fixed `x`, the limit of the inequality is `x^T A_* x >= 0`.
The matrix is symmetric, so it is PSD. Membership in `P` supplies actual
nonnegative weights realizing the nonzero pair, hence a nontrivial convex
certificate directly. This avoids both the simplex-limit contradiction and
the quantitative spectral bound; it assumes no bound on `c_k/rho_k`.

The formal development separately proves Lemma 3 in any finite-dimensional
real normed space. Its coefficient-space normalization uses the entrywise
maximum matrix norm and product maximum norm, which suffice for this
compactness argument. It also proves equivalence between the source's
increasing-sequence definition of asymptotic convexity and the existence of
arbitrarily large good levels. See the [coverage map](../formal/topics/27-quadratic-aggregation/COVERAGE.md)
and [verification record](../formal/topics/27-quadratic-aggregation/VERIFICATION.md).

## 4. Corollaries

The [consequences package](../formal/topics/28-quadratic-aggregation-consequences/README.md)
extends the original core scope to Corollaries 1, 3 and 4, Lemma 4, the
strict-feasibility counterexample below, and the relaxation-strength example
in Section 7. The examples include actual HHC proofs using a formally proved
two-form convexity theorem. Corollaries 2 and 5 remain outside this package.

**Corollary 1 (closed inequalities).** Let `T = {x : f_i(x) <= 0 for all i}`
and suppose the strict system is feasible (`S != empty`) and `f^h` has asymptotic
hyperplane convexity. Then `conv(T) != R^n` if and only if a nontrivial convex
certificate exists; moreover `conv(T) != R^n` if and only if `conv(S) != R^n`.

*Proof.* `S subseteq T` gives `conv(S) subseteq conv(T)`. If `conv(T) != R^n`
then `conv(S) != R^n` and Theorem 1 yields a nontrivial certificate. Conversely,
a nontrivial certificate `lambda` gives `T subseteq {f_lambda <= 0}`, a proper
closed convex set (same argument as in 3.1), so `conv(T) != R^n`. □

The feasibility of the strict system cannot be dropped. **Example (closed
system with empty strict system).** In `R^3` let

```
f_1 = x_1 x_2 - 1,   f_2 = -(x_1 x_2 - 1),   f_3 = x_1^2 - x_2^2,
T = {f_i <= 0} = {x_1 x_2 = 1, |x_1| <= |x_2|}.
```

Then `S = empty`, `T != empty`, and `x_1^4 = x_1^2 / x_2^2 <= 1` on `T`, so
`conv(T) subseteq {|x_1| <= 1}` is proper; `conv(T)` has nonempty interior
(it contains the barycenter `0` of the four points `(1, 1, 0)`, `(1/2, 2, 0)`,
`(-1, -1, 0)`, `(-1/2, -2, 0)` of `T`, which affinely span the `(x_1, x_2)`
plane, times the free `x_3`). Every `A_lambda = (lambda_1 - lambda_2) J + lambda_3 diag(1, -1, 0)`
(`J` the `x_1 x_2` form) is traceless, hence PSD only when zero, and all
`b_i = 0`: every convex certificate is trivial. HHC holds because the `Q_i`
span a two-dimensional space (`Q_2 = -Q_1`), so every hyperplane image is a
linear image of the image of a two-form map (Dines). So the equivalence of
Theorem 1 fails for `T` when `S = empty`, and Corollary 1's hypothesis is
sharp. The same example shows that the hypothesis "`Q_lambda != 0` for all
nonzero `lambda >= 0`" in BDS Theorem 2.23 (aggregation description of
`G = int conv(T)`) cannot be dropped, answering the implicit question of their
Remark 2.24: here `Q_{(1,1,0)} = 0`, `emptyset != G != R^3`, and no good
aggregation exists at all. Indeed `0 in G` forces `c_lambda = lambda_2 - lambda_1 < 0`,
and then `Q_lambda = blockdiag([[lambda_3, mu/2], [mu/2, -lambda_3]], 0, -mu)`
with `mu = lambda_1 - lambda_2 > 0` has two negative eigenvalues; so
`Omega_T = empty` and the intersection over `Omega_T` is `R^3 != G`
(numerical check: `code/quadratic_aggregation/check_closed_example.py`).

**Corollary 2 (complete certification under HHC).** Suppose `f^h` has HHC and
`n >= 3`. Exactly one of the following holds, and each is certified by
aggregations (for `n = 2`, items 1 and 2 still hold, and item 3 is certified
only by the existence of a nontrivial certificate, not by the hull description):

1. `S = empty`, if and only if some nonzero `lambda >= 0` has `Q_lambda` PSD
   (BDS Proposition 2.12; hidden convexity of `f^h` on `R^{n+1}` follows from
   HHC when `n + 1 >= 3`, BDS Observation 2.2).
2. `S != empty` and `conv(S) = R^n`, if and only if `S != empty` and no
   nontrivial convex certificate exists (Theorem 1).
3. `S != empty` and `conv(S) != R^n`, in which case `conv(S)` is the
   intersection of the good aggregations (BDS Theorem 2.8, for `n >= 3`).

**Corollary 3 (deciding a trivial hull by semidefinite programming).** Assume
HHC and `S != empty`. Then `conv(S) = R^n` if and only if the spectrahedral cone
`K cup {0} = {lambda >= 0 : A_lambda PSD}` is contained in the subspace
`Ttilde`. Since `pi(K cup {0})` is a convex cone, it equals `{0}` if and only if
for every coordinate functional `ell` of `Sym_n x R^n` (there are
`n(n+1)/2 + n` of them) both semidefinite programs
`max { +-ell(pi(lambda)) : lambda >= 0, sum_i lambda_i = 1, A_lambda PSD }` have
value `0` or are infeasible. Hence the question is decided by
`n(n+1) + 2n` semidefinite programs, each with an `n x n` semidefinite block and
`m` nonnegative scalar variables. (The number of programs can be reduced, since
`ell(pi(lambda))` is linear in `lambda`, but this is not needed here.) This is
an exact characterization in terms of SDP feasibility and optimum values,
not an implemented numerical certification procedure. A near-zero
floating-point optimum does not distinguish an exact zero from a small
positive value. Certifying a whole-space hull requires certified bounds or
exact arguments establishing all required zero values or infeasibility;
solver tolerances alone do not establish the conclusion.

**Corollary 4 (the Shor relaxation is trivial exactly when the hull is).** Let
`P_SDP = {x : exists X with [1 x^T; x X] PSD and <A_i, X> + 2 b_i^T x + c_i <= 0 for all i}`
be the projection of the Shor semidefinite relaxation of the closed system.
Under asymptotic hyperplane convexity and `S != empty`,

```
P_SDP = R^n   if and only if   conv(S) = R^n   if and only if   conv(T) = R^n.
```

*Proof.* `S subseteq T subseteq P_SDP`, so `conv(S) = R^n` forces
`P_SDP = R^n`. Conversely, if `conv(S) != R^n`, Theorem 1 gives a nontrivial
convex certificate `lambda`. For `x in P_SDP` with witness `X`,
`f_lambda(x) = sum_i lambda_i (<A_i, X> + 2 b_i^T x + c_i) - <A_lambda, X - x x^T> <= 0`,
because the first sum is `<= 0` and `A_lambda` and `X - x x^T` are PSD. Thus
`P_SDP subseteq {f_lambda <= 0}`, a proper subset of `R^n` because `f_lambda`
is unbounded above (argument of 3.1). The
statement for `conv(T)` is Corollary 1. □

In words: under the hypotheses, the semidefinite relaxation of a quadratic
system retains at least one valid linear inequality whenever the system itself
implies one; it never collapses to the whole space while the true hull is
proper. The following hypothesis-free lemma (suggested by the second reviewer)
shows that Corollary 4 is exactly Theorem 1 in semidefinite language.

**Lemma 4.** If `S` is nonempty, then `P_SDP = R^n` if and only if every
convex certificate is trivial.

*Proof.* Let `C = {(<A_i, Y>)_i : Y PSD} + R^m_+`, a convex cone with
`R^m_{++} subseteq int C`, and note `x in P_SDP` iff `-f(x) := (-f_i(x))_i in C`
(take `X = x x^T + Y`). Its dual cone is `C* = {lambda >= 0 : A_lambda PSD} = K cup {0}`,
so `cl C = {y : lambda^T y >= 0 for all lambda in K}`. If a nontrivial certificate
exists, `P_SDP != R^n` by the proof of Corollary 4. Conversely let every
certificate be trivial; then `lambda^T(-f(x)) = -c_lambda > 0` for all
`lambda in K` and all `x`, so `-f(x) in cl C` for every `x`. Fix `x`, pick
`x_0 in S` (so `-f(x_0) in R^m_{++} subseteq int C`) and put `x' = 2x - x_0`.
The quadratic identity `f((a + b)/2) = f(a)/2 + f(b)/2 - g(a - b)/4`, with
`g = (g_i)_i` the vector of quadratic parts, gives

```
-f(x) = (1/2)(-f(x')) + (1/2)(-f(x_0)) + (1/4) g(x' - x_0)  in  cl C + int C + C  subseteq  int C,
```

using `g(v) = (<A_i, v v^T>)_i in C`. Hence `-f(x) in C` and `x in P_SDP`. □

**Verified alternative proof of Lemma 4.** The Lean proof avoids the
possibly nonclosed image cone altogether and obtains a stronger conclusion.
Fix `x` and suppose no PSD `Y` satisfies all
`f_i(x) + <A_i,Y> < 0`. Separate the convex affine image
`{(f_i(x)+<A_i,Y>)_i : Y PSD}` from the open negative orthant. This gives
nonzero `lambda>=0` with `f_lambda(x)+<A_lambda,Y> >= 0` for every PSD `Y`.
Scaling rank-one matrices `Y=t vv^T` proves `A_lambda` is PSD; `Y=0` gives
`f_lambda(x)>=0`. If every convex certificate is trivial, the aggregate
equals `c_lambda` everywhere, and a strict feasible point gives
`c_lambda<0`, a contradiction. Thus every `x` has an actual PSD covariance
slack satisfying all lifted inequalities strictly. The standard Shor block
representation follows from the proved Schur-complement equivalence.
No closedness of a projection or PSD-image cone is assumed.

Thus `P_SDP = R^n` iff every convex certificate is trivial, unconditionally
(given `S != empty`), while `conv(S) = R^n` iff every convex certificate is
trivial holds under asymptotic hyperplane convexity (Theorem 1). Without
hyperplane convexity the two can differ: in the example of Section 5 every
convex aggregation is trivial, so `P_SDP = R^3` by Lemma 4, while `conv(S)` is
bounded in two coordinates.

For the record: `P_SDP subseteq {x : f_lambda(x) <= 0 for all lambda in K}`
always (the proof above), with equality of closures when `S != empty` (Fujie and
Kojima 1997, Theorem 2.1, under a Slater-type condition; Kojima and Tuncel
2000, Theorem 4.2, without it). Exact equality can fail: for `f_1 = 2 x_1 x_2 + 1`,
`f_2 = x_1^2` on `R^2` the intersection of convex aggregations is the line
`{x_1 = 0}` while `P_SDP` is empty (the reviewer's example; here `S` is empty).

**Corollary 5 (checkable hypotheses: two or three quadratics).** Let `S` be
nonempty. The equivalence of Theorem 1 holds in each of the following cases:

1. `m = 2` and `n >= 1` (no further hypothesis);
2. `m = 3`, `n >= 3`, and the quadratic parts satisfy PDLC: some real
   combination `theta_1 A_1 + theta_2 A_2 + theta_3 A_3` is positive definite.

More generally it holds whenever the quadratic parts `(A_1, ..., A_m)` are
*stably convex* in the sense of Sheriff (2013): every quadratic map
`x -> (x^T M_i x)_i` with `(M_i)` sufficiently close to `(A_i)` has a convex
image. (Sheriff's "Calabi stable convexity theorem" is exactly case 2, and his
roundness theorem characterizes stable convexity for `m >= 4`, `n >= m`,
`n != m + 1`.)

*Proof.* Every point of `H_{alpha, s}` is `(x, alpha^T x / s)`, so
`f^h(H_{alpha, s})` is the image of `R^n` under the quadratic map with matrices

```
M_i(s) = A_i + (1/s)(alpha b_i^T + b_i alpha^T) + (c_i / s^2) alpha alpha^T  ->  A_i   (s -> infinity).
```

Under robust hidden convexity these images are convex for all large `s`, which
is asymptotic hyperplane convexity, and Theorem 1 applies. Case 1: the image of
`R^n` under any two quadratic forms is convex (Dines 1941). Case 2: positive
definiteness is an open condition, so `sum_i theta_i M_i(s)` is positive
definite for all large `s`, and the image of `R^n` (`n >= 3`) under three
quadratic forms admitting a positive definite combination is convex (Polyak
1998, Theorem 2.1; Calabi 1982). □

*Scope of case 2.* Formally, PDLC of the blocks `A_i` is weaker than PDLC of
the homogenized matrices `Q_i` used in BDS Corollary 2.6(2). In the only
situation where Theorem 1 has content, however, the two coincide: if a trivial
convex certificate `lambda^0` exists, then `Q_{lambda^0} = c_{lambda^0} E_0`
with `E_0 = e_{n+1} e_{n+1}^T` and `c_{lambda^0} < 0`, so `E_0` lies in the span
of the `Q_i`, and adding a large multiple of `E_0` to a combination whose
`A`-block is positive definite makes the whole matrix positive definite. If no
trivial certificate exists, either a nontrivial one exists (and the easy
direction applies) or `K` is empty and BDS Proposition 2.13 applies (its
hypothesis, convexity of the image of the quadratic parts, follows from PDLC of
the `A_i` by Polyak's theorem). So case 2 is a convenient restatement of what
BDS's results plus Theorem 1 give for `m = 3`, not a genuine weakening. This was
noticed when the random instances built for the check script (all with a
trivial certificate) turned out to satisfy PDLC of the `Q_i` as well. Stable
convexity of the quadratic parts and HHC of the homogenized map should not be
identified. For an explicit example with HHC but without stable convexity,
take three identical forms with `A_i = diag(1, -1, 0)`, `b_i = 0`, and `c_i = -1`.
Every hyperplane image of `f^h` is a line, a ray, or `{0}` along `(1, 1, 1)`,
and hence is convex. For any `epsilon > 0`, perturb the quadratic parts to
the three forms
`u = x_1^2 - x_2^2`, `u + epsilon (x_1^2 + x_2^2)`, and
`u + 2 epsilon x_1 x_2`. Their images of `e_1` and `e_2` have midpoint
`(0, epsilon, 0)`. A preimage of this midpoint would require
`x_1^2 = x_2^2 = 1/2` and `x_1 x_2 = 0`, which is impossible. Thus these
arbitrarily small perturbations have nonconvex images. Conversely, the
stable-convexity argument above establishes convexity only for the hyperplanes
near `E`; it does not establish HHC on every hyperplane.
Sheriff's roundness theorem supplies stably convex tuples with `m >= 4`,
but no natural constraint class of that kind is exhibited here.

## 5. The hyperplane hypothesis is used essentially

The following system in `R^3` (so `n = 3`, `m = 4`) has a nonempty `S`, a
proper convex hull, and no nontrivial convex certificate, while `f^h` is hidden
convex on `R^4` (its full image is convex) and its quadratic parts are hidden
convex on `R^3`:

```
f_1 = x_1^2 - x_2^2 - 1,   f_2 = x_2^2 - x_1^2 - 1,   f_3 = x_1 x_2 - 1,   f_4 = -x_1 x_2 - 1.
```

*Nonempty and proper hull.* `0 in S`. Writing `z = x_1 + i x_2`, the constraints
say `|Re z^2| < 1` and `|Im z^2| < 2`, so `|z|^4 = |z^2|^2 < 5` on `S` and
`S subseteq {x_1^2 + x_2^2 < sqrt 5} x R`. Hence `conv(S) != R^3`.

*No nontrivial certificate.* `A_lambda = [[lambda_1 - lambda_2, (lambda_3 - lambda_4)/2, 0], [(lambda_3 - lambda_4)/2, lambda_2 - lambda_1, 0], [0, 0, 0]]`
has trace `0`, so it is PSD only if it is `0`, i.e. `lambda_1 = lambda_2` and
`lambda_3 = lambda_4`; all `b_i = 0`. So every convex certificate is trivial
(and `K` is nonempty: `lambda = (1, 1, 0, 0)` gives `f_lambda = -2`).

*Hidden convexity of `f^h` and of the quadratic parts.* With
`u = x_1^2 - x_2^2`, `v = x_1 x_2`, `w = t^2`,
`f^h(x, t) = (u - w, -u - w, v - w, -v - w)`. As `z` ranges over `C`, `z^2`
ranges over `C`, so `(u, v)` ranges over all of `R^2`, and `w` over `[0, infinity)`
independently. The image of `R^4` is the linear image of the convex set
`R^2 x R_+`, hence convex; the image of `E` (`w = 0`) is a linear image of `R^2`,
hence convex.

*Failure of hyperplane convexity near infinity.* Take `alpha = (1, 0, 0)` (a
supporting normal, since `x_1 < 5^{1/4}` on `S`) and `H_{alpha, s} = {x_1 = s t}`.
On this hyperplane `t = x_1 / s`, so
`f^h = (u - x_1^2/s^2, -u - x_1^2/s^2, v - x_1^2/s^2, -v - x_1^2/s^2)` with
`(u, v, x_1^2) = (x_1^2 - x_2^2, x_1 x_2, x_1^2)`. The map
`(x_1, x_2) -> (x_1^2 - x_2^2, x_1 x_2, x_1^2)` is a linear isomorphism of the
space of binary quadratic forms applied to `(x_1^2, x_1 x_2, x_2^2)`, so its
image is the non-convex rank-one cone `{(a, b, c) : a c = b^2, a, c >= 0}` in
those coordinates, and the map `(u, v, w) -> (u - w, -u - w, v - w, -v - w)` is
injective. Hence `f^h(H_{alpha, s})` is not convex for any `s != 0`: the two
points `f^h(1, 0, 0, 1/s)` and `f^h(0, 1, 0, 0)` lie in the image but their
midpoint does not (verified numerically in `code/quadratic_aggregation/check_examples.py`).
This is exactly where the proof of Theorem 1 would break: Step 1 has no
separating `lambda` for these hyperplanes.

The example also shows that in Theorem 1 the hypothesis cannot be weakened to
hidden convexity of `f^h` on `R^{n+1}` (the classical notion), in the same way
that BDS Example 2.10 shows hidden convexity does not suffice for Theorem 2.8.
Three constraints already suffice for the phenomenon (pointed out in the
review): drop `f_4`. With `u = x_1 + x_2`, `v = x_1 - x_2` the remaining
constraints read `|u v| < 1` and `u^2 - v^2 < 4`; if `|u| >= 3` then
`|v| < 1/3` and `u^2 < 4 + 1/9`, a contradiction, so `|u| < 3` on `S` and
`conv(S) != R^3` although `S` is unbounded. The aggregated quadratic parts are
still traceless, so every convex certificate is trivial, and the full image of
`f^h` is the linear image `{(u - w, -u - w, v - w) : (u, v) in R^2, w >= 0}` of
a convex set.

## 6. Comparison with the literature

- **Yildiran (2009), "Convex hull of two quadratic constraints is an LMI set",
  IMA J. Math. Control Inform. 26(4):417–450.** For `m = 2`, the convex hull is
  given by at most two aggregations, and aggregations certify `S = empty` and
  `conv(S) = R^n`. Theorem 1 recovers the `m = 2` certificate statement as a
  special case (HHC holds for two forms by Dines' theorem) with a proof that does
  not use the pencil structure (generalized eigenvalues and the interval
  structure of `{alpha : nu(alpha Q_1 + (1 - alpha) Q_2) <= 1}`).
- **Dey, Muñoz, Serrano (2022), SIAM J. Optim. 32(2), arXiv:2106.12629.** Hull
  by aggregations for `m = 3` under PDLC; no certificate statement for the
  whole-space case beyond the two-quadratic one.
- **Blekherman, Dey, Sun (2024), SIAM J. Optim. 34(1):98–126, arXiv:2210.01722.**
  Introduce HHC; Theorem 2.8 (hull by good aggregations when `S != empty`,
  `conv(S) != R^n`, `n >= 3`); Proposition 2.12 (emptiness certificate under
  hidden convexity); Proposition 2.13 (if no nonzero `lambda >= 0` has
  `A_lambda` PSD, then `conv(S) = R^n`, under hidden convexity of the quadratic
  parts); Theorem 2.11(2) (for diagonal matrices, `conv(S) != R^n` if and only
  if some `lambda >= 0` has a nonzero PSD `A_lambda`, without any HHC
  hypothesis; this is a separable special case with the same conclusion as
  Theorem 1, obtained there by a different argument); Lemma 7.3 (the sphere and
  halfspace case). Conjecture 3.3 is stated in their Section 3 as the remaining
  case: "all nonzero solutions to `sum lambda_i A_i` PSD, `lambda >= 0` also
  satisfy `sum lambda_i A_i = 0`, `sum lambda_i b_i = 0` and `sum lambda_i c_i < 0`".
  Theorem 1 resolves this case affirmatively. Their Conjectures 3.1 (infinitely
  many good aggregations may be needed under HHC) and 3.2 (six aggregations may
  be needed for three quadratics under PDLC) are not addressed here.
- **Fujie, Kojima (1997), J. Global Optim. 10:367–380, Theorem 2.1; Kojima,
  Tuncel (2000), SIAM J. Optim. 10(3):750–778, Theorem 4.2.** The projection of
  the Shor relaxation is contained in the intersection of all convex
  aggregations, and the two sets have equal closures when `S != empty`;
  used only for context in Corollary 4. The projection itself need not be closed.
- **Sheriff (2013), PhD thesis, Harvard; Dymarsky (2018), arXiv:1410.2254.**
  "Stable convexity" of quadratic maps: definiteness gives stability for
  `m <= 3`, `n >= 3`; the roundness theorem for `m >= 4`. Used to name the
  hypothesis of Corollary 5.
- **Song, Xia (2021), arXiv:2108.08517; Nguyen, Chu, Sheu (2025), arXiv:2503.01225;
  Huy et al. (2026), arXiv:2601.13511.** Extensions of Polyak's convexity
  theorem and S-lemma variants; none treats certificates for a trivial hull
  with `m` constraints (second literature check, 2026-09-22).
- **Blekherman, Dunbar (2024), arXiv:2405.18282.** Three quadrics via the
  spectral curve; finiteness and four-aggregation results under smoothness and
  hyperbolicity. Does not treat the whole-space certificate.
- **Classical hidden convexity (Dines 1941, Brickman 1961, Calabi 1982, Polyak
  1998, Yakubovich's S-lemma).** Polyak, "Convexity of quadratic
  transformations and its use in control and optimization", J. Optim. Theory
  Appl. 99 (1998) 553–583, Theorem 2.1 (three forms, `n >= 3`, positive definite
  combination, convex image) is used in Corollary 5. Step 1 of the proof is the standard passage
  from a convex image missing the negative orthant to a nonnegative aggregation
  that is nonnegative on the hyperplane; the S-lemma corresponds to `m = 2` and
  Finsler's lemma to the hyperplane restriction. The novelty of the argument is
  in Steps 2–3: sweeping the supporting hyperplane to infinity and using the
  uniform separation constant of Lemma 3 to exclude certificates that are PSD
  only on the hyperplane. Lemma 3 itself is elementary (compactness of the unit
  sphere of a closed cone).

## 7. What the result enables and its limits

- **Certification.** Under HHC and `n >= 3`, all three regimes of a quadratic
  system are now characterized by aggregations (Corollary 2). Given HHC and
  `S != empty`, Corollary 3 supplies an exact SDP characterization of whether
  any nontrivial valid linear inequality exists for `S`. This could inform
  whether to search for cuts from the quadratic system alone. No numerically
  certified classifier is implemented here; near-zero floating-point SDP
  objectives are inconclusive without certified bounds or exact arguments.
- **Relaxation strength.** If `S != empty` has a proper convex hull and the
  hypotheses of Theorem 1 hold, there is a globally convex nontrivial
  aggregation. This is an existence guarantee, not a claim that globally
  convex aggregations imply every valid linear inequality. BDS's good
  aggregations can instead have two convex components and a nonconvex
  quadratic function. For example, on `R^3` with `x_2, x_3` free, take
  `f_1 = x_1^2 - 4` and `f_2 = -x_1^2 + 2 x_1 + 3`. Here HHC holds by Dines,
  and `S = {x : -2 < x_1 < -1}`. Every globally convex nonzero aggregation
  has `lambda_1 >= lambda_2 >= 0`, so
  `f_lambda(0) = -4 lambda_1 + 3 lambda_2 < 0`. Thus all globally convex
  aggregations admit `0`, although `x_1 < -1` is valid on `S`.
  The Shor relaxation also admits `x = 0` with
  `X = diag(7/2, 0, 0)`, whose two constraint residuals are both `-1/2`.
  It is therefore a proper relaxation, not the convex hull, even under HHC.
- **Scope.** HHC is a strong hypothesis (it fails for the example of
  Section 5 and for BDS Example 2.3). The result is about the open system; the
  closed system is covered only when the strict system is feasible (Corollary 1).
  No claim is made about the finiteness questions (Conjectures 3.1 and 3.2 of
  BDS), nor about efficient verification of HHC itself.
- **Verification scope.** Theorem 1, Lemmas 1–3, and the HHC specialization
  have Lean proofs and independent statement reviews in topic 27. Topic 28
  adds Corollaries 1, 3 and 4, Lemma 4, and the two boundary examples described
  above. The numerical software, other examples, and Corollaries 2 and 5
  remain outside those packages. The separately completed
  [infinite-aggregation package](../formal/topics/29-infinite-aggregation/README.md)
  proves actual HHC, spectral goodness, indispensable strict rays and the
  finite closed-hull obstruction for its own explicit construction.
  The example computations of
  Section 5 were checked numerically, and the prediction of Theorem 1 was
  tested on random two-quadratic systems of the form `f_2 = -f_1 + const` with
  indefinite quadratic part (only trivial certificates; exact line search
  exhibited every random target as a midpoint of two points of `S`), see
  `code/quadratic_aggregation/check_examples.py`. These checks exercise the
  `m = 2` case, where the statement was already known; they guard against
  misstatement, not against a gap in the general argument.
  The [formal verification record](../formal/topics/27-quadratic-aggregation/VERIFICATION.md)
  distinguishes the checked universal theorem from these numerical sanity checks.
