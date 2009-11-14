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

class EventsPage:

    def index (self, event_id=None):
        # If event_id is None, display main event table of contents.
        # Else, display specified event details.
        # Available to all, logged in or not.
        pass
    index.exposed = True

    def new (req):
        # Create new event, available to logged in users.
        pass
    new.exposed = True

    def admin_edit (req, event_id):
        # Edit specified event, available to ADMIN users.
        pass
    admin_edit.exposed = True
