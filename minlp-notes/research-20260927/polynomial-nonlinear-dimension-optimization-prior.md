# Prior audit: exact optimization with few nonlinear polynomial directions

Date: 2026-09-28. This is a source and scope audit for the developing full
optimization extension of
[the polynomial feasibility theorem](polynomial-nonlinear-dimension-frontier.md).
It supplements the [feasibility prior audit](polynomial-nonlinear-dimension-prior.md).
It does not verify the full optimization proof or establish priority.

The main correction is that a finite infimum in the proposed class is
always attained, by an older mixed-integer theorem. The potential advance
is the exact Turing complexity and output bound for an arbitrary linear
continuous extension of a polynomial model with few nonlinear directions.
Exact optimization in fixed dimension, implicit separation, and the
existence of mixed-integer minimizers all have substantial precedents.

## Model being compared

The proposed input is

\[
 \min\{C_0v+p_0(z,u): C_iv+p_i(z,u)\leq0,
          \ i=1,\ldots,m,\quad z\in\mathbb Z^k,
          \quad u\in\mathbb R^r,\quad v\in\mathbb R^n\}.
\]

All coefficients are rational, every `p_i`, including `p_0`, is globally
convex in the joint real variables `(z,u)`, and their degrees are at most
`d`. The matrices `C_i` are constant. Coefficients and monomials are
explicitly encoded with total bit length `N`. The proposed bound is
`f(k,r,d) N^C` for an absolute constant `C`, with no supplied box or Slater
point. The intended finite output includes an exact algebraic value and
an optimizer represented over one real number field.

The objective must be included when identifying the common nonlinear
directions. Adding an objective with nonlinear dependence on the discarded
`v` coordinates changes the parameter. The number of rows and the number
of linear continuous coordinates are unrestricted. This distinction is
essential when comparing against algorithms parameterized by total
dimension.

## Finite attainment is already known, including mixed integers

