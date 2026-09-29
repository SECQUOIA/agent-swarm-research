# Rational SOS descent in three affine variables: prior results and limits

Date: 2026-09-28. Status: primary-literature search and targeted exact
calculations complete; fresh independent review requested. No publication
priority claim is made.

The relevant question concerns a rational polynomial of degree four in
**three affine variables**. Its homogenization is a **quaternary quartic
form**. The requested properties are minimum zero, a unique real zero,
and a rational positive definite Gram matrix for its Hessian biform on
the full vector \((v,x\otimes v)\). The existing arithmetic descent
counterexamples below do not establish this combination. The parent
research task has found a construction with a degree-five minimizer;
this note compares its mechanism with the literature, without replacing
the construction's separate proof and certificate review.

The dimension qualification matters. Scheiderer's classification rules
out failure of rational SOS descent in **two affine variables under
these hypotheses**, as proved in the
[earlier audit](rational-sos-convex-descent-prior.md). Thus a verified
three-variable construction would be dimension-minimal in this class.
This is not a claim that three variables are necessary for rational SOS
descent to fail without the convexity and strict Gram hypotheses.

## Closest published arithmetic counterexamples

[Laplagne, Section 3.1 and Proposition 3.1](https://arxiv.org/pdf/2312.16801)
reproduces a rational homogeneous quartic in four variables, attributed
to Capco, Laplagne, and Scheiderer. It is a sum of three squares over
\(\mathbb Q(\sqrt[3]2)\), but not a rational SOS. The section displays a
rational projective zero \([0:0:1:0]\) and an irrational real zero with
affine representative approximately \((1,-1.817,0.452,1.158)\). It reports
degree twelve for the latter's coordinate field. Its proof of failure of
rational descent uses a dual SOS functional whose kernel contains no
nonzero rational quadratic. This audit does not independently verify
that degree-twelve assertion or the dual certificate.

The same paper's Theorem 3.4 gives a strictly positive homogeneous
quartic in eight variables without rational SOS. It does not assert
convexity. These conclusions and the distinction between positive
values and interior SOS certificates are already compared in the
[earlier audit](rational-sos-convex-descent-prior.md).

The chronology is earlier than the 2023 preprint alone suggests. A
[2019 conference abstract by Capco, Laplagne, and Scheiderer](https://www.union-matematica.org.ar/suma2019/files/00-1a-005.pdf)
announces real-SOS/non-rational-SOS families in homogeneous dimensions
and degrees \((3,6)\) and \((4,4)\), using cubic coefficient fields. It
also announces uniqueness up to orthogonal transformations for its
examples. It contains no convexity claim. The abstract is evidence of
an announcement, not a substitute for a full proof. The full work
*Exact polynomial sum of squares decompositions*, cited as a 2023
preprint in Laplagne's references, was not located in this search.

[Capco–Scheiderer, Section 3.13](https://www.impan.pl/shop/en/publication/transaction/download/product/113947)
extends their strictly positive ternary-sextic analysis to quaternary
quartics. In this setting, a rational strictly positive real SOS that
fails rational descent must lie in a specified singular locus of the
algebraic boundary. The hypothesis is strict positivity of the form;
it does not cover a form with one real projective zero. It is not a
classification of all rational quaternary quartics with zeros. The
later eight-variable example does not settle every smaller-dimensional
strictly positive case discussed there.

## Why a change of chart does not convert the displayed example

The following are deductions, not statements quoted from the papers.

**Positive leading part.** Suppose a quartic \(F\) has a positive
definite Hessian Gram matrix \(M\) on \((v,x\otimes v)\). If \(F_4\)
is its degree-four homogeneous part and \(C\) is the principal block
of \(M\) on \(x\otimes v\), then

\[
12F_4(x)=x^{\mathsf T}\nabla^2F_4(x)x
        =(x\otimes x)^{\mathsf T}C(x\otimes x)>0
        \qquad(x\ne0).
\]

Consequently, if \(F\) has minimum zero, its homogenization has exactly
one real projective zero: strong convexity gives a unique affine zero,
and the displayed inequality excludes zeros at infinity. An invertible
real projective change preserves the number of real projective zeros.
The displayed Capco–Laplagne–Scheiderer form therefore cannot acquire
the requested properties by such a change of coordinates and a choice
of affine chart. Sending an unwanted zero to infinity violates the
positive-leading-part requirement.

There is also an arithmetic version of this obstruction. Any rational
projective zero stays rational under a rational projective change. If
the transformed polynomial had the requested properties, that zero
would have to be its unique affine minimizer. Taylor integration of
the rational Hessian SOS certificate at a rational minimizer would
give a rational SOS of the polynomial. Invertible rational projective
changes preserve rational SOS of forms, giving a contradiction.

The ordinary chart \(x_0=1\) is directly nonconvex: the exact Hessian
at the affine origin is

\[
\begin{pmatrix}16&32&64\\32&32&16\\64&16&64\end{pmatrix},
\]

whose first principal minor of order two is \(-512\). The displayed
form is also invariant under simultaneous sign change of
\((x_1,x_2,x_3)\). Thus the listed irrational affine zero gives its
negative as a distinct zero in the same chart. The paper's short list
of approximate representatives should not be used to infer that it
lists every real projective zero.

**Preserving an even-degree zero cannot fix the problem.** More
generally, let \(p\in\mathbb R^n\) have an even-degree coordinate field
\(K=\mathbb Q(p)\). The number of real embeddings of \(K\) is even
and positive, hence at least two. Distinct embeddings give distinct
real tuples because the coordinates generate \(K\). Every rational
polynomial vanishing at \(p\) therefore vanishes at at least two real
tuples. It cannot be a nonnegative strongly convex polynomial with
minimum zero. Subject to the reported field degree, this rules out
any rational perturbation that preserves the displayed irrational
zero, not just a perturbation by rational squares. It does not rule
out perturbations that move the zero to a different algebraic point.

## Homogeneous convexity results answer a different question

[Ahmadi–Blekherman–Parrilo, Theorem 3.1](https://arxiv.org/html/2404.14440v1)
proves that convex **ternary quartic forms** are SOS-convex over the
reals. Corollary 3.8 covers convex quaternary quartic forms with a
nonzero zero. Neither statement treats general affine ternary
quartics or rational SOS descent. Likewise,
[El Khadir, Theorem 1.1](https://optimization-online.org/wp-content/uploads/2019/09/7380.pdf)
proves real SOS for convex quaternary quartic forms. Convexity of an
affine polynomial does not imply convexity of its homogenization.

In fact, the desired irrational-zero homogenization cannot be convex.
Here is a direct reason. For a nonnegative convex homogeneous form
\(H\), a zero \(p\) gives \(H(tp)=0\) for every real \(t\). For
\(0<\varepsilon<1\), convexity gives

\[
H(x+tp)\le(1-\varepsilon)
H\!\left(\frac{x}{1-\varepsilon}\right).
\]

Letting \(\varepsilon\downarrow0\) gives \(H(x+tp)\le H(x)\).
Apply the same inequality with base point \(x+tp\) and shift
\(-tp\) to obtain the reverse inequality. Thus \(H(x+tp)=H(x)\),
and the zero set of \(H\) equals
its space of translation-invariant directions. For rational \(H\),
this space is the kernel of the rational linear system obtained by
setting every coefficient of \(D_pH\) to zero. A one-dimensional
such space is a rational line. A rational form with exactly one real
projective zero at an irrational point therefore cannot be convex as
a homogeneous form. This explains why the homogeneous theorems do
not contradict the proposed affine construction.

## Point ideals: established geometry and the different arithmetic gap

[Blekherman–Iliman–Kubitzke, Theorem 1.8](https://arxiv.org/pdf/1305.0642)
compares the degree-four parts of ordinary and symbolic squares of
point ideals in \(\mathbb P^3\). For six real points in general linear
position, the dimensions are respectively ten and eleven. For at most
five such points, the spaces have equal dimensions. Proposition 1.1
relates ordinary squares to spans of SOS faces; Proposition 1.3 and
Lemma 2.1 use independence and nondegenerate zeros to perturb
nonnegative forms. These are important prior versions of the
point-ideal perturbation method. Their real-point hypotheses and
nonnegativity conclusions do not supply rational descent or global
convexity for a Galois orbit having just one real point.

The degree-five point reported by the parent task is

\[
p=(a^{-1},a,a^{-3}),\qquad a^5=2,
\]

with rational quadratics

\[
q=(1-xy,\ x^2-yz,\ y^2-2z,\ z^2-x/2,\ xz-y/2).
\]

An independent exact calculation in this audit finds that the fifteen
products \(q_iq_j\), \(i\le j\), are linearly independent. The
rational degree-at-most-two evaluation map at \(p\) has rank five,
so these five independent quadratics form a basis of its kernel. The
rational space of quartics satisfying \(h(p)=0\) and
\(\nabla h(p)=0\) also has dimension fifteen. The product span is
contained in that space, so the spaces agree. These are calculations
for this particular orbit, not an unproved extension of the cited
real-point theorem.

Equality of these spaces does **not** force a rational SOS. It provides
a unique symmetric rational Gram matrix on \(q\) for each polynomial
in the space; that matrix can be indefinite. Rational SOS summands
vanishing at \(p\) must vanish at every conjugate, whereas real SOS
summands need only vanish at the real point. The proposed construction
uses this positivity obstruction: its base polynomial uses only the
first four quadratics, and subtraction of \(q_4^2\), with indices
starting at zero, forces a negative last Gram diagonal. Proving that
a sufficiently large multiple of the base retains a strict rational
Hessian Gram is the separate substantive convexity step. Neither the
dimension calculation nor the earlier point-ideal results prove that
step by themselves.

The precise prospective addition to the sources examined is therefore
failure of rational SOS descent with a strict rational Hessian Gram,
a unique nondegenerate irrational zero, and three affine variables.
The earlier two-variable result supplies dimension minimality in this
class once the construction is verified. These statements do not
establish hardness of exact optimization, practical solver failure,
or publication priority.

## Search and targeted verification record

Queries on 2026-09-28 included `rational SOS convex counterexample`,
`rational strongly convex sum of squares quartic`, `convex not Q-sos`,
`convex not rational SOS`, `quaternary quartic rational squares
Laplagne`, `Exact polynomial sum of squares decompositions Capco
Laplagne Scheiderer`, and queries for symbolic squares and double
points. The cited primary texts and relevant theorem statements were
read. The local extracted PDFs of Laplagne and Capco–Scheiderer were
also consulted. Scheiderer's published classification and the broader
descent results are covered in the linked earlier audit. Search
results for failure of real SOS or real SOS-convexity were not treated
as arithmetic counterexamples. Failure to find a matching theorem is
not evidence sufficient to establish novelty.

An inline `python -` command using SymPy constructed the \(35\)-by-
\(15\) coefficient matrix of the products above and verified rank
fifteen. It constructed the \(20\)-by-\(35\) first-jet matrix over
\(\mathbb Q\), reducing evaluations modulo \(a^5-2\), and verified
rank twenty and that its product with the first matrix is zero.
These checks establish the stated linear-space calculations only.
A separate exact calculation checked the displayed old example's
Hessian, sign symmetry, and rational zero, and the degree-two
evaluation rank five. No numerical approximation was used to
certify convexity, rational SOS, or failure of rational SOS.

An inline `python -` check passed the relative links, final newline,
display delimiters, whitespace, and control characters of this note.
`git diff --check -- research-20260927/three-variable-rational-sos-descent-prior.md`
also returned no diagnostics.

Only targeted checks for this note were run; no project-wide tests or
CI checks were run. The new geometric deductions and scope assessment
remain subject to the requested fresh independent review.
