# Scout report: mixed-integer convex representability and formulation size

Area: `micp-representability`. Date: 2026-09-28. Scratch files:
`research-20260928b/scouting/micp-representability/` (two scripts and
downloaded open preprints in `src/`).

**Bottom line.** The cleanest open target is Lubin, Vielma and Zadik's (LZV)
second open question: *is every compact MICP-representable set a finite union of
compact convex sets?* This scout proves the answer is yes whenever the
formulation has at most two integer variables. The proof gives a new
dichotomy: if the recession cone of the integer index set is two-dimensional,
or is a ray or line in an irrational direction, a compact represented set must
be convex. A general-dimension proof by induction looks feasible. Its solver
significance is low. The formulation-size questions are more relevant to
solvers but are either close to corollaries of known work (mixed-integer
SDP/SOCP lower bounds on integer variables) or hard (a conic analogue of
"Balas is optimal"). Recommended score: **4/10**.

Verification scope: I ran only targeted checks: the two scratch scripts
listed at the end and text extraction of the downloaded PDFs. The proofs
below are first-pass sketches. No one has reviewed them, and no CI check
applies.

---

## 1. Frontier map

### 1.1 Exact representability results

Notation (LZV Def. 1.1–1.5). A closed convex set
`M ⊆ R^{n+p+d}` *induces an MICP formulation* of `S` if
`S = proj_x(M ∩ (R^{n+p} × Z^d))`. The index set is `I = proj_z M`, and the
z-projected sets (fibers) are `A_z = proj_x(M ∩ {z})`. "Binary" means that
integer-feasible `z` lie in `{0,1}^d`; "pure" means `p = 0`.

| Result | Assumptions | Conclusion | Source (checked) |
|---|---|---|---|
| Jeroslow–Lowe | rational polyhedral `M` | `S` is rational MILP-R iff `S = ∪_i P_i + intcone(U)` with rational polytopes `P_i` and a finite `U ⊆ Z^n`. Binary rational MILP-R sets are exactly finite unions of rational polyhedra with a common recession cone. | Stated as LZV Thm 1.1 and §1.1, [[lubin2022-mixed-integer-convex-representability]] p.2-3. The original was not retrieved. |
| Jeroslow (pure binary) | `p = 0`, binary | Pure binary MICP-R sets are exactly finite unions of closed convex sets with equal recession cones. | LZV Prop 4.1, p.9 |
| LZV binary MICP-R | binary, `p` arbitrary | `S` is binary MICP-R iff it is a finite union of projections of closed convex sets, with no recession-cone condition. Constructive; one extra continuous variable suffices for unions of closed convex sets. | LZV Prop 4.2, p.10-11 |
| Midpoint lemma | none | If `S` is `w`-strongly nonconvex (`w` points whose pairwise midpoints lie outside `S`), then MICP rank ≥ ⌈log₂ w⌉. Rank-1 matrices, the spherical shell, integer points on a parabola and the primes are not MICP-R. For `S ⊆ {0,1}^n`, general integers do not beat ⌈log₂|S|⌉. | LZV Lemma 4.1, Cor 4.1, Prop 4.4, Cor 4.2, p.11-14 |
| Rational MICP-R structure | index set *rationally unbounded* (Def 5.1: every rational affine image is bounded or has a nonzero integer recession direction); `S` closed; convex subsets of `S` have uniformly bounded diameter | `S` = a finite union of compact convex sets and closed periodic sets | LZV Thm 5.1, p.16 (proof §6, p.20-32) |
| Compact rational case | `S` compact | Rational MICP-R ⇔ finite union of compact convex sets ⇔ pure binary ⇔ binary | LZV Prop 5.4, p.18-19 |
| Subsets of N | `S ⊆ N` infinite | Rational MICP-R ⇔ finite set ∪ periodic set ⇔ finite set ∪ infinite rational MILP-R set | LZV Prop 5.5, p.20; IPCO version Thm 2, arXiv 1611.07491 p.8 |
| Closure properties | — | MICP-R, binary MICP-R and rational MICP-R are closed under finite unions. Rational MICP-R is *not* closed under intersection, while rational MILP-R is closed under intersection but not under union. | LZV Prop 5.3, p.17-18 |
| Irrational data | — | `{x ∈ Z : frac(√2 x) ∉ (0.4, 0.6)}` is MILP-R with irrational data but not rational MICP-R. **Rational SOC data can produce such index sets** (LZV (1.5)/Lemma A.2; IPCO Example 2 builds `K_ε` from rational `L³` constraints). | LZV p.4-5, Cor 5.2 p.16; arXiv 1611.07491 p.7 |
| Recession cones and shapes | general integers | A rational MICP-R set in R⁴ can have countably many recession cones (fibers indexed by interior integer points share one cone, Prop 2.1). A rational MICP-R set can be a disjoint union of regular polygons with unboundedly many sides. If all fibers have equal volume, the fibers are translates of at most 2^d sets (Brunn–Minkowski). | [[zadik2024-shapes-and-recession-cones-in]] Prop 2.1, Lemma 2.1 p.4-6; Cor 3.1 p.7-9; Thm 3.1 p.10-11 |
| Ellipsoidal and convex quadratic | one convex quadratic plus linear constraints | Binary EMI-R ⇔ `∪(E_i ∩ P_i) + C` with a common cone `C`. The rational mixed-integer case adds `intcone`. Bounded mixed-binary convex quadratic sets are `∪(Q_i ∩ P_i)`. | [[pia2018-ellipsoidal-mixed-integer-representability]] p.4-5; [[pia2019-characterizations-of-mixed-binary-convex]] p.4-8 |
| MILP-R and Chvátal functions | rational | MILP-R = affine Chvátal sets; a strict hierarchy up to DMIAC | [[basu2019-mixed-integer-linear-representability-disjunctions]] p.4-10, p.17-18 |
| Bilevel | rational | The closure of MIBL-R sets equals finite unions of generalized MI-R sets | [[basu2021-mixed-integer-bilevel-representability]] p.8-10 |
| Application | — | Distributionally favorable optimization problems are MICP-R | Jiang–Xie, arXiv 2401.17899 (abstract only) |

