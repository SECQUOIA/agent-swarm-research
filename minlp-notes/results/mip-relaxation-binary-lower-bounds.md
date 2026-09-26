# Minimum number of binary variables in MIP relaxations of `x^2` and `xy`

Status: proofs written and self-checked on 2026-09-05; numerically verified by
`code/mip_relaxation_binaries/check_bounds.py`; independently reviewed with corrections on 2026-09-05 (see
`notes/review-mip-relaxation-binary-lower-bounds.md`); not externally peer reviewed. Literature searches (Sect. "Novelty assessment") found no prior
statement of these bounds for arbitrary MIP relaxations, but the argument is elementary and
may be folklore; an unsuccessful search does not establish novelty.

Summary. In the framework of Beach, Burlacu, Bärmann, Hager, Hildebrand (Part I, Comput.
Optim. Appl. 87:835–891, 2024, arXiv:2211.00876; Part II, arXiv:2302.01164), an MIP
relaxation of the graph of `f` over a box is the projection of a mixed-binary polyhedral set
onto `(x, w)`, and its quality is the maximum vertical error `E_max`. We prove:

- (A) Every MIP relaxation of `w = x^2` on `[0,1]` with `p` binary variables has
  `E_max >= 2^{-2p-2}`. The depth-`p` sawtooth relaxation of Beach et al. has
  `E_max = 2^{-2p-2}`, so it is exactly optimal among all MIP relaxations with `p` binaries,
  and `p_min(ε) = max{0, ⌈(log2(1/ε) − 2)/2⌉}` for every `ε > 0`. More generally, for an
  `m`-strongly convex (or concave) `f` on an interval of length `D` and any relaxation whose
  integer variables take at most `N` values, `E_max >= m D^2 / (8 N^2)`; in `d` dimensions,
  `E_max >= (m/2) (1/(N ω_d))^{2/d}`.
- (B) Every MIP relaxation of `w = xy` on `[0,1]^2` with `p` binary variables has
  `E_max >= 1/(16 ln 2 · 2^p) > 0.0901 · 2^{-p}`. NMDT (Part II) achieves `E_max = 2^{-p-2}`
  with `p` binaries. Hence, for `0 < ε <= 1/4`,
  `⌈log2(1/ε) − log2(16 ln 2)⌉ <= p_min(ε) <= ⌈log2(1/ε)⌉ − 2`, i.e. `p_min(ε) = log2(1/ε) + O(1)`
  with the unknown additive constant confined to an interval of length 2.
- (C) For one-sided (epigraph) relaxations of a convex `f` the argument gives nothing, and
  indeed no binary-variable lower bound exists: the sawtooth epigraph relaxation reaches
  any accuracy with zero binaries. The hypograph side still needs `2^{-2p-2}`.

The lower bounds count only binary (or bounded integer) variables. The number of
continuous auxiliary variables and of linear constraints is unrestricted.

## Setting (Beach et al., Part I, Sect. 2)

Beach et al. study mixed-integer sets
`P^IP := {(u, v, z) ∈ R^{d+1} × [0,1]^p × {0,1}^q : A(u, v, z) <= b}` (Part I, p. 839) and
their projections `proj_u(P^IP)`. Definition 2 (p. 840): `P^IP` is an *MIP relaxation* of
`U ⊆ R^{d+1}` if `U ⊆ proj_u(P^IP)`, with the main cases
`U = {(x, z) ∈ [0,1]^2 : z = x^2}` and `U = {(x, y, z) ∈ [0,1]^3 : z = xy}`. Definition 3
(pp. 840–841): the pointwise error of `ū ∈ proj_u(P^IP)` is
`E(ū, U) := min{|u_{d+1} − ū_{d+1}| : u ∈ U, u_[d] = ū_[d]}` and the maximum error is
`E^max(P^IP, U) := max_{ū ∈ proj_u(P^IP)} E(ū, U)`.

We use the following equivalent form, with the roles of the letters as in the task
statement. Let `B ⊂ R^d` be a box and `f : B → R` continuous. An *MIP relaxation of
`graph_B(f)` with `p` binary variables* is a set

```
R = proj_{(x,w)} P,    P = {(x, w, λ, z) ∈ R^d × R × R^q × {0,1}^p : A(x, w, λ) + B z <= c},
```

with `A` linear, such that `graph_B(f) = {(x, f(x)) : x ∈ B} ⊆ R`. (Bounds such as
`λ ∈ [0,1]^q` and `x ∈ B` are linear constraints and may be part of `A(...) <= c`.) Its
maximum (two-sided, vertical) error is

```
E_max(R) := sup { |w − f(x)| : (x, w) ∈ R, x ∈ B }.
```

Conventions. (i) The error is measured only over `x ∈ B`; if `R` contains points with
`x ∉ B` they are ignored (Beach et al. always include `x ∈ B` in the constraints, so this
agrees with their definition). (ii) We write `sup`; see Lemma 1(c) for when it is a `max`.
(iii) A relaxation with `p = 0` binaries is a single polyhedron. (iv) For bounded general
integer variables `z_i ∈ {l_i, …, u_i}` everything below holds with `2^p` replaced by
`N = Π_i (u_i − l_i + 1)`, the number of integer assignments.

