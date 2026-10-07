# Final recourse and integer author response

Date: 2026-10-05. Author: Sol, continuing the interrupted Opus revision after
the authorized provider fallback. Scope: `sections/07-recourse.tex`,
`sections/08-integer.tex`, `appendices/E-recourse.tex`,
`appendices/F-integer.tex`, and this report only.

The four live files now incorporate the actionable recourse and integer
findings. The constant-base solver's reviewed algebra is retained. The
remaining work is integration and independent review of the complete
manuscript, including the foundations-owned fallback proof and the
literature-owned bibliography and exact source contracts. This author
response is not an independent approval of the final manuscript.

I read the brief, notation and inventory, both live integration records,
the original recourse author report, the prewriting and early recourse and
integer reviews, the complete frozen recourse review, the editorial interim
review and disposition, the complete accepted lattice supplement, the
preliminary literature account, both typesetting records, and the newly
materialized `opus-math-partial-r1.md`. That last record supplies no final
verdict or additional location-specific actionable findings.

## Response to the mathematical and interface findings

Locations below are in the final live files at the hashes recorded below.
Some corrections were already in the interrupted live revision; I checked
and preserved them rather than rewriting the reviewed proofs.

| Finding | Final location and response |
| --- | --- |
| K1 / I1: common-root value | Section 8:64–94, `thm:int:solver`, and Appendix F:259–277, `lem:int:values`, return `r_f=f(r_1,...,r_k) mod P` at the stored root. The separate value polynomial and isolator are auxiliary comparison data. The native, flow, TU and component outputs inherit this contract. |
| K2 / I2: deformation at zero | Section 8:96–104 states the pure-power leading monomials for normalized symbolic or finite `z`, hence for symbolic or nonzero epsilon. Epsilon zero is a limit, not that specialization. Appendix F's normalized quotient proof is unchanged. |
| K3 / I3: pole projections and compactness | Section 8:104–125 qualifies the finite-limit factorization by a form that exposes every pole and separates finite limits. Degree and divisibility screening precede reconstruction; box feasibility filters every candidate. Appendix F:246–256 expressly permits a bad form's bounded pole projection and filters it. Correctness uses a convergent subsequence of deformed minimizers. |
| K4 / I4: affine empty zero sets | Section 8:498–508 and Appendix F:867–888 split the nonempty-zero-set distance bound from the empty-set vertex bound `2^{-(q+1)H_0}`. Nonzero constants and vertex faces use the second branch. Identically zero charts pass non-strict tests and are excluded from the exceptional family. |
| K5 / I5: TU input contract | Section 8:514–541 expressly supplies expanded fixed-degree rational costs, the unit core box, positive rational curvature and noise, fixed nonempty integral TU feasibility, and counted certificates. The inequality corollary inherits these premises. Appendix F retains the bounded symbolic dual basis and conformal-circuit transfer. |
| K6 / I6: marginal bit lengths | Section 8:267–291 separates real optimality from rational polynomial-height marginals. Appendix F:534–555 now scopes shortest-path bit lengths to rational marginals of height `H_m`. It does not claim a polynomial bound for repeated unit augmentation. |
| K7 / I7: joint point and value refinement | Section 8:588–634 and Appendix F:1000–1015 allocate `q+ceil(log2(n+1))` bits separately to each component's point distance, value width and certified gap. Euclidean point errors combine by a square-root bound; widths and gaps add. No distance conclusion is inferred from a gap. Section 8:370–386 explicitly gives interior-flow refinement `c_d^k poly_d(I+q)`. Appendix F:316–327 already supplies the solver's Euclidean allowance and separate gap certificate. |
| K8: certified empty core | Section 7:194–224 uses `eta_j=4^{-j}` and `epsilon_j=E_j+eta_j` when `k=0`, while `E_j=0` remains the rounding error. Appendix E:145–196 proves the search with this positive allowance; E:357–375 propagates it through incumbent localization and the base cutoff. |
| K9 / I8: empty restrictions and direct branches | Section 8:195–206 gives impossible tightened bounds and an empty restriction list value positive infinity before oracle calls. Appendix F:402 now handles a singleton residual set before applying Lipschitz bounds to its complement. Section 8:571–578 returns an all-fixed constant before maxima; Section 8:682–695 and F:1044–1045 solve `k=0` directly. No maximum over an empty row set is used. |
| K10: generic fallback format | Section 7's table and polynomial theorem, and Appendix E:61–74, now use the common-root coordinate-and-value format of `thm:count:fallback`. E explicitly includes the Euclidean coordinate precision allowance. The tensor conversion and its base-only work factor are owned by the foundations author; local recourse text assumes that integrated theorem, not separate scalar isolators. |
| N1: flow nonemptiness | Section 8:305–319 explicitly inherits the nonempty core–recourse model and performs one integral feasibility LP before sampling. Thus the interior premise cannot promise an optimizer on an empty network. TU nonemptiness is explicit as well. |
| N2: parallel-arc and loop cycles | Appendix F:543–555 proves necessity for every simple residual cycle using at most one copy of each original arc, including distinct-arc two-cycles and loops. Only the forward/backward pair of one original arc uses the separate convexity argument. |
| Root early item 2: rational quadratic fallback | Section 7's summary caption and `thm:rec:qp` say rational output on every draw, including fallback. |
| Root early item 3: certificates and input length | Section 7:87–100 counts a curvature certificate's encoding in `I` and charges checking work to runtime. Section 8 carries the same convention to TU costs. |
| Root early item 4: SOS convexity | Section 7:419–430 describes an SOS certificate for `y^T H_RR(x)y`, with rational Gram matrices and exact identity/PSD verification. An SOS objective itself is expressly insufficient. The structural even-affine-power certificate is retained. |
| Root early item 5: general `k=0` oracle | Section 7:469–477 says the general certified oracle need not arise from a convex residual objective. Convexity is the sufficient specialization of `lem:rec:convex-oracle`. |
| X16: deterministic flow-core baseline | Section 8:324–353, `cor:int:grid`, states error `kL/(8m^2)` plus the separately scoped oracle allowance `eta`, on a fixed residual set. Appendix F:559–573 now supplies its missing proof. No residual coordinate is rounded. |
| Accepted fixed-degree lattice extension | Section 8:652–739 and Appendix F:1018–1130 cover explicit rational-knot continuous globally convex piecewise-polynomial unaries of fixed degree. The scalar oracle evaluates both applicable pieces across a unit step. The theorem allows arbitrary `T`, zero/dependent/constant rows, singleton intervals and `k=0`. Expanded denominators define `Q_den`, `D_0=2 Q_den^3`, and `M>=max(2,k alpha s^2 D_0)`. F proves the original lattice, exact every-draw termination without fallback, polynomial-height evaluations, and an input exponent independent of `k`. Stale `Q_0` references are removed. |
| Universal resolution and precision regimes | Sections 7:729–735 and 8:755–769 cite `cor:count:universal-law`. Polynomial-bit routes retain their numerical factors; nonlinear boundary flow/TU keeps the supplied `k<=K` qualification. The lattice cap is reset to `log2 M` if a larger common resolution is chosen. Section 8:632–648 preserves the nonmonotonicity of the actual strong-field `q_i(M)` and requires recomputing beta. |