**Resolved conjecture.** The arXiv v1 of LZV ("Regularity in mixed-integer
convex representability", 1706.05135v1, 2017) posed Conjecture 1 (Finite
Similar Shapes): every MICP-R set is a union of fibers homothetic to finitely
many sets (v1 p.13). Zadik–Lubin–Vielma's regular-polygon union (Cor 3.1)
defeats it. In any representation each fiber lies inside one polygon, and
covering a polygon's edges by countably many convex fibers from finitely many
homothety classes permits only finitely many edge directions. That argument is
this scout's; I did not check whether the 2024 paper frames Cor 3.1 as
refuting Conjecture 1.

### 1.2 Formulation size and number of integer variables

| Result | Statement (assumptions) | Source |
|---|---|---|
| Embedding complexity | Ideal embedding formulations `conv ∪ (P_i × {h_i})`. SOS2 with Gray codes needs 2⌈log₂n⌉ general facets. Grid triangulations need ≥ n/2+1. | [[vielma2018-embedding-formulations-and-complexity-for]] p.5-18 |
| Combinatorial ideal formulations | An ideal formulation needs ≥ ⌈log₂ d⌉ binaries. Pairwise independent branching ⇔ biclique cover. | [[huchette2019-a-combinatorial-approach-for-small]] p.8-16 |
| Branching formulations | Strong "mixed-integer branching" formulations with **two** integer variables for any disjunctive constraint, motivated by the log lower bound | Huchette–Vielma, arXiv 1709.10132 (abstract) |
| Cayley embedding (convex) | `Q(C) = conv ∪(C_i × {e_i})` is closed and ideal. Nearly homothetic sets need one gauge inequality. Support-function tests separate sharpness from idealness. | [[vielma2019-small-and-strong-formulations-for]] p.7-8, p.22-24 |
| P-split | Hierarchy between big-M and the hull for separable convex disjunctions | [[kronqvist2026-p-split-formulations-a-class]] |
| Balas is optimal | For every odd dimension d there are two polytopes such that any formulation of `conv(P₁∪P₂)` with poly-many inequalities needs Ω(d) extra variables (facet counting). The same holds approximately and for lift-and-project. | Conforti–Di Summa–Faenza, arXiv 1711.00891 (abstract; Thm 2/3 scanned) |
| MILEF integer-variable bounds | Any MILEF of the matching polytope with poly-many constraints needs Ω(√n/log n) integer variables | Hildebrand–Weismantel–Zenklusen, arXiv 1611.00707 (via citations) |
| Lifting framework | Def 3: ε-MILEF (Q a **polyhedron**). Thm 4: ε-MILEF of complexity (m,k) ⇒ (ε+δ)-LEF of size m(1+k/δ)^{O(k)}. **Thm 10 holds for any convex D** (flatness theorem). Matching, cut, TSP and odd-cut need Ω(n/log n) integer variables. The §7 gaps are stable set, TSP O(n) versus O(n log n), and a log factor; original-space matching needs Ω(n). | Cevallos–Weltge–Zenklusen, arXiv 1712.02176 p.6-10, p.30-32 (downloaded, read) |
| Stable set and knapsack | Poly-size MIP formulations need Ω(n/log²n) integer variables. (1+ε/n)-approximate EFs have size 2^{Ω(n/log n)}. | Schade–Sinha–Weltge, arXiv 2308.16711 (Math. Prog. 216 (2026) 135–176); intro read |
| psd lower bounds | CUT, TSP and STAB have no spectrahedral lift of dimension < 2^{n^c}. Poly-size SDPs equal O(1)-degree SOS for max-CSP approximation. | Lee–Raghavendra–Steurer, arXiv 1411.6317 (abstract) |
| Block-size psd bounds | Lifts over products of fixed-size psd cones of CUT have exponential size. Block size 2 rules out small SOCP formulations. | Fawzi–Parrilo, arXiv 1311.2571 (abstract) |
| MISDP modeling | Exact MISDP formulations for QAP, graph partition and others | de Meijer–Sotirov, arXiv 2306.09865 (abstract) |
| Coefficients and binarization | Strong IP formulations may need exponentially large coefficients. Comparison of binary extended formulations. | [[hojny2021-strong-ip-formulations-need-large]] p.4-19; Dash–Günlük–Hildebrand, arXiv 1801.01208; [[aprile2021-binary-extended-formulations-and-sequential]] |

