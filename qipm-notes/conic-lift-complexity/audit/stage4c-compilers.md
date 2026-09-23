# Stage 4C exact-compiler author audit

Owned deliverables: `sections/10d-exact-compilers.tex` and this audit. No edits to main, bibliography, earlier sections, workbench sources, or literature packages. The section is frozen for the parent author after the final check recorded below. This is author verification, not a formal independent review.

## Source coverage and disposition

All of `audit/root-stage4-preparation.md` and the following three complete workbench notes were read.

### `2026-09-04-cone-meet-compilers.md`

- Exact one-translate compression iff vector lattice iff simplicial: Proposition `prop:cone-meet`, including the retained-input-apex condition and dimension-one conclusion. Added a direct extreme-ray/Riesz-decomposition proof, so the paper does not depend on an unexplained classification citation. Closedness, pointedness, spanning, and finite dimension remain explicit.
- Rank versus poset width: explicit coordinate minima `eq:simplicial-compiler` and incomparable-input explanation.
- Query acquisition: `eq:meet-queries` retains the upper, lower, and randomized bounds with precise scalar-entry access and explicit simultaneous classical output. Corrected the source's literal Theta quantum assertion to an O(d sqrt(N) log(d+1)) upper versus Omega(d sqrt(N)) lower. Individual minimum finding plus error amplification alone proves only this stated upper. For the minimum *value* lower bound, use zero-or-one hidden zero, not the always-one-mark promise whose minimum value would be constant. Citation ACGT Theorem 4 supplies the proper direct sum.
- Canonical barrier parameter Nd versus d and exact radial metric length: retained with the selected-barrier qualification.
- Dense inverse transform access caveat: retained. The O(d^2) arithmetic to multiply Tm is elementary and omitted as routine arithmetic, not a mathematical conclusion needed for the theorem.
- Product radial extension: equation `eq:radial-product-compiler`, barriers, and query count with B in place of d. Covers power/exponential/relative-entropy and other proper factors without listing each family.
- N indispensable Lorentz translates: Proposition `prop:lorentz-translate-arcs`, with proof of positive alternative disk radii, the finite circle-intersection argument, rank-two observation, and path-consensus block graph. Exact scope explicitly excludes auxiliary-variable or altered-map lower bounds.
- Prior-art boundary: classical vector-lattice theorem attributed to Yudin via primary Nemeth 2004, while the compiler interpretation is explained without an unsupported priority assertion.

### `2026-09-04-dilation-rank-perspective-compilers.md`

- Exact R-dimensional moment upper and continuous-encoder lower: Theorem `thm:dilation-summary`. Positive coefficients vary on an open orthant; decoder continuity is not assumed. Fixed restricted families are distinguished. Added continuity of coefficient maps by an invertible evaluation matrix.
- Classification: Proposition `prop:dilation-classification`, credited to Anselone–Korevaar/Engert, with an elementary continuous one-parameter matrix-group proof. Added the exact rank sum(degree+1) and the zero-function/empty-sum case; no new classification priority claim. Examples -log, powers, and exp retained.
- Two-moment Umegaki compiler: `eq:qre-moments`–`eq:qre-compiler`, noncommuting inputs, PSD support closure, normalized-weight geometric mean, fixed weights/scales, and summed-output-only scope all retained.
- Corrected unnormalized divergence: developed the exact additional term `(C-D_eff) tr Y`, with `C=sum w_i d_i`, rather than only warning that a correction exists.
- Source acquisition: bounded uniform-average coherent mean estimation and randomized upper bounds, exact/near-exact Hamming-weight lower, and one-sided epigraph safety retained. General implicit weights explicitly not free. No optimality claim for the elementary randomized upper in every input promise.
- Barrier versus access: the source's symmetric KL unique-search example is replaced by a simpler one-sided KL family `sum_i D(x1 || exp(-z_i) x2)`. It has the same constant log(2) oracle-value separation and source lower bounds, but its three-parameter barrier is transparently an invertible linear pullback of one scalar relative-entropy cone. This resolves the need to prove a general sum-of-symmetric-KL compatibility assertion. No distinctive stronger conclusion is lost: both examples establish constant barrier parameter versus uncompiled source access. The paper states that the bound disappears after acquiring the summary.
- Barrier citations: FS2023 and existing `HeSaundersonFawzi2026`. The parameter 2n+1 is prior work; the scaling identity is called elementary, and no new barrier claim is made.

