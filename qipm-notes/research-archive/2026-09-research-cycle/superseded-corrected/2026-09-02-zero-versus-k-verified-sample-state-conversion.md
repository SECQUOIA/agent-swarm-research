# Zero-versus-k state conversion: the verified-sample decoder closes the constant-visibility regime

Date: 2026-09-02
Status: proved and independently referee-audited (verdict: no fatal
errors; Theorem M-1 sound as stated; repairs to M-2's parameter choice,
the \(k\nmid G\) recipe, M-4's edge regime, and headline scoping applied
below). Resolves ledger Direction M
(2026-09-02-research-closure-and-open-frontier.md, Section III.M) in the
constant-winner-mass regime for all winner-set sizes
\(1\le k=O(G/\log^2G)\), where the previous collision decoder worked only
for \(k=O(1)\). The narrow transition window \(\varepsilon\to p\) remains
open up to a \(\sqrt{p-\varepsilon}\) factor; see the open-refinement
section.

## Problem

Notation follows 2026-09-02-general-block-logdet-condensation.md. There are
\(G\) independently queried blocks; block \(g\) is a winner iff a Boolean
predicate \(f\) (raw-query adversary value \(A=\operatorname{Adv}^\pm(f)\),
bounded-error complexity \(Q(f)=\Theta(A)\)) evaluates to one on its
private input. Promise: the winner set \(S\) satisfies \(|S|\in\{0,k\}\).
Targets: for \(|S|=k\), the block-diagonal center
\[
  \rho_S=\sum_{g\in S}\frac pk\,|g\rangle\langle g|\otimes\rho_W
  +\sum_{g\notin S}\frac{1-p}{G-k}\,|g\rangle\langle g|\otimes\rho_L,
\]
and for \(S=\emptyset\) the all-loser center
\(\rho_0=\frac1G\sum_g|g\rangle\langle g|\otimes\rho_L^0\), with
\(p=p_{G,k}\) and the constant-size internal states
\(\rho_W,\rho_L,\rho_L^0\) all public. Put
\(\eta=D_{\rm tr}(\rho_L,\rho_L^0)\). Task: given the oracle, output a
state within trace distance \(\varepsilon\) of the (input-determined)
target, for every promised input. The prior ledger had only the two
endpoints: cost \(0\) once \(\varepsilon\) exceeds the trace-distance
radius, and \(\Theta(A\sqrt{G/k})\) for small constant error but only when
the two-copy collision gap \((Gp-k)^2/(Gk(G-k))\approx p^2/k\) stays
constant, i.e. \(k=O(1)\). The obstruction recorded there: pairwise trace
distance gives no common measurement for unknown \(S\), and collision
loses a factor \(1/k\).

## The new idea: verify the sample instead of colliding two copies

Measuring the label register of an \(\varepsilon\)-accurate output and then
**verifying the sampled block with \(O(Q(f))\) fresh raw queries** is a
perfectly good common measurement: it needs no knowledge of \(S\), its
acceptance probability is at least \(p-\varepsilon\) (minus verification
error) when \(|S|=k\), and—crucially—**at most the verification error on
the no-winner branch**, because on a no-winner input every block genuinely
fails the predicate no matter what state was output. One-sidedness is what
kills the \(1/k\) loss: no collision statistic is needed at any \(k\).

## Theorem M-1 (lower bound via the verified-sample decoder)

Fix \(\delta\in(0,1)\). Suppose a circuit makes \(T\) raw queries and, on
every promised input, outputs a state within trace distance
\(\varepsilon\le p-\delta\) of the target. If
\(\sqrt{G/k}\ge C\,\delta^{-1}\log(1/\delta)\) for a universal constant
\(C\), then
\[
  T=\Omega\!\big(\delta\,A\sqrt{G/k}\big).
\]
For the parity/holonomy families (\(f=\mathrm{PARITY}_N\), \(A=\Theta(N)\))
this is \(T=\Omega(\delta\,N\sqrt{G/k})\).

### Proof

