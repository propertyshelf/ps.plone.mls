# -*- coding: utf-8 -*-
"""Vocabularies for listings."""

# zope imports
from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


@implementer(IVocabularyFactory)
class AvailableListingSearches(object):
    """Vocabulary which returns all available listing searches."""

    def __call__(self, context):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog.search({
            'object_provides': 'plone.mls.listing.browser.listing_search.'
                               'IListingSearch',
        })
        items = []
        for brain in brains:
            title = '{0} ({1})'.format(brain.Title, brain.getPath())
            items.append(SimpleTerm(brain.UID, brain.UID, title))
        return SimpleVocabulary(items)

AvailableListingSearchesFactory = AvailableListingSearches()
