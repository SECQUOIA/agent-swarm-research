# Author report: constraints (Section 5 and Appendix D)

Date: 2026-10-05. Author: Opus main writer for `constraints`. Files owned and
written: `sections/05-constraints.tex` and `appendices/D-constraints.tex`. No
other manuscript file, shared macro, `main.tex`, or `references.bib` was edited.
No literature research, experiment, or mathematical script was run.

## 1. Coverage

| ID | Result in the manuscript | Proof location |
| --- | --- | --- |
| C1 | `thm:constraints-unambiguous` (UP^PosSLP ∩ coUP^PosSLP via the unique full active mask and a circuit-objective LP). The support-guessing NP^PosSLP ∩ coNP^PosSLP bound is `rem:constraints-unambiguous` with `lem:constraints-support-test`. | D.1 (`app:constraints-geometry`), D.2 (`app:constraints-unambiguous`): `lem:constraints-circuit-lp`, `lem:constraints-cone-test` |
| C2 | Not duplicated. Section 3 owns `prop:upper-slack-gap`; Section 5 summarizes it in one paragraph and cites it (root instruction). My earlier draft proposition and proof were removed. | Section 3 / Appendix A |
| C3 | Included in `thm:constraints-unambiguous`, which is stated for strongly monotone cubic variational inequalities (T = ∇f gives C1). | D.1, D.2 |
| C4 | `thm:constraints-rank` (Las Vegas, expected (r+1)^{O(r)} L^C, implicit output). | D.5 (`app:constraints-rank`): `lem:constraints-violator`, `lem:constraints-rank-primitive`, contract (E3d) |
| C5 | `def:constraints-nonlinear-dimension`, `lem:constraints-essential`, `thm:constraints-nonlinear` (ordinary, F(k)=2^{O(k)}, active set, implicit optimizer with reduced modulus ν), `ex:constraints-rank-one-quartic`, `rem:constraints-psd-certificate`; mixed version `cor:constraints-nonlinear-mixed`. | D.3 (`app:constraints-nonlinear`): `lem:constraints-elimination`; D.7 |
| C6 | `def:constraints-qp-solver`, `lem:constraints-newton-step` (full proof in main text), `thm:constraints-transfer` (P need not be bounded). | D.4 (`app:constraints-newton`) |
| C7 | `cor:constraints-boxes` (forest, Stieltjes, comparison-matrix PD; infinite bounds; fixed degree D). Self-contained `lem:constraints-admissible` and `lem:constraints-box-qp` (parametric 2n-pivot procedure, O(n^4) operations). | D.4.1 (`app:constraints-boxes`), `lem:constraints-truncation` |
| C8 | `cor:constraints-flows` (separable polynomial flows; rank unrestricted; infinite bounds; checkable curvature for D ≤ 4). | D.4.2 (`app:constraints-flows`), contract (E3c), `lem:constraints-artificial` |
| new (root) | `cor:structured-single-sign` (one PosSLP instance per predicate and per polynomial Boolean combination, placed after the box/flow corollaries). | D.4.3 (`app:constraints-single-sign`) |
| M1 | Subsumed: last sentence of `cor:constraints-selection` (P^PosSLP and many-one for each fixed t). Hardness for every fixed t in the certified format: `lem:constraints-padding` (Gram-preserving padding from the fixed-integer source). | D.6 |
| M2 | `lem:constraints-integer-cut`, `thm:constraints-candidates` (2^{O(t log(t+1))} L^C, all optimal blocks, at most 2^t and sharp), `cor:constraints-selection` (nonadaptive; one PosSLP instance per threshold predicate by `thm:posslp-closure`(c), FPT construction time). | D.6 (`app:constraints-lists`): `thm:constraints-integer-query` (imported), `lem:constraints-gradient-cut` |
| M3 | `thm:constraints-mixed-candidates` (F(t) L^C, no Slater, no multiplier bound). | D.7 (`app:constraints-mixed`): `lem:constraints-residual-cut` |
| M4 | `thm:constraints-mixed-rank` (Las Vegas, lexicographically smallest optimal block, all ties retrievable). | D.7 |
| M5 | `cor:constraints-binary` (known optimal value 1/4, rational bounded unique optimizer, rank one, t = 1; full-Gram variant). | D.8 (`app:constraints-binary`) |
| new | `cor:constraints-mixed-unambiguous`: with arbitrary mixed constraints and fixed t, threshold predicates are in UP^PosSLP ∩ coUP^PosSLP (FPT-time unambiguous machines). A short composition of M3 and C1 with full proof. | D.7 |
| §8.3 | `sec:constraints-open`: the arbitrary-polyhedron deterministic P^PosSLP question is stated as open (equivalently one PosSLP instance, by `thm:posslp-closure`(b)); circuit-Hessian QP interface, penalty and accuracy-driven routes are shown to fall short; no hardness is claimed. | main text |

