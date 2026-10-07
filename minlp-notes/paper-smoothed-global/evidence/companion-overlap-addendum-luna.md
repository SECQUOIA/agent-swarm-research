# Decomposition-aware companion overlap addendum

This addendum records a read-only comparison with the local companion named
in the submission bibliography. It narrows the companion attribution audit;
it is not an external literature search, a proof review, or a priority claim.

## Identities and audit target

The companion's exact cited identity is **“Decomposition-aware global
optimization: certified coordinate grids, conditional recourse, and
structural limits,”** undated, unpublished companion manuscript
(`paper-smoothed-global/references.bib`, entry
`companion-decomposition-aware`). Its local `main.tex` has the same title
and blank author/date fields. The scientific comparison target is the frozen
submission snapshot, not later working-tree prose:

- R4 manifest SHA-256:
  `0c48e0cda82b7a4f25be956980b536577311fa71d40220cc35c8d1a47d0af061`.
- Relevant R4 files: `sections/01-introduction.tex`
  `cd485550abc8ad8a5cb6e80c003b3dd6e2178e287e504f2832992560b3a4db67`;
  `sections/05-sparse.tex`
  `df3ef7c7f7c08d415044d9d93e3f9daa9b8a5d6c301954b950c3130c6718f047`;
  `sections/06-constraints.tex`
  `9467eb72e20f355b3afb70d844bfedcf0a7fe52ba8f53d2483327162ad9db898`;
  `sections/07-recourse.tex`
  `6dbb5f51199e261d613afbe67a88b4bd9f8f43dfc3c2fd6bb34a22243f659c6b`;
  `sections/09-boundaries.tex`
  `fcc8051f9f19582837624ce11d8db5f49b8a2520ed934bf8870f119815c13761`.

The local companion source identities inspected here are:

| Local source | SHA-256 |
| --- | --- |
| `paper-decomposition-aware/main.tex` | `48d31b03b7f8bf68c4ac550b5acd9c37e59202d334ac87a859fc7afa341f28fd` |
| `paper-decomposition-aware/main.pdf` | `9430ba8ddb645b0d151963fdad37657efb131ca2ac59738e77a9196c139e8c63` |
| `sections/recourse-valuefn.tex` | `9b09bcbf05b5c0a6837d726989d02c0c670eb3e6d201a3673f50764f17fb6893` |
| `sections/recourse-local.tex` | `76871799ba2e780bc4030e07d55e054647eb7f9a293fbb922595bee37c0649e6` |
| `sections/appendix-recourse-convex.tex` | `7398cbff164d710e9f4c9aa1ae79a815c43e887c22b0e7c2b02a556962a15d0c` |
| `sections/recourse-cuts.tex` | `b794a375486d95893457f261c40ec489b4763a108909e4286a04565d38783a2e` |
| `sections/constraints.tex` | `65a2e8eb79145df34b27c21687235bc58a11c22019e87fae7365ea3510e4ef86` |
| `sections/grids.tex` | `b0f29cb640c7ceb55aaafb6ca4e282e1ad2e3acb0c7c3a03f820a75e4ebf1e74` |
| `sections/growth.tex` | `452c709bad4696bae10bed46b7891fc284bd8ca407c97ca5159c6393684d4a68` |
| `sections/growth-sharp.tex` | `635c03f1171da83bb52ff5e06337a27b44e7fae75d52b74669d9ab4dc5fe2cf5` |
| `sections/limits.tex` | `066dd1ce8dc49b323c920c26418f5626835fce62e34e6c4d75b01a7099fc44cf` |
| `sections/exact.tex` | `1427820ba895688fc67517568d685a1f223c1bba57da8ec9f7e7c4f502dda88c` |
| `sections/appendix-boundary.tex` | `7d70f537e3ad447c1a6576f7102c302e56d2357a12bd7f0b410760850ee6b7bf` |

## Exact overlaps and contribution boundary

