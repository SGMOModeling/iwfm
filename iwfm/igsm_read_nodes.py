# igsm_read_nodes.py
# Read an IGSM pre-processor node file
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


def igsm_read_nodes(node_file):
    ''' igsm_read_nodes() - Read the nodal coordinates from the nodes file

    Parameters
    ----------
    node_file : str
        IGSM preprocessor node file

    Returns
    -------
    node_coord : list
        nodes and x,y coordinates
    
    node_list : list
        nodes
        
    '''
    import iwfm as iwfm

    node_coord, node_list = iwfm.iwfm_read_nodes(node_file)
    return node_coord, node_list
