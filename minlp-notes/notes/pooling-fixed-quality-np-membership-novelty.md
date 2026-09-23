# Prior-literature audit: NP membership with fixed pool-quality dimension

Date: 2026-09-05. Status: bounded novelty audit, not a proof audit. The proposed upper bound fixes the number of pool-quality variables, permits arbitrary bypasses and shared source capacities, and uses an active flow basis as a certificate. It is intended to accompany [the one-pool copy-gadget hardness candidate](pooling-one-pool-bypass-copy-hardness.md).

No explicit NP-membership theorem for this exact pooling class was found in the inspected literature. The proposed certificate method is a natural combination of standard linear algebra, polyhedral structure, and fixed-dimensional real-algebraic decision algorithms. It should be presented as a proved supporting upper bound, without claiming a major new general certificate technique or established first priority.

## The proposed statement and why existing shorthand is insufficient

The candidate general setting has a constant-dimensional parameter vector `q`, polynomially represented coefficient functions, and a polyhedral flow fiber

```
P(q) = {x : A(q)x <= b(q)}.
```

The threshold question adds a linear-in-`x` objective inequality. For pooling, `q` consists of the fixed number of pool-quality variables; flow variables and bypass arcs can grow. Compact feasible flow fibers are assumed in the candidate.

The intended certificate guesses indices of an active flow basis. Symbolic Cramer expressions then reduce its feasibility, determinant nonvanishing, quality-domain conditions, and objective threshold to polynomial conditions in the constant number of parameters. The verifier decides whether such parameters exist. This is the author's candidate method; its determinant sizes, degree bounds, sign handling, and treatment of degenerate fibers require the separate proof review.

The certificate need not be a rational physical pooling solution. NP permits a finite combinatorial certificate checked by a polynomial-time algorithm that itself decides a real-algebraic subproblem. Thus the absence of an immediately apparent rational optimizer does not invalidate this approach. Conversely, finite-dimensional parameters alone do not permit enumerating all bases in polynomial time; guessing and verifying a basis is a different claim.

## Closest primary sources inspected

### Quadratic programming in NP

[Vavasis, *Quadratic programming is in NP*](https://doi.org/10.1016/0020-0190(90)90100-C), *Information Processing Letters* 36(2), 73–77 (1990), establishes the classical upper bound for a quadratic objective over linear constraints. The publisher abstract was inspected; a full open copy was not retrieved in this bounded audit.

An open primary treatment is [Del Pia, Dey, and Molinaro, *Mixed-integer Quadratic Programming is in NP*](https://arxiv.org/pdf/1407.4798). Section 2.2, Theorem 3, PDF p.3, states the continuous QP result and a polynomial-size rational linear-system description of an optimizer when one exists. Its formulation has linear constraints and one quadratic threshold inequality. It does not supply a general NP upper bound for systems of many bilinear constraints, so it cannot directly establish pooling membership.

In particular, linear multiplicative optimization over a rational polytope is covered by the quadratic-objective framework. This is relevant to the Matsui source problem, but a reduction **from** that problem to pooling only supplies a hardness direction. NP membership of the source does not transfer to every target instance.

### Separable bilinear programs

[Petrik and Zilberstein, *Robust Approximate Bilinear Programming for Value Function Approximation*](https://jmlr.csail.mit.edu/papers/volume12/petrik11a/petrik11a.pdf), *JMLR* 12, 3027–3063 (2011), Section 4, Definition 16, PDF p.11, explicitly restricts the paper's bilinear programs to independent linear constraints on the two variable groups and a bilinear objective. Section 5, PDF p.17, explains NP membership using basic feasible solutions. The authors' shorthand about bilinear programs must be read with that definition. Pooling's quality equations and output specifications are bilinear constraints and do not satisfy it automatically.

### Real-algebraic decision as a verifier primitive

[Vorobjov, *Lecture notes on complexity of quantifier elimination over the reals*](https://arxiv.org/pdf/2112.00456), Sections 2.1 and 5.12, PDF pp.3 and 18, develops a Renegar-style consistency algorithm with bit complexity `(s d)^{O(n)} M^{O(1)}`, where `s` is the polynomial count, `d` the degree bound, `n` the real dimension, and `M` the coefficient bit bound. Fixed dimension gives the needed polynomial-time decision primitive, provided the polynomial data produced by the certificate are polynomially sized. The notes are an open technical exposition of established machinery; this machinery is not a novel ingredient of the pooling claim.

The original foundational reference is Renegar, *On the computational complexity and geometry of the first-order theory of the reals*, Part I, DOI 10.1016/S0747-7171(10)80003-3. Bibliographic information was located, but the detailed complexity comparison here uses the inspected open Vorobjov text.

### Pooling complexity sources

Haugland's final paper proves the single-pool/fixed-quality polynomial case in a model without direct arcs. Its degree-one subdivision of bypasses changes the pool count. [[haugland2016-the-computational-complexity-of-the]] p.4, p.7

Baltean-Lugojan–Misener discusses a one-pool/one-quality bypass model with restricted capacities and asserts hardness beyond its restrictions; the inspected Remark 4.6 does not provide the present active-basis NP certificate. [[lugojan2018-piecewise-parametric-structure-in-the]] p.24

The more consequential priority caveat remains the prior hardness assertion, documented in [the bypass novelty audit](pooling-single-quality-bypass-novelty.md). Adding an NP upper bound may sharpen a rigorously proved hardness result to NP-completeness, but does not erase that earlier claim.

## Recommended positioning

If independent review accepts both arguments, state the general fixed-pool-quality NP upper bound as a supporting lemma and the precise one-pool bypass NP-completeness classification as its corollary with the new reduction. Retain the assumptions on lower/upper flow bounds, fixed supply contracts, fixed demands, and quality counting. One physical quality with upper and lower specifications corresponds to two coordinates in Haugland's upper-only convention.

Use wording such as:

> NP membership follows from a basis certificate for the flow LP and fixed-dimensional real-algebraic decision. Combined with the explicit reduction, this yields NP-completeness for the stated one-pool class.

Avoid saying that all bilinear feasibility problems are in NP, that an optimizer can always be given by polynomially many rational flow values, or that a fixed number of nonlinear parameters alone yields a deterministic polynomial algorithm. None is the proposed lemma.

## Search scope

Searches combined `pooling problem`, `fixed qualities`, `fixed pools`, `in NP`, `NP-complete`, `certificate`, `parametric linear programming`, `Cramer`, `fixed parameters`, `bilinear feasibility`, and `fixed nonlinear variables`. The main pooling complexity sources and the neighboring QP/bilinear upper bounds were inspected. No exact predecessor of the proposed parameterized-LP certificate statement was identified. This does not establish that the general observation is unpublished or unknown; its construction is sufficiently standard that a standalone novelty claim would need a much broader complexity-literature audit.
