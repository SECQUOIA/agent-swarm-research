# Row hull Theorem 2: overlap check against Kim–Tawarmalani–Richard and Padberg–Van Roy–Wolsey

Date: 2026-09-21. Scope: focused literature check of Theorem 2, 2(b), 2(c) of
[the row-hull note](../results/row-hull-separable-concave.md). No existing file
was edited. No code was run; the two reductions below are short algebra.

## Main findings

1. **Kim–Tawarmalani–Richard (KTR) do not imply Theorem 2**, not even for
   identical `gamma_i`. Their invariance is permutation of `x` with the other
   variables held fixed. The row-hull set is invariant only under simultaneous
   permutation of the pairs `(z_i, tau_i)`. What KTR do imply in the identical
   case is the envelope of the *sum* `sum_i gamma(z_i)` over `X`, and that
   envelope is the constant `delta = gamma(r)`, which is trivial.
2. **Theorem 2 is, up to an affine change of variables, the constant-capacity
   complete description of Padberg, Van Roy and Wolsey (PVW, 1985)** for the
   equality single-node flow set in which every arc has an indicator. The
   reduction needs only Proposition 1 of the note (only `gamma_i(r)` matters)
   and is given below. This is a closer overlap than the note currently
   states ("concave-cost counterpart of PVW"). I did not see this reduction in
   any source; it is my derivation, and it relies on a secondary statement of
   the PVW theorem (see "Access").
3. **Theorem 2(c) with linear variable costs is exactly the PVW description.**
   With concave variable costs *and* indicators, 2(c) is not a direct corollary
   of PVW as far as I can see.

## 1. Kim, Tawarmalani, Richard (Math. Oper. Res. 47 (2022); arXiv:1910.02573)

Read: arXiv PDF (preprint dated 10 August 2021, 38 pages), Sections 2 and 4 in
full, the rest by theorem list.

### Statements (quoted from the arXiv version)

Definition (Section 2): "a set `S ⊆ {(x, z) ∈ R^n × R^p}` is called
permutation-invariant with respect to `x` if `(x, z) ∈ S` implies that
`(P x, z) ∈ S` for all permutation matrices `P ∈ P_n`."

> **Theorem 2.1.** Suppose `S ⊆ {(x, z) | R^n × R^p}` is permutation-invariant
> with respect to `x ∈ R^n`. Then,
> `conv(S) = X := {(x, z) | (u, z) ∈ conv(S_0), u ≥_m x}`,
> where `S_0 = S ∩ {(u, z) | u_1 ≥ ··· ≥ u_n}`.

Theorem 2.2 is the same result with `u ≥_m x` written as a linear system with
`O(n^2)` extra variables. Theorem 2.4(1) allows several blocks
`x^1, ..., x^m`, each permuted **independently**
("`S` is a permutation-invariant set with respect to `x^k` for `k = 1,...,m`"),
with `u^k ≥_m x^k` for each block.

> **Lemma 4.1.** Let `φ : P → R` be a Schur-concave function, where `P ⊆ R^n`
> is a permutation-invariant polytope. Let
> `M := {x ∈ P | there is no u ∈ P with u ≥_m x and u_Δ ≠ x_Δ}`. Let
> `S := {(x, φ) | φ(x) ≤ φ ≤ α, x ∈ P}` and
> `X := {(x, φ) | φ(x) ≤ φ ≤ α, x ∈ M}`. Then `conv(S) = conv(X)`.

> **Proposition 4.1.** Consider a function `φ(x) : R^n → R` that is
> Schur-concave over `[a, b]^n` and let
> `S^α := {(x, φ) | φ(x) ≤ φ ≤ α, x ∈ [a, b]^n}`. For any `x ∈ [a, b]^n`, define
> `S(x) = sum_i (x_i − a)`. For any `s ∈ [0, n(b − a)]`, let
> `i_s = max{i | i(b − a) < s}` and `u^s_i = b` if `i ≤ i_s`,
> `u^s_i = a + s − (b − a) i_s` if `i = i_s + 1`, `u^s_i = a` otherwise. Let
> `Θ^α := {(x, φ) | φ(u^{S(x)}) ≤ φ ≤ α, x ∈ [a, b]^n}`. Then
> `conv(S^α) = conv(Θ^α)`. Moreover, if `φ` is component-wise convex then
> `Θ^α` is convex.

