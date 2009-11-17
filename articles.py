# articles.py
# Article pages for CedarRapidsOnline web service
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

class ArticlesPage:
    def index (self, article_slug=None):
        # If article_slug is None, display main article table of contents.
        # Else, display specified article.
        # Available to all, logged in or not.

        if (article_slug == None):
            article_slug = "map"

        description = None
        results = None
        comments_description = None
        comments_results = None
        author_results = []
        author_description = None
        # Try to connect to the database.
        try:
            dbconnection = pgdb.connect (database_connect_fields)
            dbcursor = dbconnection.cursor()
            dbcursor.execute ("SELECT * FROM articles WHERE slug=%s", [article_slug])
            # Get the cursor description and results from the query.
            description = dbcursor.description
            results = dbcursor.fetchone()

            # Get any comments for the article.
            if (results <> None):
                dbcursor.execute ("SELECT * FROM articles WHERE refers_to=%s",
                                  [str(results[sqlutils.getfieldindex ("article_id", description)])])
                comments_description = dbcursor.description
                comments_results = dbcursor.fetchall()
                for result in comments_results:
                    dbcursor.execute ("SELECT * FROM users WHERE user_id=%s",
                                      [str(result[sqlutils.getfieldindex ("author_id", comments_description)])])
                    author_description = dbcursor.description
                    author_results.append (dbcursor.fetchone())

            # Close the database cursor and connection.
            dbcursor.close()
            dbconnection.close()
        except:
            pass

        if (results == None):
            pass

        # Obtain the article title from the database results.
        pagetitle = ""
        try:
            pagetitle += results[sqlutils.getfieldindex ("title", description)]
        except:
            pagetitle = "Database Error."

        # Obtain the article body from the database results.
        pagetext = ""
        try:
            pagetext += results[sqlutils.getfieldindex ("body", description)]
        except:
            pagetext += "<p>Database Error.</p>"

        # Do we want to show comments on this page?
        if (int(results[sqlutils.getfieldindex ("display", description)]) > 1):
            pagetext += "<hr><h3>User Comments</h3>"
            if (comments_results <> None):
                for result in comments_results:
                    pagetext += "<p>"
                    pagetext += result[sqlutils.getfieldindex ("body", comments_description)]
                    for author in author_results:
                        if author[0] == result[sqlutils.getfieldindex ("author_id", comments_description)]:
                            pagetext += "<p><i>posted by " + author[sqlutils.getfieldindex ("name", author_description)]
                            pagetext += " on " + result[sqlutils.getfieldindex ("creation_date", comments_description)] + "</i></p>\n"
                    if (pageutils.is_admin_p()):
                        pagetext += "<p>[<a href=\"/admin/articles/delete/" + str(result[sqlutils.getfieldindex ("article_id", comments_description)]) + "\">Delete Comment</a>]</p>\n"
                    pagetext += "</p>"
                    pagetext += "<hr width=50%>\n"
            if (pageutils.is_logged_in_p()):
                pagetext += "<p><a href=\"/articles/comment/" + article_slug + "\">Add a comment</a></p>\n"
            else:
                pagetext += "<p><a href=\"/login\">Log in</a> to add a comment</a></p>\n"

        # Build the whole page and return it.
        return pageutils.generate_page (pagetitle, pagetext)
    index.exposed = True

    # We want to be able to have URLs like /articles/foo-article
    # The CherryPy index methods can't accept parameters like that, but
    # instead we route through the default method.  QED.
    def default(self, article_slug=None):
        return self.index (article_slug)
    default.exposed = True

    def comment (self, article_slug=None):
        # Verify user is logged in.
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login")

        if (article_slug == None):
            return pageutils.generate_page ("No Article Specified", "Unable to add comment.")

        # Form to add a comment.
        pagecontents = ""
        pagecontents += "<form action=\"/articles/addcomment\" method=\"post\">"
        pagecontents += "<textarea cols=80 rows=10 name=\"body\"></textarea>\n"
        pagecontents += "<br><br>"
        pagecontents += "<input type=\"hidden\" name=\"slug\" value=\"" + str(article_slug) + "\">"
        pagecontents += "<input type=\"submit\" value=\"Add Comment\">"
        pagecontents += "</form>"

        return pageutils.generate_page ("Add a comment", pagecontents)
    comment.exposed = True

    def addcomment (self, body, slug):
        # Verify user is logged in.
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login")
        
        # Remove any leading or trailing spaces from comment text.
        body = string.strip(body)

        user_id = pageutils.get_user_id()
        if (user_id == None):
            raise cherrypy.HTTPRedirect ("/login")
        
        try:
            # Connect to the database and insert the values.
            dbconnection = pgdb.connect (database_connect_fields)
            dbcursor = dbconnection.cursor()
            
            dbcursor.execute ("SELECT * FROM articles WHERE slug=%s", [slug])
            results = dbcursor.fetchone()
            if (results == None):
                return pageutils.generate_page ("Invalid Article Specified", "Unable to post comment.")
            article_id = results[0] # article_id is the first column in the table.

            dbcursor.execute ("INSERT INTO articles (author_id, body, display, refers_to, creation_date) " +
                              "VALUES (%s, %s, %s, %s, current_timestamp)",
                              [str(user_id), body, "1", str(article_id)])

            dbconnection.commit()

            # Close the database cursor and connection.
            dbcursor.close()
            dbconnection.close()
        except:
            return pageutils.generate_page ("Invalid SQL Query", "Unable to add comment.")
    addcomment.exposed = True

