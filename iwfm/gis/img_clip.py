# img_clip.py
# Clips a raster file to a shapefile clipping mask
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


def img_clip(raster, clipshape, outfile):
    """img_clip() clips a raster file to a shapefile clipping mask"""
    from osgeo import gdal_array as gdal_array
    import gdal as gdal
    import shapefile  # pyshp
    from PIL import Image, ImageDraw, ImageOps  # pillow
    import iwfm as iwfm

    if clipshape[-4:] != ".shp":
        clipshape += ".shp"
    if outfile[-4:] != ".tif":
        outfile += ".tif"
    srcArray = gdal_array.LoadFile(raster)  # Load the source data as a gdal_array array
    srcImage = gdal.Open(
        raster
    )  # Also load as a gdal image to get geotransform (world file) info
    geoTrans = srcImage.GetGeoTransform()
    r = shapefile.Reader(clipshape)  # Use pyshp to open the shapefile

    (
        minX,
        minY,
        maxX,
        maxY,
    ) = r.bbox  # Convert the layer extent to image pixel coordinates
    ulX, ulY = iwfm.world2pixel(geoTrans, minX, maxY)
    lrX, lrY = iwfm.world2pixel(geoTrans, maxX, minY)

    pxWidth = int(lrX - ulX)  # Calculate the pixel size of the new image
    pxHeight = int(lrY - ulY)
    clip = srcArray[:, ulY:lrY, ulX:lrX]

    geoTrans = list(
        geoTrans
    )  # Create a new geomatrix for the image to contain georeferencing data
    geoTrans[0] = minX
    geoTrans[3] = maxY

    pixels = (
        []
    )  # Map points to pixels for drawing the county boundary on a blank 8-bit, black and white, mask image.
    for p in r.shape(0).points:
        pixels.append(iwfm.world2pixel(geoTrans, p[0], p[1]))
    rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
    rasterize = ImageDraw.Draw(
        rasterPoly
    )  # Create a blank image in PIL to draw the polygon.
    rasterize.polygon(pixels, 0)
    mask = iwfm.img_2_array(rasterPoly)  # Convert the PIL image to a NumPy array
    clip = gdal_array.numpy.choose(mask, (clip, 0)).astype(
        gdal_array.numpy.uint8
    )  # Clip the image using the mask
    output = gdal_array.SaveArray(
        clip, outfile, format="GTiff", prototype=raster
    )  # Save ndvi as tiff
    output = None
