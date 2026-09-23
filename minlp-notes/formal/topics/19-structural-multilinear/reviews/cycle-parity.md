# Independent review of closed-trail parity

Reviewed 2026-09-20. The reviewer did not author or edit
`StructuralCycleParity.lean` or `StructuralCycleTU.lean`.

**Result: no statement or mathematical defect found in
`cycleParity_eq_zero_of_isTrail`, or in the paired-edge lifting argument present
in `StructuralCycleTU.lean` at review time. The graph-to-TU theorem was still
being assembled; this review does not certify a later unreviewed theorem.**

The parity convention was traced into `StructuralTreewidthGraph.lean`:
`cycleParity` omits the initial vertex and counts the final copy, so a simple
cycle counts each factor vertex once. For an inserted closed subwalk,
`cycleParity_remove_subcycle` subtracts exactly that closed subwalk's factor
contribution. The repeated join vertex is handled by the existing append
identities and is not counted twice.

`cycleParity_eq_zero_of_isTrail` requires parity zero for every simple cycle,
and requires the supplied closed walk to be a trail. Both hypotheses are
material. The proof extracts a simple subcycle from a non-path trail, removes
it, preserves edge distinctness through a list-subsequence argument, and
strictly decreases length because a simple cycle is nonempty. A closed path
is the zero-length walk, giving the induction base. This proof does not
assert parity zero for arbitrary closed walks: traversing one incidence edge
and immediately returning would violate that assertion.

The reviewed lifting definitions replace a paired-row edge by its two actual
incidence edges. The endpoints of each pair are distinct. The key lemma
`lift_edge_origin` shows that an incidence edge `(r,c)` determines the original
paired edge `{r, mate_c(r)}`. Hence distinct paired edges cannot reuse an
incidence edge. `lift_isTrail` uses this fact to preserve edge distinctness;
repeated column vertices cause no problem. For a closed paired walk, the
lifted factor parity equals the paired walk length modulo two. Thus applying
the closed-trail theorem to a lifted odd simple cycle is justified by a real
trail, not by an unsupported projection argument.

This was a source and statement review. No additional build was run for this
review while the graph dependency owners were compiling their pending
changes. No project-wide verification or CI inspection was performed.
