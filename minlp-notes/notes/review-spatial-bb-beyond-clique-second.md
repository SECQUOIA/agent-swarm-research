# Second independent review: spatial covers and bounded-degree monomial lifts

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`.
Reviewed files:

- `notes/spatial-bb-beyond-clique-investigation.md`
- `notes/spatial-bb-bounded-monomial-lift-investigation.md`

**Verdict: PASS in the stated certified-region-cover model.**
The unlifted transfer and strengthened lifted bound
`2^(m T/(Delta D))` are correct under their stated pseudoexpectation
hypotheses. I independently checked the primary source, substitution,
degree accounting, exact quadratic box hull, parity rank count, sparse
instance extraction, and finite order-two upper certificates. No substantive
proof defect was found. This audit does not establish novelty.

## Unlifted node functional

Fix a Boolean witness `w` in a node. A coordinate interval containing
both signs equals the full original interval. Every other coordinate
containing the witness can safely be fixed to its witnessed sign. Substitution
in the original pseudoexpectation is well-defined and normalized. It makes
no assertion that this sign assignment has positive pseudo-probability.

Let `a=deg(g)` and `b=deg(p)`, with `a+2b<=2r`.
Restricted bound factors become nonnegative constants. The remaining
factors reduce, modulo the Boolean equations, to zero or a nonnegative
multiple of an assignment indicator `I` of degree at most `a`.
The identity `I p^2=(I p)^2` is valid through degree at most
`2(a+b)<=4r`. Boolean reduction does not increase degree. The original
PSD condition therefore proves every permitted preordering inequality,
including repetitions and the empty product.

The actual distribution realizing the original first two moments can be
marginalized on unrestricted coordinates and combined with the fixed signs.
Its support belongs to the node, and all means, diagonal moments, and cross
moments equal those of the constructed functional.

An untouched clause has zero pseudo-cost. A touched clause leaves at most
two unfixed variables and has cost `(1-sigma chi_S)/2`. Its expected cost
lies in `[0,1]`; either the realizing degree-two distribution or Boolean
PSD proves this. At most `Delta |R|` clauses are touched. Consequently
`LB<=Delta |R|/m`, while a node with `|R|` restricted coordinates contains
at most a `2^(-|R|)` fraction of Boolean witnesses. The reciprocal
union bound proves the unlifted result. Overlapping boxes and repeated
clauses cause no difficulty.

## Lifted node functional and degrees

Let `C` be the union of original supports of all restricted lifted
coordinates. Substitution of `x_C=w_C` makes every such lifted coordinate
constant at its witnessed sign. Every unrestricted lifted coordinate has
both endpoints available, even if its pullback also becomes constant.

For a polynomial of lifted degree `s`, the pullback through the degree-`D`
monomial map has original degree at most `Ds`. Thus the node functional
through degree `2r` is defined using only original degree `2rD`.
The additional degree is needed only to prove positivity.

After substitution, each nonconstant slack is twice a parity indicator.
Products of parity indicators remain idempotent even when the supports
overlap, the indicators are dependent, or the product vanishes. The
product indicator has degree at most `Da`; the pulled-back square
multiplier has degree at most `Db`. Its indicator-times-polynomial square
has degree at most

```
2D(a+b) <= 4rD.
```

All Boolean reductions used in identifying it with the original preordering
term stay within that degree. Every imposed graph identity vanishes as an
ordinary polynomial after pullback, before applying the pseudoexpectation.
Its allowed multiplied identity has pullback degree at most `2rD`. Therefore
granting all polynomial graph identities through node degree causes no gap.

The first-and-second-moment matrix is PSD because a lifted linear
polynomial pulls back to degree at most `D`. Its diagonal entries are one.
Every other entry is a fixed sign times an original character moment, hence
is zero or a sign. The signed-class Gram argument supplies an actual
Boolean distribution with precisely this augmented moment matrix.
A restricted coordinate has mean equal to its witnessed endpoint, so it
equals that endpoint almost surely. All remaining endpoints belong to the
node. This proves membership in the exact quadratic moment hull of the
node box.

This last distribution need not satisfy the graph identities pointwise.
Those identities hold in the pseudoexpectation, including the prescribed
higher moments. There is no requirement that the unrelated distribution
realizing its degree-two truncation share its higher moments. This is the
essential distinction between the box hull and the feasible-graph hull.

Finally the polynomial identity `Phi(h(x))=F(x)` persists after
substitution. At most `Delta |C|` clauses are affected, giving

```
LB_r(B) <= L[Phi] <= Delta |C|/m.
```

## Incidence rank removes the occurrence assumption on the lift

I independently verified the first reviewer's strengthening. Let the rows
of a binary matrix be the incidence vectors of restricted supports and
let its rank over `F_2` be `q`. Select a basis from its ORIGINAL rows.
Every original support is contained in the union of the basis supports:
a coordinate absent from every basis row is absent from their linear span.
Each basis row has at most `D` nonzeros. Hence

```
|C| <= Dq.
```

The parity signs forced by a node are consistent because it contains a
witness. Their solution set on Boolean assignments is therefore an affine
binary space of dimension `n-q`, containing exactly `2^(n-q)`
assignments. Every Boolean witness in the box satisfies these equations.
For a certified node,

```
q >= |C|/D >= mT/(Delta D).
```

Thus its witness fraction is at most `2^(-mT/(Delta D))`, and covering
all witnesses requires the claimed reciprocal number of regions.
Repeated supports do not change this argument. Arbitrarily many overlapping
lifted coordinates of bounded support size are allowed; no lifted incidence
bound `Lambda` is needed.

As a supplementary exact check, exhaustive enumeration of all 32,768
families of nonempty supports of size at most two on five variables verified
`|C|<=2q` and the affine fiber count `2^(5-q)` for three witnessed right
hand sides per family. The general proof above is the basis of the result.

The standard pair-plus-clause lift has `D=3` and
`N=n+2m<=17n`, giving `2^(7n/3072)` regions and exponential growth
also in `N`. For general superlinear `N`, the bound is exponential in
the original dimension `n/D`; an exponential-in-`N` statement does
not follow.

## Independent check of the imported XOR construction

I read Theorems 11–12 and the full proof of Lemma 13 in
[Schoenebeck's primary manuscript](https://schoeneb.people.si.umich.edu/papers/LasserreNew.pdf).
For `k=3,d=8,delta=1/4,gamma=1/4,epsilon=0`, its width is a positive
constant times `n`. The density threshold is `1+8 ln(2)<8`.
The signed character vectors and their product-consistency formula give
Boolean character moments in `{0,-1,1}`, with a PSD character moment
matrix up to half the available width. Consequently width `w` supplies
a functional through degree `w`, positive on squares of degree at most
`w/2`. Choosing `4rD<=w` is sufficient. The random instance model
uses distinct variables within each independently sampled clause, as needed.
This imports a classical SOS gap, not a new one.

## Sparse extraction and constants

For each fixed assignment, the independent random clause signs give
`Binomial(8n,1/2)` violations. Hoeffding gives probability at most
`exp(-n)` for at most `2n` violations. The union bound over
`2^n` assignments tends to zero.

Each occurrence count is `Binomial(8n,3/n)`. The identity

```
E[D_i 2^D_i] = 48(1+3/n)^(8n-1)
```

follows by differentiating the binomial generating polynomial and
multiplying by two. Therefore the expected number of deleted clauses is
at most `n*48 exp(24)/2^64 < n/8`. Markov bounds the probability of
deleting more than `n` clauses by less than `1/8`; independence of
the occurrence counts is unnecessary. This event intersects the two
high-probability events for all sufficiently large `n`.

The retained family has `7n<=m<=8n`, maximum occurrence 64,
and at least `n` violated clauses per assignment. Its multiaffine
continuous minimum equals the Boolean minimum and is at least `1/8`.
Deleting clauses preserves the pseudoexpectation's properties.
The stated tolerances require target at least `1/16`, yielding
unlifted exponent `7n/1024` and degree-`D` lifted exponent
`7n/(1024D)`.

## Coordinate domains and finite upper certificates

For arbitrary coordinate domains, a valid univariate polynomial reduces
on Boolean endpoints to a nonnegative combination of the two endpoint
indicators when both endpoints are permitted. On a restricted coordinate,
its evaluated value is nonnegative by witness membership. Expanding products
therefore gives the same positivity argument, with no increase beyond the
stated degree. The realizing distribution has finite Boolean support in
the domain, so exact hull membership holds even for nonclosed domains.

A grid with `M=ceil(3/epsilon)` intervals per original coordinate has
width at most `2epsilon/3`. Each clause cost has derivative magnitude
at most `1/2` in each of its three coordinates. Its value varies by
at most `epsilon` across a grid box. Its multiaffine Bernstein
representation relative to that box, minus its corner minimum, has
nonnegative coefficients and degree-three products of bound slacks.
Averaging these certificates proves the required lower bound at node
order two.

For the factorable lift, the identity

```
v_e-x_i x_j x_k
=(v_e-u_e x_k)+x_k(u_e-x_i x_j)
```

uses graph multipliers of total degree at most three, so it transfers the
same certificate to the lifted linear objective at order two.
Thus `48^n` regions suffice for the fixed tolerances. These upper
certificates ensure the lower bound is not caused by impossibility of any
finite certificate.

## Limits that must remain explicit

- Regions must collectively cover the whole feasible graph. Feasible-domain
  deletions must be separately certified and charged. The theorem does not
  count only surviving final leaves after free propagation.
- Exact quadratic hull means the hull of the entire node box. Its linear
  moment inequalities are included; their arbitrary products and SOS
  localizers are not.
- The exact quadratic hull of the feasible graph would already optimize
  a linear or quadratic lifted objective and is outside the model.
- Arbitrary coupled linear branching is outside the box-cover theorem.
- Degree `4rD` must fit within the imported pseudoexpectation degree;
  increasing lift degree reduces the available node order.
- A polynomial-region consequence for variable `D` applies only within
  this degree range. No uniform claim for unbounded degree at fixed source
  degree follows.
