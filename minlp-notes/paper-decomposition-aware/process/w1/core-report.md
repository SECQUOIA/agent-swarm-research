# Core cluster report: corrected grids, filtering, state bound, schedule, bit complexity

Scope: `research-20261002-decomposition/document/main.tex`, Sections 2–4
(model, corrected grid, tree DP, filtering, contraction, localization, state
bound, capped schedule, Theorem `thm:approx`), compared with the companion
notes and with `solver/certified_grid.py` and `solver/verify_certificate.py`.
Outputs: `core-proofs.tex` (self-contained statements and proofs) and
`checks/` (exact-arithmetic checks; see `checks/core_README.md`).

## Verdict

**Sound with fixes.** I re-derived every step of Sections 2–4. No claim
fails. The interpolation inequality, conditional filtering, filtering
history, contraction constants (`1/15`, `B0`, `7/8`, `22/15`, radius 5), the
integer step rule and its node count, the capped unknown-growth schedule, the
common-denominator argument and the `log^p n` absorption are all correct. The
issues are minor: notation clashes, loose and over-complicated constants, a
missing precise FPT statement, certificate content larger than needed, and
two differences between the paper's algorithm and the implementation. The
cluster can also be strengthened in three ways: a scale-invariant
conditioning parameter, a minimal certificate, and lower bounds showing that
both parameters are necessary.

## Issues and fixes

| # | Severity | Location | Issue | Fix (verified) |
|---|---|---|---|---|
| 1 | minor | Sec. 3–4, Thm `approx` proof | `D` denotes both the correction sum `D(y)` and the common denominator. `b` denotes the grid bound, upper endpoints `b_i`, and an adjacent node `b'`. | Use shared notation: `β` for the bound, `[l_i,u_i]` for the box, `a<a'` for adjacent nodes, `Γ` for denominators (done in `core-proofs.tex`). |
| 2 | minor | eq. `correction` | `ℓ_i(v)=0` is defined only for integer coordinates. A singleton grid would need it too. The phrase "a singleton stays a singleton" suggests singletons occur, but they never do after substitution, because retained hulls contain an interval. | Define `w_i(v)=0` whenever no admissible adjacent interval exists. State that every box in `P` keeps at least two points (Prop. `core:prop:filter`). |
| 3 | minor | Lemmas `contraction`, `localize`, `states` | The constants are correct but more complicated than needed (`B0=max{1,4L/(11g)}`, `1/15`, `22/15`, cap `100θ^{-1}⌈log2(n+2)⌉`). | A single invariant `‖y_j−x*‖² ≤ κ n h_j²` (in fact `8/15`) closes the induction in one line. The gap becomes `(9/16)Lnh_j²`, the witness bound `(17/15)κnh_j²`, and the radius `4.2√(κn)h_j`. The cap is `8θ^{-1}⌈log2(n+2)⌉` with common `L`, or `10θ^{-1}⌈log2(n_P+2)⌉` with per-coordinate dyadic meshes. See Lemmas `core:lem:inv` and `core:lem:states`. In checks, the actual worst-case grids reached 31% of the cap. |
| 4 | minor | Lemma `states` | The per-side count `1+⌈x⌉` is valid but loose; `⌈x⌉` suffices. | Lemma `core:lem:graded`(b). |
| 5 | minor | Sec. 3, certificate paragraph; Prop. `filter` | The certificate is described as containing messages, filtering decisions and upper bounds. None of these is necessary. "The last grid bound, together with all preceding filtering records" is correct but does not say what is minimal. | Theorem `core:thm:cert` and Remark `core:rem:mincert`. A certificate needs only the stage grids (or boxes plus centers, meshes and grading), one bound `β` and one feasible point. Each removed interval is checked against `β` itself (not against the intermediate `U_j`). Unsuccessful trials and stages with no removal can be dropped. Messages are optional, because checking them costs as much as recomputing them. |
| 6 | minor | Thm `approx` statement | It does not say in what sense the result is FPT. Termination without growth sits in a later paragraph instead of the theorem. `C` is not explicit. | Remark `core:rem:fpt`, Theorems `core:thm:schedule` and `core:thm:bits`: the parameter is `(p,κ̄)`, it is neither input nor computed, the result is polynomial in `q`, and `C=5` (schoolbook arithmetic). With Korhonen's 2-approximation the bound holds with `p=2tw+2`. |
| 7 | minor (paper vs code) | `certified_grid.py` `solve` | (a) The code uses per-coordinate corrections `max(0,A_ii)ℓ²/8` and endpoint grids `{lo,hi}` with zero correction for coordinates with `A_ii ≤ 0`. The paper uses a common `L`. (b) The code restarts each trial at the current **incumbent**, not at the lower endpoint vector. The incumbent can be a polished coordinate-descent point or a convex-presolve KKT point with unrelated denominators. | (a) The paper's theorem with common `L=max A_ii` covers this variant: smaller corrections only shrink `D`, and endpoint coordinates contribute zero to `D` and need no localization. The per-coordinate theory in `core-proofs.tex` matches the code directly. (b) The rate proof allows any feasible center. The paper's bit proof does not cover polished centers. A sketch shows that Gauss–Seidel polishing adds `O(nI)` bits per call to a common denominator, so the cost stays polynomial with an extra `O(μ*)` factor, but this is not written out. Either restart at the lower endpoint vector as the paper says, or state the variant and add the additive-denominator argument. |
| 8 | minor | Sec. 2, "Rescaling coordinates can change L/g" | This is true for `κ=L/g`, and avoidable. | Use `κ̄` (below). It is invariant under rescaling continuous coordinates. |

