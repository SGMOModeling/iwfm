# shp2png_poly.py
# Save a shapefile as a raster filling in polygons
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


def shp2png_poly(shape, outfile, iwidth=800, iheight=600):
    ''' shp2png_poly() - Convert a shapefile to a raster and save as a
        PNG file, filling in polygon holes

    Parameters
    ----------
    shape : shapefile object
    
    outfile : str
        PNG image output file name
    
    iwidth : int, default=800
        image width in pixels
    
    iheight : int, default=600
        image height in pixels

    Returns
    -------
    nothing

    '''
    import iwfm as iwfm
    import pngcanvas as pngcanvas

    r = iwfm.shp_read(shapefile)  
    
    # Setup the world to pixels conversion
    xdist = shp.bbox[2] - shp.bbox[0]
    ydist = shp.bbox[3] - shp.bbox[1]
    xratio = iwidth / xdist
    yratio = iheight / ydist

    polygons = []
    for shape in shp.shapes():  
        # Loop through all parts to catch polygon holes!
        for i in range(len(shape.parts)):  
            pixels = []
            pt = None
            if i < len(shape.parts) - 1:
                pt = shape.points[shape.parts[i] : shape.parts[i + 1]]
            else:
                pt = shape.points[shape.parts[i] :]
            for x, y in pt:
                px = int(iwidth - ((shp.bbox[2] - x) * xratio))
                py = int((shp.bbox[3] - y) * yratio)
                pixels.append([px, py])
            polygons.append(pixels)

    c = pngcanvas.PNGCanvas(iwidth, iheight) 
    for p in polygons: 
        c.polyline(p)
    with open(outfile, 'wb') as f:  
        f.write(c.dump())
        f.close()
    return