## Response to the editorial findings

| Finding | Final response |
| --- | --- |
| P1: companion overlap and degree three | Section 7 opens with the conditional-oracle mechanism, with distinct wording. At 514–527 it credits the exact-arithmetic companion's full selected-point and value evaluator for residual-convex cubics on product boxes without a modulus or convexifier, including its selector and `k^{O(k)}(1+L/sigma)^k poly(I+q)` bound. It credits the companion's noisy-core quartic obstruction reproduced in `thm:lim:posslp(c)`. The scope at 735–742 distinguishes this obstruction from the cubic positive result and says the modulus is sufficient for the present closure, not necessary for every point evaluator. |
| P1: supplied convexifier comparison | Section 7:556–574 gives the Schur convexifier and the explicit Hessian `[[L,T],[T,mu]]`, which needs core correction at least `max(0,T^2/mu-L)`, while the direct count keeps `L/sigma`. It states the companion's supplied-convexifier point theorem at its actual scope: cubics convexified on the feasible polytope, or fixed degree convexified on all of real space. Exact source locators remain with Luna. |
| P4: numerical parameters | Section 7's opening and scope retain `k` together with `L/sigma`. Section 8 keeps the full displayed numerical factors, and its listed-label baseline says polynomial enumeration only for fixed `k`. The original-objective accuracy discussion keeps the qualification on numerical curvature. |
| P5: applications and noise | Section 7's opening permits first-stage dependence in residual costs only, and excludes core-dependent right-hand sides and bounds. Section 8:571–575 says the previous routes allow arbitrary positive noise width and distinguishes the strong-field lower-scale condition. The strong-field scale is described using its derivative variation, graph degree, label count and effective `c_d`; no practical-performance verdict is inferred. |

