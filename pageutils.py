# pageutils.py
# Page utilities for CedarRapidsOnline web service.
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

sitename = "CedarRapidsOnline"

emailregex = "^[a-zA-Z][\w\.-]*[a-zA-Z0-9]@[a-zA-Z0-9][\w\.-]*[a-zA-Z0-9]\.[a-zA-Z][a-zA-Z\.]*[a-zA-Z]$"

# Return true if current user is logged in.
def is_logged_in_p ():
    if (cherrypy.session.get('is_logged_in_p') == 'True'):
        return True
    else:
        return False

# Return true if current user is an admin.
def is_admin_p ():
    if (cherrypy.session.get('is_admin_p') == 'True' and is_logged_in_p()):
        return True
    else:
        return False

# Return string value of logged in user_id, None if not logged in.
def get_user_id ():
    if (is_logged_in_p()):
        return cherrypy.session['user_id']
    else:
        return None

# Set is_logged_in_p flag, and store user_id and admin flag. 
# Should be called upon login.
def set_logged_in (user_id, is_admin_p=False):
    cherrypy.session['is_logged_in_p'] = 'True'
    cherrypy.session['user_id'] = str (user_id)
    if (is_admin_p == True):
        cherrypy.session['is_admin_p'] = 'True'
    else:
        cherrypy.session['is_admin_p'] = 'False'

# Get year from a PostgreSQL timestamp.
def get_year (t):
    return t[0:4]

# Get month name from a PostgreSQL timestamp.
def get_month (t):
    m = int(t[5:7])
    if (m == 1):
        return "January"
    elif (m == 2):
        return "February"
    elif (m == 3):
        return "March"
    elif (m == 4):
        return "April"
    elif (m == 5):
        return "May"
    elif (m == 6):
        return "June"
    elif (m == 7):
        return "July"
    elif (m == 8):
        return "August"
    elif (m == 9):
        return "September"
    elif (m == 10):
        return "October"
    elif (m == 11):
        return "November"
    else:
        return "December"

# Get day from a PostgreSQL timestamp.
def get_day (t):
    return t[8:10]

# Return a basic page header template, including header menu.
def generate_header (title=""):
    # Return value string.
    r = ""

    # Level of user logged-in-ness.
    # 0: Not logged in
    # 1: Logged in, regular user
    # 2: Logged in, admin user
    logged_in = 0
    if (is_logged_in_p()):
        if (is_admin_p()):
            logged_in = 2
        else:
            logged_in = 1
    
    window_title = sitename
    
    # If there was no particular title specified, use the generic
    # sitename as the title; otherwise, combine the two.
    if (title == ""):
        title = sitename
    else:
        window_title = title + " | " + sitename

    r = "<html>\n"
    r += "<head>\n<title>" + window_title + "</title>\n</head>\n"
    r += "<link rel=\"stylesheet\" href=\"/css/site.css\" type=\"text/css\">"
    r += "</head>\n"
    r += "<body>\n"
    r += "<div class=\"page\">\n"

    r += "<div class=\"header\">\n"
    # r += "<h2><font color=\"#000099\">CedarRapidsOnline</font><font color=\"#d7831f\">.net</font></h2>\n"
    r += "<a href=\"/\"><img src=\"/images/cr.png\" class=\"logo\"></a>\n"

    r += "<hr>\n"
    
    r += generate_menu(logged_in)

    r += "</div>\n"

    r += "<hr>\n"

    r += "<h2>" + title + "</h2>\n"

    r += "<div class=\"content\">\n"

    return r

# Print the main menu for the site.
def generate_menu (logged_in=0):
    r = "<p class=\"menu\">"
    r += "<a href=\"/\">Home</a> | "
    r += "<a href=\"/articles/\">Articles</a> | "
    r += "<a href=\"/discussions/\">Discussions</a> | "
    r += "<a href=\"/events/\">Events</a> | "
    if (logged_in == 0):
        r += "<a href=\"/login\">Login</a> | "
        r += "<a href=\"/register\">Register</a>"
    elif (logged_in == 2):
        r += "<a href=\"/admin/\">Admin</a> | "
    if (logged_in > 0):
        r += "<a href=\"/profile\">My Profile</a> | "
        r += "<a href=\"/logout\">Logout</a>"
    r += "<p>\n"
    return r

# Print the page footer, including closing out all HTML tags.
def generate_footer ():
    r = "</div>\n"
    r += "<hr><p class=\"footer\">Copyright &copy; 2009 Clear Perception Solutions LLC\n"
    r += "<br><a href=\"mailto:cedarrapids@clearperception.net\" class=\"footer\">cedarrapids@clearperception.net</a></p>\n"
    r += "</div></body></html>\n"
    return r

def generate_page (title = "", content = ""):
    return generate_header(title) + content + generate_footer()

# Generate disclaimer for user-contributed content.
def generate_disclaimer ():
    return ("<p>Please keep your contributions on-topic and family-friendly. " +
            "Any content you contribute to this site can be removed at the sole " +
            "discretion of the site administrators. Thanks!</p>")
