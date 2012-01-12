#!/usr/bin/env python
import pymongo
from settings import db

# WARNING: THIS SCRIPT WILL DELETE ALL YOUR DATA!

db.programs.remove()
programs = []
for i in range(100):
  programs.append({"title": "program%d" % i, "public": "true" if i%2==0 else "false"})

db.programs.insert(programs)
