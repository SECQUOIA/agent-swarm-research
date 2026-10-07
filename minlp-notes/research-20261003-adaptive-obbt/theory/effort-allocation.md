# What a budget for solver enhancements can guarantee

Bounds on the cost of tightening do not establish a bound on total solving
time relative to an unmodified solver. This note separates the two statements
and gives elementary guarantees that remain valid when an enhancement changes
the search. The accounting and independent-solver scheduling arguments are
classical; no novelty is claimed for them.

## Cost on the actual enhanced run

Consider one execution. Let N be time spent on the native part of this
execution and E time charged to optional enhancements. Charge model discovery,
screening, support solves, validation, and callback bookkeeping to E; otherwise
the following bound omits real work. A ledger admits an enhancement only while

\[
 E < b+\eta N,\qquad b\ge0,\quad\eta\ge0.
\]

Assume every increment of E belongs to an admitted operation or is charged
through an enforced reservation before admission. In particular, rejected
callback entries and admission checks are not free: either their cost is
included in those operations or it is accounted for separately below.
Suppose every admitted operation is interrupted after at most delta time
units, or its cost is known in advance and reserved. In the interruptible case,

\[
 E\le b+\eta N+\delta,\qquad
 N+E\le(1+\eta)N+b+\delta.                 \tag{1}
\]

To prove this, immediately before the last admitted operation the ledger
satisfies its admission condition. That operation adds at most delta to E;
subsequent native work can only increase the right hand side. If no operation
was admitted the inequality is immediate. Reservation removes delta when
admission requires `E + reserved_cost <= b + eta N` and an enforced upper
bound on every reserved cost is respected. Per-call limits on
an LP solver do not automatically bound symbolic setup or callback work.
If admission and rejected-entry costs cannot be reserved, let J be their
total measured cost. Then (1) applies to E excluding J, while total execution
cost has the additional term J. Without a bound on J there is no total
enhancement-overhead guarantee.

Here N is native work on the **enhanced trajectory**. It is not the native
solver's work N0 on an independent baseline trajectory.

### A counterexample to a baseline runtime conclusion

Consider a deterministic search procedure with two legal branching choices at
its first decision. On an instance indexed by M, the default ordering selects
a branch with a complete proof after one work unit. A redundant row changes
the ordering, and the enhanced execution needs M work units before producing
the same valid proof. Generating the row costs a fixed b>0. Both executions
are correct, and the enhancement obeys E=b, but the total time ratio is M+b.

This is a counterexample in an abstract search model; it is not a constructed
SCIP or QCQP instance and does not predict their runtime. Its purpose is
logical: a cost ledger alone contains no assumption connecting N and N0, so
no baseline-competitive theorem follows from (1).

Likewise, a certified bound on remaining width reduction is not a bound on
remaining search time. Width reduction can leave the important relaxation
error unchanged, while a small reduction can trigger a discrete inference.
Such a certificate justifies a claim about the specified tightening operator.

## An independent baseline gives a different guarantee

Let A be an unchanged baseline solver and H an enhanced solver. They have
separate states, fixed random tapes, and the same original input. In an ideal
preemptible work model, assume the scheduler gives A at least
(1-eta)t-h units of work and H at least eta*t-h by aggregate work time t,
with 0<eta<1 and scheduling lag h>=0. If their stand-alone work requirements
are TA and TH, the first complete answer arrives by

\[
 \min\left\{\frac{T_A+h}{1-\eta},
             \frac{T_H+h}{\eta}\right\}.                \tag{2}
\]

Indeed, by either displayed time the respective solver has received the work
needed to finish. Equal shares with zero lag give at most twice the work of
the faster solver. The premises exclude shared memory exhaustion, cache
interference, wall-clock-dependent search decisions, and uncharged process
startup. Equation (2) is therefore a scheduling result, not a wall-clock
promise for two processes on a shared workstation. This continuation does
not deploy a competing solver portfolio or claim (2) for its experiments.

A simpler exact statement uses serial rescue. Run H for at most b charged
work units. If it does not finish, discard it and run A with its original
state and random tape. If startup is charged, the resulting work is at most
b+TA. Injecting an incumbent or rows from H can change A's search, so that
variant needs a new assumption to retain this particular bound.

## Limits of choosing an enhancement from past rewards

Suppose two enhancement calls cost one work unit each. At a decision point,
the observable histories are identical in two possible future environments.
In the first, only call 1 reveals a complete proof; in the second, only call 2
does. Every deterministic selector chooses the same first call in both
environments and is wrong in one. A randomized first choice has success
probability at most one half in at least one environment.

This elementary observation rules out a guaranteed correct first choice from
history alone. It does not rule out statistical learning with assumptions,
competitive portfolios, or structural tests that distinguish the environments.
For solver components the feedback also changes the future search state;
ordinary stationary bandit assumptions cannot be silently imported.

## A justified interface for multiple actions

The following contract can be shared by OBBT, support cuts, or a decomposition
bound without claiming a universal selection theorem:

1. The action declares its node domain, model identity, cutoff, supported
   relaxation, and a work limit. Every returned inference retains those
   validity premises.
2. The action returns a verified inference, a verified ceiling on benefit in
   a specified measure, or `unresolved`. Exhausting a budget is not evidence
   that no useful inference exists.
3. The ledger charges discovery and verification as well as the optimization
   call. A noninterruptible operation records its overrun.
4. The selector may rank unresolved actions using heuristics, but never turns
   that ranking into a validity claim. Native search remains available.
5. Performance is evaluated with independent full runs, including time spent
   selecting actions and preserving all failures and no-incumbent cases.

An OBBT width ceiling, a joint-cut separation distance, and a decomposition
lower bound are different quantities. They cannot be compared as expected
seconds saved without a separately validated model. The present study first
tests the OBBT instance of this interface. A larger controller has no
performance justification merely because its interface can be written down.

## Verification and attribution

`check_effort_allocation.py` verifies the ledger bound and rescue/interleaving
accounting on exact finite traces, including rejected actions and overruns.
These checks supplement the elementary proofs and do not simulate a MINLP
search or establish empirical performance. The related-work ledger covers
adaptive algorithm selection and scheduling in MIP. The limits above concern
the stated information and cost models, not an impossibility theorem for all
adaptive MINLP methods.
