This package formalizes the disproof of the uniform-constant conjecture for
positive multilinear relaxation gaps. The original statement is Conjecture 1
on page 22 of the [Luedtke–Namazifar–Linderoth author manuscript](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf).
The analytic construction is in the [result note](../../../results/positive-multilinear-gap.md)
and [Section 2 of the manuscript](../../../paper-relaxation-limits/sections/02-universal-positive.tex).

The main declarations are in
[`Results.lean`](../../Formal/MultilinearGap/Results.lean):

- `unbounded_gap_ratio`: for every real constant C, an explicit family member
  has positive convex-hull gap and term-by-term/hull gap ratio greater than C.
- `no_uniform_positive_multilinear_bound`: no constant bounds these gaps even
  for the subclass with coefficient one on every distinct squarefree support,
  on finite-dimensional unit cubes.

The gaps are the actual vertical widths of continuous graph convex hulls.
The term-by-term gap sums those widths for the individual monomials. The
existing `CubicGap` finite-law bridge is reused; the proof is not restricted
to sampled points or a relaxation of the graph hull.

For L ≥ 2 the construction has 2^L leaf variables and L anchors. Level j,
indexed from 1 through L, partitions the leaves into 2^j equal blocks and
includes the product of each block with its anchor. The anchor means are
2^(-j), and every leaf mean is 1−2^(-L). Supports are distinct, every
coefficient is one, and every coordinate mean is strictly inside the cube.

The verified estimates are

```
T_L = L,
0 < H_L ≤ s + 2 L / 2^s       for every natural s.
```

Here T is the term-by-term gap and H is the convex-hull gap. For any joint
binary law with the prescribed means, the expected number of failed leaves
is one. Partition sums and a finite geometric bound control the total
deficiency. A two-point law of cube points attains the upper envelope L.
Each individual monomial has an explicit zero-valued attaining law for its
lower envelope. The graph value at the prescribed means is strictly below L,
which establishes H > 0.

Taking L = 2^(2k) and s = 2k gives H ≤ 2k+2, while
L ≥ (k+1)^2. An Archimedean argument then exceeds every proposed constant.
This proof uses finite sums and elementary arithmetic, without logarithms,
quantile rearrangement, integration, or the exact hull-gap formula.

The [coverage table](COVERAGE.md) states the exact scope. The sharp
degree/dimension growth theorem and exact dyadic hull formula remain outside
this package. A unit-cube counterexample already refutes the conjecture on
all nonnegative boxes, so no general-box transfer theorem is needed here.

The [verification record](VERIFICATION.md) gives the checks and the
[review record](REVIEW.md) records two independent agent reviews. These
reviews concern mathematical specification and implementation; they do not
establish publication priority or constitute journal peer review.

To reproduce the build, audit, and kernel replay for this extension, run
from `formal/` with the pinned Elan toolchain on PATH:

```bash
python3 scripts/check_imports.py
lake build Formal --wfail
lake env lean Verify.lean
LEAN_NUM_THREADS=1 lake env leanchecker -v Formal.MultilinearGap
```

The build reuses unchanged dependencies. Kernel replay here targets the nine
new modules, with previously compiled imports as its dependency base. The
existing complete-project script also includes this package through the
explicit imports in `Formal.lean`.
