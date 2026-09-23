# Prior-art audit: mobility design before and after observing kinetic defects

Literature audit, 2026-09-07. The result under review is [robust-mobility-design.md](robust-mobility-design.md); its independent correctness review is [review-robust-mobility-design.md](review-robust-mobility-design.md).

## Assessment

No direct match was found for the sharp small-budget laws in the compact cosine-offset ensemble. The potentially original contribution is the pair of exponents and leading constants, with a lower bound over every admissible predetermined mobility field, including fields whose spatial variation changes with the budget. Neither expected-compliance optimization nor the benefit of observing uncertainty before making a design decision is new.

The strongest related mathematics is optimal conductivity under random forcing, where the expected squared state gradient already supplies the design sensitivity. The present work applies that variational structure to a singular random reaction field, constructs localized test fields that produce a sharp uniform lower bound, and compares it with an independently optimized design for each realization. The proof over arbitrary budget-dependent designs is substantially more informative than optimizing a fixed-shape approximation.

## Precise result being compared

On a periodic wall of length `2π`, let

\[
H_{D,c}=-\partial_sD(s)\partial_s+(c+\cos s)^2,
\quad c\sim\mathrm{Uniform}[-2,2],
\quad J_c(D)=\langle1,H_{D,c}^{-1}1\rangle,
\quad D\ge0,\quad\int D=M.
\]

The two decision problems are

\[
\Phi(M)=\inf_D\mathbb E J_c(D),\qquad
\Psi(M)=\mathbb E\inf_DJ_c(D).
\]

The research note proves

\[
\Phi(M)\sim18.3860636501M^{-1/4},\qquad
\Psi(M)\sim22.4046282307M^{-1/5},
\]

with an asymptotically optimal predetermined shape

\[
\frac{D_M(s)}M=
\frac{|\sin s|^{-2/5}}{2B(3/10,1/2)}.
\]

The shape has integrable singularities. Its budget class has no pointwise mobility cap or fixed fabrication length. The ratio is

\[
\Psi(M)/\Phi(M)\sim1.2185657929M^{1/20}\to0.
\]

The optimum chosen in advance improves the uniform-design leading constant by about 4.7%; knowing the defects changes the power. This is a dimensionless small-budget statement. The small exponent `1/20` means that a large practical gain cannot be inferred without evaluating the relevant finite budget.

## The decision framework is established

