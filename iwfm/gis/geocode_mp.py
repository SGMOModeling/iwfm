# geocode_mp.py
# Multiprocessing to find multiple geocodes
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


def geocode_mp(cities):
    ''' geo_code() - Use multiprocessing to find and return multiple geocodes

    Parameters
    ----------
    cities : list
        list of city names to geocode

    Returns
    -------
    results : list
        geocodes for the input cities
    
    '''
    import mp
    from geocode import geocode

    pool = mp.Pool(processes=mp.cpu_count())  # allocate a pool of processors
    results = pool.map(geocode, cities)  # map function and input list to pool

    return results
