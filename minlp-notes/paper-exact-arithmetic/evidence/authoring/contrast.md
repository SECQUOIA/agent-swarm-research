# Author report: contrast (Appendices J and K)

Author: Opus main-writing agent `contrast`. Date: 2026-10-05.

## Files

Written: `appendices/J-quadratic-contrast.tex` (section label `app:qc`) and
`appendices/K-boundaries.tex` (section label `app:boundaries`, the label
already used by the framing sections). No other manuscript file, shared
macro, bibliography, historical note, or other writer's file was edited.
Scratch compilation used `/tmp/qc-check`, outside the repository.

## Scope

Appendix J covers coverage entries Q1–Q12 as arithmetic comparisons, with Q7
as a short classical caveat (DECISIONS D3). Q13–Q14 are not covered and are
not mentioned. At the root's request, J also contains a proved feasible-point
parallel of Q3 from the independent-block extension of
`few-quadratic-unbounded-degree.md` (`cor:qc-feasible-output`).

Appendix K covers the fully zero Hessian proposition and the three partial
degeneracy counterexamples (coverage section 8, item 2), the selected
nullvector obstruction (G6), the uncertain-equality information limits
(section 8, item 12), and the succinct root penalty with its corrected scope:
explicitly expanded quadratic input, a polynomial-size **nonconvex**
quadratic lift, and exponential degree only after eliminating the lift
(prewrite-boundaries correction).

## Coverage map to labels

| Map ID | Statement | Proof |
| --- | --- | --- |
| Q1 | `thm:qc-span-two` (density, rational affine hull, polynomial-time rational output, hence polynomial-size witness); `prop:qc-two-rows`; `lem:qc-tangency`; `prop:qc-span-three` (irrational singleton, three PD ellipsoids, no rational exposing aggregate) | J.3, complete |
| Q2 | `thm:qc-degree` (joint degree B(n,k) over K), `thm:qc-height` (heights, separation), `thm:qc-sharp` (sharpness); supporting `lem:qc-restriction`, `lem:qc-ordered`, `lem:qc-kkt`, `lem:qc-parameter`, `lem:qc-ordered-limits`, `lem:qc-elimination`, `cor:qc-radius`, `prop:qc-decision` | J.2, complete |
| Q3 | `prop:qc-block`, `lem:qc-split`, `thm:qc-blocks`, `cor:qc-no-fpt-output`, `lem:qc-weight` (explicit weight), `lem:qc-translate`, `thm:qc-sparse` | J.5, complete |
| Q3 feasible parallel (root request) | `lem:qc-kummer`, `prop:qc-binomial-block` (explicit three-ellipsoid binomial blocks, O(log(da))-bit coefficients), `cor:qc-feasible-output` (span exactly 3k, full ellipsoids, sheared coordinate R_0+Σϖ_b^{1/d} of degree d^k with all coefficients nonzero, L=O(k³d² log(kdϖ_k))) | J.5, complete |
| Q4 | `prop:qc-quartic` (degree from `lem:qc-kummer` with d=3) | J.6 |
| Q5 | `def:qc-certificate`, `lem:qc-sound`, `thm:qc-certificate`, `lem:qc-sign`; primal construction `cor:qc-feasible-point` | J.8, J.7 |
| Q6 | `thm:qc-pencil` | J.4 |
| Q7 | `prop:qc-pell` | J.11 |
| Q8 | `thm:qc-corank-one` (necessity and the planar converse, both proved) | J.4 |
| Q9 | `thm:qc-number-field-qp` | J.10 |
| Q10 | `thm:qc-rational-infeasibility`, `prop:qc-infeasibility-lower` | J.9 |
| Q11 | `thm:qc-height` over a number field (D and B enter linearly) | J.2 |
| Q12 | `thm:qc-recovery` (with the cited `thm:qc-kll`), application `cor:qc-feasible-point` | J.7 |
| Section 8 item 2 | `prop:bnd-zero-hessian`, `prop:bnd-newton`, `prop:bnd-kernel`, regularization remark | K.1 |
| G6 | `prop:bnd-nullvector`, `lem:bnd-common-kernel` | K.2 |
| Section 8 item 12 | `prop:bnd-fixed-gap`, `prop:bnd-robust-root`; `thm:bnd-root-penalty`, `prop:bnd-penalty-limits` | K.3, K.4 |

