# Exact convex quartic decision: PosSLP prior comparison

Date: 2026-09-28. Status: scoped primary-literature audit with a
[fresh independent review](posslp-convex-quartic-prior-review.md). The SOCP
deduction below has independent mathematical checks. The quartic
reductions have separate proof reviews; this note does not replace them.
No priority claim.

Exact convex feasibility was already known to be PosSLP-hard through
semidefinite programming. Tarasov--Vyalyi's construction also gives exact
second-order-cone feasibility by the elementary duality argument below.
The potential addition in the repository is the much narrower target:
an explicitly expanded rational quartic with a supplied positive definite
rational Hessian Gram, a uniform global strong-convexity bound, and very
simple or absent constraints. Bounded arithmetic comparison itself is
also established prior work.

The strongest direct recent comparison located is *Hesse's Redemption*,
whose inspected November 2025 version leaves exact convex-quartic
threshold decision unresolved while proving polynomial-time approximation.
Its dated statement helps locate the contribution; it does not establish
priority or rule out another equivalent result.

## 1. Target problems and the relevant distinctions

The [cubic-root reduction](posslp-certified-cubic-root-reduction.md)
starts with an integer straight-line program over \(0,1,+,-,\times\).
The source question is whether its output is positive. Its intermediate
root gates have rational affine radicands in previous roots and their
individual squares, with polynomial-bit interval certificates near one.
Composing with the
[signed-root realization](signed-odd-root-circuit-quartic.md) gives the
following targets, whose proof statuses are recorded in their own files:

| Target | Extra structure that must be retained in the comparison |
| --- | --- |
| One quartic sublevel and one affine row | The quartic is globally strongly SOS-convex and has one zero; the feasible set is empty or a singleton. |
| Minimum comparison on the fixed unit cube | The objective is rational SOS, globally strongly convex, and has a supplied full positive definite rational Hessian Gram; the cube has a fixed rational interior point. |
| Unconstrained minimum-sign decision | The [reviewed perturbation](unconstrained-quartic-posslp-reduction.md) distinguishes a strictly negative minimum from a strictly positive minimum, retaining the supplied strict Hessian certificate. |

Here a full Hessian Gram means a rational matrix \(Q\succ0\) with

\[
 v^T\nabla^2F(x)v=(v,x\otimes v)^TQ(v,x\otimes v).
\]

The output polynomial and certificate have polynomial binary encoding
length. This is a bit-model statement in growing dimension, at fixed
polynomial degree. It is not a statement about succinct polynomials with
exponentially large expanded degree, convexity recognition, or fixed
dimension. The supplied Hessian certificate can be checked exactly by
rational linear algebra and coefficient comparison.

The cube's ordinary optimization domain has Slater points. The additional
zero-threshold sublevel can still be a singleton. These are different
notions of strict feasibility. For the unconstrained minimum-sign variant,
strong convexity gives existence and uniqueness of the minimizer, but
does not provide a polynomial lower bound on the absolute minimum value.

## 2. Tarasov--Vyalyi already prove broad exact convex hardness

