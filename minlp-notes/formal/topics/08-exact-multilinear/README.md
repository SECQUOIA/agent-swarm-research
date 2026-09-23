This package verifies the exact finite hull gap and an attaining probability
law for the dyadic family used in the
[multilinear disproof](../07-multilinear-disproof/README.md). It formalizes the
exact-formula argument in the
[result note](../../../results/positive-multilinear-gap.md#exact-hull-gap-for-nested-dyadic-partitions)
and [manuscript](../../../paper-relaxation-limits/sections/02-universal-positive.tex).

For every integer L ≥ 2, define B(q) = (L−q+2)/2^q. The theorem
`exists_hullGap_exact` in
[`ExactResults.lean`](../../Formal/MultilinearGap/ExactResults.lean) proves that
there is an integer s with 1 ≤ s < L and B(s+1) ≤ 1 ≤ B(s), and that

```
H_L = s + (L−s)/2^s.
```

Here H_L is the vertical width of the original continuous graph convex hull
at the family's prescribed means. The previously verified termwise gap is
T_L = L. The proof identifies and attains both envelope endpoints: the upper
endpoint is L, and `polynomial_exact_minimum` gives the lower endpoint L−H_L.
The estimate holds for every feasible binary law, using the existing bridge
between such laws and the continuous graph hull.

The attaining law mixes two adjacent cutoff laws so that the expected number
of failed leaves is exactly one. In each cutoff state, the number of failed
leaves is zero or a power of two. For 2^r failures, the implementation chooses
a uniformly random residue class modulo 2^(L−r) as the failed leaves. This
periodic construction gives equal leaf marginals and hits as many blocks
as possible at every level simultaneously. It suffices for the cutoff laws;
the implementation does not need the note's more general bit-reversal and
XOR construction for arbitrary integer failure counts.

The package contains seven modules. The
[coverage table](COVERAGE.md) maps the arithmetic, geometry, attaining law,
and dual bound to their declarations. Sharp degree and dimension asymptotics
are proved in the separate [sharp-growth package](../09-sharp-multilinear/README.md).

To reproduce the endpoint build, run from `formal/` with the pinned Elan
toolchain on PATH:

```bash
lake build --wfail Formal.MultilinearGap.ExactResults
```

The [verification record](VERIFICATION.md) gives the project audit and kernel
replay commands, their scope, and their recorded results.
