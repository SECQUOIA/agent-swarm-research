# Strategic reassessment of the Hessian-span research program

Date: 2026-09-28. This is a fresh assessment of significance, prior-work
exposure, and research priorities. It is not a replacement proof review.
The author read the current theorem statements and their main arguments,
the listed prior audits, and the primary sources identified below. A request
for a further independent subauditor hit the active-thread limit; no such
additional review is claimed.

The strongest current opportunity is to finish the exact conic optimization
frontier, then attack the dependence of exact *decision* on Hessian span.
Further variants of algebraic output, certificates, and error bounds should
be judged against these larger objectives. They are useful supporting work,
but accumulating them does not by itself make the central contribution more
important.

## What presently carries the contribution

Two algorithmic results deserve the lead position together:

- [Exact unbounded mixed-integer convex quadratic optimization](hessian-span-main-results.md)
  at fixed integer dimension and fixed continuous Hessian span returns
  exact values and optimizers, without an input box or Slater condition.
- [Exact unbounded MISOCP feasibility](unbounded-misocp-frontier.md)
  at the same fixed parameters permits indefinite squared Hessians and
  nonclosed continuous projections. It handles a broader constraint class,
  but presently provides a weaker output.

The second is the most promising expansion of the first. It is not just a
change of notation: a general rational cone system can have an irrational
recession ray, a finite unattained infimum, or continuous unboundedness
without integer unboundedness. The reviewed
[conic boundary examples](socp-unboundedness-boundaries.md) explicitly rule
out transferring the native-PSD proofs unchanged.

The [nonconvex finite-infimum precision theorem](nonconvex-finite-infimum.md)
is now the central technical candidate. Its force is a uniform effective
bound on degree and coefficient size with arbitrary affine constraints,
degeneracy, and nonattainment. Generic algebraic degree alone does not do
this. The ordered-limit proof retains a radius as a formal coefficient
parameter rather than inserting an uncontrolled numerical radius.
This distinction explains why the result can support exact conic decision.
It should be foregrounded more clearly than a long list of separate output
corollaries.

The current evidence supports a substantial candidate theoretical advance.
It does not establish publication priority, practical formulation size, or a
speedup for an existing solver. In particular, no audited distribution of
Hessian span over important application families or benchmark libraries is
available here. The parameter is computable on a supplied formulation, but
an arbitrary extended formulation can change it. Statements about widespread
applicability need additional mathematical modeling evidence, not only the
fact that SOC constraints are common.

## Findings that narrow the novelty claim

The main sources already account for much of the surrounding machinery.
These are substantive qualifications, not incidental citations.

1. The [nonconvex prior audit](nonconvex-hessian-span-prior-audit.md) derives
   short feasible-point representations and radius bounds from
   Grigoriev--Pasechnik component sampling plus a minimum-dimensional face
   argument. The new interpretation of the parameter is useful, but these
   conclusions should not be advertised as a new general certificate
   technique. This also removes the feasible-radius theorem as an independent
   novelty pillar of the conic result.
2. The updated [SOCP audit](socp-hessian-span-prior.md) derives the entire
   span-zero and span-one decision and boxed-integer projection baseline
   from older bounds. In the span-one case, one proportionality sign reduces
   to one quadratic inequality; both signs force rank at most two by SOC
   inertia. An example with many proportional cone rows does not establish
   an advance beyond that baseline.
3. Classical rational polyhedral cone approximations already provide the
   linear lifts. The main new obligation is a sufficiently small *uniform
   fiber gap*, including degenerate and unbounded fibers. Exact preservation
   of integer assignments must continue to be distinguished from exact
   preservation of the continuous feasible set.
4. Nie--Ranestad already supplies the familiar generic QCQP degree formula.
   The canonical degenerate optimizer bound and
   [explicit small-input degree examples](short-input-qcqp-degree-lower-bound.md)
   are valuable refinements, but the degree formula itself is not new. The
   examples obstruct dense minimal-polynomial output in FPT time; they do
   not obstruct FPT decision or succinct output.
5. The qualitative Hölder exponent has an established conic facial-reduction
   derivation. The arithmetic control of its constant is the separate
   candidate addition. Likewise, real primal-dual and infeasibility
   certificate mechanisms have substantial prior art; the controlled
   binary size and common-field implementation are the relevant refinements.

These corrections strengthen the case for a more focused theorem paper.
They also show why unsuccessful keyword searches are weak evidence: several
apparently new results have already become short consequences after a more
careful comparison of formulations.

