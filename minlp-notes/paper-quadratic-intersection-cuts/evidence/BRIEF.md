# Manuscript brief

Write a complete anonymous journal manuscript on the limits and guarantees of
quadratic intersection cuts. The manuscript must stand alone: no theorem or
essential proof may depend on a repository note, an author report, or a promised
companion manuscript. Use plain, precise prose and explain the geometry before
introducing technical statements. Leave authors and the date blank.

The authorized source package consists of the intersection-cut program in:

- `research-20260928b/sfree/optimal-intersection-cuts.md`;
- `research-20261001/intersection-literature/note.md`;
- `research-20261001/ratio-bound/note.md`;
- `research-20261001/orbit-closure/note.md`;
- `research-20261001/minor-sets/note.md`;
- `research-20261001/multiround/note.md`;
- `research-20261001/scip-rule-fidelity/note.md`;
- `research-20261001/scip-set-selection/note.md`;
- their reviews, exact certificates, saved computational records, and the final
  corrections in `research-20261001/CLOSEOUT.md`.

Treat the corrected October closeout as a guide to superseded claims, then
inspect and verify the actual proofs. Separate unrestricted sets, the bilinear
orbit, its maximal completions, closures, and successive reoptimization.
Separate nonnegative and positive objective weights, supremum and attainment,
exact certificates and numerical bounds, and local strength and solver work.

Preserve every substantive in-scope development, using appendices where needed.
Resolve missing hypotheses and proof gaps within the authorized topic. Retain
honest open extensions without making an established theorem depend on them.
If a result is false, repair it or document its exclusion and the reason.

Do not rerun computational experiments. Existing records may be trusted, but
their transcription, cohort definitions, provenance, and claimed implications
must be checked. Exact symbolic proof arithmetic and targeted document checks
are allowed. Do not run project-wide verification or inspect CI.

All literature research and additions use GPT Luna with maximum reasoning.
One reusable agent owns the `$lit` session and serializes knowledge-base work.
Other agents must send literature requests to the lead; they must not start
independent literature searches or knowledge-base maintenance sessions.

The final deliverables are a polished PDF, portable LaTeX submission sources,
an evidence companion for existing certificates and records, a coverage map,
resolved independent review reports, and an accurate verification record.
