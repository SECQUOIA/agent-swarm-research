# Current source boundary for submodular continuous box QP

Date: 2026-10-02. Status: direct primary-source check; no new theorem.

The general continuous submodular box-QP problem must not be used as a
known polynomial-time recourse oracle in this continuation. The original
2025 abstract of arXiv:2504.03996 claimed general semidefinite
representability. Its current version changes that conclusion.

[Burer, Natarajan, and Willemsen, version 3](https://arxiv.org/html/2504.03996v3)
proves tightness of the stated SDP relaxation only in dimension at most
three, gives an explicit four-variable gap, and states that the complexity
of general continuous quadratic submodular minimization on a box remains
open. Its discussion identifies additional tractable cases, including
nonpositive diagonal coefficients and nonpositive linear coefficients.
These extra hypotheses cannot be silently removed.

In particular, changing signs of variables to make all off-diagonal
Hessian entries nonpositive does not, by itself, provide a currently
established general polynomial-time oracle. Forest-structured box QPs do
have the separate [Del Pia–Khajavirad dynamic-programming
algorithm](https://arxiv.org/html/2609.35595v1#S2). Their forest theorem
must be credited to its actual message argument, rather than deduced
from the superseded all-dimensional SDP claim.

The source check used the current version's abstract, introduction,
complexity table, and stated dimension-four counterexample. This is a
version-sensitive literature correction, not an independent verification
of every theorem in either paper. No code, project-wide checks, or CI
inspection were needed.
