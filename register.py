# register.py
# User registration pages for CedarRapidsOnline web service
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
import crypt
import string
import pageutils
import sqlutils
import re

database_connect_fields = sqlutils.database_connect_fields

class RegisterPage:
    def index (self, errormissing=False, errorverify=False, errorduplicate=False, erroremail=False):
        pagetext = ""
        
        # Handle error cases from previous attempts.
        if (errormissing or errorverify):
            pagetext += "<div class=\"error\"><h2>Error</h2>\n"
            pagetext += "<ul>\n"
            if (errormissing):
                pagetext += "<li>Please complete all required fields.</li>\n"
            if (errorverify):
                pagetext += "<li>Both Password entries must match, to ensure password is stored correctly.</li>\n"
            if (errorduplicate):
                pagetext += "<li>Email address provided already on record; perhaps you already have an account and just need to <a href=\"/login\">log in</a>?</li>\n"
            if (erroremail):
                pagetext += "<li>Please enter a valid email address, in the form: user@bar.baz</li>\n"
            pagetext += "</ul></div>\n"
            
        pagetext += """
    <p>
    In order to participate in this web site's discussion forums
    and post your comments on articles, we ask that you register as
    a user on the site.
    </p>

    <p>
    Registration is free, and we only require
    you to give us your name (as you want it to appear on the site),
    your email address (which will not appear on the site), and select
    a password to use for logging in.
    </p>

    <p>
    You may also provide us with the address of your website, if you
    have one.  This information is optional.
    </p>"""

        pagetext += "<form action=\"/register/process\" method=\"post\">"
        pagetext += "<b>Name</b>:"
        pagetext += "<br>"
        pagetext += "<input type=\"text\" name=\"name\">"
        pagetext += "<br><br>"
        pagetext += "<b>Email Address</b>:"
        pagetext += "<br>"
        pagetext += "<input type=\"text\" name=\"email\">"
        pagetext += "<br><br>"
        pagetext += "<b>Password</b>:"
        pagetext += "<br>"
        pagetext += "<input type=\"password\" name=\"password\">"
        pagetext += "<br><br>"
        pagetext += "<b>Password</b> (enter again to verify):"
        pagetext += "<br>"
        pagetext += "<input type=\"password\" name=\"passwordverify\">"
        pagetext += "<br><br>"
        pagetext += "<b>Website</b>: (optional)"
        pagetext += "<br>"
        pagetext += "<input type=\"text\" name=\"url\">"
        pagetext += "<br><br>"
        pagetext += "<input type=\"submit\" value=\"Register!\">"
        pagetext += "</form>"
        return pageutils.generate_page ("Register as a New User", pagetext)
    index.exposed = True

    def process (self, name=None, email=None, password=None, passwordverify=None, url=None):
        # If we got to this page through the /register form, all fields should be filled
        # in, with the possible exception of URL, which is optional.  If they aren't all
        # filled in, then something unexpected happened, and we shouldn't continue processing
        # the form.
        if (name == None or email == None or password == None or passwordverify == None):
            return self.index (errormissing = True)
        else:
            # Replace single quotes with two single quotes.
            name = sqlutils.quote (str(name))
            email = sqlutils.quote (str(email))
            password = sqlutils.quote (str(password))
            passwordverify = sqlutils.quote (str(passwordverify))
            url = sqlutils.quote (str(url))
            level = "1" # default level for regular user.

            # Verify all required fields are filled in.
            if (name == '' or email == '' or password == '' or passwordverify == ''):
                return self.index (errormissing = True)

            # Verify email address is plausibly valid.
            if (re.match (pageutils.emailregex, email) == None):
                return self.index (erroremail = True)

            # Verify passwords match.
            if (password <> passwordverify):
                return self.index (errorverify = True)

            # Encypt the password.  Once we do this, we can't get the original
            # password back out of the database, so we can't send the original
            # password back to the user if they lose it.  We can generate a new
            # password and send them that.
            password = crypt.crypt (password, "23")

            # Add http:// to the URL if needed.
            if (url[0:7] =="http://" or url == ""):
                pass
            else:
                url = "http://" + url

            # FIXME: ensure that email address hasn't already been used in database.
            try:
                dbconnection = pgdb.connect (database_connect_fields)
                dbcursor = dbconnection.cursor()
                dbcursor.execute ("SELECT * FROM users WHERE email=%s", [email])
                
                results = dbcursor.fetchone()

                # Close the database cursor and connection.
                dbcursor.close()
                dbconnection.close()

                if (results <> None):
                    return self.index (errorduplicate=True)
            except:
                return pageutils.generate_page ("Database Error", "Database Error")

            try:
                # Connect to the database and insert the values.
                dbconnection = pgdb.connect (database_connect_fields)
                dbcursor = dbconnection.cursor()
                dbcursor.execute ("INSERT INTO users (name, email, password, url, level) " +
                                  "VALUES (%s, %s, %s, %s, %s)",
                                  [name, email, password, url, level])
                dbconnection.commit()

                # Close the database cursor and connection.
                dbcursor.close()
                dbconnection.close()

                # FIXME: automatically log user in.
            except:
                # FIXME: this is a public user page; provide more interesting feedback in this event.
                return pageutils.generate_page ("Invalid SQL Query", "Invalid SQL Query!")
        
        raise cherrypy.HTTPRedirect ("/register/thanks")
    process.exposed = True

    def thanks (self):
        return pageutils.generate_page ("Thanks for Registering!",
                                        "<p>Thanks for registering! You can now <a href=\"/login\">login " +
                                        "to your account</a>.</p>")
    thanks.exposed = True
