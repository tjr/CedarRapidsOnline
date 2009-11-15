# logout.py
# User logout pages for CedarRapidsOnline web service
# Copyright (C) 2009 Clear Perception Solutions, LLC.
# Written by Trevis J. Rothwell <tjr@gnu.org>
# 
# This file is part of the CedarRapidsOnline web service.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cherrypy
import pgdb

import pageutils
import sqlutils

class LogoutPage:
    def index (self):
        # Force the session to expire and redirect.
        cherrypy.lib.sessions.expire()
        raise cherrypy.HTTPRedirect ("/logout/complete")
    index.exposed = True

    def complete (self):
        return pageutils.generate_page ("Logged Out",
                                        "You are now logged out. Thanks for using CedarRapidsOnline!")
