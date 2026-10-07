# Analytical audit of the exact-cover and Gram reduction

Date: 2026-10-06. Scope: the core reduction in
`research-20261001/binary-separation/note.md`, §§1, 3–4, Lemma 5,
Corollary 3, and the corresponding revision statements. The earlier reviews
were read for known corrections. The integer precursor was used only to
identify dependencies that a standalone paper should remove. This audit does
not assess literature, priority, attribution, or the later clique constructions.

## Verdict and changes needed for a standalone proof

The current core reduction is correct. Its exact description of all violated
hypermetric inequalities, the endpoint `p/12`, the positive definiteness of
the Gram matrix, the polynomial scaling, and the metric and elliptope
promises all hold analytically. No fatal mathematical error was found in
these statements. The former exponential-magnitude scaling issue is fully
resolved by `ε = 1/(8n + 2p + 1)`.

The paper should make the following small but useful improvements.

1. Prove a direct identity for arbitrary `σ`, not only `σ = 1`. It identifies
   rounded psd separation with the parity test for the binary moment matrix
   without appealing to the integer precursor.
2. The elementary proof below can replace the short-witness proof's
   imported elimination and Hermite normal form results if a proof without
   those dependencies is desired. Its explicit certificate bound is
   `|z_i| ≤ (m + 1)(m!)²H^(2m + 2)` after denominators are cleared and the
   integer matrix entries have absolute value at most `H`.
3. Specify that rounded psd vectors describing a violated inequality occur
   in the pairs `b` and `−b`. The resulting inequalities are identical;
   vectors with sum `−1` are not literally hypermetric vectors under the
   convention `σ = 1`.
4. State hardness under bounded gonality promises with the quantifier
   “for each fixed `K ≥ 3`.” Padding by an unrestricted binary-encoded `K`
   would not necessarily be a polynomial reduction.
5. The incidental observation `s ≥ 7` for X3C assumes `n ≥ 1`. If the empty
   collection is admitted, only the general bound
   `s ≥ max_i M_ii` is always valid. This does not affect any hardness proof.
6. The note states that the general exact-cover version of Corollary 3(c)
   follows from Lemma 5, but displays only the X3C entry list in its proof.
   The general entry bound is proved explicitly below.

The first two items are proof development, not corrections to the theorem.
The remaining items are minor precision issues. The easy-case assertions
that rely on external facet bounds and fixed-dimension CVP algorithms are
not needed for the reduction and have not been bibliographically verified.

## 1. Form identities and geometry

Let `W` have `m` members. Given a rational symmetric matrix `M` indexed by
`W`, write `δ = diag(M)` and define

`d_0i = M_ii`,
`d_ij = M_ii + M_jj − 2M_ij`.

For every vector `b = (b_0,z)` on `{0} ∪ W`, with
`σ = b_0 + Σ_i z_i`, expansion gives

`Q(b,d) = σ δᵀz − zᵀMz`.                                      (1)

Indeed, the coefficient of `M_ii` from the root edges is `b_0z_i`, and
that from the nonroot edges is `z_i(Σ_j z_j − z_i)`. The off-diagonal term
is `−2Σ_{i<j}z_i z_j M_ij`. Their sum is (1). In particular, when
`σ = 1`, the unique root coefficient is `b_0 = 1 − Σ_i z_i`, and

`Q(b,d) = −g_M(z)`.

Thus integer `z` and hypermetric vectors `b` are in bijection. This proves
both directions of the cut/correlation equivalence for arbitrary rational
inputs.

If `M = BᵀB`, its columns `u_i` and the origin generate squared Euclidean
distances `d`. For any center `c` with `Bᵀc = δ/2`,

`g_M(z) = ||Bz − c||² − ||c||²`.                              (2)

The equation is exact and does not require `c` to lie in `range(B)`.
Replacing `c` by its orthogonal projection onto that range leaves (2)
unchanged: the perpendicular squared norm cancels on both sides. Hence a
violator is exactly an integer combination of the generators strictly
inside their sphere through the origin. The Gram entries, not the real
coordinates of `B` or `c`, are the reduction output; irrational square roots
in a geometric realization create no encoding issue.

