# Opus editorial review r1: exposition, coherence and submission quality

Reviewer: Opus, independent editorial reviewer (not an author).
Date: 2026-10-06.
Manuscript: "Smoothed exact global optimization beyond convexity".
Snapshot: `evidence/snapshots/complete-editorial-draft-r1/` (immutable).

Locators are `file:line` in this snapshot. Sections are abbreviated
`00`–`10` and appendices `A`–`G`; for example, `07:511` is line 511 of
`sections/07-recourse.tex`.

## Scope and method

This report covers:

- exposition and organization;
- whether claims match the proved guarantees;
- the relation to prior work and to the three companion manuscripts.

The Opus mathematics reviewer and the Sol specialists check the proofs. I
raise a mathematical point only when it changes what a sentence claims. The
bibliography is pending by design, and I do not count its absence as a
defect.

The new findings A1–A5, including the companion overlap in A2, were sent to
the root thread when found, in two messages. This report supersedes those
messages.

## Verdict

**Not ready for submission.** The draft needs a major revision of its front
matter, its account of the companion manuscripts, and the organization of
Sections 2, 4 and 8. The accepted mathematical repairs in Part C are also
still needed. No finding in my scope defeats the subject. The scientific
contribution is coherent, and the prose is already close to journal
standard.

The decisive problems are:

1. **Companions.** The relation to the two closest companion manuscripts is
   materially incomplete (A1, A2). Several results that the text presents as
   new, or does not attribute, appear in those manuscripts. A positive
   companion result contradicts an unqualified boundary statement.
2. **Fixed-parameter claims.** The abstract and Table 1 call the low-rank and
   core bounds fixed-parameter in `k` without the qualifier, stated in
   Section 2, that the curvature-to-noise ratio is part of the parameter
   (A3).
3. **Claimed uses.** The Discussion claims uses that the guarantees do not
   cover (A4).
4. **Attribution.** The critical-region tool of the quadratic route is used
   without attribution, yet listed as a contribution (A5).
5. **Organization.** Section 8 mixes three routes (A8). Section 2 contains a
   proposition whose proof depends on Sections 3–8 and uses undefined symbols
   (A9).

What already works, and should be preserved:

- **Contracts.** Section 2 states the input, law, output and evaluation
  contracts clearly. The distinction between a descriptor and its global proof
  record, the `q`-bit evaluation contract, and the regret proposition are used
  consistently, apart from the known exceptions in Part C.
- **Theorem statements.** Each main theorem names its noise model, law,
  sampling precision, outputs on ordinary and fallback draws, and the
  numerical ratio that enters its bound.
- **Scope subsections.** These are candid: `06:710–741`, `07:652–671`,
  `08:580–597`.
- **Examples.** The examples are well chosen, and each explains a
  restriction: `ex:model:tie`, `ex:count:atom`, `ex:qp:atom`,
  `ex:qp:corner-labels`, `ex:rec:feasibility`, `ex:con:premature`,
  `ex:lim:coupled`.
- **Boundaries.** Section 9 labels the kind of every boundary result
  (`09:18–56`) and says which instances other methods solve easily.
- **Prose.** The prose is plain. A count over all sources found almost no
  intensifiers ("essential" six times, in technical senses) and no
  promotional adjectives.
- **Proof presentation.** The main-text proofs of Section 5 are short and show
  the mechanism. Appendix B proves three theorems with one argument
  (`B:599–713`).

## Part A. New findings, in order of priority

### A1. Major: exact-arithmetic companion, unattributed overlap and a missing degree distinction

Locators: `09:758–762`, `G:179–182`, `01:104–111`, `01:336–341`,
`01:401–406`, `07:3–7`, `07:511–521`, `07:665–669`, `09:614–635`,
`10:130–136`.

Evidence comes from local repository files, not literature research. The
file is `paper-exact-arithmetic/sections/10-recourse.tex`:

- lines 4–8: the opening paragraph;
- lines 26–33: full points need more structure, and core noise alone does
  not help at degree four;
- `thm:recourse-core` (line 138): values and one selected core under one
  finite law, with expected work `k^{O(k)}(1+kappa/sigma)^k P_D(L)`;
- `thm:recourse-convexified` (line 272): full points under a supplied
  convexifier;
- `thm:recourse-cubic` (lines 398–416): the full selected optimizer for
  residual-convex cubics on product boxes under core noise. It assumes no
  joint convexifier, no lower bound on residual curvature, and no uniqueness
  of residual optimizers.
- `rem:recourse-quartic` (lines 572–588): add one noisy core coordinate to
  the Square Root Sum (SRS)/PosSLP quartic. Then core noise cannot make full
  points of residual-convex quartics tractable unless both problems have Las
  Vegas algorithms.

Problems:

1. **Part (c) is presented as new.** `09:758–762` says that parts (a), (b)
   and the deterministic consequence also appear in the companion, "and part
   (c) is the consequence for core-only noise". This reads as a claim that
   (c) is new. The companion's remark "Degree four" states the same
   consequence with the same construction.
2. **The modulus statement lacks a degree qualifier.** Several sentences say
   that core-only noise needs a uniform residual modulus for point output:
   `01:104–111` ("residual points need more"), `07:665–669`, `09:614–635`,
   and the open question at `10:130–136`.
   - The companion's cubic theorem gives full points under core-only noise
     with residual convexity alone.
   - The paper's own obstructions are quartic: `thm:lim:posslp`, and
     `ex:rec:fiber`, whose residual term `(z_1 - v z_2)^2` has degree four.
3. **The companion paragraph is incomplete.** `01:401–406` lists "value and
   selected-core oracles ... finite-law replacement and section-counting
   arguments ... and the point-output reductions". It omits:
   - the two full-point theorems;
   - the degree-four remark;
   - that the companion's core count has the same form as
     `prop:rec:search`.
