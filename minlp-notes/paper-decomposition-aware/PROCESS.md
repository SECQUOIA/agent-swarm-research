# Development and review process

The manuscript rewrites the October 2 technical report
`research-20261002-decomposition/document/` as a self-contained journal paper.
Every result kept in the paper has a complete proof in the paper; no proof
depends on repository notes.

## Stages

| Stage | Work | Records |
| --- | --- | --- |
| W1: verification and extraction | Ten agents: seven adversarially re-derived every result cluster of the report (core grids, exact output, convex recourse, cut recourse, TU constraints, optimal sets, structural limits) and wrote self-contained proofs; two audited the literature against primary sources; one audited the implementation and ran new experiments | `process/w1/*-report.md`, `*-proofs.tex`, `lit-*.md`, `lit-*.bib`, `checks/` |
| Assembly | The coordinator verified the core proofs line by line, integrated the fragments with one notation, wrote the introduction, related work, setting, computation and conclusion, and ran the expanding-box chain experiment | `sections/`, `experiments/chain/`, `process/fragments/` (raw fragments), `process/*-draft-v0.tex` (superseded drafts) |
| W2: first independent review | Nine reviewers: four on mathematical correctness by section group, one on global consistency, one on writing, one on literature and novelty, one on the computational claims, one referee-style report; 222 findings | `process/w2/` |
| W3: first revision | Binding conventions (structure, notation table, algorithm names, wording of the complexity and scope claims); eleven file-owner agents, each followed by a verifier; every W2 finding decided (176 accepted, 45 modified, 1 rejected) | `process/w3/CONVENTIONS.md`, `process/w3/reports/`, `process/w2/ADJUDICATION.md` |
| W4: second independent review | Ten reviewers (five mathematical, four cross-cutting, one referee); an adversarial verifier for every critical or major finding. No mathematical error was found; the major findings were editorial (length, introduction, scope caveat, a missing prior-work comparison, the explanation of SCIP's primal bounds) | `process/w4/`, `process/w4/all-results.json` |
| W5: second revision | A cut plan moved secondary results and long proofs to appendices (main text from 80 to 70 pages, no result removed); ten file-group agents, each followed by a verifier; every W4 finding decided (53 accepted, 18 modified, 1 rejected) | `process/w5/CUTPLAN.md`, `process/w5/reports/`, `process/w4/ADJUDICATION.md` |
| W6: final check | Four fresh reviewers on whole-paper consistency, the dependencies of moved proofs, proofreading, and a final referee assessment. No critical or major correctness problem; one length item and about 30 minor items | `process/w6/` |
| W7: final fixes | Five file-owner agents, each followed by a verifier, applied the W6 items; the coordinator integrated, rebuilt and checked the result | `process/w7/reports/`, `process/w6/ADJUDICATION.md` |

"Reviewer" means an independent research agent, not journal peer review.
Finite exact-arithmetic checks support the proofs; they do not replace them.

## Main changes relative to the report

* All proofs are in the paper. Results whose proofs were in companion notes
  either received complete proofs (affine-selector recognition, mixed
  submodular certificate, TU heights and recovery, proximal generator,
  boundary output) or were dropped.
* The single-box interpolation inequality is credited to Bajaj and Hasan
  (2020) and to edge-concave and alphaBB underestimators; the new statement is
  that the corrected grid computes the best cellwise bound by one tree dynamic
  program.
* The growth analysis uses a weighted, scale-invariant condition number,
  simpler constants and a minimal path certificate. The scope of the growth
  hypothesis is stated precisely: minimality alone confines negative curvature
  to directions that involve active bounds or integer coordinates; growth adds
  a quantitative local bound and a global separation of other local minima.
* Exact output uses a stationary-polytope height lemma with Hadamard's
  inequality and a snapping procedure that needs no uniqueness. A localized
  acceptance test, which uses the filtering history, accepts much earlier in
  practice.
* New results developed during verification: lower bounds on the dependence on
  width and conditioning (ETH, rETH, P vs NP, value oracle), the failure of
  single-center grids with two minimizers and the uniform-cell remedy, the
  optimality of certified convex cancellation and its limit, cut-based grid
  oracles for balanced quadratics without a width parameter, the deterministic
  core-search count, the face constraint problem for coordinatewise concave
  quadratics, every-finite-order moment obstruction, and the intrinsic margin
  cost of boundary certificates.
* Prior work: the comparison with Hochbaum and Shanthikumar's proximity
  scaling, Bienstock and Muñoz's approximation scheme, and the cluster problem
  is made explicitly, each in one place.
* Structure: the core (Sections 3-6 and 10.1-10.3) is separated from the
  extensions (Sections 7-9); long proofs of secondary results are in the
  appendices, which follow the section order.
* A new computational study (`experiments/`) and the expanding-box chain run.

## Scope rules followed

Only targeted checks for this topic were run; no project-wide verification or
CI inspection. Unrelated dirty files and running experiments in the repository
were left untouched. No commit, upload or submission was made.
