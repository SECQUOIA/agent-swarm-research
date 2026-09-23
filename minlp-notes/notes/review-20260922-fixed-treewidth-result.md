# Integrated review of exact smoothed fixed-treewidth messages

Date: 2026-09-22. Reviewer: a fresh independent agent.

## Verdict and scope

I found no substantive gap in the theorem or its proof in
[the consolidated result](../results/smoothed-fixed-treewidth-indicator-dp.md).
The proof establishes an exact algorithm for every sampled rational instance,
with polynomial expected bit complexity under the fixed numerical and width
assumptions. It constructs the full conditional value functions, represented
as lower envelopes of rational support quadratics, for every boundary mode
of the reduced rooted decomposition.

Two presentation clarifications should be made:

- The input-length dependence includes the encoding length of the rational
  noise scale `sigma`. Dependence on `1/sigma` alone cannot account for an
  arbitrarily long rational encoding. The proof already uses the full
  rational input length, so this changes no argument.
- Say explicitly that the messages belong to the reduced decomposition
  after the stated contractions. The proof does not output an additional
  dictionary for every redundant bag in an arbitrary supplied decomposition.

This is a correctness review, not a proof of publication priority. I read
the constituent reviews but independently checked the integrated argument,
including its extension from width two to arbitrary fixed width. I did not
edit the result file.

## Ownership, domains, and support semantics

The highest-bag assignment is consistent. Bags containing a vertex form a
connected subtree. Bags containing both endpoints of an edge also form a
connected subtree. If both endpoints lie in the parent separator, the
parent itself contains them, so their term is owned strictly above the
current subtree. If a vertex is internal, its incident terms cannot be
owned above that subtree. Thus the message contains exactly the internal
terms and the interactions with its separator; no separator-only term is
accidentally counted or omitted.

After contracting adjacent contained bags, each nonroot bag has a vertex
absent from its parent. Such a vertex has that bag as its unique highest
occurrence. Distinct bags therefore admit distinct assigned vertices. A
nonempty root admits one too, giving at most `n` bags. Nonroot separators
have size at most `w`, because otherwise a bag of size at most `w+1` would
be contained in its neighbor.

Every fixed internal support is a strictly convex quadratic minimization
in its free variables. The coordinate maximum argument works with any
number of boundary coordinates and with arbitrary internal support. It
depends only on the original row bounds, not on diagonal dominance of an
intermediate Schur complement. Consequently all conditional minimizers
stay in the same box, and the branch derivative contains only internal
cross terms. The stated Euclidean Lipschitz bound follows coordinate by
coordinate, without a hidden subtree-size factor.

An active indicator permits a zero continuous value. The separate boundary
modes and unrestricted fixed-support elimination respect this distinction.
Negative penalties therefore cause no inconsistency. Internal bits receive
their own independent perturbations; boundary penalties do not appear in
the message and cannot spoil the probability conditioning.

## Atomic moment bound and constants

The shattering argument does not assume independence of winner gaps.
Conditioning outside a proposed shattered set fixes every pattern-class
minimum. Comparing the zero pattern with each unit pattern then restricts
different remaining noise coordinates to fixed intervals. Independence of
these coordinates justifies the product bound, including the grid atoms.

The Sauer--Shelah estimate and the coarse tail sum give
`E |A_delta|^p <= exp[m(m+1)^p(2 phi delta + 1/N)]`.
With the theorem's global choices and `m <= n`, the continuous contribution
to the exponent is at most `1/2`, and the atomic contribution is at most
`1/2`. This includes exact ties and repeated support formulas.

Partitioning each parameter interval into
`ceil(2 M L sqrt(k)/delta)` pieces supplies the stated covering radius
`delta/(2 L)`. The midpoint net has the claimed cardinality. A support
minimizing anywhere is within `delta` of optimal at a nearby net point;
this follows from two Lipschitz inequalities. Convexity bounds the moment
of the union count without any independence among parameter points.
The cases `m=0`, `k=0`, and `L=0` are handled separately and correctly.

The bound concerns support counts, not connected winning regions. It is
therefore compatible with arbitrary Lipschitz functions in the probability
lemma. Polynomial structure enters later, when constructing the dictionary.

## Deterministic construction in general fixed width

At a bag, every child separator is contained in the bag. After fixing all
bag indicators, each child contributes polynomials in at most `w+1` active
bag coordinates. Pairwise comparisons within each dictionary suffice to
determine its minimizers on a sign-invariant cell. The construction need
not enumerate the Cartesian product of child dictionaries. Even arbitrarily
many children contribute only polynomially many comparison polynomials in
their total dictionary size, followed by fixed-dimensional CAD.