## Labels defined

Appendix J: `app:qc`, `tab:qc-summary`, `app:qc-setting`, `def:qc-native`,
`lem:qc-heights`, `app:qc-degree`, `lem:qc-restriction`, `lem:qc-ordered`,
`lem:qc-kkt`, `lem:qc-parameter`, `lem:qc-ordered-limits`, `thm:qc-bezout`,
`thm:qc-degree`, `lem:qc-elimination`, `thm:qc-height`, `cor:qc-radius`,
`prop:qc-decision`, `thm:qc-sharp`, `app:qc-rational`, `lem:qc-tangency`,
`prop:qc-two-rows`, `thm:qc-span-two`, `prop:qc-span-three`, `app:qc-spectra`,
`thm:qc-pencil`, `thm:qc-corank-one`, `app:qc-short`, `prop:qc-block`,
`lem:qc-split`, `thm:qc-blocks`, `cor:qc-no-fpt-output`, `lem:qc-weight`,
`lem:qc-translate`, `thm:qc-sparse`, `lem:qc-kummer`,
`prop:qc-binomial-block`, `cor:qc-feasible-output`, `app:qc-quartic`,
`prop:qc-quartic`, `app:qc-recovery`, `thm:qc-kll`, `thm:qc-recovery`,
`cor:qc-feasible-point`, `app:qc-certificates`, `lem:qc-sign`,
`def:qc-certificate`, `lem:qc-sound`, `thm:qc-certificate`, `app:qc-infeasible`,
`thm:qc-rational-infeasibility`, `prop:qc-infeasibility-lower`,
`app:qc-number-field`, `thm:qc-number-field-qp`, `app:qc-pell`,
`prop:qc-pell`; equations `eq:qc-system`, `eq:qc-minpoly-height`,
`eq:qc-differences`, `eq:qc-kkt`, `eq:qc-generic-kkt`,
`eq:qc-partial-fractions`, `eq:qc-block`, `eq:qc-block-value`,
`eq:qc-rational-aggregate`, `eq:qc-hoffman`.

Appendix K: `app:boundaries`, `app:bnd-degenerate`, `prop:bnd-zero-hessian`,
`prop:bnd-newton`, `prop:bnd-kernel`, `app:bnd-nullvector`,
`prop:bnd-nullvector`, `lem:bnd-common-kernel`, `app:bnd-uncertain`,
`prop:bnd-fixed-gap`, `prop:bnd-robust-root`, `app:bnd-penalty`,
`thm:bnd-root-penalty`, `prop:bnd-penalty-limits`.

`thm:qc-bezout` and `thm:qc-kll` are cited classical theorems stated in a
theorem environment with the citation in the title; no new environment was
introduced.

## Labels used from other files

All resolve in the current manuscript (the scoped checker reports no
undefined references):

- `thm:exact-upper` (K, six uses): the curvature-dependent Newton refinement
  whose hypotheses K examines.
- `thm:singleton-field` and `cor:algebraic-three-quadrics` (J.3, J.4): one
  real conjugate characterization and the three-ellipsoid realization.
- `lem:convex-value` (J.2, `prop:qc-decision`). Used exactly in the form of
  part (a) as now stated in Section 02: rational box P=[-R,R]^n, the convex
  function ν = max{0, g_i, affine rows} with explicit rational bounds W and
  G, exact rational values and subgradients (gradient of a maximizing row),
  accuracy η/3. Nothing beyond part (a) is assumed.
- `def:models-representations` (J.1); `sec:constraints` (J.11);
  `sec:heights`, `sec:fields-certificates` (K.2).

## Macros

No new macros. The absolute logarithmic Weil height is written with the
existing `\height`, defined locally in J.1 with subscripts `\rm proj` and
`\rm aff`. Fraktur and `\operatorname{...}` are used for local symbols.
Notation: L total binary length, n continuous dimension, k Hessian span (the
structural parameter of this appendix), q precision, f objective, p
canonical optimizer, θ optimal value. Λ is not used, in line with the
curvature reservation; the multiplier bound in `thm:qc-blocks` is
\bar\gamma.

