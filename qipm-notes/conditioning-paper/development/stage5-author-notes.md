# Stage 5 author completion

Stage 5 authoring is complete. The assembled manuscript is 36 pages and compiles without warnings, undefined references/citations, or overfull/underfull boxes. This is the author-complete version for the required five independent reviews; it does not pre-empt those reviews or the later full-manuscript review.

## Delivered manuscript material

- `sections/01-introduction.tex`: motivation, the central geometric law, explicit comparison to prior work, qualified and specific novelty claims, and contributions/organization.
- `sections/11-numerics.tex`: exact-example checks, benchmark representation certificates and precision screens, and synthetic clustered-CG accuracy.
- `sections/12-discussion.tex`: consequences and scope of the developed results.
- `main.tex`: complete abstract, keywords, and all section inputs; no stage placeholders remain.
- `bibliography.bib`: Netlib provenance reference and Duistermaat (2001) comparator added.
- `sections/03-geometry.tex`: precise acknowledgment of the classical same-point comparison in NN1994, distinguished from equal-gap comparison at different centers.
- `sections/08-lp-spectra.tex`: the rectangle's standard-form slack embedding and the Duistermaat oscillatory-barrier antecedent.
- README and Makefile: standalone build and reproduction instructions, with anonymous submission metadata left for the submitting authors rather than invented names.

The original paper, literature corpus, and unrelated `central-path-cost/` were not edited.

## Numerical package

`repro/reproduce.py` regenerates all numerical artifacts from bundled data. It uses NumPy, SciPy, Matplotlib and standard-library Fraction/Decimal only. `repro/decimal_linear.py` supplies independent high-precision reference solves. `repro/prepare_data.py` records the optional one-time capture and exact-certificate construction from already prepared cached `.std` NPZ files; it does not claim to perform the MPS presolve itself. Ordinary reproduction has no parent import or network dependency. Full instructions and numerical contracts are in `repro/README.md`.

The source MPS and cached arrays are hashed in `repro/data/provenance.json`; the frozen JSON arrays define the numerical representation. Each input includes rational strict-feasibility, compactness, and primal/dual objective-bracket certificates. All were verified with exact binary-rational input interpretation, without tolerances. Afiro/sc50b have eta=0 compact-feasible-set certificates; adlittle has eta=1 compact-sublevel certification. The certified objective widths are about 8.16e-12, 9.40e-12, and 4.43e-7, respectively. Root independently verified the certificates while authoring proceeded.

The package contains six sets of numerical evidence:

1. Fractional SDP: stable 80-digit quadratic-root formulas, all four scales and constants, and the two-dimensional section. Separate direct trace-product generalized Hessian eigenvalues at g=1e-2,1e-4,1e-6 agree within 1e-7. Independent checks of exported last-row constants give maximum relative error 1.30e-12 against the four proved limits; paired condition constants agree within 1e-10.
2. Near-degenerate simplex: 70-digit monotone scalar centering, factor-SVD condition numbers, and exact limiting constants.
3. Compact degenerate LP: continuation to mu=1e-9 and a separately formed limiting matrix. The scaled eigenvalues and condition number agree with the proved limit to the stated tolerances.
4. Oscillatory barrier: the exact subsequence, weak forcing/gap ratio, and relative direction error, with 80-digit scalar calculations. The limiting weak ratio is 0.01 while the relative solution error tends to one.
5. Netlib: all 81 attempted points retained. Exact rational feasibility repair and certified gap brackets are combined with an unscaled decrement test, equality/positivity/repair checks, and a conservative numerical factor-SVD resolution indicator. This last criterion is expressly not a rigorous singular-value certificate. Accepted counts are 14/27 afiro, 19/27 sc50b, 12/27 adlittle. The last accepted gaps are about 3.34e-6, 1.40e-8, and 0.680. No limiting exponent is fitted or inferred from these curves. Earlier author experiments accepted much deeper spectra on centrality alone; those were superseded before author completion by the documented spectral-resolution screen.
6. Clustered CG: 60-dimensional fixed-seed synthetic matrices with many distinct prescribed eigenvalues in two intervals. The actual float64 matrix is symmetrized, and the prescribed spectrum is checked numerically after construction. Actual matrices/RHS are stored in `cg_systems.json`. CG operates on that rounded matrix. An 80-digit reference solve of exactly those binary-rational matrix/RHS values supplies the final true residual and energy error. Final iterations are 43,71,96,124; the deepest recursive residual is about 2.95e-9 while its true residual is 2.52e-8 and energy error 8.55e-9. The paper explains both lost finite-precision conjugacy and the distinct stopping contracts. It does not reuse the three-eigenvalue symmetric old toy or unbundled precision claims.

All raw results, rejected rows, generated vector figures/TeX tables, and command/version/hash metadata are supplied. The manifest records the exact configured Python command and a portable equivalent. PDF creation timestamps are suppressed.

## Verification and presentation

The complete reproduction command was run repeatedly with the configured qipm Python and single-threaded BLAS. Two consecutive final runs produced identical hashes for every input, script, raw numerical result, TeX table, and vector figure in the manifest. The final command was:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/sgusev/miniconda3/envs/qipm/bin/python repro/reproduce.py
```

`make` passed after assembly and final citation additions. Logs are `stage5-reproduction.log`, `stage5-reproduction-repeat.log`, and `stage5-build.log`. The current extracted reading text is `stage5-manuscript-text.txt`.

Figures were regenerated near their final physical widths (6.4 inches for the two-panel SDP figure, 3.15 inches for each half-width LP panel). Rendered manuscript pages 31–33 were inspected at 1200 pixels; labels, legends, tables, and captions are legible and unclipped. This inspection caught and corrected one missing backslash before kappa in the numerical SVD screen. The final clean build has no TeX warnings.

## Source access and novelty boundaries

The existing source audit and mathematical sections guided the introduction. In this stage the author additionally browsed the primary Netlib collection index and the Xiong–Freund arXiv record. The original-MPS data index supports the benchmark attribution; no new unchecked theorem was taken from a search result.

Root identified two additional direct comparators during assembly, both incorporated before declaring author completion:

- NN1994, Proposition 2.3.2(iii), equation (2.3.9), printed p.35: the fixed-point symmetric chord/Hessian comparison. The author read the local original's extracted text (root's `/tmp/conditioning-nn-earlier.txt`). The introduction and geometric section now make clear that same-point cross-barrier comparison is classical; the present equal-gap theorem permits different centers.
- Duistermaat, *On the Boundary Behaviour of the Riemannian Structure of a Self-Concordant Barrier Function*, Asymptotic Analysis 27(1),9–46 (2001), DOI 10.3233/ASY-2001-448. The author independently opened the primary Utrecht manuscript, https://dspace.library.uu.nl/bitstream/handle/1874/2052/1113.pdf?isAllowed=y&sequence=1, and read the introduction, Definition 2.1, Assumption 2.1, and Remark 2.3 (preprint pp.1–4). The latter uses f+A sin(f) to create oscillatory rescaled derivatives within the self-concordant class. The manuscript credits this antecedent and confines the new example's claims to its mixed perturbation, global certificate, sharp projector rate, and direction-error calculation.

No priority is claimed for basic Dikin/chord comparison, the first relation between level geometry and conditioning, gap parameterization, a generic inverse-square upper bound, classical LP endpoint limits, the fractional SDP construction, oscillatory self-concordant barriers in general, or qualitative central-path nonconvergence. The introduction's qualified priority statement is specific to equal-gap comparison at different centers, its residual-dependent bounds, and the matching diameter characterization. Detailed source comparisons remain beside the relevant results.
