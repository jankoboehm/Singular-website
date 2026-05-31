---
title: "Release of SINGULAR 4-2-0"
url: "/index.php/news/release-of-singular-4-2-0.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/news/release-of-singular-4-2-0.html"
migration_status: "migrated from local legacy copy"
---

<p>Syntax changes:</p>
<ul>
<li>renamed poly.lib to polylib.lib ( <a href="/old/Manual/4-2-0/sing_1077.htm#SEC1158">polylib_lib</a>) </li>
</ul>
<p>New libraries:</p>
<p> </p>
<ul>
<li>interval.lib: interval arithmetic ( <a href="/old/Manual/4-2-0/sing_2037.htm#SEC2118">interval_lib</a>) </li>
<li>maxlike.lib: algebraic statistics ( <a href="/old/Manual/4-2-0/sing_2795.htm#SEC2876">maxlike_lib</a>) </li>
<li>nchilbert.lib: Hilbert series for LetterPlace algebras ( <a href="/old/Manual/4-2-0/sing_661.htm#SEC715">nchilbert_lib</a>) </li>
<li>polyclass.lib: class of polynomials ( <a href="/old/Manual/4-2-0/sing_2949.htm#SEC3030">polyclass_lib</a>) </li>
<li>recover.lib: Hybrid numerical/symbolical algorithms ( <a href="/old/Manual/4-2-0/sing_2082.htm#SEC2163">recover_lib</a>) </li>
<li>redcgs.lib: Reduced Comprehensive Groebner Systems ( <a href="/old/Manual/4-2-0/sing_1098.htm#SEC1179">redcgs_lib</a>) </li>
<li>ringgb.lib: coefficient rings ( <a href="/old/Manual/4-2-0/sing_2953.htm#SEC3034">ringgb_lib</a>) </li>
<li>sets.lib: Sets ( <a href="/old/Manual/4-2-0/sing_2962.htm#SEC3043">sets_lib</a>) </li>
<li>stanleyreisner.lib: T1 and T2 for a general Stanley-Reiser ring ( <a href="/old/Manual/4-2-0/sing_2971.htm#SEC3052">stanleyreisner_lib</a> </li>
<li>systhreads.lib: multi-threaded objects ( <a href="/old/Manual/4-2-0/sing_2981.htm#SEC3062">systhreads_lib</a>) </li>
</ul>
<p>Changed libraries:</p>
<ul>
<li>classify_aeq.lib: new procedure <code>classSpaceCurve</code> ( <a href="/old/Manual/4-2-0/sing_1799.htm#SEC1880">classify_aeq_lib</a>) </li>
<li>grobcov.lib: new version ( <a href="/old/Manual/4-2-0/sing_1033.htm#SEC1114">grobcov_lib</a>) </li>
<li>modular.lib: parallel version for verification via <code>system("verifyGB",I)</code> </li>
</ul>
<p>New commands:</p>
<ul>
<li><code>system("verifyGB",I)</code>: test, if I is a Groebner basis (using parallel processes) </li>
<li>Letterplace: modulo,syz,lift,liftstd, rightStd ( <a href="/old/Manual/4-2-0/sing_799.htm#SEC853">LETTERPLACE</a>) </li>
</ul>
<p>Changes in the kernel/build system:</p>
<ul>
<li>update for using FLINT 2.6.x and for FLINT 2.7.0 </li>
<li>Singular can be build with NTL or FLINT or both (if non is availabel, <code>factroize</code> and <code>gcd</code> will not work.) </li>
</ul>
