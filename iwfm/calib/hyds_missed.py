# hyds_missed.py
# Compare lists of sites and return the sites from each list that are not
# in the other list
# Copyright (C) 2020-2023 University of California
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


def hyds_missed(sim_sites,obs_sites):
    ''' hyds_missed() - compare lists of sites and return the sites
        from each list that are not in the other list

    Parameters
    ----------
    sim_sites : list of strings
        simulation sites

    obs_sites : list of strings
        observation sites

    Returns
    -------
    sim_miss : list of strings
        simulation sites not in obs_sites

    obs_miss : list of strings
        observation sites not in sim_sites

    '''
    import iwfm as iwfm
    sim_miss, both = iwfm.compare(sim_sites,obs_sites)
    obs_miss, both = iwfm.compare(obs_sites,sim_sites)
    return sim_miss, obs_miss
