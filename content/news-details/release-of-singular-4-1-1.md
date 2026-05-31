---
title: "Release of SINGULAR 4-1-1"
url: "/index.php/news/release-of-singular-4-1-1.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/news/release-of-singular-4-1-1.html"
migration_status: "migrated from local legacy copy"
---

<h2>News for version 4-1-1</h2>
<p>New syntax:</p>
<ul>
<li><code>alias</code>: may be used as a prefix to a variable declaration. Can only be used in procedure headings. ( <a href="/old/Manual/latest/sing_35.htm#SEC59">General command syntax</a>). </li>
</ul>
<p>New command:</p>
<ul>
<li><code>fres</code>: improved version of <code>sres</code>: computes a (not necessarily minimal) free resolution of the input ideal/module, using Schreyer's algorithm. ( <a href="/old/Manual/latest/sing_253.htm#SEC293">fres</a>, <a href="/old/Manual/latest/sing_352.htm#SEC392">sres</a>). </li>
</ul>
<p>Extended commands:</p>
<ul>
<li>pseudo ordering <code>L</code> allows setting of limits for exponents in polynomials ( <a href="/old/Manual/latest/sing_866.htm#SEC918">Pseudo ordering L</a>, <a href="/old/Manual/latest/sing_209.htm#SEC249">attrib</a> for <code>maxExp</code>) </li>
<li><code>%</code>,<code>mod</code>: also for poly operands ( <a href="/old/Manual/latest/sing_155.htm#SEC195">poly operations</a>). </li>
<li><code>delete</code>: extended to intvec, ideal, module ( <a href="/old/Manual/latest/sing_227.htm#SEC267">delete</a>). </li>
<li>syz ( <a href="/old/Manual/latest/sing_359.htm#SEC399">syz</a>), lift ( <a href="/old/Manual/latest/sing_285.htm#SEC325">lift</a>), liftstd ( <a href="/old/Manual/latest/sing_286.htm#SEC326">liftstd</a>), intersect( <a href="/old/Manual/latest/sing_270.htm#SEC310">intersect</a>): with a specified GB algorithm </li>
</ul>
<p>New libraries:</p>
<ul>
<li>classify2.lib: Classification of isolated singularities of corank  &lt;=2 and modality &lt;= wrt. right equivalence over the complex  numbers according to Arnold's list. ( <a href="/old/Manual/latest/sing_2321.htm#SEC2397">classify2_lib</a>) </li>
<li>goettsche.lib: Goettsche's formula for the Betti numbers of the Hilbert scheme of points on a surface, Macdonald's formula for the symmetric product ( <a href="/old/Manual/latest/sing_2404.htm#SEC2480">goettsche_lib</a>) </li>
<li>combinat.lib, modules.lib, methods,lib, nets.lib: a more mathematical view of modules ( <a href="/old/Manual/latest/sing_2342.htm#SEC2418">combinat_lib</a>: combinatorics), ( <a href="/old/Manual/latest/sing_2490.htm#SEC2566">methods_lib</a>: construct procedures), ( <a href="/old/Manual/latest/sing_2491.htm#SEC2567">modules_lib</a>: free resolutions), ( <a href="/old/Manual/latest/sing_2622.htm#SEC2698">nets_lib</a>: pretty printing) </li>
<li>ncHilb.lib: Hilbert series of non-commutative monomial algebras ( <a href="/old/Manual/latest/sing_2601.htm#SEC2677">ncHilb_lib</a>) </li>
<li>realclassify.lib: Classification of real singularities( <a href="/old/Manual/latest/sing_2674.htm#SEC2750">realclassify_lib</a>) </li>
<li>rootisolation.lib: real root isolation using interval arithmetic( <a href="/old/Manual/latest/sing_2680.htm#SEC2756">rootisolation_lib</a>) </li>
<li>rstandard.lib: Janet bases and border bases for ideals ( <a href="/old/Manual/latest/sing_2693.htm#SEC2769">rstandard_lib</a>) </li>
</ul>
<p>Changed libraries:</p>
<ul>
<li>chern.lib:  new version ( <a href="/old/Manual/latest/sing_2255.htm#SEC2331">chern_lib</a>) </li>
<li>gitfan.lib:  new (incompatible) version ( <a href="/old/Manual/latest/sing_2420.htm#SEC2496">gitfan_lib</a>) </li>
<li>grobcov.lib:  new version ( <a href="/old/Manual/latest/sing_923.htm#SEC999">grobcov_lib</a>) </li>
</ul>
<p>Changes in the kernel/build system:</p>
<ul>
<li>port to polymake 3.x.x </li>
<li>port to NTL 10 with threads (needs also C++11: gcc6 or -std=c++11) </li>
<li>p_Invers is only a helper for p_Series: now static </li>
<li>p_Divide is now p_MDivide, pDivive is a new routine </li>
</ul>
