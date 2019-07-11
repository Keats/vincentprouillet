+++
title = "Switching to TypeScript"
description = "Why use TypeScript"
category = "Programming"
tags = ["javascript", "typescript"]
+++

Until a few weeks ago, I was a convinced user of coffeescript: significant whitespace, no curly braces, list comprehensions, classes, thick arrow, chained comparisons, etc.
The list of good things coffeescript brings to the table is quite long, just have a look the [coffeescript website](http://coffeescript.org/).

Then, Microsoft announed [Typescript 1.0](http://www.typescriptlang.org/) and that made me give a second look to it.

My initial reaction the first time I heard about it was something along the line of: eh, they are probably going to stop working on it in a year or so, like lots of their projects.
Turns out I was wrong !
I am not going to detail Typescript too much as there is a complete [handbook](http://www.typescriptlang.org/Handbook) available.


## Why would I use Typescript ?

I can see several reasons.

First, it's still mostly javascript, unlike coffeescript which makes it easier to learn (coffeescript is very easy but lots of people will not contribute back if it means having to do it in coffeescript).
There is a big thread on Discourse (link now dead) about whether to use Javascript or Coffeescript.
After switching to javascript, more contributions happened so that's definitely something to take into account if you are doing an open source project.

The second is obviously types. Having types (in javascript) is awesome.
All the typescript type checking only happens for the developer, nothing will be left in the compiled js (which is perfectly readable javascript by the way).
Having types also mean that you can have autocompletion available, even for your custom types, which is pretty cool.
Keep in mind that types are optional, no one forces you to use them if you don't want to.
If you decide to use them though, a vital resource for Typescript is [DefinitelyTyped](https://github.com/borisyankov/DefinitelyTyped) which contains definitions for most of the JS libraries.

The third would be all the other features that Typescript brings: modules, classes, arrow functions, etc.
Their goal is to have an interface similar to what we will have in ES6 but, as ES6 is still changing a lot (for example the module implementation), it can differ quite a bit right now.
I am confident they will adapt to whatever standard has been adopted, unless they decide to somehow abandon their goal of sticking to ES6.

## How am I using it

I finished switching my [ng-boilerplate](https://github.com/Keats/ng-boilerplate) to Typescript and it works pretty well.
Since I use AngularJS with REST APIs, I can define the types I will receive in the API, methods on controllers/scopes and have some robust code that ensure I didn't call a made-up function or made a typo in an object attribute immediately.
The interfaces you define can also serve as a very good documentation and helps if you're dealing with a huge codebase (which is the goal of Typescript).
I made a simple [invoice app](http://vincent.is/working-on/invoicing/#/) (github [link](https://github.com/Keats/invoicer)) when I was trying it out and it caught many errors before I even opened the page.

## Conclusion
While Typescript is not the Holy Grail of Javascript, it makes writing it as nice as coffeescript (coffeescript will be more concise imo though) while having types.
I can see it working very well once a project gets big but I would use it even for small projects.
Try it out and see for yourself !
