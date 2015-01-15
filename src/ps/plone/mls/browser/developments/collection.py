# -*- coding: utf-8 -*-
"""MLS development collection."""

# zope imports
from plone.app.layout.viewlets.common import ViewletBase
from plone.directives import form
from plone.memoize.view import memoize
from plone.mls.core.navigation import ListingBatch
from z3c.form import field, button
# from z3c.form.browser import checkbox
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import queryMultiAdapter
from zope.interface import Interface, alsoProvides, noLongerProvides
from zope.traversing.browser.absoluteurl import absoluteURL

# local imports
# from plone.mls.core.navigation import ListingBatch
# from plone.mls.listing.api import prepare_search_params, search
# from plone.mls.listing.browser.interfaces import (
#     # IBaseListingItems,
#     # IListingDetails,
# )
from ps.plone.mls import _, api
from ps.plone.mls.interfaces import (
    IDevelopmentCollection,
    IDevelopmentDetails,
    IPossibleDevelopmentCollection,
)


CONFIGURATION_KEY = 'ps.plone.mls.developmentcollection'


class DevelopmentCollectionViewlet(ViewletBase):
    """Dynamic collection of MLS developments."""

    _items = None
    _batching = None
    _fields = None

    @property
    def available(self):
        return IDevelopmentCollection.providedBy(self.context) and \
            not IDevelopmentDetails.providedBy(self.view)

    @property
    def config(self):
        """Get view configuration data from annotations."""
        annotations = IAnnotations(self.context)
        return annotations.get(CONFIGURATION_KEY, {})

    def update(self):
        """Prepare view related data."""
        super(DevelopmentCollectionViewlet, self).update()
        self.context_state = queryMultiAdapter(
            (self.context, self.request), name='plone_context_state',
        )

        self.limit = self.config.get('limit', 5)
        self._get_items()

    @property
    @memoize
    def items(self):
        return self._items

    def _get_items(self):
        lang = self.portal_state.language()
        mlsapi = api.get_api(context=self.context, lang=lang, debug=True)
        params = {
            'summary': '1',
            'limit': self.limit,
            'offset': self.request.get('b_start', 0),
        }
        try:
            result = api.Development.search(mlsapi, params=params)
        except:
            pass
        else:
            self._items = result.get_items()
            headers = result.get_headers()
            self._batching = {
                'results': headers.get('CountTotal'),
            }
            self._fields = result.get_field_titles(mlsapi)

    @memoize
    def view_url(self):
        """Generate view url."""
        if not self.context_state.is_view_template():
            return self.context_state.current_base_url()
        else:
            return absoluteURL(self.context, self.request) + '/'

    @property
    def batching(self):
        return ListingBatch(
            self.items,
            self.limit,
            self.request.get('b_start', 0),
            orphan=1,
            batch_data=self._batching,
        )


