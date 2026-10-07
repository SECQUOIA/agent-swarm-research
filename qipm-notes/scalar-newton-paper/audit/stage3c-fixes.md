# Stage 3c corrections

All seven groups accepted in `stage3c-assessment.md` are addressed in
`sections/10-structured.tex`. No earlier mathematical section was changed,
and Stage 4 was not started.

1. **Bidirectional sparse interfaces.** The one-entry maps T_j now have
   constant-cost row and column count/location/value access, including
   reporting missing entries. The cone corollary also explicitly grants
   both directions of sparse access to A. This addresses reviewer 1 item 1,
   reviewer 2 item 1, reviewer 3 item 2, and reviewer 4 item 1.
2. **Separate block access and zero vectors.** The cone corollary requires
   separate SQ and norm access for each block source, together with its
   scalar data. It distinguishes this from aggregate concatenated SQ.
   Radial norm and coordinate queries include the zero case; sampling is
   requested only for nonzero radial blocks and zero radial corrections
   are omitted. This addresses reviewer 2 item 2, reviewer 4 item 2, and
   reviewer 5 item 1.
3. **Lorentz normalization and profile hypotheses.** The Lorentz identity
   explicitly defines H as the Hessian of -log(t^2-||z||^2), with
   t>||z||. The separate profile subsection repeats the block Hessian
   normalization and interior domains and assumes full row rank of the
   concatenated A. This addresses reviewer 1 items 2 and 4, reviewer 2
   item 3, reviewer 3 item 1, reviewer 4 item 3, and reviewer 5 item 2.
4. **Rank-necessity scope.** The stronger profile-wise Loewner statement
   is expressly within the same A=I witness family, allowing unequal
   block eccentricities. No claim is made for arbitrary compressive A.
   This addresses reviewer 2 item 4 and reviewer 3 item 3.
5. **Nonzero-count hypothesis.** The final full-output consequence now
   uses nnz(A)<=D^{1+o(1)} instead of the undefined phrase scalar-sparse.
   It also explains that the supplied latent incidence width itself gives
   nnz(A)=O(D(tau_L+1)), using L_c<=n. This addresses reviewer 1 item 3.
6. **Canonical coherent acquisition access.** The geometric-mean example
   now specifies uniform-pair preparation, one hidden-bit query, a known
   two-coordinate rotation, and uncomputation. Value queries, preparation,
   inverse preparation, and controlled versions have constant hidden-bit
   query overhead. The quantum lower bound is restricted to this specified
   completion, and the constant-relative example uses the same interface.
   This addresses reviewer 4 item 4.
7. **Elimination attribution and preprocessing.** The latent-width proof
   identifies Fürer--Hoppen--Trevisan Corollary 3 as the system-solving
   result. It explains their Section 3 conversion from the supplied compact
   decomposition to an O(N_aug)-node nice decomposition in
   O(k(|T|+N_aug))=O(k^2 N_aug) time. This is absorbed by the existing
   width-squared bound; the supplied decomposition promise is unchanged.
   This addresses reviewer 3 item 4. The cited primary preprocessing and
   solve statements were independently verified by the lead reviewer.

## Validation

- Ran `checks/check_structured_identities.py` with
  `/workspace/local-home/miniconda3/envs/qipm/bin/python`: all 152 numerical
  identities and comparison checks passed.
- Ran `make clean` and then `make -B` in the paper directory through
  `conda run -n qipm --live-stream`.
- The corrected staged PDF has 54 pages. The final LaTeX and BibTeX logs
  contain no warnings, undefined references/citations, or box warnings.
- `workflow.md` marks Stage 3c corrected and pending root verification.

Verdict: all accepted Stage 3c corrections are complete. The correction
check identified no further issue.
