# Final shared-tools and quadratic author report

Date: 2026-10-05. Author: Sol, completing the interrupted Opus revision
after the reported Claude limit. Scientific ownership is limited to
`sections/03-counting.tex`, `sections/04-quadratic.tex`,
`appendices/A-finite-noise.tex`, and `appendices/B-quadratic.tex`.
Only those files and this report were edited. The mathematical revisions
are complete in the live sources. This is an author handoff, not independent
review approval or a submission-ready judgment on the whole paper.

The manuscript brief, notation, complete live integration contract and
decisions, original quadratic report, root counting and integration-scope
reviews, early foundations and quadratic reviews, low-rank and two-inertia
prewriting reviews, and complete accepted shared-root and universal-law
developments were read. The partial Opus mathematical review was also read;
it supplies no final verdict and was not treated as approval. The source map
in `quadratic-r1.md` remains applicable except for the output-format request,
which is superseded by the actual shared-root construction below. No change
to the model's common-root coordinate/value contract was requested.

The response table gives final source locations; line numbers identify this
handoff version.

| Required change | Final statement and proof | Resolution |
| --- | --- | --- |
| Shared root for optimizer coordinates and value | `thm:count:fallback`, `sections/03-counting.tex:539`; `lem:count:shared-root`, `appendices/A-finite-noise.tex:439`; application at `A-finite-noise.tex:632` | Squarefree scalar factors, tensor-companion multiplication matrices, an integer moment-form search, gcd separation test, independent coefficient-direction derivatives, modular coordinate maps, and quantitative canonical tuple selection are all written out. Native integer coordinates are extracted and listed. |
| Base-only degree versus added-bit height | `thm:count:fallback`; scalar recovery and conversion in Appendix A | Scalar degrees have a base-only exponential envelope. Their product remains base-only exponential. Absolute polynomial conversion bounds give `B poly_d(I+b+q)` without a dimension-dependent power of `b` or `q`. The enlarged `B` includes conversion before thresholds or law selection. The QE bit exponent is `e_d`, not the component-solver base `c_d`. |
| Canonical objective-value compatibility | `thm:count:fallback`; `A-finite-noise.tex:632` | The scalar formulas select the same lexicographically least optimizer and its value. The value equality is asserted and can be sign-checked at the selected root only; no false congruence over all Cartesian roots is asserted. |
| Euclidean evaluation and feasible mixed-box approximation | `thm:count:fallback`(ii),(iii); `A-finite-noise.tex:656` | Coordinate refinement includes the dimension allowance. Shared-root maps give Euclidean point error and scalar value enclosure. Mixed-box clipping retains integer labels and adds a derivative/value gap certificate. Arbitrary-domain rational feasibility is not claimed. |
| Universal finite sampling budgets | `cor:count:universal-law`, `03-counting.tex:664`; `app:count:universal`, `A-finite-noise.tex:675` | Complete grid, Gaussian fixed-point, and supplied-parameter proofs; route verification follows. Same scalar families, scales, perturbation coordinates, output types, numerical factors, and oracle costs are retained. A finite collection can share an enlarged envelope with fixed formats/cost models. |
| Gaussian support/precision loop | `cor:count:universal-law`(b); Appendix A proof; `app:qp:main`, `B-quadratic.tex:639` | `H=A+D+21`, `t=ceil(4 log_2 H)`, `b=A+Dt` satisfy `b+20 <= 2^t <= 2H^4`. Integer comparisons compute `t`. Search boxes and caps are computed together for that support before sampling. |
| Nonlinear boundary flow/TU qualification | `cor:count:universal-law`(c); final paragraphs of Appendix A | A supplied `K >= k` gives a common `M(I,K)` with an explicit effective factor depending on `K`. Taking `K=I` need not preserve the bound for small actual `k`; no impossibility theorem is inferred. Interior and bilinear cases retain polynomial precision. |
| Strong-field and generic-domain qualifications | Universal-law discussion and Appendix A | Recompute actual `q_i(M), beta(M)`: endpoint grids are not nested, so these factors are not monotone. The sufficient strong-noise regime persists under larger `M`. The iterated-squaring compact-domain example prevents inferring polynomial geometric budgets from degree/format alone. |
| Finite-law motivation and singleton cases | `sec:count:laws`, `def:count:laws` at `03-counting.tex:284`; `lem:count:rare-fallback` at `03-counting.tex:471`; Appendix A | Countably supported rational laws are Turing-samplable. Our prescribed worst-case random-bit bound forces finite support. Singleton boxes are evaluated before width maxima, meshes, or thresholds; `S>0` is explicit in the dividing budget. Empty variable blocks are handled directly rather than by the stated QE theorem. |
| Renegar and sampler boundaries | `thm:count:renegar`, `A-finite-noise.tex:331`; sampler proof at `A-finite-noise.tex:167` | Quantifier block sizes are positive, the free-variable count is positive, and small logarithms are replaced by positive conventions. Exact Taylor intermediates have polynomial length; only rounded weights and atoms are claimed to have `O(b)` bits. |
| Nonempty mixed feasible set and rational factor data | `def:qp:instance`, `04-quadratic.tex:34`; `def:qp:factor`, `04-quadratic.tex:85`; `app:qp:main` | `X` is explicitly nonempty. If not promised, a zero-objective convex feasibility solve returns infeasibility before budgets or sampling. The supplied frame constant is rational and included in the input length. The smallest-face rational-output statement is qualified by nonemptiness. |
| Least sufficient Gaussian accuracy in the two-direction theorem | `thm:qp:two`, `04-quadratic.tex:261`; proof at `B-quadratic.tex:282` | Choose the least sufficient positive `b`. Larger common resolutions are allowed only with polynomially bounded bit length and with that bit cost charged. Uniform and Gaussian sampled-height statements are distinguished. The `S=0` branch precedes growth and mesh calculations. |
| Capped inverse-growth lower limit | `rem:qp:moments`, `04-quadratic.tex:299` | Lower limit is `max{1,a_0^(k/2)}`; the inequality requires `B` above that limit. The asymptotic claim fixes positive `a_0` and takes sufficiently large `B`. The claim remains a limitation of integrating a bound, not an algorithmic lower bound. |
| Guarded full-model conditioned recovery | `thm:qp:conditioned`, `04-quadratic.tex:195`; proof at `B-quadratic.tex:191` | Coordinate reconstruction is attempted only after successful value reconstruction. Singleton auxiliary coordinates are removed only from the mesh; their fixed values, every factor row, and the full PSD inner matrix are retained. Every retained cell has a near-optimal corner in the growth ball; entire cells require a diameter enlargement. The existing `c_k` packing contract is retained. |
| Deterministic mixed conditioned extension | `cor:qp:conditioned-mixed`, `04-quadratic.tex:228`; proof at `B-quadratic.tex:262` | Same growth transfer, denominator bounds, reconstruction guards, and polishing, with the exact convex-MIQP factor `f(n_z)` and absolute polynomial exponents. Auxiliary ranges are LP ranges over the relaxation. This is a deterministic extension, not a new smoothing theorem. |
| Affine-family concavity and real critical-region coverage | `lem:qp:pieces`, `04-quadratic.tex:362`; proof at `B-quadratic.tex:318`; auxiliary proof in Appendix B | An infimum over a compact affine family is concave; the family need not be finite. Region membership is at the queried residual parameter. Every feasible fixed label has regions covering all real parameter pairs, as needed during finite/continuous product replacement. |
| Support-independent mixed-gap constants and numerical FPT parameters | `lem:qp:gap`, `04-quadratic.tex:423`; sampling at `B-quadratic.tex:664`; `tab:qp:regimes`, `04-quadratic.tex:901` | Terminal mixed schedules enforce `h_J<=1`; existing constants and the sharper `J(t)<=J(0)+t` bound remain valid. Summary parameters include the numerical ratios. The `nu` table entry is explicitly intrinsic normalization; supplied-factor bounds retain `alpha,c_fr`. |

