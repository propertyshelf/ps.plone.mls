# -*- coding: utf-8 -*-
"""Test Layer for ps.plone.mls."""

# zope imports
from plone.app.testing import (
    IntegrationTesting,
    PloneSandboxLayer,
    PLONE_FIXTURE,
)
from zope.configuration import xmlconfig


class PSPloneMLS(PloneSandboxLayer):
    """Custom Test Layer for ps.plone.mls."""
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        """Set up Zope for testing."""
        # Load ZCML
        import ps.plone.mls
        xmlconfig.file(
            'configure.zcml',
            ps.plone.mls,
            context=configurationContext,
        )

    def setUpPloneSite(self, portal):
        """Set up a Plone site for testing."""
        self.applyProfile(portal, 'ps.plone.mls:default')


PS_PLONE_MLS_FIXTURE = PSPloneMLS()
PS_PLONE_MLS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PS_PLONE_MLS_FIXTURE, ),
    name='PSPloneMLS:Integration',
)
