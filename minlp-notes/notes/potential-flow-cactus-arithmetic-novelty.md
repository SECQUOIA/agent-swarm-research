# Novelty audit: exact quadratic potential comparison on cacti

Date: 2026-09-05. Scope: independent literature and computational-model audit of [the cactus investigation](potential-flow-mpd-cactus-investigation.md) and [its mathematical review](review-potential-flow-cactus-arithmetic.md).

**Assessment:** no prior polynomial-time many-one equivalence between Square-Root Sum and exact quadratic single-source/single-sink cactus MPD threshold comparison was found. The parallel-resistance formula, homogeneity, and series-parallel reduction are established. The candidate's distinct contribution is an exact arithmetic classification with a rational-input reduction and a matching upper reduction. Novelty remains provisional after this bounded search.

## Precise candidate and contribution

The target model has positive rational resistances, the law

\[
\pi_u-\pi_v=\beta_e x_e|x_e|,
\]

one source \(s\), one sink \(t\), and nominations \(b_s=q=-b_t\), \(0\le q\le1\). The decision is whether the maximum \(\pi_s-\pi_t\) is at least a rational threshold. Source and sink are also the objective terminals. No switches, potential bounds, or arc capacities are used in the MPD definition.

The independently reviewed result identifies this problem on arbitrary connected cacti with the explicitly defined weak comparison

\[
\sum_i\sqrt{a_i}\le K
\]

for positive binary-encoded integers. The lower reduction already uses simple degree-three cacti made of triangular cycle blocks and bridges, positive integer resistances, and known flow directions. The reverse reduction uses the fact that the effective resistance on a cactus is a rational term minus a sum of positive square roots of rationals. These restrictions and the comparison direction should accompany any theorem statement.

## Closest series-parallel result and its arithmetic scope

Groß, Pfetsch, Schewe, Schmidt, and Skutella, *Algorithmic results for potential-based flows: Easy and hard cases*, appeared in **Networks 73(3), 306–324 (2019), DOI 10.1002/net.21865**. The repository's 2017-report URL serves a manuscript dated **May 31, 2018**. Lemma 4.2 gives series and parallel effective-resistance reductions. For quadratic laws, its parallel rule equals \(AB/(\sqrt A+\sqrt B)^2\). Theorem 4.3 states that a passive two-terminal series-parallel graph reduces to one arc using \(O(|A|)\) applications of this lemma. Theorem 3.7 asserts efficient computation of a feasible-flow interval, with its proof starting from unit flow and corresponding potentials. Section 2.1, **printed p.3 / PDF page index 2**, explicitly names the Turing model, discusses root approximation at fixed error, and does not provide an exact radical-threshold comparison algorithm. It would therefore misdescribe this source to call it exclusively a real-RAM paper. [Open manuscript](https://optimization-online.org/wp-content/uploads/2017/08/6185.pdf), [published DOI](https://doi.org/10.1002/net.21865).

Our assessment of the distinction is as follows. A theorem counting reduction operations constructs an expression for the effective resistance. The expression can be compact while exact comparison with a rational number is difficult. Merely evaluating its radicals to a prescribed fixed error does not settle a threshold instance arbitrarily close to equality. The candidate explicitly supplies a polynomial-size rational instance that encodes such comparison. Thus it sharpens the arithmetic interpretation of the known reductions; it does not invalidate the reduction identities or the stated number of reduction applications.

The broad wording about efficient computation deserves acknowledgment in any publication. A careful discussion should say that the existing proof does not establish the stronger exact, zero-gap Turing comparison guarantee. Do not claim that the authors explicitly proved the SRS equivalence, nor that the paper is simply erroneous. Resolving the exact threshold problem in polynomial bit time would, by the new reduction, also resolve the specified SRS problem in polynomial time.

## Contemporary source explicitly separates irrational arithmetic and approximation

