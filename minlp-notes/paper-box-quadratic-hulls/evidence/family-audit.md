# Family and counterexample audit

Scope: `sections/03-counterexample.tex`, `sections/04-family.tex`, and
`appendices/A-family.tex` in this manuscript. No other manuscript files were
edited by this writer.

## Mathematical reconstruction

The following results were proved directly from the polynomial coefficients
and cube nonnegativity, without assuming that prior proof audits establish them.

1. The rational example is nonnegative by the degree-four identity, has exactly
   the five listed edge zeros, and has no disjoint-support affine-square
   certificate. The positive-at-origin term argument uses only finite sums of
   nonnegative generators. It therefore does not require a closure theorem.
2. The general family identity holds for unrestricted real `h` and nonnegative
   `d_1,d_2,d_3,k`, including zero parameters. Its diagonal coefficients are
   `d_i^2`, so validity extends to upward diagonal slacks.
3. Under the strict five-contact assumptions, the identity determines the
   entire zero set. Vanishing on the two bottom edges and three vertical edges
   determines every coefficient of a nonnegative quadratic up to a common
   nonnegative scale. The proof explicitly includes scale zero. Summed
   evaluations expose the resulting ray. The disjoint-support exclusion
   extends directly to every strict family member.
4. Direct expansion gives `ell(q)=t*h^2+2*h*b^T*v+v^T*B*v`. Eliminating the
   unrestricted scalar at positive height gives the copositive matrix
   `B-b*b^T/t`. At height zero the inequalities force `b=0` and require `B`
   copositive. Negative height is impossible. Thus the affine 5-by-5 PSD block
   with six nonnegative auxiliaries is exact at every homogenized height,
   including the recession face; it is not merely a normalized argument.
5. The classical external input `CP_4=DNN_4` / `COP_4=PSD_4+N_4` is stated
   explicitly. PSD-plus-entrywise-nonnegative closedness has an elementary
   bounded-decomposition proof in Appendix A. Moving the nonnegative diagonal
   into the PSD summand gives exactly six auxiliaries without a boundary gap.
6. The normalized separation SDP has the same optimum as the nonnegative
   unit-vector quadratic problem. A CP factorization expresses its objective
   as a convex combination of rank-one objectives. A rank-one optimum exists,
   but extraction from an arbitrary optimizer requires an additional step.
   Appendix D supplies a separate rational support-enumeration method.
7. Complements preserve diagonal surplus. At most 24 family orientations are
   needed because exchanging the first two coordinates is redundant. No
   assertion of full-hull completeness, minimal lift size, or solver speedup
   is made.

## Exact archived certificate made self-contained

The source moment table, separating value, SOC comparisons, and positive
localizing blocks are the archived exact results in
`research-20260925/three-positive-disjoint-counterexample.md`,
`research-20260925/three-positive-family-sdp.md`, and the independent publication
proof audit. Appendix A reproduces all 20 moment values and expands them into
all 27 localizing matrices, compressed only by the exact x/y symmetry. It lists
the leading integer determinants of every block and gives a six-row slack
table covering all eight complement patterns and all 24 + 48 SOC instances.
These are certificates that a reader can reproduce from the manuscript alone.

The main strict comparison includes the separate diagonal caps, the PSD base
matrix, trilinear RLT, the nonnegative factors required by rotated SOC, and
the implication of the SOC systems for ETRI1--3. Source matching and canonical
bibliography are owned by the Luna literature agent.

## Targeted check actually run

Command: `python - <<'PY'` with an inline exact-integer/SymPy transcription
check of the newly expanded manuscript tables. It compared the leading
determinants of the five distinct order-three/four numerator matrices and
the seven distinct order-two determinants against the printed entries, then
computed the displayed minima of the 3 and 6 SOC slack numerators for each of
the six distinct complement rows.

Result: exit 0; output `PASS: exact determinant and switched-SOC arithmetic in
new manuscript certificate tables.`

This was a new exact-arithmetic table check, not an optimization or sampling
experiment. No archived checker, solver experiment, project-wide check, or CI
inspection was run. The archived numeric experiments were not rerun.

## Limits and dependencies

The classical cone theorem is cited under `Diananda1962` and
`MaxfieldMinc1962`; comparator keys are `Khajavirad2026SparseBoxQP`,
`AnstreicherPuges2025ETRI`, and `AnstreicherBurer2010`. No literature research
or online browsing was performed by this writer. The root and Luna agent
control source contracts, bibliography, and novelty wording.

Referenced integration labels are `set:cones`, `three:sign`, and
`comp:family-separation`. Main exported labels include `family:definition`,
`family:valid`, `family:exposed`, `family:lmi`, `family:separation`, and
`family:gap`. Independent review and final typesetting are pending integration.

## Explanatory diagram

Added `figures/five-edge-zeros.py`, its vector PDF output, and a PNG preview
in `verification/previews/` on the root's request. The script projects the unit cube and the five listed edge
zeros to fixed planar directions. It performs no optimization, sampling,
polynomial evaluation, or mathematical verification.

Command actually run: `python paper-box-quadratic-hulls/figures/five-edge-zeros.py`.
Result: exit 0; PDF and PNG produced. Font conversion emitted notices about
low font timestamps; there was no rendering failure. The PNG was opened
with `view_image` and inspected: the five contact labels and four cube
coordinate labels are readable and do not overlap. The figure is monochrome,
with dashed rear edges and darker edges carrying zeros.
