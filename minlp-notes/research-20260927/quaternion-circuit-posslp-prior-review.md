# Independent prior and significance audit: quaternion circuit signs

Date: 2026-09-28. Reviewer: `/root/quaternion_final_prior`, with a separate
search by `/root/quaternion_final_prior/compact_group_sign_search` and its
quantum-threshold reviewer. Status: scoped literature audit complete.
Publication priority is unestablished. This audit does not replace the
independent mathematical reviews of the reduction and quartic realization.

The proposed contribution is a polynomial-time many-one reduction from
PosSLP to the nonzero sign of one coordinate of a shared circuit over a
fixed finite set of rational unit quaternions. The circuit uses only
multiplication and inversion. The separate realization theorem would
transfer this lower bound to a coordinate of a bounded, rational, unique
minimizer of a rational strongly SOS-convex quartic with a short full
positive definite Hessian Gram.

The two inspected manuscripts are
[the sign reduction](quaternion-circuit-posslp-reduction.md) and
[the realization](unit-quaternion-circuit-quartic-realization.md).
The strongest nearby sources examined below establish substantial parts
of the general methodology. None of the inspected statements gives this
complete restricted sign theorem. That finding supports a carefully
qualified comparison, not a priority claim.

## Compressed identity and matrix simulation

[König and Lohrey, *Evaluating Matrix Circuits*, arXiv:1502.03540v1](https://arxiv.org/pdf/1502.03540v1),
Section 5, defines shared multiplication circuits over fixed generators
and inverse generators. The predicate is equality to the group identity.
Theorems 5--6 state a coRP upper bound for every finitely generated linear
group and polynomial-time equivalence of the compressed word problem for
\(\mathrm{SL}_3(\mathbb Z)\) with integer polynomial identity testing.
The source attributes the proofs to Lohrey's monograph, Theorems
4.15--4.16, and the lower construction to Ben-Or--Cleve. The inspected
arXiv version presents those statements, not their full proofs.

This is direct prior for shared group circuits and arithmetic simulation.
The predicate is identity rather than real order, and the hardness group
is noncompact. Inversion of an arbitrary DAG output does not produce an
essentially different representation: storing an inverse companion for
each gate reverses product order with only linear overhead. Consequently,
the proposed distinction should rest on compact rational values and exact
coordinate sign, not on allowing inversion gates. The old identity upper
bound also applies to the fixed quaternion-generated group through its
rational matrix representation.

[Ben-Or and Cleve, *Computing Algebraic Formulas Using a Constant Number
of Registers*, SIAM J. Comput. 21 (1992), 54--58](https://doi.org/10.1137/0221006),
establishes three-register simulation of polynomial-size algebraic
formulas over arbitrary rings by polynomial-length programs with linear
invertible updates. The publisher abstract also gives algebraic
\(NC^1\)-completeness of iterated \(3\times3\) matrix multiplication.
The abstract was read independently. The publisher did not expose the
full proof, an indexed volume mirror could not be retrieved, and
[Cleve's author bibliography](https://cs.uwaterloo.ca/~cleve/papers.html)
does not link this paper's full text. Thus this audit does not claim a
full-proof comparison. Formula simulation alone does not supply the
candidate's compact rational DAG sign construction; König--Lohrey is the
closer representation-level reference.

## Commutators and shared approximation

[Dawson and Nielsen, *The Solovay--Kitaev Algorithm*, arXiv:quant-ph/0505030v2](https://arxiv.org/pdf/quant-ph/0505030v2),
Sections 4.1--4.2, establishes quadratic small-angle commutator behavior
and cancellation in perturbed near-identity factors. Section 3, printed
page 7, explicitly uses pointers to earlier outputs and avoids expanding
inverse subwords. This corrects the initial note's overly narrow
description as an explicit-sequence method. Shared reuse and commutator
cancellation are both prior art.

The source solves unitary approximation, not exact order of a succinct
rational coordinate. Its runtime is polynomial in the requested number
of accuracy bits; that bound alone is insufficient when resolving an
exponentially long accuracy request. The proposed reduction instead
controls signs using a short exactly rational signal circuit. The source
passages and Lemma 1's proof were read directly.

## Boolean group arithmetic and quantum thresholds

[Joye, *Boolean Arithmetic over \(\mathbb F_2\) from Group Commutators*,
WAIFI 2026](https://marcjoye.github.io/papers/Joy26homenc.pdf),
Sections 2--4, gives exact Boolean arithmetic using group multiplication
and inversion, including concrete commutator constructions in \(A_5\)
and \(A_6\). The definitions and constructions were read directly from
the author's paper. This is recent, explicit prior for compiling
arithmetic operations into intrinsic group operations. Its encoded ring
is the two-element field and the groups are finite. Finite-group circuit
evaluation can be performed gate by gate with constant-size group
elements; it does not establish the candidate's integer-sign hardness
inside an infinite compact rational group. The candidate is also not an
exact homomorphic encoding of every intermediate integer into a fixed
pair of group elements: it uses order-dependent leading coefficients and
controlled errors.

[Beaudry, Fernandez, and Holzer, *A common algebraic description for
probabilistic and quantum computations*, arXiv:quant-ph/0212096v1](https://arxiv.org/pdf/quant-ph/0212096v1),
Definitions 3.2--3.5, studies norm-preserving tensor formulas and a
partial-trace threshold. Theorem 5.2 gives BQP-completeness with a
probability-gap promise; the following paragraph states PP-completeness
without that promise. The inspected input is a formula tree with tensor
products, and Lemma 4.1 uses matrices of dimension \(2^n\). These are
important exact and approximate threshold precedents, but the growing
dimension, tensor operations, and partial-trace predicate differ from
one coordinate of a fixed-dimensional quaternion multiplication DAG.
The subsidiary search identified this source; this reviewer rechecked
the definitions, theorem, adjacent paragraph, and dimension statement.

## Significance and claim boundaries

If both mathematical proofs pass their separate audits, the strongest
MINLP consequence is that a rational optimizer promise does not remove
the PosSLP barrier for exact coordinate comparison, even with bounded
optimizer coordinates, global strong convexity, a short rational SOS
expression, and a supplied short Hessian certificate. This strengthens
the existing irrational-root coordinate construction. It concerns
exact decision complexity, independently of an algorithm's obligation
to print expanded optimizer fractions.

This would not show hardness of ordinary approximation with a prescribed
tolerance, numerical instability at all useful tolerances, NP-hardness,
or a separation between P and PosSLP. The signal can be extremely close
to zero. It would not prove that a subsequently perturbed quartic used
for minimum-value comparison still has a rational minimizer. The
realization itself keeps minimum zero, so its value does not encode the
sign.

The construction could provide controlled theoretical test families for
exact optimization and certificate arithmetic. Solver improvements or
important application gains remain prospective; none follows from the
hardness classification alone. The result's potential importance is a
sharp boundary between geometric regularity, rationality, and exact
arithmetic complexity, rather than an immediate speedup.

## Search scope and verification record

Searches used literal PosSLP combinations with quaternion, SU(2), SO(3),
unitary, orthogonal, compact group, and rotation, together with matrix
circuit sign, compressed word, straight-line program, succinct unitary,
and quantum threshold terminology. Separate agents repeated part of this
search. No matching restricted theorem was located in the sources
examined. Search engines returned many unrelated or misleading matches;
an unsuccessful search cannot establish novelty.

The accessible version-specific König--Lohrey statements and the other
primary passages above were inspected. The old author URL for Lohrey's
monograph currently redirects to a university home page; its full proof
was not read in this audit. That limitation and the unavailable full
Ben-Or--Cleve proof remain explicit. No external messages, purchases,
project-wide checks, or numerical proof validation were performed for
this literature audit.

Targeted checks: an inline `python3 -` check on this file and the initial
prior note passed for three local links, paired math delimiters,
whitespace, control characters, and final newlines.
`git diff --check -- research-20260927/quaternion-circuit-posslp-prior.md research-20260927/quaternion-circuit-posslp-prior-review.md`
passed. These are local document checks; they make no claim about CI or
mathematical correctness.
