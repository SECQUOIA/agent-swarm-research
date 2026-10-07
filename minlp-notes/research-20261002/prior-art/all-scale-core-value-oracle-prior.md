# Prior-art audit: one finite noise law for all-scale core value queries

Date: 2026-10-02. This focused comparison covers the candidate
[all-scale core value oracle](../new-direction/all-scale-core-value-oracle.md).
The candidate passed its
[independent actual-file review](../reviews/all-scale-core-value-oracle-review.md)
after an explicit formula-encoding repair. It extends a reviewed one- and
two-core-coordinate result. This note compares the stated ingredients with
prior results. It does not review the proof or make a novelty claim.

## Candidate model and guarantee

The domain is `[0,1]^k x [0,1]^m`, with arbitrary `k>=1`. The objective is
an explicit fixed-degree rational polynomial. The residual block is convex
for every core point, and each core coordinate has a verified upper
curvature bound `L`. Only the core's linear coefficients receive
independent noise from one finite rational grid chosen from the base input.
Residual strong convexity and a supplied growth constant are not assumed.

For the same sampled objective, every requested accuracy `2^-q` has a
rational feasible point and a certified optimal-value interval of width at
most `2^-q`. The reviewed expected bit work is
`f_d(k)(1+L/sigma)^k poly_d(I+q)`, with one random work factor controlling
all precisions. The output is a value Cauchy oracle: it does not select a
limit optimizer, certify distance to the optimizer set, or promise expanded
algebraic coordinates.

The algorithmic backbone is the reviewed dyadic core-cell refinement with
certified convex residual values, globally valid lower bounds, and an
all-draw exact fallback. Its near-optimal cell count is controlled by an
all-scale determinant proxy for padded convex hulls of near-optimal core
sets. The analysis uses a strongly convex regularization of the Fenchel
conjugate, the associated Aleksandrov Monge–Ampère measure, a `5r` covering
argument, and a two-block semialgebraic formula for transfer to one finite
noise grid. The candidate avoids bounding the cell count by a power of one
quadratic-growth constant.

## Closest established results

The closest algorithmic predecessor inside the project is the reviewed
[semiconcave cell-count theorem](../new-direction/smoothed-semiconcave-cells.md).
For an arbitrary continuous objective with an upper coordinate-curvature
bound, it uses independent continuous linear tilts and two neighboring-grid
comparisons to bound the expected number of near-optimal grid nodes uniformly
over mesh refinements. A corrected-corner branch-and-bound scheme then gives
expected logarithmic accuracy dependence in an arithmetic-oracle model at
fixed dimension. This already establishes the local counting and certified
cell-refinement mechanisms. It does not provide one finite rational law
serving every accuracy, a polynomial bit-model convex recourse oracle, or
the all-scale determinant/Monge–Ampère bound. See the full
[semiconcave prior audit](smoothed-semiconcave-cells-prior.md).

The reviewed
[one- and two-coordinate core value theorem](../new-direction/core-only-noise-value-oracle.md)
already gives the same fixed-law, all-accuracy value-oracle interface for
`k in {1,2}` with convex polynomial residual recourse and no residual growth
promise. Its proof uses a finite-law tail for projected quadratic growth and
a per-level cap. The all-scale candidate removes the two-coordinate limit
by bounding one geometric cell-count factor directly. It is a close
internal predecessor, not external prior art.

The project's
[random-tilt growth tail](../new-direction/proximal-growth-tail.md) is a
quantitative prior for the conditioning argument. For any continuous
objective on a compact set and independent coefficient densities bounded by
`phi_i`, it proves
`Pr{g_*(c)<eps} <= 2 eps sum_i phi_i w_i`, where `g_*` is the global
quadratic-growth modulus at a unique optimizer and is zero for multiple
optimizers. This is dimension-free apart from the sum of coordinate widths
and densities, and it does not require convexity or semialgebraicity. The
candidate's measure construction is a different use of convex conjugacy:
it controls an all-scale near-optimal-set size proxy rather than only a
point-growth modulus. A growth-only charging argument gives a factor of
order `(L/g_*)^(k/2)` in the core cell count; the new proxy avoids taking
that high inverse moment. The growth-tail audit separately compares the
sharp estimate with discrete winner gaps and qualitative genericity.

