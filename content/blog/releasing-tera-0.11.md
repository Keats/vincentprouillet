+++
title = "Tera 0.11 is released"
description = "Tera 0.11 is out with whitespace handling and more"
date = 2018-01-22
category = "Programming"
tags = ["rust"]
+++

The work on this version started in September 2017 so I'm pretty happy to finally have this published.

The [changelog](https://github.com/Keats/tera/blob/master/CHANGELOG.md) is pretty thorough but the main
highlights are:

- whitespace handling
- default arguments for macros
- tests, global functions calls and macro calls are now expressions and can be combined like so: `if x is divisibleby(2) and x > 10`

Quite a few of the changelog items were written by contributors and I hope this trend continues: thanks
to [@upsuper](https://github.com/upsuper), [@Alex-PK](https://github.com/Alex-PK), [@jturner314](https://github.com/jturner314),
[@hoggetaylor](https://github.com/hoggetaylor) and [@alex](https://github.com/alex) for that.


## What's next

I am satisfied with the current feature set of Tera and am not planning to do significant changes
to the template language itself, which brings us to a 1.0!

I expect most of the changes until then to happen to the Rust side:

- ergonomics improvement: I'm pretty happy with it so would welcome other viewpoints
- template rendering performance improvement (reducing the number `clone()`, etc)
- look into the benefits of [failure](https://github.com/withoutboats/failure)
and whether it's worth moving from [error-chain](https://github.com/rust-lang-nursery/error-chain) (no at a first glance)
- try to get something like [streamable templates](https://github.com/Keats/tera/issues/211) in or wait if it would be nicer when generators are stable
- look into [https://github.com/Keats/tera/issues/219](https://github.com/Keats/tera/issues/219)

If you think you can help with any of the points above, please leave a comment on the associated issue or create a new one.
