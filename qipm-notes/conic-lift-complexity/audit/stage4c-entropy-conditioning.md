# Stage 4C: entropy and conditioning author checks

## Sources read completely

- `exponential-product-exact-barrier-parameter`.
- `contact-regularity-vs-ipm-conditioning`.
- `curvature-conditioning-kkt-invariance-obstruction`.

## Coverage and corrections

Section 10b proves the orthant-input/output recession certificate directly, explicitly attributes it to Fawzi–Saunderson Theorem 3.10, and tensorizes it. It contains exact 3R+P mixed primal/dual exponential/ray parameters, compatible one-sided hypographs, matrix QRE product specialization, 3N versus 2N+B block aggregation, the general positive-output map parameter, its sparse Hessian factorization, and the parameter-only square-root comparison. The exponential projective cross-ratio certificate is an alternative proof of the identical 3R bound and is subsumed by the stronger arbitrary-barrier recession proof; no new priority is claimed for it.

**New correction:** the source's exact closed coordinatewise exponential lift is false if A has a zero column. With A=0, x=1,y=0,z=0 belongs to C_A but has no finite exponential epigraph variable. Section 10b replaces each unused exponential by two orthant rays; the corrected ambient parameter is 2N+n_++B, while intrinsic 2N+B is unchanged. Every nonzero column provides an output inequality bounding its entropy along approximating sequences because phi(x,y)>=-y/e, proving finite epigraph fibers. This covers zero and duplicate rows and all zero-column cases without an unstated closure-of-image convention.

Section 10g proves exact Schur invariance and augmented KKT congruence, sparse boost norm degeneration and lambda^-4 raw Hessian conditioning, invariant transported contact quantities, radial oscillation and rotating-boundary counterexamples, fixed and vanishing error versions, artificial identity-KKT embedding with changing RHS, and explicitly conditional chi/bit bounds. It corrects the source's H_B=0 overstatement by retaining the finite-radius infimum and requiring a fitting optimizing radius for the square-root specialization. No single fixed approximate forbidden lift or unconditional algorithmic condition-number lower bound is asserted.

## Literature actually checked

- Local FS2023 `paper.md` and extracted `fulltext.md`, especially Sections 3.1 and 3.3, plus primary HTML https://arxiv.org/html/2205.04581v3. The published Theorem 3.10 handles orthant outputs directly; do not transfer a lower bound from a larger matrix cone by restriction. Compatibility was independently derived from D2 phi=x(u-v)^2 and D3 phi=-x(u-v)^2(u+2v).
- Local He–Saunderson–Fawzi 2026 paper.md and full text introductory structured cone theorem and examples; primary arXiv https://arxiv.org/html/2407.00241v3. It establishes positive input maps including singular images and redundant determinant removal; these are attributed rather than claimed new.
- Chen–Goulart final publisher full text https://link.springer.com/article/10.1007/s10957-024-02573-5 confirms authors Yuwen Chen and Paul Goulart, JOTA204 article33(2025), sparse/low-rank nonsymmetric Hessian precedent.
- NT1997 publisher metadata and Cornell author primary copy https://people.orie.cornell.edu/miketodd/orie6327/nestonn2.pdf; pointwise self-scaled geometry is classical.

Own sections currently build cleanly in the integrated manuscript. Formal five-review cycle belongs to root and has not occurred for this stage.
