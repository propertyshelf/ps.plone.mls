# -*- coding: utf-8 -*-
"""Test utilities from ps.plone.mls.browser.utilities."""

from ps.plone.mls.testing import INTEGRATION_TESTING


try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestUtilitiesView(unittest.TestCase):
    """Validate the utility methods."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.portal = self.layer['portal']
        self.view = self.portal.restrictedTraverse('@@psplonemls-utils')

    def test_smart_truncate(self):
        """Validate the 'smart_truncate' method."""
        TEXT = (
            u'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
            u'Aliquam non lorem vulputate leo tincidunt cursus eget ac '
            u'mauris. Aliquam at orci in elit gravida faucibus eget vel '
            u'lectus.'
        )

        truncated = self.view.smart_truncate(TEXT)
        self.assertEqual(len(truncated), 156)
        self.assertEqual(
            truncated,
            u'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
            u'Aliquam non lorem vulputate leo tincidunt cursus eget ac '
            u'mauris. Aliquam at orci in elit gravida...'
        )

        truncated = self.view.smart_truncate(None)
        self.assertIsNone(truncated)
