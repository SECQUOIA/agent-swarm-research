# Root audit before Stage 1 review

The authoring request authorizes implementation and verification work as well as
writing. The earlier read-only assessment is superseded for this topic. Other
paper folders, including concurrent work in `paper-correlated-measurements/`,
remain outside this task.

## Reproduced current checker failure

The current `certify.driver.check_certificate` accepts a false bound even when
called with `require_vipr=True` and the installed `viprchk` executable. A model
with one continuous variable, `min x` subject to `x >= 1`, an empty nonlinear
lemma list, the byte-identical rational master, and the repository's
`certify/tests/review_artifacts/bogus2.vipr` returns `ok=True` and the bound
`1000000`. The actual optimum is `1`. The VIPR problem section matches the master.
The exploit uses a `sol` inference with `SOL 0`; the pinned external checker
initializes its best objective to zero. Removing the producer's SOL-dropping
fallback did not protect the accepting checker against this proof.

This is a repairable implementation defect, not a counterexample to the safe-cut
lemma or the mathematical master-bound transfer. A strict proof guard and
adversarial regression are required before claiming checker soundness.

## Saved artifact inspection

All 269 files marked verified in `cert_all.jsonl` are present. Their completed
VIPR proofs occupy 41,247,819,032 bytes; the largest is 2,163,285,624 bytes. The
larger certificate directory includes raw proofs and failed attempts as well.
There are 258 files with positive SOL counts and 11 files with SOL 0. Root
streamed the complete remaining proof text of all 11 SOL-0 files and found no
`{ sol }` inference. Consequently this particular exploit does not establish
that the saved bounds are false. Full revalidation under the repaired checker
and consistent mathematical input semantics remains necessary.

## Additional obligations

- The default checker API permits success without checking a VIPR proof. Partial
  lemma/master checks must be distinguished from complete bound verification.
- Curvature classification and cut evaluation currently normalize expressions
  through different floating-point paths. One exact interpreted model is needed.
- The safe-cut condition over the whole box is sufficient for cut validity; its
  current docstring's claim of necessity is false and must be corrected.
- Halbig et al. (INFORMS Journal on Computing, 2024) already construct and verify
  convex-MINLP optimality certificates. The new paper cannot claim the first
  convex-MINLP certificate or the first independent verification method.
- The existing 269-instance result is historical computational evidence until
  its model contract and proof checks are established by the final implementation.
