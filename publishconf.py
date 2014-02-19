#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://vincent.is'
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL
FEED_ATOM = 'feed.xml'
FEED_ALL_ATOM = False
CATEGORY_FEED_ATOM = False

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "vincentprouillet"
GOOGLE_ANALYTICS = "UA-43335571-1"