| Companion result and locator | R4 counterpart | Comparison and attribution |
| --- | --- | --- |
| `lem:valuefunction(a)`, `recourse-valuefn.tex:16–25` | `lem:rec:value(b)`, R4 `sections/07-recourse.tex:110–124` | Both establish that minimizing over a fixed residual feasible set preserves the retained/core coordinates' upper coordinate-curvature bound. Companion part (b) separately transfers point growth with the same constant; R4's other parts instead separate core noise from the conditional value and prove a Lipschitz bound for every nonempty closed residual subset. The curvature inheritance is deterministic overlap, not a smoothed result. R4's mechanism paragraph (`sections/01-introduction.tex:219–227`) states the rule but does not credit this companion lemma by name. |
| Deterministic corrected grids, min-marginal dynamic programming, and certificate recomputation, companion `sections/grids.tex`, `sections/exact.tex`, and `sections/recourse-cuts.tex` | R4 `sections/05-sparse.tex:1113–1145`; R4 intro `sections/01-introduction.tex:487–512` | The companion supplies the deterministic grid/filter/certificate pipeline. R4 already identifies corrected coordinate grids, min-marginals, growth-free certificate validity, and deterministic growth-conditioned bounds, and says it re-proves the needed pipeline. Do not attribute these deterministic mechanisms to the finite perturbation law. |
| `prop:sharp` and `cor:uniformgrid`, `sections/growth-sharp.tex:12–48`; `prop:lbproduct`, `sections/limits.tex:341–365` | R4 intro `sections/01-introduction.tex:501–510` | The corrected lower bound `sqrt((n-2) kappa)+1` is for stages of the specified filtered common uniform-grid method on its stated box family. The rETH result excludes a sublinear width exponent only in its stated product-time model for unique-minimizer integer box QP with a supplied decomposition; it is not a smoothed lower bound or a matching `p/2` result. R4 already preserves these limitations. Neither bound applies to all algorithms or to R4's different sparse smoothed count. |
| `thm:cr-search`, `recourse-cuts.tex:139–190`, and `prop:cr-growth`, `:192–204` | `prop:rec:search`, R4 `sections/07-recourse.tex:181–240` | CORE uses exact conditional values on adaptive dyadic core cells. Per level it retains cells containing an optimizer projection, bounds `lambda_j <= OPT <= U <= lambda_j + e_j`, gives a near-optimal corner in each retained cell, and returns a checkable global lower-bound record. Under point growth, `prop:cr-growth` bounds queries by `2^k + 8^k J(1+sqrt(k kappa_K))^k`; the growth constant is not an algorithm input. R4 `prop:rec:search` parts (a)–(c) give the deterministic optimizer-retention, incumbent, and witness facts, also with certified oracle answers. It does not state CORE's part-(d) global lower-bound record; its later closure tests handle global containment. R4's distinct addition is the conditional-on-residual-noise expected count for each fixed level through `J`, without a growth premise, when `M >= 2^J`: expected calls are at most `2^k + 8^k J Q_ex/ap`. Credit the deterministic CORE facts; keep the finite-law count and expected-work bound as the smoothed contribution. |
| `thm:cr-filter`, `recourse-local.tex:7–77` | `prop:sp:conditional(a),(b)` at R4 `sections/05-sparse.tex:598–631`; `prop:lim:conditional` at `sections/09-boundaries.tex:297–312` | The companion theorem is a deterministic certified bag-cell filter for an arbitrary finite cell family and recourse-value oracle. It retains minimizer-containing cells and gives near-optimal corners; its lower-bound/gap statement applies to points whose bag projection lies in the supplied cell union. R4 specializes the retention and witness parts to scheduled sparse cells with error bounded by `a e_j`; its part (c) adds an expected near-optimal tuple count under the finite law. R4 already credits parts (a),(b) at `sections/05-sparse.tex:689–692` and the companion pipeline at `:1131–1145`. The expected count is not in the deterministic companion theorem. |
| `prop:star`, `appendix-recourse-convex.tex:144–176` | `ex:rec:star`, R4 `sections/07-recourse.tex:153–179`; `prop:lim:local`, `sections/09-boundaries.tex:228–287` | R4's unperturbed star example is exactly companion family (A) with `m=32`, `h=1/2`, and `epsilon=1/16`. Companion family (A) shows required constant correction grows with leaf count while its available growth constant degrades. Family (B) is stronger in a different direction: it keeps `kappa < 11` while forcing a correction of order `sqrt(m) h`. R4 does not reproduce family (B). R4 `prop:lim:local` adds a small-noise robustness result for family (A): at the specified `sigma <= 1/1000`, every draw reaches level 1 and the bag-local allowance deletes every optimizer projection. Attribute the base obstruction to the companion and the robust finite-noise extension to R4; do not describe the entire star obstruction as new. |
| `thm:tu-states`, `constraints.tex:264–298`; `thm:tu-approx`, `:300–351`; `thm:tu-exact`, `:353–426` | R4 `sections/06-constraints.tex:789–806` | The companion's TU results are deterministic. `thm:tu-states` assumes set growth and finite optimal coordinate projections for level-independent node counts. `thm:tu-approx` certifies rational approximation without growth, but then table counts depend on accuracy; its accuracy-independent table/work bound also uses growth and a bound on each optimal projection's cardinality. `thm:tu-exact` terminates for rational quadratic objectives without uniqueness or growth; its explicit level bound needs set growth, and its table-operation bound additionally needs finite optimal projection cardinalities. These results do not give a finite-law expected count, finite-noise closure/tail estimates, or a same-draw fallback for general TU systems. The R4 exclusion concerns the general TU feasible-set route of Section 6, not the separate TU recourse results elsewhere in the paper. The frozen opening “General totally unimodular constraints are not covered” should be narrowed to the smoothed guarantees and paired with the deterministic companion citation. |

