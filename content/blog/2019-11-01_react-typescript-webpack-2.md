+++
title = "Setting up a React+TypeScript frontend with Webpack — Part 2"
description = "How to quickly get started with a React/TypeScript project using Webpack: the production environment"
+++

In this article, we are going to turn our [local environment setup](@/blog/2019-10-29_react-typescript-webpack-1.md) into
a production-ready setup. Thanks to improvements in recent Webpack versions, it is now straightforward.


## NODE_ENV=production in Webpack
The majority of JavaScript projects use the `NODE_ENV` variable to enable optimizations and remove debug code. If you need
to support Windows, setting an environment variable directly in the script the UNIX way is not going to work. You can install [cross-env](https://www.npmjs.com/package/cross-env) to handle cross-platform environment variables. 
The script in that case is `"build:prod": "cross-env NODE_ENV=production webpack"`.
Again, if you do not need Windows support, simply remove the `cross-env` from the script.

Now there are two ways to proceed:

1. split the configuration in multiple files and merge them with something like [webpack-merge](https://www.npmjs.com/package/webpack-merge)
2. keep everything in one file and use JavaScript to toggle things

I prefer the second approach as I find it more readable and doesn't require additional dependencies. You can judge for yourself
by looking at the [final result](https://github.com/Keats/webpack-react-typescript/blob/master/webpack.config.js).

As mentioned before, Webpack has been making things easier. With the introduction of [mode](https://webpack.js.org/configuration/mode/), it is easy
to get a production-ready bundle:

```diff
diff --git a/webpack.config.js b/webpack.config.js
index 53c39f2..b4d6e11 100644
--- a/webpack.config.js
+++ b/webpack.config.js
@@ -4,9 +4,11 @@ const HtmlWebpackPlugin = require("html-webpack-plugin");
 const ForkTsCheckerWebpackPlugin = require("fork-ts-checker-webpack-plugin");
 const { CleanWebpackPlugin } = require("clean-webpack-plugin");
 
+const isProd = process.env.NODE_ENV === "production";
+
 module.exports = {
   context: __dirname,
-  mode: "development",
+  mode: isProd ? "production" : "development",
   entry: {
     app: "./src/index.tsx"
   },
```

Just changing the mode will get us a minified output: you can check it by running `build:prod` yourself. 

Looking at the minified code, we can see that the sourcemap is embedded in the file still. 
The [best option for production environments](https://webpack.js.org/configuration/devtool/#production)
is `source-map` which we can set conditionally on the `isProd` variable: `devtool: isProd ? "source-map" : "eval-source-map",`.
Running `build:prod` again will now properly create a separate file ending in `.js.map`.
Remember that the sourcemap files should not be accessible by anyone other than you and your bug reporting app.

Lastly, the HMR from Webpack is injecting some code in the bundle that we do not want in our production bundle. We can disable it easily:

```diff
diff --git a/webpack.config.js b/webpack.config.js
index af5fd2f..63272fd 100644
--- a/webpack.config.js
+++ b/webpack.config.js
@@ -58,6 +58,6 @@ module.exports = {
       async: false
     }),
     new CleanWebpackPlugin(),
-    new webpack.HotModuleReplacementPlugin()
-  ]
+    isProd ? false : new webpack.HotModuleReplacementPlugin()
+  ].filter(Boolean)
 };
```


The commit is <https://github.com/Keats/webpack-react-typescript/commit/4527184f2d7a49447451774b1bf5cc8d4cb3c1e5>.

## Splitting chunks
In our current situation, we generate a single file for the whole app: it clocks in at 132KB before gzip.
This means that every time someone changes anything in the codebase, the full bundle will be invalidated and re-downloaded by every users.

There are two approaches to splitting the chunks:

1. **bundle splitting**: separating into fixed bundles, for example putting dependencies into another bundle
2. **code splitting**: splitting your own code into multiple bundles loaded on demand

### Bundle splitting
The easiest bundle splitting strategy is to create a `vendors` bundle containing all dependencies. In our case we currently
only have `react` and `react-dom` but it will inevitably grow and, unless you are upgrading dependencies every day, will not
change very often. Dividing the bundle does not change anything for first-time users as they will have to download all files but
repeat users will only download the bundles that changed.

Webpack comes with a built-in option to split everything coming from the `node_modules` folder to another bundle: [optimization.splitChunks.chunks](https://webpack.js.org/plugins/split-chunks-plugin/#splitchunkschunks).
Setting it to `"all"` will produce a new JavaScript file with a name starting by `vendors~app` in the output directory weighting 131KB while the app bundle shrank down to 1.9KB.
If you run `build:prod` again after making a change to `index.tsx`, you will notice the hash did change: we need to ensure the hash
is done on the content rather than the build. In practice this means changing `[hash]` to `[contenthash]` in the `output.filename` configuration in production.
Trying it again will now give the expected results: a change in our application code doesn't change the `vendors` bundle.

For many apps, just splitting the bundle that way will be enough to get started. If needed, you can create different kind
of strategies, for example:

- one file per `npm` dependency
- group packages per update of frequency: put the ones that change often in the same bundle
- group packages per kind: all React packages could go in one bundle, all data viz in another etc
- have multiple entry points: Webpack will create one file per entry point

The [Webpack documentation](https://webpack.js.org/plugins/split-chunks-plugin/#splitchunkscachegroups) 
has some examples demonstrating how to implement some of the strategies. Once again, start with the default dumb splitting and experiment as you go when needed.

The commit is <https://github.com/Keats/webpack-react-typescript/commit/cd2669b62d9542794fdc52e6e6fb1702716ddc36>.

### Code splitting
Code splitting is allowing you to import some code on demand. It relies on the [dynamic import() proposal](https://github.com/tc39/proposal-dynamic-import) which
is now on stage 4, eg finished. A simple React example would be:

```tsx
import React from "react";

class LocationForm extends React.Component<{}> {
   handleClickOnMap = () => {
     import('./locationModal')
      .then(({ locationModal }) => {
        // Use locationModal
      })
      .catch(err => {
        // Handle failure
      });
   }

   render() {
     return (
       <form>
         <button onClick={this.handleClickOnMap}>Select location</button>
       </form>
     );
   }
}
```

Imagine that the `locationModal` component is loading [Leaflet](https://leafletjs.com/) and that this is the only place
where it is used. With the bundle splitting, Leaflet would be in your bundle even for users never seeing that form. If you are
doing code splitting, you will obviously need to make sure Leaflet is not part of another chunk. Another
obvious contender for code splitting is data visualisation: plottting libraries are typically heavy and if you only have them in one page you can split it from your bundle to
provide a faster experience for everyone.


Code splitting is very powerful but not that useful if you are just starting: worry about it when your codebase is bigger. If you
are using React, the [documentation page on code splitting](https://reactjs.org/docs/code-splitting.html) is very well written and should
answer most questions on how to actually use it.

To use code splitting with TypeScript, you will also need to change `module` in `tsconfig.json` to `esnext`.

### Analyzing bundles

Once you have your bundle(s), a useful step is to actually check what they contain and whether there is fat that can be trimmed.
[webpack-bundle-analyzer](https://www.npmjs.com/package/webpack-bundle-analyzer) is shining for that usecase.

```bash
$ yarn add webpack-bundle-analyzer --dev
```

We only need to analyze bundles once in a while so I like to create a new script for it `"analyze": "cross-env NODE_ENV=production ANALYZE=true webpack",` and
only instantiate the plugin when that `ANALYZE` environment variable is set to `true`. 
Running `analyze` will give you a treemap visualisation of each package used and their size, with and without gzip.

Using this tool, it becomes very easy to notice some packages taking way more spaces than they should. The most classic examples I've seen
personally are not removing [Momentjs](https://momentjs.com/) locales for an English only site and having the full [Lodash](https://lodash.com/) while
only using one or two functions.

The commit is <https://github.com/Keats/webpack-react-typescript/commit/41190ae6e279c84c8614d5d77656b8afaed1dea3>.

## Extracting CSS

If you added Sass by following the previous article and looked at the bundle analyzer results, you might have noticed that the app bundle contains CSS. That's because
we've inlined them in our configuration via `style-loader` and need to extract it to a separate CSS file in production environment instead using a plugin.

```bash
$ yarn add mini-css-extract-plugin --dev
```

The change is pretty straightforward: we load the `MiniCssExtractPlugin` loader instead of `style-loader` in production and
add the plugin to the plugin list. The plugin can be set for every environment as it will not do anything unless the loader
is also used.

Running `build:prod` will now create a CSS file as well as a sourcemap in the `dist` folder. I'm not 100% sure the sourcemap
is accurate as I have never used them for CSS.

The commit is <https://github.com/Keats/webpack-react-typescript/commit/e97a368d67e88f2c1adb9b018b8a4164fdfd3283>.

## Conclusion

If you followed the articles or just cloned the repository, you should be in a good place to start actually building your project.
It might look complicated compared to [create-react-app](https://github.com/facebook/create-react-app) but this is a minimal setup
that you understand and that only has things what you need. Well, being a JavaScript project it still pulls way too many dependencies just for that but 
it's a good start.
