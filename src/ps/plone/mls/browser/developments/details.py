# -*- coding: utf-8 -*-
"""MLS development detail view."""

# python imports
from mls.apiclient.exceptions import ConnectionError

# zope imports
from Products.Five import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.component import queryMultiAdapter
from zope.interface import implementer

# local imports
from ps.plone.mls import api
from ps.plone.mls.interfaces import IDevelopmentDetails


@implementer(IDevelopmentDetails)
class DevelopmentDetails(BrowserView):
    """Detail view for MLS developments."""

    item = None

    def __init__(self, context, request):
        super(DevelopmentDetails, self).__init__(context, request)
        self.update()

    def update(self):
        item_id = getattr(self.request, 'development_id', None)
        if not item_id:
            return

        cache = IAnnotations(self.request)
        item = cache.get('ps.plone.mls.development.traversed', None)
        if item is None:

            self.portal_state = queryMultiAdapter(
                (self.context, self.request),
                name='plone_portal_state',
            )
            lang = self.portal_state.language()
            mlsapi = api.get_api(context=self.context, lang=lang)
            try:
                item = api.Development.get(mlsapi, item_id)
            except ConnectionError:
                pass
        self.item = item
