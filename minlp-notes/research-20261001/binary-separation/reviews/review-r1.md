# Review r1 of the binary-separation note

Date: 2026-10-02. Reviewer: an independent research agent (adversarial review; not
journal peer review). Object: [`note.md`](../note.md), `code/`, `logs/` and
`sources/` of the `binary-separation` stream. My own scripts, logs and downloads are
in [`r1-work/`](r1-work/) (downloads listed with URL and sha256 in
[`r1-work/MANIFEST.md`](r1-work/MANIFEST.md)).

## Verdict

**Major problems (one, easily repaired), plus four minor issues.** The core
mathematics is right. I checked Lemma 0, Lemma 1, Theorem 1, Corollaries 1–2,
Lemmas 2–4 and Theorem 4 line by line and found no error. My independent code
reproduces Theorem 1 exactly, including edge cases the author did not test. All
logs reproduce byte for byte, apart from timing lines. The literature status is
correct as far as it goes.

The major issue is that the *strong* NP-completeness claims for the classes that
are not homogeneous have a missing step. These classes are gap-1, rounded psd,
k-gonal, Boros–Hammer, odd clique, and SPLIT-SEP at binary points. Their hard
points are scaled by `ε = 1/(2δᵀM⁻¹δ)`, and this `ε` has numerators and
denominators of exponential magnitude. Changing `ε` to `1/(8n + 2p + 1)` repairs
it (§M1 below; I proved the needed bound and checked the repair exactly). Theorem 1,
Corollary 2 (strong NP-completeness of hypermetric separation and strong
co-NP-completeness of hypermetricity) and plain NP-completeness of all classes are
not affected.

## What I checked and found correct

- **Definitions and Lemma 0.** The classes, the chain hypermetric ⊂ gap-1 ⊂ rounded
  psd, and the identity `Q(b,d) = −g_M(z)` are correct. I re-derived Lemma 0 by hand
  and symbolically (sympy, `N = 3`).
- **Lemma 1 and Theorem 1.** The Gram representation, the closed form and all five
  `k`-layers are correct. Each step holds:
  - `k ≥ 2`: `(k−1)(p/4 + kη²) > 0`;
  - `k = −m ≤ −2`: `(m+1)(mη² − p/4) ≥ 0` needs `η² ≥ p/8`;
  - `k = −1`: the two nonnegative integer terms against `p/2 − 2η² ∈ (0,1]`.

  An independent box enumeration found no failures on 150 instances (2,218,986
  lattice points), with empty sets, duplicate sets, `η²` at the lower window
  endpoint and `η² = p/4 − 1/64`.
- **Corollary 1.** The formulas for `d`, `Q = 1/2` and the example are correct (4M
  and 4d match the log).
- **Lemma 2 (NP membership).** All three cases are correct. In case 3, `Pw = δ_K`,
  the bound `|yᵢ| ≤ (M_KK)ᵢᵢ^{1/2}‖y‖_G` follows from Cauchy–Schwarz, and `g`
  depends on `z` only through `Pz`. So the HNF step is legitimate.
- **Lemma 3.** (i)–(iii) are correct. For (iv), Avis–Grishukhin's Lemma 4 bounds the
  coefficients of facets of `Hyp_t` by `g₀(t)`. So enumerating each `t`-subset
  within that bound is exact, and polynomial for fixed `t`. The FPT claim follows
  the split note's Theorem 3.
- **Corollary 3 (a)–(d).** The Schur-complement argument (`X − θe₀e₀ᵀ ≻ 0 ⇔ εs < 1−θ`)
  and the parity reduction for `|u₀| ≥ 3` are correct. The translation through the
  split note's §6 identity (`σ = −u₀`, and `b ↦ −b` gives the same inequality) is
  correct.
- **Corollaries 4–7.** The class reductions and NP-membership citations are correct.
  - GKL 2012 Lemma 6 is stated for `x* ∈ [0,1]^E`. This suffices at the hard
    points, and the argument extends to any rational input.
  - Corollary 5's merging argument (copies of `0` are zero rows in Boolean quadric
    form, so `X′ = X ⊕ 0`) is correct.
  - Corollary 6's count `4C(N,2) + 4C(N,3)` equals `4C(N+1,3)` and is correct.
