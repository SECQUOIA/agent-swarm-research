# Independent review of quaternion-circuit quartic realization

Date: 2026-09-28. Verdict: the construction passes this adversarial
review. Publication priority remains unestablished.

I did not develop the quaternion realization. This review covers the
complete frozen [construction](unit-quaternion-circuit-quartic-realization.md)
with SHA-256
`4f1341519769a1ffdf2b30aae4985223ff67bee112a56e0e9e27ffa5abc0f3c1`.
I previously reviewed the circle specialization and its conditioning
variant. Here I independently checked the quaternion identities,
arbitrary shared-parent patterns, rounding, and the interface to the
[quantitative Hessian certificate](sos-convex-quartic-realization.md).
No substantive correction was needed.

After review, I reconciled the manuscript's administrative status and
verification updates. The resulting SHA-256 is
`8698b0710ad4e8a5763dd80297a868a4db996c4afd2b68c30c150b836a3eaf5b`.
Those changes accurately describe the checks and do not change the
mathematical statement or proof; the verdict remains a pass.

## Exact identity and arbitrary circuit sharing

Quaternion conjugation and norm multiplicativity give
\(\langle c,ab\rangle=\langle a,c\bar b\rangle\).
For a product gate with unit value \(p_i=p_ap_b\), expansion gives

\[
 q_i-2\langle p_i,X_i-X_aX_b\rangle-q_a-q_b
   =|X_i-p_i|^2-|X_a-p_i\bar X_b|^2.
 \tag{1}
\]

The identity uses only \(|p_i|=1\), not unit norms of the formal
variables. It is therefore an identity on the whole variable space,
not merely on the circuit's zero set. Since
\(p_i\bar p_b=p_a\), translating to the circuit point gives

\[
 |U_i|^2-|U_a-p_i\bar U_b|^2.
\]

The second term is the negative square of a linear map. If the two
parents coincide, the same identity applies with both occurrences of
\(U_a\), and the norm of that map is at most two. The worst
negative contribution is then \(-4|U_a|^2\). No assumption of
distinct gates or algebraically independent gate values is present.

For an inverse gate, the centered identity is
\(|U_i|^2-|U_a|^2\), since conjugation is orthogonal and
\(p_i=\bar p_a\). For a constant gate it is \(|U_i|^2\).
All exposing quadratics thus have zero value and full gradient at the
true circuit point.

The circuit weights also accommodate unbounded fanout. At a fixed
earlier block \(j\), each later gate contributes at worst
\(-4\omega_i|U_j|^2\) in the scalar lower bound. Summing
over all later gates, rather than over only distinct descendants,
gives

\[
 \omega_j-4\sum_{i>j}\omega_i
 \geq\frac{11}{15}\omega_j
 \geq\frac{11}{15}\omega_*.
\]

Cross terms between different parent blocks have already been included
in the inequality \(|u-v|^2\leq2|u|^2+2|v|^2\).
For the upper bound, every negative square can simply be dropped,
leaving \(\sum_j\omega_j|U_j|^2\leq\|U\|^2\).
This proves both matrix bounds for arbitrary shared circuits.

## Residual and perturbation estimates

The triangular residual system has identity diagonal Jacobian blocks,
so its determinant is one. For distinct parents, each scalar
quaternion product coordinate is a bilinear form with a signed
orthogonal coefficient matrix. Its full symmetric quadratic matrix
has norm \(1/2\). With coincident parents, the square coordinates
are the familiar diagonal form and the three forms \(2wx,2wy,2wz\);
their symmetric quadratic matrices have norm one. Linear constant
and inverse residuals have zero quadratic part. Thus the asserted
uniform norm-one bound is valid.

The four-row Jacobian of a product residual has operator norm
\(\sqrt3\) for distinct parents. For repeated parents it is
at most \(\sqrt5\), by bounding the sum of the two orthogonal
parent maps by two. Inverse and constant gates have smaller norms.
The manuscript's bound three is therefore conservative. It bounds
every scalar residual gradient as well, giving
\(\|J\|_F\leq3\sqrt N\). The determinant then yields the
stated smallest singular-value bound with \(V=4N\).

