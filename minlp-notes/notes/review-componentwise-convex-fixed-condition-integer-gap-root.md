# Independent root review: finite conditioned convex-vector gap

Date: 2026-09-05. Verdict: PASS for the current theorem in
[the candidate](componentwise-convex-fixed-condition-integer-gap.md).
This is a mathematical review, not an external peer review or priority claim.

The proof applies to arbitrary convex lifts, including nonclosed sets and
unbounded integer coordinates. Each parity support supplies midpoint errors
in the compact body. Limits are taken only in continuous projected graph
inequalities, so endpoint witnesses are unnecessary. Summing nonnegative
component Jensen gaps gives the stated infinity and Euclidean bounds.

The concave-gap maximum is at most twice its midpoint value. The finite
interval-cover trimming argument terminates with no more intervals than
the cover, including singleton supports and endpoint contacts. Restricting
a convex chord interval cannot increase its maximum error.

The level-cut refinement is valid for nonstrictly convex functions:
superlevel sets of a continuous concave gap are intervals. Their endpoints
partition each side into consecutive height ranges of width at most t,
and the middle range also has width at most t. Plateaus only eliminate
cuts. On a subinterval, the new convex-function chord gap equals the old
concave gap minus its endpoint chord and is bounded by that range width.
The resulting count is 2 ceil(E/t)-1 when E/t>=1.

The final rectangular bands contain the exact graph and admit errors in
the claimed inner infinity or Euclidean ball. All polyhedra are bounded,
so finite big-M constants exist with real coefficients; unused binary
strings must be excluded as the proof states. This is a finite linear
formulation argument, not a polynomial rational construction.

For an unconditional body, coordinate extrema exist by compactness and
are positive by interiority. Averaging independent sign flips of an
extremal point yields the corresponding signed axial vectors. Their
convex hull contains (1/m) B_infinity after positive diagonal scaling.
Such scaling preserves both convexity and admissible formulation counts.
The box bound ceil(log2(4m-1)) and unconditional bound
ceil(log2(4m^2-1)) therefore follow without a bound on original coordinate
scales. For m=1 the bound is two, consistent with the scalar statement.

No new tests are needed for this finite geometric lemma: the conclusions
follow from the interval and norm inequalities above and do not depend
on numerical approximations. The proof does not establish compact size,
rational endpoint encoding, or an output-dimension-independent bound.

## Addendum: simplex bands

The appended sharpenings also PASS. If g,v are nonnegative vectors with
one-norm at most s, then

```
||g-v||_2^2 <= ||g||_2^2+||v||_2^2 <= 2s^2,
||g-v||_1 <= 2s.
```

The simplex band w=T-v, v>=0, sum v<=s is a bounded linear polyhedron.
It contains the exact graph whenever the sum of component chord gaps is
at most s. In the Euclidean case choose s=r/sqrt(2), giving the stated
refinement factor 2sqrt(2m)R/r. For an unconditional body normalized to
contain B_1 and lie inside B_infinity, use s=1/2 and the parity-span gap
bound 2m. This gives at most 8m-1 subintervals per parity span and additive
count ceil(log2(8m-1)). Irrational constants are permitted in these finite
real-coefficient comparisons. Neither sharpening implies a polynomial
rational compiler or improves the separately cited stronger box bound.
