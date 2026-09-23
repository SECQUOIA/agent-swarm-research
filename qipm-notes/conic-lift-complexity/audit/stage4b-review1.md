# Stage 4B independent review 1

Reviewed all of `09a-whole-rows.tex`, `09b-face-sharing.tex`,
`09c-balance-slices.tex`, `09d-lp-power.tex`, and
`09e-spectral-chordal.tex`, plus the relevant reduction, curvature,
normalized-phase, and bounded-fiber results in Sections 1, 7, and 8A.
I read the author handoff and the Stage 4B source dispositions. I did not
read the other reviewers' reports or edit the manuscript.

**Assessment: no major issue found. One minor hypothesis correction is
needed.** The correction makes an intended discrete parameter explicit;
it does not require changing the results for their intended integer caps.

## Required minor correction

### R1. State explicitly that the dimension cap is an integer

Locations:

- `sections/09d-lp-power.tex:20`: the generic exact frontier assumes only
  `d >= 3` as written.
- `sections/09d-lp-power.tex:157`: the global exact frontier repeats that
  omission. Its dependent capacity-excess proposition also uses the same
  integer-cap convention.
- `sections/09b-face-sharing.tex:16`: the setup for the global budgets and
  exact ray-exposed frontier does not explicitly make `d` an integer;
  the attainment assertion at lines 151--161 needs this convention.

The formulas do not remain exact for an arbitrary real cap. For example,
in the generic norm-ball theorem take `N=4` and `d=3.5`. The displayed
formula gives two factors, but every allowed factor has integer dimension
at most three and curvature requires at least three such factors. The
global theorem has the same problem: at `N=4,d=3.5` it gives three factors,
whereas its integer-cap-three result requires four. In the ray-exposed
frontier, `p=3,d=3.5` similarly gives `h=3` instead of four.

**Fix:** state `d` is an integer at the start of the face-sharing setup and
in both norm-ball theorems (or adopt an explicit section-wide convention).
This matches the existing integer wording in the earlier proper-cone
smooth-frontier corollary. An alternative is to replace the real cap by
its floor throughout, but that is unnecessary complexity here.

## Mathematical checks

- The whole-row function-rank argument recovers the constant and all
  coordinates. Restricting the same functions to a contact cylinder gives
  the stated face dimension. The maximum exposed-face calculation for the
  shared homogenization correctly uses extreme polar normals, and the
  arbitrary-normal intersection argument supplies the required upper
  bound. The `F=0` and infeasible-group cases are handled by the grouping
  inequalities.
- Minimum-dimensional rigidity correctly eliminates free variables before
  counting dimensions. At equality the projection on the hyperplane is
  injective, which gives compactness of the slice. Strict positivity of
  its height functional follows from the two recession contradictions.
  The affine output is extended linearly only after establishing that
  this hyperplane misses zero. The separate full-slack proof correctly
  obtains equality by dualizing the second cone inclusion.
- The normalized-base proof does not need a closed extreme-point set.
  Its finite cover is relatively closed in that set, so a disconnected
  intersection graph would contradict connectedness. Empty cover members
  are discarded before using a spanning tree.
- The recession-height proposition is valid for a closed line-free set.
  Strict positivity on the recession cone makes every nonempty height
  sublevel compact; this proves that the fiber minimum is attained. A
  nonzero recession ray preserves the projected point and raises its
  height. Choosing the level above a relative-interior point ensures
  that the restricted barrier is defined on the correct relative
  interior. The polytope corollary uses finitely many vertex lifts to
  supply the otherwise missing uniform height bound. The escaping PSD
  disk correctly shows why compact projection alone does not supply it.
- The face-sharing direct sums follow from the cross-contact derivative
  identities using only first derivatives. The exact-active-label pieces
  in the top-class proof are compact; the normalized dual maps are defined
  on neighborhoods of their projections because contact primals remain
  nonzero. The dimension budget is monotone in the actual factor count.
  The ambient lower bound is obtained by product sections, so it applies
  to coupled barriers.
