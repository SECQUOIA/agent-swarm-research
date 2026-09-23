# Composed small-success search by the polynomial method: the full zero-versus-k curve

Date: 2026-09-02
Status: proved; independently referee-audited (verdict: "no fatal
errors; Theorem S and its proof are correct — every step verified,
including brute-force confirmation of the parity-collapse identity";
S2's boxed-claim domain repair applied below) and fact/novelty-swept
(all cited facts verified against primary sources; the composed
\(\sqrt\delta\cdot N\) theorem was not found stated anywhere in the
literature — ingredients separately known, so framed as new-as-stated
and plausibly derivable by experts). Closes the "\(\sqrt\delta\) window"
left open in 2026-09-02-zero-versus-k-verified-sample-state-conversion.md,
for the parity inner function.

## Result

Setting as in the zero-versus-k note: \(G\) blocks of \(N\) bits, block
\(g\) is a winner iff its parity is odd, promise \(|S|\in\{0,k\}\), raw
queries address single bits. Write \(\delta\) for a success/bias
parameter.

**Theorem S (one-sided small-bias lower bound).** Let \(\mathcal A\) be a
\(T\)-query quantum algorithm with acceptance probability at most
\(\beta\le\delta/2\) on every zero-winner input and at least \(\delta\) on
every \(k\)-winner input. Then
\[
  T\ \ge\ c_1\,N\sqrt{\delta G/k}\ -\ c_2 N
\]
for absolute constants \(c_1,c_2>0\).

**Corollary S1 (composed small-success search).** Any \(T\)-query
algorithm that, on every input with exactly \(k\) parity-marked blocks,
outputs a marked block with probability at least \(\delta\), satisfies
\(T=\Omega(\sqrt\delta\,N\sqrt{G/k})-O(N)\). (Attach exact parity
verification of the output block, \(N\) queries, to make acceptance
one-sided with \(\beta=0\), then apply Theorem S with \(T+N\) queries.)
This matches the partial-Grover upper bound
\(O(\sqrt\delta\,N\sqrt{G/k}+N)\): \(t=\Theta(\sqrt{\delta G/k})\) Grover
rounds at \(\Theta(N)\) queries per round reach winner mass
\(\sin^2((2t{+}1)\theta)=\Theta(\delta)\). The \(N=1\) case is known:
Zalka (quant-ph/9711070) is exact for one marked item only; the
\(k\)-marked small-success bound \(\delta\le8(T{+}1)^2k/G\) is
Dohotaru--Høyer (arXiv:0810.3647, Thm 8) via Carolan--Poremba
(arXiv:2403.04740, Thm 2.3/Cor 2.4), with KŠdW (quant-ph/0402123)
supplying the polynomial-method machinery. The content here is that the
inner factor \(N\) composes at full strength with the \(\sqrt\delta\)
scaling.

**Corollary S2 (full zero-versus-k state-conversion curve).** For the
zero-versus-k preparation task of the companion note (targets with winner
mass \(p\), trace-error budget \(\varepsilon\), \(\delta=p-\varepsilon\)),
a \(T\)-query preparation circuit yields, via one verified-sample trial
with **exact** parity verification of the sampled block (\(N\) queries,
zero false accepts — no majority needed for parity), a one-sided
acceptance algorithm with \(T+N\) queries, acceptance \(0\) on the
\(\emptyset\)-branch and \(\ge p-\varepsilon=\delta\) on every
\(k\)-branch input. Theorem S gives
\[
  T\ =\ \Omega\big(\sqrt{\delta}\,N\sqrt{G/k}\big)-O(N),
\]
nonvacuous as soon as \(\delta G/k\) exceeds a constant. Matching the
repaired Theorem M-2 upper bound
\(O(N(1+\sqrt{\delta G/k})\log(1/\delta))\): for parity blocks,
\(1-p=\Omega(1)\), \(\varepsilon\ge4\eta\), and
\(\delta\ge C\,k/G\) (below that threshold the free public output can
already meet the contract, and no \(\Omega(N)\) floor is claimed):
\[
  \boxed{\;Q_\varepsilon\ =\ \widetilde\Theta\big(N\sqrt{(p-\varepsilon)G/k}\big),\;}
\]
the complete accuracy curve on that domain (\(\widetilde\Theta\) hides
the \(\log(1/\delta)\) of the upper bound, legible for
\(\delta\ge1/\mathrm{poly}\)). This supersedes the linear-in-\(\delta\)
lower bound of Theorem M-1, which remains of interest because its
adversary route works for arbitrary inner predicates \(f\), while the
present proof is parity-specific.

**Corollary S3 (exactly-\(k\) AP6 profile: mixed-output lower bounds).**
The condensation note's exactly-\(k\) preparation profile (AP6) had
matching lower bounds only under operator-level access to the preparation
unitary and its inverse, with the explicit caveat that "a mere trace-close
mixed-state output is not covered by the extraction argument." Theorem S
removes that caveat. Suppose a \(T\)-query circuit outputs, on every
exactly-\(k\) input, a state within trace distance \(\varepsilon\le p/2\)
of the winner-mass-\(p\) target. Attach the verified-sample decoder with
exact parity verification (\(N\) queries, zero false accepts): on
exactly-\(k\) inputs acceptance is \(\ge p-\varepsilon\ge p/2=:\delta\);
on zero-winner inputs — which are outside the promise but on which the
circuit still physically runs — acceptance is exactly \(0\) because no
block is odd. Theorem S gives
\[
  T=\Omega\big(\sqrt p\,N\sqrt{G/k}\big)-O(N).
\]
Across the condensation phases: subcritical \(p=\Theta(1)\) gives
\(\Omega(N\sqrt{G/k})\); critical \(p=\Theta(\sqrt{k/G})\) gives
\(\Omega(N(G/k)^{1/4})\), matching AP6's middle line; in the
supercritical phase \(p=\Theta(k/G)\) the bound is vacuous, which is
consistent with (but does not certify) AP6's \(O(N)\) upper bound. Hence
the first two lines of the AP6 profile are tight for trace-close
mixed-state output contracts at relative accuracy \(\varepsilon\le p/2\),
with no unitary-access assumption.

## Proof of Theorem S

**Step 1 (acceptance polynomial).** By Beals--Buhrman--Cleve--Mosca--de
Wolf, the acceptance probability of a \(T\)-query algorithm is a real
multilinear polynomial \(P(x)\) of degree at most \(2T\) in the
\(\pm1\)-valued input bits, with \(0\le P\le1\) on all of
\(\{\pm1\}^{NG}\).

**Step 2 (parity collapse).** Condition each block \(g\) on its parity
\(p_g\in\{\pm1\}\): the conditional input distribution is uniform on the
parity coset of block \(g\), independently across blocks. For a monomial
\(x_S\), the conditional expectation factorizes over blocks;
within a block it is \(1\) if the block's share of \(S\) is empty,
\(p_g\) if it is the full block, and \(0\) for any proper nonempty share
(character sums over a coset of the parity-check code vanish unless the
character is trivial or is the parity character itself). Hence
\(q(p)=\mathbb E[P\mid p]\) is a multilinear polynomial in
\(p\in\{\pm1\}^G\) of degree at most \(D=\lfloor2T/N\rfloor\), still with
\(0\le q\le1\) on \(\{\pm1\}^G\), \(q\le\beta\) at the all-even point, and
\(q\ge\delta\) on every weight-\(k\) odd pattern.

**Step 3 (symmetrization).** Averaging over block permutations
(Minsky--Papert) gives a univariate polynomial \(h\) of degree at most
\(D\) with \(0\le h(w)\le1\) for all integers \(w\in\{0,\dots,G\}\),
\(h(0)\le\beta\), \(h(k)\ge\delta\).

**Step 4 (Coppersmith--Rivlin plus Markov).** Fix a small absolute
\(\gamma>0\). Case (i): \(D\le\gamma\sqrt G\). By Coppersmith--Rivlin, a
degree-\(D\) polynomial bounded by \(1\) in absolute value on the integers
\(\{0,\dots,G\}\) is bounded by \(C(\gamma)=O(1)\) on the whole interval
\([0,G]\) (the bound is \(\exp(O(D^2/G))\)-type; constant in this case).
Markov's inequality on the rescaled interval then gives
\(\sup_{[0,G]}|h'|\le2D^2C(\gamma)/G\). The mean value theorem on
\([0,k]\) gives some \(\xi\) with
\(h'(\xi)\ge(h(k)-h(0))/k\ge(\delta-\beta)/k\ge\delta/(2k)\). Combining:
\(2D^2C(\gamma)/G\ge\delta/(2k)\), i.e.
\(D\ge\sqrt{\delta G/(4C(\gamma)k)}\). Case (ii): \(D>\gamma\sqrt G\).
Then \(D>\gamma\sqrt G\ge\gamma\sqrt{\delta G/k}\) directly, since
\(\delta\le1\le k\) gives \(\delta G/k\le G\). In both cases
\(D=\Omega(\sqrt{\delta G/k})\), and \(D=\lfloor2T/N\rfloor\le2T/N\)
gives the theorem; the \(-c_2N\) slack absorbs floor effects (and is in
fact unnecessary: \(D=0\) is impossible since a constant cannot be both
\(\le\delta/2\) and \(\ge\delta\)). \(\square\)

## Remarks

1. The one-sidedness hypothesis (\(\beta\le\delta/2\) on the zero-winner
   branch) is what the verified-sample decoder provides for free; a
   two-sided small-bias hypothesis would not survive Step 4 (a constant
   function has bias zero but the mean-value argument needs the two
   anchored values).
2. Nothing in the proof uses the promise: \(h\) is bounded at *all*
   integer weights because the algorithm is a physical process on all
   inputs. This is where the polynomial method is stronger than the
   Chernoff-repetition adversary route of Theorem M-1, which needed
   \(\sqrt{G/k}\ge C\delta^{-1}\log(1/\delta)\); Theorem S needs only
   \(\delta G/k\) larger than a constant for a nontrivial bound.
3. Parity is essential to Step 2 (its proper sub-monomials all vanish).
   For a general inner predicate \(f\), the analogous collapse needs a
   dual-polynomial composition argument; the adversary route (Theorem
   M-1) covers general \(f\) at linear-in-\(\delta\) strength. Whether
   \(\sqrt\delta\)-strength composition holds for every \(f\) is left
   open.
4. Combined with the exactly-\(k\) profile (AP6) of the condensation
   note, the entire zero-versus-\(k\) intermediate-accuracy question for
   the parity/holonomy block families is now closed up to logarithmic
   factors and the \(\eta\)-channel caveats catalogued in the companion
   note.
5. Classical analogue: the classical law
   \(\Theta(N\delta G/k)\) (Theorem M-4, on its domain
   \(Ck/G\le\delta\le1/2\)) is linear in \(\delta\), so the
   quantum--classical cost ratio is \(\sqrt{\delta G/k}\): as \(\delta\)
   shrinks, the quantum cost falls like \(\sqrt\delta\) and the classical
   like \(\delta\), so the multiplicative separation shrinks toward 1
   while both remain nontrivial down to \(\delta\sim k/G\).

## Verification record

- Self-audit: Step 2's coset-character computation checked directly
  (proper nonempty sub-monomials of a parity coset average to zero; full
  blocks contribute \(p_g\)); degree bookkeeping \(D\le\lfloor2T/N\rfloor\)
  checked; Step 4 case split checked including the \(k\ge1\) edge; the
  upper bounds cited are the companion note's M-2 (post-repair) and
  standard partial Grover.
- Independent referee audit completed: Theorem S verified step by step
  (parity collapse brute-forced for \(N=2..5\) and end-to-end on random
  multilinear polynomials; CR+Markov combination confirmed properly
  ordered; case split confirmed). Repairs applied: S2 rewritten with
  exact parity verification (\(\beta'=0\), subtractive \(O(N)\)) and the
  domain hypothesis \(\delta\ge Ck/G\) for the boxed curve; S3 likewise,
  with the supercritical phase honestly marked vacuous and "tight"
  scoped to AP6's first two lines; the case-(ii) parenthetical and the
  Remark 5 separation-direction sentence fixed.
- Fact verification completed against primary sources:
  BBCMW Lemma 4.2 (JACM 48(4), degree \(\le2T\) multilinear acceptance);
  Markov \(2D^2M/L\) on an interval of length \(L\); Coppersmith--Rivlin
  as quoted in KŠdW quant-ph/0402123 Thm 8
  (\(|p(x)|<a\,e^{bD^2/n}\), universal \(a,b\) **unspecified in CR92** —
  this proof needs only existence, so no explicit constants are claimed;
  explicit-constant alternative: Erdélyi arXiv:1406.2560).
- Novelty sweep completed: the composed \(\sqrt\delta\cdot N\) theorem
  was not found (checked KŠdW SDPTs, Aaronson's find-all direct product
  quant-ph/0402095 Thm 10, Sherstov's hardness amplification
  (exponential-decay flavor, not \(\sqrt\delta\)), Lee--Roland,
  Bun--Thaler vanishing-error OR degree
  \(\Theta(\sqrt{n\log(1/\varepsilon)})\) — a decision-version scaling —
  and Beame et al. time-space tradeoffs). Correct \(N=1\) attributions:
  Zalka exact for one marked item; Dohotaru--Høyer Thm 8 +
  Carolan--Poremba Cor 2.4 for \(k\) marked. Evidence of apparent
  novelty, not proof of priority.
