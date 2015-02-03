# -*- coding: utf-8 -*-
"""Custom traversers for MLS Embedding items."""

# zope imports
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter, queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import (
    IBrowserPublisher,
    IBrowserRequest,
)

# local imports
from ps.plone.mls import api
from ps.plone.mls.content import featured
from ps.plone.mls.interfaces import (
    IDevelopmentTraversable,
    IListingTraversable,
)


@implementer(IBrowserPublisher)
class MLSItemTraverser(DefaultPublishTraverse):
    """Custom Traverser for MLS Embedding items.

    The traverser looks for a MLS item id in the traversal stack and
    tries to call the corresponding details view. But before it does so, it
    tries to call all (currently) known traversers.

    It also does a check on the MLS item id. By default this one returns
    ``True``. But a subclass can override it to only return items
    that match a given condition.
    """

    detail_view_name = None
    item_id = 'item_id'

    def _lookup_add_on_traverser(self):
        """Call 3rd party traversers."""
        traverser_class = None
        try:
            from plone.app.imaging.traverse import ImageTraverser
        except ImportError:
            pass
        else:
            traverser_class = ImageTraverser

        try:
            from collective.contentleadimage.extender import LeadImageTraverse
        except ImportError:
            pass
        else:
            if not traverser_class:
                traverser_class = LeadImageTraverse

        return traverser_class

    def check_item(self, item_id):
        """Check if the MLS item with given ID is available."""
        return True

    def publishTraverse(self, request, name):
        """See zope.publisher.interfaces.IPublishTraverse"""

        # Try to deliver the default content views.
        try:
            return super(MLSItemTraverser, self).publishTraverse(
                request, name,
            )
        except (NotFound, AttributeError):
            pass

        traverser_class = self._lookup_add_on_traverser()
        if traverser_class is not None:
            try:
                traverser = traverser_class(self.context, self.request)
                return traverser.publishTraverse(request, name)
            except (NotFound, AttributeError):
                pass

        name = name.split('___')[0]

        if not self.check_item(name):
            raise NotFound(self.context, name, request)

        # We store the item_id parameter in the request.
        setattr(self.request, self.item_id, name)
        self.post_lookup(name)
        if len(self.request.path) > 0:
            detail_view = self.request.path.pop()
            if detail_view.startswith('@@'):
                detail_view = detail_view[2:]
        else:
            detail_view = self.detail_view_name
        default_view = self.context.getDefaultLayout()

        # Let's call the listing view.
        view = queryMultiAdapter(
            (self.context, request), name=detail_view,
        )
        if view is not None:
            return view

        # Deliver the default item view as fallback.
        view = queryMultiAdapter(
            (self.context, request), name=default_view,
        )
        if view is not None:
            return view

        raise NotFound(self.context, name, request)

    def post_lookup(self, item_id):
        """"""
        pass


@adapter(
    IDevelopmentTraversable,
    IBrowserRequest,
)
class DevelopmentTraverser(MLSItemTraverser):
    """Custom Traverser for Developments.

    See ``MLSItemTraverser`` for details.
    """
    __used_for__ = IDevelopmentTraversable
    detail_view_name = 'development-detail'
    item_id = 'development_id'

    def post_lookup(self, item_id):
        portal_state = queryMultiAdapter(
            (self.context, self.request),
            name='plone_portal_state',
        )
        lang = portal_state.language()
        item = api.get_development(
            item_id=item_id,
            context=self.context,
            request=self.request,
            lang=lang,
        )
        if item is not None:
            cache = IAnnotations(self.request)
            cache['ps.plone.mls.development.traversed'] = item


@adapter(
    IListingTraversable,
    IBrowserRequest,
)
class ListingTraverser(MLSItemTraverser):
    """Custom Traverser for Listings.

    See ``MLSItemTraverser`` for details.
    """
    __used_for__ = IListingTraversable
    detail_view_name = 'listing-detail'
    item_id = 'listing_id'


@adapter(
    featured.IFeaturedListings,
    IBrowserRequest,
)
class FeaturedListingsTraverser(ListingTraverser):
    """Traverser for featured listings.

    It only allows listing ids which are defined in the context.
    """
    __used_for__ = featured.IFeaturedListings

    def check_item(self, item_id):
        """Check if the listing ID is available."""
        return item_id in self.context.listing_ids
