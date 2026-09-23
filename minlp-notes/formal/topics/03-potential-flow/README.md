This topic verifies rational certificates for finite potential-flow networks with
positive asymmetric quadratic edge laws. Start with
[`accepted_sound`](../../Formal/PotentialFlow/Results.lean), or the checked
[`saved_example_verified`](../../Formal/PotentialFlow/ExampleResults.lean).

Lean proves that an accepted rational certificate establishes a unique physical
flow, bounds its energy error, and encloses every edge flow and pressure drop.
The saved five-node, six-edge example has certified flow error below `1/5000`
on every edge. Candidate flows and potentials need not already be optimal.

Proofs are in [`Formal/PotentialFlow`](../../Formal/PotentialFlow). The
[coverage table](COVERAGE.md) maps claims to modules; the
[verification record](VERIFICATION.md) links build and kernel-check results.

The generator translates the saved JSON into exact rational Lean data. Its
output is checked by Lean; the generator and numerical solver are not trusted
proof steps. Check that the data is current with:

```bash
python3 topics/03-potential-flow/generate_example.py --check
```

Run this command from `formal/`. The deterministic network is verified; the
separate construction of an uncertainty envelope from an original problem is
not part of this package.

The remaining certified-computation mathematics of the same appendix -- separate-edge
Bregman intervals, posterior scenario recovery, support certificates for linear goals
with their completeness and convergence, and the conservation-aware curvature bounds --
is verified separately in [topic 16](../16-potential-flow-certificates/README.md).