## 2. Shared labels used and the exact form relied on

- `thm:exact-upper`: one PosSLP instance per relation at the unconstrained minimizer, n ≥ 1, explicit sparse f, h, supplied μ or checked Gram.
- `thm:upper-monotone`: same at the zero of a strongly monotone map; Jacobian Gram format.
- `lem:separation`: |α| ≥ 2^{-2τ d^{c_0 s}} for s ≥ 1 quantified variables, degree d ≥ 2, coefficient bit size τ. Used with s ≤ k, d = 4 (giving G(k) = 2·4^{c_0 k}, hence F(k) = 2^{O(k)}), and with s = n+m for the KKT formula of the transfer theorem. The case s = 0 is handled directly.
- `lem:newton-circuit`: part (b) with L' = M in unary for the normal-cone test of the VI verifier; part (a) for gradients. The uniformity over all observables of encoding length at most L' is essential. Please keep part (b) for strongly monotone maps.
- `thm:posslp-closure`: (b) adaptive form, whose hypothesis "halts within a polynomial number of steps on every input and for all oracle answers" is met by clocking; (c) Boolean form.
- `cor:upper-two-minima`, `prop:upper-slack-gap`, `lem:denominator-clearing`, `def:models-circuits`, `lem:models-det-trace`, `lem:models-strong-convexity`.
- `lem:convex-value` (contract E1): exactly feasible rational point with value gap at most ε ∈ (0,1] on a nonempty rational polyhedron inside a supplied box, time polynomial in L and log(1/ε). Every call in my proofs supplies an explicit box, and every accuracy is capped by one.
- `thm:quartic-complete` (value-test hardness for certified quartics) and `thm:rational-optimizer` (reduction from PosSLP to p_j > 0 with promises (i)–(iii)); the binary corollary uses exactly these promises.

`cor:structured-single-sign`: Section 3 earlier defined the same label; it now only references it. If any duplicate reappears, keep the Section 5 copy (root assignment) and the compiler in Section 3.

## 3. Labels exported

Section: `sec:constraints`, `sec:constraints-setting`, `sec:constraints-general`, `sec:constraints-nonlinear`, `sec:constraints-newton`, `sec:constraints-rank`, `sec:constraints-integer`, `sec:constraints-open`, `tab:constraints-summary`, `lem:constraints-polyhedral`, `thm:constraints-unambiguous`, `rem:constraints-unambiguous`, `def:constraints-nonlinear-dimension`, `lem:constraints-essential`, `thm:constraints-nonlinear`, `ex:constraints-rank-one-quartic`, `rem:constraints-psd-certificate`, `rem:constraints-nonlinear-prior`, `def:constraints-qp-solver`, `lem:constraints-newton-step`, `thm:constraints-transfer`, `cor:constraints-boxes`, `cor:constraints-flows`, `cor:structured-single-sign`, `thm:constraints-rank`, `lem:constraints-integer-cut`, `thm:constraints-candidates`, `cor:constraints-selection`, `thm:constraints-mixed-candidates`, `cor:constraints-nonlinear-mixed`, `thm:constraints-mixed-rank`, `cor:constraints-mixed-unambiguous`, `cor:constraints-binary`, and equations `eq:constraints-*`.

Appendix: `app:constraints` and its subsections, `lem:constraints-radius`, `lem:constraints-support-test`, `lem:constraints-circuit-lp`, `lem:constraints-cone-test`, `lem:constraints-elimination`, `lem:constraints-truncation`, `lem:constraints-admissible`, `lem:constraints-box-qp`, `lem:constraints-artificial`, `lem:constraints-violator`, `lem:constraints-rank-primitive`, `thm:constraints-integer-query`, `lem:constraints-gradient-cut`, `lem:constraints-padding`, `lem:constraints-residual-cut`.