Horn's [“Optimal Algorithms for Global Optimization in Case of Unknown
Lipschitz Constant”](https://d-nb.info/987595660/34) is the closest
classical value-only comparison for multiple minimizers and small
near-optimal sets. It studies Lipschitz functions on a box under a global
near-optimal-sublevel-volume condition and gives adaptive mesh methods for
known or unknown Lipschitz constants. Its minimax accuracy rate depends on
dimension and the supplied sublevel-volume constant; the result is not an
expected guarantee under random linear tilts and does not exploit convex
residual recourse or produce certified bit-model intervals for one finite
sample. Exact assumptions and locators are recorded in the local
[Horn source note](../../literature/papers/horn2005-optimal-algorithms-for-global-optimization/paper.md).

Röglin and Rösner's [The Smoothed Number of Pareto-Optimal Solutions in
Non-integer Bicriteria Optimization](https://doi.org/10.1007/978-3-319-55911-7_39),
Theorem 2, bounds the expected number of Pareto-optimal points in a finite
real-valued feasible set under independent random linear profit
coefficients and a coordinate-separation condition. This is strong prior
for random linear perturbations and expected near-winner counts. The domain
is finite, the counted solutions are exact Pareto optima, and the bound
depends on a separation parameter that deteriorates on fine grids. It does
not give a mesh-uniform count on a continuous core box. The full primary
text and locators are in the
[local source package](../../literature/papers/roglin2017-the-smoothed-number-of-pareto/paper.md).

Beier and Vöcking's STOC 2004 paper, Lemma 5, proves a sharp density bound
for the best-versus-second-best objective-value gap on a finite binary
feasible set under independent linear coefficient noise. That result
credits discrete winner isolation, but the candidate's continuous domain
has no positive second-best gap and the desired count is over approximate
core cells, not discrete feasible labels. The readable source is the 2004
STOC paper; a separate 2006 journal-version record is metadata-only and is
not used here. The project source note is
[here](smoothed-exact-miqp-prior.md).

Kelner and Nikolova's FOCS 2007 Theorem 2.9 gives expected projected-shadow
enumeration for fixed-rank quasi-concave minimization under a random
rotation of the objective's low-rank subspace. It is another strong
smoothed global-optimization result, but its perturbation and geometric
count are different: random rotation and projected polytope vertices, not
independent additive core tilts and near-optimal convex-hull cells. The
existing [ambient-noise audit](smoothed-ambient-noise-prior.md) gives the
precise comparison.

## Classical measure and genericity background

The candidate's measure
`mu(E)=Leb({y: grad H*(y) in E})` is the Aleksandrov Monge–Ampère measure
of `H`, since `partial H(c)={y: grad H*(y)=c}`. This is a standard
subgradient-image measure, not a new construction. Colesanti, Ludwig, and
Mussnig define `MA*(u;·)=MA(u*;·)` for supercoercive convex `u` and prove
in Theorem 5.1(a) that it is the pushforward of Lebesgue measure under
`grad u` ([primary paper](https://arxiv.org/abs/2111.05648), §5). Applying
that result to `u=H*` gives exactly the candidate's measure; Proposition
3.1(a) verifies the needed supercoercivity from finite-valued convexity of
`H`. The local source note records the precise identities and locators
([Colesanti–Ludwig–Mussnig](../../literature/papers/colesanti2022-the-hadwiger-theorem-on-convex/paper.md), Lemma 4.1 p.11 and Theorem 5.1(a) p.15). This source supports the measure identity only; it does not provide the candidate's near-optimal-set estimate.

The candidate's continuous `1/T` tail has the form of a classical
weak-(1,1) maximal inequality for a measure. A previously consulted public
text mirror of Mattila's *Geometry of Sets and Measures in Euclidean
Spaces* reported Definition 2.18 / Theorem 2.19 (1995, pp. 40–41) as the
centered maximal-function bound
`lambda({c:M_lambda nu(c)>t}) <= C_k nu(R^k)`, for
`M_lambda nu(c)=sup_r nu(B(c,r))/lambda(B(c,r))`. Under that statement,
one takes `lambda` to be Lebesgue measure and truncates `nu=mu` to the
expanded noise cube `Q_R`; this gives finite total mass, and every ball
used at a noise point lies inside `Q_R`. The candidate's hull-to-ball
inclusion and `Vol(K_h) >= D_h/k!` then turn `A(c)>T` into a lower bound
on this maximal function, at radius `r=4kLh`.

That Mattila locator remains provisional. The sole ingester checked the
official Cambridge page, found no lawful full text, and stored a
metadata-only unread record; neither the reported maximal theorem nor the
§2.1 Theorem 2.1 5r locator is verified against an archived primary text.
Allen and Beresnevich do state a 5r lemma in §3.2, Lemma 3 (printed
p.1030/PDF p.19), citing Mattila; their local source note records the
statement but not a proof
([Allen–Beresnevich](../../literature/papers/allen2018-a-mass-transference-principle-for/paper.md)).
Thus this is a standard maximal-inequality comparison consistent with the
checked mirror, not a verified KB citation. The candidate-specific step is
the embedding of its all-scale hull event in that maximal-function event.

There is a closer Monge–Ampère maximal-function analogue in Le and Nguyen,
*Geometric Properties of Boundary Sections of Solutions to the
Monge–Ampère Equation and Applications* (JFA 264 (2013), 337–361;
[arXiv:1205.6882](https://arxiv.org/abs/1205.6882)). Under their domain,
boundary separation, and density assumptions (2.3)–(2.5), Lemma 2.5 gives
a Besicovitch-type covering for boundary sections, Theorem 2.6 a covering
result, and Theorem 2.7 weak-(1,1) and strong-(p,p) bounds for the maximal
operator averaging over those sections. This is meaningful prior for the
covering-to-maximal-estimate pattern, but its sections arise from convex
solutions of a Monge–Ampère PDE. It does not state an all-scale tail for
ordinary coefficient-space balls, a near-optimal determinant proxy, or an
optimization algorithm. The full arXiv text is now read in the local
package ([Le–Nguyen](../../literature/papers/le2012-geometric-properties-of-boundary-sections/paper.md));
Theorem 2.7 is p.5, assumptions (2.3)–(2.5) are p.3, and Lemma 2.5 is
pp.4–5. The candidate's use of a regularized Fenchel conjugate supplies
its own local mass bound; it does not use a PDE section covering theorem.

The distinct smoothed-condition-number literature addresses another
problem family. Dunagan, Spielman, and Teng analyze Renegar's condition
number for linearly perturbed linear programs (Theorems 1.3.1–1.3.2,
arXiv version p.4); Rademacher and Shu study conditioning measures of
randomly perturbed polytopes for Frank–Wolfe methods (Theorems 1.2–1.3,
arXiv version p.2, with scope limits discussed p.3). Their local primary
packages have been read ([Dunagan–Spielman–Teng](../../literature/papers/dunagan2003-smoothed-analysis-of-renegars-condition/paper.md),
[Rademacher–Shu](../../literature/papers/rademacher2020-the-smoothed-complexity-of-frank/paper.md)).
These works bound algorithm-relevant condition numbers after perturbing LP
data or polytope geometry. They do not bound the candidate's near-optimal
core-set size under objective-only linear noise, or give a fixed finite
perturbation law for certified value queries at every requested precision.
They are terminology-adjacent, not equivalent results.

The candidate-specific geometric reduction places every padded
near-optimal hull at scale `h` inside a ball of radius proportional to
`Lh` in coefficient space. After that inclusion, the `1/T` tail for the
supremal determinant ratio follows from the classical maximal inequality
above. The focused comparisons do not state the resulting all-scale
near-optimal-core count as an optimization algorithm or combine it with the
candidate's single-law finite-grid transfer and certified recourse
interfaces. This comparison does not establish priority for that
composition.

Alexandrov's theorem gives almost-everywhere second-order differentiability
of finite convex functions; the verified modern proof by Azagra, Cappello,
and Hajłasz states the theorem directly. Combined with convex duality, this
implies qualitative uniqueness and some positive global quadratic growth
for almost every absolutely continuous linear tilt of a continuous
objective on a compact set. Lee and Phạm give related qualitative
genericity results for semialgebraic programs. None gives an explicit
all-scale tail, a single finite law, or expected query complexity. These
results are recorded with exact source boundaries in the
[growth-tail prior audit](proximal-growth-tail-prior.md).

The finite-noise transfer is also an established algorithmic primitive.
Renegar's Part III Theorem 1.1 bounds the degrees and component count of a
fixed-block quantified semialgebraic formula independently of coefficient
heights, with input heights entering the output bit bounds. The candidate
uses Carathéodory witnesses and an encoded QR determinant to express its
all-scale event with two quantified blocks, then applies that theorem to
bound scalar sections and choose a single finite law. The contribution is
the compact first-order encoding of this event and its use in the
all-accuracy cap argument, not quantifier elimination itself. The
[polynomial-tail source audit](sparse-smoothed-polynomial-prior.md) gives
the Renegar theorem, exact locator, and bit-model caveats.

## Comparison boundary

The established work already supplies adaptive value refinement,
near-optimal counting for finite perturbed sets, discrete winner-gap
isolation, qualitative generic growth, convex conjugacy, and standard
weak-type covering. The reviewed low-dimensional project result also
supplies a single finite law for all value precisions when `k<=2`. The
candidate's possible advance is the all-dimensional composition of
certified convex recourse, an all-scale Aleksandrov-measure proxy, and a
height-independent finite-grid section bound to obtain one fixed-law
expected value oracle for arbitrary `k`. The candidate does not return an
optimizer-coordinate oracle or expanded algebraic optimizer output.

This is a bounded comparison, not evidence that the composition is new.
The Colesanti–Ludwig–Mussnig measure identity, Allen–Beresnevich 5r
statement, Le–Nguyen maximal theorem, and Dunagan–Spielman–Teng and
Rademacher–Shu condition-number papers have full-text checked local
packages. Mattila remains metadata-only/unread in the KB because the
publisher provides no lawful full text; the personally checked text-mirror
locators above are explicitly provisional.
