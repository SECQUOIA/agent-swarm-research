# Stage 3 universality repair guidance

Two reviewers independently identified a valid major issue: the broad rational
universality claim inherits a false Boolean normal-form step from Dynamic Toolbox
Lemma A. Root agrees after reading the original proof. Read reviewer 1 and 4's
stage03-round01 reports before correcting. Also fix reviewer 3 and 4's minor
D-neighbor wording error: D has one complemented x copy with conductance 2 and
one complemented y copy with conductance 1.

## Correct positive statements

1. Every compact **basic closed** semialgebraic set over Q is rationally
   equivalent to a bounded ETR-INV set with affine coordinate recovery, hence
   to our structured network. Start with conjunctive polynomial equalities
   and weak inequalities. Introduce unique polynomial-value slack variables
   for inequalities, then audit and use the conjunction-only source chain
   C–G. Compactness is preserved by unique polynomial graphs. Arbitrarily
   small rational scaling can be chosen for this existence result, avoiding
   reliance on a particular source radius bound or a new complexity claim.
   Reviewer 1 audited C–G and flagged harmless source typos in Lemma 17 and
   a missing auxiliary center 7/4−delta in E. Inspect the actual gate formulas
   and explain enough to justify the valid restricted arithmetic lemma.
   The singleton algebraic theorem should use that restricted lemma.

2. Every compact semialgebraic set is **homeomorphic** to one of our structured
   voltage sets. Finite triangulation gives an abstract finite simplicial
   complex K. Realize K in the standard simplex by z_i>=0, sum z_i=1, and
   product_{i in F} z_i=0 for each nonface F. These rational constraints are
   basic closed and compact; permitted supports are exactly the faces of K.
   The usual barycentric map gives a piecewise linear homeomorphism to any
   geometric realization of K. Apply statement 1 to this standard realization.
   No rational homeomorphism from the original arbitrary set is claimed.
   No polynomial-size triangulation or nonface enumeration claim is needed.

A checked primary triangulation source is Ohmoto–Shiota, *C1-triangulations
of semialgebraic sets*, arXiv:1505.03970v2, Theorem 1.1 on p.2. Section 1.2
explicitly says that the complex is finite for compact X; standard triangulation
is recalled in Theorem 2.2 on p.4. The PDF and extracted text are cached as
`build/source-cache/ohmoto-shiota-triangulation.{pdf,txt}`, with receipt
`process/root-triangulation-source.json`. A classical source may be used instead
if independently verified. Coste's author PDF returned 403 and was not relied on.

## Sharp boundary for rational equivalence

Root's following argument was sanity-checked by reviewer 1. Let compact S be
rationally equivalent to basic closed T via F:S→T and G:T→S. The given rational
coordinate denominators are nonzero on their respective domains. For nonempty
S, collect all forward denominator polynomials. For each denominator of G,
substitute F and clear forward denominators without cancellation; add the
resulting numerator polynomial to the collection. Every polynomial in this
finite collection is nonzero on S. Compactness gives a rational delta>0 below
all their absolute values on S.

Define S' by the conditions that these polynomials have squared values at
least delta², F(x) belongs to T, and G(F(x))=x. The denominator conditions make
all rational expressions defined on S'. Clearing denominators by positive
multipliers turns target weak inequalities into polynomial weak inequalities
and inverse identities into polynomial equalities. Thus S' is basic closed,
over Q when F, G, and T are over Q. Construction gives S⊂S'. Conversely,
x∈S' implies F(x)∈T and x=G(F(x))∈S. Therefore S'=S. The empty set is
already basic closed.

This yields a sharp characterization: among compact semialgebraic sets over Q,
precisely the basic closed sets are rationally equivalent to RPF voltage sets.

An explicit counterexample to the broader claim is
S=[−1,1]^2 intersect ({x>=0} union {y>=0}). This set is not locally basic
closed at the origin. Any polynomial equality valid on its open quadrants is
identically zero. For a nonzero polynomial p nonnegative on its three
quadrants, the lowest nonzero homogeneous term H is nonnegative on those
directions. Its degree cannot be odd: the second and fourth quadrants both
belong to S and are negatives of each other, which would force H to vanish
on an open set. Thus its degree is even. Since S contains at least one of u
and −u in every direction, H is nonnegative in every direction. Choose a ray
in the lower-left quadrant avoiding the finitely many zero directions of all
leading terms in a proposed finite conjunction. Along that ray sufficiently
near zero, every polynomial is positive, contradicting its exclusion from S.

The closure proposition and explicit counterexample would make the boundary
complete and explain why the old source claim cannot simply be reproved.

## Integration

Correct all related abstract, README, coverage, and later introduction claims.
Keep the full topological conclusion with the correct type of map. Credit
bounded arithmetic and triangulation, and explain the Boolean normal-form
pitfall in a precisely scoped remark or appendix if needed. Keep the paper
centered on power flow while supplying the necessary mathematical justification.
Stage 3 requires five fresh reviews after correction because the finding is major.
