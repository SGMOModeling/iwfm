# iwfm_read_et_vals.py 
# Read evapotranspiration values from a file and organize them into lists
# Copyright (C) 2023-2024 University of California
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

def read_param_table_ints(file_lines, line_index, lines):
    """read_param_table_ints() - Read a table of integer parameters from a file and organize them into lists.

    Parameters
    ----------
    file_lines : list
        File contents as list of lines

    line_index : int
        The index of the line to start reading from.

    lines : int
        The number of lines to read.
  
    Returns
    -------

    params : list
        A list of parameters
    """

    import iwfm as iwfm 

    params = []
    if int(file_lines[line_index].split()[0]) == 0:                  # one set of parameter values for all elements
        params = [int(e) for e in file_lines[line_index].split()]
    else:
        for i in range(lines):
            t = [int(e) for e in file_lines[line_index].split()]
            params.append(t)
            line_index += 1

    return params, line_index

def read_param_table_floats(file_lines, line_index, lines):
    """read_param_table_floats() - Read a table of integer parameters from a file and organize them into lists.

    Parameters
    ----------
    file_lines : list
        File contents as list of lines

    line_index : int
        The index of the line to start reading from.

    lines : int
        The number of lines to read.
  
    Returns
    -------

    params : list
        A list of parameters
    """

    import iwfm as iwfm 

    params = []
    if int(file_lines[line_index].split()[0]) == 0:                  # one set of parameter values for all elements
        params = [float(e) for e in file_lines[line_index].split()]
        params[0] = int(params[0])
        line_index = iwfm.skip_ahead(line_index + 1, file_lines, 0)  # skip to next value line
    else:
        for i in range(lines):
            t = [float(e) for e in file_lines[line_index].split()]
#            print(f' *** {t=}')
            t[0] = int(t[0])
            params.append(t)
            line_index += 1                                         # skip to next line
    line_index -= 1

    return params, line_index


def iwfm_read_et_vals(file, verbose=False):
    """iwfm_read_et_vals() - Read evapotranspiration from a file and organize them into lists.

    Parameters
    ----------
    file : str
        The path of the file containing the evapotranspiration data.
  
    verbose : bool, default = False
        If True, print status messages.

    Returns
    -------

    params : list
        A list of evapotranspiration values

    """
    import iwfm as iwfm

    if verbose: print(f"Entered iwfm_read_et_vals() with {file}")

    et_lines = open(file).read().splitlines()                   # open and read input file

    line_index = iwfm.skip_ahead(0, et_lines, 0)                # skip to next value line
    nevap = int(et_lines[line_index].split()[0])                # number of columns

    line_index = iwfm.skip_ahead(line_index + 1, et_lines, 0)   # skip to next value line
    factet = float(et_lines[line_index].split()[0])             # conversion factor

    line_index = iwfm.skip_ahead(line_index + 1, et_lines, 0)   # skip to next value line
    nspet = int(et_lines[line_index].split()[0])                # number of timesteps to update et data

    line_index = iwfm.skip_ahead(line_index + 1, et_lines, 0)   # skip to next value line
    nfqet = int(et_lines[line_index].split()[0])                # repetition requency of et data

    line_index = iwfm.skip_ahead(line_index + 1, et_lines, 0)   # skip to next value line
    dssfl = et_lines[line_index].split()[0]                     # dss file name

    line_index = iwfm.skip_ahead(line_index + 1, et_lines, 0)   # skip to next value line

    # evapotranspiration data
    et = []
    while line_index < len(et_lines) and len(et_lines[line_index]) > 10:
        t = et_lines[line_index].split()
        for i in range(1,nevap):
            t[i] = float(t[i])
        et.append(t)
        line_index += 1

    params = et

        
    if verbose: print(f"Leaving iwfm_read_et_vals()")

    return params
