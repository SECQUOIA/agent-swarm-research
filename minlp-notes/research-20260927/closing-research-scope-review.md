# Independent scope review of the closing research record

Date: 2026-09-28. Status: **PASS after two qualification corrections**.
The reviewer did not author the closing record or the theorem notes
audited here. This was a fresh documentation and theorem-scope audit,
not another independent proof of every component result and not journal
peer review. No new research direction was pursued.

## Scope and conclusions

The reviewer read the [closing record](closing-research-results.md),
the complete [mixed-integer rank composition](mixed-quartic-integer-constraint-rank-oracle.md),
the [rational-optimizer coordinate theorem](rational-optimizer-posslp-coordinate-comparison.md),
the [strongly SOS-convex block construction](strongly-sos-convex-block-splitting-obstruction.md),
and the [quadratic-graph construction](quadratic-graph-quartic-realization.md).
The review also compared the relevant statements in the candidate-list,
circle certificate-height, block-lifting, and interior-Gram notes.

The closing record now preserves these distinctions:

- Coordinate comparison is PosSLP-complete, with hardness even for a
  bounded rational optimizer and known minimum zero. This does not
  promise a rational optimizer for the separate minimum-value
  perturbation construction or decide the rationality promise.
- The ordinary candidate list may contain nonoptimal blocks. Exact
  selection is separate. The combined algorithm is Las Vegas with a
  PosSLP oracle, parameterized by the integer dimension and the rank of
  the entire continuous constraint matrix. Its continuous output is
  implicit; no short expanded algebraic output is asserted.
- The sparse certificate bounds concern the prescribed block format.
  They do not establish a lower bound for unrestricted rational SOS
  certificates or for optimization time.
- The quadratic-graph construction assumes minimum zero and a supplied
  full positive definite rational Hessian Gram. It does not recognize
  the zero-minimum promise. The growing-field consequence has quadratic
  variable growth and keeps the distinction between blockwise strict
  Hessian certification and joint full-basis positive definiteness.

Publication priority and practical solver speedups remain explicitly
unestablished. The summaries credit the established oracle frameworks,
convex approximation, commutator techniques, and sparse SOS comparisons.
No unsuccessful novelty search is treated as proof of originality.

## Corrections and independent recheck

First, the circle consequence now specifies rational maximal-rank
optimal Grams and nonzero rational PSD exposing matrices. Bit-height
bounds cannot be silently extended to arbitrary real matrix entries.

Second, additive separation forces every **positive semidefinite** Gram
on the full joint Hessian basis to be singular. It does not force every
symmetric Gram to be singular. This qualifier was missing from the
closing record and the two construction notes. Their earlier review
records already stated the PSD restriction.

For an explicit check, the Hessian biform of
\(x^4+x^2+y^4+y^2\) on \((a,b,xa,xb,ya,yb)\) has a
symmetric Gram with diagonal \((2,2,12,0,0,12)\), entries
\(Q_{3,6}=Q_{6,3}=1\), and
\(Q_{4,5}=Q_{5,4}=-1\). The two cross terms cancel, and its
determinant is \(-572\), so the Gram is nonsingular and indefinite.
For a PSD Gram, the zero diagonal entries corresponding to \(xb\)
and \(ya\) force zero rows, proving singularity. The reviewer derived
this counterexample, the root independently reconstructed it, and the
reviewer reread all three corrected statements.

The mixed-linear summary was also clarified to say that the candidate
list contains every optimal integer block, without implying that every
listed block is optimal. No unresolved discrepancy remains within this
scope audit.

## Audited versions and verification limits

SHA-256 hashes of the corrected files read by this reviewer:

| File | SHA-256 |
| --- | --- |
| `closing-research-results.md` | `389f22b4962f29479519490203562b510cc9a2fa63e2af8d879f13744dc131e7` |
| `strongly-sos-convex-block-splitting-obstruction.md` | `d09395ce9ef25e8f5b0c4ccd741e4745f6dd6c04e03d5b1c6c5351c830b1cf17` |
| `quadratic-graph-quartic-realization.md` | `769a4e8ea68e0f4f169043f6220ef8e023ab685181a8614070961b12389bb5db` |

The audit used targeted reads and text searches of these topic notes,
plus exact mathematical reconstruction of the qualifier counterexample.
It did not rerun the component computational checkers, redo the external
literature searches, or formally verify the imported theorems. No Lean,
project-wide verification, or CI inspection was used.

A targeted inline Python check passed this review's five local links,
paired math delimiters, whitespace, control characters, final newline,
and all three source hashes. The command
`git diff --check -- research-20260927/closing-research-scope-review.md`
also returned no errors. The inline check covers this new file even
when it is untracked and therefore absent from the ordinary Git diff.
