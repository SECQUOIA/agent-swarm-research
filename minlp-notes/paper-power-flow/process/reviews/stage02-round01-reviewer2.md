# Stage 2, round 1 — independent reviewer 2

Verdict: **PASS. No major or minor issue requiring correction identified.**

I independently reviewed the frozen stage-2 manuscript and new exact checker, with the scaffold, bibliography, README, process and coverage records, and relevant accepted stage-1 dependencies. I did not read other reviewers' reports or change manuscript inputs. The findings below concern the actual stated models; neither fixed positive principal windows on arbitrary graphs nor symmetric tolerance robustness is claimed, so those are not missing proofs.

## Mathematical and encoding audit

1. **Model and rectangular equations (`sections/03-ac.tex:11–61`).** The complex-power convention gives exactly the stated signs for both real and reactive injections, including shunts and arbitrary signed line susceptance. The auxiliary positive magnitude variable makes `H >= c r_i r_j` valid without squaring, including negative cosine inputs. The source restriction `c > -1` excludes precisely the antipodal ambiguity relevant to the argument. Allowing `c = 1` causes no problem: all permitted differences are zero. The rational input and real-angle semantics are explicit, and no trigonometric constant is treated as rational input.

2. **Crossing count and axes (`lem:crossing`).** The sign of `D_ij` is consistent with the traversal `j -> i`. I checked both strict-wrap cases and all real-axis cases. In the first case, `f_j < 0 <= f_i` implies `alpha_j` lies in `(pi,2pi)` and `alpha_i` in `[0,pi]`; the determinant then selects the positive-ray rather than negative-ray crossing exactly. The reverse case has the opposite sign. Collinear same-direction phasors have zero determinant and zero crossing; opposite directions are excluded. Unequal radii preserve all relevant signs. The identity relating the principal difference to the arguments and `2 pi k` is correct across the entire interval `(-pi,pi)`.

3. **Lift and Turing membership (`lem:lift`, `thm:ac-membership`).** The chosen principal differences form an exact real edge potential precisely when their cycle sums vanish. A fundamental cycle for every non-tree edge suffices, independently for each connected component. Tree propagation genuinely represents the given phasors. Necessity uses the strict `pi` bound in the correct place. Encoding each three-valued crossing variable by a Boolean formula over polynomial comparisons is allowed in ETR and adds no integer quantifier. There are polynomially many variables and explicitly written cycle terms. All rational coefficient encodings remain polynomial. A root angle used in the conceptual lift need not appear as a transcendental constant in the existential formula.

4. **Equal angles and the transfer (`lem:equal-angles`, `thm:ac-complete`).** Pairing the two endpoint contributions gives the displayed energy identity with the correct sign. Positive conductances and magnitudes make each nonzero real line difference strictly costly for absolute difference below `pi`. Thus every difference vanishes. This is valid without positive cosines and without stability assumptions, but crucially requires the real lift. The chosen hard subclass has strictly positive conductances, no shunts, and zero reactive injections, satisfying every hypothesis. The converse and the fixed-data restriction follow immediately from the resistive theorem.

5. **One-sided reactive intervals (`cor:one-sided-reactive`).** Purely resistive reciprocal lines have identically zero total reactive injection. Common-sign reactive injections therefore vanish individually. Replacing all `[0,0]` intervals by `[0,1]` preserves the entire feasible set for each restricted transfer. The text correctly distinguishes this algebraic saturation from robustness to signed residuals. General shunts/susceptances are not silently included in this argument.

6. **Winding counterexample (`prop:winding-counterexample`).** The uniform cycle profile has the stated injections for every `n >= 3`, its signed principal differences sum to `2 pi`, and rational bounds around the positive active power exist. The proof does not require its generally irrational active powers to be input numbers. For each fixed rational `c < 1`, a sufficiently long cycle fits the principal window. With unit magnitudes the resistive injections are all zero, hence infeasible for the positive bounds. The explicit four-cycle has fully rational singleton data. The two-bus antipodal example also correctly shows why the equal-angle lemma needs the strict `pi` bound.

7. **Small cycle budgets and size-dependent positive windows (`lem:small-cycle-budget`, `cor:principal-hardness`).** The cycle sum is an integer multiple of `2 pi`, so the strict budget makes it zero. The elementary sine bound yields `gamma_n <= pi/(sqrt(2)n)` and consequently a strict budget for every simple cycle. The rational cosine `1 - 1/n^2` has logarithmic bit length and defines a strictly positive window. Padding with isolated buses is feasible and stays within the original data alphabet. The manuscript explicitly exempts these varying cosines from its fixed-finite-data conclusion.

8. **Rectangular boxes (`cor:box-hardness`).** The two linear inequalities and the positive lower magnitude bound force `e_i > 0` and exactly the specified `[-pi/4,pi/4]` angle choice. Each line difference is at most `pi/2`. Equal angles and the component reference therefore force all imaginary coordinates to zero. Both directions of the exact feasible-set identification hold, including isolated buses.

The abstract reflects the results actually proved, including the limitations of principal windows and the verifier condition in the certificate consequence. The accepted stage-1 homeomorphism direction is now consistent. I found the proofs readable and their endpoint assumptions explicit.

## Primary-source support

I checked the newly cited primary source, [Dörfler, Chertkov, and Bullo, arXiv:1208.0045v1](https://arxiv.org/html/1208.0045v1), particularly equation (1) and the cohesive-phase discussion. Its weighted sine equilibrium supports the limited background attribution in this draft. The manuscript supplies its own energy proof and does not import a broader uniqueness or stability theorem from that source. The arXiv landing page also links the stated PNAS DOI. The foundational ETR-INV dependency was verified against the archived original during stage 1 and is unchanged here.

## Independent verification and build

Artifacts are confined to `verification/reviewer2/stage02-round01/`:

- `check_independent.py`, `independent.log`: exact SymPy expansion of arbitrary real rectangular phasors, arbitrary line parameters, and shunts; all real/reactive signs agree. Separately, 80-digit `atan2` checks confirm the crossing identity on 16,828 pairs drawn from 130 rational unit directions, including 7,246 obtuse pairs and 514 pairs incident to the real axis. Direct analytic tree propagation agrees with the two fundamental-cycle equations for 2,923 non-antipodal graph profiles, including 1,834 liftable profiles. This code does not import the author checker. The high-precision finite checks are supplementary numerical evidence, not exact proof certificates.
- `author-check.log`: the frozen standard-library checker passes its exact pair, cycle, power-sign, and balance regressions.
- `build.log`, `build/main.pdf`: independent successful `latexmk` build in the reviewer-owned output directory. The final LaTeX log has no warnings about unresolved references/citations or overfull/underfull boxes.

All twelve frozen manifest hashes were verified after review. No optional extension is necessary to close this stage.
