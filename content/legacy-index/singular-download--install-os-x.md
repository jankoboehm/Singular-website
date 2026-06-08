---
title: "Install Singular 4-x-x on an OS X Platform"
url: "/index.php/singular-download/install-os-x.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/singular-download/install-os-x.html"
migration_status: "migrated from local legacy copy"
---

<h2 class="contentheading">Install Singular 4-x-x on an OS X Platform</h2>
<p>You can either install Singular from a dmg file or based on a fink installation:</p>
<h2>Installation from a dmg File</h2>
<p>Download <a href="/ftp/pub/Math/Singular/UNIX/Singular-4-3-2_64.dmg">/ftp/pub/Math/Singular/UNIX/Singular-4-3-2_64.dmg</a>. (x86_64 cpu) or <a href="/ftp/pub/Math/Singular/UNIX/Singular-4-4-0_M1.dmg">/ftp/pub/Math/Singular/UNIX/Singular-4-4-0_M1.dmg</a> (M1 cpu)</p>
<p>(Mirror:<a href="/ftp/pub/Math/Singular/UNIX/Singular-4-3-2_64.dmg">https://www.singular.uni-kl.de/ftp/pub/Math/Singular/UNIX/Singular-4-3-2_64.dmg</a>) and <a href="/ftp/pub/Math/Singular/UNIX/Singular-4-4-0_M1.dmg">https://www.singular.uni-kl.de/ftp/pub/Math/Singular/UNIX/Singular-4-4-0_M1.dmg</a>.</p>
<p>Installing Singular from one of these requires you to mount the image    and move its contents to your computer’s “Applications” directory.</p>
<p> </p>
<p> </p>
<p>If your Mac refuses to open Singular because of an "unidentified developer":<br />Open System Preferences. Go to the Security &amp; Privacy tab. Click on<br />the lock and enter your password so you can make changes. Change the<br />setting for 'Allow apps downloaded from' to 'App Store and identified<br />developers'.<br />You may also check <a href="https://support.apple.com/en-en/guide/mac-help/mh40616/mac">https://support.apple.com/en-en/guide/mac-help/mh40616/mac</a> <br /><br /></p>
<h2>Homebrew Installation</h2>
<p>To install Singular via Homebrew, simply type:</p>
<pre><strong>brew install Singular</strong></pre>
<p>We would like to thank Karim Abou Zeid for providing the Homebrew installation. For questions, please contact karim.abou.zeid (at) rwth-aachen.de.</p>
<h2>Fink Installation</h2>
<p>Alternatively, Singular for OS X is available via the fink project which aims at  bringing the full world of Unix Open Source software to Darwin and  OS X.</p>
<ol style="list-style-type:none;">
<li style="float:left;"> <a class="wanted" href="http://www.finkproject.org/download/index.php?phpLang=en">Fink Installation</a></li>
</ol>
<p> </p>
<p> </p>
<p>Ideally, after <strong>installing fink</strong>, type in a terminal:</p>
<pre><strong>fink selfupdate</strong><br /><br /><strong>fink install singular singular-doc<br /></strong></pre>
<ol style="list-style-type:none;"> </ol> 
<ul>
</ul>
