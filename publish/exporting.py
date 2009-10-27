"This module implements data export to different file formats."

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-11-11 -- 2009-08-30"
__copyright__ = "Copyright (C) 2008-2009 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

# Modified by Anders Logg, 2009.

from publish.importing import read_database
from publish import config
from formats import bibtex, latex, pub, pdf, html
from validation import validate_papers
from log import print_summary
from common import short_author

def export_file(filename, filters):
    "Export data into desired file format"

    # Make sure we don't overwrite the database
    database_filename = config.get("database_filename")
    if filename == database_filename:
        raise RuntimeError, ('Papers cannot be exported to the default database ("%s").' % database_filename)

    # Read and validate database
    database_papers = read_database(database_filename)
    (valid_papers, invalid_papers) = validate_papers(database_papers)

    # Filter papers
    filtered_papers = filter_papers(valid_papers, filters)

    # Get the filename suffix
    suffix = filename.split(".")[-1]

    # Choose format based on suffix
    if suffix in ("bib", "bibtex"):
        write = bibtex.write
    elif suffix == "pub":
        write = pub.write
    elif suffix == "tex":
        write = latex.write
    elif suffix == "pdf":
        write = pdf.write
    elif suffix == "html":
        write = html.write
    else:
        raise RuntimeError, "Unknown file format."

    # Open and read file
    text = write(filtered_papers)
    try:
        file = open(filename, "w")
        file.write(text)
        file.close()
    except:
        raise RuntimeError, 'Unable to open file "%s"' % filename

    # Print summary
    print_summary(filtered_papers)
    print ""
    print "Exported %d paper(s) to %s." % (len(filtered_papers), filename)

def filter_papers(papers, filters):
    "Filters papers, for instance it enables to get papers from a specific year"

    filtered_papers = []
    for paper in papers:
        match = True
        for attribute in filters:
            value, should_match = filters[attribute]
            if attribute == "author" or attribute == "editor":
                if not matching_author(paper[attribute], value, should_match):
                    match = False
                    break
            else:
                if not matching_attribute(paper, attribute, value, should_match):
                    match = False
                    break
        if match:

            # Remove private key
            paper = paper.copy()
            if "private" in paper:
                del paper["private"]

            # Append paper
            filtered_papers.append(paper)

    return filtered_papers

def matching_attribute(paper, attribute, value, should_match):
    "Check if attribute matches"

    # Check for match
    match = attribute in paper and paper[attribute] == value

    # Should either match or not
    if should_match:
        return match
    else:
        return not match

def matching_author(authors, value, should_match):
    "Check if author matches"

    # Match is case-insensitive
    value = value.lower()

    # Check for match
    match = False
    for author in authors:

        # Check match against full name and abbreviation
        author_lower = author.lower()
        author_short = short_author(author).lower()
        if value in author_lower or value in author_short:
            match = True
            break

    # Should either match or not
    if should_match:
        return match
    else:
        return not match
