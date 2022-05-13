# shp_getcol_lg.py
# Returns one column for a PyShp shapefile
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


def shp_getcol_lg(f, col):
    ''' shp_getcol_lg() - Return one column from the shapefile table.
        Works better than shp_getcol() for large DBF files

    Parameters
    ----------
    f : PyShp shapefile object
    
    col : int
        column number

    Returns
    -------
    data : list
        items from specified column

    '''
    import iwfm as iwfm

    recs = iwfm.shp_recno(f)
    data = []
    for i in range(recs):
        r = iwfm.gis.shp_getrec_lg(f, i)
        data.append(r[col])
    return data
