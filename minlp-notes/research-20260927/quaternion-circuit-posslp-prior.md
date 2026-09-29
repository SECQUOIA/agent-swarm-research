# Primary-source comparison for rational quaternion circuit signs

Date: 2026-09-28. Status: initial scoped audit by the root, followed by
an [independent primary-source audit](quaternion-circuit-posslp-prior-review.md).
The independent audit corrected the discussion of shared representations
in Dawson--Nielsen. Publication priority is unestablished. Mathematical
proof review is separate from this literature comparison.

The research target is exact comparison of a specified coordinate of a
unit rational quaternion represented by a shared multiplication and
inversion circuit. The now independently reviewed
[application](rational-optimizer-posslp-coordinate-comparison.md) realizes
the entire bounded rational circuit as the unique minimizer of a short
strongly SOS-convex quartic. It strengthens the existing coordinate
lower bound by promising a rational optimizer. It does not prove the same promise
for the minimum-value lower bound: perturbing the objective can change
the optimizer's rationality.

## Matrix circuits and compressed group words

[König and Lohrey, *Evaluating Matrix Circuits*, arXiv:1502.03540v1](https://arxiv.org/pdf/1502.03540v1),
Section 5 and Theorems 5--6, give a coRP bound for the compressed
identity problem of every fixed finitely generated linear group and
polynomial-time equivalence between polynomial identity testing over
the integers and the compressed word problem for
\(\mathrm{SL}_3(\mathbb Z)\). The paper attributes those statements
to Lohrey's earlier monograph and the lower construction to
Ben-Or--Cleve. Its circuit definition uses generator leaves and binary
group products; the represented word can have exponential length.

This is close representation-level prior, but its predicate is equality
with the identity, not the sign of one real matrix entry. Its
\(\mathrm{SL}_3(\mathbb Z)\) lower construction also does not
preserve a compact group or bounded entries. A polynomial-time
compressed identity algorithm for a subgroup would therefore not, by
itself, settle the proposed sign problem. The root read the definitions,
theorem statements, and their surrounding discussion; it did not
rederive the earlier monograph's reductions.

[Ben-Or and Cleve, *Computing Algebraic Formulas Using a Constant
Number of Registers*, SIAM Journal on Computing 21 (1992), 54--58](https://doi.org/10.1137/0221006),
proves that polynomial-size algebraic formulas over arbitrary rings
can be computed by polynomial-length programs with three registers,
using linear invertible updates. The primary publisher abstract was
read; the full proof has not yet been inspected in this audit. It is
important algebraic-simulation prior. The abstract does not impose
orthogonality or bounded intermediate values. Formula size, an explicit
product sequence, and a shared circuit are also different input models.

## Near-identity commutators are established algorithmic tools

[Dawson and Nielsen, *The Solovay--Kitaev Algorithm*,
arXiv:quant-ph/0505030v2](https://arxiv.org/pdf/quant-ph/0505030v2),
Sections 4.1--4.2, uses balanced commutators in \(\mathrm{SU}(2)\)
and quantitative cancellation of approximation errors. Section 4.1
derives the quadratic small-angle behavior of a commutator of rotations
around two perpendicular axes. Lemma 1 in Section 4.2 bounds the
commutator error when both factors are near the identity. The root read
these sections and the displayed error bound.

Thus using commutators to multiply small signals, or exploiting their
error cancellation, is not a new general technique. The source concerns
approximation of a requested unitary. Its Section 3 runtime analysis
already uses pointers to prior outputs and avoids expanding repeated
inverse subwords; shared representation is therefore also established
prior. The candidate here requires an exact sign reduction, rational
intermediate coordinates, and polynomial circuit size while controlling
errors below a potentially doubly exponentially small nonzero signal.
Those extra requirements must be proved; the approximation theorem does
not supply them directly.

## Elementary upper bound and the unresolved lower direction

For a fixed quaternion dimension and explicit rational input generators,
each multiplication appends a constant number of rational arithmetic
gates for its four coordinates. The inverse of a unit quaternion is
its conjugate. Maintaining positive-denominator numerator/denominator
circuits therefore reduces any specified coordinate sign to one
PosSLP instance in polynomial time. This elementary upper bound does
not establish the lower bound.

The lower construction must establish all of the following:
uniform control of unwanted vector components; exact vanishing needed
at zero inputs; cancellation-safe addition and multiplication; a tiny
positive rational signal obtained by a polynomial-size circuit; and
the final integer-gap comparison. The quartic realization is a separate
proof obligation. The linked construction notes now record fresh proof
reviews of these steps. None is certified merely by this literature
search or a finite numerical experiment.

## Search record and remaining work

Queries combined `PosSLP`, `quaternion`, `unitary`, `orthogonal`,
`compact groups`, `compressed word`, `matrix entry sign`, and
`arithmetic circuits`. Many hits concerned unrelated word embeddings
or quantum bit arithmetic. The primary texts above were selected after
checking the actual input and predicate definitions.

Two misleading search leads were also checked against arXiv records.
[arXiv:2412.16612](https://arxiv.org/abs/2412.16612) concerns vector
addition systems; its use of the abbreviation SLPS is unrelated to
unitary matrix straight-line programs.
[arXiv:2603.29427](https://arxiv.org/abs/2603.29427) is an introduction
to computation over the reals; its abstract does not announce a new
classification resolving PosSLP. These records were checked only to
discard the search leads, not used as theorem dependencies.

This is not an exhaustive novelty audit. The full Ben-Or--Cleve proof,
ordered matrix-group problems, compressed rotation comparison, and
related exact quantum-circuit predicates remain useful search targets.
No equivalent restricted theorem was identified in the inspected
passages; that does not establish that no such theorem exists.
