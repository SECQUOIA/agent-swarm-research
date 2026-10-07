# Objective noise does not remove sparse affine feasibility hardness

Date: 2026-10-02. Status: proved reduction, independently checked.
This note gives a barrier to extending the expected exact optimization
bound in [the polynomial box theorem](smoothed-sparse-polynomial.md) to
arbitrary sparse affine constraints. A separate example identifies a
failure of its coordinatewise counting proof even for a TU constraint.
Neither example is a lower bound for every constrained optimization
algorithm under stronger geometric assumptions.

## 1. A width-three, always-feasible reduction

Consider a SUBSET SUM instance with positive integers `a_1,...,a_n,B`.
Set

```text
A = sum_i a_i+B.
```

Introduce binary variables `t,z_1,...,z_n,w_1,...,w_n` and continuous
variables `s_1,...,s_n in [0,1]`. Substitute `s_0=0`. Impose only affine
equalities:

```text
z_i+w_i=t,                         i=1,...,n,
s_i=s_(i-1)+(a_i/A)z_i,            i=1,...,n,
s_n=(B/A)t.
```

Every coefficient has absolute value at most one, and every equality
has at most three nonconstant variables. The encoding length is
polynomial in the SUBSET SUM input length. All variable domains have
width one.

The all-zero point is always feasible. It is the only feasible point
with `t=0`: the first equalities force `z_i=w_i=0`, and the state
recurrence then forces every state to zero. For `t=1`, the first
equalities give `w_i=1-z_i`, and the remaining equalities give

```text
s_i = (sum_(j<=i) a_j z_j)/A,
sum_i a_i z_i=B.
```

Every resulting state lies in `[0,sum_i a_i/A]`, which is contained in
`[0,1]`. Thus a point with `t=1` exists exactly when the SUBSET SUM
instance is a yes-instance.

Use path bags

```text
P_i={t,s_(i-1),s_i,z_i},            i=1,...,n,
```

with `s_0` omitted, and attach to each `P_i` a leaf
`L_i={t,z_i,w_i}`. The final equality belongs to `P_n`.
The bags containing `t` form the whole tree; the bags containing each
state or label are connected. This is a tree decomposition of the
constraint and objective scopes with largest bag at most four, hence
treewidth at most three. It uses `2n` bags.

## 2. Every bounded objective perturbation preserves the answer

There are `m=3n+1` variables. Let the base objective be `F_0=-t`, and
perturb every variable independently as in the polynomial box theorem,
with

```text
sigma=1/[10(3n+2)],
F_gamma(x)=-t+gamma'x,
|gamma_i|<=sigma.
```

The argument only uses the displayed bounds; independence and the
specific law are unnecessary for the separation. Since every coordinate
lies in `[0,1]`,

```text
|gamma'x| <= m sigma < 1/10.
```

The `t=0` point has objective exactly zero. Every feasible `t=1` point
has objective strictly below `-9/10`. Consequently, on every permitted
perturbation, every exact optimizer has `t=1` on yes-instances and
`t=0` on no-instances. Reading its binary label solves SUBSET SUM.
The same separation would suffice for any optimization output with a
certified error smaller than `9/10` and a feasible incumbent.

In particular, an extension of the polynomial box theorem whose expected
bit-work bound remains polynomial on this family would give a Las Vegas
expected-polynomial-time algorithm for SUBSET SUM. This is a zero-error
randomized consequence, not a deduction that `P=NP`.

For this consequence, use an efficiently sampled finite rational noise
law with polynomial coefficient encoding length, as in the theorem.
For example, its independent uniform laws on `M` equally spaced values
apply whenever `M` is a base-computed power of two with polynomial
`log M`. Sampling then takes polynomially many random bits and ordinary
bit operations. An unspecified oracle for exact continuous random reals
would not by itself yield this Turing-model consequence. No resampling
or favorable-noise event is needed: the reduction works on every draw.

The objective is linear, so the theorem's positive diagonal-curvature
bound can be `L=1`. Here `p<=4`, `w_max=1`, and `1/sigma=O(n)`.
Thus a direct constrained analogue of its displayed bound, with the
constraint encoding included in the input length, would be polynomial.

Bounding coefficient magnitudes does not bound denominator sizes,
Hoffman constants, feasible-repair constants, or matrix conditioning.
This reduction does not claim total unimodularity or uniform bounds on
any of those quantities. A constrained theorem may avoid the barrier by
imposing additional structure or by charging parameters that are large
on these instances. Stable unconstrained forward repair also does not
apply: the state coefficient is one, the terminal equality adds a global
restriction, and the controls are binary.

## 3. A TU obstruction to the coordinatewise counting argument

A different example shows why the conditional semiconcavity proof cannot
be imported unchanged, even when the constraint matrix is TU. Take
`v_1,v_2,y in [0,1]`, impose the single inequality

```text
y >= v_1-v_2,
```

and minimize `2y+gamma_1 v_1+gamma_2 v_2+gamma_y y`, where each noise
coefficient is independently uniform on `[-1/2,1/2]`. The single
constraint row, together with coordinate bounds, is totally unimodular.
Conditioning on `gamma_y`, the value function for bag `{v_1,v_2}` is

```text
V(v_1,v_2)=kappa max(0,v_1-v_2),
kappa=2+gamma_y in [3/2,5/2].
```

This function has an upward kink. At any diagonal point, its centered
second difference in either coordinate at step `h` is `kappa h`.
It therefore fails every fixed coordinatewise semiconcavity bound of
the form `L h^2` as `h` tends to zero.

More strongly, let `h=1/r` and consider the `r-1` interior grid nodes
`v=(kh,kh)`. On the event

```text
gamma_1<=0,    gamma_2>=0,
```

which has probability `1/4`, every one of these nodes has value no
larger than each of its four coordinate neighbors. The four neighbor
increments are

```text
h(kappa+gamma_1),   -h gamma_1,
h gamma_2,          h(kappa-gamma_2),
```

and all are nonnegative. Thus the expected number passing all the
coordinatewise tests is at least `(r-1)/4`, even with zero tolerance.
The same event probability holds for an even symmetric finite uniform
noise grid, including the theorem's power-of-two laws.

This is an obstruction to that counting argument, not a divergence
claim for the number of globally near-optimal tuples. Along the diagonal
the objective is `k h (gamma_1+gamma_2)`, so comparisons in the diagonal
direction remove the spurious local candidates. For example, under the
continuous law, put `delta=C h^2`. The sum `gamma_1+gamma_2` has density
at most one. Comparing each diagonal node with both diagonal endpoints
gives the following upper bound on the expected number of diagonal
nodes within `delta` of the true optimum:

```text
2+sum_(k=1)^(r-1) delta[1/(kh)+1/(1-kh)]
  = 2+2C h H_(r-1),
```

where `H_j=sum_(k=1)^j 1/k`. This is bounded as `h` tends to zero.
Directional comparisons or a separate geometric argument are needed;
the product of independent coordinate-neighbor tests is insufficient.

## 4. Verification scope

An independent delegated reviewer checked the feasible-set equivalence,
state bounds, objective separation, tree decomposition, encoding, and
randomized complexity consequence. A targeted exact-rational inline
command, `python3 - <<'PY'`, checked 103 SUBSET SUM instances from six
fixed positive weight lists. It verified the decomposition, all binary
label assignments, state bounds, and the all-noise objective margin;
60 feasible `t=1` labels were found. These finite checks support the
algebra rather than establish the complexity reduction.

No project-wide verification, CI inspection, or literature search was
performed. External attribution and prior-art assessment remain outside
this note.