### 1.3 Repository overlap

`paper-integer-dimension/` (84 pp.) already develops parity/midpoint lower
bounds on the number of integer variables in ε-accurate convex
mixed-integer approximations of nonlinear graphs. Its "parity contact" volume
arguments are effectively the covering/colouring form of the midpoint lemma
(`sections/00-introduction.tex` l.80–82, 218–231). **I therefore do not pursue
"integer variables for ε-accurate MICP relaxations of nonconvex functions".**
`notes/open-problems-from-literature.md` item 33 lists the LZV questions as
"open (partly addressed in zadik2024)". Zadik 2024 does not address compact
sets or the midpoint question; a grep for "compact" found only restatements of LZV.

### 1.4 Sources examined

- Local: `lubin2022-...` (read intro, §2, §4–5 and the conclusion at p.33 in full;
  §6 skimmed); `zadik2024-...` (intro, §2–3 statements, Thm 3.1 proof);
  `pia2018`, `pia2019`, `basu2019`, `basu2021`, `vielma2018`, `vielma2019`,
  `huchette2019`, `kronqvist2026`, `hojny2021`, `aprile2021`, `lyu2023`,
  `hildebrand2018`, `kis2022`, `lyu2026` (notes read; full texts grepped for
  "open/conjecture/future"); `paper-integer-dimension/` sections (grep);
  `research-20260922/scouting/scout_area678_convex_decomp_new.md`.
- Downloaded (open arXiv), in `src/`: 1712.02176 (CWZ: Defs, Thms 4, 10, 11,
  §7), 2308.16711 (SSW: intro), 1711.00891 (CDF: theorem scan), 1611.07491
  (LZV IPCO: §5, Example 2; no open-question list), 1706.05135v1 (v1: abstract,
  Conjecture 1).
- Abstract pages: 1709.10132, 1801.01208, 2401.17899, 2306.09865, 1411.6317,
  1311.2571, 2002.09788.
- Semantic Scholar citation lists (API): 1706.05135 (25 citing works),
  1611.07491 (same list), 1712.02176 (16), 1611.00707 (11); 2103.03379 returned
  none. No citing work addresses the LZV open questions. The theoretical
  follow-ups are only Zadik 2024 and the Del Pia–Poskin and Basu papers.
- Web search: 7 queries (MICP representability plus compact, midpoint,
  MISDP extension complexity, Weltge 2025, CWZ). The shared session budget was
  then exhausted. **Novelty checks are therefore thin. An unsuccessful search
  does not establish that a question is open.**

---

## 2. Open questions

LZV's open questions, paraphrased from
[[lubin2022-mixed-integer-convex-representability]] p.33:

1. Does the necessary condition for MICP representability given by the midpoint lemma
   (Lemma 4.1) also suffice?
2. Can Proposition 5.4 dispense with rationality? Equivalently, must every compact
   MICP-R set be a finite union of compact convex sets?
3. Is Theorem 5.1 still valid under a weaker condition on the diameter of its convex subsets?

**Q-A (best candidate; LZV Q2).** Let `M` be closed convex and let
`S = proj_x(M ∩ (R^{n+p} × Z^d))` be compact. Is `S` a finite union of compact
convex sets? Quantitative refinement: describe the pieces through the lattice
structure of `I` and the recession cone `K = rec(cl I)`.
*Evidence that it is open:* posed in MOR 2022; the 2024 follow-up by the same
authors addresses other questions; no citing work resolves it (§1.4).
*Why rationality matters for solvers:* LZV's rationality is a condition on the
index set, not on the data. Rational SOC data can already create irrational
index sets (IPCO Example 2), so Prop 5.4 does not cover all realistic
MISOCP formulations.

**Q-B (formulation size, relevant to solvers).** Do mixed-integer SDP or SOCP
extended formulations of polytopes with no small approximate extended
formulation also need many integer variables? For example: does every MISDP
formulation of the cut polytope of size 2^{o(n^c)} need n^{Ω(1)} integer
variables? Does every MISOCP formulation of the matching or stable-set polytope
of polynomial size need Ω̃(n) general integers?
*Evidence:* CWZ and SSW define formulations with a polyhedral `Q` (CWZ
Def 3); their §7 and the SSW introduction discuss only linear formulations; no
citing work treats the conic case. LZV Cor 4.2 is the only conic
integer-variable bound, and it counts points of subsets of `{0,1}^n`.

**Q-C (conic "Balas is optimal").** Let `C₁, C₂ ⊆ R^n` be SOC- or
LMI-representable with descriptions of size `f`. Must every SOC or SDP
extended formulation of `cl conv(C₁ ∪ C₂)` of size poly(f) use Ω(n) additional
variables (conic analogue of CDF Thm 2)? Weaker: for two non-homothetic
ellipsoids, is O(1) extra variables possible? Vielma 2019 Prop 2 shows that one
extra variable suffices for nearly homothetic sets.
*Relevance:* this is exactly the P-split and Cayley question of whether sharp
convex-GDP formulations can avoid variable copies. *Evidence:* CDF's proof
counts facets, which does not transfer to non-polyhedral sets. I found no
conic version.

**Q-D (sets of integers; LZV Q1).** Characterize MICP-R subsets of `Z`
without rationality. Conjecture: finite unions of cut-and-project (model) sets
with convex windows, plus finite sets. A concrete test: **is
`N \ {2^k : k ≥ 1}` MICP-representable?** (§3.5 shows it is not rational MICP-R
and escapes both the midpoint and colouring bounds.) Solver significance is
negligible; the interest is theoretical.

LZV Q3 (the diameter assumption) was not pursued.

---

## 3. First-pass mathematics on Q-A

### 3.1 Setup and basic lemmas

Let `S ⊆ B(0,R)`, `P = I ∩ Z^d` and `K = rec(cl I)`.

- **(L0) Concavity.** `A_{Σλ_i y_i} ⊇ Σλ_i A_{y_i}` for `y_i ∈ I`. Hence the
  support function `σ_u(y) = sup_{x∈A_y} u·x` is concave on `I`, and
  `|σ_u| ≤ R|u|` on `P`.
- **(L1) Rational monotonicity.** If `z ∈ P`, `r ∈ Z^d` and `z+Nr ∈ I` for all
  `N`, then `A_{z+r} ⊇ (1-1/N)A_z + (1/N)A_{z+Nr}`, so `A_z ⊆ cl A_{z+r}`.
  Along rational recession directions, fibers therefore increase.
- **Reductions.** If `P` is finite, `S` is a union of `|P|` convex sets. If
  `aff P` is a proper rational subspace, apply a unimodular change and reduce
  `d`. Replacing `I` by `I ∩ cl conv P` does not change any fiber at a point
  of `P`.

### 3.2 Theorem A (d ≤ 2): the answer to Q-A is yes

**Theorem A.** Suppose `S` is compact and has an MICP formulation with `d ≤ 2`
integer variables. Then `S` is a finite union of compact convex sets. Moreover,
suppose `P` is infinite and affinely spans `R^d`. For `d = 1`, `S` is convex.
For `d = 2`, if `K` is neither a rational ray nor a rational line, `S` is
convex.