4. **Text overlap.** `07:3–7` nearly repeats the companion's opening
   sentences at `10-recourse.tex:4–8`: "Many structured problems ... a few
   complicating ... Two-stage models ... decomposition methods that branch
   only on ...". A journal similarity check will flag this.
5. **Unverified "new".** `07:511` says the core-only proof "has three new
   ingredients". I did not check whether the selector, Lipschitz and
   growth-lift lemma (`lem:app:rec:lift`) has a counterpart in the
   companion's appendix. Until the authors or Luna check, write "three
   ingredients".

Repair:

- **Attribution of (c).** In `09:758–762` and `G:179–182`, use the wording
  of D4.
- **Degree distinction.** State it once, in Section 9.4. Point to it from the
  introduction, Section 7.6 and the Discussion. Suggested text:
  > For residual-convex cubics on product boxes, core-only noise suffices
  > for full selected optimizers [companion-exact-arithmetic]. At degree four
  > it does not, unless Square Root Sum and PosSLP have Las Vegas algorithms
  > (Theorem 9.x(c)). Theorem 7.x covers every fixed degree under a certified
  > uniform residual modulus and returns an implicit patch.
- **Introduction.** At `01:104–111`, change "Under noise on the core alone,
  residual points need more" to "Under noise on the core alone and residual
  degree at least four, residual points need more".
- **Open question.** Rewrite `10:130–136` so that it starts from the known
  cubic case.
- **Text overlap.** Rewrite `07:3–7` in new words.
- **Companion paragraph.** Use the text of D2.

### A2. Major: the deterministic layer of Sections 5, 7 and 9 is in the decomposition-aware companion, unattributed

Locators: `01:407–410`, `05:533–565`, `05:908–929`, `06:710–729`,
`07:102–116`, `07:145–171`, `07:173–224`, `09:58–218`, `09:288–360`,
`10:110–116`.

Evidence comes from local files in `paper-decomposition-aware/sections/`.
For the abstract-level claims I relied on the abstract and did not check the
proofs.

- **`abstract.tex`.**
  - Corrected product-grid dynamic programming with the `L_i w^2/8`
    correction, min-marginal filtering, and stage-grid certificates.
  - Under growth, graded grids keep `O(sqrt(kappa_bar) log(n+2))` nodes per
    coordinate. This gives `f(p,kappa_bar)(I+q+1)^5` for approximation and
    `f_1(p,kappa) I^{O(1)}` for an exact minimizer.
  - Extensions to exact partial minimization and to totally unimodular (TU)
    coupling constraints.
- **`growth-sharp.tex:1–30` (`prop:sharp`).** Filtering on uniform grids
  keeps order `sqrt(n kappa)` nodes per coordinate; graded grids reduce this.
- **`limits.tex:340–365` (`prop:lbproduct`).** Under rETH the exponent of
  `kappa` cannot be `o(p)`. The proved bound has exponent `p/2+O(1)`.
- **`recourse-valuefn.tex` (`lem:valuefunction`).** The value function
  inherits coordinate upper curvature when the recourse feasible set does not
  depend on the retained values. The companion calls this "the only
  structural requirement".
- **`recourse-local.tex:36–75` (`thm:cr-filter`).** A bag-local correction is
  valid with exact or certified conditional values. Grid min-marginals do not
  suffice.
- **`appendix-recourse-convex.tex:144` (`prop:star`).** "Constant corrections
  must grow with dimension": the star example.
- **`recourse-cuts.tex:173–192` (`thm:cr-search`, `prop:cr-growth`).** A
  deterministic core search, CORE, with retention, value-interval and witness
  properties, and a query count under core growth.
- **`constraints.tex:266, 302, 401`.** Node counts, certified approximation
  and exact output with TU coupling constraints.

Problems:

1. **The description is too narrow.** `01:407–410` describes this companion
   as containing "curvature-corrected coordinate grids, min-marginal
   filtering, and a star example related to ex:rec:star". It omits:
   - the conditional-recourse layer: the value-function lemma, CORE, and the
     certified-value bag filter;
   - the growth-conditioned fixed-parameter bounds.

   Neither Section 5.9 (`05:908–929`) nor Section 7 cites the companion.
2. **Several statements are re-proofs.** As deterministic statements, the
   following re-prove companion results:
   - `lem:rec:value(b)`;
   - the retention part of `prop:rec:search(a)–(c)`;
   - `prop:lim:conditional(a),(b)`, the B10 bridge;
   - `prop:lim:local` and `ex:rec:star`.

   What is new here is the smoothed layer:
   - counts under a finite law without a growth premise (the expectation part
     of `prop:rec:search`, and `prop:lim:conditional(c)`);
   - the closure certificates;
   - the same-draw fallback;
   - the every-draw form of the star failure, with level-0 nonclosure.

   The front author's report (§5, item 4) calls B10 "new as a manuscript
   statement". The submission text must not imply that.
3. **An obvious question is unanswered.** An expert who knows the companion
   will ask why the sparse route does not inherit the companion's
   `f(p,kappa)` form. The answer is short and belongs next to
   `thm:lim:width` and in `sec:sp:width`:
   - Under linear noise, `kappa = L/g_*` has a tail of order `LS/(sigma t)`
     (`thm:count:growth-tail`).
   - Integrating `kappa^{p/2+O(1)}` against that tail, capped at the
     fallback factor `B`, gives a bound polynomial in `log B`, and hence in
     `I`, only when the exponent is at most one. This is the phenomenon of
     `rem:qp:moments`.
   - rETH rules out an exponent `o(p)`.

   Hence Section 5 uses closure with a same-draw fallback and pays
   `n^{Theta(p)}`.
