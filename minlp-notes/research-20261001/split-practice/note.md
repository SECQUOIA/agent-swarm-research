# Split separation in practice: ranks, violations and exact separators at SDP points

Date: 2026-10-01 to 2026-10-03. Stream: `split-practice` of the
[October 1 continuation](../PROGRAM.md). **Final status (2026-10-04): reviewed
in two rounds; r2 minor fixes applied; the last revision's fixes checked by
the coordinating agent; not refereed.**
The [independent round-1 review](reviews/review-r1.md) found one major
implementation/framing problem and minor issues. The
[independent round-2 review](reviews/review-r2.md) confirmed their resolution
and found one minor non-root reporting issue and optional improvements;
this revision addresses those findings. The coordinating agent reran
`check_nonroot_r2.py` and `summarize_revision_r2.py`.
Repository sweeps outside this program included program files in commits.
This program makes no commits; this revision makes no commits, staging or
branch changes. A first
author agent was cut off by a usage limit on 2026-10-02 around 05:05 UTC;
this note was written by a second agent that checked the first agent's code
and outputs, reran what was invalid, and finished the work (§11 lists what was
reused and what was rerun). A closeout author checked the completed shards
and reconciled the note with the logs on 2026-10-03; this was an author check,
not an independent review.

## Summary

On 187 new draws from the Buchheim–Traversi (BT) and de Meijer et al. (DM)
ternary QP generators, SDP root optima have numerical rank 1–5. After the
implemented de Meijer families, 171 points are numerically rank 1 and integral;
the 12 selected residual-gap instances have rank 9–39. Eleven have
established numerical gaps above 0.01%; `dm_LIN_t3_n60_p75_s0` has only
an upper bound on its gap because its optimum remains unresolved (§9.1).
Trace and random re-optimization of their approximate optimal faces did not reduce rank.
*(Numerical evidence, not a rank theorem.)*

The original Theorem 3 implementation’s enormous coefficients came from
unreduced integer elimination and floating-point kernel shortening. Exact
reduction removes that blow-up at the selected roots (§8). At all nine
fractional rank-1 roots, a separate exact affine-LLL check finds a most-violated
split of the grid neighbour with coefficients at most 4, violated by `0.25`
to six decimals at the stored point. The practical objection is the raw
objective: these maximizers have much smaller normalized violation than the
elementary and pair splits. Normalized enumeration finishes on 103 of 123
selected points; Lemma A certifies another 17 capped searches numerically,
so 120 of 123 are finished or certified. Only three capped results remain
heuristics (§8).

Adding `{0,±1}` splits of support at most 3 to the implemented de Meijer families
closes the gap on 6 of the 12 selected instances. Adding general splits
closes it on 4 more.
Two DM60 instances yield dense splits but little bound improvement before
the budget expires. The worst-case reduction reproduces expensive separation
at orders 62–77, but its tiny violations and full rank differ from the
benchmark points. A solver should enumerate three-index splits first, then
try normalized general separation under a budget and validate each cut at
the original point. These experiments measure root bounds, not total
branch-and-bound performance (§12).

## 1. Question and starting point

The [split note](../../research-20260928b/side-results/split-separation-np-complete.md)
proved that separating split inequalities
`q_Y(v) := ⟨v(v+e₀)ᵀ, Y⟩ ≥ 0`, `v ∈ ℤᴺ`, for integer QP is strongly
NP-complete, even at positive definite points that satisfy all of de Meijer et
al.'s cut families (its Corollary 5). It also proved that separation is
fixed-parameter tractable in `r = rank Y` (Theorem 3) and has a closed form at
rank 1 (Theorem 4). Its §8 left open whether any of this matters at the
points a solver actually separates. This stream asks:

1. What do SDP relaxation optima of benchmark-like ternary QPs look like:
   numerical rank, lower-rank optimal solutions, and violated splits?
2. Is exact separation practical there, in particular at low rank?
3. Do the hard cases of the split note occur at such points?
4. What should a solver do?

Notation follows the split note. `Y = [[1, xᵀ], [x, X]]` has order
`N = n + 1`, index 0 is the constant, `v = (v₀, w)` with `w ∈ ℤⁿ`, and the
split disjunction is `wᵀx ≤ s ∨ wᵀx ≥ s + 1` with `v₀ = −s − 1`. Ranks are
counted as the number of eigenvalues larger than `τ·λ_max(Y)`, for
`τ ∈ {10⁻³, 10⁻⁵, 10⁻⁷, 10⁻⁹}`; "rank" without qualification means
`τ = 10⁻⁵`. The *violation* of `v` is `−q_Y(v)`, and its *normalized
violation* is `−q_Y(v)/‖w‖²`.

## 2. Literature recheck (2026-10-02)

Sources and checksums are in [`sources/MANIFEST.md`](sources/MANIFEST.md).

