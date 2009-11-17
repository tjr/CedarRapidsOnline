# discussions.py
# Discussion pages for CedarRapidsOnline web service
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
import string
import sqlutils
import pageutils

database_connect_fields = sqlutils.database_connect_fields

class DiscussionsPage:
    def index (self, discussion_id=None):
        # If discussion_id is None, display main discussion table of contents.
        # Else, display specified discussion.
        # Available to all, logged in or not.
        pass
    index.exposed = True

    def comment (self, discussion_id):
        # Verify user is logged in.
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login")
        
        pagetext = ""
        pagetitle = "Add a Comment"

        pagetext += "<form action=\"/discussions/processcomment\" method=\"post\">"
        pagetext += "<textarea cols=80 rows=10 name=\"body\"></textarea>\n"
        pagetext += "<br><br>"
        pagetext += "<input type=\"hidden\" name=\"refers_to\" value=\"" + (str(discussion_id)) + "\">\n"
        pagetext += "<input type=\"submit\" value=\"Add Comment\">"
        pagetext += "</form>"
        
        return pageutils.generate_page (pagetitle, pagetext)
    comment.exposed = True

    def new (self):
        # Verify user is logged in.
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login")
        
        pagetext = ""
        pagetitle = "Start a New Discussion"

        pagetext += "<form action=\"/discusions/processnew\" method=\"post\">"
        pagetext += "<b>Subject</b>:"
        pagetext += "<br>"
        pagetext += "<input type=\"text\" name=\"subject\">\n"
        pagetext += "<br><br>"
        pagetext += "<b>Message</b>:\n<br>\n"
        pagetext += "<textarea cols=80 rows=10 name=\"body\"></textarea>\n"
        pagetext += "<br><br>"
        pagetext += "<input type=\"submit\" value=\"Start New Discussion\">"
        pagetext += "</form>"
        
        return pageutils.generate_page (pagetitle, pagetext)
    new.exposed = True

