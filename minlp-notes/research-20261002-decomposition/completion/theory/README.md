# Completed theory extensions

Two extensions close specific gaps in the previous report. Both have
complete proofs, targeted exact-arithmetic diagnostics, and independent
research-agent reviews.

| Result | What is proved | Executable evidence |
| --- | --- | --- |
| [Nonunique TU output](nonunique-tu-exact.md) | Exact rational output without supplied growth for all bounded rational TU QPs; keeping unions yields an accuracy-independent state bound when each continuous coordinate has at most \(r\) optimal values | [Union/rounding checks](check_nonunique_tu.py), [saved results](nonunique-tu-results.json), [independent review](reviews/nonunique-tu-review.md) |
| [Piecewise recourse curvature](piecewise-recourse/piecewise-curvature.md) | Certified local piecewise-affine responses cancel stiff curvature across changing active sets without a global partition overlay or wider attachment scopes | [Exact scalar constructor and verifier](piecewise-recourse/scalar_piecewise.py), [checks and results](piecewise-recourse/README.md), [independent review](piecewise-recourse/review.md) |

The TU extension imports the existing general-polytope stationary-face
recovery lemma. Its new parts are union-preserving feasible filtration,
the optimal-projection state bound, and unconditional height-isolated
acceptance. The exact theorem permits continua of minimizers; the finite
projection count does not. Its width dependence remains XP, and integer
capacity costs remain explicit.

The recourse extension uses classical parametric-QP critical regions.
Its new composition replaces direct curvature by the maximal reduced
piece curvature, with downward derivative jumps justified by concavity
of the fixed-domain value function after removing its parameter
quadratic. The separating family has three pieces per block, bounded
width and conditioning independent of stiffness, and arbitrarily many
negative eigenvalues. The general theorem measures the explicit
partition encoding as input. It does not promise polynomial discovery of
a short partition. The reusable scalar constructor has a pattern budget
and may enumerate exponentially many active sets.

The theory does not resolve the unrestricted sparse algorithm depending
only on width and negative curvature divided by growth, width-FPT
coupled TU optimization, or the desired efficient algorithm for
arbitrary unknown optimal sets.

Targeted commands actually run are documented in the two linked notes.
No project-wide verification or CI inspection was performed. The saved
finite examples support specific proof and certificate obligations;
they do not establish general solver superiority.

