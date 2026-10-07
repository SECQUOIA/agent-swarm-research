# Repair record: points, constraints, and algebraic chapters after review R1

Author: Opus main-revision writer. Date: 2026-10-05.

This record answers `evidence/reviews/points-r1.md`,
`evidence/reviews/constraints-r1.md`, and the final
`evidence/reviews/algebraic-r1.md` (R1–R6), together with the findings the
root relayed in its task messages and Luna's AG5 clearance. Line numbers
refer to the files as they stand after this repair.

Files edited: `sections/02-points.tex`, `appendices/C-points.tex`,
`sections/05-constraints.tex`, `appendices/D-constraints.tex`,
`sections/06-algebraic.tex`, `appendices/E-algebraic.tex`, and this record.
No other file was changed. In particular, `sections/00-introduction.tex`,
`sections/01-models.tex`, `sections/abstract.tex`, `macros.tex`, `main.tex`,
and `references.bib` were not edited. No literature search, source browsing,
or KB ingestion was done. No experiment, mathematical script, project-wide
check, or CI inspection was run. The `paper-exact-arithmetic/` tree is
untracked in Git and no pre-edit copies were saved, so this record quotes the
old wording where it matters.

## Readiness

Every listed finding is repaired in the text. No theorem, lemma,
proposition, or corollary statement changed, apart from three contract or
hypothesis clarifications that weaken nothing a proof uses: contract (E3c)
is stated for graphs without isolated nodes, `lem:constraints-artificial`
states that a fixed arc imposes no reduced-cost condition, and (AG5) gains
its exact locator. One analytic derivation was added
(`rem:algebraic-curvature`). The inventory rows covered by these chapters
(P1–P10, C1–C8, M1–M5, S1–S11, B3, and E1 in `evidence/coverage-map.md`, as
mapped in the original author reports) keep their statements, proofs, and
strengthenings. These include the P8/P9 strengthenings, the cubic
transverse constant, the dense-Gram `L=O(n^4 log n)` accounting with
exponent `1/4`, the restricted (AG3) range, the (AG6) surface clause, and
the five-variable degree 21 argument.

