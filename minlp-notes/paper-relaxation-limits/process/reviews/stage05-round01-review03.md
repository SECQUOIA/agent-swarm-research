# Stage 5, round 1 — independent reviewer 03

**Verdict: PASS.** I found no major or minor defect in the assigned frozen Stage 5. In particular, both order-one refinements are valid under the stated full-coordinate-domain quadratic moment oracle. The additional focus on the full local preordering, equality budgets, repeated or conflicting factors, and nonclosed coordinate sets does not reveal an omitted constraint.

## Coverage

All manuscript locations below refer to `process/snapshots/stage05-round01/`, not the working manuscript.

I read completely:

- `sections/13-xor-quadratic-hulls.tex`, lines 1–333, printed Section 16.
- `sections/14-monomial-reformulations.tex`, lines 1–228, printed Section 17.
- `sections/15-finite-certificates-affine.tex`, lines 1–218, printed Section 18.
- The shared dependencies `sections/01-foundations.tex`, `sections/11-coordinate-domains-lifts.tex`, and `sections/12-relative-blocks-cuts.tex`. For Stage 5, the operative dependencies are the certified-cover and tolerance conventions, multiaffine vertex minimization, the scope of coordinatewise endpoint interpolation, and the preceding clique/decomposition escape discussion. Stage 5 does not import the earlier fractional-cardinality positivity theorem into its XOR construction.
- Frozen `main.tex`, `macros.tex`, and the four Stage 5 entries in `references.bib`. Stage 5 introduces no separate appendix or mathematical dependency on an earlier appendix.

Process material read: `process/review-protocol.md`, `process/stage-05-review-assignment.md`, `process/stage-05-author-assignment.md`, `process/stage-05-author.md`, the Stage 5 rows and common conventions in `process/scope-proposal.md`, `process/order-one-monomial-refinement.md`, focus 03 in `process/stage05-reviewer-focus.json`, and frozen `verification/stage05-primary-sources.json`. I also read the frozen author checker as supporting verification context; I did not use its output as independent proof or rerun it as my own checker.

I read all three canonical sources and all four mapped correction/audit notes in full, relative to the repository root:

- `results/spatial-bb-quadratic-cut-exponential-lower-bound.md`.
- `results/spatial-bb-monomial-lift-exponential-lower-bound.md`.
- `notes/spatial-bb-affine-branching-barrier.md`.
- `notes/review-spatial-bb-beyond-clique.md`.
- `notes/review-spatial-bb-beyond-clique-second.md`.
- `notes/review-spatial-bb-bounded-monomial-lift.md`.
- `notes/review-spatial-bb-affine-branching-barrier.md`.

These older mapped audits were treated as correction records, not mathematical authority. I did not read another reviewer’s report from this round, edit manuscript files, or delegate.

### Primary-source reading and access

I read `literature/AGENTS.md` before accessing originals. All four mapped originals were accessible. Their independently calculated SHA-256 digests match the frozen source ledger; paths and digests are recorded in `verification/reviewer03/stage05-round01/source-access.json`.

