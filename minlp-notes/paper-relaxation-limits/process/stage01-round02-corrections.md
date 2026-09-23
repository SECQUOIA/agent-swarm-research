# Stage 1, round 2: corrections

Accepted finding R13-1 (MINOR) is addressed in `sections/01-foundations.tex`, immediately before Lemma `lem:cut-row`. The two-line setup

```tex
Let $A$ be the symmetric weighted adjacency matrix on $W$, with zero
diagonal. For a rectangular matrix define
```

was replaced with

```tex
Let $A$ be the symmetric weighted adjacency matrix on $W$, with zero
diagonal and zero entries at nonedges. Write $a_{i,T}=(A_{ij})_{j\in T}$
for $T\subseteq W$ and $a_i=a_{i,W}$. For a rectangular matrix define
```

This defines the restricted and full adjacency rows before their first use and makes zero entries at nonedges explicit. No mathematical statement or proof was changed. Frozen snapshot files were not modified.

Verification: `python paper-relaxation-limits/verification/build_and_check.py` exited with status 0. The manuscript compiled to 12 pages with no warnings and no duplicate labels. The script refreshed the live build output, report, and extracted manuscript text. Root's final inspection and Stage 1 gate decision remain pending.
