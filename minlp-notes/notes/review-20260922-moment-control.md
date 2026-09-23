# Independent closeout review: separator moments in control

Date: 2026-09-22. Reviewed
[the control note](research-20260922-moment-control.md),
[the preceding novelty screen](research-20260922-separator-novelty.md), and
the exact small-degree checker. This review closes the existing topic; it
does not initiate the proposed extensions at the ends of those notes.

**Assessment.** The two propositions and the incremental-stability extension
are correct under the intended finite-dimensional, compact metric action
model. I found no substantive proof gap. Preserve the result as a reviewed
supporting synthesis and a useful fixed-data obstruction, not as an
established original approximation theorem or a solver complexity result.
Three statement clarifications are advisable: specify compact metric action
spaces; define the normalized objective as total cost divided by the number
of stages; restrict the displayed Jackson bound to positive degree.

## Exact gap and its scope

I independently reconstructed the factor of two in Proposition 1. For
compact metric X and finite-dimensional V containing constants, V is closed
in C(X). If E is the distance of f to V and E>0, the quotient norm has a
norming functional. Pullback and Riesz representation give a signed measure
of total variation one annihilating V. Its positive and negative parts have
equal mass one half because it annihilates constants. Their doubles are
probability measures with matching V moments and expectation difference 2E.
The converse bound follows by subtracting any approximant. Weak-star
compactness gives attainment. The E=0 case is immediate. There is no
unjustified interchange of an infimum and a supremum.

For the two-stage model, minimizing h conditionally gives h=|u|, and choosing
the binary sign conditionally gives -zx=-|x|. Both selections are measurable
and feasible. Conversely, every pair of state measures in equation (2)
lifts this way to local feasible measures. Thus the reduction loses no
constraints and has the stated sign: the relaxation value is -2E_k(|x|).
The true optimum is zero. Degree zero is covered too: E_0=1/2 and the
relaxation value is -1. The k=1,2,3 witnesses and the quadratic error identity
are correct. The asymptotic rate comes from Bernstein's theorem, not those
finite checks.

The fixed-data claim is sound: neither the action triangle, two sign modes,
nor the affine reset maps depend on degree. Their contraction factor is zero.
Smooth local data therefore do not preclude a kink in the eliminated value
function. However, matching |x|, sharing a suitable extra graph variable, or
substitution can remove the example. It does not establish a lower bound
against adaptive arbitrary features or general MINLP solution methods.

## Gluing, feasible replay, and objective bounds

The local records and separator couplings form a chain. On compact metric
spaces, regular conditional probability kernels exist. Alternating their
kernels constructs a joint law with every supplied local marginal and every
chosen separator coupling. No compatibility condition beyond the stated
shared marginals is missing. Equal automaton states are joined exactly, so
the sampled action word starts correctly and ends in an accepting state.

Replaying that word from the true initial continuous state is feasible
because every chosen action is allowed independently of the continuous
state, and every transition maps X into X. These are essential assumptions,
not consequences of contraction. For example, under the state-dependent
constraint a=x, an action legal at a sampled local state epsilon need not
be legal at the repaired state zero, however small epsilon is.

The recurrence is indexed correctly. At separator t+1,

\[
 e_{t+1}\le \rho e_t+\Delta_{t+1},\qquad
 e_t\le\sum_{s=1}^{t}\rho^{t-s}\Delta_s.
\]

It is needed only through t=T-1. Bounding each cost difference by L_t e_t
and taking expectations proves equation (7). All costs are bounded under
the compactness and continuity assumptions. A feasible deterministic
trajectory with cost no greater than the displayed bound exists because
the repaired random cost has expectation no greater than that bound.

Automaton disaggregation introduces no multiplicative state-count factor.
For each positive-mass q, conditional feature moments agree, hence its
conditional Wasserstein discrepancy is at most 2A(V,X). Multiplying by
the common q mass and summing gives the same bound. Matching only
unconditional continuous moments would not suffice: distributions putting
mass one half at (q_A,-1),(q_B,1), versus (q_A,1),(q_B,-1), have identical
unconditional moments of every degree but automaton-preserving transport
cost two.