The potentially delicate case is an optimizer at a box boundary or at a
multiple switching intersection. After zero polynomial differences are
discarded, full-dimensional arrangement cells are dense in the relative
box. A sequence approaching the optimal bag point has a subsequence using
one child tuple. Continuity makes all formulas in that tuple attain their
child values at the target point. Changing separator coordinates along
the approaching sequence is harmless because the tuple supplies full
polynomials, not formulas restricted to the sampled cell.

The tuple represents a consistent complete support: different child
interiors are disjoint and have no cross edges. Its remaining forgotten
variables have a positive definite Hessian, obtained by partial elimination
of a principal submatrix of the original positive definite matrix. Its
unrestricted minimum is a valid fixed-support value at every separator
point. At the target point it is no greater than the true optimal value
by the selected tuple, and no smaller by feasibility. This proves exact
coverage even when the optimum lies only on a lower-dimensional set.

Pruning does not require retaining every tied support. After duplicate
polynomials are merged, unique-minimizer points are dense because finitely
many nonzero polynomial zero sets have empty interior. Retaining formulas
that win on full-dimensional cells therefore preserves the envelope by
continuity. The zero-dimensional case needs only one minimum constant.

These arguments do not use planar topology and extend to every fixed bag
dimension. The CAD degree can grow substantially with width, but remains a
constant for fixed width. Thus one computable exponent `a(w)` bounds all
cell construction, candidate generation, pruning, and support bookkeeping.

## Rational arithmetic and expected running time

Every stored candidate is the exact Schur expression of a complete support
of the original rational instance. Clearing denominators and applying
determinant bounds therefore gives a polynomial coefficient-length bound
uniform in the support. This avoids an unsupported inference from the number
of arithmetic operations alone. Summing at most `n` child expressions and
eliminating at most `w+1` variables also preserves polynomial intermediate
bit length when rationals are reduced.

CAD sample points decide which rational formulas to retain. They do not
become coefficients of subsequent formulas. Recursive message construction
therefore does not accumulate nested algebraic extensions. The root support
and its continuous optimizer are recovered with rational linear algebra.

The deterministic bound is polynomial in the sum of final dictionary sizes,
even if a bag generates substantially more candidates than it retains:
candidate work is already bounded polynomially in its children's retained
sizes. The chosen `p >= a(w)` then supplies the required moment. The final
convexity inequality applies to the sum of all dictionary sizes and needs
no independence between messages sharing noise. Selecting this fixed `p`
before drawing noise is not circular; it only determines the polynomial
grid size needed by that deterministic algebraic algorithm.

The grid uses `O_w(log(n+1))` bits per coordinate and always produces exact
rational input. Correctness holds for every outcome, including rare outcomes
with exponentially large dictionaries. Only the running time is averaged.

## Significance and source checks

The all-message conclusion is stronger than returning one optimizer in
output capability: it gives exact conditional functions throughout their
boxes and all boundary modes. This distinction does not itself establish
novelty or rule out obtaining those functions by a different oracle method.
The result correctly acknowledges the optimizer-only adaptation of older
smoothed methods, the classical additive comparison, and the absence of a
practical CAD speedup claim.

I opened the primary
[Arnon--Collins--McCallum CAD paper](https://www.lacl.fr/pvanier/cours/2015-2016/lm/articles/Cylindrical%20Algebraic%20Decomposition%20I-%20The%20Basic%20Algorithm.pdf).
Its introduction states polynomial computation time for fixed variable
dimension; its construction specification supplies sign information and
exact sample points. These are precisely the algebraic capabilities used
here. No new CAD theorem is needed.

I also opened [Röglin--Teng, FOCS 2009](https://www.roeglin.org/publications/FOCS09.pdf),
especially Section 6.2 and Theorem 6.2. They already give expected smoothed
algorithms from randomized pseudopolynomial binary linear optimization and
discuss polynomial-bit rounding. The result's warning against claiming
these general ideas as new is appropriate. Its treatment of shared random
penalties, nonlinear deterministic support costs, and complete conditional
functions still needs a dedicated priority comparison. This limited source
audit neither establishes nor disproves novelty of the consolidated result.

## Verification record

This review consists of direct proof checking and the two primary-source
reads above. I did not rerun the existing scalar-envelope, branching-bag,
or finite-distribution computations, and do not claim their executions as
new checks. No additional computational experiment is needed to test the
dimension-independent logical steps reviewed here. A targeted inline Python
scan of this review note's local Markdown links and trailing whitespace
passed. I did not run Lean,
project-wide checks, or CI inspection. The proof remains a mathematical
argument reviewed by humans and agents, not a formal verification.
