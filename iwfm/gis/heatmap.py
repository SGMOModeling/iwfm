# heatmap.py
# Reads (x,y) points from a CSV file and creates a heatmap overlaid on a web map
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


def heatmap(infile, outfile, title):
    """heatmap() reads (x,y) points from a CSV file and creates a heatmap
    overlaid on a web map"""
    import folium
    from folium.plugins import HeatMap

    f = open(infile, "r")
    lines = f.readlines()
    lines.pop(0)
    data = []
    incidents = [list(map(float, l.strip().split(","))) for l in lines]
    m = folium.Map([32.75, -89.52], titles=title, zoom_start=7, max_zoom=7, min_zoom=7)
    HeatMap(incidents, max_zoom=16, radius=22, min_opacity=1, blur=30).add_to(m)
    m.save(outfile)
