# Prior-art audit: nonlocal double-parabola interface inference

Date: 2026-09-07. Bounded independent audit, coordinated with ensemble_scout. This is a novelty assessment, not a substitute for the independent variational proof review.

## Assessment

The exact continuous-field elimination has close prior art in phase-field dislocation theory. Double-parabola interface models and nonlocal interfacial Hamiltonians are also established in liquid-state theory. I did not locate the full proposed theorem for an arbitrary positive integrable interaction kernel, its sharp fixed-moment surface-tension ambiguity, or its finite-band inference certificate in the primary sources inspected. These remain provisional candidates.

The strongest positioning is a **quantitative limit and certificate for inferring interfacial free energy from homogeneous harmonic response in a specified nonlocal model**. The exact solution is supporting machinery. Neither the general claim that bulk information can miss interfacial properties nor the double-parabola solution method should be presented as a new discovery.

## Candidate and model restrictions

The candidate concerns

\[
F[\phi]=\frac a2\int(|\phi|-1)^2\,dx+
\frac14\iint J(x-y)(\phi(x)-\phi(y))^2\,dx\,dy,
\]

with positive even integrable \(J\), and projected symbol \(D(k)=J_0-\widehat J(kn)\). Its proposed planar minimum is

\[
\sigma=\frac{2a}{\pi}\int_0^\infty
\frac{D(k)}{a+D(k)}\,\frac{dk}{k^2}.
\]

The harmonic response within a homogeneous well is \(\chi(k)=(a+D(k))^{-1}\). This is a Hessian response of the specified free-energy functional. Equating it to an exact finite-temperature microscopic structure factor requires additional justification. Compactly supported kernels have analytic Fourier transforms: exact data on an open continuum band identify the symbol by analytic continuation. Consequently, finite-band uncertainty statements must concern a certified reconstruction or finite precision, not exact continuum-band nonuniqueness.

## Close mathematical prior: exact elimination in a nonlocal multiwell model

