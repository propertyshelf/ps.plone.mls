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


Show how to activate the listing collection
    Enable autologin as  Site Administrator
    Create content  type=Folder
    ...  id=${FOLDER_ID}
    ...  title=A folder
    ...  description=This is the folder
    Go to  ${PLONE_URL}/${FOLDER_ID}

    Page should contain element  css=#plone-contentmenu-actions dt a
    Click link  css=#plone-contentmenu-actions dt a
    Wait until element is visible
    ...  css=#plone-contentmenu-actions dd.actionMenuContent

    ${note1}  Add pointy note  css=#plone-contentmenu-actions-listing-collection-activate
    ...  Click to activate the Listing Collection
    ...  position=left
    Mouse over  css=#plone-contentmenu-actions-listing-collection-activate
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  activate_listing_collection.png
    ...  contentActionMenus
    ...  css=#portal-column-content
    ...  ${note1}
