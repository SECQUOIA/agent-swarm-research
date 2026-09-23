# Referee review: degree-three refinement (Lemma 2 and Theorem 3)

Date: 2026-09-05. Reviewer: independent referee agent. Subject:
[results/pooling-one-quality-degree-two-hardness.md](../results/pooling-one-quality-degree-two-hardness.md),
restricted to "Lemma 2 (bounded degree)", "Theorem 3 (bounded degrees on
both layers)", and the sentences that reference them (status line, summary,
paragraph after Theorem 3, Remark 4, verification section). Theorems 1–2 and
Lemma 1 were reviewed earlier and are used here only as far as Theorem 3
depends on them.

## Verdict

**PASS WITH CORRECTIONS.** Lemma 2 and Theorem 3 are correct. Both
directions of the Lemma 2 proof hold, the graph is simple and has maximum
degree three under the standard convention that a clause is a set of
literals, Lemma 1 preserves the degrees of original vertices and puts all
degree-three vertices in one class, and Theorem 3 follows from Theorems 1–2
exactly as stated. The corrections are presentational: the proof asserts
simplicity without stating the clause-as-set convention it relies on, and the
NP-hardness of the source problem At-most-3-SAT(2L) rests on an unproved
one-line remark in Asahiro et al.; a direct citation of Tovey (1984) closes
that gap. The status line and verification section must also be updated now
that the refinement has been reviewed. No claim changes.

## What was checked

### (a) Both directions of Lemma 2

Definition of the source problem. Asahiro et al. (JOCO 2011, Section 5,
text extraction at `/tmp/joco2011.txt`, lines 757–760) define
At-most-3-SAT(2L) as "a restriction of 3-SAT where each clause includes at
most three literals and each literal (not variable) appears at most twice in a
formula". The note's paraphrase ("each clause has at most three literals and
each literal occurs at most twice") is exact. The bound is on total
occurrences of a literal over the formula, which is what the forward
direction needs.

Forward direction (satisfiable to orientation). Variable edge into the false
literal vertex: false vertex load 2, true vertex load 0 from it. Triangles
cyclic: each triangle vertex load 2. Clause `c_j`: one chosen true literal
receives 1, the other two unit edges enter `c_j`, load 2. A true literal
vertex receives only clause edges in which it is the chosen literal, at most
one per occurrence, so at most 2. False literal vertices and triangle vertices
receive nothing else because all their clause edges point into the clause
vertices. Correct.

Reverse direction (orientation to assignment). A triangle carries three
weight-2 edges over three vertices of capacity 2, so each vertex receives
exactly one, load exactly 2, and every clause edge incident to a triangle
vertex must enter the clause vertex. The variable edge enters exactly one of
the two literal vertices; that vertex has load 2 and its clause edges must
leave it. A clause vertex has exactly three unit edges and load at most 2, so
at least one unit edge leaves it; its head is not a triangle vertex and not a
false literal vertex, hence a true literal vertex. Each variable has exactly
one true literal vertex, so the assignment is well defined and satisfies every
clause. Correct. The argument is carried out directly in the in-load form, so
no reversal of Asahiro's outdegree statement is needed.

Edge cases. A one-literal clause is padded by two triangle vertices; the
proof covers it. An empty clause (not part of the source problem) would be
padded by all three triangle vertices, and the construction would correctly
report infeasibility (load 3 at the clause vertex); nothing needs to be said.
A clause containing both `x` and `¬x` produces the triangle
`c_j – x – ¬x` (weights 1, 1, 2), which is simple, and both directions of the
proof go through unchanged (one of `x`, `¬x` is always true). Such clauses
need not be excluded.

### (b) Simplicity

