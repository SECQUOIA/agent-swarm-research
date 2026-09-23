# Review of `investigation.md` (Eigen-CG Conjecture 1, arXiv:2604.00932)

Reviewer date: 2026-09-23. All checks below were done with the reviewer's own code in
`/tmp/rev_ecg/` (not added to the repo). The scripts are `exact_check.py`, `enum_sanity.py`,
`bqp5.py`, `cases.py`, `bd.py`, `v397.py`, `fp.py`, `fp2.py` and `tightw.py`. Exact work used
`~/miniconda3/envs/exact-quadratic-hull/bin/python` (Fractions, sympy). SDP, LP and qhull work
used `~/miniconda3/envs/minlp-notes/bin/python`.

## Verdict summary

| Claim | Verdict |
|---|---|
| Definitions quoted from the paper (Sec. 1) | Correct |
| Well-posedness: `P_BH(n)` is a polytope, "implied" is unambiguous (Sec. 3.1) | Correct; the citation checks out, but see the note on Sec. 3.2 |
| Sec. 3.2 "`P_BH(n)` is the switched hypermetric polytope" and "gap inequalities with σ(b) odd" | Overstated or mislabelled; not proved; not needed for (a) |
| 3.3 `P_BH ⊆ PSD`; 3.4 identity for `F` | Correct |
| (a) `n <= 5` and support at most 5 | Correct (independently verified: all 368 facets of `BQP_5` are BH) |
| (b) `v0^2` integer | Correct |
| (c) rational direction plus the distance condition | Correct; "two BH suffice" needs "plus nonnegativity BH" |
| (d) all `v_i` equal | Correct |
| Sec. 5: (13)–(15) are CG cuts of `K`; `z13, z14, z15 ∈ P_BH(6)` violate them by 1/6 | Correct, verified exactly |
| Sec. 3.4 / 5: "E-CG = rank-one CG cuts of `K`" | Correct up to domination |
| Sec. 0 / 6.2: diagnosis of the two false positives ("violates BH only for `|w_i|` in 7..10"; "bounded separation such as `|w_i|<=2` is insufficient") | **Wrong.** The point violates a BH with `|w_i| <= 2`. The false positives came from a wrong "OPTIMAL" answer by the Gurobi MIQP separation. |
| 6.4: 397 vertices exactly in `P_BH(6)`, `det = 1/139968`, 56 tight | Correct. The claim "391 with denominator 6, 6 with denominator 3" does not match the shipped JSON. |

## 1. Definitions and well-posedness

**Quotes.** I checked eqs. (7), (8), (9), Definition 1, `F0`/`F1`/`F2`, Lemmas 2–4, Conjecture 1,
and the statements on p. 4, p. 9, p. 14 (text line 796), p. 16 (`L_i=-2, U_i=2`, line 888) and
p. 22 against `code/paper_2604.00932v1.txt`. All match. The investigation's `BH(k,σ), BH(k+1,σ)`
are the paper's `E-CG(a∓1/2, r)` from Lemma 4, via Lemma 3.

**Why finitely many BH suffice.** The investigation relies on the paper's citation [33], so I
checked the source (Letchford–Sørensen, Math. Program. 131 (2012), preprint pp. 267–269):
- Their eq. (8) is exactly the BH family, with `b_{n+1} = w0`, over all of `Z^{n+1}`.
- Prop. 18 shows that `z` satisfies all BH iff a lifted point satisfies all hypermetric
  correlation inequalities of order `n+1`.
- Corollary 4 ("the rounded psd inequalities define a polytope") follows from
  Deza–Grishukhin–Laurent (1993): the hypermetric cone is polyhedral.

So `P_BH(n)` is an affine slice of a polyhedral cone, bounded by BH box inequalities. It is a
nonempty polytope and has a finite BH subsystem. The Farkas equivalences (i)–(iii) then hold.

Minor points:
- `x_i <= 1` is itself a BH for every `n` (`w = e_i, w0 = -1`), not only for `n = 1`.
- `x_i >= 0` is BH with `w = e_i, w0 = 1`.

**Sec. 3.2 is overstated.** The map `b = (w, Σw + 2w0 - 1)` is correct, and every odd-sum `b`
arises. But:
- The inequalities `(bᵀŷ)^2 >= 1` are the *rounded psd* (k-gonal) inequalities. Gap
  inequalities have right-hand side `gap(b)^2`. The two coincide only when `gap(b) = 1`, which
  is exactly the case of switchings of hypermetric inequalities.
- "`P_BH(n)` is the switched hypermetric polytope on `n+1` points" additionally requires every
  BH with `gap(b) >= 3` to be implied by the gap-1 ones. The note gives no proof. I found none in
  L–S, who needed the lifting to `n+2` points to get polyhedrality.

