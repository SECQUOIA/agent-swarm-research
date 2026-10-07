# Manuscript architecture

Date: 2026-10-05. This is design guidance for the framing/editor
assignment and the eight running topic authors. It maps the source program
onto the existing allocation in `main.tex` and `CONVENTIONS.md`. It does
not reassign files, edit shared macros, or replace the root's decisions.
Coverage identifiers (A1, P2, ...) refer to `evidence/coverage-map.md`.
Audit findings cited as "prewrite" refer to `evidence/reviews/prewrite-*.md`.
No literature search, novelty judgment, or computation was performed here.
Attribution placeholders are for the literature lead.

## 1. Organizing thesis

The paper has one claim that every section serves: **in polynomial
optimization the required output is part of the problem.** Four outputs
form a ladder, and each step needs an ingredient that the previous output
does not supply.

| Output | Contract | Ingredient needed to reach it from the level above |
| --- | --- | --- |
| V. Value | Feasible rational point and certified interval of width 2^-q for the optimal value | Convex value optimization (established; credited) |
| P. Point | (P1) feasible point within 2^-q of the optimizer set; (P2) fixed selector: the same optimizer p approximated at every q | An effective distance-to-optimum modulus with polynomial-bit constant, plus a selection rule |
| E. Exact comparison | Sign or equality of an explicit observable at the optimizer, including zero | A separation bound for nonzero values, plus a succinct way to reach the doubly exponential precision it demands |
| R. Exact representation | Implicit system or shared circuit; algebraic (primitive element, minimal polynomials, dense or sparse); expanded rational; exact certificates over a coefficient field | Separate size and field arguments; none follows from E |

The main messages, each anchored to a theorem, are:

1. **Values do not give points, and the boundary is sharp in degree and
   convexity type.** Global convexity gives an effective modulus with
   exponent 1/D and a fixed minimum-norm selector in poly(L,D,q)
   (`thm:global-point`). Convexity only on a polytope still suffices for
   cubics, with exponent 1/4 (`thm:cubic-point`). For quartics convex only
   on a box, one constant-accuracy point decides Square Root Sum or PosSLP
   (`thm:points-quartic-lower`). Even for cubics, the exact active label is
   Square Root Sum-hard while points are easy.
2. **Points do not give exact comparisons; PosSLP is exactly the missing
   arithmetic.** For explicitly given polynomials with supplied global
   strong convexity, every order or equality test at the optimizer is one
   PosSLP instance (`thm:exact-upper`). With a checked positive definite
   Hessian Gram the order tests are PosSLP-complete (`thm:quartic-complete`),
   even when the optimizer is rational, bounded, and of known value zero
   (`thm:rational-optimizer`).
3. **Constraints and integers separate search from arithmetic.** General
   polyhedra give UP^PosSLP ∩ coUP^PosSLP through a unique active-set
   certificate; structure gives P^PosSLP, ordinary FPT in nonlinear
   dimension, or Las Vegas FPT in constraint rank. Integer search runs with
   ordinary polynomial precision; only a final list of continuous fiber
   minima needs exact comparison.
4. **Exact optimizers can be large in every expanded format, independently
   of comparison hardness.** A coordinate of a strongly convex rational
   quartic singleton can be exactly the algebraic numbers with one real
   conjugate (`thm:singleton-field`); degree can be exponential in the
   number of variables with small coefficients; a rational optimizer can
   need exponentially many denominator bits (`thm:rational-height`).
5. **Exact certificates have their own arithmetic.** A strict rational
   convexity certificate does not give a rational SOS certificate of the
   optimum; the least coefficient field can be Q(2^(1/5^k)); rational
   certificates can be forced long by imposed block sparsity or prescribed
   radial multipliers while adaptive or joint certificates stay short.
6. **Compact representations often survive.** Shared circuits give short
   interior Grams (`thm:circuit-gram`), short strict witnesses, and short
   SOS coefficients; auxiliary root variables give short rational
   certificates. Lower bounds are therefore stated per format.
7. **A nonconvex core changes the point problem.** For residual-convex
   cubics on product boxes, exact face and minor-margin certificates turn
   approximate core access into full selected-point output (Section 10;
   scope depends on decision D1).

Every contribution statement in the abstract, introduction, and theorem
preambles must give: the input class and encoding; promise versus checked
certificate; the computation model; the output contract; and which
ingredients are credited as established. Recommended credit categories
(to be confirmed by the literature lead): convex value optimization and
radius bounds; Newton-circuit, algebraic-separation and division-elimination
architecture; arithmetic-circuit hardness of exact SDP; Taylor SOS and
exact moment relaxations for SOS-convex problems; violator spaces;
integer-query convex feasibility; essential-variable extraction; proximal
Newton convergence; structured QP and flow algorithms; real failures of
rational SOS descent; rational-function SOS existence; real block SOS;
rank-versus-height phenomena in SDP.

## 2. Section plan mapped to the existing files

Budgets are pages at the current 11pt, 1-inch layout. Labels follow
`CONVENTIONS.md`: shared labels are kept; others carry the topic prefix.
"Main" lists statements whose proofs belong in the appendix unless shorter
than about one page.

### 00 Introduction and abstract (framing/editor; currently unassigned)

- Motivation from MINLP: node bounds need values, branching and fixing
  need points or exact signs, certification needs exact formats.
- The ladder (Section 1 table) and Table 1, a one-page summary of results
  by output contract, class, model, and section. A skeleton is in Section 8.
- Contributions grouped by the seven messages, each pointing to its theorem.
- Relation to prior work (literature lead), with conservative wording.
- Reading guide: which appendices carry which proofs.

Budget: 6 pages including abstract.

### 01 Models (framing/editor; currently unassigned)