The only way a parallel edge can arise is a clause containing the same
literal twice (two weight-1 edges `c_j – ℓ`). Distinct clause vertices,
per-clause fresh triangles, and "distinct vertices of that triangle" rule out
every other duplication. The proof says "The graph is simple" without stating
that clauses are sets of literals. That convention is standard (Garey–Johnson
define a clause as a set; Tovey states explicitly "no repeated variables in a
clause") and is what the source hardness proof delivers, so the lemma is
correct, but the proof should say so. Should a reader's instance repeat a
literal, deleting the duplicate shrinks the clause, the triangle padding
restores degree exactly three, and occurrence counts only decrease, so
nothing is lost either way. Recommended text below.

### (c) Maximum degree three

Literal vertex: one variable edge plus one edge per occurrence, at most 2,
total at most 3. Clause vertex: exactly 3 by padding. Triangle vertex: two
triangle edges plus at most one clause edge, because the clause joins
`3 - |c_j| ≤ 2` distinct vertices of its own triangle. Correct.

### (d) Lemma 1 on the Lemma 2 graph

Replacing `{u,v}` by `u – m_e – v` leaves `deg(u)` and `deg(v)` unchanged and
gives `m_e` degree 2. The bipartition is original versus subdivision vertices,
so all degree-three vertices (clause vertices, and literal vertices with two
occurrences) lie in the original class and every vertex of the other class
has degree exactly 2. Capacities become `T_v = 2` on original vertices and
`T_{m_e} = w_e ∈ {1,2}`, so weights and capacities lie in `{1,2}` as claimed.
The subdivided graph is simple. The sentence after the proof ("keeps the
degrees of the original vertices and adds subdivision vertices of degree two;
the original vertices form one class") is accurate.

### (e) Theorem 3

Theorem 1's construction on a bipartite CO instance gives inputs out-degree
1, pools in-degree 2 and out-degree 2, and output `v` in-degree `deg_H(v)`;
Theorem 2's mirror gives input `v` out-degree `deg_H(v)`. On the Lemma 2
graphs after Lemma 1, `deg_H(v) ≤ 3` for every vertex (original vertices at
most 3, subdivision vertices exactly 2). Either class may play the role of
`U`. The numerical data are unchanged from Theorem 1 (costs in
`{-2,-1,0,1}`, capacities `T_v` and `w_e` in `{1,2}`, qualities and bounds in
`{0,1}`), so "All data are as in Theorem 1" is correct and strong
NP-hardness carries over. The proof of Theorem 3 is complete as written.

The paragraph after Theorem 3 ("the only degree pattern ... not settled ...
is the one in which all four bounds are simultaneously at most two") is
correct: any pattern with a pool bound of 1 is polynomial (Remark 2), any
pattern dominating `(1,2,2,3)` or `(3,2,2,1)` is hard, and what remains is
exactly the class with all four bounds at most 2 (including its
sub-patterns). Remark 4 is consistent with Theorem 3. The summary sentence
"and the remaining layer of degree at most three (Theorem 3)" is correct but
"remaining layer" is vague; see the optional rewording below.

### (f) NP-hardness of At-most-3-SAT(2L)

Asahiro et al. only say it "can easily be proved ... by using problem [LO1]
on p. 259 of Garey and Johnson (1979)"; they give no proof, and the note
inherits this. I could not check the wording of the [LO1] comment in
Garey–Johnson (the book is not available to this project). The standard
precise source is Tovey (1984), whose text I read (author PDF mirrored at
`https://cedric.cnam.fr/~bentzc/INITREC/Files/CB11.pdf`): Theorem 2.1 states
that satisfiability is NP-complete "when restricted to instances with 2 or 3
variables per clause and at most 3 occurrences per variable", under the
stated convention "no repeated variables in a clause". His construction
replaces a variable `x` with `k` occurrences by `x_1, …, x_k`, substitutes
`x_i` for the `i`-th occurrence, and appends the cycle clauses
`{x_i ∨ ¬x_{i+1}}` (indices mod `k`). Applied to every variable with at
least two occurrences, each `x_i` occurs exactly once in an original clause,
once positively and once negatively in cycle clauses, so every literal occurs
at most twice; a variable with a single occurrence trivially has each literal
at most once. Hence At-most-3-SAT(2L), with clauses as sets, is NP-complete
by Tovey's Theorem 2.1 directly. (The alternative derivation from
"each variable at most three times" by pure-literal elimination also works,
but needs the Garey–Johnson statement that this reviewer could not verify.)
The note should cite Tovey directly and keep the Asahiro/Garey–Johnson
pointer as the source's own attribution.

### Brute-force script

`code/pooling_degree_two/check_degree_three_gadget.py` runs in 0.1 s and
prints `247 satisfiable, 158 unsatisfiable formulas` (405 total, matching the
note). Inspection of the code:

- `random_formula` rejects a literal already in the clause and the
  complementary literal (`(v, s) in lits or (v, 1 - s) in lits`), so no clause
  repeats a variable; the graph-simplicity assertion is therefore never
  stressed by repeated literals, and tautological clauses are never produced.
  It also enforces at most two occurrences per literal over the formula.
- Unsatisfiable cases are genuinely tested: the equivalence
  `sat == orientable` is asserted in both directions, the five fixed cases
  include the complete two-variable contradiction and the four-clause
  `{x∨y∨z, ¬x, ¬y, ¬z}`, and 158 of the random formulas are unsatisfiable
  (small formulas with unit clauses make this common).
- `orientable` is a complete backtracking search (both heads tried per edge),
  and `satisfiable` enumerates all assignments. Degrees are asserted `≤ 3`
  only; clause-vertex degree exactly 3 is implied by the construction but
  not asserted.

Referee's independent check (script at `/tmp/ref_check_lemma2.py`, reusing
`build`, `orientable`, `satisfiable` from the repository script): exhaustive
enumeration of all formulas over 1–3 variables whose clauses are sets of 1–3
literals (tautological clauses `x ∨ ¬x` allowed, repeated literals
impossible), with 1–4 clauses as a multiset and each literal occurring at
most twice. For each of the 42,140 formulas (3,121 unsatisfiable; 30,188
containing a tautological clause) it asserted: no parallel edges or loops,
maximum degree 3, every clause vertex of degree exactly 3, satisfiable iff
orientable with in-load at most 2, and additionally that the Lemma 1
subdivision (`T = 2` on original vertices, `T_{m_e} = w_e`) preserves
original degrees, gives subdivision vertices degree 2, and is orientable iff
the formula is satisfiable. All assertions passed (32 s).

## Issues

**I1 (minor, proof gap).** The claim "The graph is simple" in the Lemma 2
proof depends on clauses being sets of literals, which is not stated.
Recommended text, replacing "The graph is simple, and its maximum degree is
three:" with:

> Clauses are sets of literals, as in Tovey (1984) and Garey and Johnson
> (1979), so no literal vertex is joined twice to the same clause vertex (a
> clause containing both `x` and `¬x` is allowed and produces the simple
> triangle `c_j – x – ¬x`). The graph is therefore simple, and its maximum
> degree is three:

**I2 (minor, sourcing).** NP-hardness of At-most-3-SAT(2L) is asserted by
Asahiro et al. without proof. Recommended: after the sentence "We rerun the
reduction of Asahiro et al. (Section 5) from At-most-3-SAT(2L), in which each
clause has at most three literals and each literal occurs at most twice,"
add:

> At-most-3-SAT(2L) is NP-complete: Tovey (1984, Theorem 2.1) proves
> NP-completeness of satisfiability with two or three distinct variables per
> clause and at most three occurrences per variable, and his construction
> (replace a variable with `k ≥ 2` occurrences by `x_1, …, x_k` and add the
> cycle clauses `x_i ∨ ¬x_{i+1}`) makes every literal occur at most twice.
> Asahiro et al. attribute the same fact to problem [LO1] of Garey and
> Johnson (1979); that text was not checked by this project.

and add to Sources:

> - C. A. Tovey, A simplified NP-complete satisfiability problem, Discrete
>   Appl. Math. 8 (1984) 85–89. Theorem 2.1 and the construction preceding it
>   were read in the author PDF
>   (`https://cedric.cnam.fr/~bentzc/INITREC/Files/CB11.pdf`).

**I3 (editorial, required).** Update the status and verification text now
that the refinement has been reviewed. Status line (lines 3–5): replace
"the later Lemma 2 and Theorem 3 refinement awaits review (see the
verification section)" with "a third review passed Lemma 2 and Theorem 3
with minor corrections (applied)". Verification section, last bullet:
replace "the root agent wrote that proof and its brute-force check after the
review, so Lemma 2 and Theorem 3 have not yet been independently reviewed."
with:

