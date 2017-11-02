*** Variables ***

# Variables specific for Plone 4.3.x.
# See default.robot for all available variables.

# "Listing Collection"
${LISTING_COLLECTION_N_ITEMS}  css=#listing-collection .tileItem:nth-child(3)

# "Recent Listings"
${RECENT_LISTINGS_N_ITEMS}  css=#recent-listings .tileItem:nth-child(3)

# "Development Collection"
${DEVELOPMENT_COLLECTION_N_ITEMS}  css=.development__results .tileItem:nth-child(3)
