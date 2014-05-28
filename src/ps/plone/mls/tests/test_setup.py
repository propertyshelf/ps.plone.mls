# -*- coding: utf-8 -*-
"""Test Setup of ps.plone.mls."""

# python imports
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# local imports
from ps.plone.mls.testing import INTEGRATION_TESTING


class TestSetup(unittest.TestCase):
    """Validate setup process for ps.plone.mls."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_product_is_installed(self):
        """Validate that our product is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('ps.plone.mls'))

    def test_plone_mls_listing_installed(self):
        """Validate that plone.mls.listing is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('plone.mls.listing'))
