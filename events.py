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
            most_recent_month = None
            for result in results:
                start_date = result[sqlutils.getfieldindex("start_date", description)]
                end_date = result[sqlutils.getfieldindex("end_date", description)]
                if (most_recent_month <> pageutils.get_month (start_date)):
                    most_recent_month = start_date
                    pagetext += "<h3>" + most_recent_month + "</h3>\n"
                pagetext += ("<li>" + "<a href=\"/events/" +
                             result[sqlutils.getfieldindex("event_id", description)] + "\">" +
                             result[sqlutils.getfieldindex("title", description)] + "</a> (" +
                             pageutils.get_month (start_date) + " " + pageutils.get_day (start_date))
                if (result[sqlutils.getfieldindex("end_date")] <> None):
                    pagetext += " - " + pageutils.get_month (end_date) + " " + pageutils.get_day (end_date)
                pagetext += ")</li>\n"
            pagetext += "</ul>\n"
            return pageutils.generate_page ("Events", pagetext)
                    
        # Show specific event.
        else:
            pass
    index.exposed = True

    def new (self):
        # Create new event, available to logged in users.

        # Verify user is logged in.
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login")
        
        # Form to create new event.
        pagecontents = ""
        pagecontents += "<form action=\"/events/process\" method=\"post\">"
        pagecontents += "<b>Title</b>:"
        pagecontents += "<br>"
        pagecontents += "<input type=\"text\" name=\"title\">"
        pagecontents += "<br><br>\n"
        pagecontents += "<b>Description</b>:"
        pagecontents += "<br>"
        pagecontents += "<textarea cols=80 rows=10 name=\"description\"></textarea>\n"
        pagecontents += "<br><br>"
        pagecontents += "<b>Start Date</b>:"
        pagecontents += "<br>"
        pagecontents += "<select name=\"start_month\">\n"
        for month in [["01", "January"], ["02", "February"], ["03", "March"], ["04", "April"],
                      ["05", "May"], ["06", "June"], ["07", "July"], ["08", "August"], ["09", "September"],
                      ["10", "October"], ["11", "November"], ["12", "December"]]:
            pagecontents += "<option value=\"" + month[0] + "\">" + month[1] + "</option>\n"
        pagecontents += "</select>\n"
        pagecontents += "<select name=\"start_month\">\n"
        for day in ["01", "02", "03", "04", "05", "06", "07", "08", "09",
                    "10", "11", "12", "13", "14", "15", "16", "17", "18",
                    "19", "20", "21", "22", "23", "24", "25", "26", "27",
                    "28", "29", "30", "31"]:
            pagecontents += "<option value=\"" + day + "\">" + day + "</option>\n"
        pagecontents += "</select>\n"
        pagecontents += "<select name=\"start_month\">\n"
        for year in ["2009", "2010", "2011", "2012"]:
            pagecontents += "<option value=\"" + year + "\">" + year + "</option>\n"
        pagecontents += "</select>\n"
        pagecontents += "<br><br>\n"
        pagecontents += "<input type=\"submit\" value=\"Create New Event\">"
        pagecontents += "</form>"
        return pageutils.generate_page ("Create New Event", pagecontents)
    new.exposed = True

