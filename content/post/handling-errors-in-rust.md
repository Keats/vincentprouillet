+++
title = "Handling errors in Rust"
path = "handling-errors-in-rust"
description = "Handling errors in Rust and making it easier with error-chain"
date = "2016-12-15"
category = "Programming"
tags = ["rust"]
+++


Error handling in Rust is pretty straightforward. 

The standard library comes with the `Result` type which has the following definition:

```rust
#[must_use]
pub enum Result<T, E> {
    Ok(T),
    Err(E),
}
```
In short, `Result` can either be OK with a value `T` or be an error with value `E`.
The `#[must_use]` annotation means that the compiler will warn you if you ignore a `Result`.

No more forgetting to catch that one exception or a `if err != nil { return nil, err }`.


## Handling Result

Let's have a look a small program to see the various way of creating and handling errors in Rust.
Follow this [playground link](https://is.gd/ZhThdZ) to run and play with the examples below.

```rust
use std::fmt;
use std::io;
use std::error::Error;

// Our set of errors for that program
#[derive(Debug)]
enum MyErrors {
    BadMood,
    // Badly implemented IO error
    FileFailure(String),
    // Correctly implemented IO error
    FileFailure2(io::Error),
}

// Impl display so we can have nice strings to print
impl fmt::Display for MyErrors {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            MyErrors::FileFailure(ref err) => write!(f, "File creation failed: {:?}", err),
            MyErrors::FileFailure2(ref err) => write!(f, "File creation failed: {:?}", err),
            MyErrors::BadMood => write!(f, "Nothing wrong, just wanted to error."),
        }
    }
}

impl Error for MyErrors {
    fn description(&self) -> &str {
        match *self {
            MyErrors::BadMood => "bad mood",
            MyErrors::FileFailure(ref err) => "file failure",
            MyErrors::FileFailure2(ref err) => "file failure",
        }
    }

    fn cause(&self) -> Option<&Error> {
        match *self {
            MyErrors::FileFailure(_) => None,
            // the cause is the io::error
            MyErrors::FileFailure2(ref err) => Some(err),
            MyErrors::BadMood => None,
        }
    }
}


impl From<io::Error> for MyErrors {
    fn from(err: io::Error) -> MyErrors {
        MyErrors::FileFailure2(err)
    }
}


fn will_succeed() -> Result<bool, MyErrors> {
    Ok(true)
}

fn will_fail(filename: &str) -> Result<(), MyErrors> {
    Err(MyErrors::FileFailure(format!("Failed to created {}", filename)))
}

fn do_something() -> Result<(), MyErrors> {
    match will_fail("index.html") {
        Ok(_) => {
            // we don't care about the result value, it's an empty tuple
            return Ok(());
        }
        Err(e) => {
            println!("Error while creating a file:\n {}", e);
        }
    };

    // Equivalent to match above
    if let Err(e) = will_fail("index.html") {
        println!("Error while creating a file:\n {}", e);
    } else {
        return Ok(());
    }
    // method 1 to propagate errors: try! macro
    let did_succeed = try!(will_succeed());
    // method 2 to propagate errors: question mark operator
    let did_succeed2 = will_succeed()?;

    Ok(())
}

fn main() {
    do_something();
}
```

About half of the lines are about defining errors, we will see how to reduce that boilerplate in the following section.
If you want to read more on that, the [error handling section](https://doc.rust-lang.org/book/error-handling.html) in the Rust book is very good.

The interesting part in that code is the body of the `do_something` function which showcases the various ways of
handling `Result`.

You can be in 2 situations when handling errors: 

- you want to handle them immediately
- you want to do an early return and pass them back to the caller

The `match` and `if let` constructs are equivalent in this case and  used if you are in the first situation.

The `try!` and question mark operator are also equivalent: they return the error if there is one and unpacks the `Ok` value
otherwise.

`?` was stabilised in Rust 1.13 (released about one month before this post) and is somewhat controversial
as some think that error handling is hidden when using it.

I like the `?` operator myself since I think it makes the code neater but I let you be the judge:

```rust
let val = try!(try!(try!(do_something()).do_something_else()).finish());
// or cleaner
let a = try!(do_something());
let b = try!(a.do_something_else());
let val = try!(b.finish());

let val = do_something()?.do_something_else()?.finish();
```


## Avoiding error boilerplate
As you saw from the example above, defining your own errors is very verbose.

After experimenting on my own at first, I found the [quick-error](https://crates.io/crates/quick-error) crate which
makes creating your own error and extending built-in ones like the `io::Error` in the previous section a breeze.
This was my go-to crate for error handling, until reading [this article](http://brson.github.io/2016/11/30/starting-with-error-chain) 
about [error-chain](https://crates.io/crates/error-chain).

`error-chain` builds on `quick-error` and makes it even more painless.

I have switched [Tera](https://github.com/Keats/tera) 0.5 to use [error-chain](https://crates.io/crates/error-chain) and am very
happy about the end result.

The `errors.rs` file in Tera went from [~80 lines](https://github.com/Keats/tera/blob/3471df41ab454c60a85ec271a945f7123705e49a/src/errors.rs) 
and lots of custom errors to:

```rust
error_chain! {
    errors {}
}
```

There is nothing you might say. And you would be somewhat correct!
Using the `error_chain!` macro gives me `Result`, `ResultExt` (a trait), `ErrorKind` and `Error` but I didn't define any
custom errors myself.

It's obviously not always empty though, here's the `errors.rs` of a static site engine using Tera:
 
```rust
use tera;


error_chain! {
    links {
        // Links Tera errors to that crate
        Tera(tera::Error, tera::ErrorKind);
    }

    foreign_links {
        // Link with errors not defined with error-chain
        Io(::std::io::Error);
    }

    errors {
        // I'm using this one lots of time so creating it there to keep it DRY
        InvalidConfig {
            description("invalid config")
            display("The config.toml is invalid or is using the wrong type for an argument")
        }
    }
}
```

The article linked previously made me realise that you need custom errors in 2 occasions: the user of the library will pattern match on them or you want 
to avoid repeating yourself like the `InvalidConfig` above. 

In Tera case, I was able to replace all the errors with `bail!` macro that comes with `error-chain`.
This is a very simple macro that works similarly to `println!` except it returns an error with the text given:

```rust
if something_is_wrong {
    bail!("Something wrong happened while doing {:?}", action);
}

// expands to
if something_is_wrong {
    return Err(format!("Something wrong happened while doing {:?}", action).into());
}
```
It doesn't look like much but using stringly typed errors saves a lot of time and makes you write better errors 
at the same time as you can write very specific errors without any boilerplate.

But the killer feature of `error-chain` is to chain errors, as its name implies. 
You often want to add context to errors and chaining allows just that. 

The easiest example is a function to open a file: Rust doesn't include the filename in the error but you usually want it if
you are going to display it.

```rust
use errors::ResultExt;

File::open(path)
    .chain_err(|| format!("Failed to open {}.", path))?
    .read_to_string(&mut content)?;
```

`chain_err` is coming from the `ResultExt` and is where the magic happens. If an error in `File::open` happens,
it will create a new error, storing the one caused by `File::open` as its cause. Errors can be chained multiple times, allowing you
to annotate errors at several levels and giving detailed error messages.

Printing all chained errors is as simple as the code below:

```rust
println!("Error: {}", e);
for e in e.iter().skip(1) {
    println!("Reason: {}", e);
}
```

I'm liking this approach quite a lot and will be using it for all my projects for the foreseeable future!
