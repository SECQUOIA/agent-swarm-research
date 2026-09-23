# Small-power graph formulation barrier: source and sanity assessment

Date: 2026-09-05. Bounded independent assessment by `joint_flow_novelty`.
Candidate: [small-exponent-rational-formulation-barrier.md](small-exponent-rational-formulation-barrier.md).

The strengthened `Omega(D)` lower bound passes this independent sanity check
under ordinary explicit rational MILP encoding. The LP denominator argument
is classical. This search did not locate the particular consequence for
fixed vertical approximation error and binary-encoded reciprocal powers.
Treat it as a useful elementary encoding barrier, with qualified priority,
rather than a new general theory of MILP representability.

## Mathematical check

The central step survives unrestricted integer witnesses. Write the original
linear system as `A w + C z <= b`, with rational data and integer `z`.
After choosing and fixing a witness `z_*`, only the right-hand side becomes
`b-C z_*`. Clearing the original denominators makes that vector integral,
however large its entries are. The coefficient matrix of the remaining LP
does not depend on the magnitude of `z_*`.

The graph point `(2^(-D),1/2)` makes the slice `y>=1/4` nonempty. Minimizing
`x` over the corresponding fixed-witness polyhedron has an attained finite
optimum. The tube excludes `x=0` on this slice, so its optimal value lies in
`(0,2^(-D)]`. Equivalently, the tube itself implies the positive lower bound
`x >= (3/16)^D` on this slice; attainment is already enough for the argument.

Splitting free continuous variables and adding slacks gives a nonnegative
standard-form LP with an optimal basic feasible solution. The original
polyhedron need not have a vertex. An integral basis matrix has a common
determinant denominator for all its basic coordinates. Taking a difference
of coordinates to recover `x` preserves that denominator bound. An integral
right-hand side of arbitrary size affects the numerator, not this bound.

For total explicit encoding length `s`, clear denominators separately in
each original row. If `ell_i` counts that row's original rational numerator
and denominator bits, each resulting integral coefficient has magnitude at
most `2^(ell_i)`. This includes the integer columns before fixing the witness,
so the new right-hand side is integral. Its numerator can be large without
changing this coefficient bound. If the row has `t_i` nonzero coefficients,
splitting free variables and adding a slack gives Euclidean row norm at most
`sqrt(2t_i+1) 2^(ell_i)`. Both `sum ell_i` and `sum t_i` are `O(s)`.
Deleting dependent equations selects original rows; restricting to a basis
selects columns. Neither step increases the row-norm estimate. Thus
Hadamard's inequality gives
`log2 |det B| <= sum ell_i + (1/2) sum log2(2t_i+1) = O(s)`.
A positive optimal numerator is at least one, proving
`2^(-O(s)) <= 2^(-D)` and hence `s=Omega(D)`. No polynomial-size assumption on
the selected witness is used. No numerical test is needed for this algebraic
argument.

This paragraph updates the original coarse `Omega(sqrt(D))` assessment after
the first mathematical reviewer suggested row-wise denominator accounting.
The strengthened argument was independently reread here and passes this
sanity check. The classical source attribution is unchanged; this check does
not replace the separately requested full mathematical audit.

## Closest verified sources

**Classical LP arithmetic.** Ambros Gleixner and Daniel E. Steffy, *Linear
Programming using Limited-Precision Oracles* (2019), DOI
10.1007/s10107-019-01444-6, explicitly states and proves the Cramer/Hadamard
denominator bound in Lemma 1, equation (3), printed p.3 (PDF p.5). Its proof
bounds the denominator by the determinant of an integral basis matrix.
This is a direct primary source for the established ingredient, not evidence
of priority for the small-power consequence. The fixed-integer-witness
specialization above is our comparison.
[Open report](https://optimization-online.org/wp-content/uploads/2019/12/7507.pdf).

**Qualitative MILP representability.** Amitabh Basu, Kipp Martin, Christopher
Thomas Ryan, and Guanyi Wang, *Mixed-integer linear representability,
disjunctions, and variable elimination* (2016), reproduces the
Jeroslow–Lowe characterization in Theorem 2.1, printed p.2. It describes
rational MILP projections using finitely many rational polytopes and a
finitely generated integer monoid. In particular, bounded projections have
a finite rational polyhedral description by disjunction. This is relevant
background for unrestricted integer auxiliaries, but it does not supply the
candidate's numerical lower bound as stated. The original Jeroslow–Lowe
publication was not read in this bounded audit; attribution here follows
the explicitly reproduced theorem.
[Author manuscript](https://www.ams.jhu.edu/~abasu9/papers/chvatal-projection.pdf).

**Conic power formulations are a different class.** Jie Wang, *Weighted
Geometric Mean, Minimum Mediated Set, and Optimal Simple Second-Order Cone
Representation*, DOI 10.1137/22M1531257, studies formulation sizes for
weighted geometric mean inequalities in a subclass of SOC formulations.
The publisher abstract reports exact optimal size results in the bivariate
case. Only that abstract and a search excerpt of the author-hosted paper
were checked here; no detailed theorem is being invoked. Nonlinear conic
constraints and power inequalities do not contradict a lower bound for a
rational linear formulation covering an entire graph within a vertical
tube.
[Publisher abstract](https://epubs.siam.org/doi/10.1137/22M1531257),
[author-hosted paper](https://wangjie212.github.io/jiewang/research/wgm.pdf).

**Structured polynomial approximation is an adjacent question.** The
abstract of Daniel Bienstock and Gonzalo Muñoz, *LP approximations to
mixed-integer polynomial optimization problems* (arXiv:1501.00288), reports
small LP approximations under bounded treewidth. The full theorem and its
degree dependence were not audited here, so this source cannot support a
claim that binary exponent length suffices for the present approximation
criterion. The candidate's own proof makes that distinction unavoidable.
[Primary abstract](https://arxiv.org/abs/1501.00288).

## Scope and priority wording

The size measure must count explicit binary rational coefficients, rows,
and variables. Strict inequalities, coefficients supplied by arithmetic
circuits or unit-cost real constants, and nonlinear auxiliary constraints
are outside this proof. An explicitly encoded rational affine projection
can be handled by adding its defining equalities and counting their size.

The approximation requires both exact coverage of the graph and a fixed
vertical error bound. It is not merely small Hausdorff distance, a
hypograph approximation, or a tolerance on the residual `y^D-x`.
The tiny input coordinate arises from the coverage premise; the proof does
not assume an algorithm can print it using only `O(log D)` bits.

Recommended wording: “A classical rational-LP denominator bound yields an
elementary exponential encoding barrier for rational MILP outer
approximations of reciprocal-power graphs at fixed vertical accuracy. We
did not locate this specific formulation in the primary sources checked.”

Searches combined rational MILP representability, denominator and encoding
bounds, power-function graph approximation, small or binary exponents,
and weighted-geometric-mean conic representations. The search was bounded,
not a priority certification. No directly matching small-power theorem was
located; no claim that the underlying determinant mechanism is new is
warranted.
