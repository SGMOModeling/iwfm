# gw_plot_noobs.py
# Create PDF files for simulated data vs time for all hydrographs as lines
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


def gw_plot_noobs(well_list,no_hyds,gwhyd_sim,gwhyd_names,well_dict,titlewords,yaxis_width):
    """ gw_plot_noobs() - Create PDF files for simulated data vs time for 
        all hydrographs as lines

    Parameters:
      well_list       (list): List of well names
      no_hyds         (int):  Number of simulation time series to be graphed
      gwhyd_sim       (list): Simulated IWFM groundwater hydrographs 
                                ([0]==dates, [1 to no_hyds]==datasets)
      gwhyd_names     (list): Hydrograph names from PEST observations file
      well_dict       (dict): Dictionary of well data from Groundwater.dat file
      title_words     (str):  Plot title words
      yaxis_width     (int):  Minimum y-axis width, -1 for automatic
    
    Return:
      count           (int):  Number of files produced
    """
    import iwfm as iwfm
    # cycle through the list of wells in obs to print plots
    # initialize
    i, count, date, meas = 1, 0, [], []
    date.append(gwhyd_sim[0][0][0])
    name = well_list[0]

    start_date = gwhyd_sim[0][0][0]  # get starting date
    for j in range(1, len(well_list)):  # move through the file
        if name in well_dict:  # draw and save the current plot
            iwfm.gw_plot_noobs_draw(name,date,no_hyds,gwhyd_sim,gwhyd_names,well_dict.get(name),start_date,titlewords,yaxis_width)
            count += 1
            # re-initialize for next observation well
            date, name = [], well_list[j]
        date.append(gwhyd_sim[j][0][0])
    # make the last one
    if name in well_dict:
        iwfm.gw_plot_noobs_draw(name,date,no_hyds,gwhyd_sim,gwhyd_names,well_dict.get(name),start_date,titlewords,yaxis_width)
        count += 1
    return count