*Proof sketch.* The case `d = 1` follows from L1: `I` is unbounded, so the
fibers are nested and their union is convex. The irrational and
two-dimensional case for `d = 2` goes as follows. Choose `r ∈ ri K` with
irrational slope. This is possible when `K` is an irrational ray or line, or
when `dim K = 2`.

1. *(Bounded interior fibers.)* Let `y ∈ int I`. The tube `y + B_ε + R_+ r`
   lies in `int I`. By Kronecker's theorem it contains far lattice points
   `w₁, w₂` on both sides of the line `y + Rr`. The half-triangle
   `y + [0,½](conv{w₁,w₂} − y)` contains a lattice point `p` once it is long
   enough. Concavity at `p = λ₀y + λ₁w₁ + λ₂w₂` with `λ₀ ≥ ½` gives
   `σ_u(y) ≤ 4R|u|`. The same bound for `−u` gives `|σ_u| ≤ 4R|u|` on `int I`.
2. *(Monotone limits.)* A bounded concave function on a ray is nondecreasing.
   Hence `A_y ⊆ cl A_{y+tr}`, and `B(y) := cl ∪_t A_{y+tr}` exists. `B` is
   constant along `r` and concave in `y`, so `U := ∪_{y∈int I} B(y)` is convex
   as the projection of a convex graph.
3. *(Realization, `cl U ⊆ S`.)* By Dini's theorem on compact transversal sets,
   applied jointly in `u`, far lattice points `q` near the ray `y + R_+r`
   satisfy `d_H(cl A_q, B(q)) → 0`. Such points exist by Kronecker's theorem,
   and `B(q) → B(y)` by continuity of concave functions. Since `S` is closed,
   `B(y) ⊆ S`.
4. *(Absorption, `A_z ⊆ cl U` for every `z ∈ P`, including extreme and
   boundary lattice points.)* Take far lattice points `w₁, w₂ ∈ int I` with
   different transversal offsets. For fixed `λ₀ > 0`, the scaled triangle
   `z + λ₀(conv{z,w₁,w₂} − z)` contains a strip of fixed width whose direction
   tends to the irrational `r` and whose length tends to infinity. For far
   enough `w_i`, it therefore contains an interior lattice point `y` whose
   barycentric weight on `z` is at least `1−λ₀`. Hence
   `dist(x, A_y) ≤ 2Rλ₀` for every `x ∈ A_z`, and `A_y ⊆ B(y) ⊆ U`.

   Together, `S = ∪_P A_z ⊆ cl U ⊆ S`, so `S` is convex.

*Rational ray or line.* After a unimodular change, `r = e₁`. Let `J` be the
far transversal extent. Lattice points satisfy `z₂ = c` with `c ∈ cl J`; a
point with `c ∉ cl J` would give a far point outside `J`. On lines with
`c ∈ int J`, L1 applies because far points `(T,c)` lie in `int I`. So
`B_c = cl ∪_t A_{(t,c)}` is a concave family in `c`, and the `d = 1` argument
gives finitely many pieces. The at most two lines with `c ∈ ∂J` each give one
piece or finitely many points. This argument also covers non-closed `I` that
fail LZV's rational-unboundedness condition even though `K` is rational, for
example `{0<z₂<1, z₁≥0} ∪ {0}`. ∎

Consequences:

- **(Proved, given the sketch.)** Theorem A extends LZV Prop 5.4 to *every*
  formulation with at most two integer variables. This includes the
  √2-type index sets produced by rational SOC data.
- **(New structural fact.)** For a bounded set, unbounded integer variables
  whose index recession is two-dimensional or irrational cannot create
  nonconvexity. Only rational one-dimensional recession, which behaves like a
  strip, can.
- Example: `I = R_+ × [0,1]` with fibers `{0}` and `{1}` on the two boundary
  lines gives `S = {0,1}`. With `I = R²_+`, the same attempt fails: `(1,1)` is
  a combination of `(1,0)` and `(1,N)` with weights `1−1/N` and `1/N`, which
  forces `1/N ∈ S`.

### 3.3 Computation: absorption of extreme lattice points

