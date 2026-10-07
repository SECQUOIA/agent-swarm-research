# Independent review of sparse smoothed polynomial closure

Date: 2026-10-02. Status: **passed**, including the final scalar fallback
and repaired GLS bit interface. Scope: the actual draft
[smoothed-sparse-polynomial.md](smoothed-sparse-polynomial.md), its
[finite-noise interface](polynomial-finite-noise-tails.md), and the
[convex-patch evaluation lemma](convex-patch-evaluation.md).

The sparse rounding, expected table counts, and deterministic closure pass
this review. The completed scalar algebraic fallback also passes. The
rational-ellipsoid interface required an explicit feasibility repair;
the repaired formulas below have passed independent review and are
incorporated in the evaluation note. Approval concerns that repaired
interface, not the earlier assertion that weak optimization directly
returns an exactly feasible epigraph point.

## Deterministic argument

Sequential coordinate semiconcavity gives the stated rounding error
`E_j=n L h_j^2/8` for a fixed-degree polynomial. It does not require
quadratic cross-term cancellation. The curvature bound must hold on the
continuous hull, including segments between integer labels. The reviewed
nested-cell argument preserves all bag whitelists under this rounding;
thus a retained cell has one globally consistent feasible witness with
gap at most `2E_j`. Independent per-bag witnesses would not suffice.

Conditional minimization outside a bag preserves coordinate upper
curvature because an infimum of concave functions is concave. Its feasible
set is independent of the bag values, and the conditional value function
is independent of all bag noise. The two-neighbor comparisons therefore
give coordinate noise intervals whose lengths are bounded independently
of the other bag coefficients. This justifies the product bound. Integer
singleton cells below unit resolution and the finite-law atom term are
both retained in the draft. No independence of adaptively retained cells
is assumed.

The closure constants in (16) are sufficient. Under the good event, each
retained coordinate lies within `A h_j` of the optimizer. Integer cells
then identify all integer labels exactly. For a hull midpoint `c` and
radius `r`, the computed interval
`partial_i F(c)+[-M_1 r,M_1 r]` differs from the gradient at the optimizer
by at most `2M_1 r`. The factor four in the gradient cutoff is therefore
appropriate. Only original continuous endpoints are forced by this test.

After those endpoints are fixed, every remaining original continuous
coordinate is interior at the optimizer. Point growth implies
`H_CC(a)>=2g_0 I` by a two-sided Taylor expansion. No quantitative lower
bound on its distance to an original boundary is needed. The third-
derivative row-sum estimate gives
`||H_CC(x)-H_CC(c)||_2<=Tr`. At the stated cutoff,

```
H_CC(c)-(Tr+g_0)I >= (g_0-2Tr)I >= (g_0/2)I.
```

The rational matrix test thus passes and proves uniform positive curvature
throughout the retained box. All these closure tests are sound on every
draw. Growth and gradient margins enter only the proof that they succeed
by the chosen level.

This is a real extension of the earlier patch hypothesis: the full
continuous Hessian at a boundary optimum may be indefinite. The algorithm
first fixes that boundary, then certifies the remaining block.

For example, let `u=x-1/3`, with `x in [0,1]`, `y in [0,1/4]`, and
`z in {0,1}`, and set

```
F=u^2+u^4+2y-y^2+(z-1)^2+uy+y(z-1).
```

The two cross products are bounded below by
`-u^2/4-y^2` and `-(z-1)^2/4-y^2`. Hence growth at
`(x,y,z)=(1/3,0,1)` is at least `3/4`. Bounds `L=8`, `M_1=9`, and
`T=16` are valid. The active gradient is `partial_y F=2`, but
`partial_yy F=-2`: a full continuous convex patch would fail, whereas
fixing `y=0` leaves curvature at least two. This is an algebraic sanity
check of the distinction, not an end-to-end implementation test.

## Probability and exact output

The finite-noise note uses point growth at one optimizer. Set-relative
growth would be insufficient: it can hold at tied optima and would not
justify integer identification or unique-patch closure. The two-block
formula encodes the required point property directly. Its scalar-section
complexity bound is uniform in fixed real coefficients, which is needed
for the continuous/discrete hybrid comparison.

The active-gradient argument properly counts only nonsingular free
stationary roots. Positive point growth supplies nonsingularity at the
relevant optimizer; the proof does not assert that all stationary sets are
finite. The active coordinate's linear noise does not enter those free
equations. The degree-zero/one and zero-dimensional-face cases are covered
by `max(1,d-1)` and the empty-system convention.

The same finite law can have tied or flat draws. Consequently the hybrid
output contract is necessary: a verified unique convex patch when closure
succeeds, and an exact algebraic selected optimizer on fallback draws.
An every-draw unique-patch assertion would be false.

