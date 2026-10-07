# Root mathematical integration findings

## One witness inequality covers smooth and nonsmooth quadratic recourse

Let W(a) be the minimum, over a compact fixed feasible set, of functions
whose Hessian with respect to a is alpha times the identity. Any attaining
witness at v supplies an upper model

    W(a) <= W(v) + s_v^T(a-v) + alpha ||a-v||^2 / 2.

For V(a)=W(a)+d^T a, substitute a=v-(s_v+d)/alpha. The global minimum
V* then satisfies

    ||s_v+d||^2 <= 2 alpha (V(v)-V*).

This argument needs neither differentiability nor uniqueness of the witness.
For quadratic completion recourse, s_v=alpha(v-Tx_v). On an active KKT
region, the extracted quadratic's derivative equals this witness vector
because the selected active equalities are constant along the affine chart.
Different charts must agree in value where both are valid; their gradients
need not agree when W is nonsmooth. This independently confirms the Sol
audit's proposed removal of the unnecessary kernel-inclusion hypothesis in
the supplied-factor closure theorem. The normalized intrinsic corollary
still satisfies it automatically.

The descent point can be outside the search box: the argument is valid on
all auxiliary space, and square completion shows equality of the global
auxiliary minimum and the minimum on the base-selected box. The paper must
state that equality before using the witness inequality.

A simple test case is F(x)=-x^2 on [-1,1], T=1 and alpha=2. The residual
Hessian P is zero and violates kernel inclusion. The envelope is
W(a)=a^2-2|a|, nonsmooth at zero; either endpoint x=+1 or x=-1 attains
the inner minimum there. Each supplies the required quadratic upper model.
An inline exact-Fraction diagnostic checked 210 cases over 41 rational
query points and five tilts, including both witnesses at zero. It verified
the descent inequality and upper model. This is a finite proof diagnostic,
not a computational experiment or substitute for the general argument.

## Strong-noise persistence is a separate route

The random-component results use global derivative enclosures to pin many
coordinates before decomposing the remaining primal graph. They do not
require small treewidth or a fixed core, and their sufficient noise scale
is substantially stronger. They belong in the coverage inventory and
paper, with the exact component solver shared with integer-core closure.
They use exact component solves on every draw rather than a separate rare
fallback. The global value may remain a sum of algebraic component
expressions; small expanded degree or easy sign tests of this sum do not
follow.

## No performance claim from proof fixtures

The retained exact-arithmetic fixtures check identities and invariants on
small cases. They are neither an implementation of all polynomial-time
oracles nor empirical verification of an expectation theorem. The paper
can describe them as supporting mathematical diagnostics, but must not
turn them into a benchmark or practical-complexity claim.

## Positive conservative enclosures in stopping formulas

Whenever an enclosure is used in a divisor or in a Taylor step radius, take
a positive conservative enclosure, such as the maximum of one and the computed
bound, or state a separate zero case. In particular the small-multiplier
argument uses a positive Hessian enclosure K3. The actual multiplier Hessian
may be zero (for example in a quadratic problem); that does not justify
dividing by zero or setting a release threshold by an undefined formula.
Increasing this analytical enclosure changes precision only, not the primary
L/sigma state factor.

## Noise law and integer label isolation

Do not extend the general coupled-MIQP label-isolation argument to aligned
factor noise without another proof. Distinct integer labels can have the same
factor image and remain tied on every aligned draw. For example, add a free
integer z in {0,1} with zero unary cost to -x^2 on [-1,1], and use T=(1,0).
The aligned perturbation affects x only. Independent ambient integer
coefficients remove such persistent ties with the stated finite-law budget.
The separable mixed theorem has a different scalar-recursion argument and can
permit persistent ties without requiring a unique integer label.
