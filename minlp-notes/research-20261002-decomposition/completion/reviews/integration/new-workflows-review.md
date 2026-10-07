# New workflow integration review

The targeted integration checks pass. No unresolved correctness defect was
found in the reviewed interfaces. This review covers connections between
modules; it does not repeat their broader component test suites.

The saved [check script](new-workflows-check.py) and
[results](new-workflows-results.json) contain 16 JSON certificate roundtrips
and 31 rejected model or proof mutations. The results record SHA-256 hashes
for the reviewed solver sources and the scalar piecewise helper.

- A quadratic instance with an effective native-integer domain, a fixed
  rational coordinate, permuted bag order, changing private active faces,
  and two tied optima is checked across convex recourse, submodular
  recourse, the original-model pipeline, and the polynomial representation.
  Its independently calculated minimum is `-22/9`.
- The same paths preserve valid original-model bounds after zero-time and
  convex-oracle caps. Polynomial stage and table caps also replay. These
  incomplete statuses make no exactness claim.
- A stiff three-piece recourse example is passed through fixed-integer
  substitution and original-index private-block mapping. The lifted
  certificate encloses the independently known minimum `1/20`, reaches
  the requested gap `1/100`, and rejects an altered piece coefficient.
- Polynomial boundary discovery returns an implicit convex-patch
  descriptor after four refinement rounds. Its sole free coordinate
  contains `sqrt(1/2)`; the monotone coordinate and the fixed integer
  coordinate are correctly fixed. Replay makes no rational-point or
  rational-value claim for that descriptor.
- Expected-model substitutions and altered nested statements are rejected.
  Direct recourse, polynomial, and boundary replay are also exercised with
  their optimization or discovery entry points disabled.

The first attempted full run encountered a temporary missing `pack_pieces`
helper while the scalar-curvature owner was editing the implementation.
The helper was added before the complete checks above; the final run passed
without a workaround.

Command run from the repository root:

```sh
python3 -B research-20261002-decomposition/completion/reviews/integration/new-workflows-check.py > research-20261002-decomposition/completion/reviews/integration/new-workflows-results.json
```

Only these topic-specific checks were run for this review. No project-wide
verification or CI inspection was performed.