## Bibliography keys

Present in `references.bib`: `KozlovTarasovKhachiyan1980`,
`GroetschelLovaszSchrijver1988`, `NieRanestad2009`, `SlotSteurerWiedmer2025`.

Already used by other authors (in `evidence/cited-keys.txt`), same intended
works: `BasuPollackRoy2006`, `BienstockDelPiaHildebrand2023`,
`BombieriGubler2006`, `Davenport2000`, `DedieuMalajovichShub2005`,
`DelPiaDeyMolinaro2017`, `Hoffman1952`, `KannanLenstraLovasz1988`,
`MorganSommese1987`, `Rockafellar1970`, `SafeyElDinZhi2010`, `Serre2008`,
`Vavasis1990`, `vonzurGathenGerhard2013`.

New proposed keys (details from the inspected source records; Luna to vet):

| Key | Work | Used for |
| --- | --- | --- |
| `AdachiIwataNakatsukasaTakeda2017` | Adachi, Iwata, Nakatsukasa, Takeda, Solving the trust-region subproblem by a generalized eigenvalue problem, SIAM J. Optim. 27(1) (2017) 269–291; inspected author manuscript eqs. (1.6), (2.5), Sec. 3.2 | credit: secular equation and degree-2n reduction (J.5) |
| `BasuMohammadNezhad2024` | Basu, Mohammad-Nezhad, Improved effective Łojasiewicz inequality and applications, Forum Math. Sigma (2024), doi 10.1017/fms.2024.66; Theorems 2.2 and 4.1 | contract: effective inequality and one-block QE with coefficient bounds (K.4) |
| `Canny1990` | Canny, Generalized characteristic polynomials, J. Symbolic Comput. 9 (1990) 241–250 | credit: perturbation to a finite quotient (J.2) |
| `Deimling1985` | Deimling, Nonlinear Functional Analysis, Springer 1985, Brouwer degree chapter | contract: regular-value formula, homotopy invariance (K.3) |
| `FranekRatschanZgliczynski2016` | Franek, Ratschan, Zgliczynski, Quasi-decidability of a fragment of the first-order theory of real numbers, J. Automated Reasoning 57 (2016); arXiv 1309.6280, Theorem 6, Lemma 8 | credit: robust zeros (K.3) |
| `FrankWolfe1956` | Frank, Wolfe, An algorithm for quadratic programming, Naval Res. Logist. Quart. 3 (1956) 95–110 | contract: attainment of a quadratic bounded below on a polyhedron (J.10) |
| `GiesbrechtRoche2010` | Giesbrecht, Roche, Interpolation of shifted-lacunary polynomials, Comput. Complexity 19 (2010) 333–354 | credit: basis dependence of sparsity (J.5) |
| `GrigorievPasechnik2005` | Grigoriev, Pasechnik, Polynomial-time computing over quadratic maps I, Comput. Complexity 14 (2005) 20–52; Theorem 1.10, Sec. 2 | credit: ordered limits, staircase quotients (J.2) |
| `JeyakumarLi2014` | Jeyakumar, Li, A new class of alternative theorems for SOS-convex inequalities and robust optimization, Applicable Analysis 94 (2015) 56–74 (online 2014); inspected manuscript dated 2013-07-18, Theorem 2.5. Year in key to be fixed by Luna | credit: real positive-aggregate alternative (J.9) |
| `JiaChoiMourrainWang2011` | Jia, Choi, Mourrain, Wang, An algebraic approach to continuous collision detection for ellipsoids, CAGD 28 (2011) 164–176, Theorem 3.10 | credit: repeated roots of contact determinants (J.3) |
| `JiaoPhamTuyen2025` | Jiao, Pham, Tuyen, Exact penalty functions in optimization with unbounded constraint sets, arXiv 2507.03424v2, Theorem 5.2, Remark 5.3(ii) | credit: fractional exact penalties on compact sets (K.4) |
| `Kollar1999` | Kollár, An effective Łojasiewicz inequality for real polynomials, Period. Math. Hungar. 38 (1999), Example 1 | credit: power-chain exponents (K.3) |
| `Lenstra2002` | H. W. Lenstra Jr., Solving the Pell equation, Notices AMS 49(2) (2002) 182–192 | credit: Pell output length (J.11) |
| `LiangLiBai2013` | Liang, Li, Bai, Trace minimization principles for positive semi-definite pencils, Linear Algebra Appl. 438 (2013) 3085–3106, Lemma 3.8(2) | credit: real spectra of PSD pencils (J.4) |
| `LuoZhang1999` | Luo, Zhang, On extensions of the Frank–Wolfe theorems, Comput. Optim. Appl. 13 (1999) 87–110, Theorem 1 and Corollary 2 | contract: attainment for convex QCQP with linear objective (J.9) |
| `Neukirch1999` | Neukirch, Algebraic Number Theory, Springer 1999 | contract: Eisenstein criterion, total ramification, Hensel's lemma (J.5) |
| `Nesterov2025` | Nesterov, Quartic regularity, Vietnam J. Math. 53 (2025) 553–575, Lemma 4 | credit (K.1) |
| `Rouillier1999` | Rouillier, Solving zero-dimensional systems through the rational univariate representation, AAECC 9 (1999) 433–461; the inspected record used Bouzidi–Lazard–Pouget–Rouillier, arXiv 1303.5042, Sec. 3.1 | credit: RUR derivative mechanism (J.7); Luna may prefer the BLPR source |

