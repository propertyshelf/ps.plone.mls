# -*- coding: utf-8 -*-
"""Different shared utilities."""

# python imports
import re

# zope imports
from zope.interface import Invalid

# local imports
from ps.plone.mls import _


check_email = re.compile(
    r'[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)*[a-zA-Z]{2,4}').match

check_for_url = re.compile(
    r'http[s]?://').search


def validate_email(value):
    if value:
        if not check_email(value):
            raise Invalid(_(u'Invalid email address.'))
    return True


def contains_nuts(value):
    """Check for traces of nuts, like urls or other spammer fun things"""
    if value:
        if check_for_url(value):
            raise Invalid(_(u'No URLs allowed.'))
    return True


def merge_local_contact_info(settings=None, mapping=None, data=None):
    """Merge values of locally provided contact info."""
    keys_internal = [
        'force',
        'use_custom_info',
    ]

    # Clear any existing data.
    data.clear()

    for key, value in settings.items():
        if key in keys_internal:
            continue
        if value is None:
            continue
        mapped_key = mapping.get(key)
        if mapped_key is None:
            continue
        data[mapped_key] = value


def smart_truncate(content, length=160, suffix='...'):
    """Truncate a string ror some maximum length, but split at word boundary"""
    if len(content) > length:
        content = content[:length].rsplit(' ', 1)[0] + suffix
    return content
