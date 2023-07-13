# fac2iwfm.py
# Transfer parameter values from pilot points to model nodes
# Copyright (C) 2020-2023 University of California
# from fac2reali.f90 by M Tonkin, SSPA
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

def fac2iwfm(pp_file_name, param_file_name, save_name, rlow=0, rhigh=1000000, empty=-999, verbose=False):
    ''' fac2iwfm() - Transfer parameter values from pilot points to model nodes
        from fac2reali.f90 by M Tonkin

    Parameters
    ----------
    pp_file_name : str
        File of pilot point factors for nodes

    param_file_name : str
        File with parameter values at pilot points

    save_name : str
        Name of output file

    rlow : float, default=0
        Lower inerppolation threshold value

    rhigh : float, default=1000000
        Upper interpolation threshold value

    empth : float, default=-999
        Nodal parameter value if no pilot point value

    Returns
    -------
    count : int
        Number of PDFs combined

    '''

    import iwfm as iwfm
    if verbose:
        print('\n FAC2IWFM carries out spatial parameter interpolation to IWFM 2015 node')
        print(' locations using interpolation factors calculated by PPK2FACI and ')
        print(' pilot point values contained in a pilot points file.')
    
    iwfm.file_test(pp_file_name)
    pp_file_lines = open(pp_file_name).read().splitlines()
    if verbose: print(f'\n Read {pp_file_name}')
 
    no_nodes = int(pp_file_lines[1])            # number of model nodes
    no_ppts  = int(pp_file_lines[2])            # number of pilot points
    
    # put pilot point allocation factors into list
    pp_factors = pp_file_lines[(no_ppts + 3):(no_ppts + no_nodes + 3)]


    # read parameter values at pilot points into a dictionary
    iwfm.file_test(param_file_name)
    param_file_lines = open(param_file_name).read().splitlines()
    if verbose: print(f' Read {param_file_name}')
    pp_params, i = {}, 0
    for line in param_file_lines:
        items = line.split()
        i += 1
        pp_params[i] = [items[4]]              # dictionary key: pp_name, values: x, y, layer, param_value


    # parse the spatial interpolation factors 
    with open(save_name, 'w') as f:
        for item in pp_factors:
            item = item.split()
            node, na, pval = int(item[0]), int(item[2]), 0
            for i in range(0, na):
                pp, factor = int(item[4 + i * 2]), float(item[4 + i * 2 + 1])
                pval += float(pp_params[pp][0]) * factor
            f.write(f' node:            {node} value:  {round(pval,3)}\n')
    if verbose: print(f' Wrote nodal parameter values to  {save_name}')


if __name__ == "__main__":
    ''' Run fac2iwfm() from command line '''
    import sys
    import iwfm.debug as idb

    # read arguments from command line
    if len(sys.argv) > 1:  # arguments are listed on the command line
        pp_file_name     = sys.argv[1]         # Pilot point interpolation factor file name
        param_file_name  = sys.argv[2]         # Parameter values file name
        save_name        = sys.argv[3]         # Output file name
        rlow             = sys.argv[4]         # Lower interpolation limit
        rhigh            = sys.argv[5]         # Upper interpolation limit
        empty            = sys.argv[6]         # Default value for nodes with no parameter value

    else:  # get everything form the command line
        pp_file_name     = input('Pilot point interpolation factor file name: ')
        param_file_name  = input('Parameter values file name: ')
        save_name        = input('Output file name: ')
        rlow             = input('Lower interpolation limit: ')
        rhigh            = input('Upper interpolation limit: ')
        empty            = input('Default value for nodes with no parameter value: ')
    rlow, rhigh, empty = float(rlow), float(rhigh), float(empty)

    idb.exe_time()  # initialize timer

    fac2iwfm(pp_file_name, param_file_name, save_name, rlow, rhigh, empty,verbose=True)

    print('\n')
    idb.exe_time()  # print elapsed time

