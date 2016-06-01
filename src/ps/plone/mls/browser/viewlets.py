# -*- coding: utf-8 -*-
"""Customized plone viewlets."""

# zope imports
from plone.app.layout.viewlets import common
from plone.mls.listing.browser.interfaces import IListingDetails

# local imports
from ps.plone.mls.interfaces import IDevelopmentDetails
from ps.plone.mls import utils


class DublinCoreViewlet(common.DublinCoreViewlet):
    """Customized DublinCore descriptions for MLS embeddings."""

    def update(self):
        super(DublinCoreViewlet, self).update()

        description = None
        if IDevelopmentDetails.providedBy(self.view):
            try:
                description = self.view.item.description.value
            except AttributeError:
                return
        elif IListingDetails.providedBy(self.view):
            try:
                description = self.view.description
            except AttributeError:
                return

        if description is not None:
            description = utils.smart_truncate(description)
            for meta_tuple in self.metatags:
                tag, text = meta_tuple
                if tag == 'description':
                    self.metatags.remove(meta_tuple)
            self.metatags.append(('description', description))


class TitleViewlet(common.TitleViewlet):
    """Customized title Viewlet for MLS embeddings."""

    def update(self):
        super(TitleViewlet, self).update()

        title = None
        if IDevelopmentDetails.providedBy(self.view):
            try:
                title = self.view.item.title.value
            except AttributeError:
                title = getattr(self.request, 'development_id', None)
        elif IListingDetails.providedBy(self.view):
            try:
                title = self.view.title
            except AttributeError:
                title = getattr(self.request, 'listing_id', None)

        if title is not None:
            self.site_title = u'{0} &mdash; {1}'.format(title, self.site_title)
