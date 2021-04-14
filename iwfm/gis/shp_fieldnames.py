# shp_fieldnames.py
# Returns field names for a PyShp shapefile
# Copyright (C) 2020-2021 Hydrolytics LLC
# -----------------------------------------------------------------------------
# This information is free; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This work is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# For a copy of the GNU General Public License, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# -----------------------------------------------------------------------------


def shp_fieldnames(f):
    ''' shp_fieldnames() - Return the field names for PyShp shapefile
    
    Parameters
    ----------
    f: PyShp shapefile object
        shapefile

    Returns
    -------
    field_names : list of strings
        field names
        
    '''
    from shp_fields import shp_fields

    fields = shp_fields(f)
    field_names = []
    for item in fields[1:]:  # Omit 0: Deletion Flag
        field_names.append(item[0])
    return field_names
