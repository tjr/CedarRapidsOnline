# pageutils.py
# Page utilities for CedarRapidsOnline web service.
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

__sitename = "CedarRapidsOnline"

# Return a basic page header template, including header menu.
def generate_header (title=""):
    # Return value string.
    r = ""

    # Level of user logged-in-ness.
    # 0: Not logged in
    # 1: Logged in, regular user
    # 2: Logged in, admin user
    logged_in = 0
    
    window_title = __sitename
    
    # If there was no particular title specified, use the generic
    # sitename as the title; otherwise, combine the two.
    if (title == ""):
        title = _sitename
    else:
        window_title = title + " | " + __sitename

    r = "<html>\n"
    r += "<head>\n<title>" + window_title + "</title>\n</head>\n"
    r += "<link rel=\"stylesheet\" href=\"/css/site.css\" type=\"text/css\">"
    r += "</head>\n"
    r += "<body>\n"
    r += "<div class=\"page\">\n"

    r += "<div class=\"header\">\n"
    # r += "<h2><font color=\"#000099\">CedarRapidsOnline</font><font color=\"#d7831f\">.net</font></h2>\n"
    r += "<a href=\"/\"><img src=\"/images/cr.jpg\" class=\"logo\"></a>\n"

    r += "<hr>\n"
    
    r += generate_menu(logged_in)

    r += "</div>\n"

    r += "<hr>\n"
    
    r += "<div class=\"content\">\n"

    return r

# Print the main menu for the site.
# FIXME: currently filler material!
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
        r += "<a href=\"/logout\">Logout</a>"
    r += "<p>\n"
    return r

# Print the page footer, including closing out all HTML tags.
def generate_footer ():
    r = "</div>\n"
    r += "<hr><p class=\"footer\">Copyright &copy; 2009 Clear Perception Solutions LLC</p>\n"
    r += "</div></body></html>\n"
    return r

def generate_page (title = "", content = ""):
    return generate_header(title) + content + generate_footer()

