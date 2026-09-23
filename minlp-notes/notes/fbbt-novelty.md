# Novelty audit: continuous bilinear FBBT limits and iteration counts

Audit date: 2026-09-04. This is an independent literature assessment, not external peer review
or a proof of priority. Mathematical proofs are being reviewed separately by `review_fbbt`.
No result proof was changed during this audit.

Reviewed notes:

- `results/fbbt-monotone-system-hardness.md`
- `results/fbbt-doubly-exponential-convergence.md`

## Assessment

No earlier explicit PosSLP-hardness theorem for constant-error approximation of the continuous
bilinear FBBT limit was located. The restriction to continuous variables, feasibility-promised
unit boxes, primitive equations, and small directed feedback components distinguishes the
candidate from the closest constraint-programming hardness results found.

However, nearly all underlying machinery is established: monotone least fixed points, fair
propagation, the arithmetic-circuit hardness construction and its gap amplification, and slow
iteration. The defensible potential contribution is the precise transfer to FBBT with its
restrictions. It should not be presented as a new hardness mechanism or the first complexity
barrier for constraint propagation.

The doubly exponential note has a narrower novelty claim. Existing monotone polynomial examples
already imply doubly exponential *forward Kleene iteration* to attain constant error. What is
not located in prior work is the note's schedule-independent lower bound for primitive
forward-and-reverse interval-hull updates, with constant-size coefficients, no nonlinear
feedback component, and a two-variable final linear feedback component. Its robust treatment
of reverse propagation matters more than the slow affine recurrence alone.

## Closest primary sources and exact overlaps

### Bordeaux, Katsirelos, Narodytska and Vardi (2011)

