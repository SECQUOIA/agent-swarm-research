# Independent review of the positive cubic gap certificate

Date: 2026-09-04. This is an independent agent review, not external peer review.
The reviewed certificate was supplied in
`code/multilinear_ratio/cubic_integer_certificate.py` and its recorded output.

**Verdict:** The exact 24-variable polynomial has ratio `6601/3225>2`. Its convex
envelope value is certified by matching rational primal and dual solutions. The finite
count reduction is exact. A separate fair left/right interval coupling proves the
universal cubic upper bound `8/3`. Novelty is a separate literature question.

## Polynomial and point

There are three disjoint groups of eight variables, denoted `a_i`, `b_i`, and `c_i`.
The polynomial is the sum of these six monomial families:

| Family | Coefficient per monomial | Number of monomials |
|---|---:|---:|
| `c_i c_j c_k`, `i<j<k` | 2 | 56 |
| `b_i c_j c_k`, `j<k` | 3 | 224 |
| `b_i b_j`, `i<j` | 13 | 28 |
| `a_i c_j` | 12 | 64 |
| `a_i b_j` | 8 | 64 |
| `a_i a_j`, `i<j` | 7 | 28 |

Thus all 464 monomials are squarefree, have positive integer coefficients, and have
degree two or three. The evaluation point is `a_i=1/4`, `b_i=1/2`, `c_i=3/4`.

At a binary vertex, let `A,B,C` be the success counts in the three groups. The
polynomial value is exactly

```
Φ(A,B,C)=2 choose(C,3)+3 B choose(C,2)+13 choose(B,2)
         +12 AC+8 AB+7 choose(A,2).
```

This count formula is used only on binary vertices. Treating it as an ordinary
polynomial identity in continuous sums would not be valid; the actual continuous
polynomial is the squarefree monomial sum specified above.

## Why the finite count problem is exact

For a multilinear polynomial on a cube, the graph at any interior point can itself
be represented by a distribution over lifted binary vertices: use independent binary
coordinates with the given means, for which the expectation of every squarefree
monomial equals its continuous value. Hence its convex envelope is the minimum
expected vertex value over binary distributions with the specified coordinate means.

Every such binary distribution induces a distribution on `(A,B,C)∈{0,...,8}³`, with
mean `(2,4,6)`, and exactly the same expected objective `Φ`. Conversely, given any
count distribution with these means, conditionally select a uniformly random subset
of size `A` from the first group, one of size `B` from the second, and one of size
`C` from the third. The within-group marginals are `A/8,B/8,C/8`; averaging gives
the required original marginals. The polynomial value depends only on the counts.
Thus the 729-state count problem is equivalent to the full `2^24`-vertex envelope
problem, not merely a relaxation of it. Conditional choices across groups may be
independent, since that already produces the required count-based objective.

## Rational dual and primal certificates

The proposed dual inequality is

```
7 Φ(A,B,C) ≥ 793 A+770 B+798 C−5882
```

for all integer counts in `{0,...,8}³`. Independent exact-integer enumeration verified
every one of the 729 inequalities. Equality occurs precisely at

```
(1,2,8), (1,5,6), (1,6,5), (8,4,2).
```

Therefore every feasible count distribution has expected objective at least

```
[793·2+770·4+798·6−5882]/7 = 3572/7.
```

The primal distribution is:

| Counts | Probability | Polynomial value |
|---|---:|---:|
| `(1,2,8)` | `2/7` | 405 |
| `(1,5,6)` | `4/7` | 507 |
| `(8,4,2)` | `1/7` | 734 |

The probabilities sum to one, their mean counts are exactly `(2,4,6)`, and their
expected value is `(2·405+4·507+734)/7=3572/7`. The uniform-subset construction above
lifts this primal solution to the original binary variables. Matching bounds prove
`vex f(x)=3572/7` exactly.

The following complete certificate verifier needs only integer arithmetic. It does
not call an optimizer or use floating-point tolerances:

```python
from itertools import product
from math import comb

def phi(a, b, c):
    return (2*comb(c, 3) + 3*b*comb(c, 2) + 13*comb(b, 2)
            + 12*a*c + 8*a*b + 7*comb(a, 2))

tight = []
for a, b, c in product(range(9), repeat=3):
    slack = 7*phi(a, b, c) - (793*a + 770*b + 798*c - 5882)
    assert slack >= 0
    if slack == 0:
        tight.append((a, b, c))
assert tight == [(1, 2, 8), (1, 5, 6), (1, 6, 5), (8, 4, 2)]

support = [(1, 2, 8), (1, 5, 6), (8, 4, 2)]
weights = [2, 4, 1]  # common denominator 7
assert sum(weights) == 7
for j, mean in enumerate([2, 4, 6]):
    assert sum(w*z[j] for w, z in zip(weights, support)) == 7*mean
assert sum(w*phi(*z) for w, z in zip(weights, support)) == 3572
assert 793*2 + 770*4 + 798*6 - 5882 == 3572
```

