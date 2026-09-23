# Stage 5C independent review 5

Reviewed the integrated draft on 2026-09-20. **No major issue found; three minor corrections are listed below.** These concern the precision of the introductory scope statements, not defects in the three principal mathematical results.

I read the applicable project instructions and reviewed `main.tex`, all of `sections/00-introduction.tex` and `sections/13-synthesis.tex`, the revised foundations opening, `macros.tex`, the new bibliography entries, `README.md`, and the source-map opening and routing. I checked the underlying statements and relevant proofs for the headline formulas. I did not read other Stage 5C reviews, assessments, preparation checks, or helper reports. This is the integration review, not the separate whole-paper review.

## Minor issues

### R5-1. State positivity in the introductory Hessian comparison

**Location:** `sections/00-introduction.tex:107–112`, equation `eq:intro-transfer`.

**Reason:** The displayed hypothesis gives only `mu D^0 <= D <= L D^0`. It does not state that `mu` is positive, although the conclusion inverts `mu` and uses it as a positive spectral-equivalence constant. Strict feasibility of `D` and `D^0` does not imply positivity of an arbitrary supplied lower bound `mu`. For example, `D=D^0`, `mu=-1`, and `L=1` satisfy the written matrix sandwich but not its asserted upper Hessian bound. The cited theorem correctly includes `0<mu<=1<=L`.

**Correction:** Insert `0<mu<=1<=L` immediately before or after the introductory matrix sandwich. No proof change is needed.

### R5-2. Scope the same-certificate requirement to this paper's rank-dependent work theorem

**Location:** `sections/00-introduction.tex:126–128`.

**Reason:** “A movement bound composes with work only when the same exposed rank enters both estimates” states a general necessity that does not hold. A distance lower bound, an upper bound on movement per round, and a uniform positive cost per round already compose, even if the cost bound does not involve any exposed rank. Retaining the same certificate is necessary for the particular rank/resource composition proved in `work:total`; the proof does not establish the asserted general necessity.

**Correction:** Say, for example: “Our rank-dependent work bound retains the same exposing certificate in the curvature and movement estimates and assumes an explicit fresh charge per round (Theorem ...).” Keep the following warning against multiplying a one-shot query lower bound by checkpoint counts.

### R5-3. Name the capped family when introducing the remaining barrier seam

**Location:** `sections/00-introduction.tex:74–77`.

**Reason:** At this point `B` has been defined for an arbitrary finite dictionary of simple symmetric cones. The paragraph then refers to “the remaining bounded narrow-cap cases” without naming the fixed-field Hermitian order-cap or Lorentz dimension-cap families to which the cited classification boundary belongs. The corresponding passage in `sections/06-restricted-barriers.tex:324–334` states those families explicitly. The displayed interval is not being challenged; the missing qualification makes the scope of “remaining” unclear in an introduction that promises to specify optimization classes.

**Correction:** Add “for a fixed-field Hermitian order cap or a Lorentz dimension cap” and identify `B` as that cap's primitive capacity. Do not present this as a classification boundary for arbitrary mixed dictionaries or all exceptional-cone models.

## Mathematical and scope checks

