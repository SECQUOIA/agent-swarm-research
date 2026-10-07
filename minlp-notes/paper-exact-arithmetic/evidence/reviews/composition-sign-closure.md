The deterministic October 3 structured-box and separable-flow exact predicates admit polynomial-time many-one reductions to one PosSLP instance. The September 28 adaptive integer-sign compiler removes their adaptive oracle calls. This changes the reduction form of already established deterministic P^PosSLP upper bounds; it supplies no hardness result for these subclasses and no algorithm for the unrestricted constrained problem.

This bounded analytic audit is dated 2026-10-05. I read [the adaptive compiler](../../../research-20260928/algebra/adaptive-integer-sign-circuit-compilation.md), [the prewriting reductions audit](prewrite-reductions.md), and the relevant portions of [the constraints audit](prewrite-constraints.md). I used the already audited arithmetic interfaces for the box and flow QP solvers. I did no browsing, source discovery, experiments, or mathematical checker reruns. Publication priority belongs to the separate literature audit. This report owns no writer files.

Use L for total explicit binary input length, including the objective f, rational curvature modulus mu>0, constraint data, requested explicit observable h, and the requested relation. Polynomials have degree at most four; the same reasoning applies when objective and observable degrees are fixed constants and the corresponding transfer theorem is stated for those constants. Circuit representation always means a shared directed acyclic graph. Arithmetic circuits have binary addition, subtraction, and multiplication gates and constants zero and one.

**The composed theorem.** Let p be the unique minimizer of an explicit globally mu-strongly convex rational quartic on either of these domains:

1. A rational box, with fixed coordinates substituted out, where every Hessian interaction is contained in a supplied forest, or every Hessian has nonpositive off-diagonal entries. The broader promise that each comparison matrix is positive definite also suffices.
2. A rational network-flow polyhedron, where f is a sum of univariate arc polynomials. The graph and constraint rank are unrestricted.

Allow infinite endpoints in both cases. For every supplied explicit rational polynomial h of degree at most four and every relation in {<,<=,=,!=,>=,>}, a deterministic polynomial-time algorithm constructs one division-free integer arithmetic circuit C such that, on every nonempty promised input,

\[
 C>0\quad\Longleftrightarrow\quad h(p)\mathrel{\bowtie}0.
\]

Feasibility, an explicit convention for an empty minimum, and valid checked curvature/structure certificates can be included in the language. Invalid supplied certificates then map to a fixed negative circuit before optimizer predicates are interpreted. With semantic structural or curvature promises alone, the statement remains a promise reduction; the construction need not recognize those promises. In all cases, it can be made total and polynomially bounded on arbitrary encodings by syntax checks and a clock.

An active-bound equality is one such predicate. Any polynomial-size specified Boolean combination of observable signs or active-bound predicates also reduces to one instance. This does not encode a whole output vector into one oracle answer. The complete active mask can instead be recovered from a polynomial, nonadaptive list of compiled single-predicate instances, one for each finite original bound. The theorem does not assert PosSLP-hardness or PosSLP-completeness for the structured classes.

**The original-input bound is uniform.** The relevant [Newton transfer](../../../research-20261003-arithmetic/constrained-exact/structural-newton.md) uses an ordinary exactly feasible rational warm start with objective error min(1,mu/(8K^2)), where K=max(1,M/(2mu)) and M is a rational Hessian-Lipschitz bound on a supplied containing box. These constants have polynomial encoding length. The approximation algorithm is deterministic polynomial bit time in the printed data and required accuracy. Its output rational vector therefore has polynomial total encoding length.

If endpoints are infinite, obtain a polynomial-bit feasible q and set R=1+2||grad f(q)||_1/mu. Strong convexity and f(p)<=f(q) give ||p-q||<R. Intersect every interval with [q_i-R,q_i+R]. This is polynomial-time preprocessing, preserves the box or flow structure, and places p strictly inside every added bound. Empty domains and zero-dimensional domains are ordinary rational branches. No circuit-encoded infinite magnitude is introduced.

For a feasible iterate x, the exact Taylor QP gives N(x) with

\[
 \|N(x)-p\|\le K\|x-p\|^2,
 \qquad
 \|x_j-p\|\le K^{-1}2^{-2^j}.
\]