No critical or major mathematical issue was found.

## Developments on the cluster questions

**(a) Per-coordinate curvature.** *Resolved.* Use corrections
`L_i w_i(v)²/8`. The right conditioning parameter is `κ̄ = max{1,1/γ*}`, where
`γ*` is the best constant in `F(x)−F* ≥ γ Σ_{i:L_i>0} L_i (x_i−x_i*)²`
(Definition `core:def:growth`). Properties:

- `κ̄ ≤ κ = max{1,L/g}`.
- `κ̄` is invariant under rescaling continuous coordinates. For a separable
  quadratic, `κ̄ = 2` while `κ = 2·max L_i/min L_i`, so the saving can be a
  factor `(L_max/L_min)^{p/2}` in work.
- Coordinates with `L_i=0` need no growth, no uniqueness and no localization.
  They keep a two-endpoint grid. This recovers the paper's "all diagonals
  nonpositive" case and the Del Pia–Khajavirad observation that `q_ii ≤ 0`
  variables can be fixed at endpoints. Binary variables written with
  nonpositive squares are free in `κ̄`.

The algorithm uses dyadic meshes `h_ij = 2^{E−j−e_i}` with
`4^{e_i−1} < L_i ≤ 4^{e_i}`. This keeps all mesh lengths powers of two, which
also simplifies the denominator argument. Every proof (Lemmas
`core:lem:inv`, `core:lem:states`, Theorems `core:thm:schedule`,
`core:thm:bits`) is written in this form. Caveat for the exact-output cluster:
the reconstruction theorem uses Euclidean localization of every coordinate.
With seminorm growth, coordinates outside `P` sit at endpoints but are not
localized by growth, and exact recovery would need a separate discrete-gap
argument for them.

**(b) Constants.** *Resolved.* The cleanest correct version:

- admissibility `θ ≤ 1/4` and `8κ̄θ² ≤ 1`;
- invariant `‖y_j−x*‖²_L ≤ κ̄ n_P η_j²` and center bound `≤ 4κ̄ n_P η_j²`;
- gap `≤ (9/16) n_P η_j²`;
- witness `≤ (17/15) κ̄ n_P η_j²`;
- radius `8√(κ̄ n_P) h_ij` (+1 for integers);
- cap `10θ^{-1}⌈log2(n_P+2)⌉`;
- first admissible trial `2^{μ*} ≤ 6√κ̄`;
- `f(p,κ)=c0(c1 p√κ)^p κ(1+log2κ)^2`, exponent `5`.

