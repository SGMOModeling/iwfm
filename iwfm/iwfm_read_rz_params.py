# iwfm_read_rz_params.py 
# Read root zone parameters from a file and organize them into lists
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

def iwfm_read_rz_params(rz_file, verbose=False):
    """iwfm_read_rz_params() - Read root zone parameters from a file and organize them into lists.

    Parameters
    ----------
    rz_file : str
        The path of the file containing the root zone data.
  
    verbose : bool, default = False
        If True, print status messages.

    Returns
    -------
    params : list
        A list containing parameter values. It consists of 13 sublists, each representing a different parameter.

    """

    import iwfm as iwfm

    if verbose: print(f"  Entered iwfm_read_rz_params() with {rz_file=}")

    rz_lines = open(rz_file).read().splitlines()                # open and read input file

    line_index = iwfm.skip_ahead(0, rz_lines, 18)               # skip four parameters and 15 file names
    factk = float(rz_lines[line_index].split()[0])              # K multiplier

    line_index = iwfm.skip_ahead(line_index + 1, rz_lines, 0) 
    factcp = float(rz_lines[line_index].split()[0])             # capillary rise multiplier

    line_index = iwfm.skip_ahead(line_index + 1, rz_lines, 0) 
    tkunit = rz_lines[line_index].split()[0]                    # K time unit

    line_index = iwfm.skip_ahead(line_index + 1, rz_lines, 0) 

    #  Lists for each parameter
    params = [[], [], [], [], [], [], [], [], [], [], [], [], []]
   
    #  Read the relevant lines of the RootZone.dat file
    lines = rz_lines[line_index:]                        #  The remaining lines contain the parameters

    #  Loop through all of the lines
    for values in lines:
        values = values.split()                         #  Split the line into individual values
        values = values[1:]
        #  Add values to their corresponding parameter's list
        for idx, value in enumerate(values[0:13]):
            if idx == 4:
                value = float(value) * factk
            elif idx == 6:
                value = float(value) * factcp
            params[idx].append(float(value))
    
    if verbose: print(f"  Leaving iwfm_read_rz_params()")

    return params

