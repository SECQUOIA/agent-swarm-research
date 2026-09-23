# Stage 4C: approximation author audit

Files authored: `sections/10c-conditioned-approximation.tex` (main text) and `sections/10f-approximation-refinements.tex` (appendix). These files are complete and frozen for the stage review. No main-file or bibliography edits were made.

## Sources and dispositions

All five assigned original notes and all of `audit/root-stage4-preparation.md` were read. Existing foundation/certificate normalization and Appendix 08e topology statements were checked for dependency labels and hypotheses.

- `approximate-ball-curvature-stability`: smooth near-complementarity lemma, finite-radius interpolation (including H=0), exact mixed derivative despite approximate body, reduction and local definable C2 selections, uniform quantitative contrapositive, ray treatment, ray-only polytope obstruction, two-block fixed-error example, and classical polyhedral approximation comparison are retained in 10c. The C2 error is strengthened as described below. No unconditional metric or Newton-system claim is made.
- `conditioned-approximate-curvature-capacity`: finite samples, explicit increment error, rank argument, uniform cubic-root-scale sufficient condition, radial primal/polar transfer, two-point orthant counterexample, and bounded-factor rescaling are retained in 10c. The source's final open fixed-complexity question is not presented as a theorem or as an unresolved requirement for these conditional results. No global fixed-size counterexample is claimed.
- `robust-global-saturation-topology`: canonical continuous projected maps, exact saturated bundle splitting, Adams/frame and even-sphere Euler consequences, stronger subset-rank consequences by existing proposition, fixed blockwise GL infimum, zero-factor convention, and its distinction from a Newton condition number are retained in 10f. Both source error bounds are subsumed by the sharper error estimate. Rays are explicitly excluded by nonzero norms and gamma<1; the general invariant separately permits them and handles the obstruction.
- `robust-q3-phase-integrability`: general closed simply connected manifold statement, both primal and dual phases, minimum radial bound, channelwise spectral floor, saturated near-Parseval consequence, C1 modulus and H=0 case, blockwise defect transfer, elementary factor-norm bounds, and all scope distinctions are retained in 10f. The unrelated source discussion of Tischler's theorem is unnecessary: the complete proof uses only phase lifting and extrema.
- `robust-saturated-block-submersion`: primal and symmetric dual bounds, singular values of nonsymmetric forms, Hopf exceptions, one-sided C1 interpolation, distinction from total diagonal derivative, normal-misalignment alternative, and saturated-profile arithmetic are retained in 10f. The classical sphere-submersion classification is cited through the already proved Proposition `prop:sphere-product-submersions` in 08e.

The parent owns the two conditioning-obstruction sources in 10g. My manuscript does not duplicate them and does not infer KKT lower bounds.

## Further development and verification

The source C2 error is

`U beta + V alpha + alpha beta gamma + U V gamma`.

It can be improved to

`U beta + V alpha + U V gamma`.

Indeed, with `X0=P_(b-perp) X` and `Y0=P_(a-perp) Y`,

`X*Y-X0*Y0=(X-X0)*Y+X0*(Y-Y0)`.

Thus the projection error is at most `alpha V+U beta`; no double-normal correction is needed. Deleting the last singular direction of the hyperplane pairing adds `UV gamma`. This argument is also valid for the canonical projector onto `a-perp intersect b-perp` used globally when gamma<1. It yields the sharper common bound

`E_k(eps)=2L sqrt(2H k eps)/mu+L^2 eps/mu^2`.

The original extra `2H eps^2/mu^4` is therefore unnecessary. I explicitly compare the two estimates in the text so the source is fully subsumed. Rays retain the distinct alpha*beta bound and add at most `2H eps/mu^2`. The relaxed contrapositive constant `mu/(4 sqrt(2k eps))` remains valid after the sharpening.

I independently checked the hyperplane singular values also in the parallel case, the finite rank argument, mixed-difference sign and tau identity, zero-factor two-sided differentiation, affine output offsets, saturation/direct-sum logic without positivity, GL composition invariance, phase tensor order, rank-r perturbation, and the arithmetic of the Hopf exceptions. I fixed one overfull display found by compilation.

The manuscript has no claim that ordinary definable selections give uniform charts or derivatives, no claim that an arbitrary approximation has global boundary factors, and no claim that fixed-coordinate derivative blow-up entails an intrinsic algorithmic penalty.

## Literature check

On 2026-09-20 I opened the primary arXiv full text of Gouveia, Parrilo, Thomas, *Approximate Cone Factorizations and Lifts of Polytopes*, https://arxiv.org/html/1308.2162v2, especially Sections 2.7 and 4.2 (Proposition 2.24 and Proposition 4.4). The former controls inner/outer polytope approximation from maximum Euclidean column/row errors of the finite slack matrix. The latter derives approximate generalized slack matrices from nested lifted approximations. These are explicitly distinguished from derivative and relative-increment control at curved contacts. The arXiv abstract record verifies Math. Program. 151(2) (2015), 613–637 and DOI 10.1007/s10107-014-0848-z. The automatically rendered HTML date was disregarded. I also opened the earlier Newton Institute PDF https://api.newton.ac.uk/website/v0/events/preprints/NI13069; its section numbering differs, so manuscript section citations use the final arXiv version.

The Ben-Tal–Nemirovski 2001 Theorem 1.1 and Proposition 3.1 comparison was checked against the assigned original source and root's primary-text verification. My attempted direct web request to https://www2.isye.gatech.edu/~nemirovs/MorLorentz.pdf failed; no fresh direct retrieval is claimed. Existing bibliography key `BTN2001` and topology references are reused.

No claim of priority for approximate cone factorization itself is made. The quantitative results are stated and proved on their exact hypotheses, without an unsupported absence-of-prior-work claim.

Add this bibliography entry (new key used in both files):

```bibtex
@article{GPTApprox2015,
 author={Gouveia, Jo{\~a}o and Parrilo, Pablo A. and Thomas, Rekha R.},
 title={Approximate Cone Factorizations and Lifts of Polytopes},
 journal={Mathematical Programming},
 volume={151}, number={2}, pages={613--637}, year={2015},
 doi={10.1007/s10107-014-0848-z},
 eprint={1308.2162}, archivePrefix={arXiv}
}
```

## Build

A temporary full-main wrapper inserted both new files without changing `main.tex`. Two pdflatex passes succeeded. Final check: `/tmp/approximation-check-qhb5qjzd/check.pdf`, 96 pages in the then-current integrated draft, no overfull boxes or LaTeX errors. Citation/reference warnings for other concurrently authored files and the not-yet-added bibliography entry are expected in this temporary wrapper; the stage author should run the complete integrated bibliography build after inserting the files. The temporary wrapper is not a deliverable and contains no repository mutations outside the two section files and this audit.
