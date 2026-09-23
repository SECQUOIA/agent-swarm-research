# Research closeout and verification record

Date: 2026-09-04. The user requested completion of the work already underway and
then a stop. This record distinguishes completed mathematical results from
explicitly open research questions. It supersedes intermediate progress labels
in historical log entries. The [README](../README.md) indexes the full program;
the [research assessment](research-status.md) ranks its likely impact.

Independent reviews in this repository are checks by other research agents.
They are not external peer review, formal proof-assistant certification, or
proof of publication priority. Canonical result files state their assumptions,
proofs, source comparisons, and mathematical limitations.

## Final batch: completed proofs and reviews

| Result | Final mathematical statement or scope | Verification record |
| --- | --- | --- |
| [Positive-box gap](../results/positive-multilinear-positive-box-sharp.md) | `max{2,rho} <= C_box(rho) <= rho+2`, all strictly positive boxes with maximum aspect at most rho; degree and dimension unrestricted | [First final audit](review-positive-box-rho-plus-two.md), [second final audit](review-positive-box-rho-plus-two-second.md), [separate lower audit](review-positive-multilinear-positive-box-lower.md) |
| [Finite-dimensional orientation refinement](review-positive-box-balanced-orientation-closure.md) | Upper bound `rho+beta_N`, with `beta_N=2-2/N` for even N and `2-2/(N+1)` for odd N | Complete restricted-law coefficient proof and independent audit in the linked note; root reread passed |
| [Exact width-two gap](../results/positive-multilinear-treewidth-two-exact.md) | Sharp constant two, two-TU-row partition, convex-cardinality extension, and sharpness on every fixed common-aspect positive box | [First audit](review-multilinear-treewidth-two-coloring.md), [second audit](review-multilinear-treewidth-two-second.md), [novelty screen](multilinear-treewidth-two-novelty.md) |
| [Universal CIA heavy-mode theorem](../results/cia-universal-heavy-mode-rounding.md) | Analytic rounding at error E when `T <= (s+2)E` and some terminal mode mass exceeds E; exact full-to-one-sided minimax identity for every `1<=k<n` | [Full proof and identity audit](review-cia-universal-heavy-mode.md), including exact independent construction checks |
| [Arbitrary-budget CIA bound](../results/cia-arbitrary-switch-global-bound.md) | All-profile upper bound, exact plateau for `k+1<=n<=k(k+1)/2`, and sharp first `1/n` correction for every fixed budget | Same final transfer audit; [one-sided dependency audit](review-cia-arbitrary-block-one-sided.md) |
| [Exact three-switch CIA](../results/cia-exact-three-switch-worst-case.md) | `T max{1/5,1/[n((n/(n-1))^4-1)]}` for `n>=5` | [General reach/certificate audit](review-cia-general-four-block.md), [analytic heavy-mode audit](review-cia-three-switch-heavy.md), [transfer audit](review-cia-exact-three-switch-transfer.md) |
| [Single positive monomial and rank-one transport](../results/positive-box-single-monomial-hardness.md) | Exact narrow-box envelope and graph-hull membership are NP-complete; positive rank-one transport/AMIN has a logarithmic-precision bit-complexity barrier unless P=NP | [Reduction audit](review-positive-box-single-monomial-hardness.md), [dedicated precision/source audit](review-rank-one-mot-precision.md), [completed later-literature check](rank-one-mot-precision-later-literature.md) |
| [P-split coordinate effect](common-factor-p-split-rotation-gap.md) | Rational coordinate change turns the tightest chosen auxiliary-image convexification from unbounded error into an exact hull, with the full domain transformed | [Final audit](review-common-factor-p-split-rotation-gap.md), including the strongest auxiliary-only obstruction and conic repair |
| [Auxiliary forest/compression lemmas](multilinear-treewidth-two-investigation.md) | Canonical-pair forest gluing and identical-neighborhood compression, with exact scope and gap identities | [Closing independent audit](review-multilinear-treewidth-two-elementary-lemmas.md); neither lemma is needed by the canonical width-two theorem |

The last positive-box refinement initially had a missing restriction argument.
It was completed during closure: fix one ambient balanced-orientation law and
retain it under every deletion. Pair probabilities remain unchanged; no
conditioning on deleted orientation coins occurs. This resolved the specific
proof obligation and removed the unreviewed label. It does not settle the exact
finite-dimensional optimum.

