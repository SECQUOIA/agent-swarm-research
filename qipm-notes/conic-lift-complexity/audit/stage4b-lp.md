# Stage 4B author audit: norm balls and power cones

Owned manuscript: `sections/09d-lp-power.tex`. Bibliography additions are
in `audit/stage4b-lp-bib.txt`. No main file, bibliography, other section,
workbench note or literature package was modified.

## Coverage

- `2026-09-04-lp-ball-exact-cone-granularity`: all exact tame count and
  dimension claims, curved-patch proof for all 1<p<infinity, rational
  semialgebraicity including even denominators, tree attainment, Slater,
  zero-capacity rays and endpoint exclusions are in
  `thm:lp-granularity`. Ambient universal 2k lower bound is already
  proved in 08a and is applied to smooth counts here; nonsymmetric
  factor premium is deferred to 4C as assigned.
- `2026-09-04-lp-count-saturation-equality`: exact reduced-dimension
  excess interval, every-excess padding construction with full minimal
  faces, divisible-case full-cap rigidity, local orthogonal projections,
  and quotient derivative surjectivity are included. Original and
  reduced dimensions are distinguished. No global rigidity or arbitrary
  dictionary barrier premium is inferred.
- `2026-09-04-curvature-saturation-nonrigidity`: half-cone construction,
  exact elimination, full-face Slater, saturated minimum count, exposed
  facet nonisomorphism, and identical local boundary germ are included
  in `ex:lp-halfcone`. The elementary projection identity is integrated
  with the preceding equality discussion.
- `2026-09-04-smooth-lp-perspective-cone-optimality`: all exact global
  capacity/count/dimension values, cap transition, independent primal and
  dual C1 boundary differentiations, perspective closure/properness,
  Slater, unique primal boundary fibers, whole-slice normalized dual
  certificates, and Young identity are in `thm:lp-smooth-frontier`.
  The stronger reviewed joint-cover theorem replaces the source's
  individual-submersion classification. The grouped intrinsic-barrier
  lower bound is proved by restriction to an embedded h-dimensional
  box; the p=2 exact case is cross-referenced to Stage 3 and no matching
  p!=2 upper bound is asserted.
- `2026-09-04-young-power-cone-lp-factorization`: scalar specialization,
  standard-model prior attribution, C1/C2 regularity ledger, global
  three-cone count N for N>=3, and complete N=2 exception proof are
  included. The source's erroneous assertion that both endpoints of
  [N h(p),3N] equal 2N at p=2 is not propagated. The premium and
  unresolved optimum are assigned to 4C.

## Independently developed extension

`thm:power-capacity` proves the proposed bound for generalized Euclidean
power cones: sum positive dimension-minus-two capacities >=m+k-2.
Its proof restricts the original lift by the single affine equation
sum x=1; no new cone factor is needed. The section has dimension
m+k-1. On x>0, z!=0, the defining function ||z||-g(x) has tangent
Hessian equal to a positive weighted-variance term plus the spherical
term. The only common null vector has h proportional to x, sum h=0,
and xi proportional to omega with omega dot xi=Dg[h]; hence h=xi=0.
The scalar nonnegative geometric-mean variant is proved separately
on its upper graph. The statement includes m=1, k>=2 (ordinary SOC)
and k=1, m>=2, excludes the dimension-zero curvature case m=k=1,
and allows rays, arbitrary affine maps and free variables. Minimal-face
reduction only decreases the original dimensions. No matching count
for all weights or denominator-sensitive lower bound is asserted.

## Additional proof development

The N=2 power-cone assertion in the notes was conditional on an
uncited projective regularity lemma. The manuscript supplies the
actual local graphs: |w|^(1/alpha), |w|^(1/(1-alpha)) at the two
power-cone axes, versus 1-|t|^p/p+o(|t|^p) at each of four p-circle
axes. Exactly one versus four/nonexistent non-C2 rays separates every
non-Lorentz power cone. The Lorentz case requires a separate check:
for p>2 the p-circle's zero second fundamental form at four axes
separates it from a nonsingular conic. This condition is preserved
under projective maps. The minimal-space rigidity dependency is
`thm:minimal-dimension-rigidity`, to be integrated by the 4B author.

## Primary literature reviewed

Read local Krokhmal–Soberanis metadata package (marked unread; not
modified), local Wang reader package and the source notes. Online
primary checks on 20 September 2026:

- Krokhmal–Soberanis, publisher metadata and open full journal PDF
  https://stacks.cdc.gov/view/cdc/226421/cdc_226421_DS1.pdf.
  Proposition 1, printed p.658, and Appendix A state/prove the J-1
  three-dimensional p-order cone construction. **Correction to notes:**
  the title attached to DOI 10.1016/j.ejor.2009.03.053 is *Risk
  optimization with p-order conic constraints: A linear programming
  approach*, EJOR201(3)(2010)653–671, not *A unified approach for
  modeling risk preferences in portfolio optimization*.
- Wang author-hosted published PDF
  https://wangjie212.github.io/jiewang/research/wgm.pdf.
  Theorem3.6, printed1495, states m-1 for simple representations;
  Theorem3.15, printed1497, defines arbitrary affine K^l lifts and
  proves l>=m/2 by face chains. Corollary3.12 is denominator-sensitive
  in the simple representation model. Our paragraph accurately
  distinguishes these models and does not claim scalar priority.
- Blanco–Martínez-Antón primary full text
  https://arxiv.org/html/2311.10470v2, Definition1, Theorem14 and proof.
  Definition1 broadly speaks of projections; the constructive proof
  explicitly selects triples of mediated variables and asserts a
  converse. The manuscript records this established comparison
  without alleging a gap or asserting that its priority excludes our
  scalar dimension bound. Exact affine maps are explicit in our own
  theorem. Published metadata as root already verified:
  SIOPT34(3)(2024)3088–3111, DOI10.1137/23M1617205.
- Official MOSEK Modeling Cookbook3.4.0,
  https://docs.mosek.com/modeling-cookbook/powo.html, Section4.2.2,
  eq4.7 gives the identical coordinatewise Young power model.

Additional searches for lp-ball arbitrary-cone dimension lower bounds,
geometric-mean SOC curvature bounds, and minimal p-order cone
representations found the foregoing representation papers and no
direct collision with the arbitrary proper-cone/global-C1 frontiers.
This is a targeted search, not proof of absence; precise theorem
statements carry the contribution claims.

## Scope cautions for integration and five reviewers

The manuscript's unrestricted theorem is definable and needs only one
curved patch. The global theorem does not need definability but does
require C1 selections on *both entire independent boundaries*. No
differentiation of the non-C2 Gauss map occurs. Capacity equality only
determines local derivative projections and not global cone types.
The grouped ambient parameter lower bound is not an intrinsic slice
lower bound or a matching nonsymmetric upper bound. The GM extension
is independently proved and should receive mathematical review,
including compact-section restriction and all edge cases.

## Verification

A standalone syntax build through the qipm environment's Python and
pdflatex exited successfully, producing five pages with no overfull
boxes. Log: `audit/stage4b-lp-syntax.log`. Cross-section references and
bibliography entries are intentionally unresolved in this isolated
syntax harness; the integration author must resolve them in the full
manuscript. Checked existing section labels `sec:regularity` and
`sec:concrete-barriers`. The sole new external theorem dependency is
the assigned whole-row helper's `thm:minimal-dimension-rigidity`.
