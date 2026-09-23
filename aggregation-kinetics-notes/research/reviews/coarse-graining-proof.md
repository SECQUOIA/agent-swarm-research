# Independent proof review: exact particle-coordinate coarse graining

Date: 2026-09-06. Reviewer: `/root/closure_direction/review_rigidity`.

Reviewed document: [Exact latent coordinates for additive coagulation](../ideas/coarse-graining.md), including Lemma 1, Theorems 2–6, the state-dependent fragmentation extension, and the examples. This report records an independent mathematical review of the version read on this date. It is not a publication or a certification of novelty.

## Conclusion

The proofs and constants in Theorems 2–6 are correct under the stated hypotheses, interpreted in the natural measure-ODE solution class described below. I found no mathematical counterexample or substantive proof gap. I independently reconstructed the event-polarization argument, tangent-kernel rigidity, minimum-dimension construction, fragmentation invariance argument, bounded-Lipschitz upper bound, and uniform small-rate lower bound before reading the assembled manuscript.

The strongest candidate contribution is the restriction on **every smooth, everywhere submersive particle-coordinate encoder** imposed by additive coagulation. The invariant-subspace calculation and measure-stability tools have substantial prior art. The review does not establish that the specialized rigidity and dimension theorems are absent from the literature.

## Scope and assumptions actually checked

- Particle states lie in the open convex cone (C=(0,\infty)^m), and coagulation adds states.
- The kernel is symmetric and strictly positive. The gradient formulas additionally require (C^1) regularity. Uniform upper and lower bounds are required only in the quantitative sections.
- Exactness means closure for every finite nonnegative atomic population measure, with arbitrary positive population masses. It is not closure only for probability measures or a selected initial family.
- The encoder is (C^1), maps into (\mathbb R^d), and has rank (d) everywhere. Dimension zero is allowed. Connected fibers are used only for global injectivity of the coordinate reparametrization.
- A retained observable is a (C^1) particle function whose value factors through the encoder; differentiability of its factor is unnecessary for the lower-bound argument.
- Binary fragmentation has daughters (Rx,(I-R)x), where (R=\operatorname{diag}(r_i)), (0<r_i<1). Its rate is a strictly positive constant in Theorem 4 and a constant (a\ge0) in the quantitative comparisons.
- In Theorem 5, the initial measure is finite and nonnegative with finite first total-size moment. The scalar approximation uses (0<\bar r<1). The size metric has fixed units or is nondimensionalized.
- For the bounded-kernel existence statements, kernels are understood to be Borel measurable. This follows from the earlier (C^1) assumptions; if Theorem 6 is read independently as dropping all regularity except boundedness, measurability should remain explicit. Symmetry is also retained.

## Lemma 1 and Theorem 2: closure and rigidity

For atomic inputs, polarization gives the exact cross coefficient

\[
Q(\delta_x+\delta_y)-Q(\delta_x)-Q(\delta_y)
=K(x,y)(\delta_{x+y}-\delta_x-\delta_y).
\]

Replacing either parent by a point in the same encoder fiber preserves the pushforward of this expression. Its total mass is (-K(x,y)), so the kernel itself must agree. Strict positivity then permits division, and the identical death atoms cancel. This proves that the offspring encoder value also agrees. Repeated atoms cause no exception: the polarization identity remains valid when (x=y).

For any (w\in\ker Dh(x)), the submersion theorem supplies a local curve through (x) in its encoder fiber with tangent (w). Translating that curve by any (y\in C) preserves its encoder value by the offspring congruence. Thus

\[
\ker Dh(x)\subseteq\ker Dh(x+y).
\]

Equal dimensions turn inclusion into equality. Any two positive vectors have a common strict coordinatewise upper bound, so all tangent kernels equal a fixed (W). This is the central step: closure supplies invariance under every positive translation, rather than only under a single dynamical vector field.

The factorization (h=g\circ A), (\ker A=W), is global because every affine (A)-fiber intersected with (C) is convex. Integrating (Dh) along a segment establishes constancy on the entire intersection. Local linear sections of (A) give (C^1) regularity of (g), and its derivative is invertible. A local diffeomorphism has discrete point fibers, so connected (h)-fibers force (g) to be injective.

The periodic example in the manuscript is valid: (e^{x_1}(\cos x_2,\sin x_2)) has rank two, ignores (x_3), and respects addition through complex multiplication. Its fibers can be unions of separated parallel components. Thus one must not remove the connected-fiber qualification or infer that an arbitrary noninjective local diffeomorphism gives a valid encoder. Any additional global identifications must themselves respect the event rules.

