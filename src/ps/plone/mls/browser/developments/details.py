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
from plone import api as plone_api
from plone.app.layout.viewlets.common import ViewletBase
from plone.directives import form
from plone.formwidget.captcha.widget import CaptchaFieldWidget
from plone.formwidget.captcha.validator import (
    CaptchaValidator,
    WrongCaptchaCode,
)
try:
    from plone.mls.listing.interfaces import IMLSUISettings
    HAS_UI_SETTINGS = True
except ImportError:
    HAS_UI_SETTINGS = False
from plone.registry.interfaces import IRegistry
from plone.z3cform import z2
from z3c.form import (
    button,
    field,
    validator,
)
from z3c.form.interfaces import IFormLayer
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
    _,
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
        overviewMapControl: true,
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
            default=u'',
        ),
        required=True,
        title=PMF(u'label_name', default=u"Name"),
    )

    sender_from_address = schema.TextLine(
        constraint=utils.validate_email,
        description=PMF(
            u'help_sender_from_address',
            default=u'',
        ),
        required=True,
        title=PMF(u'label_sender_from_address', default=u'E-Mail'),
    )

    message = schema.Text(
        constraint=utils.contains_nuts,
        description=PMF(
            u'help_message',
            default=u'',
        ),
        max_length=1000,
        required=True,
        title=PMF(u'label_message', default=u'Message'),
    )

    form.widget(captcha=CaptchaFieldWidget)
    captcha = schema.TextLine(
        required=True,
        title=_(u'Captcha'),
    )


class ContactForm(form.Form):
    """Contact Form."""
    fields = field.Fields(IContactForm)
    ignoreContext = True
    method = 'post'
    _email_sent = False
    fields['captcha'].widgetFactory = CaptchaFieldWidget

    def __init__(self, context, request, info=None):
        super(ContactForm, self).__init__(context, request)
        self.item_info = info

    @property
    def config(self):
        """Get view configuration data from annotations."""
        annotations = IAnnotations(self.context)
        return annotations.get(config.SETTINGS_DEVELOPMENT_COLLECTION, {})

    def update(self):
        if self.config.get('show_captcha', False) is False:
            self.fields = field.Fields(IContactForm).omit('captcha')
        super(ContactForm, self).update()

    @property
    def already_sent(self):
        return self._email_sent

    @button.buttonAndHandler(PMF(u'label_send', default='Send'), name='send')
    def handle_send(self, action):
        """Send button for sending the email."""
        can_send = True
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if 'captcha' in data:
            can_send = False
            # Verify the user input against the captcha
            captcha = CaptchaValidator(
                self.context,
                self.request,
                None,
                IContactForm['captcha'],
                None,
            )
            try:
                can_send = captcha.validate(data['captcha'])
            except WrongCaptchaCode, e:
                self.status = e.doc()
                return

        if not self.already_sent and can_send:
            if self.send_email(data):
                self._email_sent = True
                plone_api.portal.show_message(
                    message=_(u'Your contact request was sent successfully.'),
                    request=self.request,
                    type='info',
                )
        self.request.response.redirect(self.request.URL)
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
            agent = self.item_info
            rcp = agent.email.value
        except:
            rcp = from_address
        sender = '{0} <{1}>'.format(data['name'], data['sender_from_address'])
        subject = u'Customer Contact Developments'
        data['url'] = self.request.getURL()
        message = EMAIL_TEMPLATE.format(**data)
        message = message_from_string(message.encode(email_charset))
        message['To'] = rcp
        message['From'] = from_address
        message['Reply-to'] = sender
        message['Subject'] = subject
        try:
            mailhost.send(message, immediate=True, charset=email_charset)
        except:
            return False
        return True


# Register Captcha validator for the captcha field in the ICaptchaForm
validator.WidgetValidatorDiscriminators(
    CaptchaValidator, field=IContactForm['captcha'])


