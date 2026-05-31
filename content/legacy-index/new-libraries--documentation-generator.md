---
title: "Documentation Generator"
url: "/index.php/new-libraries/documentation-generator.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/new-libraries/documentation-generator.html"
migration_status: "migrated from local legacy copy"
---

<p><p> 
The typesetting language in which the Singular
doumentation is written is <code>texinfo</code>.
The info string of a library included in the Singular 
distribution will be parsed and automatically translated to the
<code>texinfo</code> format. The same applies to the help string of each
procedure listed in the <code>PROCEDURE:</code> section of the info string.
Based on various tools, <code>info</code>, <code>dvi</code>, <code>ps</code>,
and <code>html</code> versions of the <code>texinfo</code> documentation are
generated.
To see, how your library will show in the documentation, just upload the file
here.
</p>
<form data-legacy-action="/cgi-bin/lib2doc" action="#" method="post"
enctype="multipart/form-data">
<label for="file">Filename:</label>
<input type="file" name="file" id="file" /> 
<br />
<input type="submit" name="submit" value="Submit" />
</form>
<br>
<p>
Note that the process of building the documentation may take some time.<br>
When building the documentation in its final form, the example of each procedure
listed in the <code>PROCEDURE:</code> section of the info string of the library
will be computed and its output will be included in the documentation. 
<br>
Note that
the documentation generator presented here does <b>NOT</b> run your examples.
If you want to generate your documentation including your examples,
you can download the following tool and use it on your own computer.
<ol style="list-style-type:none;">
<li style="float:left;">
<a class="wanted" href="/old/Manual/latest/sing_60.htm#SEC97">lib2doc</a></li>
</ol>
</p>
</p>
