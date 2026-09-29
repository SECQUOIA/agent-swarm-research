# Convexity of the feasible set does not supply a convex representation

Date: 2026-09-28. Status: direct reduction checked against the original
Valiant–Vazirani theorem; independent adversarial review completed with no
substantive gap found.

The [SOCP feasibility result](socp-hessian-span-frontier.md) uses a supplied
conic representation to construct polyhedral outer approximations. A promise
that an arbitrary quadratic description has a convex feasible set cannot
replace that representation in a general polynomial-time theorem, unless
\(\mathrm{RP}=\mathrm{NP}\). This already holds with a supplied unit box
and exactly one Hessian direction. The observation combines a standard
Boolean encoding with an established randomized reduction; it is a scope
boundary, not a claimed original complexity theorem.

**Proposition.** Suppose a deterministic algorithm decides exact feasibility
in polynomial time for rational quadratic systems promised to have a convex
feasible set and constraint Hessian span one. Then
\(\mathrm{RP}=\mathrm{NP}\). The same conclusion follows if the algorithm
only needs to handle systems consisting of a unit box, affine inequalities,
and one concave quadratic inequality with Hessian \(-2I\).

**Proof.** For a CNF formula \(\phi\) on \(n\ge1\) Boolean variables,
introduce real variables \(x\in[0,1]^n\). Replace a positive literal by
\(x_j\), a negative literal by \(1-x_j\), and each clause \(C\) by

\[
 \sum_{\ell\in C}\ell(x)\ge1.
\]

Add the single quadratic inequality

\[
 q(x):=\sum_{j=1}^n x_j(1-x_j)\le0. \tag{1}
\]

Every summand is nonnegative on the box, so (1) holds exactly at its Boolean
vertices. The feasible set \(F_\phi\) is therefore exactly the set of
satisfying assignments of \(\phi\), with no auxiliary choices. The
construction has polynomial encoding length, and the sole nonzero Hessian
is \(-2I_n\), giving span dimension one. Inputs with no variables can be
decided directly.

A subset of \(\{0,1\}^n\) is convex exactly when it has at most one
element: the midpoint of two distinct Boolean vectors has a coordinate
strictly between zero and one. Thus the promise that \(F_\phi\) is convex
is precisely the promise that \(\phi\) has zero or one satisfying
assignment. The assumed algorithm consequently solves this promise problem
in deterministic polynomial time.

The Valiant–Vazirani reduction maps an unsatisfiable formula to an
unsatisfiable formula for every random choice. For a satisfiable input it
produces a uniquely satisfiable formula with inverse-polynomial probability.
Its parity constraints admit a polynomial-size CNF encoding that preserves
the number of solutions, by their Lemma 2.1. Apply the quadratic construction
and the assumed algorithm to each output. On an unsatisfiable input every
query meets the convexity promise and is rejected. On a satisfiable input,
each uniquely satisfiable output meets the promise and is accepted; answers
on outputs with several solutions can only increase the acceptance
probability. Polynomial repetition gives an RP algorithm for SAT, hence
\(\mathrm{NP}\subseteq\mathrm{RP}\). The reverse inclusion holds because
an accepting random string is a polynomial-size NP witness. This proves
equality. See Valiant and Vazirani, Theorem 1.1 and Corollary 1.2,
[original paper, pp. 86–88](https://www.cs.princeton.edu/courses/archive/fall05/cos528/handouts/NP_is_as.pdf).

The algorithm may behave arbitrarily outside the promise. If its stated
polynomial runtime bound applies only to promised inputs, clock it at that
bound and interpret a timeout as rejection. This preserves every required
answer and gives polynomial runtime on all queries. No answer outside the
promise needs to be trusted. \(\square\)

This is a conditional obstruction, not a proof that no such algorithm
exists and not a claim of deterministic NP-hardness under promise-preserving
reductions. The nonempty promised examples above are singletons; the argument
does not address a promise of full-dimensionality or a supplied interior
ball. It also does not obstruct the
[nonconvex algebraic-certificate theorem](nonconvex-hessian-span-frontier.md):
all feasible coordinates here are Boolean, but small certificates need not
be efficiently findable. Nor does it obstruct
exact algorithms given an explicit SOC or native convex-quadratic
representation. A singleton has a simple convex representation once its
coordinates are known; obtaining that information is the difficulty here.

**Sources examined.** L. G. Valiant and V. V. Vazirani, “NP is as easy as
detecting unique solutions,” *Theoretical Computer Science* 47 (1986),
85–93, [DOI](https://doi.org/10.1016/0304-3975(86)90135-0). The original scan
was read at printed pages 86–88: arbitrary behavior on multiple-solution
inputs, the randomized reduction and RP consequence, and the parsimonious
CNF encoding of parity constraints. The note uses the zero-versus-one
promise problem, not the different total language asking whether the number
of solutions is exactly one. No novelty is claimed for the reduction above.

**Verification.** The argument is symbolic and requires no numerical
experiment. The
[independent review](convex-representation-boundary-review.md) reconstructs
the isolation probability and checks the encoding, promise handling, and
runtime truncation. Its reasoning was then rechecked by this note's author.
A targeted `python - <<'PY'` check of both documents verified final newlines,
absence of trailing whitespace and control characters, and all four relative
Markdown links; all checks passed. No project-wide checks or CI inspection
were run.
