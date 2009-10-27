"This module implements input/output for LaTeX."

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-11-06 -- 2008-11-12"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

from publish import config

def write(papers):
    "Format the given list of papers in the LaTeX format."

    text = ""
    
    # Get formatting rule
    latex_format = config.get("latex_format")

    # Write headline
    headline = config.get("headline")
    if headline == "":
        headline = "Publications"

    # Start of LaTeX paper
    text+= "\\renewcommand \\refname{%s}\n\n" % headline
    text+= "\\begin{thebibliography}{99}\n"
  
    # Iterate over categories
    categories = config.get("categories")
    current_paper = 0
    for category in categories:

        # Extract papers in category
        category_papers = [paper for paper in papers if paper["category"] == category]
        if len(category_papers) == 0:
            continue

        # Write category
        category_headings = config.get("category_headings")
        text += "\\subsection*{%s}\n" % category_headings[category]

        # Iterate over papers in category
        for paper in category_papers:

            # Get key (or generate key)
            if "key" in paper:
                key = paper["key"]
            else:
                key = "paper%d" % current_paper

            # Write each paper as bibitem
            text += "\\bibitem{%s} {%s}\n" % (key, latex_format[category](paper))

            current_paper += 1

    text += "\\end{thebibliography}"
                
    return text
