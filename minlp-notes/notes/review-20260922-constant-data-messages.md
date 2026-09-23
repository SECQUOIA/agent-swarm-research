# Independent review of fixed-data scalar indicator messages

Date: 2026-09-22. Reviewed
[the constant-data message note](research-20260922-constant-data-messages.md)
and its exact checker. This is a fresh proof and significance review. I did
not edit the author note.

**Verdict:** I found no mathematical defect in Propositions 1, 3, and 4 or
Theorems 2, 5, and 6. In particular, the two-extreme-prefix bound and the
worst-horizon accuracy exponent are correct with the displayed constants
and quantifiers. The result is a useful restricted representation theorem.
It does not establish hardness of optimizing this fixed-data family or a new
general principle of quadratic-basis approximation. An additional direct
literature comparison is recommended below.

## Exact formulas and the indicator lift

For a fixed support, inactive controls must have error zero. After this
restriction, the terminal constraint is one linear equation in the active
control errors and all recurrence residuals. The squared norm of its
coefficient vector is exactly

\[
D_z=\sum_{j=0}^{n-1}\theta^{2j}
       +\sum_{i=1}^n\theta^{2(n-i+1)}z_i.
\]

The stated Cauchy--Schwarz equality point obeys the inactive-coordinate
restrictions and reconstructs the prescribed terminal state. Thus the
formula is an attained minimum, not just a relaxation bound.

The center separation argument is valid for every horizon, including
\(n=1\). If the leading differing power is \(k<n\), the tail estimate
dominates \(\theta^n\); if it is \(k=n\), equality holds. Since
\(D_z\in[1,C_\theta]\) and \(C_\theta<2<4\), the radius
\(\theta^n/3\) gives strict dominance over every other quadratic.
At the zero center its intersection with the domain contains a nonempty
ordinary open interval. The polynomial-identity argument therefore proves
necessity for arbitrary finite polynomial dictionaries and finite piecewise
polynomial representations. It is stronger than counting candidate supports.

I reassembled the matrix entries. Internal state rows have diagonal
\(1+\theta^2\) and absolute off-diagonal sum at most
\(3\theta+\theta^2\); the terminal state row has diagonal one and
row sum at most \(2\theta\). Control rows also satisfy the claimed
Gershgorin bounds. The triangle-chain description, degree bound, and
treewidth/pathwidth statements are correct. For fixed rational \(\theta\),
all local coefficients belong to a fixed finite alphabet; the distinction
between ordered-chain and indexed sparse encodings is appropriate.

The state-indicator lift is sound even after conditioning the terminal state.
The translated residual form is the same positive definite quadratic form.
Each disabled state has translated error at most \(-4\), while turning it
off saves only one indicator penalty. Hence a point with \(k\) disabled
states costs at least \(n+10.2k\). The all-on comparison point costs at
most \(n+1\), so every conditional minimizer has all states on. The
expanded linear-coefficient bound of eight also holds at the initial and
terminal stages, including a one-stage horizon.

One useful limitation deserves explicit emphasis: the *unconditioned*
fixed-data model is easy. For every control support, setting \(x=z\)
and following the exact recurrence makes all residual squares zero.
Its unshifted optimum is zero. In the lifted model all states can be on,
giving optimum \(n\); the same activation bound excludes any improvement
by disabling states. There are exponentially many zero-residual optimal
control supports. Thus the construction stresses an exact conditional
message interface, not optimization of its unconstrained terminal objective.

## Theorem 5: two extreme prefixes

