# iwfm_aquitard_thickness.py
# Extract aquitard thickness from IWFM stratigraphy information
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


def iwfm_aquitard_thickness(strat):
    ''' iwfm_aquitard_thickness() - Extract aquitard thicknesses from 
        IWFM stratigraphy information

    Parameters
    ----------
    strat : list
        stratigraphy for each model node

    Returns
    -------
    aquitard_thick : list
        aquitard thickness for each model layer and node
    '''
    import iwfm as iwfm

    aquitard_thick, _ = iwfm.iwfm_strat_arrays(strat)
    return aquitard_thick
