# Adversarial review of certified inexact regridding oracles

Date: 2026-10-02. Reviewed:
[inexact-oracles.md](../regridded-certificates/inexact-oracles.md),
its [base theorem](../regridded-certificates/note.md), and the relevant
certificate definition and unfolding lemma in
[decomposition-certificates.md](../../research-20260929/theory-decomposition/decomposition-certificates.md).

The inexact-oracle extension passes this review. Its local lower bounds
remain valid, backtracking pays one local gap per bag, approximate slopes
give the stated perturbation bound, and the \(1/7\) contraction and final
gap constants are correct. The rational reconstruction argument preserves
feasibility on touching faces. These conclusions use the stated certified
oracle inequalities; they do not presume exact local values, exact local
minimizers, or efficient generic convex oracles.

## 1. Local certification remains valid

At a fixed stage, regard the approximate slopes and computed rational child
intercepts as fixed data. For every local problem, the oracle requirement
is

\[
\ell\le\min_C q,\qquad q(v)\le u\le\ell+\delta,
\qquad v\in C.
\]

The first inequality proves the local certificate condition over the
entire domain, regardless of whether the stored point minimizes \(q\).
Taking the minimum of certified lower bounds over leaves supplies a valid
cell intercept. The minimum child intercept over intersecting cells gives
the required affine child minorant because the same slope is used on all
of that child's cells. The original bottom-up validity proof therefore
applies to these nonmaximal intercepts.

This argument requires lower bounds for the actual local objective in
the note, including its chosen relaxation models and approximate slopes.
Uncertified solver objectives or primal values alone would not suffice.
The note explicitly requires the needed inequalities.

Inherited intercepts are exact rational numbers once reported. Adding or
removing their sum from a numerical local objective does not consume an
additional uncertainty budget when that translation is done exactly.

## 2. The error sum is exactly one residual per bag

There is a direct identity behind the induction. Along the stored
backtracked choices, write \(\ell_t\) for the selected local lower
bound and \(z^t\) for its feasible oracle point. For each nonroot bag,

\[
\ell_t=\widehat\beta_{t,D_t}
       =b_{t,B_{p(t)}},
\]

because the child cell and then its attaining leaf were selected by their
reported lower bounds. At the root, \(\ell_r=\mathrm{LB}\).
Expanding the local objectives and cancelling these intercepts gives

\[
\widehat\Phi-\mathrm{LB}
 =\sum_t\bigl(q_t(z^t)-\ell_t\bigr).
\]

Every summand lies in \([0,\delta_{t,j}]\) by the certified oracle
inequalities. Hence

\[
0\le\widehat\Phi-\mathrm{LB}
\le\sum_t\delta_{t,j}\le dNh_j^2.
\]

No exact evaluation of any \(q_t(z^t)\) is needed to establish this
identity and bound: its value is enclosed by the oracle interval. An
unselected local task can change which lower bound wins, but it does not
appear in the selected configuration's residual sum. Errors already
present in child intercepts are included through the same cancellation
and must not be charged again. This verifies the central claim that
accuracy need not be divided by the number of solved leaf-cell pairs.

The selected configuration satisfies the original configuration
conditions. A child cell only needs to meet the parent leaf's separator
projection; it need not contain the parent's selected point. The common
child slope and the intercept minimum make precisely this weaker
compatibility sufficient.

## 3. Approximate slopes and gradient incidence

The slope calculation was also checked independently by a delegated
reviewer. For each edge, a coordinate copy difference is at most the
parent leaf width plus the child separator-cell width. Each parent
coordinate occurs in at most \(k-1\) additional child bags. Therefore

\[
H\le2p(k-1)\sum_t b_t^2+2p\sum_{t\ne r}d_t^2
 \le C_1Q.
\]

This counts coordinate incidences, so it introduces no maximum branching
factor. Cauchy--Schwarz then gives
\(|\widehat\Phi-\Phi|\le\nu\sqrt{C_1Q}\).
Combining the stated grading bound with
\(\nu\le\zeta\sqrt N h_j\) produces a constant term
\(\sqrt{12C_1}\zeta Nh_j^2\) and a cross term
\(\sqrt{12kC_1}\zeta\theta\sqrt N h_jR\).
Young's inequality with budget \(\eta R^2/4\) gives exactly

\[
K_s=\sqrt{12C_1}\zeta+
          12kC_1\zeta^2\theta^2/\eta.
\]

The bag-gradient-to-slope estimate is also correct. For one coordinate,
the subtree-sum matrix has one entry for each descendant below an
occurrence-tree edge. Its squared Frobenius norm is the sum of occurrence
depths, at most \(k(k-1)/2\). Applying that norm bound coordinate by
coordinate establishes the proposed constant \(G\).