With common `L` and `h_j=s2^{-j}`, the radius is `4.2√(κn)h_j` and the cap
`8θ^{-1}⌈log2(n+2)⌉`. None of this changes the theorem; it only shortens
proofs and reduces wasted work in failed trials.

**(c) Certificate content.** *Resolved* (Theorem `core:thm:cert`, Remark
`core:rem:mincert`). The record of removal stages is needed: the final grid
bounds `F` only on the final box. Everything else listed in the paper is
optional. This includes messages, min-marginal tables, intermediate
incumbents and upper bounds, centers and meshes (if grids are stored), and
all unsuccessful trials. Validity is checked against the claimed bound `β`.
The certificate is a branch-and-bound proof whose tree is a path. Checking
costs `k+1` dynamic programs, the same as the successful trial. The checker
in `checks/core_lib.py` implements exactly this content, and it rejected 23
tampered certificates.

**(d) Integer step rule and integer count.** *Verified, no error.*
`max{1,⌊h+θt⌋}` gives `w ≤ h+θ|v−c|` for intervals of length at least two,
including clipped ones. Unclipped steps are at least `(H+θt)/3` with
`H=max{h,1}`, using the split at `θt=2` when `h<1`. The `+1` in the integer
radius is necessary, because a unit interval survives through one good
endpoint. Exact checks covered 720 worst-radius grids, including `h<1`.

**(e) Bit complexity.** *Verified.*

- Denominators divide `Γ_X 2^α` with `α = J + O(I) + μK_μ` and do not
  multiply over stages. Centers and box endpoints are earlier nodes, and the
  initial center is the lower endpoint vector.
- With a common denominator, the dynamic program needs only integer
  additions and comparisons.
- The cap check happens before any table is formed, so an aborted stage
  costs `O(nK_μ)` arithmetic.
- `⌈log2(n_P+2)⌉^p ≤ 2p^p(n+2)` follows from `sup t^p e^{-t}=(p/e)^p`.

Totals give `f(p,κ̄)(I+q+1)^5`. The one gap is in the code, not the paper:
the code restarts at the incumbent (issue 7).

**(f) Sense of FPT.** *Resolved* (Remark `core:rem:fpt`). The running time is
at most `f(p,κ̄)(I+q+1)^5` on every instance with weighted growth. `κ̄` is a
property of the instance that the algorithm never receives or computes. `f` is
computable, and the exponent is independent of `(p,κ̄)` and polynomial in
`q`. Validity needs neither growth nor uniqueness. Without growth, the
schedule still halts with an `ε`-certificate (Theorem
`core:thm:schedule`(a)), but without the bound. Growth implies uniqueness of
`x*_P` only.

**(g) Necessity of the parameters.** *Sharpened, with complete proofs*
(Section `core:sec:lower`):

1. **Width.** ETH implies no `2^{o(p)}I^{O(1)}` algorithm even at `κ ≤ 2`.
   This holds for continuous box QP and for binary QP (Prop.
   `core:prop:lbwidth`: maximum independent set with a lexicographic
   tie-break plus `(x_i²−x_i)/(2n)`; multilinear rounding gives growth
   `1/(2n)` and `L=1/n`). Under SETH, via Lokshtanov–Marx–Saurabh, the base
   must be at least 2.
2. **Conditioning at width three.** See Prop. `core:prop:lbkappa` (an
   integer Subset Sum path encoding with `p=3`, a unique optimizer, and
   `log κ = O(m+log(A+t))`). Unless P = NP, no algorithm runs in
   `poly(I, log κ)`. Under ETH there is `c>0` with no `κ^c I^{O(1)}`
   algorithm. The paper's own algorithm is polynomial in `κ` at fixed `p`, so
   the dependence on `κ` is polynomial, not polylogarithmic, and that is
   necessary.
