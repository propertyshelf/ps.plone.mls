# -*- coding: utf-8 -*-
"""Custom wrapper for collective.jsonify."""

from collective.jsonify.methods import _clean_dict
from collective.jsonify.methods import get_catalog_results  # noqa: F401
from collective.jsonify.methods import get_children  # noqa: F401
from collective.jsonify.wrapper import Wrapper
from ps.plone.mls import config
from zope.annotation.interfaces import IAnnotations

import pprint
import sys
import traceback


try:
    import simplejson as json
except ImportError:
    import json


def get_item(self):
    """Get information about an item."""

    try:
        context_dict = MLSWrapper(self)
    except Exception, e:
        etype = sys.exc_info()[0]
        tb = pprint.pformat(traceback.format_tb(sys.exc_info()[2]))
        return 'ERROR: exception wrapping object: {0}: {1}\n{2}'.format(
            etype, str(e), tb,
        )

    passed = False
    while not passed:
        try:
            JSON = json.dumps(context_dict)
            passed = True
        except Exception, error:
            if 'serializable' in str(error):
                key, context_dict = _clean_dict(context_dict, error)
                pprint.pprint(
                    'Not serializable member {0} of {1} ignored'.format(
                        key, repr(self),
                    ),
                )
                passed = False
            else:
                return ('ERROR: Unknown error serializing object: {0}'.format(
                    error,
                ))
    self.REQUEST.response.setHeader('Content-type', 'application/json')
    return JSON


class MLSWrapper(Wrapper):
    """Wrapper for MLS embedding objects."""

    def __init__(self, context):
        super(MLSWrapper, self).__init__(context)
        self.get_mls_configuration()

    def get_mls_configuration(self):
        try:
            annotations = IAnnotations(self.context)
        except Exception:
            return

        self['_mlsconfig'] = {}

        config_items = [
            config.SETTINGS_DEVELOPMENT_COLLECTION,
            config.SETTINGS_LISTING_COLLECTION,
            config.SETTINGS_LISTING_FEATURED,
            config.SETTINGS_LISTING_RECENT,
            config.SETTINGS_LISTING_SEARCH,
            config.SETTINGS_LISTING_SEARCH_BANNER,
            config.SETTINGS_LOCAL_AGENCY,
            config.SETTINGS_LOCAL_MLS,
        ]

        for item in config_items:
            settings = annotations.get(item, {})
            if settings:
                self['_mlsconfig'][item] = settings
