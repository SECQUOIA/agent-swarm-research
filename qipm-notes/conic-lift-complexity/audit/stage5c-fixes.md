# Stage 5C corrections

The separate fixer applied all five minor corrections accepted in
[stage5c-assessment.md](stage5c-assessment.md) on 2026-09-20. No theorem
hypothesis, proof, formula, or historical stage record was changed.

1. The introduction now specifies an **integer** cone-dimension cap
   `d >= 3`, matching `cor:dimension-resources`.
2. The introductory PSD comparison now states `0 < mu <= 1 <= L`,
   matching `newt:linear` before taking inverses of the comparison constants.
3. The computational summary now attributes the common exposing certificate
   and fresh per-round charge to **our rank-dependent work bound**. It no
   longer asserts these are necessary for every movement/work composition.
   The wording agrees with the premises and proof of `work:total`.
4. The remaining bounded narrow-cap interval is explicitly restricted to a
   fixed-field Hermitian order cap or a Lorentz dimension cap, with `B`
   identified as that cap's primitive capacity. This matches the family
   stated at `eq:unsettled-range` and avoids suggesting a complete boundary
   for arbitrary mixed dictionaries.
5. The abstract now says global differentiable selections **can impose**
   additional topological costs, allowing the matching direct-cone cases.

The README and source-map opening now refer to the workflow record for the
current status of stage reviews and the separate whole-manuscript review.
This replaces temporary status prose without changing the coverage inventory,
its dispositions, or historical author records. The workflow itself was not
edited.

Validation used the required `qipm` environment:

```sh
conda run -n qipm --live-stream make clean
conda run -n qipm --live-stream make
```

Both commands completed successfully. Their complete logs are
[stage5c-fixes-clean.log](stage5c-fixes-clean.log) and
[stage5c-fixes-build.log](stage5c-fixes-build.log). The rebuilt PDF has
**183 pages**, **499 unique labels**, and **87 bibliography items**.
The final LaTeX log contains no warnings, undefined or multiply defined
references, or overfull/underfull boxes; the BibTeX log contains no warnings
or errors. A separate source check confirmed all five corrected passages.

These corrections complete the assigned minor-fix work. Root verification
and the separately required five-reviewer whole-manuscript cycle remain
outside this fixer's assignment.
