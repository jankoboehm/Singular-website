---
title: "Release of SINGULAR 3-1-1"
url: "/index.php/news/release-of-singular-311.html"
description: "Singular - an open source computer algebra system"
legacy_source: "index.php/news/release-of-singular-311.html"
migration_status: "migrated from local legacy copy"
---

<p>Dear <strong>Singular</strong> users,<br /> <br /> we would like to announce the new <strong>Singular</strong> version,<br /> <strong>Singular 3.1.1</strong>.<br /> <br /> Here is a summary of what's new. You may find more information at<br /> <a href="/old/Manual/3-1-1/sing_1610.htm" target="_blank">http://www.singular.uni-kl.de/Manual/3-1-1/sing_1610.htm</a>.<br /> <br /> The new version is already available at <a href="../../index.html" target="_blank">http://www.singular.uni-kl.de</a> for most Unix platforms, and for Windows. The Os X version will follow soon.<br /> <br /></p>
<h3>NEWS in Singular 3.1.1</h3>
<p>* new option qringNF, see option.<br /> * new system command system("cpu"), see system.<br /> <br /> New <strong>Singular</strong> functions<br /> * new command: farey: lifting to Q (see farey)<br /> * new command: monomial (see monomial)<br /> * command extended: liftstd also computes syzygies. (see liftstd)<br /> * command extended: minor has more options. (see minor)<br /> * command extended: opposite (see opposite)<br /> <br /> Internal Changes<br /> * new minor code<br /> * removed EXTGCD (use extgcd)<br /> * moved mp_set_memory_functions-call from kernel/mminit.cc to<br /> tesths.cc:main (in order not to call it for libsingular)<br /> <br /> New <strong>Singular</strong> libraries<br /> * new library: normaliz.lib (see normaliz_lib: Interface to<br /> Normaliz 2.2)<br /> <br /> Changed <strong>Singular</strong> libraries<br /> * homolog.lib ( homolog_lib): canonMap<br /> * dmod.lib ( dmod_lib): operatorModulo</p>