[*The Complexity of Integer Bound Propagation*, JAIR 40:657–676](https://www.cs.rice.edu/~vardi/papers/jair11.pdf),
[DOI](https://doi.org/10.1613/jair.3248).

The paper proves NP-completeness of integer bound-propagation fixed-point existence already
for binary linear inequalities. Section 4.1, Proposition 3, gives NP-completeness with three
variables and two constraints, one linear equality and one squaring equality. The propagated
endpoints remain integers, with floor/ceiling in the inverse square operation. The notation
`bound(R)` means real-valued support for an integer endpoint; it does **not** make this a
continuous-variable hardness theorem.

Section 3.4.1 removes integer rounding, explicitly connects the resulting operators to FBBT,
and proves continuous linear fixed-point existence LP-solvable (Observation 2), independently
of Belotti and coauthors. Therefore the new note should credit both lines of work when
contrasting linear tractability with nonlinear hardness. This source does not establish the
candidate's feasible-instance constant-error continuous bilinear hardness.

### Bordeaux, Hamadi and Vardi (2007)

[*An Analysis of Slow Convergence in Interval Propagation*, CP 2007, pp. 790–797](https://citeseerx.ist.psu.edu/document?doi=de796a5f4931c256a88ac41d15c5a4321b4c55a9&repid=rep1&type=pdf).

This predecessor studies large integer ranges, slow propagation, and intractability of the
fixed-point problem. The 2011 paper identifies its quadratic integer hardness result as
originating here. It is relevant prior art for the problem motivation, not evidence that the
continuous PosSLP result was already proved. The 2011 author manuscript supplies the precise
integer/continuous distinction used in this audit.

### Belotti, Cafieri, Lee and Liberti (2012 preprint)

[*On feasibility based bounds tightening*](https://optimization-online.org/wp-content/uploads/2012/01/3325.pdf).

The paper models FBBT using fixed-point equations, describes non-finite convergence even for
linear constraints, and computes the continuous linear FBBT limit through linear programming.
Section 2.6 and Example 2.4 use two linear equalities with a parameter near one to exhibit slow
geometric contraction. Its introduction also warns that small successive improvements may
precede larger improvements. These ideas precede both candidate notes.

The new iteration example replaces a directly encoded near-one coefficient by a compact
bilinear circuit and proves a lower bound under all primitive update schedules. Its residual
versus distance warning specializes an established concern; the potential new content is the
explicit doubly exponentially small scale from constant-size input coefficients.

### Etessami and Yannakakis (2009)

[*Recursive Markov chains, stochastic grammars, and monotone systems of nonlinear equations*,
JACM 56(1)](https://homepages.inf.ed.ac.uk/kousha/final_rmc_jacm_version.pdf),
[DOI](https://doi.org/10.1145/1462153.1462154).

Theorem 5.2 proves polynomial many-one reductions from both square-root-sum and PosSLP to a
promised gap in a two-exit recursive Markov chain termination probability: at most any fixed
positive epsilon versus exactly one. The note explicitly adapts this circuit/sign/amplification
construction. The source already supplies the constant-gap monotone-system hardness; transferring
that result into a bound-tightening model is the part needing a separate novelty claim.

Section 6 contrasts slow ordinary iteration with Newton iteration. The fixed-point machinery
and the use of tiny circuit-represented quantities are established. No explicit FBBT or interval
contractor hardness transfer was found in the inspected manuscript.

### Esparza, Kiefer and Luttenberger (2010)

[*Computing the Least Fixed Point of Positive Polynomial Systems*, SICOMP 39(6):2282–2335](https://archive.model.in.tum.de/um/bibdb/kiefer/SICOMP.pdf),
[arXiv](https://arxiv.org/abs/1001.0340).

Section 7, Theorem 7.1, constructs positive quadratic systems with singleton strongly connected
components and a unique solution equal to the all-ones vector. Newton iteration requires
exponentially many iterations per bit because error is amplified along the component chain.
This is close prior art for small-component hardness intuition and very slow approximation.
It also shows that unique solutions and tiny feedback components are not novel features by
themselves. Its iteration theorem concerns Newton's method; it does not analyze the primitive
FBBT rules of the current note.

### Stewart, Etessami and Yannakakis (2015)

[*Upper bounds for Newton's method on monotone polynomial systems, and P-time model checking
of probabilistic one-counter automata*, JACM 62(4), article 30](https://homepages.inf.ed.ac.uk/kousha/final-jacm-cav13-jversion.pdf),
[DOI](https://doi.org/10.1145/2789208).

Section 4.1 gives the simpler established bad family
`x_0=(x_0²+1)/2`, `x_i=(x_i²+x_(i−1))/2`.
Its least fixed point is all ones. Solving successive components transmits an upstream error
`a` as `sqrt(a)`, and thus amplifies it to `a^(2^(−n))`. The paper proves exponential Newton
iteration requirements and explicitly discusses repeated-squaring systems with doubly
exponentially small coordinates. Its general upper bounds depend on component depth and
minimum positive fixed-point coordinates, so small component size alone is not a tractability
guarantee.

An immediate further inference is a doubly exponential **Kleene** lower bound: the bottom
iteration has error `e_(k+1)=e_k−e_k²/2`, hence `e_k≥1/(k+1)` (induction). Monotone iterates
above it have error at least `e_k^(2^(−n))`. Attaining top error at most `1/2` requires
`k+1≥2^(2^n)`. This inference is not identified as a separately stated theorem in the source;
it shows why broad novelty claims about doubly exponential monotone iteration are unwarranted.
It does not prove the current primitive reverse-propagation lower bound.

### Apt (1999)

[*The essence of constraint propagation*, TCS 221:179–210](https://ir.cwi.nl/pub/17342/17342A.pdf),
[arXiv](https://arxiv.org/abs/cs/9811024).

This established framework treats constraint propagation through fair or chaotic iteration of
monotone operators. The candidate's least-fixed-point lemma is a short specialized argument
within this tradition. Its soundness sandwich is useful for transferring hardness, but should
not be advertised as discovering the fixed-point semantics of propagation.

## Recommended claim scope

The primary result can be described as a candidate **continuous nonlinear counterpart** to
known linear FBBT fixed-point algorithms, obtained by transferring existing PosSLP gap hardness
and enforcing explicit primitive-form restrictions. Retain the distinction between approximating
the ultimate bound and finding a nearly stationary box. Neither PosSLP hardness nor the
iteration example establishes NP-hardness of the stated continuous problem.

The convergence companion is best described as an explicit worst-case construction for
primitive interval-hull propagation that survives arbitrary scheduling and reverse updates.
Keep its exact update rules and excluded acceleration mechanisms visible. Solving the final
linear subsystem after upstream substitution immediately defeats its slow recurrence, so it
is not an oracle lower bound against all ways of obtaining the limit.

The feedback restriction is on the directed defining-equation graph. It is not bounded
undirected treewidth, and it does not control arithmetic-circuit precision or the number of
upstream gates. The no-nonlinear-feedback convergence construction and the bounded-feedback
hardness construction should be distinguished carefully.

## Search record and remaining uncertainty

Searches included exact combinations of `FBBT`, `bound tightening`, `bound propagation`,
`interval propagation`, `constraint propagation`, `contractor`, `PosSLP`, `square-root-sum`,
`monotone polynomial systems`, `positive polynomial systems`, `doubly exponential`,
`Kleene`, and `fixed point`. Targeted searches of PosSLP with FBBT, bound tightening, and
interval propagation returned no relevant earlier transfer. Broader searches located the
primary sources above; source texts were checked for the pertinent distinction or statement.

This search does not establish nonexistence of an earlier transfer under different terminology.
Abstract interpretation, numerical constraint programming, and verification contain related
fixed-point work that is not exhaustively covered. The confidence is therefore **plausible
new restricted FBBT statement, substantial established ingredients, priority unconfirmed**.
The iteration result's contribution is narrower than the hardness theorem's.

Newly saved open primary sources, alongside the pre-existing Etessami–Yannakakis copy:

- `literature/external-fbbt/bordeaux-et-al-2011.pdf` and `.txt`
- `literature/external-fbbt/esparza-et-al-2010.pdf` and `.txt`
- `literature/external-fbbt/stewart-et-al-2015.pdf` and `.txt`
