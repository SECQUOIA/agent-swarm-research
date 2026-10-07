# Stage 3, round 1: independent review 2

**Severity counts: 0 major, 0 minor.** I found no required repair in the
reviewed mathematical claims, oracle contracts, or cited applications.

I reviewed all of `sections/06-lp-application.tex`, the complete source
note `workbench/active/2026-09-04-sparse-lp-newton-access-separation.md`,
and `audit/stage3-author.md`. I did not read peer reports or edit the
manuscript. The unfinished introduction and general literature discussion
are outside this stage's scope.

## LP realization and the meaning of the direction

**Location:** `sections/06-lp-application.tex:5–50`.

The bases are orthonormal, with

\[
q_+^T\mathbf1=2\sqrt{2/3}=a,\qquad
q_-^T\mathbf1=a\sqrt\delta,\qquad
q_0^T\mathbf1=\cos\theta/\sqrt3>0.
\]

The assumed bound on `delta` makes `0 < sin(theta) < 1`, so the last
strict inequality holds. The singular values of `A_t` are `1` and
`sqrt(t)`, giving its rank, operator norm, and the stated normal-matrix
condition number. The entry bound follows from its operator norm.

The feasible set is exactly the intersection of
`1 + lambda q_0` with the orthant. Orthogonality to the strictly positive
vector `q_+` forces the nonzero vector `q_0` to have both signs. Thus the
allowed lambda interval is bounded on both sides and contains an open
neighborhood of zero. This proves both compactness and nontriviality.
The objective has strictly positive slope `cos(theta)/sqrt(3)` on the
line, so the construction is not a constant-objective example.

The central point satisfies primal feasibility, dual feasibility,
strict positivity, and complementarity at `mu=1`. With the stated dual
sign convention, eliminating the predictor equations gives

\[
\Delta s=-A_t^T\Delta y,\quad
\Delta x=-\mathbf1+A_t^T\Delta y,\quad
A_tA_t^T\Delta y=A_t\mathbf1.
\]

These equations yield precisely the displayed dual direction. They also
give

\[
\Delta x=-(q_0^T\mathbf1)q_0
        =-(\cos\theta/\sqrt3)q_0.
\]

The manuscript explicitly states the resulting limitation: the feasible
segment, objective, and primal predictor are independent of the hidden
parameter, while the dual coordinate direction varies. The state lower
bound is correctly framed as a lower bound for that specified dual
output, not for solving the LP or obtaining its primal predictor.

## State oracle contracts and lower bounds

**Location:** `sections/06-lp-application.tex:52–125`.

The full normal and factor unitaries are specified. The singular-pair
blocks verify the factor oracle's unitarity, including its action on
the column null vector; public padding introduces no hidden side
channel. The right-side preparation unitary is also fully specified and
its calls are counted. Withholding the exact right-side norm is material
and correctly stated: its formula would otherwise reveal `t`.

The endpoint target overlap gives exactly
`d_rho=(sqrt(rho)-1)/sqrt(2(rho+1))`. The oracle norm differences are
`O_rho(delta)` for normal access and `O_rho(sqrt(delta))` for factor
access. The restriction `rho delta < 1/4` puts even the factor's
singular-value parameter below `1/2`, as required by the displayed
rotation estimate. The preparation oracle differs by only
`O_rho(delta)`. The hybrid argument therefore retains the claimed
orders when all permitted query types are counted. Purification and
contractivity of trace distance justify its application to adaptive
state algorithms with a bounded worst-case count.

## Matching amplitude-estimation upper bounds

**Location:** `sections/06-lp-application.tex:127–153`.