For completeness, the negative-type characterization also follows directly
from (1). A real vector of sum zero has `Q = −zᵀMz`, so all negative-type
inequalities hold if and only if `M` is positive semidefinite.

## 2. Exact-cover construction and complete iff proof

Let `A ∈ {0,1}^{p×n}` be the incidence matrix of the sets, with `p ≥ 2`.
The exact-cover question is whether `Ax = 1` for some `x ∈ {0,1}^n`.
Empty sets, duplicate sets, and uncovered elements do not invalidate the
following proof. Put `W = {1,…,n,g}` and choose

`max{p/12,(p−2)/4} ≤ η² < p/4`.

This interval is nonempty for every `p ≥ 2`; the rational choice
`η² = (p−1)/4` lies in it. Define

`M_ij = 4·1_{i=j} + (AᵀA)_ij`,
`M_ig = |S_i|/2`,
`M_gg = p/4 + η²`.

With `η = sqrt(η²) > 0`, the columns

`u_i = (2e_i,A_i,0)`,
`u_g = (0,1_p/2,η)`

have exactly these inner products. They are linearly independent: a zero
linear combination first forces every set coefficient to be zero through
the first block, and then forces the coefficient of `u_g` to be zero
through the last coordinate. Thus `M ≻ 0` even with empty or duplicate sets.

For `z = (x,k) ∈ Z^(n+1)` and `y = Ax ∈ Z^p`, expansion gives

`g_M(x,k) = 4Σ_i x_i(x_i−1)`
`             + Σ_e [y_e² + (k−1)y_e]`
`             + k(k−1)(p/4 + η²)`.                            (3)

The use of `A ∈ {0,1}` is essential: it gives
`Σ_i |S_i|x_i = Σ_e y_e`. The first summand in (3) is nonnegative for
every integer `x`. This permits the following complete layer analysis.

- For `k = 0`, each element term is `y_e(y_e−1) ≥ 0`.
- For `k = 1`, each element term is `y_e² ≥ 0`.
- For `k ≥ 2`, completing the square in the element terms gives
  `g ≥ −p(k−1)²/4 + k(k−1)(p/4+η²)`
  `   = (k−1)(p/4+kη²) > 0`.
- For `k = −t`, `t ≥ 2`, the integer minimum of
  `y²−(t+1)y` is `−floor((t+1)²/4)`.
  If `t` is odd, necessarily `t ≥ 3`, and
  `g ≥ (t+1)(tη²−p/4) ≥ 0` because `3η² ≥ p/4`.
  If `t` is even, then
  `g ≥ t((t+1)η²−p/4) ≥ 0` for the same reason.
- For `k = −1`, (3) becomes
  `g_M(x,−1) = 4Σ_i x_i(x_i−1) + ||Ax−1||² − c`,
  where `c = p/2−2η² ∈ (0,1]`.
  The two nonconstant terms are nonnegative integers. Their sum is less
  than `c` exactly when both are zero. This is equivalent to
  `x ∈ {0,1}^n` and `Ax = 1`.

Consequently,

`g_M(z) < 0  iff  z = (x,−1), x ∈ {0,1}^n, Ax = 1`,

and every violation has value `g_M(z) = −c`. The case `c = 1` causes no
problem: a residual of exactly one is tight, rather than violated. Likewise
the endpoint `η² = p/12` gives nonnegative, sometimes zero, values in
the `k ≤ −2` layers.

The parameter restrictions are justified, but the final paper can avoid
them by using only `η² = (p−1)/4`. For the sharpness discussion:

- At `η² ≥ p/4`, the `k = −1` layer cannot be violated; the remaining layer
  bounds are also nonnegative.
- At `0 < η² < p/12`, any exact cover gives an extra negative vector
  `(x,−2)` with value `6η²−p/2`. At `p = 3`, the two sets `{1,2}` and
  `{2,3}` have no exact cover but `x = (1,1)` gives `Ax = (1,2,1)` and
  the same negative value at `k = −2`.
- At `η² < (p−2)/4`, a binary `x` with `||Ax−1||² = 1` gives a false
  `k = −1` violator. For `p ≥ 3`, the instance with the single set
  `{1,…,p−1}` supplies such a no-instance whenever this inequality and
  `η² > 0` can hold.

## 3. Cut formulas, integer magnitude, and gonality

