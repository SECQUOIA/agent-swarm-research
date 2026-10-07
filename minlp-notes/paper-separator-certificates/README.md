# Constructing separator certificates for sparse global optimization

This anonymous manuscript develops constructive affine separator certificates
on arbitrary tree decompositions. It includes consistency and approximation
theory, aggregate regridding under global quadratic growth, certified inexact
local solves, an exact rational polynomial implementation, and contracting
nonlinear dynamics with compressed feasible output. All stated results have
complete proofs. The paper is theoretical; no computational experiments were
rerun or used to replace a proof.

- [Paper PDF](main.pdf)
- [Portable submission sources](submission-source.zip)
- [TeX entry point](main.tex)
- [Literature review and source locators](evidence/LITERATURE.md)
- [Source coverage and overlap map](evidence/AUDIT-SCOPE.md)
- [Mathematical and editorial reviews](evidence/reviews/)
- [Targeted verification record](verification/RESULTS.md)

Build from this directory with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The source archive contains the manuscript, bibliography, and generated `.bbl`
file, without internal evidence or build debris. The PDF contains no author
names or date. The literature review follows the supplied literature skill and
was conducted with GPT Luna at max reasoning. Its claim table distinguishes
established ingredients from the specific contributions and records all
remaining source-access gaps. Independent mathematical review means a separate
agent checked the arguments; it does not mean journal peer review.

The main growth hypothesis forces a unique minimizer. Complexity depends on
bag dimension, coordinate occurrence, and numerical conditioning. A sufficient
fixed grading ratio gives the sharp final partition count; unknown-parameter
search has a separate total-work and output guarantee. The dynamics extension
requires full-box invariance and contraction, and returns exact trajectories
through their recurrence representation. These limits are part of the paper's
theorem statements.

The rational box realization was developed during manuscript preparation. Its
affine Taylor models satisfy the generalized bag-error contract, its local
minimizers select interval endpoints, and a common denominator gives explicit
bit and compact-certificate bounds. It does not preserve every possible
factorwise relaxation. The proof audits also repair boundary conventions,
attainment arguments, class assumptions, precision budgets, and output
accounting. Earlier incomplete smooth-band insertion and multidimensional
covering claims are excluded from the proved results.

This is a companion to the existing certificate-size analysis in
[`paper-bb-complexity`](../paper-bb-complexity/), which centers its existence
construction at a known optimizer. The separate
[`paper-decomposition-aware`](../paper-decomposition-aware/) manuscript uses
corrected coordinate grids. The present paper constructs affine separator
certificates from its own recovered points. These internal manuscripts have
no supplied public bibliographic identity, so the scientific bibliography
does not invent one. The overlap audit records exact included-file comparisons.
