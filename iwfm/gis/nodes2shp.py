# nodes2shp.py
# Create node shapefiles for an IWFM model
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


def nodes2shp(node_coords, node_strat, nlayers, shape_name, verbose=0, debug=0):
    """ nodes2shp() creates an IWFM nodes shapefile """
    import sys
    import pandas as pd
    import geopandas as gpd

    node_shapename = f"{shape_name}_Nodes.shp"

    # calculate base altitude for each node
    base = []
    for i in range(0, len(node_strat)):
        temp = node_strat[i][1]  # gse
        for j in range(0, nlayers * 2):
            temp = temp - node_strat[i][j + 2]
        base.append(temp)

    # Create field names for layer properties
    field_names = []
    for i in range(0, nlayers):
        field_names.append("aqthick_" + str(i + 1))
        field_names.append("laythick_" + str(i + 1))

    # Create a pandas dataframe
    df = pd.DataFrame(
        {
            "node_id": [row[0] for row in node_strat],
            "gse": [row[1] for row in node_strat],
            "base": base,
            "easting": [row[0] for row in node_coords],
            "northing": [row[1] for row in node_coords],
        }
    )
    for i in range(
        0, nlayers * 2
    ):  # Add two fields for each layer (aquiclude thickness and aquifer thickness)
        df.insert(i + 2, field_names[i], [row[i + 2] for row in node_strat])
    if debug:
        print(" --> Created pandas dataframe for {}".format(node_shapename))

    # Convert pandas dataframe to geopandas geodataframe
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.easting, df.northing))
    gdf.crs = "epsg:26910"

    # Write a new node shapefile - EPSG 26910 = NAD 83 UTM 10
    gdf.to_file(node_shapename)
    if verbose:
        print("  Wrote shapefile {}".format(node_shapename))
    if debug:
        print("\n")

    return 1
