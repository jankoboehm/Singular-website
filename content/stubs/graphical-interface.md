---
title: "Jupyter Notebook Interface"
url: "/index.php/graphical-interface.html"
description: "Using Singular from Jupyter notebooks."
legacy_source: "index.php/graphical-interface.html"
migration_status: "migrated from local legacy copy"
---

<h1 id="usingsingularinjupyter">Using Singular in Jupyter</h1>
<p>It is possible to use <a href="http://www.jupyter.org" target="_blank">Jupyter</a> as front-end for Singular. <span style="font-size: 12.16px;">Jupyter </span><span style="font-size: 12.16px;">notebooks provide a browser based graphical interface to Singular.</span></p>
<p><img src="../Images/screenshot_jupyter.jpg" border="0" alt="Screenshot Jupyter" title="Screenshot Jupyter" width="627" height="400" style="border: 0px;" /></p>
<h2 id="installation">Installation</h2>
<p>These installation instructions are for Ubuntu Linux 16.04 (Xenial).</p>
<p><span style="font-size: 12.16px;">As an alternative to installing Jupyter and Singular on your System, you </span><span style="font-size: 12.16px;">can also use it online in <a href="http://cloud.sagemath.com" target="_blank">SageMathCloud</a></span><span style="font-size: 12.16px;">.</span></p>
<h3 id="pythonandjupyter">Python and Jupyter</h3>
<p>If you want to run the Jupyter notebook locally on your computer, you need a recent version of Python 3 and Jupyter installed.</p>
<p>To install Python3 run</p>
<pre><code>apt-get install python3-pip
</code></pre>
<p>We recommend using Python3, but you can also use Python2.</p>
<p>To install Jupyter using pip, run</p>
<pre><code>pip3 install jupyter
</code></pre>
<h3 id="singular">Singular</h3>
<p>You need a recent (&gt;= 4.1.0) version of Singular.</p>
<p>Installation instructions for Singular can be found <a href="https://github.com/Singular/Sources/wiki/Building-Singular-from-source" target="_blank">here</a>.</p>
<p>It is important to have a correctly installed Singular and to have a <code>Singular</code> executable in your <code>PATH</code>.</p>
<p>Normally, running</p>
<pre><code>make install
</code></pre>
<p>from the Singular installation directory after configuring wth default options and compiling Singular will ensure that the <code>Singular</code> executable is present in a directory (/usr/local/bin) that is in your <code>PATH</code>.</p>
<p>If you are compiling and installing Singular with custom options, make sure both the <code>Singular</code> executable and <code>libSingular</code> are available in your system executables and include/library paths.</p>
<h3 id="jupytersingularkernel">Jupyter Singular kernel</h3>
<p>The Jupyter kernel for Singular consists of two packages. You can install them via pip using</p>
<pre><code>pip3 install PySingular
pip3 install jupyter_kernel_singular
</code></pre>
<p>While not recommended, it is possible to use the Jupyter kernel for Singular without the <code>PySingular</code> package. If you have problems to install it, do not worry, it will be fine.</p>
<h3 id="imagesusingsurf">Images using surf</h3>
<p>It is possible to display images created by surf in the Jupyter notebooks. For this, you need to download, compile, and install the <a href="ftp://www.mathematik.uni-kl.de/pub/Math/Singular/misc/surf-1.0.6-gcc6.tar.gz">latest version of surf</a>.</p>
<p>Please configure and compile it via</p>
<pre><code>./configure --disable-gui
make
make install
</code></pre>
<p>For pictures to be displayed in the Notebook, you need to load a specialized Singular library, and a specialized plot command. You can find an example of how to use it <a href="https://github.com/sebasguts/jupyter-singular/blob/master/Demo.ipynb" target="_blank">here</a>.</p>
<h2 id="usageandexamples">Usage and examples</h2>
<p>After installing the kernel, you can start a Jupyter Notebook server by running</p>
<pre><code>jupyter notebook
</code></pre>
<p>Now you can create a new notebook with Singular code.</p>
<p>Example notebooks can be found here:</p>
<ul>
<li><a href="https://github.com/sebasguts/jupyter-singular/blob/master/Demo.ipynb" target="_blank"><strong>Demo.ipynb</strong></a></li>
<li><a href="https://github.com/sebasguts/jupyter-singular/blob/master/WidgetTestSingular.ipynb" target="_blank"><strong>WidgetTestSingular.ipynb</strong></a></li>
<li><a href="https://github.com/jifarran/brnoeth/blob/master/brnoeth.ipynb" target="_blank"><strong>brnoeth.ipynb</strong></a></li>
</ul>
