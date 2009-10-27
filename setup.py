#!/usr/bin/env python

from distutils.core import setup, Extension
from os.path import join

module_levenshtein = Extension('levenshtein',
                               sources = ['publish/extensions/levenshtein.c'])

setup(name = "publish",
      version = "1.0",
      description = "Distributed publication management system",
      author = "Logg Systems/Anna Logg",
      author_email = "anna@loggsystems.se",
      url = "",
      packages = ["publish",
                  "publish.formats",
                  "publish.config",
                  "publish.extensions"],
      package_dir = {"publish": "publish"},
      scripts = [join("scripts", "publish")],
      data_files = [(join("share", "man", "man1"), [join("doc", "man", "man1", "publish.1.gz")])],
      ext_modules = [module_levenshtein])
