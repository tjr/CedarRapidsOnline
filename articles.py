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

import sqlutils
import pageutils

__database_connect_fields = sqlutils.__database_connect_fields

class ArticlesPage:
    def index (self, article_slug=None):
        # If article_slug is None, display main article table of contents.
        # Else, display specified article.
        # Available to all, logged in or not.

        if (article_slug == None):
            article_slug = "map"

        description = None
        results = None
        # Try to connect to the database.
        try:
            dbconnection = pgdb.connect (__database_connect_fields)
            dbcursor = dbconnection.cursor()
            dbcursor.execute ("SELECT * FROM articles WHERE slug=:1", [article_slug])
            # Get the cursor description and results from the query.
            description = dbcursor.description()
            results = dbcursor.fetchone()
            
            # Close the database cursor and connection.
            dbcursor.close()
            dbconnection.close()
        except:
#            cherrypy.redirect ("/404")
            pass

        if (results == None):
            #cherrypy.redirect ("/404")
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
    
        # Build the whole page and return it.
        return pageutils.generate_page (pagetitle, pagetext)
    index.exposed = True

    def comment (self, article_id):
        # Add comment to article, available to logged in users.
        pass
    comment.exposed = True

