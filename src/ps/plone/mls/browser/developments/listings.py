# -*- coding: utf-8 -*-
"""Show Listings for developments."""

# zope imports
from Products.Five import BrowserView
from plone.mls.listing.browser.interfaces import IBaseListingItems
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer


@implementer(IBaseListingItems)
class DevelopmentListings(BrowserView):
    """Show listings for a specific development."""

    @property
    def listings(self):
        """Get the listings for the development.

        Optional filter by development phase or property group via GET
        params from the request.
        """
        cache = IAnnotations(self.request)
        item = cache.get('ps.plone.mls.development.traversed', None)

        if item is None:
            return

        return item.listings()