## Theorem 3: sharp minimum dimension

For an exact encoder, all kernel gradients and retained-observable gradients annihilate (W); hence (V\subseteq W^\perp) and (d\ge\dim V). This is a global gradient span, not a rank test at one particle state.

For the converse, choose (A) with row space (V). Along each affine (A)-fiber, integrating the relevant gradients makes (K) constant in its first argument. Symmetry supplies constancy in the second argument. The same argument retains each specified observable, and linearity gives (A(x+y)=Ax+Ay). The construction therefore reaches the lower bound.

The zero-dimensional case is legitimate: a constant kernel with no retained particle observables closes on particle number alone. The positive-dimension convention in the manuscript is also correct when (m\ge1).

Both examples check out. For (f(x)=\prod_i x_i), the vectors (\nabla f(x)) span all of (\mathbb R^m), despite the separated kernel rank being two. Replacing (f) by (f/(1+f)) multiplies each gradient by a strictly positive scalar and preserves its global span. For a total-size kernel with one-dimensional nonzero gradient span, the total-size projection attains dimension one.

## Theorem 4 and the rate extension

Scaling a closure comparison by every (c>0) gives an identity of the form (c^2\Delta Q+c\Delta F=0). It forces both coefficients to vanish. This separation depends on arbitrary population masses and does not follow merely from testing normalized probabilities.

Once coagulation supplies (W), the short straight fiber (x+tw), (w\in W), has a fixed projected two-atom offspring measure under fragmentation. Each continuous child-encoder curve takes values in the fixed finite support of that measure and must therefore be constant. Differentiating gives (Rw\in W). Unordered daughter labels and coincident daughters do not create exceptions. Neither does a globally noninjective (g).

The equivalent condition is (R^T W^\perp\subseteq W^\perp). Cayley–Hamilton proves that the displayed span through power (m-1) is the smallest invariant subspace containing (V). Conversely, its row space gives (AR=BA), so both projected daughters are functions of the projected parent. This proves the claimed minimum.

For the bounded total-size example, distinct (r_i) give full rank by the Vandermonde determinant. With exactly (\ell) distinct fractions, the Krylov span has dimension (\ell), and the group-total construction attains it.

The state-dependent-rate extension is valid. The total number change of a single-parent fragmentation event is (a(x)), identifying that rate on encoder fibers. Strict positivity then allows the same offspring argument. Including all (\nabla a(x)) in the starting span is both necessary and sufficient.

## Theorem 5: existence and the finite-time upper bound

The weighted-total-variation proof is sufficient for unique global solutions in the Banach-ODE class: continuous, and in fact (C^1), paths with norm (\int(1+s)\,d|\mu|). Bounded (K) makes the coagulation bilinear operator bounded on this space; the fragmentation operator is bounded linear. The gain-loss form preserves nonnegativity. Since the mass functional is bounded on the weighted space, its exact eventwise cancellation proves conservation without an unbounded-test-function interchange. Particle number obeys the stated logistic differential inequality. The bound on number plus conservation of mass prevents blowup of the weighted norm. This establishes the natural solution notion used in the proof; it should not be read as an additional assertion about unspecified, less regular weak-solution classes.

I checked the constants:

\[
N_* = \max(N_0,2a/k_-),\qquad
C_\kappa=\max(3k_+,3L_\kappa+2k_+),\qquad
L=C_\kappa N_*+3a.
\]

For a BL-unit test function, the coagulation event bracket has supremum at most three and Lipschitz constant at most two in either parent. Multiplication by the kernel gives exactly the displayed (C_\kappa). Polarization contributes ((N_\lambda+N_\nu)/2), so there is no missing factor of two in (C_\kappa N_*).

The scalar fragmentation adjoint has supremum at most (3a) and Lipschitz constant at most (2a), hence BL operator norm at most (3a). The hidden-composition residual is bounded by (2a\delta s(x)) per particle, and thus by (2a\delta M_1) after integration. Applying the integral inequality yields precisely

\[
\|\lambda_t-\nu_t\|_{\mathrm{BL}^*}
\le 2a\delta M_1\frac{e^{Lt}-1}{L}.
\]

There is no total-variation/BL mismatch: the proof uses total variation for existence and BL estimates for the error. The result controls bounded Lipschitz observations, not arbitrary unbounded tail moments. The midpoint choice of (\bar r) minimizes the displayed worst component deviation. The estimate has uniform order (a\delta) on fixed time intervals for bounded rate ranges; its exponential constant is not a long-time sharpness claim.

## Theorem 6: a uniform lower bound as the rate vanishes