Fix `η² = (p−1)/4`, so `c = 1/2`. The corresponding distances are

`d_0i = 4+|S_i|`,
`d_0g = (2p−1)/4`,
`d_ij = 8+|S_i △ S_j|` for distinct set indices,
`d_ig = (2p+15)/4`.

The cancellation in `d_ig` is exact:
`(4+|S_i|)+(2p−1)/4−|S_i| = (2p+15)/4`.
All entries of `4d` are positive integers at most `4p+32`.
For the index set `T` of an exact cover, every hypermetric violator is

`b_T = (2−|T|)e_0 + Σ_{i∈T}e_i − e_g`,                     (4)

and has `Q(b_T,d) = 1/2`. There are no others.

For X3C, let `p = 3q` and assume `q ≥ 2`. Every exact cover contains
exactly `q` sets, since summing the equations `Ax = 1` gives
`3Σ_i x_i = 3q`. Formula (4) therefore has gonality

`|2−q| + q + 1 = 2q−1`.

Its support has `q+2` points for `q ≥ 3` and `q+1 = 3` points for `q = 2`.
Hence every inequality of gonality at most `2q−3` holds.

For general exact cover, a cover with one set yields a three-coordinate
triangle vector `(1,1,−1)`, and a cover with two sets yields the same
triangle vector on those two set indices and `g`. Every cover with at
least three sets yields a vector of gonality at least five and cannot
represent a triangle inequality. Since (4) is complete, all triangle
inequalities hold if and only if no exact cover uses at most two sets.
This includes no-instances, which satisfy every hypermetric inequality.

For every fixed `K ≥ 3`, X3C restricted to `q ≥ K` remains hard. Add
`K` disjoint triples of new elements and one set for each triple. Each new
set is forced because no other set contains its elements. Covers before
and after padding correspond bijectively after the forced sets are removed
or inserted. The new parameters are `n+K` and `p+3K`; padding is polynomial
for fixed `K`. Thus hardness survives all hypermetric inequalities of any
prescribed fixed gonality bound, by choosing `2K−3` at least that bound.

## 4. Scaling bound, with every constant explicit

Let `δ = diag(M)` and `s = δᵀM^−1δ`. Define the real vector

`c* = (1_n,1_p/2,γ)`,
`γ = (η²−p/4)/(2η) = −1/(8η)`.

For every set column,
`u_iᵀc* = 2+|S_i|/2 = M_ii/2`, and for the distinguished column,
`u_gᵀc* = p/4+ηγ = (p/4+η²)/2 = M_gg/2`.
Thus `Bᵀc* = δ/2`. The orthogonal projection
`Π = B(BᵀB)^−1Bᵀ` gives

`s = 4||Πc*||² ≤ 4||c*||²`
`  = 4n+p+1/[4(p−1)]`.

Since `p ≥ 2`, the final fractional term is at most `1/4`. With

`N = 8n+2p+1`, `ε = 1/N`,

we obtain `s < N/2` and therefore `εs < 1/2`. For the lower bound,
Cauchy–Schwarz in the positive definite `M` inner product gives

`δ_i² = (e_iᵀM M^−1δ)² ≤ M_ii s`.

Here `δ_i = M_ii > 0`, so `s ≥ M_ii` for every index, including `g`.

Define the binary moment matrix

`Y_ε = [[1,εδᵀ],[εδ,εM]]`.

Its diagonal consistency `Y_ii = Y_0i` is immediate. More strongly, for
every real `θ ≤ 1/2`, its Schur complement with respect to the positive
definite lower block `εM` gives

`Y_ε−θe_0e_0ᵀ ≻ 0  iff  1−θ−εs > 0`.

The right-hand side is positive. In particular `Y_ε ≻ 0`; no assertion
about inverse-matrix entry magnitudes is required.

All encoding assertions can be checked without matrix inversion. For X3C,
`4N Y_ε` has the entries

`4N` at `(0,0)`,
`28` at each set diagonal and root/set entry,
`2p−1` at the `g` diagonal and root/`g` entry,
`4|S_i∩S_j|` at distinct set entries,
`6` at set/`g` entries.

All are integers in `[0,4N]`. For general exact cover, replace `28` by
`16+4|S_i|` and `6` by `2|S_i|`. If a set index exists, then `n ≥ 1` and