[Tarasov and Vyalyi, *Semidefinite Programming and Arithmetic Circuit
Evaluation*, arXiv:cs/0512035v1](https://arxiv.org/pdf/cs/0512035v1),
Theorem 3, proves polynomial equivalence of comparison over several
arithmetic bases, including addition and \(x\mapsto x^2/2\), starting
from one. Theorem 4 and Section 2 reduce such comparison to exact SDP
feasibility. Their proof uses scalar addition epigraphs, two-by-two PSD
square epigraphs, and Ramana's extended dual. Thus PosSLP-hardness of
exact convex feasibility is established prior work, not the proposed
quartic contribution.

The paper appeared in *Discrete Applied Mathematics* 156(11), 2008,
2070--2078, [DOI 10.1016/j.dam.2007.04.023](https://doi.org/10.1016/j.dam.2007.04.023).
The mathematical audit here used the linked primary preprint.

### A direct SOCP deduction from the gate construction

The following is a reconstruction using their gates and standard conic
duality. It is recorded to prevent an inflated novelty claim. We did not
locate a separate primary statement with exactly this SOCP formulation.

Take a circuit \(C\) over addition and scaled squaring. Substitute its
input value one directly. Introduce one variable per remaining gate and
the constraints

\[
 x_i-x_j-x_k\ge0
 \quad\text{or}\quad
 \begin{pmatrix}2x_i&x_j\\x_j&1\end{pmatrix}\succeq0,
 \tag{1}
\]

according to the gate type. Minimize the output coordinate. All gate
values of the circuit are positive. By induction, every feasible gate
coordinate is at least its true value: addition is monotone, and the
square gate is monotone on the already positive predecessor. The true
circuit tuple is feasible, so the finite minimum equals \(C\)'s value
and is attained.

Choosing each new gate coordinate strictly above its required lower
bound, in topological order, gives a Slater point for the product cone
of scalar nonnegative cones and \(S_+^2\) blocks. Consequently its usual
conic dual has an attained optimum of the same value. This uses the
standard generalized Slater theorem; see Boyd--Vandenberghe,
*Convex Optimization*, Section 5.9, page 265
([author book page](https://web.stanford.edu/~boyd/cvxbook/),
[inspected PDF copy](https://www3.diism.unisi.it/~control/seminars/boyd/book/bv_cvxbook_draft.pdf)).
The cone is self-dual, so the ordinary dual uses the same block types.

For circuits \(A,B\), require a feasible dual solution for \(A\)
with value \(d_A\), a feasible primal solution for \(B\) with value
\(p_B\), and

\[
 \begin{pmatrix}d_A-p_B&1\\1&t\end{pmatrix}\succeq0.
 \tag{2}
\]

There exists such a \(t\) precisely when \(d_A-p_B>0\). Weak
duality implies \(d_A\le A\) and \(p_B\ge B\), so feasibility
implies \(A>B\). Conversely, if \(A>B\), attained optimal
solutions and a sufficiently large \(t\) satisfy (2). All matrices
and linear equations have polynomial-size rational descriptions.

Finally,

\[
 \begin{pmatrix}a&b\\b&c\end{pmatrix}\succeq0
 \quad\Longleftrightarrow\quad
 \|(2b,a-c)\|_2\le a+c.
\]

Thus this is an ordinary exact SOCP-feasibility reduction. No strict
inequality primitive or explicitly printed circuit value is needed.
Substituting the input one is essential to this simple Slater argument;
retaining a singular matrix block that forces it to one would hide that
step. The author and root independently checked this deduction, including
positivity, attainment, dual signs, and the strict-gap block.

This proof does not produce the target quartic. A two-by-two PSD
constraint has a convex feasible set, but its determinant inequality
need not be a globally convex polynomial row. Taking squares of gate
residuals also does not preserve convexity. A separate convex quartic
realization therefore remains a substantive step.

For current context, [Bodirsky, Loho, and Skomra, *Reducing Stochastic
Games to Semidefinite Programming*, ICALP 2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol334-icalp2025/html/LIPIcs.ICALP.2025.145/LIPIcs.ICALP.2025.145.html)
explicitly records the older PosSLP-to-SDP reduction and develops a
different stochastic-game reduction. It does not state the present
supplied-certificate quartic restriction.

## 3. The closest exact convex polynomial comparison

[Slot, Steurer, and Wiedmer, *Hesse's Redemption: Efficient Convex
Polynomial Programming*, arXiv:2511.03440v1](https://arxiv.org/html/2511.03440v1),
Section 1.3, studies the exact decision
\(\exists x\in P:f(x)\le0\), for rational \(f\) and a rational
polyhedron \(P\). Table 1 lists exact convex-quartic decision as
unknown and approximate convex polynomial programming as polynomial
time. Section 1.4 distinguishes exact SDP representation of SOS-convex
optimization from its unresolved bit complexity. Their result does not
give a polynomial separation of a nonzero optimum from zero.

The [arXiv record inspected on 2026-09-28](https://arxiv.org/abs/2511.03440)
listed version 1, dated 5 November 2025. The
[official STOC 2026 accepted-paper list](https://acm-stoc.org/stoc2026/accepted-papers.html)
includes the paper. No final proceedings text was inspected here. The
claim about its open entries is specifically about the linked version;
acceptance metadata is not evidence that every sentence remained
unchanged.

The repository's proposed lower bound fits their exact decision
framework directly, including with \(P=[0,1]^n\) or
\(P=\mathbb R^n\) for the respective variants. It would provide a
PosSLP lower bound at degree four under stronger promises. It would
not settle whether the general exact problem is in P, NP, coNP, or
PosSLP, or give a complete classification. Saying that it completely
resolves the table's unknown complexity entry would be too strong.

There is no conflict with polynomial-time approximation. To determine
an exact sign using an additive approximation, its error must be below
the absolute optimum. A reduction with doubly exponentially small
signals need not supply a polynomial-bit positive gap. The cube version
also separates a zero minimum from a positive minimum, so an arbitrary
fixed approximation error cannot decide its exact threshold.

## 4. Existing SOS exactness is a representation result

[Helton and Nie, *Semidefinite Representation of Convex Sets*,
arXiv:0705.4068v5](https://arxiv.org/pdf/0705.4068v5), Lemma 8 in the
inspected version, proves that an SOS-convex polynomial vanishing with
zero gradient at a point is a real sum of squares. The proof integrates
its Hessian on the segment from that point. Hence, for a strongly
SOS-convex polynomial \(G\) with minimum \(m\), \(G-m\) is
real SOS. In particular,

\[
                    G\ge0\quad\Longleftrightarrow\quad G\text{ is real SOS}.
\]

[Lasserre, *Representation of Nonnegative Convex Polynomials*,
arXiv:0801.3754v2](https://arxiv.org/pdf/0801.3754v2), Corollary 2.5,
gives the corresponding constant-multiplier SOS certificate for an
attained minimum under Slater's condition, with SOS-convex objective
and SOS-convex constraint rows written as \(h_j(x)\le0\). In the
paper's convention \(g_j(x)\ge0\), the requirement is SOS-convexity
of \(-g_j\). For a quartic on a cube this gives a finite
SDP description of the exact value at the first degree-compatible order
(moment order two for a quartic with affine constraints). Its statement does not
bound the binary complexity of obtaining or comparing that value.

These theorems establish useful upper representations. Neither the
existence of a polynomial-size SDP nor its exactness proves exact
bit-polynomial solvability. Conversely, old PosSLP-hardness for arbitrary
SDPs does not imply hardness of the special SDP family arising from a
strongly SOS-convex quartic. That restriction needs its own reduction.
Real polynomial SOS, rational polynomial SOS, and a rational SOS
certificate for the Hessian must also be kept distinct.

The unconstrained minimum-sign reduction consequently gives a lower
bound for real SOS testing even with
the strict rational Hessian certificate supplied. The polarity needs an
explicit step. If its construction has \(V>0\) exactly when
\(\min G<0\), apply it instead to the integer circuit \(1-V\).
Then \(V>0\) exactly when that new polynomial has positive minimum,
since the reduction excludes zero minima. This gives a many-one
reduction to SOS or nonnegativity membership. Its negative-minimum
instances are not SOS. Its positive-minimum instances are SOS by the
result just cited. This does not assert that arbitrary convex quartics
are SOS, or that every nonnegative rational SOS-convex quartic has a
rational polynomial SOS. The unconstrained proof also establishes a
stronger property of its positive-minimum branch: it has a rational
positive definite polynomial Gram. Thus its reduction also applies to
rational SOS membership. That existence argument gives no polynomial
bound on the size of the Gram.

## 5. Nearby hardness and circuit results do not subsume the target

[Ahmadi, Olshevsky, Parrilo, and Tsitsiklis, *NP-hardness of Deciding
Convexity of Quartic Polynomials and Related Problems*](https://web.mit.edu/~a_a_a/Public/Publications/convexity_nphard.pdf),
Theorem 2.1 and Propositions 3.4--3.5, concern recognition of convexity,
strong convexity, and strict convexity. Their reductions include
nonconvex instances. They do not establish hardness of minimizing a
polynomial already supplied with a valid strict Hessian certificate.
Likewise, nonnegativity testing for arbitrary quartics allows nonconvex
inputs and does not settle this promise class.

[Filos-Ratsikas, Hansen, Høgh, and Hollender, *FIXP-membership via
Convex Optimization: Games, Cakes, and Markets*](https://arxiv.org/pdf/2111.06878),
Theorem 3.2, builds an algebraic fixed-point pseudogate for bounded
convex optimization under explicit Slater assumptions, with circuit
access to functions and subgradients. This is a representation and
search-class membership result. It does not turn a fixed-point solver
into a polynomial-time exact threshold algorithm, nor state the
quartic lower bound here.

The [separate primary root-circuit audit](posslp-root-circuit-prior.md)
and its [independent source check](posslp-bounded-circuit-source-check.md)
cover older bounded averaging/multiplication simulations, the
addition/squaring basis reduction, recent polynomial-activation
gadgets, general radical-expression separation, and algebraic-program
reformulations. Those results do not supply the mandatory cubic-root
simulation with its interval and encoding promises. General root
circuits that retain multiplication are trivially at least as expressive
as integer SLPs; that observation does not settle the restricted basis.

Plain sums of radicals are a different input model. In particular, the
checked literature does not establish a PosSLP-hardness equivalence for
plain sums of cube roots. Square-root-sum comparisons and polynomial SOS
testing should not be conflated merely because their names involve
squares or roots.

## 6. Assessment, limitations, and search record

The strongest consequence of the linked reductions is
the simultaneous restriction of exact arithmetic hardness to degree
four, ordinary rational input, supplied strict SOS-convexity, and either
a fixed cube or no constraints. The unconstrained sign variant is
stronger than a zero-threshold singleton construction for explaining
why exact decision can remain difficult in a coercive, smooth problem
with a unique minimizer. The short restricted root-circuit simulation is
also a separate complexity statement.

For MINLP, the consequence would concern exact continuous subproblems
and certified threshold decisions that can occur inside a solver. It
does not by itself give a faster algorithm, prove typical numerical
difficulty, or rule out efficient approximations and condition-dependent
methods. PosSLP-hardness is an arithmetic benchmark; it is not an
unconditional NP-hardness or superpolynomial-time theorem.

Searches combined `PosSLP` with `convex polynomial`, `convex quartic`,
`strongly convex`, `SOS-convex`, `nonnegativity`, `semidefinite`,
`second-order cone`, `exact optimization`, and `root circuit`.
Primary text was read for the statements above; secondary search hits
were used only as leads. The independent root-circuit audit records its
broader source-side searches separately.

The search leaves several priority questions open: later proceedings
versions and unindexed papers may contain an equivalent restricted
convexity result; fixed-point or analog-computation literature may
contain a comparable local analytic root simulation; and an alternative
convex realization could make this reduction an old-tools corollary.
Not locating such a result is not evidence that it does not exist.

The root independently read Tarasov--Vyalyi's key equations and checked
the SOCP deduction in Section 2. That check used textbook Slater duality;
it did not independently audit every source in this note. The author
read the cited generalized Slater statement. No computation was needed
for these source comparisons. No project-wide checks or CI inspection
are part of this audit.

A targeted inline Python command checked the final newline, whitespace,
control characters, paired math delimiters, and the local links;
it passed. `git diff --check -- research-20260927/posslp-convex-quartic-prior.md`
also passed. These are document checks, not mathematical validation.
