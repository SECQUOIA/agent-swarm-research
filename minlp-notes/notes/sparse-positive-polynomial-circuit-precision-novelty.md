# Sparse positive-polynomial circuits: source assessment

Date: 2026-09-05. Bounded primary-source novelty audit of
`sparse-positive-polynomial-circuit-precision.md`; the full candidate was read.
Independent proof audits are separate.

The extension has a clear scope improvement: polynomial rational formulation
size in the sparse encoding, including binary exponent lengths, with the same
additive `O(r+sum_i log log(D_i+2))` integer-count comparison against arbitrary
convex lifts. The lower bound and layer geometry are unchanged from the
reviewed dense theorem. The new construction replaces numerical-degree
recurrences by rounded endpoint computation and Boolean circuit compilation.
No matching whole-formulation theorem was found in this bounded search.

## Closest sources and precise limits

The [compiled-knot audit](compiled-rational-knot-formulations-novelty.md)
documents the exact Boolean gate antecedent: Avis, Bremner, Tiwary and
Watanabe, [§3, Lemma 1](https://arxiv.org/pdf/1408.0807), credited there to
Valiant (1982), and the explicit bounded-computation compiler in
[Avis and Bremner's Sparktope](https://arxiv.org/pdf/2005.02853), §§2–4.
The internal continuous wires acquire Boolean values from the declared input
bits. That mechanism and its polynomial construction are established.

The same audit checks Filos-Ratsikas et al., STOC 2024,
[full manuscript §3.4](https://www.pure.ed.ac.uk/ws/portalfiles/portal/413786593/PPAD-Membership_FILOS-RATSIKAS_DOA08022024_AFV_CC_BY.pdf),
for interpolation of circuit-specified neighboring values and multiplication
of real variables by computed output bits. Their fixed-point pseudo-circuit
model differs from an exact MILP, but is direct conceptual prior.

A further direct MIP predecessor found during this search is Adams and Henry,
*Base-2 Expansions for Linearizing Products of Functions of Discrete
Variables*, Operations Research 60(6), 1477–1490 (2012),
[full primary manuscript](https://www.osti.gov/servlets/purl/1648449), §2.
They represent an arbitrary function on an `n`-point domain and its product
with a nonnegative variable using `ceil(log2 n)` binaries and `n` continuous
selectors. The binary count is logarithmic; generic total size still depends
on the number of listed values. This distinction explains why the candidate
uses computed endpoint bits instead of an explicit endpoint table.

The [dense loglog-degree source audit](positive-polynomial-loglog-degree-novelty.md)
records geometric interpolation, logarithmic disjunction encodings, log-utility
supporting scalarization, and polynomial disaggregation predecessors. In
particular, dyadic layers and shared index bits are not independent novelty
claims. The present extension leaves that attribution intact.

## What should be claimed

The candidate computes each listed monomial at exact dyadic input endpoints
using fixed-precision binary exponentiation. It therefore processes only
listed exponents and never constructs exact huge-power numerators. Combining
this with a certified interpolation band and the previous universal lower
bound yields the proposed sparse-input theorem. Rounded exponentiation is
standard arithmetic; its error and bit-length accounting are supporting proof
details, not a claim to a new numerical algorithm.

The statement concerns nonnegative coefficients in the original separable
monomial basis, unconditional output error bodies, and exponents at least
two. It does not extend to arbitrary sparse polynomials or merely positive
polynomials on the box. The double-logarithmic term is an upper-construction
overhead; no matching degree-dependent lower bound has been established.

The formulation need not be ideal or practically small, and a polynomial
construction does not imply polynomial-time solution of the MILP. The
defensible contribution is the sparse-input compact realization of the
existing near-minimum integer-count guarantee. Priority remains qualified:
the checked sources contain the component techniques, but no exact theorem
with this combined approximation model and integer-dimension comparison was
located.