class IDevelopmentCollectionConfiguration(Interface):
    """Development Collection Configuration Form."""

    # agency_listings = schema.Bool(
    #     description=_(
    #         u'If activated, only listings of the configured agency are '
    #         u'shown.',
    #     ),
    #     required=False,
    #     title=_(u'Agency Listings'),
    # )

    # listing_type = schema.Tuple(
    #     default=('cl', 'cs', 'll', 'rl', 'rs', ),
    #     required=False,
    #     title=_(u'Listing Type'),
    #     value_type=schema.Choice(
    #         source='plone.mls.listing.ListingTypes'
    #     ),
    # )

    # location_state = schema.Choice(
    #     required=False,
    #     title=_(u'State'),
    #     source='plone.mls.listing.LocationStates',
    # )

    # location_county = schema.Choice(
    #     required=False,
    #     title=_(u'County'),
    #     source='plone.mls.listing.LocationCounties',
    # )

    # location_district = schema.Choice(
    #     required=False,
    #     title=_(u'District'),
    #     source='plone.mls.listing.LocationDistricts',
    # )

    # price_min = schema.Int(
    #     required=False,
    #     title=_(u'Price (Min)'),
    # )

    # price_max = schema.Int(
    #     required=False,
    #     title=_(u'Price (Max)'),
    # )

    # location_type = schema.Tuple(
    #     required=False,
    #     title=_(u'Location Type'),
    #     value_type=schema.Choice(
    #         source='plone.mls.listing.LocationTypes'
    #     ),
    # )

    # geographic_type = schema.Tuple(
    #     required=False,
    #     title=_(u'Geographic Type'),
    #     value_type=schema.Choice(
    #         source='plone.mls.listing.GeographicTypes'
    #     ),
    # )

    # view_type = schema.Tuple(
    #     required=False,
    #     title=_(u'View Type'),
    #     value_type=schema.Choice(
    #         source='plone.mls.listing.ViewTypes'
    #     ),
    # )

    # object_type = schema.Tuple(
    #     required=False,
    #     title=_(u'Object Type'),
    #     value_type=schema.Choice(
    #         source='plone.mls.listing.ObjectTypes'
    #     ),
    # )

    # ownership_type = schema.Tuple(
    #     required=False,
    #     title=_(u'Ownership Type'),
    #     value_type=schema.Choice(
    #         source='plone.mls.listing.OwnershipTypes'
    #     ),
    # )

    limit = schema.Int(
        default=5,
        required=False,
        title=_(u'Items per Page'),
    )


class DevelopmentCollectionConfiguration(form.Form):
    """Development Collection Configuration Form."""

    fields = field.Fields(IDevelopmentCollectionConfiguration)
    # fields['geographic_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    # fields['listing_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    # fields['location_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    # fields['object_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    # fields['ownership_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    # fields['view_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    label = _(u'\'Development Collection\' Configuration')
    description = _(
        u'Adjust the behaviour for this \'Development Collection\' viewlet.'
    )

    def getContent(self):
        annotations = IAnnotations(self.context)
        return annotations.get(
            CONFIGURATION_KEY, annotations.setdefault(CONFIGURATION_KEY, {})
        )

    @button.buttonAndHandler(_(u'Save'))
    def handle_save(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        annotations = IAnnotations(self.context)
        annotations[CONFIGURATION_KEY] = data
        self.request.response.redirect(absoluteURL(self.context, self.request))

    @button.buttonAndHandler(_(u'Cancel'))
    def handle_cancel(self, action):
        self.request.response.redirect(absoluteURL(self.context, self.request))


class DevelopmentCollectionStatus(object):
    """Return activation/deactivation status of the viewlet."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def can_activate(self):
        return IPossibleDevelopmentCollection.providedBy(self.context) and \
            not IDevelopmentCollection.providedBy(self.context)

    @property
    def active(self):
        return IDevelopmentCollection.providedBy(self.context)


class DevelopmentCollectionToggle(object):
    """Toggle DevelopmentCollection viewlet for the current context."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        msg_type = 'info'

        if IDevelopmentCollection.providedBy(self.context):
            # Deactivate DevelopmentCollection viewlet.
            noLongerProvides(self.context, IDevelopmentCollection)
            self.context.reindexObject(idxs=['object_provides', ])
            msg = _(u'\'Development Collection\' viewlet deactivated.')
        elif IPossibleDevelopmentCollection.providedBy(self.context):
            alsoProvides(self.context, IDevelopmentCollection)
            self.context.reindexObject(idxs=['object_provides', ])
            msg = _(u'\'Development Collection\' viewlet activated.')
        else:
            msg = _(
                u'The \'Development Collection\' viewlet does\'t work with '
                u'this content type. Add \'IPossibleDevelopmentCollection\' '
                u'to the provided interfaces to enable this feature.'
            )
            msg_type = 'error'

        self.context.plone_utils.addPortalMessage(msg, msg_type)
        self.request.response.redirect(self.context.absolute_url())