- **Lemma 4 and Theorem 4 (gap-0).** I checked every inequality:
  - the row sums of `θ`;
  - `θ ≥ θ_lb > 0`;
  - `ν ≤ 1/(n(n−1)a_max²)`;
  - `Zᵢᵢ = 1` and `Za = −νa`;
  - `bᵀZb ≥ nθ_lb‖b‖²/a_max²` on `a⊥`;
  - `|sᵀa| < 1` in (⇒).

  The location remark (`n ≥ 6`) is also correct. The author tested `n ∈ {6,8}`.
  My code checks `n = 4`, which the theorem allows: 25 instances, all 16 `s` each,
  0 failures. It uses a different basis of `s⊥`.
- **The Carathéodory argument (§6).** It is correct. If the hard points lay in the
  cut polytope for all no-instances, X3C would be in co-NP.
- **Literature (§2).** I checked every quotation and locator against the saved texts:
  - Avis–Grishukhin 1993 §4: Corollary 6, P1, "We are not able to prove that P1
    is NP-hard", P2, P3, Corollary 10;
  - Avis 2003 §1: (1), "Its complexity status is unknown", P1, P2, the p. 454
    pointer;
  - DGL 1993 Remark 4.12, printed p. 51 (PDF p. 52);
  - Letchford–Sørensen 2012: (5) p. 261, (8) p. 267, (10), Prop. 18 p. 268,
    Prop. 19 and "long-standing open problem" p. 269, §6 "major open question";
  - GKL 2012: §2 references [1,3,9,13,20], Lemmas 1, 2, 3 and 6, Theorems 3 and 7,
    the §4 "unknown" sentence on p. 151, and the wrong venue of [18];
  - Laurent–Poljak LIENS-93-27, printed p. 14 (PDF p. 15).

  All are correct. The corrections to the split note and the review locators
  (split note §6, §8 "Limits"; split-separation-review §8.3; split-final-review
  row "§6 binary analogue") are accurate.
- **Novelty.** The qualification is appropriate ("not found in the sources checked";
  "may be folklore"). My own searches (WebSearch on hypermetricity NP-hardness,
  Delaunay-simplex and empty-sphere hardness, and Boros–Hammer and rounded psd
  separation complexity; a grep of Dutour Sikirić–Schürmann–Vallentin
  arXiv:0804.0036) found no earlier resolution either. The only new finding is the
  2022 statement of openness in §m3 below. The March 2026 paper of Caprara et al.
  (arXiv:2605.02896) on correlation polyhedra concerns membership and rank, not
  hypermetric separation.
- **Experiments.** The SCIP cross-check is a fair, independent floating-point
  optimization check. Its box bound `|zᵢ − wᵢ| < (R(M⁻¹)ᵢᵢ)^{1/2}` is correct, and
  it is not over-interpreted. The gap and cut-cone probes are honestly labeled as
  numerical evidence. No solver performance is claimed. Seeds are fixed, and every
  log reproduced exactly.

## Major issue

### M1. Strong NP-hardness at the scaled points is not established as written

*Where.* Corollary 3(c) defines `X(ε)` with `ε = 1/(2s)`, `s = δᵀM⁻¹δ`. The
following claims use these points:

- Corollary 4: "strongly NP-complete ... even when the input is restricted to the
  points of Corollary 3", for (ii) gap-1, (iii) rounded psd and Boros–Hammer, and
  (iv) k-gonal;
- Corollary 5: odd clique at `εd′`;
- Corollary 6: SPLIT-SEP "strongly NP-complete" at binary positive definite points;
- Summary items 2–3, the §8 discussion paragraph, and the author's results list.

*Problem.* Strong NP-hardness requires the numbers in the instance to be bounded by
a polynomial in the input length. For rational data this means the numerators and
denominators. The split note took care of this: its `G₀₀` is a polynomially bounded
integer. Here `s` is a ratio of minors of `M`, and in general its numerator and
denominator grow exponentially in `n`. The script `r1-work/independent_check.py`, part [C],
shows this on random X3C instances. The digit count of `ε` grows linearly in `n`:

| q, n | 3, 6 | 4, 10 | 5, 15 | 6, 20 | 8, 30 | 10, 40 |
|---|---|---|---|---|---|---|
| digits of numerator / denominator of `ε` | 3/5 | 10/12 | 13/15 | 17/19 | 22/24 | 26/29 |

