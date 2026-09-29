# Prior audit: an unrestricted PSD objective and few nonlinear constraint directions

Date: 2026-09-28. Scope: literature and significance review of
[common-range-optimization.md](common-range-optimization.md), including
its proposed exact optimizer output. This audit does not certify the
proof or change the review status of that output construction.

The strongest inspected comparator is Del Pia's FPT algorithm for
mixed-integer convex quadratic optimization over a polyhedron. The
polynomial-chart mechanism used to extend that result is classical
parametric quadratic programming. The possible contribution is the
resulting exact FPT theorem for many native nonlinear constraints, with
the objective excluded from the constraint-range parameter. The search
found no inspected statement that already establishes that full theorem.
This is a qualified literature finding, not evidence of priority.

## 1. The precise claim to compare

The input consists of rational native convex quadratic constraints or
rational SOC constraints, arbitrarily many affine rows, and a jointly
PSD quadratic objective of arbitrary rank. For continuous variables,
the native Hessians have common range dimension

\[
 r=\operatorname{codim}\bigcap_i\ker H_i.
\]

The objective Hessian is excluded. With supplied integer bounds the
parameter uses continuous Hessian blocks, together with the integer
dimension \(k\). Without those bounds, the proposed threshold theorem
uses the stronger cross-aware continuous kernel
\(\{v:H_i(0,v)=0\ \forall i\}\). Squaring a SOC row retains its
affine sign condition.

The proposed runtime is \(f(k,r)N^C\), with an absolute exponent
\(C\), for threshold decision and, with bounded integer variables, exact
value, attainment, and optimizer recovery. Continuous optimization has
the corresponding \(f(r)N^C\) bound. Unrestricted mixed-integer exact
value computation is outside the manuscript's claim.

This parameter differs from the Hessian *matrix-span* dimension \(h\).
One has \(h\le r(r+1)/2\), but \(h=1\) permits \(r=n\).
Consequently a common-range FPT theorem improves dependence on \(r\)
without subsuming the repository's broader fixed-\(h\) polynomial-time
theorem. The distinction from including the objective in \(r\) is
substantial: an identity objective Hessian would make that enlarged
parameter equal to the full continuous dimension.

## 2. Strongest direct algorithmic comparator

