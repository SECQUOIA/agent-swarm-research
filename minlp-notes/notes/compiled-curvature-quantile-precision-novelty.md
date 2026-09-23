# Compiled curvature quantiles: source and novelty audit

Date: 2026-09-05. Bounded primary-source assessment of
[the compact scalar construction](compiled-curvature-quantile-precision.md)
and its [certified integration dependency](certified-positive-polynomial-curvature-quantiles.md).
Both complete drafts were read. Mathematical audits are separate.

No matching polynomial-time construction was found that, for a densely
encoded scalar rational polynomial with nonnegative nonlinear coefficients,
produces a rational MILP approximating its whole graph and uses at most
seven more integer variables than any convex integer lift. This remains a
qualified search finding. Optimal convex segmentation, certified analytic
integration, root refinement, and Boolean-circuit linear encodings all have
direct antecedents.

The potentially new combined guarantee is

```
f(x)=a*x+b+sum_(k=2)^D c_k*x^k, c_k>=0, x in [0,1],
p_out <= p_conv+7,
```

with deterministic construction time and rational formulation size polynomial
in the dense input and tolerance encoding. The comparator allows arbitrary
continuous convex lifts and unrestricted integer coordinates. It is not
restricted to the chosen knot grid or to a particular PWL encoding.

## Minimum-piece interpolation is established

