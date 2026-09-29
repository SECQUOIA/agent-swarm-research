# Exact arithmetic comparisons encoded by one convex quartic

Date: 2026-09-28. Status: reduction and limitations passed independent
adversarial review. The quartic realization used below has separate completed proof
reviews. No NP-hardness, PosSLP-hardness, or SquareRootSum-hardness claim
is made.

Exact feasibility of one rational globally strongly convex, SOS-convex
quartic inequality together with one rational affine inequality can
decide a signed sum of real cube roots of binary integers. More generally,
it can compare a rational weighted sum of algebraic numbers supplied by
dense irreducible rational polynomials having exactly one real root.
The reduction has polynomial bit complexity. The inspected literature
does not currently justify identifying this comparison problem with
SquareRootSum or PosSLP.

This goes beyond the absence of rational feasible points: it embeds a
nontrivial arithmetic comparison into a narrowly specified convex
feasibility problem. Its complexity significance remains conditional on
the complexity of the source comparison. The main unresolved question is
whether substantially more succinct arithmetic circuits can be encoded
without losing global convexity or polynomial input size.

## Input problems and the reduction

Define **OneRealRootSum** as the following promise problem. The input is
a list of dense irreducible polynomials
\(p_i\in\mathbb Q[T]\), each with exactly one real root
\(\alpha_i\), together with binary rational numbers \(c_i,b\).
Decide whether

\[
             \sum_{i=1}^m c_i\alpha_i\leq b.                 \tag{1}
\]

The name is used locally to make the input model explicit; it is not a
claim that this is an established named complete problem. Degrees are
included through dense coefficient lists. The degree of the compositum
of the input fields is not part of this input representation.

**Proposition 1.** There is a deterministic polynomial-time reduction
from OneRealRootSum to feasibility of

\[
            F(z)\leq0,\qquad \ell(z)\leq b,                 \tag{2}
\]

where \(F\) is a rational quartic, is a rational sum of squares, is
SOS-convex, and satisfies \(\nabla^2F\succeq I\) globally.
The output can include rational certificates of its nonnegativity and
SOS-convexity. Before the affine inequality is added, its zero sublevel
is a singleton. Consequently (2) is either empty or a singleton.

**Proof.** For \(d_i=\deg p_i>1\), apply the
[verified general quartic construction](general-strongly-convex-quartic-singleton.md)
and [its Hessian-certificate extension](sos-convex-quartic-realization.md)
to obtain \(F_i\) on a separate block of \(d_i-1\) variables, with
unique zero

\[
       a_i=(\alpha_i,\alpha_i^2,\ldots,\alpha_i^{d_i-1}).
\]

For a rational root, use the one-variable polynomial
\(F_i(u)=(u-\alpha_i)^2+(u-\alpha_i)^4\).
Set \(F(z)=\sum_iF_i(z_i)\), and let
\(\ell(z)=\sum_i c_i z_{i,1}\). Nonnegativity of every summand
gives

\[
          F(z)\leq0\quad\Longleftrightarrow\quad
          z_i=a_i\text{ for every }i.                     \tag{3}
\]

Thus (2) is feasible exactly when (1) holds. Its Hessian is block
diagonal with blocks at least \(I\), and summing the rational SOS
expressions and Hessian certificates preserves those properties. The
degree is exactly four. Each block is constructed in polynomial time in
its dense input; adding the blocks and the affine row keeps total size
polynomial in the sum of the input sizes. Expanding in all variables
also takes polynomial space and time because the output degree is fixed.
No minimal polynomial for the joint tuple or its weighted sum is computed.
For an empty input list, use the dummy quartic \(F(t)=t^2+t^4\)
and the affine row \(0\leq b\); this also handles preprocessing that
removes every radical term.
\(\square\)

The sum has a rational PSD Gram certificate on the union of the block
Hessian bases. It need not have a **positive definite** Gram matrix on
the full basis \((y,z\otimes y)\): cross-block monomials such as
\(z_{i,r}^2y_{j,s}^2\), \(i\ne j\), have coefficient zero, which
precludes a positive diagonal Gram entry there. Global strong convexity
and SOS-convexity do not require that stronger representation.

The result also gives the equivalent optimization formulation

\[
       \min\{F(z):\ell(z)\leq b\}=0                       \tag{4}
\]

whenever the affine halfspace is nonempty. Strong convexity makes the
minimum attained and unique. Its value is zero exactly in the yes case;
in the no case it is strictly positive. A zero affine row producing an
empty halfspace is handled directly. This reformulation asserts no
polynomial lower bound on a positive value in the no case.

### Signed cube-root sums

For positive binary integers \(a_i\), the source condition

\[
                 \sum_i c_i\sqrt[3]{a_i}\leq b             \tag{5}
\]

is a special case with \(p_i(T)=T^3-a_i\). If \(a_i\) is not a
perfect cube, this cubic is irreducible over \(\mathbb Q\), since
a reducible cubic has a rational root and a rational root of this monic
integer cubic is an integer. Perfect cubes are recognized and their
integer roots computed by binary search in polynomial bit time; those
terms can be absorbed into \(b\), or represented by rational blocks.
Negative radicands change the sign of the coefficient, and zero terms
can be removed. Thus the reduction covers arbitrary signed coefficients
and signed integer radicands with the real cube-root convention.