For the core-search count in R4, the finite-law factors are
`Q_ex=[3+(1+k/2)L/(2 sigma)]^k` and
`Q_ap=[3+(1+k)L/(2 sigma)]^k`, for exact and certified conditional values,
respectively. Under the independent core law, conditional on the residual
noise, these bounds do not invoke point growth. The level horizon and mesh
must satisfy `M >= 2^J`.

## Closure certificates and the smoothed layer

The companion already has deterministic exact boundary-output machinery.
Its `thm:boundary` (`sections/appendix-boundary.tex:98–148`) uses sign tests,
strict complementarity at active continuous bounds, and a rational face box
on which the objective is strongly convex; its runtime bound depends on the
bit length of a reciprocal complementarity margin. Its polynomial section
also identifies this face-box output and margin condition
(`sections/exact.tex:497–508`). R4 itself gives the precise qualification in
`sections/01-introduction.tex:513–521`: its polynomial closure reuses this
kind of enclosure and adds finite-noise margin tails and an exact same-draw
fallback. Thus the closure/enclosure concept and exact implicit output are
not wholly new. The smoothed layer audited here is the finite-law expected
count without supplied growth, probability bounds for closure events under
the base-selected law, and the expected-work composition with an exact
fallback on the same draw. These are comparisons only to this decomposition-
aware companion, not a claim of absolute priority.

## Attribution status and wording repairs for frozen R4

R4 already credits the corrected-grid/min-marginal pipeline and conditional
bag filter, scopes the uniform-grid and rETH lower bounds, and distinguishes
the strong-convex face enclosure from its finite-noise extension. The
following narrow additions would make the remaining overlaps explicit:

- Near the value-function statement, name `lem:valuefunction(a)` as the
  deterministic antecedent to `lem:rec:value(b)`.
- In the companion comparison, state that CORE `thm:cr-search` supplies the
  deterministic retention, value interval, and witness facts underlying
  `prop:rec:search(a)–(c)`, while `prop:cr-growth` is a separate
  growth-conditioned query bound. Identify the expected finite-law count as
  the added smoothed statement. Do not imply that R4 repeats CORE's
  checkable global lower-bound item (d).
- Say that `ex:rec:star` specializes family (A) of `prop:star`, and that
  `prop:lim:local` is its every-draw small-noise extension. Do not imply that
  R4 includes companion family (B)'s bounded-growth obstruction.
- Scope the TU exclusion as an exclusion from this paper's smoothed
  guarantees and cite the companion's deterministic TU results. Retain the
  distinct assumptions: approximation certificates are available without
  growth but have accuracy-dependent counts; the exact quadratic algorithm
  terminates without growth/uniqueness; growth and finite projection counts
  are needed for the displayed level/work bounds.

The one-dimensional product-grid and rETH comparisons in R4 are already
properly qualified; no broader lower-bound wording is needed.

## Moving successor draft observed separately

The live working tree changed while this read-only audit was in progress; it
is not the frozen R4 target. At the last read, `paper-smoothed-global/sections/01-introduction.tex`
had SHA-256 `3f847bd1b914bb75416ea1dc2719c37bf980f8913aa510e737289b5eeb6eb7f6`.
It now explicitly names the value-function, CORE, filter, and star overlaps,
and distinguishes their deterministic parts from the finite-law counts and
same-draw fallback. It also says polynomial closure reuses the companion's
strongly convex face enclosure. `paper-smoothed-global/sections/06-constraints.tex`
had SHA-256 `7b8f691e5f085e4b1792d333db3f3519cbf487ce34f3349f34ae12d28c6c4285`;
its opening now says general TU constraints are outside this paper's
*smoothed* guarantees and describes the companion's deterministic coupling,
approximation, and exact results. One precision point remains for that prose:
accuracy-independent TU work counts require finite optimal coordinate
projections as well as growth; the exact algorithm terminates without either
premise, but termination alone is not a polynomial work bound. These moving
hashes identify observations at audit time and are not manifest-backed
submission identities.

