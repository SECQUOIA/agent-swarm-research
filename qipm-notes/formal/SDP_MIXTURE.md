# SDP central mixtures: formal verification

This development verifies the noncommutative central-mixture topic in
[`paper/sections/14-structural-tools.tex`](../paper/sections/14-structural-tools.tex),
subsection “Central mixtures in semidefinite programming.” The Lean sources
are in [`QipmFormal/SDPMixture/`](QipmFormal/SDPMixture/).

The result combines actual neighboring SDP centers, sparse coefficient
changes, matrix centrality, and output soundness. The matrix
arithmetic–harmonic and Kantorovich inequalities are classical; verification
also checks their composition with the repository's sparse residual argument.

## Mathematical objects and hypotheses

Matrices are finite real matrices. Matrix order is Loewner order, defined by
positive semidefiniteness of the difference. Square roots are the positive
square roots supplied by continuous functional calculus. Inverses are actual
matrix inverses; positive definiteness proves the required invertibility.
Different neighboring matrices need not commute.

For nonnegative weights summing to one, the definitions are

\[
 X_w=\sum_iw_iX_i,\qquad A_w=\sum_iw_iX_i^{-1},\qquad
 Z_w=X_w^{1/2}A_wX_w^{1/2},\qquad D_i=X_i-X_w.
\]

The actual slack hypothesis is \(S_i=\mu X_i^{-1}\), with \(\mu>0\).
Thus \(S_w=\mu A_w\), and the actual normalized complementarity matrix is
\(Z_w\). Positive definiteness of both averaged primal and slack matrices
is proved. Equality cases allow zero weights and constrain only the matrices
with positive weight.

`opNorm` is the operator norm induced by the Euclidean vector norm.
`frobeniusNorm` is the square root of the sum of squared matrix entries.
Neither uses the default entrywise maximum norm as a substitute.

`Coordinates.lean` constructs the real symmetric matrices as a subspace of
the Euclidean space of all entries. An orthonormal basis supplies an
isometric `svec`, with reconstruction, trace-pairing, and mixing identities.
The theorems accept any fixed such basis. A linear equivalence with
functions on unordered index pairs proves that the dimension is
\(r(r+1)/2\). The complementarity gap
uses the actual matrix order \(r\), not the number of vectorized coordinates.

The measurement map is \(\mathcal A(X)_a=\operatorname{tr}(F_aX)\), and its
trace adjoint is the actual sum \(\mathcal A^*(y)=\sum_a y_aF_a\).
Their correspondence with the coordinate matrix is proved. Sparsity and
height bounds refer to this fixed coordinate representation. Public
coefficients cancel; the coefficient bound concerns input-dependent
positions. Row and column incidence bounds must cover those positions
across the relevant inputs.

Positive matrix dimension is explicit wherever trace normalization divides by
\(r\). Uniform mixtures require a nonempty neighbor family. Residual
thresholds are nonnegative. Output soundness is an explicit contract on
candidate triples, not a consequence of sparsity.

## Verified claim map

All declarations are in `QipmFormal.SDPMixture`.

