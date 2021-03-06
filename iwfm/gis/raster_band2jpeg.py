# raster_band2jpeg.py
# Extract raster band to jpeg file
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


def raster_band2jpeg(infile, band, outfile):
    """ raster_band2jpeg(): extract a raster band to a jpeg"""
    from osgeo import gdal_array as gdal_array

    srcArray = gdal_array.LoadFile(infile)
    band = srcArray[band - 1]
    gdal_array.SaveArray(band, outfile, format='JPEG')
    return
