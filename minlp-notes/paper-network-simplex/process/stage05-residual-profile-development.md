# Residual-profile elimination — candidate strengthening during Stage 5

Root independently derived this while auditing the general fixed-state proof.
The Stage 5 author is independently developing it; it is not accepted until
five manuscript reviewers finish and all valid findings are resolved.

Let T=1-x_h and eliminate w_0=T-sum_{j=1}^m w_j. The residual state is never
observed and therefore is always in U. In explicit-state coordinates the rows are:

- -e_j w <= 0, e_j w <= lambda_j;
- 1^T w <= T, -1^T w <= lambda_0-T;
- bypass observations and both-observed gadget states give two signed singleton
  rows; one-sided observations give a negative singleton lower bound;
- gadget endpoint rows are 1_B w <= R and 1_(A union T) w <= T-R.

Here the category T in A union T means both-observed states, whereas the scalar
T above is branch total; the manuscript should avoid this notation collision.
The endpoint identity follows because the complement of B union U is A union T.

Thus the nonzero normal universe is positive subset indicators, negative
singletons, and the negative full-set indicator. Every RHS has unit flow/product
coefficients. The same circuit-minor proof yields (m+1)Delta_m for m>=1, improving
(m+2)Delta_(m+1). Exact basis recovery works in m dimensions; m=0 is immediate.
Root exact enumeration gives 2,6,11 normals and 1,5,16 positive circuits for
m=1,2,3, with largest primitive ray entries 1,1,2.

## Sharper result for two explicit coordinates

For m=2 the normals are precisely +/-e_1, +/-e_2, +/-(1,1). The five positive
circuits are the three opposite pairs and the two oriented triples. All primitive
multipliers equal one. This alone does not establish a unit bound on the original
coordinates because a product can occur in several RHS expressions.

A category-by-category cancellation does establish that bound:

- An a-only product has coefficient -1 in the lower singleton and the B endpoint,
  and +1 in the A-union-T endpoint. The B set excludes its state, the other
  endpoint includes it, and these two sets are disjoint. Whenever two of its
  occurrences enter one of the five circuits with the same sign, the circuit
  requires the opposite occurrence or cannot be a minimal dependence.
- The b-only case reverses endpoint signs and has the same cancellation.
- A both-observed a product occurs in both signed singleton rows and the two
  opposite endpoint RHS expressions. A both-observed b product occurs only in
  the two signed singleton rows. The five-circuit enumeration again permits no
  uncancelled doubled coefficient.
- A gadget aggregate x_a occurs once with each endpoint sign. The only shared
  flow variable across gadgets is x_h. In the circuit (e_1,e_2,-1), each positive
  row can contribute -1 to x_h, but the negative full row necessarily contributes
  +1. Thus its sum ranges only from -1 to +1. The other circuits also have unit
  coefficients after this cancellation. Bypass products occur only in opposite
  singleton rows and satisfy the same bound.
- Zero-row conditions have unit coefficients directly; original domain checks
  do also. m=1 has only one opposite pair and m=0 is the original flow domain.

The independent exact script `verification/stage05-root/profile_coefficients.py`
constructs every category for m=1,2 in separate gadgets, includes both bypass
observations, and computes coefficient extrema over all choices of affine branch
in every circuit. All 50 original coordinates in the m=2 enumeration have bounds
[-1,1]. Repeating a category adds distinct coordinates but cannot change the
per-coordinate extremes; x_h is already shared across every category.
The script supplements, rather than replaces, a written general cancellation
proof. No final theorem claim is accepted on the finite check alone.

## Consequences requiring later implementation and review

The m=2 flat-chain oracle can use five tests instead of 41 unreduced-profile
circuits. Stage 6 should implement this reduced version and compare it against
both the retained unreduced reference and strengthened full-state baselines.
The general compressed formulation and earlier graph separator remain available.
No claim of unit coefficients at m>=3 or on arbitrary nested series-parallel
networks follows from this development.

## Explicit five-test implementation

The reduced m=2 profile has bounds L1<=w1<=U1, L2<=w2<=U2,
Ls<=w1+w2<=Us. The complete tests are the three interval nonemptiness tests,
L1+L2<=Us, and Ls<=U1+U2. These are precisely the five circuits above.
Choose s=max(Ls,L1+L2), w1=max(L1,s-U2), w2=s-w1. The tests imply
s<=min(Us,U1+U2), which verifies all bounds. Consequently no circuit-library
construction or inverse-basis enumeration is needed in this special case.
This is the same elementary interval geometry already used for theta states.

## Further candidate: sharp state-count threshold for unit coefficients

An additional independent calculation extends the unit description to **m=3**,
after using the original gadget balance equations to change cut representatives.
The existing m=4 small example then makes the state threshold sharp on this
flat graph family. This remains a candidate until authored and reviewed.

