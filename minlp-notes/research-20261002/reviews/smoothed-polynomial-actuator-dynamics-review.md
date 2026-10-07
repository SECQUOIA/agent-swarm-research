# Review of affine-state polynomial-actuator dynamics

Date: 2026-10-02. Status: approved; no mathematical or bit-complexity
blocker. No novelty claim.

This is a fresh completed-text review of the
[dynamics theorem](../new-direction/smoothed-polynomial-actuator-dynamics.md),
including its use of the
[sparse polynomial box theorem](../new-direction/smoothed-sparse-polynomial.md),
[finite-noise tails](../new-direction/polynomial-finite-noise-tails.md), and
[coefficient-height-separated fallback](../new-direction/polynomial-exact-fallback.md).
The reduction and its bit-complexity composition have no mathematical
blocker. The review checks the application of those supporting proofs;
it does not repeat their primary-source audits.

## Model and factor scopes

The completed text now specifies bounded closed rational domains,
positive rational noise half-width, and fixed degree at least one. It
detects empty control domains after inward integer rounding and states
the optimization claims only for nonempty domains. This resolves the
initial empty-domain issue: an integer control interval such as
`[1/3,2/3]` cannot have an optimizer.

Every polynomial factor must have its entire variable scope in a supplied
bag. A decomposition of a bipartite factor-incidence graph would not
suffice: one factor can touch arbitrarily many variables while its
incidence graph is a star. The sparse theorem requires the scope-in-bag
condition, equivalently a suitable decomposition of the primal
interaction graph. The final text now states this precise condition,
resolving the factor-graph ambiguity.

Under box invariance, each free point produces exactly one feasible
trajectory, and every feasible trajectory arises from its free point.
The state bounds introduce no additional restrictions on the free product
domain. Checking the stronger full-control-hull invariance by endpoint
and derivative-root comparisons has polynomial bit cost at fixed degree.
For integer controls, using their continuous hull for this check does not
relax the actual optimization domain.

## Elimination and conditional noise

The adjoint indices in (6)--(8) are correct. Expanding one recurrence at
a time cancels every dependent state and leaves
`a_0 lambda_1 s_0 + sum_t lambda_(t+1) g_t(u_t)`. Fixed-coordinate
contributions are retained as constants. Noise on substituted fixed free
coordinates is carried separately and restored to values, so it does not
make the displayed conditional polynomial depend on the remaining free
noise.

The argument allows arbitrary explicit fixed-degree free-cost factors
with the supplied scopes. They can be coupled and nonconvex. Eliminating
the affine state costs adds only unary factors, so it preserves the
degree bound, the factor-scope condition, and polynomial explicit size.
The same identity holds at every native integer label.

Conditioning on all dependent-state noise leaves the initial-state and
control noise independent with their original common finite law. The
adjoints and resulting unary polynomial coefficients can be correlated;
they are fixed under that conditioning. No independence between those
derived coefficients is needed. This distinction justifies the subsequent
bag-noise conditioning used by the sparse theorem.

The geometric bound `|lambda_t| <= (C_s+sigma)/(1-a)` is uniform over
all conditioned draws. The bounds (10)--(11) then control the reduced
coordinate curvature, Hessian row sums, and third-derivative row sums.
Termwise monomial bounds on the full hull have polynomial encoding length
at fixed degree, even when their numerical values are large.

## One common finite grid and a uniform fallback

The uniformity argument uses more than substituting a realized reduced
input into the fallback's headline theorem. Its two-block singleton
formulas have base-fixed dimensions, degree, integer-label predicates,
and atom counts even when arbitrary polynomial coefficients vary.
The reduced polynomial has polynomially many coefficients, each with
length polynomial in `I+b`. Positive denominator clearing preserves that
height bound. The elimination and univariate-refinement proofs put height
in a polynomial factor with a fixed exponent, while their exponential
dimension factor depends only on the base data. Consequently one
base-only `B` works for every conditioned objective and for later
requested-precision evaluation. The argument does not require that the
varying coefficients occur only in linear terms.

The finite-tail section count likewise depends on formula format and
degree rather than coefficient height. It remains uniform for the real
coefficient values used in the continuous-to-discrete comparison.
The active-gradient count uses the original free-variable faces and
integer assignments; dependent state bounds do not enter that count.

