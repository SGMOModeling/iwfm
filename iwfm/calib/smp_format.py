# smp_format.py
# Read an smp file and reformat 
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


def smp_format( infile, nwidth=20, verbose=False):
    ''' smp_format() - Read an smp file and reformat 

    Parameters
    ----------
    infile : str
        Name of input smp file

    nwidth : int; default=14
        width of name field in characters
        
    verbose : bool, default = False
        Print to screen?

    Returns
    -------
    out_lines : list
        reformatted smp file contents

    '''

    import iwfm as iwfm

    iwfm.file_test(infile)

    smp_lines = open(infile).read().splitlines()
    if verbose: print(f'\n  Read {len(smp_lines):,} lines from {infile}')

    out_lines = []
    for line in smp_lines:
        items = line.split()
        name = iwfm.pad_back(items[0],nwidth)   # first field
        date = items[1].split('/')
        for i in range(len(date)):
            date[i] = int(date[i])
        date = iwfm.date2text(date[0],date[1],date[2])        # convert date from text m/d/yy to mm/dd/yyyy
        smp_out = str(f'{iwfm.pad_back(items[0],nwidth)} {date}  0:00:00 {items[3]}')
        out_lines.append(smp_out)

    return out_lines

if __name__ == "__main__":
    ''' Run smp2smp() from command line '''
    import sys
    import iwfm.debug as idb

    # read arguments from command line
    if len(sys.argv) > 1:  # arguments are listed on the command line
        smp_file  = sys.argv[1]         # Name of imput SMP file
        save_name = sys.argv[2]         # Name of output file

    else:  # get everything form the command line
        smp_file = input('Input SMP file name: ')
        save_name = input('Output SMP file name: ')

    idb.exe_time()  # initialize timer
    smp_out = smp_format(smp_file, verbose=True)

    with open(save_name, 'w') as f:
        for item in smp_out:
            f.write(f'{item}\n')
    print(f'  Wrote {len(smp_out):,} values to  {save_name}')

    idb.exe_time()  # print elapsed time