M. Koslowski, A. M. Cuitiño and M. Ortiz, *A phase-field theory of dislocation dynamics, strain hardening and hysteresis in ductile single crystals*, Journal of the Mechanics and Physics of Solids **50**, 2597–2635 (2002), DOI 10.1016/S0022-5096(02)00037-6. The preprint title begins *An Exactly Solvable Phase-Field Theory*. [Open primary manuscript](https://arxiv.org/abs/cond-mat/0109447).

The authors write a piecewise-quadratic potential as minimization over an integer-valued field, then interchange minimizations. Equations (38)–(42) eliminate continuous slip by Fourier transformation. They obtain a rational effective multiplier \(K/(1+Kd/2)\) and a smoothing multiplier \(1/(1+Kd/2)\). Equations (45)–(47) explicitly interpret the latter as a convolution kernel; equation (48) inserts a half-plane step for a straight dislocation.

This is the same algebraic mechanism as the candidate's binary-field elimination and resolvent. Their elastic symbol is anisotropic and homogeneous of order one, rather than the bounded symbol of a positive finite-range kernel; their field has all integer wells. I did not find the candidate's positive-kernel global planar minimization or bulk-response inference statement there. Nevertheless, claims to a new general elimination technique would be inaccurate.

The full primary preprint was retrieved and the relevant derivation read; local source prefix: research/sources/koslowski-etal-2002-phasefield.

## Liquid-state double-parabola theory: distinguish two kinds of nonlocality

A. O. Parry, C. Rascón, N. R. Bernardino and J. M. Romero-Enrique, *Derivation of a non-local interfacial Hamiltonian for short-ranged wetting: I. Double-parabola approximation*, Journal of Physics: Condensed Matter **18**, 6433 (2006), DOI 10.1088/0953-8984/18/28/001. [Primary journal identifier](https://doi.org/10.1088/0953-8984/18/28/001).

This starts from a **local square-gradient** Landau–Ginzburg–Wilson functional with a double-parabola local potential. The resulting interface-height Hamiltonian is nonlocal after the bulk field is eliminated. Its planar tension is the familiar square-gradient result. This is related machinery, but not an identified theorem for arbitrary nonlocal bulk kernel \(J\). The primary manuscript's displayed model and derivation were inspected through openly indexed text.

J. M. Romero-Enrique, A. Squarcini, A. O. Parry and P. M. Goldbart, *Curvature corrections to the nonlocal interfacial model for short-ranged forces*, Physical Review E **97**, 062804 (2018). [Open primary preprint](https://arxiv.org/abs/1804.04554).

This revisits the same square-gradient starting point through a boundary-integral construction and derives curvature corrections and interfacial self-interactions. Its title alone should not be treated as proof that it studies the candidate's nonlocal bulk energy.

The Sullivan model is a closer bulk-nonlocal precedent because it treats attractive Yukawa interactions. A. O. Parry and C. Rascón, *The Goldstone mode and resonances in the fluid interfacial region*, Nature Physics **15**, 287–292 (2019), DOI 10.1038/s41567-018-0361-z, discusses exactly integrable interface models and Sullivan-like theories. [Open author manuscript](https://valbuena.fis.ucm.es/gisc/papers/NP.2018.pdf).

This literature already links bulk correlations to interfacial correlation functions and surface-tension-like coefficients. It does not establish, from the sections inspected, the arbitrary-kernel formula or inference bounds at issue. The older simplified Sullivan models of Iwamatsu are an unresolved follow-up: indexed primary text indicates a double-parabola approximation in a transformed chemical-potential variable. That is not automatically the same local potential in \(\phi\). I did not retrieve enough of the original 1995 work to exclude an exact special-case overlap.

## A useful exact connection to known bulk-slab response

F. Höfling and S. Dietrich, *Finite-size corrections for the static structure factor of a liquid slab with open boundaries*, Journal of Chemical Physics **153**, 054119 (2020). [Open primary preprint](https://arxiv.org/abs/2006.06083).

F. Höfling and S. Dietrich, *Structure of liquid–vapor interfaces: Perspectives from liquid state theory, large-scale simulations, and potential grazing-incidence x-ray diffraction*, Journal of Chemical Physics **160**, 104107 (2024), DOI 10.1063/5.0186955. [Open institutional primary PDF](https://refubium.fu-berlin.de/bitstream/handle/fub188/43186/104107_1_5.0186955.pdf?isAllowed=y&sequence=1).

Equations (12)–(14) of the 2024 paper express the structure factor of a virtually cut slab using the bulk structure factor. The leading finite-slab correction is

\[
\mathcal J_0(q)=\frac1\pi\int_0^\infty
\frac{S_b(\sqrt{q^2+k^2})-S_b(q)}{k^2}\,dk.
\]

This is a known spectral functional with the same weighting as the candidate. Substituting the model harmonic response for \(S_b\), an inference made here gives

\[
\boxed{\sigma=-2a^2\mathcal J_0(0).}
\]

Equivalently, define the response of a virtual interval inside the infinite homogeneous model by

\[
\chi_L=\frac1L\langle {\bf1}_{[0,L]},(a+D)^{-1}{\bf1}_{[0,L]}\rangle.
\]

Then the proposed exact tension formula implies

\[
\sigma=a^2\lim_{L\to\infty}L\,[\chi(0)-\chi_L].
\]

This follows either from the known slab expansion \(\chi_L=\chi(0)+2\mathcal J_0(0)/L+o(L^{-1})\), or directly from convolution with the triangular window. It provides a possible real-space interpretation of the candidate's inference result. The **slab correction itself is prior work**; identifying it with the surface tension is special to this double-parabola model and must not be generalized to arbitrary fluids.

The root agent subsequently derived a finite-window certificate, undergoing independent review. Write \(G=a(a+D)^{-1}\) as the probability law of a geometric sum of steps drawn from \(J/J_0\), with continuation probability \(p=J_0/(a+J_0)\). If projected step lengths are at most \(R\), then

\[
\sigma_L=a^2L(1/a-\chi_L)
=a\,\mathbb E_G\min(|Z|,L)\uparrow\sigma,
\qquad
0\le\sigma-\sigma_{mR}\le J_0R\,p^m.
\]

The triangular-window identity and geometric resolvent expansion are standard ingredients. I did not identify this surface-tension certificate in the inspected slab-response papers. Its potential contribution is an explicitly controlled finite-window inference of the model tension, rather than a new general relation between subvolume fluctuations and bulk correlations. The error bound uses a known interaction range; it is not a model-free estimator.

The 2024 primary PDF and relevant sections were read; local source prefix: research/sources/hofling-dietrich-2024-interface.

## Kac limits and moment ambiguity

G. Alberti, G. Bellettini, M. Cassandro and E. Presutti, *Surface tension in Ising systems with Kac potentials*, Journal of Statistical Physics **82**, 743–796 (1996), DOI 10.1007/BF02179792. [Open primary author manuscript](https://pagine.dm.unipi.it/alberti/ricerca/1992-96/abcp-rdc.pdf).

This establishes the relation between microscopic Kac systems and a nonlocal variational surface tension. It is important prior context and does not use the candidate's exact double-parabola local free energy.

Fixing only finitely many kernel moments leaves substantial kernel freedom. The sharp first-moment bounds under second- and fourth-moment constraints belong to the classical moment problem. I did not identify an earlier result transferring exactly those bounds into separated finite-\(a\) surface tensions while keeping the homogeneous gradient expansion through \(k^4\) fixed. That transfer, together with explicit kernels and error control, is a better candidate than the generic observation that a gradient expansion loses information.

Likewise, the tail certificate follows from the elementary bound \(0\le D(k)\le2J_0\):

\[
0\le\sigma-\sigma_{[0,K]}
\le\frac{4aJ_0}{\pi(a+2J_0)K}.
\]

I found no exact prior occurrence in the inspected sources, but it is a short corollary of the spectral formula. Its value depends on whether realistic response data and model uncertainty can support a useful certified interval.

## Recommendation and unresolved checks

Retain the candidate, credit the elimination method, and emphasize a concrete quantitative inference theorem. Check the simplified Sullivan/Yukawa special case before making priority claims for the exact tension. An application should clearly distinguish harmonic response, microscopic scattering, and uncertainty in the local potential away from its minima. No claim of exhaustive novelty or likely high citation impact is supported by this bounded audit.