3. **Product form.** Under rETH there is no `f(p)(κI)^{o(p)}` algorithm
   (Prop. `core:prop:lbproduct`: a multicolored-clique encoding with integer
   selector chains, bag size `max{k,7}`, `κ` and `I` polynomial in `kN`, and
   the isolation lemma for uniqueness). Hence the exponent of `κ` must grow
   linearly in `p`. The upper bound has exponent `p/2+O(1)`, so the shape
   `f(p)κ^{Θ(p)}` is necessary up to the constant in the exponent.

A side consequence follows from the upper bound. Strongly NP-hard treewidth-2
instances (such as Del Pia–Khajavirad's) cannot have unique optimizers with
`κ` polynomial in `I` unless P = NP.

What failed:

- A deterministic version of item 3: a lexicographic tie-break makes
  `κ = N^{Θ(k)}` and loses the product form.
- A continuous version of item 3: encoding integer domains of size `N` with
  bounded-width quadratics needs bit expansions, which inflate `p` by
  `log N`.
- Whether the `p^p` factor, which comes from `(log n)^p`, is necessary.

**(h) Nonvacuous family.** *Resolved* (Example `core:ex:family`). Each block
`u²+v²−4uv+(u+v)/4+(ρ−u/2)²` on `[0,1]³` has an indefinite Hessian. Couple the
blocks by `(u_b−u_b')²/(16Δ)` along any graph. Then:

- the unique minimizer is non-vertex;
- global growth is `1/2`, `L ≤ 21/8`, so `κ ≤ 21/4`;
- every block-corner pattern is a strict local minimizer, giving `2^m` of them;
- `p = max{tw+1,3}`.

On a `k×m'` grid graph this gives a treewidth-`k` family with `2^{km'}` strict
local minima, solved in `f(max{k+1,3},21/4)(I+q+1)^5`. It is beyond forests,
so Del Pia–Khajavirad's exact algorithm does not apply, and it is not convex.
Honest caveat: the global minimizer is blockwise obvious to a human. Bounded
`κ` on bounded-width graphs forces each flipped block to cost a fixed amount
on average, so frustrated families with bounded `κ` tend to be locally
determined in an amortized sense. A variant with strong bilinear ferromagnetic
couplings (which do not raise `L`) appears to defeat local search with
bounded move size while keeping `κ` bounded. This was only sketched, not
proved, and it is not in the fragment. The real evidence that the theorem is
not vacuous is the combination of this family with items (g)1–3: bounded `κ`
alone, or bounded width alone, still allows hard instances.

## Classical versus new

- **Classical:**
  - Interpolation and Jensen per coordinate. The constant `L Σ w²/8` equals
    the αBB maximal separation with `α=L/2` (Androulakis–Maranas–Floudas
    1995).
  - Vertex optimality of coordinatewise-concave functions (Rosenberg 1972
    type).
  - Nonserial and junction-tree DP (Bertelè–Brioschi 1972; Dechter 1999).
  - Domain filtering and bound tightening.
  - The isolation lemma; ETH, SETH and W[1] lower-bound technology (IPZ 2001;
    CHKX 2006; LMS 2018).
- **Closest conceptual prior work** for the state bound is the cluster
  problem (Du–Kearfott 1994; Wechsung–Schaber–Barton 2014; Kannan–Barton
  2017, in the local KB). There, a second-order bound with a small prefactor
  relative to the minimum Hessian eigenvalue leaves an accuracy-independent
  number of boxes. Our condition `8κ̄θ² ≤ 1` is the analogue. The differences
  are that growth is global, grids are exact product DPs on tree
  decompositions, integer coordinates are included, growth is unknown with
  capped trials, and the result is a bit-complexity theorem. Added as Remark
  `core:rem:cluster`.
- **Comparators:**
  - Del Pia–Khajavirad 2026: exact on forests, strongly NP-hard at
    treewidth 2.
  - Bienstock–Muñoz 2018: `(1/ε)^{tw}` LP size, without conditioning.
  - Here the accuracy cost is `poly(log 1/ε)`, at the price of `κ`.
- **New, as far as I can tell:**
  - the FPT-in-`(p,κ)` bit bound for mixed-integer box QP;
  - the scale-invariant `κ̄`;
  - the minimal path certificate;
  - the three lower bounds as statements about this parameterization (the
    reductions themselves are standard).

  No prior statement of the combined result was found in the local KB.
  Priority is not asserted.

## Recommendations for the paper

| Result | Placement |
|---|---|
| Interpolation lemma (incl. conditional form) | main |
| Tree DP proposition | main, short (classical) |
| Safe filtering + path certificate theorem + minimal-content remark | main |
| Graded-grid lemma | main statement, proof in appendix |
| Stage invariants, localization/state bound | main statements, proofs in appendix |
| Schedule theorem (validity, termination without growth, work) | main |
| Bit-complexity theorem + FPT remark | main statement, proof in appendix |
| Per-coordinate curvature and `κ̄` | main: state the theorem with `κ̄` and note `κ̄ ≤ κ` |
| Cluster-problem remark | main, remark |
| Width lower bound (ETH, `κ ≤ 2`) | main |
| Conditioning lower bound at `p=3` | main |
| rETH product lower bound | main statement, proof in appendix (with isolation lemma) |
| Nonvacuous family | main as an example, proof in appendix |
| Common-`L` constants (radius 4.2, cap 8) | remark only |

## Open questions

1. Is the factor `p^p` (from `⌈log2(n+2)⌉^p`, aggregate localization)
   necessary, or can per-coordinate localization give `O(θ^{-1})` nodes per
   coordinate?
2. Is the exponent of `κ` exactly `Θ(p/2)`? There is no matching constant.
3. Do continuous instances, or deterministic reductions, also require
   `κ^{Ω(p)}`?
4. Can `κ̄` be replaced by a negative-curvature parameter such as `ν/g` (the
   extensions cluster)?
5. For the exact-output cluster: how should coordinates outside `P` be
   handled under seminorm growth?

## Citations to add (bibliographic details believed correct; specific theorem numbers not checked)

- `ImpagliazzoPaturiZane2001` (JCSS 63, "Which problems have strongly
  exponential complexity?").
- `ChenEtAl2006` (Chen, Huang, Kanj, Xia, JCSS 72, "Strong computational
  lower bounds via parameterized complexity"). The randomized/rETH
  transfer is argued in the text, not checked in a source.
- `LokshtanovMarxSaurabh2018` (TALG 14; arXiv 1007.5450). I recall the lower
  bound also holds with a supplied decomposition; not checked.
- `Korhonen2021` (FOCS 2021; arXiv 2104.07463: `2^{O(k)}n`, width `2k+1`;
  confirmed by search).
- `MulmuleyVaziraniVazirani1987` (Combinatorica 7).
- `BerteleBrioschi1972` (Nonserial Dynamic Programming).
- `DuKearfott1994` and `WechsungSchaberBarton2014` (both in the local KB).
- The ETH lower bound for Subset Sum (no `2^{o(m)}`) is stated in
  Abboud–Bringmann–Hermelin–Shabtay (arXiv 1704.04546). The `O(m)`-bit form
  used here follows from the textbook 3-SAT reduction plus sparsification.

## Verification actually run (targeted; no project-wide checks, no CI)

All from `paper-decomposition-aware/process/w1/checks/`:

- `nice python3 check_pipeline.py`: all assertions passed. 24 certificates
  accepted, 23 tampered certificates rejected, 210 admissible-stage
  invariant checks.
- `nice python3 check_grid_count.py`: 720 worst-radius grids; the largest
  grid was 31% of the cap.
- `nice python3 check_families.py`: ETH width family, Subset Sum family, and
  block family all passed.
- `nice python3 check_clique_gadget.py`: 14 clique encodings checked by exact
  counting DP.
- `pdflatex` of `core-proofs.tex` in a throwaway wrapper under `/tmp`: no
  errors; only the new citation keys are undefined.

These finite checks support the proofs; they do not replace them.