> **Theorem 4.1.** Let `a, b ∈ R`, `Z ⊆ {(x, z) | x ∈ R^n, z ∈ R^m}` be a
> compact permutation-invariant set with respect to `x`, and
> `F = {F_1, ..., F_r}` be a collection of faces of `[a, b]^n` such that
> `conv(S(Z, a, b)) = conv(X(Z, a, b, F))`. Moreover, assume that
> `conv(X(Z, a, b, {F_i}))` has a polynomial-sized compact extended formulation
> for each `F_i ∈ F`. Then `conv(S(Z, a, b))` has a polynomial-sized extended
> formulation.

Corollary 4.1 makes this explicit: only the `O(n^2)` "hole-free" faces
(`u(F) = {1..p}`, `l(F) = {q..n}`) are needed, combined by disjunctive
programming and `u ≥_m x`. Proposition 4.2 gives the envelope of a
permutation-invariant function that is vertex generated over `[a, b]^n` as
`min{f(u) | u ≥_m x, b ≥ u_1 ≥ ··· ≥ u_n ≥ a}` with `f` affine. The paper notes
after Corollary 4.1 that "Theorem 4.1 allows `z` to be multi-dimensional", which
gives simultaneous convexification of several symmetric functions of `x`.

### Answers

**(a) Vector of epigraph variables `tau_i`: not handled.** In every KTR
result the extra variables `z` are fixed when `x` is permuted. In the row-hull
set `{(z, tau) : z ∈ X, tau_i ≥ gamma(z_i)}` the variable `tau_i` is attached
to coordinate `i`; the set is invariant only under the diagonal action
`(z_i, tau_i) → (z_π(i), tau_π(i))`. It is not permutation-invariant with
respect to `z` in KTR's sense, and Theorem 2.4(1) (independent permutation of
two blocks) does not apply either, because permuting `z` and `tau` separately
leaves the set. KTR's proof of convexity of the majorization description
(Lemma 2.3) uses the sorted copy `u` of a single vector; I see no immediate
analogue for pairs (it would need matrix majorization, which is not in the
paper). The "multi-dimensional `z`" remark covers several symmetric functions
of the whole vector `x` (for example all elementary symmetric polynomials), not
one function per coordinate.

**(b) Item-dependent functions: not handled.** Item-dependent `gamma_i` or
weights break the invariance; nothing in the paper addresses this. (This
confirms what the note already says.)

**(c) Sum constraint with non-integer `B/w`: handled in principle, for the
aggregated function only.** Lemma 4.1 is stated for any permutation-invariant
polytope `P`, and `X = {z ∈ [0,w]^n : sum z_i = k w + r}` is one. Theorem 4.1
also allows a sum constraint inside `Z`, with `F` the edges of the cube. But
the paper contains no explicit result for this slice; Proposition 4.1 is for
the full cube.

**What KTR imply in the identical case.** Take one epigraph variable
`T ≥ φ(z) := sum_i gamma(z_i)`. `φ` is symmetric and concave, hence
Schur-concave. In `P = X` every point is majorized by
`u^B = (w,...,w, r, 0,...,0)`, so `M` is the set of permutations of `u^B`, that
is, the vertices of `X`. Lemma 4.1 gives
`conv{(z, T) : z ∈ X, T ≥ φ(z)} = {z ∈ X, T ≥ gamma(r)}`: the envelope is the
constant `delta`. This agrees with Theorem 2: for identical `delta_i = delta`,
(EF) gives `sum_i tau_i ≥ delta sum_i zeta_i = delta`. It also follows from the
Falk–Hoffman vertex argument alone, because `φ` takes the same value at every
vertex of `X`. So in the symmetric aggregated case there is nothing to prove,
and KTR do not reach the content of Theorem 2, which is the joint hull of the
*vector* `tau` and item-dependent `delta_i`.

