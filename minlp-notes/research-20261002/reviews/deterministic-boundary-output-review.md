# Review of deterministic boundary output

Date: 2026-10-02. Disposition: approved after a minor preprocessing
clarification. No blocking issue found in the enclosure schedule or the
nearby-local-minimum construction.

This is a fresh actual-file review of
[deterministic-boundary-output.md](../new-direction/deterministic-boundary-output.md),
including its use of the
[polynomial grid theorem](../new-direction/polynomial-pruned-grid-extension.md)
and [integer-label filter](../new-direction/implicit-convex-patch-certificate.md).
It supplements the earlier independent algebra audit of the benchmark.
It does not assess literature priority.

## 1. The certified enclosure schedule

The first trial with \(K_\mu=4^\mu\ge8\kappa\) is admissible for the
predecessor's contraction and state-cap bounds and has
\(K_\mu\le32\kappa\), including the initial-trial case. Extending its
stage budget to the two displayed accuracy thresholds does not affect
soundness or the state count. Failed earlier trials remain capped before
their tables are allocated.

The continuous hull's coordinate radius relative to the corrected-grid
point is at most \(5\sqrt{n\kappa}h_j\). Thus its Euclidean diameter is
at most \(10n\sqrt\kappa h_j\). The first threshold in the new note
makes this at most \(2^{-q}\). It also implies
\(h_j\le1/(10\sqrt{n\kappa})\), which is sufficient for the
predecessor's integer-grid unit-step argument and the individual-label
filter. The retained-label witness bound is then strictly below one in
squared distance, forcing every retained integer label to be the optimal
one. If this threshold already holds at stage zero, a nonfixed native
integer interval cannot exist because the original maximum width is below
one. This covers the initial-stage edge case.

The second threshold gives the desired objective gap using the unchanged
\(7Lnh_j^2/8\) estimate. The corrected-grid point survives both interval
and individual-label filtering. Hence the returned point belongs to the
returned box. Checking actual widths, integer singletons, and the actual
gap is a sound stopping condition without knowing the growth constant.

Both thresholds require only \(O(\operatorname{poly}(I)+q+\mu)\)
stages. Together with the predecessor's capped-trial and common-denominator
arguments this yields the claimed parameterized construction and verification
cost. The complete successful pruning history is retained; the result is
not based on checking a restricted final problem alone.

The interpretation as a certified Cauchy name is correct. Each enclosure
contains all original optimizers, and the objective bounds are finite
certificates. The growth promise proves termination and rate. A single
finite enclosure does not prove uniqueness or termination at all future
precisions. The note expressly distinguishes this output from a finite
independently verified exact uniqueness descriptor.

## 2. The nearby strict local minimum

For the benchmark \(G=F_n+y^2+3yh\), the nonnegative decomposition is
exact. It proves global point growth with \(g=9/64\), a unique global
optimizer \((a,0)\), and the stated constant curvature ratio \(140/9\).
The added pure second derivative is nonpositive, so \(L=35/16\) remains
valid. Degree four and maximum bag size three are preserved.

On the face \(x_n=0\), minimizing over \(y\) gives
\(y(u)=3u_{n-1}^2/16\), which lies in its original interval. The reduced
objective is exactly
\(H(u)=F_{n-1}(u)+7u_{n-1}^4/256\), and it is globally strongly convex.
Comparison with the optimizer prefix proves
\(\|u-a_{0:n-1}\|\le\sqrt7\,a_n/3<a_n\).
Since every prefix coordinate is at least \(a_{n-1}\), and
\(a_n\le a_{n-1}/16\), this indeed proves strict interiority. It also
keeps every coordinate strictly below its upper bound.

At the lifted point \(b\), the only active coordinate is \(x_n\).
Its inward derivative is \(u_{n-1}^2/16>0\). The free Hessian's Schur
complement is
\(\nabla^2F_{n-1}+21u_{n-1}^2ee^\top/64\), and its eliminated diagonal
entry is two. Both are positive definite, so second-order sufficiency
holds. More directly, continuity keeps the inward derivative positive
in a neighborhood, and strong local minimality on the face then proves
strict constrained local minimality in the full box.

The reduced minimum is positive: its two nonnegative terms could vanish
together only if the positive terminal coordinate of the optimizer prefix
were zero. Thus \(b\) is nonglobal. Finally,
\(u_{n-1}<17a_{n-1}/16\) gives
\(y(u)<867a_n/1024<a_n\), verifying the distance bound
\(\|b-(a,0)\|<\sqrt3a_n\). The argument includes \(n=1\).

## 3. Scope of the obstruction

The input size is \(O(n\log(n+1))\), whereas the distance scale is doubly
exponentially small in \(n\). Therefore no radius bounded below by
\(2^{-\operatorname{poly}(I)}\) uniformly isolates the global optimizer
from other box KKT points satisfying strict complementarity and second-order
sufficiency. A closure method requiring such a full relative Euclidean
neighborhood may need exponentially many accuracy bits.

This conclusion does not apply to every rational rectangle, directional
cut, correlated root descriptor, or global pruning method. The note makes
those distinctions. Its short nonnegative decomposition and recurrence
already certify this particular global optimum, so the example is neither
a hardness proof nor a counterexample to all compact exact outputs.

## 4. Clarification and verification

I requested that the note explicitly define \(n\) after the predecessor's
preprocessing, and handle the zero-variable case directly before using
thresholds that divide by \(n\). This is a model-completeness clarification,
not a change to the proof for \(n\ge1\). The author added this clarification,
and I checked it in the final file.

I read the author's exact diagnostic and ran

```text
python3 research-20261002/reviews/check_deterministic_boundary_output.py
```

It passed four symbolic identities, an exact \(n=1\) local-minimum witness
with 100 rational root-isolation bisections, and 243 enclosure-budget
fixtures. It does not implement the general grid algorithm. A separate
inline `python3` check passed local links, trailing whitespace, paired
mathematical delimiters, and sequential equation tags in the note and
review.

The mathematical review read the actual proofs and their two predecessor
interfaces. No project-wide verification, CI inspection, or external
literature search was performed.