### `2026-09-04-arbitrary-exponential-cone-lifts-vs-exponential-rank.md`

- Three-cone binomial MGF: Proposition `prop:binomial-three-exp`, full rational lift, arbitrary competing signed nodes, Vandermonde proof, bounded probability support, and logarithmic coefficient bit length retained.
- Product-cosh exact rank 2^r and 2r+1 cone upper: Theorem `thm:cosh-exp-count`, with full elimination proof and generic-line independence proof.
- Arbitrary affine exponential lift lower: **strengthened from R >= r-1 to R >= r**, also covering r=1. Intersect the entire epigraph on its given compact cube with `t <= T` for T>1. The resulting full-dimensional compact body in R^(r+1) retains an r-dimensional positive-curvature lower graph near (0,1). Theorem `thm:curvature` applies after free-variable elimination, minimal-face reduction, and translation. Only a zero-capacity ray is added. This strictly subsumes the source's level-set argument and requires no globally smooth selections.
- Full ambient optimum 3R+P: references parent Stage 4C theorem `thm:entropy-product`; artificial truncation ray is not charged to the original ambient product. Distinguishes this from a restricted barrier or intrinsic projection optimum.
- General curved epigraph corollary: stated with definability and a compact polyhedral truncation retaining the patch. This is a derived extension, not an exact count assertion.
- Approximate transfer failure: Proposition `prop:exp-polyhedral-approximation` retains all tangent-net details, L=0 case, multiplicative bounds and epigraph directions, and explicit charging of scalar inequalities. Uncharged rays allow zero exponential cones. No approximate all-IPM claim.
- Standard exponential/log-sum-exp building blocks credited to the MOSEK Modeling Cookbook; the section claims the separation of output contracts, not novelty of those constructions. Renamed theorem to “Bounds for exact exponential lifts...” at the parent's request because [r,2r+1] is not an exact optimum.

## Independent author checks

- Cone-meet proof: lattice Riesz decomposition makes positive sums of disjoint extreme rays disjoint; any finite dependence is impossible. A compact base has at most d extreme points and spans, giving exactly d rays. Total order contradicts connectedness of S^(d-1) when d >= 2.
- Lorentz-circle proof: the original slice contains the open disk centered at zero of radius R-rho, excluding zero/negative radii in an alternative exact disk intersection. Finite noncoincident circles cannot cover an open arc.
- Dilation classification: the integral matrix M is invertible for small delta since M/delta tends to I; T(s)M has the differentiable sliding-integral expression. Matrix exponential classification therefore uses only continuity initially. Real dimension equals the complexified dimension after pairing conjugates.
- Corrected divergence identity checked algebraically: both sides are A D(X||Y)+B tr X+C tr Y-A tr X.
- Simplified oracle example: map `(t,x1,x2)` to `(t-|z|x1,Nx1,Nx2)` is invertible; the scalar entropy barrier pulls back to displayed F up to -2 log N. At (2,1,1), counts zero/one give -log 2 and 0.
- Cosh Hessian positive definite everywhere. T>1 and K>0 leave a genuine lower graph patch. C is compact even when some portions of the cube have empty vertical fibers, and a neighborhood of zero has nonempty interior vertical intervals. Any exponential-cone face is definable and has dimension at most 3, enough for the curvature capacity estimate; no regularity of the original lift is imposed.
- Tangent-net approximation uses line segments inside convex D and the uniform Hessian bound there; the L=0 branch is affine on D.

## Literature checked this turn

- Local `literature/papers/anselone1964-translation-invariant-subspaces-of-finite/paper.md`: metadata-only/unread; not represented as a full-text verification.
- Engert primary full PDF, https://msp.org/pjm/1970/32-2/pjm-v32-n2-p05-s.pdf : introduction on printed p.333 explicitly identifies the continuous theorem as prior Anselone–Korevaar/Loewner; bibliography printed p.342 gives Anselone–Korevaar 15 (1964),747–752. Our full direct proof avoids relying on an inaccessible source detail.
- Nemeth primary publisher PDF, https://mathematica-pannonica.ttk.pte.hu/articles/mp15-2/mp15-2-175-198.pdf : p.175 introduction states the Yudin closed-cone characterization. Title/year/volume/pages verified directly in the first page.
- MOSEK official documentation https://docs.mosek.com/modeling-cookbook/expo.html : version 3.4.0, Sections 5.2.5–5.2.6 softplus/log-sum-exp. Our exponential coordinate convention permutes its first/third coordinates explicitly by our definition.
- Durr–Hoyer primary arXiv quant-ph/9607014: O(c sqrt(N)) minimum with failure at most 2^(-c), the bound needed for simultaneous minima.
- Ambainis–Childs–Le Gall–Tani primary publisher PDF https://www.rintonpress.com/xxqic10/qic-10-34/0181-0189.pdf : Theorem 4, printed pp.185–186, adversary direct sum for arbitrary finite output alphabet, and Theorem 3 bounded-error adversary lower. Publisher PDF has 9 pages, 181–189 (arXiv metadata sometimes says 181–188).
- Local BHMT2002 and Nayak–Wu1999 literature packages read; primary arXiv records checked. Mean/count primitives are attributed, not claimed new.
- Targeted online searches for the compiler phrasing found no direct matching statement, but that absence does not establish priority. No “first” claim is made. The manuscript identifies the exact summary interpretation and feature/lift separation as applications of established ingredients.

