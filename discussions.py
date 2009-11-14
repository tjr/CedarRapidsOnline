# discussions.py
# Discussion pages for CedarRapidsOnline web service
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

class DiscussionsPage:
    def index (self, discussion_id=None):
        # If discussion_id is None, display main discussion table of contents.
        # Else, display specified discussion.
        # Available to all, logged in or not.
        pass
    index.exposed = True

    def comment (self, discussion_id):
        # Add comment to discussion, available to logged in users.
        pass
    comment.exposed = True

    def new (self):
        # Create new discussion, available to logged in users.
        pass
    new.exposed = True