This section owns the definitions and toolkit lemmas that all authors use
(Section 3). It must exist early so that authors cite rather than re-derive.

- Encodings: explicit sparse rational polynomials; numerical degree D with
  unary encoding; rational polyhedra Ax <= b; total input length L counts
  all coefficients, exponents, constraints, thresholds, observables, and
  supplied certificates.
- Promise versus checked language: a supplied curvature bound mu is a
  promise; a supplied full positive definite Hessian Gram is checked in
  polynomial time and defines an ordinary language.
- Models: ordinary deterministic and Las Vegas bit computation;
  integer straight-line programs; rational circuits; PosSLP; many-one
  reduction to one PosSLP instance; P^PosSLP; UP^PosSLP; FPT with an
  absolute exponent of L; "relative to PosSLP" versus ordinary.
- Output contracts (`def:models-contracts`) as in Section 1.
- Certificates (`def:models-hessian-gram` and neighbors): full Hessian Gram
  on (v, x⊗v); polynomial Gram on monomials of degree at most two; SOS over a
  field E versus PSD Gram over E; rational-function SOS and common
  denominators; radial multipliers; block-separated certificates (two local
  Grams, each with its own constant entry); order-two moment matrices.
- Toolkit lemmas with proofs (Section 3, items T1-T7).
- A numbered list of external theorems used, with exact hypotheses
  (Section 7 register). Every later use cites this list.

Budget: 6-7 pages.

### 02 Points (author `points`; appendix C)

| Label | Input, model, output | IDs |
| --- | --- | --- |
| `thm:global-point` | Explicit sparse rational f, globally convex (promise, or charged certificate), numerical degree D, rational polyhedron P. Ordinary deterministic. Decides emptiness and unboundedness below in poly(L,D); otherwise attainment, rational R and Γ with log R + log Γ = poly(L,D), dist(x,S) <= Γ(f(x)-f*)^(1/D) on all of P for gap <= 1, the fixed minimum-norm optimizer to 2^-q in poly(L,D,q), value enclosure of width 2^-s in poly(L,D,q+s). Not claimed: log D dependence, circuit-encoded input, exact active sets. | P2 (subsumes P1) |
| `thm:cubic-point` | Explicit cubic, convex on a bounded rational polytope (promise; lower-dimensional allowed). Γ_P with poly(L) bits, exponent 1/4; set-distance and fixed minimum-norm output (original coordinates) in poly(L+q). Exponent 1/3 is necessary (t^3) but not claimed attainable. | P3 |
| `prop:points-active` | Exact active-bound recognition for a uniformly strongly convex cubic on a box (bags of size three, bounded coefficients and curvature) decides Square Root Sum with one query. Contrast with `thm:cubic-point`. | P4 |
| `prop:points-selector` | A box-convex quartic family where some optimizer is easy to approximate but a constant-accuracy minimum-norm selector decides Square Root Sum. | P5 |
| `thm:points-quartic-lower` | One constant-accuracy point query (distance 1/4) for a box-convex rational quartic with unique optimizer decides Square Root Sum (treewidth two, bounded coefficients) or PosSLP (unrestricted width). Conditional consequences only. | P6, P7 |
| `prop:points-regularization`, `prop:points-rectangle` (may be remarks with appendix proofs) | Method limits: Tikhonov extraction may need exponentially many printed parameter bits; rectangular certification may need exponentially many endpoint bits while implicit certificates stay short. | P8, P10 |

Appendix C carries every proof, plus the shared lemmas `lem:convex-value`,
`lem:integer-hoffman`, `lem:selector`, and the cubic transverse and slice
lemmas that Section 10 reuses. The convex value interface must be a stated
lemma with a proof or exact external contract (prewrite-points): affine
substitution is evaluated, not densely expanded.

Why it matters: it is the only place where value-to-point conversion is
quantitative, and it explains why exact labels, selectors, and some-optimizer
outputs are different problems. Budget: main 8-10, appendix 15-19.

### 03 Upper comparisons (author `upper`; appendix A)

| Label | Input, model, output | IDs |
| --- | --- | --- |
| `thm:exact-upper` | Explicit sparse f, h with unary (or polynomially bounded) numerical degrees; supplied mu with ∇²f ⪰ mu·I on R^n, or a checked full PD Hessian Gram. Each of >, >=, <, <=, = between h(p) and 0 has a deterministic polynomial-time many-one reduction to one PosSLP instance; no oracle calls during construction; no nonzero-gap promise. | A9 (A8 is the fixed-degree case) |
| `cor:upper-two-minima` | Exact comparison of two certified minima through a separable sum and a difference observable; only curvature is needed, not a joint full Gram. | A8 |
| `prop:upper-circuit-witness` | If min f < 0, a polynomial-size shared rational circuit for a point of {f <= 0} is built without an oracle. No rational or expanded witness at min f = 0. | A8 |
| `thm:posslp-closure` (decision D4) | Polynomial-size Boolean combinations of PosSLP queries, and deterministic polynomial-time adaptive PosSLP computations, compile to one PosSLP instance. | A13, A14 |
| `thm:upper-monotone` (decision D5) | The `thm:exact-upper` conclusion at the zero of a globally strongly monotone cubic map, with a checked Jacobian-Gram subclass. | A12 |
| `prop:upper-degenerate` (optional; or Section 11) | Zero-Hessian optimizer case solved by rational linear algebra; counterexamples to naive Newton extensions. | coverage §8.2 |

Appendix A: the separation lemma with the imported quantifier-elimination
theorem; derivative bounds; warm start through `lem:convex-value`; the
Newton circuit (LDL^T without pivoting; shared nodes); the shifted
comparison table; the closure compilers with the full error budgets (the
shortened schedules are known to fail); the monotone warm start if D5 keeps
it. Why it matters: the doubly exponential precision demanded by separation
is reached by a polynomial-size circuit, so the single final sign test is
the whole arithmetic difficulty. Budget: main 5-7, appendix 10-14.

