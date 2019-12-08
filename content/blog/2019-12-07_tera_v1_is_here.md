+++
title = "Tera v1 is here!"
description = "After a year of beta, Tera now reaches v1."
+++

Tera is a template engine inspired by [Jinja2](http://jinja.pocoo.org/) and the [Django template language](https://docs.djangoproject.com/en/1.9/topics/templates/).
It is also similar to [Twig](https://twig.symfony.com/) and [Liquid](https://shopify.github.io/liquid/) if you are coming from PHP/Ruby.

The last release, 0.11.20, was released back in November 2018 and the first v1 alpha was released in January 2019. During 2019,
the [Zola](https://www.getzola.org/) static engine has been keeping up with each Tera release and has therefore been tested quite a bit.

If you want to see the TL;DR of all the changes since 0.11.20, you can have a look at the [changelog](https://github.com/Keats/tera/blob/master/CHANGELOG.md#100-2019-12-07).

In most cases, the upgrade to v1 should be painless: unless you are using the error-chain part of Tera errors, it might
even work without any changes.

Before going further, a huge thank you to everyone that [contributed](https://github.com/Keats/tera/graphs/contributors).

Let's look at some of the main changes in a bit more detail now.

## Error handling
Error handling is a [hot topic](https://blog.yoshuawuyts.com/error-handling-survey/) in Rust and has been for quite some time. 
At the time of 0.11, [error-chain](https://github.com/rust-lang-nursery/error-chain) was the recommended approach but pretty much as
soon as I ported all of my code to use it, [failure](https://github.com/rust-lang-nursery/failure/) became the go-to crate. Since then,
some of `failure`'s features made their way into the standard `Error` trait including the one I am using: the [`source`](https://doc.rust-lang.org/std/error/trait.Error.html#method.source) method.

I have pretty much given up on any error handling crate for the time being and just use `std::Error` for everything, including in this new version of Tera.

## Traits for filter, tests and functions
Previously, the type for each was a simple function. It has now been changed to a trait, allowing for each of them to have a context, for example.
Zola, for example, uses structs for some of the functions in order to hold the site data. The trait is automatically implemented for the previous function
type so if you had defined your own they should continue to work, as soon as you change their arguments to be borrowed instead of owned.

## Whitespace management
You can now use the same whitespace management as Jinja2 in Tera:

```jinja2
hello
{{- username -}}
!
```

will render `hellovincent!` if `username` is `vincent`. Please see the [documentation]() for more details.

## Increased rendering performance
The whole rendering code has been rewritten to be more performant.

The bottleneck is still converting the context to JSON since it needs to clone the data. 
This is unlikely to change until we move to a borrowed approach but I do not know how to approach that. If
anyone can figure out a way to solve this issue and still be ergonomic, that would be amazing; please chime in on the [related issue](https://github.com/Keats/tera/issues/469).

How does it compare with other Rust template engines? There is a [benchmark](https://github.com/djc/template-benchmarks-rs) testing just that.
Before showing the results, it is important to understand the difference between the compiled templates and interpreted templates:

- compiled template engines: [askama](https://crates.io/crates/askama), [horrorshow](https://crates.io/crates/horrorshow) and most of the ones
in that benchmark are generating Rust code through macros. The big upsides of this are performance and being able to typecheck your templates.
The big downsides are compilation time and not being able to handle dynamic templates: you cannot render an arbitrary template file.
- interpreted template engines: [Liquid](https://crates.io/crates/liquid), [Handlebars](https://crates.io/crates/handlebars) and Tera are in this category.
They are not going to be as fast or type-safe as compiled one but can run any templates you throw at them.

For example, a static site engine could not work using a compiled template engine as users define their own templates, add arbitrary data and extend other random existing templates.

I've grouped the table output of the templates benchmark (done with [criterion.rs](https://github.com/bheisler/criterion.rs)) depending on the template engine type.
The benchmarks have been ran on a 2018 Macbook Pro.

### Big table benchmark
This is running a for loop with a context being an array of length 100 with each element being another array of length 100.

```bash
Big table/Askama        time:   [624.98 us 643.77 us 663.40 us]
Big table/fomat         time:   [228.47 us 230.94 us 234.08 us]
Big table/Horrorshow    time:   [357.87 us 371.52 us 385.84 us]  
Big table/Markup        time:   [294.43 us 302.90 us 313.99 us] 
Big table/Ructe         time:   [586.48 us 609.61 us 638.02 us]
Big table/Yarte         time:   [286.75 us 311.03 us 334.20 us]
Big table/write         time:   [353.75 us 370.98 us 391.61 us] 

Big table/Tera          time:   [3.5811 ms 3.6997 ms 3.8292 ms] 
Big table/Liquid        time:   [12.890 ms 13.113 ms 13.366 ms] 
Big table/Handlebars    time:   [83.598 ms 86.947 ms 90.391 ms]   
```

As you can see, this is a bad case for interpreted template engine. Tera is the fastest among them but is still up to 10x slower than some compiled engines.
The result from Handlebars are particularly odd: I do not see why it would be 23x slower than Tera.

Considering those results, you should probably use a compiled template engine if you are trying to render some context
requiring a lot of allocations like in that benchmark.

### Teams benchmark
This is rendering a template with a small array of structs as context, a more realistic average workload.

```bash
Teams/Askama            time:   [1.1503 us 1.2120 us 1.2800 us] 
Teams/fomat             time:   [502.20 ns 512.54 ns 524.81 ns] 
Teams/Horrorshow        time:   [466.38 ns 469.09 ns 472.31 ns] 
Teams/Markup            time:   [403.39 ns 408.75 ns 416.11 ns] 
Teams/Ructe             time:   [963.43 ns 976.63 ns 989.98 ns]
Teams/Yarte             time:   [766.24 ns 782.78 ns 800.46 ns]
Teams/write             time:   [756.18 ns 770.13 ns 784.21 ns] 

Teams/Tera              time:   [8.8657 us 8.8969 us 8.9288 us] 
Teams/Liquid            time:   [12.858 us 12.909 us 12.960 us] 
Teams/Handlebars        time:   [70.150 us 75.716 us 81.926 us]
```

Tera is again the fastest interpreted template engine, but the numbers are small enough that any engine will do the job.

## Glob patterns now supported
You can now pass patterns to `Tera::new` like `templates/**/*{html,xml}` to load exactly the type of files you want.

## A `builtins` feature
The number of dependencies started to grow quite a bit as filters and functions were being added. 
From `1.0.0`, a new active-by-default feature named `builtins` has been introduced. If you disable it, Tera will only
depend on the crates needed for parsing and rendering and all the filters and functions that were depending on those
dependencies will not be present anymore.

## Known issue

Due to a bug in [pest](https://pest.rs/), the parser generator used by Tera, some template parsing might timeout. There 
are more details in the [issue](https://github.com/Keats/tera/issues/436) but since the pest contributors are working on v3, 
it doesn't seem worth it to hold on releasing Tera 1.0 for an unknown amount of time until its release.
This issue was found while fuzzing but I've been running into <https://github.com/rust-lang/rust/issues/66140> when trying
to run the fuzzer again on OSX.
