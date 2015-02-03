# -*- coding: utf-8 -*-
"""MLS development detail view."""

# python imports
import logging

# zope imports
from Products.Five import BrowserView
from plone.mls.listing.interfaces import IMLSUISettings
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility, queryMultiAdapter
from zope.interface import implementer

# local imports
from ps.plone.mls import api, config
from ps.plone.mls.interfaces import IDevelopmentDetails

logger = logging.getLogger(config.PROJECT_NAME)

MAP_JS = """
function initializeMap() {{
    var center = new google.maps.LatLng({lat}, {lng})
    var myOptions = {{
        zoom: {zoom},
        center: center,
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        mapTypeControl: true,
        disableDoubleClickZoom: true,
        streetViewControl: true
    }}

    var map = new google.maps.Map(
        document.getElementById('{map_id}'),
        myOptions
    );

    var has_marker = true;
    if(has_marker) {{
        var myLatlng = new google.maps.LatLng({lat}, {lng});
        var marker = new google.maps.Marker({{
            position: myLatlng,
            map: map
        }});
    }}
    return map;
}};

map = initializeMap();
google.maps.event.addDomListener(window, "resize", function() {{
    var center = map.getCenter();
    google.maps.event.trigger(map, "resize");
    map.setCenter(center);
}});

"""


@implementer(IDevelopmentDetails)
class DevelopmentDetails(BrowserView):
    """Detail view for MLS developments."""

    _item = None

    @property
    def item(self):
        if self._item is None:
            self._item = self._get_item()
        return self._item

    def _get_item(self):
        self.registry = getUtility(IRegistry)

        cache = IAnnotations(self.request)
        item = cache.get('ps.plone.mls.development.traversed', None)

        if item is None:
            item_id = getattr(self.request, 'development_id', None)
            if not item_id:
                return

            self.portal_state = queryMultiAdapter(
                (self.context, self.request),
                name='plone_portal_state',
            )
            lang = self.portal_state.language()
            item = api.get_development(
                item_id=item_id,
                context=self.context,
                request=self.request,
                lang=lang,
            )

        return item

    @property
    def map_id(self):
        """Generate a unique css id for the map."""
        try:
            item_id = self.item.id.value
        except:
            item_id = 'unknown'
        return u'map__{0}'.format(item_id)

    def javascript_map(self):
        """Return the JS code for the map."""
        if not hasattr(self.item, 'geolocation'):
            return
        lat, lng = self.item.geolocation.value.split(',')
        return MAP_JS.format(
            lat=lat,
            lng=lng,
            map_id=self.map_id,
            zoom=7,
        )

    def use_fotorama(self):
        if self.registry is not None:
            try:
                settings = self.registry.forInterface(IMLSUISettings)
            except:
                logger.warning('MLS UI settings not available.')
            else:
                return getattr(settings, 'slideshow') == u'fotorama'
        return False

    def use_galleria(self):
        if self.registry is not None:
            try:
                settings = self.registry.forInterface(IMLSUISettings)
            except:
                logger.warning('MLS UI settings not available.')
            else:
                return getattr(settings, 'slideshow') == u'galleria'
        # Fallback: 'galleria' is the default.
        return True

    def titles_for_phases(self):
        """Get the titles for the Development Phase fields."""
        fake = api.DevelopmentPhase(self.item._api, {})
        raw = fake.field_titles()
        return raw.get('response', {}).get('fields', {})

    def titles_for_groups(self):
        """Get the titles for the Property Group fields."""
        fake = api.PropertyGroup(self.item._api, {})
        raw = fake.field_titles()
        return raw.get('response', {}).get('fields', {})
