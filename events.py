# events.py
# Event pages for CedarRapidsOnline web service
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

class EventsPage:
    def default(self, event_id=None):
        # We want to be able to have URLs like /events/event-id
        # The CherryPy index methods can't accept parameters like that, but
        # instead we route through the default method.  QED.
        return self.index (event_id)
    default.exposed = True

    def index (self, event_id=None):
        # If event_id is None, display main event table of contents.
        # Else, display specified event details.
        # Available to all, logged in or not.
        
        # Build table of contents.
        if (event_id == None):
            description = None
            results = None

            # Get event listing from database
            try:
                # Try to connect to the database.
                dbconnection = pgdb.connect (database_connect_fields)
                dbcursor = dbconnection.cursor()
                dbcursor.execute ("SELECT * FROM events ORDER BY start_date")
                
                # Get the cursor description and results from the query.
                description = dbcursor.description
                results = dbcursor.fetchall()

                # Close the database cursor and connection.
                dbcursor.close()
                dbconnection.close()
            except:
                return pageutils.generate_page ("Database Error",
                                                "<div class=\"error\">Can't get event data.</div>\n")
            # Build the page.
            pagetext = "<ul>\n"
            for result in results:
                start_date = result[sqlutils.getfieldindex("start_date", description)]
                end_date = result[sqlutils.getfieldindex("end_date", description)]
                pagetext += ("<li>" + "<a href=\"/events/" +
                             result[sqlutils.getfieldindex("event_id", description)] + "\">" +
                             result[sqlutils.getfieldindex("title", description)] + "</a> (" +
                             pageutils.get_month (start_date) + " " + pageutils.get_day (start_date))
                if (result[sqlutils.getfieldindex("end_date")] <> None):
                    pagetext += " - " + pageutils.get_month (end_date) + " " + pageutils.get_day (end_date)
                pagetext += ")</li>\n"
                    
        # Show specific event.
        else:
            pass
    index.exposed = True

    def new (self):
        # Create new event, available to logged in users.
        pass
    new.exposed = True

