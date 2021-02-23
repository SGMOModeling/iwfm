# iwfm_read_preproc.py
# read IWFM preprocessor main file and return dictionary of file names
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


def iwfm_read_preproc(pre_file):
    """Function iwfm_read_prepcoc(pre_file,debug = 0) reads an IWFM Preprocessor
    main input file, and returns a list of the files called and some settings.

    Parameters:
      pre_file        (str):  Name of existing preprocessor main input file

    Returns:
      pre_dict       (dict):  Dictionary of preprocessor file names
      have_lake      (bool):  Does the existing model have a lake file?

    """
    import iwfm as iwfm

    # -- read the preprocessor file into array pre_lines
    pre_lines = open(pre_file).read().splitlines()  # open and read input file

    line_index = iwfm.skip_ahead(0, pre_lines, 3)  # skip comments

    # -- read input file names and create a dictionary ------------------
    pre_dict = {}
    pre_dict['preout'] = pre_lines[line_index].split()[0]  # preproc output file

    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0)  # skip comments
    pre_dict['elem_file'] = pre_lines[line_index].split()[0]  # element file

    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0)  # skip comments
    pre_dict['node_file'] = pre_lines[line_index].split()[0]  # node file

    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0)  # skip comments
    pre_dict['strat_file'] = pre_lines[line_index].split()[0]  # stratigraphy file

    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0)  # skip comments
    pre_dict['stream_file'] = pre_lines[line_index].split()[0]  # stream file

    line_index = iwfm.skip_ahead(line_index + 1, pre_lines, 0)  # skip comments
    lake_file = pre_lines[line_index].split()[0]  # lake file
    # -- is there a lake file?
    have_lake = True
    if lake_file[0] == '/':
        lake_file = ''
        have_lake = False
    pre_dict['lake_file'] = lake_file

    return pre_dict, have_lake
