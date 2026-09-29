# Reproducing the September 25 research results

This is the verification and provenance index for this research batch.
It distinguishes exact certificates, finite checks, numerical exploration,
and written proofs. The mathematical statements and their assumptions live
in the linked result notes; this index does not strengthen their claims.
Independent review here means another research agent's review, not journal
peer review. No project-wide verification or CI inspection is required or
reported.

Run the commands below from the repository root unless a different working
directory is given. Select the commands for the result being checked. Run
Python normally: `python -O` disables the assertions used by these scripts.
The exact Python checks need no optimizer, network connection, or private
data. Their rational inputs are included in the source files.

The environment inspected for this preparation was Python 3.13.11 on
Linux x86-64, with SymPy 1.14.0. `Fraction` checks use only the Python
standard library. Symbolic checks use SymPy's exact rational and polynomial
operations; they are not proof-assistant certificates. No minimum supported
Python version has been established. The direct script invocations below
also put each script's directory on Python's module path, which resolves
the two documented sibling imports without changing `PYTHONPATH`.

| Result and proof | Targeted reproduction commands | Evidence and limits |
| --- | --- | --- |
| [Three-variable strict SDP gap](three-positive-disjoint-counterexample.md) | `python research-20260925/checks/three_positive_gap_certificate.py`<br>`python research-20260925/verify_three_positive_disjoint_review.py`<br>`python research-20260925/check_three_positive_disjoint_counterexample.py` | Standard library, exact arithmetic. Checks all 27 strict-PD matrices, objective `-1/40`, all 12 edge minima, five zeros, and the stated rank/exclusion calculations. The first script also checks 24 SOC inequalities of type (15) and 48 of type (16) under the cited symmetries. Source matching, cube nonnegativity from the edge argument, and implications for named prior cuts use the written proofs. |
| [Infinite quadratic family and compact SDP](three-positive-family-sdp.md) | `python research-20260925/verify_three_positive_family_review.py` | SymPy. Checks the parameterized nonnegative decomposition, moment matrix identities, and rational violation. The equivalence with a PSD block of order five plus six nonnegative auxiliaries relies on the written cone argument and the classical order-four copositive identity, not sampled parameter values. See [proof review](three-positive-family-lmi-review.md) and [priority review](three-positive-family-priority-review.md). |
| [Exact-penalty encoding obstruction](parametric-exploration.md) | `python research-20260925/check_parametric_penalty.py`<br>`python research-20260925/parametric-penalty-review-check.py` | Standard library. Previously passed 72 and 800 exact finite cases, respectively. The all-dimension dual formulas have the separate Lean reproduction below. Binary encoding, finite-model correspondence, convexity, and Slater properties remain written arguments. See [proof review](parametric-penalty-review.md) and [literature review](parametric-penalty-literature-review.md). |
| [Penalty calibration hardness](minimum-penalty-hardness.md) | `python research-20260925/check_minimum_penalty_hardness.py`<br>`python research-20260925/check_minimum_penalty_review.py` | Standard library. Previously passed 976 binary-box and 75 graph cases, then an independently implemented 120 box cases and 480 dual values. The reduction, asymptotic inapproximability, and distinction between a smallest and a conservative sufficient penalty are proved in the note, not by enumeration. The second script uses fixed seed `825031`. |
| [Penalty upper bounds](penalty-upper-bound.md) | Written proof and [source audit](penalty-upper-bound-source-review.md), [general proof audit](penalty-upper-bound-review.md), and [fixed-quadratic-count audit](penalty-fixed-quadratic-count-review.md) | No persistent all-theorem computational checker or Lean proof. The bounds use effective real algebraic geometry; checking a few determinant identities cannot establish the elimination theorem or coefficient-height bound. The older 2009 source was superseded by the final 2010 source, as documented in the source audit. |
| [Smoothed exact penalties](smoothed-penalty.md) | `python research-20260925/check_smoothed_penalty_review_second.py` | Standard library, seed `250925`. Previously passed 363 piecewise-linear penalty cases, 150 box/grid cases, and 1,216 sharpness cases. The general convex-body tube bound, rational sampling guarantee, and conditioning on feasibility require the written proofs and [final review](smoothed-penalty-review-second.md). The earlier [review](smoothed-penalty-review.md) addresses an earlier geometric bound and does not supersede that final review. |
| [Rational star subset-accuracy lower bound](star-subset-accuracy-lower.md) | `python research-20260925/check_star_subset_accuracy.py`<br>`python research-20260925/check_star_subset_accuracy_review.py`<br>`python research-20260925/check_publication_star_parents.py` | The first uses exact `Fraction` arithmetic: five instances, 852 subset checks, and gap/mean/cost bounds. It imports `polygon` and `rotate` from `verify_star_rational_uniform.py`, so these two scripts are not independent implementations of the geometry. The second checks eight supports and the candidate cut symbolically, then 4,706 subsets using floating point. The third independently constructs 215 local laws with 1,964 positive definite rational pattern matrices and checks all marginals; it shares no geometry helper with the author. The all-order theorem and conditioning/encoding bounds rely on the [original independent review](star-subset-accuracy-review.md) and [fresh proof audit](publication-star-proof-review.md). |