@implementer(IDevelopmentDetails)
class DevelopmentDetails(BrowserView):
    """Detail view for MLS developments."""

    _item = None
    _contact_form = None
    _contact_info = None

    def __init__(self, context, request):
        super(DevelopmentDetails, self).__init__(context, request)
        self.registry = getUtility(IRegistry)

    @property
    def config(self):
        """Get view configuration data from annotations."""
        annotations = IAnnotations(self.context)
        return annotations.get(config.SETTINGS_DEVELOPMENT_COLLECTION, {})

    @property
    def item(self):
        if self._item is None:
            self._item = self._get_item()
        return self._item

    def _get_item(self):
        cache = IAnnotations(self.request)
        item = cache.get('ps.plone.mls.development.traversed', None)

        if item is None:
            item_id = getattr(self.request, 'development_id', None)
            if not item_id:
                return

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

        return item

    @property
    def lead_image(self):
        """"""
        item = self.item
        try:
            img = item.lead_image
        except AttributeError:
            pass
        else:
            return img

        try:
            images = item.pictures()
        except AttributeError:
            pass
        else:
            if len(images) > 0:
                return images[0]

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
        geolocation = getattr(self.item, 'geolocation', None)
        if geolocation is None:
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
            zoom=self.config.get('map_zoom_level', 7),
        )

    def use_fotorama(self):
        if not HAS_UI_SETTINGS:
            return False

        if self.registry is not None:
            try:
                settings = self.registry.forInterface(IMLSUISettings)
            except:
                logger.warning('MLS UI settings not available.')
            else:
                return getattr(settings, 'slideshow') == u'fotorama'
        return False

    def use_galleria(self):
        if not HAS_UI_SETTINGS:
            return True

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

    def show_section_contact(self):
        """Should the contact us section be shown at all?"""
        show_form = self.contact_form() is not None
        show_info = self.contact_info() is not None
        return show_info or show_form

    def contact_info(self):
        """Get the contact information, if enabled."""
        if not self.config.get('show_contact_info', False):
            return

        if self._contact_info is not None:
            return self._contact_info

        item = self.item
        agency = getattr(item, 'agency', None)
        if agency is not None and agency() is not None:
            agency = agency()
            agency.override(context=self.context)
        agent = getattr(item, 'agent', None)
        if agent is not None and agent() is not None:
            agent = agent()
            agent.override(context=self.context)
        self._contact_info = {
            'agency': agency,
            'agent': agent,
        }
        return self._contact_info

    def contact_form(self):
        """Get the contact form, if enabled."""
        if not self.config.get('show_contact_form', False):
            return

        if self._contact_form is not None:
            return self._contact_form

        item_info = self.contact_info().get('agent')
        z2.switch_on(self, request_layer=IFormLayer)
        self._contact_form = ContactForm(
            aq_inner(self.context),
            self.request,
            item_info,
        )
        if HAS_WRAPPED_FORM:
            alsoProvides(self._contact_form, IWrappedForm)
        return self._contact_form


class HeaderViewlet(ViewletBase):
    """Header Image"""

    _id = None
    _title = None
    _headline = None
    _location = None
    _logo = None
    _banner = None
    _has_banner = False

    @property
    def available(self):
        # do we have a development?
        self._id = getattr(self.request, 'development_id', None)
        if self._id is not None:
            return True
        else:
            return False

    @property
    def get_title(self):
        """Get development title"""
        return self._title

    @property
    def get_headline(self):
        """Get development headline"""
        return self._headline

    @property
    def get_location(self):
        """Get development location"""
        return self._location

    @property
    def get_logo(self):
        """Get development logo"""
        return self._logo

    @property
    def get_banner(self):
        """Get development header"""
        return self._banner

    def update(self):
        """Prepare view related data."""
        super(HeaderViewlet, self).update()

        if self.available:
            self._set_development_info()

    def _set_banner(self, item):
        """Look for available Header image"""
        try:
            # banner image as regular data
            self._banner = item.banner_image.value
            self._has_banner = True
        except:
            # no header image found yet
            # take the first available picture instead
            try:
                pics = item.pictures()
                self._banner = pics[0].get()
                self._has_banner = True
            except:
                # still no header image found
                self._has_banner = False

    def _set_development_info(self):
        """set all available data for the development header"""
        cache = IAnnotations(self.request)
        item = cache.get('ps.plone.mls.development.traversed', None)

        if item is not None:
            # try to set the available data
            try:
                self._logo = item.logo.value
            except:
                pass
            try:
                self._title = item.title.value
            except:
                pass
            try:
                self._headline = item.headline.value
            except:
                pass
            try:
                seq = (item.city.value,
                       item.subdivision.value,
                       item.country.value)
                joint = ', '
                self._location = joint.join(seq)
            except:
                self._location = item.location.value
            # set header image
            self._set_banner(item)
