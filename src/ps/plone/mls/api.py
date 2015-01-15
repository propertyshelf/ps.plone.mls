# -*- coding: utf-8 -*-
"""MLS integration api."""

# zope imports
from mls.apiclient import api, resources
from plone.mls.core.api import get_settings


def get_api(context=None, lang=None, debug=None):
    """Get the API Client based on the local configuration."""
    settings = get_settings(context=context)
    base_url = settings.get('mls_site', None)
    api_key = settings.get('mls_key', None)
    mls = api.API(base_url, api_key=api_key, lang=lang, debug=debug)
    return mls


class Field(object):
    """Wraps the api data into a field structure."""

    def __init__(self, name, value, resource):
        self.name = name
        self.value = value
        self.title = name

        # Try to get the correct label for the field.
        titles = resource.field_titles().get('response')
        for category in ['fields', 'group_fields']:
            try:
                self.title = titles[category][name]
            except (KeyError, TypeError):
                continue
            else:
                break


class CacheMixin(object):
    """Extend API resources to handle some caching."""
    _field_titles = None

    def field_titles(self):
        """"""
        if self._field_titles is None:
            self._field_titles = self.__class__.get_field_titles(self._api)
        return self._field_titles

    def __getattr__(self, name):
        """Returns a data attribute or raises AttributeError.

        This version wraps the return value into a Field class for better
        access in Plone.
        """
        try:
            return Field(name, self._data[name], self)
        except KeyError:
            return object.__getattribute__(self, name)


class Development(CacheMixin, resources.Development):
    """'Development Project' entity resource class with caching support."""