The essential estimate is geometric. Write \(c_0\le c_z\le c_1\)
with \(c_1-c_0=\delta\). Choose the endpoint closest to \(t\).
Outside this interval that endpoint is no farther from \(t\) than
\(c_z\). Inside it the endpoint distance is at most \(\delta/2\).
Consequently, with \(N=(t-c_z)^2\), its numerator satisfies
\(N'\le N+\delta^2/4\).

The denominator change needs separate control because the closest endpoint
need not have the larger denominator. Both denominators are at least one,
their difference has absolute value at most \(\beta\), and \(N\le1\)
on the stated domain. Therefore

\[
\frac{N'}{D'}-\frac{N}{D_z}
\le \frac{\delta^2}{4D'}
    +\frac{N(D_z-D')}{D'D_z}
\le \frac{\delta^2}{4}+\beta.
\]

This proves the claimed bound uniformly, including the regions between
support centers. It does not assume that the selected endpoint support is
itself optimal. Cases \(m=0\) and \(m=n\) are valid: the first retains
the two extreme full supports; in the second the two prefix choices coincide
and the approximation is exact. The bound of \(2^{m+1}\) pieces is an
upper bound allowing these duplicates. Keeping \(W_n\), rather than
replacing it by \(W_m\), is essential and is done correctly.

## Theorem 6: accuracy and horizon quantifiers

For every \(n\ge m\), supports with zero omitted prefix have exactly
the length-\(m\) digit centers. Their separation is \(\theta^m\),
independent of \(n\). At each center the full value is zero. A retained
quadratic reaching error at most \(\varepsilon\) there must have its
center within \(r=\sqrt{C_\theta\varepsilon}\). If
\(2r<\theta^m\), no one retained quadratic can serve two of these
zeros. This is a valid necessary condition for approximation on the whole
interval, and yields the stated \(2^m\) lower bound.

With \(L=\log(1/\theta)\) and
\(m=\lfloor\log(1/(8C_\theta\varepsilon))/(2L)\rfloor\),
one has \(\theta^{2m}\ge8C_\theta\varepsilon\), so the strict
separation condition holds. Also \(2^m\ge
\tfrac12(8C_\theta\varepsilon)^{-\alpha_\theta}\).
For small enough accuracy this \(m\) is at least one, and the supremum
over horizons permits taking \(n=m\), or any larger horizon.

The upper-bound ceiling gives
\(A_\theta\theta^{2m+2}\le\varepsilon\). For horizons
\(n\le m\), keeping all \(2^n\) supports handles the small-horizon
case; for larger horizons Theorem 5 gives the uniform bound. The factor four
after rounding is correct. No interchange of a horizon limit and an accuracy
limit is needed. Constants may depend on the fixed \(\theta\), as the
notation explicitly states. The conclusion does not say that a fixed finite
horizon needs infinitely many pieces as accuracy vanishes: it saturates at
\(2^n\).

## Literature and significance

I independently inspected these primary sources on 2026-09-22:

- Gaubert, McEneaney, and Qu, [*Curse of dimensionality reduction in max-plus
  based approximation methods: theoretical estimates and improved pruning
  algorithms*](https://arxiv.org/pdf/1109.5241), introduction, Section III,
  and Section VI. Section VI already formulates deletion of basis functions
  under uniform error as a continuous k-center problem. Its smooth
  approximation results include cardinality/error exponents under different
  assumptions. Thus a covering interpretation and a power law for quadratic
  pruning are established background. They do not directly prove the present
  fixed-data indicator construction or its exponent: the present message is
  a nonsmooth lower envelope, its denominators vary with the support, and the
  center set is a separated digit set.
- Bhathena, Fattahi, Gómez, and Küçükyavuz, [*Solving Convex Quadratic
  Optimization with Indicators Over Structured Graphs*](https://arxiv.org/html/2603.02103v1),
  Definition 5, Lemma 9, and Theorem 1. Its positive complexity bound uses
  a margin condition in addition to structural and conditioning parameters.
  Its margin evaluates specified restricted QPs with bag variables set to
  zero. The present lift shifts the relevant terminal interval away from
  zero. Counting its wells therefore does not, by itself, calculate that
  paper's margin parameter. The author note correctly avoids such a claim.

The exponent also has a transparent geometric interpretation, derivable
directly from the note's digit-separation and tail estimates. The limiting
center set is generated by the two contractions
\(x\mapsto\theta x\) and \(x\mapsto\theta+\theta x\).
Its covering-number exponent is \(d=\log2/\log(1/\theta)\):
there are \(2^m\) separated depth-\(m\) clusters of diameter comparable
to \(\theta^m\). The squared-distance error scale gives
\(\alpha_\theta=d/2\). This is not a new fractal-dimension law. The
nontrivial model-specific step is realizing the digit geometry with a
strictly convex fixed-data indicator objective and controlling the varying
denominators well enough to get the matching upper bound.

I recommend adding the Gaubert--McEneaney--Qu comparison to the author note.
The currently cautious novelty and algorithmic qualifications otherwise
fit the evidence. A positive guarantee for general stable indicator dynamics
would need additional work; the example alone cannot support it. This review
is not an exhaustive priority search.

## Targeted verification

I inspected the imported direct residual-row QP solver as well as the new
checker. The solver actually assembles the original least-squares problem
on each active support and solves its rational normal equations; it does not
evaluate the claimed denominator formula internally. I reran:

```text
python3 code/research_20260922/check_constant_data_messages.py
PASS: 180 exact support QPs, 252 centers, 504 active-neighborhood endpoints, 6252 approximation checks; n=1..6, theta=1/10,1/20
```

The reported counts match the loops. These finite checks support the exact
formula and sampled approximation inequalities. They do not prove the
continuous-domain bounds, the asymptotic quantifiers, the state-indicator
lift, or novelty; those points were reviewed separately above. No
project-wide verification, CI inspection, or Lean formalization was run.
