---
title: "Release of SINGULAR 4-1-2"
url: "/index.php/news/release-of-singular-4-1-2.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/news/release-of-singular-4-1-2.html"
migration_status: "migrated from local legacy copy"
---

<h2>News for version 4-1-2</h2>
<p>New libraries:</p>
<ul>
<li>arnoldclassify.lib: Arnol'd Classifier of Singularities ( <a href="/old/Manual/latest/sing_2337.htm#SEC2413">arnoldclassify_lib</a>) </li>
<li>difform.lib: Procedures for differential forms ( <a href="/old/Manual/latest/sing_2454.htm#SEC2530">difform_lib</a>) </li>
<li>dmodideal.lib: Algorithms for Bernstein-Sato ideals of morphisms ( <a href="/old/Manual/latest/sing_591.htm#SEC643">dmodideal_lib</a>) </li>
<li>fpalgebras.lib: Generation of various algebras in the letterplace case ( <a href="/old/Manual/latest/sing_811.htm#SEC863">fpalgebras_lib</a>) </li>
<li>ncrat.lib: non-commutatie rational functions ( <a href="/old/Manual/latest/sing_863.htm#SEC915">ncrat_lib</a>) </li>
</ul>
<p>Changed libraries:</p>
<ul>
<li>freegb.lib: lpDivision, lpPrint ( <a href="/old/Manual/latest/sing_849.htm#SEC901">freegb_lib</a>) </li>
<li>fpadim.lib ( <a href="/old/Manual/latest/sing_805.htm#SEC857">fpadim_lib</a>) </li>
<li>schreyer.lib: deprecated </li>
<li>goettsche.lib: new, extended version (The Nakajima-Yoshioka  formula up to n-th degree,Poincare Polynomial of the punctual  Quot-scheme of rank r on n planar points Betti numbers of the punctual  Quot-scheme of rank r on n planar points)( <a href="/old/Manual/latest/sing_2554.htm#SEC2630">goettsche_lib</a>) </li>
<li>grobcov.lib: small bug fix ( <a href="/old/Manual/latest/sing_1014.htm#SEC1090">grobcov_lib</a>) </li>
</ul>
<p>Changes in the kernel/build system:</p>
<ul>
<li>integrated xalloc into omalloc: (<code>./configure --disable-omalloc</code>) </li>
<li>improved heuristic for <code>det</code> ( <a href="/old/Manual/latest/sing_230.htm#SEC270">det</a>) </li>
<li>improved reading of long polynomials </li>
<li>improved groebner bases over Z coefficients </li>
<li>code for free algebras (letterplace rings) rewritten (using now the standrad <code>+,-,*,^,std</code>,...) ( <a href="/old/Manual/latest/sing_789.htm#SEC841">LETTERPLACE</a>) </li>
<li>new commands <code>rightstd</code> ( <a href="/old/Manual/latest/sing_796.htm#SEC848">rightstd (letterplace)</a>) </li>
<li>extended <code>twostd</code> to L<small>ETTERPLACE</small> ( <a href="/old/Manual/latest/sing_798.htm#SEC850">twostd (letterplace)</a>,  <a href="/old/Manual/latest/sing_485.htm#SEC525">twostd (plural)</a>) </li>
<li>pseudo type <code>polyBucket</code> </li>
<li>new type <code>smatrix</code>: sparse matrix (experimental) ( <a href="/old/Manual/latest/sing_171.htm#SEC211">smatrix</a>). </li>
<li>extended <code>coef</code> to ideals ( <a href="/old/Manual/latest/sing_219.htm#SEC259">coef</a>). </li>
<li>error and signal handling in <code>libSingular</code> ( <a href="/old/Manual/latest/sing_2872.htm#SEC2962">libSingular</a>). </li>
<li>updated gfanlib to version 0.6.2 </li>
<li>port to NTL 11 (needs C++11: gcc6 or -std=c++11), which does not conflict with polymake (needs C++14) </li>
</ul>
