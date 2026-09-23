# Compiled rational knots: source and novelty audit

Date: 2026-09-05. This is a bounded primary-source assessment of
`compiled-rational-knot-formulations.md`, not an independent proof review or a
claim that an exhaustive literature search establishes priority.

The strongest candidate contribution is the polynomial-size rational
pure-power formulation with binary-encoded exponents, retaining an additive
`O(r)` comparison against the minimum integer dimension of arbitrary convex
lifts. Boolean gate encodings, compilation of computations into linear
constraints, and even interpolation of circuit-specified function values all
have close predecessors. Present the compiler as an established construction
adapted to the integer-count objective.

## Exact antecedent for continuous gate variables

Avis, Bremner, Tiwary and Watanabe, *Polynomial size linear programs for
problems in P*, [author manuscript](https://arxiv.org/pdf/1408.0807), §3,
Lemma 1 and equations (14)–(16), give a polytope for a Boolean circuit whose
binary input fixes a unique extension, including binary values for all gate
variables. They call this the input-0/1 property. The construction uses linear
AND/OR/NOT constraints; the internal variables need no separate integrality
requirements once inputs are fixed. Lemma 1 explicitly credits Valiant,
*Reducibility by algebraic projections*, Enseignement Mathématique 28 (1982),
253–268. Their discussion also credits Yannakakis (1991). Theorem 1 treats
polynomial-size weak extended formulations for P/poly, and Theorem 2 relates
algorithm time and space to formulation size.

Thus the induction in candidate §1 is an instance of this known lemma.
The weak formulation can have fractional vertices: neither that source nor
the candidate warrants an ideal continuous relaxation.

Avis and Bremner, *Sparktope: linear programs from algorithms*,
[author manuscript](https://arxiv.org/pdf/2005.02853), §§2–4, make the
algorithm-to-LP construction explicit. They distinguish compile-time and
runtime data, bound program time and space, and enforce a controlled version
of the input-0/1 property. This is particularly relevant to the candidate's
fixed instance data, variable index bits, bounded arithmetic precision, and
fixed-length execution with early-termination flags. It is constructive prior
for compiling the knot algorithm, rather than just an existence result about
circuits.

## Close antecedent for interpolation of computed bits

Filos-Ratsikas, Hansen, Høgh and Hollender, *PPAD-membership for Problems with
Exact Rational Solutions: A General Approach via Convex Optimization*, STOC
2024, [accepted full manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/413786593/PPAD-Membership_FILOS-RATSIKAS_DOA08022024_AFV_CC_BY.pdf),
§3.4, already considers a piecewise-linear function whose integer-indexed
values are given succinctly by a Boolean circuit. Definition 3.5 specifies
linear interpolation between neighboring values. Lemma 3.4 translates Boolean
gates to piecewise-linear gates. Definition 3.10 and Lemma 3.7 implement
multiplication of a real variable by a number represented by computed output
bits. Proposition 3.2 constructs the interpolated function using a
piecewise-linear pseudo-circuit.

There is a material model distinction: their pseudo-circuits use linear-OPT
gates guaranteed for fixed-point/PPAD purposes. This is not an ordinary linear
extended formulation, nor a statement that only index bits must be declared
integer. Nevertheless, it is direct prior art for succinct circuit-based
interpolation and bitwise multiplication. Do not present either idea as new.

## Assessment of the proposed application

A direct mixed-integer predecessor is Adams and Henry, *Base-2 Expansions
for Linearizing Products of Functions of Discrete Variables*, Operations
Research 60(6), 1477–1490 (2012),
[primary Sandia manuscript](https://www.osti.gov/servlets/purl/1648449), §2,
pp. 3–7, equations (4)–(13). An arbitrary function on `n` discrete values and
its product with a nonnegative continuous variable use the same
`ceil(log2 n)` binaries, with `n` continuous selectors. This already supplies
the finite interpolation mechanism. Circuit evaluation provides succinct
size when the indexed values are efficiently computable. The full manuscript
was downloaded from OSTI and these sections were read.

The candidate combines the classical input-0/1 property with exact bounded
binary–continuous product constraints. Its useful bookkeeping observation is
that all computed endpoint bits can remain continuous, so evaluating more
complicated knots increases formulation size without increasing declared
integer dimension. This is a natural consequence of the cited tools, with
limited standalone novelty.

The more substantial claim uses certified inverse-power knots, computed in
time polynomial in `log D`, to obtain a rational compact formulation with
`p_out <= p_conv + 13r/2 + 1` for positive pure powers, including the existing
unconditional error-body assumptions. The source search did not locate that
whole-formulation comparison, its degree-independent integer overhead, or
the sparse-degree version in these predecessors. The finite lower bound and
the rational compact upper construction must both be cited to the relevant
local proofs; this source audit does not validate their mathematics.

The intended theorem should explicitly retain polynomial dependence on the
bit lengths of exponents and tolerance/allocation data. It should not promise
a strong LP relaxation, practical compilation size, or a polynomial algorithm
for solving the resulting MILP. These are different questions.

Searches covered Boolean-circuit extended formulations, algorithm-to-LP
compilation, succinct piecewise-linear interpolation, and mixed-integer graph
approximation. No exact matching integer-count theorem was found in this
bounded search. The direct 2024 interpolation precedent substantially narrows
the defensible novelty of the generic compiler while leaving the proposed
sparse pure-power precision application distinct among the checked sources.