Beach et al.'s constructions. For `x^2` on `[0,1]`, let `F_L` be the piecewise linear
interpolant of `x^2` at the breakpoints `i/2^L`, written through the tooth function
`G(x) = min{2x, 2(1−x)}` as `F_L(x) = x − Σ_{j=1}^{L} 2^{-2j} G^{∘j}(x)` (Part I, eq. (6),
p. 842). Proposition 1 (p. 842) records `0 <= F_L(x) − x^2 <= 2^{-2L-2}` and that
`F_L − 2^{-2L-2}` consists of the tangents of `x^2` at the midpoints `i/2^L + 1/2^{L+1}`.
The depth-`L` *sawtooth relaxation* (Definition 5, eqs. (11)–(12), p. 845) is

```
SR_L = {(x, z) ∈ [0,1] × R : ∃ (g, α) ∈ [0,1]^{L+1} × {0,1}^L :
        z <= f_L(x, g),  z >= f_j(x, g) − 2^{-2j-2} (j = 0..L),  z >= 0,  z >= 2x − 1,
        (x, g, α) ∈ S_L},
```

where `S_L` (eqs. (7)–(8), pp. 842–843) forces `g_0 = x` and, for integral `α`,
`g_j = G(g_{j−1})`, and `f_j(x, g) = x − Σ_{k=1}^{j} 2^{-2k} g_k` (empty sum for `j = 0`). It uses `L` binary
variables. Its maximum error is `2^{-2L-2}` (Part I, Sect. 5.1.1, p. 851: "the (tightened)
sawtooth relaxation has the same maximum error of `2^{-2L-2}` as the sawtooth
approximation"; also Sect. 5.1.2, p. 853, and Table 1, p. 850). The sawtooth *epigraph*
relaxation `Q_L` (Definition 6, eqs. (14)–(15), p. 846) has no binary variables and
one-sided error `2^{-2L-4}` (Proposition 2, pp. 851–852).

For `xy` on `[0,1]^2`: HybS (Part I, Definition 10, eq. (21), p. 849) uses the tightened
sawtooth relaxation `R_{L,L_1}` for `x^2` and `y^2` (so `2L` binaries per product) and has
`2^{-2L-2} <= E_max <= 2^{-2L-2} + 2^{-2L_1-3}` (Propositions 3 and 4, pp. 853–854;
Remark 5, p. 854: the error tends to `2^{-2L-2}` as `L_1 → ∞` without new binaries).
NMDT (Part II, Definition 5, Sect. 4.1) discretizes `x = Σ_{j=1}^{L} 2^{-j} β_j + Δx_L`
with `β ∈ {0,1}^L` and applies McCormick on each strip; Part II, Proposition 1 (Sect. 5.1):
"The maximum error in the NMDT MIP relaxation for `z = xy` with `x, y ∈ [0,1]` is
`1/4 (2^{-L} · 1) = 2^{-L-2}`." D-NMDT (Part II, Definition 8, Sect. 4.2) discretizes both
variables with `β^x, β^y ∈ {0,1}^L` and has error `2^{-2L-2}` (Part II, Proposition 2,
Sect. 5.1; Table 1, Sect. 5). The McCormick relaxation (`p = 0`) has error
`(x̄ − x_)(ȳ − y_)/4` (Part I, p. 852), i.e. `1/4` on the unit box.

## Lemma 1 (structure of an MIP relaxation)

Let `R` be an MIP relaxation with `p` binary variables as above. Then:

(a) `R = ∪_{z ∈ {0,1}^p} R_z` with `R_z := proj_{(x,w)} P_z`,
`P_z := {(x, w, λ) : A(x, w, λ) <= c − Bz}`, and every `R_z` is a polyhedron, in
particular closed and convex (possibly empty).

(b) `R` is closed, and the sets `S_z := {x ∈ B : (x, f(x)) ∈ R_z}` are closed subsets of
`B` with `∪_z S_z = B`.

(c) If `E_max(R) < ∞`, then `R ∩ (B × R)` is compact and the supremum defining `E_max(R)`
is attained, so `E_max` coincides with the `max` in Beach et al.'s Definition 3.

Proof. (a) Fixing `z` fixes the right-hand side, so `P_z` is a polyhedron in
`(x, w, λ)`-space. The projection of a polyhedron onto a coordinate subspace is a
polyhedron (Fourier–Motzkin elimination; e.g. Ziegler, *Lectures on Polytopes*,
Sect. 1.2). A polyhedron is closed and convex. (b) A finite union of closed sets is closed.
`S_z` is the preimage of the closed set `R_z` under the continuous map
`x ↦ (x, f(x))` restricted to the closed box `B`; the union is `B` because
`graph_B(f) ⊆ R = ∪_z R_z`. (c) `R ∩ (B × R)` is closed, and if `E_max(R) < ∞` then
`|w| <= max_B |f| + E_max(R)` on it, so it is bounded; `|w − f(x)|` is continuous on this
compact set. ∎

## Lemma 2 (chord midpoints)

Let `R_z` be convex with `(x_1, f(x_1)), (x_2, f(x_2)) ∈ R_z`, `x_1, x_2 ∈ B`, `B` convex.
Then `m = (x_1 + x_2)/2 ∈ B` and `(m, (f(x_1) + f(x_2))/2) ∈ R_z`, so

```
E_max(R) >= | (f(x_1) + f(x_2))/2 − f(m) |.
```

In particular: for `f(x) = x^2`, the right-hand side is `(x_2 − x_1)^2 / 4`; for
`f(x, y) = xy`, it is `|(x_1 − x_2)(y_1 − y_2)| / 4`; and if `f − (m_2/2)|x|^2` is convex
on `B` (`m_2`-strong convexity; e.g. `f ∈ C^2` with `∇^2 f ⪰ m_2 I`, or `f'' >= m_2` in
one variable), it is at least `m_2 |x_1 − x_2|^2 / 8`. The same holds for `−f` in place of
`f`.

Proof. The midpoint statement is convexity of `R_z`. For `x^2`:
`(x_1^2 + x_2^2)/2 − ((x_1 + x_2)/2)^2 = (x_1 − x_2)^2/4`. For `xy`:
`(x_1 y_1 + x_2 y_2)/2 − (x_1 + x_2)(y_1 + y_2)/4 = (x_1 − x_2)(y_1 − y_2)/4`. For strongly
convex `f`, put `g = f − (m_2/2)|x|^2`; convexity of `g` gives
`(g(x_1) + g(x_2))/2 >= g(m)`, hence
`(f(x_1) + f(x_2))/2 − f(m) >= (m_2/2) [ (|x_1|^2 + |x_2|^2)/2 − |m|^2 ] = m_2 |x_1 − x_2|^2/8`.
∎

## Integer-dimension strengthening via the published midpoint lemma

Every lower bound below also holds with `p` interpreted as the number of
**unrestricted integer variables**, even if the lifted constraints define an
arbitrary convex set rather than a polyhedron. The upper bounds remain binary
linear formulations. To see this, group graph points by the parity class of
any feasible integer lift. Two graph points with lifts in the same parity
class have a feasible midpoint lift with integer coordinates. Therefore the
midpoint inequalities of Lemma 2 hold inside each of at most `2^p` classes.
Take the closures of these classes in the compact box: continuity preserves
the midpoint inequalities, and the closures still cover the box. All diameter
and measure arguments below then apply with `N=2^p`.

This uses the established parity mechanism of Lubin, Vielma, and Zadik's
Midpoint Lemma (Lemma 4.1),
[[lubin2022-mixed-integer-convex-representability]] p.11-12.
The full argument and its scope are recorded in
`notes/mip-binary-lower-bound-extensions.md`. Bounds based instead on the
number `N` of available integer assignments remain valid as well.

## Theorem A (univariate)

Let `R` be an MIP relaxation of `graph_{[0,1]}(x^2)` with `p` binary variables. Then

```
E_max(R) >= 2^{-2p-2}.
```

The sawtooth relaxation `SR_p` (Part I, Definition 5) has `E_max(SR_p) = 2^{-2p-2}`, so it
is optimal among all MIP relaxations with `p` binary variables, for every `p >= 0`.
Consequently the minimum number of binary variables needed for error at most `ε` is

```
p_min(ε) = max{ 0, ⌈ (log2(1/ε) − 2) / 2 ⌉ }     for every ε > 0.
```

Proof. If `E_max(R) = ∞` there is nothing to prove. By Lemma 1(b) the closed sets
`S_z ⊆ [0,1]`, `z ∈ {0,1}^p`, cover `[0,1]`. By subadditivity of Lebesgue measure,
`1 = λ([0,1]) <= Σ_z λ(S_z)`, so some `S_z` has `λ(S_z) >= 2^{-p}`. This `S_z` is a nonempty
compact subset of `[0,1]`; let `x_1 = min S_z`, `x_2 = max S_z`. Since
`S_z ⊆ [x_1, x_2]`, `x_2 − x_1 >= λ(S_z) >= 2^{-p}`. Both `(x_i, x_i^2)` lie in the convex
set `R_z`, so Lemma 2 gives `E_max(R) >= (x_2 − x_1)^2/4 >= 2^{-2p-2}`.

Optimality of the sawtooth relaxation: `SR_p` is an MIP relaxation with `p` binaries and
`E_max(SR_p) = 2^{-2p-2}` (Part I, Sect. 5.1.1, p. 851). For completeness: with `α`
integral the constraints `S_p` force `g_j = G^{∘j}(x)`, so the upper boundary of `SR_p` is
`F_p(x)`, whose error `F_p(x) − x^2 <= 2^{-2p-2}` is attained at every midpoint
`i/2^p + 1/2^{p+1}` (Proposition 1, p. 842); the lower boundary is the maximum of tangents
of `x^2`, which never lies above `x^2`, and the tangents at the `2^p` midpoints alone
already give lower error at most `2^{-2p-2}`. Hence `E_max(SR_p) = 2^{-2p-2}` exactly.
(The lower-side error is in fact `2^{-2p-4}`, since the constraints `z >= f_j − 2^{-2j-2}`
for `j < p` together with `z >= 0`, `z >= 2x − 1` supply tangents at all points
`k/2^{p+1}`; this is consistent with Proposition 2 of Part I.)

The formula for `p_min(ε)`: `SR_L` has error `<= ε` iff `2^{-2L-2} <= ε` iff
`L >= (log2(1/ε) − 2)/2`, and by the lower bound no relaxation with fewer binaries has
error `<= ε`. ∎

Remark (sharpness is exact, not just in order). The lower bound and the sawtooth
relaxation agree for every `p`, including `p = 0`, where the bound `1/4` is attained by
the McCormick-type polyhedron `{0 <= z <= x, z >= 2x − 1}`... more precisely by
`SR_0 = {(x, z) : max(0, 2x − 1, x^2-tangent at 1/2) <= z <= x}`, whose error `1/4` occurs at
`x = 1/2`.

## Theorem A' (general strongly convex or concave functions; general integers)

Let `f : [a, b] → R` be such that `f − (m_2/2)x^2` or `−f − (m_2/2)x^2` is convex for some
`m_2 > 0` (for `f ∈ C^2` it suffices that `f'' >= m_2` throughout or `f'' <= −m_2`
throughout), and let `D = b − a`. Let `R` be an MIP relaxation of `graph_{[a,b]}(f)` whose
integer variables take at most `N` distinct assignments (`N = 2^p` for `p` binaries;
`N = Π_i (u_i − l_i + 1)` for bounded integers). Then

```
E_max(R) >= m_2 D^2 / (8 N^2).
```

For `f = x^2` (`m_2 = 2`, `D = 1`, `N = 2^p`) this is `2^{-2p-2}`, so Theorem A is the
special case. More generally, if `f : B → R` on a box `B ⊂ R^d` of volume `V` is
`m_2`-strongly convex or concave, then

```
E_max(R) >= (m_2 / 2) · ( V / (N ω_d) )^{2/d},
```

where `ω_d` is the volume of the unit ball in `R^d` (`ω_1 = 2`, `ω_2 = π`).

Proof. Lemma 1 holds verbatim with `{0,1}^p` replaced by the finite set of integer
assignments, so `B` is covered by at most `N` closed sets `S_z`, and one of them has
`λ(S_z) >= V/N`. By the isodiametric inequality (Evans–Gariepy, *Measure Theory and Fine
Properties of Functions*, Sect. 2.2), `λ(S_z) <= ω_d (diam S_z / 2)^d`, so
`diam S_z >= 2 (V/(N ω_d))^{1/d}`; the diameter of a compact set is attained by two points
`x_1, x_2 ∈ S_z`. Lemma 2 (strongly convex case, or applied to `−f`) gives
`E_max(R) >= m_2 |x_1 − x_2|^2 / 8 >= (m_2/2) (V/(N ω_d))^{2/d}`. For `d = 1`, `ω_1 = 2` and
`V = D`, giving `m_2 D^2/(8N^2)`. ∎

Remark (order is right in every dimension). For `f ∈ C^2` on a neighborhood of `B`,
let `M` bound the operator norm of its Hessian. For large `N`, a regular grid with
`k = floor(N^{1/d})` cells per axis uses `k^d <= N` sub-boxes, each of diameter
`h = O(N^{-1/d})`. On a cell with center `c`, Taylor's theorem gives
`|f(x) − [f(c)+∇f(c)·(x−c)]| <= M h^2/8`. The polyhedral tube between this affine
function plus and minus `M h^2/8` contains the graph on the cell and has vertical
error at most `M h^2/4`. These bounded polyhedra can be encoded as a finite
disjunction with `ceil(log2(k^d)) <= ceil(log2 N)` binaries (unused binary words
can be excluded). Thus `E_max = Θ(2^{-2p/d})` is the correct rate for smooth
strongly convex `f`; the constants above are not claimed sharp for `d >= 2`.
Using the convex hull of a smooth graph directly would not justify an MIP upper
bound, because that hull need not be polyhedral.

## Lemma 3 (area of a set with small products of differences)

Let `S ⊆ [0,1]^2` be closed and `ε >= 0` such that `|(x_1 − x_2)(y_1 − y_2)| <= 4ε` for all
`(x_1, y_1), (x_2, y_2) ∈ S`. Then

```
λ(S) <= 16 ln 2 · ε   (≈ 11.09 ε),      and      X · Y <= 20 ε,
```

where `X`, `Y` are the widths of the projections of `S` onto the two axes.

Proof. `S` is compact; pick `a = (a_x, a_y) ∈ S` with minimal `x`-coordinate and
`b = (b_x, b_y) ∈ S` with maximal one, `X = b_x − a_x`. If `X = 0`, `S` lies on a vertical
line and `λ(S) = 0`. Otherwise, for `u ∈ (a_x, b_x)` consider the section
`S_u = {y : (u, y) ∈ S}`. Every `(u, y) ∈ S` satisfies `|y − a_y| <= 4ε/(u − a_x)` and
`|y − b_y| <= 4ε/(b_x − u)`, so `S_u` lies in the intersection of two intervals of lengths
`8ε/(u − a_x)` and `8ε/(b_x − u)`, hence `λ_1(S_u) <= min{8ε/(u − a_x), 8ε/(b_x − u)}`.
By Tonelli's theorem (S is Borel), substituting `t = u − a_x`,

```
λ(S) = ∫_{a_x}^{b_x} λ_1(S_u) du <= ∫_0^X min{8ε/t, 8ε/(X − t)} dt
      = 2 ∫_0^{X/2} 8ε/(X − t) dt = 16 ε ln 2 .
```

For the box bound: every `c ∈ S` has `|c_x − a_x| + |c_x − b_x| = X`, so one of the two
distances is `>= X/2` and correspondingly `|c_y − a_y| <= 8ε/X` or `|c_y − b_y| <= 8ε/X`;
together with `|a_y − b_y| <= 4ε/X` all `y`-values lie in an interval of length
`<= 4ε/X + 16ε/X = 20ε/X`, so `Y <= 20ε/X`. ∎

The constant `16 ln 2` is sharp for the envelope used in the proof (the region
`{(u, y) : |y − a_y| <= 4ε/(u − a_x), |y − b_y| <= 4ε/(b_x − u)}` has measure exactly
`16 ε ln 2` when it fits in the box), but the envelope is larger than any admissible `S`,
so the best constant in Lemma 3 is presumably smaller. It is not needed below.

## Theorem B (bivariate product)

Let `R` be an MIP relaxation of `graph_{[0,1]^2}(xy)` with `p` binary variables. Then

```
E_max(R) >= 1 / (16 ln 2 · 2^p) > 0.0901 · 2^{-p}.
```

Conversely, NMDT with depth `L = p` (Part II, Definition 5 and Proposition 1) is an MIP
relaxation with `p` binaries and `E_max = 2^{-p-2}`; D-NMDT with depth `L` (Part II,
Definition 8 and Proposition 2) has `2L` binaries and `E_max = 2^{-2L-2} = 2^{-p-2}`; HybS
(Part I, Definition 10, Propositions 3–4) has `2L` binaries and
`2^{-p-2} <= E_max <= 2^{-p-2} + 2^{-2L_1-3}`. Therefore, for `0 < ε <= 1/4`,

```
⌈ log2(1/ε) − log2(16 ln 2) ⌉  <=  p_min(ε)  <=  ⌈ log2(1/ε) ⌉ − 2,
```

with `log2(16 ln 2) = 3.4712…`; the two sides differ by at most 2. For `ε >= 1/4`,
`p_min(ε) = 0` (McCormick). In particular `p_min(ε) = log2(1/ε) + O(1)`, and every MIP
relaxation of `xy` with `p` binaries has error between `0.0901 · 2^{-p}` and (if it is as
good as NMDT) `0.25 · 2^{-p}`.

Proof. Assume `ε := E_max(R) < ∞`. By Lemma 1(b) the closed sets
`S_z = {(x, y) ∈ [0,1]^2 : (x, y, xy) ∈ R_z}` cover `[0,1]^2`. For two points of the same
`S_z`, Lemma 2 gives `|(x_1 − x_2)(y_1 − y_2)|/4 <= ε`, so each `S_z` satisfies the
hypothesis of Lemma 3 and `λ(S_z) <= 16 ε ln 2`. Subadditivity gives
`1 = λ([0,1]^2) <= Σ_z λ(S_z) <= 2^p · 16 ε ln 2`, i.e. `ε >= 1/(16 ln 2 · 2^p)`.

Upper bounds: NMDT with `p` binaries partitions `[0,1]` in `x` into `2^p` strips of width
`2^{-p}` and applies McCormick on each strip `[k 2^{-p}, (k+1) 2^{-p}] × [0,1]`; the
McCormick error on a `w × h` rectangle is `wh/4` (Part I, p. 852), giving `2^{-p-2}`
(Part II, Proposition 1). The statements for D-NMDT and HybS are Part II, Proposition 2
and Part I, Propositions 3–4.

The bounds on `p_min(ε)`: if `E_max(R) <= ε` then `2^p >= 1/(16 ε ln 2)`, giving the left
inequality; NMDT with `p = ⌈log2(1/ε)⌉ − 2 >= 0` binaries has error
`2^{-p-2} = 2^{-⌈log2(1/ε)⌉} <= ε`, giving the right one. The gap: with
`t = log2(1/ε)` and `c = log2(16 ln 2)`,
`⌈t⌉ − 2 − ⌈t − c⌉ < c − 1 < 2.48`, so it is at
most 2. ∎

Remark (what is not claimed). Theorem B does not identify the optimal relaxation of `xy`
for a given `p`; the factor between the lower bound `1/(16 ln 2)` and NMDT's `1/4` is
`4 ln 2 ≈ 2.77`. Closing it would require either a set `S` in Lemma 3 with measure close to
`16 ε ln 2` that is realizable as an `S_z`, or a sharper covering argument using the
convex hull of the graph over `S_z` rather than a single chord.

Remark (indefinite quadratics). For `f(x, y) = (1/2)(x, y) H (x, y)^T` with `det H < 0`,
Lemma 2 gives midpoint error `|Δ^T H Δ|/8`, and a linear change of coordinates
diagonalizing `H` to `[[0,1],[1,0]]` reduces to Lemma 3 on a parallelogram; hence
`E_max = Θ(2^{-p})` for every indefinite bivariate quadratic, with constants depending on
`H`. For positive or negative definite quadratics Theorem A' gives `Θ(2^{-p})` as well
(`d = 2`). We do not work out the constants.

## One-sided (epigraph and hypograph) relaxations

Call `R ⊇ epi_B(f)` an epigraph relaxation and measure its one-sided error
`E_under(R) = sup{ (f(x) − w)^+ : (x, w) ∈ R, x ∈ B }` (how far `R` reaches below the graph);
symmetrically `E_over` for hypograph relaxations `R ⊇ hyp_B(f)`.

Why Lemma 2 does not apply to the epigraph of a convex `f`: the midpoint of two graph
points lies on a chord, which lies *above* the graph of a convex function, hence inside
`epi f`; no error is produced. And there is no binary-variable lower bound at all: for
`f = x^2` on `[0,1]`, the sawtooth epigraph relaxation `Q_L` (Part I, Definition 6) has
zero binary variables, `L + 1` continuous variables and `O(L)` constraints, and
`E_under(Q_L) = 2^{-2L-4}` (Part I, Proposition 2); its projection is the polyhedron cut out
by the `2^{L+1} + 1` tangents of `x^2` at the points `k/2^{L+1}`. So for the convex side
the right complexity measure is the size of the extended formulation (continuous
variables plus constraints), not the number of binaries. The logarithmic order in
this size measure follows from the standard face-count lower bound: a polyhedron
with `m` inequalities has at most `2^m` faces, while any projected polyhedral
outer approximation of this epigraph within error `ε` needs at least
`1/(2 sqrt(ε))` lower facets. Hence `m >= (1/2) log2(1/ε) − 1`.
A detailed proof is retained in `notes/mip-binary-lower-bound-extensions.md`;
this is an elementary consequence of established extension-complexity counting,
not a novelty claim. Special polygons can have logarithmic-size extended
formulations (Ben-Tal–Nemirovski; Fiorini, Rothvoss, Tiwary, "Extended formulations
for polygons", Discrete Comput. Geom. 48, 2012); this is not true of all polygons.

The nonconvex side keeps the bound: for hypograph relaxations `R ⊇ hyp_{[0,1]}(x^2)`, the
proof of Theorem A applies verbatim to the sets `S_z = {x : (x, x^2) ∈ R_z}` and gives
`E_over(R) >= 2^{-2p-2}`, attained by the upper half of the sawtooth approximation
(`z <= f_p(x, g)`, Part I, Definition 4, p. 844). A two-sided graph relaxation need not contain the hypograph. Its downward
closure does contain the hypograph, uses the same binaries, and has exactly the
same overestimation error. Thus this hypograph obstruction is the source of
Theorem A.

## Comparison with the classical piecewise-linear counting argument

Two classical facts, combined, give a weaker and narrower statement:

1. Any continuous piecewise linear function with `k` affine pieces that approximates `x^2`
   on `[0,1]` uniformly within `ε` has a piece of width `h >= 1/k`, and the best uniform
   affine approximation of `x^2` on an interval of width `h` has error `h^2/8` (the
   Chebyshev alternation solution: the chord shifted down by `h^2/8`). Hence
   `k >= 1/√(8ε)`.
2. A disjunction of `k` pieces (a nonconvex piecewise linear function) needs at least
   `⌈log2 k⌉` binaries, because each binary assignment yields a convex set that can
   contain graph points from at most one piece's interior. (This is the folklore
   counterpart of the logarithmic constructions of Vielma and Nemhauser, Math. Program.
   128:49–72, 2011; their paper attains `⌈log2 k⌉` and, in its concluding section, states
   that necessary conditions for logarithmic formulations are open, so it does not contain
   the lower bound as a theorem.)

Together: an MIP formulation *of a piecewise linear approximant* needs
`p >= (1/2) log2(1/ε) − 3/2`. Theorem A differs in two ways. It applies to arbitrary MIP
relaxations — sets, not graphs of functions; any number of continuous variables and
constraints; two-sided tubes whose boundaries need not be piecewise linear interpolants —
and it has the exact constant: `p >= (1/2) log2(1/ε) − 1`, attained by the sawtooth
relaxation for every `p`. The unifying observation behind both is only that a
mixed-binary polyhedral set with `p` binaries projects to a union of `2^p` polyhedra.
Beach et al.'s own lower bound (Part I, Proposition 3) is specific to Bin2, Bin3, HybS.

## Verification

`code/mip_relaxation_binaries/check_bounds.py` (environment `minlp-notes`; runtime about
one minute) performs two checks:

1. Sawtooth relaxation of `x^2`, `L = 1, …, 6`. For every `α ∈ {0,1}^L` the polyhedron of
   Definition 5 with `α` fixed is built explicitly (variables `g_1..g_L, z`; constraints
   (8) and (12)) and, on the dyadic grid of step `2^{-(L+3)}`, `max z` and `min z` are
   computed by LP (`scipy.optimize.linprog`, HiGHS). The union over `α` covers the grid,
   the LP envelopes agree with the closed-form envelopes `F_L` and
   `max_j (F_j − 2^{-2j-2}, 0, 2x − 1)`, and the maximum error equals `2^{-2L-2}` to
   `1e-9` for every `L` (all candidate extrema — piece midpoints, breakpoints, tangent
   intersections — are dyadic points contained in the grid; a 4001-point uniform grid is
   also checked).
2. Lemma 3. Three hundred random sets `S` in `[0,1]^2` are generated greedily subject to
   `|Δx Δy| <= 4ε` for all pairs (`ε` log-uniform in `[1e-4, 1e-1]`, half of the sets seeded
   with a pair of full `x`-spread); the box product `XY/ε` stayed below 20 (maximum
   observed 15.40) and all pointwise section inequalities held (maximum `|Δy||Δx|/ε`
   observed 4.000). Two hundred random envelopes
   `{|y − a_y| <= 4ε/(u − a_x), |y − b_y| <= 4ε/(b_x − u)} ∩ [0,1]^2` had measure at most
   `16 ε ln 2` (maximum observed ratio 11.086 against the bound 11.090).

Output ends with `ALL OK`. Numerical checks support the statements; they do not replace
the proofs.

## Novelty assessment

Searches performed (web, 2026-09-05): "lower bound number of binary variables MIP
relaxation error nonconvex function"; "piecewise linear approximation x^2 number of pieces
lower bound binary variables logarithmic"; "Vielma Nemhauser modeling disjunctive
constraints logarithmic number of binary variables lower bound"; "sawtooth relaxation
optimal binary variables x^2 MIP relaxation error 2^{-2L-2}"; a search for "MIP relaxation"
of `xy` with a binary-count error trade-off or impossibility statement; and a search for
the union-of-polyhedra argument in the Huchette–Vielma literature. Full texts checked:
Part I (econstor PDF), Part II (arXiv HTML), Beach–Hildebrand–Huchette
(arXiv:2011.08823; grep for "at least", "necessary", "cannot", "optimal", "any
formulation"), and Vielma–Nemhauser (full PDF; grep for "log2", "necessary", "lower bound").

Findings. Beach et al. state maximum errors of their constructions and, in Part I
Proposition 3, a matching lower bound for those specific relaxations; neither part claims
optimality among all MIP relaxations. Beach–Hildebrand–Huchette attribute the
`2^{-2L-2}` error of the sawtooth interpolant to Yarotsky (Neural Networks 94, 2017,
Proposition 2) and state no lower bound. The classical results that surfaced are the
logarithmic formulations of Vielma–Nemhauser (upper bounds), pieces-count lower bounds for
piecewise linear approximation of concave/convex functions (Magnanti–Stratila, "Separable
concave optimization approximately equals piecewise-linear optimization", arXiv:1201.3148,
for `√x` and relative error), and comparisons of univariate versus bivariate piecewise
linear formulations of `xy` by number of simplices (Bärmann, Burlacu, Hager, Kleinert,
J. Global Optim. 2022). None of these bounds the error of an *arbitrary* MIP relaxation
in terms of the number of binary variables, and none records the exact optimality of the
sawtooth relaxation or the `Θ(2^{-p})` law for `xy`.

An additional close precedent is Lubin, Vielma, and Zadik, "Mixed-integer convex
representability", Mathematics of Operations Research 47 (2022), Lemma 4.1:
their midpoint lemma bounds integer dimension through sets of mutually incompatible
midpoints. The geometric obstruction here belongs to that established framework;
our volume arguments quantify it for approximation. Their parity proof also
extends the present lower bounds to unrestricted integer variables; see
`notes/mip-binary-lower-bound-extensions.md`.

Assessment. The mathematical content is elementary (a projection argument, a measure
count, and one integral), and the univariate statement in particular could be regarded as
folklore among people working on logarithmic formulations. Its possible contributions are:
the exact optimality `E_max = 2^{-2p-2}` of the sawtooth relaxation over the full class of
MIP relaxations; the general strongly convex/concave version with bounded integers; and
the two-sided estimate `0.0901 · 2^{-p} <= E_max <= 0.25 · 2^{-p}` for `xy`, showing that
`log2(1/ε) + O(1)` binaries are necessary and sufficient for the product, with the additive
constant pinned to within 2. Priority is unverified.

## Sources

- B. Beach, R. Burlacu, A. Bärmann, L. Hager, R. Hildebrand, "Enhancements of
  discretization approaches for non-convex mixed-integer quadratically constrained
  quadratic programming: Part I", Comput. Optim. Appl. 87(3):835–891 (2024),
  doi:10.1007/s10589-023-00543-7, arXiv:2211.00876; open copy
  https://www.econstor.eu/bitstream/10419/315244/1/10589_2024_Article_543.pdf. Locators
  (journal pagination): formulation `P^IP` p. 839; Definition 2 (MIP relaxation) p. 840;
  Definition 3 (error) pp. 840–841; Sect. 3.2, eq. (6) and Proposition 1 p. 842; `S_L`,
  eqs. (7)–(8) pp. 842–843; Definition 4 (sawtooth approximation, eq. (10)) p. 844;
  Definition 5 (sawtooth relaxation, eqs. (11)–(12)) p. 845; Definition 6 (sawtooth
  epigraph relaxation, eqs. (14)–(15)) p. 846; Definition 7 (tightened sawtooth relaxation,
  eqs. (16)–(17)) p. 847; Definitions 8–9 (Bin2, Bin3) p. 848; Definition 10 (HybS,
  eq. (21)) p. 849; Table 1 and Remark 4 p. 850; Sect. 5.1.1 (errors `2^{-2L-2}`,
  `2^{-2L-4}`) and Proposition 2 pp. 851–852; McCormick error p. 852; Sect. 5.1.2 and
  Proposition 3 p. 853; Propositions 4–5 and Remark 5 p. 854.
- B. Beach, R. Burlacu, A. Bärmann, L. Hager, R. Hildebrand, "Enhancements of
  discretization approaches for non-convex mixed-integer quadratically constrained
  quadratic programming: Part II", arXiv:2302.01164v1 (2023),
  https://arxiv.org/html/2302.01164v1. Locators: Definition 5 (NMDT) Sect. 4.1;
  Definition 8 (D-NMDT) Sect. 4.2; Propositions 1–2 (errors `2^{-L-2}`, `2^{-2L-2}`)
  Sect. 5.1; Table 1 Sect. 5.
- B. Beach, R. Hildebrand, J. Huchette, "Compact mixed-integer programming relaxations in
  quadratic optimization", J. Global Optim. (2022), arXiv:2011.08823 (sawtooth error
  `2^{-2L-2}` attributed to Yarotsky, p. 5 of the arXiv version).
- D. Yarotsky, "Error bounds for approximations with deep ReLU networks", Neural Networks
  94:103–114 (2017), Proposition 2.
- J. P. Vielma, G. L. Nemhauser, "Modeling disjunctive constraints with a logarithmic
  number of binary variables and constraints", Math. Program. 128:49–72 (2011).
- S. Fiorini, T. Rothvoss, H. R. Tiwary, "Extended formulations for polygons", Discrete
  Comput. Geom. 48:658–668 (2012).
- G. M. Ziegler, *Lectures on Polytopes*, Springer 1995, Sect. 1.2 (Fourier–Motzkin).
- L. C. Evans, R. F. Gariepy, *Measure Theory and Fine Properties of Functions*, CRC 1992,
  Sect. 2.2 (isodiametric inequality).

## Files

- `code/mip_relaxation_binaries/check_bounds.py` — numerical checks described above.


## Lean verification: scalar scope in topic 20

The [topic 20 coverage map](../formal/topics/20-scalar-quadratic/COVERAGE.md)
and [verification record](../formal/topics/20-scalar-quadratic/VERIFICATION.md)
identify the exact verified statements and final targeted checks. This is a
separate record from the dated numerical checks and source comparisons above.

For the square, Lean proves the exact threshold
`max{0,ceil[(log2(1/ε)-2)/2]}` for every `ε>0`, both for arbitrary convex lifts
with unrestricted integer coordinates and for finite binary linear lifts.
The lower proof uses parity, a finite grid and pigeonhole;
it requires neither closedness nor attainment of a largest parity interval.
The matching construction is an actual affine row system with `p` binaries,
`2+2p` real auxiliary coordinates and `11+10p` rows, including the unit-domain
bounds. Its error is `2^(-2p-2)` and that error is attained.

The square epigraph has an actual zero-binary finite linear folding lift.
The separate inequality-count theorem proves
`M >= (1/2)log2(1/ε)-1` for every finite linear extended formulation of a
square epigraph relaxation, with arbitrary continuous dimension, affine
subspace constraints and lineality. These size statements count actual rows,
not abstract convex-set descriptions.

Topic 20 also proves the exact one-sided product error `2^(-2p-2)` for
arbitrary convex integer lifts and finite linear lifts with arbitrarily small
positive extra error at the same binary count. This does not formally certify
the distinct whole-product-graph constant `1/(16 ln 2)` in part (B), the NMDT
claims, novelty statements, or every result in this source note.
