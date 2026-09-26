# Certified bounds from classical structure theorems: elec and hadamard (2026-09-23)

Status: independently reviewed ([review](review-structural-bounds.txt)); all eight bounds confirmed with
separate code; three documentation errors corrected (gap formula, elec25 rounding, a missing citation).

Scope: the eight open MINLPLib instances elec25/50/100/200 and hadamard_6..9, following the probes
in `scouting/brainstorm2-structural.md` (D1, D2). Every bound below comes with either an exact
certificate checked in rational/integer arithmetic, or a cited theorem whose hypotheses were checked
against the parsed model. Code: `benchmark-observations/code/structural/`; certificates:
`code/structural/certs/*.json`.

## Summary

| instance | listed primal | listed dual | new certified bound | new gap | status |
|---|---|---|---|---|---|
| elec25 (min) | 243.8127603 | 90.22758027 | dual >= 243.638659 | 0.0715% | open, gap 170% -> 0.07% |
| elec50 (min) | 1055.182315 | 359.0296983 | dual >= 1054.849188 | 0.0316% | open, gap 194% -> 0.03% |
| elec100 (min) | 4448.350634 | 1429.500306 | dual >= 4447.479965 | 0.0196% | open, gap 211% -> 0.02% |
| elec200 (min) | 18438.87685 | 5744.71434 | dual >= 18436.477818 | 0.0130% | open, gap 221% -> 0.013% |
| hadamard_6 (max) | 9 | 25 | dual <= 9; primal 9 | 0 | **closed** (Ehlich + integrality; also exhaustive enumeration) |
| hadamard_7 (max) | 32 | 721 | dual <= 32; primal 32 | 0 | **closed** (Hadamard bound) |
| hadamard_8 (max) | 56 | 14267.56437 | dual <= 65; primal 56 | 16.1% | open here (the literature value 56 is not re-proved) |
| hadamard_9 (max) | 144 | none | dual <= 144; primal 144 | 0 | **closed** (Ehlich–Wojtas bound) |

Gaps use the convention of `open.csv`: |primal − dual| / min(|primal|, |dual|) (corrected after
independent review; an earlier version stated (primal − dual)/|dual|). Bounds are exact rationals; the
decimals shown are rounded down (elec) or exact integers (hadamard).

