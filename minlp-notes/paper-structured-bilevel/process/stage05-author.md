# Stage 5 author record

Date: 2026-09-07. Scope: structural and arithmetic boundaries and the distinct
conditioned dense-box approximation algorithm. This authored stage is complete
and awaits the required five independent reviewers. No reviewer delegation or
stage 6 work was performed.

## Files and integration

- `sections/05-boundaries.tex` contains all stage 5 main results and complete
  proofs, with a proof of the classical maximum-minor normalization and an
  elementary exact rational inner-QP oracle.
- `appendices/d-path-geometry.tex` contains the exact cited sparse-shadow edge
  proof, message/degree lower bounds, telescoping vertex polynomial, slab and
  padding proof, and equal-gain path/forest/fixed-total-cycle-rank projection.
- `main.tex` includes those files; `references.bib`, `README.md`, and
  `process/coverage.md` provide bibliography, reproduction commands, and exact
  source-to-label mappings.
- `verification/stage05-author/` contains eight distinct existing diagnostic
  logs, one additional exact diagnostic and its log, build logs, two rendered
  inspection pages, and command/input/artifact manifests.
- All four accepted section files and all three accepted appendix files are
  byte-for-byte unchanged from the stage04-accepted snapshot; the check is
  recorded in `artifacts.json`. Root-owned status, assessments and snapshots
  and all unrelated repository work were preserved.

## Mathematical development and decisions

The initial unconditioned dense reduction is retained in full: ternary leader
witnesses, strict base-gradient margins, clause-shortfall feedback, the final
2n+m follower construction, and its zero-versus-two objective gap with no
response upper constraints. Conditional minimization proves the minority and
shortfall readout at every response. The earlier redundant symmetric auxiliary
coordinates are unnecessary because y-clip(2y-1) is already the minority distance.
The sum-of-squares representation is jointly convex; the normalized expression
obtained by deleting a leader-only term need not be. “Q independent of the
leader” explicitly means an input matrix, not a universal matrix shared by all
instances.

The near-identity reduction is a separate theorem with a separate small gap.
Its network is bounded at every continuous leader, its matrix is triangular,
and the relative-coordinate inequality controls each u_i/s_i rather than only
the tiny absolute u_i. The inverse positive triangular matrix, feedback norm,
readout error, polynomial rational scales, coefficient bounds, and simultaneous
1/infinity/2 near-identity bounds are all proved. Shrinking the coupling also
shrinks the gap. Exact NP-hardness is not presented as strong hardness or an
inverse-polynomial absolute-gap result.

The conditioned approximation proof includes equality-inclusive saturation,
zero-cost rows that must remain unfrozen, lower-dimensional cells, a maximum
volume row basis, bounded cost-coordinate intervals, and exact minimization of
the direct leader term. It explicitly covers N=0, r=0 and zero response readout;
the last case still evaluates the promised follower. The inner oracle uses
projected-gradient contraction, an integer determinant denominator bound,
continued-fraction recovery and an exact KKT check. Its runtime is polynomial
in the numerical condition estimate K, matching the outer theorem. No classical
convex-QP black box or numerical active-set guess is needed for this proof.

The parameterized classification is credited to Froese–Grillo–Hertrich–Stargalla.
The capped-ReLU transfer preserves the parameter, polynomial size, constant gap
and support on at most two leaders. Polynomial duplication bounds coefficients
without incorrectly replacing clip(h) by a rescaled clip(h/R). The independent
mixed-radix construction contains its full continuous rounding gap.

The bounded-core algorithm enumerates affine local vertex candidates and all
relative core cells. Closure LPs remain sound even when another candidate first
becomes feasible on the boundary; completeness comes from the separate cell
containing an optimal core. The weak Subset Sum path reduction and both message
identities are explicit. The identical-factor fixed-alphabet family has a
trivial zero optimum, so only its explicit message size is a lower bound.

