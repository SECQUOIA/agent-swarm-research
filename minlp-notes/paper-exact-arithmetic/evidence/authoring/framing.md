# Framing author report: abstract, Sections 00, 01, 11

Owner: framing writer (Opus). Owned files: `sections/abstract.tex`,
`sections/00-introduction.tex`, `sections/01-models.tex`,
`sections/11-discussion.tex`, and this report. No other file was edited.

Status: round-1 draft. It is reconciled against all chapter and appendix
drafts present on 2026-10-05 (Sections 02–10, Appendices A–K) and against the
vetted `evidence/literature-review.md`. The vetted `evidence/literature.bib`
had not appeared at the last update. Final readiness is not claimed. A final
revision round must integrate the vetted bibliography keys and the
chapters' final theorem statements, including the repairs root is making
after the independent reviews.

## 1. Title recommendation

**Exact Arithmetic in Convex Polynomial Optimization: Values, Optimizers, and
Certificates.**

The current title omits "Convex". Every upper bound and every hard class in the
paper concerns convex objectives (global, domain, residual, or strong
convexity). Without the word the title suggests a classification of
polynomial optimization in general, which the paper does not give.

## 2. Organizing arc

Section 00 states one thesis without slogans: each output (value, point,
exact decision, exact description) needs an ingredient that the previous
output does not supply.

1. Value to point: an effective growth modulus with a polynomially encoded
   constant, plus a selection rule. Available under global convexity at every
   degree and under domain convexity for cubics; unavailable for box-convex
   quartics unless Square Root Sum or PosSLP is easy. With a nonconvex core,
   one random core tilt restores full points for residual-convex cubics on
   product boxes.
2. Point to exact decision: a separation bound and a compact way to reach the
   precision it demands. For explicit strongly convex objectives the
   remaining difficulty is PosSLP (one instance for every predicate; order
   predicates hard for certified quartics). Constraints add active-face search;
   integers add discrete search needing only ordinary precision.
3. Exact description: separate degree, height, and field arguments; size
   depends on format. Compact descriptions are claimed only where proved: for
   the exhibited families, and for the general circuit witness and circuit
   Gram theorems.

## 3. Labels

### Defined by the framing files

Sections: `sec:intro`, `sec:intro-points`, `sec:intro-exact`,
`sec:intro-constraints`, `sec:intro-optimizers`, `sec:intro-certificates`,
`sec:intro-summary`, `sec:intro-prior`, `sec:intro-scope`,
`sec:intro-organization`, `sec:models`, `sec:models-notation`,
`sec:models-input`, `sec:models-promises`, `sec:models-outputs`,
`sec:models-computation`, `sec:models-certificates`, `sec:models-size`,
`sec:models-imported`, `sec:discussion`, `sec:discussion-summary`,
`sec:discussion-consequences`, `sec:discussion-open`.

Tables and equations: `tab:intro-results`, `tab:models-imported`,
`eq:intro-error-bound`.

Definitions: `def:models-rational`, `def:models-polynomial`,
`def:models-polyhedra`, `def:models-length`, `def:models-hessian-gram`,
`def:models-value`, `def:models-points`, `def:models-predicates`,
`def:models-representations`, `def:models-circuits`, `def:models-posslp`,
`def:models-sos`, `def:models-formats`.

Lemmas, each with a short proof in Section 01:
- `lem:models-det-trace`: `A ≻ 0` gives `A ⪰ det A/(tr A)^{m-1} I`, a rational
  bound of polynomial bit length. Cited by 03, 04, 07, A, F.
- `lem:models-gram-curvature`, with the alias `lem:models-hessian-gram` on
  the same lemma because 04, 07, and F cite the first name and 07 cites the
  second. Content: curvature from a Hessian Gram; congruence under invertible
  rational affine maps with `S=[[T,0],[c⊗T,T⊗T]]`; positive definite quartic
  form. Root may keep one name and rewrite the other references.
- `lem:models-strong-convexity`: attainment, gap-to-distance, distance from a
  gradient, constrained and unconstrained. Cited by D.
- `lem:models-low-degree`: (a) a globally convex polynomial of degree at most
  three is quadratic; (b) a globally monotone polynomial map of degree at most
  two is affine, with a rational zero when strongly monotone. Part (b) was
  added because Section 03 cites the lemma for monotone quadratic maps.
