#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'ajya'
SITENAME = u'The Blog'
SITEURL = 'https://ajya.github.io'

PATH = 'content'

TIMEZONE = 'Europe/Riga'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
RSS_FEED_SUMMARY_ONLY = False
FEED_ALL_RSS='feeds/all.rss.xml'
TAG_FEED_RSS='feeds/%s.rss.xml'
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME='Flex'

# Blogroll
LINKS = (('Outreachy', 'https://www.outreachy.org/'),
         ('OpenStack', 'https://www.openstack.org'),)

CONTACT = (('IRC OFTC','ajya'),
	   ('Matrix','@ajya:matrix.org'))

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
