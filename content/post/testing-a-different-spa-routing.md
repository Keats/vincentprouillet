+++
title = "A different approach to routing in Single-Page Applications"
url = "testing-a-different-spa-routing"
description = "Trying out a framework agnostic approach to routing for SPA"
date = "2017-05-08"
category = "Programming"
tags = ["javascript"]
+++


Routing is a big part of most SPA: 

- what to render when a user hits a certain URL
- whether the user is allowed to reach that page
- what data do we need to load before rendering 
- eventually display some loading screen if necessary.

## The problem
In the React world, [React-Router](https://github.com/ReactTraining/react-router) is the standard. 
It is a bit infamous as its API has changed drastically for each major version. 
[Proppy](https://proppy.io) is still using v2 as updating it didn't seem to bring much benefit and would take time.
Our only issue with our current setup is that we are not able to make the async transitions the way we would like them to be, but it is
an annoying one from a UX point of view.

After reading [How to decouple state and UI (a.k.a. you don’t need componentWillMount)](https://hackernoon.com/how-to-decouple-state-and-ui-a-k-a-you-dont-need-componentwillmount-cc90b787aa37) by the author of [MobX](https://mobx.js.org), I realised that routing should be something that is framework-agnostic. 
After all, isn't routing simply matching a URL state to a function? There is no need for something specific to React, Angular or anything else.

I recently started experimenting with it and I think I found a nice setup. 
I haven't tried it for a complex app yet though so it is probably lacking in some ways.
I will write another article on how it works in a real app when I have the time to try it in Proppy.

## The solution

This example will use React, MobX and [router5](http://router5.github.io/). 
router5 is a nice router library that treats routing state like any application state. 
Combined with MobX, you can have a store that will contain the routing state trivially without any framework.
I couldn't find an up to date TypeScript definition for router5 so I [made one](https://gist.github.com/Keats/1b8833b581d01e751048e1f51041817f). 
I'm not entirely sure whether this is the correct way to write a definition file though so I will wait a bit before making a PR to [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped/).

### Routing setup
Let's take a very simple routing scheme:

```tsx
const routes: Array<object> = [
  // Logged-in routes
  {name: "home", path: "/", canActivate: loggedInRequired, onActivate: dashboardStore.fetch},

  // Logged-out routes
  {name: "signin", path: "/signin"},
  {name: "signup", path: "/signup"},
  {name: "forgot-password", path: "/forgot-password"},
];

export type Routes =
  "home"
  | "signin"
  | "signup"
  | "forgot-password"
;
```
As you can see, nothing magical going on: `routes` is simply an array of routes, which are plain JavaScript objects themselves.
The `Routes` type has to be manually updated to match the routes but allows compile-time checking of the routes: a worthy trade-off in my eyes.

The `canActivate` key corresponds to a [lifecycle function](http://router5.github.io/docs/preventing-navigation.html) of router5. 
router5 will call this function before transitioning to the new state, preventing the transition if necessary.
In that case it is simply the following:

```tsx
const loggedInRequired = () => (toState: State, fromState: State, done: any) => {
  // userIsLoggedIn can be whatever you need it to be
  if (userIsLoggedIn()) {
    return true;
  } else {
    // redirect to signin page if the user isn't logged in
    done({redirect: {name: "signin"}});
  }
};
```

`onActivate` will be explained in a bit.

Before looking at the router setup, let's have a quick look at the MobX router store:

```tsx
import {action, observable} from "mobx";
import {State} from "router5";

class RouterStore {
  @observable current: State;
  @observable asyncInProgress = false;

  // Called after transition
  @action setCurrent(state: State) {
    this.current = state;
    this.asyncInProgress = false;
  }

  @action startAsyncLoading() {
    this.asyncInProgress = true;
  }
}

const routerStore = new RouterStore();
export default routerStore;
```
If you haven't used MobX before, I heavily recommend it and [wrote an introduction to it](./post/explaining-mobx/index.md) before. In a nutshell,
think of the code above as a simple class that has 2 observable values: `current` and `asyncInProgress`.

Ok we got our routes and store, we now need to create a router:

```tsx
// Router setup
const router = createRouter(routes);
router.usePlugin(browserPlugin(), mobxRouterPlugin);
router.useMiddleware(asyncMiddleware(routes));
router.start();
````

This does a few things. First we create a router using the routes we defined above. We then add 2 plugins:

- `browser`: a built-in plugin that will update the browser URL and state on route change using the HTML5 history API
- `mobxRouterPlugin`: a very simple custom made plugin shown below that will upate the store on transition success and error

```tsx
import routerStore from "./stores/router";

// Tell MobX which page we're on
export function mobxRouterPlugin(router: Router) {
  return {
    onTransitionError: (toState: State) => {
      // TODO handle that.
    },
    onTransitionSuccess: (toState: State) => {
      routerStore.setCurrent(toState);
    },
  };
}
(mobxRouterPlugin as PluginFactory).pluginName = "MOBX_PLUGIN";
```
How errors are handled is really up to you, I'm focusing on the happy path for that article.

Next up is the `asyncMiddleware` that handles any pre-loading we need to do. 
If a `onActivate` function on a route is found a route, it assumes it is an async call that returns a promise:

```tsx
const asyncMiddleware = (routes: Array<any>) => (router: Router) => (toState: any, fromState: State, done: any) => {
  const route = routes.find((r) => r.name === toState.name);
  // do we have a function to call?
  if (route.onActivate) {
    // Tell the store that will load something, might want to have some visual loading effect
    routerStore.startAsyncLoading();
    return route.onActivate(toState.params)
      .then((res: any) => {
        // Fail the transition if the call failed
        if (res.error) {
          return done({code: "TRANSITION_ERR", error: res});
        }
      });
  }
  done();
};
```

In practice, the `onActivate` method of the `home` route will be called before transitioning and will only be completed if the call succeeded. 
The store will automatically be notified of the start of an async call and of any successful transition: displaying a loading progress becomes straightforward.

Finally, we start the router which will automatically use the current URL as the current state as we are using the Browser plugin.

### Integrating React
Now that we have the routing is up and running, we need to be able to render components depending on the URL and navigate between pages. 
Since all the routing state is in a MobX store, this is simply a matter of having a component observe it:


```tsx
@observer
class App extends React.Component<{}, {}> {
  render() {
    if (routerStore.current === null) {
      return null;
    }

    let component = null;
    switch (routerStore.current.name as Routes) {
      case "signup":
        component = <SignUp />;
        break;
      case "signin":
        component = <SignIn />;
        break;
      case "forgot-password":
        component = <ForgotPassword />;
        break;
    }
    // A 404 would be quite blank.
    return (
      <div className="app-container">
        {component}
      </div>
    );
  }
```
That's it. A simple switch on the name of the current route and we're good to go. 

There is a small twist for links though: using a basic `<a href="/forgot-password">Forgot?</a>` will trigger a full reload, unless there's an option I missed. 
You will need to use the `router.navigate` method to navigate instead. 
If you are using React you might have a `Link` component in your project to standardize how links are made and the various styles it can have. 
Here's an example for a basic one:

```tsx
export interface ILinkProps {
  name: Routes;
  params?: object;
  options?: {reload: boolean, refresh: boolean};
}

class Link extends React.Component<ILinkProps, {}> {
  protected static defaultProps = {
    options: {},
    params: {},
  };

  render() {
    const {name, params} = this.props;

    // Build the end url
    const href = router.buildPath(name, params as any);
    if (href === null) {
      // tslint:disable-next-line
      console.error("<Link> Couldn't make URL for", name, params);
    }

    return (
      <a href={href} onClick={this.onClick.bind(this)}>
        {this.props.children}
      </a>
    );
  }

  private onClick(event: React.MouseEvent<{}>) {
    const {name, params, options} = this.props;
    const comboKey = event.metaKey || event.altKey || event.ctrlKey || event.shiftKey;

    if (event.button === 0 && !comboKey) {
      event.preventDefault();
      router.navigate(name, params, options);
    }
  }
}

export default Link;
```

Which can be used like so:

```tsx
<Link name="forgot-password">Forgotten password?</Link>
```

The route name will be checked at compile time as well, no more typos!

## The end
Will this work for complex apps? 
I don't know but I will certainly try it and report!

Edit: It looks like TypeScript 2.4 will support [string enums](https://github.com/Microsoft/TypeScript/pull/15486)!
This means we will be able to not duplicate the `Routes` content and use an enum instead!
