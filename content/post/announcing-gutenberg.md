+++
title = "Announcing Gutenberg, a static site engine"
path = "announcing-gutenberg"
description = "Introducing Gutenberg, an opinionated static site engine written in Rust"
date = 2017-03-25
+++

*Why would we possibly want another static site engine?* I already hear some say.
That's a very valid question!

I currently have 6 static sites live:

- [wearewizards.io](https://wearewizards.io)
- [blog.wearewizards.io](https://blog.wearewizards.io)
- [vincent.is](https://vincent.is)
- [proppy.io](https://proppy.io)
- [proppy.io/blog](https://proppy.io/blog)
- [pixelspa.com](https://pixelspa.com)

Those are all using [Hugo](https://gohugo.io/), except the blog you're reading
that moved to Gutenberg a couple of days ago.

Hugo in itself is pretty great: I switched from Pelican for the speed and the stand-alone binary and
stayed for the instant live reload. The huge pain point for me with Hugo is the Go template 
engine: I find it so bad that it turns a great experience into a, well, sad experience.

When I first looked at Rust a couple of years ago, I thought that a static site engine could be a nice first
program to write to learn the language. Sadly, I didn't find a template engine I liked at the time which
prompted me to write my own, [Tera](https://github.com/Keats/tera).

Now that Tera is getting more mature and my frustration with Go templates grows, I started
working again on the static site engine a few weeks ago and it got to a point where it's usable.

It's called **Gutenberg** and is now available in a 0.0.2 version on crates.io and [Github](https://github.com/Keats/gutenberg/releases).
It seems AppVeyor is running into some issue with curl so I haven't been able to test it on Windows yet but
it should work on Linux and OSX. Binaries are built using the very nice [trust](https://github.com/japaric/trust) project.

## The features
Gutenberg is opinionated (only TOML for configuration, only Tera for templates, only CommonMark for content) but is flexible 
enough to let you build all kinds of sites, from landing pages to knowledge bases, not only blogs. 

Features in no particular order are:

- CommonMark for content
- Categories and Tags automatic page creation (easy to disable)
- Automatic RSS feed (easy to disable)
- Built-in server with fast live reload (a bit buggy currently)
- Supports having assets next to the content: no need to put everything in a `static` folder
- Explicit sections that can have their own page and have access to potential subsections: this allows making pages like [https://easyengine.io/tutorials/](https://easyengine.io/tutorials/)
which are a big table of contents over several sections
- Good template engine: I'm a bit biased there
- Simple to use: no surprises, everything is explicit except from the default templates used

More information is available on the [README](https://github.com/Keats/gutenberg) and better documentation will come
once the tool is in a more stable shape.

## What's next
As the 0.0.2 version number indicates, Gutenberg is still a work-in-progress. Despite
that, it fills almost all my static engine needs. There are a few things that will need
to be done before being ready for a 0.1 though:

- Find and fix bugs, add tests and benchmarks
- Make it faster: parallelize if possible
- Pagination: still debating the best way to set up that up in a [Github issue](https://github.com/Keats/gutenberg/issues/7)
- Add an equivalent to [Hugo shortcodes](https://gohugo.io/extras/shortcodes#shortcodes-with-markdown): they make it easy to embed
some HTML in your markdown without repeating HTML all the time, e.g. a youtube video could be added to a page like so `{{ youtube(id=87238) }}`
and the renderer will insert whatever template we defined for the `youtube` shortcode.

And for after the 0.1 release:

- Built-in Jupyter renderer would be nice
- Proper documentation site

The current blocker to parallelization is that [syntect](https://github.com/trishume/syntect), the
great library I'm using for syntax highlighting is not thread-safe. There is an [issue](https://github.com/trishume/syntect/issues/20) open
but I haven't had the time or energy to look/fix that yet. 
It should be fairly straightforward to add Rayon once it's fixed, if the benchmarks show a significant difference.

## How does it look in practice
You can have a look at the source of [this site](https://gitlab.com/Keats/vincent.is).

This site is very simple: a blog and a couple of other pages but it should give some ideas.


## Enjoy!
Obviously, any feedback is welcome!
While the general design and current features are unlikely to change, I'd be happy to cover
more use-cases if possible.

Check it out on Github: [Gutenberg](https://github.com/Keats/gutenberg)
