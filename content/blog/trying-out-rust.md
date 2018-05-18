+++
title = "Trying out Rust"
path = "trying-out-rust"
description = "Checking out that new language from Mozilla"
date = 2014-07-19
category = "Programming"
tags = ["rust"]
+++

Rust is an in-progress systems programming language ([official website](http://www.rust-lang.org/)).  
I'll start this post by saying I'm a python/js/go developer and never really done C or C++ (my first programming languages were PHP/C# actually since I started with a degree in biology).  
Rust is mainly targeting those C/C++ developers that need speed (without a GC) and safety.  
As a guy who does only web stuff, the absence/presence of a GC is not important since you can use slow languages like python or ruby and be completely fine with it for 99% of the sites so a GC pause probably won't even be noticed unlike in video games for example.  
Why bother learning low level languages then?  
- It's fun
- It's fast
- It has types (I love types)  

This is just my feelings after playing with it a few hours, it may contain mistakes and some stuff will probably be outdated pretty soon anyway.  
Like every article I've read, I'll be comparing some of the features with Go but do note that I like them both.

## What's Rust?
As mentioned above, Rust is a language developed by Mozilla in the open: all the code is on github, decisions are taken by committee.  
A stable release is expected around Q4 of 2014.  
You can follow or even submit/comment on RFCs on the language: [RFCs repo](https://github.com/rust-lang/rfcs), decisions on these RFCs being taken in meetings for which you can find the transcripts on [github as well](https://github.com/rust-lang/meeting-minutes).  
The language itself is also in github in case you didn't guess: [rust repo](https://github.com/rust-lang/rust).  
More discussions also happen on reddit ([/r/rust](http://www.reddit.com/r/rust)) and on the [discourse forum](http://discuss.rust-lang.org/).  
I talked quite a bit about the community because I find looking at the evolution quite fascinating, let's talk a bit about the language itself now.  

Let's use bullet points and then go through those individually

- Statically and strongly typed with generics (yay!)
- Memory safety
- Easy concurrency with no data race
- Functional stuff

### Type system
It is pretty cool.  
Variables are immutable by default and the compiler will complain if you are using a variable before initalizing it (not very idiomatic in Rust to initialize a variable after declaring it apparently anyway) or if it's unused (you can make that fail compilation if you want).
It has generics which allows some cool stuff without passing interface{} if you wanted to do something similar in Go (let's say an ORM).  
It uses traits rather than the classic interfaces OOP languages, if you've used Scala it will be familiar.

## Memory safety
Part of that section could go in the type system section but since this is the complex part of rust for newcomer like me I feel it deserves its own section.  
There are 3 types of pointers in Rust:

- owned pointers: the classic ones, compiler takes care of them automatically
- borrowed pointers: as the name implies, you can use them when you want to access data, but without taking ownership of it

Ownership (and mainly the lifetimes that go with it) is a major point of Rust and documentation will do a better job than me at explaining them: [The Rust References and Lifetimes Guide](http://static.rust-lang.org/doc/master/guide-lifetimes.html).  

### Easy concurrency with no data race
Concurrency in Rust is as easy as in Go, here's a very basic example:

```rust
// run on http://is.gd/kDPsLe
fn main() {
    let (tx, rx): (Sender<int>, Receiver<int>) = channel();

    spawn(proc() { tx.send(1); });

    let result = rx.recv();
}
```
It is very easy to read and I actually find it easier to have the named channels like this than reading from the channel.  
The "no data race" part comes from the fact that you cannot access mutable data inside a task (It won't even let you reuse the tx variable here in another as you can see in that [playpen](http://is.gd/ncfyM4).  
Trying to modify a mutable structure for example would result in a compiler error: [playpen](http://is.gd/5AFfTn).  
An in-depth explanation is also present in the docs: [The Rust Tasks and Communication Guide](http://doc.rust-lang.org/guide-tasks.html).  

### Functional stuff
I'm usually a bit wary of functional elements as it can sometimes be very hard to read and understand at a glance what a functional programmer did when he was being 'neat'.  
Nevertheless, functional programming also brings very very cool stuff:

#### Options  

An idiomatic Go function will usually return 2 elements: a value and an error. You will have to check whether the error is nil or not and handle both cases

```go
books, err := GetBooks()
if err != nil {
  return nil, err
}
books = books[:5] // will give a nil error if we didn't check the error above
return books, nil
```
I don't mind explicit error handling but it's easy to forget it somewhere and end up with a null pointer exception.  
Options are basically nullable types that forces you to handle them, enforced by the compiler.  
It is typically handled using pattern matching.

#### Pattern matching  
Those are amazing, like a switch but way more powerful. 
To handle something that could fail like the Go example above, it would look like this.

```rust
// Example from docs with a few more stuff added
fn divide(numerator: f64, denominator: f64) -> Option<f64> {
    if denominator == 0.0 {
        None
    } else {
        Some(numerator / denominator)
    }
}

// The return value of the function is an option
let result = divide(2.0, 3.0);

// Pattern match to retrieve the value
match result {
    Some(1.0) => println!("Result was exactly 1"),
    Some(x) => println!("Result: {}", x),
    None    => println!("Cannot divide by 0"),
    _ => println!("Nothing") // Compiler will fail and tell that this is unreachable as you're dealing with Some and None
}
```
A playpen is available [here](http://is.gd/0tW2Bc), modify the paraneters to divide and the pattern matching to see how it works.  
You could match on types, on values, this makes the code really neat imo and is awesome.

```rust
fn main() {
    let x = 10i;
    
    match x { 
        0 => println!("It's 0!"), 
        1 ..9 => println!("Between 1 and 9: {}", x), 
        _ => println!("Different from 0-9: {}", x) // needed to be exhaustive here, compiler will yell without it
    };
}
```

#### General 'functional' functions  
I did the first Euler problems in Rust to get the hang of it and everytime I started with the naive approach of looping.  
After reading a bit of code from experience devs, I realised you could do some nice stuff like defining a Fibonacci iterator and making a simple one liner after that to solve [problem 2](https://projecteuler.net/problem=2):

```rust
Fibonacci::new().take_while(|&i| i <= 4000000).filter(|&i| i % 2 == 0).sum();
```

# What do I think of it?
As you saw from the previous part, I'm quite enthusiastic about it.  
It's still too much in flux to be used seriously but I think that it could become a pretty big thing.  
Again, talking from the point of view of websites/services, it could become a nice alternative to Go (as more and more companies start using it for services).  
The fact that they're also building a package manager ([Cargo](https://github.com/rust-lang/cargo)) along the language is a very nice thing, solving the whole dependencies issues in Go, I need to find out whether they plan to include vendoring or not.  
I think Go is easier to pick up (language has less features, some people will consider that a minus, other a plus), has the community behind it and tools like gofmt ([one](https://github.com/pcwalton/rustfmt) is in the works for Rust).  
Another issue Rust currently has is that it is changing very fast, most of the threads/posts talking about it will not work in the current version and that is confusing.  
Up to date resources includes:

- http://rustbyexample.com/
- http://doc.rust-lang.org/std/index.html (very helpful since there's no autocompletion yet, there's [racer](https://github.com/phildawes/racer) but it doesn't seem finished)

Overall, I'll keep an eye on it and try to do a small project on it as soon as I have some free time.
