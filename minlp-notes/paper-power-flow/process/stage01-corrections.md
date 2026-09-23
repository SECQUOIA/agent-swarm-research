# Stage 1 corrections

Applied all three accepted findings from
`assessments/stage01-round01.md`:

1. Proposition 2.3 now explicitly identifies the source-to-network extension
   as the rational homeomorphism and restriction to designated buses as its
   inverse.
2. The abstract now requires both polynomial-size certificates and
   deterministic polynomial-time verification in the certificate consequence.
3. The complement path uses text em-dashes with binary-operator spacing to
   represent connections instead of adjacent mathematical minus signs.

Compared both edited manuscript files against the frozen stage-1 snapshot.
Only these three passages changed; no equations, gadget data, or proofs changed.

Validation: the documented `latexmk -pdf -interaction=nonstopmode
-halt-on-error -outdir=build main.tex` command completed successfully. The actual
output is saved in `stage01-corrections-build.log`; it reports no warnings or
overfull/underfull boxes. No broad mathematical tests were repeated for these
wording and typography changes.
