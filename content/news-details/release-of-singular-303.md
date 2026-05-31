---
title: "Release of SINGULAR 3-0-3"
url: "/index.php/news/release-of-singular-303.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/news/release-of-singular-303.html"
migration_status: "migrated from local legacy copy"
---

<p>Release of <strong>Singular</strong> version 3.0.3:  available for most Unix platforms, Windows and Mac OS X:</p>
<h2></h2>
<h3>Updates for version 3.0.3</h3>
<!--docid::SEC1452::-->
<p>The current version 3.0.3 is stabilyzing release, a result of a long beta test and the integration of a lot of small fixes which were on our waiting list for integration.</p>
<p>It contains also  a lot of new features:</p>
<ul>
<li> licence changed: omalloc and MP are now (also) available under GPL; that means that all parts of S<small>INGULAR</small> are licenced under GPL (resp. LGPL). </li>
<li> factory, libfac, Singular updated for gcc 4.1.x </li>
<li> kernel updated for the optional use of boost. </li>
<li> can now be built as a library. </li>
<li> new operator <code>a:b</code> gives an <code>intvec</code> of length <code>b</code> with constant entries <code>a</code> </li>
<li> new command: ( <a href="/old/Manual/3-0-3/sing_172.htm">chinrem</a>): lifting via chinese remainder theorem </li>
<li> new command: ( <a href="/old/Manual/3-0-3/sing_219.htm">interpolation</a>): ideal of points with given multiplicities </li>
<li> non-commutative kernel subsystem was rewritten in order to support specific algebras more efficiently. Implemented algebras at the moment: super-commutative algebras (in particular exterior algebras). </li>
<li> <a href="/old/Manual/3-0-3/sing_291.htm">std</a> et al.: new selection strategy for reductions ( <a href="/old/Manual/3-0-3/sing_258.htm">option</a> (length)). </li>
<li> <a href="/old/Manual/3-0-3/sing_274.htm">reduce</a>: new strategy for selection and normalization. </li>
<li> <a href="/old/Manual/3-0-3/sing_284.htm">simplify</a> slightly changed: does not omit zero polynomial unless specified. </li>
<li> new library: compregb.lib ( <a href="/old/Manual/3-0-3/sing_614.htm">compregb_lib</a>): comprehensive Groebner base system </li>
<li> new library: kskernel.lib ( <a href="/old/Manual/3-0-3/sing_1024.htm">kskernel_lib</a>): kernel of the kodaira-spencer map for irreducible plane curve singularities </li>
<li> new library: modstd.lib ( <a href="/old/Manual/3-0-3/sing_814.htm">modstd_lib</a>): Groebner base computations over the rational numbers via modular computations </li>
<li> new library: noether.lib ( <a href="/old/Manual/3-0-3/sing_847.htm">noether_lib</a>): Noether normalization of an ideal(not nessecary homogeneous) </li>
<li> new library: atkins.lib ( <a href="/old/Manual/3-0-3/sing_1274.htm">atkins_lib</a>): the elliptic curve primality test of Atkin </li>
<li> new library: aksaka.lib ( <a href="/old/Manual/3-0-3/sing_1265.htm">aksaka_lib</a>): primality testing after Agrawal, Saxena, Kayal </li>
<li> new library: arcpoint.lib ( <a href="/old/Manual/3-0-3/sing_942.htm">arcpoint_lib</a>): truncations of arcs at a singular point </li>
<li> new library: resgraph.lib ( <a href="/old/Manual/3-0-3/sing_1218.htm">resgraph_lib</a>): visualization of resolution data. </li>
<li> new library: realrad.lib ( <a href="/old/Manual/3-0-3/sing_883.htm">realrad_lib</a>): computation of the real radical over the rational numbers and extensions thereof </li>
<li> new library: hyperel.lib ( <a href="/old/Manual/3-0-3/sing_1324.htm">hyperel_lib</a>): divisors in the jacobian of hyperelliptic curves </li>
<li> new library: curvepar.lib ( <a href="/old/Manual/3-0-3/sing_962.htm">curvepar_lib</a>): space curves </li>
<li> new library: sagbi.lib ( <a href="/old/Manual/3-0-3/sing_911.htm">sagbi_lib</a>): subalgebras bases analogous to Groebner bases for ideals </li>
<li> new library: surfex.lib ( <a href="/old/Manual/3-0-3/sing_1224.htm">surfex_lib</a>): visualizing and rotating surfaces </li>
<li> new library: cimonom.lib ( <a href="/old/Manual/3-0-3/sing_771.htm">cimonom_lib</a>): determines if the toric ideal of an affine monomial curve is a complete intersection. </li>
<li> <a href="/old/Manual/3-0-3/sing_917.htm">sheafcoh_lib</a>: new experimental functions, in particular  <a href="/old/Manual/3-0-3/sing_921.htm">sheafCohBGG2</a> </li>
<li> library <code>ncall.lib</code> merged into  <a href="/old/Manual/3-0-3/sing_613.htm">all_lib</a> </li>
<li> library center.lib (<code>center_lib</code>) renamed to <code>central.lib</code> ( <a href="/old/Manual/3-0-3/sing_419.htm">central_lib</a>) </li>
<li> <a href="/old/Manual/3-0-3/sing_505.htm">nctools_lib</a>: new functions for super-commutative algebras (i.e.  <a href="/old/Manual/3-0-3/sing_514.htm">SuperCommutative</a>,  <a href="/old/Manual/3-0-3/sing_522.htm">IsSCA</a>,  <a href="/old/Manual/3-0-3/sing_520.htm">AltVarStart</a>,  <a href="/old/Manual/3-0-3/sing_521.htm">AltVarEnd</a>) </li>
<li> resolve.lib: blow ups revised ( <a href="/old/Manual/3-0-3/sing_890.htm">resolve_lib</a>) </li>
<li> new algorithms in primdec.lib ( <a href="/old/Manual/3-0-3/sing_863.htm">primdec_lib</a>): radical et al. </li>
<li> improved version of  <a href="/old/Manual/3-0-3/sing_286.htm">slimgb</a>, incorporated into  <a href="/old/Manual/3-0-3/sing_209.htm">groebner</a>, strategy change in groebner </li>
<li> finvar.lib: the algorithm of  <a href="/old/Manual/3-0-3/sing_1105.htm">secondary_char0</a> is now used in general in the non-modular case ( <a href="/old/Manual/3-0-3/sing_1079.htm">finvar_lib</a>) </li>
<li> finvar.lib: new algorithm for  <a href="/old/Manual/3-0-3/sing_1106.htm">irred_secondary_char0</a> ( <a href="/old/Manual/3-0-3/sing_1079.htm">finvar_lib</a>) </li>
<li> finvar.lib: new function  <a href="/old/Manual/3-0-3/sing_1109.htm">irred_secondary_no_molien</a> ( <a href="/old/Manual/3-0-3/sing_1079.htm">finvar_lib</a>) </li>
<li> finvar.lib: new functions for computing minimal generating sets of invariant rings of finite groups in the non-modular case:  <a href="/old/Manual/3-0-3/sing_1084.htm">invariant_algebra_reynolds</a> for finite matrix groups and  <a href="/old/Manual/3-0-3/sing_1085.htm">invariant_algebra_perm</a> for permutation groups ( <a href="/old/Manual/3-0-3/sing_1079.htm">finvar_lib</a>) </li>
<li> operation for sparse matrices improved: multiplication, prune, conversion to module </li>
</ul>
