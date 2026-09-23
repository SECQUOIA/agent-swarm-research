# Spatial lower bounds under bounded monomial lifting

Promoted after two independent audits to [the result](../results/spatial-bb-monomial-lift-exponential-lower-bound.md).
This file preserves the investigation and earlier status language.

Date: 2026-09-05. Status: extension candidate awaiting independent review.
The underlying XOR construction and the unlifted transfer are in
[the beyond-clique investigation](spatial-bb-beyond-clique-investigation.md).

## Candidate and scope

The exponential certificate lower bound survives a bounded monomial
reformulation, including branching on pair products and clause products,
with no bound on the number of lifted coordinates. The node oracle may
include the full box preordering,
all polynomial identities of the lift through the chosen degree, and the
exact quadratic moment hull of the entire lifted node box.

This hull is the hull of the node **box**, not of the feasible graph inside
the box. Granting the latter would already solve a lifted linear or quadratic
objective. Likewise, arbitrary linear aggregation branching, lifting by unbounded-degree
monomials at the same node order, and localizers of all coupled valid
quadratic cuts are outside the statement.

## Definitions

Start from the signed 3XOR objective and pseudoexpectation in the unlifted
transfer. Write `Delta` for maximum clause occurrence and `m` for the clause
count. Choose a monomial lift

```
h_j(x)=sigma_j prod_{i in S_j} x_i,  j=1,...,N,
```

where `sigma_j in {-1,1}`, each `S_j` is nonempty, and `|S_j|<=D`. The map
includes each original coordinate as an identity coordinate. Repeated
supports are allowed, and no incidence bound on the lifted supports is
required. Consider continuous
optimization on the graph `{z=h(x):x in [-1,1]^n}`. Let `Phi(z)` be any
objective of degree at most `2r` whose pullback `Phi(h(x))` is the original
normalized cubic `F(x)`, as a polynomial identity.

Suppose the original Boolean pseudoexpectation is defined through degree
`4rD`, is positive on squares of degree at most `2rD`, satisfies all clauses,
and has **all character moments** through its available degree in
`{0,-1,1}`. This stronger signed-moment hypothesis holds for the same
classical XOR construction used in the unlifted theorem.

At a node `B=prod_j[a_j,b_j] subset [-1,1]^N`, minimize `L[Phi]` over
functionals `L` through degree `2r` with:

1. normalization and the full node box preordering, including repeated
   coordinate-bound generators;
2. `L[q v]=0` for every imposed polynomial lift identity `q` such that
   `q(h(x))` vanishes identically, whenever `deg(q v)<=2r`;
3. first and second moments in `conv{(z,zz^T):z in B}`.

Call this value `LB_r(B)`. All conditions are valid on the continuous
feasible graph in the node. Granting every available polynomial lift
identity, instead of a particular generating set, causes no problem below.
Take `r>=2` and integer `D>=1`.

## Lifted transfer theorem

Every finite cover of the feasible graph by lifted boxes with
`LB_r(B)>=T>0` contains at least

```
2^(m T/(Delta D))
```

boxes. As in the unlifted statement, this counts leaves for an ordinary
complete split tree, or counts all certified regions if propagation also
discards parts of the feasible graph.

*Proof.* Use the `2^n` witnesses `h(w)`, where `w` is a uniform Boolean
original assignment. The identity coordinates make these witnesses distinct.
For a box containing a witness, let `R` be its coordinates whose intervals
exclude at least one endpoint of `[-1,1]`. Write

```
C = union_{j in R} S_j,   |C| <= D |R|.
```

Substitute `x_C=w_C` in the original pseudoexpectation and pull polynomials
back through the monomial lift:

```
L[p(z)] = E[p(h(w_C,x_{[n] minus C}))].
```

This is defined through degree `2r`, since its pullback degree is at most
`2rD`. Every restricted lifted coordinate is fixed to its witnessed endpoint.
Each unrestricted lifted coordinate has its entire interval `[-1,1]`.

For a node preordering product `g p^2`, restricted slack factors become
nonnegative constants. Every remaining factor is `1+chi_S` or `1-chi_S`,
up to the sign of the corresponding monomial; its support has at most `D`
original variables. Modulo Boolean equations, the product is a nonnegative
scalar times a product `I` of parity indicators. These indicators commute
and are idempotent, so `I^2=I`; independence is unnecessary. Moreover,

```
deg(I) <= D deg(g),
deg(p composed with h after substitution) <= D deg(p).
```

Thus `I p^2=(I p)^2` modulo Boolean equations, and the degree of the square
is at most `2D(deg(g)+deg(p))<=4rD`. Positivity of `E` proves every required
preordering inequality. All imposed graph identities vanish directly after
pullback and substitution, so their multiplier constraints hold as well.

