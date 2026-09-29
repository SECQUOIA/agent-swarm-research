# Prior-art audit for algebraic certificates of convex quadratic optimization

Date: 2026-09-27. This is a literature comparison, not a proof review of the
proposed certificate theorem. The proposed refinement is still subject to its
separate mathematical review.

The certificate mechanisms are classical. Facial reduction followed by ordinary
duality already supplies exact certificates without Slater's condition. For
native convex quadratic inequalities, a positive aggregate proving infeasibility
is an explicit special case of an existing theorem of alternatives. The possible
addition here is a uniform bound on the degree and encoding of a common real
number field when the **linear span of the native constraint Hessian matrices**
has fixed dimension. A polynomial number of real certificate entries is not, by
itself, a polynomial binary certificate.

The parameter is

\[
h=\dim\operatorname{span}_{\mathbb Q}\{Q_1,\ldots,Q_m\},\qquad
q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i,\quad Q_i\succeq0.
\]

It does not count the objective Hessian, ambient variables, quadratic rows,
individual matrix ranks, or the dimension of the sum of their ranges. The
comparison below concerns rational input, affine additional constraints, and
exact certificates for the continuous problem. A certificate for one continuous
fiber does not certify global mixed-integer optimality.

## Closest theorem of alternatives

Jeyakumar and Li, *A new class of alternative theorems for SOS-convex inequalities
and robust optimization*, Applicable Analysis 94(1), 56–74 (2015; online 2013),
give the following qualification-free alternative in Theorem 2.5. For
SOS-convex polynomials \(f_i\) of degree at most \(d\), infeasibility of
\(f_i(x)\le0\) is equivalent to

\[
\sum_i\lambda_i f_i=\delta+\sigma,\qquad
\lambda\ge0,\quad \sum_i\lambda_i=1,\quad \delta>0,
\quad\sigma\text{ SOS},\quad\deg\sigma\le d.
\]

