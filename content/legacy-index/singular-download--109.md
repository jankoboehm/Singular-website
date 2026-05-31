---
title: "Install Singular 4-x-x on a Linux/Unix platform (Generic Installation)"
url: "/index.php/singular-download/109.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/singular-download/109.html"
migration_status: "migrated from local legacy copy"
---

<h2>Downloading SINGULAR Archives</h2>
<p>To install Singular on a Unix (inluding Linux and Mac Os X) platform, you need the following archiv:</p>
<ol> </ol> 
<ul>
<li><code>Singular-x-x-x-architecture.tar.gz</code> (system dependent)</li>
</ul>
<ol> </ol>
<p>where you have to replace the following:</p>
<ul>
<li>"x-x-x" has to be replaced by the version number of the Singular system to be installed</li>
<li><span style="font-family: courier new,courier;">"architecture"</span> has to be replaced according to the following table:                                          
<table style="width: 341px; height: 175px; border-color: #808080;" border="1">
<tbody>
<tr>
<th>Architecture</th> <th>Description of System</th>
</tr>
<tr>
<td><code>ix86-Linux</code></td>
<td>32-bit Linux System on Intel 	      Pentium (or compatible)</td>
</tr>
<tr>
<td><code>x86_64-Linux</code></td>
<td>64-bit Linux System on AMD 64 	      (or compatible)</td>
</tr>
<tr>
<td><code>ix86-freebsd</code></td>
<td>32-bit FreeBSD on Intel 	      Pentium (or compatible)</td>
</tr>
</tbody>
</table>
These (and other) archives can be downloaded from <a href="ftp://jim.mathematik.uni-kl.de/pub/Math/Singular/UNIX">ftp://jim.mathematik.uni-kl.de/pub/Math/Singular/UNIX</a>.
<p> </p>
A mirror is at <a href="/ftp/pub/Math/Singular/UNIX/"> https://www.singular.uni-kl.de/ftp/pub/Math/Singular/UNIX/ </a>.</li>
</ul>
<p>Please contact us if you cannot find an archive appropriate for your architecture.</p>
<h2>Installing SINGULAR</h2>
<p>Make sure that you have approximately 12MByte of free disk space and follow these steps:</p>
<p> </p>
<ol>
<li>Change to the directory where you wish to install Singular, for example: </li>
</ol> 
<table border="0">
<tbody>
<tr>
<td><br /></td>
<td class="smallexample"><code> cd /usr/local</code></td>
</tr>
</tbody>
</table>
<ol>
<li> (this requires <strong>superuser privileges</strong>), or </li>
</ol>
<p> </p>
<table border="0">
<tbody>
<tr>
<td><br /></td>
<td class="smallexample"><code> mkdir install; cd install </code></td>
</tr>
</tbody>
</table>
<ol>
<li> (requires <strong>no superuser privileges</strong>).
<p style="text-align: justify;">Singular specific subdirectories will be created in such a way that multiple versions and multiple architecture dependent files of Singular can peaceably coexist under the same <code>/usr/local</code> tree.</p>
</li>
<li> Unpack the archiv: </li>
</ol>
<p> </p>
<table border="0">
<tbody>
<tr>
<td><br /></td>
<td class="smallexample"><code>gzip -dc path-to-your-download-folder/Singular-x-x-x-architecture.tar.gz | tar -pxf -</code></td>
</tr>
</tbody>
</table>
<ol>
<li> (Do not forget to replace the string <span style="font-family: courier new,courier;">architecture </span>as above.)<br />
<p style="text-align: justify;">For the executable to work, the directory layout must look pretty much like this; the executable looks for "sibling" directories at run-time to figure out where its Singular libraries and on-line documentation files are. These constraints on the local directory layout are necessary to avoid having to hard-code pathnames into the executables, or require that environment variables be set before running the executable. In particular, <strong>you must not move or copy the </strong>Singular<strong> executables to another place, but use soft-links instead.</strong></p>
</li>
</ol>
<p>The following steps are <strong>optional</strong>:</p>
<p> </p>
<ul>
<li>
<h4>Arrange that typing <code>Singular</code> at the shell prompt starts up the installed Singular executable.</h4>
If you  <strong>have superuser privileges</strong>, do:                                                                         
<table border="0">
<tbody>
<tr>
<td><br /></td>
<td class="smallexample"><code>ln -s `pwd`path-to-your-installation-folder/bin/Singular  /usr/local/bin/Singular-x-x-x</code></td>
</tr>
<tr>
<td><br /></td>
<td class="smallexample"><code> ln -s `pwd`path-to-your-installation-folder/bin/ESingular  /usr/local/bin/ESingular-x-x-x </code></td>
</tr>
<tr>
<td><br /></td>
<td class="smallexample"><code> ln -s /usr/local/bin/Singular-x-x-x /usr/local/bin/Singular </code></td>
</tr>
<tr>
<td><br /></td>
<td class="smallexample"><code> ln -s /usr/local/bin/ESingular-x-x-x /usr/local/bin/ESingular </code></td>
</tr>
</tbody>
</table>
Otherwise, append the directory <code>`pwd`path-to-your-installation-folder/bin/</code> to your <code>$PATH</code> environment variable. For the <code>csh</code> (or, <code>tcsh</code>) shell do:                                                                         
<table border="0">
<tbody>
<tr>
<td><br /></td>
<td class="smallexample"><code>set path=(`pwd`path-to-your-installation-folder/bin $path) </code></td>
</tr>
</tbody>
</table>
For the <code>bash</code> (or, <code>ksh</code>) shell do:                                                                         
<table border="0">
<tbody>
<tr>
<td><br /></td>
<td class="smallexample"><code>export PATH=`pwd`path-to-your-installation-folder/bin/:$PATH </code></td>
</tr>
</tbody>
</table>
<p style="text-align: justify;">You might also want to adjust your personal start-up files (<code>~/.cshrc</code> for <code>csh</code>, <code>~/.tcshrc</code> for <code>tcsh</code>, or <code>~/.profile</code> for <code>bash</code>) accordingly, so that the <code>$PATH</code> variable is set automatically each time you login.</p>
<p><strong>IMPORTANT:</strong> <strong>Do never move or copy the file <code>bin/Singular</code> to another place, but use soft-links instead.</strong></p>
</li>
<li>
<h4>If you want to use any of following features of Singular, make sure that the respective programs are installed on your system:</h4>
<table border="1">
<tbody>
<tr>
<td><strong>Feature</strong></td>
<td><strong>Requires</strong></td>
</tr>
<tr>
<td>running <code>ESingular</code>, or <code>Singular</code> within Emacs</td>
<td><a href="http://www.gnu.org/software/emacs/emacs.html">Emacs</a> version 20 or higher, or, <a href="http://www.xemacs.org/">XEmacs</a> version 20.3 or higher (ESingular is only included in the Linux distribution, on other Unix platforms you can download the <a href="/ftp/pub/Math/Singular/src/">Singular emacs lisp files</a> but we give no warranties for specific platforms).</td>
</tr>
<tr>
<td>on-line <code>info</code> help</td>
<td><a href="http://www.texinfo.org/">info</a>, or <a href="http://math-www.uni-paderborn.de/%7Eaxel/tkinfo/">tkinfo</a> texinfo browser programs</td>
</tr>
<tr>
<td>TAB completion and history mechanism of ASCII-terminal interface</td>
<td>shared readline library, i.e. <code>/usr/lib/libreadline.so</code></td>
</tr>
<tr>
<td>visualization of curves and surfaces</td>
<td><a href="http://surf.sourceforge.net/">surf</a> version 0.9 or higher (only available for Linux and Solaris).</td>
</tr>
</tbody>
</table>
Most of these programs can be downloaded from <a href="ftp://jim.mathematik.uni-kl.de/pub/Math/Singular/utils/">ftp://jim.mathematik.uni-kl.de/pub/Math/Singular/utils/</a>.A mirror is at <a href="/ftp/pub/Math/Singular/utils/"> </a></li>
<h4>Customize the on-line help system:</h4>
<p>By default, on-line help is displayed in the first available help 	  browser defined in <code>share/singular/LIB/help.cnf</code>.</p>
<p style="text-align: justify;">This behavior can be customized in several ways using the Singular commands <code>system("--browser",)</code> and <code>system("--allow-net", 1)</code> (or, by starting up Singular 	  with the respective command line options).</p>
<p style="text-align: justify;">In particular, creating the file <code>share/singular/LIB/.singularrc</code> and putting the Singular command <code>system("--allow-net", 1);</code> in it, allows the on-line help system to fetch its <code>html</code> pages from <a href="../../index.html" target="_self">Singular's web site</a> in case its local html pages are not found.</p>
<p>We refer to the   <a href="/old/Manual/latest.1.html">online manual</a> for more details on customizing the on-line help system.</p>
<li style="text-align: justify;">
<h4>Assure that the Singular manual can be  accessed from stand-alone texinfo browser programs such as <code>info</code> or <code>Emacs</code>:</h4>
Add the line                                                                         
<table border="0">
<tbody>
<tr>
<td><br /></td>
<td class="smallexample"><code>* Singular:(singular.hlp).     A system for polynomial computations </code></td>
</tr>
</tbody>
</table>
to your system-wide <code>dir</code> file (usually <code>/usr/info/dir</code> or <code>/usr/local/info/dir</code> and  copy or soft-link the file <code>share/singular/info/singular.hlp</code> to the directory of your <code>dir</code> file. <br />This is <strong>not necessary for the use of the help system from within <code>Singular</code>.</strong> </li>
</ul>
<p> </p>
<h2>Troubleshooting</h2>
<ul>
<li>
<h4>General: Singular can not find its libraries or on-line help</h4>
<ol>
<li style="text-align: justify;"> Make sure that you have read and/or execute permission the files and directories of the Singular distribution. If in doubt, <code>cd</code> to the directory where you unpacked Singular, and do (as root, if necessary):                                                       
<table border="0">
<tbody>
<tr>
<td></td>
<td class="smallexample"><code>chmod -R a+rX .</code></td>
</tr>
</tbody>
</table>
</li>
<li style="text-align: justify;"> Start up Singular, and issue the command <code>system("Singular");</code>. If this does not return the correct and expanded location of the Singular executable, then you found a bug in Singular, which we ask you to report (see below). </li>
<li style="text-align: justify;"> Check whether the directories containing the libraries and on-line help files can be found by Singular: If <code>$bindir</code> denotes the directory where the Singular executable resides, then Singular looks for library files as follows: <br /> (0) the current directory <br /> (1) all dirs of the environment variable SINGULARPATH <br /> (2) <code>$bindir/../share/singular/LIB</code><br /> The on-line <code>info</code> files need to be at 					  <code>$bindir/../share/singular/info</code> and the  <code>html</code> pages at <code>$bindir/../share/singular/html</code>. </li>
</ol>
<p style="text-align: justify;">You can inspect the found library and <code>info</code>/<code>html</code> directories by starting up Singular with the <code>--version</code> option, or by issuing the Singular command <code>system("--version"); .</code></p>
<p style="text-align: justify;"> </p>
</li>
<li style="text-align: justify;">
<h4>For any other troubles:</h4>
Please send an email to <a href="mailto:singular@mathematik.uni-kl.de">singular@mathematik.uni-kl.de</a> and include the header which is displayed by starting up Singular with the <code>-v</code> option, and a description of your machine (issue the command <code>uname -a</code> on your shell) in your report. </li>
</ul>