The two proposed preparations have success probabilities `t^2` and `t`,
respectively. The [BHMT Theorem 12](https://arxiv.org/pdf/quant-ph/0005055)
bound and success probability are stated correctly. Counting both the
preparation and its inverse changes only the constant in `O(M)`.

For normal access, the square-root conversion is valid even if the
estimate is zero:

\[
|\sqrt{\widehat a}-t|
 =\frac{|\widehat a-t^2|}{\sqrt{\widehat a}+t}
 \leq\frac{|\widehat a-t^2|}{t}.
\]

Together with `t>=delta`, this gives the displayed additive error of
order `delta` for `M>=C/delta`. For factor access, using
`sqrt(t)<=sqrt(rho delta)` gives the stated error for
`M>=C/sqrt(delta)`. Clipping to the known interval cannot increase
distance to the true parameter.

Each independent run succeeds with probability at least `8/pi^2`,
strictly above one half. A fixed odd repetition count, chosen as a
function of the fixed requested error, makes the probability of a bad
median at most `epsilon_0/2`. Majority-good estimates ensure the median
is within the same interval of accuracy. The algorithm does not need
to identify the successful runs.

The angle derivative is

\[
|\varphi'(t)|=\frac{\sqrt\delta}{2\sqrt t(t+\delta)}
             \leq\frac1{4\delta}.
\]

Hence a successful estimate has pure-state trace error at most
`epsilon_0/4`. Since all failure outputs are still valid states,
convexity gives unconditional error at most
`epsilon_0/4 + epsilon_0/2 < epsilon_0`. The result does not depend on
postselection or an expected stopping time. This proves the sharp
orders asserted in the theorem and validly improves the source note's
logarithm-suppressed factor upper bound. The optional pseudoinverse
identity and the support overlap `(8/9)(1+delta)` also check out.

## Compiler transfer, bypasses, and scope

**Location:** `sections/06-lp-application.tex:155–213`.

The normal oracle's varying sector has exactly the scalar sine/cosine
completion used earlier. Extending that sector periodically produces a
unitary family for every real angle. The designated compressed
`u_-` matrix element remains a bounded trigonometric polynomial even
when the algorithm mixes the two public eigenspaces. Thus the
low-interval lower bounds transfer. The compiler contract explicitly
excludes `B_t`, whose entries would require a different argument.

The positive tiers and joint-accuracy upper bounds follow from the
earlier polynomial constructions with `c=1`. The coarse tier correctly
has **zero** query cost here: the public contraction
`(1-m_rho delta)P_-` has error at most `G_0 delta`. Public spectral
projectors make this family different from the general promise problem.
This is an appropriate correction to an unqualified complete-hierarchy
transfer from the source note.

For factor access, the even singular-value transform `1-s^2` produces
the desired operator on the row space. Independently, direct
multiplication confirms

\[
J_{\mathcal R}^*U_A(I-\Pi_{\mathcal C})U_A^*J_{\mathcal R}
 =I_{\mathcal R}-A_tA_t^T.
\]

A free block encoding of the public projector gives the explicit
two-query implementation. Its output has no extra column-null-space
eigenvalue.

Both digital entry formulas reveal the hidden parameter, and
`(q_-)_1` is strictly positive throughout the stated domain. The
normalization-two LCU construction uses one controlled normal-oracle
call as claimed. These bypasses, the fixed dimension, the public primal
predictor, and the limits on end-to-end interpretations are all stated
clearly. The [Orsucci–Dunjko discussion](https://quantum-journal.org/papers/q-2021-11-08-573/pdf/)
supports the cited prior factor improvements, overlap dependence, and
normalized-complement input requirement; Section 4.3 also contains the
relevant digital diagonally-dominant construction. The manuscript does
not present those general observations as new results.

## Independent numerical checks

Using `/workspace/local-home/miniconda3/envs/qipm/bin/python`, I checked instances
with `rho=1.01,2,10`, `delta=1e-2,1e-4,1e-6`, and endpoint and midpoint
values of `t`. The checks included the bounded feasible interval and
positive objective slope, `A A^T=H`, the normal equation, both remaining
predictor equations, unitarity of both matrix oracles, the projector
compression, both amplitude-estimation success probabilities, and the
endpoint state distance. The largest matrix/vector identity residual
was `8.881784197001252e-16`.

These floating-point checks supplement the algebra above. They do not
serve as certificates for continuum or asymptotic statements. No package
was installed, and no manuscript or source-note file was changed.