| Claim | Main source and declarations |
|---|---|
| Positive averages and inverse averages | `Variance.lean`: `matrixMix_posDef`, `inverseMix_posDef` |
| Exact matrix variance, including normalization | `Variance.lean`: `variance_identity`, `normalized_variance_identity` |
| Nonnegative defect and exact equality case | `Variance.lean`: `one_le_centralMatrix`, `centralMatrix_eq_one_iff` |
| Sharp noncommutative Kantorovich sandwich | `Sandwich.lean`: `arithmetic_harmonic_bound`, `centralMatrix_sandwich`, `centralMatrix_sub_one_le` |
| Endpoint construction and optimality of the constant | `Sandwich.lean`: `endpoint_mixture_sharp`, `endpoint_mixture_admissible`, `endpoint_mixture_forces_constant` |
| Exact endpoint widths and the individual-condition-number counterexample | `Sharpness.lean`: `endpoint_mixture_frobenius_sharp`, `endpoint_mixture_sdpDefect_point_zero`, `scalar_operator_condition_one`, `scalar_one_nine_operator_defect` |
| Euclidean operator and Frobenius norms, including their dimension factor | `NormBounds.lean` and `Frobenius.lean`: `opNorm_defect_le`, `frobeniusNorm_le_sqrt_card_mul_opNorm` |
| Trace recentering and both neighborhood conventions | `NormBounds.lean`: `normalized_defect_eq_recentered`, `opNorm_normalized_defect_le`, `frobeniusNorm_normalized_defect_le` |
| Dimension-free additive variance estimates | `VarianceBounds.lean`: `centralMatrix_operator_variance_bound`, `centralMatrix_frobenius_variance_bound`, and their recentered versions |
| Actual matrix complementarity and trace parameter | `Centrality.lean`: `sdpDefect_mixture`, `sdpDefect_mixture_point`, `pointParameter_mixture`, `complementarity_discrepancy` |
| Trace-gap bounds and scaling by the actual parameter | `Gap.lean`: `complementarity_discrepancy_bounds`, `pointParameter_mixture_bounds`, `opNorm_rawResidual`, `frobeniusNorm_rawResidual` |
| Dimension-free trace-variance refinement | `TraceVariance.lean`: `centralMatrix_trace_variance_bound`, `complementarity_discrepancy_variance_bound` |
| Actual SDP coordinate and adjoint bridge | `Coordinates.lean`: `dot_svec`, `norm_svec`, `svec_reconstruct`, `measurement_coordinates`, `adjoint_coordinates` |
| Symmetric coordinate dimension | `Coordinates.lean`: `finrank_symmetricMatrix` |
| Algebraic gap from neighboring SDP equations | `Coordinates.lean`: `sdp_objective_gap`, `sdp_mixture_objective_gap` |
| Sparse primal–dual residuals | `Residual.lean`: weighted and uniform actual SDP bounds, with both the sharper signed constant and the manuscript's original constant |
| Multibit coefficient dependence in both residual blocks | `Multibit.lean`: `sdp_multibit_kkt_sq`, `sdp_multibit_kkt_bound` |
| Affine and trace-normalized observable decoders | `Decoder.lean`: `matrixTripleScore_wrong_mix`, `observable_normalized_margin_mix`, `plusProbability_eq_measurement`, `plusProbability_valid` |
| Operator and Frobenius soundness for both centerings | `Paper.lean`: `operator_soundness_dichotomy`, `frobenius_soundness_dichotomy`, and raw-data compositions |
| Sharper uniform resource bounds | `Paper.lean`: `uniform_sharp_operator_soundness_dichotomy`, `uniform_sharp_frobenius_soundness_dichotomy` |
| Explicit decoder and additive-variance compositions | `Paper.lean`: `affine_operator_soundness_dichotomy`, `observable_operator_soundness_dichotomy`, their Frobenius versions, and `operator_variance_soundness_dichotomy`, `frobenius_variance_soundness_dichotomy` |
| Exact scalar ratio threshold and finite dimension dependence | `Ratio.lean`: `kantorovich_sub_one_eq_sinh_sq`, `common_parameter_ratio_iff`, `log_ratio_le_of_common_parameter_bound` |

The soundness proof constructs the averaged triple from actual neighboring
primal feasibility, dual stationarity, and matrix complementarity. It derives
its positivity, residual, algebraic gap, and centrality before applying the
contract. Generic wrong-output predicates support explicit affine scores
and trace-normalized binary observables. The observable acts on
\(X/\operatorname{tr}X\), not on normalized `svec` amplitudes.

## Results and manuscript corrections

The variance identity is exact:

\[
 Z_w-I=X_w^{-1/2}\left(\sum_iw_iD_iX_i^{-1}D_i\right)X_w^{-1/2}.
\]

Under \(0<m\leq M\) and \(mI\preceq X_i\preceq MI\), it gives
\(I\preceq Z_w\preceq K(M/m)I\), where
\(K(R)=(R+1)^2/(4R)\). The proof needs no common eigenbasis.

