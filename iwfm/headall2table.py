# headall2table.py
# Read headall.out file and write results for one date toa table
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


def headall2table(heads_file, output_file, out_date):
    ''' headall2table() - Read IWFM headall.out file and write results
        for one date to a table

    Parameters
    ----------
    heads_file : str
        IWFM headall.out file name
    
    output_file : str
        name of output file
    
    out_date : str
        date to process, mm/dd/yyyy format

    Returns
    -------
    nothing

    '''
    import numpy as np
    import pandas as pd
    import iwfm as iwfm

    out_mon = iwfm.month(out_date)
    out_day = iwfm.day(out_date)
    out_year = iwfm.year(out_date)

    file_lines = open(heads_file).read().splitlines()  # open and read input file

    start = 5  # skip the first 5 lines
    line = start
    nodes = file_lines[line].split()  # read line w/node nos
    nodes.pop(0)  # remove text
    nodes.pop(0)  # remove text

    data = []
    data.append(nodes)

    line += 1
    item = file_lines[line].split()  # read line w/date
    data.append(item)
    end_date = item.pop(0)  # remove the date
    
    while line < len(file_lines) - 1:
        line += 1
        layer = 1
        header = []
        header.append('Node')
        header.append('Layer ' + str(layer))
        while file_lines[line][0].isspace():  # get all the lines for this time step
            item = file_lines[line].split()
            data.append(item)
            layer += 1
            header.append('Layer ' + str(layer))
            line += 1
        # now check the date
        m = iwfm.month(end_date[0:10])
        d = iwfm.day(end_date[0:10])
        y = iwfm.year(end_date[0:10])
        if m == out_mon and d == out_day and y == out_year:
            out_table = np.asarray(data)
            df = pd.DataFrame(np.transpose(out_table))
            df.to_csv(output_file, header=header, index=False)
            return
        else:
            data = []
            data.append(nodes)
            item = file_lines[line].split()  # read line w/date
            data.append(item)
            end_date = item.pop(0)  # remove the date

    return


if __name__ == '__main__':
    ' Run headall2table() from command line '
    import sys
    import os
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        heads_file = sys.argv[1]
        output_file = sys.argv[2]
        out_date = sys.argv[3]
    else:  # ask for file names from terminal
        heads_file  = input('IWFM Headall file name: ')
        output_file = input('Output file name: ')
        out_date    = input('Output date: ')

    iwfm.file_test(heads_file)

    idb.exe_time()  # initialize timer
    headall2table(heads_file, output_file, out_date)

    print(f'  Read {heads_file} and wrote {output_file}.')  # update cli
    idb.exe_time()  # print elapsed time
