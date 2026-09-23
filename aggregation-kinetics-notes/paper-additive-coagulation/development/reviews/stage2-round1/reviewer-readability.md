# Stage 2 independent review: readability and full mathematical check

I reviewed both new sections in full, their use of the Stage 1 solution framework and appendix, the current bibliography, README, and coverage map. I did not read other current Stage 2 reports or communicate with other reviewers. I built and inspected a separate copy in /tmp/stage2-readability-juubpvud; no shared manuscript or build file was changed.

The main Stage 2 results are mathematically sound as written. The proof of marginal identification is sufficiently detailed and avoids relying on an unexplained uniqueness theorem for an unbounded forward operator. The distinction between the auxiliary number process and a physical particle lineage is clear. The logarithmic hypotheses are separated correctly, including the difference between an extended transport cost and ordinary first-moment Wasserstein convergence.

## Required correction

### S2-RDB-01 — MINOR: distinguish lattice reference laws from the coagulation–fragmentation law

**Location:** sections/log-limits.tex:269–275, the paragraph after the logarithmic limit theorem, especially “equal splitting can preserve a lattice in log size.”

**Reason:** In this location the statement is naturally read as describing the full coagulation–fragmentation law, with positive coagulation rate. Equal splitting preserves a fixed logarithmic lattice for the pure-fragmentation reference started from one size, but addition of unequal sizes does not preserve it. Starting from size one, equal splitting permits sizes one and one half; their coagulation produces three halves, whose logarithm is outside the lattice of integer multiples of \(\log 2\). In fact the three logarithms \(0,-\log 2,\log(3/2)\) do not lie on any common arithmetic lattice, since that would require \(\log(3/2)/\log 2\) to be rational. The intended warning about density convergence is correct, but this example conflates two different obstructions.

**Fix:** Replace the sentence with a precise example: “For monodisperse initial data and equal splitting, the full size law remains supported on a countable set, so it need not have a density. The pure-fragmentation reference is supported on a logarithmic lattice.” A concise alternative is to retain only the countable-support example. Positive dyadic rational sizes form a countable set closed under addition and halving, which supplies the required example for the full model.

This is an explanatory correction; it does not affect the weak central limit theorem, functional limit, or any quantitative bound.

## Mathematics and hypothesis scope checked

- **Jump representation:** Dividing by the exact count balance yields the stated number generator, including fragmentation rate \(2\sigma\) and coagulation rate \(\lambda N x\). The environment has first moment \(m/N\). The stopped Lyapunov argument uses a finite first moment and correctly allows overshoots at the size boundary. It provides a uniform expected stopped jump count and hence nonexplosion.
- **Marginal identification:** The prescribed jump flux is \(2\sigma+b\). The loss formula retains the full incoming gain when the output coordinate is restricted. Positive successive substitution dominates every finite-jump term of the minimal process; nonexplosion makes their total mass one. This establishes equality of the marginals without imposing a second size moment.
- **Change of sampling weight:** The inverse-size generator calculation has the correct coagulation and fragmentation terms and eigenvalue \(\sigma-b\). Its stated role is algebraic; the argument does not use it to assume a physical lineage or an unproved transformed path law.
- **Finite correction:** The logarithmic increment estimate gives \(a(t)\le \lambda H(t)^2/N(t)\). Combining it with Stage 1 gives the displayed controlled tail. Monotone convergence proves both almost-sure finiteness and \(L^1\) convergence, including the finite-total-activity case where the coarser exponential bound itself need not vanish.
- **Finite event count:** The daughter product has conditional multiplier mean one half even with parent dependence. Its deterministic finite-horizon bound makes the compensated product a true martingale on every finite horizon. The maximal bound and finite \(A_\infty\) give finite integrated coagulation intensity pathwise. Stopping that continuous compensator justifies finite total jumps. The separate identity \(\mathbb E K_\infty=B_{\mathrm c}(\infty)\) is compatible with almost-sure finiteness and is not confused with an integrability conclusion.
- **Controlled path dichotomy:** Diverging fragmentation activity sends the auxiliary size to zero through the bounded compensated product; finite activity gives finitely many fragmentation events. Combined with finite coagulations this proves eventual constancy in the latter case. The weak limits use the appropriate state spaces.
- **Transport:** Parent independence supplies independent Poisson marks. The ordered coupling and clipped one-Lipschitz tests prove exact extended transport cost without subtracting potentially infinite means. The signed remainder estimates concern paired increments and do not introduce hidden absolute logarithmic moments.
- **Constant-rate and limit results:** The constants \(D_0,\omega,r\) and their critical specializations agree with the controlled bound. The functional central limit proof reduces to iid unit-time increments and controls the within-interval error using the second jump moment. The variance is the raw Poisson variance \(r\mathbb E Y^2\). The uniform correction bound transfers convergence in \(J_1\). The weak limits require no initial log moment; ordinary transport limits add the stated first initial log moment. The first-moment truncation argument proves the slower, unquantified transport law of large numbers.
- **Remaining statements:** The infinite-mean speed conclusion, deterministic split examples, arbitrary diverging-scale transfer, mean-log identity, geometric-mean prefactor, and relative-entropy identity have the correct hypotheses and signs. The pure-coagulation endpoint and Borel example are consistent with finite log cost and diverging arithmetic mean.

## Exposition and Stage 1 integration

The new sections are sufficiently explanatory for a mathematical population-balance reader. In particular, the text explains why formal forward equations are insufficient, why a finite number of auxiliary coagulations does not mean coagulation stops in the population, and why parent dependence prevents the independent fragmentation reference. The proofs distinguish the finite correction from an independent additive error, which matters for both the probability limits and the interpretation.

The relevant Stage 1 integration is consistent: the construction assumes Definition 1.2 rather than silently invoking the stronger second-moment existence class; the half-moment estimate is available at that level; and the appendix's loss identity now explicitly includes the local integrable bound used in marginal identification. The current notation and claims in the coverage map agree with the new sections. Unwritten later stages are outside this review.

Two optional audience aids would make the probability machinery easier to enter without altering the proofs:

1. At first use, identify a jump-count compensator as the time integral of its conditional jump rate, whose stopped expectation equals the stopped expected count.
2. Describe \(D([0,S],\mathbb R)\) as the space of right-continuous paths with left limits, and briefly say that \(J_1\) permits small changes in jump times. The displayed uniform transfer estimate already supplies the substantive argument.

These are optional exposition preferences, not additional issues.

## References and isolated build

The classical Borel formula and its equation-number attribution agree with [Bertoin (2009), equation (3)](https://www.numdam.org/item/10.1016/j.anihpc.2008.10.007.pdf). The pure-fragmentation literature descriptions match the mass-weighted formulations in [Bertoin (2003)](https://ems.press/content/serial-article-files/31511?nt=1) and [Doumic–Escobedo, Corollary 1](https://arxiv.org/pdf/1510.03588). The [publisher's contents for Billingsley](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316962) place the continuous-path material in Chapter 2, consistent with citing that chapter for the interpolated invariance principle.

The isolated make succeeded and produced a nineteen-page PDF with resolved citations and cross-references and no overfull or underfull boxes. Its final pass emitted a label-rerun warning. I ran one additional PDFLaTeX pass in the same isolated directory: the warning disappeared, the auxiliary file was unchanged, and the extracted PDF text was identical. Thus I found no incorrect printed reference or substantive build failure. A representative page containing the functional central limit theorem and proof was visually legible.

**MAJOR count: 0. MINOR count: 1. Recommendation: accept Stage 2 after correcting S2-RDB-01. The main proofs are clean.**
