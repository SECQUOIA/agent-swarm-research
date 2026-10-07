# Final GPT editorial review, round 1

Review completed on 2026-10-06 UTC (2026-10-05 EDT). This is a fresh whole-manuscript editorial review, supported by three independent GPT reads of the front claims, Sections 3–5, and Sections 8–9 plus the appendix. No Opus model was used. Only this review file was written.

**Final prose disposition: ACCEPT.** The narrow final re-read confirmed every remaining repair and all small clarity/navigation suggestions. No editorial finding remains open. Bibliography/source integration and the final PDF build remain separate integration tasks; this acceptance does not claim they are complete. The final repair verification and source hashes are recorded at the end of this report. Earlier findings and intermediate dispositions are retained as the review history.

**Readiness verdict:** The paper has a coherent journal-paper argument and needs no broad rewrite. Its main rate summaries, regularity restrictions, and certificate distinctions agree with the theorem statements. The current snapshot is not yet ready for submission: fix the precise scope and explanation issues below, complete the bibliography/source integration, and rebuild the final PDF. I found no fatal editorial defect or contradiction in the central result chain. This verdict concerns exposition and claim correspondence; it does not replace the separate mathematical audits.

**Follow-up after root's integration:** I re-read the changed passages and confirmed the repairs in findings 1, 3, 4, 5, and 6. The front-matter and discussion portions of finding 2 are also resolved: the abstract now includes rational input length, and the introduction/discussion explicitly include the slack. The findings below retain the original review snapshot and its line numbers; this disposition describes the later source. The remaining changes are narrow prose and scope clarifications, not a new major concern.

| Finding | Follow-up disposition |
| --- | --- |
| 1. Rational bag data | Resolved at current `09:271–274`; every supplied local $f_b$ is rational. |
| 2. Rational encoding scope | Resolved in abstract, introduction and discussion. For consistency, current `09:6–8` and `09:295–296` should also include rational input length when summarizing the theorem. |
| 3. Merge/split cone | Resolved at current `01:229–230` and `10:39–41`; both explicitly say full-preordering certificate. |
| 4. Paired functions | Resolved at current `05:16–18`; the minima are explicitly $-\varphi$ and $\varphi$. |
| 5. Slack order | Resolved at current `05:271–272`; exact order is attached to the lower bound. |
| 6. Supported measure | Resolved at current `05:335–338`; $L_1(xy)>L_1(x)$ rules out a rectangle-supported measure. |
| 7. Source feasibility | Remains in Section 6. The analogous introduction wording at current `01:221–222` should also say “guaranteed to be feasible at the conditional source mean, but need not be feasible at the output point.” |
| 8. Global exponent | Remains at `08:396–398`; narrow the claim to loss of the exponent. |
| 9. Sharpness comparisons | Remain; the current locations for the order-one comparison and strong-duality wording are `05:309–311` and `05:432–433`. |

The small clarity/navigation suggestions remain. The introduction's optional internal-note deletion is now at `01:293–294`, and its appendix description is at `01:306–307`. No additional issue was found in the repaired passages. All citation integration remains with the literature owner.

The core significance is clear. The ordinary-module result controls arbitrary feasible finite-order functionals on overlapping bags through exactly consistent densities, with coefficient normalization and no additional bag-count factor. The private-degree-two results quantify how a large convex private block can be retained at low degree, and distinguish fixed-domain, general affine, and regular-multiplier accuracy. The sharp examples identify an obstruction that persists for actual local measures. The paper correctly treats gluing, dense kernel rates, partial-degree hierarchies, and rational SOS recovery as established methods, and does not claim a generic runtime or practical speedup. The dispatch illustration and explicit matrix-size comparison explain potential use without presenting an untested application as evidence.

The structure follows the result dependencies: definitions and tools; the common preordering kernel; the ordinary-module correction; separator sharpness; convex recourse and duality; multiplier regularity; constrained and labelled extensions; rational witnesses. The detailed degree accounting is necessary substance, and the repeated scope distinctions generally help the reader. No new generic disclaimer list or large proof relocation is needed.

## P1: Fix assumption and scope statements

### 1. The rational rate corollary needs rational supplied bag polynomials

**Location:** `sections/09-certificates.tex:271–272`, with the proof at `:298–299`.

The hypothesis requires only a rational global objective, but the proof says all local Chebyshev coefficients and budgets are rational. The setting permits real bag polynomials and treats the decomposition as data. Irrational bag terms can cancel in a rational global objective, leaving irrational local budgets. The rationalization theorem itself is unaffected; the rate corollary needs the intended data assumption.

