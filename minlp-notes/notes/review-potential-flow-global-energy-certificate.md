# Independent code audit: global resistance-design certificate

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: PASS.** I checked the certificate argument in the final section
of [the design note](potential-flow-global-energy-maximization.md), the
complete [standard-library verifier](../code/potential_flow_mpd/energy_design_certificate.py),
and its saved example. I found no soundness defect. The verifier checks
a global design gap for the complete instance encoded in the certificate,
not only an energy gap at a fixed profile.

## Global upper and selected-profile lower bounds

The verifier uses outgoing-minus-incoming incidence. It checks the
rational trial flow satisfies `Ay=b` exactly. For every admissible
resistance profile, minimum primitive energy is at most the energy of
that same conserved trial flow. With `w_e=|y_e|^3/3`, the certificate's
nonnegative multipliers satisfy the exact LP dual equality
`R^T lambda=w`. Thus `U=c^T lambda` bounds trial energy, and therefore
physical primitive energy, uniformly over the entire encoded polytope.
The multiplier order matches the assembled rows: upper box rows, lower
box rows, then additional polytope rows.

The selected resistance profile is checked against every one of those
rows. Its positive resistance box is validated separately. For its
potentials, the exact inequalities
`beta_e*t_e^2>=|pi_u-pi_v|^3`, together with `t_e>=0`, make `t_e` upper
bounds on the conjugate radicals. Fenchel weak duality therefore gives
`L=b^T pi-(2/3)sum_e t_e<=V(beta_selected)`. The roots need not be
minimal enclosures: any valid upper bounds produce a sound, possibly
looser lower certificate.

Combining these inequalities and `D=3V` gives exactly

```
max_P D-D(beta_selected) <= 3(U-L).
```

The code checks nonnegativity of this gap and that it is within the
claimed nonnegative tolerance. Both returned global lower and selected-
profile lower bounds are `3L`, which is valid because the selected
profile belongs to the polytope. The global upper is `3U`. There is no
claim that the arbitrary supplied potentials are the selected physical
potentials, or that its physical flow is rational.

The triangle example checks exactly: trial weights are all `1/24`, the
sum constraint gives `U=1/4`, and the supplied potentials and root bounds
give `L=1/4`. Thus maximum dissipation and the selected profile's actual
dissipation are both `3/4`.

## Input validation and graph scope

Every numeric vector and matrix row has its dimension checked before
any dot product or zipped arithmetic. The exact field set is enforced.
Numbers are accepted only as Python integers or exact rational strings;
booleans and floating-point values are rejected. Invalid fractions,
nonfinite numeric strings, negative roots, nonpositive resistance lower
bounds, reversed boxes, and malformed rows fail before acceptance.
Exact decimal strings, if supplied, denote their exact rational values.

The graph validator checks integer vertex indices, excludes loops,
and verifies connectedness. Parallel arcs, including oppositely oriented
parallel arcs, are allowed and are mathematically valid here; every
arc retains its own resistance and flow coordinate. The one-vertex,
zero-edge, zero-nomination case is valid. Multiple disconnected vertices
are rejected. Balanced nominations and trial conservation are checked
independently.

No potential gauge is enforced. This is sound: balanced nominations
make `b^T pi` invariant under a common shift, and all conjugate terms
depend only on differences. The independent checks below explicitly
test this invariance.

Every acceptance condition uses the unconditional `require` function.
The verifier has no `assert`-based validation that disappears under
`python -O`. CLI verification performs all checks before printing a
result. The certificate describes its own graph, nominations, box,
and additional design rows; validating correspondence to a separately
specified external model remains the caller's ordinary responsibility.
No uncertainty-model construction is hidden outside the encoded data.

## Independent exact and adversarial tests

I added
[a separate checker](../code/potential_flow_mpd/check_energy_design_certificate_review.py).
It uses exact rational known physical states, not numerical optimization.
The tests passed:

- 96 signed-flow tree certificates across one to twelve vertices,
  including exact optima and exactly known nonzero global design gaps;
- the in-memory and saved zero-gap triangle examples, and a two-arc
  parallel graph with opposite orientations, for 99 valid certificates;
- 99 potential-gauge shifts, with identical certificate results;
- 151 malformed direct inputs, all rejected;
- 294 corrupted CLI files, each rejected under normal or optimized
  Python with a nonzero exit status and no successful result on stdout.

The malformed cases cover missing/extra fields, wrong dimensions,
floating-point and boolean data, invalid rational strings, graph indices
and connectivity, nonconservation, box/polytope infeasibility, negative
or incorrect dual multipliers, underestimated roots, and an invalid
zero-gap claim. Weakening a global polytope bound while retaining its
old claimed zero gap is also rejected by the global upper/lower check.

On the tree family, conservation fixes the physical flow for every
design. The independently computed global maximum is obtained at the
box upper profile. The tests compare the verifier's global upper,
selected-profile lower, and certified gap against those exact physical
quantities, rather than merely checking that the verifier accepts its
own demonstration data.

These checks validate certificate soundness and rejection behavior.
They do not test a numerical certificate-generation algorithm or supply
a performance guarantee for finding tight certificates.
