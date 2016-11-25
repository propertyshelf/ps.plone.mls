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

    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${LINK_LISTING_COLLECTION_ACTIVATE}
    ...  Click to activate the Listing Collection
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${LINK_LISTING_COLLECTION_ACTIVATE}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  activate_listing_collection.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${LINK_LISTING_COLLECTION_ACTIVATE}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  activate_listing_collection_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}

    Click link  css=#contentview-listing-collection-config a

    Wait until element is visible  ${CONTENT}

    Capture and crop page screenshot
    ...  configure_listing_collection.png
    ...  ${CONTENT}

    Click button  css=#form-buttons-cancel

    Go to  ${PLONE_URL}/${FOLDER_ID}
    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${LINK_LISTING_COLLECTION_DEACTIVATE}
    ...  Click to deactivate the Listing Collection
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${LINK_LISTING_COLLECTION_DEACTIVATE}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  deactivate_listing_collection.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${LINK_LISTING_COLLECTION_DEACTIVATE}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  deactivate_listing_collection_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}


Show how to activate the recent listings
    Enable autologin as  Site Administrator
    Create content  type=Folder
    ...  id=${FOLDER_ID}
    ...  title=A folder
    ...  description=This is the folder
    Go to  ${PLONE_URL}/${FOLDER_ID}

    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${RECENT_LISTINGS_ACTIVATE}
    ...  Click to activate the Recent Listings
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${RECENT_LISTINGS_ACTIVATE}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  activate_recent_listings.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${RECENT_LISTINGS_ACTIVATE}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  activate_recent_listings_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}

    Click link  css=#contentview-recent-listings-config a

    Wait until element is visible  ${CONTENT}

    Capture and crop page screenshot
    ...  configure_recent_listings.png
    ...  ${CONTENT}

    Click button  css=#form-buttons-cancel

    Go to  ${PLONE_URL}/${FOLDER_ID}
    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${RECENT_LISTINGS_DEACTIVATE}
    ...  Click to deactivate the Recent Listings
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${RECENT_LISTINGS_DEACTIVATE}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  deactivate_recent_listings.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${RECENT_LISTINGS_DEACTIVATE}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  deactivate_recent_listings_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}