The augmented first-and-second-moment matrix of `L` is PSD. Its diagonal
entries are one because every lifted coordinate is a signed Boolean
character after substitution. Its other entries are original signed
character moments, possibly multiplied by fixed signs, and therefore belong
to `{0,-1,1}`. By the signed-moment realization lemma in the unlifted note,
these moments are realized by an actual Boolean distribution in the lifted
coordinates. Every restricted coordinate has expectation equal to its fixed
endpoint, so it equals that endpoint almost surely under this distribution.
All other intervals contain both endpoints. Hence this distribution is
supported in `B` and proves the exact quadratic-hull condition. It need not
be supported on the feasible lifted graph; the required graph identities
have already been checked separately in the pseudoexpectation.

At most `Delta |C|` clauses are affected by the substitution. Untouched
clauses retain pseudo-cost zero and every affected clause has pseudo-cost
in `[0,1]`. Therefore

```
LB_r(B) <= L[Phi] = E[F(w_C,x_{[n] minus C})]
         <= Delta |C|/m.
```

A pruned box consequently has `|C|>=mT/Delta`.

Each restricted coordinate forces one parity equation `h_j(w)=v_j` on
Boolean witnesses. Let `A` be the binary incidence matrix of its supports,
and write `q=rank_GF(2)(A)`. The system is consistent because the box
contains a witness, and therefore exactly a fraction `2^(-q)` of Boolean
assignments satisfy its parity equations. Choose `q` basis rows of `A`.
Every column occurring in any row must occur in one of these basis rows;
otherwise every linear combination of the basis rows would vanish in that
column. The union `C` is consequently contained in the union of the basis
supports, so `|C|<=D q`. Hence the witness fraction is at most

```
2^(-q) <= 2^(-|C|/D) <= 2^(-mT/(Delta D)).
```

The union bound over a witness cover proves the claim. This rank argument
allows repeated or heavily overlapping supports without any occurrence
hypothesis on the lift. QED.

## A standard factorable formulation

For every retained 3XOR clause on ordered variables `(i,j,k)`, introduce
`u_e=x_i x_j` and `v_e=u_e x_k`. Use the objective
`Phi=(1/m) sum_e (1-b_e v_e)/2`. There are `N=n+2m` variables, `2m`
quadratic equalities, and a linear objective. The graph is exactly the
continuous monomial lift because the original coordinates are included.
Here `D=3`; auxiliary occurrence counts do not enter the bound.

For the bounded-occurrence family of the unlifted result, `7n<=m<=8n`,
`Delta<=64`, `OPT>=1/8`, and linear original pseudo-degree is available.
Choose `r` up to a sufficiently small fixed multiple of `n` so that degree
`12r` is available. Absolute gap `1/16` and relative gap `1/2` require at
least

```
2^(7n/3072)
```

certified lifted regions. Since
`N<=17n`, this is also `2^(Omega(N))` in the reformulated dimension.

This formulation is a sparse quadratically constrained polynomial program
with linear objective. It admits arbitrary spatial branching in original
variables, pair products, and clause products under the stated oracle.
The result still does not cover branching on general linear combinations of
these variables or an exact quadratic hull of their feasible graph.

## Coordinate-domain extension

Intervals can again be replaced by arbitrary nonempty coordinate sets
`S'_j subset [-1,1]`, while imposing the full preordering of all univariate
polynomials valid on their respective sets. For unrestricted coordinates,
both endpoints belong to the set. Reducing a univariate generator in the
lifted Boolean coordinate gives a nonnegative combination of its two parity
indicators. Expanding the products reduces positivity to the same degree
argument. The signed-moment distribution has finite Boolean support inside
the coordinate domains, so it belongs to their actual quadratic hull even
when the sets are not closed. All counting arguments remain unchanged.

## Fixed-order upper certificate for the factorable formulation

The standard pair-plus-clause lift also admits the finite order-two upper
certificate from the unlifted note. Branch only the original coordinates
into `ceil(3/epsilon)` intervals apiece and keep auxiliary intervals at
`[-1,1]`. The degree-three Bernstein certificate for each original clause
is available from original-coordinate bound products. The identity

```
v_e - x_i x_j x_k
= (v_e-u_e x_k) + x_k (u_e-x_i x_j)
```

transfers this certificate to the lifted linear objective using graph
multipliers of total degree at most three. Hence at most
`ceil(3/epsilon)^n` lifted boxes suffice at node order two. The exact quadratic
box hull can only improve this node bound. For the fixed tolerances above,
`48^n` regions suffice, while exponentially many are necessary.

## Degree versus region count

The proof also applies when `D` depends on `n`. If the imported original
pseudoexpectation is available through degree `a n`, then the sufficient
condition is `4rD<=a n`, and at the fixed tolerances the region lower bound
is

```
2^(7n/(1024 D)).
```

Consequently, within this oracle model and its degree range, a polynomial
region count requires monomial branch support `D=Omega(n/log n)`. For fixed
`D`, granting any number of degree-at-most-`D` monomial coordinates and
allowing arbitrary spatial splits in them still requires exponentially many
regions, even at node order proportional to `n`. If the number of added
coordinates is superlinear, the exponent is in the original dimension `n`;
it is not automatically linear in the lifted dimension `N`.
