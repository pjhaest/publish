# Publish: A Bibliographic Reference System

## Overview

Publish may be used for handling publication lists for research
institutions and departments, or for individual researchers. Publish
imports publication metadata (title, author, year of publication etc),
validates the imported data against a database of known venues, checks
for missing attributes, corrects common errors etc, and allows simple
filtering and generation of publication lists.

For further information, refer to the Publish User Manual available in
the subdirectory doc/manual/ of this source tree.

## Installation

To install Publish, simply type
```
sudo python setup.py install
```

## Dependencies:

This version of Publish requires Python 2.6 (only tested for 2.7)
or 3.4, plus the modules levenshtein and future:

```
sudo pip install python-Levenshtein
sudo pip install future
sudo pip install lxml
```

## Author

Publish was originally developed and implemented by
Anna Logg <anna@loggsystems.se> at Logg Systems.
It is currently maintained by Anders Logg <logg@chalmers.se>.

## License:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.