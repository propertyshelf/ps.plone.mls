# -*- coding: utf-8 -*-
"""Testing utilities."""

# python imports
from mls.apiclient import testing
from mls.apiclient.tests import utils
import os


def _register(endpoint, content=None, fixture=None, params=None):
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'fixtures',
    )
    return testing._register(
        endpoint,
        content=content,
        path=path,
        fixture=fixture,
        params=params,
    )


def setup_plone_mls_fixtures():
    """Setup the test fixtures for integration tests."""
    utils.setup_listing_api_fixtures()

    # register all the field endpoints
    testing._register(
        'field_titles/developments',
        params=testing.BASE_PARAMS,
        fixture='field_titles-developments.json',
    )
    testing._register(
        'field_order/developments',
        params=testing.BASE_PARAMS,
        fixture='field_order-developments.json',
    )
    testing._register(
        'field_titles/property_groups',
        params=testing.BASE_PARAMS,
        fixture='field_titles-property_groups.json',
    )
    testing._register(
        'field_order/property_groups',
        params=testing.BASE_PARAMS,
        fixture='field_order-property_groups.json',
    )
    testing._register(
        'field_titles/development_phases',
        params=testing.BASE_PARAMS,
        fixture='field_titles-development_phases.json',
    )
    testing._register(
        'field_order/development_phases',
        params=testing.BASE_PARAMS,
        fixture='field_order-development_phases.json',
    )

    # register the development endpoints
    _register(
        'developments',
        params=dict(
            {
                'fields': ''.join([
                    'id,title,description,logo,location,lot_size,'
                    'location_type,number_of_listings,number_of_groups'
                ]),
                'limit': 5,
                'offset': 0,
            },
            **testing.BASE_PARAMS),
        fixture='developments.json',
    )
    _register(
        'developments',
        params=dict(
            {
                'fields': ''.join([
                    'id,title,description,logo,location,lot_size,'
                    'location_type,number_of_listings,number_of_groups,'
                    'banner_image'
                ]),
                'reverse': False,
                'modify_url': True,
                'limit': 5,
                'offset': 0,
            },
            **testing.BASE_PARAMS),
        fixture='developments_banner.json',
    )
