#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "by semi_transparent. Hosted by github"
SITENAME = "semi_transparent"
SITEURL = "" #'semitransparent.github.io'

PATH = 'content'

THEME = 'eevee'
THEME_PRIMARY = 'amber'
THEME_ACCENT = 'red'
MEGA_FOOTER = False
DISCLAIMER = False
SUMMARY_MAX_LENGTH = 150

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TWITTER_USERNAME = 'semitransp'

#Header config
MENUITEMS = [("<i class='fa fa-twitter fa-2x'></i>", "https://twitter.com/semitransp"), ("<i class='fa fa-envelope fa-2x'></i>", "mailto:semitransp@gmail.com")]

DEFAULT_PAGINATION = False

STATIC_PATHS = ['images', 'images/favicon.ico']
EXTRA_PATH_METADATA = {
    'images/favicon.ico': {'path': 'favicon.ico'}
}

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