## External contracts and verification status

Luna's `literature-review.md` has no Appendix J/K rows and `literature.bib`
is not yet available, so every contract below remains **unverified by
Luna**. The two partial consistencies noted come from rows written for other
chapters.

1. Multihomogeneous Bézout bound for isolated, in particular nonsingular,
   zeros, allowing positive-dimensional components (Morgan–Sommese 1987;
   Dedieu–Malajovich–Shub 2005, Sec. 5, Thm 5.1). Used in `thm:qc-degree`.
   The text transfers the statement from C to an algebraic closure of
   K(ε,δ) by field embedding.
2. Nie–Ranestad generic count: for generic coefficients the
   equality-constrained quadratic critical system has exactly 2^s binom(n,s)
   complex solutions (Thm 2.2, Cor 2.5, Sec. 3.2). Used only in
   `thm:qc-sharp`. Consistent with Luna's description (generic statement).
3. Hilbert irreducibility in density form for integral specializations of an
   irreducible polynomial over Q(u_1..u_r) (Serre, Topics in Galois Theory,
   thin sets and Theorem 3.4.4). Used in `thm:qc-sharp`.
4. Convex KKT with affine constraints and a strict point for the nonlinear
   constraints (Rockafellar Thms 28.2–28.3). Used in `lem:qc-kkt`,
   `thm:qc-certificate`.
5. Exact rational convex QP (Kozlov–Tarasov–Khachiyan) and rational LP in
   polynomial time (GLS). Used in `thm:qc-number-field-qp`,
   `thm:qc-span-two`.
6. Frank–Wolfe attainment; Luo–Zhang Corollary 2 attainment for convex QCQP
   with finite infimum. Used in `thm:qc-number-field-qp` and
   `thm:qc-rational-infeasibility`.
7. KLL Theorem 1.19 recognition, as stated in `thm:qc-kll` (degree bound e,
   coefficient bound A, approximation within 2^{-ς}/(12e), time polynomial
   in e, log A and the approximation length). Used in `thm:qc-recovery`.
8. Polynomial-time univariate gcd, resultant and evaluation over Q
   (von zur Gathen–Gerhard). Used in `lem:qc-sign`.
9. Tarski–Seidenberg transfer to the real algebraic numbers (BPR). Used in
   `thm:qc-corank-one`.
10. Prime number theorem for arithmetic progressions modulo 4 (Davenport).
    Used in `cor:qc-no-fpt-output`.
11. Eisenstein criterion, total ramification of Eisenstein roots, ramification
    index bounding valuation denominators, Hensel's lemma for simple roots
    (Neukirch). Used in `prop:qc-block`, `lem:qc-split`, `thm:qc-blocks`.
12. Weil heights, product formula, independence of the ambient field
    (Bombieri–Gubler). Used in J.1; the needed inequalities are proved in
    `lem:qc-heights`.
13. Brouwer degree (Deimling). Used only for the robustness clause of
    `prop:bnd-robust-root`(b); parts (a), (c), (d) are elementary.
