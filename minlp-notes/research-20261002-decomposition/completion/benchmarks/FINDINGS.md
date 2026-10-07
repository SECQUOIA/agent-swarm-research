The completed implementations add exact output and broader certificates. These
measurements do not establish a speed advantage over a production solver.
The final [results table](RESULTS.md) and [JSON summary](summary.json) separate
completed solves, valid partial bounds, and input refusals.

The archived and completed grid solvers each finish 12 of the same 16
configurations at additive error `1/1024`; all 32 proof replays pass. Both finish
the new random paths through 64 variables and the 32-variable random tree.
Both fail the requested gap on the two expensive affine-recourse fixtures and
the two full binary QPLIB inputs. Their total solver-plus-checker subprocess
times are 15.18 and 15.34 seconds, respectively. This comparison jointly changes
the decomposition heuristic from minimum degree to minimum fill, the finite
message engine, and sparse polishing. It cannot attribute a timing difference
to one component. Minimum fill reduces the supplied decomposition widths on
QPLIB 3852 from 25 to 19 and on QPLIB 5881 from 95 to 93, but both still
exceed the table budget. The new per-stage table cap is 30,000, compared with 20,000 in
the separate historical experiment.

All nine exact-output configurations certify the exact optimum and pass
independent rational reference checks. They represent eight distinct models;
one simple separable model is repeated with convex presolve disabled. That
repeat is not evidence of rational reconstruction: its initial lower bound is
already exact. The new random path, width-two band, mixed model, mixed rational
example, clipped response, and false-growth example provide the nontrivial
reconstruction evidence.

The final recourse lane completes ten of eleven configurations, with all eleven
proof replays valid. Six are exact and four reach the requested error. The
17-variable shuffled affine star is reduced by 16 coordinates and certified
exactly at -1 in 0.065 seconds of solving plus 0.047 seconds of checking. The
33-variable dense minimum-cut fixture reaches error `1/1024` in 0.089 seconds of
solving plus 0.099 seconds of checking. The first recourse snapshot exhausted
its budget on these two models; the retained failure artifacts motivated a
reviewed change to candidate ordering and a direct check of uniquely forced
affine responses. Only the affected recourse lane was rerun. Its remaining
limit is the complete public QPLIB 3852 model.

Changing active sets are exercised explicitly in
`M(y1+y2-z)^2+(y1-2z+1/2)^2-z^2`, with `z` in `[0,3/4]` and private variables
in the unit box. At both `M=1` and `M=100`, the verified piecewise-curvature
backend uses 17 table states, six levels, and seven local QP queries, with the
same gap `27/65536`. The independent exact values are `-17/32` and `-809/1616`.
These two measurements illustrate the proved mechanism; they are not a broad
performance study. In the separate clipped-response fixture, the prescribed
response of `y` to `z` is not affine, but automatic preprocessing can instead
eliminate `z` as an affine function of `y`.

All five optimal-set configurations produce checked compact descriptors.
Fifteen independent membership examples cover flat continuous optima, two
separated tilted optimal segments, rejection of a nonglobal KKT point, and a
native integer coordinate whose interior integer labels are also optimal.

The constrained lane has 16 configurations: seven certified approximations,
five exact optima, one infeasibility proof, two resource limits with valid
partial bounds, and one rejected invalid TU input. All 15 available proofs
replay successfully. Every feasible reported bound encloses its independent
exact reference.

Two constrained comparisons isolate useful extensions within the same model:

- For `x0(1-x0)+(x1-1/3)^2+(x2-1/3)^2` with `x1=x2` on the unit box,
  exact optimization using coordinate hulls reaches the table limit after
  15 levels and 33,502 total processed states. Keeping unions of retained
  intervals certifies the exact value zero in 43 levels and 2,538 total
  states. Both use stationary-face LP recovery with exhaustive face search
  disabled. The successful run uses two recovery LP calls and 24 pivots.
- For `1000(x0-x1)^2+(x0-1/3)^2` with `x0=x1`, the full ambient curvature
  bound reaches the two-second exact-solve limit after 252,192 total states.
  The checked curvature bound on the equality tangent space certifies zero
  using 1,938 total states. The approximation requests succeed in both modes.

The eleven [extension diagnostics](extensions/README.md) complete seven requested
outcomes, with ten independently checked certificates. They cover a quartic
without quadratic growth, a mixed polynomial, exact native-integer value-lattice
stopping, two exact implicit boundary patches, and mixed convex/concave
submodular recourse. The fresh signed six-variable mixed QP has exact value
`-509/105`, using nine QP queries, five cuts and 88 pivots. The native-integer
polynomial certifies `-53/6` after two stages and 17 states: its positive raw gap
`1/24` is smaller than the verified value-lattice spacing `1/18`. The retained
failures include a polynomial table cap, a submodular cut cap, unsupported signed
structure, and an inconclusive symmetric boundary search.

These are deliberately small diagnostic examples. The full public binary
instances still reach resource limits, and none of the three large continuous
QPLIB box inputs passes the declared prototype input screen. No public model
was modified to make it fit. Broader practical competitiveness remains
unestablished.
