# Controlled nonquadratic convex GDP instances

The generator is `code/minlp_solver_lab/lbesh_research/instances.py`. It defines
51 bounded one-level XOR GDPs: 45 technology
allocation problems and six coupled-region problems. These are synthetic
mechanism tests, not industrial case studies. The five allocation cost laws
share one structure; they must not be described as five independent application
domains.

## Fixed experimental design

Names have the form `lbesh.FAMILY.SIZE.sSEED`.

| Item | Values |
| --- | --- |
| Allocation family | `exp`, `log`, `reciprocal`, `quadratic`, `trig` |
| Region family | `logsumexp` |
| Size / number of units | `small` / 3, `medium` / 8, `large` / 16 |
| Pilot seed | 104729 |
| Held-out seeds for allocation | 130363, 155921 |
| Held-out seed for regions | 130363 |
| Alternatives per unit | 3 |

The size labels refer to generator dimensions, not observed solver difficulty.
The generator uses only a local `random.Random(seed)` stream, with no result
filtering, instance rejection, solver-dependent parameter changes, or search for
favorable seeds. Parameters match across the five allocation cost laws at each
size and seed. The prefix of unit parameters also matches across sizes, although
ring connections and aggregate resources change with size. This pairing permits
controlled comparisons but means observations are not independent draws across
laws and sizes.

The original 42 instances were defined before performance experiments. Nine
trigonometric allocation instances were subsequently added after independent
review identified that every original family had a supplied standard-cone
representation. The new law was prescribed for this structural reason, without
inspecting its solver performance or changing any other parameters or method
settings. Its three sizes and three seeds match the existing allocation design.
The full split now has 18 pilot and 33 held-out instances. Original instance
metadata, parameter hashes, and generator versions remain unchanged; the new
family also starts at generator version 1. This addition exercises a smooth
convex function for which this work supplies no standard-cone representation.
It makes no claim that such a representation is impossible. Cone-based
reference builders must explicitly report this family as unsupported unless a
correct additional formulation is supplied and reviewed.

The interface is `build(name)`, `MANIFEST`, `manifest()`, `parameters(name)`, and
`witness(name)`. The manifest records the split, generator version, exact
variable and row counts, and a SHA-256 digest of canonical JSON parameter data.
`parameters()` exposes the data to archive beside an experiment. Every model is
initialized at the same explicit feasible witness for every method. The witness
is not an optimality claim, and `known_optimum` is deliberately `None`.

Use pilot seeds to repair and configure algorithms. Freeze algorithm settings,
budgets, solver versions, and inclusion rules before performance evaluation on
held-out seeds. Structural construction and witness validation do not inspect
held-out solver performance. If a later bug requires rerunning the held-out set,
report the repair and rerun all affected methods; do not preserve a nominal
unseen-data claim. Retain failures and timeouts. Report family-level results and
paired instance results, not just an aggregate over these related generators.

## Technology allocation

Unit i produces two products x[i,0], x[i,1], each bounded by U[i], where U[i] is
uniform in [0.8,1.2]. A global row also imposes their sum at most U[i]. Its XOR
selects off, standard, or efficient operation. Off fixes production and cost to
zero. Standard capacity is between 0.58 U[i] and 0.68 U[i]; efficient capacity is
U[i]. Standard has lower fixed charge and higher operating coefficient. The
coefficient intervals are disjoint, so this tradeoff holds in every instance.
Neither technology globally dominates the other by construction.

For operating mode j, the cost epigraph is

    t[i] >= U[i] a[i,j] (w[i,0] phi(x[i,0]/D[i])
                        + w[i,1] phi(x[i,1]/D[i])
                        + c[i] phi((x[i,0]+x[i,1])/(2 D[i]))),
    D[i] = 1.1 U[i].

All weights and operating coefficients are positive. The five laws are

| Family | phi(z) | phi''(z) |
| --- | --- | --- |
| `exp` | (exp(3z)-1)/(exp(1.5)-1) | 9 exp(3z)/(exp(1.5)-1) |
| `log` | -log(1-z)/log(2) | 1/((1-z)^2 log(2)) |
| `reciprocal` | 1/(1-z)-1 | 2/(1-z)^3 |
| `quadratic` | 4 z^2 | 8 |
| `trig` | (1-cos(1.5z))/(1-cos(0.75)) | 2.25 cos(1.5z)/(1-cos(0.75)) |

Each law is zero at zero and one at z=1/2. This normalization does not equalize
derivatives or Hessians. Every argument lies in [0,10/11] on the entire variable
box, even when the global capacity row is violated by an intermediate point.
Thus the log and reciprocal domains have a margin of at least 1/11 from their
singularity, including inactive disjunct evaluations and box-based relaxations.
For the trigonometric law, 0 <= 1.5z <= 15/11 < pi/2; its first derivative is
1.5 sin(1.5z)/(1-cos(0.75)) >= 0, and its second derivative is strictly positive.
Convexity is needed only on this box and is not asserted on all real numbers.
All five laws are increasing and convex on this interval. Positive sums of
their affine compositions are convex. Subtracting t[i] preserves convexity.
The finite t[i] bound is 1.05 times the maximum cost of either operating mode
at x[i,0]=x[i,1]=U[i]. Monotonicity proves that this bound cannot exclude the
minimum cost epigraph value at any production point in the box.

The global rows contain separate product demands, a weighted linear resource
budget, and the sparse-ring congestion constraint

    sum_i ((x[i,0] + 0.35 x[(i+1) mod n,1])/U[i])^2 <= B.