For \(k=1\), all separators are empty, so the actual slope errors and
copy differences vanish. The formulas correctly require no gradient
accuracy in that case. Exact summation of rational gradient approximations
avoids a separate summation-error term; other summation errors must enter
the stated aggregate slope budget.

## 4. Contraction and the certified incumbent gap

Combining the base estimate, the slope perturbation, and the local
residual sum gives

\[
F(x^{(j)})-\mathrm{LB}_j
\le\frac g{16}\|x^{(j)}-x^{(j-1)}\|^2
 +(C+K_s+d)Nh_j^2,
\]

because \(\eta+\eta/4=g/16\). Quadratic growth and
\(\|x^{(j)}-x^{(j-1)}\|^2\le2(e_j+e_{j-1})\) give

\[
e_j\le e_{j-1}/7+\frac{8K}{7g}Nh_j^2
\]

with the larger \(K=C+K_s+d+\omega\). The inclusion of incumbent
evaluation error in this distance constant is conservative and valid.
The choice \(B_{\rm in}\ge8K/(3g)\) closes the halved-width induction:
\(4B_{\rm in}/7+8K/(7g)\le B_{\rm in}\).
The initial bound \(e_{-1}\le pNh_0^2\), together with
\(B_{\rm in}\ge p\), also proves the stage-zero case.

The maintained incumbent must be the minimum of certified feasible upper
values, associated with their feasible points. Such a value never falls
below \(f^*\). At the current stage it is at most
\(F(x^{(j)})+\omega Nh_j^2\), so

\[
0\le\mathrm{UBD}-\mathrm{LB}_j
\le(5gB_{\rm in}/8+K)Nh_j^2
\le gB_{\rm in}Nh_j^2.
\]

Thus objective-evaluation uncertainty is paid once through \(\omega\);
it is not silently replaced by an exact incumbent value. The stated
termination horizon follows. Unknown-constant trials still stop only on
valid certificates and terminate under the note's assumption that every
requested certified oracle call terminates.

## 5. Touching faces and objective uncertainty after reconstruction

Each local domain is an intersection of rational boxes. Exact endpoint
comparison determines emptiness and identifies coordinates fixed by a
touching face. Fixing those coordinates to their exact rational values
before solving prevents a tolerance-feasible point from being accepted
outside the face. Exact coordinatewise clipping of a rational vector also
gives genuine feasibility. Taking each consistent coordinate from its top
bag preserves rationality and membership in the original product box.

Feasibility alone does not preserve the objective-gap certificate. The
note correctly requires certification of the final reconstructed point
and acceptance only when the complete oracle inequalities hold. This
requirement accounts for objective interval uncertainty after rounding.

For an explicit Lipschitz-based implementation, the sufficient recipe can
be stated entirely with upper bounds: start with a certified value
\(u_0\ge q(v_0)\) satisfying
\(u_0-\ell\le\delta/2\). Transport that upper bound to a feasible
rational reconstruction \(v\) using a certified upper bound on
\(L_q\|v-v_0\|\), and require their sum to be at most
\(\ell+\delta\). The displayed coordinate-displacement condition
provides the proposed half-budget when interpreted with certified bounds.
If the reconstructed objective is freshly evaluated instead, its
evaluation uncertainty must fit the remaining slack. An unknown true
objective inequality alone is not a certified starting upper bound.

The author incorporated this clarification, and the reviewer checked the
revised Section 7. It now requires the certified starting upper value,
uses a rational \(K_q\ge L_q\sqrt p\) to transport that bound, and
explicitly budgets any fresh evaluation uncertainty. The zero-Lipschitz
case is handled separately. No reconstruction qualification remains
unresolved. No Lipschitz modulus is inferred from convexity or the
relaxation-error assumption; the note correctly makes it optional and
otherwise requires direct final certification. Zero tolerances can demand
exact oracles, whereas fixed positive budgets suffice for the inexact
extension.

## 6. Counts, limitations, and verification

The partitions and touching-pair lists are unchanged, so the stated box
and local-convex-call counts carry over. All work needed inside one
certified call, including reconstruction and final value certification,
belongs to that call's internal cost. The note expressly does not turn
the call count into a generic bit-complexity guarantee. It also correctly
distinguishes its leaf-plus-cell certificate measure from the number and
size of serialized local lower-bound proofs.

Verification consisted of algebraic inspection using targeted `cat`,
`rg -n`, and `sed -n` reads of the three files linked above. A delegated
reviewer independently checked the slope, incidence, contraction, and
gap constants. No executable checks, external research, project-wide
verification, or CI inspection were performed.