The algebraic tool list in Appendix E now requires positive quantifier
block sizes and at least one free variable, uses a positive format base,
and handles singleton domains directly. Appendix F's univariate tool
summary includes requested refinement bits in intermediate bit lengths.
These are statement clarifications; the reviewed critical-limit algebra,
weak-multiplier Schur argument, all-tied-flow certificate and TU basis
construction were not replaced.

## Targeted verification actually run

1. Scoped reads and searches of the four live files and their declared
   contracts, followed by analytical checks of the repaired branches,
   deterministic grid proof, lattice denominators and bit costs, and joint
   component accuracy allocation.
2. An inline `python3 -` source check restricted its validation to these
   four files. It checked final newlines, trailing whitespace and control
   characters, paired math delimiters, nested environments, duplicate local
   labels, unfinished markers, and removal of stale `Q_0`. For cross-reference
   validation it collected labels from the live scientific TeX sources and
   checked only references used by the assigned four files. Result: pass,
   with 40, 31, 24 and 28 labels respectively. A subsequent small prose
   refinement did not change labels, delimiters or environments.
3. A four-file scratch document in
   `/tmp/smoothed-recourse-sol-f7g73xxx` loaded the manuscript preamble and
   macros and only Sections 7/8 and Appendices E/F. Two initial passes and
   one final pass after the last scientific edits ran
   `pdflatex -interaction=nonstopmode -halt-on-error recourse-check.tex`.
   All passed. The final PDF has 48 pages, no fatal error and zero overfull
   boxes. The earlier long E/F equations were split without shrinking
   mathematics or removing terms. Other chapters' cross-references and
   bibliography entries are intentionally absent from this scratch build.
4. `git diff --check -- paper-smoothed-global/sections/07-recourse.tex
   paper-smoothed-global/sections/08-integer.tex
   paper-smoothed-global/appendices/E-recourse.tex
   paper-smoothed-global/appendices/F-integer.tex` passed.
5. A final inline `python3 -` checked this report's whitespace and control
   characters, matched all four recorded source hashes, and rechecked the
   four files' whitespace, environments and denominator spelling. All
   checks passed.

These are targeted author checks, not CI checks or project-wide
verification. No CI status or log was inspected. No experiment or saved
proof diagnostic was rerun. No literature search, historical edit, other
author's file edit, commit, publication or delegation was performed.

## Remaining source and integration dependencies

The literature owner must complete exact bibliography identities and
source contracts for the classical algebraic and oracle tools and the
companion comparisons. The Basu–Lerario key in these files now follows the
checked preliminary source, `basu2021-hausdorff-approximations-and-volume-of`,
rather than the unread journal package. I did not independently research
its theorem locator or the book/oracle locators. The scratch build omits
the bibliography and cannot establish final citation resolution.

The complete independent frozen review verifies the intended 46 results
subject to its named repairs; it does not certify these later live edits.
The partial Opus math record supplies no final acceptance. An independent
review of the integrated revision is still required. The foundations
author owns the generic shared-root fallback and universal-law corollary;
the final integrated check must confirm those interfaces and their budgets.
No unresolved mathematical blocker was found within this author scope.

Final source hashes:

| File | SHA-256 |
| --- | --- |
| `sections/07-recourse.tex` | `6dbb5f51199e261d613afbe67a88b4bd9f8f43dfc3c2fd6bb34a22243f659c6b` |
| `sections/08-integer.tex` | `27809e4472aa7e53c36e8a211bf91d348f5e25c651d74f75936e9d5df7e3f573` |
| `appendices/E-recourse.tex` | `e3bba43cbcfa9cfd373661b350711c3f890ebb73a9994dc6dfc13fae49676e1f` |
| `appendices/F-integer.tex` | `c561d9401b3cc15e9072ab7bffe843f6205a894886fba219a8ee02150a472ef0` |