## Exact gap arithmetic

For positive monomials, their separate concave-envelope values sum to the concave
envelope of the full polynomial: a common uniform threshold simultaneously attains
`min_i x_i` for every monomial. The six families contribute respectively
`84,336,182,192,128,49`, giving `cav f(x)=971`.

Only the three-`c` family has positive separate convex-envelope value at this point:
its unweighted monomial lower value is `3·(3/4)−2=1/4`. Its contribution is
`56·2·(1/4)=28`. All other monomial lower values are zero. Consequently

```
tbtgap = 971−28 = 943,
chgap = 971−3572/7 = 3225/7,
tbtgap/chgap = 6601/3225 = 2+151/3225 > 2.
```

These computations were independently reproduced with exact integers and rational
numbers. The numerical search and the numerical LP were discovery tools; neither is
needed for the final certificate.

## Independent check of the universal `8/3` bound

For each coordinate, independently and fairly choose a left or right interval of
length `x_i` in `[0,1]`: `[0,x_i]` or `[1−x_i,1]`. With a common independent uniform
`U`, set the binary variable to one when `U` lies in its chosen interval. Its marginal
is exactly `x_i`.

For a monomial, choose an anchor with smallest marginal `u`. Conditional on the
anchor's orientation, a coordinate with the same orientation is one throughout the
anchor's interval. An oppositely oriented coordinate fails on an end segment of the
anchor interval with length `a_j=min{u,1−x_j}`. These failure segments are nested,
and the opposite-orientation choices are independent fair coins. Thus its expected
monomial deficiency is the expected maximum of the selected lengths `a_j`.

For a quadratic monomial, this equals `a_1/2=T_e/2`. For a cubic monomial, sort the
two lengths as `a_1≥a_2`. The expectation is

```
a_1/2+a_2/4 ≥ 3(a_1+a_2)/8 ≥ 3T_e/8,
T_e=min{u,(1−x_j)+(1−x_k)}.
```

The last inequality uses
`min(u,p)+min(u,q)≥min(u,p+q)` for nonnegative `p,q`. Affine terms have zero gap.
The same coordinate coupling applies simultaneously to every monomial; multiplying
by positive coefficients and summing therefore gives
`chgap≥(3/8)tbtgap`, or `R(3)≤8/3` on the unit cube. Together with the certificate,

```
6601/3225 ≤ R(3) ≤ 8/3.
```

The extension to finite nonnegative boxes follows from the already reviewed positive
expansion argument: affine rescaling gives nonnegative coefficients and degree at most
three, the original term-by-term gap is no greater than the expanded one, and the
full hull gap is preserved. This upper proof does not assert that `8/3` is sharp.

## Final result text and additional certificates

The final text in [`results/positive-cubic-gap.md`](../results/positive-cubic-gap.md)
was read after the above review. Its 24-variable polynomial, count reduction, certificates,
and general endpoint-orientation bound agree with this review. The count identity is
explicitly restricted to vertices. The general coefficient
`k/(1−2^−k)` is increasing because its reciprocal is the average of the first `k`
terms of the decreasing sequence `1/2,1/4,...`; this justifies taking the largest degree.

I also independently checked the added 18-variable certificate. With three groups of
six and coefficients `(2,3,9,10,7,7)` on the same six families, every one of the 343
integer counts satisfies

```
13 Φ_18(A,B,C) ≥ 962 A+778 B+842 C−4816.
```

The zero-slack states are precisely
`(1,1,6)`, `(1,4,4)`, `(2,1,6)`, and `(6,2,1)`.
The supplied primal uses the last three states with respective weights
`17/26,4/13,1/26`. Its mean is `(3/2,3,9/2)` and its objective is `2750/13`, matching
the dual bound. Independently recomputed values are

```
cav = 1647/4,    termwise lower = 10,
chgap = 10411/52,    ratio = 20891/10411 > 2.
```

There are 212 monomials. The same exact count-to-coordinate lifting proves validity
for the original variables; no assumption about continuous group-sum identities enters.