The follower-constraint path is kept separate from that leader interaction path.
The precise Gärtner–Helbling–Ota–Takahashi price/exposure formula is proved from
its edge directions; pointwise backward evaluation remains linear in arithmetic
operations. The unextended polynomial-description obstruction is a sum-of-degrees
lower bound from distinct boundary line factors, not an arithmetic-circuit or
pointwise-optimization lower bound.

The diagonal follower vertex lemma compares against every point of the cube via
convex combinations of vertices. The explicit squared terminal separation
preserves exact vertex optimality under a positive diagonal regularizer and on
nontrivial price intervals. Identity scaling preserves this response. The
NP-completeness proof includes the nonconvex upper quadratic row and the slab;
slab-only feasibility holds for every target, so this argument does not prove
all-linear-upper feasibility hardness.

Two modest extensions were developed and fully proved during this stage:

1. **Fixed local alphabet for the bilevel path theorem.** The earlier padding
   lemma is lifted to the scalar-leader diagonal/identity-Hessian follower.
   Every needed free-bit vertex belongs to the full unpadded cube, and its
   proved strict response inequality holds throughout that larger cube. It
   therefore survives restriction by the padding bounds. The vertex polynomial
   conversely forces every padding bit to be zero. Dimension is polynomial in
   n and log W, and all local follower inequality data lie in fixed alphabets.
   Binary aggregate weights and rescaled costs remain unrestricted in magnitude.
2. **One power follower and sparse-degree output.** With polynomial upper
   objective (z-1/2)^2 and error 1/64, or affine objective z with row z>=1/2 and
   error 1/8, every acceptable rational leader is positive and at most (5/8)^P.
   Its denominator therefore needs Omega(P) bits. The latter has a strict anchor
   and a convex reduced row. These statements do not settle the one-power,
   affine-objective/no-upper-row subclass. The existing two-power example is
   reused by reference.

The full equal-gain strip proof handles negative gains, zero-edge cuts with
bounds at the original head, multiple bound candidates, arbitrary tree
orientation, and fixed *total* cycle rank. Unique-path distances and the minimum
formula prove both necessity and recovery. Polynomial products are expanded
only in fixed parameter dimension; witnesses use rational functions and minima
inside one existing field. Unbounded or nonclosed parameter domains retain the
infimum/attainment distinction. Dense eliminated-state objectives are excluded.

Finally, both curvature 3SAT examples are explicitly optimistic feasibility.
The root-sum degree argument is proved by induction using independent sign
characters and rational prime valuations. Uniformly positive-curvature cubic
followers and convex singleton quadratic leaves are both included. Exponential
common-field output degree and exact Square Root Sum comparison are distinguished
from NP-hardness and from succinct radical expressions. Sparse upper equation
x^(2^t)=2 gives a separate exact algebraic-degree obstruction by Eisenstein.

## Repository sources examined

All four canonical stage 5 results were read in full:
`bilevel-scalar-leader-spd-box-np-completeness`,
`bilevel-well-conditioned-box-exact-hardness`,
`bilevel-conditioned-box-additive-algorithm`, and
`bilevel-leader-vertex-integrity-boundary`.

All named note-only proof dependencies in the assignment were read:
`bilevel-dense-box-no-upper-constraints-extension`,
`bilevel-diagonal-leader-dimension-boundary`,
`bilevel-diagonal-box-parameterized-hardness-source-audit`,
`bilevel-leader-vertex-integrity-source-audit`,
`parametric-path-lp-obstructions`, `parametric-path-lp-investigation`,
`klee-minty-rank-one-slab-hardness`, `klee-minty-diagonal-follower-bilevel`,
`parametric-affine-strip-path-projection`, and
`fixed-core-convex-leaf-arithmetic-barrier`, together with the scalar exact
canonical source's Section 6. The dense, conditioned-hardness and conditioned
approximation novelty audits and linked focused mathematical reviews/addenda
were inspected for prior-source and scope issues. Historical PASS labels were
not used as proof authority. No source-result correction was required.

## Primary-source checks and attribution

