# Root assessment: stage 3, round 1

Read all five full independent reports. Accept one major finding and one minor
finding. Reviewers 1 and 4 independently found the major source failure;
reviewers 2, 3, and 5 accepted the printed source statement without detecting
its false general Boolean normal-form step. The explicit counterexample and
root's own proof audit take precedence over the number of passing reports.

## Accepted major M1

The claim of rational equivalence for every compact semialgebraic set is false.
Dynamic Toolbox Lemma A leaves inactive branch slack variables undetermined;
its printed broad theorem cannot support this manuscript claim. Moreover,
compact rational equivalence to a basic closed set preserves basic closedness,
whereas the compact three-quadrant set is not locally basic closed. Root read
the source proof and checked both the counterexample and the denominator
argument. This is a mathematical correction, not merely a missing citation.

Required correction: prove rational universality for compact basic closed sets
using a verified conjunction-only arithmetic construction; retain general
compact semialgebraic topology through finite triangulation and the rational
basic closed realization of a finite simplicial complex. Prove the sharp
basic-closed boundary and explain why the two types of universality differ.
Repair the singleton/coordinate proof's dependency while retaining its valid
conclusion. Update every affected summary, README, bibliography, and coverage
entry. Supply sufficient details of the surviving arithmetic gates to avoid
importing additional source typos or unsupported range estimates.

Working repair arguments and verified triangulation source are recorded in
root-universality-repair.md. These are guidance for the correction agent to
verify independently, not a substitute for the next review round.

## Accepted minor m1

The reverse residual proof misdescribes D as having two weighted x copies.
D has one complemented x neighbor of conductance 2 and one complemented y
neighbor of conductance 1, in addition to W. The bound epsilon+3delta is correct.
Correct the wording without changing its constants.

## Remaining findings and process

The structural construction, residual transfer, tiny infeasible family,
separation bound, promise certificates, and reactive stability pass all five
reviews and root's independent audit. The abstract-prioritization suggestion
from reviewer 5 belongs to the already planned integration stage and is not
a defect in a current theorem. Finite checks and a clean build do not certify
the false universality claim.

Assign a different agent to correct all accepted findings. Because M1 is major,
a fresh frozen version must receive five independent reviews before stage 3
can close. No later writing stage may begin yet.
