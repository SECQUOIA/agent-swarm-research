# Independent review: fractional-power arc-flow arithmetic barrier

Date: 2026-09-05. Verdict: **PASS**. The construction proves the stated
Square-Root-Sum reduction, including the integer-resistance variant. No
NP-hardness, completeness, or approximation lower bound follows from this
argument alone.

Reviewed: [fractional-power candidate](potential-flow-fractional-power-arc-barrier.md).

## Reduction checks

For `phi(x)=sign(x)*|x|^(3/2)`, the derivative is
`(3/2)*sqrt(|x|)` away from zero and equals zero at zero. It is continuous
there. The function is strictly increasing, odd, and has infinite limits
of opposite sign. Thus it has precisely the stated regularity, despite
the derivative vanishing at zero.

Orient the cycle consistently and let edge `i` leave vertex `i`. Assigning
`b_i=c_i-c_(i-1)` uses the stipulated outgoing-minus-incoming conservation
convention. The nominations are integral and telescope to total zero.
Every conserving flow differs from `c` by one common scalar circulation;
there are no other cycle degrees of freedom.

All resistances are positive. Therefore the cycle residual is strictly
increasing and continuous with opposite infinite limits, so it has exactly
one root. A zero residual lets the edge drops be integrated consistently
around the cycle to obtain potentials, unique up to a constant. Conversely,
any physical flow must have zero cycle residual. This establishes existence
and uniqueness without an extra flow-feasibility assumption.

The identity at zero is exact:
`(1/a_i)*phi(a_i)=sqrt(a_i)` and `K*phi(-1)=-K`.
For an increasing residual, `h(0)<=0` means its root lies at or to the
right of zero. Since the last flow is `-1+z*`, the lower-capacity comparison
has the correct direction, including equality. Reversing that edge changes
both its incidence column and signed flow, preserves the physical equations
because the law is odd, and turns the queried lower bound into upper bound
one.

The simple-cycle requirement poses no difficulty. One may uniformly append
two unit radicands and increase the threshold by two before constructing
the network. The source answer is unchanged and the resulting cycle has
at least three vertices even for an empty residual list. For the stipulated
positive-threshold, positive-radicand source, no exceptional sign case is
then needed. The draft's alternative of separately handling tiny inputs
or padding them is also correct.

The constructed nominations are differences of input integers. Rational
resistances `1/a_i` and `K` have polynomial bit length. The integer scaling
factor `A=product_i a_i` has bit length at most the sum of the radicand
bit lengths plus a constant. Each `A/a_i` and `AK` also has polynomial
length and is a positive integer. Multiplying all resistances by `A`
scales the residual without changing its root or the queried capacity.

If a capacity-validation convention requires finite bounds on all other
edges, those can be added without affecting the reduction. The root lies
strictly between `-max_i a_i` and one, so every physical edge flow has
absolute value at most `max_i a_i+1`. Give the unqueried edges these
redundant rational bounds. Singleton nomination and resistance boxes then
make universal capacity validation exactly the same comparison problem.

## Source and interpretation

Etessami and Yannakakis explicitly use the positive-integer radicands and
integer-threshold version of Square-Root-Sum in their
[primary author manuscript](https://homepages.inf.ed.ac.uk/kousha/nash_focs07_full_j_spec_issue_sub.pdf),
introduction. This supports the precise source convention used here; the
reduction does not assume that this arithmetic comparison is NP-hard.

The obstruction is an unbounded sum of radicals within one cycle equation,
even though the circulation itself has one dimension. Introducing one
radical variable per edge would no longer be a fixed-dimensional
real-algebraic formulation. This explains why the polynomial-law proof
does not automatically extend to this fixed algebraic law. It does not
contradict the reviewed polynomial or piecewise-polynomial results.

A bounded search for fractional-power network complexity did not identify
this exact reduction. That is insufficient to certify novelty; the
construction is elementary and might appear in other arithmetic-complexity
contexts.

## Independent computational check

[The separate checker](../code/potential_flow_mpd/fractional_power_arc_review.py)
passed 103 small cycle instances, including `a=(1,4,9)` at thresholds
five, six, and seven, so both strict directions and exact equality were
included. It checked the injection convention, zero-residual identity,
capacity direction, edge reversal, and common integer-resistance scaling.
The largest discrepancy between roots before and after scaling was
`2.6e-16`.

These numerical checks concern small, well-separated examples and an exact
integer-square equality case. They do not supply an algorithm for arbitrary
Square-Root-Sum instances or assume a polynomial separation bound.

## Two immediate deductions worth retaining

The same proof works for **every fixed reduced rational exponent `p/q>1`
with even denominator `q`**. Coprimality makes `p` odd. Set

```
phi(x)=sign(x)*|x|^(p/q),
c_i=a_i^(q/2),
beta_i=a_i^(-(p-1)/2),
c_last=-1, beta_last=K.
```

Then `beta_i*phi(c_i)=sqrt(a_i)`. The common law is continuously
differentiable and strictly increasing, and all powers in the construction
have fixed integer exponents, hence polynomial encoding length. The same
cycle/root/capacity proof applies. Multiplying resistances by
`product_i a_i^((p-1)/2)` gives an integer-resistance version as well.
This deduction establishes only the same Square-Root-Sum lower bound.

There is also a direct boundary for the fixed-core optimization theorem:
**convex semialgebraic leaves cannot simply replace polyhedral leaves**
with the same conclusion. With no core parameters, take scalar leaves

```
P_i={y_i : y_i>=0, y_i^2=a_i, y_i<=a_i+1}.
```

Each leaf is a compact convex singleton with a degree-two rational
description. Add one slack leaf `0<=s<=K` and the single aggregate equation
`sum_i y_i+s=K`. Feasibility is exactly Square-Root-Sum. Thus even
fixed-dimensional convex nonlinear leaves can introduce the same arithmetic
barrier; convexity and bounded leaf dimension alone do not resolve it.
This is consistent with the common-algebraic-field caveat in the reviewed
linear-fiber theorem.