`sail_absorption.py` takes the index set `I = conv(sail vertices) + R_+(1,α)`.
The sail vertices are the best lower approximations of `α`, so `I` has
infinitely many extreme lattice points. For each vertex `z`, the script
computes the smallest weight `λ` that interior lattice points place on points
other than `z`, using hull points up to `x ≤ T`. It computes these gauges with
scipy's ConvexHull in floating point; this is an illustration, not a proof.

| α | z | λ at T=200 | λ at T=2000 | λ at T=20000 |
|---|---|---|---|---|
| golden | v0=(1,0) (lower-ray corner) | 0.091 | 0.028 | 0.0072 |
| golden | v4=(34,21) | 0.079 | 0.022 | 0.0083 |
| √2−1 | v2=(29,12) | 0.111 | 0.030 | 0.0085 |
| √2−1 | v4=(985,408) | (outside window) | 0.030 | 0.0089 |

`λ√T` stays between 0.9 and 1.7. This matches the `T^{-1/2}` rate that
Dirichlet approximation predicts. Every extreme lattice point, including the
corner on the boundary ray, is absorbed into the interior fibers, as step 4
claims.

### 3.4 Plan for general d (coset-collapse induction)

1. Reduce so that `P` affinely spans `R^d`, and replace `I` by
   `I ∩ cl conv P`.
2. Pick a generic `r ∈ ri K`. Let `W` be its rational hull, the smallest
   rational subspace containing it. The line `R r` is dense in the torus
   `W/(W∩Z^d)`.
3. If `W = R^d`, Theorem A's argument works verbatim with simplices of `d`
   far vertices, so `S` is convex.
4. Otherwise, within each lattice coset `c + W` that meets `ri I`, collapse
   the fibers to `U_c` as in steps 1–4. Show that `c ↦ U_c` is a concave
   family over `π(I) ⊆ R^d/W`. That yields an MICP formulation with
   `d − dim W` integer variables, to which induction applies. When `dim W = 1`
   (rational `r`), use L1 and LZV's relaxation along `r`.
5. Treat lattice points in boundary cosets or lower-dimensional faces either
   by absorption (as in §3.2 step 4, or L1 along inward rational directions)
   or by induction on the face.

Main obstacles:

- **(a)** Showing that only finitely many faces are left unabsorbed when `I`
  is non-polyhedral and has infinitely many faces.
- **(b)** Keeping fibers bounded at real points when `W ≠ R^d`, by working
  inside the lattice-rich region.
- **(c)** Closure issues from non-closed `I` and continuous auxiliaries.

**Estimate:** 2–5 weeks for a rigorous general proof, about 15–25 pages,
comparable to LZV §6. I put about 25% probability on a counterexample, or on
needing extra hypotheses, for `d ≥ 3`. A counterexample would itself answer
the question.

### 3.5 Side results on the midpoint lemma (LZV Q1)

- **Trivial "no" for non-closed sets.** The irrationals in `[0,1]` are not a
  countable union of convex sets (Baire), so they are not MICP-R. Yet no three
  of them have all pairwise midpoints rational: `2x₁ = (x₁+x₂)+(x₁+x₃)−(x₂+x₃)`
  would be rational. So the set is 2-strongly but not 3-strongly nonconvex.
- **Closed set, rational version.** Let `S = N \ {2^k : k ≥ 1}`.
  - No three distinct positive numbers have all pairwise sums equal to powers
    of two. Pairs of different parity have non-integer midpoints. Hence
    `w(S) = 4`, witnessed by `{1,7,6,10}`, and the midpoint lemma gives only
    rank ≥ 2.
  - `S` is not finite ∪ periodic: some residue class modulo any period
    contains infinitely many powers of 2. So by LZV Prop 5.5, `S` is **not
    rational MICP-R**.
  - The midpoint condition is therefore insufficient for rational
    representability, even for closed subsets of `N`. Whether `S` is MICP-R at
    all is the test question in Q-D.