`literature/AGENTS.md` was read. Generated literature metadata was not edited,
and no user-supplied original was redistributed. The manuscript has its own
bibliography. The following primary texts/locators support the used claims;
external access failures are distinguished from full-text inspection.

- Mairal–Yu, *Complexity Analysis of the Lasso Regularization Path*, ICML2012,
  https://arxiv.org/pdf/1205.0079v2. Local original and extracted text inspected,
  especially Proposition2/equation(4) and the invertible triangular recursion.
  The normalized dual box consequence is explicitly an inference from this
  construction and duality; no polynomial-bit hardness follows from path length
  alone.
- Sugishita–Carvalho v2, https://arxiv.org/html/2510.21126v2,
  Theorem2.1 and Section4. This primary dependency was checked during the prior
  stages; the scalar ternary-coding and gap antecedent is credited again.
- El Ghaoui et al., *Implicit Deep Learning*, SIAM J.Math.DataSci.3(3),930–958
  (2021), DOI10.1137/20M1358517. Inspected author primary PDF
  https://arxiv.org/pdf/1908.06315, equations(2.6)–(2.7) on PDFp8, and the
  SIAM publisher metadata. Positive diagonal similarity/prediction preservation
  are credited. One attempted arXiv HTML URL failed; the PDF succeeded.
- Zach–Estellers, *Contrastive Learning for Lifted Networks*, BMVC2019,
  https://arxiv.org/pdf/1905.02507, Section2, equations(2)–(4), PDFpp2–3:
  convex squared-residual energies and weak feedback. The reduction's explicit
  relative-coordinate bit estimate is proved separately.
- Awerbuch–Kleinberg, STOC2004,
  https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf, Section2.3,
  Definition2.1 and Proposition2.2, PDFp4. The exact determinant-replacement
  argument is the basis normalization used here.
- Giesen–Jaggi–Laue, *Approximating Parameterized Convex Optimization Problems*:
  inspected primary author manuscript https://www.m8j.net/math/approxPaths.pdf,
  Definition1 and Corollary10 (PDFp12) with its geometric/parameter factors.
  The bibliography gives the published ACM Trans.Algorithms9(1),article10
  (2012), DOI10.1145/2390176.2390186; direct ACM page retrieval failed, so the
  mathematical comparison is based on the inspected 2010 author manuscript.
- Giesen–Müller–Laue–Swiercy, NeurIPS2012,
  https://papers.neurips.cc/paper_files/paper/2012/file/bdb106a0560c4e46ccc488ef010af787-Paper.pdf,
  Lemma4/Theorem5, PDFp3. The additive path bound retains parameter range and
  slope variation. Primary proceedings author order and metadata were checked.
- Bemporad–Filippi, CDC2001, pp4851–4856,
  https://cse.lab.imtlucca.it/~bemporad/publications/papers/cdc01-sub-mpqp.pdf,
  Section4.6/Theorem4, PDFp5: uniform optimizer error by approximate KKT regions.
- Froese–Grillo–Hertrich–Stargalla,
  https://arxiv.org/pdf/2509.22849v3 (September3,2026), local original and
  extracted text: Proposition4.1 (pp10–12), Theorem5.3 (p14), and Corollary5.5
  with bounded-box argument. The statement and transfer are attributed, not
  presented as a new W[1]/ETH classification. The independent mixed-radix proof
  avoids copying the piecewise spike typography flagged in root's source audit.
- Dvořák et al., Artificial Intelligence300:103561 (2021),
  DOI10.1016/j.artint.2021.103561; primary publisher/institutional abstract
  confirms the few-global-variables decomposition context. Only this broad
  relationship is cited; none of its ILP theorems is imported into our proof.
- Meuleau–Morris–Yorke-Smith,
  https://homepage.tudelft.nl/0p6y8/papers/n58.pdf, Lemmas1–2 and Theorem1,
  PDFpp3–4. The primary author's publication page identifies the CP/ICAPS2008
  joint workshop venue. Closure of continuous piecewise linear elimination is
  credited, while intermediate output size is analyzed independently.
