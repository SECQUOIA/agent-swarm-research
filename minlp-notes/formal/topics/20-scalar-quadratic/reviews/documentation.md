# Independent review: topic 20 notes and manuscript

Reviewed the topic 20 changes to:

- `results/quadratic-rank-integer-complexity.md`;
- `results/quadratic-inertia-one-sided-integer-complexity.md`;
- `results/mip-relaxation-binary-lower-bounds.md`;
- `paper-integer-dimension/README.md`, `main.tex`, and
  `sections/01-foundations.tex`.

The review compared the changes with the frozen claims, final declaration map,
actual construction interfaces, and independent proof reports. It did not
review the rest of the paper or repeat a PDF build.

Verdict: the mathematical statements and verification scope pass review.
The exact square threshold, rank/inertia coefficients, determinant denominator
`48 sqrt(r)`, and sharp curvature coefficient `μ/2` agree with the formal
results. The added `d>0` and `δ>=0` premises correctly repair the contact-volume
statement, including its empty-set case.

The spectral enclosing radius and normalized coefficient formula match the
formal construction. Binary, auxiliary, and row counts refer to actual affine
systems; original inputs and output are excluded from auxiliary counts.
The one-sided discussion correctly distinguishes depth `L+1` for the finer
standalone square estimate from depth `L` for the shared aggregate error
budget. Full epigraphs and hypographs retain their unbounded output direction.
The exact convex product threshold is distinguished from finite linear
approximation with arbitrary positive extra slack at the same binary count.
No exact finite-LP threshold attainment is asserted for the product.

Two narrowly authorized wording corrections were made in the inertia note and
manuscript: the sharp isodiametric proof uses a sufficiently large finite
cutoff to transfer a volume excess to a weighted-measure excess. It does not
need a limit argument to remove the weight. No mathematical claim changed.

The scope statements exclude vector quadratic topic 26, other nonlinear
results, literature attribution, and whole-paper correctness. Historical
numerical checks and old submission/review artifacts are explicitly distinct
from the new Lean verification. The binary-lower-bound note also excludes its
separate whole-product-graph constant and NMDT claims. The manuscript retains
the valid exposed-face explanation of the row bound; the formal coverage map
identifies the equivalent, fully proved active-pattern route.

At review time, the final topic audit was running and `VERIFICATION.md` still
said implementation was in progress. Several revised source paragraphs
already describe that record as containing final checks and fingerprints.
The root agent was notified to replace the provisional verification record
with actual completed results before announcing completion. This report does
not certify that running audit or its eventual outcome. The documentation's
mathematical verdict is independent of that release prerequisite.

No whole-project checks or CI inspection were performed. No Lean source was
changed by this review.