One label was added (`rem:algebraic-curvature`); none was removed or
renamed. No citation key was added or removed. The six files cite 47
distinct keys; 28 of them still await the vetted bibliography (see "Open
source gates").

## Points (`points-r1.md` and root items)

### P1. Input length of the fixed-degree families (medium)

Old: `02:573` "The input has length O(n log n)" and `02:619` "the input
length is O(n log n)".

New: `02-points.tex:582–587` and `:635–636`. With every exponent vector
written in full (Definition `def:models-polynomial`), both families have
`L=Θ(n^2)`: they have Θ(n) monomials, each with an exponent vector of n or
n+1 entries. The regularization paragraph now says that the quantities
bounded below in Proposition `prop:points-regularization`(b),(c), namely
`(log Γ)/ϑ` and the bit length of λ, are exponential in n, hence
`2^{Ω(√L)}`: superpolynomial, not exponential, in L. The later sentences of
that paragraph (`:588–597`) say "exponential in n" instead of "exponentially
many". The lower bounds themselves are unchanged.

### P2. "Exponentially longer than the inputs" (low)

Old: `02:592`. New: `02-points.tex:604–610`: the exact formats "can have
length exponential in the dimension, hence superpolynomial in the input
length". The same sentence now says that the multiplier rectangles have
treewidth two rather than path structure.

### P3. Rectangle certificate attributed to the wrong definition (low)

Old: `02:31–32` cited `def:models-representations` for "a rational box that
certifies the optimizer". New: `02-points.tex:28–34` separates exact
representations (Definition `def:models-representations`) from certificates
such as an enclosing rational box (Proposition `prop:points-rectangle`).

### P4. Interaction graph not defined (review suggestion)

New: `02-points.tex:453–456`, one sentence before the first use: the
vertices are the variables, and two variables are adjacent when some monomial
with a nonzero coefficient contains both. No use of "interaction graph" or
"treewidth" in Section 02 precedes it.

New: `C-points.tex:1050–1057`, paragraph "Treewidth". It states why the bag
constructions in the proofs suffice: every objective with a claimed
treewidth bound is a sum of terms in at most three variables, every monomial
of the expansion occurs in some term, and a tree of bags covering each term,
with connected occurrences of each variable, is a tree decomposition. The
paragraph is restricted to objectives with a treewidth claim, because the
PosSLP gate objective of Theorem `thm:points-quartic-lower`(b) has terms in
more variables and carries no treewidth claim.

### P5. Square Root Sum and PosSLP (source contract)

Old: `02:445` "Square Root Sum reduces to PosSLP". New:
`02-points.tex:448–451`: Allender et al. show that Square Root Sum is
decidable in polynomial time with a PosSLP oracle and that both problems lie
in the counting hierarchy; Theorem `thm:posslp-closure`(b) turns that oracle
algorithm into a polynomial-time many-one reduction to one PosSLP instance.
This matches the oracle form already used in `00-introduction.tex:55–57` and
`01-models.tex:409–410`, and the vetted literature report's "Turing bridge"
description. The duplicate citation in the preceding sentence was removed.

### Points: further corrections found during the recheck

- `02-points.tex:50–52`. The selector's value-bit price omitted the norm
  bound: it is now `O(d(q+log Γ+log R))`, with R a bound on the norm of the
  selected optimizer. This is the formula of `02-points.tex:207–210` and of
  Lemma `lem:selector`.
- `02-points.tex:64–68`, `:157–158`, `:325–326`, `:674–675`, `:726–727`.
  Dimension-exponential statements now say "exponential in the dimension" or
  "in n", or "superpolynomially many monomials" for the expansion example,
  as INTEGRATION.md requires. The summary-table cell now says "treewidth at
  most two" instead of "paths", because the multiplier rectangles have
  treewidth two.
- `02-points.tex:632–633`. The root-circuit sentence now names its gates: the
  recurrence uses n−1 additions and n−1 square-root gates. "Root circuit" is
  defined with precise gates in `06-algebraic.tex:118–123`.
- `02-points.tex:595`. "vanilla Tikhonov selection" became "plain Tikhonov
  selection".

The source items in `points-r1.md` (GLS contract, Ahmadi–Chaudhry–Zhang,
Ahmadi–Hall, EY2010, Tarasov–Vyalyi, Hoffman1952) are not text defects; they
remain with Luna and the root. The introduction and abstract items of that
review belong to the framing writer and were not touched.

## Constraints (`constraints-r1.md` R1–R5 and the root items)

### R1. Fixed arcs in the artificial-cost lemma (medium)

`D-constraints.tex:832–861`. The optimality conditions are now stated for
arcs with `U_e>0`; an arc with `U_e=0` imposes no reduced-cost condition,
because the multipliers of its two bounds absorb any reduced cost. Such an
arc has no residual arc, so the shortest-path potential argument is
unchanged. In the concluding convexity inequality its term is zero because
`s'_a=s^*_a=0` (`:857–859`). The reviewer's two-node counterexample to the
old wording no longer applies. The bound on artificial costs and the
exclusion of artificial flow are unchanged.

### R2. Operation count, isolated nodes, and the lower-bound shift (low)

`D-constraints.tex:798–811`. Contract (E3c) is now stated for a graph with
`m'≥1` arcs and no isolated nodes, with `O(m'^4 log(m'+2))` operations, so
the count is meaningful for one arc. A following paragraph says that an
isolated node must have zero demand and is deleted with `O(|V|)`
comparisons; a nonzero demand there means infeasibility. This restricts the
cited contract and does not broaden it.

`D-constraints.tex:869–890`. The flow corollary proof now deletes isolated
nodes after substituting fixed arcs, and states the shift explicitly: with
`s=y−ℓ` the capacities become `[0,u_e−ℓ_e]`, the demands become `b−A_Gℓ`
(computed once), and the linear coefficient becomes `c_e+2a_eℓ_e` (a
constant number of gates per arc). This puts every Taylor subproblem in the
form of `lem:constraints-artificial`. The Taylor-model flow variable is now
called y, so that s denotes only the shifted variable.

### R3. Multipliers "unbounded by any function of L" (low)

`D-constraints.tex:1342–1343`: "It need not be rational or unique, and the
proof uses no bound on its norm." The complementary-slackness argument is
unchanged.

### R4. "No lower bound on |p_j| is available" (low)

`05-constraints.tex:999–1006`: no inverse-polynomial lower bound on `|p_j|`
is assumed, and Lemma `lem:separation` guarantees only a doubly
exponentially small one, so fiber values approximated to polynomially many
bits do not certify the bit. I did not claim that the designated coordinate
is tiny in the constructed family: `rem:reductions-rational-length` proves
tininess for the generator-gate coordinate, not for the output-gate
coordinate `p_j`. The hardness corollary does not depend on this sentence.

### R5. Zero-dimensional branch after fixing variables (low)

`D-constraints.tex:757–762` (boxes): if every coordinate is fixed, then
`P={ℓ}`; the procedure evaluates `h(p)` exactly, reports every bound as
active, and stops, so neither the transfer theorem nor the box procedure is
called on an empty set of variables. `D-constraints.tex:871–874` (flows): if
no arc remains after fixed arcs are substituted, the same is done with both
bounds of every arc reported as active.

### Root item: known zero optimum in the binary corollary

`05-constraints.tex:990–992`, directly after `cor:constraints-binary`:
subtracting 1/4 from H gives an equivalent instance with known optimal value
zero; the optimal solution, the Hessian, and the full Hessian Gram matrices
do not change. This matches the M5 source's "minimum zero" form.

### Constraints: further corrections

- `05-constraints.tex:408–411`: the accuracy count `G(k)T(L)` is now
  "exponential in n" for unconstrained objectives of nonlinear dimension n.
- Overfull boxes: see the table at the end.

## Algebraic (`algebraic-r1.md` R1–R6, root items, AG5)

The repairs already made by the original writer were kept: the dense
canonical-Gram input accounting `L=O(n^4 log n)` with exponent 1/4
(`06-algebraic.tex:411–417`), the restricted (AG3) range (`E:1247–1261`), and
the (AG6) surface clause (`E:1286–1290` with its use at `E:1701–1712`).

### R1. The realization point is necessarily algebraic (medium)

Old: `06:309` "The point p need not be algebraic, need not be known, and need
not be rational". New: `06-algebraic.tex:314–319`. The hypotheses force p to
be algebraic: n of the residuals have a nonsingular Jacobian at p, so a small
rational box isolates p among their real common zeros, and the transfer
argument in the proof of `lem:one-real-conjugate` applies. The construction
uses no algebraic representation of p, and p need not be known or rational.
The lemma statement is unchanged.

In the same paragraph (`:320–324`) the vague "points given by circuits"
became the actual uses: gate values of certified odd-root circuits and of
rational unit-quaternion circuits (Section 04), cube-root chains and repeated
complex squaring (Section 07), and points with coordinates in towers of
radicals (Section 08).

### R2. Curvature without the factor n needs its own proof (low)

New: `E-algebraic.tex:444–483`, Remark `rem:algebraic-curvature`, referenced
at `06-algebraic.tex:302–304`. It proves part (b) of
`lem:quartic-realization` under `ε ≤ ν^2μ^2/(36(Λ+mβ)^2)`, with the other
conditions kept. With `s=‖u‖`, the degree-0 terms give at least `2εν^2‖v‖^2`.
The degree-2 terms give at least `(4μ^2−4εm)s^2‖v‖^2 ≥ 2μ^2s^2‖v‖^2`. The
degree-1 terms are bounded by `12ε(Λ+mβ)s‖v‖^2`, using only operator norms
at vectors `w(u,v)`. Hence

    Hess Φ ⪰ [2εν^2 − 12ε(Λ+mβ)s + 2μ^2 s^2] I ⪰ (3/2) εν^2 I.

The minimum over s is `2εν^2 − 18ε^2(Λ+mβ)^2/μ^2`, the Schur bound with n
replaced by 1. The full-Gram bound of part (c) keeps the factor n, as the
reviewer and root required. The remark says only that the proof of (c) uses
n; it does not claim that n is necessary.

### R3. "The zero set is an ellipsoid, not a point" (low)

Old: `06:645–646` parenthetical. Removed: `06-algebraic.tex:667–668` now
keeps only the exact identity `g_p̂(w_*)=f(p)=0` for every rational centre,
which is all the assembly uses.

### R4. Points at infinity; generic combinations (low)

`06-algebraic.tex:492–496`: after a rational change of coordinates, global
convexity leaves the square factors without common **real** zeros at
infinity. `:537–542`: the text adds that common complex zeros at infinity may
remain, and that the residual of length one or three lies in a complete
intersection of n rational linear combinations of the square factors,
chosen generically for length three. This matches the appendix: the first
bound uses n selected factors, the second uses a generic rational matrix A
(`E:1423–1436`).

### R5. Cyclic integer magnitudes (low)

`E-algebraic.tex:940–945`: the integers used in the denominator-clearing and
scaling step (`z_i, Q_1, M_1, a_1, b_1, S_0, D_0`, and the coefficients of
`2r_j`) have magnitude polynomial in n. The O(n)-bit integers `d_n, e_i`
enter only through the weights `w_i` and are never coefficients. I rechecked
that `D_0L_ϱ` has entries `S_0(S_0b_1^2−a_1^2Q_1^2)δ_ij + 2a_1^2Q_1^2 z_iz_j`,
so the `O(log(n+1))`-bit claim for the `s_i` holds.

### R6. Normalization of P in the power-coordinate explanation (low)

`06-algebraic.tex:348–354`: the algorithm first replaces P, which may be any
rational multiple of the minimal polynomial including a negative one, by the
monic `P_1`. The paragraph now uses `(T−α)P_1(T)(1+T^2)^e` with
`e=n−(d+1)/2`, as in the appendix (`e=n−s−1`, `s=(d−1)/2`).

### Root item: rational circuits cannot output irrational coordinates

Old: `06:117` "shared arithmetic circuit, radical expression, or tower of
extensions" and `06:403–405` "Short circuit or radical output is not
excluded". New:

- `06-algebraic.tex:113–127` defines **root circuits** with precise gates:
  rational circuits (Definition `def:models-circuits`) that may also contain
  gates `z ↦ z^{1/k}`, returning the positive real k-th root of a positive
  input, with the integer `k≥2` written in binary. The text states that
  rational circuits alone compute only rational numbers.
- `06-algebraic.tex:418–423`: each `p_i=2^{e_i/d_n}` is determined by its
  O(n)-bit rational exponent, and since `e_{i+1}=−2e_i−1`, `p_1=1/a` and
  `p_{i+1}=1/(ap_i^2)` with `a=2^{1/d_n}`. Hence one root gate with the
  O(n)-bit index `d_n`, applied to 2, followed by O(n) multiplications and
  divisions, is a root circuit for the whole optimizer. I checked the
  recurrence against `e_0=0, e_1=−1, e_2=1, e_3=−3`.
- `06-algebraic.tex:603–604`: the univariate realization G is computed by a
  rational arithmetic circuit **with input T**. This is a circuit for a
  polynomial, not for an irrational number.

### AG5 (Luna clearance) and AG2 (optional clarity)

`E-algebraic.tex:1268–1285`. Following Luna's clearance, (AG5) now cites
EJP Theorem 3.2 and Remark 3.3 for the residual count, and Fulton
Proposition 4.1 for the Segre class of a local complete intersection,
singular or not. The unvetted "Chapter 9" locator was dropped; Fulton–
Lazarsfeld is not cited. One sentence records that the cited count holds for
an arbitrary closed subscheme cut out by forms of degree at most two, and
that the lci property is used only for the Segre-class formula. The formula,
the hypotheses, the generic perturbation, and the implicit-function
persistence step (`E:1764–1771`) are unchanged, as Luna confirmed no formula
correction is needed.

`E-algebraic.tex:1245–1246`: (AG2) now says "every linear form that vanishes
at no point of Z is a nonzerodivisor on S/(F_1,…,F_N)".

## Overfull boxes from the root's first full build

| Old location | Width | Repair | New location |
| --- | --- | --- | --- |
| `D:381–384` | 29.16pt | ν moved to a display | `D-constraints.tex:381–386` |
| `D:515–521` | 1.67pt | sentence reworded | `D-constraints.tex:518–521` |
| `E:38` | 3.85pt | two long equalities split across lines | `E-algebraic.tex:26–38` |
| `E:139` | 2.35pt | `gathered` | `E-algebraic.tex:133–141` |
| `E:382` | 1.73pt | `gathered` on two lines | `E-algebraic.tex:379–386` |
| `E:407–414` | 2.94pt | identity displayed | `E-algebraic.tex:411–416` |

No font size or global setting was changed.

## Open source gates (for Luna and the root)

These are contracts, not internal proof gaps. Each statement in the text is
proved locally given the contract as written.

- Bibliography: 28 keys cited in these files await `literature.bib`:
  `AriHildebrand2026, ArratiaBollobasSorkin2004,
  BalisterBollobasCutlerPebody2002, Basu2023Integers, BasuPollackRoy2006,
  BorweinErdelyi1995, DelPia2023, Eisenbud1995, EisenbudGreenHarris1996,
  EisenbudSturmfels1996, Fulton1998, GaertnerMatousekRuestSkovron2008,
  GranotSkorinKapov1990, Harris1992, Hartshorne1977, Hatcher2002,
  HildebrandGoess2024, HildebrandKoeppe2013, Hoffman1952,
  KurdykaSpodzieja2015, LoncParolWojciechowski2001, MehlhornSagraloffWang2015,
  Milnor1965, OertelWagnerWeismantel2014, Pan2002, Schonhage1982, Tutte1948,
  vanAardenneEhrenfestDeBruijn1951`. Two key pairs need unification:
  `GaertnerMatousekRuestSkovron2008` here versus
  `GaertnerMatousekRustSkovron2008` in the introduction, and
  `BasuPollackRoy2006` here versus `BasuPollackRoy1996` in Section 07.
- `AllenderEtAl2009`: locator for the P^PosSLP bound on Square Root Sum
  (the vetted report names Propositions 1.1/1.3 for the Turing bridge).
- `Vegh2016` Theorem 20 and Section 6.1: confirm that the quadratic count is
  `O(m^4 log m)` for graphs without isolated nodes and that the output is the
  exact rational optimum. The restated contract is weaker than the old one.
- (AG3) EGH CB5/CB7 in the restricted range; (AG6) Harris Corollary 18.12 for
  varieties of arbitrary dimension (surface clause); network contracts (N1)–
  (N4); `MehlhornSagraloffWang2015` Theorem 5; `BorweinErdelyi1995` Markov
  inequality locator. EJP (AG5) and Scheiderer are cleared per the root and
  STATUS; their exact source report is still to come.
- Points: GLS locators (STATUS reports GLS verified), Ahmadi–Chaudhry–Zhang
  Lemma 5, Ahmadi–Hall Theorem 2.3, EY2010, Tarasov–Vyalyi, SSW version.
- Constraints: GLS Theorem 6.6.3, KTK, Gärtner et al. Theorem 27,
  Ari–Hildebrand Definition 3.4/Theorem 3.5, Del Pia Theorem 3,
  Hildebrand–Köppe Theorem 1.1, as listed in `constraints.md`.

## Items for other owners (not edited)

- `00-introduction.tex:350–353` says the cyclic family's dense and sparse
  lists are "exponentially long". Section 06 now says exponential in n and
  `2^{Ω((L/log L)^{1/4})}` in L, which INTEGRATION.md requires to be kept
  distinct.
- `00-introduction.tex:124–126` says "exponentially many bits" for the
  regularization family. Section 02 now gives `2^{Ω(√L)}` with `L=Θ(n^2)`.
- `00-introduction.tex:119`, `:386`, `:390` use "interaction graph" before
  its definition in Section 02 (`02-points.tex:453–456`). A forward reference
  may help.
- The only other owner that cites a label touched here is Section 08 /
  Appendix G, which applies `lem:quartic-realization` with the n-dependent
  condition. That condition is unchanged, so those uses remain valid.

## Checks actually run (targeted; not CI)

- Scratch build of a copy of the manuscript in `/tmp/pca-r1-build` with
  `latexmk -pdf -interaction=nonstopmode main.tex`, run twice: once after
  the edits and once after the final wording changes. Both runs finished
  with no LaTeX errors and no undefined or multiply defined references. The
  only warnings were 155 unresolved citations, which await the bibliography.
  The output was 296 pages. The log has no overfull box in any of the six
  files; the only overfull box (0.24pt) is in
  `appendices/J-quadratic-contrast.tex`, which I do not own. The repository's
  own build artifacts were not touched.
- `pdftotext` on page 182 of the scratch PDF, to check the rendering of
  Remark E.2 (`rem:algebraic-curvature`).
- `python3 verification/check_manuscript.py`: 26 source files, 612 labels,
  1648 references, 118 cited works, and 87 errors. All 87 are missing
  bibliography keys; 28 of them are cited in these files and none is new.
  There were no missing labels, duplicate labels, or unfinished-text
  findings.
- `grep`/`sed`/`awk` inspection of the six files to locate every instance of
  the repaired phrases and to record line numbers.
- Analytic rechecks by hand, with no scripts: the curvature estimate of R2,
  the cyclic recurrence `e_{i+1}=−2e_i−1`, the `D_0L_ϱ` integrality and
  magnitude, the `Θ(n^2)` input lengths, the fixed-arc KKT conditions and
  residual graph, the lower-bound shift formulas, and the binary-corollary
  Hessian and Gram invariance under subtracting a constant.

No experiment, historical mathematical script, project-wide verification, or
CI inspection was run. This internal review is not external peer review.
