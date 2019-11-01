+++
title = "Gutenberg is out, Zola 0.5.0 is in"
description = "Gutenberg changes name to Zola and gets a big release to celebrate"
+++

Stop the presses! This is an important update for Gutenberg users - please read on
if you are one of them.

[Gutenberg/Zola](https://www.getzola.org) is a powerful static site generator (SSG)
inspired by [Hugo](https://gohugo.io/) but simpler to use. One of its goals is to try
to do as much as possible at built time: anchors, search, Sass, table of contents, syntax highlighting and more.
It is highly flexible and allows you to do any kind of sites:

- a blog like the one you are reading right now
- a landing page
- a knowledge base
- a gitbook: see the [book theme](https://github.com/getzola/book)
- a documentation site for your library like the one for [Zola](https://www.getzola.org)

You can find an up-to-date comparison of Zola with other SSG [on the README](https://github.com/getzola/zola#comparisons-with-other-static-site-generators).

## A bit of history and changing name to Zola

The first commit on Gutenberg was done in May 2015 after the first stable version of Rust was released.
The goal for that project was for a friend and I to learn Rust and a SSG was a pretty good fit for that.
Since it was a learning project, we didn't really care about name conflict: we expected to be the only
users.

> If you are looking at the date of the first commit in the GitHub repo, you will see 2016.
> When I started Gutenberg, there was no templates library I liked at the time so I spent some time
> building [Tera](https://tera.netlify.com/) and deleted the original repo as it was outdated by then.

Gutenberg grew more than anticipated and every time it got posted somewhere, half of the comments were pointing out
the name was not original. Most of the name conflicts were with [Project Gutenberg](https://www.gutenberg.org/) or
some [CSS](https://github.com/BafS/Gutenberg) [frameworks](https://github.com/matejlatin/Gutenberg). I fully agree
with the people saying it isn't original. By that time, Gutenberg was already in many package managers and on [Netlify](https://www.netlify.com/):
changing name was a bit problematic.

More recently though, a small project called [WordPress](https://wordpress.org/) started advertising their new editor, [gutenberg](https://wordpress.org/gutenberg/).
Being WordPress it will simply eclipse every single search for my Gutenberg and any others: I
already had trouble finding one of the CSS framework named Gutenberg while writing this post since all results were about the WordPress editor, which isn't
even released yet at that time.
Another point against the Gutenberg name is that my SO works for a WordPress agency: I hear about it all the time.

I opened [an issue](https://github.com/Keats/gutenberg/issues/377) to rename the project and ended up choosing `zola`.
Émile Zola is a very famous French writer - at least in France -, mainly for his [J'accuse](https://en.wikipedia.org/wiki/J%27Accuse%E2%80%A6!) letter. His
writing style doesn't appeal to everyone but his most famous books are [L'Assomoir](https://en.wikipedia.org/wiki/L%27Assommoir)
and [Germinal](https://en.wikipedia.org/wiki/Germinal_(novel)) if you want to read one.
The name `zola` itself it very short, easy to pronounce and I couldn't find any open-source projects with that name other than an [inactive organization](https://github.com/ZolaApp).

As the name is brand new, `zola` will not be available immediately in all package managers and not natively on Netlify as I will talk about a bit more below.

## Changelog

0.5.0 took longer than expected but is packed with bug fixes, new features and improvements. Part of the reason this
version has been so slow to be released is that I wanted to have Netlify support on release since all my sites
are using it. However, since my [PR](https://github.com/netlify/binrc/pull/19) to add it is not really being looked at, I decided
to stop waiting and release it now.
If you are using the current Gutenberg Netlify support, you can either stay on 0.4.1 or 0.4.2 or download the `zola` binary manually like
mentioned in [the documentation](https://www.getzola.org/documentation/deployment/netlify/#automatic-deploys).

With that said, let's have a look at the headlines.

### Performance

A big focus for this release was performance. While fast enough for medium sites (< 500 pages), it was slowing down
and consuming lots of memory when dealing with bigger sites and I knew some of the features
I wanted to add would make the problem even worse. Thanks to the help of [@Freaky](https://github.com/Freaky), we were
able to improve speed dramatically (4-10x in general) while lowering the memory usage, you can see the evolution in [the issue](https://github.com/Keats/gutenberg/issues/420).

To give an idea of the speed, there are some benchmarks in the repository but you will need to generate them first: `python gen.py` in `components/site/benches`.
This will generate several sites of various sizes and setup but I'll use `huge-blog` for illustration.
It is a blog with 10000 pages, paginated by 5 with several taxonomies (one of them having a RSS feed).
Each page contains shortcode, syntax highlighting and, although not used in the templates in this cases, a table of contents.
Here are the results on my 4.5 years old laptop:

![Building a huge blog with Zola](huge-blog.png "Building a huge blog with Zola")

Not too bad. I am pretty sure we can optimize the speed further but I won't spend more time on it myself, I would rather
try to lower the memory usage right now, which is still way too high: I believe it used around 3GB during the screenshot above, which is insanely
high.

Most of the time spent is now serializing the data to JSON for usage in [Tera](https://tera.netlify.com/).
There is an issue for [writing Tera's own serde format](https://github.com/Keats/tera/issues/340) but I am not sure how it would look like
despite the help of [@dtolnay](https://github.com/dtolnay/). If you have ideas on how to improve on that side, I am very happy to hear them!

### Ancestry

Each page and section will now have all their parent sections paths in an `ancestors` property.
This allows you to easily do breadcrumbs as well as just being able to access the parent section, which wasn't possible before.

### Loading CSV/TOML/JSON data
A new Tera function aptly named `load_data` has been added.
It can load data from both a local file or a remote URL and convert it to Tera values for usage in templates. As such, this is equivalent
to the feature some SSG call data files but also to `getJSON` and `getCSV` in Hugo. Thanks to [serde](https://github.com/serde-rs/serde)
for the super simple and powerful serializations!

### Date from filename
If a page with a `YYYY-MM-DD{-,_}` format, this date will now automatically be set as the page date, unless
overwritten in the front-matter, and the text after `{-,_}` will be the slug.
For now, a slug is still required but it seems likely that I will allow a file named `YYYY-MM-DD` in the future
as, in some cases like meeting minutes, pages do not always have a slug different from the date.

### Page templates
Previously, if you had a site that was for example a landing page + blog, it is likely you would need
to specify the template to use to render a blog post on every page. A bit tedious and not very DRY.
From 0.5.0, you can set the `page_template` attribute in a section and every pages below that section including subsections pages will use it.
Sub-sections can override it by setting their own `page_template` and pages by setting `template`.

### Transparent sections

A commonly requested feature was the YYYY/MM/DD url scheme. I do not think it is a good
one and explained [why](https://github.com/Keats/gutenberg/issues/408#issuecomment-429025773) previously.
However, someone had [a very good idea](https://github.com/Keats/gutenberg/issues/408): transparent section.

By setting `transparent` to `true` in a section front-matter, all its pages will be passed to the parent section and so on,
until a section isn't `transparent`.

In practice, this allows you to do the YYYY/MM/DD scheme easily:

```bash
.
├── 2018
│   ├── 10
│   │   ├── 10
│   │   │   ├── 2018-10-10_zola-release.md
│   │   │   └── _index.md
│   │   └── _index.md
│   └── _index.md
└── _index.md
```

It is definitely more verbose than what Jekyll or Hugo (setting `/:year/:month/:title/` in the config) but is also more powerful.
As far as I'm aware, you have no way of selecting the intermediate templates in alternatives or they are sometimes not rendered at all.

For example, if I'm on [https://intellij-rust.github.io/2018/11/07/changelog-86.html](https://intellij-rust.github.io/2018/11/07/changelog-86.html) and try
to want to see all the posts in 2018 (https://intellij-rust.github.io/2018/), I get a 404. I would be very surprised
if Jekyll doesn't handle that but it looks optional at least.

Another advantage is that it isn't limited to the data in the front-matter: you can organise it however you want. Want to have a blog, prefix all the blog posts
by `/blog/` but paginate it in the homepage? Create a `blog` section, mark it as `transparent`, paginate the index and you're done.

### Bug fixes
Many bugs were fixed, including the big Tera one with macros that was shipped in 0.4.2.
Refer to the [changelog](https://github.com/getzola/zola/blob/next/CHANGELOG.md) for a full list.

## Roadmap

The first step now will be to get a [Discourse](https://www.discourse.org/) up and running to have a better forum than GitHub and move all discussions/feature requests to it in
order to keep the GitHub issues for actual bugs.
The major part of my effort will go towards [Tera 1.0.0](https://github.com/Keats/tera/issues/331), with a beta version shipping in a future version
of Zola soonish.

I know I keep saying that on every release post but the focus for the next version will be on [i18n support](https://github.com/getzola/zola/pull/111) since some
of the cleanup needed is now done. The RFC will need to be updated to take into account the new features in the last year once a Discourse instance is live.

Lastly, if you are looking for a place to get started with Rust, Zola is great for that!
The codebase is relatively small and separated in a few sub-crates making it easy to contribute: you can modify the bit you want to change in the sub-crate,
compile/test only that one and once you're satisfied check where is the compiler complaining in the rest of the project. I will also help personally anyone wanting to start working on an issue.
This offer is valid for any of [my projects](https://github.com/Keats) and if I don't respond for a while, don't hesitate to ping me.