- **de Meijer, Piccialli, Sotirov, Sudoso**, *Beyond binarity: Semidefinite
  programming for ternary quadratic problems*, arXiv:2603.28979. The arXiv
  abstract page fetched on 2026-10-01 and again on 2026-10-02 lists only v1
  (30 March 2026); the page is byte-identical (same sha256). The Optimization
  Online record (posted 30 March 2026) gives no revision and no code or data
  link. Semantic Scholar lists no citing paper (2026-10-02). Locators used
  here: §4 p. 11 (split inequalities; "it is unclear whether the separation of
  split inequalities is an NP-hard problem or not"), (2.1)–(2.3), (4.1),
  (4.3)–(4.12), (5.2)–(5.4), §6.4 (cutting-plane rules: tolerance 10⁻³, at
  most 5000 cuts per round, stop when fewer than `n` violated cuts are found),
  §7 (instances with `n ∈ {60, …, 120}`), Appendix A (generators). The task
  text refers to an "SDP-based branch-and-bound for ternary or integer QP,
  2026"; this arXiv paper is the only 2026 de Meijer et al. paper found, and
  it is the one the split note used.
- **Buchheim and Traversi (B–T)**, Optimization Online 2013/07/3953, preprint
  dated 21 February 2013; published in Discrete Optim. 15 (2015) 1–14
  (Crossref record checked; full text not open). Locators: problem (7), §4
  (separation by convex integer QP; Algorithm 1 for non-psd points), §6.1
  (instances: `n = 10`, `p` negative eigenvalues, 10 seeds; Tables 1–2), §6.2
  (`n = 20…50`; "conducting the separation until the end is not doable in
  practice").
- **Burer and Letchford**, Math. Program. 143 (2014) 231–256; only the 2011
  Optimization Online preprint (3172) is open; it poses the complexity of
  split separation as a question (§8). The published version was not read.
- **Letchford**, *Integer quadratic quasi-polyhedra*, IPCO 2010 (author copy).
  It introduces the split inequalities and proves that linear optimization
  over `IQₙ` is strongly NP-hard (Prop. 3, via CVP). It contains no
  separation result and asks in its concluding remarks whether split
  separation can be solved in polynomial time.
- **Buchheim, Montenegro, Wiegele**, *SDP-based branch-and-bound for
  non-convex quadratic integer optimization*, arXiv:1901.10335 (2019). Found
  in the search; it is about solving the SDP duals, not split separation.
- **Complexity claims, 2025–2026.** Web searches (WebSearch, standard and
  extended modes), the arXiv API (`all:"split inequalities"`, newest first)
  and the Semantic Scholar citation lists of B–T 2015 (12 entries, unchanged
  since 2026-10-01) and of de Meijer et al. (none) found no 2025–2026 claim
  about the complexity of split separation for integer QP. The only new
  related complexity paper found is Herrmann, *Integer Quadratic Programming
  is W[1]-Hard Parameterized by the Number of Variables*, arXiv:2608.17818v1
  (18 August 2026). It concerns linearly constrained IQP with general `Q` and
  says nothing about split separation. It does not conflict with Theorem 3 of
  the split note: split separation is an unconstrained convex integer QP,
  that is, a closest vector problem, which is fixed-parameter tractable in the
  dimension (Kannan).

An unsuccessful search does not establish novelty. The binary analogue
(hypermetric, gap-1, rounded psd) is covered by the
[`binary-separation`](../binary-separation/note.md) stream and is not
discussed here.

## 3. Instances and relaxations

**No published instance files.** Neither B–T nor de Meijer et al. publish
instance files or seeds (B–T §6.1; de Meijer et al. Appendix A and the
Optimization Online record). Both describe random generators precisely, so
the closest open equivalent is to draw from the stated distributions with our
own seeds ([`code/instances.py`](code/instances.py)):

- **BT**: B–T §6.1. `p` eigenvalues from `U[−1,0]`, `n − p` from `U[0,1]`,
  eigenvectors from orthonormalized `U[−1,1]` vectors, linear term from
  `U[−1,1]`, `x ∈ {−1,0,1}ⁿ` (B–T speak of ternary instances; bounds
  `−1 ≤ x ≤ 1`). Sets: BT10 = all 110 instances (`p = 0…10`, seeds 0–9, as in
  B–T); BT20 and BT30 = `p ∈ {0, n/5, …, n}`, seeds 0–2 (18 each); BT50 =
  `p ∈ {0,10,25,40,50}`, seed 0 (5).
- **DM**: de Meijer et al. Appendix A, QUTO and TQP-Linear (`1ᵀx = 0`), Types
  1–3, `p ∈ {25,50,75}`, seed 0; sets DM30 and DM60 (18 each). Substitutions:
  their sizes start at `n = 60`; we use `n = 30` and `n = 60` because each SDP
  is solved by cvxpy/Clarabel rather than MOSEK. For Type 2, "each remaining
  entry is nonnegative with probability p/100 and zero otherwise" is read as
  `U[0,1]` with probability `p/100`. TQP-Ratio instances are not used.

Optimal values: brute force for `n ≤ 12`; otherwise the Gurobi 13.0.2
command line, nonconvex MIQP, 300 s, 1 thread
([`code/gurobi_opt.py`](code/gurobi_opt.py), `logs/opt_gurobi.jsonl`). All
BT20–BT50 and DM30 instances and 11 of 18 DM60 instances were solved to
optimality; 7 DM60 instances hit the time limit, and there the best of the
Gurobi incumbent and any integral SDP point is used, so gaps reported for
them are upper bounds. The earlier author reported three small brute-force
cross-checks of Gurobi, but no dedicated output for them is retained here;
they are not counted as independently reproduced checks.

**Relaxations** ([`code/sdp.py`](code/sdp.py)). BT base: B–T's SDP relaxation
(`Y ⪰ 0`, `Y₀₀ = 1`, `x ∈ [−1,1]ⁿ`, `diag X ∈ [0,1]ⁿ`). DM base: de Meijer et
al. (4.1), with (5.2) for QUTO and the facially reduced form of (5.4) for
TQP-Linear (`Y = WZWᵀ`, `Z ⪰ 0`, so `⟨J,X⟩ = 0` holds exactly). Cut families,
checked against the arXiv text: triangle (2.1)–(2.2), pair (2.3), RLT
(4.5)–(4.8), 1-index split (4.3), 2-index split (4.11)–(4.12) and a
local-search heuristic for pentagonal odd-set inequalities ((4.4) with
`|S| = 5`). The "de Meijer loop" adds up to 5000 most violated cuts with
tolerance 10⁻³ per round until none is violated (at most 40 rounds); BT
instances use triangle, pair, RLT and the 1- and 2-index splits, DM
instances use triangle, pair, RLT, 2-index splits and pentagonal cuts. This
differs from their §6.4 stopping rule (fewer than `n` violated cuts); we run
to zero violated cuts to get a well-defined point. Heptagonal cuts are not
used.

**Points.** For every instance the following points are stored in
`data/points_SET/`: the root optimum (`root`), the optimum after the de Meijer
loop (`cut`), and two re-optimizations over the approximate optimal face of
the final relaxation, minimizing `trace Y` (`cut_trace`) or `⟨W, Y⟩` for a
random psd `W` (`cut_rand`), with objective at most `opt + 10⁻⁷(1+|opt|)`
([`code/exp_points.py`](code/exp_points.py)). The trace heuristic is the usual
attempt to find a lower-rank optimal solution.

**Solver accuracy.** Clarabel was asked for tolerance 10⁻⁹. It often returns
`optimal_inaccurate` (reduced accuracy, roughly 10⁻⁵ to 10⁻⁸): for 27 of 187
root solves and 180 of 187 final solves. Eigenvalues below about
`10⁻⁷·λ_max` are therefore noise, and ranks at `τ = 10⁻⁷, 10⁻⁹` are not
reliable. The conclusions below use `τ = 10⁻³` and `10⁻⁵` and are checked
against eigenvalue gaps.

## 4. Proved statements

These statements explain the measurements. Their algebraic identities and
finite constructions are checked in exact rational arithmetic by
[`code/check_props.py`](code/check_props.py); the tests do not replace proofs.

**Lemma A (best right-hand side).** Let `Y` be symmetric with `Y₀₀ = 1`,
`S := X − xxᵀ`, `v = (v₀, w)` and `t := wᵀx`. Then
`q_Y(v) = (v₀ + t)(v₀ + t + 1) + wᵀSw`, and
`max_{v₀∈ℤ} (−q_Y(v₀, w)) = φ(t) − wᵀSw` with `φ(t) := {t}(1 − {t}) ∈ [0, ¼]`.
If `Y ⪰ 0`, then `S ⪰ 0`, so `w` gives a violated split if and only if
`wᵀSw < φ(wᵀx)`, and its normalized violation is at most `1/(4‖w‖²)`.
*(Proved.)*

*Proof.* Expand `q_Y(v) = v₀² + 2v₀t + v₀ + wᵀXw + t` and use
`wᵀXw = wᵀSw + t²`. Over `v₀ ∈ ℤ`, `u = v₀ + t` ranges over `t + ℤ`, and
`u(u+1)` is smallest at `u = {t} − 1` when `0 < {t} < 1`, giving
`−{t}(1 − {t})`; when `{t} = 0`, both `u = −1` and `u = 0` minimize it.
`S ⪰ 0` is the Schur complement of `Y₀₀ = 1`. ∎

This makes every `{0,±1}` family with `|supp w| ≤ k` enumerable in
`O(nᵏ2ᵏ)` evaluations, each with the best `v₀` ([`code/exp_separate.py`](code/exp_separate.py),
`family_best`).

**Lemma B (non-primitive splits are dominated).** Let `w = kw′` with `k ≥ 2`
an integer and `w′ ∈ ℤⁿ`, `v = (−s−1, w)`, `t := ⌊(2s + 1 − k)/(2k)⌋`,
`v_t := (−t−1, w′)`, `v_{t+1} := (−t−2, w′)`. Then for every symmetric `Y`

`q_Y(v) = a·q_Y(v_t) + b·q_Y(v_{t+1}) + c·Y₀₀`, with
`b = ((2s+1)k − (2t+1)k²)/2`, `a = k² − b`, `c = (k(t+1) − s)(k(t+1) − s − 1)`,

and `a, b, c ≥ 0`. Hence if `v` is violated, so is `v_t` or `v_{t+1}`, and the
normalized violation of `v` is at most the larger normalized violation of
`v_t` and `v_{t+1}`. *(Proved.)*

*Proof.* With `z = w′ᵀx` and `Z = w′ᵀXw′`, the three split inequalities are
linear in `(Y₀₀, z, Z)`: `q(v) = k²Z − (2s+1)kz + s(s+1)Y₀₀` and
`q(v_t) = Z − (2t+1)z + t(t+1)Y₀₀`. Matching the coefficients of `Z` and `z`
gives `a + b = k²` and the stated `b`. The constant `c` is then fixed; since the
polynomial identity `g(z) = a·f_t(z) + b·f_{t+1}(z) + c` holds for
`g(z) = (kz − s)(kz − s − 1)` and `f_t(z) = (z − t)(z − t − 1)`, evaluating at
`z = t + 1`, where `f_t = f_{t+1} = 0`, gives `c = g(t+1) ≥ 0` because `g ≥ 0`
on ℤ. The choice of `t` gives `2tk ≤ 2s + 1 − k < 2tk + 2k`, i.e.
`(2t+1)k ≤ 2s+1 < (2t+3)k`, which is `0 ≤ b < k²`. Finally
`−q(v)/(k²‖w′‖²) ≤ (a(−q(v_t)) + b(−q(v_{t+1})))/(k²‖w′‖²)`. ∎

Lemma B is the one-dimensional fact that `conv{(z, z²) : z ∈ ℤ}` is described
by the elementary splits, transported along `w′`. We did not find it stated in
the sources, but it is elementary and probably known.

**Proposition C (the value ¼).** Let `Y ⪰ 0` with `Y₀₀ = 1`.

- (a) `q_Y(v) ≥ −¼` for all `v`, since `q_Y(v) = (uᵀYu − 1)/4` with
  `u = 2v + e₀` (split note, Lemma 1).
- (b) If `Y` is rational, the minimum of `q_Y` over `ℤᴺ` is attained, and it
  equals `−¼` if and only if `Yu = 0` for some `u ∈ e₀ + 2ℤᴺ`, that is, the
  integer kernel of `Y` meets `e₀ + 2ℤᴺ`.
- (c) If `Y = ℓ(x)` with rational `x ∉ ℤⁿ` and least common denominator `D`,
  the maximum violation is `⌊D²/4⌋/D² ≥ 2/9`, however close `x` is to `ℤⁿ`
  (split note, Theorem 4). For `x₁ = 1 − 1/D` the elementary split on `x₁` has
  violation `(D−1)/D²`, while `v = (−a, a·e₁)` with `a = ⌊D/2⌋` has violation
  `⌊D/2⌋⌈D/2⌉/D²`. For `D ≥ 4`, this `w = a·e₁` is non-primitive
  and its normalized violation is strictly smaller than the elementary one.
  For `D = 2, 3`, `a = 1`: it is the elementary split and the ratios agree.
- (d) If `Y = ℓ(x)` with some `xᵢ` irrational, `sup_v (−q_Y(v)) = ¼`.
  It is attained if and only if `wᵀx ∈ ½ + ℤ` for some `w ∈ ℤⁿ`.
  In particular it is not attained when `1,x₁,…,xₙ` are linearly independent
  over `ℚ`.

*(Proved.)* *Proof.* (b) For a common denominator `δ` of `Y`, the values
`uᵀYu` lie in `δ⁻¹ℤ_{≥0}`, so the minimum is attained; `uᵀYu = 0` if and only
if `Yu = 0` because `Y ⪰ 0`. (c) Theorem 4 of the split note gives
`q = m(m+D)/D²` with `m = pᵀv`, `p = D(1, x)`; here
`m = D(−a) + (D−1)a = −a`. `⌊D²/4⌋/D² ≥ 2/9` for `D ≥ 2` (equality at
`D = 3`). (d) `q = t(t+1)` with `t = v₀ + wᵀx`, and `wᵀx mod 1` is dense in
`[0,1)` when `xᵢ` is irrational (take `w = keᵢ`), so `t` comes arbitrarily
close to `−½`. Equality holds precisely when `v₀ + wᵀx = −½`.
An irrational coordinate alone does not exclude this: `x = (√2, ½)`
attains equality with `v₀ = −1`, `w = (0,1)`. ∎

*Consequence (heuristic, supported by §8).* The unnormalized maximum
violation, which is what B–T's problem (7) maximizes, is a poor criterion at
rank-deficient points. At the rational neighbours tested in §8 it is almost
always close to `¼`. Exact reduction removes the old implementation’s
coefficient blow-up at the roots (§8); even short raw maximizers can have much worse
normalized violation than elementary or pair splits. This is not a
general frequency claim: `check_props.py` [P2] finds exact `min q = −¼` in
only 21 of 140 random rank-deficient matrices. At a floating-point SDP
solution, large-coefficient splits can amplify tiny near-kernel errors.
Normalizing by `‖w‖²` controls this effect: by Lemma A every normalized
violation is at most `1/(4‖w‖²)`.

**Proposition D (a restricted family can be harder than the full family).**
At rank-1 rational points, exact separation over all splits is polynomial
(split note, Theorem 4), but deciding whether some 0/1 split
`v ∈ {0,1}^{n+2}` is violated is NP-complete. *(Proved; NP-complete in the
ordinary sense, from SUBSET SUM.)*

*Proof.* Given positive integers `a₁, …, aₙ, T`, put `xᵢ = −12aᵢ/5` for
`i ≤ n`, `x_{n+1} = (12T − 2)/5` and `Y = ℓ(x)`. Then `q_Y(v) = τ(τ+1)` with
`τ = v₀ + Σᵢ vᵢxᵢ`, and `v` is violated iff `−1 < τ < 0`. If `v_{n+1} = 0`,
`τ = v₀ − (12/5)a(S)` with `S = supp(v₁..vₙ)`, which is never in `(−1, 0)`
(`a(S) = 0` gives `τ = v₀ ∈ {0,1}`; `a(S) ≥ 1` gives `τ ≤ 1 − 12/5`). If
`v_{n+1} = 1`, `τ = v₀ − 2/5 + (12/5)(T − a(S))`; for `T − a(S) = 0` this is
`−2/5` when `v₀ = 0`; for `T − a(S) ≤ −1` it is at most `1 − 2/5 − 12/5 < −1`,
and for `T − a(S) ≥ 1` it is at least `−2/5 + 12/5 = 2`. So a violated 0/1 split exists iff some subset sums to `T`.
Membership in NP is clear. ∎

So a 0/1 restriction can give an NP-hard search problem exactly where
unrestricted separation is trivial. The box MIQP in §8 instead uses
`{−1,0,1}`. The proposed signed analogue was checked exhaustively for
`n ≤ 3` by the reviewer, but is not proved here. Proposition D as proved
here establishes only the 0/1 result.

**Proposition E (a fixed normalized threshold is polynomial).** For fixed
`ρ > 0` there is an algorithm that, given a rational psd `Y` with `Y₀₀ = 1`,
finds a split with normalized violation greater than `ρ` or reports that none
exists, in time `n^{O(1/ρ)}·poly(size of Y)`. *(Proved.)*

*Proof.* By Lemma A, `−q(v)/‖w‖² ≤ 1/(4‖w‖²)`, so a split with normalized
violation `> ρ` has `‖w‖² < 1/(4ρ)`: fewer than `1/(4ρ)` nonzero entries,
each of absolute value below `1/(2√ρ)`. There are `n^{O(1/ρ)}` such `w`; for
each, Lemma A gives the best `v₀` in polynomial time. ∎

Non-psd points need no separate treatment in practice: B–T's Algorithm 1 and
Lemma 4 of the split note separate them in polynomial time. So the
NP-hardness of the split note concerns vanishing normalized violations. At
its hard points every violating split has `‖w‖² = k + 1`, where the X3C
universe has size `3k`, and violation at most `1/(4(n+1+h²))`, so normalized
violation below `1/(4(k+1)(n+1))`. A fixed small threshold can be expensive
(for `ρ = 0.02`, Proposition E permits supports up to 12). Applied adaptively
with the ratio already found, Lemma A gives a cheap post-check on many
points, including 17 capped searches (§8).

## 5. Exact separators implemented

All code is in [`code/lattice.py`](code/lattice.py) and
[`code/miqp_sep.py`](code/miqp_sep.py).

- **Theorem 3 (fixed rank), `thm3_exact`.** Input: a rational psd `Y`
  (or a factorization `Y = PᵀGP`). Steps: rank factorization by the
  elimination of the split note's Lemma 4, column Hermite normal form of the
  integer matrix behind `P` (basis `W = PT` of `Λ = Pℤᴺ`), with reduced
  off-diagonal entries and exact integer graph-lattice preconditioning; exact LLL on the
  rational Gram matrix `WᵀGW`, Schnorr–Euchner enumeration (in C, floating
  point) for `min ‖Wz + w₀/2‖²_G < ¼ + 10⁻⁹`, then re-evaluation in exact
  arithmetic of all collected candidates within `10⁻⁹` of the floating
  minimum and the first enumeration’s minimizer, stopping early only when
  exact `−¼` certifies the lower bound,
  and exact Fraction LLL, Babai nearest-plane and affine-lattice embedding
  reduction of `v` modulo the integer kernel. Both enumeration flags are
  retained; `complete` requires both.
  Attaining exact `−¼` separately certifies optimality by Proposition C(a),
  even if the second enumeration is capped. The violated split it returns is
  certified exactly; the claim that no better split exists rests on the
  floating-point enumeration with that margin, so the implementation is exact
  up to floating-point error in the enumeration, not fully rational. Tests
  ([`code/test_lattice.py`](code/test_lattice.py)): 150 random rational psd
  matrices of rank 1–4 and order 2–5 against brute force over a box (the exact
  value is never above the box minimum and equals it in 144 cases; in the
  other 6 the minimizer lies outside the box), and 200 matrices of the split
  note's Theorem 1 against its complete exact Fincke–Pohst violator lists.
- **Theorem 4 (rank 1), `thm4_rank1`.** Extended Euclid on `p = D(1,x)`.
  Tested against `thm3_exact` on 200 random rank-1 points.
- **Exact maximum violation at positive definite points, `sep_pd_float`.**
  Floating LLL plus Schnorr–Euchner enumeration in dimension `N`.
- **Normalized separation, `sep_ratio`.** Dinkelbach iteration for
  `ρ* = max −q_Y(v)/‖w‖²`: given `η > 0`, solve
  `min_v q_Y(v) + η‖w‖²` exactly with `sep_pd_float` (this is maximum-violation
  separation for the positive definite matrix `Y + η·diag(0,1,…,1)`); if the
  minimum is negative, its minimizer has ratio `> η`, and `η` is raised to that
  ratio. Starting below a positive `ρ*`, the ideal exact iteration reaches
  `ρ*`: only finitely many `w` have ratio above its positive starting value.
  The implementation starts at the larger of the best elementary ratio and
  `10⁻⁶`, with residual tolerance `10⁻¹⁰`. If no candidate improves that
  starting value, a returned zero does not exclude ratios in `(0,10⁻⁶]`.
  Small negative eigenvalues of the SDP
  output are clipped first and `Y₀₀ = 1` is restored by the congruence
  `diag(Y₀₀^{−1/2}, 1, …, 1)`. Tested against brute force on 60 random psd
  matrices. Each enumeration has a node cap; if a cap is hit the result is a
  lower bound on `ρ*` and is flagged "incomplete". A "complete" flag means
  enumeration finished under these numerical rules; it is not a rational
  certificate of the global maximum (§8).
- **B–T comparator, `gurobi_sep` and `scip_sep`.** B–T separate by solving the
  convex integer QP (7) with the Buchheim–Caprara–Lodi code, which is not
  available. As the closest open equivalent we solve
  `min q_Y(v), v ∈ ℤᴺ, |vᵢ| ≤ K` with the Gurobi 13.0.2 command line (LP file,
  1 thread, `MIPGap = 0`) and with SCIP 10 through PySCIPOpt 6.2.1. General
  MIQP solvers need a box, so `K ∈ {1, 3, 10}` is a parameter.

## 6. SDP points: rank and gap (BT and DM sets)

Command: `python3 code/summ_points2.py` (and `code/summ_points.py SET` for
rank histograms at all thresholds); raw data `logs/points_*.jsonl`. These
values come from the first agent's runs; they do not depend on timing and
were checked for completeness (all 187 instances, four stages each, no
top-level errors; ten face re-optimizations failed in Clarabel and are recorded as
such).

| set | inst. | root rank (min/med/max) | SDP gap, mean % of \|opt\| | closed by de Meijer loop (count / mean % of SDP gap) | rank after loop (min/med/max) |
| --- | --- | --- | --- | --- | --- |
| BT10 | 110 | 1/2/3 | 5.58 | 110 / 100.0 | 1/1/1 |
| BT20 | 18 | 1/2/4 | 8.02 | 16 / 99.8 | 1/1/10 |
| BT30 | 18 | 1/3/4 | 9.53 | 18 / 100.0 | 1/1/12 |
| BT50 | 5 | 1/4/4 | 10.4 | 4 / 98.3 | 1/1/17 |
| DM30 | 18 | 2/3/4 | 8.16 | 15 / 97.5 | 1/1/17 |
| DM60 | 18 | 2/4/5 | 9.91 | 12 / 98.4 | 1/1/39 |

"Closed" means the final bound is within `10⁻⁴·|opt|` of the optimal value
(for the 7 DM60 instances where Gurobi hit its time limit, of the best known
value). *(Computed; numerical evidence for the instance distributions.)*

Findings:

1. **Root optima have very low rank: 1 to 5.** The gap below the rank is
   sharp: the ratio `λ_{r+1}/λ_r` at the rank boundary has median `1.1·10⁻⁹`
   and maximum `4.7·10⁻⁵` over all 187 roots. This is consistent with the
   Barvinok–Pataki bound (an SDP with `m` active linear constraints has an
   optimal solution of rank `r` with `r(r+1)/2 ≤ m`), but the observed ranks
   are far below that bound; we did not analyze why. *(Numerical evidence.)*
2. **Most closed final points have rank 1; the selected residual-gap
   points have ranks 9–39.** 171 of
   187 instances end at a numerically rank-1 integral point. The 16 others
   have ranks 2 to 39. Four of them are closed or nearly closed: two closed
   instances of rank 2 with a tiny second eigenvalue (`bt_n20_p16_s2`,
   eigenvalues 21.0 and 0.0015; `bt_n50_p25_s0`, 51.0 and 0.0014), and two
   with gaps of 0.0016% (`bt_n30_p0_s1`, rank 12) and 0.0034%
   (`dm_QUTO_t2_n30_p25_s0`, rank 3). One rank-1 instance,
   `dm_LIN_t3_n60_p50_s0`, ends at an integral point whose value `−279.780` is
   better than Gurobi's 300 s incumbent (`−279.381`), so it is closed too.
   That leaves **12 selected residual-gap instances**, 11 with established
   numerical gaps and `dm_LIN_t3_n60_p75_s0` with an upper bound only (§9.1).
   Their reported gaps or upper bound range from 0.012% to 1.04% (`logs/open_gap.txt`), at ranks 9–39 (at `τ = 10⁻⁵`; 5–38 at
   `τ = 10⁻³`). The second eigenvalue at these points is 0.37–7.4, so the rank
   is not a numerical artifact.
3. **No lower-rank optimal solution was found at the open instances.**
   Minimizing `trace Y` or a random linear function over the approximate
   optimal face returned the same rank at both reliable thresholds for all 12
   open instances. Either the optimal face is a single point or the
   re-optimization does not leave the relative interior; we did not
   distinguish these. *(Numerical evidence; a negative result.)*
4. **The polynomial families do most of the work.** On BT10, the de Meijer loop
   closes the whole SDP gap on all 110 instances, whereas B–T report that the
   full split closure closes 66.4% on average (their Table 2, STD ALL) and we
   find 65.0% (§7). The pair inequalities (2.3), which are non-standard
   splits, and the triangle and RLT inequalities are not split inequalities in
   the sense of (4.10) (apart from the 1- and 2-index ones), so this does not
   contradict B–T.

The two main classes are roots of numerical rank 1–5 and the open final
points of rank 9–39 for `n = 20…60`. Small root rank makes Theorem 3 look
promising, but its exact-rank hypothesis does not hold automatically for
the numerical input (§8).

## 7. Replication of B–T's split closure

Command: `python3 code/exp_splitloop.py bt BT10 logs/loop_bt_BT10.jsonl 2`
(and `btfam`, and both for BT20); summaries by `python3 code/summ_loop_bt.py
logs/loop_bt_BT10.jsonl`. These are the first agent's runs; the bound values do
not depend on timing, the BT10 run was repeated once with identical final
bounds (`logs/loop_bt_BT10_firstrun.jsonl`, maximum difference 0.0), and
there were no errors.

Setup: B–T's SDP relaxation plus split inequalities only. Each round adds
every violated split among (i) all Dinkelbach iterates of the numerical
normalized separator `sep_ratio` and (ii) the 100 most violated `{0,±1}` splits
with `|supp w| = 1, 2, 3` (best `v₀` by Lemma A). A split is added if its
violation exceeds `10⁻⁶`; the loop stops when none is added or after 150 rounds.
This approximates the split closure under the separator's numerical rules;
its normalized starting threshold (§5) does not certify a uniform `10⁻⁶`
unnormalized tolerance over all splits.
Mode `btfam` adds only (ii).

BT10 (110 instances, 107 with an open SDP gap). Both SDP gap columns average
over all 10 instances per `p` in their respective samples. All three closure
columns average the percentage of the SDP gap closed over open instances
in their respective samples. Both rounds columns average over all 10 of
our instances per `p`. The B–T columns reproduce their published Table 2.

| p (neg. eigenvalues) | our SDP gap % | B–T SDP gap % | split closure (ours) | B–T STD ALL | `{0,±1}`, `\|supp\| ≤ 3` only | mean rounds | rounds where only general splits were violated |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 14.29 | 4.12 | 100.0 | 100.00 | 100.0 | 2.2 | 0 |
| 1 | 4.53 | 2.71 | 99.4 | 95.71 | 99.3 | 2.4 | 0.3 |
| 2 | 6.23 | 4.21 | 71.6 | 79.77 | 64.7 | 20.2 | 14.9 |
| 3 | 8.99 | 5.75 | 46.2 | 61.12 | 38.0 | 27.9 | 22.4 |
| 4 | 7.32 | 5.33 | 52.4 | 56.44 | 42.6 | 29.1 | 22.5 |
| 5 | 4.40 | 5.71 | 53.1 | 49.70 | 44.4 | 34.2 | 28.3 |
| 6 | 4.48 | 3.91 | 57.0 | 64.24 | 44.0 | 27.5 | 20.1 |
| 7 | 4.01 | 3.59 | 54.3 | 57.50 | 39.2 | 34.9 | 27.0 |
| 8 | 3.06 | 2.71 | 61.2 | 60.07 | 50.0 | 28.0 | 22.4 |
| 9 | 2.34 | 2.27 | 57.9 | 49.25 | 46.6 | 34.0 | 25.8 |
| 10 | 1.71 | 1.83 | 59.8 | 55.12 | 50.9 | 28.4 | 22.0 |
| all | 5.58 | 3.83 | **65.0** | **66.36** | **56.5** | | |

*(Computed; numerical evidence.)* Our instances are new draws from B–T's
distribution, so only averages are comparable. The average closure, 65.0%,
matches B–T's 66.36%, which supports both the instance substitute and the
separators. The `{0,±1}` families with support at most 3 reach 56.5%, so
general splits add about 8.5 points of the SDP gap on average at `n = 10`, and
in 76.5% of the rounds (2057 of 2688) no `{0,±1}` split with support ≤ 3 was
violated while the general separator still found one. Those splits have support
2–10 and coefficients up to 6 (`logs/loop_bt_BT10.jsonl`, fields
`ratio_supp`, `ratio_vmax`); their median violation is 0.007, the largest 0.22.

BT20 (18 instances): split closure at least 54.5% on average versus 44.2% for
the `{0,±1}` families. The loop hit the 150-round cap on 13 of 18 instances,
so 54.5% is a lower bound. The tail consists of many rounds with small
violations, which matches B–T's remark (§6.2) that running the separation to
the end "is not doable in practice".

**Rank along the loop.** The rank grows as split cuts are added. On BT10 the
points visited by the loop have rank up to 11 = `N`, mostly 6–9; on BT20 up to
20, mostly 11–17; the final points of the BT20 runs that hit the cap have
rank 11–20 out of 21. Near the split closure, the points to be separated are
therefore close to full rank, where Theorem 3 gives no advantage.

**Cost of normalized separation.** All 5168 calls of `sep_ratio` in
these loops completed (4768 in `bt`, 400 in `btfam`; no node cap hit).
Median and maximum time per call in `bt` mode:
0.025 s and 0.055 s at `n = 10`; 0.14 s and 0.47 s at `n = 20`. These times
were measured while the machine was heavily oversubscribed (load average
about 190–220 on 36 cores according to the first agent’s transcript;
no first-run load log is retained). They are observed
wall-clock times, not controlled single-core costs. One BT10 duration is
negative (`−0.00389` s), consistent with a wall-clock adjustment; the reported
median and maximum are unchanged at the stated precision if it is discarded.
*(Numerical evidence.)*

## 8. Split separation at the stored points

The closeout audit is [`code/audit_closeout.py`](code/audit_closeout.py);
its full output is [`logs/audit_closeout.json`](logs/audit_closeout.json).
The readable per-point summary is
[`logs/summary_sep_closeout.txt`](logs/summary_sep_closeout.txt).
The original normalized and MIQP results are retained. After review r1,
Theorem 3 was rerun with exact reduction and the normalized results were
post-checked using Lemma A; see below and the revision Checks.

**Coverage and errors.** `sep_selection_A.txt` (92 paths) and
`sep_selection_B.txt` (31) contain 123 distinct points. The three shards are
disjoint selections, not three repeated trials: each has exactly 41 matching
records in `sep_run2_s0.jsonl`, `sep_run2_s1.jsonl`, `sep_run2_s2.jsonl`.
All three original output logs finish without a traceback. They contain 8, 6 and 5
overflow/invalid-value warnings, respectively, from the floating kernel
shortening code used by Theorem 3. Two Theorem 3 records in shard 0 have
errors when converting integers with more than 4300 digits to strings:
`bt_n20_p0_s2__BT__cut` and `bt_n30_p0_s1__BT__cut`. Their other separators
completed and their records are retained. Shards 1 and 2 have no such errors.
These original failures must not be counted as successful fixed-rank
separation; the corrected experiment is reported separately below.

The selection consists of 99 roots (22 BT10 and all 77 larger instances),
17 final/trace points from the 12 open instances of §6, and 7 final/trace
points from four nearly closed instances. The last group deliberately selects
non-rank-1 points; it does not represent the 171 integral final points.
No random-face point is in the separation selection.

**Normalized separation.** Enumeration has a cap of `2·10⁷` nodes per
Dinkelbach step. "Finished" below means the implementation's `complete`
flag (§5). Reported times include both finished and unfinished calls;
quantiles use linear interpolation. Violation medians omit calls returning
no vector. All of these results are numerical evidence.

| point class | points | finished / finished or certified | time median / 90th percentile / max (s) | normalized violation median | violation median | support of returned splits with violation > `10⁻³` |
| --- | --- | --- | --- | --- | --- | --- |
| root | 99 | 83 / 99 | 0.123 / 0.920 / 1.714 | 0.1180 | 0.2347 | 1–3 (98 points) |
| open final/trace | 17 | 13 / 14 | 0.363 / 6.806 / 11.362 | 0.05070 | 0.1598 | 3–5 (15), 37–38 (2) |
| nearly closed final/trace | 7 | 7 / 7 | 0.054 / 0.553 / 0.763 | 0.005386 | 0.02346 | 3–4 (4 points) |

**Post-hoc norm certification (review r1).**
[`code/certify_ratio_r1.py`](code/certify_ratio_r1.py) independently enumerates
all integer directions allowed by Lemma A’s adaptive norm bound at the
stored points ([records](logs/ratio_certificates_r1.jsonl),
[log](logs/ratio_certificates_r1.txt)). For `Y₀₀ = 1`, let
`ε = max(0, −λ_min(X−xxᵀ)) + 10⁻⁹`. A direction beating the reported ratio
`ρ > ε` must have `‖w‖² ≤ floor(1/(4(ρ−ε)))`. The script first scales the
stored matrix by `Y₀₀` and rescales ratios afterward, so Lemma A’s hypothesis
is respected. It enumerates every norm pattern within that bound, modulo
global sign, when there are at most `2·10⁸` directions. On 110 of 123 records
the exhaustive maximum exceeds the reported ratio by at most
`7.622911167987079·10⁻⁷`, below the `10⁻⁶` comparison tolerance. This includes
all 16 capped roots and `bt_n50_p0_s0__BT__cut`, whose norm bound is 3.
Thus **17 of 20 capped searches are numerically certified**, and **120 of
123 are finished or certified**. Three zero-ratio records have no finite
bound and ten bounds are too large; ten of these thirteen records already
finished. The remaining uncertified capped records are the two dense DM60
points and `dm_QUTO_t1_n60_p75_s0__DM__cut` (norm bound 7).
These are certificates under floating-point rules and a `10⁻⁶` tolerance,
not exact rational proofs of the stored-point maxima.

Among roots, all 22 of size 10, all 18 of size 20, and all 36 of size 30
finish. Only 1 of 5 at size 50 and 6 of 18 at size 60 finish; the remaining
16 searches hit a cap despite returning useful small-support splits.
All 16 are now certified numerically by the post-check above.
Median times by size are 0.022, 0.064, 0.163, 0.760 and 0.926 s.
The best found normalized split at the roots has support 1 on 14 points, 2 on
81 and 3 on 3; the remaining root is numerically integral. All returned
coefficients, including `v₀`, have absolute value at most 2. No root result
improves the best normalized `{0,±1}` split of support at most 3 by more
than `10⁻⁸`; numerical clipping causes small differences in the opposite
direction. Thus low rank is not needed to find the useful root cuts here.

At the open final/trace points, three-index `{0,±1}` splits have violation
above `10⁻³` on 15 of 17 points (median over all 17 signed values, including two negative ones, 0.152;
median over the 15 violations above `10⁻³`, 0.1545; maximum 0.199). Six points
have a general normalized improvement above `10⁻⁸`, with returned supports
4, 4, 4, 5, 37 and 38. The two dense results are
`dm_LIN_t3_n60_p75_s0__DM__cut` (support 37, `max|vᵢ| = 2`, violation
0.07219, ratio 0.001388) and `dm_QUTO_t1_n60_p50_s0__DM__cut` (support 38,
`max|vᵢ| = 4`, violation 0.12345, ratio 0.001260). Both are unfinished,
as are `bt_n50_p0_s0__BT__cut` and `dm_QUTO_t1_n60_p75_s0__DM__cut`.
The post-check certifies the BT50 result; only the two dense points and
`dm_QUTO_t1_n60_p75_s0__DM__cut` remain uncertified. A reviewer rerun at
`2·10⁸` nodes per step gives ratios 0.001628785914232908 (QUTO) and
0.0017227177103663232 (LIN), still capped
([log](reviews/r1-logs/r1_dense_cap.out)). These are about 29.3% and 24.1%
above the original lower bounds, so those lower bounds are cap-sensitive.
For the 13 finished open-point calls, median/max time is 0.334/1.015 s.
Re-evaluating all 120 returned vectors at the stored matrices changes `q`
by at most `2.29·10⁻⁶`; every violation above `10⁻³` survives. This check
separates useful cuts from claims of global optimality.

The nearly closed group shows that a small objective gap does not imply
membership in the split closure: four points still have violations above
`10⁻³`, including the two `dm_QUTO_t2_n30_p25_s0` points with violations
0.1303 and 0.1331. Conversely, the support-13 result at
`bt_n50_p25_s0__BT__cut` has violation only `1.46·10⁻⁵` and ratio
`7.53·10⁻⁷`; it is not evidence for useful dense separation.

**Box-constrained MIQP.** Gurobi gets 30 s, one thread and `MIPGap = 0` for
each box `|vᵢ| ≤ K`. This maximizes unnormalized violation within a box;
it solves a different problem from `sep_ratio` and does not certify all-split
separation. Counts of `Optimal solution found` are:

| point class | `K = 1` | `K = 3` | `K = 10` |
| --- | --- | --- | --- |
| root (99) | 29 | 15 | 29 |
| open final/trace (17) | 6 | 0 | 0 |
| nearly closed final/trace (7) | 0 | 0 | 0 |

All other statuses are `Time limit reached`; there are no unknown or
infeasible statuses. Median wall time is about 30–31 s in every class/box.
At roots, the median incumbent violation is about `¼` in every box, usually
with much denser vectors than the normalized separator. At open points,
median incumbent violations are 0.237, 0.247 and 0.249 for the three boxes,
but Gurobi finds no violated incumbent at either dense exceptional point.
Larger boxes amplify numerical residuals: one `K = 3` and six `K = 10`
records have raw `q < −0.250001`, down to `−0.25224`. Gurobi optimizes a
clipped psd matrix while logged `q` is re-evaluated at the stored matrix
(`miqp_sep.py`); this is a warning about numerical input, not a violation of
Proposition C(a).

**Theorem 3 at rational neighbours, corrected after review r1.** The
experiment truncates to rank `r` at `τ = 10⁻⁵`, rounds pivot rows on a
`10⁻⁶` grid, and builds an exact rational psd matrix with `Y₀₀ = 1` (§5).
The original 113 attempts had 111 recorded values and two serialization
errors. Of 109 returned vectors only 7 passed the stored-point sanity check.
The old coefficient blow-up came from this implementation’s unreduced
column form and floating kernel shortening. Its root failures do not show
that Theorem 3 requires huge coefficients at low rank. The non-root results
are assessed separately below.

The corrected implementation uses reduced column HNF, exact Fraction LLL
and exact affine-coset shortening. An exact graph-lattice reduction before
HNF avoids huge intermediate kernel bases. It checks every candidate from
the second enumeration and the first enumeration’s minimizer with a common
integer denominator, and retains both
enumeration flags; the old implementation discarded the second flag and
checked only the first 200 candidates. A returned rational violation is
checked exactly. The global-minimum claim still depends on floating CVP
enumeration, except when exact `q = −¼` proves optimality by Proposition C(a).
The two node caps are `2·10⁶` and `2·10⁵`; hitting either marks the combined
flag incomplete. Timing now includes lifting and exact shortening, with
rationalization and total times recorded separately.
The targeted rerun uses [`code/rerun_thm3_r1.py`](code/rerun_thm3_r1.py),
[records](logs/thm3_r1.jsonl) and [output](logs/thm3_r1.out).
That rerun completed all **113 attempts without errors**: 99 roots,
7 open final/trace points and 7 nearly closed points. It returned 111 vectors.
All first enumerations finished; 14 second enumerations hit their cap
(7 roots and all 7 open points), so **99 calls have both flags complete**.
Exact values are within `10⁻⁹` of `−¼` on 109 of 113 calls and equal `−¼`
as Fractions on 35. Closeness to this exact lower bound also certifies raw
optimality to additive error `10⁻⁹`, even when a flag is incomplete.
For the 35 attaining `−¼`, raw optimality is exact.

In the table, “sane” means `−¼−10⁻⁶ ≤ q_Y(v) < 0` at the stored point;
coefficient and support statistics cover returned vectors. Times include
rationalization, both enumerations, exact verification, lifting and shortening.
The [revision summary](logs/revision_summary_r1.txt) recomputes every entry.
A round-2 rerun with the first minimizer always retained
([records](logs/thm3_r2.jsonl), [output](logs/thm3_r2.out)) reproduces all
113 vectors or no-vector results, exact neighbour/stored values, supports
and flags. The table retains the round-1 timings; the
[round-2 comparison](logs/revision_summary_r2.txt) confirms that no numerical
claim changes.

| point class | attempts / returned | both enumerations complete | exact `−¼` / within `10⁻⁹` | max coefficient median / max | support range | sane | total time median / max (s) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| root | 99 / 98 | 92 | 34 / 98 | 5 / 70 | 6–38 | 98 | 0.913 / 41.162 |
| open final/trace | 7 / 7 | 0 | 0 / 6 | 1220 / 5790 | 20–58 | 5 | 20.682 / 49.789 |
| nearly closed final/trace | 7 / 6 | 7 | 1 / 5 | 6177.5 / 69618975 | 20–50 | 0 | 1.072 / 13.425 |

All 98 returned root vectors now pass the sanity check, compared with only
7 previously. Their raw stored-point values lie between
`−0.25000020774206355` and `−0.24998328282798365`; the maximum change from the
rational neighbour is `1.671716981094251·10⁻⁵`. Their median normalized
violation is only `0.0016898834397569152`, versus the normalized separator’s
root median `0.1180` in the earlier table. The enormous root coefficients
were implementation artefacts, while the poor normalized values reflect
the raw objective.

All 13 non-root returned vectors have maximum coefficients from 30 to
69618975 (`6.96·10⁷`). Eight are not violated at the stored point: two open
and all six nearly closed vectors. The other five have normalized violation
at most `8.2·10⁻⁶` (median `3.077003639805213·10⁻⁸`), so none of the 13 is
a useful cut in this sample. The review’s `2.8·10⁻⁸` median covers all
seven open-point signed ratios, including the two unviolated vectors.
The largest coefficient’s stored value is
`584865655.5109526`.

At four of the six nearly closed neighbours with a returned vector, both
enumeration flags are complete and no short exact raw maximizer exists.
The reviewer’s exact projection bounds on the returned kernel cosets are
reproduced by [`code/check_nonroot_r2.py`](code/check_nonroot_r2.py)
([records](logs/nonroot_r2.jsonl), [log](logs/nonroot_r2.txt)). The new check
also enumerates every minimizing image in exact rational arithmetic and
bounds every maximizing coset by projecting onto two kernel directions.
Thus every exact maximizer at these four neighbours has norm at least
`1.1·10⁴`–`1.0·10⁸`, depending on the point, and the returned vector is
within 1.5% of the shortest:

| nearly closed point | norm lower bound for every exact maximizer (approx.) | returned norm (approx.) |
| --- | --- | --- |
| `dm_QUTO_t2_n30_p25_s0__DM__cut` | `1.139·10⁴` | `1.149·10⁴` |
| `dm_QUTO_t2_n30_p25_s0__DM__cut_trace` | `1.01831·10⁸` | `1.01831·10⁸` |
| `bt_n20_p16_s2__BT__cut` | `7.48888·10⁵` | `7.48888·10⁵` |
| `bt_n50_p25_s0__BT__cut` | `1.46865·10⁴` | `1.46865·10⁴` |

Their stored-point values range from `297.9331428895137` to
`584865655.5109526`. At least 99.8% of each value comes from the
eigen-directions discarded by rank truncation; `λ_{r+1}` ranges from
`2.7·10⁻⁷` to `1.7·10⁻⁴`. These long vectors therefore come from exact raw
maximization on a rank-truncated neighbour, not from the shortening code.
The bounds at the other two nearly closed neighbours are inconclusive.
At all seven open neighbours the second enumeration is capped, so bounds
on the returned coset do not exclude shorter maximizers in other images.
Stored-point validation remains necessary.
The maximum entrywise matrix errors are `8.579499948258018·10⁻⁶` at roots,
`2.0499569765242143·10⁻⁴` at open points, and `5.7977058759539624·10⁻⁵` at
nearly closed points. The exact-neighbour values are independent of the
old serialization failures and floating shortening; their relevance to the
original point is a separate numerical question.

**Rank-1 check and the objective.** To check the review independently,
[`code/check_rank1_short_r1.py`](code/check_rank1_short_r1.py) rounds the
first column directly on the `10⁻⁶` grid and reduces an exact integer
embedding of `pᵀv = −D/2` ([records](logs/rank1_short_r1.jsonl),
[log](logs/rank1_short_r1.txt)). All nine fractional rank-1 roots have
`D = 10⁶`, exact neighbour value `−¼`, coefficients at most 4 and supports
5–12; the stored-point value differs from `−¼` by at most
`2.8200390997379365·10⁻⁷`. Their normalized violations are
0.005434782196430684–0.035714283093631366, whereas the best normalized
root splits have ratios 0.2436118334018897–0.24999949399147514 on those same
nine points. The tenth rank-1 root has an integral grid neighbour and is
skipped by this check. Pivot-row and first-column rationalization are
different procedures, but give identical denominators, vectors, exact values
and stored-point values at all 10 rank-1 roots in the Theorem 3 rerun.
The main `thm3_exact` itself returns coefficients 1–5 at the nine fractional
roots; the separate affine-LLL check above finds coefficients at most 4.
The [round-2 reporting check](logs/revision_summary_r2.txt) verifies this
agreement. The existence of short exact raw maximizers is clear in both
the review and this check. Raw maximization selects dense near-kernel
directions even when their coefficients are small; normalization selects
more useful small-norm cuts here.

Rationalization remains a separate issue. If `Δ = Y − Ŷ`, then
`q_Y(v) − q_Ŷ(v) = vᵀΔv + vᵀΔe₀`; entrywise error `ε` gives the bound
`ε(‖v‖₁² + ‖v‖₁)`. Exact reduction controls the representative but does not
turn a rational neighbour into the stored SDP point or prove that a shortest
representative was found. Each cut must still be re-evaluated at the stored
point. Neither this experiment nor the old implementation establishes that
low numerical rank makes Theorem 3 impractical.

**Agreement and load.** The first run has 115 common points; the remaining
8 were lost when `sep_A` crashed (§11). Family values agree exactly on all
115. Normalized values agree within `10⁻⁸` on 113; only the two unfinished
dense searches differ, by at most 0.000748. The second run improves the
linear instance's ratio but lowers the QUTO instance's ratio: a larger cap
and changed psd preprocessing do not make these heuristic outcomes
monotone. Completeness flags agree on all 115 common points, and all 103
common successful Theorem 3 values agree within `10⁻¹²`. MIQP statuses and
incumbents vary under the time limits; their comparison is tabulated in the
audit, not treated as replication of an optimum.

`machine_load_run2.txt` contains 360 one-minute samples from
2026-10-02 19:14:55 to 2026-10-03 01:13:49, UTC−4. The one-minute load
ranges from 10.15 to 172.39 (median 16.42; 90th percentile 103.06) on the
reported 36-core host. These samples span the rerun and subsequent work;
per-record start/end timestamps were not saved, so they cannot normalize
individual timings. All timings here are observed wall-clock times under
varying shared load, not controlled speed comparisons.

## 9. What general splits add after de Meijer et al.'s families

Commands (each instance limited to 40 rounds and a 2400 s wall-clock budget,
checked after each round):
`python3 code/exp_splitloop.py dmfam SET logs/loop_dmfam_open.jsonl 2 logs/open_gap.txt 40 2400`
and the same with `dmplus`, for SET = BT20, BT50, DM30, DM60; summary
`python3 code/summ_loops_dm.py`. Mode `dmfam` runs de Meijer et al.'s
families together with the `{0,±1}` splits with `|supp w| ≤ 3` (polynomial,
`O(n³)` candidates). Mode `dmplus` adds, in addition, every Dinkelbach iterate
of the normalized separator, that is, general splits. Both start from
the root and stop when nothing is violated (families: `10⁻³`; splits:
`10⁻⁶`). On `dm_LIN_t2_n30_p75_s0` Clarabel failed in the first attempt of
both modes (`logs/loop_failed_attempts.jsonl`); the rerun retries at
tolerance `10⁻⁷`, with SCS as the next fallback. The final logs record one
successful retry in each mode; they do not identify which fallback solver
succeeded.

Remaining gap in % of the best known value (12 open instances of §6):

| instance | root | de Meijer families | + `{0,±1}`, `\|supp\| ≤ 3` | + general splits | rank of final `dmplus` point |
| --- | --- | --- | --- | --- | --- |
| bt_n20_p0_s2 | 23.59 | 0.6176 | 0 | 0 | 1 |
| bt_n20_p0_s0 | 19.46 | 0.2593 | 0 | 0 | 1 |
| bt_n50_p0_s0 | 12.25 | 1.0378 | 0 | 0 | 1 |
| dm_LIN_t2_n30_p50_s0 | 0.75 | 0.0204 | 0 | 0 | 1 |
| dm_QUTO_t1_n30_p75_s0 | 10.17 | 0.4200 | 0.1788 | 0 | 1 |
| dm_LIN_t2_n30_p75_s0 | 1.06 | 0.2391 | 0.0220 | 0 | 1 |
| dm_QUTO_t2_n60_p25_s0 | 0.14 | 0.0117 | 0.0002 | 0 | 1 |
| dm_QUTO_t2_n60_p75_s0 | 0.38 | 0.0357 | 0 | 0 | 1 |
| dm_QUTO_t1_n60_p75_s0 | 13.80 | 0.1048 | 0.0777 | 0 | 1 |
| dm_LIN_t2_n60_p75_s0 | 0.46 | 0.0148 | 0 | 0 | 1 |
| dm_QUTO_t1_n60_p50_s0 ‡ | 15.05 | 0.9523 | 0.9523 | 0.9485 (budget) | 39 |
| dm_LIN_t3_n60_p75_s0 † | 18.68 | 0.2217 | 0.2217 | 0.2195 (budget) | 42 |

"0" means the final point is numerically rank 1 and integral; the absolute
bound/incumbent mismatch is below `5·10⁻⁶` %. † Gurobi remains time-limited;
the gap against its incumbent is an upper bound on the true gap. ‡ The
longer run returned optimal to `MIPGap = 10⁻⁶` (§9.1). Budget stops took
2523 and 2452 s because the budget is checked between rounds. All other runs
converged under their implemented rules. *(Computed; numerical evidence on 12
instances.)*

Findings:

1. **The support-at-most-3 extension closes most of the remaining gap.** Added to
   de Meijer et al.'s families (which contain only the 1- and 2-index
   splits), they close the gap completely on 6 of the 12 instances and reduce
   it on 4 more. The additional three-index family has `4·C(n,3)` directions
   and Lemma A gives the best right-hand side of each in `O(1)`. The experiment
   also tests all right-hand sides for supports 1–2 at tolerance `10⁻⁶`,
   rather than the original `10⁻³`; it does not isolate the contribution of
   three-index cuts alone. The stored-point violations in §8 nevertheless
   identify that family as the main missing small-support source.
2. **General splits close the rest on 10 of 12 instances.** On the four
   instances where the three-index splits leave a gap
   (`dm_QUTO_t1_n30_p75_s0`, `dm_LIN_t2_n30_p75_s0`, `dm_QUTO_t2_n60_p25_s0`,
   `dm_QUTO_t1_n60_p75_s0`), adding the normalized separator ends at a
   numerically integral rank-1 point and closes the gap to numerical
   accuracy. At the final `dmfam` points of
   these instances, the most violated split (normalized) has support 5–6,
   coefficients at most 3 and violation 0.047–0.167, far above the cut
   tolerance `10⁻³`. These diagnostic calls completed on three of the four
   final points; the size-60 Type-1 call was capped. Also, `dmfam` and
   `dmplus` start from the root and follow different cut paths, so the final
   bound comparison is an experiment with added families, not sequential
   separation at an identical final point.
3. **Two instances behave differently.** On `dm_QUTO_t1_n60_p50_s0` and
   `dm_LIN_t3_n60_p75_s0`, no split with support at most 3 is violated after
   the families, the three-index splits change nothing, and the bound moves
   by only 0.004 and 0.002 percentage points in 2400 s of general split
   separation. The ranks are 39 and 42 out of 61. In 19 of 21 and 22 of 24
   rounds no `{0,±1}` split with support ≤ 3 was violated, while the separator found
   dense splits with support 24–49, coefficients up to 13 and violation
   0.031–0.172. Every call of `sep_ratio` at these points hit its node cap
   in at least one enumeration (`2·10⁶` per Dinkelbach step in these loops),
   so these were the best splits
   found, not certified maxima. These two points are the only stored
   separation points with useful dense splits after the tested `{0,±1}`
   families of support at most 3 find nothing, and are the two such instances
   in the `dmfam`/`dmplus` loops. The BT10 loops also have general-only rounds
   with support up to 10 out of 10 (§7). This does not
   exclude other short-support, larger-coefficient splits. Exact separation
   was not completed; §10 compares them with the hard instances of
   the split note.
4. **Rank along the loops.** In `dmplus` the rank rises from 1–5 at the root
   to 7–34 in the middle rounds and drops to 1 when the gap closes
   (`logs/loop_dmplus_open.jsonl`, field `rank`). The normalized separator took a
   median of 0.02–0.7 s per round (maximum 1.4 s) on 9 of the 10 converging
   instances. On `dm_QUTO_t1_n60_p75_s0` (ranks up to 34) the median was 3.9 s
   and the enumeration hit its cap in 9 of 10 rounds, yet the loop still
   closed the gap. On the two instances of item 3 the median was 7–8 s, with
   a cap hit in every round. Times include shared-machine contention; the
   available load log does not establish per-call load (§8).

### 9.1 Optimal values of the two time-limited instances

The completed longer runs use a 3600 s solver limit and one thread
(`logs/opt_gurobi_long_1.jsonl`, `opt_gurobi_long_2.jsonl`;
outputs `run_opt_long_1.out`, `run_opt_long_2.out`). Neither improves its
300 s incumbent.

For `dm_QUTO_t1_n60_p50_s0`, Gurobi reports optimal after 3017 s with
incumbent `−46.88445474016` and lower bound `−46.88448727441`.
The residual optimization gap is `0.00006939` %, consistent with the
requested `MIPGap = 10⁻⁶`. The final `dmplus` bound is
`−47.32915857923395`, leaving 0.948510% against the incumbent; using the
Gurobi lower bound instead changes that percentage by less than 0.000071
percentage points. Thus the remaining gap is established numerically on
this instance and is not explained by a poor incumbent.

For `dm_LIN_t3_n60_p75_s0`, Gurobi times out after 3607 s with incumbent
`−335.9002670476` and lower bound `−356.093786466` (6.01176% optimization
gap). The `dmplus` bound is `−336.63750881563215`, giving only an upper
bound of 0.219482% on the true remaining relaxation gap. Its true optimum
is unresolved; no claim that this gap is strictly positive follows from
the logs. The summaries in §§6 and 9 retain the original 300 s values
for comparability; the incumbent values for these two instances are unchanged.

## 10. The hard instances of the split note in practice

Commands: `python3 code/exp_hard.py logs/hard_run2.jsonl` (88 records; the
first, high-load run is in `logs/run1_highload/hard.jsonl` and gives the same
values), `python3 code/summ_hard.py thm1` and `... cor5`, and
`python3 code/exp_hard_long.py logs/hard_long.jsonl 1e10`.

Instances: random X3C instances with universe size `3k` and `n = 2k` or `3k`
sets, with a planted exact cover (C) or without (R; for `k = 2` the random
instance happens to have a cover too), `k = 2…25`. For each, the matrices of
Theorem 1 (`h² = n + 1`) and of Corollary 5 (`4h² = max(3, n+1)·Ĝ`, which
satisfy all of de Meijer et al.'s families) are built in exact arithmetic
(`check_split_separation.reduction` from the split note's directory) and
passed to the separators in floating point. Separators: the `{0,±1}` families
with `|supp w| ≤ 3`; exact maximum-violation enumeration `sep_pd_float` (node
cap `5·10⁸`); `sep_ratio`; Gurobi with `|vᵢ| ≤ 1` (300 s); SCIP with
`|vᵢ| ≤ 1` (300 s, only `k ≤ 10`).

Selected rows, Corollary 5 matrices (times in seconds; `*` = node cap hit;
TL = time limit; "found" = the violated split was found but optimality not
proved):

| k (X3C) | n | N | cond. | min q (C) | best `\|supp\| ≤ 3` | enumeration C / R | Gurobi C / R | SCIP C / R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 9 | 11 | 93 | −3.1e−3 | none violated | 0.00 / 0.00 | 0.1 / 0.0 | 0.5 / 0.4 |
| 6 | 18 | 20 | 282 | −8.9e−4 | none | 0.01 / 0.01 | 0.3 / 0.3 | 8.1 / 9.4 |
| 10 | 30 | 32 | 737 | −3.4e−4 | none | 0.03 / 0.02 | 6.5 / 4.1 | 29.5 / 41.2 |
| 15 | 45 | 47 | 1605 | −1.6e−4 | none | 0.90 / 0.27 | TL found / TL | – |
| 20 | 60 | 62 | 2822 | −8.9e−5 | none | 11.4* found / 11.0* | TL not found / TL | – |
| 25 | 50 | 52 | 2920 | −1.1e−4 | none | 5.5 / 0.10 | TL found / 41.1 | – |
| 25 | 75 | 77 | 4370 | −5.7e−5 | none | 13.0* not found / 15.2* | TL not found / TL | – |

The full tables (both matrix kinds, all 22 `(k, n)` pairs) are printed by
`summ_hard.py`. The Theorem 1 matrices behave the same way, except that SCIP
also times out at `n = 18, 24, 30`. Longer enumeration on the Theorem 1
matrices (`logs/hard_long.jsonl`, node cap `10¹⁰`): `n = 60` completes in
206 s (`9.3·10⁹` nodes) with the cover and 28 s (`1.4·10⁹` nodes) without; at
`n = 75` the cap is hit after about 240 s in both cases and the planted
violated split is not found. *(Computed; numerical evidence.)*

Findings:

1. **The predicted values are reproduced to floating-point accuracy** wherever a method
   completes: the minimum of `q` equals `−1/(4(n+1+h²))` with a cover and 0
   without (to floating-point accuracy), and the `{0,±1}` families with
   support ≤ 3 never detect a violated split for `k ≥ 3`, as Corollary 1(iii)
   of the split note predicts.
2. **The hard instances become hard in practice around `N ≈ 50–77`.**
   Gurobi with the smallest box fails to prove optimality within 300 s on 13
   of the 16 records with `N ≥ 47` (both matrix kinds; 7 of 8 for Corollary 5);
   exact lattice enumeration is fast up to `N = 52` and needs minutes at
   `N = 62`; at `N = 77` neither method finds the planted violator in its
   budget. Where both finish, SCIP's observed wall time is 2 to 431 times
   Gurobi's on
   this convex integer QP, and it times out on several instances that Gurobi
   solves in a few seconds.
3. **Their violations are below the usual cut tolerance.** For the
   Corollary 5 points, which are the ones that satisfy de Meijer et al.'s
   families, the violation is below `10⁻³` (their tolerance, §6.4) for every
   instance with `N ≥ 18`, and below `10⁻⁴` for `N ≥ 62`. A solver with tolerance
   `10⁻³` would treat these points as being in the split closure. The
   normalized violations are smaller still (Proposition E).
4. **Comparison with the practical points.** The hard points are positive
   definite (full rank) with condition numbers 24–4400. Every violating split
   corresponds to an exact cover and has support `k + 1`; uniqueness of
   the planted cover was not checked. Violations are of order `10⁻⁵–10⁻²`. The
   practical open stored points of §6 have rank 9–39 out of 21–61 (up to
   rank 42 after `dmplus`). Their best found splits have violation 0.03–0.25,
   mostly with support ≤ 3 (and
   support 5–6 after the three-index family). The two exceptional DM60 points
   of §9 share one feature with the hard points: the tested small-support
   `{0,±1}` splits fail while dense splits (support 24–49) are found.
   Their violations (0.03–0.17) are
   two to three orders of magnitude larger and many different dense splits
   are violated. The BT10 general-only rounds also reach full support (§7).
   [Binary-separation Corollary 6](../binary-separation/note.md) separately
   proves strong NP-hardness at positive definite binary points satisfying
   Boolean quadric triangle inequalities, with all violators in `{0,±1}`.
   So neither low coefficients nor binary structure removes worst-case
   hardness. The X3C construction tested here does not describe what was
   seen at these practical points; it does show where exact separation becomes
   expensive (dense violators, `N` of 50–80).

## 11. Reuse of the first agent's work; corrections

The first agent's transcript was read; it wrote no note. Its code was read in
full and its outputs were checked for completeness, parameters and validity.

Reused (bound values and split statistics checked; numerical limitations
are stated where used):
`logs/points_*.jsonl` and `data/points_*` (187 instances, 4 stage records,
including 10 failed face solves);
`logs/opt_gurobi.jsonl` (77 instances, the 300 s limit was reached on 7);
`logs/loop_bt_BT10.jsonl`, `loop_btfam_BT10.jsonl`, `loop_bt_BT20.jsonl`,
`loop_btfam_BT20.jsonl` (bounds and split statistics; timings are affected
by load, see below); the tests `test_lattice.py` and `check_props.py` [P1]–[P3]
(rerun here after a code change, §Checks).

Rerun, and why:

- `sep_A` crashed after 84 of 92 points: at `dm_QUTO_t2_n30_p25_s0__DM__root`
  Clarabel returned `Y₀₀ = 1 + 4.4·10⁻⁷`, and `sep_ratio` reset the entry to 1
  after clipping, which made the matrix indefinite (smallest eigenvalue
  `−2.0·10⁻⁷` on recomputation from the stored point), so the Cholesky factorization failed. Fixed by restoring
  `Y₀₀ = 1` with a congruence (§5). The node cap of `sep_ratio` was also raised
  from `2·10⁶` to `2·10⁷` per enumeration, since several points of `n = 50, 60`
  hit the old cap.
- All separation and hard-instance timings of the first run (`sep_A`,
  `sep_B`, `hard`; now in `logs/run1_highload/`) were taken at load averages
  of about 190–220 on 36 cores according to its transcript, without a
  retained first-run load log. Gurobi's 30 s and 300 s time limits are wall
  clock, so its status and gaps from that run are not comparable with the
  enumeration times. These experiments were rerun (`logs/sep_run2_s*.jsonl`,
  `logs/hard_run2.jsonl`). The machine was again shared during the rerun;
  the load average is logged every minute in `logs/machine_load_run2.txt`.
- The loop experiments with de Meijer et al.'s families plus splits
  (`dmplus`, `dmfam`) had been coded but never run; they were run here (§9)
  after adding a round cap, a wall-clock budget and a retry when Clarabel
  fails.

The first agent's intermediate numbers (smoke tests in its transcript) are
not used as experiment results; numerical claims come from the cited logs
except the explicitly attributed first-run load estimate.

**Historical author-closeout corrections (2026-10-03, before review r1).**
The author audit checked the then-quoted tables against the completed logs.
The following records those corrections; the review-r1 revision below
supersedes the old Theorem 3 findings and corrects §§6–7 further:

- §6: 10 failed face re-optimizations, not 6; there are 748 stage records,
  not 748 successful stored solutions. All root and cut solves succeeded.
- §7: 2057/2688 is 76.5%, not approximately 80%. Failure of the tested
  `{0,±1}` family does not mean failure of every split of support at most 3.
  In 91 of those rounds the returned split has support at most 3 with larger
  coefficients. The actual support range is 2–10 and maximum coefficient 6.
  One negative wall-clock duration is recorded. Finished enumeration is
  distinguished from an exact split-closure certificate (§5).
- §8: all three shards are complete; they are disjoint batches. Theorem 3
  has two integer-serialization errors and 111 recorded values, 107 within
  `10⁻⁹` of `−¼`. The logs do not establish exact equality or coefficient
  counts for the failed records. Fixed-rank `time` excludes lifting and
  shortening. Load over the saved interval is 10.15–172.39, not uniformly
  110–140, and cannot be matched to individual calls.
- §9: the dense-support range in the general-only `dmplus` rounds is 24–49,
  not 24–50. Each separator call was capped in at least one step, which does
  not imply that every enumeration was capped. Numerical zero gaps have
  absolute discrepancies up to `4.85·10⁻⁶` %, not below `10⁻⁶` %.
  §9.1 incorporates the completed longer optimization logs: QUTO now has an
  optimum to Gurobi's requested tolerance; the linear instance remains open.
  Both final runs of the retried size-30 linear instance record one retry;
  the logs do not establish that SCS was the successful solver.
  The `dmfam` improvement cannot be attributed solely to three-index cuts:
  supports 1–2 are also separated with best right-hand sides and tighter
  tolerance. The comparison is stated as the support-at-most-3 extension.
- §10: 13/16 large hard-instance MIQPs are unfinished across both matrix
  kinds (7/8 for Corollary 5). The observed SCIP/Gurobi time ratio where
  both finish is 2–431, not 5–200. The planted exact cover need not be unique;
  the experiment checked existence, not uniqueness. The smallest constructed
  violations are of order `10⁻⁵`.
- §4: Lemma A's formula was correct but its minimizing `u` description was
  not; it is now `u = {t}−1`, with the two integer endpoint ties. Proposition
  C(d)'s nonattainment assertion was false for a vector with an irrational
  coordinate and a rational half-integer coordinate; the exact attainment
  criterion and a counterexample are now given. The frequency claim
  "usually exactly `¼`" is restricted to the tested neighbours and weakened
  to numerical closeness. These changes do not alter the split note's proofs.

**Comparison with the earlier notes.** Nothing in the split note is
contradicted. Two of its statements need a practical qualification:

- §8, "Fixed-rank points are separable exactly. A point of rank `r` costs
  `r^{O(r)}·poly` time." This holds for exact rational input. Numerical rank
  alone does not identify that input. Exact reduction corrects the old
  implementation’s coefficient blow-up at roots; all nine fractional
  rank-1 roots have short exact maximizers of their grid neighbours that
  remain violated at the stored points (§8). The practical qualification
  concerns the raw-violation objective, which can prefer dense directions
  with poor normalized violation, and validation after rationalization.
  It is not a claim that low rank itself defeats Theorem 3.
- §8, "Whether relaxation optima in practice have low rank depends on the
  instance." On the instance families tested, the answer is sharper: root
  optima have rank 1–5; after the implemented families 171 points have rank
  1, the 12 open points have rank 9–39, and four nearly closed exceptions
  have rank 2–12 (§6).

## 12. Conclusions for solvers

**Recommended policy (heuristic, supported by these root-bound experiments).**
Keep the implemented de Meijer families, add exhaustive `{0,±1}` splits
of support at most 3 with their best right-hand sides, and invoke general
normalized separation only when a meaningful gap remains. Reduce
non-primitive directions and re-evaluate each candidate at the original SDP
point before adding it. Put a node or time budget on general separation and
retain its completeness flag. Apply Lemma A’s adaptive norm bound to
certify the found ratio or cap the remaining search; account for small
negative eigenvalues when checking stored matrices. A capped search can
supply valid useful cuts;
failure to find one is not a certificate.

The evidence for this policy is specific: the existing families already
close almost all of the gap on these distributions (§6); the support-at-most-3 extension
closes the gap on 6 of the 12 selected instances; general splits close 4 more (§9). On the
two dense exceptional instances, the extra separation and SDP rounds cost
about 2400 s for only 0.003784 and 0.002216 percentage points of additional
bound improvement. Dense violations of size 0.1 alone do not imply useful
objective progress. An adaptive stop based on recent bound improvement is a
reasonable solver heuristic, but was not compared experimentally here.

**Exactness and rank.** Theorem 3 remains a proved result for exact rational
psd input. Numerical rank is useful for describing the SDP points; it does
not justify treating a truncated rational neighbour as the original input.
With exact reduction, the root-neighbour experiment returns short splits
with raw violation near `¼`. At rank 1, Euclid followed by exact reduction
supplies short certificates; the nine fractional roots confirm this directly.
Their raw maximizers have much worse normalized violation than elementary
or pair splits. All 13 non-root returned splits have maximum coefficients
at least 30; eight are not violated at the stored point, and the other five
have normalized violation at most `8.2·10⁻⁶`. None is useful here.
At four completed nearly closed neighbours, every exact maximizer is long:
the returned vectors are within 1.5% of shortest, and their stored values
come almost entirely from discarded eigen-directions (§8). Exact raw
maximization on rank-truncated neighbours causes this failure, so neighbour
validation remains necessary. The rank also rises along cutting loops,
removing much of the low-rank advantage near their limits.

**Choose cuts for numerical use.** Lemma A proves that normalized violation
penalizes large direction norms; Lemma B proves that primitive directions
suffice, and Proposition E gives a polynomial search for a fixed normalized
threshold. None of these proves that normalized violation maximizes bound
improvement or total solver speed. The lattice implementation is attractive
at the tested sizes up to 30. At larger sizes, try the adaptive post-check
before treating a capped result as a heuristic: it certifies all 16 capped roots and one capped final point
here, leaving 3 of 123 results uncertified (§8). The 30 s box-constrained
MIQP experiments spend much longer on a different objective and frequently return dense cuts whose
raw violation is near `¼`; they provide no all-split optimality certificate.

**What the hardness result predicts.** It rules out efficient exact
separation in the worst case, including after de Meijer et al.'s families.
It does not predict that every SDP optimum is difficult.
[Binary-separation Corollary 6](../binary-separation/note.md) extends strong
NP-hardness to positive definite binary points passing Boolean quadric
triangle inequalities, with `{0,±1}` violators; those points were not used
in this stream’s timing experiments. The constructed
Corollary 5 violations fall below `10⁻³` at all tested orders at least 18;
a solver using that fixed tolerance ignores them. The benchmark exceptions
share a dense-search difficulty, but their larger violations and rank
deficiency do not reproduce the reduction. Total branch-and-bound runtime,
node counts and the best adaptive separator policy remain unmeasured.

## Revision after review round 1

Date: 2026-10-03. Revised after the [independent review](reviews/review-r1.md);
the [round-2 review](reviews/review-r2.md) subsequently confirmed these
fixes and identified the residual non-root reporting issue addressed below.

1. **Major issue 1 and issue 9:** replaced the unreduced column form with
   reduced HNF, added exact graph-lattice preconditioning and Fraction LLL,
   and replaced floating shortening with exact Babai and affine embedding.
   Retained both enumeration flags and removed the hidden 200-candidate
   verification limit. Reran all 113 selected rank-at-most-12 points and
   independently checked the nine fractional rank-1 roots (§8). Rewrote
   Summary, §§8, 11, 12, Limits and Open question 2 around the corrected
   evidence and the distinction between raw and normalized violation.
2. **Issue 2:** added the adaptive norm-bound post-check with code and logs.
   It numerically certifies 17 capped searches, bringing the finished or
   certified count to 120 of 123. Added this check to the solver policy.
3. **Issue 3:** fixed minimization’s best-known rule in `summ_points2.py`.
   It now validates the rounded integer point and evaluates its feasible
   objective. DM60 becomes 12 closed, 98.4% mean closure, 9.91% mean root gap.
4. **Issue 4:** `summ_loop_bt.py` now checks all supports 1–3 and the returned
   raw violation. Its per-`p` means sum to the text’s 2057 general-only rounds.
5. **Issue 5:** Proposition C(c) now restricts non-primitivity and strict
   domination to `D ≥ 4`; `D = 2, 3` give equality with the elementary split.
6. **Issue 6:** restricted the remark to the proved 0/1 result, labelled the
   signed extension unproved here, and corrected the box-MIQP reference to §8.
7. **Issue 7:** renamed the X3C parameter `k` in §§4 and 10, including the
   table heading, so the split value keeps the name `q`.
8. **Issue 8:** restricted the dense-exception claim to the stored separation
   selection and `dmfam`/`dmplus`, and acknowledged BT10’s full-support rounds.
9. **Issue 10:** Summary and §6 distinguish 11 established numerical gaps
   from the unresolved linear DM60 instance’s upper bound.
10. **Optional issues 11–17:** specified both family-violation medians;
    corrected the total to 5168 normalized calls while retaining the `bt`-mode
    timing definition; reported the reviewer’s cap-sensitive dense ratios;
    credited Letchford’s separation question; cited the binary stream’s
    Corollary 6 after checking its statement; attributed the unlogged first-run
    load to the transcript; recomputed the reset eigenvalue; and fixed
    “extension closes”. The revision reporting check verifies the changed
    numbers from their saved records.
11. **Status and commit wording:** the header records the independent review,
    this revision’s unconfirmed status and outside repository sweeps.
    This program makes no commits. `PROGRAM.md`, reviews and the protected load log were
    left unchanged because they are outside the authorized edits.

## Revision after review round 2

Date: 2026-10-03. Revised after the
[independent round-2 review](reviews/review-r2.md); this revision has not
been independently re-reviewed; its fixes were checked by the coordinating agent.
The main conclusions are unchanged.

1. **Minor issue 1:** replaced “mixed” and “some” with the full non-root
   result in §§8 and 12: all 13 returned vectors have maximum coefficients
   30–69618975, eight are unviolated, and the other five have normalized
   violation at most `8.2·10⁻⁶`. Added an independent check of exact
   neighbour/stored values and the discarded-eigenvalue contribution.
   Exact enumeration of every maximizing image and stronger projection
   bounds rule out short exact maximizers at four completed nearly closed
   neighbours; the returned norms are within 1.5% of shortest. Restricted
   the coefficient blow-up correction to roots in §4 and Limits, and stated
   the remaining uncertainty at the other neighbours.
2. **Optional issue 2:** `thm3_exact` always adds the first enumeration’s
   minimizer to the exact-check candidates, including when the second
   enumeration is capped and nonempty. Added a regression for that case
   and kept the candidate-201 regression independent of the first minimizer.
   Reran all 113 Theorem 3 points: vectors, exact values, supports and flags
   are unchanged. No claim changes.
3. **Optional issue 3:** changed §8’s “post-check below” to “above”, §4’s
   supporting reference from §6 to §8, and clarified §7’s averages: our
   gap and both rounds columns use all 10 instances per `p`; closure
   columns use open instances in their respective samples. The B–T
   columns retain published averages with the same averaging conventions.
4. **Optional issue 4:** stated that pivot-row and first-column procedures
   return identical vectors, denominators and exact/stored values at all
   10 rank-1 roots. The main `thm3_exact` returns coefficients 1–5 at the
   nine fractional roots; the separate affine-LLL check still gives ≤4.
5. **Status and scope:** the header records the round-2 revision and its
   unconfirmed status. All edits are inside this stream. Review files,
   `logs/machine_load_run2.txt`, `PROGRAM.md`, commits, staging and branches
   are unchanged.

## Checks actually run

**Review-r2 revision checks.** Commands ran from this stream with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`, under
`timeout`. At most three single-thread Python computations ran at once.
Only this topic was checked; no project-wide verification or CI status/logs
were inspected.

| Command | Output | Outcome |
| --- | --- | --- |
| `timeout 300s python3 code/check_nonroot_r2.py` | `logs/nonroot_r2.txt`, `.jsonl` | Exit 0; 13 exact neighbour/stored values reproduced; eight unviolated, five normalized violations ≤`8.2·10⁻⁶`; exact checks of all maximizing images at four completed neighbours prove the long-vector bounds and the 1.5% comparison. |
| `timeout 300s python3 code/test_revision_r1.py` | `logs/test_revision_r2.txt` | Exit 0; all existing revision regressions pass, including candidate 201; the new nonempty capped-collection regression retains and exactly checks the first minimizer. Reran after strengthening candidate 201’s test. |
| `timeout 300s python3 code/test_lattice.py` | `logs/test_lattice_r2.txt` | Exit 0; all 150 random rational, 200 Theorem 1, 200 rank-1, 200 positive-definite and 60 normalized comparisons pass. |
| `timeout 1000s python3 code/rerun_thm3_r1.py logs/thm3_r2.jsonl` | `logs/thm3_r2.out`, `.jsonl` | Exit 0; all 113 points, no errors, 111 returned vectors, 99 combined complete flags. |
| `timeout 60s python3 code/summarize_revision_r2.py` | `logs/revision_summary_r2.txt` | Exit 0; every vector, exact value, coefficient, support and flag agrees with r1; all 10 rank-1 results agree between rationalizations; main coefficients 1–5 at nine fractional roots; all 13 reviewer coset bounds reproduced. No claim changes. |
| `timeout 60s python3 code/check_closeout_note.py` | `logs/note_check_r2.txt` | Exit 0; revised status, both revision sections, 42 local links and saved headline counts/flags pass. |

Inline Python checks under `timeout 60s` passed: `ast.parse` of all five
changed or added Python files, and three exact-ball boundary comparisons
against exhaustive enumeration (a negative center, rational cross terms
and an empty zero-radius ball).

An inline SHA-256 comparison with the start-of-task snapshot confirms that
all 28 protected review/load-log files, git HEAD and the git index are
unchanged (`logs/scope_check_r2.txt`). The final command
`pgrep -af '^python3 (code/|reviews/r2-code/)' > logs/process_check_r2.txt`
exited 1 with no matches. No experiment or child process from this task
remains running. These are targeted local checks, not CI checks.

An initial non-root check used an unnecessarily large exact enumeration
radius for coset projections. It was terminated (exit 143), then rerun
with an exact nearest-plane candidate providing a smaller radius. The final
successful log supersedes that exploratory output. The reviewer’s
one-direction bound gives a 1.5408% comparison at one point; the new
two-direction bounds prove a comparison within 1.5% for every maximizing
coset at all four points, rather than relying on that rounding.

**Review-r1 revision checks.** Commands ran from this stream with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`, under
`timeout`, with at most four single-thread Python computations at once.
Only this topic was checked; no project-wide checks or CI status/logs were
inspected. No experiment or child process remains running at closeout.

| Command | Output | Outcome |
| --- | --- | --- |
| `timeout 1000s python3 code/rerun_thm3_r1.py logs/thm3_r1.jsonl` | `logs/thm3_r1.out`, `logs/thm3_r1.jsonl` | Exit 0; all 113 points, no errors, 111 returned vectors, 99 combined complete flags. |
| `timeout 1700s python3 code/certify_ratio_r1.py logs/ratio_certificates_r1.jsonl 2e8` | `logs/ratio_certificates_r1.txt` | Exit 0; 110 norm certificates, 17 newly certified caps, 120 finished or certified, no discrepancy above `10⁻⁶`. |
| `timeout 120s python3 code/check_rank1_short_r1.py` | `logs/rank1_short_r1.txt`, `.jsonl` | Exit 0; all 9 fractional rank-1 roots have exact `−¼` with coefficients ≤4, still violated at the stored point. |
| `timeout 300s python3 code/test_revision_r1.py` | `logs/test_revision_r1.txt` | Exit 0; 40 HNF/unimodularity/kernel checks, a 350-digit kernel, both enumeration flags, candidate 201 and Proposition C(c) boundaries pass. |
| `timeout 300s python3 code/test_lattice.py` | `logs/test_lattice_r1.txt` | Exit 0; all 150 random rational, 200 Theorem 1, 200 rank-1, 200 positive-definite and 60 normalized comparisons pass. |
| `timeout 300s python3 code/check_props.py` | `logs/check_props_r1.txt` | Exit 0; all 300 identities, 200 kernel-parity checks, 3150 subset-sum instances and 500 domination identities pass. |
| `timeout 60s python3 code/summ_points2.py` | `logs/summary_points_r1.txt` | Exit 0; DM60 `9.91`, `12 / 98.4`. |
| `timeout 60s python3 code/summ_loop_bt.py logs/loop_bt_BT10.jsonl` | `logs/summary_bt10_r1.txt` | Exit 0; corrected per-`p` means agree with 2057 rounds. |
| `timeout 900s python3 reviews/r1-code/r1_tables.py` | `logs/tables_recomputed_r1.txt` | Exit 0; independently reproduces the original tables, best-known correction and 5168-call count. Reads review code without editing it. |
| `timeout 60s python3 code/summarize_revision_r1.py` | `logs/revision_summary_r1.txt`, `.json` | Exit 0; all revised counts, table cells, medians, dense-ratio changes and the congruence eigenvalue check pass. |
| `timeout 60s python3 code/check_closeout_note.py` | `logs/note_check_r1.txt` | Exit 0; status, sections, local links, historical audit and revised counts/flags pass. |

An inline `ast.parse` check of all ten changed/added Python files also
passed. The final process check was
`pgrep -af '^python3 (code/|reviews/r1-code/)' > logs/process_check_r1.txt`;
it exited 1 with no matches, confirming that no matching Python computation
remained. These are targeted checks, not CI checks.

Exploratory probes exposed an assertion failure in the installed SymPy LLL
on a huge kernel; the final code uses Fraction LLL instead. An initial
kernel-only experiment was interrupted (exit 143), and a 60 s probe timed
out (exit 124). A preliminary complete rerun is retained in
`logs/thm3_r1_preliminary.*`; it revealed the inherited 200-candidate
verification limit, which was then removed. The final run uses exact
integer arithmetic with a shared denominator to verify all collected
candidates efficiently. Preliminary statistics are superseded by the final
records; these exploratory exits are not successful checks.

**Historical author-closeout checks.** The commands below were run by the
closeout author before independent review. They read existing records and
stored matrices and do not describe the review-r1 rerun.

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout 300s python3 code/check_props.py > logs/check_props_closeout.txt 2>&1
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout 300s python3 code/test_lattice.py > logs/test_lattice_closeout.txt 2>&1
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout 60s python3 code/audit_closeout.py > logs/audit_closeout.txt 2>&1
OMP_NUM_THREADS=1 timeout 60s python3 code/summ_sep2.py --rows > logs/summary_sep_closeout.txt
OMP_NUM_THREADS=1 timeout 60s python3 code/summ_points2.py > logs/summary_points_closeout.txt
OMP_NUM_THREADS=1 timeout 60s python3 code/summ_loop_bt.py logs/loop_bt_BT10.jsonl > logs/summary_bt10_closeout.txt
OMP_NUM_THREADS=1 timeout 60s python3 code/summ_loop_bt.py logs/loop_btfam_BT10.jsonl > logs/summary_btfam10_closeout.txt
OMP_NUM_THREADS=1 timeout 60s python3 code/summ_loops_dm.py > logs/summary_dm_closeout.txt
OMP_NUM_THREADS=1 timeout 60s python3 code/summ_hard.py cor5 > logs/summary_hard_cor5_closeout.txt
OMP_NUM_THREADS=1 timeout 60s python3 code/summ_hard.py thm1 > logs/summary_hard_thm1_closeout.txt
OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 60s python3 code/check_closeout_note.py > logs/note_closeout_check.txt
pgrep -af split-practice
pgrep -af 'machine_load_run2|/proc/loadavg'
```

All final Python check executions exited 0. `check_props.py` reports 0 failures for
300 Lemma A identities, 200 kernel-parity checks (140 rank-deficient,
21 attaining exact `−¼`), 3150 rank-1 subset-sum instances (2259 solvable),
and 500 non-primitive domination identities. `test_lattice.py` passes the
150 random rational matrices, 200 reduction comparisons, 200 rank-1
comparisons, 200 positive-definite reduction comparisons and 60 normalized
separator comparisons reported in §5. The earlier saved
`logs/test_lattice_run2.txt` gives the same counts and outcomes.

The note check passes the finalized-section, local-link and headline-count
checks (first run inline, then saved as `check_closeout_note.py`). The two
`pgrep` checks exit 1 with no matches: no stream experiment or load-logging
loop remains, and no process needed to be stopped. These exit codes indicate
absence of matching processes, not failed mathematical checks.

The audit asserts shard/selection agreement and uniqueness, absence of
terminal tracebacks, the 12-instance coverage of each DM loop, and
`ratio = −q/‖w‖²` for returned vectors. It saves counts, quantiles,
first-run comparisons, raw-point evaluations, rank/face checks, loop bounds,
hard-instance values and the longer Gurobi results to
`logs/audit_closeout.json`. Its first invocation failed on a missing BT20
`opt` field; the summary code was corrected to use `opt_gurobi.jsonl`, and
the subsequent executions passed. This was an audit-script failure, not a
failed experiment.

**Earlier experiments relied on.** Their saved outputs establish outcomes
and parameters, but do not contain the full launching shell commands,
outer timeouts or all worker arguments. The producer entry points and
recoverable arguments are recorded below; these are not claims that the
closeout author reran them or recovered a shell transcript.

- `code/exp_points.py SET [workers]`, for SET = BT10, BT20, BT30, BT50,
  DM30, DM60: `run_points_BT10.out`, `run_points_rest.out` and
  `points_*.jsonl` record all 187 roots and final solves, plus 374 attempted
  face solves (10 failures). Bounds and ranks are reproduced by the summary.
- `code/gurobi_opt.py SET logs/opt_gurobi.jsonl 300`, for the five sets other
  than BT10: `run_opt.out` has 77 results, 70 optimal statuses and 7 time
  limits. The longer commands are
  `python3 code/gurobi_opt.py DM60 logs/opt_gurobi_long_1.jsonl 3600 logs/long_opt_1.txt`
  and
  `python3 code/gurobi_opt.py DM60 logs/opt_gurobi_long_2.jsonl 3600 logs/long_opt_2.txt`;
  each filter has one name and each output has one result (§9.1).
- `python3 code/exp_splitloop.py MODE SET logs/loop_MODE_SET.jsonl 2`,
  MODE = `bt`, `btfam`, SET = BT10, BT20, as recorded in §7: all 256
  instance runs are present. The extra BT10 repetition has 110 records and
  identical final bounds. The BT20 general loop reaches its 150-round cap
  on 13 of 18 instances; this is not a completed split-closure computation.
- The `dmfam`/`dmplus` commands with `40 2400` and `logs/open_gap.txt`
  are given in §9. `run_loop_dm*.out` retain the initial failures and retries;
  `loop_failed_attempts.jsonl` records the two failed attempts. Both final
  logs cover all 12 instances. Ten `dmplus` runs converge and two stop on
  budget; the final `dmfam` runs all stop under their family rules.
- `python3 code/exp_separate.py logs/sep_run2_s0.jsonl $(cat logs/sep_shard_00)`
  and the analogous commands with `s1`/`01` and `s2`/`02` identify the three
  separation batches: 41 records apiece, all selected paths accounted for,
  with the warnings and two caught errors detailed in §8. The first run's
  `sep_A.jsonl` has 84/92 points and `sep_B.jsonl` has 31/31; its timings and
  MIQP outcomes are kept separate.
- `python3 code/exp_hard.py logs/hard_run2.jsonl`, saved in
  `run_hard_run2.out`: 88 records, 80 finished maximum-violation enumerations
  and 8 capped ones. Finished values match the reduction formula to within
  `1.16·10⁻¹⁶`; all first/second-run enumeration values agree.
  `python3 code/exp_hard_long.py logs/hard_long.jsonl 1e10`, saved in
  `run_hard_long.out`: 4 records, the two order-62 searches finish and the
  two order-77 searches hit the cap (§10).

The shell form containing `$(cat ...)` above reconstructs the input-list
expansion from the shard files; its original shell spelling is not retained.
The earlier literature checks are documented in §2 and `sources/MANIFEST.md`;
they were not repeated at closeout. Failed attempts and incomplete results
are preserved, rather than silently counted as successful checks.

## Limits

- These are new random draws from published generators, not the papers'
  original instance files. Sizes are 10–60, with few seeds for larger sets;
  DM30 is below de Meijer et al.'s reported size range. Ratio-constrained
  TQP, node relaxations and application data were not studied.
- The implemented families and stopping rules differ from the published
  solver (§3). Pentagonal separation is a local-search heuristic and
  heptagonal cuts are omitted. "After de Meijer families" always refers to
  this implementation; it does not certify the full published closure.
- Ranks and integral endpoints are numerical. Clarabel often reports
  `optimal_inaccurate`; 10 face solves failed. A negative result from trace
  or random face re-optimization is not proof of a minimum achievable rank.
  SDP bounds and inferred optimality are not exact rational certificates.
- Floating enumeration, clipping, residual tolerances and positive starting
  thresholds limit exactness (§5). Node caps give lower bounds on the best
  normalized violation; zero or a finished flag does not certify an exact
  all-split closure. Box MIQP compares a different restricted objective.
- Fixed-rank lifting uses one pivot-row rationalization and exact LLL/Babai
  and embedding shortening, which need not find the shortest representative.
  Pivot-row and first-column procedures return identical vectors at all 10
  rank-1 roots.
  Shortening removes the coefficient blow-up at the roots. All 13 returned
  non-root vectors are unusable here; at four completed nearly closed
  neighbours every exact maximizer is long. The returned vectors’
  stored-point failures come from discarded eigen-directions (§8).
  The other two nearly closed
  bounds are inconclusive, and capped open-point bounds cover only the
  returned coset. Exact algebra does not make the floating
  enumeration or approximate SDP input an exact global certificate.
- Seven original DM60 optimization runs are time-limited; one of the two
  exceptional instances is resolved later only to Gurobi's requested
  tolerance (§9.1). Remaining gaps against unresolved incumbents are upper
  bounds. The cutting-loop comparisons follow different paths from the root.
  The support-at-most-3 extension also tightens the support-1/2 tolerance and
  chooses their best right-hand sides, so it is not an isolated triples test.
- Timings were collected on a shared host under changing load; there are no
  per-record timestamps or controlled CPU-time comparisons. One inherited
  duration is negative. Even `dmfam` computes the general separator for
  diagnostics, so its measured time is not the cost of a pure polynomial
  family implementation.
- The hard-instance generator plants an exact cover but does not ensure
  uniqueness. Absence of a tested small-support `{0,±1}` violator does not
  prove that only dense general splits are violated at a benchmark point.
  No branch-and-bound runtime or node-count comparison was made, and the
  literature search is limited to its recorded date and sources.

## Open questions

1. Does adding three-index splits and budgeted normalized separation improve
   total branch-and-bound time on the original DM sizes 60–120 and on
   application instances? What stopping rule balances bound progress against
   SDP re-solve time?
2. How should a fixed-rank separator control rationalization error at
   higher-rank final points and choose among raw maximizers? Exact reduction
   already finds short valid maximizers at the fractional rank-1 roots. A
   coefficient box changes the separation problem and can discard its exact
   maximizer; an error budget needs a clear formulation.
3. Why do these generators produce rank-1–5 roots but much higher-rank open
   points after cuts? Are the open optimal faces singletons, or do lower-rank
   optima exist that the two face heuristics miss?
4. What distinguishes the dense DM60 exceptions from the other points? The
   QUTO residual gap is now established to solver tolerance; the linear
   instance's true optimum remains unresolved. No new long optimization is
   needed to state that limitation.
5. How does normalization by `‖w‖²` compare with cut efficacy using the full
   lifted coefficient norm, or with estimated objective improvement? Can
   separation certify the absence of useful cuts under such a criterion
   without maximizing vanishing raw violations?
6. Are there application-derived SDP points resembling the full-rank X3C
   reduction after all published families, including omitted heptagonal
   cuts? The present sample gives no evidence that the precise hard
   construction occurs as a benchmark SDP optimum. The binary construction
   in [Corollary 6](../binary-separation/note.md) gives a second family to
   compare with application-derived points.
