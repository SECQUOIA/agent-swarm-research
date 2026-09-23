# Independent review of documentation and the paper supplement

Reviewed the frozen claims, declaration coverage, source inventory,
updated exact-hull discussion in the source note, and
`paper-quadratic-aggregation/sections/93-formal-exact-hull.tex` with its
standalone `formal-exact-hull.tex` wrapper.

The mathematical statements match the formal interfaces: ordinary strict
hull, its closure, hull of the original weak system, strict PD and weak
PSD lifts, and all strict/weak source-good aggregation intersections.
Every headline covers `r≥2`. The two-point proof uses a perpendicular to
one weighted difference and generally unequal convex weights, which
correctly explains how it includes the four-variable case.

The review requested that the endpoint expansion explicitly restrict
`t` to the two quadratic roots, and that the closing comparison distinguish
the countable strict-description obstruction from the finite weak-description
obstruction. Both clarifications are present in the final paper. The
source note also records the direct proof and separates the unverified
arbitrary-quadratic obstruction from the proved hull result.

The source inventory records the proof obligation at scope freeze and the
subsequent direct resolution; it does not suggest that HHC alone supplied
an imported BDS hull theorem. The lift discussion preserves the exact
strict and weak scalar bounds and actual matrix conditions. The closure
argument and compact segment-union proof are accurately described.

The coordinator's verification record reports a warning-free targeted
build of all ten owned modules, an audit of 93 owned declarations with
only standard Lean axioms, ten successful kernel replays, and stable
source hashes. The paper record identifies a clean two-page PDF and
fingerprints its wrapper, macros, section, and output. These checks were
not duplicated by this review. The declaration map's qualified references
and local documentation links were separately checked.

No mathematical, scope, documentation, or paper mismatch remains in the
reviewed files. The supplement explicitly excludes a numerical SDP solver,
arbitrary-quadratic impossibility, the general hull theorem, and the
separately queued accuracy package. It does not replace review of the
concurrently developed main manuscript.
