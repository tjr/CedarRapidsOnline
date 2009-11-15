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

class AdminUsersPage:
    def index (self):
        # Present listing of all users.
        return "ADMIN: Present listing of all users."
    index.exposed = True

    def edit (self, user_id=None):
        # Edit form for given user.
        return "ADMIN: Edit form for given user."
    edit.exposed = True

class AdminArticlesPage:
    def index (self):
        # Present listing of all articles.
        return "ADMIN: Present listing of all articles."
    index.exposed = True

    def new (self):
        # Create new article.
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

    def edit (self, article_id = None):
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
        # No reason to present listing of events, as this is available
        # from the main public view.
        return "ADMIN: Select admin EDIT from a particular event."
    index.exposed = True

    def edit (self, event_id=None):
        # Edit form for given event.
        return "ADMIN: Edit form for given event."
    edit.exposer = True

class AdminPage:
    def __init__(self):
        # Set up the nested admin page classes.  No reason
        # to maintain these from the top-level index.py file.
        self.users = AdminUsersPage()
        self.articles = AdminArticlesPage()
        self.discussions = AdminDiscussionsPage()
        self.events = AdminEventsPage()

    def index (self):
        # Present menu of administrative activities
        return """
             <a href=\"/admin/users/\">Users Admin</a><p>
             <a href=\"/admin/articles/\">Articles Admin</a><p>
             <a href=\"/admin/discussions/\">Discussions Admin</a><p>
             <a href=\"/admin/events/\">Events Admin</a>"""
    index.exposed = True