Convex quadratics are SOS-convex. Their Corollary 2.7 also characterizes failure
of strict feasibility by a simplex-weighted aggregate that is SOS, with no
positive constant required. The proof of Theorem 2.5 uses strong separation of
convex polynomial epigraph sets. Affine equalities can be expressed as two
inequalities. [Author manuscript, Theorem 2.5 and Corollary 2.7](https://web.maths.unsw.edu.au/~gyli/papers/jl-zero-sum-final-18-07-13.pdf),
[publication record](https://doi.org/10.1080/00036811.2013.859251).

The inspected theorem and proof concern real coefficients in the certificate.
They do not give rationality, number-field degree, coefficient-height, or binary
size bounds. The manuscript contains no discussion indexed by “rational” or
“complexity.” This text search supplements inspection of the theorem and its
proof; it does not establish an absence result about the surrounding literature.
Consequently, the positive-aggregate existence theorem must be credited to this
prior work, even if a different minimax proof is used locally.

## Exact duals and facial reduction

Ramana's *An exact duality theory for semidefinite programming and its complexity
implications* constructs an explicit extended SDP dual of polynomial formulation
size and coefficient encoding. For a feasible primal, finite value is equivalent
to extended-dual feasibility; in the finite case the values agree and the dual
attains its value. It also gives an exact alternative SDP for infeasibility. The
stated complexity consequences distinguish the Turing model from the
Blum–Shub–Smale real-arithmetic model. This does not assert that an arbitrary
feasible dual has a polynomial-length rational or algebraic solution.
[Author's DIMACS report abstract, 1995](https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/1995/95-02.html).
For the structural proof, the openly available sources below were inspected;
this audit did not inspect the complete original Ramana article.

Pataki, *Strong duality in conic linear programming: facial reduction and extended
duals*, presents the classical Borwein–Wolkowicz facial-reduction mechanism and
extends Ramana-type duals to nice cones. His Theorem 1 bounds reducing iterations
by \(\min\{\ell_K-1,\dim L\}\), where \(\ell_K\) is the longest face-chain
length and \(L=\ker(A,b)^*\). Reduction reaches the minimal cone and restores
relative strict feasibility. This is a dimension bound on reductions, not a
binary bound on their entries. The native-quadratic claim of at most \(h\)
curved reductions needs a separate argument that each step kills a nonzero
member of the restricted Hessian span. It is not a direct substitution into
Pataki's conic face-chain parameter.
[Primary manuscript, Sections 3–5, especially Theorem 1](https://optimization-online.org/wp-content/uploads/2013/02/3772.pdf).

Liu and Pataki, *Exact duals and short certificates of infeasibility and weak
infeasibility in conic linear programming*, give exact extended duals and
facial-reduction certificates for general closed convex cones. Theorem 1 bounds
strict sequence length, Theorem 2 gives the extended dual, and Theorem 4 gives
infeasibility and weak-infeasibility characterizations. For SDP, regularized
sequences yield particularly transparent certificates. Their earlier
*Exact duality in semidefinite programming based on elementary reformulations*
uses row operations and invertible congruences to produce readily checked
infeasible forms or feasible forms with strong duality for every objective.
These results preclude claiming novelty for a short sequence of exact facial
exposures followed by KKT or for an independent certificate verifier in real
arithmetic. They do not provide the proposed native-Hessian-span binary bound.
[General-conic primary manuscript](https://arxiv.org/pdf/1507.00290),
[SDP primary manuscript](https://arxiv.org/pdf/1406.7274).

Klep and Schweighofer supply an algebraic predecessor: their
*Infeasibility certificates for linear matrix inequalities* gives a
Positivstellensatz for infeasible pencils in Theorem 2.2.5 and a polynomial-size
SOS extended dual in Theorem 3.5.2. The latter certifies linear nonnegativity on a
spectrahedron, including degenerate cases, through auxiliary identities and
semidefinite conditions. Thus replacing facial-reduction language by polynomial
identities would not make the mechanism new. The relevant additional issue is
the degree and height of the numbers used in those identities, not merely their
polynomial degrees in the primal variables.
[Author manuscript](https://igorklep.github.io/files/infeasible-25aug11.pdf).

## Rational certificates require a separate argument

Naldi and Sinn, *Conic programming: infeasibility certificates and projective
geometry*, treat rationality explicitly in Section 3.2. Their Remark 3.6 gives a
rational separating certificate when both \(K\cap L\) and \((-K)\cap L\) are
stably infeasible. Example 3.8 constructs a strongly infeasible rational SDP
without a rational separating certificate in their specified sense, using a
Scheiderer example. Their Theorem 4.7 gives SDP feasibility in
\(\mathrm{NP}_{\mathbb R}\cap\mathrm{coNP}_{\mathbb R}\), explicitly in the
Blum–Shub–Smale model. These statements do not rule out more elaborate rational
proof objects, and they must not be restated as Turing-model NP membership.
[Published primary PDF, Section 3.2 and Theorem 4.7](https://www.unilim.fr/pages_perso/simone.naldi/papers/2018_naldi_sinn.pdf).

For the present native PSD-quadratic class, rational aggregate certificates are
plausible for a more specific reason. This is an elementary deduction to verify,
not a theorem attributed to the sources above. Fix the positive support \(I\)
of a real positive aggregate. Throughout the relative interior of that support,

\[
\ker\Bigl(\sum_{i\in I}\lambda_iQ_i\Bigr)
=\bigcap_{i\in I}\ker Q_i=:W.
\]

The space \(W\) is rational. Finiteness of the aggregate's minimum requires
\(\sum_i\lambda_i a_i\perp W\), a rational linear condition on \(\lambda\).
On the resulting support-preserving parameter set, the aggregate is positive
definite on \(W^\perp\), and its minimum varies continuously. Rational weights
sufficiently close to the original ones therefore preserve a strictly positive
minimum. This suggests a rational positive aggregate and rational PSD Gram
certificate. Arbitrary coordinatewise rounding would not suffice: it can break
the exact kernel-orthogonality equations and create an unbounded negative
direction. Existence by density gives no polynomial bit bound. A quantitative
version must control the positive support, curvature, margin, and the rational
affine parameterization used in rounding.

No explicit prior theorem giving this native-quadratic rationalization together
with a fixed-Hessian-span bit bound was found in the searches recorded below.
That is not a novelty claim. The rationalization argument is short enough that
it should be treated as a supporting lemma unless a broader consequence is
established.

## Algebraic solutions and existing exact algorithms

Nie and Ranestad, *Algebraic degree of polynomial optimization*, derive algebraic
degrees from complex critical systems under genericity assumptions. Section 3.1
gives the familiar QCQP count \(2^s\binom ns\) for \(s\) active quadratic
constraints, with sharpness in the generic regime. Their framework concerns
critical-point degree, not uniform coefficient height or a common-field facial
certificate for every singular convex instance. A small Hessian span is not
the same as a small active constraint count. Any comparison must state the
regularity or finiteness requirements, rather than claiming an improvement over
their sharp generic count.
[Primary manuscript, Section 2 and Section 3.1](https://arxiv.org/pdf/0802.1233).

Henrion, Naldi, and Safey El Din, *Exact algorithms for semidefinite programs
with degenerate feasible set*, use symbolic homotopy to remove assumptions on
the feasible spectrahedron. The inspected February 2018 author manuscript
retains genericity assumptions on the objective and counts arithmetic
operations; Section 1.2 makes both qualifications explicit. The parameters are
matrix size and number of variables, with polynomial arithmetic complexity if
either is fixed. This is a direct antecedent for exact algebraic output in
degenerate conic optimization. It does not immediately imply polynomial binary
certificates with only native Hessian-span dimension fixed.
[Author manuscript, Sections 1.1–1.2](https://homepages.laas.fr/henrion/Papers/degsdp.pdf).

Kolmogorov, Naldi, and Zapata, *Certifying solutions of degenerate semidefinite
programs*, give a numerical-symbolic certification approach. The inspected
author extended abstract assumes a numerical matrix sufficiently close to a
maximal-rank exact solution, then constructs a polynomial system with an
isolated correct solution. This is further evidence that exact certification
through algebraic solution recovery is established practice. The inspected
abstract does not supply the proposed uniform Hessian-span guarantee.
[Author extended abstract](https://www.unilim.fr/pages_perso/simone.naldi/extabstr.pdf).

## What the proposed result must add and prove

The credible contribution is a structural encoding theorem: for rational native
convex QCQP with fixed \(h\), one can choose a primal optimizer and a complete
dual certificate in one explicitly represented real number field, with degree
and total bit length polynomial in the input size. The certificate can then be
checked independently using exact field arithmetic. This would strengthen the
output and verification guarantees of the local exact-optimization theorem;
it would not create a new complexity-class inclusion once that theorem already
places the same fixed-parameter class in P.

Several distinctions are essential:

- A bound on each coordinate's degree does not bound their joint field by that
  same number. The common-field theorem and a bounded power-basis encoding are
  separate requirements.
- Linear systems over the primal field can place exposing multipliers and final
  KKT multipliers in that field, but their nonnegativity, existence, and bit
  growth must all be proved. A real solution does not automatically provide a
  well-encoded field solution without such an argument.
- At most \(h\) curved reductions does not mean at most \(h\) affine equations,
  all certificate entries, or total nonzero multipliers. Affine support can
  depend on the ambient dimension.
- A checker must verify soundness from the supplied data. It need not verify
  that the supplied point is the canonical minimum-norm optimizer if ordinary
  feasibility and the dual identities already certify the desired value.
- Native PSD-quadratic systems are a special class of SOCP-representable sets.
  General SOC constraints can produce indefinite quadratic polynomials after
  squaring. The native-Hessian-span theorem must not be advertised for every
  SOCP without another reduction preserving its hypotheses and bounds.
- Formula size, real-arithmetic verification time, certificate binary size,
  certificate construction time, and practical numerical recovery are distinct
  guarantees. Neither general extended duality nor qualitative field existence
  proves all five.

The potential solver benefit is a complete exact certificate format for a
structured class, including singular instances where ordinary KKT multipliers
may fail. Practical value still requires a reliable certificate extraction
algorithm and evidence about size and runtime on useful instances. Neither is
established by this literature audit.

## Search and inspection record

Searches covered exact duality, Ramana extended duals, Liu–Pataki certificates,
convex quadratic Farkas alternatives, SOS-convex alternatives, rational
infeasibility certificates, degenerate exact SDP algorithms, number-field
certification, and Hessian-span terminology. Primary statements and surrounding
proofs were inspected for Jeyakumar–Li Theorem 2.5/Corollary 2.7, Pataki Theorem 1,
Liu–Pataki Theorems 1–4, Klep–Schweighofer Theorems 2.2.5/3.5.2, Naldi–Sinn
Section 3.2/Theorem 4.7, and Nie–Ranestad Section 3.1. Inspection of the exact
algorithm papers was limited as stated above. The unpublished conference item
*Convex facial reduction algorithm and strong extended dual* by Lin, Liu, and
Lourenço was located in the official
[ISMP 2024 program, p. 122](https://www.gerad.ca/Charles.Audet/ISMP2024Complete_Program.pdf);
its abstract extends reduction to intersections of general closed convex sets,
but no full theorem was inspected here. It is an unresolved comparison lead.

This audit found substantial overlap in mechanism and no verified prior
fixed-native-Hessian-span certificate theorem. Establishing priority requires
further comparison; unsuccessful searches do not establish novelty.
