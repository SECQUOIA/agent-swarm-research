Independent source audit, 2026-09-12. Question: does Wang et al.'s correlated-noise selection formulation compute Fisher information for the marginal observations actually selected?

**Finding: generally no.** The source equations and public implementation use a principal submatrix of the full inverse covariance. Marginal selected observations require the inverse of their principal covariance submatrix. These operations differ for correlated noise. This is a statistical-model mismatch even for a linear Gaussian model with exact arithmetic. It does not invalidate independent-noise instances, the implementation of the stated optimization problem, or every possible correlated instance.

The strongest defensible interpretation is narrower than “the formula conditions on all candidate observations.” It represents selected responses supplemented by the unselected **noise values**, or a modified experiment in which every candidate channel is observed but only selected channels carry a parameter-dependent signal. Conditioning on the actual unselected responses generally changes the mean sensitivity as well. The distinction is derived below.

Sources and versions inspected:

| Source | Version and access | Relevant locators |
|---|---|---|
| Wang, Peng, Hughes, Bhattacharyya, Bernal Neira, and Dowling, *Measure This, Not That: Optimizing the Cost and Model-Based Information Content of Measurements* | [arXiv:2406.09557v1](https://arxiv.org/pdf/2406.09557v1), submitted June 13, 2024; 56 PDF pages | Printed pp. 8–11, Eqs. (6)–(11); p. 15, Eq. (17); p. 22; SI p. S-2, Table S-1. PDF pages 10–13, 17, 24, 48 respectively. |
| Same work, *Computers & Chemical Engineering* 189, 108786 | [DOI 10.1016/j.compchemeng.2024.108786](https://doi.org/10.1016/j.compchemeng.2024.108786). [OSTI accepted manuscript](https://www.osti.gov/servlets/purl/2447595), identified as such by its [repository record](https://www.osti.gov/biblio/2447595); title-page date September 20, 2024; 54 PDF pages | Same printed locators; PDF pages 9–12, 16, 23, 46 respectively. |
| Liu, Chepuri, Fardad, Masazade, Leus, and Varshney, *Sensor Selection for Estimation with Correlated Measurement Noise* | IEEE *Transactions on Signal Processing* 64(13), 3509–3522, 2016; [DOI 10.1109/TSP.2016.2550005](https://doi.org/10.1109/TSP.2016.2550005); [author-hosted journal PDF](https://ecs.syr.edu/faculty/fardad/Papers/LiuCheFarMasLeuVar16.pdf) | p. 3511, Eqs. (5)–(11); pp. 3514–3515, Eqs. (29)–(32) and Proposition 2; PDF pages 3, 6–7. |
| Authors' software | [dowlinglab/measurement-opt](https://github.com/dowlinglab/measurement-opt/tree/430090e610446aab88328ce495ffb15b684c56c4), commit `430090e610446aab88328ce495ffb15b684c56c4`, January 14, 2025 | Immutable file links below. |

The inspected Wang methodology pages, kinetics covariance page, and SI covariance page have identical whitespace-normalized extracted text in the two versions. Important equations and the asymmetric SI table entry were also checked visually against the PDFs. The publisher's version of record was not retrieved: the publisher page returned HTTP 403. This audit therefore does not certify identity with the final typeset article. The later accepted manuscript is stronger evidence than relying on the arXiv version alone.

Wang's Eqs. (8)–(10) define pair coefficients from blocks or entries of the full inverse error covariance. Equation (11) gates those coefficients by joint selection. The approximation language accompanying Eqs. (6)–(7) concerns nonlinear-model asymptotics; the inspected methodology does not describe a weak-correlation approximation or observations of unselected noise. [Accepted manuscript, printed pp. 8–11](https://www.osti.gov/servlets/purl/2447595).

The implementation removes potential ambiguity in “corresponding” inverse blocks:

- [`measure_optimize.py`, lines 757–841](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/measure_optimize.py#L757) computes `np.linalg.pinv(Sigma)` once, then extracts entries or blocks. For the positive definite examples below, the pseudoinverse equals the inverse.
- [Lines 843–923](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/measure_optimize.py#L843) precompute sensitivity–precision–sensitivity contributions. [Lines 1157–1188](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/measure_optimize.py#L1157) sum them with pair-selection variables; lines 1216–1248 impose the binary product conditions.
- The CVXPY comparison reuses those same coefficients: [`cvxpy_problem.py`, lines 150–160](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/cvxpy_problem.py#L150), and [`measure_optimize.py`, lines 2333–2345](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/measure_optimize.py#L2333). Agreement between these solver paths does not independently validate the observation likelihood.

For an independent derivation, let

\[
Y=\mu(\theta)+\epsilon,\qquad \epsilon\sim N(0,R),\qquad R\succ0,
\]

where the known covariance is independent of the parameter. Let \(J=\partial\mu/\partial\theta\), let \(U\) be the selected indices, and let \(V\) be their complement. Arrange

\[
R=\begin{bmatrix}A&B\\B^\top&C\end{bmatrix},
\quad A=R_{UU},\quad C=R_{VV}.
\]

Marginalizing the unobserved responses gives \(Y_U\sim N(\mu_U,A)\). Its score is \(J_U^\top A^{-1}(Y_U-\mu_U)\), so its information is exactly

\[
I_{\mathrm{marg}}(U)=J_U^\top A^{-1}J_U.
\]

The intended ordered-pair computation in the software instead gives

\[
I_{\mathrm{gate}}(U)
=J_U^\top(R^{-1})_{UU}J_U
=J_U^\top(A-BC^{-1}B^\top)^{-1}J_U.
\]

The following conclusions are independent of nonlinear parameter-estimation approximations. They also apply after adding the same prior information matrix to both expressions. The elementary counterexamples use one measurement type only, so they do not depend on the counting convention for mixed SCM/DCM cross terms in the displayed paper equation.

1. **The information error is positive semidefinite at any fixed selection.** By block inversion,
   \[
   I_{\mathrm{gate}}-I_{\mathrm{marg}}
   =J_U^\top A^{-1}B(C-B^\top A^{-1}B)^{-1}B^\top A^{-1}J_U\succeq0.
   \]
   Equality holds exactly when \(B^\top A^{-1}J_U=0\). Thus zero selected/unselected covariance is sufficient, but is not necessary for a particular sensitivity matrix.
2. **Several important cases remain exact.** They include selecting everything, independent noise, selecting unions of complete independent covariance blocks, and special sensitivity directions satisfying the equality condition. Temporal correlation within an all-or-nothing sensor block is harmless if that block is independent of all other selection units.
3. **Conditioning on raw noise matches the gated formula.** If \(\epsilon_V\) is supplied as parameter-independent side information, then the conditional mean of \(Y_U\) is \(\mu_U+BC^{-1}\epsilon_V\), with sensitivity \(J_U\), and conditional covariance \(A-BC^{-1}B^\top\). Equivalently, observe all channels under the different model \(Y=D\mu(\theta)+\epsilon\), where \(D\) is the diagonal selection mask.
4. **Conditioning on actual responses is different.** For fixed \(Y_V=y_V\),
   \[
   E[Y_U\mid Y_V=y_V]=\mu_U+BC^{-1}(y_V-\mu_V),
   \]
   so the conditional sensitivity is \(J_U-BC^{-1}J_V\), and
   \[
   I_{U\mid V}=(J_U-BC^{-1}J_V)^\top
   (A-BC^{-1}B^\top)^{-1}(J_U-BC^{-1}J_V).
   \]
   The full-response information adds \(J_V^\top C^{-1}J_V\) to this conditional information. Calling the gated formula the information “conditional on the other observations” without this sensitivity correction is generally false.

Two exact rational witnesses make the consequences explicit.

First, take two equally sensitive measurements,

\[
R=\begin{bmatrix}1&3/4\\3/4&1\end{bmatrix},\qquad J=\begin{bmatrix}1\\1\end{bmatrix}.
\]

| Data or calculation | Information |
|---|---:|
| Only response 1 observed, marginal likelihood | \(1\) |
| Only response 1 selected, full-inverse gating | \(16/7\) |
| Both responses observed | \(8/7\) |
| Response 1 conditional on the actual response 2 | \(1/7\) |

The gated score even decreases when the second response is selected. Marginal information increases from \(1\) to \(8/7\), as it must. The gated selection-dependent experiment changes which channels carry signal, so its failure of the ordinary “more observations cannot hurt” property is explicable under that different model.

Second, suppose exactly one of three equal-cost sensors may be selected, with

\[
R=\begin{bmatrix}1&0&3/4\\0&1&0\\3/4&0&1\end{bmatrix},\qquad
J=\begin{bmatrix}1\\6/5\\0\end{bmatrix}.
\]

The exact singleton information values are \((1,36/25,0)\); the gated values are \((16/7,36/25,0)\). Therefore the marginal criterion selects sensor 2 while gating selects sensor 1. This is a change in the optimal decision, not just objective scaling. For one parameter the ranking also holds for log information and for minimizing inverse information.

The connection to Liu et al. is direct. Their exact selected covariance appears in Eqs. (5)–(7), and Eq. (11) rewrites its dependence on binary selection without an inverse of a changing-size submatrix. Their Eqs. (29)–(31) analyze the same full-inverse gating expression, with prior information added. Proposition 2 establishes agreement through first order for a weak-correlation family \(R=\Lambda+\varepsilon\Upsilon\), with an \(O(\varepsilon^2)\) information error. [Journal PDF, pp. 3511, 3514–3515](https://ecs.syr.edu/faculty/fardad/Papers/LiuCheFarMasLeuVar16.pdf).

For clarity, write \(R=aI+S\), with \(a>0\) and \(S\succ0\). Liu's observation-information identity, in the notation of this audit, is

\[
I_{\mathrm{marg}}(D)=J^\top S^{-1}J
-J^\top S^{-1}(S^{-1}+a^{-1}D)^{-1}S^{-1}J.
\]

This supplies a general exact baseline; adding a prior is separate. Weak correlation is a sufficient asymptotic regime for the gated approximation, not a necessary condition for every accidental equality or correct optimal decision. Neither the Liu result nor the witnesses establish that every published correlated instance changes its optimizer. Also, Wang maximizes trace of information under the label A-optimality, whereas Liu's main criterion minimizes trace of inverse information; the objectives should not be conflated.

The actual kinetics covariance makes the discrepancy relevant to the supplied experiment, while also revealing a simple exact alternative. Define

\[
C_0=\begin{bmatrix}1&1/10&1/10\\1/10&4&1/2\\1/10&1/2&8\end{bmatrix}.
\]

The construction in [`kinetics_MO.py`, lines 69–109](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/kinetics_MO.py#L69) gives, at each time, in the order SCM-A, SCM-B, SCM-C, DCM-A, DCM-B, DCM-C,

\[
R_6=\begin{bmatrix}C_0&C_0/2\\C_0/2&C_0\end{bmatrix}
=\begin{bmatrix}1&1/2\\1/2&1\end{bmatrix}\otimes C_0.
\]

Different times are independent. The code's covariance is symmetric positive definite; its determinant is \(16893387/40000>0\), and all leading principal minors are positive. Same-species cross-modality correlations are \(1/2\). Thus small cross-species correlations do not make every off-diagonal standardized correlation small.

The inverse's SCM–SCM block is \((4/3)C_0^{-1}\). Selecting all SCM channels and no DCM channels at a time therefore produces exactly \(4/3\) times the marginal information, for any sensitivities. This algebraic example is not asserted to be feasible at every published budget. A single selected A, B, or C channel has information inflation factor respectively

\[
3175/2373\approx1.337969,\qquad
3196/2373\approx1.346818,\qquad
152/113\approx1.345133.
\]

These factors follow from the supplied covariance, not from generic invented correlations. SI Table S-1 has an apparent transcription error: its DCM-A/DCM-C entry is 0.01 but its transpose is 0.1. Both visually inspected manuscripts contain that asymmetry. The public code uses 0.1 in both entries; the calculations here use the code's symmetric covariance rather than silently treating the literal table as a valid covariance matrix.

For the rotary-bed case, [`rotary_bed_MO.py`, lines 111–120](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/rotary_bed_MO.py#L111) builds a diagonal covariance. This selection-versus-inversion issue does not affect that case.

An exact formulation for the actual kinetics structure can precompute at most \(2^6=64\) subset patterns per time. For pattern \(P\), its contribution is

\[
F_{t,P}=J_{t,P}^{\top}(R_6)_{PP}^{-1}J_{t,P},\quad F_{t,\varnothing}=0.
\]

Choose one pattern at each time, tie each SCM's presence across all times, and apply the original installation, sampling, and budget constraints. Then \(I=I_0+\sum_{t,P}z_{t,P}F_{t,P}\) is exactly the marginal selected information. Infeasible patterns can be removed. This is an independent derivation of a baseline, not a claim of novelty or a completed benchmark rerun.

Treating modalities as independent temporal chains would lose the same-time correlations. The supplied example has independent time blocks, so a temporal predecessor model is unnecessary. If temporal Markov noise is introduced, predecessor factors for complete observed vector blocks do not automatically remain valid under arbitrary partial channel observation. The full block here has six channels; a two-dimensional block applies only to a separately specified one-species/two-modality model. A temporal extension must justify the observation structure instead of assuming that the latent process's Markov property survives arbitrary missing channels.

For a separate benchmark reproduction, the following public files and distinctions matter:

| Item | Source and audit finding |
|---|---|
| Sensitivity input actually read | [`kinetics_source_data/Q_drop0.csv`](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/kinetics_source_data/Q_drop0.csv): 24 rows, four columns `A1,A2,E1,E2`; eight rows each for CA, CB, CC. `kinetics_MO.py` duplicates each species' sensitivities across SCM/DCM modalities. The leading CSV column is an index, not a parameter. |
| Time grid | `kinetics_MO.py` sets `Nt=8` and maps the nonzero points of `linspace(0,60,9)` to the eight observations: 7.5, 15, …, 60 minutes. The stored sensitivity input omits time zero. |
| Costs and budgets | SCM installation costs 2000 per species; DCM installation 200, then 400 per sample. `kinetics_MO.py`, lines 14–64 and 218–219, uses budgets 1000, 1400, …, 5000 for integer runs. |
| Restrictions implemented | `kinetics_MO.py`, lines 209–210, excludes simultaneous SCM/DCM installation for each species and enables the global 10-minute DCM separation option. `measure_optimize.py`, lines 1424–1454, applies that separation across all DCM species. This differs from a reading that permits separate species to be sampled independently at the same time. |
| Parameter regularization | `kinetics_MO.py` sets the default diagonal addition to `0.0001`. A reproduction must explicitly match whether objective evaluation includes this term. |
| Physical equations | [`kinetics_source_data/reactor_kinetics.py`](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/kinetics_source_data/reactor_kinetics.py): consecutive first-order reactions, Arrhenius rates, and mass balance. |
| Generator defaults, not established input provenance | `reactor_kinetics.py`, lines 67–93, has time range 0–1 h, temperature defaults 300 K, and initial concentration 1. Its local `theta_pe` dictionary contains A1=84.79085853498033, A2=371.71773413976416, E1=7.777032028026428, E2=15.047135137500822. That dictionary is unused; actual parameters come from the supplied `scena`. The rates multiply activation energies by 1000 with gas constant 8.31446261815324. These defaults do not establish the experiment or sensitivity scaling that generated `Q_drop0.csv`. No corresponding generator driver was located in the inspected tree. |
| Stored selections | `kinetics_results/MILP_<budget>_a` and `kinetics_results/MINLP_<budget>_d`, with corresponding `*_fim_*` files. These were located but not deserialized or checked in this audit. |
| License evidence | No repository-wide LICENSE file was found at the audited commit. `reactor_kinetics.py`, lines 1–49, contains its own copyright notice and redistribution terms with attribution, binary-notice, and non-endorsement conditions. This observation should not be generalized into a license for every repository file. |

The archived sensitivities are sufficient to compare two selection objectives using the same supplied local statistical inputs. Independently regenerating the physical experiment requires resolving the generator and scaling provenance. Matching the code's constraints also requires choosing explicitly between the archived implementation and the paper's description. This audit makes no claim that published selections or reported benchmark performance have been reproduced.

Independent verification is preserved in [the runnable exact-check script](../code/measurement_selection_source_audit.py). The command used was:

```sh
python code/measurement_selection_source_audit.py \
  /tmp/minlp-measurement-source-audit-20260912/measurement-opt/measure_optimize.py
```

The script passed the two rational witnesses, positive definiteness of the kinetics covariance, all 64 selections for Liu's identity and positive semidefinite inflation, and all eight selections of an independent-noise control. With the optional source path, it extracts and executes the two unchanged coefficient-building methods from the inspected author file, supplying only their NumPy dependency. Those methods returned 2.28571428571 for the two-sensor singleton and 1.14285714286 for both sensors, matching \(16/7\) and \(8/7\). No optimization solver or original benchmark run was needed for those checks.

Temporary source files are under `/tmp/minlp-measurement-source-audit-20260912/`; the Liu PDF used was `/tmp/minlp-design-opportunities-20260912/liu2016.pdf`. Source SHA-256 values:

```text
wang-arxiv-v1.pdf  fd98c5af5b865ffca25ab2a39795138e004cccf9bc1d6f18bbb5aaa1a0373978
wang-osti.pdf      7c6b6bb18044097ec4c6acb151db007a3c7831399a6c19ca819a5fcfd23ad6d0
liu2016.pdf        462fc51fe3ed9608af9682d9cd35a099fd1a813b826146e0010826fd06954e22
```

The newer journal manuscript and code permalink were sent to the sole literature maintainer, `/root/literature`. This audit did not modify the literature KB or run its index checks. The unretrieved scholarly artifact is Wang's final typeset version of record; the accepted manuscript and arXiv source were both retrieved. The statistical finding is supported by both available manuscript versions, the public implementation, and independent exact calculations.
