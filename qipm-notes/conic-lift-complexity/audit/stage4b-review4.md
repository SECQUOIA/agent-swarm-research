# Stage 4B independent review 4

Reviewer: `/root/stage4b_review4`; 20 September 2026.

I personally read all five new sections 09a–09e, the universal local
curvature and reduction lemmas, the joint-cover/proper-phase results in
08a, the lp author audit, and the relevant lp workbench notes. I did not
read the other reviewers' reports or edit the manuscript.

**Disposition: no major issues; one minor hypothesis clarification.**

## Minor issue: declare the dimension cap to be an integer

Locations: `sections/09d-lp-power.tex:20` (`thm:lp-granularity`),
`:156–157` (`thm:lp-smooth-frontier`), and the cap setup
`sections/09b-face-sharing.tex:16`, used by the exact ray-exposed frontier.

The exact formulas use `d-2`, including partitions into integer group
sizes and the divisibility alternative in the global count proof. The
statements do not explicitly say that the cap d is an integer. A bound
on cone dimensions can also be given by a real number, in which case the
effective cap is floor(d), and the displayed exact formulas need not hold.
For example, N=4 and d=7/2 in the generic lp theorem would predict two
factors, but every allowed factor has dimension at most three and hence
capacity at most one, so three are necessary. Similarly N=3,d=7/2 in
the global theorem predicts two factors when three are necessary.

Proposed correction: state an integer d>=3 once in the setup of 09b and
in both exact-frontier theorems of 09d (or introduce a clear common
integer-cap convention). The capacity-excess proposition then inherits
the intended integer cap. This is a minor statement precision issue,
not a defect in the integer-cap proofs. The corresponding source
granularity note explicitly assumes integer d.

## Mathematical checks completed

- **09d generic counts:** the nonzero-coordinate patch has positive
  curvature for all 1<p<infinity; minimal-face reduction and definable
  selection apply. Zero-capacity factors cannot improve either objective.
  The chain has exactly N leaves, each cone dimension is b_i+2, and the
  inverse assignment by subtree norms and Slater assignment are valid.
  The rational-power description respects nonnegative roots. Padding
  realizes every integer excess while preserving full minimal faces.
- **09d equality and nonrigidity:** the diagonal nonnegative kernels give
  positive semidefinite mixed forms on a common smooth contact chart.
  Rank equality yields the square Parseval matrix and orthogonal
  projections; both quotient derivatives are onto. The half-cone example
  has strict feasibility, a two-dimensional exposed face, and the same
  curved local germ. No global cone classification follows or is claimed.
- **09d global frontier:** the primal and polar boundaries are independent
  C1 manifolds. Their tangent pairing is nondegenerate without
  differentiating the polarity map. The continuous contact map exists
  by strict convexity. Joint-cover equality excludes strict-cap capacity
  N-1 for N>=3. The grouped Young dual belongs to the dual cone, has
  correct whole-slice multipliers and objective value, and is C1 at
  coordinate zeros. The ambient and intrinsic barrier lower bounds are
  distinguished, and the p=2-only attainment qualification is correct.
- **09d two-dimensional exception:** the power cone has exactly one
  non-C2 axial ray unless it is Lorentz. The p-circle has four such rays
  for p<2, none for p>2, and four points of vanishing projective second
  fundamental form for p>2. These invariants, together with the proved
  minimum-dimensional rigidity, exclude a one-power-cone lift for p!=2.
  The argument includes affine maps and free variables.
- **09d new generalized-power bound:** sum x=1 is a compact section of
  dimension m+k-1, and restricting a lift introduces no factors. The
  weighted variance vanishes only for h proportional to x; the simplex
  tangent removes that direction. The spherical term and tangent
  equation then remove all xi directions. Thus the tangent Hessian has
  rank m+k-2. The cases m=1,k>=2 and k=1,m>=2 work separately as stated.
  The nonnegative scalar cone uses its positive upper graph, so no
  absolute-value boundary issue arises. This is a dimension bound, not
  a denominator-sensitive exact SOC count.
