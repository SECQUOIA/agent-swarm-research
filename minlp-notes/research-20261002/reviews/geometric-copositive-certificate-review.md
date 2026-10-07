# Independent review of the sparse geometric copositivity certificate

Date: 2026-10-02. Verdict: **pass**. This review read the complete
[author note](../new-direction/geometric-copositive-certificate.md),
including the optional signed-margin search, and inspected its exact
diagnostic source. No substantive correction is required.

The result is scoped to a homogeneous quadratic on the nonnegative
orthant. It is a deterministic, checkable margin certificate, not a
general certificate for nonhomogeneous box optima.

## Every accepted trial proves its own margin

For the mean-preserving endpoint rounding, independent coordinates leave
all cross-term expectations unchanged. Thus arbitrarily large positive
cross coefficients do not enter the rounding loss. On a positive grid
interval, its width is at most \(\delta\) times its lower endpoint,
so \(4\operatorname{Var}(Y_i)\le\delta^2\mathbb E Y_i^2\).
The initial interval contributes at most \(\eta^2\), where
\(\eta=\delta/n\). Their sum gives exactly the stated relative
variance bound.

Apply this bound to \(R=Q-\sigma\|x\|^2\), whose diagonal quadratic
coefficients are at most \(L/2\). With
\(\sigma=L\delta^2/8\), the remaining additive term is
\(Ln\eta^2/8=\sigma/n\). Consequently

\[
 R(x)\ge\mathbb E[Q(Y)-2\sigma\|Y\|^2]-\sigma/n
          \ge m_\delta-\sigma/n=b_\delta.
\]

Normalization by the infinity norm is legitimate because a coordinate
equal to one remains exactly one under rounding. Every rounding outcome
therefore belongs to the normalized grid over which \(m_\delta\) is
computed. Homogeneity proves, for every nonnegative vector,

\[
 Q(x)\ge\sigma\|x\|^2+b_\delta\|x\|_\infty^2.
\]

This is a sound statement even on an unsuccessful trial or a matrix with
negative orthant margin. A positive \(b_\delta\) certifies a positive
Euclidean margin without trusting a growth promise.

## The first-success guarantee is correct

If the true orthant margin is \(g>0\) and \(\sigma\le g/4\),
then \(Q(y)-2\sigma\|y\|^2\ge(g-2\sigma)\|y\|^2\).
Every normalized grid point has squared Euclidean norm at least one.
Hence \(b_\delta\ge g-(2+1/n)\sigma\ge g/4>0\).

A failed predecessor has parameter \(4\sigma>g/4\), giving
\(\sigma>g/16\) at the first later success. At an initial success,
\(\sigma=L/32\ge g/16\), since \(g\le L/2\).
The accepted certificate itself gives
\(g\ge\sigma+b_\delta/n>\sigma\). These arguments establish the
complete factor-sixteen statement, including the one-variable case.

The algorithm need not know \(g\). Strict positivity guarantees
termination after \(O(1+\log(L/g))\) trials; a failed finite trial is
inconclusive. The statement does not claim termination at zero margin.

## One DP suffices and the rational size is FPT

Running intersection makes the highest bag containing each variable
unique. Counting the event “value equals one” only at that owner gives
an exact two-state OR summary of each subtree. Conditional on a bag
assignment, combining child states one at a time costs a constant
number of operations per child. Arbitrary branching therefore introduces
no exponential child-count factor and no need for separate anchored
problems. All quadratic terms and corrections are assigned exactly once.

Checking the complete message minima verifies the normalized grid optimum;
it is not enough merely to trust a returned minimizing assignment. The
verifier must also validate the decomposition, factor assignments, grid,
and all message states. These are finite rational checks of the stated
size. A negative-witness DP can backtrack a globally consistent grid
assignment by the same recurrences.

At first success, \(\delta^{-1}\le\sqrt{2L/g}\). The grid has
\(O(\sqrt{\kappa}\log(2n\sqrt{\kappa}))\) nodes. Its \(p\)-th
power has the claimed fixed-parameter bound because
\((\log(2n))^p\) is bounded by a function of \(p\) times \(n\).
Summing over bags, children, and earlier trials preserves an absolute
input exponent.

The rational-node formula and common denominator in the note are valid.
One may use a common denominator for the input matrix, a common grid
denominator, and the dyadic correction denominator for all local entries.
Every finite message is a sum of assigned terms evaluated at grid nodes;
taking minima does not multiply denominators. The bit length is bounded
by the input length and \(O(rK+\log n+\log N)\), up to polynomial
factors. Thus the arithmetic bound extends to
\(f_1(p,\kappa)\operatorname{poly}(I)\) bit work and certificate size.
Large input coefficients still cost their encoding length.

## The optional negative-witness search is sound

On positive grid intervals, the stronger bound
\(4\operatorname{Var}(Y_i)\le\delta^2x_i^2\) holds because the
lower endpoint is at most \(x_i\). It gives
\(\mathbb E Q(Y)\le Q(x)+\sigma\|x\|^2+\sigma/n\).
Rescaling a negative unit-sphere minimizer to the normalized shell and
using \(\|x\|^2\ge1\) proves a negative grid value whenever
\(\sigma\le |g|/4\). The sign reversal in this step is handled
correctly: \(g+\sigma<0\).

The corrected and uncorrected DPs therefore give the stated two-sided
termination bound for \(g\ne0\), with parameter
\(\max(1,L/|g|)\). A small ratio is handled by the initial trial.
Neither branch can report an incorrect conclusion, and no claim is made
for general boundary-copositive matrices.

When \(L=0\), all diagonal quadratic coefficients are nonpositive.
Independent endpoint rounding cannot increase expected objective and
preserves a coordinate equal to one. Normalized endpoint DP consequently
decides copositivity exactly by homogeneity. A zero diagonal disproves
strict copositivity, but is correctly distinguished from a negative
noncopositivity witness.

## Diagnostics and interpretation

The author ran the exact checker and reports six positive fixtures, ten
positive trials, 39,908 bag assignments, ten positive brute-force
comparisons, 1,330 interval checks, six boundary/negative checks, and four
refined negative-witness trials. This review inspected the source rather
than rerunning that command. It implements owned-variable OR convolution,
compares small grid optima with exhaustive enumeration, and checks an
enumerated negative witness against the DP optimum exactly. The branching
and large-cross-term fixtures test distinct parts of the claimed mechanism.

The Horn perturbation accepts the first trial with the displayed positive
margin. This is consistent with its absence of an unmultiplied box
preordering identity: the finite DP plus rounding proof is a different
certificate family. The result does not supply arbitrary tangent-cone,
nonhomogeneous, or general mixed-constraint certificates.

The derivation is a short, parameter-sensitive specialization of corrected
geometric grids, homogeneity, and standard tree DP. Its verified unknown
margin and sparse dependence are the substantive claims to compare with
prior art; this review establishes no priority.

A scoped inline Python check passed whitespace, mathematical delimiters,
and local links. No additional delegation, external search, executable
solver test, project-wide verification, or CI inspection was performed.
