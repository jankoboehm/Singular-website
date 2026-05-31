---
title: "Release of SINGULAR 4-3-0"
url: "/index.php/news/release-of-singular-4-3-0.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/news/release-of-singular-4-3-0.html"
migration_status: "migrated from local legacy copy"
---

<h2>News for version 4.3.0</h2>
<p>New libraries:</p>
<ul>
<li>enumpoints.lib: enumerating rational points ( <a href="/old/Manual/4-3-0/sing_2784.htm#SEC2865">enumpoints_lib</a>) </li>
<li>sagbigrob.lib: Sagbi-Groebner basis of an ideal of a subalgebra ( <a href="/old/Manual/4-3-0/sing_2953.htm#SEC3034">sagbigrob_lib</a>) </li>
<li>puiseuxexpansion.lib: Puiseux expansions over algebraic extensions ( <a href="/old/Manual/4-3-0/sing_2938.htm#SEC3019">puiseuxexpansions_lib</a>) </li>
<li>integralbasis_lib: Integral basis in algebraic function fields: new version ( <a href="/old/Manual/4-3-0/sing_1337.htm#SEC1418">integralbasis_lib</a>) </li>
</ul>
<p>Changes in the kernel/build system:</p>
<ul>
<li>ABI change: all number routines (<code>n_...</code>) have only <code>coeffs</code> as last argument,      functions with <code>ring</code> as last argument are removed </li>
<li>PATH is not changed for <code>system("sh",..)</code> (use  <a href="/old/Manual/4-3-0/sing_361.htm#SEC401">SingularBin</a>) </li>
<li><code>hilb</code> avoids int overflow (also in <code>degree, stdhilb</code>) </li>
<li><code>liftstd</code> (with 2 arguments) improved ( <a href="/old/Manual/4-3-0/sing_289.htm#SEC329">liftstd</a>) </li>
<li><code>noether</code> improved ( <a href="/old/Manual/4-3-0/sing_403.htm#SEC443">noether</a>), use in <code>groebner(I,"HC")</code> for faster results for local orderings, 0-dimensional ideals ( <a href="/old/Manual/4-3-0/sing_261.htm#SEC301">groebner</a>). </li>
<li>letterplace routines improved ( <a href="/old/Manual/4-3-0/sing_799.htm#SEC853">LETTERPLACE</a>) </li>
<li>info file is now <code>singular.info</code> instead of <code>singular.hlp</code> </li>
<li>update for using FLINT 2.8.x </li>
</ul>
<p><a name="SEC3082"></a></p>