Write e_S for subset indicators in R^3. The 16 positive circuits are:

1. {e_S} union {-e_j:j in S}, for all seven nonempty S; all weights one.
2. {-1} plus indicators of a partition of [3], for the five partitions;
   all weights one.
3. {-1,-e_i,e_{ij},e_{ik}} for the three choices of i; all weights one.
4. {-1,e_{12},e_{13},e_{23}}, with weight two on -1 and one elsewhere.

Completeness can be checked by the minimal-support bound at most four and exact
rank/sign tests of the eleven-row universe. Without -1, a minimal circuit must
have just one positive row, cancelled by its negative singleton rows. With -1,
checking the singleton/pair possibilities gives the last three families.

In this list, no circuit contains -e_j together with a positive subset excluding
j, or +e_j together with a distinct positive subset containing j. Therefore the
same category proof as for m=2 gives unit product coefficients. The only doubled
multiplier is on -1, whose RHS lambda_0-t contains no observed products. Every
x_a coefficient is also unit because its two endpoint occurrences have opposite
signs and unit multipliers. No x_b occurs in a profile cut.

Only x_h can have magnitude two:

- A coefficient -2 requires the partition into three singletons, with all three
  selected positive rows coming from t-R_i. They belong to distinct gadgets,
  since one gadget has only one A_i-union-T_i normal. Each of those x_a
  coefficients is -1. Add one such gadget's equation x_a+x_b+x_h=1 to the
  Farkas row: x_h becomes -1, that x_a becomes zero, and x_b becomes +1.
- A coefficient +2 requires the last circuit, with all three pair rows coming
  from R_i. These likewise belong to distinct gadgets and have x_a coefficient
  +1. Subtract one such gadget equation: x_h becomes +1, x_a zero, x_b -1.

Every other branch already has unit flow/product coefficients. Adding a valid
flow equation preserves global validity and violation at a query that passed
flow-domain checks. Thus a finite exact unit description results. Separation
uses the 16 grouped circuit tests and this simple correction when necessary;
recovery remains a fixed three-dimensional basis enumeration.

`verification/stage05-root/profile_three_coefficients.py` independently checks
all 64 observation categories and bypass observations, all per-coordinate branch
extrema on the 16 circuits, and every offending branch combination. Only x_h
exceeds one before correction; all **539** offending combinations pass the
balance correction. Repeated categories add distinct coordinates and do not
change the argument. This finite audit supports the complete classification
proof; the author must independently verify and reviewers must scrutinize it.

The m=4 example with five vertices, nine arcs and seven observations forces an
actual product coefficient ratio two, invariant under affine equations. It rules
out any finite unit description there. The same obstruction embeds at every
larger m by adding unobserved labels and fixing their weights to zero in the
coordinate section. The candidate result therefore establishes exactly m<=3 as
the dimensions for which every sparse observation pattern on every flat chain
admits a unit flow/product description. It makes no claim that every instance
with m>=4 needs larger coefficients.

### Queries that isolate both coefficient repairs

These exact rational candidates were derived by the root for author verification:

- Three gadgets, y=(1/3,1/3,1/3), residual zero, x_h=1/2, each x_a=2/5,
  x_b=1/10. Observe just (a_i,i), with value zero. Each positive singleton
  upper endpoint is 1/10, and the negative full RHS is -1/2. Their circuit
  sum is -1/5, with x_h coefficient -2; all other present circuit tests pass.
- Three gadgets, y=(1/4,1/4,1/4), residual 1/4, x_h=1/2, each x_a=1/20,
  x_b=9/20. Observe only b-products in pairs {1,2},{1,3},{2,3}, respectively,
  all equal to 1/20. Each pair RHS is 3/20, and the negative full RHS is -1/4.
  The triangle circuit sum is -1/20, with x_h coefficient +2. Other circuits
  pass, including tight overlapping-pair tests.

Both candidates satisfy original flow/simplex/product-nonnegativity checks and
all individual McCormick inequalities. They should test the actual implementation
repair paths, not merely coefficient combinations that never become active.

## Observed-label corollary

The accepted homothetic merger applies globally to this single block. Let J be
the labels occurring in any observation and a=|J|. Keep only their state flows
and one merged state of weight 1-sum_{j in J} y_j. The original simplex variables
are retained, including unused labels. Thus all new flat-chain bounds apply in
a profile of dimension a; the unit-description threshold is really a<=3.
Separation costs O((a+1)L+|O|+m)+2^{O(a^2)}, including the O(L) flow-domain scan even when a=0. Coefficients on x/z are
unchanged by the weight substitution. Refinement reconstructs unused labels
proportionally from the one merged default. Dense state-flow output still costs
O((m+1)L). The original m=4 counterexample observes all four labels, so it also
makes the observed-label threshold sharp. The author was asked to include this
immediate corollary rather than leave the structural sparsity benefit implicit.