### 04 Lower reductions (author `reductions`; appendix B)

| Label | Input, model, output | IDs |
| --- | --- | --- |
| `lem:quartic-realization` | Shared assembly lemma; exact contract in Section 3, item S1. | S3 core |
| `thm:reductions-root-circuit` | PosSLP maps to certified positive cube-root circuits (radicands affine in earlier roots and their squares; rational boxes certify every gate); a designated output is not 1 and exceeds 1 exactly when V > 0. | A5 |
| `thm:reductions-root-language` | That root-comparison language is PosSLP-complete. May instead sit in Section 03, since its upper half uses the Newton machinery. | A5, A6 |
| `thm:reductions-signed-root` | Signed odd-root circuits with checked boxes away from zero and unary degrees give polynomial-size quartic singletons: ∇²F ⪰ (3/2)I, n+1 rational squares, rational PD Hessian Gram. A2 is a remark. | A3 (A2) |
| `thm:reductions-min-sign` | Minimum-sign hardness with a promised nonzero minimum and full Gram at least I. | A7 |
| `thm:quartic-complete` | Assembled classification, including real SOS, nonnegativity and PD polynomial Gram existence (complete) and rational SOS membership (hard; matching upper bound open at minimum zero). Equality has only the upper bound. | A5, A7, A9 |
| `thm:rational-optimizer` | Coordinate comparison stays PosSLP-complete with a rational optimizer in [-1,1]^n, known minimum zero, n+1 short rational square factors, and a checked full Gram. Rationality is a promise. | A10, A11 |

Remarks: A1 (comparison of sums of one-real-conjugate numbers reduces to one
quartic plus one affine inequality; a different source problem), A4 (a
box-convex baseline lacks the global format), and the failed naive gate
lifting (coverage §8.1). Appendix B carries the full analytic constants and
interval certificates. Why it matters: the hardness survives every natural
restriction that might have suggested ordinary exact algorithms — strict
checked convexity, no constraints, nonzero optimum, rational optimizer.
Budget: main 7-9, appendix 18-22.

### 05 Constraints and integer selection (author `constraints`; appendix D)

Use k for nonlinear dimension, t for the number of integer variables, and
r for the rank of the continuous constraint normals (prewrite-constraints).

| Label | Input, model, output | IDs |
| --- | --- | --- |
| `thm:constraints-unambiguous` | Strongly convex quartic on an arbitrary rational polyhedron: value and coordinate comparisons in UP^PosSLP ∩ coUP^PosSLP via the unique full active set and an LP with a circuit objective. The support-guessing NP^PosSLP version is a remark. | C1 |
| `prop:constraints-active-gap` | A supplied lower bound on nonzero optimal slacks gives one PosSLP instance per relation. | C2 |
| `thm:constraints-nonlinear` | Ordinary deterministic F(k)L^C exact comparison and active-set recovery, k = nonlinear dimension; implicit optimizer as an affine image of the zero of a k-variable strongly convex quartic. Mixed corollary: ordinary F(k+t)L^C. | C5 |
| `thm:constraints-transfer`, `cor:constraints-boxes`, `cor:constraints-flows` | A polynomial-operation exact QP interface transfers to P^PosSLP; instantiated for comparison-matrix-PD boxes (forests, Stieltjes) and separable polynomial network flows. | C6, C7, C8 |
| `thm:constraints-rank` | Las Vegas, expected (r+1)^O(r) L^C with a PosSLP oracle. State for gradient maps or for monotone VIs according to D5. | C3, C4 |
| `thm:constraints-candidates` | Ordinary 2^O(t log(t+1)) L^C list containing every optimal integer block (at most 2^t of them) with unconstrained continuous fibers; nonadaptive PosSLP selection. | M2 (subsumes M1) |
| `thm:constraints-mixed-candidates` | Arbitrary mixed linear constraints: ordinary a(t)L^C list. The sharper parameter function is not proved here. | M3 |
| `thm:constraints-mixed-rank` | Expected F(t,r)L^C with PosSLP: an optimal integer block and an implicit continuous optimizer. | M4 |
| `cor:constraints-binary` | One unique optimal binary decision stays PosSLP-hard with known minimum zero, bounded rational optimizer, rank-one continuous constraints. | M5 |

Close with the open unrestricted case (coverage §8.3), including why
penalties and barrier accuracy bounds do not supply the missing interface.
Why it matters: it locates exactly where constraints add difficulty and
gives the solver-relevant separation of discrete search (ordinary
precision) from exact selection. Budget: main 9-11, appendix 16-20.

### 06 Algebraic singletons and degree (author `algebraic`; appendix E)

