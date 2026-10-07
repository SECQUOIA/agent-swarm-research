# Independent grid and cap review of the core value oracle

Date: 2026-10-02. Verdict: **PASS** on the actual saved
[core-only-noise value-oracle theorem](core-only-noise-value-oracle.md).
This review checks the cell construction, global certificates, projected
growth formula, and cap accounting. It is separate from the designated
[full composition and probability review](../reviews/core-only-noise-value-review.md).
No external search was used.

## Global certificate and retained-cell count

The fixed residual domain is essential: holding a residual optimizer
fixed while independently rounding the core preserves feasibility.
The coordinate upper-curvature premise gives a corner interpolation
penalty \(e_j=kLh_j^2/8\). With conditional interval width at most
\(e_j\), every generated cell has the valid lower bound
\(\min\ell_v-e_j\), and every optimal core cell survives.

The final stage incumbent satisfies \(U-f^*\le2e_j\). Every queried
corner satisfies \(\ell_v\ge u_v-e_j\ge U-e_j\); therefore every
current cell lower bound is at least \(U-2e_j\). Previously excluded
cells have lower bounds above an older incumbent, hence above the current
one. The recorded dyadic coverage and these inequalities certify the
global interval \([U-2e_j,U]\). This does not depend on a growth promise.

Retaining cells against the **final** level incumbent matters. A retained
cell then has a minimizing corner of true conditional value at most
\(U+2e_j\le f^*+4e_j\). Positive projected growth \(g\) confines this
corner to radius \(h_j\sqrt{kL/(2g)}\) around the unique optimal core.
Counting lattice coordinates, corner incidence, and children gives

\[
 \#\{\text{generated cells at the next level}\}
 \le4^k(3+\sqrt{2kL/g})^k
 \le512\max\{1,L/g\}^{k/2}.
\]

The final constant is valid for \(k=1,2\): if
\(Z=\max\{1,L/g\}\), the preceding expression is at most
\(4(3+\sqrt2)\sqrt Z\) for \(k=1\), and \(400Z\) for \(k=2\).
It also covers the initial cell. This argument has no condition relating
the refinement width to the noise-grid spacing.

## Projected growth and the cap

The two-block quantified growth formula is correct despite residual
ties. Its existential residual point attains the global value, and its
universal residual variable compares against every feasible completion.
The norm contains only core coordinates. The finite-section complexity
is consequently uniform in the threshold and sampled coefficient heights,
as required by the previously reviewed finite-law transfer.

Let \(W=\max\{1,L/g\}^{k/2}\), with \(W=+\infty\) at \(g=0\).
Before generating a new level, comparing \(2^k\) times the retained
parent count with \(512B\) prevents an oversized candidate list or
oracle batch. Every cap event, over all levels and all requested
precisions, lies in the single event \(\{W>B\}\). No union over the
number of levels is needed.

The tail \(\Pr\{W>s\}\le(kL/\sigma)s^{-2/k}+\beta\) for
\(s\ge1\), with \(\beta=C_0/M\), directly yields the stated
truncated moments. It also gives the slightly stronger explicit chain

\[
 B\Pr\{\text{any cap}\}
 \le B\Pr\{W>B\}
 \le(kL/\sigma)B^{1-2/k}+\beta B.
\]

Thus the indicator \(\mathbf1_{\{W>B\}}\) used in the simultaneous
work bound is controlled, whether or not a particular query actually
reaches an oversized level. Choosing \(B\ge B_0\) and \(M\ge C_0B\)
pays for the base exponential fallback factor and the finite-law atoms.
The \(\log B\) term for \(k=2\) has polynomial input bit length.

The nonnegative-curvature case split is complete: \(L>0\) permits
positive corner tolerances, while \(L=0\) reduces the value to the
minimum of the core-vertex values. The proof promises objective accuracy
and feasible witnesses, not distance to an optimizer or stable residual
labels.

## Exact grid diagnostic and commands actually run

The [persistent diagnostic](check_core_value_grid.py) records the code
previously executed as an inline `python3 - <<'PY'` command. The actual
inline run passed:

- 108 exact refinement stages;
- 5,656 cell lower-bound checks;
- 2,131 safe pruning decisions.

The examples use one- and two-dimensional quadratic cores with interior
and boundary optima, three growth scales, and a convex residual objective
\(y^2\). At tolerance \(e\), the supplied feasible residual witness is
\(y=e/(1+e)\); its nonzero rational value supplies deliberately inexact
conditional certificates of width \(e\). Checks cover global objective
intervals, optimal-cell containment, retained-corner witnesses, and
generated-cell packing. The diagnostic uses the safe packing coefficient
\(512(1+L/g)^{k/2}\); the sharper \(512\max\{1,L/g\}^{k/2}\) in the
saved theorem was checked algebraically above.

The persistent copy was saved after the actual-file review and was not
rerun separately. No new fixtures or probability tests were added; the
other reviewer owns the linked finite-law diagnostics. No project-wide
verification, CI inspection, or index edit was performed.

A subsequent inline Python command parsed the saved checker with
`ast.parse` and checked the two new review documents' math delimiters,
whitespace, and local links. It passed without running mathematical
diagnostics. A `git diff --check` restricted to the checker and those two
reviews also passed.
