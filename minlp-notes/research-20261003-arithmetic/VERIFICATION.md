# Targeted verification record

This record covers topic 2 only. Commands below were run by the named
workstream authors/reviewers or during integration. No project-wide local
checks, CI status inspection, or CI log inspection were performed. A passed
finite diagnostic is evidence about its fixtures, not a proof of a universal
theorem. Independent research-agent review is internal review.

## Mathematical review

| Scope | Saved independent review | Outcome |
| --- | --- | --- |
| Existing point theorems | [Point core](reviews/point-core/review.md) | No substantive defect found. |
| Quartic point reductions | [Hardness audit](reviews/point-core/hardness-audit.md) | Passed with domain-convexity and conditional-complexity qualifications. |
| New global sparse/unbounded theorem | [Point review](reviews/point-core/global-extension-review.md), [radius review](global-point/radius-independent-review.md) | Two complete reconstructions passed. |
| Full cubic recourse | [Cubic extension](reviews/cubic-extension/review.md) | Passed; the integrated kernel/interiority clarification was incorporated. |
| Nonlinear-dimension exact comparison | [Independent review](constrained-exact/independent-review.md) | Passed, including coefficient bounds and ordinary FPT composition. |
| Structured box Newton | [Structural review](constrained-exact/review-structural-newton.md) | Passed after tightening the arithmetic-operation interface. |
| Polynomial flows | [Flow review](constrained-exact/network-flow-review.md) | Passed, including the exact source-operation model and artificial-arc bound. |
| Historical exact quartics and witnesses | [Consolidated exact audit](reviews/exact-core/review.md) | No substantive defect found; individual reduction and witness reviews are linked there. |
| Variable-degree exact upper | [Degree review](reviews/exact-core/general-degree/general-degree-review.md) | Passed. |
| Circuit interior Gram | [Gram review](reviews/exact-core/general-degree/circuit-interior-gram-review.md) | Passed, including six exact symbolic fixtures. |
| Reference implementation | [Implementation review](implementation/REVIEW.md) | Passed; incomplete box-tangent certification is documented and tested. |

Report sections received further integration reviews against those saved
proofs. The [point integration review](reviews/point-core/report-integration-review.md)
records the notation and scaling clarifications. The exact-core,
nonlinear-dimension, and cubic reviews include their integration verdicts.
The final statements retain the difference between ordinary FPT, a single
PosSLP reduction, and an adaptive `P^PosSLP` algorithm.

## Reproducible diagnostics actually run

All commands in this section are from the repository root. Their workstream
records identify who ran each command; integration did not repeat passing
mathematical diagnostics after prose-only changes.

```sh
python3 research-20261003-arithmetic/global-point/check_radius_construction.py
python3 -B research-20261003-arithmetic/cubic-recourse/check_cubic_recourse.py
python research-20261003-arithmetic/constrained-exact/check_nonlinear_dimension.py
python3 research-20261003-arithmetic/constrained-exact/check_structural_newton_review.py
python3 research-20261003-arithmetic/constrained-exact/check_network_flow.py
python3 -B research-20261003-arithmetic/literature/check_source_formulas.py
```

All passed. The distinct fixture counts are:

- Global points: nine interpolation degrees, 455 integrated-quadratic and
  decomposition checks, 121 sublevel checks, five radius fixtures, and
  explicit unboundedness/bounded-representative cases.
- Cubic recourse: 257 face cases, 24 regularization completions, 234
  polynomial-margin checks accompanying nine LLL acceptances, and nine
  exact-relation rejections. These do not implement the general core oracle.
- Nonlinear dimension: eight polynomial cases, 40 affine faces, and 15
  sign/equality threshold checks.
- Structured boxes: 90 exact box QPs, 714 principal-submatrix checks, and
  four quartic Newton steps. Zero optimal multipliers are included.
- Flows: six cases and 42 exact Newton steps, including tiny positive slacks.
- Source formulas: five diagnostic groups, including 67 rational sublevel
  fixtures and 396 positive even-monomial coefficients.

The detailed records are [global points](global-point/verification.md),
[cubic theorem, Section 8](cubic-recourse/theorem.md#8-targeted-verification),
[constrained exact](constrained-exact/verification.md), and
[source audit](literature/source-audit.md). Counts from overlapping reviewer
reruns or separate ad hoc fixtures are not added into a misleading total.

The exact-core authors/reviewers also ran the following narrow commands,
all of which passed:

```sh
python research-20261003-arithmetic/reviews/exact-core/check_boundary_sos.py
python3 research-20261003-arithmetic/reviews/exact-core/lower_diagnostics.py
python research-20261003-arithmetic/reviews/exact-core/check_rational_lower.py
python research-20261003-arithmetic/reviews/exact-core/check_witness_output_audit.py
python3 research-20260927/check_posslp_cubic_root_reduction.py
python research-20260927/check_strict_quartic_witness_lower_bound.py
python research-20260927/check_interior_gram_bit_lower_bound_review.py
python research-20260927/check_convex_quartic_irrational_zero.py
python research-20260927/check_convex_quartic_rational_sos.py
```

These historical-file checks are limited to mathematical dependencies of
this topic. Their claims and execution records are in the
[exact audit](reviews/exact-core/review.md) and its linked individual reviews.

## Reference implementation

The implementation author and independent reviewer ran:

```sh
python -m unittest discover -s research-20261003-arithmetic/implementation -p 'test_*.py' -v
python research-20261003-arithmetic/implementation/demo.py
```

The final suite passed all ten tests. A constant-objective row bug was fixed
during development; the final suite covers it. The demo confirms the
optimizer-set/fixed-selector distinction, the `2^(-80)` gap with distance
one, and the 13-node recurrence with a 4,097-bit expanded denominator.
[Implementation verification](implementation/VERIFICATION.md) records the
precise scope and the separate reviewer diagnostics. This is a witness
checker, not a general optimizer or PosSLP implementation.

## Integrated document

The primary-source author normalized citation keys and ran a temporary
BibTeX check covering all 22 bibliography entries; it passed without warnings.
The report was built from `research-20261003-arithmetic/document` with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The first integrated build found one math-mode typo in section 7. It was
corrected. The successful build produced a 29-page PDF. Its final log has
no undefined citations or references, no LaTeX warnings, and no overfull or
underfull boxes. The PDF remains beside its source so relative companion
links retain their targets.

Final scoped document checks are run from the repository root:

```sh
python3 -B research-20261003-arithmetic/check_documents.py
git diff --check -- README.md research-20261003-arithmetic
```

The checker validates authored Markdown/LaTeX whitespace, local link targets,
input files, unique labels, references, and bibliography keys. It includes
untracked new documents, which an unstaged Git diff alone does not check.
It passed 53 documents, 263 local links, 55 LaTeX labels, and 12 cited keys;
the scoped Git whitespace check also passed. The final counts are recorded in
[PROGRESS.md](PROGRESS.md). Link existence is not a mathematical or
publication-priority check.

The first PDF page was rendered with `pdftoppm` and visually inspected;
the title, abstract, and contents were readable without clipping. This
spot-check supplements the final compiler log and is not a claim of a
page-by-page visual review.

The [source ledger](literature/source-ledger.md) retains two source-access
limits: Yang's full primary text and the Hesse proceedings version were
unavailable. The remaining unrestricted constrained comparison problem is
documented in [general-boundary.md](constrained-exact/general-boundary.md).
Neither source access nor this mathematical question is marked solved.
