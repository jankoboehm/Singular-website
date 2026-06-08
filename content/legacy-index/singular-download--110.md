---
title: "Install Singular 4.x.x on a Linux/Unix platform (via APT/DEB)"
url: "/index.php/singular-download/110.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/singular-download/110.html"
migration_status: "migrated from local legacy copy"
---

<p>The Singular repository provides a user-friendly installation of Singular on a Debian or Debian like system (such as Knoppix, Ubuntu etc.) with       installed package tool APT.  Just follow the below instructions matching your package tool.</p>
<p>The following installation instructions require <strong>superuser privileges</strong> and <strong>internet connection</strong>.</p>
Some OS versions require additional the line to enable ftp transport<p>
Dir::Bin::Methods::ftp "ftp";<p>
in /etc/apt/apt.conf or a file in /etc/apt/cond.d/<p>
<ul>
</ul>
<p>Step-by-step instructions for <strong>Debian 11/12/13</strong> (only 64 bit):</p>
<ul>
<li>add GPG key:<br /><code>wget https://www.singular.uni-kl.de/ftp/repo/extra/gpg</code><br /><code>apt-key add gpg</code></li>
<li>add (for debian11)<br /><code>deb https://www.singular.uni-kl.de/ftp/repo/debian11 bullseye main</code><br />to <code>/etc/apt/sources.list</code></li>
<li>add (for debian12)<br /><code>deb https://www.singular.uni-kl.de/ftp/repo/debian12 bookworm main</code><br />to <code>/etc/apt/sources.list</code></li>
<li>add (for debian13)<br /><code>deb https://www.singular.uni-kl.de/ftp/repo/debian13 trixie main</code><br />to <code>/etc/apt/sources.list</code></li>
<li><code>apt-get update</code></li>
<li><code>apt-get install singular41</code></li></ul>
An old version of Singular can be found in the official repositories. Note that the two versions conflict with each other.</li>
<ul>
Repository directories are at
<li><a href="https://www.singular.uni-kl.de/ftp/repo/debian11">Debian 11 repository</a></li>
<li><a href="https://www.singular.uni-kl.de/ftp/repo/debian12">Debian 12 repository</a></li>
<li><a href="https://www.singular.uni-kl.de/ftp/repo/debian13">Debian 13 repository</a></li>
</ul>
<ul>
</ul>
<ul>
</ul>
<ul>
</ul>
<p style="font-size: 12.16px;">For <strong>Ubuntu 20.04, 22.04, 24.04</strong> Singular can be found in the official repository:</p>
<ul style="font-size: 12.16px;">
<li><code>apt-get update</code></li>
<li><code>apt-get install singular</code></li>
</ul>
<p style="font-size: 12.16px; padding-left: 30px;">However, this will most probably not install the latest version. For the latest version, <a href="109.html">manually install Singular via TGZ</a>, or follow these instructions (only 64 bit):</p>
<ul style="font-size: 12.16px;">
<li>add GPG key:<br /><code>wget https://www.singular.uni-kl.de/ftp/repo/extra/gpg</code><br /><code>apt-key add gpg</code></li>
<li><code>add (for 20.04)<br /><code>deb https://www.singular.uni-kl.de/ftp/repo/ubuntu20 focal main</code><br />to <code>/etc/apt/sources.list</code></code></li>
<li><code>add (for 22.04)<br /><code>deb https://www.singular.uni-kl.de/ftp/repo/ubuntu22 jammy main</code><br />to <code>/etc/apt/sources.list</code></code></li>
<li><code>add (for 24.04)<br /><code>deb https://www.singular.uni-kl.de/ftp/repo/ubuntu24 noble main</code><br />to <code>/etc/apt/sources.list</code></code></li>
<li><code>apt-get update</code></li>
<li><code>apt-get install singular41</code></li>
</ul>
<p style="font-size: 12.16px; padding-left: 30px;">Note that the two packages <code>singular</code> and <code>singular41</code> conflict with each other.</p>
<ul>
</ul>
<ul>
Repository directories are at
<li><a href="https://www.singular.uni-kl.de/ftp/repo/ubuntu20">Ubuntu 20.04 repository</a></li>
<li><a href="https://www.singular.uni-kl.de/ftp/repo/ubuntu22">Ubuntu 22.04 repository</a></li>
<li><a href="https://www.singular.uni-kl.de/ftp/repo/ubuntu24">Ubuntu 24.04 repository</a></li>
</ul>