The prior source-development map gains two accepted elementary developments:
`fallback-shared-root-sol.md` maps to `lem:count:shared-root` and the
strengthened `thm:count:fallback`, and `universal-law-budget-sol.md` maps to
`cor:count:universal-law` and `app:count:universal`. The deterministic
mixed conditioned corollary covers inventory A0's supported extension.
All existing public theorem/reference aliases in the four assigned files
were retained. No macro addition is needed.

Targeted local checks actually run:

- Scoped `cat`, `sed`, `rg --files`, `rg -n`, and `nl -ba` reads of the
  assigned sources, their contracts and requested evidence, the model/main
  preamble, and relevant live route schedules. These were investigation,
  not project-wide verification.
- An inline `python3` format check of the four assigned TeX files checked
  final newlines, trailing whitespace, environment nesting, display and
  inline math delimiters, absence of the alternate uniform-law notation,
  and uniqueness of the 84 assigned-file labels. It passed.
- A scratch document containing only the four assigned TeX files, with the
  current manuscript preamble/macros, was built using
  `pdflatex -interaction=nonstopmode -halt-on-error -file-line-error
  -output-directory=/tmp/minlp-quadratic-sol-check
  /tmp/minlp-quadratic-sol-check/check.tex`. Initial and resolving passes
  succeeded. An initial 0.66534 pt overfull Renegar line was corrected by
  displaying its quantified formula. The final pass has 44 pages, no TeX
  errors, and no overfull boxes. Expected external-reference/citation
  warnings remain in this deliberately four-file scratch document.
