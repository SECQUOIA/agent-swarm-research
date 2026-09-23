# Paper skeleton: verified-sample decoders and accuracy curves for block state conversion

Date: 2026-09-02
Status: outline only; assembles the day's audited query-complexity results.
Source notes: 2026-09-02-zero-versus-k-verified-sample-state-conversion.md,
2026-09-02-composed-small-success-search-polynomial.md, building on the
model of 2026-09-02-general-block-logdet-condensation.md.

## Proposed title

"Verified-sample decoders and the accuracy curve of hidden-block state
preparation"

## Narrative arc

1. Problem: prepare (to trace error \(\varepsilon\)) the block-diagonal
   center of a hidden winner set \(S\), \(|S|\in\{0,k\}\), each winner
   marked by an \(N\)-bit parity; motivated by condensed central paths of
   winner-take-all SDP families (QIPM context), but stated as a clean
   query-complexity question. Prior state: endpoints only; two-copy
   collision decoders lose \(1/k\); "pairwise trace distance gives no
   common measurement".
2. Tool 1 — verified-sample decoder: measure the label, verify with
   fresh queries; one-sided by construction (zero-winner branches cannot
   pass verification). Kills the \(1/k\) loss, works on mixed outputs, no
   unitary access.
3. Tool 2 — polynomial method for one-sided small bias: parity collapse
   to block variables, symmetrization, Coppersmith--Rivlin + Markov:
   degree \(\Omega(\sqrt{\delta G/k})\), hence
   \(T=\Omega(\sqrt\delta\,N\sqrt{G/k})\). The \(N=1\) case is
   Zalka/KŠdW; the composed version with full inner factor appears new.
4. Matching algorithm: detuned rejection sampling + fixed-point
   amplification (two-regime detuning parameter; the \(\emptyset\)-branch
   over-rotation pitfall and its fix).
5. Main theorem: full accuracy curve
   \(Q_\varepsilon=\widetilde\Theta(N(1+\sqrt{(p-\varepsilon)G/k}))\)
   for the zero-vs-k promise (hypotheses: \(p\) bounded away from 0,1;
   \(\varepsilon\ge4\eta\); \(k=O(G/\log^2G)\) only for the
   adversary-route version — the polynomial route needs just
   \(\delta G/k=\Omega(1)\)). Classical:
   \(\Theta(N(1+\delta G/k))\) — a \(\sqrt{\cdot}\)-vs-linear separation
   at every accuracy.
6. Application back to the QIPM family: exactly-\(k\) condensation
   profile (AP6) lower bounds upgraded from operator-level unitary access
   to trace-close mixed outputs; critical-regime \(\Theta(N(G/k)^{1/4})\)
   proved tight for \(\varepsilon\le p/2\) contracts.
7. Open: \(\sqrt\delta\)-strength composition for general inner
   predicates \(f\) (adversary route gives linear-\(\delta\) only); the
   \(\eta\)-channel minimax radius exactly; sliver regimes
   (\(\delta=o(k/G)\)).

## Verification status

Both source notes referee-audited (zero-vs-k fully repaired; polynomial
note audit pending at outline time). Fact and novelty sweep complete:

- BBCMW Lemma 4.2 (degree \(\le2T\) multilinear acceptance) verified
  verbatim; Markov \(2D^2M/L\) verified; Coppersmith--Rivlin verified as
  quoted in KŠdW Theorem 8 — universal constants exist but are
  **unspecified in CR92**, so no explicit \(C_1,C_2\) may be claimed
  (the proof only needs existence; alternative with explicit constants:
  Erdélyi arXiv:1406.2560, different parametrization).
- Citation corrections to adopt: Zalka (quant-ph/9711070) proves exact
  optimality for **one** marked item only; the \(k\)-marked small-success
  bound \(\varepsilon\le8(T{+}1)^2k/N\) is Dohotaru--Høyer
  (arXiv:0810.3647, Thm 8) via Carolan--Poremba (arXiv:2403.04740,
  Thm 2.3/Cor 2.4). Aaronson's direct-product theorem
  (quant-ph/0402095, Thm 10) is the find-all-\(k\) analog.
- Novelty verdict: the composed \(\sqrt\delta\cdot N\) small-success
  theorem was **not found stated anywhere** (checked KŠdW, Sherstov
  hardness amplification — exponential-decay flavor, not \(\sqrt\delta\);
  Lee--Roland SDPTs; Bun--Thaler vanishing-error OR degree
  \(\Theta(\sqrt{n\log(1/\varepsilon)})\), a decision-version scaling;
  Beame et al. time-space tradeoffs). All ingredients separately known;
  honest framing: new-as-stated, plausibly derivable by experts.