The prior-risk that remains most serious is an existing coefficient-sensitive
critical-point or asymptotic-value theorem that already permits arbitrarily
many affine inequalities at a cost logarithmic in their number. The current
sampling audit does not prove that such a theorem is absent. Before a priority
claim, inspect whether the older perturbation proofs can preserve affine
rows rather than raising them to the maximum degree, and whether a parametric
few-quadratic sampling theorem already controls the boundary values of the
objective projection. A generic KKT theorem alone is insufficient, but a
suitable specialization theorem could subsume much of the argument.

## First priority: complete unbounded mixed-integer conic optimization

The consequential target is a theorem for rational linear objectives over
rational MISOCP sets, with fixed integer dimension and fixed continuous
squared-Hessian span, without an input box. It should distinguish infeasible,
unbounded below, finite attained infimum, and finite unattained infimum.
In the finite cases it should give an exact value representation of controlled
size; in the attained case, an exact optimizer. This is a proposed target,
not a consequence established by this assessment.

A useful intermediate theorem has a shorter route. If the objective involves
only integer coordinates and has rational coefficients, scale it to be
integer-valued. A finite infimum is then attained. Apply the optimal-integer
witness part of Khachiyan--Porkolab to the compressed convex projection in
[the unbounded MISOCP proof](unbounded-misocp-frontier.md), rather than only
its feasibility consequence. A resulting magnitude bound would make one
sufficiently low objective-threshold query distinguish unboundedness from
finite optimum. The existing feasibility oracle would then support integer
bisection. This route does not use continuous/integer unboundedness
equivalence. It still requires its own proof and parameter accounting.

The hard step is a continuous objective coordinate. Neither a small feasible
integer point nor a polynomial bound for every *fixed* integer fiber controls
an infimizing sequence of integer assignments escaping to infinity. One
must prove a bound for the mixed-integer value itself, or find a counterexample
to the proposed algebraicity/height statement. Treating the integer variable
as a real coefficient parameter and taking an arbitrary real limit can lose
the lattice restriction.

A concrete early test is the rational semialgebraic convex projection onto
(integer variables, objective value). Determine what the closure of its
integer slices can add at the lower objective boundary. The two-dimensional
irrational ray and strip examples should be included from the start. The
strip admits a rounding-based escape sequence and no rational polynomial
escape curve. Thus the final theorem may need a certificate involving
rounding or lattice approximation, rather than the existing polynomial-curve
format.

This target would expand the theory beyond currently handled pathological
cases. It could support exact classification of degenerate conic subproblems
inside a MINLP solver. An actual solver benefit would still require usable
bounds and an algorithm avoiding enormous universal precisions.

## Second priority: decide whether the exponent in span is necessary

The current running times are XP in span: the exponent on input length can
grow with the parameter. The most consequential parameter question is whether
exact *feasibility* admits a bound

\[
                         f(h,k)N^C
\]

with an absolute constant \(C\). The dense-output lower bound leaves this
question untouched. Its hard examples even consist of small, explicit
trust-region blocks, each easy to approximate. Their compositum degree is
large, but large degree is not evidence that comparison with zero is hard.

A concrete, narrower target is a separation theorem for positive optimal
violations of boxed rational convex QCQPs or SOC systems:

\[
 \alpha>0\quad\Longrightarrow\quad
 \log(1/\alpha)\le f(h)N^C.
\]

If accompanied by the corresponding radius and construction bounds, such a
statement could improve the MILP reduction and exact decision complexity.
Conversely, explicit polynomial-input examples with
\(\log(1/\alpha)\ge N^{\Omega(h)}\) would rule out this particular
precision-based FPT route. They would still not rule out FPT decision by a
different representation or comparison algorithm. Existing high-degree
examples establish neither alternative.

The sum-of-square-roots problem is a useful warning about this distinction.
Eisenbrand, Haeberle, and Singer obtain a separation estimate with a constant
depending on the radicands that is not explicit. It therefore does not supply
an input-uniform decision bound. This illustrates why a formally stronger
asymptotic inequality can be inadequate for exact complexity.
[Primary SoCG 2024 paper and abstract](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2024.54).

An initial restricted problem is comparison of sums of a fixed number of
independent trust-region optimal values. This uses the explicit constructions
already developed and isolates the field-compositum issue from active-set
geometry. A useful result would either exploit its analytic structure to
avoid full compositum expansion or prove a genuine comparison barrier.
Merely storing each summand separately does not supply an efficient exact
sign test for their sum.

This is a higher-risk direction than finishing continuous conic optimization.
It is nevertheless a more significant question than another representation
of the same \(N^{O(h)}\)-size optimizer.

## Third priority: a finite certificate interface for degenerate conic fibers

