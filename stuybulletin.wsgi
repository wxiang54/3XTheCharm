#!/usr/bin/python
import sys
sys.path.insert(0,"/var/www/stuybulletin/")

from app import app as application
application.secret_key = "not_so_secret_key"