## Bibliography additions requested

Existing `FS2023`, `Hatcher2002`, `HeSaundersonFawzi2026`, and parent-merged `DurrHoyer1996` are reused. Parent should add or merge the following keys (some may later be shared with Stage 5):

```bibtex
@article{Nemeth2004,
 author={N{\'e}meth, A. B.},
 title={The Facial Structure of the Finite Dimensional Latticial Cone},
 journal={Mathematica Pannonica}, volume={15}, number={2},
 pages={175--198}, year={2004},
 url={https://mathematica-pannonica.ttk.pte.hu/articles/mp15-2/mp15-2-175-198.pdf}}
@article{AnseloneKorevaar1964,
 author={Anselone, P. M. and Korevaar, J.},
 title={Translation Invariant Subspaces of Finite Dimension},
 journal={Proceedings of the American Mathematical Society},
 volume={15}, number={5}, pages={747--752}, year={1964},
 doi={10.1090/S0002-9939-1964-0169048-7}}
@article{Engert1970,
 author={Engert, Martin},
 title={Finite Dimensional Translation Invariant Subspaces},
 journal={Pacific Journal of Mathematics}, volume={32}, number={2},
 pages={333--343}, year={1970},
 url={https://msp.org/pjm/1970/32-2/pjm-v32-n2-p05-s.pdf}}
@article{ACGT2010,
 author={Ambainis, Andris and Childs, Andrew M. and Le Gall, Fran{\c c}ois and Tani, Seiichiro},
 title={The Quantum Query Complexity of Certification},
 journal={Quantum Information and Computation},
 volume={10}, number={3--4}, pages={181--189}, year={2010},
 eprint={0903.1291}, archivePrefix={arXiv},
 url={https://www.rintonpress.com/xxqic10/qic-10-34/0181-0189.pdf}}
@incollection{BHMT2002,
 author={Brassard, Gilles and H{\o}yer, Peter and Mosca, Michele and Tapp, Alain},
 title={Quantum Amplitude Amplification and Estimation},
 booktitle={Quantum Computation and Information},
 series={Contemporary Mathematics}, volume={305}, pages={53--74},
 publisher={American Mathematical Society}, year={2002},
 doi={10.1090/conm/305/05215}, eprint={quant-ph/0005055}, archivePrefix={arXiv}}
@inproceedings{NayakWu1999,
 author={Nayak, Ashwin and Wu, Felix},
 title={The Quantum Query Complexity of Approximating the Median and Related Statistics},
 booktitle={Proceedings of the Thirty-First Annual ACM Symposium on Theory of Computing},
 pages={384--393}, year={1999}, doi={10.1145/301250.301349},
 eprint={quant-ph/9804066}, archivePrefix={arXiv}}
@manual{MosekExpoCookbook,
 author={{MOSEK ApS}}, title={MOSEK Modeling Cookbook},
 edition={3.4.0}, year={n.d.},
 note={Sections 5.2.5--5.2.6; accessed 20 September 2026},
 url={https://docs.mosek.com/modeling-cookbook/expo.html}}
```

## Build check

A temporary standalone article in `/tmp/stage4c-compilers-check.tex` inputs the repository macros and this section. `pdflatex -interaction=nonstopmode -halt-on-error` succeeds, producing 7 pages. Cross-references to other stages and bibliography entries are intentionally undefined in this isolated harness; the parent must check the integrated build. The initially long proposition heading was shortened to remove the sole overfull hbox; the final repeated check is recorded in the handoff message.
