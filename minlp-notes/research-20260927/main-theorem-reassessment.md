**Reassessment of the exact unbounded Hessian-span theorem**

Date: 2026-09-27. This is a fresh assessment of the current package, including
the ordered optimizer construction and the multihomogeneous degree refinement.
It is a source comparison and a selective proof audit, not another complete
verification of every dependency or a publication-priority determination.

The stronger headline is a substantial candidate result: exact optimization
of rational jointly convex quadratic systems in polynomial Turing time for
each fixed integer dimension `k` and continuous constraint-Hessian matrix-span
dimension `h`, with arbitrarily many continuous variables and rows, no supplied
bounds, and no Slater condition. It includes exact status classification and
an algebraic optimizer. I found no direct older theorem that supplies this
parameterization without an additional reduction. The strongest new content
remains the active affine restriction and its use to control algebraic
precision and projection formulas. The result combines classical tools in a
way that reaches a broader exact class; it does not supply a new general
algebraic optimization method.

This assessment read [the synthesis](hessian-span-main-results.md),
[the unbounded mixed-integer theorem](mixed-integer-attainment-frontier.md),
[the projection construction](unbounded-integer-frontier.md),
[the ordered optimizer proof](ordered-perturbation-optimizer.md),
[the degree refinement](multihomogeneous-span-degree.md), and the existing
prior audits. Two delicate proof chains were independently reconstructed
below. No substantive gap was found in those chains. This finding is narrower
than certifying the entire package.

The precise headline matters. All full mixed-integer constraint and objective
Hessians must be PSD; `h` counts only native continuous constraint blocks.
The objective is excluded from that count, although a threshold query can add
one direction. Polynomial time for each fixed `(k,h)` is an XP-type guarantee,
not an FPT guarantee. Exact algebraic output is necessary in the stated class.
The bounded MILP projection result preserves integer assignments; its displayed
continuous coordinates need not solve the original constraints. Removing
input bounds for optimization does not give a finite MILP preserving every
unbounded integer assignment. These are substantive boundaries, not cosmetic
qualifications.

The current synthesis still states valid, weaker optimizer-coordinate bounds
from the earlier recovery proof. The ordered construction improves their
degree and height to `N^{O(h+1)}`, and the new degree note gives the sharper
common-field bound

\[
 [\mathbb Q(x^*,q_0(x^*)):\mathbb Q]
 \le \max_{0\le s\le\min(h,n)}2^s\binom ns.
\]

That refinement can replace the weaker representation bounds after its own
review is complete. It does not by itself improve every composed algorithm's
running-time exponent. The maximum over support sizes must remain: the
binomial expression need not increase with `s`.

**Older results and possible direct subsumption.** The prior attribution to
Grigoriev--Pasechnik, Nie--Ranestad, Bank--Mandel, Khachiyan--Porkolab, Del Pia,
and Kocuk is appropriate. This pass additionally checked the following
potential shortcuts rather than treating an unsuccessful title search as
evidence of novelty.

