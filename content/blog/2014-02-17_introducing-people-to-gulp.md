+++
title = "Gulp by example"
description = "Showing how to use Gulp, a new javascript build system and its difference with Grunt"
category = "Programming"
tags = ["javascript"]

[extra]
updated = 2014-07-23
+++

#### UPDATE (2014/07/23)
I have updated gulp and replaced connect with browsersync (I did that already in the article with an earlier version of browser-sync but not on the [example project](https://github.com/Keats/gulp-example) on github, it is now up to date).
I also do not use coffeescript anymore, I [switched to typescript](@/blog/2014-05-04_switching-to-typescript.md) and use plain js for the gulpfile but everything in this post is still valid.

#### UPDATE (2015/05/07)
This article was written for gulp 3.
If you want to move to gulp 4, please go [this article](@/blog/2015-03-20_migrating-to-gulp4.md).

## Introduction
So I wanted to make changes to my [ng-boilerplate](https://github.com/Keats/ng-boilerplate "ng-boilerplate") project to make it simple enough for a javascript newbie to understand what was going on.
The main issue was the Gruntfile and its configuration, roughly 400 lines of javascript handling all the possible tasks (watch, releasse, test, etc): it was working, but was pretty hard to see what was going on.
Also having to put files in temporary directory all the time was bugging me.
Enter [gulp.js](http://gulpjs.com/ "gulp.js") (an example project following the example described in this post is available [here](https://github.com/Keats/gulp-example "https://github.com/Keats/gulp-example")).


## Gulp
Gulp uses Node.js streams ([explanations here](https://github.com/substack/stream-handbook "stream handbook")), meaning it doesn't need to create files and thus is faster than Grunt.
Another advantage for Gulp is that gulpfiles are actually code, not configuration like Grunt, making it very easy to understand what's going on at a glance (and shorter in my case as well).
The way gulp works is the following:

- select the input files (for example all the .coffee files)
- pass them through plugins (linting, coffeescript, concat, minify)
- output them somewhere if needed

Contrary to grunt, you only define the source files once, not for every plugin.

## Example
I am going to use a basic sass/coffeescript project setup for the example.
The project is organised the following way:

```bash
.
├── dist
│   ├── css
│   ├── index.html
│   └── js
├── gulpfile.coffee
├── index.html
├── coffee
│   └── **/*.coffee
├── package.json
├── README.md
├── sass
│   └── **/*.scss

```

The goal is to have automatic compilation of sass and copy of index.html and *.coffee files to the dist folder on change, automatically reloading the page when that happens.
First we need to install gulp and create a gulpfile (in coffeescript for the example).

```bash
$ sudo npm install -g gulp # for the cli
$ npm install gulp gulp-util coffee-script --save-dev
$ touch gulpfile.coffee
```
You can run a gulp task that way:

```bash
$ gulp mytaskname
$ gulp
```

The second command will run the task called default.

Before modifying the file, let's think at what we will need:

- sass compiler (gulp-sass)
- something to reload the page (browsersync)
- coffeescript linter (gulp-coffeelint)
- coffeescript compiler (gulp-coffee)
- concat files (gulp-concat)
- minify js (gulp-uglify)

Let's install those.

```bash
$ npm install gulp-sass browser-sync gulp-coffeelint gulp-coffee gulp-concat gulp-uglify --save-dev
```

No need to load task the Grunt way, we can just require those the node way:

```
gulp = require 'gulp'
gutil = require 'gulp-util'

sass = require 'gulp-sass'
browserSync = require 'browser-sync'
coffeelint = require 'gulp-coffeelint'
coffee = require 'gulp-coffee'
concat = require 'gulp-concat'
uglify = require 'gulp-uglify'
```

I like to define the sources/destinations paths right at the beginning, works for me but everyone will do that differently.

```
sources =
  sass: 'sass/**/*.scss'
  html: 'index.html'
  coffee: 'src/**/*.coffee'

destinations =
  css: 'dist/css'
  html: 'dist/'
  js: 'dist/js'
```

Gulp has a very simple API and we are going to use 4 methods from it: task, src, dest and watch (that's pretty much the whole API).

The first task will be to set the server for the dev environment with the autoreload.

```
# Reloads the page for us
gulp.task 'browser-sync', ->
    browserSync.init null,
    open: false
    server:
      baseDir: "./dist"
    watchOptions:
      debounceDelay: 1000
```
There are several plugins that reload the page but this one is the simplest I found, simply defines the files you want to watch and it will reload for you, no need for additional config.
This task is not a really good example of what gulp does so let's move to a more exciting one, the sass task.

```
gulp.task 'style', ->
  gulp.src(sources.sass) # we defined that at the top of the file
  .pipe(sass({outputStyle: 'compressed', errLogToConsole: true}))
  .pipe(gulp.dest(destinations.css))
```

Now you can see a bit more of a magic but it's still fairly straightforward.
gulp.src finds the files that matches the glob, pipe them to the sass plugin that will compile them (setting errLogToConsole to true means we won't exit gulp if we make a mistake in the sass file, good when watching), result is piped to gulp.dest which defines the destination to which we want to write the file.

The HTML task just copies the index.html file to the dist folder and reloads the server, you should be able to follow the code by now.

```
gulp.task 'html', ->
  gulp.src(sources.html)
  .pipe(gulp.dest(destinations.html))
```

Now the coffeescript task is more interesting because it really highlights the difference between Grunt and Gulp.
With Grunt you would need to put your files into temporary folders, for example after compiling the .coffee files.

```
# I put linting as a separate task so we can run it by itself if we want to
gulp.task 'lint', ->
  gulp.src(sources.coffee)
  .pipe(coffeelint())
  .pipe(coffeelint.reporter())

gulp.task 'src', ->
  gulp.src(sources.coffee)
  .pipe(coffee({bare: true}).on('error', gutil.log))
  .pipe(concat('app.js'))
  .pipe(uglify())
  .pipe(gulp.dest(destinations.js))
```

I find this system quite brilliant, no need to go through temp folders just to be able to run all your tasks and it's WAY more readable than going through the config for each of these plugins you would do in Grunt.

The last bit to do is the watch task, ie the one used in dev to do all these things when a file changes.
```
gulp.task 'watch', ->
  gulp.watch sources.sass, ['style']
  gulp.watch sources.app, ['lint', 'src', 'html']
  gulp.watch sources.html, ['html']

  # And we reload our page if something changed in the output folder
  gulp.watch 'dist/**/**', (file) ->
    browserSync.reload(file.path) if file.type is "changed"
```

And that's it, you got the whole thing set up (well...), very easy to understand even by someone that never used gulp.
Any dev should be able to tell what's going on from the code itself.

I lied a bit when I said everything was setup.
Right now there are 2 glaring issues:

- no way to make a clean build
- we don't want to have the js minified when developing

Let's fix that !
We need to install a few additional plugins and add a few tasks:

```bash
$ npm install gulp-clean run-sequence --save-dev
```

```
gulp.task 'clean', ->
  gulp.src(['dist/'], {read: false}).pipe(clean())

gulp.task 'build', ->
  runSequence 'clean', ['style', 'lint', 'src', 'html']

gulp.task 'default', ['build', 'browser-sync','watch']
```
This allows us to make a clean build and watch over the changes.
For the env/prod differences (like minifying), you need to pass another argument called type when running gulp:

```bash
$ gulp --type prod
```

And then retrieve that value using gulp-util and use it in the tasks:

```
isProd = gutil.env.type is 'prod'

# Do your if statements in the tasks
.pipe(if isProd then uglify() else gutil.noop())
```

You can find an example app using this gulpfile here [https://github.com/Keats/gulp-example](https://github.com/Keats/gulp-example "https://github.com/Keats/gulp-example"), and see the whole gulpfile [there](https://github.com/Keats/gulp-example/blob/master/gulpfile.coffee "finished gulpfile").

## Conclusion
I really like Gulp !
This feels way more simple to write and to read than Grunt was.
I got my ng-boilerplate setup to be equal to how it was with Grunt in one afternoon and it certainly feels faster.
If you have any comments or feedback (ie I'm doing something horribly wrong), feel free to post a comment and/or make a pull request to the example project.

