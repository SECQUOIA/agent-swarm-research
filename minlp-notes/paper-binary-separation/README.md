# The separation complexity of hypermetric and binary quadratic inequalities

The manuscript develops the binary-separation results into one anonymous
journal paper with complete proofs. The submission files are
[main.pdf](main.pdf) and [submission-source.zip](submission-source.zip).
[BUILD.md](BUILD.md) gives the standalone build command.

The central result is strong NP-completeness of unrestricted hypermetric
separation, with hard points in the metric polytope and the elliptope interior.
Switching and a positive definite orthogonal extension prove the corresponding
results for the related binary families. The paper also gives short
certificates, rank and normalized-threshold algorithms, general-integer
boundary examples, and NP-completeness of gap-zero separation. General gap
separation at positive semidefinite points is explicitly outside the resolved
classification.

The paper has no dependency on the internal research notes or their programs.
No computational experiments were rerun or added. The proof audit, independent
mathematical and editorial reviews, and literature audit are recorded below.
These are internal reviews, not journal peer review.

| Location | Contents |
|---|---|
| `sections/` | Complete manuscript proofs and discussion |
| `references.bib` | Bibliography used by the manuscript |
| `evidence/coverage.md` | Result coverage and provenance |
| `evidence/literature-audit.md` | Inspected sources, attribution, novelty, and access limits |
| `reviews/` | Source audits and independent manuscript reviews |
| `evidence/review-resolution.md` | Disposition of review findings and corrections |
| `verification/VERIFICATION.md` | Targeted build, reference, layout, and archive checks actually run |

The literature workflow used GPT Luna with max reasoning and the
[`lit` skill](/workspace/local-home/repo/skills/literature/SKILL.md). Source papers and
reading records are maintained in the local, git-ignored literature collection;
they are not redistributed with the submission archive.

The archive includes only the manuscript, bibliography, and build instructions.
Evidence and review files remain here for inspection. The earlier notes,
existing experiment records, and unrelated manuscript folders are preserved.
