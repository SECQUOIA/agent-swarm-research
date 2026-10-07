# Attribution and the boundary of completion

Checked on 2026-10-03. This continuation closes specified mathematical and
implementation contracts. It does not establish a first joint
convexification method or make the whole research area complete.

The [previous audit](../../research-20261002-convexification/literature/README.md)
and its [23-source ledger](../../research-20261002-convexification/literature/sources/MANIFEST.md)
remain the provenance for inherited simultaneous-convexification,
Bernstein, star, moment, and native-SCIP claims. The bibliography here
retains those entries and adds the primary sources needed for the new
arguments. Sources not re-read are not presented as newly verified.

| Addition | Established basis | Claim justified by this continuation |
| --- | --- | --- |
| Direct original-variable cuts | Weak Lagrangian duality and convex separation | A native-preserving cut interface with explicit source binding and replay |
| Closure of all aggregate support rows | Support representation of a closed convex set and projection of a joint graph relaxation | A self-contained characterization of the precise relaxation expressed by the interface |
| Final machine-row correction | Safe bound-assisted rounding and exact aggregation | Validation of the actual inserted row; the proof permits a sufficient one-sided bound, while the current exporter requires both finite bounds for a changed coefficient |
| Quadratic support in fixed small dimension | Classical face stationarity and rational quadratic-programming certificates | Exact rational enumeration, degeneracy handling, resource bounds, and checked implementation |
| Positive-tolerance graph separation | Classical support/separation duality and finite approximation | A stated finite algorithm with a verifiable answer or explicit resource exhaustion |
| Broad usefulness to solvers | Requires computational evidence against existing solver facilities | Only the effects demonstrated by the frozen comparative experiments |

The [aggregation audit](aggregation-prior.md) identifies the direct
Lagrangian, rounding, and related quadratic aggregation precedents. Its
distinction between nonlinear aggregation and redundant aggregation of
already linear rows matters for the method's practical interpretation.

## Exact quadratic support is classical structure

