# Completeness of the three-variable cube cuts, and four positive variables

Date: work began 2026-10-01 and continued through revisions on 2026-10-03. Stream:
`three-var-completeness`. Final status (2026-10-04): reviewed in two rounds;
r2 minor fixes applied; the last revision's fixes checked by the coordinating
agent against the logs; the author performed the S1 symbolic rerun during
the r2 revision (`logs/check_boundary_rank_symbolic_r2_revision.txt`);
not refereed. The independent [round-2 review](reviews/review-r2.md)
confirmed all 12 round-1 fixes and found one minor reporting issue and three
cosmetic issues, with no error in a proved statement. "Reviewed" in this
program means checked by another research agent, not journal peer review.
A first author run was cut off by a usage limit on
2026-10-02 at about 04:30 UTC; this note completes and corrects its draft
(Section 6 lists the corrections). Existing stream material was included in
repository commits made outside this program; the program itself makes no commits.

## Summary

**(a) Three variables.** Read literally, the answer is no: the 24 symmetry
copies of the three-positive family together with the disjoint-support
affine-SOS cone `D3` cannot describe all quadratics nonnegative on `[0,1]^3`,
because every quadratic in either cone has nonnegative square coefficients.
The three caps `x_i(1-x_i) >= 0` (moment form `Y_ii <= x_i`) are missing, and
they are the only gap of this kind (Proposition 2.2, proved). The substantive
question is whether the positive-loop cone `P3+` (cube-nonnegative quadratics
with nonnegative square coefficients) equals `cl(D3) + (24 family cones)`.

New proved results narrow this question sharply.

- *Sign classes (Theorem 2.5, proved; uses Theorem 1 of Burer, Natarajan and
  Willemsen, arXiv:2504.03996v3, as an external input).* If the three cross
  coefficients satisfy `q_12 q_13 q_23 <= 0`, a cube-nonnegative quadratic with
  nonnegative square coefficients already lies in `cl(D3)`; without the sign
  condition on squares it lies in `cl(D3) + caps`. The key new step is that the
  disjoint moment relaxation is invariant under an exact "rounding" map
  (Lemma 2.3, proved and checked symbolically). Hence the family copies are
  needed only for quadratics with `q_12 q_13 q_23 > 0`, which after
  complementing coordinates have all three cross coefficients positive
  (supermodular), and only 6 of the 24 copies can contribute an extreme ray of
  that sign pattern (Corollary 2.6).
- *Extreme rays of the family beyond the five-contact regime (Proposition 2.10,
  proved with exact symbolic rank computations).* Family members on five
  boundary strata, where one contact becomes a tangential vertex zero or two
  contacts merge at a vertex, span extreme rays of the cube-nonnegative cone
  for all parameters in each stratum.

No missing ray was found. About 36,400 valid quadratics (mostly extreme rays)
from ten samplers were tested against the relaxation `R` (the 27 disjoint
localizing matrices plus the 24 family LMIs); 1,371 of them lie outside
`cl(D3)` numerically, and none lies outside the dual of `R` at the detection
threshold (smallest normalized value `-7.0e-9`, at solver-accuracy scale;
the corresponding ray was not stored or re-solved). These samplers include a
systematic enumeration of all 6,418 combinatorial types of point-contact zero
configurations that can determine an extreme ray, with about 3.35 million
rank-9 contact systems solved at random positions (Section 2.8): the rays it
found outside `cl(D3)` come from six types, and every stored example (34) fits
a family member, in the five-contact regime or on the boundary strata above.
We also prove that a point of `R` outside `H3+` must satisfy all three caps
strictly (Corollary 2.4 (iv)). We conjecture that
`P3+ = cl(D3) + sum of the 24 family cones`, equivalently that `R` together
with `Y_ii <= x_i` is the quadratic moment hull `QPB_3` (Conjecture 2.11). This is numerical evidence, not a proof; by Corollary 2.6 a
proof only has to treat strictly supermodular quadratics.

**(b) Four positive variables: the complete graph has no finite SDP lift.**
The quadratic moment hull `QPB_4 = conv{(x, xx^T) : x in [0,1]^4}`, its
positive-loop version `H_4^+`, and their dual cones are not spectrahedral
shadows (Theorem 4.2, proved, using results of Bodirsky, Kummer and Thom as
external inputs). So the positive graph `K_4` admits no finite SDP extended
formulation of any size. More generally, if the positive graph has a `K_4`
minor, the joint hull has no finite SDP lift (Theorem 4.6). This improves the
`K_5`-minor theorem of 2026-09-25 to `K_4`. The same argument shows that the
copositive and completely positive cones over any pointed polyhedral cone of
dimension at least five with a simple extreme ray are not spectrahedral
shadows; in particular the cone of quadratics nonnegative on any polytope of
dimension at least four with a simple vertex is not a shadow (Theorem 4.4).
The fact `CP_4 = DNN_4` gives finite lifts only for components with at most
three positive vertices: a triangulation of `[0,1]^4` has simplices with five
vertices, whose moment cones are `CP_5`, and Theorem 4.2 shows that no other
construction can succeed.

What remains open is the series-parallel case: positive graphs without a `K_4`
minor that have a component with four or more vertices. The class of positive
graphs with a finite lift is closed under minors (Proposition 4.7), so the two
minimal open graphs are the path `P_4` and the star `K_{1,3}`. If both lack
finite lifts, a finite lift exists exactly when every positive component has
at most three vertices. For `P_4` our method would settle the case if the cone
of copositive `5 x 5` matrices with the fan pattern `F_5` is not a
spectrahedral shadow (Lemma 4.8); a numerical sum-of-squares test is
inconclusive (Section 4.7). For `K_{1,3}` every local cone is a shadow, so a
proof of non-representability needs a global argument. For trees, the
question reduces to the submodular part of the cone, and a finite lift for the
submodular part of the dense four-variable cone would give lifts for both
`P_4` and `K_{1,3}` (Remark 4.9).

