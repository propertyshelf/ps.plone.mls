# -*- coding: utf-8 -*-
"""MLS development detail view."""

# python imports
from mls.apiclient.exceptions import ConnectionError

# zope imports
from Products.Five import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.component import queryMultiAdapter
from zope.interface import implementer

# local imports
from ps.plone.mls import api
from ps.plone.mls.interfaces import IDevelopmentDetails

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

    item = None

    def __init__(self, context, request):
        super(DevelopmentDetails, self).__init__(context, request)
        self.update()

    def update(self):
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
            mlsapi = api.get_api(context=self.context, lang=lang)
            try:
                item = api.Development.get(mlsapi, item_id)
            except ConnectionError:
                pass
        self.item = item

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