The [coefficient development note](positive-box-rho-plus-two-proof.md) also retains
a checked optimality statement for fixed mixtures of independent and fair
endpoint-orientation rounding, and a coefficient-regularity consequence for
cardinality potentials. Root reread the latter summation: the nonnegative
independent deficiencies and `a_(j+1)<=L a_j` give factor `L+3`. These statements
have their stated restricted scope; neither proves that `rho+2` is the true
worst polynomial ratio.

## Earlier completed results remain available

The README links the reviewed degree/dimension asymptotics, joint parameter
characterization, marginal-floor theorem, explicit cubic witnesses and upper
bound, frequency-two and convex-cardinality results, feedback-variable bound,
rank-one hardness and conic lower bounds, FBBT results, common-factor hulls,
integer-anchor separator, pooling consequences, and network–simplex results.
Their individual audits remain the detailed evidence; this closeout does not
replace their assumptions with a blanket claim.

The final quantitative positive-box upper bound supersedes the coarse and
asymmetric upper estimates. Those proofs are preserved as valid alternatives,
with working links and explicit predecessor status. Exact CIA results similarly
supersede older partial upper bounds; current headers now link the completed
results while historical derivations are retained.

## Verification artifacts and reproducibility

Mathematical arguments, not numerical searches, justify the universal analytic
statements. Exact searches and independently constructed certificates provide
additional checks where appropriate. Significant final records include:

- [Positive-box coefficient checker](../code/audit-positive-box-coefficients.py):
  1,589 exact rational cases, including coefficient/spreading checks and the
  counterexample to a stronger Schur-concavity assertion.
- [Independent heavy-mode checker](../code/cia_tv_conjecture/audit_universal_heavy.py):
  1,415 exact cases. The [author construction](../code/cia_tv_conjecture/universal_heavy_certificate.py)
  checked 1,612 cases, including 703 prefix uncrossings.
- [General four-block certificate checker](../code/cia-distinct-reach/verify_general_four_block.py):
  179 finite certificates and ten symbolic polynomial certificates. The separate
  audit checked the symmetry quotient, inequality meanings, and reconstruction;
  a successful matrix calculation alone was not treated as proof of that reduction.
- [Single-monomial verifier](../code/audit_single_monomial_hardness.py): exact
  rational PARTITION and tilted-objective checks, with model/accuracy limits in
  the two independent audits.
- Treewidth-three experiments and their exact finite records are indexed in
  [the closed investigation](multilinear-treewidth-three-investigation.md).
  Passing those finite searches is explicitly not a theorem for all graphs.

The closing repository check parsed all 32 changed or new Python files without
syntax errors, checked local document/artifact links across 194 Markdown files
with no missing targets, and passed `git diff --check`.
Existing successful mathematical checks were not repeatedly rerun without a
new proof obligation. The code has not been represented as a production solver
library or a single comprehensive automated test suite.

## Open questions retained, not unfinished theorem claims

- Exact fixed-rho positive-box constants, exact cubic ratio, and matching
  second-order degree/dimension asymptotics.
- Exact constants or balanced/TU row partitions beyond incidence treewidth two;
  the width-three and planar leads remain conjectural. The all-cycle coloring
  route has a recorded obstruction on `K_(3,m)`.
- General unequal-aspect frequency-two constants. Common-aspect results are
  proved; they do not silently extend to all positive boxes.
- Exact finite-mode one-sided CIA values beyond four blocks, and the resulting
  full minimax values outside proved ranges; general finite-grid formulas.
- The largest-heavy-mode adjacent-repeat variant. The proved universal theorem
  only needs the first repeated mode of an appropriate rounded word; a stronger
  specified-mode version is false and its counterexample is saved.
- Stronger approximation-hardness regimes and definitive publication priority.
  The proved precision and geometric error scales must be preserved.

No open question in this list is used as a premise of a verified theorem.
Useful abandoned routes, correct negative results, and classical rediscoveries
remain in the repository with their status made explicit.

## Repository state

Proofs, reviews, experiments, and useful negative findings have been saved in
`results/`, `notes/`, and `code/`. Literature summaries remain in the existing
`literature/` folder, which is excluded from version control by repository policy.
No commit, external submission, or publication was made. Files marked untracked
by Git are still present locally; the working tree contains the saved research.
All research-agent assignments were closed after their final records were saved.