The publication assessments for [quadratic hulls](publication-quadratic-assessment.md),
[penalties](publication-penalty-assessment.md),
[indicator stars](publication-star-assessment.md), and
[supporting results](publication-supporting-assessment.md) identify the
final claims, fresh proof and priority audits, and publication scope.

The finite counts above are historical successful-run records in the result
and review notes, not claims that every script was rerun during publication
preparation. Most scripts print a concise success record and retain no log;
their source and rational input tables are the reproducible evidence. The
[root record](root-research-log.md) distinguishes root runs from other
agents' runs. A passed script does not establish novelty, source equivalence,
asymptotic complexity, or a universal quantified statement beyond its
symbolic identities.

The two implementations of the 27-block certificate use the same published
rational data, as they must, but reconstruct localizing entries separately
and perform their own exact symmetric elimination. This is useful
implementation cross-checking, not independent discovery of the witness.
Likewise, the independent five-variable star checker below reads only the
literal input matrices from the author checker using `ast.literal_eval`;
its symbolic leaf elimination and all-principal-minor checks are separate.
Changing those literal assignment names or data format would require
updating that reader.

For the formal penalty result, use the existing pinned formal project:

```sh
cd paper-certified-minlp/formal
lake env lean ../../research-20260925/formal/PenaltyEncoding.lean
```

The toolchain is `leanprover/lean4:v4.33.1`. The existing
[`lake-manifest.json`](../paper-certified-minlp/formal/lake-manifest.json)
pins mathlib to commit `0df444a360eaa60ab8c11dca51a86af692955474` and records
the transitive dependencies. A fresh checkout needs that toolchain and
those dependencies available before this targeted command can run.
Do not replace the manifest by a current mathlib release to reproduce the
recorded check.

The reviewed `PenaltyEncoding.lean` SHA-256 is
`f42d98e8997e65f77a5573886673b00d823bd0aa1aa3f08d560ee4b5b780d72d`.
The file still matched that hash during this preparation. The retained
[successful log](formal/penalty-encoding-lean.log) records exit code zero,
no warnings, and nine axiom reports containing only `propext`,
`Classical.choice`, and `Quot.sound`. It is a recorded transcript, not an
independently signed build artifact. The source contains no `sorry`,
custom axiom, or native-computation proof step. It was compiled by the
author and independently by the reviewer; this preparation did not repeat
those unchanged checks.

Read the [coverage map](formal/penalty-encoding-coverage.md) and
[statement audit](formal/penalty-lean-review.md) with the source. In
particular, Lean stores a finite prefix of an infinite real sequence;
equivalence with the finite-dimensional model is a manual correspondence
check. Lean proves the two optimized dual formulas and value-exactness
thresholds. It does not formalize every claim about encoding length,
Slater regularity, minimizer feasibility, upper bounds, calibration
hardness, novelty, or solver impact.

The following exact checks support additional retained results. They are
not prerequisites for the three principal result packages above.

| Supporting result | Command and scope |
| --- | --- |
| [Uniformly conditioned rational stars](star-uniform-condition-subset-gaps.md) | `python research-20260925/verify_star_rational_uniform.py`: standard library, eight instances (`N=2,...,9`), 1,020 exact signed-sum PSD checks. Its final decimal displays are diagnostic; assertions use exact fractions. |
| [Two-leaf indicator moment gap](tree-indicator-moment-gluing.md) | `python research-20260925/verify_tree_indicator_moment_gap.py`: SymPy identities for the support cut, inverse mixture, hull witness, and relaxation witness. The pairwise example and general transfer also have written reviews in the linked note. |
| [Dense SDP–RLT gap on a five-variable continuous star](star-hull-proof-exploration.md) | `python research-20260925/check_star_counterexample.py` and `python research-20260925/check_star_independent_review.py`: exact rational witness, all RLT slacks, scalar leaf elimination and true minimum zero; the second uses SymPy and checks all 63 principal minors. Relaxed value is `-9337/250000`. |
| [Other continuous moment gaps](disjunctive-exploration.md) | `python research-20260925/verify_disjunctive_review.py`: SymPy checks of the two-bag example and two cited rational examples. Source theorems and scope still require [the review](disjunctive-review.md). |
| [Treewidth source correction](treewidth-elimination-review.md) | `python research-20260925/check_treewidth_elimination.py`: standard library, exact elimination-order calculation for the small examples and torso graph identity through eight branch vertices. The growing-family formula and corrected general bound use written graph arguments. |
| [Copositive minor and Horn supporting results](three-positive-exploration.md) | `python research-20260925/verify_cp5_face.py` (SymPy), `python research-20260925/verify_horn_disjoint_review.py` (standard library), and `python research-20260925/checks/three_positive_horn_certificate.py` (SymPy). Checks exposing identities and the explicit 243-block certificate; nonrepresentability relies on the cited theorem, not these finite checks. |
| [Star epigraph faces](../notes/research-20260925-star-epigraph-faces.md) | `python code/check_star_epigraph_faces.py`: standard library, 77 cases and 3,232 exact support checks, rerun by the star author during publication preparation. This supporting checker is outside this folder; see its [independent review](../notes/review-20260925-star-epigraph-faces.md) for the exact theorem scope. |
| [Signed low-rank indicator quadratics](integer-structure-exploration.md) | `python research-20260925/check_integer_structure.py`: standard library, 852 positive-update instances, 11,820 support checks, and 1,400 exact support solves on 40 rank-two partition-matroid instances, including independent-set and basis variants. Checks the pseudopolynomial dynamic program as well as the formulas; does not implement arrangement enumeration. Seed `20260925`. |