Hypermetric inequalities are homogeneous, so class (i) and Corollary 2 can use the
integral `4d`, and they are fine. The other classes are not homogeneous: the
unscaled `d` violates perimeter inequalities. So their strong hardness rests on
`ε`, and as written it is unproved. Plain NP-completeness is unaffected, because
`ε` has polynomial bit size.

*Repair (checked).* Use `ε = 1/N` with `N = 8n + 2p + 1`. Every argument in
Corollary 3(c)–(e) needs only `εs < 3/4`, and this choice gives `εs < 1/2`.

*Proof of the bound.* Let `B` have columns `uᵢ` and `u_g`, as in Lemma 1. The point
`c* = (𝟙_n, ½𝟙_p, γ)` with `γ = (η² − p/4)/(2η)` satisfies `Bᵀc* = δ/2`. Hence
`s = 4‖Πc*‖² ≤ 4‖c*‖² = 4n + p + 4γ²`, where `Π` is the orthogonal projection onto
`range B`. For `η² = (p−1)/4`, this gives `s ≤ 4n + p + 1/(4(p−1)) < N/2`. Then
the entries of `X(1/N)` have denominators dividing `4N`.

Part [D] of my script confirms the bound and all of the following exactly on 60
X3C instances, with 0 failures:

- `εs < 1/2`;
- `X` positive definite;
- `X − e₀e₀ᵀ/4` positive definite;
- `εd ∈ [0,1]`;
- `J − 2εD` positive definite.

With this `ε`, the maximum violation is exactly `1/(2N) = 1/(16n + 4p + 2)`. That
also fixes m1.

## Minor issues

### m1. The claimed violation `Θ(1/(n+p))` is not proved and fails in general

*Where.* The Summary ("Relevance for solvers"), §9 ("The violations are small"), the
"Limits" section, and the author's open question 4.

*Problem.* With `ε = 1/(2s)` the violation is `ε/2 = 1/(4s)`. The proved bounds are:

- `s ≥ max(Mᵢᵢ, M_gg)`, which is at least 7 for X3C;
- `s ≤ 4n + p + 1/(4(p−1))` (see M1).

So `1/(16n + 4p + 1) ≤ ε/2 ≤ 1/28`. The upper half of `Θ` fails when `n ≫ p`
(part [D] of my script):

- `n` copies of `{0,1,2}` plus `{3,4,5}`, with `p = 6`: `s = 21.1, 24.7, 25.9` at
  `n = 5, 20, 80`;
- all triples of `[9]`, with `n = 84` and no duplicates: `s/(n+p) = 0.67`, falling
  from 1.43 for all triples of `[6]`.

There the violation stays near `0.01` while `1/(n+p) → 0`. The point "only
polynomially small" (a lower bound) is correct. *Fix.* State the bounds above, or
adopt the `ε` of M1, for which the violation is exactly `1/(16n + 4p + 2)`.

### m2. Corollary 3(e): the proof of `εd ∈ [0,1]` covers only `q ≥ 3`

*Problem.* Corollary 3(e) states `εd ∈ [0,1]^{E(V)}` for every X3C instance with
`q ≥ 2`. The proof derives `0 ≤ εd ≤ 1` from the triangle and perimeter
inequalities, but the triangle inequalities are proved only for `q ≥ 3` (they can
fail for small covers). The claim is true for all `q`. `X(ε) ≻ 0` is equivalent to
`J − 2εD ⪰ 0`, and a psd matrix with unit diagonal has entries in `[−1, 1]`, so
`0 ≤ εd_uv ≤ 1`. My check [E] confirms `εd ∈ [0,1]` on 40 instances whose
triangle inequalities fail. The elliptope statement also holds for all `q`, not
only `q ≥ 3`. *Fix.* Cite the elliptope argument for the box, and drop the `q ≥ 3`
restriction on the elliptope.

### m3. A 2022 statement of openness was missed, and so was a consequence it makes visible

