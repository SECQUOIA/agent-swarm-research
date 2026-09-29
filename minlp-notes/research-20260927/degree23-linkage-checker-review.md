# Independent review of the degree-23 linkage checks

Date: 2026-09-28. Status: passed. Reviewer:
`one_parameter_spectrahedral_fields`; not the author of the explicit
equations, eliminant, or retained checks.

I read [the negative example](degree23-linkage-negative-example.md),
[its Python checker](check_degree23_linkage.py), and
[its Singular script](check_degree23_linkage.sing). I then ran:

```sh
SINGULARPATH=/tmp/degree23-singular/usr/share/singular/LIB \
LD_LIBRARY_PATH=/tmp/degree23-singular/usr/lib/x86_64-linux-gnu \
python research-20260927/check_degree23_linkage.py \
  --singular /tmp/degree23-singular/usr/bin/Singular
```

All assertions passed. Singular reported that an optional dynamic
acceleration library was unavailable, then completed the calculation.
No system packages were installed by this review, and no project-wide
checks or CI inspection were performed.

The two scripts use exactly the same five homogeneous quadrics and
degree-23 eliminant as the note. The Python checks verify their
vanishing at all nine proposed residual points, rank five of the
projective Jacobian at those points, the sixth-quadric identity, and
linear independence of the six quadrics. The finite-field
irreducibility test is sufficient: degree 23 is prime, so
`t^(293^23)=t mod p` permits factor degrees only one or 23, and
`gcd(p,t^293-t)=1` excludes degree one. The leading coefficient is
nonzero modulo 293. Exact Sturm counting gives three real roots.

The Singular checks establish a homogeneous intersection of dimension
one and degree 32 with the five-quadratic complete-intersection
Hilbert series. They compute the colon residual, verify its degree
23 and Hilbert numerator, verify the double colon and saturation,
and verify that it has no projective point on `x5=0`. The affine
coordinate algebra has dimension 23, and the shape basis contains
the asserted irreducible degree-23 polynomial in `x4`. This is enough
to make that affine coordinate algebra a field. The scripts further
verify the exact ideal equality between the six-quadratic base and
the union of the field point with the extra rational point, of degree
24.

These computations therefore certify both informative failures of
this candidate: the degree-23 field has three real embeddings, and
its full quadratic vanishing space retains a distinct rational
projective point. They do not establish an example with one real
embedding, a convex quartic realization, a general degree bound, or
publication priority.

The note's chart distinction is correct. A retained point at infinity
does not alone give a second affine zero. The stated obstruction for
globally convex rational SOS quartics additionally uses the linked
flat-direction reduction, which removes the rational direction and
preserves the minimizer's field. The reduced four-variable problem
then has isolated-point quadratic Bezout bound 16, contradicting
degree 23. This conclusion uses convexity and positive definite
Hessian at the zero; it does not assert the same obstruction for an
arbitrary affine SOS singleton.
