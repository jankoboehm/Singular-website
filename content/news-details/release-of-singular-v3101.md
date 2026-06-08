---
title: "Release of SINGULAR 3-1-0-1"
url: "/index.php/news/release-of-singular-v3101.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/news/release-of-singular-v3101.html"
migration_status: "migrated from local legacy copy"
---

<p class="archive-links">Published: Thursday, 30 April 2009 00:00</p>

<h2>News for version 3.1.0.1</h2>
<ul>
<li> new coefficients: Z, Z/m, Z/(2^n) (see  <a href="/old/Manual/latest/sing_28.htm#SEC38">Rings and orderings</a>) </li>
<li> new handling of the default argument in libraries (see  <a href="/old/Manual/latest/sing_45.htm#SEC83">Parameter list</a>) </li>
<li> <code>ESingular</code> updated for emacs 22 </li>
<li> licences for all parts of SINGULAR clarified (see  <a href="/old/Manual/latest/sing_1.htm#SEC1">Preface</a>) </li>
</ul>
<h2>New SINGULAR functions</h2>
<!--docid::SEC1665::--> 
<ul>
<li> new command: kernel (see  <a href="/old/Manual/latest/sing_226.htm#SEC267">kernel</a>) </li>
<li> new command: sqrfree (see  <a href="/old/Manual/latest/sing_289.htm#SEC330">sqrfree</a>) </li>
<li> command changed: the first argument to <code>monitor</code> should be an ASCII link. (see  <a href="/old/Manual/latest/sing_246.htm#SEC287">monitor</a>) </li>
<li> command extended: eliminate: variables to eliminate may also be given as intvec. (see  <a href="/old/Manual/latest/sing_189.htm#SEC230">eliminate</a>) </li>
</ul>
<h2>Internal Changes</h2>
<!--docid::SEC1666::--> 
<ul>
<li> handling of large input for std improved </li>
<li> <a href="/old/Manual/latest/sing_220.htm#SEC261">interred</a> implemented in a different way </li>
<li> <a href="/old/Manual/latest/sing_225.htm#SEC266">kbase</a> honors the attribute "isHomog" </li>
<li> <a href="/old/Manual/latest/sing_222.htm#SEC263">jacob</a> accepts modules and matrices</li>
<li><a href="/old/Manual/latest/sing_206.htm#SEC247">gcd</a> over algebraic extensions of the rationals implemented in a different way </li>
<li>new build target: libsingular.a (for gfan etc.) </li>
<li>code variants now depend on CPU type, not OS </li>
<li>better test for built-in limits (see  <a href="/old/Manual/latest/sing_343.htm#SEC384">Limitations</a>) </li>
<li> operator <code>new(size_t,const std::nothrow_t&amp;)</code> now also overloaded </li>
</ul>
<p><a name="SEC1667"></a></p>
<h2>New SINGULAR libraries</h2>
<!--docid::SEC1667::--> 
<ul>
<li> surfex: new version 0.90 (see  <a href="/old/Manual/latest/sing_1334.htm#SEC1411">surfex_lib</a>). </li>
<li> new library: redcgs.lib (see  <a href="/old/Manual/latest/sing_762.htm#SEC839">redcgs_lib</a>: Reduced Comprehensive Groebner Systems) </li>
<li> new library: tropical.lib (see  <a href="/old/Manual/latest/sing_1545.htm#SEC1622">tropical_lib</a>: Computations in Tropical Geometry) </li>
<li> new library: polymake.lib (see  <a href="/old/Manual/latest/sing_1524.htm#SEC1601">polymake_lib</a>: Computations with polytopes and fans, interface to polymake and TOPCOM) </li>
<li> new library: sing4ti2.lib (see  <a href="/old/Manual/latest/sing_1030.htm#SEC1107">sing4ti2_lib</a>: interface to 4ti2 </li>
<li> new library: decodegb.lib (see  <a href="/old/Manual/latest/sing_1355.htm#SEC1432">decodegb_lib</a>: Generating and solving systems of polynomial equations for decoding and finding the minimum distance of linear codes) </li>
<li> new library: dmodapp.lib (see  <a href="/old/Manual/latest/sing_498.htm#SEC551">dmodapp_lib</a>: applications of D-modules) </li>
<li> new library: bfun.lib global (see  <a href="/old/Manual/latest/sing_432.htm#SEC485">bfun_lib</a>: Bernstein-Sato polynomial) </li>
<li> new library: freegb.lib (see  <a href="/old/Manual/latest/sing_517.htm#SEC570">freegb_lib</a>): Twosided Non-commutative Groebner bases in Free Algebras </li>
<li> new library: jacobson.lib (see  <a href="/old/Manual/latest/sing_1392.htm#SEC1469">jacobson_lib</a>): Algorithms for Smith and Jacobson Normal Form </li>
<li> contributed library: cimonom.lib (see  <a href="/old/Manual/latest/sing_869.htm#SEC946">cimonom_lib</a>): determines if the toric ideal of an affine monomial curve is a complete intersection </li>
<li> contributed library: phindex.lib (see  <a href="/old/Manual/latest/sing_1579.htm#SEC1656">phindex_lib</a>): Poincare-Hopf index of a real analytic vector field </li>
</ul>
<p><a name="SEC1668"></a></p>
<h2>Changed SINGULAR libraries</h2>
<!--docid::SEC1668::--> 
<ul>
<li> normal.lib ( <a href="/old/Manual/latest/sing_950.htm#SEC1027">normal_lib</a>): changed structure of the result, <br /> new algorithms have been implemented which improve the performance </li>
<li> elim.lib ( <a href="/old/Manual/latest/sing_873.htm#SEC950">elim_lib</a>):  <a href="/old/Manual/latest/sing_876.htm#SEC953">elim</a>,  <a href="/old/Manual/latest/sing_879.htm#SEC956">nselect</a>,  <a href="/old/Manual/latest/sing_881.htm#SEC958">select</a>,  <a href="/old/Manual/latest/sing_882.htm#SEC959">select1</a>: changed syntax </li>
<li> homolog.lib: kernel renamed to  <a href="/old/Manual/latest/sing_904.htm#SEC981">hom_kernel</a>.  <br />(See also  <a href="/old/Manual/latest/sing_226.htm#SEC267">kernel</a>,  <a href="/old/Manual/latest/sing_861.htm#SEC938">alg_kernel</a>). </li>
<li> matrix.lib ( <a href="/old/Manual/latest/sing_794.htm#SEC871">matrix_lib</a>): new commands for computing symmetric/exterior powers/bases </li>
<li> surf.lib: new command <code>surfer</code>: interface to program <code>surfer</code> <br />(See  <a href="/old/Manual/latest/sing_1331.htm#SEC1408">surf_lib</a>). </li>
<li> teachstd.lib ( <a href="/old/Manual/latest/sing_1470.htm#SEC1547">teachstd_lib</a>): spoly works now in non-commutative algebras and  <a href="/old/Manual/latest/sing_1483.htm#SEC1560">standard</a> can thus be used there. However, since product criterion is a priori not applicable in the non-commutative case, one may want to disable it first (see <code>prodcrit</code> for details). </li>
<li> many changes of names in libraries (to have a more consistent naming scheme) </li>
</ul>
