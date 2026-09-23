# Eigen-CG Conjecture 1 (Dey, Jiang, Kazachkov, Lodi, Muñoz, arXiv:2604.00932)

Date: 2026-09-23. Independently reviewed ([review.md](review.md)); corrections marked in the text. Code: `code/` (paths below are relative to this folder).
Python: `~/miniconda3/envs/exact-quadratic-hull/bin/python` (Gurobi 13.0.3, sympy);
SDP scripts use `~/miniconda3/envs/minlp-notes/bin/python` (cvxpy + Clarabel), because the
first environment has no scipy/cvxpy.

## 0. Summary

- **Status.** Conjecture 1 is still open. I found no resolution and no citing work
  (Section 2). I did not prove or refute it.
- **Well-posedness.** The conjecture is well posed. All natural readings of "implied" are
  equivalent: validity on the BH closure `P_BH(n)`, a finite nonnegative combination, a
  closure/limit. The conjecture is equivalent to "E-CG closure = BH closure" (Section 3).
- **Proved partial results** (Section 4):
  - (a) true for `n <= 5`, and for every `n` when `|supp v| <= 5`;
  - (b) true whenever `v0^2` is an integer (for example `v0 = 0`);
  - (c) true whenever the direction `v` is rational (`v = rho*sigma`, `sigma` integer) and
    `dist(v0, rho*Z)^2 >= frac(v0^2)`. This contains Lemma 4 of the paper (family `F2`), and
    two BH inequalities suffice;
  - (d) true whenever all `v_i` are equal (symmetrization argument).
