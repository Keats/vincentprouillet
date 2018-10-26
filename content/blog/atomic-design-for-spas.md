+++
title = "Atomic Design in Single Page Applications"
description = "How I use Atomic Design to architect my SPAs in React"
date = 2018-10-26
+++

This post will outline how I architect visual part of the SPAs I work on. But first, let me explain the issues I faced that led me there.
I used to put every components in a `components` folder, which obviously doesn't scale and make
it hard finding a specific component. After that, I grouped at least the top level routing
components which made things a bit tidier but was still very unsatisfying.
Looking around for various ways to organise design elements, I found [Atomic Design](http://bradfrost.com/blog/post/atomic-web-design/).
I am not going to dive deep into explaning what is Atomatic Design as the linked article does a very good job
so I would recommend taking 2 minutes to read it beforehand.

You can find a basic clone of [HackerNews](https://news.ycombinator.com/) on GitHub: <https://github.com/Keats/hn-react> made using
the principles described in this post to illustrate this article.

Lastly, while the title doesn't mention a specific framework, all the samples will use React. The
ideas presented in this post will work equally well in Vue.js or any other component-based
framework.


## Self-contained components
That is something Vue.js users can get behind!
Each component has now its own folder containing everything it needs to be used, apart from
the other components it is using as we will see in a bit.

What this means is that every component folder looks very similar to something like:

```bash
input
├── index.tsx
└── _style.scss
```

You can replace `tsx` by `js` if you are not using [TypeScript](https://www.typescriptlang.org/).

As you can see, the folder also contains a `_style.scss`. I prefer to keep my CSS out of JS and since I use [Sass](https://sass-lang.com/)
for other projects without JavaScript, it makes sense to use it. You can use whatever floats your boat though.
Those Sass files are only targeting specific CSS classes of that component, which solves potentially overlapping styling:

```css
.input {
  // the CSS of the component
}
```

The main Sass file will import each component individual style after setting up some base rules like fonts or vertical rhythm as can be seen in
[app.scss](https://github.com/Keats/hn-react/blob/91bb067276006b0ea9d191f753112a5688b7c518/src/style/app.scss).

Since each component has its own folder, it is a good place to keep related code.
For example, if I am using [GraphQL](https://graphql.org/) with [Apollo](https://www.apollographql.com/), I will also have a `queries.tsx` in there with the queries
used by the component as well as the types:


```tsx
import gql from "graphql-tag";
import {Query} from "react-apollo";

import {IOrganization} from "../../../types";

export const ALL_ORGS_QUERY = gql`
  query allOrgs {
    organizations {
      id
      name
      slug

      members {
        id
        role

        user {
          id
          name
          timezone
        }
      }
    }
  }
`;

export interface IData {
  organizations: Array<IOrganization>;
}

export class AllOrgsQuery extends Query<IData> {}
```

Now that we have seen how I organise each individual component, let's dive in the Atomic Design part.

## Atomic Design

If you have read the article introducing Atomic Design, you can probably guess that your `components` folder is going to look like that:

```bash
.
├── atoms
├── molecules
├── organisms
├── templates
└── pages
```

Let's look at them in the same order.

### Atoms

Atoms are independent components that do not have any dependencies on other components and that exist in isolation: they
probably don't do anything on their own, are mostly composed of `props` and any action they do is coming from `props`.
In terms of Redux/MobX, all of those components should be dumb/pure/presentational components.

Looking at one private project atoms, I have:

- `button`
- `input`
- `link`
- `tag`
- `toast`
- `portal`
- `icon`

There are obviously many more but this should be enough to give you an idea: they are the building blocks
of your site.

Try to have as many of your components in that folder, you will have a much easier time composing interfaces later on.

While atoms can become fairly complex (`input` for example), they can also be as simple as [a spinner](https://github.com/Keats/hn-react/blob/master/src/app/components/atoms/spinner/index.tsx).


### Molecules

By themselves, atoms are not very useful and need to be combined to make something useable: `input` + `button` giving you a `form` for example.
That is what molecules are: a combination of 2 or more `atoms` or, in rarer cases, a smart wrapper around an atom.
Therefore molecules should be dumb components when possible but it isn't required.

Here are some of the molecules from the same project:

- `form` (`input` + `label`): using MobX for state but dumb otherwise
- `dialog` (`overlay` + `button`): dumb
- `toast-container` (`toast`): smart component that will display the currents `<Toast>` components from the store

Since the HackerNews repository is a basic example, I didn't create enough atoms to have interesting molecules. However, looking at
the [story-item](https://github.com/Keats/hn-react/blob/master/src/app/components/molecules/story-item/index.tsx) it is easy to imagine
adding an `upvote` atom in there.

If you need to use a molecule in another molecule, it probably means it is an organism folder as we will now see.

### Organisms

As with molecules, there are two types of organisms I distinguish here:

- components using one or more molecules
- business-specific usage of molecule

A good definition comes from the original article:

>  Organisms are groups of molecules joined together to form a relatively complex, distinct section of an interface.

As before, here are some examples in my project:

- `sidebar`: uses only one molecule but is a distinct section of the interface
- `login-form`: the `form` molecule set-up with the right fields and the GraphQL login query
- `signup-form`: the `form` molecule set-up with the right fields and the GraphQL signup query

Each form in the app gets its own component, making testing/storybook very easy.
Most of those forms components do not have style of their own as they just rely on the `form` molecule for that.

I do not have any organisms in the HackerNews example.

### Templates

If you look at most SaaS sites, you will notice they use different layouts for different parts of their site:
the most common one being one logged out layout for the login/signup forms and the logged in layout
with your dashboard and the actual tool.

I classify those different layouts as templates and you could have for example:

- `logged-in`: a `sidebar` organism on the left and the `child` on the rest of the page
- `logged-out`: a different background with centered forms
- `settings`: some tabs

Each of those templates will have their own styling - since that's their main use - but potentially also queries: you probably
need to fetch the current user information for a `logged-in` template so moving that query at the template level will allow each page using it
to automatically fetch the data in a uniform way.

The HackerNews example has only [one template](https://github.com/Keats/hn-react/blob/master/src/app/components/templates/main/index.tsx) as, even
when logged in, the interface doesn't change significantly.

### Pages

Those are the components you use in your router, each of them corresponding to a specific URL.
They are therefore connected to your data stores and will probably have to fetch some data from your server. Most of the time,
these components `render` method will be wrapped into a template component to ensure consistent styling.

Pages tie all of the elements of Atomic Design we just talked about in a small component. There shouldn't be any styling
in those components other than the (rare) occasional divergence.
I also follow a slightly more lax approach to the "one component = one folder" mantra and group sub-routes in the same folder as the main route
for easy discovery.

Example of pages components:

- `login`
- `home`
- `user-settings`
- `verify-email`

You can view the [HackerNews homepage](https://github.com/Keats/hn-react/blob/master/src/app/components/pages/stories-list/index.tsx) for an example.

## Conclusion

While some of the rules I introduced seem inflexible, you can bend them so they make sense to you.
For example, I put my `overlay` component in the atoms folder despite it using the `portal` atom simply because I kept looking for it in the atoms folder
since I always forget it actually uses `portal`.

Overall, this structure has been a big improvement for me:

- super easy to find components (if you don't have a Go To Definition shortcut)
- trivial to test and make storybook stories
- self contained enough that I can copy-paste the atoms and molecules folder and have everything working quickly

As mentioned in the introduction, I wrote a [HN clone](https://github.com/Keats/hn-react) as an example for that article.
It is a basic React app following Atomic Design using TypeScript and MobX, as well as the routing
method [I wrote about before](./blog/testing-a-different-spa-routing-update.md) if you are curious about how it looks in practice.
In my own projects, I also use [StoryBook](https://storybook.js.org/) to easily have a visual overview of every component but I skipped adding it
for this example app.
