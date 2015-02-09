# -*- coding: utf-8 -*-
"""MLS development detail view."""

# python imports
from email import message_from_string
import json
import logging

# zope imports
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as PMF
from Products.Five import BrowserView
from plone.directives import form
from plone.mls.listing.interfaces import IMLSUISettings
from plone.registry.interfaces import IRegistry
from plone.z3cform import z2
from z3c.form import (
    button,
    field,
)
from z3c.form.interfaces import (
    # HIDDEN_MODE,
    IFormLayer,
)
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import (
    getUtility,
    queryMultiAdapter,
)
from zope.interface import (
    alsoProvides,
    implementer,
)

# starting from 0.6.0 version plone.z3cform has IWrappedForm interface
try:
    from plone.z3cform.interfaces import IWrappedForm
    HAS_WRAPPED_FORM = True
except ImportError:
    HAS_WRAPPED_FORM = False

# local imports
from ps.plone.mls import (
    api,
    config,
    utils,
)
from ps.plone.mls.interfaces import IDevelopmentDetails


logger = logging.getLogger(config.PROJECT_NAME)

EMAIL_TEMPLATE = """
Enquiry from: {name} <{sender_from_address}>
Development URL: {url}

Message:
{message}
"""


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
            map: map,
            icon: {icon}
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


class IContactForm(form.Schema):
    """Contact Form schema."""

    name = schema.TextLine(
        description=PMF(
            u'help_sender_fullname',
            default=u'Please enter your full name',
        ),
        required=True,
        title=PMF(u'label_name', default=u"Name"),
    )

    sender_from_address = schema.TextLine(
        constraint=utils.validate_email,
        description=PMF(
            u'help_sender_from_address',
            default=u'Please enter your e-mail address',
        ),
        required=True,
        title=PMF(u'label_sender_from_address', default=u'E-Mail'),
    )

    subject = schema.TextLine(
        required=True,
        title=PMF(u'label_subject', default=u'Subject')
    )

    message = schema.Text(
        constraint=utils.contains_nuts,
        description=PMF(
            u'help_message',
            default=u'Please enter the message you want to send.',
        ),
        max_length=1000,
        required=True,
        title=PMF(u'label_message', default=u'Message'),
    )


class ContactForm(form.Form):
    """Contact Form."""
    fields = field.Fields(IContactForm)
    ignoreContext = True
    method = 'post'
    _email_sent = False

    def __init__(self, context, request, info=None):
        super(ContactForm, self).__init__(context, request)
        self.item_info = info

    @property
    def already_sent(self):
        return self._email_sent

    def updateWidgets(self):
        super(ContactForm, self).updateWidgets()
        # urltool = getToolByName(self.context, 'portal_url')
        # portal = urltool.getPortalObject()
        # subject = u'{portal_title}: {title} ({lid})'.format(
        #     lid=self.listing_info['listing_id'],
        #     portal_title=portal.getProperty('title').decode('utf-8'),
        #     title=self.listing_info['listing_title'],
        # )
        # self.widgets['subject'].mode = HIDDEN_MODE
        # self.widgets['subject'].value = subject

    @button.buttonAndHandler(PMF(u'label_send', default='Send'), name='send')
    def handle_send(self, action):
        """Send button for sending the email."""
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if not self.already_sent:
            self.send_email(data)
            self._email_sent = True
        return

    def send_email(self, data):
        mailhost = getToolByName(self.context, 'MailHost')
        urltool = getToolByName(self.context, 'portal_url')
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')

        # Construct and send a message.
        from_address = portal.getProperty('email_from_address')
        from_name = portal.getProperty('email_from_name')
        if from_name is not None:
            from_address = '{0} <{1}>'.format(from_name, from_address)

        try:
            agent = self.listing_info['agent']
            rcp = agent.get('agent_email').get('value')
        except:
            rcp = from_address
        sender = '{0} <{1}>'.format(data['name'], data['sender_from_address'])
        subject = data['subject']
        data['url'] = self.request.getURL()
        message = EMAIL_TEMPLATE.format(**data)
        message = message_from_string(message.encode(email_charset))
        message['To'] = rcp
        message['From'] = from_address
        message['Reply-to'] = sender
        message['Subject'] = subject

        mailhost.send(message, immediate=True, charset=email_charset)
        return


@implementer(IDevelopmentDetails)
class DevelopmentDetails(BrowserView):
    """Detail view for MLS developments."""

    _item = None
    _contact_form = None

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
        icon = getattr(self.item, 'icon', None)
        if icon is not None:
            icon = icon.value
        icon_url = json.dumps(icon)
        lat, lng = self.item.geolocation.value.split(',')
        return MAP_JS.format(
            icon=icon_url,
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

    def contact_form(self):
        if self._contact_form is not None:
            return self._contact_form

        item_info = {}
        z2.switch_on(self, request_layer=IFormLayer)
        self._contact_form = ContactForm(
            aq_inner(self.context),
            self.request,
            item_info,
        )
        if HAS_WRAPPED_FORM:
            alsoProvides(self._contact_form, IWrappedForm)
        return self._contact_form
