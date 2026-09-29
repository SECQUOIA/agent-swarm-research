# An FPT candidate list for exact strongly convex quartic MINLP

Date: 2026-09-28. Status: the complete proof and the all-optimizer
strengthening passed
[fresh independent adversarial review](fixed-integer-strong-quartic-fpt-independent-review.md).
This strengthens the separately reviewed
[fixed-integer-dimension theorem](fixed-integer-strong-quartic-posslp.md).
The integer-query oracle theorem and the general idea of optimization
without objective bisection are prior results. Publication priority for
this application remains unestablished.

Let \(f\in\mathbb Q[Z_1,\ldots,Z_k,Y_1,\ldots,Y_n]\) have degree
at most four, with a supplied rational \(\mu>0\) and the promise

\[
                \nabla^2 f(z,y)\succeq\mu I_{k+n}
                \quad\text{on }\mathbb R^{k+n}.
\tag{1}
\]

Let \(Q\subseteq\mathbb R^k\) be an explicit rational polyhedron,
possibly unbounded or deficient dimensional. There are no constraints
on \(y\). Let \(L\) be the total explicit binary input length,
including \(Q\) and \(\mu\), increased to at least two.

**Theorem.** A deterministic algorithm, using no PosSLP queries, either
certifies \(Q\cap\mathbb Z^k=\varnothing\), or constructs a finite
list \(Z\subseteq Q\cap\mathbb Z^k\) containing every integer block
of every global optimizer of

\[
                 \min_{z\in Q\cap\mathbb Z^k, y\in\mathbb R^n}
                         f(z,y).
\tag{2}
\]

Its running time and total list encoding length are at most

\[
                     2^{O(k\log(k+1))}L^C,
\tag{3}
\]

for an absolute constant \(C\), independent of \(k\) and \(n\).
It uses ordinary rational convex optimization only at polynomially
specified accuracy. It may contain additional, nonoptimal blocks and
does not itself identify which members are optimal.

Using the reviewed [continuous observable comparison theorem](strong-convex-quartic-posslp-upper.md),
one can then return all optimal integer blocks, or decide any exact
comparison of the optimum with a rational threshold, within a bound of
the form (3), with PosSLP as an oracle. All PosSLP queries can be prepared
**nonadaptively**, after the candidate list has been constructed. This
does not assert a reduction to one PosSLP instance, or use closure of
PosSLP under arbitrary Boolean combinations.

The continuous block has unrestricted dimension. The theorem is fixed-
parameter tractability with respect to the number of integer variables,
relative to PosSLP only in its exact-selection step. It is not an ordinary
polynomial-time algorithm for exact comparison: that problem remains
PosSLP-hard even when \(k=0\), and for every fixed positive \(k\),
as established by the earlier theorem and its certificate-preserving
padding.

## 1. The precise existing integer-query theorem

We use the following oracle statement. A closed convex set
\(S\subseteq[-R,R]^k\), with integer \(R\ge2\), is given by an
oracle queried only at integer points. At \(z\in\mathbb Z^k\) the
oracle either confirms membership, or returns a rational inequality
valid on all of \(S\) and strictly violated by \(z\). No inradius,
positive dimension, rational facet description, or normalized-normal
promise is required.

If \(\Phi(t)\) bounds the bit cost and output length of an answer
on an integer input of total bit length at most \(t\), including the
fixed instance data, exact integer feasibility takes

\[
 2^{O(k\log(k+1))}
 \operatorname{poly}\bigl(k,1+\langle R\rangle,
       \Phi(c_0k(1+\langle R\rangle))\bigr).
\tag{4}
\]

The polynomial degree and \(c_0\) are absolute. Queries outside the
containing box can be answered by its inequalities; queried lattice
points under affine parametrizations are returned to the original
coordinates before the supplied oracle is called.

