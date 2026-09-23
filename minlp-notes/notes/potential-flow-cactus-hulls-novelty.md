# Cactus uncertainty hulls: bounded literature audit

Date: 2026-09-05. Scope: source comparison for [the candidate](potential-flow-cactus-uncertainty-hulls.md), not an independent proof audit.

The 2025 JOTA cactus characterization does **not** state the candidate's nonlinear uncertainty-hull theorem. However, the candidate's adjoint-current sign mechanism is classical, and a directly relevant 1993 nonlinear tolerance paper remains unread. The broad claim that cactus pressure monotonicity or endpoint tolerance analysis is new is therefore **not cleared**. Retain the candidate as a qualified structural result, with its strongest potentially distinct part being the necessity construction for a fixed common quadratic law and its explicit positive hull gap.

## The 2025 theorem concerns a different property

Brandenberg and Stursberg, *Extremal Solutions for Network Flow with Differential Constraints: A Generalization of Spanning Trees*, JOTA 207, article 70 (2025), [publisher full text](https://link.springer.com/article/10.1007/s10957-025-02792-4), DOI 10.1007/s10957-025-02792-4. Read the full HTML and corresponding 31-page PDF, especially §3.

Definitions 1.1–1.2 use linear DC flow with fixed positive elasticities and edge-flow/node-injection bounds. Definition 3.1 and Theorem 3.1 characterize when conforming alpha-trees identify extreme points for every choice of bounds and weights: this universal nondegeneracy holds exactly on cactus graphs. Example 3.1 uses a balanced Wheatstone bridge; Proposition 3.1 recalls cactus equivalences involving a diamond topological minor. These are PDF pages 16–20. The end of §3, PDF page 22, relates the graph class to adding an arbitrary edge and obtaining a confluent/series-parallel graph, citing Duffin. Neither the theorem nor its proof asserts resistance-box pressure extrema for nonlinear passive states.

Our comparison: the same obstruction graph does not identify the same mathematical property. In fact, the linear case separates them, as explained below. Cite this paper for related extremal-flow topology, not as either an exact predecessor or evidence that the candidate's graph-theoretic mechanism is new.

## Duffin supplies the classical sign mechanism

R. J. Duffin, *Topology of Series-Parallel Networks*, Journal of Mathematical Analysis and Applications 10 (1965), 303–318, DOI 10.1016/0022-247X(65)90125-3, [open university PDF](https://sites.math.washington.edu/~reu/papers/current/jim/duffin.pdf). Read the full paper.

Section 2 defines confluence of an edge pair by consistency of their relative orientations in circuits containing both. Theorem 0, printed pages 306–307 (PDF pages 4–5), states that the direction of current in one edge produced by a battery in another is independent of resistance values exactly when the pair is confluent. Theorem 1 characterizes confluent graphs by exclusion of an embedded Wheatstone network. Here the illustrated Wheatstone includes its source branch; do not silently identify it with the five-edge diamond used by the 2025 paper. Section 5, printed pages 314–316 (PDF pages 12–14), extends series/parallel constructions to nonlinear monotone resistors; Theorem 4 gives circuit characteristics from addition and inversion for a single source on a confluent graph.

Our inference: introducing the terminal-pair adjoint source maps the candidate's resistance-independent adjoint-current orientation directly to this classical framework. The positive cactus argument is consequently a natural application of confluence plus a nonlinear state-comparison argument. No novelty should be assigned to the sign mechanism, the cactus/diamond graph equivalence, or series/parallel nonlinear reduction itself. The single-source nonlinear construction is not an explicit theorem about arbitrary fixed nominations and independent uncertain edge parameters.

## Important missing predecessor: nonlinear parameter tolerances

Hasler and Wang, *Parameter tolerances in non-linear resistive circuits: worst case analysis based on monotonicity*, International Symposium on Nonlinear Theory and its Applications, Hawaii, 1993, pages 841–846.

Its bibliographic existence is supported by reference 2 on PDF page 20 of Stefano Pastore, *DC tolerance analysis of electronic circuits by polyhedral circuits*, DOI 10.1002/cta.2098, [open author-institution postprint](https://arts.units.it/retrieve/e2913fde-d2e2-f688-e053-3705fe0a67e0/2869823_10.1002-cta.2098-PostPrint.pdf). Pastore's introduction, PDF page 1, describes that predecessor as obtaining rigorous lower bounds on worst-case parameter tolerances in nonlinear resistive circuits. I inspected the introduction and bibliography; this is a citation lead, not direct evidence of the 1993 theorems.

Targeted exact-title, author, page-range, NOLTA, and EPFL searches did not locate an openly readable copy. The 1993 source has **not been read**. Its title directly overlaps the proposed positive tolerance result; absence of retrieved text cannot clear novelty. A later review must inspect its parameter model, topological assumptions, and whether it proves exact endpoint extrema or only certified tolerance bounds.

Further lead: Hasler–Wang, *Monotonic dependence on sources in nonlinear resistive circuits*, AEU 46(4), 242–249 (1992). Its citation is confirmed in the references of the authors' [*Convexity of Resistive Circuit Characteristics* manuscript](https://infoscience.epfl.ch/bitstreams/d2fb4e43-bb7e-42b7-977c-39560d9e7d46/download). Only indexed portions of that manuscript were usable; subsequent full-text requests failed. Do not treat either source as fully reviewed. Source monotonicity and circuit-parameter monotonicity need separate comparison.

## Linear laws provide a useful distinction

The following is our mathematical comparison, also independently suggested by the candidate author; it is not attributed to the JOTA paper. Ground one vertex, fix balanced injections (b), and let one edge conductance vary by (t-t_0). With reduced incidence vector (a),

\[
L(t)=L_0+(t-t_0)aa^T,
\qquad
F(t)=c^TL_0^{-1}b-
\frac{(t-t_0)(c^TL_0^{-1}a)(a^TL_0^{-1}b)}
 {1+(t-t_0)a^TL_0^{-1}a}.
\]

For positive conductances, the denominator is positive and the derivative has a constant sign. Thus a fixed terminal potential difference is separately monotone in each conductance, and therefore in each positive resistance, on **every** connected graph. Compact product sets and their interval hulls have the same extrema in this linear setting. The candidate's noncactus necessity cannot follow merely by substituting the JOTA linear degeneracy example. The common quadratic law and its strict interior extremum supply a real distinction.

## Recommended claim and priority

The defensible present statement is: “We give a cactus characterization of exact independent-set interval-hull replacement for passive pressure extrema, with an explicit counterexample for a common quadratic law on every noncactus graph. The sufficiency proof applies classical circuit confluence; novelty relative to earlier nonlinear tolerance theory remains under review.”

The explicit theta example, its rational (1/24) gap, and extension to arbitrary noncactus graphs are the most concrete parts not located in the sources read here. This is a bounded negative search result, not proof of novelty. The positive result may be a useful corollary or reformulation of classical nonlinear circuit theory. The endpoint replacement implication, once separate monotonicity is available, is elementary. Joint optimization over an arbitrary nomination set inherits the same pointwise replacement and is not by itself a separate topological discovery.

Priority: retain the fully audited mathematics and precise scope, but do not rank this as a cleared major new topology theorem until the 1993 paper is compared. The known mechanism and unresolved predecessor should appear next to any publication or impact assessment.
