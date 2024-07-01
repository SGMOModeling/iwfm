# iwfm_read_rz.py 
# Read unsaturated zone parameters from a file and organize them into lists
# Copyright (C) 2023 University of California
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

def get_name(s):
    ''' get_name() - Read an IWFM Simulation Groundwater file and return
        a dictionary of sub-process file names, and arrays of parameters

    Parameters
    ----------
    s : str
        line from IWFM Simulation Groundwater file

    Returns
    -------
    name : string
        if file name: Groundwater sub-process file name
        if blank, 'none'
    '''

    temp = s.split()[0]
    if temp[0] == '/':   # check for presence of file name
        name = 'none'
    else:
        name = temp
    return name



def iwfm_read_uz(file, verbose=False):
    """iwfm_read_uz() - Read unsaturated zone data from a file and organize them into lists.

    Parameters
    ----------
    file : str
        The path of the file containing the urban land use data.
  
    verbose : bool, default = False
        If True, print status messages.

    Returns
    -------

    params : list
        A list of parameters: [perv, cnurb, icpopul, icwtruse, fracdm, iceturb, icrtfurb, icrufurb, icurbspec, ic]

    """
    import iwfm as iwfm
    import numpy as np

    uz_dict = {}

    if verbose: print(f"Entered iwfm_read_uz() with {file}")

    uz_lines = open(file).read().splitlines()                   # open and read input file
    uz_version = uz_lines[0].split()[0]                         # version number

    line_index = iwfm.skip_ahead(0, uz_lines, 0)                # skip to next value line
    layers = int(uz_lines[line_index].split()[0])               # number of layers

    line_index = iwfm.skip_ahead(line_index + 1, uz_lines, 0)   # skip to next value line
    uzconv = float(uz_lines[line_index].split()[0])             # convergence criteria

    line_index = iwfm.skip_ahead(line_index + 1, uz_lines, 0)   # skip to next value line
    itmax = int(uz_lines[line_index].split()[0])                # max iterations

    line_index = iwfm.skip_ahead(line_index + 1, uz_lines, 0)   # skip to next value line
    uz_dict['bud'] = get_name(uz_lines[line_index]) 

    line_index = iwfm.skip_ahead(line_index + 1, uz_lines, 0)   # skip to next value line
    uz_dict['zbud'] = get_name(uz_lines[line_index]) 

    line_index = iwfm.skip_ahead(line_index + 1, uz_lines, 0)   # skip to next value line
    uz_dict['fcond'] = get_name(uz_lines[line_index]) 

    line_index = iwfm.skip_ahead(line_index + 1, uz_lines, 0)   # skip to next value line
    ngroup = int(uz_lines[line_index].split()[0])               # number of parametric grid groups

    line_index = iwfm.skip_ahead(line_index + 1, uz_lines, 0)   # skip to next value line
    factors = [float(i) for i in uz_lines[line_index].split()]

    line_index = iwfm.skip_ahead(line_index + 1, uz_lines, 0)   # skip to next value line
    tunit = uz_lines[line_index].split()[0]                     # time unit for aquifer Kh

    if ngroup > 0:                                              # read parameter grid
        line_index = iwfm.skip_ahead(line_index, uz_lines, 1)   # skip to next value line

        nodes = int(uz_lines[line_index].split()[0])            # number of parametric grid nodes
        line_index = iwfm.skip_ahead(line_index, uz_lines, 1)   # skip to next value line
        nep = int(uz_lines[line_index].split()[0])              # number of parametric grid elements

        line_index = iwfm.skip_ahead(line_index, uz_lines, 1)   # skip to next value line

        # read parametric grid nodal data
        elems = []
        for i in range(nep):
            elems.append([int(i) for i in uz_lines[line_index].split()])
            line_index += 1

        # initialize parameter arrays
        elem_id = [0 for row in range(nodes)]
        x = [0 for row in range(nodes)]
        y = [0 for row in range(nodes)]
        pd = [[0 for col in range(layers)] for row in range(nodes)]
        pn = [[0 for col in range(layers)] for row in range(nodes)]
        pi = [[0 for col in range(layers)] for row in range(nodes)]
        pk = [[0 for col in range(layers)] for row in range(nodes)]
        prhc = [[0 for col in range(layers)] for row in range(nodes)]

        # read parameter values
        for node in range(nodes):
            for layer in range(layers):
                values = uz_lines[line_index].split()
                if layer == 0:
                    elem_id[node] = int(values.pop(0))
                    x[node] = int(values.pop(0))
                    y[node] = int(values.pop(0))
                pd[node][layer] = float(values[0])
                pn[node][layer] = float(values[1])
                pi[node][layer] = float(values[2])
                pk[node][layer] = float(values[3])
                prhc[node][layer] = float(values[4])
                line_index += 1

    else:                                                               # read parameter values
        line_index = iwfm.skip_ahead(line_index, uz_lines, 1)   # skip to next value line
        # how many elements?
        elems = 0
        while uz_lines[line_index + elems][0] != 'C':
            elems += 1

        # initialize parameter arrays
        elem_id = [0 for row in range(elems)]
        pd = [[0 for col in range(layers)] for row in range(elems)]
        pn = [[0 for col in range(layers)] for row in range(elems)]
        pi = [[0 for col in range(layers)] for row in range(elems)]
        pk = [[0 for col in range(layers)] for row in range(elems)]
        prhc = [[0 for col in range(layers)] for row in range(elems)]

        # read parameter values
        for elem in range(elems):
            values = uz_lines[line_index].split()

            elem_id[elem] = int(values[0])
            for layer in range(layers):
                pd[elem][layer] = float(values[1 + (layer * 5)])
                pn[elem][layer] = float(values[2 + (layer * 5)])
                pi[elem][layer] = float(values[3 + (layer * 5)])
                pk[elem][layer] = float(values[4 + (layer * 5)])
                prhc[elem][layer] = float(values[5 + (layer * 5)])
            line_index += 1

    # how many elements?
    line_index = iwfm.skip_ahead(line_index, uz_lines, 0)   # skip to next value line
    ne = 0
    while len(uz_lines[line_index + ne]) > 2 and uz_lines[line_index + ne][0] != 'C':
        ne += 1
        #print(f' ==> {ne=}\t{uz_lines[line_index + ne]=}\t{len(uz_lines[line_index + ne])=}')

    # initial condition
    ic, line_index = read_param_table_floats(uz_lines, line_index, ne)

    params = [pd, pn, pi, pk, prhc, ic]

        
    if verbose: print(f"Leaving iwfm_read_uz()")

    return uz_dict, params
