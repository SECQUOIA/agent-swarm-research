# Independent review of bounded-degree monomial lifting

Date: 2026-09-05. Reviewer: independent `spatial_sdp_review` agent.
Reviewed: `notes/spatial-bb-bounded-monomial-lift-investigation.md`, including
the strengthened parity-rank count, arbitrary coordinate domains, and
the fixed-order upper certificate.

**Verdict: PASS.** The original candidate with a support-incidence bound
was correct. During review, a stronger count removed that assumption and
improved the exponent to `mT/(Delta D)`. The author incorporated this
strengthening. The pullback degree, exact lifted-box quadratic hull,
graph identities, factorable formulation, and upper certificate are sound.
This review does not assess priority.

## The stronger count obtained during review

Keep the union `C` of all restricted lifted-coordinate supports instead
of replacing its size by the coarser bound `D|R|`. The exhibited functional
has value at most `Delta|C|/m`. A pruned domain therefore has

```
|C| >= mT/Delta.
```

The restricted lifted coordinates impose a consistent system of parity
equations on the uniformly random original Boolean witness. Let `A` be
their support-incidence matrix over `GF(2)`, and let its rank be `q`.
Choose `q` linearly independent rows spanning all rows. Every column
appearing anywhere in `A` must appear in at least one chosen row:
otherwise every linear combination of the chosen rows is zero in that
column, contradicting the occurrence of that column in another row.
Each chosen row has at most `D` nonzero entries, so

```
|C| <= Dq.
```

A consistent rank-`q` parity system has exactly `2^(n-q)` solutions.
Signs of the monomial coordinates alter the right-hand side but not
the rank. Thus the fraction of witnesses in the domain is at most

```
2^(-q) <= 2^(-|C|/D) <= 2^(-mT/(Delta D)).
```

The union bound gives the revised theorem. Repeated supports, arbitrary
overlap, and arbitrarily many lifted coordinates do not affect this
argument. No incidence bound is necessary.

An independent exact test generated 10,000 random support matrices,
including repeated supports and dense overlap. Gaussian elimination
over `GF(2)` selected original basis rows. In every case their support
union equaled the union of all rows, and `|C|<=D rank(A)` held. The
preceding argument proves the identity in general.

## Pullback and all graph identities

Every lift coordinate is explicitly a signed **squarefree** monomial
with nonempty original support of size at most `D`. Substitution of
original witness signs on `C` leaves another signed Boolean character,
possibly a constant. Pullback of a lifted polynomial of degree at most
`2r` has original degree at most `2rD`; hence the functional is defined.

Every restricted lifted coordinate has all its original variables in
`C`, so it is deterministically its witnessed endpoint. Unrestricted
lifted coordinates have the full endpoint interval available. The
operation chooses an original assignment on `C` compatible with the
contained witness; it does not condition the original pseudoexpectation
on those signs or on the restricted parities.

If `q(h(x))` vanishes identically as a real polynomial, its pullback
remains zero after substitution. Any allowed multiplier has total
lifted product degree at most `2r`, so its pullback is also within
degree `2rD`. All asserted graph-identity constraints therefore hold,
including identities beyond a particular generating set.

The squarefree and nonempty support convention matters for the parity
count. A coordinate such as `x_i^2` is constant on Boolean witnesses;
its restriction need not impose any nontrivial parity equation. The
candidate's displayed lift definition excludes this case and is the
definition used by the theorem. The standard pair and clause lifts
satisfy it.

## Full box preordering after the nonlinear lift

After deterministic factors are removed, each bound slack is a positive
scalar times a parity indicator. Products of these indicators are
idempotent in the Boolean quotient, even when their supports overlap or
the parity equations are inconsistent. In the inconsistent case the
product is simply zero. Independence is not needed for this positivity
step.

For a lifted term `g p^2`, write `I` for the product of parity indicators
and `P` for the pulled-back, substituted multiplier. Then

```
deg(I) <= D deg(g),
deg(P) <= D deg(p),
I P^2 = (I P)^2 modulo Boolean identities.
```

The square has degree at most
`2D(deg(g)+deg(p))<=4rD`. The source pseudoexpectation is positive
on precisely these squared degrees, and respects all Boolean reductions
needed to identify the two expressions. Thus the factor `4rD` is
sufficient for every node preordering constraint, including repeated
slacks and globally coupled square multipliers.

## Exact quadratic hull in lifted coordinates

