# -*- coding: utf-8 -*-
"""Listing search banner."""

# zope imports
# from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.directives import form
from plone.supermodel.directives import fieldset
from zope import schema
from zope.annotation.interfaces import IAnnotations

# local imports
from ps.plone.mls import (
    _,
    config,
)

FIELDS_SECTION_1 = [
    'section_1_search_target',
    'section_1_title',
    'section_1_categories',
    'section_1_default_category',
    'section_1_hide_categories',
    'section_1_hide_section',
]
FIELDS_SECTION_2 = [
    'section_2_search_target',
    'section_2_title',
    'section_2_categories',
    'section_2_default_category',
    'section_2_hide_categories',
    'section_2_hide_section',
]
FIELDS_SECTION_3 = [
    'section_3_search_target',
    'section_3_title',
    'section_3_categories',
    'section_3_default_category',
    'section_3_hide_categories',
    'section_3_hide_section',
]
FIELDS_SECTION_4 = [
    'section_4_search_target',
    'section_4_title',
    'section_4_categories',
    'section_4_default_category',
    'section_4_hide_categories',
    'section_4_hide_section',
]

LABEL_SECTION_SEARCH_PAGE = _(u'Search Target Page')
LABEL_SECTION_TITLE = _(u'Title')
LABEL_SECTION_CATEGORIES = _(u'Categories')
LABEL_SECTION_DEFAULT_CATEGORY = _(u'Default Category')
LABEL_SECTION_HIDE_CATEGORY = _(u'Hide category')
LABEL_SECTION_HIDE_SECTION = _(u'Hide section')

DESCRIPTION_SECTION_SEARCH_PAGE = _(
    u'Find the search page which will be used to show the results.'
)
DESCRIPTION_SECTION_TITLE = _(u'')
DESCRIPTION_SECTION_CATEGORIES = _(u'')
DESCRIPTION_SECTION_DEFAULT_CATEGORY = _(u'')
DESCRIPTION_SECTION_HIDE_CATEGORY = _(
    u'Hide the category field and use default setting.'
)
DESCRIPTION_SECTION_HIDE_SECTION = _(
    u'Don\'t show this section at all.'
)

DEFAULT_CATEGORIES_1 = (
    u'all:All:\n'
    u'houses:Houses:listing_type=rs&object_type=house,mobile,multiplex,'
    u'townhouse,freestanding_villa\n'
    u'condos:Condos:listing_type=rs&object_type=apartment,condominium,'
    u'half_duplex\n'
    u'land:Land:listing_type=ll\n'
    u'commercial:Commercial:listing_type=cs&object_type=\n'
)

DEFAULT_CATEGORIES_2 = (
    u'all:All:\n'
    u'houses:Houses:listing_type=rl&object_type=house,mobile,multiplex,'
    u'townhouse,freestanding_villa\n'
    u'condos:Condos:listing_type=rs&object_type=apartment,condominium,'
    u'half_duplex\n'
    u'commercial:Commercial:listing_type=cl&object_type=\n'
)