- **09a:** the ordinary affine-function rank and contact-cylinder rank
  yield the stated whole-row bounds; extreme polar normals suffice for
  all exposed-face bounds. Minimum-dimensional rigidity works for both
  exact lifts and arbitrary full-slack factorizations. Connected extreme
  sets exclude products at equality but do not justify a per-factor
  tax. The finite closed-cover proof gives that tax only for a single
  normalized product base. Recession sublevel compactness, attained
  minima, and the strict normalization level needed for barrier
  restriction are correctly proved. The escaping-disk counterexample
  addresses arbitrary projection-preserving affine restrictions.
- **09b:** the cross-contact annihilation identities establish the direct
  sum of the radial vector and active source derivative spaces. The
  compact active-label pieces, proper source neighborhoods, and top-class
  cover prove the global budgets. The resource inequalities use a
  monotone function of L correctly. Shared-square face dimensions,
  function ranks, and completion-barrier lower sections are consistent.
- **09c:** the minimal-face criterion restricts extreme points to one
  or two primitive blocks. The sign geometry and paths also handle the
  disconnected two-point zero region and the Albert chart. The diagonal
  orthant/simplex sections inherit the boundary, and the restricted
  gradient norm calculation gives rho-1. The cap comparison concerns
  different bodies, as explicitly stated.
- **09e:** the spectral mixed rank includes the imaginary scalar phase
  channel and is delta*c-1, also for quaternions. The whole-row contact
  codimension is delta*(r+c-1). The explicit recession certificate gives
  R+g for arbitrary coupled barriers, rather than only homogeneous ones.
  The slice gradient norm and diagonal cube prove parameter R. The
  completion cone is closed because diagonals bound all completion
  entries; the signed Legendre transform, clique/separator formula, star
  slack maps, and fixed-coordinate Newton equivalence are correct.

## Literature and scope check

I read the local Wang, Blanco–Martínez-Antón and Krokhmal–Soberanis
literature records, then checked these primary sources online:

- [Wang's published paper](https://wangjie212.github.io/jiewang/research/wgm.pdf),
  Theorems 3.6 and 3.15, printed pp. 1495 and 1497: the manuscript
  accurately separates the simple-representation m-1 bound from the
  arbitrary affine SOC-lift m/2 bound.
- [Blanco–Martínez-Antón](https://arxiv.org/html/2311.10470v2), Definition 1
  and Theorem 14: their stated correspondence is broad, while the
  displayed construction uses mediated variable triples. The manuscript
  appropriately declines to infer scalar priority from this comparison.
- [Krokhmal–Soberanis journal PDF](https://stacks.cdc.gov/view/cdc/226421/cdc_226421_DS1.pdf),
  Proposition 1 and Appendix A: the classical p-norm tree attribution and
  corrected title are supported.
- [MOSEK Modeling Cookbook 3.4.0](https://docs.mosek.com/modeling-cookbook/powo.html),
  Section 4.2.2: the scalar Young model is established prior modeling.
- [Fawzi–Saunderson](https://arxiv.org/html/2205.04581v3), Theorem 3.9:
  Nesterov's recession bound has exactly the hypotheses used for the
  shared spectral cones and permits arbitrary self-concordant barriers.
- [Andersen–Dahl–Vandenberghe](https://arxiv.org/pdf/1203.2742), Section 1.2,
  equations (3)–(4): the signed conjugate barrier and inverse completion
  characterization match the manuscript.

I found no unsupported novelty claim requiring revision. Classical trees,
Young models, spectral/completion barriers, and full-slack equivalence are
attributed; original claims are tied to explicit representation and
regularity hypotheses. This review does not certify absence of all prior
work. Stage4C and Stage5 deferrals are outside this stage and are not
treated as completed claims here.
