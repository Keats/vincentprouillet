+++
title = "Making third party widgets"
description = "How to develop cross-domains javascript widgets such as Facebook Like buttons"
category = "Programming"
tags = ["javascript"]
+++

## Introduction
By third-party widgets, I mean javascript that you load on an external website and
that talks to your website, think Facebook Like button or Disqus comments.
Since I didn't find a lot of resources explaining how to create them (except the excellent book simply
named [Third-party JavaScript](http://thirdpartyjs.com/ "Third-party JavaScript")), I will give some details on how I did the widgets for
[Playfire](https://www.playfire.com/ "Playfire")).

## Examples
Here are some examples of the widgets I made:

- disqus-like comments on the playfire blog: example [here](http://blog.playfire.com/2013/11/bf-vs-cod-which-do-you-want.html "Link to blog article")
- Want button, to add a game to their wishlist from the GreenManGaming website: example [here](http://www.greenmangaming.com/s/gb/en/pc/games/strategy/football-manager-2014/ "GMG")

## The theory
Let's define some terms first.
The website where the widget is embedded is called a **consumer** while the website hosting is is called a **provider**.
Communicating between the consumer and the provider is the biggest problem you will meet early on.
There are a few ways to deal with it, I will only present the ones that are usable if you intent to send/receive data with the widgets.

### Iframe
Iframe embeds another page in the page, avoiding completely the cross origin problem since the widget would actually be on domain.
The problem with using iframe like this is that iframes do not inherit styles from the main page, meaning it might look completely different
from the rest of the website. You can sniff the style and apply them but designing becomes tricky.

### CORS
CORS (Cross Origin Resource Sharing) is an official spec designed to do exactly that ([this article](http://www.html5rocks.com/en/tutorials/cors/ "Article about CORS")) explains it well).
If you don't need to support older browsers (IE8 and IE9 have some [issues](http://blogs.msdn.com/b/ieinternals/archive/2010/05/13/xdomainrequest-restrictions-limitations-and-workarounds.aspx "CORS in IE8-9")), CORS should be the way to go.
This will require the server to set appropriate headers to responses from the widgets.

### Hidden iframes
This method will not use iframes directly.
Instead, as its name suggest, a hidden iframe will be created and will be used to transmit and receive data from the provider.
The widgets itself will be inserted in the page HTML normally.
This is the approach I used since it works on every browsers.

So now that you have decied on how to communicate between consumer and provider, let's focus on the consumer part.

### Consumer side
The consumer will probably embed your widgets to add a feature to their website (social buttons, stats, ...) but they are most of the time
not the main part of a page.
It's critical that your widget doesn't slow down the consumer website or cause errors.
For the speed part, you need to load your script asynchronously otherwise you could block the rendering of the page.

P4W (Playfire 4 Web, name of the Playfire widgets) uses this to load:

```html
<script>
    (function() {
      var p4w = document.createElement('script');
      p4w.async = true;
      p4w.src = 'https://p4w.playfire.com/embed.js';
      (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(p4w);
    })();
</script>

```

This assumes that the page has a &lt;head&amp; or &lt;body&amp; tag. A better way would be to find the first &lt;script&amp; (since we have at least one for sure) and insert the new script tag before it.
In this case embed.js is just a very small file that will load the real javascript file.
Keeping it simple here means that you can change whatever you want behind the scene, it will still works for the people using the above snippet in their website.

### Provider side
Nothing particular needs to be done on the server since we are not using CORS.
If you are, don't forget to set the Allowed- headers.

### Notes about logging in
If your widget needs to allow people to log in, you will need to use a popup on your domain, since you won't be able to set the cookies from an another domain, more on that later.

## The practice

Most of the P4W widgets are doing the same thing: get data from Playfire, display them and modify it if you're logged in (there are some read-only widgets though).
Creating some kind of frameworks thus made sense.

### Choosing the tools
Since your javascript will be loaded on external websites, your impact on the page needs to be as small as possible so you can't just add jQuery or any library you want.
After looking around, I settled on these libraries:

- [qwery](https://github.com/ded/qwery "qwery") for the css selector
- [bonzo](https://github.com/ded/bonzo "bonzo") for the dom manipulation
- [bean](https://github.com/fat/bean "bean") for the events
- [easyXDM](http://easyxdm.net/wp/ "easyXDM") for the cross origin messaging
- [browserify](http://browserify.org/ "browserify") to create bundles and use require like in node.js
- [Handlebars](http://handlebarsjs.com/ "handlebars") for the templates

These 6 libraries are the core of P4W.
If I started now, I might have chosen [Minified](http://minifiedjs.com/ "Minified") to replace qwery, bonzo and bean.

The build is using [Grunt](http://gruntjs.com/ "Grunt") and we use [Sass](http://sass-lang.com/ "Sass") for the style.
We currently only have integration tests using [CasperJS](http://casperjs.org/ "CasperJS").

### Creating a framework
Since all of those widgets have a similar pattern, creating some kind of framework makes sense.
It is organised the following way:

```bash
.
├── style
│   ├── css
│   ├── sass
├── templates
│   └── widget1
│       └── widget1.html
├── main.js
├── login.js
├── widget1.js

```
All of these files will be linted and concatenated by the Grunt task to form the lib.js loaded by the embed.js mentionned in the snippet above.

The main.js is the entry point of the framework: it requires all the other javascripts files and use qwery to detect whether the page it's loaded in contains
HTML elements having classes corresponding to widgets and will initialise them.
This will also detect whether one of those widgets needs to know if a user is logged in or not in Playfire (for example the blog comment will need to) and do that call to
Playfire while the widgets are initialising.
Widgets will then do calls for their own data and display themself.

If the user is not logged and an action like a click on the Want button requires the logged in state, a login popup will open, with its URL on the playfire domain so it can properly set the cookie as mentionned above.
The tricky part of that bit is actually closing the popup once the use logged in.
With most browsers, you can use postMessage to pass the data back to the opener page but this doesn't work with IE.
The easy (not so good) solution is to poll the server for login status once the popup has been opened for a while and close it on success response or timeout.

The widgets themselves all have a similar structure, allowing for copy/paste of it and then filling in the blank.
Using a common class for that would probably be better but some widgets (thinking of the comments one) can be quite different from others.

### Testing
Testing third-party widgets is a bit of a pain.
Since most of the logic will be in the server and it can be unit tested properly, I mainly focused on testing integration on the javascript side.
This means tests are not that fast (around 5s for one) but if the tests pass, there's no reason why the widgets wouldn't work on live.
CasperJS was a very nice interface for PhantomJS and is quite fun to use.

### Things to watch out for
While this hasn't happened to us yet since the widgets are mainly on pages we control, you have to be careful with the javascript/css you're using.

#### Javascript
Remember, this file will be executed on a third-party website and you don't control what they are doing with their javascript.
They could have redefined undefined or added functions to every prototypes for all you know so you can't make any assumption about what's present or not so you need to develop with that in mind.
You also need to make sure you're not leaking global variables of adding to prototypes yourself, which would mess up their own javascript.

#### CSS
Again, you don't need what kind of crazy design they might have and you don't want your css to be applied to the whole website either.
The solution for that is to use highly specific CSS selectors and use **defensive css**.
By defensive css I mean the css to ensure your widgets renders how it should. If your widget is a small box like the Tweet button, you can't exactly have a text of font size 10em there.
Adding css rules to ensure minimal consistency is the key here. While you are not going to set the font type or color, you can definitely force the font-size for example.


## Conclusion
While there's not a lot of code to show since it's not open source, I hope this article gave a good overview on how to approach the development of third party widget.
