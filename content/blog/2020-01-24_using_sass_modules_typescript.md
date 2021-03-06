+++
title = "Using CSS modules with Sass, Webpack and TypeScript"
description = "A brief explanation on how to add CSS modules for the React/TS/Webpack starter"
+++

A few months ago, I mentioned in my articles about setting up Webpack with TypeScript ([part 1](@/blog/2019-10-29_react-typescript-webpack-1.md) and 
[part 2](@/blog/2019-11-01_react-typescript-webpack-2.md)) that CSS modules would be a nice addition to it. Here we go!

## What are CSS modules?
One common issue for anyone writing CSS is **specificity**. As a site grows, the number of CSS rules and classes grow. 
This makes it easy to accidentally re-use an existing class name by inadvertence and wonder why your text is now red. 

CSS modules are pretty simple. Let's start by writing CSS/Sass/Less as you would normally do:

```css
.my-class {
   color: red;
}
.title {
   font-size: 2rem;
}
```
You can then import the file in your `.js`/`.ts` variable (like `import styles from "_style.scss";`) and access the class names from it: `styles.title`.
Not very impressive but if you look at the source of your HTML page you will notice the class is some random combination of letters and numbers.
This is the powerful part of CSS modules: each class gets its own unique name which means that there cannot be specificity issues anymore.


There are a few other ways to solve the specificity issues:

- use something like [BEM](http://getbem.com/), which requires discipline
- use a CSS-in-JS library like [emotion](https://emotion.sh/docs/introduction), which is more complex and has lower performance than alternatives
- hope for the best

## Adding CSS module to the Webpack boilerplate
Turns out enabling them is really easy! The only tricky part is, as some might have guessed from the example above, ensuring
TypeScript does not error when loading the Sass file. Thankfully, a loader exists to automatically create definition file from CSS files: 
[typings-for-css-modules-loader](https://www.npmjs.com/package/@teamsupercell/typings-for-css-modules-loader). 

Let's go quickly through the main changes needed to the Webpack configuration:

```diff
-          // Translates CSS into CommonJS
-          "css-loader",
+          {
+            loader: "@teamsupercell/typings-for-css-modules-loader",
+            options: {
+              banner: "// autogenerated by typings-for-css-modules-loader."
+            }
+          },
+          // Translates CSS into CommonJS with modules
+          {
+            loader: "css-loader",
+            options: {
+              modules: {
+                mode: "local",
+                localIdentName: '[local]--[hash:base64:6]',
+              },
+              localsConvention: "camelCase"
+            }
+          },

```

We go from a plain `css-loader` to one with modules enabled with a `local` scope and where the generated classes are still readable.
We also tell the loader to camel case the classes in order to satisfy the various linters.
Lastly, we set the `@teamsupercell/typings-for-css-modules-loader` **above** the `css-loader`, the position is important.
There are other changes in the commit, such as ignoring all generated files, that are pretty straightforward.

The commit is <https://github.com/Keats/webpack-react-typescript/commit/9786130bf283d47af1d1945ac66679a0529254c4>.


## Anything missing?
Now that we have CSS modules in place, the only thing I consider missing is [Storybook](https://storybook.js.org/). This is
unlikely to get an article as it is pretty easy to follow the instructions to install it though.

Are there any amazing libraries/Webpack plugins I'm missing out on?