The discovery scripts `checks/three_positive_search.py`,
`checks/three_positive_search_log.py`, `four_star_countersearch.py`, and
`four_star_spline_search.py` are not certification programs. Neither are
the numerical corroborations `check_star_short_arc.py` and
`check_star_specker_gap.py`. They use floating-point eigensolvers or conic
optimization and can neither prove feasibility at zero tolerance nor
establish exactness by failing to find a gap. The installed optional
environment was NumPy 2.5.1, SciPy 1.18.0, CVXPY 1.9.3, Clarabel 0.11.1,
and SCS 3.3.1. These dependencies are unnecessary for the exact certificates
in the first table. Discovery results may vary with solver versions.

`four_star_spline_search.py` imports the relaxation and leaf minimizer from
`four_star_countersearch.py`. Its retained
`four_star_countersearch_results.json` is a historical search summary,
including tightened numerical reruns. It does not record every invocation,
seed, and software version used to produce the historical output, so a
bit-for-bit regeneration is not asserted. It supports no claimed theorem;
unrestricted four-variable star exactness remains unresolved here.

The direction audit, unsuccessful searches, superseded conjectures, and old
review scopes are retained as research history, not as additional
publication claims. A filename ending in `-exploration.md` does not by
itself determine status: `parametric-exploration.md` is the main penalty
lower-bound proof, and the accepted supporting results above retain some
such filenames. The pooling reduction and several integer-structure
observations have close or classical antecedents. The integer-structure
note's former inline checks now have a retained reproduction listed above.
Later result notes and their
explicit correction records control when they supersede an earlier claim.

Primary sources already retained in this batch have paired PDF/text files
in `parametric-sources/`, `smoothed-sources/`, `extreme-prior-sources/`, and
`treewidth-sources/`. The corresponding literature reviews give public
URLs, inspected passages, and limitations. Proof-critical additional
snapshots and SHA-256 hashes are indexed in
[`publication-sources/source-manifest.json`](publication-sources/source-manifest.json).
That manifest records frozen versions rather than silently replacing them
by later revisions. A snapshot preserves what was inspected; it does not
establish that a priority search was exhaustive. Extracted text is for
searching and can omit mathematical symbols; formulas must be checked
against the PDF.

The retained Anstreicher–Puges v1 HTML and pinned v1 PDF display different
manuscript dates (24 August 2026 and 17 January 2025). Both artifacts are
preserved. The cut comparison is tied to the inspected equations and
source audit, rather than assuming identical content from a shared version
label. The [fresh quadratic source audit](publication-quadratic-priority-audit.md)
also compared the pinned and current public PDFs and found that the
relevant SOC equations and their implications agree. Original retrieval
times that were not recorded remain unknown in
the manifest; archival retention dates do not replace them.

To verify the retained source artifacts from the repository root:

```sh
python - <<'PY'
from pathlib import Path
import hashlib, json
m = json.loads(Path('research-20260925/publication-sources/source-manifest.json').read_text())
for source in m['sources']:
    for artifact in source['artifacts']:
        data = Path(artifact['path']).read_bytes()
        assert len(data) == artifact['bytes'], artifact['path']
        assert hashlib.sha256(data).hexdigest() == artifact['sha256'], artifact['path']
print('PASS: every retained source artifact matches its manifest.')
PY
```

An independent local manifest check during this preparation passed for
31 source records and 61 artifacts, including byte counts, SHA-256 hashes,
and PDF file headers. All links in this index and its 23 Python script
paths existed; no unexpected control characters were present. These are
artifact integrity and documentation checks, not theorem verification.

This preparation inspected script imports, exact versus floating-point
operations, sibling dependencies, retained command records, the formal
manifest, and the unchanged Lean hash. It did not run a project-wide suite,
inspect CI, rerun exploratory searches, or rebuild Lean. Result authors'
new targeted runs and substantive corrections, if any, are recorded in
their publication-readiness audits.
