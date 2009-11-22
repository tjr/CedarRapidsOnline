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
            raise cherrypy.HTTPRedirect ("/login/e")

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
        pagetext += ("<li><b>Email address</b>: " + results[sqlutils.getfieldindex("email", description)] +
                     "<br>[<a href=\"/profile/email\">Change my email address</a>]</li>\n")
        pagetext += ("<li><b>URL</b>: " + url + "<br>[<a href=\"/profile/url\">Change my URL</a>]</li>\n")
        pagetext += "<br><li>[<a href=\"/profile/password\">Change my password</a>]</li>\n"
        pagetext += "<br><li>[<a href=\"/profile/name\">Change my name</a>]</li>\n"
        pagetext += "</ul>\n"

        return pageutils.generate_page (pagetitle, pagetext)
    index.exposed = True

    def name (self, error=None):
        # Logged in users can edit their own data.
        # This page should also be known as /profile
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login/e")
        pagetext = ""
        if (error <> None):
            pagetext += "<div class=\"error\">Name cannot be blank.</div>\n"
        pagetext += "<form action=\"/profile/process\" method=\"post\">"
        pagetext += "<b>Name</b>:"
        pagetext += "<br>"
        pagetext += "<input type=\"text\" name=\"name\">"
        pagetext += "<br><br>"
        pagetext += "<input type=\"submit\" value=\"Change Your Name\">"
        pagetext += "</form>"
        return pageutils.generate_page ("Change Your Name", pagetext)
    name.exposed = True

    def email (self, error=None):
        # Logged in users can edit their own data.
        # This page should also be known as /profile
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login/e")
        pagetext = ""
        if (error == "invalid"):
            pagetext += "<div class=\"error\">Please enter a valid email address, in the form: user@bar.baz</div>"
        elif (error <> None):
            pagetext += "<div class=\"error\">Email address cannot be blank.</div>\n"
        pagetext += "<form action=\"/profile/process\" method=\"post\">"
        pagetext += "<b>Email Address</b>:"
        pagetext += "<br>"
        pagetext += "<input type=\"text\" name=\"email\">"
        pagetext += "<br><br>"
        pagetext += "<input type=\"submit\" value=\"Change Your Email Address\">"
        pagetext += "</form>"
        return pageutils.generate_page ("Change Your Email Address", pagetext)
    email.exposed = True

    def url (self):
        # Logged in users can edit their own data.
        # This page should also be known as /profile
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login/e")
        pagetext = ""
        pagetext += "<form action=\"/profile/process\" method=\"post\">"
        pagetext += "<b>URL</b> (leave blank to clear existing URL):"
        pagetext += "<br>"
        pagetext += "<input type=\"text\" name=\"url\">"
        pagetext += "<br><br>"
        pagetext += "<input type=\"submit\" value=\"Change Your URL\">"
        pagetext += "</form>"
        return pageutils.generate_page ("Change Your  URL", pagetext)
    url.exposed = True

    def password (self, error=None):
        # Logged in users can edit their own data.
        # This page should also be known as /profile
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login/e")
        pagetext = ""
        if (error == "verify"):
            pagetext += "<div class=\"error\">Password fields must match.</div>\n"
        elif (error <> None):
            pagetext += "<div class=\"error\">Neither password field can be blank.</div>\n"
        pagetext += "<form action=\"/profile/process\" method=\"post\">"
        pagetext += "<b>Password</b>:"
        pagetext += "<br>"
        pagetext += "<input type=\"password\" name=\"password\">"
        pagetext += "<br><br>"
        pagetext += "<b>Password</b> (enter again to verify):"
        pagetext += "<br>"
        pagetext += "<input type=\"password\" name=\"passwordverify\">"
        pagetext += "<br><br>"
        pagetext += "<input type=\"submit\" value=\"Change Your Email Address\">"
        pagetext += "</form>"
        return pageutils.generate_page ("Change Your Email Address", pagetext)
    password.exposed = True

    def processname (self, name=None):
        # Logged in users can edit their own data.
        # This page should also be known as /profile
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login/e")
        if (name == None):
            raise cherrypy.HTTPRedirect ("/profile/name/e")
        else:
            return self.process (name=name)
    processname.exposed = True

    def processemail (self, email=None):
         if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login/e")
        if (email == None):
            raise cherrypy.HTTPRedirect ("/profile/name/e")

        # Verify email address is plausibly valid.
        if (re.match (pageutils.emailregex, email) == None):
            raise cherrypy.HTTPRedirect ("/profile/email/invalid")

        return self.process (email=email)
    processemail.exposed = True

    def processurl (self, url=None):
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login/e")
        if (url == None):
            url = True
        
        return self.process (url=url)
    processurl.exposed = True

    def processpassword (self, password=None, passwordverify=None):
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login/e")
        if (password == None or passwordverify == None):
            raise cherrypy.HTTPRedirect ("/profile/password/e")
        
        # Remove leading/trailing spaces.
        password = string.strip (password)
        passwordverify = string.strip (passwordverify)

        # Verify passwords match.
        if (password <> passwordverify):
            raise cherrypy.HTTPRedirect ("/profile/password/verify")

        # Encypt the password.  
        password = crypt.crypt (password, "23")

        return self.process (password=password)
    processpassword.exposed = True

    def process (self, name=None, email=None, url=None, password=None):
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login/e")

        # One of the parameters should be non-null; otherwise, something is wrong.
        if (name == email == url == password == None):
            return pageutils.generate_page ("System Error",
                                            "<div class=\"error\">Unable to process request.</div>")

        # Get the user_id
        user_id = str(pageutils.get_user_id())
        if (user_id == None):
            return pageutils.generate_page ("System Error",
                                            "<div class=\"error\">Unable to process request.</div>")

        # Build the SQL query.
        query = ""
        if (email <> None):
            query = "UPDATE users SET email=%s WHERE user_id=%d", [email, int(user_id)]
        if (url == True):
            query = "UPDATE users SET url=NULL WHERE user_id=%d", [int(user_id)]
        elif (url <> None):
            query = "UPDATE users SET url=%s WHERE user_id=%d", [url, int(user_id)]
        if (password <> None):
            query = "UPDATE users SET password=%s WHERE user_id=%d", [password, int(user_id)]
        if (name <> None):
            query = "UPDATE users SET name=%s WHERE user_id=%d", [name, int(user_id)]
        
        # Run the database transaction.
        try:
            # Connect to the database and insert the values.
            dbconnection = pgdb.connect (database_connect_fields)
            dbcursor = dbconnection.cursor()
            dbcursor.execute (query)
            dbconnection.commit()
            
            # Close the database cursor and connection.
            dbcursor.close()
            dbconnection.close()

        except:
            # FIXME: this is a public user page; provide more interesting feedback in this event.
            return pageutils.generate_page ("Invalid SQL Query", "Invalid SQL Query!")
        raise cherrypy.HTTPRedirect ("/profile")
    process.exposed = True