The singleton KKT formula of the original printed input gives an effective polynomial a such that a nonzero h(p) has magnitude at least gamma=2^{-2^{a(L)+1}}. A polynomial-bit bound on ||grad h|| and O(a(L)) exact Newton iterations make |h(x_j)-h(p)|<=gamma/8. These are uniform polynomial schedules chosen from the original encoding, not from expanded iterates or unknown active faces. The separation and derivative-bound proof is already reconstructed in the two prewriting audits.

For boxes, each Taylor solve takes at most 2n pivots and polynomially many rational arithmetic operations and comparisons, independently of the expanded coefficient lengths. Fresh principal-system solves give O(n^4) arithmetic operations. Forest sign selection, comparison-matrix construction, and d=B^{-1}1 and v=(H+B)d/2 use polynomially many additional operations. The admissibility and pivot proofs in the constraints audit include zero slopes, tied events, and degenerate bounds. Ratios are taken only on positive-denominator branches and principal systems are positive definite. Since n<=L under the explicit input convention, a polynomial number of Newton steps preserves a polynomial bound in L.

For flows, the [recorded quadratic-flow interface](../../../research-20261003-arithmetic/constrained-exact/network-flow-review.md) is an exact strongly polynomial elementary-arithmetic and comparison algorithm, with a polynomial bound in graph size independently of coefficient encoding lengths. Fixed arcs, isolated nodes, capacity gadgets, and artificial arcs change graph size by only a polynomial factor. Its quadratic implementation uses rational linear systems and rational parametric search, with no additional root or unrestricted rounding oracle. The audited theorem supplies a worst-case operation bound rather than an expected one. Fix all ordinary tie choices deterministically.

High artificial-arc costs do not invalidate this bound. After finite-capacity normalization, bound absolute quadratic derivatives on each printed flow interval by a rational circuit C0>=1, using endpoint evaluations and absolute values. For N gadget nodes, the cost M0=N C0+1 works: derivative residual potentials of an original optimum can be chosen in [-(N-1)C0,0], so artificial reduced costs are strictly positive. The original optimum extended by zero artificial flow is optimal in the augmented graph, and strict positivity forces every augmented optimum to use zero artificial flow. The proof uses the unknown potentials only to justify this explicit cost. Its construction uses polynomially many circuit operations and sign tests, without inspecting coefficient expansion lengths. The strongly polynomial solver's count does not depend on the possibly large numerical value of M0.

Fixed polynomial degree makes derivative evaluation, Taylor-coefficient construction, and explicit h evaluation polynomial in L and stored circuit size. The flow objective must remain separable, while h may couple several arcs. The compiler itself does not require a degree restriction, but the current optimization proof does. Sparse binary exponents of unbounded degree are outside this composed theorem unless a separate uniform transfer bound is supplied.

Thus there is a fixed effective polynomial p such that the entire deterministic decision procedure has at most p(L) ordinary bit operations for preprocessing and circuit-description management, arithmetic operations, numerical comparisons, and oracle-query gates. Gate indices use O(log p(L)) bits. The maximum query-description length is also polynomial in L. No step expands the numerator or denominator of a circuit value. I found no reason the audited box or flow algorithms lack this uniform bound. A generic bit-polynomial QP algorithm, or one retaining expanded Hessian-encoding dependence, would fail this check and is not being substituted for either source algorithm.

**Rational operations become integer circuit queries.** Build every explicit signed integer constant from its binary digits using doubling, addition of zero or one, and optional negation. This includes the original rational numerators and denominators, the ordinary warm-start output, and rational derivative bounds. All take polynomially many zero/one arithmetic gates. Generate gamma by repeated squaring from 1/2; it has polynomial circuit size, although its expanded denominator is large.

Represent a rational value by integer circuits (P,Q), with Q>0. Addition, subtraction, and multiplication use common-denominator formulas. For division by a nonzero rational P2/Q2, use

\[
 \frac{P_1/Q_1}{P_2/Q_2}
  =\frac{P_1Q_2P_2}{Q_1P_2^2}.
\]

Each operation adds constantly many shared gates, and the denominator remains positive. A comparison of P1/Q1 and P2/Q2 is the sign of P1 Q2-P2 Q1. Equality is the Boolean conjunction of the two nonpositive strict-sign tests. Absolute values and ratio-order tests use these same integer sign queries. Every division is justified by the QP solver's valid execution and the positive-definite matrix systems. The generally irrational p is never inserted as an arithmetic constant.

For v=h(x_j), three final rational expressions are

\[
 v-\gamma/2,\qquad v+\gamma/2,
       \qquad\gamma^2/4-v^2.
\]

