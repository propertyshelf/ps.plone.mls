*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***

Show how to activate the add-on
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/prefs_install_products_form
    ${note1}  Add pointy note  css=label[for="ps.plone.mls"]
    ...  Select the item to install the add-on
    ...  position=left
    Capture and crop page screenshot
    ...  setup_select_add_on.png
    ...  css=label[for="ps.plone.mls"]
    ...  ${note1}
