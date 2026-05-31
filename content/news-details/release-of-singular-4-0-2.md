---
title: "Release of SINGULAR 4-0-2"
url: "/index.php/news/release-of-singular-4-0-2.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/news/release-of-singular-4-0-2.html"
migration_status: "migrated from local legacy copy"
---

<h2>News for version 4-0-2</h2>
<p>New commands:</p>
<ul>
<li>align ( <a href="/old/Manual/4-0-2/sing_260.htm#SEC299">align</a>) </li>
<li>branchTo ( <a href="/old/Manual/4-0-2/sing_155.htm#SEC194">procs with different argument types</a>) </li>
<li><code>-&gt;</code> ( <a href="/old/Manual/4-0-2/sing_154.htm#SEC193">proc expression</a>) </li>
</ul>
<p>Change in ring handling:</p>
<ul>
<li><code>typeof(</code> qring <code>)</code> returns <code>"ring"</code> </li>
</ul>
<p>New libraries:</p>
<ul>
<li>algemodstd.lib:  Groebner bases of ideals in polynomial rings       over algebraic number fields( <a href="/old/Manual/4-0-2/sing_2025.htm#SEC2100">algemodstd_lib</a>) </li>
<li>arr.lib: arrangements of hyperplanes ( <a href="/old/Manual/4-0-2/sing_2028.htm#SEC2103">arr_lib</a>) </li>
<li>brillnoether.lib: Riemann-Roch spaces of divisors on curve ( <a href="/old/Manual/4-0-2/sing_2073.htm#SEC2148">brillnoether_lib</a>) </li>
<li>hess.lib: Riemann-Roch space of divisors       on function fields and curves ( <a href="/old/Manual/4-0-2/sing_2155.htm#SEC2230">hess_lib</a>) </li>
<li>gradedModules.lib: graded modules/matrices/resolutions ( <a href="/old/Manual/4-0-2/sing_2142.htm#SEC2217">gradedModules_lib</a>) </li>
</ul>
<p>Changed libraries:</p>
<ul>
<li>revised polymake interface ( <a href="/old/Manual/4-0-2/sing_1941.htm#SEC2016">polymake_lib</a>, <a href="/old/Manual/4-0-2/sing_2284.htm#SEC2359">polymake_so</a>) </li>
<li>revised gfanlib interface ( <a href="/old/Manual/4-0-2/sing_2275.htm#SEC2350">gfanlib_so</a>) </li>
<li>Presolve::findvars ( <a href="/old/Manual/4-0-2/sing_1672.htm#SEC1747">findvars</a>,  <a href="/old/Manual/4-0-2/sing_416.htm#SEC455">variables</a>) </li>
<li>Ring::addvarsTo ( <a href="/old/Manual/4-0-2/sing_1043.htm#SEC1118">addvarsTo</a>) </li>
<li>Ring::addNvarsTo ( <a href="/old/Manual/4-0-2/sing_1044.htm#SEC1119">addNvarsTo</a>) </li>
<li>Ring::hasAlgExtensionCoefficient ( <a href="/old/Manual/4-0-2/sing_1039.htm#SEC1114">hasAlgExtensionCoefficient</a>) </li>
<li>Schreyer::s_res ( <a href="/old/Manual/4-0-2/sing_2270.htm#SEC2345">s_res</a>) </li>
<li>grobcov.lib (grobcovK) ( <a href="/old/Manual/4-0-2/sing_956.htm#SEC1031">grobcov_lib</a>) with new routines    AddCons ( <a href="/old/Manual/4-0-2/sing_971.htm#SEC1046">AddCons</a>), AddConsP ( <a href="/old/Manual/4-0-2/sing_972.htm#SEC1047">AddConsP</a>). </li>
<li>normaliz.lib (for normaliz &gt;=2.8) ( <a href="/old/Manual/4-0-2/sing_1243.htm#SEC1318">normaliz_lib</a>) </li>
<li>renamed groebnerFan to groebnerFanP in polymake.lib ( <a href="/old/Manual/4-0-2/sing_1941.htm#SEC2016">polymake_lib</a>) </li>
<li>renamed fVector to fVectorP in polymake.lib ( <a href="/old/Manual/4-0-2/sing_1941.htm#SEC2016">polymake_lib</a>, <a href="/old/Manual/4-0-2/sing_2284.htm#SEC2359">polymake_so</a>) </li>
</ul>