4. **The barrier is overstated.** The open question at `10:110–116` says that
   `thm:lim:width` and `prop:lim:local` "show that this needs certified
   conditional values for the variables outside a bag". They show two things
   only:
   - the global-error retention rule cannot give a bound that is
     fixed-parameter in the width;
   - a bag-local allowance is unsound with grid min-marginals.

   They do not show that every method needs certified conditional values.
   `05:562–565` ("A dimension-free count would require exact or certified
   conditional values") overstates in the same way.
5. **TU scope.** `06:710–729` says general TU constraints are not covered.
   Add that the companion treats TU coupling deterministically under growth,
   and that what is missing here is a smoothed count without a growth
   premise.

Repair:

- Rewrite the companion paragraph as in D2.
- Add one attribution sentence at each of the following places:
  - `05:908–929`;
  - `07:102–116`, after `lem:rec:value`;
  - `07:196–224`;
  - `09:288–295`, before `prop:lim:conditional`;
  - `07:145–171` and `09:220–238`;
  - `06:710–729`.
- Replace the width open question with D3.

### A3. Major: "fixed-parameter" without the numerical-ratio qualifier

Locators: `00:9–11`, `00:16–18`, `01:148`, `01:222–229`, `02:401–403`.

**The bounds are XP when the ratio grows with the input.**

- The core bound is `8^k [3+(1+k)L/(2 sigma)]^k poly(I)`.
- The Gaussian-like low-rank bound is
  `f(n_z) C_0^k (1 + [9+5k+2(1+2k) nu diam(P)/sigma]^k) (I+1)^{C_1}`
  (`04:508–519`).

Both are fixed-parameter only if the ratio counts as part of the parameter,
as `02:401–403` and `01:275–278` say. If `L/sigma = poly(I)`, both bounds
are `I^{O(k)}`: polynomial for each fixed `k`, but not fixed-parameter in
`k`.

**The abstract and Table 1 drop the qualifier.** The abstract says
"fixed-parameter tractable in the negative inertia and the integer
dimension" and "fixed-parameter tractable in the core size". Table 1 says
"fixed-parameter" (`01:148`). A reader takes these as `f(k) poly(I)`
bounds.

**The difference from the sparse route gets lost.** For bounded ratios, the
core and low-rank bounds are fixed-parameter, while the sparse bound is still
`n^{Theta(p)}`, because `n` enters the rounding allowance. The mechanism
paragraph (`01:222–229`) says only that the confining interval has length
"proportional to the curvature bound times the mesh". It omits the factor
that counts the coordinates in the rounding allowance: all `n` in the sparse
route, but only the searched coordinates in the core and low-rank routes.
That factor is the whole difference between the routes.

**`02:401–403` lists all low-negative-inertia results as fixed-parameter.**
`thm:qp:uniform` is not.

Repair:

- **Abstract.** Use D1.
- **Mechanism paragraph** (`01:222–229`). After "times the mesh", add: "and
  the number of coordinates whose rounding error the allowance absorbs. These
  are all `n` coordinates in the sparse route but only the `k` searched
  coordinates in the core and low-rank routes."
- **Section 2.** At `02:401–403`, write "the aligned and Gaussian-like
  low-negative-inertia results".
- **Table 1** (`01:148`). Write "fixed-parameter in `k` and the ratio".

### A4. Major: uses not supported by the guarantees

Locators: `10:9–14`, `10:39–49`, `07:3–7`.

1. **Exogenous noise.** `10:9–14` says: "For problems whose linear costs are
   themselves uncertain or estimated, the sampled instance can be the problem
   of interest."
   - The algorithm computes the law (`def:model:algorithm`, `02:259–275`).
     Section 2 (`02:147–150`) says that no other finite law is covered.
   - So exogenous noise is not covered, even at the same scale. Replace the
     paragraph with D5.
2. **Two-stage models.** `10:39–41` and `07:3–7` name "two-stage problems".
   - In standard two-stage models, first-stage decisions enter the
     second-stage constraints, as in `W y <= h - T x`. That is the
     core-dependent feasibility that `ex:rec:feasibility` excludes.
   - Write "two-stage problems whose first-stage decisions enter only the
     second-stage costs, for example prices or tariffs".
   - The same check applies to "design problems with a few shape ...
     parameters" (`07:5–6`). A shape parameter usually changes feasibility.
3. **Application classes.** `10:42–49` lists further classes without a cited
   model. Either give one cited model per class together with its
   restriction, or reduce the paragraph to one sentence. The restrictions
   are:
   - whole-block bags for simplices;
   - bounded dependency depth or global brackets for graph charts;
   - box invariance and affine states for actuator recurrences.

### A5. Moderate to major: critical regions of parametric convex QP used without attribution, yet listed as a contribution

Locators: `01:243–244`, `01:349–364`, `01:384–386`, `04:330–374`,
`B:284–337`.

`lem:qp:pieces` is the critical-region decomposition of multiparametric
convex quadratic programming: on a polyhedral region of the parameter, a
fixed active set gives an affine optimal solution.

- Neither frozen snapshot cites that literature. I checked
  `complete-proof-draft-r1` and `complete-editorial-draft-r1`;
  `04-quadratic.tex` is identical in both.
- The quadratic author report (§4, item 7) says that Bemporad et al., Tøndel
  et al., Patrinos–Sarimveis and Ding are cited. Their keys appear in
  `evidence/current-citation-requests.txt`, but not in the TeX.
- Meanwhile `01:384–386` lists "closure by regions of a parametric convex
  program" as a contribution.

Repair:

- After `lem:qp:pieces`, add:
  > Such regions are the critical regions of multiparametric convex
  > quadratic programming [Bemporad et al.; Tøndel et al.;
  > Patrinos–Sarimveis]. What is new here is their use as exact closure
  > certificates in the auxiliary search, their extraction from one exact
  > solve, and the fixed-hyperplane exceptional set.

  Luna should confirm the sources and locators.
- Add multiparametric programming to the classical ingredients at
  `01:349–364`.

### A6. Moderate: the sparse-indicator companion is described too vaguely

Locator: `01:411–412`.

The source is the companion's abstract,
`paper-sparse-indicator-quadratics/main.tex:30–58`.

- **Model.** It perturbs only the indicator penalties, that is, the linear
  costs of the binary indicators, by an independent uniform draw from a grid
  in `[-sigma, sigma]`.
- **Exactness and cost.** It solves every draw exactly and computes exact
  separator messages at fixed treewidth. The expected bit complexity is
  polynomial in the input length and the numerical parameters.
- **Lower bound.** Unless NP ⊆ ZPP, the polynomial dependence on the
  coefficient bound cannot be replaced by dependence on encoding length.

This is close to the sparse route here (grid law, every-draw exactness,
bounds polynomial for each fixed width) and to `thm:lim:constraints`
(NP ⊆ ZPP). "Under a different perturbation model" understates the
overlap.

Repair: state the companion's model, its problem class, its output and its
lower bound, and say that neither paper contains the other. The problem class
is positive definite quadratics with indicator constraints, which lie outside
the mixed-box model of Section 5. The output is exact messages. D2 includes
this.

### A7. Moderate: strong-noise route, misdescribed weight and an impractical polynomial regime

Locators: `00:20–21`, `01:113–121`, `08:463–470`, `08:486–491`,
`08:508–519`.

The weight `a_i` is (`08:463–470`):

- the number of labels for an integer coordinate;
- 3 for a continuous coordinate of a quadratic;
- otherwise the solver constant `c_d`, for which `lem:int:budget` proves
  `c_d = 2^{10000 D}`.

The sufficient regime at `08:489` is `sigma >= 8 Delta_+ max_i (a_i R_i)`.

- For non-quadratic objectives, the noise must therefore exceed the
  derivative variation by a factor of order `2^{10000 D}`, so the polynomial
  case is a structural statement only.
- `01:115–116` says "weighted by the size of the coordinate's domain". That
  is wrong for continuous coordinates.
- The section text (`08:510–513`) states the `c_d` scaling honestly; the
  introduction and abstract do not.

Repair, at `01:113–121`:

> ... if the noise scale exceeds the variation of every coordinate derivative
> by a factor proportional to the degree of the interaction graph and to the
> cost of solving that coordinate exactly ... For quadratic objectives this
> regime is meaningful; for higher degree the result is structural.

The cost of solving a coordinate exactly is the number of labels of an
integer coordinate, 3 for a continuous coordinate of a quadratic, and
otherwise the solver constant `c_d`, which our proof makes astronomically
large.

### A8. Moderate: one route per section

Locators: `08:1–15`, `08:449–519`, `08:521–578`, `01:51–71`,
`01:156–158`, `01:418–426`.

Section 8 contains three routes:

- small-core integer recourse (8.1–8.4);
- strong noise (8.5);
- a few-negative-directions result (8.6, `thm:int:lowrank`).

The introduction (`01:69–71`) and Table 1 (`01:156–158`) place the lattice
theorem under "Few negative directions". Readers then find it in a section
titled "Integer recourse, flows, and random components".

The lattice theorem belongs with Section 4:

- Its model is that of `def:qp:sep`, restricted to integer boxes with
  polynomial unaries: `F = sum_j g_j - (alpha/2)||Tx||^2`, with aligned
  noise.
- Its proof (`F:937–982`) uses only `thm:count:cells`, `def:count:mesh` and
  `cor:count:levels`, nothing from Sections 7 or 8.
- The sketch at `08:561–562` says it uses "the core search of
  sec:rec:value", which does not match the proof (`F:961`).

Repair:

- **Lattice theorem.** Move `thm:int:lowrank` to Section 4 as 4.7, after
  `thm:qp:sep-gauss`, with its proof in Appendix B. Fix the sketch to cite
  `thm:count:cells`.
- **Strong noise.** Give the strong-noise theorem its own short section
  before the boundaries, framed as the contrasting regime.
- **Exact box solver.** Keep `thm:int:solver` at the start of Section 8.
  Optionally, move it to Section 3 as a second exact tool next to
  `thm:count:fallback`, so that both exact tools sit together.
- **Route count.** Use one count everywhere: "three structural routes and a
  strong-noise regime", as in `evidence/architecture.md` §1. The abstract
  (`00:8`) and introduction (`01:47`) say four; `07:9` and `09:843–845` say
  three plus strong noise.
- **Organization paragraph.** Update `01:418–426`.

### A9. Moderate: `prop:model:uniform` depends on later sections and uses undefined symbols

Locators: `02:154–158`, `02:169–242`.

- **Forward dependence.** The proposition and its proof cite
  `lem:count:transfer`, `thm:count:fallback`, `lem:count:finite-tails`,
  `app:qp:main`, `thm:int:lowrank`, `thm:int:flow-boundary` and
  `thm:int:tu`.
- **Undefined symbols.** The text uses the following before they are
  defined:
  - the strong-noise quantities `q_i`, `a_i`, `R_i` and `Delta_+`
    (`02:190–192`, `02:232–235`);
  - the lattice cap `J` and the denominator `D_0` (`02:180–181`,
    `02:215–218`).

A reader cannot check the proposition at that point.

Repair: keep the sentence at `02:154–158` as a forward pointer. Move the
proposition and its proof to one of:

- the end of the new strong-noise section;
- a short subsection before the Discussion;
- Appendix A.

The integration contract calls the result an elementary consequence, so
placing it in an appendix is appropriate.

### A10. Moderate: treewidth-two qualifier attached to PosSLP

Locator: `01:336–341`.

The sentence "...would give Las Vegas algorithms for Square Root Sum and
PosSLP, even when the residual problems have treewidth two and bounded
coefficients" can be read as covering PosSLP. Integration decision 11 says
not to assert a treewidth bound for the PosSLP construction, and
`09:762–764` is careful about this. Write instead: "...for Square Root Sum,
already on residual problems of treewidth two with bounded coefficients, and
for PosSLP".

### A11. Moderate: the Discussion omits the main applicability restriction

Locators: `10:60–106`, `10:108–149`.

The limitation that most affects applications is that residual feasibility
must not depend on the core (`ex:rec:feasibility`, `07:87–88`). In the TU
and flow theorems, supplies and right-hand sides must not depend on it either
(`08:139–140`). The list of supplied premises at `10:79–87` omits this.

Also add to the limitations:

- the self-randomization point of A4;
- the `c_d` constant of the strong-noise regime (A7).

Among the open questions, core-dependent feasibility is a natural candidate,
given `ex:rec:feasibility` and `ex:lim:coupled`.

### A12. Moderate: the same knowledge proved twice

1. **Quadratic face enumeration.** `lem:sp:faces` (`C:220–255`) reproves
   `lem:qp:face(c),(d)` (`04:295–316`, `B:117–145`).
   - Both use the smallest-face argument. For a mixed box, (c) and (d)
     together already give the enumeration over `N_Z 3^{n_c}` faces.
   - The two lemmas state different enumeration rules for the same fallback.
     `lem:qp:face(b)` says "Multiplier signs and definiteness tests are
     unnecessary". `lem:sp:faces` and tool T10 (`E:105–109`) keep only faces
     whose free Hessian block is positive definite.
   - Keep `lem:qp:face`, state the mixed-box count as a corollary, and cite
     it from `05:897`, `07:341`, `E:105–109` and the strong-field proof.
2. **Restated tools.** `E:29–110` restates ten earlier results, T1–T10, in
   new notation:
   - `N_act` for `K_act` (`E:60` vs `03:434`);
   - Renegar's theorem with `(s, d_0)`, where `A:328–342` uses `(m, d)`;
   - the GLS lemma in a specialized form.

   Replace them with a short cross-reference list. State the only new
   external tool, the Basu–Lerario tube bound (T7), once, next to Renegar's
   theorem in an "External tools" subsection of Appendix A. Cite both from
   Appendices E and F. This removes about 1.5 pages and a source of notation
   drift.

### A13. Minor to moderate: notation collisions

Several symbols have more than one meaning, often in adjacent text.

| Symbol | Meanings and locators |
| --- | --- |
| name of `sigma` | "noise scale" (`01`, `02:135`); "noise width" (`03:11`, `04:37`); "noise half-width" (`05:49`, `06:146`, `07:82`) |
| `b` | linear coefficients (`02:20`, `04:35`, `05:874`); `log2 M` (`02:161`); Gaussian accuracy (`02:144`, `03:271`); added coefficient bit length (`03:505`); simplex block (`06:496`, Appendix D); right-hand side (`06:713`, `08:126`, `08:418`) |
| `k` | negative inertia or factor rows (Section 4); core size (Section 7); search dimension (`03:36`); parent bound of graph charts (`06:127–130`, table `06:43–46`); time index (`06:384`) |
| `C_0` | absolute constant (`04:509`, `05:148`, `06:33`; "may change between occurrences" at `D:3–5`); data-dependent integer (`04:353–355`, `B:619`); a cell (`05:321`) |
| `Z` | number of integer points (`04:224`, `04:308`, `B:610`); `max{1, nu/g}` in the adjacent `thm:qp:conditioned` (`04:199`, `04:262`); tangent basis (`06:585`) |
| `H` | input length of the solver (`08:68`); Hessian bound (`08:338`); `K_2/mu` (`07:576`, `E:474`) |
| `K` | face of the core cube (`07:523`); mixed-derivative bound (`08:338`); several count constants |
| `rho` | allocation parameter (`03:468`, `D:581`); integer budget (`D:367`) |
| `sigma_s` | slack of a constraint (`D:603–605`), next to the noise scale `sigma` |
| `I_k` | state intervals (`06:389`), next to the input length `I` |
| `w_i` | coordinate width (`02:40`); width of the auxiliary box (`04:538`, `04:558`, `08:535`) |

Repair:

- Use "noise scale" for `sigma` everywhere.
- Give each concept one symbol.
- Add a notation table at the end of Section 2. `evidence/notation.md`
  already fixes most of the choices.

### A14. Minor items

1. `00:21`: change "The common mechanism" to "The main mechanism". The
   lattice and strong-noise results do not use the fallback (`01:264–269`).
2. `00:18`: change "strongly convex continuous recourse" to "continuous
   recourse with a certified uniform strong-convexity modulus".
3. `01:147–148`, `01:155`, `01:157`: Table 1 uses `H_al` and `H_rat`
   without defining them, and "as above" is ambiguous. Define the symbols in
   the caption or write out the bracket.
4. `01:204–205`: the sentence about sampling bits does not belong in the
   outputs paragraph, and `01:291–294` repeats it. Delete it here.
5. `02:270–271`: "condition on any event of the draw" is ambiguous, because
   every algorithm branches on the draw. Write "does not reject the draw or
   draw again".
6. `02:509`: "the smallest instance of this phenomenon" is an unsupported
   superlative. Write "a simple instance".
7. `03:18`: the text says "The section has four parts", but there are six
   subsections.
8. `03:255`: "In the low-rank quadratic results" narrows too far. The
   closure-and-fallback design applies to the closure-based results of
   Sections 4–8, but not to the lattice and component results. This item
   relates to C3.
9. `03:220–239`: `cor:count:approx` is used nowhere else. Its "logarithmic
   in `1/epsilon`" concerns the sampled objective, and it sits uneasily next
   to the original-objective approximation, which is polynomial in
   `1/epsilon`. Cut it, or add one sentence on its role.
10. `08:331–339`: nine symbols come before the idea of `thm:int:face`, which
    arrives only at `08:363–368`. Put the idea first.
11. `06:480–486`: `ex:con:actuator` only checks the definition on one
    transition. Fold it into one sentence after `def:con:actuator`.
12. `01:366–379`: the prior-work subsection does not mention deterministic
    fixed-rank algorithms, although `08:570–578` discusses them (zonotope
    vertex enumeration on `{0,1}^n`). Ask Luna for the nearest sources on
    exact and approximate algorithms for fixed negative inertia, including
    mixed-integer variants, and compare in one sentence.
13. `09:362–423`: `thm:lim:ambient` covers `alpha` in `{1, m}`, but the text
    never says what `alpha = m` adds. Explain it or drop it.

## Part B. Consolidation plan

Every theorem and proof is kept. The estimated saving is 6–8 pages, and the
reading order improves.

| Move | From | To | Effect |
| --- | --- | --- | --- |
| Lattice theorem | `08:521–578`, `F:937–982` | Section 4.7 and Appendix B | route in one place |
| Strong noise | `08:449–519`, `F:891–935` | own short section before Boundaries | Section 8 fits its title |
| `prop:model:uniform` | `02:169–242` | end of the strong-noise section, or Appendix A; pointer kept at `02:154–158` | no forward dependence |
| Ambient barrier | `04:630–651` and `09:362–440` | one statement (`thm:lim:ambient`); two sentences remain in Section 4 | −0.5 p |
| Star example | `07:145–171` and `09:220–286` | `prop:lim:local` in Section 9; Section 7 keeps a pointer and the sentence on exact conditional values; the positive definite variant stays in E | −0.7 p |
| Rank-separation discussion | `07:462–471`, `07:503–509`, `09:819–837` | keep Section 7; cut `09:819–837` to two sentences | −0.5 p |
| Mechanism restated | `05:12–24`, `07:16–33` | one sentence each, naming the route-specific instantiation | −0.5 p |
| Repeated caveats ("sampled objective only", Gaussian-like law, no experiments) | `01:319–320`, `03:315–323`, `04:524–532`, `04:574–583`, `07:654–655`, `08:591–592` | each stated once in Section 2 and once in the Discussion | −0.5 p |
| Section 9.1 recap | `09:67–97` | list only the properties the theorem uses | −0.5 p |
| Appendix E tools | `E:29–110` | cross-reference list; external tools in Appendix A | −1.5 p |
| Quadratic face lemma | `C:220–255` | corollary of `lem:qp:face` | −0.7 p |
| Approximation corollary | `03:220–239`, `A:124–136` | cut, or one remark | −0.4 p |
| Section 3 preamble | `03:10–16` | pointer to Section 2 | −0.2 p |

## Part C. Accepted pending fixes still visible in the frozen text

These are not new findings. They come from:

- the integration contract (`evidence/integration-contract.md`);
- the root reviews (`evidence/reviews/root-*.md`);
- the Sol reviews (`evidence/reviews/*-sol*.md`);
- the author reports (`evidence/author-reports/*.md`).

They are listed so that the next snapshot can be checked against one list.
"Resolved" means that the snapshot already contains the accepted repair.

| # | Item | Frozen location | Source | Status |
| --- | --- | --- | --- | --- |
| C1 | Common-root fallback output with degree/height budget | `02:344–348` vs `03:518–552`, `A:428–509`; callers `05:109–110`, `06:200–202`, `07:419–421` | contract; early foundations 1; `fallback-shared-root-sol.md`; K10 | pending |
| C2 | Fallback output length "up to B" | `03:540–541` | early foundations 3 | pending |
| C3 | Scope of closure and fallback (now over-narrowed, see A14 item 8) | `03:251–260` | early foundations 4; root counting 2 | pending |
| C4 | "A Turing machine can sample only ..." | `03:264` | root counting 1; early foundations 5 | pending |
| C5 | Singleton domain (`S = 0`) in the rare budget | `03:467–478`, `A:413–424` | early foundations 2 | pending |
| C6 | Intermediate bit length in the Taylor weights | `A:218` | early foundations 6 | pending |
| C7 | Renegar conventions | `A:328–342` | early foundations 8 | pending |
| C8 | `O(log n)` allowance for Euclidean `q`-bit point error | `03:528–534`, `A:494–508` | early foundations 7; contract | pending |
| C9 | `thm:qp:two(b)` accuracy unbounded | `04:251–252`, `B:254–255` | early quadratic 1; contract | pending |
| C10 | Lower integration limit in `rem:qp:moments` | `04:281–283` | early quadratic 2; contract | pending |
| C11 | Empty mixed feasible set | `04:33–48`, `04:534–548`, `04:314–315` | early quadratic 3; contract | pending (`thm:qp:gauss` already reports `X` empty at `04:507`) |
| C12 | Reconstruction guard; singleton auxiliary ranges kept in the full model; retained-cell ball; "finite minimum" wording | `B:204–212`; `B:191–194`; `04:213–216`; Appendix B concavity sentence | early quadratic 4, 5, 7; contract | pending |
| C13 | Supplied frame constant must be rational; queried-pair inclusion | `04:84–93`; `04:340–345` | early quadratic 7 | pending |
| C14 | Patch output definition omits singleton-hull fixing | `02:326–328` vs `05:110–114` | early sparse 5; contract | pending |
| C15 | "All three routes need ..." fixed feasibility; (P1) for orders | `01:260–264`; `06:3–25` vs `06:598–599` | contract; complete sparse Sol | pending |
| C16 | Rational quadratic outputs only for polyhedral/box classes | `01:194–195` | contract | pending |
| C17 | Actuator curvature `L_q >= 0` | `06:426–432` | early sparse 2; contract | pending |
| C18 | Coefficient lengths in the uniform family | `06:65–78`, `D:47`, `D:322–323` | early sparse 4; contract | pending |
| C19 | All-fixed instances before maxima | `05:35–65`, `05:776–791`; actuator | early sparse 5; contract | pending |
| C20 | Simplex S1 (equality multipliers), S2 (coarse corners), S3 (empty block), S4 (point evaluation); graph S5 | `06:573–594`; `D:350–621`; `D:9–200`, `D:286–300`, `D:968–987` | complete sparse Sol r1; contract | pending |
| C21 | Hardness/threshold sentence | `05:901–906` | early sparse 5; complete sparse Sol | pending |
| C22 | Solver value map; `epsilon = 0`; projections | `08:63–96` | K1–K3; contract | pending |
| C23 | Affine margin for empty zero sets | `08:408–410` | K4 | pending |
| C24 | TU theorem inherits the flow premises | `08:417–424` | K5; contract | pending |
| C25 | Potential bit lengths; short cycles | `08:229–238`; `F:484–499` | K6; N2 | pending |
| C26 | Meaning of strong-field evaluation; interior-flow refinement | `08:483–484`; `08:283–295` | K7 | pending |
| C27 | Certified empty-core search | `07:193–198`, `E:138–143` | K8; root recourse 1 | pending |
| C28 | Impossible restrictions; all-fixed strong field; zero-row lattice | `08:165–169`, `08:454–466`, `08:533–537` | K9 | pending |
| C29 | Flow nonemptiness | `08:256–265` | N1 | pending |
| C30 | Recourse wording: certificate size vs verification work; SOS for the residual Hessian; the `k = 0` sentence | `07:87–93`; `07:402–404`; `07:437–439` | root recourse 3–5 | pending |
| C31 | Lattice theorem is quartic-only, but the introduction says "separable convex polynomial terms" | `08:531–533` vs `01:69–71`, `01:156` | `integer-lattice-generalization-sol.md` | pending (extension) |
| C32 | X16 deterministic flow-core error bound | absent | decision 10 | pending |
| C33 | B10 bridge | `09:296–348` | decision 10 | resolved; attribution per A2 |
| C34 | Direct width-two SRS boundary | `09:725–732`, `G:247–334` | decision 11 | resolved |
| C35 | Threshold `delta >= 0`; narrowed conclusion; level-0 nonclosure | `09:561–593`, `09:260–273` | early boundaries 1–3 | resolved |
| C36 | Uniform resolution replaces the universal-law open question | `02:169–242`, `10:69–75` | `universal-law-budget-sol.md` | resolved; placement per A9 |
| C37 | Original-objective qualification; Gaussian support calibration | `01:309–316`, `02:464–500`, `04:574–579`, `10:16–25` | contract | resolved |
| C38 | Duplicate ambient barrier; regret remark; `Q_ex` redefined in the Table 1 caption | `04:630–651` vs `09:392–423`; `04:574–583`; `01:129–130` | front report §5.1, §7; quadratic report §4.2 | pending (Part B) |
| C39 | Star example stated twice | `07:145–171` vs `09:227–286` | root model 10 | partly resolved (Part B) |
| C40 | Bibliography; key alias `BasuLerario2023` vs `basu2023-...` | `01:359` vs `07:563` | front report §6; recourse report §5 | pending (by design) |
| C41 | Overfull boxes | `A:329–342`; `E:209`, `E:296`, `E:398`, `E:503–512`, `E:656–666`; `F:376–380` | root typesetting | pending |

## Part D. Suggested wording

**D1. Abstract, the sentences on few negative directions and on the small
core.**

> For quadratic and mixed-integer quadratic programs with `k` negative
> eigenvalues and `n_z` integer variables, the expected bit work is
> `f(n_z)(c k (1 + nu D/sigma))^k poly(I)` with an absolute exponent under
> Gaussian-like noise on all coefficients, where `D` is the diameter of the
> relaxation. It is also polynomial for continuous problems under noise
> aligned with the negative directions. These bounds are fixed-parameter in
> `k` and `n_z` when the curvature-to-noise ratio is bounded. Under uniform
> noise on all coefficients the bound is polynomial for each fixed `k`, with
> a power of the dimension that grows with `k`. ... For a small continuous
> core whose fixing leaves tractable recourse, the bound is
> `8^k [3+(1+k)L/(2 sigma)]^k poly(I)`.

**D2. Companion paragraph (replaces `01:401–416`).** Luna should check the
details before this text is frozen.

> Three unpublished companion manuscripts overlap with this paper.
>
> - [companion-decomposition-aware] studies deterministic
>   decomposition-aware optimization. It contains the deterministic layer of
>   our sparse and core searches:
>   - corrected product-grid lower bounds and min-marginal filtering;
>   - the value-function curvature lemma and a corrected core search with
>     exact or certified conditional values;
>   - the validity of bag-local corrections with certified conditional
>     values, and the star example showing that grid min-marginals do not
>     suffice.
>
>   Under a growth assumption with condition number `kappa`, it obtains
>   bounds `f(p,kappa) poly(I)` through graded grids. Under rETH, it shows
>   that the exponent of `kappa` cannot be `o(p)`. We re-prove the
>   deterministic statements we need. Our contribution is the smoothed
>   layer: finite-law counts without a growth premise, closure certificates,
>   and a same-draw fallback. Section 5.4 explains why the
>   growth-conditioned bound does not yield a bound that is fixed-parameter
>   in the width under linear noise.
> - [companion-exact-arithmetic] studies exact output formats for polynomial
>   optimization. Under noise on a core it obtains:
>   - values and selected cores for residual-convex problems;
>   - full selected optimizers under a supplied convexifier, and for
>     residual-convex cubics without any residual modulus;
>   - the Square Root Sum and PosSLP quartic reductions and their core-only
>     consequence at degree four.
>
>   We reproduce those reductions in Theorem 9.x and Proposition 9.y. Our
>   core-only results cover every fixed degree under a certified uniform
>   residual modulus (Theorem 7.x), and integer flow and totally unimodular
>   recourse (Section 8).
> - [companion-sparse-indicator] perturbs only the indicator penalties of
>   sparse positive definite indicator quadratics by the same grid law. It
>   computes exact separator messages at fixed treewidth. It shows that,
>   unless NP ⊆ ZPP, numerical dependence cannot be replaced by dependence on
>   encoding length. Its indicator constraints lie outside our mixed-box
>   model, and neither paper contains the other.

**D3. Width open question (replaces `10:110–116`).**

> Is there an exact algorithm for sparse polynomial optimization under
> independent linear noise whose expected work is fixed-parameter in the
> width? The global-error retention rule cannot give one (Theorem 9.1). A
> bag-local allowance is unsound with grid min-marginals (Proposition 9.2),
> but sound with certified conditional values (Proposition 9.3). Graded grids
> remove the dimension factor when the growth ratio is bounded
> [companion-decomposition-aware], but their exponent of that ratio cannot be
> integrated against the growth tail of Theorem 3.x.

**D4. Overlap sentence in Section 9 (replaces `09:758–762`).**

> Parts (a) and (b), the deterministic consequence, and the core-only
> consequence in (c) also appear in [companion-exact-arithmetic]. We
> reproduce the constructions with proofs to keep the paper self-contained.

**D5. Discussion, first use (replaces `10:9–14`).**

> The randomness is introduced by the algorithm. The guarantees are
> smoothed-analysis statements about a randomly perturbed copy of an
> arbitrary instance, and, through Proposition 2.x, certified approximations
> for the original instance. They do not apply to data whose noise follows
> another law.

## Checks performed

All checks were targeted to this review. None is a CI result.

1. **Snapshot identity.** An inline `python3 -I` check compared all 20 files
   in `manifest.json` by SHA-256 and byte count. All matched.
2. **Manuscript reading.** I read every line of Sections 00–10 with line
   numbers. In the appendices I read:
   - A: in full;
   - B: lines 1–12, 186–340 and 599–715, plus the full outline;
   - C: in full;
   - D: lines 1–630, plus the outline of 631–994;
   - E: lines 1–112, 270–340 and 471–560, plus the outline;
   - F: lines 1–70, 502–560 and 891–983, plus the outline;
   - G: lines 1–20 and 175–300, plus the outline.
3. **Evidence files read.**
   - `BRIEF.md`, `independent-review-brief.md`, `integration-contract.md`,
     `integration-decisions.md`, `root-mathematical-findings.md`,
     `STATUS.md`, `notation.md`, and lines 1–60 of `architecture.md`.
   - The author reports `front-r1.md`, `quadratic-r1.md`, `sparse-r1.md`
     and `recourse-r1.md`, lines 1–80 of `universal-law-budget-sol.md`, and
     the headings of the other supplements.
   - The root reviews of the introduction, model, counting, recourse and
     typesetting.
   - The Sol reviews `early-boundaries-sol-r1`,
     `early-foundations-sol-r1`, `early-quadratic-sol` (findings and
     interfaces), `early-sparse-domain-sol` (findings),
     `early-integer-interfaces-sol` (finding headings),
     `complete-recourse-sol-r1` and `complete-sparse-domain-sol-r1`.
4. **Targeted searches over the snapshot.**
   - Names used for `sigma`; route counts; novelty phrases; companion
     mentions; intensifier words; citation keys used.
   - Parametric-programming attribution, checked in both complete snapshots.
     `04-quadratic.tex` has the same hash in both.
5. **Label and reference scan.** An inline `python3 -I` script found
   theorem-like labels that are never referenced, and results referenced
   only from their own file.
6. **Companion manuscripts.** These were local repository reads, not
   literature research:
   - `paper-exact-arithmetic/sections/10-recourse.tex`, lines 1–60, 138–160,
     272–290, 398–420 and 572–600, plus its abstract;
   - `paper-decomposition-aware/sections/`: `abstract.tex`,
     `growth-sharp.tex` lines 1–30, `limits.tex` lines 340–365, the opening
     paragraphs of the recourse and constraint section files,
     `recourse-local.tex` lines 36–75, and the theorem lines of
     `recourse-cuts.tex`;
   - `paper-sparse-indicator-quadratics/main.tex` lines 30–58 (abstract),
     and a search of its introduction.
7. **Messages.** Two messages with the prompt findings were sent to the root
   thread.
8. **Not performed.** No TeX, source or bib file was edited. No build,
   experiment, literature search, project-wide verification, CI inspection,
   commit or delegation was performed.