Only the inclusion `P_BH(n) ⊆ switched-HYP_{n+1}` is needed for (a), and it holds. The
equality is used informally in Sec. 6.4 and Sec. 8 ("derivable from HYP_7"). It should be
stated as a conjecture, or the correct object should be used: a slice of the hypermetric cone
on `n+2` points.

## 2. Proved special cases

**(a) `n <= 5` / support at most 5.**
- Lemma 1 (E-CG valid for `BQP`) is immediate.
- For `n <= 5`: `P_BH ⊆ switched-HYP_{n+1} = CUT_{n+1}` (covariance image) for `n+1 <= 6`.
- Independent check (`bqp5.py`): I computed `BQP_5` with qhull and found 368 facets, which
  matches the known facet count of `CUT_6`. Each facet is a positive multiple of a BH with
  `|w_i| <= 3`. So `P_BH(5) = BQP_5` exactly.
- The support reduction is correct. Coefficients off `S` are `⌈0⌉ = 0`, and BH on `S`,
  zero-padded, are BH on `[n]`.

Verdict: proved.

**(b) `v0^2 ∈ Z`.**
- Identity checked: `F = q_M(ŵ) + Σρ(p_i)x_i + Σρ(q_ij)X_ij - frac(v0^2)`.
- `P_BH ⊆ K` holds by 3.3 (the `t → ±∞` scaling argument is sound) and BH nonnegativity.
- Numerical test (`bd.py`): 150 random `n = 6` cuts with integer `v0` and Gaussian `v`. The
  minimum of E-CG over `K` (Clarabel) was `-7.6e-9`, which is solver zero.

Verdict: proved.

**(c) Rational direction.** I re-derived the argument:
- `λ(u)(u-1) + μ(u+1)u = ρ^2[(h+τ)^2 - (τ-k)^2]` with `u = h+k`.
- `λ = ρ^2(1-2(τ-k))/2 >= 0` and `μ = ρ^2(1+2(τ-k))/2 >= 0` iff `|τ-k| <= 1/2`.
- The rounding residuals are in `[0,1)` and are covered by `x_i >= 0` and `X_ij >= 0`, which
  are BH.
- The combined constant is `v0^2 - (v0-kρ)^2`.
- The reduction of Lemma 4 is correct: in `F2`, `v0^2 - (v0-kρ)^2 = k(2v0ρ) - k^2ρ^2 ∈ Z`.
- The `F3` counterexample polynomial `(h-1)(h-4)/4` checks out.

Exact test (`cases.py`), 20,000 random cases with rational `ρ` and `n` from 2 to 7:
- In all 20,000 cases the certificate identity holds and all residuals lie in `[0,1)`.
- When the condition holds (10,016 cases), the certificate proves the cut in all of them.
- When the condition fails (9,984 cases), the constant is too large in all of them, so the
  condition is sharp for this certificate.
- 300 cases with irrational `ρ` were checked in sympy; the condition held in 171, and all 171
  were proved.

Verdict: proved. The summary's "two BH inequalities suffice" should read "two BH plus the
nonnegativity BH `x_i >= 0`, `X_ij >= 0` for the rounding slack". Exactly two suffice only
without rounding, as in Lemma 4.

**(d) Constant `v`.**
- The cut and `P_BH` are both `S_n`-invariant, so symmetrization is valid.
- BH with `w = 1` and `w0 = -k` is the chord through `(k, k(k-1))` and `(k+1, k(k+1))`.
- Summed McCormick gives the upper chord `m2 <= (n-1)m1`.
- Together these give `conv{(k, k(k-1))}`, which is the symmetric slice of `BQP_n`.

LP test (`bd.py`): 3,000 random cases with `n` from 2 to 10, minimized over only these
constraints. The minimum was exactly `0.0`. 1,892 of these cases are not covered by (c).

Verdict: proved.

## 3. Negative result (Sec. 5), verified exactly (`exact_check.py`)

I typed facets (13)–(15) myself from the paper text, independently of `facets.py`. For each
facet:
- **Facet check.** It is valid on all 64 points of `{0,1}^6`, with 21 tight points of affine
  rank 21, so it is a facet.
- **Certificate** (`cg_certificates.json`):
  - `S` is symmetric and PSD by an exact rational `LDL^T` that allows zero pivots. All pivots
    are positive; the minimum pivot is about 0.02, so `S` is in fact positive definite.
  - `N_i = a_i - 2S_0i - S_ii` and `N_ij = a_ij - 2S_ij` satisfy `N >= 0`, with minimum
    `9999/10^6` or `1/100`.
  - The identity `a·z + S_00 = <S, M(z)> + N·z` was checked at random rational `z`.
  - `⌈-S_00⌉ = -2, -5, -1 = -c`.
