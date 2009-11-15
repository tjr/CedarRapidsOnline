# admin.py
# Admin pages for CedarRapidsOnline web service
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

database_connect_fields = sqlutils.database_connect_fields

class AdminUsersPage:
    def index (self):
        # Verify user is logged-in admin.
        if (not pageutils.is_admin_p()):
            raise cherrypy.HTTPRedirect ("/")

        # Present listing of all users.
        return "ADMIN: Present listing of all users."
    index.exposed = True

    def edit (self, user_id=None):
        # Verify user is logged-in admin.
        if (not pageutils.is_admin_p()):
            raise cherrypy.HTTPRedirect ("/")

        # Edit form for given user.
        return "ADMIN: Edit form for given user."
    edit.exposed = True

class AdminArticlesPage:
    def index (self):
        # Verify user is logged-in admin.
        if (not pageutils.is_admin_p()):
            raise cherrypy.HTTPRedirect ("/")

        # Present listing of all articles.
        return pageutils.generate_page ("Articles Administration", "<a href=\"/admin/articles/new\">New</a>")
    index.exposed = True

    def new (self):
        # Verify user is logged-in admin.
        if (not pageutils.is_admin_p()):
            raise cherrypy.HTTPRedirect ("/")

        # Form to create new article.
        pagecontents = ""
        pagecontents += "<form action=\"/admin/articles/processnew\" method=\"post\">"
        pagecontents += "<b>Title</b>:"
        pagecontents += "<br>"
        pagecontents += "<input type=\"text\" name=\"title\">"
        pagecontents += "<br><br>\n"
        pagecontents += "<b>Slug</b>:"
        pagecontents += "<br>"
        pagecontents += "<input type=\"text\" name=\"slug\">"
        pagecontents += "<br><br>"
        pagecontents += "<b>Display</b>: (0, 1, or 2 only)"
        pagecontents += "<br>"
        pagecontents += "<input type=\"text\" name=\"display\">"
        pagecontents += "<br><br>"
        pagecontents += "<b>Body</b>:"
        pagecontents += "<br>"
        pagecontents += "<textarea cols=80 rows=10 name=\"body\"></textarea>\n"
        pagecontents += "<br>"
        pagecontents += "<input type=\"submit\" value=\"Create New Article\">"
        pagecontents += "</form>"

        return pageutils.generate_page ("Create New Article", pagecontents)
    new.exposed = True
    
    def processnew (self, title=None, slug=None, display=None, body=None):
        # Verify user is logged-in admin.
        if (not pageutils.is_admin_p()):
            raise cherrypy.HTTPRedirect ("/")

        # If we got to this page through the /admin/articles/new form, all fields
        # should be filled in.  If they aren't, something unexpected happened, and
        # we shouldn't continue processing the form.
        if (title == None or slug == None or display == None or body == None):
            return pageutils.generate_page ("Invalid Input for New Article",
                                            "Invalid Input for New Article!")
        else:
            # Remove any leading or trailing spaces.
            title = string.strip (title)
            slug = string.strip (slug)
            body = string.strip (body)
            display = string.strip (display)
            author_id = pageutils.get_user_id()

            try:
                # Connect to the database and insert the values.
                dbconnection = pgdb.connect (database_connect_fields)
                dbcursor = dbconnection.cursor()
                dbcursor.execute ("INSERT INTO articles (title, author_id, slug, body, display, creation_date) " +
                                  "VALUES (%s, %s, %s, %s, %s, current_timestamp)",
                                  [title, author_id, slug, body, display])
                dbconnection.commit()

                # Close the database cursor and connection.
                dbcursor.close()
                dbconnection.close()
            except:
                return pageutils.generate_page ("Invalid SQL Query", "Invalid SQL Query!")
        
        raise cherrypy.HTTPRedirect ("/admin/articles/")
    processnew.exposed = True

    def edit (self, article_id = None):
        # Verify user is logged-in admin.
        if (not pageutils.is_admin_p()):
            raise cherrypy.HTTPRedirect ("/")

        # Edit form for given article.
        return "ADMIN: Edit form for given article."
    edit.exposed = True

class AdminDiscussionsPage:
    def index (self):
        # No reason to present listing of discussions, as this is
        # available from the main public view.
        return "ADMIN: Select admin EDIT from a particular discussion."
    index.exposed = True

    def edit (self, discussion_id=None):
        # Edit form for given discussion.
        return "ADMIN: Edit form for given discussion."
    edit.exposed = True

class AdminEventsPage:
    def index (self):
        # Verify user is logged-in admin.
        if (not pageutils.is_admin_p()):
            raise cherrypy.HTTPRedirect ("/")

        # No reason to present listing of events, as this is available
        # from the main public view.
        return "ADMIN: Select admin EDIT from a particular event."
    index.exposed = True

    def edit (self, event_id=None):
        # Verify user is logged-in admin.
        if (not pageutils.is_admin_p()):
            raise cherrypy.HTTPRedirect ("/")

        # Edit form for given event.
        return "ADMIN: Edit form for given event."
    edit.exposed = True

class AdminPage:
    def __init__(self):
        # Set up the nested admin page classes.  No reason
        # to maintain these from the top-level index.py file.
        self.users = AdminUsersPage()
        self.articles = AdminArticlesPage()
        self.discussions = AdminDiscussionsPage()
        self.events = AdminEventsPage()

    def index (self):
        # Verify user is logged-in admin.
        if (not pageutils.is_admin_p()):
            raise cherrypy.HTTPRedirect ("/")

        # Present menu of administrative activities
        return """
             <a href=\"/admin/users/\">Users Admin</a><p>
             <a href=\"/admin/articles/\">Articles Admin</a><p>
             <a href=\"/admin/discussions/\">Discussions Admin</a><p>
             <a href=\"/admin/events/\">Events Admin</a>"""
    index.exposed = True
