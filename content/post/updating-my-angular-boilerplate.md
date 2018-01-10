+++
title = "Updating my AngularJS boilerplate"
path = "updating-my-angular-boilerplate"
description = "Starting an AngularJS project the easy way v2"
date = "2014-03-26"
category = "Programming"
tags = ["javascript"]
+++

I made a post about starting an angular project a few months ago ([there](http://vincent.is/starting-an-angularjs-project/)) and I kept updating the boilerplate to adapt to my workflow.  
Here's what's different from that time (spoiler: mostly the build system).

## Structure
The structure is very similar to what I had before:
```bash
.
├── app
│   ├── app.coffee
│   └── home
│       └── module.coffee
├── assets
│   └── img
│       └── test.png
├── index.html
├── style
│   ├── app.scss
│   ├── _foundation.scss
│   ├── _grid-settings.scss
│   └── snowflake
├── templates
│   └── home
│       └── index.html
└── tests
    ├── integration
    │   └── home
    │       └── basic.tests.coffee
    └── unit
        └── home
            └── basic.tests.coffee

```

If you compare with the previous version, you can notice it changed a bit.  
The templates, tests and styles are placed in their own directory (with tests being separated by unit and integration) since I personally find it cleaner that way.  
I've seen quite a few people mentionning they were putting all of this in the feature directory but to me it makes it hard to find stuff (I use the same templates and tests directory in my django projects as well so it may be an habit).  

In the style directory, you might have noticed the snowflake thing.   
This is my base SCSS (you can see the repo on github: [https://github.com/Keats/snowflake](https://github.com/Keats/snowflake)) which is Bourbon (for the mixins you would usually use compasss), Neat (for the grid system) and Bitters (for the typography for now).  

## Build and features
The previous build system was using Grunt but I switched to Gulp as the config file made much more sense to me (and way simpler to understand and faster).  
The build does the same thing the Grunt was doing and a few additional things:

- watch over .coffee file and compile them
- watch over .sass file and compile them
- watch over .html file and minify them (wasn't there before)
- watch over the images in the assets directory and copy them when added/modified
- reload the page when any of this is happening

Another thing I added is Protractor (end to end testing using webdrivers) support.  
By default, it does not run on the watch task as it can take some time but a CI task that run both unit and integration tests is available (and runs on travis with the .travis.yml file provided).  
If you have an opensource project on github, Travis CI works out of the box.

## What's next
I'm pretty happy with the current setup, the only thing I'm thinking of is to use coffeescript classes a bit more instead of functions for controllers and services but I haven't explored that too much yet.  
Another thing I do on my own project but didn't do in that boilerplate is checking in the node_modules and libs directory. I do that in order to not have failures on CI or on deploy due to internet or npm issues but I prefer giving people the choice and keeping the repo small so it's still gitignored for now.

Any feedback is obviously much appreciated !
