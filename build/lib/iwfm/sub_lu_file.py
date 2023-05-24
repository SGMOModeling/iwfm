# sub_lu_file.py
# Copy original land use input file, remove the elements that are not in the
# submodel, and write out the new file
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


def sub_lu_file(in_filename, out_filename, elems, verbose=False):
    ''' sub_lu_file() - Copy original land use input file, 
        remove the elements that are not in the submodel, 
        and write out the new file

    Parameters
    ----------
    in_filename : str
        name of existing land use file
    
    out_filename : str
        name of new land use file
    
    elems : list of ints
        list of existing model elements in submodel

    verbose : bool, default=False
        turn command-line output on or off

    Returns:
    nothing

    '''
    import iwfm as iwfm

    # -- read the land use file into array lu_lines
    lu_lines = open(in_filename).read().splitlines()  # open and read input file

    line_index = iwfm.skip_ahead(0, lu_lines, 4)  # skip comments

    # read the land use data into lists
    lu_table, lu_dates, lu_elems = iwfm.read_lu_file(in_filename)

    lu_elems = lu_elems[0]

    # remove data for elements that are not in the submodel
    for row in reversed(range(len(lu_table[0]))):
        if int(lu_elems[row]) not in elems:
            del lu_elems[row]
            for t in range(len(lu_table)):
                del lu_table[t][row]

    for i in range(len(lu_table)):
        # convert lu_table list entry to output format
        table_data = ''
        for t in lu_table[i][0]:
            table_data = table_data + str(t) + '\t'
        lu_lines[line_index] = lu_dates[i] + '\t' + str(lu_elems[0]) + '\t' + table_data
        line_index += 1

        for j in range(1, len(lu_elems)): 
            # convert lu_table list entry to output format
            table_data = ''
            for t in lu_table[i][j]:
                table_data = table_data + str(t) + '\t'
            lu_lines[line_index] = '\t' + str(lu_elems[j]) + '\t' + table_data
            line_index += 1

    del lu_lines[line_index:]
    lu_lines.append('')

    # -- write new preprocessor input file
    with open(out_filename, 'w') as outfile:
        outfile.write('\n'.join(lu_lines))

    if verbose:                
        print(f'      Wrote submodel land use area file {out_filename}')

    return





if __name__ == "__main__":
    ''' Run sub_lu_file() from command line '''
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    verbose = True

    if len(sys.argv) > 1:               # arguments are listed on the command line
        in_filename     = sys.argv[1]   # original land use file
        out_filename    = sys.argv[2]   # submodel land use file name
        elem_pairs_file = sys.argv[3]   # submodel elements
    else:  # ask for file names from terminal
        in_filename      = input('Existing land use file name: ')
        out_filename     = input('Submodel land use file name: ')
        elem_pairs_file  = input('Submodel elements file name: ')

    # == test that the input files exist
    iwfm.file_test(in_filename)
    iwfm.file_test(elem_pairs_file)

    sub_elem_list, *temp = iwfm.get_elem_list(elem_pairs_file)

    idb.exe_time()  # initialize timer
    sub_lu_file(in_filename, out_filename, sub_elem_list)

    if verbose:
        print(' ')
        print(f'  Created submodel land use file {out_filename} from {in_filename}.')
    idb.exe_time()  # print elapsed time