- **Colouring strengthening (immediate from LZV's proof).** The parity of the
  chosen index properly colours the graph `G_S` whose edges are pairs with
  midpoint outside `S`. So rank ≥ ⌈log₂ χ(G_S)⌉ ≥ ⌈log₂ ω(G_S)⌉. For
  `N \ {2^k}`, `χ = ω = 4`: within each parity class, `G_S` is bipartite
  (colour by the odd part mod 4), so colouring does not help either. For
  random `S ⊆ [N]`, a heuristic estimate gives `ω(G_S) = O(log N)` but
  `χ(G_S) ≳ N/log N`. That would be a log-versus-loglog gap between the two
  bounds, but I have not proved it. `midpoint_chromatic.py` (exact bitset max
  clique, N ≤ 120) does not yet separate the bounds: both give 4. Low priority,
  because the repository's parity-contact method already uses the covering
  form.
- **Compact analogue (conditional).** `[0,1]` minus tiny open gaps around
  `2^{-k}` has infinitely many components and apparently small `w`. By
  Theorem A it has no formulation with at most 2 integer variables; if Q-A
  holds in general, it is not MICP-R at all. I did not pin down its exact `w`.

### 3.6 First-pass on Q-B (for comparison)

**Proved by composition:** CWZ Thm 10 is stated for any convex `D`, and the
slices `D ∩ H` of a spectrahedral shadow are spectrahedral shadows. With
bounded or binary integers the number of fibers is at most `2^k`. So a binary
MISOCP formulation with total cone dimension `m` and `k` binaries gives an
exact lift over 2×2 psd blocks of size `O(2^k m)`. (SOC splits exactly into
3-dimensional cones.) Fawzi–Parrilo then force `k ≥ cn − log₂ m` for
`CUT_n`. LRS similarly give n^{Ω(1)} binaries for binary MISDP formulations of
CUT, TSP and STAB of size 2^{o(n^c)}.

For *general* integers one needs **approximate** psd or fixed-block lower
bounds with relative distance 1/poly. These are the missing ingredient. LRS's
CSP approximation theorem, with constant gaps, may supply them for
3-XOR/3-SAT-type polytopes; I have not checked this. For matching, even the
exact psd extension complexity is open.

Assessment: easy for binaries (probably folklore, but I did not find it
stated) and genuinely open for general integers.

---

## 4. Significance

| | Q-A (compact) | Q-B (MISDP/MISOCP integers) | Q-C (conic Balas) |
|---|---|---|---|
| **Proved if solved** | For bounded sets, general integer variables never add modeling power beyond binaries for *any* MICP formulation, including rational-data MISOCP with irrational index sets. There is an explicit link between index-set recession and nonconvexity. | Limits on how few integer variables conic mixed-integer models of CUT, TSP, STAB and others can use | Whether sharp convex-GDP formulations must copy variables |
| **Plausible benefits** | A rationality-free route to LZV Thm 5.1 (possibly Q3); cleaner modeling guidance; a basis for the structure theory of MICP-R subsets of `Z` (Q-D) | Guidance for MISDP modeling (de Meijer–Sotirov) and for Pajarito/SCIP-SDP users | A theoretical ceiling (or a new small formulation) for P-split and Cayley hierarchies |
| **Speculative** | Presolve that detects replaceable general-integer structure | New approximate psd lower bounds of independent interest | New copy-free ideal formulations for unions of ellipsoids (robotics, power systems) |
| **Still needed for practical value** | Pieces are not constructive or bounded in number; a certificate or algorithm would be needed | Positive constructions matching the bounds | Tight constructions and computational tests |

The area as a whole is structural. Its route to faster solvers is indirect.
The closest links to solvers are Q-C and log/ideal formulations, which are
already well developed (Vielma, Huchette, Lyu).

---

## 5. Recommendation

Take Q-A only as a **short, self-contained theory paper**. It would answer a
published open question: prove the general-`d` theorem by coset-collapse
induction, using Theorem A as the base case and model. The note would
include the "irrational or two-dimensional recession ⇒ convex" dichotomy and
the §3.5 examples on midpoint insufficiency. Feasibility is good: Theorem A is
done in sketch, and the induction plan is concrete. Originality is good: the
question was posed in MOR 2022, and I found no resolution with a limited
search. Significance for solvers is low. Q-B for general integers is the best
solver-facing extension, but it depends on approximate psd lower bounds that
may not exist yet. Q-C is important but I see no viable technique. The area
should not displace a direction with a direct algorithmic payoff.

**Score: 4/10** (significance 3, feasibility 7, originality 7). Q-B scores
about 4 and Q-C about 3.

---

## Commands run (targeted only)

- `python3 sail_absorption.py`: absorption weights (§3.3 table).
- `python3 midpoint_chromatic.py`: clique versus colouring bounds on random
  `S ⊆ [N]`, N ∈ {40, 80, 120} (§3.5).
- `pdftotext` on the downloaded arXiv PDFs; Semantic Scholar and arXiv
  abstract fetches via `curl`.

No project-wide verification was run, and CI was not consulted.
