# Stage 2 author report — 2026-09-20

## Delivered mathematical material

- `sections/03-products.tex`: all-EJA support-join/compression identity; selection-free sequential existence of genuine original-slice pure-row aggregate certificates; every-final-fiber nullity; pointwise Hermitian private source dimensions and sharper `delta p_i d_ia` curvature; exact one-factor column packing, with genuine whole-slice certificates.
- `sections/04-global-regularity.tex`: pointwise Lorentz no-sharing; complete relative top-class cover proof with heterogeneous dimensions, active labels and vertex sets; exact globally C1 Lorentz factor/capacity/dimension frontier versus generic affine norm trees; exact two-ball joint Q3 count and general bounds; open-vertex switching necessity, explicit flat continuation counterexample; Lipschitz unique-fiber codimension-two norm-tree counterexample; local orthogonal projection splitting; everywhere differentiable strict capacity gap with checked Saint Raymond inverse theorem.
- `sections/05-support-orbits.tex`: global simple-EJA support-orbit covering and complete single-sphere classification; ball-specific exclusion of the real PSD3 exception; exact globally selected rank for any finite simple-EJA dictionary, including mixed fields/Albert; sequential additive selected ranks and factor-aware adaptive finite capacity envelope.

The selected-rank theorem is stated uniformly for simple EJA dictionaries, which consolidates and slightly generalizes the fixed-field and mixed-Hermitian source statements. Saturation forces q rank-one factors attaining B. Their primitive support orbits give a covering; only a lone matching spin can survive. Proper faces strictly decrease B, so compression cannot create a new exception. The fixed-tail Peirce construction attains the result, including Albert.

## Independent mathematical check and proof improvements

A separate agent reconstructed the single-ball topology while I wrote product/no-sharing sections. Its full proof text and audit are retained in `stage2-topology-proof.tex` and `stage2-topology-check.md`.

The real PSD3 exclusion was substantially simplified. Finite ray-status sets make the rank-two primal sheet affine on finitely many open regions; the C1 finite-affine-selection lemma glues them. An affine PSD pencil with nullity one and no common kernel has an injective kernel-line map: a nonnegative affine function on a sphere has at most one zero unless it vanishes identically. The required S2→RP2 double covering is impossible. This also eliminates every real order-R projective exception in the selected-rank proof. No determinant divisibility, Clifford relations, or unproved pencil normalization is needed.

The independent checker corrected Nomura's DOI to `10.1007/BF02108300`, publisher-verified. Hatcher Examples 4.47 and 4.53–4.55 were separately checked in the author-hosted PDF: they cover the octonionic Hopf construction, Stiefel/Grassmannian fibrations, and classical group stability used here. Saint Raymond's exact everywhere-differentiable local inversion hypothesis was checked against the Cambridge publisher abstract and Tao's author-hosted complete exposition. Bibliography entries were added. No priority claims are made for classical topology or Jordan calculus.

No invalidating defect in the retained results was found. The source quantifiers are corrected/preserved: sequential selection-free existence is not a bound on every aggregate certificate or on aggregate-fiber minimum rank; joint weighted kernels are not whole-row affine lifts; globally selected smooth rank is not an arbitrary-lift rank lower bound; ambient Lorentz parameter is not restricted-slice parameter.

## Exact source dispositions

The comprehensive source routing is appended to `source-map.md`. The main new theorems subsume precursor methods but not unrelated unique structural extensions. By agreement with root, general proper-cone face-sharing and global tangent-bundle/submersion/Steenrod results, all-EJA product-orbit classification, projective embedding and residual-kernel refinements are deferred to Stage4. Stage3 owns barrier consequences and all-EJA selection-free one-channel rigidity, which subsumes the critical-real selection-free affine note.

## Validation

`make -C conic-lift-complexity` completed successfully after integration. The log has no undefined references/citations or overfull boxes. Source proof reconstruction is the mathematical validation; no implementation-mirroring tests were added. Five independent stage reviewers are still required by the user's workflow; this report does not assert review completion.