They are strictly positive exactly for h(p)>0, h(p)>=0, and h(p)=0, respectively; negation handles the remaining relations. For equality, a true zero gives |v|<=gamma/8, whereas a nonzero value gives |v|>=7gamma/8. The equality test is therefore a robust sign predicate, not a test that a rational Newton iterate already equals its generally irrational limit. Apply it to h=x_i-l_i or h=u_i-x_i for each finite original box or flow bound. Redundant balance equations and fixed arcs pose no problem. Feasibility and ordinary certificate rejection can return fixed Boolean values without invoking Newton refinement.

The result so far is a deterministic polynomial-time oracle Turing machine whose queries are division-free integer circuit signs. Every later circuit description may depend on earlier answers. The next two paragraphs prove that this adaptivity can be removed without enumerating answer transcripts.

**A bounded interpreter accounts for changing query descriptions.** Let T be a fixed polynomial bound on decision time and query length. Clock the machine for T steps and pad early terminal configurations by copying their Boolean result. Unroll its Boolean configurations. AND, NOT, and OR on exact bits are respectively ab, 1-a, and a+b-ab. At each possible query step attach a query module; ignore its answer if the control state does not issue a query.

The query module parses and validates a possibly answer-dependent binary SLP description, reserving polynomially many instruction slots. For each slot, compute Boolean indicators for the opcode, operand indices, and availability of earlier operand slots. Select an operand by a sum of earlier slot values multiplied by the corresponding address indicators. Invalid or forward addresses select zero. Compute sum, difference, and product candidates and select the requested opcode by Boolean multiplication and addition. Select the output slot similarly, apply H(v)=1[v>0], and conjoin the answer with the validity bit. All intermediate values are integers, and all malformed descriptions still produce defined integer expressions. Padding uses zero/one slots and preserves the designated output; if an encoding requires the last slot as output, append a copy using addition of zero. The construction has polynomially many gates in T: it enumerates possible bounded addresses, not possible answer transcripts. Parser, selector, machine-control, and padding gates all count toward its total size S.

On valid promised inputs the exact machine follows valid divisions and the exact source algorithm. To make the constructed interpreter total on arbitrary inputs and artificial control histories, enforce syntax limits and the clock and implement each arithmetic instruction by its integer pair formulas; an invalid instruction can return a fixed reject state. Testing a proposed zero divisor by integer sign/equality gates is also a permissible guard if needed. This changes no valid execution. The integer arithmetic/threshold circuit obtained from the clocked machine is defined on every Boolean input and has a Boolean terminal result, which is what the compiler requires. Its eventual approximate internal controls need not be Boolean: the global compiler error bound covers their arithmetic gates as well.

**The threshold compiler has a complete uniform error proof.** Consider this integer arithmetic/threshold circuit of total size S>=1. Every exact intermediate magnitude is at most B=2^{2^S}: start with bound two, and at each binary arithmetic gate at most square the prior bound; thresholds output zero or one. Set Lambda=3B and epsilon=2^{-2^{2S+4}}, so epsilon Lambda^S<1/4.

For M>=1, F_M(x)=2Mx/(M+x^2) preserves sign and maps 1<=|x|<=M into 1<=|F_M(x)|<=sqrt(M). The lower bound follows because the convex polynomial t^2-2Mt+M is nonpositive at t=1,M; the upper bound follows from M+t^2>=2sqrt(M)t. Shared repeated squares generate M_j=2^{2^j}. Applying F_{M_{S+2}},...,F_{M_1} compresses magnitude in [1,M_{S+2}] to [1,2].

If an exact threshold input v is an integer and its current rational approximation vtilde differs by at most 1/4, x=4vtilde-2 is at least one for v>=1 and at most minus one for v<=0. Also |x|<=4B+3<=B^4=M_{S+2}. Compress it as above and apply G(x)=2x/(1+x^2) exactly 2S+5 times. The first application sends signed magnitudes in [1,2] to [4/5,1]. Subsequently

\[
 1-G(t)=\frac{(1-t)^2}{1+t^2}\le(1-t)^2
       \quad(0\le t\le1),
\]

so error from the correct sign is at most 2^{-2^{2S+4}}. Return (1+z)/2 to approximate the exact threshold bit with error at most epsilon.

