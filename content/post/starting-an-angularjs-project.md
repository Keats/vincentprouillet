+++
title = "Starting an AngularJS project"
url = "starting-an-angularjs-project"
description = "A Boilerplate for a complete dev environment using AngularJS"
date = "2013-10-23"
category = "Programming"
tags = ["javascript"]
+++

I don't think there is any need to introduce [AngularJS](http://angularjs.org/ "AngularJS") anymore, but here's a (very) small introduction of it to make sure everyone knows the basics.  

AngularJS is a client-side framework, replacing the jquery code usually present on most sites.    
Instead of modifying the DOM on events manually (like displaying a div on a click event), AngularJS takes a declarative approach.

The following examples show the difference in paradigm between these two.

```javascript
// jQuery version
$('my-button').click(function() {
  $('my-div').show();  
});
```

```html
<!-- AngularJS version -->
<button ng-click="showDiv = !showDiv">Click me</button>
<div ng-show="showDiv">Hidden by default</div>
```

Some people will not like the fact that you're putting logic in the HTML, I personally much prefer this kind of approach to a 
jquery based one, and I find it much easier to organise your code using directives, controllers, services than the usual jquery 
spaghetti.

For a real overview, please check the official website.  


## Starting a new project
A problem new developers encounter is how to organise their code.    
For simple (and I mean -learning how it works- kind of simple only), putting everything in one file is file but obviously does not work once you start working on bigger projects.  
Since I like organising code properly, I looked around to see what was the recommended way for that in AngularJS project.  


### ng-boilerplate by Josh David Miller
While I didn't find THE answer (there's no imposed structure like in many server-side frameworks so everyone do their own thing, which can be great), I found [ng-boilerplate](http://joshdmiller.github.io/ng-boilerplate/#/home "ng-boilerplate").  
This boilerplate separates code by feature, containing all the code (including css/html) for that particular feature.  
It also uses [ui-router](https://github.com/angular-ui/ui-router "ui-router") which is quite awesome.  
It also comes with a whole lot of grunt tasks to automate dev/test/release cycle: everytime you save a file, it runs the associated task with this type of file and reloads your page.
I used this boilerplate for a learning project, [kCalculator](https://github.com/Keats/kCalculator "kCalculator") and while it is a very good start, I found it not that practical for my own use (I use Sass, it uses LESS for example) and it had lots of things that I didn't really want.


### My own ng-boilerplate
Since I wanted to start a new project (which will be much more complex than kCalculator), I decided that this time I would use something tailored for me.  
Rather than forking and changing most of the code of the original, I started from scratch and added feature by feature what I needed.  
Result is [ng-boilerplate](https://github.com/Keats/ng-boilerplate "ng-boilerplate") (yes the name is lazy). 
The end results differs quite a bit from the original :

- no ng-min in the build (since you can do it by hand in your code)
- coffeescript only
- Sass with Foundation
- templates and css in their own directory instead of inside their small 'feature app'
- reorganised grunt tasks
- not concatenating dist libs with app libs (need to implement using CDN for dist libs on release task)

## Architecture example
Here is the layout of the project I'm working on (this is still very early, probably going to change some things later on) :

```bash
.
├── app
│   ├── app.coffee
│   ├── app.tests.coffee
│   ├── home
│   │   └── home.coffee
│   ├── teams
│   │   ├── list.coffee
│   │   ├── module.coffee
│   │   ├── service.coffee
│   │   └── tests
│   │       └── list.tests.coffee
│   └── users
│       ├── module.coffee
│       ├── new.coffee
│       └── service.coffee
├── assets
│   └── img
│   └── fonts
├── common
│   └── form
│       └── directives.coffee
├── index.html
├── style
│   ├── app.scss
│   ├── _forms.scss
│   ├── _normalize.scss
│   └── _settings.scss
└── templates
    ├── home
    │   └── index.html
    ├── teams
    │   └── list.html
    └── users
        ├── main.html
        ├── new.html
        └── verification.html

```
All of the different 'features' are nicely placed under the app folder and each file in it has a unique function. 
The module.coffee under each looks something like the following:

```coffeescript
modules = [
  'ui.router.state',

  'users.new'
]

users = angular.module 'arena.users', modules

users.config ['$stateProvider', ($stateProvider) ->
  $stateProvider.state 'users',
    abstract: true
    url: '/users'
    views:
      main:
        template: '<ui-view/>'

  $stateProvider.state 'users.new',
    url: '/new'
    templateUrl: 'users/new.html'
    controller: 'NewUserCtrl'
    data:
      pageTitle: 'Register'

    $stateProvider.state 'users.verification',
      url: '/verification'
      templateUrl: 'users/verification.html'
      data:
        pageTitle: 'Check your emails'
```

This file is the entry point of the feature, injecting all the different modules (list, create, etc) and defining the views (using ui-router).  
All of the other files are standard AngularJS controllers, services, directives.  
If I think something can be reused in another feature/project, it goes in the common directory.

## Conclusion
So far I really like this organisation, and this is working well for now.  
I will update it as the project grows bigger since I will probably find flaws by then.  

## How to learn AngularJS

- [egghead.io](http://egghead.io/ "egghead.io"): short videos explaining very well everything
- [thinkster.io](http://www.thinkster.io/ "thinkster.io"): explains lots of concept using egghead videos as a base and expand on them 
