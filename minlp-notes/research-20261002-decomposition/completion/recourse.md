# Original-model recourse implementation

The solver now accepts an original rational `BoxQP`, discovers useful private
blocks or a minimum-cut core, solves the reduced problem, and returns a
certificate for the original objective and variables. The earlier experiments
on manually written reduced families remain historical diagnostics; these
interfaces perform the transformation themselves.

## Affine convex response

[`recourse.py`](../solver/recourse.py) implements the complete recognition
procedure from [the affine-selector theorem](../negative-curvature/adversary/affine-selector-recognition.md):
one convex box QP at the parameter-box midpoint, followed when needed by one rational LP.
It uses the common central gradient, rather than the active bounds of an
arbitrary central optimizer. Singular PSD private Hessians are supported.
A nonsingular zero-gradient block forces one affine map; exact whole-box KKT
checking accepts or rejects that map directly. A singular block continues to
the full recognition LP. This avoids expensive LPs for scalar response maps
with many attachments while preserving the complete recognition argument.
A negative result applies to an affine response over the whole continuous
parameter box, even when the retained problem also has integer coordinates.

The exact LP and convex-QP backends are capped reference algorithms. Their
successful outputs have independently checked rational witnesses; their
implementation does not have the theorem's polynomial runtime guarantee.
Failure to finish is reported separately from certified LP infeasibility.

Automatic candidate discovery tries nonnegative-diagonal continuous graph
components, their one-vertex deletions, private coordinates in leaf bags, and
single coordinates. It prioritizes fewer attachments and smaller private
blocks, so useful leaves are eliminated before expensive large candidates.
Each accepted candidate passes exact PSD, affine range,
and whole-box KKT checks. This heuristic does not find every useful partition.
Discovery and recognition are separate: rejecting a candidate leaves its
variables in the model.

Accepted responses are substituted by exact rational matrix algebra. The
pipeline recomputes a decomposition for the actual reduced interaction graph,
so fill from elimination is included. Fixed continuous and integer coordinates
are substituted before recognition. Supplied blocks use original coordinate
indices; subsequent substitutions preserve that mapping.

[`verify_recourse.py`](../solver/verify_recourse.py) checks the whole-box KKT
identities, rebuilds each reduced quadratic, checks its solver certificate, and
lifts its point to the original coordinates. It checks original feasibility
and exact objective equality. It does not solve an LP, QP, or minimum cut.
Pass the expected `BoxQP` to `verify_pipeline` to bind the certificate to an
external instance; otherwise the explicitly embedded model is the instance.

## Minimum-cut residual search

[`mincut_adapter.py`](../solver/mincut_adapter.py) exposes the earlier exact
minimum-cut oracle through the same `BoxQP` representation. It automatically
places positive-diagonal continuous variables in the core and branches on
inconsistent signed cycles to find an admissible residual, subject to the core
and search budgets. Residual variables may be continuous or integer and have
arbitrary rational boxes. Fixed coordinates are substituted and nonunit
continuous core intervals are normalized exactly.

Each query carries a rational flow and cut certificate. The adaptive core
search carries its actual queries and pruning history. Its verifier reconstructs
normalization and checks the flow, search, lift, and objective against the
original model. Exact output uses rational value separation and a final small
core face solve. A positive-diagonal nonfixed integer residual is outside this
backend's class; the integrated pipeline can use the general grid solver.

This minimum-cut adapter requires all residual coordinates to be
coordinatewise concave and sign-switchable to attractive pair interactions
after selecting the core. A separate backend handles the broader mixed class.

## Changing active sets and mixed convex/concave residuals

[`convex_recourse.py`](../solver/convex_recourse.py) accepts disjoint continuous
PSD private blocks even when no affine response works on the whole parameter
box. Exact conditional QP values and KKT witnesses supply factors to the shared
tree dynamic program. The backend uses corrected geometric grids,
min-marginal filtering, and unknown-conditioning trials on the retained
variables. It supports native integer retained variables and exact rational
output. For scalar attachments it can construct and verify exact piecewise
affine responses, then use their largest conditional-value curvature in the
grid correction. On the tested stiff family this reduces the curvature bound
from `2M+6` to `6`, including after the active bounds change. Its separate
[implementation note](convex-recourse.md) records the factor-curvature
certificate and targeted review.

Use `backend="convex"` with `blocks=[[...], ...]` in original coordinates, or
omit blocks for the pipeline's greedy PSD block discovery. Private blocks
must be disjoint and have no direct interactions between blocks. Their
attachment scopes determine the verified residual decomposition. This route
does not require global convexity of the original objective.

[`submodular_recourse.py`](../solver/submodular_recourse.py) handles the mixed
class with a jointly convex continuous block and coordinatewise-concave
endpoint variables, when interaction signs can be switched to a submodular
quadratic. Exact convex QP queries evaluate the set function. Greedy
separation and rational LP cutting planes minimize its Lovasz extension;
the completed result is an exact original-model optimum. Its independent
[verifier](../solver/verify_submodular_recourse.py) checks conditional KKT
witnesses and the global lower-bound certificate. This is a bounded reference
implementation; no polynomial iteration bound is claimed for its cutting
plane method. The root-owned backend has its own tests and review.

## Use and limits

From the solver directory:

```python
from fractions import Fraction
from recourse import solve_with_recourse
from verify_recourse import verify_pipeline

certificate = solve_with_recourse(problem, epsilon=Fraction(1, 1000),
                                  time_limit=10, max_table_states=100000)
assert verify_pipeline(certificate, problem)["valid"]
```

Set `exact=True` for exact-output mode. `backend="grid"` uses the general sparse
solver after affine preprocessing. `backend="auto"` tries mixed submodular
recourse when convex coordinates remain, then minimum-cut recourse, then the
general sparse solver if those classes do not apply. The explicit
`"convex"`, `"submodular"`, and `"mincut"` routes are also available. The returned
method and status state what actually ran and whether it finished. CLI
equivalents are available in `recourse.py` and `verify_recourse.py`.
A supplied `warm_start` uses original coordinates and is validated there;
the grid route projects it to the retained coordinates after elimination.
The specialized convex, minimum-cut, and submodular routes use their own
incumbent construction and ignore that optional hint.

Limits cover candidate count, block size, LP pivots, convex-QP faces, core size,
minimum-cut queries, refinement stages, and table states. A cooperative deadline
is shared across recognition and reduced search. Individual reference
maximum-flow calls and final small-core face enumeration are atomic; a wall
clock deadline is therefore cooperative rather than a strict process timeout.
An unfinished run still returns valid original-domain lower and upper bounds.

## Targeted verification

The command actually run is:

```sh
cd research-20261002-decomposition/solver
python3 -B -m unittest test_recourse test_mincut_adapter test_submodular_recourse test_convex_recourse -v
```

It passed 41 tests covering singular selectors, clipped-response rejection,
bound-active responses, automatically discovered multiple blocks under
permutations, fixed coordinates, arbitrary boxes, native integer residuals,
signed-cycle discovery, rational exact output, malformed certificates, and
resource limits, changing-active-set convex factors, and original-model mixed
submodular dispatch. The adapter's
[independent review](../solver/mincut-adapter-review.md) additionally compared
180 oracle problems with exact enumeration, 1,500 core-discovery instances,
1,705 malformed proof mutations, and 120 independent search replays.
The affine pipeline's [independent review](reviews/recourse-review.md) records
its separate adversarial checks, including 23 additional composition cases
for the convex and submodular routes and 63 comparisons of the nonsingular
recognition shortcut against the complete LP fallback. No project-wide checks
or CI inspection were run.