Klimm, Pfetsch, Skutella, and Strubberg, *Approximating the Network Design Problem for Potential-Based Flows*, arXiv:2604.26882, posted **2026-04-29**, is newer than the January survey. Remark 8 explicitly discusses irrational numbers arising from rational inputs. For its exact shortest-path result it assumes transformed arc lengths are supplied as rationals. For subsequent approximation results, it explains that bounded precision addresses the arithmetic issue even though the exposition uses exact calculations. Section 4.1, Lemma 10 credits Groß et al. for series-parallel effective-resistance composition and applies it in a dynamic program. No SRS discussion or exact cactus MPD classification was found in the full text. Its stated network-design algorithms do not supersede the candidate threshold result. [Open preprint](https://arxiv.org/abs/2604.26882).

This paper is a useful citation for the practical distinction: numerical approximation algorithms can remain efficient despite exact comparison having an unresolved arithmetic complexity. The candidate should not be presented as an approximation-hardness result.

## What the 2026 cactus open question actually says

Pfetsch, Schmidt, Skutella, and Thürauf, *Potential-Based Flows—An Overview*, January 2026 draft, printed pp.9–10, defines MPD with bounded entry and exit nominations and without additional potential or arc-capacity bounds. Its objective can compare any two specified nodes. On printed p.10 it says that nonlinear MPD on cacti has an open hardness question; it contrasts this with polynomial cases for trees and a single cycle and known NP-hardness on general networks. [Open survey](https://optimization-online.org/wp-content/uploads/2026/01/ch_potential.pdf).

The candidate is a classification of the **one-entry, one-exit, terminal-objective subclass** in the exact bit model. It gives a lower bound for the general cactus problem, but does not prove that general cactus MPD reduces to SRS. It also does not establish NP-hardness of cactus MPD. Accordingly, claiming to have completely solved the survey's general cactus complexity question would be too broad.

## Single-cycle polynomial algorithm is genuinely a bit-model result

Labbé, Plein, Schmidt, and Thürauf, *Deciding feasibility of a booking in the European gas market on a cycle is in P*, open manuscript at the 2019 URL, has an explicit two-stage computational analysis in Section 6, printed pp.24–27. Theorem 6.4 reduces each structural configuration to at most nine real variables and 42 polynomial constraints. Theorem 6.5 invokes real algebraic decision methods at fixed dimension and bounds rational coefficient encoding lengths; Corollary 6.6 concludes polynomial-time booking validation on a single cycle. Thus this result is not merely a unit-cost arithmetic claim. [Open manuscript](https://optimization-online.org/wp-content/uploads/2019/11/7472.pdf).

There is no conflict with the candidate: one cycle has only a bounded number of relevant algebraic interactions after that structural reduction. A chain with an unbounded number of independent cycle blocks can accumulate an unbounded radical sum even when no internal nodes have nominations. Combining exact subproblem solutions by numerical addition needs its own comparison analysis.

## Other checked leads

Rico Raber's 2022 dissertation, *Optimization, Reduction, and Robustness of Potential-Based Flow Networks*, includes recovery of cactus networks from effective-resistance data in Section 5.3.3. Full-text searches for radical comparison, Turing computation, square-root sums, and arithmetic complexity found no candidate-equivalent result. Its cactus recovery question concerns reconstructing networks from data, rather than exact comparison of a rationally specified network's terminal drop. [Primary dissertation](https://d-nb.info/1258349914/34).

Brandenberg and Stursberg, *Extremal Solutions for Network Flow with Differential Constraints: A Generalization of Spanning Trees*, JOTA 207, article 70 (2025), appeared in cactus-related searches. Its Definition 1.2 uses the **linear** relation \(f_{vw}=b_{vw}(\phi_w-\phi_v)\); its cactus conclusions concern extreme points of a polytope. It is not a nonlinear quadratic MPD result. [Published open paper](https://link.springer.com/article/10.1007/s10957-025-02792-4).

## Recommended positioning

A suitable statement is: **Known series-parallel reductions admit a compact exact expression, but rational-threshold comparison already captures Square-Root Sum on passive triangular cacti with one source and one sink. Conversely, every such single-source/single-sink cactus threshold comparison reduces to Square-Root Sum.**

The result is useful as a precise arithmetic barrier for extending single-cycle algorithms. It demonstrates that fixing flow directions and eliminating uncertainty in internal nominations do not remove exact comparison difficulty. Its impact is narrower than an NP-hardness theorem or a new approximation algorithm, but it supplies a complete arithmetic equivalence for a sharply defined network class.

## Search record and remaining uncertainty

Searches combined potential-based flow, potential flow, gas network, water network, hydraulic, nonlinear network, resistance, series-parallel, cactus, MPD, exact comparison, Turing, arithmetic complexity, Square-Root Sum, SQRT-SUM, and sum-of-square-roots. No directly matching antecedent appeared. The primary texts above were inspected either through the repository, public PDF extraction, or publisher full text. Downloaded supporting texts are in `/tmp/minlp-graph-novelty/` under `potential2026`, `potential_thesis`, and `cycle`; these temporary files are not the durable record.

The published 2019 Wiley page returned HTTP 403 to the browsing tool, so the theorem-number audit uses the openly accessible May 2018 manuscript. No communication with authors was attempted. Unindexed papers, theses, unpublished observations, or differences in the final version remain possible. The result should therefore retain a provisional novelty label until a publication-level citation review is complete.
