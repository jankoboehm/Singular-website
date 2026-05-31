---
title: "How to Cite Singular"
url: "/index.php/how-to-cite-singular.html"
description: "Citation information for Singular."
legacy_source: "index.php/how-to-cite-singular.html"
migration_status: "migrated from local legacy copy"
---

Singular is a free service to the scientific community.      The only request we have is to acknowledge its usage.</p>
<p>If you have used Singular in the       preparation of a publication, please use the following BibTeX entry       (with adjusted Singular version and year, here 4-2-1 and 2021, respectively):</p>
<pre>@misc {DGPS,
 title = {{\sc Singular} {4-4-0} --- {A} computer algebra system for polynomial computations},
 author = {Decker, Wolfram and Greuel, Gert-Martin and Pfister, Gerhard and Sch\"onemann, Hans},
 year = {2024},
 howpublished = {\url{http://www.singular.uni-kl.de}},
}</pre>
<!-- [GPS01] G.-M. Greuel, G. Pfister, H. Sch\"onemann: {\sc Singular} 3.0 - A Computer Algebra System for Polynomial Computations. In M. Kerber and M. Kohlhase: Symbolic Computation and Automated Reasoning, The Calculemus-2000 Symposium. (2001), 227-233. --> <!-- [GPS05] G.-M. Greuel, G. Pfister, and H. Sch\"onemann. {\sc Singular} 3.0 A Computer Algebra System for Polynomial Computations. Centre for Computer Algebra, University of Kaiserslautern (2005). {\tt http://www.singular.uni-kl.de}. -->
<p>If you are using LaTeX, but<strong> not </strong>BibTeX, here is the bibliography   environment of LaTeX. (Again, Singular version and year may have to be adjusted.)</p>
<pre>\bibitem[DGPS]{DGPS}<br />Decker, W.; Greuel, G.-M.; Pfister, G.; Sch{\"o}nemann, H.: <br />\newblock {\sc Singular} {4-4-0} --- {A} computer algebra system for polynomial computations.<br />\newblock {https://www.singular.uni-kl.de} (2024).</pre>
<p>Please remember that Singular itself uses other C/C++ libraries,    like NTL, GMP, etc.</p>
<p>If you have used a particular Singular library then you should, additionally,    cite it as in the following example:</p>
<pre>\bibitem[GLP]{GLP} <br />Greuel, G.-M.; Laplagne, S.; Pfister, G.: <br />{\tt normal.lib}. {A} {\sc Singular} {4-2-0} library for computing<br />the normalization of affine rings (2020).</pre>
<p>(Make once again sure that Singular version and year are correct.)<br /> Information on author(s) and purpose of a library can be found in the header of the library file (here: normal.lib).</p>