*Problem.* The task asked for results from 2010–2026. The note's table, §7 and the
§8 paragraph stop at 2012 ("all hypermetric sources through 2012 state it as
open"). A later survey states the problem as open: A. N. Letchford, "The Boolean
quadric polytope", in A. P. Punnen (ed.), *The Quadratic Unconstrained Binary
Optimization Problem*, Springer 2022, pp. 97–120. The accepted manuscript is at
https://eprints.lancs.ac.uk/id/eprint/172098/1/qubo_chapter.pdf, saved in
`r1-work/`; the page numbers below are manuscript pages.

- §7.2, p. 18: "The complexity of the separation problems for the inequalities
  (10)–(13) is unknown, but we suspect that they are all NP-hard." Here (10) are
  Padberg's clique inequalities, (11) the cut inequalities, (12) their common
  generalization `(Σ_S x − Σ_T x − s)(Σ_S x − Σ_T x − s − 1) ≥ 0`, and (13) the
  Boros–Hammer inequalities.
- §7.2, p. 19: "At the time of writing, the complexity of separation is unknown for
  the remaining inequalities for the cut polytope." The same paragraph says
  Letchford–Sørensen showed (13), (19), (23) and (25) to be equivalent.
- §8, p. 20, research directions: "Determine whether or not the separation problem
  for the hypermetric inequalities (23) can be solved in polynomial time."

This is the most recent statement I found. It belongs in the §2 table, in §7 and
in the §8 discussion paragraph.

It also shows a consequence the note does not state. At `X(ε)`, every violator
`z = (x, −1)` lies in `{0, ±1}`. A hypermetric correlation inequality with
`z = 𝟙_S − 𝟙_T` is exactly Padberg's cut inequality (11),
`Σ_{S×T} y ≤ Σ_T x + Σ_{S pairs} y + Σ_{T pairs} y`. The violators are therefore
members of (11), and of (12) with `s = 0`, with `S` the cover and `T = {g}`. They
satisfy the facet condition that Letchford states for (12): `|S| + |T| ≥ 3` and
`1 − |T| ≤ s ≤ |S| − 2`, for `q ≥ 2`.

At these points the violated Boros–Hammer inequalities are exactly these. So
Theorem 1 with the `ε` of M1 settles (11), (12) and (13): they are strongly
NP-complete to separate, even at positive definite binary points in the
McCormick/triangle relaxation, with no repeated points. NP membership for (11) and
(12) is trivial. The clique inequalities (10) and the Barahona–Mahjoub inequalities
(18) are not settled, because the violators have mixed signs.

So the "repeated points" caveat of Corollary 5 belongs to GKL's cut-form odd clique
family, where the root coefficient `2 − q` must also lie in `{0, ±1}`. It does not
apply to the Boolean quadric `{0, ±1}` family. *Fix.* Add the source and the
consequence, and qualify "through 2012".

Dey, Jiang, Kazachkov, Lodi and Muñoz (arXiv:2604.00932, April 2026) discuss
Boros–Hammer separation (solved with Gurobi as an integer program) and make no
complexity statement. They could be cited as evidence that the question is still
treated as open.

### m4. §9 misdescribes what the max-cut codes do

*Problem.* §9 says "BiqMac, BiqBin and MADAM separate triangle, pentagonal and
heptagonal inequalities by enumeration". The BiqBin paper (arXiv:2009.06240, §3)
says otherwise: "Similarly as in BiqMac and BiqCrunch, we use triangle
inequalities" (BiqMac: triangles only). It enumerates the triangles, but "separation
of pentagonal and heptagonal inequalities is done heuristically" (simulated
annealing). MADAM (arXiv:2010.07839, §2) says the same: "the separation has to be
done heuristically". These codes also restrict to `b ∈ {0,±1}` with 3, 5 or 7
nonzeros, that is, small odd clique inequalities.

The Summary's wording ("enumerate fixed small families ... or use heuristics") is
closer, but still implies that the codes enumerate the pentagonal and heptagonal
inequalities. *Fix.* Say that triangles are enumerated and that pentagonal and
heptagonal inequalities are separated heuristically even though their families are
of polynomial size. That still fits the point that only bounded families are
tractable.

## Optional

- **o1.** Theorem 1's lower window endpoint `p/8` can be relaxed to the sharp `p/12`.
  The integer minimum of `y² − (m+1)y` is `−⌊(m+1)²/4⌋`. This gives
  `g ≥ (m+1)(mη² − p/4)` for odd `m` and `g ≥ m((m+1)η² − p/4)` for even `m`, both
  `≥ 0` once `η² ≥ p/12`. The note's own control (`η² = p/16`) shows `p/12` cannot
  be lowered. "The window is needed" overstates the necessity of `p/8`. This
  matters only for `p ≤ 3`.