Mohammadi Fathabad, Cheng, Pan, and Yang,
[Asymptotically Tight Conic Approximations for Chance-Constrained AC Optimal Power Flow](https://ira.lib.polyu.edu.hk/bitstream/10397/99199/1/Fathabad_Asymptotically_Tight_Conic.pdf)
(online 2022; European Journal of Operational Research 305, 2023, 738–753;
DOI `10.1016/j.ejor.2022.06.020`), is a particularly direct predecessor.
Section 3.2, printed pages 20–22, proves monotonicity of chord error in an
interval endpoint. Algorithm 1 successively extends each interval until its
error equals the prescribed tolerance. Theorem 2 proves a minimum number of
interpolation points for the Gaussian CDF construction. The paragraph after
the proof states extension to other strictly monotone convex or concave
functions bounded on at least one side. The algorithm explicitly constructs
each successive knot through line search. The checked section does not give
a polynomial-bit random-access knot algorithm or compare with arbitrary
convex integer lifts. Its optimal segment claim concerns its interpolatory
class; it is not a theorem about the smallest number of declared integers
in any possible formulation.

Gavrilović,
[Optimal approximation of convex curves by functions which are piecewise linear](https://www.sciencedirect.com/science/article/pii/0022247X75900955)
(1975, DOI `10.1016/0022-247X(75)90095-5`), already describes minimax
convex-curve segmentation using equalized local errors. Only the publisher
abstract was checked here, so its exact computational model is not assessed.
Ploussard,
[Piecewise linear approximation with minimum number of linear segments and minimum error](https://doi.org/10.1016/j.ejor.2023.11.017)
(2024), gives a hierarchical MILP fitting method and an iterative algorithm
using `O(S log N)` LPs for a possibly discontinuous fit to `N` data points
with `S` pieces. This comparison uses the primary publisher abstract and
introduction available through search, not a complete proof review.

The candidate does not need to compute an optimal partition. Its mass-based
partition has a constant-factor piece bound, and the logarithm converts that
factor to constant integer overhead. Crucially, its formulation represents
exponentially many possible intervals without enumerating them. A sequential
minimum-piece algorithm whose runtime grows with the number of pieces does
not automatically supply that guarantee.

The finite density and local-modulus predecessors are documented in the
[accuracy-dependent curvature audit](accuracy-dependent-curvature-precision-novelty.md).
In particular, Simchowitz et al. already uses an accuracy-dependent,
endpoint-corrected secant modulus. The present result should not be called
the first adaptive curvature formulation or the first minimum-piece method.

## Analytic integration: established machinery, explicit conditioning

Müller,
[Uniform computational complexity of Taylor series](https://ub-deposit.fernuni-hagen.de/servlets/MCRFileNodeServlet/mir_derivate_00001451/Mueller_Taylor_Series_1987.pdf)
(1987), studies polynomial-time Taylor coefficients, analytic functions, and
integration. Its introduction and Section 4 establish polynomial-time
integration in the analytic setting. A blanket appeal to this fact is
insufficient for a varying family whose singularities approach the interval:
uniform parameter dependence matters.

Kawamura, Müller, Rösnick, and Ziegler,
[Parameterized Uniform Complexity in Numerics](https://arxiv.org/pdf/1211.4974),
Theorem 3.7(b)(v), printed pages 27–29, gives uniformly polynomial parametric
integration under enriched analytic representations. The preceding
definitions encode bounds on magnitude and distance to complex singularities,
with their encodings explicitly affecting runtime. The proof partitions into
local analytic regions and sums local antiderivatives. This is close prior
machinery for the candidate's panel argument. Its positive-coefficient sector
estimate explicitly supplies suitable local analytic neighborhoods, while
cutoff and root-neighborhood removal bound the omitted mass. The minimum of
two branches is not globally analytic, so applying an analytic theorem to the
whole density without the branch decomposition would be unjustified.

Sagraloff and Mehlhorn,
[Computing Real Roots of Real Polynomials](https://arxiv.org/pdf/1308.4088),
Theorem 3, restated as Theorem 36, gives for square-free integer polynomials
of degree `n` and coefficient bit bound `tau` root intervals narrower than
`2^-kappa` in `O-tilde(n(n^2+n*tau+kappa))` bit operations. The integer
specialization appears explicitly on printed page 5. It supports the
candidate's polynomial root-isolation/refinement import after denominator
clearing and square-free preprocessing. It also applies to the Legendre
nodes. Root isolation itself is not new here.

[NIST DLMF Section 3.5(v)](https://dlmf.nist.gov/3.5#v), Equations
3.5.18–3.5.20, supplies Gaussian nodes, positive weights, and the polynomial
exactness/remainder formula. The candidate additionally proves the rational
precision and weight-conditioning estimates it needs; the DLMF statements
alone are not a polynomial-bit quadrature theorem. The analytical novelty
should be positioned modestly: an explicit uniform reduction of this
piecewise algebraic density to established certified computation.

## The compact encoding also has direct predecessors

Avis, Bremner, Tiwary, and Watanabe,
[Polynomial size linear programs for problems in P](https://arxiv.org/pdf/1408.0807),
Section 3, Lemma 1, gives the input-0/1 property: binary inputs force a
unique Boolean extension through continuous linear gate variables. That
lemma credits Valiant (1982). Avis and Bremner's
[Sparktope](https://arxiv.org/pdf/2005.02853) makes compilation of bounded
algorithms into linear formulations explicit. Neither continuous gate
variables nor algorithm compilation should be presented as new.

Adams and Henry,
[Base-2 Expansions for Linearizing Products of Functions of Discrete Variables](https://www.osti.gov/servlets/purl/1648449)
(2012), Section 2, Equations (4)–(13), represents arbitrary discrete function
values and their products with a nonnegative continuous variable using the
same logarithmic number of binaries, with a selector for each discrete value.
The candidate's circuit representation removes the need to list every value
when an indexed computation is short. Further direct circuit-interpolation
antecedents are recorded in the
[compiler source audit](compiled-rational-knot-formulations-novelty.md).

The useful new connection is therefore the particular indexed mass-quantile
algorithm, with bounded rational computation and a whole-graph error band,
combined with the universal convex-lift lower bound. Its proof does not need
a lower bound on density for mass-accurate inversion, nor exact comparison
of algebraic integrals. Those features make the finite benchmark compatible
with the polynomial-size compiler.

## Scope to retain

This is one scalar output, one scalar input, dense polynomial encoding, and
nonnegative coefficients on all nonlinear powers. Arbitrary affine terms are
handled exactly. Neither sparse binary-encoded huge degree nor a polynomial
that is merely nonnegative on the real interval is covered. The result does
not compute the exact optimum integer count, prove ideality of the
continuous relaxation, or make the resulting MILP easy to solve.

A defensible summary is: “Using established certified integration and
circuit-encoding tools, we construct a polynomial-size rational graph
formulation within an absolute constant of the minimum integer dimension
over all convex lifts, for densely encoded positive scalar polynomials.
No matching universal integer-count construction was found in the open
primary literature inspected.” Keep the finite-density novelty assessment
and its search limitations linked to this algorithmic claim.
