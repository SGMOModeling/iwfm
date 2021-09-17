# write_results.py
# Writes simulated and observed values for one observation well to a text file
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


def write_results(name, date, meas, sim, start_date):
    ''' write_results() - Write simulated and observed values for one 
        observation well to a text file

    Parameters
    ----------
    name : str
        name of output file
    
    date : list
        dates corresponding to measured values
    
    meas : list of floats
        measured values
    
    sim : list of floats
        simulated equivalents to measured values
    
    start_date : str
        date in MM/DD/YYYY format

    Returns
    -------
    nothing
    
    '''
    import iwfm as iwfm

    output_filename = name + '_obs.out'
    with open(output_filename, 'w') as output_file:
        output_file.write(f'# Observations for well {name}\n')
        output_file.write('# Date\tObserved\tModeled\n')
        for i in range(0, len(date)):
            output_file.write(f'{iwfm.date_index(int(date[i]),start_date)}'+
                f'\t{meas[i]}\t{sim[i]}\n')
    return