- Gärtner–Helbling–Ota–Takahashi,
  https://arxiv.org/abs/1308.2495, local original PDF Section4, especially
  Definition11/Lemma12 on printedpp8–9. A layout-preserving PDF extraction
  verified the exact powers and parity products hidden in the repository's
  Markdown extraction. The complete used edge proof is reproduced with credit.
- Pardalos–Vavasis, Journal of Global Optimization1:15–22 (1991),
  https://link.springer.com/article/10.1007/BF00120662. Primary publisher
  abstract/metadata checked; subscription full text not accessed. Only its
  broad rank-one-concave hardness statement is cited; all specialized slab and
  bilevel arguments are proved here.
- Eisenbrand–Haeberle–Singer, SoCG2024,
  https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2024.54.
  Primary abstract and metadata checked for the exact Square Root Sum open
  problem. Its separation-bound theorem is not used as an effective uniform
  algorithmic bound.

## Exact diagnostics and build

`python paper-structured-bilevel/verification/stage05-author/run_checks.py`
from the repository root ran the following distinct checks; all exited zero.
The manifest retains exact commands, SHA256 hashes, elapsed times and log names.

| Check | Actual outcome |
| --- | --- |
| `code/bilevel_dense_box/second_review_checks.py` | 510 Boolean KKT certificates, 8 earlier midpoint identities, 1,000 literal/readout cases, 1,008 final clause-feedback certificates and 125 no-upper-row gap cases. |
| `code/bilevel_dense_box/check_conditioned_hardness_first_review.py` | 42 exact follower KKT/error/gap cases from 390 rational active systems. |
| `code/bilevel_response/check_conditioned_additive_second.py` | 60 maximum-minor basis cases; seven scalar global comparisons, 25 true affine pieces and 299 grid candidates. |
| `code/bilevel_vertex_integrity/check_structure_and_path.py` | 521 exact path arrangement vertices across four instances and three independent core comparisons. |
| `code/bilevel_parameterized/check_mixed_radix_gap.py` | 1,000 exact continuous gap samples, 630 triangle checks and normalized ramp identities. |
| `code/parametric_path_lp/exact_shadow_check.py` | 8,190 exact vertex witnesses and 8,178 ordered breakpoints, dimensions1–12, including independent backward evaluation. |
| `code/parametric_path_lp/exact_diagonal_follower_check.py` | 1,530 strictly positive KKT certificates and 3,060 regularized convex-combination inequalities. |
| `code/parametric_path_lp/check_affine_strip_projection_review.py` | 1,200 exact projection comparisons:635 feasible/565 infeasible;707 zero-gain/983 negative-gain cases; all witnesses verified in original coordinates. |

The additional script `check_padding_and_recovery.py` independently checked the
new padded response scope against every vertex of each full cube, and compared
the rational gradient oracle against exact original-coordinate active-face
solutions. Its 14,240 directional inequalities, 21 target/slab equivalences and
five rational-recovery cases (526 exact iterations) all passed. No further
mathematical diagnostics were broadened after those passed.

The final command
`latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`
completed successfully and produced a **63-page** `build/main.pdf`. The final
LaTeX log contains no warnings, overfull/underfull boxes, unresolved citations
or references. Rendered pages35 and59 were visually inspected, including the
split network equations and the strip proof. Two initial file-write commands
used a duplicated paper path from the paper working directory and failed before
writing; corrected absolute paths were then used. This did not change unrelated
files. The initial bibliography-free compile was superseded by the clean final
build. `artifacts.json` records final manuscript/PDF/check hashes and preservation
of the accepted mathematical files.

The finite diagnostics are not implementations of general quantifier elimination,
proofs of a complexity theorem, or solver-performance experiments. Stage6's
executable convex/nonconvex algorithms, contact reconstruction, independent full
bilevel baseline and computations remain to be authored after this stage's gate;
stage7 synthesis and the full five-reviewer manuscript gate also remain.
