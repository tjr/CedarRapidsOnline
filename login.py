# login.py
# User login pages for CedarRapidsOnline web service
# Copyright (C) 2009 Clear Perception Solutions, LLC.
# Written by Trevis J. Rothwell <tjr@gnu.org>
# 
# This file is part of the CedarRapidsOnline web service.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cherrypy
import pgdb
import pageutils
import sqlutils
import string
import crypt

database_connect_fields = sqlutils.database_connect_fields

class LoginPage:
    def default(self, accessviolation=None, errornotfound=False, errorbadpassword=False):
        # We want to be able to have URLs like /login/accessviolation
        # The CherryPy index methods can't accept parameters like that, but
        # instead we route through the default method.  QED.
        return self.index (accessviolation, errornotfound, errorbadpassword)
    default.exposed = True

    def index (self, accessviolation=None, errornotfound=False, errorbadpassword=False):
        pagetext = ""
        
        # Check to see if we've been redirected here from an access violation.
        if (accessviolation <> None):
            pagetext += "<div class=\"notice\"><h2>Notice</h2>You must be logged in to access that page.</div><br><br>\n"

        # Check to see if we've been here before, with bad user input.
        if (errornotfound or errorbadpassword):
            pagetext += "<div class=\"error\"><h2>Error</h2><ul>\n"
            if (errornotfound):
                pagetext += "<li>Email address not found. Have you <a href=\"/register\">registered</a> yet?</li>\n"
            if (errorbadpassword):
                pagetext += "<li>Incorrect password provided.</li>\n"
            pagetext += "</ul></div><br><br>\n"

        # Build the login form.
        pagetext += "<form action=\"/login/process\" method=\"post\">"
        pagetext += "<b>Email Address</b>:"
        pagetext += "<br>"
        pagetext += "<input type=\"text\" name=\"email\">"
        pagetext += "<br><br>"
        pagetext += "<b>Password</b>:"
        pagetext += "<br>"
        pagetext += "<input type=\"password\" name=\"password\">"
        pagetext += "<br><br>"
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
            dbconnection = pgdb.connect (database_connect_fields)
            dbcursor = dbconnection.cursor()
            dbcursor.execute ("SELECT * FROM users WHERE email=%s", [email])
            # Get the cursor description and results from the query.
            description = dbcursor.description
            results = dbcursor.fetchone()
            
            # Close the database cursor and connection.
            dbcursor.close()
            dbconnection.close()
        except:
            # FIXME: do something more useful here.
            pass        
        
        # If we don't have any results, the email address wasn't on record.
        if (results == None):
            return self.index (errornotfound=True)
        else:
            stored_password = ""
            try:
                stored_password = results[sqlutils.getfieldindex ("password", description)]
            except:
                # FIXME: do something more useful here.
                raise cherrypy.HTTPRedirect ("/fatalerror")
            # Verify password equivalence.
            if (password <> stored_password):
                return self.index (errorbadpassword=True)
            else:
                # If we got this far, the email address was on record, and the password
                # matches it, so we deem the user to be logged in.  Hooray!
                user_id = None
                user_level = 0
                try:
                    user_id = results[sqlutils.getfieldindex ("user_id", description)]
                    user_level = results[sqlutils.getfieldindex ("level", description)]
                except:
                    # FIXME: do something more useful here.
                    raise cherrypy.HTTPRedirect ("/fatalerror")
                # If the user level is 2 or higher, the user is an admin user.
                pageutils.set_logged_in (user_id, (user_level > 1))

        # FIXME: Might want to redirect to some sort of user dashboard page in the future.
        raise cherrypy.HTTPRedirect ("/")
    process.exposed = True