**Decision lower bound for the 0-vs-k promise.** Set
\(G'=\lfloor G/k\rfloor\). Given a 0-vs-1 instance on \(G'\) blocks, build
a 0-vs-k instance on \(G\) blocks by taking \(k\) identical copies of each
of the \(G'\) blocks and pinning the \(<k\) leftover blocks to a fixed
public loser input (nonempty \(\mathcal X_0\) is Theorem P assumption 3);
this preserves the \(\{0,k\}\) promise and loses only constants. One raw
query to copy \((i,j)\), coordinate \(\ell\), is simulated by one raw
query to \((i,\ell)\). Zero winners map
to zero winners, a unique winner \(a\) maps to the valid size-\(k\) winner
set \(\{(a,j):j\in[k]\}\), and all embedded inputs are Cartesian-product
promised inputs. Theorem P
(2026-09-02-general-block-logdet-condensation.md, (O18)) gives
\(\operatorname{Adv}^\pm=\Omega(A\sqrt{G'})\) for 0-vs-1 on \(G'\) blocks,
so bounded-error 0-vs-k decision costs \(\Omega(A\sqrt{G/k})\) raw
queries.

**Decoder.** Repeat \(R=\Theta(1/\delta)\) times: run the preparation
circuit fresh (\(T\) queries); measure the label register, obtaining \(g\);
run a bounded-error evaluator for \(f\) on block \(g\) with error reduced
to \(\beta=\delta/8\) by majority (\(O(Q(f)\log(1/\delta))\) queries);
accept if it outputs one. Per trial:

- \(|S|=k\): the label-in-\(S\) event is a two-outcome measurement, so its
  probability under the output is at least
  \(p-\varepsilon\ge\delta\); acceptance
  \(\ge\delta(1-\beta)\ge\delta/2\).
- \(S=\emptyset\): every block fails \(f\) on this input, so acceptance
  \(\le\beta=\delta/8\) regardless of what state was output.

A Chernoff bound over \(R=\Theta(1/\delta)\) trials distinguishes
acceptance rates \(\ge\delta/2\) from \(\le\delta/8\) with error \(1/3\).
Total cost \(O\big(\delta^{-1}(T+Q(f)\log(1/\delta))\big)\) must be
\(\Omega(A\sqrt{G/k})\); the hypothesis on \(\sqrt{G/k}\) absorbs the
verification term, leaving \(T=\Omega(\delta A\sqrt{G/k})\).
\(\square\)

Remarks. (i) Only the winner-mass property
\(\operatorname{tr}[(\Pi_S\otimes I)\rho_S]=p\) of the targets is used; the
internal states and even the loser masses are irrelevant to the lower
bound. (ii) No coherent evaluator, inverse preparation access, or
purification contract is assumed — the decoder consumes trace-close mixed
outputs, unlike the extraction argument (A8), which needed an
operator-level unitary. (iii) \(\eta\) plays no role here; the bound is
about the winner-mass channel.

## Theorem M-2 (matching upper bound by partial fixed-point amplification)

Let \(T_{\rm eval}\) be the clean-evaluator cost ((A1) of the condensation
note), \(\delta=p-\varepsilon\), and assume \(1-p\ge c_0>0\) (the
\(\emptyset\)-branch acceptance needs \(1-m=\Omega(1)\); without this the
round count inflates by \((1-m)^{-1/2}\)). For \(4\eta\le\varepsilon\le p\):
\[
  Q_\varepsilon=O\!\Big(T_{\rm eval}\big(1+\sqrt{\delta\,G/k}\,\big)
  \log(1/\delta)\,c_0^{-1/2}\Big).
\]
For \(\varepsilon<4\eta\):
\(Q_\varepsilon=O(T_{\rm eval}\sqrt{G/k}\,\log(1/\varepsilon))\), which is
flat in \(\varepsilon\) and matched by Theorem M-1 whenever
\(\delta=\Omega(1)\).

### Proof sketch (all steps standard; referee repairs F1--F3 applied)

Run the coherent rejection preparation of the condensation note with
*detuned* masses \(a'_W=m/k\), \(a'_L=(1-m)/(G-k)\), where
\[
  m=\min\bigl\{\,p,\ \max\{(3/2)\delta,\;k/G\}\,\bigr\}
\]
(the cap at \(p\) covers \(\delta>2p/3\), where \(m=p\) gives zero
detuning error and cost \(\Theta(\sqrt{pG/k})=\Theta(\sqrt{\delta G/k})\);
the cap also guarantees \(1-m\ge1-p\ge c_0\)):
copy the label to an environment register, apply \(V_f\), rotate
acceptance amplitudes \(\sqrt{a'_b/a'_{\max}}\), attach the public
purifications of \(\rho_W/\rho_L\) conditioned on the predicate bit. (The
earlier draft's choice \(m=p-\varepsilon/2\) proves only
\(O(\sqrt{pG/k})\) rounds in the \(\varepsilon=\Theta(p)\) window; the
detuning error budget must be spent down to \(\Theta(\delta)\), not
\(\Theta(\varepsilon)\), to get the \(\sqrt\delta\) cost — this is why the
log factor is \(\log(1/\delta)\), not \(\log(1/\varepsilon)\).) One-trial
acceptance is exactly \(k/(Gm)\) on the \(k\)-branch and
\(k(1-m)/(m(G-k))\) on the \(\emptyset\)-branch — both
\(\Omega(c_0\,k/(Gm))\) since the cap \(m\le p\) keeps
\(1-m\ge c_0\). Fixed-point amplification (Yoder--Low--Chuang) with
\(O(\sqrt{Gm/k}\,\log(1/\delta)\,c_0^{-1/2})\) rounds drives the
acceptance-subspace *residual* below \((\delta/8)^2\) **on both branches
simultaneously** (the residual must be quadratically small because
pure-state overlap converts to trace distance by a square root), which is
why fixed-point rather than exact tuned amplification is used: exact
amplification tuned to the \(k\)-branch angle over-rotates the
\(\emptyset\)-branch by a relative angle \(\Theta(m)\), leaving
\(\Theta(m^2)\) junk mass, not affordable at constant \(p\). Conditioned
on acceptance the outputs are exactly the detuned center (winner mass
\(m\), correct uniform shapes, exact public internals) on the
\(k\)-branch and exactly
\(\frac1G\sum_g|g\rangle\langle g|\otimes\rho_L\) on the
\(\emptyset\)-branch. Total errors: \(k\)-branch
\(\le(p-m)+\delta/8\le\varepsilon-\delta/2+\delta/8<\varepsilon\);
\(\emptyset\)-branch \(\le\eta+\delta/8\le\varepsilon/4+\delta/8
<\varepsilon\). For \(\varepsilon<4\eta\), first decide existence by
bounded-error search over the \(k\)-marked promise
(\(O(T_{\rm eval}\sqrt{G/k}\log(1/\varepsilon))\), error folded into
trace distance) and then prepare the identified branch exactly ((AP3),
cost \(O(T_{\rm eval}\sqrt{Gp/k})\) at worst; no exactly-\(k\)
circularity since the branch is decided first). \(\square\)

## Corollary M-3 (ledger Direction M, constant-visibility regime, closed)

In the subcritical regime with \(p=\Theta(1)\) bounded away from both
\(0\) and \(1\), for every \(k\) with \(\sqrt{G/k}=\Omega(\log G)\)
(equivalently \(k=O(G/\log^2G)\); this hypothesis comes from Theorem M-1's
verification-absorption condition and is not merely cosmetic), every
\(4\eta\le\varepsilon\le(1-c)p\) with constant \(c\) (the range
\(\varepsilon<4\eta\) is covered at the same
\(\Theta\)-cost by M-2's fallback and M-1), and \(f=\mathrm{PARITY}_N\):
\[
  Q_\varepsilon=\Theta\!\big(N\sqrt{G/k}\big)
\]
up to \(\log\) factors (which are \(\operatorname{polylog}(G)\) here since
\(\delta=\Omega(1)\)). Both the previous \(k=O(1)\) collision restriction
and the common-measurement obstruction are gone. The free-output endpoint
is unchanged: for \(\varepsilon\) above the minimax radius
\(\min_\sigma\max\{D_{\rm tr}(\sigma,\rho_0),\max_SD_{\rm tr}(\sigma,\rho_S)\}\)
(at most \(\max\{p_{G,k},k/G\}\) plus internal terms by (M15)), zero
queries suffice.

## Theorem M-4 (classical query complexity, tight in its stated regime)

With classical raw queries (state synthesis after querying is free), for
\(f=\mathrm{PARITY}_N\), writing \(\delta=p-\varepsilon\): if
\(2\eta\le\varepsilon\), \(Ck/G\le\delta\le1/2\), and \(1-p=\Omega(1)\),
then
\[
  R_\varepsilon=\Theta\!\big(N\,\delta\,G/k\big).
\]
Upper: test \(t=O(\delta G/k)\) uniformly random blocks without
replacement (\(N\) queries each, parity exact); \(P_{\rm find}=
1-\binom{G-k}{t}/\binom{G}{t}\) is public and \(\ge\delta+\Theta(k/G)\)
with the stated budget (this needs \(\delta\le1/2\); for
\(\delta\to1\) the budget is \(\Theta((G/k)\log\frac1{1-\delta})\)).
Found winners are uniform on \(S\) by exchangeability. Output the publicly
calibrated mixture: on find, the \(\rho_S\)-shaped state with the found
winner and internals \(\rho_W/\rho_L\); on no-find, the uniform
\(\otimes\rho_L\) shape. Error accounting: winner-mass deficit
\(\le p-\min\{P_{\rm find},p\}\le\varepsilon-\Theta(k/G)\) on the
\(k\)-branch (the \(\Theta(k/G)\) slack absorbs the loser-internal mass
placed on \(S\)-blocks by the no-find output), and exactly \(\eta\le
\varepsilon/2\) on the \(\emptyset\)-branch.
Lower: the classical verified-sample decoder gives a distinguisher with
one-sided acceptance \(\ge\delta\) vs \(0\) (parity verification is exact
at cost \(N\)), and \(O(1/\delta)\) repetitions decide 0-vs-k. Hard
distribution: \(k\)-copy embedding with parity-conditioned uniform block
strings, so every proper subset of a block's bits is uniform; \(T\)
queries complete at most \(T/N\) distinct original blocks, the planted
winner is hit with probability at most \((T/N)/(G'/1)=Tk/(NG)\) up to
constants, and incomplete transcripts are identically distributed on both
branches. Hence \(\delta^{-1}(T+N)=\Omega(NG/k)\), and with
\(\delta\ge Ck/G\) the additive term is absorbed:
\(T=\Omega(\delta NG/k)\). \(\square\)

Boundary remark (referee finding F6): for \(\delta=o(k/G)\) the free
output may already meet the contract (the uniform-label output has
winner-mass deficit \(\approx p-k/G\le\varepsilon\)), so no
\(\Omega(N)\) floor is claimed there. Classically the linear-in-\(\delta\)
law is tight on both sides of the stated regime; the quantum--classical
separation \(\sqrt{G/k}\) versus \(G/k\) persists at every fixed relative
accuracy.

## Open refinement: the \(\sqrt{\delta}\) window — NOW CLOSED for parity

Update (same date, later):
2026-09-02-composed-small-success-search-polynomial.md proves the missing
composed small-success theorem for the parity inner function by the
polynomial method (parity collapse + symmetrization + Coppersmith--Rivlin
+ Markov): one-sided bias \(\delta\) at \(k\) winners forces
\(T=\Omega(\sqrt\delta N\sqrt{G/k})-O(N)\). Combined with the repaired
Theorem M-2, the full curve is
\(Q_\varepsilon=\widetilde\Theta(N(1+\sqrt{(p-\varepsilon)G/k}))\). The
discussion below is retained for the record and for general inner
predicates \(f\), where only the linear-in-\(\delta\) adversary route is
known.

For \(\delta=p-\varepsilon=o(1)\) the quantum bounds are
\(O(N\sqrt{\delta}\sqrt{G/k}\,\log(1/\delta))\) (Theorem M-2 after the
detuning repair — the \(\sqrt\delta\) upper is genuine only with the
budget spent to \(\Theta(\delta)\)) versus \(\Omega(\delta N\sqrt{G/k})\)
(Theorem M-1, which additionally requires
\(\sqrt{G/k}\ge C\delta^{-1}\log(1/\delta)\), i.e. \(G/k\gtrsim
\delta^{-2}\) — the linear-in-\(\delta\) lower is only proved there), a
\(\sqrt\delta\) gap. The truth is plausibly the upper bound: for plain
search (Zalka; Klauck--Špalek--de Wolf), \(T\)-query success is
\(O(T^2k/G)\), i.e. success \(\delta\) costs \(\Theta(\sqrt{\delta G/k})\).
The missing piece is a *composed* small-success theorem
\(Q_\delta(\mathrm{SEARCH}_{G,k}\circ f)=\Omega(\sqrt\delta\,A\sqrt{G/k})\);
the reduction to plain search loses the inner factor \(A\), and adversary
progress arguments natively give only the linear-in-\(\delta\) scaling.
The multiplicative adversary (Špalek) or a KŠdW-style polynomial argument
composed through parity are the plausible routes. Until then, the curve is
pinned to within \(\sqrt{p-\varepsilon}\), which is a constant everywhere
except the transition window \(\varepsilon\to p\).

At and above the condensation threshold (\(p=O(\sqrt{k/G})\) or
\(p=\Theta(k/G)\)), any constant \(\varepsilon\) exceeds \(p\) and the
free output already meets the contract on the winner-mass channel (only
the \(\eta\)-channel can retain hardness); the fixed-error collapse
recorded in the condensation note is thereby confirmed, and the
interesting scaling there is the exactly-\(k\) profile (AP6), not
zero-vs-k.

## Verification record

- Independent adversarial referee audit completed. Verdict: no fatal
  errors; Theorem M-1 sound as stated with "parameter accounting exactly
  right" (one-sidedness, trace-distance usage, Chernoff separation,
  verification absorption, and the copy embedding all verified);
  Corollary M-3 undamaged by the flaws found elsewhere.
- Referee repairs applied in this revision: (F1) M-2's detuning parameter
  respecified to \(m=\min\{p,\max\{(3/2)\delta,k/G\}\}\) with a
  \(\Theta(\delta)\) junk budget and \(\log(1/\delta)\) factor — the
  earlier \(m=p-\varepsilon/2\) proved only \(O(\sqrt{pG/k})\) in the
  \(\varepsilon=\Theta(p)\) window; (F2) the \(1-p\ge c_0\) hypothesis
  and the cap \(m\le p\); (F3) quadratic residual targets for the
  overlap-to-trace-distance conversion; (F5) the \(\lfloor G/k\rfloor\)
  copies-plus-loser-padding recipe for \(k\nmid G\); (F6/F7) M-4
  restricted to \(Ck/G\le\delta\le1/2\), \(1-p=\Omega(1)\), with explicit
  calibration and error accounting and the boundary remark; (F8) headline
  and M-3 scoped to \(k=O(G/\log^2G)\); (F9) the open-refinement section
  now states both caveats (repaired upper; \(G/k\gtrsim\delta^{-2}\)
  domain of the lower).
- Original self-audit items retained: acceptance on the
  \(\emptyset\)-branch depends only on the verifier and the true input;
  only Theorem P assumptions (1)--(3) are used; copies of one block share
  queries, which is exactly why the effective block count is \(G/k\) on
  both the quantum and classical sides; (M15)/(M16) are used only for the
  free-output endpoint — the \(1/k\) collision loss is bypassed, not
  contradicted.
