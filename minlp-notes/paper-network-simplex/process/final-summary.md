# Completed manuscript

The 48-page paper, *Sparse convex hulls for network flows coupled to a simplex*,
is complete within its stated scope. Read [the PDF](../main.pdf),
[LaTeX source](../main.tex), or [source coverage map](coverage.md).
The [final validation manifest](../verification/final-validation.json) identifies
the accepted sources, evidence and review records.

## Development during writing

The paper goes beyond the earlier notes. It supplies exact finite-basis compact
recovery for bounded block rank, a smaller two-label/five-product K4 sharpness
construction, and the sharp flat-chain unit-coefficient guarantee through three
observed labels with failure at four. Eliminating the residual profile gives
five tests at two labels and 16 circuits at three; explicit balance repairs
establish the latter unit bound. Globally unused labels are merged while all
original simplex coordinates and compact recovery are preserved.

The manuscript also completes the fixed-arc preprocessing argument and records
the classical integral-data hull equality with its integral-decomposition-size
limitation. It gives self-contained proofs of the existing compression,
structured separation, universality, sparse Fibonacci, and degree-three results,
with precise attribution and encoding/coefficient qualifications.

Computational review strengthened the full and globally merged baselines with
native fixed-weight bounds and added elementary positive-state/one-flow controls.
These corrections remove some earlier runtime claims. The all-labels-observed
control still isolates a substantial local compression benefit. All measured
results are synthetic, and exact certificates are distinguished from numerical
LP answers. Old code, measurements and negative findings remain as documented
provenance. An independent full five-repeat run in the whole-paper review
reproduced objectives, input/model counts and the main qualified conclusions.

## Completed review process

Each of seven authoring stages was frozen before five independent reviews.
The root read every full report and assessed every finding. A different agent
corrected all valid findings. The major baseline issue in Stage 6 triggered a
second five-reviewer round; it and all remaining minor findings were resolved
before proceeding. Stage 8 used five fresh reviewers to examine the entire
manuscript. Its sole minor citation-locator finding was corrected separately
and verified by the root.

There are 45 independent reports in nine review rounds, retained under
[reviews](reviews/), with root dispositions under [assessments](assessments/).
The complete paper builds without warnings or unresolved references. Independent
exact algebra, construction and certificate checks, the principal 23-test suite,
full-model comparisons, complete table regeneration and source hashes support
the recorded verification. Finite tests supplement the proofs.

All valid findings are resolved. No further research is needed to establish
the claims made in this manuscript; claims outside its stated scope are not
implied. Internal acceptance does not establish exhaustive priority or replace
external peer review. Author and affiliation fields are intentionally empty
for the owner. No submission or external publication was performed.
