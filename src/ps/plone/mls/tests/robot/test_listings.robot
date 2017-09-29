*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***


Show how to activate the listing search
    Enable autologin as  Site Administrator
    Create content  type=Folder
    ...  id=${FOLDER_ID}-3
    ...  title=A Listing Search
    ...  description=This is the folder
    Go to  ${PLONE_URL}/${FOLDER_ID}-3

    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${LISTING_SEARCH_ACTIVATE_LINK}
    ...  Click to activate the Listing Search
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${LISTING_SEARCH_ACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  activate_listing_search.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${LISTING_SEARCH_ACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  activate_listing_search_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}

    Click link  css=#contentview-listing-search-config a

    Wait until element is visible  ${CONTENT}

    Capture and crop page screenshot
    ...  configure_listing_search.png
    ...  ${CONTENT}

    Click button  css=#form-config-buttons-cancel

    Go to  ${PLONE_URL}/${FOLDER_ID}-3
    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${LISTING_SEARCH_DEACTIVATE_LINK}
    ...  Click to deactivate the Listing Search
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${LISTING_SEARCH_DEACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  deactivate_listing_search.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${CONTENT}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${LISTING_SEARCH_DEACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  deactivate_listing_search_done.png
    ...  ${STATUS_MESSAGE}
    ...  ${CONTENT}