| Label | Content | IDs |
| --- | --- | --- |
| `prop:algebraic-bivariate` | Integer bivariate quartic, ∇²F ⪰ 4096 I with printed rational certificate, unique zero (2^(1/3), 4^(1/3)); no rational feasible point of {F <= 0}. | S1 |
| `thm:singleton-field` | A real algebraic number is a coordinate of the unique zero of a strongly convex rational SOS quartic with rational PD Hessian Gram exactly when it has one real conjugate; polynomial-time construction from a dense minimal polynomial; necessity holds for every rational convex-polynomial singleton. Three strictly convex quadrics as a corollary. | S2, S3 |
| `cor:algebraic-sums` | Comparison of sums of one-real-conjugate numbers reduces to one quartic plus one affine inequality. | A1 |
| `thm:algebraic-dimension` | (d+1)/2 power coordinates suffice and are optimal for the prescribed truncated power point only. | S4 |
| `thm:algebraic-cyclic` | Integer quartics in n variables, O(log n)-bit coefficients, zero field degree (2^(n+1)-(-1)^(n+1))/3, n+1 squares after compression; dense and ordinary sparse coordinate minimal polynomials exponential after a rational translation. | S5, S6 |
| `thm:sos-length` | Globally convex degree-four F with a zero and PD Hessian there needs at least n+1 real squares; sharp. | S6 |
| `thm:algebraic-degree-bounds` | Rational SOS quartic with unique real zero and PD Hessian: degree <= 2^n-1; global convexity gives 2^n-3 (n>=3) and 2^n-5 (n>=4); sharp for n = 2,3,4. Five variables per D2. | S8, S9 |
| `thm:algebraic-univariate` | Univariate convex realizations of some O(b)-bit cubic numbers need degree 2^Ω(b); two-variable quartics realize them; a polynomial-size univariate circuit realization exists. | S10, S11 |
| `prop:algebraic-network` (appendix) | Cyclic degree is maximal within minimum-size strongly connected binomial exposing networks. | S7 |
| Examples | Conditioned nested-root path with exponentially many nonzero minimal-polynomial coefficients; quartic epigraph value of degree 3^n. | P9, Q4 |

Why it matters: it determines which exact outputs are possible at all, and
shows that strong certified convexity does not bound algebraic degree.
Budget: main 8-10, appendix 18-24 (plus 8-10 if S9 is included).

### 07 Expanded output, heights, moment and Gram matrices (author `heights`; appendix F)

| Label | Content | IDs |
| --- | --- | --- |
| `thm:heights-witness` | Polynomial-size strongly SOS-convex quartics in n = 2k variables with compact zero sublevels with interior, where every rational point of the closed sublevel needs Ω(n 2^(n/2)) denominator bits; a short shared-circuit strict witness exists. | H1 |
| `thm:rational-height` | Bounded rational minimizer with denominators 5^(2^k) in n = 2(k+1) variables; short square factors and full Gram; local Hessian condition polynomial at the optimizer only. | H2, H3 |
| `thm:interior-gram` | Interior (PD) rational polynomial Grams: size poly(L)2^O(n) always suffices; Ω(n 2^(n/2)) denominator bits are sometimes necessary although short singular Grams exist. | G1, G2 |
| `thm:circuit-gram` | Polynomial-time, sign-oracle-free shared-circuit Gram, PD exactly when min f > 0. No cheap validation claim. | G3 |
| `thm:heights-moment` | Full PD Hessian Gram gives a unique rank-one order-two moment optimum; the optimizer field is the least field for maximal-rank optimal Grams and for nonzero PSD exposing matrices of the real optimal Gram face. | G4 |
| `cor:heights-gram` | The circle family forces long entries in the moment optimum, in every maximal-rank rational optimal Gram, and in every nonzero rational exposing matrix; short lower-rank Grams remain. | G5 |
| Remark | Nullvector compression caution. | G6 |

Why it matters: it separates "a rational object exists" from "a short
rational object exists", and shows which certificate shapes (maximal rank,
interior, exposing) carry the optimizer's arithmetic. Budget: main 6-8,
appendix 11-14.

### 08 SOS fields and rational descent (author `fields`; appendix G)

| Label | Content | IDs |
| --- | --- | --- |
| `thm:fields-ternary` | 31-monomial integer ternary quartic, ∇²F ⪰ I, printed rational PD Hessian Gram, minimum 0; SOS over E iff PSD Gram over E iff 2^(1/5) ∈ E; three variables minimal under the strict Gram hypothesis. | F2 |
| `lem:fields-positive-constant` | F + eta is rational SOS for every rational eta > 0; the rational SOS bound is not attained. | F1, F2 |
| `thm:fields-prime` | Every prime ℓ >= 5 is the exact least field degree, in (ℓ+1)/2 variables. Rename the prime away from p. | F3 |
| `thm:tower-field` | Polynomial-size quartic in 3k variables with least SOS/PSD-Gram field Q(2^(1/5^k)). | F4 |
| `thm:fields-coefficient-degree` | Some individual algebraic coefficient has degree >= 5^k. | F5 |
| `prop:fields-compact` | Polynomial-size root-circuit SOS coefficients and polynomial-size rational certificates modulo the solvable root system. | F6 |
| `thm:fields-tower-spaces` | Complete rational quadratic vanishing space and stationary quartic space of the tower; rational SOS recognition at that supplied zero is linear algebra plus one PSD test. | F7 |
| `thm:fields-descent` | Small vanishing-space descent criterion; prewrite review found it correct. Cyclic applications only in recorded finite dimensions unless proved for all n. | F8 |
| Appendix | Four-variable example with a membership (not positivity) obstruction. | F1 |

Why it matters: exact SOS output can require large fields even with short
rational convexity certificates; compact formats avoid it. Budget: main 6-8,
appendix 12-15.

### 09 Rational-function and block certificates (owner to confirm: D8; appendix H)

| Label | Content | IDs |
| --- | --- | --- |
| `prop:certificates-quadratic-denominator` | Printed rational multiplier certificate for the ternary example; common denominator of degree two is minimal. | R1 |
| `lem:certificates-multiplier` | General quadratic multiplier lemma and its several-relation and higher-membership forms. | R2, R3, R4 |
| `thm:certificates-radial` | Scaled ternary family: every fixed radial order fails for large t, an adapted quadratic denominator stays short; quantitative order Ω(log L / log log L). | R5, R6 |
| `thm:certificates-block` | Short joint rational SOS, no rational block-separated SOS; growing separated field Q(2^(1/5^k)); a positive family with exponentially long separated certificates. | B1 |
| `thm:certificates-block-convex` | The same with strongly SOS-convex blocks; full joint PSD Hessian Grams are singular. | B2 |
| `thm:quadratic-graph` | Polynomial-size realization of the optimizer and its quadratic products; zero-minimum promise. | B3 |