Bank and Mandel, *Nonlinear parametric integer programming*, 1987,
pp. 16–48, provide the stronger relevant result. In the
[primary publisher preview](https://api.pageplace.de/preview/DT0400.9783112720936_A50662169/preview-9783112720936_A50662169.pdf),
the model on p. 18 uses globally quasiconvex polynomials. Theorem 3(iii),
p. 24, gives an integer-generated recession cone for rational coefficients.
The stable subsystem on p. 34 retains a subfamily of those polynomials.
Its recession cone therefore also has this property, which implies the
mixed-integer generation assumption in Theorem 7(ii). That theorem makes
the feasible right-hand-side domain closed. It does not require the
compact-plus-cone assumption used for a different model in that chapter.

Append the objective as one more inequality. Feasible right-hand sides
with objective coordinates decreasing to a finite infimum converge to
the right-hand side containing that infimum. Closedness gives a feasible
optimizer. Thus the proposed rational globally convex-polynomial class
has only three statuses: infeasible, unbounded below, or finite and
attained. This holds without fixed dimensions or degree.

The earlier [mixed-integer attainment audit](mixed-integer-attainment-prior.md)
records the same deduction. This audit independently checked the standing
definitions and visually read Theorems 3 and 7. Their published statements
are accessible; the preview omits the proof of Theorem 7.

For continuous variables, Belousov and Klatte,
[*A Frank–Wolfe Type Theorem for Convex Polynomial Programs*](https://link.springer.com/article/10.1023/A:1014813701864),
Computational Optimization and Applications 22 (2002), 37–48, state in
their publisher abstract that a convex polynomial bounded below on a
nonempty set defined by convex polynomial inequalities attains its minimum.
They credit Belousov's 1977 book. The full 2002 article was not available
in this audit, so no internal theorem number or additional assumption is
attributed to it. Bank–Mandel supplies the directly inspected
mixed-integer result needed here.

An algorithm that handles nonattainment for a broader semialgebraic class
can still be used internally. Its broader capability should not suggest
that nonattainment occurs under the displayed model's assumptions.

## The strongest algorithmic comparisons

**Hildebrand–Köppe already give exact FPT integer polynomial optimization.**
Their
[*A new Lenstra-type Algorithm for Quasiconvex Polynomial Integer Minimization with Complexity 2^O(n log n)*](https://arxiv.org/abs/1006.4661),
Theorem 1.1, treats explicitly listed quasiconvex polynomials in integer
variables, including the objective. Its unbounded-input running time is
`s l^O(1) d^O(a) 2^O(a log a)` in total integer dimension `a`, row count
`s`, and coefficient length `l`. Their proof already combines a small
optimal-point bound with objective bisection. This is a direct predecessor
for exact optimization, not just feasibility. The proposed extension must
account for continuous algebraic output and an implicit family of
projected polynomials; merely adding objective bisection is not a new
algorithmic principle. Theorem 1.1 and its proof were read from the saved
primary text.

**A published folklore statement already includes mixed integers.**
Gavenčiak, Knop, and Koutecký,
[*Integer Programming in Parameterized Complexity: Three Miniatures*](https://arxiv.org/pdf/1711.02032),
Appendix A.1, printed p. 21, say that the cited convex integer results do
not explicitly treat mixed integers, but that their FPT extension is
folklore. The paper's original arXiv title was *Applying Convex Integer
Programming: Sum Multicoloring and Bounded Neighborhood Diversity*.
The surrounding discussion distinguishes polynomial descriptions,
semialgebraic descriptions, and oracles. It does not supply the exact
algebraic-output and uniform precision theorem for arbitrarily many
linear continuous coordinates considered here. Nevertheless, claims of a
first mixed-integer convex-polynomial FPT algorithm would need to address
this statement rather than ignore it.

**Khachiyan–Porkolab provide size bounds independent of predicate count.**
In
[*Integer Optimization on Convex Semialgebraic Sets*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
Theorem 1.1 bounds an optimal integer point of a convex first-order
description. Its bound depends on degree, coefficient length, and free
and quantified dimensions, independently of the number of predicates.
Theorem 1.2's algorithm has a predicate-count exponent depending on
dimension. Corollary 2.3 also provides exact real algebraic samples and
common-field encodings, with degree and coefficient bounds independent
of predicate count but runtime dependent on it. These are strong
predecessors for both size and output arguments. They do not make an
exponentially long Farkas projection computationally free. Theorem 1.1
optimizes an integer coordinate; it does not directly return an arbitrary
real-valued mixed-integer optimum after continuous elimination. The
displayed statements on pp. 208 and 211–212 were inspected.

**Implicit convex optimization is an older subject.**
Norton–Plotkin–Tardos,
[*Using separation algorithms in fixed dimension*](https://ecommons.cornell.edu/server/api/core/bitstreams/36e75f7f-421a-43aa-b069-052b4c6850d7/content),
Theorems 2.3–2.4 and 3.1, optimize from suitable affine-comparison
separation algorithms and already avoid explicit LP projection. Toledo,
[*Maximizing Non-Linear Concave Functions in Fixed Dimension*](https://www.tau.ac.il/~stoledo/Pubs/concave.pdf),
Theorem 4.4, extends this to a restricted polynomial-comparison model.
Its generic sequential bound has a dimension-dependent exponent.
However, its explicit-row application in Section 5 has arithmetic bound
`O(m (log m log log m)^(2^a-1))`. Such logarithmic powers can be absorbed
into a parameter factor times a fixed power of `m`; this application
should not be described as an FPT obstruction. The remaining comparison
issues are the RAM model, control of exact bit operations, and whether
the LP evaluation routine meets the special comparison restrictions.
An arbitrary polynomial-time LP routine is not automatically admissible.
The primary definitions, Theorem 4.4, and Section 5 were reread.

**Oracle reductions already give exact optimization with exact oracles.**
Oertel–Wagner–Weismantel,
[*Integer convex minimization by mixed integer linear optimization*](https://orca.cardiff.ac.uk/id/eprint/86766/1/IntegerConvexMinRev4.pdf),
Theorem 1 and the following discussion, assume a known integer box and
first-order evaluation oracles of prescribed accuracy. Their method
returns exact optimization when the function-value error is zero. The
paper discusses extension to mixed integers through sufficiently accurate
continuous minimization. This supports decomposition as an established
approach. It does not furnish the required unbounded-input radius,
algebraic output, or implementation of the precise oracles for the
displayed model. The primary theorem and its exact-oracle discussion were
inspected.

**Slot–Steurer–Wiedmer are stronger for a continuous objective over a
polyhedron.**
[*Hesse's Redemption: Efficient Convex Polynomial Programming*](https://arxiv.org/abs/2511.03440),
Theorem 1.1 and Corollary 1.2, give polynomial-size solution bounds and
polynomial-time arbitrary-accuracy optimization of a convex polynomial
over a rational polyhedron, in variable dimension. Their Theorem 1.3
also gives an effective rational decomposition into affine directions
and a polynomial with a controlled strongly convex quadratic lower
bound. Their encoding uses unary multi-indices. These results do not
cover arbitrary families of convex polynomial inequalities or exact
algebraic optimizer output. They do establish that identifying and
removing affine directions, and obtaining effective bounds in a large
linear model, are not new principles. The saved primary theorem
statements and input model were inspected; the arXiv record was checked.

The publisher abstract of Bank–Heintz–Krick–Mandel–Solernó,
[*Computability and Complexity of Polynomial Optimization Problems*](https://link.springer.com/chapter/10.1007/978-3-662-02851-3_1),
1992, also gives earlier quasiconvex integer solution-size bounds. The
full chapter was not obtained, and no stronger matching algorithm is
inferred from its title or abstract. The later Khachiyan–Porkolab and
Hildebrand–Köppe statements above are directly accessible and more useful
for the present comparison.

## Boundaries that the statement must preserve

Global convexity of the defining polynomials is stronger than convexity
of the feasible set. For example,

\[
 S=\{(x,y):x\geq0,\ y\geq0,\ xy\geq1\}
\]

is closed, convex, rationally semialgebraic, and SOC representable. The
infimum of `x` is zero and is not attained. Its native row `1-xy` is not
globally convex. This example cannot contradict Bank–Mandel or the
proposed polynomial theorem. It also shows why results for general SOC
or convex semialgebraic representations can require a nonattainment
case that the present model excludes.

Rational coefficients matter for mixed-integer attainment. With
`z,w` integer, minimize `w-sqrt(2)z` subject to `z>=1` and
`w-sqrt(2)z>=0`. All functions are affine, but the coefficients are
irrational. Every feasible objective is positive. Positive Pell pairs
`w^2-2z^2=1` give

\[
 w-\sqrt2z=\frac1{w+\sqrt2z}\longrightarrow0,
\]

so the infimum is not attained. This is an elementary boundary example,
not a novelty claim.

Exact output need not be rational, even with no constraints and one
nonlinear coordinate. The globally convex objective `x^4-2x` has unique
minimizer `x=2^(-1/3)` and value `-3x/2`. An exact theorem must therefore
specify an algebraic representation, not promise rational optimizers.
The existence of one algebraic point of bounded encoding does not alone
give an algorithm that finds it within the same bound.

The proposed parameter counts the common nonlinear continuous
directions of all rows and the objective. It is not interchangeable with
the number of nonlinear rows, a sum of individual row ranks, Hessian
matrix span, or the number of variables in each individual polynomial.
Adding a quadratic norm in every linear coordinate may increase this
parameter; a recovery argument using such a norm must independently
justify its complexity or avoid that increase.

## Assessment and verification record

The defensible candidate is a uniform exact bit-complexity theorem for
convex polynomial models with a large linear continuous part. Its useful
content would be that precision, integer bounds, and exact algebraic
recovery can be controlled by `(k,r,d)` while the exponent of total input
size remains absolute. This could support exact certification and
decomposition for a few nonlinear aggregate variables coupled to a large
linear network. Useful constants, stable implementations, and computational
advantages remain to be established.

The result should not be presented as a new existence theorem, a new
Lenstra algorithm, a new general algebraic-sampling theorem, or the first
fixed-dimensional mixed-integer convex optimization method. Searches did
not locate a primary theorem that explicitly combines all the proposed
assumptions and outputs. This does not establish novelty. In particular,
the published folklore statement warrants further comparison before a
priority claim.

Searches covered convex-polynomial attainment, Bank–Mandel,
Belousov–Klatte, mixed convex polynomial exact optimization, few nonlinear
variables, partially linear polynomial programming, linear extensions,
and parameterized integer convex optimization. Sources already checked
in the feasibility audit were reused only with their stated scope;
selected primary passages were reread as identified above.

New local source copies are
`polynomial-dimension-prior-sources/bank-mandel-1987-preview.{pdf,txt}`
and `polynomial-dimension-prior-sources/gavenciak-knop-koutecky-1711.02032.{pdf,txt}`.
The Bank–Mandel PDF was converted with `pdftotext -layout`; printed
pp. 24 and 34 were rendered with `pdftoppm` and inspected visually.
Font metadata warnings did not prevent extraction or rendering. A failed
web screenshot was replaced by those local renders. These checks verify
the source statements and their application, not the omitted original
proof or the developing algorithm.

Targeted document checks covered final newline, trailing whitespace,
control characters, and local Markdown links in this file. No project-wide
verification, CI inspection, numerical experiment, or Lean formalization
was performed for this audit.
