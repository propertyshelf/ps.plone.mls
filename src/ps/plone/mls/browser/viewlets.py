# -*- coding: utf-8 -*-
"""Customized plone viewlets."""

# zope imports
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.layout.viewlets import common
from plone.mls.listing.browser.interfaces import IListingDetails

# local imports
from ps.plone.mls.interfaces import IDevelopmentDetails
from ps.plone.mls import utils


class DublinCoreViewlet(common.DublinCoreViewlet):
    """Customized DublinCore descriptions for MLS embeddings."""

    def _get_mls_description(self):
        """Get the description from an embedded item."""
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

        description = utils.smart_truncate(description)
        return description

    def update(self):
        super(DublinCoreViewlet, self).update()

        description = self._get_mls_description()

        if description is None:
            return

        meta_dict = dict(self.metatags)
        meta_dict['description'] = description

        try:
            use_all = api.portal.get_registry_record(
                'plone.exposeDCMetaTags'
            )
        except InvalidParameterError:
            try:
                props = api.portal.get_tool(name='portal_properties')
                use_all = props.site_properties.exposeDCMetaTags
            except Exception:
                use_all = False

        if use_all:
            meta_dict['DC.description'] = description
        self.metatags = meta_dict.items()


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