Replace the opening with:

> Let every supplied bag polynomial $f_b$ have rational coefficients, let $\lambda\in\Q$, and let $\tau\in\Q_{>0}$. Choose either of the following cones and rational gap budgets:

This preserves the given decomposition and proves the claimed rational-budget property without an additional decomposition procedure.

### 2. Rational encoding bounds depend on input bit length as well as dimensions

**Locations:** `sections/00-abstract.tex:26–28`, `sections/01-introduction.tex:265–267`, `sections/09-certificates.tex:6–8` and `:294–295`, and `sections/10-discussion.tex:89–93`.

The abstract and discussion currently make encoding length polynomial in expanded SDP dimensions alone. The precise theorem at `09-certificates.tex:56–59` also depends on rational input length, including the slack, and on $\log^+(1/\tau)$. Fixed dimensions cannot bound coefficient bit lengths. The shorter introductory and corollary summaries should use the same qualification. Input length already includes the binary encoding of $\tau$ and therefore controls this logarithmic dependence.

For the abstract, replace the ending with:

> Extensions cover polynomial constraints under a global error bound, finite states with common continuous boxes, and exact rational box certificates with positive slack and encoding length polynomial in the expanded SDP dimensions and rational input length, including the slack.

Use this common wording in the other summaries:

> encoding length polynomial in the expanded SDP dimensions and rational input length, including the slack

Keep the existing distinction between a short witness, exact verification, and a method for finding a real witness. That distinction is clear throughout Section 9 and should not be weakened.

### 3. Name the cone in the merge/split exactness summary

**Locations:** `sections/01-introduction.tex:229–230` and `sections/10-discussion.tex:39–41`; supporting result `sections/06-recourse.tex:956–969`.

The introduction discusses both private-degree-two and total-degree sharpness immediately before the unqualified merge/split sentence. The cited remark supplies full-preordering certificates. In particular, the merged identity contains $y_1^2y_2$, which has private degree three if both variables remain private. That identity does not itself establish exactness of a merged private-degree-two formulation.

Introduction replacement:

> For full preorderings, merging the two bags, or splitting at the active-set change, makes the same instance exact at low order.

Discussion replacement:

> For the sharp inverse-order instance, merging bags or splitting the shared domain at zero gives low-order exact full-preordering certificates (\cref{rem:merge-split}).

No extra theorem is needed for this clarification.

## P2: Fix local mathematical explanations

### 4. State the paired separator functions directly

**Location:** `sections/05-sharpness.tex:16–18`.

The two fiber minima are $-\varphi$ and $\varphi$, so they differ by $2\varphi$, not by $\varphi$ as the current sentence says.

Replacement:

> Minimizing each bag over its private coordinate leaves the separator functions $-\varphi(y)$ and $\varphi(y)$, where $\varphi(y)=\max\{y,0\}^2$.

### 5. Do not assign an exact order to arbitrary certificate slack

**Location:** `sections/05-sharpness.tex:268–272`.

The argument proves a lower bound on any admissible $\epsilon$. An arbitrarily larger slack need not have order $r^{-2}$. Attribute the exact order to the necessary approximation width.

Replace the end of the sentence with:

> Thus $\epsilon\ge2E_{2r}(\varphi)=\Theta(r^{-2})$.

The established upper bound for the local-measure gap supports the displayed $\Theta$ statement. Using $\epsilon=\Omega(r^{-2})$ would also be correct, but less informative.

### 6. Justify why the order-one functional has no supported representing measure

**Location:** `sections/05-sharpness.tex:334–336`.

An atom outside the rectangle does not by itself exclude a different representing measure inside the rectangle. The intended conclusion is true, and a single moment inequality proves it.

Replacement:

> The atom $(1,\frac32)$ lies outside the rectangle. Moreover, $L_1(xy)=3/8>L_1(x)=1/4$, whereas $xy\le x$ on the rectangle. Thus $L_1$ is a feasible truncated functional with no representing measure on the bag's feasible set.

This strengthens the explanation of the finite-SDP versus exact local-measure distinction without adding machinery.

### 7. Source feasibility is a guarantee, not an exclusive location

**Locations:** `sections/06-recourse.tex:267–269` and `:593–596`.

