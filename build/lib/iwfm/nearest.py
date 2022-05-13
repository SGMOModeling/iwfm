# nearest.py
# Return nearest IWFM node to an (x,y) location
# the nearest node to each (x,y) point
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


def nearest(d_nodes, x, y):
    ''' nearest() - Find the nearest node to a point from a node dictionary

    Parameters
    ----------
    d_nodes : dictionary
        key = model node, value = x and y locations
    
    x : float
        x location of point
    
    y : float
        y location of point

    Returns
    -------
    nearest : int
        node ID of node closest to (x,y)
    
    '''
    import iwfm as iwfm

    point = [x, y]
    dist = 9.9e30
    nearest = -1
    for key in d_nodes:
        pt = d_nodes[key]
        new_dist = iwfm.distance(point, pt)
        if dist > new_dist:
            dist = new_dist
            nearest = key
    return nearest
