# sub_unsat_file.py
# Copies the old node file and replaces the contents with those of the new
# submodel, and writes out the new file
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


def sub_unsat_file(old_filename, new_filename, elem_list, verbose=False):
    '''sub_unsat_file() - Read the original unsaturated zone file, determine 
        which elements are in the submodel, and write out a new file

    Parameters
    ----------
    old_filename : str
        name of existing model unsaturated zone file

    new_filename : str
        name of new subnmodel unsaturated zone file

    elem_list : list of ints
        list of existing model elements in submodel

    verbose : bool, default=False
        turn command-line output on or off

    Returns
    -------
    nothing

    '''
    import iwfm as iwfm

    comments = ['Cc*#']
    elems = []
    for e in elem_list:
        elems.append(e[0])

    unsat_lines = open(old_filename).read().splitlines()  
    unsat_lines.append('')

    line_index = iwfm.skip_ahead(0, unsat_lines, 9)  # skip factors and comments

    while line_index < len(unsat_lines):
        if (
            len(unsat_lines[line_index]) > 1
            and unsat_lines[line_index][0] not in comments
        ):
            if int(unsat_lines[line_index].split()[0]) not in elems:  # remove the line
                del unsat_lines[line_index]
                line_index -= 1
        line_index += 1

    unsat_lines.append('')

    with open(new_filename, 'w') as outfile:
        outfile.write('\n'.join(unsat_lines))

    return
