---
title: "Install Singular 4-x-x on a Microsoft Windows Platform"
url: "/index.php/singular-download/install-windows.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/singular-download/install-windows.html"
migration_status: "migrated from local legacy copy"
---

<h2 class="contentheading">Install Singular 4-x-x on a Microsoft Windows Platform</h2>
<p><strong> </strong></p>
<p><span style="font-size: 12.16px;">1) install cygwin (<a href="https://cygwin.com/setup-x86_64.exe"> https://cygwin.com/setup-x86_64.exe</a>) with default settings,</span></p>
<p><span style="font-size: 12.16px;">at "Cygwin setup - Select packages" change "View" to Full and "Search" to wget,</span></p>
<p><span style="font-size: 12.16px;">change in the row "wget" the column "New" from "Skip" to some version</span></p>
<p><span style="font-size: 12.16px;">and finish the installation</span></p>
<p>2) in the cygwin terminal:</p>
wget https://www.singular.uni-kl.de/ftp/repo/cygwin/64/build.tar <br /> tar xf build.tar;
bash build_cygwin</p>
<p>Now Singular can be started within the cygwin terminal as Singular.</p>
<p> </p>
<p><strong style="font-size: 12.16px;">Important Note:</strong><span style="font-size: 12.16px;"> </span><span style="font-size: 12.16px;">If you want to make use of the Singular</span><strong style="font-size: 12.16px;"> </strong><span style="font-size: 12.16px;">command</span><span style="font-size: 12.16px;"> </span><span style="font-family: Courier;">surfer</span><span style="font-size: 12.16px;">, you will additionally have to download and install</span><span style="font-size: 12.16px;"> </span><a href="http://data.imaginary2008.de/surfer-setup.exe" target="_blank" style="font-size: 12.16px;">surfer-setup.exe</a><span style="font-size: 12.16px;">, and make sure that the newly installed surfer.exe is included in the Windows environment variable</span><span style="font-size: 12.16px;"> </span><em style="font-size: 12.16px;">Path</em><span style="font-size: 12.16px;">.</span></p>
<div><span style="font-size: 12.16px;">All versions of Singular and all setup routines are powered by </span><a href="http://www.cygwin.com/" target="_blank" style="font-size: 12.16px;">Cygwin</a><span style="font-size: 12.16px;"> and their setup program.</span></div>

<h2 class="contentheading">Alternative Install of Singular 4-x-x on a Microsoft Windows Platform</h2>
<ol>
  <li>
    Get Ubuntu "bash" in cmd. Install "Linux subsystem for Windows" with Ubuntu.
    Follow the instructions at <a href="https://msdn.microsoft.com/en-us/commandline/wsl/install_guide">https://msdn.microsoft.com/en-us/commandline/wsl/install_guide</a>.
  </li>
  <li>Open Ubuntu bash. Hit Start then type "bash", or open command prompt and type "bash".</li>
  <li>Install the Ubuntu version of Singular through bash. Type <code>apt install singular</code>.</li>
</ol>
