+++
title = "Releasing Gutenberg 0.1.0"
path = "releasing-gutenberg-0.1.0"
description = "Releasing Gutenberg 0.1.0: what's in it and what's coming"
date = 2017-07-14
category = "Programming"
tags = ["rust"]
+++

[Gutenberg](https://github.com/Keats/gutenberg) is a powerful static site engine inspired by [Hugo](https://gohugo.io/) but simpler to use.
You can build pretty much any kind of static site with it using markdown:

- a basic blog
- a landing site
- a knowledge base
- a gitbook
- a documentation site
- all of the above combined

You can download built binaries from the [Github releases page](https://github.com/Keats/gutenberg/releases). If you were using Gutenberg
through Cargo, I will not upload new versions to crates.io for three reasons:

- [package for binary crates don't use the `Cargo.lock`](https://github.com/rust-lang/cargo/issues/2263) which means a dependency having breaking changes
without respecting SemVer will cause the crate to compile but [fail at runtime](https://github.com/Keats/gutenberg/issues/92) in some cases
- I moved to using a Cargo workspace with many small crates to improve iteration speed
- with Sass, building Gutenberg has become more involved and it is easier to let user install the already built binary

As mentioned in [my article introducing Gutenberg](./post/announcing-gutenberg.md), 
my main issue with Hugo is the extremely poor — and I'm being kind here — template engine it is using.
This was solved in the first release of Gutenberg by using a template engine similar to Jinja2 I wrote: [Tera](https://github.com/Keats/tera).

Another annoying thing was that, since I was using [Sass](http://sass-lang.com/) to write CSS, each static site had to set up
Sass compilation, usually with node/yarn/gulp.

With Gutenberg 0.1.0, this is solved as it ships with a static version of libsass, the C++ Sass compiler and allows 
commits like [this one](https://gitlab.com/Keats/vincent.is/commit/2a05cdad4cfd9dac103c9907488ad71518886440).

Let's have a look at the current set of features - it's pretty packed for a 0.1.0:

- **live reload**: when anything changes, Gutenberg will do the minimum work required and will live reload assets (js/css/images/...) if possible
- **syntax highlighting** built-in via [syntect](https://github.com/trishume/syntect)
- **pagination**
- **easy internal linking**: they look like `[my article](./post/blabla.md)`
- **automatic table of contents**
- **automatic insertion of anchors on titles**: same as [READMEs on Github](https://github.com/Keats/gutenberg)
- **shortcodes**: when you want to insert some HTML in a page but don't want to copy the HTML everywhere. For example
`{{ youtube(id="dQw4w9WgXcQ") }}` is a built-in shortcode and will insert the YouTube video for that id.
- **Sass compilation**
- **RSS feed** generation when requested
- **Tags and categories** generation when requested
- **co-location of assets and content**: when an article has some images and you want to keep them in the same folder

## What's next
The current features are pretty much what I wanted to have when I started Gutenberg but that doesn't mean there isn't anything left to do!

### i18n
The discussion started on [github](https://github.com/Keats/gutenberg/issues/13) but as it isn't a feature I need, I would
rather have someone else doing it, once there is consensus on the implementation

### Alternative rendering backends
Right now, only markdown is supported. While I definitely don't want to have too many backend, [Asciidoc](http://asciidoctor.org/docs/what-is-asciidoc/)
is one I was interested in and [antoyo](https://github.com/Keats/gutenberg/issues/32) started working on a asciidoc implementation so
it should be coming eventually!

### Theme support
[An issue](https://github.com/Keats/gutenberg/issues/91) was opened on Gutenberg to support themes. 
While the idea in the issue is IMO too complex, I would like to have some theme support baked in `gutenberg`, 
unless the `git clone a-template-repo` approach is simpler.

### Deploying
A subcommand to upload/push the generated site to Github Pages/server/service could be nice. Maybe this can be resolved
with documentation instead though.

### A documentation site
Now that things are a bit more stable in Gutenberg, I will start working on a documentation site as Gutenberg Readme is currently not 
nearly enough. I've already started one for [Tera](https://github.com/Keats/tera/tree/master/docs) and am mostly waiting for design inspiration 
before publishing it.

### Packaging
Lastly, I think it's time to put Gutenberg in [packages managers](https://github.com/Keats/gutenberg/issues/12). I will probably
put it on [AUR](https://aur.archlinux.org/) if no one beats me to it but I will need help for the other package managers.

## Conclusion
As always I welcome any feedback. If you are using Gutenberg, please reply on [this issue](https://github.com/Keats/gutenberg/issues/100) so I
can update the list in the README.

Joyeux 14 Juillet!