Why it matters: certificate format (polynomial versus rational function,
adaptive versus prescribed multiplier, joint versus block) can change
existence or size while real feasibility is unaffected. Budget: main 6-8,
appendix 13-16.

### 10 Cubic recourse (author `recourse`; appendix I)

Scope depends on decision D1. Under the recommended option A:

| Label | Content | IDs |
| --- | --- | --- |
| `prop:recourse-fiber` | Residual-convex cubics on product boxes: rational Hessian kernel constant on each relative core face; optimizer slice with one varying quadratic row; error bound with exponent 1/4 under supplied face and minor margins. | RQ4 |
| `prop:recourse-examples` | vz^2 and γv - v^2 z: no uniform fiber constant; approximate-core minimum-norm completion picks the wrong optimizer; no finite core convexifier. | RQ4 |
| `lem:recourse-face`, `lem:recourse-lattice` | Sound endpoint certificate by tilt monotonicity; LLL margin certificate with sufficient acceptance condition. | RQ3 |
| `thm:recourse-completion` | Given Cauchy oracles for the selected cores of F_γ and its 2k coordinate tilts, a deterministic procedure either rejects or certifies face and margins; after acceptance it returns the fixed selected full optimizer to 2^-q in polynomial overhead. Every acceptance is correct. | RQ3 |
| `prop:recourse-margin-probability` | Under continuous uniform core noise, rejection has small probability (contact-gradient and quadratic sublevel bounds). The finite-grid version needs a semialgebraic section count (imported). | RQ3 |

The smoothed expected-work statement f(k)(1+Λ_c/σ)^k poly(L+q) is then a
conditional corollary naming the selected-core theorem (V2) and exact
fallback as hypotheses, or is omitted. Budget: main 5-7, appendix 9-12.

### 11 Discussion (framing/editor)

Summary of the ladder results; uses for MINLP (exact node decisions,
certificate formats, certificate sparsity, discrete search versus exact
selection); open problems: unrestricted polyhedral P^PosSLP; equality lower
bound; degenerate convex quartics; all-PSD Gram size; degree maxima for
n >= 6 (or n >= 5 per D2); coupled-domain and quartic recourse; binary
degree and circuit input; cubic exponent 1/3. Budget: 3-4 pages.

## 3. Shared interfaces: one owner, one statement

Several results are used by more than one author. Each needs exactly one
statement and proof, and every other author must cite it. Writers should
receive these contracts now; mismatched local versions are the most likely
integration failure.

