# draw_plot.py
# Creates a PDF file with a graph of the simulated data vs time for all
# hydrographs as lines, with observed values vs time as dots, saved as the well_name.pdf
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


def draw_plot( well_name, date, meas, no_hyds, gwhyd_obs, gwhyd_name, well_info,
    start_date, title_words, yaxis_width=-1):
    ''' draw_plot() - Creates a PDF file with a graph of the simulated data vs time
        for all hydrographs as lines, with observed values vs time as dots, saved 
        as the well_name.pdf

    Parameters
    ----------
    well_name : str
        Well name, often state well number
    
    date : list
        list of dates (paired with meas)
    
    meas : list
        list of observed values (paired with date)
    
    no_hyds : int
        number of simulation time series to be graphed
    
    gwhyd_obs : list
        simulated IWFM groundwater hydrographs 
        [0]==dates, [1 to no_hyds]==datasets
    
    gwhyd_name : list
        hydrograph names from PEST observations file
    
    well_dict : dict
        key = well name, value = well data from Groundwater.dat file
    
    start_date : str
        first date in simulation hydrograph files
    
    title_words : str
        plot title words
    
    yaxis_width : int, default=-1
        minimum y-axis width, -1 for automatic
    
    Return
    ------
    nothing

    '''
    import iwfm as iwfm
    import datetime
    import matplotlib

    # Force matplotlib to not use any Xwindows backend.
    matplotlib.use('TkAgg')  # Set to TkAgg ...
    matplotlib.use('Agg')  # ... then reset to Agg
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    line_colors = [
        'r-',
        'g-',
        'c-',
        'y-',
        'b-',
        'm-',
        'k-',
        'r--',
        'g--',
        'c--',
        'y--',
        'b--',
        'm--',
        'k--',
        'r:',
        'g:',
        'c:',
        'y:',
        'b:',
        'm:',
        'k:',
    ]
    # 'r-' = red line, 'bo' = blue dots, 'r--' = red dashes, 
    # 'r:' = red dotted line, 'bs' = blue squares, 'g^' = green triangles, etc

    col = well_info[0]  # gather information

    # each hydrograph in gwhyd_obs has dates in the first column
    # convert the observed values and each set of simulated values to a pair of
    # lists, with 'date, meas' format.
    ymin, ymax = 1e6, -1e6
    sim_heads, sim_dates = [], []
    for j in range(0, no_hyds):
        date_temp, sim_temp = [], []
        for i in range(0, len(gwhyd_obs[j])):
            date_temp.append(datetime.datetime.strptime(gwhyd_obs[j][i][0], '%m/%d/%Y'))
            sim_temp.append(gwhyd_obs[j][i][col])
            ymin = min(ymin, gwhyd_obs[j][i][col])
            ymax = max(ymax, gwhyd_obs[j][i][col])
        sim_dates.append(date_temp)
        sim_heads.append(sim_temp)

    for i in range(0, len(meas)):
        ymin = min(ymin, meas[i])
        ymax = max(ymax, meas[i])

    meas_dates = []
    for i in range(0, len(date)):
        meas_dates.append(datetime.datetime.strptime(date[i], '%m/%d/%Y'))

    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    yearsFmt = mdates.DateFormatter('%Y')

    # plot simulated vs sim_dates as line, and meas vs specific dates as points, on one plot
    with PdfPages(well_name + '_' + iwfm.pad_front(col, 4, '0') + '.pdf') as pdf:
        fig = plt.figure(figsize=(10, 7.5))
        ax = plt.subplot(111)
        ax.xaxis_date()
        plt.grid(linestyle='dashed')
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)
        ax.xaxis.set_minor_locator(years)
        plt.xlabel('Date')
        plt.ylabel('Head (ft msl)')
        plt.title(
            title_words + ': ' + well_name.upper() + ' Layer ' + str(well_info[3])
        )
        plt.plot(meas_dates, meas, 'bo', label='Observed')

        # minimum y axis width was set by user, so check and set if necessary
        if yaxis_width > 0:
            if ymax > ymin:
                if ymax - ymin < yaxis_width:  # set minimum and maximum values
                    center = (ymax - ymin) / 2 + ymin
                    plt.ylim(center - yaxis_width / 2, center + yaxis_width / 2)

        for j in range(0, no_hyds):
            plt.plot(sim_dates[j], sim_heads[j], line_colors[j], label=gwhyd_name[j])

        leg = ax.legend(frameon=1, facecolor='white')
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()
    return 
