"This module controls general system parameters."

__author__    = "Anna Logg (anna@loggsystems.se)"
__date__      = "2008-11-01 -- 2008-12-12"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__   = "GNU GPL version 3 or any later version"

# Modified by Benjamin Kehlet, 2011

database_filename       = "papers.pub"
local_venues_filename   = "venues.list"
invalid_filename_prefix = "invalid_papers"

matching_distance_strong = 0.1
matching_distance_weak   = 0.5

autofix  = False
debug    = False

pdf_viewer = "evince"
view_pdf = True
pdf_dir = "papers"

headline = ""

compact = False

require_page_range = False
page_separator = "-"

# Set a prefix for the class names when generating html.
# Example: class="publish_item_title"
html_class_prefix = "publish"

# Should numbering in report be global
# or start over for each category
# NOTE: Not fully implemented for all report types.
global_numbering = False
