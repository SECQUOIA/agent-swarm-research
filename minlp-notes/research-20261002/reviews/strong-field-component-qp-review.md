# Review of the strong-field component QP theorem

Date: 2026-10-02. Disposition: approved after two minor model/encoding
clarifications. No blocking issue found.

This is a fresh independent actual-file review of
[strong-field-component-qp.md](../new-direction/strong-field-component-qp.md).
It checks the exact algorithm, finite noise law, probability argument, and
certificate scope. It is not a literature comparison or priority assessment.

## 1. Persistence and the finite law

For a symmetric Hessian, each base derivative is affine, so its exact
interval over the continuous box follows from independent endpoint choices.
Its range width is \(R_i=\sum_j|H_{ij}|w_j\). The two strict sign cases
force the respective original bound at every global optimizer. The same
conclusion holds for native integers by integrating the derivative between
successive labels. Keeping equality cases bad correctly handles finite
noise atoms.

Each bad event depends only on its own original noise coefficient and
deterministic base data. Thus the Bernoulli events are independent before
any substitution. No conditional-independence assertion about an adaptive
pinning rule is needed. Substituting the certified coordinates leaves no
quadratic cross terms between distinct components of the bad induced graph.

The finite-grid probability bound is valid for a closed interval:
\(q_i\le R_i/(2\sigma)+1/M\). The two sufficient bounds each contribute
at most \(1/(16\Delta)\) to \(a_iq_i\), giving
\(\beta\le1/(8\Delta)\). The geometric-series denominator is consequently
at least one half in that regime. Choosing the least allowed power of two
requires only polynomially many sampling bits, even when a native-integer
label count is exponentially large in its endpoint encoding.

The exact-probability regime \(4\Delta\beta<1\) is also correct. Its
displayed bound retains the numerical reciprocal
\(1/(1-4\Delta\beta)\); polynomial runtime is not asserted when this
quantity is unrestricted. The strong-noise sufficient condition supplies
a uniform gap.

## 2. Exact component optimization, including singular cases

The component configuration count is exactly bounded by the product of
three face states for each continuous coordinate and the numerical label
count for each integer coordinate. Enumeration may be expensive on a draw
with a large component; the theorem does not hide that expense.

The singular-Hessian argument is valid. After fixing an optimal integer
assignment, choose an optimal continuous point with the fewest strictly
interior coordinates. On its free face, the gradient vanishes and the
restricted Hessian is positive semidefinite. A nonzero vector in its kernel
would preserve the quadratic value on a line. Since the box is bounded,
following this line reaches an additional bound while keeping feasibility
and optimality. This contradicts the chosen minimum free-coordinate count.
Hence some global optimizer lies on a face with nonsingular free Hessian,
or at a vertex. Both cases are enumerated.

Singular configurations can therefore be skipped without losing every
optimizer, even when the global optimal set has positive dimension. Keeping
other feasible stationary candidates without checking their KKT signs is
sound: feasible saddles cannot beat the true global minimum. The proof
requires exhaustive face and integer-label enumeration, not a local search.

Rational stationary systems have dimension at most the input dimension.
All substituted integer labels and bounds have polynomial bit length, even
when their number is large. Determinant bounds therefore give polynomial
candidate and objective-value bit lengths in \(I+\log M\), with an absolute
polynomial exponent. This includes nonoptimal candidates. Singular-system
detection and each successful rational solve have the same polynomial
per-configuration bound. Combining component outputs also preserves
polynomial encoding length. Exact rational output on every draw is justified.

## 3. Connected-set counting and expected work

The rooted ordered spanning-tree encoding proves the claimed upper bound
\((4\Delta)^{k-1}\) for connected sets of size \(k\) containing a fixed
vertex. A canonical spanning tree maps distinct vertex sets to distinct
encoded trees. Counting all ordered tree shapes and allowing repeated
neighbor labels only increases the bound.

For a connected set \(S\), being an entire bad component implies that all
its vertices are bad. Dropping conditions on its exterior and using the
original independent events bounds that probability by \(\prod_{i\in S}q_i\).
Multiplying by its enumeration cost gives the weight
\(\prod_{i\in S}a_iq_i\). Rooting and deliberately overcounting connected
sets gives

\[
\mathbb E\sum_C\prod_{i\in C}a_i
\le\frac{\sum_i a_iq_i}{1-4\Delta\beta}.
\]

The per-configuration polynomial factor can be bounded uniformly by the
whole input length. Preprocessing, sampling, direct isolated-variable
optimization, and graph traversal add polynomial work. These observations
prove the stated expected bound without an exceptional branch or resampling.

Large native-integer widths are paid for by the \(a_i\) weights inside
the probability condition. They are not silently treated as unary input,
nor eliminated by a bit-length argument. This scope is explicit in the note.

## 4. Certificates and limits

The derivative intervals, pinned bounds, bad-component partition, and
complete component enumeration form a direct global proof record. A
verifier can repeat the exhaustive finite checks within the same realized
work bound. Its soundness does not use the probability condition. The
returned optimizer and value have polynomial length on every draw, while
the proof record and discovery work can be large on individual draws.

The result addresses the sampled objective under a material strong-field
condition. It is not a treewidth-free theorem for arbitrary noise strengths
or a certificate of exact unperturbed optimization. General coupled
constraints are excluded. The caution about polynomial objectives is also
correct: exponentially decaying component tails do not generally pay for
an arbitrary \(2^{\operatorname{poly}(k)}\) component fallback.

## 5. Clarification and verification

The opening draft called \(H\) a rational quadratic matrix without
explicitly stating symmetry. I requested \(H=H^\top\), or preliminary
symmetrization, because the derivative formula, interaction graph, and
PSD/nullspace argument use the symmetric Hessian. This is a conventional
model clarification; replacing \(H\) by \((H+H^\top)/2\) preserves the
objective and has polynomial cost. The author added the convention, and I
checked it in the revised file.

I also requested that \(I\) count the original input and any required
preprocessing/substitution data, rather than only a potentially much smaller
instance after fixed-coordinate elimination. Reading the original input
and reinserting fixed output coordinates require that convention. This
does not change the component or probability argument. The author added
the original-input and reinsertion accounting, and I checked the final
wording.

An independent inline `python3` check exhaustively enumerated the Bernoulli
bad sets for eight weighted-component fixtures on an edge, a path, a star,
and a cycle. It checked the exact expected component enumeration cost
against both the connected-set sum and the displayed geometric bound.
Four fixtures included an 81-bit native-integer label count. All passed.
These finite checks supplement the general proof and do not implement the
optimization algorithm.

I read the author's persistent exact checker and ran

```text
python3 -B research-20261002/new-direction/check_strong_field_components.py
```

It passed 324 exact comparisons of component optimization with full-instance
enumeration, 96 weighted bad-site patterns, three expected-cost bounds, and
two known-value singular-Hessian fixtures. The component and whole-instance
checks reuse one enumerator, so their agreement tests persistence and
separation rather than independently proving the enumeration algorithm.
The note correctly states this limitation. The singular cases and the
minimum-free-face proof provide distinct support for degeneracy handling.

A final inline `python3` document check passed local links, trailing
whitespace, paired mathematical delimiters, and sequential equation tags
in the theorem note and review.

No project-wide verification, CI inspection, or external literature search
was performed. The separately requested primary-source assessment is
outside this review.
