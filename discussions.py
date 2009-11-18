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
    def default(self, discussion_id=None):
        # We want to be able to have URLs like /discussions/discussion-id
        # The CherryPy index methods can't accept parameters like that, but
        # instead we route through the default method.  QED.
        return self.index (discussion_id)
    default.exposed = True

    def index (self, discussion_id=None):
        # If discussion_id is None, display main discussion table of contents.
        # Else, display specified discussion.
        # Available to all, logged in or not.
        
        # Toplevel index.
        if (discussion_id == None):
            description = None
            results = None
            author_description = None
            author_results = []

            # Get discussion listing from database
            try:
                # Try to connect to the database.
                dbconnection = pgdb.connect (database_connect_fields)
                dbcursor = dbconnection.cursor()
                dbcursor.execute ("SELECT * FROM discussions WHERE refers_to IS null ORDER BY creation_date")
                
                # Get the cursor description and results from the query.
                description = dbcursor.description
                results = dbcursor.fetchall()

                # Get and store the user (author) data.
                for result in results:
                    dbcursor.execute ("SELECT * FROM users WHERE user_id=%s",
                                      [str(result[sqlutils.getfieldindex("author_id", description)])])
                    if (dbcursor.description <> None):
                        author_description = dbcursor.description
                    author_results.append (dbcursor.fetchone())

                # Close the database cursor and connection.
                dbcursor.close()
                dbconnection.close()
            except:
                return pageutils.generate_page ("Database Error",
                                                "<div class=\"error\">Can't get discussion data.</div>\n")

            pagetext = "<a href=\"/discussions/new\">Start New Discussion</a>\n"
            pagetext += "<ul>\n"
            for result in results:
                pagetext += "<li>\n"
                pagetext += ("<a href=\"/discussions/" +
                             str(result[sqlutils.getfieldindex ("discussion_id", description)]) +
                             "\">" + result[sqlutils.getfieldindex ("subject", description)] + "</a> (posted by ")
                for author in author_results:
                    if author == None:
                        continue
                    if author[0] == result[sqlutils.getfieldindex ("author_id", description)]:
                        pagetext += author[sqlutils.getfieldindex ("name", author_description)]
                pagetext += " on " + result[sqlutils.getfieldindex ("creation_date", description)] + ")\n"
                pagetext += "</li>\n"
            pagetext += "</ul>\n"
            return pageutils.generate_page ("Discussions", pagetext)
        else:
            pass
    index.exposed = True

    def comment (self, discussion_id=None):
        # Verify user is logged in.
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login")
        
        # Verify a discussion_id was supplied, so we know where this comment goes.
        if (discussion_id == None):
            return pageutils.generate_page ("Discussion Reference Missing",
                                            "<div class=\"error\"><p>Unable to add comment.</p></div>")

        pagetext = ""
        pagetitle = "Add a Comment"

        pagetext += "<form action=\"/discussions/process\" method=\"post\">"
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
            raise cherrypy.HTTPRedirect ("/login/access")
        
        pagetext = ""
        pagetitle = "Start a New Discussion"

        pagetext += "<form action=\"/discussions/process\" method=\"post\">"
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

    def process (self, body=None, subject=None, refers_to=None):
        # Verify user is logged in.
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login/access")

        # FIXME: Make sure we have all of the data we need in the form.

        # Remove any leading or trailing spaces from comment text.
        body = string.strip(body)
        subject = string.strip(subject)

        # Make sure refers_to, if it exists, is an integer.
        if (refers_to <> None):
            try:
                refers_to = str(int(refers_to))
            except:
                return pageutils.generate_page ("Invalid Reference",
                                                "<div class=\"error\">Unable to add discussion element.</div>\n")

        user_id = pageutils.get_user_id()
        if (user_id == None):
            raise cherrypy.HTTPRedirect ("/login/access")
        
        # Insert the discussion / comment into the database.
        try:
            # Connect to the database and insert the values.
            dbconnection = pgdb.connect (database_connect_fields)
            dbcursor = dbconnection.cursor()

            # Category value currently unused; default to 0.

            # Is this a top-level discussion?
            if (refers_to == None):
                dbcursor.execute ("INSERT INTO discussions (category, author_id, subject, body, display, creation_date) " +
                                  "VALUES (%s, %s, %s, %s, %s, current_timestamp)",
                                  ["0", str(user_id), subject, body, "1"])
            # Or is this a reply?
            else:
                dbcursor.execute ("INSERT INTO discussions (refers_to, category, author_id, subject, body, display, creation_date) " +
                                  "VALUES (%s, %s, %s, %s, %s, %s, current_timestamp)",
                                  [str(refers_to), "0", str(user_id), subject, body, "1"])

            dbconnection.commit()

            # Close the database cursor and connection.
            dbcursor.close()
            dbconnection.close()
        except:
            return pageutils.generate_page ("Database Error",
                                            "<div class=\"error\">Unable to add discussion element.</div>\n")
        
        if (refers_to == None):
            raise cherrypy.HTTPRedirect ("/discussions/")
        else:
            raise cherrypy.HTTPRedirect ("/discussions/" + str(refers_to))
    process.exposed = True
