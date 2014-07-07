# -*- coding: utf-8 -*-
"""Test 'Featured Listings' Content Type."""

# python imports
import unittest2 as unittest

# zope imports
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject, queryUtility

# local imports
from ps.plone.mls.content.featured import IFeaturedListings
from ps.plone.mls.testing import INTEGRATION_TESTING


CT = 'ps.plone.mls.featured'


class FeaturedListingsIntegrationTestCase(unittest.TestCase):
    """Test Case for the 'ps.plone.mls.featured' content type."""
    layer = INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'folder')

        self.ct = api.content.create(self.folder, CT, 'fl1')

    def test_ct_available(self):
        """Validate that the content type is available."""
        portal_types = getToolByName(self.portal, 'portal_types')
        self.assertTrue(CT in portal_types)

    def test_fti(self):
        """Validate that the factory type information is available."""
        fti = queryUtility(IDexterityFTI, name=CT)
        self.assertIsNotNone(fti)

    def test_adding(self):
        """Validate the created content type."""
        self.assertTrue(IFeaturedListings.providedBy(self.ct))

    def test_schema(self):
        """Validate the correct schema."""
        fti = queryUtility(IDexterityFTI, name=CT)
        schema = fti.lookupSchema()
        self.assertEqual(IFeaturedListings, schema)

    def test_factory(self):
        """Validate the content type factory."""
        fti = queryUtility(IDexterityFTI, name=CT)
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IFeaturedListings.providedBy(new_object))

    def test_behaviors(self):
        """Validate that the required behaviors are available."""
        self.assertTrue(IExcludeFromNavigation.providedBy(self.ct))