Architecture differences: `prop:constraints-active-gap` was replaced by `prop:upper-slack-gap`. New labels: `cor:constraints-selection`, `cor:constraints-nonlinear-mixed`, `cor:constraints-mixed-unambiguous`, `cor:structured-single-sign`.

## 4. Macros

No new macro is required. The files use `\PosSLP`, `\NP`, `\rank`, `\Span`, `\diag`, `\tr`, `\poly`, `\bits`, `\argmin` from `macros.tex`, and inline `\mathrm{UP}`, `\mathrm{coUP}`, `\mathrm{coNP}`, `\mathrm P`, `\operatorname{cone}`. Optional shared macros if the root wants uniform class names: `\newcommand{\UP}{\mathrm{UP}}`, `\newcommand{\coUP}{\mathrm{coUP}}`.

## 5. Citation keys

Already in `references.bib`: `AllenderEtAl2009`, `Carlini2006`, `GroetschelLovaszSchrijver1988`, `KannanRademacher2009`, `KozlovTarasovKhachiyan1980`, `LeeSunSaunders2014`, `MittalSchulz2013`, `PangHan2023`, `Vegh2016`.

New keys for Luna to vet and add (exact contracts used are stated in the appendix):

- `GaertnerMatousekRuestSkovron2008`: Gärtner, Matoušek, Rüst, Škovroň, *Violator spaces: structure and algorithms*, Discrete Appl. Math. 156 (2008); arXiv cs/0606087v3. Used: Definitions 6–7 and 19, Primitive 22, Theorem 27, Sections 4.2–4.5; first argument of every violation test has size at most δ (returned bases, or subsets of size at most δ and one-element deletions in the base routine); O(δ log m) doublings per reweighting call. The introduction cites the same work as `GaertnerMatousekRustSkovron2008`; one key should be chosen.
- `AriHildebrand2026`: arXiv 2609.18266v2, Definition 3.4 and Theorem 3.5 (deterministic integer feasibility with integer-point separation; closed convex S in [-R,R]^t; empty and one-point S allowed; original coordinates; time bound with oracle cost Φ).
- `HildebrandGoess2024`: arXiv 2409.05308v2, Theorem 9 and Appendix B.
- `Basu2023Integers`: A. Basu, *Complexity of optimizing over the integers*, arXiv 2110.06172v6 (and its journal version), Theorem 5.7, Remarks 5.9–5.11 (no-bisection idea credited).
- `HildebrandKoeppe2013`: Hildebrand, Köppe, *A new Lenstra-type algorithm for quasiconvex polynomial integer minimization with complexity 2^{O(n log n)}*, Discrete Optim. 10 (2013); arXiv 1006.4661v3, Theorem 1.1 specialized to linear constraints and a constant objective.
- `DelPia2023`: A. Del Pia, *Convex quadratic sets and the complexity of mixed integer convex quadratic programming*, arXiv 2311.00099v2 (and journal version), Theorem 3 with zero objective (FPT mixed-integer linear feasibility with a rational witness).
- `GranotSkorinKapov1990`: Granot, Skorin-Kapov, Math. Program. 46 (1990) 225–236 (boundary discussion only).
- `OertelWagnerWeismantel2014`: Oertel, Wagner, Weismantel, *Integer convex minimization by mixed integer linear optimization*, Oper. Res. Lett. (2014). Credit only; text says its oracle contract differs, per Luna's note that the accepted text was not retrieved.

Contracts that Luna should confirm: GLS Theorem 6.6.3 (optimal vertex; operation count polynomial in the constraint matrix encoding, independent of objective and right-hand side; roundings implemented by comparisons on bounded ranges), KTK (exact rational minimizer of a convex quadratic attaining its minimum on a rational polyhedron), Végh Theorem 20 and Section 6.1 (capacitated quadratic case, O(m^4 log m) elementary operations and comparisons in the model of p. 1729). Lee–Sun–Saunders, Pang–Han, and Carlini are credited, but the needed statements are proved in the paper.

## 6. Response to `evidence/reviews/prewrite-constraints.md`