**Listed values.** The "listed" columns are the headline values in the current MINLPLib instance
table (https://www.minlplib.org/instances.html, fetched 2026-09-23). They match `open.csv`. Each
instance page also lists every solver's reported dual bound, with the three best in bold. In all
eight cases the headline dual equals the **third-best** reported value. This is inferred from the
pages; the MINLPLib documentation does not state the rule. Some single-solver values on the pages
are tighter than the headline values: for elec25 and elec50, LINDO reports a dual equal to the
primal; for elec100, BARON reports 4448.350577; for hadamard_6, ANTIGONE reports 9.75, which
rounds down to 9 by integrality. None of these values contradicts the certified bounds here.
MINLPLib does not adopt them as headline values.

## 1. elec: Thomson problem

### 1.1 Model (checked exactly)

`code/structural/elec_model.py` parses the OSiL file with the independent parser `code/osil_eval.py`.
It asserts the following structure for elec25/50/100/200 (N = 25/50/100/200):

- `3N` continuous variables, all free. Point `i` is `(x[i], x[i+N], x[i+2N])`.
- `N` rows `x[i]^2 + x[i+N]^2 + x[i+2N]^2 = 1`, with lb = ub = 1, no linear or other terms, and
  constant 0. The points lie exactly on the unit sphere S^2 in R^3.
- The objective is `min sum_{a<b} 1/sqrt(sum_c (x[a+cN] - x[b+cN])^2)`, with no linear, quadratic, or
  constant part. Each of the N(N−1)/2 unordered pairs occurs exactly once, and the three squared
  differences are between matching coordinates of the same two points.

So the model is the Thomson (Coulomb energy) problem on S^2. The objective is defined only for
pairwise distinct points.

### 1.2 Bound and proof (Delsarte–Yudin)

Let `t_ij = <x_i, x_j>`, so `|x_i − x_j| = sqrt(2 − 2 t_ij)` and `f(t) = (2−2t)^(−1/2)`. Let
`P_k` be the Legendre polynomials (the Gegenbauer polynomials for S^2, normalized so that `P_k(1) = 1`).

**Claim.** If `h(t) = sum_{k=0..K} h_k P_k(t)` with `h_k >= 0` for `k >= 1` and `h(t) <= f(t)`
on `[−1, 1)`, then every feasible point satisfies

    E = sum_{i<j} f(t_ij) >= (N^2 h_0 − N h(1)) / 2,   where h(1) = sum_k h_k.

**Proof.**

1. By the addition theorem for spherical harmonics (Schoenberg 1942),
   `P_k(<x,y>) = (4π/(2k+1)) sum_m Y_km(x) conj(Y_km(y))`. Therefore
   `sum_{i,j} P_k(t_ij) = (4π/(2k+1)) sum_m |sum_i Y_km(x_i)|^2 >= 0`, and the sum equals `N^2` for
   `k = 0`.
2. Because `h_k >= 0` for `k >= 1`, step 1 gives `sum_{i,j} h(t_ij) >= N^2 h_0`. Here the sum
   runs over all ordered pairs, including `i = j`.
3. The diagonal terms `i = j` have `t_ii = 1` and contribute `N h(1)`. Each off-diagonal pair has
   `t_ij < 1`, so `h(t_ij) <= f(t_ij)`, and the off-diagonal sum is at most `2E`. Hence
   `N^2 h_0 <= N h(1) + 2E`.

**Exact check of `h <= f`.** Substitute `s = sqrt(2 − 2t)`, which maps `t ∈ [−1, 1)` to
`s ∈ (0, 2]`, with `t = 1 − s^2/2`. Then `h(t) <= f(t)` holds if and only if

    g(s) := 1 − s · h(1 − s^2/2) >= 0.

`g` is a polynomial of degree `2K+1` with rational coefficients. `elec_verify.py` builds `g`
exactly in Python `Fraction` arithmetic, using the exact Legendre recurrence and exact composition.
It then proves `g > 0` on the closed interval `[0, 2]` twice, with two independent exact subdivision
methods:

- (i) all Bernstein coefficients are positive on dyadic subintervals, using de Casteljau splitting;
- (ii) on dyadic cells `[c−r, c+r]`, an exact Taylor expansion at `c` satisfies
  `a_0 − sum_{j>=1} |a_j| r^j > 0`.

The verifier also checks `h_k >= 0` for `k >= 1` and recomputes the stated bound exactly from `h`.
No floating-point arithmetic enters the verification.

**How the certificates were built** (`elec_yudin.py`). Gurobi solves the LP
`max (N^2 h_0 − N sum h_k)/2` over `K = 60`, subject to `h(1 − s^2/2) <= 1/s` on 20,000 grid
points in `s ∈ [0.002, 2]`. The solution `h` is rounded to exact decimals, negative `h_k` values
with `k >= 1` are clipped to 0, and `h_0` is lowered by a small rational `δ`. Lowering `h_0` by `δ`
adds `δ s` to `g`; the resulting cost to the bound is `N(N−1)δ/2`. The values of `δ` are 2.5e−9,
5.9e−9, 1.6e−8 and 4.3e−8. The certified bounds lie within 1e−6 (elec25), 8e−6 (elec50),
8e−5 (elec100) and 9e−4 (elec200) of the LP values. The limiting factor is the Yudin LP itself,
not the certification: with K = 80, the elec200 LP rises by only 0.0002 (an
unarchived observation; its output was not saved).

**Checks of the checker.**

- Negative test: removing twice the `δ` shift, or adding 1e−6 to `h_5`, makes both positivity
  proofs fail.
- Sanity test (unarchived run; its output was not saved): a BFGS local optimum for N = 25
  (243.8127603) lies above the certified bound (243.6387).
- Rejected method: the sympy Sturm-sequence root count on the degree-121 polynomial did not finish in
  about 10 minutes (gmpy2 is not installed), so it was replaced by methods (i) and (ii).

### 1.3 Results

| instance | K | nonzero `h_k` (k>=1) | LP value (float) | certified bound (exact rational) | listed primal | new gap |
|---|---|---|---|---|---|---|
| elec25 | 60 | 19 | 243.638661 | 9745546397461602351591/40000000000000000000 ≈ 243.6386599 (rounded down: 243.638659) | 243.8127603 | 0.0715% |
| elec50 | 60 | 30 | 1054.849196 | ≈ 1054.849188 | 1055.182315 | 0.0316% |
| elec100 | 60 | 47 | 4447.480044 | ≈ 4447.479965 | 4448.350634 | 0.0196% |
| elec200 | 60 | 54 | 18436.478674 | 18436477818333876246068897/10^21 ≈ 18436.477818 | 18438.87685 | 0.0130% |

The exact rational values of all four bounds are stored in the certificates (key `bound`).

**Caveats.**

- The bound holds for points exactly on the sphere, as the model states. MINLPLib accepts primal
  points with infeasibility up to 1e−8; the bound is not claimed for such points.
- The listed primal feasibility was not checked, because it does not affect the dual bound.
- The best known (putative) Thomson energy for N = 200 is 18438.842717530 (Wikipedia, "Thomson
  problem"). This is 0.034 below the MINLPLib primal value. For N = 25, 50 and 100 the Wikipedia
  values agree with MINLPLib's primal values.
- The Yudin LP bound is not expected to close these gaps. Three-point SDP bounds would be the next
  step.

## 2. hadamard_6..9: maximum determinant of a 0/1 matrix

### 2.1 Model identification (exact, all four sizes)

`code/structural/had_model.py` parses each OSiL file with `osil_eval.py` and asserts the following
structure:

- Variables `b1..b_{n^2}` are binary in [0,1]; `objvar` is continuous and free.
- The objective is `max objvar`.
- The single row `e1` is `poly(b) − objvar >= 0`, with constant 0 and no other terms.
- `poly` is a sum of products of variables with coefficients ±1, and no variable repeats within a
  product.

The script builds the coefficient dictionary of `poly` (monomial = set of variable indices) and
checks that it is **identical** to the Leibniz expansion of `det(B)`, where `B[i,j] = b_{i n + j + 1}`
(row-major). The polynomials have 720, 5040, 40320 and 362880 terms for n = 6, 7, 8, 9. Equal
coefficient dictionaries prove that the two sides are the same real polynomial. This is an exact
symbolic identity, not a random test, and no `b^2 = b` reduction is needed. The run takes 11 s and
uses 2 GB, including the 74 MB hadamard_9 file.

Because `objvar` is free and bounded only by `objvar <= det(B)`, the optimal value is
`D01(n) = max{det B : B ∈ {0,1}^{n×n}}`. This value is an integer, since `det` of an integer matrix
is an integer.

### 2.2 Dual bounds

**Reduction to ±1 matrices.** Given a 0/1 matrix `B` of order n, let `A` be the ±1 matrix of
order `m = n+1` with first row and column all +1 and lower-right block `J − 2B`. Subtracting the
first row from the others gives `det A = det(−2B) = (−2)^n det B`. So
`D01(n) <= Dpm(m)/2^n`, where `Dpm(m)` is the maximal determinant of a ±1 matrix of order m. The
reverse inequality also holds (normalize the first row and column), so the two are equal. Only the
`<=` direction is used here.

The script `had_bounds.py` applies the classical bounds on `Dpm(m)` below. They are squared so that
all arithmetic is exact, and then combined with integrality:
`D01(n) <= isqrt(floor(Dpm_bound^2 / 4^n))`. The statements were checked against Wikipedia
("Hadamard's maximal determinant problem") and against Browne, Egan, Hegarty and Ó Catháin,
*A survey of the Hadamard maximal determinant problem*, arXiv:2104.06756 (Corollary 10, Theorem 17 (Ehlich–Wojtas, used for hadamard_9) and
Theorem 25).

- **Hadamard (1893), all m:** `Dpm(m)^2 <= m^m`. This follows from Hadamard's inequality applied to
  the Gram matrix `AA^T`, whose diagonal entries are all m.
- **Barba (1933), m odd:** `Dpm(m)^2 <= (2m−1)(m−1)^(m−1)`.
- **Ehlich (1964) / Wojtas (1964), m ≡ 2 (mod 4):** `Dpm(m) <= (2m−2)(m−2)^((m−2)/2)`.
- **Ehlich (1964, Math. Z. 84), m ≡ 3 (mod 4):**
  `Dpm(m)^2 <= (m−3)^(m−s) (m−3+4r)^u (m+1+4r)^v [1 − ur/(m−3+4r) − v(r+1)/(m+1+4r)]`,
  with `s = 5` for `m = 7`, `r = floor(m/s)`, `v = m − rs` and `u = s − v`.

| instance | m | applicable bounds on D01(n) (real → integer) | certified dual | theorem used |
|---|---|---|---|---|
| hadamard_6 | 7 (≡ 3 mod 4) | Hadamard 14.18→14, Barba 12.17→12, Ehlich 9.165→9 | 9 | Ehlich (`Dpm^2 <= 344064`) + integrality |
| hadamard_7 | 8 | Hadamard 32→32 | 32 | Hadamard |
| hadamard_8 | 9 (odd, ≡ 1 mod 4) | Hadamard 76.89→76, Barba 65.97→65 | 65 | Barba + integrality |
| hadamard_9 | 10 (≡ 2 mod 4) | Hadamard 195.3→195, Ehlich–Wojtas 144→144 | 144 | Ehlich–Wojtas |

**Independent proof for hadamard_6.** The Ehlich bound is the least elementary theorem used here, so
`D01(6) = 9` was also verified by exhaustive enumeration, independent of Ehlich (`exhaustive6` in
`had_bounds.py`). The enumeration uses exact int64 arithmetic and 5×5 Leibniz minors, and takes
about 40 s. The reduction is as follows:

1. A permutation of the columns (which does not change `|det|`) makes one row `1^w 0^(6−w)`.
2. The next four rows range over all 4-subsets of the 63 nonzero 0/1 vectors. Row order changes only
   the sign of the determinant, and repeated or zero rows give determinant 0.
3. The last row is optimized exactly. The determinant is linear in that row, so the maximum of
   `|det|` is `max(sum of positive cofactors, −sum of negative cofactors)`.

The result is `max |det| = 9`.

### 2.3 Primal certificates

A local search found 0/1 matrices with determinants 9, 32, 56 and 144. For each matrix:

- `det` was computed exactly with sympy's Bareiss algorithm;
- the OSiL model was evaluated in exact `Fraction` arithmetic at `(B, objvar = det B)`;
- all variable bounds, integrality and row `e1` were checked (activity exactly 0);
- the objective equals 9, 32, 56 and 144 exactly.

The matrices are stored in `certs/hadamard_n.json` (key `primal_matrix_rowmajor`).

### 2.4 Status

- **hadamard_6, hadamard_7 and hadamard_9 are closed**: the certified dual equals the certified
  primal. hadamard_7 uses only Hadamard's bound. hadamard_9 uses the Ehlich–Wojtas theorem, cited
  and not re-proved. hadamard_6 follows from Ehlich's theorem and, independently, from the
  exhaustive enumeration.
- **hadamard_8 is not closed here.** The certified dual is 65 against a primal of 56, a gap of
  16.1%, down from 254x. The literature value `D01(8) = 56` (±1 order 9: 14336 = 7·2^11) is listed in
  OEIS A003432, which cites Ehlich and Zeller, *Binäre Matrizen*, ZAMM 42 (1962). I did not check the
  original paper, and no closed-form bound gives 56. Closing hadamard_8 with a certificate would need
  a Gram-matrix exclusion argument or a computation.

## 3. Files and verification commands

Python: `~/miniconda3/envs/exact-quadratic-hull/bin/python`. Run from
`benchmark-observations/code/structural/`.

| file | role |
|---|---|
| `elec_model.py` | exact structural check of elec OSiL (sphere rows, pair-energy objective) |
| `elec_yudin.py` | builds `certs/elecN.json` (Gurobi LP, rounding, δ shift, exact positivity) |
| `elec_verify.py` | independent exact verifier (Fractions; Bernstein and Taylor subdivision) |
| `had_model.py` | exact identity poly == det(B) for hadamard_6..9 |
| `had_bounds.py` | exact bounds, primal search, exhaustive n=6 check, writes `certs/hadamard_n.json` |
| `had_verify.py` | deterministic re-verification of the hadamard certificates |
| `certs/elec{25,50,100,200}.json` | `h` (exact decimals), exact `bound`, `δ` |
| `certs/hadamard_{6,7,8,9}.json` | bounds (exact squared values), certified dual, primal matrix, exact det/objective |

Commands run for this report (targeted checks only; no CI checks were run or inspected):

    python elec_model.py                    # 4x "structure verified", 0.5 s
    python elec_yudin.py 60                 # builds certificates, 34 s
    python elec_verify.py certs/elec25.json certs/elec50.json certs/elec100.json certs/elec200.json
                                            # "ALL CERTIFIED", 49 s
    python had_model.py 6 7 8 9             # 4x "polynomial == det(B) VERIFIED", 11 s
    python had_bounds.py                    # writes certificates, 58 s
    python had_verify.py                    # "ALL VERIFIED" incl. exhaustive n=6, 61 s

## Sources

- MINLPLib instance pages https://www.minlplib.org/<name>.html and table https://www.minlplib.org/instances.html (fetched 2026-09-23).
- Hadamard's maximal determinant problem, Wikipedia (raw wikitext fetched 2026-09-23).
- P. Browne, R. Egan, F. Hegarty, P. Ó Catháin, A survey of the Hadamard maximal determinant problem, arXiv:2104.06756 (v4).
- G. Barba, Giorn. Mat. Battaglini 71 (1933) 70–86; H. Ehlich, Math. Z. 83 (1964) 123–132 and Math. Z. 84 (1964) 438–447; M. Wojtas, Colloq. Math. 12 (1964) 73–83.
- OEIS A003432 (values 9, 32, 56, 144; reference Ehlich–Zeller 1962).
- Thomson problem, Wikipedia (best known energies for N = 25, 50, 100, 200).
- V. A. Yudin, Minimum potential energy of a point system of charges, Discret. Mat. 4 (1992); I. J. Schoenberg, Positive definite functions on spheres, Duke Math. J. 9 (1942).