For any fixed admissible `D`, the pointwise inequality `inf_A J_c(A)≤J_c(D)` immediately yields `Ψ≤Φ` after expectation and minimization. No convexity or Jensen inequality is required. The difference `Φ−Ψ` is the usual expected value of perfect information, measured in the objective's units. It becomes a monetary value only after specifying a cost model. Birge's 1982 paper distinguishes perfect-information comparisons from replacing random data by their mean and studies bounds in stochastic linear programming. [Primary repository record and paper](https://deepblue.lib.umich.edu/items/c11c92bf-3041-4e83-b561-77daa349bc81), [published article](https://doi.org/10.1007/BF01585113).

Conti, Held, Pach, Rumpf and Schultz, *Shape Optimization Under Uncertainty—A Stochastic Programming Perspective* (2009), combine two-stage stochastic programming with shape optimization under stochastic loading. This already places the time at which a design is selected at the center of the model. [Published primary article](https://doi.org/10.1137/070702059), [earlier author presentation](https://www.math.uni-bonn.de/people/dmv2006/minisymposien/20/vortraege/Held.pdf).

Schultz's 2013 Oberwolfach contribution explicitly discusses information availability in PDE-constrained design: a shape selected before the load is observed must not anticipate the realization. It distinguishes that problem from allowing the shape to adjust to the random data. This is a direct conceptual precedent for the blind/adaptive distinction here. It does not state the singular small-budget laws. [Primary report, printed page 285](https://oa.tib.eu/renate/server/api/core/bitstreams/0b429314-4b9e-4a5a-82ee-f7d1013db05d/content).

The current objective is risk-neutral expected response. It is not a worst-case objective and does not constrain variance or failure probabilities. Although the word *robust* is common in this literature, the manuscript should specify the objective rather than relying on that word alone.

## Closest coefficient-design precedent

Buttazzo and Maestre, *Optimal Shape for Elliptic Problems with Random Perturbations* (2010 preprint; 2011 publication), optimize a deterministic elliptic conductivity with lower and upper bounds and an integral budget when the forcing is random. They study expected costs including compliance, relaxation, and numerical designs. Their Theorem 4, equation (16), gives the derivative with respect to conductivity as the negative expected product of state and adjoint gradients. For compliance the adjoint equals the state, giving `−E|∇u|²`. Their budget multiplier therefore balances this expected gradient quantity. [Open paper](https://arxiv.org/pdf/1002.2770), [published article](https://doi.org/10.3934/dcds.2011.31.1115).

This substantially overlaps the general variational architecture of the present proof. It does not have random vanishing killing, a zero-baseline conductivity budget tending to zero, or the stated exponent gap. The new lower-bound argument should be presented as a specific asymptotic certificate within this established optimization framework. It is not a new sensitivity formula or a new general principle of placing conductivity where expected gradients are largest.

Buttazzo, Oudet and Velichkov, *A free boundary problem arising in PDE optimization* (2015), provide the fixed-budget reinforcement and gradient-constraint duality underlying the adaptive local design. Their baseline reinforced membrane differs from the singular reaction problem, but the mass-constrained dual mechanism is already present. [Open paper](https://arxiv.org/pdf/1506.00141). Further overlap with optimal conductivity and cooling-fin design is recorded in [optimal-mobility-placement-prior-art.md](optimal-mobility-placement-prior-art.md).

## Expected compliance and random elliptic input

Dunning and Kim, *Robust topology optimization: Minimization of expected and variance of compliance* (2013), optimize both expected compliance and variance under uncertain load magnitudes, derive analytic sensitivities, and implement the problem through level-set topology optimization. This is an established engineering counterpart to the expectation objective. It does not analyze the present mobility budget or singular reaction field. [Primary institutional record with accepted manuscript](https://researchportal.bath.ac.uk/en/publications/robust-topology-optimization-minimization-of-expected-and-varianc/), [published article](https://doi.org/10.2514/1.J052183).

Martínez-Frutos, Kessler and Periago, *Robust optimal shape design for an elliptic PDE with uncertainty in its input data* (2015), study an elliptic problem whose design enters a lower-order term, with a measure constraint and a mean-plus-variance compliance objective. They derive a relaxation and solve it numerically. This is relevant because uncertain elliptic design is not restricted to conductivity or random forcing in structural models. In their formulation the lower-order coefficient is itself designed; here the killing field is random and conductivity is designed. The available primary description gives no small-budget exponent comparison. [Open primary record](https://www.numdam.org/item/COCV_2015__21_4_901_0/), [published article](https://doi.org/10.1051/cocv/2014049).

These precedents are stronger and more relevant than generic references to machine learning or stochastic optimization algorithms. No statistical learning algorithm is part of the present theorem: the adaptive benchmark assumes exact information without modeling how it is acquired.

## Established calculations versus the specific advance

For a fixed positive shape, the local harmonic-well law and the root-coordinate change of variables reduce the expected response to

\[
C_0M^{-1/4}\int w(s)d(s)^{-1/4}\,ds,
\qquad w(s)=\tfrac14|\sin s|^{-1/2},\quad\int d=1.
\]

The optimizer `d∝w^(4/5)` follows from Hölder's inequality or an elementary Lagrange multiplier. This allocation rule is not independently a strong novelty claim. Likewise, the distinction between an integral of minima and a minimum of an integral is elementary.

The prospective advance is proving that the fixed-shape answer is the actual infimum over unrestricted designs as the budget vanishes. The ensemble of localized dual tests establishes a spatially uniform bound on its expected squared derivative. Combining that bound with the budget rules out a better power or leading constant from narrow peaks, zero-mobility regions, or arbitrarily fast oscillations. The adaptive comparison additionally controls the coalescing-zero layer before taking the disorder expectation. These are the steps on which the exact exponent-gap claim rests.

## An elementary warning about averaging the kinetic field

Replacing the random killing field by its pointwise mean gives

\[
\bar k(s)=\mathbb E(c+\cos s)^2=4/3+\cos^2s\ge4/3.
\]

For this deterministic surrogate, the variational formula gives `J_{\bar k}(D)≤∫1/\bar k≤3π/2` for every nonnegative `D`. Thus it predicts a bounded response even as `M→0`, whereas the true optimized expected response diverges as `M^(-1/4)`. This calculation follows directly from the current model; it is not claimed as a new general theorem. It clarifies that blind optimization uses the full probability law and is not optimization with mean coefficients. Averaging the operator and averaging its inverse are different operations.

## Recommended originality claim and limits

A defensible claim is a sharp small-budget information advantage for an explicit singular transport-design problem: exact knowledge of the random defect locations changes the optimal expected-response exponent from `−1/4` to `−1/5`, while the optimal predetermined shape and its sharp constant can be computed despite an unrestricted mobility budget class.

No exact collision was found in searches on stochastic compliance, optimal reinforcement, conductivity under random loads, random lower-order elliptic terms, nonanticipative shape design, value of perfect information, singular random potentials, and small-budget asymptotics. This is a search outcome, not proof of global originality. The sources above establish the surrounding methods and decision concepts but do not contain the identified operator/ensemble result.

The validated theorem concerns the scalar surface functional and its exactly well-mixed bulk interpretation. A finite-transverse-bulk result still needs a uniform remainder estimate for the selected designs. Fixed mobility caps, finite fabrication resolution, noisy defect measurements, acquisition cost, minimax design, and higher-moment objectives are different problems. They should not be described as consequences of the present result without further analysis.
