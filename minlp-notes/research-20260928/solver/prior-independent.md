# Independent prior-work and significance audit: sparse kernel rounding

Date: 2026-09-28. Scope: the candidate in
[sparse-kernel-rounding.md](sparse-kernel-rounding.md). This audit began with
an exact-local-measure formulation; the principal candidate now concerns
finite-order local Schmüdgen pseudoexpectations. That strengthening is
essential to the significance assessment.

**Corrected assessment, 2026-09-28.** The `O(r^-2)` sparse box-preordering
rate was already publicly asserted in Victor Magron's lecture slides dated
7 July 2025, logical slide 23/44, PDF page 90, and repeated on
16 February 2026, logical slide 35/90, PDF page 121. The slides explicitly
uses two local full preorderings and attributes its theorem to Korda,
Ríos-Zertuche, and Magron (2024). Its rendered formula was checked; this is
not an extraction artifact. The published paper's Theorem 6 gives the
slower width-dependent rate recorded below. That discrepancy remains
unresolved: this audit cannot assume that the slide is a typo or that it
rests on an unreported assumption. The rate itself must therefore not be
presented as newly asserted here. A contribution may remain in the explicit
finite-order rounding theorem, proof, constants, and further implications,
but priority for those features requires separate comparison. See the
[dedicated correction and retained primary evidence](sparse-putinar-prior.md).

The kernel, its second-order approximation rate, finite-moment smoothing,
and junction-tree gluing are established ingredients. An exact-measure
version alone would be a substantially weaker contribution.

## Exact scope of the possible advance

Let the bags satisfy running intersection, with largest cardinality `w`.
The hierarchy must require each local functional to be nonnegative on
every degree-admissible term

\[
 q^2\prod_{i\in I}(1-x_i^2),\qquad I\subseteq B.
\]

Adjacent functionals agree on all separator moments within the stated
truncation. This is the full **local box preordering**. It is stronger than
the usual local quadratic module generated only by the individual box
inequalities. It does not assume that a local functional already has a
representing measure.

The proposed common tensor kernel has four properties doing distinct work:
finite input degree makes the functional evaluation meaningful; a local
preordering certificate makes each output density nonnegative; exact
constant preservation makes marginalization remove unused coordinates;
common coefficients make overlap moment agreement become exact marginal
agreement. Running intersection then permits global gluing.

The current bound is

\[
0\le f^*-\rho_r\le
\frac{3 A(f;B)}{2(\lfloor r/w\rfloor+1)^2+1},
\qquad
A(f;B)=\sum_{b,\alpha}|c_{b,\alpha}|\sum_i\alpha_i^2,
\]

for `r>=max(w,max_b deg f_b)`, with `c_{b,alpha}` the local tensor-Chebyshev
coefficients. Thus this is a fixed-objective asymptotic exponent, with an
explicit dependence on its decomposition. It is not a dimension-free
absolute error for objectives whose number or magnitude of terms grows.
For averages of uniformly bounded local costs, the coefficient budget can
remain bounded independently of the number of bags.

## Sources examined and comparison

