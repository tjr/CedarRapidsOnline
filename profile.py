# profile.py
# User profile pages for CedarRapidsOnline web service
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

class ProfilePage:

    def index (self):
        # Logged in users can edit their own data.
        # This page should also be known as /profile
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login/v")

        # Get the user_id for the logged-in user.
        user_id = str(pageutils.get_user_id())
        if (user_id == None):
            return pageutils.generate_page ("System Error",
                                            "<div class=\"error\">Unable to access user profile page.</div>")
        
        description = None
        results = []
        # Get user data from database
        try:
            # Try to connect to the database.
            dbconnection = pgdb.connect (database_connect_fields)
            dbcursor = dbconnection.cursor()
            dbcursor.execute ("SELECT * FROM users WHERE user_id=%s", user_id)
            
            # Get the cursor description and results from the query.
            description = dbcursor.description
            results = dbcursor.fetchone()

            # Close the database cursor and connection.
            dbcursor.close()
            dbconnection.close()
        except:
            return pageutils.generate_page ("Database Error",
                                            "<div class=\"error\">Can't get user data.</div>\n")

        url = results[sqlutils.getfieldindex("url", description)]
        if (url == None):
            url = "NONE"
        pagetitle = results[sqlutils.getfieldindex("name", description)]
        pagetext = ""
        pagetext += "<ul>\n"
        pagetext += ("<li><br>Email address</b>: " + results[sqlutils.getfieldindex("email", description)] +
                     "<br>[<a href=\"/profile/email\">Change my email address</a>]</li>\n")
        pagetext += ("<li><b>URL</b>: " + url + "<br>[<a href=\"/profile/url\">Change my URL</a>]</li>\n")
        pagetext += "<li>[<a href=\"/profile/password\">Change my password</a>]</li>\n"
        pagetext += "</ul>\n"

        return pageutils.generate_page (pagetitle, pagetext)
    index.exposed = True