Each coefficient approximation changes one gate's exposing form by
\(-2\langle\Delta p_i,r_i\rangle\). With coordinate errors
at most \(\eta\), the quadratic matrix error is at most
\(8\eta\), and the gradient error is at most
\(2\cdot3\cdot2\eta=12\eta\). Summing at most \(s\)
weights bounded by one gives the stated estimates. Exact vanishing
is preserved because every residual still vanishes exactly at \(p\).

The leading quadratic lower margin after rounding is at least
\((11/15-1/4)\omega_*=(29/60)\omega_*\), exceeding
the claimed \(\gamma=\omega_*/4\). The upper bound is at
most \(1+\omega_*/4<2\), and the gradient bound is at most
\(3\varepsilon/4\). All constants therefore have slack.

## Approximation, realization, and bit complexity

The approximation argument uses exact unit norms only for the true
gate values. The rounded values themselves need not be unit. If both
parent errors are at most \(e\), multiplication differs from the
true product by at most \(2e+e^2\). Conjugation is a valid
approximation operation for inverse gates because the true inverse
equals conjugation. No inverse of a possibly nonunit approximation is
computed.

Rounding four coordinates to mesh \(h\) contributes at most
\(2h\) in Euclidean norm. In topological order, the running
maximum error is bounded by the recurrence
\(e_i\leq3e_{i-1}+2h\), starting at zero. The mesh choice
keeps every error below \(\eta/2\leq1\), so the assumption
needed for \(2e+e^2\leq3e\) is justified inductively. This
works for coincident parents and reused earlier gates as well.
Constant gates are rounded directly from their input fractions, with
their input bit lengths included in the running-time bound.

I checked each abstract hypothesis of the cited quartic construction:
there are exactly \(N\) rational residuals, with controlled
quadratic parts, gradient bounds and an invertible controlled Jacobian;
the rational quadratic \(G\) vanishes exactly and has positive
leading part and small gradient. The specified square dyadic
\(\varepsilon\) is the stronger bound needed for a full
positive definite Hessian Gram. Its factor \(N\) in the last
denominator is present. Consequently the ordinary global Hessian
estimate and the Gram Schur-complement estimate both apply.

The rational certificate does not require expanding the rational
optimizer. For fixed output quadratics, the translated Gram entries
are polynomials of degree at most two in the center: the centered
constant block is quadratic, the cross block affine, and the trailing
block constant. The circle review's coefficient-derivative estimate
therefore applies with the bound \(\|p\|\leq N\). The known
positive rational spectral margin and polynomial coefficient lengths
require only polynomially many center bits. Exact projection onto the
Hessian coefficient equations is nonexpansive and preserves positivity.

All reciprocal logarithms in the construction have polynomial length:
\(\log V=O(\log N)\), \(\log(1/\nu)=O(N\log N)\),
and \(\log(1/\gamma)=O(s)\). The remaining tolerances and
dyadic meshes inherit polynomial lengths. Expanding the fixed-degree
quartic and the full Gram requires polynomially many rational entries.
The leading part of \(G\) is positive definite, so the polynomial
has degree exactly four. Its SOS factors vanish at the unique real
common zero of the triangular residual system, which proves the
claimed singleton and rational-minimizer promise.

## Exact checks and scope

I wrote and ran an independent
[symbolic and rational checker](check_quaternion_realization_independent.py):

```text
python research-20260927/check_quaternion_realization_independent.py
```

It passed symbolic quaternion norm and inner-product identities,
the product exposer identity, its repeated-parent substitution, and
the scalar quadratic matrix bounds. An eight-gate rational circuit
with repeated parents, reused gates, and an inverse passed exact
zero/gradient checks, determinant-one Jacobian, positive weighted
exposer margin, and exact vanishing plus matrix and gradient error
bounds after dyadic coefficient rounding.

These finite checks supplement the general proof. They do not prove
the uniform bit bound, which was checked analytically above. I did not
run project-wide checks, inspect CI, or formalize the argument in Lean.

The theorem covers unit-quaternion multiplication and conjugation
circuits, not arbitrary bounded arithmetic circuits. Its positivity
identity is material. No sign-complexity conclusion follows from the
realization alone. A separate fresh reviewer is checking the proposed
PosSLP compiler. This review supplies mathematical verification of the
realization, not a publication-priority claim.

An inline `python - <<'PY'` check passed local-link, math-delimiter,
whitespace, control-character, and final-newline checks on this review
and its checker: two files and three local links. `git diff --check --`
restricted to those paths also passed.
