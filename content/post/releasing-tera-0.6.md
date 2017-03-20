+++
title = "Releasing Tera 0.6 and thoughts on a validation crate"
url = "releasing-tera-0.6"
description = "Releasing Tera 0.6 and thoughts on a validation crate"
date = "2016-12-26"
category = "Programming"
tags = ["rust"]
+++

[Tera](https://github.com/Keats/tera) 0.6 has been released on [crates.io](https://crates.io/)!

I will let the changelog speaks for itself:


#### BREAKING CHANGES
- `not` is now a Tera keyword

#### Others
- Added `#![deny(missing_docs)]` to the crate
- Added `Tera::one_off` to parse and render a single template
- Added `not` operator in conditions to mean falsiness (equivalent to `!` in Rust)
- Remove specific error message when using `||` or `&&`
- Improved performances for parsing and rendering (~5-20%)
- Added `precision` arg to `round` filter
- Added `date` filter to format a timestamp to a date(time) string


Nothing too exciting in that release except finally handling `not` in expressions.

I don't foresee big changes in the API coming soon anymore as we approach feature completeness from my point of view.

The 2 main things still lacking are:

- **custom tags**: we would need to expose the renderer or the AST somehow
- **i18n**: no mature i18n libraries in Rust as far as I'm aware

I am not using any of those in my own projects but anyone wanting to discuss them is welcome.


## Validation crate
I've been working through the `requirements.txt` of [Proppy](https://proppy.io) to decide what crate to work on in Rust.

The next one will probably be a crate similar to the [marshmallow](https://marshmallow.readthedocs.io/en/latest/index.html) library.
Since Serde can handle the serialization/deserialization aspect already, it will focus only on actual validation with an API looking like
that:

```rust
#[derive(Debug, Deserialize, Validate)]
struct SignupData {
    #[validate(email)]
    email: String,
    #[validate(url)]
    site: String,
    #[validate(custom="validate_unique_username")]
    #[validate(length(min=2))]
    username: String,
    #[validate(length(min=8, max=255), custom="validate_common_passwords")]
    password: String,
}
```

A non-goal of that crate will be error messages as it's always a pain to handle. Errors will be referenced by a keyword
and it will be up to the frontend or the backend to write error messages in the correct format for that application.

The first step is figuring out how macros 1.1 work but once it's done, it seems like it will be a fairly small crate.

See you in 2017!
