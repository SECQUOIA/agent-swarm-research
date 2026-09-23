# Whole-manuscript corrections after round 1

I read the root assessment and all five independent full-paper reports. The
only accepted finding was the minor connectedness omission when the
principal-window transfer receives the zero-variable arithmetic source.

The correction changes only the proof of Corollary 5.5 in
`sections/04-structural.tex`. It states that a source with a named variable
already produces at least two buses after connection and subdivision, so
the structural principal transfer needs no isolated padding. For the
zero-variable source, it explicitly uses two voltage-1 buses with zero
active and reactive injections, joined by one unit-conductance line, and
sets `c_2 = 3/4`. The statement that the transfers preserve the graph is
qualified by this exception. The existing RPF empty-source convention and
all checker implementations are unchanged. The one-sided reactive option
is retained.

## Independent verification

The two-bus graph is a tree, hence connected, simple, planar, bipartite,
and of infinite girth, with maximum degree one. Both magnitudes are pinned
to 1. At the equal-phase rectangular witness, each active and reactive
injection is exactly zero and the cosine inequality is `1 >= 3/4`.
Thus the feasible magnitude set is exactly the singleton `(1,1)`, which
represents the point of `R^0`. All numerical data are permitted. One-sided
reactive intervals also work: their common sign and cancellation of total
reactive injection force both reactive injections to zero. For every
source with a named variable, the connector step adds a distinct bus to
at least one root; subsequent subdivision cannot reduce that count.

I reran reviewer 2's independent boundary-composition check successfully
and separately evaluated both rectangular power equations with exact
rational arithmetic. A comparison with the frozen full-round inputs
confirms that only the structural section changed among manuscript and
checker inputs. The root-owned `PROCESS.md` also differs from its snapshot;
I did not edit it.

I cleaned the LaTeX outputs and rebuilt from source. The final manuscript
has 28 pages, with no LaTeX warnings, unresolved citations or references,
overfull boxes, or underfull boxes. I rendered and visually inspected page
16, which contains the complete corrected proof and the following section
transition. The text and mathematics are readable and unclipped.

Evidence:

- `verification/full-corrections.diff`: exact manuscript diff against the
  reviewed snapshot.
- `verification/full-corrections-boundary.log`: successful independent
  boundary and analytic-example check.
- `verification/full-corrections-verification.json`: exact rectangular
  evaluation, graph assessment, and changed-input record.
- `verification/full-corrections-clean.log` and
  `verification/full-corrections-build.log`: actual clean and build output.
- `verification/full-corrections-layout.log`: final log assessment and PDF
  metadata.
- `verification/full-corrections-page16.png`: inspected rendering.

The accepted minor has been addressed. This report returns the correction
to root for final verification; it does not change process status or freeze
a new snapshot.