The last row is convex because it is a sum of squares of affine forms. It
couples neighboring units; nonlinear mode costs couple products within a unit.
The model therefore has continuous interactions beyond independent one-variable
cost curves. Nevertheless, the allocation structure remains deliberately small
and controlled, and it does not establish transfer to general GDP applications.

The witness selects standard operation everywhere and sets
x[i,0]=0.28 U[i], x[i,1]=0.22 U[i]. Demands equal these aggregate productions.
The linear resource and congestion limits equal 1.08 times their witness
values. The standard capacity exceeds witness production 0.50 U[i]. Set t[i]
equal to its standard cost. All global and active-disjunct rows then hold, as
do every variable bound. Thus every instance is feasible independently of an
optimization run.

Each allocation instance has 3n continuous variables, 3n indicator binaries,
n XORs, 3n disjuncts, n+4 global constraints, and 6n disjunct constraints. Exactly
one global row and 2n disjunct rows are nonlinear. The objective is the linear
sum of t[i] and mode fixed charges. Quadratic controls have convex quadratic
rows only and permit an exact conic hull baseline. The nonquadratic rows are
truly nonlinear disjunct rows in the original GDP; they are not solely global
objective terms.

## Coupled exponential regions

The second mechanism places each two-dimensional x[i] in one of three smooth
convex regions. Each coordinate lies in [-2,2]. Mode j imposes

    sum_(p=0,1) (exp(s[i,j,p] (x[i,p]-c[i,j,p]))
                 + exp(-s[i,j,p] (x[i,p]-c[i,j,p]))) <= r[i,j].

This is equivalent to a log-sum-exp sublevel set (taking the logarithm of both
sides). The implemented sum-of-exponentials form avoids adding a redundant
logarithm. Mode centers are independent perturbations of (-0.75,-0.35),
(0.25,0.70), and (0.80,-0.45); perturbations are bounded by 0.08 per coordinate.
Scales are in [1.7,2.3] and radii in [4.8,5.6]. Each exponential has an affine
argument, so the row is convex on all of R^(2n). It is genuinely nonquadratic
and defines mode feasibility directly, rather than an operating-cost epigraph.

Global rows require sum_i x[i,0] >= 0 and sum_i x[i,1] >= 0.1n, and impose

    sum_i (x[i,0] - 0.5 x[(i+1) mod n,1])^2 <= t,
    sum_(i,p) (x[i,p] - x[(i+1) mod n,p])^2 <= 0.55n.

Both rows are convex. The bound 0 <= t <= 9n is valid for the minimum epigraph
value throughout the coordinate box because each first-row difference has
absolute value at most 3. The linear objective has positive, nonuniform
coordinate prices, a 0.1 coefficient on t, and small mode fixed charges.

The witness selects mode 1 at each unit and sets x to that mode's center.
Every active region row has left side exactly 4 < 4.8. The demand sums are
strictly feasible because witness coordinates exceed 0.17 and 0.62. Each
neighboring coordinate difference has absolute value at most 0.16, so total
variation is at most 2n(0.16)^2 = 0.0512n < 0.55n. Set t to the congestion sum;
its bound follows from the coordinate box. This proves feasibility for all
random draws, not just the chosen seeds.

Each region instance has 2n+1 continuous variables, 3n indicator binaries,
n XORs, 3n disjuncts, four global constraints, and 3n disjunct constraints.
Two global rows and all 3n disjunct rows are nonlinear. These instances add
nonquadratic disjunct geometry; their invented coordinates and prices should
not be presented as calibrated facility-location data.

## Verification and limitations

Initial targeted verification built all 42 models and checked the declared
variable counts, finite bounds, initialized variable values, global rows, and
every selected disjunct row at the explicit witness, with maximum allowed
residual 1e-9. It performed no solver runs and inspected no CI. The command was
a `.venv/bin/python -` script from `code/minlp_solver_lab`; it imported
`MANIFEST`, `build`, and `witness`, traversed ordinary global constraints and
mode-1 constraints separately, and checked all original GDP variables including
indicator binaries. The environment was Python 3.13.11 and Pyomo 6.10.1.
Generation uses Python's standard library and Pyomo; it adds no dependencies.

A second `.venv/bin/python -` check extracted each of the five small pilot
models using `lbesh.structure.extract`, verified the manifest's nonlinear-row
counts, and evaluated every nonlinear function and gradient at its witness,
lower variable-box corner, and upper variable-box corner. All values and
gradients were finite. This is a domain and interface check, not a numerical
proof of convexity; the convexity proofs are given above.

After adding `trig`, a further `.venv/bin/python -` check compared every original
manifest entry with a saved snapshot and found all 42 unchanged. It checked
the nine new models' witness feasibility, variable bounds and counts, the
51-instance split counts, the scalar law's normalization, and the strict
convexity interval inequality 15/11 < pi/2. For each of the three new pilot
sizes it also extracted all nonlinear rows and verified finite function values
and gradients at the witness and both variable-box corners. All checks passed;
no solver runs or held-out performance evaluations were made for this addition.

The feasible witnesses provide primal upper bounds, not optimal references.
Small cases have only 3^3=27 assignments and permit independent enumeration of
convex continuous subproblems. Validated lower bounds or independently checked
convex optimality conditions are still needed to certify reference objectives.
A local NLP solver success message alone does not provide such a certificate.
Published conclusions also need external models: these synthetic families were
constructed to exercise particular algorithmic mechanisms, and family diversity
or numerical scaling alone cannot establish practical superiority.
