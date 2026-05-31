---
title: "Release of SINGULAR 4-1-0"
url: "/index.php/news/release-of-singular-4-1-0.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/news/release-of-singular-4-1-0.html"
migration_status: "migrated from local legacy copy"
---

<h2>News for version 4-1-0</h2>
<p>Syntax changes:</p>
<ul>
<li>new (additional) form of ring definitions: (for example <code>ring R=QQ[x,y,z];</code>)       ( <a href="/old/Manual/latest/sing_30.htm#SEC41">General syntax of a ring declaration</a>) </li>
<li>new (additional) form of multi-indicies: (for example <code>i(1,2,3,4,5)</code>)       ( <a href="/old/Manual/latest/sing_37.htm#SEC65">Names</a>) </li>
<li>changed behaviour of <code>charstr</code> ( <a href="/old/Manual/latest/sing_209.htm#SEC249">charstr</a>) </li>
<li>new data type <code>cring</code> to describe the coeffient rings, to be used       for the new definitions for (polynomial) rings ( <a href="/old/Manual/latest/sing_30.htm#SEC41">General syntax of a ring declaration</a>) </li>
<li>new command <code>ring_list</code> to access the parts used to contruct polynomial rings ( <a href="/old/Manual/latest/sing_333.htm#SEC373">ring_list</a>, <a href="/old/Manual/latest/sing_332.htm#SEC372">ringlist</a>) </li>
<li>extended polynomial ring construction: also from lists produced by <code>ring_list</code> </li>
<li>new attribute <code>ring_cf</code> for <code>ring</code> ( <a href="/old/Manual/latest/sing_204.htm#SEC244">attrib</a>) </li>
<li>printing of rings changed to match <code>cring</code> names ( <a href="/old/Manual/latest/sing_209.htm#SEC249">charstr</a>) </li>
</ul>
<p>New libraries:</p>
<ul>
<li>new library: classifyMapGerms.lib: standard basis of the tangent space at the orbit of an algebraic group action ( <a href="/old/Manual/latest/sing_2301.htm#SEC2377">classifyMapGerms_lib</a>) </li>
<li>new library: ffmodstd.lib:  Groebner bases of ideals in polynomial rings over algebraic function fields( <a href="/old/Manual/latest/sing_2337.htm#SEC2413">ffmodstd_lib</a>) </li>
<li>new library: nfmodsyz.lib: syzygy modules of submodules of free modules       over algebraic number fields( <a href="/old/Manual/latest/sing_2482.htm#SEC2558">nfmodsyz_lib</a>) </li>
<li>new library: curveInv.lib: invariants of curves ( <a href="/old/Manual/latest/sing_2309.htm#SEC2385">curveInv_lib</a>) </li>
<li>new library: gfan.lib: interface to gfanlib ( <a href="/old/Manual/latest/sing_1993.htm#SEC2069">gfan_lib</a>) </li>
<li>extended library: interface to polymake merged into  <a href="/old/Manual/latest/sing_2052.htm#SEC2128">polymake_lib</a> </li>
<li>new library: tropicalNewton.lib: Newton polygon methods in tropical geometry ( <a href="/old/Manual/latest/sing_2535.htm#SEC2611">tropicalNewton_lib</a>) </li>
<li>new library: schubert.lib: some procedures for intersction theory ( <a href="/old/Manual/latest/sing_2496.htm#SEC2572">schubert_lib</a>) </li>
</ul>
<p>Changed libraries:</p>
<ul>
<li>classify_aeq.lib: new procedures ( <a href="/old/Manual/latest/sing_2293.htm#SEC2369">classify_aeq_lib</a>) </li>
<li>grobcov.lib: new version ( <a href="/old/Manual/latest/sing_900.htm#SEC976">grobcov_lib</a>) </li>
<li>ncfactor.lib: factorization in some noncommuative algebras ( <a href="/old/Manual/latest/sing_684.htm#SEC736">ncfactor_lib</a>) with new routine ncfactor ( <a href="/old/Manual/latest/sing_685.htm#SEC737">ncfactor</a>) </li>
<li>primdec.lib: new option "subsystem" ( <a href="/old/Manual/latest/sing_1270.htm#SEC1346">primdec_lib</a>) </li>
</ul>
<p>Changes in the kernel:</p>
<ul>
<li>improved mapping of polynomials/ideals/... </li>
<li>port to gcc 6 </li>
<li>port to gfanlib 0.6 (requires C++11, i.e. gcc &gt;=4.3) </li>
<li>port to NTL 10 </li>
<li>port to polymake 3.0 </li>
<li>port to readline 7 </li>
<li> <a href="/old/Manual/latest/sing_335.htm#SEC375">sba</a> works for global orderings, also for coefficient types Z and Z/m </li>
<li> <a href="/old/Manual/latest/sing_346.htm#SEC386">std</a> works for all orderings, also for coefficient types Z and Z/m with local/mixed orderings </li>
<li> <a href="/old/Manual/latest/sing_236.htm#SEC276">factorize</a> works for polynomial rings over ZZ </li>
</ul>
<p>Experimental stuff:</p>
<ul>
<li>module  <a href="/old/Manual/latest/sing_2202.htm#SEC2278">customstd_lib</a>: modify <code>std</code> ( <a href="/old/Manual/latest/sing_2204.htm#SEC2280">satstd</a>) </li>
</ul>
