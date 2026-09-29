# Independent audit of the strict cube extreme-ray classification

Date: 2026-09-27. Reviewer: fresh adversarial subagent
`strict_cube_proof_adversary`, given the candidate note and checker without the
research conversation. The reviewer made no edits.

The reviewer found no substantive proof gap or counterexample in
[cube-strict-extreme-classification.md](cube-strict-extreme-classification.md).
The review specifically checked the local perturbation argument establishing
at least five contacts, the finite orbit enumeration, slack forcing, six-cycle
decomposition, and recovery of the five-parameter family. It confirmed that
`D+k>0` excludes the negative branch when deriving `k>0`.

The reviewer ran the targeted command

```sh
python research-20260927/check_cube_strict_extreme_classification.py
```

and reported a pass. A separate delegated audit checked the referenced
converse and exposed-ray proof, including the zero-multiple case. Its symbolic
checks covered the family nonnegativity identity, eight vertices, five
contacts, derivatives at those contacts, and principal determinants.

The main reviewer also found the closure proof in
[cube-frontier.md](cube-frontier.md) sound: the Gram integral matrices are
positive definite, the normalized family parameter image is compact and
excludes zero, and bounded integrals bound coefficients on the relevant
nonnegative polynomial cones.

The reviewer identified three missing LaTeX backslashes in the candidate note;
these were corrected. It suggested replacing “integration is a norm on its
nonnegative cone” with the precise compactness statement that the integral has
a positive minimum on the coefficient-norm unit sphere in that cone.

This is a qualified mathematical review, not a formal proof. Neither this
review nor the exact graph enumeration establishes novelty, full relaxation
completeness, or solver benefit. No project-wide or CI checks were run.