- **o2.** §10 item 4: "For at most 6 points this is uninformative, because the
  hypermetric cone equals the cut cone there." Gap inequalities concern the cut
  *polytope*. By Letchford–Sørensen's Prop. 19, rounded psd inequalities on `|V|`
  points correspond to hypermetric inequalities on `|V| + 1` points. So the
  box-search outcome follows from `HYP = CUT` only for `|V| ≤ 5`, and the 6-point
  runs carry some information.
- **o3.** Corollary 4 should state the input domain of the decision problems
  (arbitrary rational vectors, or `[0,1]^E`). GKL's Lemma 6 is stated for
  `[0,1]^E`. Its proof extends to all rational inputs, because the gap-1
  inequalities are switchings of hypermetric ones and so define a polyhedron with
  facets of polynomial size.
- **o4.** `sources/MANIFEST.md` lists arXiv:1503.04554 as "M. Dutour Sikiric". The
  PDF's authors are M. Deza and M. Dutour Sikirić.

## Checks run by the reviewer

All commands were run from `research-20261001/binary-separation/`, at most two at a
time. Outputs are in `reviews/r1-work/`.

1. `python3 code/check_binary_separation.py`: `ALL CHECKS PASSED`, 18.6 s. Output
   identical to `logs/check_binary_separation.log`, apart from timing lines.
2. `python3 code/check_gap0.py`: `ALL CHECKS PASSED`, 39 s. Identical to the log
   apart from timing.
3. `python3 code/scip_crosscheck.py`: 24 instances, 0 disagreements. Identical to
   the log apart from timing.
4. `python3 code/probe_cutcone.py`: 24 of 24 instances with `εd` in the cut
   polytope. Identical apart from timing and a blank line.
5. `python3 code/probe_gap.py 3`, `python3 code/probe_gap.py 3 5 5 30` and
   `python3 code/probe_gap.py 2 6 6 20`: 27, 12 and 9 no-instances with 0
   violations. All three are identical to the logs.
6. `python3 reviews/r1-work/independent_check.py` (my code; it does not import the
   author's) → `reviews/r1-work/independent_check.log`, `REVIEWER CHECKS PASSED`,
   18.6 s:
   - [A] Lemma 0 and Lemma 1 hold symbolically (sympy);
   - [B] Theorem 1 by exact box enumeration: 150 instances, 105 with a cover,
     2,218,986 points, 0 failures;
   - [C] digit counts of `ε` (table in M1);
   - [D] the bound `s ≤ 4n + p + 1/(4(p−1))` and the repaired `ε = 1/(8n+2p+1)`:
     0 failures on 60 instances; the values of `s` for the degenerate families
     (m1);
   - [E] `εd ∈ [0,1]` when the triangle inequalities fail: 40 instances, 0
     failures;
   - [F] Theorem 4 at `n = 4`: 25 instances, 0 failures.
7. Literature: `pdftotext` page checks for DGL 1993 (Remark 4.12 on PDF p. 52 =
   printed p. 51) and Laurent–Poljak (PDF p. 15). Greps of the saved texts of
   Avis–Grishukhin 1993, Avis 2003, GKL 2012 and LS 2012 for every quotation in
   §2. WebSearch queries for hypermetricity NP-hardness, Delaunay and empty-sphere
   hardness, and Boros–Hammer and rounded psd separation complexity. Downloads, with
   sha256 in `r1-work/MANIFEST.md`: Letchford 2022 chapter, Dey et al. 2026,
   BiqBin, MADAM, and Dutour Sikirić–Schürmann–Vallentin.

I did not check the full Deza–Laurent chapter or Dash's thesis. These were not
accessible to the author either. So the novelty caveat remains necessary.

## Required changes for a clean verdict

1. M1: replace `ε = 1/(2s)` by `ε = 1/(8n + 2p + 1)` (or any polynomially bounded
   integer `N ≥ 2s`), and add the bound `s ≤ 4n + p + 1/(4(p−1))` with its proof.
   Then recheck the code at the new `ε`.
2. m1: correct the `Θ(1/(n+p))` statements.
3. m2: fix the proof of `εd ∈ [0,1]` for `q = 2`.
4. m3: add Letchford 2022 to §2, §7 and §8. State the consequence for Padberg's
   (11) and (12) and the Boros–Hammer inequalities (13), and qualify the
   repeated-points caveat.
5. m4: correct the description of BiqMac, BiqBin and MADAM.
