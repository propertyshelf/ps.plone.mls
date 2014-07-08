# -*- coding: utf-8 -*-
"""Featured Listings Viewlet."""

# zope imports
from plone.app.layout.viewlets.common import ViewletBase
from plone.autoform import directives
from plone.directives import form
from plone.mls.listing.browser.interfaces import IListingDetails
from plone.supermodel import model
from z3c.form import button
from z3c.form.browser.multi import multiFieldWidgetFactory
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.interface import Interface, alsoProvides, noLongerProvides
from zope.traversing.browser.absoluteurl import absoluteURL

# local imports
from ps.plone.mls import _
from ps.plone.mls.interfaces import IListingTraversable


CONFIGURATION_KEY = 'ps.plone.mls.listing.featuredlistings'


class IPossibleFeaturedListings(Interface):
    """Marker interface for possible FeaturedListings viewlet."""


class IFeaturedListings(IListingTraversable):
    """Marker interface for FeaturedListings viewlet."""


class FeaturedListingsViewlet(ViewletBase):
    """Show featured MLS listings."""

    @property
    def available(self):
        return IFeaturedListings.providedBy(self.context) and \
            not IListingDetails.providedBy(self.view)

    @property
    def config(self):
        """Get view configuration data from annotations."""
        annotations = IAnnotations(self.context)
        return annotations.get(CONFIGURATION_KEY, {})


class IFeaturedListingsConfiguration(model.Schema):
    """Featured Listings Configuration Form Schema."""

    directives.widget(listing_ids=multiFieldWidgetFactory)
    listing_ids = schema.List(
        description=_(u'Add one Listing ID for each entry to show up.'),
        title=_(u'MLS Listing IDs'),
        unique=True,
        value_type=schema.TextLine(
            title=_(u'ID'),
        ),
    )


class FeaturedListingsConfiguration(form.SchemaForm):
    """Featured Listings Configuration Form."""

    schema = IFeaturedListingsConfiguration

    label = _(u'\'Featured Listings\' Configuration')
    description = _(
        u'Adjust the behaviour for this \'Featured Listings\' viewlet.'
    )

    def getContent(self):
        annotations = IAnnotations(self.context)
        return annotations.get(
            CONFIGURATION_KEY, annotations.setdefault(CONFIGURATION_KEY, {}),
        )

    @button.buttonAndHandler(_(u'Save'))
    def handle_save(self, action):
        data, errors = self.extractData()
        if not errors:
            annotations = IAnnotations(self.context)
            annotations[CONFIGURATION_KEY] = data
            self.request.response.redirect(
                absoluteURL(self.context, self.request),
            )

    @button.buttonAndHandler(_(u'Cancel'))
    def handle_cancel(self, action):
        self.request.response.redirect(absoluteURL(self.context, self.request))


class FeaturedListingsStatus(object):
    """Return activation/deactivation status of FeaturedListings viewlet."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def can_activate(self):
        return IPossibleFeaturedListings.providedBy(self.context) and \
            not IFeaturedListings.providedBy(self.context)

    @property
    def active(self):
        return IFeaturedListings.providedBy(self.context)


class FeaturedListingsToggle(object):
    """Toggle FeaturedListings viewlet for the current context."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        msg_type = 'info'

        if IFeaturedListings.providedBy(self.context):
            # Deactivate FeaturedListings viewlet.
            noLongerProvides(self.context, IFeaturedListings)
            self.context.reindexObject(idxs=['object_provides', ])
            msg = _(u'\'Featured Listings\' viewlet deactivated.')
        elif IPossibleFeaturedListings.providedBy(self.context):
            alsoProvides(self.context, IFeaturedListings)
            self.context.reindexObject(idxs=['object_provides', ])
            msg = _(u'\'Featured Listings\' viewlet activated.')
        else:
            msg = _(
                u'The \'Featured Listings\' viewlet does\'t work with this '
                u'content type. Add \'IPossibleFeaturedListings\' to the '
                u'provided interfaces to enable this feature.'
            )
            msg_type = 'error'

        self.context.plone_utils.addPortalMessage(msg, msg_type)
        self.request.response.redirect(self.context.absolute_url())
