# index.py
# Main index page for CedarRapidsOnline web service
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
import pageutils

# Subpages.
import articles
import discussions
import events
import users
import admin


class HomePage:
    def index (self):
        return pageutils.generate_page("Welcome", """
           <a href="/articles/">Articles</a><p>
           <a href="/discussions/">Discussions</a><p>
           <a href="/events/">Events</a><p>
           <a href="/users/">Users</a><p>
           <a href=\"/admin\">Admin</a><p>
           """)
    index.exposed = True

    def register (self):
        return pageutils.generate_page ("Register as a New User",
                                        "Registration Page")
    register.exposed = True

    def login (self):
        return pageutils.generate_page ("Login",
                                        "Login")
    login.exposed = True

    def logout (self):
        return pageutils.generate_page ("Logout",
                                        "Logout")
    logout.exposed = True

root = HomePage()
root.articles = articles.ArticlesPage()
root.discussions = discussions.DiscussionsPage()
root.events = events.EventsPage()
root.users = users.UsersPage()
root.admin = admin.AdminPage()
cherrypy.tree.mount (root, config="site.conf")

if __name__ == "__main__":
    import os.path
    thisdir = os.path.dirname(__file__)
    cherrypy.quickstart()