- [Khachiyan--Porkolab, *Integer optimization on convex semialgebraic sets*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
  Theorems 1.1--1.2, printed pp. 208--209, and Proposition 2.1, p. 211,
  are the strongest general transfer theorem here. The small integer-witness
  bound depends on atom degree, coefficient bits, free dimension and quantified
  block dimensions, but not the number of atoms. The algorithm's time bound
  does depend on the number of atoms. Therefore a possibly enormous compressed
  formula can legitimately prove a small witness without being an efficiently
  generated input to their algorithm. Applying their theorem directly to the
  original `exists x` description leaves the unbounded continuous dimension
  in the exponent. The compressed formula is doing essential additional work.
- [Oertel--Wagner--Weismantel, *Integer convex minimization by mixed integer linear optimization*](https://orca.cardiff.ac.uk/id/eprint/86766/1/IntegerConvexMinRev4.pdf),
  Theorem 1 and the introductory assumptions, gives an older exact
  oracle-polynomial reduction in fixed integer dimension. It assumes a known
  integer box and sufficiently accurate first-order evaluation oracles for
  the functions in the integer variables; with exact values its conclusion
  is exact. Applying this to a projected continuous value function requires
  constructing those oracles and controlling their answers. Neither the
  unknown integer radius nor exact continuous value/subgradient precision is
  supplied by that theorem. It confirms that the general transfer from
  suitable convex oracles to fixed-dimensional integer optimization is old.
- [Basu, *Complexity of optimizing over the integers*, v6](https://arxiv.org/pdf/2110.06172v6),
  Definition 4.1 and Theorems 5.7--5.8, provides a useful scope check on more
  general mixed-integer convex oracle algorithms. The feasibility theorem
  permits reporting absence of a sufficiently deep feasible point; the
  optimization theorem is an approximation result with a supplied radius
  and a strict-feasibility radius in the relevant optimal fiber. These are
  not the package's exact degenerate and unbounded conclusion. The source
  explicitly distinguishes its feasibility procedure from exact feasibility.
- [Basu--Zell, *On projections of semi-algebraic sets defined by few quadratic inequalities*](https://www.math.purdue.edu/~sbasu/proj_quad.pdf),
  Theorem 1.2 and Section 8, studies low-order Betti numbers of projections
  of compact sets defined by a fixed number of complete quadratic
  inequalities. Its parameter is the total quadratic row count, including
  any affine rows encoded as quadratics. It does not give an exact
  fixed-Hessian-span description or integer optimization algorithm. In
  particular, a bound on topological complexity is not the degree-and-height
  bound needed for the new witness argument.
- A recent adjacent result is [Hu, *An Exact Dual for Second-Order Cone Programming Using Only Lorentz-Cone Constraints*](https://arxiv.org/pdf/2609.06757),
  September 2026, Theorem 3.5 and Corollary 3.7. It gives polynomial-size
  exact dual and infeasibility formulations over real data, including weak
  infeasibility. The abstract and Sections 1.2 and 4 explicitly separate
  formulation size from polynomial solution time and polynomial rational
  certificate bits. It does not subsume the current exact Turing theorem.
  This is a current preprint, not an independently verified source for a
  stronger bit-complexity claim.

A consequential follow-up source correction concerns unboundedness itself.
The [escape-certificate prior audit](succinct-unboundedness-prior.md) located
Obuchowska, *On boundedness of (quasi-)convex integer optimization problems*
(2008), [primary PDF](https://link.springer.com/content/pdf/10.1007/s00186-007-0196-3.pdf).
Its Algorithm A, pp. 461--462, and Theorem 5.1 give the recession-system
boundedness test; p. 466 explicitly states polynomial time. Corollary 5.1,
p. 465, gives continuous--integer unboundedness equivalence conditional on
integer feasibility, and p. 447 discusses the mixed-integer extension.
That audit checked the full source and its rationality assumptions. It also
identified Caron--Obuchowska's 1995 continuous algorithm. Thus even the
parameter-free boundedness classification on a promise-feasible native PSD
quadratic instance should be credited as old. A proposed uniform
integer-polynomial increment curve with a polynomial-size arithmetic circuit
would need its own comparison and proof. This correction narrows the
unboundedness contribution without removing the fixed-span finite-value,
feasibility, or exact-output contribution assessed here.
After the web PDF opening failed, I also directly read Algorithm A,
Theorem 5.1, Corollary 5.1, the final polynomial-time statement and the
mixed-integer-extension paragraph in the shared downloaded primary text
`/tmp/obuchowska-2008.txt`. They support this correction. Rational native
PSD quadratics fit the faithfully convex branch after rational factorization
and denominator clearing; no fixed-dimensional hypothesis is introduced.

The previous quadratic-image and simultaneous-diagonalization audit still
applies. A family such as `||x||^2 + 2 x_i - 1` has native span one but
unbounded complete-polynomial and augmented-matrix span. A standard SOCP or
SDP reformulation does not make its number of cone blocks, affine variables,
or complete coefficient directions fixed. Native PSD quadratic systems are
also narrower than general SOCP systems: squaring a norm inequality with a
variable right-hand side normally produces an indefinite Hessian. Thus a
general exact-conic formulation is neither an automatic subsumption nor a
contradiction to the proposed theorem.

**First reconstructed proof chain: unbounded optimization and the original
optimal integer witness.** This is the most exposed algorithmic step because
a small feasible point does not imply a small optimizer, and lifting
eliminated continuous variables can repeatedly square their size.

For a nonempty sublevel, the stated recession cone follows from PSD:
`d^T Q_i d = 0` implies `Q_i d = 0`, so the slopes are the rational linear
forms `a_i^T d`. If every feasible recession direction has objective slope
zero, moving far enough along such a direction satisfies every row with
strictly negative slope. Deleting those rows therefore gives the exact
projection and preserves every attainable objective value. If the integer
part of the direction vanishes, setting one continuous coordinate to zero
in the retained rows really only deletes coefficients. If it does not
vanish, primitive integer scaling and a unimodular completion give the
claimed lattice bijection. Only at most `k` steps of this second kind occur.
The stated polynomial coefficient growth for fixed `k` is consequently
consistent; it is not an unsupported bound on an arbitrary long sequence of
general substitutions.

At termination, zero recession cone makes each nonempty closed objective
sublevel bounded. The terminal mixed-integer optimum is attained in a compact
sublevel. The compressed formula gives uniform atom degree and height bounds
for the projection of such a sublevel. Quantifying the other integer
coordinates as real variables leaves bounded block dimensions for fixed
`(k,h)`. A finite endpoint of the resulting interval must be a zero of a
nonzero defining polynomial: if all nonzero signs were locally constant,
that point would not be an endpoint. The root bound therefore bounds the
whole terminal integer projection, not merely one arbitrary feasible point.

The subsequent return to the original coordinates is valid. The terminal
value has a uniformly bounded integer annihilator and a rational isolating
interval. In the original projected optimal set, adjoining one real scalar
`T`, its annihilator equation and that interval fixes `T` to the desired
value. The Boolean formula itself need not have convex atoms: its set in the
free integer-coordinate variables is exactly the convex projection of
`C intersect {q_0 <= v}`. Khachiyan--Porkolab applies to that set. Existence
of a bounded annihilator and interval is sufficient for an a priori witness
bound; the algorithm need not know their coefficients first. This avoids
the circularity that would arise from first computing the unknown optimum.

Finally, the implementation must use the original integer witness box with
threshold-specific continuous boxes, or a box proved to preserve every
fiber optimum. Section 5 supplies both justifications. A box preserving
mere feasibility would not suffice. The resulting separation-and-bisection
step is classical but correctly used here. No decreasing straight ray in
the original variables follows from unboundedness after projection; the
manuscript correctly avoids promising one.

**Second reconstructed proof chain: canonical optimizer, regular roots, and
degree through ordered limits.** The lexicographic active restriction is
sound. A point with lower objective, or equal objective and lower norm, in
the retained system would contradict original optimality along a sufficiently
short segment. The Hessian-dependency differences are rational affine
equations that vanish at the selected optimizer. They make the complete
retained polynomials span at most `h` without adjoining the optimal value.

The two compactness arguments must remain separate. On the exact retained
set, minimizing `q_0 + epsilon ||x||^2` bounds the selected points' norms by
the minimum-norm optimizer's norm and selects that optimizer as `epsilon`
tends to zero. For each fixed positive `epsilon`, relaxing the rows by
`delta` puts their minimizers in a compact sublevel of a coercive objective.
Their inner limit is the exact regularized minimizer. Neither argument
requires a uniform relation `delta(epsilon)`. The original-coordinate norm,
not the free-coordinate norm after affine elimination, is essential.

A minimum-support nonnegative representation by active gradients has
independent columns and at most `min(h,d)` members. One support can be fixed
on inner subsequences and then an outer subsequence before selecting the
coordinate output. Its full KKT Jacobian has positive-definite upper block
`M` and Schur complement `-G^T M^{-1} G`, hence is nonsingular. The
multihomogeneous bound counts these isolated regular roots even if other
components have positive dimension.

The parameter lemma in the new degree note addresses the important remaining
pitfall. Over the rational function field in the perturbation parameters,
localizing at the Jacobian determinant and output denominator leaves a finite
reduced algebra. Multiplication by the output gives one polynomial identity
of degree bounded by its dimension. At exceptional parameter values, an
analytic continuation of any regular root and continuity extend the same
identity; merely discarding those values would not suffice. Lowest nonzero
coefficient extraction, first in `delta` and then `epsilon`, gives a nonzero
annihilator at the ordered limit. The multiplier limits themselves need not
exist or be bounded.

Applying this argument to every rational linear combination of the fixed
optimizer coordinates and then using a primitive element bounds the degree
of their common field. Separate coordinate-degree bounds alone would not
justify that conclusion. The sharper root count supplies no height bound;
the separate height-controlled deformation proof is still necessary. I found
no gap in this chain. Its intersection-theoretic count and limit mechanisms
are classical; its new use depends on the Hessian-span restriction.

**Significance and the next question.** The final package deserves a stronger
assessment than the initial bounded value note. It identifies a structured
exact class that is not obtained by substituting `h` for a parameter in the
inspected older statements. Arbitrary affine rows, arbitrary continuous
dimension, degenerate algebraic fibers, unbounded input domains, and
continuous-dependent objectives all remain covered. The common-field result
also gives a cleaner explanation of why explicit exact outputs stay small.
These extensions are mathematically useful even without a practical solver.

The contribution should nevertheless be presented as one structural theorem
and its consequences. Finite attainment, semialgebraic integer optimization,
algebraic recognition, the generic QCQP degree formula, ordered infinitesimal
limits, and integer-preserving approximation are not separate discoveries of
this package. The shortest conceptual proof of some radius or degree
consequences may be the active affine restriction followed by established
few-quadratic machinery. That does not make the fixed-native-span statement
a direct old corollary before the restriction is proved, but it should temper
claims about how much of the algebraic machinery is new.

The most consequential next theoretical question is the **parameter
dependence of exact decision, separated from the cost of explicit algebraic
output**. In particular, can fixed-span exact feasibility or a rational
threshold decision be solved in `f(k,h) N^C` time with one absolute exponent
`C`? The current theorem does not answer this. A credible first step is a
sharp output-size analysis: construct polynomial-bit rational, strictly
feasible convex examples whose canonical optimizer field has degree
`n^{Omega(h)}`. Separable collections of trust-region or ellipsoidal
subproblems suggest a concrete route: obtain large irreducible degrees in
individual blocks and prove independence of their fields. Generic complex
root counts alone do not establish this rational, convex, bounded-height
construction, so no such lower bound is claimed here.

If that construction succeeds, it would explain why an FPT claim with fully
expanded minimal-polynomial output needs a different representation or an
output-sensitive qualification. The decision problem could still be FPT.
The positive route would have to exploit the few curvature directions through
oracles or compressed certificates without enumerating all algebraic roots
or all affine active faces. The negative route would need a parameterized
reduction preserving full PSD; familiar nonconvex few-quadratic hardness
reductions cannot be reused without checking this. This is more consequential
than shaving a constant from the existing worst-case precision bound.

Source inspection in this pass included the primary statements listed above,
the existing local Basu v6 text, and the local proof manuscripts. Searches
covered exact SOCP feasibility and duals, bit complexity, few-quadratic
projections, and convex integer oracle reductions. No direct subsumption was
identified, but this bounded search does not establish novelty. No numerical
test, Lean formalization, project-wide verification, or CI inspection was
used to validate the universal claims. Targeted document checks are recorded
with the completion report. The commands actually run were
`git diff --check -- research-20260927/main-theorem-reassessment.md` and an
inline Python check of local links, trailing whitespace, control characters
and the final newline; both passed. A subsequent
`git diff --no-index --check /dev/null research-20260927/main-theorem-reassessment.md`
reported no whitespace errors; its exit status was 1 because the file differs
from `/dev/null`. The Python check also passed after the source correction.
These checks verify the document, not
the mathematical theorems. The Obuchowska follow-up also used the downloaded
primary text identified above after a direct web opening failed.
