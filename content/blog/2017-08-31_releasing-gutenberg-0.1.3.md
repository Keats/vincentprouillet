+++
title = "Gutenberg 0.1.3: themes are in"
description = "Gutenberg 0.1.3 is out with theme support"
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

You can download built binaries from the [Github releases page](https://github.com/Keats/gutenberg/releases).

## What's new

The highlight of this release is, as you might have guessed from the title of the post, themes.

Themes are a staple of static site engines: you can use one to get started with your site and only tweak little bits.

As a proof of concept I have ported a famous theme from Jekyll: [hyde](https://github.com/Keats/hyde).

Since [Tera](https://github.com/Keats/tera), the template engine used in Gutenberg,
supports multiple levels of [inheritance](https://tera.netlify.com/docs/templates/#inheritance), using a theme is almost seamless.
For example, if you want to change the about part of the sidebar of Hyde, it is as easy as adding a `index.html` in your
`templates` folder with the following:

```jinja2
{% extends "hyde/templates/index.html" %}

{% block sidebar_about %}
    Something else
    You can of course render the theme block
    first by calling {{/* super() */}} if wanted.
{% endblock sidebar_about %}
```

The architecture chosen for themes is the same as [Hugo](https://gohugo.io/): you have a themes folder in which you download your
themes (via `git clone` or copy/paste) and tell Gutenberg which one to load by adding a `theme = "theme_name"` line in your `config.toml`.

This is the first pass at themes so there are probably features missing or bugs laying around but it's ready to be used!

## What's next

The main focus now will be to get a site up and running for Gutenberg and to put it in various package managers.
If someone reading this is on Mac and has some time to spare, I would love to get it on Homebrew but I don't have access to one.

Lastly, the [i18n RFC](https://github.com/Keats/gutenberg/pull/111) is open. If you are interested
in multi-lingual sites, please have a look and comment!
