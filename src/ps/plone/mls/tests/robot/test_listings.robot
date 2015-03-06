*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***


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
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  css=#plone-contentmenu-actions-listing-collection-activate@href
    go to  ${href}

    Capture and crop page screenshot
    ...  activate_listing_collection_done.png
    ...  css=#portal-column-content

    Click Overlay Link  css=#contentview-listing-collection-config a

    Wait until element is visible
    ...  css=div.pb-ajax

    Capture and crop page screenshot
    ...  configure_listing_collection.png
    ...  css=div.pb-ajax

    Click button  css=#form-buttons-cancel

    Page should contain element  css=#plone-contentmenu-actions dt a
    Click link  css=#plone-contentmenu-actions dt a
    Wait until element is visible
    ...  css=#plone-contentmenu-actions dd.actionMenuContent

    ${note1}  Add pointy note  css=#plone-contentmenu-actions-listing-collection-deactivate
    ...  Click to deactivate the Listing Collection
    ...  position=left
    Mouse over  css=#plone-contentmenu-actions-listing-collection-deactivate
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  deactivate_listing_collection.png
    ...  contentActionMenus
    ...  css=#portal-column-content
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  css=#plone-contentmenu-actions-listing-collection-deactivate@href
    go to  ${href}

    Capture and crop page screenshot
    ...  deactivate_listing_collection_done.png
    ...  css=#portal-column-content
