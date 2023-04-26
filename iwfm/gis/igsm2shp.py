# igsm2shp.py
# Create shapefiles for an IGSM model
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


def igsm2shp(main_file, shape_name, verbose=False):
    ''' igsm2shp() - Read the names of the preprocessor component input files, 
        read the contents of these files, and create node, element, stream 
        node and stream reach shapefiles

    Parameters
    ----------
    main_file : str
        IGSM Preprocessor input file name
    
    shape_name : str
        output shapefiles base name

    Returns
    -------
    nothing

    '''

    import iwfm as iwfm
    import iwfm.gis as gis

    # read main_file for file names
    main_lines = open(main_file).read().splitlines()
    line_index = iwfm.skip_ahead(0, main_lines, 6)
    elem_file = main_lines[line_index].split()[0]
    line_index += 1
    node_file = main_lines[line_index].split()[0]
    line_index += 1
    strat_file = main_lines[line_index].split()[0]
    line_index += 1
    stream_file = main_lines[line_index].split()[0]
    line_index += 1
    lake_file = main_lines[line_index].split()[0]
    if lake_file[0] == '/': # no lake file listed
        lake_file = ''
    line_index += 2
    char_file = main_lines[line_index].split()[0]

    iwfm.file_test(elem_file)
    iwfm.file_test(node_file)
    iwfm.file_test(strat_file)
    iwfm.file_test(stream_file)
    if len(lake_file) > 1:
        iwfm.file_test(lake_file)
    iwfm.file_test(char_file)


    elem_nodes, elem_list = iwfm.igsm_read_elements(elem_file)
    if verbose:
        print(f'  Read nodes of {len(elem_nodes):,} elements from {elem_file}')

    node_coords, node_list = iwfm.igsm_read_nodes(node_file)
    if verbose:
        print(f'  Read coordinates of {len(node_coords):,} nodes from {node_file}')

    elem_char = iwfm.igsm_read_chars(char_file, elem_nodes)
    if verbose:
        print(f'  Read characteristics for {len(elem_char):,} elements from {char_file}')

    node_strat, nlayers = iwfm.igsm_read_strat(strat_file, node_coords)
    if verbose:
        print(f'  Read stratigraphy for {len(node_strat):,} nodes from {strat_file}')

    if len(lake_file) > 1:
        lake_elems, lakes = iwfm.igsm_read_lake(lake_file)
        if verbose:
            if len(lakes) > 1:
                print(f'  Read info for {len(lakes):,} lakes from {lake_file}')
            elif len(lakes) == 1:
                print(f'  Read info for {len(lakes):,} lake from {lake_file}')
    else:
        lake_elems = [[0,0,0]]
        if verbose:
            print('  No lakes')

    reach_list, stnodes_dict, nsnodes = iwfm.igsm_read_streams(stream_file)
    if verbose:
        print(f'  Read info for {len(reach_list):,} stream reaches and {nsnodes:,} stream nodes from {stream_file}\n')


    gis.nodes2shp(node_coords, node_strat, nlayers, shape_name, verbose=verbose)

    gis.igsm_elem2shp(elem_nodes,node_coords,elem_char,lake_elems,
        shape_name,verbose=verbose)

    gis.snodes2shp(nsnodes, stnodes_dict, node_coords, shape_name, verbose=verbose)

    gis.reach2shp(reach_list, stnodes_dict, node_coords, shape_name, verbose=verbose)

    if verbose:
        print('  Wrote node, element, stream node and stream reache shapefiles\n')

    return


if __name__ == "__main__":
    ''' Run igsm2shp() from command line '''
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        input_file = sys.argv[1]
        output_basename = sys.argv[2]
    else:  # ask for file names from terminal
        input_file = input('IGSM Preprocessor main file name: ')
        output_basename = input('Output shapefile basename: ')

    iwfm.file_test(input_file)

    idb.exe_time()  # initialize timer
    igsm2shp(input_file, output_basename, verbose=True)

    idb.exe_time()  # print elapsed time
