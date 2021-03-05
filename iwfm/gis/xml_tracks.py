# xml_tracks.py
# get tracking points from an XML file
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


def xml_tracks(filename, verbose=False):
    """xml_tracks() - Reproject from UTM to geographic coordinates

    Parameters:
      filename        (str):  Name of file continaing UTM coordinates
      verbose         (bool): Turn command-line output on or off

    Returns:
      tracks         (list)   Tracking points

    """
    from bs4 import BeautifulSoup

    gpx = open(filename)
    soup = BeautifulSoup(gpx.read(), features='xml')
    tracks = soup.findAll('trkpt')  # get all the tracking points from the file
    if verbose:
        print(f'=> Found {tracks} tracking points in {filename}')
    return tracks