A further proposed homogeneous interior variant is also correct. Write the 24-variable
polynomial as `f=P+Q`, where `P` contains its cubic terms and `Q` its quadratic terms.
Introduce a new variable `z`, define `g=P+zQ`, and evaluate at the old point with
`z=999/1000`. Every monomial of `g` has degree three, every coefficient is positive,
and all 25 coordinates are strictly between zero and one.

The sum of the quadratic coefficients, counted with multiplicity over monomials, is

```
Q_max = 13·28+12·64+8·64+7·28 = 1840.
```

At every binary vertex, `0≤Q≤1840`. Every binary distribution with the new prescribed
means therefore obeys

```
E g = E f−E[(1−Z)Q] ≥ vex f−1840/1000
    = 3572/7−46/25.
```

The new concave envelope stays 971 because the new coordinate exceeds every old
marginal, so it does not change any term's minimum marginal. The termwise lower sum
stays 28: the original cubic terms are unchanged, and each lifted quadratic term has
zero monomial lower envelope at the new point. Thus

```
tbtgap_g = 943,
chgap_g ≤ 3225/7+46/25 = 80947/175,
tbtgap_g/chgap_g ≥ 165025/80947 > 2.
```

This is a certified lower bound on the homogeneous example's ratio, not a claim of
its exact convex envelope. Positivity of its hull gap follows, for example, from the
reviewed universal cubic bound applied to its positive termwise gap. The homogeneous
extension avoids relying on a coordinate fixed at the boundary of the cube.

## Stronger 192-variable certificate

A later certificate uses three groups of 64 variables, with the same respective
marginals `1/4,1/2,3/4`. The six family coefficients are now
`(2,3,120,105,70,63)`. At integer counts its value is

```
Φ_64(A,B,C)=2 choose(C,3)+3 B choose(C,2)+120 choose(B,2)
            +105 AC+70 AB+63 choose(A,2).
```

An independent enumeration using unbounded Python integers checked all
`65³=274625` inequalities

```
105 Φ_64(A,B,C) ≥ 871710 A+900446 B+899046 C−51743768,
0≤A,B,C≤64, all counts integral.
```

The only zero-slack states are `(4,19,64)`, `(5,19,64)`, `(16,40,43)`, and
`(64,31,17)`. All other integer slacks are strictly positive. This is the supplied
dual inequality after multiplying through by 105; in particular
`105·8302=871710` and `105·(299682/35)=899046`.

The independently evaluated matching primal is:

| Count state | Probability | Polynomial value |
|---|---:|---:|
| `(4,19,64)` | `241/735` | 251338 |
| `(5,19,64)` | `4/245` | 259640 |
| `(16,40,43)` | `419/735` | 351242 |
| `(64,31,17)` | `3/35` | 449936 |

With common denominator 735, the probability numerators are `241,12,419,63` and
sum to 735. The mean count vector is exactly `(16,32,48)`. Their expected objective
is `34172072/105`, matching the dual bound at that mean. Uniform conditional subsets
within the three groups lift this distribution to the original 192 variables exactly
as in the earlier certificates.

Independent rational arithmetic also gives

```
cav = 587944,
termwise lower = 20832,
tbtgap = 567112,
vex = 34172072/105,
chgap = 27562048/105,
ratio = 7443345/3445256 = 2+552833/3445256 > 2.
```

The separate concave-envelope contributions use the six orbit sizes
`choose(64,3)`, `64 choose(64,2)`, `choose(64,2)`, `4096`, `4096`, and `choose(64,2)`.
Only the first family has a positive termwise lower contribution, namely one-quarter
of its total coefficient. No floating-point values, solver feasibility tolerances,
or approximate marginal checks were used in this independent verification.

For a compact additional check on the enumeration, the minimum integer slack at each
fixed value of `C=0,...,64` was:

```
1735558,1542112,1359691,1188505,1028520,879174,741378,615342,501276,
399390,309894,229919,162368,107522,63772,30556,10360,0,1119,13754,
35768,69718,110771,144789,167782,182375,189723,190981,186569,177608,
164901,150409,133888,115721,98255,81243,63462,47991,35040,22614,
13128,6792,1611,0,2169,4829,11303,19948,30307,43257,56312,71186,
85711,99921,113816,125191,135377,140347,142482,138107,128658,110108,
84384,47459,0.
```

The inserted 192-variable section and updated headline lower bound in the final result
file were subsequently read. Its common-denominator dual and primal weights, all envelope
values, and the ratio agree exactly with the independent calculations above. The updated
headline `7443345/3445256≤R(3)≤8/3` is supported by the reviewed certificates.
