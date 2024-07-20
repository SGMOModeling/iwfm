# reach2shp.py
# Create stream reach shapefile for an IWFM model
# Copyright (C) 2020-2024 University of California
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


def reach2shp(reach_list, stnodes_dict, node_coords, shape_name, epsg=26910, 
        verbose=False):
    ''' reach2shp() - Creates an IWFM stream reaches shapefile from IWFM
        Preprocessor stream specification information

    TODO:
      - change from fiona to pyshp and wkt format?

    Parameters
    ----------
    reach_list : list
        list of elements and associated nodes
    
    stnodes_dict : dictionary
        key = stream node ID, values = [groundwater node, reach, elevation]
    
    node_coords : list
        list of nodes and associated X and Y coordinates
    
    shape_name : str
        base name for output shapefiles
    
    epsg : int, default=26910 (NAD 83 UTM 10, CA)
        EPSG projection
    
    verbose : bool, default=False
        True = command-line output on

    Returns
    -------
    nothing

    '''
    import iwfm as iwfm
    import fiona
    from shapely.geometry import mapping, LineString

    shapename = f'{shape_name}_StreamReaches.shp'

    schema = {
        'geometry': 'LineString',
        'properties': {'reach_id': 'int', 'flows_to': 'int'},
    }

    node_coords_dict = iwfm.list2dict(node_coords)

    with fiona.open(
            shapename,
            'w',
            crs=f'epsg:{epsg}',      #depricated: crs=fiona.crs.from_epsg(epsg),
            driver='ESRI Shapefile',
            schema=schema,
        ) as out:
        for i in range(len(reach_list)):
            upper, lower = reach_list[i][1], reach_list[i][2]
            points, n = [], 0
            for snode in range(upper, lower + 1):
                gw_node, reach, elev = stnodes_dict[snode]
                if gw_node != 0:
                    x, y = node_coords_dict[gw_node][0],node_coords_dict[gw_node][1]
                    points.append((x, y))
                    n += 1
            if points:
                line = LineString(points)
                properties = {
                    'reach_id': reach,
                    'flows_to': reach_list[i][3],
                    }
                feature = {'geometry': mapping(line), 'properties': properties}
                out.write(feature)
    if verbose:
        print(f'  Wrote shapefile {shapename}\n')
    return
