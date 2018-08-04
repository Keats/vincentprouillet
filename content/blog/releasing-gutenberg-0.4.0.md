+++
title = "Gutenberg 0.4.0: custom taxonomies, image processing and more"
description = "Gutenberg 0.4.0 is out with custom taxonomies, image processing, improved shortcodes and more"
date = 2018-08-03
draft = true
+++

[Gutenberg](https://github.com/Keats/gutenberg) is a powerful static site engine inspired by [Hugo](https://gohugo.io/) but simpler to use.
You can build pretty much any kind of static site with it using markdown:

- a basic blog
- a landing site
- a knowledge base
- a gitbook (there is a [theme](https://github.com/Keats/book) for that)
- a documentation site
- all of the above combined

You can download built binaries from the [Github releases page](https://github.com/Keats/gutenberg/releases) or install
it from [one of the installation methods](https://www.getgutenberg.io/documentation/getting-started/installation/).

You should also be able install it on Ubuntu via Snapcraft once [this bug](https://forum.snapcraft.io/t/the-rust-plugin-sets-an-invalid-manifest-path/6565/6)
is resolved.

## What's new

Lots of things! You can view the [CHANGELOG](https://github.com/Keats/gutenberg/blob/master/CHANGELOG.md) for
a quick overview: I will look at the biggest changes in more details here including the breaking ones and how to migrate.

### Breaking: custom taxonomies
Before 0.4.0, you could only have two kind of taxonomies: `tags` and `categories`. You
couldn't paginate their pages, have a RSS feed for each or create your own taxonomy.

Let's see how to use, and also how to migrate from the point of view of a current user
already using tags/categories.

If you are looking for more information, the [docs](https://www.getgutenberg.io/documentation/content/taxonomies/) have been updated — look
for the various taxonomies pages in the side menu.

#### Updating the configuration
The first thing to do is open your `config.toml` and list the taxonomies you want to use:

```toml
# You can delete those 2 lines, they aren't used anymore.
generate_tags_pages = true
generate_categories_pages = true

# And define them like so instead
taxonomies = [
    # each tag will have its own RSS feed
    {name: "tags", rss: true},
    # 5 items per page for a term, you can also customise the pagination path
    # like for the rest of the paginated content
    {name: "categories", paginate_by: 5},
    # Basic definition: no RSS or pagination
    {name: "authors"},
]
```

#### Updating the templates
We need to change two things regarding the taxonomies templates:

- their location
- the main variable they use

 First we need to move the templates their new location:

- `tags.html` -> `tags/list.html`
- `tag.html` -> `tag/single.html`
- `categories.html` -> `categories/list.html`
- `category.html` -> `categories/single.html`

In short, Gutenberg is now looking for:

- `$TAXONOMY_NAME/single.html`
- `$TAXONOMY_NAME/list.html`

Lastly, the name of the variables available have changed:

- replace `tags` and `categories` with `terms`
- replace `tag` and `category` with `term`

#### Updating the content
Before, your front-matter would look like:

```
+++
title = "Provisioning and deploying this blog with Ansible"
description = "Showing off Ansible by example"
date = 2013-08-17
category = "Devops"
tags = ["ansible"]
+++
```

An updated version is:

```
+++
title = "Provisioning and deploying this blog with Ansible"
description = "Showing off Ansible by example"
date = 2013-08-17

[taxonomies]
categories = ["Devops"]
tags = ["ansible"]
+++
```

Note that every taxonomies is now required to take an array of string, whereas before
there could be only a single category.

### Breaking: removal of `order` sorting & renaming of `next`/`previous`
Before 0.4.0, you could sort pages by `date`, `order` and `weight`.

`order` and `weight` were the opposite of each other but the difference of meaning led
to [confusion](https://github.com/Keats/gutenberg/issues/338) when trying to get the `previous` or the `next` page.

To make things more explicit two changes have been made:

- `order` has been removed
- `page.previous` and `page.next` have been renamed depending on the sorting used:
    - `date`: now called `page.earlier` and `page.later`
    - `weight`: now called `page.lighter` and `page.heavier`

No more `<a class="previous" href="{{page.next.permalink}}>{{page.next.title}}</a>`!

This has been implemented by [Daniel Sockwell](https://github.com/codesections) as his first ever Rust PR!
Daniel has also made tons of improvements to the documentation, something always appreciated.

### Image processing

This is the amazing work of [Vojtech Kral](https://github.com/vojtechkral) who also wrote
a thorough [documentation page](https://www.getgutenberg.io/documentation/content/image-processing/) explaining it in detail.

In short: you can now resize images from a template and implementing a gallery is trivial. Open an issue if you have an idea for
some image processing not already in!

### Shortcodes fixes
In the previous versions, [shortcodes](https://www.getgutenberg.io/documentation/content/shortcodes/) were parsed with a Regex and built up
while parsing the Markdown which ended up being some of the worst spaghetti code I have ever written.
It lead to numerous bugs as well some valuable features like array arguments to be almost impossible to implement — at least for me.


In Gutenberg 0.4.0, shortcodes are now rendered before Markdown as a separate pass, going through a custom parser specifically written for it.
The rendered shortcodes are then inserted back into the Markdown as raw HTML so the (much simplified) Markdown parser can ignore them.
Thanks to that redesign, all shortcodes feature requests were added easily and every known bug has been fixed.

### External link checker
Link rot can be a big issue: some pages might not make sense anymore as a whole if an important link stopped working.

Since Gutenberg already checks internal links, only external links were left to check!
Simply add `check_external_links = true` to your `config.toml` and Gutenberg will look up every link in your pages, reporting the ones
not working.

This process is quite slow though so I would recommend enabling it once in a while to check but not all the time.
Keep in mind that some results might be false negatives: crates.io for example [always returns a 404](https://github.com/rust-lang/crates.io/issues/788).

## What's next

The main goal for the next version is i18n support. There is an [open RFC](https://github.com/Keats/gutenberg/pull/111) to
discuss how the implementation would look like, comments are very welcome.

The main issue left seems to be the translation of the template texts as I'm not sure how to handle that.
Right now it's a dictionary in `config.toml` but that can grow to be quite large so a separate file for each language
would make sense. Pluralization also becomes an issue.

Once the spec is clearly defined on all points, I would happy to mentor people of any skill level on bits of it: `gutenberg` is divided in
many sub-crates, making changes pretty self-contained.

As always if you have any feedback or bugs, please open an issue. Hopefully soon Gutenberg will have enough users
to qualify for a free open-source Discourse forum to have a good way to interact with users more efficiently than GitHub issues.
If you are using Gutenberg and are not featured in [the list of sites](https://github.com/Keats/gutenberg/blob/master/EXAMPLES.md), please
add yourself!