This is the explicit formulation in Ari--Hildebrand,
[*Hidden Convexity via Symmetric Displacement Covers*](https://arxiv.org/html/2609.18266v2#S3.SS3),
Definition 3.4 and Theorem 3.5 (version 2, 23 September 2026). The theorem
credits Hildebrand--Göß,
[*Complexity of Integer Programming in Reverse Convex Sets via Boundary
Hyperplane Cover*](https://arxiv.org/html/2409.05308v2), Theorem 9 and
Appendix B, and Basu,
[*Complexity of optimizing over the integers*](https://arxiv.org/html/2110.06172v6#S5.SS2),
Theorem 5.7 and Remark 5.11. The source proofs use deterministic lattice
subroutines. The [source audit](integer-query-convex-oracle-prior.md)
records the exact assumptions and checks the underlying statements.

Basu's Remark 5.9 already gives optimization without objective bisection
by retaining queried feasible candidates. We use that idea with cuts
that need only preserve better integer points. We do not invoke
Ari--Hildebrand's subsequent Lemma 3.6, whose objective encoding and
bisection assumptions do not directly cover algebraic fiber minima.

## 2. Bounding the integer search with FPT preprocessing

If \(k=0\), the candidate list is the singleton empty integer vector,
provided the zero-dimensional rational polyhedron is nonempty. Below
assume \(k\ge1\).

Use deterministic FPT integer linear feasibility to find
\(z_0\in Q\cap\mathbb Z^k\), or certify emptiness. A precise primary
bound follows by specializing Hildebrand--Köppe,
[*A new Lenstra-type Algorithm for Quasiconvex Polynomial Integer
Minimization*](https://arxiv.org/pdf/1006.4661v3), Theorem 1.1, to linear
constraints, a constant objective, and degree bound two. Clear each
rational row separately; an integer weak inequality \(p(z)\le0\)
becomes \(p(z)-1<0\). Their bound is
\(2^{O(k\log(k+1))}L^{O(1)}\), with output-coordinate length at
most \(2^{O(k)}L^{O(1)}\), with absolute polynomial exponents. The
constant objective attains a minimum whenever the integer domain is
nonempty, including when \(Q\) is unbounded. The precise specialization
was independently source-checked in the
[FPT interface audit](fixed-integer-quartic-fpt-oracle-interface.md).

Set \(C_0=f(z_0,0)\), \(a=\nabla f(0)\), and

\[
 A=\|a\|_1+|C_0-f(0)|+1,
 \qquad R=2+\left\lceil\frac{2A}{\mu}\right\rceil.
\tag{5}
\]

As in the reviewed bounded-domain reduction, strong convexity implies
\(f(x)\ge f(0)+a^{\mathsf T}x+\mu\|x\|^2/2\). For
\(\|x\|\ge R\) this exceeds \(C_0\). Coercivity and closedness
give attainment of (2), and every optimizer lies inside that radius.
Consequently the bounded polytope

\[
                         P=Q\cap[-R,R]^k
\tag{6}
\]

contains an optimal integer block and contains \(z_0\). The bit length
of \(R\) is at most \(2^{O(k)}L^{O(1)}\), with absolute exponents.
For an unconstrained integer block, take \(z_0=0\); then the simpler
radius from the earlier theorem has ordinary polynomial bit length.

Define \(g(z)=\min_y f(z,y)\). Every fiber has a unique minimizer,
and the reviewed projection argument proves global \(\mu\)-strong
convexity and

\[
                    \nabla g(z)=\nabla_z f(z,y(z)).
\tag{7}
\]

## 3. Strict cuts require no exact objective values

At an integer query \(z\in P\), compute a rational vector \(q(z)\)
such that

\[
                      \|q(z)-\nabla g(z)\|_2\le\mu/4.
\tag{8}
\]

Use the deterministic weak-optimization construction in Section 4.1
of the reviewed fixed-dimension theorem, always in the original
coordinates. For clarity, its bounds here are

\[
 m=n+k,\quad C=\max\{1,\textstyle\sum_\alpha|f_\alpha|\},\quad
 D=4mC(1+R)^3,\quad S=1+R+D/\mu,\quad K=1+12mCS^2.
\tag{9}
\]

The fiber minimizer has norm at most \(D/\mu\), and the
cross-Hessian has norm less than \(K\) on its unit neighborhood.
With \(\tau=\mu/(4k)\) and \(\eta=\min\{1,\tau/K\}\), a
rational fiber point of objective error at most \(\mu\eta^2/2\)
gives componentwise gradient error at most \(\tau\), hence (8).
Slot--Steurer--Wiedmer's
[convex polynomial approximation result](https://arxiv.org/html/2511.03440v1),
Corollary 1.2, provides that point in ordinary polynomial time in the
explicit fiber input and the requested accuracy encoding. For \(n=0\),
evaluate the rational gradient exactly.

For every distinct integer \(w\), put \(r=\|w-z\|\ge1\). Strong
convexity and (8) imply

\[
 g(w)-g(z)\ge q(z)^{\mathsf T}(w-z)
                   +\frac\mu2r^2-\frac\mu4r
 \ge q(z)^{\mathsf T}(w-z)+\frac\mu4r^2.
\tag{10}
\]

If \(q(z)=0\), then \(z\) is the unique integer minimizer, so it
is a valid immediate answer. Otherwise every other integer point with
\(g(w)\le g(z)\) satisfies the strict-query cut

\[
                    q(z)^{\mathsf T}(x-z)\le-\mu/4.
\tag{11}
\]

This cut is strictly violated at \(z\). In particular it retains every
strictly improving integer point. No exact objective value, normalized
gradient, objective gap, or algebraic number representation is used.
It can cut off a better nonintegral point; this is why the integer-query
oracle contract matters.

The deterministic construction of \(q(z)\) depends only on the fixed
input and \(z\), not on any incumbent or earlier oracle answers.
For a query of length \(t\), its bit cost and output length, including
the right side in (11), are bounded by

\[
                    (L+k+\langle R\rangle+t)^{C_1}
\tag{12}
\]

for an absolute constant \(C_1\). This follows directly from (9),
fixed degree four, and the ordinary polynomial-time approximation
theorem. There is no repeated transformation of the polynomial and no
bit-height bound iterated through dimension reductions. Queries under
the feasibility algorithm's internal parametrizations reach this
original-coordinate routine, as specified in the source theorem.

## 4. Constructing the candidate list

Initialize the list with \(z_0\). Run the deterministic feasibility
algorithm of Section 1 with radius \(R\), answering each integer query
\(z\) as follows.

1. If \(z\notin P\), return an explicitly violated inequality of
   \(P\). Do not append it to the list.
2. If \(z\in P\), append it to the list and compute \(q(z)\).
   If \(q(z)=0\), terminate with the current list.
3. Otherwise return (11), always as a rejection. Never return a
   membership confirmation.

Repeated queries can be answered by the same deterministic rule; a
cache is optional. No objective comparisons enter this construction.

### Termination and running time are not circular

Consider the fixed target set \(S=\varnothing\). Every returned
inequality is valid on \(S\) and strictly violated at its query.
Thus these are valid answers of an integer-query separation oracle for
the empty set. To make this an oracle defined on all queries, specify
that if step 2 would find \(q(z)=0\), it instead returns the arbitrary
strict rejection \(x_1\le z_1-1\). This completion has the same
bound (12); the actual list algorithm stops before using such an answer.

Until that possible early stop, the algorithm therefore follows exactly
a run with a fixed valid oracle for the empty set. The bound (4) applies.
Without an early stop, the feasibility algorithm must terminate with
integer emptiness, since no membership answer was given and its oracle
is valid for \(\varnothing\). In particular this argument does not
define a final incumbent before termination has been proved.

Substituting (12) and the bound on \(\langle R\rangle\) into (4)
gives (3). The number of appended points and their combined length are
bounded by the same running time. The initial FPT linear-feasibility
step also fits that bound.

### Why the list contains every optimal integer block

An early stop at \(q(z)=0\) gives a unique integer optimum by (10),
and that point has been appended. Otherwise suppose an optimal integer
block \(w\) is omitted from the final list. Define a fixed oracle for
the singleton \(\{w\}\): at \(w\), confirm membership; elsewhere
use exactly the same domain cuts and canonical gradient cuts as the
actual run.

This is a total valid oracle. Outside \(P\), the domain cut retains
\(w\). Inside \(P\), a query \(z\ne w\) has
\(g(w)\le g(z)\), so (10) makes (11) valid at \(w\), including
when \(z\) is a different optimizer with the same value. Such a query
cannot have \(q(z)=0\), since that would make \(z\) the unique
integer optimizer. The singleton oracle has the same answer-cost bound
(12): hardcode \(w\), whose length is \(O(k\langle R\rangle)\),
and add only an equality test at each query.

By the omission assumption the actual run never queried \(w\). It
therefore has exactly the same transcript with this fixed singleton
oracle. Its integer-emptiness verdict would contradict correctness.
Every optimal integer block must belong to the list. This singleton
argument and the stronger all-optimizer conclusion were identified by
the fresh reviewer and then independently rechecked by the author.

There are at most \(2^k\) optimal integer blocks. If two distinct
ones had the same coordinatewise parity, their midpoint would be a
feasible integer point of \(P\); strict convexity of \(g\) would
give it a strictly smaller value. The bound is attained by
\(\sum_{i=1}^k(z_i-1/2)^2\), with optional \(\|y\|^2\). This
elementary parity observation is an output-size consequence, not a
novel lattice bound.

## 5. Exact selection uses only nonadaptive PosSLP queries

Write the list as \(z_1,\ldots,z_s\). For a rational threshold \(r\),
the optimum is at most \(r\) if and only if at least one predicate

\[
                          \min_y f(z_i,y)\le r
\tag{13}
\]

holds. Each predicate reduces to one PosSLP instance by the continuous
theorem, and every instance can be constructed before any answer is
received. Strict comparison uses the corresponding strict predicates;
equality of the overall optimum with \(r\) follows from the answers
to the weak and strict batches.

To output all optimal integer blocks, prepare every pairwise comparison
of fiber minima. For indices \(i,j\), use the strongly convex quartic

\[
 H(y,y')=f(z_i,y)+f(z_j,y'),
 \qquad h(y,y')=f(z_i,y)-f(z_j,y')
\tag{14}
\]

and the continuous polynomial-observable theorem. The supplied curvature
is still \(\mu\); a full positive definite Hessian Gram for this
separable joint objective is not required. After all answers are
returned, retain each distinct member whose value is no larger than
all the others. Since the list contains every optimizer, this returns
the entire optimal integer-block set. There are at most \(s^2\) queries, which
still fits a bound of the form (3), and all can be generated
nonadaptively. Alternatively a sequential tournament uses \(s-1\)
comparisons if only one optimum is requested, with adaptive queries.

For each returned block, its continuous coordinate vector can be
specified by \(\nabla_y f(z_*,y)=0\), its unique real solution.
Expanded algebraic coordinates are outside the output guarantee. No Boolean closure
property of PosSLP is assumed: the final ordinary computation explicitly
combines the oracle answers.

## 6. Scope, significance, and remaining checks

The candidate list is a stronger structural output than a fixed-
dimension exact-decision upper bound. It shows that the discrete search
can be completed with ordinary polynomial-precision convex optimization;
the exact arithmetic difficulty is confined to comparing a finite list
of continuous fiber minima. The list is not claimed to be useful in
size or speed for a practical solver without further algorithm design.

The main earlier result remains valid and gives a separate geometric
derivation using the Oertel--Wagner--Weismantel central-point algorithm.
Its vertex enumeration only proved polynomial time for fixed \(k\).
The present stronger bound uses the more precise integer-query theorem
directly, so it does not need to promote generic polynomial bit bounds
at each recursive stage to a uniform FPT bound.

The strongest quadratic comparator is Del Pia,
[*Convex quadratic sets and the complexity of mixed integer convex
quadratic programming*](https://arxiv.org/html/2311.00099v2), Theorem 3:
exact convex mixed-integer quadratic optimization is ordinary
deterministic FPT in the number of integer variables, with arbitrary
mixed linear constraints and no supplied strict-curvature assumption.
The present result permits quartic objectives but uses stronger curvature
and domain assumptions and an oracle for exact selection. It does not
subsume that quadratic theorem. Del Pia's Section 4.4 also identifies
the missing oracle interfaces in attempts to derive such results just
from partial minimization; the current gradient and integer-query
construction supplies a specific interface under (1).

Ari--Hildebrand's recent quadratic and cubic optimization theorems
measure their mixed-integer complexity in total dimension. Their
quartic extension concerns pure integer objectives with concave quartic
parts. Neither statement is the theorem here. The shared ingredient is
the older convex integer-query oracle framework. Basu's existing
no-bisection optimization observation is also credited above. Absence
of a matching theorem in the examined sources is not proof of novelty.

Global supplied curvature, explicit fixed-degree input, and unrestricted
continuous fibers are substantive assumptions. No result is claimed
here for general constraints involving \(y\), for merely convex
objectives without a supplied positive curvature bound, or for circuit-
encoded polynomial objectives. The exact-selection statements are
relative to PosSLP and do not establish ordinary FPT exact comparison.

The [fresh review](fixed-integer-strong-quartic-fpt-independent-review.md)
independently checked the full proof and primary oracle contract,
identified the stronger singleton argument, and verified its amendment.
The root independently reconstructed the full original proof and the
subsequent strengthening. Positive reviews are evidence rather than
formal verification; neither review establishes exhaustive novelty.

Targeted author command actually run:

```text
python research-20260927/check_fixed_integer_candidate_list.py
```

It passed 72 exact value-free candidate-list runs and 660 strict cuts,
including retained optimizer transcripts, pairwise and threshold
batches, an adjacent integer tie, a zero-normal stop, and the empty-
oracle completion. The finite feasibility simulator enumerates a small
integer box: it is not an implementation or timing test of the FPT
algorithm. The independent reviewer additionally ran
`check_fixed_quartic_fpt_transcript_review.py`, passing 1,296 exact
affine-line runs, 3,429 queries, 216 tie cases, 42 zero-normal stops,
and a radius-\(2^{100}\) case with 101 queries. These checks challenge
the transcript logic and degeneracies. They do not verify the cited
general feasibility algorithm or its asymptotic complexity. No Lean
formalization, project-wide checks, or CI inspection was performed.
