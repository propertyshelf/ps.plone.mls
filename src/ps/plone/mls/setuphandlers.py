# -*- coding: utf-8 -*-
"""Post install import steps for ps.plone.mls."""

# zope imports
from Products.CMFPlone.interfaces import INonInstallable
from Products.GenericSetup.interfaces import IProfileImportedEvent
from plone import api
from zope.component import adapter
from zope.interface import implementer

# local imports
from ps.plone.mls import config


@implementer(INonInstallable)
class HiddenProfiles(object):
    """Define hidden GenericSetup profiles."""

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'ps.plone.mls:testfixture',
            'ps.plone.mls:uninstall',
        ]


@adapter(IProfileImportedEvent)
def handle_profile_imported_event(event):
    """Update 'last version for profile' after a full import."""
    if event.profile_id == 'profile-plone.app.upgrade.v50:to50alpha3':
        setup = api.portal.get_tool(name='portal_setup')
        setup.runAllImportStepsFromProfile(config.INSTALL_PROFILE)