[Murty's Internet edition (1997), Section 2.9, pp. 163–166](https://public.websites.umich.edu/~murty/books/linear_complementarity_webbook/kat2.pdf)
directly develops bounded general quadratic optimization by face
enumeration, including reduction of equality and universally binding
constraints. Page 166 credits earlier work by Mueller and Murty.
The author's catalog identifies the original 1988 book; the Internet
edition's cover is dated 1997. These passages were inspected in the
author-hosted chapter PDF. This is a direct precedent for the algorithmic
principle. Our nonsingular-system enumeration and its complete replay
contract are a specific realization, not a new face-enumeration theorem.

[Vavasis (1990)](https://www.sciencedirect.com/science/article/pii/002001909090100C),
*Quadratic programming is in NP*, Information Processing Letters 36(2),
73–77, DOI 10.1016/0020-0190(90)90100-C, establishes polynomial-size
certificates for rational quadratic programming. The publisher abstract
and metadata were checked; the complete proof was not retrieved in this
continuation. The present note proves its own restricted active-face
enumeration argument rather than treating an unread proof as verified.

For fixed dimension, enumeration over active-row subsets is polynomial
in the number of rows; allowing dimension to grow changes that cost.
Rational stationary points of nonsingular bordered systems and the
minimal-face argument are not new optimization principles. The earlier
[Anstreicher–Burer audit](../../research-20261002-convexification/literature/README.md)
already records exact low-dimensional quadratic graph representations.
The extension here should be described as a complete implementation of
an explicit support class, not a newly discovered tractable class.

## Support and separation are established dual problems

[Grötschel, Lovász and Schrijver (1981)](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1981a.pdf),
*The ellipsoid method and its consequences in combinatorial optimization*,
Combinatorica 1(2), 169–197, Theorem 3.1, establishes polynomial
equivalence of weak optimization and weak separation in its encoded
convex-body model. Page 172 states the supplied inner and outer ball
assumptions; these must not be silently discarded when applying that
theorem. The relevant passages on pp. 171–178 were inspected. The
[1984 corrigendum](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1984c.pdf)
addresses the later submodular-set-function result, rather than Theorem
3.1; its first-page statement was checked.

The continuation uses a simpler finite-net proof over a compact graph
hull. Its bound on the support function's change with direction and its
verified lower/upper support bounds imply a positive-tolerance answer.
It does not need a full-dimensional graph hull or an inner ball. This
is a direct elementary construction, not a new general equivalence
theorem or a polynomial-time substitute for the ellipsoid method.
The normal net can be exponentially large in the number of graph
coordinates, and its dependence on tolerance is not polynomial in the
bit length of that tolerance. These costs remain part of a claim of
algorithmic completeness.

The answer contracts must also remain distinct. A rational separating
row, a proof that the query is within a stated distance of the hull,
and an unresolved budget stop are different outcomes. Positive-distance
tolerance is not exact membership. A bounded solver cut loop is not the
same algorithm as the complete finite-net fallback. A rational row may
need separate rounding before it becomes an effective binary64 cut.

## An explicit hardness boundary

General quadratic support over a box already contains weighted maximum
cut. Let \(G=(V,E)\) have nonnegative integer weights \(w_{ij}\), and set

\[
 q(x)=-\sum_{\{i,j\}\in E}w_{ij}(x_i+x_j-2x_ix_j),
 \qquad x\in[0,1]^{|V|}.
\]

The function is affine in each coordinate separately. Given a minimizer,
move one coordinate at a time to a minimizing endpoint while fixing the
others; the objective never increases. Thus a binary minimizer exists.
At a binary point, \(x_i+x_j-2x_ix_j\) is one exactly for a cut edge.
Consequently

\[
 \min_{x\in[0,1]^{|V|}}q(x)=-\operatorname{MaxCut}(G,w).
\]

The reduction is explicit and polynomial in its input encoding.
[Karp (1972)](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf),
*Reducibility among Combinatorial Problems*, lists weighted MAX CUT as
problem 21 of its completeness theorem, original pp. 94 and 97, and
gives the PARTITION reduction on p. 100. These passages were inspected
in the author-identified 2010 reprint of the original paper. Therefore
an unrestricted polynomial-time exact quadratic support algorithm would
imply P = NP. Merely representing the quadratic graph by coordinates
does not remove the hard optimization problem.

This boundary does not make all unsolved extensions impossible.
Special graphs, constraints, signs, parameters, approximation contracts,
and useful heuristics can still give stronger results. It rules out an
unqualified tractable completion of general exact support under the
usual complexity assumption. Fixed-dimensional and constrained-star
algorithms are valuable precisely because their hypotheses identify
classes outside this unrestricted claim.

## How to state completion accurately

A theorem can completely characterize a specified class. An algorithm
can implement that theorem, distinguish refusal from success, and have
its certificates and experiments checked. A research package can close
all its declared implementation and evaluation tasks, including a
negative performance finding.

None of those statements proves that further useful research cannot
exist. In particular, native-preserving aggregation can eliminate an
unhelpful reformulation while still have unhelpful cut overhead. Exact
support can coexist with expensive direction search. Complete graph
separation can coexist with a graph relaxation strictly weaker than the
original feasible-set hull, as the explicit example in
[row-aggregation.md](../theory/row-aggregation.md) shows.

The final report should say exactly which contracts and evidence are
complete, state the measured deployment recommendation, and leave these
mathematical distinctions intact. This audit is a targeted primary-source
comparison; it is not an exhaustive priority search and supplies no
publication-novelty certificate.

## Targeted checks

The 34-entry bibliography passed a standalone `bibtex refs` parse using
a temporary auxiliary file that cited all entries and the `plain` style.
The entry-key count was 34, with no duplicates. Download hashes and the
project-local ignore rules were checked. The
[independent proof review](row-proof-review.md) found no unresolved issue
in the row theorem or its final-row correction and records 1,224 exact
rounding diagnostics. These are topic-specific checks; no project-wide
verification or CI inspection was performed.