`16+4|S_i| ≤ 16+4p ≤ 32n+8p+4 = 4N`.

The other bounds are immediate from `|S_i| ≤ p`. If `n = 0`, no such entries
exist and the same conclusion holds. Thus the general exact-cover assertion
is valid too. Reduced fractions for the entries of `Y_ε` have numerators
and denominators at most `4N`. The scaled distances have denominator
dividing `4N` and positive numerators at most `4p+32` whenever a set
exists, also at most `4N`; with no set index the single root/`g` entry is
bounded directly by `2p−1`.

## 5. Complete classification of rounded psd and split violators

For an odd integer `σ` and `z ∈ Z^W`, set
`b = (σ−Σ_i z_i,z)` and `u = (σ,−2z)`. By (1), the slack of the rounded
psd inequality at `εd` is

`(σ²−1)/4 − Q(b,εd)`
`  = (σ²−1)/4 + ε(zᵀMz−σδᵀz)`
`  = (uᵀY_εu−1)/4`.                                         (5)

If `|σ| ≥ 3`, positive definiteness of
`Y_ε−e_0e_0ᵀ/2` implies

`uᵀY_εu > σ²/2 ≥ 9/2 > 1`.

Consequently no such inequality is violated. For `σ = 1`, the slack is
`εg_M(z)`. For `σ = −1`, it is `εg_M(−z)`. The reduction theorem then
shows that all violated rounded psd vectors are exactly

`b = b_T` and `b = −b_T`,

where `T` is an exact cover. The pair describes the same inequality.
Each violation is `1/(2N)`.

The split convention used in the precursor and the proposed paper is
`q_Y(v) = vᵀYv+e_0ᵀYv`. Its parity identity is a direct expansion:

`q_Y(v) = [(2v+e_0)ᵀY(2v+e_0)−Y_00]/4`.

Every parity vector has odd root coordinate and even remaining
coordinates. Applying (5) and the exact-cover classification gives exactly
the split violators

`v = (0,−x,1)` and `v = (−1,x,−1)`,

where `Ax = 1` and `x ∈ {0,1}^n`. Both have
`q_{Y_ε}(v) = −1/(2N)`. This also proves the Boolean quadric
Boros–Hammer classification directly, without importing a theorem about
the earlier integer construction.

## 6. Elliptope and metric membership

Let `D` be the symmetric distance matrix of `εd`, with zero diagonal, and
put `Z = J−2D`. Define

`L = [[1,0],[1_W,−2I]]`.

It is invertible, with determinant `(-2)^|W|`. Entrywise use of
`Y_ii = Y_0i` gives

`Z = L Y_ε Lᵀ`.

Indeed, its root/set entries are `1−2εM_ii`, its nonroot diagonal entries
are one, and its other nonroot entries are
`1−2εM_ii−2εM_jj+4εM_ij = 1−2εd_ij`.
Therefore `Z ≻ 0` and `diag(Z) = 1`. This is exactly interior membership
in the elliptope relative to its affine hull. Every `2×2` principal
minor is positive, so `|Z_uv| < 1` for `u ≠ v`; hence
`0 < εd_uv < 1`. This argument works for all general exact-cover
instances with `p ≥ 2` and does not require triangle inequalities.

Triangle inequalities are homogeneous hypermetric inequalities, so they
hold after scaling whenever they held before scaling. Perimeter
inequalities `d_uv+d_uw+d_vw ≤ 2` are rounded psd inequalities with
`b = e_u+e_v+e_w` and `σ = 3`; they hold by (5). Thus the scaled distance
belongs to the metric polytope whenever no cover uses at most two sets,
in particular for X3C with `q ≥ 3`. All these promises are independently
proved; none is inferred from a numerical experiment.

## 7. Self-contained short-integer-witness lemma

This is a replacement for Lemma 2's precursor/Hermite-normal-form
dependencies. It is deliberately coarse; polynomial encoding, rather than
the best coordinate bound, is the required conclusion.

**Lemma.** Let `C ∈ Z^(m×m)` be symmetric, `m ≥ 1`, let `c = diag(C)`, and
let `H = max{1,max_ij |C_ij|}`. If
`zᵀCz−cᵀz < 0` for some `z ∈ Z^m`, then it holds for a vector satisfying