## 2. Padberg, Van Roy, Wolsey (Oper. Res. 33 (1985) 842–861)

### What their result is

Abstract (via OpenAlex; the INFORMS page returned 403): "we consider the mixed
integer programs whose feasible region `X` is composed of (i) a simple additive
constraint in the continuous variables `x_j`, for `j = 1, ..., n` and (ii)
constraints `0 ≤ x_j ≤ m_j y_j` defined by binary variables `y_j` for
`j = 1, ..., n`. [...] We derive two classes of facet-defining linear
inequalities of the convex hull of `X`, and show that the second of these
classes gives a complete description of the convex hull when `m_j = m` for all
`j`."

So: **every arc has an indicator.** The abstract does not say whether the row
is an equality. Atamtürk, Gómez, Küçükyavuz (*Three-partition flow cover
inequalities for constant capacity fixed-charge network flow problems*,
Networks 2016, preprint on Atamtürk's site, Section 2) state it precisely. In
their notation (`x` binary, `y` flow, capacity `c`):

> `X := {(x, y) ∈ B^n × R^n_+ : y(N^+) − y(N^−) = d, y_j ≤ c x_j, j ∈ N}`, and
> let `X_≤` be the relaxation where the equality is replaced with an inequality.
> [...] Padberg et al. [10] studied the convex hull of `X` and `X_≤`. [...] the
> lifted flow cover inequality
> `sum_{j∈S^+} (y_j + ρ(1 − x_j)) − sum_{j∈N^−} min{y_j, (c − ρ) x_j} + sum_{j∈N^+\S^+} max{y_j − ρ x_j, 0} ≤ d`   (4)
> is also valid for `X_≤` and `X`. Moreover, inequalities (4) together with the
> flow conservation and bound constraints completely describe the convex hull
> of `X`.

Here `λ = c|S^+| − d > 0`, `ρ = (c − λ)^+`. So the complete description is for
the **equality** set, with indicators on all arcs. Atamtürk (ORL 29, 2001)
says PVW treat the case `N^− = ∅`; the statement with `N^−` is the reflected
form. I found no precise statement of a complete description for `X_≤`.

### Theorem 2(c) with linear variable costs equals the PVW description

With linear costs `gamma_i = 0`, the third entry is omitted and the 2(c)
inequality is `sum_i min{z_i/r, (w y_i − z_i)/(w − r)} ≥ 1`. Select the second
entry on `C` and the first on `N \ C`, substitute
`sum_{N\C} z_i = k w + r − sum_C z_i`, and multiply by `r(w − r)/w`:

```
sum_{i in C} z_i + r sum_{i in C} (1 - y_i) <= k w + r + r (|C| - k - 1).
```

- `|C| = k+1`: the flow cover inequality (`λ = w − r`, `ρ = r`).
- `|C| > k+1`: write `C = S ∪ L`, `|S| = k+1`. This is (4) with the terms
  `max{z_j − r y_j, 0}` selected on `L`.
- `|C| ≤ k`: implied by `z_i ≤ w y_i`, `y_i ≤ 1`.

So the selections of 2(c) with `gamma = 0` are exactly the PVW lifted flow
covers (4) for `N^− = ∅`, and 2(c) reduces to the PVW theorem. The min-sum
form packs the exponential family into one inequality; that packaging, and the
extended form (EF), I did not find stated in the sources I could read, but it
is a restatement, not a new hull.

### Theorem 2 itself follows from PVW plus Proposition 1

By Proposition 1, `Q` depends on `gamma_i` only through its values at vertex
coordinates `{0, r, w}`, that is, only through `delta_i = gamma_i(r)`. Replace
`gamma_i` by the chord gap of a fixed charge `h_i` on `[0, w]`:
`g_i(z) = h_i (1 − z/w)` for `z > 0`, `g_i(0) = 0`, with
`h_i = delta_i w/(w − r)`, so that `g_i(r) = delta_i`. Then `Q` is unchanged.
For the PVW set put `tau_i = h_i (y_i − z_i/w)`. This affine map sends the PVW
points onto `{(z, tau) : z ∈ X, g_i(z_i) ≤ tau_i ≤ h_i(1 − z_i/w)}`, whose
upward closure in `tau` is the generating set of `Q`. Under the map,

```
(w y_i - z_i)/(w - r) = tau_i / delta_i,     y_i <= 1  <=>  tau_i/delta_i <= (w - z_i)/(w - r),
```

so the PVW description becomes `z ∈ X`, `tau ≥ 0`,
`tau_i/delta_i ≤ (w − z_i)/(w − r)`, `sum_i min{z_i/r, tau_i/delta_i} ≥ 1`, and
taking the upward closure in `tau` (replace `tau_i` by
`min{tau_i, delta_i (w − z_i)/(w − r)}`) gives exactly (RH). Items with
`delta_i = 0` are arcs without fixed charge, that is, `y_i = 1` fixed.

Hence **Theorem 2 = Falk–Hoffman vertex argument + PVW constant-capacity
equality description + an affine change of variables.** In the other
direction, PVW's equality result is the special case of Theorem 2 in which each
`gamma_i` is a fixed-charge gap. The two statements are equivalent in content.
The note's TU proof is short and self-contained, and may well differ from
PVW's proof (not checked), but the polyhedron is the same.

Consequences for other parts of the note:

- *Tilted flow covers (Lim–Linderoth–Luedtke).* Under the same map their
  tilted inequalities at equal capacities are images of PVW lifted flow
  covers. The note's strictness witness (`F = N` missing) corresponds to a
  lifted flow cover with `|C| > k+1`, which is in PVW's complete family but not
  among the simple covers.
- *Theorem 2(b).* By the same map it is equivalent to a complete description of
  the constant-capacity inequality set `X_≤` with indicators on all arcs. PVW
  studied `X_≤` (per Atamtürk et al.), but I could not confirm that they, or
  Nemhauser–Wolsey Section II.2.4, state a complete description for it. Status:
  not verified either way.
- *Theorem 2(c) with concave variable costs.* Each arc then carries two
  independent quantities (`y_i` and `tau_i`) and four generator types
  `(0,0,0), (0,1,0), (w,1,0), (r,1,delta_i)`. I see no affine map to the PVW
  set, so this part is not a direct corollary. Its proof is the same bipartite
  TU argument.

## 3. Other sources

From the papers' abstracts and my knowledge of them; full texts of the two
Math. Program. papers were not fetched.

- **Tawarmalani, Richard, Chung (Math. Program. 124, 2010), orthogonal
  disjunctions.** Hull of a union of sets lying in orthogonal subspaces, in the
  form "sum of one concave function per block `≥ 1`". For `k = 0` the vertices
  `r e_j` with gap vectors `delta_j e_j` are orthogonal and (RH) is of this
  type (the note already says this). For `k ≥ 1` the vertices
  `w 1_S + r e_j` are not orthogonal, so the result does not apply, although
  (RH) has the same outward form.
- **Tawarmalani, Richard, Xiong (Math. Program. 138, 2013), polyhedral
  subdivisions.** Envelopes of a single function over a hyper-rectangle (or
  subsets of it obtained from the subdivision), for functions that are
  concave-extendable from vertices, for example supermodular ones via the Kuhn
  triangulation. One epigraph variable, no row constraint. Does not cover the
  claim.
- **Meyer–Floudas (edge-concave, 2005), Tardella (2008), Locatelli (envelopes
  over simplices and polytopes, mostly low dimension or quadratic),
  Bao–Khajavirad–Sahinidis–Tawarmalani (multilinear over boxes, 2015).** All
  concern the envelope of one function, mostly over boxes. Falk–Hoffman and
  Tardella give vertex generation (the note's Proposition 1) but no closed form
  on the slice. A web search for envelopes of separable concave functions over
  hypersimplex-like slices returned nothing relevant; this is weak evidence.
- **Wolsey, Yaman (Math. Program. 187, 2021), "Convex hull results for
  generalizations of the constant capacity single node flow set".** Extends the
  PVW constant-capacity result (extreme points, extended formulations,
  projection). Abstract only; full text not accessible. It should be cited and
  checked, since its generalizations may cover 2(b) or 2(c)-like sets.

## 4. Assessment and suggested wording

Already implied by the literature:

- Theorem 2 (equality row, equal widths, arbitrary item-dependent concave
  `gamma_i`): equivalent to PVW (1985) for the constant-capacity equality
  single-node flow set, via Proposition 1 and `tau_i = h_i (y_i − z_i/w)`. The
  set of facets is PVW's lifted flow covers.
- Theorem 2(c) with linear variable costs: exactly PVW.
- The identical-`gamma` aggregated envelope (constant `delta`): trivial, and
  also a consequence of KTR Lemma 4.1.

Apparently not in these sources:

- The observation that the row hull of *arbitrary* concave terms on an
  equal-width row is the PVW polyhedron in disguise (I did not find this
  stated; Lim–Linderoth–Luedtke do not claim a complete description).
- The single min-sum inequality (RH), the `n`-variable extended form (EF) and
  `O(n)` separation as a presentation of that polyhedron.
- Theorem 2(c) with both indicators and concave variable costs.
- Theorem 2(b): unverified; could be in PVW or Nemhauser–Wolsey.
- Nothing in KTR covers the vector-`tau` hull or item-dependent terms.

Suggested wording for the note: do not call Theorem 2 new without
qualification. Say instead, for example: "Theorem 2 is equivalent, through the
vertex argument of Proposition 1 and the substitution
`tau_i = h_i (y_i − z_i/w)`, to the complete description of the
constant-capacity single-node flow set with equality row by Padberg, Van Roy
and Wolsey (1985); its linearizations are their lifted flow cover
inequalities. What we add is the observation that this description is the row
hull of arbitrary separable concave terms, the single-inequality form (RH) with
its compact extended form, and the extension 2(c) to indicators with concave
variable costs. Kim, Tawarmalani and Richard (2022) treat sets invariant under
permutation of `x` alone; they give the (constant) envelope of the sum for
identical terms but not the joint hull of the vector of terms." The sentence in
"Relation to tilted flow covers" that calls Theorem 2 "the concave-cost
counterpart" of PVW should be replaced by the equivalence, and the claim
paragraph in "Literature" adjusted accordingly.

## Access

- Read in full text: KTR arXiv:1910.02573 (PDF); Atamtürk–Gómez–Küçükyavuz
  preprint (`atamturk.ieor.berkeley.edu/pubs/TPInequalities.pdf`); Atamtürk,
  ORL 29 (2001) (only its one-sentence description of PVW used).
- Abstract only: PVW 1985 (OpenAlex; INFORMS returned 403); Wolsey–Yaman 2021
  (RePEc summary; Springer and the KU Leuven repository link failed).
- Not accessed: full text of PVW 1985, so the equality-row completeness claim
  rests on Atamtürk et al.'s statement and the PVW abstract; Nemhauser–Wolsey
  Section II.2.4; Tawarmalani–Richard–Chung 2010 and Tawarmalani–Richard–Xiong
  2013 (Springer paywall; characterized from abstracts and memory);
  Meyer–Floudas, Locatelli, Bao et al. (from memory only).
- An unsuccessful search does not establish novelty of the parts listed as
  "apparently not in these sources".