- `lem:models-rational-squares`: positive rationals as sums of O(bit length)
  rational squares by binary expansion; rational PSD Gram to rational SOS in
  polynomial time. Cited by 04, 07, 08, F.

Remarks: `rem:models-encodings`, `rem:models-gram-kinds`, `rem:models-socp`
(exact SOCP feasibility is PosSLP-hard by the Tarasov–Vyalyi gates and
standard conic duality, with a short proof; cited in the introduction's
comparison with exact conic optimization).

### Referenced labels from other files

Shared (CONVENTIONS), all now defined: `thm:exact-upper`,
`thm:quartic-complete`, `thm:global-point`, `thm:cubic-point`,
`lem:quartic-realization`, `thm:quadratic-graph`, `thm:singleton-field`,
`thm:sos-length`, `thm:rational-height`, `thm:circuit-gram`.

Other theorem labels used: `thm:posslp-closure`, `prop:upper-slack-gap`,
`lem:denominator-clearing` (all Section 03).

Sections and appendices, all defined except one: `sec:points`, `sec:upper`,
`sec:reductions`, `sec:constraints`, `sec:algebraic`, `sec:heights`,
`sec:fields`, `sec:fields-certificates` (Section 09), `sec:recourse`,
`app:points`, `app:upper`, `app:reductions`, `app:constraints`,
`app:algebraic`, `app:heights`, `app:fields`, `app:fields-certificates`
(Appendix H), `app:recourse`, `app:qc` (Appendix J), and `app:boundaries`
(Appendix K). All resolve in the full build.

## 4. Notation: choice for Section 01 and global mapping for root

Section 01 now uses the names that most chapters use:

| Object | Section 01 symbol | Meaning |
| --- | --- | --- |
| Hessian basis | `w(x,v)=(v, x⊗v)` | Coordinates `x_i v_j` ordered by `(i,j)`; general degree uses a monomial vector linear in `v` containing all `v_i` |
| Monomial vector | `z(x)` | All monomials of degree at most two, constant first |
| Its length | no symbol; written `binom(n+2,2)` | `D` is reserved for the numerical degree (Sections 01–03, A, C) |
| Degree | `D=max{2,deg f}` | Numerical degree |
| Gram margin | `ρ(A)=det A/(tr A)^{m-1}` | Lemma `lem:models-det-trace` |
| Curvature | `μ` lower, `Λ` upper | As in DECISIONS |

Exact usage found in the drafts (counts of occurrences when last surveyed):

| File | Hessian basis | Monomial vector | Length of monomial vector | Variables |
| --- | --- | --- | --- | --- |
| 01 | `w(x,v)` | `z(x)` | unnamed | `x` |
| 03 | `w(X,v)`, also `(v,X⊗v)` | — | — | `X` |
| 04 | `(v,x⊗v)` unnamed | `m(x)` | — | `x` |
| 05, D | `(v,x⊗v)` unnamed | `z_2` (D) | — | `x` |
| 06, E | `w(x,v)` | — | — | `x` |
| 07, F | `w(X,v)`, also `(v,X⊗v)` | `z(X)` | `D=binom(n+2,2)` | `X` |
| 08, G | `w(X,v)` | `z(X)` | (inherits 07) | `X` |
| 09 | — | `z(x)` | — | `x` |
| A | `w(X,v)` | `m(x)` | — | `X` |
| H | `w(X,v)` | — | — | `X` |
| J | — | `m(x)` | — | `x` |

Recommended global mapping: Hessian basis `w(·,v)` everywhere (rename the
unnamed `(v,x⊗v)` only where a name is used repeatedly); monomial vector
`z(·)` everywhere (rename `m(x)` in 04, A, J and `z_2` in D); length of the
monomial vector `N` (rename `D` in 07 and F, since `D` is the degree in 01–03,
A, and C; 07 and F never use the degree symbol, so keeping `D` with its local
definition is the minimal alternative). Variables: Section 01 writes `x`;
03, 07, 08, A, F, G, H write `X` for indeterminates. Either convention works
if stated once; Section 01 does not force a choice.

## 5. Citation keys

### Existing keys in `references.bib` used by the framing

