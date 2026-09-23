# Stage 5 independent review — reviewer 2

## Decision

**No major issues identified. One minor abstract correction is required.** The literature positioning is substantially qualified and distinguishes the closest antecedents by their actual mathematical objects. The numerical package is coherent with the manuscript's stated precision limits. After the abstract correction, this stage can proceed to the required whole-manuscript review.

Reviewed the complete abstract, introduction, numerical section, discussion, README, bibliography additions, reproduction scripts and documentation, relevant integrations in the geometry and LP-spectrum sections, and the Stage 5 author notes. I did not read other Stage 5 reports. I made no manuscript edits and did not rerun the numerical package in its source directory.

## MINOR 1 — the LP cluster count in the abstract needs the singleton exception

Location: `main.tex`, abstract sentence “For linear programs, every fixed barrier has two spectral scales.”

The theorem proves **at most two** scales. At a unique optimum, including a degenerate vertex, `f=0`, so the weak cluster is empty and every reduced-Hessian eigenvalue has the hard scale. The unconditional abstract wording conflicts with this prominent case and with the bounded-conditioning contribution described later.

Fix: write “For linear programs, every fixed barrier has at most two spectral scales,” or state explicitly that both scales occur when the optimal face has positive dimension. The compact-instance context already established in the abstract should remain clear.

## Independent source and originality audit

### Nesterov–Nemirovskii and the equal-gap contribution

I read the cached extraction of the local NN1994 primary text around Proposition 2.3.2(iii), equation (2.3.9). It defines the symmetric chord radius at a fixed point and bounds it above and below by multiples of the local Hessian radius. This does imply cross-barrier quadratic-form comparison at the same point. The introduction and updated geometric section acknowledge exactly that antecedent.

The manuscript's substantive distinction is comparison at generally different points selected by the same primal objective gap, mediated by a center-independent sublevel difference body. The residual-dependent containment and matching diameter characterization are then specified as the claimed additional package. The priority sentence is qualified and does not advertise cross-barrier comparison in general as unprecedented.

### Xiong–Freund, Peña and classical conditioning

The discussion agrees with the primary statements independently inspected in earlier rounds: Xiong–Freund Fact 5.2/Remark 5.1 connects primal–dual sublevel geometry with central-path ellipsoids; Peña Proposition 3.2 uses primal objective-gap parameterization, and Section 3.3 treats a Schur matrix under its stated conditions. The introduction makes these distinctions explicit and excludes novelty claims for gap parameterization and generic inverse-square bounds. Renegar and the implicit-barrier literature receive appropriate classical context without unchecked theorem-level claims.

The matching diameter law and equal-gap Loewner comparison remain precise theorem statements whose novelty is described cautiously. The wording does not purport to prove exhaustive absence of prior art.

### Duistermaat and oscillatory barriers

My live fetch of the institutional PDF returned 403, but the coordinating author supplied its previously retrieved original PDF at `/tmp/conditioning-duistermaat.pdf`. I independently extracted and read its Definition 2.1, Assumption 2.1 and Remark 2.3. The remark gives the perturbation `f + A sin f` and explains oscillation of derivatives rescaled by powers of boundary distance. Its definition permits an explicit differential self-concordance constant, which can be normalized by scaling; it also imposes a finite gradient ratio. This supports the manuscript's broad attribution to the self-concordant class.

The manuscript does not claim the first oscillatory barrier. It identifies the new example's role as the mixed-direction perturbation with a global parameter certificate, sharp projector rate and residual-versus-solution calculation. Those claims match the proved example. [Institutional record](https://dspace.library.uu.nl/handle/1874/2052).

### Bolte–Pauwels and nonconvergent paths

I independently opened the primary arXiv paper and checked its central-path statement, also available in the cached extraction. Corollary 11 uses a Legendre function finite and continuous on a closed square. It therefore does not meet this manuscript's barrier-divergence requirement. The added paragraph accurately states both the qualitative antecedent and this mathematical distinction. The introduction credits qualitative central-path nonconvergence rather than claiming it as new. [Primary preprint](https://arxiv.org/pdf/2001.07999).

### Sturm and spectral SDP antecedents

The introduction preserves the earlier stage's verified attribution of the nested quarter-power construction to Sturm and its presentation in Drusvyatskiy–Wolkowicz. It does not promote the basic fractional error geometry as a new example. It also distinguishes the reduced primal Hessian from Alizadeh–Haeberly–Overton's Schur matrix and the fixed affine central path from Sremac–Woerdeman–Wolkowicz's external regularization path. The stated contribution is the exact reduced-Hessian calculation, paired section and all-barrier transfer; it is narrower than a first spectral-degeneracy result.

The LP scaled-Hessian limit remains explicitly classical. These qualifications are consistent between introduction, detailed sections and discussion.

## Numerical package and integration checks

I inspected the certificate verifier, rational feasibility repair, factor-SVD Newton and spectral calculations, acceptance rules, synthetic CG construction, high-precision reference solver and manifest generation. No dependency on parent-repository imports or external data appears in ordinary reproduction. The optional preparation script is transparently described as capture from an already prepared cache, rather than a complete MPS presolver.

The exact input certificates check strict primal feasibility, bounded feasible sets or objective sublevels, and primal/dual optimal-value brackets using rational arithmetic. The manuscript correctly limits what these certify: its reported Hessian singular values and decrements remain numerical. The additional SVD resolution screen is explicitly presented as an indicator rather than a rigorous spectral interval bound.

The accepted Netlib counts and final gaps in the stored raw data agree with the manuscript: 14/27, 19/27 and 12/27, with final gaps about `3.34e-6`, `1.40e-8` and `0.680`. All attempted rows remain available, and the text makes no asymptotic slope claim from their truncated ranges.

I independently recomputed all SHA-256 entries in the supplied manifest. All 23 matched the current files. This establishes artifact consistency, not a separate execution of the numerical algorithms. The formulas and numerical contracts are also consistent with the earlier analytical reviews.

The CG test correctly forms and symmetrizes an actual float64 matrix, operates on that matrix, and uses a Decimal solve of its exact binary-rational values for the final true residual and energy error. Intermediate reference-spectrum diagnostics are labeled separately in the reproduction README. The text explains why iterations can exceed the dimension in floating arithmetic and why the recursive stopping residual does not certify the final true residual threshold.

The figures and tables are referenced in their relevant numerical subsections, and the discussion does not introduce unproved extensions. The anonymous author field is deliberate and disclosed in the README; supplying author identities is an administrative submission step rather than missing scientific content.

## Remaining process

Correct the abstract's cluster count, then perform the prescribed whole-manuscript review. No additional Stage 5 major-issue cycle is required on the basis of this report.
