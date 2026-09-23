# A finite two-bit gap for every continuous scalar convex graph

Date: 2026-09-05. Status: independently reviewed finite lemma.

Let `f` be a continuous convex real function on `[0,1]`, and fix absolute
error `epsilon>0`. Compare whole-graph approximations by arbitrary convex
lifts with `p_conv` general integer variables and by binary linear lifts
with `p_bin` binary variables. With unrestricted continuous formulation
size and real coefficients,

```
p_conv<=p_bin<=p_conv+2.                              (1)
```

This is a finite comparison. It does not assert a polynomial-size or rational
construction from an evaluation oracle, and it applies to one scalar output.

Write `N_epsilon` for the smallest number of chord intervals needed to cover
`[0,1]` with vertical chord error at most `epsilon`. Uniform continuity of
`f` ensures that this number is finite. Each interval's band from chord minus
`epsilon` to chord contains the exact graph and admits only the prescribed
error, so logarithmic encoding of their finite union gives

```
p_bin<=ceil(log2 N_epsilon).                          (2)
```

The parity-support span argument in the
[curvature note](accuracy-dependent-curvature-precision.md) uses only continuity
and convexity, not differentiability or monotone curvature. It therefore gives

```
N_(2epsilon)<=2^(p_conv).                             (3)
```

The remaining observation is

```
N_epsilon<=3N_(2epsilon).                             (4)
```

To prove it, take one interval whose chord error is at most `2epsilon`, and
let `g` be its chord minus `f`. This is a continuous concave nonnegative function
with zero endpoint values. If its maximum is at most `epsilon`, keep the interval.
Otherwise, the set where `g>=epsilon` is a closed nondegenerate interval `[u,v]`
strictly inside it, with `g(u)=g(v)=epsilon`.

On the two outside intervals, `g<=epsilon`. The new chord error of `f` equals
`g` minus its own chord on that subinterval, so it is nonnegative and at most
`g<=epsilon`. On the middle interval, that chord of `g` is identically `epsilon`,
and its new error is `g-epsilon<=epsilon`. Thus at most three subintervals suffice.
Apply this to every interval in a `2epsilon` partition to obtain (4).

Combining (2)--(4), and using that `p_conv` is an integer, gives

```
p_bin<=ceil(log2(3*2^(p_conv)))=p_conv+2.
```

The finite Hamming-distance disjunction can exclude unused binary strings.
All bands are bounded after adding global input/output bounds, so finite
valid linear constants exist. No claim of ideality for the relaxation with
fractional bits is needed.

The midpoint/parity obstruction and logarithmic finite-disjunction encoding
are established methods. This note records their elementary scalar convex
consequence and does not claim independent priority. A compact computational
version needs random access to a near-optimal partition; a sequential algorithm
using time proportional to the number of intervals is insufficient when that
number is exponential in the accuracy encoding.

The [first curvature audit](review-accuracy-dependent-curvature-precision.md)
and [second curvature audit](review-accuracy-dependent-curvature-precision-second.md)
both checked this supporting result and passed.