For clarity, if p* is the original optimum and r_k the infimum over exact
local measures with the prescribed degree-k overlaps, the consequence for
T>=1 and k>=1 is

\[
 0\le p^*-r_k
 \le {2LC_X(T-1)\over(1-\rho)k},\qquad
 {p^*-r_k\over T}\le {2LC_X\over(1-\rho)k}.
\]

Use arbitrarily near-optimal local measures if attainment is not invoked.
This is the meaning needed for the note's phrase "normalized objective
gap." Supplied feasible local measures can have cost exceeding p*, so their
cost alone is not a certified lower bound. The note explicitly handles this
correctly in its sampling guarantee. With a separate certified lower bound,
Markov's inequality and independent sampling give the stated probabilities.

For variable Lipschitz factors the exact coefficient of Delta_s in e_t is
the product over j=s,...,t-1, with the empty product equal to one. Assumption
(8), uniformly for every subword of every accepted complete word, gives the
claimed C/(1-rho) bound. Assume nonnegative factors and 0<=rho<1 explicitly.
No independence of factors and mismatches is needed. Replacing this uniform
assumption by their separate expectations is invalid: if lambda=10 and
Delta=1 on an event of probability .01 and both vanish otherwise, then
E(lambda Delta)=.1 whereas E(lambda)E(Delta)=.001. This tests the warning
already present in the source, not a new theorem.

## Prior results and significance

I reopened [Han, Jiao, and Weissman, Lemma 25, equation (24)](https://proceedings.mlr.press/v75/han18b/han18b.pdf).
It states precisely the polynomial moment-matching identity with factor
two. Its next discussion uses a translated absolute-value function. The
lemma's positive interval restriction is immaterial under translation;
this is a direct antecedent, not merely related subject matter. The
general finite-feature version uses the same classical duality.

I also inspected the introduction of
[Lubinsky's Bernstein-constant paper](https://lubinsky.math.gatech.edu/Research%20papers/BrnstnDec05CA.pdf).
It supports the invoked limit and reports the numerical constant, while
crediting its numerical determination to Varga and Carpenter. No numerical
certification or independent asymptotic proof is supplied here.

The earlier novelty screen identifies Neufeld--Xiang's reassembly theorem
and its sum of Wasserstein discrepancies as the closest primal transport
comparison. That theorem does not by itself preserve deterministic dynamic
support relations. The control note's replay argument supplies this under
its restrictive action and invariance assumptions. I did not independently
retrieve the full theorem in this pass: the versioned PDF fetch failed for
size, and the HTML response did not expose the searched theorem. The
earlier screen remains the source of that theorem-level comparison.

The [Philippe--Essick--Dullerud--Jungers abstract](https://arxiv.org/abs/1503.06984)
confirms automaton-constrained switched linear systems and multinorm
stability as established antecedents. I did not inspect its full proofs.
The present scalar product estimate is an elementary propagation argument;
it introduces no new stability criterion. The existing ALP and occupation
measure comparisons remain qualified as in the source notes.

No reviewed evidence supports promoting this package to a substantial
standalone originality claim. Its useful contribution here is a particularly
small control encoding of a known approximation obstruction and a precise
primal feasibility statement with explicit restrictions. Efficient local
measure optimization, extraction from truncated SDP data, and broader
state-dependent feasibility remain outside the proved result. They should
remain recorded limitations, without starting their investigation during
this closeout.

## Verification record

Ran `python3 code/research_20260922/check_moment_control.py` successfully:
degree-one gap one; degree-two and degree-three gaps one quarter; exact
matched moments and the quadratic error values at all three extrema.
These are rational finite-instance checks. They do not verify gluing,
functional analysis, asymptotics, or novelty. The proof checks above were
independent mathematical reconstruction, without Lean. No project-wide
verification or CI inspection was performed. The reviewed source files
were not edited.