The constants in (15)--(16) are sufficient. The growth threshold term
and its finite-grid correction are each at most `rho/2`; the two terms
in the active-gradient bound are also each at most `rho/2`. Hence the
failure probability is at most `2 rho = 1/(2B)` for every fixed state
noise vector and after averaging over it. All quantities defining the
cutoff precede the choice of `M`. Only the polynomial height factor uses
the eventual sampling precision. There is no sampling-precision circle
or conditioning of the noise law on successful closure.

The imported pruning and patch tests are sound for every draw. On the
good event, the stated derivative bounds and cutoff give integer fixing,
active-bound fixing, and positive Hessian certification by level `J`.
On all other draws the same sampled reduced objective has an exact
fallback. Averaging its uniform budget against the failure probability
gives polynomial expected fallback work and subsequent evaluation work.
The conditional sparse count has the same uniform `L`, so averaging it
also gives (5).

## Exact trajectory output and evaluation

An implicit exact free optimizer together with the original recurrence
specifies one common exact trajectory. This does not require separate
minimal polynomials or an expanded algebraic representation of each
state. The global pruning record can still be large; the compact patch
descriptor supports subsequent evaluation after its global validity has
been established, as in the underlying sparse theorem.

For rational free inputs, the polynomial `g_t` is evaluated only at its
own control. At fixed degree its denominator length grows by a constant
multiple of that control's precision, plus the coefficient lengths.
The affine state update adds the previous state denominator length and
the current rational operand lengths. Summing these contributions over
the horizon gives polynomial bit length and polynomial exact forward
evaluation work. There is no repeated powering of a previous state's
denominator. Exact forward simulation enforces every equality, and
invariance enforces every state interval. Integer labels remain exact.

The Euclidean trajectory bound (17) is safe, including a varying initial
state and varying signed coefficients `a_t`. The absolute values of the
state propagation matrix are dominated by the finite geometric
convolution matrix. Its row and column sums are at most `1/(1-a)`, so
its Euclidean operator norm has the same bound. Its input vector is
`(Delta s_0, Delta g_0, ..., Delta g_(H-1))`, with norm at most
`max(1,G_1) ||Delta z||_2`. Including the controls themselves gives a
Lipschitz bound no larger than
`1 + max(1,G_1)/(1-a)`, which is bounded by the stated `K_traj`.
Thus the additional accuracy bits claimed in Section 5 suffice for the
entire trajectory, with no hidden horizon factor.

The reduced and original objective values agree exactly under the
recurrence, including retained constants. Feasible rational free-point
approximants and their certified reduced gaps therefore transfer to
exactly feasible rational trajectories with the same gaps. The logarithm
of `K_traj` has polynomial base length, so this transfer preserves the
expected polynomial requested-accuracy cost.

## Scope and verification

The example's exact state-image interval is `[-3/8,5/8]`. The transition
has nonzero state dependence and nonlinear control response. The
conditional value `-|gamma| sqrt(s)` has unbounded upper curvature at
zero when `gamma != 0`, so the opening fiber obstruction is correct.
It explains why this result depends on elimination rather than applying
the box proof directly to equality fibers.

The theorem's exclusions are material and correctly stated: affine
state dependence, affine dependent-state costs, a free product domain,
and a decomposition controlling free-cost factor scopes. It does not
cover arbitrary nonlinear state recurrences, nonlinear state costs,
additional path constraints, or a width promise on the original equality
graph alone. It optimizes the sampled objective exactly; no claim of
exact unperturbed optimization or polynomial expanded algebraic output
is needed.

This review performed a mathematical read of the completed text and the
relevant supporting proof sections. The author's targeted reduction and
trajectory checker is recorded in the main note and was not rerun here.
Targeted inline Python checks of this review's local links, trailing
whitespace, newline, and accidental patch markers passed. The scoped
command `git diff --check -- research-20261002/reviews/smoothed-polynomial-actuator-dynamics-review.md`
also passed; because the file was untracked, the explicit file-content
check supplies the whitespace verification. No external literature
search, project-wide verification, or CI inspection was performed.
