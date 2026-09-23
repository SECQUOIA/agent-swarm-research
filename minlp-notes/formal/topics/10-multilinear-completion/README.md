# Complete mathematical coverage of the multilinear paper

This package completes the mathematical coverage of
[`paper-multilinear-gap`](../../../paper-multilinear-gap/README.md).
The earlier packages prove the disproof, exact finite formula, and sharp
leading degree and dimension growth. This package adds the paper's remaining
envelope, construction-size, family-asymptotic, and numerical-example claims.

## Where to look

- [Paper and standalone distribution](../../../paper-multilinear-gap/README.md).
- [Paper-to-Lean coverage](../../../paper-multilinear-gap/formal/COVERAGE.md).
- Canonical proof sources: [`Formal/MultilinearGap`](../../Formal/MultilinearGap).
- [Earlier exact formula](../08-exact-multilinear/README.md).
- [Earlier sharp growth](../09-sharp-multilinear/README.md).

The canonical sources are maintained in `formal/`. The standalone paper
contains an exported dependency closure, which must agree byte for byte with
those sources. Do not develop separate versions of a proof in the two places.

## Completion requirements

The completion audit includes mathematical statements in prose as well as
numbered theorems. It checks general envelope attainment, exact individual
monomial envelopes, comparison of the full and original-term gaps, exact
construction counts and sparsity bounds, actual family asymptotics, and all
four printed examples. Different proof routes are permitted when they prove
the same statement about the original graph hull.

Completion requires a warning-free integrated build, complete module imports,
transitive axiom audit, kernel replay, an updated standalone export, checked
paper build, and an independent claim-to-statement review. Literature priority,
external peer review, and correctness of Lean's implementation are not
mathematical claims proved by this package.

Status: complete. The integrated canonical checks and the standalone package
checks passed, including both kernel replays. See [the verification record](VERIFICATION.md).