1. **Schoenebeck, author full version.** Original: `/tmp/minlp-relaxation-limits-sources/schoenebeck-full.pdf`; extraction: the adjacent `schoenebeck-full.txt`. I read the complete 19-page extraction, including definitions, Theorems 11–12, all of Lemma 13, and the width argument in the appendix. I visually inspected printed pages 7 and 10 against the PDF renders. The source specifies independent clauses with distinct variables; its width closure and signed-class construction agree with the manuscript’s conversion. Theorem 11 gives a strictly positive constant, avoiding dependence on Theorem 12’s weakly written `alpha >= 0`. The printed norm-zero sentence contradicts its immediately preceding displayed unit vector; the manuscript correctly normalizes the constant vector. The chosen `gamma=1/4` avoids the displayed denominator boundary. The open [author PDF](https://schoeneb.people.si.umich.edu/papers/LasserreNew.pdf) was also accessible through the web tool.
2. **Ahmadi–Dash–Hua–Stellato, arXiv 2605.28674v1.** Original: `literature/papers/ahmadi2026-disjunctive-sum-of-squares/original.pdf`; corresponding `fulltext.md`. I read the abstract/introduction, Definitions 1–2, Theorem 1 and its context, the simplicial construction and Theorem 8 statements, Sections 6.1–6.2, and the closing scope discussion. I rendered and inspected original printed pages 4, 8, 31, and 32 because the extraction loses displayed formulas. The local SDP and spherical/simplex region models differ from the present oracle; Algorithms 2–3 use a scaled positive-tolerance stopping test. The manuscript only reports their stated positive-tolerance termination and makes no numerical identification with its own tolerances or lower bound on these algorithms. [Version metadata](https://arxiv.org/abs/2605.28674v1) was accessible and confirmed.
3. **Beame et al., arXiv 1710.03219v3.** Original: `/tmp/stage05-author-sources/stabbing.pdf`, with adjacent text extraction. I read the abstract and introduction through the result statements and subsequent-work discussion on printed pages 1–4, and visually checked Theorem 1 on printed page 3. Its bound is quasipolynomial, and its integer-negation disjunction permits omitting an integer-empty slab. Both qualifications are preserved. [Version metadata](https://arxiv.org/abs/1710.03219v3) confirmed the 2023 version.
4. **Fleming et al., arXiv 2102.05019v2.** Original: `/tmp/stage05-author-sources/branch-cut.pdf`, with adjacent extraction. I read the abstract and introduction through Theorems 1.1–1.5 and their surrounding explanation; I visually checked printed page 4. Theorem 1.3 concerns CNF encodings and measures size relative to the encoding, while Theorem 1.4 restricts coefficients in SP*. The manuscript retains these scopes. [Version metadata](https://arxiv.org/abs/2102.05019v2) confirmed the cited version.

For the three comparison papers, this is a verification of the inspected definitions and result statements, not a fresh proof audit of every theorem in those papers. No access failure prevents checking a Stage 5 ingredient. No priority conclusion follows from this targeted reading.

## Findings

None. The following checks explain the PASS verdict rather than impose additional requirements.

## Independent verification

### Full node preordering and equality budgets

At `13-xor-quadratic-hulls.tex:85–130`, substitution fixes a coordinate whenever its set fails to contain both Boolean endpoints. Witness membership ensures the substituted sign is in that set, even if the set is nonclosed or consists of a singleton. A surviving coordinate permits both endpoints. Thus every locally valid polynomial has nonnegative endpoint values; its Boolean reduction is the displayed nonnegative endpoint interpolation. This uses membership, not continuity, compactness, or a finite description of the domain.

For a product with total generator degree `a` and multiplier degree `d`, the node condition is `a+2d <= 2r`. Every nonconstant generator consumes at least one degree. After expanding endpoint interpolation, each indicator product `I` has degree at most `a`; factors may repeat, and contradictory factors give zero. In the Boolean quotient,

```
I P_hat^2 = (I P_hat)^2,
deg(I P_hat) <= a+d <= 2r.
```

The original expression, expanded expression, and squared expression all have degree at most `4r`. Boolean reduction never raises degree, so truncated identity consistency is sufficient. Constant or zero generators cause no exception. With no generators, the same argument is ordinary square positivity. Globally coupled multipliers are allowed throughout.

At `14-monomial-reformulations.tex:80–110`, replace the indicator and multiplier bounds by `Da` and `Dd`. This gives square degree at most `2D(a+d) <= 4rD`; the localizer’s literal pullback has degree at most `D(a+2d) <= 2rD`. Products of parity indicators are idempotent without requiring disjoint supports, independent equations, or consistent prescribed signs. The source’s identity convention therefore proves every granted localizer at its actual budget.

Every local equality evaluates to zero at a restricted sign or has zero values at both surviving endpoints. Multiplication by an arbitrary permitted global polynomial preserves its zero Boolean reduction. Every graph identity has identically zero literal pullback before applying the functional, and any allowed product has degree at most `2rD`. Neither case assumes that an equality generator has a special form or comes from a chosen generating set.

### Signed realization, objective cost, and cover count

The signed-matrix lemma at `13:159–179` correctly includes the constant vector’s class. Unit Gram vectors with inner product of absolute value one coincide up to sign; other classes are orthogonal. Fixing the constant class to one and choosing independent unbiased signs for the other classes realizes all augmented entries, including deterministic means and cross moments with the constant class.

For the unlifted theorem, marginalizing the actual quadratic law and fixing the other coordinates gives exactly the constructed functional’s degree-two moments. For the lifted theorem (`14:112–125`), the augmented matrix is PSD because a lifted linear square pulls back from a polynomial of degree at most `D`; diagonal entries are one and all entries are signed character moments. Its realizing law fixes each restricted coordinate almost surely because that coordinate’s mean is an endpoint. The resulting finite law lies in the actual coordinate product, so no closure of a nonclosed hull is needed. It may leave the graph. The manuscript neither replaces the box hull by the graph hull nor grants localizers or products of arbitrary coupled quadratic cuts.

At `13:132–148` and `14:127–158`, untouched clauses retain zero pseudo-cost, at most `Delta` times the number of fixed originals are affected, and positivity of `(1 +/- chi_A)^2` bounds each substituted cost between zero and one. The six-degree calculation is available under the stated hypotheses. Occurrence counts include clause repetitions. The original Boolean witness fraction is exactly `2^(-|R|)`.

In the lift, the restricted signed coordinates impose a consistent binary affine system of rank `q`. Its fiber has exactly `2^(n-q)` assignments. A coordinate absent from every original basis row is absent from their span, so the support union of all rows equals the basis-row union, and `|C| <= Dq`. This proves the claimed witness bound with arbitrary repeated supports and arbitrarily many auxiliaries. Empty restriction sets have rank and union zero and cannot certify a positive target. A witness-free region contributes zero mass. The union bound needs neither disjoint regions nor a split-tree representation, and charged discarded regions remain necessary under the shared cover convention.

### Width, random family, constants, and order one

The width construction at `13:187–229` is complete. Opposite derived signs imply contradiction; the signed relation on supports of size at most `floor(w/2)` is transitive because the symmetric difference of two such supports has size at most `w`. Its Gram identity proves positivity for any polynomial in that character span, including polynomials whose collective support is much larger than the degree bound. Defining top character moments directly also handles odd `w`. Thus the required original degrees are `4r` and `4rD`, respectively.

At `13:261–312`, the independent random clause signs give a binomial violation count for each fixed assignment regardless of support overlaps. The displayed generating-function bound with `t=1` is `exp(-n)`; the assignment union bound tends to zero. Differentiating the binomial generating function gives exactly `48(1+3/n)^(8n-1)`. The bound on expected deletion is below `n/8`, and Markov’s inequality supplies an event intersecting the two high-probability events for every sufficiently large integer `n`. Independence between those events is unnecessary. Removing at most `n` clauses leaves `7n <= m <= 8n`, maximum occurrence at most 64, and at least `n` violations at every vertex. Multiaffinity then gives continuous `OPT >= 1/8`. The same functional survives deletion and restriction to every smaller permitted degree.

The best-incumbent absolute and relative targets are both at least `1/16`; a worse incumbent cannot weaken them. Consequently the original exponent is `7n/(16*64)=7n/1024`, and the `D=3` exponent is `7n/3072`. The factorable graph uses exactly two auxiliaries and two quadratic equations per clause, so `N=n+2m <= 17n`, giving the displayed `7N/52224` comparison. Differentiating the normalized objective yields the stated gradient and symmetric-Hessian row-sum bounds.

For lifted `r=1`, all first/second moments, local equality products, graph identities, and the preceding preordering construction remain available. The clause-cost square needs `3 <= 2rD`, for which the stated integer condition `rD >= 2` suffices. Objective availability is separately required by `deg Phi <= 2r`; exact polynomial pullback supplies the objective comparison. Thus the original cubic remains at `r>=2`, while the linear pair-plus-clause objective allows `r=1` with source width at least 12. The degree/region corollary is explicitly confined to `4rD <= an`; taking logarithms gives the claimed necessary `D=Omega(n/log n)` for a polynomial count in original dimension. There is no unsupported statement in an arbitrarily inflated lifted dimension.

### Both upper certificates and affine boundaries

The Bernstein identity at `15:19–51` uses eight nonnegative corner differences and three normalized bound slacks, so order two suffices. Its average lower bound loses at most `3h/2`, where `h=2/ceil(3/epsilon) <= 2epsilon/3`. This remains valid when `epsilon >= 3`, for which there is one interval. The lifted graph transfer has degree three, with multiplier `x_k` on the first quadratic equality; it is available at order two.

For the new order-one certificate (`15:64–107`), the actual box distribution supplies only first and second moments. The two equalities on moments imply

```
|L[v_e]-a_i*a_j*a_k|
<= |L[u_e*(x_k-a_k)]| + |a_k|*|L[x_i*x_j]-a_i*a_j|
<= h+2h.
```

Every expression evaluated is quadratic or lower. Expansion of the displayed quadratic-cut identity cancels `u_e*x_k` and `a_k*u_e` exactly, leaving the required signed clause difference. Its pointwise nonnegativity holds on the entire box with `u_e` independently bounded by one. Graph-supported realization is neither used nor needed. This proves the bound for every feasible functional and therefore its infimum, including the convention for no feasible functional. Both upper certificates yield `48^n` at `epsilon=1/16`; because `OPT>=1/8`, this target also implies the stated relative target.

The first affine obstruction (`15:127–145`) contradicts zero first moment and positive second moment for a nonnegative random variable; symmetry gives at least half the witnesses for all `n>=1`. For the substitution obstruction (`15:149–177`), assuming both strict count failures gives enough free variables for an indicator on `a+1` negative signs and permitted degree `1+2(a+1) <= 2r-1`. Its exact localizer is `-2^(-(a+1))`; negative `a` is already rejected by the constant multiplier. The order-one necessary bound is explicitly trivial. These examples show failure of the present method only. Finally, an inconsistent Boolean XOR formula gives a normalized lower bound of only `1/m`; multiaffinity transfers that value to the cube but cannot increase it to a fixed gap.

### Independent executable checks and build

I wrote and ran `verification/reviewer03/stage05-round01/check.py` using standard Python exact rational arithmetic. Its result is in `check.json`:

- 7,800 coefficientwise Boolean-quotient localizer identities using signed, overlapping and repeated supports, nonnegative endpoint interpolation of linear and quadratic generators, and coupled multipliers. The expansion includes 1,400 zero indicator summands. It also checks deterministic substitutions and vanishing local equalities.
- 13,824 rational vertex checks of the quadratic upper-cut inequality and identity over 216 selected boxes, including unequal widths and singleton coordinates, both clause signs, and independent auxiliary endpoints.

These checks test finite algebraic cases; they do not establish the universal transfer or random-width theorem. The proof audit above supplies the universal reasoning. I did not claim an LP distribution experiment or numerical SDP verification.

An independent `latexmk -pdf -interaction=nonstopmode -halt-on-error` build from the frozen snapshot, with all output directed to the assigned verification directory, completed successfully and produced 91 pages. The final log has no unresolved references, citations, or overfull boxes. It has one underfull-hbox diagnostic in the unchanged `appendix-structural-auxiliary.tex`, outside Stage 5. I visually inspected the independently built pages 65, 70, 71, 73, and 74; no clipping or unreadable Stage 5 equation was found. Build output and renders are in the same verification directory.

## Remaining limits

The proof does not address localizers of all coupled quadratic cuts, exact feasible-graph hulls, arbitrary affine branching, monomial degrees outside the imported source-width regime, or computational tractability of the exact quadratic box oracle. The manuscript states these boundaries. The comparison-source reading does not audit all external algorithms or establish priority. The frozen introductory abstract still reflects the earlier stage; complete-paper integration is assigned to Stage 6 and is not a missing Stage 5 proof.