`|z_i| ≤ U := (m+1)(m!)²H^(2m+2)` for every `i`.

**Proof.** For any `r×r` submatrix with entries bounded by `H`, determinant
expansion gives absolute determinant at most `r!H^r`. Every cofactor is
at most `(r−1)!H^(r−1)`. Use these bounds below.

### 7.1 Non-positive-semidefinite matrices

Choose a positive definite principal submatrix `D = C_KK` maximal under
inclusion, where `r = |K|`. The empty block is allowed, with determinant
one. Write `h = det(D) > 0` for a nonempty block and form the Schur
complement `S` on the remaining coordinates. Maximality implies
`S_ii ≤ 0`, since a strictly positive entry would extend `D` to a positive
definite principal block. If some `S_ii < 0`, take a vector with remaining
part `e_i` and `K` part `−D^−1 C_Ki`. Its quadratic value is `S_ii < 0`.
If all `S_ii = 0`, non-positive-semidefiniteness implies some
`S_ij ≠ 0`; otherwise `S = 0` and block elimination would make `C`
positive semidefinite. Choose `t ∈ {−1,1}` so that `tS_ij < 0` and use
remaining part `e_i+t e_j` and `K` part
`−D^−1(C_Ki+t C_Kj)`. Its quadratic value is `2tS_ij < 0`.

Multiplication by `h` makes the resulting vector `y` integral. The
determinant and cofactor bounds give
`|y_i| ≤ 2r!H^r ≤ 2m!H^m`. Choose between `y` and `−y` so that
`cᵀy ≥ 0`. Then
`yᵀCy−cᵀy < 0` already, without any additional multiplier. Its
coordinates obey the stated bound `U`. For the empty block the same proof
uses an integral coordinate vector or a sum of two coordinate vectors.

### 7.2 Positive-semidefinite matrices with `c` outside the range

Let `r = rank(C)`. If `r = 0`, then `C = 0` and `c = 0`, so this case
cannot arise. A positive-semidefinite matrix of rank `r` has a positive
definite principal `r×r` block `D = C_KK`: choose linearly independent
vectors in any Gram representation. Put `P = C_{K,·}` and `h = det(D)`.
The zero Schur complement gives

`C = PᵀD^−1P`.

For every nonroot coordinate `j` outside `K`, the integral vector

`y_j = h`,
`y_K = −adj(D)C_Kj`,
`y_i = 0` otherwise

satisfies `Py = 0` and therefore `Cy = 0`. At least one of these vectors
has `cᵀy ≠ 0`. Otherwise all entries of `c` would satisfy
`c = PᵀD^−1c_K`, placing `c` in `range(C)`. Choose its sign so that
`cᵀy > 0`. Then `yᵀCy−cᵀy = −cᵀy < 0`, and
`|y_i| ≤ r!H^r ≤ U`.

### 7.3 Positive-semidefinite matrices with `c` in the range

The rank-zero case again has no violation. Choose `D`, `P`, and `h` as
above. The range condition implies
`c = PᵀD^−1c_K`, because the restriction of `Pᵀ` to `K` is `D`.
For `y = Pz`, therefore,

`zᵀCz−cᵀz = ||y−c_K/2||²_{D^−1}−||c_K/2||²_{D^−1}`.

At a violator, the triangle inequality gives
`||y||_{D^−1} < ||c_K||_{D^−1}`. Cauchy–Schwarz for each coordinate gives

`|y_i|² ≤ D_ii ||y||²_{D^−1}`
`        < H c_KᵀD^−1c_K`
`        ≤ r²(r−1)!H^(r+2)`
`        = r·r!H^(r+2)`.

Here `h ≥ 1` and the cofactor bound were used in the last inequality.
The coarse bound
`|y_i| ≤ T := m!H^(m+2)` follows. Also `y = Pz` is integral.

There is an integer solution of `Pz = y` by assumption. Partition its
coordinates into `K` and its complement, so `P = [D,F]` after a column
permutation. Replace each complementary coordinate by its remainder
`t_j ∈ {0,…,h−1}` modulo `h`. Define the new `K` part by

`z_K' = D^−1(y−Ft)`.

