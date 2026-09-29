# A limit of the sparse book-graph certificate route

Research date: 2026-09-27. Status: exact counterexample to a proposed proof
strategy, with an explicit SDP–RLT certificate for the example. This does
not settle SDP–RLT exactness for all four-variable stars. No novelty claim
is made.

The [earlier four-star investigation](../research-20260925/four-star-analytic.md)
proposed subtracting nonnegative RLT products from a box-nonnegative star
quadratic, then applying the corrected SPN theorem for the book graph
\(T_5\) to its orthant homogenization. The following example shows that
this bridge cannot hold universally if the remaining quadratic must
retain book sparsity. The obstruction persists under independent leaf
complementations and center complementation.

## Exact example

On \((t,y,z,w)\in[0,1]^4\), put

\[
q=(y-2t+\tfrac12)^2+(t-\tfrac3{16})z
 +(\tfrac{13}{16}-t)w.
\]

The interaction graph is a star centered at \(t\). The identity

\[
\begin{aligned}
q={}&(y-2t+\tfrac12-\tfrac14z+\tfrac14w)^2\\
 &+\tfrac12 yz+\tfrac12(1-y)w
 +\tfrac1{16}\{z(1-z)+w(1-w)\}+\tfrac18zw
\end{aligned}
\]

proves nonnegativity and is a full SDP–RLT certificate. Every term after
the square is a nonnegative multiple of a box-literal product. The
minimum is zero; for example, it is attained at
\((t,y,z,w)=(1/2,1/2,0,0)\). More generally, the whole segment

\[
t\in[1/4,3/4],\qquad y=2t-1/2,\qquad z=w=0
\]

consists of minimizers. Two additional minimizers are
\((1/8,0,1,0)\) and \((7/8,1,0,1)\).

In particular, the example has an exact full SDP–RLT relaxation. The
certificate uses leaf–leaf products and an affine square whose expansion
has leaf–leaf terms. Those terms cancel in the resulting polynomial.

## No star-supported RLT correction gives a bound release

A box literal is one of \(t,1-t,y,1-y,z,1-z,w,1-w\). Allow a correction
\(R\) that is a nonnegative combination of literal products of degree at
most two. First suppose that every product is supported on the center
and at most one leaf. Constants and individual literals may also be
included, making this a larger class than needed for standard RLT.

Choose arbitrary leaf orientations. In the resulting extended domain,
the center remains in \([0,1]\), and each original leaf is allowed either
in \([0,\infty)\) or in \(( -\infty,1]\). Suppose that \(q-R\) were
nonnegative on this extended domain.

At the box minimizer \((1/2,1/2,0,0)\), one has \(q=0\) and \(R\geq0\).
Thus \(R=0\) there. Every literal product involving \(y\) and supported
on \(t,y\), including \(y(1-y)\), is strictly positive there. Every
nonnegative coefficient of such a product must therefore be zero.
The same argument removes center-only products and all positive
constant terms. Consequently \(R\) is independent of \(y\).

If the orientation releases the upper bound of \(y\), the extended
domain contains

\[
(t,y,z,w)=(1,3/2,0,1),\qquad q=-3/16.
\]

If the orientation releases its lower bound, the domain contains

\[
(t,y,z,w)=(0,-1/2,1,0),\qquad q=-3/16.
\]

At either point every variable other than \(y\) remains in its original
box. Since \(R\) is independent of \(y\), its literal-product
representation gives \(R\geq0\) at that point. Hence \(q-R<0\), a
contradiction. The argument allows arbitrary orientations of \(z,w\),
because each extended domain still contains both of their box endpoints.
Complementing the center only swaps the descriptions of the endpoints.

## Allowing cancellations in the RLT correction does not help

The conclusion also holds when individual products in \(R\) may involve
two leaves, provided their total polynomial has star support. This is
precisely the support requirement when both \(q\) and \(q-R\) have star
support.

To see this, collect all products involving a particular distinct pair
of leaves \(u,v\). Their sum is a bilinear polynomial nonnegative on
\([0,1]^2\). Star support forces its \(uv\) coefficient to vanish:
no other pair or center–leaf term can cancel that coefficient. The sum
is therefore an affine nonnegative polynomial
\(A+B u+C v\). It can be written as

\[
m+B_+u+(-B)_+(1-u)+C_+v+(-C)_+(1-v),
\quad m=A+\min(B,0)+\min(C,0)\geq0,
\]

where \(r_+=\max(r,0)\). Replace the pair's products by this equivalent
nonnegative combination of constants and individual literals. Repeating
for each leaf pair reduces to the class already ruled out above.

Thus even an unrestricted RLT correction whose aggregate polynomial
retains star support cannot make the usual two-hub homogenization
copositive after an orientation and bound release. Since copositivity of
that homogenization is equivalent to nonnegativity on the extended
domain, the standard \(T_5\) route fails on this exact instance.

This does not rule out a certificate using a denser intermediate matrix,
a different representation, or a direct proof of full SDP–RLT exactness.
It identifies why sparsity of the final polynomial alone does not justify
imposing that same sparsity on the intermediate certificate.

## Verification and scope

The identity was expanded manually by the author and a delegated reviewer,
`/root/frontier_cube/four_star_route/four_star_bound_bridge/sparse_copositive_bridge`.
A second delegated reviewer,
`/root/frontier_cube/four_star_route/four_star_bound_bridge/sparse_copositive_bridge/zero_obstruction`,
independently checked the identity, the
listed minimizers, the two negative extension points, and the
orientation argument. An exact SymPy calculation checked the polynomial
identity and all five specified points. The author then ran the same
targeted symbolic checks independently. The reusable author check is

```text
python research-20260927/check_four_star_bound_bridge.py
```

This command passed. It checks the certificate identity, zero segment,
three specified minimizers, two negative extension witnesses, and the
algebraic reduction of a leaf-pair collection to an affine polynomial.
It leaves the analytic sign and orientation arguments to the written
proof and independent reviews.

These checks establish the displayed algebra and the stated obstruction,
not novelty or a characterization of all exact star objectives. No
project-wide verification or CI inspection was performed.
