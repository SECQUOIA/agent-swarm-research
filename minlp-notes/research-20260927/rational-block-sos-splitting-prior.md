# Prior results on rational SOS and prescribed block separation

Date: 2026-09-28. This is a targeted literature audit for
[the block-separation construction](rational-block-sos-splitting-obstruction.md).
It is not an independent proof review. Publication priority remains
unestablished.

The proposed contribution concerns the cost of imposing a prescribed
variable partition on a certificate that already has a short unrestricted
rational SOS. Three established subjects are close but distinct: real SOS
splitting, support-based SDP reductions, and rational descent of SOS.
None of the inspected statements below establishes the proposed combination.
That comparison and an unsuccessful search do not prove novelty.

## 1. The exact real splitting question already appears in 2004

Kojima, Kim, and Waki, *Sparsity in Sums of Squares of Polynomials*,
Research Report B-391, June 2003, revised July 2004; subsequently
*Mathematical Programming* 103 (2005), 45–62,
[author-uploaded report](https://www.researchgate.net/publication/2477507_Sparsity_in_Sums_of_Squares_of_Polynomials),
[DOI](https://doi.org/10.1007/s10107-004-0554-3).

Printed report page 16 defines separability as
\(F=\sum_i f_i(x^i)\), with disjoint vector-variable blocks.
It conjectures that if \(F\) is SOS in the joint variables, then it
has an SOS whose square factors each use one block. It reports that
this holds when \(F\) attains minimum zero. The assertion concerns
real coefficients; it supplies no rational descent or coefficient-size
claim. In particular, the proposed zero-minimum example does not refute
that reported real result.

The author-uploaded full text and an independently indexed copy of the
same concluding paragraph were examined. This audit did not locate a
later primary source that explicitly resolves the general disjoint-block
real conjecture. Do not describe it as still open on this evidence. A
tensor-moment argument suggested in the current research is a proof task,
not evidence of publication priority or a substitute for this missing
literature attribution.

## 2. Support partitions can preserve rational certificates

Dai and Xia, *Smaller SDP for SOS Decomposition*, *Journal of Global
Optimization* 63 (2015), 343–361,
[primary preprint](https://arxiv.org/pdf/1407.2679),
[DOI](https://doi.org/10.1007/s10898-015-0300-9).

Theorem 2 treats support covered by pairwise disjoint faces of the
Newton polytope. Definition 8 and Theorem 4 extend this to their
combinatorially defined split polynomials: an SOS exists exactly when
each prescribed coefficient projection is SOS. These projections partition
the polynomial's support. They are not arbitrary decompositions of the
form \(f(x)+t\), \(g(y)-t\), with a shared constant to be chosen.
Theorem 3's proof constructs block square factors by deleting monomials
from the original square factors. Thus, when its hypotheses hold and the
supplied rational SOS already has every square factor supported in the
chosen set \(Q\), that proof preserves rational coefficients. The
condition SOSS alone asserts existence of a real representation on \(Q\);
it does not justify moving a rational representation onto \(Q\).
This arithmetic observation follows directly
from the proof; the paper does not state the proposed bit lower bound.

Li and Xia, *Block SOS Decomposition*,
[primary preprint, arXiv:1801.07954v2](https://arxiv.org/pdf/1801.07954),
Definition 2 and Section 2.3.

Their block SOS supports \(Q_i\) are pairwise disjoint sets of
monomial exponents. The definition requires the reduction for every
real SOS with the given support. Propositions 7 and 12 place split
polynomials and minimal coordinate projections within that framework.
Theorem 22 proves a measure-zero statement in the full space of SOS
polynomials. It is not a statement about coefficient bit complexity,
nor about the relative size of a fixed separable subspace. The ordinary
degree-two bases for two disjoint variable blocks both contain the
constant monomial, so those two bases do not themselves meet the
definition's disjointness requirement. Another valid support partition
would have to be justified separately.

Permenter and Parrilo, *Finding Sparse, Equivalent SDPs Using Minimal
Coordinate Projections*, CDC 2015, 7274–7279,
[DOI](https://doi.org/10.1109/CDC.2015.7403367).
The indexed [author PDF](https://www.mit.edu/~fperment/pdf/invariant.pdf)
could not be fetched during this audit. Its abstract was examined, and
the precise projection definition and proposition were checked as
reproduced in Li–Xia, Section 2.3. This access limitation matters when
attributing the original theorem.

The relevant condition is a coordinate projection that preserves PSD,
the affine feasible set, and the objective. Such a projection deletes
entries using a zero-one mask. Here is the elementary arithmetic
consequence, independent of any novelty claim: applying it to a rational
feasible Gram leaves every retained entry unchanged, so it preserves
rationality and cannot increase the retained entry bit lengths. An
obstruction to rational block splitting therefore cannot arise from a
valid projection of this kind onto the requested separated Grams.

Explicitly, if \(P(Q)=M\circ Q\), \(M\) is a zero-one mask,
\(P(\mathbb S_+)\subseteq\mathbb S_+\), and
\(P(\mathcal A)\subseteq\mathcal A\) for the affine Gram
constraints \(\mathcal A\), then rational
\(Q\in\mathcal A\cap\mathbb S_+\) maps to a rational
feasible Gram. Every entry is either zero or the same entry of \(Q\).
An objective-preservation condition is needed when comparing optima.
Existence of some real block decomposition by itself supplies none of
these projection properties. Duplicating the constant monomial in two
local bases changes the representation; it must not be silently identified
with entry deletion in a basis containing one copy of each monomial.

## 3. Sparse Positivstellensätze and sparse relaxation bounds

Grimm, Netzer, and Schweighofer, *A Note on the Representation of
Positive Polynomials with Structured Sparsity*, *Archiv der Mathematik*
89 (2007), 399–403,
[primary preprint](https://arxiv.org/pdf/math/0611498).

Corollary 5 assumes the running intersection property and archimedean
quadratic modules on the variable blocks. Every polynomial that is
strictly positive on the associated feasible set and is a sum of block
polynomials belongs to the sum of those modules. Lemma 3 first splits
a positive polynomial on a compact box into positive block polynomials,
using polynomial corrections on overlaps. These are real, constrained
representation statements, with no fixed quartic degree or rational
coefficient-size bound. They do not imply that a given unconstrained
quartic SOS has a short rational SOS respecting a prescribed partition.
The paper explicitly attributes the compact sparse representation result
to Lasserre and its extension to Kojima–Muramatsu.

Nie and Demmel, *Sparse SOS Relaxations for Minimizing Functions That
Are Summations of Small Polynomials*,
[primary preprint](https://arxiv.org/pdf/math/0606476).

Theorem 3.1 orders the sparse SOS, dense SOS, and true optimization
bounds. Example 3.5 shows that the sparse bound can be weaker. Theorem
3.3 states a conditional equality result involving the running
intersection property and representing measures for the block moment
matrices. These results compare real relaxation values and allow
overlapping blocks. They do not establish an arithmetic gap between
existing rational certificates at the same real value. The current
construction's real block certificates should therefore be stated
explicitly, so its arithmetic obstruction is not confused with a known
loss in real relaxation strength.

## 4. Rational descent is the necessary arithmetic comparison

Scheiderer, *Sums of Squares of Polynomials with Rational Coefficients*,
*Journal of the European Mathematical Society* 18 (2016), 1495–1513,
[primary published article](https://ems.press/content/serial-article-files/32129).

This work constructs rational homogeneous polynomials that are SOS
over the reals but not over the rationals, settling Sturmfels' question
negatively. It characterizes the ternary quartic examples arising in
that setting and also studies degrees of denominators in rational-function
SOS representations. The latter concerns polynomial denominator degree,
not binary length of rational scalar coefficients. Rational nonexistence
by itself is therefore established prior art. The proposed added feature
is embedding a rational non-SOS block in a short rational joint SOS of
the form \(f(x)+g(y,z)\), and then quantifying the cost of enforcing
that separation after a positive perturbation.

Hillar, *Sums of Squares over Totally Real Fields Are Rational Sums of
Squares*, *Proceedings of the American Mathematical Society* 137 (2009),
921–930, [primary preprint](https://arxiv.org/abs/0704.2824).
Rational polynomials admitting an SOS over a totally real number field
admit a rational SOS, constructively. This does not apply to an arbitrary
real embedding of a number field with nonreal conjugates. In particular,
\(\mathbb Q(2^{1/5^k})\) is not totally real.

Capco and Scheiderer, *Two Remarks on Sums of Squares with Rational
Coefficients*, [primary preprint](https://arxiv.org/pdf/1905.13282),
Introduction and Section 3.
The paper sharpens the earlier Galois construction and studies strictly
positive forms that might be real SOS without rational SOS. It distinguishes
strict positivity from interior membership in the SOS cone. The proposed
positive family is already rational SOS jointly and asserts rational
existence for separated certificates, so it does not resolve the paper's
strict-positive rational-existence question. Any claims about that question's
present status require checking subsequent work separately.

## 5. Existing coefficient-size results do not give this comparison

The sources and exact statements are documented in
[the Gram bit-size audit](gram-bit-size-prior.md) and
[the constrained-SOS audit](gram-bit-size-constrained-sos-prior-review.md).
The most relevant distinctions are:

- O'Donnell's [ITCS 2017 example](https://drops.dagstuhl.de/storage/00lipics/lipics-vol067-itcs2017/LIPIcs.ITCS.2017.59/LIPIcs.ITCS.2017.59.pdf)
  forces huge coefficients in degree-two constrained SOS proofs. It has
  a small higher-degree proof. The target and equality constraints are
  essential to the statement.
- Raghavendra–Weitz's [2017 lower bounds](https://arxiv.org/pdf/1702.05139)
  concern constrained proofs. In the non-Boolean repeated-squaring chain,
  the direct argument forces a large equality multiplier. It does not
  force a large ordinary polynomial Gram.
- Davis–Papp's [rational dual-certificate bounds](https://arxiv.org/pdf/2305.19039)
  depend on distance from the relevant weighted-SOS boundary and
  representation parameters. Such dependence is consistent with an
  arithmetic cost for a prescribed sparse representation.
- Gärtner–Magron–Vallentin's [2026 result](https://arxiv.org/html/2606.25118v1),
  Corollary 1.3, supplies polynomial-time exact rational Gram recovery
  when an ordinary Gram with a supplied positive eigenvalue margin is
  available; the margin's encoding counts. It is not a theorem that a
  prescribed block restriction preserves a short certificate.

The proposed family uses ordinary binary rational encoding. Its large
denominator conclusion must be transferred to an actual Gram entry or
the total coefficient length, not merely to an auxiliary constant that
a verifier need not print. The main note does that transfer explicitly.
It claims neither a lower bound for every certificate system nor an
exponential bound in the total input bit length.

## 6. Assessment and remaining literature work

The strongest defensible comparison is currently: the main note proposes
a constructive separation between unrestricted and prescribed-block
rational SOS, including rational nonexistence at a zero minimum and
existing but long rational certificates in a positive quartic family.
This is more specific than real sparse-versus-dense relaxation gaps,
ordinary rational descent failure, or coefficient lower bounds with
equality multipliers. The base construction does not claim convexity of
the joint polynomial. A subsequent
[strongly SOS-convex upgrade](strongly-sos-convex-block-splitting-obstruction.md)
proves both blocks can be made strongly SOS-convex, preserving the short
joint certificate and the rational splitting obstruction. Its fresh
independent mathematical review has passed; publication priority remains
unestablished. Its short joint SOS
Hessian certificate is distinct from a positive definite Gram on the full
joint Hessian basis, which additive block separation excludes.

Two primary SOS-convexity results delimit what that upgrade adds.
Helton and Nie, *Semidefinite Representation of Convex Sets*,
[primary preprint](https://arxiv.org/pdf/0705.4068), Lemmas 7–8,
printed pages 9–10, show that an SOS Hessian yields a real SOS for a
polynomial with zero value and zero gradient at a real point. The proof
integrates the Hessian along the segment from that point. A nonrational
base point does not become rational through that proof.
Ahmadi and Parrilo, *A Complete Characterization of the Gap between
Convexity and SOS-Convexity*,
[primary preprint](https://arxiv.org/pdf/1111.4587), Theorem 3.1,
equates the SOS Hessian condition with the real SOS property of the
first-order Taylor remainder in joint variables. These standard results
explain real SOS existence for the blocks and the starting Taylor identity.
Neither states a short rational certificate transfer to prescribed blocks.

The recent Naskar–Singh preprint
[*Convexity and SOS-Convexity of Sum of Separable and Biquadratic Quartic
Polynomials and Optimization*](https://arxiv.org/abs/2607.23476)
was also checked at its abstract and definition. It studies real convexity
versus SOS-convexity of separable-plus-biquadratic forms. Its separable
part is a sum of univariate forms, and the biquadratic part couples
variable groups. That class and question are different from the arithmetic
cost of certifying a sum of two multivariable blocks.

Its practical relevance is a warning about exact certification after
variable-block reduction. It does not show that sparsity is generally
harmful, or that numerical sparse optimization must be slower. A useful
next theory question is which rationally computable reductions preserve
short exact witnesses, with the coordinate projections above providing
one safe class.

Searches used the exact KKW title, its separability conjecture, disjoint
variables, additive block SOS, split polynomials, block SOS decomposition,
rational descent, rational sparse certificates, and coefficient bit
complexity. The audit also inspected neighboring material on tensor
separability, chordal polynomial-matrix decompositions, and SOS modulo
square-free monomial ideals. Those use different certificate identities
and are not treated as equivalent results. Searches returning no match
provide no proof of novelty. A broader citation-chain audit of the KKW
conjecture and arithmetic sparse-SOS literature remains necessary before
a publication-priority claim.

## Verification record

The source statements above were read at the specified locations, with
the Permenter–Parrilo access limitation recorded. The main construction
was read only to identify its assumptions and claims; this audit does
not certify its proof. No numerical computation or Lean formalization
was used. No project-wide verification or CI inspection was performed.

A second reader independently checked the KKW concluding paragraph,
Dai–Xia Theorem 3's projection proof and Definition 8/Theorem 4,
and the coordinate-projection definition and proposition reproduced in
Li–Xia. The rationality consequences above were checked with the explicit
supplied-support qualification. This is a scoped cross-check of those
claims, not an independent review of the whole literature audit.

A targeted inline Python document check passed: four local links,
balanced math delimiters, whitespace, control characters, and final
newline. This checks the document, not the mathematical assertions.