class ISearchBannerConfiguration(form.Schema):
    """Listing Search Banner Configuration Form."""

    fieldset('section_1', label=_(u'Section 1'), fields=FIELDS_SECTION_1)
    fieldset('section_2', label=_(u'Section 2'), fields=FIELDS_SECTION_2)
    fieldset('section_3', label=_(u'Section 3'), fields=FIELDS_SECTION_3)
    fieldset('section_4', label=_(u'Section 4'), fields=FIELDS_SECTION_4)

    section_1_search_target = schema.Choice(
        description=DESCRIPTION_SECTION_SEARCH_PAGE,
        required=False,
        vocabulary='ps.plone.mls.listings.available_searches',
        title=LABEL_SECTION_SEARCH_PAGE,
    )

    section_1_title = schema.TextLine(
        default=_(u'Buy'),
        description=DESCRIPTION_SECTION_TITLE,
        required=False,
        title=LABEL_SECTION_TITLE,
    )

    form.widget('section_1_categories', rows=6)
    section_1_categories = schema.Text(
        default=DEFAULT_CATEGORIES_1,
        description=DESCRIPTION_SECTION_CATEGORIES,
        required=False,
        title=LABEL_SECTION_CATEGORIES,
    )

    section_1_default_category = schema.TextLine(
        default=u'houses',
        description=DESCRIPTION_SECTION_DEFAULT_CATEGORY,
        required=False,
        title=LABEL_SECTION_DEFAULT_CATEGORY,
    )

    section_1_hide_categories = schema.Bool(
        description=DESCRIPTION_SECTION_HIDE_CATEGORY,
        required=False,
        title=LABEL_SECTION_HIDE_CATEGORY,
    )

    section_1_hide_section = schema.Bool(
        description=DESCRIPTION_SECTION_HIDE_SECTION,
        required=False,
        title=LABEL_SECTION_HIDE_SECTION,
    )

    section_2_search_target = schema.Choice(
        description=DESCRIPTION_SECTION_SEARCH_PAGE,
        required=False,
        vocabulary='ps.plone.mls.listings.available_searches',
        title=LABEL_SECTION_SEARCH_PAGE,
    )

    section_2_title = schema.TextLine(
        default=_(u'Rent'),
        description=DESCRIPTION_SECTION_TITLE,
        required=False,
        title=LABEL_SECTION_TITLE,
    )

    form.widget('section_2_categories', rows=6)
    section_2_categories = schema.Text(
        default=DEFAULT_CATEGORIES_2,
        description=DESCRIPTION_SECTION_CATEGORIES,
        required=False,
        title=LABEL_SECTION_CATEGORIES,
    )

    section_2_default_category = schema.TextLine(
        default=u'houses',
        description=DESCRIPTION_SECTION_DEFAULT_CATEGORY,
        required=False,
        title=LABEL_SECTION_DEFAULT_CATEGORY,
    )

    section_2_hide_categories = schema.Bool(
        description=DESCRIPTION_SECTION_HIDE_CATEGORY,
        required=False,
        title=LABEL_SECTION_HIDE_CATEGORY,
    )

    section_2_hide_section = schema.Bool(
        description=DESCRIPTION_SECTION_HIDE_SECTION,
        required=False,
        title=LABEL_SECTION_HIDE_SECTION,
    )

    section_3_search_target = schema.Choice(
        description=DESCRIPTION_SECTION_SEARCH_PAGE,
        required=False,
        vocabulary='ps.plone.mls.listings.available_searches',
        title=LABEL_SECTION_SEARCH_PAGE,
    )

    section_3_title = schema.TextLine(
        description=DESCRIPTION_SECTION_TITLE,
        required=False,
        title=LABEL_SECTION_TITLE,
    )

    form.widget('section_3_categories', rows=6)
    section_3_categories = schema.Text(
        description=DESCRIPTION_SECTION_CATEGORIES,
        required=False,
        title=LABEL_SECTION_CATEGORIES,
    )

    section_3_default_category = schema.TextLine(
        description=DESCRIPTION_SECTION_DEFAULT_CATEGORY,
        required=False,
        title=LABEL_SECTION_DEFAULT_CATEGORY,
    )

    section_3_hide_categories = schema.Bool(
        description=DESCRIPTION_SECTION_HIDE_CATEGORY,
        required=False,
        title=LABEL_SECTION_HIDE_CATEGORY,
    )

    section_3_hide_section = schema.Bool(
        default=True,
        description=DESCRIPTION_SECTION_HIDE_SECTION,
        required=False,
        title=LABEL_SECTION_HIDE_SECTION,
    )

    section_4_search_target = schema.Choice(
        description=DESCRIPTION_SECTION_SEARCH_PAGE,
        required=False,
        vocabulary='ps.plone.mls.listings.available_searches',
        title=LABEL_SECTION_SEARCH_PAGE,
    )

    section_4_title = schema.TextLine(
        description=DESCRIPTION_SECTION_TITLE,
        required=False,
        title=LABEL_SECTION_TITLE,
    )

    form.widget('section_4_categories', rows=6)
    section_4_categories = schema.Text(
        description=DESCRIPTION_SECTION_CATEGORIES,
        required=False,
        title=LABEL_SECTION_CATEGORIES,
    )

    section_4_default_category = schema.TextLine(
        description=DESCRIPTION_SECTION_DEFAULT_CATEGORY,
        required=False,
        title=LABEL_SECTION_DEFAULT_CATEGORY,
    )

    section_4_hide_categories = schema.Bool(
        description=DESCRIPTION_SECTION_HIDE_CATEGORY,
        required=False,
        title=LABEL_SECTION_HIDE_CATEGORY,
    )

    section_4_hide_section = schema.Bool(
        default=True,
        description=DESCRIPTION_SECTION_HIDE_SECTION,
        required=False,
        title=LABEL_SECTION_HIDE_SECTION,
    )


class SearchBannerConfiguration(form.SchemaForm):
    """Listing Search Banner Configuration Form."""

    schema = ISearchBannerConfiguration
    label = _(u'\'Listing Search Banner\' Configuration')
    description = _(
        u'Adjust the behaviour for this \'Listing Search Banner\'.'
    )

    def getContent(self):
        annotations = IAnnotations(self.context)
        return annotations.get(
            config.SETTINGS_LISTING_SEARCH_BANNER,
            annotations.setdefault(config.SETTINGS_LISTING_SEARCH_BANNER, {})
        )