There are at most two variables per nonrational cube-root block.
The construction is polynomial in the number of summands and the binary
lengths of the radicands, coefficients, and threshold. It is not
polynomial in the logarithm of an arbitrary exponent supplied in binary:
a polynomial \(T^D-a\) then need not have a polynomial-size dense
description. Fixed odd exponents or explicitly supplied dense
one-real-root inputs avoid that issue.

## What the primary literature presently supports

The [independent odd-radical audit](odd-radical-sum-complexity-prior.md)
records the search and precise source statements. Three distinctions are
essential.

**Equality is already easy for the relevant radical sums.** Hunter,
Bouyer, Markey, Ouaknine, and Worrell prove that deciding whether
\(\sum_i C_i A_i^{X_i}=0\), for positive rational \(A_i\), rational
\(C_i\), and rational \(X_i\in[0,1]\), belongs to uniform
\(\mathrm{TC}^0\). This includes cube-root-sum equality. Their
theorem is not a sign-comparison algorithm.
[Primary paper, Theorem 1](https://people.mpi-sws.org/~joel/publications/fsttcs10.pdf).
Replacing (5) by an equality test therefore does not create an established
hardness source.

**Cube-root comparison has an explicit connection to the radical-sum
literature, but no equivalence has been verified.** Kayal and Saha study
separation of square-root sums, prove polynomial bounds for a structured
class of radicands, and explicitly state in their final discussion that
their proofs and results extend to cube and fourth roots. Their stated
structured-radicand theorem is not an algorithm for arbitrary cube-root
sums, and that discussion is not a reduction from SquareRootSum to
cube-root-sum comparison.
[Primary paper, Theorem 1.4 and Section 5](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Sum20of20Square20Roots20ToCT.pdf).

**The famous hardness benchmarks must not be imported by analogy.**
Allender, B\"urgisser, Kjeldgaard-Pedersen, and Miltersen study PosSLP,
establish its counting-hierarchy upper bound, and give a reduction from
SquareRootSum to PosSLP. A reduction *to* PosSLP is an upper-bound
statement; it does not prove PosSLP-hardness of the source.
[Primary paper](https://people.cs.rutgers.edu/~allender/papers/slp.pdf).
Tarasov and Vyalyi reduce arithmetic-circuit comparison to exact SDP
feasibility. Their target is a general semidefinite system, not (2).
No conversion from that target to the present quartic class has been
established here.
[Primary paper, Section 2](https://arxiv.org/pdf/cs/0512035).

The odd-radical audit also gives an explicit adaptation of the
norm-separation and rational-Newton argument showing that both strict
and weak cube-root-sum comparison polynomial-time many-one reduce to
PosSLP. An [independent proof review](odd-radical-sum-upper-bound-review.md)
checks the separation gap, polynomial circuit length, positive
denominators, and treatment of equality. Thus the source lies in the
counting hierarchy using the cited PosSLP theorem. This is an upper bound,
not the missing reverse reduction or a polynomial bit-time sign algorithm.

The safe conclusion is that (2) can carry out signed odd-radical
comparison, an arithmetic problem directly discussed in the primary
literature. The audit has not located a proved NP-hardness,
PosSLP-hardness, or SquareRootSum-hardness theorem for the fixed-cube
source. That bounded search outcome must not be promoted to a proof that
no such theorem exists, or to a definitive current complexity
classification. The general OneRealRootSum source has an immediate
existential-real encoding by its defining equations and affine row;
this observation also supplies no hardness conclusion.

## Why the square-root route is obstructed

The [reviewed real-embedding obstruction](singleton-field-characterization-prior.md)
states that every coordinate of a rational convex-polynomial singleton
has exactly one real conjugate. In particular, no such singleton can
have a coordinate equal to \(\sqrt2\), or any other irrational
totally real number. Adding the affine row after constructing a
singleton cannot restore the missing coordinate realization.

This rules out the proposed **value-preserving block construction** for
SquareRootSum. It does not rule out an arbitrary polynomial-time
many-one reduction that encodes only the sign through different numbers
or a different geometry. Such a reduction would require a new argument.
Cardano formulas containing square roots do not supply it: the resulting
coefficients or radicands need not be rational or satisfy the required
single-real-conjugate condition.

## Odd-root circuits: a field condition is not a short construction

The signature condition itself is preserved by real odd-root circuits.
Here circuits start with rational constants, use rational arithmetic
with nonzero divisors where applicable, and take the unique real odd
root. Let \(K\) be the field generated by all values computed so far.
Inductively, it has exactly one real embedding. Adjoining
\(\beta\) with \(\beta^{2r+1}=a\in K\) preserves this property:
any real embedding of \(K(\beta)\) must fix \(K\), and then maps
\(\beta\) to the unique real root of that equation. Similarly, a
compositum of fields with one real embedding has one real embedding,
since every real embedding fixes each generating field. Rational
arithmetic adds no new generators. The passage to a field generated by
only the final output uses the odd-degree subfield argument in the
reviewed obstruction.

Consequently odd-root circuit outputs meet the necessary qualitative
field condition. This does not make the dense-input realization
polynomial in circuit length. Even a chain
\(\beta_0=2\), \(\beta_{j+1}=\sqrt[3]{\beta_j}\)
has final output \(2^{1/3^m}\), whose minimal polynomial
\(T^{3^m}-2\) is irreducible by Eisenstein and has exponentially
large dense description. The existing theorem cannot be invoked on
that expanded polynomial as a polynomial-time circuit reduction.
Independent blocks avoid compositum expansion; they do not simulate
nested dependent roots or multiplication gates.

### A proved obstruction to unscaled circuit values

**Proposition 2.** If \(F\) is twice continuously differentiable and
\(\nabla^2F\succeq I\) globally, with minimizer \(a\), then

\[
                         \|a\|\leq\|\nabla F(0)\|.       \tag{6}
\]

**Proof.** Strong monotonicity of the gradient gives
\((\nabla F(0)-\nabla F(a))^{\mathsf T}(0-a)
\geq\|a\|^2\). Since \(\nabla F(a)=0\), Cauchy--Schwarz
proves (6), including the case \(a=0\). \(\square\)

For a rational polynomial whose explicit coefficients have polynomial
bit length, its gradient at zero has at most exponentially large norm.
An arithmetic circuit of length \(O(m)\) can nevertheless produce
\(2^{2^m}\) by repeated squaring. Therefore a polynomial-size
construction of normalized strongly convex quartics cannot always
preserve all unscaled circuit values as coordinates of their minimizers.
The general solution-radius theorem of Slot--Steurer--Wiedmer gives the
corresponding obstruction for arbitrary explicitly encoded convex
polynomials, without a supplied strong-convexity normalization.
[Primary paper, Theorem 1.1](https://arxiv.org/html/2511.03440v1).

This argument leaves bounded, rescaled, or sign-only encodings open.
A short circuit can also create extremely small numbers, so controlling
only coordinate magnitudes does not address every succinctness issue.
No blanket impossibility of a PosSLP reduction follows from (6).

### Squared gate residuals do not preserve global convexity

Start with the strongly convex rational polynomial \(F_0(x)=x^2+x^4\)
and introduce a multiplication gate by the squared residual

\[
        H(x,y)=F_0(x)+\varepsilon(y-x^2)^2,
        \qquad\varepsilon>0.
\]

This nonnegative quartic has the intended unique zero \((0,0)\), but

\[
          \frac{\partial^2H}{\partial x^2}(0,y)
                            =2-4\varepsilon y              \tag{7}
\]

is negative for large positive \(y\). No choice of a small positive
weight fixes global convexity. Thus a unique real solution of a rational
quadratic circuit system, and even an invertible Jacobian there, do not
justify the claimed global quartic convexification. The existing proof
needs its special rational vanishing quadratic with a positive definite
quadratic part and arbitrarily small gradient. Producing that object
from a succinct dependent circuit is additional work.

## Consequence and next research question

The present proved reduction supports the statement:

> Exact feasibility for one rational globally strongly convex SOS-convex
> quartic inequality and one rational affine inequality can decide signed
> cube-root-sum comparison, with polynomial-size input and rational
> certificates of convexity and nonnegativity.

It does not yet support a standard hardness label. A polynomial-time
algorithm for this quartic feasibility class would yield one for the
source comparison. Conversely, any independently established lower bound
for that source transfers through Proposition 1. No such lower bound is
proved in this note.

The higher-potential open direction is a polynomial-size realization for
a rigorously specified bounded arithmetic-circuit class that already has
an established sign-comparison hardness theorem. Such a result must
control coefficient bit length and certify global convexity, while
avoiding expansion of the joint minimal polynomial. Signature closure
alone, ordinary SOS residual lifting, and numerical approximations
without a proved separation bound do not meet those requirements.

## Verification record

The reduction uses the already reviewed quartic construction rather than
rechecking it. The [independent review](quartic-exact-arithmetic-reductions-review.md)
checks the new block composition, input-size accounting, signature
closure, radius bound, and multiplication-gate counterexample. Its two
requested clarifications, the empty-list dummy block and the radius
lemma's explicit smoothness assumption, were independently rechecked.
The reviewer also separately verified the companion cube-sum upper bound;
the [author's independent check](odd-radical-sum-upper-bound-review.md)
records a second review of that proof.

Targeted inline `python - <<'PY'` commands checked the Newton error
identity and rational update, the gate Hessian identity, and Markdown
links, delimiters, whitespace, and final newlines. They passed. The
independent reviewer ran further exact block and affine-boundary examples,
listed in its review. These finite checks support the specified identities
and cases; the general claims rest on the proofs and their dependencies.
No Lean proof, project-wide verification, or CI inspection was performed
for this note.