Replace all arithmetic gates by the same operations on approximations and all threshold gates by this rational construction. Inductively, after topological gate i the maximum error is at most epsilon Lambda^i. Addition and subtraction multiply prior error by at most two; multiplication multiplies it by at most 2B+1, since |ab-atilde btilde|<=2B delta+delta^2 and delta<1. Threshold replacement has its own error at most epsilon, because the preceding bound is below 1/4. This induction includes arithmetic decoder/control gates. The final approximate Boolean result lies below 1/4 when the exact result is zero and above 3/4 when it is one.

For a rational pair P/Q with Q>0, the threshold macro uses only integer pair updates

\[
 F_M(P/Q)=\frac{2MPQ}{MQ^2+P^2},\qquad
 G(P/Q)=\frac{2PQ}{Q^2+P^2}.
\]

Every displayed denominator is strictly positive. The ordinary arithmetic pair updates and conversion (1+z)/2 preserve positivity as well. There are O(S) macro operations per threshold and at most S thresholds, so the resulting shared division-free integer DAG has O(S^2) gates. If its final approximate Boolean pair is P/Q, the single integer output 2P-Q is positive exactly when the original machine accepts. All input bits can now be hardwired. Construction requires polynomial time in S, performs no oracle query, and never prints B, epsilon, or any expanded huge integer.

Combining the uniform optimization bound, bounded interpreter, and threshold compilation proves the composed theorem. Uniformity is essential: a particular successful execution having short circuits, without a computable bound on every valid execution, would not justify a polynomial-size unrolling. Both deterministic structured solvers meet the required bound at their audited arithmetic interfaces.

**Parameter bounds and randomness retain their original limits.** The same compiler works for a deterministic parameterized algorithm with total ordinary/oracle time and maximum query length at most F(k)L^C. Its interpreter and compiler then have size and construction time F1(k)L^{C1}, with absolute exponents after absorbing fixed powers of F into F1. This is an FPT many-one reduction to PosSLP; it is not a uniform polynomial-time reduction when k grows as part of the input. Merely taking a nonadaptive batch of FPT many queries does not make its total length polynomial in L.

For example, combine the ordinary mixed-integer candidate list with deterministic structured continuous-fiber comparisons, provided every candidate fiber has the required box or separable-flow form. Pairwise products preserve the concrete structural classes: disjoint forests remain forests, block-diagonal Z-matrix Hessians remain Z-matrices, and disjoint union preserves separable flows. Substituted input lengths are polynomial in the candidate list's total encoding, and joint curvature passes to fibers and products. Exact threshold predicates and selection predicates for any specified candidate block therefore have FPT many-one PosSLP reductions. If one asks for an entire optimal integer block or all blocks, these are multi-bit outputs; compile their decision/output-bit predicates separately. The ordinary nonlinear-dimension FPT algorithm also yields an FPT reduction, even trivially by deciding first and returning a fixed yes or no instance. Neither observation reduces the varying-parameter runtime to polynomial time.

A Las Vegas expected-time rank algorithm does not meet the deterministic bounded-machine hypothesis. An expected bound is not a worst-case clock, and fixing a random seed is not a proof that a bounded deterministic execution succeeds on every input. A truncated run can fail to produce an answer, so its circuit is not an exact predicate for the original problem. The compiler can represent any particular bounded run with its random bits as extra inputs, but it neither eliminates randomness nor chooses successful bits. The existing constraint-rank and its mixed composition therefore remain Las Vegas oracle results. A separately proved deterministic algorithm would be needed for the corresponding deterministic many-one claim.

For arbitrary constrained quartics the missing circuit-Hessian QP interface remains missing. The compiler transforms a proved deterministic bounded oracle decision procedure; it does not supply that procedure. UP^PosSLP intersect coUP^PosSLP is likewise not converted into deterministic PosSLP by this argument, since the nondeterministic active-mask guess is not eliminated.

The historical October 3 statements that only establish Turing reductions are sound as proofs made without the closure lemma. In the new manuscript, their composed deterministic predicate theorems can be stated with the stronger polynomial many-one upper bound and a direct reference to the proved adaptive compilation lemma. Keep their original structural, encoding, promise, and output assumptions. No claim that the composition is new is needed.

Verification here was analytic reconstruction and inspection of the recorded source interfaces. The scoped command `git diff --no-index --check /dev/null paper-exact-arithmetic/evidence/reviews/composition-sign-closure.md` produced no whitespace diagnostics; exit status one records that the new file differs from the empty file. No executable mathematical test was run. No project-wide verification or CI status/log inspection was performed.