0. **Magron, “Sparse polynomial optimization,” Lorentz Center, 7 July 2025;
   and “(Non)linear moment problems: theory and practice,” TENORS
   Learning Week 2, The Arctic University of Norway, 16 February 2026.**
   [2025 primary slides](https://homepages.laas.fr/vmagron/slides/lorentz25.pdf),
   logical slide 23/44, PDF page 90;
   [2026 primary slides](https://homepages.laas.fr/vmagron/nlmoment.pdf), logical
   slide 35/90, PDF page 121; [retained 2025 PDF](prior-sources/magron-lorentz-2025-07-07.pdf),
   [retained 2026 PDF](prior-sources/magron-nlmoment-2026-02-16.pdf)
   and [rendered slide](prior-sources/magron-nlmoment-slide35-page121.png).
   This source already asserts the sparse full-preordering rate `O(r^-2)`.
   Its theorem label cites the same 2024 paper whose explicit Theorem 6
   yields `O(r^(-2/(w+3)))`. No independent proof of the stronger slide
   statement was found in the inspected material. Neither priority nor
   erroneousness can be inferred from that absence.

1. **Korda, Magron, Ríos-Zertuche, “Convergence rates for sums-of-squares
   hierarchies with correlative sparsity,” published online 2024, Mathematical
   Programming 209 (2025), 435–473.**
   [Primary open article](https://link.springer.com/article/10.1007/s10107-024-02071-6).
   Read Theorems 2 and 6, Section 2, and the polynomial decomposition in
   Section 3. Their box-preordering rate is
   `O(r^(-2/(w+3)))` for fixed data and maximum bag size `w`; they also treat
   general semialgebraic sets using sparse quadratic modules. Their proof
   constructs positive clique polynomials by approximating separator value
   functions, then applies a sparse Jackson operator. Lemma 10 already has
   tensor eigenvalues and `O(r^-2)` damping; Theorems 11–12 already supply
   fixed-section preordering positivity. The slower sparse exponent comes
   from the intermediate decomposition, so the kernel alone is no advance.
   The candidate bypasses that intermediate approximation through a primal
   construction. The paper uses coordinatewise degree cutoffs; the candidate
   uses total degree. These conventions differ by fixed width factors and
   do not explain the exponent difference.

2. **Lasserre, “Convergent SDP-relaxations in polynomial optimization with
   sparsity,” SIAM Journal on Optimization 17 (2006), 822–843.**
   [DOI](https://doi.org/10.1137/05064504X);
   [local primary text](../../literature/papers/lasserre2006-convergent-sdprelaxations-in-polynomial-optimization/fulltext.md).
   Read the asymptotic moment construction and Appendix 6.2–6.3, especially
   Lemma 6.4. Consistent local probability measures already glue under
   running intersection, including support restrictions. The convergence
   proof reaches consistent measures by a limiting argument and compact
   moment determinacy. The candidate's proposed addition is a finite-order,
   quantified construction that first makes genuine consistent measures.
   Neither junction-tree gluing nor qualitative sparse convergence is new.

3. **de Klerk, Hess, Laurent, “Improved convergence rates for Lasserre-type
   hierarchies of upper bounds for box-constrained polynomial optimization,”
   SIAM Journal on Optimization 27 (2017), 347–367.**
   [Primary preprint](https://arxiv.org/abs/1603.03329).
   The inspected abstract and introduction give `O(r^-2)` bounds using
   Jackson kernels, the Chebyshev measure, and Schmüdgen-type polynomial
   densities. This establishes strong precedent for the kernel and rate.
   The hierarchy chooses a global density to obtain an upper bound;
   it does not establish the candidate's sparse lower-bound rate or round
   a family of compatible local truncated functionals.

4. **Catala, Hockmann, Kunis, Wageringel, “Approximation and Interpolation
   of Singular Measures by Trigonometric Polynomials,” Constructive
   Approximation 60 (2024), 405–442.**
   [Primary open article](https://link.springer.com/article/10.1007/s00365-024-09686-0).
   Read the introduction, Section 3.1, and Remark 3.7. The latter explicitly
   observes that equal low-order trigonometric moments give equal Jackson
   convolutions. Positive finite-rank smoothing of arbitrary measures and
   Wasserstein approximation are therefore established even for singular
   measures. Replacing angle variables by their cosines transfers the
   relevant moment identity to Chebyshev moments. This source sharply
   limits any claim that “moment matching becomes exact agreement after
   smoothing” is itself new. It does not concern sparse SDP functionals.

5. **Magron, “Convergence Rates for Polynomial Optimization on Set
   Products,” SIAM Journal on Optimization (2026).**
   [Primary preprint](https://arxiv.org/abs/2505.18580);
   [local primary text](../../literature/papers/magron2026-convergence-rates-for-polynomial-optimization/fulltext.md).
   Read Theorem 11, Corollary 12, and the conclusion. Product-domain
   Schmüdgen rates of `O(r^-2)` follow by multiplying factor kernels,
   including products of spheres, balls, simplexes, and cubes. This already
   establishes broad kernel tensorization. Its certificate cone is a dense
   cone on the product; overlapping sparse bags are a different relaxation.
   Its generalized-moment application imports a dual-attainment condition.
   Consequently an extension to other product factors would need to add
   overlap compatibility, not merely multiply the established kernels.

6. **Gamertsfelder and Mourrain, “The Effective Countable Generalized
   Moment Problem,” arXiv:2501.09385v4 (2025).**
   [Primary current text](https://arxiv.org/html/2501.09385).
   Read the sequence-space dual, Assumptions 3, 9, 10, Theorem 12,
   Theorem 13, and Corollary 14. This is particularly close: it permits
   vectors of measures and countably many constraints, and transfers
   geometric positivity rates to moment relaxations. Using the full box
   preordering gives exponent two. However Assumption 9 requires an
   attained dual in the finitely supported multiplier space; its constants
   depend on that optimizer. For separator moment equalities this means
   polynomial separator potentials. The explicit example below shows that
   this condition can fail in the candidate's width-two setting. Therefore
   the unconditional candidate is not an immediate instance of this
   conditional result.

7. **Gribling, de Klerk, Vera, “Squared polynomial approximation kernels
   for the hypercube: improved error bounds and implications for Lasserre
   hierarchies,” arXiv:2605.31496v1 (2026).**
   [Primary text](https://arxiv.org/html/2605.31496).
   Read the introduction and the squared-kernel normalization construction
   in Section 3. Their dense Putinar rate is `O(log^3(r)/r^2)`.
   The squared SOS kernel has a nonconstant integral `M_r(x)`; the paper
   handles reciprocal normalization through polynomial approximation.
   This is relevant prior work but not an immediate substitute in the
   candidate: exact constant preservation is needed for exact separator
   consistency. An approximate normalization needs a separate repair
   argument. The candidate must not be advertised as improving this dense
   Putinar theorem, since it uses a stronger sparse preordering.

8. **Bienstock and Muñoz, “LP Formulations for Polynomial Optimization
   Problems,” SIAM Journal on Optimization 28 (2018), 1121–1150.**
   [Primary preprint](https://arxiv.org/abs/1501.00288);
   [local paper notes](../../literature/papers/bienstock2018-lp-formulations-for-polynomial-optimization/paper.md).
   Read local primary-paper metadata and source-grounded notes, and the
   online abstract. Bounded-treewidth mixed-integer polynomial optimization
   already admits LP approximation schemes via discretization, with scaled
   feasibility and objective tolerances. Thus broad claims of first
   approximation tractability from treewidth would be incorrect. The
   candidate instead quantifies a particular continuous SDP hierarchy and
   its rounding. That distinction matters even if a grid algorithm is
   easier on some of the same box-only problems.

9. **Piazzon and Vianello, “A note on total degree polynomial optimization
   by Chebyshev grids,” Optimization Letters 12 (2018), 63–71.**
   [Primary manuscript](https://www.math.unipd.it/~marcov/pdf/opticheb.pdf),
   DOI `10.1007/s11590-017-1166-1`.
   Read Lemma 1 and Propositions 2–3. For degree `d`, their grid has
   `md+1` Chebyshev–Lobatto nodes per coordinate and objective error at
   most `epsilon_m (f_max-f_min)`, where
   `epsilon_m=sec(pi/(2m))-1 < 2/m^2`. Thus the second-order grid
   approximation exponent is established. Combining such a grid with
   finite-state tree optimization is an immediate alternative on a sparse
   box objective; a theorem for SDP rounding must be distinguished from
   this existing approximation mechanism.

10. **Tran and Toh, “On the convergence rates of moment-SOS hierarchies
    approximation of truncated moment sequences,” arXiv:2507.00572v1
    (2025).** [Primary text](https://arxiv.org/html/2507.00572v1).
    The independent late-prior reviewer read Theorems 3.3–3.5. Theorem 3.5
    gives a second-order Hausdorff approximation for fixed-degree truncated
    moment sequences over products of balls and simplexes, including
    intervals, with a redundant global ball inequality. This concerns
    one dense pseudo-moment sequence. Independently selecting close true
    moments for each bag does not ensure equal separator marginals, so
    this estimate alone does not give the candidate's compatible rounding.
    The reviewer's full-text search found no clique-gluing theorem. A
    subsequent direct retrieval here returned HTTP 503; this entry records
    the delegated primary-text review rather than claiming a second full
    reading.

## A checked obstruction to polynomial dual attainment

The following example was independently rediscovered by the late-prior
reviewer and algebraically rechecked here. Its rational-separator
obstruction is already present in **Nie, Qu, Tang, and Zhang,
“A characterization for tightness of the sparse Moment-SOS hierarchy,”
Example 6.7** ([primary article, Section 6](https://link.springer.com/article/10.1007/s10107-025-02223-2)).
It is not a new example mechanism. On `[-1,1]^3`, use two bags `{x,y}` and
`{y,z}` and the degree-four costs

\[
f_1(x,y)=(1+y^2)x^2-2yx,
\qquad
f_2(y,z)=y^2-2y^2z+(1+y^2)z^2.
\]

Set `q(y)=y^2/(1+y^2)`. Completion of squares gives

\[
f_1+q=(1+y^2)\left(x-\frac{y}{1+y^2}\right)^2,
\qquad
f_2-q=(1+y^2)\left(z-\frac{y^2}{1+y^2}\right)^2.
\]

Both minimizing coordinates lie in the box for every `y in [-1,1]`.
Consequently `min(f_1+f_2)=0`, attained for every separator value `y`.

For the precise algebraic relation, their objective is
`F(x,y,t)=x^2+(xy-1)^2+(yt)^2+(t-1)^2`, with minimum one.
Substitution gives `F(x,y,1-z)-1=f_1(x,y)+f_2(y,z)`.
Their box for `t` becomes `z in [0,2]`, whereas this note uses
`z in [-1,1]`; these domains are not identical. Both contain every
fiber minimizer `z=y^2/(1+y^2) in [0,1/2]`, so the same separator
obstruction applies. Their dense SOS identity becomes
`f_1+f_2=(xy-z)^2+(x-y+yz)^2` after this substitution.

Suppose the zero lower bound were certified by two nonnegative clique
polynomials `h_1(x,y)` and `h_2(y,z)` summing to `f_1+f_2`.
The polynomial identity forces `h_1=f_1+u(y)` and `h_2=f_2-u(y)` for a
polynomial `u`: their differences can depend on neither `x` nor `z`.
Evaluating at the displayed minimizers requires both `u(y)>=q(y)` and
`u(y)<=q(y)`. Thus `u=q` on an interval, which is impossible for a
polynomial since `y^2` and `1+y^2` are relatively prime.

This is nonattainment of the exact polynomial separator dual; it is not
a failure of continuous separator duality, since the rational continuous
function `q` works. In particular, no finite-degree sparse preordering
certificate can attain zero for this instance. The example does not prove
a lower bound of order `r^-2`: a hierarchy can converge much faster on it.

Targeted verification run: a short `python`/SymPy calculation expanded
both completed-square residuals and returned exact zero; it returned
`gcd(y^2,1+y^2)=1`. The interval bounds and the separator-polynomial
argument above were checked mathematically. No project-wide checks or CI
status were inspected. This computation checks the displayed algebra, not
the kernel theorem or the completeness of the literature search.
The later attribution audit separately used SymPy to check the affine
objective identity and transformed dense SOS identity; both residuals
were exactly zero.

## Limitations that must survive presentation

- **Hard constraints are not preserved.** Even smoothing a point mass at
  `x=0` yields an absolutely continuous probability measure relative to
  arcsine measure. Its probability of the singleton is zero, so the
  equality constraint is lost. Sparse hard-constraint MINLP needs a new
  support-preserving mechanism or a rigorously controlled repair.
- **Integrality needs a separate construction.** A continuous box kernel
  does not preserve binary or general integer supports. Identity kernels
  on finite domains may address bounded discrete variables, but their
  positivity, degree accounting, and conditioning are additional claims.
- **The preordering matters.** Multiplying univariate interval
  certificates introduces products of box inequalities. One cannot drop
  those localizing constraints and retain this proof for a quadratic-module
  hierarchy. There can be up to `2^w` localizer types per bag.
- **Rounding existence is not a bit-complexity bound.** Conditional laws
  give an exact global measure mathematically. Numerically stable sampling,
  rational extraction, or finite quadrature need explicit algorithms.
- **The exponent is an upper bound, not a proved optimum.** Worst-case
  lower bounds for dense polynomial-density upper hierarchies do not
  automatically give matching lower bounds for this sparse lower hierarchy.
- **No solver speedup follows yet.** A better degree bound may reduce the
  predicted SDP order, but conditioning, localizer count, coefficient
  budgets, and alternative discretization methods still determine practical
  value.

For a finite quadrature variant, a common positive tensor quadrature exact
for the kernel densities and their products with the objective would
preserve separator marginals and expected objective exactly. Standard
finite-state tree optimization could then select a grid point. This is a
plausible constructive consequence to prove separately. It would not make
grid approximation or tree dynamic programming new.

## Search coverage and remaining uncertainty

Searches covered sparse Lasserre rates, sparse Jackson kernels, compatible
marginals and polynomial kernels, Jackson moment reconstruction,
correlative sparsity in 2025–2026, and treewidth/grid approximation.
Primary open versions were preferred. Local literature searches found
Lasserre 2006, Waki et al. 2006, Magron 2026, and Bienstock–Muñoz 2018.
Waki's local notes were consulted for historical context, without treating
their experimental performance claims as a comparison for this candidate.
An independent child reviewer additionally investigated later sparse-rate
and generalized-moment work.

The July 2025 and February 2026 slides correct the earlier search assessment: an earlier
primary source does assert the same sparse box-preordering rate. The
remaining priority question concerns the explicit compatible rounding
construction, its proof, constants, and implications, together with the
unresolved relation between that slide and the published theorem. Before
publication, further source comparison must resolve or explicitly preserve
this uncertainty. The Tran–Toh comparison above covers one particularly
close truncated-moment result.