- The shared-square face calculation includes both equality and strict
  dual cases, including `q=1`. The ordinary function rank and contact
  cylinder rank give the claimed minimal resources. Its completion
  barrier and orthant section independently prove the parameter optimum.
- The balance section's extremality classification, two-block paths,
  real rank-two exception, and Albert chart argument are consistent.
  The two octonionic chart coordinates generate an associative algebra,
  which justifies the displayed idempotent calculation. The diagonal
  orthant/simplex sections inherit the boundary. The trace-hyperplane
  gradient norm gives the matching `rho-1` upper bound; the further
  balance restriction can only decrease it. Essentiality uses another
  block, as allowed by `L >= 2`.
- The norm-tree construction has the claimed number of leaves and cone
  dimensions, and positive decreasing internal variables give Slater
  feasibility. Padding at fixed zero coordinates preserves full-face
  Slater feasibility. The global Young factors give genuine certificates
  on the whole affine slice and remain `C^1` at coordinate zeros.
  The two-dimensional power-cone exception uses projectively invariant
  boundary regularity/flatness, with the Lorentz case checked separately.
- The generalized power-cone section is compact and has the required
  dimension. Its weighted variance Hessian is positive on the simplex
  tangent; the Euclidean output supplies the remaining spherical
  directions. The `m=1` and scalar-output cases agree with the claim.
- The spectral mixed-rank count includes the imaginary scalar channel,
  including the quaternionic case and the zero-rank real scalar case.
  The whole-row contact codimension and general rank-`h` face formula
  agree with the singular-value equality conditions.
- The explicit spectral recession certificate satisfies all hypotheses
  of the cited lower-bound theorem and can be put in direct summands to
  handle coupled barriers. The slice gradient-norm computation and real
  diagonal cube give matching upper and lower parameters.
- The completion cone is closed because specified bounded diagonals
  bound every completion entry. The Legendre/maxdet proof works without
  chordality; the separator identity is reserved for chordal graphs.
  The block-star slack factor has the correct factor of one half and is
  independent of the rank-one representation's common phase. The two
  reduced formulations really do have the same barrier and derivatives;
  the text correctly excludes ambient oracle-construction claims.

I also checked the rejected coupled-log example directly: its displayed
one-variable restriction gives second derivative `13/4` and third
derivative `25`, which violate self-concordance.

## Literature and scope checks

I consulted the local GPT, Nesterov--Nemirovskii, Krokhmal--Soberanis,
Wang, and Blanco--Martínez-Antón packages. I checked the following primary
online texts where needed:

- [Lee--Yue, Theorem 2](https://manchungyue.com/nSC.pdf): the dimension
  upper bound for the universal barrier supports the polytope endpoint.
- [Fawzi--Saunderson, Theorem 3.9](https://arxiv.org/html/2205.04581v3):
  the recession-direction lower bound has precisely the hypotheses used
  by the spectral certificate and does not require logarithmic homogeneity.
- [Andersen--Dahl--Vandenberghe, Section 1.2](https://arxiv.org/pdf/1203.2742):
  the signed conjugate barrier and maximum-determinant completion identity
  are classical as stated in the manuscript.
- [Coey's thesis, Section 2.6.1](https://chriscoey.github.io/assets/pdf/phd_thesis.pdf):
  the rectangular real/complex spectral barrier has the stated formula.
- [Wang, Theorems 3.6 and 3.15](https://wangjie212.github.io/jiewang/research/wgm.pdf)
  and [Blanco--Martínez-Antón, Definition 1 and Theorem 14](https://arxiv.org/html/2311.10470v2):
  the manuscript appropriately distinguishes the simple mediated
  representation count from its affine-lift curvature proof and does not
  claim unsupported scalar priority.

The corrected Krokhmal--Soberanis title, DOI, and journal data agree with
the [publisher record](https://www.sciencedirect.com/science/article/abs/pii/S0377221709002264).
The stage does not claim that classical spectral/completion barriers or
norm trees are new, and its explicit deferrals to movement and
nonsymmetric-barrier stages do not present those results as already proved.

After the integer-cap correction, I recommend accepting this stage without
a major-issue review cycle.
