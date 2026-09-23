# Independent review of polynomial binary-path cut values

Date: 2026-09-05. Reviewer: `close_inventory`, independent of the derivation.
Scope: Section 1 of [the path-cut note](parametric-path-cut-clamp-investigation.md).
Verdict: **PASS**. This review does not verify Section 2's proposed pooling reduction.

Subtracting the two conditional prefix recurrences gives
`D_i=u_i+min(D_(i-1),a_i)-min(0,D_(i-1)+b_i)`.
For `a_i,b_i>=0`, its three regions are `D<-b_i`,
`-b_i<=D<=a_i`, and `D>a_i`; the difference is respectively
`-b_i,D,a_i`. Translation by the unary prefix sum therefore gives the
stated clamp recurrence for `Z_i`. This calculation includes zero edge
costs, signed unary costs, and equality cases.

Every clamp returns either its preceding value or one of its two endpoints.
Induction puts all prefix values in the common list of zero and the
`2(n-1)` polynomial endpoints. The choice of the increment of `E_i(0)`
uses the comparison of `Z_(i-1)` with `-b_i-P_(i-1)`, already in that
list. The terminal label uses comparison with `-P_n`, so the additional
`-P_i` polynomials suffice. The same comparisons recover minimizing
predecessor labels if a witness is requested.

Pairwise differences of the list have bounded degree and polynomial
coefficient length. In fixed parameter dimension their realizable sign
conditions have polynomial total complexity. On every such condition the
dynamic program selects a fixed sequence of polynomial expressions, whose
sum still has bounded degree and polynomial coefficient length. Lower
dimensional sign conditions must be included, as the note requires.
The argument can construct the ambient sign conditions before restricting
to the parameter domain; it does not assume an algorithmic oracle for an
otherwise unspecified domain.

Conditioning on one cycle label absorbs both incident interactions into
the remaining path's endpoint unary terms. Running the two conditioned
path problems and refining by comparisons of their polynomial values
preserves polynomial complexity. Fixed nonnegative transition costs are
essential to the particular clamp identity; the proof is not a claim
about arbitrary continuous path LPs or arbitrary parametric treewidth.

I inspected and reran the retained exact checker:
`python code/pooling_bypass_paths/check_path_cut_clamps.py`.
It passed 360 rational instances, each compared with every original
binary labeling. These checks corroborate the recurrence; the argument
above supplies the symbolic-cell and encoding justification.

This is an elementary dynamic-programming consequence, with no separate
priority claim. Any application to physical pooling still needs the
independent reduction and source checks stated in Section 2.