**Solver relevance.** Limited. For a three-variable box QP, Theorem 2.5 says
that a solver which already imposes the disjoint system needs the family block
only when the objective cross coefficients have a positive product; this
halves the strict sign patterns for which the block can help. In a larger or
constrained model, the relevant quadratic on a triple is a dual aggregate of
the objective and constraints, so the objective's cross coefficients alone do
not justify omitting a block. We make no runtime claim. If
Conjecture 2.11 holds, `R` plus the caps is an exact SDP description of the
three-variable box hull without a triangulation, but it uses 27 localizing
blocks and 24 five-by-five blocks, more than the six `4 x 4` DNN blocks of the
Anstreicher-Burer lift. Part (b) is a limitation: no exact compact SDP exists
for a dense four-variable box-QP term, so exact convexification there must rely
on separation (for example Burer-Dong's recursive procedure) or on non-SDP
cones.

## 1. Setting and notation

Write a quadratic on `R^3` as `p(x) = c_0 + sum_i c_i x_i + sum_i q_ii x_i^2 +
sum_{i<j} q_ij x_i x_j`, and let

- `P3` be the cone of quadratics with `p >= 0` on `C = [0,1]^3`;
- `P3+` be the subcone with `q_ii >= 0` for all `i` (the dual of the
  positive-loop hull);
- `K3 = conv{(x, xx^T) : x in C}` (the quadratic moment hull, `QPB_3`), and
  `H3+ = K3 + D`, where `D` adds nonnegative slack to the three diagonal moment
  coordinates;
- `V` be the span of the 20 monomials `x^a` with `a in {0,1,2}^3` and at most
  one exponent equal to 2, and `W` the span of the ten monomials of degree at
  most two;
- a *generator* be a polynomial `g = w_{A,B} L^2`, where `A, B` are disjoint
  subsets of `{1,2,3}`, `w_{A,B} = prod_{i in A} x_i prod_{j in B} (1-x_j)`,
  and `L` is affine in the coordinates outside `A u B`. Every generator lies in
  `V`. `K` is the convex cone in `V` generated by all generators, `D3^quad =
  K cap W` (the quadratic disjoint-support certificates of the 2026-09-25 note);
- `R_D` be the set of quadratic moment points `(m, Y)` that extend to a linear
  functional `l` on `V` with `l(1) = 1` and `l(g) >= 0` for every generator
  (equivalently, all 27 localizing matrices are positive semidefinite);
- `F` be the valid family `q_{h,d,k} = L^2 + 2 d_3 k z (1-x-y) + k(2D+k) xy`,
  `L = h - d_1 x - d_2 y + d_3 z`, `D = d_1 + d_2 - h`, `h` real, `d, k >= 0`
  ([family note](../../research-20260925/three-positive-family-sdp.md)), and
  `gF = {q o g : q in F}` for `g` in the symmetry group `G48` of the cube (24
  distinct copies, since swapping `x` and `y` only swaps `d_1` and `d_2`);
- `R` be the set of points of `R_D` that satisfy the family LMI of every copy
  `g`: `[[1, b^T],[b, B - N_g]] >= 0` with `N_g >= 0`, zero diagonal, where
  `b, B` are formed from the moments of `g(x)`.

Write `p(y) = <p, y>` for the value of a quadratic at a moment point.

**Duality remark (proved).** A quadratic `p` is nonnegative on `R_D` if and
only if `p in cl(D3^quad)`, and `p` is nonnegative on `R` if and only if
`p in cl(D3^quad) + sum_g cl cone(gF)`.

*Proof.* If `l` is feasible and `l'` is nonnegative on generators with
`l'(1) = 0`, then `l + t l'` is feasible for all `t >= 0`; so `p >= 0` on `R_D`
means `l(p) >= 0` for every `l` in the dual cone `K*`, that is
`p in cl(K) cap W`. The set `W` meets the interior of `K`: otherwise some
nonzero `l in K*` vanishes on `W`; testing `l` on the generators
`x_i L(x_j,x_k)^2` and `(1-x_i) L(x_j,x_k)^2` (whose degree-two parts have
`l = 0`) shows that the 2 x 2 matrix of values of `l` on `x_i x_j^2`,
`x_1 x_2 x_3`, `x_i x_k^2` is both positive and negative semidefinite, hence
zero, and then `x_i x_j L(x_k)^2` and `x_i (1-x_j) L(x_k)^2` give
`l(x_i x_j x_k^2) = 0`; so `l = 0`. Hence `cl(K) cap W = cl(K cap W)`
(Rockafellar, Corollary 6.5.1). For `R`, the family theorem of 2026-09-25 says
that the LMI of copy `g` holds exactly when `l(q) >= 0` for all `q in gF`, a
closed condition. The uniform moment point lies in the interior of `H3+`, hence
of `R_D`, and satisfies the family constraints, so `R` is dense in
`cl(R_D) cap (family constraints)`; the dual of an intersection of closed
convex cones is the closure of the sum of the duals, and the sum is closed by
Lemma 2.7. ∎

## 2. Part (a): do the symmetry copies complete the description?

### 2.1 The caps are the only literal gap

**Lemma 2.1 (rounding of measures; proved).** For every `n`, `K_n = H_n^+ cap
{Y_ii <= x_i, i = 1..n}`, where `K_n = conv{(x, xx^T) : x in [0,1]^n}` and
`H_n^+ = K_n + D`.

*Proof.* At atoms `Y_ii = x_i^2 <= x_i`, so `K_n` lies in the right side.
Conversely let `z = k + d` with `k in K_n`, `d` diagonal slack, and suppose
`z` satisfies `Y_ii <= x_i`. Let `mu` be a finite measure representing `k`.
Replacing coordinate `i` of every atom by an independent Bernoulli variable
with the same mean gives a measure `mu^(i)` with the same first moments and the
same products `E[x_i x_j]` for `j != i`, and with `E[x_i^2] = E[x_i]`. The
mixture `(1-t) mu + t mu^(i)` changes only `Y_ii`, which moves continuously from
`Y_ii(k)` to `x_i`. Since `Y_ii(k) <= Y_ii(z) <= x_i`, some `t` matches `Y_ii(z)`.
Rounding coordinate `i` does not change other diagonal entries, so the
coordinates can be treated one at a time. Hence `z in K_n`. ∎

**Proposition 2.2 (proved).** `P3 = P3+ + cone{x_1(1-x_1), x_2(1-x_2),
x_3(1-x_3)}`. Consequently, if `P3+ = cl(D3^quad) + sum_g cl cone(gF)` (that
is, `H3+ = R`), then `P3 = cl(D3^quad) + sum_g cl cone(gF) + (caps)` and
`K3 = R cap {Y_ii <= x_i}`. The converse implications also hold
(Corollary 2.4 (iv)).

*Proof.* Homogenize: the closed cone over `K3` is the intersection of the
closed cone over `H3+` with the three homogeneous halfspaces `Y_ii <= x_i`
(at height zero the first cone contains only nonnegative diagonal directions,
which the halfspaces remove). Dualizing an intersection of closed cones gives
the closure of the sum of the duals, that is `cl(P3+ + caps)`. The sum is
closed: if `a_k + sum_i c_{k,i} x_i(1-x_i) -> p` with `a_k in P3+` and
`c_{k,i} >= 0`, evaluation at the center gives `a_k(center) + sum_i c_{k,i}/4
-> p(center)`, so the `c_{k,i}` are bounded, and a convergent subsequence
leaves `a_k -> p - sum_i c_i x_i(1-x_i) in P3+`. The consequences follow from
Lemma 2.1 (`R cap caps = H3+ cap caps = K3`) and the duality remark. Note that
`D3^quad` and `F` only contain quadratics with nonnegative square coefficients: the coefficient of the
monomial `x_i^2` in a generator `w_{A,B} L^2` is `w_{A,B}(0) c_i^2`, where
`c_i` is the `x_i` coefficient of `L` (zero if `i in A u B`) and
`w_{A,B}(0) in {0, 1}`; the family members have square coefficients `d_i^2`. ∎

So the literal answer to question (a) is "no, the caps are needed", and the
substantive question is whether `H3+ = R`, equivalently whether
`K3 = R cap {Y_ii <= x_i}`.

### 2.2 The disjoint relaxation is closed under rounding

The moment version of Lemma 2.1 holds for the disjoint relaxation itself. For
a coordinate `i`, define the linear *rounding map* on polynomials

```
rho_i(f)(x) = (1 - x_i) f(x)|_{x_i = 0} + x_i f(x)|_{x_i = 1}.
```

For a measure, `l o rho_i` is the moment functional of the measure in which
coordinate `i` of every atom is replaced by an independent Bernoulli variable
with the same conditional mean.

**Lemma 2.3 (proved; identities computed exactly).**

1. `rho_i` maps `V` into `V`: it fixes every monomial not containing `x_i`, and
   it replaces a factor `x_i^2` by `x_i`.
2. For every generator `g = w_{A,B} L^2`: if `i in A u B`, then
   `rho_i(g) = g`; if `i` is a free coordinate, then
   `rho_i(g) = w_{A, B+i} L|_{x_i=0}^2 + w_{A+i, B} L|_{x_i=1}^2`, a sum of two
   generators.
3. The functional `delta_i(f)` = (coefficient of `x_i^2` in `f`, with the other
   coordinates set to 0) is nonnegative on every generator, equals 1 on
   `x_i^2`, and vanishes on every other monomial of degree at most two.

Consequently, if `(m, Y) in R_D`, then (a) `(m, Y + t E_ii) in R_D` for all
`t >= 0`, where `E_ii` is the diagonal unit matrix; (b) the point obtained by replacing `Y_ii` with `m_i` is in
`R_D`. Hence `R_D + D = R_D` and `R_D = (R_D cap {Y_ii <= m_i for all i}) + D`.

*Proof.* Parts 1 and 2 are direct computations. For `i in A`, `g` vanishes at
`x_i = 0` and equals `(w_{A,B}/x_i) L^2` at `x_i = 1`; for `i in B` the roles
are exchanged; for `i` free, `L|_{x_i=0}` and `L|_{x_i=1}` are affine in the
remaining free coordinates. For part 3, the `x_i^2` coefficient of `g` is zero
if `i in A u B` and is `w_{A,B} c_i^2` otherwise, where `c_i` is the `x_i`
coefficient of `L`; at the point with the other coordinates zero this is
`w_{A,B}(0) c_i^2 >= 0`. Now let `l` be a feasible functional for `(m, Y)`. Then
`l + t delta_i` is feasible (it is nonnegative on generators and still has
value 1 at the constant), which gives (a). The functional `l o rho_i` is
nonnegative on every generator by part 2, has value 1 at the constant, and has
the same quadratic moments as `l` except that `x_i^2` gets the value `l(x_i)`,
which gives (b). For the last statement, apply (b) to each coordinate with
`Y_ii > m_i` (the maps change only their own diagonal entry) and add back the
slack `Y_ii - m_i >= 0`. ∎

The script `code/check_rounding_map.py` verifies parts 1-3 in exact symbolic
arithmetic for all 27 weights and the three coordinates (81 cases). The same
lemma, with the same proof, holds for the two-variable disjoint system.

**Corollary 2.4 (proved).** (i) Every quadratic in two variables that is
nonnegative on `[0,1]^2` and has nonnegative square coefficients is nonnegative
on the two-variable disjoint relaxation `R_D2`. (ii) Every `q in P3+` with some
`q_ii = 0` lies in `cl(D3^quad)`. (iii) Every `q in P3` whose Hessian is
positive semidefinite lies in `D3^quad`. (iv) For every `(m, Y) in R_D` and
every `i`, the point obtained by setting `Y_ii = m_i` lies in `H3+`.
Consequently every point of `R_D`, and hence of `R`, outside `H3+` satisfies
`Y_ii < m_i` for all `i`; `R` is invariant under the rounding maps; and the
converses in Proposition 2.2 hold: `K3 = R cap {Y_ii <= x_i}` implies
`H3+ = R`, and `P3 = S + caps` implies `P3+ = S`, where
`S = cl(D3^quad) + sum_g cl cone(gF)`.

*Proof.* (i) By Theorem 2 of Anstreicher and Burer (2010) (as quoted in BNW,
Proposition 2), for two variables the Shor matrix together with all RLT
inequalities, including `X_ii <= x_i`, is an exact relaxation. Every RLT
inequality is `l` of a generator (`x_i`, `1 - x_i`, `x_i x_j`, `x_i(1-x_j)`,
`(1-x_i)(1-x_j)`, `x_i^2`, `(1-x_i)^2`) or a cap, so `R_D2 cap {caps}` lies in
that relaxation. By
Lemma 2.3, `inf_{R_D2} q = inf_{R_D2 cap caps} q` when `q_ii >= 0`, and this is
at least `min_{[0,1]^2} q >= 0`.
(ii) Say `q_33 = 0`. Then `q` is affine in `x_3`, so
`q = (1 - x_3) q_0 + x_3 q_1` with `q_c = q|_{x_3 = c}`; both are two-variable
quadratics as in (i). For a feasible `l` on `V`, the functional
`f -> l((1 - x_3) f)` is nonnegative on the two-variable generators (their
products with `1 - x_3` are three-variable generators). If its value at 1 is
positive, (i) gives `l((1 - x_3) q_0) >= 0`; if it is zero, the same follows by
the recession argument of the duality remark. Likewise
`l(x_3 q_1) >= 0`, so `l(q) >= 0`, and the duality remark gives the claim.
(iii) Let `x*` minimize `q` over the cube. The KKT conditions give
`grad q(x*) . (x - x*) = sum_{x*_i = 0} lambda_i x_i + sum_{x*_i = 1} mu_i (1 - x_i)`
with `lambda, mu >= 0`, so
`q(x) = q(x*) + sum lambda_i x_i + sum mu_i (1 - x_i) + (x - x*)^T Q (x - x*)`,
and every term is in `D3^quad` (a positive semidefinite form is a sum of affine
squares).
(iv) Let `l` be feasible for `(m, Y)` and `q in P3+`. Then
`(l o rho_i)(q) = l((1 - x_i) q|_{x_i=0}) + l(x_i q|_{x_i=1})`, and both
restrictions are two-variable quadratics as in (i); the argument of (ii) shows
that both terms are nonnegative. So the quadratic moments of `l o rho_i`, which
are those of `(m, Y)` with `Y_ii` replaced by `m_i`, are nonnegative on all of
`P3+`, that is, they lie in `H3+` (the dual of `P3+` at height one, by the
bipolar theorem; `H3+` is closed). If `Y_ii >= m_i`, then `(m, Y)` is this point
plus diagonal slack, hence in `H3+`. Since `H3+ subseteq R`, rounding maps `R`
into itself. If `K3 = R cap caps` and `y in R`, either some `Y_ii >= m_i` and
`y in H3+`, or `y` satisfies the caps and lies in `K3`; so `R = H3+`. Finally, if
`P3 = S + caps`, every `y in R cap caps` is nonnegative on `P3`, so it lies in
`K3`, and the previous sentence applies. ∎

In words: once one coordinate is rounded to a Bernoulli variable, the problem
splits into two two-variable problems, on which the disjoint system is exact.
The script `check_rounding_hull.py` tests (iv) numerically (Section 7).

### 2.3 Submodular sign class: the disjoint system suffices

Complementing coordinate `i` (`x_i -> 1 - x_i`) maps the cube to itself, maps
generators to generators (it exchanges the roles of `i` in `A` and `B`), maps
the family copies to family copies, keeps square coefficients, and changes the
sign of `q_ij` for `j != i`. The product `q_12 q_13 q_23` is invariant.

**Theorem 2.5 (proved, given BNW Theorem 1).** Let `q` be a quadratic that is
nonnegative on `[0,1]^3` with `q_12 q_13 q_23 <= 0`. Then
`q in cl(D3^quad) + cone{x_i(1-x_i)}`. If in addition `q_ii >= 0` for all `i`,
then `q in cl(D3^quad)`.

*Proof.* First, some complementation makes all three cross coefficients
nonpositive. If, say, `q_12 = 0`, complement `x_1` if `q_13 > 0` and `x_2` if
`q_23 > 0`. If all three are nonzero and their product is negative, complement
`x_2` if `q_12 > 0` and `x_3` if `q_13 > 0`; then `q_12, q_13 < 0` and the sign
of `q_23` is the sign of the product, which is negative. By the invariance
above we may assume `q_ij <= 0` for `i != j`.

Burer, Natarajan and Willemsen (arXiv:2504.03996v3, 31 August 2026,
Theorem 1) prove: for `n <= 3` and every `(Q, c)` with nonpositive
off-diagonal entries of `Q`,
`min{x^T Q x + c^T x : x in [0,1]^n} = min{Q . X + c^T x : [[1, x^T],[x, X]] >= 0,
X <= x e^T}`. Here `Q_ii = q_ii` and `Q_ij = q_ij / 2`.

Assume first `q_ii >= 0`. Let `y = (m, Y) in R_D`. By Lemma 2.3,
`y = y' + s` with `y' in R_D cap {Y_ii <= m_i}` and `s` nonnegative diagonal.
The point `y'` is feasible for the BNW relaxation: its moment matrix is the
localizing matrix with `A = B = {}`; `Y'_ij <= m_i` for `i != j` is `l` of the
generator `x_i (1 - x_j)`; `Y'_ii <= m_i` holds by construction. Hence
`q(y') >= min_C q >= 0` and `q(y) = q(y') + sum q_ii s_ii >= 0`. By the duality
remark, `q in cl(D3^quad)`. For general square coefficients, Proposition 2.2
writes `q = q+ + sum c_i x_i(1-x_i)` with `q+ in P3+`; the caps change only
square and linear coefficients, so `q+` has the same cross coefficients and lies
in `cl(D3^quad)`. ∎

**Corollary 2.6 (where a missing ray must be; proved).** Let `q in P3+` be
outside `cl(D3^quad)`. Then `q_12 q_13 q_23 > 0`, all `q_ii > 0`, and the
Hessian is indefinite. After complementing at most one coordinate,
all three cross coefficients are positive. Every family member has
`q_xz = -2 d_3 (d_1 + k) <= 0` and `q_yz = -2 d_3 (d_2 + k) <= 0`, while
`q_xy = 2 d_1 d_2 + k(2D + k)` can have either sign (it is negative for some
`h > d_1 + d_2`; such members are submodular and lie in `cl(D3^quad)` by
Theorem 2.5). The copies whose members can have all cross coefficients
positive are exactly `q_{h,d,k}(pi(x, y, 1-z))` and `q_{h,d,k}(pi(1-x, 1-y, z))`
for the three choices of which coordinate plays `z`: six of the 24 copies. So
an extreme ray of `P3+` with all cross coefficients positive lies in
`cl(D3^quad) + sum_g cl cone(gF)` if and only if it lies in `cl(D3^quad)` or is
a limit of normalized members of one of these six copies (Lemma 2.7).
Conjecture 2.11 is therefore equivalent to its restriction to quadratics with
all three cross coefficients positive.

*Proof.* Theorem 2.5 and Corollary 2.4 (ii), (iii). Positive product means
either no negative cross coefficient or two negative
ones. In the latter case, complement their common coordinate; in the former,
no complementation is needed. For the family copies,
complementing the set `S` of coordinates multiplies `q_ij` by
`(-1)^{[i in S] + [j in S]}`. Members near an extreme ray with all cross
coefficients positive have the same strict signs. The base pattern
`(+, -, -)` of `(q_xy, q_xz, q_yz)` becomes `(+, +, +)` exactly for `S = {z}` and
`S = {x, y}`; the pattern `(-, -, -)` has negative product and cannot. ∎

Numerical check (Section 2.9): on 3,998 boundary rays of the submodular part
`P3+ cap {q_ij <= 0}` the smallest value over `R_D` was `-1.5e-8` and the
smallest value over the BNW relaxation `-1.7e-9`; on 3,991 boundary rays of the
supermodular part, 9 were outside `cl(D3)` and the BNW relaxation failed on
1,102.

### 2.4 Extreme rays and closedness

**Lemma 2.7 (proved).** The cone `S = cl(D3^quad) + sum_g cl cone(gF)` is
closed. An extreme ray of `P3+` lies in `S` if and only if it lies in
`cl(D3^quad)` or is a limit of normalized members of a single copy `gF`.

*Proof.* All summands lie in the pointed cone `P3+`. If `sum_j x_{k,j}`
converges with some summands unbounded, normalizing by the largest norm gives
a limit `sum_j y_j = 0` with `y_j` in the summands, not all zero, contradicting
pointedness; so the sum is closed. If an extreme ray `p` of `P3+` is written as
`sum_j p_j` with `p_j in P3+`, each `p_j` is a multiple of `p`. Finally `cl cone(gF)`
is the cone over the compact set of normalized limits of members of `gF`
(this set avoids zero), so its extreme rays lie in that set. ∎

An extreme ray of `P3+` with all `q_ii > 0` is an extreme ray of `P3` (the
diagonal constraints are inactive near it).

### 2.5 A combinatorial criterion for exclusion from `D3`

For a vertex `v` of the cube and a set `Fr` of coordinates, let
`S_Fr(v) = {x in C : x_j != 1 - v_j for all j not in Fr}` (the cube minus the
facets opposite to `v` in the directions outside `Fr`), and let `pi_Fr` be the
projection onto the coordinates in `Fr`.

**Lemma 2.8 (blocking criterion; proved).** Let `p >= 0` on `C` with zero set
`Z`, and let `v` be a vertex with `p(v) > 0`. Suppose that for every
`Fr subseteq {1,2,3}`, `pi_Fr(v)` lies in the affine hull of
`pi_Fr(Z cap S_Fr(v))` (for `Fr` empty this means `Z cap S_empty(v)` is
nonempty). Then `p` is not in `D3^quad`. We then call `v` *blocked*.

*Proof.* Suppose `p = sum_s w_s L_s^2` is a `D3` identity. Since `p(v) > 0`,
some summand has `w_s(v) > 0` and `L_s(v) != 0`. Positivity of `w_s = w_{A,B}`
at `v` forces `v_i = 1` for `i in A` and `v_j = 0` for `j in B`; with
`Fr = {1,2,3} \ (A u B)`, the weight is positive exactly on `S_Fr(v)`. All
summands are nonnegative on `C` and sum to `p`, so each vanishes on `Z`; where
`w_s > 0` this forces `L_s = 0`. Thus the affine function `L_s`, which depends
only on the coordinates in `Fr`, vanishes on `pi_Fr(Z cap S_Fr(v))` and hence on
its affine hull, which contains `pi_Fr(v)`. So `L_s(v) = 0`, a contradiction. ∎

The exclusion proof of the 2026-09-25 counterexample is the case `v = 0` of
this lemma for the five-contact family. The lemma concerns exact identities;
exclusion from the closure needs a separate argument (for example a strictly
feasible rational moment point, as in the 2026-09-25 note). Numerically we test
closure membership through `R_D`. All 66 stored rays outside `cl(D3)` from the
first runs (Section 2.9) have a blocked vertex (`check_nond3_blocked.py`).

**Lemma 2.9 (three zero edges at a vertex; proved).** If `p in P3` vanishes at
interior points `a_i e_i` of the three edges at the origin and `p(0) > 0`, then
`p = p(0) [ (1 - sum_i x_i/a_i)^2 + 2 sum_{i<j} r_ij x_i x_j/(a_i a_j) ]` with
`r_ij >= 0`. In particular `p in D3^quad`, and `p` is extreme only if it is an
affine square.

*Proof.* On edge `i` the restriction is a nonnegative quadratic with an
interior zero and positive value at the origin, so it equals
`p(0)(1 - t/a_i)^2`. This fixes the constant, linear and square coefficients;
the cross coefficients are free, which gives the displayed form with some real
`r_ij`. Evaluating at `(a_i e_i + a_j e_j)/2` gives `p(0) r_ij/2 >= 0`. ∎

### 2.6 Extreme rays of the family beyond the five-contact regime

In the five-contact regime `0 < h < min(d_1, d_2)`, `k > 0`, `d_3 > D + k`,
the family member has the edge contacts `a = (h/d_1, 0, 0)`,
`b = (0, h/d_2, 0)`, `c = (1, 0, (d_1-h)/d_3)`, `d = (0, 1, (d_2-h)/d_3)`,
`e = (1, 1, (D+k)/d_3)`, and spans an exposed ray (2026-09-25 note). The searches
of this note found family members on five boundary strata (Section 2.8):

| Stratum | Parameters (`k > 0` throughout) | Zeros and tangencies |
| --- | --- | --- |
| S1 | `0 < h < min(d_1,d_2)`, `d_3 = D + k` | `a, b, c, d`; vertex `(1,1,1)`, tangent along `z` |
| S2 | `h = 0`, `d_3 > d_1 + d_2 + k` | vertex `0`, tangent along `x` and `y`; `c, d, e` |
| S3 | `h = d_1 < d_2`, `d_3 > d_2 + k` | vertex `(1,0,0)`, tangent along `x` and `z`; `b, d, e` |
| S4 | `h = 0`, `d_3 = d_1 + d_2 + k` | vertex `0` as in S2; `c, d`; vertex `(1,1,1)` as in S1 |
| S5 | `h = d_1 < d_2`, `d_3 = d_2 + k` | vertex `(1,0,0)` as in S3; `b, d`; vertex `(1,1,1)` as in S1 |

(S3 with `d_1` and `d_2` exchanged is the image under `x <-> y`.) Here
`d_1, d_2 >= 0`, as in the family definition. On S2/S4, `d_1 = 0` makes `c`
the vertex `(1,0,0)`, and `d_2 = 0` makes `d` the vertex `(0,1,0)`, in each
case with a `z` tangency. On S3/S5, `h = d_1 = 0` makes `b` the origin,
with a `y` tangency. These cases are included. Their zero sets contain whole
cube edges: at `h = 0`, `q(x,0,0) = d_1^2 x^2` and
`q(0,y,0) = d_2^2 y^2`, so `d_1 = 0` or `d_2 = 0` on S2/S4, or
`h = d_1 = 0` on S3/S5, gives a zero edge. These members lie outside the
isolated-point-contact enumeration of Section 2.8 and inside `cl(D3^quad)`
by Corollary 2.4 (ii); the extremality proof below does not require isolated
zeros.

**Proposition 2.10 (proved; exact symbolic computation).** On each stratum
S1-S5, for all parameters in the stated range, `q_{h,d,k}` spans an extreme ray
of `P3` (and of `P3+`).

*Proof.* Nonnegativity is the family identity. The listed contact conditions
are linear in the ten coefficients: the value at each zero, the edge derivative
at each interior edge contact, and the derivative along each listed tangent
edge at a vertex zero. The scripts `check_boundary_rank_symbolic.py` (S1) and
`check_family_strata_symbolic.py` (S2-S5) verify symbolically that `q` satisfies
them and that the system has rank 9 on the whole stratum: for S1 the 9 x 9
minor `h^2 (d_1 - 2h)(d_2 - h)^2 / (d_1 d_2^2 d_3^2)` is nonzero off `d_1 = 2h`,
and on `d_1 = 2h` the minor `h^2 (d_2-h)^2 / (4 d_2^2 (d_2 + h + k)^2)` is
nonzero; for S2 and S4 a minor equals `2k/d_3`, including when `d_1` or `d_2`
is zero. For S3 and S5 with `d_1 > 0`, a minor equals
`d_1^2 (d_1 - d_2)^2 / (d_2^2 d_3^2)`. At `h = d_1 = 0`, a minor instead
equals `-2k/d_3` (`-2k/(d_2+k)` on S5), which is nonzero. The extended
symbolic check records these cases in
`logs/check_family_strata_symbolic_r1_revision.txt`.
Now let `q = q_1 + q_2` with `q_i in P3`.
Both vanish at every zero of `q`; at an interior edge contact each has an
interior minimum on the edge, so its edge derivative vanishes; along a tangent
edge at a vertex zero each restriction is nonnegative with a zero at the vertex,
so its one-sided derivative into the edge is at least zero, and the two
derivatives sum to zero, so both vanish. This one-sided argument also handles
the contacts `b`, `c` or `d` that reach a vertex at a zero parameter.
Thus `q_1, q_2` lie in the
one-dimensional kernel. ∎

Without the tangency equation at `(1,1,1)`, the S1 contact system has rank 8, so
the vertex zero alone does not determine the ray. Whether these rays are
exposed was not checked. All 30 stored boundary examples of Section 2.8 lie
outside `cl(D3)` numerically: their values over `R_D` range from `-9.4e-6` to
`-1.7e-3` (unrounded endpoints `-9.3669165969478829e-6` and
`-0.0017388270667593464`). This does not cover every member of the stated
strata: members with some `d_i = 0` have a zero square coefficient and lie in
`cl(D3^quad)` by Corollary 2.4 (ii). All these rays are family members, so they
do not bear on Conjecture 2.11; they matter because
the searches find them and must be able to recognize them.

### 2.7 Minimal blocking configurations and special positions

Throughout this note, a *family fit cost* (called a "residual" in the fit
logs) is the `least_squares` cost `c = 0.5 ||v_hat - p_hat||_2^2`, where
`v_hat = v/||v||_2`, `p_hat = p/||p||_2`, and `v` is the fitted family
coefficient vector. It is half a squared Euclidean distance; the distance to
the fitted member is `sqrt(2c)`. These local fits do not certify the distance
to the entire family. The position search instead uses the squared contact
residual `||A(theta) p||_2^2`, with the normalization imposed by its inner SDP.

A *zero configuration* lists faces of the cube carrying a zero of `p`, with
the free coordinates of each zero generic in `(0,1)`. With positive square
coefficients and `p(0) > 0` the following are necessary: the origin is not a
zero; no two zeros lie on a common axis-parallel line (the restriction to that
line is strictly convex); and a facet with an interior zero carries no two
further generic zeros (the restriction to the facet is a positive semidefinite
form centered at the interior zero, whose zero set is a point or a line).

We enumerated all configurations of at most four point zeros satisfying these
conditions, up to the coordinate permutations fixing the origin, and tested
blocking at the origin at random generic positions (two independent draws must
both block). There are 312 subset-minimal blocking configurations; the count
was obtained with floating-point rank tests (`blocking2.py`) and confirmed in
exact rational arithmetic (`blocking_exact.py`, computed exactly at random
rational positions). Every blocked zero set of this kind contains one of them.
For each one we asked whether the face `F(B)` of `P3+` (quadratics vanishing at
the configuration, with zero face derivatives at relative-interior zeros)
contains an element with `p(0) > 0`:

- At random generic positions (4 draws each), only six configurations have a
  nonempty face (normalized `p(0)` above `1e-3`; all others below `4e-7` or
  infeasible): one sub-pattern of the family's contact pattern (F4), and five
  others (C1, C2, C3, C5, C6), four of which contain a vertex zero. Their faces
  were sampled (192 extreme rays, `explore_config.py`): all lie in the dual of
  `R`; the 11 outside `cl(D3)` fit family members to fit cost below `1e-15`
  (`fit_all.py`), 9 on stratum S1 and 2 in the five-contact regime.
- A local search over positions for all 312 configurations (Nelder-Mead from
  three starts, `blocking_positions.py`) minimized the distance of the contact
  conditions from the face with `p(0) >= 0.01`. For 265 configurations the
  search reached squared contact residual `<= 1e-6`, and all 265 were
  post-processed. On re-solving the inner SDP, 264 passed the strict
  `< 1e-6` cutoff. The excluded configuration
  `((-1,-1,0), (-1,0,-1), (-1,0,0), (-1,1,1))` had stored search cost
  `1.48e-9` but retest cost `2.535309231191649e-6`; it produced no tested
  quadratic. The retest read positions rounded to four decimal places from
  the search's text logs, while its JSON logs retain full precision; rerunning
  the reviewer's independent inner SDP gives cost `9.212e-10` at the
  full-precision positions and `2.535e-6` at the rounded positions
  (`logs/check_rounded_theta_r2_revision.txt`), explaining the exclusion.
  The 264 retested valid quadratics (`positions_retest.py`)
  all lie in the dual of `R` (smallest value `6.9e-9`),
  and 8 lie outside `cl(D3)`. Imposing exact contacts at the rounded positions
  returned a value for only 24 of the 265 configurations: 19 at or below
  `p(0) = 1e-4` and 5 above. The other 241 solves returned no value; the main
  log has 224 Clarabel panic messages and 229 records without a value among
  its 241 records (`logs/postprocess_positions.txt`). Missing values are not
  evidence of infeasibility. Among the 24 configurations with a returned
  value, only two outside the six generically nonempty configurations admit
  `p(0) > 1e-4`. In both cases the maximizer of `p(0)` is an affine square
  (rank-one homogenized matrix) whose zero plane contains all prescribed
  zeros, so it lies in `D3` and blocking fails at those positions
  (`special_config_check.py`). The conclusion that no valid quadratic was
  found outside the dual of `R` rests on the 264 direct retests, all with
  returned relaxation values, rather than on this incomplete exact-contact
  check.

The 8 valid quadratics outside `cl(D3)` from `positions_retest.py` fit single
family members only to fit costs between `3e-7` and `4e-3` (`fit_more.py`),
or distances of about `8e-4` to `0.09` between unit coefficient vectors.
They are not extreme rays: the search minimizes the squared contact residual
over the face, so its minimizers are typically relative-interior points of
faces. All 8 lie in
the dual of `R`, so numerically they are sums of elements of `cl(D3^quad)` and
family members.

### 2.8 Systematic enumeration of point-contact strata

The samplers above draw rays at random. As a systematic complement,
`stratum_enum.py` enumerates every combinatorial type of point zero
configuration that can determine an extreme ray. A zero of type `(s, T)` sits
on the face `s` (a vertex, an edge or a facet) at a generic point; `T` is a set
of fixed coordinates in which the first derivative also vanishes (a tangential
contact; facet zeros get no tangency, since that forces a convex quadratic). It
imposes `1 + (number of free coordinates) + |T|` linear conditions. We
enumerated all sets of zero types, one per face, with

- 9 conditions in total (*generic strata*: the conditions determine `p` up to
  scale at generic positions), or
- 10 conditions (*determinantal strata*: one position coordinate is solved from
  the determinant condition, the others are random),

subject to the necessary conditions of Section 2.7, and reduced them modulo the
48 cube symmetries: 2,146 generic and 4,272 determinantal types. For each type
and each random sample of positions we computed the kernel (rank 9 required),
kept `+-p` when it is nonnegative on the cube, and tested every nonnegative
`p` with positive square coefficients and indefinite Hessian against `R_D` and,
when outside `cl(D3)`, against `R`. Untested nonnegative kernels also include
those with a negative square coefficient, which are outside `P3+` and do not
affect Conjecture 2.11. Within `P3+`, the other kernels are convex or have a
zero square coefficient (up to the numerical thresholds); these cases lie in
`cl(D3^quad)` by Corollary 2.4.

| Run | Samples per type (generic / determinantal) | Kernels | Nonnegative | Tested | Outside `cl(D3)` | Outside dual of `R` |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `stratum_enum.py` (3 parts) | 60 / 40 | 218,352 | 91,719 | 417 | 95 | 0 |
| `stratum_enum.py` dense (4 shards, forward and reverse) | 500 / 800 | 3,133,560 | 1,304,623 | 6,654 | 923 | 0 |

In both runs the rays outside `cl(D3)` come from the same six types: the
five-edge family stratum, S1, and the vertex-merged strata S2-S5 (in
transformed coordinates). All 34 stored examples (16 and 18) fit family members
to fit cost below `1e-28` (`fit_stratum_examples.py`). The smallest value over
`R` was `-2.1e-9` in the first run and `-7.0e-9` in the dense run. The ray
behind `-7.0e-9` was not stored and was not re-solved. Five stored rays with
original `R` values from `-1.37e-10` to `1.04e-11` were re-solved
(`logs/check_min_rR_dense.txt`): the new values range from `-4.91e-8` to
`1.65e-10`, and some change sign between Clarabel at tight tolerance and SCS.
This supports a solver-noise interpretation for values near zero, but does
not verify the particular `-7.0e-9` ray. No nonnegative
kernel with negative product of cross coefficients appeared; this
matches the submodular sampler, where only 1 of 3,998 boundary rays had all
cross coefficients strictly negative, positive squares and an indefinite
Hessian (that class is covered by Theorem 2.5 anyway).

The enumeration covers isolated point contacts only. It misses zero segments
inside facets, contacts of higher order than first-derivative tangency, and
strata that need two or more position constraints. It is also thin on
determinantal strata: on the family's own five-edge stratum only 1 of 27
kernels was nonnegative in the first run, which is why the dense run was made
(49 of 511 there).

### 2.9 Numerical evidence and its calibration

All searches use `cvxpy` 1.9.3 with Clarabel. Membership of a valid quadratic
`p` in the dual of `R` is tested by `min {p(y) : y in R}`, and membership in
`cl(D3^quad)` by the same with `R_D`. Validity and separation use the exact
description of `P3` by the six order simplices, each with `COP_4 = PSD_4 +
NN_4` (Anstreicher-Burer, Theorem 7). Quadratics are normalized to maximum
coefficient 1 (or `p(u) = 1` for the uniform moments `u`). A ray is counted as
outside `cl(D3)` or missing if its value is below `-1e-6` (`-1e-7` in the
configuration runs).

| Sampler | Script (arguments) | Rays | Outside `cl(D3)` | Missing |
| --- | --- | ---: | ---: | ---: |
| Random Gaussian moment directions | `explore_random.py 1 300 gauss` | 300 | 0 | 0 |
| Separation of moment points from atoms partly outside the cube | `explore_psd.py` (seeds 1, 11, 12, 13) | 7,798 | 55 | 0 |
| Extreme rays of faces with random contact configurations | `face_explore_generic.py` (seeds 21, 22) | 13,582 | 10 | 0 |
| Faces of monotone-path contacts | `face_explore.py 1 40 3` | 120 | 7 | 0 |
| Faces of family contacts with one or two contacts dropped | `family_neighborhood.py` (`1 40 2 1`, `41 600 5 2`) | 3,080 | 253 | 0 |
| Faces of the six generically nonempty blocking configurations | `explore_config.py` | 192 | 11 | 0 |
| Boundary rays of the supermodular part | `signclass.py 2 4000 sup` | 3,991 | 9 | 0 |
| Point-contact strata, first run | `stratum_enum.py` | 417 | 95 | 0 |
| Valid quadratics at searched special positions | `positions_retest.py` | 264 | 8 | 0 |
| Point-contact strata, dense run | `stratum_enum.py` (500 / 800 samples) | 6,654 | 923 | 0 |
| Central optimal points of `R` for family members, separated | `face_probe.py 1 60 family` | 60 points | - | 0 |
| Projections onto `R` of `R_D`-points outside `H3+` | `project_probe.py 33 300 l2 0.0` | 300 points | - | 0 |
| Projections onto `R` from perturbed-objective minimizers in `R_D` (mostly already in `H3+`) | `project_probe.py 34 300 l1 0.03` | 300 points | - | 0 |
| Alternating ascent | `ascent.py 1 40 family` | 40 starts | - | 0 |

The control run `signclass.py 1 4000 sub` (3,998 boundary rays of the
submodular part) found no ray outside `cl(D3)`, as Theorem 2.5 predicts.
Every extreme ray outside `cl(D3)` that was fitted is a family member: the 66
rays of the first runs (`fit_all.py`, max fit cost `3.1e-14`), the 9 rays of the
supermodular sampler (`fit_more.py`, five-contact regime, fit cost below
`1e-16`) and the stored stratum examples (Section 2.8). On
the `explore_psd` runs, where all values were stored, the smallest value over
`R` was `-2.3e-9`, against `-2.6e-3` over `R_D`; over all runs the smallest
value over `R` was `-7.0e-9`. The alternating ascent is weak: from a
point of `H3+` it stalls at value zero after one step, so its negative result
carries little weight; a second ascent run without the family LMIs stopped on
a solver error. The `l1 0.03` projection run also carries little weight:
every logged progress line has `sep(y0)` near `+1e-8`, so those starting
points are already in `H3+` within solver accuracy. The `l2 0.0` run has
logged starting separations near `-1e-3` to `-8e-3` and tests projections
from outside `H3+`.

*Calibration (heuristic).* The same samplers detect the known gap of `D3` at
rates between 0.07% (random contact faces) and 8% (family neighborhoods),
1.2% over the random samplers, and 14% of the rays tested in the stratum
enumeration. If another family of missing rays had a "size" comparable to the
family that `D3` misses, one would expect dozens of detections among the rays
tested against `R`; there were none. This argument is only heuristic: a
missing family with much smaller normal cones, or living on strata the
samplers do not reach (zero segments, higher-order contacts), could be missed.
Random objective comparisons are weak evidence here: the 2026-09-25 runs found
no `D3` gap in 21,000 random instances although `D3` is incomplete, which is
why the samplers above target extreme rays and faces.

### 2.10 Conjecture and what is missing for a proof

**Conjecture 2.11.** `P3+ = cl(D3^quad) + sum_{g} cl cone(gF)`. Equivalently,
`H3+ = R`, and (by Proposition 2.2 and Corollary 2.4 (iv))
`QPB_3 = K3 = R cap {Y_ii <= x_i}`. A point of `R` outside `H3+` must satisfy
`Y_ii < m_i` for all `i`. By Corollary 2.6 it suffices
to prove that every extreme ray of `P3` with all cross coefficients positive,
positive square coefficients and indefinite Hessian lies in `cl(D3^quad)` or is
a limit of members of one of the six copies listed there.

Status: conjecture, supported by the numerical evidence of Sections 2.7-2.9.
Its stable identifier is **Conjecture 2.11**; references to Conjecture 2.9 in
earlier versions or in the sibling `three-var-computation/note.md` refer to
this same conjecture. Existing statement numbers will be kept in future
revisions; additional results will use labels that do not renumber them.
Two routes to a proof suggest themselves.

1. Adapt the rank-and-active-set argument of BNW (their Lemma 1 and
   Propositions 3-5) to `R` and supermodular objectives. Their relaxation fails
   on supermodular objectives (1,102 of 3,991 sampled rays), so the family LMIs
   would have to replace the RLT upper bounds in that argument. One step
   carries over directly (proved): every point of `R cap {Y_ii <= x_i}` whose
   moment matrix `[[1, x^T],[x, X]]` has rank at most 2 lies in `K3`. Indeed
   `X - x x^T = w w^T`; complementing the coordinates with `w_i < 0` (which maps
   `R cap {Y_ii <= x_i}` to itself and flips the signs of those `w_i`) gives
   `X >= x x^T` entrywise, and BNW's Lemma 4 (an elementary rotation argument)
   shows that such a rank-2 point satisfying `X <= x e^T` is a mixture of cube
   atoms. So a point of `R cap {Y_ii <= x_i}` outside the hull has moment
   rank 3 or 4.
2. Classify the extreme rays of `P3` with all cross coefficients positive by
   zero configuration, using the elimination of one coordinate (for a
   supermodular `q`, the minimizing `z` is a monotone function of `(x, y)`), and
   show that every stratum outside `cl(D3)` is a family stratum. Section 2.8
   is a numerical version of this for point contacts.

## 3. Comparison with the earlier notes (part a)

- The [family note](../../research-20260925/three-positive-family-sdp.md) stated
  that completeness of the symmetry copies was not established. That remains
  true. This note adds that the literal question needs the three caps, that the
  copies are needed only in one sign class (Theorem 2.5), and that no
  counterexample was found.
- The [counterexample note](../../research-20260925/three-positive-disjoint-counterexample.md)
  proves exposedness only on the open five-contact region. Proposition 2.10
  adds five boundary strata of extreme rays (exposedness not checked).
  Lemma 2.8 generalizes its exclusion argument.
- The [exploration note](../../research-20260925/three-positive-exploration.md),
  Section 6, reports 21,000 random instances "with strictly positive diagonals
  and positive cross coefficients" without a `D3` gap. Those instances are in
  the supermodular class, the only class where gaps can occur (Corollary 2.6),
  so the negative result there reflects the small size of the gap region, not
  the sign class.

## 4. Part (b): four positive variables

### 4.1 Tools

A *spectrahedral shadow* is a linear image of a spectrahedron. Equivalently,
the set has a finite SDP extended formulation (finite SDP lift). We use:

- (S1) Shadows are closed under intersections, linear preimages and dual cones
  (Nishijima, arXiv:2602.23725v3, Lemma 2.4 (i)-(iii), citing
  Netzer-Plaumann, *Geometry of Linear Matrix Inequalities*, Birkhauser 2023,
  Theorem 3.5; for duals of closed cones also BKT, Remark 3.17, citing Nie).
  Closure under linear images follows from the definition. Minkowski sums
  are linear images of products of shadows; products have block-diagonal
  SDP lifts. Exposed faces are intersections with supporting hyperplanes.
- (S2) Bodirsky-Kummer-Thom (BKT), Lemma 2.3: on a real closed field
  `R' >= R`, a map `L : R' -> R'` preserves every set defined by a linear matrix
  inequality with real coefficients if and only if `L` is unital, `R`-linear
  and completely positive. By Tarski transfer, if `S subseteq R^m` is a
  shadow, the same formula defines `S(R')`, and such an `L` maps `S(R')` into
  itself coordinatewise.
- (S3) BKT, Theorem 2.13(1): if `f` maps a divisible ordered abelian group
  `Lambda` to a real closed field `R'` and is positive definite (the matrices
  `(f(a_i + a_j))` are positive definite for distinct `a_i`), then
  `L_f(sum c_a eps^a) = sum f(a) c_a eps^a` is completely positive on the Hahn
  field `R'[[eps^Lambda]]`.
- (S4) BKT, Example 3.4, Remark 3.2, Theorem 3.7 and the proof of
  Proposition 3.11: for the Horn matrix `H` there are a real closed field
  `R' >= R` and a positive definite `f : Q^5 -> R'` with `f(0) = 1` and
  `sum_{i,j} H_ij f(2e_i + 2e_j) < 0` (namely `f(w) = T(eps^w)/T(1)` for a
  functional `T` that is positive on nonzero squares in `R'[Q^5]` and negative on
  `h(x_1^2, ..., x_5^2)`, which is not a sum of squares in `R[Q^5]`).

We order `Q^5` lexicographically with the first coordinate most significant.
Then `eps^a` is a positive infinitesimal whenever the first nonzero coordinate
of `a` is positive. We read the statements we use in the BKT text; we did not
re-check their proofs.

### 4.2 The four-dimensional box

**Theorem 4.2 (proved).** Let `n >= 4`. The cone `P_n` of quadratics
nonnegative on `[0,1]^n` and its subcone `P_n^+` with nonnegative square
coefficients are not spectrahedral shadows. Consequently
`QPB_n = conv{(x, xx^T) : x in [0,1]^n}` and `H_n^+` have no finite SDP lift.
For `n <= 3` both are shadows (Anstreicher-Burer), so four is the threshold.

*Proof.* First let `n = 4`. Take `R'` and `f` from (S4) and put
`H' = R'[[eps^{Q^5}]]`, which is real closed. Define the quadratic

```
q(x_1, ..., x_4) = sum_{i,j=1}^{5} H_ij (eps^{2e_i} u_i)(eps^{2e_j} u_j),
u_1 = 1,  u_{k+1} = x_k.
```

Each coefficient of `q` is a real number times a single monomial `eps^a`, its
square coefficients are positive, and for `x >= 0` the vector
`(eps^{2e_i} u_i)_i` is nonnegative. The Horn matrix is copositive over `R`,
hence over `H'` by Tarski transfer, so `q >= 0` on `[0,1]^4` over `H'`, that is
`q in P_4^+(H')`.

Apply `L_f` to the coefficients. At `xi_k = eps^{2e_1 - 2e_{k+1}}` (positive
infinitesimals, so `xi in [0,1]^4`) every term of `L_f(q)(xi)` equals
`H_ij f(2e_i + 2e_j) eps^{4e_1}`, hence

```
L_f(q)(xi) = eps^{4 e_1} sum_{i,j} H_ij f(2e_i + 2e_j) < 0.
```

So `L_f(q)` is not in `P_4(H')`. But `L_f` is unital, `R`-linear and
completely positive by (S3), so if `P_4` or `P_4^+` were a shadow, (S2) would
give `L_f(q) in P_4^+(H') subseteq P_4(H')`. This contradiction proves the
statement for `n = 4`. For `n > 4`, the quadratics that depend only on
`x_1, ..., x_4` form a linear section of `P_n` (and of `P_n^+`) equal to
`P_4` (respectively `P_4^+`), and sections of shadows are shadows. If `QPB_n`
or `H_n^+` were a shadow, the dual cone of `{1} x QPB_n` (respectively
`{1} x H_n^+`), which is `P_n` (respectively `P_n^+`), would be a shadow by
(S1). ∎

The bookkeeping in this proof (single monomial coefficients, position of
`xi`, and the evaluation identity) is checked by
`code/check_apex_bookkeeping.py`. In words: near a vertex the cube looks like
an orthant, the constant coordinate acts as a fifth copositive variable, and
the BKT witness for `COP_5` can be placed in an infinitesimal neighborhood of
that vertex by choosing the order of the value group.

### 4.3 Polyhedral cones and polytopes

**Theorem 4.4 (proved).** Let `K subseteq R^m`, `m >= 5`, be a closed convex
semialgebraic cone, and suppose there is a linear map
`ell = (ell_1, ..., ell_5) : R^m -> R^5` with `ell(K) subseteq R^5_+` and
`ell(K) contains {u in R^5_+ : u_k <= delta u_1, k = 2..5}` for some real
`delta > 0`. Then the cone `COP(K)` of quadratic forms nonnegative on `K` is not
a spectrahedral shadow, and neither is its dual `CP(K) = cl conv{z z^T : z in K}`.
The hypothesis holds for every pointed polyhedral cone of dimension `m >= 5`
with a simple extreme ray (an extreme ray lying in exactly `m - 1` facets).
Hence for every polytope `X subseteq R^n` of dimension `n >= 4` with a simple
vertex, the cone of quadratics nonnegative on `X` and the moment hull
`conv{(x, xx^T) : x in X}` are not spectrahedral shadows.

*Proof.* With `R'`, `f`, `H'` as in Theorem 4.2, let
`M(z) = sum_{i,j} H_ij eps^{2e_i + 2e_j} ell_i(z) ell_j(z)`. It is nonnegative
on `K(H')` because `ell(z) >= 0` there and `H` is copositive. Written in the
monomial basis, each coefficient of `M` is a finite sum of real multiples of
monomials `eps^a`, so by `R`-linearity
`L_f(M)(z) = sum_{i,j} H_ij f(2e_i+2e_j) eps^{2e_i+2e_j} ell_i(z) ell_j(z)`.
The point `u = (1, eps^{2e_1 - 2e_2}, ..., eps^{2e_1 - 2e_5})` satisfies
`u_k <= delta u_1`; the inclusion hypothesis is a first-order statement with real
parameters, so it transfers to `H'`, and some `w in K(H')` has `ell(w) = u`.
Then `L_f(M)(w) = eps^{4e_1} sum H_ij f(2e_i + 2e_j) < 0`, and (S2), (S3) give
the contradiction as before; `CP(K)` follows by (S1).
For a pointed polyhedral cone with a simple extreme ray `r`, let `ell_2, ...,
ell_m` be inner facet normals of the `m-1` facets through `r` (linearly
independent) and `ell_1` a linear form positive on `K \ {0}`; then
`(ell_1, ..., ell_m)` is a basis. For `u` as in the hypothesis, the point `z`
with `ell_1(z) = u_1`, `ell_k(z) = u_k` (`k = 2..5`) and `ell_k(z) = 0`
(`k > 5`) is close to the ray `r` when `delta` is small, so it satisfies the
remaining facet inequalities (which are strict on `r`) and lies in `K`. For a
polytope `X`, apply this to `K = cl cone({1} x X)`, whose extreme ray through
`(1, v)` is simple when the vertex `v` is simple. ∎

This contains BKT's result for `COP_n`, `n >= 5` (`K = R^n_+`) and Theorem 4.2
(every vertex of the cube is simple). It does not cover polytopes without a
simple vertex, such as the four-dimensional cross-polytope.

**Remark 4.5 (why a face argument cannot work; proved).** Every face of
`QPB_4` is a spectrahedral shadow. An exposed face has the form
`conv{(x, xx^T) : x in Z}`, where `Z` is the zero set on the cube of a nonzero
nonnegative quadratic `p`. On the relative interior of a face of the cube that
contains a zero, `p` is a positive semidefinite form centered at that zero, so
`Z` is a finite union of polytopes of dimension at most three. The moment hull
of each of them is an affine image of the moment hull of a polytope in `R^3`,
which is a shadow by the Anstreicher-Burer triangulation, and the convex hull
of finitely many compact shadows is a shadow (Helton-Nie; Netzer-Sinn). Every
face is reached from `QPB_4` by finitely many steps of taking exposed faces,
and exposed faces of shadows are shadows. So the face-and-projection method
that proved the `K_5`-minor theorem cannot detect the obstruction of Theorem
4.2; the completely positive maps act on all coordinates at once.

### 4.4 Graphs with a `K_4` minor

Use the setting of the [2026-09-25 exploration](../../research-20260925/three-positive-exploration.md):
`G = (V, E, L+, L-)`, `P` the positive-loop vertices, `H(G) = K(G) + D` the
joint hull with signed diagonal slack.

**Theorem 4.6 (proved).** If `G[P]` contains a `K_4` minor, then `H(G)` is not a
spectrahedral shadow. Extra vertices, edges and negative loops are allowed.

*Proof.* Choose disjoint connected branch sets `C_1, ..., C_4 subseteq P`, a
spanning tree of each, and one edge `e_ab` between each pair. The affine
function `F = sum over tree edges ij of (Y_ii + Y_jj - 2Y_ij)` is nonnegative
on `H(G)`, since at a generating point it equals `sum (x_i - x_j)^2` plus
diagonal slacks. On the exposed face `F = 0`, every atom is constant on each
branch set, and the slack vanishes on branch sets with at least two vertices.
Project the face onto `u_a = x_{r_a}` (a representative `r_a in C_a`),
`Z_aa = Y_{r_a r_a}` and `Z_ab = Y_{e_ab}`. The image is `QPB_4 + D_S`, where
`D_S` is diagonal slack on the singleton branch sets. Every `u in [0,1]^4`
is attained: give `C_a` the value `u_a`, all other vertices the value 0, and set
diagonal coordinates to squares. If `H(G)` were a shadow, so would be the
face, its projection `QPB_4 + D_S`, and then `QPB_4 + D_S + D_{S^c} = H_4^+`,
contradicting Theorem 4.2. ∎

This supersedes Theorem 3 of the 2026-09-25 exploration (`K_5` minor). In
particular every positive graph that contains `K_4` as a subgraph, or any
subdivision of `K_4` (for example a long cycle with two crossing chords), has
no finite SDP lift. Khajavirad (12 February 2026 version, end of Section 5)
proposes to relax the assumption `|V_c| <= 2` on positive components to
`|V_c| <= k` for a fixed `k`. Theorem 4.6 shows that this cannot hold for
`k >= 4` without further restrictions on the graph. For `k = 3` finite lifts
exist (Proposition 1 of the 2026-09-25 exploration).

### 4.5 Minor closure and the apex lemma

Work with all-positive graphs (`V = P`); write `H(G)` for the hull.

**Proposition 4.7 (proved).** If `H(G)` is a shadow and `G'` is a minor of
`G`, then `H(G')` is a shadow.

*Proof.* Deleting an edge or a vertex is a coordinate projection. Contracting
the edge `ij` is the face `Y_ii + Y_jj - 2Y_ij = 0`, followed by the projection
that identifies `i` and `j` (keeping one of `Y_ik`, `Y_jk` for each neighbor
`k`) and by Minkowski addition of diagonal slack at the merged vertex, exactly
as in Theorem 4.6. ∎

**Lemma 4.8 (apex lemma; proved).** Let `G` have vertex set `{1, ..., n}` and
let `G*` be `G` plus a vertex `0` joined to every vertex. If the cone `COP(G*)`
of copositive `(n+1) x (n+1)` matrices whose off-diagonal support lies in the
edges of `G*` is not a spectrahedral shadow, then `H(G)` is not a shadow.

*Proof.* `COP(G*)` is identified with the nonnegative polynomials
`m(x_0^2, ..., x_n^2)` of support `2S` (BKT, Remark 3.16). By BKT Theorem 3.15,
if it is not a shadow, there are a real closed field `R`, a matrix
`M in COP(G*)(R)`, and `p = m(x^2)` such that `p(x^d)` is a sum of squares for
no `d`. By their Remark 3.2, `p` is then not a sum of squares in `R[Q^{n+1}]`.
Theorem 3.7 then gives `R' >= R` and `T` with `T(a^2) > 0` for `a != 0` and
`T(p) < 0`; put `f(w) = T(eps^w)/T(1)`. The quadratic
`q = sum_{i,j} M_ij (eps^{2e_i} u_i)(eps^{2e_j} u_j)` (with `u_0 = 1`, the apex
coordinate first in the order) has only monomials allowed by `G`, nonnegative
square coefficients (the diagonal of a copositive matrix is nonnegative), and
is nonnegative on the cube. The proof of Theorem 4.2 gives `L_f(q)(xi) < 0`.
Since the dual cone of `{1} x H(G)` is the cone of allowed quadratics
nonnegative on the cube with nonnegative square coefficients, (S1) and (S2)
give the claim. ∎

For `G = K_4`, `G* = K_5` and `COP(K_5) = COP_5`, which recovers
Theorem 4.2.

### 4.6 Small graphs

Every connected graph with at least four vertices contains `P_4` or
`K_{1,3}` as a subgraph. With Proposition 4.7 and Proposition 1 of 2026-09-25
(components of at most three vertices have finite lifts), this gives:

- if `H(P_4)` and `H(K_{1,3})` both lack finite lifts, then `H(G)` has a finite
  lift exactly when every positive component has at most three vertices;
- otherwise some graph with a four-vertex component has a finite lift, and
  the forbidden-minor list contains `K_4` together with series-parallel
  graphs to be determined.

The connected graphs on four vertices other than `K_4` (the diamond, `C_4`,
the paw, `P_4`, `K_{1,3}`) are all series-parallel; the first four contain
`P_4`. The apex patterns are

| `G` | `G*` | SPN? (Shaked-Monderer) | Apex lemma |
| --- | --- | --- | --- |
| `K_4` | `K_5` | no; `COP_5` is not a shadow (BKT) | no finite lift |
| diamond | `K_5 - e` | no (contains `F_5`, Thm 7.3) | open |
| `C_4` | wheel `W_4` | no (contains `F_5`) | open |
| paw | `K_5 -` (path of 2 edges) | no (contains `F_5`) | open |
| `P_4` | fan `F_5` | no (Lemma 7.1) | open |
| `K_{1,3}` | `T_5 = K_{1,1,3}` | yes (corrigendum, `T_5` SPN) | gives nothing |

For `K_{1,3}`, `COP(T_5)` equals the SPN matrices with that pattern, a shadow.
At non-vertex points of the cube the local cone is also a shadow: if `b >= 1`
coordinates are interior, eliminating them by a Schur complement leaves
copositivity of an `(5-b) x (5-b)` matrix, and `COP_k` is a shadow for
`k <= 4`. So the apex construction, which uses only the copositive cone at one
point of the cube, cannot decide `K_{1,3}`; a proof would need a quadratic whose
nonnegativity on the cube is a global property. For the other four the
question is whether a non-SPN copositive pattern is a shadow. To our knowledge
this is open: the BKT argument for the Horn matrix uses perfect-square
restrictions on the triangles of an odd cycle, which force contradictory sign
relations; in `G*` for a tree `G` the triangles through the apex form a disk,
and the corresponding relations are consistent (for the fan matrix `A` below,
the three perfect-square restrictions force the pure-power coefficients of
every square in a putative decomposition to be proportional to
`(1, 1, -1, -1, 1)`, with no contradiction).

**Remark 4.9 (trees reduce to the submodular part; proved).** If the positive
graph `T` is a forest, complementing coordinates can give every edge
coefficient either sign independently (root each tree and decide from the root
outward). So the cone of allowed cube-nonnegative quadratics with nonnegative
squares is the Minkowski sum of the complementation images of its submodular
part `S_-(T)` (edge coefficients `<= 0`), and `H(T)` has a finite lift if and
only if `S_-(T)` is a spectrahedral shadow. Since `S_-(T)` is a linear section
of the submodular part `S_-(K_4)` of `P_4^+`, a finite lift for `S_-(K_4)` would
give finite lifts for both `P_4` and `K_{1,3}` (and every forest on four
vertices). For `T = P_4` the BNW relaxation is not exact (their Example 4 has a
tridiagonal `Q`), and Zhang and Wang show that no SDP relaxation of the form
"Shor matrix plus finitely many linear cuts" is exact for submodular box QP when
`n >= 4`; neither result concerns extended formulations, so neither decides
shadow-ness.

### 4.7 A numerical probe of `COP(F_5)`

BKT Theorem 3.15 says `COP(F_5)` is a shadow if and only if some fixed `d`
makes `m(x_1^{2d}, ..., x_5^{2d})` a sum of squares for every `M` in it. We
tested Shaked-Monderer's non-SPN fan matrix

```
A = [[1,-1,1,0,0],[-1,1,-1,1,0],[1,-1,1,-1,1],[0,1,-1,1,-1],[0,0,1,-1,1]]
```

and the Horn matrix. For each we computed the smallest uniform shift `t` that
makes Gram matrices `G + tI` positive semidefinite in an SOS decomposition of
`m(x^{2d})`; `t > 0` means not SOS (`code/sos_subst.py`, parity
block-diagonalized):

| `d` | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| `A` (fan `F_5`) | `5.17e-2` | `6.37e-4` | `1.25e-5` | `1.83e-7` |
| Horn | `1.46e-1` | `4.54e-3` | `2.75e-4` | `8.63e-6` |

The Horn matrix is never SOS after substitution (BKT, Example 3.4); its
values stay positive but decrease by factors 16 to 32 per step. The values for
`A` are also positive but decrease faster (factors 50 to 80), and `1.8e-7` at
`d = 4` approaches solver accuracy. These data neither show that `A` fails for
every `d` nor that it eventually becomes SOS. The question remains open. A
`d = 5` run was not attempted: its value would be at the level of solver
accuracy and could not decide the question.

## 5. Prior work and novelty

- Anstreicher and Burer (2010), Theorem 7: exact DNN lift of `QPB_n` for
  `n <= 3` by triangulation; Theorem 2: Shor plus RLT is exact for `n = 2`. For
  `n = 4` the simplex pieces are `CP_5`, which is not a shadow. Theorem 4.2
  shows that no other construction can succeed either.
- Burer and Dong (2013), Corollaries 3-4: separation procedures for the
  homogeneous box cones in dimensions 4 and 5 (that is `n = 3, 4`). Separation
  does not give a finite lift, so there is no conflict with Theorem 4.2.
- Burer, Natarajan and Willemsen (arXiv:2504.03996, v3 of 31 August 2026):
  the relaxation `{Shor, X <= x e^T}` is tight for submodular box QP when
  `n <= 3` and not tight for `n = 4`. Theorem 2.5 transfers their result to the
  disjoint relaxation through the rounding map; it depends on their Theorem 1,
  whose proof we read (Propositions 3-5, Section 6) but did not check line by
  line. Zhang and Wang (arXiv:2609.03617v2) show that for `n >= 4` every SDP
  relaxation with finitely many linear cuts has a gap on some submodular
  instance; this is consistent with Theorem 4.2 and Remark 4.9 but does not
  imply them, since it concerns relaxations of a particular form.
- Bodirsky, Kummer and Thom (JEMS 2024): `COP_n`, `n >= 5`, is not a shadow.
  Nishijima (arXiv:2602.23725v3) extends this to symmetric cones of rank at
  least 5 using linear sections. Our homogenization makes the constant
  coordinate act as a fifth copositive variable at a vertex of the
  four-dimensional cube. All faces of `QPB_4` are shadows (Remark 4.5), and we
  know no linear section of `QPB_4` isomorphic to a known non-shadow, so the
  proof uses the completely positive maps directly.
- Shaked-Monderer (LAA 2016, and the corrigendum): SPN graphs on five
  vertices (exactly those not containing the fan `F_5`), and `T_5` is SPN.
- Khajavirad (2026): exact SDP formulations for positive components of size
  at most two; open three-variable question, answered negatively for her
  relaxation on 2026-09-25.

Searches on 2026-10-01 and 2026-10-02 ("spectrahedral shadow" with hypercube,
box, quadratic moment, polytope, copositive over polyhedral cone, sparsity
pattern, SPN, fan, and dimension four; "QPB" with "semidefinite extended
formulation") found no statement of Theorems 2.5, 4.2, 4.4 or 4.6. An
unsuccessful search does not establish novelty. Theorem 4.2 is a short
consequence of BKT once the homogenization is seen, and may be known to
specialists; Theorem 2.5 is a short consequence of BNW once Lemma 2.3 is seen.

## 6. Corrections to earlier notes and to the interrupted draft

Earlier notes:

- [Exploration, Section 4](../../research-20260925/three-positive-exploration.md):
  the `K_5`-minor obstruction holds with `K_4` (Theorem 4.6). The sentence
  "four-positive-variable components ... remain outside these sufficient
  conditions" is now false for components that contain a `K_4` minor; it
  stays true for series-parallel components.
- [Publication assessment](../../research-20260925/publication-quadratic-assessment.md),
  table row "Sparse obstruction to every finite SDP lift": `K_5` can be
  replaced by `K_4`, at the price of using the full BKT machinery (completely
  positive maps on real closed fields) instead of only their Corollary 3.18.
- [Counterexample note](../../research-20260925/three-positive-disjoint-counterexample.md):
  the exposed-ray theorem covers only the open five-contact region. On the
  boundary strata S1-S5 the family still gives extreme rays
  (Proposition 2.10); exposedness of these was not checked.
- [Family note](../../research-20260925/three-positive-family-sdp.md), Section 3:
  "No claim is made that all symmetry copies together describe the full
  quadratic hull" is still accurate. The caps `Y_ii <= x_i` must be added for
  the full hull (Proposition 2.2), only six copies matter for each supermodular
  sign pattern (Corollary 2.6), and completeness is now Conjecture 2.11.

The interrupted draft of this note (written 2026-10-02 before 04:30 UTC)
is not preserved. The historical corrections below describe the author's
account; draft-specific counts cannot be checked against that draft:

- Its summary said "about 29,000 rays", "380 rays outside `D3`" and
  "Five samplers". The author's reconstruction was 24,944 rays with 337
  outside `cl(D3)`, from nine samplers; these draft-specific totals cannot be
  checked from the surviving logs. The present totals (Section 2.9) are based
  on stored statistics and include the runs added on 2026-10-02.
- Three runs in its table had no surviving statistics (`face_explore.py`,
  `face_probe.py`, `family_neighborhood.py` with one contact dropped). They were
  rerun with logging. The first two reproduced the stated numbers (120 rays, 7
  outside `cl(D3)`; 60 points, none found); the third gave 37 rays outside
  `cl(D3)` among 80, not the 42 implied by the draft.
- The restart of the position search after a solver crash skipped 32 of the
  312 configurations (part 0 had finished 35, not 67, configurations; the line
  count included a traceback). The missing slice was run on 2026-10-02.
- The draft post-processing treated a solver failure as infeasibility. The
  position results are now based on `positions_retest.py`, which tests the
  valid quadratics found by the search directly.
- The draft justified "zero square coefficient implies `cl(D3)`" by citing
  Khajavirad's Theorems 4-5. Corollary 2.4 now proves it from Lemma 2.3 and the
  classical two-variable theorem of Anstreicher and Burer. The draft's
  statement "an extreme ray with positive semidefinite Hessian is an affine
  square" is replaced by Corollary 2.4 (iii) (every convex cube-nonnegative
  quadratic is in `D3^quad`).
- The draft proved extremality on the stratum `d_3 = D + k` only at four
  rational parameter points; Proposition 2.10 now covers the whole stratum and
  four more strata.
- The draft's Proposition 2.2 asserted "`P3 = S + caps` if and only if
  `P3+ = S`" and "`K3 = R cap caps` if and only if `H3+ = R`", but its proof
  gave only the direction from `P3+ = S`; the converse needs the fact that
  points of `R` outside `H3+` satisfy all caps strictly, which is now
  Corollary 2.4 (iv).

## Revision after review round 1

Revised on 2026-10-03 after the independent review's "minor fixes" verdict;
review round 2 confirmed all 12 fixes below. The conclusions of the proved
statements and their numbers are unchanged. Each numbered row corresponds to
an issue in `reviews/review-r1.md`.

| Issue | Change |
| --- | --- |
| 1. Zero parameters in Proposition 2.10 | Kept the full ranges. Added the S3/S5 minors `-2k/d_3` and `-2k/(d_2+k)` at `h = d_1 = 0`; explained the vertex tangencies on S2-S5. Extended `check_family_strata_symbolic.py` to check the family kernel and exact nonzero minors in all eight zero-parameter cases. Output: `logs/check_family_strata_symbolic_r1_revision.txt`. |
| 2. Boundary examples and `cl(D3)` | Limited the numerical claim to the 30 stored boundary examples; corrected the range to `-9.4e-6` through `-1.7e-3` and gave unrounded endpoints. Members with some `d_i = 0` lie in `cl(D3^quad)` by Corollary 2.4 (ii). |
| 3. Solver relevance | Restricted the objective sign test to three-variable box QPs; stated that larger or constrained models require the quadratic from the dual aggregate. |
| 4. Which hull | The Summary now says "outside `H3+`". |
| 5. Fit residuals | Defined the reported least-squares cost as half a squared distance between unit coefficient vectors; labeled the fit numbers as costs throughout. The eight retest fits have distances about `8e-4` through `0.09` to their fitted family members. |
| 6. Dense minimum | Stated in the Summary and Section 2.8 that the `-7.0e-9` ray was neither stored nor re-solved. Section 7 identifies the five re-solved stored rays and their original value range. Solver noise remains an interpretation, not a verified conclusion for that ray. |
| 7. Projection probe | Split the `l1` and `l2` table rows. The `l1 0.03` run mostly starts inside `H3+`; only the `l2 0.0` run supports the stated outside-hull projection experiment. |
| 8. Untested kernels | Added kernels with negative square coefficients, which are outside `P3+`; preserved the numerical threshold qualification. |
| 9. Position counts | Reconciled 265 original low-cost searches/post-processed configurations with 264 successful retests. Named the excluded configuration and its costs `1.48e-9` and `2.535309231191649e-6`; the latter exceeds the retest cutoff. |
| 10. Citation (S1) | Attributed intersections, preimages and dual cones to Nishijima's Lemma 2.4 (i)-(iii). Explained linear images, sums and exposed faces separately. |
| 11. Complementations | Corollary 2.6 now says "at most one coordinate". Exhaustively checked the four strict positive-product sign patterns. |
| 12. Interrupted draft counts | Stated that the draft is not preserved and its draft-specific counts cannot be checked from surviving logs; retained them only as the author's historical reconstruction. |
| Numbering | Kept Conjecture 2.11 and all existing statement numbers. Added an explicit mapping from the old Conjecture 2.9 references, including those in the sibling note, which is outside the edit scope. |
| Commit status | Replaced the outdated blanket status with an explicit statement that existing material was included in commits made outside this program and that this revision creates no commit. The out-of-scope `PROGRAM.md` is unchanged. |

The stored-data checks for issues 2, 5-7, 9 and 11 are reproducible with
`code/check_review_r1_reporting.py`; output is in
`logs/check_review_r1_reporting.txt`. This script audits existing data and
performs no new solves. The code and logs supplied by the reviewer are
unchanged. Review round 2 confirmed the added one-sided tangencies and exact
minors at zero parameters, the interpretation of costs, and the count
reconciliation. Completeness remains conjectural.

## Revision after review round 2

Revised on 2026-10-03 after the independent review's "minor fixes" verdict.
This revision has not been independently re-reviewed; its fixes were checked by the
coordinating agent. The proved statements are unchanged,
and all statement numbers, including Conjecture 2.11, are preserved.

| Issue | Change |
| --- | --- |
| N1. Exact-contact solve coverage | Limited the "only two" statement to the 24 configurations with returned values: 19 at or below `1e-4`, 5 above. Of 265 solves, 241 returned no value; the main log has 224 Clarabel panic messages and 229 missing values in 241 records. These failures do not establish infeasibility. The main numerical conclusion rests on the 264 direct retests, all with returned relaxation values. Corrected the Section 7 post-processing row. |
| N2. Rounded positions | Explained that the retest and exact-contact check read positions rounded to four decimals from the search's text logs. Reran the reviewer's independent inner SDP: the excluded configuration has cost `9.212e-10` at full precision and `2.535e-6` at rounded positions, reproducing the cause of its exclusion. |
| N3. S1 runtime | The 180-second timeout did not establish script failure. The reviewer completed the unchanged script in about 195 seconds; this revision reran it with `timeout 1200` and completed in 222.24 seconds (exit 0), reproducing both stated minors. |
| N4. Zero edges | Added the exact edge restrictions at `h = 0`, explaining the whole zero edges in the zero-parameter cases. These members lie outside the isolated-point-contact enumeration and in `cl(D3^quad)`; the extremality proof does not require isolated zeros. |

The reviewer files are unchanged. New verification outputs are in `logs/`;
the commands and outcomes are recorded below. Completeness remains conjectural.

## 7. Checks actually run

Unless stated otherwise, commands were run from
`/workspace/minlp-notes/research-20261001/three-var-completeness/code`
with the miniconda Python (cvxpy 1.9.3 with Clarabel, sympy, numpy, scipy),
with at most four processes at a time and an explicit `timeout` on every long
run started on 2026-10-02. Raw outputs are in `../logs`. No project-wide checks
were run and CI was not inspected. "Exact" means rational or symbolic
arithmetic; all SDP results are floating point.

Runs from 2026-10-01/02 (first author run; logs present):

| Command | Outcome |
| --- | --- |
| `python explore_random.py 1 300 gauss` | 300 rays, 0 outside `cl(D3)`, 0 missing |
| `python explore_psd.py 1 300 0.1`; `11 2500 0.05`; `12 2500 0.15`; `13 2500 0.3` | 300/2, 2499/15, 2499/20, 2500/18 (rays/outside `cl(D3)`); 0 missing; min value over `R` `-2.26e-9` |
| `python face_explore_generic.py 21 3000 3`; `22 2500 3` | 7,383 and 6,199 rays; 5 and 5 outside `cl(D3)`; 0 missing (statistics in the `.txt` logs) |
| `python family_neighborhood.py 41 600 5 2` | 3,000 rays, 216 outside `cl(D3)`, 0 missing |
| `python explore_config.py C1 8 4 1`, `C2 8 4 1`; `C3`, `C5`, `C6`, `F4` with `8 4 2` | 192 rays, 11 outside `cl(D3)` (threshold `1e-7`), 0 missing |
| `python blocking.py 4` | 341 minimal configurations under a weaker realizability filter (superseded) |
| `python blocking2.py 4 4` | 312 minimal blocking configurations; 6 with nonempty face at generic positions |
| `python blocking_positions.py ../logs/blocking2_k4.txt {0,1,2} 3 3` and restart `... 0 3 3 67 0b` | 280 configurations searched (part 0 crashed after 35; see Section 6) |
| `python fit_all.py` (the four `explore_psd` and four `explore_config` logs) | 66 rays outside `cl(D3)`; all fit family members, max fit cost `3.1e-14` (57 five-contact, 9 on S1) |
| `python project_probe.py 34 300 l1 0.03`; `33 300 l2 0.0` | 300 and 300 points, 0 found; `l1` logged starts are already in `H3+` within solver accuracy, `l2` logged starts are outside (two earlier runs were stopped early; partial logs kept) |
| `python ascent.py 1 40 family` | 40 starts, 0 found (weak method, see Section 2.9) |
| `python ascent.py 2 40 d3` | crashed with a Clarabel solver error |
| `python sos_subst.py A 3`, `A 4`, `H 3`, `H 4` | values in the table of Section 4.7 |

Runs from 2026-10-02 (this continuation):

| Command | Outcome |
| --- | --- |
| `python sanity.py` | cube minimum of the 2026-09-25 counterexample `-8.9e-16`; value over `R_D` `-0.0281`; over `R` `-5.1e-10`; min over all 48 compositions `-7.8e-10` |
| `python check_boundary_members.py` | PASS at four rational points (zero set, tangency, blocking) |
| `python check_apex_bookkeeping.py` | PASS |
| `python check_rounding_map.py` | PASS (exact; 81 generator cases) |
| `python check_rounding_numeric.py 5 200` | 200 optimal points of `R_D`: smallest localizing eigenvalue `-1.5e-8` before and `-2.1e-8` after rounding; other quadratic moments unchanged |
| `python check_boundary_rank_symbolic.py` | rank 9 on all of S1 (minors in Proposition 2.10) |
| `python check_family_strata_symbolic.py` | generic S2-S5 minors (zero-parameter cases added and checked in the r1 revision below) |
| `python check_nond3_blocked.py` (the 8 logs of `fit_all.py`) | 66 of 66 rays outside `cl(D3)` have a blocked vertex |
| `python blocking_exact.py 4` | 312 minimal blocking configurations (exact at random rational positions) |
| `python blocking_positions.py ../logs/blocking2_k4.txt 0 3 3 35 0c 32` | the 32 skipped configurations searched |
| `python postprocess_positions.py` (two runs; the first crashed on an uncaught solver error and was made robust) | 265 configurations with original squared contact residual `<= 1e-6` post-processed at four-decimal positions; only 24 exact-contact solves returned values (19 at or below `1e-4`, 5 above: 3 generically nonempty, 2 special). The other 241 returned no value; the main log has 224 Clarabel panic messages and 229 missing values in 241 records. The "only two special" result covers the 24 solved cases; the main conclusion rests on the 264 direct retests. |
| `python special_config_check.py` | both special maximizers are affine squares (in `D3`) |
| `python positions_retest.py` | 264 valid quadratics tested; one of the 265 original low-cost configurations failed the retest cutoff (Section 2.7); min value over `R` `6.9e-9`; 8 outside `cl(D3)` |
| `python face_explore.py 1 40 3` | 120 rays, 7 outside `cl(D3)`, 0 missing |
| `python family_neighborhood.py 1 40 2 1` | 80 rays, 37 outside `cl(D3)`, 0 missing |
| `python face_probe.py 1 60 family` | 60 points, 0 found |
| `python signclass.py 1 4000 sub` | 3,998 rays; min value over `R_D` `-1.5e-8`, over BNW `-1.7e-9`; 0 below `-1e-6` |
| `python signclass.py 2 4000 sup` | 3,991 rays; 9 outside `cl(D3)`; min value over `R` `-1.7e-9`; BNW below `-1e-6` on 1,102 |
| `python stratum_enum.py {0,1,2} 3 60 40 11` | 6,418 types, 218,352 kernels, 91,719 nonnegative, 417 tested, 95 outside `cl(D3)`, 0 missing; min value over `R` `-2.1e-9` |
| `python fit_stratum_examples.py ''` (log `stratum_enum_fit.txt`; an earlier inline run of the same code gave `stratum_enum_fit_inline.txt`) | 16 examples, all fit family members (max fit cost `6.5e-29`); strata S1-S5 and five-contact |
| `python fit_more.py` | 9 supermodular-sampler rays fit five-contact family members (fit cost `< 1e-16`); 8 retest quadratics have fit costs `3e-7`-`4e-3`, or unit-coefficient distances about `8e-4`-`0.09` (not extreme rays) |
| `python stratum_enum.py {0,1} 2 500 800 23 _dense` and `python stratum_enum.py {0,1} 2 500 800 29 _denseR rev` (stopped by a monitor once all types were covered) | 6,418 types, 3,133,560 kernels, 1,304,623 nonnegative, 6,654 tested, 923 outside `cl(D3)`, 0 missing; min value over `R` `-7.0e-9` (`summarize_strata.py '_dense*'`) |
| `python fit_stratum_examples.py '_dense*'` | 18 examples, all fit family members (max fit cost `4.8e-31`) |
| re-solve of five stored rays (inline, log `check_min_rR_dense.txt`) | original stored values `-1.37e-10` to `1.04e-11`; re-solved values `-4.91e-8` to `1.65e-10`, some changing sign between Clarabel (tight tolerance) and SCS; the unstored `-7.0e-9` ray was not re-solved |
| `python check_rounding_hull.py 7 200` | 200 optimal points of `R_D`, 100 outside `H3+` (separation down to `-1.6e-2`); all 100 satisfy the caps strictly (gap `>= 4.8e-3`); after rounding any coordinate the separation value is `>= -2.0e-7` |
| `python check_rounding_R.py 8 60 0.05` | 60 points of `R` with a forced diagonal excess; family values after rounding `>= -1.4e-8` |
| `python sos_subst.py A 1`, `A 2`, `H 1`, `H 2` | `5.17e-2`, `6.37e-4`, `1.46e-1`, `4.54e-3` |

Runs from 2026-10-03 (revision after review round 1), from the same `code/`
directory unless stated otherwise. These are targeted local checks; no CI
checks or project-wide verification were run. Each Python command used
`OMP_NUM_THREADS=1`; at most two Python processes ran at once, with no
background process left running.

| Command | Outcome |
| --- | --- |
| `OMP_NUM_THREADS=1 timeout 180 python check_family_strata_symbolic.py > ../logs/check_family_strata_symbolic_r1_revision.txt 2>&1` | PASS (exit 0): generic S2-S5 kernel checks and minors; exact kernel and nonzero-minor checks in all eight zero-parameter cases. |
| `OMP_NUM_THREADS=1 timeout 60 python check_review_r1_reporting.py > ../logs/check_review_r1_reporting.txt 2>&1` | PASS (exit 0): 30 boundary examples and their value range; eight fit-distance conversions; scope of five re-solved rays; signs of projection starts in the progress logs; 265-to-264 reconciliation; all four strict positive-product sign patterns. No new solves. |
| `OMP_NUM_THREADS=1 timeout 180 python check_boundary_rank_symbolic.py > ../logs/check_boundary_rank_symbolic_r1_revision.txt 2>&1` | Timed out (exit 124), not a script failure. The unchanged script completed in the round-2 review in about 195 seconds (exit 0), reproducing the stated minors (`reviews/r2-logs/rerun_check_boundary_rank_symbolic.txt`); the revision rerun with `timeout 1200` is recorded below. |
| Two `OMP_NUM_THREADS=1 timeout 60 python` inline checks from the repository root | PASS (exit 0): preliminary stored count/range audit; `ast.parse` syntax checks of the two revised/new scripts. |
| `git diff --check -- research-20261001/three-var-completeness` (repository root) | PASS (exit 0). |
| `pgrep -af three-var-completeness` (repository root), plus a check for the three script names in Python/timeout command lines | No matches (exit 1 for each); no remaining stream process. |

Runs from 2026-10-03 (revision after review round 2), from the stream
directory unless stated otherwise. Every Python command used
`OMP_NUM_THREADS=1` and `PYTHONDONTWRITEBYTECODE=1`; at most two Python
processes ran at once. The reviewer scripts were run unchanged and read
the stream's original logs. These were targeted local checks; no project-wide
verification or CI checks were run.

| Command | Outcome |
| --- | --- |
| `OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 60 python reviews/r2-code/r2_reporting.py > logs/check_review_r2_reporting.txt 2>&1` | PASS (exit 0): 265 exact-contact records, 241 without a value, 19 at or below `1e-4`, 5 above; main-log categories include 224 missing values preceded by Clarabel panics. The direct-retest count is 264, all with `R` values. No new solves. |
| `OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 300 python reviews/r2-code/r2_rounded_theta.py > logs/check_rounded_theta_r2_revision.txt 2>&1` | PASS (exit 0): excluded configuration has cost `9.212e-10` at full precision and `2.535e-6` at four-decimal positions. Five control configurations also reproduced the reviewer's values. These are fixed-position inner SDPs, not new position searches. |
| `OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 60 python - <<'PY' > logs/check_r2_counts_and_zero_edges.txt 2>&1` (inline assertions) | PASS (exit 0): independently counted all 265 exact-contact records and all 241 main-log records (229 without a value, 224 panic messages); all 264 direct retests have both `R` and `R_D` values, none below `-1e-6` over `R`. Exact symbolic substitution verified both edge restrictions at `h = 0` and the zero-edge cases. |
| `OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 1200 /usr/bin/time -p python check_boundary_rank_symbolic.py > ../logs/check_boundary_rank_symbolic_r2_revision.txt 2>&1` (from `code/`) | PASS (exit 0) in 222.24 seconds (3 min 42 s): family kernel check and both 9 x 9 minors stated in Proposition 2.10. This confirms that the earlier 180-second timeout was too short. |
| `git diff --check -- research-20261001/three-var-completeness` (repository root) | PASS (exit 0). |
| `pgrep -af '^(python\|/workspace/local-home/miniconda3/bin/python\|timeout\|/usr/bin/time)( \|$).*(check_boundary_rank_symbolic\.py\|r2_rounded_theta\.py\|r2_reporting\.py)'` (repository root; `\|` shown escaped for the table) | No matches (exit 1); no remaining process from these checks. |

File guide. Core modules: `cube3.py` (polynomials, symmetries, family,
localizing matrices, face enumeration), `sdp3.py` (relaxations `R_D`, `R`, exact
separation over `P3+`), `fit_family.py` (family fitting), `zero_pattern.py`,
`face_explore.py` (contact rows). Exact checks: `check_rounding_map.py`,
`check_boundary_rank_symbolic.py`, `check_family_strata_symbolic.py`,
`check_boundary_members.py`, `check_apex_bookkeeping.py`, `blocking_exact.py`.
Searches and their analysis: the scripts in the tables above, plus
`check_rounding_numeric.py`, `check_rounding_R.py`, `classify_notd3.py`. The
files `dbg_ascent.py` and `killpy.sh` are debugging leftovers of the first run
and are not used for any reported number.

## 8. Limits

- Conjecture 2.11 is not proved. The searches sample extreme rays and
  point-contact strata; a family of missing rays with very small normal cones,
  on strata with zero segments or higher-order contacts, or with relaxation
  values between `-1e-6` and `0`, could have been missed.
- Theorem 2.5 depends on Theorem 1 of Burer, Natarajan and Willemsen, a recent
  preprint (v3, 31 August 2026). We read its proof but did not verify it line by
  line; our numerical control (3,998 submodular rays) agrees with it.
- The blocking enumeration covers point zeros only (at most four); zero
  segments were not enumerated (`blocking_exact.py` has an option for one
  segment, which was not run). The special-position search uses local
  optimization (Nelder-Mead from three starts) and can miss feasible positions.
- Membership tests are floating-point SDPs. Only the statements labeled
  "computed exactly" or "proved" rest on exact arithmetic or proofs.
- Theorems 4.2-4.6 and Lemma 4.8 rest on BKT's Lemma 2.3, Theorems 2.13, 3.7
  and 3.15, Example 3.4, on Tarski transfer, and on the closure of shadows under
  dual cones. We checked the statements we use against the BKT text, not their
  proofs.
- Part (b) leaves open all positive graphs without a `K_4` minor that have a
  component with at least four vertices.

## 9. Open questions

1. Prove Conjecture 2.11, or find a missing ray. By Corollary 2.6 only
   quadratics with all three cross coefficients positive need to be treated.
2. Can the rank-and-active-set proof of BNW be adapted to the relaxation `R`
   for supermodular objectives?
3. Are the boundary-stratum rays of Proposition 2.10 exposed?
4. Is `COP(F_5)` a spectrahedral shadow? A negative answer would settle `P_4`
   and, by minor closure, every positive component that contains a path on
   four vertices.
5. Does `H(K_{1,3})` (the star with three positive leaves) have a finite SDP
   lift? All local cones are shadows, so a proof of non-representability
   would need a global construction; by Remark 4.9 it suffices to study the
   submodular part.
6. Which series-parallel positive graphs have finite lifts? The forbidden
   minors include `K_4`; the rest of the list is unknown.
7. Is the cone of submodular quadratics (nonpositive cross coefficients) that
   are nonnegative on `[0,1]^4` a spectrahedral shadow? A positive answer would
   give finite lifts for `P_4` and `K_{1,3}` (Remark 4.9).
8. Is the cone of quadratics nonnegative on a four-dimensional polytope
   without simple vertices (for example the cross-polytope) a spectrahedral
   shadow?

## Process hygiene

Every computation started in this continuation had an explicit `timeout`
(between 600 s and 9,000 s), long searches wrote checkpoint files
(`postprocess_positions.jsonl`, `stratum_enum*_*.jsonl`) so that interrupted work
can resume, and no open-ended search was started. The dense stratum shards were
stopped by a monitor script once every type had a record. Before this note was
finalized (2026-10-02, about 21:10 EDT), `pgrep` showed no remaining process of
this stream: every background process started in this continuation had
finished or been stopped. The first author run left no running processes
either (checked at the start of the continuation).

The 2026-10-03 round-1 revision used timeouts of 60 or 180 seconds, no new
searches, and at most two Python processes at once. The added S2-S5 checks and
stored-data audit passed; the optional rerun of the unchanged S1 script timed
out after 180 seconds; the reviewer completed it in about 195 seconds (exit 0)
with the stated minors. Final process checks found no remaining stream process.
Only files under `three-var-completeness/` were edited, excluding `reviews/`;
no commit, staging, branch change or other git-state change was made.

The round-2 revision used timeouts of 60, 300 and 1,200 seconds and at most
two Python processes at once. The stored-data checks, fixed-position inner
SDPs, exact zero-edge identities and unchanged S1 script all passed. The S1
rerun completed in 222.24 seconds (exit 0) with both stated minors; its earlier
180-second timeout was too short. Final process checks found no remaining
process from these checks. Only the note and new logs under
`three-var-completeness/` were written; reviewer files were unchanged. No
commit, staging, branch change or other git-state change was made.
