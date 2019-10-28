+++
title = "A boilerplate for a React+TypeScript frontend — Part 1"
description = "How to quickly get started with a React/TypeScript project using Webpack"
+++

Starting a new frontend project is tiresome. My usual process is to look at the last project I worked on, 
try to extract all the base dependencies and configuration and see if a Hello World still works after upgrading everything.
This problem might be alleviated with tools such as [create-react-app](https://github.com/facebook/create-react-app) but
I personally prefer not having an abstraction layer for the configuration as it is something I always end up having to
tweak. Even when using frameworks like [Next.js](https://nextjs.org/) where the configuration is hidden, you still need
to make some changes and understanding [Webpack](https://webpack.js.org/) goes a long way in the frontend world.

The article is split in two parts: 

1. Getting a local dev environment set up: this article
2. Making it production ready: an upcoming article

The focus for these article is to set up a build process for modern browsers with TypeScript: I am not going to pick any library other than React.
State management, testing framework etc are all up to you. The slight
exception to that rule is that I will use [Sass](https://sass-lang.com/) to handle the styling rather than alternatives such as Less/CSS-in-JS.
Once again, this is up to you. If you prefer to use JS for your CSS, just skip the last section of this article.

I am also going to use [yarn](https://yarnpkg.com/lang/en/) as package manager but `npm` will work as well.

You can view the end result in <https://github.com/Keats/webpack-react-typescript>.

## TypeScript setup
[TypeScript](https://www.typescriptlang.org/) is the most important tool for me in the frontend world. I first talked about 
it on this blog [in 2014](@./blog/2014-5-4_switching-to-typescript.md) and it only got better with time. This is a superset of JavaScript, simply adding 
types to it. I don't think static typing in dynamic languages are controversial anymore, seeing how [many](https://sorbet.org/) [languages](http://mypy-lang.org/) adopt it.
Static typing is the ultimate form of documentation as it HAS to be correct.

Let's add it to the project:

```bash
$ yarn add typescript --dev
```

This will create your project `package.json` as well as a lock file: `yarn.lock`.

The next step is to create a `tsconfig.json`, containing our TypeScript configuration:

```json
{
  "compilerOptions": {
    "module": "es6",
    "moduleResolution": "node",
    "esModuleInterop": true,
    "target": "es6",
    "jsx": "react",
    "sourceMap": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "allowUnreachableCode": false
  },
  "include": [
    "./src/**/*"
  ]
}
```

Let's go through them quickly:

- `module` and `esModuleInterop`: ensures we use the latest module system and compatible with the Babel ecosystem
- `moduleResolution`: look into the `node_modules` folder for packages
- `target`: we target modern browsers so ES6 is fine here. If you need IE11 support, change it to `es5`
- `jsx`: we use React and transpile from TypeScript directly so we use `react`
- `sourceMap`: we want them
- `strict`: enable all the strict flags automatically

All the other options are adding some additional checks, such as not allowing unused variables and a list 
of all the options can be found in [TypeScript documentation](https://www.typescriptlang.org/docs/handbook/compiler-options.html).
Lastly, we set up an include path containing `"./src/**/*"`: we will put all our code in a `src` folder.

In this setup, we will only use TypeScript and not [Babel](https://babeljs.io/). It is possible to use TypeScript for
typechecking only and pass the code to Babel for transpilation but, unless you need a specific Babel plugin, there are no 
reasons to do that nowadays. You will have to wait a few more months before getting stage 3 features - not a big deal.

The commit for that step can be seen in <https://github.com/Keats/webpack-react-typescript/commit/a083ce1511b15c51d4a8d3ef95f2da05a669758b>.

## Webpack setup
Let's start the slightly more complex part! Once you understand how Webpack works, this is actually pretty simple.

### Webpack itself
We first need webpack and its CLI:

```bash
$ yarn add webpack webpack-cli --dev
```

Let's also create a file named `webpack.config.js` as well as a `src` folder and an empty `index.tsx` file in it.
Lastly, I always set up an [.editorconfig](https://editorconfig.org/) file to let text editors sync on how to format things.

A very basic configuration for Webpack doing nothing would be something like:

```js
const path = require("path");

module.exports = {
    context: __dirname,
    mode: "development",
    entry: {
        app: "./src/index.tsx"
    },
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "app.[hash].js"
    },
    devtool: "eval-source-map",
    resolve: {
        extensions: [".js", ".jsx", ".ts", ".tsx"]
    },
    module: {
        rules: []
    },
};
```
This means we are using `src/index.tsx` as the entry point (e.g. what Webpack is loading) and the output will be created in
the `dist` directory, containing the hash in the filename for caching reasons.
We use `eval-source-map` as `devtool` value as this is the best setting for development, You can see all the different values
in the [Webpack devtool documentation](https://webpack.js.org/configuration/devtool/#devtool). Finally, we let Webpack know that
it should try to load imports with no extensions as `.js`, `.jsx`, .`ts` and `.tsx` (so we can do `import something from "../index"`) and add a script to build our project.

```diff
diff --git a/package.json b/package.json
index eb50375..1bc2df7 100644
--- a/package.json
+++ b/package.json
@@ -1,4 +1,8 @@
 {
+  "scripts": {
+    "build": "webpack",
+  },
   "devDependencies": {
     "typescript": "^3.6.4",
     "webpack": "^4.41.2",
```

Running that script (`yarn build`) will create the `dist` folder containing a file with a name like `app.5730f5cdf8cb70458282.js`.
Since we didn't write any code yet, it currently only contains Webpack's own code.

The commit for those changes is in <https://github.com/Keats/webpack-react-typescript/commit/48fc3f342c3f4f53c30af1b457d90351f442b4f0>.

### Loaders and plugin

In this article we are aiming for a simple SPA without SSR so let's setup a super basic React application in order to actually bundle something.

```bash
$ yarn add react react-dom
$ yarn add @types/react @types/react-dom --dev
```

React doesn't ship the TypeScript type definitions by default so we need to download them manually.

The simplest React code we can write in `src/index.tsx` is:

```tsx
import React from "react";
import ReactDOM from "react-dom";

ReactDOM.render(<h1>Hello world</h1>, document.getElementById("root"));
```

This will render the React app in the HTML element with id `root`, which, as some of you might have noticed, doesn't exist yet.

There is a plugin that will handle the HTML for us: [html-webpack-plugin](https://github.com/jantimon/html-webpack-plugin).

```bash
$ yarn add html-webpack-plugin --dev
```

We are using this plugin here because we do not need to display dynamic `<meta>` attributes depending on the page. If you
need it for SEO or other reasons, you will need to use another approach, likely involving some kind of SSR.

Enabling it in our `webpack.config.js` is trivial:

```diff
diff --git a/webpack.config.js b/webpack.config.js
index 2267dfd..bcbe494 100644
--- a/webpack.config.js
+++ b/webpack.config.js
@@ -1,4 +1,5 @@
 const path = require("path");
+const HtmlWebpackPlugin = require("html-webpack-plugin");
 
 module.exports = {
     context: __dirname,
@@ -17,4 +18,7 @@ module.exports = {
     module: {
         rules: []
     },
+    plugins: [
+        new HtmlWebpackPlugin({ template: "index.html" }),
+    ]
 };
```

The template can be something very basic such as:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>My project</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>
```
Do remember that the `id` of a container needs to match the one set in `index.tsx`.

Trying to run the build against at this point will give you an error about a missing loader for this type of file, referring
to our `index.tsx`.

The commit for the above is <https://github.com/Keats/webpack-react-typescript/commit/3af8820f98b3645381edfb99792700922823394b>.

Loaders are the way Webpack knows what to do with each filetype. In our case, we have these TypeScript files but we didn't tell
Webpack what to do with them: we need to add a loader for it. In the case of TypeScript, we will add a plugin in addition.

```bash
$ yarn add ts-loader fork-ts-checker-webpack-plugin --dev
```

The reason we use a loader and a plugin is performance: the loader will only perform transpilation while the plugin
will typecheck in another thread.

```diff
diff --git a/webpack.config.js b/webpack.config.js
index bcbe494..cd657ff 100644
--- a/webpack.config.js
+++ b/webpack.config.js
@@ -1,5 +1,6 @@
 const path = require("path");
 const HtmlWebpackPlugin = require("html-webpack-plugin");
+const ForkTsCheckerWebpackPlugin = require("fork-ts-checker-webpack-plugin");
 
 module.exports = {
     context: __dirname,
@@ -16,9 +17,19 @@ module.exports = {
         extensions: [".js", ".jsx", ".ts", ".tsx"]
     },
     module: {
-        rules: []
+        rules: [
+            {
+                test: /\.(ts|tsx)$/,
+                loader: "ts-loader",
+                options: {
+                    // We use ForkTsCheckerWebpackPlugin for typechecking
+                    transpileOnly: true
+                }
+            },
+        ]
     },
     plugins: [
         new HtmlWebpackPlugin({ template: "index.html" }),
+        new ForkTsCheckerWebpackPlugin(),
     ]
 };
```

Those changes are in the commit <https://github.com/Keats/webpack-react-typescript/commit/a3fdbade49deaffd4b5cd762021920efad0fbc8c>.

Running `yarn build` again will now bundle our code: just open `dist/index.html` to check for yourself. While opening that folder,
you might have noticed that there are many `.js` files in there: we never actually cleaned that folder. 
Nothing a Webpack plugin ([clean-webpack-plugin](https://www.npmjs.com/package/clean-webpack-plugin)) or a `rm -rf dist/` in the script cannot solve.

The commit for the plugin way is <https://github.com/Keats/webpack-react-typescript/commit/42ca8ba4f4ec0312d26defef610f7652a26ce40c>.

### webpack-dev-server
We have our build working now but it builds from scratch every time, which sucks.
Thankfully, Webpack has some nice tooling with its dev server allowing Hot Modules Replacement (HMR): live reloading of your code
without having to refresh.

```bash
$ yarn add webpack-dev-server --dev
```

And update `webpack.config.js`:

```diff
diff --git a/webpack.config.js b/webpack.config.js
index 9bf647a..3b576bd 100644
--- a/webpack.config.js
+++ b/webpack.config.js
@@ -1,4 +1,5 @@
 const path = require("path");
+const webpack = require("webpack");
 const HtmlWebpackPlugin = require("html-webpack-plugin");
 const ForkTsCheckerWebpackPlugin = require("fork-ts-checker-webpack-plugin");
 const { CleanWebpackPlugin } = require("clean-webpack-plugin");
@@ -29,9 +30,21 @@ module.exports = {
         },
         ]
     },
+    devServer: {
+        contentBase: path.join(__dirname, "dist"),
+        port: 9000,
+        hot: true,
+        historyApiFallback: true,
+        overlay: true,
+        stats: "minimal"
+    },
     plugins: [
         new HtmlWebpackPlugin({ template: "index.html" }),
-        new ForkTsCheckerWebpackPlugin(),
+        new ForkTsCheckerWebpackPlugin({
+            // For the dev server overlay to work
+            async: false,
+        }),
         new CleanWebpackPlugin(),
+        new webpack.HotModuleReplacementPlugin(),
     ]
 };

```

And add a new script, `dev` with a value of `webpack-dev-server`. Running `yarn dev` will now run a local server on
port 9000 that will also recompiles on change and reload the components without causing a refresh: try it for yourself
by changing the text `index.tsx` while having the page open.

Let's backtrack a bit to explain the `devServer` options though. As always, the complete documentation is available
on [Webpack documentation](https://webpack.js.org/configuration/dev-server/) but the key options there are:

- `hot`: yes please, we do want HMR
- `historyApiFallback`: if your app is a SPA with navigation you will need that option enabled to not see 404s
- `overlay`: display errors as an overlay on the app, useful to ensure you're not missing it out from the terminal
- `stats`: Webpack is very noisy by default, this turns the output level to something more reasonable

For the changes in the `plugins` section, we do disable `async` of `ForkTsCheckerWebpackPlugin` to have overlay still
work as well as adding the builtin HMR plugin.

The commit is <https://github.com/Keats/webpack-react-typescript/commit/ed546d935487f4e4350e5267261b2c6a7bac015b>.

At this point we have a functional working setup but there are a couple of tools we can add to improve the code quality.

## Auto-formatting

[Prettier](https://prettier.io/) is a very nice tool to format pretty much every language used in the JavaScript world.

```bash
$ yarn add prettier --dev
```

Prettier is opinionated and as such has [few options](https://prettier.io/docs/en/options.html) to configure. The only change I like to make is setting the maximum
number of characters in a line to be 100 instead of the default 80. It can be configured directly from `package.json`.

```js
  "prettier": {
    "printWidth": 100
  },
```

As well as a new script `fmt`: `prettier --write 'src/**/**.ts*'` that will format all TypeScript files in the `src` folder.
The main issue is that for these tools to matter, they need to be enforced. An easy way to do that is via a commit hook, using
something like [husky](https://www.npmjs.com/package/husky). As with `prettier`, we can configure `husky` easily in `package.json`:

```js
  "husky": {
    "hooks": {
      "pre-commit": "yarn fmt:check"
    }
  },
```

where `fmt:check` is a new script that only checks whether there are files needing to be formatted: `prettier --list-different 'src/**/**.ts*'`.

The next time someones working on that project calls `git commit`, this command will be ran before and will fail if any file
needs formatting. Don't forget to run this command in your CI as well!

The commit is <https://github.com/Keats/webpack-react-typescript/commit/a464f58d80af0aa45be55bd3df87bb00d74ed958>.

## Linting
The last code quality tooling we are going to add is [ESLint](https://eslint.org/). Setting it up requires a few more 
dependencies than the other tools as we need to make it work with React, Prettier and Typescript and that is split in
several packages.

```bash
$ yarn add eslint eslint-config-prettier eslint-plugin-react @typescript-eslint/eslint-plugin @typescript-eslint/parser --dev
```

The configuration is kept in a file named `.estlintrc.js`:

```js
const path = require("path");

module.exports = {
  parser: "@typescript-eslint/parser",
  extends: [
    "plugin:react/recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier/@typescript-eslint"
  ],
  parserOptions: {
    project: path.resolve(__dirname, "./tsconfig.json"),
    tsconfigRootDir: __dirname,
    ecmaVersion: 2018,
    sourceType: "module"
  },
  rules: {
    // Place to specify ESLint rules. Can be used to overwrite rules specified from the extended configs
    // e.g. "@typescript-eslint/explicit-function-return-type": "off",
    "react/prop-types": [0],
  },
  settings: {
    react: {
      version: "detect" // Tells eslint-plugin-react to automatically detect the version of React to use
    }
  }
};
```

Essentially we tell ESLint that we are going to use TypeScript and what configuration to use for the parser,
enable the recommended lints for React and TypeScript and lastly we add `prettier/@typescript-eslint` to disable all rules
conflicting with `prettier`. I also disable the `react/prop-types` linting rule as we are using TypeScript and actually
have strongly typed props already.

The linting script in our case is `"lint": "eslint 'src/**/**.ts*'"`.

The commit is <https://github.com/Keats/webpack-react-typescript/commit/f30c07b1564457e55f9110c32ca766caf060b34d>.

## Bonus: Sass handling

You can skip that section if you prefer using some CSS-in-JS.

```bash
$ yarn add sass-loader node-sass style-loader css-loader --dev
```

As you might have understood already, we need to add some _loaders_ to handle Sass files in our Webpack config:

```js
{
    test: /\.s[ac]ss$/i,
    use: [
      // Creates `style` nodes from JS strings injected in our index.html
      "style-loader",
      // Translates CSS into CommonJS
      "css-loader",
      // Compiles Sass to CSS
      "sass-loader"
    ]
}
```

And then you need to tell Webpack to load the root file by importing it into your `index.tsx` file, in my case 
`import "../style/app.scss";`. If you added `scss` to `resolve.extensions` in the Webpack configuration, you can skip the `.scss`.
Live reload will continue to work with Sass editing: you can change the background colour and see it immediately reflected
in your browser.

This setup will not solve the classic CSS specificity issues where some changes in a component might affect another component, unless
you are well disciplined with naming classes such as using [BEM](http://getbem.com/). One nice automatic solution to that
are [CSS modules](https://github.com/css-modules/css-modules) but that will likely be a separate article.

The commit is <https://github.com/Keats/webpack-react-typescript/commit/3d74c80168c18c2a6eef75d6b66a7dd9befa167c>.

## What's next
With that, we have a working development setup. It is not production and deployment ready however and that is what we will look at
in the second part.