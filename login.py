# login.py
# User login pages for CedarRapidsOnline web service
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
import string
import crypt

class LoginPage:
    def index (self):
        pagetext = "<form action=\"/login/process\" method=\"post\">"
        pagetext += "<b>Email Address</b>:"
        pagetext += "<br>"
        pagetext += "<input type=\"text\" name=\"email\">"
        pagetext += "<br><br>"
        pagetext += "<b>Password</b>:"
        pagetext += "<br>"
        pagetext += "<input type=\"password\" name=\"password\">"
        pagetext += "<br>"
        pagetext += "<input type=\"submit\" value=\"Log In\">"
        pagetext += "</form>"
        # FIXME: offer to send a new password to the user's email address.
        return pageutils.generate_page ("Log In", pagetext)
    index.exposed = True

    def process (self, email=None, password=None):
        # Clean up text for usage with database.
        email = sqlutils.quote (email)
        password = sqlutils.quote (password)

        # Encrypt password using the same encryption we used when the password
        # was stored in the database.
        password = crypt.crypt (password, "23")

        description = None
        results = None
        # Try to connect to the database.
        try:
            dbconnection = pgdb.connect (__database_connect_fields)
            dbcursor = dbconnection.cursor()
            dbcursor.execute ("SELECT * FROM users WHERE email=%s", [email])
            # Get the cursor description and results from the query.
            description = dbcursor.description()
            results = dbcursor.fetchone()
            
            # Close the database cursor and connection.
            dbcursor.close()
            dbconnection.close()
        except:
            # FIXME: do something more useful here.
            pass        
        
        # If we don't have any results, the email address wasn't on record.
        if (results == None):
            # FIXME: do something more useful here.
            raise cherrypy.HTTPRedirect ("/login")
        else:
            stored_password = ""
            try:
                stored_password = results[sqlutils.getfieldindex ("password", description)]
            except:
                # FIXME: do something more useful here.
                raise cherrypy.HTTPRedirect ("/fatalerror")
            # Verify password equivalence.
            if (password <> stored_password):
                # FIXME: do something more useful here.
                raise cherrypy.HTTPRedirect ("/login")
            else:
                # If we got this far, the email address was on record, and the password
                # matches it, so we deem the user to be logged in.  Hooray!
                user_id = None
                user_level = 0
                try:
                    user_id = results[sqlutils.getfieldindex ("user_id", description)]
                    user_level = results[sqlutiles.getfieldindex ("level", description)]
                except:
                    # FIXME: do something more useful here.
                    raise cherrypy.HTTPRedirect ("/fatalerror")
                # If the user level is 2 or higher, the user is an admin user.
                set_logged_in (user_id, (user_level > 1))

        # FIXME: Might want to redirect to some sort of user dashboard page in the future.
        raise cherrypy.HTTPRedirect ("/")
    process.exposed = True