The augmented lifted first/second-moment matrix is PSD, either by the
just-proved empty-product positivity or directly by pulling back a
lifted linear square. Its diagonal entries are one: every lifted
coordinate becomes a signed Boolean character. Each other entry is a
signed original character moment of degree at most `2D`, so belongs
to `{0,-1,1}` under the stated hypothesis.

The signed-moment realization lemma from the previous independent
review therefore constructs an actual Boolean distribution on the
lifted coordinates with these first and second moments. A restricted
coordinate has mean equal to its forced endpoint. A Boolean variable
of mean `+1` or `-1` equals that endpoint almost surely, so this
distribution is supported in the entire node box.

The distribution need not lie on the nonlinear feasible graph. That
is consistent with the oracle: it asks for the quadratic moment hull
of the box and separately asks the polynomial functional to satisfy
graph identities. It does not ask one actual distribution to realize
all higher moments or those graph identities. No unsupported graph-hull
claim enters the proof.

## Objective, source degree, and explicit factorization

The identity `Phi(h(x))=F(x)` guarantees exactly the claimed evaluated
objective. Every clause avoiding `C` retains zero cost expectation.
At most `Delta|C|` clauses touch `C`, and each affected cost lies in
`[0,1]` under the source moments. Therefore the stronger objective
estimate used in the parity-rank argument is valid.

The previous source audit established linear available original
pseudo-degree with all character moments zero or signs. Restricting
to `4rD` available degrees is legitimate. Thus fixed `D` allows
node orders up to a sufficiently small constant multiple of `n`.

For the usual pair-plus-clause formulation,

```
u_e=x_i x_j,
v_e=u_e x_k,
Phi=(1/m) sum_e (1-b_e v_e)/2,
```

the original coordinates make the continuous graph representation
exact. There are `n+2m` variables, `2m` quadratic equations, and a
linear objective. Here `D=3`; original degree `12r` is sufficient.
The revised count at the fixed target `1/16` is

```
2^(m/(16*64*3)) >= 2^(7n/3072).
```

Since `15n<=N=n+2m<=17n`, this is exponential in the reformulated
dimension as well. For unrestricted numbers of added coordinates,
the general theorem's exponential bound is in the original dimension;
one should not infer exponential dependence on an arbitrarily inflated
lifted dimension.

## Arbitrary coordinate domains

If coordinate intervals are replaced by arbitrary sets, a locally valid
univariate polynomial on an unrestricted lifted coordinate has nonnegative
values at both endpoints. Boolean reduction expresses it as a
nonnegative combination of the two parity indicators. Products can
therefore be expanded into nonnegative multiples of idempotent parity
products. The number of nonconstant coordinate factors cannot exceed
the original sum of generator degrees, so the same `4rD` bound applies.

Restricted coordinates are fixed to values belonging to their local
sets. The realizing distribution has finite Boolean support contained
in the coordinate product, even for disconnected or nonclosed sets.
Its moment vector belongs to the actual convex hull, which is stronger
than merely satisfying the closed-hull quadratic inequalities. Parity
restrictions and the rank count are unchanged. This extension passes.

## Independent audit of the fixed-order upper certificate

Divide every original interval into `M=ceil(3/epsilon)` equal parts.
Their width is at most `2epsilon/3`. A clause derivative has magnitude
at most `1/2` in each of three coordinates, so its oscillation from a
fixed corner is at most `epsilon`. Hence the average of the individual
clause minima on a grid box is at least
`F(corner)-epsilon>=OPT-epsilon`.

For each clause, multiaffine interpolation represents its value minus
its exact box minimum as a nonnegative combination of the eight
products of three normalized coordinate-bound slacks. All coefficients
are corner values minus the minimum. This is a degree-three preordering
certificate, so node order two suffices.

In the standard lifted formulation, the polynomial identity

```
v_e-x_i x_j x_k
=(v_e-u_e x_k)+x_k(u_e-x_i x_j)
```

uses graph multipliers of total degree at most three. It transfers
the original clause certificate to the lifted linear objective under
the order-two equality constraints. Keeping auxiliary intervals at
`[-1,1]` and branching only original variables therefore gives at most
`M^n` lifted regions. The exact quadratic box hull can only strengthen
their lower bounds.

At `epsilon=1/16`, `M=48`. Because `OPT>=1/8`, an absolute certificate
at that tolerance also certifies relative gap `1/2`. Thus both the
unlifted and standard lifted examples have finite exponential upper
certificates alongside the exponential lower bounds. Arbitrary
uncharged objective propagation still requires the previously stated
discarded-region accounting.
