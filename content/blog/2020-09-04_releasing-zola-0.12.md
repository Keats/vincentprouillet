+++
title = "Releasing Zola 0.12"
description = "A brand new zola serve is here"
+++

A brand new [Zola](https://www.getzola.org/) version is out! Zola is a flexible static site engine.

This new version doesn't contain a lot of new changes, summer and global pandemic not being the most productive
environment - at least for me.

The main improvement of this release is completely changing how `zola serve`. Before 0.12, it used to write the whole site 
to disk and on changes try to figure out what changed and the minimum things we need to rebuild. It sounds good 
in theory but in practice was very buggy as Zola is pretty flexible: you can access the site content from any template 
(for example there could be a box with the most recent 5 articles on every page). And, well, it was trying to be too smart.

With 0.12, the rendered content will be stored in a HashMap in memory instead. Only the HTML content is stored in that
HashMap, the assets stay on disk. When anything changes in a template or in a Markdown file, we rebuild *everything*. 
This is slower than the previous mechanism but has the advantage of always producing the correct output.
The downside is that it is slower: making a change to a Markdown file on the Zola documentation used to do a rebuild
in 8ms and would now take 200ms. Still fast enough for the majority of cases. If you have a huge site and the rebuild
is now too slow, you can use `zola serve --fast` that rebuilds only the section or page that changed and gets you back to 
the 8ms rebuild time.
Hopefully this approach works better for most people!

There are a few other changes that you can see in the [CHANGELOG](https://github.com/getzola/zola/blob/master/CHANGELOG.md#0120-2020-09-04).

The next version will be focused on finishing the multi-language story with a full i18n integration based on
 [Fluent](https://www.projectfluent.org/) as well as adding some options to he Markdown rendering, such as smart
 punctuation.
