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
                             str(result[sqlutils.getfieldindex("event_id", description)]) + "\">" +
                             result[sqlutils.getfieldindex("title", description)] + "</a> (" +
                             str(pageutils.get_month (start_date)) + " " + str(pageutils.get_day (start_date)))
                if (result[sqlutils.getfieldindex("end_date")] <> None):
                    pagetext += " - " + pageutils.get_month (end_date) + " " + str(pageutils.get_day (end_date))
                pagetext += ")</li>\n"
            pagetext += "</ul>\n"
            return pageutils.generate_page ("Events", pagetext)
                    
        # Show specific event.
        else:
            description = None
            results = None

            # Get event listing from database
            try:
                # Try to connect to the database.
                dbconnection = pgdb.connect (database_connect_fields)
                dbcursor = dbconnection.cursor()
                dbcursor.execute ("SELECT * FROM events WHERE event_id=%s", [str(event_id)])
                
                # Get the cursor description and results from the query.
                description = dbcursor.description
                results = dbcursor.fetchone()

                # Close the database cursor and connection.
                dbcursor.close()
                dbconnection.close()
            except:
                return pageutils.generate_page ("Database Error",
                                                "<div class=\"error\">Can't get event data.</div>\n")
            # Build the page.
            pagetext = ""
            start_date = result[sqlutils.getfieldindex("start_date", description)]
            end_date = result[sqlutils.getfieldindex("end_date", description)]
            pagetext += "<h3>" + pageutils.get_month (start_date) + " " + str(pageutils.get_day (start_date))
            if (end_date <> None):
                pagetext += " - " + pageutils.get_month (end_date) + " " + str(pageutils.get_day (end_date))
                pagetext += " " + pageutils.get_year (end_date)
            else:
                pagetext += " " + pageutils.get_year (start_date)
            pagetext += "<p>" + result[sqlutils.getfieldindex("description", description)]
            pagetitle = result[sqlutils.getfieldindex("title", description)]

            return pageutils.generate_page (pagetitle, pagetext)
    index.exposed = True

    def new (self, missing=False, title=None, description=None):
        # Create new event, available to logged in users.

        # Verify user is logged in.
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login")
        
        # Form to create new event.
        pagecontents = ""
        if (missing):
            pagecontents += "<div class=\"error\"><h2>Error</h2>Be sure to fill in both the "
            pagecontents += "title and description fields.</div>\n"
        pagecontents += "<form action=\"/events/process\" method=\"post\">"
        pagecontents += "<b>Title</b>:"
        pagecontents += "<br>"
        pagecontents += "<input type=\"text\" "
        if (title <> None):
            pagecontents += "value=\"" + title + "\" "
        pagecontents += "name=\"title\">"
        pagecontents += "<br><br>\n"
        pagecontents += "<b>Description</b>:"
        pagecontents += "<br>"
        pagecontents += "<textarea cols=80 rows=10 name=\"description\">"
        if (description <> None):
            pagecontents += description
        pagecontents += "</textarea>\n"
        pagecontents += "<br><br>"
        pagecontents += "<b>Start Date</b>:"
        pagecontents += "<br>"
        pagecontents += "<select name=\"start_month\">\n"
        for month in [["01", "January"], ["02", "February"], ["03", "March"], ["04", "April"],
                      ["05", "May"], ["06", "June"], ["07", "July"], ["08", "August"], ["09", "September"],
                      ["10", "October"], ["11", "November"], ["12", "December"]]:
            pagecontents += "<option value=\"" + month[0] + "\">" + month[1] + "</option>\n"
        pagecontents += "</select>\n"
        pagecontents += "<select name=\"start_day\">\n"
        for day in ["01", "02", "03", "04", "05", "06", "07", "08", "09",
                    "10", "11", "12", "13", "14", "15", "16", "17", "18",
                    "19", "20", "21", "22", "23", "24", "25", "26", "27",
                    "28", "29", "30", "31"]:
            pagecontents += "<option value=\"" + day + "\">" + day + "</option>\n"
        pagecontents += "</select>\n"
        pagecontents += "<select name=\"start_year\">\n"
        for year in ["2009", "2010", "2011", "2012"]:
            pagecontents += "<option value=\"" + year + "\">" + year + "</option>\n"
        pagecontents += "</select>\n"
        pagecontents += "<br><br>\n"
        pagecontents += "<b>End Date</b>: (<i>Leave blank for one-day events</i>)"
        pagecontents += "<br>"
        pagecontents += "<select name=\"end_month\">\n"
        for month in [["", ""], ["01", "January"], ["02", "February"], ["03", "March"], ["04", "April"],
                      ["05", "May"], ["06", "June"], ["07", "July"], ["08", "August"], ["09", "September"],
                      ["10", "October"], ["11", "November"], ["12", "December"]]:
            pagecontents += "<option value=\"" + month[0] + "\">" + month[1] + "</option>\n"
        pagecontents += "</select>\n"
        pagecontents += "<select name=\"end_day\">\n"
        for day in ["", "01", "02", "03", "04", "05", "06", "07", "08", "09",
                    "10", "11", "12", "13", "14", "15", "16", "17", "18",
                    "19", "20", "21", "22", "23", "24", "25", "26", "27",
                    "28", "29", "30", "31"]:
            pagecontents += "<option value=\"" + day + "\">" + day + "</option>\n"
        pagecontents += "</select>\n"
        pagecontents += "<select name=\"end_year\">\n"
        for year in ["", "2009", "2010", "2011", "2012"]:
            pagecontents += "<option value=\"" + year + "\">" + year + "</option>\n"
        pagecontents += "</select>\n"
        pagecontents += "<br><br>\n"
        pagecontents += "<input type=\"submit\" value=\"Create New Event\">"
        pagecontents += "</form>"
        return pageutils.generate_page ("Create New Event", pagecontents)
    new.exposed = True

    def process (self, title=None, description=None, start_month=None, start_day=None, start_year=None,
                 end_month=None, end_day=None, end_year=None):
        # Verify user is logged in.
        if (not pageutils.is_logged_in_p()):
            raise cherrypy.HTTPRedirect ("/login")

        # Make sure the title and description are present.
        if (title == None or description == None):
            return self.index (missing=True, title=title, description=description)

        # Prepare start/end date strings.
        start_date = start_year + "-" + start_month + "-" + start_day
        end_date = None
        if (end_year <> "" and end_month <> "" and end_day <> ""):
            end_date = end_year + "-" + end_month + "-" + end_day

        # Get the user_id.
        user_id = str(pageutils.get_user_id())

        # Insert the event into the database.
        try:
            # Connect to the database and insert the values.
            dbconnection = pgdb.connect (database_connect_fields)
            dbcursor = dbconnection.cursor()

            # Category value currently unused; default to 0.

            if (end_date <> None):
                dbcursor.execute ("INSERT INTO events (category, author_id, creation_date, title, " +
                                  "description, start_date, end_date, display) " +
                                  "VALUES (%s, %s, current_timestamp, %s, %s, %s, %s, %s)",
                                  ["0", user_id, title, description, start_date, end_date, "1"])
            else:
                dbcursor.execute ("INSERT INTO events (category, author_id, creation_date, title, " +
                                  "description, start_date, display) " +
                                  "VALUES (%s, %s, current_timestamp, %s, %s, %s, %s)",
                                  ["0", user_id, title, description, start_date, "1"])
            dbconnection.commit()

            # Close the database cursor and connection.
            dbcursor.close()
            dbconnection.close()
        except:
            return pageutils.generate_page ("Database Error",
                                            "<div class=\"error\">Unable to add event.</div>\n")
        raise cherrypy.HTTPRedirect ("/events/")
    process.exposed = True