- **Integer points of `K`.** The 2×2 and 3×3 minors of `M(z)` force `z` to be a binary point
  with `X_ij = x_i x_j`, so a CG cut of `K` is valid for `BQP_6`. Hence each facet is a CG cut
  of `K`.
- **Violating point.** Each `z13/14/15 = (listed)/6` has `z >= 0` and facet value exactly
  `-1/6`. Also `det M = 1/139968 = 2/6^7`, so `M` is positive definite.
- **Membership in `P_BH(6)`.** For positive definite `M`, `g(ŵ) = (ŵ - e0/2)ᵀM(ŵ - e0/2) - 1/4`,
  because `c = M e0`. So `P_BH` membership is equivalent to "no integer point strictly inside
  a bounded ellipsoid". I enumerated this set exactly with my own Fincke–Pohst on an exact
  `LDL^T`, computing integer ranges by exact comparison. For each point, exactly 56 integer
  `ŵ` have `g <= 0`, all with `g = 0`, and none is violated.
- **Enumerator sanity check.** At a positive definite point that violates the clique
  inequality, the enumerator found both violators, matching brute force over `|w| <= 3`.

The author's certification method (`exact_bh_separation_general`, the same ellipsoid
enumeration with float radius plus ±1 padding and exact acceptance) is sound for these
positive definite points. I also re-certified all 397 surveyed vertices (`v397.py`):
- all 397 are in `P_BH(6)`, with `det = 1/139968` and 56 tight points each;
- `6M` is even, integral and has determinant 2, which is consistent with E7;
- every vertex has lcm-denominator 6 (x-part in `(1/3)Z`), which contradicts the claim
  "391 with denominator 6, 6 with denominator 3".

The consequence "CG closure of `K` ⊊ `P_BH(6)`" is correct:
`BH ⊆ E-CG ⊆ CG(K)`, and `z13 ∈ P_BH \ CG(K)`.

## 4. "Eigen-CG cuts are exactly the rank-one CG cuts of `K`"

- **E-CG is a rank-one CG cut.** It comes from `S = ŵŵᵀ` and `N = ⌈(p,q)⌉ - (p,q) >= 0`.
- **Conversely,** a rank-one certificate `a = (p,q) + N` with integer `a` has `a >= ⌈(p,q)⌉`.
  Scaling `S` is absorbed into `ŵ`. It yields `a·z >= -⌊v0^2⌋`, which the E-CG cut dominates on
  `z >= 0`.
- `K` has a Slater point (`x = 1/2`, `X = 1/4`), so the conic multiplier form loses nothing.

Verdict: correct, with "exactly" meaning "up to adding nonnegativity multiples".

## 5. Error found: the false-positive diagnosis in Sec. 0 and 6.2 is wrong

The point `z = (3,5,3,3,3,3 | 1,0,2,2,2,2,2,2,2,1,1,1,1,1,1)/8` violates the BH
`(w0,w) = (0, 2,1,1,-1,-1,-1)` with value `-1/2`, checked exactly (`fp2.py`). Twelve BH with
`|w_i| <= 2` are violated.

The cause of the false positives: the author's `separate_bh(6, z, W=6)` returns Gurobi status
OPTIMAL with objective and bound both `0.0`, in 0.0 s. The true minimum over `|w_i| <= 6` is
`-2.5` (brute force, `fp.py`). With `W = 2` the same routine finds `-0.5`. So Gurobi's
nonconvex MIQP returned a wrong "optimal" answer on a nearly-PSD `M`
(`det M = -3/65536`).

Consequences:
- Remove the statements "violates a BH inequality only for some `|w_i|` between 7 and 10" and
  "smallest violated BH found has `|w_i| = 10`". The `-6.75` inequality is the *most* violated
  one, not the smallest.
- The evidence for "bounded separation like the paper's `|w_i| <= 2` cannot certify
  membership" is invalid. The general statement ("a bounded family is not a proof") is still
  logically true. Weak supporting evidence: tight BH at the E7 vertices have `|w_i|` up to 3.
- The search conclusions in Sec. 6 are **not** invalidated:
  - LP minima are taken over outer relaxations, so a missed cut can only weaken the
    relaxation. A reported minimum of 0 still means "implied".
  - `complete_separation` is fail-safe. It either certifies exactly or raises an error.
  - The `separate_bh` unreliability should nevertheless be documented.

## 6. Other remarks

- Sec. 4(a): "needs `n >= 6` and full support 6" should read "support at least 6".
- Sec. 6 "implied" results are float LP minima, which the note already states. They are
  evidence, not certificates.