## Follow-up (2026-10-06): positive-definite star and TU rounding

This follow-up records two additional source comparisons and corrects one
statement in the initial audit (preserved separately as
`companion-overlap-addendum-luna-initial.md`, SHA-256
`d0f31e1edb7351beed62103050aaddc6a76ee16b3b3cb2750ef62dae1fce5e31`). The
initial audit said that R4 does not reproduce family (B) of `prop:star`.
That was too broad: R4 does not state the general-`h` family as a theorem,
but its positive-definite construction and proof are the exact `h=1/4`
specialization of family (B). This follow-up supersedes that non-reproduction
claim; the remaining frozen-R4 observations above are unchanged.

### Positive-definite star variant

The variant in frozen R4 `appendices/E-recourse.tex:840–856` is exactly
companion `prop:star` family (B), specialized to `h=1/4`. The R4 objective
`(v-1/2)^2 + sum_i (z_i-1/8-(v-1/2)/d)^2` is family (B) after setting
`x=v`, `y_i=z_i`, and `h=1/4`. Its `m=d^2`, `d>=8` conditions are exactly
the companion's `m=d^2`, `d>=2/h`; both use the level-2 mesh `h=1/4`.

The spectral and growth statements also coincide: the Hessian eigenvalues
are `2` on the leaf-difference subspace and `3 +/- sqrt(5)` on the center
and normalized leaf-sum subspace; `L=4`, `g=(3-sqrt(5))/2`, and
`kappa=2(3+sqrt(5))<11`. The companion's excess corner min-marginal over
the grid incumbent is
`d h(1/2-h)+2h^2-1/2`; at `h=1/4` this is exactly R4's
`q_C-U=d/16-3/8`. The companion proof also gives
`V^G(t)=2t^2-dh|t|+d^2h^2/4`; subtracting `V(t)=t^2` at adjacent center
nodes `t=0,h` gives the R4 error variation `-(d-1)h^2`. Thus the
positive-definite obstruction, including its bounded-growth scaling, is
already present in companion `prop:star(B)` and its proof
(`appendix-recourse-convex.tex:161–176,209–236`). R4 specializes the family
and spells out one deleted bag cell; it is not a new positive-definite star
example. The frozen R4 appendix hash is
`e3bba43cbcfa9cfd373661b350711c3f890ebb73a9994dc6dfc13fae49676e1f`;
the companion appendix hash is recorded in the source table above.

### Aligned TU rounding and pruning

Frozen R4 `sections/06-constraints.tex:789–806` uses the deterministic layer
of companion `lem:tu-round`, `lem:tu-allow`, and `prop:tu-sound`
(`paper-decomposition-aware/sections/constraints.tex:113–180,235–253`). In
both proofs, scaling an aligned dyadic cell gives a TU system with integral
right-hand side, so feasible points are convex combinations of feasible grid
corners. Rounding preserves the point in expectation and bounds the squared
displacement by `n_c h^2/4`; the companion's Hessian bound on the permitted
displacement subspace (a full-space bound when that subspace is all of
`R^{n_c}`) then gives the allowance `n_c \bar L h^2/8`. The companion uses
this allowance in certified filtering
and verifies sound pruning over the current feasible domain by recomputing
grid values and min-marginals. R4's statement is a specialization to
`[0,1]^n`, `Ax<=b`, and cells with every constraint assigned inside a bag,
where its sparse pruning rule is sound.

The companion lemma is more general: it permits mixed discrete coordinates,
aligned non-cube coordinate domains, and rounding constrained to an
equality-preserving subspace. The R4 section cites TU integrality through
Hoffman–Kruskal but, in the frozen snapshot, does not directly credit this
companion deterministic rounding/filtering layer. Its smoothed gap is the
retained-cell count and closure/tail control under finite noise, not the
aligned feasible-rounding argument or the `n_c \bar L h^2/8` correction.
Frozen R4 Section 6 has SHA-256
`9467eb72e20f355b3afb70d844bfedcf0a7fe52ba8f53d2483327162ad9db898`;
the companion constraints source hash is recorded above.

At a later read, the live successor `paper-smoothed-global/sections/06-constraints.tex`
had SHA-256 `4673754153b8e86cb107464d1aa3f69fc26cf6ac22530816372a5a4579872efc`.
Its opening directly credits the companion's deterministic TU algorithm and
separates that result from this paper's smoothed guarantee. The aligned
rounding paragraph still cites the classical TU-vertex result without
naming `lem:tu-round`, `lem:tu-allow`, or `prop:tu-sound`; adding that
specific credit would make this second overlap explicit.
