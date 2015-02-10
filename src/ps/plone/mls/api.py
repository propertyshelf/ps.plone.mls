# -*- coding: utf-8 -*-
"""MLS integration api."""

# python imports
from mls.apiclient import (
    api,
    exceptions,
    resources,
)

# zope imports
from plone import api as plone_api
from plone.mls.core.api import get_settings
from zope.annotation.interfaces import IAnnotations
from zope.globalrequest import getRequest
import Globals

# local imports
from ps.plone.mls import _


def get_api(context=None, lang=None):
    """Get the API Client based on the local configuration."""
    settings = get_settings(context=context)
    base_url = settings.get('mls_site', None)
    api_key = settings.get('mls_key', None)
    debug = Globals.DevelopmentMode
    mls = api.API(base_url, api_key=api_key, lang=lang, debug=debug)
    return mls


def get_development(item_id=None, context=None, request=None, lang=None):
    """Get a single development."""
    mlsapi = get_api(context=context, lang=lang)
    try:
        item = Development.get(mlsapi, item_id)
    except exceptions.ServerError:
        if not plone_api.user.is_anonymous():
            message = _(
                u'An error occured trying to connect to the '
                u'configured MLS. Please check your settings or try '
                u'again later.'
            )
            plone_api.portal.show_message(
                message=message,
                request=request,
                type='warning',
            )
    except exceptions.ResourceNotFound:
        message = _(
            u'The requested development was not found.'
        )
        plone_api.portal.show_message(
            message=message,
            request=request,
            type='info',
        )
    except exceptions.ConnectionError:
        pass
    else:
        return item


class Field(object):
    """Wraps the api data into a field structure."""

    def __init__(self, name, value, resource, title=None):
        self.name = name
        self.value = value
        self.title = title

        if self.title is not None:
            return

        # Try to get the correct label for the field.
        titles = resource.field_titles().get('response', {})

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
        if self.title is None:
            self.title = name


class CacheMixin(object):
    """Extend API resources to handle some caching."""
    _field_titles = None

    def _get_field_titles(self):
        """Get the translated field titles from the API endpoint."""
        return self.__class__.get_field_titles(self._api)

    def field_titles(self):
        """Get the translated field titles for that resource."""
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
            try:
                data = self._get_field_titles()
            except exceptions.ResourceNotFound:
                data = {}
            else:
                cache[key] = data
                self._field_titles = data
        else:
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


class Agency(CacheMixin, resources.Agent):
    """'Agency' entity resource class with caching support."""


class Agent(CacheMixin, resources.Agent):
    """'Agent' entity resource class with caching support."""


class Development(CacheMixin, resources.Development):
    """'Development Project' entity resource class with caching support."""

    def __init__(self, api, data):
        super(Development, self).__init__(api, data)
        self.__class_agency__ = Agency
        self.__class_agent__ = Agent
        self.__class_group__ = PropertyGroup
        self.__class_phase__ = DevelopmentPhase


class DevelopmentPhase(CacheMixin, resources.DevelopmentPhase):
    """'Development Phase' entity resource class with caching support."""


class Listing(CacheMixin, resources.Listing):
    """'Listing' entity resource class with caching support."""


class PropertyGroup(CacheMixin, resources.PropertyGroup):
    """'Property Group' entity resource class with caching support."""
