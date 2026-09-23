# Independent audit of discrete-resistance pressure hardness

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`.

Reviewed: [the discrete-resistance investigation](potential-flow-discrete-resistance-hardness.md)
and the explicit theta solution in
[the cactus uncertainty-hull investigation](potential-flow-cactus-uncertainty-hulls.md).

**Verdict: PASS for the common signed quadratic law `phi(x)=x|x|` and a
prescribed ordered pair of objective terminals.** The Subset-Sum reduction,
positive-threshold bridge, rational gap, and integer scaling are correct.
They prove NP-hardness and rule out polynomial complexity in input size
and additive precision bits unless `P=NP`. They do not prove strong
NP-hardness or rule out an FPTAS.

The author was asked to state the common law and prescribed terminal pair
explicitly in the theorem opening. These are scope clarifications; no
mathematical repair to the reduction is required.

## Physical solution and series aggregation

Use the incidence convention that positive nomination is net outgoing flow.
Write `a=(q+1)/2` and `b=(7-q)/2`. The four outer edge flows are `(a,b,b,a)`.
Their balances at vertices `0,1,2,3` are respectively `4,-4,3,-3`, since
`a+b=4` and `b+q-a=3`. All flows are positive whenever `0<q<2`.

Zero nominations at the internal vertices of the cross path force the same
signed flow on every path edge. Adding their constitutive drops therefore
gives effective resistance equal to their sum, with no approximation:

```
tau = 1/2 + sum_i(a_i*sigma_i)/(2K).
```

For every `tau>0`, the polynomial

```
p_tau(q)=(12tau+1)q^2+10q-23
```

is strictly increasing for `q>=0`, is negative at zero, and is positive at
two. It consequently has exactly one positive root in `(0,2)`.
The two outer terminal paths have the same drop, and

```
pi_2-pi_3 = b^2/6-a^2/2
           = (23-10q-q^2)/12
           = tau*q^2.
```

Thus the displayed flows admit consistent potentials satisfying all laws.
The strictly convex passive-flow energy identifies them with the unique
physical flow. This argument also verifies the internal cross-path
potentials after subdivision.

The outer potential difference is exactly

```
pi_0-pi_1 = a^2/2+b^2/6 = 2+(q-1)^2/6.
```

Its reverse therefore has a unique maximum at `q=1`. Substitution in the
root equation gives `p_tau(1)=12(tau-1)`, so that maximum occurs precisely
when the selected item sum is `K`.

## Positive objective and graph restrictions

The added leaf has nomination `1` and its edge is oriented toward vertex
`1`. Its flow is exactly one. Changing the nomination of vertex `1` from
`-4` to `-5` preserves every original theta balance and flow. With bridge
resistance `3`, its potential increment is `pi_4-pi_1=3`. Therefore

```
F=pi_4-pi_0=1-(q-1)^2/6.
```

All nominated values belong to the fixed set `{0,1,3,4,-3,-5}` and sum to
zero. No uncertain nominations, flow capacities, potential bounds, or
additional physical feasibility constraints are used.

For `n>=1`, the theta has `n+3` vertices and `n+4` edges. The three
internally disjoint paths between vertices `2` and `3` make it biconnected,
with cycle rank `(n+4)-(n+3)+1=2`. The added leaf adds one vertex and one
edge and creates exactly one bridge. Vertices `2` and `3` have degree
three, vertex `1` has degree three after the addition, and all other
degrees are at most two except the degree-one leaf. The graph is simple,
including when the cross path has only one edge. The full graph also has
global cycle rank two. Omitting the leaf gives a single theta block if a
negative comparison threshold is acceptable.

## Quantitative separation

The exact polynomial identity

```
p_tau(q) = (q-1)*[(12tau+1)(q+1)+10] + 12(tau-1)
```

gives the claimed formula for `|q-1|` at the physical root. Its denominator
is positive. In a no instance, the selected item sum differs from `K` by
at least one, hence `|tau-1|>=1/(2K)`.

The inequality `q<2` implies

```
(12tau+1)(q+1)+10 < 36tau+13
 <= 36*(K+S)/(2K)+13 = 31+18S/K.
