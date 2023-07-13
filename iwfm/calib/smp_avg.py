# smp_avg.py
# read an smp file and average the observations values for
# each observation ID, then write out with the average value
# replacing the original observation value
# Based on getaverages.f90 from PEST-IEFM Tools
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


def smp_avg( smp_file, verbose=False):
    ''' smp_avg() - read an smp file and average the observations values for
        each observation ID

    Parameters
    ----------
    smp_file : str
        Name of input smp file

    verbose : bool, default = False
        Print to screen?

    Returns
    -------
    averages: list of smp-format strings
        

    '''

    import iwfm as iwfm

    iwfm.file_test(smp_file)

    smp_lines = open(smp_file).read().splitlines()
    if verbose: print(f'\n  Read {len(smp_lines):,} lines from {smp_file}')

    sites = []
    # [site_name, value_sum, value_count]
    for line in smp_lines:
        items = line.split()
        site_name, value = items[0], float(items[3])

        index = name_index(sites, site_name)

        if len(index) == 0:
            sites.append([site_name,items[1],value,1])
        else:
            sites[index[0]][2] += value
            sites[index[0]][3] += 1

    averages = []
    for line in smp_lines:
        items = line.split()
        site_name = items[0]
        index = name_index(sites, site_name)

        # get average for this site
        average = sites[index[0]][2]/sites[index[0]][3]

        smp_out = str(f'{iwfm.pad_back(items[0],20)} {items[1]}  0:00:00 {iwfm.pad_front(round(average,4),22)}')
        averages.append(smp_out)

    return averages

def name_index(names_list, name):
    index = []
    for i, item in enumerate(names_list):
        if name in item:
            index.append(i)
    return index

if __name__ == "__main__":
    ''' Run smp_avg() from command line '''
    import sys
    import iwfm.debug as idb

    # read arguments from command line
    if len(sys.argv) > 1:  # arguments are listed on the command line
        smp_file  = sys.argv[1]         # Name of imput SMP file
        save_name = sys.argv[2]         # Name of output file

    else:  # get everything form the command line
        smp_file = input('Input SMP file name: ')
        save_name = input('Output file name: ')

    idb.exe_time()  # initialize timer
    averages = smp_avg(smp_file, verbose=True)

    with open(save_name, 'w') as f:
        for item in averages:
            f.write(f'{item}\n')
    print(f'  Wrote {len(averages):,} values to  {save_name}')

    idb.exe_time()  # print elapsed time