- The bibliography subset comparison was a local key check, not literature
  research. At its first run, root `references.bib` did not exist; the
  adjusted subset check therefore did not attempt to certify that file.

The new arguments and boundary repairs were checked analytically against the
complete accepted developments. No optimization experiment or old proof
diagnostic was rerun. No project-wide check, CI status, or CI log was inspected;
no work was delegated, committed, sent externally, or published. Final
independent review and the root's complete bibliography/layout integration
remain separate required work.

Citation/source requests for the Luna literature owner and root follow.
No new source identity was researched by this author. The supplied
preliminary verified subset supports the retained keys for Beier--Vocking,
Roglin--Vocking, Bemporad et al., Tondel et al., Del Pia's convex-MIQP and
rational-Jacobi results. The qualitative genericity comparison now uses the
verified key `lee2017-generic-properties-for-semialgebraic-programs` rather
than the provisional Lee 2016/Azagra paragraph. The following inherited
citations are not certified by that preliminary subset and need the final
source audit; their presence is not a claim that this author verified them.

| Key needing final verification | Required source scope or locator |
| --- | --- |
| `renegar1992-on-the-computational-complexity-and` | Correct part of the three-paper series and Theorem 1.1 locator for the displayed block-sensitive format, coefficient-height and work bounds, including fixed admissible constants. |
| `basu2006-algorithms-in-real-algebraic-geometry` | Polynomial degree/height bit bounds for squarefree/gcd arithmetic, real-root isolation, separation, sign determination and refinement; the shared-root proof uses these classical univariate operations. |
| `mehlhorn2015-from-approximate-factorization-to-root` | Correct identity and root-isolation/refinement scope. Confirm which claimed separation/refinement facts the read source supports, or narrow the citations. |
| `kozlov1980-the-polynomial-solvability-of-convex` | Exact rational convex-QP optimizer/value and polynomial bit work, including singular Hessians and lower-dimensional rational feasible sets. |
| `grotschel1988-geometric-algorithms-and-combinatorial-optimization` | Exact rational LP/vertex extraction and polynomial continued-fraction reconstruction within an interval under a denominator bound. |
| `evans2015-measure-theory-and-fine` | Rademacher and the Lipschitz area formula used in the global-growth proof. |
| `federer1969-geometric-measure-theory` | Exact area-formula locator or an adequate verified substitute. |
| `rockafellar1970-convex-analysis` | Almost-everywhere differentiability of finite convex functions, and the proximal/subgradient facts used in Appendix A. |
| `fulton1998-intersection-theory` | Refined Bezout/nonsingular isolated root count used through `lem:sp:bezout`. |
| `ding1996-a-parametric-solution-for-local` | The thesis's stated indefinite-QP parametric-convex-value reduction and optimizer recovery. |
| `patrinos2011-convex-parametric-piecewise-quadratic-optimization` | Correct identity and scope for convex parametric piecewise-quadratic machinery; do not attribute the draft's degenerate extraction or expected-work theorem to it. |

The verified Del Pia convex-MIQP key also needs the exact final Theorem 3
locator attached to the attained rational optimizer/value and absolute
input-polynomial exponent used by `prop:qp:primitives`. Literature ownership
remains exclusively with Luna. The mathematical common-root and universal-law
repairs have no unresolved new mathematical dependency beyond these stated
classical algorithms and the existing route contracts.
