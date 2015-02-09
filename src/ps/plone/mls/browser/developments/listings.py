# -*- coding: utf-8 -*-
"""Show Listings for developments."""

# zope imports
from Products.Five import BrowserView
from zope.annotation.interfaces import IAnnotations


class DevelopmentListings(BrowserView):
    """Show listings for a specific development."""

    @property
    def listings(self):
        """"""
        cache = IAnnotations(self.request)
        item = cache.get('ps.plone.mls.development.traversed', None)

        if item is None:
            return

        return item.listings()