- **Structural (negative) result, exactly verified** (Section 5). General CG cuts of the
  SDP-plus-nonnegativity set `K = {z >= 0 : M(z) PSD}`, whose PSD multipliers may have rank
  above one, are **not** implied by BH for `n = 6`. The paper's non-BH facets (13), (14) and
  (15) of `BQP_6` are CG cuts of `K`. The rational certificates are in
  `code/cg_certificates.json`, and a rational point of `P_BH(6)` violates each facet by 1/6.
  Eigen-CG cuts are exactly the rank-one CG cuts of `K`. So any proof of Conjecture 1 must
  use rank one essentially, and the obvious strengthening ("the CG closure of `K` equals
  `P_BH`") is false.
- **Computational evidence** (Section 6). No counterexample was found. Every candidate was
  checked by LP over (an outer approximation of) `P_BH`, and every would-be violation was
  checked in exact arithmetic. The searches were:
  - 6,036 "exact-part" cuts for `n = 6`;
  - 50,316 perturbed limit cuts: 10,680 + 39,636 for `n = 6`, and 8,862 for `n = 7`;
  - 100,000 random structured cuts for `n = 6` and 30,000 for `n = 7`;
  - a direct E-CG separation heuristic at 397 exactly certified fractional vertices of
    `P_BH(6)`.

  All 397 vertices are of one type, the E7 / Gosset `3_21` type.
- **Two spurious "counterexamples"** appeared in a first pass with BH separation
  restricted to `|w_i| <= 6`. Both disappeared under exact separation. *Corrected after
  independent review ([review.md](review.md)):* the cause was a failure of that separation
  run (Gurobi reported an optimal separation value 0 while the true minimum is -2.5), not
  large BH coefficients. The point `z` violates the BH inequality `(0; 2,1,1,-1,-1,-1)` by
  1/2, and twelve BH inequalities with `|w_i| <= 2` are violated. The earlier statements
  that `z` violates BH only for `|w_i|` between 7 and 10, and that bounded separation like
  the paper's (18) is therefore insufficient, were wrong and are withdrawn.

## 1. Definitions, quoted from arXiv:2604.00932v1 (pdftotext in `code/paper_2604.00932v1.txt`)

Setting (p. 2). `QPB_n = conv{(x, X) in [0,1]^{n + C(n+1,2)} : X_ij = x_i x_j, 1 <= i <= j <= n}`
(eq. (2)). The Boolean quadric polytope is
`BQP_n = conv{(x, X) in {0,1}^{n + C(n,2)} : X_ij = x_i x_j, 1 <= i < j <= n}` (eq. (5)).
Proposition 1 (Burer–Letchford): an inequality valid for `BQP_n` is valid for `QPB_n`.
All inequalities below live in the space `(x, X_ij)_{i<j}`. There are no `X_ii` variables.

Eigen-cuts (p. 3, eq. (7)):
"sum_{1<=i<j<=n} 2 v_i v_j X_{i,j} + sum_{i=1}^n v_i^2 X_{i,i} + sum_{i=1}^n 2 v_i v_0 x_i + v_0^2 >= 0."

Eigen-CG inequalities (p. 3, eq. (8)):
"sum_{1<=i<j<=n} ⌈2 v_i v_j⌉ X_{i,j} + sum_{i=1}^n ⌈v_i^2 + 2 v_i v_0⌉ x_i + ⌊v_0^2⌋ >= 0.
We call these Eigen-CG inequalities or Eigen-CG cuts."

Boros–Hammer inequalities (p. 3, eq. (9)): "for any (w0, w) in Z^{n+1}, the following holds:
(w^T x + w0 - 1)(w^T x + w0) >= 0 for all x in {0,1}^n. Expanding this product and replacing
x_i x_j by X_{i,j}, we obtain the BH inequalities
sum_{1<=i<j<=n} 2 w_i w_j X_{i,j} + sum_{i=1}^n w_i (w_i + 2 w0 - 1) x_i + w0 (w0 - 1) >= 0."

Definition 1 (p. 5): "Given (v0, v) in R^{n+1}, we define E-CG(v0, v) as the coefficients of
(8) obtained using (v0, v). This means that E-CG(v0, v) = (α, β, γ) in R^{n+C(n,2)+1} where
α_i = ⌈v_i^2 + 2 v_i v_0⌉, β_ij = ⌈2 v_i v_j⌉, γ = ⌊v_0^2⌋."

The families (p. 5) are
`F0 = {E-CG(v0,v) : v in Z^n, v0 + 1/2 in Z}`,
`F1 = {E-CG(v0,v) : v in Z^n, 2 v_i v0 in Z for all i}`, and
`F2 = {E-CG(v0,v) : v_i^2 in Z, 2 v_i v_j in Z (i != j), 2 v_i v0 in Z}`.
The results about them are:
- Lemma 2 (p. 6): the inclusions `F0 ⊊ F1 ⊊ F2 ⊊ E-CG` are strict up to scaling.
- Lemma 3 (p. 7): "The F0 family is exactly the family of Boros–Hammer inequalities."
- Lemma 4 (p. 7): "Take (v0, v) such that E-CG(v0, v) in F2. Then, E-CG(v0, v) is implied by
  a nonnegative combination of at most two BH inequalities."

The proof of Lemma 4 (pp. 8–9) makes precise what "implied" means there. It matches the
`X` and `x` coefficients exactly and shows that the combined constant is `<= ⌊v0^2⌋`.

**Conjecture 1 (p. 9, exact wording).** "For any (v0, v) in R^{n+1}, the inequality defined by
E-CG(v0, v) is implied by a nonnegative combination of BH inequalities.
To date, every computational test we have devised suggests that this conjecture is true, but
we have not been able to find a proof."

Related statements:
- p. 4: "We conjecture that the closure of Eigen-CG is also equal to that of BH."
- p. 4: "Though there are infinitely many BH inequalities, the closure is a polytope [33]"
  ([33] = Letchford and Sørensen, "Binary positive semidefinite matrices and associated
  integer polytopes").
- p. 9: "Via exhaustive enumeration, we know that BH inequalities capture all facets of
  BQP_5; in particular, Eigen-CG inequalities describe BQP_5." The same page adds:
  "BQP_6 has 116,764 facets [23]. Among these, … 3,676 inequalities can be represented as
  Eigen-CG inequalities (furthermore, BH), while the remaining 113,088 facets are not of the
  Eigen-CG type."
- p. 14: "Since we have not yet found any Eigen-CG cuts that cannot be expressed as BH
  inequalities, we limit Eigen-CG cuts to BH inequalities in this section."
- p. 22 (Conclusions): "We conjecture that Eigen-CG inequalities have the same conic closure
  as the BH inequalities, but we have not yet found a proof."

The paper describes no specific tests for the conjecture beyond this sentence. Its
separation experiments bound `w` by `L_i = -2, U_i = 2` (p. 16, problem (18)).

## 2. Has it been resolved?

- arXiv listing: only v1 (2026-04-01). An arXiv API search for "Eigen-CG" and for
  "Boros Hammer" abstracts returns only this paper.
- Semantic Scholar API (paperId d036a041…): `citationCount: 0` (queried 2026-09-23).
- A web search found nothing beyond the paper itself.
- de Meijer–Sotirov (arXiv:2201.10224, the CG framework for ISDPs that the paper mentions)
  has no BQP, max-cut or BH content (grep of the full text).

Conclusion: as of 2026-09-23 the conjecture appears open.

## 3. Precise formulation and equivalences

Notation.
- `z = (x, X) in R^{n + C(n,2)}`. An inequality is written `a.z + c >= 0`.
- `M(z)` is the `(n+1) x (n+1)` matrix `[[1, x^T], [x, Y]]` with `Y_ii = x_i` and
  `Y_ij = X_ij`.
- `c(z) = (1, x)`.
- For `ŵ = (w0, w) in Z^{n+1}`, the BH left-hand side equals
  `g_z(ŵ) = ŵ^T M(z) ŵ - c(z)^T ŵ`.
- `P_BH(n) = {z : g_z(ŵ) >= 0 for all ŵ in Z^{n+1}}`.

**3.1 "Implied" is unambiguous.** `P_BH(n)` is a nonempty polytope defined by finitely many
BH inequalities (paper p. 4, citing [33]). By the affine Farkas lemma the following are
equivalent for an E-CG cut `f`:
- (i) `f` is valid on `P_BH(n)`;
- (ii) there is a finite `λ >= 0` with `sum λ_k (BH_k coefficients) = (α, β)` and
  `sum λ_k (BH_k constants) <= γ` (the sense used in Lemma 4);
- (iii) `f` is valid on the BH closure (any limits or infinite combinations).

Box and nonnegativity constraints add nothing because they are BH-implied:
- `X_ij >= 0` is BH with `w = e_i + e_j, w0 = 0`;
- `X_ij <= x_j` is BH with `w = e_i - e_j, w0 = 0`;
- `x_i <= 1` follows from McCormick (for `n = 1`, BH with `w = 1, w0 = -1` gives
  `2 - 2x >= 0`).

Conjecture 1 is therefore equivalent to **E-CG closure = BH closure**, because `F0 = BH`
is contained in E-CG. A counterexample is any pair `(z, (v0, v))` with `z in P_BH(n)` and
`E-CG(v0, v)` violated at `z`. Checking `z in P_BH(n)` exactly requires all BH
inequalities, not a bounded subset (Section 6.2).

**3.2 BH and switched hypermetric inequalities.** *Correction after independent review:*
the paragraph below claims more than it proves. The equality "`P_BH(n)` = switched
hypermetric polytope" is not shown, and BH inequalities are not gap inequalities in the
usual sense. Only the inclusion `BQP_n ⊆ P_BH(n)` is used later, and it holds. That
finitely many BH inequalities define `P_BH(n)` follows from Letchford and Sørensen (Math.
Program. 2012, Proposition 18 and Corollary 4). For `n = 5` the reviewer computed `BQP_5`
with qhull (368 facets, all BH), confirming `P_BH(5) = BQP_5`.

Original text: Put `y = 2x - 1 in {±1}^n`, add a root
coordinate, and let `b = (w, sum w + 2 w0 - 1) in Z^{n+1}`. Then
`(w^T x + w0)(w^T x + w0 - 1) >= 0` becomes `(b^T ŷ)^2 >= 1` with `sum b` odd. Every
`b in Z^{n+1}` with odd sum arises this way. These are the gap inequalities with
`σ(b)` odd, and they contain all switchings of the hypermetric inequalities. Consequently
`P_BH(n)` is the (switched) hypermetric polytope on `n+1` points, under the covariance map.
For `n + 1 <= 6` the cut polytope `CUT_{n+1}` is described by switched hypermetric
inequalities (Deza–Laurent), so `P_BH(n) = BQP_n` for `n <= 5`, as the paper also states on
p. 9.

**3.3 `P_BH` lies inside the SDP set.** If `z in P_BH` then `M(z)` is PSD. Proof: for integer
`ŵ` and integer `t`, `g_z(tŵ) = t^2 ŵ^T M ŵ - t c^T ŵ >= 0`. Letting `t -> ∞` gives
`ŵ^T M ŵ >= 0` for integer, hence rational, hence real `ŵ`.

**3.4 E-CG = rank-one CG cuts of `K = {z >= 0 : M(z) PSD}`.** For `ŵ = (v0, v)`:
- the eigen-cut `<ŵŵ^T, M(z)> >= 0` reads `v0^2 + sum p_i x_i + sum q_ij X_ij >= 0`, where
  `p_i = v_i^2 + 2 v_i v0` and `q_ij = 2 v_i v_j`;
- rounding the coefficients up is valid on `K` because `z >= 0` there;
- the CG step then turns `-v0^2` into `⌈-v0^2⌉ = -⌊v0^2⌋`.

Conversely, a CG cut of `K` with multiplier `S = ŵŵ^T` (plus nonnegativity multipliers) is
dominated by `E-CG(ŵ)`. General CG cuts of `K` use any PSD `S`. The key identity is

`F(z; v0, v) := E-CG value at z = q_M(ŵ) + sum_i x_i ρ(p_i) + sum_{i<j} X_ij ρ(q_ij) - frac(v0^2)`,

with `q_M(ŵ) = ŵ^T M(z) ŵ >= 0` on `P_BH` and `ρ(t) = ⌈t⌉ - t in [0,1)`. So the only source
of strength beyond `K` is the floor on the constant. A violation at `z in P_BH` needs
`q_M(ŵ) < frac(v0^2) < 1`.

## 4. Proved partial results

**(a) `n <= 5`, and support at most 5 for any `n`.** For `n <= 5`, `P_BH(n) = BQP_n`
(Section 3.2), and E-CG cuts are valid for `BQP_n` (Lemma 1). For general `n`, let
`S = supp(v)`. Every coefficient involving an index outside `S` is `⌈0⌉ = 0`. So the cut is
an inequality on the `S`-coordinates that is valid for `BQP_S`. If `|S| <= 5`, it is a
nonnegative combination of BH inequalities on `S`, which are BH inequalities on `[n]` with
`w_i = 0` off `S`. A counterexample therefore needs `n >= 6` and full support 6.

**(b) `v0^2 in Z` (in particular `v0 = 0`).** From the identity in 3.4, `F >= q_M(ŵ) >= 0` on
`P_BH ⊆ K`.

**(c) Rational direction (a generalization of Lemma 4).** Let `v = ρσ` with `σ in Z^n` and
`ρ > 0`, write `v0 = ρτ`, and let `h = σ^T x`. Take `k in Z` with `|τ - k| <= 1/2`. The
combination `λ BH(k, σ) + μ BH(k+1, σ)` with `λ + μ = ρ^2` and `μ - λ = 2ρ^2(τ - k)` has
`λ, μ >= 0` and equals, as a polynomial in `h` before linearization,
`ρ^2[(h+τ)^2 - (τ-k)^2]`. Its linearization is exactly the linearization of `(v0 + v^T x)^2`
minus `(v0 - kρ)^2`.

Hence on `P_BH`, `lin((v0 + v^T x)^2) >= (v0 - kρ)^2`. Therefore

`E-CG(v0,v)(z) = lin((v0+v^Tx)^2)(z) + [rounding terms >= 0] - frac(v0^2) >= (v0 - kρ)^2 - frac(v0^2)`.

**Proposition.** If `v` is proportional to an integer vector and `dist(v0, ρZ)^2 >= frac(v0^2)`,
then `E-CG(v0, v)` is implied by two BH inequalities plus the BH inequalities `x_i >= 0`,
`X_ij >= 0` that absorb the rounding.
The proof above is complete; I checked it symbolically by hand.

The proposition contains Lemma 4. In the `F2` case, `ρ^2 = p^2 in Z` and `2 v0 ρ in Z`, so
`v0^2 - (v0 - kρ)^2 = k(2 v0 ρ) - k^2 ρ^2` is an integer. Hence `(v0-kρ)^2 ≡ v0^2 (mod 1)`,
and so `(v0-kρ)^2 >= frac(v0^2)`.

It also covers the "exact-part" family `F3` (no rounding in `x` and `X`, i.e.
`2ρ^2σ_iσ_j in Z` and `ρ^2(σ_i^2 + 2τσ_i) in Z`) whenever `f(h) := ρ^2(h+τ)^2 - frac(ρ^2τ^2) >= 0`
at the integer `h = -k`. Integrality holds only on subset sums of `σ`, so `f(-k) < 0` can
happen when `-k` is not a subset sum. An example is `σ = (-4,-4,-3)`, `a = ρ^2 = 1/4`,
`b = 2aτ = -5/4`, which gives `f(h) = (h-1)(h-4)/4 < 0` at `h = 2, 3`. These are exactly the
cases this certificate does not cover; Section 6.1 tests them.

**(d) Constant `v` (all `v_i` equal).** The cut is `S_n`-invariant, so its minimum over the
convex, `S_n`-invariant `P_BH` is attained at a symmetric point `(s·1, t·1)`. At such points:
- BH with `w = 1` and all integers `w0` give `E[(k+w0)(k+w0-1)] >= 0` for the pseudo-moments
  `E[k] = ns` and `E[k(k-1)] = n(n-1)t`;
- McCormick gives `E[k^2] <= n E[k]`.

These describe `conv{(k, k(k-1)) : k = 0..n}`, the symmetric slice of `BQP_n`. The cut is
valid there, so it is implied.

Numerically, the same slice equality appears to hold for block-constant `v` with blocks
`(3,3)`, `(4,2)`, `(2,2,2)`, `(3,2,1)`, `(5,1)` at `n = 6`. Over 300 random invariant
objectives per partition, the minimum over `P_BH(6)` equals the minimum over `BQP_6` to
`1e-14` (`code/block_slices.py`). This is numerical evidence only, not a proof.

**(e) Trivial cases.** If `v0 v_i >= 0` for all `i`, every coefficient is `>= 0` and
`⌊v0^2⌋ >= 0`.

## 5. Negative structural result: general-rank CG cuts of `K` are not BH-implied

Claim (exact). The non-BH facets (13), (14), (15) of `BQP_6` quoted in the paper (pp. 9–11)
are Chvátal–Gomory cuts of `K = {z >= 0 : M(z) PSD}`.

Certificate. `code/cg_cert.py` finds rational `S` and `N` with `S` positive definite (checked
by an exact `LDL^T`) and `N >= 0` componentwise, such that
`a.z + S_00 = <S, M(z)> + N.z` holds identically, with `S_00 < c + 1`. Then
`a.z >= -S_00` on `K`, and CG rounding gives `a.z >= ⌈-S_00⌉ = -c`. The certificate values
are:
- (13): `S_00 = 508527/200000 < 3`;
- (14): `S_00 = 5687159/1000000 < 6`;
- (15): `S_00 = 320117/200000 < 2`.

The matrices are in `code/cg_certificates.json`. The SDP values of the linear parts over `K`
are -2.4607, -5.5042 and -1.4790.

Why these cuts are not BH-implied, exactly: the rational points `z13`, `z14`, `z15` (all
coordinates in (1/6)Z, listed in `code/vertices6.py`) are proved to lie in `P_BH(6)` by exact
lattice enumeration (Section 6.2). Each violates its facet by exactly `1/6`. In addition, a
facet of `BQP_6` that is not BH cannot be a nonnegative combination of BH inequalities.

Consequences:
- The CG closure of `K`, which is the de Meijer–Sotirov-type closure with arbitrary PSD
  aggregation, is strictly smaller than `P_BH(6)`.
- Conjecture 1 is only plausible because of the rank-one restriction.
- "Aggregated" Eigen-CG cuts that round several eigen-cuts jointly are genuinely stronger
  than BH.

The paper proves that (13)–(15) are not rank-one representable (Props. 3–5), so this is
consistent.

## 6. Computational search for a counterexample

Machinery (`code/bh.py`, `code/verify.py`):
- `PBH(n)` minimizes a linear function over `P_BH(n)` by cutting planes. The initial pool is
  all BH with `|w_i| <= 1` (2,181 inequalities for `n = 6`).
- Separation is a Gurobi MIQP over `|w_i| <= 6`.
- With `exact=True` (all runs in 6.3–6.5), or after a would-be hit (6.2), a
  *complete* separation `complete_separation` follows:
  - if `M(z)` is not PSD, the MIQP is rerun with `|w_i| <= 12, 25, 50, 100`;
  - otherwise the LP vertex is rationalized and `exact_bh_separation_general` decides
    `z in P_BH` exactly.
- `exact_bh_separation_general` works as follows:
  1. It computes the rational kernel of `M`.
  2. It reduces modulo the saturated integer kernel lattice, using an integer
     column-echelon form with a unimodular transform.
  3. It enumerates all integer points in the ellipsoid
     `{y : (y-m)^T M' (y-m) <= m^T M' m}` (Fincke–Pohst on an exact `LDL^T`).

  A point `z` is in `P_BH` iff no enumerated `ŵ` has `g_z(ŵ) < 0`.

Caveat on "implied" results: the LP minima are floating-point (Gurobi tolerances `1e-9`).
They certify implication by an explicit finite set of genuine BH inequalities up to that
tolerance. I did not extract rational dual certificates for them.

### 6.1 Exact-part family `F3` (`code/f3_enum.py`, `code/t6.py`)

Enumeration: `σ in {±1,…,±4}^6` up to permutation with `gcd = 1`, `a = m/(2g)` for
`m <= 12` (where `g = gcd` of the pairwise products `σ_iσ_j`), and `b` in the forced coset
mod 1 (a Bézout argument). `τ` is kept in the relevant range, and only cases with
`f(h) < 0` at some integer `h` are retained, since the others are covered by 4(c).

Result: **6,036 cuts, all implied**. The minimum over `P_BH(6)` is `>= -2.3e-13`.

### 6.2 Perturbed limits of exact points (`code/perturb_milp.py`, `code/run_perturb.py`)

The function `v -> F(z; v)` is piecewise constant. Ceilings are lower semicontinuous, but
the floor is not. The strongest cuts near an exact point `v*` (all coefficients integral,
`v0*^2` integral) therefore arise from `v* + εδ` in two ways: `⌊v0^2⌋` drops by 1
(`v0*δ0 < 0`), while each integral coefficient stays or rises by 1 according to the sign of
its first-order change `J_k δ`. The resulting cut is `f*(z) - 1 + sum_{k in S+} z_k >= 0`.

For each exact base point, a MILP minimizes this over `z` in the BH pool, over `δ`
(margin `1e-3`), and over the sign pattern `S+`, with BH cuts added lazily. A necessary
filter keeps only bases with `ρ^2(τ - round τ)^2 < 1`, by 4(c).

Results:
- `n = 6`, `|σ_i| <= 2`, `m <= 24`: 10,680 bases (first pass with `|w_i| <= 6` separation only;
  `code/perturb_n6_R2_a24_firstpass.log`, `code/perturb_n6_R2_a24.json`). There were two "hits", both with
  `σ = (-2,-1,-1,1,1,1)`, `τ = 1`, and `a = 11` or `a = 8`. The objective was -0.625 or -0.25
  at the same point `z = (3,5,3,3,3,3 | 1,0,2,2,2,2,2,2,2,1,1,1,1,1,1)/8`.
  - Exact check (`code/check_hits.py`, `code/t9.py`, `code/t10.py`): `M(z)` has a negative
    eigenvalue (`det M = -3/65536` exactly), so `z ∉ P_BH`. *(Corrected after review: it
    violates the BH `(0; 2,1,1,-1,-1,-1)` by 1/2; `(-1, 10, 5, 4, -6, -6, -6)` with value -6.75
    is the most violated BH found, not the smallest.)*
  - With complete separation, both bases give minimum 0 (implied). They were false
    positives caused by a failed `|w_i| <= 6` separation run (Gurobi reported optimal value
    0; the true minimum is -2.5), per the independent review.
  - Lesson (corrected): separation results should be checked exactly; the earlier
    conclusion that bounded separation as in the paper's (18) is insufficient is withdrawn.
- `n = 6`, `|σ_i| <= 3`, `m <= 12`, complete separation: 39,636 bases.
  **0 hits, 0 undetermined**. The lowest MILP objective is `-6.4e-9`, which is numerical
  zero (`code/perturb_n6_R3_a12.log`, `code/perturb_n6_R3_a12.json`).
- `n = 7`, `|σ_i| <= 2`, `m <= 12`, complete separation: 8,862 bases.
  **0 hits, 0 undetermined**. The lowest objective is `-6.5e-8`, which is within the
  MILP tolerances (`code/perturb_n7_R2_a12.log`, `code/perturb_n7_R2_a12.json`).

### 6.3 Random structured E-CG cuts (`code/random_ecg.py`)

Sampling:
- With probability 0.7, `ŵ = ρ(τ, σ)` plus Gaussian noise of scale in
  `{1e-4, 1e-3, 1e-2, 0.05, 0.2}`, with `σ in {±1..±3}^n`, `ρ^2 in [0.2, 12]`, and `τ` in the
  subset-sum range. Otherwise a Gaussian `ŵ`.
- `ŵ` is made rational (denominator 1e9), and E-CG is computed exactly.
- Discarded: duplicates, supports below `n`, all-nonnegative cuts, and integral `v0^2`.

Results with `PBH(exact=True)`:
- `n = 6`: **100,000** distinct cuts. Minimum over `P_BH(6)` is `-1.4e-13`: no violation,
  no undetermined cases (`code/random_ecg_n6_s1.log`).
- `n = 7`: **30,000** distinct cuts. Minimum is `-2.7e-13`: no violation
  (`code/random_ecg_n7_s2.log`).

### 6.4 The fractional vertices of `P_BH(6)` are of E7 type (`code/vertex_survey.py`, `code/vertices6.py`)

Minimizing the paper's facets (13), (14), (15) over `P_BH(6)` gives points `z13`, `z14`,
`z15` with coordinates in (1/6)Z. Exactly:
- each is in `P_BH(6)`;
- each violates its facet by 1/6;
- `rank M = 7` and `det M = 1/139968 = 2/6^7`;
- each has 56 integer points on the empty sphere (the tight BH).

`det = 2/6^7` is the determinant of the E7 root lattice with norms scaled by 1/6. The 56
tight lattice points are the vertices of the Gosset polytope `3_21`, the Delaunay polytope of
E7. So `M(z)` is the Gram matrix of a basis of `E7/√6`, and `z` is the E7 hypermetric.

Survey: 400 random permuted and switched copies of (13)–(15), with 1e-3 perturbations,
minimized over `P_BH(6)`, gave **397 distinct fractional vertices**. All are exactly
certified in `P_BH(6)`, all have `det M = 1/139968` with 56 tight points (the
reviewer found every vertex in the stored JSON has denominator 6; the earlier "391 with
denominator 6, 6 with denominator 3" is wrong), and all violate the corresponding facet by exactly 1/6.

I did not prove that these are all the non-integral vertices of `P_BH(6)`. The survey
suggests that the `n = 6` case reduces to E-CG separation at E7-type points.

### 6.5 Direct E-CG separation at the E7 points

The E-CG separation at a fixed `z` minimizes the piecewise-constant `F(z; ·)` over `ŵ` in the
ellipsoid `q_M < 1`, with `v0 >= 0`. Three methods were tried:
- **Gurobi MIQCP** (`code/ecgsep.py`, `code/ecg_feas.py`): did not close. The bound stayed
  near -1.3 after 120 s. A feasibility version with the valid strengthenings
  `q_M <= 1 - viol` and per-coefficient rounding caps hit its 1,800 s time limit at `z13`.
  Inconclusive.
- **Interval branch-and-bound** (`code/ecg_bnb.py`): exact ranges of each quadratic on boxes,
  and bounds `max(LB1, LB3)` from the identity in 3.4. It is exact in principle but too
  slow: 5×10^7 boxes per point without resolution. The ellipsoid is thin
  (`λ_min(M) ≈ 0.013`), and there are 28 quadric families of integer level sets in 7
  dimensions. Inconclusive.
- **Exact one-dimensional minimization along lines** (`code/linesearch.py`). All integer
  crossings of the 28 quadratics are enumerated inside the ellipsoid, and `F` is evaluated at
  every crossing (boundary values) and between crossings. This is used with random restarts
  and coordinate or random directions.
  - At the 3 × 64 switchings of `z13, z14, z15` (20 restarts × 40 line searches): the
    minimum `F` found is `0.0` (up to 1e-15), attained by tight cuts of support at most 5.
    No negative value.
  - At all 397 surveyed vertices (30 restarts × 40 line searches each,
    `code/run_linesearch.py`, results in `code/linesearch_results.json`): the minimum `F`
    found is `0` (up to 4e-15) at every point. No negative value.

## 7. Proof attempts that failed, and why

1. **Via the SDP/CG closure.** Showing that every CG cut of `K` is BH-implied would suffice.
   This is false (Section 5), so any proof must exploit rank one.
2. **Rounding to integer directions.** Lemma 4 and 4(c) use two BH in the single direction
   `σ`. When `dist(v0, ρZ)^2 < frac(v0^2)` this one-direction certificate provably fails:
   the combination is a quadratic in `h = σ^T x` that is `>= 0` at all integers `h`, while
   the E-CG polynomial is negative at the non-subset-sum integer `h = -k`. The computations in
   6.1 and 6.2 show that such cuts are nevertheless implied, through BH in other directions
   and the rounding slack. I found no general pattern for these certificates.
3. **Lattice (Delaunay) picture.** `z in P_BH` iff the Gram vectors `u_0..u_n` of `M(z)` generate
   a module `L` such that the open ball with diameter `[0, u_0]` contains no point of `L`
   (the empty-sphere condition). The E-CG value is
   `|v0 u_0 + sum v_i u_i|^2 + (weighted rounding) - frac(v0^2)`. A proof would need to show
   that a real point `y` with `|y|^2 < frac(v0^2)` forces enough rounding loss. I could not
   turn this into an argument. The integer data `(α, β, γ)` interact with the lattice only
   through the specific coordinates `v`.
4. **Switching symmetry.** `P_BH` and `BQP_n` are invariant under switching `x_i -> 1-x_i`,
   but the E-CG family is not. The ceilings are taken with respect to `x, X >= 0`, not the
   switched nonnegativity. So one cannot reduce to `v0 >= 0, v >= 0` (the trivial case).
   After switching the negative set `N`, all quadratic coefficients become nonnegative, which
   is the hard (max-cut-like) sign pattern.

## 8. What would settle `n = 6`

Suppose the fractional vertices of `P_BH(6)` are exactly the switchings and permutations of
the E7 point, as the survey suggests; this is plausibly derivable from the known structure of
`HYP_7` (Deza–Dutour–Grishukhin). Then Conjecture 1 for `n = 6` is equivalent to a finite
list of fixed-point E-CG separation problems: at most 64 switchings modulo `S_6`, since E-CG
is `S_6`-invariant.

Each problem is a 7-dimensional piecewise-constant minimization. Exact resolution needs
either a much better branch-and-bound (e.g. branching in lattice coordinates adapted to the
thin direction, with bounds that couple `q_M` and the roundings) or an algebraic argument
specific to E7.

## 9. Files

The table covers `code/`.

| file | purpose |
|---|---|
| `paper_2604.00932v1.txt` | pdftotext of the paper |
| `bh.py` | BH/E-CG coefficients, BH pool, MIQP separation, `PBH` LP with complete separation |
| `verify.py` | exact rational tools: `exact_bh_separation_general` (decides `z in P_BH`), exact E-CG, binary validity |
| `facets.py` | the paper's facets (13)–(15) |
| `f3_enum.py`, `t6.py` | exact-part family enumeration and LP test (6.1) |
| `perturb_milp.py`, `run_perturb.py` | perturbation MILP search (6.2); logs `perturb_*.log`, results `perturb_*.json` |
| `check_hits.py`, `t9.py`, `t10.py` | exact refutation of the two false positives (6.2) |
| `random_ecg.py` | random structured E-CG test (6.3); logs `random_ecg_*.log` |
| `vertex_survey.py`, `vertices6.py`, `pbh6_fractional_vertices.json` | E7-type vertices of `P_BH(6)` (6.4) |
| `linesearch.py`, `t12.py`, `run_linesearch.py` | line-search E-CG separation at vertices (6.5) |
| `ecgsep.py`, `ecg_feas.py`, `ecg_bnb.py`, `sample_search.py`, `t2.py`, `t4.py`, `t7.py`, `t11.py` | inconclusive exact/MIQCP separation attempts and uniform sampling in the ellipsoid (6.5) |
| `t1.py`, `t3.py`, `t5.py`, `t8.py` | exploratory: facet minimization over `P_BH(6)`, moment-matrix spectra, `F3` negativity counts, the serial precursor of `run_perturb.py` |
| `cg_sdp.py`, `cg_cert.py`, `cg_certificates.json` | Section 5: general-rank CG cuts of `K` (minlp-notes env) |
| `block_slices.py` | numerical block-symmetric slice test (4d) |

Commands actually run (targeted; no project-wide checks): each script above was run directly
with the stated interpreter. The outputs quoted here come from those runs (logs in `code/`).