[Del Pia, *Convex quadratic sets and the complexity of mixed integer
convex quadratic programming*, v2](https://arxiv.org/html/2311.00099v2),
Proposition 4, solves feasibility for an arbitrary rational polyhedron
intersected with one PSD quadratic inequality in FPT time parameterized
by integer dimension. Theorem 3 solves convex quadratic optimization over
a rational mixed-integer polyhedron with the same parameter. Continuous
dimension and quadratic rank are unrestricted. Sections 4.2 and 4.4,
including their proofs, were inspected.

This completely covers the new theorem's polyhedral-constraint case.
It is also the exact subroutine retained after approximating the native
nonlinear constraints. The candidate advance is allowing many such
constraints sharing a small common range. It is not a new one-quadratic
algorithm. The final discussion in Section 4.4 explicitly identifies
obstacles to inferring worst-case FPT from general convex evaluation
oracles: extension domains, subgradient access, and expected versus
worst-case time. This reinforces the need to prove the proposed reduction
and its precision bound, rather than appeal loosely to convex oracle
optimization.

## 3. The chart construction is established parametric-QP theory

[Spjøtvold, Tøndel, and Johansen, *Unique Polyhedral Representations of
Continuous Selections for Convex Multiparametric Quadratic Programs*,
ACC 2005](https://skoge.folk.ntnu.no/prost/proceedings/acc05/PDFs/Papers/0149_WeB08_6.pdf),
Equation (1), treats a fixed PSD Hessian and fixed constraint matrix,
with affine objective and right-hand-side parameters. Theorem 1 gives
piecewise affine optimizer selections. Section IV permits singular and
zero Hessians; Lemma 3 obtains the least-norm optimizer through a secondary
strictly convex QP. Its Proposition 1 also uses constancy of the objective
gradient across an optimal face. The primary text at pp. 816--820 was
read. The 2007 journal extension is
[DOI 10.1007/s10957-007-9215-z](https://doi.org/10.1007/s10957-007-9215-z).
The conference exposition assumes a full-dimensional parameter domain
and omits lower-dimensional regions during enumeration; it should not
replace the manuscript's direct argument for all degenerate charts.

[Patrinos and Sarimveis, *Convex parametric piecewise quadratic
optimization: Theory, algorithms and control applications*, author
preprint](https://www.chemeng.ntua.gr/labs/control_lab/zipfiles/tr2010-01.pdf),
Proposition 5 and Section 4.2, give piecewise quadratic values, polyhedral
optimizer graphs, and least-norm piecewise affine selections. The latter
section addresses failed LICQ through projection and credits the earlier
selection result. Those sections and the parameter model were read.
There is a qualification: the preprint's literal statement that a proper
convex piecewise quadratic function always has a proper inf-projection
needs a boundedness assumption. The function \(f(v,u)=-v\) is a
counterexample. This audit uses its structure results only on fibers
with finite attained minima. The manuscript's separate recession
argument remains necessary.

Here is the explicit connection, reconstructed in this audit. After the
common-kernel split, the fiber has constant matrix \(C\) and quadratic
right-hand side \(d(u)\); the objective is

\[
 q(u,v)=\tfrac12v^TQv+b(u)^Tv+c(u).
\]

Introduce formal parameters \(U_{ij}\) for the monomials \(u_i u_j\).
Then \(Cv\le d(u,U)\) is affine in its parameters. The original
jointly PSD objective remains quadratic in \((u,v)\), independent of
\(U\). Classical affine solution pieces, followed by the substitution
\(U_{ij}=u_i u_j\), give polynomial optimizer pieces of degree at most
two. Substituting them in the objective gives value pieces of degree at
most four. This degree count is an immediate consequence of established
theory. The particular all-active-row pseudoinverse proof is useful for
degeneracy and rational coefficient bounds, but should not be advertised
as discovery of the underlying piecewise-polynomial phenomenon.

Neither inspected source provides the desired FPT algorithm. Explicit
region enumeration can be exponential in the original input size. The
proposed proof instead uses existence of the charts to bound precision
and never enumerates their family. That distinction is central.

## 4. Other nearby formulations

[Kannan and Rademacher, *Optimization of a Convex Program with a
Polynomial Perturbation*](https://www.math.ucdavis.edu/~lrademac/fplusp.pdf),
Theorem 4, permits a convex objective plus a degree-\(d\) polynomial
depending on \(r\) coordinates over a convex body. It gives error
\(\epsilon\operatorname{range}(p)\), with a factor
\((O(rd^2/\sqrt\epsilon))^r\) times convex optimization cost and a
rounding cost. The introduction, model, algorithm, and theorem were
read. This is a strong precedent for isolating a few nonlinear directions
while leaving a large convex core. It does not furnish exact algebraic
output, native-constraint feasibility certification, or complexity
polynomial in the *bit length* of very small tolerances.

[Oertel, Wagner, and Weismantel, *Integer convex minimization by mixed
integer linear optimization*](https://orca.cardiff.ac.uk/id/eprint/86766/1/IntegerConvexMinRev4.pdf),
Theorem 1, reduces bounded integer convex minimization in fixed dimension
to MILP calls, given first-order evaluation oracles with prescribed
precision. It is exact when value oracles are exact. The statement,
oracle assumptions, discussion of precision, and both algorithm outlines
were read. Its final paragraph also permits a mixed-integer extension
conditional on sufficiently precise continuous minimization. It does not
construct exact projected value or subgradient
oracles for degenerate high-dimensional QCQPs. Therefore it is an
important oracle-reduction precedent, not a direct replacement for the
present bit-complexity argument.

[Brand, Koutecký, Lassota, and Ordyniak, *Separable Convex Mixed-Integer
Optimization: Improved Algorithms and Lower Bounds*, ESA 2024](https://drops.dagstuhl.de/storage/00lipics/lipics-vol308-esa2024/LIPIcs.ESA.2024.32/LIPIcs.ESA.2024.32.pdf),
Theorem 1, treats separable convex objectives under linear constraints,
parameterizing row count and maximum matrix-entry magnitude. Its runtime
also includes the cost of solving the continuous relaxation. The model,
Theorem 1, and the beginning of its proof were read. This neither allows
the same nonlinear constraint family nor uses the same parameters.
Separability of an objective, few nonlinear constraint directions, and
small linear constraint coefficients must not be conflated.

[Scott and Geunes, *A normal fan projection algorithm for low-rank
optimization*](https://doi.org/10.1007/s10107-024-02079-y), Sections 1--2,
give exact minimization of a low-rank quasiconcave objective on suitable
polytopes using a supplied normal-fan refinement. The local primary
full text was read. The number of arrangement cells is
\(O(s^{r-1})\), where \(s\) counts relevant hyperplanes. This is a
different, generally nonconvex optimization direction; the input-size
exponent depends on rank. It does not establish the claimed FPT convex
minimization theorem.

The prior feasibility audit already compares Basu--Roy radius bounds,
Khachiyan--Porkolab integer witness bounds, Hildebrand--Köppe, Toledo, and
LP-type algorithms. Those quantitative algebraic and oracle ingredients
remain prior results. This audit did not reinterpret them as new
elimination theorems. See
[common-range-fpt-prior.md](common-range-fpt-prior.md).

## 5. Significance and limits

Conditional on completion of the proof reviews, the strongest theorem
would extend exact FPT mixed-integer convex quadratic optimization from a
polyhedron to many quadratic or conic constraints controlled by a few
continuous directions. Excluding the objective lets a model penalize all
individual continuous variables while nonlinear constraints involve only
a few aggregate features. For example, a full-rank convex quadratic cost
is compatible with many native constraints
\((Fx)^TS_i(Fx)+a_i^Tx+b_i^Tz+c_i\le0\), where
\(S_i\succeq0\) and the rank of \(F\) is small. This is a model
family covered by the proposed theorem, not evidence of measured solver
benefits or prevalence in a particular application.

The theoretical gain is an input-size exponent independent of the
structural parameter, including degeneracy and exact decisions. A small
range alone does not make the parameter factor small. Global radius and
separation bounds may produce impractical tolerances. A solver benefit
would require sharper instance-specific certificates, a practical way to
detect or exploit this structure, and computational evaluation. The
present work establishes none of those empirical consequences.

The exact optimizer output is more than a numerical approximation and
requires its own proof. A short algebraic optimizer, an exact threshold
oracle, and a full polynomial-time reconstruction algorithm are distinct
claims. Likewise the finite bounded-integer argument must not be extended
to unbounded integer assignments without a new value theorem. The
manuscript currently preserves both qualifications.

The candidate contribution should therefore be stated as a precise
complexity extension assembled from established ingredients. Calling the
coordinate split, parametric-QP charts, algebraic radius theorem, or
one-quadratic FPT oracle individually novel would be unsupported. A
publication-level novelty assessment still needs broader citation-chain
review, especially in structured convex programming and implicit
semialgebraic optimization.

## 6. Search and verification record

Searches on 2026-09-28 covered common range/common kernel, low-rank
constraints, few nonlinear variables, nonlinear aggregate coordinates,
implicit convex programming, partial separability, convex polynomial
perturbations, parametric QPs, and exact FPT quadratic or conic
optimization. Searches of the local literature index and full texts
located the parametric-programming and low-rank objective comparators.
Search snippets served only as discovery aids.

The exact primary sections inspected are identified above. The local
Scott--Geunes source is
`literature/papers/geunes2025-a-normal-fan-projection-algorithm/fulltext.md`.
The local Tøndel, Bemporad, and Avraamidou collections were supplied to a
separate parametric-QP subauditor, who identified the stronger primary
Spjøtvold and Patrinos sources; this auditor then inspected their relevant
sections independently. Both noticed the Patrinos properness issue.
Zhao--Fan's *On subspace properties of the quadratically constrained
quadratic program* was searched again; the publisher's full-text link
required access, so its abstract was not used to exclude overlap.

No mathematical implementation was changed or tested. An inline
`python3` document check passed for this note's final newline, whitespace,
control characters, and two local Markdown links. It does not establish correctness
or novelty. No project-wide verification or CI inspection was performed.