`KozlovTarasovKhachiyan1980`, `SlotSteurerWiedmer2025`, `AllenderEtAl2009`,
`TarasovVyalyi2008`, `EtessamiStewartYannakakis2012`, `BuergisserJindal2024`,
`EY2010`, `Li2010`, `Li2013`, `Yang2009`, `AhmadiChaudhryZhang2024`,
`AhmadiHall2020`, `GroetschelLovaszSchrijver1988`, `LeeSunSaunders2014`,
`PangHan2023`, `Vegh2016`, `Carlini2006`, `NieRanestad2009`,
`MittalSchulz2013`, `KannanRademacher2009`, `LenstraLenstraLovasz1982`,
`Basu2014`.

### Keys not yet in `references.bib`

Aligned with the keys other chapters already use where the same work is
cited. Luna's final `literature.bib` keys will replace these if they differ.

| Key | Source as identified in Luna's review or existing audits | Claim made in framing | Also cited by |
| --- | --- | --- | --- |
| `Scheiderer2016` | Scheiderer, Sums of squares of polynomials with rational coefficients, JEMS 18 (2016) | Real-but-not-rational SOS forms; excluded fields; nonnegative ternary quartics that are not rational SOS | 06, 08, E |
| `Hillar2009` | Hillar, Sums of squares over totally real fields are rational sums of squares, Proc. AMS 137 (2009), Thms. 1.2/1.4 | Descent from totally real fields (does not apply to the paper's fields) | 08 |
| `Laplagne2023` | Laplagne, arXiv:2312.16801, Sec. 3.1 | Quartic forms SOS over a cubic field but not over Q, including strictly positive ones; displayed examples are not convex | 08 |
| `ChuaPlaumannSinnVinzant2017` | Gram spectrahedra (Contemp. Math. 697; arXiv:1608.00234) | Rational PSD Gram equivalent to rational SOS; fails over general ordered fields | 07 (08 uses `...2016`) |
| `PeyrlParrilo2008` | Peyrl, Parrilo, TCS 409 (2008) | Rounding interior numerical Grams to rational certificates | 07, 08 |
| `SafeyElDinZhi2010` | Safey El Din, Zhi, SIAM J. Optim. 20 (2010) | Rational SOS algorithms with bit bounds when a rational SOS exists | 07 |
| `MagronSafeyElDin2021` | Magron, Safey El Din (2021), per Luna's review | Exact certificates in the strict SOS-cone interior | — |
| `DavisPapp2022` | Davis, Papp, rational dual certificates (per Luna's review) | Recovery needs a supplied positive margin | 08 |
| `GaertnerMagronVallentin2026` | Gärtner, Magron, Vallentin, arXiv:2606.25118 (per Luna) | Exact Gram recovery given a supplied eigenvalue margin | 07 |
| `RaghavendraWeitz2017` | Raghavendra, Weitz, bit complexity of SOS proofs (per Luna) | Lower bounds for constrained SOS proof systems | 07 |
| `HeltonNie2010` | Helton, Nie, Math. Program. 122 (2010), Lemma 8 | SOS-convex stationary zero gives real SOS | 07 |
| `AhmadiParrilo2013` | Ahmadi, Parrilo, SIAM J. Optim. 23 (2013), Thm. 3.1 proof | Taylor SOS principle | 08 |
| `Lasserre2009` | Lasserre, Convexity in semi-algebraic geometry and polynomial optimization, SIAM J. Optim. 19 (2009) — the key Section 07 uses | SOS-convex Taylor/exactness credit | 07 |
| `Ngai2015` | Ngai, Global error bounds for systems of convex polynomials over polyhedral constraints (Luna's KB entry `ngai2015-global-error-bounds-for-systems`, Theorems 8–11) | Error bounds over polyhedra, function-dependent constants | — |
| `BienstockDelPiaHildebrand2023` | Bienstock, Del Pia, Hildebrand, Complexity, exactness, and rationality in polynomial optimization, Example 1 (September audit only; not in Luna's review) | Cubic with irrational singleton sublevel in a rectangle; convexity on the rectangle is an audit inference | — |
| `AhmadiOlshevskyParriloTsitsiklis2013` | NP-hardness of deciding convexity of quartics (Luna cites "Ahmadi et al. 2013") | Convexity recognition NP-hard | — |
| `NieRanestadSturmfels2010` | Algebraic degree of SDP, Math. Program. 122 (2010) (September audit only) | Generic SDP degree | — |
| `Balaji2016` | Balaji, CMI thesis (2016), §3.5.1, Lemma 3.30; only indexed excerpts were read by Luna | Model of circuits with internal sign gates analyzed by counting-hierarchy arguments | — |
| `KojimaKimWaki2005` | Kojima, Kim, Waki, Math. Program. 103 (2005) | Real SOS respecting a block separation | 09 |
| `GaertnerMatousekRuestSkovron2008` | Violator spaces, Discrete Appl. Math. 156 (2008) | Violator-space sampling | 05, D |
| `HildebrandKoeppe2013` | Hildebrand, Köppe, Discrete Optim. 10 (2013) | Fixed-dimension convex integer minimization | D |

Removed from the framing after Luna's review or root's notes: `ODonnell2017`
(not vetted; replaced by the margin-dependent rational-SOS algorithms),
`Lasserre2008` (replaced by `Lasserre2009` per root), and the 2024 date for
Laplagne (aligned with 08's `Laplagne2023`).

### Claims that depend on vetted source contracts

1. `SlotSteurerWiedmer2025`: Theorem 1.1 (attainment within a ball whose
   radius has polynomial bit length, not optimizer bit length), Corollary 1.2
   (value approximation), Table 1 open entries, Lemma C.3 (univariate quartic),
   Appendix C (irrational convex singleton), all as arXiv v1 statements. The
   STOC 2026 text is unverified (Luna). The intro's description of Appendix C
   ("irrational singletons defined by convex polynomials were also known
   before, for example [SSW, App. C]") must be checked against v1: earlier
   audits describe a sextic zero sublevel without rational points, while
   Luna's table mentions a "univariate convex cubic singleton" at
   pp. 30–31.
2. `Yang2009`: only "studies global error bounds for convex polynomials" is
   attributed; the framing says the exponent form is not claimed as new and
   makes no comparison of constants with Yang (Luna: unread).
3. `AllenderEtAl2009`: counting hierarchy; P^PosSLP and constant-free real
   computation; Square Root Sum in P^PosSLP; Newton circuits; division
   elimination; and, in Section 11 open question 2, that zero testing of
   integer circuits lies in coRP. The last attribution is not in Luna's
   review and must be checked; if unsupported, delete that sentence.
4. `TarasovVyalyi2008`: basis equivalence (Theorem 3) and 2×2 gate
   constructions used in `rem:models-socp`.
5. `EtessamiStewartYannakakis2012`, Appendix C, Corollary C.8 (arXiv v2).
6. `BuergisserJindal2024`: cited for the open status of PosSLP hardness and
   for the oracle characterization (Proposition 1.1), as in Luna's review.
7. `GroetschelLovaszSchrijver1988`: ellipsoid weak optimization, rounded
   central-cut method, and linear programming with an operation count
   independent of the objective encoding, as listed in
   `tab:models-imported`.
8. `EY2010`: residual versus solution approximation and its hardness for
   equilibria, as Section 02 attributes it.
9. The adaptive compiler: per Luna, no inspected source states the explicit
   O(S²) compiler, and priority is unestablished. The introduction now
   describes the construction precisely, lists the nearby oracle/Turing,
   specific many-one, and internal-sign-gate work, and states that no
   priority is claimed.

## 6. Exact contribution scope stated in the framing

Each statement was checked against the prewrite audits and the chapter
drafts. If a chapter's final theorem changes, the abstract, Table
`tab:intro-results`, and Section 11 must change with it.

- Global point (`thm:global-point`): explicit sparse, globally convex
  (promise), numerical degree D, arbitrary rational polyhedron; decides
  emptiness and unboundedness; R, Γ of poly(L,D) bits; dist ≤ Γ gap^{1/D} for
  gap ≤ 1; fixed minimum-norm selector in poly(L,D,q). Exponent not claimed
  new; attainment and radius credited to SSW v1 Theorem 1.1.
- Domain cubic (`thm:cubic-point`): convex on a bounded rational polytope;
  exponent 1/4; poly(L+q); 1/3 an upper limit only.
- Point boundaries (Section 02): accuracy-1/4 point of a box-convex quartic
  with unique minimizer decides Square Root Sum (treewidth two, bounded
  coefficients) or PosSLP; exact active bound of a strongly convex cubic is
  Square Root Sum-hard; selector versus some-optimizer; unconditional
  exponential-bit error constants and regularization parameters for an easy
  box-convex quartic family; conditioned-path minimal polynomials with
  2^{n-2}+1 terms; rectangle certificates with long endpoints.
- Recourse (Section 10, D1): residual-convex cubic on a product box, one
  finite core-tilt law, every draw correct, expected
  k^{O(k)}(1+Λ/σ)^k poly(L+q); values and selected core for every fixed
  degree; supplied convexifier on coupled polytopes; jointly convex case
  without numerical factor; residual quartics excluded conditionally.
- Upper (Section 03): explicit f, h of unary degree with supplied μ or a
  checked Hessian certificate; one PosSLP instance for each of the six
  relations <, ≤, =, ≠, ≥, >, no gap promise; strongly monotone polynomial
  maps of unary degree (completeness only for certified cubic maps);
  supplied slack gap (`prop:upper-slack-gap`); compilation theorem; the
  structured box/flow single-instance corollary, with multi-bit outputs as
  nonadaptive lists.
- Lower (Section 04): certified quartics; eight order tests complete;
  nonnegativity, real SOS, PD polynomial Gram existence complete; rational
  SOS hard; equality upper bound only; hard instances with nonzero minimum;
  rational minimizer in [-1,1]^n with known minimum zero (promise).
- Constraints (Section 05): UP^PosSLP ∩ coUP^PosSLP; nonlinear dimension
  F(k)L^C; structured boxes/flows; Las Vegas (r+1)^{O(r)}L^C; integer lists
  2^{O(t log(t+1))}L^C (unrestricted fibers) and a(t)L^C (mixed); F(k+t)L^C;
  Las Vegas F(t,r)L^C; binary decision with known optimum hard.
- Singletons and degree (Section 06): bivariate quartic with
  ∇²F ⪰ 4096 I by a rational certificate (4124 analytically); one-real-
  conjugate characterization including unique minimizers and single real
  zeros; (d+1)/2 power coordinates; cyclic degree d_n with O(log n)-bit data,
  n+1 integer squares, O(n²) local condition number, d_n+1 nonzero
  coefficients after translation; bounds 2^n−1, 2^n−3, 2^n−5, maxima
  3, 5, 11, 21 (D2); 2·3^{n−1}−1 without rational SOS (Section 11 only);
  SOS length n+1 over R; univariate degree 2^{Ω(b)}.
- Heights (Section 07): circle family f_k with last coordinates of reduced
  denominator exactly 5^{2^k}; rescaled variant with denominators divisible
  by 5^{2^k} and polynomial local condition number (two families, not one);
  witnesses Ω(n2^{n/2}); interior Grams poly(L)2^{O(n)} versus Ω(n2^{n/2});
  circuit Gram; unique moment optimum and least fields of maximal-rank and
  exposing matrices; long entries for the circle family.
- Fields and formats (Sections 08, 09): prime least fields in (ℓ+1)/2
  variables (ternary at ℓ=5); tower Q(2^{1/5^k}) and individual coefficient
  degree; root-circuit and auxiliary-variable certificates for the tower;
  recognition at the tower point; descent criterion with its baseline
  hypothesis; quadratic common denominators for the tower after a scale
  increase (degree two minimal); radial order Ω(log L/log log L) with an
  adapted O(L) certificate; block-separated certificates absent, with field
  Q(2^{1/5^k}), or of Ω(k2^k) bits; quadratic graph lift.

## 7. Corrections applied at root's request

1. Height attribution: exact last denominator 5^{2^k} for the circle family;
   divisibility by 5^{2^k} and polynomial local conditioning for the
   rescaled variant, stated as two families (intro text and table).
2. Slack-gap result pointed to `prop:upper-slack-gap` in Section 03 (bullet
   and a separate table row).
3. Monotone upper bound stated for polynomial maps of unary degree, with
   completeness only for certified cubic maps (text, table, prior work).
4. `Lasserre2009` instead of `Lasserre2008`.
5. Notation in Section 01 unified as in Section 4 above; mapping reported.
6. Compiler paragraph rewritten: exact construction (threshold gates,
   scaled compressor maps, inverse Newton refinement, integer separation,
   one error budget, positive denominators, padded interpreter, O(S²) size),
   its limits, and nearby work; no priority claim.
7. Hesse attainment: "attains its minimum within a ball whose radius has
   polynomial bit length" with `[Theorem 1.1]`, value approximation with
   `[Corollary 1.2]`, and an explicit note that the radius bounds the norm,
   not the coordinates' bit length (intro paragraph and prior work).
8. Compact-description claims restricted: the abstract now says only that
   the exhibited families have polynomial-size compact descriptions; Section
   11 names the specific compact format per family; rational circuits are
   claimed only for rational objects (long rational minimizers, the strict
   circuit witness of `prop:upper-circuit-witness`, the circuit Gram of
   `thm:circuit-gram`); the general "report by a compact circuit" advice was
   removed; tower compact formats are labeled as family-specific.
9. Relations: the introduction now lists all six relations and says the
   shifted comparisons handle six.
10. Abstract: the global-point sentence now states time polynomial in the
    input length, the degree, and the number of requested bits.
11. Conditioned-path formats (Section 02): the introduction now states a path
    interaction graph for the coordinate minimal polynomial and the
    enclosing-box certificate, and treewidth two for boxes certifying the
    sign of an active multiplier.
12. Input-length claims: the framing states no tight input-length bound for
    any family (no `L=O(n log n)`, `O(n² log n)`, or `2^{Ω(L)}`); size lower
    bounds are described only as exponential in the dimension and
    superpolynomial in the input length. The tight length claims flagged in
    Sections 02 and 06 are in those chapters, not in the framing.
13. Summary table: each row now cites the specific theorem (for example
    `thm:points-quartic-lower`, `thm:rational-optimizer`,
    `thm:constraints-unambiguous`, `cor:structured-single-sign`,
    `thm:heights-witness`, `thm:fields-prime`, `cor:fields-tower-denominator`),
    and the columns are ragged-right with a full-width caption.
14. Degree qualifiers: Section 11's statements that value enclosures and a
    fixed approximate optimizer cost polynomial time now say "of fixed or
    unary degree"; the abstract says "of unary degree" for known value
    approximation and states the point bound in L, the degree, and q.
15. Order versus equality: the table row for monotone maps says "order tests
    complete for certified cubic maps"; the introduction says "coordinate
    order comparisons" and Section 11 "coordinate order predicates"; the
    abstract says the order tests are complete, also for coordinates of a
    rational minimizer, and that equality has only the upper bound.
16. Abstract length: 300 words (each math expression counted as one word).
17. Variable fixing: the introduction now says that activity at the
    relaxation optimizer informs the choice of branching variables, not that
    it decides fixing. Section 11's paragraph is now "Points and active
    sets": it states exact active-set recovery for the relaxation optimizer
    (Square Root Sum-hard in general; recovered by ordinary approximation
    under a supplied slack gap; no guarantee otherwise) and says that using
    the active set to fix variables of the original mixed-integer problem
    needs an additional optimization argument that the paper does not give.
18. Uniqueness and degrees in Section 01: the selected optimizer is unique
    "when f is strictly convex on a convex feasible set", with mixed-integer
    problems named as a case with several optimal points; the introduction
    says "strongly convex and the feasible set is convex". The joint-degree
    sentence now states the one-directional relation
    `[Q(p_j):Q] ≤ [Q(p):Q]`: a coordinate lower bound bounds the joint
    degree, but not conversely. No formal theorem statement changed.

## 8. Readiness concerns and unresolved editorial dependencies

1. **Appendix K** now exists under `app:boundaries`; Section 11's open
   question 3 and `tab:models-imported` match its degenerate-quartic examples
   and its effective Łojasiewicz-type penalty tool.
2. **Bibliography pending.** Twenty-one keys used by the framing are not in
   `references.bib`; the checker reports them until Luna's `literature.bib`
   is merged.
3. **Cross-file label state.** At the last survey no label was defined twice,
   and the earlier conflicts (`cor:structured-single-sign` in 03 and 05,
   `thm:fields-ternary` cited by 04, `lem:models-division` cited by B and D)
   no longer appear, and the supplied-slack-gap result now has the single
   label `prop:upper-slack-gap` (03), which the framing cites. Remaining items
   for root: `ChuaPlaumannSinnVinzant2016` (08) and `...2017` (07, framing)
   are one paper; undefined references outside the framing files were
   `app:recourse-cubic-proof` (10) and `prop:qc-pell` (J).
4. **Recourse (D1).** The framing states the full expected-work theorem.
   It depends on Appendix I, which is still being written, and on
   `prewrite-core-noise-chain.md` (no analytic obstruction found). If
   Appendix I ends conditional, the abstract, the recourse paragraph, the
   table row, and Section 11 must be weakened.
5. **Five-variable maximum 21 (D2).** Stated as proved. If source-contract
   vetting fails, replace "exact maxima for n ≤ 5" by "n ≤ 4" in Sections
   00 and 11 and in the table, and add n = 5 to the open questions.
6. **Numbers to re-verify against final chapters.** Accuracy 1/4; 4096 I;
   (d+1)/2; O(n²) monomials, O(log n)-bit coefficients, n+1 integer squares,
   O(n²) condition number; 5^{2^k} in 2(k+1) variables; Ω(n2^{n/2});
   poly(L)2^{O(n)}; (ℓ+1)/2 variables; 3k variables; Ω(log L/log log L);
   O(L); Ω(k2^k); k^{O(k)}(1+Λ/σ)^k; known optimum 1/4; 2^{n−2}+1 terms.
7. **Toolkit deduplication.** Several chapters reprove facts that Section 01
   states once (determinant–trace margin, Hessian Gram congruence, strong
   convexity radius, rational squares, circuit conventions in Section 03).
8. **`rem:models-socp`** is prior-work context with a short proof; it can
   move to Appendix J or be replaced by a vetted citation.
9. **`tab:models-imported`** must be reconciled with the final imports (for
   example the integer-query feasibility sources, root isolation, open
   semialgebraic sampling, and the effective Łojasiewicz inequality for K).
10. **Length.** In a full temporary build with root's table of contents,
    the introduction occupies pp. 7–17, Section 01 pp. 18–24, and Section 11
    about 3.5 pages. The architecture budget was about 6 pages for the
    introduction. If root wants it shorter, the cleanest cuts are (a) the
    "Constraints and integer variables" prior-work paragraph, whose credits the
    chapters repeat, and (b) the per-family detail in Sections 1.4–1.5, which
    the summary table repeats; together about 2 pages.

## 9. Suggestions for `main.tex` (not edited)

- Title as in Section 1 (root has not changed it yet).
- The table of contents suggested earlier is now in `main.tex`.
- D7: the organization paragraph matches the current order; the appendix
  sentence uses labels and is order-independent.
- Consider reordering the appendix `\input` lines so that Appendix C
  (points) precedes A (upper), matching the section order.

## 10. Checks performed for the framing files

All checks were targeted; none is a mathematical verification, and no CI
result is claimed.

1. Standalone compilation of only the four owned files in a temporary
   directory outside the repository (`/tmp/framing-check/wrapper.tex`, using
   the `main.tex` preamble and `macros.tex`): `pdflatex
   -interaction=nonstopmode -halt-on-error wrapper.tex`, `bibtex wrapper`,
   then two more `pdflatex` runs. Last outcome: exit status 0, no LaTeX
   errors, no overfull boxes.
2. Full-manuscript compilation in a temporary copy (`/tmp/fullbuild`, a copy
   of `main.tex`, `macros.tex`, `references.bib`, `sections/`,
   `appendices/`; no repository file was written): `pdflatex`, `bibtex`,
   `pdflatex`, `pdflatex`, all with `-interaction=nonstopmode`. Last outcome
   after Appendix K appeared: no LaTeX errors, 0 undefined references,
   286 pages; undefined citations remain for keys not yet in
   `references.bib`. Overfull boxes in that build occur only in Appendices
   D, E, G, H, J, and K, none in the framing files. Pages 13–14 (summary
   table) were rendered with `pdftoppm` and inspected.
3. `python3 verification/check_manuscript.py` (the manuscript's scoped
   checker). Last outcome: 26 source files, 606 labels, 1602 references;
   no unfinished-text, repository-path, duplicate-label, or undefined-
   reference finding anywhere; all 84 remaining findings are missing
   bibliography keys awaiting the vetted `literature.bib`.
4. A scoped `grep` for process language and banned phrasing (audit, review,
   repository, draft, novel, first, crucial, and similar) in the four owned
   files: no matches. A scoped `grep` for tight input-length claims in the
   owned files: none. An inline Python check of the four owned files and this
   report: final newline present, no trailing whitespace.

No experiment, mathematical script, project-wide check, or CI inspection was
run.
