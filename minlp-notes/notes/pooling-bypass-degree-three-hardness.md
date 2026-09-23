# Candidate refinement: bypass maximum degree three

Date: 2026-09-05. Status: two fresh independent reviews PASS.

This strengthens the verified
[degree-four averaging construction](pooling-bypass-degree-four-hardness.md).
Half-sized signal ports reduce each averaging input to three outgoing
arcs. The reviewed result is NP-completeness with one pool, two upper-bound
quality coordinates, input total out-degree at most three, output total
in-degree at most three, and pool out-degree two. The pool's in-degree
is unrestricted. Fixed supplies and demands are still used.

## Full and half signal ports

A full copy gadget has two outputs of exact demand four and exact
quality `3/2`. Each receives an endpoint port of quality zero, an
endpoint port of quality three, and an arc from a common quality-`3/2`
input with exact supply four. Endpoint arc capacities are two; middle
arc capacities are four. The reviewed midpoint argument gives its ports

```
A-zero: x,       B-zero: 2-x,
A-three: x,      B-three: 2-x,             0<=x<=2.         (F)
```

A half copy gadget has the same endpoint quality labels zero and three,
but both outputs have exact demand three and exact quality one. The
shared middle input has quality one and exact supply three. Zero-quality
endpoint arcs have capacity two, quality-three endpoint arcs have capacity
one, and middle arcs have capacity three.

At its first output, write endpoint flows `u,v` and middle flow `m`.
Mass and quality give `u+v+m=3` and `3v+m=3`, hence `u=2v`.
Put `u=x`, so `v=x/2` and `m=3-3x/2`. Applying the same equations at
the other output and using the common middle supply gives zero-quality
endpoint sum two. Its ports are therefore exactly

```
A-zero: x,       B-zero: 2-x,
A-three: x/2,    B-three: 1-x/2,           0<=x<=2.         (H)
```

Conversely every `x in [0,2]` fills either gadget within all its bounds.
The middle flow at each endpoint remains nonnegative, including at
`x=0` and `x=2`.

As before, a quality-zero input with exact supply two and exactly two
outgoing arcs joins the `B-zero` port of one gadget to the `A-zero`
port of the next. Their sum condition forces the same signal `x` in
both gadgets. Crucially, their zero-quality port formulas agree in (F)
and (H), so a chain may mix full and half gadgets in any order.

For every requested quality-three port occurrence, allocate its own
full or half gadget, choose the positive or complementary port needed,
and privately supply the unused port. Its private upper supply equals
the port capacity, two for full ports and one for half ports. Unused
zero-quality chain endpoints have private upper supply two. All private
nodes are distinct. This ensures unique physical arcs, even for repeated
occurrences of the same signal in one equation.

Original intake signals still use the full quality-conversion gadget
with endpoint labels `0,a_i`, midpoint `a_i/2`, demands four, and
common midpoint supply four. Its `B-a_i` port and the actual pool
intake share a quality-`a_i` source with exact supply two. Its intake
is therefore the chain signal `x_i`. These conversion gadgets can also
be joined to full or half chains through their common zero-quality ports.

## A degree-three averaging input

For `u,w,v in [0,2]`, use a quality-three input with exact supply two
and exactly the following outgoing arcs:

```
one full positive v port,
one complementary half port of u, carrying 1-u/2,
one complementary half port of w, carrying 1-w/2.
```

The source supply equation is

```
v + (1-u/2) + (1-w/2) = 2
iff 2v=u+w.                                               (A)
```

It has out-degree three, and all arcs have capacities two, one, and
one respectively. Repeated children cause no parallel arcs because their
port occurrences are allocated to distinct gadgets.

A child may be the complement of an original signal. If `u=2-x_i`,
the needed half quantity is `1-u/2=x_i/2`, so use a positive half
`x_i` port. If `u=x_i`, use its complementary half port. Auxiliary
children use the same rule.

