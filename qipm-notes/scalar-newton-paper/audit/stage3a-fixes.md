# Stage 3a corrections

All eleven accepted items in `stage3a-assessment.md` are addressed. The
main coherent-access and cyclic-realization proofs and conclusions remain
intact. No later stage was started.

1. **Box-centering accuracy:** `07-scalar-realizations.tex` now retains
   rho(eta)^2 in the sufficient objective-gap threshold and specifies an
   absolute sufficiently small constant. This addresses reviewer 1 item 1,
   reviewer 3 item 2, and reviewer 5 item 1.
2. **Counting range:** the sparse quantum comparison in `06-coherent.tex`
   explicitly requires d>=2, kappa>=4, and epsilon<=1/128, and states that
   its lower bound already holds for two-sparse sign blocks. This addresses
   reviewer 1 item 2 and the lead's integration finding.
3. **Setup margin:** the sampling discussion requires good-setup
   probability at least 1/2+c_setup for an absolute positive constant and
   conditional error at most c_setup/2. Even with adversarial bad setups,
   the resulting success is bounded above one half by a fixed margin.
   This addresses reviewer 1 item 3, reviewer 4 item 2, and reviewer 5
   item 2.
4. **Perturbation domain:** the projected-vector inequality explicitly
   assumes 0<=epsilon_v<1. This addresses reviewer 4 item 1.
5. **Finite synthesis:** the coherent history construction distinguishes
   its exact ideal state from its synthesized state. It gives a Euclidean
   error eta in (0,1), allocates eta/G_public operator error per public
   gate, retains O(k) hidden calls, and identifies eta<=epsilon_v with
   the relative-vector sampling tolerance. This addresses reviewer 4
   item 3.
6. **Tree label:** the product-barrier sum now has the proper internal-node
   label. This addresses reviewer 2 item 1 and reviewer 5 item 3.
7. **Padded-tree symmetry:** the center is established first with all D
   leaves free. Since it has all leaves zero, it remains the unique
   minimizer on the padded-leaf slice. The text no longer relies on the
   restricted problem retaining full-tree symmetry. This addresses
   reviewer 2 item 2.
8. **Vector-error notation:** epsilon_v is used consistently throughout
   the sampling subsection, including the conditioning and feasible-sample
   comparisons. Zeta remains the failure probability elsewhere. The
   p=Theta(epsilon_v) and p=Theta(epsilon_v^2) choices are stated in the
   small-vector-error regime relative to the fixed source gap. This
   addresses reviewer 2 item 3.
9. **Affine length calibration:** the additive O(1) calibration is inside
   the logarithm's numerator before division by 3 alpha_K. The text
   explains its O(K) layer effect and reserves the final O(1) term for
   allowed-length rounding. This addresses reviewer 3 item 1.
10. **Accumulator scaling:** the text explicitly replaces a by Ra in
    the readout coefficients multiplying x and uses w as objective. It
    does not suggest multiplying the whole equality. This addresses
    reviewer 3 item 3.
11. **Prior-work comparison:** `06-coherent.tex` now cites
    Orsucci--Dunjko, Proposition 6 and Sections 4.2--4.3, for the
    positive-definite solution-state lower bound and normalized shifted
    access. It distinguishes their output and access assumptions from
    this paper's relative scalar bound and bounded unshifted transform.
    It does not equate their inverse-polynomial degree with the complete
    state-preparation cost. `bibliography.bib` includes the verified
    Quantum 5, 573 (2021) metadata. This addresses reviewer 5 item 4.

The local primary full text was consulted for the Orsucci--Dunjko comparison;
its metadata were checked against the [publisher record](https://quantum-journal.org/papers/q-2021-11-08-573/).
The article DOI is 10.22331/q-2021-11-08-573.

## Validation

- `/workspace/local-home/miniconda3/envs/qipm/bin/python
  notes/scalar-newton-paper/scripts/verify_cyclic.py` passed all cyclic
  history, public metadata, tilt, decrement, tree, and completion checks.
- A clean, forced build ran through `conda run -n qipm --live-stream`
  with `make clean` and then `make -B` in the paper directory.
- The resulting PDF has 32 pages. Final LaTeX and BibTeX logs contain no
  warnings, undefined citations/references, or overfull/underfull boxes.
- `audit/workflow.md` records Stage 3a as corrected and pending root
  verification.

Verdict: all accepted Stage 3a corrections are complete, with no additional
issue identified during this correction pass.