14. Basu–Mohammad-Nezhad Theorem 4.1 (one-block QE: degree d^{O(κ)},
    coefficient bits τ d^{O(κ)O(ℓ)}) and Theorem 2.2 (g^q ≤ C h with
    q ≤ (8d)^{2(n+7)}, log₂C ≤ τ d^{O(n²)}). Used in `thm:bnd-root-penalty`.
15. Slot–Steurer–Wiedmer v1, Theorem 1.1/Corollary 1.2 (objective-gap
    approximation for globally convex polynomials). Credit only in K.1;
    consistent with Luna's verified description of v1.

## Deviations from the source notes and new analytic derivations

These are the places a fresh review should check most carefully.

1. **Exact decision at fixed span (`prop:qc-decision`).** The radius comes
   from the height of the minimum-norm feasible point
   (`cor:qc-radius`, from `thm:qc-height`), not from Grigoriev–Pasechnik
   sampling; the decision then uses `lem:convex-value` and the value gap of
   `cor:qc-radius`(b). The gap is linear in log R, so the bound stays
   L^{O(k+1)}.
2. **Constructive span-two output (`thm:qc-span-two`(b)).** Rewritten to use
   only exact feasibility decisions. Rows identically tight on F are found by
   gap tests on F∩[-2R,2R]^n (attainment by compactness, no attainment
   theorem); the strict branch fixes δ equal to a gap bound on a box of
   radius 3R; a single quadratic is handled by the same margin/zero-set
   recursion. Vavasis, KTK and the fixed-span value algorithm are no longer
   used, and the polynomial-size witness follows from the algorithm.
3. **Q2 and Q11 merged.** One elimination lemma over a number field with
   local norms (`lem:qc-elimination`) gives both the rational height bound
   and the linear dependence on D and B. The sharp degree theorem is stated
   over K (`[K(p):K] ≤ B(n,k)`); the parameter-lemma proof is identical over
   any real field. The sources state B(n,k) over Q and only
   (2n+1)^{min(k,n)} over K, so this K-statement is a new (short) derivation.
4. **Linear forms.** `thm:qc-height` is stated for c^T p as well (needed for
   the certificate encoding); the proof is the same.
5. **Minimal polynomials from annihilators.** Bounds use the elementary
   Cauchy/Gauss argument (`eq:qc-minpoly-height`), not Mignotte or Mahler.
6. **Q9 output step.** Instead of common-field recognition, the active set
   at p is identified exactly from an approximation and the separation
   bound in F, and p is computed from the rational pseudoinverse chart. KLL
   is not used for Q9.
7. **Verifier (`lem:qc-sign`).** Elementary: squarefreeness, sign change on
   an interval shorter than the discriminant separation bound, gcd test for
   zero, resultant lower bound and bisection for the sign. Irreducibility is
   not trusted.
8. **Certificate lower example.** The chain example in J.8 is argued to need
   k exposing records for any certificate in the stated format (only the
   last unfixed row can carry weight), slightly stronger than "the scheme
   uses k records".
9. **Feasible parallel (`cor:qc-feasible-output`).** Restricted to odd prime
   d, which suffices for the output bound. The joint degree uses a Kummer
   and norm argument over Q(ζ_d) (`lem:qc-kummer`) rather than the source's
   unramified-compositum argument for general odd d. The block construction
   is the source's explicit binomial construction (projection onto 𝓛, grid
   approximation, triangle of size ε_0=1/(100a^5d^2), weights >1/4, margin
   1/(2a^4d^2)), built on the pencil of `thm:qc-corank-one`. Mixing uses
   ε'=1/(8k) with weights τ_i−1/11>1/8. The dense minimal polynomial uses
   R_0=1+Σϖ_b (no existential translation). Span exactly 3k is proved.
10. **Q4.** The Galois/norm argument is now `lem:qc-kummer` with d=3.
11. **Q3 weights.** Main statements use the existential weight;
    `lem:qc-weight` gives the explicit weight in general form, with the
    Sylvester bound sketched for the blocks (H = O(ℓ_k² log ℓ_k + kℓ_k log
    ℓ_k)); that resultant estimate is the least detailed computation in J
    and could be expanded if a reviewer asks.