One additional signal `zeta` is fixed to zero by assigning a full
positive port to an input with upper supply zero. Its chains supply zero
leaves for padding. In half gadgets, its complementary quality-three
port has flow one; in full gadgets it has flow two. The formulas above
show that all its gadget demands and supplies remain feasible.

## Replacing row capacity inputs

Retain the original reduction's list of full signal values
`f_1,...,f_m`, each `x_i` or `2-x_i`, whose sum must be at most
`B=2 sum_{c_i<0}(-c_i)` for a homogeneous row `sum_i c_i x_i<=0`.
For `m=0`, omit the vacuous row. For `m>=1`, pad with zeros to
`N=2^ceil(log2 m)` leaves. Associate a new signal with each internal
node of the complete binary tree and impose that it averages its two
children through (A). The root satisfies

```
v_root = sum_j f_j / N,       0<=v<=2 at every node.
```

Assign a full positive root port to a single-arc input with upper supply
`B/N`. This is a nonnegative dyadic bound at most two. For `m=1`, use
the original leaf's full positive or complementary port directly, without
an averaging node. Remove the former high-degree row input completely.

Every feasible original signal assignment extends by computing the
averages and filling the full/half gadgets with those values. Conversely,
each exact two-unit averaging input forces (A); induction from the leaves
then recovers the original row inequality at the root bound. Thus the
projection onto original signals and actual pool intakes is unchanged.
In particular, the zero-intake assignment remains feasible, even when
the source product polytope is empty. Auxiliary averages need not be zero
there, because some leaves are complementary original signals.

## Polynomial size and precise topology

For each nonempty row, `m<=N<2m`. There are `N-1` new averaging
signals and equations, three requested ports per equation, and one root
port. The number of full/half gadgets and chain links is therefore
`O(m)`. The Matsui-specific homogeneous source system has polynomial
total coefficient sum, so the overall reduction remains polynomial in
binary encoding length. No general binary-coefficient representation
lemma is needed.

Each averaging input has degree three; midpoint, chain-link, and
conversion inputs have degree two; private-port, root-bound, zero-bound,
and anchor inputs have degree one. Conversion input degree counts its
pool intake as well as its bypass. Every full, half, and conversion
gadget output has exactly three incoming arcs. The two primary outputs
have in-degrees two and one. The sole pool has out-degree two and
unrestricted in-degree. Therefore total input out-degree and total output
in-degree are at most three, and the bypass graph has maximum degree
three. Equal quality values never identify source nodes or add routes.

All upper flow bounds are at most four. Apart from the dyadic root
bounds in `[0,2]`, the bounds are zero, one, two, three, or four.
All new arcs have zero cost in the base arc-cost version. The source
profit identity, the standard production-cost variant, and NP-membership
therefore carry over from the reviewed one-pool reduction.

There is one physical quality with lower and upper output specifications.
Duplicating its negative gives two upper-bound quality coordinates;
affine shifts and positive scaling put all values and bounds into
`[0,1]`. Fixed supply and demand contracts remain part of this result.
The large source objective and quality encodings prevent a strong
NP-completeness claim. Bypass degree two is not settled by this argument.

## Status

The half-port formulas and their chain composition have been checked
independently by the author and the reviewer who proposed the refinement.
The [author checker](../code/pooling_bypass_copy/check_degree_three.py)
passed 26 original-network global solves, including shifted qualities and
boundary cases; its [log](../code/pooling_bypass_copy/degree_three_output.txt)
is retained. It verifies input/output degrees at most three, no parallel
arcs, and upper flow bounds at most four. A negative control weakening
an averaging supply changes the optimum from 10 to 20. The [first fresh review](review-pooling-bypass-degree-three.md) and
[second fresh review](review-pooling-bypass-degree-three-second.md) both
PASS. The second reviewer's independent constructor passed 120 projection
LPs and 114 fixed-composition pooling LPs, including 56 excluded
compositions. The broader one-pool/single-quality hardness boundary was asserted
previously; priority of this precise degree refinement is unclaimed.