- Exact-feasibility contract: every approximation call is through contract (E1), stated with exact feasibility; the proofs use the constrained first-order inequality, not only objective error.
- min(1, ε) caps: used in every call (nonlinear dimension, transfer warm start, gradient cuts, residual cuts). The residual multiplier problem is solved exactly by (E3b) because no a priori box is available for its minimizers; the attainment argument is retained.
- 2^{O(t log(t+1))} is claimed only for unrestricted fibers; mixed constraints use F(t)L^C.
- Every-basis argument: `lem:constraints-violator`; the final-support caveat is in the main text.
- Total candidate encoding (not count) is charged in all compositions (Q_L).
- Rank 2r and nonlinear dimension 2k are carried through product fibers.
- Reduced curvature modulus ν = μ det(D^T D)/tr(D^T D)^{s-1} is now part of `thm:constraints-nonlinear`(iii).
- The two box-QP derivations (comparison-matrix admissibility by a Jacobi contraction, and the parametric pivot proof including ties, zero slopes and degeneracy) are included as `lem:constraints-admissible` and `lem:constraints-box-qp`.
- The distinctions between implicit optimizers and rational-circuit iterates, and among nonadaptive batches, Turing reductions, and single many-one instances, are explicit throughout.
- The artificial-cost argument of the flow review is included as `lem:constraints-artificial`, generalized to capacitated networks, with any M_0 > (N_0-1)C_0.

## 7. Response to `evidence/reviews/composition-sign-closure.md`

`cor:structured-single-sign` is stated after `cor:constraints-flows` for one requested predicate and for polynomial Boolean combinations; the active mask is a nonadaptive list of compiled single instances; parameterized compositions give FPT many-one reductions only; Las Vegas rank sampling and the UP certificate are not compiled; no subclass hardness, completeness, or ordinary solver is claimed. The proof checks the hypotheses of `thm:posslp-closure`(b): deterministic, worst-case polynomial time and query length independent of expanded circuit values, totality by syntax checks and a clock, valid queries even when a promise fails.

## 8. Corrections and changes relative to the source notes

1. The dense graph-Laplacian example: the source's implicit identification of nonlinear dimension with the rank of the edge vectors is not used; the text proves k = n-1 for a star with positive weights.
2. Flow curvature check: the valid quadratic test is "α > 0 and 4αγ_0 ≥ β^2, or α = β = 0 ≤ γ_0".
3. The transfer theorem no longer assumes a bounded polyhedron: the Hessian-Lipschitz constant is taken on a box of radius R_0+1 from the coercivity radius, and the iterates stay within 1/2 of p.
4. The remark on why ordinary approximation fails to find the active set no longer asserts that doubly exponentially small slacks occur; it says the separation bound does not exclude them.
5. The mixed residual quadratic program uses exact convex QP rather than value approximation (no box available for multipliers).
6. In the candidate lists the radius is an integer R ≥ 2, as the integer-query theorem requires; domain answers are the first violated inequality of Q ∩ [-R,R]^t in a fixed order.
7. Added `lem:constraints-padding` (preserved from the fixed-integer source) and the new composition `cor:constraints-mixed-unambiguous`.
8. Corollary M5 states the known optimal value 1/4 (the coverage map says "minimum zero"; subtracting 1/4 gives that form).

No source result was found invalid. The unrestricted constrained question remains open and is presented as such.

## 9. Checks actually run (targeted; not CI)

- Standalone build of `macros.tex` + Section 5 + Appendix D + `references.bib` with pdflatex/bibtex in `/tmp/constraints-build`: no LaTeX errors; undefined references only to labels in other files; undefined citations only for the new keys of §5; one 1.5pt overfull line.
- `python3 verification/check_manuscript.py` from the paper directory: no errors attributed to my files except the 8 missing bibliography keys above (the remaining errors belong to files of other authors or missing files).
- `git diff --no-index --check /dev/null` on both files: no whitespace diagnostics.
- No experiment, mathematical checker, project-wide verification, or CI inspection.

## 10. Requests and open items for the root

- Add the new bibliography keys after vetting, and unify the violator-space key.
- Keep `lem:newton-circuit`(b) and `thm:posslp-closure`(b),(c) in their present forms; Section 5 relies on them.
- The introduction and discussion should describe Section 5 as: UP^PosSLP ∩ coUP^PosSLP in general; one PosSLP instance under a supplied slack gap and for structured boxes and flows; ordinary FPT in nonlinear dimension; Las Vegas FPT in constraint rank; ordinary candidate lists with nonadaptive or structured selection; a PosSLP-hard binary decision at a known optimum; the deterministic arbitrary-polyhedron case open.