> the root agent wrote that proof and its brute-force check after the
> review.
> - [Third review (Lemma 2 and Theorem 3)](review-pooling-degree-three-refinement.md):
>   PASS WITH CORRECTIONS (clause-as-set convention made explicit; Tovey
>   cited for At-most-3-SAT(2L)). The referee's exhaustive check over all
>   formulas with at most three variables, at most four clauses, and each
>   literal at most twice (42,140 formulas, 3,121 unsatisfiable, tautological
>   clauses included) confirmed Lemma 2 and the Lemma 1 subdivision on top of
>   it.

**I4 (optional, clarity).** Summary sentence "and the remaining layer of
degree at most three (Theorem 3)": suggest "and the one layer that is not of
degree one (outputs in the first class, inputs in the second) of degree at
most three (Theorem 3)".

**I5 (optional, script).** To make the repository check cover the case the
proof now mentions explicitly, allow tautological clauses in
`random_formula` (drop the `(v, 1 - s) in lits` test, or add a fixed case such
as `(1, [[(0, 0), (0, 1)]])`), and assert `deg[('cl', j)] == 3` for every
clause. Neither affects the lemma; the referee's run already covers both.

## Not covered

Theorems 1–2, Lemma 1's proof, the Gurobi cross-checks, and the novelty
audit were reviewed earlier and are not re-examined here beyond the degree
and data facts Theorem 3 uses from them.
