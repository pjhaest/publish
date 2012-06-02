"This module handles configuration parameters."

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-11-09 -- 2009-07-31"
__copyright__ = "Copyright (C) 2008-2009 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

# Modified by Anders Logg 2009-2012
# Modified by Benjamin Kehlet 2012
# Last modified: 2012-06-02

from os.path import isfile
import __builtin__
data = None

def get(key):
    "Return data/parameter value for given key"

    # Initialize parameters if necessary
    if data is None:
        init()

    # Check key
    if not key in data:
        raise RuntimeError, ("Unknown parameter key: %s"% str(key))

    return data[key]

def set(key, value):
    "Set data/parameter value for given key"

    # Check key
    if not key in data:
        raise RuntimeError, ("Unknown parameter key: %s"% str(key))

    # Set value
    data[key] = value

def set_from_string(key, value):
    "Set data/parameter value from string for given key"
    if value == "yes":
        set(key, True)
    elif value == "no":
        set(key, False)
    else:
        #set(key, eval(value))
        set(key, value)

def has_key(key):
    "Check if parameter exist for key"
    if data is None:
        init()

    return key in data

def init():

    global data
    data = {}

    # Import parameters from general
    import general
    data["database_filename"]        = general.database_filename
    data["local_venues_filename"]    = general.local_venues_filename
    data["invalid_filename_prefix"]  = general.invalid_filename_prefix
    data["matching_distance_strong"] = general.matching_distance_strong
    data["matching_distance_weak"]   = general.matching_distance_weak
    data["autofix"]                  = general.autofix
    data["debug"]                    = general.debug
    data["pdf_viewer"]               = general.pdf_viewer
    data["view_pdf"]                 = general.view_pdf
    data["pdf_dir"]                  = general.pdf_dir
    data["headline"]                 = general.headline
    data["repeat_headline"]          = general.repeat_headline
    data["compact"]                  = general.compact
    data["require_page_range"]       = general.require_page_range
    data["page_separator"]           = general.page_separator
    data["html_class_prefix"]        = general.html_class_prefix
    data["html_add_internal_links"]  = general.html_add_internal_links
    data["global_numbering"]         = general.global_numbering
    data["use_labels"]               = general.use_labels
    data["skip_categories"]          = general.skip_categories

    # Import parameters from capitalization
    import capitalization
    data["lowercase"] = capitalization.lowercase
    data["uppercase"] = capitalization.uppercase

    # Import parameters from typos
    import typos
    data["typos"] = typos.typos

    # Import parameters from attributes
    import attributes
    data["categories"]           = attributes.categories
    data["category_headings"]    = attributes.category_headings
    data["category_labels"]      = attributes.category_labels
    data["category_attributes"]  = attributes.category_attributes
    data["category_venues"]      = attributes.category_venues
    data["ordered_attributes"]   = attributes.ordered_attributes
    data["entrytypes"]           = attributes.entrytypes
    data["entrytype_attributes"] = attributes.entrytype_attributes
    data["entrytype2category"]   = attributes.entrytype2category
    data["category2entrytype"]   = attributes.category2entrytype

    # Import parameters from formatting
    import formatting
    data["latex_format"] = formatting.latex_format
    data["html_format"] = formatting.html_format
    data["rst_format"] = formatting.rst_format
    data["mark_author"] = __builtin__.set()
    data["use_textsc"]  = True

    # Import parameters from institutions
    import institutions
    data["institutions"] = list(institutions.institutions)

    # Import parameters from schools
    import schools
    data["schools"] = list(schools.schools)

    # Import parameters from publishers
    import publishers
    data["publishers"] = list(publishers.publishers)

    # Empty list of meetings (could be extended in meetings.py)
    data["meetings"] = []

    # Import parameters from journals
    import journals

    # Create list of all journals (including both short and long names)
    journal_list = [short for (short, long, issn) in journals.journals] + \
                   [long  for (short, long, issn) in journals.journals]
    data["journals"] = journal_list

    # Create mapping from long to short journal names
    long2short = {}
    for (short, long, issn) in journals.journals:
        long2short[long] = short
    data["long2short"] = long2short

    # Create mapping from short to long journal names
    short2long = {}
    for (short, long, issn) in journals.journals:
        short2long[short] = long
    data["short2long"] = short2long

    # Create mapping from long name to issn number
    long2issn = {}
    for (short, long, issn) in journals.journals:
        long2issn[long] = issn
    data["long2issn"] = long2issn

    # Read local venues
    _read_uservenues(general.local_venues_filename,
                     data["journals"],
                     data["publishers"],
                     data["schools"],
                     data["institutions"],
                     data["meetings"])

def _read_uservenues(filename, journals, publishers, schools, institutions, meetings):
    "Read venues from file"

    # Check for file
    if not isfile(filename):
        return

    # Open and read file
    try:
        file = open(filename, "r")
        text = file.read()
        file.close()
    except:
        raise RuntimeError, 'Unable to read local venues from file "%s".' % filename

    # Parse file
    lines = text.split("\n")
    for line in lines:

        if not ":" in line:
            continue

        venue_type = line.split(":")[0].strip()
        venue_name = ":".join(line.split(":")[1:]).strip()

        if venue_type == "journal":
            journals.append(venue_name)
        elif venue_type == "publisher":
            publishers.append(venue_name)
        elif venue_type == "school":
            schools.append(venue_name)
        elif venue_type == "institution":
            institutions.append(venue_name)
        elif venue_type == "meeting":
            meetings.append(venue_name)
        else:
            print 'Unknown venue type: "%s"' % venue_type
