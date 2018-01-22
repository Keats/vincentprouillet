+++
title = "Releasing Tera 0.4 and state of my other crates"
path = "releasing-tera-0.4"
description = "Releasing Tera 0.4 and state of my other crates"
date = 2016-12-02
category = "Programming"
tags = ["rust"]
+++


I'm happy to announce [Tera](https://github.com/Keats/tera) 0.4 has been released on [crates.io](https://crates.io/)!

Tera is a template engine based on [Jinja2](http://jinja.pocoo.org/docs/dev/) and the [Django template language](https://docs.djangoproject.com/en/1.10/ref/templates/language/).
I say based as it's not a 1:1 port and has some minor differences with them but is close enough that you should be able
to use the same syntax highlighting.

This version introduces the last big features:

- [Macros](https://github.com/Keats/tera#macros)
- [Multiple level extend, super() and nested blocks](https://github.com/Keats/tera#inheritance)
- [Autoescape](https://github.com/Keats/tera#autoescaping)

It also adds the `filesizeformat` filter thanks to the [humansize crate](https://crates.io/crates/humansize).

Some bits are experimental (named endblock/endmacro, kwargs only) and subject to changes depending on feedback.

There are probably features that others deem essential (please [create an issue](https://github.com/Keats/tera/issues) if you can think of one missing!) but for my own use case it seems feature complete, apart from
the missing `not` operator in conditions. Custom tags would be nice too.

The focus for the next version will be on:

- fixing the inevitable bugs
- add the `not` operator
- improving documentation: a website and more examples
- improving error handling and reporting (maybe [error-chain](https://github.com/brson/error-chain) could help there?)
- optimizations and code cleanup

As you can see, no new big features planned, it will be mostly polishing. 

To ensure Tera is easy to use, I'm thinking of making a static site engine using it but that will depend on how much free time I have.
I'm currently using [Hugo](https://gohugo.io/) for all my sites but the Golang template engine is godawful.

Making the templates compile to Rust functions is still not planned in the near future. 
Check out [Maud](https://maud.lambda.xyz/) or [horrorshow](https://docs.rs/horrorshow/0.6.1/horrorshow/) if you want type-safe HTML.


If you want to help you have 2 options: use it and report bugs and/or look at the issues tagged for the 0.5 milestone on [github](https://github.com/Keats/tera/issues).
The code is fairly clean, commented and has lots of tests so it should be easy to jump in.

Thanks to [SergioBenitez](https://github.com/SergioBenitez) and [yonran](https://github.com/yonran) for the help!

## Other crates

### bcrypt (0.1.2)
This one has an explicit name and is stable. 
I was thinking of extracting the bcrypt specific code from [rust-crypto](https://github.com/DaGenix/rust-crypto) 
but someone already started on that: https://github.com/RustCrypto so I'll just wait.

### dbmigrate (0.2.7)
A CLI tool to general and manage SQL migrations for MySQL, SQLite and Postgres.
It is stable and I don't foresee the API or the migration file format changing so I will probably promote it to 1.0 soon.

### jsonwebtoken (1.1.5)
Strongly typed JWT library. I like the current API but a few more features are planned for 2.0:

- moving to Serde from rustc-serialize
- implementing the missing algorithms

Issues are created on the [github repo](https://github.com/Keats/rust-jwt/issues) so feel free to take one of these before I get to them.

### vat (0.1.0)
Validate EU VAT number and VAT rates for each country. Still not entirely sure why I made that crate but I think I'll try switching it
to [reqwest](https://crates.io/crates/reqwest) when I have time.

I also never got around handling errors from the VIES API since it was always working when I was looking at it and they don't (AFAIK) detail
their error messages anywhere.
