+++
title = "This month in my Rust projects"
url = "working-on-rust-projects-in-april-2017"
description = "Progress of my Rust projects in April 2017"
date = "2017-04-23"
category = "Programming"
tags = ["rust"]
+++

I have just released v2 of [jsonwebtoken](https://github.com/Keats/jsonwebtoken) and 
thought a blog post would be a good way to talk about the progress of jsonwebtoken, Tera and Gutenberg this month.

## jsonwebtoken
Version 2 is almost a full rewrite, but trying to keep the UX as good as possible.

The following improvements have been made:

- use `serde` instead of `rustc_serialize`: no brainer as `serde` is now usable on stable and reached 1.0.0
- RSA signing and verification
- Validation

Validation is the main thing that was missing from version 1 and brings `jsonwebtoken` to almost parity with libraries
in other languages. It is detailed [in the README](https://github.com/Keats/jsonwebtoken#validation).

As an aside, the signature of `decode` is an example of why I would like to have default arguments in functions.
The signature is:

```rust
pub fn decode<T: DeserializeOwned>(
    token: &str, 
    key: &[u8], 
    validation: &Validation
) -> Result<TokenData<T>>
```
But I expect `Validation` to be the default most of the time so the ideal signature would be something like:

```rust
pub fn decode<T: DeserializeOwned>(
    token: &str, 
    key: &[u8], 
    validation = &Validation::default() // or whatever the syntax would be
) -> Result<TokenData<T>>
```

And using `decode` would be cleaner (at least for me):

```rust
decode(&token, "key", &Validation::default());
// VS
decode(&token, "key");
```

There is a [pre RFC](https://internals.rust-lang.org/t/pre-rfc-named-arguments/3831/234) but not much progress has
been made recently.

Thanks a lot to [Mike Engel](https://github.com/mike-engel) for all the feedback!

## Tera

> [Tera](https://github.com/Keats/tera) is a template engine based on Jinja2/Django templates

Tera has gone through 2 versions in April: 0.9.0 and now 0.10. 

0.9 fixed a major bug on Windows and 0.10 updated `serde` to 1.0, no major changes otherwise: Tera is pretty stable now.

## Gutenberg

> [Gutenberg](https://github.com/Keats/gutenberg) is a static site engine

Lots of progress this month on Gutenberg! 

A short list of the biggest new features:

- Shortcodes inspired by [Hugo](https://gohugo.io/extras/shortcodes/)
- Relative links to your own content: `[my last article](./posts/an-article.md)`
- Anchors for titles with an option to insert some HTML to allow behaviour similar to the Github READMEs
- Works on Windows!

Next up is [sorting by weight/order](https://github.com/Keats/gutenberg/issues/14) and finishing up
[pagination](https://github.com/Keats/gutenberg/issues/7).

Once those features are in, I will probably spend some time making an actual documentation site to ensure it works for sites 
more complex than this blog.

If anyone is knowledgeable about [Live Reload](http://livereload.com/), I'd like some help tracking down [this issue](https://github.com/Keats/gutenberg/issues/10).

Solving [this issue in Syntect](https://github.com/trishume/syntect/issues/20) would also help but I don't have time/motivation for it myself right now.

Otherwise, Gutenberg mostly needs feedback and even feature request for things I didn't consider yet.

