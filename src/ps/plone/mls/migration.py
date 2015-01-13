# -*- coding: utf-8 -*-
"""Migration steps for ps.plone.mls."""

# zope imports
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import getUtility


PROFILE_ID = 'profile-ps.plone.mls:default'


def migrate_to_1001(context):
    """Migrate from 1000 to 1001.

    * Activate portal actions.
    """
    site = getUtility(IPloneSiteRoot)
    setup = getToolByName(site, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'actions')
