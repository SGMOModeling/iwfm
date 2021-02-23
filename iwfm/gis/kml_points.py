# kml_points.py
# get point coords from KML file
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


def kml_points(filename, debug=0):
    """ get point coordinates from KML file"""
    from xml.dom import minidom  # python -m pip install xml

    kml = minidom.parse(filename)
    Placemarks = kml.getElementsByTagName("Placemark")
    if debug:
        print("=> Retrieved {} placemarks from '{}'".format(len(Placemarks), filename))
        print("Point\tCoordinates")
    points = []
    for i in range(0, len(Placemarks)):
        coordinates = Placemarks[i].getElementsByTagName("coordinates")
        point = coordinates[0].firstChild.data.split(",")
        points.append(point)
        if debug > 0:
            print(" {} \t{}".format(i, point))
    return points
