# shp_get.py
# Open a shapefile with PyShp
# Copyright (C) 2020-2021 University of California
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


def shp_get(infile):
    ''' shp_get() - Read a shapefile with PyShp

    Parameters
    ----------
    infile : str
        shapefile name

    Returns
    -------
    shp : Shapefile object

    '''
    import iwfm as iwfm

    return iwfm.gis.shp_get_PyShp(infile)
