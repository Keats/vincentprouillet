+++
title = "A different approach to routing in Single-Page Applications: now in production"
description = "A framework agnostic approach to routing for SPA: now in production"
category = "Programming"
tags = ["javascript"]
+++

I've recently wrote [an article](./blog/2017-05-08_testing-a-different-spa-routing.md) about a
framework agnostic routing approach for SPA and promised to post an update once it is a bit more tested.
I have since moved [Proppy](https://proppy.io) from [react-router](https://github.com/ReactTraining/react-router) v2 to
the structure described in my article and the result is pretty great!

I did change a few things from it though.

First, the `onClick` of the `Link` component was incorrect and has been changed to:

```ts
private onClick(event: React.MouseEvent<{}>) {
    event.preventDefault();
    event.stopPropagation();
    // I also changed the props `name` to `to`
    const {to, params, options} = this.props;
    router.navigate(to, params, options);
}
```

The store also changed in order to only display an animation after a certain amount of time, avoiding blinking effects:

```ts
class RouterStore {
  @observable current: State;
  @observable asyncInProgress = false;
  // Only happens if the page wasn't loaded in less than 500ms
  @observable showLoadingScreen = false;
  loadingTimeout: null | number;

  @action setCurrent(state: State) {
    this.current = state;
    this.asyncInProgress = false;
    clearTimeout(this.loadingTimeout);
    this.showLoadingScreen = false;
  }

  @action startAsyncLoading() {
    this.asyncInProgress = true;
    this.loadingTimeout = setTimeout(() => this.showLoadingScreen = true, 500);
  }
}
```

Any component can now observe `showLoadingScreen` and render a loading effect very easily. 500 milliseconds is probably
too high but I was on a slow connection several thousands of kilometers away from our servers when I tried it.

The only issue we encountered was that some users were faced with a blank page. I was not able
to reproduce it and no errors were reported to our Sentry server. After a couple of unsuccessful debugging
sessions, I noticed something in the [router5 documentation](http://router5.github.io/docs/router-options.html):
the `strictQueryParams`.

By default in `router5`, a route with a path of `/` will not be matched by the URL `/?_ga=blabla`:
turns out this was exactly what was happening for [Proppy](https://proppy.io). I
[opened an issue](https://github.com/router5/router5/issues/137) to change the default to a saner one and it seems
it will happen, but in the next major version as this is a breaking change. In the meantime,
the paragraph about `strictQueryParams` got moved to the top in the docs in order to be more visible.

Lastly, someone mailed me mentioning [react-mobx-router5](https://github.com/LeonardoGentile/react-mobx-router5) which
was inspired by [the same article](https://hackernoon.com/how-to-decouple-state-and-ui-a-k-a-you-dont-need-componentwillmount-cc90b787aa37)
as this serie of posts. I think a library for this routing approach is overkill. Pretty much all the code needed is in
the [previous article](./blog/2017-05-08_testing-a-different-spa-routing.md) and is less than 100 LOC that you can customise
any way you want since different apps will have different needs.