- **Local geometry and exact resource counts:** The two-sided derivative argument removes the primal and dual contact directions, giving the dimension-minus-two channel bound; the Peirce overlap gives `apq`. The norm-tree construction uses `k=ceil((s-1)/(d-2))` factors and total dimension `s-1+2k`. The introduction correctly distinguishes factor dimension from Jordan rank.
- **Entire-fiber rank:** I checked the minimum-rank semialgebraic choice, the dense open lower-bound locus, reduction to smaller faces, and the Peirce-perspective attainment, including non-full coordinate groups and zero objective groups. The worst-support/minimum-fiber quantifiers in the abstract and introduction match `thm:rank-frontier`; the exceptional pole does not alter the maximum. The Albert case uses Jordan identities rather than an unproved associative representation.
- **Global versus generic selection:** The introductory claims match the stronger full-slack global selection statements. They do not globalize a generic selector or replace an entire-fiber hypothesis by one favorable completion.
- **Barriers:** Ambient standard, restricted standard, and intrinsic fixed-domain parameters remain distinct. The narrow-cap interval is not asserted to be exact. The nonsymmetric discussion preserves its logarithmically homogeneous scope in its cited section. The introduction does not claim intrinsic norm-tree optimality.
- **Weighted tree distance:** I checked the telescoping active pairings, inactive-subtree determinant bound, product dual norm of the lower potential, and the explicit upper curve. They yield the stated `K_c`, with the objective and tree fixed before accuracy tends to zero. The central-route coefficient and its excess agree with the cited corollary.
- **PSD quotient:** Eliminating the auxiliary directions yields the stated quotient. Exact allocations identify the middle trace with `M_0`, which gives first-power bounds. The two-source example realizes the relative condition factor. The introduction preserves the distinction between Hessian comparison, the reduced right-hand side, and preconditioner construction.
- **Computational contracts:** I checked the cited work theorem, central-start primal–dual gap statement, and fresh-update maintenance statement against their introductory summaries. Fresh adversarial batches are not advertised as a fixed conic program's Newton trajectory. Output and access distinctions remain visible.

## Source disposition

I independently parsed the historical linked inventory and compared its resolved paths with both current workbench directories. There are **201 links, 201 unique paths, no missing files, no stale paths, and no unlisted current notes**. The initial groups contain 128 core sources, 10 context sources, three navigation sources, and 60 excluded sources. Applying the six context promotions, two excluded-source promotions, and two excluded-to-comparator changes gives exactly **136 included, six comparator-only, 56 excluded, and three navigation sources**.

The opening explicitly controls the historical dispositions, so superseded exclusions and deferred-stage wording are not current omissions. The dynamic scale source is routed to its fresh-update, reusable-service, and fixed-data results. The direct-ball comparator explicitly changes feasible bodies. Entropy compilation keeps ambient `3N/3B` separate from fixed-slice `N/B`.

The retained spectral movement overlap is attributed to the companion. Its separate water-filling, shortest-path, and shortcut programs are reasonable comparator boundaries. The solver and spectral-access projects excluded from the present paper likewise have identifiable scope; I found no integration-level reason to require their wholesale inclusion. The file-level inclusion count does not claim 136 independently new theorems or validate every workbench headline.

## Literature, contribution, and presentation

I compared the new positioning with primary records for [Scheiderer's Theorem 1.2](https://arxiv.org/html/2509.17121v2), [the lifts survey](https://arxiv.org/abs/2002.09788), [Averkov](https://arxiv.org/abs/1806.08656), [Saunderson](https://arxiv.org/abs/1902.06401), and [Kummer](https://arxiv.org/abs/1506.07699). Their representation resources differ from the present fiber minimax; the introduction does not conflate SOC existence with its quantitative frontiers. The Scheiderer version date is correct.

The references to existing barrier theory are consistent with [Hildebrand](https://arxiv.org/abs/1909.01883) and [Cardoso–Vieira](https://optimization-online.org/wp-content/uploads/2003/11/774.pdf). The [iterative-refinement article](https://doi.org/10.1007/s10107-024-02183-z) supports the stated high-precision improvement, and its 2026 volume, pages, and author list agree with the new entry.

I also inspected the relevant source in `../central-path-cost/`: the exposed-minor theorem, matrix-ball compressed estimate, and grouped/packed/tree calculations substantiate the overlap attribution. The present three highlighted contributions are stated as specific formulas with specific quantifiers; the introduction does not claim priority for standard Jordan algebra, self-concordance, matrix order, or query lower-bound methods. Bounded independent searches found no concrete priority collision, which is not proof of priority.

A clean build from a temporary copy containing only manuscript sources succeeded with `conda run -n qipm --live-stream make`: 183 pages and 87 bibliography items, with no final LaTeX/BibTeX warnings, undefined references, or overfull/underfull boxes. I inspected the rendered title/abstract and model-table pages and extracted the introductory PDF text. The six-part structure, appendices, notation guide, anonymous metadata, and README build instructions are consistent. No manuscript file was edited.
