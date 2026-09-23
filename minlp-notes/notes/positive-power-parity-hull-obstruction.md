# Pairwise midpoint control does not control a multivariate convex hull

Date: 2026-09-05. Status: elementary supporting observation; no novelty claim.

The scalar parity-span argument does not extend by simply taking the convex
hull of a higher-dimensional parity support with a dimension-independent error
factor. This already fails for a sum of positive pure powers.

Let `r>=2`, `D>=2`, and

```
f(x)=sum_(i=1)^r x_i^D,             x in [0,1]^r.
```

Consider the `r` points `v^k=1-e_k`. Each has function value `r-1`. For two
distinct points, their midpoint has two coordinates equal to one half and
all others equal to one, so

```
[f(v^k)+f(v^ell)]/2-f((v^k+v^ell)/2)=1-2^(1-D)<1.
```

Their uniform barycenter is `(1-1/r)1`, and its full Jensen error is

```
(1/r)sum_k f(v^k)-f((1/r)sum_k v^k)
 =(r-1)-r(1-1/r)^D.
```

For fixed `r`, this tends to `r-1` as `D` grows. For example, choosing
`D>=r ln(2r)` makes the final subtracted term at most one half, so the
Jensen error is at least `r-3/2`.

Thus all pairs can satisfy a unit midpoint-error condition while the graph
convex hull admits an error of order `r`. This is only an obstruction to
that proof mechanism: no claim is made that these finitely many points are
the entire parity support of a valid formulation, or that the example proves
a lower bound on a compact approximation algorithm. The reviewed
power-transformed covariance arguments avoid this invalid inference.