| Item | Proposed label | Owner | Consumers | Required content |
| --- | --- | --- | --- | --- |
| T1 | `lem:models-det-trace` | 01 | 03-09 | det(M)/tr(M)^(m-1) <= λ_min(M) for M ≻ 0; polynomial bit length |
| T2 | `lem:models-gram-curvature` | 01 | 03-09 | Full PD Hessian Gram M gives ∇²f ⪰ λ_min(M)I; invertible rational affine changes act by congruence on (v, x⊗v) |
| T3 | `lem:models-division` | 01 | 03, 05, 07 | Rational circuits as positive-denominator integer pairs without sign queries; one PosSLP instance decides a rational sign |
| T4 | `lem:models-rational-squares` | 01 | 04, 08, 09 | A positive rational is a sum of O(bit length) rational squares in polynomial time without factoring; rational LDL gives unweighted rational SOS |
| T5 | `lem:taylor-sos` | 01 | 03, 04, 07, 08, 09 | Taylor integration of a Hessian Gram at a stationary point; ∫(1-t)(U+tV)^2 = ½(U+V/3)^2 + (V/6)^2; coefficients lie in the field generated by the point and the Gram; strict version (PD on nonconstant monomials); gradient completion f = Taylor term + (mu/2)||d+b/mu||^2 + [f(a) - ||b||^2/(2mu)] |
| T6 | `lem:models-low-degree` | 01 | 03, 04, 06 | A globally convex polynomial of degree <= 3 is quadratic (and, if D5 keeps A12, a strongly monotone quadratic map is affine) |
| T7 | `lem:models-strong-convexity` | 01 | 03, 05, 06, 09 | Gap-to-distance, minimizer radius from a feasible point, fiber strong convexity under partial minimization |
| C1 | `lem:convex-value` | 02 / app C | 02, 03, 05, 06, 09, 10 | Feasible rational point with value gap <= η on an explicit rational polyhedron inside a known box, for a convex function given by sparse or composed evaluation and subgradients, in poly(L, log 1/η, D); affine hull, interior ball, exact feasibility repair. Derive from the classical ellipsoid theorem; credit value-gap results for unbounded polyhedra separately |
| C2 | `lem:integer-hoffman` | app C | 02, 10 | Distance to P ∩ {Tx = t} from points of P bounded by (sC)^(s-1)||Tx - t|| with integer rows and arbitrary real right-hand side; a variant with supplied nonzero-minor margins |
| C3 | `lem:selector` | app C | 02, 10 | Regularization schedule turning dist <= Γ·gap^(1/D) and ||p|| <= R into a fixed minimum-norm selector, including unbounded optimizer sets |
| C4 | `lem:points-cubic-transverse`, `lem:points-cubic-slice` | app C | 10 | Transverse estimate E >= (d'H_c d)^2 / (384 M R^2) and the optimizer slice with the gradient row |
| U1 | `lem:separation` | 03 / app A | 03, 05, 07 | If ∃X Φ(X,z) defines the singleton {α}, then α = 0 or |α| >= 2^(-2^(e(L))). Second form needed by C5: fixed degree d, s quantified variables, coefficient bits τ, gives log(1/|α|) <= τ·c(d)^s·poly, linear in τ. States the imported elimination theorem exactly |
| U2 | `lem:newton-circuit` | app A | 03, 05, 07 | Polynomial-size shared rational circuit x_K with ||x_K - p|| small enough for every observable whose encoding is at most a common bound M (the uniformity used by the unambiguous verifier and the circuit Gram) |
| U3 | `thm:posslp-closure` | app A | 03, 05, 11 | Per decision D4 |
| R1 | `lem:quartic-realization` | 04 / app B | 04, 06, 07, 08, 09 | Rational quadratics r_1..r_n vanishing at an unknown a with J'J ⪰ ν²I, ||∇r_j(a)|| <= β, quadratic parts of norm <= 1, ||a|| <= K; rational quadratic G with G(a) = 0, quadratic part between m·I and Λ·I, ||∇G(a)|| <= ε, where ε = t² <= min{1, m²/(2n), ν²m²/(36n(Λ+nβ)²)}. Then F = (G/(tν))² + Σ(r_j/ν)² has ∇²F ⪰ (3/2)I, unique zero a, n+1 rational squares; with a rational approximation oracle for a, a rational PD Hessian Gram of polynomial size is computed in polynomial time (formal-center Gram plus exact projection onto the Gram identities). The factor n in the last denominator is required for the Gram, not for convexity |
| R2 | `lem:reductions-small-signal` | app B | 04, 07 | Repeated root squaring S(z) = (1+3z²)^(1/3) - 1 with rational interval boxes produces 0 < δ <= δ_0^(2^q) by a short circuit; used by witness and interior-Gram families unless they use their own specialized construction (prewrite-heights) |
| E1 | `lem:one-real-conjugate` | app E | 04, 06 | Coordinates of a rational convex-polynomial singleton have exactly one real conjugate |
| F1 | `thm:tower-field` | 08 / app G | 09 | Least field and the slice argument |
| H1 | `thm:interior-gram` family h_k | 07 / app F | 09 | Polynomial-size strictly positive family with tiny minimum m_k |

Section label prefixes: `sec:`, `app:` with the topic name; equations
`eq:<topic>-...`.

## 4. Structure gaps and decisions for the root

**D1. Cubic recourse scope (critical; author `recourse` is running).**
The October 3 expected-work theorem depends on the all-scale value count,
the selected-core hull theorem, the projected-growth tail, the finite-noise
section bound, and the same-selector exact fallback (V1, V2, and their
predecessors). None is in any appendix, and repository notes cannot fill
the gap (prewrite-points). Options:

- A (recommended): prove the deterministic content in full (fiber
  geometry, examples, face certificate, LLL margin certificate, certified
  completion relative to selected-core oracles, continuous-noise rejection
  probability). State the smoothed expected-work bound only as a
  conditional corollary with V2 and the fallback named as hypotheses, or
  omit it. This keeps Section 10 an output-contract result.
- B: add a self-contained appendix for V1, V2, the growth tail, section
  counts, and the fallback. Estimated 35-45 additional pages of smoothed
  analysis and real-algebraic machinery outside the paper's subject.
- C: keep only fiber geometry and examples.

**D2. Five-variable sharp degree 21 (S9).** The prewrite audit reconstructs
it, but it rests on residual-intersection and low-degree classification
imports. Include it with full proof in appendix E if those imports can be
quoted exactly; otherwise state S8 and record the exact five-variable value
as not established in this paper.

**D3. Quadratic and spectrahedral contrasts (Q1-Q14).** No file exists in
`main.tex`. Recommended: a short appendix (new `appendices/J-contrasts.tex`)
with proofs of Q1 (span at most two gives rational witnesses; span three
does not), Q6 and Q8 (spectrahedral singleton fields), and the sparse-output
part of Q3. Mention the remaining Hessian-span algorithms only in Section 11,
without claims. Alternatively fold Q1, Q6, Q8 into appendix E.

**D4. PosSLP closure (A13, A14).** The prewrite audit found the Boolean and
adaptive compilers valid, giving many-one completeness of PosSLP for
P^PosSLP under standard conventions. If adopted, every deterministic
P^PosSLP statement (C6-C8, selection in M2) can also be stated as one
PosSLP instance; UP, Las Vegas, and nonadaptive-list statements keep their
form. Decide once and apply uniformly. Use restrained wording until the
literature lead reports the status of this closure.

**D5. Monotone maps (A12, C3, C4).** Keeping them adds the rounded-ellipsoid
warm start and its external contract. Restricting to gradient maps loses
nothing for optimization. Decide before `upper` and `constraints` finalize
statements.

**D6. Printed finite certificates.** Several proofs use explicit rational
data: the bivariate certificate, the ternary 12×12 Hessian Gram with its
leading principal minors, the 15×15 multiplier Gram, product-independence
determinants. A printed exact certificate that a reader can verify is a
proof object; "a script passed" is not. Confirm that appendices may print
these (or their LDL pivots) and that numerical thresholds not needed for a
theorem (for example τ_1) are omitted or marked illustrative.

**D7. Position of Section 10.** Under D1-A it is a point-output result and
reads best directly after Section 02 (reorder the `\input`, no renaming).
Under D1-B it can stay last as an application.

**D8. Owner of Section 09 and appendix H.** No `certificates` author is
listed; confirm that `fields` owns it.

**D9. Value-optimization dependency.** Replace reliance on a single
preprint corollary by `lem:convex-value` from the classical ellipsoid
theorem, with the value-gap literature credited. This also removes doubt
about sparse versus dense encodings when D grows (A9, P2).

**D10. Unowned supporting items.** Assign: degeneracy frontier (§8.2) and
equality frontier (§8.12) to Section 11 (optional short proposition in
appendix A); G6 to Section 07; P9 to Section 06; M5 to Section 05; A1 and
A4 as remarks. Exclude the reference checker and partial formal proofs
from the main text; at most an availability note.

## 5. Notation and vocabulary reservations

These supplement `CONVENTIONS.md`; the source notes collide on most of them.

| Symbol | Reserved meaning | Needed changes from sources |
| --- | --- | --- |
| L | total binary input length (at least two) | October 3 uses I; recourse notes use L for curvature (use Λ_c); realization notes use L for ||H|| bounds (use Λ); field lemmas use L for a field (use E_1) |
| n | number of continuous variables of the instance at hand | constructions that use N for variables state n = N |
| k, t, r | k the theorem's stated structural parameter; in Section 05 t = integer variables, r = continuous constraint rank | each theorem defines k |
| q | requested precision bits, ε = 2^-q | quaternions (use u, w), quadratics q_j (use r_j, s_j, g_j), rational centers (use c) |
| p | the selected optimizer or unique zero | minimal polynomials p(T) become P_α or m_α; the prime in F3 becomes ℓ |
| f, F | f generic objective; F with subscripts for constructed families, introduced as "the objective f = F_k" | |
| h | observable | the interior-Gram family h_k needs another name (for example φ_k) where both appear |
| S, f* | optimizer set, optimal value | |
| μ, Λ | curvature lower bound; curvature or Lipschitz upper bound | sources use M, L_0, L_*, L_M |
| D | numerical degree (Sections 02-03) | rename denominators, diagonal matrices, and D(b,T) locally |
| e(L) | the separation exponent polynomial | sources write a(L), colliding with points a |
| V, W | PosSLP output and W = 2V - 1 | gradient bound V in the realization lemma becomes β |
| K, E | coordinate field Q(p); arbitrary real subfield | constants K_D, K need other names in Sections 06-08 |

Model words must be used consistently: "curvature promise" versus "checked
Hessian Gram"; "one PosSLP instance" versus "P^PosSLP" versus
"UP^PosSLP ∩ coUP^PosSLP" versus "Las Vegas with a PosSLP oracle" versus
"ordinary"; "shared rational circuit" versus "expanded rational"; "dense
minimal polynomial" versus "ordinary sparse list" versus "root circuit";
"SOS over E" versus "PSD polynomial Gram over E"; "Hessian Gram" versus
"polynomial Gram"; "set distance" versus "fixed selector" versus "value
enclosure".

## 6. Editorial priorities for the framing/editor

1. Publish the Section 3 contracts and labels to all authors and write
   Section 01 first, so that appendices cite one toolkit.
2. Obtain decisions D1, D4, D5, D8 immediately; each changes statements in
   more than one file.
3. Build the abstract and introduction around the ladder, Table 1, and
   per-theorem contribution statements. No research history, no repository
   references, no "reviewed" language.
4. Consistency pass across all files: notation (Section 5); promise versus
   checked input; equality excluded from completeness; "exponential in
   dimension, superpolynomial in L" rather than 2^Ω(L) (prewrite-heights);
   field statements versus encoding statements; local versus uniform
   conditioning.
5. Deduplication pass: each shared item proved once; appendices cite.
   Likely duplicates: Taylor SOS, Hoffman bounds, separation, Newton
   circuits, the realization lemma, small-signal generation, convex value
   calls, the one-real-conjugate argument.
6. Self-containment pass: every proof step either proved or a numbered
   external theorem with exact hypotheses (Section 7). Search for
   "companion", "note", "repository", links, and "see ... for details".
7. Length pass: target main text at most about 65 pages; move constructions
   longer than about a page to appendices; keep one motivation paragraph per
   section.
8. Integrate the literature lead's report with conservative attribution;
   any statement about the inspected version of the convex polynomial
   programming preprint is version-specific.

## 7. Serious correctness and editorial risks

Ranked by consequence. None is a known mathematical error; the prewrite
audits found no blocking defect in the audited scopes.

1. **Unproved inherited interfaces in Section 10 (critical).** Copying the
   October 3 theorem would leave a main claim resting on unpublished notes.
   Mitigation: D1.
2. **External theorem contracts.** Several proofs depend on exact
   hypotheses of imported results (Section 8 register). The highest risks:
   (a) the quantifier-elimination bound must give coefficient height linear
   in τ for the FPT theorem, and the sources cite two different statements;
   (b) the value-optimization source must handle the actual encoding and
   degree (D9); (c) the integer-query feasibility theorem is quoted from a
   very recent preprint; (d) the flow and box QP algorithms must use only
   rational arithmetic and comparisons, with no floor or root operations on
   circuit-valued data; (e) the LP with circuit objective needs the
   operation count independent of objective encoding.
3. **The closure theorem (D4)** is strong and changes how half the paper
   states complexity. It needs its complete interpreter proof and the full
   error budget; shortened schedules are known to fail.
4. **Notation collisions** (Section 5) are pervasive in the sources and
   would make merged statements wrong, not just awkward (for example L as
   both length and curvature in the recourse work bound).
5. **Promise and format drift.** Hardness instances must lie in the checked
   language; upper bounds hold for the promise. Rationality (A11),
   zero-minimum (B3), dense irreducible one-real-root input (S2-S4), unary
   degree (A3, A9, P2), and supplied slack gaps (C2) are promises or input
   formats and must stay visible.
6. **Overstated size bounds.** Height and degree lower bounds are
   exponential in dimension and superpolynomial in L; none is 2^Ω(L). They
   concern specified expanded formats and do not exclude NP certificates,
   circuits, root towers, or sparse auxiliary encodings.
7. **Field-statement subtleties.** A PSD Gram over E need not factor over E;
   least-field claims need both directions; individual-coefficient degree
   (F5) is stronger than field degree (F4); rational vanishing spans differ
   from real ones (R5, F8).
8. **Restricted certificate claims.** Maximal-rank and exposing-matrix
   bounds (G5) concern rational matrices and exposing matrices of all real
   feasible Grams; interior-Gram lower bounds concern PD Grams only; joint
   Hessian-Gram singularity concerns PSD Grams.
9. **Finite computation inside proofs.** Explicit certificates must be
   printed and checkable; "all n" claims cannot rest on finite-dimension
   computations (F8 cyclic applications, S7).
10. **FPT hygiene.** Parameter functions must not enter the exponent of L;
    the sharper 2^O(t log t) bound is proved only for unrestricted fibers.
11. **Length and coherence.** At the budgets below the manuscript is about
    200 pages. Without the ladder framing and aggressive appendix use it
    will read as a report. A two-part split is the main alternative, but it
    conflicts with the single-manuscript brief.
12. **Attribution.** Several statements are corollaries of established
    techniques (error-bound exponent, Taylor SOS, moment exactness, violator
    spaces, rank-versus-height in SDP, regular denominators). Contribution
    language must say what is added; the literature lead settles priority.

## 8. External theorem register (for the literature lead) and Table 1 skeleton

Each entry needs an exact primary statement, hypotheses, and model.

| Result to vet | Used in |
| --- | --- |
| One-block real quantifier elimination with degree and coefficient-height bounds | `lem:separation` (03, 05, 07) |
| Ellipsoid-method weak constrained convex minimization with evaluation and subgradient oracles | `lem:convex-value` |
| Value-gap and radius theorems for convex polynomial programs (credit; optional use) | 02, 03 |
| LP with operation count polynomial in the constraint-matrix size (objective-independent), and its rounding implementation | C1 |
| Rounded-ellipsoid cut-or-stop | A12 if kept |
| Integer-query convex feasibility with FPT bound; FPT integer linear feasibility; mixed-integer convex quadratic feasibility | M2, M3 |
| Violator-space sampling bound | C4 |
| Strongly polynomial separable quadratic flow and its arithmetic model | C8 |
| Box QP pivoting algorithm (or the self-contained replacement in prewrite-constraints) | C7 |
| Proximal Newton estimate (replaceable by a short direct proof) | C6 |
| LLL reduced-basis inequality | Section 10 |
| Certified complex root isolation in polynomial bit time | S2-S4, S10 |
| Isolated-point Bézout bound; Cayley-Bacharach; residual intersection and low-degree classification | S8, S9 |
| Brouwer degree and properness facts | S6 |
| Rational nonnegative ternary quartics that are not rational SOS | F2 minimality |
| Rational SOS versus rational PSD Gram | 08 |
| Rational sampling in open semialgebraic sets | G1 |
| Exact SOS-convex moment relaxation (credit) | G4 |
| Pure-state criterion for regular denominators (only if finiteness of radial order is claimed) | R5 remark |
| Semialgebraic section component counts (only under D1-B or the finite-grid probability) | Section 10 |
| Credit only: compressed Newton classifications, real-computation characterization of P^PosSLP, SDP arithmetic hardness, conditional PosSLP hardness, essential variables, Taylor SOS for SOS-convexity, Khachiyan-type height examples, real block SOS, radial multipliers, rational certificate algorithms, convex MIQP FPT | 00, 11 and theorem preambles |

Table 1 skeleton for the introduction (one row per result family):

| Output | Class | Result | Model | Section |
| --- | --- | --- | --- | --- |
| Point | globally convex, sparse, degree D | fixed selector, poly(L,D,q) | ordinary | 02 |
| Point | cubic convex on polytope | fixed selector, poly(L+q) | ordinary | 02 |
| Point | quartic convex on box | constant accuracy decides SRS / PosSLP | conditional | 02 |
| Label | strongly convex cubic on box | exact active bound decides SRS | conditional | 02 |
| Exact | strongly convex explicit polynomial | one PosSLP instance per relation | many-one | 03 |
| Exact | certified quartic | order tests PosSLP-complete; also with rational optimizer | many-one | 04 |
| Exact | quartic on polyhedron | UP ∩ coUP relative to PosSLP; structured P^PosSLP; FPT in nonlinear dimension | various | 05 |
| Exact | mixed integer | ordinary candidate lists; Las Vegas FPT in t + r with PosSLP | various | 05 |
| Representation | singletons | one real conjugate characterization; exponential degree | construction | 06 |
| Representation | expanded rational | witnesses, rational optimizers, interior Grams, moment and exposing matrices | size bounds | 07 |
| Certificate | SOS fields | ternary, prime, tower fields; compact alternatives | field bounds | 08 |
| Certificate | formats | multipliers, radial order, block separation | existence and size | 09 |
| Point | residual-convex cubic core | certified completion (per D1) | ordinary given core oracle | 10 |

## 9. Length budget

| Part | Main pages | Appendix pages |
| --- | --- | --- |
| Abstract, 00, 01 | 12-13 | - |
| 02 points / C | 8-10 | 15-19 |
| 03 upper / A | 5-7 | 10-14 |
| 04 reductions / B | 7-9 | 18-22 |
| 05 constraints / D | 9-11 | 16-20 |
| 06 algebraic / E | 8-10 | 18-24 (+8-10 with S9) |
| 07 heights / F | 6-8 | 11-14 |
| 08 fields / G | 6-8 | 12-15 |
| 09 certificates / H | 6-8 | 13-16 |
| 10 recourse / I (D1-A) | 5-7 | 9-12 (+35-45 under D1-B) |
| 11 discussion | 3-4 | - |
| Contrasts / J (D3) | - | 5-7 |
| Total | about 75-95 | about 125-165 |

To meet a main-text target near 65 pages, the main text should carry
statements, contracts, importance, and proof ideas, with every proof longer
than about a page moved to its appendix.
