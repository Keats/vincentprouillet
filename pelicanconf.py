#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Vincent Prouillet'
SITENAME = u'Vincent Prouillet'
SITEURL = 'http://localhost:8000'
SITE_SUBTITLE = u'Contractor in London <br> Python + Javascript'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

DELETE_OUTPUT_DIRECTORY = True
PATH = 'content/'
THEME = "hyde"

STATIC_PATHS = [
  'images',
  'extras'
]

# A list of extra files to copy from the source to the destination
EXTRA_PATH_METADATA = {
  'extras/robots.txt': {'path': 'robots.txt'}
}

# I don't want pagination/tags/categories/etc
DEFAULT_PAGINATION = False
AUTHOR_SAVE_AS = False
AUTHORS_SAVE_AS = False
TAG_SAVE_AS = False
TAGS_SAVE_AS = False
CATEGORY_SAVE_AS = False
CATEGORIES_SAVE_AS = False
ARCHIVES_SAVE_AS = False

MENU = {
  'About': '%s/presenting-himself/' % SITEURL,
  'Projects': '%s/working-on/' % SITEURL,
  'Github': 'https://github.com/Keats'
}

COLOR_SCHEME = 'theme-base-0f'

PLUGIN_PATH = 'plugins'
PLUGINS = ['gzip_cache', 'sitemap']

# Settings for the sitemap plugin
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
        'indexes': 0.7,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

