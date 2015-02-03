# -*- coding: utf-8 -*-
"""MLS integration api."""

# zope imports
from mls.apiclient import api, resources
from plone.mls.core.api import get_settings
from zope.annotation.interfaces import IAnnotations
from zope.globalrequest import getRequest
import Globals


def get_api(context=None, lang=None):
    """Get the API Client based on the local configuration."""
    settings = get_settings(context=context)
    base_url = settings.get('mls_site', None)
    api_key = settings.get('mls_key', None)
    debug = Globals.DevelopmentMode
    mls = api.API(base_url, api_key=api_key, lang=lang, debug=debug)
    return mls


class Field(object):
    """Wraps the api data into a field structure."""

    def __init__(self, name, value, resource, title=None):
        self.name = name
        self.value = value
        self.title = title

        if self.title is not None:
            return

        # Try to get the correct label for the field.
        titles = resource.field_titles().get('response')

        try:
            self.title = titles['fields'][name]
        except (KeyError, TypeError):
            pass
        else:
            return

        group_fields = titles.get('group_fields', [])
        for group in group_fields:
            try:
                self.title = group_fields[group][name]
            except (KeyError, TypeError):
                continue
            else:
                break


class CacheMixin(object):
    """Extend API resources to handle some caching."""
    _field_titles = None

    def _get_field_titles(self):
        """"""
        return self.__class__.get_field_titles(self._api)

    def field_titles(self):
        """"""
        if self._field_titles is not None:
            return self._field_titles

        request = getRequest()
        key = 'cache-{0}-{1}-{2}'.format(
            self.__class__.__name__,
            self._api.base_url,
            self._api.lang,
        )
        cache = IAnnotations(request)
        data = cache.get(key, None)
        if not data:
            data = self._get_field_titles()
            cache[key] = data
        self._field_titles = data
        return data

    def __getattr__(self, name):
        """Returns a data attribute or raises AttributeError.

        This version wraps the return value into a Field class for better
        access in Plone.
        """
        try:
            value = self._data[name]
        except KeyError:
            return object.__getattribute__(self, name)
        else:
            if value is not None:
                return Field(name, value, self)


class Agent(CacheMixin, resources.Agent):
    """'Agent' entity resource class with caching support."""


class Development(CacheMixin, resources.Development):
    """'Development Project' entity resource class with caching support."""

    def __init__(self, api, data):
        super(Development, self).__init__(api, data)
        self.__class_agent__ = Agent
        self.__class_group__ = PropertyGroup
        self.__class_phase__ = DevelopmentPhase


class DevelopmentPhase(CacheMixin, resources.DevelopmentPhase):
    """'Development Phase' entity resource class with caching support."""


class Listing(CacheMixin, resources.Listing):
    """'Listing' entity resource class with caching support."""


class PropertyGroup(CacheMixin, resources.PropertyGroup):
    """'Property Group' entity resource class with caching support."""