I independently obtained the manuscript's constants

\[
\widehat N=\max(1,2a_0/k_-),\quad
B=\tfrac32k_+\widehat N^2+3a_0\widehat N,
\quad L_Q=3k_+\widehat N,
\]
\[
C_T=3\widehat N L_Qe^{L_QT}+3B.
\]

The bound (B) follows from the TV norms of one coagulation event, at most three, and one fragmentation event, at most three. Projected differences start at zero. Their forcing has TV norm at most (6a\widehat N), while their coagulation term is TV-Lipschitz with constant (L_Q). This gives the stated first Grönwall bound. Its time integral contributes at most (3a\widehat N L_Q e^{L_QT}t^2). Subtracting the initial fragmentation derivative contributes at most (3aBt^2). Both bounds hold uniformly for (0\le a\le a_0), including (a=0).

The triangle inequality then gives the minimax lower bound for any deterministic predictor supplied with identical initial observed data and parameters. A predictor with internally generated memory is covered. A predictor receiving additional composition-dependent measurements or a subsequently observed trajectory is not supplied identical information and is outside this assertion.

The witness in the manuscript has (D=1/2) and therefore gives the stated lower bound (at/8). More generally, writing (p=r^Tx), (q=r^Tx'), and (z=s(x)=s(x')), one can verify the exact identity

\[
D=2\min\!\left(2,\left||p-z/2|-|q-z/2|\right|\right).
\]

To prove it, sort each symmetric daughter pair around (z/2). Corresponding atoms are separated by the common distance (h=\left||p-z/2|-|q-z/2|\right|), giving the upper bound (2\min(h,2)). The admissible test function (\phi(u)=\min(1,\operatorname{dist}(u,\{q,z-q\})-1)) attains it. Thus (D>0) precisely when the unordered daughter pairs differ. When (D=0), the displayed lower bound is valid but uninformative.

## Novelty limitations and remaining diligence

The following distinctions are essential to a publication claim:

- Eventwise closure is related to strong lumpability and is not independently new.
- General nonlinear lumpability and tangent-kernel invariance predate this work. The proposed distinction is the derivation of invariance under every positive translation, which forces a fixed tangent kernel for these particle-coordinate encoders.
- Minimal invariant-subspace constructions are established tools. [CLUE](https://academic.oup.com/bioinformatics/article/37/12/1732/6126795) explicitly treats constrained linear lumping of polynomial ODEs. The present lower bound must be presented as applying against all smooth submersive particle-coordinate encoders, not as a new invariant-subspace algorithm.
- A directly adjacent source is [A new efficient framework for reduced two-dimensional nonlinear aggregation population balance models](https://www.sciencedirect.com/science/article/pii/S000925092601599X). I surfaced this paper in the independent search but did not inspect its full text. Its possible overlap requires further review.
- BL stability and Grönwall arguments are established machinery. The useful proposed combination is the explicit composition residual, the uniform lower bound, and their relation to discontinuous exact dimension.

Independent web searches on 2026-09-06 included “exact lumping aggregation fragmentation population balance multicomponent lumpability”, “Smoluchowski coagulation equation dimensionality reduction exact projection multicomponent aggregation fragmentation”, “coagulation lumping”, “nonlinear lumping linear invariant subspace differential equations”, and “exact reduction multicomponent coagulation kernel”. They did not reveal a direct match to the complete rigidity and sharp-dimension statement. This limited search is not proof of absence. The manuscript records a broader literature audit by its author; that audit is not independently certified by this proof review.

No numerical experiment is needed to establish these analytical arguments. An atomic consistency check and a rank calculation can still help detect transcription errors. They should be recorded as implementation checks, not substituted for the proofs above.

## Subsequent prior-art correction

Later on 2026-09-06, the team found Hofmann–Ruppert, *The Foliation of Semigroups by Congruence Classes* (1988). I independently checked Proposition 16, Corollary 19, and Theorem 21 against the full text and inspected the PDF statement of Theorem 21. These results imply the general gradient-span and diagonal-fragmentation minimum formulas even for arbitrary continuous encoders. The detailed argument is recorded in the [1988 theorem addendum to the continuous-encoder review](coarse-graining-continuous-review.md#addendum-direct-consequence-of-hofmannruppert-1988).

This discovery supersedes the earlier limited novelty assessment in this report. The mathematical verification remains valid, but the core rigidity and dimension conclusions should now be treated as applications or corollaries of established semigroup theory, rather than as independently novel structural theorems. The explicit quantitative bounds require their own prior-art assessment.
