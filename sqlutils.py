# sqlutils.py
# SQL utilities and data for CedarRapidsOnline web service
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

__database_connect_fields = "host:database:username:password"

# The PGDB implementation lets users access columns in a returned
# row via index number rather than field name. This is rather annoying
# to me; I don't want to have to memorize the significance of index
# numbers for database tables.  This function takes a desired field name
# and a PGDB cursor description and returns the appropriate index, or None
# if no such index exists.
#
# "None" is an invalid array index; be sure to wrap calls to this in try/except
# blocks to prevent traceback errors in case there's no index to return.
def getfieldindex (fieldname, dbdescription):
    if fieldname == "" or dbdescription == None:
        return None
    for fieldposition in range(len(dbdescription)):
        if dbdescription[fieldposition][0] == fieldname:
            return fieldposition
    return None

