# Stage 1 author record

Author: delegated stage author. Date: 2026-09-05.

## Delivered

- `sections/01-foundations.tex`: physical standard/generalized/cyclic models, quality and flow contracts, zero-flow semantics, cost distinctions, decision/output conventions, affine quality compression, physical rank-one block identity; full proofs of destination decomposition, single-product LP projection, sign detection, sparse shortest-path witness, output-count approximation and destination LP bound, exact uncapacitated conic hull; reviewed cyclic reconstruction/sign/conic extension; singular-cycle conditioning example; full facial-integrality characterization, recognition LP, fixed-pool/affine-dimension enumeration, and endpoint disjunction/MILP.
- `process/coverage.md`: result-by-result stage mapping; distinct developments hidden in investigation notes; superseded/failed routes; individually listed audit/source/history files and computational artifacts; adjacent rank-one/common-factor/network-simplex disposition.
- `process/foundations-sources.md`: citation keys, actual evidence inspected, and source version caveats.

## Independent mathematical checks and improvements

The draft was derived from the equations and rechecked, not mechanically converted from Markdown. In particular:

1. Product quality regions are imposed homogeneously, including empty allowed regions at zero flow. No positive contract is silently dropped. Threshold hardness is explicitly separated from feasibility.
2. Integral-optimum statements now explicitly assume feasibility. Branch deletions with positive lower bounds are rejected; a network branch cannot silently discard those requirements.
3. Network branch integrality receives a complete incidence-matrix determinant proof, and the node/return-arc construction explains the source/product throughput constraints.
4. The face enumeration algorithm is stated using fixed affine input dimension, the actual parameter used in the repository proof; this strengthens the wording from fixed attribute count without changing the proof. The affine coordinate reduction and face count are proved.
5. Cyclic reconstruction uses the positive-flow support. Singular isolated circulations receive constant qualities; the remaining rational system is nonsingular. No blanket invertibility claim is made and no criticism of an unchecked final published source is included.
6. A small completion proposed by root was independently checked and included: cyclic algebraic pooling also has the same output-count approximation and destination-LP inequalities when a product exists. Merge the isolated circulation into one destination component (disjoint positive support), then repeat the averaging proof. An additional compactness argument establishes optimum attainment even with source-free circulations; the no-product case remains minimum-cost circulation.
7. The rank-one identity explicitly distinguishes arbitrary input-product matrix objectives from additive physical feed/outlet costs.
8. Rational quality reconstruction is bounded using a single rational linear system and determinant estimates, rather than an unquantified repeated-arithmetic claim.

No unresolved mathematical blocker was found in the scope of this stage. This is an author assessment, not a replacement for the requested 15 independent reviews. Statements in later-stage source files have been inventoried and their known boundaries recorded; the inventory is not a claim that all those proofs have already been checked in full.

## Literature checks

Read `literature/AGENTS.md` before accessing the knowledge base. Inspected local Gupte et al. formulation and Remark 2.2; Boland et al. destination-commodity text and cyclic formulation discussion; Dey–Gupte actual open article retrieved by root; rank-one source association. The Dey local package contains slides despite article metadata, so article theorem attribution is based on root's separately retrieved article. Boland's local open artifact is the 2015 manuscript. No knowledge-base generated index or bibliography was edited.

## Verification

Ran `pdflatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp main.tex` from `papers/pooling`. Exit status 0; 10-page stage draft generated, with expected missing bibliography and first-pass cross-reference warnings. No overfull-box warning appeared. Main file and bibliography ownership remained with root.

Root separately supplied exact finite checks for cyclic decomposition, conditioning, and nonfacial witnesses, recorded in `root-foundations-check.md`. These supplement the proofs and are not presented as exhaustive mathematical verification.

## Later-stage follow-up

Root found and repaired analytically the irrational-example inequality in `code/pooling_degree_two/irrational_example.py`: its prose had omitted `(1+b)` in a denominator. Root also completed the missing global-optimality proof, obtaining exact optimum `-(5+sqrt(3))/2`. The example belongs naturally in stage 2 as a fully proved illustration of irrational optimal flow; the source code transcription should be corrected before its fresh verification run.
