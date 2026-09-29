# Targeted verification of sparse kernel rounding

Date: 2026-09-28.

The core theorem is in [sparse-kernel-rounding.md](sparse-kernel-rounding.md).
The targeted command actually run was:

```sh
python research-20260928/solver/check_sparse_kernel.py
```

It completed successfully and printed:

```text
PASS: 2967 rational kernel checks; 189 separator/density checks; parity counterexample.
```

All arithmetic in this script uses Python `Fraction`. For kernel parameters
`m=2,...,24`, it checks the exact normalization coefficient, the adjacent
Fourier coefficient difference, coefficient positivity, the damping bound
including frequencies above the kernel degree, and kernel nonnegativity at
25 rational point pairs for each parameter.

For hierarchy orders `r=2,...,8`, the script constructs two distinct rational
probability measures on the separator using alternating binomial weights.
Their moments agree through degree `2r`, while the next Chebyshev moments
differ. It checks that the transformed separator density coefficients agree
exactly, and checks nonnegativity of the transformed two-variable bag
densities at 16 rational point pairs per order. The bags use different leaf
maps, so this is not a test of identical local measures.

The final check verifies a warning supplied by an independent reviewer.
The order-one pseudoexpectation with moment matrix

\[
 \begin{pmatrix}1&1/2&1/2\\1/2&1&-1/2\\1/2&-1/2&1\end{pmatrix}
\]

is positive semidefinite and its two box-generator expectations are zero,
but it evaluates `(1-x)(1-y)` to `-1/2`. Thus the raw total degree of a
positive tensor polynomial does not suffice to establish positivity under
a truncated box preordering. The theorem's even univariate kernel degree
and interval-certificate degree accounting are necessary safeguards.

These finite computations check implementation-level algebra and selected
boundary examples. They do not establish the general theorem, global kernel
positivity, the interval positivity representation, junction-tree gluing,
SDP Slater duality, or priority. Those parts require the written proof and
independent mathematical review. No project-wide verification or CI
inspection was performed.