The current wording says the private mean is feasible only at the source mean and not at the output. It can be feasible at both; the lemma guarantees source feasibility, while output feasibility can fail. Likewise, the distance estimate supplies a general inverse-order upper bound, not an exact repair cost for every model.

Replace `:267–269` with:

> Part (d) guarantees feasibility at the conditional mean $\bar x_b(u)$ of the input shared variables. In the affine case the private mean need not be feasible at the output $u$. Bounding the cost of repairing it there gives the general $O(r^{-1})$ term in \cref{thm:affine-recourse}.

Replace the opening of the affine subsection with:

> When the fibers move with $x$, the conditional private mean is guaranteed to be feasible at the conditional input mean $\bar x_b(u)$ of \cref{lem:conditional-matrix}(d), but need not be feasible at the output $u$. We repair it by Euclidean projection onto the output fiber and bound the cost using a Hoffman error bound.

The precise theorem, its sharp example, and the improved regularity estimates then establish the different rates separately.

### 8. The local/global error-bound example establishes loss of exponent

**Location:** `sections/08-extensions.tex:395–398`; related summary at `sections/10-discussion.tex:79–80`.

The example has local linear bounds and requires a smaller global exponent. It does not prove that no global Hölder bound can be obtained from local assumptions under any changed exponent or additional argument. Narrow the comparison to what the example establishes.

Replace the final sentence of the Section 8 remark with:

> \Cref{ex:global-local} shows that local error bounds need not preserve the global exponent, so these rates do not imply uniform improvement for all such domains.

In the discussion, replace “which may be weaker than the separate local geometric bounds” with:

> whose exponent may be smaller than those of separate local geometric bounds

### 9. Tighten the sharpness section's remaining comparisons

These are short precision changes, rather than changes to any result.

- **`05-sharpness.tex:10–12`:** Match the theorem's qualification of “every relaxation.” Suggested wording: “It therefore applies to every relaxation whose feasible set contains these integration functionals and whose only coupling between bags is agreement of these separator moments.”
- **`05-sharpness.tex:308–310`:** “Local positivity constraints cost more than separator truncation” can suggest a quantitative comparison of the extra gap with the separator gap. Say: “At order one, the finite SDP has a larger gap than the local-measure relaxation: $\rhopre_1<v_2$. At order two the entire gap is caused by separator truncation, even for the ordinary module.”
- **`05-sharpness.tex:430–431`:** Replace “nor SDP duality” with “nor strong SDP duality”; the proof explicitly uses weak duality at `:323`.

## Small clarity and navigation changes

These are optional except where desired for consistent final editing. They do not alter scope or proof substance.