It remains integral: changing the complementary part by a multiple of
`h` changes the `K` part by `hD^−1` times an integer vector, and
`hD^−1 = adj(D)` is integral. Its coordinates satisfy

`|z_K'|_∞ ≤ r!H^(r−1)[T+(m−r)H(h−1)]/h`
`          ≤ r!H^(r−1)T+(m−r)r!H^r`
`          ≤ m!H^(m−1)T+m·m!H^m`
`          ≤ (m+1)(m!)²H^(2m+2) = U`.

The complementary coordinates are also bounded by `U`, since
`h ≤ r!H^r`. The new vector has the same `Pz = y` and hence the same
negative quadratic slack. This completes the proof.

### 7.4 Rational inputs and certificate size

For a rational symmetric `M` of input bit length `L`, take the product
`a` of its positive entry denominators and put `C = aM`. Then `C` is
integral, `diag(C) = a diag(M)`, and `g_C = a g_M`; the sign of the slack
is preserved. The crude bounds `a ≤ 2^L` and
`H ≤ 2^(2L)` suffice. Thus

`log_2 U ≤ log_2(m+1)+2m log_2 m+4(m+1)L`.

The total bit length of the integer vector is polynomial in the input
length. The hypermetric root coefficient has absolute value at most
`1+mU`, so its encoding is polynomial too. Exact rational verification
of the inequality is polynomial in the input and certificate lengths.
Consequently hypermetric violation belongs to NP for all rational inputs.

The proof does not claim a polynomial algorithm for finding the bounded
image `y` in the last case; that is the hard closest-vector step. It only
proves that some polynomial-size certificate exists.

## 8. Complexity statements and clean theorem chain

Use the explicit finite-universe encoding of X3C, or its incidence matrix.
Then `n+p` is polynomial in the source length. If instead the universe
`[3q]` is represented implicitly with binary `q`, first map every instance
with `n < q` to a fixed no-instance. On the remaining instances
`p = 3q ≤ 3n`, so the output size and the padding size are still polynomial.

For the unscaled integral output `4d`, the number of coordinates is
`binom(n+2,2)` and every coordinate is at most `4p+32`. The reduction is
computable by incidence intersections, uses polynomial time, and has
polynomially bounded numerical magnitudes. Hypermetric violation is
strongly NP-hard and, by the witness lemma, strongly NP-complete. Taking
the complement gives strong co-NP-completeness of hypermetricity.

The scaled rational output uses denominator `4N`, with
`N = 8n+2p+1`, and numerators at most `4N`. Its total binary encoding is
`O((n+2)² log(n+p+2))`, and its unary numerical encoding is also
polynomial. The exact same yes/no equivalence holds simultaneously for
hypermetric, rounded psd, and binary split/Boros–Hammer violation by the
complete classifications above. This proves strong hardness on inputs
that lie in the metric polytope and the interior of the elliptope and
whose binary moment matrix is positive definite. NP membership for the
larger classes should be proved in the algorithms section; a statement of
hardness at the end of the construction does not need to assume it.

A minimal standalone theorem chain is:

1. The form identity `Q = σδᵀz−zᵀMz`, with the hypermetric bijection and
   the direct parity/split identity.
2. The exact-cover Gram theorem, using the fixed value `(p−1)/4` in the
   main proof and optionally giving the full parameter window in a remark.
3. The scaling lemma and the explicit polynomial entry bounds.
4. The relaxation theorem: complete hypermetric and rounded/split
   classifications, low-gonality promises, and metric/elliptope membership.
5. The complexity corollary, using fixed-`K` forced-triple padding and
   forward references to the short-witness lemmas.

The geometrical sphere picture explains the binary structure, but the
complexity proof is entirely an integer layer argument. The paper should
not require readers to know closest-vector reductions or Kannan embedding
in order to verify its main theorem.

## Verification record

This was an analytical audit. Read-only commands were `cat`, `sed`, and
`rg` on the root `AGENTS.md`, the core source, its three review reports,
its revision sections, and the relevant headings in the integer precursor.
The manuscript preamble and macro file were also read after section
authorship was authorized. No checker, numerical experiment, benchmark,
project-wide verification, or CI inspection was run. Earlier computational
results were treated as context, not as evidence for this audit's verdict.