A solver-oriented theoretical target is an exact certificate procedure for
fixed-span SOC fibers that handles infeasibility, weak infeasibility,
nonattainment, and attained optimum without Slater assumptions, while allowing
a branch-and-bound or outer-approximation algorithm to retain rational linear
master problems. The output must be checkable without rerunning a global
conic optimization algorithm. An informative complexity bound would depend
on the certificates actually produced, with the universal span bound serving
as a fallback.

This is only worth a main research lane if it goes beyond established conic
certificate outer approximation. Coey, Lubin, and Vielma already derive
finite termination and tolerance-aware cut guarantees from conic certificates.
Their presentation assumes finite integer bounds and well-posed continuous
primal-dual subproblems; in particular, their status classification uses
attainment and strong duality. Those hypotheses identify a concrete boundary
for an extension. Their paper already supplies the practical motivation, so
that motivation must not be claimed as new.
[Primary 2018 manuscript, §§2.1 and 3](https://arxiv.org/pdf/1808.05290).

There are two separate difficulties. First, a weakly infeasible fiber need
not admit the usual strict separating conic ray. Second, an exactly known
irrational optimizer need not itself give rational supporting cuts whose
small finite collection preserves an exact objective threshold. The current
uniform-gap MILP construction offers a possible finite fallback, but a theorem
that only rebuilds the entire worst-case lift at each node would add little.
The desired advance is a compositional certificate with a meaningful bound
on the extra work caused by degeneracy.

By contrast, constructing the facial multipliers in the existing common
number field would close a useful implementation gap in the current
certificate theorem. It should be completed when convenient, but it is
supporting work rather than the next substantial theoretical objective.

## Directions that should not absorb the main effort

The following are useful boundaries or completion tasks, not leading routes
to the user's requested increase in significance:

- More variants of the span-one conic result, already covered by the audited
  older bounds.
- Another sharp algebraic-degree example without a new input-size,
  comparison, or precision consequence.
- Replacing explicit convex representations by a promise that the resulting
  set is convex. The reviewed
  [representation boundary](convex-representation-boundary.md) reduces the
  zero-or-one-solution SAT promise to span-one quadratic feasibility. Its
  Valiant--Vazirani consequence blocks the naive tractability claim.
- Extending quadratic theorems to arbitrary bounded-degree polynomials merely
  by counting the polynomial span. One quartic sum of squares can encode an
  arbitrarily long system of quadratic equalities; the quadratic stationarity
  elimination is an essential mechanism, not incidental notation.
- Treating a small SDP formulation as a bit-polynomial exact algorithm.
  Exact algorithms for degenerate SDP already give polynomial complexity when
  the affine-variable count or matrix order is fixed. Neither parameter is
  automatically bounded by the native quadratic Hessian span.
  [Henrion and Naldi, primary manuscript](https://arxiv.org/abs/1802.02834).

The most useful immediate sequence is therefore: complete continuous conic
optimization as a checked milestone, establish the integer-objective conic
case, and attack the continuous-objective mixed-integer boundary while a
separate lane studies decision/precision dependence on span. Retain the
certificate interface as an application-driven alternative if it produces
a theorem beyond known outer-approximation assumptions.

## Sources examined and verification limits

First-hand local reading included the research index, main synthesis,
nonconvex finite-infimum proof, nonconvex prior audit, SOCP theorem and prior
audit, unbounded MISOCP proof, direct degree construction, conic boundary
examples, and the repository's open-theory-challenges note. The main
source-backed comparisons above were checked against the primary cone
complexity paper, the primary conic outer-approximation manuscript, the
primary Valiant--Vazirani paper, the SoCG separation paper's statement, and
the exact-SDP manuscript's statement. The new conic complexity source was
also inspected directly:
[Blanco, Magron, and Martínez-Antón, §§4--5](https://arxiv.org/html/2501.09828v2).
Its nonpolynomial fixed-cone-count upper bounds do not establish that the
fixed-cone-count problem was open or that the present theorem has priority.

Searches covered exact SOCP complexity, fixed quadratic counts and affine
rows, mixed-integer finite infima and attainment, parameterized exact convex
optimization, and algebraic separation. No complete citation-graph search
or external expert review was performed. This assessment found no direct
subsuming theorem, but that unsuccessful search does not establish novelty.

No mathematical claims in the main package were changed. Only this note was
written. The targeted command `python -` checked nine local links, the final newline,
trailing whitespace, and control characters; it passed. These are document checks;
they do not establish the proposed new theorems. No project-wide checks,
CI inspection, or numerical optimization tests were performed.
