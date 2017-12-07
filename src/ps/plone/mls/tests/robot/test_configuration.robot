*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***

Show how to configure the base MLS settings
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@mls-controlpanel
    ${note1}  Add pointy note  css=#form-widgets-mls_key
    ...  Enter your MLS API-Key
    ...  position=right
    ${note2}  Add pointy note  css=#form-widgets-mls_site
    ...  Enter the URL for the MLS
    ...  position=right
    ${note3}  Add pointy note  css=#form-widgets-agency_id
    ...  Enter your agency id
    ...  position=right
    Capture and crop page screenshot
    ...  configure_base_settings.png
    ...  css=#content
    ...  ${note1}  ${note2}  ${note3}
    Remove elements  ${note1}  ${note2}  ${note3}