12. **K root penalty.** Scope corrected as required; the sparse high-degree
    objective is presented as outside the theorem's input model.

## Responses to the prewrite audits

`prewrite-quadratic-contrast.md`: the malformed −½ in the source formula is
typeset correctly; native PSD versus squared SOC rows, Hessian span versus
row count and polynomial span, B(n,k) with the maximum and the n=k=3
example, the canonical optimizer in original coordinates, the
cancellation-before-gcd condition (with the ball example), the face
restriction before reading a zero margin (with the x≥1 example), joint
versus coordinatewise output, existence-only translations, and the
"no decision or approximation lower bound" scope are all in the text. The
external contracts listed at the end of that audit are items 1–11 above. The
audit's suggestion to define k=h is followed (k is the Hessian span here).

`prewrite-boundaries.md`: Proposition 1, Examples 2–4, Propositions 5–7, the
common-kernel repair, and the penalty limits are included with the stated
scopes. The all-PSD Gram frontier and the item-9 core-value paragraph belong
to heights and recourse and are not reproduced. The nullvector example is
presented as a mathematical safeguard without any claim about the wording of
an external book.

Framing helper comments (J lines 129–132 and 1665 in the earlier draft): the
degree paragraph now separates the degree of one scalar (dense minimal
polynomial of that scalar) from the joint field degree (common-field
representation, not coordinatewise output), and both places now say that a
rational circuit computes only rational numbers, so the compact formats for
irrational coordinates are implicit systems, radical towers or root-selection
circuits.

## Coordination items for the root

1. **Duplicate G6.** `rem:heights-nullvector` in Section 07 contains the same
   counterexample and maximum-rank fact as `prop:bnd-nullvector` and
   `lem:bnd-common-kernel`. DECISIONS D10 assigns this boundary to K.
   Suggest shortening the heights remark to cite K, or deleting K.2 and
   citing the heights remark from K; one copy should remain.
2. **Imported-results table** (`tab:models-imported`, Section 01): its App. J
   row says "Exact algorithms and degree bounds ... with few constraint
   Hessians", which J now proves. Suggested replacement row for J: isolated
   root count (Morgan–Sommese), generic QCQP degree (Nie–Ranestad), Hilbert
   irreducibility, certified recognition (KLL), exact rational QP and LP,
   convex QCQP attainment (Luo–Zhang), Eisenstein/Hensel, primes in
   progressions. For K: effective Łojasiewicz inequality and one-block QE
   with coefficient bounds (Basu–Mohammad-Nezhad), Brouwer degree.
3. `final-coverage.md` line numbers for J changed after the corollary and
   review edits; labels are unchanged except the new
   `lem:qc-kummer`, `prop:qc-binomial-block`, `cor:qc-feasible-output`.
4. The Discussion may list as open: exact comparison for partially
   degenerate convex quartics (K.1), and running time φ(k)L^{O(1)} for
   fixed-span feasibility (not claimed in `prop:qc-decision`).

## Checks run

- Targeted LaTeX compile of a temporary wrapper (`/tmp/qc-check/wrapper.tex`)
  containing `macros.tex`, Appendix J and Appendix K with the main preamble:
  `pdflatex -interaction=nonstopmode -halt-on-error wrapper.tex`, run
  repeatedly during writing; final run exit 0, no LaTeX errors, about 40
  pages, one 0.24pt overfull line. Unresolved references in that wrapper are
  only the external labels listed above; citations are unresolved there by
  design.
- `python3 verification/check_manuscript.py` (scoped to this manuscript, run
  on the integrated drafts): final run 94 errors, all "Missing bibliography
  key" (pending `literature.bib`); no undefined references, unfinished-text
  markers, or repository paths were reported for any file. These appendices
  cite 36 keys; 4 are in `references.bib` and 32 are among the missing keys
  listed above.
- Targeted grep of both appendices for TODO/FIXME/placeholder phrases,
  "companion proof", "independently reviewed", repository paths: none.
- No experiments, mathematical scripts, project-wide checks, or CI
  inspection were run. All verification of the mathematics is by the proofs
  written in the appendices; recorded diagnostics from the source notes were
  not rerun or relied on.