- **`08-extensions.tex:28–30`:** State the available Lipschitz bound directly: “Let $L_f$ be a Euclidean Lipschitz constant of $f$ on the entire box; one may take $L_f=\Abud$, since $\abs{T_k'}\le k^2$.”
- **`10-discussion.tex:49–51`:** “Order exponent” is ambiguous between accuracy and matrix size. Use: “The exponent of $r$ in the recourse hierarchy's block sizes depends only on the number of shared variables; at fixed shared width, its SDP dimensions grow polynomially in the private dimension.”
- **`01-introduction.tex:305–306`:** Only one appendix is included. Replace “Long proofs are in the appendices” with “The appendix proves the failure result when private quadratic bounds are omitted.”
- **`01-introduction.tex:291–292`:** Delete “Priority for the candidate contributions above is qualified by the comparisons in each section.” The specific attribution qualifications are already stated; this sentence sounds like an internal drafting note and adds no substantive caveat.
- **`03-kernels.tex:100`:** Replace “the first inequality” with “the upper bound” in the damping estimate.
- **`04-ordinary.tex:484–486`:** Replace “the only coupling between bags is the common scalar $\Delta_w$” with “The positivity correction couples bags only through the common scalar $\Delta_w$.” The original hierarchy also couples bags through separator equalities.
- **`04-ordinary.tex:10–11`:** Replace “still grow with the number of bags” with “can still grow with the number of bags” for the absolute error through $\Cf$. The normalized theorem permits a fixed coefficient budget across a growing bag family.

## Claims that should be preserved

The earlier `front-root-r1.md` concerns are resolved in the current source: Archimedean convergence assumptions; upper approximation bounds versus exact orders; constraint activation versus corners; the coordinatewise Lipschitz restriction; globally SOS products versus interval tensor certificates; regime-dependent grid rates and lower bounds; and normalization by the coefficient budget. Do not reintroduce the original formulations.

The local-measure identity $2E_{2r}(h)$ is now limited to the paired models and supplies a lower bound on finite SDP gaps. The order-one versus order-two values make the distinction concrete. The regularity theorems explicitly require a univariate component $\phi_{bi}(u_i)$ in their coordinatewise branch, or weighted tensor summability in the other branch; the sufficient QP regime is restricted to scalar bags for its automatic inverse-square corollary. There is no unsupported multivariate Lipschitz theorem in this snapshot.

Box dual attainment, recourse equality of supremum values with strict-level certificates, constrained primal rounding, and labelled duality after pruning remain distinct. Fixed convex rounding is correctly one-sided. The finite-state extension states its empty-bag and zero-width conventions, common boxes, and label-size costs. Appendix B's prose and dependence on the hierarchy tests are clear.

The supplied preliminary literature evidence supports the stated attribution boundaries. This review did not verify primary sources, priority, bibliographic metadata, or source locators. Those remain with the literature owner and root's final integration. The manuscript's specific prior-work comparisons should be checked against that final evidence, without inventing a stronger negative literature claim.

## Snapshot and actual checks

Reviewed source scope: `main.tex`, `macros.tex`, all Sections `00`–`10`, and `appendices/B-recourse.tex`. The whole source was covered by the lead review and independent assigned full-line reads. Context read: repository `AGENTS.md`, `evidence/BRIEF.md`, `evidence/LITERATURE-PRELIMINARY.md`, `evidence/reviews/front-root-r1.md`, and `evidence/WRITER-FRONT-R2.md`.

Read-only commands actually run included targeted `rg --files`, `cat`, `nl -ba`, `sed -n`, a Python extraction of theorem/corollary statements and section headings, `sha256sum`, `pdfinfo`, and `pdftotext -f 1 -l 5 -layout build/main.pdf -`. No experiment, solve, checker rerun, TeX build, CI check, or project-wide verification was run. The PDF inspection was text-only, not a final layout review.

The existing PDF has 71 pages and unresolved citations. Its abstract is an older long version, so it is stale relative to the reviewed `00-abstract.tex`. Source is authoritative for this review. Root's planned final rebuild is necessary before any PDF readiness claim.

SHA-256 snapshot (paths relative to `paper-sparse-sos/`):

```text
206dd022e955dc7981b3e400cce0d05060c5181dd10b73c8e93eb864888331df  main.tex
00b454c4dcc72727d78c77817d3cab911a3d7f2205efd4af467a9407e27c04bb  macros.tex
c5818b22fd00210470838f9e8f119e09daeff4d2df1cb516c6cc3a3654784f79  sections/00-abstract.tex
11d457039c8bfe203a03106cd404a010989259897b6d8982e07fd2a43d3c77d8  sections/01-introduction.tex
6db76f3db9195300a335e61feba66c387692e4e40dc59951fb2b50b020e8936b  sections/02-setting.tex
aa99f3f741b7fd0d61d4bd395b4a4f236589952d1c721645aac6985f7f1c8a2a  sections/03-kernels.tex
c259609d74d3ef5520d2bf1773eb363391c119ec2df0202abf278aa0191556e4  sections/04-ordinary.tex
92835b3988400ec22a363886b66abe8663cd9ca341d1f97d3b5f545e033588f9  sections/05-sharpness.tex
b8b88edc1f966255db50470c754ff123b43dab7aeb7a54d1c62656a083c31ba6  sections/06-recourse.tex
67ae728c7d2e982eddd1b8c68b26b85ee6658b50a890215071328bb4b46a9510  sections/07-regularity.tex
652761da6e0453aa04465ec823a75711b59caad3e296e42b456485c22a205f07  sections/08-extensions.tex
56351e2a33ed14724eabc185fa1e2536a54b9dd3b2d05be1eb3952709458f384  sections/09-certificates.tex
4cbcc0716204ffc2375a37d467c4577bf35dbb8f0c7bf2a09c9026fe12413137  sections/10-discussion.tex
4c2250b5d513be3f2f0dc8f9019abc05dc1fa27c9cecf55d6586266c9625240f  appendices/B-recourse.tex
bad891c64f96e4258c68a2ac7cb7c6cbc913ed2a28784945a4eacdf805db6191  build/main.pdf
```

The follow-up re-read used targeted `nl -ba`/`sed -n` reads and `sha256sum` on the five changed sections. A focused Python check confirmed that this review file exists, ends with a newline, and has no trailing whitespace. That document check is not a manuscript or mathematical verification. Follow-up hashes:

```text
62d688f2d5b10d9e69c1cc6df5155c62f3d14db79c25c7864bbf55347eae5aee  sections/00-abstract.tex
51384bd368b9ab33f4d8b2da423b1faa5c98be6fbffc97c3ed48b0d1d3e364d5  sections/01-introduction.tex
d9e05f07c613115c042ba16121fdd371609c996c4720d37870418cef5a3706a3  sections/05-sharpness.tex
8d3819602848dc43441ae99e090f60ee4f46e703de8a86560544e96966b582a2  sections/09-certificates.tex
db5d120d53ea703679191cfa8ada8b43513fedd0827157bfad9434526e037dcb  sections/10-discussion.tex
```

## Final repair verification: ACCEPT

On 2026-10-06 UTC, I narrowly re-read the repaired passages without reopening unchanged mathematics or adding new review topics.

| Remaining finding | Verified final disposition |
| --- | --- |
| 2. Rational encoding summaries | Resolved at `09:6–8` and `09:296–297`; both include expanded dimensions, rational input length, and slack. The previously verified front/discussion qualifications remain. |
| 7. Source feasibility and repair rate | Resolved at `01:220–224`, `06:267–270`, and `06:594–598`. Feasibility is guaranteed at the source; output feasibility can fail. The cost statement is the general inverse-order upper-bound term. |
| 8. Global versus local exponent | Resolved at `08:396–398` and `10:79–80`; the comparison concerns loss of exponent rather than impossibility of any global bound. |
| 9. Sharpness comparisons | Resolved at `05:10–12`, `05:310–312`, and `05:433–434`. The integration-functional qualification, finite-SDP/local-measure comparison, and strong-duality wording are precise. |
| Small clarity/navigation suggestions | All resolved: the explicit Lipschitz constant (`08:28–30`); the matrix-size exponent (`10:49–51`); the single-appendix description (`01:304–305`); deletion of the internal priority sentence; the damping upper-bound reference (`03:100`); positivity-correction scope (`04:483–486`); and possible coefficient-budget growth (`04:10–11`). |

Findings 1, 3, 4, 5, and 6 had already been verified as resolved in the preceding follow-up. All prose findings are now closed. The repairs preserve the necessary caveats and make the theorem summaries more exact. The journal-level argument, contribution framing, and reader navigation receive **ACCEPT** for this editorial scope. Citation finalization remains with the literature owner, and no final typeset-PDF acceptance is asserted here.

Actual final verification consisted only of targeted `nl -ba`/`sed -n` reads of the reported locations and `sha256sum` of the section files. No experiments, numerical solves, TeX builds, CI checks, or manuscript edits were performed by this reviewer.

Final source hashes for Sections 00–10 (relative to `paper-sparse-sos/`):

```text
62d688f2d5b10d9e69c1cc6df5155c62f3d14db79c25c7864bbf55347eae5aee  sections/00-abstract.tex
63f4a03303e23b1ddd539f6bdfb38f0a8cb0aaa8f95fcaeebbcddf1fd9e6c873  sections/01-introduction.tex
6db76f3db9195300a335e61feba66c387692e4e40dc59951fb2b50b020e8936b  sections/02-setting.tex
2033e33774a7ad029bbfe0303d932ab554b43dd6953b3a7f6adb91da2bcf9f5e  sections/03-kernels.tex
94e988857c6476493c3fc7b92403252baa610ce53d624a11e1fc8603a2593cc2  sections/04-ordinary.tex
9f6e5df9f447297fce0fedca96b80a5e438464178f190742da84165e106eae63  sections/05-sharpness.tex
005dda97977a5edc4a09e1e6dad979b3fd04fecc85cbbe88842ee0639924ea02  sections/06-recourse.tex
67ae728c7d2e982eddd1b8c68b26b85ee6658b50a890215071328bb4b46a9510  sections/07-regularity.tex
f3977f81a98142998586de633ec59ec9d692386dc7cd8f7422a4e1c4f42fc7dd  sections/08-extensions.tex
9a351a105ae08e17299bd10532b4032e120ebbc116f7dc320d8abc40930c1f2b  sections/09-certificates.tex
5082043d00376df50e12faeaf3a510f394074c0773ef997556daf3615ad2e69b  sections/10-discussion.tex
```
