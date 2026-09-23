# Stage 4C projected-compiler author audit

Owned manuscript file: `sections/10e-projected-compilers.tex` (frozen for integration and review).
Source read in full: `workbench/active/2026-09-04-projected-block-angular-barriers.md`.
Root preparation read in full: `audit/root-stage4-preparation.md`.

## Complete source disposition

- Shared-normal-fan Farkas compilation: included as Proposition `projected-fan`, with all lineality equations retained. The dual is restricted to `range W`, where it is pointed. Public full row rank is a sufficient condition for the advertised threshold-only query bound. The original source omitted the lineality qualification.
- Strict local recourse reconstruction: included with the exact necessary regime `h_i-Tx in ri(W R_+^p)`. Coercivity, unique minimization, and invertible KKT derivative proved. Boundary feasibility alone is insufficient; the local solve or facial reduction is charged separately.
- Varying recourse matrices: included with extreme-ray count `binom(p,r_i-1)` in the effective rank, and compatibility equalities. The full-row-rank special case recovers source count `binom(p,q-1)`. The explicit first-stage LP reduction is conditional on the published quantum LP algorithm's row access, data precision, full dimensionality, finite optimum, and central-path initialization. No claim of automatic initialization or cheap full recourse output.
- Ordered symmetric-cone scenario compiler: included. Rank parameter and worst-scenario quantum query exponent retain their proper scope.
- Scalar quadratic compiler: all formulas and exact parameter-one restriction are proved. Singular Q is handled on the quotient by its kernel or by adding the X0 barrier. The source's raw singular Hessian would not be a nondegenerate barrier on unreduced variables.
- Quantum Gram compiler: included using the actual published Loewner convention. Safe inflation is `(1+delta) Mtilde` when `(1-delta) Mtilde <= M <= (1+delta) Mtilde`; the resulting upper ratio is `(1+delta)/(1-delta)`. This is equivalent to source convention after reparameterization, but avoids silently reversing its bounds. Row queries are distinguished from block queries and arithmetic/output costs. Relative objective guarantee is limited to pure nonnegative least-squares minimization with fixed X0, and numerical solve error is additive.
- Matrix quadratic compiler: included with direct derivative proof of SC and exact parameter s. The arbitrary-barrier lower bound uses a diagonal orthant slice. Flat x-directions are quotiented or controlled by X0. The block Gram matrix has order `(k+1)s`. Spectral approximation preserves a uniform Loewner upper bound but does not automatically establish a relative guarantee for every SDP objective.
- Factorized Cramer obstruction: included with the concrete uniform measure, exact conjugacy identities, and derivative asymptotics. This makes the tight boundary ratio rigorous instead of differentiating an unspecified O(1) error. Degenerate blocks are expressly part of the theorem. The conclusion is a scalar normalization obstruction, not an impossibility for arbitrary entropic or universal barriers.
- Distinct exponential weights: included continuous-summary lower bound d >= N, with Vandermonde and invariance-of-domain proof; no decoder continuity hypothesis. Parent approved its inclusion despite the adjacent dilation-rank discussion.
- Reusable boundary/membership summary obstruction: included for the full rotated-SOC example, with a precise joint-success and reuse contract for either classical or quantum summaries. A consumed quantum state is not silently treated as a reusable oracle. Membership margin is stated as vertical, not Euclidean. Full oracle interrogation lower bound is proved using Fourier degree and state-span dimension. Power/exponential transfer is included, rescaling exposed locations to i/N to keep the common exponential bounded.
- Local weighted barrier obstruction: included with exact asymptotic derivative ratio and vertical decrement lower bound. Universal parameter-two existence is correctly distinguished from efficient oracle access. This is not a lower bound on arbitrary barriers.
- Source novelty speculation: not promoted to a priority claim. The manuscript expressly identifies Farkas elimination, quadratic epigraph barriers, quantum spectral approximation, and oracle interrogation as established ingredients, and limits the claims to the proved compilation and formula-restricted obstructions.

## Literature verification

Local literature note `../literature/papers/lee2021-universal-barrier-is-n-self/paper.md` was read; it confirms the theorem for proper convex domains, including the scope of the existential parameter bound.

Primary online sources checked on 20 September 2026:

1. Apers and Gribling, *Quantum Speedups for Linear Programming via Interior Point Methods*, SIAM J. Comput. 55(1) (2026), 93--134, DOI 10.1137/25M1736098. Published full text: https://epubs.siam.org/eprint/SRMWD7QVGV6NK54DQNUC/full . **Published LP theorem is 1.3, not 1.1 (the preprint numbering).** Theorem 3.1 retains the Gram approximation statement. Theorem 6.1 and Remark 6.2 require a near-central starting point. Primary arXiv v2 was also read for the full row-access and pseudoinverse context: https://arxiv.org/html/2311.03215v2 . The manuscript cites published numbering.
2. Durr and Hoyer, primary https://arxiv.org/abs/quant-ph/9607014, minimum finding. Joint success across thresholds is allowed logarithmic amplification.
3. Bennett, Bernstein, Brassard and Vazirani, primary https://arxiv.org/abs/quant-ph/9701001, standard quantum search lower bound. The source family is an immediate OR reduction.
4. van Dam, primary https://arxiv.org/abs/quant-ph/9805006. Author's thesis publication list https://sites.cs.ucsb.edu/~vandam/cwi_thesis.pdf confirms FOCS 1998, pages 362--367. The lower bound used here is also proved directly rather than relying on an unverified theorem number.
5. Targeted searches for Cramer/convolution/self-concordant normalization and quadratic recourse projected barriers found no matching impossibility theorem. This is not an exhaustive novelty certification and no priority claim was added. The source's tentative claim of a new general barrier was not retained.

## Validation

A temporary standalone wrapper outside the repository compiled the new section successfully with pdflatex. It is six pages in 11pt article format. Two overfull lines found on the first pass were rewritten before freezing. New bibliography keys below must be integrated by the parent; the isolated wrapper's undefined citation warnings are expected until that integration. No other project files were edited.

## BibTeX entries to integrate

```bibtex
@article{ApersGribling2026,
 author={Apers, Simon and Gribling, Sander},
 title={Quantum Speedups for Linear Programming via Interior Point Methods},
 journal={SIAM Journal on Computing}, volume={55}, number={1},
 pages={93--134}, year={2026}, doi={10.1137/25M1736098},
 eprint={2311.03215}, archivePrefix={arXiv}}
@misc{DurrHoyer1996,
 author={D{\"u}rr, Christoph and H{\o}yer, Peter},
 title={A Quantum Algorithm for Finding the Minimum}, year={1996},
 eprint={quant-ph/9607014}, archivePrefix={arXiv},
 url={https://arxiv.org/abs/quant-ph/9607014}}
@article{BBBV1997,
 author={Bennett, Charles H. and Bernstein, Ethan and Brassard, Gilles and Vazirani, Umesh},
 title={Strengths and Weaknesses of Quantum Computing},
 journal={SIAM Journal on Computing}, volume={26}, number={5},
 pages={1510--1523}, year={1997}, doi={10.1137/S0097539796300933},
 eprint={quant-ph/9701001}, archivePrefix={arXiv}}
@inproceedings{vanDam1998,
 author={van Dam, Wim},
 title={Quantum Oracle Interrogation: Getting All Information for Almost Half the Price},
 booktitle={Proceedings of the 39th Annual IEEE Symposium on Foundations of Computer Science},
 pages={362--367}, year={1998}, doi={10.1109/SFCS.1998.743486},
 eprint={quant-ph/9805006}, archivePrefix={arXiv}}
```