The capped-epigraph reduction in the evaluation note is valid. Its known
inner ball avoids any strict-interior assumption on the optimizer, and
its objective is the globally linear coordinate `t`. Strong convexity
converts a gap of at most `g_0 2^(-2q)/2` into distance at most `2^-q`.
The required numerical conditioning enters only through its binary
encoding. Reusing the earlier grid evaluator with a numerical factor
depending on `L/g_0` would not establish the desired smoothed evaluation
bound.

The fallback obligation is precisely
`B_base poly(I+log M+q)`, with `log B_base=poly(I)` and `B_base`
chosen before sampling. It must cover construction and refinement of an
exact algebraic sample at a global minimum, including positive-dimensional
optimal sets. An undifferentiated exponential in sampled coefficient
height would not justify the stated probability budget. The completed
[scalar fallback](polynomial-exact-fallback.md) establishes this interface:
compactness gives one lexicographically first optimizer; two-block scalar
formulas describe each of its coordinates and its value as singletons.
Renegar's count, degree, and coefficient-height bounds separate the base
factor from sampled bit length. Univariate squarefree reduction, isolation,
and sign determination then recover the correct root of each formula.
All coordinates refer to the same canonical optimizer. The extra feasible
rational approximation in its Section 6 is also valid: exact integer
labels, clipped continuous approximations, and an `l_1` gradient bound give
the claimed original-domain objective gap. This review read the completed
fallback file rather than relying only on its proposed interface.

## Necessary presentation qualifications

Two corrections were sent to the author after reading the actual draft
and are now applied:

- The compact successful patch descriptor has polynomial length in the
  base input. A full global-containment DP trace has the expected work
  bound; no every-successful-draw polynomial trace-size bound was proved.
  Separate the descriptor used for later evaluation from its global proof
  trace.
- A valid supplied `L` is a mathematical input promise. For an independently
  checked global certificate, derive `L` by the stated monomial method or
  include a verifiable sharper-curvature proof and charge its size and
  verification cost. Verifying an arbitrary sharp polynomial curvature
  estimate is not free.

The evaluator's classical source attribution required a substantive repair.
Dadush's theorem uses an oracle arithmetic-operation convention. GLS gives
the needed rational bit interface, but its weak-optimization output lies
in an `epsilon` neighborhood of the body and compares against its
`epsilon` erosion. It does not directly provide exact epigraph feasibility.

The following repair is explicit. Let `r_K` be the known epigraph inner
radius, with center `(c,W+1)`, and let `G>=max{1,sup_B||grad f||_2}` be
a rational monomial bound. Put

```
A=1+(2W+1)/r_K,       C=G+2+(2W+1)/r_K.
```

For `epsilon<=r_K/2`, homothety of an optimizer toward that center with
weight `epsilon/r_K` lies in the erosion and increases its `t` coordinate
by at most `epsilon(2W+1)/r_K`. Consequently GLS's returned `(x,t)`
satisfies `t<=f*+A epsilon`. Choose a point of the epigraph at distance
at most `epsilon` from `(x,t)`. Projection of `x` onto the rational box
cannot increase distance to that point's box coordinate. Thus the exactly
feasible rational point `xhat=proj_B(x)` satisfies

```
U=f(xhat)<=t+(G+1)epsilon,
t-A epsilon<=f*<=U,
U-(t-A epsilon)<=C epsilon.
```

Choose `epsilon<=min{r_K/2,eta/C}` for the desired gap `eta`.
All constants and oracle queries have polynomial bit length. Exact rational
strong separators cover box violations, the top epigraph cap, and the
convex tangent plane. The root reviewer checked these signs and constants
against GLS Definition 2.1.10 and Corollary 4.2.7, and checked the Turing
oracle conventions in Sections 1.2--1.3 and 4.1. The main author independently
checked the same repair. This is the bit-model route used by the approved
composition.

This reviewer also read GLS Definition 2.1.10, Section 4.1, and Corollary
4.2.7 in the local primary text. Their maximization convention becomes the
stated minimization inequality by choosing objective `-t`. Its circumscribed
outer ball is centered at the origin: translate the epigraph by its rational
center or add that center's `l_1` norm to the stated outer radius. Either
choice preserves polynomial encoding length.

## Significance and verification scope

With those interfaces, this yields discovery for arbitrary integer
dimension and fixed-degree sparse nonlinear objectives under one finite
linear-noise law, with exact implicit output and polynomial-bit evaluation.
It does not plant a rational optimizer or assume a boundary Hessian
condition. Its rate is fixed-width expected polynomial under the stated
numerical ratio; it is not FPT in width and does not control the original
unperturbed optimum. The expected cell argument and filtering mechanism
come from the quadratic predecessor. The new obligations are polynomial
finite-law control and exact local convex-patch closure.

This review read the actual drafts and the local Dadush statement. It used
direct mathematical checks and the displayed algebraic fixture. It did
not rerun the predecessor's DP tests, run project-wide verification, inspect
CI, search externally, or edit an index. The author's focused implementation
checks and the other fallback reviews remain distinct evidence.
A targeted document check passed for whitespace, paired fenced blocks,
and local links.