```

The resulting conservative bounds are valid:

```
|q-1| >= 6/(31K+18S),
F <= 1-Delta,
Delta = 6/(31K+18S)^2.
```

Yes instances attain value exactly one, and every possible resistance
selection in a no instance has value at most `1-Delta`. This is a gap
between whole optimization instances, rather than a gap for one selected
resistance vector.

## Reduction size and precision model

Positive-integer Subset Sum is NP-hard; a primary research reference also
states this standard starting point in its discussion of pseudopolynomial
algorithms: [Polak, Rohwedder, and Węgrzycki (2021)](https://arxiv.org/abs/2105.04035).
Restricting to `n>=1` and `1<=K<=S` does not remove hardness: instances
outside this range are directly decidable and can be mapped to fixed yes
or no instances as appropriate.

The graph has linear size in `n`. Each rational uncertain option has a
representation with denominator `2nK` and numerator either `K` or
`K+n*a_i`, so the total output length is polynomial in the original
binary input length. The sum `S` has bit length at most
`max_i bitlength(a_i)+O(log n)`. The rational gap has bit length
`O(log(K+S))`.

Suppose a value approximation has absolute error less than `Delta/3`.
Comparison with the rational midpoint `1-Delta/2` distinguishes yes and
no instances. The same comparison works with any point in a certified
optimum interval of width less than `Delta/3`: because the interval
contains the optimum, every such point has absolute error below that
width. A dyadic tolerance `2^(-k)<Delta/3` can be chosen with
`k=O(log(K+S))`. Thus an algorithm polynomial in network encoding length
and `k` would decide Subset Sum in polynomial time.

There is also a witness version: an algorithm returning a feasible
resistance selection with objective within less than `Delta` of the
optimum must return an exact target subset on every yes instance. Checking
the selected item sum is enough to decide whether the returned selection
is such a subset. No exact evaluation of its physical pressure is needed
for this witness argument.

## Integer scaling

Multiplication of every resistance by the common positive factor `6nK`
multiplies the energy by that factor. Its unique minimizing physical flow
is therefore unchanged. All potential differences scale by the same
factor. The proposed values follow exactly:

```
outer resistances: 3nK, nK, nK, 3nK,
cross-path choices: {3K, 3K+3n*a_i},
bridge resistance: 18nK,
threshold: 6nK.
```

Every value is a positive integer of polynomial encoding length. The gap
scales to `6nK*Delta`, also of polynomial encoding length. Integer scaling
does not make the numerical magnitudes polynomially bounded in the
original input length, so it gives no strong-hardness conclusion.

## Additional verification and limits

An independent SymPy check expanded nine identities exactly: all four
original/modified balance identities, equality of the terminal path drops,
the cross-drop polynomial, the original and shifted objectives, and the
root-subtraction identity. All nine reduced to zero. These symbolic checks
support the direct proof; no floating-point root calculation is needed.

If `K<=S`, the interval hull of the independent two-point choices permits
every effective cross resistance between `1/2` and `(K+S)/(2K)`, including
one. Thus its optimum is one even for a discrete no instance. This
explains why the continuous interval algorithm does not solve the discrete
problem and verifies the claimed distinction on these exact instances.

The hardness concerns maximum pressure difference for a prescribed ordered
terminal pair. It does not by itself show hardness of edge-flow extrema;
indeed, individual edge flows in this gadget are monotone functions of the
single effective resistance. The gap can be exponentially small in binary
input length. Consequently the proof excludes polynomial dependence on
precision bits, but not polynomial dependence on the reciprocal tolerance,
an FPTAS, or pseudopolynomial algorithms. General network-design hardness
and novelty relative to that literature require separate analysis.
