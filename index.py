# index.py
# Main index page for CedarRapidsOnline web service
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

# Subpages.
import articles
import discussions
import events
import profile
import admin
import register
import login
import logout

class HomePage:
    articles = articles.ArticlesPage()

    def index (self):
        return self.articles.index (article_slug="welcome")
    index.exposed = True

    def default (self, parameter=None):
        if (parameter == "404"):
            return pageutils.generate_page ("Page Not Found", "Page Not Found")
    default.exposed = True

root = HomePage()
root.articles = articles.ArticlesPage()
root.discussions = discussions.DiscussionsPage()
root.events = events.EventsPage()
root.profile = profile.ProfilePage()
root.register = register.RegisterPage()
root.login = login.LoginPage()
root.logout = logout.LogoutPage()
root.admin = admin.AdminPage()

cherrypy.tree.mount (root, config="site.conf")

if __name__ == "__main__":
    cherrypy.quickstart()

