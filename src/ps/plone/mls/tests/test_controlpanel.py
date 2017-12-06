# -*- coding: utf-8 -*-
"""Test Control Panel for plone.mls.core."""

from plone import api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.mls.core.interfaces import IMLSSettings
from plone.registry import Registry
from ps.plone.mls.browser.interfaces import IPloneMLSLayer
from ps.plone.mls.testing import INTEGRATION_TESTING
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestMLSControlPanel(unittest.TestCase):
    """Validate control panels are available."""
    layer = INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.portal = self.layer['portal']
        alsoProvides(self.portal.REQUEST, IPloneMLSLayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = Registry()
        self.registry.registerInterface(IMLSSettings)

    def test_controlpanel_base_view(self):
        """Validate that the base configuration view is available."""
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST),
            name='mls-controlpanel-base',
        )
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_base_view_protected(self):
        """Validate that the base configuration view needs authentication."""
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(
            Unauthorized,
            self.portal.restrictedTraverse,
            '@@mls-controlpanel-base',
        )

    def test_mls_in_controlpanel(self):
        """Validate that there is an MLS entry in the control panel."""
        controlpanel = api.portal.get_tool(name='portal_controlpanel')
        actions = [
            a.getAction(self)['id'] for a in controlpanel.listActions()
        ]
        self.assertTrue('ps_plone_mls' in actions)
