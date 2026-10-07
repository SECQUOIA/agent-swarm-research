# Manuscript brief and shared conventions

User request: produce a complete, clear, anonymous journal manuscript on quadratic hulls on boxes, incorporating the September 25 and October 1 developments coherently. Critically reconstruct proofs, repair errors, develop necessary incomplete arguments, preserve archived computations without rerunning experiments, and qualify novelty through a careful literature review. All literature research uses GPT Luna with max reasoning. One reusable Luna agent owns literature additions through /workspace/local-home/repo/skills/literature/SKILL.md.

Working title: Quadratic hulls on boxes: valid inequalities and semidefinite representability.

## Ownership

Root owns main.tex, macros.tex, introduction, setting, archived computational evidence, discussion, integration, documentation, final builds and packaging.
Family writer owns sections/03-counterexample.tex, sections/04-family.tex, appendices/A-family.tex, and evidence/family-audit.md.
Three-variable writer owns sections/05-three-variables.tex, appendices/B-three-variables.tex, and evidence/three-variable-audit.md.
Representability writer owns sections/06-representability.tex, sections/07-graphs.tex, appendices/C-representability.tex, and evidence/representability-audit.md.
Development agent owns only evidence/development.md, and may supply mathematical findings to root and writers.
Luna literature agent owns evidence/literature-audit.md, references.bib, and serialized literature/ KB changes. Never have two lit sessions on this repository.

## Mathematical conventions

C_n=[0,1]^n. Quadratic q(x)=q_0+sum_i a_i x_i+sum_i b_i x_i^2+sum_{i<j} c_{ij}x_ix_j. Thus cross coefficients are full polynomial coefficients, not half-matrix entries.
mathcal P_n is the cone of quadratics nonnegative on C_n. mathcal P_n^+ imposes b_i>=0. mathcal Q_n=conv{(x,xx^T):x in C_n}; mathcal H_n=mathcal Q_n+{(0,Diag(s)):s>=0}. Pairing is evaluation L_{m,Y}(q)=q_0+sum a_i m_i+sum b_iY_ii+sum c_ijY_ij; use a homogenized cone when taking duals, and state that normalization matters.
For n=3, V is the 20-dimensional span with exponent vectors in {0,1,2}^3 and at most one exponent 2; W is the quadratic subspace. w_{A,B}=prod_{i in A}x_i prod_{j in B}(1-x_j), A and B disjoint. K_D is the cone of sums w_{A,B} L^2 with L affine in coordinates outside A union B. D_3=K_D intersect W. R_D projects normalized functionals nonnegative on K_D into (m,Y); closures and duality must be proved, not assumed. Caps are x_i(1-x_i)>=0 / Y_ii<=m_i.
The new family q_{h,d,k}=(h-d_1x-d_2y+d_3z)^2+2d_3kz(1-x-y)+k(2(d_1+d_2-h)+k)xy, h real, d_i,k>=0. Exposed subclass h,d_i,k>0, h<min(d_1,d_2), d_1+d_2-h+k<d_3.
Graphs G carry V,E,L_+,L_-. Only diagonal slacks for recorded loops. All minor operations in representability claims are on the positive-induced graph; retained moment coordinates must be specified.

## TeX interface

Use ordinary theorem/proposition/lemma/corollary/definition/example/remark environments; theorem numbering within sections. Labels prefixed family:, three:, repr:, graph: respectively. Root labels set: and intro:. Shared macros in macros.tex: R,Q,Sbb,Sn,conv,cone,cl,COP,CP,DNN,PSD,tr,diag,rank,inner{a}{b},norm{a},abs{a}. Standard amsmath, amssymb, amsthm, mathtools, bm, enumitem, booktabs, longtable, graphicx, xcolor, natbib, hyperref, cleveref. Do not redefine shared macros locally. Use citep/citet with citation keys proposed to Luna; unknown keys may be supplied as clear standard surnameYear keys for root mapping.

## Standards

No repository paths, Markdown proof dependencies, agent/review history, unfinished placeholders, or historical section identifiers in submission prose. Every claimed new theorem must have a complete proof in manuscript or its appendices; external classical theorem inputs must be precisely stated and cited. Do not copy errors merely because reviewed before. Do not run old experiments, optimization samplers, timing campaigns, or project-wide checks. Focused algebraic reasoning and new symbolic checks are allowed when needed; distinguish them from archived evidence. No novelty searching by mathematical agents: ask Luna for source contracts. Any unproved completeness or series-parallel classification must remain an explicit open question unless actually resolved; a conjecture cannot support a theorem.

The paper should explain importance without claiming a general solver improvement. It must distinguish moment hulls from objective-specific epigraphs, exact lifts from separation algorithms, compact family enforcement from complete hull descriptions, and numerically sampled evidence from proof. Be thorough but remove research-log repetition and LLM stock language.