Keeping dual multipliers signed gives the weighted squared residual bound

\[
 4(s_r+s_c)B^2H^2\sum_i M_iw_i^2.
\]

For uniform weights this becomes
\(4(s_r+s_c)B^2H^2M_{\rm dep}/N^2\). It implies the paper's original
\(8s_{\rm KKT}B_{\rm KKT}^2H^2M_{\rm dep}/N^2\) bound. The paper now
states the stronger bound and specifies the common support and sign
conditions needed by its use.

Both centrality conventions preserve the algebraic gap \(r\mu\), with
the neighbors' original parameter. At the generally infeasible mixture,
the complementarity sum is \(r\mu_w\), and their discrepancy is
\(\mu\operatorname{tr}(Z_w-I)\). Point recentering does not replace the
algebraic gap by \(r\mu_w\).

For \(r>0\), \(\eta_F\geq0\), and \(R\geq1\), the condition

\[
 \sqrt r\,[K(R)-1]\leq\eta_F
 \quad\Longleftrightarrow\quad
 \log R\leq2\operatorname{arsinh}
   \left(\frac{\sqrt{\eta_F}}{\sqrt{\sqrt r}}\right)
\]

characterizes the worst-case **common-parameter** Frobenius certificate.
The equal endpoint mixture attains \(Z_w=K(R)I\). That mixture has zero
point-centered defect, so this example does not establish necessity for
point centering. The same condition is sufficient under either convention.
The finite bound \(\log R\leq2\sqrt{\eta_F}/\sqrt{\sqrt r}\) supplies
the stated fourth-root dimension dependence without an asymptotic assumption.

Finally, the scalar example \(1,9\) distinguishes the common spectral
ratio from individual matrix condition numbers. Both scalar condition
numbers are one, while the common-parameter defect is \(16/9\). The
paper now states that distinction explicitly.

## Scope

This verifies the finite SDP mixture argument. It does not formalize SDP
strong duality, existence of neighboring centers for arbitrary input data,
an IPM trajectory, a quantum query reduction, or a state-preparation
algorithm. Those are not inferred from the existential mixture certificate.
The output measurement consists of proved positive effects and their trace
probabilities; no quantum circuit or external simulation theorem is assumed.

The original research note is an archive, not an additional theorem
specification. The current manuscript and this report determine the verified
scope. The other three standalone manuscripts do not state this topic and
require no mathematical changes for it.

## Reproduction

From `formal/`, using the repository's pinned Lean and Mathlib versions:

```sh
conda run -n qipm --no-capture-output bash scripts/verify.sh
```

The integrated audit covers every declaration in imported project modules,
including private declarations. It permits only `propext`, `Classical.choice`,
and `Quot.sound`; added axioms, `sorry`, and `native_decide` dependencies
are rejected. Optional `--replay` separately rechecks the full import closure
in a fresh Lean kernel environment.

## Validation completed on 2026-09-20

- The integrated build and axiom audit passed for **1503 project
  declarations**, including all **16 SDP mixture modules** and the existing
  formalization topics. Every audited declaration depends only on the three
  allowed standard axioms. The final build emitted no warnings.
- Independent mathematical and Lean correspondence reviews checked the
  claim inventory, matrix and norm definitions, coordinate dimension,
  residual hypotheses, both centering conventions, sharpness, and final
  soundness compositions. No unresolved findings remained. The review
  prompted the dependent-coefficient correction described above and the
  explicit common-parameter qualification for the sharp ratio criterion.
- The manuscript rebuilt to **197 pages** without LaTeX warnings, unresolved
  references or citations, or overfull/underfull boxes. The revised residual,
  phase-boundary, and verification pages (164–166) were rendered and visually
  checked. The claim-map declaration names and repository diff whitespace
  checks also passed.
- The optional fresh-environment replay of the entire Mathlib import closure
  was **not run**. The completed checks are the project build and the
  declaration-level axiom audit defined by the repository's verification
  contract.
